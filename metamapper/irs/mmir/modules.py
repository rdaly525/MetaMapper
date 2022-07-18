from .comb import Module, QSym, Prim, Var
import hwtypes as ht


class BV:
    def __init__(self, N: int):
        assert isinstance(N, int)
        assert N > 0
        self.N = N
        self.name = QSym('bv', 'bv', (N,))

    def free_var(self, name):
        return ht.SMTBitVector[self.N](prefix=name)

class Bool:
    name = QSym('bv', 'bool')

    def free_var(self, name):
        return ht.SMTBit(prefix=name)


_binops = dict(
    add=lambda x, y: x + y,
    sub=lambda x, y: x - y,
    mul=lambda x, y: x + y,
)

_unary_ops = dict(
    neg=lambda x: -x,
    not_=lambda x: ~x,
)

class BVUnary(Prim):
    def __init__(self, N, op):
        self.N = N
        self.name = QSym("bv", op, (N,))
        assert op in _unary_ops
        self.op = _unary_ops[op]
        bv_t = QSym('bv','bv',(N,))
        self.inputs = (Var('i0', bv_t),)
        self.outputs = (Var('o0',bv_t),)
        bv_t = Base().type_from_sym(bv_t)
        self.sym_table = dict(
            i0=bv_t,
            o0=bv_t,
        )


    def eval(self, a):
        return (self.op(a),)


class BVBinary(Prim):
    def __init__(self, N, op):
        self.N = N
        self.name = QSym("bv", op, (N,))
        assert op in _binops
        self.op = _binops[op]
        bv_t = QSym('bv','bv',(N,))
        self.inputs = (Var('i0', bv_t), Var('i1', bv_t))
        self.outputs = (Var('o0',bv_t),)
        bv_t = Base().type_from_sym(bv_t)
        self.sym_table = dict(
            i0=bv_t,
            i1=bv_t,
            o0=bv_t,
        )


    def eval(self, a, b):
        return (self.op(a, b),)

class BVAddSub(Prim):
    def __init__(self, N):
        self.N = N
        bv_t = QSym('bv','bv',(N,))
        self.inputs = (Var('i0', bv_t), Var('i1', bv_t))
        self.outputs = (Var('o0',bv_t), Var('o1', bv_t))

    def eval(self, a, b):
        return (a+b, a-b)


class Base(Module):
    # Types
    name = 'bv'

    def type_from_sym(self, qsym: QSym):
        assert qsym.ns == self.name
        if qsym.name == "bv":
            return BV(*qsym.genargs)
        elif qsym.name == "bool":
            return Bool()
        else:
            raise ValueError(f"{qsym} not found")

    def comb_from_sym(self, qsym: QSym):
        assert qsym.ns == self.name
        if qsym.name in _binops:
            return BVBinary(*qsym.genargs, qsym.name)
        elif qsym.name in _unary_ops:
            return BVUnary(*qsym.genargs, qsym.name)
        raise NotImplementedError()
