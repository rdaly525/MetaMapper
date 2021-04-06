module mapping_function_17 (
    input [15:0] in0,
    input [15:0] in1,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
assign O = 16'(in1 + in0);
endmodule

