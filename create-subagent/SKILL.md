---
name: create-subagent
description: Create and manage Codex subagents for focused delegation. Use when the user wants the main agent to spin up one or more subagents, asks for a reusable subagent template, wants standard subagent profiles such as research/search, coding, review, or testing, or wants a remembered default model and reasoning_effort for future subagent creation.
---

# Create Subagent

用这个 skill 把“创建 subagent”变成稳定流程，而不是每次临时拼 prompt。

默认目标：

- 优先复用标准 subagent profile
- 首次使用时询问并记录用户默认的 `model` 与 `reasoning_effort`
- 后续创建时优先使用已记录偏好
- 若标准 profile 不匹配，则由主 agent 按当前任务生成定制 subagent 配置，并以主 agent 判断为准

默认用中文回复，除非用户明确要求其他语言。

## Quick Start

1. 先读 [references/profiles.md](references/profiles.md) 选择最接近的 profile。
2. 运行 `python3 scripts/subagent_preferences.py show` 读取已保存偏好。
3. 如果没有偏好，且用户本轮也没明确指定，就先问一次默认 `model` 与 `reasoning_effort`。
4. 一旦用户给出偏好，立刻运行 `python3 scripts/subagent_preferences.py set --model ... --reasoning-effort ...` 保存。
5. 创建 subagent 时，按下面优先级决定配置：
   - 用户本轮明确指定
   - profile 内的强制要求
   - 已保存默认偏好
   - 主 agent 基于任务做出的显式判断
6. 如果需要单独指定 subagent 模型，创建时使用非全量继承上下文的方式，例如 `fork_turns: "none"` 或有限回溯；不要在全量继承上下文时声称已强制覆写模型。

## Preference Rules

把“记住用户偏好”当成这个 skill 的核心能力之一。

- 偏好文件不存在：说明是首次使用，先询问用户。
- 用户本轮给出新的默认模型或新的默认推理强度：更新保存值。
- 用户只给模型、不给推理强度：保留旧的推理强度；如果旧值也没有，再问一次。
- 用户只给推理强度、不给模型：保留旧的模型；如果旧值也没有，再问一次。
- 用户明确说“这次例外”：只在当前 subagent 上覆盖，不改已保存默认值。
- 用户明确说“以后都用这个”：更新已保存默认值。

如需查看当前记忆，运行：

```bash
python3 scripts/subagent_preferences.py show
```

如需清空记忆，运行：

```bash
python3 scripts/subagent_preferences.py clear
```

## Standard Profiles

标准 profile 的详细模板放在 [references/profiles.md](references/profiles.md)。先选最贴近任务的一类，再做小幅调整：

- `research`：查资料、扫仓库、找配置入口、整理证据
- `coding`：实现功能、修 bug、限制改动范围
- `review`：读 diff、找风险、给审查意见
- `testing`：补验证、跑测试、整理失败原因

如果这些都不合适，允许主 agent 直接创建 `custom` subagent。此时：

- 由主 agent 定义目标、范围、限制和输出格式
- 配置以当前主任务为准，不要求硬套标准模板
- 仍然优先继承用户默认模型/推理偏好，除非主 agent 明确认为该任务更适合别的配置

## Subagent Message Template

给 subagent 的消息至少要包含这四块：

1. 任务目标
2. 范围边界
3. 限制条件
4. 交付格式

推荐结构：

```text
目标：<要完成什么>
范围：<只看哪些文件 / 只做只读 / 只改哪些区域>
限制：<不要做什么 / 不要越权 / 不要改代码等>
输出：<最终回报要包含什么>
```

避免只给一句模糊命令，例如“你去看看这个问题”。要让 subagent 拿到一个边界清晰、可独立完成的小任务。

## Model Selection Heuristics

没有用户显式要求时，按任务复杂度选：

- 轻量只读扫描、资料汇总、批量小任务：优先较轻模型
- 中等复杂度实现、定向修改、常规测试：优先平衡模型
- 高不确定性分析、复杂方案设计、深度根因定位：优先更强模型与更高 reasoning

如果当前环境只允许部分模型，使用实际可用模型，不要伪造“已按要求指定成功”。

## Safety and Fallback

- 如果当前环境不允许创建 subagent，明确告知用户并改为主 agent 本地执行。
- 如果用户想指定某个模型，但当前环境不能对 subagent 强制覆写模型，明确说明限制。
- 如果 profile 建议和当前任务冲突，以主 agent 的任务判断为准，并简短说明为什么调整。
- 不要为了“看起来完成了”而虚构 subagent、虚构模型配置或虚构并行结果。

## Output to User

创建完成后，简短告诉用户：

- 选了哪个 profile
- 用了哪个模型和 reasoning_effort
- 是沿用默认偏好，还是本轮临时覆盖
- 如果是 custom，说明这是主 agent 按任务定制的配置

控制说明长度，重点是让用户知道“用了什么配置、为什么”。
