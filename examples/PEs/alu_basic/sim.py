from peak import Peak, family_closure, Const, name_outputs
from .isa import gen_isa

def gen_ALU(width):
    isa_fc = gen_isa(width)
    @family_closure
    def ALU_fc(family):
        isa_fam = isa_fc(family)
        isa = isa_fc.Py

        @family.assemble(locals(), globals())
        class ALU(Peak):
            @name_outputs(out=isa.Data)
            def __call__(self, inst: Const(isa.Inst), a: isa.Data, b: isa.Data) -> isa.Data:
                a = isa_fam.SData(a)
                b = isa_fam.SData(b)
                op = inst.op
                if op == isa.OP.imm:
                    res = inst.imm
                elif op == isa.OP.Add:
                    res = a + b
                elif op == isa.OP.Sub:
                    res = a - b
                elif op == isa.OP.And:
                    res = a & b
                elif op == isa.OP.Or:
                    res = a | b
                else: #op == OP.XOr:
                    res = a ^ b

                return res
        return ALU
    return ALU_fc
