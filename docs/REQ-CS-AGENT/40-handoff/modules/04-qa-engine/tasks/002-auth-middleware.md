# 002：终端用户身份认证中间件

## 目标

实现用户身份认证中间件，在涉及用户个人数据（账户余额/充提记录/KYC/交易）时强制鉴权。

## 输入

- HTTP 请求头（`Authorization: Bearer <token>` 或 `X-API-Key: <key>`）
- 当前会话上下文

## 输出

- 认证通过时：`AuthSession`（含 userId, tenantId, sessionId）
- 认证失败时：401 响应 + "请先登录后查询个人账户信息"

## 编码范围

```
backend/src/
├── middleware/
│   └── AuthMiddleware.ts      // 身份认证中间件
├── service/
│   └── AuthService.ts         // Token 解析/验签
├── infra/
│   └── JwtProvider.ts         // JWT 验证（依赖交易所用户系统）
```

## 认证流程

1. 从请求头提取 Token
2. Token 有效且未过期 → 解析 Token 得到 userId + tenantId
3. 无 Token 或已过期 → 判断当前场景是否需要个人数据
   - 需要 → 返回 401
   - 不需要（FAQ/Gas）→ 跳过认证
4. 认证通过后会话级别缓存（不重复验证）

## API 鉴权约束

- `signature = HMAC-SHA256({userId}:{merchantId}:{timestamp}:{nonce})`
- 时间戳与服务器差超过 60s → 拒绝
- 单 userId 查询 ≤ 30 次/分钟 → 限流

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 已登录自动认证 | AI-VERIFY | 携带有效 JWT → 解析得到 userId → 继续查询 |
| 2 | 未登录引导登录 | AI-VERIFY | 无 Token → 返回 401 + 引导提示 |
| 3 | 越权查询拦截 | AI-VERIFY | 用户 A 查用户 B 数据 → 拒绝 + 审计日志 |
| 4 | API 限流 | AI-VERIFY | 30 次/分钟超限 → 返回 429 + 冷却 5min |
| 5 | FAQ 场景跳过认证 | AI-VERIFY | FAQ 查询无 Token → 跳过认证 → 正常回复 |

## Mock 清单

- `MockJwtProvider`：预置合法/非法 Token 用于测试
- `MockAuthCache`：会话级别认证状态缓存

## 不可做

- 不包含 Token 的生成（由交易所用户系统生成）
- 不包含用户登录页面（由商户前端提供）
