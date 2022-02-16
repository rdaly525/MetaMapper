from metamapper.lake_mem import gen_MEM_fc
from peak import family
from metamapper import peak_util as putil
from metamapper import CoreIRContext


def test_mem_header():
    MEM_fc = gen_MEM_fc()
    MEM_py = MEM_fc(family.PyFamily())
    MEM = MEM_fc(family.MagmaFamily())
    cmod = putil.magma_to_coreir(MEM)
    c = CoreIRContext()
    c.serialize_header("libs/mem_header.json", [cmod])

