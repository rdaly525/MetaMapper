import examples.PEs.alu_basic as alu_basic
import examples.PEs.PE_lut as PE_lut
from hwtypes import BitVector as BV
from peak import family
from metamapper import CoreIRContext

def test_alu():
    CoreIRContext(reset=True)
    width = 8
    ALU_fc = alu_basic.gen_ALU(width)
    isa_fc = alu_basic.gen_isa(width)
    isa = isa_fc.Py
    inst = isa.Inst(op=isa.OP.Add, imm=family.PyFamily().BitVector[8](0))
    alu = (ALU_fc.Py)()

    #check add
    assert BV[8](10) == alu(inst, a=BV[8](6), b=BV[8](4))

    #check if it can compile to magma
    alu_m = ALU_fc.Magma

def test_PE_lut():
    CoreIRContext(reset=True)
    PE_fc = PE_lut.gen_PE(8)
    PE_fc.Py
    PE_fc.SMT
    PE_fc.Magma
    isa = PE_lut.gen_isa(8).Py
    inst = isa.Inst(
        alu_inst=isa.AluInst(
            op=isa.OP.Add,
            imm=isa.Data(5)
        ),
        lut=isa.LUT_t(3),
    )
    res = PE_fc.Py()(inst, isa.Data(3), isa.Data(1), isa.Bit(1), isa.Bit(0), isa.Bit(1))
