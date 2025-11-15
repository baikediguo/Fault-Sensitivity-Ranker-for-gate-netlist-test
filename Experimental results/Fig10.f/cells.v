module DFFX1 (D, CLK, Q, QN); input D; input CLK; output reg Q; output QN; always @(posedge CLK) Q <= D; assign QN = ~Q; endmodule
module NBUFFX2 (INP, Z); input INP; output Z; assign Z = INP; endmodule
module INVX0 (INP, ZN); input INP; output ZN; assign ZN = ~INP; endmodule
module AND2X1 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 & IN2; endmodule
module OR2X1 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 | IN2; endmodule
module NAND2X0 (IN1, IN2, QN); input IN1; input IN2; output QN; assign QN = ~(IN1 & IN2); endmodule
module NOR2X0 (IN1, IN2, QN); input IN1; input IN2; output QN; assign QN = ~(IN1 | IN2); endmodule
module OR2X2 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 | IN2; endmodule
module OR2X4 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 | IN2; endmodule
module AND2X4 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 & IN2; endmodule
module AND2X2 (IN1, IN2, Q); input IN1; input IN2; output Q; assign Q = IN1 & IN2; endmodule
module NBUFFX4 (INP, Z); input INP; output Z; assign Z = INP; endmodule
module NAND2X1 (IN1, IN2, QN); input IN1; input IN2; output QN; assign QN = ~(IN1 & IN2); endmodule
module DFFX2 (D, CLK, Q, QN); input D; input CLK; output reg Q; output QN; always @(posedge CLK) Q <= D; assign QN = ~Q; endmodule
module INVX32 (INP, ZN); input INP; output ZN; assign ZN = ~INP; endmodule
