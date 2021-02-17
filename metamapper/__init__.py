import magma
import coreir

_cache = None
def CoreIRContext(reset=False) -> coreir.Context:
    global _cache
    if not reset and _cache is not None:
        return _cache
    if reset:
        magma.frontend.coreir_.ResetCoreIR()
    c = magma.backend.coreir.coreir_runtime.coreir_context()
    if reset:
        c.load_library("commonlib")
        _cache = c
    return c

