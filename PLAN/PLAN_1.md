# PLAN_1 — 总纲（Clint Browser 简体中文汉化）

> 本文件是整套计划的唯一契约。**任何一次新对话，先读本文件 + 自己那一份 PLAN_N，再动手。**
> 数据基线：`66acf9d`（v1.2.6）+ `7ed7b75`（恢复 .gitignore）。文中所有数量均为仓库实测值。

---

## 0. 会话协议（跨对话协作的关键）

### 开工（30 秒）
1. 读本文件第 2 节索引，找到本次要执行的 `PLAN_N`。
2. 读该 `PLAN_N` 全文，特别是「条目范围」「特殊条目」「完成判据」。
3. 确认工作区状态：`git status --short`，应只有 `PLAN/` 未跟踪；若有其他改动先问清楚。
4. 跑一次 `python tests/check_i18n.py --locale zh` 拿当前基线（若工具尚未建立，说明本次是 PLAN_2）。

### 收工（必做）
1. 跑该阶段的校验命令，把结果贴进对话。
2. 更新本文件第 8 节「进度台账」：状态、commit hash、遗留问题。
3. 明确告知下一次该从哪份 PLAN 开始。

### 铁律
- **一次对话只做一个批次**（PLAN_4、PLAN_6 例外，各含两个小批次）。
- 上下文接近告警就停手，宁可留半批下一次续，也不要压缩后再继续写译文。
- 译文必须**写进文件**再校验，不允许只在对话里展示。

---

## 1. 目标与非目标

### 目标
1. 界面全量简体中文，无中英混杂（除禁译清单）。
2. 「简体中文」出现在 设置 → 外观 → 语言，与现有 6 语种同级。
3. 系统语言为中文时，首次启动即为中文。
4. 建立可复用校验脚本，上游新增字符串后能一键发现漏译。
5. 每批独立可编译、可回滚。

### 非目标
- 不做繁体（预留 `values-zh-rTW`）。
- 不碰 Bergamot 网页翻译的语言数据（那是运行时模型文件）。
- 不做运行时机器翻译 / overlay APK / Xposed。
- 不改字符串 ID、结构、顺序（除明确的占位符微重构）。

---

## 2. 文档索引

| 文件 | 会话 | 内容 | 条目量 | 前置 |
|---|---|---|---|---|
| **PLAN_1.md** | — | 总纲：事实、决策、术语、规则、台账 | — | — |
| **PLAN_2.md** | S1 | Phase 0 骨架 + 工具链 + 占位符重构 | 32 处重构 | 装 SDK 37 |
| **PLAN_3.md** | S2 | B1 通用动作 / 设置导航 / 对话框 | 333 + 3 复数 | PLAN_2 |
| **PLAN_4.md** | S3 | B2 外观与主题 + B5 媒体与权限 | 234 + 104 | PLAN_3 |
| **PLAN_5.md** | S4 | B3 下载 / 下载管理器 / MEGA | 440 + 13 复数 | PLAN_2 |
| **PLAN_6.md** | S5 | B4 标签页/书签/历史 + B8 备份/关于/引导 | 186 + 194 | PLAN_3 |
| **PLAN_7.md** | S6 | B6 隐私 / 网站屏蔽 / 过滤列表 | 354 | PLAN_2 |
| **PLAN_8.md** | S7 | B7 脚本/翻译/数据/崩溃 + 全量终检 | 334 + 5 复数 | PLAN_4/5/6/7 |
| **PLAN_9.md** | S8 | 收尾：一次编译 + 交付（PR 可选） | — | 全部 |

合计：2179 字符串 + 25 组复数（50 项）= 与源文件严格对平，无遗漏无重复。

---

## 3. 项目事实速查

