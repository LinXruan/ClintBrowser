# PLAN_8 — B7：用户脚本、页面翻译、数据与崩溃报告

> 会话 S7 · 334 条字符串 + 5 组复数（10 项）· 前置：PLAN_4/5/6/7 至少完成任意三个
> 本批是**最后一个翻译批次**，收尾时同时执行全量终检（第 7 节）。

---

## 1. 目标（可验证）

1. 用户脚本：安装提示、编辑器状态栏、元数据、运行时机、更新结果全部中文。
2. 页面翻译：翻译条、语言偏好、语言包下载/删除、模型说明全部中文。
3. 省流模式 40 条开关与说明全部中文；桌面版网站、自动填充、网页加速相关文案中文。
4. 清除数据页（含 4 组复数）中文。
5. 崩溃报告页、配置文件（多账号）、性能检测、测试版通道中文。
6. `i18n_scope.py B7 --stat` = 334/334，且全库覆盖率达到 2179/2179。

---

## 2. 分块

| 块 | 前缀 | 条数 | 界面 |
|---|---|---|---|
| C1 | `user_scripts` 89 · `user_script` 4 · `js_*` 7 · `javascript_*` 2 · `browser_*` 2 | **104** | 用户脚本列表/编辑器/安装页 |
| C2 | `translation_*` 53 · `engine_*` 10 | **63** | 翻译条、翻译设置、语言包 |
| C3 | `data_saver_*` 40 · `desktop_*` 13 · `autofill_*` 6 · `speed_*` 2 · `web_*` 2 | **63** | 省流模式、桌面版网站、自动填充 |
| C4 | `crash_*` 25 · `profiles_*` 25 · `measurement_*` 8 · `beta_*` 5 · `clint_*` 1 · `google_*` 2 | **66** | 崩溃报告、多账号、性能检测、测试版 |
| C5 | `delete_data_*` 23 · `update_*` 15 | **38** | 清除数据页、应用更新 |
| | | **334** | |

---

## 3. 特殊条目

### 3.1 复数（5 组）

| key | 英文 other | 建议 |
|---|---|---|
| `delete_data_history_items` | %1$d items | %1$d 项 |
| `delete_data_history_from_sites` | From %1$s + %2$d sites | 来自 %1$s 及 %2$d 个网站 |
| `delete_data_tabs_summary` | Closes %1$d open tabs | 关闭 %1$d 个已打开的标签页 |
| `delete_data_site_settings_summary` | %1$d sites | %1$d 个网站 |
| `translation_never_sites_count` | %d sites → `%1$d` | %1$d 个网站 |

### 3.2 非位置占位符（已重构）

| key | 英文 | 建议 |
|---|---|---|
| `desktop_mode_delete_confirm_message` | Remove %d saved site(s)? | 移除 %1$d 个已保存的网站？ |
| `user_scripts_runs_on_patterns` | Runs on %d URL patterns | 匹配 %1$d 条 URL 规则 |
| `user_scripts_delete_confirm_message` | This will delete %d selected scripts. | 将删除 %1$d 个已选脚本。 |
| `user_scripts_metadata_version` | Version %s | 版本 %1$s |
| `user_scripts_metadata_author` | by %s | 作者：%1$s |
| `user_scripts_metadata_requires` | Requires %d external scripts | 依赖 %1$d 个外部脚本 |
| `data_saver_exception_delete_message` | Remove %d saved site(s)? | 移除 %1$d 个已保存的网站？ |

### 3.3 转义与多行

| key | 特征 | 处理 |
|---|---|---|
| `js_warning_message` | 长段，含 `\n\n` | 保留段落分隔 |
| `google_warning_message` | `…\n\nFor b…` | 保留 `\n\n` |
| `crash_report_instructions` | 含 `\u2014`（破折号） | 保留破折号转义 |
| `crash_step_open_github` | `Tap \u201cOpen GitHub Issues\u201d` | 保留中文引号或改「」，不要留 `\u201c` |
| `beta_enrol_message`（277 字符） | 多段，含 `\n\n` | 保留段落；说明「可能不稳定」 |
| `user_scripts_update_all_failed` / `_partial_result` | 多参数 + `\n\n` | 参数顺序别错位 |
| `user_scripts_editor_status_position` | `Ln %1$d, Col %2$d` | 第 %1$d 行，第 %2$d 列 |
| `update_download_preparing` | `Preparing\u2026` | 正在准备\u2026 |

