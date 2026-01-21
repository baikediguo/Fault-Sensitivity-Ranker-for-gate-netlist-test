/* ============================================================================
   文件名: simulation_models.v
   用途: 包含所有仿真所需的模型 (标准单元 + Stratix IV 黑盒逻辑)
   包含:
     1. 标准逻辑门 (BUF, NAND2, TIEHI...) - 对应 simple_plus.lib
     2. 标准触发器 (DFF, DFF_SR...) - 对应 simple_plus.lib
     3. Stratix IV LUT (stratixiv_lcell_comb) - 官方全逻辑模型
     4. Stratix IV FF  (dffeas) - 官方接口的行为级实现
     5. Stratix IV VPR 模块 (RAM/MAC 等) - 支持 VPR 命名格式
   ============================================================================ */

`timescale 1 ps/1 ps

// ============================================================
// PART 1: 标准单元库 (Standard Cells)
// 对应 simple_plus.lib，用于处理 Yosys 生成的连线和胶水逻辑
// ============================================================

module BUF (A, Y);
    input A; output Y;
    assign Y = A;
endmodule

module INV (A, Y);
    input A; output Y;
    assign Y = ~A;
endmodule

module AND2 (A, B, Y);
    input A, B; output Y;
    assign Y = A & B;
endmodule

module AND2B (A, B, Y);
    input A, B; output Y;
    assign Y = ~A & B;
endmodule

module OR2 (A, B, Y);
    input A, B; output Y;
    assign Y = A | B;
endmodule

module OR2B (A, B, Y);
    input A, B; output Y;
    assign Y = ~A | B;
endmodule

module NAND2 (A, B, Y);
    input A, B; output Y;
    assign Y = ~(A & B);
endmodule

module NOR2 (A, B, Y);
    input A, B; output Y;
    assign Y = ~(A | B);
endmodule

module XOR2 (A, B, Y);
    input A, B; output Y;
    assign Y = A ^ B;
endmodule

module MUX2 (A, B, S, Y);
    input A, B, S; output Y;
    assign Y = (S) ? B : A; 
endmodule

module TIEHI (Y);
    output Y; assign Y = 1'b1;
endmodule

module TIELO (Y);
    output Y; assign Y = 1'b0;
endmodule

// --- 标准 DFF (用于 Yosys 映射的通用触发器) ---

module DFF (C, D, Q);
    input C, D; output reg Q = 0;  // 初始化为 0，避免 X
    always @(posedge C) Q <= D;
endmodule

module DFF_RST (C, D, R, Q);
    input C, D, R; output reg Q = 0;
    always @(posedge C or negedge R) 
        if (!R) Q <= 1'b0; else Q <= D;
endmodule

module DFF_SET (C, D, S, Q);
    input C, D, S; output reg Q = 0;
    always @(posedge C or negedge S) 
        if (!S) Q <= 1'b1; else Q <= D;
endmodule

module DFF_SR (C, D, R, S, Q);
    input C, D, R, S; output reg Q = 0;
    always @(posedge C or negedge R or negedge S) begin
        if (!R) Q <= 1'b0;
        else if (!S) Q <= 1'b1;
        else Q <= D;
    end
endmodule


// ============================================================
// PART 2: Stratix IV 查找表 (LCELL_COMB)
// 包含完整的 LUT_MASK 解析逻辑
// ============================================================

module stratixiv_lcell_comb (
    input dataa, datab, datac, datad, datae, dataf, datag,
    input cin, sharein,
    output combout, sumout, cout, shareout
);
    parameter lut_mask = 64'hFFFFFFFFFFFFFFFF;
    parameter shared_arith = "off";
    parameter extended_lut = "off";
    parameter dont_touch = "off";
    parameter lpm_type = "stratixiv_lcell_comb";

    // 内部信号定义
    wire [15:0] f0_mask = lut_mask[15:0];
    wire [15:0] f1_mask = lut_mask[31:16];
    wire [15:0] f2_mask = lut_mask[47:32];
    wire [15:0] f3_mask = lut_mask[63:48];
    
    reg f0_out, f1_out, f2_out, f3_out;
    reg g0_out, g1_out;
    reg f2_input3;
    reg f2_f;
    reg adder_input2;
    reg combout_tmp, sumout_tmp, cout_tmp;
    
    integer ishared_arith;
    integer iextended_lut;

    // LUT4 函数
    function lut4;
        input [15:0] mask;
        input da, db, dc, dd;
        begin
            lut4 = dd ? (dc ? (db ? (da ? mask[15] : mask[14]) : (da ? mask[13] : mask[12])) 
                            : (db ? (da ? mask[11] : mask[10]) : (da ? mask[9]  : mask[8])))
                      : (dc ? (db ? (da ? mask[7]  : mask[6])  : (da ? mask[5]  : mask[4]))
                            : (db ? (da ? mask[3]  : mask[2])  : (da ? mask[1]  : mask[0])));
        end
    endfunction

    // LUT5 函数
    function lut5;
        input [31:0] mask;
        input da, db, dc, dd, de;
        reg e0, e1;
        begin
            e0 = lut4(mask[15:0],  da, db, dc, dd);
            e1 = lut4(mask[31:16], da, db, dc, dd);
            lut5 = (de === 1'b1) ? e1 : e0;
        end
    endfunction

    // LUT6 函数
    function lut6;
        input [63:0] mask;
        input da, db, dc, dd, de, df;
        reg f0, f1;
        begin
            f0 = lut5(mask[31:0],  da, db, dc, dd, de);
            f1 = lut5(mask[63:32], da, db, dc, dd, de);
            lut6 = (df === 1'b1) ? f1 : f0;
        end
    endfunction

    // 参数处理
    initial begin
        ishared_arith = (shared_arith == "on") ? 1 : 0;
        iextended_lut = (extended_lut == "on") ? 1 : 0;
    end

    // 核心逻辑计算
    always @(*) begin
        // 扩展模式检查
        f2_input3 = (iextended_lut == 1) ? datag : datac;

        // 计算 4个 子LUT
        f0_out = lut4(f0_mask, dataa, datab, datac, datad);
        f1_out = lut4(f1_mask, dataa, datab, f2_input3, datad);
        f2_out = lut4(f2_mask, dataa, datab, datac, datad);
        f3_out = lut4(f3_mask, dataa, datab, f2_input3, datad);

        // 组合输出逻辑
        if (iextended_lut == 1) begin
            if (datae == 1'b0) begin
                g0_out = f0_out; g1_out = f2_out;
            end else if (datae == 1'b1) begin
                g0_out = f1_out; g1_out = f3_out;
            end else begin
                g0_out = (f0_out == f1_out) ? f0_out : 1'bX;
                g1_out = (f2_out == f3_out) ? f2_out : 1'bX;
            end

            if (dataf == 1'b0) combout_tmp = g0_out;
            else if (dataf == 1'b1) combout_tmp = g1_out;
            else combout_tmp = (g0_out == g1_out) ? g0_out : 1'bX;
        end 
        else begin
            combout_tmp = lut6(lut_mask, dataa, datab, datac, datad, datae, dataf);
        end

        // 算术/进位链逻辑
        if (ishared_arith == 1) 
            adder_input2 = sharein;
        else begin
            f2_f = lut4(f2_mask, dataa, datab, datac, dataf);
            adder_input2 = !f2_f;
        end

        sumout_tmp = cin ^ f0_out ^ adder_input2;
        cout_tmp = (cin & f0_out) | (cin & adder_input2) | (f0_out & adder_input2);
    end

    assign combout = combout_tmp;
    assign sumout  = sumout_tmp;
    assign cout    = cout_tmp;
    assign shareout = f2_out;

endmodule


// ============================================================
// PART 3: Stratix IV 触发器 (DFFEAS)
// 行为级实现，不依赖底层原语，保证兼容性
// ============================================================

module dffeas (
    input d,
    input clk,
    input ena,
    input clrn,  // 异步复位 (Active Low)
    input prn,   // 异步置位 (Active Low)
    input aload, // 异步加载 (Active High)
    input asdata,// 异步加载数据
    input sclr,  // 同步清零 (Active High)
    input sload, // 同步加载 (Active High)
    input devclrn, 
    input devpor,
    output q
);

    parameter power_up = "dont_care";
    parameter is_wysiwyg = "false";
    parameter dont_touch = "false";
    parameter x_on_violation = "on";
    parameter sclr_over_ena = "false";
    parameter lpm_type = "dffeas";

    reg q_reg;
    wire reset_n;
    wire preset_n;

    // 处理全局复位信号
    assign reset_n = clrn && devclrn && devpor;
    assign preset_n = prn;

    // 初始化
    initial begin
        if (power_up == "high") q_reg = 1'b1;
        else q_reg = 1'b0;
    end

    // 核心时序逻辑
    // 优先级: 异步复位 > 异步置位 > 异步加载 > 同步逻辑
    always @(posedge clk or negedge reset_n or negedge preset_n or posedge aload) begin
        if (reset_n == 1'b0) begin
            q_reg <= 1'b0;
        end
        else if (preset_n == 1'b0) begin
            q_reg <= 1'b1;
        end
        else if (aload == 1'b1) begin
            q_reg <= asdata;
        end
        else begin
            // 同步逻辑 (受 Enable 控制)
            if (ena == 1'b1) begin
                if (sclr == 1'b1) begin
                    q_reg <= 1'b0;      // 同步清零
                end
                else if (sload == 1'b1) begin
                    q_reg <= asdata;    // 同步加载
                end
                else begin
                    q_reg <= d;         // 正常数据
                end
            end
        end
    end

    assign q = q_reg;

endmodule

module DFFX1 (D, CLK, Q, QN); input D; input CLK; output reg Q = 0; output QN; always @(posedge CLK) Q <= D; assign QN = ~Q; endmodule
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
module DFFX2 (D, CLK, Q, QN); input D; input CLK; output reg Q = 0; output QN; always @(posedge CLK) Q <= D; assign QN = ~Q; endmodule
module INVX32 (INP, ZN); input INP; output ZN; assign ZN = ~INP; endmodule


// ============================================================
// PART 4: Stratix IV VPR 命名格式模块 (Escaped Identifiers)
// 用于支持 VPR 生成的带参数编码的模块名
// ============================================================

// --- stratixiv_mac_mult 变体 ---
module \stratixiv_mac_mult.input_type{reg} (
    input [17:0] dataa, datab,
    input signa, signb,
    input clk, aclr, ena,
    output reg [35:0] dataout
);
    initial dataout = 0;
    wire signed [17:0] a_s = signa ? $signed(dataa) : $signed({1'b0, dataa[16:0]});
    wire signed [17:0] b_s = signb ? $signed(datab) : $signed({1'b0, datab[16:0]});
    wire signed [35:0] product = a_s * b_s;
    always @(posedge clk or posedge aclr)
        if (aclr) dataout <= 0;
        else if (ena) dataout <= product;
endmodule

module \stratixiv_mac_mult.input_type{comb} (
    input [17:0] dataa, datab,
    input signa, signb,
    output [35:0] dataout
);
    wire signed [17:0] a_s = signa ? $signed(dataa) : $signed({1'b0, dataa[16:0]});
    wire signed [17:0] b_s = signb ? $signed(datab) : $signed({1'b0, datab[16:0]});
    assign dataout = a_s * b_s;
endmodule

// --- stratixiv_mac_out 变体 ---
module \stratixiv_mac_out.opmode{36_bit_multiply}.input_type{reg}.output_type{reg} (
    input [71:0] dataa,
    input clk, aclr, ena,
    input signa, signb,
    output reg [71:0] dataout
);
    initial dataout = 0;
    always @(posedge clk or posedge aclr)
        if (aclr) dataout <= 0;
        else if (ena) dataout <= dataa;
endmodule

module \stratixiv_mac_out.opmode{36_bit_multiply}.input_type{comb}.output_type{comb} (
    input [35:0] dataa,
    output [35:0] dataout
);
    assign dataout = dataa;
endmodule

module \stratixiv_mac_out.opmode{36_bit_multiply}.input_type{comb}.output_type{reg} (
    input [35:0] dataa,
    input clk, aclr, ena,
    output reg [35:0] dataout
);
    initial dataout = 0;
    always @(posedge clk or posedge aclr)
        if (aclr) dataout <= 0;
        else if (ena) dataout <= dataa;
endmodule

module \stratixiv_mac_out.opmode{double}.input_type{comb}.output_type{reg} (
    input [71:0] dataa,
    input clk, aclr, ena,
    output reg [71:0] dataout
);
    initial dataout = 0;
    always @(posedge clk or posedge aclr)
        if (aclr) dataout <= 0;
        else if (ena) dataout <= dataa;
endmodule

module \stratixiv_mac_out.opmode{output_only}.input_type{comb}.output_type{comb} (
    input [35:0] dataa,
    output [35:0] dataout
);
    assign dataout = dataa;
endmodule

// --- stratixiv_ram_block 变体 (双端口 RAM) ---

// Address width 4
module \stratixiv_ram_block.opmode{dual_port}.output_type{reg}.port_a_address_width{4}.port_b_address_width{4} (
    input [17:0] portadatain,
    input [3:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output reg [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:15];
    initial begin portadataout = 0; portbdataout = 0; end
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    always @(posedge clk1) if (ena1 && portbre) portbdataout <= mem[portbaddr];
endmodule

// Address width 5
module \stratixiv_ram_block.opmode{dual_port}.output_type{reg}.port_a_address_width{5}.port_b_address_width{5} (
    input [17:0] portadatain,
    input [4:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output reg [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:31];
    initial begin portadataout = 0; portbdataout = 0; end
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    always @(posedge clk1) if (ena1 && portbre) portbdataout <= mem[portbaddr];
endmodule

// Address width 6
module \stratixiv_ram_block.opmode{dual_port}.output_type{reg}.port_a_address_width{6}.port_b_address_width{6} (
    input [17:0] portadatain,
    input [5:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output reg [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:63];
    initial begin portadataout = 0; portbdataout = 0; end
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    always @(posedge clk1) if (ena1 && portbre) portbdataout <= mem[portbaddr];
endmodule

// Address width 7
module \stratixiv_ram_block.opmode{dual_port}.output_type{reg}.port_a_address_width{7}.port_b_address_width{7} (
    input [17:0] portadatain,
    input [6:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output reg [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:127];
    initial begin portadataout = 0; portbdataout = 0; end
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    always @(posedge clk1) if (ena1 && portbre) portbdataout <= mem[portbaddr];
endmodule

// Address width 8
module \stratixiv_ram_block.opmode{dual_port}.output_type{reg}.port_a_address_width{8}.port_b_address_width{8} (
    input [17:0] portadatain,
    input [7:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output reg [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:255];
    initial begin portadataout = 0; portbdataout = 0; end
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    always @(posedge clk1) if (ena1 && portbre) portbdataout <= mem[portbaddr];
endmodule

// Combinational output variants
module \stratixiv_ram_block.opmode{dual_port}.output_type{comb}.port_a_address_width{3}.port_b_address_width{3} (
    input [17:0] portadatain,
    input [2:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:7];
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    assign portbdataout = mem[portbaddr];
    assign portadataout = mem[portaaddr];
endmodule

module \stratixiv_ram_block.opmode{dual_port}.output_type{comb}.port_a_address_width{13}.port_b_address_width{13} (
    input [17:0] portadatain,
    input [12:0] portaaddr, portbaddr,
    input portawe, portbre,
    input clk0, clk1, ena0, ena1,
    input clr0, clr1,
    input devclrn, devpor,
    output [17:0] portadataout, portbdataout
);
    reg [17:0] mem [0:8191];
    always @(posedge clk0) if (ena0 && portawe) mem[portaaddr] <= portadatain;
    assign portbdataout = mem[portbaddr];
    assign portadataout = mem[portaaddr];
endmodule

// ROM variants
module \stratixiv_ram_block.opmode{rom}.output_type{comb}.port_a_address_width{1} (
    input [0:0] portaaddr,
    input clk0, ena0,
    input devclrn, devpor,
    output [17:0] portadataout
);
    reg [17:0] mem [0:1];
    initial begin mem[0] = 0; mem[1] = 0; end
    assign portadataout = mem[portaaddr];
endmodule

module \stratixiv_ram_block.opmode{rom}.output_type{comb}.port_a_address_width{9} (
    input [8:0] portaaddr,
    input clk0, ena0,
    input devclrn, devpor,
    output [17:0] portadataout
);
    reg [17:0] mem [0:511];
    assign portadataout = mem[portaaddr];
endmodule
