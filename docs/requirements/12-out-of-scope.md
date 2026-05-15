# 12 — 0.0.1 明确不做

> 版本：0.0.1
> 用途：把"不做"集中列一份清单，避免 PR / issue 反复辩论。
> 各模块详细的"不做"也在各自文档末尾的 §"0.0.1 不做"中。

## 1. 平台与分发

- **不做 macOS 代码签名 / notarization**：自签名分发，首次打开需用户右键 → 打开。
- **不做 Windows 数字签名 / SmartScreen 白名单**。
- **不做自动更新**（无 Sparkle / Squirrel）。用户更新需重新下载安装包。
- **不做 Linux 桌面包**（仅源码可跑）。
- **不做应用商店分发**（Mac App Store / Microsoft Store / Snap / Flatpak）。
- **不做精简版**（CPU-only / 不带 Chromium）—— 全功能单一安装包。
- **不做手机端 / iPad 端**。

## 2. 多用户与协作

- **不做多用户登录**（单机单用户）。
- **不做团队协作 / 实时多人编辑工作区**。
- **不做企业级 RBAC / 多租户隔离**。
- **不做 SSO / OIDC / SAML**。

## 3. 云端与运营

- **不做云端 SaaS**（不在云端代理用户的 LLM 流量）。
- **不做远程托管**（MCP / ACP 全部本机进程）。
- **不做服务端日志上报 / 用户行为埋点**。
- **不做云端配置同步 / 跨设备同步**。

## 4. 模型与推理

- **不内置模型权重**。
- **不打包本地推理后端**（Ollama / LMStudio 由用户自行安装）。
- **不做企业级负载均衡 / fallback 链 / 多模型 A/B**。
- **不做按 token / 延迟 / 失败率自动智能切换**（路由仅做 local_first / cloud_first 静态模式）。
- **不做模型微调 / 训练**。

## 5. 工具与技能

- **不做 OCR**（如需识图中文字，由模型从截图中读取）。
- **不做录制 / 回放 / 宏**。
- **不做内置 MCP server**（只做 client 接入）。
- **不做 ACP agent server**（只做 client 调用外部 agent）。
- **不做 MCP / ACP 间桥接**（如把外部 agent 暴露成 MCP 工具）。
- **不做技能市场 / 插件市场**（plugin 仅通过 `config.json` 配置）。
- **不做技能版本管理**（同名 skill 直接覆盖）。

## 6. 渠道

- **不做企业版渠道 SDK 接入**（如企业微信 IPaaS、Salesforce）。
- **不做声音克隆 / TTS**（仅做 STT / Whisper 转录）。
- **不做视频通话渠道**（Zoom / Meet / Teams 视频）。
- **不做支付 / 订阅**。

## 7. 安全

- **不做 macOS Accessibility / TCC 授权引导**（首次使用由系统弹窗，需用户手动同意）。
- **不做端到端加密**（消息在内存与本地磁盘明文流转，靠 OS 文件系统权限保护）。
- **不做敏感词 / 内容审核**（输出内容由模型决定）。
- **不做审计日志合规导出**（CSV / SIEM 上报）。

## 8. 调度与可观测

- **不做跨设备 / 跨 agent 全局调度**（每个 workspace 各自独立）。
- **不做任务依赖图 / DAG 编排**。
- **不做 retry policy**（cron 失败就失败；用户可用 `cron run` 手动补跑）。
- **不做 Prometheus / OpenTelemetry 指标导出**。

## 9. 前端

- **不做主题切换**（默认浅色 + 系统色跟随）。
- **不做插件市场页面**（plugin 仅通过 `config.json` 配置）。
- **不做团队协作 / 实时多人编辑工作区**。
- **不做 PWA / 离线缓存**。

## 10. 桌面控制

- **不做 macOS Accessibility 全自动授权**。
- **不做 OCR 识屏文字**。
- **不做录制 / 回放 / 宏**。
- 阶段 1 仅做"视觉派 MVP"（截屏 + 坐标输入），阶段 2 才考虑 AX/UIA 结构化适配（不在 0.0.1 范围）。

## 11. 凭据（绝对约束）

仓库与发布产物绝对不允许出现：

- 真实账号 / 密码 / API key / token / 证书。
- 测试 / 演示用的"已脱敏但实际可用"的凭据。
- 内置 SKILL.md / site.json / 内置工具源码中的任何登录信息。

凭据只能存在用户机器上：
- `~/.wowooai/providers.json` — LLM API key
- `~/.wowooai/workspaces/<id>/agent.json > channels` — 渠道 token / secret
- `~/.wowooai/config.json > plugins.<plugin_id>` — 插件凭据

## 12. 浏览器登录（绝对约束）

- 浏览器自动化工具（`browser_use` / `renliwo_browser` / `agent-browser`）默认有头模式。
- **绝对禁止**用 `action=type` 自动填账号 / 密码 / 验证码 / 短信 OTP / 滑动验证。
- 即使配置或环境变量中存在凭据，也不要自动填充。
- 登录由用户在可见浏览器窗口手动完成；agent 等待用户确认"已登录"后继续。

---

## 附：未来版本可能做（不承诺）

- 0.1.x 候选：macOS notarization、自动更新、Linux 桌面包。
- 0.2.x 候选：阶段 2 桌面控制（AX/UIA）、内置 MCP server。
- 1.0 之前不会做：多用户、企业 RBAC、云端 SaaS。
