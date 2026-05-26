# 001：商户配置 CRUD + 知识库管理

## 目标

实现商户后台上五个配置页面的 API 端点和知识库管理功能。

## 输入

- 配置项增/删/改/查请求
- FAQ 条目管理
- 文档上传（PDF/Markdown）

## 输出

- 配置持久化到 DB
- 知识库 embedding 重建事件（触发向量数据库更新）

## 编码范围

```
backend/src/
├── api/
│   ├── MerchantConfigController.ts  // 配置 API
│   └── KnowledgeBaseController.ts   // 知识库 API
├── domain/
│   ├── MerchantConfig.ts
│   └── FaqEntry.ts
├── service/
│   ├── ConfigService.ts
│   └── KnowledgeBaseService.ts      // FAQ CRUD + 文档切片 + 索引
└── infra/
    └── ConfigRepo.ts
```

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 全局开关生效 | HUMAN-VERIFY | 关闭后新消息转人工，已有会话完成 |
| 2 | 阈值覆盖生效 | AI-VERIFY | 商户设全自动阈值 90% → query 中带新阈值 |
| 3 | FAQ 增删改 | AI-VERIFY | 新增 FAQ → 用户匹配新答案 |
| 4 | 知识库批量导入 | AI-VERIFY | 上传 300 条 CSV → 导入成功，无效行跳过 |
| 5 | 搜索测试 | AI-VERIFY | 测试问题 → 返回 Top 5 + 匹配分 |
| 6 | 日处理上限 | AI-VERIFY | 超限后新会话转人工 |

## Mock 清单

- `MockVectorStore`：按商户隔离的向量库

## 不可做

- 不包含监控统计数据（M6 处理）
- 不包含前端页面渲染（仅 API）
