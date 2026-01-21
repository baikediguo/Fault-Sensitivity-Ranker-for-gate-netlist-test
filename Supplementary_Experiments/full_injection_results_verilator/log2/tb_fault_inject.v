`timescale 1ns / 1ps

module tb;

  reg \a[0] ;
  reg \a[10] ;
  reg \a[11] ;
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
  reg \a[3] ;
  reg \a[4] ;
  reg \a[5] ;
  reg \a[6] ;
  reg \a[7] ;
  reg \a[8] ;
  reg \a[9] ;
  wire \result[0] ;
  wire \result[10] ;
  wire \result[11] ;
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
  wire \result[3] ;
  wire \result[4] ;
  wire \result[5] ;
  wire \result[6] ;
  wire \result[7] ;
  wire \result[8] ;
  wire \result[9] ;

  // DUT (combinational)
  top uut (
    .\a[0] (\a[0] ),
    .\a[1] (\a[1] ),
    .\a[2] (\a[2] ),
    .\a[3] (\a[3] ),
    .\a[4] (\a[4] ),
    .\a[5] (\a[5] ),
    .\a[6] (\a[6] ),
    .\a[7] (\a[7] ),
    .\a[8] (\a[8] ),
    .\a[9] (\a[9] ),
    .\a[10] (\a[10] ),
    .\a[11] (\a[11] ),
    .\a[12] (\a[12] ),
    .\a[13] (\a[13] ),
    .\a[14] (\a[14] ),
    .\a[15] (\a[15] ),
    .\a[16] (\a[16] ),
    .\a[17] (\a[17] ),
    .\a[18] (\a[18] ),
    .\a[19] (\a[19] ),
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
    .\a[30] (\a[30] ),
    .\a[31] (\a[31] ),
    .\result[0] (\result[0] ),
    .\result[1] (\result[1] ),
    .\result[2] (\result[2] ),
    .\result[3] (\result[3] ),
    .\result[4] (\result[4] ),
    .\result[5] (\result[5] ),
    .\result[6] (\result[6] ),
    .\result[7] (\result[7] ),
    .\result[8] (\result[8] ),
    .\result[9] (\result[9] ),
    .\result[10] (\result[10] ),
    .\result[11] (\result[11] ),
    .\result[12] (\result[12] ),
    .\result[13] (\result[13] ),
    .\result[14] (\result[14] ),
    .\result[15] (\result[15] ),
    .\result[16] (\result[16] ),
    .\result[17] (\result[17] ),
    .\result[18] (\result[18] ),
    .\result[19] (\result[19] ),
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
    .\result[30] (\result[30] ),
    .\result[31] (\result[31] )
  );

  integer i;
  parameter CYCLES = 2;

  task run_stimulus_pass;
  begin
    \a[0]  = 1'b0;
    \a[1]  = 1'b0;
    \a[2]  = 1'b0;
    \a[3]  = 1'b0;
    \a[4]  = 1'b0;
    \a[5]  = 1'b0;
    \a[6]  = 1'b0;
    \a[7]  = 1'b0;
    \a[8]  = 1'b0;
    \a[9]  = 1'b0;
    \a[10]  = 1'b0;
    \a[11]  = 1'b0;
    \a[12]  = 1'b0;
    \a[13]  = 1'b0;
    \a[14]  = 1'b0;
    \a[15]  = 1'b0;
    \a[16]  = 1'b0;
    \a[17]  = 1'b0;
    \a[18]  = 1'b0;
    \a[19]  = 1'b0;
    \a[20]  = 1'b0;
    \a[21]  = 1'b0;
    \a[22]  = 1'b0;
    \a[23]  = 1'b0;
    \a[24]  = 1'b0;
    \a[25]  = 1'b0;
    \a[26]  = 1'b0;
    \a[27]  = 1'b0;
    \a[28]  = 1'b0;
    \a[29]  = 1'b0;
    \a[30]  = 1'b0;
    \a[31]  = 1'b0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        if (i == 0) begin \a[31]  = 1'b1; #10; $display("o_sum=%b", \result[31]  ); end
        else begin \a[31]  = 1'b0; #10; $display("o_sum=%b", \result[31]  ); end
    end

    $display("o_sum=%b [final]", \result[31]  );
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 64056;

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
