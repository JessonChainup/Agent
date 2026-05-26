# L1 模块边界：01—Agent 状态机

## 模块职责

定义 Agent 实例状态机和任务状态机的完整生命周期，包含状态迁移、超时处理和幂等保护。

## 输入

- 用户输入消息（来自前端嵌件 WebSocket/HTTP）
- 人工客服回调（"处理完成"）
- 系统超时信号（10min/120s/30s）

## 输出

- 状态变更事件（推送给 M2 协作漏斗和 M4 问答引擎）
- 确认卡片事件（推送给前端的 L2 卡片渲染）
- 转人工事件（推送给商户客服系统）

## 状态机定义

### 实例状态机

7 个状态，16 条迁移（详见 M1 模块 PRD 的状态迁移总表）

### 任务状态机

5 个状态 + 1 个失败终止：PENDING → MATCHING → CLARIFYING → EXECUTING → CONFIRMING → COMPLETED / FAILED

## 核心实体

```
AgentInstance {
  instanceId: string          // 全局唯一
  tenantId: string            // 租户 ID（多租户隔离）
  userId: string              // 终端用户 ID
  state: AgentState enum      // 当前实例状态
  currentTaskId: string|null  // 当前任务 ID
  sessionContext: Session     // 会话上下文
  createdAt: datetime
  updatedAt: datetime
  expiresAt: datetime         // INACTIVE 超时时间（最后活跃 + 10min）
}

AgentTask {
  taskId: string
  instanceId: string
  state: TaskState enum
  requestId: string           // 用于幂等去重
  input: string               // 用户输入
  intent: string|null         // 意图分类
  confidence: float           // 置信度
  result: any|null            // 处理结果
  createdAt: datetime
}
```

## 错误码段

- 2001：状态机非法转移
- 2002：重复 requestId
- 2003：任务超时
- 2004：实例已过期
- 2005：并发冲突（version 校验失败）

## 依赖

- 无（最底层模块，其他模块均依赖本模块的状态定义）
