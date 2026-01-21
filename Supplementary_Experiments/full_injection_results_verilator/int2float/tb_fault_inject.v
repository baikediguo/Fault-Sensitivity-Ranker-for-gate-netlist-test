`timescale 1ns / 1ps

module tb;

  reg \B[0] ;
  reg \B[10] ;
  reg \B[1] ;
  reg \B[2] ;
  reg \B[3] ;
  reg \B[4] ;
  reg \B[5] ;
  reg \B[6] ;
  reg \B[7] ;
  reg \B[8] ;
  reg \B[9] ;
  wire \E[0] ;
  wire \E[1] ;
  wire \E[2] ;
  wire \M[0] ;
  wire \M[1] ;
  wire \M[2] ;
  wire \M[3] ;

  // DUT (combinational)
  top uut (
    .\B[0] (\B[0] ),
    .\B[10] (\B[10] ),
    .\B[1] (\B[1] ),
    .\B[2] (\B[2] ),
    .\B[3] (\B[3] ),
    .\B[4] (\B[4] ),
    .\B[5] (\B[5] ),
    .\B[6] (\B[6] ),
    .\B[7] (\B[7] ),
    .\B[8] (\B[8] ),
    .\B[9] (\B[9] ),
    .\E[0] (\E[0] ),
    .\E[1] (\E[1] ),
    .\E[2] (\E[2] ),
    .\M[0] (\M[0] ),
    .\M[1] (\M[1] ),
    .\M[2] (\M[2] ),
    .\M[3] (\M[3] )
  );

  // Random function
  integer SEED = 6;
  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF;
  endfunction

  // Main stimulus (combinational)
  integer i;
  parameter CYCLES = 512;
  parameter PRINT_EVERY = 1;

  task run_stimulus_pass;
  begin
    \B[0] = 0;
    \B[10] = 0;
    \B[1] = 0;
    \B[2] = 0;
    \B[3] = 0;
    \B[4] = 0;
    \B[5] = 0;
    \B[6] = 0;
    \B[7] = 0;
    \B[8] = 0;
    \B[9] = 0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        // \B[0]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[0] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[0] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[0] = (i + 0) % 2;  // Phase3: 翻转
          end
        end

        // \B[10]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[10] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[10] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[10] = (i + 1) % 2;  // Phase3: 翻转
          end
        end

        // \B[1]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[1] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[1] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[1] = (i + 2) % 2;  // Phase3: 翻转
          end
        end

        // \B[2]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[2] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[2] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[2] = (i + 3) % 2;  // Phase3: 翻转
          end
        end

        // \B[3]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[3] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[3] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[3] = (i + 4) % 2;  // Phase3: 翻转
          end
        end

        // \B[4]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[4] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[4] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[4] = (i + 5) % 2;  // Phase3: 翻转
          end
        end

        // \B[5]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[5] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[5] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[5] = (i + 6) % 2;  // Phase3: 翻转
          end
        end

        // \B[6]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[6] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[6] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[6] = (i + 7) % 2;  // Phase3: 翻转
          end
        end

        // \B[7]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[7] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[7] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[7] = (i + 8) % 2;  // Phase3: 翻转
          end
        end

        // \B[8]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[8] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[8] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[8] = (i + 9) % 2;  // Phase3: 翻转
          end
        end

        // \B[9]: 1-bit 三阶段 (稀疏更新)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \B[9] = 1'b0;  // Phase1: 全0 (检测SA1)
          end else if (i < 340) begin
            \B[9] = 1'b1;  // Phase2: 全1 (检测SA0)
          end else begin
            \B[9] = (i + 10) % 2;  // Phase3: 翻转
          end
        end

      #10;

      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", {\E[0] , \E[1] , \E[2] , \M[0] , \M[1] , \M[2] , \M[3] });
      end
    end

    $display("o_sum=%06x [final]", {\E[0] , \E[1] , \E[2] , \M[0] , \M[1] , \M[2] , \M[3] });
    // $finish; // disabled
  end
  endtask


  // VCD output
  reg [510:0] dumpfile_name;
  initial begin
    if (!$value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
      $display("Error: No +DUMPFILE argument");
      // $finish; // disabled
    end
    $display("Dumping VCD to: %s", dumpfile_name);
    $dumpfile(dumpfile_name);
    $dumpvars(0, tb);
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 506;

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
