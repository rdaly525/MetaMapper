module mapping_function_14 (
    input [15:0] in0,
    input [15:0] in1,
    input CLK,
    input ASYNCRESET,
    output O
);
assign O = in1 == in0;
endmodule

