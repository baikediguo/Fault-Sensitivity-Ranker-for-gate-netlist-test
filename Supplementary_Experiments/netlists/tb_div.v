`timescale 1ns / 1ps

module tb;

  reg [63:0] a_vec;
  reg [63:0] b_vec;
  wire [63:0] q_vec;
  wire [63:0] r_vec;

  top uut (
    .\a[0] (a_vec[0]),     .\a[1] (a_vec[1]),     .\a[2] (a_vec[2]),     .\a[3] (a_vec[3]),     .\a[4] (a_vec[4]),     .\a[5] (a_vec[5]),     .\a[6] (a_vec[6]),     .\a[7] (a_vec[7]), 
    .\a[8] (a_vec[8]),     .\a[9] (a_vec[9]),     .\a[10] (a_vec[10]),     .\a[11] (a_vec[11]),     .\a[12] (a_vec[12]),     .\a[13] (a_vec[13]),     .\a[14] (a_vec[14]),     .\a[15] (a_vec[15]), 
    .\a[16] (a_vec[16]),     .\a[17] (a_vec[17]),     .\a[18] (a_vec[18]),     .\a[19] (a_vec[19]),     .\a[20] (a_vec[20]),     .\a[21] (a_vec[21]),     .\a[22] (a_vec[22]),     .\a[23] (a_vec[23]), 
    .\a[24] (a_vec[24]),     .\a[25] (a_vec[25]),     .\a[26] (a_vec[26]),     .\a[27] (a_vec[27]),     .\a[28] (a_vec[28]),     .\a[29] (a_vec[29]),     .\a[30] (a_vec[30]),     .\a[31] (a_vec[31]), 
    .\a[32] (a_vec[32]),     .\a[33] (a_vec[33]),     .\a[34] (a_vec[34]),     .\a[35] (a_vec[35]),     .\a[36] (a_vec[36]),     .\a[37] (a_vec[37]),     .\a[38] (a_vec[38]),     .\a[39] (a_vec[39]), 
    .\a[40] (a_vec[40]),     .\a[41] (a_vec[41]),     .\a[42] (a_vec[42]),     .\a[43] (a_vec[43]),     .\a[44] (a_vec[44]),     .\a[45] (a_vec[45]),     .\a[46] (a_vec[46]),     .\a[47] (a_vec[47]), 
    .\a[48] (a_vec[48]),     .\a[49] (a_vec[49]),     .\a[50] (a_vec[50]),     .\a[51] (a_vec[51]),     .\a[52] (a_vec[52]),     .\a[53] (a_vec[53]),     .\a[54] (a_vec[54]),     .\a[55] (a_vec[55]), 
    .\a[56] (a_vec[56]),     .\a[57] (a_vec[57]),     .\a[58] (a_vec[58]),     .\a[59] (a_vec[59]),     .\a[60] (a_vec[60]),     .\a[61] (a_vec[61]),     .\a[62] (a_vec[62]),     .\a[63] (a_vec[63]), 
    .\b[0] (b_vec[0]),     .\b[1] (b_vec[1]),     .\b[2] (b_vec[2]),     .\b[3] (b_vec[3]),     .\b[4] (b_vec[4]),     .\b[5] (b_vec[5]),     .\b[6] (b_vec[6]),     .\b[7] (b_vec[7]), 
    .\b[8] (b_vec[8]),     .\b[9] (b_vec[9]),     .\b[10] (b_vec[10]),     .\b[11] (b_vec[11]),     .\b[12] (b_vec[12]),     .\b[13] (b_vec[13]),     .\b[14] (b_vec[14]),     .\b[15] (b_vec[15]), 
    .\b[16] (b_vec[16]),     .\b[17] (b_vec[17]),     .\b[18] (b_vec[18]),     .\b[19] (b_vec[19]),     .\b[20] (b_vec[20]),     .\b[21] (b_vec[21]),     .\b[22] (b_vec[22]),     .\b[23] (b_vec[23]), 
    .\b[24] (b_vec[24]),     .\b[25] (b_vec[25]),     .\b[26] (b_vec[26]),     .\b[27] (b_vec[27]),     .\b[28] (b_vec[28]),     .\b[29] (b_vec[29]),     .\b[30] (b_vec[30]),     .\b[31] (b_vec[31]), 
    .\b[32] (b_vec[32]),     .\b[33] (b_vec[33]),     .\b[34] (b_vec[34]),     .\b[35] (b_vec[35]),     .\b[36] (b_vec[36]),     .\b[37] (b_vec[37]),     .\b[38] (b_vec[38]),     .\b[39] (b_vec[39]), 
    .\b[40] (b_vec[40]),     .\b[41] (b_vec[41]),     .\b[42] (b_vec[42]),     .\b[43] (b_vec[43]),     .\b[44] (b_vec[44]),     .\b[45] (b_vec[45]),     .\b[46] (b_vec[46]),     .\b[47] (b_vec[47]), 
    .\b[48] (b_vec[48]),     .\b[49] (b_vec[49]),     .\b[50] (b_vec[50]),     .\b[51] (b_vec[51]),     .\b[52] (b_vec[52]),     .\b[53] (b_vec[53]),     .\b[54] (b_vec[54]),     .\b[55] (b_vec[55]), 
    .\b[56] (b_vec[56]),     .\b[57] (b_vec[57]),     .\b[58] (b_vec[58]),     .\b[59] (b_vec[59]),     .\b[60] (b_vec[60]),     .\b[61] (b_vec[61]),     .\b[62] (b_vec[62]),     .\b[63] (b_vec[63]), 
    .\quotient[0] (q_vec[0]),     .\quotient[1] (q_vec[1]),     .\quotient[2] (q_vec[2]),     .\quotient[3] (q_vec[3]),     .\quotient[4] (q_vec[4]),     .\quotient[5] (q_vec[5]),     .\quotient[6] (q_vec[6]),     .\quotient[7] (q_vec[7]), 
    .\quotient[8] (q_vec[8]),     .\quotient[9] (q_vec[9]),     .\quotient[10] (q_vec[10]),     .\quotient[11] (q_vec[11]),     .\quotient[12] (q_vec[12]),     .\quotient[13] (q_vec[13]),     .\quotient[14] (q_vec[14]),     .\quotient[15] (q_vec[15]), 
    .\quotient[16] (q_vec[16]),     .\quotient[17] (q_vec[17]),     .\quotient[18] (q_vec[18]),     .\quotient[19] (q_vec[19]),     .\quotient[20] (q_vec[20]),     .\quotient[21] (q_vec[21]),     .\quotient[22] (q_vec[22]),     .\quotient[23] (q_vec[23]), 
    .\quotient[24] (q_vec[24]),     .\quotient[25] (q_vec[25]),     .\quotient[26] (q_vec[26]),     .\quotient[27] (q_vec[27]),     .\quotient[28] (q_vec[28]),     .\quotient[29] (q_vec[29]),     .\quotient[30] (q_vec[30]),     .\quotient[31] (q_vec[31]), 
    .\quotient[32] (q_vec[32]),     .\quotient[33] (q_vec[33]),     .\quotient[34] (q_vec[34]),     .\quotient[35] (q_vec[35]),     .\quotient[36] (q_vec[36]),     .\quotient[37] (q_vec[37]),     .\quotient[38] (q_vec[38]),     .\quotient[39] (q_vec[39]), 
    .\quotient[40] (q_vec[40]),     .\quotient[41] (q_vec[41]),     .\quotient[42] (q_vec[42]),     .\quotient[43] (q_vec[43]),     .\quotient[44] (q_vec[44]),     .\quotient[45] (q_vec[45]),     .\quotient[46] (q_vec[46]),     .\quotient[47] (q_vec[47]), 
    .\quotient[48] (q_vec[48]),     .\quotient[49] (q_vec[49]),     .\quotient[50] (q_vec[50]),     .\quotient[51] (q_vec[51]),     .\quotient[52] (q_vec[52]),     .\quotient[53] (q_vec[53]),     .\quotient[54] (q_vec[54]),     .\quotient[55] (q_vec[55]), 
    .\quotient[56] (q_vec[56]),     .\quotient[57] (q_vec[57]),     .\quotient[58] (q_vec[58]),     .\quotient[59] (q_vec[59]),     .\quotient[60] (q_vec[60]),     .\quotient[61] (q_vec[61]),     .\quotient[62] (q_vec[62]),     .\quotient[63] (q_vec[63]), 
    .\remainder[0] (r_vec[0]),     .\remainder[1] (r_vec[1]),     .\remainder[2] (r_vec[2]),     .\remainder[3] (r_vec[3]),     .\remainder[4] (r_vec[4]),     .\remainder[5] (r_vec[5]),     .\remainder[6] (r_vec[6]),     .\remainder[7] (r_vec[7]), 
    .\remainder[8] (r_vec[8]),     .\remainder[9] (r_vec[9]),     .\remainder[10] (r_vec[10]),     .\remainder[11] (r_vec[11]),     .\remainder[12] (r_vec[12]),     .\remainder[13] (r_vec[13]),     .\remainder[14] (r_vec[14]),     .\remainder[15] (r_vec[15]), 
    .\remainder[16] (r_vec[16]),     .\remainder[17] (r_vec[17]),     .\remainder[18] (r_vec[18]),     .\remainder[19] (r_vec[19]),     .\remainder[20] (r_vec[20]),     .\remainder[21] (r_vec[21]),     .\remainder[22] (r_vec[22]),     .\remainder[23] (r_vec[23]), 
    .\remainder[24] (r_vec[24]),     .\remainder[25] (r_vec[25]),     .\remainder[26] (r_vec[26]),     .\remainder[27] (r_vec[27]),     .\remainder[28] (r_vec[28]),     .\remainder[29] (r_vec[29]),     .\remainder[30] (r_vec[30]),     .\remainder[31] (r_vec[31]), 
    .\remainder[32] (r_vec[32]),     .\remainder[33] (r_vec[33]),     .\remainder[34] (r_vec[34]),     .\remainder[35] (r_vec[35]),     .\remainder[36] (r_vec[36]),     .\remainder[37] (r_vec[37]),     .\remainder[38] (r_vec[38]),     .\remainder[39] (r_vec[39]), 
    .\remainder[40] (r_vec[40]),     .\remainder[41] (r_vec[41]),     .\remainder[42] (r_vec[42]),     .\remainder[43] (r_vec[43]),     .\remainder[44] (r_vec[44]),     .\remainder[45] (r_vec[45]),     .\remainder[46] (r_vec[46]),     .\remainder[47] (r_vec[47]), 
    .\remainder[48] (r_vec[48]),     .\remainder[49] (r_vec[49]),     .\remainder[50] (r_vec[50]),     .\remainder[51] (r_vec[51]),     .\remainder[52] (r_vec[52]),     .\remainder[53] (r_vec[53]),     .\remainder[54] (r_vec[54]),     .\remainder[55] (r_vec[55]), 
    .\remainder[56] (r_vec[56]),     .\remainder[57] (r_vec[57]),     .\remainder[58] (r_vec[58]),     .\remainder[59] (r_vec[59]),     .\remainder[60] (r_vec[60]),     .\remainder[61] (r_vec[61]),     .\remainder[62] (r_vec[62]),     .\remainder[63] (r_vec[63]) 
  );

  integer i;
  parameter STEPS = 512;

  initial begin
    a_vec = 64'b0;
    b_vec = 64'b0;

    #10;

    // Fixed divisor to create physical silent zone
    b_vec[48] = 1'b1;

    for (i = 0; i < STEPS; i = i + 1) begin
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[48] = 1'b0;
          else if (i < 320) a_vec[48] = 1'b1;
          else a_vec[48] = (i/8 + 0) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[49] = 1'b0;
          else if (i < 320) a_vec[49] = 1'b1;
          else a_vec[49] = (i/8 + 1) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[50] = 1'b0;
          else if (i < 320) a_vec[50] = 1'b1;
          else a_vec[50] = (i/8 + 2) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[51] = 1'b0;
          else if (i < 320) a_vec[51] = 1'b1;
          else a_vec[51] = (i/8 + 3) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[52] = 1'b0;
          else if (i < 320) a_vec[52] = 1'b1;
          else a_vec[52] = (i/8 + 4) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[53] = 1'b0;
          else if (i < 320) a_vec[53] = 1'b1;
          else a_vec[53] = (i/8 + 5) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[54] = 1'b0;
          else if (i < 320) a_vec[54] = 1'b1;
          else a_vec[54] = (i/8 + 6) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[55] = 1'b0;
          else if (i < 320) a_vec[55] = 1'b1;
          else a_vec[55] = (i/8 + 7) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[56] = 1'b0;
          else if (i < 320) a_vec[56] = 1'b1;
          else a_vec[56] = (i/8 + 8) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[57] = 1'b0;
          else if (i < 320) a_vec[57] = 1'b1;
          else a_vec[57] = (i/8 + 9) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[58] = 1'b0;
          else if (i < 320) a_vec[58] = 1'b1;
          else a_vec[58] = (i/8 + 10) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[59] = 1'b0;
          else if (i < 320) a_vec[59] = 1'b1;
          else a_vec[59] = (i/8 + 11) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[60] = 1'b0;
          else if (i < 320) a_vec[60] = 1'b1;
          else a_vec[60] = (i/8 + 12) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[61] = 1'b0;
          else if (i < 320) a_vec[61] = 1'b1;
          else a_vec[61] = (i/8 + 13) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[62] = 1'b0;
          else if (i < 320) a_vec[62] = 1'b1;
          else a_vec[62] = (i/8 + 14) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 160) a_vec[63] = 1'b0;
          else if (i < 320) a_vec[63] = 1'b1;
          else a_vec[63] = (i/8 + 15) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[0] = 1'b0;
          else if (i < 320) a_vec[0] = 1'b1;
          else a_vec[0] = (i/1 + 0) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[1] = 1'b0;
          else if (i < 320) a_vec[1] = 1'b1;
          else a_vec[1] = (i/1 + 1) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[2] = 1'b0;
          else if (i < 320) a_vec[2] = 1'b1;
          else a_vec[2] = (i/1 + 2) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[3] = 1'b0;
          else if (i < 320) a_vec[3] = 1'b1;
          else a_vec[3] = (i/1 + 3) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[4] = 1'b0;
          else if (i < 320) a_vec[4] = 1'b1;
          else a_vec[4] = (i/1 + 4) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[5] = 1'b0;
          else if (i < 320) a_vec[5] = 1'b1;
          else a_vec[5] = (i/1 + 5) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[6] = 1'b0;
          else if (i < 320) a_vec[6] = 1'b1;
          else a_vec[6] = (i/1 + 6) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[7] = 1'b0;
          else if (i < 320) a_vec[7] = 1'b1;
          else a_vec[7] = (i/1 + 7) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[8] = 1'b0;
          else if (i < 320) a_vec[8] = 1'b1;
          else a_vec[8] = (i/1 + 8) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[9] = 1'b0;
          else if (i < 320) a_vec[9] = 1'b1;
          else a_vec[9] = (i/1 + 9) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[10] = 1'b0;
          else if (i < 320) a_vec[10] = 1'b1;
          else a_vec[10] = (i/1 + 10) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[11] = 1'b0;
          else if (i < 320) a_vec[11] = 1'b1;
          else a_vec[11] = (i/1 + 11) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[12] = 1'b0;
          else if (i < 320) a_vec[12] = 1'b1;
          else a_vec[12] = (i/1 + 12) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[13] = 1'b0;
          else if (i < 320) a_vec[13] = 1'b1;
          else a_vec[13] = (i/1 + 13) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[14] = 1'b0;
          else if (i < 320) a_vec[14] = 1'b1;
          else a_vec[14] = (i/1 + 14) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[15] = 1'b0;
          else if (i < 320) a_vec[15] = 1'b1;
          else a_vec[15] = (i/1 + 15) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[16] = 1'b0;
          else if (i < 320) a_vec[16] = 1'b1;
          else a_vec[16] = (i/1 + 16) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[17] = 1'b0;
          else if (i < 320) a_vec[17] = 1'b1;
          else a_vec[17] = (i/1 + 17) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[18] = 1'b0;
          else if (i < 320) a_vec[18] = 1'b1;
          else a_vec[18] = (i/1 + 18) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[19] = 1'b0;
          else if (i < 320) a_vec[19] = 1'b1;
          else a_vec[19] = (i/1 + 19) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[20] = 1'b0;
          else if (i < 320) a_vec[20] = 1'b1;
          else a_vec[20] = (i/1 + 20) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[21] = 1'b0;
          else if (i < 320) a_vec[21] = 1'b1;
          else a_vec[21] = (i/1 + 21) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[22] = 1'b0;
          else if (i < 320) a_vec[22] = 1'b1;
          else a_vec[22] = (i/1 + 22) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[23] = 1'b0;
          else if (i < 320) a_vec[23] = 1'b1;
          else a_vec[23] = (i/1 + 23) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[24] = 1'b0;
          else if (i < 320) a_vec[24] = 1'b1;
          else a_vec[24] = (i/1 + 24) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[25] = 1'b0;
          else if (i < 320) a_vec[25] = 1'b1;
          else a_vec[25] = (i/1 + 25) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[26] = 1'b0;
          else if (i < 320) a_vec[26] = 1'b1;
          else a_vec[26] = (i/1 + 26) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[27] = 1'b0;
          else if (i < 320) a_vec[27] = 1'b1;
          else a_vec[27] = (i/1 + 27) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[28] = 1'b0;
          else if (i < 320) a_vec[28] = 1'b1;
          else a_vec[28] = (i/1 + 28) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[29] = 1'b0;
          else if (i < 320) a_vec[29] = 1'b1;
          else a_vec[29] = (i/1 + 29) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[30] = 1'b0;
          else if (i < 320) a_vec[30] = 1'b1;
          else a_vec[30] = (i/1 + 30) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 160) a_vec[31] = 1'b0;
          else if (i < 320) a_vec[31] = 1'b1;
          else a_vec[31] = (i/1 + 31) % 2;
        end

      #1;
      $display("o_sum=%016x", {q_vec[0] , q_vec[1] , q_vec[10] , q_vec[11] , q_vec[12] , q_vec[13] , q_vec[14] , q_vec[15] , q_vec[16] , q_vec[17] , q_vec[18] , q_vec[19] , q_vec[2] , q_vec[20] , q_vec[21] , q_vec[22] , q_vec[23] , q_vec[24] , q_vec[25] , q_vec[26] , q_vec[27] , q_vec[28] , q_vec[29] , q_vec[3] , q_vec[30] , q_vec[31] , q_vec[32] , q_vec[33] , q_vec[34] , q_vec[35] , q_vec[36] , q_vec[37] , q_vec[38] , q_vec[39] , q_vec[4] , q_vec[40] , q_vec[41] , q_vec[42] , q_vec[43] , q_vec[44] , q_vec[45] , q_vec[46] , q_vec[47] , q_vec[48] , q_vec[49] , q_vec[5] , q_vec[50] , q_vec[51] , q_vec[52] , q_vec[53] , q_vec[54] , q_vec[55] , q_vec[56] , q_vec[57] , q_vec[58] , q_vec[59] , q_vec[6] , q_vec[60] , q_vec[61] , q_vec[62] , q_vec[63] , q_vec[7] , q_vec[8] , q_vec[9] , r_vec[0] , r_vec[1] , r_vec[10] , r_vec[11] , r_vec[12] , r_vec[13] , r_vec[14] , r_vec[15] , r_vec[16] , r_vec[17] , r_vec[18] , r_vec[19] , r_vec[2] , r_vec[20] , r_vec[21] , r_vec[22] , r_vec[23] , r_vec[24] , r_vec[25] , r_vec[26] , r_vec[27] , r_vec[28] , r_vec[29] , r_vec[3] , r_vec[30] , r_vec[31] , r_vec[32] , r_vec[33] , r_vec[34] , r_vec[35] , r_vec[36] , r_vec[37] , r_vec[38] , r_vec[39] , r_vec[4] , r_vec[40] , r_vec[41] , r_vec[42] , r_vec[43] , r_vec[44] , r_vec[45] , r_vec[46] , r_vec[47] , r_vec[48] , r_vec[49] , r_vec[5] , r_vec[50] , r_vec[51] , r_vec[52] , r_vec[53] , r_vec[54] , r_vec[55] , r_vec[56] , r_vec[57] , r_vec[58] , r_vec[59] , r_vec[6] , r_vec[60] , r_vec[61] , r_vec[62] , r_vec[63] , r_vec[7] , r_vec[8] , r_vec[9]});
    end
    $finish;
  end

endmodule
