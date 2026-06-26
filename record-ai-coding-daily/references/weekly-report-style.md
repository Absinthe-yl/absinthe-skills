# Weekly Report Style

Use this reference when turning one calendar week of `工作记录/` files into a final weekly report under `周报/`.

## Output Shape

Use this exact section shape:

```markdown
#### 一、需求进展
##### 1.1 <需求或主题名>
###### 需求：
###### 进展：

##### 1.2 <需求或主题名>
###### 需求：
###### 进展：

#### 二、效率
###### 2.1 <提效工具或方法名>

#### 三、其他
###### 3.1 <其他事项名>
```

Use Markdown heading markers even when the saved report format is `txt`, because the weekly-report convention explicitly requires this shape. For `txt`, avoid other Markdown syntax such as lists, links, code fences, and backticks unless the user asks.

Omit the entire `#### 二、效率` section when there is no real efficiency content in the work records. Never include `（可选）` in the visible report heading.

Omit the entire `#### 三、其他` section when there are no meaningful sharing sessions, meetings, coordination items, support work, or miscellaneous items in the work records.

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
- Under each `##### 1.x` item in `一、需求进展`, always write `###### 需求：` and `###### 进展：` in that order.
- In each `进展：`, `效率`, and `其他` subsection, write concrete items with Chinese parenthesized numbering: `（1）`, `（2）`, `（3）`. Do not use Markdown bullets for those sections.
- Do not mention how records were read. Never include script-version notes, missing parameter notes, `show-week --all`, or fallback file-reading explanations in the report or user-facing response.
- Avoid code blocks unless the user explicitly asks for them.

## Section Guidance

### #### 一、需求进展

Use one `##### 1.x` subsection per major demand, objective, or work stream. The subsection title should be short and concrete, such as `新增 Agent 框架接入`, `dag-viewer 调试台`, `mmeulershowagentserver`, or `langfuse 相关`.

Inside each `##### 1.x` subsection, use this exact shape:

```text
##### 1.x <主题名>
###### 需求：
<1-2 short sentences>
###### 进展：
（1）<progress item>
（2）<progress item>
```

`需求：` must cover at least these ideas, but compress them into 1-2 short sentences:

- Target problem or objective: what is being solved or delivered.
- Value: why this matters to users, the team, reliability, delivery speed, production readiness, observability, maintainability, or risk reduction.
- Measurement: how success can be judged, such as visible behavior, smoke results, platform visibility, error rates, latency, coverage, pass counts, metric curves, acceptance checks, or reduced manual work.

Do not write long background paragraphs. Do not invent business value or metrics not present in the records; phrase uncertain items as pending confirmation.

`进展：` should use numbered items and explain only the most important facts:

- What the user actually completed, implemented, verified, or decided this week.
- What evidence supports the progress, such as working behavior, checks, tests, comparisons, or platform observations.
- What remains pending, blocked, or risky.

Use `（1）`, `（2）`, `（3）` for progress items. Keep each item short; it is acceptable to include simple status words such as `已完成`, `进行中`, `待补测`, or expected completion dates when that makes the report easier to scan.

Preserve useful image or attachment links under the relevant `进展：` subsection when the work records include them and they help explain the work.

Good demand-progress style:

```text
##### 1.1 dag-viewer 调试台
###### 需求：
提升本地排障效率，让开发者不用依赖外部平台也能看清执行记录、节点状态和关键观测信息。效果主要看页面是否可用、关键信息是否完整、敏感输入是否被控制。
###### 进展：
（1）已补齐执行记录、节点状态、时间线、节点检查器和观测摘要，并完成后端查询、详情和统计接口。
（2）完成缩放、平移、适应视图、主题切换和节点动效优化，已通过脚本检查和浏览器页面验证。
```

### #### 二、效率

Include this section only when the records mention reusable personal/team tooling, process improvements, automation, templates, standards, or methods that reduce repeated work.

Use `###### 2.x` subsection headings and explain what changed and who benefits through `（1）`, `（2）`, `（3）` numbered items. Good topics include:

- A reusable skill, script, template, or checklist that saves repeated prompting or manual work.
- A standardized smoke flow, validation method, or reporting format that reduces communication cost.
- A debugging or review workflow that helps the team locate problems faster.

Do not include this section just to restate ordinary project progress.

Good efficiency style:

```text
###### 2.1 skill
（1）read-project-architecture：每次重开上下文需要理解项目信息，因此写一个 skill 轻量化阅读，主要阅读架构层面，存入外部记忆，以 docs/ 形式沉淀。
```

### #### 三、其他

Include this section only when the records mention sharing sessions, meetings, cross-team communication, support work, planning, or other items worth showing to a leader but not suitable for `需求`, `进展`, or `效率`.

Use one `###### 3.x` subsection per topic and `（1）`, `（2）`, `（3）` numbered items under it.

Good other style:

```text
###### 3.1 分享会
（1）当前 Agent 开发框架进展。
（2）Agent 相关技术分享。
```
