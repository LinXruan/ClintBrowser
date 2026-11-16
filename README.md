<div align="center">

<img src="docs/icon.png" width="120" alt="Clint Browser 中文分支图标" />

# Clint Browser（中文分支）

**可定制的分层网络浏览工具**

轻量浏览器，支持媒体嗅探、广告拦截、下载管理器和多身份配置

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blueviolet.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%208.0%2B-blueviolet.svg)](https://developer.android.com)
[![Version](https://img.shields.io/badge/Version-1.2.7-blueviolet.svg)](https://github.com/LinXruan/ClintBrowser/releases)
[![Fork of](https://img.shields.io/badge/Fork%20of-jhaiian%2FClintBrowser-8B5CF6.svg)](https://github.com/jhaiian/ClintBrowser)

</div>

---

## 关于本仓库

> **这是 [jhaiian/ClintBrowser](https://github.com/jhaiian/ClintBrowser) 的非官方中文分支。**
>
> 由社区维护，与原作者没有隶属、赞助或背书关系。上游仍然是这个项目的主线：想要原版、最新功能或英文说明，请访问 [上游仓库](https://github.com/jhaiian/ClintBrowser)。
>
> 代码同样遵循 GPLv3，源码、修改记录和完整提交历史都在本仓库公开。

### 本仓库相对上游的改动

| 改动 | 说明 |
|---|---|
| 界面汉化 | 全部界面文案翻译为简体中文，保留占位符、复数与转义 |
| 全局刷新率同步 | 应用可见时申请屏幕支持的最高刷新率，滚动与动画不再固定在 60Hz；系统省电模式和刷新率上限仍然优先，60Hz 设备无变化 |
| 全新图标 | 黑底紫色渐变大写 `C`，同时用于应用图标和本 README |
| 独立安装包名 | `com.linxruan.clint.zh`，可与上游正式版同时安装，互不覆盖 |
| 独立更新源 | 应用内「检查更新」读取本仓库的 `Update/*.json`，不再跳转到上游 APK |

> **关于图标**：上游的名称、Logo、截图属于原作者的商标/专有资产，**不在 GPLv3 授权范围内**，因此本分支不再使用原 Logo，改为自行设计的图标。

英文版说明和完整的功能更新日志请见上游仓库：[README](https://github.com/jhaiian/ClintBrowser#readme) · [CHANGELOG](CHANGELOG.md)。

---

## 这是什么

一个开源 Android 浏览器：没有自建后端，具备常见浏览器的绝大多数功能，界面基于 Material 3 构建。

应用不收集任何数据，也不统计活跃用户数。

Clint 的目标是做一个功能更多、好看且高度可定制的 Android 浏览器：没有广告，没有付费墙，完全免费。

---

## 截图

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="fastlane/metadata/android/en-US/images/phoneScreenshots/1.jpg" width="180" alt="截图 1" /></td>
      <td align="center"><img src="fastlane/metadata/android/en-US/images/phoneScreenshots/2.jpg" width="180" alt="截图 2" /></td>
    </tr>
    <tr>
      <td align="center"><img src="fastlane/metadata/android/en-US/images/phoneScreenshots/3.jpg" width="180" alt="截图 3" /></td>
      <td align="center"><img src="fastlane/metadata/android/en-US/images/phoneScreenshots/4.jpg" width="180" alt="截图 4" /></td>
    </tr>
  </table>
</div>

---

## 功能

### 🎬 媒体嗅探

- 自动识别网页中的视频、音频与字幕流
- 支持普通视频、HLS/M3U8 与 DASH 流
- 在浏览器内直接下载嗅探到的媒体

### ⬇️ 下载管理器

- 多线程、多分片下载
- 暂停与续传
- 下载计划任务
- 限速
- 自定义下载目录
- 卡住的下载会自动暂停并重试

### 📜 用户脚本

- 从 URL 安装用户脚本，或用内置代码编辑器自己写
- 兼容 Tampermonkey 风格元数据（`@match`、`@include`、`@exclude`、`@require`、`@resource`、`@grant`）
- 支持 GM API，包括 `GM.setValue`/`GM.getValue`、`GM.xmlHttpRequest` 和 `GM.notification`
- 从 URL 安装的脚本会自动检查更新
- 随时启用或停用单个脚本

### 🎨 界面与定制

基于 **Material 3** 与 **Jetpack Compose** 构建，界面高度可定制。

- 50 种强调色
- 浅色与深色主题
- 5 档表面强度
- 合计 **500 种主题组合**

### 🛡️ Quiver Guard

- 内置广告与跟踪器拦截
- 外观过滤与网络过滤
- 多份过滤规则列表
- 按站点单独控制

### 🚫 网站屏蔽

- 屏蔽色情、赌博等不想要的网站类别
- 按类别划分的规则列表（滥用、广告、加密货币、毒品、诈骗、赌博等）
- 可自行添加要屏蔽的网站

### 👤 身份配置

- 同一网站可同时登录多个账号
- 每个身份拥有独立的 Cookie、登录状态与站点数据
- 新建标签页时选择身份
- 为每个身份设置名称与颜色

### 🔗 快捷方式

- 把任意网站添加到桌面，自定义名称与图标
- 无边框模式隐藏搜索栏和底栏，接近原生应用的观感
- 内置快捷方式管理器统一管理

### 🌐 浏览器

- 多标签浏览
- 无痕模式
- 阅读模式
- 桌面模式
- 弹窗拦截
- 流量节省

> 装上自己体验就好。

---

## 系统要求

- Android 8.0（API 26）及以上
- 系统 WebView

---

## 安装

从本仓库的 [Releases](https://github.com/LinXruan/ClintBrowser/releases) 页面下载最新 APK。

- 请选择与自己设备 ABI 对应的安装包（`arm64-v8a`、`armeabi-v7a`、`x86`、`x86_64`）。
- `universal` 包在本项目上存在启动崩溃问题，不建议安装。
- 包名与上游不同，因此**可以和上游版本同时安装**；两者数据互不影响。

---

## 参与贡献

欢迎提交代码、缺陷报告和功能建议。

- 与**本分支**相关的问题（汉化、刷新率、图标、包名）：请到[本仓库 Issues](https://github.com/LinXruan/ClintBrowser/issues) 反馈。
- 与原版功能相关的问题：请到[上游 Issues](https://github.com/jhaiian/ClintBrowser/issues) 反馈，避免重复。
- 提交代码改动前请先读 [AGENTS.md](AGENTS.md)，构建与调试见 [DEBUG.md](DEBUG.md)。

---

## 社区

上游社区（英文）：

- **Discord** – [discord.gg/4kUe4yPQ32](https://discord.gg/4kUe4yPQ32)
- **Reddit** – [reddit.com/r/ClintBrowser](https://reddit.com/r/ClintBrowser)

---

## 许可证

本项目源代码遵循 [GNU 通用公共许可证 v3.0（GPLv3）](LICENSE)。

「Clint」「Clint Browser」名称、上游 Logo、截图及相关品牌资产属于上游作者的商标或专有资产，**不在 GPL 授权范围内**，使用需获得原作者明确许可。本分支为非官方版本，已自行重绘图标，也不代表原作者的立场。

应用内使用的第三方库各自遵循其许可证，详见 [Attribution.md](Attribution.md)。

---

## 相关文档

- [更新日志](CHANGELOG.md)
- [隐私政策](PRIVACY_POLICY.md)
- [服务条款](TERMS_OF_SERVICE.md)
- [贡献者名单](Contributors.md)
