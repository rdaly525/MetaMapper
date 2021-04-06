from peak import family, family_closure, Peak, name_outputs, Const
from metamapper import peak_util as putil
from metamapper import CoreIRContext
from lassen import PE_fc

PE = PE_fc(family.MagmaFamily())
cmod = putil.magma_to_coreir(PE)
c = CoreIRContext()
c.serialize_header("lassen_header.json", [cmod])