# -*- coding: utf-8 -*-
"""第 05 讲：渲染命令截图 + 绘制封装/解封装示意图。"""
import os
import unicodedata

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(HERE, "build")

BG = (12, 12, 12)
FG = (214, 214, 214)
BAR_BG = (32, 32, 32)
BAR_FG = (170, 170, 170)
BORDER = (58, 58, 58)

FONT = r"C:\Windows\Fonts\simsun.ttc"
TITLE_FONT = r"C:\Windows\Fonts\msyh.ttc"
SIZE = 20
LH = 26
PAD = 22
TITLE_H = 32


def dw(text):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in text)


def render_console(lines, out_path, title):
    font = ImageFont.truetype(FONT, SIZE, index=0)
    tfont = ImageFont.truetype(TITLE_FONT, 13, index=0)
    maxw = max(dw(l) for l in lines)
    char_w = SIZE // 2
    width = PAD * 2 + maxw * char_w
    height = TITLE_H + PAD * 2 + len(lines) * LH
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, TITLE_H], fill=BAR_BG)
    d.line([0, TITLE_H, width, TITLE_H], fill=BORDER)
    d.text((14, 9), title, font=tfont, fill=BAR_FG)
    y = TITLE_H + PAD
    for line in lines:
        d.text((PAD, y), line, font=font, fill=FG)
        y += LH
    d.rectangle([0, 0, width - 1, height - 1], outline=BORDER)
    img.save(out_path)
    return img.size


FIG1 = [
    "$ ipconfig /all",
    "  描述 . . . . . . . . : Intel(R) Wi-Fi 7 BE201 320MHz",
    "  物理地址 . . . . . . : 4C-0F-3E-7B-49-72",
    "  IPv4 地址 . . . . . . : 10.250.220.234",
    "  子网掩码 . . . . . . : 255.255.0.0",
    "  默认网关 . . . . . . : 10.250.0.1",
    "  DNS 服务器 . . . . . : 10.248.98.30",
]

FIG2 = [
    "$ ping 10.250.0.1          （默认网关）",
    "  Reply from 10.250.0.1: bytes=32 time=3ms TTL=255",
    "  Reply from 10.250.0.1: bytes=32 time=3ms TTL=255",
    "  Reply from 10.250.0.1: bytes=32 time=2ms TTL=255",
    "",
    "$ ping baidu.com          （外网）",
    "  Pinging baidu.com [111.63.65.247]",
    "  Reply from 111.63.65.247: bytes=32 time=47ms TTL=49",
    "  Reply from 111.63.65.247: bytes=32 time=44ms TTL=49",
    "  Reply from 111.63.65.247: bytes=32 time=46ms TTL=49",
    "",
    "$ nslookup baidu.com",
    "  Name: baidu.com",
    "  Addresses: 124.237.177.164, 111.63.65.247, 110.242.74.102, 111.63.65.103",
]

FIG3 = [
    "$ netstat -ano          （活动 TCP 连接，替代 Wireshark 抓包）",
    "  TCP  10.250.220.234:1024   4.145.79.81:443      ESTABLISHED",
    "  TCP  10.250.220.234:1220   39.105.251.195:443   ESTABLISHED",
    "  TCP  10.250.220.234:1165   36.248.69.35:443     TIME_WAIT",
    "  TCP  0.0.0.0:445           0.0.0.0:0            LISTENING",
    "  （源端口动态分配，目的端口 443=HTTPS / 445=SMB）",
    "",
    "$ tracert -d baidu.com     （拓展：观察跳数）",
    "  1   3 ms   3 ms   40 ms   10.250.0.1",
    "  2   *      *      *       Request timed out.",
    "  3   7 ms   *      *       120.80.167.97",
    "  （中间 * 是 ICMP 被过滤，路由器不回 TTL 超时）",
]


