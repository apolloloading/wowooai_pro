# QwenPaw 上游同步操作手册（v1）

> **执行者**：AI 助手（自主执行，无需用户逐步确认）
> **目标**：把 QwenPaw 上游仓库自基线 commit 之后的所有变更，逐 commit 审查并形成可决策的同步追踪文档。**只读分析，不修改任何源码、不修改任何 git 历史**。
> **预计耗时**：取决于上游 commit 数量，通常 30 分钟内完成所有分析与文档输出。

---

## 0. 关键事实（前置上下文，不要重新探索）

| 项 | 值 |
|---|---|
| 工作目录 | `/Users/rlw/AI项目/wowooai` |
| 当前分支 | `main` |
| 当前 origin | `https://github.com/apolloloading/wowooai_pro.git`（私有，可读写） |
| 上游仓库 URL | `https://github.com/agentscope-ai/QwenPaw.git` |
| **fork 基线 commit** | `283293f1ae4e6c5dcb8d3e866415bb6b8e870d37`（2026-04-29） |
| 本地仓库 commit 总数 | 13（一次性 squash 导入，基线 commit 在本地不存在，需 fetch upstream 后才可解析） |
| console 是否子模块 | 否，单一 git 仓库 |
| 输出文档目录 | `docs/changelog/upstream-sync/`（需新建） |

**已知品牌化与定制改动**（决定哪些上游 commit 应跳过）：

- 全局重命名：`qwenpaw → wowooai`、`QwenPaw → WowooAI`、`Agent → 数字员工`（UI 层）
- 我方独有模块：
  - `src/wowooai/agents/tools/renliwo_browser.py`（人力窝浏览器自动化）
  - `src/wowooai/agents/skills/onboarding-guide-{zh,en,ru}/`（入职小助手知识库）
  - `src/wowooai/agents/skills/QA_source_index-{zh,en}/`、`guidance-{zh,en}/`（已被替换）
  - `policy-diff-compare` 技能
  - `BUILTIN_QA_AGENT_*` 已改造为"入职小助手"（见 [src/wowooai/constant.py](src/wowooai/constant.py)、[src/wowooai/agents/templates.py](src/wowooai/agents/templates.py)）
  - macOS / Windows 打包脚本：`scripts/pack/build_macos.sh`、`scripts/pack/build_win.ps1`
  - `pyproject.toml` 包名 `wowooai`
- 我方独有的修复（不要被上游覆盖）：
  - memory `auto_memory_interval` 默认从 `None` 改为 `5`（commit `5a20e1ec`）
  - 桌面端 pandoc 通过 `pypandoc-binary` 绑定（commit `e2ad58ca`）
  - Windows 打包 `PACKBOT_BASE_ENV` 快速路径（commit `c7c39ebe`）

---

## 1. 执行原则（必读）

1. **只读、不改、不推**：本任务**严禁**修改任何源码、严禁 cherry-pick、严禁 merge、严禁 push。
2. **不需要询问用户**：所有决策按本手册的"分类规则"自主完成；遇到模糊情况标记 `🟠 待人工裁定` 并继续。
3. **每个 commit 都要落到追踪表里**——不能跳过、不能合并行。
4. **commit message 中文/英文都正常处理**，不要因为编码问题中断。
5. **TodoWrite 跟踪进度**，每完成一个阶段勾掉一项。
6. 所有命令在 `/Users/rlw/AI项目/wowooai` 目录下执行（除非另有说明）。

---

## 2. 阶段 1：添加 upstream 并 fetch（写时操作）

### 2.1 添加 upstream remote 并禁掉推送

```bash
cd /Users/rlw/AI项目/wowooai

# 如果 upstream 已存在则先确认，避免重复添加
git remote -v | grep -q '^upstream' && echo "upstream EXISTS, skip add" || \
  git remote add upstream https://github.com/agentscope-ai/QwenPaw.git

# 物理禁掉对 upstream 的推送（只读保护）
git remote set-url --push upstream DISABLED

# 验证
git remote -v
```