---

## 4. 术语

| 英文 | 中文 |
|---|---|
| User Script | 用户脚本 |
| Metadata | 元数据 |
| Runs at page start / end | 页面开始/结束时运行 |
| URL patterns | URL 匹配规则 |
| Engine | 引擎 |
| Language pack / model | 语言包 / 模型 |
| Translate | 翻译 |
| Always / Never translate | 始终翻译 / 永不翻译 |
| Data Saver | 省流模式 |
| Desktop Mode | 桌面版网站 |
| Autofill | 自动填充 |
| Web acceleration | 网页加速 |
| Clear browsing data | 清除浏览数据 |
| Time range | 时间范围 |
| Profile | 配置文件 |
| Crash report | 崩溃报告 |
| Measurement | 性能检测 |
| Beta channel | 测试版通道 |

---

## 5. 参考译法

| key | 英文 | 建议 |
|---|---|---|
| `translation_bar_prompt` | Translate this page? | 翻译此页面？ |
| `translation_language_preferences_summary` | Choose languages to always or never translate | 选择始终翻译或永不翻译的语言 |
| `data_saver_block_scripts_summary` | Stops pages from downloading JavaScript… | 阻止页面下载 JavaScript 文件，可大幅节省流量，但许多网站会无法正常使用 |
| `desktop_mode_no_saved_sites` | No sites saved | 未保存任何网站 |
| `user_scripts_add_fab_desc` | Write a new script | 编写新脚本 |
| `user_scripts_run_at_start` | Runs at page start | 页面开始时运行 |
| `user_scripts_item_local_no_update` | Local scripts don't have updates to check | 本地脚本没有可检查的更新 |
| `crash_copy` | Copy crash report | 复制崩溃报告 |
| `profiles_settings_summary` | Stay signed in to several accounts… | 在同一网站上同时登录多个账号 |
| `desktop_mode` | Desktop Mode | 桌面版网站 |

---

## 6. 操作步骤

1. C1（104）→ C2（63）→ C3（63）→ C4（66）→ C5（38）。
2. C2 注意：`translation_*` 里区分「语言包（下载的文件）」与「模型（引擎）」两个词，不要混。
3. 每块后 `check_i18n.py --locale zh --allow-missing`。
4. 全部完成后执行第 7 节全量终检。

---

## 7. 全量终检（脚本三条，5 分钟）

```bash
# 1) 覆盖率：应 2179/2179
python tools/i18n_scope.py --all --stat

# 2) 严格模式：不允许 missing
python tools/check_i18n.py --locale zh

# 3) 一次 grep 兜底：繁体字 / 机翻口头禅 / (s) 残留
grep -nE '個|這|們|與|為|請點擊|您的|的的|\(s\)' app/src/main/res/values-zh/strings.xml
```

三条全过即完成，不再做人工逐条审计；编译留到 PLAN_9。

---

## 8. 完成判据

- [ ] `i18n_scope.py B7 --stat` = 334/334（+ 5 组复数），`--all --stat` 达到 2179/2179
- [ ] `check_i18n.py --locale zh`（严格模式）无 FAIL；第 7 节 grep 无命中
- [ ] 提交：`i18n(zh): user scripts, translation and data`

---

## 9. 本批独有的坑

| 坑 | 说明 |
|---|---|
| `translation_*` 里「语言」与「语言包」混用 | 下载的是语言包，引擎是 Bergamot，两者不能互换 |
| `profiles_*` 译成「个人资料」 | 此处是浏览器多账号容器，统一「配置文件」 |
| `measurement_*` 译成「测量」 | 指性能/启动耗时统计，用「性能检测」 |
| `user_scripts_metadata_author` 的 `by %s` | 中文写「作者：%1$s」，冒号用全角 |
| 清除数据的 4 组复数 | 只写 `other`；`delete_data_history_from_sites` 有两个参数，别丢 `%2$d` |
| google_warning_message 的段落 | 丢了 `\n\n` 会变成一大段密不透风的字 |

---

## 10. 交接

- 下一步：`PLAN_9.md`（编译一次 + 交付）。已经没什么要验的了，装一次看眼即可。
- 台账记录：B7 完成 + 全量统计数字（2179/2179）。
