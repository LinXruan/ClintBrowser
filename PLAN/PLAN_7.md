# PLAN_7 — B6：隐私、网站屏蔽与过滤列表

> 会话 S6 · 354 条字符串 · 前置：PLAN_2
> 本批专业度最高：屏蔽引擎、过滤规则、站点权限。**术语一旦漂移，用户会认为功能坏了。**

---

## 1. 目标（可验证）

1. 网站屏蔽页（分类、启用状态、下载分类数据）全部中文。
2. Quiver Guard（品牌名保留）的规则管理、编译、更新流程全部中文。
3. 过滤规则列表（添加、检查更新、强制更新、进度、失败）全部中文。
4. 站点信息面板与站点设置（权限、Cookie、桌面模式）全部中文。
5. Cookie 控制、HTTPS 优先、Do Not Track、WebRTC 保护、全局隐私控制全部中文。
6. `i18n_scope.py B6 --stat` = 354/354。

---

## 2. 分块

| 块 | 前缀 | 条数 | 界面 |
|---|---|---|---|
| C1 | `website_blocker` 63 · `website_blocked` 3 · `additional_*` 14 · `block_*` 2 | **82** | 网站屏蔽主页、附加网站、拦截页 |
| C2 | `quiver_guard_*` 80 | **80** | Quiver Guard 规则管理 |
| C3 | `filter_list_*` 77 | **77** | 过滤规则列表（含手动规则） |
| C4 | `site_permission` 18 · `site_info` 18 · `site_settings` 12 · `site_section` 5 | **53** | 站点信息浮层、站点设置 |
| C5 | `cookies_*` 27 · `ssl_*` 9 · `http_*` 8 · `https_*` 5 · `privacy_*` 7 · `do_*` 2 · `global_*` 2 · `webrtc_*` 2 | **62** | Cookie 控制、连接安全、隐私开关 |
| | | **354** | |

---

## 3. 特殊条目

### 3.1 非位置占位符（已重构为 `%1$d` / `%1$s`）

| key | 英文 | 建议 |
|---|---|---|
| `quiver_guard_exception_delete_message` | Remove %d saved site(s)? | 移除 %1$d 个已保存的网站？ |
| `site_permission_delete_confirm_message` | Remove %d exception(s)? | 移除 %1$d 条例外？ |
| `filter_list_delete_confirm_message` | Remove %d filter list(s)? | 移除 %1$d 个过滤规则列表？ |
| `website_blocker_status_active` | Protecting you from %d known domains | 正在拦截 %1$d 个已知域名 |
| `website_blocker_delete_confirm_message` | This removes … %d selected categories… | 这会删除 %1$d 个已选分类的下载数据，之后可重新下载。 |
| `additional_websites_summary` | Websites added: %d | 已添加网站：%1$d |
| `additional_websites_delete_confirm_message` | This will delete %d selected websites… | 将从「附加网站」中删除 %1$d 个已选网站。 |

### 3.2 转义与多行

| key | 特征 | 处理 |
|---|---|---|
| `https_only_summary` | `don\u2019t` | 中文写「不支持 HTTPS 的网站」 |
| `filter_list_update_progress_checking` | `Checking\u2026` | 正在检查\u2026 |
| `filter_list_force_update_progress_preparing` | `Preparing to force update\u2026` | 正在准备强制更新\u2026 |
| `filter_list_update_success_recompiling` | `%1$d filter list(s) updated. Recompiling\u2026` | 已更新 %1$d 个过滤规则列表，正在重新编译\u2026 |
| `filter_list_update_all_failed` | `%1$d … failed to update:\n\n%2$s` | 保留 `\n\n`，失败详情在下一段 |
| `filter_list_update_partial_result` | 三参数 + 两次换行 | 保留结构：已更新 → 失败 → 是否立即编译 |
| `quiver_guard_compile_progress_list` | `%1$d of %2$d` | %1$d / %2$d |
| `quiver_guard_no_active_lists_message`（257 字符） | 带编号列表 `1. … 2. …` | 保留 `\n\n` 与编号，步骤动词用「点按」 |

### 3.3 撇号密集
本批 25 条含 `\'`（`don't`、`isn't`、`Clint's`），中文不含撇号，**不要保留反斜杠**。

---

## 4. 术语（本批最高优先级）

