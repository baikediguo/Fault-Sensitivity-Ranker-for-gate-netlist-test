`timescale 1ns / 1ps

module tb;

  reg \op_ext[0] ;
  reg \op_ext[1] ;
  reg \opcode[0] ;
  reg \opcode[1] ;
  reg \opcode[2] ;
  reg \opcode[3] ;
  reg \opcode[4] ;
  wire \alu_op[0] ;
  wire \alu_op[1] ;
  wire \alu_op[2] ;
  wire \alu_op_ext[0] ;
  wire \alu_op_ext[1] ;
  wire \alu_op_ext[2] ;
  wire \alu_op_ext[3] ;
  wire \sel_alu_opB[0] ;
  wire \sel_alu_opB[1] ;
  wire \sel_reg_dst[0] ;
  wire \sel_reg_dst[1] ;
  wire Cin;
  wire beqz;
  wire bgez;
  wire bltz;
  wire bnez;
  wire halt;
  wire invA;
  wire invB;
  wire jump;
  wire mem_write;
  wire reg_write;
  wire sel_pc_opA;
  wire sel_pc_opB;
  wire sel_wb;
  wire sign;

  // DUT (combinational)
  top uut (
    .\op_ext[0] (\op_ext[0] ),
    .\op_ext[1] (\op_ext[1] ),
    .\opcode[0] (\opcode[0] ),
    .\opcode[1] (\opcode[1] ),
    .\opcode[2] (\opcode[2] ),
    .\opcode[3] (\opcode[3] ),
    .\opcode[4] (\opcode[4] ),
    .\alu_op[0] (\alu_op[0] ),
    .\alu_op[1] (\alu_op[1] ),
    .\alu_op[2] (\alu_op[2] ),
    .\alu_op_ext[0] (\alu_op_ext[0] ),
    .\alu_op_ext[1] (\alu_op_ext[1] ),
    .\alu_op_ext[2] (\alu_op_ext[2] ),
    .\alu_op_ext[3] (\alu_op_ext[3] ),
    .\sel_alu_opB[0] (\sel_alu_opB[0] ),
    .\sel_alu_opB[1] (\sel_alu_opB[1] ),
    .\sel_reg_dst[0] (\sel_reg_dst[0] ),
    .\sel_reg_dst[1] (\sel_reg_dst[1] ),
    .Cin(Cin),
    .beqz(beqz),
    .bgez(bgez),
    .bltz(bltz),
    .bnez(bnez),
    .halt(halt),
    .invA(invA),
    .invB(invB),
    .jump(jump),
    .mem_write(mem_write),
    .reg_write(reg_write),
    .sel_pc_opA(sel_pc_opA),
    .sel_pc_opB(sel_pc_opB),
    .sel_wb(sel_wb),
    .sign(sign)
  );

  function [7:0] urand(input integer s);
    urand = $random(s) & 8'hFF;
  endfunction

  integer i;
  parameter CYCLES = 512;
  parameter PRINT_EVERY = 1;

  initial begin
    \op_ext[0] = 0;
    \op_ext[1] = 0;
    \opcode[0] = 0;
    \opcode[1] = 0;
    \opcode[2] = 0;
    \opcode[3] = 0;
    \opcode[4] = 0;

    #10;

    for (i = 0; i < CYCLES; i = i + 1) begin
        // Inputs Phase Logic (0 -> 1 -> Rotating Patterns)
        if ((i % 4) == 0) begin
          if (i < 170) begin
            // Phase 1: All Zero
            \op_ext[0] = 0; \op_ext[1] = 0;
            \opcode[0] = 0; \opcode[1] = 0; \opcode[2] = 0; \opcode[3] = 0; \opcode[4] = 0;
          end else if (i < 340) begin
            // Phase 2: All One
            \op_ext[0] = 1; \op_ext[1] = 1;
            \opcode[0] = 1; \opcode[1] = 1; \opcode[2] = 1; \opcode[3] = 1; \opcode[4] = 1;
          end else begin
            // Phase 3: Single fixed pattern (only 3 total unique vectors like original)
            // This is deliberately a SINGLE pattern to avoid saturating coverage
            \op_ext[0] = 1; \op_ext[1] = 0;
            \opcode[0] = 1; \opcode[1] = 0; \opcode[2] = 1; \opcode[3] = 0; \opcode[4] = 1;
          end
        end

      #10;

      if ((i % PRINT_EVERY) == 0) begin
        $display("o_sum=%06x", {\alu_op[0] , \alu_op[1] , \alu_op[2] , \alu_op_ext[0] , \alu_op_ext[1] , \alu_op_ext[2] , \alu_op_ext[3] , \sel_alu_opB[0] , \sel_alu_opB[1] , \sel_reg_dst[0] , \sel_reg_dst[1] , Cin, beqz, bgez, bltz, bnez, halt, invA, invB, jump, mem_write, reg_write, sel_pc_opA, sel_pc_opB, sel_wb, sign});
      end
    end

    $display("o_sum=%06x [final]", {\alu_op[0] , \alu_op[1] , \alu_op[2] , \alu_op_ext[0] , \alu_op_ext[1] , \alu_op_ext[2] , \alu_op_ext[3] , \sel_alu_opB[0] , \sel_alu_opB[1] , \sel_reg_dst[0] , \sel_reg_dst[1] , Cin, beqz, bgez, bltz, bnez, halt, invA, invB, jump, mem_write, reg_write, sel_pc_opA, sel_pc_opB, sel_wb, sign});
    $finish;
  end

  // VCD output - commented out for Verilator (use --trace instead)
  // reg [510:0] dumpfile_name;
  // initial begin
  //   if (!$value$plusargs("DUMPFILE=%s", dumpfile_name)) begin
  //   end else begin
  //     $dumpfile(dumpfile_name);
  //   end
  //   $dumpvars(0, tb);
  // end

endmodule
