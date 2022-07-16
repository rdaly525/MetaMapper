from metamapper.irs.mmir import program_to_ast
from metamapper.irs.mmir.modules import Base
import pytest


padd = '''
comb test.add3
input i0 : bv.bv<16>
input i1 : bv.bv<16>
input i2 : bv.bv<16>
output o0 : bv.bv<16>
t0 = bv.add<16>(i0, i1)
o0 = bv.add<16>(t0, i2)
'''

pconst = '''
comb test.pconst
input i0 : bv.bv<13>
output o0 : bv.bv<13>
o0 = bv.add<13>(i0, 13'h23)
'''

pmulti_out = '''
comb test.multi_out
input  i0 : bv.bv<13>
output o0 : bv.bv<13>
output o1 : bv.bv<13>
o0, o1 = bv.addsub<13>(i0, 13'h23)
'''


#TODO, small dependent typing
pgen = '''
comb test.addN<n>
input i0 : b.bv<n>
input i1 : b.bv<n>
output o0 : b.bv<n>
o0 : b.bv<n> = bv.add<n>(i0, i1)
'''

@pytest.mark.parametrize("p", [
    padd,
    pconst,
    pmulti_out,
])
def test_programs(p):
    result = program_to_ast(p, debug=False)
    assert result is not None
    result.resolve_qualified_symbols(dict(bv=Base()))
    print(result)
