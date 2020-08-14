#include "bv_macros.h"
int32_t p12(int32_t x, int32_t y) {
  int32_t o1  = bvnot(y);
  int32_t o2  = bvand(x, o1);
  int32_t res = bvule(o2, y);
  return res;
}
