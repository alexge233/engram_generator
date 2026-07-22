"""Knowledge atoms for OS, distributed systems, and compiler optimization.

Covers process scheduling, memory management, distributed consensus,
replication, and compiler optimization passes. Each atom includes
a Wikipedia-sourced description and a worked example.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# OS deep (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="process_scheduling_sjf",
    content=(
        "Shortest Job First (SJF) is a scheduling algorithm that selects "
        "the process with the smallest execution time. In non-preemptive SJF, "
        "once a process starts, it runs to completion. In preemptive SJF "
        "(Shortest Remaining Time First), a running process can be preempted "
        "if a new process arrives with a shorter burst time. SJF is optimal "
        "for minimising average waiting time among non-preemptive algorithms."
    ),
    example=(
        "Processes P1=6, P2=8, P3=7, P4=3 (burst times). "
        "SJF order: P4(3), P1(6), P3(7), P2(8). "
        "Waiting: P4=0, P1=3, P3=9, P2=16. Avg = (0+3+9+16)/4 = 7.0"
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'Shortest job next', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shortest_job_next",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="memory_allocation",
    content=(
        "Memory allocation strategies determine how free memory blocks are "
        "assigned to processes. First Fit selects the first block large enough. "
        "Best Fit selects the smallest block that is large enough, minimising "
        "wasted space. Worst Fit selects the largest block, leaving the biggest "
        "remainder. Next Fit is like First Fit but starts from the last "
        "allocation point."
    ),
    example=(
        "Blocks: [100, 500, 200, 300, 600]. Request 212KB. "
        "First Fit: block 500 (index 1). Best Fit: block 300 (index 3). "
        "Worst Fit: block 600 (index 4)."
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'Memory management', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Memory_management",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="page_table_lookup",
    content=(
        "In virtual memory systems, a page table maps virtual page numbers "
        "to physical frame numbers. A virtual address is split into a page "
        "number and an offset. The page table translates the page number to "
        "a frame number; the physical address is frame_number * page_size + "
        "offset. Multi-level page tables reduce memory overhead by only "
        "allocating table entries for used regions."
    ),
    example=(
        "Virtual address 0x3A7F, page size 4096 (0x1000). "
        "Page number = 0x3A7F / 0x1000 = 3, offset = 0xA7F. "
        "Page table: page 3 -> frame 7. Physical = 7 * 4096 + 0xA7F = 0x7A7F."
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'Page table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Page_table",
    prerequisites=["base_conversion"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="disk_scheduling",
    content=(
        "Disk scheduling algorithms determine the order in which disk I/O "
        "requests are serviced. FCFS processes requests in arrival order. "
        "SSTF (Shortest Seek Time First) selects the request closest to the "
        "current head position. SCAN (elevator) moves the head in one "
        "direction servicing requests, then reverses. C-SCAN services "
        "requests in one direction only, then jumps back to the start."
    ),
    example=(
        "Head at 53, requests: [98, 183, 37, 122, 14, 124, 65, 67]. "
        "SSTF order: 65, 67, 37, 14, 98, 122, 124, 183. "
        "Total head movement: 12+2+30+23+84+24+2+59 = 236 cylinders."
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'I/O scheduling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/I/O_scheduling",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="deadlock_detection",
    content=(
        "Deadlock occurs when processes are waiting for resources held by "
        "each other in a circular chain. Detection uses a resource allocation "
        "graph: if a cycle exists among processes, deadlock is present. "
        "The four Coffman conditions are: mutual exclusion, hold and wait, "
        "no preemption, and circular wait. All four must hold for deadlock."
    ),
    example=(
        "P1 holds R1, requests R2. P2 holds R2, requests R1. "
        "Cycle: P1->R2->P2->R1->P1. Deadlock detected."
    ),
    tier=5,
    domain="operating_systems",
    source="Wikipedia contributors, 'Deadlock', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deadlock",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="semaphore_trace",
    content=(
        "A semaphore is a synchronisation primitive with an integer value "
        "and two atomic operations: wait (P) decrements the value and blocks "
        "if it becomes negative; signal (V) increments the value and wakes "
        "a blocked process if any. Binary semaphores (mutex) have values 0 "
        "or 1. Counting semaphores allow values greater than 1 to control "
        "access to a pool of resources."
    ),
    example=(
        "Semaphore S=1. Thread A: wait(S) -> S=0 (enters CS). "
        "Thread B: wait(S) -> S=-1 (blocks). "
        "Thread A: signal(S) -> S=0 (B unblocks, enters CS). "
        "Thread B: signal(S) -> S=1."
    ),
    tier=5,
    domain="operating_systems",
    source="Wikipedia contributors, 'Semaphore (programming)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Semaphore_(programming)",
    prerequisites=["process_scheduling_sjf"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="virtual_memory_replacement",
    content=(
        "Page replacement algorithms decide which page to evict when a page "
        "fault occurs and no free frames are available. LRU (Least Recently "
        "Used) evicts the page that has not been used for the longest time. "
        "FIFO evicts the oldest page. Optimal (Belady's) evicts the page "
        "that will not be used for the longest future time (theoretical)."
    ),
    example=(
        "Frames=3, reference string: 7,0,1,2,0,3,0,4. "
        "LRU: faults at 7(miss),0(miss),1(miss),2(evict 7),0(hit),"
        "3(evict 1),0(hit),4(evict 2). Total faults = 6."
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'Page replacement algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Page_replacement_algorithm",
    prerequisites=["page_table_lookup"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="file_allocation",
    content=(
        "File allocation methods determine how disk blocks are assigned to "
        "files. Contiguous allocation assigns consecutive blocks (fast "
        "sequential access, external fragmentation). Linked allocation uses "
        "pointers between blocks (no fragmentation, slow random access). "
        "Indexed allocation stores block pointers in an index block "
        "(direct access, index overhead)."
    ),
    example=(
        "File of 5 blocks. Contiguous: blocks 10-14. "
        "Linked: 10->23->7->45->31. "
        "Indexed: index block 50 contains [10,23,7,45,31]."
    ),
    tier=4,
    domain="operating_systems",
    source="Wikipedia contributors, 'File allocation table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/File_allocation_table",
    prerequisites=["memory_allocation"],
))

# ---------------------------------------------------------------------------
# Distributed deep (tier 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="byzantine_generals",
    content=(
        "The Byzantine Generals Problem models consensus in the presence "
        "of faulty or malicious nodes. A system of n nodes can tolerate "
        "f Byzantine faults if and only if n >= 3f + 1. The original "
        "Lamport, Shostak, Pease algorithm achieves consensus in f+1 "
        "rounds of message exchange. Practical BFT (PBFT) reduces "
        "message complexity to O(n^2) per round."
    ),
    example=(
        "n=4 nodes, f=1 fault. 4 >= 3*1+1 = 4, so consensus is possible. "
        "With f=2: need n >= 7. With n=4 and f=2: 4 < 7, cannot guarantee consensus."
    ),
    tier=6,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Byzantine fault', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Byzantine_fault",
    prerequisites=["consensus_round"],
))

register_atom(Atom(
    atom_type="definition",
    name="quorum_systems",
    content=(
        "A quorum system is a collection of subsets (quorums) of nodes such "
        "that any two quorums intersect. For a system of n nodes, a simple "
        "majority quorum requires ceil((n+1)/2) nodes. Read and write quorums "
        "must satisfy R + W > N for consistency. Quorum intersection ensures "
        "that any read sees the most recent write."
    ),
    example=(
        "N=5 replicas. Write quorum W=3, Read quorum R=3. "
        "R+W = 6 > 5, so consistency guaranteed. "
        "Any read quorum of 3 overlaps with write quorum of 3 by at least 1 node."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Quorum (distributed computing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quorum_(distributed_computing)",
    prerequisites=["consensus_round"],
))

register_atom(Atom(
    atom_type="definition",
    name="eventual_consistency",
    content=(
        "Eventual consistency is a consistency model where, given no new "
        "updates, all replicas will eventually converge to the same value. "
        "It is weaker than strong consistency but allows higher availability. "
        "CRDTs (Conflict-free Replicated Data Types) provide eventual "
        "consistency with automatic conflict resolution. The CAP theorem "
        "states that a distributed system cannot simultaneously provide "
        "consistency, availability, and partition tolerance."
    ),
    example=(
        "G-Counter CRDT: Node A=[3,0,0], Node B=[0,2,0], Node C=[0,0,1]. "
        "Merge: max per position = [3,2,1]. Total count = 6."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Eventual consistency', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Eventual_consistency",
    prerequisites=["vector_clock_compare"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sharding_strategy",
    content=(
        "Sharding partitions data across multiple nodes to distribute load. "
        "Hash sharding uses hash(key) mod N to assign keys to shards, "
        "providing uniform distribution. Range sharding assigns contiguous "
        "key ranges to shards, supporting range queries. Consistent hashing "
        "minimises redistribution when nodes are added or removed by mapping "
        "both keys and nodes onto a hash ring."
    ),
    example=(
        "3 shards, hash sharding. Key 'user_42': hash('user_42') mod 3 = 1. "
        "Assigned to shard 1. Key 'user_99': hash('user_99') mod 3 = 0. "
        "Assigned to shard 0."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Shard (database architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shard_(database_architecture)",
    prerequisites=["modular"],
))

register_atom(Atom(
    atom_type="formula",
    name="replication_factor",
    content=(
        "The replication factor R is the number of copies of each data item "
        "stored across nodes. With R replicas and N nodes, each node stores "
        "approximately R/N of the total data. The system can tolerate up to "
        "R-1 node failures without data loss. Write availability requires "
        "at least W nodes responsive (where W is the write quorum)."
    ),
    example=(
        "N=6 nodes, R=3 replicas. Each item on 3 of 6 nodes. "
        "Can tolerate 2 node failures. Storage overhead = 3x. "
        "With W=2, R_q=2: W+R_q=4 > 3=R, so strong consistency."
    ),
    tier=4,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Replication (computing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Replication_(computing)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="log_structured_merge",
    content=(
        "A Log-Structured Merge-tree (LSM-tree) is a data structure with "
        "high write throughput. Writes go to an in-memory buffer (memtable). "
        "When full, it is flushed to disk as a sorted run (SSTable). "
        "Background compaction merges SSTables to maintain read performance. "
        "Read amplification increases with the number of levels but is "
        "bounded by bloom filters and level-based compaction."
    ),
    example=(
        "Memtable size 4MB, 4 levels. Write key 'abc': insert into memtable. "
        "Memtable full: flush to L0 as sorted SSTable. "
        "L0 has 4 SSTables: compact into L1 (merge-sort)."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Log-structured merge-tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Log-structured_merge-tree",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="gossip_protocol",
    content=(
        "Gossip protocols disseminate information through random peer-to-peer "
        "communication. Each round, a node selects a random peer and exchanges "
        "state. After O(log N) rounds, information reaches all N nodes with "
        "high probability. Gossip is robust to failures and scales well. "
        "Used in membership detection, failure detection, and aggregate "
        "computation in distributed systems."
    ),
    example=(
        "N=8 nodes, node 1 has update. Round 1: tells node 5 (2 know). "
        "Round 2: each tells 1 random peer (up to 4 know). "
        "Round 3: up to 8 know. Expected rounds to full spread: log2(8) = 3."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Gossip protocol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gossip_protocol",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="snapshot_algorithm",
    content=(
        "The Chandy-Lamport snapshot algorithm captures a consistent global "
        "state of a distributed system. An initiator saves its local state "
        "and sends marker messages on all outgoing channels. When a process "
        "receives a marker for the first time, it records its own state and "
        "begins recording messages on all other incoming channels until "
        "markers arrive on those channels."
    ),
    example=(
        "Process P1 initiates snapshot: saves state S1, sends markers to P2, P3. "
        "P2 receives marker: saves state S2, records channel P3->P2. "
        "P3 receives marker: saves state S3, records channel P2->P3. "
        "All markers received: snapshot = {S1, S2, S3, channel states}."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Chandy-Lamport algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chandy%E2%80%93Lamport_algorithm",
    prerequisites=["lamport_clock"],
))

# ---------------------------------------------------------------------------
# Compilers deep (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="constant_folding",
    content=(
        "Constant folding is a compiler optimisation that evaluates constant "
        "expressions at compile time rather than runtime. If both operands "
        "of an arithmetic operation are known constants, the compiler computes "
        "the result and replaces the expression with the constant value. "
        "Constant propagation extends this by tracking known constant values "
        "through variable assignments."
    ),
    example=(
        "Input: x = 3 + 4; y = x * 2. "
        "After folding: x = 7; y = 14. "
        "Both expressions evaluated at compile time."
    ),
    tier=4,
    domain="compilers",
    source="Wikipedia contributors, 'Constant folding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Constant_folding",
    prerequisites=["addition", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dead_code_elimination",
    content=(
        "Dead code elimination (DCE) removes code that does not affect "
        "program output. A variable is dead if its value is never used "
        "after assignment. Unreachable code (after unconditional return or "
        "in a branch that is always false) is also eliminated. DCE is "
        "typically performed after other optimisations that may create "
        "dead code."
    ),
    example=(
        "Input: x = 5; y = x + 1; z = 10; return y. "
        "z is never used, so 'z = 10' is dead code. "
        "After DCE: x = 5; y = x + 1; return y."
    ),
    tier=4,
    domain="compilers",
    source="Wikipedia contributors, 'Dead-code elimination', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dead-code_elimination",
    prerequisites=["constant_folding"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="register_allocation",
    content=(
        "Register allocation assigns program variables to CPU registers. "
        "Graph colouring is the classic approach: build an interference "
        "graph where nodes are variables and edges connect simultaneously "
        "live variables. Colour the graph with k colours (k = number of "
        "registers). If the graph is k-colourable, all variables fit in "
        "registers; otherwise, some variables are spilled to memory."
    ),
    example=(
        "Variables a, b, c. a and b are live simultaneously (edge a-b). "
        "b and c are live simultaneously (edge b-c). a and c are not. "
        "2 registers suffice: a=R1, b=R2, c=R1."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Register allocation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Register_allocation",
    prerequisites=["graph_coloring"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="instruction_selection",
    content=(
        "Instruction selection maps intermediate representation (IR) "
        "operations to target machine instructions. Tree pattern matching "
        "covers the IR expression tree with instruction tiles. Each tile "
        "has a cost; the goal is to find a minimum-cost tiling. Dynamic "
        "programming over the tree computes optimal selections bottom-up."
    ),
    example=(
        "IR: ADD(LOAD(R1), CONST(5)). Tiles: LOAD+ADD -> ADDI instruction. "
        "Cost of ADDI = 1 vs LOAD(1) + ADD(1) = 2. "
        "Optimal: select ADDI R1, 5."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Instruction selection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instruction_selection",
    prerequisites=["dead_code_elimination"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="ssa_conversion",
    content=(
        "Static Single Assignment (SSA) form is an IR property where each "
        "variable is assigned exactly once. Existing variables are split "
        "into versions (x1, x2, ...). At control flow join points, phi "
        "functions merge different versions: x3 = phi(x1, x2). SSA "
        "simplifies many optimisations (constant propagation, dead code "
        "elimination) because def-use chains are explicit."
    ),
    example=(
        "Original: x=1; if(c) x=2; y=x. "
        "SSA: x1=1; if(c) x2=2; x3=phi(x1,x2); y1=x3."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Static single-assignment form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Static_single-assignment_form",
    prerequisites=["constant_folding"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="loop_optimization",
    content=(
        "Loop optimisation techniques improve loop performance. "
        "Loop-invariant code motion (LICM) moves computations that produce "
        "the same value on every iteration out of the loop. Loop unrolling "
        "replicates the loop body to reduce branch overhead and enable "
        "instruction-level parallelism. Loop fusion combines adjacent loops "
        "with the same bounds to improve cache locality."
    ),
    example=(
        "LICM: for i in range(n): a[i] = b[i] + c (c is invariant). "
        "Optimised: t = c; for i in range(n): a[i] = b[i] + t. "
        "c is computed once instead of n times."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Loop optimization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loop_optimization",
    prerequisites=["constant_folding"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="strength_reduction",
    content=(
        "Strength reduction replaces expensive operations with cheaper "
        "equivalents. The most common case replaces multiplication inside "
        "a loop with addition: if i*k appears where i is the loop variable "
        "and k is invariant, replace with a variable incremented by k each "
        "iteration. Division by a constant power of 2 can be replaced with "
        "a right shift."
    ),
    example=(
        "Original: for i in range(n): a[i*4]. "
        "Strength reduced: j=0; for i in range(n): a[j]; j+=4. "
        "Multiplication replaced with addition."
    ),
    tier=4,
    domain="compilers",
    source="Wikipedia contributors, 'Strength reduction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Strength_reduction",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="tail_call_optimization",
    content=(
        "Tail call optimisation (TCO) reuses the current stack frame for "
        "a function call in tail position (the last action before return). "
        "Instead of pushing a new frame, the compiler replaces the current "
        "frame's arguments and jumps to the function entry. This converts "
        "tail-recursive functions into loops, preventing stack overflow "
        "for deep recursion."
    ),
    example=(
        "factorial(n, acc=1): if n==0 return acc; return factorial(n-1, n*acc). "
        "TCO: reuse frame with n=n-1, acc=n*acc, jump to start. "
        "factorial(5) uses O(1) stack instead of O(n)."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Tail call', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tail_call",
    prerequisites=["recursion"],
))
