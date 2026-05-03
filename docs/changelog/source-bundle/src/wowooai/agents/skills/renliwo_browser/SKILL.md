---
name: renliwo_browser
description: "当任务涉及人力窝（renliwo）内部系统时，必须使用本工具。凡 URL 中包含 renliwo 的操作，一律使用 renliwo_browser，禁止使用 browser_use。"
metadata:
  builtin_skill_version: "2.0"
  wowoohr:
    emoji: "🏢"
    requires: {}
---

# renliwo_browser 使用说明（Action 模式）

## 什么时候必须使用本工具

以下情况必须使用 `renliwo_browser`，不得使用 `browser_use`：

- URL 包含 `renliwo`
- 用户明确提到“人力窝 / Renliwo / 内部 HR 系统”
- 登录、菜单导航、查询、提交、下载等内部站点操作

`browser_use` 对 renliwo URL 会被硬拦截并提示改用 `renliwo_browser`。

---

## 核心能力

- 使用 `snapshot + ref` 做稳定元素定位（更快更准）
- 内置 renliwo 专用动作：`login` / `nav_menu` / `nav_submenu` / `ant_select`

---

## 推荐标准流程（最稳）

1. `action='start'`
2. `action='open'`（可省略 url，默认打开 renliwo 登录页）
3. `action='login'`（从 `config.json -> plugins.renliwo` 读取账号密码）
4. `action='nav_menu'`（点顶部模块）
5. `action='nav_submenu'`（展开侧边菜单）
6. `action='nav_submenu', is_leaf=true`（进入最终页面）
7. `action='snapshot'`（获取 refs）
8. 使用 `click/type/evaluate/wait_for` 等动作完成业务操作

> 注意：登录后不要直接 `goto` 业务 URL。renliwo 常会跳回登录页，应通过菜单层级进入。

---

## 可用 Actions

### 生命周期
- `start`：启动浏览器（`headed=True` 可开可视窗口）
- `stop`：关闭浏览器并清理状态
- `status`：查看当前运行状态与页面信息

### 导航与登录（renliwo 专用）
- `open`：打开页面（默认登录页）
- `login`：自动登录（配置缺失会报错）
- `nav_menu`：点击顶部菜单（参数：`menu_text`）
- `nav_submenu`：侧栏菜单操作（参数：`item_text`，可配 `is_leaf`）

### 页面交互
- `snapshot`：抓取 ARIA 快照，返回 `refs`
- `click`：点击（优先用 `ref`）
- `type`：输入
- `wait_for`：等待文本出现/消失或固定时长
- `evaluate`：执行页面 JS
- `press_key`：键盘输入
- `ant_select`：Ant Design 下拉选择（参数：`label` + `value`）

### 其它
- `screenshot`：截图
- `tabs`：标签页管理（`list/new/select/close`）
- `file_upload`：文件上传
- `handle_dialog`：处理弹窗
- `cookies_clear`：清空 cookies（强制下次重登）

---

## 参数重点

- `page_id`：多标签页时标识页面，默认 `default`
- `ref`：来自 `snapshot` 的稳定元素引用（优先于 selector）
- `frame_selector`：在 iframe 内操作时使用
- `menu_text`：`nav_menu` 用
- `item_text` / `is_leaf`：`nav_submenu` 用
- `label` / `value`：`ant_select` 用

---

## 配置要求（login 依赖）

在 `config.json` 中配置：

```json
{
  "plugins": {
    "renliwo": {
      "username": "your_username",
      "password": "your_password",
      "base_url": "https://ereference-v-uat.renliwo.com"
    }
  }
}
```

---

## 最佳实践

- 每到新页面先 `snapshot`，后续尽量用 `ref` 操作
- 菜单跳转后加 `wait_for` 或使用内置 `wait_after`
- Ant Design 表单优先 `ant_select`，不要硬写复杂 selector
- 一个流程结束后可不 `stop`，复用会话更快

---

## 导出行为规则（重要）

renliwo 系统的「导出/批量导出」按钮有两种不同的工作方式，**不可混淆**：

### 1. 直接下载（绝大多数页面）
点击按钮后，**浏览器直接触发文件下载**，文件默认保存到用户**桌面（~/Desktop）**，无需其他步骤。

已确认直接下载的页面（节选）：
- 专项职能外包：任务列表（批量导出）、开票进度（查询导出）、订单审核运营（查询导出）
- 综合管理：合同产品列表、外包项目列表、任务类型管理
- 通用岗位外包：订单审核（运营）
- 业财一体：记账规则、常规业务请款、子订单列表、付款单列表、对私付款明细、项目客户关系、正常订单认款、对私支付单、审批中心

**操作指引**：使用 `action='export', btn_text='查询导出'`（默认保存桌面）；若用户指定路径则加 `save_to='...'`。
⚠️ 禁止用 `action='click'` 直接点导出按钮——有头模式会弹 macOS 系统 Save As 对话框导致卡住。

### 2. 异步导出中心（少数页面）
点击按钮后，**系统创建异步导出任务**，文件生成后须到「综合管理 → 导出中心 → 异步导出记录」页面下载。

已确认走异步导出的页面：
- 综合管理：到款认款表（查询导出）
- 专项职能外包：渠道费账单（常规查询导出）、费用结算财务（批量导出）

**操作指引**：
1. 点击导出按钮，等待 3 秒
2. 导航到「综合管理 → 导出中心 → 异步导出记录」
3. 等待列表中出现新的导出记录，状态变为「文件已生成」
4. 点击操作列的「下载」链接

### 3. 导出无响应（数据为空或权限不足）
当当前查询结果为空，或账号对该模块无导出权限时，点击导出按钮**不会有任何提示或下载**。
处理方式：先确认表格中有数据，再点击导出；若仍无响应，说明账号无权限。

### ⚠️ 禁止使用的错误说法
- ❌「所有导出都走异步导出中心」— **错误**，绝大多数是直接下载
- ❌「需要去异步导出中心查看」— 只有少数特定页面才走异步流程
- 正确表述：「该页面的导出会直接下载到本地」或「该页面的导出会进入异步导出队列，需要到导出中心下载」
