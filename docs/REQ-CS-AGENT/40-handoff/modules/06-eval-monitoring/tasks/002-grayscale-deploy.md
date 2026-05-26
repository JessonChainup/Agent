# 002：灰度部署引擎

## 目标

实现三阶段灰度发布引擎，支持影子模式、比例灰度、场景灰度，并管理回滚快照。

## 输入

- 灰度配置（当前 Phase、比例、开放场景列表）
- 用户请求上下文

## 输出

- Agent 并行处理但不展示（影子模式）
- 按比例/场景分配用户走 Agent
- 回滚事件（触发回退到快照）

## 编码范围

```
backend/src/
├── service/
│   └── GrayscaleService.ts        // 灰度引擎
├── domain/
│   └── GrayscaleConfig.ts          // 灰度配置实体
```

## 验收标准

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | 影子模式不展示 | AI-VERIFY | Phase 1 → Agent 处理但不展示给用户 |
| 2 | 比例灰度 | AI-VERIFY | Phase 2 20% → 新会话 20% 走 Agent，80% 纯人工 |
| 3 | 场景灰度 | AI-VERIFY | 仅 FAQ + 充提 → KYC/交易/Gas 仍走纯人工 |
| 4 | 一键回滚 | AI-VERIFY | 触发回滚 → 5min 内自动回复关闭 |
| 5 | 回滚快照保留 | AI-VERIFY | 回退到 Phase 2 配置 → Agent 行为匹配快照 |

## Mock 清单

- `MockUserAllocator`：模拟按百分比分配用户逻辑

## 不可做

- 不包含商户配置界面（M5 处理）
- 不包含真实用户分流（依赖前端或网关）
