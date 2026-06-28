# Absinthe Skills

一个个人 Codex Skills 仓库，主要沉淀面向日常开发、项目理解、简历表达和工作记录的可复用 AI 工作流。

这些 skills 的目标不是替代通用提示词，而是把反复使用的写作标准、项目分析路径、输出格式和本地脚本固定下来，让 Codex 在不同项目里保持更稳定的执行质量。

## Skills

| Skill | 用途 | 适合场景 |
| --- | --- | --- |
| `write-project-highlights` | 生成中文项目亮点、技术关键词拆解和面试问答 | 简历项目经历、实习项目包装、个人项目表达、根据代码库提炼亮点 |
| `read-project-architecture` | 快速初读陌生项目架构 | 接手新仓库、给 AI 编码工具建立项目地图、定位入口和核心模块 |
| `record-ai-coding-daily` | 记录 AI 编码过程并生成日报/周报 | Codex、Claude、Cursor 等 AI 编码会话后的工作记录和汇总 |
| `format-docs` | 将零散材料整理成中文规划/方案文档 | 技术方案、部署步骤、操作说明、会议纪要、路线规划 |

## Repository Structure

```text
.
├── format-docs/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── read-project-architecture/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── record-ai-coding-daily/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
└── write-project-highlights/
    ├── SKILL.md
    ├── PROMPT.md
    └── agents/openai.yaml
```

每个 skill 至少包含：

- `SKILL.md`：Codex 识别和执行 skill 的核心说明。
- `agents/openai.yaml`：Codex UI 展示元数据。
- `references/`：按需读取的详细写作规范或参考资料。
- `scripts/`：可重复执行的本地脚本。

## Install

将仓库中的 skills 同步到 Codex 全局目录：

```powershell
$src = "C:\Users\22353\Desktop\skills"
$dst = "C:\Users\22353\.codex\skills"
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
使用 $record-ai-coding-daily，记录刚才这次 Codex 编码工作。
```

Codex 也可以根据 `SKILL.md` 的 `description` 自动判断是否触发，但明确写出 `$skill-name` 通常更稳定。

## Notes

- `write-project-highlights/PROMPT.md` 是平台无关提示词，也可以直接给 Claude、Claude Code 或其他 AI 工具使用。
- `record-ai-coding-daily` 包含本地写入脚本，会在用户指定目录下维护工作记录、日报和周报。
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
C:\Users\22353\.codex\skills
```
