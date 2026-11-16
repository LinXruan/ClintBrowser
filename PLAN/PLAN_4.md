# PLAN_4 — B2 外观与主题 + B5 媒体与权限

> 会话 S3 · 234 + 104 = 338 条字符串 · 前置：PLAN_3 完成
> 两个子批各自可独立收工；上下文吃紧时先交 B2，B5 留到下一次。

---

## 1. 目标（可验证）

1. 外观设置页、主题编辑器的所有标签、分组名、说明文字中文，且**配色名不重名、长度统一**。
2. 媒体嗅探面板（视频/音频/字幕列表）全部中文。
3. 网站权限弹窗（摄像头、麦克风、定位、通知、剪贴板、语音）全部中文，句式统一。
4. `i18n_scope.py B2 --stat` = 234/234，`B5 --stat` = 104/104。

---

## 2. 界面清单

### B2（234）

| 界面 | 入口 | 前缀 | 条数 |
|---|---|---|---|
| 配色选择器 | 设置 → 外观 → 强调色 | `accent_*` | 101 |
| 自定义主题编辑器 | 设置 → 外观 → 自定义主题 | `custom_theme_*` | 78 |
| 自定义搜索引擎 | 设置 → 浏览器 → 搜索引擎 → 自定义 | `custom_search_*` | 14 |
| 主题明暗 | 设置 → 外观 → 主题 | `theme_*` | 6 |
| 表面强度 | 设置 → 外观 → 表面强度 | `surface_*` | 12 |
| 自定义主题列表 | 外观 → 我的主题 | `custom_themes_*` | 3 |
| 其他 | — | `custom_select` `custom_js` `custom_http` `custom_ssl` `custom_date` `custom_color` `custom_user` `color_*` `frameless_*` | 20 |

### B5（104）

| 界面 | 入口 | 前缀 | 条数 |
|---|---|---|---|
| 媒体嗅探面板 | 页面内浮层 / 长按媒体 | `media_capture_*` | 46 |
| 图片长按菜单 | 长按图片 | `image_*` | 10 |
| 剪贴板权限 | 网页请求剪贴板 | `clipboard_*` | 8 |
| 后台播放 | 长按视频 → 后台播放 | `background_*` | 7 |
| 摄像头权限 | 网页请求摄像头 | `camera_*` | 6 |
| 文档查看 | 打开 PDF 等 | `document_*` | 6 |
| 定位权限 | 网页请求定位 | `location_*` | 5 |
| 通知权限 | 网页请求通知 | `notification_*` | 5 |
| 语音输入 | 输入框语音 | `voice_*` | 4 |
| 麦克风权限 | 网页请求麦克风 | `mic_*` | 3 |
| 电池优化 | 设置 → 后台限制 | `battery_*` | 2 |
| 截图 | 长按菜单 | `screenshot_*` | 2 |

---

## 3. 配色命名规范（B2 的核心难点）

101 条 = 50 个色名 + 50 条描述 + `section_presets`。

### 3.1 命名规则
- 色名 **2–4 字**，能读出颜色，不用「色」结尾（除非单字色：紫色、红色、绿色、蓝色、黄色、橙色、粉色）
- 宝石/材质类直译：Ruby 红宝石、Emerald 祖母绿、Amethyst 紫水晶、Onyx 黑玛瑙、Obsidian 黑曜石、Graphite 石墨、Titanium 钛灰、Copper 铜色
- 深浅修饰放前面：Deep Purple 深紫、Deep Orange 深橙
- 品牌词不译：Material You 保留原文
- **全表禁止重复**：译完用 `grep -o '<string name="accent_[a-z_]*">[^<]*' | cut -d'>' -f2 | sort | uniq -d` 查重

### 3.2 色名对照

| key | 英文 | 建议 |
|---|---|---|
| `accent_default` | Monochrome | 单色 |
| `accent_material_you` | Material You | Material You |
| `accent_purple` | Purple | 紫色 |
| `accent_deep_purple` | Deep Purple | 深紫 |
| `accent_royal_purple` | Royal Purple | 宝紫 |
| `accent_amethyst` | Amethyst | 紫水晶 |
| `accent_lavender` | Lavender | 薰衣草 |
| `accent_violet` | Violet | 紫罗兰 |
| `accent_plum` | Plum | 梅子紫 |
| `accent_indigo` | Indigo | 靛蓝 |
| `accent_teal` | Teal | 青碧 |
| `accent_azure` | Azure | 天青 |
| `accent_cyan` | Cyan | 青色 |
| `accent_sky` | Sky | 天蓝 |
| `accent_mint` | Mint | 薄荷绿 |
| `accent_sage` | Sage | 鼠尾草绿 |
| `accent_forest` | Forest | 森林绿 |
| `accent_emerald` | Emerald | 祖母绿 |
| `accent_olive` | Olive | 橄榄绿 |
| `accent_lime` | Lime | 青柠 |
| `accent_amber` | Amber | 琥珀 |
| `accent_gold` | Gold | 金色 |
| `accent_mustard` | Mustard | 芥末黄 |
| `accent_lemon` | Lemon | 柠檬黄 |
| `accent_sand` | Sand | 沙色 |
| `accent_sepia` | Sepia | 棕褐 |
| `accent_terracotta` | Terracotta | 赤陶 |
| `accent_copper` | Copper | 铜色 |
| `accent_coral` | Coral | 珊瑚 |
| `accent_peach` | Peach | 蜜桃 |
| `accent_apricot` | Apricot | 杏色 |
| `accent_tangerine` | Tangerine | 橘橙 |
| `accent_orange` / `deep_orange` | Orange / Deep Orange | 橙色 / 深橙 |
| `accent_crimson` | Crimson | 绯红 |
| `accent_ruby` | Ruby | 红宝石 |
| `accent_scarlet` | Scarlet | 猩红 |
| `accent_burgundy` | Burgundy | 勃艮第红 |
| `accent_red` | Red | 红色 |
| `accent_pink` | Pink | 粉色 |
| `accent_slate` | Slate | 石板灰 |
| `accent_graphite` | Graphite | 石墨灰 |
| `accent_charcoal` | Charcoal | 炭黑 |
| `accent_obsidian` | Obsidian | 黑曜石 |
| `accent_onyx` | Onyx | 黑玛瑙 |
| `accent_titanium` | Titanium | 钛灰 |
| `accent_midnight` | Midnight Blue | 午夜蓝 |

