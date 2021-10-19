from peak import Peak, family_closure, Const
from peak import family
from peak.family import AbstractFamily

@family_closure
def mult_middle_fc(family: AbstractFamily):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    SInt = family.Signed[16]
    UInt = family.Unsigned[16]
    Bit = family.Bit
    @family.assemble(locals(), globals())
    class mult_middle(Peak):
        def __call__(self, in1 : Data, in0 : Data) -> Data:
                res = Data32(in0) * Data32(in1)
                return Data(res[8:24])
    return mult_middle
    