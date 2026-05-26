# L0 全局上下文 — 客服 Agent

> 本文件定义 AICoding 交付的技术栈、架构约定、全局约束。所有 L1 模块和 L2 任务包均以此为基础。
> 来源：客服 Agent PRD（7 模块 + 四角色评审修复版）

## 技术栈（需研发确认后固化）

| 层级 | 技术选型 | 决策状态 | 备注 |
|:-----|:---------|:---------|:------|
| 前端嵌件 | Web Widget（JS SDK）| 待确认 | 嵌入商户交易所 Web 前端 |
| 后端服务 | 按团队现用方案 | 待确认 | 建议独立服务，不混入商户后台 |
| 向量数据库 | 见基础设施清单 | 研发决策 | M4 清单中 3 选 1 |
| LLM | 见基础设施清单 | 研发决策 | M4 清单中 4 选 1 |
| 缓存 | Redis | 建议 | — |
| 主数据库 | PostgreSQL（建议）| 建议 | — |
| 消息队列 | 按团队现用方案 | 待确认 | 异步任务和事件驱动 |
| 部署 | 商户可独立部署 | 架构决策 | SaaS 多租户 vs 混合云 |

## 项目目录结构

```
l0-l1-l2/
├── l0-context.md                       ← 本文件
├── modules/
│   ├── 01-agent-state-machine/
│   │   ├── l1-module-boundary.md        ← L1 模块边界
│   │   └── tasks/
│   │       ├── 001-state-machine-core.md
│   │       ├── 002-escalated-return.md
│   │       └── 003-idempotent-confirm.md
│   ├── 02-collaboration-funnel/
│   │   ├── l1-module-boundary.md
│   │   └── tasks/
│   ├── 03-confidence-threshold/
│   ├── 04-qa-engine/
│   │   └── tasks/
│   │       ├── 001-faq-retrieval.md
│   │       ├── 002-auth-middleware.md
│   │       ├── 003-tenant-isolation.md
│   │       └── 004-kyc-compliance.md
│   ├── 05-merchant-config/
│   ├── 06-eval-monitoring/
│   │   └── tasks/
│   │       ├── 001-offline-eval.md
│   │       ├── 002-grayscale-deploy.md
│   │       └── 003-p0-auto-disable.md
│   └── 07-error-audit/
└── spec/
    ├── openapi.yaml                     ← 结构化 API 契约
    └── state-machine.json               ← 状态机可编程制品
```

## 全局架构约定

1. **多租户隔离**：所有数据表/集合/缓存 Key 携带 `tenant_id` 字段
2. **幂等性**：所有资金/权限修改操作必须支持幂等（requestId 去重）
3. **审计日志**：敏感数据查询必须记录并可追溯
4. **身份认证**：涉及用户个人数据的 API 调用必须通过 JWT/API Token 鉴权
5. **错误码**：统一错误码段 — Agent 内部错误 2000-2999，API 调用错误 3000-3999
6. **日志**：所有 Agent 处理后端日志统一按 `agent:{tenant_id}:{session_id}` 格式组织
7. **响应时间**：P95 ≤ 5s，超过 5s 按异步处理
8. **超时**：外部 API 调用 5s 超时，embedding 搜索 3s 超时，链上数据 10s 超时

## 全局约束

- 不执行资金操作（提现审批、转账）——仅查询状态
- 不实质提交 KYC 资料——仅查询状态和引导
- LLM 回复末尾自动添加免责声明（硬编码不可删减）
- 高风险关键词（被盗/黑客/诉讼/冻结/监管举报）触发强制 L3
- 所有数据传输使用 HTTPS + TLS 1.3
