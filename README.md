# iperf-standard-test

iperf3 标准吞吐测试方法论 skill — 测试矩阵设计、执行通道选择、数据分析（爬坡/重传/丢包/环境波动/伴随指标）、报告模板。

适用于嵌入式设备（单核 MIPS/ARM）WiFi/以太网吞吐基准测试、驱动/网络栈/系统改动后的性能回归验证、消融实验。

## 安装

### 方式 1：一键脚本（推荐）

```bash
curl -fsSL https://gitee.com/GreatBigM/iperf-standard-test-skill/raw/main/install.sh | bash
```

等价于手动复制，不经过安全扫描。重复执行 = 升级（自动备份旧版到 `.bak.<时间戳>`）。

指定目标：`bash install.sh --target hermes,claude,zcode` 或 `--all`（自动探测已装 agent，含 ZCode）。

### 方式 2：手动复制（永远可行）

```bash
git clone --depth 1 https://gitee.com/GreatBigM/iperf-standard-test-skill.git /tmp/iperf-skill
cp -r /tmp/iperf-skill/templates /tmp/iperf-skill/references /tmp/iperf-skill/scripts /tmp/iperf-skill/SKILL.md /tmp/iperf-skill/CHANGELOG.md ~/.hermes/skills/iperf-standard-test/   # Hermes
cp -r /tmp/iperf-skill/templates /tmp/iperf-skill/references /tmp/iperf-skill/scripts /tmp/iperf-skill/SKILL.md /tmp/iperf-skill/CHANGELOG.md ~/.zcode/skills/iperf-standard-test/   # ZCode
```

### 方式 3：GitHub 镜像（海外备选）

```bash
curl -fsSL https://raw.githubusercontent.com/GreatBigM/iperf-standard-test-skill/main/install.sh | bash
```

## 依赖

| 依赖 | 必需 | 说明 |
|------|------|------|
| Hermes / Claude / Codex / ZCode | ✓ | skill 由 agent 加载执行 |
| iperf3 | ✓ | 设备端 `/tmp/iperf3` + 主机端 `iperf3 -s` |
| adb | ✓（ADB 通道测试时） | 短测（≤60s）通道 |
| 串口 | ✓（长测 >60s 时） | 串口持久 shell 后台执行 |

## 使用

对 AI 说"测吞吐 / 跑 iperf / 压测"，或加载本 skill 按流程执行：

1. 测试矩阵设计（方向 × 流数 × 协议 × 速率模式 × 时长 × 通道）
2. 前置检查（wpa COMPLETED / server 可用 / /tmp 工具）
3. 执行（ADB 前台 ≤60s / 串口后台 >60s）
4. 数据分析（完成性 / 爬坡 / 重传 / 丢包 / 伴随指标归因）
5. 报告（templates/report-template.md）

## 内容

- `SKILL.md` — 主流程
- `scripts/iperf_bench.py` — 标准测试执行器（多轮执行 + 结果汇总，AI/终端双通道）
- `references/data-analysis-pitfalls.md` — 10 条实测数据分析坑
- `templates/report-template.md` — 测试报告模板
- `CHANGELOG.md` — 版本历史
