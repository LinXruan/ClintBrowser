# 项目开发守则（Clint Browser / Kotlin + Compose Android）

> 给 AI Agent 的项目提示词。开工前通读；调试相关一律看 [DEBUG.md](DEBUG.md)。

## 0. 守则

- 改代码前先读相关文件，不要凭印象改。
- 遇到阻塞（构建失败、环境缺失、需求歧义）**立即停下汇报**，不要猜着改。
- 装真机、抓 UI、看日志前先读 [DEBUG.md](DEBUG.md)。
- 不擅自 push、开 PR、卸载应用或清除用户数据。
- 改完按 §5.6 跑验证，验证没过不要说「完成」。

## 1. 项目概况

| 项 | 值 |
|---|---|
| 应用 | Clint Browser —— Android 浏览器：多标签、广告/跟踪屏蔽（Quiver Guard）、媒体嗅探、下载管理器、用户脚本、本地网页翻译 |
| 技术栈 | Kotlin + Jetpack Compose（Material 3），少量注入 JS，Rust/C++ 屏蔽引擎 |
| 包名 | `com.jhaiian.clint`，debug 自动加后缀 `.debug` |
| 版本 | `versionName v1.2.6` / `versionCode 46`（`app/build.gradle.kts`） |
| 构建 | AGP 9.4.1、Gradle 9.8.1、`compileSdk = targetSdk = 37`、`minSdk = 26` |
| 上游 | `jhaiian/ClintBrowser`，GPLv3 |

## 2. 常用命令

| 目的 | 命令 |
|---|---|
| 编译 debug（github 渠道，日常用） | `./gradlew :app:assembleGithubDebug` |
| 编译 debug（foss 渠道） | `./gradlew :app:assembleFossDebug` |
| 只验证资源（最快查资源错误） | `./gradlew :app:processGithubDebugResources` |
| 发布包 | `./gradlew assembleGithubRelease` |
| 停 Gradle 守护进程 | `./gradlew --stop` |

## 3. 环境要点

- **JDK**：本机 21；工程 `jvmTarget = 17`，不要跟着改 21。
- **SDK**：`compileSdk = targetSdk = 37`，本机平台目录是 `platforms/android-37.0`（带 `.0`，不叫 `android-37`）。
- **`local.properties`**（gitignore）：至少要有 `sdk.dir`；release 签名读 `signingConfig.*`，缺了只出未签名包。
- **`gradle/wrapper/gradle-wrapper.jar`**：上游不提交，CI 每次现生成。本地缺它时 `./gradlew` 报 `Unable to access jarfile`，处理见 DEBUG.md §6。
- **远端**：本地未配置 remote；推分支、开 PR 都要用户同意。

## 4. 项目结构

```
app/src/main/java/com/jhaiian/clint/
  app/ base/            Application 与 Activity 基类
  browser/             主界面、地址栏、WebView 宿主、媒体
  tabs/                标签页、标签组、标签条
  bookmarks/ history/ shortcuts/
  downloads/           下载管理器、前台服务、MEGA 导入
  blocker/ privacy/ quiver/    网站屏蔽、隐私开关、Quiver Guard
  mediacapture/ userscripts/ translation/
  settings/ customtheme/ ui/theme/
  setup/ backup/ profiles/ crash/ update/ util/
app/src/main/res/
  values/strings.xml   英文源文件（唯一真源）
  values-<lang>/       各语种
app/src/main/assets/   JavaScript/ 注入脚本、translations/ 离线翻译模型
native/                Rust/C++ 屏蔽引擎，产物进 app/src/main/jniLibs
tools/                 辅助脚本（非主流程）
```

关键约束：

