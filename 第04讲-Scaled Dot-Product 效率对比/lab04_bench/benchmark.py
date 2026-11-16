# -*- coding: utf-8 -*-
"""
benchmark.py — 统一计时编排器（仅标准库）。

职责：
  1. 对每个规模 N，调用 dot.py / dot_c / dot_rs 三份可执行文件；
  2. 用外层 perf_counter 记录每次调用的墙钟时间（含启动 + 读文件），
     与程序内部"纯计算"的耗时做对照，演示计时口径差异；
  3. 解析各程序自报的 min_us，生成 3 规模 × 3 语言对比表与加速倍数；
  4. 整个基准连跑两遍，校验两轮耗时偏差 < 5%。

统计口径：各程序内部预热 3 轮后正式 100 轮，取最小值（min）。
取 min 而不是中位数的原因见实验报告的"问题与解决"——共享混合核心
笔记本上调度抖动只会让耗时变大、不会变小，min 最接近真实计算时间，
这也是 Criterion 等专业基准库的默认做法。
"""
import re
import subprocess
import sys
import time

BASE = "."
N_SIZES = [10 ** 4, 10 ** 5, 10 ** 6]

CMDS = {
    "python": [sys.executable, f"{BASE}/dot.py"],
    "c":      [f"{BASE}/dot_c.exe"],
    "rust":   [f"{BASE}/dot_rs.exe"],
}

MIN_RE = re.compile(r"min_us=([0-9.]+)")


def run_one(lang, n):
    """启动一次，返回 (外层墙钟秒, 程序自报 min 秒)。"""
    a = f"{BASE}/data/a_f64_{n}.bin"
    b = f"{BASE}/data/b_f64_{n}.bin"
    cmd = CMDS[lang] + [a, b, str(n)]
    t0 = time.perf_counter()
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", check=True).stdout
    wall = time.perf_counter() - t0
    m = MIN_RE.search(out)
    if not m:
        print("PARSE FAIL:", lang, n, out, file=sys.stderr)
        raise SystemExit(1)
    return wall, float(m.group(1)) / 1e6


def main():
    print("统一计时协议：同一份 data/*.bin，预热 3 轮 + 正式 100 轮取最小值；")
    print("校验和逐轮消费；Python=生成器 sum，C=-O2 -static，Rust=--release。\n")

    rounds = [{}, {}]
    for rep in range(2):
        for n in N_SIZES:
            for lang in ("python", "c", "rust"):
                wall, m = run_one(lang, n)
                rounds[rep][(lang, n)] = (wall, m)

    print("两轮稳定性核对（min 相对偏差）：")
    stable = True
    for n in N_SIZES:
        for lang in ("python", "c", "rust"):
            m1 = rounds[0][(lang, n)][1]
            m2 = rounds[1][(lang, n)][1]
            dev = abs(m1 - m2) / max(m1, 1e-9) * 100
            flag = "OK " if dev < 5 else "FAIL"
            if dev >= 5:
                stable = False
            print(f"  {lang:6s} n={n:<7d}  {m1*1e6:9.2f} us vs {m2*1e6:9.2f} us  dev={dev:4.1f}%  {flag}")

    print("\n=== 耗时对比表（取第 1 轮 min） ===\n")
    print(f"{'N':>8} | {'Python (us)':>12} | {'C (us)':>10} | {'Rust (us)':>10} | "
          f"{'C 加速':>8} | {'Rust 加速':>8}")
    print("-" * 70)
    for n in N_SIZES:
        pm = rounds[0][("python", n)][1]
        cm = rounds[0][("c", n)][1]
        rm = rounds[0][("rust", n)][1]
        print(f"{n:>8} | {pm*1e6:12.2f} | {cm*1e6:10.2f} | {rm*1e6:10.2f} | "
              f"{pm/cm:7.1f}x | {pm/rm:7.1f}x")

    print("\n=== 外层 perf_counter 墙钟（含启动 + 读文件，仅作对照） ===\n")
    print(f"{'N':>8} | {'Python (ms)':>12} | {'C (ms)':>10} | {'Rust (ms)':>10}")
    print("-" * 50)
    for n in N_SIZES:
        pw = rounds[0][("python", n)][0]
        cw = rounds[0][("c", n)][0]
        rw = rounds[0][("rust", n)][0]
        print(f"{n:>8} | {pw*1e3:12.2f} | {cw*1e3:10.2f} | {rw*1e3:10.2f}")

    print("\n" + ("稳定性 OK：两轮偏差 < 5%" if stable else "稳定性 FAIL，需回到计时口径修正"))

    return 0 if stable else 1


if __name__ == "__main__":
    sys.exit(main())
