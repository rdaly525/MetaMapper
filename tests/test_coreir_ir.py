from metamapper.irs.coreir import gen_CoreIRNodes
from hwtypes import Bit, BitVector as BV
from peak import family

def test_coreir_add():
    #Generate an 8 bit coreir
    ir = gen_CoreIRNodes(8)
    assert "add" in ir.peak_nodes
    Add_fc = ir.peak_nodes["add"]
    Add = Add_fc(family.PyFamily())

    add = Add()
    assert BV[8](6) == add(BV[8](5), BV[8](1))
