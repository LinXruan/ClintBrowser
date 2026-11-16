# PLAN_11 — 发布准备：非官方中文分支（v1.2.7 / versionCode 48）

> 会话 S10 · 前置：PLAN_10（全局刷新率）已完成
> 目标：把本仓库整理成一个可以独立发布的中文分支，推到 `LinXruan/ClintBrowser`，并在 GitHub 上保留 `forked from jhaiian/ClintBrowser` 关系。
> 版本名不变（v1.2.7），只升 `versionCode`，保证覆盖安装时 Android 认作升级。

---

## 1. 已定决策

| 项 | 决定 | 理由 |
|---|---|---|
| `versionName` | 保持 `v1.2.7` | 功能集与上游 1.2.7 一致，不虚构新版本 |
| `versionCode` | `47` → `48` | 同一 versionName 下必须靠 versionCode 区分新旧 |
| `applicationId` | `com.jhaiian.clint` → `com.linxruan.clint.zh` | 与上游签名不同，同包名无法覆盖安装；换包名后可与上游共存 |
| `namespace` / Kotlin 包名 | **不动**（仍为 `com.jhaiian.clint`） | applicationId 与源码包名解耦；改 namespace 会牵动全部 import，收益为零 |
| debug 包名 | 自动变为 `com.linxruan.clint.zh.debug` | `applicationIdSuffix = ".debug"` 不变 |
| 更新检查 | 指向 `LinXruan/ClintBrowser` 的 `Update/*.json` | 原逻辑会把用户引到上游 APK，签名不同装不上 |
| `Update/*.json` | 改写为 `1.2.7` / `48`，下载地址指向本仓库 releases | 当前版本号相等 → 不误报更新；发新版时手动改这两个文件 |
| README | 中文重写，顶部非官方声明 + 改动清单 + 上游链接；不保留英文版 | 用户明确要求 |
| 仓库文档 | `AGENTS.md`、`DEBUG.md`、`PLAN/`、`fastlane/`、`tools/`、其余 workflows 全部保留 | 用户明确要求保留前三个；其余为上构建与商店元数据，留着无害 |
| `release.yml` | **删除** | 依赖上游 secrets（签名 keystore、`PERSONAL_GITHUB_TOKEN`），打 tag 必失败，且有误推上游仓库的风险 |
| Logo | 重新设计：纯黑底 + 紫色渐变大写 `C` | 上游 Logo 属商标资产、不在 GPL 授权内；README 注明更换原因 |

---

## 2. 现状核实（已实测）

| 检查项 | 结果 |
|---|---|
| 本地 remote | 无 |
| 本地历史 | 347 个提交，首条 `Initial commit` |
| 与上游关系 | 上游 `main` HEAD `66acf9d` 已在本地历史中；本地领先 **21** 个提交 → 推 fork 为快进，无需 force |
| 工作区 | 干净 |
| 跟踪文件 | 616 个，`.git` 37MB（含 `jniLibs` 预编译 `.so` 约 11MB，必须保留） |
| 已忽略且不会入库 | `local.properties`、`app/release_keystore.jks`、`build/`、`.gradle/`、`.kotlin/`、`__pycache__/`、`tools/.adb_last_endpoint` |
| 包名硬编码 | 仅通知/广播的 action 字符串（`com.jhaiian.clint.*`），与安装包名无关，**不需要改** |
| 图标资产 | 只有 `mipmap-anydpi-v26` 两份 XML + `drawable/ic_launcher_foreground.xml`；无 PNG mipmap（minSdk 26，够用） |
| 上游链接位置 | `UpdateChecker.kt`（更新源 + releases）、`AboutScreen.kt`（仓库/贡献者）、`SetupActivity.kt`（隐私政策/条款）、`SettingsPanes.kt`（新建 issue）、`values*/strings.xml` 的 `about_github_url` |
| 现有徽章版本 | README 写 1.2.5，代码是 1.2.7，顺手更正 |

---

## 3. 变更清单

### 3.1 代码与配置

| 文件 | 改动 |
|---|---|
| `app/build.gradle.kts` | `versionCode = 48`；`applicationId = "com.linxruan.clint.zh"`；`versionName` 不变 |
| `update/UpdateChecker.kt` | `STABLE_URL` / `BETA_URL` → `raw.githubusercontent.com/LinXruan/ClintBrowser/main/...`；`onViewGithub` 的 releases 链接同步 |
| `settings/about/AboutScreen.kt` | `GITHUB_URL`、`CONTRIBUTORS_URL` → 本仓库；作者、社区、邮箱等署名信息保持上游 |
| `setup/SetupActivity.kt` | `PRIVACY_POLICY_URL`、`TERMS_URL` → 本仓库（文件随仓库一起发布） |
| `settings/SettingsPanes.kt` | 反馈入口 `issues/new` → 本仓库 |
| `res/values*/strings.xml` | `about_github_url` 的地址改为 `github.com/LinXruan/ClintBrowser`（只替换 URL，不新增 key） |
| `tools/adb_install_release.py` | 注释里的包名更新为新的 release/debug 包名 |

### 3.2 图标

| 文件 | 改动 |
|---|---|
| `res/drawable/ic_launcher_foreground.xml` | 重写为渐变填充的 `C`（矢量路径，非 stroke，才能吃渐变） |
| `res/drawable/ic_launcher_monochrome.xml` | 新增；纯色 `C`，供系统主题图标着色 |
| `res/mipmap-anydpi-v26/ic_launcher.xml`、`ic_launcher_round.xml` | `monochrome` 指向新文件 |
| `res/values/ic_launcher_bg.xml` | `#111111` → `#000000` |
| `docs/icon.png` | 512×512，README 用 |
| `fastlane/metadata/android/en-US/images/icon.png` | 同步替换，避免商店素材还是旧 Logo |

