# Weekly Report Style

Use this reference when turning one calendar week of `工作记录/` files into a final weekly report under `周报/`.

## Output Shape

Use this exact section shape:

```markdown
##### 一、需求
###### 1.1 <需求或主题名>

###### 1.2 <需求或主题名>

##### 二、进展
###### 2.1 <对应需求或主题名>

###### 2.2 <对应需求或主题名>

##### 三、效率
###### 3.1 <提效工具或方法名>
```

Use Markdown heading markers even when the saved report format is `txt`, because the weekly-report convention explicitly requires this shape. For `txt`, avoid other Markdown syntax such as lists, links, code fences, and backticks unless the user asks.

Omit the entire `##### 三、效率` section when there is no real efficiency content in the work records. Never include `（可选）` in the visible report heading.

## Style

- Write in Chinese.
- Prefer concise, leader-facing updates.
- Focus on work streams and outcomes rather than chat-window chronology.
- Center the report on what the user completed, verified, clarified, or decided. Mention AI tools only when their usage itself is relevant.
- Group same-module or same-objective work together instead of splitting it by day or AI window.
- Preserve concrete evidence from the work records when it helps judgment: project names, platform names, metrics, test results, acceptance checks, known verification gaps, or user-visible behavior.
- Distinguish verified progress from planned or pending validation.
- Keep code-level details out of the main prose. Prefer "完成本地调试台体验优化" over internal function names, route names, config keys, or node names.
- Make the report understandable to a reader who has no chat context and only sees the weekly report.
- Weekly reports are not daily reports. Do not expand every technical detail; keep each subsection to 1-2 short sentences unless the user explicitly asks for detail.
- Do not begin every subsection with repeated openings such as "本周重点处理", "本周继续完善", or "本周围绕". Start directly with the work or status.
- Use short, concrete subsection titles. Good titles look like "dag-viewer 调试台", "菜单推荐 Agent", "MR 冲突收敛", or "[LLM] MCP 数据能力". Bad titles look like "本地调试台可观测能力建设" or "Agent 框架工程化与接入能力建设".
- Do not mention how records were read. Never include script-version notes, missing parameter notes, `show-week --all`, or fallback file-reading explanations in the report or user-facing response.
- Avoid code blocks unless the user explicitly asks for them.

## Section Guidance

### ##### 一、需求

Use one `###### 1.x` subsection per major demand, objective, or work stream. The subsection title should be short and concrete, such as `dag-viewer 调试台`, `菜单推荐 Agent`, or `MR 冲突收敛`.

Each demand subsection must cover at least these ideas, but compress them into 1-2 short sentences:

- Target problem or objective: what is being solved or delivered.
- Value: why this matters to users, the team, reliability, delivery speed, production readiness, observability, maintainability, or risk reduction.
- Measurement: how success can be judged, such as visible behavior, smoke results, platform visibility, error rates, latency, coverage, pass counts, metric curves, acceptance checks, or reduced manual work.

Do not write long background paragraphs. Do not invent business value or metrics not present in the records; phrase uncertain items as pending confirmation.

Good demand style:

```text
###### 1.1 dag-viewer 调试台
提升本地排障效率，让开发者不用依赖外部平台也能看清执行记录、节点状态和关键观测信息。效果主要看页面是否可用、关键信息是否完整、敏感输入是否被控制。
```

### ##### 二、进展

Use one `###### 2.x` subsection per corresponding demand or progress stream. The subsection order should usually match `一、需求`.

Each progress subsection should explain only the most important facts:

- What the user actually completed, implemented, verified, or decided this week.
- What evidence supports the progress, such as working behavior, checks, tests, comparisons, or platform observations.
- What remains pending, blocked, or risky.

Keep each progress subsection to 1-2 short sentences. It is acceptable to include simple status words such as `已完成`, `进行中`, or `待补测` when that makes the report easier to scan.

Good progress style:

```text
###### 2.1 dag-viewer 调试台
已补齐执行记录、节点状态、时间线、节点检查器和观测摘要，并完成基础页面与脚本检查。复杂图布局和批量 trace 对比暂缓，后续按调试需求继续补。
```

### ##### 三、效率

Include this section only when the records mention reusable personal/team tooling, process improvements, automation, templates, standards, or methods that reduce repeated work.

Efficiency content should explain what changed and who benefits in 1-2 short sentences. Good topics include:

- A reusable skill, script, template, or checklist that saves repeated prompting or manual work.
- A standardized smoke flow, validation method, or reporting format that reduces communication cost.
- A debugging or review workflow that helps the team locate problems faster.

Do not include this section just to restate ordinary project progress.
