from lassen import PE_fc as lassen_fc

from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
import metamapper.peak_util as putil
from metamapper import CoreIRContext
from metamapper.delay_matching import STA, CombineRegs
from metamapper.common_passes import print_dag, gen_dag_img_simp, gen_dag_img
from lassen.sim import PE_fc as lassen_fc
import sys



file_name = str(sys.argv[1])
lassen_header = "/nobackup/melchert/MetaMapper/libs/lassen_header.json"

if len(sys.argv) > 2:
    pe_cycles = int(sys.argv[2])
else:
    pe_cycles = 0

c = CoreIRContext(reset=True)
cmod = cutil.load_from_json(file_name)

nodes = gen_CoreIRNodes(16)
putil.load_and_link_peak(
    nodes,
    lassen_header,
    {"global.PE": lassen_fc},
)
kernels = dict(c.global_namespace.modules)
for kname, kmod in kernels.items():
    if kname != "PE":
        print(f"{kname}")
        dag = cutil.coreir_to_dag(nodes, kmod)
        CombineRegs().run(dag)
        print(STA().doit(dag))

        gen_dag_img_simp(dag, f"img/{kname}")
        gen_dag_img(dag, f"img/{kname}_complex")