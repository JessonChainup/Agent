# memory-store — 外部持久化记忆层

## 为什么做

Hermes 内置 memory 只有 8,000 字符，且不可回溯、不可按项目隔离。本方案用文件系统 + Git 版本化替代内存存储。

## 存储架构

```
delivery-repo-template/
├── memory-store.json      ← 跨项目记忆（行为修正、会话规则、活跃项目指针）
└── docs/<REQ-ID>/
    └── .memory-store.json ← 项目级记忆（该项目的上下文、决策记录、关键断点）
```

## memory-store.json 结构

```json
{
  "version": 1,
  "lastUpdated": "2026-05-30T10:00:00Z",
  "entries": [
    {
      "id": "uuid",
      "type": "correction|rule|pointer|fact",
      "scope": "global|project:<REQ-ID>",
      "key": "短标识（用于去重更新）",
      "value": "内容",
      "createdAt": "2026-05-30T09:00:00Z",
      "expiresAt": "2026-06-30T09:00:00Z"
    }
  ]
}
```

### entry type 含义

| type | 说明 | 保留策略 |
|:-----|:-----|:---------|
| correction | 你纠正过我的行为/偏好 | 永久保留 |
| rule | 会话启动规则、流程协议 | 永久保留 |
| pointer | 活跃项目指针、当前阶段 | 项目结束后可清除 |
| fact | 产品知识、环境事实 | 30 天自动过期 |

## 读写规则

### 读取（每次响应前）
1. 读取 `memory-store.json` 全部 entries
2. 按 `scope` 过滤：global + 当前活跃项目的 project 条目
3. 过滤已过期条目（`expiresAt < now`）
4. 注入到会话上下文

### 写入（每次写入/修正后）
1. 新增 entry：生成 UUID + 设置 `createdAt`
2. 更新 entry：按 `key` 匹配替换内容，更新 `lastUpdated`
3. 删除 entry：按 `id` 或 `key` 标记过期
4. 写入文件，保持 JSON 格式

### 同步
- cron 每日 03:00：commit + push 到 GitHub（与项目文件一起版本化）
- 每次会话启动时要么读本地文件（若最新），要么拉取 GitHub 最新版本

## 迁移计划

1. 创建 memory-store.json + Python 读写脚本
2. 将当前 memory 中所有条目迁移到文件
3. 创建 cron 每日同步
4. 新会话切换为从文件读取
