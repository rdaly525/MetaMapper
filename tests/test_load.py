import coreir
from metamapper import coreir_module_to_dag
from metamapper.common_passes import AddID, Printer

def test_load_add():
    c = coreir.Context()
    mod = c.load_from_file("examples/add4.json")
    expr = coreir_module_to_dag(mod)
    assert len(expr.inputs) == 4
    for i in range(4):
        assert expr.inputs[i].port_name == f"in{i}"
    assert len(expr.outputs) == 1
    assert expr.outputs[0].port_name == "out"

    AddID(expr)
    Printer(expr)
