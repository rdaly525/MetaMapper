#include "bv_macros.h"
int32_t p10(int32_t x, int32_t y) {
  int32_t o1  = bvand(x, y);
  int32_t o2  = bvxor(x, y);
  int32_t res = bvule(o2, o1);
  return res;
}