### 3.1 资源规模
- `app/src/main/res/values/strings.xml`：2185 `<string>`，其中 6 条 `translatable="false"` → **需翻译 2179 条**（S1 新增 `language_name_chinese`，原 2184/2178）
- `<plurals>` 25 组 / 50 个 item
- 188 条含位置占位符 `%1$s` / `%1$d`；29 条含非位置 `%s` / `%d`；另有 3 组复数（6 个 item）含非位置 `%d`
- 无 `<string-array>` 需翻译（`arrays.xml` 只有搜索引擎名）

### 3.2 语言机制（改这 4 处即可）
| 文件 | 行 | 作用 |
|---|---|---|
| `util/LocaleHelper.kt` | 11–18 | 语言常量 |
| 同上 | 21–28 | `SUPPORTED_LANGUAGE_TAGS` 白名单，**不加就回退** |
| 同上 | 46–54 | `supportedSystemLocale()` 系统语言映射 |
| `settings/lookandfeel/LanguageUtils.kt` | 9–17 | 语言列表 |
| `values/strings.xml` | 236–246 | `language_name_*` 名称 |

生效链路：`ClintApplication.attachBaseContext`、`ClintActivity.kt:55`、`BackgroundPlaybackService:54`、`DownloadForegroundService:65` 全部走 `LocaleHelper.wrapContext`；切换语言由 `ClintActivity.captureAndApplyLanguage()`（:167）写 prefs + `recreate()`。

### 3.3 构建
| 项 | 值 | 备注 |
|---|---|---|
| compileSdk / targetSdk | 37 | 本机已装 `platforms/android-37.0`（build-tools 仅 35/36，实测不影响构建） |
| minSdk | 26 | 无需考虑 Android 13 每应用语言强制 |
| Gradle | wrapper 9.8.1 | `configuration-cache=true` |
| JDK | 21（`jvmTarget 17`） | 满足 |
| flavor | `github` / `foss` | 验收用 `githubDebug` |
| 语言拆分 | `bundle.language.enableSplit = false` | 中文整体入包，无需动态下发 |
| 原生库 | `jniLibs` 4 ABI 已提交 | 会产出多 APK |
| CI | `assembleGithubRelease` | aapt2 错误必红 |

### 3.4 已确认的“无需担心”
- UI 文案 100% 走 `stringResource`/`getString`；Kotlin 仅 2 处剪贴板标签为硬编码，不显示在界面
- JS assets 无用户可见英文
- 无自定义字体 → 中文走系统字体，无豆腐块
- 设置搜索基于 `getString()`（`SettingsSearch.kt:498-527`）→ 中文搜索自动生效

### 3.5 已确认的“必须处理”
- 俄语 3 处、印地语 2 处复数 `one` 分支混入 `%1$d`（源文件该分支无占位符）→ 仓库无任何跨语种校验，必须自建
- 29 条字符串 + 6 个复数 item 用非位置占位符 → 中文改语序前必须重构

---

## 4. 关键决策

| # | 决策 | 选择 | 理由 | 被否方案 |
|---|---|---|---|---|
| D1 | 资源目录 / tag | `values-zh` + `zh` | zh 语族兜底，一次覆盖简繁设备；一个目录维护 | `values-zh-rCN`：繁体设备整屏英文 |
| D2 | 繁体 | 本期不做，预留 | 加 `values-zh-rTW` 即可，无需改代码 | 同批做两份：成本翻倍 |
| D3 | 范围 | 2179 条全量 + 禁译清单 | 中英混杂比不翻更劝退；缺键自动回退，可分批发 | 只翻设置页 |
| D4 | 生产方式 | 术语表 + 分批机辅 + 人审 | 440 条下载类高度模板化；但术语必须锁死 | 整文件一次生成即提交 |
| D5 | 校验 | 自建 `tests/check_i18n.py` | 无 lint 配置，lint 也查不出占位符错配 | 只靠编译 |
| D6 | 上游 | 先骨架 PR，再分批推 | 2100 条 PR 无人 review | 一次性全量 PR |

---

## 5. 术语表（全篇唯一写法，禁止同义替换）