| 英文 | 中文 | 备注 |
|---|---|---|
| Website Blocker | 网站屏蔽 | 不写「拦截器」「广告拦截」 |
| Category（屏蔽分类） | 分类 | 欺诈、恶意软件、成人内容等 |
| Additional Websites | 附加网站 | 设置项名 |
| Quiver Guard | Quiver Guard | **品牌名不译** |
| Filter list | 过滤规则列表 | 首次出现可写「过滤规则列表（filter list）」，后续统一 |
| Rule | 规则 | |
| Manual filter | 手动规则 | |
| Compile / Recompile | 编译 / 重新编译 | 不写「合成」 |
| Exception | 例外 | 例外站点 |
| Allowlist / Blocklist | 允许列表 / 阻止列表 | 视上下文 |
| Site permission | 网站权限 | |
| Site settings | 网站设置 | |
| Cookies Control | Cookie 控制 | |
| Session cookies | 会话 Cookie | |
| Third-party cookies | 第三方 Cookie | |
| HTTPS Only | 仅 HTTPS | 开关名 |
| Do Not Track | 请勿追踪 | 括号保留 DNT |
| Global Privacy Control | 全局隐私控制 | 括号保留 GPC |
| WebRTC protection | WebRTC 保护 | |
| Secure connection | 安全连接 | |

---

## 5. 参考译法

| key | 英文 | 建议 |
|---|---|---|
| `website_blocker_category_fraud_desc` | Blocks fraud sites | 屏蔽欺诈网站 |
| `website_blocker_search_hint` | Search categories… | 搜索分类… |
| `website_blocker_link_clip_label` | Category Download URL | 分类数据下载地址 |
| `filter_list_add_title_hint` | Title | 名称 |
| `filter_list_force_update_all` | Force update (all lists) | 强制更新（全部列表） |
| `filter_list_update_error_generic` | Update check failed. Check your connection. | 检查更新失败，请检查网络连接 |
| `filter_list_item_check_update_progress_title` | Checking %1$s | 正在检查 %1$s |
| `quiver_guard_manual_filter_edit_dialog_title` | Edit Rule | 编辑规则 |
| `quiver_guard_auto_update_summary` | Checks for new versions in the background… | 在后台检查新版本，到期后自动应用 |
| `cookies_control_title` | Cookies Control | Cookie 控制 |
| `site_info_connection_secure_desc` | Information you send to this site… | 你发送到此网站的信息（如密码、卡号）不会被他人看到 |

---

## 6. 操作步骤

1. C1（82）→ C2（80）→ C3（77）→ C4（53）→ C5（62）。
2. C2 与 C3 术语必须共用同一套（「规则」「编译」「更新」），**先译 C3 再回头译 C2 也可**，但两块的词表要一次性定。
3. 每块后跑 `check_i18n.py --locale zh --allow-missing`。
4. C1 完成后编译一次，进「网站屏蔽」页看分类卡片文字是否溢出（分类名多为 2 字，描述较长）。

---

## 7. 校验

```bash
python tools/i18n_scope.py B6 --stat
python tools/check_i18n.py --locale zh --allow-missing
```

---

## 8. 完成判据

- [ ] `i18n_scope.py B6 --stat` = 354/354
- [ ] `check_i18n.py --locale zh --allow-missing` 无 FAIL
- [ ] 提交：`i18n(zh): privacy, website blocker and filter lists`

---

## 9. 本批独有的坑

| 坑 | 说明 |
|---|---|
| `filter_list_update_partial_result` 三个参数顺序 | 中文语序会变，`%1$d` 指「已更新」、`%2$d` 指「失败」、`%3$s` 是详情，**不要错位** |
| 把 Quiver Guard 译成「箭袋守卫」 | 品牌名，译了就无法与文档对应 |
| `website_blocker_status_active` 译成「保护你免受…」 | 开关状态行，越短越好：「正在拦截 %1$d 个域名」 |
| `ssl_warning_title` 直译「你的连接不是私密的」 | 建议「此连接不安全」，避免「私密」歧义 |
| 例外站点与允许列表混用 | 全批统一「例外」 |

---

## 10. 交接

- 下一步：`PLAN_8.md`（B7 脚本/翻译/数据 334 条 + 全量终检）。
- 台账记录 commit；若 C5 未完成，注明「Cookie/安全相关未译」。
