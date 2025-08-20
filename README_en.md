## Project Title: Fault-Sensitivity-Ranker-for-gate-netlist-test

[English](README_en.md) | [中文说明](README.md)

This is English readme...

## Objective
Uses AI (particularly graph neural networks) to predict or rank the likelihood of faults at each node in a Verilog circuit netlist without explicitly injecting faults.

## Motivation
1. Testing and simulation efficiency increased.
* The traditional approach involves evenly or fully injecting into a large number of nodes, with costs increasing exponentially with scale.
* Fewer VVP/ATE vectors, reducing the total time for the Iverilog compile-run-compare loop.

2. Faster convergence, fewer regressions
* Focus on high-risk nodes to detect 'fatal fault paths' earlier, thereby shortening the design-validation-repair closed-loop cycle.

3. DFT/ATPG/redundancy optimization of 'amplifier'

* High-sensitivity nodes are often located at high fan-out, strong convergence, or near timing boundary positions, significantly affecting test observability and controllability.。
* The ranking results can directly provide quantitative basis for ATPG targetization, insertion of observation/control points, and selective TMR/ECC/parity hardening.（Triple Modular Redundancy/Error-Correcting Code/Parity Check）

4. Reliability and manufacturability（Yield/Reliability）improve

* For scenarios involving soft errors (SEUs)/aging/process corner variations, prioritizing reinforcement and monitoring of high-sensitivity nodes can suppress the propagation of system-level failures, enhancing stability and yield.
* In scenarios such as safety, automotive regulations, and aerospace, it helps meet specific fault coverage goals and compliance requirements.

5. Safety analysis (Fault Attack Surface) assistance

* In secure chips/encryption modules, sorting sensitive nodes helps identify high-value surfaces for fault injection attacks, providing a basis for offensive and defensive research as well as mitigation strategies.

6. Debugging and ECO guidance（Engineering Change Order）

* Sensitive nodes are often shortcuts for debugging: placing logs/probes at these points can improve diagnostic speed.

* The change in sensitivity before and after ECO can quantify risks, helping to evaluate the impact of modifications on testability/observability.

7. Save hardware/simulation resource costs

* In environments with limited computing power or licenses (such as CI, cloud simulation, shared farms), the Top-K strategy can convert the same budget into higher coverage benefits.

## Fault injection using Pyverilog in a single PE

[Pyverilog](https://github.com/PyHDI/Pyverilog) can parse the Verilog netlists into Abstract Syntax Trees (ASTs) and generate verilog code from ASTs. ASTs can be modified to inject faults.

Golden Simulation:
* Compile and run the gate-level model 
* Outputs golden simulation results in `sim_logs/sim_logs_manual`

Fault Injection:
* Model: single stuck-at fault
* `gatesa_fault_injection.py` traverses all gates (such as AND/OR/XOR...) and performs 'fault injection' on each gate—such as forcing the output to 0 (stuck-at-0) or 1 (stuck-at-1). Injects faults into all gate output ports, regardless of whether they are wires or registers, by inserting an assign statement to achieve 'generalized node-level' injection, ensuring no output nodes are skipped. This indirectly covers all Q-end registers and wire nodes.
* For each fault version, generate a modified Verilog file, call Icarus Verilog (iverilog) to run functional simulation, and extract the output.

Evaluation:
* `unsup_sensitivity.py` Predicting or ranking the likelihood of faults at each node in a Verilog circuit netlist without explicit fault injection.
* `manual_validation.py` Verify through fault injection simulation whether the sensitive nodes predicted by GNN are truly effective.

##  Environment Setup Notes
For a quick setup, you can use the following command to install all dependencies at once:

pip install -r requirements.txt

Alternatively, if you prefer to install the dependencies step-by-step, please follow the instructions below:
* [Pyverilog](https://github.com/PyHDI/Pyverilog): `pip install pyverilog`
* [iVerilog](https://steveicarus.github.io/iverilog/)
* On Windows: Use [mingw-w64](https://www.mingw-w64.org) or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
* Technology libraries need to be downloaded separately (Optional):
  * Synopsys Educational Design Kit (SAED90nm)
  * [Nangate Open Cell Library](https://github.com/JulianKemmerer/Drexel-ECEC575/tree/master/Encounter/NangateOpenCellLibrary)
 
 ## Below is a detailed guide for the experimental process, broken down into 5 steps to provide clear instructions： 
