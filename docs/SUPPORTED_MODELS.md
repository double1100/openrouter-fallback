# 支持的免费模型列表

> 这些模型在 OpenRouter 上完全免费使用（无需信用卡）

---

## 📊 默认推荐列表（Top 10）

模型按优先级排序，综合考虑**质量、速度、国内可用性**。

| 排名 | 模型 ID | 上下文 | 特点 | 国内 | 适合场景 |
|------|---------|--------|------|------|----------|
| 1 | `qwen/qwen3.6-plus:free` | 100万 | Qwen最强 | ✅ 快 | 通用问答、长文档 |
| 2 | `nvidia/nemotron-3-super-120b-a12b:free` | 128k | NVIDIA顶级 | ✅ 快 | 高质量推理、分析 |
| 3 | `nvidia/nemotron-3-nano-30b-a3b:free` | 4k | 轻量快速 | ✅ 快 | 简单问答、快速响应 |
| 4 | `stepfun/step-3.5-flash:free` | 32k | 专为对话优化 | ✅ 快 | 友好对话、解释性任务 |
| 5 | `qwen/qwen3-coder:free` | 32k | 编码专用 | ✅ 快 | 写代码、调试 |
| 6 | `nvidia/nemotron-nano-9b-v2:free` | 4k | 极轻量 | ✅ 快 | 简单问答、备胎 |
| 7 | `nvidia/nemotron-nano-12b-v2-vl:free` | 4k | 多模态 | ✅ 快 | 图像+文本（需支持） |
| 8 | `qwen/qwen3-next-80b-a3b-instruct:free` | 32k | Qwen 80B | ✅ 中 | 复杂任务、推理 |
| 9 | `arcee-ai/trinity-mini:free` | 4k | 小巧精致 | ⚠️ 待测 | 备选 |
| 10 | `meta-llama/llama-3.2-3b-instruct:free` | 4k | Meta 轻量 | ✅ 快 | 极简任务、备用 |

---

## 🌍 地区可用性说明

| 地区 | 可用模型 | 备注 |
|------|----------|------|
| **中国大陆** | StepFun, Qwen, NVIDIA | Google/Meta 部分受限 |
| **香港/台湾** | 全部 | 无限制 |
| **海外** | 全部 | 无限制 |

**国内推荐：** 优先使用 StepFun、Qwen、NVIDIA 系模型，速度快且稳定。

---

## 🔄 模型更新周期

- 模型列表由 `skills/freeride/main.py refresh` 更新
- 自动更新频率：每天一次（通过 cron 或 HEARTBEAT）
- 新模型上架后，会在下次刷新时加入推荐列表

---

## 📝 如何查看当前可用模型？

```bash
or-auto --list-models
```

输出示例：
```
✅ 可用免费模型（按优先级）：
1. qwen/qwen3.6-plus:free (100万上下文)
2. nvidia/nemotron-3-super-120b-a12b:free
...
```

---

## ⚙️ 自定义模型列表

如果你有偏好，可以创建 `~/.openrouter_fallback_config.json`：

```json
{
  "models": [
    {"id": "stepfun/step-3.5-flash:free", "priority": 1, "max_tokens": 4096},
    {"id": "qwen/qwen3.6-plus:free", "priority": 2}
  ]
}
```

优先级数字越小越靠前。

---

## 🆓 什么是"免费模型"？

- **免费** = 不需要付费订阅也能用
- **有限额** = 每分钟/小时有请求次数限制（如 20 次/分钟）
- **自动降级** = 当某个模型达到限额，自动换下一个
- **永不付费** = 自由使用，不扣费（但需注意，OpenRouter 可能随时调整政策）

---

## 🎯 模型选择建议

| 需求 | 推荐模型 |
|------|----------|
| 最长对话、处理大文档 | `qwen/qwen3.6-plus:free` |
| 最可靠、质量最高 | `nvidia/nemotron-3-super-120b-a12b:free` |
| 最快响应 | `nvidia/nemotron-3-nano-30b-a3b:free` |
| 写代码 | `qwen/qwen3-coder:free` |
| 友好对话、解释概念 | `stepfun/step-3.5-flash:free` |
| 备用（其他都挂了） | `meta-llama/llama-3.2-3b-instruct:free` |

---

**提示：** 模型列表会变，运行 `or-auto --list-models` 查看最新推荐。
