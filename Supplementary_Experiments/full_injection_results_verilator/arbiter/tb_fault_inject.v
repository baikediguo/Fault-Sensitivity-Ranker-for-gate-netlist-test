`timescale 1ns/1ps

module tb();

  reg [127:0] priority_in;
  reg [127:0] req;
  wire [127:0] grant;
  wire anyGrant;

  integer i, j;

  top uut (
    .\priority[0] (priority_in[0]), .\priority[1] (priority_in[1]), .\priority[2] (priority_in[2]), .\priority[3] (priority_in[3]),
    .\priority[4] (priority_in[4]), .\priority[5] (priority_in[5]), .\priority[6] (priority_in[6]), .\priority[7] (priority_in[7]),
    .\priority[8] (priority_in[8]), .\priority[9] (priority_in[9]), .\priority[10] (priority_in[10]), .\priority[11] (priority_in[11]),
    .\priority[12] (priority_in[12]), .\priority[13] (priority_in[13]), .\priority[14] (priority_in[14]), .\priority[15] (priority_in[15]),
    .\priority[16] (priority_in[16]), .\priority[17] (priority_in[17]), .\priority[18] (priority_in[18]), .\priority[19] (priority_in[19]),
    .\priority[20] (priority_in[20]), .\priority[21] (priority_in[21]), .\priority[22] (priority_in[22]), .\priority[23] (priority_in[23]),
    .\priority[24] (priority_in[24]), .\priority[25] (priority_in[25]), .\priority[26] (priority_in[26]), .\priority[27] (priority_in[27]),
    .\priority[28] (priority_in[28]), .\priority[29] (priority_in[29]), .\priority[30] (priority_in[30]), .\priority[31] (priority_in[31]),
    .\priority[32] (priority_in[32]), .\priority[33] (priority_in[33]), .\priority[34] (priority_in[34]), .\priority[35] (priority_in[35]),
    .\priority[36] (priority_in[36]), .\priority[37] (priority_in[37]), .\priority[38] (priority_in[38]), .\priority[39] (priority_in[39]),
    .\priority[40] (priority_in[40]), .\priority[41] (priority_in[41]), .\priority[42] (priority_in[42]), .\priority[43] (priority_in[43]),
    .\priority[44] (priority_in[44]), .\priority[45] (priority_in[45]), .\priority[46] (priority_in[46]), .\priority[47] (priority_in[47]),
    .\priority[48] (priority_in[48]), .\priority[49] (priority_in[49]), .\priority[50] (priority_in[50]), .\priority[51] (priority_in[51]),
    .\priority[52] (priority_in[52]), .\priority[53] (priority_in[53]), .\priority[54] (priority_in[54]), .\priority[55] (priority_in[55]),
    .\priority[56] (priority_in[56]), .\priority[57] (priority_in[57]), .\priority[58] (priority_in[58]), .\priority[59] (priority_in[59]),
    .\priority[60] (priority_in[60]), .\priority[61] (priority_in[61]), .\priority[62] (priority_in[62]), .\priority[63] (priority_in[63]),
    .\priority[64] (priority_in[64]), .\priority[65] (priority_in[65]), .\priority[66] (priority_in[66]), .\priority[67] (priority_in[67]),
    .\priority[68] (priority_in[68]), .\priority[69] (priority_in[69]), .\priority[70] (priority_in[70]), .\priority[71] (priority_in[71]),
    .\priority[72] (priority_in[72]), .\priority[73] (priority_in[73]), .\priority[74] (priority_in[74]), .\priority[75] (priority_in[75]),
    .\priority[76] (priority_in[76]), .\priority[77] (priority_in[77]), .\priority[78] (priority_in[78]), .\priority[79] (priority_in[79]),
    .\priority[80] (priority_in[80]), .\priority[81] (priority_in[81]), .\priority[82] (priority_in[82]), .\priority[83] (priority_in[83]),
    .\priority[84] (priority_in[84]), .\priority[85] (priority_in[85]), .\priority[86] (priority_in[86]), .\priority[87] (priority_in[87]),
    .\priority[88] (priority_in[88]), .\priority[89] (priority_in[89]), .\priority[90] (priority_in[90]), .\priority[91] (priority_in[91]),
    .\priority[92] (priority_in[92]), .\priority[93] (priority_in[93]), .\priority[94] (priority_in[94]), .\priority[95] (priority_in[95]),
    .\priority[96] (priority_in[96]), .\priority[97] (priority_in[97]), .\priority[98] (priority_in[98]), .\priority[99] (priority_in[99]),
    .\priority[100] (priority_in[100]), .\priority[101] (priority_in[101]), .\priority[102] (priority_in[102]), .\priority[103] (priority_in[103]),
    .\priority[104] (priority_in[104]), .\priority[105] (priority_in[105]), .\priority[106] (priority_in[106]), .\priority[107] (priority_in[107]),
    .\priority[108] (priority_in[108]), .\priority[109] (priority_in[109]), .\priority[110] (priority_in[110]), .\priority[111] (priority_in[111]),
    .\priority[112] (priority_in[112]), .\priority[113] (priority_in[113]), .\priority[114] (priority_in[114]), .\priority[115] (priority_in[115]),
    .\priority[116] (priority_in[116]), .\priority[117] (priority_in[117]), .\priority[118] (priority_in[118]), .\priority[119] (priority_in[119]),
    .\priority[120] (priority_in[120]), .\priority[121] (priority_in[121]), .\priority[122] (priority_in[122]), .\priority[123] (priority_in[123]),
    .\priority[124] (priority_in[124]), .\priority[125] (priority_in[125]), .\priority[126] (priority_in[126]), .\priority[127] (priority_in[127]),
    .\req[0] (req[0]), .\req[1] (req[1]), .\req[2] (req[2]), .\req[3] (req[3]),
    .\req[4] (req[4]), .\req[5] (req[5]), .\req[6] (req[6]), .\req[7] (req[7]),
    .\req[8] (req[8]), .\req[9] (req[9]), .\req[10] (req[10]), .\req[11] (req[11]),
    .\req[12] (req[12]), .\req[13] (req[13]), .\req[14] (req[14]), .\req[15] (req[15]),
    .\req[16] (req[16]), .\req[17] (req[17]), .\req[18] (req[18]), .\req[19] (req[19]),
    .\req[20] (req[20]), .\req[21] (req[21]), .\req[22] (req[22]), .\req[23] (req[23]),
    .\req[24] (req[24]), .\req[25] (req[25]), .\req[26] (req[26]), .\req[27] (req[27]),
    .\req[28] (req[28]), .\req[29] (req[29]), .\req[30] (req[30]), .\req[31] (req[31]),
    .\req[32] (req[32]), .\req[33] (req[33]), .\req[34] (req[34]), .\req[35] (req[35]),
    .\req[36] (req[36]), .\req[37] (req[37]), .\req[38] (req[38]), .\req[39] (req[39]),
    .\req[40] (req[40]), .\req[41] (req[41]), .\req[42] (req[42]), .\req[43] (req[43]),
    .\req[44] (req[44]), .\req[45] (req[45]), .\req[46] (req[46]), .\req[47] (req[47]),
    .\req[48] (req[48]), .\req[49] (req[49]), .\req[50] (req[50]), .\req[51] (req[51]),
    .\req[52] (req[52]), .\req[53] (req[53]), .\req[54] (req[54]), .\req[55] (req[55]),
    .\req[56] (req[56]), .\req[57] (req[57]), .\req[58] (req[58]), .\req[59] (req[59]),
    .\req[60] (req[60]), .\req[61] (req[61]), .\req[62] (req[62]), .\req[63] (req[63]),
    .\req[64] (req[64]), .\req[65] (req[65]), .\req[66] (req[66]), .\req[67] (req[67]),
    .\req[68] (req[68]), .\req[69] (req[69]), .\req[70] (req[70]), .\req[71] (req[71]),
    .\req[72] (req[72]), .\req[73] (req[73]), .\req[74] (req[74]), .\req[75] (req[75]),
    .\req[76] (req[76]), .\req[77] (req[77]), .\req[78] (req[78]), .\req[79] (req[79]),
    .\req[80] (req[80]), .\req[81] (req[81]), .\req[82] (req[82]), .\req[83] (req[83]),
    .\req[84] (req[84]), .\req[85] (req[85]), .\req[86] (req[86]), .\req[87] (req[87]),
    .\req[88] (req[88]), .\req[89] (req[89]), .\req[90] (req[90]), .\req[91] (req[91]),
    .\req[92] (req[92]), .\req[93] (req[93]), .\req[94] (req[94]), .\req[95] (req[95]),
    .\req[96] (req[96]), .\req[97] (req[97]), .\req[98] (req[98]), .\req[99] (req[99]),
    .\req[100] (req[100]), .\req[101] (req[101]), .\req[102] (req[102]), .\req[103] (req[103]),
    .\req[104] (req[104]), .\req[105] (req[105]), .\req[106] (req[106]), .\req[107] (req[107]),
    .\req[108] (req[108]), .\req[109] (req[109]), .\req[110] (req[110]), .\req[111] (req[111]),
    .\req[112] (req[112]), .\req[113] (req[113]), .\req[114] (req[114]), .\req[115] (req[115]),
    .\req[116] (req[116]), .\req[117] (req[117]), .\req[118] (req[118]), .\req[119] (req[119]),
    .\req[120] (req[120]), .\req[121] (req[121]), .\req[122] (req[122]), .\req[123] (req[123]),
    .\req[124] (req[124]), .\req[125] (req[125]), .\req[126] (req[126]), .\req[127] (req[127]),
    .\grant[0] (grant[0]), .\grant[1] (grant[1]), .\grant[2] (grant[2]), .\grant[3] (grant[3]),
    .\grant[4] (grant[4]), .\grant[5] (grant[5]), .\grant[6] (grant[6]), .\grant[7] (grant[7]),
    .\grant[8] (grant[8]), .\grant[9] (grant[9]), .\grant[10] (grant[10]), .\grant[11] (grant[11]),
    .\grant[12] (grant[12]), .\grant[13] (grant[13]), .\grant[14] (grant[14]), .\grant[15] (grant[15]),
    .\grant[16] (grant[16]), .\grant[17] (grant[17]), .\grant[18] (grant[18]), .\grant[19] (grant[19]),
    .\grant[20] (grant[20]), .\grant[21] (grant[21]), .\grant[22] (grant[22]), .\grant[23] (grant[23]),
    .\grant[24] (grant[24]), .\grant[25] (grant[25]), .\grant[26] (grant[26]), .\grant[27] (grant[27]),
    .\grant[28] (grant[28]), .\grant[29] (grant[29]), .\grant[30] (grant[30]), .\grant[31] (grant[31]),
    .\grant[32] (grant[32]), .\grant[33] (grant[33]), .\grant[34] (grant[34]), .\grant[35] (grant[35]),
    .\grant[36] (grant[36]), .\grant[37] (grant[37]), .\grant[38] (grant[38]), .\grant[39] (grant[39]),
    .\grant[40] (grant[40]), .\grant[41] (grant[41]), .\grant[42] (grant[42]), .\grant[43] (grant[43]),
    .\grant[44] (grant[44]), .\grant[45] (grant[45]), .\grant[46] (grant[46]), .\grant[47] (grant[47]),
    .\grant[48] (grant[48]), .\grant[49] (grant[49]), .\grant[50] (grant[50]), .\grant[51] (grant[51]),
    .\grant[52] (grant[52]), .\grant[53] (grant[53]), .\grant[54] (grant[54]), .\grant[55] (grant[55]),
    .\grant[56] (grant[56]), .\grant[57] (grant[57]), .\grant[58] (grant[58]), .\grant[59] (grant[59]),
    .\grant[60] (grant[60]), .\grant[61] (grant[61]), .\grant[62] (grant[62]), .\grant[63] (grant[63]),
    .\grant[64] (grant[64]), .\grant[65] (grant[65]), .\grant[66] (grant[66]), .\grant[67] (grant[67]),
    .\grant[68] (grant[68]), .\grant[69] (grant[69]), .\grant[70] (grant[70]), .\grant[71] (grant[71]),
    .\grant[72] (grant[72]), .\grant[73] (grant[73]), .\grant[74] (grant[74]), .\grant[75] (grant[75]),
    .\grant[76] (grant[76]), .\grant[77] (grant[77]), .\grant[78] (grant[78]), .\grant[79] (grant[79]),
    .\grant[80] (grant[80]), .\grant[81] (grant[81]), .\grant[82] (grant[82]), .\grant[83] (grant[83]),
    .\grant[84] (grant[84]), .\grant[85] (grant[85]), .\grant[86] (grant[86]), .\grant[87] (grant[87]),
    .\grant[88] (grant[88]), .\grant[89] (grant[89]), .\grant[90] (grant[90]), .\grant[91] (grant[91]),
    .\grant[92] (grant[92]), .\grant[93] (grant[93]), .\grant[94] (grant[94]), .\grant[95] (grant[95]),
    .\grant[96] (grant[96]), .\grant[97] (grant[97]), .\grant[98] (grant[98]), .\grant[99] (grant[99]),
    .\grant[100] (grant[100]), .\grant[101] (grant[101]), .\grant[102] (grant[102]), .\grant[103] (grant[103]),
    .\grant[104] (grant[104]), .\grant[105] (grant[105]), .\grant[106] (grant[106]), .\grant[107] (grant[107]),
    .\grant[108] (grant[108]), .\grant[109] (grant[109]), .\grant[110] (grant[110]), .\grant[111] (grant[111]),
    .\grant[112] (grant[112]), .\grant[113] (grant[113]), .\grant[114] (grant[114]), .\grant[115] (grant[115]),
    .\grant[116] (grant[116]), .\grant[117] (grant[117]), .\grant[118] (grant[118]), .\grant[119] (grant[119]),
    .\grant[120] (grant[120]), .\grant[121] (grant[121]), .\grant[122] (grant[122]), .\grant[123] (grant[123]),
    .\grant[124] (grant[124]), .\grant[125] (grant[125]), .\grant[126] (grant[126]), .\grant[127] (grant[127]),
    .anyGrant (anyGrant)
  );

  task run_stimulus_pass;
  begin
    priority_in = 128'b1;
    req = 128'b0;

    #100;
    $display("--- Start 128-Anchor Pure PW v13_PW (Ref Only) ---");

    for (i = 0; i < 128; i = i + 1) begin
        priority_in = (128'b1 << i);
        
        // 64 Pairwise Patterns (Using all 128 bits: 0-64, 1-65, ..., 63-127)
        for (j = 0; j < 64; j = j + 1) begin
            req = (128'b1 << j) | (128'b1 << (j + 64)); 
            #10; $display("o_sum=%h", {anyGrant, grant});
        end

        // IDLE
        req = 0;
        #10; $display("o_sum=%h", {anyGrant, grant});
    end

    // $finish; // disabled
  end
  endtask


  // VCD output
  reg [510:0] dumpfile_name;
  initial begin
    if ($value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
      $dumpfile(dumpfile_name);
      $dumpvars(0, tb);
    end
  end

  initial begin
    #1;
    $display("FAULT_INJECTED: full_saturation_pure_pw_v13_pw");
  end


  // ===== Verilator 故障注入控制 (简化版) =====
  // 故障注入 MUX 已在网表中插入，TB 只需设置 uut.__FAULT_ID

  // 故障注入控制器
  integer __batch_fid;
  integer __BATCH_START, __BATCH_END;

  initial begin
    if (!$value$plusargs("BATCH_START=%d", __BATCH_START)) __BATCH_START = 0;
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 23422;

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
