#include "bv_macros.h"
int32_t p9(int32_t x) {
  int32_t o1  = bvshr(x, 31);
  int32_t o2  = bvxor(x, o1);
  int32_t res = bvsub(o2, o1);
  return res;
}
