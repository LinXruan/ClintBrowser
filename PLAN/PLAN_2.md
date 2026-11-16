# PLAN_2 — Phase 0：骨架、工具链、占位符重构

> 会话 S1 · 前置：安装 Android SDK Platform 37 · 后面所有批次都依赖本文件产出的目录与脚本
> 本阶段**不翻译业务文案**，只让「中文」这个语言存在、可被选中、可被校验。

---

## 1. 本阶段要达成什么

1. `values-zh` 存在，`zh` 进白名单，语言列表出现「简体中文」。
2. `tests/i18n_scope.py` 与 `tests/check_i18n.py` 可运行。
3. 29 条字符串 + 6 个复数 item 的非位置占位符全部改为位置参数（`grep -cE '%[sd]' values/strings.xml` = 0）。

---

## 2. 前置：环境

| 项 | 现状 | 要做 |
|---|---|---|
| JDK | 21 ✅ | 无 |
| Gradle wrapper | 9.8.1 ✅（`gradle-wrapper.jar` 已补入） | 无 |
| SDK Platform | 37.0 ✅ | 无 |

> 环境已就位，S1 的 `assembleGithubDebug` 已通过。后续批次只跑脚本，不要求每批编译。

---

## 3. 步骤

### 0.1 建资源目录（先只放 5 条）

新建 `app/src/main/res/values-zh/strings.xml`：

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Clint 浏览器</string>
    <string name="clint_downloader_label">Clint 下载器</string>
    <string name="settings">设置</string>
    <string name="language_name_chinese">简体中文</string>
    <string name="language_system">跟随系统</string>
</resources>
```

- `app_name` 的取舍：改成「Clint 浏览器」会让桌面图标名变中文；若希望保留品牌原样，可只写 `Clint Browser`。**默认取「Clint 浏览器」**，与国内习惯一致。
- 这里用 `language_system` 覆盖一条，是为了立刻肉眼确认语言确实切换了。

### 0.2 注册语言常量与白名单

文件 `app/src/main/java/com/jhaiian/clint/util/LocaleHelper.kt`

**改动 1**（第 11–18 行的常量区，末尾追加）：

```kotlin
const val LANGUAGE_SPANISH = "es"
const val LANGUAGE_CHINESE = "zh"      // ← 新增
```

**改动 2**（第 21–28 行的白名单，末尾追加）：

```kotlin
private val SUPPORTED_LANGUAGE_TAGS = listOf(
    LANGUAGE_ENGLISH,
    LANGUAGE_FILIPINO,
    LANGUAGE_HINDI,
    LANGUAGE_INDONESIAN,
    LANGUAGE_PORTUGUESE_BRAZIL,
    LANGUAGE_RUSSIAN,
    LANGUAGE_SPANISH,
    LANGUAGE_CHINESE                     // ← 新增
)
```

**改动 3**：不需要。

`supportedSystemLocale()`（46–54 行）里 `"zh"` 加入白名单后会自动落到 `in SUPPORTED_LANGUAGE_TAGS -> system` 分支，返回系统 locale（zh-CN / zh-TW 均可），资源查找会命中 `values-zh`。**不要**再手写 `"zh" -> Locale.forLanguageTag("zh")` 分支，否则 zh-TW 会被强行改成 zh-CN，日期格式反而失配。

### 0.3 语言列表加一项

文件 `app/src/main/java/com/jhaiian/clint/settings/lookandfeel/LanguageUtils.kt`

```kotlin
val languageOptions = listOf(
    LanguageOption(LocaleHelper.LANGUAGE_ENGLISH, R.string.language_name_english),
    ...
    LanguageOption(LocaleHelper.LANGUAGE_SPANISH, R.string.language_name_spanish),
    LanguageOption(LocaleHelper.LANGUAGE_CHINESE, R.string.language_name_chinese)   // ← 新增
)
```

顺序：追加在末尾，与现有「按加入时间」排列一致。

### 0.4 语言名称字符串

文件 `app/src/main/res/values/strings.xml`，第 246 行 `language_name_spanish` 之后追加：

```xml
<string name="language_name_chinese">简体中文</string>
```

其他 6 个语种文件同步补一条（可选，但不做的话它们的语言列表会显示英文 “Chinese”）：

| 文件 | 值 |
|---|---|
| `values-es` | Chino (simplificado) |
| `values-fil` | Tsino (Pinasimple) |
| `values-hi` | चीनी (सरलीकृत) |
| `values-in` | Tionghoa (Sederhana) |
| `values-pt-rBR` | Chinês (simplificado) |
| `values-ru` | Китайский (упрощённый) |

### 0.5 `localeConfig`（默认不做）

Android 13+ 系统设置里的「应用语言」需要 `android:localeConfig`。**默认不加**，原因：本应用自带切换器，两套机制同时存在时，系统级设置会在下次启动覆盖应用内偏好，产生“我明明选了中文又变回英文”的怪现象。

若以后要做，需同时满足：
1. 新建 `app/src/main/res/xml/locales_config.xml` 列出全部 `<locale android:name="…"/>`
2. `AndroidManifest.xml` 第 56 行 `<application` 加 `android:localeConfig="@xml/locales_config"`
3. 实测「系统设置改语言 → 应用内再改 → 重启」三者行为一致

### 0.6 新建 `tests/i18n_scope.py`（范围单一事实源）

作用：把第 4 节那张前缀表变成可执行文件，任何会话都能算出「本批到底有哪些 key、还差多少」。

```python
#!/usr/bin/env python3
"""按批次导出待译 key。用法：
    python tests/i18n_scope.py B3              # 打印 B3 全部 key + 状态
    python tests/i18n_scope.py B3 --missing    # 只打印未翻译的
    python tests/i18n_scope.py --all --stat    # 各批覆盖率
"""
SCOPE = {
    "B1": ["pref", "app", "language", "look", "misc", "menu", "action", "popup",
           "address", "link", "search", "suggestion", "suggestions", "open", "clear",
           "choose", "create", "check", "hide", "view", "skip", "remember", "restart",
           "install", "default", "exit", "back", "forward", "share", "next", "get",
           "use", "close", "no", "reader", "toast", "content", "select", "preview",
           "date", "shortcut", "settings", "home", "downloading", "refresh"],
    "B2": ["accent", "custom", "surface", "theme", "color", "frameless"],
    "B3": ["download", "downloads", "mega", "redownload"],
    "B4": ["tab", "tabs", "homepage", "bookmarks", "history", "incognito",
           "nested", "strip", "new", "delete_inactive"],
    "B5": ["media", "image", "document", "camera", "mic", "location", "voice",
           "notification", "clipboard", "background", "screenshot", "battery"],
    "B6": ["website", "quiver", "filter", "cookies", "additional", "privacy", "do",
           "webrtc", "global", "block", "ssl", "http", "https", "site"],
    "B7": ["user", "js", "translation", "data", "engine", "desktop", "autofill",
           "speed", "beta", "update", "crash", "profiles", "measurement", "browser",
           "clint", "google", "javascript", "web", "delete_data"],
    "B8": ["backup", "restore", "about", "support", "setup", "debug", "rerun"],
}

