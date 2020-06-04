from peak import Peak, family_closure
from .isa import Inst, OP

def gen_ALU(width):
    @family_closure
    def ALU_fc(family):
        Data = family.BitVector[width]
        SData = family.Signed[width]

        @family.assemble(locals(), globals())
        class ALU(Peak):
            def __call__(self, inst: Inst, a: Data, b: Data) -> Data:
                a = SData(a)
                b = SData(b)
                op = inst.op
                if op == OP.Add:
                    res = a + b
                elif op == OP.Sub:
                    res = a - b
                elif op == OP.And:
                    res = a & b
                elif op == OP.Or:
                    res = a | b
                else: # op == ALUOP.XOr:
                    res = a ^ b
                return res
        return ALU
    return ALU_fc
