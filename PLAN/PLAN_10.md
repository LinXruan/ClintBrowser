# PLAN_10 — 全局刷新率同步（v1.2.7 / versionCode 47）

> 会话 S9 · 前置：PLAN_9（汉化收尾）已完成
> 目标：应用在可见时始终跑在「系统允许的最高刷新率」，滚动/动画不再被 60Hz 拖住。
> **无开关、默认常开**；安全性靠内建约束而不是用户手动关闭。

---

## 1. 现状调查（已核实）

| 检查项 | 结果 |
|---|---|
| `refreshRate` / `preferredRefreshRate` / `setFrameRate` / `FRAME_RATE_` / `Display.Mode` / `preferredDisplayModeId` | 全库 **0 命中** |
| `Choreographer` 限帧 / 固定 16ms 循环 | 无 |
| 自定义 `SurfaceView` / `TextureView` 渲染 | 无（视频预览走系统组件） |
| `android:hardwareAccelerated` | `true`（application 级） |
| 窗口 `preferredRefreshRate` | 未设置，保持默认 0（= 不表态） |
| SDK 37 的帧率 API 现状 | `View.setRequestedFrameRate` ✅、`LayoutParams.preferredRefreshRate` ✅、`Window.setFrameRate` ❌（已移除） |

结论：

1. 应用**没有把帧率写死 60**，也没有降帧逻辑。
2. 但它**完全不向系统表态**：窗口 vote 为空，`DisplayModeDirector` 只能取显示器默认 mode。多数 OEM 的默认 mode 是 60Hz 省电档，于是观感就是「锁 60」；开了高刷的机器又会自己跑到 120——同一份代码在不同机器上表现不一致。
3. 渲染侧没有瓶颈：WebView 走 Chromium 合成器 + 应用 RenderThread，Compose 走 vsync，窗口给多少 Hz 就能跑多少。

→ 唯一要补的就是「窗口层刷新率 vote」这一环。

---

## 2. 方案取舍（为什么是这个做法）

### 2.1 语义定义

「自动同步刷新率」= **申请显示器支持的最高刷新率，把最终决定权交给系统**。

两句话解释清楚，避免自相矛盾：

- 应用只负责「申请」：`setFrameRate(maxRate, FIXED_SOURCE)` / `preferredRefreshRate = maxRate`。
- 系统仍可覆盖：省电模式、`peak_refresh_rate`（显示设置里的高刷开关）、开发者选项的峰值限制，都在 DisplayModeDirector 层优先于应用 vote。

所以实际结果 = `min(面板最高, 系统允许的最高)` —— 用户把系统设成 60 就还是 60，开了 120 就吃满 120。这正是「同步」，而不是「强行锁 120」。

### 2.2 为什么不做开关

用户明确要求常开。因此把安全性做进实现，而不是做成一个没人会关的开关：

| 安全阀 | 规则 |
|---|---|
| 面板本来只有 60 | 目标 ≤ 60 时**完全不调用**任何 API（no-op，零副作用） |
| 省电模式 | `PowerManager.isPowerSaveMode` 为真 → 不投票，交还系统 |
| 系统限制更高优先 | 只「申请」，不绕过 `peak_refresh_rate`，不重试、不循环拉高 |
| 目标未变 | 记住上次 apply 的值，相同则跳过，避免重复触发模式切换（防闪屏） |
| 任何异常 | 全链路 try/catch，失败静默降级；宁可退回 60 也不崩、不弹窗 |

### 2.3 三层 API 阶梯（按系统版本取最优，全部降到 minSdk 26 可用）

| 系统 | 手段 | 说明 |
|---|---|---|
| API 35+ | `window.decorView.setRequestedFrameRate(rate)` | Android 15 新增的 View 级请求，粒度最细、最不容易触发整窗模式切换 |
| API 26+（全版本） | `window.attributes.preferredRefreshRate = rate` | 旧但有效的 legacy vote，多数 OEM 只认这条 |

> **SDK 37 实测结论**：`Window.setFrameRate(float, int)` 与 `LayoutParams.FRAME_RATE_COMPATIBILITY_*` 已从 API 37 的 android.jar 中移除（编译期 unresolved），`View.setRequestedFrameRate` 与 `LayoutParams.preferredRefreshRate` 仍在。因此不调用 Window 版，也不做反射，避免版本差异带来的运行时风险。

两条路径各写一次：API 35+ 先走 View 级请求，再写一次 `preferredRefreshRate` 兜底（多写无副作用）。

### 2.4 何时生效

- `ClintActivity.onCreate`：bind 并首次 apply（26 个 Activity 全继承，一处挂载全局生效）。
- `onResume`：再 apply 一次（切后台回来、从设置页返回都能纠正被系统降下来的模式），目标未变则内部跳过。
- `DisplayManager.DisplayListener#onDisplayChanged`：系统切 60↔120、插拔外接屏、旋转时重算并重新 apply。
- `onDestroy`：注销监听。

### 2.5 明确不做的「暴力手段」

- 不调用隐藏 API（`setPreferredDisplayModeId` 需要系统权限）。
- 不用 `Surface.setFrameRate` 直接怼 WebView 的 surface（拿不到、也不该拿）。
- 不写死 120/90：只从 `display.supportedModes` 里取真实存在的值。
- 不在后台或不可见窗口投票。

