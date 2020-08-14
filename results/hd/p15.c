#include "bv_macros.h"
int32_t p15(int32_t x, int32_t y) {
  int32_t o1  = bvor(x, y);
  int32_t o2  = bvxor(x, y);
  int32_t o3  = bvshr(o2, 1);
  int32_t res = bvsub(o1, o3);
  return res;
}
