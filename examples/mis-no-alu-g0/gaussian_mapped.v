module mapping_function_4 (
    input [15:0] in0,
    input [15:0] in1,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
assign O = 16'(in0 + in1);
endmodule

