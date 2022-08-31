from metamapper.irs.mmir import program_to_comb
from metamapper.irs.mmir.comb import QSym
from metamapper.irs.mmir.modules import Base
from metamapper.irs.mmir.synth import SynthQuery, verify
import pytest
import hwtypes as ht


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

psub_v2 = '''
comb test.sub
input i0 : bv.bv<13>
input i1 : bv.bv<13>
output o0 : bv.bv<13>
t0 = bv.not<13>(i1)
t1 = bv.add<13>(t0, 13'h1)
o0 = bv.add<13>(t1, i0)
'''

pnot = '''
comb test.sub
input i0 : bv.bv<13>
output o0 : bv.bv<13>
o0 = bv.not_<13>(i0)
'''

@pytest.mark.parametrize("p,ops", [
    (psub, (
        QSym('bv', 'add', (13,)),
        QSym('bv', 'add', (13,)),
        QSym('bv', 'not_', (13,)),
    ))
])
def test_synth(p,ops):
    comb = program_to_comb(p, [Base()], debug=False)

    op_list = []
    for op in ops:
        op_list.append(Base().comb_from_sym(op))
    sq = SynthQuery(comb, op_list, const_list=(1, 0))
    comb_synth = sq.cegis_comb()
    assert comb_synth is not None
    res = verify(comb, comb_synth)
    assert res is None


    #Verify Round trip
    p1 = comb.serialize()
    print(p1)
    comb1 = program_to_comb(p1)
    p2 = comb1.serialize()
    assert p1 == p2


ab_p_ac = '''
comb test.sub
input a : bv.bv<8>
input b : bv.bv<8>
input c : bv.bv<8>
output o : bv.bv<8>
ab = bv.mul<8>(a,b)
ac = bv.mul<8>(a,c)
o = bv.add<8>(ab, ac)
'''

a_bpc = '''
comb test.sub
input a : bv.bv<8>
input b : bv.bv<8>
input c : bv.bv<8>
output o : bv.bv<8>
b_p_c = bc.add<8>(b, c)
o = bv.mul<8>(a, b_p_c)
'''

# A*(B+C) == A*B + A*C
def test_dist():
    res = verify(ab_p_ac, a_bpc)
    assert res is None


