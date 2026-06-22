---
name: read-project-architecture
description: 快速初读陌生软件项目的架构，面向后续编码 AI 工具和人类开发者。Use when Codex needs a concise Chinese project/system overview, one-sentence purpose summary, architecture shape, important guidance docs such as AGENTS.md/CODEBUDDY.md/HARNESS.md, entry points, core directories, module responsibilities, and coding orientation without deep audit, exhaustive file reading, or code changes.
---

# Read Project Architecture

## Overview

使用这个 skill 在编码前快速建立项目架构地图。目标读者同时包括 AI 编码工具和人类开发者，因此输出要短、清楚、可继续行动。

默认使用中文回复，除非用户明确要求其他语言。不要改代码，除非用户另行要求。不要做完整业务逻辑审计、全量依赖图、安全审计或完整测试调查。

## Reuse Existing Architecture Map

如果项目根目录已有 `ARCHITECTURE.md`、`PROJECT_ARCHITECTURE.md`、`docs/architecture.md` 或类似架构地图，先评估是否可复用，避免重复初读：

- 先读架构地图的标题、摘要、目录和关键章节，不要默认全量读长文档。
- 检查它是否覆盖系统用途、技术栈、入口、目录职责、核心模块和架构流向。
- 用 `ls -l`、`stat`、`git status --short` 或相关配置文件时间判断是否可能过期。
- 如果架构地图足够新且覆盖当前问题，优先基于它输出简短更新，不重新扫描全项目。
- 如果明显过期或缺关键部分，只补读缺失区域。
- 不要默认创建或更新架构地图文件；只有用户要求保存时，才写入 `ARCHITECTURE.md` 或用户指定路径。

## Context Budget

控制上下文占用，把它当作“项目初读”，不是“项目深读”：

- 优先读少量高信号文件，不要把大文件、大目录、完整依赖树塞进上下文。
- 对大型项目，只抽样主路径和明显核心模块。
- 项目指导文档很多时，优先读根目录和最相关的 3-6 个。
- 对 `harness.md`、`.harness/*`、`CODEBUDDY.md`、`AGENTS.md` 这类文档，默认只提取架构/流程信号；除非用户要求，不要全量展开长文件。
- 读取长文档时优先看目录、标题、前 80-120 行、包含关键词的片段，而不是整文件。
- 工具输出应服务架构判断；如果某个文件只能提供实现细节，停止继续读取。
- `Directory Map` 只列核心目录，通常 6-12 项。
- `Core Modules` 只列核心模块，通常 4-8 项。
- 最终报告保持紧凑，面向“下一步该读哪里、该怎么理解架构”。

## Reading Order

1. 定位仓库根目录，用 `rg --files`、`ls` 或类似快速命令查看顶层结构。
2. 先查找可复用架构地图：`ARCHITECTURE.md`、`PROJECT_ARCHITECTURE.md`、`docs/architecture.md`、`docs/architecture*`。如果足够新且完整，优先复用。
3. 再读项目概览文件：`README*`、`docs/development*` 等。
4. 主动查找 AI 工具、协作或 harness 相关文档，但只提取架构初读需要的信号：
   - `AGENTS.md`
   - `CLAUDE.md`
   - `CODEBUDDY.md`
   - `HARNESS.md`
   - `GEMINI.md`
   - `.cursor/rules/*`
   - `.github/copilot-instructions.md`
   - 其他文件名包含 agents、harness、coding assistant、architecture、development、contributing 等含义的文档
5. 读取能揭示技术栈和命令的依赖/构建文件：`package.json`、`pnpm-workspace.yaml`、`pyproject.toml`、`requirements*.txt`、`go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle*`、`Makefile`、`Dockerfile`、`docker-compose*.yml`、CI workflow 和框架配置。
6. 检查明显入口、路由和配置文件。大型项目只看主路径，不逐模块深挖。

## What To Extract

只提取初步架构阅读需要的信息：

- 用一句话说明这个系统/项目是做什么的、作用是什么。
- 项目类型和主要技术栈。
- 架构形态，例如前端应用、后端 API、全栈应用、CLI、库、服务、monorepo、插件、扩展或数据管道。
- 运行入口、路由入口、配置入口、构建/测试入口。
- 顶层目录职责。
- 核心模块/组件和对应关键文件。
- 主控制流、请求流、页面流、数据流或任务流。
- 项目指导文档里的架构线索和编码约束。
- 后续 AI 工具或人类开发者应优先阅读的文件。

尽量用文件路径支撑判断。若是推测，明确标注“推测”。

## Guidance Docs

把项目指导文档当作一等输入，而不是可选背景。提取：

- 架构说明或模块边界
- 推荐阅读顺序
- 构建、测试、lint 或 harness 命令
- 编码规范
- 禁止修改或敏感区域
- 生成代码规则
- AI 编码工具专用工作约定

对于 `harness.md` 和 `.harness/*`，优先回答“是否存在 harness 层、它负责什么、后续编码如何使用它”。不要为了架构初读读取完整 harness 实现、完整测试说明或长日志示例。

如果指导文档与用户请求或更高优先级规则冲突，遵循更高优先级规则，并在输出中简短标注冲突。

## Output Format

必须以一句话总结开头。报告要方便 AI 工具和人类开发者快速理解项目，不要写成长文档。

```markdown
# 项目架构初读

## 一句话总结
这个系统用于……，主要作用是……。

## 概览
- 项目类型：
- 主要技术栈：
- 架构形态：

## 项目指导文档
| 文件 | 有用信息 |
| --- | --- |

## 入口
- 应用/运行入口：
- 路由入口：
- 配置入口：

## 目录地图
| 路径 | 职责 |
| --- | --- |

## 核心模块
| 模块 | 职责 | 关键文件 |
| --- | --- | --- |

## 架构流向
简要说明主控制流、页面流、请求流、数据流或任务流。

## 编码导向
后续 AI 工具或人类开发者建议优先阅读：
- 
```

## Quality Bar

结果应该让新的 AI 编码工具或人类开发者在几分钟内理解项目形状。保持架构优先、上下文节省，只提供足够定位后续编码入口的信息，不替代深度实现阅读。
