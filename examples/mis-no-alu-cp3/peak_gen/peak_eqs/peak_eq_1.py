
from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mapping_function_1_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    SData = family.Signed[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mapping_function_1(Peak):
        def __call__(self, const0 : Const(Data), const1 : Const(Data), in2 : Data, in1 : Data) -> Data:
            
            return Data(Data(Data(in2 + in1) + const0) >> const1)
      
    return mapping_function_1
