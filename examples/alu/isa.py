from peak import Enum_fc, Product_fc, family_closure

@family_closure
def Inst_fc(family):
    class OP(Enum_fc(family)):
        Add = 1
        Sub = 2
        Or =  3
        And = 4
        XOr = 5

    class Inst(Product_fc(family)):
        op = OP

    return Inst, OP
