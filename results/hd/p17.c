#include "bv_macros.h"
int32_t p17(int32_t x) {
  int32_t o1  = bvsub(x, 1);
  int32_t o2  = bvor(x, o1);
  int32_t o3  = bvadd(o2, 1);
  int32_t res = bvand(o3, x);
  return res;
}
