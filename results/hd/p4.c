#include "bv_macros.h"
int32_t p4(int32_t x) {
  int32_t o1 = bvsub(x, 1);
  int32_t res = bvxor(x, o1);
  return res;
}
