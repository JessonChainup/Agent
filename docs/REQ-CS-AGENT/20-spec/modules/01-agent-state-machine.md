## M1：Agent 状态机

### 概述

定义客服 Agent 的两层状态机——实例状态机（Agent 实例的完整生命周期）和任务状态机（单次请求的处理过程）。

### 实例状态机（修复版）

实例状态机定义 Agent 整体的生命周期，包含新增加的回归路径来解决原版本的死循环问题。

```
                    ┌──────────────┐
                    │              │
                    ▼              │
              ┌──────────┐        │ 新请求 / 超时回归
         ┌───►│ INACTIVE │◄───────┼──────────────┐
         │    └─────┬────┘        │              │
         │          │命中FAQ/查询  │              │
         │          ▼             │              │
         │    ┌──────────┐       │              │
         │    │  ACTIVE  │───────┼──► 完成 →     │
         │    └─────┬────┘       │  从 COMPLETED │
         │          │L2确认      │   超时回归     │
         │          ▼            │              │
         │ ┌──────────────────┐ │              │
         │ │WAITING_FOR_      │ │              │
         │ │  CONFIRM         │ │              │
         │ └────────┬─────────┘ │              │
         │          │用户确认   │              │
         │          ▼           │              │
         │    ┌──────────┐     │              │
         │    │PROCESSING│     │              │
         │    └─────┬────┘     │              │
         │          │成功/失败  │              │
         │          ▼           │              │
         │    ┌──────────┐     │              │
         │    │COMPLETED │──────┘              │
         │    └─────┬────┘                    │
         │          │L3升级（超时→人工处理完）  │
         │          ▼                          │
         │    ┌──────────┐                    │
         │    │ESCALATED │────────────────────┘
         │    └─────┬────┘  人工处理完成
         │          │ERROR
         │          ▼
         │    ┌──────────┐
         └────┤  ERROR   │
              └──────────┘
```

**状态定义**：

| 状态 | 说明 | 进入条件 | 超时策略 |
|:-----|:-----|:---------|:---------|
| INACTIVE | 空闲，无活跃会话 | 初始状态 / COMPLETED 超时 10min / ESCALATED 人工处理完成 / ERROR 用户新请求 | 无（本身就是空闲）|
| ACTIVE | 正在处理用户请求 | 用户输入命中 FAQ 或查询逻辑 | 无（同步处理）|
| WAITING_FOR_CONFIRM | 等待用户确认（L2） | 置信度 50%-79% 或涉及限额/权限变更 | 120s 超时→升级 ESCALATED |
| PROCESSING | 执行中 | 用户确认 L2 操作 | 30s 超时→ERROR |
| COMPLETED | 处理完成 | 执行成功 / L1 完成 | 10min 无新消息→回退 INACTIVE |
| ESCALATED | 已转人工 | L2 超时 / L3 条件触发 | 无（等待人工客服处理完成回调）|
| ERROR | 执行异常 | 执行中出错 / L2 确认取消 | 用户发送新请求→回退 INACTIVE |

**状态迁移总表**（v2 修复版）：

| 当前状态 | 触发事件 | 下一状态 | 条件 |
|:---------|:---------|:---------|:-----|
| INACTIVE | 用户输入 | ACTIVE | 命中 FAQ 或查询逻辑，置信度 ≥ 50% |
| ACTIVE | 置信度 ≥ 80% | COMPLETED | L1 直接返回结果 |
| ACTIVE | 置信度 50%-79% | WAITING_FOR_CONFIRM | 需用户确认 |
| ACTIVE | 置信度 < 50% | ESCALATED | 直接转人工 |
| ACTIVE | 触发资金/安全/合规条件 | ESCALATED | 强制 L3 |
| WAITING_FOR_CONFIRM | 用户确认 | PROCESSING | — |
| WAITING_FOR_CONFIRM | 用户取消 | ERROR | — |
| WAITING_FOR_CONFIRM | 超时 120s | ESCALATED | 用户未响应 |
| WAITING_FOR_CONFIRM | 用户发新消息（与当前确认无关）| 维持 WAITING_FOR_CONFIRM | 新消息追加为上下文，不替换确认 |
| PROCESSING | 执行成功 | COMPLETED | — |
| PROCESSING | 执行异常 | ERROR | — |
| PROCESSING | 超时 30s | ERROR | — |
| COMPLETED | 10min 无新消息 | INACTIVE | 超时回归 |
| COMPLETED | 用户新消息（10min 内）| ACTIVE | 续用同一实例 |
| ESCALATED | 人工客服回调"处理完成" | INACTIVE | 明确回归路径 |
| ESCALATED | 用户新消息（短会话内）| ACTIVE | 人工还未接手 |
| ERROR | 用户新请求 | ACTIVE | 用户重试 |
| ERROR | 用户关闭会话 | INACTIVE | 会话结束 |

### 任务状态机

任务状态机定义单次请求的微观处理过程，独立于实例状态机运行。一个实例可以串行执行多个任务。

```
PENDING → MATCHING → CLARIFYING → EXECUTING → CONFIRMING → COMPLETED
                                                              ↘  FAILED
```

### 验收标准

**AC-SM-01：COMPLETED 超时回归**
- Given Agent 处于 COMPLETED 状态
- When 10min 内无新消息
- Then 实例自动回退到 INACTIVE 状态
- And 释放占用的资源（上下文、临时数据）

**AC-SM-02：ESCALATED 人工完成回归**
- Given Agent 已转人工（ESCALATED）
- When 人工客服发起"处理完成"回调
- Then 实例回退到 INACTIVE 状态
- And 记录该会话的最终状态为"人工处理完成"

**AC-SM-03：重复确认去重（幂等）**
- Given 已发出 L2 确认卡片（requestId=abc123）
- When 用户在 5s 内重复点击确认
- Then 后端识别重复请求（requestId 相同）
- And 只执行一次操作
- And 返回已处理的确认结果

**AC-SM-04：WAITING_FOR_CONFIRM 并发消息**
- Given Agent 处于 WAITING_FOR_CONFIRM 状态
- When 用户发送新消息
- Then 新消息追加为当前确认的上下文
- And WAITING_FOR_CONFIRM 状态不退出
- And 确认卡片仍然有效

**AC-SM-05：ERROR 用户重试**
- Given Agent 处于 ERROR 状态（执行异常）
- When 用户发送新请求
- Then 实例回到 ACTIVE 重新处理
- And 保留原有上下文作为参考

**AC-SM-06：PENDING 超时转异步**
- Given 任务进入 PENDING 状态
- When 超过 5s 未进入下一状态
- Then 任务标记为异步处理
- And 用户收到"已收到请求，处理中请稍候"提示

### 修复记录

| 版本 | 修复内容 |
|:-----|:---------|
| v1（原始版） | 6 状态 + 7 状态迁移，L3 转人工后无回归路径，COMPLETED 无超时回归 |
| v2（本版） | 新增 ESCALATED 状态（独立的 L3 人工标记状态）+ COMPLETED 10min 超时回归 + ERROR 用户重试路径 + 并发消息处理规则 + 幂等确认去重 |
