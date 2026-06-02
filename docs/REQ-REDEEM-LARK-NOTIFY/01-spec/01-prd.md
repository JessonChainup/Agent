# PRD：理财产品赎回 Lark 通报

> REQ-ID：REQ-REDEEM-LARK-NOTIFY
> 版本：v1.0
> 作者：StaffOnewsbot
> 编写日期：2026-06-01
> 状态：DEFINING

---

## 1. 背景与目标

### 1.1 问题陈述

Chainup SaaS 理财平台支持多种理财产品（定期/活期/封闭锁仓/封闭定期），由多个上游供应商提供底层资产。当前赎回流程中：

- 用户手动赎回或产品到期自动赎回后，上游供应商**无法及时知晓**需回款的金额和明细
- 运营需要**手动汇总**每日各供应商的应打款金额，效率低且易出错
- 供应商回款后，**缺乏标准的确认链路**，运营需人工追踪到账情况

### 1.2 目标

建立一套基于 Lark 的自动化赎回通报体系，覆盖：

1. **事件型通知**：每笔赎回发生时即时通知对应供应商
2. **日报汇总**：每日按供应商分组汇总应打款金额，推送对应供应商进行回款
3. **回款确认**：运营在 Lark 上确认供应商回款到账情况
4. **超时预警**：供应商超时未回款时提醒运营跟进

### 1.3 成功指标

| 指标 | 目标值 | 说明 |
|:----|:-----|:-----|
| 通知覆盖率 | 100% | 每笔赎回都触发通知 |
| 日报推送准时率 | 100% | 每日按约定时间推送 |
| 供应商回款确认时效 | < 24h | 从日报推送到运营确认 |
| 运营操作效率提升 | 减少 80% 手工汇总 | 以前人工汇总，现在系统自动出 |

---

## 2. 范围

### 2.1 本期做（P0）

| 编号 | 功能点 | 优先级 |
|:----|:-------|:------:|
| F1 | 事件型通知：单笔赎回时即时推送 Lark 卡片 | P0 |
| F2 | 日报汇总：每日按供应商+币种汇总应打款金额，推送到 Lark | P0 |
| F3 | 运营确认回款：Lark 卡片按钮确认供应商已打款 | P0 |
| F4 | 供应商超时预警：超过打款截止时间未确认，推送黄色预警 | P0 |

### 2.2 本期不做（P2 及以上）

| 功能点 | 原因 |
|:-------|:-----|
| 自动对账（系统自动比对链上到账） | 需要对接供应商链上地址，二期再做 |
| 财务报表导出 | 与已有的财务系统职责重叠 |
| 供应商自助查询历史赎回记录 | 一期先做推送到账确认，后续扩展 |

---

## 3. 用户与场景

### 3.1 用户画像

| 角色 | 说明 | 使用场景 |
|:----|:-----|:---------|
| 上游供应商 | 提供底层理财资产的机构 | 接收赎回通知、查看日报应打款、点击确认打款 |
| 运营人员 | 平台内部运营 | 确认供应商回款到账、跟进超时未打款供应商 |
| 平台用户 | 购买理财产品的终端用户 | 赎回后等待资金到账（不直接看到 Lark 卡片） |

### 3.2 核心场景

**场景 1：用户手动赎回**
> 用户在理财产品详情页点击「赎回」，系统处理成功后，即时推送 Lark 通知给对应供应商和运营群。

**场景 2：产品到期自动赎回**
> 理财产品到期日，系统自动处理赎回并发放本息，即时推送 Lark 通知。

**场景 3：每日回款汇总**
> 每日 10:00 系统自动按供应商分组汇总前一日所有赎回，推送给各供应商和运营群。

**场景 4：供应商回款确认**
> 供应商收到日报后，点击「✅ 已打款」按钮确认，运营核实到账后确认。

**场景 5：供应商超时未打款**
> 供应商超过打款截止时间（24h）未确认回款，自动推送黄色预警给运营群。

---

## 4. 业务逻辑与字段定义

### 4.1 事件型通知（单笔赎回）

