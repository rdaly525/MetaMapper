module mapping_function_11 (
    input [15:0] in2,
    input [15:0] in1,
    input CLK,
    input ASYNCRESET,
    output O
);
assign O = ($signed(in2)) <= ($signed(in1));
endmodule

