# Title: ReMCA: A Reconfigurable Multi-Core Architecture for Full RNS Variant of BFV Homomorphic Evaluation(TCAS I)

# <center>Preliminaries
## The Textbook BFV Scheme

## Parameter Setup
polynomial degree: 4096

the size of modulus *q*: 128 bit(product of four 32 bit primes)

the standard deviation of the Gaussian
distribution to σ: 3.19

the size of the larger modulus Q
to at least 288-bit

32-bit primes to construct the RNS for our implementation
# <center>Algorithm And Approach
## Unified Low-Complexity NTT/INTT
![avatar](/Pic/Unified%20Low-Complexity%20CG%20NTT%20INTT.png)
It is a algorithm can control the butterfly unit to do NTT or INTT
, decrease the complexity of memory access.
## RNS Basis Extension
![avatar](/Pic/RNS%20Basis%20Extension.png)

# <center>Architecture
## Overall Architecture
![avatar](/Pic/Architecture%20of%20ReMCA.png)
Reconfigurable PE Array: perform NTT/INTT, the modular multplication. One
row or multiple rows of PE can be configured as a channel
to perform the polynomial arithmetic operations on one RNS
base.

TF ROM Array: store the twiddle factor array

Data RAM Array: store the input polynomials, intermediate results and final results

Total of 40 PEs, in which each row corresponds to one channel and each channel contains two slices and 8 PEs (4 for each slice). To maximize the parallelism of the processing path and match the number of extended RNS bases, set five channels in PE array.
## Reconfigurable PE Unit
![avatar](/Pic/Architecture%20of%20reconfigurable%20PE.png)
Reconfigurable PE: INTT,NTT,MULT

Barrett modular multiplier: modular multiplier, modular reduction
### Property:1
$\frac{x}{2}= (2\lfloor \frac{x}{2}\rfloor+1)\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor(q+1)+\frac{q+1}{2}=\lfloor \frac{x}{2}\rfloor+\frac{q+1}{2}(modq)$