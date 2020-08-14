#include "bv_macros.h"
int32_t p8(int32_t x) {
  int32_t o1  = bvsub(x, 1);
  int32_t o2  = bvnot(x);
  int32_t res = bvand(o1, o2);
  return res;
}
