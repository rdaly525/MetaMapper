#include "bv_macros.h"
int32_t p16(int32_t x, int32_t y) {
  int32_t o1 = bvxor(x, y);
  int32_t o2 = bvneg(bvuge(x, y));
  int32_t o3 = bvand(o1, o2);
  int32_t res = bvxor(o3, y);
  return res;
}
