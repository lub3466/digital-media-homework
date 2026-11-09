# -*- coding: utf-8 -*-
"""
第 02 讲 · 外围系统与 AI 算力 —— 主机配置单的容量与成本复算
config_calc.py

用途：把「模型能不能装下、能跑多快、值不值这个价」三件事算清楚，
      避免只凭电商页面上的 TOPS 数字拍脑袋。

用法：
    python config_calc.py

约定：
    1. 模型体积按 GB（10^9 B）给出，显存/内存容量按 GiB（2^30 B）核对，
       两者换算关系写在同一行，别再混用（第 01 讲的坑）；
    2. 出词速度先用「每 token 读取字节数 ÷ 有效带宽」算理论上限，
       再乘一个折损系数，折损系数的来源写在注释里；
    3. 价格取 2026-11-10 电商自营参考价，含税，波动 ±5%。
"""

import sys

# ---------------------------------------------------------------- 输出工具

BAR = "─" * 64
OK = "√"

GI = 2 ** 30          # 1 GiB
GB = 10 ** 9          # 1 GB


def dw(text):
    """终端显示宽度：全角字符算 2 列。"""
    return sum(2 if unicodedata_east(c) else 1 for c in str(text))


def unicodedata_east(c):
    import unicodedata
    return unicodedata.east_asian_width(c) in ("W", "F")


def pad(text, width, align="l"):
    text = str(text)
    gap = " " * max(0, width - dw(text))
    return text + gap if align == "l" else gap + text


def rule(char="─"):
    print(char * 64)


def section(title):
    print()
    print(title)
    rule()


# ---------------------------------------------------------------- 一、容量

PARAMS = 128e9            # 128B 总参数
ACTIVE = 10e9             # MoE 每 token 激活约 10B
CTX = 32768               # 32K 上下文
LAYERS = 64               # 层数
KV_HEADS = 4              # GQA 的 KV 组数
HEAD_DIM = 128            # 每头维度
KV_BYTES = 1              # KV 用 INT8 存，每元素 1 B
OVERHEAD = 2.0            # 框架 + 激活 + 显存碎片，GiB


def weight_bytes(bits):
    return PARAMS * bits / 8


def kv_bytes(ctx=CTX, elem=KV_BYTES):
    return LAYERS * KV_HEADS * HEAD_DIM * 2 * elem * ctx


def gib(n):
    return n / GI


def num(n, nd=1):
    return format(round(n, nd), ",")


def capacity():
    section("【1】容量推导：128B 模型 + 32K 上下文要占多少")

    print("权重 = 参数量 × 位宽 ÷ 8")
    for bits, name in ((4, "INT4"), (8, "INT8"), (16, "FP16")):
        b = weight_bytes(bits)
        print("   %s：128B × %2d bit ÷ 8 = %7.1f GB = %6.1f GiB"
              % (pad(name, 4), bits, b / GB, gib(b)))

    kv = kv_bytes()
    print()
    print("KV cache = 层数 × KV 组数 × 头维 × 2 × 元素字节 × 上下文")
    print("        = %d × %d × %d × 2 × %d B × %d"
          % (LAYERS, KV_HEADS, HEAD_DIM, KV_BYTES, CTX))
    print("        = %s B = %.2f GiB / 请求（FP16 翻倍 %.2f GiB）"
          % (format(int(kv), ","), gib(kv), gib(kv) * 2))

    need = gib(weight_bytes(4)) + gib(kv) + OVERHEAD
    print()
    print("单请求总需求 = %.1f（权重）+ %.2f（KV）+ %.1f（框架）= %.1f GiB"
          % (gib(weight_bytes(4)), gib(kv), OVERHEAD, need))
    print("双并发请求   = %.1f GiB" % (need + gib(kv)))
    print("32 GiB 单卡缺口 = %.1f - 32 = %.1f GiB（%.0f%% 的权重放不下）"
          % (need, need - 32, (need - 32) / need * 100))
    return need


# ---------------------------------------------------------------- 二、带宽

BW_5090 = 1792.0          # GB/s，GDDR7 512-bit
BW_DDR5 = 96.0            # GB/s，双通道 DDR5-6000 实测
BW_UNIFIED = 256.0        # GB/s，LPDDR5X-8000 256-bit


def per_token_gb():
    """每生成 1 个 token 需要读过的权重（INT4）。"""
    return ACTIVE * 0.5 / GB


def theoretical(bw):
    return bw / per_token_gb()


