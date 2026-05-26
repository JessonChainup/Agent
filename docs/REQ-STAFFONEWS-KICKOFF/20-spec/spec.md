---
spec_type: feature-standard
title: StaffOnews 产品线：GitHub+MCP 双轨交付试点
req_id: REQ-STAFFONEWS-KICKOFF
status: draft
owner_pm: Jesson / StaffOnewsbot
risk_level: low
channels:
  - web-app
  - internal-docs
---

<!-- 本条为「方法论落地」试点；业务功能 REQ 可复制本目录结构与 Gate 节奏新开 REQ-ID -->

# 1. 一句话与成功指标

- **电梯稿**：用 **REQ-STAFFONEWS-KICKOFF** 打通 **`docs/` 阶段文档 + CI 原型**，让研发与分身按同一套 Gate 交出可验收的包，而不是聊天长文。
- **成功指标（可度量）**：
  - `main`：**Build prototype** workflow **成功率 100%**（修复性提交除外）。
  - 本 REQ 下 **必选文件齐备**（见各阶段 README / ORCHESTRATION）。
  - **`50-qa/ac.md`** 中 AC 可被 **QA/PM** 人工逐条勾选通过。
- **护栏指标**：**不引入**仓库密钥明文；不写死未 **CONFIRMED** 的内部域名；不代替合规结论。

# 2. 用户与场景

| Persona | 场景 | 当前痛点 |
|---------|------|----------|
| PM（你） | 同时用 Hermes 分身与 Cursor 演进需求 | 状态散落聊天，难追溯 Gate |
| 研发 | Clone 交付仓接手 | PRD 散、原型与 SPEC 割裂 |
| 分身（Hermes） | MCP 写入 `drafts/<REQ-ID>/` | 缺 REQ-ID / 跳阶段 |

# 3. 当前行为 vs 期望行为

| Step | Current | Desired |
|------|---------|---------|
| 1 | 口述需求后直接要「整 PRD」 | 先声明 **REQ-ID + 当前阶段**，再补缺的 md |
| 2 | Markdown 仅在 MCP，无 GH | Gate 后对齐 **`docs/<REQ-ID>/`** 并 **`git push`** |
| 3 | 原型只口头描述 | **`apps/prototype`** 可构建；链接回 **Spec** |

# 4. 范围 / 非目标

- **In scope**：
  - 本 REQ 目录结构与 **`feature-standard`**；
  - 原型占位页 **显性链接**指向本 REQ **Spec URL**；
  - **AC / test-plan / rollout** 最小可用。
- **Out of scope**：
  - 主站交易系统核心交易路径改造；
  - 多端 Design System / 品牌化大改版。

# 5. 方案概述

- **MVP 轮廓**：以 **[Agent](https://github.com/JessonChainup/Agent)** 为真相源，`docs/` 走阶段，`apps/prototype` 走 Vite/React。
- **关键交互**：原型首页展示 **REQ 导航**；`30-proto/links.md` 提供 **GitHub 直链**。
- **依赖团队**：N/A（纯试点）；后续业务 REQ 填真实 **Lead/设计/法务**。

# 6. Web3 / 资金 / 合规（交易线必填；无则显式写 N/A）

| 条目 | 说明 |
|------|------|
| 资金路径 | N/A（本 REQ 不涉及入金/划转/提现） |
| 风控触点 | N/A |
| 对外口径 | 对外说明仍须走既有 Brand/合规审稿流程（本 Req 不产生新对外承诺） |

# 7. 埋点与实验（可选）

- N/A。

# 8. Rollout / 灰度（可选）

- **`main`** 持续集成；若要灰度只对 **预览环境**切片，单列未来 REQ。

---

## 附录 A：AI Coding Handoff（与实现同步更新）

（摘自 `references/product-delivery/requirements-templates/_shared-ai-coding-appendix.md`，随实现更新。）

### H. AI Coding / 研发 Handoff 块（必须随 spec 一起成长）

#### H1. 仓库与运行假设（不确定就写 TODO）

| 字段                  | 内容                                        |
| ------------------- | ----------------------------------------- |
| 主仓库 / Monorepo 路径占位 | 交付原型：`apps/prototype`；主站路径 **TODO CONFIRMED** |
| 受影响环境               | dev / staging / prod（与本试点：CI=GitHub-hosted）                      |
| Feature flag        | N/A                                                 |

#### H2. 拟修改文件清单（猜测允许，但必须标 `CONFIRMED`/`GUESS`）

| Path | `CONFIRMED`/`GUESS` | 改动类型（api/ui/db/config） |
| ---- | ------------------- | ---------------------- |
| `apps/prototype/src/App.tsx` | GUESS | ui |
| `docs/REQ-STAFFONEWS-KICKOFF/**` | CONFIRMED | docs |

#### H3. 数据与契约

- 无对外 REST/事件契约；占位见 **`40-handoff/contracts/README.md`**。

#### H4. 验收标准（写成可脚本/可人工逐条勾选）

详见同级 **`../50-qa/ac.md`**。

#### H5. 非目标与非功能

| NFR | 指标           |
| --- | ------------ |
| 性能  | 静态原型首屏无明显卡顿（手工） |
| 安全  | 无密钥进仓；Deploy Key/PAT **仅存服务器本机 chmod 文件** |
| 兼容  | 现代 Chromium / Safari 最近两个大版本 |

#### H6. 回滚与灰度

- `git revert` 上一合并提交；Pages 追随 **main** HEAD。
