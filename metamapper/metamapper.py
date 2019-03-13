import coreir
from collections import OrderedDict
from hwtypes import BitVector
from peak.mapper import gen_mapping
import peak
from .rewrite_rule import Peak1to1

class MetaMapper:

    primitives = {}
    rules = []
    def __init__(self,context : coreir.context,namespace_name):
        self.context = context
        self.ns = context.new_namespace(namespace_name)
    
    def add_rewrite_rule(self,rule):
        self.rules.append(rule)

    #def add_backend_primitive(self, prim : coreir.module.Module):
    #    self.primitives[prim.name] = (prim,None)

    def map_app(self,app : coreir.module.Module):
        self.context.run_passes(['flatten'])
        mapped_instances = {}
        for rule in self.rules:
            mapped = rule(self.context,app)
            assert isinstance(mapped,dict)
            mapped_instances = {**mapped_instances,**mapped}
        # Verify that all the instances in the application have the same type as the primitive list.
        return mapped_instances

class PeakMapper(MetaMapper):
    def __init__(self,context : coreir.context,namespace_name):
        super(PeakMapper,self).__init__(context,namespace_name)

    def add_peak_primitive(self,prim_name,gen_fn):
        peak_fn = gen_fn(BitVector.get_family())
        c = self.context
        #Create the coreIR type for this module
        inputs = peak_fn._peak_inputs_
        outputs = peak_fn._peak_outputs_
        isa = list(peak_fn._peak_isa_.items())[0][1]
        record_params = OrderedDict()
        for (io,bit_dir) in ((inputs,c.BitIn()),(outputs,c.Bit())):
            for name,bvtype in io.items():
                num_bits = bvtype(0).num_bits
                record_params[name] = self.context.Array(num_bits,bit_dir)
        modtype = c.Record(record_params)
        
        #Create the modargs for this module
        isa_name = isa.__name__
        modparams = c.newParams({isa_name : c.String()})

        coreir_prim = self.ns.new_module(prim_name,modtype,modparams)
        self.primitives[prim_name] = (coreir_prim,peak_fn,gen_fn,isa)
        return coreir_prim
    def add_io_primitive(self, width, to_fabric_name, from_fabric_name):
        self.width = width
        self.output = to_fabric_name
        self.input = from_fabric_name

    #This will automatically discover rewrite rules for the coreir primitives using all the added peak primitives
    def discover_rewrite_rules(self,width):
        
        #TODO replace this with the actual SMT methods
        __COREIR_MODELS = {
            'add' : lambda in0, in1: in0.bvadd(in1),
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
        for gen in lib.generators.values():
            if gen.params.keys() == {'width'}:
                mods.append(gen(width=width))
        #for all the peak primitives
        for pname, (peak_prim,_,gen_fun, pisa) in self.primitives.items():
            for mod in mods:
                if mod.name in __COREIR_MODELS:
                    mappings = list(gen_mapping(
                        gen_fun,
                        pisa,
                        mod,
                        __COREIR_MODELS[mod.name],
                        1,)
                    )
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

    
