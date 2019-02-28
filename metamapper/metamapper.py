import coreir
from collections import OrderedDict
from bit_vector import BitVector

class MetaMapper:

    primitives = {}
    rewrites = {}
    def __init__(self,context : coreir.context,namespace_name):
        self.context = context
        self.ns = context.new_namespace(namespace_name)

    def add_peak_primitive(self,prim_name,prim_fn,isa):
        assert hasattr(prim_fn,"_peak_inputs_")
        assert hasattr(prim_fn,"_peak_outputs_")
        c = self.context
        
        #Create the coreIR type for this module
        inputs = prim_fn._peak_inputs_
        outputs = prim_fn._peak_outputs_
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
        self.add_coreir_primitive(coreir_prim)
        return coreir_prim

    def add_coreir_primitive(self,prim : coreir.module.Module):
        self.primitives[prim.name] = prim

    #This is a simple 1:1 rewrite rule. IO must match exactly other than in name.
    def add_1to1_rewrite_rule(self,coreir_prim,peak_prim_name,peak_instr, io_mapping):
        assert peak_prim_name in self.primitives
        if coreir_prim not in self.rewrites:
            self.rewrites[coreir_prim] = []
        
        #Actually construct the coreir definition
        coreir_def = coreir_prim.new_definition()
        modvalues = self.context.new_values(dict(Inst=peak_instr.name))
        peak_inst = coreir_def.add_module_instance(name="prim_inst",module=self.primitives[peak_prim_name],config=modvalues)
        for coreir_port,peak_port in io_mapping.items():
            coreir_def.connect(peak_inst.select(peak_port),coreir_def.interface.select(coreir_port))
        self.rewrites[coreir_prim].append(coreir_def)
    
    def add_coreir_rewrite_rule(self,pattern,match):
        pass

    def map_module(self,mod : coreir.module.Module):
        mdef = mod.definition
        assert mdef
        for inst in mdef.instances:
            inst_mod = inst.module
            assert inst_mod in self.rewrites
            inst_mod.definition=self.rewrites[inst_mod][0]
        #Would be better to just inline each instance rather than flatten everything
        self.context.run_passes(['flatten'])

