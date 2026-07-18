# MCP Server Production Checklist

在交付 MCP server 之前，用这份清单做最后一轮自检。

## 1. Capability Fit

先确认能力形态选对了：

- 频繁、动态、带参数的操作：优先 `tool`
- 大块只读上下文：优先 `resource`
- 需要模板化提示词：再考虑 prompt/resource 组合

不要把所有东西都塞进一个工具里。

## 2. Tool Naming

好名字应该让 agent 不看实现也能猜对用途。

推荐：

- `search_customers`
- `get_order_detail`
- `create_support_ticket`
- `list_project_files`

避免：

- `query`
- `run`
- `process_data`
- `tool_1`

## 3. Schema Design

每个工具至少检查：

- 是否定义了明确类型
- 是否标记了真正的必填项
- 是否给了克制的默认值
- 是否限制了 `limit`、时间范围、字符串长度
- 是否对排序、状态、模式类字段使用枚举
- 是否把互斥条件写成结构，而不是运行时瞎猜

### 常见参数建议

- `limit`: 默认 10~50，且有上限
- `offset` 或 `cursor`: 二选一，不要两个都必填
- 时间范围：明确时区、格式和最大跨度
- 关键字搜索：说明大小写、模糊匹配、字段范围

## 4. Output Contract

优先给 agent 好消费的结果：

- 小结果：结构化 JSON + 一句摘要
- 大结果：分页结果 + 总数 + 下一页线索
- 混合结果：`summary` + `items` 的双层结构

推荐成功结果模式：

```json
{
  "summary": "Found 12 matching customers",
  "items": [
    {
      "id": "cust_001",
      "name": "Acme"
    }
  ],
  "nextCursor": null
}
```

错误结果不要伪装成成功文本。要么抛出明确异常，要么返回足够具体的失败说明。

## 5. Security

最少检查这些点：

- 凭证是否来自环境变量，而不是硬编码
- 日志里是否会打印 token、cookie、Authorization 头、手机号、身份证、邮箱全量
- 写操作是否做了权限边界拆分
- 查询是否限制了范围和条数
- 是否存在注入风险（SQL、shell、模板、路径拼接）
- 是否需要速率限制或简单缓存，避免上游被打爆

## 6. Error Handling

好错误要满足三件事：

1. 能区分是谁错了：调用参数、上游服务、网络、权限、数据不存在
2. 能提示怎么改：缺哪个参数、参数格式应是什么、上游当前为什么失败
3. 不泄漏秘密：不把密钥、内部堆栈、全量上游响应直接暴露出去

推荐错误文案风格：

- `Missing required parameter: customer_id`
- `Order not found: ord_123`
- `Upstream CRM request timed out after 8000ms`
- `Invalid status. Expected one of: draft, active, archived`

避免：

- `Internal error`
- `Something went wrong`
- 直接把长堆栈甩给用户

## 7. Test Coverage

最少做这些验证：

- 每个关键工具至少 1 条成功路径
- 每个关键工具至少 1 条失败路径
- server 启动与工具注册冒烟测试
- 参数边界测试：空值、非法枚举、超大 limit、错误日期格式

如果工具涉及写操作，再补：

- 幂等或重复提交测试
- 权限失败测试
- 上游 4xx/5xx 映射测试

## 8. Delivery Checklist

给用户交付时，不要漏掉这些：

- 文件结构
- 依赖安装命令
- 环境变量说明
- 启动命令
- 最小验证方式
- 已知限制
- 推荐下一步

## 9. Good Default File Layout

```text
src/
  index.ts          # MCP server 入口
  clients/          # 上游 API/DB 封装
  tools/            # 每个工具的 schema + handler
  resources/        # 只读资源定义
  utils/            # 错误、日志、配置
package.json
README.md
```

如果项目很小，也可以先用单文件入口；但一旦超过 3~5 个工具，就尽快拆层。