**预期输出**：
```
origin    https://github.com/apolloloading/wowooai_pro.git (fetch)
origin    https://github.com/apolloloading/wowooai_pro.git (push)
upstream  https://github.com/agentscope-ai/QwenPaw.git (fetch)
upstream  DISABLED (push)
```

### 2.2 fetch 上游历史

```bash
git fetch upstream --tags
```

**这一步只下载到 `.git/objects/`，不改工作区**。完成后立即验证：

```bash
git status   # 应仍是当前未变状态
git cat-file -t 283293f1ae4e6c5dcb8d3e866415bb6b8e870d37   # 应输出 "commit"
git remote show upstream | grep "HEAD branch"                # 记录上游主分支名（main/master/develop）
```

将 `HEAD branch` 的值赋给变量 `UPSTREAM_BRANCH`（下文以 `upstream/main` 占位，若实际是 master 则全局替换）。

### 2.3 失败处理

- 如果 `git fetch` 卡住或网络失败：等 30 秒后重试一次，仍失败则在追踪文档头部注明 `❌ fetch 失败：<错误信息>`，停止后续步骤。
- 如果 `git cat-file` 仍报 `could not get object info`：说明上游已 force-push 或 rewrite history，记录此情况后停止。

---

## 3. 阶段 2：拉取上游 commit 列表

### 3.1 创建输出目录

```bash
mkdir -p docs/changelog/upstream-sync
```

### 3.2 生成原始数据文件（供后续分析使用）

将以下三个文件写入 `docs/changelog/upstream-sync/`：

```bash
BASE=283293f1ae4e6c5dcb8d3e866415bb6b8e870d37
UP=upstream/main   # 若实际分支不同，替换之

# 文件 A：commit 列表（按时间正序，最早在前）
git log $BASE..$UP --reverse --no-merges \
  --pretty=format:"%H%x09%ad%x09%an%x09%s" --date=short \
  > docs/changelog/upstream-sync/_raw_commits.tsv

# 文件 B：每个 commit 改了哪些文件
git log $BASE..$UP --reverse --no-merges \
  --pretty=format:"=== %H | %ad | %s ===" --date=short --name-status \
  > docs/changelog/upstream-sync/_raw_commits_files.txt

# 文件 C：高频改动文件统计（冲突重灾区预警）
git log $BASE..$UP --no-merges --pretty=format: --name-only \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -50 \
  > docs/changelog/upstream-sync/_raw_hotspots.txt

# 总数
wc -l docs/changelog/upstream-sync/_raw_commits.tsv
```

**这三个 `_raw_*` 文件是中间产物，用于后续分类，但不是最终交付物**。

### 3.3 边界情况

- 若 `_raw_commits.tsv` 行数为 0：说明上游自基线之后没有新 commit，写一个简短的 `README.md` 说明情况，跳到阶段 5 仅生成框架文档即可。
- 若超过 200 个 commit：在追踪文档里**分批**（每 50 个一批，文件名 `commits-batch-01.md`、`-02.md`…），避免单个文档过长。

---

## 4. 阶段 3：自主分类规则

对每一个 commit，根据下面的**优先级规则**（从上往下匹配，命中即停）打标签：

### 4.1 标签定义

| 标签 | 含义 | 决策 |
|---|---|---|
| 🔴 **跳过-冲突** | 改了我方已重写/品牌化的文件 | 不合入，记录原因 |
| ⚪ **跳过-无关** | 改了我方独有模块、上游 demo、上游文档、CI 配置 | 不合入 |
| 🟠 **待人工** | 改动复杂、夹杂多类内容、或不确定 | 标记后由用户决定 |
| 🟡 **裁剪合入** | 大体可合入，但需要排除某些文件/hunk | 合入时需手工选 hunk |
| ✅ **直接合入** | 纯 bug fix / 新功能，文件路径与我方无冲突 | cherry-pick 即可 |