- 界面文案 100% 走 `stringResource` / `getString`，禁止硬编码中文或英文。
- `app/src/main/res/values/strings.xml` 是文案唯一真源；新增 key 同时补 `values-zh`（其余语种缺键自动回退英文）。
- `assets/JavaScript/`、`assets/translations/`、`native/` 由上游维护，不要改。
- 以下文件已很大，新逻辑另起文件，别继续往里塞：`ui/theme/ClintThemeResolver.kt`（4373 行）、`settings/SettingsPanes.kt`（1508）、`downloads/ClintDownloadManager.kt`（1380）、`browser/MainActivity.kt`（1359）。

## 5. 工程规范

### 5.1 文件规模

- 新增 Kotlin 文件 **≤300 行**；超了先拆。
- 既有大文件（见 §4）只减不增，新分支逻辑写进新文件。
- 单个 Composable 建议 ≤120 行，超了抽子组件。

### 5.2 分层与命名

- 一个包一个领域，禁止 `utils2`、`misc`、`common` 这类垃圾桶包。
- 文件按角色命名：`XxxScreen.kt` `XxxDialog.kt` `XxxManager.kt` `XxxStore.kt` `XxxHelper.kt` `XxxUtils.kt`。
- 包名小写、单数；Compose 组件首字母大写，与文件名一致。

### 5.3 单一真相

- 一个状态只存一份，其余表现现算派生。
- 禁止哨兵值承载第二语义（「空列表 = 全选」「-1 = 未选」）。
- 跨页共享状态用显式对象传递，不引入第三方状态管理库。

### 5.4 删除优先

- 重构必须删掉被取代的旧函数、旧字段、旧分支，不留双份实现。
- 不写兼容壳（`_legacy`、`_v2`、`Deprecated` 转发），直接改调用点。
- 删完全库 `grep` 确认无残留引用。

### 5.5 文案与资源

- 文案只进 `values/strings.xml`，值不得以 `@` 或 `?` 开头，裸 `&` / `<` 会让 aapt2 失败。
- 占位符保持 `%1$s` / `%1$d` 的编号与类型，`%%` 是字面百分号，不能吞。
- 复数只写 `other`；`\n`、`\u2026`、`&amp;`、`&lt;b&gt;` 等转义原样保留。
- 引号统一用「」，避免与 `\"` 纠缠。

### 5.6 验证

- 改 Kotlin 或资源：`./gradlew :app:assembleGithubDebug` 必须成功（改文案也要跑，aapt2 会查转义）。
- 本仓库**没有单元测试**，不要编造测试结论；验证手段是编译 + 真机目视。
- 涉及界面时装 ABI 包看一遍（不要装 universal，见 §6）。

### 5.7 提交

| 前缀 | 用途 |
|---|---|
| `feat(<模块>): ...` | 新功能 |
| `fix(<模块>): ...` | 缺陷修复 |
| `refactor(<模块>): ...` | 重构 |
| `chore(build): ...` `docs: ...` | 构建、文档 |

不提交：`build/`、`.gradle/`、`.kotlin/`、`local.properties`、`__pycache__/`、APK、keystore。

## 6. 构建与产物

| 项 | 值 |
|---|---|
| flavor | `github` / `foss`（`IS_FOSS = true`） |
| debug 包名 | `com.jhaiian.clint.debug` |
| ABI 拆分 | `arm64-v8a` `armeabi-v7a` `x86` `x86_64` + `universal` |
| 产物目录 | `app/build/outputs/apk/<flavor>/<buildType>/` |
| release | `isMinifyEnabled` + `isShrinkResources`，需 `local.properties` 签名 |

- **`app-github-universal-debug.apk` 装机必崩**（`ClassNotFoundException: com.jhaiian.clint.app.ClintApplication`）。装真机用对应 ABI 包。
- 首次全量构建约 7 分钟（dex + NDK 符号处理），增量十几秒，别误判卡死。

## 7. 调试

> [!IMPORTANT]
> 构建安装、启动停止、日志、UI 抓取、已知故障，全部收敛在 **[DEBUG.md](DEBUG.md)**。
> 动手前先读它，尤其 §2（装哪个包）和 §6（报错对照表）。
