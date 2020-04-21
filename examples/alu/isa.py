from peak import family_closure
from hwtypes import Enum, Product

class OP(Enum):
    Add = 2
    Sub = 3
    Or =  4
    And = 5
    XOr = 6

class Inst(Product):
    op = OP