### 4.2 自动分类规则（按优先级从上到下应用）

**规则 1 → 🔴 跳过-冲突**（命中任一即停）

commit 改动包含以下任一文件/路径：
- `pyproject.toml` / `setup.py` / `setup.cfg`（包名相关）
- `README.md` / `README_zh.md` / `LICENSE` / `CONTRIBUTING*.md`
- `src/qwenpaw/**`（上游用旧路径，我方已是 `src/wowooai/`，路径冲突）
- 任何含有"qwenpaw" / "QwenPaw" 字样的重命名 commit（看 commit message 与 diff）
- `src/wowooai/constant.py` 中 `BUILTIN_QA_AGENT_*` 相关行（我方已改入职小助手）
- `src/wowooai/agents/templates.py` 中 `QA_TEMPLATE_DESCRIPTION` 段落
- `src/wowooai/config/config.py` 中 `build_qa_agent_tools_config` 段落
- `src/wowooai/agents/md_files/qa/**`（我方已替换）
- `src/wowooai/agents/skills/{guidance,QA_source_index}-*/**`（我方已废弃）

**规则 2 → ⚪ 跳过-无关**（命中任一即停）

commit 改动**全部**位于以下路径：
- `docs/**`（除非是修代码的同时改文档）
- `website/**`
- `tests/**`（可选，但通常我方测试结构不同）
- `.github/**` / `.gitlab/**`（CI 配置）
- `examples/**` / `demo/**`
- `Makefile`（如果只是改打包目标）

或者 commit message 含明显跳过信号：
- `docs:` / `chore:` / `style:` / `ci:` / `test:` 前缀且改动 < 20 行
- "release"、"bump version"、"changelog"

**规则 3 → 🟡 裁剪合入**（命中任一即标记）

- commit 同时改动了"应合入"和"应跳过"的文件
- commit 改了 `src/wowooai/agents/tools/__init__.py`（工具注册中心，我方加了 renliwo_browser，需手工合并）
- commit 改了 `console/src/locales/{zh,en,ru}.json`（我方已大量定制中文翻译，要逐条比）

**规则 4 → 🟠 待人工**

- commit 同时影响 5 个以上文件且涉及核心模块（react_agent / multi_agent_manager / workspace）
- commit message 含 `BREAKING CHANGE` / `refactor!:`
- commit 改了 `src/wowooai/agents/skills_manager.py`（我方独有的 onboarding-guide 注册路径）

**规则 5 → ✅ 直接合入**（默认）

不命中以上任何规则，且：
- 是 `fix:` / `feat:` / `perf:` 前缀
- 改动局限于：MCP 子系统、channel、memory、cron、agent_browser、browser_visible、browser_cdp、desktop_*、file_io 等通用工具
- 改动行数 < 200 行

### 4.3 操作步骤

对 `_raw_commits.tsv` 中每一条 commit：

1. 读取 commit hash、日期、作者、subject
2. 跑 `git show --stat <SHA>` 看动了哪些文件
3. 按上述规则匹配，得出标签
4. 必要时跑 `git show <SHA> -- <文件>` 看具体 diff，决定是否升级到 🟠
5. 写一行到追踪表，**附简短理由**

### 4.4 边界与降级处理

- 若某 commit 文件路径同时命中"我方独有模块"与"通用 bug fix"：标记 🟡，备注哪些 hunk 可保留
- 若 commit 是 merge commit（`%P` 有两个 parent）：通常 fetch 时已被 `--no-merges` 过滤；如有遗漏，跳过
- 若 commit message 完全无法判断（如 `update`、`fix bug`、`修复`）：标记 🟠，备注 `commit message 不清晰`

---

## 5. 阶段 4：生成交付文档

输出位置：`docs/changelog/upstream-sync/`

### 5.1 生成 [README.md](docs/changelog/upstream-sync/README.md)

