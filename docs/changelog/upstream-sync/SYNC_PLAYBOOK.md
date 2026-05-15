# 上游同步执行手册（cherry-pick 阶段）

## 执行前置
1. 工作区干净：`git status` 无未提交改动
2. 已读完 [commits.md](commits.md)、各批次文档与 [decisions.md](decisions.md)
3. 用户已对 🟠 标签做出决策

## 批量执行流程

### 第一批：✅ 直接合入
```bash
# 从批次文档提取所有 ✅ 标签的 SHA，逐条 pick
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
3. **`locales/zh.json` 的翻译冲突**：保留我方“数字员工”等术语，逐 key diff

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
- 切换到入职小助手 Agent，问“公司WiFi密码”，验证 onboarding-guide 技能仍工作

## 回滚
- 当前 cherry-pick 中冲突想放弃：`git cherry-pick --abort`
- 已 commit 但发现错误（最近 1 个）：`git reset --hard HEAD~1`
- 已 commit 多个想全部撤回到同步前：`git reset --hard <同步前 SHA>`
  （建议同步开始前打个 tag：`git tag pre-qwenpaw-sync-2026-05-14`）

## 完成后
1. 推送：`git push origin main`
2. 更新 [README.md](README.md) 的“我方基线”为最后 pick 的上游 SHA
3. 给用户一份 cherry-pick 总结（多少个 ✅ 成功、多少 🟡 裁剪、多少跳过）
