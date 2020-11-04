module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module coreir_mul #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 * in1;
endmodule

module coreir_lshr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 >> in1;
endmodule

module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_ashr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = $signed(in0) >>> in1;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module corebit_or (
    input in0,
    input in1,
    output out
);
  assign out = in0 | in1;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module commonlib_muxn__N2__width32 (
    input [31:0] in_data [1:0],
    input [0:0] in_sel,
    output [31:0] out
);
wire [31:0] _join_out;
coreir_mux #(
    .width(32)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width16 (
    input [15:0] in_data [1:0],
    input [0:0] in_sel,
    output [15:0] out
);
wire [15:0] _join_out;
coreir_mux #(
    .width(16)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xUInt32 (
    input [31:0] I0,
    input [31:0] I1,
    input S,
    output [31:0] O
);
wire [31:0] coreir_commonlib_mux2x32_inst0_out;
wire [31:0] coreir_commonlib_mux2x32_inst0_in_data [1:0];
assign coreir_commonlib_mux2x32_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x32_inst0_in_data[0] = I0;
commonlib_muxn__N2__width32 coreir_commonlib_mux2x32_inst0 (
    .in_data(coreir_commonlib_mux2x32_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x32_inst0_out)
);
assign O = coreir_commonlib_mux2x32_inst0_out;
endmodule

module Mux2xUInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
wire [15:0] coreir_commonlib_mux2x16_inst0_out;
wire [15:0] coreir_commonlib_mux2x16_inst0_in_data [1:0];
assign coreir_commonlib_mux2x16_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x16_inst0_in_data[0] = I0;
commonlib_muxn__N2__width16 coreir_commonlib_mux2x16_inst0 (
    .in_data(coreir_commonlib_mux2x16_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x16_inst0_out)
);
assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module SHR_comb (
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
wire [15:0] Mux2xUInt16_inst0_O;
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [0:0] const_1_1_out;
wire [15:0] magma_Bits_16_ashr_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [15:0] magma_Bits_16_lshr_inst0_out;
wire magma_Bits_1_eq_inst0_out;
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(magma_Bits_16_lshr_inst0_out),
    .I1(magma_Bits_16_ashr_inst0_out),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xUInt16_inst0_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) const_0_16 (
    .out(const_0_16_out)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);
coreir_ashr #(
    .width(16)
) magma_Bits_16_ashr_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_ashr_inst0_out)
);
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(Mux2xUInt16_inst0_O),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_lshr #(
    .width(16)
) magma_Bits_16_lshr_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_lshr_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
assign O0 = Mux2xUInt16_inst0_O;
assign O1 = bit_const_0_None_out;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = Mux2xUInt16_inst0_O[15];
assign O4 = bit_const_0_None_out;
assign O5 = bit_const_0_None_out;
endmodule

