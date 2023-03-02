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
![bg right 80%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/radix_4.jpeg?raw=true)
- radix based (radix = $2^k$) FFT idea
radix 2:  mult: $N/2 * log2^N$ add:$N* log2^N$
radix 4: mult:$(3/4)N*log4^N$ add:$2N* log4^N$
radix 8: mult:$(7/8)N*log8^N$ add：$4N* log8^N$
improve speed but bring additional overhead 

---
![w:820 h:330](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/NTT_fusion.jpeg?raw=true)
#### HFAuto
If X = ⌊{a mod (C ∗ R)}/C⌋, where a,C, and R are positive integers. Then, X = ⌊a/C⌋ mod R

---
### FHE ACCELERATOR-POSEIDON
#### Overall Architecture
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Poseidon%20architecture.jpeg?raw=true)
- scratchpad and high bandwidth memory, computing cores(cascade MA and MM cores)
- decompose higher level operations into basic operations to maximize parallelism

---
#### Memory System
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Poseidon%20architecture.jpeg?raw=true)
- HBM architecture involves two HBM2 stacks, which has 16 channels. Each channel is 64 bit with bit rate of up to 1800Mbps，provides 460GB/s

---
#### Memory System
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Poseidon%20architecture.jpeg?raw=true)
- stage1:data loaded from DDR to HBM via PCIe
- stage2:HBM transfers the data to the reg and BRAM
- stage3:the cores obtain the data from the scratchpad to accomplish computation and write back



---
#### Computational Cores
##### MA/MM
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/MA:MM%20core%20architecture.jpeg?raw=true)
- MA/MM: MA : two polynomials element-wise add/mult and obtain the modulo result
__fine-grained calculation module__
![w:320 h:80](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/MM:MA.jpeg?raw=true?raw=true)
![w:320 h:130](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/ModMult.jpeg?raw=true)

---
#### RNSconv
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/RNSconv%20architecture.jpeg?raw=true)
- accelerate $Keyswitch$ though __Modup__ and __Moddown__ operation
- Modup: vector-scalar multiplication, element-wise accumulation
- Moddown: vector subtraction, vector-scalar multiplication

---
#### RNSconv
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/RNSconv%20architecture.jpeg?raw=true)
- fetches two groups of data from the input buffer and takes the result as the input of the MM core to complete Modup
- takes the result as the input of MA core to complete Moddown

---
#### NTT/INTT
adopt radix 8 NTT
- Conventional NTT require $log2^8$=3 phases with 24 unfused TAMs in total
- taking 8 operands as input: 1 phase with 8 fused TAMs

---
#### Data access pattern
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Data%20access%20pattern%20comparison.jpeg?raw=true)
- phases required change from 12 to 4($(log2^{4096})/3$)
- conventional NTT offset $2^{iter-1}$,Poseidon offset $2^{(iter-1)*k}$

---
#### Data access pattern
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Data%20access%20pattern%20in%20Poseidon.jpeg?raw=true)
- iteration 1:load with index 0-7,8-15,...4088-4095
- iteration 2:load with fixed offset(index 0,8,16,24,32,40..)
- iteration 3: offset is 64 because it reorder the index for the next phase



---
#### Automorphism
![bg  100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/Automorphism%20architecture%20in%20Poseidon.jpeg?raw=true)

---
#### Automorphism

- stage 1: $row_i$ to $row_{ik mode R}$. Read 512 data per cycle from BRAMS according to the address selection circuit and write them to FIFO.
- stage 2: $FIFO_{(i,k)}$ to $FIFO_{(i+jk/C mod R,k)}$. This stage cyclically shifts the data in each FIFO
- stage 3: Switching data dimension. We use a similar idea with the memory access pattern of the NTT core to map the physical row data to the logical rows, and realize the two- dimensional data access on BRAMs.
- stage 4: $column_i$ to $column_{ikmod C}$. This stage is similar to Stage 1, where the data in column i will be read and write to the $column_{ik mod C}$.

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
![bg  60%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/parameter%20selection%20-k.jpeg?raw=true)

---
##### HFAuto
![bg  70%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Poseidon_Pic/resource%20and%20performance.jpeg?raw=true)


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


