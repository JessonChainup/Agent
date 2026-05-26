# L1 模块边界：05—商户配置

## 模块职责

提供商户在后台对客服 Agent 的管理界面，包括全局开关、阈值配置、知识库管理、安全限制和监控面板。

## 输入

- 商户管理员的操作事件（增/删/改配置）
- 知识库文档上传（PDF/Markdown）
- 搜索测试请求

## 输出

- 配置变更事件（影响 M3 阈值和 M4 问答引擎行为）
- 知识库 embedding 重建事件

## 配置页

1. 基础开关（全局启用/停用、入口显示、服务语言）
2. 自动回复规则（三级阈值、超时、矛盾次数、高风险模式）
3. 知识库管理（FAQ CRUD、文档上传/切片、搜索测试、版本回滚）
4. 安全限制（敏感词、高风险操作类型、日处理上限、IP 白名单）
5. 监控统计（只读看板，数据来自 M6）

## 核心实体

```
MerchantConfig {
  tenantId: string
  autoReplyEnabled: boolean
  globalEnabled: boolean
  autoThreshold: number         // 默认 80
  confirmTimeoutMs: number      // 默认 120000
  contradictionLimit: number    // 默认 2
  highRiskLock: boolean         // 默认 true
  sensitiveKeywords: string[]
  dailyLimit: number            // 0=不限制
  language: string[]
  createdAt: datetime
  updatedAt: datetime
}
```

## 依赖

- M3（阈值配置引用）
- M6（监控数据来源）
