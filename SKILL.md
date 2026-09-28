---
name: iperf-standard-test
description: iperf3 标准吞吐测试：测试矩阵设计、执行通道选择、数据分析与报告模板全流程。
version: 1.2.2
category: devops
metadata:
  agent:
    triggers: [iperf测试, 吞吐测试, 带宽测试, 压测, 性能测试, 测试报告, 爬坡, 重传率分析]
---

# iperf3 标准吞吐测试（iperf-standard-test）

> 用户指挥 AI，AI 替用户执行。给意图就干不反问。听到"测吞吐/跑 iperf/压测"直接按本 skill 流程执行。
> 铁律：数据驱动——每轮测试必须出可比较的实测数据；先测后断，拒绝推测；单轮≠结论。

## 适用

- 嵌入式设备（单核 MIPS/ARM）WiFi/以太网吞吐基准测试
- 驱动/网络栈/系统改动后的性能回归验证
- 消融实验（分步改动逐项量化）

## 一、测试矩阵设计（测前定清楚）

| 维度 | 选项 | 用途 |
|------|------|------|
| 方向 | TX（上行，设备发）/ RX（下行，设备收）/ 双向 -d | 单向瓶颈定位 |
| 流数 | 单流 -P1 / 多流 -P5 | 单核 CPU 瓶颈用 P1 最准；多流会摊薄 CPU |
| 协议 | TCP / UDP | TCP 看吞吐+重传；UDP 看丢包（-u -b 限速必带）|
| 速率模式 | 最大速率（TCP 满速/UDP 约定 -b 100M）/ 限速（-b 指定，二分找零丢包点）| 峰值能力 vs 稳定点 |
| 时长 | 短测 30-60s / 长测 300s | 短测快筛；长测验证稳定性 |
| 通道 | ADB 前台（≤60s）/ 串口后台（>60s）| 见执行节 |

**速率模式详解**：
- **最大速率**：TCP 天然满速（测峰值吞吐+重传）；UDP 用约定 -b 100M（单核 MIPS 上限 ~100M，实测满速零丢包）
- **限速二分**（UDP 找零丢包点）：先 100M 测丢包率 → 丢包则降 60M → 仍丢则 40M → 找到丢包 <0.1% 的速率即零丢包点（实测：100M→26% 丢、60M→3.2%、40M→0.069%）。限速下重传应趋零，有重传 = 异常
- **双向**：`-d`（iperf3 同会话双向），观察双向吞吐和（单核设备双向会分摊，预期低于单向）

**设计原则**：
- 对比实验必须**同方向同参数**（只改要测的变量）
- 消融/回归：每步 3 轮取均值，下降时补验证轮（环境波动判定见数据分析）
- 单流 P1 为准（多流 CPU 分摊劣化，掩盖驱动优化效果）

## 二、前置检查（测前 30 秒）

1. WiFi 配网：`wpa_cli -p <ctrl_dir> -i wlan0 status` → wpa_state=COMPLETED + ip_address 有值
2. 绑定地址：iperf 必须 `-B <wlan0_IP>`（强制走 WiFi，多网卡时双保险）
3. server 可用：`ss -tlnp | grep 5201` 本机 iperf3 -s 在跑；`iperf3: error - the server is busy` 是重试信号不是失败
4. /tmp 工具：iperf3 二进制存在（烧录后必重推，死链接检查 `ls -l /tmp/iperf3`）
5. **设备默认流数陷阱**：09-02 起设备 `/data/iperf3` 为默认 P5 重编版（num_streams 1→5，src/iperf_api.c，commit 4598bf8；**重刷镜像回退工程单流版**）——跑不带 `-P` 的裸命令得到的是 5 流结果；判单流性能必须显式 `-P 1`（下方模板已全显式，勿在裸命令上省参数）

## 三、执行（通道选择铁律）

| 通道 | 时长 | 方式 | 注意 |
|------|------|------|------|
| ADB 前台 | ≤60s | `timeout 45 adb -s <IP> shell '/tmp/iperf3 -c <S> -B <WLAN> -t 30 -P 5'` | 不用 `&`（SIGHUP 杀）|
| 串口后台 | >60s | 脚本 push 到设备 → 串口持久 shell `sh /tmp/test.sh &` | 无 nohup 的 busybox 用 `&` 即可 |

**标准命令模板**：
```bash
# TCP TX（5 流，30s）
timeout 45 adb -s <IP>:5555 shell '/tmp/iperf3 -c <SERVER> -B <WLAN_IP> -t 30 -P 5'
# TCP RX
... -t 30 -P 5 -R
# 双向（-d，单核设备双向分摊，预期 < 单向）
... -t 30 -P 5 -d
# UDP TX 最大速率（约定 -b 100M）
... -u -b 100M -t 30 -P 1
# UDP 限速二分（找零丢包点：100M → 60M → 40M）
... -u -b 60M -t 30 -P 1
# TCP 限速（-b 指定，限速下重传应趋零）
... -b 50M -t 30 -P 1
# 300s 长测（串口后台 + wpa 全程采样）
sh /tmp/tx300.sh &   # 脚本内含 iperf3 300s + 完成标记
```

## 四、数据分析（核心）

### 4.1 取数

