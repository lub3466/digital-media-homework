# 复现步骤
1. python gen_data.py          # 重新生成 data/*.bin（固定种子，三语言共用）
2. gcc -O2 -static dot.c -o dot_c.exe
3. rustc -C opt-level=2 dot.rs -o dot_rs.exe
4. python test_dot.py          # 5 个边界用例
5. python benchmark.py         # 3 规模 x 3 语言对比表 + 两轮稳定性

data/*.bin 体积约 18 MB，未入库；由 gen_data.py 一键重建，字节与提交时一致（固定种子 20261116）。
