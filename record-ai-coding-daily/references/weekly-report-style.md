# Weekly Report Style

Use this reference when turning one calendar week of `工作记录/` files into a final weekly report under `周报/`.

## Output Shape

Use exactly these top-level sections:

```text
一、目标解决什么问题、这个问题的价值
二、如何衡量
三、进展
四、总结（如有）
```

## Style

- Write in Chinese.
- Prefer concise, manager-readable paragraphs.
- Focus on work streams and outcomes rather than chat-window chronology.
- Preserve concrete evidence from the work records: project names, platform names, metrics, tests, request ids, trace ids, table names, and known verification gaps.
- Distinguish verified progress from planned or pending validation.
- Avoid code blocks unless the user explicitly asks for them.

## Section Guidance

### 一、目标解决什么问题、这个问题的价值

Explain the problem being solved and why it matters. Connect engineering work to reliability, efficiency, production readiness, observability, delivery speed, user value, or risk reduction.

### 二、如何衡量

Describe how progress or success can be measured. Use concrete signals when available, such as smoke results, platform visibility, error rates, latency, coverage, pass counts, metric curves, acceptance checks, or user-visible behavior.

### 三、进展

Summarize the week's concrete progress. Group by objective or work stream, not by AI tool. Mention unresolved checks plainly instead of implying closure.

### 四、总结（如有）

Include this section when there are meaningful conclusions, risks, lessons learned, or next-step judgment. If there is nothing useful to add, keep the heading and write `无。`.
