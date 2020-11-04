
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function(Peak):
        def __call__(self, in1 : Data, in0 : Data) -> Data:
            
            return Data((SData(in0) <= SData(in1)).ite(SData(in0), SData(in1)))
      
    return mapping_function
