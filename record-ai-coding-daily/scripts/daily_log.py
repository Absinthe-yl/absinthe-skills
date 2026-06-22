#!/usr/bin/env python3
"""Append and write date-organized AI coding daily notes."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import sys
from typing import Iterable
import uuid


UNREPORTED_VALUES = {"", "no", "false", "pending", "unreported"}


def resolve_root(args: argparse.Namespace) -> Path:
    if getattr(args, "root", None):
        return Path(args.root).expanduser()

    env_root = os.environ.get("AI_CODING_DAILY_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    raise SystemExit(
        "Daily report root is required. Ask the user where to store AI coding "
        "daily documents, then pass --root or set AI_CODING_DAILY_ROOT."
    )


def parse_date(value: str | None) -> dt.date:
    if not value:
        return dt.date.today()
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date {value!r}; expected YYYY-MM-DD") from exc


def day_dir(root: Path, day: dt.date) -> Path:
    return root / f"{day:%Y}" / f"{day:%Y-%m-%d}"


def paths(root: Path, day: dt.date) -> tuple[Path, Path]:
    folder = day_dir(root, day)
    return folder / "activity.md", folder / "daily-report.md"


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


def parse_range(args: argparse.Namespace) -> tuple[dt.date, dt.date]:
    dates = parse_selected_dates(args)
    return min(dates), max(dates)


def date_span(start: dt.date, end: dt.date) -> Iterable[dt.date]:
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)


def is_contiguous(dates: list[dt.date]) -> bool:
    ordered = sorted(dates)
    return ordered == list(date_span(ordered[0], ordered[-1]))


def report_path(root: Path, dates: list[dt.date]) -> Path:
    ordered = sorted(dates)
    if len(ordered) == 1:
        return paths(root, ordered[0])[1]

    if is_contiguous(ordered):
        folder_name = f"{ordered[0]:%Y-%m-%d}_to_{ordered[-1]:%Y-%m-%d}"
    else:
        folder_name = "_plus_".join(f"{day:%Y-%m-%d}" for day in ordered)

    folder = root / f"{ordered[0]:%Y}" / folder_name
    return folder / "daily-report.md"


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


def reported_value(block: list[str]) -> str | None:
    for line in block:
        match = re.match(r"- Reported:\s*(.*)", line)
        if match:
            return match.group(1).strip()
    return None


def is_unreported(block: list[str]) -> bool:
    value = reported_value(block)
    return value is None or value.lower() in UNREPORTED_VALUES


def render_activity(text: str, include_reported: bool) -> str:
    header, blocks = split_activity(text)
    selected = [block for block in blocks if include_reported or is_unreported(block)]
    if not selected:
        return "".join(header).rstrip() + "\n\n(no unreported activity entries)\n"
    return "".join(header + [line for block in selected for line in block])


def mark_reported_text(text: str, report: Path) -> tuple[str, int]:
    header, blocks = split_activity(text)
    changed_count = 0
    report_label = str(report)
    updated_blocks: list[list[str]] = []

    for block in blocks:
        if not is_unreported(block):
            updated_blocks.append(block)
            continue

        changed_count += 1
        updated = list(block)
        replaced = False
        for index, line in enumerate(updated):
            if line.startswith("- Reported:"):
                updated[index] = f"- Reported: {report_label}\n"
                replaced = True
                break

        if not replaced:
            insert_at = 1
            for index, line in enumerate(updated):
                if line.startswith("- Entry ID:") or line.startswith("- AI tool:"):
                    insert_at = index + 1
            updated.insert(insert_at, f"- Reported: {report_label}\n")

        updated_blocks.append(updated)

    return "".join(header + [line for block in updated_blocks for line in block]), changed_count


def append_entry(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    day = parse_date(args.date)
    activity, _report = paths(root, day)
    activity.parent.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now().strftime("%H:%M")
    entry_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    title = args.title.strip() if args.title else "AI coding session"
    tool = args.tool.strip() if args.tool else "Unknown"

    entry = [
        f"\n## {now} - {title}\n",
        f"- Entry ID: {entry_id}\n",
        "- Reported: no\n",
        f"- AI tool: {tool}\n",
    ]
    if args.project:
        entry.append(f"- Project: {args.project.strip()}\n")
    if args.source:
        entry.append(f"- Source: {args.source.strip()}\n")
    if args.tags:
        entry.append(f"- Tags: {', '.join(clean_lines(args.tags))}\n")

    entry.append(bullet_block("Completed", args.done))
    entry.append(bullet_block("TODO", args.todo))
    entry.append(bullet_block("Problems/thoughts", args.issue))

    note_lines = clean_lines(args.note)
    if note_lines:
        entry.append("- Notes:\n")
        entry.extend(f"  - {line}\n" for line in note_lines)

    if not activity.exists():
        header = f"# AI coding activity - {day:%Y-%m-%d}\n"
        activity.write_text(header, encoding="utf-8")

    with activity.open("a", encoding="utf-8") as handle:
        handle.writelines(entry)

    print(activity)


def show_day(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    dates = parse_selected_dates(args)
    print(f"report: {report_path(root, dates)}")
    for day in dates:
        activity, _report = paths(root, day)
        print()
        print(f"activity: {activity}")
        print()
        if activity.exists():
            print(render_activity(activity.read_text(encoding="utf-8"), args.all))
        else:
            print("(no activity log yet)")


def write_report(args: argparse.Namespace) -> None:
    root = resolve_root(args)
    dates = parse_selected_dates(args)
    report = report_path(root, dates)
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
            activity, _unused = paths(root, day)
            if not activity.exists():
                continue
            updated, changed_count = mark_reported_text(
                activity.read_text(encoding="utf-8"), report
            )
            if changed_count:
                activity.write_text(updated, encoding="utf-8")
                marked += changed_count
        print(f"marked_reported: {marked}")
    print(report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="User-chosen daily report root directory")

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

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
