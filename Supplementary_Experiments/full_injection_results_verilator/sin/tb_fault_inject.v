`timescale 1ns / 1ps

module tb;

  // Vector signals for logic and display
  reg [23:0] a_vec;
  wire [24:0] sin_vec;

  // DUT Instance - Connecting vectors to escaped identifiers
  top uut (
    .\a[0] (a_vec[0]),     .\a[1] (a_vec[1]),     .\a[2] (a_vec[2]),     .\a[3] (a_vec[3]),     .\a[4] (a_vec[4]),     .\a[5] (a_vec[5]), 
    .\a[6] (a_vec[6]),     .\a[7] (a_vec[7]),     .\a[8] (a_vec[8]),     .\a[9] (a_vec[9]),     .\a[10] (a_vec[10]),     .\a[11] (a_vec[11]), 
    .\a[12] (a_vec[12]),     .\a[13] (a_vec[13]),     .\a[14] (a_vec[14]),     .\a[15] (a_vec[15]),     .\a[16] (a_vec[16]),     .\a[17] (a_vec[17]), 
    .\a[18] (a_vec[18]),     .\a[19] (a_vec[19]),     .\a[20] (a_vec[20]),     .\a[21] (a_vec[21]),     .\a[22] (a_vec[22]),     .\a[23] (a_vec[23]), 
    .\sin[0] (sin_vec[0]),     .\sin[1] (sin_vec[1]),     .\sin[2] (sin_vec[2]),     .\sin[3] (sin_vec[3]),     .\sin[4] (sin_vec[4]),     .\sin[5] (sin_vec[5]), 
    .\sin[6] (sin_vec[6]),     .\sin[7] (sin_vec[7]),     .\sin[8] (sin_vec[8]),     .\sin[9] (sin_vec[9]),     .\sin[10] (sin_vec[10]),     .\sin[11] (sin_vec[11]), 
    .\sin[12] (sin_vec[12]),     .\sin[13] (sin_vec[13]),     .\sin[14] (sin_vec[14]),     .\sin[15] (sin_vec[15]),     .\sin[16] (sin_vec[16]),     .\sin[17] (sin_vec[17]), 
    .\sin[18] (sin_vec[18]),     .\sin[19] (sin_vec[19]),     .\sin[20] (sin_vec[20]),     .\sin[21] (sin_vec[21]),     .\sin[22] (sin_vec[22]),     .\sin[23] (sin_vec[23]), 
    .\sin[24] (sin_vec[24])   );

  integer i;
  localparam STEPS = 128;

  task run_stimulus_pass;
  begin
    // 所有输入初始化为0
    a_vec = 24'b0;
    #10;

    $display("=== Sin Circuit INVERTED Priority V4 ===");
    $display("Strategy: a[0-7] every 2, a[8-15] every 8, a[16-23] every 64");

    for (i = 0; i < STEPS; i = i + 1) begin

        // === HIGH PRIORITY: a[0-7] - EVERY 2 STEPS (1 bit) ===
        if ((i % 2) == 0) begin
            a_vec[0] = i[1];
        end
        a_vec[1] = i[2];
        a_vec[2] = i[3];
        a_vec[3] = i[4];
        a_vec[4] = i[5];
        a_vec[5] = i[6];
        a_vec[6] = i[7];
        a_vec[7] = i[3] ^ i[4];

        // === MEDIUM PRIORITY: a[8-15] - EVERY 32 STEPS ===
        if ((i % 32) == 0) begin
            a_vec[8] = i[3];
            a_vec[9] = i[4];
            a_vec[10] = i[5];
            a_vec[11] = i[6];
            a_vec[12] = i[4] ^ i[2];
            a_vec[13] = i[5] ^ i[3];
            a_vec[14] = i[6] ^ i[4];
            a_vec[15] = i[7] ^ i[5];
        end

        // === LOW PRIORITY: a[16-23] - EVERY 64 STEPS ===
        if ((i % 64) == 0) begin
            a_vec[23:16] = i[7:0];
        end

        #1;
        $display("o_sum=%07x", sin_vec);
    end

    $display("o_sum=%07x [final]", sin_vec);
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 10782;

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
