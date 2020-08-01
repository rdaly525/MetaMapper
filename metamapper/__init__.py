import magma
import coreir

import DagVisitor

def CoreIRContext(reset=False) -> coreir.Context:
    if reset:
        magma.frontend.coreir_.ResetCoreIR()
    c = magma.backend.coreir_.CoreIRContextSingleton().get_instance()
    if reset:
        c.load_library("commonlib")
    return c

