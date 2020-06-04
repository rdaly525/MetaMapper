from peak import family_closure
from hwtypes import Enum, Product

class OP(Enum):
    Add = 2
    Sub = 3
    Or =  4
    And = 5
    XOr = 6
    imm = 6

def gen_Inst(width):
    @family_closure
    def Inst_fc(family):
        class Inst(Product):
            op = OP
            imm = family.BitVector[width]
        return Inst
    return Inst_fc
