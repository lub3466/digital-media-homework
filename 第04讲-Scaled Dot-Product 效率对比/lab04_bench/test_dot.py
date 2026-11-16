# -*- coding: utf-8 -*-
"""
test_dot.py — 点积函数的 5 个边界用例（用 Python 版 dot() 做载体，
纯 Python 双重循环作黄金基准逐位比对）。

五个用例：
  1. n = 0        空向量 → 结果必须为 0
  2. n = 1        单元素 → a[0] * b[0]
  3. 长度不匹配   a 长 3、b 长 4 → 必须抛错
  4. 全零向量     a 全 0 → 结果 0
  5. 含 NaN       a 含 NaN → 结果必须是 NaN（NaN 传播）

运行：python test_dot.py，全部通过则退出码 0。
"""
import math
import sys

sys.path.insert(0, ".")
from dot import dot  # noqa: E402


def ref_dot(a, b):
    """黄金基准：手写双重循环，最直白、最不可能写错。"""
    s = 0.0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s


def check_close(name, got, want, tol=1e-12):
    ok = (math.isnan(got) and math.isnan(want)) or abs(got - want) <= tol * max(1.0, abs(want))
    print(f"  [{ 'PASS' if ok else 'FAIL' }] {name}: got={got!r} want={want!r}")
    return ok


def main():
    passed = 0
    total = 0

    # 1) n = 0
    total += 1
    passed += check_close("n=0 空向量", dot((), ()), ref_dot((), ()))

    # 2) n = 1
    total += 1
    a, b = (2.5,), (4.0,)
    passed += check_close("n=1 单元素", dot(a, b), ref_dot(a, b))

    # 3) 长度不匹配
    total += 1
    try:
        dot((1.0, 2.0, 3.0), (4.0, 5.0, 6.0, 7.0))
        ok = False
        print("  [FAIL] 长度不匹配：未抛错")
    except Exception:
        ok = True
        print("  [PASS] 长度不匹配：正确抛错")
    passed += ok

    # 4) 全零向量
    total += 1
    a = (0.0, 0.0, 0.0, 0.0)
    b = (1.0, 2.0, 3.0, 4.0)
    passed += check_close("全零向量", dot(a, b), ref_dot(a, b))

    # 5) 含 NaN
    total += 1
    a = (float("nan"), 1.0, 2.0)
    b = (1.0, 2.0, 3.0)
    passed += check_close("含 NaN 输入", dot(a, b), ref_dot(a, b))

    print(f"\n边界用例：{passed}/{total} 通过")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