def prefix(name: str) -> str:
    if name.startswith("delete_inactive"):
        return "delete_inactive"
    if name.startswith("delete_data"):
        return "delete_data"
    return name.split("_")[0]
```

实现要点：
- 用 `xml.etree.ElementTree` 解析 `values/strings.xml` 与 `values-zh/strings.xml`
- 排除 `translatable="false"`
- `--stat` 输出形如：`B1 333/333 100%`，并给出总计 2179
- 退出码：全部完成返回 0，否则 1（便于串联 CI）

### 0.7 新建 `tests/check_i18n.py`（质量门禁）

CLI：`python tests/check_i18n.py --locale zh [--report-missing]`

9 项断言（任一失败 `exit 1`，逐条打印 `[FAIL] key …`）：

| # | 断言 | 判定方式 |
|---|---|---|
| 1 | XML 可解析、根为 `<resources>` | `ET.parse` 异常即失败 |
| 2 | key 集合一致（排除 6 条禁译项） | 双向差集为空 |
| 3 | 复数 quantity 合法 | zh 只允许 `other`；出现其他即失败 |
| 4 | 占位符多重集一致 | 对每个 key / 每个 quantity 提取 `%\d+\$[sd]`，排序后比较 |
| 5 | 非位置占位符计数一致 | 统计 `%[sd]`（排除 `%%` 与 `%\d+\$`），数量必须与源文相同 |
| 6 | 值不以 `@`/`?` 开头、无裸 `&`、无裸 `<` | 正则检测，XML 已转义的 `&amp;`/`&lt;` 不算 |
| 7 | 单引号已转义 | 含 `'` 且未被 `\` 前缀、且整串非双引号包裹 → 失败 |
| 8 | 无空值；长度 ≤ 源文 1.6 倍 | 超长只告警，不阻断（避免误伤） |
| 9 | 术语抽查 | 命中禁用写法表（如 `Tab`、`Incognito` 未译为中文）→ 告警 |

`--report-missing` 输出未译 key 清单（按批次分组），供 PLAN_3–8 续译使用。

输出样例：

```
[OK]   strings 2179/2179  plurals 25/25
[WARN] 3 keys longer than 1.6x source
[FAIL] placeholder mismatch: downloads_selected_count  src=[%1$d]  zh=[%d]
exit 1
```

> 这两个脚本**不进上游 PR**（先本地提交，提 PR 时用分支裁剪排除）。

### 0.8 非位置占位符重构（32 处 = 29 条字符串 + 3 组复数共 6 项）

把 `%s` → `%1$s`、`%d` → `%1$d`（**只改英文源文件**，其他语种保持 `%s`/`%d` 仍能正常工作）。

**字符串（29 条）**

