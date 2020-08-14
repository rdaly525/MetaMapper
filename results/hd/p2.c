#include "bv_macros.h"
int32_t p2(int32_t x) {
  int32_t o1 = bvadd(x, 1);
  int32_t res = bvand(x, o1);
  return res;
}
