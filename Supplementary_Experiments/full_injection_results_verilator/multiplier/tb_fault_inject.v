`timescale 1ns / 1ps

module tb;

  reg [63:0] a_vec;
  reg [63:0] b_vec;
  wire [127:0] f_vec;

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
    .\f[0] (f_vec[0]),     .\f[1] (f_vec[1]),     .\f[2] (f_vec[2]),     .\f[3] (f_vec[3]),     .\f[4] (f_vec[4]),     .\f[5] (f_vec[5]),     .\f[6] (f_vec[6]),     .\f[7] (f_vec[7]), 
    .\f[8] (f_vec[8]),     .\f[9] (f_vec[9]),     .\f[10] (f_vec[10]),     .\f[11] (f_vec[11]),     .\f[12] (f_vec[12]),     .\f[13] (f_vec[13]),     .\f[14] (f_vec[14]),     .\f[15] (f_vec[15]), 
    .\f[16] (f_vec[16]),     .\f[17] (f_vec[17]),     .\f[18] (f_vec[18]),     .\f[19] (f_vec[19]),     .\f[20] (f_vec[20]),     .\f[21] (f_vec[21]),     .\f[22] (f_vec[22]),     .\f[23] (f_vec[23]), 
    .\f[24] (f_vec[24]),     .\f[25] (f_vec[25]),     .\f[26] (f_vec[26]),     .\f[27] (f_vec[27]),     .\f[28] (f_vec[28]),     .\f[29] (f_vec[29]),     .\f[30] (f_vec[30]),     .\f[31] (f_vec[31]), 
    .\f[32] (f_vec[32]),     .\f[33] (f_vec[33]),     .\f[34] (f_vec[34]),     .\f[35] (f_vec[35]),     .\f[36] (f_vec[36]),     .\f[37] (f_vec[37]),     .\f[38] (f_vec[38]),     .\f[39] (f_vec[39]), 
    .\f[40] (f_vec[40]),     .\f[41] (f_vec[41]),     .\f[42] (f_vec[42]),     .\f[43] (f_vec[43]),     .\f[44] (f_vec[44]),     .\f[45] (f_vec[45]),     .\f[46] (f_vec[46]),     .\f[47] (f_vec[47]), 
    .\f[48] (f_vec[48]),     .\f[49] (f_vec[49]),     .\f[50] (f_vec[50]),     .\f[51] (f_vec[51]),     .\f[52] (f_vec[52]),     .\f[53] (f_vec[53]),     .\f[54] (f_vec[54]),     .\f[55] (f_vec[55]), 
    .\f[56] (f_vec[56]),     .\f[57] (f_vec[57]),     .\f[58] (f_vec[58]),     .\f[59] (f_vec[59]),     .\f[60] (f_vec[60]),     .\f[61] (f_vec[61]),     .\f[62] (f_vec[62]),     .\f[63] (f_vec[63]), 
    .\f[64] (f_vec[64]),     .\f[65] (f_vec[65]),     .\f[66] (f_vec[66]),     .\f[67] (f_vec[67]),     .\f[68] (f_vec[68]),     .\f[69] (f_vec[69]),     .\f[70] (f_vec[70]),     .\f[71] (f_vec[71]), 
    .\f[72] (f_vec[72]),     .\f[73] (f_vec[73]),     .\f[74] (f_vec[74]),     .\f[75] (f_vec[75]),     .\f[76] (f_vec[76]),     .\f[77] (f_vec[77]),     .\f[78] (f_vec[78]),     .\f[79] (f_vec[79]), 
    .\f[80] (f_vec[80]),     .\f[81] (f_vec[81]),     .\f[82] (f_vec[82]),     .\f[83] (f_vec[83]),     .\f[84] (f_vec[84]),     .\f[85] (f_vec[85]),     .\f[86] (f_vec[86]),     .\f[87] (f_vec[87]), 
    .\f[88] (f_vec[88]),     .\f[89] (f_vec[89]),     .\f[90] (f_vec[90]),     .\f[91] (f_vec[91]),     .\f[92] (f_vec[92]),     .\f[93] (f_vec[93]),     .\f[94] (f_vec[94]),     .\f[95] (f_vec[95]), 
    .\f[96] (f_vec[96]),     .\f[97] (f_vec[97]),     .\f[98] (f_vec[98]),     .\f[99] (f_vec[99]),     .\f[100] (f_vec[100]),     .\f[101] (f_vec[101]),     .\f[102] (f_vec[102]),     .\f[103] (f_vec[103]), 
    .\f[104] (f_vec[104]),     .\f[105] (f_vec[105]),     .\f[106] (f_vec[106]),     .\f[107] (f_vec[107]),     .\f[108] (f_vec[108]),     .\f[109] (f_vec[109]),     .\f[110] (f_vec[110]),     .\f[111] (f_vec[111]), 
    .\f[112] (f_vec[112]),     .\f[113] (f_vec[113]),     .\f[114] (f_vec[114]),     .\f[115] (f_vec[115]),     .\f[116] (f_vec[116]),     .\f[117] (f_vec[117]),     .\f[118] (f_vec[118]),     .\f[119] (f_vec[119]), 
    .\f[120] (f_vec[120]),     .\f[121] (f_vec[121]),     .\f[122] (f_vec[122]),     .\f[123] (f_vec[123]),     .\f[124] (f_vec[124]),     .\f[125] (f_vec[125]),     .\f[126] (f_vec[126]),     .\f[127] (f_vec[127]) 
  );

  integer i;
  parameter STEPS = 256;  // Increased for richer coverage

  task run_stimulus_pass;
  begin
    a_vec = 64'b0;
    b_vec = 64'b0;

    #10;

    // Fixed multiplier pattern at low bits (more complex than single bit)
    b_vec[7:0] = 8'hAA;  // 10101010 pattern

    for (i = 0; i < STEPS; i = i + 1) begin
        // === DYNAMIC b_vec variation ===
        if ((i % 64) == 0) begin
          if (i < 64) b_vec[7:0] = 8'hAA;
          else if (i < 128) b_vec[7:0] = 8'h55;
          else if (i < 192) b_vec[7:0] = 8'hFF;
          else b_vec[7:0] = 8'h0F;
        end

        // === HIGH WINDOW: a_vec[48:63] (16 bits, multi-freq) ===
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[48] = 1'b0;
          else if (i < 96) a_vec[48] = 1'b1;
          else a_vec[48] = ((i/4) + 0) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[49] = 1'b0;
          else if (i < 96) a_vec[49] = 1'b1;
          else a_vec[49] = ((i/4) + 1) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[50] = 1'b0;
          else if (i < 96) a_vec[50] = 1'b1;
          else a_vec[50] = ((i/4) + 2) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[51] = 1'b0;
          else if (i < 96) a_vec[51] = 1'b1;
          else a_vec[51] = ((i/4) + 3) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 48) a_vec[52] = 1'b0;
          else if (i < 96) a_vec[52] = 1'b1;
          else a_vec[52] = ((i/8) + 4) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 48) a_vec[53] = 1'b0;
          else if (i < 96) a_vec[53] = 1'b1;
          else a_vec[53] = ((i/8) + 5) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 48) a_vec[54] = 1'b0;
          else if (i < 96) a_vec[54] = 1'b1;
          else a_vec[54] = ((i/8) + 6) % 2;
        end
        if ((i % 8) == 0) begin
          if (i < 48) a_vec[55] = 1'b0;
          else if (i < 96) a_vec[55] = 1'b1;
          else a_vec[55] = ((i/8) + 7) % 2;
        end
        if ((i % 12) == 0) begin
          if (i < 48) a_vec[56] = 1'b0;
          else if (i < 96) a_vec[56] = 1'b1;
          else a_vec[56] = ((i/12) + 8) % 2;
        end
        if ((i % 12) == 0) begin
          if (i < 48) a_vec[57] = 1'b0;
          else if (i < 96) a_vec[57] = 1'b1;
          else a_vec[57] = ((i/12) + 9) % 2;
        end
        if ((i % 12) == 0) begin
          if (i < 48) a_vec[58] = 1'b0;
          else if (i < 96) a_vec[58] = 1'b1;
          else a_vec[58] = ((i/12) + 10) % 2;
        end
        if ((i % 12) == 0) begin
          if (i < 48) a_vec[59] = 1'b0;
          else if (i < 96) a_vec[59] = 1'b1;
          else a_vec[59] = ((i/12) + 11) % 2;
        end
        if ((i % 16) == 0) begin
          if (i < 48) a_vec[60] = 1'b0;
          else if (i < 96) a_vec[60] = 1'b1;
          else a_vec[60] = ((i/16) + 12) % 2;
        end
        if ((i % 16) == 0) begin
          if (i < 48) a_vec[61] = 1'b0;
          else if (i < 96) a_vec[61] = 1'b1;
          else a_vec[61] = ((i/16) + 13) % 2;
        end
        if ((i % 16) == 0) begin
          if (i < 48) a_vec[62] = 1'b0;
          else if (i < 96) a_vec[62] = 1'b1;
          else a_vec[62] = ((i/16) + 14) % 2;
        end
        if ((i % 16) == 0) begin
          if (i < 48) a_vec[63] = 1'b0;
          else if (i < 96) a_vec[63] = 1'b1;
          else a_vec[63] = ((i/16) + 15) % 2;
        end

        // === LOW WINDOW: a_vec[0:15] (16 bits, multi-freq) ===
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[0] = 1'b0;
          else if (i < 96) a_vec[0] = 1'b1;
          else a_vec[0] = ((i/1) + 0) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[1] = 1'b0;
          else if (i < 96) a_vec[1] = 1'b1;
          else a_vec[1] = ((i/1) + 1) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[2] = 1'b0;
          else if (i < 96) a_vec[2] = 1'b1;
          else a_vec[2] = ((i/1) + 2) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[3] = 1'b0;
          else if (i < 96) a_vec[3] = 1'b1;
          else a_vec[3] = ((i/1) + 3) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[4] = 1'b0;
          else if (i < 96) a_vec[4] = 1'b1;
          else a_vec[4] = ((i/1) + 4) % 2;
        end
        if ((i % 1) == 0) begin
          if (i < 48) a_vec[5] = 1'b0;
          else if (i < 96) a_vec[5] = 1'b1;
          else a_vec[5] = ((i/1) + 5) % 2;
        end
        if ((i % 2) == 0) begin
          if (i < 48) a_vec[6] = 1'b0;
          else if (i < 96) a_vec[6] = 1'b1;
          else a_vec[6] = ((i/2) + 6) % 2;
        end
        if ((i % 2) == 0) begin
          if (i < 48) a_vec[7] = 1'b0;
          else if (i < 96) a_vec[7] = 1'b1;
          else a_vec[7] = ((i/2) + 7) % 2;
        end
        if ((i % 2) == 0) begin
          if (i < 48) a_vec[8] = 1'b0;
          else if (i < 96) a_vec[8] = 1'b1;
          else a_vec[8] = ((i/2) + 8) % 2;
        end
        if ((i % 2) == 0) begin
          if (i < 48) a_vec[9] = 1'b0;
          else if (i < 96) a_vec[9] = 1'b1;
          else a_vec[9] = ((i/2) + 9) % 2;
        end
        if ((i % 2) == 0) begin
          if (i < 48) a_vec[10] = 1'b0;
          else if (i < 96) a_vec[10] = 1'b1;
          else a_vec[10] = ((i/2) + 10) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[11] = 1'b0;
          else if (i < 96) a_vec[11] = 1'b1;
          else a_vec[11] = ((i/4) + 11) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[12] = 1'b0;
          else if (i < 96) a_vec[12] = 1'b1;
          else a_vec[12] = ((i/4) + 12) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[13] = 1'b0;
          else if (i < 96) a_vec[13] = 1'b1;
          else a_vec[13] = ((i/4) + 13) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[14] = 1'b0;
          else if (i < 96) a_vec[14] = 1'b1;
          else a_vec[14] = ((i/4) + 14) % 2;
        end
        if ((i % 4) == 0) begin
          if (i < 48) a_vec[15] = 1'b0;
          else if (i < 96) a_vec[15] = 1'b1;
          else a_vec[15] = ((i/4) + 15) % 2;
        end

      #1;
      $display("o_sum=%07x", {f_vec[127], f_vec[126], f_vec[125], f_vec[124], f_vec[123], f_vec[122], f_vec[121], f_vec[120], f_vec[119], f_vec[118], f_vec[117], f_vec[116], f_vec[115], f_vec[114], f_vec[113], f_vec[112], f_vec[67], f_vec[66], f_vec[65], f_vec[64], f_vec[35], f_vec[34], f_vec[33], f_vec[32], f_vec[3], f_vec[2], f_vec[1], f_vec[0]});
    end
    // $finish; // disabled
  end
  endtask



  // ===== Verilator 故障注入控制 (简化版) =====
  // 故障注入 MUX 已在网表中插入，TB 只需设置 uut.__FAULT_ID

  // 故障注入控制器
  integer __batch_fid;
  integer __BATCH_START, __BATCH_END;

  initial begin
    if (!$value$plusargs("BATCH_START=%d", __BATCH_START)) __BATCH_START = 0;
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 53868;

    $display("[BATCH] Start=%0d End=%0d", __BATCH_START, __BATCH_END);

    // 批量故障注入循环
    for (__batch_fid = __BATCH_START; __batch_fid < __BATCH_END; __batch_fid = __batch_fid + 1) begin
      // 通过 hierarchical reference 设置 DUT 内部的 __FAULT_ID
      uut.__FAULT_ID = __batch_fid;
      $display("[FID:%0d]", __batch_fid);
      run_stimulus_pass();
    end

    $finish;
  end

endmodule
