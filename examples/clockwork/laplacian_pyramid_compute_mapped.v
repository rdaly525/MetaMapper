module mapping_function_9 (
    input [15:0] in1,
    input [15:0] in2,
    input CLK,
    input ASYNCRESET,
    output [15:0] O
);
assign O = in2 >> in1;
endmodule

