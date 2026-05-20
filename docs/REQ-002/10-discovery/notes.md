# REQ-002: Discovery Notes — Google/Apple 社交登录

## 竞品对标

参照主流 CEX 社交登录实现对比：

| 维度 | Binance | Coinbase | Bybit | Chainup（当前） | 目标态 |
|------|---------|----------|-------|---------------|--------|
| Google 登录 | ✅ Web + App | ✅ Web + App | ✅ Web + App | ❌ | ✅ |
| Apple 登录 | ✅ Web + App | ✅ Web + App | ✅ iOS App | ❌ | ✅ |
| 老用户关联 | ✅ 绑定已有账户 | ✅ 绑定已有账户 | ✅ 绑定已有账户 | - | ✅ |
| 隐藏邮箱 | - | ✅（Apple 中继） | ✅（Apple 中继）| - | ✅ |
| 地区限制 | ✅ | ✅ | ✅ | - | ✅ |
| KYC 流程位置 | 登录后 | 登录后 | 登录后 | 登录后 | 登录后 |
| 登录方式 | OAuth 2.0 code flow | OAuth 2.0 | OAuth 2.0 | 邮箱+短信 | OAuth 2.0 |

## 技术选型要点

### Google 登录
- 使用 Google Identity Services (GIS) 库
- 返回 id_token（JWT），包含 email、name、sub（唯一用户 ID）
- Web 端：GIS 弹窗模式；App 端：Google Sign-In SDK
- 后端验证 id_token：通过 Google 公钥验证签名

### Apple 登录（Sign in with Apple）
- Apple 强制要求使用原生按钮样式
- 返回 id_token（JWT），包含 sub（唯一用户 ID）、email（可选隐藏）
- "Hide My Email" 模式返回 `xxx@privaterelay.appleid.com` 中继邮箱
- 需 Apple Developer Program 账号
- Web 端：redirect_uri 回调；App 端：ASAuthorizationController
- 后端验证：通过 Apple 公钥验证 id_token 签名

### 地区限制策略
- 通过 IP/GeoIP 判断请求来源地区
- 白名单/黑名单地区配置（可配置化由商户后台控制）
- 登录流程开始时检测 → 不符合条件则隐藏社交登录按钮或提示

## 技术风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Apple 隐藏邮箱导致用户找不到账户 | 用户无法找回密码 | 提示用户首次登录后绑定邮箱 |
| 跨端 Apple 登录 token 不通用 | 用户困惑 | Web 端用 redirect_uri、App 端用 native SDK，后端统一 jwt |
| OAuth 凭证泄露 | 恶意注册 | 凭证存在安全存储，定期轮换 |
| 地区限制误判（CDN IP 等） | 正常用户无法使用 | 支持商户自定义白名单+兜底提示 |

## 用户侧流程对齐

### 新用户注册流程
1. 打开登录/注册页面
2. 点击「Google 登录」或「Apple 登录」
3. 浏览器/系统弹出 OAuth 授权页
4. 授权成功后，系统自动创建账户并登录
5. 自动跳转到补充资料/KYC 页面

### 老用户关联流程
1. 用户已登录（邮箱/手机号）
2. 进入「安全设置 / 绑定第三方账号」
3. 点击「绑定 Google」或「绑定 Apple」
4. 授权成功后，第三方账号与当前账号关联
5. 后续可用该第三方账号登录

### 登录流程
1. 点击「Google 登录」或「Apple 登录」
2. 授权成功后，后端通过 sub/id_token 查找关联的本地账户
3. 找到 → 登录成功；找不到 → 引导注册
