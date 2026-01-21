`timescale 1ns / 1ps

module tb;

  reg \a[0] ;
  reg \a[100] ;
  reg \a[101] ;
  reg \a[102] ;
  reg \a[103] ;
  reg \a[104] ;
  reg \a[105] ;
  reg \a[106] ;
  reg \a[107] ;
  reg \a[108] ;
  reg \a[109] ;
  reg \a[10] ;
  reg \a[110] ;
  reg \a[111] ;
  reg \a[112] ;
  reg \a[113] ;
  reg \a[114] ;
  reg \a[115] ;
  reg \a[116] ;
  reg \a[117] ;
  reg \a[118] ;
  reg \a[119] ;
  reg \a[11] ;
  reg \a[120] ;
  reg \a[121] ;
  reg \a[122] ;
  reg \a[123] ;
  reg \a[124] ;
  reg \a[125] ;
  reg \a[126] ;
  reg \a[127] ;
  reg \a[12] ;
  reg \a[13] ;
  reg \a[14] ;
  reg \a[15] ;
  reg \a[16] ;
  reg \a[17] ;
  reg \a[18] ;
  reg \a[19] ;
  reg \a[1] ;
  reg \a[20] ;
  reg \a[21] ;
  reg \a[22] ;
  reg \a[23] ;
  reg \a[24] ;
  reg \a[25] ;
  reg \a[26] ;
  reg \a[27] ;
  reg \a[28] ;
  reg \a[29] ;
  reg \a[2] ;
  reg \a[30] ;
  reg \a[31] ;
  reg \a[32] ;
  reg \a[33] ;
  reg \a[34] ;
  reg \a[35] ;
  reg \a[36] ;
  reg \a[37] ;
  reg \a[38] ;
  reg \a[39] ;
  reg \a[3] ;
  reg \a[40] ;
  reg \a[41] ;
  reg \a[42] ;
  reg \a[43] ;
  reg \a[44] ;
  reg \a[45] ;
  reg \a[46] ;
  reg \a[47] ;
  reg \a[48] ;
  reg \a[49] ;
  reg \a[4] ;
  reg \a[50] ;
  reg \a[51] ;
  reg \a[52] ;
  reg \a[53] ;
  reg \a[54] ;
  reg \a[55] ;
  reg \a[56] ;
  reg \a[57] ;
  reg \a[58] ;
  reg \a[59] ;
  reg \a[5] ;
  reg \a[60] ;
  reg \a[61] ;
  reg \a[62] ;
  reg \a[63] ;
  reg \a[64] ;
  reg \a[65] ;
  reg \a[66] ;
  reg \a[67] ;
  reg \a[68] ;
  reg \a[69] ;
  reg \a[6] ;
  reg \a[70] ;
  reg \a[71] ;
  reg \a[72] ;
  reg \a[73] ;
  reg \a[74] ;
  reg \a[75] ;
  reg \a[76] ;
  reg \a[77] ;
  reg \a[78] ;
  reg \a[79] ;
  reg \a[7] ;
  reg \a[80] ;
  reg \a[81] ;
  reg \a[82] ;
  reg \a[83] ;
  reg \a[84] ;
  reg \a[85] ;
  reg \a[86] ;
  reg \a[87] ;
  reg \a[88] ;
  reg \a[89] ;
  reg \a[8] ;
  reg \a[90] ;
  reg \a[91] ;
  reg \a[92] ;
  reg \a[93] ;
  reg \a[94] ;
  reg \a[95] ;
  reg \a[96] ;
  reg \a[97] ;
  reg \a[98] ;
  reg \a[99] ;
  reg \a[9] ;
  reg \shift[0] ;
  reg \shift[1] ;
  reg \shift[2] ;
  reg \shift[3] ;
  reg \shift[4] ;
  reg \shift[5] ;
  reg \shift[6] ;
  wire \result[0] ;
  wire \result[100] ;
  wire \result[101] ;
  wire \result[102] ;
  wire \result[103] ;
  wire \result[104] ;
  wire \result[105] ;
  wire \result[106] ;
  wire \result[107] ;
  wire \result[108] ;
  wire \result[109] ;
  wire \result[10] ;
  wire \result[110] ;
  wire \result[111] ;
  wire \result[112] ;
  wire \result[113] ;
  wire \result[114] ;
  wire \result[115] ;
  wire \result[116] ;
  wire \result[117] ;
  wire \result[118] ;
  wire \result[119] ;
  wire \result[11] ;
  wire \result[120] ;
  wire \result[121] ;
  wire \result[122] ;
  wire \result[123] ;
  wire \result[124] ;
  wire \result[125] ;
  wire \result[126] ;
  wire \result[127] ;
  wire \result[12] ;
  wire \result[13] ;
  wire \result[14] ;
  wire \result[15] ;
  wire \result[16] ;
  wire \result[17] ;
  wire \result[18] ;
  wire \result[19] ;
  wire \result[1] ;
  wire \result[20] ;
  wire \result[21] ;
  wire \result[22] ;
  wire \result[23] ;
  wire \result[24] ;
  wire \result[25] ;
  wire \result[26] ;
  wire \result[27] ;
  wire \result[28] ;
  wire \result[29] ;
  wire \result[2] ;
  wire \result[30] ;
  wire \result[31] ;
  wire \result[32] ;
  wire \result[33] ;
  wire \result[34] ;
  wire \result[35] ;
  wire \result[36] ;
  wire \result[37] ;
  wire \result[38] ;
  wire \result[39] ;
  wire \result[3] ;
  wire \result[40] ;
  wire \result[41] ;
  wire \result[42] ;
  wire \result[43] ;
  wire \result[44] ;
  wire \result[45] ;
  wire \result[46] ;
  wire \result[47] ;
  wire \result[48] ;
  wire \result[49] ;
  wire \result[4] ;
  wire \result[50] ;
  wire \result[51] ;
  wire \result[52] ;
  wire \result[53] ;
  wire \result[54] ;
  wire \result[55] ;
  wire \result[56] ;
  wire \result[57] ;
  wire \result[58] ;
  wire \result[59] ;
  wire \result[5] ;
  wire \result[60] ;
  wire \result[61] ;
  wire \result[62] ;
  wire \result[63] ;
  wire \result[64] ;
  wire \result[65] ;
  wire \result[66] ;
  wire \result[67] ;
  wire \result[68] ;
  wire \result[69] ;
  wire \result[6] ;
  wire \result[70] ;
  wire \result[71] ;
  wire \result[72] ;
  wire \result[73] ;
  wire \result[74] ;
  wire \result[75] ;
  wire \result[76] ;
  wire \result[77] ;
  wire \result[78] ;
  wire \result[79] ;
  wire \result[7] ;
  wire \result[80] ;
  wire \result[81] ;
  wire \result[82] ;
  wire \result[83] ;
  wire \result[84] ;
  wire \result[85] ;
  wire \result[86] ;
  wire \result[87] ;
  wire \result[88] ;
  wire \result[89] ;
  wire \result[8] ;
  wire \result[90] ;
  wire \result[91] ;
  wire \result[92] ;
  wire \result[93] ;
  wire \result[94] ;
  wire \result[95] ;
  wire \result[96] ;
  wire \result[97] ;
  wire \result[98] ;
  wire \result[99] ;
  wire \result[9] ;

  // DUT (combinational)
  top uut (
    .\a[0] (\a[0] ),
    .\a[100] (\a[100] ),
    .\a[101] (\a[101] ),
    .\a[102] (\a[102] ),
    .\a[103] (\a[103] ),
    .\a[104] (\a[104] ),
    .\a[105] (\a[105] ),
    .\a[106] (\a[106] ),
    .\a[107] (\a[107] ),
    .\a[108] (\a[108] ),
    .\a[109] (\a[109] ),
    .\a[10] (\a[10] ),
    .\a[110] (\a[110] ),
    .\a[111] (\a[111] ),
    .\a[112] (\a[112] ),
    .\a[113] (\a[113] ),
    .\a[114] (\a[114] ),
    .\a[115] (\a[115] ),
    .\a[116] (\a[116] ),
    .\a[117] (\a[117] ),
    .\a[118] (\a[118] ),
    .\a[119] (\a[119] ),
    .\a[11] (\a[11] ),
    .\a[120] (\a[120] ),
    .\a[121] (\a[121] ),
    .\a[122] (\a[122] ),
    .\a[123] (\a[123] ),
    .\a[124] (\a[124] ),
    .\a[125] (\a[125] ),
    .\a[126] (\a[126] ),
    .\a[127] (\a[127] ),
    .\a[12] (\a[12] ),
    .\a[13] (\a[13] ),
    .\a[14] (\a[14] ),
    .\a[15] (\a[15] ),
    .\a[16] (\a[16] ),
    .\a[17] (\a[17] ),
    .\a[18] (\a[18] ),
    .\a[19] (\a[19] ),
    .\a[1] (\a[1] ),
    .\a[20] (\a[20] ),
    .\a[21] (\a[21] ),
    .\a[22] (\a[22] ),
    .\a[23] (\a[23] ),
    .\a[24] (\a[24] ),
    .\a[25] (\a[25] ),
    .\a[26] (\a[26] ),
    .\a[27] (\a[27] ),
    .\a[28] (\a[28] ),
    .\a[29] (\a[29] ),
    .\a[2] (\a[2] ),
    .\a[30] (\a[30] ),
    .\a[31] (\a[31] ),
    .\a[32] (\a[32] ),
    .\a[33] (\a[33] ),
    .\a[34] (\a[34] ),
    .\a[35] (\a[35] ),
    .\a[36] (\a[36] ),
    .\a[37] (\a[37] ),
    .\a[38] (\a[38] ),
    .\a[39] (\a[39] ),
    .\a[3] (\a[3] ),
    .\a[40] (\a[40] ),
    .\a[41] (\a[41] ),
    .\a[42] (\a[42] ),
    .\a[43] (\a[43] ),
    .\a[44] (\a[44] ),
    .\a[45] (\a[45] ),
    .\a[46] (\a[46] ),
    .\a[47] (\a[47] ),
    .\a[48] (\a[48] ),
    .\a[49] (\a[49] ),
    .\a[4] (\a[4] ),
    .\a[50] (\a[50] ),
    .\a[51] (\a[51] ),
    .\a[52] (\a[52] ),
    .\a[53] (\a[53] ),
    .\a[54] (\a[54] ),
    .\a[55] (\a[55] ),
    .\a[56] (\a[56] ),
    .\a[57] (\a[57] ),
    .\a[58] (\a[58] ),
    .\a[59] (\a[59] ),
    .\a[5] (\a[5] ),
    .\a[60] (\a[60] ),
    .\a[61] (\a[61] ),
    .\a[62] (\a[62] ),
    .\a[63] (\a[63] ),
    .\a[64] (\a[64] ),
    .\a[65] (\a[65] ),
    .\a[66] (\a[66] ),
    .\a[67] (\a[67] ),
    .\a[68] (\a[68] ),
    .\a[69] (\a[69] ),
    .\a[6] (\a[6] ),
    .\a[70] (\a[70] ),
    .\a[71] (\a[71] ),
    .\a[72] (\a[72] ),
    .\a[73] (\a[73] ),
    .\a[74] (\a[74] ),
    .\a[75] (\a[75] ),
    .\a[76] (\a[76] ),
    .\a[77] (\a[77] ),
    .\a[78] (\a[78] ),
    .\a[79] (\a[79] ),
    .\a[7] (\a[7] ),
    .\a[80] (\a[80] ),
    .\a[81] (\a[81] ),
    .\a[82] (\a[82] ),
    .\a[83] (\a[83] ),
    .\a[84] (\a[84] ),
    .\a[85] (\a[85] ),
    .\a[86] (\a[86] ),
    .\a[87] (\a[87] ),
    .\a[88] (\a[88] ),
    .\a[89] (\a[89] ),
    .\a[8] (\a[8] ),
    .\a[90] (\a[90] ),
    .\a[91] (\a[91] ),
    .\a[92] (\a[92] ),
    .\a[93] (\a[93] ),
    .\a[94] (\a[94] ),
    .\a[95] (\a[95] ),
    .\a[96] (\a[96] ),
    .\a[97] (\a[97] ),
    .\a[98] (\a[98] ),
    .\a[99] (\a[99] ),
    .\a[9] (\a[9] ),
    .\shift[0] (\shift[0] ),
    .\shift[1] (\shift[1] ),
    .\shift[2] (\shift[2] ),
    .\shift[3] (\shift[3] ),
    .\shift[4] (\shift[4] ),
    .\shift[5] (\shift[5] ),
    .\shift[6] (\shift[6] ),
    .\result[0] (\result[0] ),
    .\result[100] (\result[100] ),
    .\result[101] (\result[101] ),
    .\result[102] (\result[102] ),
    .\result[103] (\result[103] ),
    .\result[104] (\result[104] ),
    .\result[105] (\result[105] ),
    .\result[106] (\result[106] ),
    .\result[107] (\result[107] ),
    .\result[108] (\result[108] ),
    .\result[109] (\result[109] ),
    .\result[10] (\result[10] ),
    .\result[110] (\result[110] ),
    .\result[111] (\result[111] ),
    .\result[112] (\result[112] ),
    .\result[113] (\result[113] ),
    .\result[114] (\result[114] ),
    .\result[115] (\result[115] ),
    .\result[116] (\result[116] ),
    .\result[117] (\result[117] ),
    .\result[118] (\result[118] ),
    .\result[119] (\result[119] ),
    .\result[11] (\result[11] ),
    .\result[120] (\result[120] ),
    .\result[121] (\result[121] ),
    .\result[122] (\result[122] ),
    .\result[123] (\result[123] ),
    .\result[124] (\result[124] ),
    .\result[125] (\result[125] ),
    .\result[126] (\result[126] ),
    .\result[127] (\result[127] ),
    .\result[12] (\result[12] ),
    .\result[13] (\result[13] ),
    .\result[14] (\result[14] ),
    .\result[15] (\result[15] ),
    .\result[16] (\result[16] ),
    .\result[17] (\result[17] ),
    .\result[18] (\result[18] ),
    .\result[19] (\result[19] ),
    .\result[1] (\result[1] ),
    .\result[20] (\result[20] ),
    .\result[21] (\result[21] ),
    .\result[22] (\result[22] ),
    .\result[23] (\result[23] ),
    .\result[24] (\result[24] ),
    .\result[25] (\result[25] ),
    .\result[26] (\result[26] ),
    .\result[27] (\result[27] ),
    .\result[28] (\result[28] ),
    .\result[29] (\result[29] ),
    .\result[2] (\result[2] ),
    .\result[30] (\result[30] ),
    .\result[31] (\result[31] ),
    .\result[32] (\result[32] ),
    .\result[33] (\result[33] ),
    .\result[34] (\result[34] ),
    .\result[35] (\result[35] ),
    .\result[36] (\result[36] ),
    .\result[37] (\result[37] ),
    .\result[38] (\result[38] ),
    .\result[39] (\result[39] ),
    .\result[3] (\result[3] ),
    .\result[40] (\result[40] ),
    .\result[41] (\result[41] ),
    .\result[42] (\result[42] ),
    .\result[43] (\result[43] ),
    .\result[44] (\result[44] ),
    .\result[45] (\result[45] ),
    .\result[46] (\result[46] ),
    .\result[47] (\result[47] ),
    .\result[48] (\result[48] ),
    .\result[49] (\result[49] ),
    .\result[4] (\result[4] ),
    .\result[50] (\result[50] ),
    .\result[51] (\result[51] ),
    .\result[52] (\result[52] ),
    .\result[53] (\result[53] ),
    .\result[54] (\result[54] ),
    .\result[55] (\result[55] ),
    .\result[56] (\result[56] ),
    .\result[57] (\result[57] ),
    .\result[58] (\result[58] ),
    .\result[59] (\result[59] ),
    .\result[5] (\result[5] ),
    .\result[60] (\result[60] ),
    .\result[61] (\result[61] ),
    .\result[62] (\result[62] ),
    .\result[63] (\result[63] ),
    .\result[64] (\result[64] ),
    .\result[65] (\result[65] ),
    .\result[66] (\result[66] ),
    .\result[67] (\result[67] ),
    .\result[68] (\result[68] ),
    .\result[69] (\result[69] ),
    .\result[6] (\result[6] ),
    .\result[70] (\result[70] ),
    .\result[71] (\result[71] ),
    .\result[72] (\result[72] ),
    .\result[73] (\result[73] ),
    .\result[74] (\result[74] ),
    .\result[75] (\result[75] ),
    .\result[76] (\result[76] ),
    .\result[77] (\result[77] ),
    .\result[78] (\result[78] ),
    .\result[79] (\result[79] ),
    .\result[7] (\result[7] ),
    .\result[80] (\result[80] ),
    .\result[81] (\result[81] ),
    .\result[82] (\result[82] ),
    .\result[83] (\result[83] ),
    .\result[84] (\result[84] ),
    .\result[85] (\result[85] ),
    .\result[86] (\result[86] ),
    .\result[87] (\result[87] ),
    .\result[88] (\result[88] ),
    .\result[89] (\result[89] ),
    .\result[8] (\result[8] ),
    .\result[90] (\result[90] ),
    .\result[91] (\result[91] ),
    .\result[92] (\result[92] ),
    .\result[93] (\result[93] ),
    .\result[94] (\result[94] ),
    .\result[95] (\result[95] ),
    .\result[96] (\result[96] ),
    .\result[97] (\result[97] ),
    .\result[98] (\result[98] ),
    .\result[99] (\result[99] ),
    .\result[9] (\result[9] )
  );

  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF;
  endfunction

  integer i;
  parameter CYCLES = 256;
  parameter PRINT_EVERY = 1;

  task run_stimulus_pass;
  begin
    \a[0] = 0;
    \a[100] = 0;
    \a[101] = 0;
    \a[102] = 0;
    \a[103] = 0;
    \a[104] = 0;
    \a[105] = 0;
    \a[106] = 0;
    \a[107] = 0;
    \a[108] = 0;
    \a[109] = 0;
    \a[10] = 0;
    \a[110] = 0;
    \a[111] = 0;
    \a[112] = 0;
    \a[113] = 0;
    \a[114] = 0;
    \a[115] = 0;
    \a[116] = 0;
    \a[117] = 0;
    \a[118] = 0;
    \a[119] = 0;
    \a[11] = 0;
    \a[120] = 0;
    \a[121] = 0;
    \a[122] = 0;
    \a[123] = 0;
    \a[124] = 0;
    \a[125] = 0;
    \a[126] = 0;
    \a[127] = 0;
    \a[12] = 0;
    \a[13] = 0;
    \a[14] = 0;
    \a[15] = 0;
    \a[16] = 0;
    \a[17] = 0;
    \a[18] = 0;
    \a[19] = 0;
    \a[1] = 0;
    \a[20] = 0;
    \a[21] = 0;
    \a[22] = 0;
    \a[23] = 0;
    \a[24] = 0;
    \a[25] = 0;
    \a[26] = 0;
    \a[27] = 0;
    \a[28] = 0;
    \a[29] = 0;
    \a[2] = 0;
    \a[30] = 0;
    \a[31] = 0;
    \a[32] = 0;
    \a[33] = 0;
    \a[34] = 0;
    \a[35] = 0;
    \a[36] = 0;
    \a[37] = 0;
    \a[38] = 0;
    \a[39] = 0;
    \a[3] = 0;
    \a[40] = 0;
    \a[41] = 0;
    \a[42] = 0;
    \a[43] = 0;
    \a[44] = 0;
    \a[45] = 0;
    \a[46] = 0;
    \a[47] = 0;
    \a[48] = 0;
    \a[49] = 0;
    \a[4] = 0;
    \a[50] = 0;
    \a[51] = 0;
    \a[52] = 0;
    \a[53] = 0;
    \a[54] = 0;
    \a[55] = 0;
    \a[56] = 0;
    \a[57] = 0;
    \a[58] = 0;
    \a[59] = 0;
    \a[5] = 0;
    \a[60] = 0;
    \a[61] = 0;
    \a[62] = 0;
    \a[63] = 0;
    \a[64] = 0;
    \a[65] = 0;
    \a[66] = 0;
    \a[67] = 0;
    \a[68] = 0;
    \a[69] = 0;
    \a[6] = 0;
    \a[70] = 0;
    \a[71] = 0;
    \a[72] = 0;
    \a[73] = 0;
    \a[74] = 0;
    \a[75] = 0;
    \a[76] = 0;
    \a[77] = 0;
    \a[78] = 0;
    \a[79] = 0;
    \a[7] = 0;
    \a[80] = 0;
    \a[81] = 0;
    \a[82] = 0;
    \a[83] = 0;
    \a[84] = 0;
    \a[85] = 0;
    \a[86] = 0;
    \a[87] = 0;
    \a[88] = 0;
    \a[89] = 0;
    \a[8] = 0;
    \a[90] = 0;
    \a[91] = 0;
    \a[92] = 0;
    \a[93] = 0;
    \a[94] = 0;
    \a[95] = 0;
    \a[96] = 0;
    \a[97] = 0;
    \a[98] = 0;
    \a[99] = 0;
    \a[9] = 0;
    \shift[0] = 0;
    \shift[1] = 0;
    \shift[2] = 0;
    \shift[3] = 0;
    \shift[4] = 0;
    \shift[5] = 0;
    \shift[6] = 0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        // \a[0]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[0] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[0] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[0] = (i + 0) % 2;  // Phase3
          end
        end

        // \a[100]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[100] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[100] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[100] = (i + 1) % 2;  // Phase3
          end
        end

        // \a[101]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[101] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[101] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[101] = (i + 2) % 2;  // Phase3
          end
        end

        // \a[102]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[102] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[102] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[102] = (i + 3) % 2;  // Phase3
          end
        end

        // \a[103]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[103] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[103] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[103] = (i + 4) % 2;  // Phase3
          end
        end

        // \a[104]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[104] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[104] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[104] = (i + 5) % 2;  // Phase3
          end
        end

        // \a[105]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[105] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[105] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[105] = (i + 6) % 2;  // Phase3
          end
        end

        // \a[106]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[106] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[106] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[106] = (i + 7) % 2;  // Phase3
          end
        end

        // \a[107]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[107] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[107] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[107] = (i + 8) % 2;  // Phase3
          end
        end

        // \a[108]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[108] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[108] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[108] = (i + 9) % 2;  // Phase3
          end
        end

        // \a[109]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[109] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[109] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[109] = (i + 10) % 2;  // Phase3
          end
        end

        // \a[10]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[10] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[10] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[10] = (i + 11) % 2;  // Phase3
          end
        end

        // \a[110]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[110] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[110] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[110] = (i + 12) % 2;  // Phase3
          end
        end

        // \a[111]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[111] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[111] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[111] = (i + 13) % 2;  // Phase3
          end
        end

        // \a[112]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[112] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[112] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[112] = (i + 14) % 2;  // Phase3
          end
        end

        // \a[113]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[113] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[113] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[113] = (i + 15) % 2;  // Phase3
          end
        end

        // \a[114]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[114] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[114] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[114] = (i + 16) % 2;  // Phase3
          end
        end

        // \a[115]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[115] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[115] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[115] = (i + 17) % 2;  // Phase3
          end
        end

        // \a[116]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[116] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[116] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[116] = (i + 18) % 2;  // Phase3
          end
        end

        // \a[117]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[117] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[117] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[117] = (i + 19) % 2;  // Phase3
          end
        end

        // \a[118]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[118] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[118] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[118] = (i + 20) % 2;  // Phase3
          end
        end

        // \a[119]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[119] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[119] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[119] = (i + 21) % 2;  // Phase3
          end
        end

        // \a[11]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[11] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[11] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[11] = (i + 22) % 2;  // Phase3
          end
        end

        // \a[120]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[120] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[120] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[120] = (i + 23) % 2;  // Phase3
          end
        end

        // \a[121]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[121] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[121] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[121] = (i + 24) % 2;  // Phase3
          end
        end

        // \a[122]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[122] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[122] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[122] = (i + 25) % 2;  // Phase3
          end
        end

        // \a[123]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[123] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[123] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[123] = (i + 26) % 2;  // Phase3
          end
        end

        // \a[124]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[124] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[124] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[124] = (i + 27) % 2;  // Phase3
          end
        end

        // \a[125]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[125] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[125] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[125] = (i + 28) % 2;  // Phase3
          end
        end

        // \a[126]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[126] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[126] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[126] = (i + 29) % 2;  // Phase3
          end
        end

        // \a[127]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[127] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[127] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[127] = (i + 30) % 2;  // Phase3
          end
        end

        // \a[12]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[12] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[12] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[12] = (i + 31) % 2;  // Phase3
          end
        end

        // \a[13]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[13] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[13] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[13] = (i + 32) % 2;  // Phase3
          end
        end

        // \a[14]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[14] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[14] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[14] = (i + 33) % 2;  // Phase3
          end
        end

        // \a[15]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[15] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[15] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[15] = (i + 34) % 2;  // Phase3
          end
        end

        // \a[16]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[16] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[16] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[16] = (i + 35) % 2;  // Phase3
          end
        end

        // \a[17]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[17] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[17] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[17] = (i + 36) % 2;  // Phase3
          end
        end

        // \a[18]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[18] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[18] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[18] = (i + 37) % 2;  // Phase3
          end
        end

        // \a[19]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[19] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[19] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[19] = (i + 38) % 2;  // Phase3
          end
        end

        // \a[1]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[1] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[1] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[1] = (i + 39) % 2;  // Phase3
          end
        end

        // \a[20]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[20] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[20] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[20] = (i + 40) % 2;  // Phase3
          end
        end

        // \a[21]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[21] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[21] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[21] = (i + 41) % 2;  // Phase3
          end
        end

        // \a[22]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[22] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[22] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[22] = (i + 42) % 2;  // Phase3
          end
        end

        // \a[23]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[23] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[23] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[23] = (i + 43) % 2;  // Phase3
          end
        end

        // \a[24]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[24] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[24] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[24] = (i + 44) % 2;  // Phase3
          end
        end

        // \a[25]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[25] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[25] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[25] = (i + 45) % 2;  // Phase3
          end
        end

        // \a[26]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[26] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[26] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[26] = (i + 46) % 2;  // Phase3
          end
        end

        // \a[27]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[27] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[27] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[27] = (i + 47) % 2;  // Phase3
          end
        end

        // \a[28]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[28] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[28] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[28] = (i + 48) % 2;  // Phase3
          end
        end

        // \a[29]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[29] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[29] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[29] = (i + 49) % 2;  // Phase3
          end
        end

        // \a[2]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[2] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[2] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[2] = (i + 50) % 2;  // Phase3
          end
        end

        // \a[30]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[30] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[30] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[30] = (i + 51) % 2;  // Phase3
          end
        end

        // \a[31]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[31] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[31] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[31] = (i + 52) % 2;  // Phase3
          end
        end

        // \a[32]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[32] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[32] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[32] = (i + 53) % 2;  // Phase3
          end
        end

        // \a[33]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[33] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[33] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[33] = (i + 54) % 2;  // Phase3
          end
        end

        // \a[34]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[34] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[34] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[34] = (i + 55) % 2;  // Phase3
          end
        end

        // \a[35]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[35] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[35] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[35] = (i + 56) % 2;  // Phase3
          end
        end

        // \a[36]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[36] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[36] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[36] = (i + 57) % 2;  // Phase3
          end
        end

        // \a[37]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[37] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[37] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[37] = (i + 58) % 2;  // Phase3
          end
        end

        // \a[38]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[38] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[38] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[38] = (i + 59) % 2;  // Phase3
          end
        end

        // \a[39]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[39] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[39] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[39] = (i + 60) % 2;  // Phase3
          end
        end

        // \a[3]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[3] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[3] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[3] = (i + 61) % 2;  // Phase3
          end
        end

        // \a[40]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[40] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[40] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[40] = (i + 62) % 2;  // Phase3
          end
        end

        // \a[41]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[41] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[41] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[41] = (i + 63) % 2;  // Phase3
          end
        end

        // \a[42]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[42] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[42] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[42] = (i + 64) % 2;  // Phase3
          end
        end

        // \a[43]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[43] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[43] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[43] = (i + 65) % 2;  // Phase3
          end
        end

        // \a[44]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[44] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[44] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[44] = (i + 66) % 2;  // Phase3
          end
        end

        // \a[45]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[45] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[45] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[45] = (i + 67) % 2;  // Phase3
          end
        end

        // \a[46]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[46] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[46] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[46] = (i + 68) % 2;  // Phase3
          end
        end

        // \a[47]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[47] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[47] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[47] = (i + 69) % 2;  // Phase3
          end
        end

        // \a[48]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[48] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[48] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[48] = (i + 70) % 2;  // Phase3
          end
        end

        // \a[49]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[49] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[49] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[49] = (i + 71) % 2;  // Phase3
          end
        end

        // \a[4]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[4] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[4] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[4] = (i + 72) % 2;  // Phase3
          end
        end

        // \a[50]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[50] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[50] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[50] = (i + 73) % 2;  // Phase3
          end
        end

        // \a[51]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[51] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[51] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[51] = (i + 74) % 2;  // Phase3
          end
        end

        // \a[52]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[52] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[52] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[52] = (i + 75) % 2;  // Phase3
          end
        end

        // \a[53]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[53] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[53] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[53] = (i + 76) % 2;  // Phase3
          end
        end

        // \a[54]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[54] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[54] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[54] = (i + 77) % 2;  // Phase3
          end
        end

        // \a[55]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[55] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[55] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[55] = (i + 78) % 2;  // Phase3
          end
        end

        // \a[56]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[56] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[56] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[56] = (i + 79) % 2;  // Phase3
          end
        end

        // \a[57]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[57] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[57] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[57] = (i + 80) % 2;  // Phase3
          end
        end

        // \a[58]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[58] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[58] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[58] = (i + 81) % 2;  // Phase3
          end
        end

        // \a[59]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[59] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[59] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[59] = (i + 82) % 2;  // Phase3
          end
        end

        // \a[5]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[5] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[5] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[5] = (i + 83) % 2;  // Phase3
          end
        end

        // \a[60]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[60] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[60] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[60] = (i + 84) % 2;  // Phase3
          end
        end

        // \a[61]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[61] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[61] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[61] = (i + 85) % 2;  // Phase3
          end
        end

        // \a[62]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[62] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[62] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[62] = (i + 86) % 2;  // Phase3
          end
        end

        // \a[63]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[63] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[63] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[63] = (i + 87) % 2;  // Phase3
          end
        end

        // \a[64]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[64] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[64] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[64] = (i + 88) % 2;  // Phase3
          end
        end

        // \a[65]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[65] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[65] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[65] = (i + 89) % 2;  // Phase3
          end
        end

        // \a[66]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[66] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[66] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[66] = (i + 90) % 2;  // Phase3
          end
        end

        // \a[67]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[67] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[67] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[67] = (i + 91) % 2;  // Phase3
          end
        end

        // \a[68]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[68] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[68] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[68] = (i + 92) % 2;  // Phase3
          end
        end

        // \a[69]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[69] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[69] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[69] = (i + 93) % 2;  // Phase3
          end
        end

        // \a[6]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[6] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[6] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[6] = (i + 94) % 2;  // Phase3
          end
        end

        // \a[70]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[70] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[70] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[70] = (i + 95) % 2;  // Phase3
          end
        end

        // \a[71]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[71] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[71] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[71] = (i + 96) % 2;  // Phase3
          end
        end

        // \a[72]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[72] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[72] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[72] = (i + 97) % 2;  // Phase3
          end
        end

        // \a[73]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[73] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[73] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[73] = (i + 98) % 2;  // Phase3
          end
        end

        // \a[74]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[74] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[74] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[74] = (i + 99) % 2;  // Phase3
          end
        end

        // \a[75]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[75] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[75] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[75] = (i + 100) % 2;  // Phase3
          end
        end

        // \a[76]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[76] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[76] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[76] = (i + 101) % 2;  // Phase3
          end
        end

        // \a[77]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[77] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[77] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[77] = (i + 102) % 2;  // Phase3
          end
        end

        // \a[78]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[78] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[78] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[78] = (i + 103) % 2;  // Phase3
          end
        end

        // \a[79]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[79] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[79] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[79] = (i + 104) % 2;  // Phase3
          end
        end

        // \a[7]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[7] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[7] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[7] = (i + 105) % 2;  // Phase3
          end
        end

        // \a[80]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[80] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[80] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[80] = (i + 106) % 2;  // Phase3
          end
        end

        // \a[81]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[81] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[81] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[81] = (i + 107) % 2;  // Phase3
          end
        end

        // \a[82]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[82] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[82] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[82] = (i + 108) % 2;  // Phase3
          end
        end

        // \a[83]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[83] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[83] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[83] = (i + 109) % 2;  // Phase3
          end
        end

        // \a[84]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[84] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[84] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[84] = (i + 110) % 2;  // Phase3
          end
        end

        // \a[85]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[85] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[85] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[85] = (i + 111) % 2;  // Phase3
          end
        end

        // \a[86]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[86] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[86] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[86] = (i + 112) % 2;  // Phase3
          end
        end

        // \a[87]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[87] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[87] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[87] = (i + 113) % 2;  // Phase3
          end
        end

        // \a[88]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[88] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[88] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[88] = (i + 114) % 2;  // Phase3
          end
        end

        // \a[89]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[89] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[89] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[89] = (i + 115) % 2;  // Phase3
          end
        end

        // \a[8]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[8] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[8] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[8] = (i + 116) % 2;  // Phase3
          end
        end

        // \a[90]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[90] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[90] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[90] = (i + 117) % 2;  // Phase3
          end
        end

        // \a[91]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[91] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[91] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[91] = (i + 118) % 2;  // Phase3
          end
        end

        // \a[92]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[92] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[92] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[92] = (i + 119) % 2;  // Phase3
          end
        end

        // \a[93]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[93] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[93] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[93] = (i + 120) % 2;  // Phase3
          end
        end

        // \a[94]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[94] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[94] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[94] = (i + 121) % 2;  // Phase3
          end
        end

        // \a[95]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[95] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[95] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[95] = (i + 122) % 2;  // Phase3
          end
        end

        // \a[96]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[96] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[96] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[96] = (i + 123) % 2;  // Phase3
          end
        end

        // \a[97]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[97] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[97] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[97] = (i + 124) % 2;  // Phase3
          end
        end

        // \a[98]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[98] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[98] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[98] = (i + 125) % 2;  // Phase3
          end
        end

        // \a[99]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[99] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[99] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[99] = (i + 126) % 2;  // Phase3
          end
        end

        // \a[9]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \a[9] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \a[9] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \a[9] = (i + 127) % 2;  // Phase3
          end
        end

        // \shift[0]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[0] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[0] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[0] = (i + 128) % 2;  // Phase3
          end
        end

        // \shift[1]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[1] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[1] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[1] = (i + 129) % 2;  // Phase3
          end
        end

        // \shift[2]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[2] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[2] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[2] = (i + 130) % 2;  // Phase3
          end
        end

        // \shift[3]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[3] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[3] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[3] = (i + 131) % 2;  // Phase3
          end
        end

        // \shift[4]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[4] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[4] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[4] = (i + 132) % 2;  // Phase3
          end
        end

        // \shift[5]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[5] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[5] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[5] = (i + 133) % 2;  // Phase3
          end
        end

        // \shift[6]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 85) begin
            \shift[6] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 170) begin
            \shift[6] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \shift[6] = (i + 134) % 2;  // Phase3
          end
        end

      #10;

      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", {\result[0] , \result[100] , \result[101] , \result[102] , \result[103] , \result[104] , \result[105] , \result[106] , \result[107] , \result[108] , \result[109] , \result[10] , \result[110] , \result[111] , \result[112] , \result[113] , \result[114] , \result[115] , \result[116] , \result[117] , \result[118] , \result[119] , \result[11] , \result[120] , \result[121] , \result[122] , \result[123] , \result[124] , \result[125] , \result[126] , \result[127] , \result[12] , \result[13] , \result[14] , \result[15] , \result[16] , \result[17] , \result[18] , \result[19] , \result[1] , \result[20] , \result[21] , \result[22] , \result[23] , \result[24] , \result[25] , \result[26] , \result[27] , \result[28] , \result[29] , \result[2] , \result[30] , \result[31] , \result[32] , \result[33] , \result[34] , \result[35] , \result[36] , \result[37] , \result[38] , \result[39] , \result[3] , \result[40] , \result[41] , \result[42] , \result[43] , \result[44] , \result[45] , \result[46] , \result[47] , \result[48] , \result[49] , \result[4] , \result[50] , \result[51] , \result[52] , \result[53] , \result[54] , \result[55] , \result[56] , \result[57] , \result[58] , \result[59] , \result[5] , \result[60] , \result[61] , \result[62] , \result[63] , \result[64] , \result[65] , \result[66] , \result[67] , \result[68] , \result[69] , \result[6] , \result[70] , \result[71] , \result[72] , \result[73] , \result[74] , \result[75] , \result[76] , \result[77] , \result[78] , \result[79] , \result[7] , \result[80] , \result[81] , \result[82] , \result[83] , \result[84] , \result[85] , \result[86] , \result[87] , \result[88] , \result[89] , \result[8] , \result[90] , \result[91] , \result[92] , \result[93] , \result[94] , \result[95] , \result[96] , \result[97] , \result[98] , \result[99] , \result[9] });
      end
    end

    $display("o_sum=%06x [final]", {\result[0] , \result[100] , \result[101] , \result[102] , \result[103] , \result[104] , \result[105] , \result[106] , \result[107] , \result[108] , \result[109] , \result[10] , \result[110] , \result[111] , \result[112] , \result[113] , \result[114] , \result[115] , \result[116] , \result[117] , \result[118] , \result[119] , \result[11] , \result[120] , \result[121] , \result[122] , \result[123] , \result[124] , \result[125] , \result[126] , \result[127] , \result[12] , \result[13] , \result[14] , \result[15] , \result[16] , \result[17] , \result[18] , \result[19] , \result[1] , \result[20] , \result[21] , \result[22] , \result[23] , \result[24] , \result[25] , \result[26] , \result[27] , \result[28] , \result[29] , \result[2] , \result[30] , \result[31] , \result[32] , \result[33] , \result[34] , \result[35] , \result[36] , \result[37] , \result[38] , \result[39] , \result[3] , \result[40] , \result[41] , \result[42] , \result[43] , \result[44] , \result[45] , \result[46] , \result[47] , \result[48] , \result[49] , \result[4] , \result[50] , \result[51] , \result[52] , \result[53] , \result[54] , \result[55] , \result[56] , \result[57] , \result[58] , \result[59] , \result[5] , \result[60] , \result[61] , \result[62] , \result[63] , \result[64] , \result[65] , \result[66] , \result[67] , \result[68] , \result[69] , \result[6] , \result[70] , \result[71] , \result[72] , \result[73] , \result[74] , \result[75] , \result[76] , \result[77] , \result[78] , \result[79] , \result[7] , \result[80] , \result[81] , \result[82] , \result[83] , \result[84] , \result[85] , \result[86] , \result[87] , \result[88] , \result[89] , \result[8] , \result[90] , \result[91] , \result[92] , \result[93] , \result[94] , \result[95] , \result[96] , \result[97] , \result[98] , \result[99] , \result[9] });
    // $finish; // disabled
  end
  endtask


  // VCD output - commented out for Verilator (use --trace instead)
  // reg [510:0] dumpfile_name;
  // initial begin
  //   if (!$value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
  //   end else begin
  //     $dumpfile(dumpfile_name);
  //   end
  //   $dumpvars(0, tb);
  // end


  // ===== Verilator 故障注入控制 (简化版) =====
  // 故障注入 MUX 已在网表中插入，TB 只需设置 uut.__FAULT_ID

  // 故障注入控制器
  integer __batch_fid;
  integer __BATCH_START, __BATCH_END;

  initial begin
    if (!$value$plusargs("BATCH_START=%d", __BATCH_START)) __BATCH_START = 0;
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 6416;

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
