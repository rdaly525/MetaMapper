#include "bv_macros.h"
int32_t p19(int32_t x, int32_t m, int32_t k) {
  int32_t o1  = bvshr(x, k);
  int32_t o2  = bvxor(x, o1);
  int32_t o3  = bvand(o2, m);
  int32_t o4  = bvshl(o3, k);
  int32_t o5  = bvxor(o4, o3);
  int32_t res = bvxor(o5, x);
  return res;
}
