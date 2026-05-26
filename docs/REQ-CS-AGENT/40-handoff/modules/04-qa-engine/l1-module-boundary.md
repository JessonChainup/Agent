# L1 模块边界：04—AI 问答引擎

## 模块职责

实现六大场景（FAQ/账户/充提/KYC/交易/Gas）的处理流程，包括分类路由、参数识别、数据获取和输出模板。作为数据安全的第一道防线，同时实现终端用户身份认证和多租户隔离。

## 输入

- 用户输入消息（已通过输入安全检测）
- 当前实例状态（从 M1 获取）
- 商户知识库数据（从 M5 读取）

## 输出

- 场景分类结果 + 置信度因子明细
- 各场景的模板化回复

## 场景映射

| 场景 | 典型输入 | 是否需要身份认证 |
|:-----|:---------|:----------------|
| FAQ | 手续费是多少 | 否 |
| 账户管理 | 我的限额多少 | 是 |
| 充值与提现 | 提现没到账 | 是 |
| KYC | 认证为什么没通过 | 是 |
| 交易操作 | 订单状态 | 是 |
| Gas 费用 | 网络拥堵吗 | 否 |

## 通用处理流程

```
用户输入 → 输入安全检测 → 身份认证（涉及个人数据时）→ 分类路由 → 场景匹配 → 参数识别 → 数据获取 → 置信度计算 → 输出
```

## 核心实体

```
SceneClassification {
  sceneId: string           // FAQ/ACCOUNT/DEPOSIT_WITHDRAW/KYC/TRADE/GAS
  sceneName: string
  subScene: string|null     // 子场景代码
  confidence: float
  params: Record<string, any>  // 提取的参数（币种、txId 等）
}

AuthSession {
  sessionId: string
  userId: string
  tokenType: JWT|API_KEY|SESSION
  token: string
  expiresAt: datetime
  isAuthenticated: boolean
}
```

## 错误码段

- 2401：身份认证失败
- 2402：场景分类失败（全局匹配度 < 30%）
- 2403：参数提取失败
- 2404：内部 API 超时
- 2405：越权查询
- 2406：API 限流（30 次/分钟超限）

## 依赖

- M1（状态定义）
- M2（分流决策）
- M3（置信度计算输入因子）
- M5（知识库数据）
