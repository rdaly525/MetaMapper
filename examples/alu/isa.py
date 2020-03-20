from peak import Enum_fc, Product_fc, family_closure

@family_closure
def Inst_fc(family):
    class OP(Enum_fc(family)):
        Add = 2
        Sub = 3
        Or =  4
        And = 5
        XOr = 6

    class Inst(Product_fc(family)):
        op = OP

    return Inst, OP
