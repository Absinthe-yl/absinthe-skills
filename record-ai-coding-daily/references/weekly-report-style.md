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

##### 三、效率（可选）
###### 3.1 <提效工具或方法名>
```

Use Markdown heading markers even when the saved report format is `txt`, because the weekly-report convention explicitly requires this shape. For `txt`, avoid other Markdown syntax such as lists, links, code fences, and backticks unless the user asks.

Omit the entire `##### 三、效率（可选）` section when there is no real efficiency content in the work records.

## Style

- Write in Chinese.
- Prefer concise, manager-readable paragraphs.
- Focus on work streams and outcomes rather than chat-window chronology.
- Center the report on what the user completed, verified, clarified, or decided. Mention AI tools only when their usage itself is relevant.
- Group same-module or same-objective work together instead of splitting it by day or AI window.
- Preserve concrete evidence from the work records when it helps judgment: project names, platform names, metrics, test results, acceptance checks, known verification gaps, or user-visible behavior.
- Distinguish verified progress from planned or pending validation.
- Keep code-level details out of the main prose. Prefer "完成本地调试台体验优化" over internal function names, route names, config keys, or node names.
- Make the report understandable to a reader who has no chat context and only sees the weekly report.
- Avoid code blocks unless the user explicitly asks for them.

## Section Guidance

### ##### 一、需求

Use one `###### 1.x` subsection per major demand, objective, or work stream. The subsection title should be short and concrete, such as `调试台可观测能力建设` or `菜单推荐能力验证`.

Each demand subsection must cover at least:

- Target problem or objective: what is being solved or delivered.
- Value: why this matters to users, the team, reliability, delivery speed, production readiness, observability, maintainability, or risk reduction.
- Measurement: how success can be judged, such as visible behavior, smoke results, platform visibility, error rates, latency, coverage, pass counts, metric curves, acceptance checks, or reduced manual work.

When records support it, also include scope, target users, constraints, current risks, or acceptance criteria. Do not invent business value or metrics not present in the records; phrase uncertain items as pending confirmation.

### ##### 二、进展

Use one `###### 2.x` subsection per corresponding demand or progress stream. The subsection order should usually match `一、需求`.

Each progress subsection should explain:

- What the user actually completed, implemented, verified, or decided this week.
- What evidence supports the progress, such as working behavior, checks, tests, comparisons, or platform observations.
- What remains pending, blocked, or risky.

Write in paragraphs rather than raw bullet dumps unless the user explicitly wants a list.

### ##### 三、效率（可选）

Include this section only when the records mention reusable personal/team tooling, process improvements, automation, templates, standards, or methods that reduce repeated work.

Efficiency content should explain what changed and who benefits. Good topics include:

- A reusable skill, script, template, or checklist that saves repeated prompting or manual work.
- A standardized smoke flow, validation method, or reporting format that reduces communication cost.
- A debugging or review workflow that helps the team locate problems faster.

Do not include this section just to restate ordinary project progress.
