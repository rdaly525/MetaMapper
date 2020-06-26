from examples.PEs.alu_basic import gen_ALU, gen_Inst, OP as ALUOP
from examples.PEs.PE_lut import gen_isa, gen_PE as gen_PE_lut
from hwtypes import BitVector as BV
from peak import family
from metamapper import CoreIRContext

def test_alu():
    CoreIRContext(reset=True)
    width = 8
    ALU_fc = gen_ALU(8)
    Inst_fc = gen_isa(8)
    ALU_bv = ALU_fc(family.PyFamily())
    Inst = Inst_fc(family.PyFamily())
    inst = Inst(op=ALUOP.Add, imm=family.PyFamily().BitVector[8](0))
    alu = ALU_bv()

    #check add
    assert BV[8](10) == alu(inst, a=BV[8](6), b=BV[8](4))

    #check if it can compile to magma
    alu_m = ALU_fc.Magma

def test_PE_lut():
    CoreIRContext(reset=True)
    PE_fc = gen_PE_lut(8)
    PE_fc.Py
    PE_fc.SMT
    PE_fc.Magma
    isa = gen_isa(8).Py
    inst = isa.Inst(
        alu_inst=isa.AluInst(
            op=isa.OP.Add,
            imm=isa.Data(5)
        ),
        lut=isa.LUT_t(3),
    )
    out = PE_fc.Py()(inst, isa.Data(3), isa.Data(1), isa.Bit(1), isa.Bit(0), isa.Bit(1))
