`timescale 1ns / 1ps

module tb;

  reg \ctable[0] ;
  reg \ctable[1] ;
  reg \ctable[2] ;
  reg \totalcoeffs[0] ;
  reg \totalcoeffs[1] ;
  reg \totalcoeffs[2] ;
  reg \totalcoeffs[3] ;
  reg \totalcoeffs[4] ;
  reg \trailingones[0] ;
  reg \trailingones[1] ;
  wire \coeff_token[0] ;
  wire \coeff_token[1] ;
  wire \coeff_token[2] ;
  wire \coeff_token[3] ;
  wire \coeff_token[4] ;
  wire \coeff_token[5] ;
  wire \ctoken_len[0] ;
  wire \ctoken_len[1] ;
  wire \ctoken_len[2] ;
  wire \ctoken_len[3] ;
  wire \ctoken_len[4] ;

  // DUT (combinational)
  top uut (
    .\ctable[0] (\ctable[0] ),
    .\ctable[1] (\ctable[1] ),
    .\ctable[2] (\ctable[2] ),
    .\totalcoeffs[0] (\totalcoeffs[0] ),
    .\totalcoeffs[1] (\totalcoeffs[1] ),
    .\totalcoeffs[2] (\totalcoeffs[2] ),
    .\totalcoeffs[3] (\totalcoeffs[3] ),
    .\totalcoeffs[4] (\totalcoeffs[4] ),
    .\trailingones[0] (\trailingones[0] ),
    .\trailingones[1] (\trailingones[1] ),
    .\coeff_token[0] (\coeff_token[0] ),
    .\coeff_token[1] (\coeff_token[1] ),
    .\coeff_token[2] (\coeff_token[2] ),
    .\coeff_token[3] (\coeff_token[3] ),
    .\coeff_token[4] (\coeff_token[4] ),
    .\coeff_token[5] (\coeff_token[5] ),
    .\ctoken_len[0] (\ctoken_len[0] ),
    .\ctoken_len[1] (\ctoken_len[1] ),
    .\ctoken_len[2] (\ctoken_len[2] ),
    .\ctoken_len[3] (\ctoken_len[3] ),
    .\ctoken_len[4] (\ctoken_len[4] )
  );

  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF;
  endfunction

  integer i;
  parameter CYCLES = 512;
  parameter PRINT_EVERY = 1;

  task run_stimulus_pass;
  begin
    \ctable[0] = 0;
    \ctable[1] = 0;
    \ctable[2] = 0;
    \totalcoeffs[0] = 0;
    \totalcoeffs[1] = 0;
    \totalcoeffs[2] = 0;
    \totalcoeffs[3] = 0;
    \totalcoeffs[4] = 0;
    \trailingones[0] = 0;
    \trailingones[1] = 0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        // \ctable[0]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \ctable[0] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \ctable[0] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \ctable[0] = (i + 0) % 2;  // Phase3
          end
        end

        // \ctable[1]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \ctable[1] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \ctable[1] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \ctable[1] = (i + 1) % 2;  // Phase3
          end
        end

        // \ctable[2]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \ctable[2] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \ctable[2] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \ctable[2] = (i + 2) % 2;  // Phase3
          end
        end

        // \totalcoeffs[0]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \totalcoeffs[0] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \totalcoeffs[0] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \totalcoeffs[0] = (i + 3) % 2;  // Phase3
          end
        end

        // \totalcoeffs[1]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \totalcoeffs[1] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \totalcoeffs[1] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \totalcoeffs[1] = (i + 4) % 2;  // Phase3
          end
        end

        // \totalcoeffs[2]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \totalcoeffs[2] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \totalcoeffs[2] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \totalcoeffs[2] = (i + 5) % 2;  // Phase3
          end
        end

        // \totalcoeffs[3]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \totalcoeffs[3] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \totalcoeffs[3] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \totalcoeffs[3] = (i + 6) % 2;  // Phase3
          end
        end

        // \totalcoeffs[4]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \totalcoeffs[4] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \totalcoeffs[4] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \totalcoeffs[4] = (i + 7) % 2;  // Phase3
          end
        end

        // \trailingones[0]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \trailingones[0] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \trailingones[0] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \trailingones[0] = (i + 8) % 2;  // Phase3
          end
        end

        // \trailingones[1]: 1-bit Phase (0->1->Rnd)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            \trailingones[1] = 1'b0;  // Phase1 (SA1 check)
          end else if (i < 340) begin
            \trailingones[1] = 1'b1;  // Phase2 (SA0 check)
          end else begin
            \trailingones[1] = (i + 9) % 2;  // Phase3
          end
        end

      #10;

      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", {\coeff_token[0] , \coeff_token[1] , \coeff_token[2] , \coeff_token[3] , \coeff_token[4] , \coeff_token[5] , \ctoken_len[0] , \ctoken_len[1] , \ctoken_len[2] , \ctoken_len[3] , \ctoken_len[4] });
      end
    end

    $display("o_sum=%06x [final]", {\coeff_token[0] , \coeff_token[1] , \coeff_token[2] , \coeff_token[3] , \coeff_token[4] , \coeff_token[5] , \ctoken_len[0] , \ctoken_len[1] , \ctoken_len[2] , \ctoken_len[3] , \ctoken_len[4] });
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 1364;

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
