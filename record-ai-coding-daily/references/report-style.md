# Daily Report Style

Use this reference when turning one or more files from `工作记录/` into a final `.md` or `.txt` report under `日报/`.

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
- Mention AI tools only when tool usage itself matters; otherwise summarize what the user completed, clarified, implemented, verified, or decided.
- Avoid excessive code, command dumps, or raw logs.
- Preserve important concrete identifiers: dates, module names, endpoints, trace_id/request_id, platform names, metric IDs, table names, test file names, and pass/fail counts.
- Group repeated work across Claude, Codex, CodeBuddy, Cursor, or other tools by project or objective rather than by chat window.
- Group same-module or same-objective work together. For example, keep dag-viewer frontend, backend trace APIs, observability summaries, theme work, and browser checks together as one coherent dag-viewer work stream instead of scattering them across unrelated paragraphs.
- Do not write `一、已完成事项` as many isolated one-line items. When there is enough material, use 4-5 substantial prose paragraphs or compact prose items.
- Avoid blank lines between individual completed-work items inside a section; keep them visually adjacent and continuous.

## Section Guidance

### 一、已完成事项

Summarize what the user actually completed or verified. Prefer paragraphs like:

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

Target 4-5 work streams when the day's material is rich. If there are fewer than four natural work streams, do not invent filler; merge by objective and keep the section readable. If there are more than five raw items, combine them by module or goal.

Bad pattern:

```text
完成了项目架构初读。

梳理了配置链路。

优化了 dag-viewer 页面。

增加了 trace 接口。
```

Better pattern:

```text
今天主要围绕 mmeuleragentserver 的项目结构理解和欧拉agent框架 dag-viewer 调试台体验优化展开。项目架构方面，完成了 framework、servers、agents 三层结构初读，梳理了 main.py 动态加载服务、FastAPI app 装配、Agent 自动注册以及 GraphBuilder.run() 串起 trace、监控、finalizer 和 LangGraph 执行的主请求流。
配置和部署链路方面，确认了 schema 默认值、servers/{service}/config/default.toml、环境 TOML 和环境变量覆盖的加载顺序，并梳理了 BUILD、Dockerfile、pb_branch_img.sh、pb_build_img.sh 对多服务镜像装配的支撑关系。
dag-viewer 方面，围绕本地调试台定位完成了 trace 列表、统计指标、节点状态映射、执行时间线、节点检查器和原始 JSON 观测区等体验优化，同时补充了后端 trace 查询、详情和统计接口。
```

### 二、TODO

List concrete next steps. Keep each item action-oriented and independently executable. Use adjacent short lines instead of putting a blank line between every TODO.

Good TODO wording:

```text
继续在 WeCube 平台按具体 trace_id 查询 bizid24099，确认 graph_run、node_run 等记录真实入库。
```

### 三、问题和思考

Capture risks, conclusions, and engineering judgment. This section should explain what the work revealed, not repeat every completed item. Group related concerns together and avoid isolated one-line fragments unless the issue is genuinely standalone.

Good topics:

- Difference between application-side success and platform-side closure.
- Boundaries between observability/reporting and the main business path.
- Remaining failure modes or validation gaps.
- Process improvements for future smoke tests or production checks.
