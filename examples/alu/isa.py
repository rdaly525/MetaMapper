from peak import Enum_fc, Product_fc, family_closure

@family_closure
def Inst_fc(family):
    class OP(Enum_fc(family)):
        Add = 0
        Sub = 1
        Or =  2
        And = 3
        XOr = 4

    class Inst(Product_fc(family)):
        op = OP

    return Inst, OP
