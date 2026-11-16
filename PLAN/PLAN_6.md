# PLAN_6 — B4 标签页/书签/历史 + B8 备份/关于/引导

> 会话 S5 · 186 + 194 = 380 条字符串 · 前置：PLAN_3（B1 已锁定通用词）
> 两批风格差异大：B4 是高频交互文案，B8 是长文本与法律文本。建议先 B4 后 B8。

---

# 第一部分：B4（186 条 + 4 组复数）

## 1. 目标

1. 标签页：标签组（新建/重命名/配色/拖动）、标签条、多选菜单全部中文。
2. 书签：新建、文件夹、移动、排序、导入导出、格式名全部中文。
3. 历史：清空、排序、多选、空状态全部中文。
4. 主页：布局、壁纸、搜索框样式、快捷图标全部中文。
5. `i18n_scope.py B4 --stat` = 186/186。

## 2. 分块

| 块 | 前缀 | 条数 | 界面 |
|---|---|---|---|
| B4-C1 | `tab_group` 31 · `tab_menu` 14 · `tab_bar` 4 · `tab_strip` 3 · `tab_selection` 2 · `tab_mute` `tab_unmute` 2 | **56** | 标签组、标签条、标签菜单 |
| B4-C2 | `bookmarks_*` 40 · `history_*` 28 | **68** | 书签页、历史页 |
| B4-C3 | `homepage_*` 30 · `incognito_*` 11 · `nested_*` 8 · `delete_inactive_*` 6 · `tabs_*` 3 · `new_*` 2 · `strip_*` 2 | **62** | 主页定制、无痕、嵌套滚动、清理闲置标签 |

## 3. 特殊条目

### 3.1 复数（4 组）

| key | 英文 other | 建议 |
|---|---|---|
| `tab_menu_tab_count` | %1$d tabs | %1$d 个标签页 |
| `tab_menu_selected_count` | %1$d selected | 已选择 %1$d 个 |
| `tab_menu_closed_tabs` | Closed %1$d tabs | 已关闭 %1$d 个标签页 |
| `tab_menu_closed_duplicates` | Closed %1$d duplicate tabs | 已关闭 %1$d 个重复标签页 |

### 3.2 非位置占位符（已在 PLAN_2 重构为 `%1$d`）

| key | 英文 | 建议 |
|---|---|---|
| `bookmarks_selected_count` | %d selected | 已选择 %1$d 项 |
| `bookmarks_delete_confirm_message` | Delete %d bookmark(s)? | 删除 %1$d 个书签？ |
| `bookmarks_delete_confirm_message_folders` | Delete %d item(s)? … | 删除 %1$d 项？所选文件夹内的书签和文件夹也会一并删除。 |
| `bookmarks_folder_item_count` | %d items | %1$d 项 |
| `bookmarks_import_success` | Imported %d bookmarks | 已导入 %1$d 个书签 |
| `history_selected_count` | %d selected | 已选择 %1$d 项 |
| `history_delete_confirm_message` | Remove %d item(s) from history? | 从历史记录中移除 %1$d 项？ |

> 注意：中文没有单复数，原文的 `(s)` 不要照搬成「书签(s)」。

### 3.3 其他
- `bookmarks_format_sqlite` = `SQLite Database` → 「SQLite 数据库」，保留产品名
- `bookmarks_sort_by_date_added` = `Date Added` → 「添加日期」
- 全大写英文（如 `No` / `New`）按正常中文写，不模拟大写

## 4. 术语

| 英文 | 中文 |
|---|---|
| Tab group | 标签组 |
| Tab strip | 标签条 |
| Nested scroll | 嵌套滚动 |
| Both | 两者 |
| Inactive tabs | 闲置标签页 |
| Bookmark / Folder | 书签 / 文件夹 |
| Move | 移动 |
| Import / Export | 导入 / 导出 |
| Sort by | 排序方式 |
| Clear all | 全部清空 |
| Incognito Mode | 无痕模式 |
| Homepage | 主页 |
| Favorites（主页图标） | 常用网站 |

## 5. 参考译法

| key | 英文 | 建议 |
|---|---|---|
| `tab_strip_add_to_new_group` | Add to New Group | 添加到新标签组 |
| `tab_menu_close_all_tabs` | Close All Tabs | 关闭全部标签页 |
| `tab_group_bar_open_desc` | Show %1$s in the tab switcher | 在标签页切换器中显示 %1$s |
| `history_clear_all` | Clear all | 全部清空 |
| `bookmarks_add_fab_desc` | Add bookmark or folder | 添加书签或文件夹 |
| `homepage_search_engine` | Search Engine Homepage | 搜索引擎主页 |
| `homepage_design_image` | Custom Image | 自定义图片 |
| `incognito_search_history_title` | Show search history in Incognito Mode | 在无痕模式下显示搜索历史 |

