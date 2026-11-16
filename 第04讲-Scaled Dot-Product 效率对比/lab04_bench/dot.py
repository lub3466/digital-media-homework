# -*- coding: utf-8 -*-
"""
dot.py — Python 版点积（仅标准库，纯原生语法，不开 BLAS / numpy）。

用法：python dot.py <a.bin> <b.bin> <n>

计时协议：读文件不计时；预热 10 轮后正式 200 轮，同时输出最小值与中位数；
每轮都累加校验和（checksum），保证结果被消费、不会被解释器"优化"。
"""
import statistics
import struct
import sys
import time

WARMUP = 10
ROUNDS = 200


def read_f64(path):
    with open(path, "rb") as f:
        raw = f.read()
    return struct.unpack(f"<{len(raw) // 8}d", raw)


def dot(a, b):
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} vs {len(b)}")
    # 原生生成器表达式：Python 层不写双重 for 循环（慢 20 倍以上）
    return sum(x * y for x, y in zip(a, b))


def main():
    if len(sys.argv) != 4:
        print("usage: python dot.py <a.bin> <b.bin> <n>")
        return 2
    a_path, b_path, n = sys.argv[1], sys.argv[2], int(sys.argv[3])

    a = read_f64(a_path)
    b = read_f64(b_path)
    assert len(a) == n and len(b) == n, f"length mismatch: {len(a)} vs {len(b)}"

    checksum = 0.0
    for _ in range(WARMUP):          # 预热，不进计时
        checksum += dot(a, b)

    times = []
    for _ in range(ROUNDS):
        t0 = time.perf_counter()
        checksum += dot(a, b)        # 结果被累加 → 不会被优化掉
        times.append(time.perf_counter() - t0)

    result = dot(a, b)
    median_s = statistics.median(times)
    min_s = min(times)
    print(f"lang=python n={n} result={result:.12f} checksum={checksum:.6f} "
          f"median_us={median_s * 1e6:.2f} min_us={min_s * 1e6:.2f}")


if __name__ == "__main__":
    main()
