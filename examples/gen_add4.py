import coreir

def gen_add4(file):
    c = coreir.Context()
    BV16_Out = c.Array(16,c.Bit())
    BV16_In = c.Flip(BV16_Out)
    mtype = c.Record(dict(
        in0=BV16_In,
        in1=BV16_In,
        in2=BV16_In,
        in3=BV16_In,
        out=BV16_Out
    ))
    Add4 = c.global_namespace.new_module("Add4", mtype)
    md = Add4.new_definition()
    io = md.interface
    add16 = c.get_namespace("coreir").generators["add"](width=16)
    a00 = md.add_module_instance("a00", add16)
    a01 = md.add_module_instance("a01", add16)
    a1 = md.add_module_instance("a1", add16)
    md.connect(io.select("in0"),a00.select("in0"))
    md.connect(io.select("in1"),a00.select("in1"))
    md.connect(io.select("in2"),a01.select("in0"))
    md.connect(io.select("in3"),a01.select("in1"))
    md.connect(a00.select("out"),a1.select("in0"))
    md.connect(a01.select("out"),a1.select("in1"))
    md.connect(a1.select("out"), io.select("out"))
    Add4.definition = md
    Add4.print_()
    Add4.save_to_file(file)

gen_add4("/Users/rdaly/Metamapper/examples/Add4.json")
