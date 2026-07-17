#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = SKILL_DIR / ".state"
STATE_FILE = STATE_DIR / "preferences.json"


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_state(data: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_show() -> int:
    print(json.dumps(load_state(), ensure_ascii=False, indent=2))
    return 0


def cmd_set(model: str | None, reasoning_effort: str | None) -> int:
    state = load_state()
    if model:
        state["model"] = model
    if reasoning_effort:
        state["reasoning_effort"] = reasoning_effort
    save_state(state)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def cmd_clear() -> int:
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    if STATE_DIR.exists():
        try:
            STATE_DIR.rmdir()
        except OSError:
            pass
    print("{}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage remembered default subagent preferences.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show")

    set_parser = subparsers.add_parser("set")
    set_parser.add_argument("--model")
    set_parser.add_argument("--reasoning-effort")

    subparsers.add_parser("clear")

    args = parser.parse_args()
    if args.command == "show":
        return cmd_show()
    if args.command == "set":
        return cmd_set(args.model, args.reasoning_effort)
    if args.command == "clear":
        return cmd_clear()
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
