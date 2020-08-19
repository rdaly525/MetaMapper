#include "bv_macros.h"
int32_t p23(int32_t x) {
  int32_t o1 = bvshr(x, 1);
  int32_t o2 = bvand(o1, 0x55555555);
  int32_t o3 = bvsub(x, o2);
  int32_t o4 = bvand(o3, 0x33333333);
  int32_t o5 = bvshr(o3, 2);
  int32_t o6 = bvand(o3, 0x33333333);
  int32_t o7 = bvadd(o4, o6);
  int32_t o8 = bvshr(o7, 4);
  int32_t o9 = bvadd(o8, o7);
  int32_t res = bvand(o9, 0x0F0F0F0F);
  return res;
}
