import coreir
import peak
from hwtypes import BitVector, is_adt_type
from hwtypes.adt_meta import BoundMeta

#Represents a single rewrite rule that can be applied to a flattened CoreIR graph
class RewriteRule:
    def __call__(self,c,app):
        raise NotImplementedError

#prim_instr can either be a lambda or an adt instruction
class Peak1to1(RewriteRule):
    def __init__(self,coreir_prim : coreir.module.Module, peak_prim : coreir.module.Module, prim_instr : BoundMeta, io_mapping):
        self.instr_map = {}
        self.coreir_prim = coreir_prim
        if is_adt_type(type(prim_instr)):
            self.instr_lambda = lambda _ : prim_instr
        else:
            self.instr_lambda = prim_instr
        #Actually construct the coreir definition
        coreir_def = coreir_prim.new_definition()
        c = coreir_prim.context

        peak_inst = coreir_def.add_module_instance(name="inst",module=peak_prim)
        for coreir_port,peak_port in io_mapping.items():
            pio = peak_inst.select(peak_port)
            if coreir_port == "0":
                coreir.connect_const(pio,0)
            else:
                cio = coreir_def.interface.select(coreir_port)
                coreir_def.connect(pio,cio)
        self.coredef = coreir_def

    #returns whether any change occured
    def __call__(self,app : coreir.module.Module):
        c = app.context
        mdef = app.definition
        assert mdef
        to_inline = [inst for inst in mdef.instances if inst.module==self.coreir_prim ]
        if len(to_inline)==0:
            return False
        self.coreir_prim.definition = self.coredef
        for inst in to_inline:
            instr = self.instr_lambda(inst)
            inst_name = inst.name+"$inst"
            coreir.inline_instance(inst)
            inlined_inst = mdef.get_instance(inst_name)
            inlined_inst.add_metadata("instr_debug",f"\"{str(instr)}\"")
            self.instr_map[inst_name] = instr
        return len(to_inline)>0

class PeakIO(RewriteRule):
    #Interpreting is_input as an input to the fabric which indicates the io_port_name is an output
    def __init__(self, width, is_input, io_prim : coreir.module.Module):
        io_port_name = None
        for port_name, port_type in io_prim.type.items():
            if port_type.is_output() and is_input:
                io_port_name = port_name
            elif port_type.is_input() and not is_input:
                io_port_name = port_name
        assert io_port_name is not None

        assert io_port_name in dict(io_prim.type.items())
        assert io_prim.type[io_port_name].is_input() == (not is_input)
        assert io_prim.type[io_port_name].is_output() == is_input
        self.io_prim = io_prim
        self.is_input = is_input
        self.io_port_name = io_port_name
        self.width = width

    def __call__(self,app : coreir.module.Module):
        c = app.context
        mdef = app.definition
        io = mdef.interface
        modified = False
        for port_name, port_type in app.type.items():
            if port_type.size != self.width:
                continue
            if port_type.is_input() != self.is_input:
                continue
            modified = True
            #This is a valid port
            pt = mdef.add_passthrough(io.select(port_name))
            
            io_inst = mdef.add_module_instance(name=f"io_{port_name}",module=self.io_prim)
            mdef.connect(pt.select("in"),io_inst.select(self.io_port_name))
            mdef.disconnect(pt.select("in"),io.select(port_name))
            coreir.inline_instance(pt)
        return modified
