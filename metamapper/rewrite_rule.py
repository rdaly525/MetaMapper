import coreir
import peak

#Represents a single rewrite rule that can be applied to a flattened CoreIR graph
class RewriteRule:
    def __call__(self,c,app):
        raise NotImplementedError


#Only works with a single debug string
class Peak1to1(RewriteRule):
    def __init__(self,coreir_prim : coreir.module.Module, peak_prim : coreir.module.Module, prim_instr : peak.ISABuilder, io_mapping):
        self.coreir_prim = coreir_prim
        self.prim_instr = prim_instr
        #Actually construct the coreir definition
        coreir_def = coreir_prim.new_definition()
        c = coreir_prim.context
        param_name = prim_instr.__class__.__name__
        print(param_name)
        modvalues = c.new_values({param_name : str(prim_instr)})

        peak_inst = coreir_def.add_module_instance(name="inst",module=peak_prim,config=modvalues)
        peak_inst.type.print_()
        for coreir_port,peak_port in io_mapping.items():
            print(coreir_port,peak_port)
            pio = peak_inst.select(peak_port)
            cio = coreir_def.interface.select(coreir_port)
            coreir_def.connect(pio,cio)
        self.coredef = coreir_def

    #returns a map from instance name to peak instr
    def __call__(self,c,app):
        mdef = app.definition
        assert mdef
        mapped_instances = {}
        for inst in mdef.instances:
            inst_mod = inst.module
            if inst_mod == self.coreir_prim:
                mapped_instances[inst.name+"$inst"] = self.prim_instr
                inst_mod.definition = self.coredef
                coreir.inline_instance(inst)

        return mapped_instances


