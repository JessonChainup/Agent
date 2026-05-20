---
spec_type: feature-standard
title: Google / Apple 社交登录集成
req_id: REQ-002
status: draft
owner_pm: Jesson / StaffOnewsbot
risk_level: medium
channels: [web, app-ios, app-android]
---

# 1. 一句话与成功指标

- **电梯稿**：在交易所 Web 端和 App 端集成 Google 登录和 Apple 登录，支持新用户一键注册登录、老用户绑定已有账户，同时按地区限制使用范围。
- **成功指标（可度量）**：
  - 注册转化率提升 ≥15%（接入后对比接入前，同周期线）
  - 登录页平均完成时间缩短 ≥40%
  - 密码找回相关客服工单量下降 ≥20%
- **护栏指标**（不能做坏什么）：
  - 现有邮箱/手机号登录转化率不下降
  - 社交登录导致的重复账户（一个人同时有社交账号和邮箱账号）比例 ≤ 用户总数 1%
  - 合规地区限制误拦截率 < 0.1%

# 2. 用户与场景

| Persona | 场景 | 当前痛点 |
|---------|------|----------|
| 新用户 Alice（Web，无账户） | 首次访问交易所网页，点击 Google 登录直接完成注册 | 需填写邮箱、验证码、设置密码，流程长放弃率高 |
| 新用户 Bob（iOS App，无账户） | 首次打开 App，点击 Sign in with Apple 一键注册 | 同上；iOS 用户期望原生登录体验 |
| 老用户 Carol 已有邮箱账户 | 在「安全设置」中绑定 Google 账号，以后可用 Google 直接登录 | 记不住密码，频繁找回 |
| 受限地区用户 Dave | 在受限制国家访问时，社交登录按钮不显示或提示不可用 | 无（合规要求） |

# 3. 当前行为 vs 期望行为

## 注册/登录（新用户）

| Step | Current | Desired |
|------|---------|---------|
| 1 | 点击「注册」填写邮箱→验证码→密码 | 点击「Google 登录」「Apple 登录」按钮 |
| 2 | - | 弹出 OAuth 授权页面 |
| 3 | - | 授权成功后，自动创建账户并登录 |
| 4 | 完成注册后进入主页 | 跳转到补充资料/KYC 页面 |

## 老用户关联

| Step | Current | Desired |
|------|---------|---------|
| 1 | 无关联入口 | 安全设置 - 绑定第三方账号 |
| 2 | - | 点击「绑定 Google」/「绑定 Apple」 |
| 3 | - | 授权成功后，第三方账号与当前账号关联 |
| 4 | 仅能用邮箱/手机登录 | 后续可用 Google/Apple 一键登录 |

## 地区限制

| Step | Current | Desired |
|------|---------|---------|
| 1 | 无限制 | 登录页面加载时检测用户 IP 地区 |
| 2 | - | 如果该地区不可用 → 隐藏社交登录按钮并显示提示 |
| 3 | - | 配置项由商户后台可管理（白名单/黑名单） |

# 4. 范围 / 非目标

- **In scope**：
  - Google 登录：Web（GIS SDK）+ App（Android/iOS Google Sign-In）
  - Apple 登录：Web（redirect_uri）+ App（ASAuthorizationController）
  - 新用户注册流程（通过社交登录首次自动注册）
  - 老用户绑定第三方账号（安全设置页面）
  - 地区限制（可配置白名单/黑名单国家代码列表）
  - 后端 id_token 验证、jwt 签发、用户关联逻辑
  - 统一账户模型扩展（关联表 `user_social_accounts`）

- **Out of scope**：
  - 不做其他社交登录（Facebook、Twitter、WeChat 等）
  - 不做 OAuth 登录跳过 KYC（KYC 流程位置不变）
  - 不改动现有邮箱/手机号登录流程
  - 不涉及自托管钱包的社交恢复功能

# 5. 方案概述

- **MVP 轮廓**：
  1. 后端新增 OAuth 认证模块（Google + Apple），处理 id_token 验证、用户匹配/创建、jwt 签发
  2. 数据库新增 `user_social_accounts` 表（user_id, provider, provider_account_id, email, created_at）
  3. 前端 Web 端在登录页新增 Google/Apple 按钮（根据地区限制显示/隐藏）
  4. App 端集成 Google Sign-In SDK + ASAuthorizationController
  5. 安全设置页新增绑定/解绑第三方账号入口
  6. 商户后台新增地区限制配置（国家代码列表、启用/禁用开关）

