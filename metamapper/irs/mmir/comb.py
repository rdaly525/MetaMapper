import abc
import re
from dataclasses import dataclass
import typing as tp
import hwtypes as ht

@dataclass
class BVConst:
    width: int
    val: int

    @property
    def qsym(self):
        return QSym("bv","bv",(self.width,))

    def serialize(self):
        return f"{self.width}\'h{hex(self.val)[2:]}"



def get_sym(qsym_str):
    m = re.search(r'')


@dataclass
class QSym:
    ns: str
    name: str
    genargs: tp.Tuple[int] = ()

    def __post_init__(self):
        assert isinstance(self.genargs, (list, tuple))

    @property
    def qualified_name(self):
        if len(self.genargs) == 0:
            return f"{self.ns}.{self.name}"
        else:
            args_str = ", ".join(str(arg) for arg in self.genargs)
            return f"{self.ns}.{self.name}<{args_str}>"

    def __str__(self):
        return self.qualified_name

    def __hash__(self):
        return hash(self.qualified_name)

    def __eq__(self, other):
        if not isinstance(other, QSym):
            return False
        return self.ns == other.ns and self.name == other.name and all(g0==g1 for g0,g1 in zip(self.genargs,other.genargs))


#Software Module
class Module:
    name: str

    @abc.abstractmethod
    def type_from_sym(self, qsym: QSym) -> 'Type':
        ...

    @abc.abstractmethod
    def comb_from_sym(self, qsym: QSym) -> 'CombFun':
        ...


@dataclass
class Type:
    name: QSym

    @property
    def ns(self):
        return self.name.ns

    @property
    def type(self):
        return self.name.name

    @property
    def genargs(self):
        return self.name.genargs

    @property
    def qualified_name(self):
        return self.qsym.qualified_name

@dataclass
class Var:
    name: str
    type: QSym

@dataclass
class Stmt:
    lhss: tp.Tuple[str]
    op: QSym
    args: tp.Tuple[str]

class Comb:
    def input_free_vars(self, prefix=""):
        return [self.sym_table[ivar.name].free_var(f"{prefix}__{ivar.name}") for ivar in self.inputs]

    def output_free_vars(self, prefix=""):
        return [self.sym_table[ivar.name].free_var(f"{prefix}__{ivar.name}") for ivar in self.outputs]


class Prim(Comb): pass


@dataclass
class CombFun(Comb):
    name: QSym
    inputs: tp.Tuple[Var]
    outputs: tp.Tuple[Var]
    stmts: tp.Tuple[Stmt]


    def create_symbolic_inputs(self):
        assert self._resolved
        return (self.sym_table[ivar.name].free_var(ivar.name) for ivar in self.inputs)

    def serialize(self):
        assert self._resolved
        lines = []
        lines.append(f"comb {self.name}")
        lines += [f"input {i.name} : {i.type}" for i in self.inputs]
        lines += [f"output {o.name} : {o.type}" for o in self.outputs]
        for stmt in self.stmts:
            lhss = ", ".join(stmt.lhss)
            args = []
            for arg in stmt.args:
                if isinstance(arg, BVConst):
                    args.append(arg.serialize())
                else:
                    args.append(arg)
            args = ", ".join(args)
            lines.append(f"{lhss} = {stmt.op}({args})")
        return "\n".join(lines)

    #Only evaling for SMT
    def eval(self, *args):
        if not self._resolved:
            raise ValueError("Link all libraries")
        assert len(args) == len(self.inputs)
        val_table = {var.name:arg for arg, var in zip(args, self.inputs)}
        def get_val(arg):
            if isinstance(arg, BVConst):
                return ht.SMTBitVector[arg.width](arg.val)
            else:
                return val_table[arg]
        for stmt in self.stmts:
            args = [get_val(arg) for arg in stmt.args]
            vals = self.ext_ops[stmt.op].eval(*args)
            assert isinstance(vals, tuple)
            assert len(vals) == len(stmt.lhss)
            for val, sym in zip(vals, stmt.lhss):
                val_table[sym] = val
        return tuple(val_table[var.name] for var in self.outputs)

    def __post_init__(self):
        if len(self.name.genargs) > 0:
            raise NotImplementedError()
        self._resolved = False

    def resolve_type(self, qsym):
        if qsym.ns not in self.modules:
            raise ValueError("Missing module ", qsym.ns)
        return self.modules[qsym.ns].type_from_sym(qsym)

    def resolve_qualified_symbols(self, module_list: tp.List[Module]):
        if self._resolved:
            raise ValueError("Already resolved")
        modules = {m.name:m for m in module_list}
        self.module_list = module_list
        self.modules = modules

        def resolve_op(qsym):
            if qsym.ns not in modules:
                raise ValueError("Missing module ", qsym.ns)
            return modules[qsym.ns].comb_from_sym(qsym)

        #Resolve Ops
        self.ext_ops = {}
        for stmt in self.stmts:
            self.ext_ops[stmt.op] = resolve_op(stmt.op)

        #Type Resolution
        #Type Inference
        #Type checking

        self.sym_table = {} #VARID -> Type
        for ivar in self.inputs:
            assert isinstance(ivar, Var)
            self.sym_table[ivar.name] = self.resolve_type(ivar.type)
        for stmt in self.stmts:
            op = self.ext_ops[stmt.op]
            op_in_types = [op_in.type for op_in in op.inputs]
            op_out_types = [op_out.type for op_out in op.outputs]

            #Verify same number of args
            if len(op_in_types) != len(stmt.args):
                raise ValueError("TC: type mismatch")
            for expected_type, arg in zip(op_in_types, stmt.args):
                if isinstance(arg, BVConst):
                    if expected_type != arg.qsym:
                        raise ValueError(f"TC: {arg} inconsistent BV type")
                else:
                    assert isinstance(arg, str), str(arg)
                    if arg not in self.sym_table:
                        raise ValueError(f"TC: {arg} used before defined")
                    if expected_type != self.sym_table[arg].name:
                        raise ValueError(f"TC: {arg}: ({expected_type}!={self.sym_table[arg].name}) inconsistent types")
            #Verify same number of outputs
            if len(op_out_types) != len(stmt.lhss):
                raise ValueError("TC: Wrong number of outputs")
            for lhs, t in zip(stmt.lhss, op_out_types):
                assert not isinstance(lhs, BVConst)
                self.sym_table[lhs] = self.resolve_type(t)

        # Verify outputs are consistent
        for ovar in self.outputs:
            if ovar.name not in self.sym_table:
                raise ValueError(f"output {ovar.name} never assigned!")
            if ovar.type != self.sym_table[ovar.name].name:
                raise ValueError(f"{ovar.type} != {self.sym_table[ovar.name].name} inconsistent types")
        self._resolved = True