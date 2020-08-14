#include "bv_macros.h"
int32_t p18(int32_t x) {
  int32_t o1  = bvsub(x, 1);
  int32_t o2  = bvand(o1, x);
  int32_t o3  = bvredor(x);
  int32_t o4  = bvredor(o2);
  int32_t o5  = !(o4);
  int32_t res = (o5 && o3);
  return res;
}
