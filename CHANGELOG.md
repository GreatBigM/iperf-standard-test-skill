# Changelog

## 1.2.7 (2026-10-15)

### Fixed
- **README「内容」清单与随安装下发的实际文件对齐**（清单原本只列 4 个文件，读者无从知道闸门与钩子也在安装面内）：
  补 `scripts/publish-check.py`（发布前脱敏闸门，随 `scripts/` 一并安装，自带 `--self-test`）与
  `scripts/hooks/`（推送前钩子，启用方式见「安装」节）
- **同一实物两个条数**（1.0.0 条目写「10 条实测教训」，而实物 `references/data-analysis-pitfalls.md`
  与 README 均已 12 条）⇒ 只在该历史条目末**加注**「后续增至 12 条」，史实结论不重写
- **占位化条目补一句可读性说明**（1.2.5 / 1.2.6 条目）：例示改成 `HM####` / `BW###` 这类占位写法后，
  读者已无法复原原先的洞的形态 ⇒ 各加一句「原例中的真实代号已换占位写法」，不删史、不加真名
- 版本 1.2.6 → 1.2.7
- pre-push 的 CHANGELOG 同步名单注释补 `assets/`（与正则实际枚举一致）——九仓该文件文本归一

## 1.2.6 (2026-10-15)

### Fixed
- **CHANGELOG 自身含真名**（上版条目里用来举例的标识是真实代号，而本仓闸门对 CHANGELOG 同样扫描）⇒ 例示改用 `HM####` / `BW###` / 「项目hm####」这类形态占位；历史条目里的项目代号一并换 `<项目A>`
- **README 支持文件说明与实物对齐**：数据分析坑条数按 `references/data-analysis-pitfalls.md` 的实际条目数改写（原写 10 条）
- **支持文件清单补 `scripts/publish-check.py`**（发布前脱敏闸门，随安装下发；自带 `--self-test`）
- **报告模板 TCP 数据表删 `jitter` 列**（jitter 是 iperf3 的 UDP 输出列，TCP 表不该有；UDP 表保留）
- **CHANGELOG 结构**：删重复 H1；1.2.1 段从文件末归位到 1.2.2 与 1.2.0 之间；版本标题去 `v` 前缀
- 版本 1.2.5 → 1.2.6
- 注：本条目与 1.2.5 条目的例示原为真实代号，现已换占位写法（述及的缺陷形态与结论未改）

## 1.2.5 (2026-10-15)

### Fixed
- **发布闸门 publish-check.py 三个洞同批修**（脱敏反复回潮的根因之一：闸门对真实标识零防护却一直报「干净」）：
  ① 代号正则大小写不敏感（旧版只认小写，`HM####`/`BW###` 整体漏）；
  ② 白名单改为**按匹配项豁免**（旧版 `if any(a in line for a in ALLOW): continue` 是整行豁免——一行里出现
  `<项目A>` 就给同行的真名背书；且原 7 个词对 12 条 pattern 全部零命中 = 纯死豁免）；
  ③ 词边界改用显式字符类（`\b` 在 str 模式下 `\w` 含汉字 ⇒「项目hm####」这类中文常见写法漏检，
  加不加空格决定报不报）。另补 PRJ0## / 裸数字代号 / MAC 连字符 / 凭据变体（`token=`、`Bearer`、中文「密码」键）/
  邮箱 六类形态。
- **`--self-test` 样本按已知缺陷类别扩容**（原 15 条只覆盖「正常裸值」一档，上述六类一条样本都没有）；
  自检与扫描共用同一份判定口径（`line_hits`），不再各写一套造成假绿。
- **`scripts/hooks/pre-push` 在推送路径上先跑 `--self-test`**（规则表被改坏时不得静默通过）；
  CHANGELOG 名单统一为超集（SKILL / SCHEMA / install.sh / templates / references / scripts，9 仓文本自此一致）；
  基点改为 `origin/main → gitee/main → 根提交` 三级回落（旧版无 `origin/main` 时回落到 `HEAD~1`，
  多笔提交一起推会只看最后一笔）。
- **新增本机私用名单 `scripts/publish-deny.local`**（gitignore、不进仓）：人名 / 昵称 / 厂商 SDK 名 /
  内部 skill 名这类**无法正则枚举、也不该写进发布仓**的标识，在本机未跟踪文件里逐行列真名，闸门自动一并扫。

### 说明
- 口径全文见 `scripts/publish-check.py` 文件头（已知边界：长 hash 折行、全角句点 IP 不识别；该文件自身在
  `SKIP_FILES` 内，改它时需人工核对）。9 仓共用同一份闸门（md5 一致）——改一处必须批量同步。
- 版本 1.2.4 → 1.2.5
- 注：本条目例示原为真实代号，现已换占位写法（述及的缺陷形态与结论未改）

## 1.2.4 (2026-10-14)

