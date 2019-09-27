import coreir
from .metamapper import MetaMapper
from collections import OrderedDict
from hwtypes import BitVector, AbstractBit, AbstractBitVector
from peak.mapper import gen_mapping, SMTBitVector
from peak.assembler.assembler import Assembler
import peak
from .rewrite_rule import Peak1to1, PeakIO



class PeakMapper(MetaMapper):
    def __init__(self,context : coreir.context,namespace_name):
        self.peak_primitives = {}
        self.io_primitives = {}
        self.discover_constraints = []
        super(PeakMapper,self).__init__(context,namespace_name)

    def extract_instr_map(self,app : coreir.module.Module):
        instr_map = {}
        for rr in self.rules:
            if isinstance(rr,Peak1to1):
                instr_map.update(rr.instr_map)
        return instr_map

    def add_peak_primitive(self,prim_name,family_closure):
        c = self.context
        #Just pass in BitVector to get the class
        peak_class = family_closure(BitVector.get_family())
        peak_fn = peak_class.__call__
        #Create the coreIR type for this module
        inputs = peak_fn._peak_inputs_
        outputs = peak_fn._peak_outputs_
        isa = peak_fn._peak_isa_[1]
        record_params = OrderedDict()
        for (io,bit_dir) in ((inputs,c.BitIn()),(outputs,c.Bit())):
            for name,bvtype in io.items():
                if issubclass(bvtype,AbstractBit):
                    btype = bit_dir
                elif issubclass(bvtype,AbstractBitVector):
                    btype = self.context.Array(bvtype.size,bit_dir)
                else:
                    raise ValueError("Bad type")
                record_params[name] = btype
        modtype = c.Record(record_params)


        coreir_prim = self.ns.new_module(prim_name,modtype)
        self.peak_primitives[prim_name] = (coreir_prim, family_closure, isa)
        self.add_backend_primitive(coreir_prim)
        return coreir_prim

    def add_io_primitive(self, name, width, to_fabric_name, from_fabric_name):
        c = self.context
        self.name = name
        self.width = width
        self.output = to_fabric_name
        self.input = from_fabric_name
        record_params = OrderedDict()
        if width > 1:
            record_params[self.output] = c.Array(width,c.Bit())
            record_params[self.input] = c.Array(width,c.BitIn())
        else:
            record_params[self.output] = c.Bit()
            record_params[self.input] = c.BitIn()

        modtype = c.Record(record_params)
        io_prim = self.ns.new_module(name,modtype)
        self.io_primitives[name] = io_prim
        self.add_backend_primitive(io_prim)
        return io_prim

    def add_io_and_rewrite(self, name, width, to_fabric_name, from_fabric_name):
        io_prim = self.add_io_primitive(name,width,to_fabric_name,from_fabric_name)
        assert self.context == io_prim.context
        self.add_rewrite_rule(PeakIO(
            width=width,
            is_input=True,
            io_prim=io_prim
        ))
        self.add_rewrite_rule(PeakIO(
            width=width,
            is_input=False,
            io_prim=io_prim
        ))

    def add_discover_constraint(self,fun):
        assert callable(fun)
        self.discover_constraints.append(fun)

    def add_rr_from_description(self,rr):

        assert rr['kind'] == "1to1"

        #get coreir module
        ns, name = rr['coreir_prim']
        genargs = rr['genargs']
        coreir_prim = self.context.get_namespace(ns).generators[name](**genargs)

        peak_prim, _, isa  = self.peak_primitives[rr['peak_prim']]
        coreir_mapping = rr['binding']
        assembler = Assembler(isa)
        width = assembler.width
        isize, ival = rr['instr']
        assert width == isize
        instr = assembler.disassemble(BitVector[isize](ival))

        mod_rule = Peak1to1(
            coreir_prim,
            peak_prim,
            instr,
            coreir_mapping
        )
        self.add_rewrite_rule(mod_rule)

    #This will automatically discover rewrite rules for the coreir primitives using all the added peak primitives
    def discover_peak_rewrite_rules(self,width,coreir_primitives=None,serialize=False,verbose=False):
        #Add constants
        self.add_const(width)
        self.add_const(1)
        #TODO replace this with the actual SMT methods
        _COREIR_MODELS_ = {
            'add' : lambda in0, in1: in0.bvadd(in1),
            'mul' : lambda in0, in1: in0.bvmul(in1),
            'sub' : lambda in0, in1: in0.bvsub(in1),
            'or'  : lambda in0, in1: in0.bvor(in1),
            'and' : lambda in0, in1: in0.bvand(in1),
            'shl' : lambda in0, in1: in0.bvshl(in1),
            'lshr': lambda in0, in1: in0.bvlshr(in1),
            'not' : lambda in_: in_.bvnot(),
            'neg' : lambda in_: in_.bvneg(),
            'eq'  : lambda in0, in1: in0.bveq(in1),
            'neq' : lambda in0, in1: in0.bvne(in1),
            'ult' : lambda in0, in1: in0.bvult(in1),
            'ule' : lambda in0, in1: in0.bvule(in1),
            'ugt' : lambda in0, in1: in0.bvugt(in1),
            'uge' : lambda in0, in1: in0.bvuge(in1),
            'xor' : lambda in0, in1: in0.bvxor(in1),
        }
        lib = self.context.get_namespace('coreir')
        mods = []
        if coreir_primitives:
            for mname in coreir_primitives:
                gen = lib.generators[mname]
                mods.append(gen(width=width))
        else:
            for name,gen in lib.generators.items():
                #TODO this is a hack
                if name not in _COREIR_MODELS_:
                    continue;
                if gen.params.keys() == {'width'}:
                    mods.append(gen(width=width))

        #datastructure for serializing
        #For now just keep them in a list
        rrs = []
        #for all the peak primitives
        for pname, (peak_prim,family_closure,_pisa) in self.peak_primitives.items():
            smt_peak_class = family_closure(SMTBitVector.get_family())
            bv_peak_class = family_closure(BitVector.get_family())
            smt_isa = smt_peak_class.__call__._peak_isa_[1]
            bv_isa = bv_peak_class.__call__._peak_isa_[1]
            assembler = Assembler(bv_isa)
            for mod in mods:
                assert mod.name in _COREIR_MODELS_
                genargs = {k:v.value for k,v in mod.generator_args.items()}
                if mod.name in _COREIR_MODELS_:
                    mappings = list(gen_mapping(
                        smt_peak_class,
                        bv_isa,
                        smt_isa,
                        mod,
                        _COREIR_MODELS_[mod.name],
                        1,
                        constraints=self.discover_constraints,
                        verbose=verbose
                    ))
                    if mappings:
                        instr = mappings[0]['instruction']
                        input_map = mappings[0]['input_map']
                        output_map = mappings[0]['output_map']
                        port_binding = {**input_map,**output_map}
                        assem_instr = assembler.assemble(instr)
                        iwidth,ival = assem_instr.size, int(assem_instr)
                        rr = dict(
                            kind="1to1",
                            coreir_prim = ["coreir",mod.name],
                            genargs = genargs,
                            peak_prim = pname,
                            binding = port_binding,
                            instr= [iwidth,ival], #size,value
                            instr_debug= str(instr)
                        )
                        rrs.append(rr)
                        print(f'Mappings found for {mod.name}', rr)

                    else:
                        print(f'No Mapping found for {mod.name}')
                    print('\n------------------------------------------------\n')
        if serialize:
            return rrs
        else:
            for rr in rrs:
                self.add_rr_from_description(rr)

