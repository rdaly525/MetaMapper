#include "bv_macros.h"
int32_t p13(int32_t x) {
  int32_t o1  = bvshr(x, 31);
  int32_t o2  = bvneg(x);
  int32_t o3  = bvshr(o2, 31);
  int32_t res = bvor(o1, o3);
  return res;
}
