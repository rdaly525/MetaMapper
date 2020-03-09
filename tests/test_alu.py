from examples.alu import gen_ALU, Inst_fc
from hwtypes import Bit, BitVector as BV


def test_alu():
    width = 8
    ALU_fc = gen_ALU(8)
    ALU_bv = ALU_fc(Bit.get_family())
    Inst, OP = Inst_fc(Bit.get_family())
    print(Inst)
    Inst(op=OP.Add)
    alu = ALU_bv()

    #check add
    assert BV[8](10) == alu(Inst(op=OP.Add), a=BV[8](6), b=BV[8](4))

