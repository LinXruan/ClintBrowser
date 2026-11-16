package com.jhaiian.clint.util

import android.app.Activity
import android.content.Context
import android.hardware.display.DisplayManager
import android.os.Build
import android.os.PowerManager
import java.lang.ref.WeakReference
import java.util.WeakHashMap

/**
 * 让窗口申请显示器支持的最高刷新率。
 *
 * 只「申请」不「强制」：省电模式、系统里的高刷新率开关与峰值限制都在
 * DisplayModeDirector 层优先于应用投票，因此实际速率 = min(面板最高, 系统允许的最高)。
 *
 * 面板最高不超过 60Hz 时完全不介入，保证 60Hz 设备上的行为与旧版本一致。
 */
internal object RefreshRateSync {

    private const val MIN_INTEREST_HZ = 60f

    private val appliedRates = WeakHashMap<Activity, Float>()
    private val displayListeners = WeakHashMap<Activity, DisplayManager.DisplayListener>()

    /** onCreate / onResume 调用：首次申请并挂上显示器变化监听。 */
    fun bind(activity: Activity) {
        apply(activity)
        if (displayListeners.containsKey(activity)) return
        val displayManager = activity.getSystemService(Context.DISPLAY_SERVICE) as? DisplayManager ?: return
        val activityRef = WeakReference(activity)
        val listener = object : DisplayManager.DisplayListener {
            override fun onDisplayAdded(displayId: Int) = Unit
            override fun onDisplayRemoved(displayId: Int) = Unit
            override fun onDisplayChanged(displayId: Int) {
                val live = activityRef.get() ?: return
                if (currentDisplay(live)?.displayId == displayId) apply(live)
            }
        }
        runCatching { displayManager.registerDisplayListener(listener, null) }
            .onSuccess { displayListeners[activity] = listener }
    }

    /** onDestroy 调用：注销监听，避免持有 Activity。 */
    fun unbind(activity: Activity) {
        displayListeners.remove(activity)?.let { listener ->
            (activity.getSystemService(Context.DISPLAY_SERVICE) as? DisplayManager)
                ?.let { runCatching { it.unregisterDisplayListener(listener) } }
        }
        appliedRates.remove(activity)
    }

    /** 重新计算并申请；目标未变时直接返回，避免重复触发模式切换。 */
    fun apply(activity: Activity) {
        if (activity.isFinishing || activity.isDestroyed) return

        val display = currentDisplay(activity) ?: return
        val maxRate = runCatching { display.supportedModes?.maxOfOrNull { it.refreshRate } }.getOrNull()
            ?: runCatching { display.refreshRate }.getOrNull()
            ?: return

        if (maxRate < MIN_INTEREST_HZ) {       // 60Hz 面板：不介入
            appliedRates.remove(activity)
            return
        }
        if (isPowerSave(activity)) {           // 省电模式：交还系统决定
            appliedRates.remove(activity)
            return
        }
        if (appliedRates[activity] == maxRate) return

        val window = activity.window
        var applied = false

        // Android 15+：View 级帧率请求（Window.setFrameRate 已在 SDK 37 移除）
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.VANILLA_ICE_CREAM) {
            applied = runCatching { window.decorView.setRequestedFrameRate(maxRate) }.isSuccess || applied
        }
        // 全版本兜底：legacy vote，API 23 起有效，不少 ROM 只认这条路径
        applied = runCatching {
            val attrs = window.attributes
            attrs.preferredRefreshRate = maxRate
            window.attributes = attrs
        }.isSuccess || applied

        if (applied) appliedRates[activity] = maxRate
    }

    @Suppress("DEPRECATION")
    private fun currentDisplay(activity: Activity): android.view.Display? =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) activity.display
        else activity.windowManager.defaultDisplay

    private fun isPowerSave(activity: Activity): Boolean =
        (activity.getSystemService(Context.POWER_SERVICE) as? PowerManager)?.isPowerSaveMode == true
}