| 字段 | 类型 | 示例值 | 校验规则 | 说明 |
|:----|:----|:-------|:---------|:-----|
| `time` | datetime | `2026-06-01 02:00` | 必填 | 记录生成时间 |
| `product_type` | string | `定期理财` | 枚举值 | 产品类型：定期理财/活期理财/封闭锁仓理财/封闭定期理财 |
| `supplier_name` | string | `ABC Finance` | 必填 | 供应商名称 |
| `supplier_address` | string | `TXYZ...abc` | 必填 | 供应商地址（打款目标地址） |
| `merchant_uid` | string | `M10086` | 必填 | 商户 UID |
| `user_uid` | string | `UID-888888` | 必填 | 用户 UID |
| `currency` | string | `USDT` | 必填 | 币种 |
| `product_duration` | string | `30天` | 可选 | 项目周期 |
| `annual_yield` | string | `5.2%` | 可选 | 年化收益率 |
| `principal_amount` | string | `4.05` | 必填，数值>0 | 赎回本金 |
| `interest_amount` | string | `0.05` | 必填 | 赎回利息 |
| `redemption_time` | date | `2026-06-01` | 必填 | 赎回日期 |
| `redemption_period` | string | `14天` | 可选 | 赎回期天数 |
| `redemption_arrival_time` | date | `2026-06-15` | 必填 | 应赎回到账时间 |
| `apply_time` | datetime | `2026-06-01 10:30:00` | 必填 | 申请时间 |
| `upstream_notify_status` | string | `已通知` | 枚举值 | 通知上游状态：已通知/待通知/通知失败 |

### 4.2 日报汇总（按供应商+币种分组）

| 字段 | 类型 | 示例值 | 校验规则 | 说明 |
|:----|:----|:-------|:---------|:-----|
| `supplier_name` | string | `001` | 必填 | 供应商 |
| `currency` | string | `USDT` | 必填 | 币种 |
| `stat_start_date` | date | `2026-05-31` | 必填 | 统计起始日 |
| `stat_end_date` | date | `2026-06-01` | 必填 | 统计截止日 |
| `total_principal` | string | `500.00` | 必填 | 该供应商+该币种赎回本金合计 |
| `total_interest` | string | `0.50` | 必填 | 该供应商+该币种赎回利息合计 |
| `settle_address` | string | `TXYZ...abc` | 必填 | 供应商打款地址 |
| `settle_deadline` | datetime | `2026-06-02 18:00` | 必填 | 打款截止 |
| `confirm_status` | string | `pending` | 枚举值 | 确认状态：pending / confirmed / discrepancy |

> **每条日报记录 = 一个供应商 + 一个币种**。多币种时每个币种独立一条记录，分别推送。无总笔数字段。

---

## 5. 交互与流程

### 5.1 核心流程

```
用户发起赎回（手动赎回/到期自动赎回）
    ↓
系统处理赎回 → 计算本金 + 利息
    ↓
┌─ 步骤1：事件型通知（即时） ──────────────┐
│ Lark 卡片推送到对应供应商群 + 运营群      │
│ 告知：谁赎回了什么、多少钱、几时到账      │
└─────────────────────────────────────────┘
    ↓
┌─ 步骤2：日报汇总（每日 10:00） ──────────┐
│ 按 supplier → currency 分组汇总          │
│ 每供应商一张卡片推送到对应供应商群        │
│ 卡片含「已打款」「金额有差异」「尚未处理」按钮  │
└─────────────────────────────────────────┘
    ↓
┌─ 步骤3：运营确认 ──────────────────────┐
│ 供应商点击「已打款」                     │
│ 运营核实到账 → 点击确认                  │
│ 状态变更为 confirmed                     │
└─────────────────────────────────────────┘
    ↓
┌─ 步骤4（可选）：超时预警 ───────────────┐
│ 超过 deadline 未确认 → 黄色预警推送运营群  │
└─────────────────────────────────────────┘
```

### 5.2 交互四态

**事件型通知卡片：**

| 状态 | 显示内容 |
|:----|:---------|
| 正常态 | 完整字段，通知上游状态：已通知 |
| 通知失败态 | 红色提示「通知失败，请手动处理」+ 显示失败原因 |
| 待通知态 | 灰度显示「处理中...」 |
| 空态 | 不适用（事件触发才有卡片） |

**日报卡片：**

| 状态 | 显示内容 |
|:----|:---------|
| 待确认态 | 运营确认状态：⏳ 待确认，三个按钮均可用 |
| 已确认态 | 运营确认状态：✅ 已确认（已打款金额），按钮置灰 |
| 差异态 | 运营确认状态：⚠️ 有差异，显示差异金额 |
| 超时态 | 黄色 header，显示「已超时 X 小时」 |

---

## 6. 卡片模板

### 6.1 事件型通知卡片