- **关键交互**（附状态/边界）：
  - OAuth 流程强制使用 nonce 防重放（Google Identity SDK 的 nonce 参数 / Apple ASAuthorizationController 的 nonce 属性）
  - 通过 Google 首次登录 → 自动创建账户 → 强制设置登录密码 → 强制绑定手机号 → 引导 KYC
  - 通过 Google 登录但此 Google 已绑定某账户 → 直接登录成功
  - 通过 Google 登录但此 Google **未绑定任何账户、且 id_token 中的 email 匹配 users 表中某已有账户** → 弹窗引导：输入该账户密码或短信验证码确认身份 → 自动绑定社交账号并登录
  - 通过 Google 登录但此 Google 未绑定任何账户且 email 不匹配 → 引导注册
  - Apple 隐藏邮箱模式下，中继邮箱唯一绑定，用户可后续在安全页设置常用邮箱
  - 地区受限 → 隐藏按钮 + 显示「您所在地区暂不支持此登录方式」
  - 已绑定 Google 账号的用户解绑 → 需有至少一种登录方式剩下的才能解绑

- **依赖团队**：法务（地区限制名单确认）、风控（恶意注册防刷策略）

# 6. Web3 / 资金 / 合规（交易线必填）

| 条目 | 说明 |
|------|------|
| 资金路径 | N/A（仅登录入口变更，不涉及资金操作） |
- **风控触点**：
  - nonce 防重放机制（OAuth replay 防护）
  - 社交登录注册场景：设备指纹采集 + 同一 IP/device 速率限制（每小时最多 N 次）
  - 同邮箱检测：匹配已有账户时要求密码或短信验证码验证身份
  - 社交登录注册用户强制设密码并绑定手机号（账户恢复保障）
| 对外口径 | 需法务确认：哪些国家地区限制使用 Google/Apple 登录；用户协议中更新第三方数据分享说明 |

# 7. 埋点与实验（可选）

| 事件 | 属性 | 用途 |
|------|------|------|
| social_login_click | provider (google/apple), platform (web/app) | 点击率统计 |
| social_login_success | provider, is_new_user | 转化漏斗 |
| social_login_failure | provider, error_reason | 问题诊断 |
| social_bind_click | provider | 绑定入口点击 |
| social_bind_success | provider | 绑定成功 |
| social_bind_unlink | provider | 解绑事件 |

# 8. Rollout / 灰度（可选）

- **策略**：先开放 Google 登录（Web），观察一周数据无问题后再开放 Apple 登录和 App 端
- **Kill switch**：商户后台「社交登录→全局开关」，关闭后隐藏所有社交登录按钮

---

## 评审已确认决定

以下问题在预审阶段提出，已确认解决方案并纳入 spec：

| 严重度 | 问题 | 决定 |
|:-----:|------|------|
| 🔴 | OAuth replay（缺少 nonce） | Google/Apple SDK 原生 nonce 参数 |
| 🔴 | 同邮箱重复账户 | 匹配时弹窗要求输入密码/短信验证码后绑定 |
| 🔴 | 社交登录绕过密码 | 首次社交登录后强制设密码 |
| 🔴 | 防刷策略失效 | 设备指纹 + 速率限制组合 |
| 🔴 | 账户不可恢复 | 强制绑定手机号 |
| 🟠 | 同一 Google 账号绑多个交易所账户 | 唯一活跃绑定，提示「已被绑定」引导解绑重绑 |
| 🟠 | Apple 跨设备 relay email | 身份匹配靠 sub 而非 email，中继邮箱仅通知用途 |
| 🟠 | Apple 私钥存储/轮转 | KMS 或加密存储 + 轮转告警，运维/安全确认方案 |
| 🟠 | 社交登录 + 2FA | 已有 2FA 用户须验证；新注册用户建议立即设置 2FA |
| 🟠 | 地区限制名单 | 法务确认 MVP 名单，开发前输出 |
| 🟠 | Apple 中继邮箱 KYC 验证 | KYC 流程允许用户手动修改邮箱 |
| 🟠 | 数据跨境 | 需法务评估（Google/Apple 服务器可能在境外） |

---

## 附录 A：AI Coding Handoff（与实现同步更新）

### H1. 仓库与运行假设

| 字段 | 内容 |
| ---- | ---- |
| 主仓库 / Monorepo 路径占位 | `services/api`（身份认证服务）、`apps/trade-web`（Web 前端）、`apps/trade-app`（移动端） |
| 受影响环境 | dev → staging → prod（灰度阶段区分） |
| Feature flag | `social_login_enabled` / `google_login_enabled` / `apple_login_enabled` |

### H2. 拟修改文件清单（猜测）

