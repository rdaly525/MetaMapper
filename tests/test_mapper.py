from peak.alu import *
from peak import Bits
import coreir
from metamapper import MetaMapper


def test_alu():
    inst = Inst(ALUOP.Add)
    alu = ALU(inst)
    res = alu(Data(4), Data(5))
    assert res==Data(9)

def test_mapper():
    #Create an ALU primitive
    #For now keep it in global. but really should have new namespace
    c = coreir.Context()
    mapper = MetaMapper(c)

    #This adds a peak primitive 
    Alu = mapper.add_peak_primitive("alu",ALU.__call__,Inst)
    
    add16 = c.get_namespace("coreir").generators['add'](width=16)
    
    #Adds a simple "1 to 1" rewrite rule
    mapper.add_simple_rewrite_rule(
        add16,
        "alu",
        ALUOP.Add,
        dict(in0='data0',in1='data1',out="alu_res")
    )

    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    print(app)
    mapper.map_module(app)
    c.run_passes(['printer'])

test_alu()
test_mapper()