def bandwidth(need):
    section("【2】带宽决定出词：把「装得下」换算成「跑多快」")

    print("每 token 读过的权重 = 激活参数 × 0.5 B = %.0f B × 0.5 = %.1f GB"
          % (ACTIVE / 1e9, per_token_gb()))
    print("理论出词 = 有效带宽 ÷ 每 token 字节数")
    print()
    print("   " + pad("设备", 22) + pad("带宽 GB/s", 12, "r") + pad("理论 tok/s", 12, "r"))
    print("   " + "┄" * 50)
    for name, bw in (("RTX 5090 GDDR7", BW_5090),
                     ("DDR5-6000 双通道", BW_DDR5),
                     ("统一内存 LPDDR5X", BW_UNIFIED)):
        print("   " + pad(name, 22) + pad("%.0f" % bw, 12, "r")
              + pad("%.0f" % theoretical(bw), 12, "r"))

    # 三种方案的显存占比与折损系数
    share_a = 28 / need                      # 28 GiB 热层上卡
    share_b = 1.0
    share_c = min(1.0, 62 / need)            # 双卡扣掉驱动/框架只剩 62 GiB
    k_a, k_b, k_c = 0.24, 0.28, 0.11         # 折损：调度、KV 读写、双卡通信

    def effective(share):
        """两种介质串联，等效带宽取调和平均：t = 一部分走显存 + 一部分走内存。"""
        return 1.0 / (share / BW_5090 + (1 - share) / BW_DDR5)

    t_a = effective(share_a)
    t_b = BW_UNIFIED
    t_c = effective(share_c)

    print()
    print("三种方案（显存占比 × 对应带宽取调和平均，再乘折损系数）：")
    print("   " + pad("方案", 18) + pad("显存占比", 10, "r") + pad("等效带宽", 10, "r")
          + pad("折损", 8, "r") + pad("估出词", 8, "r"))
    print("   " + "┄" * 54)
    for name, s, bw, k in (("A 单卡 32G 分层", share_a, t_a, k_a),
                           ("B 统一内存 128G", share_b, t_b, k_b),
                           ("C 双卡 64G", share_c, t_c, k_c)):
        print("   " + pad(name, 18) + pad("%.0f%%" % (s * 100), 10, "r")
              + pad("%.0f" % bw, 10, "r") + pad("%.2f" % k, 8, "r")
              + pad("%.0f" % (bw / per_token_gb() * k), 8, "r"))
    return {"A": round(t_a / per_token_gb() * k_a),
            "B": round(t_b / per_token_gb() * k_b),
            "C": round(t_c / per_token_gb() * k_c)}


# ---------------------------------------------------------------- 三、成本

PLANS = {
    "A 单卡 32G + 128G 内存": {
        "RTX 5090 32G 显卡": 25999,
        "Ryzen 9 9950X": 4299,
        "X870E 主板": 2599,
        "DDR5-6000 64G×2": 13999,
        "2TB PCIe 5.0 SSD": 1299,
        "1200W 白金电源": 1499,
        "360 水冷": 699,
        "全塔机箱": 799,
    },
    "B 统一内存迷你主机": {
        "锐龙 AI Max+ 395 迷你主机（128G 统一内存 / 2TB）": 23999,
    },
    "C 双卡 64G": {
        "RTX 5090 32G × 2": 51998,
        "Ryzen 9 9950X": 4299,
        "X870E 双卡主板": 3299,
        "DDR5-6000 64G×2": 13999,
        "2TB PCIe 5.0 SSD": 1299,
        "1600W 钛金电源": 3299,
        "360 水冷": 699,
        "全塔机箱": 899,
    },
}


def cost(speed):
    section("【3】三方案成本与性价比")

    totals = {}
    for name, parts in PLANS.items():
        total = sum(parts.values())
        totals[name] = total

    print("   " + pad("方案", 24) + pad("总价 元", 12, "r") + pad("出词 tok/s", 12, "r")
          + pad("每万元 tok/s", 14, "r"))
    print("   " + "┄" * 60)
    for name, total in totals.items():
        key = name[0]
        print("   " + pad(name, 24) + pad(format(total, ","), 12, "r")
              + pad(speed[key], 12, "r")
              + pad("%.2f" % (speed[key] / (total / 10000)), 14, "r"))

    print()
    a = PLANS["A 单卡 32G + 128G 内存"]
    total_a = totals["A 单卡 32G + 128G 内存"]
    gpu = a["RTX 5090 32G 显卡"]
    mem = a["DDR5-6000 64G×2"]
    plat = a["Ryzen 9 9950X"] + a["X870E 主板"] + a["2TB PCIe 5.0 SSD"]
    other = total_a - gpu - mem - plat
    print("方案 A 预算分配（指南建议 55–60 / 25 / 10 / 5）：")
    for label, value, hint in (("显卡", gpu, "55–60"), ("内存", mem, "25"),
                               ("平台 CPU+主板+SSD", plat, "10"), ("电源 散热 机箱", other, "5")):
        print("   " + pad(label, 20) + pad("%s 元" % format(value, ","), 12, "r")
              + pad("%.1f%%" % (value / total_a * 100), 9, "r") + "   建议 " + hint + "%")
    return totals