```json
{
  "config": {
    "update_multi": true,
    "wide_screen_mode": true
  },
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "🔵 赎回通知 — 需回款"
    },
    "template": "blue"
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "**时间：** {time}\n**产品类型：** {product_type}\n**供应商：** {supplier_name}\n**供应商地址：** `{supplier_address}`"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**商户 UID：** {merchant_uid}\n**用户 UID：** {user_uid}\n**币种：** {currency}\n**项目周期：** {product_duration}\n**年化收益率：** {annual_yield}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**本金：** {principal_amount} {currency}\n**利息：** {interest_amount} {currency}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**赎回时间：** {redemption_time}\n**赎回期：** {redemption_period}\n**应赎回到账时间：** **{redemption_arrival_time}**\n**申请时间：** {apply_time}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**通知上游状态：** {upstream_notify_status}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "note",
      "elements": [
        {
          "tag": "plain_text",
          "content": "⏱ {timestamp} · 自动推送"
        }
      ]
    }
  ]
}
```

### 6.2 日报汇总卡片（每供应商+币种一条记录推送一张卡片）

```json
{
  "config": {
    "update_multi": true,
    "wide_screen_mode": true
  },
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "📋 赎回日报 — {stat_start_date} ~ {stat_end_date}"
    },
    "template": "green"
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "**供应商：** {supplier_name}\n**币种：** {currency}\n**打款地址：** `{settle_address}`\n**打款截止：** {settle_deadline}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**赎回本金：** **{total_principal} {currency}**\n**赎回利息：** {total_interest} {currency}"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**统计时间：** {stat_start_date} — {stat_end_date}\n**回款确认状态：** {confirm_status_label}"
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "✅ 已打款"
          },
          "type": "primary",
          "value": {
            "action": "supplier_made_payment",
            "supplier_name": "{supplier_name}",
            "currency": "{currency}",
            "stat_end_date": "{stat_end_date}",
            "amount": "{total_principal}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "⏳ 尚未处理"
          },
          "type": "default",
          "value": {
            "action": "supplier_not_processed",
            "supplier_name": "{supplier_name}",
            "currency": "{currency}",
            "stat_end_date": "{stat_end_date}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "⚠️ 金额有差异"
          },
          "type": "default",
          "value": {
            "action": "supplier_discrepancy",
            "supplier_name": "{supplier_name}",
            "currency": "{currency}",
            "stat_end_date": "{stat_end_date}"
          }
        }
      ]
    },
    {
      "tag": "hr"
    },
    {
      "tag": "note",
      "elements": [
        {
          "tag": "plain_text",
          "content": "⏱ {timestamp} · 自动推送"
        }
      ]
    }
  ]
}
```

> **单条日报记录 = 一个供应商 + 一个币种**。如供应商 001 有 USDT 和 ETH 两个币种需打款，则推送两张独立卡片。每张卡片展示该币种的本金和利息合计。

### 6.3 超时预警卡片

```json
{
  "config": {
    "update_multi": true,
    "wide_screen_mode": true
  },
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "🟡 供应商回款超时预警"
    },
    "template": "orange"
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "**供应商：** {supplier_name}（{supplier_id}）\n**币种：** {currency}\n**应打款：** {upstream_payable} {currency}\n**截止时间：** {settle_deadline}\n**已超时：** {overdue_hours} 小时"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**影响：** 影响 {merchant_count} 个商户、{user_count} 个用户的赎回资金到账"
    },
    {
      "tag": "hr"
    },
    {
      "tag": "markdown",
      "content": "**建议操作：** 联系供应商催促回款，或确认是否有异常需要升级处理"
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "✅ 已跟进，供应商已在处理"
          },
          "type": "primary",
          "value": {
            "action": "followed_up_supplier",
            "supplier_id": "{supplier_id}",
            "currency": "{currency}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "🔴 需要升级处理"
          },
          "type": "default",
          "value": {
            "action": "escalate_supplier_delay",
            "supplier_id": "{supplier_id}",
            "currency": "{currency}"
          }
        }
      ]
    },
    {
      "tag": "hr"
    },
    {
      "tag": "note",
      "elements": [
        {
          "tag": "plain_text",
          "content": "⏱ {timestamp} · 自动提醒"
        }
      ]
    }
  ]
}
```

---

## 7. 推送规则与消息接收方

| 卡片类型 | 推送给谁 | 推送时机 | 推送条件 |
|:--------|:---------|:---------|:---------|
| 事件型通知 | **对应供应商群** + **运营总群** | 每笔赎回完成后即时 | status=settled |
| 日报汇总 | **各供应商专属群**（每供应商一张独立卡片） | 每日 10:00 | 有当日赎回记录 |
| 超时预警 | **运营总群** | 超过打款截止后 | confirm_status=pending 且超过 deadline |

### KV 配置

