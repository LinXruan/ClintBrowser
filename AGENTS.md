# AGENTS.md

给在本仓库工作的 AI 代理看的说明。**开工前先读完本文件，再读 `PLAN/PLAN_1.md`。**

---

## 1. 这是什么项目

Android 浏览器 **Clint Browser**（Kotlin + Jetpack Compose，GPLv3），上游仓库 `jhaiian/ClintBrowser`。
本 fork 的唯一目的：**做简体中文汉化**，把界面从英文翻译成简体中文，不改变上游功能行为。

- 语言：Kotlin、少量 JS（注入脚本）、Rust/C++（屏蔽引擎，见 `native/`）
- 构建：Gradle wrapper 9.8.1，`compileSdk/targetSdk = 37`，`minSdk = 26`，JDK 17+（本机 21）
- 当前基线：`7ed7b75`（上游 v1.2.6 + 恢复 .gitignore 的本地提交）

---

## 2. 目录速查

```
app/src/main/
  java/com/jhaiian/clint/     Kotlin 源码（界面全部 Compose）
    util/LocaleHelper.kt      ★ 语言开关的核心：常量 + 白名单 + Context 包装
    settings/lookandfeel/     ★ 语言选择 UI（LanguageUtils / LookAndFeelDialogs）
    settings/search/          设置搜索（基于 getString，中文自动生效）
    translation/              Bergamot 网页翻译功能（勿与界面语言混淆）
    downloads/ browser/ settings/ mediacapture/ blocker/ ...
  res/
    values/strings.xml        ★ 英文源文件，2184 条，唯一真源
    values-es|fil|hi|in|pt-rBR|ru/   现有 6 个语种（各约 2178 条）
    values-zh/                ← 目标目录，尚未创建
  assets/JavaScript/          注入脚本，无用户可见英文，不要动
  assets/translations/        Mozilla 离线翻译模型，勿动
PLAN/PLAN_1..9.md             ★ 汉化计划，唯一契约（见第 4 节）
tools/                        ← 计划中要建的校验脚本（尚未创建）
native/                       Rust/C++ 屏蔽引擎
fastlane/metadata/android/    商店文案（en-US/es/fil/ru，无 zh）
```

---

## 3. 翻译工作的技术事实（已核实，不要推翻重查）

| 事实 | 数值 / 位置 |
|---|---|
| 需翻译字符串 | **2178** 条（2184 减去 6 条 `translatable="false"`） |
| 复数 | 25 组 / 50 个 item |
| 现有语种 | `values-es` `values-fil` `values-hi` `values-in` `values-pt-rBR` `values-ru`，**无中文** |
| 位置占位符 | 188 条含 `%1$s` / `%1$d` |
| 非位置占位符 | 29 条 + 3 组复数仍用 `%s`/`%d`，计划在 PLAN_2 重构为位置参数 |
| 语言白名单 | `LocaleHelper.kt:21-28`，不在名单内的 tag 一律回退英文 |
| 语言列表 | `LanguageUtils.kt:9-17` |
| 语言名称字符串 | `values/strings.xml` 第 236–246 行 `language_name_*` |
| Context 挂载点 | `ClintApplication` / `ClintActivity:55` / `BackgroundPlaybackService:54` / `DownloadForegroundService:65` |
| 切换语言 | `ClintActivity.captureAndApplyLanguage()`（:167），写 prefs 后 `recreate()` |
| 自定义字体 | 无 `res/font`，中文走系统字体，无豆腐块风险 |
| 设置搜索 | 匹配 `getString()` 结果，中文搜索无需额外开发 |
| Lint | 仓库无 `lint.xml`、无 `lint {}` 配置；CI 只跑 `assembleGithubRelease` |
| 硬编码界面文案 | 仅 2 处剪贴板 ClipData 标签，不在界面显示 |

---

## 4. 工作方式：以 PLAN/ 为契约

**一次会话只做一个批次。** 新对话开工流程：

