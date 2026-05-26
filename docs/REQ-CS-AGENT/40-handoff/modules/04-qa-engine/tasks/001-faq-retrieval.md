# 001：FAQ 检索与场景路由

## 目标

实现基于 embedding 语义匹配的场景分类路由引擎，支持六大场景的分类和 FAQ 知识库检索。

## 输入

- 用户输入文本（已通过安全检测）
- 商户知识库 embedding 索引（从向量数据库加载）

## 输出

- 场景分类结果（`SceneClassification`）
- FAQ 匹配结果（如场景为 FAQ）
- embedding 匹配分数（作为置信度计算因子「语义匹配度」的输入）

## 编码范围

```
backend/src/
├── service/
│   ├── SceneRouter.ts        // 场景分类路由
│   └── FaqRetriever.ts       // FAQ 知识库检索
├── infra/
│   └── VectorStore.ts        // 向量数据库接口（适配器模式）
```

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | FAQ 命中返回答案 | AI-VERIFY | 输入"手续费多少"→ 知识库匹配 → 输出答案 |
| 2 | FAQ 未命中转 L3 | AI-VERIFY | 知识库无匹配 → 返回"未收录" → 转 L3 |
| 3 | 场景分类正确 | AI-VERIFY | "我的提现呢" → 分类为充提场景 |
| 4 | 全局匹配度 < 30% 未识别 | AI-VERIFY | 无关输入 → 未识别 → 转 L3 |
| 5 | 知识库多租户隔离 | AI-VERIFY | 商户 A 和商户 B 的知识库独立检索，不跨商户 |

## Mock 清单

- `MockVectorStore`：内存向量检索，支持按 tenant_id 隔离
- `MockKnowledgeBase`：预置测试 FAQ 条目

## 不可做

- 不包含身份认证（任务 002 处理）
- 不包含多租户隔离完整方案（任务 003 处理）
- 不包含 KYC/充提等个人数据场景（任务 004/005/006 处理）