包含：
- 同步起止区间（基线 SHA、上游 HEAD SHA、抓取日期）
- commit 总数、各标签数量统计
- 高频改动文件 top 20（取自 `_raw_hotspots.txt`）
- 文件使用说明：合并者从 `commits.md` 开始，按 ✅ → 🟡 → 🟠 顺序处理

模板：

```markdown
# QwenPaw 上游同步追踪

## 概况
- 我方基线：`283293f1` (2026-04-29)
- 上游 HEAD：`<HEAD_SHA>` (`<HEAD_DATE>`)
- 抓取日期：`<TODAY>`
- 上游分支：`upstream/<branch>`
- 新 commit 总数：`<N>`

## 分类统计
| 标签 | 数量 | 含义 |
|---|---|---|
| ✅ 直接合入 | xx | bug fix / 新功能，无冲突 |
| 🟡 裁剪合入 | xx | 部分 hunk 可合 |
| 🟠 待人工 | xx | 需要用户决策 |
| ⚪ 跳过-无关 | xx | 文档/CI/demo |
| 🔴 跳过-冲突 | xx | 与我方品牌化/重写冲突 |

## 高频改动文件 (top 20)
（取自 _raw_hotspots.txt）

## 处理建议顺序
1. 先看 [commits.md](commits.md) ✅ 标签 commit，逐条 cherry-pick
2. 再处理 🟡，每条单独 review hunk
3. 最后和用户讨论 🟠
4. 🔴 / ⚪ 永久跳过，记录在表里即可

## 二次同步指引
完成本轮 cherry-pick 后，将 [README.md](README.md) 顶部的"我方基线"
更新为最后 pick 的上游 SHA，下次只需对比新增 commit。
```

### 5.2 生成 [commits.md](docs/changelog/upstream-sync/commits.md)（核心交付物）

按上游时间正序排列。每个 commit 一段：

```markdown
## [N] `<short_sha>` <subject>

- **完整 SHA**：`<full_sha>`
- **日期**：`YYYY-MM-DD`
- **作者**：`<name>`
- **改动文件数**：`<count>`，新增 `+X` / 删除 `-Y` 行
- **标签**：`<emoji 标签>`
- **理由**：`<一句话说明命中了哪条规则>`
- **改动文件列表**：
  ```
  M   src/...
  A   src/...
  D   src/...
  ```
- **建议操作**：
  - ✅ → `git cherry-pick <full_sha>`
  - 🟡 → `git cherry-pick -n <full_sha>`，然后 `git reset HEAD <要排除的文件>` && `git checkout -- <要排除的文件>`，再 `git commit`
  - 🟠 → 暂不处理，等用户决策
  - ⚪ / 🔴 → 跳过，无需操作

---
```

> 若 commit 数 > 50，按 50 一批切到 `commits-batch-01.md`、`-02.md`…，并在 README 索引。

### 5.3 生成 [decisions.md](docs/changelog/upstream-sync/decisions.md)（用户决策表）

只列 🟠 待人工 的 commit，让用户能在一个文件内集中决策：

```markdown
# 待人工决策清单

> 处理完后请把决策结果填入 `决策` 列，并把 commit 同步到 [commits.md](commits.md)。

| # | SHA | 标题 | 改动概览 | 待决策原因 | 决策（用户填） |
|---|---|---|---|---|---|
| 1 | abc1234 | refactor!: rename foo | ... | BREAKING change | ⬜ 合入 / ⬜ 跳过 / ⬜ 部分合入 |
| ... | | | | | |
```

### 5.4 生成 [SYNC_PLAYBOOK.md](docs/changelog/upstream-sync/SYNC_PLAYBOOK.md)（合并执行手册）

留给"下一个 AI"做实际 cherry-pick 时用，内容包括：

- 如何按 [commits.md](commits.md) 标签批量处理
- 冲突解决标准做法（品牌化 sed 命令、import 路径修正）
- commit message 规范：`sync(qwenpaw): <short_sha> — <原 subject>`
- 推送前 smoke test 列表
- 失败回滚命令：`git cherry-pick --abort` / `git reset --hard ORIG_HEAD`

