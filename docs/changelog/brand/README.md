# WowooAI 品牌资产（蓝色版）

> 这套蓝色调 logo / favicon 是 WowooAI 在「原 qwen 源码 → WowooAI」改造后推荐使用的品牌视觉。**仅放在 `docs/changelog/brand/` 内**，方便复刻者按需采用，不污染 `console/public/` 中现有资产。

---

## 文件清单

| 文件 | 用途 | 推荐替换的源码位置 |
|---|---|---|
| `wowooai-logo.svg` | 通用主 logo（带文字） | `console/public/wowooai.png`（如要换成 SVG，可改 `index.html` 引用） |
| `favicon.svg` | 浏览器标签页图标 | `console/public/favicon.svg` |
| `logo-light.svg` | 浅色背景版（带文字） | `console/public/logo-light.svg` |
| `logo-dark.svg`  | 深色背景版（带文字） | `console/public/logo-dark.svg` |

> 目标桌面 / 网页 UI 默认 light 主题（见 [frontend.md §3](../frontend.md)），日常只会用到 `favicon.svg` + `logo-light.svg`。`logo-dark.svg` 留给后续可能引入的暗色模式使用。

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

## 如何采用（可选，复刻者按需）

```bash
# 把蓝色品牌图覆盖到前端静态资源
cp docs/changelog/brand/favicon.svg     console/public/favicon.svg
cp docs/changelog/brand/logo-light.svg  console/public/logo-light.svg
cp docs/changelog/brand/logo-dark.svg   console/public/logo-dark.svg

# 如果要把主 logo 也换成蓝色 SVG（替换 wowooai.png 引用）
cp docs/changelog/brand/wowooai-logo.svg console/public/wowooai-logo.svg
# 然后在引用 wowooai.png 的页面（如 Chat 头像）改为引用 wowooai-logo.svg
```

> 不强制替换。如果对现有 `wowooai.png` 满意，可以保留，本目录只作为蓝色调备选方案存档。

---

## 设计说明

- 图形完全沿用 source-bundle 内 `console/public/{favicon,logo-light,logo-dark}.svg` 的结构（W 折线 + AI node 圆点 + `wowooai` 字标），**只把品牌色从橙 `#FF7A3D` 换成蓝 `#2563EB`**，不改形状、字号、viewBox。
- 复刻者可直接 `cp docs/changelog/brand/*.svg console/public/` 完成换色，无需调整任何前端代码。
- 所有素材均为 SVG，矢量无损。
