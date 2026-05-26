# 001：五因子置信度计算引擎

## 目标

实现五因子加权置信度计算函数，支持商户阈值覆盖和自动调优。

## 输入

- `calculateConfidence(factors: ConfidenceFactors, merchantConfig: MerchantConfig): number`
- `factors` 包含：semanticScore, clarityScore, contextScore, riskScore, historyScore

## 输出

- 置信度分数（0-100）
- 分档文本（high/medium/low）
- 因子明细（用于审计日志）

## 编码范围

```
backend/src/
├── domain/
│   └── ConfidenceFactors.ts    // 因子实体
├── service/
│   └── ConfidenceEngine.ts     // 置信度计算引擎
```

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 高置信度 L1 | AI-VERIFY | 各因子总分 ≥ 80% → 返回 high + L1 |
| 2 | 中置信度 L2 | AI-VERIFY | 总分 50-79% → 返回 medium + L2 |
| 3 | 低置信度 L3 | AI-VERIFY | 总分 < 50% → 返回 low + L3 |
| 4 | 商户阈值覆盖 | AI-VERIFY | 商户设全自动阈值 90% → 85% 分进入 L2 而非 L1 |
| 5 | 高风险关键词强制 L3 | AI-VERIFY | 输入含"被盗"/"黑客" → 跳过计算，直接返回 L3 |
| 6 | 因子明细输出 | AI-VERIFY | 计算结果含各因子原始分和加权分 |

## Mock 清单

- `MockFactorProvider`：模拟各因子输入值

## 不可做

- 不包含 embedding 向量搜索（M4 处理）
- 不包含意图分类（M4 处理）
- 不包含商户配置的持久化（M5 处理）