1. 读 `PLAN/PLAN_1.md`（总纲：术语表、10 条硬规则、禁译清单、进度台账）。
2. 读用户指定的那一份 `PLAN_N.md`（范围、特殊条目、参考译法、完成判据）。
3. `git status --short` 确认工作区干净（应只有 `PLAN/` 未跟踪）。
4. 若用户没说做哪一批，看 `PLAN_1` 第 8 节台账里第一个 ⬜ 的条目。

收工必做：跑校验命令 → 更新 `PLAN_1` 第 8 节台账（状态 / commit / 遗留）→ 告知下一份 PLAN。

| 文件 | 内容 | 条目 |
|---|---|---|
| PLAN_1 | 总纲、术语表、规则、台账 | — |
| PLAN_2 | 骨架 + 两个脚本 + 占位符重构（必须先做） | 32 处重构 |
| PLAN_3 | B1 通用动作 / 设置导航 / 对话框 | 332 + 3 复数 |
| PLAN_4 | B2 外观主题 + B5 媒体权限 | 234 + 104 |
| PLAN_5 | B3 下载管理器（内分 5 块） | 440 + 13 复数 |
| PLAN_6 | B4 标签页书签历史 + B8 备份关于 | 186 + 194 |
| PLAN_7 | B6 隐私 / 网站屏蔽 / 过滤列表 | 354 |
| PLAN_8 | B7 脚本 / 翻译 / 数据 + 全量终检 | 334 + 5 复数 |
| PLAN_9 | 手工验收 + PR 准备 | — |

---

## 5. 铁律

**必须：**
- 占位符 `%1$s`/`%1$d` 原样保留，编号与类型不变；字面百分号写 `%%`
- 转义原样：`\n` `\u2026` `\u2192` `\u2014` `&amp;` `&lt;`；中文不含撇号，别照抄 `\'`
- 复数只写 `<item quantity="other">`（中文按 CLDR 只有 other）
- key 顺序、注释、`translatable` 属性与源文件逐行对应，不重排
- 术语以 `PLAN_1` 第 5 节为准，新词先补表
- 全角标点；中文与数字间不加空格；按钮 2–4 字；设置项标题 ≤ 12 字不加句号

**禁止：**
- 翻译 `about_license_text`（GPL 正文）、品牌名（Quiver Guard / MEGA / Material You）、URL、许可证名
- 改动 `translation/` 与 `assets/translations/`（那是网页翻译模型，与界面语言无关）
- 改动 `assets/JavaScript/`（无用户可见英文）
- 提交 `build/` `.gradle/` `.kotlin/` `local.properties`
- 未确认就 `push`、提 PR、改上游可见的分支

---

## 6. 常用命令

```bash
# 校验（PLAN_2 建好后可用）
python tools/i18n_scope.py B3 --stat          # 某批覆盖率
python tools/i18n_scope.py --all --stat       # 全库 2178 分母
python tools/check_i18n.py --locale zh        # 9 项断言
python tools/check_i18n.py --locale zh --allow-missing   # 分批阶段用

# 构建
./gradlew :app:assembleGithubDebug
./gradlew :app:assembleFossDebug
```

本机 Windows + bash，路径用正斜杠。Python 可用（校验脚本用它写）。

---

## 7. 当前状态（2026-11-16）

- 分支 `main`，工作区干净；`PLAN/` 未跟踪（默认不入库、不进上游 PR）
- 已完成：上游 v1.2.6 拉取、`.gitignore` 恢复（`7ed7b75`，修掉了上游 v1.0.8 误删导致构建产物外露的问题）
- **尚未开始**：`values-zh` 目录、语言注册、任何译文（进度 0/2178）
- 阻塞项：本机未装 SDK Platform 37（现有 35/36），`assembleDebug` 会报找不到 android-37
- 待用户拍板（`PLAN_1` 第 11 节）：目录用 `values-zh` 还是 `values-zh-rCN`、是否做繁体、是否提上游 PR、`localeConfig` 是否加

---

## 8. 沟通约定

- 用户说「按 PLAN_5 做」就是要执行 B3，不要重新规划；计划有问题先提出再动手。
- 汇报用中文，简短；贴实际命令输出，不要转述。
- 不确定的术语或口径先问，不要自创第二套译法。
