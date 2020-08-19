#include "bv_macros.h"
int32_t p7(int32_t x) {
  int32_t o1  = bvnot(x);
  int32_t o2  = bvadd(x, 1);
  int32_t res = bvand(o1, o2);
  return res;
}
