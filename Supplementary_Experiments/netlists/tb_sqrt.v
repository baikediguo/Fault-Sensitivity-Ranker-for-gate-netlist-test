`timescale 1ns / 1ps

module tb;

  // Vector signals for logic and display
  reg [127:0] a_vec;
  wire [63:0] asqrt_vec;

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
    .\a[64] (a_vec[64]),
    .\a[65] (a_vec[65]),
    .\a[66] (a_vec[66]),
    .\a[67] (a_vec[67]),
    .\a[68] (a_vec[68]),
    .\a[69] (a_vec[69]),
    .\a[70] (a_vec[70]),
    .\a[71] (a_vec[71]),
    .\a[72] (a_vec[72]),
    .\a[73] (a_vec[73]),
    .\a[74] (a_vec[74]),
    .\a[75] (a_vec[75]),
    .\a[76] (a_vec[76]),
    .\a[77] (a_vec[77]),
    .\a[78] (a_vec[78]),
    .\a[79] (a_vec[79]),
    .\a[80] (a_vec[80]),
    .\a[81] (a_vec[81]),
    .\a[82] (a_vec[82]),
    .\a[83] (a_vec[83]),
    .\a[84] (a_vec[84]),
    .\a[85] (a_vec[85]),
    .\a[86] (a_vec[86]),
    .\a[87] (a_vec[87]),
    .\a[88] (a_vec[88]),
    .\a[89] (a_vec[89]),
    .\a[90] (a_vec[90]),
    .\a[91] (a_vec[91]),
    .\a[92] (a_vec[92]),
    .\a[93] (a_vec[93]),
    .\a[94] (a_vec[94]),
    .\a[95] (a_vec[95]),
    .\a[96] (a_vec[96]),
    .\a[97] (a_vec[97]),
    .\a[98] (a_vec[98]),
    .\a[99] (a_vec[99]),
    .\a[100] (a_vec[100]),
    .\a[101] (a_vec[101]),
    .\a[102] (a_vec[102]),
    .\a[103] (a_vec[103]),
    .\a[104] (a_vec[104]),
    .\a[105] (a_vec[105]),
    .\a[106] (a_vec[106]),
    .\a[107] (a_vec[107]),
    .\a[108] (a_vec[108]),
    .\a[109] (a_vec[109]),
    .\a[110] (a_vec[110]),
    .\a[111] (a_vec[111]),
    .\a[112] (a_vec[112]),
    .\a[113] (a_vec[113]),
    .\a[114] (a_vec[114]),
    .\a[115] (a_vec[115]),
    .\a[116] (a_vec[116]),
    .\a[117] (a_vec[117]),
    .\a[118] (a_vec[118]),
    .\a[119] (a_vec[119]),
    .\a[120] (a_vec[120]),
    .\a[121] (a_vec[121]),
    .\a[122] (a_vec[122]),
    .\a[123] (a_vec[123]),
    .\a[124] (a_vec[124]),
    .\a[125] (a_vec[125]),
    .\a[126] (a_vec[126]),
    .\a[127] (a_vec[127]),
    .\asqrt[0] (asqrt_vec[0]),
    .\asqrt[1] (asqrt_vec[1]),
    .\asqrt[2] (asqrt_vec[2]),
    .\asqrt[3] (asqrt_vec[3]),
    .\asqrt[4] (asqrt_vec[4]),
    .\asqrt[5] (asqrt_vec[5]),
    .\asqrt[6] (asqrt_vec[6]),
    .\asqrt[7] (asqrt_vec[7]),
    .\asqrt[8] (asqrt_vec[8]),
    .\asqrt[9] (asqrt_vec[9]),
    .\asqrt[10] (asqrt_vec[10]),
    .\asqrt[11] (asqrt_vec[11]),
    .\asqrt[12] (asqrt_vec[12]),
    .\asqrt[13] (asqrt_vec[13]),
    .\asqrt[14] (asqrt_vec[14]),
    .\asqrt[15] (asqrt_vec[15]),
    .\asqrt[16] (asqrt_vec[16]),
    .\asqrt[17] (asqrt_vec[17]),
    .\asqrt[18] (asqrt_vec[18]),
    .\asqrt[19] (asqrt_vec[19]),
    .\asqrt[20] (asqrt_vec[20]),
    .\asqrt[21] (asqrt_vec[21]),
    .\asqrt[22] (asqrt_vec[22]),
    .\asqrt[23] (asqrt_vec[23]),
    .\asqrt[24] (asqrt_vec[24]),
    .\asqrt[25] (asqrt_vec[25]),
    .\asqrt[26] (asqrt_vec[26]),
    .\asqrt[27] (asqrt_vec[27]),
    .\asqrt[28] (asqrt_vec[28]),
    .\asqrt[29] (asqrt_vec[29]),
    .\asqrt[30] (asqrt_vec[30]),
    .\asqrt[31] (asqrt_vec[31]),
    .\asqrt[32] (asqrt_vec[32]),
    .\asqrt[33] (asqrt_vec[33]),
    .\asqrt[34] (asqrt_vec[34]),
    .\asqrt[35] (asqrt_vec[35]),
    .\asqrt[36] (asqrt_vec[36]),
    .\asqrt[37] (asqrt_vec[37]),
    .\asqrt[38] (asqrt_vec[38]),
    .\asqrt[39] (asqrt_vec[39]),
    .\asqrt[40] (asqrt_vec[40]),
    .\asqrt[41] (asqrt_vec[41]),
    .\asqrt[42] (asqrt_vec[42]),
    .\asqrt[43] (asqrt_vec[43]),
    .\asqrt[44] (asqrt_vec[44]),
    .\asqrt[45] (asqrt_vec[45]),
    .\asqrt[46] (asqrt_vec[46]),
    .\asqrt[47] (asqrt_vec[47]),
    .\asqrt[48] (asqrt_vec[48]),
    .\asqrt[49] (asqrt_vec[49]),
    .\asqrt[50] (asqrt_vec[50]),
    .\asqrt[51] (asqrt_vec[51]),
    .\asqrt[52] (asqrt_vec[52]),
    .\asqrt[53] (asqrt_vec[53]),
    .\asqrt[54] (asqrt_vec[54]),
    .\asqrt[55] (asqrt_vec[55]),
    .\asqrt[56] (asqrt_vec[56]),
    .\asqrt[57] (asqrt_vec[57]),
    .\asqrt[58] (asqrt_vec[58]),
    .\asqrt[59] (asqrt_vec[59]),
    .\asqrt[60] (asqrt_vec[60]),
    .\asqrt[61] (asqrt_vec[61]),
    .\asqrt[62] (asqrt_vec[62]),
    .\asqrt[63] (asqrt_vec[63])
  );

  integer i;
  localparam STEPS = 128;

  initial begin
    // 所有输入初始化为0
    a_vec = 128'b0;
    #10;

    $display("=== Sqrt Circuit Priority Stimulus V1 ===");
    $display("Strategy: a[0-15] every 2, a[16-31] every 32, a[32-127] static 0");

    for (i = 0; i < STEPS; i = i + 1) begin

        // === HIGH PRIORITY: a[0-15] - FAST TOGGLE ===
        if ((i % 2) == 0) begin
            a_vec[0] = i[1];
            a_vec[1] = i[2];
            a_vec[2] = i[3];
            a_vec[3] = i[4];
            a_vec[4] = i[5];
            a_vec[5] = i[6];
            a_vec[6] = i[7];
            a_vec[7] = i[1] ^ i[2];
            a_vec[8] = i[2] ^ i[3];
            a_vec[9] = i[3] ^ i[4];
            a_vec[10] = i[4] ^ i[5];
            a_vec[11] = i[5] ^ i[6];
            a_vec[12] = i[6] ^ i[7];
            a_vec[13] = i[1] ^ i[3];
            a_vec[14] = i[2] ^ i[4];
            a_vec[15] = i[3] ^ i[5];
        end

        // === MEDIUM PRIORITY: a[16-47] - EVERY 32 STEPS ===
        if ((i % 32) == 0) begin
            a_vec[47:16] = {4{i[7:0]}};
        end

        // === LOW PRIORITY: a[48-127] - STATIC 0 ===
        // a_vec[127:48] remains 0

        #1;
        $display("o_sum=%04x", asqrt_vec[15:0]);
    end

    $display("o_sum=%04x [final]", asqrt_vec[15:0]);
    $display("=== Test Complete ===");
    $finish;
  end

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

endmodule
