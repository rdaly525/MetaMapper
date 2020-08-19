#include "bv_macros.h"
int32_t p21(int32_t x, int32_t a, int32_t b, int32_t c) {
  int32_t o1  = bvneg(bveq(x, c));
  int32_t o2  = bvxor(a, c);
  int32_t o3  = bvneg(bveq(x, a));
  int32_t o4  = bvxor(b, c);
  int32_t o5  = bvand(o1, o2);
  int32_t o6  = bvand(o3, o4);
  int32_t o7  = bvxor(o5, o6);
  int32_t res = bvxor(o7, c);
  return res;
}
