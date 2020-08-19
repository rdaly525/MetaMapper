#include "bv_macros.h"
int32_t p20(int32_t x) {
  int32_t o1  = bvneg(x);
  int32_t o2  = bvand(x, o1);
  int32_t o3  = bvadd(x, o2);
  int32_t o4  = bvxor(x, o2);
  int32_t o5  = bvshr(o4, 2);
  int32_t o6  = bvdiv(o5, o2);
  int32_t res = bvor(o6, o3);
  return res;
}