### Fixed（install.sh 两处 + 发布闸门，与 qwiki-skill 同款）

- **`--target hermes,claude`（空格形式）从未生效**：解析只认 `--target=`，空格形式把值吞成空串后落进"非交互 = 装全部"分支——而 README / 用法行 / 脚本头部**三处文档全写的空格形式**。现两种形式都支持，且 `--target` 缺参数时直接报错退出（不再静默装全部）。
- **备份落在 skills 扫描根之内**：旧版备份写成 `<skills>/<name>.bak.<时间戳>`，而 agent 按「含 SKILL.md 的目录」发现技能、不看目录名 ⇒ 备份被当成**第二个同名技能**加载（重名歧义下静默跳过其一）。现备份落 `<tool 根>/skills-backup/`（扫描根之外），README 与脚本尾注同步。
- **挂上 pre-push 闸门（脱敏 + CHANGELOG 同步）**：`scripts/publish-check.py`（扫项目代号 / 内网 IP / MAC / 长 hash / 凭据 / 本机路径，自带 `--self-test`）+ `scripts/hooks/pre-push`；启用一次 `git config core.hooksPath scripts/hooks`。理由与脱敏规则同源：**靠人记必然回潮**，检查要做成"推送时自动拦"而不是"记得手动跑"。CHANGELOG 闸门名单 = SKILL.md / install.sh / templates/ / scripts/ / references/。
- **脱敏：正文里的项目代号与示例内网 IP 换占位符**——`scripts/publish-check.py` 挂上后首扫命中，逐条判定（另 4 处『凭据赋值』为误报：都是串口提示符 `Password:` 字面量与说明，无真实密钥）后替换：正文 / references 里的项目代号 → `<项目A>`（多处依次 A/B/C/D），模板示例里的内网 IP → 文档保留段 `192.0.2.x`。这些标识已随历史提交公开过，本次只保证**往后的版本不再含**；历史不回改——force push 也收不回（已 clone/fork/缓存的副本），脱敏的真实收益是往后不再泄漏。
- 版本 1.2.3 → 1.2.4

## 1.2.3 (2026-09-29)

### Fixed

- **纠正 `-B <wlan0_IP>` 的错误说法**（原文写"强制走 WiFi，双保险"）：eth0 与 wlan0 同网段时 `-B` 拦不住路由走 eth0（09-28 实测一组数全压 94~95M = 100BASE-TX 天花板）
- 前置检查新增第 3 条**网口归属自证**（打流前后 `/proc/net/dev` 差分，wlan0 增量须≈流量）+ §4.2 增补第 0 查（先验归属再分析）
- 版本 1.2.2 → 1.2.3

## 1.2.2 (2026-09-28)

### Changed

- 回灌本机 Hermes 副本的实测修正：设备默认流数 P5 陷阱（裸命令≠单流）+ data-analysis-pitfalls §11 32 位计数器回绕
- 版本 1.2.1 → 1.2.2


## 1.2.1 (2026-08-28)

### Added

- install.sh 新增 pi 安装目标（探测 `~/.pi/agent` → 安装到 `~/.pi/agent/skills/<skill>`，pi 自动发现）
- 版本 1.2.0 → 1.2.1

## 1.2.0 (2026-08-18)

- **README 依赖表补 ZCode**：多 agent 列表统一为 Hermes / Claude Code / Codex / ZCode
- 版本 1.1.0 → 1.2.0

## 1.1.0 (2026-08-18)

- **ZCode 安装目标**：install.sh 支持 ZCode（探测 `~/.zcode` → 安装到 `~/.zcode/skills/iperf-standard-test`），README 补 `--target zcode` 示例与手动复制路径，发布页一键命令即可装到 ZCode

## 1.0.0 (2026-08-11)

- 初版：iperf3 标准吞吐测试方法论
- 测试矩阵设计（方向/流数/协议/速率模式/时长/通道）
- 速率模式：最大速率（TCP 满速/UDP 100M）+ 限速二分（UDP 零丢包点 100M→60M→40M）+ 双向 -d
- 执行通道选择（ADB 前台 ≤60s / 串口后台 >60s）
- 数据分析四查（完成性/爬坡/重传/丢包）+ 观察项全清单（TCP/UDP × 最大/限速 + jitter）+ 环境波动判别
- 伴随指标采集（CPU loadavg / 驱动-协议栈分层丢包 / RSSI / 池状态）+ 归因规则 + 实测锚点
- 报告模板（templates/report-template.md，含伴随指标表）
- 数据分析坑参考（references/data-analysis-pitfalls.md，10 条实测教训：新增丢包分层误归因/池耗尽骤降）——后续增至 12 条（1.2.7 加注）
- 标准测试执行脚本（scripts/iperf_bench.py，isatty 双通道）
- 来源：2026-08-07~11 <项目A> 系列实测经验提炼（TCP 512K 消融/爬坡检查/环境波动补测）

