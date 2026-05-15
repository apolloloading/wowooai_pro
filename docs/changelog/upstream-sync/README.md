# QwenPaw 上游同步追踪

## 概况
- 我方基线：`283293f1` (2026-04-29)
- 上游 HEAD：`00ede853fac401296c58a49ec782b907e2e1d882` (`2026-05-14`)
- 抓取日期：`2026-05-14`
- 上游分支：`upstream/main`
- 新 commit 总数：`130`

## 分类统计
| 标签 | 数量 | 含义 |
|---|---:|---|
| ✅ 直接合入 | 15 | bug fix / 新功能，无冲突 |
| 🟡 裁剪合入 | 2 | 部分 hunk 可合 |
| 🟠 待人工 | 10 | 需要用户决策 |
| ⚪ 跳过-无关 | 5 | 文档/CI/demo |
| 🔴 跳过-冲突 | 98 | 与我方品牌化/重写冲突 |

## 高频改动文件 (top 20)

```text
  18 console/src/locales/zh.json
  18 console/src/locales/ru.json
  18 console/src/locales/ja.json
  18 console/src/locales/en.json
  13 console/src/locales/pt-BR.json
  11 src/qwenpaw/config/config.py
  10 src/qwenpaw/__version__.py
   8 src/qwenpaw/agents/react_agent.py
   8 console/src/pages/Control/Channels/components/ChannelDrawer.tsx
   6 src/qwenpaw/app/runner/runner.py
   6 src/qwenpaw/app/channels/wecom/channel.py
   5 src/qwenpaw/providers/provider_manager.py
   5 src/qwenpaw/app/_app.py
   5 console/src/pages/Chat/index.tsx
   5 console/src/layouts/index.module.less
   5 console/src/layouts/Sidebar.tsx
   4 src/qwenpaw/providers/anthropic_provider.py
   4 src/qwenpaw/plugins/registry.py
   4 src/qwenpaw/cli/skills_cmd.py
   4 src/qwenpaw/app/routers/skills.py
```

## 文件索引
- [commits.md](commits.md)：批次索引
- [commits-batch-01.md](commits-batch-01.md)：逐 commit 分类表
- [commits-batch-02.md](commits-batch-02.md)：逐 commit 分类表
- [commits-batch-03.md](commits-batch-03.md)：逐 commit 分类表
- [merge-priority.md](merge-priority.md)：按合入优先级汇总，推荐先从这里判断要不要合
- [impact-index.md](impact-index.md)：按模块查看影响范围
- [impact-batch-01.md](impact-batch-01.md)：逐 commit 代码影响分析
- [impact-batch-02.md](impact-batch-02.md)：逐 commit 代码影响分析
- [impact-batch-03.md](impact-batch-03.md)：逐 commit 代码影响分析
- [impact-batch-04.md](impact-batch-04.md)：逐 commit 代码影响分析
- [impact-batch-05.md](impact-batch-05.md)：逐 commit 代码影响分析
- [impact-batch-06.md](impact-batch-06.md)：逐 commit 代码影响分析
- [review-batch-01.md](review-batch-01.md)：逐 commit 深度评估
- [review-batch-02.md](review-batch-02.md)：逐 commit 深度评估
- [review-batch-03.md](review-batch-03.md)：逐 commit 深度评估
- [decisions.md](decisions.md)：待人工裁定项
- [SYNC_PLAYBOOK.md](SYNC_PLAYBOOK.md)：后续 cherry-pick 执行手册

## 处理建议顺序
1. 先看 [impact-index.md](impact-index.md) 或 [merge-priority.md](merge-priority.md)，确认关心模块和优先级
2. 再处理 🟡，每条单独 review hunk
3. 最后和用户讨论 🟠
4. 🔴 / ⚪ 永久跳过，记录在表里即可

## 二次同步指引
完成本轮 cherry-pick 后，将本文件顶部的“我方基线”更新为最后 pick 的上游 SHA，下次只需对比新增 commit。
