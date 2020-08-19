#include "bv_macros.h"
int32_t p1(int32_t x) {
  int32_t o1 = bvsub(x, 1);
  int32_t res = bvand(x, o1);
  return res;
}
