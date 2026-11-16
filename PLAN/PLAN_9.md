# PLAN_9 — 收尾：一次编译与交付

> 会话 S8 · 前置：PLAN_8 的脚本终检已过（`--all --stat` 2179/2179）
> 本阶段只做三件事：**编译一次、装一次看眼、交付**。不做逐屏验收。

---

## 1. 编译一次

```bash
./gradlew :app:assembleGithubDebug
```

通过即算过。若失败，先看是不是 aapt2 报错（转义/裸 `&`），那说明某条译文有转义问题，跑 `check_i18n.py` 定位。

只在这一步跑编译；其余批次不要求每批都编。

---

## 2. 装一次看眼（可选，5 分钟）

```bash
adb install -r app/build/outputs/apk/github/debug/app-github-arm64-v8a-debug.apk
```

看三处就够，别逐页翻：

1. 设置 → 外观 → 语言，列表里有「简体中文」，选中后界面变中文。
2. 设置首页随便点两页，没有英文残留。
3. 下载管理器打开一次，按钮和空状态正常。

> 注意：`app-github-universal-debug.apk` 实测装上去会崩（`ClassNotFoundException`，dex 合并问题），装机请用对应 ABI 包。

---

## 3. 提交与交付

- 每批一个 commit，信息见各 `PLAN_N` 末尾；`PLAN/`、`tools/`、`AGENTS.md` 默认不入库、不进上游 PR。
- 是否推上游、是否提 PR：**先问用户**，不要自行 push。
- 交付物：

| 交付物 | 位置 |
|---|---|
| 中文字符串 | `app/src/main/res/values-zh/strings.xml` |
| 语言注册 | `LocaleHelper.kt`、`LanguageUtils.kt`、`values/strings.xml` |
| 校验脚本 | `tools/check_i18n.py`、`tools/i18n_scope.py` |

---

## 4. 已知限制（交付时提一句）

1. 繁体设备显示简体（`values-zh` 兜底）；要做繁体另加 `values-zh-rTW`。
2. `about_license_text`（GPLv3 正文）与品牌名保留英文。
3. 未做 `localeConfig`，Android 13+ 系统设置里没有「应用语言」入口，应用内切换正常。

---

## 5. 上游发版后

```bash
git fetch origin && git merge origin/main
python tools/i18n_scope.py --all --stat
python tools/check_i18n.py --locale zh --report-missing
```

新增 key 会回退英文，不会崩；补齐即可。
