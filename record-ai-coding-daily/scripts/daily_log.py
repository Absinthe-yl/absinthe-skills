#!/usr/bin/env python3
"""Append and write date-organized AI coding daily notes."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import sys
from typing import Iterable


def default_root() -> Path:
    env_root = os.environ.get("AI_CODING_DAILY_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    knowledge_base = Path("~/Desktop/个人知识库").expanduser()
    if knowledge_base.exists():
        return knowledge_base / "AI编码日报"

    return Path("~/Documents/ai-coding-daily").expanduser()


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


def parse_range(args: argparse.Namespace) -> tuple[dt.date, dt.date]:
    if getattr(args, "start_date", None) or getattr(args, "end_date", None):
        if getattr(args, "date", None):
            raise SystemExit("Use either --date or --start-date/--end-date, not both")
        if not args.start_date or not args.end_date:
            raise SystemExit("--start-date and --end-date must be used together")
        start = parse_date(args.start_date)
        end = parse_date(args.end_date)
    else:
        start = end = parse_date(getattr(args, "date", None))

    if start > end:
        raise SystemExit("--start-date must be on or before --end-date")
    return start, end


def date_span(start: dt.date, end: dt.date) -> Iterable[dt.date]:
    current = start
    while current <= end:
        yield current
        current += dt.timedelta(days=1)


def report_path(root: Path, start: dt.date, end: dt.date) -> Path:
    if start == end:
        return paths(root, start)[1]
    folder = root / f"{start:%Y}" / f"{start:%Y-%m-%d}_to_{end:%Y-%m-%d}"
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


def append_entry(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser() if args.root else default_root()
    day = parse_date(args.date)
    activity, _report = paths(root, day)
    activity.parent.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now().strftime("%H:%M")
    title = args.title.strip() if args.title else "AI coding session"
    tool = args.tool.strip() if args.tool else "Unknown"

    entry = [f"\n## {now} - {title}\n", f"- AI tool: {tool}\n"]
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
    root = Path(args.root).expanduser() if args.root else default_root()
    start, end = parse_range(args)
    print(f"report: {report_path(root, start, end)}")
    for day in date_span(start, end):
        activity, _report = paths(root, day)
        print()
        print(f"activity: {activity}")
        print()
        if activity.exists():
            print(activity.read_text(encoding="utf-8"))
        else:
            print("(no activity log yet)")


def write_report(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser() if args.root else default_root()
    start, end = parse_range(args)
    report = report_path(root, start, end)
    report.parent.mkdir(parents=True, exist_ok=True)

    if args.from_file:
        text = Path(args.from_file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if not text:
        raise SystemExit("Refusing to write an empty report")

    report.write_text(text + "\n", encoding="utf-8")
    print(report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Daily report root directory")

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
    show.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    show.add_argument("--end-date", help="End date in YYYY-MM-DD format")
    show.set_defaults(func=show_day)

    write = subparsers.add_parser("write-report", help="Write final daily report")
    write.add_argument("--date", help="Report date in YYYY-MM-DD format")
    write.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    write.add_argument("--end-date", help="End date in YYYY-MM-DD format")
    write.add_argument("--from-file", help="Markdown report file to write")
    write.set_defaults(func=write_report)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
