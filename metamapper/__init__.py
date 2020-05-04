import magma

def CoreIRContext():
    return magma.backend.coreir_.CoreIRContextSingleton().get_instance()

