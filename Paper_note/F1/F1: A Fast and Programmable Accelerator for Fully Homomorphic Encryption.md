---
marp: true
size: 16:9
theme: gaia
_class: lead
backgroundColor: #fff
paginate: true
---

## Title: F1: A Fast and Programmable Accelerator for Fully Homomorphic Encryption
###### *(2021 MICRO)*
---
### Introduction
#### Challenges
- Complex operations on long vectors: modular arithmetic, several thousan elements
- Regular computation: all operations are known ahead of time, VLIM
- Challenging data movement: large amounts (tens of MBs) of data; encrypting data increase its size(50X); data in long vectors

---
### Introduction
#### Contributions
- F1 features an explicitly managed on-chip memory hierarchy, with a heavily bank scratchpad and distributed reg files
- ##### F1 uses mechanisms to decoupled data movement and hide access latencies by loading data far ahead of its use
- F1 uses new scheduling algorithms that maximize reuse and make the best out of limited memory bandwidth
- F1 used few functional units with hight throughtput that reduces the amount of data

---
### Background
#### FHE programming model and operations
- element-wise
- addition (mod t)
- multiplication (mod t)
- a small set of particular vector permutations.

---
#### BGV implementation overview
Data types:
$a = a_0+a_1x+...+a_{N-1}x^{N-1}\in R_t$
Each plaintext is encrypted into a ciphertext consisting of two polynomials of N integer coefficients modulo some $Q≫t$. Each ciphertext polynomial is a member of $R_Q$.

Encrtyption and decryption:
secret key: $s \in R_Q$.To encrypt a plaintext $m∈R_t$,one samples a uniformly random $a ∈ R_Q$ , an error (or noise) $e ∈ R_Q$ with small entries, and computes the ciphertext ct as
$ct =(a,b=as+te+m)$