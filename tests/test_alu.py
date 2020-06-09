from examples.alu import gen_ALU, gen_Inst, OP
from hwtypes import Bit, BitVector as BV
import magma as m
from peak import family

def test_alu():
    width = 8
    ALU_fc = gen_ALU(8)
    Inst_fc = gen_Inst(8)
    ALU_bv = ALU_fc(family.PyFamily())
    Inst = Inst_fc(family.PyFamily())
    inst = Inst(op=OP.Add, imm=family.PyFamily().BitVector[8](0))
    alu = ALU_bv()

    #check add
    assert BV[8](10) == alu(inst, a=BV[8](6), b=BV[8](4))

    #check if it can compile to magma
    alu_m = ALU_fc(family.MagmaFamily())
