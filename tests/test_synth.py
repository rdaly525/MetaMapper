from metamapper.irs.mmir import program_to_comb, discover
from metamapper.irs.mmir.comb import QSym
from metamapper.irs.mmir.modules import Base
from metamapper.irs.mmir.synth import SynthQuery, verify
import pytest
import hwtypes as ht

padd4 = '''
comb test.add4
input i0 : bv.bv<16>
input i1 : bv.bv<16>
input i2 : bv.bv<16>
input i3 : bv.bv<16>
output o0 : bv.bv<16>
t1 = bv.add<16>(i2, i3)
t0 = bv.add<16>(i0, i1)
o0 = bv.add<16>(t0, t1)
'''

padd2 = '''
comb test.add2
input i0 : bv.bv<16>
input i1 : bv.bv<16>
output o0 : bv.bv<16>
o0 = bv.add<16>(i0, i1)
'''

padd3 = '''
comb test.add3
input i0 : bv.bv<16>
input i1 : bv.bv<16>
input i2 : bv.bv<16>
output o0 : bv.bv<16>
t0 = bv.add<16>(i0, i1)
o0 = bv.add<16>(i2, t0)
'''
import itertools as it

@pytest.mark.parametrize("p,ops,num_sols", [
    (padd2, tuple(it.repeat(QSym('bv', 'add', (16,)), 1)), 2),
    (padd3, tuple(it.repeat(QSym('bv', 'add', (16,)), 2)), 12),
    (padd4, tuple(it.repeat(QSym('bv', 'add', (16,)), 3)), 144),
])
def test_add(p, ops, num_sols):
    comb = program_to_comb(p)

    op_list = []
    for op in ops:
        op_list.append(Base().comb_from_sym(op))

    sq = SynthQuery(comb, op_list, unique_comm=True)
    combs = sq.gen_all_sols(maxloops=10000, permutations=True, verbose=True)
    assert len(combs) == num_sols, str((len(combs), num_sols))

    sq = SynthQuery(comb, op_list, unique_comm=False)
    combs = sq.gen_all_sols(maxloops=10000, permutations=False, verbose=True)
    assert len(combs)  == num_sols, str((len(combs), num_sols))

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
b_p_c = bv.add<8>(b, c)
o = bv.mul<8>(a, b_p_c)
'''

# A*(B+C) == A*B + A*C
def test_dist():
    c1 = program_to_comb(ab_p_ac)
    c2 = program_to_comb(a_bpc)
    res = verify(c1, c2)
    assert res is None

#@pytest.mark.parametrize("p, N", [
#    (padd2, 3),
#    (padd2, 2),
#])
#def test_discover(p, N: int):
#    c1 = program_to_comb(p)
#    discover(c1)
