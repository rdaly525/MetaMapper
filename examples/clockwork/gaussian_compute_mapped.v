module mapping_function_24 (
    input [15:0] in1,
    input [15:0] in0,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
assign O = in0 >> in1;
endmodule