module SHR (
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
wire [15:0] SHR_comb_inst0_O0;
wire SHR_comb_inst0_O1;
wire SHR_comb_inst0_O2;
wire SHR_comb_inst0_O3;
wire SHR_comb_inst0_O4;
wire SHR_comb_inst0_O5;
SHR_comb SHR_comb_inst0 (
    .signed_(signed_),
    .a(a),
    .b(b),
    .O0(SHR_comb_inst0_O0),
    .O1(SHR_comb_inst0_O1),
    .O2(SHR_comb_inst0_O2),
    .O3(SHR_comb_inst0_O3),
    .O4(SHR_comb_inst0_O4),
    .O5(SHR_comb_inst0_O5)
);
assign O0 = SHR_comb_inst0_O0;
assign O1 = SHR_comb_inst0_O1;
assign O2 = SHR_comb_inst0_O2;
assign O3 = SHR_comb_inst0_O3;
assign O4 = SHR_comb_inst0_O4;
assign O5 = SHR_comb_inst0_O5;
endmodule

module PE_comb (
    input [22:0] inst,
    input [31:0] inputs,
    input clk_en,
    input [15:0] self_modules_0_O,
    input [15:0] self_modules_1_O0,
    input self_modules_1_O1,
    input self_modules_1_O2,
    input self_modules_1_O3,
    input self_modules_1_O4,
    input self_modules_1_O5,
    input [15:0] self_modules_2_O0,
    input self_modules_2_O1,
    input self_modules_2_O2,
    input self_modules_2_O3,
    input self_modules_2_O4,
    input self_modules_2_O5,
    output [0:0] O0,
    output [0:0] O1,
    output [15:0] O2,
    output [15:0] O3,
    output [15:0] O4,
    output [15:0] O5,
    output [0:0] O6,
    output [15:0] O7,
    output [15:0] O8,
    output [15:0] O9
);
wire [15:0] Mux2xUInt16_inst0_O;
wire [15:0] Mux2xUInt16_inst1_O;
wire [15:0] Mux2xUInt16_inst2_O;
wire [15:0] Mux2xUInt16_inst3_O;
wire [15:0] Mux2xUInt16_inst4_O;
wire [15:0] Mux2xUInt16_inst5_O;
wire [15:0] Mux2xUInt16_inst6_O;
wire [15:0] Mux2xUInt16_inst7_O;
wire [0:0] const_0_1_out;
wire [1:0] const_0_2_out;
wire [0:0] const_1_1_out;
wire [1:0] const_1_2_out;
wire [1:0] const_2_2_out;
wire [1:0] const_3_2_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire magma_Bits_1_eq_inst3_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst2_out;
wire magma_Bits_2_eq_inst3_out;
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(inst[16:1]),
    .I1(inst[16:1]),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xUInt16_inst0_O)
);
Mux2xUInt16 Mux2xUInt16_inst1 (
    .I0(Mux2xUInt16_inst0_O),
    .I1(inputs[31:16]),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xUInt16_inst1_O)
);
Mux2xUInt16 Mux2xUInt16_inst2 (
    .I0(self_modules_0_O),
    .I1(self_modules_0_O),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xUInt16_inst2_O)
);
Mux2xUInt16 Mux2xUInt16_inst3 (
    .I0(Mux2xUInt16_inst2_O),
    .I1(inputs[15:0]),
    .S(magma_Bits_1_eq_inst3_out),
    .O(Mux2xUInt16_inst3_O)
);
Mux2xUInt16 Mux2xUInt16_inst4 (
    .I0(self_modules_2_O0),
    .I1(self_modules_2_O0),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xUInt16_inst4_O)
);
Mux2xUInt16 Mux2xUInt16_inst5 (
    .I0(Mux2xUInt16_inst4_O),
    .I1(self_modules_1_O0),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xUInt16_inst5_O)
);
Mux2xUInt16 Mux2xUInt16_inst6 (
    .I0(Mux2xUInt16_inst5_O),
    .I1(self_modules_0_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xUInt16_inst6_O)
);
Mux2xUInt16 Mux2xUInt16_inst7 (
    .I0(Mux2xUInt16_inst6_O),
    .I1(inst[16:1]),
    .S(magma_Bits_2_eq_inst3_out),
    .O(Mux2xUInt16_inst7_O)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) const_0_1 (
    .out(const_0_1_out)
);
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);
coreir_const #(
    .value(2'h1),
    .width(2)
) const_1_2 (
    .out(const_1_2_out)
);
coreir_const #(
    .value(2'h2),
    .width(2)
) const_2_2 (
    .out(const_2_2_out)
);
coreir_const #(
    .value(2'h3),
    .width(2)
) const_3_2 (
    .out(const_3_2_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(inst[18]),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst1 (
    .in0(inst[18]),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst1_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst2 (
    .in0(inst[17]),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst2_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst3 (
    .in0(inst[17]),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst3_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(inst[20:19]),
    .in1(const_0_2_out),
    .out(magma_Bits_2_eq_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst1 (
    .in0(inst[20:19]),
    .in1(const_1_2_out),
    .out(magma_Bits_2_eq_inst1_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst2 (
    .in0(inst[20:19]),
    .in1(const_2_2_out),
    .out(magma_Bits_2_eq_inst2_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst3 (
    .in0(inst[20:19]),
    .in1(const_3_2_out),
    .out(magma_Bits_2_eq_inst3_out)
);
assign O0 = inst[0];
assign O1 = inst[21];
assign O2 = inputs[15:0];
assign O3 = Mux2xUInt16_inst1_O;
assign O4 = Mux2xUInt16_inst3_O;
assign O5 = inputs[31:16];
assign O6 = inst[22];
assign O7 = inputs[31:16];
assign O8 = inputs[15:0];
assign O9 = Mux2xUInt16_inst7_O;
endmodule

module MUL_comb (
    input [0:0] instr,
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    output [15:0] O
);
wire [15:0] Mux2xUInt16_inst0_O;
wire [31:0] Mux2xUInt32_inst0_O;
wire [31:0] Mux2xUInt32_inst1_O;
wire bit_const_0_None_out;
wire [0:0] const_0_1_out;
wire [0:0] const_1_1_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire [31:0] magma_Bits_32_mul_inst0_out;
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(magma_Bits_32_mul_inst0_out[31:16]),
    .I1(magma_Bits_32_mul_inst0_out[15:0]),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xUInt16_inst0_O)
);
wire [31:0] Mux2xUInt32_inst0_I0;
assign Mux2xUInt32_inst0_I0 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,a[15:0]};
wire [31:0] Mux2xUInt32_inst0_I1;
assign Mux2xUInt32_inst0_I1 = {a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15:0]};
Mux2xUInt32 Mux2xUInt32_inst0 (
    .I0(Mux2xUInt32_inst0_I0),
    .I1(Mux2xUInt32_inst0_I1),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xUInt32_inst0_O)
);
wire [31:0] Mux2xUInt32_inst1_I0;
assign Mux2xUInt32_inst1_I0 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,b[15:0]};
wire [31:0] Mux2xUInt32_inst1_I1;
assign Mux2xUInt32_inst1_I1 = {b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15:0]};
Mux2xUInt32 Mux2xUInt32_inst1 (
    .I0(Mux2xUInt32_inst1_I0),
    .I1(Mux2xUInt32_inst1_I1),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xUInt32_inst1_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) const_0_1 (
    .out(const_0_1_out)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst1 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst1_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst2 (
    .in0(instr),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst2_out)
);
coreir_mul #(
    .width(32)
) magma_Bits_32_mul_inst0 (
    .in0(Mux2xUInt32_inst0_O),
    .in1(Mux2xUInt32_inst1_O),
    .out(magma_Bits_32_mul_inst0_out)
);
assign O = Mux2xUInt16_inst0_O;
endmodule

module MUL (
    input [0:0] instr,
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
wire [15:0] MUL_comb_inst0_O;
MUL_comb MUL_comb_inst0 (
    .instr(instr),
    .signed_(signed_),
    .a(a),
    .b(b),
    .O(MUL_comb_inst0_O)
);
assign O = MUL_comb_inst0_O;
endmodule

module ADD_comb (
    input [15:0] a,
    input [15:0] b,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [16:0] const_0_17_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_or_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [16:0] magma_Bits_17_add_inst0_out;
wire [16:0] magma_Bits_17_add_inst1_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) const_0_16 (
    .out(const_0_16_out)
);
coreir_const #(
    .value(17'h00000),
    .width(17)
) const_0_17 (
    .out(const_0_17_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(a[15]),
    .in1(b[15]),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_and_inst0_out),
    .in1(magma_Bit_not_inst0_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_not_inst1_out),
    .in1(magma_Bit_not_inst2_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_and magma_Bit_and_inst3 (
    .in0(magma_Bit_and_inst2_out),
    .in1(magma_Bits_17_add_inst1_out[15]),
    .out(magma_Bit_and_inst3_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bits_17_add_inst1_out[15]),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(a[15]),
    .out(magma_Bit_not_inst1_out)
);
corebit_not magma_Bit_not_inst2 (
    .in(b[15]),
    .out(magma_Bit_not_inst2_out)
);
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bit_and_inst1_out),
    .in1(magma_Bit_and_inst3_out),
    .out(magma_Bit_or_inst0_out)
);
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(magma_Bits_17_add_inst1_out[15:0]),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
wire [16:0] magma_Bits_17_add_inst0_in0;
assign magma_Bits_17_add_inst0_in0 = {bit_const_0_None_out,a[15:0]};
wire [16:0] magma_Bits_17_add_inst0_in1;
assign magma_Bits_17_add_inst0_in1 = {bit_const_0_None_out,b[15:0]};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst0 (
    .in0(magma_Bits_17_add_inst0_in0),
    .in1(magma_Bits_17_add_inst0_in1),
    .out(magma_Bits_17_add_inst0_out)
);
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst1 (
    .in0(magma_Bits_17_add_inst0_out),
    .in1(const_0_17_out),
    .out(magma_Bits_17_add_inst1_out)
);
assign O0 = magma_Bits_17_add_inst1_out[15:0];
assign O1 = magma_Bits_17_add_inst1_out[16];
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = magma_Bits_17_add_inst1_out[15];
assign O4 = magma_Bits_17_add_inst1_out[16];
assign O5 = magma_Bit_or_inst0_out;
endmodule

module ADD (
    input [15:0] a,
    input [15:0] b,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
wire [15:0] ADD_comb_inst0_O0;
wire ADD_comb_inst0_O1;
wire ADD_comb_inst0_O2;
wire ADD_comb_inst0_O3;
wire ADD_comb_inst0_O4;
wire ADD_comb_inst0_O5;
ADD_comb ADD_comb_inst0 (
    .a(a),
    .b(b),
    .O0(ADD_comb_inst0_O0),
    .O1(ADD_comb_inst0_O1),
    .O2(ADD_comb_inst0_O2),
    .O3(ADD_comb_inst0_O3),
    .O4(ADD_comb_inst0_O4),
    .O5(ADD_comb_inst0_O5)
);
assign O0 = ADD_comb_inst0_O0;
assign O1 = ADD_comb_inst0_O1;
assign O2 = ADD_comb_inst0_O2;
assign O3 = ADD_comb_inst0_O3;
assign O4 = ADD_comb_inst0_O4;
assign O5 = ADD_comb_inst0_O5;
endmodule

module PE (
    input [22:0] inst,
    input [31:0] inputs,
    input clk_en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
wire [15:0] ADD_inst0_O0;
wire ADD_inst0_O1;
wire ADD_inst0_O2;
wire ADD_inst0_O3;
wire ADD_inst0_O4;
wire ADD_inst0_O5;
wire [15:0] MUL_inst0_O;
wire [0:0] PE_comb_inst0_O0;
wire [0:0] PE_comb_inst0_O1;
wire [15:0] PE_comb_inst0_O2;
wire [15:0] PE_comb_inst0_O3;
wire [15:0] PE_comb_inst0_O4;
wire [15:0] PE_comb_inst0_O5;
wire [0:0] PE_comb_inst0_O6;
wire [15:0] PE_comb_inst0_O7;
wire [15:0] PE_comb_inst0_O8;
wire [15:0] PE_comb_inst0_O9;
wire [15:0] SHR_inst0_O0;
wire SHR_inst0_O1;
wire SHR_inst0_O2;
wire SHR_inst0_O3;
wire SHR_inst0_O4;
wire SHR_inst0_O5;
ADD ADD_inst0 (
    .a(PE_comb_inst0_O4),
    .b(PE_comb_inst0_O5),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(ADD_inst0_O0),
    .O1(ADD_inst0_O1),
    .O2(ADD_inst0_O2),
    .O3(ADD_inst0_O3),
    .O4(ADD_inst0_O4),
    .O5(ADD_inst0_O5)
);
MUL MUL_inst0 (
    .instr(PE_comb_inst0_O0),
    .signed_(PE_comb_inst0_O1),
    .a(PE_comb_inst0_O2),
    .b(PE_comb_inst0_O3),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(MUL_inst0_O)
);
PE_comb PE_comb_inst0 (
    .inst(inst),
    .inputs(inputs),
    .clk_en(clk_en),
    .self_modules_0_O(MUL_inst0_O),
    .self_modules_1_O0(ADD_inst0_O0),
    .self_modules_1_O1(ADD_inst0_O1),
    .self_modules_1_O2(ADD_inst0_O2),
    .self_modules_1_O3(ADD_inst0_O3),
    .self_modules_1_O4(ADD_inst0_O4),
    .self_modules_1_O5(ADD_inst0_O5),
    .self_modules_2_O0(SHR_inst0_O0),
    .self_modules_2_O1(SHR_inst0_O1),
    .self_modules_2_O2(SHR_inst0_O2),
    .self_modules_2_O3(SHR_inst0_O3),
    .self_modules_2_O4(SHR_inst0_O4),
    .self_modules_2_O5(SHR_inst0_O5),
    .O0(PE_comb_inst0_O0),
    .O1(PE_comb_inst0_O1),
    .O2(PE_comb_inst0_O2),
    .O3(PE_comb_inst0_O3),
    .O4(PE_comb_inst0_O4),
    .O5(PE_comb_inst0_O5),
    .O6(PE_comb_inst0_O6),
    .O7(PE_comb_inst0_O7),
    .O8(PE_comb_inst0_O8),
    .O9(PE_comb_inst0_O9)
);
SHR SHR_inst0 (
    .signed_(PE_comb_inst0_O6),
    .a(PE_comb_inst0_O7),
    .b(PE_comb_inst0_O8),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(SHR_inst0_O0),
    .O1(SHR_inst0_O1),
    .O2(SHR_inst0_O2),
    .O3(SHR_inst0_O3),
    .O4(SHR_inst0_O4),
    .O5(SHR_inst0_O5)
);
assign O = PE_comb_inst0_O9;
endmodule

