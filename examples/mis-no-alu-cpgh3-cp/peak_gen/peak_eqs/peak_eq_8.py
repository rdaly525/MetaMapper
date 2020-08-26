
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_8_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_8(Peak):
        def __call__(self, const1 : Const(Data), const0 : Const(Data), in2 : Data, in3 : Data) -> Data:
            
            return Data(Data(Data(in2 + in3) + const1) >> const0)
      
    return mapping_function_8
