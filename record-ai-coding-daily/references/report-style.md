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
- Keep the entire daily report around 130 Chinese characters, including punctuation, unless the user explicitly asks for a detailed version.
- Prefer plain human wording over technical replay.
- Use short TODO lines for next actions; keep only the most important 1-3 items.
- Keep a professional engineering tone: factual, specific, and calm.
- For multi-day reports, name the covered dates early, such as `这两天主要推进...` or `6.21 到 6.22 主要完成...`.
- For non-contiguous dates, name the actual work dates rather than implying every calendar day was active.
- Mention AI tools only when tool usage itself matters; otherwise summarize what the user completed, clarified, implemented, verified, or decided.
- Avoid code details, command dumps, raw logs, function names, route names, config keys, and internal node names.
- Preserve at most 1-2 important business-facing identifiers when necessary, such as product/module names or test result counts.
- Group repeated work across Claude, Codex, CodeBuddy, Cursor, or other tools by project or objective rather than by chat window.
- Group same-module or same-objective work together. For example, summarize dag-viewer frontend、后端接口、观测信息和主题调整 as "优化 dag-viewer 本地调试体验", not as separate technical rows.
- Do not write `一、已完成事项` as many isolated one-line items. Use 1-2 compact sentences covering 3-5 major work streams when material allows.
- Avoid blank lines between individual completed-work items inside a section; keep them visually adjacent and continuous.

## Section Guidance

### 一、已完成事项

Summarize what the user actually completed or verified. Keep this section short enough that a human can scan it in seconds. Prefer wording like:

```text
今天主要完成项目架构梳理、dag-viewer 调试台优化、AI 工具链更新、服务目录规范化和菜单推荐能力开发，并完成关键路径验证。
```

For two-day or multi-day reports, use wording like:

```text
这两天主要推进框架调试体验、服务规范化和新 Agent 开发，重点完成可用性优化与核心链路验证。
```

For non-contiguous days such as Friday and the following Monday, use wording like:

```text
上周五和本周一主要完成框架调试台优化和新能力验证，遗留真实环境测试与命名一致性确认。
```

Compress the main work streams. Include:

- What was completed.
- What remains important to follow up.

Target 3-5 work streams when the day's material is rich. If there are more than five raw items, combine them by module or goal. Do not exceed about 60 Chinese characters for this section unless the user asks for detail.

Bad pattern:

```text
罗列函数名、配置键、接口路径和内部节点名，把实现细节当成日报正文。
用大量英文技术名描述内部链路，而没有说明使用者完成了什么。
```

Better pattern:

```text
完成项目架构梳理、dag-viewer 调试台优化、AI 工具链更新、服务目录规范化和菜单推荐能力开发，并验证关键路径。
```

### 二、TODO

List only the most important 1-3 next steps. Keep each item short, action-oriented, and readable by non-specialists.

Good TODO wording:

```text
补测真实环境效果。
完善自动化测试。
确认命名和配置一致性。
```

### 三、问题和思考

Capture only the most important risk or conclusion. Keep it to 1 short sentence unless the user asks for detail.

Good topics:

- Real environment verification gaps.
- Naming/config consistency risks.
- User-facing quality concerns.
