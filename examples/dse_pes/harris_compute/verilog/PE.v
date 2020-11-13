module coreir_ule #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 <= in1;
endmodule

module coreir_uge #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 >= in1;
endmodule

module coreir_sle #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = $signed(in0) <= $signed(in1);
endmodule

module coreir_sge #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = $signed(in0) >= $signed(in1);
endmodule

module coreir_not #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = ~in;
endmodule

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

module coreir_and #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 & in1;
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

module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
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

module commonlib_muxn__N2__width1 (
    input [0:0] in_data [1:0],
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module SUB_comb (
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
wire [16:0] const_1_17_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_or_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [15:0] magma_Bits_16_not_inst0_out;
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
    .value(17'h00001),
    .width(17)
) const_1_17 (
    .out(const_1_17_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(a[15]),
    .in1(magma_Bits_16_not_inst0_out[15]),
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
    .in(magma_Bits_16_not_inst0_out[15]),
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
coreir_not #(
    .width(16)
) magma_Bits_16_not_inst0 (
    .in(b),
    .out(magma_Bits_16_not_inst0_out)
);
wire [16:0] magma_Bits_17_add_inst0_in0;
assign magma_Bits_17_add_inst0_in0 = {bit_const_0_None_out,a[15:0]};
wire [16:0] magma_Bits_17_add_inst0_in1;
assign magma_Bits_17_add_inst0_in1 = {bit_const_0_None_out,magma_Bits_16_not_inst0_out[15:0]};
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
    .in1(const_1_17_out),
    .out(magma_Bits_17_add_inst1_out)
);
assign O0 = magma_Bits_17_add_inst1_out[15:0];
assign O1 = magma_Bits_17_add_inst1_out[16];
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = magma_Bits_17_add_inst1_out[15];
assign O4 = magma_Bits_17_add_inst1_out[16];
assign O5 = magma_Bit_or_inst0_out;
endmodule

module SUB (
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
wire [15:0] SUB_comb_inst0_O0;
wire SUB_comb_inst0_O1;
wire SUB_comb_inst0_O2;
wire SUB_comb_inst0_O3;
wire SUB_comb_inst0_O4;
wire SUB_comb_inst0_O5;
SUB_comb SUB_comb_inst0 (
    .a(a),
    .b(b),
    .O0(SUB_comb_inst0_O0),
    .O1(SUB_comb_inst0_O1),
    .O2(SUB_comb_inst0_O2),
    .O3(SUB_comb_inst0_O3),
    .O4(SUB_comb_inst0_O4),
    .O5(SUB_comb_inst0_O5)
);
assign O0 = SUB_comb_inst0_O0;
assign O1 = SUB_comb_inst0_O1;
assign O2 = SUB_comb_inst0_O2;
assign O3 = SUB_comb_inst0_O3;
assign O4 = SUB_comb_inst0_O4;
assign O5 = SUB_comb_inst0_O5;
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

module Mux2xOutUInt16 (
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

module Mux_comb (
    input [15:0] a,
    input [15:0] b,
    input sel,
    output [15:0] O
);
wire [15:0] Mux2xOutUInt16_inst0_O;
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(a),
    .I1(b),
    .S(sel),
    .O(Mux2xOutUInt16_inst0_O)
);
assign O = Mux2xOutUInt16_inst0_O;
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
assign coreir_commonlib_mux2x1_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x1_inst0_in_data[0] = I0;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module PE_comb (
    input [49:0] inst,
    input [50:0] inputs,
    input clk_en,
    input [15:0] self_modules_0_O0,
    input self_modules_0_O1,
    input self_modules_0_O2,
    input self_modules_0_O3,
    input self_modules_0_O4,
    input self_modules_0_O5,
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
    input self_cond_2_O,
    input [15:0] self_modules_3_O0,
    input self_modules_3_O1,
    input self_modules_3_O2,
    input self_modules_3_O3,
    input self_modules_3_O4,
    input self_modules_3_O5,
    input self_cond_3_O,
    input [15:0] self_modules_4_O,
    input self_modules_5_O,
    input [15:0] self_modules_6_O0,
    input self_modules_6_O1,
    input self_modules_6_O2,
    input self_modules_6_O3,
    input self_modules_6_O4,
    input self_modules_6_O5,
    input self_cond_6_O,
    input [15:0] self_modules_7_O,
    input [15:0] self_modules_8_O0,
    input self_modules_8_O1,
    input self_modules_8_O2,
    input self_modules_8_O3,
    input self_modules_8_O4,
    input self_modules_8_O5,
    output [15:0] O0,
    output [15:0] O1,
    output [15:0] O2,
    output [15:0] O3,
    output [0:0] O4,
    output [15:0] O5,
    output [15:0] O6,
    output [4:0] O7,
    output O8,
    output O9,
    output O10,
    output O11,
    output O12,
    output [0:0] O13,
    output [15:0] O14,
    output [15:0] O15,
    output [4:0] O16,
    output O17,
    output O18,
    output O19,
    output O20,
    output O21,
    output [0:0] O22,
    output [0:0] O23,
    output [15:0] O24,
    output [15:0] O25,
    output [7:0] O26,
    output O27,
    output O28,
    output O29,
    output [15:0] O30,
    output [15:0] O31,
    output [4:0] O32,
    output O33,
    output O34,
    output O35,
    output O36,
    output O37,
    output [15:0] O38,
    output [15:0] O39,
    output O40,
    output [0:0] O41,
    output [15:0] O42,
    output [15:0] O43,
    output [16:0] O44
);
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst2_O;
wire [15:0] Mux2xUInt16_inst0_O;
wire [15:0] Mux2xUInt16_inst1_O;
wire [15:0] Mux2xUInt16_inst2_O;
wire [15:0] Mux2xUInt16_inst3_O;
wire [15:0] Mux2xUInt16_inst4_O;
wire [15:0] Mux2xUInt16_inst5_O;
wire [15:0] Mux2xUInt16_inst6_O;
wire [15:0] Mux2xUInt16_inst7_O;
wire [15:0] Mux2xUInt16_inst8_O;
wire [1:0] const_0_2_out;
wire [3:0] const_0_4_out;
wire [1:0] const_1_2_out;
wire [3:0] const_1_4_out;
wire [1:0] const_2_2_out;
wire [3:0] const_2_4_out;
wire [3:0] const_3_4_out;
wire [3:0] const_4_4_out;
wire [3:0] const_5_4_out;
wire [3:0] const_6_4_out;
wire [3:0] const_7_4_out;
wire [3:0] const_8_4_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst2_out;
wire magma_Bits_4_eq_inst0_out;
wire magma_Bits_4_eq_inst1_out;
wire magma_Bits_4_eq_inst2_out;
wire magma_Bits_4_eq_inst3_out;
wire magma_Bits_4_eq_inst4_out;
wire magma_Bits_4_eq_inst5_out;
wire magma_Bits_4_eq_inst6_out;
wire magma_Bits_4_eq_inst7_out;
wire magma_Bits_4_eq_inst8_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(self_modules_5_O),
    .I1(self_modules_5_O),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(Mux2xBit_inst0_O),
    .I1(self_cond_6_O),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(Mux2xBit_inst1_O),
    .I1(self_cond_3_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(self_modules_6_O0),
    .I1(self_modules_6_O0),
    .S(magma_Bits_4_eq_inst0_out),
    .O(Mux2xUInt16_inst0_O)
);
Mux2xUInt16 Mux2xUInt16_inst1 (
    .I0(Mux2xUInt16_inst0_O),
    .I1(self_modules_8_O0),
    .S(magma_Bits_4_eq_inst1_out),
    .O(Mux2xUInt16_inst1_O)
);
Mux2xUInt16 Mux2xUInt16_inst2 (
    .I0(Mux2xUInt16_inst1_O),
    .I1(self_modules_1_O0),
    .S(magma_Bits_4_eq_inst2_out),
    .O(Mux2xUInt16_inst2_O)
);
Mux2xUInt16 Mux2xUInt16_inst3 (
    .I0(Mux2xUInt16_inst2_O),
    .I1(self_modules_4_O),
    .S(magma_Bits_4_eq_inst3_out),
    .O(Mux2xUInt16_inst3_O)
);
Mux2xUInt16 Mux2xUInt16_inst4 (
    .I0(Mux2xUInt16_inst3_O),
    .I1(self_modules_7_O),
    .S(magma_Bits_4_eq_inst4_out),
    .O(Mux2xUInt16_inst4_O)
);
Mux2xUInt16 Mux2xUInt16_inst5 (
    .I0(Mux2xUInt16_inst4_O),
    .I1(self_modules_3_O0),
    .S(magma_Bits_4_eq_inst5_out),
    .O(Mux2xUInt16_inst5_O)
);
Mux2xUInt16 Mux2xUInt16_inst6 (
    .I0(Mux2xUInt16_inst5_O),
    .I1(self_modules_2_O0),
    .S(magma_Bits_4_eq_inst6_out),
    .O(Mux2xUInt16_inst6_O)
);
Mux2xUInt16 Mux2xUInt16_inst7 (
    .I0(Mux2xUInt16_inst6_O),
    .I1(self_modules_0_O0),
    .S(magma_Bits_4_eq_inst7_out),
    .O(Mux2xUInt16_inst7_O)
);
Mux2xUInt16 Mux2xUInt16_inst8 (
    .I0(Mux2xUInt16_inst7_O),
    .I1(inst[31:16]),
    .S(magma_Bits_4_eq_inst8_out),
    .O(Mux2xUInt16_inst8_O)
);
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_const #(
    .value(4'h0),
    .width(4)
) const_0_4 (
    .out(const_0_4_out)
);
coreir_const #(
    .value(2'h1),
    .width(2)
) const_1_2 (
    .out(const_1_2_out)
);
coreir_const #(
    .value(4'h1),
    .width(4)
) const_1_4 (
    .out(const_1_4_out)
);
coreir_const #(
    .value(2'h2),
    .width(2)
) const_2_2 (
    .out(const_2_2_out)
);
coreir_const #(
    .value(4'h2),
    .width(4)
) const_2_4 (
    .out(const_2_4_out)
);
coreir_const #(
    .value(4'h3),
    .width(4)
) const_3_4 (
    .out(const_3_4_out)
);
coreir_const #(
    .value(4'h4),
    .width(4)
) const_4_4 (
    .out(const_4_4_out)
);
coreir_const #(
    .value(4'h5),
    .width(4)
) const_5_4 (
    .out(const_5_4_out)
);
coreir_const #(
    .value(4'h6),
    .width(4)
) const_6_4 (
    .out(const_6_4_out)
);
coreir_const #(
    .value(4'h7),
    .width(4)
) const_7_4 (
    .out(const_7_4_out)
);
coreir_const #(
    .value(4'h8),
    .width(4)
) const_8_4 (
    .out(const_8_4_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(inst[37:36]),
    .in1(const_0_2_out),
    .out(magma_Bits_2_eq_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst1 (
    .in0(inst[37:36]),
    .in1(const_1_2_out),
    .out(magma_Bits_2_eq_inst1_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst2 (
    .in0(inst[37:36]),
    .in1(const_2_2_out),
    .out(magma_Bits_2_eq_inst2_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst0 (
    .in0(inst[35:32]),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst0_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst1 (
    .in0(inst[35:32]),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst1_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst2 (
    .in0(inst[35:32]),
    .in1(const_2_4_out),
    .out(magma_Bits_4_eq_inst2_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst3 (
    .in0(inst[35:32]),
    .in1(const_3_4_out),
    .out(magma_Bits_4_eq_inst3_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst4 (
    .in0(inst[35:32]),
    .in1(const_4_4_out),
    .out(magma_Bits_4_eq_inst4_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst5 (
    .in0(inst[35:32]),
    .in1(const_5_4_out),
    .out(magma_Bits_4_eq_inst5_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst6 (
    .in0(inst[35:32]),
    .in1(const_6_4_out),
    .out(magma_Bits_4_eq_inst6_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst7 (
    .in0(inst[35:32]),
    .in1(const_7_4_out),
    .out(magma_Bits_4_eq_inst7_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst8 (
    .in0(inst[35:32]),
    .in1(const_8_4_out),
    .out(magma_Bits_4_eq_inst8_out)
);
assign O0 = inputs[15:0];
assign O1 = inputs[31:16];
assign O2 = inputs[47:32];
assign O3 = self_modules_0_O0;
assign O4 = inst[38];
assign O5 = inputs[47:32];
assign O6 = inputs[31:16];
assign O7 = inst[4:0];
assign O8 = self_modules_2_O1;
assign O9 = self_modules_2_O2;
assign O10 = self_modules_2_O3;
assign O11 = self_modules_2_O4;
assign O12 = self_modules_2_O5;
assign O13 = inst[39];
assign O14 = inputs[47:32];
assign O15 = inputs[31:16];
assign O16 = inst[9:5];
assign O17 = self_modules_3_O1;
assign O18 = self_modules_3_O2;
assign O19 = self_modules_3_O3;
assign O20 = self_modules_3_O4;
assign O21 = self_modules_3_O5;
assign O22 = inst[15];
assign O23 = inst[40];
assign O24 = inputs[47:32];
assign O25 = inputs[31:16];
assign O26 = inst[49:42];
assign O27 = inputs[48];
assign O28 = inputs[49];
assign O29 = inputs[50];
assign O30 = inputs[47:32];
assign O31 = inputs[31:16];
assign O32 = inst[14:10];
assign O33 = self_modules_6_O1;
assign O34 = self_modules_6_O2;
assign O35 = self_modules_6_O3;
assign O36 = self_modules_6_O4;
assign O37 = self_modules_6_O5;
assign O38 = inputs[47:32];
assign O39 = inputs[15:0];
assign O40 = inputs[48];
assign O41 = inst[41];
assign O42 = inputs[47:32];
assign O43 = inputs[31:16];
assign O44 = {Mux2xBit_inst2_O,Mux2xUInt16_inst8_O[15:0]};
endmodule

module Mux (
    input [15:0] a,
    input [15:0] b,
    input sel,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
wire [15:0] Mux_comb_inst0_O;
Mux_comb Mux_comb_inst0 (
    .a(a),
    .b(b),
    .sel(sel),
    .O(Mux_comb_inst0_O)
);
assign O = Mux_comb_inst0_O;
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

module LUT_comb (
    input [7:0] lut,
    input bit0,
    input bit1,
    input bit2,
    output O
);
wire bit_const_0_None_out;
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_and_inst0_out;
wire [7:0] magma_Bits_8_lshr_inst0_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_and #(
    .width(8)
) magma_Bits_8_and_inst0 (
    .in0(magma_Bits_8_lshr_inst0_out),
    .in1(const_1_8_out),
    .out(magma_Bits_8_and_inst0_out)
);
wire [7:0] magma_Bits_8_lshr_inst0_in1;
assign magma_Bits_8_lshr_inst0_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit2,bit1,bit0};
coreir_lshr #(
    .width(8)
) magma_Bits_8_lshr_inst0 (
    .in0(lut),
    .in1(magma_Bits_8_lshr_inst0_in1),
    .out(magma_Bits_8_lshr_inst0_out)
);
assign O = magma_Bits_8_and_inst0_out[0];
endmodule

module LUT (
    input [7:0] lut,
    input bit0,
    input bit1,
    input bit2,
    input CLK,
    input ASYNCRESET,
    output O
);
wire LUT_comb_inst0_O;
LUT_comb LUT_comb_inst0 (
    .lut(lut),
    .bit0(bit0),
    .bit1(bit1),
    .bit2(bit2),
    .O(LUT_comb_inst0_O)
);
assign O = LUT_comb_inst0_O;
endmodule

module LTE_comb (
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
wire Mux2xBit_inst0_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [0:0] const_1_1_out;
wire magma_Bits_16_eq_inst0_out;
wire magma_Bits_16_sle_inst0_out;
wire magma_Bits_16_ule_inst0_out;
wire magma_Bits_1_eq_inst0_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(magma_Bits_16_ule_inst0_out),
    .I1(magma_Bits_16_sle_inst0_out),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(b),
    .I1(a),
    .S(Mux2xBit_inst0_O),
    .O(Mux2xOutUInt16_inst0_O)
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
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(Mux2xOutUInt16_inst0_O),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_sle #(
    .width(16)
) magma_Bits_16_sle_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_sle_inst0_out)
);
coreir_ule #(
    .width(16)
) magma_Bits_16_ule_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_ule_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
assign O0 = Mux2xOutUInt16_inst0_O;
assign O1 = Mux2xBit_inst0_O;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = Mux2xOutUInt16_inst0_O[15];
assign O4 = bit_const_0_None_out;
assign O5 = bit_const_0_None_out;
endmodule

module LTE (
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
wire [15:0] LTE_comb_inst0_O0;
wire LTE_comb_inst0_O1;
wire LTE_comb_inst0_O2;
wire LTE_comb_inst0_O3;
wire LTE_comb_inst0_O4;
wire LTE_comb_inst0_O5;
LTE_comb LTE_comb_inst0 (
    .signed_(signed_),
    .a(a),
    .b(b),
    .O0(LTE_comb_inst0_O0),
    .O1(LTE_comb_inst0_O1),
    .O2(LTE_comb_inst0_O2),
    .O3(LTE_comb_inst0_O3),
    .O4(LTE_comb_inst0_O4),
    .O5(LTE_comb_inst0_O5)
);
assign O0 = LTE_comb_inst0_O0;
assign O1 = LTE_comb_inst0_O1;
assign O2 = LTE_comb_inst0_O2;
assign O3 = LTE_comb_inst0_O3;
assign O4 = LTE_comb_inst0_O4;
assign O5 = LTE_comb_inst0_O5;
endmodule

module GTE_comb (
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
wire Mux2xBit_inst0_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [0:0] const_1_1_out;
wire magma_Bits_16_eq_inst0_out;
wire magma_Bits_16_sge_inst0_out;
wire magma_Bits_16_uge_inst0_out;
wire magma_Bits_1_eq_inst0_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(magma_Bits_16_uge_inst0_out),
    .I1(magma_Bits_16_sge_inst0_out),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(b),
    .I1(a),
    .S(Mux2xBit_inst0_O),
    .O(Mux2xOutUInt16_inst0_O)
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
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(Mux2xOutUInt16_inst0_O),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_sge #(
    .width(16)
) magma_Bits_16_sge_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_sge_inst0_out)
);
coreir_uge #(
    .width(16)
) magma_Bits_16_uge_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_uge_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
assign O0 = Mux2xOutUInt16_inst0_O;
assign O1 = Mux2xBit_inst0_O;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = Mux2xOutUInt16_inst0_O[15];
assign O4 = bit_const_0_None_out;
assign O5 = bit_const_0_None_out;
endmodule

module GTE (
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
wire [15:0] GTE_comb_inst0_O0;
wire GTE_comb_inst0_O1;
wire GTE_comb_inst0_O2;
wire GTE_comb_inst0_O3;
wire GTE_comb_inst0_O4;
wire GTE_comb_inst0_O5;
GTE_comb GTE_comb_inst0 (
    .signed_(signed_),
    .a(a),
    .b(b),
    .O0(GTE_comb_inst0_O0),
    .O1(GTE_comb_inst0_O1),
    .O2(GTE_comb_inst0_O2),
    .O3(GTE_comb_inst0_O3),
    .O4(GTE_comb_inst0_O4),
    .O5(GTE_comb_inst0_O5)
);
assign O0 = GTE_comb_inst0_O0;
assign O1 = GTE_comb_inst0_O1;
assign O2 = GTE_comb_inst0_O2;
assign O3 = GTE_comb_inst0_O3;
assign O4 = GTE_comb_inst0_O4;
assign O5 = GTE_comb_inst0_O5;
endmodule

module Cond_comb (
    input [4:0] code,
    input alu,
    input Z,
    input N,
    input C,
    input V,
    output O
);
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst10_O;
wire Mux2xBit_inst11_O;
wire Mux2xBit_inst12_O;
wire Mux2xBit_inst13_O;
wire Mux2xBit_inst14_O;
wire Mux2xBit_inst15_O;
wire Mux2xBit_inst16_O;
wire Mux2xBit_inst17_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
wire [4:0] const_0_5_out;
wire [4:0] const_10_5_out;
wire [4:0] const_11_5_out;
wire [4:0] const_12_5_out;
wire [4:0] const_13_5_out;
wire [4:0] const_14_5_out;
wire [4:0] const_15_5_out;
wire [4:0] const_16_5_out;
wire [4:0] const_17_5_out;
wire [4:0] const_1_5_out;
wire [4:0] const_2_5_out;
wire [4:0] const_3_5_out;
wire [4:0] const_4_5_out;
wire [4:0] const_5_5_out;
wire [4:0] const_6_5_out;
wire [4:0] const_7_5_out;
wire [4:0] const_8_5_out;
wire [4:0] const_9_5_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst10_out;
wire magma_Bit_and_inst100_out;
wire magma_Bit_and_inst101_out;
wire magma_Bit_and_inst102_out;
wire magma_Bit_and_inst103_out;
wire magma_Bit_and_inst104_out;
wire magma_Bit_and_inst105_out;
wire magma_Bit_and_inst106_out;
wire magma_Bit_and_inst107_out;
wire magma_Bit_and_inst108_out;
wire magma_Bit_and_inst109_out;
wire magma_Bit_and_inst11_out;
wire magma_Bit_and_inst110_out;
wire magma_Bit_and_inst111_out;
wire magma_Bit_and_inst112_out;
wire magma_Bit_and_inst113_out;
wire magma_Bit_and_inst114_out;
wire magma_Bit_and_inst115_out;
wire magma_Bit_and_inst116_out;
wire magma_Bit_and_inst117_out;
wire magma_Bit_and_inst118_out;
wire magma_Bit_and_inst119_out;
wire magma_Bit_and_inst12_out;
wire magma_Bit_and_inst120_out;
wire magma_Bit_and_inst121_out;
wire magma_Bit_and_inst122_out;
wire magma_Bit_and_inst123_out;
wire magma_Bit_and_inst124_out;
wire magma_Bit_and_inst125_out;
wire magma_Bit_and_inst126_out;
wire magma_Bit_and_inst127_out;
wire magma_Bit_and_inst128_out;
wire magma_Bit_and_inst129_out;
wire magma_Bit_and_inst13_out;
wire magma_Bit_and_inst130_out;
wire magma_Bit_and_inst131_out;
wire magma_Bit_and_inst132_out;
wire magma_Bit_and_inst133_out;
wire magma_Bit_and_inst134_out;
wire magma_Bit_and_inst135_out;
wire magma_Bit_and_inst136_out;
wire magma_Bit_and_inst137_out;
wire magma_Bit_and_inst138_out;
wire magma_Bit_and_inst139_out;
wire magma_Bit_and_inst14_out;
wire magma_Bit_and_inst140_out;
wire magma_Bit_and_inst141_out;
wire magma_Bit_and_inst142_out;
wire magma_Bit_and_inst143_out;
wire magma_Bit_and_inst144_out;
wire magma_Bit_and_inst145_out;
wire magma_Bit_and_inst146_out;
wire magma_Bit_and_inst147_out;
wire magma_Bit_and_inst148_out;
wire magma_Bit_and_inst149_out;
wire magma_Bit_and_inst15_out;
wire magma_Bit_and_inst150_out;
wire magma_Bit_and_inst151_out;
wire magma_Bit_and_inst152_out;
wire magma_Bit_and_inst153_out;
wire magma_Bit_and_inst154_out;
wire magma_Bit_and_inst155_out;
wire magma_Bit_and_inst156_out;
wire magma_Bit_and_inst16_out;
wire magma_Bit_and_inst17_out;
wire magma_Bit_and_inst18_out;
wire magma_Bit_and_inst19_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst20_out;
wire magma_Bit_and_inst21_out;
wire magma_Bit_and_inst22_out;
wire magma_Bit_and_inst23_out;
wire magma_Bit_and_inst24_out;
wire magma_Bit_and_inst25_out;
wire magma_Bit_and_inst26_out;
wire magma_Bit_and_inst27_out;
wire magma_Bit_and_inst28_out;
wire magma_Bit_and_inst29_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_and_inst30_out;
wire magma_Bit_and_inst31_out;
wire magma_Bit_and_inst32_out;
wire magma_Bit_and_inst33_out;
wire magma_Bit_and_inst34_out;
wire magma_Bit_and_inst35_out;
wire magma_Bit_and_inst36_out;
wire magma_Bit_and_inst37_out;
wire magma_Bit_and_inst38_out;
wire magma_Bit_and_inst39_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst40_out;
wire magma_Bit_and_inst41_out;
wire magma_Bit_and_inst42_out;
wire magma_Bit_and_inst43_out;
wire magma_Bit_and_inst44_out;
wire magma_Bit_and_inst45_out;
wire magma_Bit_and_inst46_out;
wire magma_Bit_and_inst47_out;
wire magma_Bit_and_inst48_out;
wire magma_Bit_and_inst49_out;
wire magma_Bit_and_inst5_out;
wire magma_Bit_and_inst50_out;
wire magma_Bit_and_inst51_out;
wire magma_Bit_and_inst52_out;
wire magma_Bit_and_inst53_out;
wire magma_Bit_and_inst54_out;
wire magma_Bit_and_inst55_out;
wire magma_Bit_and_inst56_out;
wire magma_Bit_and_inst57_out;
wire magma_Bit_and_inst58_out;
wire magma_Bit_and_inst59_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst60_out;
wire magma_Bit_and_inst61_out;
wire magma_Bit_and_inst62_out;
wire magma_Bit_and_inst63_out;
wire magma_Bit_and_inst64_out;
wire magma_Bit_and_inst65_out;
wire magma_Bit_and_inst66_out;
wire magma_Bit_and_inst67_out;
wire magma_Bit_and_inst68_out;
wire magma_Bit_and_inst69_out;
wire magma_Bit_and_inst7_out;
wire magma_Bit_and_inst70_out;
wire magma_Bit_and_inst71_out;
wire magma_Bit_and_inst72_out;
wire magma_Bit_and_inst73_out;
wire magma_Bit_and_inst74_out;
wire magma_Bit_and_inst75_out;
wire magma_Bit_and_inst76_out;
wire magma_Bit_and_inst77_out;
wire magma_Bit_and_inst78_out;
wire magma_Bit_and_inst79_out;
wire magma_Bit_and_inst8_out;
wire magma_Bit_and_inst80_out;
wire magma_Bit_and_inst81_out;
wire magma_Bit_and_inst82_out;
wire magma_Bit_and_inst83_out;
wire magma_Bit_and_inst84_out;
wire magma_Bit_and_inst85_out;
wire magma_Bit_and_inst86_out;
wire magma_Bit_and_inst87_out;
wire magma_Bit_and_inst88_out;
wire magma_Bit_and_inst89_out;
wire magma_Bit_and_inst9_out;
wire magma_Bit_and_inst90_out;
wire magma_Bit_and_inst91_out;
wire magma_Bit_and_inst92_out;
wire magma_Bit_and_inst93_out;
wire magma_Bit_and_inst94_out;
wire magma_Bit_and_inst95_out;
wire magma_Bit_and_inst96_out;
wire magma_Bit_and_inst97_out;
wire magma_Bit_and_inst98_out;
wire magma_Bit_and_inst99_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst10_out;
wire magma_Bit_not_inst100_out;
wire magma_Bit_not_inst101_out;
wire magma_Bit_not_inst102_out;
wire magma_Bit_not_inst103_out;
wire magma_Bit_not_inst104_out;
wire magma_Bit_not_inst105_out;
wire magma_Bit_not_inst106_out;
wire magma_Bit_not_inst107_out;
wire magma_Bit_not_inst108_out;
wire magma_Bit_not_inst109_out;
wire magma_Bit_not_inst11_out;
wire magma_Bit_not_inst110_out;
wire magma_Bit_not_inst111_out;
wire magma_Bit_not_inst112_out;
wire magma_Bit_not_inst113_out;
wire magma_Bit_not_inst114_out;
wire magma_Bit_not_inst115_out;
wire magma_Bit_not_inst116_out;
wire magma_Bit_not_inst117_out;
wire magma_Bit_not_inst118_out;
wire magma_Bit_not_inst119_out;
wire magma_Bit_not_inst12_out;
wire magma_Bit_not_inst120_out;
wire magma_Bit_not_inst121_out;
wire magma_Bit_not_inst122_out;
wire magma_Bit_not_inst123_out;
wire magma_Bit_not_inst124_out;
wire magma_Bit_not_inst125_out;
wire magma_Bit_not_inst126_out;
wire magma_Bit_not_inst127_out;
wire magma_Bit_not_inst128_out;
wire magma_Bit_not_inst129_out;
wire magma_Bit_not_inst13_out;
wire magma_Bit_not_inst130_out;
wire magma_Bit_not_inst131_out;
wire magma_Bit_not_inst132_out;
wire magma_Bit_not_inst133_out;
wire magma_Bit_not_inst134_out;
wire magma_Bit_not_inst135_out;
wire magma_Bit_not_inst136_out;
wire magma_Bit_not_inst137_out;
wire magma_Bit_not_inst138_out;
wire magma_Bit_not_inst139_out;
wire magma_Bit_not_inst14_out;
wire magma_Bit_not_inst140_out;
wire magma_Bit_not_inst141_out;
wire magma_Bit_not_inst142_out;
wire magma_Bit_not_inst143_out;
wire magma_Bit_not_inst144_out;
wire magma_Bit_not_inst145_out;
wire magma_Bit_not_inst146_out;
wire magma_Bit_not_inst147_out;
wire magma_Bit_not_inst148_out;
wire magma_Bit_not_inst149_out;
wire magma_Bit_not_inst15_out;
wire magma_Bit_not_inst150_out;
wire magma_Bit_not_inst151_out;
wire magma_Bit_not_inst152_out;
wire magma_Bit_not_inst153_out;
wire magma_Bit_not_inst154_out;
wire magma_Bit_not_inst155_out;
wire magma_Bit_not_inst156_out;
wire magma_Bit_not_inst157_out;
wire magma_Bit_not_inst158_out;
wire magma_Bit_not_inst159_out;
wire magma_Bit_not_inst16_out;
wire magma_Bit_not_inst160_out;
wire magma_Bit_not_inst161_out;
wire magma_Bit_not_inst162_out;
wire magma_Bit_not_inst163_out;
wire magma_Bit_not_inst164_out;
wire magma_Bit_not_inst165_out;
wire magma_Bit_not_inst17_out;
wire magma_Bit_not_inst18_out;
wire magma_Bit_not_inst19_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst20_out;
wire magma_Bit_not_inst21_out;
wire magma_Bit_not_inst22_out;
wire magma_Bit_not_inst23_out;
wire magma_Bit_not_inst24_out;
wire magma_Bit_not_inst25_out;
wire magma_Bit_not_inst26_out;
wire magma_Bit_not_inst27_out;
wire magma_Bit_not_inst28_out;
wire magma_Bit_not_inst29_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst30_out;
wire magma_Bit_not_inst31_out;
wire magma_Bit_not_inst32_out;
wire magma_Bit_not_inst33_out;
wire magma_Bit_not_inst34_out;
wire magma_Bit_not_inst35_out;
wire magma_Bit_not_inst36_out;
wire magma_Bit_not_inst37_out;
wire magma_Bit_not_inst38_out;
wire magma_Bit_not_inst39_out;
wire magma_Bit_not_inst4_out;
wire magma_Bit_not_inst40_out;
wire magma_Bit_not_inst41_out;
wire magma_Bit_not_inst42_out;
wire magma_Bit_not_inst43_out;
wire magma_Bit_not_inst44_out;
wire magma_Bit_not_inst45_out;
wire magma_Bit_not_inst46_out;
wire magma_Bit_not_inst47_out;
wire magma_Bit_not_inst48_out;
wire magma_Bit_not_inst49_out;
wire magma_Bit_not_inst5_out;
wire magma_Bit_not_inst50_out;
wire magma_Bit_not_inst51_out;
wire magma_Bit_not_inst52_out;
wire magma_Bit_not_inst53_out;
wire magma_Bit_not_inst54_out;
wire magma_Bit_not_inst55_out;
wire magma_Bit_not_inst56_out;
wire magma_Bit_not_inst57_out;
wire magma_Bit_not_inst58_out;
wire magma_Bit_not_inst59_out;
wire magma_Bit_not_inst6_out;
wire magma_Bit_not_inst60_out;
wire magma_Bit_not_inst61_out;
wire magma_Bit_not_inst62_out;
wire magma_Bit_not_inst63_out;
wire magma_Bit_not_inst64_out;
wire magma_Bit_not_inst65_out;
wire magma_Bit_not_inst66_out;
wire magma_Bit_not_inst67_out;
wire magma_Bit_not_inst68_out;
wire magma_Bit_not_inst69_out;
wire magma_Bit_not_inst7_out;
wire magma_Bit_not_inst70_out;
wire magma_Bit_not_inst71_out;
wire magma_Bit_not_inst72_out;
wire magma_Bit_not_inst73_out;
wire magma_Bit_not_inst74_out;
wire magma_Bit_not_inst75_out;
wire magma_Bit_not_inst76_out;
wire magma_Bit_not_inst77_out;
wire magma_Bit_not_inst78_out;
wire magma_Bit_not_inst79_out;
wire magma_Bit_not_inst8_out;
wire magma_Bit_not_inst80_out;
wire magma_Bit_not_inst81_out;
wire magma_Bit_not_inst82_out;
wire magma_Bit_not_inst83_out;
wire magma_Bit_not_inst84_out;
wire magma_Bit_not_inst85_out;
wire magma_Bit_not_inst86_out;
wire magma_Bit_not_inst87_out;
wire magma_Bit_not_inst88_out;
wire magma_Bit_not_inst89_out;
wire magma_Bit_not_inst9_out;
wire magma_Bit_not_inst90_out;
wire magma_Bit_not_inst91_out;
wire magma_Bit_not_inst92_out;
wire magma_Bit_not_inst93_out;
wire magma_Bit_not_inst94_out;
wire magma_Bit_not_inst95_out;
wire magma_Bit_not_inst96_out;
wire magma_Bit_not_inst97_out;
wire magma_Bit_not_inst98_out;
wire magma_Bit_not_inst99_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst10_out;
wire magma_Bit_or_inst11_out;
wire magma_Bit_or_inst12_out;
wire magma_Bit_or_inst13_out;
wire magma_Bit_or_inst14_out;
wire magma_Bit_or_inst15_out;
wire magma_Bit_or_inst16_out;
wire magma_Bit_or_inst17_out;
wire magma_Bit_or_inst18_out;
wire magma_Bit_or_inst19_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst20_out;
wire magma_Bit_or_inst21_out;
wire magma_Bit_or_inst22_out;
wire magma_Bit_or_inst23_out;
wire magma_Bit_or_inst24_out;
wire magma_Bit_or_inst25_out;
wire magma_Bit_or_inst26_out;
wire magma_Bit_or_inst27_out;
wire magma_Bit_or_inst28_out;
wire magma_Bit_or_inst29_out;
wire magma_Bit_or_inst3_out;
wire magma_Bit_or_inst30_out;
wire magma_Bit_or_inst31_out;
wire magma_Bit_or_inst32_out;
wire magma_Bit_or_inst33_out;
wire magma_Bit_or_inst34_out;
wire magma_Bit_or_inst4_out;
wire magma_Bit_or_inst5_out;
wire magma_Bit_or_inst6_out;
wire magma_Bit_or_inst7_out;
wire magma_Bit_or_inst8_out;
wire magma_Bit_or_inst9_out;
wire magma_Bit_xor_inst0_out;
wire magma_Bit_xor_inst1_out;
wire magma_Bit_xor_inst2_out;
wire magma_Bit_xor_inst3_out;
wire magma_Bits_5_eq_inst0_out;
wire magma_Bits_5_eq_inst1_out;
wire magma_Bits_5_eq_inst10_out;
wire magma_Bits_5_eq_inst100_out;
wire magma_Bits_5_eq_inst101_out;
wire magma_Bits_5_eq_inst102_out;
wire magma_Bits_5_eq_inst103_out;
wire magma_Bits_5_eq_inst104_out;
wire magma_Bits_5_eq_inst105_out;
wire magma_Bits_5_eq_inst106_out;
wire magma_Bits_5_eq_inst107_out;
wire magma_Bits_5_eq_inst108_out;
wire magma_Bits_5_eq_inst109_out;
wire magma_Bits_5_eq_inst11_out;
wire magma_Bits_5_eq_inst110_out;
wire magma_Bits_5_eq_inst111_out;
wire magma_Bits_5_eq_inst112_out;
wire magma_Bits_5_eq_inst113_out;
wire magma_Bits_5_eq_inst114_out;
wire magma_Bits_5_eq_inst115_out;
wire magma_Bits_5_eq_inst116_out;
wire magma_Bits_5_eq_inst117_out;
wire magma_Bits_5_eq_inst118_out;
wire magma_Bits_5_eq_inst119_out;
wire magma_Bits_5_eq_inst12_out;
wire magma_Bits_5_eq_inst120_out;
wire magma_Bits_5_eq_inst121_out;
wire magma_Bits_5_eq_inst122_out;
wire magma_Bits_5_eq_inst123_out;
wire magma_Bits_5_eq_inst124_out;
wire magma_Bits_5_eq_inst125_out;
wire magma_Bits_5_eq_inst126_out;
wire magma_Bits_5_eq_inst127_out;
wire magma_Bits_5_eq_inst128_out;
wire magma_Bits_5_eq_inst129_out;
wire magma_Bits_5_eq_inst13_out;
wire magma_Bits_5_eq_inst130_out;
wire magma_Bits_5_eq_inst131_out;
wire magma_Bits_5_eq_inst132_out;
wire magma_Bits_5_eq_inst133_out;
wire magma_Bits_5_eq_inst134_out;
wire magma_Bits_5_eq_inst135_out;
wire magma_Bits_5_eq_inst136_out;
wire magma_Bits_5_eq_inst137_out;
wire magma_Bits_5_eq_inst138_out;
wire magma_Bits_5_eq_inst139_out;
wire magma_Bits_5_eq_inst14_out;
wire magma_Bits_5_eq_inst140_out;
wire magma_Bits_5_eq_inst141_out;
wire magma_Bits_5_eq_inst142_out;
wire magma_Bits_5_eq_inst143_out;
wire magma_Bits_5_eq_inst144_out;
wire magma_Bits_5_eq_inst145_out;
wire magma_Bits_5_eq_inst146_out;
wire magma_Bits_5_eq_inst147_out;
wire magma_Bits_5_eq_inst148_out;
wire magma_Bits_5_eq_inst149_out;
wire magma_Bits_5_eq_inst15_out;
wire magma_Bits_5_eq_inst150_out;
wire magma_Bits_5_eq_inst151_out;
wire magma_Bits_5_eq_inst152_out;
wire magma_Bits_5_eq_inst153_out;
wire magma_Bits_5_eq_inst154_out;
wire magma_Bits_5_eq_inst155_out;
wire magma_Bits_5_eq_inst156_out;
wire magma_Bits_5_eq_inst157_out;
wire magma_Bits_5_eq_inst158_out;
wire magma_Bits_5_eq_inst159_out;
wire magma_Bits_5_eq_inst16_out;
wire magma_Bits_5_eq_inst160_out;
wire magma_Bits_5_eq_inst161_out;
wire magma_Bits_5_eq_inst162_out;
wire magma_Bits_5_eq_inst163_out;
wire magma_Bits_5_eq_inst164_out;
wire magma_Bits_5_eq_inst165_out;
wire magma_Bits_5_eq_inst166_out;
wire magma_Bits_5_eq_inst167_out;
wire magma_Bits_5_eq_inst168_out;
wire magma_Bits_5_eq_inst169_out;
wire magma_Bits_5_eq_inst17_out;
wire magma_Bits_5_eq_inst170_out;
wire magma_Bits_5_eq_inst171_out;
wire magma_Bits_5_eq_inst172_out;
wire magma_Bits_5_eq_inst173_out;
wire magma_Bits_5_eq_inst174_out;
wire magma_Bits_5_eq_inst175_out;
wire magma_Bits_5_eq_inst176_out;
wire magma_Bits_5_eq_inst177_out;
wire magma_Bits_5_eq_inst178_out;
wire magma_Bits_5_eq_inst179_out;
wire magma_Bits_5_eq_inst18_out;
wire magma_Bits_5_eq_inst180_out;
wire magma_Bits_5_eq_inst181_out;
wire magma_Bits_5_eq_inst182_out;
wire magma_Bits_5_eq_inst183_out;
wire magma_Bits_5_eq_inst184_out;
wire magma_Bits_5_eq_inst185_out;
wire magma_Bits_5_eq_inst186_out;
wire magma_Bits_5_eq_inst187_out;
wire magma_Bits_5_eq_inst188_out;
wire magma_Bits_5_eq_inst189_out;
wire magma_Bits_5_eq_inst19_out;
wire magma_Bits_5_eq_inst190_out;
wire magma_Bits_5_eq_inst191_out;
wire magma_Bits_5_eq_inst192_out;
wire magma_Bits_5_eq_inst193_out;
wire magma_Bits_5_eq_inst194_out;
wire magma_Bits_5_eq_inst195_out;
wire magma_Bits_5_eq_inst196_out;
wire magma_Bits_5_eq_inst197_out;
wire magma_Bits_5_eq_inst198_out;
wire magma_Bits_5_eq_inst199_out;
wire magma_Bits_5_eq_inst2_out;
wire magma_Bits_5_eq_inst20_out;
wire magma_Bits_5_eq_inst200_out;
wire magma_Bits_5_eq_inst201_out;
wire magma_Bits_5_eq_inst21_out;
wire magma_Bits_5_eq_inst22_out;
wire magma_Bits_5_eq_inst23_out;
wire magma_Bits_5_eq_inst24_out;
wire magma_Bits_5_eq_inst25_out;
wire magma_Bits_5_eq_inst26_out;
wire magma_Bits_5_eq_inst27_out;
wire magma_Bits_5_eq_inst28_out;
wire magma_Bits_5_eq_inst29_out;
wire magma_Bits_5_eq_inst3_out;
wire magma_Bits_5_eq_inst30_out;
wire magma_Bits_5_eq_inst31_out;
wire magma_Bits_5_eq_inst32_out;
wire magma_Bits_5_eq_inst33_out;
wire magma_Bits_5_eq_inst34_out;
wire magma_Bits_5_eq_inst35_out;
wire magma_Bits_5_eq_inst36_out;
wire magma_Bits_5_eq_inst37_out;
wire magma_Bits_5_eq_inst38_out;
wire magma_Bits_5_eq_inst39_out;
wire magma_Bits_5_eq_inst4_out;
wire magma_Bits_5_eq_inst40_out;
wire magma_Bits_5_eq_inst41_out;
wire magma_Bits_5_eq_inst42_out;
wire magma_Bits_5_eq_inst43_out;
wire magma_Bits_5_eq_inst44_out;
wire magma_Bits_5_eq_inst45_out;
wire magma_Bits_5_eq_inst46_out;
wire magma_Bits_5_eq_inst47_out;
wire magma_Bits_5_eq_inst48_out;
wire magma_Bits_5_eq_inst49_out;
wire magma_Bits_5_eq_inst5_out;
wire magma_Bits_5_eq_inst50_out;
wire magma_Bits_5_eq_inst51_out;
wire magma_Bits_5_eq_inst52_out;
wire magma_Bits_5_eq_inst53_out;
wire magma_Bits_5_eq_inst54_out;
wire magma_Bits_5_eq_inst55_out;
wire magma_Bits_5_eq_inst56_out;
wire magma_Bits_5_eq_inst57_out;
wire magma_Bits_5_eq_inst58_out;
wire magma_Bits_5_eq_inst59_out;
wire magma_Bits_5_eq_inst6_out;
wire magma_Bits_5_eq_inst60_out;
wire magma_Bits_5_eq_inst61_out;
wire magma_Bits_5_eq_inst62_out;
wire magma_Bits_5_eq_inst63_out;
wire magma_Bits_5_eq_inst64_out;
wire magma_Bits_5_eq_inst65_out;
wire magma_Bits_5_eq_inst66_out;
wire magma_Bits_5_eq_inst67_out;
wire magma_Bits_5_eq_inst68_out;
wire magma_Bits_5_eq_inst69_out;
wire magma_Bits_5_eq_inst7_out;
wire magma_Bits_5_eq_inst70_out;
wire magma_Bits_5_eq_inst71_out;
wire magma_Bits_5_eq_inst72_out;
wire magma_Bits_5_eq_inst73_out;
wire magma_Bits_5_eq_inst74_out;
wire magma_Bits_5_eq_inst75_out;
wire magma_Bits_5_eq_inst76_out;
wire magma_Bits_5_eq_inst77_out;
wire magma_Bits_5_eq_inst78_out;
wire magma_Bits_5_eq_inst79_out;
wire magma_Bits_5_eq_inst8_out;
wire magma_Bits_5_eq_inst80_out;
wire magma_Bits_5_eq_inst81_out;
wire magma_Bits_5_eq_inst82_out;
wire magma_Bits_5_eq_inst83_out;
wire magma_Bits_5_eq_inst84_out;
wire magma_Bits_5_eq_inst85_out;
wire magma_Bits_5_eq_inst86_out;
wire magma_Bits_5_eq_inst87_out;
wire magma_Bits_5_eq_inst88_out;
wire magma_Bits_5_eq_inst89_out;
wire magma_Bits_5_eq_inst9_out;
wire magma_Bits_5_eq_inst90_out;
wire magma_Bits_5_eq_inst91_out;
wire magma_Bits_5_eq_inst92_out;
wire magma_Bits_5_eq_inst93_out;
wire magma_Bits_5_eq_inst94_out;
wire magma_Bits_5_eq_inst95_out;
wire magma_Bits_5_eq_inst96_out;
wire magma_Bits_5_eq_inst97_out;
wire magma_Bits_5_eq_inst98_out;
wire magma_Bits_5_eq_inst99_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(magma_Bit_and_inst3_out),
    .I1(magma_Bit_or_inst3_out),
    .S(magma_Bit_and_inst20_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(Mux2xBit_inst0_O),
    .I1(magma_Bit_and_inst2_out),
    .S(magma_Bit_and_inst36_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(Mux2xBit_inst9_O),
    .I1(magma_Bit_not_inst3_out),
    .S(magma_Bit_and_inst135_out),
    .O(Mux2xBit_inst10_O)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(Mux2xBit_inst10_O),
    .I1(V),
    .S(magma_Bit_and_inst141_out),
    .O(Mux2xBit_inst11_O)
);
Mux2xBit Mux2xBit_inst12 (
    .I0(Mux2xBit_inst11_O),
    .I1(magma_Bit_not_inst2_out),
    .S(magma_Bit_and_inst146_out),
    .O(Mux2xBit_inst12_O)
);
Mux2xBit Mux2xBit_inst13 (
    .I0(Mux2xBit_inst12_O),
    .I1(N),
    .S(magma_Bit_and_inst150_out),
    .O(Mux2xBit_inst13_O)
);
Mux2xBit Mux2xBit_inst14 (
    .I0(Mux2xBit_inst13_O),
    .I1(magma_Bit_not_inst1_out),
    .S(magma_Bit_and_inst153_out),
    .O(Mux2xBit_inst14_O)
);
Mux2xBit Mux2xBit_inst15 (
    .I0(Mux2xBit_inst14_O),
    .I1(C),
    .S(magma_Bit_and_inst155_out),
    .O(Mux2xBit_inst15_O)
);
Mux2xBit Mux2xBit_inst16 (
    .I0(Mux2xBit_inst15_O),
    .I1(magma_Bit_not_inst0_out),
    .S(magma_Bit_and_inst156_out),
    .O(Mux2xBit_inst16_O)
);
Mux2xBit Mux2xBit_inst17 (
    .I0(Mux2xBit_inst16_O),
    .I1(Z),
    .S(magma_Bits_5_eq_inst201_out),
    .O(Mux2xBit_inst17_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(Mux2xBit_inst1_O),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bit_and_inst51_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(Mux2xBit_inst2_O),
    .I1(alu),
    .S(magma_Bit_and_inst65_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(Mux2xBit_inst3_O),
    .I1(magma_Bit_or_inst1_out),
    .S(magma_Bit_and_inst78_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(Mux2xBit_inst4_O),
    .I1(magma_Bit_and_inst1_out),
    .S(magma_Bit_and_inst90_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(Mux2xBit_inst5_O),
    .I1(magma_Bit_xor_inst1_out),
    .S(magma_Bit_and_inst101_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(Mux2xBit_inst6_O),
    .I1(magma_Bit_not_inst6_out),
    .S(magma_Bit_and_inst111_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(Mux2xBit_inst7_O),
    .I1(magma_Bit_or_inst0_out),
    .S(magma_Bit_and_inst120_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(Mux2xBit_inst8_O),
    .I1(magma_Bit_and_inst0_out),
    .S(magma_Bit_and_inst128_out),
    .O(Mux2xBit_inst9_O)
);
coreir_const #(
    .value(5'h00),
    .width(5)
) const_0_5 (
    .out(const_0_5_out)
);
coreir_const #(
    .value(5'h0a),
    .width(5)
) const_10_5 (
    .out(const_10_5_out)
);
coreir_const #(
    .value(5'h0b),
    .width(5)
) const_11_5 (
    .out(const_11_5_out)
);
coreir_const #(
    .value(5'h0c),
    .width(5)
) const_12_5 (
    .out(const_12_5_out)
);
coreir_const #(
    .value(5'h0d),
    .width(5)
) const_13_5 (
    .out(const_13_5_out)
);
coreir_const #(
    .value(5'h0e),
    .width(5)
) const_14_5 (
    .out(const_14_5_out)
);
coreir_const #(
    .value(5'h0f),
    .width(5)
) const_15_5 (
    .out(const_15_5_out)
);
coreir_const #(
    .value(5'h10),
    .width(5)
) const_16_5 (
    .out(const_16_5_out)
);
coreir_const #(
    .value(5'h11),
    .width(5)
) const_17_5 (
    .out(const_17_5_out)
);
coreir_const #(
    .value(5'h01),
    .width(5)
) const_1_5 (
    .out(const_1_5_out)
);
coreir_const #(
    .value(5'h02),
    .width(5)
) const_2_5 (
    .out(const_2_5_out)
);
coreir_const #(
    .value(5'h03),
    .width(5)
) const_3_5 (
    .out(const_3_5_out)
);
coreir_const #(
    .value(5'h04),
    .width(5)
) const_4_5 (
    .out(const_4_5_out)
);
coreir_const #(
    .value(5'h05),
    .width(5)
) const_5_5 (
    .out(const_5_5_out)
);
coreir_const #(
    .value(5'h06),
    .width(5)
) const_6_5 (
    .out(const_6_5_out)
);
coreir_const #(
    .value(5'h07),
    .width(5)
) const_7_5 (
    .out(const_7_5_out)
);
coreir_const #(
    .value(5'h08),
    .width(5)
) const_8_5 (
    .out(const_8_5_out)
);
coreir_const #(
    .value(5'h09),
    .width(5)
) const_9_5 (
    .out(const_9_5_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(C),
    .in1(magma_Bit_not_inst4_out),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_not_inst7_out),
    .in1(magma_Bit_not_inst8_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst10 (
    .in0(magma_Bit_and_inst9_out),
    .in1(magma_Bit_not_inst19_out),
    .out(magma_Bit_and_inst10_out)
);
corebit_and magma_Bit_and_inst100 (
    .in0(magma_Bit_and_inst99_out),
    .in1(magma_Bit_not_inst109_out),
    .out(magma_Bit_and_inst100_out)
);
corebit_and magma_Bit_and_inst101 (
    .in0(magma_Bit_and_inst100_out),
    .in1(magma_Bit_not_inst110_out),
    .out(magma_Bit_and_inst101_out)
);
corebit_and magma_Bit_and_inst102 (
    .in0(magma_Bits_5_eq_inst119_out),
    .in1(magma_Bit_not_inst111_out),
    .out(magma_Bit_and_inst102_out)
);
corebit_and magma_Bit_and_inst103 (
    .in0(magma_Bit_and_inst102_out),
    .in1(magma_Bit_not_inst112_out),
    .out(magma_Bit_and_inst103_out)
);
corebit_and magma_Bit_and_inst104 (
    .in0(magma_Bit_and_inst103_out),
    .in1(magma_Bit_not_inst113_out),
    .out(magma_Bit_and_inst104_out)
);
corebit_and magma_Bit_and_inst105 (
    .in0(magma_Bit_and_inst104_out),
    .in1(magma_Bit_not_inst114_out),
    .out(magma_Bit_and_inst105_out)
);
corebit_and magma_Bit_and_inst106 (
    .in0(magma_Bit_and_inst105_out),
    .in1(magma_Bit_not_inst115_out),
    .out(magma_Bit_and_inst106_out)
);
corebit_and magma_Bit_and_inst107 (
    .in0(magma_Bit_and_inst106_out),
    .in1(magma_Bit_not_inst116_out),
    .out(magma_Bit_and_inst107_out)
);
corebit_and magma_Bit_and_inst108 (
    .in0(magma_Bit_and_inst107_out),
    .in1(magma_Bit_not_inst117_out),
    .out(magma_Bit_and_inst108_out)
);
corebit_and magma_Bit_and_inst109 (
    .in0(magma_Bit_and_inst108_out),
    .in1(magma_Bit_not_inst118_out),
    .out(magma_Bit_and_inst109_out)
);
corebit_and magma_Bit_and_inst11 (
    .in0(magma_Bit_and_inst10_out),
    .in1(magma_Bit_not_inst20_out),
    .out(magma_Bit_and_inst11_out)
);
corebit_and magma_Bit_and_inst110 (
    .in0(magma_Bit_and_inst109_out),
    .in1(magma_Bit_not_inst119_out),
    .out(magma_Bit_and_inst110_out)
);
corebit_and magma_Bit_and_inst111 (
    .in0(magma_Bit_and_inst110_out),
    .in1(magma_Bit_not_inst120_out),
    .out(magma_Bit_and_inst111_out)
);
corebit_and magma_Bit_and_inst112 (
    .in0(magma_Bits_5_eq_inst132_out),
    .in1(magma_Bit_not_inst121_out),
    .out(magma_Bit_and_inst112_out)
);
corebit_and magma_Bit_and_inst113 (
    .in0(magma_Bit_and_inst112_out),
    .in1(magma_Bit_not_inst122_out),
    .out(magma_Bit_and_inst113_out)
);
corebit_and magma_Bit_and_inst114 (
    .in0(magma_Bit_and_inst113_out),
    .in1(magma_Bit_not_inst123_out),
    .out(magma_Bit_and_inst114_out)
);
corebit_and magma_Bit_and_inst115 (
    .in0(magma_Bit_and_inst114_out),
    .in1(magma_Bit_not_inst124_out),
    .out(magma_Bit_and_inst115_out)
);
corebit_and magma_Bit_and_inst116 (
    .in0(magma_Bit_and_inst115_out),
    .in1(magma_Bit_not_inst125_out),
    .out(magma_Bit_and_inst116_out)
);
corebit_and magma_Bit_and_inst117 (
    .in0(magma_Bit_and_inst116_out),
    .in1(magma_Bit_not_inst126_out),
    .out(magma_Bit_and_inst117_out)
);
corebit_and magma_Bit_and_inst118 (
    .in0(magma_Bit_and_inst117_out),
    .in1(magma_Bit_not_inst127_out),
    .out(magma_Bit_and_inst118_out)
);
corebit_and magma_Bit_and_inst119 (
    .in0(magma_Bit_and_inst118_out),
    .in1(magma_Bit_not_inst128_out),
    .out(magma_Bit_and_inst119_out)
);
corebit_and magma_Bit_and_inst12 (
    .in0(magma_Bit_and_inst11_out),
    .in1(magma_Bit_not_inst21_out),
    .out(magma_Bit_and_inst12_out)
);
corebit_and magma_Bit_and_inst120 (
    .in0(magma_Bit_and_inst119_out),
    .in1(magma_Bit_not_inst129_out),
    .out(magma_Bit_and_inst120_out)
);
corebit_and magma_Bit_and_inst121 (
    .in0(magma_Bits_5_eq_inst144_out),
    .in1(magma_Bit_not_inst130_out),
    .out(magma_Bit_and_inst121_out)
);
corebit_and magma_Bit_and_inst122 (
    .in0(magma_Bit_and_inst121_out),
    .in1(magma_Bit_not_inst131_out),
    .out(magma_Bit_and_inst122_out)
);
corebit_and magma_Bit_and_inst123 (
    .in0(magma_Bit_and_inst122_out),
    .in1(magma_Bit_not_inst132_out),
    .out(magma_Bit_and_inst123_out)
);
corebit_and magma_Bit_and_inst124 (
    .in0(magma_Bit_and_inst123_out),
    .in1(magma_Bit_not_inst133_out),
    .out(magma_Bit_and_inst124_out)
);
corebit_and magma_Bit_and_inst125 (
    .in0(magma_Bit_and_inst124_out),
    .in1(magma_Bit_not_inst134_out),
    .out(magma_Bit_and_inst125_out)
);
corebit_and magma_Bit_and_inst126 (
    .in0(magma_Bit_and_inst125_out),
    .in1(magma_Bit_not_inst135_out),
    .out(magma_Bit_and_inst126_out)
);
corebit_and magma_Bit_and_inst127 (
    .in0(magma_Bit_and_inst126_out),
    .in1(magma_Bit_not_inst136_out),
    .out(magma_Bit_and_inst127_out)
);
corebit_and magma_Bit_and_inst128 (
    .in0(magma_Bit_and_inst127_out),
    .in1(magma_Bit_not_inst137_out),
    .out(magma_Bit_and_inst128_out)
);
corebit_and magma_Bit_and_inst129 (
    .in0(magma_Bits_5_eq_inst155_out),
    .in1(magma_Bit_not_inst138_out),
    .out(magma_Bit_and_inst129_out)
);
corebit_and magma_Bit_and_inst13 (
    .in0(magma_Bit_and_inst12_out),
    .in1(magma_Bit_not_inst22_out),
    .out(magma_Bit_and_inst13_out)
);
corebit_and magma_Bit_and_inst130 (
    .in0(magma_Bit_and_inst129_out),
    .in1(magma_Bit_not_inst139_out),
    .out(magma_Bit_and_inst130_out)
);
corebit_and magma_Bit_and_inst131 (
    .in0(magma_Bit_and_inst130_out),
    .in1(magma_Bit_not_inst140_out),
    .out(magma_Bit_and_inst131_out)
);
corebit_and magma_Bit_and_inst132 (
    .in0(magma_Bit_and_inst131_out),
    .in1(magma_Bit_not_inst141_out),
    .out(magma_Bit_and_inst132_out)
);
corebit_and magma_Bit_and_inst133 (
    .in0(magma_Bit_and_inst132_out),
    .in1(magma_Bit_not_inst142_out),
    .out(magma_Bit_and_inst133_out)
);
corebit_and magma_Bit_and_inst134 (
    .in0(magma_Bit_and_inst133_out),
    .in1(magma_Bit_not_inst143_out),
    .out(magma_Bit_and_inst134_out)
);
corebit_and magma_Bit_and_inst135 (
    .in0(magma_Bit_and_inst134_out),
    .in1(magma_Bit_not_inst144_out),
    .out(magma_Bit_and_inst135_out)
);
corebit_and magma_Bit_and_inst136 (
    .in0(magma_Bits_5_eq_inst165_out),
    .in1(magma_Bit_not_inst145_out),
    .out(magma_Bit_and_inst136_out)
);
corebit_and magma_Bit_and_inst137 (
    .in0(magma_Bit_and_inst136_out),
    .in1(magma_Bit_not_inst146_out),
    .out(magma_Bit_and_inst137_out)
);
corebit_and magma_Bit_and_inst138 (
    .in0(magma_Bit_and_inst137_out),
    .in1(magma_Bit_not_inst147_out),
    .out(magma_Bit_and_inst138_out)
);
corebit_and magma_Bit_and_inst139 (
    .in0(magma_Bit_and_inst138_out),
    .in1(magma_Bit_not_inst148_out),
    .out(magma_Bit_and_inst139_out)
);
corebit_and magma_Bit_and_inst14 (
    .in0(magma_Bit_and_inst13_out),
    .in1(magma_Bit_not_inst23_out),
    .out(magma_Bit_and_inst14_out)
);
corebit_and magma_Bit_and_inst140 (
    .in0(magma_Bit_and_inst139_out),
    .in1(magma_Bit_not_inst149_out),
    .out(magma_Bit_and_inst140_out)
);
corebit_and magma_Bit_and_inst141 (
    .in0(magma_Bit_and_inst140_out),
    .in1(magma_Bit_not_inst150_out),
    .out(magma_Bit_and_inst141_out)
);
corebit_and magma_Bit_and_inst142 (
    .in0(magma_Bits_5_eq_inst174_out),
    .in1(magma_Bit_not_inst151_out),
    .out(magma_Bit_and_inst142_out)
);
corebit_and magma_Bit_and_inst143 (
    .in0(magma_Bit_and_inst142_out),
    .in1(magma_Bit_not_inst152_out),
    .out(magma_Bit_and_inst143_out)
);
corebit_and magma_Bit_and_inst144 (
    .in0(magma_Bit_and_inst143_out),
    .in1(magma_Bit_not_inst153_out),
    .out(magma_Bit_and_inst144_out)
);
corebit_and magma_Bit_and_inst145 (
    .in0(magma_Bit_and_inst144_out),
    .in1(magma_Bit_not_inst154_out),
    .out(magma_Bit_and_inst145_out)
);
corebit_and magma_Bit_and_inst146 (
    .in0(magma_Bit_and_inst145_out),
    .in1(magma_Bit_not_inst155_out),
    .out(magma_Bit_and_inst146_out)
);
corebit_and magma_Bit_and_inst147 (
    .in0(magma_Bits_5_eq_inst182_out),
    .in1(magma_Bit_not_inst156_out),
    .out(magma_Bit_and_inst147_out)
);
corebit_and magma_Bit_and_inst148 (
    .in0(magma_Bit_and_inst147_out),
    .in1(magma_Bit_not_inst157_out),
    .out(magma_Bit_and_inst148_out)
);
corebit_and magma_Bit_and_inst149 (
    .in0(magma_Bit_and_inst148_out),
    .in1(magma_Bit_not_inst158_out),
    .out(magma_Bit_and_inst149_out)
);
corebit_and magma_Bit_and_inst15 (
    .in0(magma_Bit_and_inst14_out),
    .in1(magma_Bit_not_inst24_out),
    .out(magma_Bit_and_inst15_out)
);
corebit_and magma_Bit_and_inst150 (
    .in0(magma_Bit_and_inst149_out),
    .in1(magma_Bit_not_inst159_out),
    .out(magma_Bit_and_inst150_out)
);
corebit_and magma_Bit_and_inst151 (
    .in0(magma_Bit_or_inst32_out),
    .in1(magma_Bit_not_inst160_out),
    .out(magma_Bit_and_inst151_out)
);
corebit_and magma_Bit_and_inst152 (
    .in0(magma_Bit_and_inst151_out),
    .in1(magma_Bit_not_inst161_out),
    .out(magma_Bit_and_inst152_out)
);
corebit_and magma_Bit_and_inst153 (
    .in0(magma_Bit_and_inst152_out),
    .in1(magma_Bit_not_inst162_out),
    .out(magma_Bit_and_inst153_out)
);
corebit_and magma_Bit_and_inst154 (
    .in0(magma_Bit_or_inst34_out),
    .in1(magma_Bit_not_inst163_out),
    .out(magma_Bit_and_inst154_out)
);
corebit_and magma_Bit_and_inst155 (
    .in0(magma_Bit_and_inst154_out),
    .in1(magma_Bit_not_inst164_out),
    .out(magma_Bit_and_inst155_out)
);
corebit_and magma_Bit_and_inst156 (
    .in0(magma_Bits_5_eq_inst199_out),
    .in1(magma_Bit_not_inst165_out),
    .out(magma_Bit_and_inst156_out)
);
corebit_and magma_Bit_and_inst16 (
    .in0(magma_Bit_and_inst15_out),
    .in1(magma_Bit_not_inst25_out),
    .out(magma_Bit_and_inst16_out)
);
corebit_and magma_Bit_and_inst17 (
    .in0(magma_Bit_and_inst16_out),
    .in1(magma_Bit_not_inst26_out),
    .out(magma_Bit_and_inst17_out)
);
corebit_and magma_Bit_and_inst18 (
    .in0(magma_Bit_and_inst17_out),
    .in1(magma_Bit_not_inst27_out),
    .out(magma_Bit_and_inst18_out)
);
corebit_and magma_Bit_and_inst19 (
    .in0(magma_Bit_and_inst18_out),
    .in1(magma_Bit_not_inst28_out),
    .out(magma_Bit_and_inst19_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_not_inst10_out),
    .in1(magma_Bit_not_inst11_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_and magma_Bit_and_inst20 (
    .in0(magma_Bit_and_inst19_out),
    .in1(magma_Bit_not_inst29_out),
    .out(magma_Bit_and_inst20_out)
);
corebit_and magma_Bit_and_inst21 (
    .in0(magma_Bits_5_eq_inst20_out),
    .in1(magma_Bit_not_inst30_out),
    .out(magma_Bit_and_inst21_out)
);
corebit_and magma_Bit_and_inst22 (
    .in0(magma_Bit_and_inst21_out),
    .in1(magma_Bit_not_inst31_out),
    .out(magma_Bit_and_inst22_out)
);
corebit_and magma_Bit_and_inst23 (
    .in0(magma_Bit_and_inst22_out),
    .in1(magma_Bit_not_inst32_out),
    .out(magma_Bit_and_inst23_out)
);
corebit_and magma_Bit_and_inst24 (
    .in0(magma_Bit_and_inst23_out),
    .in1(magma_Bit_not_inst33_out),
    .out(magma_Bit_and_inst24_out)
);
corebit_and magma_Bit_and_inst25 (
    .in0(magma_Bit_and_inst24_out),
    .in1(magma_Bit_not_inst34_out),
    .out(magma_Bit_and_inst25_out)
);
corebit_and magma_Bit_and_inst26 (
    .in0(magma_Bit_and_inst25_out),
    .in1(magma_Bit_not_inst35_out),
    .out(magma_Bit_and_inst26_out)
);
corebit_and magma_Bit_and_inst27 (
    .in0(magma_Bit_and_inst26_out),
    .in1(magma_Bit_not_inst36_out),
    .out(magma_Bit_and_inst27_out)
);
corebit_and magma_Bit_and_inst28 (
    .in0(magma_Bit_and_inst27_out),
    .in1(magma_Bit_not_inst37_out),
    .out(magma_Bit_and_inst28_out)
);
corebit_and magma_Bit_and_inst29 (
    .in0(magma_Bit_and_inst28_out),
    .in1(magma_Bit_not_inst38_out),
    .out(magma_Bit_and_inst29_out)
);
corebit_and magma_Bit_and_inst3 (
    .in0(N),
    .in1(magma_Bit_not_inst12_out),
    .out(magma_Bit_and_inst3_out)
);
corebit_and magma_Bit_and_inst30 (
    .in0(magma_Bit_and_inst29_out),
    .in1(magma_Bit_not_inst39_out),
    .out(magma_Bit_and_inst30_out)
);
corebit_and magma_Bit_and_inst31 (
    .in0(magma_Bit_and_inst30_out),
    .in1(magma_Bit_not_inst40_out),
    .out(magma_Bit_and_inst31_out)
);
corebit_and magma_Bit_and_inst32 (
    .in0(magma_Bit_and_inst31_out),
    .in1(magma_Bit_not_inst41_out),
    .out(magma_Bit_and_inst32_out)
);
corebit_and magma_Bit_and_inst33 (
    .in0(magma_Bit_and_inst32_out),
    .in1(magma_Bit_not_inst42_out),
    .out(magma_Bit_and_inst33_out)
);
corebit_and magma_Bit_and_inst34 (
    .in0(magma_Bit_and_inst33_out),
    .in1(magma_Bit_not_inst43_out),
    .out(magma_Bit_and_inst34_out)
);
corebit_and magma_Bit_and_inst35 (
    .in0(magma_Bit_and_inst34_out),
    .in1(magma_Bit_not_inst44_out),
    .out(magma_Bit_and_inst35_out)
);
corebit_and magma_Bit_and_inst36 (
    .in0(magma_Bit_and_inst35_out),
    .in1(magma_Bit_not_inst45_out),
    .out(magma_Bit_and_inst36_out)
);
corebit_and magma_Bit_and_inst37 (
    .in0(magma_Bits_5_eq_inst39_out),
    .in1(magma_Bit_not_inst46_out),
    .out(magma_Bit_and_inst37_out)
);
corebit_and magma_Bit_and_inst38 (
    .in0(magma_Bit_and_inst37_out),
    .in1(magma_Bit_not_inst47_out),
    .out(magma_Bit_and_inst38_out)
);
corebit_and magma_Bit_and_inst39 (
    .in0(magma_Bit_and_inst38_out),
    .in1(magma_Bit_not_inst48_out),
    .out(magma_Bit_and_inst39_out)
);
corebit_and magma_Bit_and_inst4 (
    .in0(magma_Bits_5_eq_inst0_out),
    .in1(magma_Bit_not_inst13_out),
    .out(magma_Bit_and_inst4_out)
);
corebit_and magma_Bit_and_inst40 (
    .in0(magma_Bit_and_inst39_out),
    .in1(magma_Bit_not_inst49_out),
    .out(magma_Bit_and_inst40_out)
);
corebit_and magma_Bit_and_inst41 (
    .in0(magma_Bit_and_inst40_out),
    .in1(magma_Bit_not_inst50_out),
    .out(magma_Bit_and_inst41_out)
);
corebit_and magma_Bit_and_inst42 (
    .in0(magma_Bit_and_inst41_out),
    .in1(magma_Bit_not_inst51_out),
    .out(magma_Bit_and_inst42_out)
);
corebit_and magma_Bit_and_inst43 (
    .in0(magma_Bit_and_inst42_out),
    .in1(magma_Bit_not_inst52_out),
    .out(magma_Bit_and_inst43_out)
);
corebit_and magma_Bit_and_inst44 (
    .in0(magma_Bit_and_inst43_out),
    .in1(magma_Bit_not_inst53_out),
    .out(magma_Bit_and_inst44_out)
);
corebit_and magma_Bit_and_inst45 (
    .in0(magma_Bit_and_inst44_out),
    .in1(magma_Bit_not_inst54_out),
    .out(magma_Bit_and_inst45_out)
);
corebit_and magma_Bit_and_inst46 (
    .in0(magma_Bit_and_inst45_out),
    .in1(magma_Bit_not_inst55_out),
    .out(magma_Bit_and_inst46_out)
);
corebit_and magma_Bit_and_inst47 (
    .in0(magma_Bit_and_inst46_out),
    .in1(magma_Bit_not_inst56_out),
    .out(magma_Bit_and_inst47_out)
);
corebit_and magma_Bit_and_inst48 (
    .in0(magma_Bit_and_inst47_out),
    .in1(magma_Bit_not_inst57_out),
    .out(magma_Bit_and_inst48_out)
);
corebit_and magma_Bit_and_inst49 (
    .in0(magma_Bit_and_inst48_out),
    .in1(magma_Bit_not_inst58_out),
    .out(magma_Bit_and_inst49_out)
);
corebit_and magma_Bit_and_inst5 (
    .in0(magma_Bit_and_inst4_out),
    .in1(magma_Bit_not_inst14_out),
    .out(magma_Bit_and_inst5_out)
);
corebit_and magma_Bit_and_inst50 (
    .in0(magma_Bit_and_inst49_out),
    .in1(magma_Bit_not_inst59_out),
    .out(magma_Bit_and_inst50_out)
);
corebit_and magma_Bit_and_inst51 (
    .in0(magma_Bit_and_inst50_out),
    .in1(magma_Bit_not_inst60_out),
    .out(magma_Bit_and_inst51_out)
);
corebit_and magma_Bit_and_inst52 (
    .in0(magma_Bits_5_eq_inst57_out),
    .in1(magma_Bit_not_inst61_out),
    .out(magma_Bit_and_inst52_out)
);
corebit_and magma_Bit_and_inst53 (
    .in0(magma_Bit_and_inst52_out),
    .in1(magma_Bit_not_inst62_out),
    .out(magma_Bit_and_inst53_out)
);
corebit_and magma_Bit_and_inst54 (
    .in0(magma_Bit_and_inst53_out),
    .in1(magma_Bit_not_inst63_out),
    .out(magma_Bit_and_inst54_out)
);
corebit_and magma_Bit_and_inst55 (
    .in0(magma_Bit_and_inst54_out),
    .in1(magma_Bit_not_inst64_out),
    .out(magma_Bit_and_inst55_out)
);
corebit_and magma_Bit_and_inst56 (
    .in0(magma_Bit_and_inst55_out),
    .in1(magma_Bit_not_inst65_out),
    .out(magma_Bit_and_inst56_out)
);
corebit_and magma_Bit_and_inst57 (
    .in0(magma_Bit_and_inst56_out),
    .in1(magma_Bit_not_inst66_out),
    .out(magma_Bit_and_inst57_out)
);
corebit_and magma_Bit_and_inst58 (
    .in0(magma_Bit_and_inst57_out),
    .in1(magma_Bit_not_inst67_out),
    .out(magma_Bit_and_inst58_out)
);
corebit_and magma_Bit_and_inst59 (
    .in0(magma_Bit_and_inst58_out),
    .in1(magma_Bit_not_inst68_out),
    .out(magma_Bit_and_inst59_out)
);
corebit_and magma_Bit_and_inst6 (
    .in0(magma_Bit_and_inst5_out),
    .in1(magma_Bit_not_inst15_out),
    .out(magma_Bit_and_inst6_out)
);
corebit_and magma_Bit_and_inst60 (
    .in0(magma_Bit_and_inst59_out),
    .in1(magma_Bit_not_inst69_out),
    .out(magma_Bit_and_inst60_out)
);
corebit_and magma_Bit_and_inst61 (
    .in0(magma_Bit_and_inst60_out),
    .in1(magma_Bit_not_inst70_out),
    .out(magma_Bit_and_inst61_out)
);
corebit_and magma_Bit_and_inst62 (
    .in0(magma_Bit_and_inst61_out),
    .in1(magma_Bit_not_inst71_out),
    .out(magma_Bit_and_inst62_out)
);
corebit_and magma_Bit_and_inst63 (
    .in0(magma_Bit_and_inst62_out),
    .in1(magma_Bit_not_inst72_out),
    .out(magma_Bit_and_inst63_out)
);
corebit_and magma_Bit_and_inst64 (
    .in0(magma_Bit_and_inst63_out),
    .in1(magma_Bit_not_inst73_out),
    .out(magma_Bit_and_inst64_out)
);
corebit_and magma_Bit_and_inst65 (
    .in0(magma_Bit_and_inst64_out),
    .in1(magma_Bit_not_inst74_out),
    .out(magma_Bit_and_inst65_out)
);
corebit_and magma_Bit_and_inst66 (
    .in0(magma_Bits_5_eq_inst74_out),
    .in1(magma_Bit_not_inst75_out),
    .out(magma_Bit_and_inst66_out)
);
corebit_and magma_Bit_and_inst67 (
    .in0(magma_Bit_and_inst66_out),
    .in1(magma_Bit_not_inst76_out),
    .out(magma_Bit_and_inst67_out)
);
corebit_and magma_Bit_and_inst68 (
    .in0(magma_Bit_and_inst67_out),
    .in1(magma_Bit_not_inst77_out),
    .out(magma_Bit_and_inst68_out)
);
corebit_and magma_Bit_and_inst69 (
    .in0(magma_Bit_and_inst68_out),
    .in1(magma_Bit_not_inst78_out),
    .out(magma_Bit_and_inst69_out)
);
corebit_and magma_Bit_and_inst7 (
    .in0(magma_Bit_and_inst6_out),
    .in1(magma_Bit_not_inst16_out),
    .out(magma_Bit_and_inst7_out)
);
corebit_and magma_Bit_and_inst70 (
    .in0(magma_Bit_and_inst69_out),
    .in1(magma_Bit_not_inst79_out),
    .out(magma_Bit_and_inst70_out)
);
corebit_and magma_Bit_and_inst71 (
    .in0(magma_Bit_and_inst70_out),
    .in1(magma_Bit_not_inst80_out),
    .out(magma_Bit_and_inst71_out)
);
corebit_and magma_Bit_and_inst72 (
    .in0(magma_Bit_and_inst71_out),
    .in1(magma_Bit_not_inst81_out),
    .out(magma_Bit_and_inst72_out)
);
corebit_and magma_Bit_and_inst73 (
    .in0(magma_Bit_and_inst72_out),
    .in1(magma_Bit_not_inst82_out),
    .out(magma_Bit_and_inst73_out)
);
corebit_and magma_Bit_and_inst74 (
    .in0(magma_Bit_and_inst73_out),
    .in1(magma_Bit_not_inst83_out),
    .out(magma_Bit_and_inst74_out)
);
corebit_and magma_Bit_and_inst75 (
    .in0(magma_Bit_and_inst74_out),
    .in1(magma_Bit_not_inst84_out),
    .out(magma_Bit_and_inst75_out)
);
corebit_and magma_Bit_and_inst76 (
    .in0(magma_Bit_and_inst75_out),
    .in1(magma_Bit_not_inst85_out),
    .out(magma_Bit_and_inst76_out)
);
corebit_and magma_Bit_and_inst77 (
    .in0(magma_Bit_and_inst76_out),
    .in1(magma_Bit_not_inst86_out),
    .out(magma_Bit_and_inst77_out)
);
corebit_and magma_Bit_and_inst78 (
    .in0(magma_Bit_and_inst77_out),
    .in1(magma_Bit_not_inst87_out),
    .out(magma_Bit_and_inst78_out)
);
corebit_and magma_Bit_and_inst79 (
    .in0(magma_Bits_5_eq_inst90_out),
    .in1(magma_Bit_not_inst88_out),
    .out(magma_Bit_and_inst79_out)
);
corebit_and magma_Bit_and_inst8 (
    .in0(magma_Bit_and_inst7_out),
    .in1(magma_Bit_not_inst17_out),
    .out(magma_Bit_and_inst8_out)
);
corebit_and magma_Bit_and_inst80 (
    .in0(magma_Bit_and_inst79_out),
    .in1(magma_Bit_not_inst89_out),
    .out(magma_Bit_and_inst80_out)
);
corebit_and magma_Bit_and_inst81 (
    .in0(magma_Bit_and_inst80_out),
    .in1(magma_Bit_not_inst90_out),
    .out(magma_Bit_and_inst81_out)
);
corebit_and magma_Bit_and_inst82 (
    .in0(magma_Bit_and_inst81_out),
    .in1(magma_Bit_not_inst91_out),
    .out(magma_Bit_and_inst82_out)
);
corebit_and magma_Bit_and_inst83 (
    .in0(magma_Bit_and_inst82_out),
    .in1(magma_Bit_not_inst92_out),
    .out(magma_Bit_and_inst83_out)
);
corebit_and magma_Bit_and_inst84 (
    .in0(magma_Bit_and_inst83_out),
    .in1(magma_Bit_not_inst93_out),
    .out(magma_Bit_and_inst84_out)
);
corebit_and magma_Bit_and_inst85 (
    .in0(magma_Bit_and_inst84_out),
    .in1(magma_Bit_not_inst94_out),
    .out(magma_Bit_and_inst85_out)
);
corebit_and magma_Bit_and_inst86 (
    .in0(magma_Bit_and_inst85_out),
    .in1(magma_Bit_not_inst95_out),
    .out(magma_Bit_and_inst86_out)
);
corebit_and magma_Bit_and_inst87 (
    .in0(magma_Bit_and_inst86_out),
    .in1(magma_Bit_not_inst96_out),
    .out(magma_Bit_and_inst87_out)
);
corebit_and magma_Bit_and_inst88 (
    .in0(magma_Bit_and_inst87_out),
    .in1(magma_Bit_not_inst97_out),
    .out(magma_Bit_and_inst88_out)
);
corebit_and magma_Bit_and_inst89 (
    .in0(magma_Bit_and_inst88_out),
    .in1(magma_Bit_not_inst98_out),
    .out(magma_Bit_and_inst89_out)
);
corebit_and magma_Bit_and_inst9 (
    .in0(magma_Bit_and_inst8_out),
    .in1(magma_Bit_not_inst18_out),
    .out(magma_Bit_and_inst9_out)
);
corebit_and magma_Bit_and_inst90 (
    .in0(magma_Bit_and_inst89_out),
    .in1(magma_Bit_not_inst99_out),
    .out(magma_Bit_and_inst90_out)
);
corebit_and magma_Bit_and_inst91 (
    .in0(magma_Bits_5_eq_inst105_out),
    .in1(magma_Bit_not_inst100_out),
    .out(magma_Bit_and_inst91_out)
);
corebit_and magma_Bit_and_inst92 (
    .in0(magma_Bit_and_inst91_out),
    .in1(magma_Bit_not_inst101_out),
    .out(magma_Bit_and_inst92_out)
);
corebit_and magma_Bit_and_inst93 (
    .in0(magma_Bit_and_inst92_out),
    .in1(magma_Bit_not_inst102_out),
    .out(magma_Bit_and_inst93_out)
);
corebit_and magma_Bit_and_inst94 (
    .in0(magma_Bit_and_inst93_out),
    .in1(magma_Bit_not_inst103_out),
    .out(magma_Bit_and_inst94_out)
);
corebit_and magma_Bit_and_inst95 (
    .in0(magma_Bit_and_inst94_out),
    .in1(magma_Bit_not_inst104_out),
    .out(magma_Bit_and_inst95_out)
);
corebit_and magma_Bit_and_inst96 (
    .in0(magma_Bit_and_inst95_out),
    .in1(magma_Bit_not_inst105_out),
    .out(magma_Bit_and_inst96_out)
);
corebit_and magma_Bit_and_inst97 (
    .in0(magma_Bit_and_inst96_out),
    .in1(magma_Bit_not_inst106_out),
    .out(magma_Bit_and_inst97_out)
);
corebit_and magma_Bit_and_inst98 (
    .in0(magma_Bit_and_inst97_out),
    .in1(magma_Bit_not_inst107_out),
    .out(magma_Bit_and_inst98_out)
);
corebit_and magma_Bit_and_inst99 (
    .in0(magma_Bit_and_inst98_out),
    .in1(magma_Bit_not_inst108_out),
    .out(magma_Bit_and_inst99_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(Z),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(C),
    .out(magma_Bit_not_inst1_out)
);
corebit_not magma_Bit_not_inst10 (
    .in(N),
    .out(magma_Bit_not_inst10_out)
);
corebit_not magma_Bit_not_inst100 (
    .in(magma_Bits_5_eq_inst106_out),
    .out(magma_Bit_not_inst100_out)
);
corebit_not magma_Bit_not_inst101 (
    .in(magma_Bits_5_eq_inst107_out),
    .out(magma_Bit_not_inst101_out)
);
corebit_not magma_Bit_not_inst102 (
    .in(magma_Bit_or_inst16_out),
    .out(magma_Bit_not_inst102_out)
);
corebit_not magma_Bit_not_inst103 (
    .in(magma_Bit_or_inst17_out),
    .out(magma_Bit_not_inst103_out)
);
corebit_not magma_Bit_not_inst104 (
    .in(magma_Bits_5_eq_inst112_out),
    .out(magma_Bit_not_inst104_out)
);
corebit_not magma_Bit_not_inst105 (
    .in(magma_Bits_5_eq_inst113_out),
    .out(magma_Bit_not_inst105_out)
);
corebit_not magma_Bit_not_inst106 (
    .in(magma_Bits_5_eq_inst114_out),
    .out(magma_Bit_not_inst106_out)
);
corebit_not magma_Bit_not_inst107 (
    .in(magma_Bits_5_eq_inst115_out),
    .out(magma_Bit_not_inst107_out)
);
corebit_not magma_Bit_not_inst108 (
    .in(magma_Bits_5_eq_inst116_out),
    .out(magma_Bit_not_inst108_out)
);
corebit_not magma_Bit_not_inst109 (
    .in(magma_Bits_5_eq_inst117_out),
    .out(magma_Bit_not_inst109_out)
);
corebit_not magma_Bit_not_inst11 (
    .in(Z),
    .out(magma_Bit_not_inst11_out)
);
corebit_not magma_Bit_not_inst110 (
    .in(magma_Bits_5_eq_inst118_out),
    .out(magma_Bit_not_inst110_out)
);
corebit_not magma_Bit_not_inst111 (
    .in(magma_Bits_5_eq_inst120_out),
    .out(magma_Bit_not_inst111_out)
);
corebit_not magma_Bit_not_inst112 (
    .in(magma_Bits_5_eq_inst121_out),
    .out(magma_Bit_not_inst112_out)
);
corebit_not magma_Bit_not_inst113 (
    .in(magma_Bit_or_inst18_out),
    .out(magma_Bit_not_inst113_out)
);
corebit_not magma_Bit_not_inst114 (
    .in(magma_Bit_or_inst19_out),
    .out(magma_Bit_not_inst114_out)
);
corebit_not magma_Bit_not_inst115 (
    .in(magma_Bits_5_eq_inst126_out),
    .out(magma_Bit_not_inst115_out)
);
corebit_not magma_Bit_not_inst116 (
    .in(magma_Bits_5_eq_inst127_out),
    .out(magma_Bit_not_inst116_out)
);
corebit_not magma_Bit_not_inst117 (
    .in(magma_Bits_5_eq_inst128_out),
    .out(magma_Bit_not_inst117_out)
);
corebit_not magma_Bit_not_inst118 (
    .in(magma_Bits_5_eq_inst129_out),
    .out(magma_Bit_not_inst118_out)
);
corebit_not magma_Bit_not_inst119 (
    .in(magma_Bits_5_eq_inst130_out),
    .out(magma_Bit_not_inst119_out)
);
corebit_not magma_Bit_not_inst12 (
    .in(Z),
    .out(magma_Bit_not_inst12_out)
);
corebit_not magma_Bit_not_inst120 (
    .in(magma_Bits_5_eq_inst131_out),
    .out(magma_Bit_not_inst120_out)
);
corebit_not magma_Bit_not_inst121 (
    .in(magma_Bits_5_eq_inst133_out),
    .out(magma_Bit_not_inst121_out)
);
corebit_not magma_Bit_not_inst122 (
    .in(magma_Bits_5_eq_inst134_out),
    .out(magma_Bit_not_inst122_out)
);
corebit_not magma_Bit_not_inst123 (
    .in(magma_Bit_or_inst20_out),
    .out(magma_Bit_not_inst123_out)
);
corebit_not magma_Bit_not_inst124 (
    .in(magma_Bit_or_inst21_out),
    .out(magma_Bit_not_inst124_out)
);
corebit_not magma_Bit_not_inst125 (
    .in(magma_Bits_5_eq_inst139_out),
    .out(magma_Bit_not_inst125_out)
);
corebit_not magma_Bit_not_inst126 (
    .in(magma_Bits_5_eq_inst140_out),
    .out(magma_Bit_not_inst126_out)
);
corebit_not magma_Bit_not_inst127 (
    .in(magma_Bits_5_eq_inst141_out),
    .out(magma_Bit_not_inst127_out)
);
corebit_not magma_Bit_not_inst128 (
    .in(magma_Bits_5_eq_inst142_out),
    .out(magma_Bit_not_inst128_out)
);
corebit_not magma_Bit_not_inst129 (
    .in(magma_Bits_5_eq_inst143_out),
    .out(magma_Bit_not_inst129_out)
);
corebit_not magma_Bit_not_inst13 (
    .in(magma_Bits_5_eq_inst1_out),
    .out(magma_Bit_not_inst13_out)
);
corebit_not magma_Bit_not_inst130 (
    .in(magma_Bits_5_eq_inst145_out),
    .out(magma_Bit_not_inst130_out)
);
corebit_not magma_Bit_not_inst131 (
    .in(magma_Bits_5_eq_inst146_out),
    .out(magma_Bit_not_inst131_out)
);
corebit_not magma_Bit_not_inst132 (
    .in(magma_Bit_or_inst22_out),
    .out(magma_Bit_not_inst132_out)
);
corebit_not magma_Bit_not_inst133 (
    .in(magma_Bit_or_inst23_out),
    .out(magma_Bit_not_inst133_out)
);
corebit_not magma_Bit_not_inst134 (
    .in(magma_Bits_5_eq_inst151_out),
    .out(magma_Bit_not_inst134_out)
);
corebit_not magma_Bit_not_inst135 (
    .in(magma_Bits_5_eq_inst152_out),
    .out(magma_Bit_not_inst135_out)
);
corebit_not magma_Bit_not_inst136 (
    .in(magma_Bits_5_eq_inst153_out),
    .out(magma_Bit_not_inst136_out)
);
corebit_not magma_Bit_not_inst137 (
    .in(magma_Bits_5_eq_inst154_out),
    .out(magma_Bit_not_inst137_out)
);
corebit_not magma_Bit_not_inst138 (
    .in(magma_Bits_5_eq_inst156_out),
    .out(magma_Bit_not_inst138_out)
);
corebit_not magma_Bit_not_inst139 (
    .in(magma_Bits_5_eq_inst157_out),
    .out(magma_Bit_not_inst139_out)
);
corebit_not magma_Bit_not_inst14 (
    .in(magma_Bits_5_eq_inst2_out),
    .out(magma_Bit_not_inst14_out)
);
corebit_not magma_Bit_not_inst140 (
    .in(magma_Bit_or_inst24_out),
    .out(magma_Bit_not_inst140_out)
);
corebit_not magma_Bit_not_inst141 (
    .in(magma_Bit_or_inst25_out),
    .out(magma_Bit_not_inst141_out)
);
corebit_not magma_Bit_not_inst142 (
    .in(magma_Bits_5_eq_inst162_out),
    .out(magma_Bit_not_inst142_out)
);
corebit_not magma_Bit_not_inst143 (
    .in(magma_Bits_5_eq_inst163_out),
    .out(magma_Bit_not_inst143_out)
);
corebit_not magma_Bit_not_inst144 (
    .in(magma_Bits_5_eq_inst164_out),
    .out(magma_Bit_not_inst144_out)
);
corebit_not magma_Bit_not_inst145 (
    .in(magma_Bits_5_eq_inst166_out),
    .out(magma_Bit_not_inst145_out)
);
corebit_not magma_Bit_not_inst146 (
    .in(magma_Bits_5_eq_inst167_out),
    .out(magma_Bit_not_inst146_out)
);
corebit_not magma_Bit_not_inst147 (
    .in(magma_Bit_or_inst26_out),
    .out(magma_Bit_not_inst147_out)
);
corebit_not magma_Bit_not_inst148 (
    .in(magma_Bit_or_inst27_out),
    .out(magma_Bit_not_inst148_out)
);
corebit_not magma_Bit_not_inst149 (
    .in(magma_Bits_5_eq_inst172_out),
    .out(magma_Bit_not_inst149_out)
);
corebit_not magma_Bit_not_inst15 (
    .in(magma_Bit_or_inst4_out),
    .out(magma_Bit_not_inst15_out)
);
corebit_not magma_Bit_not_inst150 (
    .in(magma_Bits_5_eq_inst173_out),
    .out(magma_Bit_not_inst150_out)
);
corebit_not magma_Bit_not_inst151 (
    .in(magma_Bits_5_eq_inst175_out),
    .out(magma_Bit_not_inst151_out)
);
corebit_not magma_Bit_not_inst152 (
    .in(magma_Bits_5_eq_inst176_out),
    .out(magma_Bit_not_inst152_out)
);
corebit_not magma_Bit_not_inst153 (
    .in(magma_Bit_or_inst28_out),
    .out(magma_Bit_not_inst153_out)
);
corebit_not magma_Bit_not_inst154 (
    .in(magma_Bit_or_inst29_out),
    .out(magma_Bit_not_inst154_out)
);
corebit_not magma_Bit_not_inst155 (
    .in(magma_Bits_5_eq_inst181_out),
    .out(magma_Bit_not_inst155_out)
);
corebit_not magma_Bit_not_inst156 (
    .in(magma_Bits_5_eq_inst183_out),
    .out(magma_Bit_not_inst156_out)
);
corebit_not magma_Bit_not_inst157 (
    .in(magma_Bits_5_eq_inst184_out),
    .out(magma_Bit_not_inst157_out)
);
corebit_not magma_Bit_not_inst158 (
    .in(magma_Bit_or_inst30_out),
    .out(magma_Bit_not_inst158_out)
);
corebit_not magma_Bit_not_inst159 (
    .in(magma_Bit_or_inst31_out),
    .out(magma_Bit_not_inst159_out)
);
corebit_not magma_Bit_not_inst16 (
    .in(magma_Bit_or_inst5_out),
    .out(magma_Bit_not_inst16_out)
);
corebit_not magma_Bit_not_inst160 (
    .in(magma_Bits_5_eq_inst191_out),
    .out(magma_Bit_not_inst160_out)
);
corebit_not magma_Bit_not_inst161 (
    .in(magma_Bits_5_eq_inst192_out),
    .out(magma_Bit_not_inst161_out)
);
corebit_not magma_Bit_not_inst162 (
    .in(magma_Bit_or_inst33_out),
    .out(magma_Bit_not_inst162_out)
);
corebit_not magma_Bit_not_inst163 (
    .in(magma_Bits_5_eq_inst197_out),
    .out(magma_Bit_not_inst163_out)
);
corebit_not magma_Bit_not_inst164 (
    .in(magma_Bits_5_eq_inst198_out),
    .out(magma_Bit_not_inst164_out)
);
corebit_not magma_Bit_not_inst165 (
    .in(magma_Bits_5_eq_inst200_out),
    .out(magma_Bit_not_inst165_out)
);
corebit_not magma_Bit_not_inst17 (
    .in(magma_Bits_5_eq_inst7_out),
    .out(magma_Bit_not_inst17_out)
);
corebit_not magma_Bit_not_inst18 (
    .in(magma_Bits_5_eq_inst8_out),
    .out(magma_Bit_not_inst18_out)
);
corebit_not magma_Bit_not_inst19 (
    .in(magma_Bits_5_eq_inst9_out),
    .out(magma_Bit_not_inst19_out)
);
corebit_not magma_Bit_not_inst2 (
    .in(N),
    .out(magma_Bit_not_inst2_out)
);
corebit_not magma_Bit_not_inst20 (
    .in(magma_Bits_5_eq_inst10_out),
    .out(magma_Bit_not_inst20_out)
);
corebit_not magma_Bit_not_inst21 (
    .in(magma_Bits_5_eq_inst11_out),
    .out(magma_Bit_not_inst21_out)
);
corebit_not magma_Bit_not_inst22 (
    .in(magma_Bits_5_eq_inst12_out),
    .out(magma_Bit_not_inst22_out)
);
corebit_not magma_Bit_not_inst23 (
    .in(magma_Bits_5_eq_inst13_out),
    .out(magma_Bit_not_inst23_out)
);
corebit_not magma_Bit_not_inst24 (
    .in(magma_Bits_5_eq_inst14_out),
    .out(magma_Bit_not_inst24_out)
);
corebit_not magma_Bit_not_inst25 (
    .in(magma_Bits_5_eq_inst15_out),
    .out(magma_Bit_not_inst25_out)
);
corebit_not magma_Bit_not_inst26 (
    .in(magma_Bits_5_eq_inst16_out),
    .out(magma_Bit_not_inst26_out)
);
corebit_not magma_Bit_not_inst27 (
    .in(magma_Bits_5_eq_inst17_out),
    .out(magma_Bit_not_inst27_out)
);
corebit_not magma_Bit_not_inst28 (
    .in(magma_Bits_5_eq_inst18_out),
    .out(magma_Bit_not_inst28_out)
);
corebit_not magma_Bit_not_inst29 (
    .in(magma_Bits_5_eq_inst19_out),
    .out(magma_Bit_not_inst29_out)
);
corebit_not magma_Bit_not_inst3 (
    .in(V),
    .out(magma_Bit_not_inst3_out)
);
corebit_not magma_Bit_not_inst30 (
    .in(magma_Bits_5_eq_inst21_out),
    .out(magma_Bit_not_inst30_out)
);
corebit_not magma_Bit_not_inst31 (
    .in(magma_Bits_5_eq_inst22_out),
    .out(magma_Bit_not_inst31_out)
);
corebit_not magma_Bit_not_inst32 (
    .in(magma_Bit_or_inst6_out),
    .out(magma_Bit_not_inst32_out)
);
corebit_not magma_Bit_not_inst33 (
    .in(magma_Bit_or_inst7_out),
    .out(magma_Bit_not_inst33_out)
);
corebit_not magma_Bit_not_inst34 (
    .in(magma_Bits_5_eq_inst27_out),
    .out(magma_Bit_not_inst34_out)
);
corebit_not magma_Bit_not_inst35 (
    .in(magma_Bits_5_eq_inst28_out),
    .out(magma_Bit_not_inst35_out)
);
corebit_not magma_Bit_not_inst36 (
    .in(magma_Bits_5_eq_inst29_out),
    .out(magma_Bit_not_inst36_out)
);
corebit_not magma_Bit_not_inst37 (
    .in(magma_Bits_5_eq_inst30_out),
    .out(magma_Bit_not_inst37_out)
);
corebit_not magma_Bit_not_inst38 (
    .in(magma_Bits_5_eq_inst31_out),
    .out(magma_Bit_not_inst38_out)
);
corebit_not magma_Bit_not_inst39 (
    .in(magma_Bits_5_eq_inst32_out),
    .out(magma_Bit_not_inst39_out)
);
corebit_not magma_Bit_not_inst4 (
    .in(Z),
    .out(magma_Bit_not_inst4_out)
);
corebit_not magma_Bit_not_inst40 (
    .in(magma_Bits_5_eq_inst33_out),
    .out(magma_Bit_not_inst40_out)
);
corebit_not magma_Bit_not_inst41 (
    .in(magma_Bits_5_eq_inst34_out),
    .out(magma_Bit_not_inst41_out)
);
corebit_not magma_Bit_not_inst42 (
    .in(magma_Bits_5_eq_inst35_out),
    .out(magma_Bit_not_inst42_out)
);
corebit_not magma_Bit_not_inst43 (
    .in(magma_Bits_5_eq_inst36_out),
    .out(magma_Bit_not_inst43_out)
);
corebit_not magma_Bit_not_inst44 (
    .in(magma_Bits_5_eq_inst37_out),
    .out(magma_Bit_not_inst44_out)
);
corebit_not magma_Bit_not_inst45 (
    .in(magma_Bits_5_eq_inst38_out),
    .out(magma_Bit_not_inst45_out)
);
corebit_not magma_Bit_not_inst46 (
    .in(magma_Bits_5_eq_inst40_out),
    .out(magma_Bit_not_inst46_out)
);
corebit_not magma_Bit_not_inst47 (
    .in(magma_Bits_5_eq_inst41_out),
    .out(magma_Bit_not_inst47_out)
);
corebit_not magma_Bit_not_inst48 (
    .in(magma_Bit_or_inst8_out),
    .out(magma_Bit_not_inst48_out)
);
corebit_not magma_Bit_not_inst49 (
    .in(magma_Bit_or_inst9_out),
    .out(magma_Bit_not_inst49_out)
);
corebit_not magma_Bit_not_inst5 (
    .in(C),
    .out(magma_Bit_not_inst5_out)
);
corebit_not magma_Bit_not_inst50 (
    .in(magma_Bits_5_eq_inst46_out),
    .out(magma_Bit_not_inst50_out)
);
corebit_not magma_Bit_not_inst51 (
    .in(magma_Bits_5_eq_inst47_out),
    .out(magma_Bit_not_inst51_out)
);
corebit_not magma_Bit_not_inst52 (
    .in(magma_Bits_5_eq_inst48_out),
    .out(magma_Bit_not_inst52_out)
);
corebit_not magma_Bit_not_inst53 (
    .in(magma_Bits_5_eq_inst49_out),
    .out(magma_Bit_not_inst53_out)
);
corebit_not magma_Bit_not_inst54 (
    .in(magma_Bits_5_eq_inst50_out),
    .out(magma_Bit_not_inst54_out)
);
corebit_not magma_Bit_not_inst55 (
    .in(magma_Bits_5_eq_inst51_out),
    .out(magma_Bit_not_inst55_out)
);
corebit_not magma_Bit_not_inst56 (
    .in(magma_Bits_5_eq_inst52_out),
    .out(magma_Bit_not_inst56_out)
);
corebit_not magma_Bit_not_inst57 (
    .in(magma_Bits_5_eq_inst53_out),
    .out(magma_Bit_not_inst57_out)
);
corebit_not magma_Bit_not_inst58 (
    .in(magma_Bits_5_eq_inst54_out),
    .out(magma_Bit_not_inst58_out)
);
corebit_not magma_Bit_not_inst59 (
    .in(magma_Bits_5_eq_inst55_out),
    .out(magma_Bit_not_inst59_out)
);
corebit_not magma_Bit_not_inst6 (
    .in(magma_Bit_xor_inst0_out),
    .out(magma_Bit_not_inst6_out)
);
corebit_not magma_Bit_not_inst60 (
    .in(magma_Bits_5_eq_inst56_out),
    .out(magma_Bit_not_inst60_out)
);
corebit_not magma_Bit_not_inst61 (
    .in(magma_Bits_5_eq_inst58_out),
    .out(magma_Bit_not_inst61_out)
);
corebit_not magma_Bit_not_inst62 (
    .in(magma_Bits_5_eq_inst59_out),
    .out(magma_Bit_not_inst62_out)
);
corebit_not magma_Bit_not_inst63 (
    .in(magma_Bit_or_inst10_out),
    .out(magma_Bit_not_inst63_out)
);
corebit_not magma_Bit_not_inst64 (
    .in(magma_Bit_or_inst11_out),
    .out(magma_Bit_not_inst64_out)
);
corebit_not magma_Bit_not_inst65 (
    .in(magma_Bits_5_eq_inst64_out),
    .out(magma_Bit_not_inst65_out)
);
corebit_not magma_Bit_not_inst66 (
    .in(magma_Bits_5_eq_inst65_out),
    .out(magma_Bit_not_inst66_out)
);
corebit_not magma_Bit_not_inst67 (
    .in(magma_Bits_5_eq_inst66_out),
    .out(magma_Bit_not_inst67_out)
);
corebit_not magma_Bit_not_inst68 (
    .in(magma_Bits_5_eq_inst67_out),
    .out(magma_Bit_not_inst68_out)
);
corebit_not magma_Bit_not_inst69 (
    .in(magma_Bits_5_eq_inst68_out),
    .out(magma_Bit_not_inst69_out)
);
corebit_not magma_Bit_not_inst7 (
    .in(Z),
    .out(magma_Bit_not_inst7_out)
);
corebit_not magma_Bit_not_inst70 (
    .in(magma_Bits_5_eq_inst69_out),
    .out(magma_Bit_not_inst70_out)
);
corebit_not magma_Bit_not_inst71 (
    .in(magma_Bits_5_eq_inst70_out),
    .out(magma_Bit_not_inst71_out)
);
corebit_not magma_Bit_not_inst72 (
    .in(magma_Bits_5_eq_inst71_out),
    .out(magma_Bit_not_inst72_out)
);
corebit_not magma_Bit_not_inst73 (
    .in(magma_Bits_5_eq_inst72_out),
    .out(magma_Bit_not_inst73_out)
);
corebit_not magma_Bit_not_inst74 (
    .in(magma_Bits_5_eq_inst73_out),
    .out(magma_Bit_not_inst74_out)
);
corebit_not magma_Bit_not_inst75 (
    .in(magma_Bits_5_eq_inst75_out),
    .out(magma_Bit_not_inst75_out)
);
corebit_not magma_Bit_not_inst76 (
    .in(magma_Bits_5_eq_inst76_out),
    .out(magma_Bit_not_inst76_out)
);
corebit_not magma_Bit_not_inst77 (
    .in(magma_Bit_or_inst12_out),
    .out(magma_Bit_not_inst77_out)
);
corebit_not magma_Bit_not_inst78 (
    .in(magma_Bit_or_inst13_out),
    .out(magma_Bit_not_inst78_out)
);
corebit_not magma_Bit_not_inst79 (
    .in(magma_Bits_5_eq_inst81_out),
    .out(magma_Bit_not_inst79_out)
);
corebit_not magma_Bit_not_inst8 (
    .in(magma_Bit_xor_inst2_out),
    .out(magma_Bit_not_inst8_out)
);
corebit_not magma_Bit_not_inst80 (
    .in(magma_Bits_5_eq_inst82_out),
    .out(magma_Bit_not_inst80_out)
);
corebit_not magma_Bit_not_inst81 (
    .in(magma_Bits_5_eq_inst83_out),
    .out(magma_Bit_not_inst81_out)
);
corebit_not magma_Bit_not_inst82 (
    .in(magma_Bits_5_eq_inst84_out),
    .out(magma_Bit_not_inst82_out)
);
corebit_not magma_Bit_not_inst83 (
    .in(magma_Bits_5_eq_inst85_out),
    .out(magma_Bit_not_inst83_out)
);
corebit_not magma_Bit_not_inst84 (
    .in(magma_Bits_5_eq_inst86_out),
    .out(magma_Bit_not_inst84_out)
);
corebit_not magma_Bit_not_inst85 (
    .in(magma_Bits_5_eq_inst87_out),
    .out(magma_Bit_not_inst85_out)
);
corebit_not magma_Bit_not_inst86 (
    .in(magma_Bits_5_eq_inst88_out),
    .out(magma_Bit_not_inst86_out)
);
corebit_not magma_Bit_not_inst87 (
    .in(magma_Bits_5_eq_inst89_out),
    .out(magma_Bit_not_inst87_out)
);
corebit_not magma_Bit_not_inst88 (
    .in(magma_Bits_5_eq_inst91_out),
    .out(magma_Bit_not_inst88_out)
);
corebit_not magma_Bit_not_inst89 (
    .in(magma_Bits_5_eq_inst92_out),
    .out(magma_Bit_not_inst89_out)
);
corebit_not magma_Bit_not_inst9 (
    .in(N),
    .out(magma_Bit_not_inst9_out)
);
corebit_not magma_Bit_not_inst90 (
    .in(magma_Bit_or_inst14_out),
    .out(magma_Bit_not_inst90_out)
);
corebit_not magma_Bit_not_inst91 (
    .in(magma_Bit_or_inst15_out),
    .out(magma_Bit_not_inst91_out)
);
corebit_not magma_Bit_not_inst92 (
    .in(magma_Bits_5_eq_inst97_out),
    .out(magma_Bit_not_inst92_out)
);
corebit_not magma_Bit_not_inst93 (
    .in(magma_Bits_5_eq_inst98_out),
    .out(magma_Bit_not_inst93_out)
);
corebit_not magma_Bit_not_inst94 (
    .in(magma_Bits_5_eq_inst99_out),
    .out(magma_Bit_not_inst94_out)
);
corebit_not magma_Bit_not_inst95 (
    .in(magma_Bits_5_eq_inst100_out),
    .out(magma_Bit_not_inst95_out)
);
corebit_not magma_Bit_not_inst96 (
    .in(magma_Bits_5_eq_inst101_out),
    .out(magma_Bit_not_inst96_out)
);
corebit_not magma_Bit_not_inst97 (
    .in(magma_Bits_5_eq_inst102_out),
    .out(magma_Bit_not_inst97_out)
);
corebit_not magma_Bit_not_inst98 (
    .in(magma_Bits_5_eq_inst103_out),
    .out(magma_Bit_not_inst98_out)
);
corebit_not magma_Bit_not_inst99 (
    .in(magma_Bits_5_eq_inst104_out),
    .out(magma_Bit_not_inst99_out)
);
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bit_not_inst5_out),
    .in1(Z),
    .out(magma_Bit_or_inst0_out)
);
corebit_or magma_Bit_or_inst1 (
    .in0(Z),
    .in1(magma_Bit_xor_inst3_out),
    .out(magma_Bit_or_inst1_out)
);
corebit_or magma_Bit_or_inst10 (
    .in0(magma_Bits_5_eq_inst60_out),
    .in1(magma_Bits_5_eq_inst61_out),
    .out(magma_Bit_or_inst10_out)
);
corebit_or magma_Bit_or_inst11 (
    .in0(magma_Bits_5_eq_inst62_out),
    .in1(magma_Bits_5_eq_inst63_out),
    .out(magma_Bit_or_inst11_out)
);
corebit_or magma_Bit_or_inst12 (
    .in0(magma_Bits_5_eq_inst77_out),
    .in1(magma_Bits_5_eq_inst78_out),
    .out(magma_Bit_or_inst12_out)
);
corebit_or magma_Bit_or_inst13 (
    .in0(magma_Bits_5_eq_inst79_out),
    .in1(magma_Bits_5_eq_inst80_out),
    .out(magma_Bit_or_inst13_out)
);
corebit_or magma_Bit_or_inst14 (
    .in0(magma_Bits_5_eq_inst93_out),
    .in1(magma_Bits_5_eq_inst94_out),
    .out(magma_Bit_or_inst14_out)
);
corebit_or magma_Bit_or_inst15 (
    .in0(magma_Bits_5_eq_inst95_out),
    .in1(magma_Bits_5_eq_inst96_out),
    .out(magma_Bit_or_inst15_out)
);
corebit_or magma_Bit_or_inst16 (
    .in0(magma_Bits_5_eq_inst108_out),
    .in1(magma_Bits_5_eq_inst109_out),
    .out(magma_Bit_or_inst16_out)
);
corebit_or magma_Bit_or_inst17 (
    .in0(magma_Bits_5_eq_inst110_out),
    .in1(magma_Bits_5_eq_inst111_out),
    .out(magma_Bit_or_inst17_out)
);
corebit_or magma_Bit_or_inst18 (
    .in0(magma_Bits_5_eq_inst122_out),
    .in1(magma_Bits_5_eq_inst123_out),
    .out(magma_Bit_or_inst18_out)
);
corebit_or magma_Bit_or_inst19 (
    .in0(magma_Bits_5_eq_inst124_out),
    .in1(magma_Bits_5_eq_inst125_out),
    .out(magma_Bit_or_inst19_out)
);
corebit_or magma_Bit_or_inst2 (
    .in0(magma_Bit_not_inst9_out),
    .in1(Z),
    .out(magma_Bit_or_inst2_out)
);
corebit_or magma_Bit_or_inst20 (
    .in0(magma_Bits_5_eq_inst135_out),
    .in1(magma_Bits_5_eq_inst136_out),
    .out(magma_Bit_or_inst20_out)
);
corebit_or magma_Bit_or_inst21 (
    .in0(magma_Bits_5_eq_inst137_out),
    .in1(magma_Bits_5_eq_inst138_out),
    .out(magma_Bit_or_inst21_out)
);
corebit_or magma_Bit_or_inst22 (
    .in0(magma_Bits_5_eq_inst147_out),
    .in1(magma_Bits_5_eq_inst148_out),
    .out(magma_Bit_or_inst22_out)
);
corebit_or magma_Bit_or_inst23 (
    .in0(magma_Bits_5_eq_inst149_out),
    .in1(magma_Bits_5_eq_inst150_out),
    .out(magma_Bit_or_inst23_out)
);
corebit_or magma_Bit_or_inst24 (
    .in0(magma_Bits_5_eq_inst158_out),
    .in1(magma_Bits_5_eq_inst159_out),
    .out(magma_Bit_or_inst24_out)
);
corebit_or magma_Bit_or_inst25 (
    .in0(magma_Bits_5_eq_inst160_out),
    .in1(magma_Bits_5_eq_inst161_out),
    .out(magma_Bit_or_inst25_out)
);
corebit_or magma_Bit_or_inst26 (
    .in0(magma_Bits_5_eq_inst168_out),
    .in1(magma_Bits_5_eq_inst169_out),
    .out(magma_Bit_or_inst26_out)
);
corebit_or magma_Bit_or_inst27 (
    .in0(magma_Bits_5_eq_inst170_out),
    .in1(magma_Bits_5_eq_inst171_out),
    .out(magma_Bit_or_inst27_out)
);
corebit_or magma_Bit_or_inst28 (
    .in0(magma_Bits_5_eq_inst177_out),
    .in1(magma_Bits_5_eq_inst178_out),
    .out(magma_Bit_or_inst28_out)
);
corebit_or magma_Bit_or_inst29 (
    .in0(magma_Bits_5_eq_inst179_out),
    .in1(magma_Bits_5_eq_inst180_out),
    .out(magma_Bit_or_inst29_out)
);
corebit_or magma_Bit_or_inst3 (
    .in0(N),
    .in1(Z),
    .out(magma_Bit_or_inst3_out)
);
corebit_or magma_Bit_or_inst30 (
    .in0(magma_Bits_5_eq_inst185_out),
    .in1(magma_Bits_5_eq_inst186_out),
    .out(magma_Bit_or_inst30_out)
);
corebit_or magma_Bit_or_inst31 (
    .in0(magma_Bits_5_eq_inst187_out),
    .in1(magma_Bits_5_eq_inst188_out),
    .out(magma_Bit_or_inst31_out)
);
corebit_or magma_Bit_or_inst32 (
    .in0(magma_Bits_5_eq_inst189_out),
    .in1(magma_Bits_5_eq_inst190_out),
    .out(magma_Bit_or_inst32_out)
);
corebit_or magma_Bit_or_inst33 (
    .in0(magma_Bits_5_eq_inst193_out),
    .in1(magma_Bits_5_eq_inst194_out),
    .out(magma_Bit_or_inst33_out)
);
corebit_or magma_Bit_or_inst34 (
    .in0(magma_Bits_5_eq_inst195_out),
    .in1(magma_Bits_5_eq_inst196_out),
    .out(magma_Bit_or_inst34_out)
);
corebit_or magma_Bit_or_inst4 (
    .in0(magma_Bits_5_eq_inst3_out),
    .in1(magma_Bits_5_eq_inst4_out),
    .out(magma_Bit_or_inst4_out)
);
corebit_or magma_Bit_or_inst5 (
    .in0(magma_Bits_5_eq_inst5_out),
    .in1(magma_Bits_5_eq_inst6_out),
    .out(magma_Bit_or_inst5_out)
);
corebit_or magma_Bit_or_inst6 (
    .in0(magma_Bits_5_eq_inst23_out),
    .in1(magma_Bits_5_eq_inst24_out),
    .out(magma_Bit_or_inst6_out)
);
corebit_or magma_Bit_or_inst7 (
    .in0(magma_Bits_5_eq_inst25_out),
    .in1(magma_Bits_5_eq_inst26_out),
    .out(magma_Bit_or_inst7_out)
);
corebit_or magma_Bit_or_inst8 (
    .in0(magma_Bits_5_eq_inst42_out),
    .in1(magma_Bits_5_eq_inst43_out),
    .out(magma_Bit_or_inst8_out)
);
corebit_or magma_Bit_or_inst9 (
    .in0(magma_Bits_5_eq_inst44_out),
    .in1(magma_Bits_5_eq_inst45_out),
    .out(magma_Bit_or_inst9_out)
);
corebit_xor magma_Bit_xor_inst0 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst0_out)
);
corebit_xor magma_Bit_xor_inst1 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst1_out)
);
corebit_xor magma_Bit_xor_inst2 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst2_out)
);
corebit_xor magma_Bit_xor_inst3 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst3_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst0 (
    .in0(code),
    .in1(const_17_5_out),
    .out(magma_Bits_5_eq_inst0_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst1 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst1_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst10 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst10_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst100 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst100_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst101 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst101_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst102 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst102_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst103 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst103_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst104 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst104_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst105 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst105_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst106 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst106_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst107 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst107_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst108 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst108_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst109 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst109_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst11 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst11_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst110 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst110_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst111 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst111_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst112 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst112_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst113 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst113_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst114 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst114_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst115 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst115_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst116 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst116_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst117 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst117_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst118 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst118_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst119 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst119_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst12 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst12_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst120 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst120_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst121 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst121_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst122 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst122_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst123 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst123_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst124 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst124_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst125 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst125_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst126 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst126_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst127 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst127_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst128 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst128_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst129 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst129_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst13 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst13_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst130 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst130_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst131 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst131_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst132 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst132_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst133 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst133_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst134 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst134_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst135 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst135_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst136 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst136_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst137 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst137_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst138 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst138_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst139 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst139_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst14 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst14_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst140 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst140_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst141 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst141_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst142 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst142_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst143 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst143_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst144 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst144_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst145 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst145_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst146 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst146_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst147 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst147_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst148 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst148_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst149 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst149_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst15 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst15_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst150 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst150_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst151 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst151_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst152 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst152_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst153 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst153_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst154 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst154_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst155 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst155_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst156 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst156_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst157 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst157_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst158 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst158_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst159 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst159_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst16 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst16_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst160 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst160_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst161 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst161_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst162 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst162_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst163 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst163_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst164 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst164_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst165 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst165_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst166 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst166_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst167 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst167_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst168 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst168_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst169 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst169_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst17 (
    .in0(code),
    .in1(const_14_5_out),
    .out(magma_Bits_5_eq_inst17_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst170 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst170_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst171 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst171_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst172 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst172_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst173 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst173_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst174 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst174_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst175 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst175_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst176 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst176_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst177 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst177_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst178 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst178_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst179 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst179_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst18 (
    .in0(code),
    .in1(const_15_5_out),
    .out(magma_Bits_5_eq_inst18_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst180 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst180_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst181 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst181_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst182 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst182_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst183 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst183_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst184 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst184_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst185 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst185_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst186 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst186_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst187 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst187_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst188 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst188_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst189 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst189_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst19 (
    .in0(code),
    .in1(const_16_5_out),
    .out(magma_Bits_5_eq_inst19_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst190 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst190_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst191 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst191_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst192 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst192_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst193 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst193_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst194 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst194_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst195 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst195_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst196 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst196_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst197 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst197_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst198 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst198_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst199 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst199_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst2 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst2_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst20 (
    .in0(code),
    .in1(const_16_5_out),
    .out(magma_Bits_5_eq_inst20_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst200 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst200_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst201 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst201_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst21 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst21_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst22 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst22_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst23 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst23_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst24 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst24_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst25 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst25_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst26 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst26_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst27 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst27_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst28 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst28_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst29 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst29_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst3 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst3_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst30 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst30_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst31 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst31_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst32 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst32_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst33 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst33_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst34 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst34_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst35 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst35_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst36 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst36_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst37 (
    .in0(code),
    .in1(const_14_5_out),
    .out(magma_Bits_5_eq_inst37_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst38 (
    .in0(code),
    .in1(const_15_5_out),
    .out(magma_Bits_5_eq_inst38_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst39 (
    .in0(code),
    .in1(const_15_5_out),
    .out(magma_Bits_5_eq_inst39_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst4 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst4_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst40 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst40_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst41 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst41_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst42 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst42_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst43 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst43_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst44 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst44_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst45 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst45_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst46 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst46_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst47 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst47_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst48 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst48_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst49 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst49_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst5 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst5_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst50 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst50_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst51 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst51_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst52 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst52_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst53 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst53_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst54 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst54_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst55 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst55_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst56 (
    .in0(code),
    .in1(const_14_5_out),
    .out(magma_Bits_5_eq_inst56_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst57 (
    .in0(code),
    .in1(const_14_5_out),
    .out(magma_Bits_5_eq_inst57_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst58 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst58_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst59 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst59_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst6 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst6_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst60 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst60_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst61 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst61_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst62 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst62_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst63 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst63_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst64 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst64_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst65 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst65_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst66 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst66_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst67 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst67_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst68 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst68_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst69 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst69_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst7 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst7_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst70 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst70_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst71 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst71_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst72 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst72_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst73 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst73_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst74 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst74_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst75 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst75_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst76 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst76_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst77 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst77_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst78 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst78_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst79 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst79_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst8 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst8_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst80 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst80_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst81 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst81_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst82 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst82_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst83 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst83_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst84 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst84_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst85 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst85_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst86 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst86_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst87 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst87_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst88 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst88_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst89 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst89_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst9 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst9_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst90 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst90_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst91 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst91_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst92 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst92_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst93 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst93_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst94 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst94_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst95 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst95_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst96 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst96_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst97 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst97_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst98 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst98_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst99 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst99_out)
);
assign O = Mux2xBit_inst17_O;
endmodule

module Cond (
    input [4:0] code,
    input alu,
    input Z,
    input N,
    input C,
    input V,
    input CLK,
    input ASYNCRESET,
    output O
);
wire Cond_comb_inst0_O;
Cond_comb Cond_comb_inst0 (
    .code(code),
    .alu(alu),
    .Z(Z),
    .N(N),
    .C(C),
    .V(V),
    .O(Cond_comb_inst0_O)
);
assign O = Cond_comb_inst0_O;
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
    input [49:0] inst,
    input [50:0] inputs,
    input clk_en,
    input CLK,
    input ASYNCRESET,
    output [16:0] O
);
wire [15:0] ADD_inst0_O0;
wire ADD_inst0_O1;
wire ADD_inst0_O2;
wire ADD_inst0_O3;
wire ADD_inst0_O4;
wire ADD_inst0_O5;
wire [15:0] ADD_inst1_O0;
wire ADD_inst1_O1;
wire ADD_inst1_O2;
wire ADD_inst1_O3;
wire ADD_inst1_O4;
wire ADD_inst1_O5;
wire Cond_inst0_O;
wire Cond_inst1_O;
wire Cond_inst2_O;
wire [15:0] GTE_inst0_O0;
wire GTE_inst0_O1;
wire GTE_inst0_O2;
wire GTE_inst0_O3;
wire GTE_inst0_O4;
wire GTE_inst0_O5;
wire [15:0] LTE_inst0_O0;
wire LTE_inst0_O1;
wire LTE_inst0_O2;
wire LTE_inst0_O3;
wire LTE_inst0_O4;
wire LTE_inst0_O5;
wire LUT_inst0_O;
wire [15:0] MUL_inst0_O;
wire [15:0] Mux_inst0_O;
wire [15:0] PE_comb_inst0_O0;
wire [15:0] PE_comb_inst0_O1;
wire [15:0] PE_comb_inst0_O2;
wire [15:0] PE_comb_inst0_O3;
wire [0:0] PE_comb_inst0_O4;
wire [15:0] PE_comb_inst0_O5;
wire [15:0] PE_comb_inst0_O6;
wire [4:0] PE_comb_inst0_O7;
wire PE_comb_inst0_O8;
wire PE_comb_inst0_O9;
wire PE_comb_inst0_O10;
wire PE_comb_inst0_O11;
wire PE_comb_inst0_O12;
wire [0:0] PE_comb_inst0_O13;
wire [15:0] PE_comb_inst0_O14;
wire [15:0] PE_comb_inst0_O15;
wire [4:0] PE_comb_inst0_O16;
wire PE_comb_inst0_O17;
wire PE_comb_inst0_O18;
wire PE_comb_inst0_O19;
wire PE_comb_inst0_O20;
wire PE_comb_inst0_O21;
wire [0:0] PE_comb_inst0_O22;
wire [0:0] PE_comb_inst0_O23;
wire [15:0] PE_comb_inst0_O24;
wire [15:0] PE_comb_inst0_O25;
wire [7:0] PE_comb_inst0_O26;
wire PE_comb_inst0_O27;
wire PE_comb_inst0_O28;
wire PE_comb_inst0_O29;
wire [15:0] PE_comb_inst0_O30;
wire [15:0] PE_comb_inst0_O31;
wire [4:0] PE_comb_inst0_O32;
wire PE_comb_inst0_O33;
wire PE_comb_inst0_O34;
wire PE_comb_inst0_O35;
wire PE_comb_inst0_O36;
wire PE_comb_inst0_O37;
wire [15:0] PE_comb_inst0_O38;
wire [15:0] PE_comb_inst0_O39;
wire PE_comb_inst0_O40;
wire [0:0] PE_comb_inst0_O41;
wire [15:0] PE_comb_inst0_O42;
wire [15:0] PE_comb_inst0_O43;
wire [16:0] PE_comb_inst0_O44;
wire [15:0] SHR_inst0_O0;
wire SHR_inst0_O1;
wire SHR_inst0_O2;
wire SHR_inst0_O3;
wire SHR_inst0_O4;
wire SHR_inst0_O5;
wire [15:0] SUB_inst0_O0;
wire SUB_inst0_O1;
wire SUB_inst0_O2;
wire SUB_inst0_O3;
wire SUB_inst0_O4;
wire SUB_inst0_O5;
ADD ADD_inst0 (
    .a(PE_comb_inst0_O0),
    .b(PE_comb_inst0_O1),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(ADD_inst0_O0),
    .O1(ADD_inst0_O1),
    .O2(ADD_inst0_O2),
    .O3(ADD_inst0_O3),
    .O4(ADD_inst0_O4),
    .O5(ADD_inst0_O5)
);
ADD ADD_inst1 (
    .a(PE_comb_inst0_O2),
    .b(PE_comb_inst0_O3),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(ADD_inst1_O0),
    .O1(ADD_inst1_O1),
    .O2(ADD_inst1_O2),
    .O3(ADD_inst1_O3),
    .O4(ADD_inst1_O4),
    .O5(ADD_inst1_O5)
);
Cond Cond_inst0 (
    .code(PE_comb_inst0_O7),
    .alu(PE_comb_inst0_O8),
    .Z(PE_comb_inst0_O9),
    .N(PE_comb_inst0_O10),
    .C(PE_comb_inst0_O11),
    .V(PE_comb_inst0_O12),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Cond_inst0_O)
);
Cond Cond_inst1 (
    .code(PE_comb_inst0_O16),
    .alu(PE_comb_inst0_O17),
    .Z(PE_comb_inst0_O18),
    .N(PE_comb_inst0_O19),
    .C(PE_comb_inst0_O20),
    .V(PE_comb_inst0_O21),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Cond_inst1_O)
);
Cond Cond_inst2 (
    .code(PE_comb_inst0_O32),
    .alu(PE_comb_inst0_O33),
    .Z(PE_comb_inst0_O34),
    .N(PE_comb_inst0_O35),
    .C(PE_comb_inst0_O36),
    .V(PE_comb_inst0_O37),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Cond_inst2_O)
);
GTE GTE_inst0 (
    .signed_(PE_comb_inst0_O4),
    .a(PE_comb_inst0_O5),
    .b(PE_comb_inst0_O6),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(GTE_inst0_O0),
    .O1(GTE_inst0_O1),
    .O2(GTE_inst0_O2),
    .O3(GTE_inst0_O3),
    .O4(GTE_inst0_O4),
    .O5(GTE_inst0_O5)
);
LTE LTE_inst0 (
    .signed_(PE_comb_inst0_O13),
    .a(PE_comb_inst0_O14),
    .b(PE_comb_inst0_O15),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(LTE_inst0_O0),
    .O1(LTE_inst0_O1),
    .O2(LTE_inst0_O2),
    .O3(LTE_inst0_O3),
    .O4(LTE_inst0_O4),
    .O5(LTE_inst0_O5)
);
LUT LUT_inst0 (
    .lut(PE_comb_inst0_O26),
    .bit0(PE_comb_inst0_O27),
    .bit1(PE_comb_inst0_O28),
    .bit2(PE_comb_inst0_O29),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(LUT_inst0_O)
);
MUL MUL_inst0 (
    .instr(PE_comb_inst0_O22),
    .signed_(PE_comb_inst0_O23),
    .a(PE_comb_inst0_O24),
    .b(PE_comb_inst0_O25),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(MUL_inst0_O)
);
Mux Mux_inst0 (
    .a(PE_comb_inst0_O38),
    .b(PE_comb_inst0_O39),
    .sel(PE_comb_inst0_O40),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Mux_inst0_O)
);
PE_comb PE_comb_inst0 (
    .inst(inst),
    .inputs(inputs),
    .clk_en(clk_en),
    .self_modules_0_O0(ADD_inst0_O0),
    .self_modules_0_O1(ADD_inst0_O1),
    .self_modules_0_O2(ADD_inst0_O2),
    .self_modules_0_O3(ADD_inst0_O3),
    .self_modules_0_O4(ADD_inst0_O4),
    .self_modules_0_O5(ADD_inst0_O5),
    .self_modules_1_O0(ADD_inst1_O0),
    .self_modules_1_O1(ADD_inst1_O1),
    .self_modules_1_O2(ADD_inst1_O2),
    .self_modules_1_O3(ADD_inst1_O3),
    .self_modules_1_O4(ADD_inst1_O4),
    .self_modules_1_O5(ADD_inst1_O5),
    .self_modules_2_O0(GTE_inst0_O0),
    .self_modules_2_O1(GTE_inst0_O1),
    .self_modules_2_O2(GTE_inst0_O2),
    .self_modules_2_O3(GTE_inst0_O3),
    .self_modules_2_O4(GTE_inst0_O4),
    .self_modules_2_O5(GTE_inst0_O5),
    .self_cond_2_O(Cond_inst0_O),
    .self_modules_3_O0(LTE_inst0_O0),
    .self_modules_3_O1(LTE_inst0_O1),
    .self_modules_3_O2(LTE_inst0_O2),
    .self_modules_3_O3(LTE_inst0_O3),
    .self_modules_3_O4(LTE_inst0_O4),
    .self_modules_3_O5(LTE_inst0_O5),
    .self_cond_3_O(Cond_inst1_O),
    .self_modules_4_O(MUL_inst0_O),
    .self_modules_5_O(LUT_inst0_O),
    .self_modules_6_O0(SUB_inst0_O0),
    .self_modules_6_O1(SUB_inst0_O1),
    .self_modules_6_O2(SUB_inst0_O2),
    .self_modules_6_O3(SUB_inst0_O3),
    .self_modules_6_O4(SUB_inst0_O4),
    .self_modules_6_O5(SUB_inst0_O5),
    .self_cond_6_O(Cond_inst2_O),
    .self_modules_7_O(Mux_inst0_O),
    .self_modules_8_O0(SHR_inst0_O0),
    .self_modules_8_O1(SHR_inst0_O1),
    .self_modules_8_O2(SHR_inst0_O2),
    .self_modules_8_O3(SHR_inst0_O3),
    .self_modules_8_O4(SHR_inst0_O4),
    .self_modules_8_O5(SHR_inst0_O5),
    .O0(PE_comb_inst0_O0),
    .O1(PE_comb_inst0_O1),
    .O2(PE_comb_inst0_O2),
    .O3(PE_comb_inst0_O3),
    .O4(PE_comb_inst0_O4),
    .O5(PE_comb_inst0_O5),
    .O6(PE_comb_inst0_O6),
    .O7(PE_comb_inst0_O7),
    .O8(PE_comb_inst0_O8),
    .O9(PE_comb_inst0_O9),
    .O10(PE_comb_inst0_O10),
    .O11(PE_comb_inst0_O11),
    .O12(PE_comb_inst0_O12),
    .O13(PE_comb_inst0_O13),
    .O14(PE_comb_inst0_O14),
    .O15(PE_comb_inst0_O15),
    .O16(PE_comb_inst0_O16),
    .O17(PE_comb_inst0_O17),
    .O18(PE_comb_inst0_O18),
    .O19(PE_comb_inst0_O19),
    .O20(PE_comb_inst0_O20),
    .O21(PE_comb_inst0_O21),
    .O22(PE_comb_inst0_O22),
    .O23(PE_comb_inst0_O23),
    .O24(PE_comb_inst0_O24),
    .O25(PE_comb_inst0_O25),
    .O26(PE_comb_inst0_O26),
    .O27(PE_comb_inst0_O27),
    .O28(PE_comb_inst0_O28),
    .O29(PE_comb_inst0_O29),
    .O30(PE_comb_inst0_O30),
    .O31(PE_comb_inst0_O31),
    .O32(PE_comb_inst0_O32),
    .O33(PE_comb_inst0_O33),
    .O34(PE_comb_inst0_O34),
    .O35(PE_comb_inst0_O35),
    .O36(PE_comb_inst0_O36),
    .O37(PE_comb_inst0_O37),
    .O38(PE_comb_inst0_O38),
    .O39(PE_comb_inst0_O39),
    .O40(PE_comb_inst0_O40),
    .O41(PE_comb_inst0_O41),
    .O42(PE_comb_inst0_O42),
    .O43(PE_comb_inst0_O43),
    .O44(PE_comb_inst0_O44)
);
SHR SHR_inst0 (
    .signed_(PE_comb_inst0_O41),
    .a(PE_comb_inst0_O42),
    .b(PE_comb_inst0_O43),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(SHR_inst0_O0),
    .O1(SHR_inst0_O1),
    .O2(SHR_inst0_O2),
    .O3(SHR_inst0_O3),
    .O4(SHR_inst0_O4),
    .O5(SHR_inst0_O5)
);
SUB SUB_inst0 (
    .a(PE_comb_inst0_O30),
    .b(PE_comb_inst0_O31),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(SUB_inst0_O0),
    .O1(SUB_inst0_O1),
    .O2(SUB_inst0_O2),
    .O3(SUB_inst0_O3),
    .O4(SUB_inst0_O4),
    .O5(SUB_inst0_O5)
);
assign O = PE_comb_inst0_O44;
endmodule

