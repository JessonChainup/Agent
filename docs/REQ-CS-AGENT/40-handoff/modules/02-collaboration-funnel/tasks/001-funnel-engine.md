# 001：三级分流引擎

## 目标

实现根据置信度将请求分配到 L1/L2/L3 的核心分流逻辑，包括确认卡片的生成、超时处理和升级条件判断。

## 输入

- `classifyRequest(instanceId, confidence, userInput)` 调用
- `handleConfirmation(requestId, action: confirm|cancel)` 调用
- 120s 超时信号

## 输出

- `L1ResponseEvent` / `L2ConfirmEvent` / `L3TransferEvent`

## 编码范围

```
backend/src/
├── domain/
│   ├── L2Confirmation.ts     // 确认卡片实体
│   └── L3Transfer.ts         // 转人工实体
├── service/
│   └── CollaborationFunnel.ts // 三级分流引擎
└── event/
    └── FunnelEvent.ts         // 事件定义
```

## 验收标准

AC-02-01 到 AC-02-06（M2 模块定义），加上评审修复的新增：

| # | AC | 验证方式 | 检查点 |
|:--|:---|:---------|:-------|
| 1 | L1 直接应答 | AI-VERIFY | 置信度 ≥ 80% → 直接返回，不请求确认 |
| 2 | L2 确认卡片 | AI-VERIFY | 置信度 50-79% → 生成带 requestId 的确认卡片 |
| 3 | L2 超时升级 | AI-VERIFY | 120s 无响应 → 升级 L3 并附上下文摘要 |
| 4 | L3 转人工 | AI-VERIFY | 资金/安全/合规 → 生成脱敏摘要 → 转人工 |
| 5 | 重复确认去重 | AI-VERIFY | 同 requestId 重复确认 → 返回已处理结果 |
| 6 | WAITING_FOR_CONFIRM 并发消息 | AI-VERIFY | 新消息追加为上下文，不退出状态 |
| 7 | L3 最小化传递 | HUMAN-VERIFY | 转人工只传递摘要，全量需额外鉴权 |
| 8 | L3 数据脱敏 | AI-VERIFY | 转交摘要中邮箱→[EMAIL]，地址→[ADDRESS] |

## Mock 清单

- `MockConfirmationHandler`：模拟用户确认/取消操作
- `MockTransferWebhook`：模拟 L3 转人工的目标接口

## 不可做

- 不包含置信度计算（由 M3 处理）
- 不包含确认卡片的 UI 渲染（前端嵌件处理）
- 不包含实际的人工客服队列管理（商户自有）
