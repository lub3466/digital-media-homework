# -*- coding: utf-8 -*-
"""
gen_data.py — 生成三语言共用的同一组随机向量（float64 二进制）。

固定随机种子，保证 Python / C / Rust 读到的字节完全相同，
避免"各算各的随机数"导致结果不可比。

产物：
    data/a_f64_{n}.bin, data/b_f64_{n}.bin   (n = 1e3, 1e4, 1e5, 1e6)
"""
import os
import random
import struct

SEED = 20261116
SIZES = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]


def main():
    os.makedirs("data", exist_ok=True)
    random.seed(SEED)
    for n in SIZES:
        a = [random.uniform(-1.0, 1.0) for _ in range(n)]
        b = [random.uniform(-1.0, 1.0) for _ in range(n)]
        with open(f"data/a_f64_{n}.bin", "wb") as f:
            f.write(struct.pack(f"<{n}d", *a))
        with open(f"data/b_f64_{n}.bin", "wb") as f:
            f.write(struct.pack(f"<{n}d", *b))
        print(f"wrote data/a_f64_{n}.bin + data/b_f64_{n}.bin  ({n} x f64)")


if __name__ == "__main__":
    main()
