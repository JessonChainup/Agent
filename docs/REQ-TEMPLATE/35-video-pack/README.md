# 35-video-pack（可选）— 短视频云端 API 成片包

> 当本条 REQ 需要 **可渲染的短视频规格 + 合规记录** 时使用。  
> **完整流程**：见交付方法论仓库 **`references/product-delivery/VIDEO-CLOUD-PIPELINE.zh.md`**（或本 monorepo 的 **`product-delivery/VIDEO-CLOUD-PIPELINE.zh.md`**）。

## 与阶段门的关系

- 建议在 **`20-spec/spec.md` 评审通过** 后填充本目录。  
- **进入 Worker / 火山方舟前**：本目录内 **`compliance-check.md`** 与 **`render-spec.json` 内 `compliance_pass`** 须与 PM Gate 一致。

## 推荐文件清单

| 文件 | 说明 |
|------|------|
| `brief.md` | 目标、受众、渠道、时长与画幅、预算与 deadline |
| `script.md` | 口播/字幕正文；与 RevMate **`short-video-hospitality-commercial`** 输出对齐 |
| `storyboard.md` | 分镜表：镜号、画面描述、时长、素材来源（自建/图库/生成） |
| `compliance-check.md` | 对照清单结论：附录 C 要点 + `COMPLIANCE-ADS-CHECKLIST.zh.md` 勾选记录 |
| **`render-spec.json`** | **Worker 唯一机器入口**；字段约定见 **VIDEO-CLOUD-PIPELINE.zh.md §五** |
| `subtitles.srt`（可选） | 若 `render-spec.post.burn_subtitles` 为 true |

## `render-spec.json` 骨架

复制后替换 `req_id`、完善 `scenes`；**不得**在文件内粘贴云 API 密钥。

```json
{
  "spec_version": "1.0",
  "req_id": "REQ-REPLACE-ME",
  "compliance_pass": false,
  "compliance_notes": "",
  "output": {
    "aspect_ratio": "9:16",
    "target_duration_sec": 45,
    "fps": 25
  },
  "provider": {
    "video_generation": "volcengine-ark",
    "model_or_endpoint_id": "",
    "poll_interval_sec": 10,
    "max_poll_minutes": 30
  },
  "scenes": [],
  "voice": {
    "type": "none",
    "provider": "",
    "voice_id": ""
  },
  "post": {
    "burn_subtitles": true,
    "subtitle_file_ref": "35-video-pack/subtitles.srt"
  },
  "artifacts": {
    "upload_bucket": ""
  }
}
```

## 输出回写

成片完成后，在 **`50-qa/`** 或本目录新增 **`outputs.md`**：存储 URI、`task_id`、生成时间、模型版本（便于审计）。
