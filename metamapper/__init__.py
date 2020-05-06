import magma
import coreir

def CoreIRContext(reset=False) -> coreir.Context:
    if reset:
        magma.frontend.coreir_.ResetCoreIR()
    return magma.backend.coreir_.CoreIRContextSingleton().get_instance()

