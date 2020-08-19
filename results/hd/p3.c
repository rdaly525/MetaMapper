#include "bv_macros.h"
int32_t p3(int32_t x) {
  int32_t o1 = bvneg(x);
  int32_t res = bvand(x, o1);
  return res;
}
