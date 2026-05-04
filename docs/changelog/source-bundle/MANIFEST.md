# source-bundle 说明

> 这个目录是 [docs/changelog/](..) 的**附属源码包**。把整个 `docs/changelog/` 目录交付出去时，必须连带本目录一起。
>
> 目标：让阅读者在一份干净的原 qwen 源码上，直接拿到改造成 WowooAI 所需的大文件、py 源码、技能目录、前端 logo 与关键页面源码，而不需要依赖历史分支或 commit。

---

## 目录内容

```text
source-bundle/
├── pyproject.toml
├── scripts/
│   ├── pack/build_macos.sh
│   └── wheel_build.sh
├── src/wowooai/
│   ├── __version__.py
│   ├── cli/
│   │   ├── app_cmd.py
│   │   └── desktop_cmd.py
│   ├── app/
│   │   ├── migration.py
│   │   └── routers/
│   │       ├── agents.py
│   │       └── skills.py
│   ├── config/
│   └── agents/
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── renliwo_browser.py
│       │   ├── file_io.py
│       │   └── shell.py
│       ├── md_files/{zh,en}/SOUL.md
│       └── skills/
│           ├── renliwo_browser/
│           ├── onboarding-guide-{zh,en}/
│           ├── ai_create_agent-{zh,en}/
│           ├── ai_create_cron_job-{zh,en}/
│           └── ai_create_skill-{zh,en}/
├── tests/e2e/
└── console/
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── public/
    └── src/
```

bundle 规模参考：

```bash
find docs/changelog/source-bundle -type f | wc -l   # 365
du -sh docs/changelog/source-bundle                # 约 3.3M
```

---

## 如何使用

### 方式 A：覆盖到一个已有仓库

在仓库根目录执行：

```bash
SRC=/path/to/docs/changelog/source-bundle
DST=/path/to/target-repo

rsync -a "$SRC/" "$DST/"
```

然后执行校验：

```bash
cd "$DST"
.venv/bin/python -m compileall src/wowooai/agents/tools/renliwo_browser.py \
  src/wowooai/agents/tools/file_io.py \
  src/wowooai/agents/tools/shell.py

find console/public -maxdepth 1 -type f | sort
.venv/bin/pytest tests/e2e/ -m e2e --co
```

### 方式 B：只取某一类文件

```bash
# 只取后端大 py 文件
rsync -a docs/changelog/source-bundle/src/wowooai/agents/tools/ \
  src/wowooai/agents/tools/

# 只取技能目录
rsync -a docs/changelog/source-bundle/src/wowooai/agents/skills/ \
  src/wowooai/agents/skills/

# 只取前端 logo / 静态资源
rsync -a docs/changelog/source-bundle/console/public/ \
  console/public/
```

---

## 必须附带的后端源码

| 文件 / 目录 | 为什么必须带 |
|---|---|
| `src/wowooai/agents/tools/renliwo_browser.py` | 人力窝浏览器工具是完整 py 文件，约 1829 行，无法靠片段复刻 |
| `src/wowooai/agents/skills/renliwo_browser/` | renliwo_browser 的技能说明和页面结构 data |
| `src/wowooai/agents/tools/file_io.py` | 桌面沙箱写文件逻辑在完整 tool 文件中 |
| `src/wowooai/agents/tools/shell.py` | shell 破坏性命令拦截在完整 tool 文件中 |
| `src/wowooai/agents/md_files/{zh,en}/SOUL.md` | agent 系统提示里的沙箱规则 |
| `src/wowooai/cli/app_cmd.py` | 8088 默认端口、`WOWOOAI_API_BASE_URL` 注入、父进程 watchdog |
| `src/wowooai/cli/desktop_cmd.py` | `WOWOOAI_PARENT_PID` 注入 |
| `src/wowooai/app/migration.py` | 默认 agent id、scene_prompts、内置技能安装 |
| `src/wowooai/app/routers/agents.py` | agent schema / scene_prompts 返回 |
| `src/wowooai/app/routers/skills.py` | `POST /api/skills` 手动/AI 创建技能路径 |
| `src/wowooai/config/` | 目标实现使用配置包目录，而不是单文件 `config.py` |
| `src/wowooai/agents/skills/onboarding-guide-*` | 知识库技能 v5 |
| `src/wowooai/agents/skills/ai_create_*` | 三个 AI 创建技能 |
| `tests/e2e/` | E2E 自动化验证 |

---

## 必须附带的前端源码 / 资产

| 文件 / 目录 | 为什么必须带 |
|---|---|
| `console/public/` | logo、favicon、背景图等静态资产 |
| `console/index.html` | favicon 和 title |
| `console/package.json` | 前端包名、版本、依赖脚本 |
| `console/vite.config.ts` | 8088 代理 / 构建配置 |
| `console/src/layouts/` | Header / Sidebar / MainLayout |
| `console/src/pages/` | 目标 Console 页面目录：Chat、Knowledge、Login、PersonalCenter |
| `console/src/App.tsx` / `main.tsx` / `i18n.ts` / `locales/` | 应用入口、语言锁定、文案 |
| `console/src/api/` | 前端 API 类型与请求模块 |
| `console/src/components/` | 页面依赖组件（包括部分旧组件，避免 import 断裂） |
| `console/src/constants/` / `hooks/` / `utils/` / `styles/` | 运行所需配套代码 |
| `console/src/contexts/ThemeContext.tsx` | 默认 light 主题 |
| `console/src/stores/agentStore.ts` | 默认选中 `wowooai` |

### source-bundle 中的 logo / 静态资产

```text
console/public/favicon.svg
console/public/logo-dark.svg
console/public/logo-light.svg
console/public/wowooai.png
console/public/wowooaiBack.png
```

> 如果要使用蓝色调品牌图，把 [../brand/](../brand/) 下同名 SVG 覆盖到 `console/public/` 即可，前端无需改代码。

---

## 目标项目页面目录

复刻完成后，目标项目的 `console/src/pages/` 应包含以下目录：

```text
console/src/pages/Chat/
console/src/pages/Knowledge/
console/src/pages/Login/
console/src/pages/PersonalCenter/
```

bundle 严格按这个交付结构组织，不引入文档中提到但实际不需要交付的目录。

---

## 快速完整性校验

```bash
# 后端大文件行数
wc -l docs/changelog/source-bundle/src/wowooai/agents/tools/renliwo_browser.py  # 1829
wc -l docs/changelog/source-bundle/src/wowooai/agents/tools/file_io.py          # 449
wc -l docs/changelog/source-bundle/src/wowooai/agents/tools/shell.py            # 556

# logo / 静态资源
find docs/changelog/source-bundle/console/public -maxdepth 1 -type f | sort

# 技能版本
G=docs/changelog/source-bundle
grep -l 'builtin_skill_version: "2.2"' \
  $G/src/wowooai/agents/skills/ai_create_*/SKILL.md | wc -l  # 6

grep '"5"' $G/src/wowooai/agents/skills/onboarding-guide-zh/SKILL.md

# 不应带缓存 / node_modules / dist
find docs/changelog/source-bundle \( -name '__pycache__' -o -name '*.pyc' -o -name node_modules -o -name dist \) -print
# 期望：无输出
```
