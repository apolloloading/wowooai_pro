# 05 — LLM 模型供应商（Providers）

> 版本：0.0.1
> 对应代码：[src/wowooai/providers/](../../src/wowooai/providers/) · `providers.json`

## 1. 内置 Provider 类型

| Provider | 类型 | 说明 |
|---|---|---|
| `anthropic` | 云端 | Claude 系列（Opus / Sonnet / Haiku） |
| `openai` | 云端 | GPT 系列 |
| `gemini` | 云端 | Google Gemini |
| `openrouter` | 云端聚合 | 通过 OpenRouter 访问多家模型 |
| `dashscope` | 云端 | 阿里通义千问 / Qwen 系列 |
| `deepseek` | 云端 | DeepSeek API |
| `siliconflow` | 云端 | 硅基流动 |
| `moonshot` | 云端 | Kimi |
| `zhipu` | 云端 | 智谱 GLM |
| `ollama` | 本地 | 本地 Ollama 后端 |
| `lmstudio` | 本地 | 本地 LMStudio 后端 |
| `openai_compat` | 自定义 | 任意 OpenAI-compatible 端点 |

总计 ≥ 12 种 provider type（精确清单以代码 [provider_manager.py](../../src/wowooai/providers/provider_manager.py) 为准）。

## 2. Provider 配置存储

- 文件：`~/.wowooai/providers.json`
- 结构：`{ active_llm: ModelSlotConfig, providers: { <id>: ProviderConfig } }`
- 一个 provider 可包含多个 model（如 anthropic provider 下挂 opus / sonnet / haiku）。

`ModelSlotConfig`：
```json
{ "provider_id": "anthropic-001", "model": "claude-opus-4-5-20251101" }
```

## 3. 模型切换

| 路径 | 行为 |
|---|---|
| `agent.json > active_model` | 当前数字员工使用的模型槽（最高优先级） |
| `providers.json > active_llm` | 全局兜底（agent 未指定时用） |
| `agent.json > llm_routing` | 启用后按 local_first / cloud_first 在两个槽间路由 |

## 4. AgentsLLMRoutingConfig

| 字段 | 默认 | 说明 |
|---|---|---|
| `enabled` | False | 关 = 只用 `active_model` |
| `mode` | `local_first` | `local_first` / `cloud_first` |
| `local` | 空 `ModelSlotConfig` | 本地模型槽 |
| `cloud` | None | 不填则用 providers.json `active_llm` |

0.0.1 只做"按模式默认走哪个槽"。智能切换（按 token / 延迟 / 失败率自动切）不在本版本范围。

## 5. 限流 / 重试（AgentsRunningConfig 内）

| 字段 | 默认 | 说明 |
|---|---|---|
| `llm_retry_enabled` | True | 瞬态错误自动重试 |
| `llm_max_retries` | 3 | 最大重试次数 |
| `llm_backoff_base` / `_cap` | 1.0 / 30.0 | 指数退避（base ≤ cap） |
| `llm_max_concurrent` | 10 | 全局并发上限 |
| `llm_max_qpm` | 0 | 60 秒滑窗 QPM（0 = 关） |
| `llm_rate_limit_pause` / `_jitter` | 60 / 5 | 429 全局暂停 + 抖动 |
| `llm_acquire_timeout` | 600 | 等待限流槽超时 |

并发与限流跨 agent 共享（只在第一次初始化时生效）。

## 6. 能力探测（capability_baseline）

- 启动时探测每个 model 的 capability（vision / function call / json mode / max context）。
- 结果缓存在 `~/.wowooai/model_capability_cache.json`。
- 多模态 prober 单独跑（[multimodal_prober.py](../../src/wowooai/providers/multimodal_prober.py)）。

## 7. 凭据隐私

- 所有 API key 仅存 `providers.json`（用户机器）。
- 后端不主动上报；UI 显示时遮罩。
- 严禁在源码、SKILL.md、site.json 中写入任何真实 API key（包括"测试 key"）。

## 8. 转录（Whisper）配套

`AgentsConfig` 中：

| 字段 | 默认 |
|---|---|
| `audio_mode` | `auto` / `native` |
| `transcription_provider_type` | `disabled` / `whisper_api` / `local_whisper` |
| `transcription_provider_id` | "" |
| `transcription_model` | `whisper-1` |

不属于聊天 LLM 路由，但归入 provider 体系统一管理。

## 9. 新增 Provider

要在 0.0.1 范围内新增内置 provider：

1. `src/wowooai/providers/<name>_provider.py` 实现 chat / streaming / capability。
2. `provider_manager.py` 注册 type → class。
3. 前端 [console/src/pages/Settings/Providers](../../console/src/pages/Settings/Providers) 加配置 UI。
4. `model_capability_cache` 与 retry / rate-limit 自动继承（不需 provider 侧改动）。

## 10. 0.0.1 不做

- 不内置任何模型权重 / 不打包本地推理后端（Ollama / LMStudio 由用户自行安装）。
- 不做企业级负载均衡 / fallback 链 / 多模型 A/B。
- 不在云端代理用户的 API 流量。
