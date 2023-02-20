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

---
Ciphertext $ct = (a, b)$ is decrypted by recovering $e ′ = te + m =b − as\mod Q$, and then recovering $m = e^′\mod t$. Decryption is correct as long as $e^′$ does not “wrap around” modulo $Q$, i.e., its coefficients have magnitude less than $Q/2.$

---
##### Homomorphic operations
- addition
$ct_0 = (a_0,b_0)$ and $ct_1 =(a_1,b_1)$
$ct_{add}=ct_0+ct_1=(a_0+a_1,b_0+b_1)$
- multiplication
$ct_× = (l_2 , l_1 , l_0 ) = (a_0 a_1 , a_0 b_1 + a_1 b_0 , b_0 b_1 )$
$(u_1,u_0)=KeySwitch(I_2)$
$ct_{mul}=(I_1+u_1,I_0+u_0)$

---
- permutations
There are N automorphisms, denoted $σ_k (a)$ and $σ_{−k} (a)$ for all positive odd $k < N$ . Specifically,$σ_k(a) : a_i ->(−1)^s a_{ik} \mod N$ for $i = 0, ..., N−1$
where $s = 0$ if $ik \mod 2N < N$ , and $s = 1$ otherwise.
1.compute an automorphism on the ciphertext polynomials: $ct_σ = (σ_k (a), σ_k (b))$
2.$ct_{perm}=(u_1,σ_k (b)+u_0)$where $(u_1 , u_0 ) =KeySwitch(σ_k (a))$

---
##### Noise growth and management
Different operations induce different noise growth: addition and permutations cause little growth, but multiplication incurs much more significant growth.So, to a first order, the amount of  noise is determined by **multiplicative depth** , i.e., the longest chain of homomorphic multiplications in the computation.
**Noise forces the use of a large ciphertext modulus Q.** For example,
an FHE program with multiplicative depth of 16 needs Q to be about 512 bits. The noise budget, and thus the tolerable multiplicative depth,grow linearly $\log Q$

---
- Bootstrapping:
strength: enable FHE computations of unbounded depth;remove noise from a ciphertext without access to the secret key
weakness:need a large noise budget(large $Q$)
- Modulus switching:
rescales ciphertexts from modulus $Q$ to a modulus $Q'$.
To execute an multiplicative depth 16, we start with a 512 bit modulus $Q$. Before multiplicatino,switch to a modulus that is 32 bits shorter.

---
##### Security and parameters
demension *N* and modulus *Q*
$N/logQ$ must be above a certain level  for sufficient security.

---
#### Algorithmic insights and optimizations
- Fast polynomial multiplication via NTTs
- Avoiding wide arithmetic via Residue Number System(RNS)

---
#### Architectural analysis of FHE

![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Key%20switch.png?raw=true)

Three input: a polynomial $x$(store in $L$ residue polyniamials), two key-switch hint matrices $ksh0$,$ksh1$. Inputs and outputs are in the NTT domain; only $y[i]$ are in coefficient form.

---
**Computation vs. data movement**
- $L^2$ NTTs,$2L^2$multiplications,$2L^2$additions of N-element vectors
- In RNS, the rest of a homomorphic multiplication is $4L$ multiplications and $3L$ additions

$L=16,N=16K$
each RNS polynimial is 64KB, each polynimial is 1MB, each ciphertext is 2MB,key switch hints is 32MB. 
key switchinging demand 10TB/s of memory andwidth.

---
- Performance requirement:
(1) decouples data movement from computation, as demand
misses during frequent key-switches would tank performance
(2) implements a large amount of on-chip storage (over 32 MB in
our example) to allow reuse across entire homomorphic operations
- Functionality requirements:
Programmable FHE accelerators must support a wide range of parameters, both N (polynomial/vec-tor sizes) and L (number of RNS polynomials, i.e., number of 32-bit prime factors of Q). While N is generally fixed for a single program, L changes as modulus switching sheds off polynomials.

---
### F1 ARCHITECTURE
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)
###### Vector processing with specialized functional units
FUs process vectors of configurable length N using a fixed number of vector lanes E. 
- 128 lanes
- N from 1024 to 16384
- pipelined, throughput: E = 128 elements/cycle

---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)

###### Compute clusters:
- 1 NTT, 1 automorphism
- 2 multipliers
- 2 adders 
- a banked register file 

---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)

###### Memory system:
- a large, heavily banked scratchpad (64 MB across 16 banks)
- scratchpad interfaces with both high-bandwidth off-chip memory (HBM2) and with compute clusters through an on-chip network.

