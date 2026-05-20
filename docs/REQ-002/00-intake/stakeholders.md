# REQ-002: Stakeholders

| 角色 | 利益 | 参与阶段 |
|------|------|----------|
| 终端用户（交易所注册用户） | 注册/登录流程更快捷 | 体验评审 |
| 商户（交易所运营方） | 提升用户注册转化、降低客服密码找回压力 | DISCOVERY 访谈 |
| Chainup 开发团队 | 后端 OAuth 集成、前端 SDK 调用、合规地区限制逻辑 | SPEC → AICODE |
| 合规/法务 | 限制特定国家/地区使用 Google/Apple 登录（受当地法规限制） | SPEC 评审 |
| 运维/安全 | OAuth 凭证管理、jwt/refresh token 落地、防恶意注册 | SPEC 评审 |
| 测试 | 多端（App+Web）+ 多登录方式交叉测试 | QA 阶段 |