### 3.3 发布内容

| 文件 | 改动 |
|---|---|
| `README.md` | 中文重写；顶部非官方声明、上游链接、改动清单、Logo 说明；徽章指向本仓库 |
| `Update/Stable.json`、`Update/Beta.json` | 版本 `1.2.7` / `48`，changelog 改为本分支说明，下载地址指向本仓库 releases |
| `.github/workflows/release.yml` | 删除 |
| `PLAN/PLAN_1.md` | 台账补 S10 行 |

**不做**：不动 `namespace`、不改 `app_name`、不改上游 `Attribution.md` / `CONTRIBUTORS` / 版权头、不加新文案 key。

---

## 4. 图标规格

- 画布 108×108（adaptive icon 标准），安全区 72dp，图形内容约 64dp。
- 背景：纯黑 `#000000`。
- 前景：大写 `C`，外半径 32、内半径 19.5、开口朝右（±32°），圆环中心 (54,54)。
- 填充：线性渐变 `#C084FC`（左上）→ `#6D28D9`（右下），"略带渐变"，不是彩虹。
- 路径：`M81.14,70.96 A32,32 0 1 1 81.14,37.04 L70.54,43.67 A19.5,19.5 0 1 0 70.54,64.33 Z`（外边顺时针大弧 → 内边逆时针大弧，闭合成环）。
- monochrome：同一路径，纯白填充，系统自行着色。
- `docs/icon.png`：同几何，512×512，黑色圆角方块底 + 同一渐变，4× 超采样后缩放抗锯齿。

---

## 5. 执行步骤

1. 升 `versionCode`、换 `applicationId`，编译一次确认没漏改包名。
2. 切更新源与仓库链接，改写 `Update/*.json`。
3. 生成新图标（vector + PNG）并替换；目视检查 512 PNG。
4. 重写 README，补 Logo 说明。
5. 删 `release.yml`，补 PLAN_1 台账。
6. 全量校验（§6）。
7. `gh repo fork` 建 `LinXruan/ClintBrowser` → 推 `main` → 提交 PLAN_11 → 再推。

---

## 6. 校验

```bash
python tests/i18n_scope.py --all --stat     # 条目数与改动前一致
python tests/check_i18n.py --locale zh      # 无 FAIL
./gradlew :app:assembleGithubDebug          # BUILD SUCCESSFUL
```

完成判据：

- [ ] 编译通过，产物包名为 `com.linxruan.clint.zh.debug`
- [ ] `Update/*.json` 的 `versionCode` 与本版一致（48），不会自提示更新
- [ ] 仓库内不存在上游签名密钥、token、`local.properties`、keystore、构建产物
- [ ] GitHub 仓库显示 `forked from jhaiian/ClintBrowser`
- [ ] README 有非官方声明、上游链接、改动清单与 Logo 说明

---

## 7. 推送方案

```bash
gh repo fork jhaiian/ClintBrowser --clone=false --remote=false
git remote add origin https://github.com/LinXruan/ClintBrowser.git
git push -u origin main                     # 快进，保留 347 条历史
git commit -m "48_pl11：发布准备（中文分支、包名、图标、更新源）"
git push
```

- 保留完整历史（不用 squash）：来源链、blame、GPL 义务都更清楚。
- 不 force：本地已包含上游 HEAD，fork 的 `main` 可直接快进。
- fork 出来的仓库 workflow 默认关闭，需要时在网页手动启用。
- 不推 tag、不发 release；APK 由用户后续手动上传。

---

## 8. 风险与回退

| 风险 | 处理 |
|---|---|
| 换 `applicationId` 后旧版数据不共享 | 预期行为：与上游/旧包并存，不迁移数据；README 说明 |
| 更新检查自提示 | `Update/*.json` 的 `versionCode` 固定为本版 48；发版前手动改 |
| 渐变在低版本 VectorDrawable 不支持 | 渐变填充自 API 24 supported；minSdk 26 安全；真机若不显示则退回单色 `#8B5CF6` |
| 删 `release.yml` 丢掉发版自动化 | 该流程本来依赖上游密钥，不可用；改为手动上传 APK |
| 误把敏感文件推上去 | 已确认 `.gitignore` 覆盖 keystore、`local.properties`、构建目录；推送前 `git status --ignored` 复查 |
| 回退 | 还原 `build.gradle.kts` 两行 + 图标文件；`git revert` 单个提交即可 |

---

## 9. 合规说明

- 代码沿用 GPLv3，`LICENSE` 原样保留，版权头不改。
- 修改过的文件在 README 的「本仓库改动」中列明，并链接上游仓库与原始提交历史。
- "Clint" / "Clint Browser" 名称、原 Logo、截图属上游作者的商标/专有资产，不在 GPL 授权内：本仓库明确标注为非官方分支，Logo 已自行重绘。
- 不声称获得上游作者背书。

---

## 10. 交接

- 提交信息：`48_pl11：发布准备（中文分支、包名、图标、更新源）`。
- 推送后把仓库地址与 fork 状态回报用户。
- 后续发版流程：改 `versionCode`/`versionName` → 更新 `Update/Stable.json` → 构建对应 ABI 包 → 网页上传 release。
