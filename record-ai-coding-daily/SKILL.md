---
name: record-ai-coding-daily
description: Record and summarize the user's AI coding tool activity into local date-organized daily and weekly report documents, with remembered storage root and txt/md report format preferences. Use when the user asks to log what they just did with AI coding tools such as Claude, Codex, CodeBuddy, Cursor, Copilot, or similar assistants; append an entry after an AI coding session; read today's accumulated AI work notes; configure the local report memory; generate a final Chinese daily report with completed work, TODOs, and problems/thoughts; or generate a weekly report for a natural week or explicit date range such as last Friday to this Thursday with demand-progress, efficiency, and other sections.
---

# Record AI Coding Daily

## Overview

Maintain a local, date-organized record of AI-assisted coding work. Use this skill in three modes:

1. **Session logging**: after each AI window/session, append a concise entry to today's activity document.
2. **Daily report generation**: near the end of a day or after a multi-day work span, read the accumulated activity documents and write a polished Chinese daily report.
3. **Weekly report generation**: read one natural week or explicit date range of work records and write a Chinese weekly report.

Use `scripts/daily_log.py` for all filesystem writes so paths and document structure stay consistent.

## Storage

Always ask the user where to store the AI coding daily documents and whether final reports should be `txt` or `md` before the first write unless those values are already explicit in the conversation, saved in this skill's local config, or set through environment variables. Do not silently choose defaults.

Ask in Chinese when needed:

```text
你希望 AI 编码日报保存到哪个本地目录？
日报文件希望保存为 txt 还是 md？
```

Then save the chosen directory and report format once:

```bash
python3 <skill>/scripts/daily_log.py configure --root "/path/chosen/by/user" --format md
```

This writes a local config file at `~/.config/ai-coding-daily/config.json` unless `AI_CODING_DAILY_CONFIG` points elsewhere. Treat that config as the durable memory shared by future invocations. If the user has configured `AI_CODING_DAILY_ROOT` and `AI_CODING_DAILY_FORMAT`, use them without asking again. Use `--root <path>` or `--format md|txt` on individual commands only for explicit one-off overrides.

Inspect saved config with:

```bash
python3 <skill>/scripts/daily_log.py config
```

The script creates exactly three first-level directories under the user-chosen root:

```text
<root>/工作记录/
<root>/日报/
<root>/周报/
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

If the saved report format is `txt`, use the same names with `.txt`:

```text
<root>/日报/6.17 日报.txt
```

Treat files in `工作记录/` as the incremental raw log and files in `日报/` as final user-facing reports.

Weekly reports are stored in `周报/`, with filenames based on the Monday of the selected report period:

```text
<root>/周报/2026-M6-20260615.md
<root>/周报/2026-M6-20260615.txt
```

In this name, `M6` means June and `20260615` is the Monday used for that report period. For an explicit range such as Friday to the following Thursday, use the Monday inside that range as the filename anchor.

Each activity entry includes:

```text
- Entry ID: <unique-id>
```

Daily and weekly reports leave activity entries unchanged. Regenerating a report for the same date or week may overwrite the existing report file.

## Tool Compatibility

This skill is tool-agnostic. Use it with Claude, Codex, CodeBuddy, Cursor, Copilot, or any AI coding tool that can follow the workflow and run or delegate the local script. Set `--tool` to the actual assistant name so the source remains clear in the `工作记录/` files.

## Workflow

### 1. Append a session entry

When the user says they have just finished using an AI coding tool, collect the minimum missing context from the current conversation and append one entry. Do not over-ask; infer from the conversation when possible.

Write the entry from the user's work perspective: describe what the user understood, decided, implemented, verified, or completed today. Treat the AI tool as source metadata only. Do not write the work record as if Claude, Codex, CodeBuddy, or "the AI" completed the work.

Capture:

- AI tool name, such as `Codex`, `Claude`, or `CodeBuddy`.
- Project/module name when known.
- A short title for the session.
- Completed user work in prose-oriented bullets.
- TODOs or next checks.
- Problems, risks, or thoughts.
- Weekly-report context when known: demand/problem, value, measurement or acceptance signals, current progress, and efficiency impact.
- Optional source, such as thread/window name, repo path, or issue id.

Prefer a factual work log over a celebratory summary. Include technical names, endpoints, tests, metrics, and platform names when they matter, but avoid dumping large code snippets. Good records sound like "完成了 dag-viewer 调试台体验优化" or "确认了配置加载链路", not "让 Codex 优化了页面".

Make `工作记录/` understandable to a zero-context AI that only reads the files later. When the session contributes to a larger weekly objective, include enough context to recover:

- What user need, engineering problem, or delivery objective this work belongs to.
- Why it matters to users, the team, reliability, delivery efficiency, or risk control.
- How success can be judged, such as visible behavior, smoke results, platform checks, test pass counts, acceptance criteria, or reduced manual work.
- What concrete progress changed in this session.
- Whether the session produced a reusable tool, method, or workflow that improves personal or team efficiency.

Run:

```bash
python3 <skill>/scripts/daily_log.py append \
  --tool "Codex" \
  --project "agent-framework" \
  --title "Validated monitoring smoke path" \
  --demand "提升 Agent 框架真实环境验收能力，避免只看本地日志就误判上线质量。" \
  --value "让监控链路能被稳定验证，降低新增业务接入和生产排障风险。" \
  --measure "以真实请求、平台可见性和关键测试通过作为验收信号。" \
  --done "完成了音乐推荐链路验证，确认请求能走通并产生关键观测信息。" \
  --progress "已确认应用侧请求链路和观测上报正常，平台侧查询留作下一步。" \
  --todo "继续在真实平台确认观测数据可查。" \
  --issue "当前已确认应用侧正常，平台侧可见性仍需补验。"
