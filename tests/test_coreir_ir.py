from metamapper.irs.coreir import gen_CoreIR
from hwtypes import Bit, BitVector as BV

def test_coreir_add():
    #Generate an 8 bit coreir
    ir = gen_CoreIR(8)
    assert "add" in ir.instructions
    Add_fc = ir.instructions["add"]
    Add = Add_fc(Bit.get_family())

    add = Add()
    assert BV[8](6) == add(BV[8](5), BV[8](1))
