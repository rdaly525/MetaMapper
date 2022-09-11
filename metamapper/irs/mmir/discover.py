from .comb import QSym, Comb
from .synth import SynthQuery, verify
import typing as tp
import itertools as it


#Iterate overa ll possible combinations of the op list
def discover(spec: Comb, N: int, op_list: tp.List[QSym]):

    #THere has to be a more efficient soliution...
    cache = set()
    for indices in it.product(range(len(op_list)), repeat=N):
        k = frozenset(indices)
        if k in cache:
            continue


    for ops in somet        hing:
        sq = SynthQuery(spec, ops)
        combs = sq.gen_all_sols(maxloops=10000, verbose=True)
        for comb in combs:
            yield comb

