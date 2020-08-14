sigs = dict(
    p1=['x'],
    p2=['x'],
    p3=['x'],
    p4=['x'],
    p5=['x'],
    p6=['x'],
    p7=['x'],
    p8=['x'],
    p9=['x'],
    p10=['x','y'],
    p11=['x','y'],
    p12=['x','y'],
    p13=['x'],
    p14=['x','y'],
    p15=['x','y'],
    p16=['x','y'],
    p17=['x'],
    p18=['x'],
    p19=['x','m','k'],
    p20=['x'],
    p21=['x','a','b','c'],
    p22=['x'],
    p23=['x'],
    p24=['x'],
    p25=['x','y'],
)

bodies = [
[
"int32_t o1 = bvsub(x, 1);",
"int32_t res = bvand(x, o1);",
],
[
"int32_t o1 = bvadd(x, 1);",
"int32_t res = bvand(x, o1);",
],
[
"int32_t o1 = bvneg(x);",
"int32_t res = bvand(x, o1);",
],
[
"int32_t o1 = bvsub(x, 1);",
"int32_t res = bvxor(x, o1);",
],
[
"int32_t o1 = bvsub(x, 1);",
"int32_t res = bvor(x, o1);",
],
[
"int32_t o1 = bvadd(x, 1);",
"int32_t res = bvor(x, o1);",
],
[
"int32_t o1  = bvnot(x);",
"int32_t o2  = bvadd(x, 1);",
"int32_t res = bvand(o1, o2);",
],
[
"int32_t o1  = bvsub(x, 1);",
"int32_t o2  = bvnot(x);",
"int32_t res = bvand(o1, o2);",
],
[
"int32_t o1  = bvshr(x, 31);",
"int32_t o2  = bvxor(x, o1);",
"int32_t res = bvsub(o2, o1);",
],
[
"int32_t o1  = bvand(x, y);",
"int32_t o2  = bvxor(x, y);",
"int32_t res = bvule(o2, o1);",
],
[
"int32_t o1  = bvnot(y);",
"int32_t o2  = bvand(x, o1);",
"int32_t res = bvugt(o2, y);",
],
[
"int32_t o1  = bvnot(y);",
"int32_t o2  = bvand(x, o1);",
"int32_t res = bvule(o2, y);",
],
[
"int32_t o1  = bvshr(x, 31);",
"int32_t o2  = bvneg(x);",
"int32_t o3  = bvshr(o2, 31);",
"int32_t res = bvor(o1, o3);",
],
[
"int32_t o1  = bvand(x, y);",
"int32_t o2  = bvxor(x, y);",
"int32_t o3  = bvshr(o2, 1);",
"int32_t res = bvadd(o1, o3);",
],
[
"int32_t o1  = bvor(x, y);",
"int32_t o2  = bvxor(x, y);",
"int32_t o3  = bvshr(o2, 1);",
"int32_t res = bvsub(o1, o3);",
],
[
"int32_t o1 = bvxor(x, y);",
"int32_t o2 = bvneg(bvuge(x, y));",
"int32_t o3 = bvand(o1, o2);",
"int32_t res = bvxor(o3, y);",
],
[
"int32_t o1  = bvsub(x, 1);",
"int32_t o2  = bvor(x, o1);",
"int32_t o3  = bvadd(o2, 1);",
"int32_t res = bvand(o3, x);",
],
[
"int32_t o1  = bvsub(x, 1);",
"int32_t o2  = bvand(o1, x);",
"int32_t o3  = bvredor(x);",
"int32_t o4  = bvredor(o2);",
"int32_t o5  = !(o4);",
"int32_t res = (o5 && o3);",
],
[
"int32_t o1  = bvshr(x, k);",
"int32_t o2  = bvxor(x, o1);",
"int32_t o3  = bvand(o2, m);",
"int32_t o4  = bvshl(o3, k);",
"int32_t o5  = bvxor(o4, o3);",
"int32_t res = bvxor(o5, x);",
],
[
"int32_t o1  = bvneg(x);",
"int32_t o2  = bvand(x, o1);",
"int32_t o3  = bvadd(x, o2);",
"int32_t o4  = bvxor(x, o2);",
"int32_t o5  = bvshr(o4, 2);",
"int32_t o6  = bvdiv(o5, o2);",
"int32_t res = bvor(o6, o3);",
],
[
"int32_t o1  = bvneg(bveq(x, c));",
"int32_t o2  = bvxor(a, c);",
"int32_t o3  = bvneg(bveq(x, a));",
"int32_t o4  = bvxor(b, c);",
"int32_t o5  = bvand(o1, o2);",
"int32_t o6  = bvand(o3, o4);",
"int32_t o7  = bvxor(o5, o6);",
"int32_t res = bvxor(o7, c);",
],
[
"int32_t o1  = bvshr(x, 1);",
"int32_t o2  = bvxor(o1, x);",
"int32_t o3  = bvshr(o2, 2);",
"int32_t o4  = bvxor(o2, o3);",
"int32_t o5  = bvand(o4, 0x11111111);",
"int32_t o6  = bvmul(o5, 0x11111111);",
"int32_t o7  = bvshr(o6, 28);",
"int32_t res = bvand(o7, 0x1);",
],
[
"int32_t o1 = bvshr(x, 1);",
"int32_t o2 = bvand(o1, 0x55555555);",
"int32_t o3 = bvsub(x, o2);",
"int32_t o4 = bvand(o3, 0x33333333);",
"int32_t o5 = bvshr(o3, 2);",
"int32_t o6 = bvand(o3, 0x33333333);",
"int32_t o7 = bvadd(o4, o6);",
"int32_t o8 = bvshr(o7, 4);",
"int32_t o9 = bvadd(o8, o7);",
"int32_t res = bvand(o9, 0x0F0F0F0F);",
],
[
"int32_t o1 = bvsub(x, 1);",
"int32_t o2  = bvshr(o1, 1);",
"int32_t o3  = bvor(o1, o2);",
"int32_t o4  = bvshr(o3, 2);",
"int32_t o5  = bvor(o3, o4);",
"int32_t o6  = bvshr(o5, 4);",
"int32_t o7  = bvor(o5, o6);",
"int32_t o8  = bvshr(o7, 8);",
"int32_t o9  = bvor(o7, o8);",
"int32_t o10 = bvshr(o9, 16);",
"int32_t o11 = bvor(o9, o10);",
"int32_t res = bvadd(o10, 1);",
],
[
"int32_t o1 = bvand(x, 0xFFFF);",
"int32_t o2 = bvshr(x, 16);",
"int32_t o3 = bvand(y, 0xFFFF);",
"int32_t o4 = bvshr(y, 16);",
"int32_t o5 = bvmul(o1, o3);",
"int32_t o6 = bvmul(o2, o3);",
"int32_t o7 = bvmul(o1, o4);",
"int32_t o8 = bvmul(o2, o4);",
"int32_t o9 = bvshr(o5, 16);",
"int32_t o10 = bvadd(o6, o9);",
"int32_t o11 = bvand(o10, 0xFFFF);",
"int32_t o12 = bvshr(o10, 16);",
"int32_t o13 = bvadd(o7, o11);",
"int32_t o14 = bvshr(o13, 16);",
"int32_t o15 = bvadd(o14, o12);",
"int32_t res = bvadd(o15, o8);",
]
]

def gen():
    path = "results/hd"
    for i in range(1, 26):
        n = f"p{i}"
        body = bodies[i-1]
        with open(f"{path}/{n}.c", "w") as f:
            args = ", ".join([f"int32_t {arg}" for arg in sigs[n]])
            print(f'#include "bv_macros.h"', file=f)
            print(f"int32_t {n}({args}) {{", file=f)
            for l in body:
                print(f"  {l}", file=f)
            print("  return res;", file=f)
            print("}", file=f)

gen()
