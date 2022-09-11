from metamapper.irs.mmir import program_to_comb, discover
from metamapper.irs.mmir.comb import QSym
from metamapper.irs.mmir.modules import Base
from metamapper.irs.mmir.synth import SynthQuery, verify
import pytest
import hwtypes as ht

psub = '''
comb test.sub
input a : bv.bv<8>
input b : bv.bv<8>
output o : bv.bv<8>
t0 = bv.identity<8>(a)
'''


ops = [
    #'identity',
    #'not_',
    'neg',
    'add',
    #'mul',
    'sub',
]

@pytest.mark.parametrize("p, N", [
    (psub, 2),
])
def test_discover(p, N: int):
    c1 = program_to_comb(p)
    op_list = [QSym('bv', op, (8,)) for op in ops]
    discover(c1, op_list)