### 3.3 描述句式（50 条统一模板）

英文是「{形容} {色系} tones across the UI」，中文统一为「界面整体采用**{形容}{色系}**色调」。示例：

| 英文 | 中文 |
|---|---|
| Neutral grayscale tones across the UI | 界面整体采用中性灰色调 |
| Cool violet tones across the UI | 界面整体采用冷色调紫罗兰色 |
| Deep near-black tones with a cool undertone across the UI | 界面整体采用偏冷调的近黑色 |
| Rich, vivid jewel-tone purple across the UI | 界面整体采用浓郁的宝石紫 |
| Warm neutral beige tones across the UI | 界面整体采用暖调米色 |

> 统一「采用…色调」句式后，50 条读起来才像一个产品，而不是 50 个人翻的。

---

## 4. 特殊条目

### B5 权限句式（5 条，已重构为 `%1$s`）

| key | 英文 | 建议 |
|---|---|---|
| `camera_web_request_message` | %1$s wants to use your camera. | %1$s 想要使用你的摄像头 |
| `mic_web_request_message` | %1$s wants to use your microphone. | %1$s 想要使用你的麦克风 |
| `location_web_request_message` | %1$s wants to access your location. | %1$s 想要获取你的位置信息 |
| `notification_web_request_message` | %1$s wants to send you notifications. | %1$s 想要向你发送通知 |
| `clipboard_web_request_message` | %1$s wants to see text on your clipboard. | %1$s 想要读取你的剪贴板内容 |

配合 `*_web_request_remember` = 「不再询问」、`clipboard_web_request_origin_unknown` = 「本网站」，三者要在同一句里读通。

### 转义

| key | 特征 | 处理 |
|---|---|---|
| `media_capture_scanning` | `Scanning this page for media\u2026` | `正在扫描本页媒体\u2026` |
| `media_capture_{video,audio,subtitle}_preview_error` | `Couldn\u2019t …\nPlease …` | 中文用「无法…。\n请…」，保留 `\n` |
| `document_viewer_error` | 同上 | 同上 |
| `battery_opt_rationale_message`（211 字符） | 长段说明 | 分句译，保留末尾无句号风格 |

### 长文本
- `battery_opt_rationale_message` 211 字符，是本批唯一需要通读的长句，注意不要漏掉「允许后台运行」的因果。

---

## 5. 本批术语

| 英文 | 中文 |
|---|---|
| Accent / Accent color | 强调色 |
| Surface intensity | 表面强度 |
| Presets | 预设 |
| Slot（主题色槽） | 色槽 |
| Stream | 流 |
| Segment | 分片 |
| Quality | 画质 |
| Subtitle | 字幕 |
| Preview | 预览 |
| Scan | 扫描 |
| Background playback | 后台播放 |
| Story / 无 | — |

---

## 6. 操作步骤

1. B2 分三段：`accent_*`（101）→ `custom_theme_*`（78）→ 剩余 55。
2. 每段写完跑一次 `check_i18n.py --locale zh --allow-missing`。
3. 色名用 §3.2 表格直接落，描述用 §3.3 模板批量套。
4. B5 按 §2 表格顺序，46 条媒体面板优先（用户感知最强）。
5. 编译 + 在设备上看一次配色选择器（重点：色名换行、描述两行是否溢出）。

---

## 7. 校验

```bash
python tools/i18n_scope.py B2 --stat
python tools/i18n_scope.py B5 --stat
python tools/check_i18n.py --locale zh --allow-missing
```

手动附加检查（色名查重）：

```bash
python - <<'PY'
import re
s=open('app/src/main/res/values-zh/strings.xml',encoding='utf-8').read()
names=re.findall(r'<string name="accent_[a-z_]+">([^<]+)</string>',s)
dup={n for n in names if names.count(n)>1}
print('duplicates:',dup)
print('count:',len(names))
PY
```

---

## 8. 完成判据

- [ ] `B2 --stat` = 234/234，`B5 --stat` = 104/104
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL；上面那段色名查重输出 `duplicates: set()`
- [ ] 提交：`i18n(zh): appearance and custom theme` + `i18n(zh): media capture and permission prompts`

---

## 9. 本批独有的坑

| 坑 | 说明 |
|---|---|
| 色名与描述重复翻译 | `accent_x` 与 `accent_x_desc` 是两条，别把描述写成色名 |
| 「靛蓝」「天青」这类词认知度低 | 保留但在描述里补一句通俗说明（如“冷调蓝紫”） |
| 权限句式混用「您的/你的」 | 全篇统一「你的」 |
| 媒体面板 `media_capture_menu_stream` 译成「直播」 | Stream 此处指媒体流，不是直播 |
| `custom_theme_slot_on_primary` 直译成「主色上的文字」 | 建议「强调色上的文字」，与 accent=强调色 对齐 |

---

## 10. 交接

- 下一步：`PLAN_5.md`（B3 下载 440 + 13 组复数，最大的一批）。
- 交接前确认 `values-zh` 中 accent 段完整，否则 PLAN_5 与外观无关但会出现在同一文件里，容易误改。
