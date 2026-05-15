# 25 — 内网穿透（Cloudflare Tunnel）

> 版本：0.0.1
> 对应代码：[src/wowooai/tunnel/](../../src/wowooai/tunnel/) · `CloudflareTunnelDriver` · `BinaryManager`

## 1. 定位

把本机后端（`http://127.0.0.1:<port>`）通过 **Cloudflare Quick Tunnel** 暴露成 `https://<rand>.trycloudflare.com`，让外部渠道（钉钉 / 飞书 webhook、Telegram bot 等需要公网回调的场景）能够回连。

**不是**：
- 不是给团队访问的"WowooAI 公网部署"——单机单用户产品。
- 不是反向代理 / 域名托管 —— 仅 trycloudflare.com 临时随机域名。
- 不是必须组件 —— 不需要 webhook 的渠道（console / iMessage / 桌面 IM 客户端）完全用不到。

## 2. CloudflareTunnelDriver

[tunnel/cloudflare.py:34](../../src/wowooai/tunnel/cloudflare.py#L34)

| 方法 | 用途 |
|---|---|
| `start(local_port)` | 启动 cloudflared 子进程，等待 trycloudflare URL 出现，返回 `TunnelInfo` |
| `stop()` | 终止子进程 |
| `health_check()` | 返回当前是否在跑 |
| `get_public_url()` / `get_info()` | 拿当前公网 URL |

### 2.1 TunnelInfo

```python
@dataclass
class TunnelInfo:
    public_url: str       # https://abc123.trycloudflare.com
    public_wss_url: str   # wss://abc123.trycloudflare.com
    started_at: datetime
    pid: Optional[int]
```

### 2.2 启动行为

1. 通过 `BinaryManager` 拿 cloudflared 路径（详见 §3）；
2. spawn `cloudflared tunnel --url http://localhost:<port>`；
3. 监听 stderr，正则 `_URL_RE` 匹配 `*.trycloudflare.com`；
4. **30 秒**超时未拿到 URL → 抛错；
5. 启动 `_monitor` 协程，cloudflared 退出时清空 `_info`（不自动重启 Quick Tunnel —— Quick Tunnel 每次会拿到新随机域名，重启会让外部 webhook 失效）。

## 3. BinaryManager

[tunnel/binary_manager.py](../../src/wowooai/tunnel/binary_manager.py)

`cloudflared` 二进制不打入安装包（避免增 30MB+），按需下载：

1. 优先用 `PATH` 中已安装的 `cloudflared`；
2. 否则下载固定版本到 `~/.wowooai/binaries/cloudflared`；
3. 校验 checksum（pinned 版本 + checksum，避免供应链）；
4. 不自动升级版本 —— 升级要随仓库代码一起推 commit。

## 4. 何时启动隧道

启动条件由用户配置决定（**不**默认启动）。典型场景：

- 钉钉 / 飞书 / 微信 群机器人需要公网 callback URL；
- Telegram bot polling 不需要隧道（主动拉），webhook 模式才需要；
- iMessage / console 不需要。

各渠道的 channel adapter 在 `enabled=True` 且需要 webhook 时调 `CloudflareTunnelDriver.start(...)` 拿 URL，写入对应 webhook 配置。

## 5. URL 不稳定性

**Quick Tunnel 每次启动得到随机域名**：

- 后端重启 → URL 变化 → 已配置的渠道 webhook 失效；
- 用户每次重启需要回去对应渠道更新 webhook URL；
- 0.0.1 不做 Named Tunnel（要求 Cloudflare 账号 + DNS）—— 复杂度太高。

UI 应在 `/control/channels` 显眼显示当前 trycloudflare URL，并提供"复制"按钮。

## 6. 健康检查

`health_check()` 仅检查子进程是否存活。**不**做：

- HTTP probe 隧道是否真能通；
- 自动重启（Quick Tunnel 重启会换 URL，反而引入混乱）；

cloudflared 异常退出 → driver 把 `_info` 清空 → UI 显示"隧道已断"，用户决定是否手动重启（重启即换 URL）。

## 7. 与渠道的协作

```
启动 channel
   ├─ channel 需要 webhook?
   │     ├─ 否 → 直接连
   │     └─ 是 → 调 CloudflareTunnelDriver.start(local_port)
   │              ├─ 拿 public_url
   │              ├─ 写入 channel 的 webhook config
   │              └─ channel 上传 webhook 到第三方平台
   │
关闭 channel
   └─ 不一定关 tunnel（其他 channel 可能复用）
```

## 8. 凭据隐私

- Quick Tunnel 不需要 Cloudflare 账号，无凭据；
- 隧道一旦建立，**所有发往公网 URL 的请求都会进本地后端** —— 后端 API 鉴权（Bearer token）是唯一防线；
- 用户应避免把含 Bearer token 的内部 API 路径泄露到公网；
- 仓库**严禁**包含真实 trycloudflare URL 样本。

## 9. 0.0.1 不做

- 不做 Named Tunnel（不需要用户登录 Cloudflare）。
- 不做多隧道同时运行（一个进程一个隧道）。
- 不做断线自动重启（避免域名漂移产生更多麻烦）。
- 不做其他隧道方案（ngrok / frp / localtunnel）。
- 不做隧道流量统计 / 限速。
