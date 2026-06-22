---
name: record-ai-coding-daily
description: Record and summarize the user's AI coding tool activity into local date-organized daily report documents. Use when the user asks to log what they just did with AI coding tools such as Claude, Codex, CodeBuddy, Cursor, Copilot, or similar assistants; append an entry after an AI coding session; read today's accumulated AI work notes; or generate a final Chinese daily report with completed work, TODOs, and problems/thoughts.
---

# Record AI Coding Daily

## Overview

Maintain a local, date-organized record of AI-assisted coding work. Use this skill in two modes:

1. **Session logging**: after each AI window/session, append a concise entry to today's activity document.
2. **Report generation**: near the end of a day or after a multi-day work span, read the accumulated activity documents and write a polished Chinese report.

Use `scripts/daily_log.py` for all filesystem writes so paths and document structure stay consistent.

## Storage

Default root resolution in `scripts/daily_log.py`:

1. `AI_CODING_DAILY_ROOT` if set.
2. `~/Desktop/个人知识库/AI编码日报` if `~/Desktop/个人知识库` exists.
3. `~/Documents/ai-coding-daily` otherwise.

Per-day files use:

```text
<root>/<YYYY>/<YYYY-MM-DD>/activity.md
<root>/<YYYY>/<YYYY-MM-DD>/daily-report.md
```

Multi-day reports use:

```text
<root>/<YYYY>/<YYYY-MM-DD>_to_<YYYY-MM-DD>/daily-report.md
```

Treat `activity.md` as the incremental raw log and `daily-report.md` as the final user-facing report.

## Workflow

### 1. Append a session entry

When the user says they have just finished using an AI coding tool, collect the minimum missing context from the current conversation and append one entry. Do not over-ask; infer from the conversation when possible.

Capture:

- AI tool name, such as `Codex`, `Claude`, or `CodeBuddy`.
- Project/module name when known.
- A short title for the session.
- Completed work in prose-oriented bullets.
- TODOs or next checks.
- Problems, risks, or thoughts.
- Optional source, such as thread/window name, repo path, or issue id.

Prefer a factual work log over a celebratory summary. Include technical names, endpoints, tests, metrics, and platform names when they matter, but avoid dumping large code snippets.

Run:

```bash
python3 <skill>/scripts/daily_log.py append \
  --tool "Codex" \
  --project "agent-framework" \
  --title "Validated monitoring smoke path" \
  --done "Confirmed music_recommend request enters GraphBuilder.run() and reports WeCube traces to mesh sidecar." \
  --todo "Query WeCube by trace_id to verify platform ingestion." \
  --issue "Application-side reporting works, but platform-side visibility still needs confirmation."
```

Use `--date YYYY-MM-DD` only when the user asks to record a non-current day. The script prints the written file path; mention it briefly if useful.

### 2. Inspect accumulated notes

Before generating a report, read the accumulated log. For a single day:

```bash
python3 <skill>/scripts/daily_log.py show --date YYYY-MM-DD
```

For a report covering two or more days:

```bash
python3 <skill>/scripts/daily_log.py show --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

If the selected date range has no activity entries, ask the user for the raw work notes instead of inventing a report.

### 3. Generate the final report

Read `references/report-style.md` before drafting the report. Then synthesize the selected activity entries into three sections:

```text
一、已完成事项
二、TODO
三、问题和思考
```

Write mostly prose paragraphs, not code-heavy lists. Merge related entries across dates and multiple AI tools into coherent work streams. Preserve concrete facts from the log, including dates, platform names, request ids, test results, and unresolved verification items.

Write a single-day report with:

```bash
python3 <skill>/scripts/daily_log.py write-report --date YYYY-MM-DD --from-file /tmp/report.md
```

Write a multi-day report with:

```bash
python3 <skill>/scripts/daily_log.py write-report --start-date YYYY-MM-DD --end-date YYYY-MM-DD --from-file /tmp/report.md
```

Never overwrite an existing `daily-report.md` silently when the new report drops meaningful content from the previous report. If a previous report exists, read it first and merge or explicitly preserve relevant material.

## Quality Bar

- Keep session entries small enough to append often.
- Keep final reports natural and manager-readable.
- Distinguish verified facts from pending checks.
- Do not claim platform-side closure unless the activity log says the platform was actually checked.
- Do not include long code blocks in the final report unless the user explicitly requests them.

## Resources

- `scripts/daily_log.py`: deterministic append, show, and write-report operations.
- `references/report-style.md`: Chinese report style and section guidance.
