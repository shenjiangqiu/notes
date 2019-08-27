# __different types of prefetcher__
- [__different types of prefetcher__](#different-types-of-prefetcher)
- [stride Prefetching](#stride-prefetching)
  - [1. Instruction-based Stride Prefetcher](#1-instruction-based-stride-prefetcher)
  - [2. Best-Offset Prefetcher (BOP).](#2-best-offset-prefetcher-bop)
    - [2.1 the Sandbox Prefetcher,SP,BOP was extened from SP.](#21-the-sandbox-prefetcherspbop-was-extened-from-sp)
    - [2.2 BOP:](#22-bop)
- [Temporal Prefetching](#temporal-prefetching)
  - [two state of the art temporal prefetching](#two-state-of-the-art-temporal-prefetching)
    - [1. Sampled Temporal MemoryStreaming (STMS)](#1-sampled-temporal-memorystreaming-stms)
    - [2. Irregular Stream Buffer (ISB).](#2-irregular-stream-buffer-isb)
  - [3.Spatial Prefetching](#3spatial-prefetching)
    - [3.1 Spatial Memory Streaming(SMS)](#31-spatial-memory-streamingsms)
    - [3.2 Variable Length Delta Prefetcher](#32-variable-length-delta-prefetcher)
# stride Prefetching

## 1. Instruction-based Stride Prefetcher
 *RPT: Reference Prediction Table*
|  Tag   | Last Block | Last stride |
| :----: | :--------: | :---------: |
| 0x1450 | 0x135f41D  |      5      |
|   ..   |     ..     |     ..      |
| 0x1900 | 0x21rr97f3 |      6      |
- Each entry in the RPT corresponds to a specific load instruction; it keeps the Last Block referenced by the instruction and the Last Stride observed in the stream
- trigger access (i.e., a cache miss or a prefetch hit)
- the RPT is searched with the __PC of the instruction__. If the search results in a miss, then it means that no history does exist for the instruction, and hence no prefetch request can be issued
- Under two circumstances, a search may result in a miss: 
1. whenever a load instruction is a __new one__ in the execution flow of the program
2. whenever a load instruction is re-executed after a long time, and was __evicted__
- when new entry create:__tagged__ with PC, __Last Block__: referenced address,__stride__:0.
- when hit
  - if it is a stride stream, issue multiple request, and update
  - if it is not, only update
 
---
## 2. Best-Offset Prefetcher (BOP).
###  2.1 the Sandbox Prefetcher,SP,BOP was extened from SP.
  - SP want to find the offest that yield __*accurate*__ prefetch requst
  - SP defines an __*evaluation period*__ in which it accesses the prefetching accuracy of multiple predefined offsets,from *-n* to *+n* , where n is a constant, say eight
  - For every prefetch offset, a *score* value is associated
  - SP issues **virtual prefetch** requests using various offsets.
  - For the sake of **storage efficiency**, SP uses a Bloom Filter as the specific storage for keeping the **record of prefetch candidates** of each offset 

 *sp structure*
![SP](https://sjqpc.tk/img/SP.png)
1. in evaluation period, SPU send evaluate request to ***BLOOM FILTER*** in a round robin fashion. 
2.  when a Cache miss, or prefetch hit happened, the ***bloom*** filter will tell spu to update the score. 
3.  After evaluation period, only score greater than a threshhold, the prefetch can be issue. 

### 2.2 BOP:

 *BOP structure*
1. main ideal
   1. For k to be a **timely** prefetch offset for line A, line A − k should have been accessed recently.
   2. offsets whose prefetch candidates are used by the application **not much longer** than they generated are considered as the suitable offsets
   3. their score values are incremented
2. Recent Requests Table (RRT),a replace to Bloom filter
   1. size: small to keep only recent requsets
   2. for event A, and in evaluation period of offset k, if A-k in RRT, increase the score of offset k.
   3. that means, if the prefetcher had issued a request upon A-k, the request(A) should be timely.
   

![BOP](https://sjqpc.tk/img/BOP.png)

# Temporal Prefetching
1. Temporal prefetching is an ideal choice to eliminate long chains ofdependent cache misses, that are common in **pointer-chasing** applications
2. replaying the sequence of past cache misses to avert future misses
3. low accuracy as they do not know where streams end

## two state of the art temporal prefetching

### 1. Sampled Temporal MemoryStreaming (STMS)
![STMS](https://sjqpc.tk/img/STMS.png)

- STMS uses a circular FIFO buffer, named *History Table*,
- For locating every address in the History Table, STMS uses an auxiliary set-associative structure, named *Index Table*.
  
1. all streams are stored next to each other in a storage-efficient manner.
2. The Index Table stores a pointer for every observed miss address to its **last occurrence** in the *History Table*
3. whenever a cache miss occurs, the prefetcher first looks up the *Index Table* with the missed address and gets the corresponding pointer.
4. Using the pointer, the prefetcher proceeds to the *History Table* and issues prefetch requests for addresses that have **followed the missed address** in the history

### 2. Irregular Stream Buffer (ISB). 
> this is from the survey, Maybe wrong.

![ISB](https://sjqpc.tk/img/ISB.png)

 ***Physic-to-Structural Address Mapping***
| Physical Address | Structual Address |
| :--------------: | :---------------: |
|        A         |         m         |
|       ...        |        ...        |
|        B         |        m+1        |
|        X         |         n         |

 ***Structural-to-Physical Address Mapping***
| Structual Address | Physical Address |
| :---------------: | :--------------: |
|     m,m+1,...     |     A,B,...      |
|        ...        |       ...        |
|     n,n+1,...     |     X,Y,...      |
|        ...        |       ...        |

- **ISB attempts to extract temporal correlation among memory references on a per load instruction basis**
- **training**: 
    1. check the traning unit, and update or insert to the PSAM and SPAM
    2. if a pair(A,B)exsit, increase the confidence counter for B's entry in the PSAMC.
    3. if A,B have been assigned non-consecutive structural addresses, decrement the confidence counter.
    4. when hit zero, re-assign B next to A;
    5. When A not exist, generate a new, assign B. Structural address are allocated in fixed size chunks of size c.(c = 256)
- **Prediction**:
    1. find the structural address from the trigger in **PS-AMC**
    2. predict the sequential structural address
    3. convert the predicted structrual address to a physical address.
> ISB from the paper

![ISB2](https://sjqpc.tk/img/ISB2.png)

## 3.Spatial Prefetching

### 3.1 Spatial Memory Streaming(SMS)
![SMS](https://sjqpc.tk/img/sms.png)



### 3.2 Variable Length Delta Prefetcher
![VLDP](https://sjqpc.tk/img/VLDP.png)


### 3.3 Spatio-temporal Prefetching

```
Temporal and spatial prefetching techniques capture separate subsets of cache misses, and hence each omits a considerable portion of cache misses unpredicted. As a considerable fraction of data misses is predictable only by one of the two prefetching techniques, spatio-temporal prefetching tries to combine them to reap the benefits ofboth methods. Anothermotivation for spatio-temporal prefetching is the fact that the effectiveness of temporal and spatial prefetching techniques varies across applications. As discussed, pointer-chasing applications (e.g., OLTP) produce long chains of dependent cache misses that cannot be effectively captured by spatial prefetching but can be captured by temporal prefetching. On the contrary, scan-dominated applications (e.g., DSS) produce a large number of compulsory cache misses that are predictable by spatial prefetchers and not by temporal prefetchers. We include Spatio-Temporal Memory Streaming (STeMS) [104], as it is the only proposal in
this class of prefetching techniques. STeMS synergistically integrates spatial and temporal prefetching techniques in a unified
prefetcher; STeMS uses a temporal prefetcher to capture the stream of trigger accesses (i.e., the first access to each spatial region) and a spatial prefetcher to predict the expected misses within the spatial regions. The metadata organization of STeMS mainly consists of the metadata tables of STMS [110]and SMS[105]. STeMS, however, seeks to stream the sequence of cache misses in the order they have been generated by the processor, regardless of how the corresponding metadata information has been stored in the history tables of STMS and SMS. To do so, STeMS employs a Reconstruction Buffer, which is responsible for reordering the prefetch requests generated by the temporal and the spatial prefetchers of STeMS to send prefetch requests (and deliver their responses) in the order the processor is supposed to consume them. For enabling the reconstruction process, the metadata tables ofSMS and STMS are slightly modified. SMS is modified to record the order of the accessed cache blocks within a spatial region by encoding spatial patterns as ordered lists of offsets, stored in Patterns Sequence Table (PST). Although PSTis less compact than PHT(in the original SMS), the offset lists maintain the order required for accurately interleaving temporal and spatial streams. STMS is also modified and records only spatial triggers (and not all events as in STMS) in a Region Miss Order Buffer (RMOB).Moreover, entries in both spatial and temporal streams are augmented with a delta field. The delta field in a spatial (temporal) stream represents the number of events from the temporal (spatial) stream that is interleaved between the current and next events ofthe same type. Figure 9 gives an example of how STeMS reconstructs the total miss order.
```