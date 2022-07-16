import peak.mapper.formula_constructor as fc
import hwtypes as ht



def synth(p, const_list=[0,1,-1],const_synth=0):
    # Structure
    input_vars = []
    hard_consts = []
    const_vars = []
    output_vars = []
    op_out_vars = [[]]
    op_in_vars = [[]]

    tstart = len(input_vars) + len(hard_consts) + len(const_vars)


    #These can be hardcoded
    input_lvars = []
    hard_const_lvars = []
    const_lvars = []
    output_lvars = []

    #These need to be solved for
    op_out_lvars = [[]]
    op_in_lvars = [[]]

    #Formal Spec (P_spec)
    P_spec = []
    for (i, ov) in enumerate(p.spec(*input_vars)):
        P_spec.append(output_vars[i] == ov)

    #Lib Spec (P_lib)
    #   temp_var[i] = OP(*op_in_vars[i])
    P_lib = []
    for i, op in enumerate(p.ops):
        ovars = op(*op_in_vars[i])
        for j, op_out_var in enumerate(ovars):
            P_lib.append(op_out_vars[i][j] == op_out_var)

    #Well formed program (P_wfp)
    # Temp locs are in range(NI, NI + Nops)
    # Temp locs are unique
    # ACYC Constraint
    #  op_out_lvars[i] > op_in_lvars[i]
    #
    P_wfp = []


    #Locations correspond to vars (P_conn)
    # (Lx == Ly) => (X==Y)
    P_conn = []



    #Final query:
    #  Exists(L) Forall(V) P_wfp & (P_lib & P_conn) => P_spec
    And = fc.And
    query = And([
        And(P_wfp),
        fc.Implies(
            And([And(P_lib), And(P_conn)]),
            And(P_spec),
        )
    ])
    return query



