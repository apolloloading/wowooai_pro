# 06 — 安全与守卫

> 版本：0.0.1
> 对应代码：[src/wowooai/security/](../../src/wowooai/security/) · [src/wowooai/agents/tool_guard_mixin.py](../../src/wowooai/agents/tool_guard_mixin.py) · [src/wowooai/agents/tools/file_io.py](../../src/wowooai/agents/tools/file_io.py) · [src/wowooai/agents/tools/shell.py](../../src/wowooai/agents/tools/shell.py)

## 1. 三层守卫

| 层 | 文件 | 拦什么 |
|---|---|---|
| 工具守卫（ToolGuard） | [security/tool_guard/](../../src/wowooai/security/tool_guard/) | 命令注入、危险参数模式 |
| 文件守卫（FileGuard） | `tool_guard_mixin._file_guard_guardian` | 敏感文件读写 |
| 技能扫描（SkillScanner） | [security/skill_scanner/](../../src/wowooai/security/skill_scanner/) | SKILL.md 内容审查 |

## 2. 审批级别（approval_level）

存于 `agent.json > approval_level`，默认 `AUTO`。

| 级别 | 行为 |
|---|---|
| `OFF` | 跳过 tool guard，所有工具直接执行 |
| `STRICT` | 所有工具调用都需审批 |
| `SMART` | 低风险（LOW / INFO）发现自动放行；中高风险进入审批 |
| `AUTO`（默认） | 仅 guarded tools 走完整规则；非 guarded 只跑 always-run guardian（如文件防护） |

`denied_tools` 优先级最高：命中即拒绝、不可审批。

## 3. ToolGuardConfig

| 字段 | 默认 |
|---|---|
| `enabled` | True |
| `guarded_tools` | None（用内置默认集）/ `[]`（不守卫任何工具） |
| `denied_tools` | `[]` |
| `custom_rules` | `[]`（用户自定义规则） |
| `disabled_rules` | `[]`（关闭某些内置规则） |
| `shell_evasion_checks` | 全部 False（按需打开） |

### 3.1 Shell evasion 检查

[security/tool_guard/](../../src/wowooai/security/tool_guard/) 中的子检查：

```python
{
    "command_substitution": False,
    "obfuscated_flags": False,
    "backslash_escaped_whitespace": False,
    "backslash_escaped_operators": False,
    "newlines": False,
    "comment_quote_desync": False,
    "quoted_newline": False,
}
```

默认全关；用户在严格场景可开启。

## 4. FileGuardConfig

| 字段 | 默认 |
|---|---|
| `enabled` | True |
| `sensitive_files` | `[]` |

`sensitive_files` 中的文件不可被 `read_file` / `write_file` / `edit_file` 访问，命中即拒绝。

## 5. 副本沙箱（核心规则）

### 5.1 受保护的用户原始目录

```python
_PROTECTED_USER_DIRS = ("Desktop", "Documents", "Downloads")
```

写入、编辑、覆盖以下路径下的文件时：

- `~/Desktop/**`
- `~/Documents/**`
- `~/Downloads/**`

必须先在 `<workspace>/.sandbox/input/` 下创建 `<原名>_副本.<ext>`，再对副本操作。

### 5.2 三层约束（必须同时生效）

1. **提示词层**：[md_files/zh/AGENTS.md](../../src/wowooai/agents/md_files/zh/AGENTS.md) / [SOUL.md](../../src/wowooai/agents/md_files/zh/SOUL.md) 写明沙箱准则。
2. **文件工具层**：`_sandbox_copy_for_write` 自动重定向到沙箱副本。
3. **Shell 工具层**：`_check_destructive_command` 拦截以下绕过路径——
   - 重定向覆盖：`>`, `>>`, `&>`, `2>>` 等
   - inline edit：`sed -i`, `perl -i`, `awk -i inplace`
   - in-place 修改：`mv`, `dd`, `shred`, `truncate`
   - 写入目标命令：`tee`, `cp`, `install`, `ln`, `rsync`, `touch`, `chmod`, `chown`
   - 编辑器：`vim`, `vi`, `nano`, `emacs`, `ed`, `code`, `subl`, `open`
   - 解释器 inline：`python -c`, `node -e`, `ruby -e`, `perl -e/-pe/-ne`

### 5.3 删除类操作

`rm` / `rmdir` / `unlink` **不属于副本沙箱规则**，按普通风险操作处理。

### 5.4 例外

用户在当次会话明确说"原地修改 / 覆盖原文件"才允许覆盖。

## 6. 技能扫描器（SkillScanner）

| 字段 | 默认 |
|---|---|
| `mode` | `warn`（默认）/ `block` / `off` |
| `timeout` | 30 秒 |
| `whitelist` | `[]`（`SkillScannerWhitelistEntry { skill_name, content_hash }`） |

- `block`：扫描并阻止不安全 skill 加载
- `warn`：仅记录警告日志
- `off`：完全关闭

白名单中 `content_hash=""` 表示任意内容都放行。

## 7. 凭据隐私（绝对约束）

仓库与运行时绝对不允许出现以下内容：

- 真实账号 / 密码 / API key / token / 证书。
- 测试 / 演示用的"已脱敏但实际可用"的凭据。
- 内置 SKILL.md / site.json / 内置工具源码中的任何登录信息。

凭据只能存在以下位置（用户机器）：

- `~/.wowooai/providers.json` — LLM API key
- `~/.wowooai/workspaces/<id>/agent.json > channels` — 渠道 token / secret
- `~/.wowooai/config.json > plugins.<plugin_id>` — 插件凭据（如 `plugins.renliwo[site_id]`）

## 8. 浏览器登录硬规则

[browser_visible / browser_cdp / agent_browser SKILL.md](../../src/wowooai/agents/skills/) 全部要求：

- 浏览器自动化工具（`browser_use` / `renliwo_browser` / `agent-browser`）默认有头模式。
- 绝对禁止用 `action=type` 自动填账号 / 密码 / 验证码 / 短信 OTP / 滑动验证。
- 即使配置或环境变量中存在凭据，也不要自动填充。
- 登录由用户在可见浏览器窗口手动完成；agent 等待用户确认"已登录"后继续自动化操作。

## 9. API 鉴权 / 网络访问

`SecurityConfig.allow_no_auth_hosts` 默认：

```python
["127.0.0.1", "::1"]
```

只有这两个 IP 可以无鉴权访问 API。其他 IP 必须带 token。

## 10. 0.0.1 不做

- 不引入 macOS Accessibility / TCC 授权引导（首次使用由系统弹窗，需用户手动同意）。
- 不做 macOS 代码签名 / notarization（本版本桌面包自签名分发）。
- 不做企业级 RBAC / 多租户隔离。
- 不做端到端加密（消息在内存与本地磁盘明文流转，靠 OS 文件系统权限保护）。
