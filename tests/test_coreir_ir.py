from metamapper.irs.coreir import gen_CoreIRNodes
from metamapper import CoreIRContext
from hwtypes import Bit, BitVector as BV
from peak import family

def test_coreir_add():
    CoreIRContext(reset=True)
    #Generate an 8 bit coreir
    ir = gen_CoreIRNodes(8)
    assert "coreir.add" in ir.peak_nodes
    Add_fc = ir.peak_nodes["coreir.add"]
    Add = Add_fc(family.PyFamily())

    add = Add()
    assert BV[8](6) == add(BV[8](5), BV[8](1))
