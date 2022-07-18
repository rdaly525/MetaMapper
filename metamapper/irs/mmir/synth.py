from pysmt.fnode import FNode

import peak.mapper.formula_constructor as fc
import hwtypes as ht
from dataclasses import dataclass
from .comb import Comb, CombFun, Stmt, QSym, Var, BVConst
import typing as tp
import pysmt.shortcuts as smt
from pysmt.logics import QF_BV, BV

def _int_to_pysmt(x: int, sort):
    if sort.is_bv_type():
        return smt.BV(x % sort.width, sort.width)
    else:
        assert sort.is_bool_type()
        return smt.Bool(bool(x))



SBV = ht.SMTBitVector
SBit = ht.SMTBit

def flat(l):
    return [l__ for l_ in l for l__ in l_]

@dataclass
class SynthQuery:
    spec : CombFun
    op_list : tp.List[Comb]
    const_list : tp.Tuple[int] = (0,1,-1)

    def __post_init__(self):
        # Structure
        input_vars = self.spec.input_free_vars()
        Ninputs = len(input_vars)
        hard_consts = self.const_list
        Nconsts = len(hard_consts)
        #const_vars = []
        output_vars = self.spec.output_free_vars()
        op_out_vars = []
        op_in_vars = []
        tot_locs = Ninputs + Nconsts
        for op in self.op_list:
            assert isinstance(op, Comb)
            op_in_vars.append(op.input_free_vars())
            op_out_vars.append(op.output_free_vars())
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

        P_wfp = [And(P_in_range), And(P_loc_unique), And(P_multi_out), And(P_acyc)]


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
        #  Exists(L) Forall(V) P_wfp & (P_lib & P_conn) => P_spec
        query = And([
            And(P_wfp),
            fc.Implies(
                And([And(P_lib), And(P_conn)]),
                And(P_spec)
            )
        ])
        #in fc form
        self.query = query
    def external_loop_solve(self, logic=QF_BV, maxloops=1000, solver_name="z3"):
        assert maxloops > 0
        query = self.query.to_hwtypes()
        query = query.value
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
                print(f"{i}..", end='',flush=True)

                if not E_res:
                    print("UNSAT")
                    #No Solution (UNSAT)
                    return None
                else:
                    E_guess = {v: solver.get_value(v) for v in E_vars}
                    #print(E_guess)
                    query_guess = query.substitute(E_guess).simplify()
                    model = smt.get_model(smt.Not(query_guess), solver_name=solver_name, logic=logic)

                    if model is None:
                        #Solved!
                        print("SOLVED")
                        return self.comb_from_solved(E_guess)
                    else:
                        A_vals = {v: model.get_value(v) for v in A_vars}
                        solver.add_assertion(query.substitute(A_vals).simplify())
            raise ValueError(f"Unknown result in CEGIS in {maxloops} number of iterations")
    def comb_from_solved(self, lvals):

        inputs = self.spec.inputs
        outputs = self.spec.outputs


        input_vars, hard_consts, output_vars, op_out_vars, op_in_vars = self.vars
        input_lvars, hard_const_lvars, output_lvars, op_out_lvars, op_in_lvars = self.lvars

        #Fill in all the lvars
        def to_int(val:FNode):
            return int(val.constant_value())
        output_lvars = [to_int(lvals[lvar.value]) for lvar in output_lvars]
        def name_from_loc(loc):
            if loc < len(inputs):
                return f"i{loc}"
            elif loc < len(inputs) + len(hard_consts):
                #TODO Replace 13 with the actual type
                return BVConst(13, hard_consts[loc-len(inputs)])
            else:
                loc = loc - (len(inputs) + len(hard_consts))
                return f"t{loc}"


        tmp_map = {}
        for i in range(len(op_out_lvars)):
            op_out_lvars[i] = [to_int(lvals[lvar.value]) for lvar in op_out_lvars[i]]
            tmp_map[i] = op_out_lvars[i]
            op_in_lvars[i] = [to_int(lvals[lvar.value]) for lvar in op_in_lvars[i]]

        stmts = []
        for i, out_lvars in sorted(tmp_map.items(), key=lambda item: item[1][0]):
            lhss = [name_from_loc(loc) for loc in out_lvars]
            op = self.op_list[i]
            args = [name_from_loc(loc) for loc in op_in_lvars[i]]
            stmts.append(Stmt(lhss, op.name, args))
        outputs = [Var(name_from_loc(output_lvars[i]),v.type) for i, v in enumerate(self.spec.outputs)]
        name = QSym('solved', 'v0')
        comb = CombFun(name, inputs, outputs, stmts)
        comb.resolve_qualified_symbols(self.spec.module_list)
        return comb