---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)
###### Static scheduling(programs are regular):
- VLIW processors?
- FUs: no stalling logic
- Memory: no conflicts
- On-chip network: use switch change configuration


---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)
###### Distribute control:
- independent instruction stream: programs have loops, unroll them avoid branches, and compile programs into linear sequences of instructions

---
### F1 ARCHITECTURE
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20architecture.png?raw=true)

###### Register file design:
use an 8-banked element-partitioned register file design that leverages long vectors: each vector is striped across banks, and each FU cycles through all banks over time, using a single bank each cycle

--- 
### SCHEDULING DATA AND COMPUTATION
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20compiler.png?raw=true)
- Compiler: orders high level operations to maximize reuse and translates the program into a DFG

---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20compiler.png?raw=true)
- DM Scheduler: transfer between main memory andthe scratchpad to achieve decoupling and maximize reuse 

---
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/F1%20compiler.png?raw=true)
- CL Scheduler: determine the exact cycles of all operations and produces the instruction strams for all components

---
#### Translating the program to a dataflow graph
![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/matrix%20vector%20muliply%20using%20FHE.png?raw=true)
![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/matrix%20vector%20multply%20in%20F1's%20DSL.png?raw=true)


---
#### Compiling homomorphic operations
It clusters operations to improve reuse and translates them down to instruction.
- Ordering: maximize the reuse of key switch hints(line 8)(line 12)
- Translation:  minimize the amount of instructions intermediates

---
#### Scheduling data transfers
- data transfers decoupled from computation
- minmize off-chip data transfers
- achieve good parallelism

---
It does not consider on-chip data movement, and simply treats all functional units as being directly connected to the scratchpad.

It considers instructions ready if their inputs are available in the
scratchpad, and follows instruction priority among ready ones. To
schedule loads, we assign each load a priority
$p(load) = max\{p(u)|u ∈ users(load)\}$
then greedily issue loads as bandwidth becomes available. When
issuing an instruction, we must ensure that there is space to store
its result. We can often replace a dead value.

---
#### Cycle-level scheduling

---
### FUNCTIONAL UNITS
#### Automorphism unit
![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Applying%20%CF%833%20on%20an%20RNS%20polynomial.png?raw=true)
![bg 50%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Automorphism%20unit.png?raw=true)

---
#### Transpose unit
![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Transpose%20unit%20(right)%20and%20its%20component%20quadrant-%0Aswap%20unit%20(left).png?raw=true)
![bg 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Transpose%20unit.png?raw=true)

---
#### Four-step NTT unit
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Four-step%20NTT%20unit.png?raw=true)

---
#### Optimized modular multiplier
![bg right 100%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Area%2C%20power%2C%20and%20delay%20of%20modular%20multipliers.png?raw=true)

---
### F1 IMPLEMENTATION
![bg 45%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Area%20and%20Thermal%20Design%20Power%20(TDP)%20of%20F1%2C%20and%0Abreakdown%20by%20component.png?raw=true)

---
### EXPERIMENTAL METHODOLOGY
- Modeled system: 
a cycle-accurate simulator to execute F1 programs
activity-level energies from RTL synthesis to produce energy breakdowns
- Benchmarks:
Logistic regression: uses the HELR algorithm:256 features, 256  samples, depth L =16
Neural network:LoLa-MNIST,LoLa-CIFAR
DB Lookup:A BGV-encrypted query string is used to traverse an encrypted key-value store and return the corresponding value.

---
- Bootstrapping: 
BGV: Sheriff and Peikert’s algorithm
CKKS: non-packed CKKS bootstrapping
- Baseline systems:
F1 with a CPU system running the baseline programs (a 4-core, 8-thread, 3.5 GHz Xeon E3-1240v5)

---
### EVALUATION
#### Performance
##### Benchmarks
![bg 50%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Performance%20of%20F1%20and%20CPU%20on%20full%20FHE%20bench-%0Amarks:%20execution%20times%20in%20milliseconds%20and%20F1%E2%80%99s%20speedup.png?raw=true)

---
##### Microbenchmarks
![bg 90%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Performance%20on%20microbenchmarks.png?raw=true)

---
#### Performance
##### Data movement&Power consumption
![bg 35%](https://github.com/Muxucao0812/Paper-Management/blob/main/Pic/F1_Pic/Perbenchmark%20breakdowns.png?raw=true)
