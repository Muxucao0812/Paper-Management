---
marp: true
size: 16:9
theme: gaia
_class: lead
backgroundColor: #fff
paginate: true
---

## Title: ReMCA: A Reconfigurable Multi-Core Architecture for Full RNS Variant of BFV Homomorphic Evaluation 
###### *(TCAS I)*
---

### Preliminaries
#### The Textbook BFV Scheme
- BFV.KeyGen($\lambda,\omega$)
- BFV.Enc($m,pk$)
- BFV.Dec($ct,sk$)
- BFV.HomAdd($ct_0,ct_1$)
- BFV.HomMult($ct_0,ct_1,rlk$)

---
### Preliminaries
#### Parameter Setup
- polynomial degree: 4096
- the standard deviation of the Gaussian distribution to σ: 3.19
- the size of modulus *q*: 128 bit(product of four 32 bit primes)?
- the size of the larger modulus Q to at least 288-bit(product of nine 32 bit primes)
- 32-bit primes to construct the RNS for our implementation

---
### Algorithm And Approach
#### Unified Low-Complexity NTT/INTT
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Unified%20Low-Complexity%20CG%20NTT%20INTT.png?raw=true)
 It is a algorithm can control the butterfly unit to do NTT or INTT, decrease the complexity of memory access.
# <!-- fit -->$(\frac{N}{2}log_2^{N}+N)+(\frac{N}{2}log_2^{N}+2N)->(Nlog_2^{N}+N)$

---
### Algorithm And Approach
#### RNS Basis Extension
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/RNS%20Basis%20Extension.png?raw=true)
Chinese remainder theorem
# <!-- fit -->$q = \prod_{i = 1}^{k}q_i,p = \prod_{j = k+1}^{k+k'}q_j,Q=p*q$
###### $where \quad k=4 \quad k'=5$

# <!-- fit --> $A_j\equiv(\sum({A_i*\tilde{q_i}}mod q_{i})*q_i^*-V'*q)mod q_j$

######  $V'=\lfloor \sum(A_i*\tilde{q_i}modq_i^*)/q_i \rceil$

---
### Algorithm And Approach
#### RNS Basis


---
### Architecture
#### Overall Architecture
![w:500px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Architecture%20of%20ReMCA.png?raw=true)

---
Reconfigurable PE Array: perform NTT/INTT, the modular multplication. One
row or multiple rows of PE can be configured as a channel to perform the polynomial arithmetic operations on one RNS
base.
TF ROM Array: store the twiddle factor array
Data RAM Array: store the input polynomials, intermediate results and final results
Total of 40 PEs, in which each row corresponds to one channel and each channel contains two slices and 8 PEs (4 for each slice). To maximize the parallelism of the processing path and match the number of extended RNS bases, set five channels in PE array.

---
### Architecture
#### Reconfigurable PE Unit
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Architecture%20of%20reconfigurable%20PE.png?raw=true)

---
Reconfigurable PE: INTT,NTT,MULT
Barrett modular multiplier: modular multiplier, modular reduction
1.PE not onlu supports the functions with the variable modulus, but also supports the summation of modular multiplication
2.By merging the multiplicative factor 1/2 into the twiddle factors, the reconfigurable PE eliminates the multiplication of 1/2 in the subtraction path and improves the performance of PE unit.
$\frac{x}{2}= (2\lfloor \frac{x}{2}\rfloor+1)\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor(q+1)+\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor+\frac{q+1}{2}(modq)$
3.The Barrett modular multiplier we presented employs a reconfigurable architecture and avoids the needs of other computing units for ReMCA.

---
### Architecture
#### Confilct-Free Memory Access for NTT/INTT
![w:1000px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Data%20memory%20access%20pattern.png?raw=true)

---
Bank is dual-port pattern(could select the bank read port based on PEs)
For the bit-reversal operation, could change the address mapping pattern to avoid timing-consuming or memory-consuming.

---
### Architecture
#### Unified Computing Model
##### Unified Hardware Architecture Mapping Model:
![w:400px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Unified%20hardware%20architect%20mapping%20model.png?raw=true)

---
model 1: compute 32 bits modular mult of four contiguous integers in vector **$A_i$** nad vector **$B_i$** or four constants in parallel. 
model 2: compute the summation of four products, while the inputs of four products are from four different vectors and four constants respectively
model 3: The NTT/INTT transforms are computed using Mode 3
model 4: compute the summation of four products followed by a rounding operation

---
### Architecture
#### Unified Computing Model
##### Unified Data Memory Organization Model:
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Unified%20data%20memory%20organization%20model.png?raw=true)

---
MEM consists of four memory banks, where each memory bank further contains four 1024-depth and 32-bit-width dual-port RAMs. 
MEMA is used to store
the inputs/outputs and intermediates results of almost all functional units in homomorphic evaluation of RNS-BFV
except for the NTT and INTT.
MEMB is mainly used to store the inputs/outputs and intermediate results of NTT and INTT

---
![w:800px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Detailed%20structure%20of%20interconnection%20network%20of%20each%20slice.png?raw=true)

---
### Mapping Method And Execution Flow
The homomorphic multiplication of RNS-BFV includes four computing units: basis extension, ciphertext multiplica-tion, basis scaling and relinearization

---
### Mapping Method And Execution Flow
#### Computing Units Mapping
##### Basis Extension Unit
![w:700px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Mapping%20method%20of%20basis%20extension%20unit.png?raw=true)

---
### Mapping Method And Execution Flow
#### Computing Units Mapping
##### Ciphertext Multiplication Unit
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Mapping%20method%20of%20ciphertext%20multiplication%20unit.png?raw=true)

---
### Mapping Method And Execution Flow
#### Computing Units Mapping
##### Basis Scaling Unit:
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/Mapping%20method%20of%20basis%20scaling%20unit.png?raw=true)

---
### Execution Flow of RNS-BFV
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/PERFORMANCE%20COMPARISON%20OF%20NTT%20INTT.png?raw=true)

---
## IMPLEMENTATION RESULTS AND COMPARISONS
### FPGA Implementation Result
Xilinx Vivado tool
Virtex-7 XC7VX1140T
synthesized the design and achieved 250MHz
frequency under the parameter set (N = 4096, log(q) = 128-bit, log(qi) = 32-bit)

---
![w:600px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/ReMCA%20result.png?raw=true)

---
![w:900px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/The%20relationship%20between%20the%20number%20of%20PEs%20and%20performance.png?raw=true)

---
### Comparison of NTT/INTT Acceleration
![w:1200px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/PERFORMANCE%20COMPARISON%20OF%20NTT%20INTT.png?raw=true)

---
### Comparison of BFV Acceleration
![w:1200px](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/ReMCA_Pic/PERFORMANCE%20COMPARISON%20OF%20HOMOMORPHIC%20EVALUATION%20OF%20RNS-BFV.png?raw=true)




