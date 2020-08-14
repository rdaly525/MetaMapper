#include "bv_macros.h"
int32_t p25(int32_t x, int32_t y) {
  int32_t o1 = bvand(x, 0xFFFF);
  int32_t o2 = bvshr(x, 16);
  int32_t o3 = bvand(y, 0xFFFF);
  int32_t o4 = bvshr(y, 16);
  int32_t o5 = bvmul(o1, o3);
  int32_t o6 = bvmul(o2, o3);
  int32_t o7 = bvmul(o1, o4);
  int32_t o8 = bvmul(o2, o4);
  int32_t o9 = bvshr(o5, 16);
  int32_t o10 = bvadd(o6, o9);
  int32_t o11 = bvand(o10, 0xFFFF);
  int32_t o12 = bvshr(o10, 16);
  int32_t o13 = bvadd(o7, o11);
  int32_t o14 = bvshr(o13, 16);
  int32_t o15 = bvadd(o14, o12);
  int32_t res = bvadd(o15, o8);
  return res;
}
