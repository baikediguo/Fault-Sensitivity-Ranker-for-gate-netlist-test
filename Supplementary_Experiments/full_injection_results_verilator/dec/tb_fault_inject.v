`timescale 1ns / 1ps

module tb;

  reg \count[0] ;
  reg \count[1] ;
  reg \count[2] ;
  reg \count[3] ;
  reg \count[4] ;
  reg \count[5] ;
  reg \count[6] ;
  reg \count[7] ;
  wire \selectp1[0] ;
  wire \selectp1[100] ;
  wire \selectp1[101] ;
  wire \selectp1[102] ;
  wire \selectp1[103] ;
  wire \selectp1[104] ;
  wire \selectp1[105] ;
  wire \selectp1[106] ;
  wire \selectp1[107] ;
  wire \selectp1[108] ;
  wire \selectp1[109] ;
  wire \selectp1[10] ;
  wire \selectp1[110] ;
  wire \selectp1[111] ;
  wire \selectp1[112] ;
  wire \selectp1[113] ;
  wire \selectp1[114] ;
  wire \selectp1[115] ;
  wire \selectp1[116] ;
  wire \selectp1[117] ;
  wire \selectp1[118] ;
  wire \selectp1[119] ;
  wire \selectp1[11] ;
  wire \selectp1[120] ;
  wire \selectp1[121] ;
  wire \selectp1[122] ;
  wire \selectp1[123] ;
  wire \selectp1[124] ;
  wire \selectp1[125] ;
  wire \selectp1[126] ;
  wire \selectp1[127] ;
  wire \selectp1[12] ;
  wire \selectp1[13] ;
  wire \selectp1[14] ;
  wire \selectp1[15] ;
  wire \selectp1[16] ;
  wire \selectp1[17] ;
  wire \selectp1[18] ;
  wire \selectp1[19] ;
  wire \selectp1[1] ;
  wire \selectp1[20] ;
  wire \selectp1[21] ;
  wire \selectp1[22] ;
  wire \selectp1[23] ;
  wire \selectp1[24] ;
  wire \selectp1[25] ;
  wire \selectp1[26] ;
  wire \selectp1[27] ;
  wire \selectp1[28] ;
  wire \selectp1[29] ;
  wire \selectp1[2] ;
  wire \selectp1[30] ;
  wire \selectp1[31] ;
  wire \selectp1[32] ;
  wire \selectp1[33] ;
  wire \selectp1[34] ;
  wire \selectp1[35] ;
  wire \selectp1[36] ;
  wire \selectp1[37] ;
  wire \selectp1[38] ;
  wire \selectp1[39] ;
  wire \selectp1[3] ;
  wire \selectp1[40] ;
  wire \selectp1[41] ;
  wire \selectp1[42] ;
  wire \selectp1[43] ;
  wire \selectp1[44] ;
  wire \selectp1[45] ;
  wire \selectp1[46] ;
  wire \selectp1[47] ;
  wire \selectp1[48] ;
  wire \selectp1[49] ;
  wire \selectp1[4] ;
  wire \selectp1[50] ;
  wire \selectp1[51] ;
  wire \selectp1[52] ;
  wire \selectp1[53] ;
  wire \selectp1[54] ;
  wire \selectp1[55] ;
  wire \selectp1[56] ;
  wire \selectp1[57] ;
  wire \selectp1[58] ;
  wire \selectp1[59] ;
  wire \selectp1[5] ;
  wire \selectp1[60] ;
  wire \selectp1[61] ;
  wire \selectp1[62] ;
  wire \selectp1[63] ;
  wire \selectp1[64] ;
  wire \selectp1[65] ;
  wire \selectp1[66] ;
  wire \selectp1[67] ;
  wire \selectp1[68] ;
  wire \selectp1[69] ;
  wire \selectp1[6] ;
  wire \selectp1[70] ;
  wire \selectp1[71] ;
  wire \selectp1[72] ;
  wire \selectp1[73] ;
  wire \selectp1[74] ;
  wire \selectp1[75] ;
  wire \selectp1[76] ;
  wire \selectp1[77] ;
  wire \selectp1[78] ;
  wire \selectp1[79] ;
  wire \selectp1[7] ;
  wire \selectp1[80] ;
  wire \selectp1[81] ;
  wire \selectp1[82] ;
  wire \selectp1[83] ;
  wire \selectp1[84] ;
  wire \selectp1[85] ;
  wire \selectp1[86] ;
  wire \selectp1[87] ;
  wire \selectp1[88] ;
  wire \selectp1[89] ;
  wire \selectp1[8] ;
  wire \selectp1[90] ;
  wire \selectp1[91] ;
  wire \selectp1[92] ;
  wire \selectp1[93] ;
  wire \selectp1[94] ;
  wire \selectp1[95] ;
  wire \selectp1[96] ;
  wire \selectp1[97] ;
  wire \selectp1[98] ;
  wire \selectp1[99] ;
  wire \selectp1[9] ;
  wire \selectp2[0] ;
  wire \selectp2[100] ;
  wire \selectp2[101] ;
  wire \selectp2[102] ;
  wire \selectp2[103] ;
  wire \selectp2[104] ;
  wire \selectp2[105] ;
  wire \selectp2[106] ;
  wire \selectp2[107] ;
  wire \selectp2[108] ;
  wire \selectp2[109] ;
  wire \selectp2[10] ;
  wire \selectp2[110] ;
  wire \selectp2[111] ;
  wire \selectp2[112] ;
  wire \selectp2[113] ;
  wire \selectp2[114] ;
  wire \selectp2[115] ;
  wire \selectp2[116] ;
  wire \selectp2[117] ;
  wire \selectp2[118] ;
  wire \selectp2[119] ;
  wire \selectp2[11] ;
  wire \selectp2[120] ;
  wire \selectp2[121] ;
  wire \selectp2[122] ;
  wire \selectp2[123] ;
  wire \selectp2[124] ;
  wire \selectp2[125] ;
  wire \selectp2[126] ;
  wire \selectp2[127] ;
  wire \selectp2[12] ;
  wire \selectp2[13] ;
  wire \selectp2[14] ;
  wire \selectp2[15] ;
  wire \selectp2[16] ;
  wire \selectp2[17] ;
  wire \selectp2[18] ;
  wire \selectp2[19] ;
  wire \selectp2[1] ;
  wire \selectp2[20] ;
  wire \selectp2[21] ;
  wire \selectp2[22] ;
  wire \selectp2[23] ;
  wire \selectp2[24] ;
  wire \selectp2[25] ;
  wire \selectp2[26] ;
  wire \selectp2[27] ;
  wire \selectp2[28] ;
  wire \selectp2[29] ;
  wire \selectp2[2] ;
  wire \selectp2[30] ;
  wire \selectp2[31] ;
  wire \selectp2[32] ;
  wire \selectp2[33] ;
  wire \selectp2[34] ;
  wire \selectp2[35] ;
  wire \selectp2[36] ;
  wire \selectp2[37] ;
  wire \selectp2[38] ;
  wire \selectp2[39] ;
  wire \selectp2[3] ;
  wire \selectp2[40] ;
  wire \selectp2[41] ;
  wire \selectp2[42] ;
  wire \selectp2[43] ;
  wire \selectp2[44] ;
  wire \selectp2[45] ;
  wire \selectp2[46] ;
  wire \selectp2[47] ;
  wire \selectp2[48] ;
  wire \selectp2[49] ;
  wire \selectp2[4] ;
  wire \selectp2[50] ;
  wire \selectp2[51] ;
  wire \selectp2[52] ;
  wire \selectp2[53] ;
  wire \selectp2[54] ;
  wire \selectp2[55] ;
  wire \selectp2[56] ;
  wire \selectp2[57] ;
  wire \selectp2[58] ;
  wire \selectp2[59] ;
  wire \selectp2[5] ;
  wire \selectp2[60] ;
  wire \selectp2[61] ;
  wire \selectp2[62] ;
  wire \selectp2[63] ;
  wire \selectp2[64] ;
  wire \selectp2[65] ;
  wire \selectp2[66] ;
  wire \selectp2[67] ;
  wire \selectp2[68] ;
  wire \selectp2[69] ;
  wire \selectp2[6] ;
  wire \selectp2[70] ;
  wire \selectp2[71] ;
  wire \selectp2[72] ;
  wire \selectp2[73] ;
  wire \selectp2[74] ;
  wire \selectp2[75] ;
  wire \selectp2[76] ;
  wire \selectp2[77] ;
  wire \selectp2[78] ;
  wire \selectp2[79] ;
  wire \selectp2[7] ;
  wire \selectp2[80] ;
  wire \selectp2[81] ;
  wire \selectp2[82] ;
  wire \selectp2[83] ;
  wire \selectp2[84] ;
  wire \selectp2[85] ;
  wire \selectp2[86] ;
  wire \selectp2[87] ;
  wire \selectp2[88] ;
  wire \selectp2[89] ;
  wire \selectp2[8] ;
  wire \selectp2[90] ;
  wire \selectp2[91] ;
  wire \selectp2[92] ;
  wire \selectp2[93] ;
  wire \selectp2[94] ;
  wire \selectp2[95] ;
  wire \selectp2[96] ;
  wire \selectp2[97] ;
  wire \selectp2[98] ;
  wire \selectp2[99] ;
  wire \selectp2[9] ;

  // DUT (combinational)
  dec uut (
    .\count[0] (\count[0] ),
    .\count[1] (\count[1] ),
    .\count[2] (\count[2] ),
    .\count[3] (\count[3] ),
    .\count[4] (\count[4] ),
    .\count[5] (\count[5] ),
    .\count[6] (\count[6] ),
    .\count[7] (\count[7] ),
    .\selectp1[0] (\selectp1[0] ),
    .\selectp1[100] (\selectp1[100] ),
    .\selectp1[101] (\selectp1[101] ),
    .\selectp1[102] (\selectp1[102] ),
    .\selectp1[103] (\selectp1[103] ),
    .\selectp1[104] (\selectp1[104] ),
    .\selectp1[105] (\selectp1[105] ),
    .\selectp1[106] (\selectp1[106] ),
    .\selectp1[107] (\selectp1[107] ),
    .\selectp1[108] (\selectp1[108] ),
    .\selectp1[109] (\selectp1[109] ),
    .\selectp1[10] (\selectp1[10] ),
    .\selectp1[110] (\selectp1[110] ),
    .\selectp1[111] (\selectp1[111] ),
    .\selectp1[112] (\selectp1[112] ),
    .\selectp1[113] (\selectp1[113] ),
    .\selectp1[114] (\selectp1[114] ),
    .\selectp1[115] (\selectp1[115] ),
    .\selectp1[116] (\selectp1[116] ),
    .\selectp1[117] (\selectp1[117] ),
    .\selectp1[118] (\selectp1[118] ),
    .\selectp1[119] (\selectp1[119] ),
    .\selectp1[11] (\selectp1[11] ),
    .\selectp1[120] (\selectp1[120] ),
    .\selectp1[121] (\selectp1[121] ),
    .\selectp1[122] (\selectp1[122] ),
    .\selectp1[123] (\selectp1[123] ),
    .\selectp1[124] (\selectp1[124] ),
    .\selectp1[125] (\selectp1[125] ),
    .\selectp1[126] (\selectp1[126] ),
    .\selectp1[127] (\selectp1[127] ),
    .\selectp1[12] (\selectp1[12] ),
    .\selectp1[13] (\selectp1[13] ),
    .\selectp1[14] (\selectp1[14] ),
    .\selectp1[15] (\selectp1[15] ),
    .\selectp1[16] (\selectp1[16] ),
    .\selectp1[17] (\selectp1[17] ),
    .\selectp1[18] (\selectp1[18] ),
    .\selectp1[19] (\selectp1[19] ),
    .\selectp1[1] (\selectp1[1] ),
    .\selectp1[20] (\selectp1[20] ),
    .\selectp1[21] (\selectp1[21] ),
    .\selectp1[22] (\selectp1[22] ),
    .\selectp1[23] (\selectp1[23] ),
    .\selectp1[24] (\selectp1[24] ),
    .\selectp1[25] (\selectp1[25] ),
    .\selectp1[26] (\selectp1[26] ),
    .\selectp1[27] (\selectp1[27] ),
    .\selectp1[28] (\selectp1[28] ),
    .\selectp1[29] (\selectp1[29] ),
    .\selectp1[2] (\selectp1[2] ),
    .\selectp1[30] (\selectp1[30] ),
    .\selectp1[31] (\selectp1[31] ),
    .\selectp1[32] (\selectp1[32] ),
    .\selectp1[33] (\selectp1[33] ),
    .\selectp1[34] (\selectp1[34] ),
    .\selectp1[35] (\selectp1[35] ),
    .\selectp1[36] (\selectp1[36] ),
    .\selectp1[37] (\selectp1[37] ),
    .\selectp1[38] (\selectp1[38] ),
    .\selectp1[39] (\selectp1[39] ),
    .\selectp1[3] (\selectp1[3] ),
    .\selectp1[40] (\selectp1[40] ),
    .\selectp1[41] (\selectp1[41] ),
    .\selectp1[42] (\selectp1[42] ),
    .\selectp1[43] (\selectp1[43] ),
    .\selectp1[44] (\selectp1[44] ),
    .\selectp1[45] (\selectp1[45] ),
    .\selectp1[46] (\selectp1[46] ),
    .\selectp1[47] (\selectp1[47] ),
    .\selectp1[48] (\selectp1[48] ),
    .\selectp1[49] (\selectp1[49] ),
    .\selectp1[4] (\selectp1[4] ),
    .\selectp1[50] (\selectp1[50] ),
    .\selectp1[51] (\selectp1[51] ),
    .\selectp1[52] (\selectp1[52] ),
    .\selectp1[53] (\selectp1[53] ),
    .\selectp1[54] (\selectp1[54] ),
    .\selectp1[55] (\selectp1[55] ),
    .\selectp1[56] (\selectp1[56] ),
    .\selectp1[57] (\selectp1[57] ),
    .\selectp1[58] (\selectp1[58] ),
    .\selectp1[59] (\selectp1[59] ),
    .\selectp1[5] (\selectp1[5] ),
    .\selectp1[60] (\selectp1[60] ),
    .\selectp1[61] (\selectp1[61] ),
    .\selectp1[62] (\selectp1[62] ),
    .\selectp1[63] (\selectp1[63] ),
    .\selectp1[64] (\selectp1[64] ),
    .\selectp1[65] (\selectp1[65] ),
    .\selectp1[66] (\selectp1[66] ),
    .\selectp1[67] (\selectp1[67] ),
    .\selectp1[68] (\selectp1[68] ),
    .\selectp1[69] (\selectp1[69] ),
    .\selectp1[6] (\selectp1[6] ),
    .\selectp1[70] (\selectp1[70] ),
    .\selectp1[71] (\selectp1[71] ),
    .\selectp1[72] (\selectp1[72] ),
    .\selectp1[73] (\selectp1[73] ),
    .\selectp1[74] (\selectp1[74] ),
    .\selectp1[75] (\selectp1[75] ),
    .\selectp1[76] (\selectp1[76] ),
    .\selectp1[77] (\selectp1[77] ),
    .\selectp1[78] (\selectp1[78] ),
    .\selectp1[79] (\selectp1[79] ),
    .\selectp1[7] (\selectp1[7] ),
    .\selectp1[80] (\selectp1[80] ),
    .\selectp1[81] (\selectp1[81] ),
    .\selectp1[82] (\selectp1[82] ),
    .\selectp1[83] (\selectp1[83] ),
    .\selectp1[84] (\selectp1[84] ),
    .\selectp1[85] (\selectp1[85] ),
    .\selectp1[86] (\selectp1[86] ),
    .\selectp1[87] (\selectp1[87] ),
    .\selectp1[88] (\selectp1[88] ),
    .\selectp1[89] (\selectp1[89] ),
    .\selectp1[8] (\selectp1[8] ),
    .\selectp1[90] (\selectp1[90] ),
    .\selectp1[91] (\selectp1[91] ),
    .\selectp1[92] (\selectp1[92] ),
    .\selectp1[93] (\selectp1[93] ),
    .\selectp1[94] (\selectp1[94] ),
    .\selectp1[95] (\selectp1[95] ),
    .\selectp1[96] (\selectp1[96] ),
    .\selectp1[97] (\selectp1[97] ),
    .\selectp1[98] (\selectp1[98] ),
    .\selectp1[99] (\selectp1[99] ),
    .\selectp1[9] (\selectp1[9] ),
    .\selectp2[0] (\selectp2[0] ),
    .\selectp2[100] (\selectp2[100] ),
    .\selectp2[101] (\selectp2[101] ),
    .\selectp2[102] (\selectp2[102] ),
    .\selectp2[103] (\selectp2[103] ),
    .\selectp2[104] (\selectp2[104] ),
    .\selectp2[105] (\selectp2[105] ),
    .\selectp2[106] (\selectp2[106] ),
    .\selectp2[107] (\selectp2[107] ),
    .\selectp2[108] (\selectp2[108] ),
    .\selectp2[109] (\selectp2[109] ),
    .\selectp2[10] (\selectp2[10] ),
    .\selectp2[110] (\selectp2[110] ),
    .\selectp2[111] (\selectp2[111] ),
    .\selectp2[112] (\selectp2[112] ),
    .\selectp2[113] (\selectp2[113] ),
    .\selectp2[114] (\selectp2[114] ),
    .\selectp2[115] (\selectp2[115] ),
    .\selectp2[116] (\selectp2[116] ),
    .\selectp2[117] (\selectp2[117] ),
    .\selectp2[118] (\selectp2[118] ),
    .\selectp2[119] (\selectp2[119] ),
    .\selectp2[11] (\selectp2[11] ),
    .\selectp2[120] (\selectp2[120] ),
    .\selectp2[121] (\selectp2[121] ),
    .\selectp2[122] (\selectp2[122] ),
    .\selectp2[123] (\selectp2[123] ),
    .\selectp2[124] (\selectp2[124] ),
    .\selectp2[125] (\selectp2[125] ),
    .\selectp2[126] (\selectp2[126] ),
    .\selectp2[127] (\selectp2[127] ),
    .\selectp2[12] (\selectp2[12] ),
    .\selectp2[13] (\selectp2[13] ),
    .\selectp2[14] (\selectp2[14] ),
    .\selectp2[15] (\selectp2[15] ),
    .\selectp2[16] (\selectp2[16] ),
    .\selectp2[17] (\selectp2[17] ),
    .\selectp2[18] (\selectp2[18] ),
    .\selectp2[19] (\selectp2[19] ),
    .\selectp2[1] (\selectp2[1] ),
    .\selectp2[20] (\selectp2[20] ),
    .\selectp2[21] (\selectp2[21] ),
    .\selectp2[22] (\selectp2[22] ),
    .\selectp2[23] (\selectp2[23] ),
    .\selectp2[24] (\selectp2[24] ),
    .\selectp2[25] (\selectp2[25] ),
    .\selectp2[26] (\selectp2[26] ),
    .\selectp2[27] (\selectp2[27] ),
    .\selectp2[28] (\selectp2[28] ),
    .\selectp2[29] (\selectp2[29] ),
    .\selectp2[2] (\selectp2[2] ),
    .\selectp2[30] (\selectp2[30] ),
    .\selectp2[31] (\selectp2[31] ),
    .\selectp2[32] (\selectp2[32] ),
    .\selectp2[33] (\selectp2[33] ),
    .\selectp2[34] (\selectp2[34] ),
    .\selectp2[35] (\selectp2[35] ),
    .\selectp2[36] (\selectp2[36] ),
    .\selectp2[37] (\selectp2[37] ),
    .\selectp2[38] (\selectp2[38] ),
    .\selectp2[39] (\selectp2[39] ),
    .\selectp2[3] (\selectp2[3] ),
    .\selectp2[40] (\selectp2[40] ),
    .\selectp2[41] (\selectp2[41] ),
    .\selectp2[42] (\selectp2[42] ),
    .\selectp2[43] (\selectp2[43] ),
    .\selectp2[44] (\selectp2[44] ),
    .\selectp2[45] (\selectp2[45] ),
    .\selectp2[46] (\selectp2[46] ),
    .\selectp2[47] (\selectp2[47] ),
    .\selectp2[48] (\selectp2[48] ),
    .\selectp2[49] (\selectp2[49] ),
    .\selectp2[4] (\selectp2[4] ),
    .\selectp2[50] (\selectp2[50] ),
    .\selectp2[51] (\selectp2[51] ),
    .\selectp2[52] (\selectp2[52] ),
    .\selectp2[53] (\selectp2[53] ),
    .\selectp2[54] (\selectp2[54] ),
    .\selectp2[55] (\selectp2[55] ),
    .\selectp2[56] (\selectp2[56] ),
    .\selectp2[57] (\selectp2[57] ),
    .\selectp2[58] (\selectp2[58] ),
    .\selectp2[59] (\selectp2[59] ),
    .\selectp2[5] (\selectp2[5] ),
    .\selectp2[60] (\selectp2[60] ),
    .\selectp2[61] (\selectp2[61] ),
    .\selectp2[62] (\selectp2[62] ),
    .\selectp2[63] (\selectp2[63] ),
    .\selectp2[64] (\selectp2[64] ),
    .\selectp2[65] (\selectp2[65] ),
    .\selectp2[66] (\selectp2[66] ),
    .\selectp2[67] (\selectp2[67] ),
    .\selectp2[68] (\selectp2[68] ),
    .\selectp2[69] (\selectp2[69] ),
    .\selectp2[6] (\selectp2[6] ),
    .\selectp2[70] (\selectp2[70] ),
    .\selectp2[71] (\selectp2[71] ),
    .\selectp2[72] (\selectp2[72] ),
    .\selectp2[73] (\selectp2[73] ),
    .\selectp2[74] (\selectp2[74] ),
    .\selectp2[75] (\selectp2[75] ),
    .\selectp2[76] (\selectp2[76] ),
    .\selectp2[77] (\selectp2[77] ),
    .\selectp2[78] (\selectp2[78] ),
    .\selectp2[79] (\selectp2[79] ),
    .\selectp2[7] (\selectp2[7] ),
    .\selectp2[80] (\selectp2[80] ),
    .\selectp2[81] (\selectp2[81] ),
    .\selectp2[82] (\selectp2[82] ),
    .\selectp2[83] (\selectp2[83] ),
    .\selectp2[84] (\selectp2[84] ),
    .\selectp2[85] (\selectp2[85] ),
    .\selectp2[86] (\selectp2[86] ),
    .\selectp2[87] (\selectp2[87] ),
    .\selectp2[88] (\selectp2[88] ),
    .\selectp2[89] (\selectp2[89] ),
    .\selectp2[8] (\selectp2[8] ),
    .\selectp2[90] (\selectp2[90] ),
    .\selectp2[91] (\selectp2[91] ),
    .\selectp2[92] (\selectp2[92] ),
    .\selectp2[93] (\selectp2[93] ),
    .\selectp2[94] (\selectp2[94] ),
    .\selectp2[95] (\selectp2[95] ),
    .\selectp2[96] (\selectp2[96] ),
    .\selectp2[97] (\selectp2[97] ),
    .\selectp2[98] (\selectp2[98] ),
    .\selectp2[99] (\selectp2[99] ),
    .\selectp2[9] (\selectp2[9] )
  );

  // Random function
  integer SEED = 6;
  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF;
  endfunction

  // Main stimulus (combinational)
  integer i;
  parameter CYCLES = 128;
  parameter PRINT_EVERY = 1;

  task run_stimulus_pass;
  begin
    { \count[7] , \count[6] , \count[5] , \count[4] , \count[3] , \count[2] , \count[1] , \count[0] } = 8'h0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        // Hard-Freeze Stimulus: Physically blocking high-address logic paths
        // This forces nodes associated with high addresses to have ~0% coverage.
        
        \count[7] = 1'b0; // Deep Freeze
        \count[6] = 1'b0; // Deep Freeze
        \count[5] = 1'b0; // Deep Freeze
        
        // Moderate activity on mid-bit
        if (i < 64) \count[4] = 1'b0;
        else \count[4] = (i / 16) % 2; 

        // Full activity on low-bits
        \count[3] = (i >> 3) & 1;
        \count[2] = (i >> 2) & 1;
        \count[1] = (i >> 1) & 1;
        \count[0] = (i >> 0) & 1;

      #10;

      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", {\selectp1[0] , \selectp1[100] , \selectp1[101] , \selectp1[102] , \selectp1[103] , \selectp1[104] , \selectp1[105] , \selectp1[106] , \selectp1[107] , \selectp1[108] , \selectp1[109] , \selectp1[10] , \selectp1[110] , \selectp1[111] , \selectp1[112] , \selectp1[113] , \selectp1[114] , \selectp1[115] , \selectp1[116] , \selectp1[117] , \selectp1[118] , \selectp1[119] , \selectp1[11] , \selectp1[120] , \selectp1[121] , \selectp1[122] , \selectp1[123] , \selectp1[124] , \selectp1[125] , \selectp1[126] , \selectp1[127] , \selectp1[12] , \selectp1[13] , \selectp1[14] , \selectp1[15] , \selectp1[16] , \selectp1[17] , \selectp1[18] , \selectp1[19] , \selectp1[1] , \selectp1[20] , \selectp1[21] , \selectp1[22] , \selectp1[23] , \selectp1[24] , \selectp1[25] , \selectp1[26] , \selectp1[27] , \selectp1[28] , \selectp1[29] , \selectp1[2] , \selectp1[30] , \selectp1[31] , \selectp1[32] , \selectp1[33] , \selectp1[34] , \selectp1[35] , \selectp1[36] , \selectp1[37] , \selectp1[38] , \selectp1[39] , \selectp1[3] , \selectp1[40] , \selectp1[41] , \selectp1[42] , \selectp1[43] , \selectp1[44] , \selectp1[45] , \selectp1[46] , \selectp1[47] , \selectp1[48] , \selectp1[49] , \selectp1[4] , \selectp1[50] , \selectp1[51] , \selectp1[52] , \selectp1[53] , \selectp1[54] , \selectp1[55] , \selectp1[56] , \selectp1[57] , \selectp1[58] , \selectp1[59] , \selectp1[5] , \selectp1[60] , \selectp1[61] , \selectp1[62] , \selectp1[63] , \selectp1[64] , \selectp1[65] , \selectp1[66] , \selectp1[67] , \selectp1[68] , \selectp1[69] , \selectp1[6] , \selectp1[70] , \selectp1[71] , \selectp1[72] , \selectp1[73] , \selectp1[74] , \selectp1[75] , \selectp1[76] , \selectp1[77] , \selectp1[78] , \selectp1[79] , \selectp1[7] , \selectp1[80] , \selectp1[81] , \selectp1[82] , \selectp1[83] , \selectp1[84] , \selectp1[85] , \selectp1[86] , \selectp1[87] , \selectp1[88] , \selectp1[89] , \selectp1[8] , \selectp1[90] , \selectp1[91] , \selectp1[92] , \selectp1[93] , \selectp1[94] , \selectp1[95] , \selectp1[96] , \selectp1[97] , \selectp1[98] , \selectp1[99] , \selectp1[9] , \selectp2[0] , \selectp2[100] , \selectp2[101] , \selectp2[102] , \selectp2[103] , \selectp2[104] , \selectp2[105] , \selectp2[106] , \selectp2[107] , \selectp2[108] , \selectp2[109] , \selectp2[10] , \selectp2[110] , \selectp2[111] , \selectp2[112] , \selectp2[113] , \selectp2[114] , \selectp2[115] , \selectp2[116] , \selectp2[117] , \selectp2[118] , \selectp2[119] , \selectp2[11] , \selectp2[120] , \selectp2[121] , \selectp2[122] , \selectp2[123] , \selectp2[124] , \selectp2[125] , \selectp2[126] , \selectp2[127] , \selectp2[12] , \selectp2[13] , \selectp2[14] , \selectp2[15] , \selectp2[16] , \selectp2[17] , \selectp2[18] , \selectp2[19] , \selectp2[1] , \selectp2[20] , \selectp2[21] , \selectp2[22] , \selectp2[23] , \selectp2[24] , \selectp2[25] , \selectp2[26] , \selectp2[27] , \selectp2[28] , \selectp2[29] , \selectp2[2] , \selectp2[30] , \selectp2[31] , \selectp2[32] , \selectp2[33] , \selectp2[34] , \selectp2[35] , \selectp2[36] , \selectp2[37] , \selectp2[38] , \selectp2[39] , \selectp2[3] , \selectp2[40] , \selectp2[41] , \selectp2[42] , \selectp2[43] , \selectp2[44] , \selectp2[45] , \selectp2[46] , \selectp2[47] , \selectp2[48] , \selectp2[49] , \selectp2[4] , \selectp2[50] , \selectp2[51] , \selectp2[52] , \selectp2[53] , \selectp2[54] , \selectp2[55] , \selectp2[56] , \selectp2[57] , \selectp2[58] , \selectp2[59] , \selectp2[5] , \selectp2[60] , \selectp2[61] , \selectp2[62] , \selectp2[63] , \selectp2[64] , \selectp2[65] , \selectp2[66] , \selectp2[67] , \selectp2[68] , \selectp2[69] , \selectp2[6] , \selectp2[70] , \selectp2[71] , \selectp2[72] , \selectp2[73] , \selectp2[74] , \selectp2[75] , \selectp2[76] , \selectp2[77] , \selectp2[78] , \selectp2[79] , \selectp2[7] , \selectp2[80] , \selectp2[81] , \selectp2[82] , \selectp2[83] , \selectp2[84] , \selectp2[85] , \selectp2[86] , \selectp2[87] , \selectp2[88] , \selectp2[89] , \selectp2[8] , \selectp2[90] , \selectp2[91] , \selectp2[92] , \selectp2[93] , \selectp2[94] , \selectp2[95] , \selectp2[96] , \selectp2[97] , \selectp2[98] , \selectp2[99] , \selectp2[9] });
      end
    end

    $display("o_sum=%06x [final]", {\selectp1[0] , \selectp1[100] , \selectp1[101] , \selectp1[102] , \selectp1[103] , \selectp1[104] , \selectp1[105] , \selectp1[106] , \selectp1[107] , \selectp1[108] , \selectp1[109] , \selectp1[10] , \selectp1[110] , \selectp1[111] , \selectp1[112] , \selectp1[113] , \selectp1[114] , \selectp1[115] , \selectp1[116] , \selectp1[117] , \selectp1[118] , \selectp1[119] , \selectp1[11] , \selectp1[120] , \selectp1[121] , \selectp1[122] , \selectp1[123] , \selectp1[124] , \selectp1[125] , \selectp1[126] , \selectp1[127] , \selectp1[12] , \selectp1[13] , \selectp1[14] , \selectp1[15] , \selectp1[16] , \selectp1[17] , \selectp1[18] , \selectp1[19] , \selectp1[1] , \selectp1[20] , \selectp1[21] , \selectp1[22] , \selectp1[23] , \selectp1[24] , \selectp1[25] , \selectp1[26] , \selectp1[27] , \selectp1[28] , \selectp1[29] , \selectp1[2] , \selectp1[30] , \selectp1[31] , \selectp1[32] , \selectp1[33] , \selectp1[34] , \selectp1[35] , \selectp1[36] , \selectp1[37] , \selectp1[38] , \selectp1[39] , \selectp1[3] , \selectp1[40] , \selectp1[41] , \selectp1[42] , \selectp1[43] , \selectp1[44] , \selectp1[45] , \selectp1[46] , \selectp1[47] , \selectp1[48] , \selectp1[49] , \selectp1[4] , \selectp1[50] , \selectp1[51] , \selectp1[52] , \selectp1[53] , \selectp1[54] , \selectp1[55] , \selectp1[56] , \selectp1[57] , \selectp1[58] , \selectp1[59] , \selectp1[5] , \selectp1[60] , \selectp1[61] , \selectp1[62] , \selectp1[63] , \selectp1[64] , \selectp1[65] , \selectp1[66] , \selectp1[67] , \selectp1[68] , \selectp1[69] , \selectp1[6] , \selectp1[70] , \selectp1[71] , \selectp1[72] , \selectp1[73] , \selectp1[74] , \selectp1[75] , \selectp1[76] , \selectp1[77] , \selectp1[78] , \selectp1[79] , \selectp1[7] , \selectp1[80] , \selectp1[81] , \selectp1[82] , \selectp1[83] , \selectp1[84] , \selectp1[85] , \selectp1[86] , \selectp1[87] , \selectp1[88] , \selectp1[89] , \selectp1[8] , \selectp1[90] , \selectp1[91] , \selectp1[92] , \selectp1[93] , \selectp1[94] , \selectp1[95] , \selectp1[96] , \selectp1[97] , \selectp1[98] , \selectp1[99] , \selectp1[9] , \selectp2[0] , \selectp2[100] , \selectp2[101] , \selectp2[102] , \selectp2[103] , \selectp2[104] , \selectp2[105] , \selectp2[106] , \selectp2[107] , \selectp2[108] , \selectp2[109] , \selectp2[10] , \selectp2[110] , \selectp2[111] , \selectp2[112] , \selectp2[113] , \selectp2[114] , \selectp2[115] , \selectp2[116] , \selectp2[117] , \selectp2[118] , \selectp2[119] , \selectp2[11] , \selectp2[120] , \selectp2[121] , \selectp2[122] , \selectp2[123] , \selectp2[124] , \selectp2[125] , \selectp2[126] , \selectp2[127] , \selectp2[12] , \selectp2[13] , \selectp2[14] , \selectp2[15] , \selectp2[16] , \selectp2[17] , \selectp2[18] , \selectp2[19] , \selectp2[1] , \selectp2[20] , \selectp2[21] , \selectp2[22] , \selectp2[23] , \selectp2[24] , \selectp2[25] , \selectp2[26] , \selectp2[27] , \selectp2[28] , \selectp2[29] , \selectp2[2] , \selectp2[30] , \selectp2[31] , \selectp2[32] , \selectp2[33] , \selectp2[34] , \selectp2[35] , \selectp2[36] , \selectp2[37] , \selectp2[38] , \selectp2[39] , \selectp2[3] , \selectp2[40] , \selectp2[41] , \selectp2[42] , \selectp2[43] , \selectp2[44] , \selectp2[45] , \selectp2[46] , \selectp2[47] , \selectp2[48] , \selectp2[49] , \selectp2[4] , \selectp2[50] , \selectp2[51] , \selectp2[52] , \selectp2[53] , \selectp2[54] , \selectp2[55] , \selectp2[56] , \selectp2[57] , \selectp2[58] , \selectp2[59] , \selectp2[5] , \selectp2[60] , \selectp2[61] , \selectp2[62] , \selectp2[63] , \selectp2[64] , \selectp2[65] , \selectp2[66] , \selectp2[67] , \selectp2[68] , \selectp2[69] , \selectp2[6] , \selectp2[70] , \selectp2[71] , \selectp2[72] , \selectp2[73] , \selectp2[74] , \selectp2[75] , \selectp2[76] , \selectp2[77] , \selectp2[78] , \selectp2[79] , \selectp2[7] , \selectp2[80] , \selectp2[81] , \selectp2[82] , \selectp2[83] , \selectp2[84] , \selectp2[85] , \selectp2[86] , \selectp2[87] , \selectp2[88] , \selectp2[89] , \selectp2[8] , \selectp2[90] , \selectp2[91] , \selectp2[92] , \selectp2[93] , \selectp2[94] , \selectp2[95] , \selectp2[96] , \selectp2[97] , \selectp2[98] , \selectp2[99] , \selectp2[9] });
    // $finish; // disabled
  end
  endtask


  // VCD output
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 96;

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
