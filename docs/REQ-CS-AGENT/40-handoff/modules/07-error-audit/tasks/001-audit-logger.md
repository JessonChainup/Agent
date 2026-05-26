# 001：审计日志写入和查询服务

## 目标

实现审计日志的追加写入（不可篡改）、按多租户隔离查询、自动脱敏和过期清理。

## 输入

- 每次会话处理完成后的审计事件对象
- 商户管理员的查询请求

## 输出

- 持久化到审计日志表
- 审计查询结果（按时间/场景/漏斗级别/满意度过滤）

## 编码范围

```
backend/src/
├── domain/
│   └── AuditLog.ts              // 审计日志实体
├── service/
│   ├── AuditLogger.ts           // 追加写日志
│   └── AuditQueryService.ts     // 商户侧审计查询
├── infra/
│   ├── AuditLogRepo.ts          // 仅支持 INSERT + SELECT
│   └── DataMasker.ts            // 脱敏处理
```

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 日志不可篡改 | AI-VERIFY | 写入后尝试 UPDATE/DELETE → 被拒绝 |
| 2 | 日志脱敏 | AI-VERIFY | 输入含"1A1zP1e..." → 存为[REDACTED] |
| 3 | 多租户隔离 | AI-VERIFY | 商户 A 查询 → 只返回商户 A 数据 |
| 4 | 180 天清理 | AI-VERIFY | 超期日志自动归档，KYC 相关 30 天清理 |
| 5 | 审计查询过滤 | AI-VERIFY | 按时间/场景/漏斗级别过滤返回值正确 |

## Mock 清单

- `MockAuditLogRepo`：内存追加存储，模拟不可篡改

## 不可做

- 不包含数据删除的用户请求流程（外部系统触发）
