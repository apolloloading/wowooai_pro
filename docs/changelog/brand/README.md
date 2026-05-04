# WowooAI 品牌资产

> 此目录是 WowooAI 品牌 SVG 的**权威来源**。`console/public/` 中的同名文件由此处复制而来。

---

## 文件清单

| 文件 | 用途 | 对应前端位置 |
|---|---|---|
| `wowooai-logo.svg` | 通用主 logo（带文字） | `console/public/wowooai-logo.svg` |
| `favicon.svg` | 浏览器标签页图标 + 聊天 AI 头像 | `console/public/favicon.svg` |
| `logo-light.svg` | 浅色背景版（Header / Login） | `console/public/logo-light.svg` |
| `logo-dark.svg`  | 深色背景版（Header / Login） | `console/public/logo-dark.svg` |

> 日常只会用到 `favicon.svg` + `logo-light.svg`。`logo-dark.svg` 留给暗色模式使用。

---

## 配色规范

| 用途 | HEX | 备注 |
|---|---|---|
| 主蓝 | `#2563EB` | 品牌主色（Tailwind `blue-600`） |
| 高光蓝 | `#38BDF8` | 渐变高光（Tailwind `sky-400`） |
| 深蓝 | `#1E3A8A` | 渐变阴影底色（Tailwind `blue-900`） |
| 文字（浅底） | `#0F172A` | Tailwind `slate-900` |
| 文字（深底） | `#E0F2FE` | Tailwind `sky-100` |
| 副高光（圆环阴影） | `#BAE6FD` / `#DBEAFE` | sky-200 / blue-100 |

---

## 如何同步到前端

```bash
# 从品牌目录复制到前端静态资源
cp docs/changelog/brand/favicon.svg     console/public/favicon.svg
cp docs/changelog/brand/logo-light.svg  console/public/logo-light.svg
cp docs/changelog/brand/logo-dark.svg   console/public/logo-dark.svg
cp docs/changelog/brand/wowooai-logo.svg console/public/wowooai-logo.svg
```

---

## 设计说明

- 图形：W 折线 + AI node 圆点 + `wowooai` 字标，品牌色 `#2563EB`（Tailwind blue-600）。
- 复刻者可直接 `cp docs/changelog/brand/*.svg console/public/` 完成同步，无需调整任何前端代码。
- 所有素材均为 SVG，矢量无损。