## 6. 完成判据（B4）

- [ ] `i18n_scope.py B4 --stat` = 186/186（+ 4 组复数）
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL
- [ ] 提交：`i18n(zh): tabs, homepage, bookmarks and history`

---

# 第二部分：B8（194 条）

## 7. 目标

1. 备份/恢复全流程（选择分类、设密码、进度、结果）中文。
2. 关于页：简介、版本信息、开源声明、依赖库列表、社区链接中文（**许可证名与库名保留英文**）。
3. 首次启动引导 4 个步骤中文。
4. `i18n_scope.py B8 --stat` = 194/194。

## 8. 分块

| 块 | 前缀 | 条数 | 说明 |
|---|---|---|---|
| B8-C1 | `about_*` 74 | 74 | 含 1 条禁译 + 4 条长文本 |
| B8-C2 | `backup_*` 60 | 60 | 分类勾选、密码、进度、结果 |
| B8-C3 | `setup_*` 29 + `rerun_*` 2 | 31 | 引导页 |
| B8-C4 | `restore_*` 22 + `support_*` 5 + `debug_*` 2 | 29 | 恢复、支持作者、调试 |

## 9. 禁译与特殊处理

| key | 长度 | 处理 |
|---|---|---|
| `about_license_text` | 348 | **原文保留**，不进 zh 文件（check 脚本白名单） |
| `support_clint_markdown` | 1040 | 只翻标题与正文；`##`、链接、`%20`、emoji 原样 |
| `about_description` | 521 | 通读后直译，保留营销语气，不逐词硬译 |
| `about_keep_android_open_text` | 208 | 直译 |
| `about_library_*_license` 共 13 条 | — | 许可证名保留英文（Apache License 2.0 / MIT / ISC…），箭头 `\u2197` 保留 |
| `about_contact_email` | — | 邮箱原样 |
| `about_github_url` 等 URL | — | 原样 |

全大写标题（`setup_section_*`、`backup_category_*` 有的大写）用正常中文，不加大写。

## 10. 参考译法

| key | 英文 | 建议 |
|---|---|---|
| `setup_subtitle` | Lightweight browser with ADM, ad blocking… | 小巧的浏览器，支持 ADM 下载、广告屏蔽、媒体嗅探与多账号 |
| `setup_terms_continue` | Agree & Continue | 同意并继续 |
| `setup_section_address_bar` | ADDRESS BAR POSITION | 地址栏位置 |
| `backup_password_too_short` | Password must be at least 6 characters | 密码至少需要 6 个字符 |
| `backup_result_success_message` | Your backup has been saved. | 备份已保存 |
| `restore_row_summary` | Restore your data from a backup file | 从备份文件恢复数据 |
| `backup_category_cookies` | Browser Cookies | 浏览器 Cookie |
| `about_opensource_text` | The full source code is publicly available… | 完整源码公开在 GitHub 上，欢迎贡献代码、报告问题或提出功能建议 |
| `about_version_info` | Version: %1$s (build %2$d)\nDevice architecture: %3$s | 版本：%1$s（构建 %2$d）\n设备架构：%3$s |

## 11. 完成判据（B8）

- [ ] `i18n_scope.py B8 --stat` = 194/194，`about_license_text` 未出现在 zh 文件
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL
- [ ] 提交：`i18n(zh): backup, about and setup`

---

## 12. 两批共同的坑

| 坑 | 说明 |
|---|---|
| 把 `(s)` 照搬进中文 | 例如「书签(s)」，必须去掉 |
| 翻译许可证名 | Apache License 2.0 翻成「阿帕奇许可协议」会显得不专业，保留英文 |
| `support_clint_markdown` 里的 `%20` | 那是 URL 编码，不是占位符，改了链接就断 |
| 关于页依赖库名 | `adblock-rust by Brave`、`Markwon` 等保留原名，只翻「by」为「作者」或直接省略 |
| 引导页大写标题 | 中文不用全大写，正常写即可 |

---

## 13. 交接

- 下一步：`PLAN_7.md`（B6 隐私与屏蔽 354 条）。
- 台账记录：B4、B8 各自一个 commit；若只完成 B4，明确写「B8 未开始」。
