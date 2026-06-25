#!/usr/bin/env python3
"""Append and write date-organized AI coding daily notes."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
from typing import Iterable
import uuid


UNREPORTED_VALUES = {"", "no", "false", "pending", "unreported"}
CONFIG_ENV = "AI_CODING_DAILY_CONFIG"
FORMAT_ENV = "AI_CODING_DAILY_FORMAT"
REPORT_FORMATS = {"md", "txt"}


def config_path() -> Path:
    env_path = os.environ.get(CONFIG_ENV)
    if env_path:
        return Path(env_path).expanduser()
    return Path("~/.config/ai-coding-daily/config.json").expanduser()


def load_config() -> dict[str, str]:
    path = config_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid config file: {path}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid config file: {path}")
    return {str(key): str(value) for key, value in data.items()}


def normalize_report_format(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower().lstrip(".")
    if normalized not in REPORT_FORMATS:
        raise SystemExit("Report format must be 'md' or 'txt'")
    return normalized


def save_config(root: Path, report_format: str) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "root": str(root.expanduser()),
        "report_format": normalize_report_format(report_format),
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def resolve_root(args: argparse.Namespace | None = None) -> Path:
    if args and getattr(args, "root", None):
        return Path(args.root).expanduser()

    env_root = os.environ.get("AI_CODING_DAILY_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    configured_root = load_config().get("root")
    if configured_root:
        return Path(configured_root).expanduser()

    raise SystemExit(
        "Daily report root is required. Ask the user where to store AI coding "
        "daily documents, then run configure, pass --root, or set "
        "AI_CODING_DAILY_ROOT."
    )


def resolve_report_format(args: argparse.Namespace | None = None) -> str:
    if args and getattr(args, "format", None):
        return normalize_report_format(args.format) or "md"

    env_format = normalize_report_format(os.environ.get(FORMAT_ENV))
    if env_format:
        return env_format

    configured_format = normalize_report_format(load_config().get("report_format"))
    if configured_format:
        return configured_format

    raise SystemExit(
        "Daily report format is required. Ask the user whether reports should be "
        "txt or md, then run configure with --format, pass --format, or set "
        "AI_CODING_DAILY_FORMAT."
    )


def parse_date(value: str | None) -> dt.date:
    if not value:
        return dt.date.today()
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date {value!r}; expected YYYY-MM-DD") from exc


def record_dir(root: Path) -> Path:
    return root / "工作记录"


def diary_dir(root: Path) -> Path:
    return root / "日报"


def weekly_dir(root: Path) -> Path:
    return root / "周报"


def record_path(root: Path, day: dt.date) -> Path:
    return record_dir(root) / f"{day:%Y-%m-%d}.md"


def short_date_label(day: dt.date, include_year: bool = False) -> str:
    if include_year:
        return f"{day.year}.{day.month}.{day.day}"
    return f"{day.month}.{day.day}"


def parse_dates(value: str) -> list[dt.date]:
    dates = [parse_date(item.strip()) for item in value.split(",") if item.strip()]
    if not dates:
        raise SystemExit("--dates must include at least one YYYY-MM-DD value")
    return list(dict.fromkeys(dates))


def parse_selected_dates(args: argparse.Namespace) -> list[dt.date]:
    has_range = getattr(args, "start_date", None) or getattr(args, "end_date", None)
    has_date = getattr(args, "date", None)
    has_dates = getattr(args, "dates", None)

    selected_modes = sum(bool(value) for value in [has_date, has_range, has_dates])
    if selected_modes > 1:
        raise SystemExit("Use only one of --date, --dates, or --start-date/--end-date")

    if has_dates:
        return parse_dates(args.dates)

    if has_range:
        if getattr(args, "date", None):
            raise SystemExit("Use either --date or --start-date/--end-date, not both")
        if not args.start_date or not args.end_date:
            raise SystemExit("--start-date and --end-date must be used together")
        start = parse_date(args.start_date)
        end = parse_date(args.end_date)
        if start > end:
            raise SystemExit("--start-date must be on or before --end-date")
        return list(date_span(start, end))

    return [parse_date(getattr(args, "date", None))]


def date_span(start: dt.date, end: dt.date) -> Iterable[dt.date]:
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)


def is_contiguous(dates: list[dt.date]) -> bool:
    ordered = sorted(dates)
    return ordered == list(date_span(ordered[0], ordered[-1]))


def report_path(root: Path, dates: list[dt.date], report_format: str) -> Path:
    ordered = sorted(dates)
    include_year = len({day.year for day in ordered}) > 1
    suffix = normalize_report_format(report_format) or "md"

    if len(ordered) == 1:
        file_name = f"{short_date_label(ordered[0], include_year)} 日报.{suffix}"
        return diary_dir(root) / file_name

    if is_contiguous(ordered):
        label = (
            f"{short_date_label(ordered[0], include_year)}-"
            f"{short_date_label(ordered[-1], include_year)}"
        )
    else:
        label = "、".join(short_date_label(day, include_year) for day in ordered)

    return diary_dir(root) / f"{label} 日报.{suffix}"


def week_monday(day: dt.date) -> dt.date:
    return day - dt.timedelta(days=day.weekday())


def week_dates(day: dt.date) -> list[dt.date]:
    monday = week_monday(day)
    return [monday + dt.timedelta(days=offset) for offset in range(7)]


def weekly_report_path(root: Path, day: dt.date, report_format: str) -> Path:
    monday = week_monday(day)
    suffix = normalize_report_format(report_format) or "md"
    return weekly_dir(root) / f"{monday.year}-M{monday.month}-{monday:%Y%m%d}.{suffix}"


def clean_lines(values: Iterable[str] | None) -> list[str]:
    if not values:
        return []
    lines: list[str] = []
    for value in values:
        for line in value.splitlines():
            text = line.strip()
            if text:
                lines.append(text)
    return lines


def bullet_block(label: str, values: Iterable[str] | None) -> str:
    lines = clean_lines(values)
    if not lines:
        return ""
    rendered = "\n".join(f"  - {line}" for line in lines)
    return f"- {label}:\n{rendered}\n"


def split_activity(text: str) -> tuple[list[str], list[list[str]]]:
    header: list[str] = []
    blocks: list[list[str]] = []
    current: list[str] | None = None

    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            current = [line]
            blocks.append(current)
        elif current is None:
            header.append(line)
        else:
            current.append(line)

    return header, blocks


def reported_value(block: list[str], field: str = "Reported") -> str | None:
    for line in block:
        match = re.match(rf"- {re.escape(field)}:\s*(.*)", line)
        if match:
            return match.group(1).strip()
    return None


def is_unreported(block: list[str], field: str = "Reported") -> bool:
    value = reported_value(block, field)
    return value is None or value.lower() in UNREPORTED_VALUES


def render_activity(
    text: str, include_reported: bool, field: str = "Reported", empty_label: str = "unreported"
) -> str:
    header, blocks = split_activity(text)
    selected = [block for block in blocks if include_reported or is_unreported(block, field)]
    if not selected:
        return "".join(header).rstrip() + f"\n\n(no {empty_label} activity entries)\n"
    return "".join(header + [line for block in selected for line in block])


def mark_reported_text(
    text: str, report: Path, field: str = "Reported"
) -> tuple[str, int]:
    header, blocks = split_activity(text)
    changed_count = 0
    report_label = str(report)
    updated_blocks: list[list[str]] = []

    for block in blocks:
        if not is_unreported(block, field):
            updated_blocks.append(block)
            continue

        changed_count += 1
        updated = list(block)
        replaced = False
        for index, line in enumerate(updated):
            if line.startswith(f"- {field}:"):
                updated[index] = f"- {field}: {report_label}\n"
                replaced = True
                break

        if not replaced:
            insert_at = 1
            for index, line in enumerate(updated):
                if line.startswith("- Entry ID:") or line.startswith("- AI tool:"):
                    insert_at = index + 1
            updated.insert(insert_at, f"- {field}: {report_label}\n")

        updated_blocks.append(updated)

    return "".join(header + [line for block in updated_blocks for line in block]), changed_count


def append_entry(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    day = parse_date(args.date)
    record = record_path(root, day)
    record.parent.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now().strftime("%H:%M")
    entry_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    title = args.title.strip() if args.title else "AI coding session"
    tool = args.tool.strip() if args.tool else "Unknown"

    entry = [
        f"\n## {now} - {title}\n",
        f"- Entry ID: {entry_id}\n",
        "- Reported: no\n",
        "- Weekly Reported: no\n",
        f"- AI tool: {tool}\n",
    ]
    if args.project:
        entry.append(f"- Project: {args.project.strip()}\n")
    if args.source:
        entry.append(f"- Source: {args.source.strip()}\n")
    if args.tags:
        entry.append(f"- Tags: {', '.join(clean_lines(args.tags))}\n")

    entry.append(bullet_block("Demand/problem", args.demand))
    entry.append(bullet_block("Value", args.value))
    entry.append(bullet_block("Measurement", args.measure))
    entry.append(bullet_block("Progress", args.progress))
    entry.append(bullet_block("Efficiency", args.efficiency))
    entry.append(bullet_block("Completed", args.done))
    entry.append(bullet_block("TODO", args.todo))
    entry.append(bullet_block("Problems/thoughts", args.issue))

    note_lines = clean_lines(args.note)
    if note_lines:
        entry.append("- Notes:\n")
        entry.extend(f"  - {line}\n" for line in note_lines)

    if not record.exists():
        header = f"# AI coding activity - {day:%Y-%m-%d}\n"
        record.write_text(header, encoding="utf-8")

    with record.open("a", encoding="utf-8") as handle:
        handle.writelines(entry)

    print(record)


def show_day(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    report_format = resolve_report_format(args)
    dates = parse_selected_dates(args)
    print(f"report: {report_path(root, dates, report_format)}")
    for day in dates:
        record = record_path(root, day)
        print()
        print(f"record: {record}")
        print()
        if record.exists():
            print(render_activity(record.read_text(encoding="utf-8"), args.all))
        else:
            print("(no work record yet)")


def write_report(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    report_format = resolve_report_format(args)
    dates = parse_selected_dates(args)
    report = report_path(root, dates, report_format)
    report.parent.mkdir(parents=True, exist_ok=True)

    if args.from_file:
        text = Path(args.from_file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if not text:
        raise SystemExit("Refusing to write an empty report")

    report.write_text(text + "\n", encoding="utf-8")
    if not args.no_mark_reported:
        marked = 0
        for day in dates:
            record = record_path(root, day)
            if not record.exists():
                continue
            updated, changed_count = mark_reported_text(
                record.read_text(encoding="utf-8"), report
            )
            if changed_count:
                record.write_text(updated, encoding="utf-8")
                marked += changed_count
        print(f"marked_reported: {marked}")
    print(report)


def show_week(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    report_format = resolve_report_format(args)
    day = parse_date(args.date)
    print(f"weekly_report: {weekly_report_path(root, day, report_format)}")
    for record_day in week_dates(day):
        record = record_path(root, record_day)
        print()
        print(f"record: {record}")
        print()
        if record.exists():
            print(
                render_activity(
                    record.read_text(encoding="utf-8"),
                    args.all,
                    field="Weekly Reported",
                    empty_label="unreported weekly",
                )
            )
        else:
            print("(no work record yet)")


def write_weekly_report(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    report_format = resolve_report_format(args)
    day = parse_date(args.date)
    report = weekly_report_path(root, day, report_format)
    report.parent.mkdir(parents=True, exist_ok=True)

    if args.from_file:
        text = Path(args.from_file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if not text:
        raise SystemExit("Refusing to write an empty weekly report")

    report.write_text(text + "\n", encoding="utf-8")
    if not args.no_mark_reported:
        marked = 0
        for record_day in week_dates(day):
            record = record_path(root, record_day)
            if not record.exists():
                continue
            updated, changed_count = mark_reported_text(
                record.read_text(encoding="utf-8"),
                report,
                field="Weekly Reported",
            )
            if changed_count:
                record.write_text(updated, encoding="utf-8")
                marked += changed_count
        print(f"marked_weekly_reported: {marked}")
    print(report)


def configure(args: argparse.Namespace) -> None:
    root = Path(args.daily_root).expanduser()
    report_format = normalize_report_format(args.report_format)
    record_dir(root).mkdir(parents=True, exist_ok=True)
    diary_dir(root).mkdir(parents=True, exist_ok=True)
    weekly_dir(root).mkdir(parents=True, exist_ok=True)
    path = save_config(root, report_format or "md")
    print(f"config: {path}")
    print(f"root: {root}")
    print(f"report_format: {report_format}")


def show_config(_args: argparse.Namespace) -> None:
    path = config_path()
    print(f"config: {path}")
    config = load_config()
    if config.get("root"):
        print(f"root: {Path(config['root']).expanduser()}")
    else:
        print("(no root configured)")
    if config.get("report_format"):
        print(f"report_format: {config['report_format']}")
    else:
        print("(no report format configured)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="User-chosen daily report root directory")
    parser.add_argument("--format", choices=sorted(REPORT_FORMATS), help="Report format")

    subparsers = parser.add_subparsers(dest="command", required=True)

    append = subparsers.add_parser("append", help="Append one AI coding session entry")
    append.add_argument("--date", help="Entry date in YYYY-MM-DD format")
    append.add_argument("--tool", help="AI coding tool name")
    append.add_argument("--project", help="Project or module name")
    append.add_argument("--title", help="Short session title")
    append.add_argument("--source", help="Thread, repo path, issue, or other source hint")
    append.add_argument("--done", action="append", help="Completed work item")
    append.add_argument("--todo", action="append", help="Follow-up item")
    append.add_argument("--issue", action="append", help="Problem, risk, or thought")
    append.add_argument("--demand", action="append", help="Weekly demand, problem, or objective")
    append.add_argument("--value", action="append", help="Why the demand matters")
    append.add_argument("--measure", action="append", help="Success signal or acceptance check")
    append.add_argument("--progress", action="append", help="Weekly progress context")
    append.add_argument("--efficiency", action="append", help="Reusable tool, method, or workflow impact")
    append.add_argument("--note", action="append", help="Additional note")
    append.add_argument("--tags", action="append", help="Tag")
    append.set_defaults(func=append_entry)

    show = subparsers.add_parser("show", help="Show paths and activity for a day")
    show.add_argument("--date", help="Date in YYYY-MM-DD format")
    show.add_argument("--dates", help="Comma-separated dates in YYYY-MM-DD format")
    show.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    show.add_argument("--end-date", help="End date in YYYY-MM-DD format")
    show.add_argument("--all", action="store_true", help="Show reported entries too")
    show.set_defaults(func=show_day)

    write = subparsers.add_parser("write-report", help="Write final daily report")
    write.add_argument("--date", help="Report date in YYYY-MM-DD format")
    write.add_argument("--dates", help="Comma-separated dates in YYYY-MM-DD format")
    write.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    write.add_argument("--end-date", help="End date in YYYY-MM-DD format")
    write.add_argument("--from-file", help="Markdown report file to write")
    write.add_argument(
        "--no-mark-reported",
        action="store_true",
        help="Do not mark selected activity entries as reported after writing",
    )
    write.set_defaults(func=write_report)

    show_weekly = subparsers.add_parser(
        "show-week", help="Show work records for the week containing a date"
    )
    show_weekly.add_argument("--date", help="Any date in the target week")
    show_weekly.add_argument("--all", action="store_true", help="Show weekly-reported entries too")
    show_weekly.set_defaults(func=show_week)

    weekly = subparsers.add_parser("write-weekly-report", help="Write final weekly report")
    weekly.add_argument("--date", help="Any date in the target week")
    weekly.add_argument("--from-file", help="Weekly report file to write")
    weekly.add_argument(
        "--no-mark-reported",
        action="store_true",
        help="Do not mark selected activity entries as weekly reported after writing",
    )
    weekly.set_defaults(func=write_weekly_report)

    config = subparsers.add_parser("configure", help="Remember the daily report root")
    config.add_argument(
        "--root",
        dest="daily_root",
        required=True,
        help="User-chosen daily report root directory to remember",
    )
    config.add_argument(
        "--format",
        dest="report_format",
        choices=sorted(REPORT_FORMATS),
        required=True,
        help="Report file format to remember",
    )
    config.set_defaults(func=configure)

    show_saved = subparsers.add_parser("config", help="Show saved configuration")
    show_saved.set_defaults(func=show_config)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
