from .ir import gen_peak_CoreIR
from ...node import Nodes, Constant, DagNode, Select
from ... import CoreIRContext
from ...peak_util import load_from_peak, peak_to_coreir
import coreir
from hwtypes import BitVector, Product, strip_modifiers
from peak import family

def strip_trailing(op):
    if op[-1] == "_":
        return op[:-1]
    return op

def gen_CoreIRNodes(width):
    CoreIRNodes = Nodes("CoreIR")
    peak_ir = gen_peak_CoreIR(width)
    c = CoreIRContext()

    basic = ("mul", "add", "const", "and_", "or_", "neg")
    other = ("ashr", "eq", "lshr", "mux", "sub", "slt", "sle", "sgt", "sge", "ult", "ule", "ugt", "uge", "shl")
    bit_ops = ("const", "or_", "and_", "xor", "not_", "mux")
    commonlib_ops = ("abs", "smax", "smin", "umin", "umax")
    for namespace, ops, is_module in (
        ("corebit", bit_ops, True),
        ("coreir", basic + other, False)
        #("commonlib", commonlib_ops, False)
    ):
        for op in ops:
            assert c.get_namespace(namespace) is c.get_namespace(namespace)
            name = f"{namespace}.{op}"
            peak_fc = peak_ir.instructions[name]
            coreir_op = strip_trailing(op)
            if is_module:
                cmod = c.get_namespace(namespace).modules[coreir_op]
            else:
                gen = c.get_namespace(namespace).generators[coreir_op]
                cmod = gen(width=width)
            modparams = ()
            if op == "const":
                modparams = ("value",)
            name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name=name, modparams=modparams)
            assert name_ == name
            assert name in CoreIRNodes.coreir_modules
            assert CoreIRNodes.name_from_coreir(cmod) == name
            # print(f"Loaded {name}!")


      

    class Rom(DagNode):
        def __init__(self, raddr, ren, *, init, iname):
            super().__init__(raddr, ren, init=init, iname=iname)
            self.modparams=()

        @property
        def attributes(self):
            return ("init", "iname")

        #Hack to get correct port name
        def select(self, field, original=None):
            self._selects.add("rdata")
            return Select(self, field="rdata",type=BitVector[16])

        nodes = CoreIRNodes
        static_attributes = {}
        node_name = "memory.rom2"
        num_children = 2
        type = Product.from_fields("Output",{"rdata":BitVector[16]})

    rom2 = CoreIRContext().get_namespace("memory").generators["rom2"](depth=1024, width=width)

    CoreIRNodes.add("memory.rom2", peak_ir.instructions["memory.rom2"], rom2, Rom)
    assert "memory.rom2" in CoreIRNodes.dag_nodes
    assert CoreIRNodes.dag_nodes["memory.rom2"] is not None
    

    # name = f"coreir.ashr32"
    # peak_fc = peak_ir.instructions[name]
    # cmod = c.get_namespace("coreir").generators["ashr"](width=32)
    # name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.ashr32", modparams=())

    # name = f"coreir.mul32"
    # peak_fc = peak_ir.instructions[name]
    # cmod = c.get_namespace("coreir").generators["mul"](width=32)
    # name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.mul32", modparams=())

    # name = f"coreir.sext"
    # peak_fc = peak_ir.instructions[name]
    # cmod = c.get_namespace("coreir").generators["sext"](width_in=16, width_out=32)
    # name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.sext", modparams=())

    # name = f"coreir.slice"
    # peak_fc = peak_ir.instructions[name]
    # cmod = c.get_namespace("coreir").generators["slice"](width=32, hi=24, lo=8)
    # name_ = load_from_peak(CoreIRNodes, peak_fc, cmod=cmod, name="coreir.slice", modparams=())

    peak_fc = peak_ir.instructions["commonlib.mult_middle"]
    MultMiddle = CoreIRNodes.create_dag_node("commonlib.mult_middle", 2, stateful=False, static_attrs=dict(type=strip_modifiers(peak_fc(family.PyFamily()).output_t)), modparams=())

    mult_middle = CoreIRContext().get_namespace("commonlib").generators["mult_middle"](width=width)

    CoreIRNodes.add("commonlib.mult_middle", peak_ir.instructions["commonlib.mult_middle"], mult_middle, MultMiddle)
    assert "commonlib.mult_middle" in CoreIRNodes.dag_nodes
    assert CoreIRNodes.dag_nodes["commonlib.mult_middle"] is not None
    
    return CoreIRNodes

