# 推送到 GitHub（JessonChainup/Agent）

本目录应已存在 **首次提交** 与 **`origin` → `https://github.com/JessonChainup/Agent.git`**。

## 若 `git push` 报 403 / Permission denied

通常表示本机保存的 GitHub 账号**不是**对 `JessonChainup/Agent` 有写权限的账号（例如钥匙串里是其他个人号）。

任选其一：

1. **安装并登录 GitHub CLI（推荐）**  
   ```bash
   brew install gh
   gh auth login
   cd "/Users/jesson/Documents/Hermes Agent/product-delivery/delivery-repo-template"
   git push -u origin main
   ```

2. **HTTPS + PAT（JessonChainup 下有 repo 权限的 fine-grained/classic PAT）**  
   先在「钥匙串访问」删掉 `github.com` 的旧口令，或使用一次性远程 URL（**勿**把 PAT 提交进仓库或发到聊天）：  
   ```bash
   cd "/Users/jesson/Documents/Hermes Agent/product-delivery/delivery-repo-template"
   git push -u origin main
   ```

3. **SSH**  
   将 **JessonChainup** 账号下的公钥加到 GitHub 后：  
   ```bash
   cd "/Users/jesson/Documents/Hermes Agent/product-delivery/delivery-repo-template"
   git remote set-url origin git@github.com:JessonChainup/Agent.git
   git push -u origin main
   ```

推送成功后：**Settings → Pages → Source：GitHub Actions**，等待 **`Deploy prototype to GitHub Pages`** 成功后核对预览：**https://jessonchainup.github.io/Agent/**

---

## 从服务器（lumai-163）推送

Hermes 的 **`GITHUB_TOKEN`**（`/root/.hermes/.env`）通常只有 **读/metadata** 权限（例如拉 Skills），**不能用 GitHub API 添加 Deploy Key**，也**不足以 `git push` 写 Contents**。脚本默认 **先试 SSH Deploy Key**，失败后再尝试 **`agent-git.env` 里的 PAT（HTTPS）**。

### A. Deploy Key（推荐，不把 PAT 留在服务器）

1. 在服务器查看公钥（可安全粘贴到 GitHub）：  
   ```bash
   ssh lumai-163 'cat /root/.ssh/gh_agent_deploy_ed25519.pub'
   ```
2. 打开 **[Agent → Settings → Deploy keys](https://github.com/JessonChainup/Agent/settings/keys)** → **Add deploy key**。  
   - **Title**：例如 `lumai-163-deploy`  
   - **Key**：粘贴上一步公钥  
   - **勾选 Allow write access**  
3. 执行推送脚本：  
   ```bash
   ssh lumai-163 '/root/.hermes/bin/push-agent-delivery.sh'
   ```

### B. PAT 兜底（Fine-grained）

仅在无法用 Deploy Key 时使用。**完整 Token** 长度通常 **远大于 21**；若只有占位串会导致 HTTPS 兜底失败。

- Resource owner：**JessonChainup**  
- Repository：**Agent**  
- Permissions：**Contents → Read and write**

写入 **`/root/.hermes/agent-git.env`**（**`chmod 600`**）：

```
AGENT_GIT_TOKEN=github_pat_<完整令牌>
```

然后同样执行 **`/root/.hermes/bin/push-agent-delivery.sh`**（SSH 失败时会自动走 HTTPS）。

推送前可先在本机 **`rsync`** 更新远端 references 模板（见 **`product-delivery/README.md`**）。
