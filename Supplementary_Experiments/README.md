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

### Folder Structure

```
Supplementary_Experiments/
├── full_injection_results_verilator/   # Fault injection simulation results
│   ├── summary_coverage_timing.csv     # ★ Summary of coverage and timing for all circuits
│   └── <circuit_name>/
│       ├── cumulative_coverage_v1.csv  # Coverage data: comparison between GNN and random selection
│       ├── full_injection_results.json # Detailed injection results
│       ├── golden_result.json          # Golden (fault-free) results
│       ├── <circuit>_fi.v              # Fault-injected netlist
│       └── tb_fault_inject.v           # Testbench
├── gnn_ranks/                          # GNN ranking results ✔️
│   └── gnn_rank_<circuit>_v1.txt       # Node sensitivity rankings (Text format)
├── netlists/                           # Original gate-level netlists
│   ├── <circuit>.v                     # Circuit netlist
│   └── tb_<circuit>.v                  # Testbench
├── feature_cache/                      # Cached feature data
└── full_node_injection_verilator_parallel.py  # Injection script
```

### Experiment Results

Below is the summary of fault injection results (`summary_coverage_timing.csv`), showing the performance of GNN-based ranking compared to random selection:

| Circuit | Nodes | GNN Time (s) | Injection Time (s) | Node Cov (10%) | Node Cov (20%) | Node Cov (Final) | Fault Cov (10%) | Fault Cov (20%) | Fault Cov (Final) | Gap 10% | Gap 20% |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **adder** | 2296 | 2.79 | 0.01 | 100.00 | 99.44 | 99.78 | 100.00 | 99.44 | 78.31 | +21.69 | +21.13 |
| **arbiter** | 23934 | 30.61 | 0.08 | 72.16 | 70.54 | 55.19 | 70.32 | 69.28 | 53.84 | +16.48 | +15.44 |
| **bar** | 6807 | 4.34 | 0.03 | 100.00 | 100.00 | 100.00 | 99.84 | 91.03 | 77.76 | +22.08 | +13.27 |
| **cavlc** | 1396 | 1.57 | 0.01 | 72.06 | 62.50 | 31.67 | 37.50 | 32.35 | 16.06 | +21.44 | +16.29 |
| **ctrl** | 357 | 1.41 | 0.00 | 93.75 | 93.75 | 80.86 | 53.12 | 50.00 | 49.38 | +3.74 | +0.62 |
| **dec** | 616 | 1.45 | 0.00 | 100.00 | 100.00 | 100.00 | 75.00 | 88.89 | 79.17 | -4.17 | +9.72 |
| **div** | 114622 | 170.16 | 0.45 | 34.81 | 40.25 | 34.73 | 25.11 | 27.83 | 22.69 | +2.42 | +5.14 |
| **hyp** | 428926 | 3647.69 | 1.97 | 54.30 | 49.74 | 48.79 | 37.48 | 30.77 | 28.10 | +9.38 | +2.67 |
| **i2c** | 2861 | 1.90 | 0.04 | 97.78 | 88.93 | 60.57 | 59.26 | 54.80 | 33.49 | +25.77 | +21.31 |
| **int2float** | 531 | 1.44 | 0.00 | 88.00 | 66.00 | 36.36 | 46.00 | 35.00 | 19.57 | +26.43 | +15.43 |
| **log2** | 64152 | 79.35 | 0.22 | 24.52 | 22.51 | 11.51 | 12.34 | 11.30 | 5.78 | +6.56 | +5.52 |
| **max** | 6242 | 4.78 | 0.03 | 100.00 | 96.34 | 78.61 | 50.37 | 48.54 | 40.35 | +10.02 | +8.19 |
| **mem_ctrl** | 95424 | 94.21 | 0.33 | 57.42 | 40.47 | 21.00 | 39.89 | 26.10 | 12.56 | +27.33 | +13.54 |
| **multiplier** | 54252 | 48.15 | 0.20 | 58.74 | 54.92 | 50.95 | 35.22 | 32.38 | 28.60 | +6.62 | +3.78 |
| **priority** | 2084 | 1.85 | 0.01 | 89.69 | 89.69 | 81.57 | 67.01 | 65.21 | 55.92 | +11.09 | +9.29 |
| **router** | 628 | 1.45 | 0.00 | 28.00 | 26.00 | 13.39 | 14.00 | 13.00 | 7.68 | +6.32 | +5.32 |
| **sin** | 10856 | 10.10 | 0.04 | 86.83 | 88.13 | 87.07 | 78.57 | 78.80 | 67.10 | +11.47 | +11.70 |
| **sqrt** | 49364 | 192.74 | 0.17 | 99.84 | 99.76 | 60.96 | 60.37 | 62.04 | 36.37 | +24.00 | +25.67 |
| **square** | 37036 | 79.11 | 0.12 | 55.26 | 53.47 | 48.82 | 50.25 | 47.43 | 37.58 | +12.67 | +9.85 |
| **voter** | 28517 | 47.20 | 0.10 | 60.87 | 56.63 | 37.85 | 30.44 | 28.32 | 18.93 | +11.51 | +9.39 |

> **Metircs Explained:**
> *   **GNN Time**: Time taken to generate rankings.
> *   **Node Cov**: Percentage of critical nodes identified (Top 10%/20%).
> *   **Fault Cov**: Percentage of actual faults detected.
> *   **Gap**: Improvement over random selection.

### Detailed Simulation Results

For each circuit, comprehensive simulation data is stored in `Supplementary_Experiments/full_injection_results_verilator/<circuit_name>/`. Key files include:

*   **`full_injection_results.json`**: Contains the raw outcome of every fault injection trial (detected vs. undetected).
*   **`cumulative_coverage_v1.csv`**: Tracks how fault coverage increases as more nodes are tested, comparing GNN-based ranking against random selection.

## Usage

### 1. Generate GNN Rankings

To analyze the circuit and generate node sensitivity rankings:

```bash
python unsup_sensitivity.py --netlist netlists/<circuit>.v
```
This will produce a ranking file in `gnn_ranks/gnn_rank_<circuit>_v1.txt`.

### 2. Run Fault Injection Simulation

To run fault injection based on the generated rankings:

```bash
python full_node_injection_verilator_parallel.py
```

## Citation

If you use these benchmarks, please cite the original paper:

> L. Amarú, P.-E. Gaillardon, G. De Micheli, "The EPFL Combinational Benchmark Suite", Proc. IWLS, Mountain View, CA, June 2015.

Repository: [lsils/benchmarks](https://github.com/lsils/benchmarks)
