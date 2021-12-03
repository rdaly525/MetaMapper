from metamapper.lake_pond import gen_Pond_fc
from peak import family
from metamapper import peak_util as putil
from metamapper import CoreIRContext

Pond_fc = gen_Pond_fc()
Pond = Pond_fc(family.MagmaFamily())
cmod = putil.magma_to_coreir(Pond)
c = CoreIRContext()
c.serialize_header("libs/pond_header.json", [cmod])


