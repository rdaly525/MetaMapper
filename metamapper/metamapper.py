import coreir
from collections import OrderedDict
from hwtypes import BitVector
from peak.mapper import gen_mapping
import peak

class MetaMapper:

    primitives = {}
    rules = []
    def __init__(self,context : coreir.context,namespace_name):
        self.context = context
        self.ns = context.new_namespace(namespace_name)
    
    def add_rewrite_rule(self,rule):
        self.rules.append(rule)

    def add_backend_primitive(self, prim : coreir.module.Module):
        self.primitives[prim.name] = (prim,None)

    def map_app(self,app : coreir.module.Module):
        self.context.run_passes(['flatten'])
        mapped_instances = {}
        for rule in self.rules:
            mapped = rule(self.context,app)
            assert isinstance(mapped,dict)
            mapped_instances = {**mapped_instances,**mapped}
        return mapped_instances

class PeakMapper(MetaMapper):
    peak_primitives = {}
    def __init__(self,context : coreir.context,namespace_name):
        self.context = context
        self.ns = context.new_namespace(namespace_name)
        self.primitives = {}

    def add_peak_primitive(self,prim_name,gen_fn,isa : peak.ISABuilder):
        peak_fn = gen_fn(BitVector.get_family())
        assert hasattr(peak_fn,"_peak_inputs_")
        assert hasattr(peak_fn,"_peak_outputs_")
        c = self.context
        self.peak_primitives[prim_name] = (peak_fn,gen_fn,isa)
        #Create the coreIR type for this module
        inputs = peak_fn._peak_inputs_
        outputs = peak_fn._peak_outputs_
        record_params = OrderedDict()
        inst_cnt = 0
        for (io,bit_dir) in ((inputs,c.BitIn()),(outputs,c.Bit())):
            for name,bvtype in io.items():
                if not issubclass(bvtype,BitVector):
                    inst_cnt += 1
                    continue
                num_bits = bvtype(0).num_bits
                record_params[name] = self.context.Array(num_bits,bit_dir)
        assert inst_cnt == 1, inst_cnt
        modtype = c.Record(record_params)
        
        #Create the modargs for this module
        isa_name = isa.__name__
        modparams = c.newParams({isa_name : c.String()})

        coreir_prim = self.ns.new_module(prim_name,modtype,modparams)
        return coreir_prim

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
        for pname, (_,gen_fun, pisa) in self.peak_primitives.items():
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
                        print(f'Mappings found for {mod.name}')
                        inst = mappings['instruction']
                        coreir_mapping = mappings['coreir to peak']
                        mod_rule = Rule1to1(
                            mod,
                            peak_prim,
                            inst,
                            coreir_mapping
                        )
                        self.add_rewrite_rule(mod_rule)
                    else:
                        print(f'No Mapping found for {mod.name}')
                    print('\n------------------------------------------------\n')

    
