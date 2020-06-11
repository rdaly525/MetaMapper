from peak import Peak, family_closure, Const, name_outputs
from .isa import gen_Inst, OP

def gen_ALU(width):
    Inst_fc = gen_Inst(width)
    @family_closure
    def ALU_fc(family):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        Inst = Inst_fc(family)
        @family.assemble(locals(), globals())
        class ALU(Peak):
            @name_outputs(out=Data)
            def __call__(self, inst: Const(Inst), a: Data, b: Data) -> Data:
                a = SData(a)
                b = SData(b)
                op = inst.op
                if op == OP.imm:
                    res = inst.imm
                elif op == OP.Add:
                    res = a + b
                elif op == OP.Sub:
                    res = a - b
                elif op == OP.And:
                    res = a & b
                elif op == OP.Or:
                    res = a | b
                else: #op == OP.XOr:
                    res = a ^ b

                return res
        return ALU
    return ALU_fc
