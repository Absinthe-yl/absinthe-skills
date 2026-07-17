# Subagent Profiles

## 1. research

适合：

- 查找配置入口
- 扫描仓库结构
- 收集证据
- 对比实现差异

推荐配置：

```json
{
  "task_name": "research_helper",
  "fork_turns": "3",
  "model": "<preferred-model>",
  "reasoning_effort": "medium",
  "message": "帮我做只读分析。目标：<目标>。范围：<范围>。限制：不要改代码。输出：返回证据、结论、未确认点。"
}
```

## 2. coding

适合：

- 实现功能
- 修复 bug
- 在明确边界内改代码

推荐配置：

```json
{
  "task_name": "feature_impl",
  "fork_turns": "3",
  "model": "<preferred-model>",
  "reasoning_effort": "medium",
  "message": "实现这个子任务。目标：<目标>。范围：仅修改 <文件/目录>。限制：最小改动，不处理无关问题。输出：说明改动、原因、风险、验证结果。"
}
```

## 3. review

适合：

- 检查设计或实现风险
- 做只读 code review
- 帮主 agent 进行第二视角审查

推荐配置：

```json
{
  "task_name": "review_helper",
  "fork_turns": "none",
  "model": "<preferred-model>",
  "reasoning_effort": "high",
  "message": "做只读审查。目标：识别缺陷、风险、遗漏场景。限制：不要改代码。输出：按严重程度返回问题、证据、建议。"
}
```

## 4. testing

适合：

- 运行或补做验证
- 分析失败测试
- 整理回归风险

推荐配置：

```json
{
  "task_name": "test_helper",
  "fork_turns": "3",
  "model": "<preferred-model>",
  "reasoning_effort": "medium",
  "message": "负责验证。目标：<验证目标>。范围：<测试范围>。限制：不要做超出范围的改动。输出：测试结果、失败原因、复现信息、建议下一步。"
}
```

## 5. custom

当标准 profile 不适合时，允许主 agent 自定义。

原则：

- 主 agent 决定结构
- 优先重用标准消息骨架
- 明确说明为什么不用标准 profile
- 模型和 reasoning 优先沿用用户默认偏好，除非任务性质明显要求覆盖

推荐模板：

```json
{
  "task_name": "custom_helper",
  "fork_turns": "none",
  "model": "<preferred-or-overridden-model>",
  "reasoning_effort": "<preferred-or-overridden-reasoning>",
  "message": "目标：<目标>。范围：<范围>。限制：<限制>。输出：<输出格式>。"
}
```

## Selection Rules

- 先看任务类型，再看复杂度
- 复杂度高但范围清晰：优先提高 reasoning_effort，而不是盲目扩大任务范围
- 子任务如果必须独立指定模型，使用可覆写模型的创建方式
- 如果当前任务本身不值得拆分，不要为了使用 skill 而强行创建 subagent
