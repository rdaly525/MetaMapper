
from dataclasses import dataclass
import typing as tp
import ply.yacc as yacc
from .lexer import MMIRLexer
tokens = MMIRLexer.tokens

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


# varid
# nsid
# number
# type ::= nsid
def p_type_0(p):
    'type : NSID'
    p[0] = Type(*p[1].value)

# input ::= input <varid> : <type>
def p_input_0(p):
    'input : INPUT VARID COLON type'
    t = Type(*p[4].value)
    p[0] = Var(p[2].value, t)
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
    'output : OUTPUT VARID COLON TYPE'
    t = Type(*p[4].value)
    p[0] = Var(p[2].value, t)

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
    p[0] = Op(*p[1].value)

def p_op_0(p):
    'op : NSID LANGLE genargs RANGLE'
    p[0] = Op(*p[1].value, p[3])

# args :: = varid
#         | args comma varid
def p_args_0(p):
    'args : VARID'
    p[0] = [p[1].value]

def p_args_1(p):
    'args : args COMMA VARID'
    p[0] = p[1] + [p[3].value]

# stmt ::= <varid> : <type> <- op "(" <id>(, <id>)
def p_stmt_1(p):
    'stmt : VARID COLON type ASSIGN op LPAREN args RPAREN'
    lhs = Var(p[1].value,Type(*p[3].value))
    p[0] = Stmt(lhs,p[5],p[7])

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
    p[0] = Comb(*p[2].value, p[3], p[4], p[5])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