```

Use `--date YYYY-MM-DD` only when the user asks to record a non-current day. The script prints the written file path; mention it briefly if useful.

### 2. Inspect accumulated notes

Before generating a report, read the accumulated log. For a single day:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --date YYYY-MM-DD
```

After `configure` has saved a root, omit `--root`:

```bash
python3 <skill>/scripts/daily_log.py show --date YYYY-MM-DD
```

If the user explicitly wants to preview a different output format once, pass `--format md` or `--format txt` before the subcommand:

```bash
python3 <skill>/scripts/daily_log.py --format txt show --date YYYY-MM-DD
```

For a report covering a continuous date range:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

For non-contiguous dates, such as Friday and the following Monday only:

```bash
python3 <skill>/scripts/daily_log.py show --root "/path/chosen/by/user" --dates YYYY-MM-DD,YYYY-MM-DD
```

If the selected dates have no activity entries, ask the user whether to pick different dates or provide raw work notes. Do not invent a report.

### 3. Generate the final daily report

Read `references/report-style.md` before drafting the report. Then synthesize the selected activity entries into three sections:

```text
一、已完成事项
二、TODO
三、问题和思考
```

If the saved report format is `txt`, produce plain text only: no Markdown title prefix (`#`/`##`), no backticks, no Markdown links, no fenced code blocks, and no `-` bullet markers. Use plain section headings exactly as shown above. If the saved report format is `md`, Markdown headings are allowed but still avoid code blocks and excessive inline code.

Write a short human-facing summary, not a technical replay. For `一、已完成事项`, keep each individual completed-work item around 130 Chinese characters, including punctuation, unless the user explicitly asks for a detailed version. The whole report may be longer when there are multiple completed items. Merge related entries across dates and multiple AI tools into coherent work streams.

For `一、已完成事项`, write 3-5 compact completed-work items when there is enough material. Each item should be one natural-language sentence or a short paragraph around 130-150 Chinese characters. Keep related work from the same module or objective together. Prioritize delivered changes, validated results, and user-visible progress. Do not turn reading, studying, or "梳理" into standalone completed work unless it produced a concrete decision, document, or implementation direction. Do not list function names, route names, node names, config keys, file paths, or command names unless they are the actual thing the user needs to report. Replace code details with plain descriptions such as "优化调试台体验", "新增菜单推荐能力", or "完成服务目录规范化".

Write a single-day report with:

```bash
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --date YYYY-MM-DD --from-file /tmp/report.md
```

After `configure` has saved a root, omit `--root`:

```bash
python3 <skill>/scripts/daily_log.py write-report --date YYYY-MM-DD --from-file /tmp/report.md
```

If the user explicitly wants a different output format once, pass `--format md` or `--format txt` before the subcommand:

```bash
python3 <skill>/scripts/daily_log.py --format txt write-report --date YYYY-MM-DD --from-file /tmp/report.txt
```

Write a multi-day report with:

```bash
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --start-date YYYY-MM-DD --end-date YYYY-MM-DD --from-file /tmp/report.md
```

Write a report for non-contiguous dates, such as Friday and the following Monday, with:

```bash
python3 <skill>/scripts/daily_log.py write-report --root "/path/chosen/by/user" --dates YYYY-MM-DD,YYYY-MM-DD --from-file /tmp/report.md
```

Writing a report overwrites the target report file and leaves source records untouched.

Never overwrite an existing report file silently when the new report drops meaningful content from the previous report. If a previous report exists, read it first and merge or explicitly preserve relevant material.

### 4. Generate the final weekly report

Read `references/weekly-report-style.md` before drafting the report. Then inspect work records for the requested period.

For a natural week containing the target date:

```bash
python3 <skill>/scripts/daily_log.py show-week --date YYYY-MM-DD
```

For an explicit non-natural week such as "上周五到这周四":