| 英文 | 中文 | 备注 |
|---|---|---|
| Tab / Tabs | 标签页 | 不写“选项卡” |
| Incognito | 无痕 | 无痕模式 / 无痕标签页 |
| Bookmark | 书签 | |
| History | 历史记录 | 设置项内可简称“历史” |
| Download / Downloads | 下载 | 名词视上下文作“下载内容” |
| Download Manager | 下载管理器 | |
| Segment | 分片 | 下载分片 |
| Connection | 连接数 | 并发连接 |
| Thread | 线程 | 多线程下载 |
| Resume | 续传 | |
| Homepage | 主页 | |
| Home | 首页 | 与「主页」区分 |
| New Tab | 新建标签页 | |
| Reader Mode | 阅读模式 | |
| User Script | 用户脚本 | |
| Website Blocker | 网站屏蔽 | 不写“拦截器” |
| Filter List | 过滤规则列表 | |
| Category | 分类 | 过滤列表分类 |
| Exception | 例外 | 例外站点 |
| Custom Prompts | 自定义提示 | |
| Data Saver | 省流模式 | |
| Desktop Mode | 桌面版网站 | |
| Media Capture | 媒体嗅探 | 检测网页音视频 |
| Background Playback | 后台播放 | |
| Cookies | Cookie | 保留英文 |
| User Agent | 用户代理 | |
| Profile | 配置文件 | 不写“档案” |
| Backup / Restore | 备份 / 恢复 | |
| Setup | 初始设置 | 引导页 |
| Crash Report | 崩溃报告 | |
| Measurement | 性能检测 | |
| Quiver Guard | Quiver Guard | 品牌名不译 |
| MEGA | MEGA | 品牌名不译 |
| Bergamot | Bergamot | 引擎名不译 |

---

## 6. 硬性规则

1. **占位符**：`%1$s`/`%1$d` 可调语序，编号与类型必须一一对应；禁止降级为 `%s`。
2. **非位置占位符已重构**：PLAN_2 完成后源文件全部是位置参数，译文直接复用编号。
3. **复数**：zh 只有 `other`。`values-zh` 内 `<plurals>` 只写一个 `<item quantity="other">`。
4. **转义**：`'` → `\'`；`&` → `&amp;`；`<` → `&lt;`；`\n`、`\u2026` 原样；值不得以 `@` 或 `?` 开头。
5. **标点**：全角；省略号 `…`；引号 `「」`；括号全角；破折号 `——`。
6. **空格**：汉字与数字之间**不加**空格；英文品牌名与汉字之间加一个半角空格（如「使用 MEGA 下载」）。
7. **风格**：按钮 2–4 字（确定/取消/删除/保存/关闭）；设置项标题 ≤ 12 字、不加句号；描述句末不加句号；少用“请”。
8. **结构**：key 顺序、注释、`translatable` 属性与源文件逐行对应，禁止重排（便于 diff 与续译）。
9. **一致性**：同一概念全篇同一译法，以第 5 节为准；新术语先补表再动笔。
10. **禁止机翻痕迹**：不出现「点击此处」「您的」「一個」等；不出现繁体字；不出现全角英文。

---

## 7. 禁译清单

| key / 范围 | 处理 |
|---|---|
| `about_license_text` | **原文保留**（GPLv3 法律文本） |
| `custom_theme_preview_*` 6 条 | 源文件已 `translatable="false"`，不进 zh 文件 |
| `quiver` 前缀中的品牌名 | Quiver Guard 等保留英文 |
| 搜索引擎名 DuckDuckGo / Brave / Google | 保留 |
| 值中的 URL、MIME、文件名、协议名 | 一字不改 |
| `support_clint_markdown` | 只翻标题与正文；徽章链接、`%20` 编码、emoji 原样 |

---

## 8. 进度台账

> 每次收工更新。状态：⬜ 未开始 / 🟨 进行中 / ✅ 完成 / ⛔ 阻塞

