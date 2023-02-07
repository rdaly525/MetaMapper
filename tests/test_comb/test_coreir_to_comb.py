import metamapper.coreir_util as cutil
from metamapper import CoreIRContext
from metamapper.comb_utils import coreir_to_comb
import pytest
from comb.ir import CombProgram, Obj

from metamapper.comb_utils.loader import coreir_to_obj

examples_coreir = [
    #"add4",
    "add3_const_flat",
]

examples_kernels = [
    "gaussian_flat",
]

@pytest.mark.parametrize("name", examples_coreir)
def test_coreir_to_comb(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/coreir/{name}.json"
    cmod = cutil.load_from_json(file_name)
    comb_fun = coreir_to_comb(cmod)
    assert isinstance(comb_fun, CombProgram)
    print(comb_fun)

@pytest.mark.parametrize("name", examples_kernels)
def test_coreir_to_obj(name):
    c = CoreIRContext(reset=True)
    file_name = f"examples/kernels/{name}.json"
    obj: Obj = coreir_to_obj(file_name)
    assert isinstance(obj, Obj)
    print(obj)