```bash
# 汇总行（吞吐 + 重传）
grep "SUM" test.log | tail -2
# 逐秒趋势（爬坡检查）
grep -E "\[SUM\]" test.log | awk '{print $4, $5, $6, $7}'
```

### 4.2 分析四查

1. **完成性**：`iperf Done.` + SUM 行存在 = 测试完整；无 Done = 中途断连（掉线红线上报）
2. **爬坡**：首秒吞吐 vs 全程均值——首秒 ≥80% 均值 = 无爬坡（TCP 窗口到位）；首秒低持续爬升 = 窗口/BDP 不足
3. **重传率**：`retr` 列——重传高 = 无线环境差（AP 干扰），不是驱动问题；对比轮次间重传差异判断环境波动
4. **丢包**：UDP `0/147884 (0%)` 格式——RX 高限速丢包是设计内背压（TCP 有重传吸收，UDP 无）；丢包判定用 wpa_state 全程 COMPLETED + TX 零丢包 + TCP 正常

### 4.3 观察项全清单（按测试类型）

| 测试类型 | 观察项 | 判定 |
|---------|--------|------|
| TCP 最大速率 | 吞吐峰值 / retr 重传 / 爬坡 | 吞吐达基线；重传高=环境 |
| TCP 限速（-b） | 吞吐=限速值？/ retr 应趋零 | 限速下重传 >0 = 异常（窗口/驱动问题）|
| UDP 最大速率 | 吞吐 vs -b / 丢包率 / jitter | 丢包率归因（背压 vs 链路）|
| UDP 限速二分 | 各档丢包率 → 零丢包点 | 找到 <0.1% 丢的档位 |
| 双向 -d | 双向吞吐和 / 单向占比 | 单核预期 < 单向，双向和 ≈ 单核上限 |
| 长测 300s | Done / wpa 采样 / 重传累积 | 零掉线 + Done rc=0 |

**jitter**（UDP 输出列，实时流关键）：`0.487 ms` 格式——波动增大预示队列延迟，配合丢包率看链路质量。

### 4.4 环境波动判别（消融/回归必做）

```
某改动后吞吐下降？
  ├─ 重传率明显升高 → 无线环境波动，补测验证（同时段交替测 3 轮）
  ├─ 重传率持平 → 真回归，检查改动
  └─ 单轮下降不可信，必须补验证轮
```

**对比判据**：多轮取均值（3 轮 ×30s），CV>5% 时不可信需补测；跨时段（>30min）对比天然不可靠，须同时段交替测。

### 4.5 伴随指标采集（嵌入式单核必备，归因关键）

**只测 iperf 吞吐不够**——单核 MIPS 设备吞吐是 CPU/驱动/系统三者共同结果，必须有伴随指标才能归因"慢在哪"：

```bash
# ① CPU 负载（测前/测中/测后各采一次）
cat /proc/loadavg                              # 单核 loadavg >1 = 过载
top -bn1 | head -8                             # 找 CPU 大户（c_mi_ipc 等应用进程）

# ② 驱动/协议栈分层丢包（区分"驱动丢" vs "协议栈丢"）
cat /proc/net/dev | grep -E "wlan0"            # rx_dropped/rx_errors
cat /proc/net/snmp | grep -A1 "Udp:"           # InErrors = 协议栈丢
# 驱动内部计数（插桩时）：dmesg | grep -c "rxq_drop\|deliver_drop\|emergency alloc"

# ③ RSSI 信号伴随（判断环境 vs 改动）
cat /proc/net/wireless                         # link/level/noise 列

# ④ 池/内存状态（池耗尽 → 吞吐骤降）
dmesg | grep -c "emergency alloc"              # 非零 = 池压力信号
cat /proc/meminfo | grep -E "MemFree|MemAvailable"
```

**归因规则**：
- loadavg 高 + c_mi_ipc 类进程吃 CPU → 系统负载问题（非驱动）
- rxq_drop/deliver_drop 恒 0 + UDP InErrors 高 → 丢包在协议栈（CPU 饱和），驱动没丢
- RSSI 波动大 + 重传高 → 环境问题
- emergency alloc 持续增长 → 池压力，稳定性风险

**实测锚点**（单核 MIPS 设备实测，2026-08）：
- 系统进程过订阅 CPU 93.9% → 同驱动差 45M（137 vs 92.5M）
- UDP RX 丢包：rxq_drop/deliver_drop 恒 0，丢在 udp_rcv CPU 饱和（InErrors）——驱动从不丢
- 单帧模式池耗尽：吞吐 45M 持续崩到 28M（emergency 补池上限 2100）

## 五、测试报告模板

报告模板见 `templates/report-template.md`。结构：

```
标题 + 日期 + 测试人
测试环境（设备/固件版本/AP/通道/参数表）
数据表（方向×流数×轮次 → 吞吐/重传/丢包/完成）
分析（爬坡检查/重传归因/环境波动判定）
结论（PASS/FAIL + 数据支撑）
```

## 支持文件清单

- `templates/report-template.md` — 测试报告模板（YAML 头 + 数据表 + 分析 + 结论）
- `references/data-analysis-pitfalls.md` — 数据分析坑（爬坡误判/单轮陷阱/跨时段对比/重传归因）
- `scripts/iperf_bench.py` — 标准测试执行脚本（测试矩阵 → 多轮执行 → 结果汇总，isatty 双通道）
- `CHANGELOG.md` — 版本历史
