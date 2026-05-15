---
name: desktop_control
description: "当用户需要操作本机桌面应用（如 Excel、钉钉、内部 ERP、IM 客户端等）并触发点击、键入或截屏验证时，使用本 skill。配合 desktop_app（启动/聚焦/列窗口/退出）、desktop_screenshot（看屏幕）、desktop_input（鼠标键盘注入）三个工具，构成「看屏幕 → 推坐标 → 点击/键入 → 再看屏幕」的闭环。网页任务一律转给 browser_use，不要用本 skill。"
metadata:
  builtin_skill_version: "1.0"
  wowooai:
    emoji: "🖥️"
    requires: {}
---

# 桌面应用控制

让 Agent 像人类一样操作本机 macOS / Windows 桌面应用。

## 什么时候使用

- 用户要求"打开桌面上的 xxx.xlsx / xxx.docx"并对内容进行查看或操作
- 用户要求操作本地 app：Excel、Numbers、Word、Pages、钉钉、飞书桌面端、企业微信、内部 ERP / SAP / OA 客户端
- 网页流程下载完文件后，需要在本地 app 中继续处理

## 什么时候**不**使用

- 网页上能完成的任务一律用 `browser_use`，不要用 `desktop_input` 去点网页
- 纯文本/Office 文件读写已有专用 skill：`xlsx` / `docx` / `pptx` / `pdf` 优先用 Python 脚本处理，不要点 GUI
- 不要用本 skill 录屏、做宏、批量自动化无监督任务

## 三个工具的分工

- `desktop_app`：app 生命周期与窗口聚焦
  - `launch` 启动、`activate` 切前台、`list_windows` 列可见/托盘窗口、`focus_window` 按标题子串聚焦、`ensure_frontmost` **稳态化复合操作（推荐）**、`zoom_window` 可选最大化、`quit` 退出
- `desktop_screenshot`：截屏（已有工具）
  - 默认全屏；macOS 下 `capture_window=true` 让用户点选一个窗口
- `desktop_input`：单步鼠标/键盘操作
  - 一次调用只做一个动作：`move_to` / `click` / `double_click` / `right_click` / `drag` / `type_text` / `press_keys` / `scroll` / `screen_size`

## 强制循环

每次想点击或输入前**必须**先把目标窗口稳态化并截屏，操作后**也必须**再截屏验证：

1. `desktop_app(action="ensure_frontmost", name="<AppName>", title_substring="<窗口标题片段>")` —— 自动恢复最小化、抢到前台、二次校验
2. `desktop_screenshot` → 看清当前界面
3. 从图中找目标控件，结合 `desktop_input(action="screen_size")` 推算像素坐标
4. `desktop_input(action="click", x=..., y=...)` 触发动作（每次只发一个 action）
5. `desktop_screenshot` 再次截屏，确认结果符合预期
6. 失败处理：连续 2 次操作未达预期，停止动作并向用户报告，不要盲目重试

## 坐标与分辨率

`desktop_input` 的坐标是**屏幕像素**，原点为主屏左上角 `(0, 0)`。

- 在 macOS Retina 屏上，截图的像素尺寸通常是真实屏幕坐标的 2 倍。先调用 `desktop_input(action="screen_size")` 获取真实屏幕宽高（如 `1920x1080`），再用截图中估算的位置按比例换算（截图 3840×2160 → 屏幕 1920×1080，要把截图坐标除以 2）。
- 屏外坐标会被拒绝（返回 `error`），不要自己裁剪。

## 跨平台键盘

`press_keys` 接收一个键名数组，组合键示例：

```json
{"action": "press_keys", "keys": ["cmd", "c"]}
```

- 在 Windows 上，`cmd` / `command` / `meta` 会被自动映射为 `win`
- 在 Linux 上，会被映射为 `super`
- `option` 自动映射为 `alt`
- 模型可以始终用 macOS 写法（`cmd`、`option`），跨平台无需改

## 典型流程示例

> 用户：「打开桌面上的 `关联数据.xlsx`，截屏给我看前 10 行内容。」

1. 启动 app：
   ```json
   {"tool": "desktop_app", "action": "launch", "name_or_path": "Microsoft Excel"}
   ```
   或更通用的方式（让 macOS 选默认 app）：
   ```json
   {"tool": "execute_shell_command", "command": "open ~/Desktop/关联数据.xlsx"}
   ```
2. 等 1-2 秒让 app 起来，再截屏：
   ```json
   {"tool": "desktop_screenshot"}
   ```
3. 用 `view_image` 看截图，直接在回复里描述前 10 行内容。

> 用户：「在打开的 Excel 里把光标定位到 A1，粘贴一下。」

1. `desktop_app(action="ensure_frontmost", name="Microsoft Excel")` 把 Excel 拉到前台并验证
2. `desktop_screenshot` 看清 A1 在哪
3. `desktop_input(action="click", x=..., y=...)` 点击 A1
4. `desktop_input(action="press_keys", keys=["cmd", "v"])` 粘贴
5. `desktop_screenshot` 验证

## 失败兜底

- 点击后没反应：调 `desktop_app(action="ensure_frontmost", name="<AppName>", title_substring="...")`，它会自动 deminimize、抢前台、重试并校验；然后再截屏重试一次
- 控件位置漂移（窗口被拖动 / 分辨率变化）：重新截屏定位，不要复用旧坐标
- 窗口被最小化到 Dock / 任务栏：`ensure_frontmost` 会自动恢复并把它带回前台
- `list_windows` 返回里看到某条 `tray: true`：表示 app 在跑但当前没有可见窗口（如钉钉/微信缩到托盘），需要 `ensure_frontmost` 把窗口召出来
- Windows 上 `focus_window` 报 `LockSetForegroundWindow` 拦截：用 `ensure_frontmost` 会自动重试到超时（默认 1500ms）
- 连续 2 次失败：停止，向用户说明当前看到的画面和卡住的原因，让用户决定继续还是放弃
- 不要在用户没明确要求时做"模糊的智能"操作，例如不要主动关闭未保存的窗口、不要主动同意系统对话框

## 何时用 `zoom_window`

**默认不要**最大化窗口。只有当出现下面任一情况时，再显式调用：

- 当前窗口太小，关键控件被裁掉或挤在一起，截屏看不清；
- 侧栏被折叠，看不到目标会话/标签页；
- 用户明确说"先把窗口拉大"。

调用之后**所有先前估算的坐标全部作废**——必须立即重新 `desktop_screenshot` 重新定位。macOS 用 zoom 按钮（绿灯钮）等价方式，**不会**切 Space / 进入全屏；Windows 用 `SW_MAXIMIZE`。

```json
{"action": "zoom_window", "name": "DingTalk", "title_substring": "张三"}
```

## 注意

- 本 skill 只做单步动作；批量场景请把动作拆成多次工具调用
- 不要尝试通过 `desktop_input` 截屏或读剪贴板，截屏走 `desktop_screenshot`、文件走 `read_file`
- macOS 首次执行时系统可能弹出辅助功能/屏幕录制授权窗口，需用户手动同意；如未授权，工具会以错误形式返回
- Windows 端注意输入焦点：组合键作用在当前前台窗口，先 `activate` 或 `focus_window` 再发键
