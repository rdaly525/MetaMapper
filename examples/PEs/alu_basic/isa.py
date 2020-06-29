from functools import lru_cache

from peak import family_closure
from hwtypes import Enum, Product
from types import SimpleNamespace

class OP(Enum):
    imm = 1
    Add = 2
    Sub = 3
    Or =  4
    And = 5
    XOr = 6

@lru_cache(None)
def gen_isa(width):
    @family_closure
    def isa_fc(family):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        class Inst(Product):
            op = OP
            imm = Data
        return SimpleNamespace(**locals(), OP=OP)
    return isa_fc
