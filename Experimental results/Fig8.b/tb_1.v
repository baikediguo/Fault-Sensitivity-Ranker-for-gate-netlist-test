`timescale 1ns / 1ps

module tb;

  reg clock;
  reg reset;
  reg [7:0] i_weight;
  reg [7:0] i_activation;
  reg [23:0] i_sum;
  wire [23:0] o_sum;

  // DUT
  pe uut (
    .clock(clock),
    .reset(reset),
    .i_weight(i_weight),
    .i_activation(i_activation),
    .i_sum(i_sum),
    .o_sum(o_sum)
  );

  // Clock
  initial begin
    clock = 0;
    forever #5 clock = ~clock;
  end

  // ==============================
  // 自定义可复现随机函数
  // ==============================
  integer SEED = 6; // 随机种子
  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF; // 8位随机数
  endfunction

  // ==============================
  // 主激励逻辑
  // ==============================
  integer i;
  parameter CYCLES = 255;
  parameter UPDATE_EVERY = 8                                                                                                                                                                                                                                                      ;  // 每多少周期更新一次输入
  parameter PRINT_EVERY  = 1;  // 每多少周期打印一次输出

  initial begin
    reset = 1;
    i_weight = 0;
    i_activation = 0;
    i_sum = 0;

    #20;
    reset = 0;

    for (i = 0; i < CYCLES; i = i + 1) begin
      @(posedge clock);

      if ((i % UPDATE_EVERY) == 0) begin
        // i_weight：大部分小范围随机，偶尔用计数
        if ((i % 8) == 0) begin
          i_weight = i[7:0];
        end else begin
          i_weight = urand(SEED + i) % 4; // 0~31
        end

        // i_activation：大部分小范围随机，偶尔取 ~i
        if ((i % 12) == 1) begin
          i_activation = ~i[7:0];
        end else begin
          i_activation = urand(SEED + i + 1) % 6; // 0~31
        end

        // i_sum：平稳模式为主，偶尔全0或全1
        if ((i % 128) == 0) begin
          i_sum = 24'h000000;  // 罕见全零
        end else if ((i % 256) == 0) begin
          i_sum = 24'hFFFFFF;  // 更罕见全一
        end else begin
          i_sum = {8'h00, i[7:0], i[7:0]}; // 稳定模式
        end
      end

      // 输出打印
      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", o_sum);
      end
    end

    // 结束前额外等待
    repeat (10) @(posedge clock);
    $display("o_sum=%06x [final]", o_sum);
    $finish;
  end

  // ==============================
  // VCD波形输出
  // ==============================
  reg [510:0] dumpfile_name;
  initial begin
    if (!$value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
      $display("❌ Error: No +DUMPFILE argument provided");
      $finish;
    end
    $display("✅ Dumping VCD to: %s", dumpfile_name);
    $dumpfile(dumpfile_name);
    $dumpvars(0, tb);
  end

  // ==============================
  // 注入检测日志
  // ==============================
  initial begin
    #1;
    $display("FAULT_INJECTED: check_if_force_took_effect");
  end

endmodule