模板内容（直接照抄）：

```markdown
# 上游同步执行手册（cherry-pick 阶段）

## 执行前置
1. 工作区干净：`git status` 无未提交改动
2. 已读完 [commits.md](commits.md) 与 [decisions.md](decisions.md)
3. 用户已对 🟠 标签做出决策

## 批量执行流程

### 第一批：✅ 直接合入
```bash
# 从 commits.md 提取所有 ✅ 标签的 SHA，逐条 pick
for SHA in <sha1> <sha2> ...; do
  git cherry-pick -x $SHA
  if [ $? -ne 0 ]; then
    echo "冲突在 $SHA，停止批量处理"
    break
  fi
done
```

`-x` 让 cherry-pick 自动在 commit message 加 `(cherry picked from commit <sha>)` 留痕。

### 冲突解决标准做法
1. **import 路径冲突**（`qwenpaw` → `wowooai`）：
   ```bash
   # 在冲突文件上跑
   sed -i '' 's/from qwenpaw/from wowooai/g; s/import qwenpaw/import wowooai/g' <file>
   ```
2. **`tools/__init__.py` 的注册表冲突**：保留我方 `renliwo_browser` 注册行，再追加上游新加的工具
3. **`locales/zh.json` 的翻译冲突**：保留我方"数字员工"等术语，逐 key diff

### 第二批：🟡 裁剪合入
```bash
git cherry-pick -n <sha>
git status  # 看动了哪些文件
git checkout HEAD -- <要排除的文件>   # 还原不要的改动
git diff --staged                     # 确认剩下的是我们要的
git commit -c <sha>                   # 用上游 commit message
```

### 第三批：🟠 用户已决策的
按用户在 decisions.md 的填写处理。

## Smoke test
推送前最少跑：
- 后端启动：`/Users/rlw/AI项目/wowooai/client/bundled-venv/bin/python3 -m wowooai app --host 127.0.0.1 --port 8088`
- 前端启动：`cd console && pnpm dev --host --port 5174`
- 创建一个测试 Agent
- 发一条对话
- 切换到入职小助手 Agent，问"公司WiFi密码"，验证 onboarding-guide 技能仍工作

## 回滚
- 当前 cherry-pick 中冲突想放弃：`git cherry-pick --abort`
- 已 commit 但发现错误（最近 1 个）：`git reset --hard HEAD~1`
- 已 commit 多个想全部撤回到同步前：`git reset --hard <同步前 SHA>`
  （建议同步开始前打个 tag：`git tag pre-qwenpaw-sync-2026-05-14`）

## 完成后
1. 推送：`git push origin main`
2. 更新 [README.md](README.md) 的"我方基线"为最后 pick 的上游 SHA
3. 给用户一份 cherry-pick 总结（多少个 ✅ 成功、多少 🟡 裁剪、多少跳过）
```

### 5.5 清理中间文件（可选）

`_raw_*` 文件可保留，方便审计。如要精简：

```bash
# 不删，作为审计材料保留在 docs/changelog/upstream-sync/ 下
```

---

## 6. 阶段 5：自检与汇报

执行完阶段 1-4 后，AI 必须做以下自检：

```bash
# 1. 工作区无变化
git status   # 应只有 docs/changelog/upstream-sync/ 下的新文件

# 2. 没有意外的代码改动
git diff --stat   # 应为空（追踪文件还没 add）

# 3. 没有任何 cherry-pick / merge / rebase 残留
ls .git/CHERRY_PICK_HEAD .git/MERGE_HEAD .git/rebase-* 2>/dev/null
# 应全部 "No such file or directory"

# 4. upstream 推送仍被禁
git remote -v | grep "upstream.*DISABLED"   # 应有一行匹配
```

**最终向用户汇报内容**（控制台输出，不写文件）：

