"""Knowledge atoms for advanced economics, quantum information, and systems."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# =========================================================================
# Advanced Economics
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="cobb_douglas",
    content=(
        "The Cobb-Douglas production function is a particular functional "
        "form of the production function, widely used to represent the "
        "technological relationship between the amounts of two or more "
        "inputs and the amount of output that can be produced: "
        "Y = A * L^alpha * K^beta, where Y is total production, L is "
        "labour input, K is capital input, A is total factor productivity, "
        "and alpha, beta are output elasticities."
    ),
    example=(
        "Given A=1, L=100, K=50, alpha=0.6, beta=0.4: "
        "Y = 1 * 100^0.6 * 50^0.4 = 15.849 * 4.757 = 75.39"
    ),
    tier=5,
    domain="economics",
    source="Wikipedia contributors, 'Cobb-Douglas production function', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="elasticity",
    content=(
        "Price elasticity of demand measures how much the quantity demanded "
        "of a good responds to a change in price: "
        "E_d = (dQ/Q) / (dP/P) = (dQ/dP) * (P/Q). "
        "If |E_d| > 1, demand is elastic; if |E_d| < 1, demand is inelastic; "
        "if |E_d| = 1, demand is unit elastic."
    ),
    example=(
        "Given Q=100, P=10, dQ=-20, dP=2: "
        "E_d = (-20/2) * (10/100) = -10 * 0.1 = -1.0 (unit elastic)"
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Price elasticity of demand', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Price_elasticity_of_demand",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="auction_revenue",
    content=(
        "In a sealed-bid auction with n bidders drawing values uniformly "
        "from [0, v_max], the expected revenue from a second-price auction "
        "equals that of a first-price auction by the Revenue Equivalence "
        "Theorem: E[Revenue] = v_max * (n-1)/(n+1)."
    ),
    example=(
        "Given n=5 bidders, v_max=100: "
        "E[Revenue] = 100 * (5-1)/(5+1) = 100 * 4/6 = 66.67"
    ),
    tier=5,
    domain="economics",
    source="Wikipedia contributors, 'Revenue equivalence', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Revenue_equivalence",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="supply_demand_equilibrium",
    content=(
        "Market equilibrium occurs where the quantity demanded equals "
        "the quantity supplied. Given linear demand Q_d = a - b*P and "
        "supply Q_s = c + d*P, the equilibrium price is "
        "P* = (a - c) / (b + d) and equilibrium quantity is "
        "Q* = a - b*P* = (a*d + b*c) / (b + d)."
    ),
    example=(
        "Given Q_d = 100 - 2P, Q_s = 20 + 3P: "
        "P* = (100 - 20) / (2 + 3) = 80/5 = 16, "
        "Q* = 100 - 2*16 = 68"
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Economic equilibrium', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Economic_equilibrium",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="principle",
    name="comparative_advantage",
    content=(
        "A country has a comparative advantage in producing a good if it "
        "can produce that good at a lower opportunity cost than another "
        "country. Even if one country has an absolute advantage in all "
        "goods, trade based on comparative advantage benefits both. "
        "The opportunity cost of good X in terms of good Y is the amount "
        "of Y foregone to produce one unit of X."
    ),
    example=(
        "Country A: 10 hours for 1 wine, 5 hours for 1 cloth. "
        "Country B: 20 hours for 1 wine, 15 hours for 1 cloth. "
        "A's OC of wine = 10/5 = 2 cloth. B's OC of wine = 20/15 = 1.33 cloth. "
        "B has comparative advantage in wine (lower OC)."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Comparative advantage', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Comparative_advantage",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="utility_maximise",
    content=(
        "A consumer maximises utility U(x, y) subject to budget constraint "
        "p_x * x + p_y * y = M. Using Lagrange multipliers, the optimal "
        "bundle satisfies MU_x/p_x = MU_y/p_y (marginal utility per dollar "
        "equalised across goods). For Cobb-Douglas utility U = x^a * y^b, "
        "the optimal allocation is x* = (a/(a+b)) * M/p_x."
    ),
    example=(
        "Given U = x^0.5 * y^0.5, p_x=2, p_y=4, M=100: "
        "x* = (0.5/1.0) * 100/2 = 25, y* = (0.5/1.0) * 100/4 = 12.5, "
        "U = 25^0.5 * 12.5^0.5 = 5 * 3.536 = 17.68"
    ),
    tier=6,
    domain="economics",
    source="Wikipedia contributors, 'Utility maximization problem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Utility_maximization_problem",
    prerequisites=["lagrange_multiplier", "derivative"],
))

# =========================================================================
# Quantum Information
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="bell_state",
    content=(
        "Bell states are the four maximally entangled two-qubit quantum "
        "states: |Phi+> = (|00> + |11>)/sqrt(2), "
        "|Phi-> = (|00> - |11>)/sqrt(2), "
        "|Psi+> = (|01> + |10>)/sqrt(2), "
        "|Psi-> = (|01> - |10>)/sqrt(2). "
        "They form an orthonormal basis for the two-qubit Hilbert space "
        "and are fundamental to quantum teleportation and superdense coding."
    ),
    example=(
        "Prepare |Phi+>: apply H to |0> giving (|0>+|1>)/sqrt(2), "
        "then CNOT with second qubit |0>: "
        "(|00> + |11>)/sqrt(2). Measuring qubit 1 in |0> collapses "
        "qubit 2 to |0> with probability 1/2."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Bell state', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Bell_state",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="formula",
    name="entanglement_measure",
    content=(
        "The von Neumann entropy of the reduced density matrix quantifies "
        "bipartite entanglement: S(rho_A) = -Tr(rho_A * log2(rho_A)). "
        "For a pure bipartite state |psi>, rho_A = Tr_B(|psi><psi|). "
        "S = 0 for separable states and S = log2(d) for maximally "
        "entangled states in dimension d."
    ),
    example=(
        "For |Phi+> = (|00>+|11>)/sqrt(2): "
        "rho_A = Tr_B(|Phi+><Phi+|) = (|0><0| + |1><1|)/2 = I/2. "
        "S = -2*(1/2)*log2(1/2) = 1 ebit (maximally entangled)."
    ),
    tier=7,
    domain="quantum_information",
    source="Wikipedia contributors, 'Entropy of entanglement', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Entropy_of_entanglement",
    prerequisites=["bell_state"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="quantum_teleportation",
    content=(
        "Quantum teleportation transfers a quantum state from one party "
        "to another using shared entanglement and classical communication. "
        "Protocol: Alice and Bob share |Phi+>. Alice performs a Bell "
        "measurement on her qubit and the state to teleport, obtaining "
        "two classical bits. She sends these to Bob, who applies the "
        "corresponding Pauli correction (I, X, Z, or XZ) to recover "
        "the original state."
    ),
    example=(
        "Teleport |psi> = a|0> + b|1>. After Bell measurement, if "
        "Alice gets |Phi+>, Bob's qubit is already |psi>. If Alice "
        "gets |Psi->, Bob applies ZX to recover |psi>."
    ),
    tier=7,
    domain="quantum_information",
    source="Wikipedia contributors, 'Quantum teleportation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Quantum_teleportation",
    prerequisites=["bell_state", "quantum_gate"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="grover_step",
    content=(
        "Grover's algorithm searches an unsorted database of N items in "
        "O(sqrt(N)) queries. Each iteration applies the Grover operator "
        "G = (2|s><s| - I) * O_f, where O_f is the oracle that flips "
        "the sign of the target state, and |s> = H^n|0> is the uniform "
        "superposition. After ~pi/4 * sqrt(N) iterations, measurement "
        "yields the target with high probability."
    ),
    example=(
        "N=4 items, target |11>. Initial state |s> = (|00>+|01>+|10>+|11>)/2. "
        "After oracle: flip |11> sign. After diffusion: amplitude of |11> "
        "becomes 1.0. One iteration suffices for N=4."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Grover's algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Grover%27s_algorithm",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="qft_compute",
    content=(
        "The Quantum Fourier Transform maps |j> to "
        "(1/sqrt(N)) * sum_k exp(2*pi*i*j*k/N) |k>. "
        "For n qubits, N = 2^n. It is implemented using n Hadamard gates "
        "and n*(n-1)/2 controlled phase gates. The QFT is a key "
        "subroutine in Shor's algorithm and quantum phase estimation."
    ),
    example=(
        "QFT on 2 qubits, input |1> (j=1, N=4): "
        "output = (1/2)(|0> + exp(i*pi/2)|1> + exp(i*pi)|2> + exp(i*3pi/2)|3>) "
        "= (1/2)(|0> + i|1> - |2> - i|3>)"
    ),
    tier=7,
    domain="quantum_information",
    source="Wikipedia contributors, 'Quantum Fourier transform', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Quantum_Fourier_transform",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="error_syndrome",
    content=(
        "In quantum error correction, the error syndrome is obtained by "
        "measuring stabiliser generators without disturbing the encoded "
        "information. For the 3-qubit bit-flip code encoding |0> as |000> "
        "and |1> as |111>, the stabilisers are Z1Z2 and Z2Z3. Measuring "
        "these yields a 2-bit syndrome that identifies which qubit (if any) "
        "experienced a bit flip."
    ),
    example=(
        "3-qubit code, state |010> (bit flip on qubit 2): "
        "Z1Z2 = (-1)(+1)(-1) eigenvalue = +1 -> syndrome bit 0 = 0. Wait, "
        "Z1Z2|010> = Z1(0)*Z2(1) = (+1)(-1) = -1 -> syndrome 1. "
        "Z2Z3|010> = Z2(1)*Z3(0) = (-1)(+1) = -1 -> syndrome 1. "
        "Syndrome = (1,1) -> error on qubit 2."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Quantum error correction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="definition",
    name="density_matrix",
    content=(
        "A density matrix (density operator) rho describes the state of "
        "a quantum system, generalising pure states to mixed states. "
        "For a pure state |psi>, rho = |psi><psi|. For a mixed ensemble "
        "{p_i, |psi_i>}, rho = sum_i p_i |psi_i><psi_i|. Properties: "
        "rho is Hermitian, positive semi-definite, and Tr(rho) = 1. "
        "A state is pure iff Tr(rho^2) = 1."
    ),
    example=(
        "Mixed state: 50% |0>, 50% |1>. "
        "rho = 0.5*|0><0| + 0.5*|1><1| = [[0.5, 0], [0, 0.5]] = I/2. "
        "Tr(rho^2) = 0.25 + 0.25 = 0.5 < 1, confirming mixed state."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Density matrix', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Density_matrix",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="theorem",
    name="no_cloning_proof",
    content=(
        "The no-cloning theorem states that it is impossible to create "
        "an identical copy of an arbitrary unknown quantum state. "
        "Proof: suppose a unitary U exists such that U|psi>|0> = |psi>|psi> "
        "for all |psi>. Then for two states |a>, |b>: "
        "<a|b> = <a|<0| U^dag U |b>|0> = (<a|<a|)(|b>|b>) = <a|b>^2. "
        "This implies <a|b> = 0 or 1, so U can only clone orthogonal "
        "or identical states, not arbitrary ones."
    ),
    example=(
        "Attempt to clone |+> = (|0>+|1>)/sqrt(2): "
        "If cloning worked, |+>|+> = (|00>+|01>+|10>+|11>)/2. "
        "But CNOT(|+>|0>) = (|00>+|11>)/sqrt(2) = |Phi+> (entangled, not cloned)."
    ),
    tier=7,
    domain="quantum_information",
    source="Wikipedia contributors, 'No-cloning theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/No-cloning_theorem",
    prerequisites=["quantum_gate", "bell_state"],
))

# =========================================================================
# Systems (databases, OS, networking)
# =========================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="relational_algebra",
    content=(
        "Relational algebra provides a theoretical foundation for "
        "relational databases. Core operations: selection (sigma) filters "
        "rows by predicate, projection (pi) selects columns, union "
        "combines tuples, set difference removes tuples, Cartesian product "
        "combines all pairs, and rename (rho) changes attribute names. "
        "Join is derived: R join S = sigma(R x S)."
    ),
    example=(
        "R = {(1, Alice), (2, Bob)}. sigma(id=1)(R) = {(1, Alice)}. "
        "pi(name)(R) = {Alice, Bob}."
    ),
    tier=4,
    domain="systems",
    source="Wikipedia contributors, 'Relational algebra', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Relational_algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="normalisation",
    content=(
        "Database normalisation organises a relational database to reduce "
        "redundancy and improve integrity. 1NF: atomic values, no repeating "
        "groups. 2NF: 1NF + no partial dependencies on composite keys. "
        "3NF: 2NF + no transitive dependencies. BCNF: every determinant "
        "is a candidate key. Each normal form removes specific types of "
        "update anomalies."
    ),
    example=(
        "Table (StudentID, CourseID, CourseName, Grade). "
        "CourseName depends on CourseID (partial dependency on composite key). "
        "Not in 2NF. Fix: split into (CourseID, CourseName) and "
        "(StudentID, CourseID, Grade)."
    ),
    tier=5,
    domain="systems",
    source="Wikipedia contributors, 'Database normalization', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Database_normalization",
    prerequisites=["relational_algebra"],
))

register_atom(Atom(
    atom_type="definition",
    name="sql_equivalence",
    content=(
        "SQL equivalence determines whether two SQL queries produce the "
        "same result for all possible database instances. Two queries are "
        "equivalent if they can be transformed into the same relational "
        "algebra expression. Common equivalences: "
        "SELECT WHERE A AND B = intersect two SELECTs; "
        "subquery IN can be rewritten as JOIN; "
        "HAVING = WHERE on grouped results."
    ),
    example=(
        "Query A: SELECT name FROM emp WHERE dept='CS' AND salary>50000. "
        "Query B: SELECT name FROM emp WHERE salary>50000 INTERSECT "
        "SELECT name FROM emp WHERE dept='CS'. "
        "Both produce the same result set."
    ),
    tier=5,
    domain="systems",
    source="Wikipedia contributors, 'Query optimization', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Query_optimization",
    prerequisites=["relational_algebra"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="scheduling_algorithm",
    content=(
        "CPU scheduling algorithms determine which process runs next. "
        "FCFS: first come first served, simple but may cause convoy effect. "
        "SJF: shortest job first, optimal average waiting time but requires "
        "knowing burst times. Round Robin: time quantum rotation, fair "
        "but context switch overhead. Priority: highest priority first, "
        "may cause starvation."
    ),
    example=(
        "SJF with processes P1(burst=6), P2(burst=2), P3(burst=8), P4(burst=3): "
        "Order: P2(2), P4(3), P1(6), P3(8). "
        "Waiting times: P2=0, P4=2, P1=5, P3=11. "
        "Average = (0+2+5+11)/4 = 4.5"
    ),
    tier=4,
    domain="systems",
    source="Wikipedia contributors, 'Scheduling (computing)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Scheduling_(computing)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="page_replacement",
    content=(
        "Page replacement algorithms decide which page to evict from "
        "memory when a page fault occurs. FIFO: replace oldest page. "
        "LRU: replace least recently used page. Optimal (OPT): replace "
        "page not used for longest time in the future (theoretical). "
        "Clock: circular FIFO with reference bit approximating LRU."
    ),
    example=(
        "LRU with 3 frames, reference string 1,2,3,4,1,2,5,1,2,3,4,5: "
        "Frames after each ref: [1],[1,2],[1,2,3],[4,2,3],[4,1,3],[4,1,2],"
        "[5,1,2],[5,1,2],[5,1,2],[3,1,2],[3,4,2],[3,4,5]. "
        "Page faults = 10."
    ),
    tier=4,
    domain="systems",
    source="Wikipedia contributors, 'Page replacement algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Page_replacement_algorithm",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="subnet_calculate",
    content=(
        "IPv4 subnetting divides an IP address space into smaller networks. "
        "Given an IP address and CIDR notation /n, the subnet mask has n "
        "ones followed by (32-n) zeros. Network address = IP AND mask. "
        "Broadcast = network OR (NOT mask). "
        "Number of hosts = 2^(32-n) - 2 (excluding network and broadcast)."
    ),
    example=(
        "IP 192.168.1.100/26: mask = 255.255.255.192. "
        "Network = 192.168.1.64, broadcast = 192.168.1.127. "
        "Hosts = 2^6 - 2 = 62."
    ),
    tier=4,
    domain="systems",
    source="Wikipedia contributors, 'Subnetwork', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Subnetwork",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="consistent_hashing",
    content=(
        "Consistent hashing maps both keys and nodes to positions on a "
        "hash ring (typically [0, 2^32)). A key is assigned to the first "
        "node found clockwise from the key's position. When a node is "
        "added or removed, only K/n keys need to be remapped on average "
        "(K = total keys, n = total nodes), compared to nearly all keys "
        "in traditional hashing."
    ),
    example=(
        "Ring [0, 100). Nodes at positions 10, 40, 70. "
        "Key hashes to 55 -> assigned to node at 70 (first clockwise). "
        "If node 70 is removed, key 55 -> node at 10 (wraps around)."
    ),
    tier=5,
    domain="systems",
    source="Wikipedia contributors, 'Consistent hashing', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Consistent_hashing",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="vector_clock_update",
    content=(
        "Vector clocks are used in distributed systems to capture causal "
        "ordering of events. Each process i maintains a vector VC[i] of "
        "logical timestamps. Rules: (1) before each event at process i, "
        "increment VC[i][i]. (2) When sending a message, attach the current "
        "vector. (3) On receiving, merge: VC[i][j] = max(VC[i][j], "
        "VC_msg[j]) for all j, then increment VC[i][i]."
    ),
    example=(
        "3 processes, all start at [0,0,0]. "
        "P1 sends msg: P1=[1,0,0]. "
        "P2 receives: merge max([0,0,0],[1,0,0])=[1,0,0], increment P2: [1,1,0]. "
        "P2 sends to P3: P3 receives [1,1,0], merge, increment: [1,1,1]."
    ),
    tier=5,
    domain="systems",
    source="Wikipedia contributors, 'Vector clock', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Vector_clock",
    prerequisites=[],
))