```bash
python3 <skill>/scripts/daily_log.py show-week --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

For non-contiguous selected dates:

```bash
python3 <skill>/scripts/daily_log.py show-week --dates YYYY-MM-DD,YYYY-MM-DD
```

The target date can be any day in the week. The script derives the report file path from Monday: for natural weeks, the Monday of that week; for explicit ranges, the Monday inside the selected range when present, otherwise the Monday of the range start.
Do not add `--all` to `show-week`; weekly output already includes the full week. If an older installed script or another AI attempt has parameter differences, handle that silently and continue. Do not tell the user about script-version differences, missing `show-week --all`, or "directly reading work record files"; those are implementation details and should not appear in the final response or report.

Draft the weekly report with exactly these sections:

```markdown
#### 一、需求进展
##### 1.1 <需求或主题名>
###### 需求：
###### 进展：
#### 二、效率
###### 2.1 <提效工具或方法名>
#### 三、其他
###### 3.1 <其他事项名>
```

In `一、需求进展`, each `1.x` subsection must combine demand and progress for the same topic. Under each `##### 1.x`, write `###### 需求：` followed by 1-2 short sentences covering the objective, value, and how to judge success. Then write `###### 进展：` followed by concrete numbered items using `（1）`, `（2）`, `（3）`.

Include `二、效率` only when the work records mention reusable personal/team tools, methods, automation, standards, or workflow improvements. Omit the entire section when there is no real efficiency content; never print `（可选）` in the final report heading. Use `（1）`, `（2）`, `（3）` under each `2.x` subsection.

Include `三、其他` only when the work records mention sharing sessions, meetings, cross-team communication, support work, or other meaningful items that do not fit demand/progress/efficiency. Use `（1）`, `（2）`, `（3）` under each `3.x` subsection.

Write the weekly report with:

```bash
python3 <skill>/scripts/daily_log.py write-weekly-report --date YYYY-MM-DD --from-file /tmp/weekly-report.md
```

For explicit ranges, write with:

```bash
python3 <skill>/scripts/daily_log.py write-weekly-report --start-date YYYY-MM-DD --end-date YYYY-MM-DD --from-file /tmp/weekly-report.md
```

Use the saved txt/md format unless the user explicitly overrides it with `--format md` or `--format txt` before the subcommand. Weekly reports always read the full target week of work records; do not filter source records.

## Quality Bar

- Keep session entries small enough to append often.
- Use the saved config before asking for storage path or report format; ask only when no saved value, no explicit command override, and no environment override is available.
- Keep final reports short, natural, and manager-readable; each completed-work item in `一、已完成事项` should be about 130-150 Chinese characters, including punctuation.
- In daily reports, group same-module work together and write 3-5 completed-work items when material allows.
- Do not format completed work as one isolated line per item with blank lines between items.
- Avoid code-level jargon in daily reports. Prefer "完成菜单推荐能力开发并验证成功/失败链路" over function names, route names, config keys, or internal node names.
- Keep work records and reports centered on what the user did or completed; mention AI tools only as source metadata when useful.
- Distinguish verified facts from pending checks.
- Generating a report must not hide source records from later review.
- Never mention internal metadata, inclusion state, or marker mechanics in user-facing report responses.
- Weekly reports must use `#### 一、需求进展`, `#### 二、效率` when efficiency content exists, and `#### 三、其他` when other meaningful items exist; do not use the old separated demand/progress format or the old goal/measurement/progress/summary four-section format, and do not include `（可选）` in the visible report.
- Weekly reports should usually be at least 70 lines when there is enough source material. They should be richer than daily reports, written for leaders and teammates, and organized for review and alignment.
- Weekly reports should not become raw daily logs. Avoid long background paragraphs and avoid starting every item with phrases like "本周重点处理", "本周继续完善", or "本周围绕".
- Merge related content under the same `1.x` topic before drafting. Keep work from the same module, platform, Agent, service, data domain, or delivery objective together instead of splitting by date, AI window, stage, or minor implementation step.
- Use one topic for one business/workstream unless there is a clearly different owner-facing goal or acceptance path. Reliability fixes, field completion, configuration work, environment validation, UI support, data debugging, and interface development should be folded into the same topic when they support the same delivery objective.
- Prefer fewer, fuller weekly topics over many repetitive 1.x sections. A dense week usually reads better as 4-6 substantial `需求进展` topics than 8-12 fragmented topics with similar wording.
- Do not separately report low leader-value noise such as git conflict mechanics, pure parameter explanation, temporary probe attempts, or one-off debugging process unless it materially changes delivery risk, schedule, ownership, or final conclusion.
- In weekly `需求进展`, `效率`, and `其他` sections, use `（1）`, `（2）`, `（3）` numbered items for progress/detail lists instead of long paragraphs or Markdown bullets.
- Use concrete, plain subsection titles such as "dag-viewer 调试台", "菜单推荐 Agent", or "MR 冲突收敛"; avoid abstract official titles such as "本地调试台可观测能力建设".
- Never mention script compatibility details, missing parameters, `show-week --all`, or fallback file-reading mechanics in user-facing weekly-report responses.
- Make work records rich enough for a zero-context AI to generate weekly reports from files alone.
- Do not claim platform-side closure unless the activity log says the platform was actually checked.
- Do not include long code blocks in the final report unless the user explicitly requests them.

## Resources

- `scripts/daily_log.py`: deterministic append, show, and write-report operations.
- `references/report-style.md`: Chinese report style and section guidance.
- `references/weekly-report-style.md`: Chinese weekly report style and section guidance.
