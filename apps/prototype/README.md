# 可交互原型（Vite + React + TS）

本地运行：

```bash
npm install
npm run dev
```

构建静态资源（便于 nginx / Pages 部署）：

```bash
npm run build
# 产出 dist/
```

## 约束（交付开发 / AI Coding）

- **不接生产 API**：使用 mock / `.env.example` 中的占位变量。  
- 关键交互路径须与 **`docs/<REQ-ID>/20-spec/spec.md`**、**`30-proto`** 描述一致。  