---

## 3. 新增文件清单

| 路径 | 预估行数 | 职责 |
|---|---|---|
| `app/src/main/java/com/jhaiian/clint/util/RefreshRateSync.kt` | ~170 | 读 mode、算目标、分级 apply、监听 display 变化、异常降级 |

接口：

```kotlin
internal object RefreshRateSync {
    fun bind(activity: Activity)      // onCreate / onResume
    fun unbind(activity: Activity)    // onDestroy
    fun apply(activity: Activity)     // 内部使用，也可供 setup 完成等时机调用
}
```

关键实现点：

```kotlin
// 目标速率
val display = activity.display ?: return
val max = display.supportedModes.maxOfOrNull { it.refreshRate } ?: display.refreshRate
if (max < 60f) return                       // 60Hz 设备：完全不介入

// 省电模式不投票
if (powerManager.isPowerSaveMode) return

// API 35+
if (Build.VERSION.SDK_INT >= 35) rootView.setRequestedFrameRate(max)

// API 30+
if (Build.VERSION.SDK_INT >= 30) window.setFrameRate(max, FRAME_RATE_COMPATIBILITY_FIXED_SOURCE)

// 全版本兜底（OEM 兼容）
window.attributes = window.attributes.apply { preferredRefreshRate = max }
```

去重：`WeakHashMap<Activity, Float>` 记录上次应用值，相同直接 return；`unbind` 时清理。

## 4. 修改清单

| 文件 | 改动 | 行数 |
|---|---|---|
| `base/ClintActivity.kt` | `onCreate` 末尾 `RefreshRateSync.bind(this)`；`onDestroy` `RefreshRateSync.unbind(this)` | +4 |
| `app/build.gradle.kts` | `versionCode = 47`、`versionName = "v1.2.7"` | 2 行改值 |
| `CHANGELOG.md` | 顶部新增 `# v1.2.7` 段 | +12 |

**删除清单**：无。
**新增文案**：无（不加设置项，不动 `strings.xml`，i18n 数字保持 2185/2179）。

---

## 5. 执行步骤

1. 写 `RefreshRateSync.kt`，先在 `MainActivity` 临时验证帧率是否真的上去。
2. 挪到 `ClintActivity`，确认 26 个 Activity 全继承、无崩溃。
3. 加 `DisplayListener`，验证系统切 60/120 后自动跟随。
4. 加省电模式判断与去重逻辑。
5. 升版本号 + 写 CHANGELOG。
6. 跑校验（§6）。

---

## 6. 校验

```bash
python tests/i18n_scope.py --all --stat     # 仍为 2179/2179（本批不加文案）
python tests/check_i18n.py --locale zh      # 无 FAIL
./gradlew :app:assembleGithubDebug          # BUILD SUCCESSFUL
```

完成判据（3 条）：

- [ ] 真机滚动时窗口刷新率 = 系统允许的最高值（60Hz 设备上无任何行为变化）
- [ ] 26 个 Activity 进出无崩溃；切后台回前台、系统切 60/120 均能跟上
- [ ] `check_i18n` 与 `assembleGithubDebug` 通过

---

## 7. 真机验证（3 条）

```bash
# 1) 当前活跃 mode
adb shell dumpsys SurfaceFlinger | grep -iE 'active mode|refresh' | head

# 2) 找出应用 layer 并测帧间隔（滚动页面时执行）
adb shell dumpsys SurfaceFlinger --list | grep -i clint
adb shell dumpsys SurfaceFlinger --latency '<上一步的 layer 名>' | head -20
#   帧间隔 ≈16.6ms → 60Hz；≈8.3ms → 120Hz

# 3) 开发者选项 → 显示刷新率（叠加实时 Hz），开关前后对比
```

---

## 8. 风险与回退

| 风险 | 处理 |
|---|---|
| 120Hz 常驻增加耗电 | 只在窗口可见时投票；系统省电模式自动不投票；不硬编码超过面板的值 |
| 模式切换瞬间闪屏（个别 ROM） | 去重（目标未变不调用）+ 优先用 API 35 的 View 级接口 |
| 个别 ROM `setFrameRate` 抛异常 | try/catch 降级为只写 `preferredRefreshRate`；再失败则 no-op |
| 视频/24fps 内容被强行 120 导致抖动 | Chromium 自会为视频 surface 设帧率，窗口 vote 只影响 UI 合成；真机若发现抖动，对该 Activity 跳过（预留一个 `skipActivities` 集合） |
| 分屏/多显示器 | 用 `activity.display`，为空直接 return |
| 回退 | 删 `RefreshRateSync.kt` + 还原 `ClintActivity` 两行；无数据迁移、无残留偏好 |

---

## 9. 不做的事

- 不改 WebView 渲染管线、不加 `setLayerType`。
- 不做手动档位（锁 90/120）、不做「省电时降 60」的自定义策略——交给系统。
- 不引入第三方库；不动 `native/`、`assets/`。

---

## 10. 交接

- 完成后在 `PLAN/PLAN_1.md` 台账新增 S9 行并标 ✅。
- 版本 `v1.2.7` / `47`，提交前缀 `feat(display): ...`。
