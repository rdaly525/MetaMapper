import coreir
from collections import OrderedDict
from hwtypes import BitVector, AbstractBit, AbstractBitVector
from peak.mapper import gen_mapping, SMTBitVector
import peak
from .rewrite_rule import Peak1to1, PeakIO

class MetaMapper:
    def __init__(self,context : coreir.context,namespace_name):
        self.backend_modules = set()
        self.rules = []

        self.context = context
        self.ns = context.new_namespace(namespace_name)
    
    def add_rewrite_rule(self,rule):
        self.rules.append(rule)

    def add_backend_primitive(self, prim : coreir.module.Module):
        self.backend_modules.add(prim)
    
    def add_const(self,width):
        c = self.context
        if width==1:
            cnst = c.get_namespace("corebit").modules["const"]
        else:
            cnst = c.get_namespace("coreir").generators["const"](width=width)
        self.add_backend_primitive(cnst)

    def map_app(self,app : coreir.module.Module):
        self.context.run_passes(['flatten','flattentypes'])
        mapped_instances = {}
        for rule in self.rules:
            mapped = rule(app)
            if mapped is not None:
                assert isinstance(mapped,dict)
                mapped_instances = {**mapped_instances,**mapped}
        # Verify that all the instances in the application have the same type as the primitive list.
        adef = app.definition
        for inst in adef.instances:
            if inst.module not in self.backend_modules:
                raise Exception(f"{inst.name}:{inst.module.name} is not a backend_primitive\n prims: {str([mod.name for mod in self.backend_modules])}")
        return mapped_instances

class PeakMapper(MetaMapper):
    def __init__(self,context : coreir.context,namespace_name):
        self.peak_primitives = {}
        self.io_primitives = {}
        self.discover_constraints = []
        super(PeakMapper,self).__init__(context,namespace_name)
        
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
        
        #Create the modargs for this module
        isa_name = isa.__name__
        modparams = c.newParams({isa_name : c.String()})

        coreir_prim = self.ns.new_module(prim_name,modtype,modparams)
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
        record_params[self.output] = self.context.Array(width,c.Bit())
        record_params[self.input] = self.context.Array(width,c.BitIn())
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
    #This will automatically discover rewrite rules for the coreir primitives using all the added peak primitives
    def discover_peak_rewrite_rules(self,width,coreir_primitives=None):
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
        #for all the peak primitives
        for pname, (peak_prim,family_closure,_pisa) in self.peak_primitives.items():
            peak_class = family_closure(SMTBitVector.get_family())
            pisa = peak_class.__call__._peak_isa_[1]
            for mod in mods:
                assert mod.name in _COREIR_MODELS_
                if mod.name in _COREIR_MODELS_:
                    mappings = list(gen_mapping(
                        peak_class,
                        pisa,
                        mod,
                        _COREIR_MODELS_[mod.name],
                        1,
                        constraints=self.discover_constraints
                    ))
                    if mappings:
                        print(f'Mappings found for {mod.name}', mappings)
                        inst = mappings[0]['instruction']
                        input_map = mappings[0]['input_map']
                        output_map = mappings[0]['output_map']
                        coreir_mapping = {**input_map,**output_map}
                        mod_rule = Peak1to1(
                            mod,
                            peak_prim,
                            inst,
                            coreir_mapping
                        )
                        self.add_rewrite_rule(mod_rule)
                    else:
                        print(f'No Mapping found for {mod.name}')
                    print('\n------------------------------------------------\n')

    
