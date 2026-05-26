# L1 模块边界：07—错误处理与审计追溯

## 模块职责

定义 Agent 运行中的错误分类、降级策略、审计日志存储、以及数据反馈闭环。

## 错误分类

| 级别 | 示例 | 策略 |
|:-----|:-----|:------|
| L1 输入 | 为空/非法字符/超长 | 忽略或截断，不转 L3 |
| L2 执行 | API 超时/知识库查询失败 | 重试 1 次或直接降级 |
| L3 关键 | 资金操作异常/KYC 错误 | 不重试，转人工 + 即时通知 |
| L4 灾难 | 误执行资金操作/数据泄露 | 立即锁定商户 + 通知风控 |

## 审计日志

每次会话处理记录包含 8 字段：event_id, timestamp, merchant_id, session_id, user_input（已脱敏）, classification, confidence, funnel_level, action_taken, api_calls, error_level, error_detail, user_satisfied。

- 保留 180 天（KYC 相关 30 天）
- 不可篡改（仅追加）
- 多租户隔离
- 脱敏规则：地址→[REDACTED]，邮箱→[REDACTED]，电话→[REDACTED]

## 数据反馈闭环

每日扫描失败案例 → 四类自动归因（知识库未覆盖/置信度误判/输入理解错误/API 错误/系统错误）→ 写入"候补列表"→ 人工复核后触发改进。

## 依赖

- M1-M4（数据来源）
