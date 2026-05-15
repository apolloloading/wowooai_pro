# 24 — 备份与恢复

> 版本：0.0.1
> 对应代码：[src/wowooai/backup/](../../src/wowooai/backup/) · [src/wowooai/app/routers/backup.py](../../src/wowooai/app/routers/backup.py)

## 1. 定位

把数字员工的**配置 + 工作区 + 全局设置**打包成单个 zip / tar，便于：

- 换机器迁移（macOS ↔ Windows ↔ 同台不同 user）
- 重要状态前存档
- 排错时回滚

**不是**消息历史的备份系统（dialog log 在 workspace 里，备份会一并带走）。
**不**自动定时备份 —— 用户主动触发。

## 2. 备份范围（BackupScope）

[backup/models.py:13](../../src/wowooai/backup/models.py#L13)

| 字段 | 默认 | 含义 |
|---|---|---|
| `include_agents` | True | workspace 目录（含 sessions / dialog / memory / sandbox / skills 等） |
| `include_global_config` | True | `~/.wowooai/config.json` |
| `include_secrets` | **False** | secrets 目录（API keys / channel tokens） |
| `include_skill_pool` | True | `~/.wowooai/skill_pool/` |

`include_secrets=False` 是默认 — **凭据不进备份**，避免备份文件外泄变成凭据外泄。需要带凭据迁移时用户显式打开开关。

## 3. BackupMeta

```python
{
  "id": "wowooai-{version}-{timestamp}-{short8}",
  "name": "用户起的名字",
  "description": "可选",
  "created_at": ISO8601,
  "version": "1",                 # 备份格式版本（用于兼容）
  "scope": BackupScope,
  "agent_count": int,
  "wowooai_version": "0.0.1",
  "system_info": { "os": ..., "python": ... }
}
```

## 4. API

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/api/backup/list` | 列出全部备份 |
| `GET` | `/api/backup/<id>` | 详情（BackupDetail） |
| `POST` | `/api/backup/create` | 创建备份（SSE 进度） |
| `POST` | `/api/backup/restore` | 恢复备份（SSE 进度） |
| `POST` | `/api/backup/delete` | 批量删除 |
| `GET` | `/api/backup/<id>/download` | 下载备份 zip |
| `POST` | `/api/backup/upload` | 上传外部备份 zip |

create / restore 走 SSE（详见 [18-streaming.md](18-streaming.md)），实时推进度（"打包 agent X / 解压中 / ..."）。

## 5. 创建流程

[backup/_ops/create.py](../../src/wowooai/backup/_ops/create.py)

1. 写 `BackupMeta` 到临时目录；
2. 按 scope 复制：
   - `include_global_config` → 复制 `config.json`（**移除** `providers.json` 引用如果 `include_secrets=False`）；
   - `include_agents` → 选定的 agent IDs 对应 workspace 整体打包；
   - `include_skill_pool` → `skill_pool/` 全量；
   - `include_secrets` → secrets 文件（仅在显式开启时）；
3. 压缩为 `<id>.zip`；
4. 落 `~/.wowooai/backups/<id>.zip`；
5. SSE 推 `done` 事件。

## 6. 恢复流程

[backup/_ops/restore.py](../../src/wowooai/backup/_ops/restore.py) + [_utils/safe_swap.py](../../src/wowooai/backup/_utils/safe_swap.py)

1. 解压到临时目录；
2. 校验 `BackupMeta.version` —— 不兼容直接报错；
3. 按 `RestoreBackupRequest` 选择恢复哪些部分；
4. 用 `safe_swap` 原子替换：
   - 旧目录改名为 `<name>.bak.<ts>`；
   - 新目录就位；
   - 失败 → 还原旧目录，不留半截状态；
5. 触发 `_preload_agents_background` 异步把恢复后的 agents 加载到 `MultiAgentManager`；
6. SSE 推 `done`。

## 7. 冲突处理

[backup/models.py:127 `BackupConflictError`](../../src/wowooai/backup/models.py#L127)：恢复时若现有 agent ID 与备份内冲突，要求用户显式选 `overwrite` / `skip` / `rename`。

## 8. 上传外部备份

`POST /api/backup/upload` 让用户从其��机器拷贝来的 zip 注册到本机备份列表。校验：

- 是有效 zip；
- 含合法的 `BackupMeta`；
- `wowooai_version` 与当前接近（major / minor 一致即可，否则警告但不阻止）。

## 9. 凭据隐私（绝对约束）

- 备份文件可能包含**用户私有数据**（对话、文件、记忆）—— 仅本地存储，不上传任何云。
- `include_secrets=False` 是默认，避免误把 API key 写入备份。
- 备份 zip 不加密 —— 由 OS 文件系统权限保护；用户跨设备传输时**应自行加密**（如 zip 加密 / 通过 EE2E 通道）。
- 仓库**严禁**包含任何样本备份文件。

## 10. 0.0.1 不做

- 不做自动定时备份（用户主动触发）。
- 不做备份增量 / 差异（每次全量打包）。
- 不做备份加密（用户机器内信任 OS 文件系统）。
- 不做云端备份（不传 OSS / S3 / GitHub）。
- 不做备份保留策略（不自动清理；用户手动 delete）。
- 不做备份 → 备份的迁移工具（仅当前 v=1 格式）。
