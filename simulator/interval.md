# Interval Simulation: Raising the level of abstraction in architectural simulation
## abstract
 By raising the level of abstraction, interval simulation reduces both development time and evaluation time
### accuracy
 * average error of 4.6% and max error of 11% for the multi-threaded fullsystem workloads
### fast
 * while achieving a one order of magnitude simulation speedup compared to cycle-accurate simulation.
### easy to implement
* our implementation of the mechanistic analytical model incurs only one thousand lines of code
---
## introduction
* The key challenge in raising the level of abstraction in multi-core simulation is how to cope with the tight performance entanglement between co-executing threads
* Branch predictor, memory hierarchy, cache coherence and interconnection network simulators determine the miss events;
* The cooperation between the mechanistic analytical model and the miss event simulators enables the modeling of the tight performance entanglement between co-executing threads on multi-core processors.
---
## interval Analysis(background)

![Image of Yaktocat](../images/1.png)
* For an I-cache miss (or I-TLB miss), the penalty equals the miss delay, i.e., the time to access the next level in the memory hierarchy.
* For a branch misprediction, the penalty equals the time between the mispredicted branch being dispatched and new instructions along the correct control flow path being dispatched. This penalty **includes the branch resolution time plus the front-end pipeline depth.**
* Upon a long-latency load miss, i.e., a last-level L2 Dcache load miss or a D-TLB load miss, the processor back-end will stall because of the reorder buffer (ROB), issue queue, or rename registers getting exhausted. As a result, dispatch will stall. When the miss returns from memory, instructions at the ROB head will be committed, and new instructions will enter the ROB. The penalty for a long-latency D-cache miss thus equals the time between dispatch stalling upon a full ROB and the miss returning from memory. This penalty can be approximated by the memory access latency. In case multiple independent longlatency load misses make it into the ROB simultaneously, both will overlap their execution, thereby exposing memory-level parallelism (MLP) [5], provided that a sufficient number of outstanding long-latency loads are supported by the hardware. The penalty of multiple overlapping long-latency loads thus equals the penalty for an isolated long-latency load. In case of dependent long-latency loads, their penalties serialize.
* Chains of dependent instructions, L1 data cache misses and long-latency functional unit instructions (divide, multiply, etc.), or store instructions, may cause a resource (e.g., reorder buffer, issue queue, physical register file, write buffer, etc.) to fill up. A resource stall as a result of it may (eventually) stall dispatch. The penalty or the number of cycles where dispatch stalls due to a resource stall are attributed to the instruction at the ROB head, i.e., the instruction blocking commit and thereby stalling dispatch