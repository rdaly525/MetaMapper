#include "bv_macros.h"
int32_t p22(int32_t x) {
  int32_t o1  = bvshr(x, 1);
  int32_t o2  = bvxor(o1, x);
  int32_t o3  = bvshr(o2, 2);
  int32_t o4  = bvxor(o2, o3);
  int32_t o5  = bvand(o4, 0x11111111);
  int32_t o6  = bvmul(o5, 0x11111111);
  int32_t o7  = bvshr(o6, 28);
  int32_t res = bvand(o7, 0x1);
  return res;
}
