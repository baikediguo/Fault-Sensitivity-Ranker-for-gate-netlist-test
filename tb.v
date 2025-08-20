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

  integer i;
  initial begin
    reset = 1;
    i_weight = 0;
    i_activation = 0;
    i_sum = 0;
    #20;
    reset = 0;

    for (i = 0; i < 1024; i = i + 1) begin
      @(posedge clock);
      i_weight     = (i % 3 == 0) ? i[7:0] : $random % 256;
      i_activation = (i % 3 == 1) ? ~i[7:0] : $random % 256;
      i_sum        = (i % 4 == 0) ? 24'h000000 :
                     (i % 4 == 1) ? 24'hFFFFFF :
                     (i % 4 == 2) ? $random :
                                   {i[7:0], i[7:0], i[7:0]};
      $display("o_sum=%06x", o_sum); // ✅ 每拍都输出，便于排查
    end

    repeat (10) @(posedge clock);
    $display("o_sum=%06x [final]", o_sum); // ✅ 仿真结束前再输出一次
    $finish;
  end

  // VCD波形输出
  reg [1023:0] dumpfile_name;
  initial begin
    if (!$value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
      $display("❌ Error: No +DUMPFILE argument provided");
      $finish;
    end
    $display("✅ Dumping VCD to: %s", dumpfile_name);
    $dumpfile(dumpfile_name);
    $dumpvars(0, tb);
  end

  // 注入检测日志
  initial begin
    #1;
    $display("FAULT_INJECTED: check_if_force_took_effect");
  end

endmodule
