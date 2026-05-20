# GitHub Actions — 原型构建 / 部署

## `build-prototype.yml`

在 **`push`** / **`pull_request`**（针对 `main`、`master`）及 **`workflow_dispatch`** 时：

- 在 `apps/prototype` 执行 **`npm ci`** + **`npm run build`**  
- 上传 artifact **`prototype-dist`**（内含 `dist/`）

用途：**PR 门禁**（确认能构建）、本地下载 artifact 再上传到自建静态服务器。

## `deploy-prototype-pages.yml`

仅在 **`push`** 到 **`main` / `master`**（或手动 **`workflow_dispatch`**）时运行：

- 使用 **`VITE_PAGES_BASE`** 按仓库名生成正确的资源前缀（适配 `https://<owner>.github.io/<repo>/`；若为 **`/<owner>.github.io`** 用户站点仓库则用 **`/`**）  
- 通过 **`upload-pages-artifact`** + **`deploy-pages`** 发布到 **GitHub Pages**

### 启用 Pages（一次性）

1. 仓库 **Settings → Pages → Build and deployment**  
2. **Source** 选 **GitHub Actions**（不要用 Branch/deploy from branch，与本 workflow 冲突）  
3. 推送默认分支后，在 **Actions** 打开 **`Deploy prototype to GitHub Pages`**，成功后 **Settings → Pages** 顶部可见站点 URL  

### 限制说明

- **私有仓库**：是否在免费套餐下可使用 Pages，取决于 GitHub 当前策略；若不可用，保留 **`build-prototype.yml`** artifact + 自建 OSS/nginx 即可。  
- **不要在仓库提交任何密钥**；本模板 Pages 流程依赖 Actions 自带的 **`GITHUB_TOKEN`**，无需额外 PAT。
