from peak import Peak, name_outputs, family_closure, assemble
from .isa import Inst_fc

def gen_ALU(width):
    @family_closure
    def ALU_fc(family):
        Data = family.BitVector[width]
        Inst, OP = Inst_fc(family)

        @assemble(family, locals(), globals())
        class ALU(Peak):
            @name_outputs(alu_res=Data)
            def __call__(self, inst : Inst, a : Data, b : Data):
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
