# -*- coding: utf-8 -*-
"""
第 01 讲 · 计算机核心结构 —— 数制转换与存储容量估算
estimate.py：把纸上的手算结果交给机器复算，再统一按公式估算存储体积。

用法：
    python estimate.py                    # 完整复算 + 估算 + 生成截图样张
    python estimate.py --no-image         # 不生成截图样张
    python estimate.py --image shot.png   # 用真实截图替换内置样张

设计约定：
    1. 所有“手算结果”先写成常量，再用 assert 与 Python 内置函数比对，
       脚本能跑通就说明手算无误；
    2. 容量一律先算 bit、再折成 byte，最后分别给出十进制（10^3）与
       二进制（2^10）两种口径，避免 MB / MiB 混用；
    3. 只依赖标准库，可直接拷到任何装有 Python 3 的机器上运行。
"""

import argparse
import os
import struct
import sys
import unicodedata
import zlib

# ---------------------------------------------------------------- 输出工具

BAR = "─" * 64
OK = "√"


def dw(text):
    """按终端显示宽度计数：中日韩全角字符算 2 列。"""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
               for c in str(text))


def pad(text, width, align="l"):
    text = str(text)
    gap = " " * max(0, width - dw(text))
    return text + gap if align == "l" else gap + text


def rule(char="─", width=64):
    print(char * width)


def section(title):
    print()
    print(title)
    rule()


def line(label, value="", width=14):
    print("   " + pad(label, width) + str(value))


def col_row(label, cells, cell_w=6, label_w=14):
    print("   " + pad(label, label_w) + "".join(pad(c, cell_w, "r") for c in cells))


# ---------------------------------------------------------------- 单位换算

def mb(n):      # 十进制：10^6
    return n / 10 ** 6


def mib(n):     # 二进制：2^20
    return n / 2 ** 20


def gb(n):
    return n / 10 ** 9


def gib(n):
    return n / 2 ** 30


def dev_pct(a, b):
    """二进制口径相对十进制口径的偏差。"""
    return (a - b) / a * 100


# ---------------------------------------------------------------- 一、数制转换

BIN_SRC = "10110101"     # 待转换的二进制串
DEC_EXPECT = 181         # 手算结果：十进制
HEX_SRC = 255            # 待转换的十进制数
HEX_EXPECT = "FF"        # 手算结果：十六进制
HEX2_SRC = "1A"          # 待转换的十六进制串
BIN2_EXPECT = "11010"    # 手算结果：二进制
DEC2_EXPECT = 26         # 1A(16) 的十进制值


def num_systems():
    section("【1】数制转换：手算结果的复算")

    # 1.1 二进制 -> 十进制，逐位写权
    bits = [int(c) for c in BIN_SRC]
    n = len(bits)
    weights = [2 ** (n - 1 - k) for k in range(n)]
    products = [bits[k] * weights[k] for k in range(n)]
    total = sum(products)

    print("1.1  二进制 → 十进制：0b%s = ?（按权展开，权为 2 的幂）" % BIN_SRC)
    col_row("位序 i", range(n - 1, -1, -1))
    col_row("数码 d", bits)
    col_row("权值 2^i", weights)
    col_row("d × 2^i", products)
    print("   " + pad("求和", 14) + " + ".join(str(p) for p in products) + " = %d" % total)
    line("Python 验算", "int('%s', 2) = %d" % (BIN_SRC, total))
    assert total == DEC_EXPECT, "1.1 手算结果与 bincount 不一致"
    print("   " + pad("结论", 14) + "%s(2) = %d(10)   %s 与手算一致" % (BIN_SRC, total, OK))

    # 1.2 十进制 -> 十六进制，除 16 取余、逆序排列
    print()
    print("1.2  十进制 → 十六进制：%d(10) = ?（除 16 取余，逆序排列）" % HEX_SRC)
    digits = "0123456789ABCDEF"
    steps, rest, rems = [], HEX_SRC, []
    while True:
        q, r = divmod(rest, 16)
        rems.append(r)
        steps.append("   %4d ÷ 16 = %3d  … 余 %2d → %s" % (rest, q, r, digits[r]))
        rest = q
        if q == 0:
            break
    print("\n".join(steps))
    hex_str = "".join(digits[r] for r in reversed(rems))
    print("   " + pad("结果", 14) + "高位到低位：%s，验算 %d × 16 + %d = %d"
          % (hex_str, int(hex_str[0], 16), int(hex_str[1], 16), int(hex_str, 16)))
    assert hex_str == HEX_EXPECT
    print("   " + pad("结论", 14) + "%d(10) = %s(16)   hex(%d) = %s   %s 与手算一致"
          % (HEX_SRC, hex_str, HEX_SRC, hex(HEX_SRC), OK))

    # 1.3 十六进制 -> 二进制，一位拆四位
    print()
    print("1.3  十六进制 → 二进制：%s(16) = ?（一位十六进制拆成四位）" % HEX2_SRC)
    for ch in HEX2_SRC:
        print("   %s → %s" % (ch, format(int(ch, 16), "04b")))
    bin_str = "".join(format(int(ch, 16), "04b") for ch in HEX2_SRC).lstrip("0")
    dec2 = int(HEX2_SRC, 16)
    print("   " + pad("拼接", 14) + " ".join(format(int(ch, 16), "04b") for ch in HEX2_SRC)
          + " → 去掉前导 0 → " + bin_str)
    line("Python 验算", "int('%s', 16) = %d，bin(%d) = %s" % (HEX2_SRC, dec2, dec2, bin(dec2)))
    assert bin_str == BIN2_EXPECT and dec2 == DEC2_EXPECT
    print("   " + pad("结论", 14) + "%s(16) = %s(2) = %d(10)   %s 与手算一致"
          % (HEX2_SRC, bin_str, dec2, OK))


