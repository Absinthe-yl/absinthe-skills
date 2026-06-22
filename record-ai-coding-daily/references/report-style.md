# Daily Report Style

Use this reference when turning one or more `activity.md` entries into the final `daily-report.md`.

## Output Shape

Use exactly these top-level sections:

```text
一、已完成事项
二、TODO
三、问题和思考
```

## Style

- Write in Chinese.
- Prefer narrative paragraphs for completed work.
- Use short TODO lines for next actions.
- Keep a professional engineering tone: factual, specific, and calm.
- For multi-day reports, name the covered dates early, such as `这两天主要推进...` or `6.21 到 6.22 主要完成...`.
- For non-contiguous dates, name the actual work dates rather than implying every calendar day was active.
- Mention AI tools only when tool usage itself matters; otherwise summarize the engineering outcome.
- Avoid excessive code, command dumps, or raw logs.
- Preserve important concrete identifiers: dates, module names, endpoints, trace_id/request_id, platform names, metric IDs, table names, test file names, and pass/fail counts.
- Group repeated work across Claude, Codex, CodeBuddy, Cursor, or other tools by project or objective rather than by chat window.

## Section Guidance

### 一、已完成事项

Summarize what was actually completed or verified. Prefer paragraphs like:

```text
今天主要推进 xxx 的真实链路验证，重点确认 xxx、xxx、xxx 是否能在当前环境中闭环。
```

For two-day or multi-day reports, use wording like:

```text
这两天主要推进 xxx 的真实链路验证，重点确认 xxx、xxx、xxx 是否能在真实环境中闭环。
```

For non-contiguous days such as Friday and the following Monday, use wording like:

```text
上周五和本周一主要推进 xxx 的真实链路验证，重点确认 xxx、xxx、xxx 是否能在真实环境中闭环。
```

Then describe the main work streams. For each stream, include:

- What was changed, verified, or clarified.
- What evidence supports it.
- What remains unverified, if relevant.

### 二、TODO

List concrete next steps. Keep each item action-oriented and independently executable.

Good TODO wording:

```text
继续在 WeCube 平台按具体 trace_id 查询 bizid24099，确认 graph_run、node_run 等记录真实入库。
```

### 三、问题和思考

Capture risks, conclusions, and engineering judgment. This section should explain what the work revealed, not repeat every completed item.

Good topics:

- Difference between application-side success and platform-side closure.
- Boundaries between observability/reporting and the main business path.
- Remaining failure modes or validation gaps.
- Process improvements for future smoke tests or production checks.
