from peak import Peak, family_closure, Const, name_outputs
from .isa import gen_isa

def gen_ALU(width):
    isa_fc = gen_isa(width)
    @family_closure
    def ALU_fc(family):
        isa = isa_fc(family)
        @family.assemble(locals(), globals())
        class ALU(Peak):
            def __call__(self, inst: Const(isa.Inst), a: isa.Data, b: isa.Data, c: isa.Data, d: isa.Data) -> (isa.Data, family.Bit):
                a = isa.SData(a)
                b = isa.SData(b)
                op = inst.op
                if op == isa.OP.imm:
                    res = inst.imm
                elif op == isa.OP.Add:
                    res = a + inst.imm
                elif op == isa.OP.Sub:
                    res = a + b
                elif op == isa.OP.And:
                    t = a + b
                    res = t + t
                elif op == isa.OP.Or:
                    res = a*b
                else: #op == OP.XOr:
                    res = a + (b*inst.imm) + (c*inst.imm1) + (d*inst.imm2)

                return res, inst.use_imm
        return ALU
    return ALU_fc