# ---------------------------- 封装示意图 ----------------------------
def draw_diagram(out_path):
    W, H = 1600, 760
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f18 = ImageFont.truetype(FONT, 20, index=0)
    f15 = ImageFont.truetype(FONT, 16, index=0)
    f13 = ImageFont.truetype(FONT, 14, index=0)
    f_hei = ImageFont.truetype(TITLE_FONT, 22, index=0)

    INK = (22, 44, 70)
    GRAY = (90, 107, 123)

    # 标题
    d.text((W // 2 - 260, 20), "数据「发消息」的封装与解封装", font=f_hei, fill=INK)

    # 各层配色
    layers = [
        ("应用层", "数据 Data", (214, 234, 248)),
        ("传输层", "报文段 Segment", (209, 236, 214)),
        ("网络层", "数据报 Packet", (253, 245, 205)),
        ("链路层", "帧 Frame", (250, 225, 205)),
        ("物理层", "比特 Bits", (232, 232, 238)),
    ]

    def host(x, title, order):
        d.text((x + 90, 80), title, font=f_hei, fill=INK)
        y0 = 130
        bh = 88
        for idx, (name, pdu, color) in enumerate(layers):
            y = y0 + idx * bh
            d.rectangle([x, y, x + 340, y + bh], outline=INK, width=2, fill=color)
            d.text((x + 16, y + 12), name, font=f18, fill=INK)
            d.text((x + 16, y + 46), pdu, font=f13, fill=GRAY)

    # 发送端（左）
    host(40, "发送端 · 主机 A", None)
    # 加头箭头（左列左侧）
    d.text((12, 150), "自", font=f15, fill=INK)
    d.text((12, 180), "上", font=f15, fill=INK)
    d.text((12, 210), "而", font=f15, fill=INK)
    d.text((12, 240), "下", font=f15, fill=INK)
    d.text((12, 280), "逐", font=f15, fill=INK)
    d.text((12, 310), "层", font=f15, fill=INK)
    d.text((12, 340), "加", font=f15, fill=INK)
    d.text((12, 370), "头", font=f15, fill=INK)
    d.rectangle([32, 150, 38, 400], fill=INK)  # 竖线箭头
    d.polygon([(28, 400), (42, 400), (35, 422)], fill=INK)

    # 接收端（右）
    host(1220, "接收端 · 主机 B", None)
    d.text((1436, 150), "自", font=f15, fill=INK)
    d.text((1436, 180), "下", font=f15, fill=INK)
    d.text((1436, 210), "而", font=f15, fill=INK)
    d.text((1436, 240), "上", font=f15, fill=INK)
    d.text((1436, 280), "逐", font=f15, fill=INK)
    d.text((1436, 310), "层", font=f15, fill=INK)
    d.text((1436, 340), "剥", font=f15, fill=INK)
    d.text((1436, 370), "头", font=f15, fill=INK)
    d.rectangle([1456, 150, 1462, 400], fill=INK)
    d.polygon([(1452, 150), (1466, 150), (1459, 128)], fill=INK)

    # 中间路由器（网络层 + 链路层，物理层）
    rx = 620
    d.text((rx + 90, 80), "路由器（网络层设备）", font=f_hei, fill=INK)
    d.rectangle([rx, 218, rx + 340, 218 + 88], outline=INK, width=2, fill=layers[2][2])
    d.text((rx + 16, 230), "网络层", font=f18, fill=INK)
    d.text((rx + 16, 264), "查 IP 表，剥到网络层再重新封装", font=f13, fill=GRAY)
    d.rectangle([rx, 306, rx + 340, 306 + 88], outline=INK, width=2, fill=layers[3][2])
    d.text((rx + 16, 318), "链路层", font=f18, fill=INK)
    d.text((rx + 16, 352), "换 MAC 头（每段链路不同）", font=f13, fill=GRAY)
    d.rectangle([rx, 394, rx + 340, 394 + 88], outline=INK, width=2, fill=layers[4][2])
    d.text((rx + 16, 406), "物理层", font=f18, fill=INK)
    d.text((rx + 16, 440), "比特", font=f13, fill=GRAY)

    # 水平箭头
    for xa, xb in [(380, 620), (960, 1220)]:
        ymid = 350
        d.line([(xa, ymid), (xb - 20, ymid)], fill=INK, width=3)
        d.polygon([(xb - 20, ymid), (xb - 40, ymid - 8), (xb - 40, ymid + 8)], fill=INK)
        d.text(((xa + xb) // 2 - 30, ymid + 8), "帧", font=f15, fill=GRAY)

    # 底部：头部嵌套顺序
    dy = 625
    d.text((40, dy - 36), "帧的头部嵌套（发送端逐层加头后的最终封装）", font=f_hei, fill=INK)
    parts = [
        ("以太网头", (250, 225, 205)),
        ("IP 头", (253, 245, 205)),
        ("TCP 头", (209, 236, 214)),
        ("应用数据", (214, 234, 248)),
        ("FCS", (250, 225, 205)),
    ]
    x = 40
    for name, color in parts:
        w = 240 if name != "应用数据" else 400
        d.rectangle([x, dy, x + w, dy + 60], outline=INK, width=2, fill=color)
        d.text((x + w // 2 - 40, dy + 20), name, font=f15, fill=INK)
        x += w + 6

    img.save(out_path)
    return out_path, img.size


def main():
    render_console(FIG1, os.path.join(BUILD, "fig1_console.png"), "命令提示符 — ipconfig /all")
    render_console(FIG2, os.path.join(BUILD, "fig2_console.png"), "命令提示符 — ping / nslookup")
    render_console(FIG3, os.path.join(BUILD, "fig3_console.png"), "命令提示符 — netstat / tracert")
    print(draw_diagram(os.path.join(BUILD, "fig4_encap.png")))


if __name__ == "__main__":
    main()
