---
name: mcp-builder
description: This skill should be used when the user wants to design, scaffold, implement, review, or harden a Model Context Protocol (MCP) server. It fits API wrappers, database tools, filesystem adapters, workflow automation servers, existing MCP server refactors, and tasks that require well-named tools, typed schemas, strong error handling, security guardrails, and runnable delivery instructions.
---

# MCP Builder

## Overview

把“给 AI 接一个系统能力”收敛成稳定的 MCP server 交付流程。先定义能力边界与工具接口，再实现 server 代码、校验、测试和运行说明；默认目标不是只给建议，而是产出可运行、可维护、可继续扩展的结果。

默认优先使用 TypeScript + `@modelcontextprotocol/sdk` + `zod`。只有当用户明确指定 Python，或者现有项目已经是 Python 生态时，再切换实现语言。

## Trigger Conditions

在下面这些场景触发本 skill：

- 用户要“做一个 MCP server”或“把某个系统接成 MCP”。
- 用户要把 API、数据库、文件系统、内部平台、脚本流程、工作流能力暴露给 agent。
- 用户已经有一个 MCP server，需要补工具、补 resource、改 schema、补测试、修错误处理或加安全约束。
- 用户只给出业务目标，例如“让 AI 能查订单”“让 agent 能操作知识库”，需要反推出合适的 MCP 工具设计。

如果用户只是想调用现成 MCP server，而不是构建/改造它，不要使用本 skill。

## Default Deliverable

默认交付物至少包含：

1. 工具/资源设计说明：说明每个能力的名字、输入、输出和边界。
2. 可运行代码：至少要有 server 入口、依赖声明、配置说明。
3. 安全与错误处理：说明鉴权、校验、超时、限流、异常返回策略。
4. 验证方法：给出本地运行、冒烟测试、示例调用方式。
5. 后续扩展建议：明确下一步该补什么，而不是把半成品伪装成完成品。

如果用户只要设计稿，不强行生成整套代码；但要明确指出哪些部分已设计、哪些部分尚未实现。

## Working Workflow

### 1. 先判断要暴露的能力，而不是先写代码

先识别真实目标：

- 是查询型能力，还是写操作能力？
- 是低频人工辅助，还是高频自动调用？
- 是适合做 `tool`，还是更适合做 `resource`？
- 是否涉及分页、大对象、长任务、敏感数据、鉴权、配额？

缺信息时，只问会直接影响接口设计的关键问题，例如：

- 数据源/系统是什么。
- 鉴权方式是什么。
- 读写边界到哪里。
- 是否有部署语言或运行时限制。

不要为了“显得严谨”把用户问成需求评审会。

### 2. 先设计工具接口，再决定内部实现

每个工具都先写清楚四件事：

1. 工具名
2. 输入 schema
3. 输出 contract
4. 失败时怎么报错

命名规则：

- 用清楚的动词 + 对象：`search_orders`、`get_invoice`、`create_ticket`
- 不用模糊名：`query1`、`handler_tool`、`process_data`
- 一个工具只做一件主事，避免“万能入口工具”

输入规则：

- 用 `zod` 明确定义类型、可选项、默认值和枚举。
- 对分页、过滤、排序、时间范围等常见参数给合理默认值。
- 对互斥参数、条件必填参数，优先用可判别结构或显式规则，而不是留给实现里兜底猜测。

输出规则：

- 数据型结果优先输出结构化 JSON。
- 面向人读的说明写成 Markdown 或简洁文本。
- 不要把错误文本混进成功 JSON 里。

### 3. 决定 server 形态

默认采用：

- 单一 `stdio` server 入口
- 独立 client/service 层封装外部系统
- 环境变量承载凭证与配置
- 轻量文件结构，优先保证可跑通

从零开始时，优先参考 `references/server-template.md`。
如果只需要快速起一个干净骨架，运行：

```bash
python3 <skill>/scripts/render_typescript_mcp_server.py \
  --server-name my-server \
  --tool-name search_items \
  --output /tmp/server.ts
```

生成的是单文件 TypeScript skeleton，适合快速起步或做最小可运行样例。

### 4. 实现时保持“工具无状态、边界清晰”

实现阶段遵守这些约束：

- 把外部 API/数据库访问放到单独函数或 client，避免把业务细节塞进 `server.tool(...)` 回调。
- 工具调用不依赖“上一次先调过某个工具”。每次调用都应独立成立。
- 对外部请求设置超时、错误映射和必要的重试策略。
- 避免在日志和错误里泄漏 token、cookie、隐私字段或全量响应。
- 对大结果集做分页、limit、summary，而不是一次吐给模型几十万字。

### 5. 该用 resource 时就用 resource

下列情况优先考虑 resource，而不是 tool：

- 需要暴露大块只读上下文，例如 schema、配置快照、知识库目录、长文档。
- 数据适合被 agent 读取，而不是每次通过工具主动执行查询。
- 内容天然是“被浏览/引用”的，而不是“执行一个动作”。

如果是小而频繁的动态查询，还是优先 tool。

### 6. 把安全和失败路径当成功能的一部分

至少补齐这些保护：

- 输入校验：类型、范围、枚举、长度、必填。
- 权限边界：只读/可写能力明确拆开。
- 超时控制：外部请求不能无限挂起。
- 限流与分页：防止大查询直接打爆上游或把模型撑爆。
- 错误表达：返回可执行的错误信息，例如“订单不存在”“参数 customer_id 缺失”，不要只抛 `Internal error`。

需要更完整的检查项时，加载 `references/production-checklist.md`。

### 7. 交付时给用户完整落地路径

最终答复至少覆盖：

- 改了哪些文件
- 入口文件在哪里
- 依赖怎么安装
- 环境变量怎么配
- 本地怎么启动
- 怎么做一轮最小验证
- 已知限制和下一步建议

不要只贴一段 server 代码就结束，留用户自己猜怎么跑。

## Tool Design Rules

始终遵守下面这组规则：

1. **名字可被模型直接理解**：工具名要能反映用途与对象。
2. **schema 比注释更重要**：让类型系统约束输入，而不是让调用者靠描述猜。
3. **输出对 agent 友好**：能结构化就结构化，必要时再补一层可读摘要。
4. **错误要能行动**：报错信息要告诉调用方“哪里错了、怎么改”。
5. **默认值要克制**：只给合理默认，不要偷偷改变业务含义。
6. **一把刀只切一种菜**：不要把检索、写入、审批、统计混进一个工具。
7. **先做最小可用，再做大全套**：先把关键主路径做通，再补批量、筛选、扩展字段。

## Review Existing MCP Servers

如果任务是改造已有 MCP server，按这个顺序审查：

1. 工具命名是否清楚。
2. schema 是否真的能拦住脏输入。
3. 输出是否稳定、是否容易被 agent 消费。
4. 错误信息是否可执行。
5. 是否有泄漏敏感信息的风险。
6. 是否缺测试或启动说明。
7. 是否把业务逻辑、I/O、server 注册揉成一团，导致难维护。

审查时优先指出高风险问题：鉴权错误、注入、越权写入、无限制大查询、未处理超时、异常吞掉真实错误。

## Resources

- `references/server-template.md`：TypeScript MCP server 骨架、推荐目录结构、依赖与测试起步方式。
- `references/production-checklist.md`：工具设计、输出契约、安全、测试与交付清单。
- `scripts/render_typescript_mcp_server.py`：快速生成单文件 TypeScript server skeleton。