| 配置键 | 默认值 | 取值范围 | 说明 |
|:------|:------|:---------|:-----|
| `redeem.daily_report.time` | `10:00` | HH:MM | 日报推送时间 |
| `redeem.settle_deadline_hours` | `24` | 1-72 | 供应商应在几小时内打款 |
| `redeem.overdue_reminder_interval` | `6` | 1-24 | 超时后每隔几小时提醒一次 |
| `redeem.notify_retry_count` | `3` | 1-5 | 通知失败后重试次数 |
| `redeem.notify_retry_interval` | `60` | 秒 | 重试间隔 |

---

## 8. 数据聚合逻辑

```
原始数据（赎回事件流）
    ↓
每笔赎回记录包含：{merchant_uid, user_uid, currency, product_type,
                    supplier_name, principal_amount, interest_amount, ...}
    ↓
（事件型）→ 即时推送单笔通知
    ↓
（日报，每日 10:00）
    ↓ 按 supplier_name + currency 分组（每组合一条记录）
    ↓ 无总笔数统计
    ↓
输出：每组合一张独立卡片
  ├ 供应商 + 币种
  ├ 赎回本金合计
  └ 赎回利息合计
```

### 理财类型字段生效规则

| 字段 | 定期理财 | 活期理财 | 封闭锁仓理财 | 封闭定期理财 |
|:----|:--------:|:--------:|:------------:|:------------:|
| 募集期开关 | ✅ 总后台配置 | ❌ | ❌ | ❌ |
| 募集开始/结束时间 | 开关开启时显示 | ❌ | ✅ 原有 | ✅ 原有 |
| 赎回期开关 | ✅ 总后台配置 | ❌ | ✅ 总后台配置 | ✅ 总后台配置 |
| 赎回期天数 | 开关开启时输入 | ❌ | 开关开启时输入 | 开关开启时输入 |
| 赎回到账时间 | 计息结束+赎回期 | 即时 | 计息结束+赎回期 | 计息结束+赎回期 |

---

## 9. 验收标准

### AC-RDM-01：用户手动赎回触发通知
- **Given** 用户发起一笔手动赎回，系统处理成功
- **When** 赎回状态变为 settled
- **Then** 系统即时推送事件型 Lark 卡片到对应供应商群
- **And** 卡片字段包含 product_type / supplier_name / redemption_amount 等全部必填字段

### AC-RDM-02（异常）：赎回失败不触发通知
- **Given** 用户发起赎回但系统处理失败
- **When** 赎回状态变为 failed
- **Then** 系统不推送事件型通知

### AC-RDM-03：日报准时推送
- **Given** 当日某供应商+某币种有赎回记录
- **When** 到达每日 10:00
- **Then** 系统按 supplier_name + currency 组合推送日报卡片
- **And** 每组合一张独立卡片，卡片展示该组合的赎回本金和利息合计

### AC-RDM-04：多币种多卡片
- **Given** 供应商 001 当日有 USDT 和 ETH 两种币种的赎回记录
- **When** 到达每日 10:00
- **Then** 系统推送两张独立卡片（001+USDT / 001+ETH）
- **And** 每张卡片独立展示对应币种的本金和利息

### AC-RDM-05：供应商确认已打款
- **Given** 供应商收到日报卡片
- **When** 供应商点击「✅ 已打款」按钮
- **Then** 运营群收到确认通知
- **And** 运营核实到账后确认，状态变更为 confirmed

### AC-RDM-06（异常）：供应商金额有差异
- **Given** 供应商点击「⚠️ 金额有差异」按钮
- **When** 运营收到差异通知
- **Then** 状态变更为 discrepancy，运营人工处理

### AC-RDM-07：超时预警
- **Given** 供应商超时 (24h) 未打款
- **When** 超过 settle_deadline
- **Then** 推送黄色预警卡片到运营群
- **And** 每 6 小时重复提醒直至确认

---

## 10. 风控与异常场景

| 场景 | 影响 | 处理逻辑 |
|:----|:----|:---------|
| Lark 推送失败 | 供应商收不到通知 | 重试 3 次，每次间隔 60s，仍失败则标记 notify_status=failed 并告警运营 |
| 供应商打款地址变更 | 资金打错地址 | 供应商地址由总后台维护，修改需审核 |
| 同一供应商同一币种多条日报 | 数据重复 | 日报以 stat_end_date + supplier_name + currency 为唯一键，覆盖写入 |
| 运营误操作确认 | 状态错误 | 已确认状态需二次确认才能撤销 |
| 供应商不点击按钮 | 超时 | 超时后自动推送预警给运营，运营人工跟进 |

---

> 文档结束
