# Absinthe Skills

一个个人 Codex Skills 仓库，主要沉淀面向日常开发、项目理解、简历表达和工作记录的可复用 AI 工作流。

这些 skills 的目标不是替代通用提示词，而是把反复使用的写作标准、项目分析路径、输出格式和本地脚本固定下来，让 Codex 在不同项目里保持更稳定的执行质量。

## Skills

| Skill | 用途 | 适合场景 |
| --- | --- | --- |
| `write-project-highlights` | 生成中文项目亮点、技术关键词拆解和面试问答 | 简历项目经历、实习项目包装、个人项目表达、根据代码库提炼亮点 |
| `resume-optimizer` | 简历评分、40+ 项深度润色、JD 定制与多格式导出 | 简历评分与改写、按岗位定制提升匹配度、ATS 优化、导出 PDF/Word/HTML/LaTeX |
| `read-project-architecture` | 快速初读陌生项目架构 | 接手新仓库、给 AI 编码工具建立项目地图、定位入口和核心模块 |
| `record-ai-coding-daily` | 记录 AI 编码过程并生成日报/周报 | Codex、Claude、Cursor 等 AI 编码会话后的工作记录和汇总 |
| `format-docs` | 将零散材料整理成中文规划/方案文档 | 技术方案、部署步骤、操作说明、会议纪要、路线规划 |
| `mcp-builder` | 设计、实现和加固可交付的 MCP Server，沉淀工具/资源接口、TypeScript 骨架、安全与测试约束 | API 封装、数据库或文件系统接入、内部平台能力暴露给 agent、现有 MCP server 改造与补强 |
| `database-optimizer` | 分析慢 SQL、执行计划、索引与 schema 设计，并给出安全迁移与连接池建议 | PostgreSQL/MySQL/Supabase/PlanetScale 性能调优、EXPLAIN ANALYZE 解读、N+1 排查、生产迁移评审 |
| `absinthe-assistant` | 通用能力基线，固化研究、写作、分析、实现、可视化、自动化、PPT 制作和多角色/多 Agent 编排能力 | 开放式任务、跨能力域任务、专项 skill 不命中时的兜底与编排层、需要按角色切换或多 Agent 协作的任务 |

## Repository Structure

```text
.
├── format-docs/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── mcp-builder/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── read-project-architecture/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── record-ai-coding-daily/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── write-project-highlights/
│   ├── SKILL.md
│   ├── PROMPT.md
│   └── agents/openai.yaml
├── resume-optimizer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── scripts/
│   └── assets/
├── database-optimizer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       └── postgres-playbook.md
└── absinthe-assistant/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        └── roles.md
```

每个 skill 通常包含以下内容（按需取舍）：

- `SKILL.md`：Codex 识别和执行 skill 的核心说明。
- `agents/openai.yaml`：Codex UI 展示元数据。
- `references/`：按需读取的详细规范、速查手册或参考资料。
- `scripts/`：可重复执行的本地脚本。
- `assets/`：模板、样例或其他输出资源。

## Install

将仓库中的 skills 同步到 Codex 全局目录：

```powershell
$src = (Get-Location).Path
$dst = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Get-ChildItem -Path $src -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
  ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $dst $_.Name) -Recurse -Force
  }
```

同步后重新打开 Codex 线程，使新 skill 被加载。

## Usage

显式调用某个 skill：

```text
使用 $write-project-highlights，根据下面项目信息生成简历亮点：
...
```

```text
使用 $read-project-architecture，帮我快速初读这个项目架构。
```

```text
使用 $format-docs，把下面的部署步骤整理成一份规划文档。
```

```text
使用 $mcp-builder，帮我把这个 REST API 封装成一个 MCP server，并给出可运行的 TypeScript 骨架和测试建议。
```

```text
使用 $record-ai-coding-daily，记录刚才这次 Codex 编码工作。
```

```text
使用 $resume-optimizer，帮我评分并润色这份简历，再按目标岗位定制：
...
```

```text
使用 $absinthe-assistant，先判断这项任务应该走 Plan 还是 Craft，再切换到合适角色帮我完成。
```

Codex 也可以根据 `SKILL.md` 的 `description` 自动判断是否触发，但明确写出 `$skill-name` 通常更稳定。部分 skill 也可以通过 `allow_implicit_invocation: true` 支持更自然的自动触发。

## Notes

- `write-project-highlights/PROMPT.md` 是平台无关提示词，也可以直接给 Claude、Claude Code 或其他 AI 工具使用。
- `mcp-builder` 内置 MCP server 交付规范、TypeScript 骨架参考和单文件 skeleton 生成脚本，适合从 0 到 1 起服务或改造现有服务。
- `record-ai-coding-daily` 包含本地写入脚本，会在用户指定目录下维护工作记录、日报和周报。
- `resume-optimizer` 内置百分制评分模型、40+ 项润色清单、JD 关键词覆盖脚本和 HTML 模板，适合简历评分、深度润色、按岗位定制与多格式导出。
- `absinthe-assistant` 适合作为通用兜底 skill 和上层编排器，角色切换说明放在 `references/roles.md`。
- 本仓库只提交可复用 skill 内容；本地工具配置目录如 `.claude/` 通常不应提交。

## Maintenance

新增或更新 skill 后建议执行：

```powershell
git status --short
git add <skill-folder>
git commit -m "Update <skill-name>"
git push
```

如果需要让 Codex 立即使用最新版本，同步到：

```text
%USERPROFILE%\.codex\skills
```
