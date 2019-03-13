from peak.alu import *
import coreir
from metamapper import *
from hwtypes import BitVector

PE = gen_alu(BitVector.get_family())

def test_add():
    inst = Inst(ALUOP.Add)
    assert Data(9) == PE(inst,Data(4), Data(5))
    assert Data(1) == PE(inst,Data(0), Data(1))

def test_add_rewrite():
    #Create an ALU primitive
    #For now keep it in global. but really should have new namespace
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")

    #This adds a peak primitive 
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    
    add16 = c.get_namespace("coreir").generators['add'](width=16)
    
    #Adds a simple "1 to 1" rewrite rule
    add16_rule = Peak1to1(
        add16,
        Alu,
        Inst(),
        dict(in0='a',in1='b',out="alu_res")
    )
    mapper.add_rewrite_rule(add16_rule)

    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    print(app)
    print("instance map",mapper.map_app(app))
    c.run_passes(['printer'])

def test_discover():
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    mapper.discover_rewrite_rules(width=16)
    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    print(app)
    print("instance map",mapper.map_app(app))
    c.run_passes(['printer'])

#test_add()
#test_add_rewrite()
test_discover()
