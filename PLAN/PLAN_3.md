# PLAN_3 — B1：通用动作、设置导航与对话框

> 会话 S2 · 333 条字符串 + 3 组复数（6 项）· 前置：PLAN_2 完成（目录、脚本、占位符重构）
> 本批是「骨架 PR 可提」的最后一块：翻完它，中文版已经能日常使用。

---

## 1. 目标（可验证）

1. 设置首页 15 个分类入口、长按菜单、工具栏动作、主页、快捷方式管理全部中文。
2. 通用按钮（返回/前进/首页/分享/关闭/保存/确定/取消）无遗漏。
3. 对话框骨架（标题+内容+两个按钮）全部中文，按钮不被截断。
4. 覆盖率：`python tests/i18n_scope.py B1 --stat` 显示 333/333。

---

## 2. 界面清单

| 界面 | 入口 | 主要前缀 |
|---|---|---|
| 设置首页 | 设置 → 分类列表 | `pref_category_*`（15） |
| 各设置页标题/描述 | 设置内所有页面 | `pref_*`（42） |
| 长按/溢出菜单 | 工具栏 ⋮、长按标签页、长按链接 | `menu_*`（29）、`action_*`（26） |
| 主页 | 首页 | `home_*`（24） |
| 桌面快捷方式管理 | 设置 → 快捷方式 | `shortcut_*`（21） |
| 地址栏 | 顶部输入框 | `address_*`（10） |
| 搜索建议 | 输入时的建议列表 | `suggestions_*`（11）、`suggestion_*`（4） |
| 通用对话框 | 各处 | `popup_*`（10） |
| 日期/时间选择 | 下载计划、历史筛选 | `date_*`（11） |
| 其他零散 | 各处 | `open` `clear` `choose` `create` `check` `hide` `view` `skip` `install` `exit` `link` `search` `settings` `language` `app` `look` `misc` `refresh` `restart` `remember` `default` 及 15 个单词键 |

---

## 3. 条目明细

| 前缀 | 条数 | 前缀 | 条数 | 前缀 | 条数 |
|---|---|---|---|---|---|
| pref | 42 | menu | 29 | action | 26 |
| home | 24 | shortcut | 21 | open | 16 |
| app | 14 | date | 11 | suggestions | 11 |
| exit | 11 | link | 11 | settings | 10 |
| language | 10 | popup | 10 | address | 10 |
| clear | 8 | refresh | 6 | search | 6 |
| choose | 5 | install | 5 | hide | 4 |
| check | 4 | create | 4 | suggestion | 4 |
| default | 3 | restart | 3 | remember | 2 |
| look | 2 | skip | 2 | view | 2 |
| misc | 2 | back | 1 | forward | 1 |
| share | 1 | downloading | 1 | next | 1 |
| get | 1 | use | 1 | close | 1 |
| no | 1 | reader | 1 | toast | 1 |
| content | 1 | preview | 1 | select | 1 |
| **合计** | **332** | | | | |

> `home` 这个单词键已计入上面的 `home | 24`，不重复计算。45 个前缀合计 332，与脚本统计一致。

---

## 4. 特殊条目

### 4.1 复数（3 组，全部只有 one / other）

| key | one | other |
|---|---|---|
| `shortcut_manager_delete_selected_title` | Delete shortcut? | Delete %1$d shortcuts? |
| `shortcut_manager_delete_selected_message` | This shortcut will be removed and stop working on your home screen… | %1$d shortcuts will be removed… |
| `shortcut_manager_deleted_count` | Shortcut deleted | %1$d shortcuts deleted |

中文写法（只写 `other`）：

```xml
<plurals name="shortcut_manager_delete_selected_title">
    <item quantity="other">删除 %1$d 个快捷方式？</item>
</plurals>
<plurals name="shortcut_manager_delete_selected_message">
    <item quantity="other">%1$d 个快捷方式将从桌面移除并停止工作，你之后可以自行删除图标。</item>
</plurals>
<plurals name="shortcut_manager_deleted_count">
    <item quantity="other">已删除 %1$d 个快捷方式</item>
</plurals>
```

### 4.2 转义与特殊字符（必须原样保留）

