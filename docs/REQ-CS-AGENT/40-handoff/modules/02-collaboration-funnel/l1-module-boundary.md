# L1 模块边界：02—三级协作漏斗

## 模块职责

根据置信度将用户请求分配到 L1（全自动）、L2（确认）、L3（人工）三个层级，管理确认卡片的生成、超时和升级。

## 输入

- 用户输入（从实例状态机接收 `instanceId + message`）
- 置信度分数（从 M3 置信度引擎接收）
- 用户确认/取消操作（从前端接收）
- 超时信号（120s）

## 输出

- L1：直接回复用户
- L2：确认卡片（操作预览 + 确认/取消按钮）
- L3：上下文摘要 + 转人工事件
- 升级事件（L1→L2→L3）

## 核心逻辑

```
用户输入 → M3 置信度计算 → L1/L2/L3 分流:
  ≥ 80%  → L1：直接回复
  50-79% → L2：生成确认卡片，等待 120s
  < 50%  → L3：转人工
  高风险关键词 → 强制 L3（跳过置信度）
```

## 核心实体

```
L2Confirmation {
  requestId: string        // 幂等去重标识
  instanceId: string
  operationPreview: string  // 操作预览
  impact: string            // 影响范围
  status: PENDING|CONFIRMED|CANCELLED|TIMEOUT
  createdAt: datetime
  expiresAt: datetime       // created + 120s
}

L3Transfer {
  instanceId: string
  summary: string           // 脱敏后的问题摘要
  fullHistoryHash: string   // 全量对话历史的 hash（按需获取）
  transferredAt: datetime
}
```

## 幂等和并发规则

- 确认卡片携带唯一 `requestId`，5s 内重复请求去重
- 确认后卡片 UI 锁定（按钮置灰）
- WAITING_FOR_CONFIRM 状态下新消息追加上下文，不退出状态
- 连续 2 次 L2 确认矛盾 → 升级 L3

## 错误码段

- 2101：无效的确认操作
- 2102：确认超时
- 2103：重复 requestId

## 依赖

- M1 状态机（状态定义和实例生命周期）
- M3 置信度阈值（置信度计算和分档）
