#include "bv_macros.h"
int32_t p6(int32_t x) {
  int32_t o1 = bvadd(x, 1);
  int32_t res = bvor(x, o1);
  return res;
}
