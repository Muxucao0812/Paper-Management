---
marp: true
size: 16:9
theme: gaia
_class: lead
backgroundColor: #fff
paginate: true
---

# Title: ReMCA: A Reconfigurable Multi-Core Architecture for Full RNS Variant of BFV Homomorphic Evaluation 
###### *(TCAS I)*
---

## Preliminaries
### The Textbook BFV Scheme
#### Parameter Setup
polynomial degree: 4096
the size of modulus *q*: 128 bit(product of four 32 bit primes)
the standard deviation of the Gaussian distribution to σ: 3.19
the size of the larger modulus Q to at least 288-bit
32-bit primes to construct the RNS for our implementation

---
## Algorithm And Approach
### Unified Low-Complexity NTT/INTT
![30%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/Unified%20Low-Complexity%20CG%20NTT%20INTT.png)
 It is a algorithm can control the butterfly unit to do NTT or INTT, decrease the complexity of memory access.

---

## Algorithm And Approach
### RNS Basis Extension
![w:200px, h:400px](/Pic/RNS%20Basis%20Extension.png)

---
## Architecture
### Overall Architecture
![w:150px, h:300px](/Pic/Architecture%20of%20ReMCA.png)
Reconfigurable PE Array: perform NTT/INTT, the modular multplication. One
row or multiple rows of PE can be configured as a channel to perform the polynomial arithmetic operations on one RNS
base.
TF ROM Array: store the twiddle factor array
Data RAM Array: store the input polynomials, intermediate results and final results
Total of 40 PEs, in which each row corresponds to one channel and each channel contains two slices and 8 PEs (4 for each slice). To maximize the parallelism of the processing path and match the number of extended RNS bases, set five channels in PE array.

---
## Architecture
### Reconfigurable PE Unit
![w:150px, h:300px](/Pic/Architecture%20of%20reconfigurable%20PE.png)
Reconfigurable PE: INTT,NTT,MULT
Barrett modular multiplier: modular multiplier, modular reduction
1.PE not onlu supports the functions with the variable modulus, but also supports the summation of modular multiplication
2.By merging the multiplicative factor 1/2 into the twiddle factors, the reconfigurable PE eliminates the multiplication of 1/2 in the subtraction path and improves the performance of PE unit.

$\frac{x}{2}= (2\lfloor \frac{x}{2}\rfloor+1)\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor(q+1)+\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor+\frac{q+1}{2}(modq)$

3.The Barrett modular multiplier we presented employs a reconfigurable architecture and avoids the needs of other computing units for ReMCA.

---
## Architecture
### Confilct-Free Memory Access for NTT/INTT
![w:150px, h:300px](/Pic/Data%20memory%20access%20pattern.png)
Bank is dual-port pattern(could select the bank read port based on PEs)
For the bit-reversal operation, could change the address mapping pattern to avoid timing-consuming or memory-consuming.

---
### Unified Computing Model
#### Unified Hardware Architecture Mapping Model:
![w:150px, h:300px](/Pic/Unified%20hardware%20architect%20mapping%20model.png)
model 1: compute 32 bits modular mult of four contiguous integers in vector **$A_i$** nad vector **$B_i$** or four constants in parallel. 
model 2: compute the summation of four products, while the inputs of four products are from four different vectors and four constants respectively
model 3: The NTT/INTT transforms are computed using Mode 3
model 4: compute the summation of four products followed by a rounding operation

---
#### Unified Data Memory Organization Model:
![w:150px, h:300px](/Pic/Unified%20data%20memory%20organization%20model.png )
MEM consists of four memory banks, where each memory bank further contains four 1024-depth and 32-bit-width dual-port RAMs. 
MEMA is used to store
the inputs/outputs and intermediates results of almost all functional units in homomorphic evaluation of RNS-BFV
except for the NTT and INTT.
MEMB is mainly used to store the inputs/outputs and intermediate results of NTT and INTT
![w:150px, h:300px](/Pic/Detailed%20structure%20of%20interconnection%20network%20of%20each%20slice.png)

---
## Mapping Method And Execution Flow
The homomorphic multiplication of RNS-BFV includes four computing units: basis extension, ciphertext multiplica-tion, basis scaling and relinearization

---
### Computing Units Mapping
#### Basis Extension Unit
![avatar](/Pic/Mapping%20method%20of%20basis%20extension%20unit.png)

---
### Computing Units Mapping
#### Ciphertext Multiplication Unit
![avatar](/Pic/Mapping%20method%20of%20ciphertext%20multiplication%20unit.png)

---
### Computing Units Mapping
#### Basis Scaling Unit:
![avatar](/Pic/Mapping%20method%20of%20basis%20scaling%20unit.png)

---
### Execution Flow of RNS-BFV
![avatar](/Pic/PERFORMANCE%20COMPARISON%20OF%20NTT%20INTT.png)

---
## IMPLEMENTATION RESULTS AND COMPARISONS
### FPGA Implementation Result
Xilinx Vivado tool
Virtex-7 XC7VX1140T
synthesized the design and achieved 250MHz
frequency under the parameter set (N = 4096, log(q) = 128-bit, log(qi) = 32-bit)
![avatar](/Pic/ReMCA%20result.png)

![avatar](/Pic/The%20relationship%20between%20the%20number%20of%20PEs%20and%20performance.png)
### Comparison of NTT/INTT Acceleration
![avatar](/Pic/PERFORMANCE%20COMPARISON%20OF%20NTT%20INTT.png)
### Comparison of BFV Acceleration
![avatar](/Pic/PERFORMANCE%20COMPARISON%20OF%20HOMOMORPHIC%20EVALUATION%20OF%20RNS-BFV.png)




