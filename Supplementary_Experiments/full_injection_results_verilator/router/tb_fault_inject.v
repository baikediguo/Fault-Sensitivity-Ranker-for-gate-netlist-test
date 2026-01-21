`timescale 1ns / 1ps

module tb;

  // Vector signals for logic and display
  reg [29:0] dest_x_vec;
  reg [29:0] dest_y_vec;
  wire [29:0] outport_vec;

  // DUT Instance - Connecting vectors to escaped identifiers
  top uut (
    .\dest_x[0] (dest_x_vec[0]),     .\dest_x[1] (dest_x_vec[1]),     .\dest_x[2] (dest_x_vec[2]),     .\dest_x[3] (dest_x_vec[3]),     .\dest_x[4] (dest_x_vec[4]),     .\dest_x[5] (dest_x_vec[5]), 
    .\dest_x[6] (dest_x_vec[6]),     .\dest_x[7] (dest_x_vec[7]),     .\dest_x[8] (dest_x_vec[8]),     .\dest_x[9] (dest_x_vec[9]),     .\dest_x[10] (dest_x_vec[10]),     .\dest_x[11] (dest_x_vec[11]), 
    .\dest_x[12] (dest_x_vec[12]),     .\dest_x[13] (dest_x_vec[13]),     .\dest_x[14] (dest_x_vec[14]),     .\dest_x[15] (dest_x_vec[15]),     .\dest_x[16] (dest_x_vec[16]),     .\dest_x[17] (dest_x_vec[17]), 
    .\dest_x[18] (dest_x_vec[18]),     .\dest_x[19] (dest_x_vec[19]),     .\dest_x[20] (dest_x_vec[20]),     .\dest_x[21] (dest_x_vec[21]),     .\dest_x[22] (dest_x_vec[22]),     .\dest_x[23] (dest_x_vec[23]), 
    .\dest_x[24] (dest_x_vec[24]),     .\dest_x[25] (dest_x_vec[25]),     .\dest_x[26] (dest_x_vec[26]),     .\dest_x[27] (dest_x_vec[27]),     .\dest_x[28] (dest_x_vec[28]),     .\dest_x[29] (dest_x_vec[29]), 
    .\dest_y[0] (dest_y_vec[0]),     .\dest_y[1] (dest_y_vec[1]),     .\dest_y[2] (dest_y_vec[2]),     .\dest_y[3] (dest_y_vec[3]),     .\dest_y[4] (dest_y_vec[4]),     .\dest_y[5] (dest_y_vec[5]), 
    .\dest_y[6] (dest_y_vec[6]),     .\dest_y[7] (dest_y_vec[7]),     .\dest_y[8] (dest_y_vec[8]),     .\dest_y[9] (dest_y_vec[9]),     .\dest_y[10] (dest_y_vec[10]),     .\dest_y[11] (dest_y_vec[11]), 
    .\dest_y[12] (dest_y_vec[12]),     .\dest_y[13] (dest_y_vec[13]),     .\dest_y[14] (dest_y_vec[14]),     .\dest_y[15] (dest_y_vec[15]),     .\dest_y[16] (dest_y_vec[16]),     .\dest_y[17] (dest_y_vec[17]), 
    .\dest_y[18] (dest_y_vec[18]),     .\dest_y[19] (dest_y_vec[19]),     .\dest_y[20] (dest_y_vec[20]),     .\dest_y[21] (dest_y_vec[21]),     .\dest_y[22] (dest_y_vec[22]),     .\dest_y[23] (dest_y_vec[23]), 
    .\dest_y[24] (dest_y_vec[24]),     .\dest_y[25] (dest_y_vec[25]),     .\dest_y[26] (dest_y_vec[26]),     .\dest_y[27] (dest_y_vec[27]),     .\dest_y[28] (dest_y_vec[28]),     .\dest_y[29] (dest_y_vec[29]), 
    .\outport[0] (outport_vec[0]),     .\outport[1] (outport_vec[1]),     .\outport[2] (outport_vec[2]),     .\outport[3] (outport_vec[3]),     .\outport[4] (outport_vec[4]),     .\outport[5] (outport_vec[5]), 
    .\outport[6] (outport_vec[6]),     .\outport[7] (outport_vec[7]),     .\outport[8] (outport_vec[8]),     .\outport[9] (outport_vec[9]),     .\outport[10] (outport_vec[10]),     .\outport[11] (outport_vec[11]), 
    .\outport[12] (outport_vec[12]),     .\outport[13] (outport_vec[13]),     .\outport[14] (outport_vec[14]),     .\outport[15] (outport_vec[15]),     .\outport[16] (outport_vec[16]),     .\outport[17] (outport_vec[17]), 
    .\outport[18] (outport_vec[18]),     .\outport[19] (outport_vec[19]),     .\outport[20] (outport_vec[20]),     .\outport[21] (outport_vec[21]),     .\outport[22] (outport_vec[22]),     .\outport[23] (outport_vec[23]), 
    .\outport[24] (outport_vec[24]),     .\outport[25] (outport_vec[25]),     .\outport[26] (outport_vec[26]),     .\outport[27] (outport_vec[27]),     .\outport[28] (outport_vec[28]),     .\outport[29] (outport_vec[29]) 
  );

  integer i, j;
  localparam STEPS = 1024;

  task run_stimulus_pass;
  begin
    dest_x_vec = 30'b0;
    dest_y_vec = 30'b0;
    #10;

    $display("=== Router GNN-Directed Test ==");
    $display("Strategy: High-bit intensive, Low-bit sparse");

    for (i = 0; i < STEPS; i = i + 1) begin

        // === HIGH PRIORITY: dest_x[20-29], dest_y[20-29] ===
        // High frequency toggling with diversity (every 2 steps)
        if ((i % 2) == 0) begin
            // dest_x high bits: diverse pattern based on i
            dest_x_vec[29] = ((i >> 1) ^ (i >> 3)) & 1;
            dest_x_vec[28] = ((i >> 2) ^ (i >> 4)) & 1;
            dest_x_vec[27] = ((i >> 3) ^ (i >> 5)) & 1;
            dest_x_vec[26] = ((i >> 4) ^ (i >> 1)) & 1;
            dest_x_vec[25] = ((i >> 5) ^ (i >> 2)) & 1;
            dest_x_vec[24] = ((i >> 6) ^ (i >> 3)) & 1;
            dest_x_vec[23] = ((i >> 1) ^ (i >> 5)) & 1;
            dest_x_vec[22] = ((i >> 2) ^ (i >> 6)) & 1;
            dest_x_vec[21] = ((i >> 3) ^ (i >> 7)) & 1;
            dest_x_vec[20] = ((i >> 4) ^ (i >> 8)) & 1;
            // dest_y high bits: complementary pattern
            dest_y_vec[29] = ~dest_x_vec[29];
            dest_y_vec[28] = ((i >> 3) ^ (i >> 6)) & 1;
            dest_y_vec[27] = ((i >> 4) ^ (i >> 7)) & 1;
            dest_y_vec[26] = ((i >> 5) ^ (i >> 8)) & 1;
            dest_y_vec[25] = ((i >> 6) ^ (i >> 1)) & 1;
            dest_y_vec[24] = ((i >> 7) ^ (i >> 2)) & 1;
            dest_y_vec[23] = ~dest_x_vec[23];
            dest_y_vec[22] = ((i >> 4) ^ (i >> 2)) & 1;
            dest_y_vec[21] = ((i >> 5) ^ (i >> 3)) & 1;
            dest_y_vec[20] = ((i >> 6) ^ (i >> 4)) & 1;
        end

        // === MEDIUM PRIORITY: dest_x[9-19], dest_y[9-19] ===
        // Medium frequency toggling (every 8 steps)
        if ((i % 8) == 0) begin
            dest_x_vec[19] = (i >> 3) & 1;
            dest_x_vec[18] = (i >> 4) & 1;
            dest_x_vec[17] = (i >> 5) & 1;
            dest_x_vec[16] = (i >> 6) & 1;
            dest_x_vec[15] = (i >> 7) & 1;
            dest_x_vec[14] = (i >> 8) & 1;
            dest_x_vec[13] = (i >> 3) & 1;
            dest_x_vec[12] = (i >> 4) & 1;
            dest_x_vec[11] = (i >> 5) & 1;
            dest_x_vec[10] = (i >> 6) & 1;
            dest_x_vec[9]  = (i >> 7) & 1;
            // dest_y medium bits: similar pattern
            dest_y_vec[19:9] = dest_x_vec[19:9] ^ 11'b10101010101;
        end

        // === LOW PRIORITY: dest_x[0-8], dest_y[0-8] ===
        // Very low frequency toggling (every 64 steps) - mostly static
        if ((i % 64) == 0) begin
            if (i < 256) begin
                // Phase 1: All zeros
                dest_x_vec[8:0] = 9'b0;
                dest_y_vec[8:0] = 9'b0;
            end else if (i < 512) begin
                // Phase 2: All ones
                dest_x_vec[8:0] = 9'h1FF;
                dest_y_vec[8:0] = 9'h1FF;
            end else if (i < 768) begin
                // Phase 3: Alternating
                dest_x_vec[8:0] = 9'b101010101;
                dest_y_vec[8:0] = 9'b010101010;
            end else begin
                // Phase 4: Complementary
                dest_x_vec[8:0] = (i >> 6) & 9'h1FF;
                dest_y_vec[8:0] = ~dest_x_vec[8:0];
            end
        end

        // === BOUNDARY TESTS: X vs Y comparison diversity ===
        // Every 16 steps, add specific comparison patterns
        if ((i % 16) == 8) begin
            // Force X > Y scenario
            dest_x_vec[29:24] = 6'b111111;
            dest_y_vec[29:24] = 6'b000000;
        end
        if ((i % 16) == 12) begin
            // Force X < Y scenario
            dest_x_vec[29:24] = 6'b000000;
            dest_y_vec[29:24] = 6'b111111;
        end

        #1;
        $display("o_sum=%02x", outport_vec[2:0]);
    end

    $display("o_sum=%02x [final]", outport_vec[2:0]);
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
    if (!$value$plusargs("BATCH_END=%d", __BATCH_END)) __BATCH_END = 508;

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
