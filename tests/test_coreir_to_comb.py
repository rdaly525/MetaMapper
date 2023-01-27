import metamapper.coreir_util as cutil
from metamapper import CoreIRContext
from metamapper.comb_utils import coreir_to_comb
import pytest
from comb.ir import CombProgram

examples_coreir = [
    "add2",
]

@pytest.mark.parametrize("name", examples_coreir)
def test_coreir_to_comb(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{name}.json"
    cmod = cutil.load_from_json(file_name)
    comb_fun = coreir_to_comb(cmod)
    assert isinstance(comb_fun, CombProgram)

