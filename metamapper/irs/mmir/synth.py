import itertools as it

from pysmt.fnode import FNode

import peak.mapper.formula_constructor as fc
import hwtypes as ht
from dataclasses import dataclass
from .comb import Comb, CombFun, Stmt, QSym, Var, BVConst
from .modules import BV as mds_BV
import typing as tp
import pysmt.shortcuts as smt
from pysmt.logics import QF_BV

class IterLimitError(Exception):
    pass


def _int_to_pysmt(x: int, sort):
    if sort.is_bv_type():
        return smt.BV(x % sort.width, sort.width)
    else:
        assert sort.is_bool_type()
        return smt.Bool(bool(x))

def _to_int(x):
    assert x.is_constant()
    return x.constant_value()


SBV = ht.SMTBitVector
SBit = ht.SMTBit

def flat(l):
    return [l__ for l_ in l for l__ in l_]


@dataclass
class SynthQuery:
    spec: CombFun
    op_list: tp.List[Comb]
    const_list: tp.Tuple[int] = ()
    unique_comm: bool = True

    #TODO have a strict ordering on identical operations
    def __post_init__(self):
        # Structure
        input_vars = self.spec.input_free_vars(prefix="VI")
        Ninputs = len(input_vars)
        hard_consts = self.const_list
        Nconsts = len(hard_consts)
        #const_vars = []
        output_vars = self.spec.output_free_vars(prefix="VO")
        op_out_vars = []
        op_in_vars = []
        tot_locs = Ninputs + Nconsts
        for i, op in enumerate(self.op_list):
            assert isinstance(op, Comb)
            op_in_vars.append(op.input_free_vars(f"V_op{i}"))
            op_out_vars.append(op.output_free_vars(f"V_op{i}"))
            tot_locs += len(op.outputs)
        self.vars = (input_vars, hard_consts, output_vars, op_out_vars, op_in_vars)

        lvar_t = SBV[len(bin(tot_locs))-2]
        #These can be hardcoded
        input_lvars = list(range(len(input_vars)))
        Ninputs = len(input_vars)
        hard_const_lvars = list(range(Ninputs, Ninputs +len(hard_consts)))
        op_out_lvars = []
        op_in_lvars = []
        for i, op in enumerate(self.op_list):
            op_out_lvars.append([lvar_t(prefix=f"Lo[{i},{j}]") for j in range(len(op.outputs))])
            op_in_lvars.append([lvar_t(prefix=f"Li[{i},{j}]") for j in range(len(op.inputs))])
        output_lvars = [lvar_t(prefix=f"Lo{i}") for i in range(len(output_vars))]

        #get list of lvars (existentially quantified in final query)
        self.E_vars = output_lvars + flat(op_out_lvars) + flat(op_in_lvars)
        self.lvars = (input_lvars, hard_const_lvars, output_lvars, op_out_lvars, op_in_lvars)


        #Formal Spec (P_spec)
        P_spec = []
        for (i, ov) in enumerate(self.spec.eval(*input_vars)):
            P_spec.append(output_vars[i] == ov)

        #Lib Spec (P_lib)
        #   temp_var[i] = OP(*op_in_vars[i])
        P_lib = []
        for i, op in enumerate(self.op_list):
            ovars = op.eval(*op_in_vars[i])
            for j, op_out_var in enumerate(ovars):
                P_lib.append(op_out_vars[i][j] == op_out_var)


        #Well formed program (P_wfp)
        And = fc.And
        flat_op_out_lvars = flat(op_out_lvars)

        # Temp locs and output locs are in range of temps
        P_in_range = []
        for lvar in flat_op_out_lvars:
            P_in_range.append(And([lvar>=Ninputs+Nconsts, lvar < tot_locs]))

        #op in locs and outputs are in range(0,tot)
        for lvars in [lvars for lvars in op_in_lvars] + [output_lvars]:
            for lvar in lvars:
                P_in_range.append(lvar < tot_locs)


        # Temp locs are unique
        P_loc_unique = []
        for i in range(len(flat_op_out_lvars)):
            for j in range(i+1, len(flat_op_out_lvars)):
                P_loc_unique.append(flat_op_out_lvars[i] != flat_op_out_lvars[j])

        # multi outputs are off by 1
        P_multi_out = []
        for lvars in op_out_lvars:
            for lv0, lv1 in zip(lvars, lvars[1:]):
                P_multi_out.append(lv0+1==lv1)

        P_acyc = []
        # ACYC Constraint
        #  op_out_lvars[i] > op_in_lvars[i]
        for o_lvars, i_lvars in zip(op_out_lvars, op_in_lvars):
            P_acyc += [o_lvars[0] > ilvar for ilvar in i_lvars]


        #Same operations have a strict order
        op_to_i = {}
        for i, op in enumerate(self.op_list):
            op_to_i.setdefault(op.name, []).append(i)

        P_same_op = []
        for op, ilist in op_to_i.items():
            if len(ilist) > 1:
                for i, j in zip(ilist[:-1], ilist[1:]):
                    assert i < j
                    P_same_op.append(op_out_lvars[i][0] < op_out_lvars[j][0])


        #Strict ordering on arguments of commutative ops
        P_comm = []
        if self.unique_comm:
            for i, op in enumerate(self.op_list):
                if op.commutative:
                    for lv0, lv1 in  zip(op_in_lvars[i][:-1], op_in_lvars[i][1:]):
                        P_comm.append(lv0 <= lv1)


        P_wfp = [
            And(P_in_range),
            And(P_loc_unique),
            And(P_multi_out),
            And(P_acyc),
            And(P_same_op),
            And(P_comm),
        ]

        #Locations correspond to vars (P_conn)
        # (Lx == Ly) => (X==Y)
        pairs = []
        for lvars, vars in (
            (input_lvars, input_vars),
            (output_lvars, output_vars),
            (hard_const_lvars, hard_consts),
            (flat(op_out_lvars), flat(op_out_vars)),
            (flat(op_in_lvars), flat(op_in_vars)),
        ):
            for lvar, var in zip(lvars, vars):
                pairs.append((lvar, var))
        P_conn = []
        for i in range(len(pairs)):
            for j in range(i+1, len(pairs)):
                lv0, v0 = pairs[i]
                lv1, v1 = pairs[j]
                #Types need to match
                #Type is allowed to be an int
                if type(v0) != type(v1) and not isinstance(v0, int) and  not isinstance(v1, int):
                    continue
                #skip if both loc vars are int
                if isinstance(lv0, int) and isinstance(lv1, int):
                    continue
                P_conn.append(fc.Implies(lv0==lv1, v0==v1))


        #Final query:
        #  Exists(L) Forall(V) P_wfp(L) & (P_lib & P_conn) => P_spec
        query = And([
            And(P_wfp),
            fc.Implies(
                And([And(P_lib), And(P_conn)]),
                And(P_spec)
            )
        ])
        #in fc form
        self.query = query
        #print(self.query.serialize())
        #Create the massive bitvector
        self.unique_dag = {}
        for i, _ in enumerate(self.op_list):
            for j, i_lvar in enumerate(op_in_lvars[i]):
                for k in input_lvars:
                    self.unique_dag[(i, j, k, 0)] = (i_lvar==k)
                for k, _ in enumerate(self.op_list):
                    for l, o_lvar in enumerate(op_out_lvars[k]):
                        self.unique_dag[(i,j,k+len(input_lvars),l)] = (i_lvar==o_lvar)

    def unique_dag_cond(self, sol, debug=False):
        input_lvars, hard_const_lvars, output_lvars, op_out_lvars, op_in_lvars = self.lvars
        unique_dag = {}
        for i, _ in enumerate(self.op_list):
            for j, i_lvar in enumerate(op_in_lvars[i]):
                for k in input_lvars:
                    unique_dag[(i, j, k, 0)] = (_to_int(sol[i_lvar.value])==k)
                    if debug:
                        print(f"{(i, j, k, 0)} -> {unique_dag[(i, j, k, 0)]}")
                for k, _ in enumerate(self.op_list):
                    for l, o_lvar in enumerate(op_out_lvars[k]):
                        k_ = k + len(input_lvars)
                        unique_dag[(i,j,k_,l)] = (_to_int(sol[i_lvar.value])==_to_int(sol[o_lvar.value]))
                        if debug:
                            print(f"{(i, j, k_, l)} -> {unique_dag[(i, j, k_, l)]}")

        assert unique_dag.keys() == self.unique_dag.keys()
        P_unique = []
        for k in unique_dag:
            P_unique.append(self.unique_dag[k] == unique_dag[k])
        return fc.And(P_unique).to_hwtypes().value

    def gen_permutations(self, sol):
        #Get indices of each commutative op
        input_lvars, hard_const_lvars, output_lvars, op_out_lvars, op_in_lvars = self.lvars
        commute_idxs = []
        for i, op in enumerate(self.op_list):
            if op.commutative:
                commute_idxs.append(i)


        lvar_perms = []
        lvar_list = []
        for i in commute_idxs:
            lvar_list += [lvar.value for lvar in op_in_lvars[i]]
            lvals = [sol[lvar.value] for lvar in op_in_lvars[i]]
            lvar_perms.append(it.permutations(lvals))

        sols = []
        for lvals in it.product(*lvar_perms):
            lval_list = flat([lval_tuple for lval_tuple in lvals])
            new_vals = {lvar: lval for lvar, lval in zip(lvar_list, lval_list)}
            new_sol = {**sol, **new_vals}
            sols.append(new_sol)
        assert sum([int(sol==_sol) for _sol in sols]) == 1, str([int(sol==_sol) for _sol in sols])
        return sols

    #Tactic. Generate all the non-permuted solutions.
    # For each of those solutions, generate all the permutations
    def gen_all_sols(self, logic=QF_BV, maxloops=1000, solver_name="z3", verbose=False, permutations=True):
        sol = self.cegis(logic, maxloops, solver_name, verbose)

        exclude_list = []
        combs = []
        _unique_cache = {}
        while sol is not None:
            if permutations:
                sol_perms = self.gen_permutations(sol)
            else:
                sol_perms = [sol]
            for sol_perm in sol_perms:
                comb_perm = self.comb_from_solved(sol_perm)
                combs.append(comb_perm)
                p_serialize = comb_perm.serialize()
                if p_serialize in _unique_cache:
                    raise ValueError("Somethng went wrong")
                _unique_cache[p_serialize] = sol_perm
            exclude_list.append(sol)
            try:
                sol = self.cegis(logic, maxloops, solver_name, verbose, exclude_list=exclude_list)
            except IterLimitError:
                break
        return combs

    def cegis(self, logic=QF_BV, maxloops=1000, solver_name="z3", verbose=True, exclude_list=[]):
        assert maxloops > 0
        query = self.query.to_hwtypes().value

        for sol in exclude_list:
            sol_term = smt.Bool(True)
            for var, val in sol.items():
                sol_term = smt.And(sol_term, smt.Equals(var, val))
            query = smt.And(query, smt.Not(sol_term))
            #query = smt.And(query, smt.Not(self.unique_dag_cond(sol)))

        #get exist vars:
        E_vars = set(var.value for var in self.E_vars)  # forall_vars
        A_vars = query.get_free_variables() - E_vars  # exist vars

        with smt.Solver(logic=logic, name=solver_name) as solver:
            solver.add_assertion(smt.Bool(True))

            # Start with checking all A vals beings 0
            A_vals = {v: _int_to_pysmt(0, v.get_type()) for v in A_vars}
            solver.add_assertion(query.substitute(A_vals).simplify())
            for i in range(maxloops):
                E_res = solver.solve()
                if verbose and i%50==0:
                    print(f"{i}..", end='', flush=True)

                if not E_res:
                    if verbose:
                        print("No solution, UNSAT")
                    return None
                else:
                    E_guess = {v: solver.get_value(v) for v in E_vars}
                    query_guess = query.substitute(E_guess).simplify()
                    model = smt.get_model(smt.Not(query_guess), solver_name=solver_name, logic=logic)

                    if model is None:
                        if verbose:
                            print("SAT")
                        return E_guess
                    else:
                        A_vals = {v: model.get_value(v) for v in A_vars}
                        solver.add_assertion(query.substitute(A_vals).simplify())

            raise IterLimitError(f"Unknown result in CEGIS in {maxloops} number of iterations")

    def cegis_comb(self, logic=QF_BV, maxloops=1000, solver_name="z3", verbose=True):
        E_vals = self.cegis(logic, maxloops, solver_name, verbose)
        if E_vals is not None:
            return self.comb_from_solved(E_vals)

    def comb_from_solved(self, lvals):

        inputs = self.spec.inputs
        outputs = self.spec.outputs

        input_vars, hard_consts, output_vars, op_out_vars, op_in_vars = self.vars
        input_lvars, hard_const_lvars, output_lvars, op_out_lvars, op_in_lvars = self.lvars

        #Fill in all the lvars
        def to_int(val:FNode):
            return int(val.constant_value())
        output_lvars = [to_int(lvals[lvar.value]) for lvar in output_lvars]
        def name_from_loc(loc, src=None):
            if loc < len(inputs):
                return f"i{loc}"
            elif loc < len(inputs) + len(hard_consts):
                assert src is not None
                i, j = src
                type = self.spec.resolve_type(self.op_list[i].inputs[j].type)
                if isinstance(type, mds_BV):
                    return BVConst(type.N, hard_consts[loc-len(inputs)])
                else:
                    raise NotImplementedError()
            else:
                loc = loc - (len(inputs) + len(hard_consts))
                return f"t{loc}"


        out_lvar_vals = {}
        in_lvar_vals = {}
        for i in range(len(op_out_lvars)):
            out_lvar_vals[i] = [to_int(lvals[lvar.value]) for lvar in op_out_lvars[i]]
            in_lvar_vals[i] = [to_int(lvals[lvar.value]) for lvar in op_in_lvars[i]]

        stmts = []
        for i, out_lvars in sorted(out_lvar_vals.items(), key=lambda item: item[1][0]):
            lhss = [name_from_loc(loc) for loc in out_lvars]
            op = self.op_list[i]
            args = [name_from_loc(loc,src=(i,j)) for j, loc in enumerate(in_lvar_vals[i])]
            stmts.append(Stmt(lhss, op.name, args))
        outputs = [Var(name_from_loc(output_lvars[i]),v.type) for i, v in enumerate(self.spec.outputs)]
        name = QSym('solved', 'v0')
        comb = CombFun(name, inputs, outputs, stmts)
        comb.resolve_qualified_symbols(self.spec.module_list)
        return comb

def verify(comb0: Comb, comb1: Comb, logic=QF_BV, solver_name='z3'):
    #Verify that the two interfaces are identical
    for i0, i1 in zip(comb0.inputs, comb1.inputs):
        assert i0.type == i1.type
    for o0, o1 in zip(comb0.outputs, comb1.outputs):
        assert o0.type == o1.type

    inputs = comb0.input_free_vars()
    o0 = comb0.eval(*inputs)
    o1 = comb1.eval(*inputs)

    formula = fc.And(o0_ == o1_ for o0_, o1_ in zip(o0, o1))

    not_formula = ~(formula.to_hwtypes())

    with smt.Solver(logic=logic, name=solver_name) as solver:
        solver.add_assertion(not_formula.value)
        res = solver.solve()
        if res is False:
            return None
        vals = {v.value: v.value.constant_value() for v in inputs}
        return vals
















