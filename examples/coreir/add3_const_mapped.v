// Module `mul` defined externally
// Module `add` defined externally
module coreir_reg_arst #(
    parameter width = 1,
    parameter arst_posedge = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input arst,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
  end
  assign out = outReg;
endmodule

module Mux2xOutUInt8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
reg [7:0] coreir_commonlib_mux2x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x8_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x8_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Mux2xOutUInt32 (
    input [31:0] I0,
    input [31:0] I1,
    input S,
    output [31:0] O
);
reg [31:0] coreir_commonlib_mux2x32_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x32_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x32_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x32_inst0_out;
endmodule

module Mux2xOutUInt23 (
    input [22:0] I0,
    input [22:0] I1,
    input S,
    output [22:0] O
);
reg [22:0] coreir_commonlib_mux2x23_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x23_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x23_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x23_inst0_out;
endmodule

module Mux2xOutUInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
reg [15:0] coreir_commonlib_mux2x16_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x16_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x16_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module Register_comb (
    input [15:0] value,
    input en,
    input [15:0] self_value_O,
    output [15:0] O0,
    output [15:0] O1
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(self_value_O),
    .I1(value),
    .S(en),
    .O(O0)
);
assign O1 = self_value_O;
endmodule

module Register (
    input [15:0] value,
    input en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
wire [15:0] Register_comb_inst0_O0;
wire [15:0] reg_PR_inst0_out;
Register_comb Register_comb_inst0 (
    .value(value),
    .en(en),
    .self_value_O(reg_PR_inst0_out),
    .O0(Register_comb_inst0_O0),
    .O1(O)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(16'h0000),
    .width(16)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(Register_comb_inst0_O0),
    .out(reg_PR_inst0_out)
);
endmodule

module Mux2xOutUInt1 (
    input [0:0] I0,
    input [0:0] I1,
    input S,
    output [0:0] O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out;
endmodule

module PE_comb (
    input [66:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
    input [7:0] config_addr,
    input [31:0] config_data,
    input config_en,
    input [15:0] self_rega_O0,
    input [15:0] self_rega_O1,
    input [15:0] self_regb_O0,
    input [15:0] self_regb_O1,
    input self_regd_O0,
    input self_regd_O1,
    input self_rege_O0,
    input self_rege_O1,
    input self_regf_O0,
    input self_regf_O1,
    input [15:0] self_alu_O0,
    input self_alu_O1,
    input self_alu_O2,
    input self_alu_O3,
    input self_alu_O4,
    input self_alu_O5,
    input self_cond_O,
    input self_lut_O,
    output [1:0] O0,
    output [15:0] O1,
    output [15:0] O2,
    output O3,
    output O4,
    output [15:0] O5,
    output [1:0] O6,
    output [15:0] O7,
    output [15:0] O8,
    output O9,
    output O10,
    output [15:0] O11,
    output [1:0] O12,
    output O13,
    output O14,
    output O15,
    output O16,
    output O17,
    output [1:0] O18,
    output O19,
    output O20,
    output O21,
    output O22,
    output O23,
    output [1:0] O24,
    output O25,
    output O26,
    output O27,
    output O28,
    output O29,
    output [7:0] O30,
    output [0:0] O31,
    output [15:0] O32,
    output [15:0] O33,
    output O34,
    output [4:0] O35,
    output O36,
    output O37,
    output O38,
    output O39,
    output O40,
    output O41,
    output [7:0] O42,
    output O43,
    output O44,
    output O45,
    output [15:0] O46,
    output O47,
    output [31:0] O48
);
wire [0:0] Mux2xOutUInt1_inst0_O;
wire [0:0] Mux2xOutUInt1_inst1_O;
wire [0:0] Mux2xOutUInt1_inst2_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bits_3_eq_inst1_out;
Mux2xOutUInt1 Mux2xOutUInt1_inst0 (
    .I0(1'h0),
    .I1(1'h1),
    .S(self_regd_O1),
    .O(Mux2xOutUInt1_inst0_O)
);
Mux2xOutUInt1 Mux2xOutUInt1_inst1 (
    .I0(1'h0),
    .I1(1'h1),
    .S(self_rege_O1),
    .O(Mux2xOutUInt1_inst1_O)
);
Mux2xOutUInt1 Mux2xOutUInt1_inst2 (
    .I0(1'h0),
    .I1(1'h1),
    .S(self_regf_O1),
    .O(Mux2xOutUInt1_inst2_O)
);
wire [31:0] Mux2xOutUInt32_inst0_I0;
assign Mux2xOutUInt32_inst0_I0 = {self_regb_O1[15:0],self_rega_O1[15:0]};
wire [31:0] Mux2xOutUInt32_inst0_I1;
assign Mux2xOutUInt32_inst0_I1 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,Mux2xOutUInt1_inst2_O[0],Mux2xOutUInt1_inst1_O[0],Mux2xOutUInt1_inst0_O[0]};
Mux2xOutUInt32 Mux2xOutUInt32_inst0 (
    .I0(Mux2xOutUInt32_inst0_I0),
    .I1(Mux2xOutUInt32_inst0_I1),
    .S(magma_Bits_3_eq_inst1_out),
    .O(O48)
);
assign magma_Bit_and_inst0_out = (config_addr[2:0] == 3'h3) & config_en;
assign magma_Bit_and_inst1_out = magma_Bits_3_eq_inst1_out & config_en;
assign magma_Bits_3_eq_inst1_out = config_addr[2:0] == 3'h4;
assign O0 = inst[23:22];
assign O1 = inst[39:24];
assign O2 = data0;
assign O3 = clk_en;
assign O4 = magma_Bit_and_inst0_out;
assign O5 = config_data[15:0];
assign O6 = inst[41:40];
assign O7 = inst[57:42];
assign O8 = data1;
assign O9 = clk_en;
assign O10 = magma_Bit_and_inst0_out;
assign O11 = config_data[31:16];
assign O12 = inst[59:58];
assign O13 = inst[60];
assign O14 = bit0;
assign O15 = clk_en;
assign O16 = magma_Bit_and_inst1_out;
assign O17 = config_data[0];
assign O18 = inst[62:61];
assign O19 = inst[63];
assign O20 = bit1;
assign O21 = clk_en;
assign O22 = magma_Bit_and_inst1_out;
assign O23 = config_data[1];
assign O24 = inst[65:64];
assign O25 = inst[66];
assign O26 = bit2;
assign O27 = clk_en;
assign O28 = magma_Bit_and_inst1_out;
assign O29 = config_data[2];
assign O30 = inst[7:0];
assign O31 = inst[8];
assign O32 = self_rega_O0;
assign O33 = self_regb_O0;
assign O34 = self_regd_O0;
assign O35 = inst[21:17];
assign O36 = self_alu_O1;
assign O37 = self_lut_O;
assign O38 = self_alu_O2;
assign O39 = self_alu_O3;
assign O40 = self_alu_O4;
assign O41 = self_alu_O5;
assign O42 = inst[16:9];
assign O43 = self_regd_O0;
assign O44 = self_rege_O0;
assign O45 = self_regf_O0;
assign O46 = self_alu_O0;
assign O47 = self_cond_O;
endmodule

module Mux2xOutSInt9 (
    input [8:0] I0,
    input [8:0] I1,
    input S,
    output [8:0] O
);
reg [8:0] coreir_commonlib_mux2x9_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x9_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x9_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x9_inst0_out;
endmodule

module Mux2xOutSInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
reg [15:0] coreir_commonlib_mux2x16_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x16_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x16_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Register_comb_unq1 (
    input value,
    input en,
    input self_value_O,
    output O0,
    output O1
);
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(self_value_O),
    .I1(value),
    .S(en),
    .O(O0)
);
assign O1 = self_value_O;
endmodule

module RegisterMode_comb_unq1 (
    input [1:0] mode,
    input const_,
    input value,
    input clk_en,
    input config_we,
    input config_data,
    input self_register_O,
    output O0,
    output O1,
    output O2,
    output O3
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst11_out;
wire magma_Bits_2_eq_inst12_out;
wire magma_Bits_2_eq_inst13_out;
wire magma_Bits_2_eq_inst14_out;
wire magma_Bits_2_eq_inst2_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(value),
    .I1(value),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(1'b0),
    .I1(clk_en),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst6_O),
    .I1(Mux2xOutBit_inst3_O),
    .S(magma_Bits_2_eq_inst11_out),
    .O(O0)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst7_O),
    .I1(Mux2xOutBit_inst4_O),
    .S(magma_Bits_2_eq_inst12_out),
    .O(O1)
);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst8_O),
    .I1(const_),
    .S(magma_Bits_2_eq_inst13_out),
    .O(O2)
);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst9_O),
    .I1(Mux2xOutBit_inst5_O),
    .S(magma_Bits_2_eq_inst14_out),
    .O(O3)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(self_register_O),
    .I1(self_register_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst0_O),
    .I1(config_data),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst1_O),
    .I1(1'b1),
    .S(magma_Bit_not_inst1_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst2_O),
    .I1(self_register_O),
    .S(magma_Bit_not_inst2_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst3_O),
    .I1(Mux2xOutBit_inst3_O),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst4_O),
    .I1(Mux2xOutBit_inst4_O),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(value),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(Mux2xOutBit_inst5_O),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xOutBit_inst9_O)
);
assign magma_Bit_and_inst0_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst1_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst2_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst3_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_not_inst0_out = ~ (config_we ^ 1'b1);
assign magma_Bit_not_inst1_out = ~ (config_we ^ 1'b1);
assign magma_Bit_not_inst2_out = ~ (config_we ^ 1'b1);
assign magma_Bits_2_eq_inst0_out = mode == 2'h3;
assign magma_Bits_2_eq_inst1_out = mode == 2'h3;
assign magma_Bits_2_eq_inst11_out = mode == 2'h0;
assign magma_Bits_2_eq_inst12_out = mode == 2'h0;
assign magma_Bits_2_eq_inst13_out = mode == 2'h0;
assign magma_Bits_2_eq_inst14_out = mode == 2'h0;
assign magma_Bits_2_eq_inst2_out = mode == 2'h3;
endmodule

module RegisterMode_comb (
    input [1:0] mode,
    input [15:0] const_,
    input [15:0] value,
    input clk_en,
    input config_we,
    input [15:0] config_data,
    input [15:0] self_register_O,
    output [15:0] O0,
    output O1,
    output [15:0] O2,
    output [15:0] O3
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst2_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [15:0] Mux2xOutUInt16_inst1_O;
wire [15:0] Mux2xOutUInt16_inst2_O;
wire [15:0] Mux2xOutUInt16_inst3_O;
wire [15:0] Mux2xOutUInt16_inst4_O;
wire [15:0] Mux2xOutUInt16_inst5_O;
wire [15:0] Mux2xOutUInt16_inst6_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst11_out;
wire magma_Bits_2_eq_inst12_out;
wire magma_Bits_2_eq_inst13_out;
wire magma_Bits_2_eq_inst14_out;
wire magma_Bits_2_eq_inst2_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(1'b0),
    .I1(clk_en),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst0_O),
    .I1(1'b1),
    .S(magma_Bit_not_inst1_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst1_O),
    .I1(Mux2xOutBit_inst1_O),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst2_O),
    .I1(Mux2xOutBit_inst1_O),
    .S(magma_Bits_2_eq_inst12_out),
    .O(O1)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(value),
    .I1(value),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xOutUInt16_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst1 (
    .I0(self_register_O),
    .I1(self_register_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xOutUInt16_inst1_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst2 (
    .I0(Mux2xOutUInt16_inst0_O),
    .I1(config_data),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutUInt16_inst2_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst3 (
    .I0(Mux2xOutUInt16_inst1_O),
    .I1(self_register_O),
    .S(magma_Bit_not_inst2_out),
    .O(Mux2xOutUInt16_inst3_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst4 (
    .I0(Mux2xOutUInt16_inst2_O),
    .I1(Mux2xOutUInt16_inst2_O),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xOutUInt16_inst4_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst5 (
    .I0(Mux2xOutUInt16_inst3_O),
    .I1(value),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutUInt16_inst5_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst6 (
    .I0(Mux2xOutUInt16_inst3_O),
    .I1(Mux2xOutUInt16_inst3_O),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xOutUInt16_inst6_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst7 (
    .I0(Mux2xOutUInt16_inst4_O),
    .I1(Mux2xOutUInt16_inst2_O),
    .S(magma_Bits_2_eq_inst11_out),
    .O(O0)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst8 (
    .I0(Mux2xOutUInt16_inst5_O),
    .I1(const_),
    .S(magma_Bits_2_eq_inst13_out),
    .O(O2)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst9 (
    .I0(Mux2xOutUInt16_inst6_O),
    .I1(Mux2xOutUInt16_inst3_O),
    .S(magma_Bits_2_eq_inst14_out),
    .O(O3)
);
assign magma_Bit_and_inst0_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst1_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst2_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_and_inst3_out = (mode == 2'h2) & (~ (mode == 2'h0));
assign magma_Bit_not_inst0_out = ~ (config_we ^ 1'b1);
assign magma_Bit_not_inst1_out = ~ (config_we ^ 1'b1);
assign magma_Bit_not_inst2_out = ~ (config_we ^ 1'b1);
assign magma_Bits_2_eq_inst0_out = mode == 2'h3;
assign magma_Bits_2_eq_inst1_out = mode == 2'h3;
assign magma_Bits_2_eq_inst11_out = mode == 2'h0;
assign magma_Bits_2_eq_inst12_out = mode == 2'h0;
assign magma_Bits_2_eq_inst13_out = mode == 2'h0;
assign magma_Bits_2_eq_inst14_out = mode == 2'h0;
assign magma_Bits_2_eq_inst2_out = mode == 2'h3;
endmodule

module RegisterMode (
    input [1:0] mode,
    input [15:0] const_,
    input [15:0] value,
    input clk_en,
    input config_we,
    input [15:0] config_data,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output [15:0] O1
);
wire [15:0] RegisterMode_comb_inst0_O0;
wire RegisterMode_comb_inst0_O1;
wire [15:0] Register_inst0_O;
RegisterMode_comb RegisterMode_comb_inst0 (
    .mode(mode),
    .const_(const_),
    .value(value),
    .clk_en(clk_en),
    .config_we(config_we),
    .config_data(config_data),
    .self_register_O(Register_inst0_O),
    .O0(RegisterMode_comb_inst0_O0),
    .O1(RegisterMode_comb_inst0_O1),
    .O2(O0),
    .O3(O1)
);
Register Register_inst0 (
    .value(RegisterMode_comb_inst0_O0),
    .en(RegisterMode_comb_inst0_O1),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Register_inst0_O)
);
endmodule

module LUT_comb (
    input [7:0] lut,
    input bit0,
    input bit1,
    input bit2,
    output O
);
wire [7:0] magma_Bits_8_and_inst0_out;
assign magma_Bits_8_and_inst0_out = (lut >> ({1'b0,1'b0,1'b0,1'b0,1'b0,bit2,bit1,bit0})) & 8'h01;
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
LUT_comb LUT_comb_inst0 (
    .lut(lut),
    .bit0(bit0),
    .bit1(bit1),
    .bit2(bit2),
    .O(O)
);
endmodule

module DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue (
    input I,
    output O,
    input CLK,
    input ASYNCRESET
);
wire [0:0] reg_PR_inst0_out;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(I),
    .out(reg_PR_inst0_out)
);
assign O = reg_PR_inst0_out[0];
endmodule

module Register_unq1 (
    input value,
    input en,
    input CLK,
    input ASYNCRESET,
    output O
);
wire DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire Register_comb_inst0_O0;
DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(Register_comb_inst0_O0),
    .O(DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
Register_comb_unq1 Register_comb_inst0 (
    .value(value),
    .en(en),
    .self_value_O(DFF_init0_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .O0(Register_comb_inst0_O0),
    .O1(O)
);
endmodule

module RegisterMode_unq1 (
    input [1:0] mode,
    input const_,
    input value,
    input clk_en,
    input config_we,
    input config_data,
    input CLK,
    input ASYNCRESET,
    output O0,
    output O1
);
wire RegisterMode_comb_inst0_O0;
wire RegisterMode_comb_inst0_O1;
wire Register_inst0_O;
RegisterMode_comb_unq1 RegisterMode_comb_inst0 (
    .mode(mode),
    .const_(const_),
    .value(value),
    .clk_en(clk_en),
    .config_we(config_we),
    .config_data(config_data),
    .self_register_O(Register_inst0_O),
    .O0(RegisterMode_comb_inst0_O0),
    .O1(RegisterMode_comb_inst0_O1),
    .O2(O0),
    .O3(O1)
);
Register_unq1 Register_inst0 (
    .value(RegisterMode_comb_inst0_O0),
    .en(RegisterMode_comb_inst0_O1),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Register_inst0_O)
);
endmodule

module Cond_comb (
    input [4:0] code,
    input alu,
    input lut,
    input Z,
    input N,
    input C,
    input V,
    output O
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst12_O;
wire Mux2xOutBit_inst13_O;
wire Mux2xOutBit_inst14_O;
wire Mux2xOutBit_inst15_O;
wire Mux2xOutBit_inst16_O;
wire Mux2xOutBit_inst17_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst108_out;
wire magma_Bit_and_inst119_out;
wire magma_Bit_and_inst129_out;
wire magma_Bit_and_inst138_out;
wire magma_Bit_and_inst146_out;
wire magma_Bit_and_inst153_out;
wire magma_Bit_and_inst159_out;
wire magma_Bit_and_inst164_out;
wire magma_Bit_and_inst168_out;
wire magma_Bit_and_inst171_out;
wire magma_Bit_and_inst173_out;
wire magma_Bit_and_inst174_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst21_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_and_inst38_out;
wire magma_Bit_and_inst54_out;
wire magma_Bit_and_inst69_out;
wire magma_Bit_and_inst83_out;
wire magma_Bit_and_inst96_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst6_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst3_out;
wire magma_Bit_xor_inst1_out;
wire magma_Bits_5_eq_inst222_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(magma_Bit_and_inst3_out),
    .I1(magma_Bit_or_inst3_out),
    .S(magma_Bit_and_inst21_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst0_O),
    .I1(magma_Bit_and_inst2_out),
    .S(magma_Bit_and_inst38_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst9_O),
    .I1(magma_Bit_and_inst0_out),
    .S(magma_Bit_and_inst146_out),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst10_O),
    .I1(magma_Bit_not_inst3_out),
    .S(magma_Bit_and_inst153_out),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst11_O),
    .I1(V),
    .S(magma_Bit_and_inst159_out),
    .O(Mux2xOutBit_inst12_O)
);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst12_O),
    .I1(magma_Bit_not_inst2_out),
    .S(magma_Bit_and_inst164_out),
    .O(Mux2xOutBit_inst13_O)
);
Mux2xOutBit Mux2xOutBit_inst14 (
    .I0(Mux2xOutBit_inst13_O),
    .I1(N),
    .S(magma_Bit_and_inst168_out),
    .O(Mux2xOutBit_inst14_O)
);
Mux2xOutBit Mux2xOutBit_inst15 (
    .I0(Mux2xOutBit_inst14_O),
    .I1(magma_Bit_not_inst1_out),
    .S(magma_Bit_and_inst171_out),
    .O(Mux2xOutBit_inst15_O)
);
Mux2xOutBit Mux2xOutBit_inst16 (
    .I0(Mux2xOutBit_inst15_O),
    .I1(C),
    .S(magma_Bit_and_inst173_out),
    .O(Mux2xOutBit_inst16_O)
);
Mux2xOutBit Mux2xOutBit_inst17 (
    .I0(Mux2xOutBit_inst16_O),
    .I1(magma_Bit_not_inst0_out),
    .S(magma_Bit_and_inst174_out),
    .O(Mux2xOutBit_inst17_O)
);
Mux2xOutBit Mux2xOutBit_inst18 (
    .I0(Mux2xOutBit_inst17_O),
    .I1(Z),
    .S(magma_Bits_5_eq_inst222_out),
    .O(O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst1_O),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bit_and_inst54_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst2_O),
    .I1(lut),
    .S(magma_Bit_and_inst69_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst3_O),
    .I1(alu),
    .S(magma_Bit_and_inst83_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst4_O),
    .I1(magma_Bit_or_inst1_out),
    .S(magma_Bit_and_inst96_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(magma_Bit_and_inst1_out),
    .S(magma_Bit_and_inst108_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst6_O),
    .I1(magma_Bit_xor_inst1_out),
    .S(magma_Bit_and_inst119_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst7_O),
    .I1(magma_Bit_not_inst6_out),
    .S(magma_Bit_and_inst129_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst8_O),
    .I1(magma_Bit_or_inst0_out),
    .S(magma_Bit_and_inst138_out),
    .O(Mux2xOutBit_inst9_O)
);
assign magma_Bit_and_inst0_out = C & (~ Z);
assign magma_Bit_and_inst1_out = (~ Z) & (~ (N ^ V));
assign magma_Bit_and_inst108_out = ((((((((((((code == 5'h0c) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b));
assign magma_Bit_and_inst119_out = (((((((((((code == 5'h0b) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a));
assign magma_Bit_and_inst129_out = ((((((((((code == 5'h0a) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09));
assign magma_Bit_and_inst138_out = (((((((((code == 5'h09) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08));
assign magma_Bit_and_inst146_out = ((((((((code == 5'h08) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07));
assign magma_Bit_and_inst153_out = (((((((code == 5'h07) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06));
assign magma_Bit_and_inst159_out = ((((((code == 5'h06) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05));
assign magma_Bit_and_inst164_out = (((((code == 5'h05) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04));
assign magma_Bit_and_inst168_out = ((((code == 5'h04) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)));
assign magma_Bit_and_inst171_out = ((((code == 5'h03) | (code == 5'h03)) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)));
assign magma_Bit_and_inst173_out = (((code == 5'h02) | (code == 5'h02)) & (~ (code == 5'h00))) & (~ (code == 5'h01));
assign magma_Bit_and_inst174_out = (code == 5'h01) & (~ (code == 5'h00));
assign magma_Bit_and_inst2_out = (~ N) & (~ Z);
assign magma_Bit_and_inst21_out = ((((((((((((((((((code == 5'h12) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c))) & (~ (code == 5'h0d))) & (~ (code == 5'h0f))) & (~ (code == 5'h0e))) & (~ (code == 5'h10))) & (~ (code == 5'h11));
assign magma_Bit_and_inst3_out = N & (~ Z);
assign magma_Bit_and_inst38_out = (((((((((((((((((code == 5'h11) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c))) & (~ (code == 5'h0d))) & (~ (code == 5'h0f))) & (~ (code == 5'h0e))) & (~ (code == 5'h10));
assign magma_Bit_and_inst54_out = ((((((((((((((((code == 5'h10) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c))) & (~ (code == 5'h0d))) & (~ (code == 5'h0f))) & (~ (code == 5'h0e));
assign magma_Bit_and_inst69_out = (((((((((((((((code == 5'h0e) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c))) & (~ (code == 5'h0d))) & (~ (code == 5'h0f));
assign magma_Bit_and_inst83_out = ((((((((((((((code == 5'h0f) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c))) & (~ (code == 5'h0d));
assign magma_Bit_and_inst96_out = (((((((((((((code == 5'h0d) & (~ (code == 5'h00))) & (~ (code == 5'h01))) & (~ ((code == 5'h02) | (code == 5'h02)))) & (~ ((code == 5'h03) | (code == 5'h03)))) & (~ (code == 5'h04))) & (~ (code == 5'h05))) & (~ (code == 5'h06))) & (~ (code == 5'h07))) & (~ (code == 5'h08))) & (~ (code == 5'h09))) & (~ (code == 5'h0a))) & (~ (code == 5'h0b))) & (~ (code == 5'h0c));
assign magma_Bit_not_inst0_out = ~ Z;
assign magma_Bit_not_inst1_out = ~ C;
assign magma_Bit_not_inst2_out = ~ N;
assign magma_Bit_not_inst3_out = ~ V;
assign magma_Bit_not_inst6_out = ~ (N ^ V);
assign magma_Bit_or_inst0_out = (~ C) | Z;
assign magma_Bit_or_inst1_out = Z | (N ^ V);
assign magma_Bit_or_inst2_out = (~ N) | Z;
assign magma_Bit_or_inst3_out = N | Z;
assign magma_Bit_xor_inst1_out = N ^ V;
assign magma_Bits_5_eq_inst222_out = code == 5'h00;
endmodule

module Cond (
    input [4:0] code,
    input alu,
    input lut,
    input Z,
    input N,
    input C,
    input V,
    input CLK,
    input ASYNCRESET,
    output O
);
Cond_comb Cond_comb_inst0 (
    .code(code),
    .alu(alu),
    .lut(lut),
    .Z(Z),
    .N(N),
    .C(C),
    .V(V),
    .O(O)
);
endmodule

module ALU_comb (
    input [7:0] alu,
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    input d,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst12_O;
wire Mux2xOutBit_inst13_O;
wire Mux2xOutBit_inst14_O;
wire Mux2xOutBit_inst15_O;
wire Mux2xOutBit_inst16_O;
wire Mux2xOutBit_inst17_O;
wire Mux2xOutBit_inst18_O;
wire Mux2xOutBit_inst19_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst20_O;
wire Mux2xOutBit_inst21_O;
wire Mux2xOutBit_inst22_O;
wire Mux2xOutBit_inst23_O;
wire Mux2xOutBit_inst24_O;
wire Mux2xOutBit_inst25_O;
wire Mux2xOutBit_inst26_O;
wire Mux2xOutBit_inst27_O;
wire Mux2xOutBit_inst28_O;
wire Mux2xOutBit_inst29_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst30_O;
wire Mux2xOutBit_inst31_O;
wire Mux2xOutBit_inst32_O;
wire Mux2xOutBit_inst33_O;
wire Mux2xOutBit_inst34_O;
wire Mux2xOutBit_inst35_O;
wire Mux2xOutBit_inst36_O;
wire Mux2xOutBit_inst37_O;
wire Mux2xOutBit_inst38_O;
wire Mux2xOutBit_inst39_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst40_O;
wire Mux2xOutBit_inst41_O;
wire Mux2xOutBit_inst42_O;
wire Mux2xOutBit_inst43_O;
wire Mux2xOutBit_inst44_O;
wire Mux2xOutBit_inst45_O;
wire Mux2xOutBit_inst46_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst50_O;
wire Mux2xOutBit_inst51_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire [15:0] Mux2xOutSInt16_inst0_O;
wire [15:0] Mux2xOutSInt16_inst1_O;
wire [15:0] Mux2xOutSInt16_inst10_O;
wire [15:0] Mux2xOutSInt16_inst11_O;
wire [15:0] Mux2xOutSInt16_inst12_O;
wire [15:0] Mux2xOutSInt16_inst13_O;
wire [15:0] Mux2xOutSInt16_inst14_O;
wire [15:0] Mux2xOutSInt16_inst15_O;
wire [15:0] Mux2xOutSInt16_inst16_O;
wire [15:0] Mux2xOutSInt16_inst17_O;
wire [15:0] Mux2xOutSInt16_inst18_O;
wire [15:0] Mux2xOutSInt16_inst19_O;
wire [15:0] Mux2xOutSInt16_inst2_O;
wire [15:0] Mux2xOutSInt16_inst20_O;
wire [15:0] Mux2xOutSInt16_inst21_O;
wire [15:0] Mux2xOutSInt16_inst22_O;
wire [15:0] Mux2xOutSInt16_inst23_O;
wire [15:0] Mux2xOutSInt16_inst24_O;
wire [15:0] Mux2xOutSInt16_inst25_O;
wire [15:0] Mux2xOutSInt16_inst26_O;
wire [15:0] Mux2xOutSInt16_inst27_O;
wire [15:0] Mux2xOutSInt16_inst28_O;
wire [15:0] Mux2xOutSInt16_inst29_O;
wire [15:0] Mux2xOutSInt16_inst3_O;
wire [15:0] Mux2xOutSInt16_inst30_O;
wire [15:0] Mux2xOutSInt16_inst4_O;
wire [15:0] Mux2xOutSInt16_inst5_O;
wire [15:0] Mux2xOutSInt16_inst6_O;
wire [15:0] Mux2xOutSInt16_inst7_O;
wire [15:0] Mux2xOutSInt16_inst8_O;
wire [15:0] Mux2xOutSInt16_inst9_O;
wire [8:0] Mux2xOutSInt9_inst0_O;
wire [8:0] Mux2xOutSInt9_inst1_O;
wire [8:0] Mux2xOutSInt9_inst10_O;
wire [8:0] Mux2xOutSInt9_inst11_O;
wire [8:0] Mux2xOutSInt9_inst12_O;
wire [8:0] Mux2xOutSInt9_inst13_O;
wire [8:0] Mux2xOutSInt9_inst14_O;
wire [8:0] Mux2xOutSInt9_inst15_O;
wire [8:0] Mux2xOutSInt9_inst16_O;
wire [8:0] Mux2xOutSInt9_inst17_O;
wire [8:0] Mux2xOutSInt9_inst18_O;
wire [8:0] Mux2xOutSInt9_inst19_O;
wire [8:0] Mux2xOutSInt9_inst2_O;
wire [8:0] Mux2xOutSInt9_inst20_O;
wire [8:0] Mux2xOutSInt9_inst21_O;
wire [8:0] Mux2xOutSInt9_inst22_O;
wire [8:0] Mux2xOutSInt9_inst23_O;
wire [8:0] Mux2xOutSInt9_inst24_O;
wire [8:0] Mux2xOutSInt9_inst25_O;
wire [8:0] Mux2xOutSInt9_inst26_O;
wire [8:0] Mux2xOutSInt9_inst27_O;
wire [8:0] Mux2xOutSInt9_inst28_O;
wire [8:0] Mux2xOutSInt9_inst29_O;
wire [8:0] Mux2xOutSInt9_inst3_O;
wire [8:0] Mux2xOutSInt9_inst30_O;
wire [8:0] Mux2xOutSInt9_inst31_O;
wire [8:0] Mux2xOutSInt9_inst32_O;
wire [8:0] Mux2xOutSInt9_inst33_O;
wire [8:0] Mux2xOutSInt9_inst34_O;
wire [8:0] Mux2xOutSInt9_inst35_O;
wire [8:0] Mux2xOutSInt9_inst36_O;
wire [8:0] Mux2xOutSInt9_inst37_O;
wire [8:0] Mux2xOutSInt9_inst38_O;
wire [8:0] Mux2xOutSInt9_inst39_O;
wire [8:0] Mux2xOutSInt9_inst4_O;
wire [8:0] Mux2xOutSInt9_inst40_O;
wire [8:0] Mux2xOutSInt9_inst41_O;
wire [8:0] Mux2xOutSInt9_inst42_O;
wire [8:0] Mux2xOutSInt9_inst5_O;
wire [8:0] Mux2xOutSInt9_inst6_O;
wire [8:0] Mux2xOutSInt9_inst7_O;
wire [8:0] Mux2xOutSInt9_inst8_O;
wire [8:0] Mux2xOutSInt9_inst9_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [15:0] Mux2xOutUInt16_inst1_O;
wire [15:0] Mux2xOutUInt16_inst10_O;
wire [15:0] Mux2xOutUInt16_inst11_O;
wire [15:0] Mux2xOutUInt16_inst12_O;
wire [15:0] Mux2xOutUInt16_inst13_O;
wire [15:0] Mux2xOutUInt16_inst14_O;
wire [15:0] Mux2xOutUInt16_inst15_O;
wire [15:0] Mux2xOutUInt16_inst16_O;
wire [15:0] Mux2xOutUInt16_inst17_O;
wire [15:0] Mux2xOutUInt16_inst18_O;
wire [15:0] Mux2xOutUInt16_inst19_O;
wire [15:0] Mux2xOutUInt16_inst2_O;
wire [15:0] Mux2xOutUInt16_inst20_O;
wire [15:0] Mux2xOutUInt16_inst21_O;
wire [15:0] Mux2xOutUInt16_inst22_O;
wire [15:0] Mux2xOutUInt16_inst23_O;
wire [15:0] Mux2xOutUInt16_inst24_O;
wire [15:0] Mux2xOutUInt16_inst25_O;
wire [15:0] Mux2xOutUInt16_inst26_O;
wire [15:0] Mux2xOutUInt16_inst27_O;
wire [15:0] Mux2xOutUInt16_inst28_O;
wire [15:0] Mux2xOutUInt16_inst29_O;
wire [15:0] Mux2xOutUInt16_inst3_O;
wire [15:0] Mux2xOutUInt16_inst30_O;
wire [15:0] Mux2xOutUInt16_inst31_O;
wire [15:0] Mux2xOutUInt16_inst32_O;
wire [15:0] Mux2xOutUInt16_inst33_O;
wire [15:0] Mux2xOutUInt16_inst34_O;
wire [15:0] Mux2xOutUInt16_inst35_O;
wire [15:0] Mux2xOutUInt16_inst36_O;
wire [15:0] Mux2xOutUInt16_inst37_O;
wire [15:0] Mux2xOutUInt16_inst38_O;
wire [15:0] Mux2xOutUInt16_inst39_O;
wire [15:0] Mux2xOutUInt16_inst4_O;
wire [15:0] Mux2xOutUInt16_inst40_O;
wire [15:0] Mux2xOutUInt16_inst41_O;
wire [15:0] Mux2xOutUInt16_inst42_O;
wire [15:0] Mux2xOutUInt16_inst43_O;
wire [15:0] Mux2xOutUInt16_inst44_O;
wire [15:0] Mux2xOutUInt16_inst45_O;
wire [15:0] Mux2xOutUInt16_inst46_O;
wire [15:0] Mux2xOutUInt16_inst47_O;
wire [15:0] Mux2xOutUInt16_inst48_O;
wire [15:0] Mux2xOutUInt16_inst49_O;
wire [15:0] Mux2xOutUInt16_inst5_O;
wire [15:0] Mux2xOutUInt16_inst50_O;
wire [15:0] Mux2xOutUInt16_inst51_O;
wire [15:0] Mux2xOutUInt16_inst52_O;
wire [15:0] Mux2xOutUInt16_inst53_O;
wire [15:0] Mux2xOutUInt16_inst54_O;
wire [15:0] Mux2xOutUInt16_inst55_O;
wire [15:0] Mux2xOutUInt16_inst56_O;
wire [15:0] Mux2xOutUInt16_inst57_O;
wire [15:0] Mux2xOutUInt16_inst58_O;
wire [15:0] Mux2xOutUInt16_inst59_O;
wire [15:0] Mux2xOutUInt16_inst6_O;
wire [15:0] Mux2xOutUInt16_inst60_O;
wire [15:0] Mux2xOutUInt16_inst61_O;
wire [15:0] Mux2xOutUInt16_inst62_O;
wire [15:0] Mux2xOutUInt16_inst63_O;
wire [15:0] Mux2xOutUInt16_inst64_O;
wire [15:0] Mux2xOutUInt16_inst65_O;
wire [15:0] Mux2xOutUInt16_inst66_O;
wire [15:0] Mux2xOutUInt16_inst67_O;
wire [15:0] Mux2xOutUInt16_inst68_O;
wire [15:0] Mux2xOutUInt16_inst69_O;
wire [15:0] Mux2xOutUInt16_inst7_O;
wire [15:0] Mux2xOutUInt16_inst70_O;
wire [15:0] Mux2xOutUInt16_inst8_O;
wire [15:0] Mux2xOutUInt16_inst9_O;
wire [22:0] Mux2xOutUInt23_inst0_O;
wire [31:0] Mux2xOutUInt32_inst0_O;
wire [31:0] Mux2xOutUInt32_inst1_O;
wire [7:0] Mux2xOutUInt8_inst0_O;
wire [7:0] Mux2xOutUInt8_inst1_O;
wire [7:0] Mux2xOutUInt8_inst10_O;
wire [7:0] Mux2xOutUInt8_inst11_O;
wire [7:0] Mux2xOutUInt8_inst12_O;
wire [7:0] Mux2xOutUInt8_inst13_O;
wire [7:0] Mux2xOutUInt8_inst14_O;
wire [7:0] Mux2xOutUInt8_inst15_O;
wire [7:0] Mux2xOutUInt8_inst16_O;
wire [7:0] Mux2xOutUInt8_inst17_O;
wire [7:0] Mux2xOutUInt8_inst18_O;
wire [7:0] Mux2xOutUInt8_inst19_O;
wire [7:0] Mux2xOutUInt8_inst2_O;
wire [7:0] Mux2xOutUInt8_inst20_O;
wire [7:0] Mux2xOutUInt8_inst3_O;
wire [7:0] Mux2xOutUInt8_inst4_O;
wire [7:0] Mux2xOutUInt8_inst5_O;
wire [7:0] Mux2xOutUInt8_inst6_O;
wire [7:0] Mux2xOutUInt8_inst7_O;
wire [7:0] Mux2xOutUInt8_inst8_O;
wire [7:0] Mux2xOutUInt8_inst9_O;
wire [15:0] magma_BFloat_16_add_inst0_out;
wire [15:0] magma_BFloat_16_mul_inst0_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst8_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst10_out;
wire magma_Bit_not_inst11_out;
wire magma_Bit_not_inst12_out;
wire magma_Bit_not_inst13_out;
wire magma_Bit_not_inst14_out;
wire magma_Bit_not_inst15_out;
wire magma_Bit_not_inst16_out;
wire magma_Bit_not_inst17_out;
wire magma_Bit_not_inst18_out;
wire magma_Bit_not_inst19_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst20_out;
wire magma_Bit_not_inst21_out;
wire magma_Bit_not_inst22_out;
wire magma_Bit_not_inst23_out;
wire magma_Bit_not_inst24_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst4_out;
wire magma_Bit_not_inst5_out;
wire magma_Bit_not_inst6_out;
wire magma_Bit_not_inst7_out;
wire magma_Bit_not_inst8_out;
wire magma_Bit_not_inst9_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst11_out;
wire magma_Bit_or_inst13_out;
wire magma_Bit_or_inst15_out;
wire magma_Bit_or_inst17_out;
wire magma_Bit_or_inst19_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst22_out;
wire magma_Bit_or_inst25_out;
wire magma_Bit_or_inst28_out;
wire magma_Bit_or_inst3_out;
wire magma_Bit_or_inst31_out;
wire magma_Bit_or_inst34_out;
wire magma_Bit_or_inst37_out;
wire magma_Bit_or_inst40_out;
wire magma_Bit_or_inst43_out;
wire magma_Bit_or_inst46_out;
wire magma_Bit_or_inst49_out;
wire magma_Bit_or_inst5_out;
wire magma_Bit_or_inst7_out;
wire magma_Bit_or_inst9_out;
wire [15:0] magma_Bits_16_and_inst0_out;
wire [15:0] magma_Bits_16_and_inst1_out;
wire [15:0] magma_Bits_16_and_inst10_out;
wire [15:0] magma_Bits_16_and_inst12_out;
wire [15:0] magma_Bits_16_and_inst14_out;
wire [15:0] magma_Bits_16_and_inst3_out;
wire [15:0] magma_Bits_16_and_inst4_out;
wire [15:0] magma_Bits_16_and_inst5_out;
wire [15:0] magma_Bits_16_and_inst7_out;
wire [15:0] magma_Bits_16_and_inst9_out;
wire [15:0] magma_Bits_16_ashr_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire magma_Bits_16_eq_inst1_out;
wire magma_Bits_16_eq_inst2_out;
wire [15:0] magma_Bits_16_lshr_inst0_out;
wire [15:0] magma_Bits_16_lshr_inst1_out;
wire [15:0] magma_Bits_16_lshr_inst2_out;
wire [15:0] magma_Bits_16_neg_inst0_out;
wire [15:0] magma_Bits_16_neg_inst1_out;
wire [15:0] magma_Bits_16_neg_inst2_out;
wire [15:0] magma_Bits_16_neg_inst3_out;
wire [15:0] magma_Bits_16_not_inst0_out;
wire [15:0] magma_Bits_16_or_inst1_out;
wire [15:0] magma_Bits_16_or_inst2_out;
wire [15:0] magma_Bits_16_or_inst4_out;
wire [15:0] magma_Bits_16_or_inst7_out;
wire [15:0] magma_Bits_16_or_inst8_out;
wire [15:0] magma_Bits_16_or_inst9_out;
wire magma_Bits_16_sge_inst0_out;
wire magma_Bits_16_sge_inst1_out;
wire magma_Bits_16_sge_inst2_out;
wire [15:0] magma_Bits_16_shl_inst2_out;
wire [15:0] magma_Bits_16_shl_inst4_out;
wire [15:0] magma_Bits_16_shl_inst5_out;
wire [15:0] magma_Bits_16_shl_inst6_out;
wire magma_Bits_16_sle_inst0_out;
wire [15:0] magma_Bits_16_sub_inst0_out;
wire [15:0] magma_Bits_16_sub_inst1_out;
wire magma_Bits_16_uge_inst0_out;
wire magma_Bits_16_uge_inst1_out;
wire magma_Bits_16_ule_inst0_out;
wire [15:0] magma_Bits_16_xor_inst0_out;
wire [15:0] magma_Bits_16_xor_inst1_out;
wire [16:0] magma_Bits_17_add_inst1_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire magma_Bits_1_eq_inst3_out;
wire magma_Bits_1_eq_inst4_out;
wire magma_Bits_1_eq_inst5_out;
wire magma_Bits_1_eq_inst6_out;
wire [22:0] magma_Bits_23_lshr_inst0_out;
wire [22:0] magma_Bits_23_shl_inst0_out;
wire [31:0] magma_Bits_32_mul_inst0_out;
wire [7:0] magma_Bits_8_add_inst0_out;
wire [7:0] magma_Bits_8_add_inst1_out;
wire magma_Bits_8_eq_inst100_out;
wire magma_Bits_8_eq_inst101_out;
wire magma_Bits_8_eq_inst102_out;
wire magma_Bits_8_eq_inst103_out;
wire magma_Bits_8_eq_inst104_out;
wire magma_Bits_8_eq_inst105_out;
wire magma_Bits_8_eq_inst106_out;
wire magma_Bits_8_eq_inst107_out;
wire magma_Bits_8_eq_inst108_out;
wire magma_Bits_8_eq_inst109_out;
wire magma_Bits_8_eq_inst110_out;
wire magma_Bits_8_eq_inst111_out;
wire magma_Bits_8_eq_inst112_out;
wire magma_Bits_8_eq_inst113_out;
wire magma_Bits_8_eq_inst114_out;
wire magma_Bits_8_eq_inst115_out;
wire magma_Bits_8_eq_inst116_out;
wire magma_Bits_8_eq_inst117_out;
wire magma_Bits_8_eq_inst118_out;
wire magma_Bits_8_eq_inst119_out;
wire magma_Bits_8_eq_inst12_out;
wire magma_Bits_8_eq_inst120_out;
wire magma_Bits_8_eq_inst121_out;
wire magma_Bits_8_eq_inst122_out;
wire magma_Bits_8_eq_inst123_out;
wire magma_Bits_8_eq_inst124_out;
wire magma_Bits_8_eq_inst125_out;
wire magma_Bits_8_eq_inst126_out;
wire magma_Bits_8_eq_inst127_out;
wire magma_Bits_8_eq_inst128_out;
wire magma_Bits_8_eq_inst129_out;
wire magma_Bits_8_eq_inst130_out;
wire magma_Bits_8_eq_inst131_out;
wire magma_Bits_8_eq_inst132_out;
wire magma_Bits_8_eq_inst133_out;
wire magma_Bits_8_eq_inst134_out;
wire magma_Bits_8_eq_inst135_out;
wire magma_Bits_8_eq_inst136_out;
wire magma_Bits_8_eq_inst137_out;
wire magma_Bits_8_eq_inst138_out;
wire magma_Bits_8_eq_inst139_out;
wire magma_Bits_8_eq_inst140_out;
wire magma_Bits_8_eq_inst141_out;
wire magma_Bits_8_eq_inst142_out;
wire magma_Bits_8_eq_inst143_out;
wire magma_Bits_8_eq_inst144_out;
wire magma_Bits_8_eq_inst145_out;
wire magma_Bits_8_eq_inst146_out;
wire magma_Bits_8_eq_inst147_out;
wire magma_Bits_8_eq_inst148_out;
wire magma_Bits_8_eq_inst149_out;
wire magma_Bits_8_eq_inst15_out;
wire magma_Bits_8_eq_inst150_out;
wire magma_Bits_8_eq_inst151_out;
wire magma_Bits_8_eq_inst152_out;
wire magma_Bits_8_eq_inst153_out;
wire magma_Bits_8_eq_inst154_out;
wire magma_Bits_8_eq_inst155_out;
wire magma_Bits_8_eq_inst156_out;
wire magma_Bits_8_eq_inst157_out;
wire magma_Bits_8_eq_inst158_out;
wire magma_Bits_8_eq_inst159_out;
wire magma_Bits_8_eq_inst16_out;
wire magma_Bits_8_eq_inst160_out;
wire magma_Bits_8_eq_inst161_out;
wire magma_Bits_8_eq_inst162_out;
wire magma_Bits_8_eq_inst163_out;
wire magma_Bits_8_eq_inst164_out;
wire magma_Bits_8_eq_inst165_out;
wire magma_Bits_8_eq_inst166_out;
wire magma_Bits_8_eq_inst167_out;
wire magma_Bits_8_eq_inst168_out;
wire magma_Bits_8_eq_inst169_out;
wire magma_Bits_8_eq_inst17_out;
wire magma_Bits_8_eq_inst170_out;
wire magma_Bits_8_eq_inst171_out;
wire magma_Bits_8_eq_inst172_out;
wire magma_Bits_8_eq_inst173_out;
wire magma_Bits_8_eq_inst174_out;
wire magma_Bits_8_eq_inst175_out;
wire magma_Bits_8_eq_inst176_out;
wire magma_Bits_8_eq_inst177_out;
wire magma_Bits_8_eq_inst178_out;
wire magma_Bits_8_eq_inst179_out;
wire magma_Bits_8_eq_inst18_out;
wire magma_Bits_8_eq_inst180_out;
wire magma_Bits_8_eq_inst181_out;
wire magma_Bits_8_eq_inst182_out;
wire magma_Bits_8_eq_inst183_out;
wire magma_Bits_8_eq_inst184_out;
wire magma_Bits_8_eq_inst185_out;
wire magma_Bits_8_eq_inst186_out;
wire magma_Bits_8_eq_inst187_out;
wire magma_Bits_8_eq_inst188_out;
wire magma_Bits_8_eq_inst19_out;
wire magma_Bits_8_eq_inst2_out;
wire magma_Bits_8_eq_inst20_out;
wire magma_Bits_8_eq_inst21_out;
wire magma_Bits_8_eq_inst22_out;
wire magma_Bits_8_eq_inst23_out;
wire magma_Bits_8_eq_inst230_out;
wire magma_Bits_8_eq_inst24_out;
wire magma_Bits_8_eq_inst25_out;
wire magma_Bits_8_eq_inst26_out;
wire magma_Bits_8_eq_inst27_out;
wire magma_Bits_8_eq_inst28_out;
wire magma_Bits_8_eq_inst29_out;
wire magma_Bits_8_eq_inst3_out;
wire magma_Bits_8_eq_inst30_out;
wire magma_Bits_8_eq_inst31_out;
wire magma_Bits_8_eq_inst32_out;
wire magma_Bits_8_eq_inst33_out;
wire magma_Bits_8_eq_inst34_out;
wire magma_Bits_8_eq_inst35_out;
wire magma_Bits_8_eq_inst36_out;
wire magma_Bits_8_eq_inst37_out;
wire magma_Bits_8_eq_inst38_out;
wire magma_Bits_8_eq_inst39_out;
wire magma_Bits_8_eq_inst4_out;
wire magma_Bits_8_eq_inst40_out;
wire magma_Bits_8_eq_inst41_out;
wire magma_Bits_8_eq_inst42_out;
wire magma_Bits_8_eq_inst43_out;
wire magma_Bits_8_eq_inst44_out;
wire magma_Bits_8_eq_inst45_out;
wire magma_Bits_8_eq_inst46_out;
wire magma_Bits_8_eq_inst47_out;
wire magma_Bits_8_eq_inst48_out;
wire magma_Bits_8_eq_inst49_out;
wire magma_Bits_8_eq_inst5_out;
wire magma_Bits_8_eq_inst50_out;
wire magma_Bits_8_eq_inst51_out;
wire magma_Bits_8_eq_inst52_out;
wire magma_Bits_8_eq_inst53_out;
wire magma_Bits_8_eq_inst54_out;
wire magma_Bits_8_eq_inst55_out;
wire magma_Bits_8_eq_inst56_out;
wire magma_Bits_8_eq_inst57_out;
wire magma_Bits_8_eq_inst58_out;
wire magma_Bits_8_eq_inst59_out;
wire magma_Bits_8_eq_inst6_out;
wire magma_Bits_8_eq_inst60_out;
wire magma_Bits_8_eq_inst61_out;
wire magma_Bits_8_eq_inst62_out;
wire magma_Bits_8_eq_inst63_out;
wire magma_Bits_8_eq_inst64_out;
wire magma_Bits_8_eq_inst65_out;
wire magma_Bits_8_eq_inst7_out;
wire magma_Bits_8_eq_inst90_out;
wire magma_Bits_8_eq_inst91_out;
wire magma_Bits_8_eq_inst92_out;
wire magma_Bits_8_eq_inst93_out;
wire magma_Bits_8_eq_inst94_out;
wire magma_Bits_8_eq_inst95_out;
wire magma_Bits_8_eq_inst96_out;
wire magma_Bits_8_eq_inst97_out;
wire magma_Bits_8_eq_inst98_out;
wire magma_Bits_8_eq_inst99_out;
wire magma_Bits_8_ugt_inst0_out;
wire [8:0] magma_Bits_9_neg_inst0_out;
wire [8:0] magma_Bits_9_neg_inst1_out;
wire magma_Bits_9_slt_inst0_out;
wire magma_Bits_9_slt_inst1_out;
wire magma_Bits_9_slt_inst2_out;
wire magma_Bits_9_slt_inst3_out;
wire [8:0] magma_Bits_9_sub_inst0_out;
wire [8:0] magma_Bits_9_sub_inst1_out;
wire [8:0] magma_Bits_9_sub_inst2_out;
wire magma_Bits_9_ugt_inst0_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(magma_Bits_16_uge_inst0_out),
    .I1(magma_Bits_16_sge_inst0_out),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(magma_Bits_16_ule_inst0_out),
    .I1(magma_Bits_16_sle_inst0_out),
    .S(magma_Bits_1_eq_inst3_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst8_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst39_out),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst9_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst43_out),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst10_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst48_out),
    .O(Mux2xOutBit_inst12_O)
);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst11_O),
    .I1(magma_Bits_9_ugt_inst0_out),
    .S(magma_Bits_8_eq_inst51_out),
    .O(Mux2xOutBit_inst13_O)
);
Mux2xOutBit Mux2xOutBit_inst14 (
    .I0(Mux2xOutBit_inst12_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst56_out),
    .O(Mux2xOutBit_inst14_O)
);
Mux2xOutBit Mux2xOutBit_inst15 (
    .I0(Mux2xOutBit_inst13_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst58_out),
    .O(Mux2xOutBit_inst15_O)
);
Mux2xOutBit Mux2xOutBit_inst16 (
    .I0(Mux2xOutBit_inst14_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst63_out),
    .O(Mux2xOutBit_inst16_O)
);
Mux2xOutBit Mux2xOutBit_inst17 (
    .I0(Mux2xOutBit_inst15_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst65_out),
    .O(Mux2xOutBit_inst17_O)
);
Mux2xOutBit Mux2xOutBit_inst18 (
    .I0(Mux2xOutBit_inst16_O),
    .I1(1'b0),
    .S(magma_Bit_or_inst15_out),
    .O(Mux2xOutBit_inst18_O)
);
Mux2xOutBit Mux2xOutBit_inst19 (
    .I0(Mux2xOutBit_inst17_O),
    .I1(1'b0),
    .S(magma_Bit_or_inst19_out),
    .O(Mux2xOutBit_inst19_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(magma_Bits_16_uge_inst1_out),
    .I1(magma_Bits_16_sge_inst1_out),
    .S(magma_Bits_1_eq_inst4_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst20 (
    .I0(Mux2xOutBit_inst18_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst95_out),
    .O(Mux2xOutBit_inst20_O)
);
Mux2xOutBit Mux2xOutBit_inst21 (
    .I0(Mux2xOutBit_inst19_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst97_out),
    .O(Mux2xOutBit_inst21_O)
);
Mux2xOutBit Mux2xOutBit_inst22 (
    .I0(Mux2xOutBit_inst20_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst103_out),
    .O(Mux2xOutBit_inst22_O)
);
Mux2xOutBit Mux2xOutBit_inst23 (
    .I0(Mux2xOutBit_inst21_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst105_out),
    .O(Mux2xOutBit_inst23_O)
);
Mux2xOutBit Mux2xOutBit_inst24 (
    .I0(Mux2xOutBit_inst22_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst111_out),
    .O(Mux2xOutBit_inst24_O)
);
Mux2xOutBit Mux2xOutBit_inst25 (
    .I0(Mux2xOutBit_inst23_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst113_out),
    .O(Mux2xOutBit_inst25_O)
);
Mux2xOutBit Mux2xOutBit_inst26 (
    .I0(Mux2xOutBit_inst24_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst119_out),
    .O(Mux2xOutBit_inst26_O)
);
Mux2xOutBit Mux2xOutBit_inst27 (
    .I0(Mux2xOutBit_inst25_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst121_out),
    .O(Mux2xOutBit_inst27_O)
);
Mux2xOutBit Mux2xOutBit_inst28 (
    .I0(Mux2xOutBit_inst26_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst127_out),
    .O(Mux2xOutBit_inst28_O)
);
Mux2xOutBit Mux2xOutBit_inst29 (
    .I0(Mux2xOutBit_inst27_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst129_out),
    .O(Mux2xOutBit_inst29_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(1'b0),
    .I1(d),
    .S(magma_Bit_or_inst1_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst30 (
    .I0(Mux2xOutBit_inst28_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst135_out),
    .O(Mux2xOutBit_inst30_O)
);
Mux2xOutBit Mux2xOutBit_inst31 (
    .I0(Mux2xOutBit_inst29_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst137_out),
    .O(Mux2xOutBit_inst31_O)
);
Mux2xOutBit Mux2xOutBit_inst32 (
    .I0(Mux2xOutBit_inst30_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst143_out),
    .O(Mux2xOutBit_inst32_O)
);
Mux2xOutBit Mux2xOutBit_inst33 (
    .I0(Mux2xOutBit_inst31_O),
    .I1(a[15]),
    .S(magma_Bits_8_eq_inst145_out),
    .O(Mux2xOutBit_inst33_O)
);
Mux2xOutBit Mux2xOutBit_inst34 (
    .I0(Mux2xOutBit_inst32_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst151_out),
    .O(Mux2xOutBit_inst34_O)
);
Mux2xOutBit Mux2xOutBit_inst35 (
    .I0(Mux2xOutBit_inst33_O),
    .I1(Mux2xOutBit_inst1_O),
    .S(magma_Bits_8_eq_inst153_out),
    .O(Mux2xOutBit_inst35_O)
);
Mux2xOutBit Mux2xOutBit_inst36 (
    .I0(Mux2xOutBit_inst34_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst159_out),
    .O(Mux2xOutBit_inst36_O)
);
Mux2xOutBit Mux2xOutBit_inst37 (
    .I0(Mux2xOutBit_inst35_O),
    .I1(Mux2xOutBit_inst0_O),
    .S(magma_Bits_8_eq_inst161_out),
    .O(Mux2xOutBit_inst37_O)
);
Mux2xOutBit Mux2xOutBit_inst38 (
    .I0(1'b0),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst167_out),
    .O(Mux2xOutBit_inst38_O)
);
Mux2xOutBit Mux2xOutBit_inst39 (
    .I0(Mux2xOutBit_inst36_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst168_out),
    .O(Mux2xOutBit_inst39_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst3_O),
    .I1(1'b1),
    .S(magma_Bits_8_eq_inst12_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst40 (
    .I0(Mux2xOutBit_inst37_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst170_out),
    .O(Mux2xOutBit_inst40_O)
);
Mux2xOutBit Mux2xOutBit_inst41 (
    .I0(Mux2xOutBit_inst38_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst176_out),
    .O(Mux2xOutBit_inst41_O)
);
Mux2xOutBit Mux2xOutBit_inst42 (
    .I0(Mux2xOutBit_inst39_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst177_out),
    .O(Mux2xOutBit_inst42_O)
);
Mux2xOutBit Mux2xOutBit_inst43 (
    .I0(Mux2xOutBit_inst40_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst179_out),
    .O(Mux2xOutBit_inst43_O)
);
Mux2xOutBit Mux2xOutBit_inst44 (
    .I0(Mux2xOutBit_inst41_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst185_out),
    .O(Mux2xOutBit_inst44_O)
);
Mux2xOutBit Mux2xOutBit_inst45 (
    .I0(Mux2xOutBit_inst42_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst186_out),
    .O(Mux2xOutBit_inst45_O)
);
Mux2xOutBit Mux2xOutBit_inst46 (
    .I0(Mux2xOutBit_inst43_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst188_out),
    .O(Mux2xOutBit_inst46_O)
);
Mux2xOutBit Mux2xOutBit_inst47 (
    .I0(Mux2xOutBit_inst44_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst37_out),
    .O(O4)
);
Mux2xOutBit Mux2xOutBit_inst48 (
    .I0(Mux2xOutBit_inst45_O),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bit_or_inst40_out),
    .O(O5)
);
Mux2xOutBit Mux2xOutBit_inst49 (
    .I0(Mux2xOutBit_inst46_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst46_out),
    .O(O1)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(1'b0),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst19_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst50 (
    .I0(magma_Bits_16_eq_inst2_out),
    .I1(magma_Bit_and_inst6_out),
    .S(magma_Bit_or_inst49_out),
    .O(Mux2xOutBit_inst50_O)
);
Mux2xOutBit Mux2xOutBit_inst51 (
    .I0(Mux2xOutBit_inst50_O),
    .I1(1'b1),
    .S(magma_Bit_and_inst8_out),
    .O(Mux2xOutBit_inst51_O)
);
Mux2xOutBit Mux2xOutBit_inst52 (
    .I0(Mux2xOutBit_inst50_O),
    .I1(Mux2xOutBit_inst51_O),
    .S(magma_Bits_8_eq_inst230_out),
    .O(O2)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(1'b0),
    .I1(magma_Bits_8_ugt_inst0_out),
    .S(magma_Bits_8_eq_inst23_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst29_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst6_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst33_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst7_O),
    .I1(1'b0),
    .S(magma_Bits_8_eq_inst35_out),
    .O(Mux2xOutBit_inst9_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst0 (
    .I0(16'hff81),
    .I1(16'h0000),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutSInt16_inst0_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst1 (
    .I0(Mux2xOutSInt16_inst0_O),
    .I1(16'h0001),
    .S(magma_Bit_not_inst1_out),
    .O(Mux2xOutSInt16_inst1_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst10 (
    .I0(Mux2xOutSInt16_inst9_O),
    .I1(16'h0002),
    .S(magma_Bit_not_inst11_out),
    .O(Mux2xOutSInt16_inst10_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst11 (
    .I0(Mux2xOutSInt16_inst10_O),
    .I1(16'h0003),
    .S(magma_Bit_not_inst12_out),
    .O(Mux2xOutSInt16_inst11_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst12 (
    .I0(Mux2xOutSInt16_inst11_O),
    .I1(16'h0004),
    .S(magma_Bit_not_inst13_out),
    .O(Mux2xOutSInt16_inst12_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst13 (
    .I0(Mux2xOutSInt16_inst12_O),
    .I1(16'h0005),
    .S(magma_Bit_not_inst14_out),
    .O(Mux2xOutSInt16_inst13_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst14 (
    .I0(Mux2xOutSInt16_inst13_O),
    .I1(16'h0006),
    .S(magma_Bit_not_inst15_out),
    .O(Mux2xOutSInt16_inst14_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst15 (
    .I0(Mux2xOutSInt16_inst14_O),
    .I1(16'h0007),
    .S(magma_Bit_not_inst16_out),
    .O(Mux2xOutSInt16_inst15_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst16 (
    .I0(Mux2xOutSInt16_inst15_O),
    .I1(16'h0008),
    .S(magma_Bit_not_inst17_out),
    .O(Mux2xOutSInt16_inst16_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst17 (
    .I0(Mux2xOutSInt16_inst16_O),
    .I1(16'h0009),
    .S(magma_Bit_not_inst18_out),
    .O(Mux2xOutSInt16_inst17_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst18 (
    .I0(Mux2xOutSInt16_inst17_O),
    .I1(16'h000a),
    .S(magma_Bit_not_inst19_out),
    .O(Mux2xOutSInt16_inst18_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst19 (
    .I0(Mux2xOutSInt16_inst18_O),
    .I1(16'h000b),
    .S(magma_Bit_not_inst20_out),
    .O(Mux2xOutSInt16_inst19_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst2 (
    .I0(Mux2xOutSInt16_inst1_O),
    .I1(16'h0002),
    .S(magma_Bit_not_inst2_out),
    .O(Mux2xOutSInt16_inst2_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst20 (
    .I0(Mux2xOutSInt16_inst19_O),
    .I1(16'h000c),
    .S(magma_Bit_not_inst21_out),
    .O(Mux2xOutSInt16_inst20_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst21 (
    .I0(Mux2xOutSInt16_inst20_O),
    .I1(16'h000d),
    .S(magma_Bit_not_inst22_out),
    .O(Mux2xOutSInt16_inst21_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst22 (
    .I0(Mux2xOutSInt16_inst21_O),
    .I1(16'h000e),
    .S(magma_Bit_not_inst23_out),
    .O(Mux2xOutSInt16_inst22_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst23 (
    .I0(Mux2xOutSInt16_inst22_O),
    .I1(16'h000f),
    .S(magma_Bit_not_inst24_out),
    .O(Mux2xOutSInt16_inst23_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst24 (
    .I0(Mux2xOutSInt16_inst23_O),
    .I1(Mux2xOutSInt16_inst7_O),
    .S(magma_Bits_8_eq_inst3_out),
    .O(Mux2xOutSInt16_inst24_O)
);
wire [15:0] Mux2xOutSInt16_inst25_I1;
assign Mux2xOutSInt16_inst25_I1 = {Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7],Mux2xOutSInt9_inst0_O[7:0]};
Mux2xOutSInt16 Mux2xOutSInt16_inst25 (
    .I0(Mux2xOutUInt16_inst3_O),
    .I1(Mux2xOutSInt16_inst25_I1),
    .S(magma_Bits_8_eq_inst4_out),
    .O(Mux2xOutSInt16_inst25_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst26 (
    .I0(magma_Bits_16_sub_inst1_out),
    .I1(magma_Bits_16_sub_inst0_out),
    .S(magma_Bits_8_eq_inst5_out),
    .O(Mux2xOutSInt16_inst26_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst27 (
    .I0(16'h7f00),
    .I1(16'h007f),
    .S(magma_Bits_8_eq_inst6_out),
    .O(Mux2xOutSInt16_inst27_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst28 (
    .I0(magma_Bits_23_lshr_inst0_out[15:0]),
    .I1(magma_Bits_16_neg_inst2_out),
    .S(magma_Bits_16_eq_inst0_out),
    .O(Mux2xOutSInt16_inst28_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst29 (
    .I0(magma_Bits_16_and_inst14_out),
    .I1(magma_Bits_16_neg_inst3_out),
    .S(magma_Bits_16_eq_inst1_out),
    .O(Mux2xOutSInt16_inst29_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst3 (
    .I0(Mux2xOutSInt16_inst2_O),
    .I1(16'h0003),
    .S(magma_Bit_not_inst3_out),
    .O(Mux2xOutSInt16_inst3_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst30 (
    .I0(Mux2xOutSInt16_inst29_O),
    .I1(Mux2xOutSInt16_inst28_O),
    .S(magma_Bits_8_eq_inst27_out),
    .O(Mux2xOutSInt16_inst30_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst4 (
    .I0(Mux2xOutSInt16_inst3_O),
    .I1(16'h0004),
    .S(magma_Bit_not_inst4_out),
    .O(Mux2xOutSInt16_inst4_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst5 (
    .I0(Mux2xOutSInt16_inst4_O),
    .I1(16'h0005),
    .S(magma_Bit_not_inst5_out),
    .O(Mux2xOutSInt16_inst5_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst6 (
    .I0(Mux2xOutSInt16_inst5_O),
    .I1(16'h0006),
    .S(magma_Bit_not_inst6_out),
    .O(Mux2xOutSInt16_inst6_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst7 (
    .I0(Mux2xOutSInt16_inst6_O),
    .I1(16'h0007),
    .S(magma_Bit_not_inst7_out),
    .O(Mux2xOutSInt16_inst7_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst8 (
    .I0(16'hff81),
    .I1(16'h0000),
    .S(magma_Bit_not_inst9_out),
    .O(Mux2xOutSInt16_inst8_O)
);
Mux2xOutSInt16 Mux2xOutSInt16_inst9 (
    .I0(Mux2xOutSInt16_inst8_O),
    .I1(16'h0001),
    .S(magma_Bit_not_inst10_out),
    .O(Mux2xOutSInt16_inst9_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst0 (
    .I0(magma_Bits_9_sub_inst0_out),
    .I1(magma_Bits_9_neg_inst0_out),
    .S(magma_Bits_9_slt_inst1_out),
    .O(Mux2xOutSInt9_inst0_O)
);
wire [8:0] Mux2xOutSInt9_inst1_I0;
assign Mux2xOutSInt9_inst1_I0 = {1'b0,a[14:7]};
wire [8:0] Mux2xOutSInt9_inst1_I1;
assign Mux2xOutSInt9_inst1_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst1 (
    .I0(Mux2xOutSInt9_inst1_I0),
    .I1(Mux2xOutSInt9_inst1_I1),
    .S(magma_Bits_8_eq_inst16_out),
    .O(Mux2xOutSInt9_inst1_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst10 (
    .I0(Mux2xOutSInt9_inst8_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst46_out),
    .O(Mux2xOutSInt9_inst10_O)
);
wire [8:0] Mux2xOutSInt9_inst11_I1;
assign Mux2xOutSInt9_inst11_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst11 (
    .I0(Mux2xOutSInt9_inst9_O),
    .I1(Mux2xOutSInt9_inst11_I1),
    .S(magma_Bits_8_eq_inst53_out),
    .O(Mux2xOutSInt9_inst11_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst12 (
    .I0(Mux2xOutSInt9_inst10_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst54_out),
    .O(Mux2xOutSInt9_inst12_O)
);
wire [8:0] Mux2xOutSInt9_inst13_I1;
assign Mux2xOutSInt9_inst13_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst13 (
    .I0(Mux2xOutSInt9_inst11_O),
    .I1(Mux2xOutSInt9_inst13_I1),
    .S(magma_Bits_8_eq_inst60_out),
    .O(Mux2xOutSInt9_inst13_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst14 (
    .I0(Mux2xOutSInt9_inst12_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst61_out),
    .O(Mux2xOutSInt9_inst14_O)
);
wire [8:0] Mux2xOutSInt9_inst15_I1;
assign Mux2xOutSInt9_inst15_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst15 (
    .I0(Mux2xOutSInt9_inst13_O),
    .I1(Mux2xOutSInt9_inst15_I1),
    .S(magma_Bit_or_inst9_out),
    .O(Mux2xOutSInt9_inst15_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst16 (
    .I0(Mux2xOutSInt9_inst14_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bit_or_inst11_out),
    .O(Mux2xOutSInt9_inst16_O)
);
wire [8:0] Mux2xOutSInt9_inst17_I1;
assign Mux2xOutSInt9_inst17_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst17 (
    .I0(Mux2xOutSInt9_inst15_O),
    .I1(Mux2xOutSInt9_inst17_I1),
    .S(magma_Bits_8_eq_inst92_out),
    .O(Mux2xOutSInt9_inst17_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst18 (
    .I0(Mux2xOutSInt9_inst16_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst93_out),
    .O(Mux2xOutSInt9_inst18_O)
);
wire [8:0] Mux2xOutSInt9_inst19_I1;
assign Mux2xOutSInt9_inst19_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst19 (
    .I0(Mux2xOutSInt9_inst17_O),
    .I1(Mux2xOutSInt9_inst19_I1),
    .S(magma_Bits_8_eq_inst100_out),
    .O(Mux2xOutSInt9_inst19_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst2 (
    .I0(magma_Bits_9_sub_inst0_out),
    .I1(magma_Bits_9_sub_inst2_out),
    .S(magma_Bits_8_eq_inst17_out),
    .O(Mux2xOutSInt9_inst2_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst20 (
    .I0(Mux2xOutSInt9_inst18_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst101_out),
    .O(Mux2xOutSInt9_inst20_O)
);
wire [8:0] Mux2xOutSInt9_inst21_I1;
assign Mux2xOutSInt9_inst21_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst21 (
    .I0(Mux2xOutSInt9_inst19_O),
    .I1(Mux2xOutSInt9_inst21_I1),
    .S(magma_Bits_8_eq_inst108_out),
    .O(Mux2xOutSInt9_inst21_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst22 (
    .I0(Mux2xOutSInt9_inst20_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst109_out),
    .O(Mux2xOutSInt9_inst22_O)
);
wire [8:0] Mux2xOutSInt9_inst23_I1;
assign Mux2xOutSInt9_inst23_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst23 (
    .I0(Mux2xOutSInt9_inst21_O),
    .I1(Mux2xOutSInt9_inst23_I1),
    .S(magma_Bits_8_eq_inst116_out),
    .O(Mux2xOutSInt9_inst23_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst24 (
    .I0(Mux2xOutSInt9_inst22_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst117_out),
    .O(Mux2xOutSInt9_inst24_O)
);
wire [8:0] Mux2xOutSInt9_inst25_I1;
assign Mux2xOutSInt9_inst25_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst25 (
    .I0(Mux2xOutSInt9_inst23_O),
    .I1(Mux2xOutSInt9_inst25_I1),
    .S(magma_Bits_8_eq_inst124_out),
    .O(Mux2xOutSInt9_inst25_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst26 (
    .I0(Mux2xOutSInt9_inst24_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst125_out),
    .O(Mux2xOutSInt9_inst26_O)
);
wire [8:0] Mux2xOutSInt9_inst27_I1;
assign Mux2xOutSInt9_inst27_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst27 (
    .I0(Mux2xOutSInt9_inst25_O),
    .I1(Mux2xOutSInt9_inst27_I1),
    .S(magma_Bits_8_eq_inst132_out),
    .O(Mux2xOutSInt9_inst27_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst28 (
    .I0(Mux2xOutSInt9_inst26_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst133_out),
    .O(Mux2xOutSInt9_inst28_O)
);
wire [8:0] Mux2xOutSInt9_inst29_I1;
assign Mux2xOutSInt9_inst29_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst29 (
    .I0(Mux2xOutSInt9_inst27_O),
    .I1(Mux2xOutSInt9_inst29_I1),
    .S(magma_Bits_8_eq_inst140_out),
    .O(Mux2xOutSInt9_inst29_O)
);
wire [8:0] Mux2xOutSInt9_inst3_I1;
assign Mux2xOutSInt9_inst3_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst3 (
    .I0(Mux2xOutSInt9_inst1_O),
    .I1(Mux2xOutSInt9_inst3_I1),
    .S(magma_Bits_8_eq_inst21_out),
    .O(Mux2xOutSInt9_inst3_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst30 (
    .I0(Mux2xOutSInt9_inst28_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst141_out),
    .O(Mux2xOutSInt9_inst30_O)
);
wire [8:0] Mux2xOutSInt9_inst31_I1;
assign Mux2xOutSInt9_inst31_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst31 (
    .I0(Mux2xOutSInt9_inst29_O),
    .I1(Mux2xOutSInt9_inst31_I1),
    .S(magma_Bits_8_eq_inst148_out),
    .O(Mux2xOutSInt9_inst31_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst32 (
    .I0(Mux2xOutSInt9_inst30_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst149_out),
    .O(Mux2xOutSInt9_inst32_O)
);
wire [8:0] Mux2xOutSInt9_inst33_I1;
assign Mux2xOutSInt9_inst33_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst33 (
    .I0(Mux2xOutSInt9_inst31_O),
    .I1(Mux2xOutSInt9_inst33_I1),
    .S(magma_Bits_8_eq_inst156_out),
    .O(Mux2xOutSInt9_inst33_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst34 (
    .I0(Mux2xOutSInt9_inst32_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst157_out),
    .O(Mux2xOutSInt9_inst34_O)
);
wire [8:0] Mux2xOutSInt9_inst35_I1;
assign Mux2xOutSInt9_inst35_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst35 (
    .I0(Mux2xOutSInt9_inst33_O),
    .I1(Mux2xOutSInt9_inst35_I1),
    .S(magma_Bits_8_eq_inst164_out),
    .O(Mux2xOutSInt9_inst35_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst36 (
    .I0(Mux2xOutSInt9_inst34_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst165_out),
    .O(Mux2xOutSInt9_inst36_O)
);
wire [8:0] Mux2xOutSInt9_inst37_I1;
assign Mux2xOutSInt9_inst37_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst37 (
    .I0(Mux2xOutSInt9_inst35_O),
    .I1(Mux2xOutSInt9_inst37_I1),
    .S(magma_Bits_8_eq_inst173_out),
    .O(Mux2xOutSInt9_inst37_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst38 (
    .I0(Mux2xOutSInt9_inst36_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst174_out),
    .O(Mux2xOutSInt9_inst38_O)
);
wire [8:0] Mux2xOutSInt9_inst39_I1;
assign Mux2xOutSInt9_inst39_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst39 (
    .I0(Mux2xOutSInt9_inst37_O),
    .I1(Mux2xOutSInt9_inst39_I1),
    .S(magma_Bits_8_eq_inst182_out),
    .O(Mux2xOutSInt9_inst39_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst4 (
    .I0(Mux2xOutSInt9_inst2_O),
    .I1(magma_Bits_9_sub_inst1_out),
    .S(magma_Bits_8_eq_inst22_out),
    .O(Mux2xOutSInt9_inst4_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst40 (
    .I0(Mux2xOutSInt9_inst38_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst183_out),
    .O(Mux2xOutSInt9_inst40_O)
);
wire [8:0] Mux2xOutSInt9_inst41_I1;
assign Mux2xOutSInt9_inst41_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst41 (
    .I0(Mux2xOutSInt9_inst39_O),
    .I1(Mux2xOutSInt9_inst41_I1),
    .S(magma_Bit_or_inst28_out),
    .O(Mux2xOutSInt9_inst41_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst42 (
    .I0(Mux2xOutSInt9_inst40_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bit_or_inst31_out),
    .O(Mux2xOutSInt9_inst42_O)
);
wire [8:0] Mux2xOutSInt9_inst5_I1;
assign Mux2xOutSInt9_inst5_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst5 (
    .I0(Mux2xOutSInt9_inst3_O),
    .I1(Mux2xOutSInt9_inst5_I1),
    .S(magma_Bits_8_eq_inst31_out),
    .O(Mux2xOutSInt9_inst5_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst6 (
    .I0(Mux2xOutSInt9_inst4_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst32_out),
    .O(Mux2xOutSInt9_inst6_O)
);
wire [8:0] Mux2xOutSInt9_inst7_I1;
assign Mux2xOutSInt9_inst7_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst7 (
    .I0(Mux2xOutSInt9_inst5_O),
    .I1(Mux2xOutSInt9_inst7_I1),
    .S(magma_Bits_8_eq_inst37_out),
    .O(Mux2xOutSInt9_inst7_O)
);
Mux2xOutSInt9 Mux2xOutSInt9_inst8 (
    .I0(Mux2xOutSInt9_inst6_O),
    .I1(magma_Bits_9_sub_inst0_out),
    .S(magma_Bits_8_eq_inst38_out),
    .O(Mux2xOutSInt9_inst8_O)
);
wire [8:0] Mux2xOutSInt9_inst9_I1;
assign Mux2xOutSInt9_inst9_I1 = {1'b0,a[14:7]};
Mux2xOutSInt9 Mux2xOutSInt9_inst9 (
    .I0(Mux2xOutSInt9_inst7_O),
    .I1(Mux2xOutSInt9_inst9_I1),
    .S(magma_Bits_8_eq_inst45_out),
    .O(Mux2xOutSInt9_inst9_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(magma_Bits_16_lshr_inst0_out),
    .I1(magma_Bits_16_ashr_inst0_out),
    .S(magma_Bits_1_eq_inst5_out),
    .O(Mux2xOutUInt16_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst1 (
    .I0(16'h0000),
    .I1(16'h8000),
    .S(magma_Bits_9_slt_inst0_out),
    .O(Mux2xOutUInt16_inst1_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst10 (
    .I0(magma_Bits_16_neg_inst1_out),
    .I1(a),
    .S(Mux2xOutBit_inst2_O),
    .O(Mux2xOutUInt16_inst10_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst11 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(a),
    .S(d),
    .O(Mux2xOutUInt16_inst11_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst12 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(magma_Bits_16_xor_inst1_out),
    .S(magma_Bit_or_inst3_out),
    .O(Mux2xOutUInt16_inst12_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst13 (
    .I0(magma_Bits_16_shl_inst6_out),
    .I1(magma_Bits_16_lshr_inst2_out),
    .S(magma_Bits_9_slt_inst3_out),
    .O(Mux2xOutUInt16_inst13_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst14 (
    .I0(magma_Bits_16_or_inst1_out),
    .I1(Mux2xOutSInt16_inst29_O),
    .S(magma_Bits_8_eq_inst18_out),
    .O(Mux2xOutUInt16_inst14_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst15 (
    .I0(magma_Bits_16_and_inst12_out),
    .I1(magma_Bits_16_and_inst10_out),
    .S(magma_Bits_8_eq_inst24_out),
    .O(Mux2xOutUInt16_inst15_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst16 (
    .I0(magma_Bits_16_or_inst9_out),
    .I1(magma_Bits_16_or_inst8_out),
    .S(magma_Bits_8_eq_inst25_out),
    .O(Mux2xOutUInt16_inst16_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst17 (
    .I0(magma_Bits_16_and_inst14_out),
    .I1(magma_Bits_23_lshr_inst0_out[15:0]),
    .S(magma_Bits_8_eq_inst26_out),
    .O(Mux2xOutUInt16_inst17_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst18 (
    .I0(Mux2xOutUInt16_inst14_O),
    .I1(Mux2xOutSInt16_inst28_O),
    .S(magma_Bits_8_eq_inst28_out),
    .O(Mux2xOutUInt16_inst18_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst19 (
    .I0(Mux2xOutUInt16_inst18_O),
    .I1(magma_Bits_16_or_inst1_out),
    .S(magma_Bits_8_eq_inst34_out),
    .O(Mux2xOutUInt16_inst19_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst2 (
    .I0(16'h0000),
    .I1(magma_Bits_16_and_inst0_out),
    .S(magma_Bits_1_eq_inst6_out),
    .O(Mux2xOutUInt16_inst2_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst20 (
    .I0(Mux2xOutUInt16_inst15_O),
    .I1(magma_Bits_16_and_inst7_out),
    .S(magma_Bits_8_eq_inst40_out),
    .O(Mux2xOutUInt16_inst20_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst21 (
    .I0(Mux2xOutUInt16_inst16_O),
    .I1(magma_Bits_16_and_inst9_out),
    .S(magma_Bits_8_eq_inst41_out),
    .O(Mux2xOutUInt16_inst21_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst22 (
    .I0(Mux2xOutUInt16_inst19_O),
    .I1(magma_Bits_16_or_inst7_out),
    .S(magma_Bits_8_eq_inst42_out),
    .O(Mux2xOutUInt16_inst22_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst23 (
    .I0(Mux2xOutUInt16_inst4_O),
    .I1(magma_Bits_16_and_inst5_out),
    .S(magma_Bits_8_eq_inst47_out),
    .O(Mux2xOutUInt16_inst23_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst24 (
    .I0(magma_Bits_16_shl_inst5_out),
    .I1(magma_Bits_16_shl_inst4_out),
    .S(magma_Bits_8_eq_inst49_out),
    .O(Mux2xOutUInt16_inst24_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst25 (
    .I0(Mux2xOutUInt16_inst22_O),
    .I1(magma_Bits_16_or_inst4_out),
    .S(magma_Bits_8_eq_inst50_out),
    .O(Mux2xOutUInt16_inst25_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst26 (
    .I0(Mux2xOutUInt16_inst23_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst55_out),
    .O(Mux2xOutUInt16_inst26_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst27 (
    .I0(Mux2xOutUInt16_inst25_O),
    .I1(magma_Bits_16_and_inst4_out),
    .S(magma_Bits_8_eq_inst57_out),
    .O(Mux2xOutUInt16_inst27_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst28 (
    .I0(Mux2xOutUInt16_inst26_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst62_out),
    .O(Mux2xOutUInt16_inst28_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst29 (
    .I0(Mux2xOutUInt16_inst27_O),
    .I1(magma_BFloat_16_mul_inst0_out),
    .S(magma_Bits_8_eq_inst64_out),
    .O(Mux2xOutUInt16_inst29_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst3 (
    .I0(a),
    .I1(magma_Bits_16_neg_inst0_out),
    .S(magma_Bit_not_inst8_out),
    .O(Mux2xOutUInt16_inst3_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst30 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(Mux2xOutUInt16_inst12_O),
    .S(magma_Bit_or_inst5_out),
    .O(Mux2xOutUInt16_inst30_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst31 (
    .I0(Mux2xOutUInt16_inst28_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bit_or_inst13_out),
    .O(Mux2xOutUInt16_inst31_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst32 (
    .I0(Mux2xOutUInt16_inst29_O),
    .I1(magma_BFloat_16_add_inst0_out),
    .S(magma_Bit_or_inst17_out),
    .O(Mux2xOutUInt16_inst32_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst33 (
    .I0(Mux2xOutUInt16_inst30_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst90_out),
    .O(Mux2xOutUInt16_inst33_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst34 (
    .I0(Mux2xOutUInt16_inst31_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst94_out),
    .O(Mux2xOutUInt16_inst34_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst35 (
    .I0(Mux2xOutUInt16_inst32_O),
    .I1(magma_Bits_16_shl_inst2_out),
    .S(magma_Bits_8_eq_inst96_out),
    .O(Mux2xOutUInt16_inst35_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst36 (
    .I0(Mux2xOutUInt16_inst33_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst98_out),
    .O(Mux2xOutUInt16_inst36_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst37 (
    .I0(Mux2xOutUInt16_inst34_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst102_out),
    .O(Mux2xOutUInt16_inst37_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst38 (
    .I0(Mux2xOutUInt16_inst35_O),
    .I1(Mux2xOutUInt16_inst0_O),
    .S(magma_Bits_8_eq_inst104_out),
    .O(Mux2xOutUInt16_inst38_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst39 (
    .I0(Mux2xOutUInt16_inst36_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst106_out),
    .O(Mux2xOutUInt16_inst39_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst4 (
    .I0(Mux2xOutUInt16_inst2_O),
    .I1(Mux2xOutUInt16_inst1_O),
    .S(magma_Bits_8_eq_inst2_out),
    .O(Mux2xOutUInt16_inst4_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst40 (
    .I0(Mux2xOutUInt16_inst37_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst110_out),
    .O(Mux2xOutUInt16_inst40_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst41 (
    .I0(Mux2xOutUInt16_inst38_O),
    .I1(magma_Bits_16_xor_inst0_out),
    .S(magma_Bits_8_eq_inst112_out),
    .O(Mux2xOutUInt16_inst41_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst42 (
    .I0(Mux2xOutUInt16_inst39_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst114_out),
    .O(Mux2xOutUInt16_inst42_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst43 (
    .I0(Mux2xOutUInt16_inst40_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst118_out),
    .O(Mux2xOutUInt16_inst43_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst44 (
    .I0(Mux2xOutUInt16_inst41_O),
    .I1(magma_Bits_16_or_inst2_out),
    .S(magma_Bits_8_eq_inst120_out),
    .O(Mux2xOutUInt16_inst44_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst45 (
    .I0(Mux2xOutUInt16_inst42_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst122_out),
    .O(Mux2xOutUInt16_inst45_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst46 (
    .I0(Mux2xOutUInt16_inst43_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst126_out),
    .O(Mux2xOutUInt16_inst46_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst47 (
    .I0(Mux2xOutUInt16_inst44_O),
    .I1(magma_Bits_16_and_inst3_out),
    .S(magma_Bits_8_eq_inst128_out),
    .O(Mux2xOutUInt16_inst47_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst48 (
    .I0(Mux2xOutUInt16_inst45_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst130_out),
    .O(Mux2xOutUInt16_inst48_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst49 (
    .I0(Mux2xOutUInt16_inst46_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst134_out),
    .O(Mux2xOutUInt16_inst49_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst5 (
    .I0(16'h0000),
    .I1(magma_Bits_16_and_inst1_out),
    .S(magma_Bits_16_sge_inst2_out),
    .O(Mux2xOutUInt16_inst5_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst50 (
    .I0(Mux2xOutUInt16_inst47_O),
    .I1(Mux2xOutUInt16_inst11_O),
    .S(magma_Bits_8_eq_inst136_out),
    .O(Mux2xOutUInt16_inst50_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst51 (
    .I0(Mux2xOutUInt16_inst48_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst138_out),
    .O(Mux2xOutUInt16_inst51_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst52 (
    .I0(Mux2xOutUInt16_inst49_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst142_out),
    .O(Mux2xOutUInt16_inst52_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst53 (
    .I0(Mux2xOutUInt16_inst50_O),
    .I1(Mux2xOutUInt16_inst10_O),
    .S(magma_Bits_8_eq_inst144_out),
    .O(Mux2xOutUInt16_inst53_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst54 (
    .I0(Mux2xOutUInt16_inst51_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst146_out),
    .O(Mux2xOutUInt16_inst54_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst55 (
    .I0(Mux2xOutUInt16_inst52_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst150_out),
    .O(Mux2xOutUInt16_inst55_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst56 (
    .I0(Mux2xOutUInt16_inst53_O),
    .I1(Mux2xOutUInt16_inst9_O),
    .S(magma_Bits_8_eq_inst152_out),
    .O(Mux2xOutUInt16_inst56_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst57 (
    .I0(Mux2xOutUInt16_inst54_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst154_out),
    .O(Mux2xOutUInt16_inst57_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst58 (
    .I0(Mux2xOutUInt16_inst55_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst158_out),
    .O(Mux2xOutUInt16_inst58_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst59 (
    .I0(Mux2xOutUInt16_inst56_O),
    .I1(Mux2xOutUInt16_inst8_O),
    .S(magma_Bits_8_eq_inst160_out),
    .O(Mux2xOutUInt16_inst59_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst6 (
    .I0(Mux2xOutUInt16_inst5_O),
    .I1(magma_Bits_16_lshr_inst1_out),
    .S(magma_Bits_8_eq_inst7_out),
    .O(Mux2xOutUInt16_inst6_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst60 (
    .I0(Mux2xOutUInt16_inst57_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst162_out),
    .O(Mux2xOutUInt16_inst60_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst61 (
    .I0(Mux2xOutUInt16_inst58_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst166_out),
    .O(Mux2xOutUInt16_inst61_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst62 (
    .I0(Mux2xOutUInt16_inst59_O),
    .I1(magma_Bits_32_mul_inst0_out[31:16]),
    .S(magma_Bits_8_eq_inst169_out),
    .O(Mux2xOutUInt16_inst62_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst63 (
    .I0(Mux2xOutUInt16_inst60_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst171_out),
    .O(Mux2xOutUInt16_inst63_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst64 (
    .I0(Mux2xOutUInt16_inst61_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst175_out),
    .O(Mux2xOutUInt16_inst64_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst65 (
    .I0(Mux2xOutUInt16_inst62_O),
    .I1(magma_Bits_32_mul_inst0_out[23:8]),
    .S(magma_Bits_8_eq_inst178_out),
    .O(Mux2xOutUInt16_inst65_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst66 (
    .I0(Mux2xOutUInt16_inst63_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bits_8_eq_inst180_out),
    .O(Mux2xOutUInt16_inst66_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst67 (
    .I0(Mux2xOutUInt16_inst64_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_8_eq_inst184_out),
    .O(Mux2xOutUInt16_inst67_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst68 (
    .I0(Mux2xOutUInt16_inst65_O),
    .I1(magma_Bits_32_mul_inst0_out[15:0]),
    .S(magma_Bits_8_eq_inst187_out),
    .O(Mux2xOutUInt16_inst68_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst69 (
    .I0(Mux2xOutUInt16_inst66_O),
    .I1(Mux2xOutUInt16_inst7_O),
    .S(magma_Bit_or_inst22_out),
    .O(Mux2xOutUInt16_inst69_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst7 (
    .I0(b),
    .I1(magma_Bits_16_not_inst0_out),
    .S(magma_Bit_or_inst0_out),
    .O(Mux2xOutUInt16_inst7_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst70 (
    .I0(Mux2xOutUInt16_inst67_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bit_or_inst34_out),
    .O(Mux2xOutUInt16_inst70_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst71 (
    .I0(Mux2xOutUInt16_inst68_O),
    .I1(magma_Bits_17_add_inst1_out[15:0]),
    .S(magma_Bit_or_inst43_out),
    .O(O0)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst8 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(a),
    .S(Mux2xOutBit_inst0_O),
    .O(Mux2xOutUInt16_inst8_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst9 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(a),
    .S(Mux2xOutBit_inst1_O),
    .O(Mux2xOutUInt16_inst9_O)
);
Mux2xOutUInt23 Mux2xOutUInt23_inst0 (
    .I0(magma_Bits_23_shl_inst0_out),
    .I1(23'h000000),
    .S(magma_Bits_9_slt_inst2_out),
    .O(Mux2xOutUInt23_inst0_O)
);
wire [31:0] Mux2xOutUInt32_inst0_I0;
assign Mux2xOutUInt32_inst0_I0 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,a[15:0]};
wire [31:0] Mux2xOutUInt32_inst0_I1;
assign Mux2xOutUInt32_inst0_I1 = {a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15:0]};
Mux2xOutUInt32 Mux2xOutUInt32_inst0 (
    .I0(Mux2xOutUInt32_inst0_I0),
    .I1(Mux2xOutUInt32_inst0_I1),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xOutUInt32_inst0_O)
);
wire [31:0] Mux2xOutUInt32_inst1_I0;
assign Mux2xOutUInt32_inst1_I0 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,b[15:0]};
wire [31:0] Mux2xOutUInt32_inst1_I1;
assign Mux2xOutUInt32_inst1_I1 = {b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15:0]};
Mux2xOutUInt32 Mux2xOutUInt32_inst1 (
    .I0(Mux2xOutUInt32_inst1_I0),
    .I1(Mux2xOutUInt32_inst1_I1),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xOutUInt32_inst1_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst0 (
    .I0(a[14:7]),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst15_out),
    .O(Mux2xOutUInt8_inst0_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst1 (
    .I0(Mux2xOutUInt8_inst0_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst20_out),
    .O(Mux2xOutUInt8_inst1_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst10 (
    .I0(Mux2xOutUInt8_inst9_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst107_out),
    .O(Mux2xOutUInt8_inst10_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst11 (
    .I0(Mux2xOutUInt8_inst10_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst115_out),
    .O(Mux2xOutUInt8_inst11_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst12 (
    .I0(Mux2xOutUInt8_inst11_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst123_out),
    .O(Mux2xOutUInt8_inst12_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst13 (
    .I0(Mux2xOutUInt8_inst12_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst131_out),
    .O(Mux2xOutUInt8_inst13_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst14 (
    .I0(Mux2xOutUInt8_inst13_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst139_out),
    .O(Mux2xOutUInt8_inst14_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst15 (
    .I0(Mux2xOutUInt8_inst14_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst147_out),
    .O(Mux2xOutUInt8_inst15_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst16 (
    .I0(Mux2xOutUInt8_inst15_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst155_out),
    .O(Mux2xOutUInt8_inst16_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst17 (
    .I0(Mux2xOutUInt8_inst16_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst163_out),
    .O(Mux2xOutUInt8_inst17_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst18 (
    .I0(Mux2xOutUInt8_inst17_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst172_out),
    .O(Mux2xOutUInt8_inst18_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst19 (
    .I0(Mux2xOutUInt8_inst18_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst181_out),
    .O(Mux2xOutUInt8_inst19_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst2 (
    .I0(Mux2xOutUInt8_inst1_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst30_out),
    .O(Mux2xOutUInt8_inst2_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst20 (
    .I0(Mux2xOutUInt8_inst19_O),
    .I1(a[14:7]),
    .S(magma_Bit_or_inst25_out),
    .O(Mux2xOutUInt8_inst20_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst3 (
    .I0(Mux2xOutUInt8_inst2_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst36_out),
    .O(Mux2xOutUInt8_inst3_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst4 (
    .I0(Mux2xOutUInt8_inst3_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst44_out),
    .O(Mux2xOutUInt8_inst4_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst5 (
    .I0(Mux2xOutUInt8_inst4_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst52_out),
    .O(Mux2xOutUInt8_inst5_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst6 (
    .I0(Mux2xOutUInt8_inst5_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst59_out),
    .O(Mux2xOutUInt8_inst6_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst7 (
    .I0(Mux2xOutUInt8_inst6_O),
    .I1(a[14:7]),
    .S(magma_Bit_or_inst7_out),
    .O(Mux2xOutUInt8_inst7_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst8 (
    .I0(Mux2xOutUInt8_inst7_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst91_out),
    .O(Mux2xOutUInt8_inst8_O)
);
Mux2xOutUInt8 Mux2xOutUInt8_inst9 (
    .I0(Mux2xOutUInt8_inst8_O),
    .I1(a[14:7]),
    .S(magma_Bits_8_eq_inst99_out),
    .O(Mux2xOutUInt8_inst9_O)
);
float_add__exp_bits8__frac_bits7 magma_BFloat_16_add_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst12_O),
    .out(magma_BFloat_16_add_inst0_out)
);
float_mul__exp_bits8__frac_bits7 magma_BFloat_16_mul_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst7_O),
    .out(magma_BFloat_16_mul_inst0_out)
);
assign magma_Bit_and_inst6_out = (O0[14:7] == 8'h00) & (O0[6:0] == 7'h00);
assign magma_Bit_and_inst8_out = (((a[14:7] == 8'hff) & (a[6:0] == 7'h00)) & ((b[14:7] == 8'hff) & (b[6:0] == 7'h00))) & (~ (a[15] ^ b[15]));
assign magma_Bit_not_inst0_out = ~ (Mux2xOutSInt9_inst0_O[0] ^ 1'b1);
assign magma_Bit_not_inst1_out = ~ (Mux2xOutSInt9_inst0_O[1] ^ 1'b1);
assign magma_Bit_not_inst10_out = ~ (Mux2xOutUInt16_inst3_O[1] ^ 1'b1);
assign magma_Bit_not_inst11_out = ~ (Mux2xOutUInt16_inst3_O[2] ^ 1'b1);
assign magma_Bit_not_inst12_out = ~ (Mux2xOutUInt16_inst3_O[3] ^ 1'b1);
assign magma_Bit_not_inst13_out = ~ (Mux2xOutUInt16_inst3_O[4] ^ 1'b1);
assign magma_Bit_not_inst14_out = ~ (Mux2xOutUInt16_inst3_O[5] ^ 1'b1);
assign magma_Bit_not_inst15_out = ~ (Mux2xOutUInt16_inst3_O[6] ^ 1'b1);
assign magma_Bit_not_inst16_out = ~ (Mux2xOutUInt16_inst3_O[7] ^ 1'b1);
assign magma_Bit_not_inst17_out = ~ (Mux2xOutUInt16_inst3_O[8] ^ 1'b1);
assign magma_Bit_not_inst18_out = ~ (Mux2xOutUInt16_inst3_O[9] ^ 1'b1);
assign magma_Bit_not_inst19_out = ~ (Mux2xOutUInt16_inst3_O[10] ^ 1'b1);
assign magma_Bit_not_inst2_out = ~ (Mux2xOutSInt9_inst0_O[2] ^ 1'b1);
assign magma_Bit_not_inst20_out = ~ (Mux2xOutUInt16_inst3_O[11] ^ 1'b1);
assign magma_Bit_not_inst21_out = ~ (Mux2xOutUInt16_inst3_O[12] ^ 1'b1);
assign magma_Bit_not_inst22_out = ~ (Mux2xOutUInt16_inst3_O[13] ^ 1'b1);
assign magma_Bit_not_inst23_out = ~ (Mux2xOutUInt16_inst3_O[14] ^ 1'b1);
assign magma_Bit_not_inst24_out = ~ (Mux2xOutUInt16_inst3_O[15] ^ 1'b1);
assign magma_Bit_not_inst3_out = ~ (Mux2xOutSInt9_inst0_O[3] ^ 1'b1);
assign magma_Bit_not_inst4_out = ~ (Mux2xOutSInt9_inst0_O[4] ^ 1'b1);
assign magma_Bit_not_inst5_out = ~ (Mux2xOutSInt9_inst0_O[5] ^ 1'b1);
assign magma_Bit_not_inst6_out = ~ (Mux2xOutSInt9_inst0_O[6] ^ 1'b1);
assign magma_Bit_not_inst7_out = ~ (Mux2xOutSInt9_inst0_O[7] ^ 1'b1);
assign magma_Bit_not_inst8_out = ~ (Mux2xOutUInt16_inst2_O[15] ^ 1'b1);
assign magma_Bit_not_inst9_out = ~ (Mux2xOutUInt16_inst3_O[0] ^ 1'b1);
assign magma_Bit_or_inst0_out = (alu == 8'h01) | (alu == 8'h06);
assign magma_Bit_or_inst1_out = (alu == 8'h02) | (alu == 8'h06);
assign magma_Bit_or_inst11_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst13_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst15_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst17_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst19_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst2_out = ((a[15] & Mux2xOutUInt16_inst7_O[15]) & (~ magma_Bits_17_add_inst1_out[15])) | (((~ a[15]) & (~ Mux2xOutUInt16_inst7_O[15])) & magma_Bits_17_add_inst1_out[15]);
assign magma_Bit_or_inst22_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst25_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst28_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst3_out = (alu == 8'h17) | (alu == 8'h18);
assign magma_Bit_or_inst31_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst34_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst37_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst40_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst43_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst46_out = (((alu == 8'h00) | (alu == 8'h01)) | (alu == 8'h02)) | (alu == 8'h06);
assign magma_Bit_or_inst49_out = (((alu == 8'h17) | (alu == 8'h16)) | (alu == 8'h19)) | (alu == 8'h18);
assign magma_Bit_or_inst5_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst7_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bit_or_inst9_out = ((alu == 8'h16) | (alu == 8'h17)) | (alu == 8'h18);
assign magma_Bits_16_and_inst0_out = a & 16'h8000;
assign magma_Bits_16_and_inst1_out = (Mux2xOutSInt16_inst25_O << Mux2xOutSInt16_inst26_O) & Mux2xOutSInt16_inst27_O;
assign magma_Bits_16_and_inst10_out = a & 16'h8000;
assign magma_Bits_16_and_inst12_out = a & 16'h8000;
assign magma_Bits_16_and_inst14_out = Mux2xOutUInt16_inst13_O & 16'h007f;
assign magma_Bits_16_and_inst3_out = a & Mux2xOutUInt16_inst7_O;
assign magma_Bits_16_and_inst4_out = a & 16'h007f;
assign magma_Bits_16_and_inst5_out = a & 16'h8000;
assign magma_Bits_16_and_inst7_out = a & 16'h8000;
assign magma_Bits_16_and_inst9_out = a & 16'h007f;
assign magma_Bits_16_ashr_inst0_out = ($signed(a)) >>> b;
assign magma_Bits_16_eq_inst0_out = magma_Bits_16_and_inst10_out == 16'h8000;
assign magma_Bits_16_eq_inst1_out = magma_Bits_16_and_inst12_out == 16'h8000;
assign magma_Bits_16_eq_inst2_out = O0 == 16'h0000;
assign magma_Bits_16_lshr_inst0_out = a >> b;
assign magma_Bits_16_lshr_inst1_out = Mux2xOutUInt16_inst5_O >> 16'h0008;
assign magma_Bits_16_lshr_inst2_out = magma_Bits_16_or_inst9_out >> ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_9_neg_inst1_out[8:0]});
assign magma_Bits_16_neg_inst0_out = - a;
assign magma_Bits_16_neg_inst1_out = - a;
assign magma_Bits_16_neg_inst2_out = - magma_Bits_23_lshr_inst0_out[15:0];
assign magma_Bits_16_neg_inst3_out = - magma_Bits_16_and_inst14_out;
assign magma_Bits_16_not_inst0_out = ~ b;
assign magma_Bits_16_or_inst1_out = (Mux2xOutUInt16_inst4_O | (((16'(Mux2xOutSInt16_inst24_O + 16'h007f)) << 16'h0007) & 16'h7f80)) | Mux2xOutUInt16_inst6_O;
assign magma_Bits_16_or_inst2_out = a | Mux2xOutUInt16_inst7_O;
assign magma_Bits_16_or_inst4_out = (magma_Bits_16_and_inst5_out | magma_Bits_16_shl_inst4_out) | (a & 16'h007f);
assign magma_Bits_16_or_inst7_out = ((magma_Bits_16_and_inst7_out | (Mux2xOutUInt16_inst7_O & 16'h8000)) | magma_Bits_16_shl_inst5_out) | magma_Bits_16_and_inst9_out;
assign magma_Bits_16_or_inst8_out = (a & 16'h007f) | 16'h0080;
assign magma_Bits_16_or_inst9_out = (a & 16'h007f) | 16'h0080;
assign magma_Bits_16_sge_inst0_out = ($signed(a)) >= ($signed(b));
assign magma_Bits_16_sge_inst1_out = ($signed(a)) >= ($signed(16'h0000));
assign magma_Bits_16_sge_inst2_out = ($signed(Mux2xOutSInt16_inst24_O)) >= ($signed(16'h0000));
assign magma_Bits_16_shl_inst2_out = a << Mux2xOutUInt16_inst7_O;
assign magma_Bits_16_shl_inst4_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_8_add_inst0_out[7:0]}) << 16'h0007;
assign magma_Bits_16_shl_inst5_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_8_add_inst1_out[7:0]}) << 16'h0007;
assign magma_Bits_16_shl_inst6_out = magma_Bits_16_or_inst9_out << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_9_sub_inst2_out[8:0]});
assign magma_Bits_16_sle_inst0_out = ($signed(a)) <= ($signed(b));
assign magma_Bits_16_sub_inst0_out = 16'(16'h0007 - Mux2xOutSInt16_inst7_O);
assign magma_Bits_16_sub_inst1_out = 16'(16'h000f - Mux2xOutSInt16_inst23_O);
assign magma_Bits_16_uge_inst0_out = a >= b;
assign magma_Bits_16_uge_inst1_out = a >= 16'h0000;
assign magma_Bits_16_ule_inst0_out = a <= b;
assign magma_Bits_16_xor_inst0_out = a ^ Mux2xOutUInt16_inst7_O;
assign magma_Bits_16_xor_inst1_out = (16'h0001 << 16'h000f) ^ Mux2xOutUInt16_inst7_O;
assign magma_Bits_17_add_inst1_out = 17'((17'(({1'b0,a[15:0]}) + ({1'b0,Mux2xOutUInt16_inst7_O[15:0]}))) + ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,Mux2xOutBit_inst4_O}));
assign magma_Bits_1_eq_inst0_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst1_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst2_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst3_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst4_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst5_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst6_out = signed_ == 1'h1;
assign magma_Bits_23_lshr_inst0_out = Mux2xOutUInt23_inst0_O >> 23'h000007;
assign magma_Bits_23_shl_inst0_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_16_or_inst8_out[15:0]}) << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_9_sub_inst1_out[8:0]});
assign magma_Bits_32_mul_inst0_out = 32'(Mux2xOutUInt32_inst0_O * Mux2xOutUInt32_inst1_O);
assign magma_Bits_8_add_inst0_out = 8'(a[14:7] + Mux2xOutUInt16_inst7_O[7:0]);
assign magma_Bits_8_add_inst1_out = 8'((8'(a[14:7] - Mux2xOutUInt16_inst7_O[14:7])) + 8'h7f);
assign magma_Bits_8_eq_inst100_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst101_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst102_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst103_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst104_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst105_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst106_out = alu == 8'h14;
assign magma_Bits_8_eq_inst107_out = alu == 8'h14;
assign magma_Bits_8_eq_inst108_out = alu == 8'h14;
assign magma_Bits_8_eq_inst109_out = alu == 8'h14;
assign magma_Bits_8_eq_inst110_out = alu == 8'h14;
assign magma_Bits_8_eq_inst111_out = alu == 8'h14;
assign magma_Bits_8_eq_inst112_out = alu == 8'h14;
assign magma_Bits_8_eq_inst113_out = alu == 8'h14;
assign magma_Bits_8_eq_inst114_out = alu == 8'h12;
assign magma_Bits_8_eq_inst115_out = alu == 8'h12;
assign magma_Bits_8_eq_inst116_out = alu == 8'h12;
assign magma_Bits_8_eq_inst117_out = alu == 8'h12;
assign magma_Bits_8_eq_inst118_out = alu == 8'h12;
assign magma_Bits_8_eq_inst119_out = alu == 8'h12;
assign magma_Bits_8_eq_inst12_out = alu == 8'h01;
assign magma_Bits_8_eq_inst120_out = alu == 8'h12;
assign magma_Bits_8_eq_inst121_out = alu == 8'h12;
assign magma_Bits_8_eq_inst122_out = alu == 8'h13;
assign magma_Bits_8_eq_inst123_out = alu == 8'h13;
assign magma_Bits_8_eq_inst124_out = alu == 8'h13;
assign magma_Bits_8_eq_inst125_out = alu == 8'h13;
assign magma_Bits_8_eq_inst126_out = alu == 8'h13;
assign magma_Bits_8_eq_inst127_out = alu == 8'h13;
assign magma_Bits_8_eq_inst128_out = alu == 8'h13;
assign magma_Bits_8_eq_inst129_out = alu == 8'h13;
assign magma_Bits_8_eq_inst130_out = alu == 8'h08;
assign magma_Bits_8_eq_inst131_out = alu == 8'h08;
assign magma_Bits_8_eq_inst132_out = alu == 8'h08;
assign magma_Bits_8_eq_inst133_out = alu == 8'h08;
assign magma_Bits_8_eq_inst134_out = alu == 8'h08;
assign magma_Bits_8_eq_inst135_out = alu == 8'h08;
assign magma_Bits_8_eq_inst136_out = alu == 8'h08;
assign magma_Bits_8_eq_inst137_out = alu == 8'h08;
assign magma_Bits_8_eq_inst138_out = alu == 8'h03;
assign magma_Bits_8_eq_inst139_out = alu == 8'h03;
assign magma_Bits_8_eq_inst140_out = alu == 8'h03;
assign magma_Bits_8_eq_inst141_out = alu == 8'h03;
assign magma_Bits_8_eq_inst142_out = alu == 8'h03;
assign magma_Bits_8_eq_inst143_out = alu == 8'h03;
assign magma_Bits_8_eq_inst144_out = alu == 8'h03;
assign magma_Bits_8_eq_inst145_out = alu == 8'h03;
assign magma_Bits_8_eq_inst146_out = alu == 8'h05;
assign magma_Bits_8_eq_inst147_out = alu == 8'h05;
assign magma_Bits_8_eq_inst148_out = alu == 8'h05;
assign magma_Bits_8_eq_inst149_out = alu == 8'h05;
assign magma_Bits_8_eq_inst15_out = alu == 8'h97;
assign magma_Bits_8_eq_inst150_out = alu == 8'h05;
assign magma_Bits_8_eq_inst151_out = alu == 8'h05;
assign magma_Bits_8_eq_inst152_out = alu == 8'h05;
assign magma_Bits_8_eq_inst153_out = alu == 8'h05;
assign magma_Bits_8_eq_inst154_out = alu == 8'h04;
assign magma_Bits_8_eq_inst155_out = alu == 8'h04;
assign magma_Bits_8_eq_inst156_out = alu == 8'h04;
assign magma_Bits_8_eq_inst157_out = alu == 8'h04;
assign magma_Bits_8_eq_inst158_out = alu == 8'h04;
assign magma_Bits_8_eq_inst159_out = alu == 8'h04;
assign magma_Bits_8_eq_inst16_out = alu == 8'h97;
assign magma_Bits_8_eq_inst160_out = alu == 8'h04;
assign magma_Bits_8_eq_inst161_out = alu == 8'h04;
assign magma_Bits_8_eq_inst162_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst163_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst164_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst165_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst166_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst167_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst168_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst169_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst17_out = alu == 8'h97;
assign magma_Bits_8_eq_inst170_out = alu == 8'h0d;
assign magma_Bits_8_eq_inst171_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst172_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst173_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst174_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst175_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst176_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst177_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst178_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst179_out = alu == 8'h0c;
assign magma_Bits_8_eq_inst18_out = alu == 8'h97;
assign magma_Bits_8_eq_inst180_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst181_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst182_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst183_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst184_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst185_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst186_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst187_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst188_out = alu == 8'h0b;
assign magma_Bits_8_eq_inst19_out = alu == 8'h97;
assign magma_Bits_8_eq_inst2_out = alu == 8'h95;
assign magma_Bits_8_eq_inst20_out = alu == 8'h96;
assign magma_Bits_8_eq_inst21_out = alu == 8'h96;
assign magma_Bits_8_eq_inst22_out = alu == 8'h96;
assign magma_Bits_8_eq_inst23_out = alu == 8'h96;
assign magma_Bits_8_eq_inst230_out = alu == 8'h18;
assign magma_Bits_8_eq_inst24_out = alu == 8'h96;
assign magma_Bits_8_eq_inst25_out = alu == 8'h96;
assign magma_Bits_8_eq_inst26_out = alu == 8'h96;
assign magma_Bits_8_eq_inst27_out = alu == 8'h96;
assign magma_Bits_8_eq_inst28_out = alu == 8'h96;
assign magma_Bits_8_eq_inst29_out = alu == 8'h96;
assign magma_Bits_8_eq_inst3_out = alu == 8'h95;
assign magma_Bits_8_eq_inst30_out = alu == 8'h95;
assign magma_Bits_8_eq_inst31_out = alu == 8'h95;
assign magma_Bits_8_eq_inst32_out = alu == 8'h95;
assign magma_Bits_8_eq_inst33_out = alu == 8'h95;
assign magma_Bits_8_eq_inst34_out = alu == 8'h95;
assign magma_Bits_8_eq_inst35_out = alu == 8'h95;
assign magma_Bits_8_eq_inst36_out = alu == 8'h94;
assign magma_Bits_8_eq_inst37_out = alu == 8'h94;
assign magma_Bits_8_eq_inst38_out = alu == 8'h94;
assign magma_Bits_8_eq_inst39_out = alu == 8'h94;
assign magma_Bits_8_eq_inst4_out = alu == 8'h95;
assign magma_Bits_8_eq_inst40_out = alu == 8'h94;
assign magma_Bits_8_eq_inst41_out = alu == 8'h94;
assign magma_Bits_8_eq_inst42_out = alu == 8'h94;
assign magma_Bits_8_eq_inst43_out = alu == 8'h94;
assign magma_Bits_8_eq_inst44_out = alu == 8'h93;
assign magma_Bits_8_eq_inst45_out = alu == 8'h93;
assign magma_Bits_8_eq_inst46_out = alu == 8'h93;
assign magma_Bits_8_eq_inst47_out = alu == 8'h93;
assign magma_Bits_8_eq_inst48_out = alu == 8'h93;
assign magma_Bits_8_eq_inst49_out = alu == 8'h93;
assign magma_Bits_8_eq_inst5_out = alu == 8'h95;
assign magma_Bits_8_eq_inst50_out = alu == 8'h93;
assign magma_Bits_8_eq_inst51_out = alu == 8'h93;
assign magma_Bits_8_eq_inst52_out = alu == 8'h92;
assign magma_Bits_8_eq_inst53_out = alu == 8'h92;
assign magma_Bits_8_eq_inst54_out = alu == 8'h92;
assign magma_Bits_8_eq_inst55_out = alu == 8'h92;
assign magma_Bits_8_eq_inst56_out = alu == 8'h92;
assign magma_Bits_8_eq_inst57_out = alu == 8'h92;
assign magma_Bits_8_eq_inst58_out = alu == 8'h92;
assign magma_Bits_8_eq_inst59_out = alu == 8'h19;
assign magma_Bits_8_eq_inst6_out = alu == 8'h95;
assign magma_Bits_8_eq_inst60_out = alu == 8'h19;
assign magma_Bits_8_eq_inst61_out = alu == 8'h19;
assign magma_Bits_8_eq_inst62_out = alu == 8'h19;
assign magma_Bits_8_eq_inst63_out = alu == 8'h19;
assign magma_Bits_8_eq_inst64_out = alu == 8'h19;
assign magma_Bits_8_eq_inst65_out = alu == 8'h19;
assign magma_Bits_8_eq_inst7_out = alu == 8'h98;
assign magma_Bits_8_eq_inst90_out = alu == 8'h11;
assign magma_Bits_8_eq_inst91_out = alu == 8'h11;
assign magma_Bits_8_eq_inst92_out = alu == 8'h11;
assign magma_Bits_8_eq_inst93_out = alu == 8'h11;
assign magma_Bits_8_eq_inst94_out = alu == 8'h11;
assign magma_Bits_8_eq_inst95_out = alu == 8'h11;
assign magma_Bits_8_eq_inst96_out = alu == 8'h11;
assign magma_Bits_8_eq_inst97_out = alu == 8'h11;
assign magma_Bits_8_eq_inst98_out = alu == 8'h0f;
assign magma_Bits_8_eq_inst99_out = alu == 8'h0f;
assign magma_Bits_8_ugt_inst0_out = a[14:7] > 8'h8e;
assign magma_Bits_9_neg_inst0_out = - magma_Bits_9_sub_inst0_out;
assign magma_Bits_9_neg_inst1_out = - magma_Bits_9_sub_inst2_out;
assign magma_Bits_9_slt_inst0_out = ($signed(magma_Bits_9_sub_inst0_out)) < ($signed(9'h000));
assign magma_Bits_9_slt_inst1_out = ($signed(magma_Bits_9_sub_inst0_out)) < ($signed(9'h000));
assign magma_Bits_9_slt_inst2_out = ($signed(magma_Bits_9_sub_inst1_out)) < ($signed(9'h000));
assign magma_Bits_9_slt_inst3_out = ($signed(magma_Bits_9_sub_inst2_out)) < ($signed(9'h000));
assign magma_Bits_9_sub_inst0_out = 9'(({1'b0,a[14:7]}) - 9'h07f);
assign magma_Bits_9_sub_inst1_out = 9'(({1'b0,a[14:7]}) - 9'h07f);
assign magma_Bits_9_sub_inst2_out = 9'(({1'b0,a[14:7]}) - 9'h07f);
assign magma_Bits_9_ugt_inst0_out = (9'(({1'b0,a[14:7]}) + Mux2xOutUInt16_inst7_O[8:0])) > 9'h0ff;
assign O3 = O0[15];
endmodule

module ALU (
    input [7:0] alu,
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    input d,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5
);
ALU_comb ALU_comb_inst0 (
    .alu(alu),
    .signed_(signed_),
    .a(a),
    .b(b),
    .d(d),
    .O0(O0),
    .O1(O1),
    .O2(O2),
    .O3(O3),
    .O4(O4),
    .O5(O5)
);
endmodule

module PE (
    input [66:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
    input [7:0] config_addr,
    input [31:0] config_data,
    input config_en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1,
    output [31:0] O2
);
wire [15:0] ALU_inst0_O0;
wire ALU_inst0_O1;
wire ALU_inst0_O2;
wire ALU_inst0_O3;
wire ALU_inst0_O4;
wire ALU_inst0_O5;
wire Cond_inst0_O;
wire LUT_inst0_O;
wire [1:0] PE_comb_inst0_O0;
wire [15:0] PE_comb_inst0_O1;
wire [15:0] PE_comb_inst0_O2;
wire PE_comb_inst0_O3;
wire PE_comb_inst0_O4;
wire [15:0] PE_comb_inst0_O5;
wire [1:0] PE_comb_inst0_O6;
wire [15:0] PE_comb_inst0_O7;
wire [15:0] PE_comb_inst0_O8;
wire PE_comb_inst0_O9;
wire PE_comb_inst0_O10;
wire [15:0] PE_comb_inst0_O11;
wire [1:0] PE_comb_inst0_O12;
wire PE_comb_inst0_O13;
wire PE_comb_inst0_O14;
wire PE_comb_inst0_O15;
wire PE_comb_inst0_O16;
wire PE_comb_inst0_O17;
wire [1:0] PE_comb_inst0_O18;
wire PE_comb_inst0_O19;
wire PE_comb_inst0_O20;
wire PE_comb_inst0_O21;
wire PE_comb_inst0_O22;
wire PE_comb_inst0_O23;
wire [1:0] PE_comb_inst0_O24;
wire PE_comb_inst0_O25;
wire PE_comb_inst0_O26;
wire PE_comb_inst0_O27;
wire PE_comb_inst0_O28;
wire PE_comb_inst0_O29;
wire [7:0] PE_comb_inst0_O30;
wire [0:0] PE_comb_inst0_O31;
wire [15:0] PE_comb_inst0_O32;
wire [15:0] PE_comb_inst0_O33;
wire PE_comb_inst0_O34;
wire [4:0] PE_comb_inst0_O35;
wire PE_comb_inst0_O36;
wire PE_comb_inst0_O37;
wire PE_comb_inst0_O38;
wire PE_comb_inst0_O39;
wire PE_comb_inst0_O40;
wire PE_comb_inst0_O41;
wire [7:0] PE_comb_inst0_O42;
wire PE_comb_inst0_O43;
wire PE_comb_inst0_O44;
wire PE_comb_inst0_O45;
wire [15:0] RegisterMode_inst0_O0;
wire [15:0] RegisterMode_inst0_O1;
wire [15:0] RegisterMode_inst1_O0;
wire [15:0] RegisterMode_inst1_O1;
wire RegisterMode_inst2_O0;
wire RegisterMode_inst2_O1;
wire RegisterMode_inst3_O0;
wire RegisterMode_inst3_O1;
wire RegisterMode_inst4_O0;
wire RegisterMode_inst4_O1;
ALU ALU_inst0 (
    .alu(PE_comb_inst0_O30),
    .signed_(PE_comb_inst0_O31),
    .a(PE_comb_inst0_O32),
    .b(PE_comb_inst0_O33),
    .d(PE_comb_inst0_O34),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(ALU_inst0_O0),
    .O1(ALU_inst0_O1),
    .O2(ALU_inst0_O2),
    .O3(ALU_inst0_O3),
    .O4(ALU_inst0_O4),
    .O5(ALU_inst0_O5)
);
Cond Cond_inst0 (
    .code(PE_comb_inst0_O35),
    .alu(PE_comb_inst0_O36),
    .lut(PE_comb_inst0_O37),
    .Z(PE_comb_inst0_O38),
    .N(PE_comb_inst0_O39),
    .C(PE_comb_inst0_O40),
    .V(PE_comb_inst0_O41),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(Cond_inst0_O)
);
LUT LUT_inst0 (
    .lut(PE_comb_inst0_O42),
    .bit0(PE_comb_inst0_O43),
    .bit1(PE_comb_inst0_O44),
    .bit2(PE_comb_inst0_O45),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O(LUT_inst0_O)
);
PE_comb PE_comb_inst0 (
    .inst(inst),
    .data0(data0),
    .data1(data1),
    .bit0(bit0),
    .bit1(bit1),
    .bit2(bit2),
    .clk_en(clk_en),
    .config_addr(config_addr),
    .config_data(config_data),
    .config_en(config_en),
    .self_rega_O0(RegisterMode_inst0_O0),
    .self_rega_O1(RegisterMode_inst0_O1),
    .self_regb_O0(RegisterMode_inst1_O0),
    .self_regb_O1(RegisterMode_inst1_O1),
    .self_regd_O0(RegisterMode_inst2_O0),
    .self_regd_O1(RegisterMode_inst2_O1),
    .self_rege_O0(RegisterMode_inst3_O0),
    .self_rege_O1(RegisterMode_inst3_O1),
    .self_regf_O0(RegisterMode_inst4_O0),
    .self_regf_O1(RegisterMode_inst4_O1),
    .self_alu_O0(ALU_inst0_O0),
    .self_alu_O1(ALU_inst0_O1),
    .self_alu_O2(ALU_inst0_O2),
    .self_alu_O3(ALU_inst0_O3),
    .self_alu_O4(ALU_inst0_O4),
    .self_alu_O5(ALU_inst0_O5),
    .self_cond_O(Cond_inst0_O),
    .self_lut_O(LUT_inst0_O),
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
    .O44(PE_comb_inst0_O44),
    .O45(PE_comb_inst0_O45),
    .O46(O0),
    .O47(O1),
    .O48(O2)
);
RegisterMode RegisterMode_inst0 (
    .mode(PE_comb_inst0_O0),
    .const_(PE_comb_inst0_O1),
    .value(PE_comb_inst0_O2),
    .clk_en(PE_comb_inst0_O3),
    .config_we(PE_comb_inst0_O4),
    .config_data(PE_comb_inst0_O5),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(RegisterMode_inst0_O0),
    .O1(RegisterMode_inst0_O1)
);
RegisterMode RegisterMode_inst1 (
    .mode(PE_comb_inst0_O6),
    .const_(PE_comb_inst0_O7),
    .value(PE_comb_inst0_O8),
    .clk_en(PE_comb_inst0_O9),
    .config_we(PE_comb_inst0_O10),
    .config_data(PE_comb_inst0_O11),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(RegisterMode_inst1_O0),
    .O1(RegisterMode_inst1_O1)
);
RegisterMode_unq1 RegisterMode_inst2 (
    .mode(PE_comb_inst0_O12),
    .const_(PE_comb_inst0_O13),
    .value(PE_comb_inst0_O14),
    .clk_en(PE_comb_inst0_O15),
    .config_we(PE_comb_inst0_O16),
    .config_data(PE_comb_inst0_O17),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(RegisterMode_inst2_O0),
    .O1(RegisterMode_inst2_O1)
);
RegisterMode_unq1 RegisterMode_inst3 (
    .mode(PE_comb_inst0_O18),
    .const_(PE_comb_inst0_O19),
    .value(PE_comb_inst0_O20),
    .clk_en(PE_comb_inst0_O21),
    .config_we(PE_comb_inst0_O22),
    .config_data(PE_comb_inst0_O23),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(RegisterMode_inst3_O0),
    .O1(RegisterMode_inst3_O1)
);
RegisterMode_unq1 RegisterMode_inst4 (
    .mode(PE_comb_inst0_O24),
    .const_(PE_comb_inst0_O25),
    .value(PE_comb_inst0_O26),
    .clk_en(PE_comb_inst0_O27),
    .config_we(PE_comb_inst0_O28),
    .config_data(PE_comb_inst0_O29),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(RegisterMode_inst4_O0),
    .O1(RegisterMode_inst4_O1)
);
endmodule

module WrappedPE (
    input [66:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
    input [7:0] config_addr,
    input [31:0] config_data,
    input config_en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1,
    output [31:0] O2
);
PE PE_inst0 (
    .inst(inst),
    .data0(data0),
    .data1(data1),
    .bit0(bit0),
    .bit1(bit1),
    .bit2(bit2),
    .clk_en(clk_en),
    .config_addr(config_addr),
    .config_data(config_data),
    .config_en(config_en),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(O0),
    .O1(O1),
    .O2(O2)
);
endmodule

