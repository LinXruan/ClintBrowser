# Clint Browser 调试手册（DEBUG.md）

构建、安装、启停、日志、UI 抓取的实测命令与已知坑。工程约定见 [AGENTS.md](AGENTS.md)。

## 1. 环境

```bash
export PATH="$LOCALAPPDATA/Android/Sdk/platform-tools:$PATH"
export MSYS_NO_PATHCONV=1      # Git Bash 必加，否则 /sdcard 会被改写成 D:/...
adb devices
adb shell getprop ro.product.cpu.abi      # 决定装哪个 ABI 包
```

- SDK 在 `%LOCALAPPDATA%\Android\Sdk`，平台目录是 `android-37.0`。
- `local.properties` 缺 `sdk.dir` 时构建报 `SDK location not found`。
- 设备由用户提供；**不要卸载已装版本，也不要 `pm clear`**（会清数据），覆盖安装用 `install -r`。

## 2. 构建与安装

| 目的 | 命令 |
|---|---|
| debug（github） | `./gradlew :app:assembleGithubDebug` |
| debug（foss） | `./gradlew :app:assembleFossDebug` |
| 只验证资源 | `./gradlew :app:processGithubDebugResources` |
| 停止守护进程 | `./gradlew --stop` |

产物在 `app/build/outputs/apk/github/debug/`，每个 ABI 一个包 + 一个 universal。

```bash
adb install -r app/build/outputs/apk/github/debug/app-github-arm64-v8a-debug.apk
```

> [!WARNING]
> `app-github-universal-debug.apk` 装机启动即崩：
> `ClassNotFoundException: com.jhaiian.clint.app.ClintApplication`（包内 22 个 dex）。
> 与代码无关，装对应 ABI 包即可。

## 3. 启动与停止

| 项 | 值 |
|---|---|
| 包名 | `com.jhaiian.clint.debug` |
| 主界面 | `com.jhaiian.clint.browser.MainActivity` |
| 首次启动 | `com.jhaiian.clint.setup.SetupActivity`（引导页） |

```bash
adb shell am start -n com.jhaiian.clint.debug/com.jhaiian.clint.browser.MainActivity
adb shell am force-stop com.jhaiian.clint.debug
adb shell dumpsys activity activities | grep -m1 topResumedActivity
adb shell pidof com.jhaiian.clint.debug
```

`monkey -p com.jhaiian.clint` 会报 `No activities found`——包名少了 `.debug`。

## 4. 日志

```bash
adb logcat -c
adb logcat -b crash -d | tail -40
adb logcat -d | grep -E 'AndroidRuntime|FATAL' | tail -30

PID=$(adb shell pidof com.jhaiian.clint.debug | tr -d '\r')
adb logcat -d --pid=$PID | tail -100
```

## 5. UI 抓取与操作

```bash
adb shell uiautomator dump /sdcard/ui.xml
adb shell cat /sdcard/ui.xml

# 可见文本
adb shell cat /sdcard/ui.xml | tr '>' '\n' | grep -o 'text="[^"]*"' | grep -v 'text=""'

# 文本 + 坐标（用于点击）
adb shell cat /sdcard/ui.xml | tr '<' '\n' \
  | grep -oE 'text="[^"]+"[^>]*bounds="[^"]+"' | sed 's/ class=.*bounds=/ /'

adb shell input tap 540 2000
adb shell input keyevent 4        # 返回
```

- dump 前 `sleep 1`，Compose 动画没结束会抓到半屏。
- 同一文本可能出现多次，按 `bounds` 判断点哪个。
- 偶发 `could not get idle state`，重试一次即可。

## 6. 报错对照表

| 现象 | 原因 | 处理 |
|---|---|---|
| `Unable to access jarfile .../gradle-wrapper.jar` | 上游不提交该 jar，CI 现生成 | 用缓存分发跑一次 `gradle wrapper --gradle-version 9.8.1 --distribution-type bin`（临时空目录执行后拷回），或照 `.github/workflows/build.yml` 的 Provision 步骤 |
| `SDK location not found` | 缺 `local.properties` | 补 `sdk.dir` |
| `Failed to find target with hash string 'android-37'` | 平台目录是 `android-37.0`，或没装 | `sdkmanager "platforms;android-37.0"` |
| `Could not close incremental caches ... source-to-classes.tab` | Kotlin 增量缓存损坏 | `./gradlew --stop` → `rm -rf app/build/kotlin` → 重跑 |
| `:app:processGithubDebugJavaRes FAILED` 无明细 | 偶发（文件被索引/杀毒占用） | 原命令重跑一次 |
| `Android resource compilation failed` | 资源转义错误（裸 `&`、`<`、未配对 `%`） | 修 `values*/strings.xml` 对应值，或先跑 `processGithubDebugResources` 定位 |
| 启动即崩 `ClassNotFoundException` | 装的是 universal 包 | 换 ABI 包 |
| 构建长时间无输出（~7 分钟） | 首次 dex/NDK 处理 | 正常，等它跑完 |

## 7. 清理

```bash
./gradlew --stop
rm -rf app/build/kotlin     # 只清 Kotlin 增量缓存
rm -rf app/build            # 全量产物
```

`build/`、`.gradle/`、`.kotlin/`、`local.properties` 均已 ignore，提交前 `git status` 确认。
不要同时跑多份 `assemble`，共用一个 daemon 抢锁，容易触发上面的增量缓存报错。