# ---------------------------------------------------------------- 二、容量估算

PHOTO_W, PHOTO_H, PHOTO_BPP = 1920, 1080, 24          # 1920×1080，24 位真彩
AUDIO_FS, AUDIO_BITS, AUDIO_CH, AUDIO_MIN = 44100, 16, 2, 4   # 44.1 kHz / 16 bit / 双声道 / 4 min
VIDEO_BPS, VIDEO_HOUR = 8 * 10 ** 6, 2                # 8 Mbps，2 小时
SHOT_W, SHOT_H = 1080, 2400                           # 待核对的截图分辨率


def photo_bytes():
    return PHOTO_W * PHOTO_H * PHOTO_BPP // 8


def audio_rate_bytes():
    return AUDIO_FS * (AUDIO_BITS // 8) * AUDIO_CH


def audio_bytes():
    return audio_rate_bytes() * AUDIO_MIN * 60


def video_bytes():
    return VIDEO_BPS * VIDEO_HOUR * 3600 // 8


def shot_raw_bytes():
    return SHOT_W * SHOT_H * 3


# ----- 生成一张 1080×2400 的界面样张（纯标准库写 PNG）

def _png_chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path, width, height, rows):
    raw = bytearray()
    for row in rows:
        raw += b"\x00" + row          # 每行不做滤波，交给 zlib
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _png_chunk(b"IEND", b"")
    with open(path, "wb") as fp:
        fp.write(png)


def png_size(path):
    """只读 IHDR 拿分辨率，返回 (宽, 高, 文件字节数)。"""
    with open(path, "rb") as fp:
        head = fp.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h, os.path.getsize(path)


def make_sample_png(path, width=SHOT_W, height=SHOT_H):
    """画一张典型手机界面：渐变壁纸 + 纯色卡片 + 一块带噪声的缩略图。

    纯色卡片让 PNG 压得很狠，噪声缩略图又逼着它压不动，
    这样得到的压缩比才接近真实截图，而不是纯色图的极端值。
    """
    rows = []
    for y in range(height):
        t = y / height
        base = (int(16 + 46 * t), int(28 + 30 * t), int(58 + 96 * t))
        rows.append(bytes(base) * width)

    def fill(y0, y1, x0, x1, color):
        seg = bytes(color) * (x1 - x0)
        for y in range(y0, y1):
            row = bytearray(rows[y])
            row[x0 * 3:x1 * 3] = seg
            rows[y] = bytes(row)

    fill(0, 96, 0, width, (10, 18, 34))              # 状态栏
    fill(96, 300, 0, width, (24, 42, 76))            # 标题栏
    fill(96, 104, 0, width, (58, 96, 160))           # 标题栏分隔线

    # 三张内容卡片
    card_y = 1180
    for i in range(3):
        y0 = card_y + i * 300
        fill(y0, y0 + 250, 60, width - 60, (250, 251, 253))
        for k in range(3):                            # 卡片里的“文字行”
            ty = y0 + 60 + k * 56
            fill(ty, ty + 22, 120, 120 + (620, 480, 760)[k], (206, 214, 226))
        fill(y0 + 250, y0 + 254, 60, width - 60, (232, 237, 244))

    # 带噪声的“照片缩略图”，模拟照片区域
    tx0, tx1, ty0, ty1 = 180, 900, 360, 1080
    seed = 20261110
    for y in range(ty0, ty1):
        row = bytearray(rows[y])
        t = (y - ty0) / (ty1 - ty0)
        for x in range(tx0, tx1):
            seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
            noise = (seed >> 16) % 25 - 12
            base_r = int(60 + 150 * t)
            base_g = int(120 + 90 * (1 - t))
            base_b = int(190 - 80 * t)
            o = x * 3
            row[o] = max(0, min(255, base_r + noise))
            row[o + 1] = max(0, min(255, base_g + noise))
            row[o + 2] = max(0, min(255, base_b + noise))
        rows[y] = bytes(row)

    fill(height - 120, height, 0, width, (12, 20, 38))   # 底部导航栏
    write_png(path, width, height, rows)
    return path


