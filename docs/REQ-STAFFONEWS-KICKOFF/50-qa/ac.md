# 验收标准（AC）

每条 **给定 / 当 / 则**（或 **步骤 → 期望**）。

- **AC-01**：克隆 **[Agent](https://github.com/JessonChainup/Agent)** 后，`npm install && npm run build` 于 **`apps/prototype`** **成功**（与 CI 一致）。
- **AC-02**：`docs/REQ-STAFFONEWS-KICKOFF/` 下 **阶段目录齐备**，**`20-spec/spec.md`** 含 **`spec_type: feature-standard`** 与 **附录 Handoff**。
- **AC-03**：原型或 **`30-proto/links.md`** 中至少一种 **可读入口**指向本 REQ **Spec**（人工可点开核对）。
- **AC-04**：根 **`README.md`** **REQ 索引表**包含本 REQ 一行。
- **AC-05**：（若启用 Pages）预览 URL **可打开**，静态资源前缀 **无 404**（`/Agent/` base 兼容）。
