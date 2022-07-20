from metamapper.irs.mmir import program_to_comb
from metamapper.irs.mmir.comb import QSym
from metamapper.irs.mmir.modules import Base
from metamapper.irs.mmir.synth import SynthQuery
import pytest


padd = '''
comb test.add3
input i0 : bv.bv<16>
input i1 : bv.bv<16>
input i2 : bv.bv<16>
input i3 : bv.bv<16>
output o0 : bv.bv<16>
t0 = bv.add<16>(i0, i1)
t1 = bv.add<16>(i2, i3)
o0 = bv.add<16>(t0, t1)
'''

psub = '''
comb test.sub
input i0 : bv.bv<13>
input i1 : bv.bv<13>
output o0 : bv.bv<13>
o0 = bv.sub<13>(i0, i1)
'''

pnot = '''
comb test.sub
input i0 : bv.bv<13>
output o0 : bv.bv<13>
o0 = bv.not_<13>(i0)
'''



@pytest.mark.parametrize("p", [
    pnot,
    #psub,
])
def test_synth(p):
    comb = program_to_comb(p, [Base()], debug=False)

    op_list = []
    for op in (
        QSym('bv','add',(13,)),
        QSym('bv','add',(13,)),
        QSym('bv','not_',(13,)),
    ):
        op_list.append(Base().comb_from_sym(op))
    #print(comb)
    sq = SynthQuery(comb, op_list, const_list=(1, 0))
    comb = sq.cegis()

    #Verify Round trip
    p1 = comb.serialize()
    print(p1)
    comb1 = program_to_comb(p1)
    p2 = comb1.serialize()
    assert p1 == p2