| 批次 | key | 原文 |
|---|---|---|
| B3 | `downloads_selected_count` | `%d selected` |
| B3 | `downloads_delete_confirm_message` | `Remove %d download(s)?` |
| B3 | `mega_error_generic` | `MEGA couldn't open this link (error %d)` |
| B4 | `bookmarks_selected_count` | `%d selected` |
| B4 | `bookmarks_delete_confirm_message` | `Delete %d bookmark(s)?` |
| B4 | `bookmarks_delete_confirm_message_folders` | `Delete %d item(s)? …` |
| B4 | `bookmarks_folder_item_count` | `%d items` |
| B4 | `bookmarks_import_success` | `Imported %d bookmarks` |
| B4 | `history_selected_count` | `%d selected` |
| B4 | `history_delete_confirm_message` | `Remove %d item(s) from history?` |
| B5 | `camera_web_request_message` | `%s wants to use your camera.` |
| B5 | `mic_web_request_message` | `%s wants to use your microphone.` |
| B5 | `location_web_request_message` | `%s wants to access your location.` |
| B5 | `notification_web_request_message` | `%s wants to send you notifications.` |
| B5 | `clipboard_web_request_message` | `%s wants to see text on your clipboard.` |
| B6 | `quiver_guard_exception_delete_message` | `Remove %d saved site(s)?` |
| B6 | `site_permission_delete_confirm_message` | `Remove %d exception(s)?` |
| B6 | `filter_list_delete_confirm_message` | `Remove %d filter list(s)?` |
| B6 | `website_blocker_status_active` | `Protecting you from %d known domains` |
| B6 | `website_blocker_delete_confirm_message` | `This removes the downloaded data for %d selected categories…` |
| B6 | `additional_websites_summary` | `Websites added: %d` |
| B6 | `additional_websites_delete_confirm_message` | `This will delete %d selected websites…` |
| B7 | `desktop_mode_delete_confirm_message` | `Remove %d saved site(s)?` |
| B7 | `user_scripts_runs_on_patterns` | `Runs on %d URL patterns` |
| B7 | `user_scripts_delete_confirm_message` | `This will delete %d selected scripts.` |
| B7 | `user_scripts_metadata_version` | `Version %s` |
| B7 | `user_scripts_metadata_author` | `by %s` |
| B7 | `user_scripts_metadata_requires` | `Requires %d external scripts` |
| B7 | `data_saver_exception_delete_message` | `Remove %d saved site(s)?` |

**复数（3 组 / 6 个 item，均在 `other` 与 `one` 内）**

| key | 批次 | 原文 |
|---|---|---|
| `mega_folder_started` | B3 | `Downloading %d file(s)` |
| `mega_folder_added_paused` | B3 | `Added %d file(s) to Downloads, paused` |
| `translation_never_sites_count` | B7 | `%d site(s)` |

**改法**：逐条把 `%d`→`%1$d`、`%s`→`%1$s`，语义与文案不变。

**不需要人工验证**：位置参数与单参数调用完全兼容，脚本第 4/5 项会逐条比对占位符。

### 0.9 校验

```bash
python tests/i18n_scope.py B1 --stat      # 应报 0/333
python tests/check_i18n.py --locale zh --allow-missing
```

> 注意：`check_i18n.py` 在 zh 尚不完整时应**把缺失计为“未译”而非失败**，只有出现“多余 key / 占位符错配 / 转义错误”才失败。这一策略写进脚本参数 `--allow-missing`（分批阶段都用），全量译完后的终检不加。

### 0.10 提交

```
i18n(zh): add locale skeleton and language entry
refactor(i18n): use positional args in format strings
chore(i18n): add translation scope and consistency scripts
```

三个独立 commit，顺序如上。第二、三个若担心污染 PR，可在提 PR 时单独挑出（第一个是必提的）。

---

## 4. 完成判据

- [ ] `values-zh/strings.xml` 存在、含 5 条，语言列表有「简体中文」
- [ ] 两个脚本可运行，`--stat` 输出 2179 总数
- [ ] 35 处占位符已改，`grep -cE '%[sd]' values/strings.xml` = 0
- [ ] 3 个 commit 完成

---

## 5. 本阶段独有的坑

| 坑 | 说明 |
|---|---|
| 把 `zh` 写成 `zh-CN` 加进白名单 | 资源目录仍是 `values-zh`，但 `Locale.forLanguageTag("zh-CN")` 也会命中 `values-zh`；两种都能用，但**统一用 `zh`**，避免日后加繁体时白名单要写两条 |
| 给 `supportedSystemLocale()` 加 `"zh" -> Locale.forLanguageTag("zh")` | 会丢失 zh-TW 的地区信息，日期/数字格式变大陆风格，属过度设计 |
| 以为 zh 文件必须一次写全才不报错 | 缺键自动回退英文，分批完全合法 |
| 用 `values-zh-rCN` 却把 tag 写成 `zh` | 也能命中，但语义不一致，日后维护会困惑；二选一，本方案统一 `zh` |
| `app_name` 改中文后桌面图标名变化 | 预期行为；如果不想，保留英文 |

---

## 6. 交接

- 下一步：`PLAN_3.md`（B1，333 条 + 3 组复数），这是“骨架 PR 可提”的最后一块。
- 交接时确认：`tests/i18n_scope.py B1 --stat` 应为 `0/332`，`values-zh` 里只有 5 条。
- S1 编译已过；S2 起每批只跑脚本，除非改到 Kotlin 才需要再编一次。
