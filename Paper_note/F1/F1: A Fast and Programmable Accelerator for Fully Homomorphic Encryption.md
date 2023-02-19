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
