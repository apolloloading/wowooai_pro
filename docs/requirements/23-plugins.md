# 23 — 插件体系（Plugins）

> 版本：0.0.1
> 对应代码：[src/wowooai/plugins/](../../src/wowooai/plugins/) · `config.json > plugins`

## 1. 定位

**插件** = 第三方包可以向 wowooai 注入：

- LLM Provider（新增模型供应商类型）
- Startup / Shutdown 钩子
- Control commands（新的 `/xxx` 命令）

插件**不**等同于 SKILL —— SKILL 是 markdown，靠模型自然加载；插件是 Python 代码，扩展后端能力。

## 2. 插件发现路径

[app/_app.py:318](../../src/wowooai/app/_app.py#L318) 启动时只扫描一个目录：

```python
plugin_dirs = [get_plugins_dir()]
```

`get_plugins_dir()` → `~/.wowooai/plugins/`（用户机器）。
仓库内**不**内置任何插件目录。

## 3. 插件目录结构

```
~/.wowooai/plugins/<plugin_id>/
├─ manifest.json     ← PluginManifest
└─ plugin.py         ← 入口（或 manifest.entry.backend 指向其他文件）
```

`manifest.json`（[plugins/architecture.py:18 PluginManifest](../../src/wowooai/plugins/architecture.py#L18)）：

```json
{
  "id": "renliwo",
  "name": "Renliwo 集成",
  "version": "0.1.0",
  "description": "...",
  "author": "...",
  "entry": {
    "backend": "plugin.py",
    "frontend": null
  },
  "dependencies": [],
  "min_version": "0.1.0",
  "meta": {}
}
```

## 4. 插件入口

`plugin.py` 必须导出一个 `plugin` 对象，实现 `register(api)` 方法，通过 [plugins/api.py PluginApi](../../src/wowooai/plugins/api.py) 注册扩展：

```python
class MyPlugin:
    def register(self, api: PluginApi):
        api.register_provider(provider_id="...", provider_class=...)
        api.register_startup_hook(name="...", hook=async_fn)
        api.register_shutdown_hook(name="...", hook=async_fn)
        api.register_control_command(name="...", handler=...)

plugin = MyPlugin()
```

## 5. PluginApi 接口

[plugins/api.py:10](../../src/wowooai/plugins/api.py#L10)

| 方法 | 用途 |
|---|---|
| `register_provider(provider_id, provider_class, ...)` | 加一种 LLM provider 类型 |
| `register_startup_hook(name, hook)` | 后端启动时调（init 完成后） |
| `register_shutdown_hook(name, hook)` | shutdown 时调 |
| `register_control_command(name, handler)` | 加 `/<name>` 命令 |
| `runtime` 属性 | 拿 RuntimeHelpers（如 `provider_manager`） |

## 6. 配置传递

`~/.wowooai/config.json`：

```json
{
  "plugins": {
    "renliwo": {
      "enabled": true,
      "site_id": "...",
      "username": "",
      "...": "..."
    }
  }
}
```

`PluginLoader.load_all_plugins(configs=plugin_configs)` 把对应 id 的配置作为参数传给 `register`，让插件读取自己的设置。

## 7. PluginRegistry

[plugins/registry.py](../../src/wowooai/plugins/registry.py)

进程内全局单例（`PluginRegistry`）保存所有注册项：

| 类 | 字段 |
|---|---|
| `ProviderRegistration` | provider_id / class / 元数据 |
| `HookRegistration` | name / hook（async callable）/ priority |
| `ControlCommandRegistration` | name / handler |

`get_provider(id)` / `get_all_providers()` / `get_startup_hooks()` / `get_shutdown_hooks()` / `get_control_commands()` 提供给后端各模块查询。

## 8. RuntimeHelpers

[plugins/runtime.py](../../src/wowooai/plugins/runtime.py)

注入给插件的"后端 SDK"：

- `provider_manager` — 可查 provider 配置 / 列模型
- 其他帮助函数（按需扩展）

插件**不应**直接 import wowooai 内部模块；通过 RuntimeHelpers 拿能力，便于版本演进时保持兼容。

## 9. 加载顺序

后端 `_app.py` 启动序列（详见 [11 §3](11-startup-runtime.md)）：

1. config 加载完毕；
2. `provider_manager` 初始化（含内置 12 种 provider）；
3. `PluginLoader` 扫描 `~/.wowooai/plugins/` → 调每个插件的 `register(api)`；
4. **plugin-provided providers** 与内置 providers 合并；
5. `MultiAgentManager` 启动 workspace 时已能看到插件 provider；
6. 启动完成 → 执行所有 `startup_hooks`。

shutdown 时倒序：先 `shutdown_hooks`，再关 workspaces。

## 10. 凭据隐私（绝对约束）

- 插件**必须**通过 `config.json > plugins.<id>` 读凭据；
- 仓库代码 / 插件源码内**严禁**硬编码任何账号 / API key（即使是测试 key）；
- 插件可写日志，但**不应**记录原始凭据；
- 插件加载失败 / 凭据缺失 → 报错日志但不要把凭据 echo 回来。

## 11. 默认插件清单（0.0.1）

仓库内置插件目录**为空**。用户机器上可能存在 `renliwo` 等业务插件，但这些**不在仓库发布范围**——只通过用户自行安装到 `~/.wowooai/plugins/` 加载。

## 12. 0.0.1 不做

- 不做插件商店 / 远程下载 / 一键安装。
- 不做插件签名 / 沙箱（插件在主进程内运行，等同于后端代码权限）。
- 不做插件热重载（增删插件需重启后端）。
- 不做前端插件扩展点（`entry.frontend` 字段保留但未生效）。
- 不做插件间依赖图（`dependencies` 字段仅信息记录）。
