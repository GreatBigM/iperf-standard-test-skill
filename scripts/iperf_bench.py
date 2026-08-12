#!/usr/bin/env python3
"""iperf3 标准吞吐测试执行器 — 测试矩阵 → 多轮执行 → 结果汇总。

用法（AI/管道非 TTY 通道）：
    python3 iperf_bench.py --device <IP>:5555 --server <S> --wlan-ip <WLAN_IP> \
        --direction tx --streams 5 --duration 30 --rounds 3 [--udp --rate 100M]

真实终端交互：不带参数运行进入向导。
退出码：0=全部完成；1=测试未完成（掉线/超时）；2=参数错误。
"""
import argparse
import subprocess
import sys
import time

DEFAULT_CTRL = "/tmp/wpa"


def run_cmd(cmd, timeout=50):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def precheck(device, server):
    """前置检查：wpa COMPLETED + server 可达。"""
    out = run_cmd(f"timeout 10 adb -s {device} shell 'wpa_cli -p {DEFAULT_CTRL} -i wlan0 status | grep wpa_state'")
    if "COMPLETED" not in out:
        print(f"[FAIL] wpa_state 非 COMPLETED: {out.strip()}")
        return False
    out = run_cmd(f"ss -tlnp | grep 5201")
    if not out.strip():
        print("[FAIL] 本机 iperf3 server 未运行")
        return False
    return True


def bench_round(device, server, wlan_ip, direction, streams, duration, udp, rate):
    """执行一轮 iperf3，返回 (完成, 输出全文)。"""
    extra = " -R" if direction == "rx" else ""
    if udp:
        rate_arg = f" -b {rate}" if rate else " -b 100M"
        cmd = (f"timeout {duration+15} adb -s {device} shell "
               f"'/tmp/iperf3 -c {server} -B {wlan_ip} -u{rate_arg} -t {duration} -P {streams}{extra}'")
    else:
        cmd = (f"timeout {duration+15} adb -s {device} shell "
               f"'/tmp/iperf3 -c {server} -B {wlan_ip} -t {duration} -P {streams}{extra}'")
    out = run_cmd(cmd, timeout=duration + 20)
    done = "iperf Done." in out
    return done, out


def parse_sum(out):
    """提取 SUM 汇总行。返回 (吞吐Mbps, 丢包率, jitter)。

    iperf3 输出格式：
      TCP receiver: [SUM] 0.00-30.20 sec 402 MBytes 112 Mbits/sec receiver        (len=8)
      UDP receiver: [SUM] ... sec 197 MBytes 110 Mbits/sec 0.487 ms 0/147884 (0%) receiver (len=12)
      TCP sender:   [SUM] ... sec 318 MBytes 88.9 Mbits/sec 57 (null)              (retr 在 sender 行)
    parts 索引（receiver）：[SUM]/时间/sec/字节/MBytes/速率/Mbits/sec/[jitter]/ms/[丢包]/(%)/receiver
    """
    bw = retr = loss = jitter = ""
    for line in out.splitlines():
        if "[SUM]" not in line:
            continue
        parts = line.split()
        if len(parts) < 7:
            continue
        if "receiver" in line:
            bw = parts[5]                     # 速率数值
            if len(parts) >= 12:              # UDP 行：有 jitter + 丢包列
                jitter = parts[7]
                loss = parts[9]
        elif len(parts) > 8 and "(null)" in line:  # 客户端 sender 行带 retr（尾部 (null)）
            retr = parts[7]
    return bw, retr, loss, jitter


def main():
    ap = argparse.ArgumentParser(description="iperf3 标准吞吐测试")
    ap.add_argument("--device", help="adb 设备地址 IP:5555")
    ap.add_argument("--server", default="<SERVER_IP>", help="iperf3 server（本机常驻 iperf3 -s 的 IP）")
    ap.add_argument("--wlan-ip", help="wlan0 IP（-B 绑定）")
    ap.add_argument("--direction", default="tx", choices=["tx", "rx"])
    ap.add_argument("--streams", type=int, default=5)
    ap.add_argument("--duration", type=int, default=30)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--udp", action="store_true")
    ap.add_argument("--rate", help="UDP 限速如 100M")
    args = ap.parse_args()

    if not sys.stdin.isatty() and not args.device:
        print("[ERROR] 非终端调用必须传 --device（和 --wlan-ip）")
        return 2

    if not args.device:
        args.device = input("设备 (IP:5555): ").strip()
    if not args.wlan_ip:
        if not sys.stdin.isatty():
            print("[ERROR] 非终端调用必须传 --wlan-ip（iperf 需要 -B 绑定）")
            return 2
        args.wlan_ip = input("wlan0 IP: ").strip()

    if not precheck(args.device, args.server):
        return 1

    proto = "UDP" if args.udp else "TCP"
    print(f"=== {proto} {args.direction.upper()} P{args.streams} {args.duration}s ×{args.rounds}轮 ===")
    results = []
    for i in range(1, args.rounds + 1):
        print(f"--- 轮 {i} ---", flush=True)
        done, out = bench_round(args.device, args.server, args.wlan_ip,
                                args.direction, args.streams, args.duration, args.udp, args.rate)
        bw, retr, loss, jitter = parse_sum(out)
        extra = f"  丢包:{loss}  jitter:{jitter}" if args.udp else f"  重传:{retr}"
        print(f"完成: {done}  吞吐: {bw}{extra}")
        results.append((done, bw))
        time.sleep(2)

    ok = sum(1 for d, _ in results if d)
    print(f"\n=== 汇总: {ok}/{args.rounds} 完成 ===")
    for i, (d, bw) in enumerate(results, 1):
        print(f"  轮{i}: {'OK' if d else 'FAIL'} {bw}")
    return 0 if ok == args.rounds else 1


if __name__ == "__main__":
    sys.exit(main())
