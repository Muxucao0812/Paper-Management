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
