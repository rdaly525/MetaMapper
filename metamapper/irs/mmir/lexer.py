import ply.lex as lex
import ply.yacc as yacc
import typing as tp
from .comb import *

#'genarg  : NUMBER | ...
#'genargs : genarg'
#         | genargs COMMA genarg'
#'qsym    : NSID'
#         | NSID LANGLE genargs RANGLE'
#'sym'    : VARID
#'type'   : qsym
#'input   : INPUT sym COLON type'
#'inputs  : input'
#'        | inputs input'
#'output  : OUTPUT sym COLON type'
#'outputs : output'
#'        | outputs output'
#'arg : sym | BVCONST
#'args : arg
#'     | args COMMA arg'
#'stmt : args ASSIGN op LPAREN args RPAREN'
#'stmts : stmt'
#'      | stmts stmt'

# List of token names.   This is always required
tokens = (
    'NSID',
    'VARID',
    'COMB',
    'INPUT',
    'OUTPUT',
    'COLON',
    'COMMA',
    'NUMBER',
    'BVCONST',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
    'LANGLE',
    'RANGLE',
)

# Regular expression rules for simple tokens
t_COLON   = r':'
t_COMMA   = r','
t_ASSIGN  = r'='
t_LANGLE  = r'\<'
t_RANGLE  = r'\>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

_reserved = dict(
    comb="COMB",
    input="INPUT",
    output="OUTPUT",
)

def t_BVCONST(t):
    r'\'h[0-9a-f]+'
    t.value = int(t.value[2:],16)
    return t

def t_VARID(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    kind = _reserved.get(t.value)
    if kind is not None:
        t.type = kind
    else:
        vals = t.value.split(".")
        if len(vals) > 1:
            t.type = "NSID"
            t.value = vals
        else:
            assert len(vals) == 1
            t.type = "VARID"
    return t

#import re
##like 13'h23
#def parse_bv(s):
#    m = re.search(r'([1-9]\d+)\'h([0-9a-f]*)',s)
#    assert m is not None
#    width = int(m.group(1))
#    val = int(m.group(2))
#    assert 0 <= val < 2**width
#    return BVConst(width, val)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#YACC
start = 'comb'


def p_genarg_0(p):
    'genarg : NUMBER'
    p[0] = p[1]

def p_genargs_0(p):
    'genargs : genarg'
    p[0] = [p[1]]

def p_genargs_1(p):
    'genargs : genargs COMMA genarg'
    p[0] = p[1] + [p[3]]

def p_qsym_0(p):
    'qsym : NSID'
    p[0] = QSym(*p[1])

def p_qsym_1(p):
    'qsym : NSID LANGLE genargs RANGLE'
    p[0] = QSym(*p[1], p[3])

def p_sym_0(p):
    'sym : VARID'
    p[0] = p[1]

def p_type_0(p):
    'type : qsym'
    p[0] = p[1]

# input ::= input <varid> : <type>
def p_input_0(p):
    'input : INPUT VARID COLON type'
    p[0] = Var(p[2], p[4])
# inputs ::= input
#          | inputs input
def p_inputs_0(p):
    'inputs : input'
    p[0] = [p[1]]

def p_inputs_1(p):
    'inputs : inputs input'
    p[0] = p[1] + [p[2]]

# output ::= output <varid> : <type>
def p_output_0(p):
    'output : OUTPUT sym COLON type'
    p[0] = Var(p[2], p[4])

# outputs ::= output
#           | outputs output
def p_outputs_0(p):
    'outputs : output'
    p[0] = [p[1]]

def p_outputs_1(p):
    'outputs : outputs output'
    p[0] = p[1] + [p[2]]

def p_bvconst_0(p):
    'bvconst : NUMBER BVCONST'
    p[0] = BVConst(p[1], p[2])


def p_arg_0(p):
    'arg : sym'
    p[0] = p[1]

def p_arg_1(p):
    'arg : bvconst'
    p[0] = p[1]

# args :: = arg
#         | args comma arg
def p_args_0(p):
    'args : arg'
    p[0] = [p[1]]

def p_args_1(p):
    'args : args COMMA arg'
    p[0] = p[1] + [p[3]]

def p_stmt_1(p):
    'stmt : args ASSIGN qsym LPAREN args RPAREN'
    p[0] = Stmt(p[1], p[3], p[5])

# stmts ::= stmt
#         | stmts stmt

def p_stmts_0(p):
    'stmts : stmt'
    p[0] = [p[1]]

def p_stmts_1(p):
    'stmts : stmts stmt'
    p[0] = p[1] + [p[2]]

# comb ::= <comb> <nsid> <inputs> <outputs> <stmts>
def p_comb_0(p):
    'comb : COMB qsym inputs outputs stmts'
    p[0] = CombFun(p[2], p[3], p[4], p[5])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()


def program_to_comb(program: str, modules, debug=False) -> CombFun:
    comb = parser.parse(program, lexer=lexer, debug=debug)
    if comb is None:
        raise ValueError("Syntax Error!")
    comb.resolve_qualified_symbols(modules)
    return comb

