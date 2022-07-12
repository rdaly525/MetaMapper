import ply.lex as lex
import ply.yacc as yacc


#'type : NSID'
#'input : INPUT VARID COLON type'
#'inputs : input'
#'inputs : inputs input'
#'output : OUTPUT VARID COLON TYPE'
#'outputs : output'
#'outputs : outputs output'
#'genargs : NUMBER'
#'genargs : genargs COMMA NUMBER'
#'op : NSID'
#'op : NSID LANGLE genargs RANGLE'
#'args : VARID'
#'args : args COMMA VARID'
#'stmt : VARID COLON type ASSIGN op LPAREN args RPAREN'
#'stmts : stmt'
#'stmts : stmts stmt'

# List of token names.   This is always required
tokens = (
    'ID',
    'NSID',
    'VARID',
    'COMB',
    'INPUT',
    'OUTPUT',
    'COLON',
    'COMMA',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
    'LANGLE',
    'RANGLE',
)

# Regular expression rules for simple tokens
t_COLON   = r':'
t_COMMA   = r','
t_ASSIGN  = r'\<\-'
t_LANGLE  = r'\<'
t_RANGLE  = r'\>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

_reserved = dict(
    comb="COMB",
    input="INPUT",
    output="OUTPUT",
)

def t_ID(t):
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

# A regular expression rule with some action code
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
#
from dataclasses import dataclass
import typing as tp

@dataclass
class Type:
    ns: str
    type: str

@dataclass
class Var:
    name: str
    type: Type

@dataclass
class Op:
    ns: str
    name: str
    genargs: tp.Tuple[int] = ()

@dataclass
class Stmt:
    lhs: Var
    op: Op
    args: tp.Tuple[Var]

@dataclass
class Comb:
    ns: str
    name: str
    inputs: tp.Tuple[Var]
    outputs: tp.Tuple[Var]
    stmts: tp.Tuple[Stmt]

# type ::= nsid
def p_type_0(p):
    'type : NSID'
    p[0] = Type(*p[1])

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
    'output : OUTPUT VARID COLON type'
    p[0] = Var(p[2], p[4])

# outputs ::= output
#           | outputs output
def p_outputs_0(p):
    'outputs : output'
    p[0] = [p[1]]

def p_outputs_1(p):
    'outputs : outputs output'
    p[0] = p[1] + [p[2]]

# genargs ::= number
#            | genargs comma number
def p_genargs_0(p):
    'genargs : NUMBER'
    p[0] = [p[1]]

def p_genargs_1(p):
    'genargs : genargs COMMA NUMBER'
    p[0] = p[1] + [p[3]]

# op ::= nsid
#      | nsid langle genargs rangle
def p_op_0(p):
    'op : NSID'
    p[0] = Op(*p[1])

def p_op_0(p):
    'op : NSID LANGLE genargs RANGLE'
    p[0] = Op(*p[1], p[3])

# args :: = varid
#         | args comma varid
def p_args_0(p):
    'args : VARID'
    p[0] = [p[1]]

def p_args_1(p):
    'args : args COMMA VARID'
    p[0] = p[1] + [p[3]]

# stmt ::= <varid> : <type> <- op "(" <id>(, <id>)
def p_stmt_1(p):
    'stmt : VARID COLON type ASSIGN op LPAREN args RPAREN'
    lhs = Var(p[1], p[3])
    p[0] = Stmt(lhs, p[5], p[7])

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
    'comb : COMB NSID inputs outputs stmts'
    p[0] = Comb(*p[2], p[3], p[4], p[5])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()


def program_to_ast(program: str):
    return parser.parse(program, lexer=lexer)