| key | 源文特征 | 中文处理 |
|---|---|---|
| `downloading` | `Downloading\u2026` | `正在下载\u2026`（保留转义写法，不要写成 … 字符以外的形式） |
| `next` | `Next \u2192` | `下一步 \u2192` |
| `open_folder_error_message` | `…\n\n%1$s` | 保留两个换行与 `%1$s` |
| `skip_update_on_metered_summary` | `Don\u2019t` | 中文不含撇号，直接写「不要在…」 |
| `view_changelog_summary` | `what\u2019s new` | 同上 |
| `suggestions_google_warning_message` | 长句，含 `%1$s`?（无占位符） | 直译，保留句意，不加句号 |
| 含 `\'` 的 14 条 | 均为英文所有格/缩写 | 中文不会出现，**不要照抄反斜杠** |

### 4.3 长文本
本批无 >200 字符的字符串，最长是 `skip_update_on_metered_summary` 与 `suggestions_google_warning_message`，一次译完即可。

---

## 5. 语境与参考译法

### 5.1 本批风格要点
- `pref_category_*` 是**设置首页的分类名**，必须是 2–4 字名词短语：隐私与安全、外观、浏览器、下载、数据节省、自定义提示…（与后续批次页面标题呼应）
- `action_*` 是按钮标签，2–4 字动词：保存、复制、粘贴、重命名、全选
- `menu_*` 是菜单项，可用 3–6 字：在新标签页打开、添加到主页、复制链接地址
- `home_*` 是主页控件文案，允许口语化一点
- 单词键多为无障碍描述（`contentDescription`），译法统一为名词：返回、前进、关闭、首页

### 5.2 参考译法（对齐用，不强制逐字）

| key | 英文 | 建议中文 |
|---|---|---|
| `back` / `forward` | Back / Forward | 返回 / 前进 |
| `downloading` | Downloading… | 正在下载… |
| `next` | Next → | 下一步 → |
| `action_save` | Save | 保存 |
| `menu_style_bottom_sheet` | Bottom Sheet | 底部弹出菜单 |
| `menu_data_saver` | Data Saver | 省流模式 |
| `pref_category_fullscreen` | Full screen | 全屏 |
| `pref_show_home_button_summary` | Show a home button next to the address bar | 在地址栏旁显示首页按钮 |
| `address_bar_position_split` | Split | 分栏 |
| `home_favorites_empty` | Pin the sites you visit most. Tap here to add one | 固定你最常访问的网站，点此添加 |
| `shortcut_manager_already_pinned` | This shortcut is already on your home screen | 该快捷方式已在桌面上 |
| `date_time_picker_week_label` | Week %1$d, %2$d | 第 %1$d 周，%2$d |

---

## 6. 操作步骤

1. 导出清单：
   ```bash
   python tests/i18n_scope.py B1 --missing > .tmp_b1.txt
   wc -l .tmp_b1.txt     # 应为 332 + 3 组复数
   ```
2. 按上面的「界面清单」顺序译，**每次只处理 60–90 条**，写入 `values-zh/strings.xml`（追加，保持源文件 key 顺序）。
3. 每完成一段，跑一次 `python tests/check_i18n.py --locale zh --allow-missing`，确保没有转义/占位符错误累积。
4. 全部完成后去掉 `--allow-missing` 再跑一次（此时仍可能因其他批次缺失而报 missing，用 `--report-missing` 确认缺口只在别的批次）。

---

## 7. 校验

```bash
python tests/i18n_scope.py B1 --stat          # 333/333 100%
python tests/check_i18n.py --locale zh --allow-missing
```

---

## 8. 完成判据

- [ ] `i18n_scope.py B1 --stat` = 333/333（+ 3 组复数）
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL
- [ ] 提交：`i18n(zh): core actions, settings navigation and dialogs`

---

## 9. 本批独有的坑

| 坑 | 说明 |
|---|---|
| `pref_category_*` 与后续页面标题不一致 | 分类叫「隐私与安全」，进页面标题却是「安全」，用户会觉得换了个地方。先定分类名，后批沿用 |
| 把 `action_*` 译成名词 | 会出现在按钮上，必须动词 |
| `home` 与 `homepage` 混用 | 本批的 `home` 是「首页」按钮；B4 的 `homepage_*` 是「主页」设置，二者不同 |
| 照抄源文的 `\u2019` | 中文无撇号，直接删除，不要保留转义 |
| `open_folder_error_message` 少写换行 | 路径会接在句尾，很难看；必须保留 `\n\n` |

---

## 10. 交接

- 下一步：`PLAN_4.md`（B2 外观 234 + B5 媒体 104）。
- 交接时 `i18n_scope.py --all --stat` 应显示 B1 100%，总计约 15%。
- 若本批出现新的术语，先补 `PLAN_1` 第 5 节再继续。
