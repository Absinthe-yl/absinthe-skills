---
name: write-interface-docs
description: Draft standardized Chinese interface documentation from completed API definitions, request/response structs, proto files, handler code, or field lists. Use when Codex needs to generate service module, interface name, request examples in minimal-required and maximal-all-fields forms, a response example, and a field quick-reference table for one or more backend or internal service interfaces.
---

# Write Interface Docs

## Overview

Use this skill to turn a finished interface into delivery-ready Markdown documentation.
Output only fields, defaults, constraints, and behaviors that are grounded in source artifacts. Do not invent optional fields, default values, response members, or semantics.

## Output Contract

Write the final answer directly as the interface document. Do not prepend analysis, background, or implementation notes unless the user explicitly asks for them.

For each interface, use this structure:

````markdown
##### 一、<接口名称>
###### 1.1 接口信息
接口内容：<用 1-3 句说明这个接口的用途、输入对象、输出结果或主要业务动作>
服务模块：<服务模块>
接口名称：<接口名称>
req：
（1）最小必须格式（仅必填字段）

```json
{
  "...": "..."
}
```

<只在有依据时补充默认值/过滤规则/0 值语义等说明>

（2）最大格式（含所有可选字段）

```json
{
  "...": "..."
}
```

resp：

```json
{
  "...": "..."
}
```

###### 1.2 字段说明速查
|**字段**|**类型**|**必填**|**默认值**|**说明**|
|:-:|:-:|:-:|:-:|:-:|
|**Req**|||||
|...|...|...|...|...|
|**Resp**|||||
|...|...|...|...|...|
````

If multiple interfaces are requested, number them as `一、二、三...`, and use matching subsection numbers such as `1.1 / 1.2`, `2.1 / 2.2`, `3.1 / 3.2`.
Treat `接口内容` as a required item for every interface.

## Source Priority

Resolve field shape and semantics from the strongest available source, in this order:

1. `proto` / IDL / typed request-response definitions
2. Validation logic in handler, router, or service entry code
3. Default assignment code and config constants
4. Inline comments, examples, tests, or existing docs
5. User-provided field lists when code is unavailable

If two sources conflict, prefer executable code over examples or prose comments. If the conflict cannot be resolved, keep the field but mark the uncertain part as `待确认` instead of guessing.

## Writing Workflow

1. Identify the service module and interface name exactly as they appear in source artifacts.
2. Summarize `接口内容` in reader-friendly Chinese: explain what the interface does, what core input it consumes, and what result it returns or what action it completes.
3. Enumerate request and response fields, including nested objects, arrays, enums, and common wrapper fields.
4. Determine which request fields are truly required by checking validation code, non-optional schema markers, or explicit comments.
5. Determine defaults from actual code or authoritative comments. If no explicit default exists, write `-`.
6. Draft the minimal request example with only required top-level and nested fields.
7. Draft the maximal request example with all documented optional fields that can be filled from source.
8. Draft a success-path response example that reflects the real response shape. Do not add speculative error-only fields unless the interface always returns them.
9. Build the quick-reference table so a reader can scan the contract without reading the examples.

## Example Construction Rules

Follow these rules when generating examples:

- Write `接口内容` before `服务模块` and `接口名称`.
- Keep `接口内容` short and readable, usually 1-3 sentences or 1 compact paragraph.
- Ground `接口内容` in comments, requirement text, function names, return semantics, or handler logic. If the business purpose is not clear from source, write `待确认：` and state the most certain part only.
- Explain business intent in natural Chinese, but keep interface names, service names, and field names source-faithful.
- Use fenced `json` code blocks for every request and response example.
- Use realistic placeholder values that match type and business meaning.
- Preserve actual field names exactly; do not translate keys into Chinese.
- Keep the minimal request example strictly minimal. Do not include optional tuning parameters, debug switches, or defaultable fields.
- Keep the maximal request example exhaustive only within proven scope. If a field is mentioned nowhere authoritative, leave it out.
- Add one or more short note lines after the minimal request example only when the source proves behaviors such as `0` meaning unknown, omission triggering default logic, or limit fields falling back to config.
- Prefer a success response example unless the user explicitly asks for error cases.

## Table Rules

Use this table format:

- Columns must be `字段 | 类型 | 必填 | 默认值 | 说明`.
- Split the table into `Req` and `Resp` sections.
- Write `是` or `否` in the `必填` column.
- Write the actual default in the `默认值` column when proven; otherwise use `-`.
- For array or object children, prefer tree-style names such as `├─ finder_uin` and `└─ age` under the parent row.
- If tree markers would become ambiguous at deeper nesting, use explicit paths such as `items[].score`.
- Keep type names source-faithful when possible, for example `uint64`, `repeated uint64`, `bool`, `float`, `FooItem[]`.
- Write short explanations that help a reader understand purpose, constraints, ordering, count limits, or special sentinel values.

## Quality Bar

Before finishing, verify all of the following:

- The service module and interface name are present for every interface.
- The interface purpose is summarized under `接口内容`.
- The minimal request example contains only mandatory fields.
- The maximal request example does not contain invented fields.
- The response example matches the documented response shape.
- The quick-reference table covers all fields shown in examples and any always-present wrapper fields.
- Default values, max counts, ordering rules, and `0`/empty semantics are included only when grounded in source.
