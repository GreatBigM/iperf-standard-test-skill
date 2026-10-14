# Changelog
## 1.2.4 (2026-10-14)

### Fixed（install.sh 两处 + 发布闸门，与 qwiki-skill 同款）

- **`--target hermes,claude`（空格形式）从未生效**：解析只认 `--target=`，空格形式把值吞成空串后落进"非交互 = 装全部"分支——而 README / 用法行 / 脚本头部**三处文档全写的空格形式**。现两种形式都支持，且 `--target` 缺参数时直接报错退出（不再静默装全部）。
- **备份落在 skills 扫描根之内**：旧版备份写成 `<skills>/<name>.bak.<时间戳>`，而 agent 按「含 SKILL.md 的目录」发现技能、不看目录名 ⇒ 备份被当成**第二个同名技能**加载（重名歧义下静默跳过其一）。现备份落 `<tool 根>/skills-backup/`（扫描根之外），README 与脚本尾注同步。
- **挂上 pre-push 闸门（脱敏 + CHANGELOG 同步）**：`scripts/publish-check.py`（扫项目代号 / 内网 IP / MAC / 长 hash / 凭据 / 本机路径，自带 `--self-test`）+ `scripts/hooks/pre-push`；启用一次 `git config core.hooksPath scripts/hooks`。理由与脱敏规则同源：**靠人记必然回潮**，检查要做成"推送时自动拦"而不是"记得手动跑"。CHANGELOG 闸门名单 = SKILL.md / install.sh / templates/ / scripts/ / references/。
- 版本 1.2.3 → 1.2.4

# CHANGELOG
## 1.2.3 (2026-09-29)

### Fixed

- **纠正 `-B <wlan0_IP>` 的错误说法**（原文写"强制走 WiFi，双保险"）：eth0 与 wlan0 同网段时 `-B` 拦不住路由走 eth0（09-28 实测一组数全压 94~95M = 100BASE-TX 天花板）
- 前置检查新增第 3 条**网口归属自证**（打流前后 `/proc/net/dev` 差分，wlan0 增量须≈流量）+ §4.2 增补第 0 查（先验归属再分析）
- 版本 1.2.2 → 1.2.3

## 1.2.2 (2026-09-28)

### Changed

- 回灌本机 Hermes 副本的实测修正：设备默认流数 P5 陷阱（裸命令≠单流）+ data-analysis-pitfalls §11 32 位计数器回绕
- 版本 1.2.1 → 1.2.2


## v1.2.0 (2026-08-18)

- **README 依赖表补 ZCode**：多 agent 列表统一为 Hermes / Claude Code / Codex / ZCode
- 版本 1.1.0 → 1.2.0

## v1.1.0 (2026-08-18)

- **ZCode 安装目标**：install.sh 支持 ZCode（探测 `~/.zcode` → 安装到 `~/.zcode/skills/iperf-standard-test`），README 补 `--target zcode` 示例与手动复制路径，发布页一键命令即可装到 ZCode

## v1.0.0 (2026-08-11)

- 初版：iperf3 标准吞吐测试方法论
- 测试矩阵设计（方向/流数/协议/速率模式/时长/通道）
- 速率模式：最大速率（TCP 满速/UDP 100M）+ 限速二分（UDP 零丢包点 100M→60M→40M）+ 双向 -d
- 执行通道选择（ADB 前台 ≤60s / 串口后台 >60s）
- 数据分析四查（完成性/爬坡/重传/丢包）+ 观察项全清单（TCP/UDP × 最大/限速 + jitter）+ 环境波动判别
- 伴随指标采集（CPU loadavg / 驱动-协议栈分层丢包 / RSSI / 池状态）+ 归因规则 + 实测锚点
- 报告模板（templates/report-template.md，含伴随指标表）
- 数据分析坑参考（references/data-analysis-pitfalls.md，10 条实测教训：新增丢包分层误归因/池耗尽骤降）
- 标准测试执行脚本（scripts/iperf_bench.py，isatty 双通道）
- 来源：2026-08-07~11 HM6502 系列实测经验提炼（TCP 512K 消融/爬坡检查/环境波动补测）

## 1.2.1 (2026-08-28)

### Added

- install.sh 新增 pi 安装目标（探测 `~/.pi/agent` → 安装到 `~/.pi/agent/skills/<skill>`，pi 自动发现）
- 版本 1.2.0 → 1.2.1
