# Chainup / StaffOnews — 需求交付仓库（模板）

**完整交付物** = **`docs/<REQ-ID>/`**（Markdown，AI Coding / Cursor 友好）+ **`apps/prototype/`**（可交互前端）。

交给开发：**本仓库 GitHub URL**；可选另附：**预览环境 URL**（见下文表格）。

**本仓库（生产）**：[`https://github.com/JessonChainup/Agent`](https://github.com/JessonChainup/Agent)

## 开发接手（最短路径）

```bash
git clone https://github.com/JessonChainup/Agent.git
cd Agent
cd apps/prototype && npm install && npm run dev
```

### 文档阅读顺序（推荐）

1. 根 **`README.md`**（本文件）— REQ 索引、预览链接  
2. **`docs/<REQ-ID>/20-spec/spec.md`**  
3. **`docs/<REQ-ID>/40-handoff/`**  
4. **`docs/<REQ-ID>/50-qa/ac.md`**  

编排与 Gate：`references/product-delivery/ORCHESTRATION.md`（Hermes MCP **`chainup-fs`** → `references/product-delivery/`）。

**首次创建远端仓库并推送**：在上级目录打开 **`product-delivery/FIRST-PUSH-GITHUB.zh.md`**（复制本文件夹为新仓库根 → `git init` → `gh repo create` / `push`）。

## 目录结构

| 路径 | 说明 |
|------|------|
| `docs/<REQ-ID>/00-intake … 50-qa` | 阶段化 Markdown，与 Gate 对齐 |
| `apps/prototype/` | **可交互原型**（Vite + React + TypeScript）；合并产品线后可迁入 `apps/web` |
| `.github/workflows/` | **`build-prototype.yml`**（artifact / PR）；**`deploy-prototype-pages.yml`**（可选 GitHub Pages，见 workflows 目录内 README） |

## 新建一条需求

```bash
cp -R docs/REQ-TEMPLATE docs/<REQ-ID>
# 编辑 docs/<REQ-ID>/20-spec/spec.md（从 references/product-delivery/requirements-templates/ 拷贝模版正文）
```

并在下方 **REQ 索引表** 追加一行。

## 预览部署 URL（填写）

启用 **GitHub Pages（Actions）** 后，默认项目站为（部署成功后再核对）：

| 环境 | URL |
|------|-----|
| 原型预览 | [`https://jessonchainup.github.io/Agent/`](https://jessonchainup.github.io/Agent/) |

## REQ 索引

| REQ-ID | 标题 | spec_type | 分支 / PR |
|--------|------|-----------|-----------|
| REQ-TEMPLATE | （示例）复制目录改名 | feature-standard | — |
|| **REQ-STAFFONEWS-KICKOFF** | GitHub+MCP 双轨交付试点 | **feature-standard** | `main` |
|| **REQ-CS-AGENT** | 客服 Agent（AI 问答 + 三级漏斗 + 灰度监控） | **api-backend** | `main` |
