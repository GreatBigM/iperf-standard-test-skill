# CHANGELOG

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