# ---------------------------------------------------------------- 四、云 vs 本地

TOKENS_DAY = 300_000        # 每天出词量
VIDEOS_DAY = 30             # 每天出片数
CLOUD_TOK = 10.0            # 元 / 百万 tokens
CLOUD_VIDEO = 2.0           # 元 / 条（768p 5s）
POWER_W = 500               # 平均整机功耗
PRICE_KWH = 0.6             # 元 / kWh
YEARS = 3


def cloud_vs_local(totals):
    section("【4】本地 vs 云：3 年总拥有成本")

    days = 365 * YEARS
    tok_cost = TOKENS_DAY * days / 1e6 * CLOUD_TOK
    vid_cost = VIDEOS_DAY * days * CLOUD_VIDEO
    cloud = tok_cost + vid_cost

    kwh = POWER_W / 1000 * 8 * days
    power = kwh * PRICE_KWH
    local = totals["A 单卡 32G + 128G 内存"] + power

    print("假设：每天 %s 万 tokens、%d 条视频，%d 年" % (TOKENS_DAY // 10000, VIDEOS_DAY, YEARS))
    print()
    print("   云端 LLM   = %.2f 亿 tokens × %.0f 元/百万 = %s 元"
          % (TOKENS_DAY * days / 1e8, CLOUD_TOK, format(round(tok_cost), ",")))
    print("   云端 H3    = %s 条 × %.0f 元/条 = %s 元"
          % (format(VIDEOS_DAY * days, ","), CLOUD_VIDEO, format(round(vid_cost), ",")))
    print("   全云合计   = %s 元" % format(round(cloud), ","))
    print()
    print("   本地整机   = %s 元" % format(totals["A 单卡 32G + 128G 内存"], ","))
    print("   电费       = %d W × 8 h × %d 天 × %.1f 元 = %s 元"
          % (POWER_W, days, PRICE_KWH, format(round(power), ",")))
    print("   本地合计   = %s 元" % format(round(local), ","))
    print()
    print("   差额 = %s - %s = %s 元（%s）"
          % (format(round(cloud), ","), format(round(local), ","),
             format(abs(round(cloud - local)), ","),
             "本地更省" if cloud > local else "云更省"))
    print("   只看 LLM：3 年云端只要 %s 元，本地整机不划算。"
          % format(round(tok_cost), ","))
    return cloud, local, tok_cost


# ---------------------------------------------------------------- 五、自检

def check(need, speed, totals, cloud, local, tok_cost):
    section("【5】自检")
    cases = [
        ("INT4 权重 64.0 GB", abs(weight_bytes(4) / GB - 64.0) < 0.05),
        ("KV/请求 2.0 GiB", abs(gib(kv_bytes()) - 2.0) < 0.05),
        ("32G 单卡装不下（缺口 > 30 GiB）", need - 32 > 30),
        ("A 出词 8 tok/s（个位数）", speed["A"] == 8),
        ("C 出词 > A 出词", speed["C"] > speed["A"]),
        ("B 每万元 tok/s 最高", speed["B"] / (totals["B 统一内存迷你主机"] / 10000)
         > speed["C"] / (totals["C 双卡 64G"] / 10000)),
        ("本地 3 年 < 全云 3 年", local < cloud),
        ("只跑 LLM 时云更省", tok_cost < local),
    ]
    passed = 0
    for expr, good in cases:
        print("   " + pad(expr, 36) + (OK if good else "×"))
        passed += bool(good)
    print("   " + pad("全部通过", 36) + "%d / %d" % (passed, len(cases)))
    return passed == len(cases)


def main():
    print(BAR)
    print("  第 02 讲 · H3 与 Strata Qwen3.8 128B 主机配置单 · 复算")
    print("  Python %s  |  价格口径：2026-11-10 电商自营含税价" % sys.version.split()[0])
    print(BAR)

    need = capacity()
    speed = bandwidth(need)
    totals = cost(speed)
    cloud, local, tok_cost = cloud_vs_local(totals)
    ok = check(need, speed, totals, cloud, local, tok_cost)

    print()
    rule("═")
    print("  结论：32 GiB 单卡必然分层；A 够用、B 最便宜但跑不了 H3、C 最快也最贵。")
    print("  提醒：本地整机只有在「要跑 H3」时才比云端划算。")
    rule("═")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

