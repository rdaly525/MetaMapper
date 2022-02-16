from lassen import PE_fc as lassen_fc
from metamapper import peak_util as putil, CoreIRContext
from metamapper import coreir_util as cutil

#Compiles
def compile_PE_spec(arch_fc: "peak_fc", header_file: str, def_file: str):
    cmod = putil.peak_to_coreir(arch_fc)

    output_t = arch_fc.Py.output_t
    for i, field in enumerate(output_t.field_dict):
        print(i, field, type(field))

    c = CoreIRContext()
    c.serialize_header(header_file, [cmod])
    #c.serialize_definitions(def_file, [cmod])


lassen_header = "./libs/lassen_header.json"
lassen_def = "./libs/lassen_def.json"

if __name__ == "__main__":
    compile_PE_spec(lassen_fc, lassen_header, lassen_def)
