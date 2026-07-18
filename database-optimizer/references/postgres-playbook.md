# PostgreSQL / MySQL Database Optimization Playbook

## 1. Slow Query Triage

排查慢查询时，优先按下面顺序收集信息：

1. 真实 SQL（不要只看 ORM 片段）
2. 数据库类型与版本
3. 表结构、主键、外键、现有索引
4. 典型参数值、返回行数、分页方式
5. `EXPLAIN ANALYZE`（PostgreSQL）或 `EXPLAIN FORMAT=JSON`（MySQL）
6. 相关慢日志、接口耗时、QPS、锁等待信息

### PostgreSQL 重点观察项

- 是否出现 `Seq Scan` 扫大表
- `rows` 与 `actual rows` 是否差距很大
- `loops` 是否异常偏高
- 是否有 `Sort Method: external merge` / hash spill 到磁盘
- 是否发生大量 `Heap Fetches`、回表或宽行读取
- `Planning Time` 是否异常高（统计信息/过多索引/超复杂 SQL）

### MySQL 重点观察项

- `type` 是否退化到 `ALL`
- `key` / `possible_keys` 是否为空或命中错误索引
- `Using filesort` / `Using temporary` 是否出现在核心路径
- 复合索引是否被最左前缀破坏

## 2. Index Selection Heuristics

### B-Tree

优先用于：等值过滤、范围过滤、排序、join key。

常见规则：

- 单列高频过滤字段
- 外键列
- 复合索引：先等值、再范围、再排序
- 如果查询固定为 `WHERE status = 'published' ORDER BY created_at DESC`，优先考虑：

```sql
CREATE INDEX idx_posts_published_created_at
ON posts (created_at DESC)
WHERE status = 'published';
```

### GIN

优先用于：JSONB containment、数组包含、全文检索。

```sql
CREATE INDEX idx_events_payload_gin
ON events USING GIN (payload jsonb_path_ops);
```

### BRIN

优先用于：超大、天然按时间追加的数据表。只有当物理顺序与过滤条件高度相关时才有价值。

### Partial Index

适合低基数字段 + 热查询子集。

```sql
CREATE INDEX idx_orders_unpaid_created_at
ON orders (created_at DESC)
WHERE status = 'unpaid';
```

### 不要这样做

- 为每个看起来重要的列都建单列索引
- 已有有效复合索引还重复建前缀完全重叠索引
- 忽略写入成本、vacuum、统计信息与 bloat

## 3. Common SQL Rewrite Patterns

### 消除 SELECT *

```sql
-- Bad
SELECT *
FROM orders
WHERE user_id = $1;

-- Better
SELECT id, status, total_amount, created_at
FROM orders
WHERE user_id = $1;
```

### 消除深分页

```sql
-- Bad
SELECT id, created_at
FROM logs
ORDER BY created_at DESC
LIMIT 50 OFFSET 100000;

-- Better: keyset pagination
SELECT id, created_at
FROM logs
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT 50;
```

### 消除函数包裹导致的索引失效

```sql
-- Bad
WHERE DATE(created_at) = CURRENT_DATE

-- Better
WHERE created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
```

## 4. N+1 Detection Cheatsheet

常见信号：

- 先查一批父记录，再在循环里逐条查子记录
- ORM debug log 出现同一 SQL 模板被重复执行上百次
- 每个列表项都单独触发 count / exists / aggregate

优先改法：

1. JOIN + 聚合
2. `WHERE id IN (...)` 批量抓取
3. 预加载 / eager loading
4. batch loader（按请求批量合并）

## 5. Safe Migration Checklist

### PostgreSQL

- 大表建索引优先 `CREATE INDEX CONCURRENTLY`
- 加非空列时，先加 nullable / default，再分批回填，再加约束
- 约束校验可用 `NOT VALID` + `VALIDATE CONSTRAINT`
- 长事务会拖住 vacuum 与 DDL，迁移窗口前先确认

示例：

```sql
ALTER TABLE posts ADD COLUMN view_count integer;

UPDATE posts
SET view_count = 0
WHERE view_count IS NULL;

ALTER TABLE posts
ALTER COLUMN view_count SET DEFAULT 0;

ALTER TABLE posts
ALTER COLUMN view_count SET NOT NULL;
```

### MySQL / PlanetScale

- 评估 online DDL 能力与元数据锁
- 大表优先考虑 gh-ost / pt-online-schema-change / deploy requests
- 变更顺序要兼容旧代码与新代码并行运行

## 6. Pooling and Runtime Notes

### PgBouncer / Supabase Pooler

- serverless 更适合 transaction pooling
- prepared statements 在 transaction pooling 下需要额外注意
- 避免长事务和 session 级状态依赖
- 连接池调优先看连接生命周期与复用，不要只调大连接数

### 应用侧排查

- 确认是否每个请求都新建连接
- 确认连接是否正确归还
- 检查 ORM 默认 pool size 与 serverless 并发模型是否冲突
- 把 DB timeout、statement timeout、idle timeout 分开理解

## 7. Recommended Output Template

```markdown
## 问题判断
- ...

## 证据
- ...

## 优化方案
1. ...
2. ...

## 风险与取舍
- ...

## 验证
- 跑 `EXPLAIN ANALYZE`
- 观察 p95 / p99、buffer hit、rows、lock wait
```
