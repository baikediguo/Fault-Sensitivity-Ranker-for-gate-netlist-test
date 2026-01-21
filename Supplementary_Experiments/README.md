# Supplementary Experiments

This folder contains the supplementary experimental data and code for the GNN-based fault sensitivity ranking project.

## Environment

| Component | Version |
|-----------|---------|
| **GPU** | NVIDIA GeForce RTX 5060 Laptop GPU |
| **Driver Version** | 577.03 |
| **CUDA Version** | 12.9 |
| **Python** | 3.11.9 |
| **Simulator** | Verilator |


## Benchmarks

The gate-level netlists used in this project are from the **EPFL Combinational Benchmark Suite**, which provides a set of arithmetic and random/control circuits for logic synthesis and testing.

### Circuits Included

| Circuit | Description |
|---------|-------------|
| adder | Arithmetic adder |
| arbiter | Bus arbiter |
| bar | Barrel shifter |
| cavlc | CAVLC encoder |
| ctrl | Controller |
| dec | Decoder |
| div | Divider |
| hyp | Hypotenuse calculator |
| i2c | I2C controller |
| int2float | Integer to float converter |
| log2 | Logarithm base 2 |
| max | Maximum finder |
| mem_ctrl | Memory controller |
| multiplier | Multiplier |
| priority | Priority encoder |
| router | Router |
| sin | Sine function |
| sqrt | Square root |
| square | Square function |
| voter | Voter circuit |

## Folder Structure

```
Supplementary_Experiments/
├── full_injection_results_verilator/   # Fault injection simulation results
│   └── <circuit_name>/
│       ├── cumulative_coverage_v1.csv  # Coverage data
│       ├── full_injection_results.json # Detailed injection results
│       ├── golden_result.json          # Golden (fault-free) results
│       ├── <circuit>_fi.v              # Fault-injected netlist
│       └── tb_fault_inject.v           # Testbench
├── gnn_ranks/                          # GNN ranking results
│   └── gnn_rank_<circuit>_v1.txt       # Node sensitivity rankings
├── netlists/                           # Original gate-level netlists
│   ├── <circuit>.v                     # Circuit netlist
│   └── tb_<circuit>.v                  # Testbench
├── feature_cache/                      # Cached feature data
└── full_node_injection_verilator_parallel.py  # Injection script
```

## Usage

### Running Fault Injection Simulation

```bash
python full_node_injection_verilator_parallel.py
```

## Citation

If you use these benchmarks, please cite the original paper:

> L. Amarú, P.-E. Gaillardon, G. De Micheli, "The EPFL Combinational Benchmark Suite", Proc. IWLS, Mountain View, CA, June 2015.

Repository: [lsils/benchmarks](https://github.com/lsils/benchmarks)