def capacity(shot_path=None, make_shot=True):
    section("【2】存储容量估算")

    print("公式：照片 S = 宽 × 高 × 位深 ÷ 8")
    print("      音频 S = 采样率 × (位深 ÷ 8) × 声道数 × 时长")
    print("      视频 S = 码率 × 时长 ÷ 8")
    print("换算：1 MB = 10^6 B，1 MiB = 2^20 B，1 GB = 10^9 B，1 GiB = 2^30 B")

    # 2.1 照片
    pb = photo_bytes()
    print()
    print("2.1  未压缩照片：%d × %d，%d 位" % (PHOTO_W, PHOTO_H, PHOTO_BPP))
    line("像素数", "= %d × %d = %s px" % (PHOTO_W, PHOTO_H, format(PHOTO_W * PHOTO_H, ",")))
    line("字节数", "= %s × %d ÷ 8 = %s B"
         % (format(PHOTO_W * PHOTO_H, ","), PHOTO_BPP, format(pb, ",")))
    line("十进制", "= %s ÷ 10^6 = %.2f MB  → 约 6.2 MB" % (format(pb, ","), mb(pb)))
    line("二进制", "= %s ÷ 2^20 = %.2f MiB → 约 5.9 MiB" % (format(pb, ","), mib(pb)))
    line("口径偏差", "= (%.2f - %.2f) ÷ %.2f = %.1f%%"
         % (mb(pb), mib(pb), mb(pb), dev_pct(mb(pb), mib(pb))))
    assert pb == 6_220_800

    # 2.2 音频
    rate, sec = audio_rate_bytes(), AUDIO_MIN * 60
    ab = audio_bytes()
    print()
    print("2.2  音频：%d 分钟，%.1f kHz / %d bit / %d 声道"
          % (AUDIO_MIN, AUDIO_FS / 1000, AUDIO_BITS, AUDIO_CH))
    line("每秒字节", "= %s × (%d ÷ 8) × %d = %s B/s"
         % (format(AUDIO_FS, ","), AUDIO_BITS, AUDIO_CH, format(rate, ",")))
    line("码率", "= %s × 8 = %s bit/s = %.1f kbps"
         % (format(rate, ","), format(rate * 8, ","), rate * 8 / 1000))
    line("总字节", "= %s × %d = %s B" % (format(rate, ","), sec, format(ab, ",")))
    line("", "= %.2f MB = %.2f MiB" % (mb(ab), mib(ab)))
    assert ab == 42_336_000

    # 2.3 视频
    vb = video_bytes()
    secs = VIDEO_HOUR * 3600
    print()
    print("2.3  视频：%d 小时，%d Mbps" % (VIDEO_HOUR, VIDEO_BPS // 10 ** 6))
    line("时长", "= %d × 3600 = %s s" % (VIDEO_HOUR, format(secs, ",")))
    line("总比特", "= %s × %s = %s bit" % (format(VIDEO_BPS, ","), format(secs, ","), format(VIDEO_BPS * secs, ",")))
    line("总字节", "= %s ÷ 8 = %s B" % (format(VIDEO_BPS * secs, ","), format(vb, ",")))
    line("", "= %.2f GB = %.2f GiB = %s MB" % (gb(vb), gib(vb), format(vb // 10 ** 6, ",")))
    assert vb == 7_200_000_000

    # 2.4 截图核对
    print()
    print("2.4  截图核对：未压缩 vs 实际文件")
    raw = shot_raw_bytes()
    line("未压缩", "= %d × %d × 3 = %s B = %.2f MB" % (SHOT_W, SHOT_H, format(raw, ","), mb(raw)))

    if shot_path is None:
        shot_path = "screenshot_sample.png"
        if make_shot and not os.path.exists(shot_path):
            print("   " + "（生成 %d × %d 界面样张…）" % (SHOT_W, SHOT_H))
            make_sample_png(shot_path)

    info = png_size(shot_path) if os.path.exists(shot_path) else None
    if info is None:
        print("   " + "未找到图片，跳过实际体积比对（可用 --image 指定）")
        return
    w, h, size = info
    line("实际文件", "%s  %d × %d，%s B = %.2f MB"
         % (os.path.basename(shot_path), w, h, format(size, ","), mb(size)))
    line("压缩比", "= %s ÷ %s = %.1f : 1（字节）"
         % (format(raw, ","), format(size, ","), raw / size))
    line("说明", "PNG 无损，界面大面积纯色，故仍可压到 1/%.0f；" % (raw / size))
    line("", "照片类截图含细节，压缩比会明显低于此值。")


# ---------------------------------------------------------------- 三、两种口径

def unit_table():
    section("【3】同一体积的两种写法（MB / MiB）")
    rows = [
        ("未压缩照片", photo_bytes()),
        ("4 分钟音频", audio_bytes()),
        ("2 小时视频", video_bytes()),
        ("截图未压缩", shot_raw_bytes()),
    ]

    def two_ways(n):
        if n >= 10 ** 9:
            return "%.2f GB" % gb(n), "%.2f GiB" % gib(n)
        return "%.2f MB" % mb(n), "%.2f MiB" % mib(n)

    print("   " + pad("项目", 13) + pad("字节数 B", 14, "r") + pad("十进制", 11, "r")
          + pad("二进制", 11, "r") + pad("偏差", 8, "r"))
    print("   " + "┄" * 56)
    for name, n in rows:
        dec, binary = two_ways(n)
        print("   " + pad(name, 13) + pad(format(n, ","), 14, "r")
              + pad(dec, 11, "r") + pad(binary, 11, "r")
              + pad("%.1f%%" % dev_pct(mb(n), mib(n)), 8, "r"))


# ---------------------------------------------------------------- 四、拓展

def extension():
    section("【4】拓展：256 GB 手机能存多少张照片")
    cap = 256 * 10 ** 9
    line("按未压缩 6.22 MB/张", "= 256×10^9 ÷ 6.22×10^6 = %s 张"
         % format(int(cap / photo_bytes()), ","), width=20)
    line("按 JPEG 2.0 MB/张", "= 256×10^9 ÷ 2.0×10^6 = %s 张"
         % format(int(cap / 2.0e6), ","), width=20)
    line("若再存 4K 视频", "= 60 Mbps × 3600 s ÷ 8 = %.0f GB/小时"
         % gb(60e6 * 3600 / 8), width=20)


# ---------------------------------------------------------------- 五、自检

def self_check():
    section("【5】自检：assert 逐条比对")
    cases = [
        ("int('10110101', 2) == 181", int(BIN_SRC, 2) == DEC_EXPECT),
        ("hex(255) == '0xff'", hex(HEX_SRC) == "0xff"),
        ("int('1A', 16) == 26", int(HEX2_SRC, 16) == DEC2_EXPECT),
        ("bin(26) == '0b11010'", bin(DEC2_EXPECT) == "0b" + BIN2_EXPECT),
        ("照片 == 6,220,800 B", photo_bytes() == 6_220_800),
        ("音频 == 42,336,000 B", audio_bytes() == 42_336_000),
        ("视频 == 7,200,000,000 B", video_bytes() == 7_200_000_000),
        ("截图未压缩 == 7,776,000 B", shot_raw_bytes() == 7_776_000),
    ]
    passed = 0
    for expr, good in cases:
        print("   " + pad(expr, 34) + (OK if good else "×"))
        passed += bool(good)
    print("   " + pad("全部通过", 34) + "%d / %d" % (passed, len(cases)))
    return passed == len(cases)


# ---------------------------------------------------------------- main

def main(argv=None):
    parser = argparse.ArgumentParser(description="数制转换与存储容量估算验证脚本")
    parser.add_argument("--image", metavar="PNG", help="用真实截图替换内置样张")
    parser.add_argument("--no-image", action="store_true", help="不生成截图样张")
    args = parser.parse_args(argv)

    print(BAR)
    print("  第 01 讲 · 数制转换与存储容量估算  ——  验证脚本")
    print("  Python %s  |  %s" % (sys.version.split()[0], os.name == "nt" and "Windows" or sys.platform))
    print("  运行：python estimate.py")
    print(BAR)

    num_systems()
    capacity(shot_path=args.image, make_shot=not args.no_image)
    unit_table()
    extension()
    ok = self_check()

    print()
    rule("═")
    print("  结论：三组数制转换与三类容量估算均与手算一致（%s）" % (OK if ok else "存在不一致"))
    print("  提醒：报告里写容量必须注明口径，MB 与 MiB 相差约 4.6%。")
    rule("═")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
