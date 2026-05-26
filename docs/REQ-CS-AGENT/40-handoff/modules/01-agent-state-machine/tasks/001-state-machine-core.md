# 001：状态机核心实现

## 目标

实现 Agent 实例状态机和任务状态机的核心状态迁移逻辑，包括 7 个状态、16 条迁移、超时处理和状态持久化。

## 输入

- 初始化的 AgentInstance 对象（调用 `createInstance(tenantId, userId)`）
- 用户消息（`processMessage(instanceId, message)`）

## 输出

- 状态变更事件（`InstanceStateChangedEvent` / `TaskStateChangedEvent`）
- 确认卡片事件（当状态转为 WAITING_FOR_CONFIRM）
- 转人工事件（当状态转为 ESCALATED）

## 编码范围

```
backend/src/
├── domain/
│   ├── AgentInstance.ts        // 实体定义
│   ├── AgentTask.ts             // 任务实体
│   ├── AgentState.ts            // 状态枚举 + 迁移定义
│   └── AgentInstanceRepo.ts     // 仓储接口
├── service/
│   └── AgentStateMachine.ts     // 状态机引擎
└── event/
    └── InstanceEvent.ts         // 事件定义
```

## 验收标准

引用了 M1 模块的 AC-SM-01 到 AC-SM-06。

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | AC-SM-01 COMPLETED 10min 回归 | AI-VERIFY | 创建实例 → 完成 → 等待 10min → 状态变为 INACTIVE |
| 2 | AC-SM-02 ESCALATED 人工回调 | AI-VERIFY | 实例 ESCALATED → 调用 completeEscalation → 状态变为 INACTIVE |
| 3 | AC-SM-03 重复确认去重 | AI-VERIFY | 同 requestId 重复调用 → 第二次返回已处理结果 |
| 4 | AC-SM-04 并发消息 | AI-VERIFY | WAITING_FOR_CONFIRM 状态收到新消息 → 追加上下文 |
| 5 | AC-SM-05 ERROR 重试 | AI-VERIFY | ERROR → 新消息 → 进入 ACTIVE |
| 6 | AC-SM-06 PENDING 超时 | AI-VERIFY | 任务 PENDING > 5s → 标记异步 |
| 7 | 非法迁移拒绝 | HUMAN-VERIFY | ACTIVE 直接 → ERROR → 拒绝，返回错误码 2001 |

## Mock 清单

- `MockInstanceRepo`：内存存储，支持 `save` / `findById` / `findByUserId`
- `MockTimerService`：可手动触发超时，不依赖真实时间

## 不可做

- 不包含用户输入的安全检测（由 M4 问答引擎处理）
- 不包含 L2 确认卡片的 UI 渲染（由前端嵌件处理）
- 不包含 embedding 语义匹配（由 M4 问答引擎处理）