| Path | CONFIRMED/GUESS | 改动类型 |
| ---- | --------------- | -------- |
| `services/api/src/auth/social/` | GUESS | 新增目录：Google 验证服务、Apple 验证服务 |
| `services/api/src/auth/social/socialAuthController.ts` | GUESS | 新增：OAuth 回调处理 |
| `services/api/src/db/migrations/xxx_create_user_social_accounts.ts` | GUESS | 新增迁移 |
| `services/api/src/models/UserSocialAccount.ts` | GUESS | 新增 model |
| `apps/trade-web/src/pages/login.tsx` | GUESS | 新增社交登录按钮区域 |
| `apps/trade-web/src/pages/settings/security.tsx` | GUESS | 新增绑定/解绑入口 |
| `apps/trade-app/ios/...` | GUESS | Apple Sign-In 集成 |
| `apps/trade-app/android/...` | GUESS | Google Sign-In 集成 |
| `apps/admin-portal/...` | GUESS | 地区限制配置界面 |

### H3. 数据与契约

**REST 端点**：

| 方法 | 路径 | 用途 |
|------|------|------|
| POST | `api/v1/auth/social/google` | Google id_token 验证并登录/注册 |
| POST | `api/v1/auth/social/apple` | Apple id_token 验证并登录/注册 |
| POST | `api/v1/auth/social/bind` | 已登录用户绑定第三方账号 |
| POST | `api/v1/auth/social/unbind` | 已登录用户解绑第三方账号 |
| GET | `api/v1/auth/social/supported` | 获取当前地区支持的社交登录方式列表 |

**请求/响应（示例）**：

```json
// POST /api/v1/auth/social/google
// Request
{
  "id_token": "eyJhbGciOiJSUzI1NiIs...",
  "platform": "web"  // web | ios | android
}
// Response (新用户)
{ "token": "jwt...", "is_new_user": true, "user": { ... } }
// Response (老用户登录)
{ "token": "jwt...", "is_new_user": false, "user": { ... } }
// Response (错误)
{ "error": "invalid_token" }
```

**DB**：

```sql
CREATE TABLE user_social_accounts (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  provider VARCHAR(20) NOT NULL COMMENT 'google / apple',
  provider_account_id VARCHAR(255) NOT NULL COMMENT 'sub from id_token',
  email VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_provider_account (provider, provider_account_id),
  INDEX idx_user_id (user_id)
);
```

### H4. 验收标准

| AC# | 条件 | 期望结果 |
|-----|------|----------|
| AC-01 | 新用户在 Web 端点击 Google 登录并授权 | 自动创建账户、强制设置密码、强制绑定手机号、签发 jwt、跳转到 KYC 页 |
| AC-02 | 已绑定 Google 的用户点击 Google 登录 | 直接登录成功 |
| AC-03 | 用户点击 Apple 登录（隐藏邮箱模式） | 账户使用中继邮箱创建，强制设置密码+绑定手机号，绑定成功 |
| AC-04 | 已登录用户在安全设置绑定 Google | 关联成功，下次可用 Google 登录 |
| AC-05 | 用户解绑第三方账号（只剩一种登录方式） | 提示「需保留至少一种登录方式」，不执行 |
| AC-06 | 用户从受限地区访问 | 隐藏社交登录按钮，显示区域提示 |
| AC-07 | 商户后台关闭社交登录开关 | 全局隐藏社交登录按钮 |
| AC-08 | 无效 id_token | 返回 401，前端提示「登录失败，请重试」|
| AC-09 | 攻击者重放截获的 id_token | 后端验证 nonce，返回 401「token 已过期或无效」|
| AC-10 | Google id_token 的 email 匹配 users 表中某已有邮箱账户 | 弹窗引导输入该账户密码或短信验证码，验证通过后自动绑定社交账号并登录 |
| AC-11 | 同一 IP/device 短时间内多次社交注册 | 触发速率限制，返回 429「操作频繁，请稍后再试」|
| AC-12 | 社交注册用户忘记密码 | 通过绑定手机号找回密码（与现有找回流程一致）|

### H5. 非目标与非功能

| NFR | 指标 |
| --- | ---- |
| 性能 | 社交登录接口响应时间 < 500ms（id_token 验证 + jwt 签发）|
| 安全 | id_token 仅在后端验证，前端不处理签名；OAuth 流程强制使用 nonce 防重放；Apple 私钥应存储于 KMS 或加密存储并设置轮转告警（方案由运维/安全确认）|
| 2FA | 已有 2FA 的用户使用社交登录后须再完成 2FA 验证；新注册用户首次登录后建议立即设置 2FA |
| 兼容 | iOS 13+、Android 6+、主流浏览器（Chrome/Safari/Edge）|
| 风控 | 社交注册场景：设备指纹采集 + 同一 IP/device 速率限制（每小时最多 N 次，N 由风控确认）|

### H6. 回滚与灰度

- **Feature flag**：三层开关（全局 `social_login_enabled` + 各 provider 独立 flag）
- **灰度**：先开放 Google Web（可控 10% 用户），观察 3 天后再全量
- **回滚**：关闭 flag，同时确保 DB 表 `user_social_accounts` 删除不依赖现有登录流程（该表不影响原邮箱登录）