```
✅ 同步分析完成

📊 总览
- 上游新 commit：N 个
- 直接合入：N1 / 裁剪合入：N2 / 待人工：N3 / 跳过：N4

📁 输出文件
- docs/changelog/upstream-sync/README.md            （总览）
- docs/changelog/upstream-sync/commits.md           （逐 commit 决策表）
- docs/changelog/upstream-sync/decisions.md         （待人工裁定项）
- docs/changelog/upstream-sync/SYNC_PLAYBOOK.md     （后续执行手册）

🔜 用户下一步
1. 打开 decisions.md，对 N3 个 🟠 commit 做决策
2. 决策后通知 AI 进入阶段 6（实际 cherry-pick），按 SYNC_PLAYBOOK.md 执行
```

---

## 7. 严格禁止清单（红线）

以下操作**禁止执行**，违反即视为任务失败：

- ❌ `git cherry-pick`、`git merge`、`git rebase`、`git pull`
- ❌ `git push`（任何 remote）
- ❌ `git reset --hard` / `git checkout <branch>`
- ❌ 修改 `src/`、`console/`、`scripts/`、`pyproject.toml` 等任何源码与配置
- ❌ 删除 `.git/objects` 或修改任何已存在的 git 对象
- ❌ 修改 origin 的 URL 或推送配置
- ❌ 添加或删除 origin 之外的 push 通道

允许的操作：
- ✅ `git remote add upstream` / `git fetch upstream`
- ✅ `git log` / `git show` / `git diff`（只读）
- ✅ 在 `docs/changelog/upstream-sync/` 下新建文件
- ✅ TodoWrite 跟踪进度

---

## 8. 异常情况快速指引

| 情况 | 处理 |
|---|---|
| `git fetch` 网络失败 | 重试 1 次，仍失败则在 README.md 顶部记录"❌ 阶段 1 失败：<原因>"并退出 |
| 上游主分支不是 `main` | 用 `git remote show upstream` 查到的 HEAD branch 替换全文 `upstream/main` |
| 基线 SHA 在 fetch 后仍 not found | 上游可能 force-push，记录后退出，不强行假设 |
| commit 数 0 | 只生成 README.md 写明"上游无新提交"，跳过 commits.md |
| commit 数 > 200 | 按 50 切批，文件名 `commits-batch-01.md` 起 |
| 某 commit 看不出标签 | 标 🟠，理由写"自动规则未命中，需人工" |
| 某文件路径既在我方独有列表又在通用 fix 列表 | 标 🟡，备注两边的 hunk |

---

## 9. 完成标志

任务完成的判定标准（全部满足）：

- [ ] `git remote -v` 显示 upstream 已添加且 push 为 DISABLED
- [ ] `git cat-file -t 283293f1ae4e6c5dcb8d3e866415bb6b8e870d37` 输出 `commit`
- [ ] `docs/changelog/upstream-sync/README.md` 存在且填充完整
- [ ] `docs/changelog/upstream-sync/commits.md`（或分批文件）存在，每个 commit 都有标签与理由
- [ ] `docs/changelog/upstream-sync/decisions.md` 存在（即使 🟠 数量为 0 也写一个空表）
- [ ] `docs/changelog/upstream-sync/SYNC_PLAYBOOK.md` 存在
- [ ] `git status` 显示只有 `docs/changelog/upstream-sync/` 下的新增 untracked 文件
- [ ] `git diff --stat` 为空
- [ ] 没有 `.git/CHERRY_PICK_HEAD` 等过程残留

---

## 10. 给执行者的最后提醒

- 本手册是**完整自包含**的，不要询问用户任何问题（除非阶段 5 自检失败）
- 输出文档面向**人类阅读**，文字尽量精简清晰，emoji 标签必须统一
- 如果某条规则与现实情况冲突，**以现实为准并在文档中注明**——不要为了对齐规则而误标
- 完成后用一段简短中文向用户汇报，列出关键数字与下一步动作
- 不要在控制台粘贴大段 commit 列表——结果在 markdown 里，控制台只放摘要
