# 数字媒体程序设计 · 实验代码

2026 秋《数字媒体程序设计》三次实验的源码。

| 项目 | 内容 |
| --- | --- |
| 班级 | 数媒三班 |
| 姓名 | 卢文博 |
| 学号 | 2025311640 |

## 目录

```
第01讲-数制转换与存储容量估算/
    estimate.py      数制互转与照片/音频/视频容量估算，含 assert 自检
第02讲-主机配置单/
    config_calc.py   128B 模型的权重 / KV cache / 带宽 / 三方案成本复算
第03讲-矩阵乘法四层实现/
    matmul.c         C 三重循环
    matmul.v          Verilog 组合逻辑（generate + genvar，9 个乘法器）
    tb_matmul.v       testbench
    matmul.cu         CUDA 核函数（1 线程算 1 个 C[i][j]）
    matmul_musa.cu    MUSA 迁移版（只改 11 行前缀）
    matmul_bench.c    N=256 循环顺序基准（i-j-k vs i-k-j）
    matmul_O0.s       gcc -S -O0 输出
    matmul_O2.s       gcc -S -O2 输出
第04讲-Scaled Dot-Product 效率对比/
    lab04_bench/      点积 Python/C/Rust 三实现 + 统一计时基准
```

## 运行

```bash
# 第 01 / 02 讲：只依赖 Python 3 标准库
python 第01讲-数制转换与存储容量估算/estimate.py
python 第02讲-主机配置单/config_calc.py

# 第 03 讲：需要 gcc、Icarus Verilog（CUDA 需 Toolkit，可选）
gcc 第03讲-矩阵乘法四层实现/matmul.c -O2 -o matmul.exe && ./matmul.exe
iverilog -g2012 -o tb.vvp 第03讲-矩阵乘法四层实现/tb_matmul.v 第03讲-矩阵乘法四层实现/matmul.v && vvp tb.vvp
```

退出码 0 表示全部自检通过。

## 两个脚本各自做了什么

**estimate.py（第 01 讲）**

- 10110101(2) → 181(10)，255(10) → FF(16)，1A(16) → 11010(2) → 26(10)，三组结果逐条打印位权展开过程
- 1920×1080×24 bit 照片 = 6,220,800 B = 6.22 MB = 5.93 MiB
- 4 min、44.1 kHz/16 bit/双声道音频 = 42,336,000 B = 42.34 MB = 40.37 MiB
- 2 h、8 Mbps 视频 = 7.2×10⁹ B = 7.20 GB = 6.71 GiB
- 生成 1080×2400 界面样张，实测 PNG 压缩比（默认 14.9:1）
- 最后跑 8 条 assert，全部通过才返回 0

**config_calc.py（第 02 讲）**

- 128B 模型 INT4 / INT8 / FP16 权重 = 64.0 / 128.0 / 256.0 GB
- 32K 上下文 KV cache = 2.00 GiB/请求，单请求总需求 63.6 GiB，32 GiB 单卡缺口 31.6 GiB
- 按「显存占比 × 带宽取调和平均」估三种方案的出词：A 8 / B 14 / C 27 tok/s
- 三方案总价 51,192 / 23,999 / 79,791 元，每万元 tok/s 1.56 / 5.83 / 3.38
- 本地 3 年 53,820 元 vs 全云 3 年 68,985 元

**matmul 四层（第 03 讲）**

- 同一组 A、B，四份实现输出完全一致：30/24/18、84/69/54、138/114/90
- 内层乘加 `s += a[i][k]*b[k][j]` = 1 条 imull + 1 条 addl；-O0 326 行 → -O2 214 行
- N=256 下 i-k-j 比 i-j-k 快 1.9×（缓存命中）
- MUSA 迁移只改 11 行 cuda* → musa* 前缀

**dot 三语言（第 04 讲）**

- 同一份 data/*.bin，三版 result/checksum 逐位一致，边界用例 5/5
- C 与 Rust 稳定在纯 Python 的约 68×（N=10^4~10^6，内存带宽受限）
- 计时协议：预热 10 轮 + 200 轮取 min（噪声只加时间，min 最稳），两轮偏差 <5%
- 依赖：Python 3.13 / gcc 16.2.0 / Rust 1.100.0（均为标准库，无第三方）

## 说明

- 价格口径：2026-11-10 电商自营含税参考价，波动 ±5%
- 出词速度是「带宽模型 + 折损系数」的估算，不是真机实测；折损系数的取值写在脚本注释里
- 报告里的「截图」是脚本输出的控制台记录渲染成的图，内容与真实运行结果一致
