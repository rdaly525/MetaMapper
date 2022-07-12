from metamapper.irs.mmir import program_to_ast
from metamapper.irs.mmir.lexer import lexer

# Test it out
program = '''
comb ab.cdef
input i0 : bv.16
output o0 : bv.16
t0 : bv.16 <- bv.add<16>(i0, i0)
o0 : bv.16 <- bv.neg<16>(t0)
'''
def test_lex():
    # Build the lexer

    # Give the lexer some input
    lexer.input(program)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

    result = program_to_ast(program)
    print(result)
