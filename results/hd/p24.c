#include "bv_macros.h"
int32_t p24(int32_t x) {
  int32_t o1 = bvsub(x, 1);
  int32_t o2  = bvshr(o1, 1);
  int32_t o3  = bvor(o1, o2);
  int32_t o4  = bvshr(o3, 2);
  int32_t o5  = bvor(o3, o4);
  int32_t o6  = bvshr(o5, 4);
  int32_t o7  = bvor(o5, o6);
  int32_t o8  = bvshr(o7, 8);
  int32_t o9  = bvor(o7, o8);
  int32_t o10 = bvshr(o9, 16);
  int32_t o11 = bvor(o9, o10);
  int32_t res = bvadd(o10, 1);
  return res;
}
