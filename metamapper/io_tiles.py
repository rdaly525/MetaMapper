


from hwtypes import BitVector
from peak import family, family_closure, Peak, name_outputs, Const

@family_closure
def IO_fc(family):
    BV = family.BitVector
    Bit = family.Bit

    @family.assemble(locals(), globals())
    class IO(Peak):
        @name_outputs(out=BV[16])
        def __call__(self, in_: BV[16]) -> (BV[16]):
            return in_

    return IO

@family_closure
def BitIO_fc(family):
    BV = family.BitVector
    Bit = family.Bit

    @family.assemble(locals(), globals())
    class BitIO(Peak):
        @name_outputs(out=Bit)
        def __call__(self, in_: Bit) -> (Bit):
            return in_

    return BitIO

