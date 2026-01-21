`timescale 1ns / 1ps

module tb;

  // Vector signals for logic and display
  reg [63:0] a_vec;
  wire [127:0] asquared_vec;

  // DUT Instance - Connecting vectors to escaped identifiers
  top uut (
    .\a[0] (a_vec[0]),
    .\a[1] (a_vec[1]),
    .\a[2] (a_vec[2]),
    .\a[3] (a_vec[3]),
    .\a[4] (a_vec[4]),
    .\a[5] (a_vec[5]),
    .\a[6] (a_vec[6]),
    .\a[7] (a_vec[7]),
    .\a[8] (a_vec[8]),
    .\a[9] (a_vec[9]),
    .\a[10] (a_vec[10]),
    .\a[11] (a_vec[11]),
    .\a[12] (a_vec[12]),
    .\a[13] (a_vec[13]),
    .\a[14] (a_vec[14]),
    .\a[15] (a_vec[15]),
    .\a[16] (a_vec[16]),
    .\a[17] (a_vec[17]),
    .\a[18] (a_vec[18]),
    .\a[19] (a_vec[19]),
    .\a[20] (a_vec[20]),
    .\a[21] (a_vec[21]),
    .\a[22] (a_vec[22]),
    .\a[23] (a_vec[23]),
    .\a[24] (a_vec[24]),
    .\a[25] (a_vec[25]),
    .\a[26] (a_vec[26]),
    .\a[27] (a_vec[27]),
    .\a[28] (a_vec[28]),
    .\a[29] (a_vec[29]),
    .\a[30] (a_vec[30]),
    .\a[31] (a_vec[31]),
    .\a[32] (a_vec[32]),
    .\a[33] (a_vec[33]),
    .\a[34] (a_vec[34]),
    .\a[35] (a_vec[35]),
    .\a[36] (a_vec[36]),
    .\a[37] (a_vec[37]),
    .\a[38] (a_vec[38]),
    .\a[39] (a_vec[39]),
    .\a[40] (a_vec[40]),
    .\a[41] (a_vec[41]),
    .\a[42] (a_vec[42]),
    .\a[43] (a_vec[43]),
    .\a[44] (a_vec[44]),
    .\a[45] (a_vec[45]),
    .\a[46] (a_vec[46]),
    .\a[47] (a_vec[47]),
    .\a[48] (a_vec[48]),
    .\a[49] (a_vec[49]),
    .\a[50] (a_vec[50]),
    .\a[51] (a_vec[51]),
    .\a[52] (a_vec[52]),
    .\a[53] (a_vec[53]),
    .\a[54] (a_vec[54]),
    .\a[55] (a_vec[55]),
    .\a[56] (a_vec[56]),
    .\a[57] (a_vec[57]),
    .\a[58] (a_vec[58]),
    .\a[59] (a_vec[59]),
    .\a[60] (a_vec[60]),
    .\a[61] (a_vec[61]),
    .\a[62] (a_vec[62]),
    .\a[63] (a_vec[63]),
    .\asquared[0] (asquared_vec[0]),
    .\asquared[1] (asquared_vec[1]),
    .\asquared[2] (asquared_vec[2]),
    .\asquared[3] (asquared_vec[3]),
    .\asquared[4] (asquared_vec[4]),
    .\asquared[5] (asquared_vec[5]),
    .\asquared[6] (asquared_vec[6]),
    .\asquared[7] (asquared_vec[7]),
    .\asquared[8] (asquared_vec[8]),
    .\asquared[9] (asquared_vec[9]),
    .\asquared[10] (asquared_vec[10]),
    .\asquared[11] (asquared_vec[11]),
    .\asquared[12] (asquared_vec[12]),
    .\asquared[13] (asquared_vec[13]),
    .\asquared[14] (asquared_vec[14]),
    .\asquared[15] (asquared_vec[15]),
    .\asquared[16] (asquared_vec[16]),
    .\asquared[17] (asquared_vec[17]),
    .\asquared[18] (asquared_vec[18]),
    .\asquared[19] (asquared_vec[19]),
    .\asquared[20] (asquared_vec[20]),
    .\asquared[21] (asquared_vec[21]),
    .\asquared[22] (asquared_vec[22]),
    .\asquared[23] (asquared_vec[23]),
    .\asquared[24] (asquared_vec[24]),
    .\asquared[25] (asquared_vec[25]),
    .\asquared[26] (asquared_vec[26]),
    .\asquared[27] (asquared_vec[27]),
    .\asquared[28] (asquared_vec[28]),
    .\asquared[29] (asquared_vec[29]),
    .\asquared[30] (asquared_vec[30]),
    .\asquared[31] (asquared_vec[31]),
    .\asquared[32] (asquared_vec[32]),
    .\asquared[33] (asquared_vec[33]),
    .\asquared[34] (asquared_vec[34]),
    .\asquared[35] (asquared_vec[35]),
    .\asquared[36] (asquared_vec[36]),
    .\asquared[37] (asquared_vec[37]),
    .\asquared[38] (asquared_vec[38]),
    .\asquared[39] (asquared_vec[39]),
    .\asquared[40] (asquared_vec[40]),
    .\asquared[41] (asquared_vec[41]),
    .\asquared[42] (asquared_vec[42]),
    .\asquared[43] (asquared_vec[43]),
    .\asquared[44] (asquared_vec[44]),
    .\asquared[45] (asquared_vec[45]),
    .\asquared[46] (asquared_vec[46]),
    .\asquared[47] (asquared_vec[47]),
    .\asquared[48] (asquared_vec[48]),
    .\asquared[49] (asquared_vec[49]),
    .\asquared[50] (asquared_vec[50]),
    .\asquared[51] (asquared_vec[51]),
    .\asquared[52] (asquared_vec[52]),
    .\asquared[53] (asquared_vec[53]),
    .\asquared[54] (asquared_vec[54]),
    .\asquared[55] (asquared_vec[55]),
    .\asquared[56] (asquared_vec[56]),
    .\asquared[57] (asquared_vec[57]),
    .\asquared[58] (asquared_vec[58]),
    .\asquared[59] (asquared_vec[59]),
    .\asquared[60] (asquared_vec[60]),
    .\asquared[61] (asquared_vec[61]),
    .\asquared[62] (asquared_vec[62]),
    .\asquared[63] (asquared_vec[63]),
    .\asquared[64] (asquared_vec[64]),
    .\asquared[65] (asquared_vec[65]),
    .\asquared[66] (asquared_vec[66]),
    .\asquared[67] (asquared_vec[67]),
    .\asquared[68] (asquared_vec[68]),
    .\asquared[69] (asquared_vec[69]),
    .\asquared[70] (asquared_vec[70]),
    .\asquared[71] (asquared_vec[71]),
    .\asquared[72] (asquared_vec[72]),
    .\asquared[73] (asquared_vec[73]),
    .\asquared[74] (asquared_vec[74]),
    .\asquared[75] (asquared_vec[75]),
    .\asquared[76] (asquared_vec[76]),
    .\asquared[77] (asquared_vec[77]),
    .\asquared[78] (asquared_vec[78]),
    .\asquared[79] (asquared_vec[79]),
    .\asquared[80] (asquared_vec[80]),
    .\asquared[81] (asquared_vec[81]),
    .\asquared[82] (asquared_vec[82]),
    .\asquared[83] (asquared_vec[83]),
    .\asquared[84] (asquared_vec[84]),
    .\asquared[85] (asquared_vec[85]),
    .\asquared[86] (asquared_vec[86]),
    .\asquared[87] (asquared_vec[87]),
    .\asquared[88] (asquared_vec[88]),
    .\asquared[89] (asquared_vec[89]),
    .\asquared[90] (asquared_vec[90]),
    .\asquared[91] (asquared_vec[91]),
    .\asquared[92] (asquared_vec[92]),
    .\asquared[93] (asquared_vec[93]),
    .\asquared[94] (asquared_vec[94]),
    .\asquared[95] (asquared_vec[95]),
    .\asquared[96] (asquared_vec[96]),
    .\asquared[97] (asquared_vec[97]),
    .\asquared[98] (asquared_vec[98]),
    .\asquared[99] (asquared_vec[99]),
    .\asquared[100] (asquared_vec[100]),
    .\asquared[101] (asquared_vec[101]),
    .\asquared[102] (asquared_vec[102]),
    .\asquared[103] (asquared_vec[103]),
    .\asquared[104] (asquared_vec[104]),
    .\asquared[105] (asquared_vec[105]),
    .\asquared[106] (asquared_vec[106]),
    .\asquared[107] (asquared_vec[107]),
    .\asquared[108] (asquared_vec[108]),
    .\asquared[109] (asquared_vec[109]),
    .\asquared[110] (asquared_vec[110]),
    .\asquared[111] (asquared_vec[111]),
    .\asquared[112] (asquared_vec[112]),
    .\asquared[113] (asquared_vec[113]),
    .\asquared[114] (asquared_vec[114]),
    .\asquared[115] (asquared_vec[115]),
    .\asquared[116] (asquared_vec[116]),
    .\asquared[117] (asquared_vec[117]),
    .\asquared[118] (asquared_vec[118]),
    .\asquared[119] (asquared_vec[119]),
    .\asquared[120] (asquared_vec[120]),
    .\asquared[121] (asquared_vec[121]),
    .\asquared[122] (asquared_vec[122]),
    .\asquared[123] (asquared_vec[123]),
    .\asquared[124] (asquared_vec[124]),
    .\asquared[125] (asquared_vec[125]),
    .\asquared[126] (asquared_vec[126]),
    .\asquared[127] (asquared_vec[127])
  );

  integer i;
  localparam STEPS = 512;

  task run_stimulus_pass;
  begin
    // 所有输入初始化为0
    a_vec = 64'b0;
    #10;

    $display("=== Square Circuit Priority Stimulus V6 ===");
    $display("Strategy: a[20-43] LFSR every 2 (24 bits), a[12-19,44-51] every 8 (16 bits)");

    for (i = 0; i < STEPS; i = i + 1) begin

        // === CORE HIGH PRIORITY: a[20-43] (24 bits) - LFSR every 2 steps ===
        if ((i % 2) == 0) begin
            a_vec[20] = i[1] ^ i[3];
            a_vec[21] = i[2] ^ i[4];
            a_vec[22] = i[3] ^ i[5];
            a_vec[23] = i[4] ^ i[6];
            a_vec[24] = i[5] ^ i[7];
            a_vec[25] = i[1] ^ i[2] ^ i[6];
            a_vec[26] = i[2] ^ i[3] ^ i[7];
            a_vec[27] = i[3] ^ i[4] ^ i[1];
            a_vec[28] = i[4] ^ i[5] ^ i[2];
            a_vec[29] = i[5] ^ i[6] ^ i[3];
            a_vec[30] = i[6] ^ i[7] ^ i[4];
            a_vec[31] = i[7] ^ i[1] ^ i[5];
            a_vec[32] = i[1] ^ i[2];
            a_vec[33] = i[2] ^ i[3];
            a_vec[34] = i[3] ^ i[4];
            a_vec[35] = i[4] ^ i[5];
            a_vec[36] = i[5] ^ i[6];
            a_vec[37] = i[6] ^ i[7];
            a_vec[38] = i[7] ^ i[1];
            a_vec[39] = i[1] ^ i[3] ^ i[5];
            a_vec[40] = i[2] ^ i[4] ^ i[6];
            a_vec[41] = i[3] ^ i[5] ^ i[7];
            a_vec[42] = i[4] ^ i[6] ^ i[1];
            a_vec[43] = i[5] ^ i[7] ^ i[2];
        end

        // === AUXILIARY: a[12-19,44-51] (16 bits) - every 8 steps ===
        if ((i % 8) == 0) begin
            a_vec[19:12] = i[7:0];
            a_vec[51:44] = i[7:0];
        end

        // === LOW PRIORITY: a[0-11] and a[52-63] - STATIC 0 ===

        #1;
        $display("o_sum=%08x", asquared_vec[95:64]);
    end

    $display("o_sum=%08x [final]", asquared_vec[95:64]);
    $display("=== Test Complete ===");
    // $finish; // disabled
  end
  endtask


  reg [510:0] dumpfile_name;
  initial begin
    if ($value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
      $display("Dumping VCD to: %s", dumpfile_name);
      $dumpfile(dumpfile_name);
      $dumpvars(0, tb);
    end
  end

  initial begin
    #1;
    $display("FAULT_INJECTED: check_if_force_took_effect");
  end


  // ===== Verilator 故障注入控制 (简化版) =====
  // 故障注入 MUX 已在网表中插入，TB 只需设置 uut.__FAULT_ID

  // 故障注入控制器
  integer __batch_fid;
  integer __BATCH_START, __BATCH_END;

  initial begin
    if (!$value$plusargs("BATCH_START=%d", __BATCH_START)) __BATCH_START = 0;
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 36716;

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
