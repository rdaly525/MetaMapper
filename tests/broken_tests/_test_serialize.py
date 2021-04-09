from examples.alu import gen_alu, Inst, ALUOP
from peak.assembler.assembler import Assembler
import coreir
from metamapper import *
import json
from hwtypes.adt import Product, Sum, new_instruction, Enum
from hwtypes import BitVector

def test_add_ser():
    #Create an ALU primitive
    #c = coreir.Context()
    #mapper = PeakMapper(c,"alu_ns")
    #This adds a peak primitive 
    #Alu = mapper.add_peak_primitive("alu",gen_alu)

    #add16 = c.get_namespace("coreir").generators['add'](width=16)

    assembler = Assembler(Inst)
    add_instr = Inst(ALUOP.Add)
    instr_bv = assembler.assemble(add_instr)
    size, value = instr_bv.size, int(instr_bv)
    assert assembler.disassemble(instr_bv) == add_instr

    #dictionary containing the rewrite rule information:
    add16_rr = dict(
        kind="1to1",
        coreir_prim = ["coreir","add"],
        genargs = dict(width=16),
        peak_prim = "alu",
        binding = dict( #From CoreIR to Peak
            in0='a',
            in1='b',
            out="alu_res"
        ),
        instr= [size,value], #size,value
        instr_debug = str(add_instr)
    )
    with open('tests/examples/_addrr.json','w') as jfile:
        json.dump(add16_rr,jfile,indent=2)


    #Create an ALU primitive
    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    #This adds a peak primitive 
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    with open('tests/examples/_addrr.json','r') as jfile:
        rr = json.load(jfile)

    mapper.add_rr_from_description(rr)

    #test the mapper on simple add4 app
    app = c.load_from_file("tests/examples/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3
    c.run_passes(['printer'])

def test_ser_discovery():

    c = coreir.Context()
    mapper = PeakMapper(c,"alu_ns")
    Alu = mapper.add_peak_primitive("alu",gen_alu)
    rrs = mapper.discover_peak_rewrite_rules(width=16,coreir_primitives=["add","sub","or","xor","and"],serialize=True)
    assert rrs
    with open('tests/examples/_discover_rr.json','w') as jfile:
        json.dump(rrs,jfile,indent=2)

    with open('tests/examples/_discover_rr.json','r') as jfile:
        rrs = json.load(jfile)

    for rr in rrs:
        mapper.add_rr_from_description(rr)

    #test the mapper on simple add4 app
    app = c.load_from_file("tests/examples/add4.json")
    mapper.map_app(app)
    imap = mapper.extract_instr_map(app)
    assert len(imap) == 3

