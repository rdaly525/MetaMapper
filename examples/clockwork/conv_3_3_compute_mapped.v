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

module PE_comb (
    input [62:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
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
    output [4:0] O30,
    output [0:0] O31,
    output [15:0] O32,
    output [15:0] O33,
    output O34,
    output [3:0] O35,
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
    output O47
);
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
assign magma_Bit_and_inst0_out = (3'h0 == 3'h3) & 1'b0;
assign magma_Bit_and_inst1_out = (3'h0 == 3'h4) & 1'b0;
assign O0 = inst[19:18];
assign O1 = inst[35:20];
assign O2 = data0;
assign O3 = clk_en;
assign O4 = magma_Bit_and_inst0_out;
assign O5 = 16'h0000;
assign O6 = inst[37:36];
assign O7 = inst[53:38];
assign O8 = data1;
assign O9 = clk_en;
assign O10 = magma_Bit_and_inst0_out;
assign O11 = 16'h0000;
assign O12 = inst[55:54];
assign O13 = inst[56];
assign O14 = bit0;
assign O15 = clk_en;
assign O16 = magma_Bit_and_inst1_out;
assign O17 = 1'b0;
assign O18 = inst[58:57];
assign O19 = inst[59];
assign O20 = bit1;
assign O21 = clk_en;
assign O22 = magma_Bit_and_inst1_out;
assign O23 = 1'b0;
assign O24 = inst[61:60];
assign O25 = inst[62];
assign O26 = bit2;
assign O27 = clk_en;
assign O28 = magma_Bit_and_inst1_out;
assign O29 = 1'b0;
assign O30 = inst[4:0];
assign O31 = inst[5];
assign O32 = self_rega_O0;
assign O33 = self_regb_O0;
assign O34 = self_regd_O0;
assign O35 = inst[17:14];
assign O36 = self_alu_O1;
assign O37 = self_lut_O;
assign O38 = self_alu_O2;
assign O39 = self_alu_O3;
assign O40 = self_alu_O4;
assign O41 = self_alu_O5;
assign O42 = inst[13:6];
assign O43 = self_regd_O0;
assign O44 = self_rege_O0;
assign O45 = self_regf_O0;
assign O46 = self_alu_O0;
assign O47 = self_cond_O;
endmodule

module Mux2xUInt32 (
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

module Mux2xUInt16 (
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
Mux2xUInt16 Mux2xUInt16_inst0 (
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

module Mux2xBit (
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
Mux2xBit Mux2xBit_inst0 (
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
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
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
Mux2xBit Mux2xBit_inst0 (
    .I0(value),
    .I1(value),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(1'b0),
    .I1(clk_en),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(Mux2xBit_inst6_O),
    .I1(Mux2xBit_inst3_O),
    .S(magma_Bits_2_eq_inst11_out),
    .O(O0)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(Mux2xBit_inst7_O),
    .I1(Mux2xBit_inst4_O),
    .S(magma_Bits_2_eq_inst12_out),
    .O(O1)
);
Mux2xBit Mux2xBit_inst12 (
    .I0(Mux2xBit_inst8_O),
    .I1(const_),
    .S(magma_Bits_2_eq_inst13_out),
    .O(O2)
);
Mux2xBit Mux2xBit_inst13 (
    .I0(Mux2xBit_inst9_O),
    .I1(Mux2xBit_inst5_O),
    .S(magma_Bits_2_eq_inst14_out),
    .O(O3)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(self_register_O),
    .I1(self_register_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(Mux2xBit_inst0_O),
    .I1(config_data),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(Mux2xBit_inst1_O),
    .I1(1'b1),
    .S(magma_Bit_not_inst1_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(Mux2xBit_inst2_O),
    .I1(self_register_O),
    .S(magma_Bit_not_inst2_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(Mux2xBit_inst3_O),
    .I1(Mux2xBit_inst3_O),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(Mux2xBit_inst4_O),
    .I1(Mux2xBit_inst4_O),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(Mux2xBit_inst5_O),
    .I1(value),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(Mux2xBit_inst5_O),
    .I1(Mux2xBit_inst5_O),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xBit_inst9_O)
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
Mux2xBit Mux2xBit_inst0 (
    .I0(1'b0),
    .I1(clk_en),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(Mux2xBit_inst0_O),
    .I1(1'b1),
    .S(magma_Bit_not_inst1_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(Mux2xBit_inst1_O),
    .I1(Mux2xBit_inst1_O),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(Mux2xBit_inst2_O),
    .I1(Mux2xBit_inst1_O),
    .S(magma_Bits_2_eq_inst12_out),
    .O(O1)
);
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(value),
    .I1(value),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xUInt16_inst0_O)
);
Mux2xUInt16 Mux2xUInt16_inst1 (
    .I0(self_register_O),
    .I1(self_register_O),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xUInt16_inst1_O)
);
Mux2xUInt16 Mux2xUInt16_inst2 (
    .I0(Mux2xUInt16_inst0_O),
    .I1(config_data),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xUInt16_inst2_O)
);
Mux2xUInt16 Mux2xUInt16_inst3 (
    .I0(Mux2xUInt16_inst1_O),
    .I1(self_register_O),
    .S(magma_Bit_not_inst2_out),
    .O(Mux2xUInt16_inst3_O)
);
Mux2xUInt16 Mux2xUInt16_inst4 (
    .I0(Mux2xUInt16_inst2_O),
    .I1(Mux2xUInt16_inst2_O),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xUInt16_inst4_O)
);
Mux2xUInt16 Mux2xUInt16_inst5 (
    .I0(Mux2xUInt16_inst3_O),
    .I1(value),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xUInt16_inst5_O)
);
Mux2xUInt16 Mux2xUInt16_inst6 (
    .I0(Mux2xUInt16_inst3_O),
    .I1(Mux2xUInt16_inst3_O),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xUInt16_inst6_O)
);
Mux2xUInt16 Mux2xUInt16_inst7 (
    .I0(Mux2xUInt16_inst4_O),
    .I1(Mux2xUInt16_inst2_O),
    .S(magma_Bits_2_eq_inst11_out),
    .O(O0)
);
Mux2xUInt16 Mux2xUInt16_inst8 (
    .I0(Mux2xUInt16_inst5_O),
    .I1(const_),
    .S(magma_Bits_2_eq_inst13_out),
    .O(O2)
);
Mux2xUInt16 Mux2xUInt16_inst9 (
    .I0(Mux2xUInt16_inst6_O),
    .I1(Mux2xUInt16_inst3_O),
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
    input [3:0] code,
    input alu,
    input lut,
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
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst100_out;
wire magma_Bit_and_inst103_out;
wire magma_Bit_and_inst105_out;
wire magma_Bit_and_inst106_out;
wire magma_Bit_and_inst15_out;
wire magma_Bit_and_inst28_out;
wire magma_Bit_and_inst40_out;
wire magma_Bit_and_inst51_out;
wire magma_Bit_and_inst61_out;
wire magma_Bit_and_inst70_out;
wire magma_Bit_and_inst78_out;
wire magma_Bit_and_inst85_out;
wire magma_Bit_and_inst91_out;
wire magma_Bit_and_inst96_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst6_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_xor_inst1_out;
wire magma_Bits_4_eq_inst144_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(lut),
    .I1(alu),
    .S(magma_Bit_and_inst15_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(Mux2xBit_inst0_O),
    .I1(magma_Bit_or_inst1_out),
    .S(magma_Bit_and_inst28_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(Mux2xBit_inst9_O),
    .I1(N),
    .S(magma_Bit_and_inst100_out),
    .O(Mux2xBit_inst10_O)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(Mux2xBit_inst10_O),
    .I1(magma_Bit_not_inst1_out),
    .S(magma_Bit_and_inst103_out),
    .O(Mux2xBit_inst11_O)
);
Mux2xBit Mux2xBit_inst12 (
    .I0(Mux2xBit_inst11_O),
    .I1(C),
    .S(magma_Bit_and_inst105_out),
    .O(Mux2xBit_inst12_O)
);
Mux2xBit Mux2xBit_inst13 (
    .I0(Mux2xBit_inst12_O),
    .I1(magma_Bit_not_inst0_out),
    .S(magma_Bit_and_inst106_out),
    .O(Mux2xBit_inst13_O)
);
Mux2xBit Mux2xBit_inst14 (
    .I0(Mux2xBit_inst13_O),
    .I1(Z),
    .S(magma_Bits_4_eq_inst144_out),
    .O(O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(Mux2xBit_inst1_O),
    .I1(magma_Bit_and_inst1_out),
    .S(magma_Bit_and_inst40_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(Mux2xBit_inst2_O),
    .I1(magma_Bit_xor_inst1_out),
    .S(magma_Bit_and_inst51_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(Mux2xBit_inst3_O),
    .I1(magma_Bit_not_inst6_out),
    .S(magma_Bit_and_inst61_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(Mux2xBit_inst4_O),
    .I1(magma_Bit_or_inst0_out),
    .S(magma_Bit_and_inst70_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(Mux2xBit_inst5_O),
    .I1(magma_Bit_and_inst0_out),
    .S(magma_Bit_and_inst78_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(Mux2xBit_inst6_O),
    .I1(magma_Bit_not_inst3_out),
    .S(magma_Bit_and_inst85_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(Mux2xBit_inst7_O),
    .I1(V),
    .S(magma_Bit_and_inst91_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(Mux2xBit_inst8_O),
    .I1(magma_Bit_not_inst2_out),
    .S(magma_Bit_and_inst96_out),
    .O(Mux2xBit_inst9_O)
);
assign magma_Bit_and_inst0_out = C & (~ Z);
assign magma_Bit_and_inst1_out = (~ Z) & (~ (N ^ V));
assign magma_Bit_and_inst100_out = ((((code == 4'h4) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)));
assign magma_Bit_and_inst103_out = ((((code == 4'h3) | (code == 4'h3)) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)));
assign magma_Bit_and_inst105_out = (((code == 4'h2) | (code == 4'h2)) & (~ (code == 4'h0))) & (~ (code == 4'h1));
assign magma_Bit_and_inst106_out = (code == 4'h1) & (~ (code == 4'h0));
assign magma_Bit_and_inst15_out = ((((((((((((((code == 4'hf) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8))) & (~ (code == 4'h9))) & (~ (code == 4'ha))) & (~ (code == 4'hb))) & (~ (code == 4'hc))) & (~ (code == 4'hd));
assign magma_Bit_and_inst28_out = (((((((((((((code == 4'hd) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8))) & (~ (code == 4'h9))) & (~ (code == 4'ha))) & (~ (code == 4'hb))) & (~ (code == 4'hc));
assign magma_Bit_and_inst40_out = ((((((((((((code == 4'hc) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8))) & (~ (code == 4'h9))) & (~ (code == 4'ha))) & (~ (code == 4'hb));
assign magma_Bit_and_inst51_out = (((((((((((code == 4'hb) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8))) & (~ (code == 4'h9))) & (~ (code == 4'ha));
assign magma_Bit_and_inst61_out = ((((((((((code == 4'ha) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8))) & (~ (code == 4'h9));
assign magma_Bit_and_inst70_out = (((((((((code == 4'h9) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7))) & (~ (code == 4'h8));
assign magma_Bit_and_inst78_out = ((((((((code == 4'h8) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6))) & (~ (code == 4'h7));
assign magma_Bit_and_inst85_out = (((((((code == 4'h7) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5))) & (~ (code == 4'h6));
assign magma_Bit_and_inst91_out = ((((((code == 4'h6) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4))) & (~ (code == 4'h5));
assign magma_Bit_and_inst96_out = (((((code == 4'h5) & (~ (code == 4'h0))) & (~ (code == 4'h1))) & (~ ((code == 4'h2) | (code == 4'h2)))) & (~ ((code == 4'h3) | (code == 4'h3)))) & (~ (code == 4'h4));
assign magma_Bit_not_inst0_out = ~ Z;
assign magma_Bit_not_inst1_out = ~ C;
assign magma_Bit_not_inst2_out = ~ N;
assign magma_Bit_not_inst3_out = ~ V;
assign magma_Bit_not_inst6_out = ~ (N ^ V);
assign magma_Bit_or_inst0_out = (~ C) | Z;
assign magma_Bit_or_inst1_out = Z | (N ^ V);
assign magma_Bit_xor_inst1_out = N ^ V;
assign magma_Bits_4_eq_inst144_out = code == 4'h0;
endmodule

module Cond (
    input [3:0] code,
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
    input [4:0] alu,
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
wire Mux2xBit_inst18_O;
wire Mux2xBit_inst19_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst20_O;
wire Mux2xBit_inst21_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [15:0] Mux2xOutUInt16_inst1_O;
wire [15:0] Mux2xOutUInt16_inst2_O;
wire [15:0] Mux2xOutUInt16_inst3_O;
wire [15:0] Mux2xUInt16_inst0_O;
wire [15:0] Mux2xUInt16_inst1_O;
wire [15:0] Mux2xUInt16_inst10_O;
wire [15:0] Mux2xUInt16_inst11_O;
wire [15:0] Mux2xUInt16_inst12_O;
wire [15:0] Mux2xUInt16_inst2_O;
wire [15:0] Mux2xUInt16_inst3_O;
wire [15:0] Mux2xUInt16_inst4_O;
wire [15:0] Mux2xUInt16_inst5_O;
wire [15:0] Mux2xUInt16_inst6_O;
wire [15:0] Mux2xUInt16_inst7_O;
wire [15:0] Mux2xUInt16_inst8_O;
wire [15:0] Mux2xUInt16_inst9_O;
wire [31:0] Mux2xUInt32_inst0_O;
wire [31:0] Mux2xUInt32_inst1_O;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst11_out;
wire magma_Bit_or_inst14_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst5_out;
wire magma_Bit_or_inst8_out;
wire [15:0] magma_Bits_16_and_inst0_out;
wire [15:0] magma_Bits_16_ashr_inst0_out;
wire [15:0] magma_Bits_16_lshr_inst0_out;
wire [15:0] magma_Bits_16_neg_inst0_out;
wire [15:0] magma_Bits_16_not_inst0_out;
wire [15:0] magma_Bits_16_or_inst0_out;
wire magma_Bits_16_sge_inst0_out;
wire magma_Bits_16_sge_inst1_out;
wire [15:0] magma_Bits_16_shl_inst0_out;
wire magma_Bits_16_sle_inst0_out;
wire magma_Bits_16_uge_inst0_out;
wire magma_Bits_16_uge_inst1_out;
wire magma_Bits_16_ule_inst0_out;
wire [15:0] magma_Bits_16_xor_inst0_out;
wire [16:0] magma_Bits_17_add_inst1_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire magma_Bits_1_eq_inst3_out;
wire magma_Bits_1_eq_inst4_out;
wire magma_Bits_1_eq_inst5_out;
wire [31:0] magma_Bits_32_mul_inst0_out;
wire magma_Bits_5_eq_inst10_out;
wire magma_Bits_5_eq_inst11_out;
wire magma_Bits_5_eq_inst12_out;
wire magma_Bits_5_eq_inst13_out;
wire magma_Bits_5_eq_inst14_out;
wire magma_Bits_5_eq_inst15_out;
wire magma_Bits_5_eq_inst16_out;
wire magma_Bits_5_eq_inst17_out;
wire magma_Bits_5_eq_inst18_out;
wire magma_Bits_5_eq_inst19_out;
wire magma_Bits_5_eq_inst20_out;
wire magma_Bits_5_eq_inst21_out;
wire magma_Bits_5_eq_inst22_out;
wire magma_Bits_5_eq_inst23_out;
wire magma_Bits_5_eq_inst24_out;
wire magma_Bits_5_eq_inst25_out;
wire magma_Bits_5_eq_inst26_out;
wire magma_Bits_5_eq_inst27_out;
wire magma_Bits_5_eq_inst28_out;
wire magma_Bits_5_eq_inst29_out;
wire magma_Bits_5_eq_inst30_out;
wire magma_Bits_5_eq_inst31_out;
wire magma_Bits_5_eq_inst32_out;
wire magma_Bits_5_eq_inst4_out;
wire magma_Bits_5_eq_inst5_out;
wire magma_Bits_5_eq_inst6_out;
wire magma_Bits_5_eq_inst7_out;
wire magma_Bits_5_eq_inst8_out;
wire magma_Bits_5_eq_inst9_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(magma_Bits_16_uge_inst0_out),
    .I1(magma_Bits_16_sge_inst0_out),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(magma_Bits_16_ule_inst0_out),
    .I1(magma_Bits_16_sle_inst0_out),
    .S(magma_Bits_1_eq_inst3_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(Mux2xBit_inst9_O),
    .I1(a[15]),
    .S(magma_Bits_5_eq_inst16_out),
    .O(Mux2xBit_inst10_O)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(Mux2xBit_inst10_O),
    .I1(Mux2xBit_inst1_O),
    .S(magma_Bits_5_eq_inst18_out),
    .O(Mux2xBit_inst11_O)
);
Mux2xBit Mux2xBit_inst12 (
    .I0(Mux2xBit_inst11_O),
    .I1(Mux2xBit_inst0_O),
    .S(magma_Bits_5_eq_inst20_out),
    .O(Mux2xBit_inst12_O)
);
Mux2xBit Mux2xBit_inst13 (
    .I0(1'b0),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst21_out),
    .O(Mux2xBit_inst13_O)
);
Mux2xBit Mux2xBit_inst14 (
    .I0(1'b0),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst22_out),
    .O(Mux2xBit_inst14_O)
);
Mux2xBit Mux2xBit_inst15 (
    .I0(Mux2xBit_inst12_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst24_out),
    .O(Mux2xBit_inst15_O)
);
Mux2xBit Mux2xBit_inst16 (
    .I0(Mux2xBit_inst13_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst25_out),
    .O(Mux2xBit_inst16_O)
);
Mux2xBit Mux2xBit_inst17 (
    .I0(Mux2xBit_inst14_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst26_out),
    .O(Mux2xBit_inst17_O)
);
Mux2xBit Mux2xBit_inst18 (
    .I0(Mux2xBit_inst15_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst28_out),
    .O(Mux2xBit_inst18_O)
);
Mux2xBit Mux2xBit_inst19 (
    .I0(Mux2xBit_inst16_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst29_out),
    .O(Mux2xBit_inst19_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(magma_Bits_16_uge_inst1_out),
    .I1(magma_Bits_16_sge_inst1_out),
    .S(magma_Bits_1_eq_inst4_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst20 (
    .I0(Mux2xBit_inst17_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst30_out),
    .O(Mux2xBit_inst20_O)
);
Mux2xBit Mux2xBit_inst21 (
    .I0(Mux2xBit_inst18_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst32_out),
    .O(Mux2xBit_inst21_O)
);
Mux2xBit Mux2xBit_inst22 (
    .I0(Mux2xBit_inst19_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst5_out),
    .O(O4)
);
Mux2xBit Mux2xBit_inst23 (
    .I0(Mux2xBit_inst20_O),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bit_or_inst8_out),
    .O(O5)
);
Mux2xBit Mux2xBit_inst24 (
    .I0(Mux2xBit_inst21_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst14_out),
    .O(O1)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(1'b0),
    .I1(d),
    .S(magma_Bit_or_inst1_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(Mux2xBit_inst3_O),
    .I1(1'b1),
    .S(magma_Bits_5_eq_inst4_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(1'b0),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst6_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(Mux2xBit_inst5_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst8_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(Mux2xBit_inst6_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst10_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(Mux2xBit_inst7_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst12_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(Mux2xBit_inst8_O),
    .I1(1'b0),
    .S(magma_Bits_5_eq_inst14_out),
    .O(Mux2xBit_inst9_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(Mux2xUInt16_inst1_O),
    .I1(a),
    .S(Mux2xBit_inst0_O),
    .O(Mux2xOutUInt16_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst1 (
    .I0(Mux2xUInt16_inst1_O),
    .I1(a),
    .S(Mux2xBit_inst1_O),
    .O(Mux2xOutUInt16_inst1_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst2 (
    .I0(magma_Bits_16_neg_inst0_out),
    .I1(a),
    .S(Mux2xBit_inst2_O),
    .O(Mux2xOutUInt16_inst2_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst3 (
    .I0(Mux2xUInt16_inst1_O),
    .I1(a),
    .S(d),
    .O(Mux2xOutUInt16_inst3_O)
);
Mux2xUInt16 Mux2xUInt16_inst0 (
    .I0(magma_Bits_16_lshr_inst0_out),
    .I1(magma_Bits_16_ashr_inst0_out),
    .S(magma_Bits_1_eq_inst5_out),
    .O(Mux2xUInt16_inst0_O)
);
Mux2xUInt16 Mux2xUInt16_inst1 (
    .I0(b),
    .I1(magma_Bits_16_not_inst0_out),
    .S(magma_Bit_or_inst0_out),
    .O(Mux2xUInt16_inst1_O)
);
Mux2xUInt16 Mux2xUInt16_inst10 (
    .I0(Mux2xUInt16_inst9_O),
    .I1(magma_Bits_32_mul_inst0_out[31:16]),
    .S(magma_Bits_5_eq_inst23_out),
    .O(Mux2xUInt16_inst10_O)
);
Mux2xUInt16 Mux2xUInt16_inst11 (
    .I0(Mux2xUInt16_inst10_O),
    .I1(magma_Bits_32_mul_inst0_out[23:8]),
    .S(magma_Bits_5_eq_inst27_out),
    .O(Mux2xUInt16_inst11_O)
);
Mux2xUInt16 Mux2xUInt16_inst12 (
    .I0(Mux2xUInt16_inst11_O),
    .I1(magma_Bits_32_mul_inst0_out[15:0]),
    .S(magma_Bits_5_eq_inst31_out),
    .O(Mux2xUInt16_inst12_O)
);
Mux2xUInt16 Mux2xUInt16_inst13 (
    .I0(Mux2xUInt16_inst12_O),
    .I1(magma_Bits_17_add_inst1_out[15:0]),
    .S(magma_Bit_or_inst11_out),
    .O(O0)
);
Mux2xUInt16 Mux2xUInt16_inst2 (
    .I0(magma_Bits_16_shl_inst0_out),
    .I1(Mux2xUInt16_inst0_O),
    .S(magma_Bits_5_eq_inst5_out),
    .O(Mux2xUInt16_inst2_O)
);
Mux2xUInt16 Mux2xUInt16_inst3 (
    .I0(Mux2xUInt16_inst2_O),
    .I1(magma_Bits_16_xor_inst0_out),
    .S(magma_Bits_5_eq_inst7_out),
    .O(Mux2xUInt16_inst3_O)
);
Mux2xUInt16 Mux2xUInt16_inst4 (
    .I0(Mux2xUInt16_inst3_O),
    .I1(magma_Bits_16_or_inst0_out),
    .S(magma_Bits_5_eq_inst9_out),
    .O(Mux2xUInt16_inst4_O)
);
Mux2xUInt16 Mux2xUInt16_inst5 (
    .I0(Mux2xUInt16_inst4_O),
    .I1(magma_Bits_16_and_inst0_out),
    .S(magma_Bits_5_eq_inst11_out),
    .O(Mux2xUInt16_inst5_O)
);
Mux2xUInt16 Mux2xUInt16_inst6 (
    .I0(Mux2xUInt16_inst5_O),
    .I1(Mux2xOutUInt16_inst3_O),
    .S(magma_Bits_5_eq_inst13_out),
    .O(Mux2xUInt16_inst6_O)
);
Mux2xUInt16 Mux2xUInt16_inst7 (
    .I0(Mux2xUInt16_inst6_O),
    .I1(Mux2xOutUInt16_inst2_O),
    .S(magma_Bits_5_eq_inst15_out),
    .O(Mux2xUInt16_inst7_O)
);
Mux2xUInt16 Mux2xUInt16_inst8 (
    .I0(Mux2xUInt16_inst7_O),
    .I1(Mux2xOutUInt16_inst1_O),
    .S(magma_Bits_5_eq_inst17_out),
    .O(Mux2xUInt16_inst8_O)
);
Mux2xUInt16 Mux2xUInt16_inst9 (
    .I0(Mux2xUInt16_inst8_O),
    .I1(Mux2xOutUInt16_inst0_O),
    .S(magma_Bits_5_eq_inst19_out),
    .O(Mux2xUInt16_inst9_O)
);
wire [31:0] Mux2xUInt32_inst0_I0;
assign Mux2xUInt32_inst0_I0 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,a[15:0]};
wire [31:0] Mux2xUInt32_inst0_I1;
assign Mux2xUInt32_inst0_I1 = {a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15:0]};
Mux2xUInt32 Mux2xUInt32_inst0 (
    .I0(Mux2xUInt32_inst0_I0),
    .I1(Mux2xUInt32_inst0_I1),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xUInt32_inst0_O)
);
wire [31:0] Mux2xUInt32_inst1_I0;
assign Mux2xUInt32_inst1_I0 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,b[15:0]};
wire [31:0] Mux2xUInt32_inst1_I1;
assign Mux2xUInt32_inst1_I1 = {b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15:0]};
Mux2xUInt32 Mux2xUInt32_inst1 (
    .I0(Mux2xUInt32_inst1_I0),
    .I1(Mux2xUInt32_inst1_I1),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xUInt32_inst1_O)
);
assign magma_Bit_or_inst0_out = (alu == 5'h01) | (alu == 5'h06);
assign magma_Bit_or_inst1_out = (alu == 5'h02) | (alu == 5'h06);
assign magma_Bit_or_inst11_out = (((alu == 5'h00) | (alu == 5'h01)) | (alu == 5'h02)) | (alu == 5'h06);
assign magma_Bit_or_inst14_out = (((alu == 5'h00) | (alu == 5'h01)) | (alu == 5'h02)) | (alu == 5'h06);
assign magma_Bit_or_inst2_out = ((a[15] & Mux2xUInt16_inst1_O[15]) & (~ magma_Bits_17_add_inst1_out[15])) | (((~ a[15]) & (~ Mux2xUInt16_inst1_O[15])) & magma_Bits_17_add_inst1_out[15]);
assign magma_Bit_or_inst5_out = (((alu == 5'h00) | (alu == 5'h01)) | (alu == 5'h02)) | (alu == 5'h06);
assign magma_Bit_or_inst8_out = (((alu == 5'h00) | (alu == 5'h01)) | (alu == 5'h02)) | (alu == 5'h06);
assign magma_Bits_16_and_inst0_out = a & Mux2xUInt16_inst1_O;
assign magma_Bits_16_ashr_inst0_out = ($signed(a)) >>> b;
assign magma_Bits_16_lshr_inst0_out = a >> b;
assign magma_Bits_16_neg_inst0_out = - a;
assign magma_Bits_16_not_inst0_out = ~ b;
assign magma_Bits_16_or_inst0_out = a | Mux2xUInt16_inst1_O;
assign magma_Bits_16_sge_inst0_out = ($signed(a)) >= ($signed(b));
assign magma_Bits_16_sge_inst1_out = ($signed(a)) >= ($signed(16'h0000));
assign magma_Bits_16_shl_inst0_out = a << Mux2xUInt16_inst1_O;
assign magma_Bits_16_sle_inst0_out = ($signed(a)) <= ($signed(b));
assign magma_Bits_16_uge_inst0_out = a >= b;
assign magma_Bits_16_uge_inst1_out = a >= 16'h0000;
assign magma_Bits_16_ule_inst0_out = a <= b;
assign magma_Bits_16_xor_inst0_out = a ^ Mux2xUInt16_inst1_O;
assign magma_Bits_17_add_inst1_out = 17'((17'(({1'b0,a[15:0]}) + ({1'b0,Mux2xUInt16_inst1_O[15:0]}))) + ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,Mux2xBit_inst4_O}));
assign magma_Bits_1_eq_inst0_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst1_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst2_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst3_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst4_out = signed_ == 1'h1;
assign magma_Bits_1_eq_inst5_out = signed_ == 1'h1;
assign magma_Bits_32_mul_inst0_out = 32'(Mux2xUInt32_inst0_O * Mux2xUInt32_inst1_O);
assign magma_Bits_5_eq_inst10_out = alu == 5'h12;
assign magma_Bits_5_eq_inst11_out = alu == 5'h13;
assign magma_Bits_5_eq_inst12_out = alu == 5'h13;
assign magma_Bits_5_eq_inst13_out = alu == 5'h08;
assign magma_Bits_5_eq_inst14_out = alu == 5'h08;
assign magma_Bits_5_eq_inst15_out = alu == 5'h03;
assign magma_Bits_5_eq_inst16_out = alu == 5'h03;
assign magma_Bits_5_eq_inst17_out = alu == 5'h05;
assign magma_Bits_5_eq_inst18_out = alu == 5'h05;
assign magma_Bits_5_eq_inst19_out = alu == 5'h04;
assign magma_Bits_5_eq_inst20_out = alu == 5'h04;
assign magma_Bits_5_eq_inst21_out = alu == 5'h0d;
assign magma_Bits_5_eq_inst22_out = alu == 5'h0d;
assign magma_Bits_5_eq_inst23_out = alu == 5'h0d;
assign magma_Bits_5_eq_inst24_out = alu == 5'h0d;
assign magma_Bits_5_eq_inst25_out = alu == 5'h0c;
assign magma_Bits_5_eq_inst26_out = alu == 5'h0c;
assign magma_Bits_5_eq_inst27_out = alu == 5'h0c;
assign magma_Bits_5_eq_inst28_out = alu == 5'h0c;
assign magma_Bits_5_eq_inst29_out = alu == 5'h0b;
assign magma_Bits_5_eq_inst30_out = alu == 5'h0b;
assign magma_Bits_5_eq_inst31_out = alu == 5'h0b;
assign magma_Bits_5_eq_inst32_out = alu == 5'h0b;
assign magma_Bits_5_eq_inst4_out = alu == 5'h01;
assign magma_Bits_5_eq_inst5_out = alu == 5'h0f;
assign magma_Bits_5_eq_inst6_out = alu == 5'h0f;
assign magma_Bits_5_eq_inst7_out = alu == 5'h14;
assign magma_Bits_5_eq_inst8_out = alu == 5'h14;
assign magma_Bits_5_eq_inst9_out = alu == 5'h12;
assign O2 = O0 == 16'h0000;
assign O3 = O0[15];
endmodule

module ALU (
    input [4:0] alu,
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
    input [62:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1
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
wire [4:0] PE_comb_inst0_O30;
wire [0:0] PE_comb_inst0_O31;
wire [15:0] PE_comb_inst0_O32;
wire [15:0] PE_comb_inst0_O33;
wire PE_comb_inst0_O34;
wire [3:0] PE_comb_inst0_O35;
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
    .O47(O1)
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
    input [62:0] inst,
    input [15:0] data0,
    input [15:0] data1,
    input bit0,
    input bit1,
    input bit2,
    input clk_en,
    input CLK,
    input ASYNCRESET,
    output [15:0] O0,
    output O1
);
PE PE_inst0 (
    .inst(inst),
    .data0(data0),
    .data1(data1),
    .bit0(bit0),
    .bit1(bit1),
    .bit2(bit2),
    .clk_en(clk_en),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET),
    .O0(O0),
    .O1(O1)
);
endmodule

