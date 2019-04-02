from peak.alu import gen_alu, Inst, ALUOP
import coreir
from metamapper import *
from hwtypes import BitVector

ALU = gen_alu(BitVector.get_family())
Data = BitVector[16]

def test_add():
    alu = ALU()
    inst = Inst(ALUOP.Add)
    assert Data(9) == alu(inst,Data(4), Data(5))
    assert Data(1) == alu(inst,Data(0), Data(1))

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
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3
    c.run_passes(['printer'])

def test_discover():
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    mapper.discover_peak_rewrite_rules(width=16)
    
    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3

def test_discover_add():
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    mapper.discover_peak_rewrite_rules(width=16,coreir_primitives=["add"])
    
    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3

def test_io():
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    #This adds a peak primitive 
    io16 = mapper.add_io_primitive("io16",16,"tofab","fromfab")
    mapper.add_rewrite_rule(PeakIO(
        width=16,
        is_input=True,
        io_prim=io16
    ))
    mapper.add_rewrite_rule(PeakIO(
        width=16,
        is_input=False,
        io_prim=io16
    ))
    
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    mapper.discover_peak_rewrite_rules(width=16)
    
    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3
    c.run_passes(['printer'])

def test_io_simple():
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    #This adds a peak primitive 
    io16 = mapper.add_io_and_rewrite("io16",16,"tofab","fromfab")
    mapper.add_const(16)
    mapper.add_const(1)
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    mapper.discover_peak_rewrite_rules(width=16)
    
    #test the mapper on simple add4 app
    app = c.load_from_file("tests/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3
    c.run_passes(['printer'])
    

#test_add()
#test_add_rewrite()
#test_discover()
#test_io()
