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

Always ask the user where to store the AI coding daily documents before the first write unless the path is already explicit in the conversation, saved in this skill's local config, or `AI_CODING_DAILY_ROOT` is set. Do not silently choose a default path.

Ask in Chinese when needed:

```text
你希望 AI 编码日报保存到哪个本地目录？
```

Then save the chosen directory once:

```bash
python3 <skill>/scripts/daily_log.py configure --root "/path/chosen/by/user"
```

This writes a local config file at `~/.config/ai-coding-daily/config.json` unless `AI_CODING_DAILY_CONFIG` points elsewhere. Treat that config as the durable memory shared by future invocations. If the user has configured `AI_CODING_DAILY_ROOT`, use it without asking again. Use `--root <path>` on individual commands only for an explicit one-off override.

Inspect saved config with:

```bash
python3 <skill>/scripts/daily_log.py config
```

The script creates exactly two first-level directories under the user-chosen root:

```text
<root>/工作记录/
<root>/日报/
```

Daily work records are stored in `工作记录/`, one file per date:

```text
<root>/工作记录/YYYY-MM-DD.md
```

Reports are stored in `日报/`, with filenames in the `<日期> 日报.md` style:

```text
<root>/日报/6.17 日报.md
<root>/日报/6.17-6.18 日报.md
<root>/日报/6.17、6.22 日报.md
```

Treat files in `工作记录/` as the incremental raw log and files in `日报/` as final user-facing reports.

Each activity entry includes:

```text
- Entry ID: <unique-id>
- Reported: no
```

After writing a report, `scripts/daily_log.py write-report` marks selected unreported entries as reported by replacing `Reported: no` with the report file path. Use this marker, not only the date, to decide whether content still needs to be included in a future report.

## Tool Compatibility

This skill is tool-agnostic. Use it with Claude, Codex, CodeBuddy, Cursor, Copilot, or any AI coding tool that can follow the workflow and run or delegate the local script. Set `--tool` to the actual assistant name so the source remains clear in the `工作记录/` files.

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

Before generating a report, read the accumulated unreported log. For a single day:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --date YYYY-MM-DD
```

After `configure` has saved a root, omit `--root`:

```bash
python3 <skill>/scripts/daily_log.py show --date YYYY-MM-DD
```

For a report covering a continuous date range:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

For non-contiguous dates, such as Friday and the following Monday only:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --dates YYYY-MM-DD,YYYY-MM-DD
```

By default, `show` omits entries already marked as reported. Use `--all` only when the user explicitly wants to inspect or regenerate already reported content.

If the selected dates have no unreported activity entries, ask the user whether to include already reported entries, pick different dates, or provide raw work notes. Do not invent a report.

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
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --date YYYY-MM-DD --from-file /tmp/report.md
```

After `configure` has saved a root, omit `--root`:

```bash
python3 <skill>/scripts/daily_log.py write-report --date YYYY-MM-DD --from-file /tmp/report.md
```

Write a multi-day report with:

```bash
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --start-date YYYY-MM-DD --end-date YYYY-MM-DD --from-file /tmp/report.md
```

Write a report for non-contiguous dates, such as Friday and the following Monday, with:

```bash
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --dates YYYY-MM-DD,YYYY-MM-DD --from-file /tmp/report.md
```

After writing, the script marks the selected unreported entries as reported. Use `--no-mark-reported` only for dry runs or explicit user requests.

Never overwrite an existing report file silently when the new report drops meaningful content from the previous report. If a previous report exists, read it first and merge or explicitly preserve relevant material.

## Quality Bar

- Keep session entries small enough to append often.
- Use the saved config before asking for a storage path; ask only when no saved root, no explicit `--root`, and no `AI_CODING_DAILY_ROOT` is available.
- Keep final reports natural and manager-readable.
- Distinguish verified facts from pending checks.
- Prefer unreported entries when generating reports; include already reported entries only when the user explicitly wants regeneration or correction.
- Do not claim platform-side closure unless the activity log says the platform was actually checked.
- Do not include long code blocks in the final report unless the user explicitly requests them.

## Resources

- `scripts/daily_log.py`: deterministic append, show, and write-report operations.
- `references/report-style.md`: Chinese report style and section guidance.