| 阶段 | 内容 | 条目 | 状态 | commit | 备注 |
|---|---|---|---|---|---|
| S1 | Phase 0 骨架 + 工具 + 占位符重构 | — | ✅ | `3c62c2c` `f85750e` `a69cd38` | 脚本过：`strings 5/2185`、`5/2179`；`assembleGithubDebug` BUILD SUCCESSFUL（SDK 37.0 已装，本地补了 `gradle-wrapper.jar`） |
| S2 | B1 通用/设置导航 | 333 + 3 | ✅ | `76a08d5` | `B1 333/333 100%`，`check_i18n --allow-missing` OK，全库 334/2179（15%） |
| S3 | B2 外观 + B5 媒体 | 234 + 104 | ✅ | `8c436f1` `b54a760` | `B2 234/234`、`B5 104/104`，色名查重无重复，全库 672/2179（30%） |
| S4 | B3 下载 | 440 + 13 | ✅ | `4657915` | `B3 440/440 100%`，五个块一次提交，全库 1112/2179（51%） |
| S5 | B4 标签页 + B8 备份/关于 | 186 + 194 | ✅ | `95776f3` `13267e9` | `B4 186/186`、`B8 194/194`，全库 1492/2179（68%） |
| S6 | B6 隐私屏蔽 | 354 | ✅ | `ffafc0c` | `B6 354/354`，全库 1846/2179（84%） |
| S7 | B7 脚本/翻译/数据 + 终检 | 334 + 5 | ✅ | `c9e20e0` `c218347` | `B7 334/334`，**全库 2179/2179、25/25**，严格模式 OK，繁体/机翻/`(s)` grep 0 命中 |
| S8 | 收尾：一次编译 + 交付 | — | ✅ | — | 编译通过；真机验收交用户 |
| S9 | 全局刷新率同步（PLAN_10，v1.2.7/47） | — | 🟨 | `08981fa` `d1fd59a` | 代码完成、编译通过；**真机帧率未验**（设备未连接） |

---

## 9. 全局风险

| 风险 | 影响 | 对策 |
|---|---|---|
| 未转义 `'` / 裸 `&` | aapt2 编译失败 | check 脚本第 6/7 项 + 本地 assemble |
| 占位符改写/漏写 | 运行时崩溃 | check 脚本第 4/5 项 |
| 复数写了 `one` | lint 噪音 / 误用 | 脚本第 3 项强制只有 `other` |
| 术语漂移 | 观感业余 | 每份 PLAN_N 开头复述本批术语；收工自查 |
| 上游新增字符串 | 英文碎片 | `check_i18n.py --report-missing` |
| `accent` 101 色名重复 | 主题选择器无法区分 | 命名法见 PLAN_4，脚本查重 |
| `app-github-universal-debug.apk` 装上闪崩 | 装机验证失败 | 用对应 ABI 包（如 `arm64-v8a`） |
| 跨批续译遗漏 | 漏条 | `i18n_scope.py` 实时统计覆盖率 |

---

## 10. 完成定义（DoD）

**验收只看脚本，不做逐屏人工验收。** 整库只在 PLAN_9 跑一次编译。

1. `python tests/check_i18n.py --locale zh` 无 FAIL（占位符、复数、转义、多余 key）。
2. `python tests/i18n_scope.py --all --stat` 达到 2179/2179。
3. 该批已提交，`git status` 干净（`PLAN/`、`AGENTS.md`、`local.properties` 除外）。

---

## 11. 待确认

| # | 问题 | 建议 |
|---|---|---|
| Q1 | 目录 `values-zh` vs `values-zh-rCN` | `values-zh`（D1） |
| Q2 | 本期做繁体 | 不做（D2） |
| Q3 | 是否提上游 PR | 先骨架 PR（D6） |
| Q4 | `about_license_text` / `support_clint_markdown` | 前者不译，后者只翻正文（D3） |
| Q5 | 是否加 `localeConfig` | 默认不加（与自带切换器有冲突风险） |
| Q6 | 是否重构非位置占位符 | 是，PLAN_2 内完成 |