import magma
import coreir

def CoreIRContext(reset=False) -> coreir.Context:
    coreir_singleton = magma.backend.coreir_.CoreIRContextSingleton()
    if reset:
        coreir_singleton.reset_instance()
    return coreir_singleton.get_instance()

