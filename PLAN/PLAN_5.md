# PLAN_5 — B3：下载与下载管理器

> 会话 S4 · 440 条字符串 + 13 组复数（26 项）· 前置：PLAN_2
> **全项目最大的一批，建议单独占用一个对话，不要再塞别的工作。**
> 内部拆成 5 个块，每块完成后都可以停手，下次从断点续。

---

## 1. 目标（可验证）

1. 下载设置页（并发、分片、限速、计划下载、保存位置、日志）全部中文。
2. 下载管理器（列表、分组、筛选、排序、多选、空状态）全部中文。
3. 下载过程中的状态、通知、重试、错误提示全部中文，且术语一致。
4. MEGA 链接导入流程（选择文件、目录、暂停策略）全部中文。
5. `i18n_scope.py B3 --stat` = 440/440。

---

## 2. 分块（务必按块提交，避免一次写 440 条）

| 块 | 范围（二级前缀） | 条数 | 主要界面 |
|---|---|---|---|
| C1 | `download_settings` `download_schedule` `download_location` `download_manager` `download_speed` `download_manual` `download_update` `download_log` `download_history` `download_categorize` `download_metered` `download_unmetered` `download_foreground` `download_quick` `download_keep` `download_ignore` `download_setting` `download_resumable` `download_multithreading` `download_split` | **97** | 设置 → 下载（全部子页） |
| C2 | `download_dialog` `download_props` `download_error` `download_storage` `download_grant` `download_change` `download_rename` `download_conflict` `download_duplicate` `download_already` `download_detect` `download_more` | **114** | 下载对话框、文件属性、全部错误提示 |
| C3 | `download_status` `download_section` `download_retry` `download_menu` `download_notification` `download_stage` `download_eta` `download_total` `download_event` `download_push` `download_pause` `download_resume` `download_started` `download_added` `download_file` `download_info` `download_copying` `download_deleting` `download_response` `download_icon` `download_multi` `download_paused` `download_concurrent` | **110** | 进度、通知栏、重试、长按菜单 |
| C4 | `downloads_*` 全部（sheet/group/type/sort/filter/select/empty…） | **93** | 下载管理器整页 |
| C5 | `mega_*`（21）+ `redownload_*`（5） | **26** | MEGA 链接导入、重新下载确认 |
| | | **440** | |

---

## 3. 特殊条目

### 3.1 复数（13 组，中文只写 other）

| key | 英文 other | 建议中文 |
|---|---|---|
| `downloads_pulse_active` | %1$d active | 活跃 %1$d 项 |
| `downloads_pulse_queued` | %1$d queued | 排队 %1$d 项 |
| `downloads_setting_connections` | %1$d connections | %1$d 个连接 |
| `downloads_library_summary` | %1$d files · %2$s | %1$d 个文件 · %2$s |
| `downloads_meta_pages` | %1$d pages | %1$d 页 |
| `download_notification_group_summary` | %1$d downloads in progress | 正在下载 %1$d 项 |
| `download_concurrent_value` | %1$d simultaneous downloads | 同时下载 %1$d 项 |
| `download_split_parts_value` | %1$d parts | %1$d 个分片 |
| `download_multithreading_value` | up to %1$d parts at a time | 每次最多 %1$d 个分片 |
| `download_concurrent_segments_value` | up to %1$d segments at a time | 每次最多 %1$d 个分段 |
| `mega_folder_file_count` | %1$d files · %2$s | %1$d 个文件 · %2$s |
| `mega_folder_started` | Downloading %d files | 正在下载 %1$d 个文件 |
| `mega_folder_added_paused` | Added %d files to Downloads, paused | 已将 %1$d 个文件添加到下载并暂停 |

> 后两条在 PLAN_2 里已从 `%d` 重构为 `%1$d`，直接写位置参数。

### 3.2 转义与格式（本批最密集，务必逐条看）

| key | 源文特征 | 处理 |
|---|---|---|
| `download_status_progress` | `%1$d%%  ·  %2$s / %3$s` | **`%%` 是字面百分号**，必须保留；三个参数顺序保留 |
| `download_status_progress_unknown_total` | `%1$d%%  ·  %2$s / ?` | 同上 |
| `download_info_with_time` | `%1$s  ·  %2$s` | 中间是 `\u2022` 圆点，不是普通空格 |
| `download_error_storage_direct` | `…\n\nRequired: %1$s\nAvailable: %2$s` | 三处换行全保留；建议「所需：%1$s\n可用：%2$s」 |
| `download_error_storage_emulated` | 含括号说明 + `%1$s` `%2$s` | 括号用全角，换行保留 |
| `download_error_storage_temp` | 同上 | 同上 |
| `download_error_storage_dest` | 同上 | 同上 |
| `download_error_fat32_message` | 含 `\'`、`\n\n`、`%1$s` | 中文不含撇号；换行保留 |
| `download_dialog_file_size_fetching` | `File Size: Fetching\u2026` | 「文件大小：正在获取\u2026」 |
| `download_props_computing` | `Computing\u2026` | 「正在计算\u2026」 |
| `download_props_dash` | `\u2014` | 保留破折号 `\u2014` |
| `download_notification_retrying_in` | `Retrying in %1$ds\u2026` | 「%1$s 秒后重试\u2026」（`s` 是秒，可保留字母或改「秒」） |
| `download_concurrent_value_easter_egg` | `24 simultaneous downloads \uD83D\uDE08` | 彩蛋文案，保留 emoji 转义 |

