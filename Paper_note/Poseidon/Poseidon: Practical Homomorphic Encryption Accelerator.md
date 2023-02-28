---
marp: true
size: 16:9
theme: gaia
_class: lead
backgroundColor: #fff
paginate: true
---

## Poseidon: Practical Homomorphic Encryption Accelerator
###### *(2023 HPCA)*
---
### Methodology
#### NTT-fusion
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/NTT_fusion.jpeg?raw=true)


---
#### HFAuto

---
### FHE ACCELERATOR-POSEIDON
#### Overall Architecture
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Poseidon%20architecture.jpeg?raw=true)

---
#### Computational Cores
##### MA/MM
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/MA:MM%20core%20architecture.jpeg?raw=true)

---
#### RNSconv
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/RNSconv%20architecture.jpeg?raw=true)

---
#### NTT/INTT
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Data%20access%20pattern%20in%20Poseidon.jpeg?raw=true)

---
#### Data access pattern
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Data%20access%20pattern%20comparison.jpeg?raw=true)

---
#### Automorphism
![bg  100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Automorphism%20architecture%20in%20Poseidon.jpeg?raw=true)

---
### EVALUATION
#### Platform
Xilinx Alveo U280(owns HBM) FPGA plugged into the PCIe slot of the mainboard
Vivado and Vitis on the host side.

#### Baseline 
CPU (Intel Xeon Gold 6234) running at 3.3 GHz with a single thread 
state-of-the-art GPU 
FPGA 
4 FHE accelerator ASICs

---
#### Benchmark
- Logistic regression (LR). It is the HELR algorithm implementation based on the CKKS scheme.In combination with Bootstrapping, we use the multiplication depth of L = 38 and evaluate the average performance of 10 iterations supported by two Bootstrapping operations.
- LSTM. It is the Long-Term Short-Term (LSTM) model. It requires 50
Bootstrapping operations in total during one inference.
- ResNet-20. This benchmark is the inference of an image on the ResNet-20 model implemented with FHE.
- Packed bootstrapping(packed bootstrapping algorithm). bootstrapping L = 3; multiplication depth L = 57.
  
---
#### Accelerator Performance
##### FHE Basic Operations
![bg  90%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Operator%20core%20analysis.jpeg?raw=true)
![bg  100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Performance%20comparison%20of%20FHE%20basic%20operations.jpeg?raw=true)

---
##### Full-system performance
![bg  100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/full%20system%20performance.jpeg?raw=true)
![bg  100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/comparison%20of%20the%20storage%20resource%20consumption.jpeg?raw=true)

---
##### Bandwidth Utilization
![bg  90%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/lowest%20and%20average%20bandwidth%20utilization%20analysis.jpeg?raw=true)

---
##### Poseidon Specifics
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/parameter%20selection%20-k.jpeg?raw=true)

---
##### HFAuto
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/resource%20and%20performance.jpeg?raw=true)


---
##### Scalability
![bg 75%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/sensitivity%20of%20the%20lanes.jpeg?raw=true)

---
#### Energy
##### Energy Consumption and Breakdown
![bg 50%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Energy%20consumption%20and%20breakdown.jpeg?raw=true)

---
##### Efficiency and Utilization
![bg 90%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/efficiency%20and%20fpga%20resource.jpeg?raw=true)

![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/resouce%20utilization%20comparison.jpeg?raw=true)


