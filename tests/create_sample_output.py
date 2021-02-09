from examples.alu import gen_ALU, Inst_fc
from metamapper.peak_loader import load_from_peak
from metamapper.node import Nodes
import magma as m

ArchNodes = Nodes("Arch")
ALU_fc = gen_ALU(16)
load_from_peak(ArchNodes, ALU_fc)
Alu_m = ArchNodes.modules["ALU"]

def doit(io):
    add00 = Alu_m(name="add00")
    add01 = Alu_m(name="add01")
    add1 = Alu_m(name="add1")
    add00.ASYNCRESET @= io.RESET
    add01.ASYNCRESET @= io.RESET
    add1.ASYNCRESET @= io.RESET
    add00.inst @= 2
    add01.inst @= 2
    add1.inst @= 2
    add1.inst @= 2
    m.wire(io.in0, add00.a)
    m.wire(io.in1, add00.b)
    m.wire(io.in2, add01.a)
    m.wire(io.in3, add01.b)
    m.wire(add00.O, add1.a)
    m.wire(add01.O, add1.b)
    m.wire(add1.O, io.out)

class Add4(m.Circuit):
    io = m.IO(
        in0=m.In(m.Bits[16]),
        in1=m.In(m.Bits[16]),
        in2=m.In(m.Bits[16]),
        in3=m.In(m.Bits[16]),
        out=m.Out(m.Bits[16]),
    ) + m.ClockIO(has_reset=True)
    doit(io)


# Create a fresh context for second compilation.
m.compile("add4_mapped", Add4, output="coreir")

