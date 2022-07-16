from metamapper.irs.mmir import program_to_ast
from metamapper.irs.mmir.lexer import lexer
from metamapper.irs.mmir.modules import b
import pytest


padd = '''
comb test.add3
input i0 : b.bv<16>
input i1 : b.bv<16>
input i2 : b.bv<16>
output o0 : b.bv<16>
t0 : b.bv<16> = bv.add<16>(i0, i1)
o0 : b.bv<16> = bv.add<16>(t0, i2)

'''

pconst = '''
comb test.pconst
input i0 : bv.13
output o0 : bv.13
o0 : bv.13 = bv.add<13>(i0, 13'h23)
'''

@pytest.mark.parametrize("p", [
    padd,
    pconst,
])
def test_synth(p):
    comb = program_to_ast(p, debug=False)
    comb.resolve_qualified_symbols()


    assert result is not None
    print(result)