### 3.3 长文本
本批无 >200 字符条目，但 `download_error_*` 25 条彼此相似，**必须成组对照译**，否则会出现「空间不足」「存储空间不够」两种说法。

---

## 4. 术语（本批最需要锁定）

| 英文 | 中文 | 说明 |
|---|---|---|
| Download | 下载 | |
| Download Manager | 下载管理器 | |
| Queue | 队列 | 排队 |
| Concurrent / Simultaneous | 并发 / 同时 | 设置项「并发下载数」 |
| Connection | 连接 | 连接数 |
| Segment | 分段 / 分片 | `download_split_parts` = 分片；`concurrent_segments` = 分段；全批统一「分片」优先 |
| Part | 分片 | |
| Resume | 续传 | 断点续传 |
| Retry | 重试 | |
| ETA | 剩余时间 | 不写 ETA |
| Speed | 速度 | |
| Metered network | 计费网络 | 设置项里说明为「移动数据等计费网络」 |
| Foreground service | 前台服务 | 一般不直接暴露给用户 |
| Category | 分类 | 下载分类（图片/视频/文档…） |
| Conflict | 冲突 | 同名文件冲突 |
| Duplicate | 重复 | 重复下载 |
| Save path | 保存路径 | 不写「存储路径」 |
| Properties | 属性 | |

---

## 5. 参考译法

| key | 英文 | 建议 |
|---|---|---|
| `download_settings_title` | Downloads | 下载 |
| `download_props_label_path` | Save path | 保存路径 |
| `download_concurrent_segments_title` | Concurrent Segments | 并发分段数 |
| `downloads_action_pause` | Pause | 暂停 |
| `downloads_pulse_live` | Live speed | 实时速度 |
| `download_stage_audio` | Downloading audio | 正在下载音频 |
| `download_schedule_end_title` | End time | 结束时间 |
| `download_schedule_past_time_error` | Pick a date and time in the future | 请选择将来的日期和时间 |
| `download_update_link_dialog_size_unverifiable` | File size could not be verified | 无法验证文件大小 |
| `download_log_share_title` | Share download log | 分享下载日志 |
| `download_history_incognito_title` | Save Incognito download history | 保存无痕模式下载记录 |
| `download_storage_permission_denied_message` | Downloads can't be saved… | 没有存储权限，无法保存到「下载」文件夹… |

---

## 6. 操作步骤（按块推进）

```bash
python tests/i18n_scope.py B3 --missing > .tmp_b3.txt
wc -l .tmp_b3.txt          # 440
```

1. **C1（97）**：设置类，句式统一「标题 + 描述」，描述不加句号。
2. **C2（114）**：错误提示必须成组对照；先译 25 条 `download_error_*`，再译 `download_props_*`。
3. **C3（110）**：状态与通知，注意 `%%` 与 `\u2026`。
4. **C4（93）**：列表 UI，多选、排序、筛选词要短（「名称」「大小」「日期」「类型」）。
5. **C5（26）**：MEGA 与重新下载。
6. 每块结束：`check_i18n.py --locale zh --allow-missing`。

---

## 7. 校验

```bash
python tests/i18n_scope.py B3 --stat        # 440/440
python tests/check_i18n.py --locale zh --allow-missing
```

---

## 8. 完成判据

- [ ] `i18n_scope.py B3 --stat` = 440/440（+ 13 组复数）
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL
- [ ] 提交：`i18n(zh): downloads and download manager`

---

## 9. 本批独有的坑

| 坑 | 说明 |
|---|---|
| 把 `%%` 写成 `%` | 编译能过，运行时抛 `UnknownFormatConversionException`，且只有下载中才崩，极难排查 |
| 把 `\u2026` 换成半角 `...` | 观感廉价；统一 `\u2026` |
| `download_error_*` 逐条独立翻译 | 必然出现五种「空间不足」说法；必须成组译 |
| `segments` 与 `parts` 混译 | 一个界面里同时出现「分段」和「分片」会让人以为是两回事 |
| 通知标题过长 | 中文虽短，但 `download_notification_*` 里有的带文件名，注意别再加前缀 |

---

## 10. 交接

- 下一步：`PLAN_6.md`（B4 标签页 186 + B8 备份/关于 194）。
- 若本批只完成部分块，在台账记录「B3-C1/C2 完成」，下次从 C3 继续，不要重头来。
