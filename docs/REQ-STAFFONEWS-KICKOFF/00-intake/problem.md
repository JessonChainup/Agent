# 问题陈述（INTAKE）

## 一句话

团队在 **Hermes MCP 草稿目录**与 **GitHub 交付仓库**之间存在「口述需求 / 无序长文」，缺少 **REQ-ID + 阶段 Gate**，研发与分身难以稳定交接 **Markdown 规格 + 可运行的原型占位**。

## 成功标准（草案）

- 至少 **1 条** REQ 在 **`docs/<REQ-ID>/`** 下落盘到 **HANDOFF/QC 可追溯**；
- **`apps/prototype`** 可构建，且在 UI 或 **`30-proto/links.md`** 中可找到 **对本 REQ Spec 的阅读入口**；
- **CI（Build prototype）** 对 **`main`** 保持稳定绿。

## 非问题（暂不解决）

- 主站交易业务全量模块化迁移；本条仅 **交付链路试点**。
