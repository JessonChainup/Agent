# 003：多租户隔离数据访问层

## 目标

实现数据访问层的多租户隔离，确保知识库检索、对话日志、缓存数据不跨商户泄露。

## 输入

- 每个 API 请求携带 `tenant_id` 参数

## 输出

- 所有数据查询强制限制在本商户范围内

## 编码范围

```
backend/src/
├── middleware/
│   └── TenantMiddleware.ts    // tenant_id 强制注入
├── infra/
│   ├── TenantAwareRepo.ts     // 带 tenant_id 过滤的仓储基类
│   ├── VectorStore.ts         // 向量库隔离（独立 Collection）
│   └── RedisCache.ts          // Redis Key 前缀隔离
```

## 隔离策略

| 维度 | 实现 |
|:-----|:------|
| 知识库向量检索 | 独立 Collection `faq_{tenant_id}` |
| 对话日志 | DB 表含有 `tenant_id` 字段，查询强制 AND tenant_id = ? |
| Redis 缓存 | Key 前缀 `agent:{tenant_id}:` |
| API 访问 | 未携带 tenant_id 参数 → 拒绝 |

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 知识库检索隔离 | AI-VERIFY | 商户 A 查"ETH 费率" → 只查商户 A 的知识库 |
| 2 | 对话日志隔离 | AI-VERIFY | 商户 A 管理员查日志 → 只返回商户 A 数据 |
| 3 | Redis 隔离 | AI-VERIFY | Key 以 `agent:{tenant_id}:` 为前缀 |
| 4 | 未授权商户拦截 | AI-VERIFY | 不在白名单的商户请求 → 拒绝 |
| 5 | 无 tenant_id 拒绝 | AI-VERIFY | 请求无 tenant_id → 拒绝 + 返回 400 |

## Mock 清单

- `MockTenantAwareVectorStore`：按 tenant_id 分 Collection 的模拟向量库
- `MockTenantAwareDb`：按 tenant_id 过滤的模拟数据库

## 不可做

- 不包含商户白名单的配置界面（M5 处理）
- 不包含 Schema 级隔离的 DDL 脚本（研发自行决定）
