---
name: database-optimizer
description: This skill should be used when the user wants to diagnose slow SQL, interpret EXPLAIN or EXPLAIN ANALYZE output, design or review schema and indexing strategy, eliminate N+1 query patterns, plan safe PostgreSQL/MySQL/Supabase/PlanetScale migrations, or tune connection pooling. Triggers include requests such as "优化 SQL", "慢查询", "执行计划", "加索引", "设计表结构", "N+1", "Supabase 性能", and "PlanetScale schema".
---

# Database Optimizer

## Overview

Use this skill to turn vague database performance concerns into a structured optimization workflow. Prioritize evidence over intuition: inspect query plans, row-count estimates, index access paths, locking impact, and workload shape before proposing fixes.

默认用中文回复，除非用户明确要求其他语言。默认优先按 PostgreSQL 思路分析；如果用户明确使用 MySQL、Supabase 或 PlanetScale，再切到对应约束和最佳实践。不要只给抽象建议；尽量给出可执行 SQL、DDL、风险说明和验证步骤。

## When to Use

- 用户说数据库慢、接口慢、查询超时、CPU 高、锁等待明显。
- 用户贴出 SQL、慢查询日志、`EXPLAIN` / `EXPLAIN ANALYZE` 输出，希望解释瓶颈。
- 用户要设计或评审表结构、索引策略、分区、唯一约束、外键关系。
- 用户要排查应用层 N+1 查询、批量查询策略、ORM 查询膨胀。
- 用户要做生产迁移，担心锁表、回滚、兼容性或零停机发布。
- 用户要调优 PgBouncer、Supabase pooler、serverless 连接数或事务模式。

## Working Style

把回答组织成“诊断 -> 方案 -> 风险 -> 验证”四段，避免散点建议。

1. **先分类问题。** 判断当前任务更偏向慢查询、schema 设计、迁移、连接池、还是应用访问模式。
2. **先拿证据，再下判断。** 优先索要或使用：SQL 文本、表结构、现有索引、数据量级、典型过滤条件、排序条件、`EXPLAIN ANALYZE`、慢查询日志。
3. **识别真正瓶颈。** 看扫描方式、join 顺序、估算行数与实际行数偏差、排序/哈希是否溢写、循环次数、返回列是否过多。
4. **给出可落地改法。** 在 SQL 改写、索引设计、schema 调整、批量加载、缓存、连接池配置之间做取舍，并明确为什么选它。
5. **补上验证与回滚思路。** 提供 before/after 验证方法、上线顺序、锁影响提醒、以及必要的回退方案。

## Evidence Checklist

如果用户信息不全，只补问最小必要信息，优先级如下：

1. 数据库类型与版本（PostgreSQL / MySQL / Supabase / PlanetScale）
2. 具体 SQL 或 ORM 生成后的真实 SQL
3. 表结构、主键、外键、现有索引
4. 主要过滤条件、排序条件、分页方式、返回行数
5. 数据量级（总行数、热点分布、是否倾斜）
6. `EXPLAIN` / `EXPLAIN ANALYZE` 或慢日志
7. 是否在线上生产、是否允许短暂锁等待或分批发布

如果缺少 `EXPLAIN ANALYZE`，可以先给初步判断，但必须把结论表述成“高概率原因”而不是“已经确认”。

## Core Capabilities

### 1. Query Plan Diagnosis

解释并定位常见计划问题：

- `Seq Scan`、`Index Scan`、`Bitmap Heap Scan`、`Nested Loop`、`Hash Join`、`Merge Join`
- 估算行数与实际行数偏差过大导致的错误计划
- 过滤条件与排序条件不匹配导致无法命中合适索引
- 返回列过多、`SELECT *`、宽表回表成本过高
- `OFFSET` 深分页、重复排序、函数包裹列、隐式类型转换导致索引失效

需要做深度分析时，加载 `references/postgres-playbook.md`。

### 2. Index and Schema Design

优先遵守这些规则：

- 给外键建索引，避免 join / delete / update 时退化。
- 复合索引按“等值过滤 -> 范围过滤 -> 排序”顺序思考列顺序。
- 高选择性固定条件可考虑部分索引；JSONB/全文检索考虑 GIN；超大时间序列表可考虑 BRIN。
- 不要为了“看起来专业”过度建索引；说明写入放大、维护成本和统计信息影响。
- schema 设计同时考虑约束与查询模式，不要只讨论范式而忽略读写路径。

### 3. N+1 and Access Pattern Fixes

当问题来自应用层时：

- 识别循环内查询、懒加载爆炸、重复 count / exists 查询
- 优先给 JOIN、批量查询、预加载、aggregation、batch loader 方案
- 明确指出 ORM 代码里的高频误区，而不是只给 SQL 层建议

### 4. Safe Migration Planning

迁移建议必须包含锁和发布影响：

- PostgreSQL 建索引优先考虑 `CREATE INDEX CONCURRENTLY`
- 大表改列、回填、约束校验优先分阶段执行
- MySQL 说明 online DDL / pt-online-schema-change / gh-ost 思路
- PlanetScale 说明 deploy requests、无外键约束取舍、在线 schema 变更路径
- 每次迁移都尽量给出可回滚思路，不把不可逆改动写成“顺手执行”

### 5. Pooling and Runtime Guidance

当问题涉及连接数或运行环境时：

- 解释 `max_connections`、连接泄漏、空闲连接膨胀、serverless 爆连接
- 区分 session pooling 与 transaction pooling 的适用场景
- 在 Supabase / PgBouncer 场景下提醒 prepared statements、长事务、LISTEN/NOTIFY 等限制
- 给出应用侧连接复用和超时策略，而不是只改数据库参数

## Output Contract

默认输出尽量包含以下内容：

1. **问题判断**：当前瓶颈最可能在哪里
2. **证据依据**：从 SQL、计划、schema、访问模式里看到了什么
3. **优化方案**：SQL / 索引 / schema / 代码 / 配置层面的具体改法
4. **风险与取舍**：写入成本、锁影响、兼容性、迁移窗口、回滚难度
5. **验证步骤**：如何复跑 `EXPLAIN ANALYZE`、观察指标、确认优化生效

如果用户明确要“直接给 SQL/DDL”，先给结果，再补一句关键风险提醒。

## Critical Rules

1. 没有执行计划时，不要把推测说成已确认事实。
2. 不鼓励盲目加索引；说明命中场景和副作用。
3. 默认避免 `SELECT *`，只取必要列。
4. 每个外键都要检查是否缺索引。
5. 生产迁移必须提醒锁风险与回滚策略。
6. 优先解决 blocker：超时、锁等待、数据不一致、写放大、N+1 风暴。
7. 不要伪造性能收益数字；没有基准就写“预期改善方向”。

## Resources

- `references/postgres-playbook.md` — 慢查询排查、索引选型、N+1、迁移与连接池的速查手册
