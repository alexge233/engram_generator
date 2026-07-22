"""Knowledge atoms for algorithms and chemistry domains.

Covers sorting algorithms, string matching, graph algorithms,
dynamic programming, and advanced chemistry (electrochemistry,
thermodynamics, equilibrium).
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Algorithms -- sorting & searching (tiers 3-4)
# =========================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="binary_search_trace",
    content=(
        "Binary search finds a target value in a sorted array by repeatedly "
        "dividing the search interval in half. At each step, compare the "
        "target to the middle element: if equal, return; if less, search "
        "the left half; if greater, search the right half. Time complexity "
        "O(log n), space O(1)."
    ),
    example=(
        "Array [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], target=23: "
        "lo=0, hi=9, mid=4 (16<23) -> lo=5, hi=9, mid=7 (56>23) -> "
        "lo=5, hi=6, mid=5 (23=23) -> found at index 5"
    ),
    tier=3,
    domain="algorithms",
    source="Wikipedia contributors, 'Binary search algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_algorithm",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="counting_sort",
    content=(
        "Counting sort is a non-comparison-based sorting algorithm that "
        "counts the number of occurrences of each distinct element. It "
        "then computes prefix sums to determine the position of each "
        "element in the output. Time complexity O(n + k) where k is "
        "the range of input values. Stable sort."
    ),
    example=(
        "Input [4, 2, 2, 8, 3, 3, 1]: count=[0,1,2,2,1,0,0,0,1], "
        "prefix=[0,1,3,5,6,6,6,6,7], output=[1,2,2,3,3,4,8]"
    ),
    tier=3,
    domain="algorithms",
    source="Wikipedia contributors, 'Counting sort', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Counting_sort",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="merge_sort_trace",
    content=(
        "Merge sort is a divide-and-conquer algorithm that recursively "
        "splits the array into halves until single elements remain, then "
        "merges sorted halves back together. Stable sort with guaranteed "
        "O(n log n) time complexity and O(n) auxiliary space."
    ),
    example=(
        "Input [38, 27, 43, 3, 9, 82, 10]: "
        "split -> [38,27,43,3] [9,82,10] -> ... -> "
        "merge [27,38] [3,43] -> [3,27,38,43], "
        "merge [9,82] [10] -> [9,10,82], "
        "merge [3,27,38,43] [9,10,82] -> [3,9,10,27,38,43,82]"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Merge sort', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Merge_sort",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="quicksort_partition",
    content=(
        "Quicksort selects a pivot element and partitions the array into "
        "elements less than and greater than the pivot (Lomuto or Hoare "
        "partition scheme). It then recursively sorts both partitions. "
        "Average O(n log n), worst case O(n^2). In-place, not stable."
    ),
    example=(
        "Input [10, 80, 30, 90, 40, 50, 70], pivot=70 (Lomuto): "
        "partition -> [10, 30, 40, 50, 70, 90, 80], pivot at index 4"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Quicksort', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quicksort",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="heap_sort_trace",
    content=(
        "Heap sort builds a max-heap from the input array, then repeatedly "
        "extracts the maximum element and places it at the end. Uses the "
        "sift-down operation to maintain the heap property. O(n log n) "
        "time, O(1) auxiliary space. Not stable."
    ),
    example=(
        "Input [4, 10, 3, 5, 1]: build max-heap -> [10, 5, 3, 4, 1], "
        "extract 10 -> [5, 4, 3, 1, |10], extract 5 -> [4, 1, 3, |5, 10], "
        "... -> [1, 3, 4, 5, 10]"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Heapsort', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heapsort",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="radix_sort",
    content=(
        "Radix sort processes elements digit by digit, from least "
        "significant to most significant (LSD) or vice versa (MSD). "
        "Uses a stable sort (typically counting sort) as a subroutine "
        "for each digit position. Time O(d*(n+k)) where d is the "
        "number of digits and k is the radix."
    ),
    example=(
        "Input [170, 45, 75, 90, 802, 24, 2, 66]: "
        "by ones: [170,90,802,2,24,45,75,66], "
        "by tens: [802,2,24,45,66,170,75,90], "
        "by hundreds: [2,24,45,66,75,90,170,802]"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Radix sort', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radix_sort",
    prerequisites=["sorting", "counting_sort"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hash_chaining",
    content=(
        "Hash table with separate chaining resolves collisions by storing "
        "all elements that hash to the same bucket in a linked list. "
        "Insert, search, and delete are O(1) average, O(n) worst case. "
        "Load factor alpha = n/m where n is elements and m is buckets."
    ),
    example=(
        "Table size m=7, h(k)=k mod 7. Insert 50,700,76,85,92,73,101: "
        "bucket 0: [50,700], bucket 1: [85,92], bucket 3: [73,101], "
        "bucket 6: [76]. Search 73: h(73)=3, chain [73,101], found."
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Hash table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hash_table",
    prerequisites=["modular"],
))

# =========================================================================
# Algorithms -- graph & string (tier 5)
# =========================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="dijkstra_trace",
    content=(
        "Dijkstra's algorithm finds the shortest path from a source "
        "vertex to all other vertices in a weighted graph with non-negative "
        "edge weights. Uses a priority queue to greedily select the "
        "unvisited vertex with smallest tentative distance. Time "
        "O((V+E) log V) with a binary heap."
    ),
    example=(
        "Graph: A->B(1), A->C(4), B->C(2), B->D(5), C->D(1). "
        "Source A: dist={A:0,B:1,C:3,D:4}. "
        "Path A->D: A->B->C->D (cost 4)"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Dijkstra's algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="kruskal_trace",
    content=(
        "Kruskal's algorithm finds a minimum spanning tree by sorting "
        "all edges by weight, then adding edges in order if they don't "
        "create a cycle (checked via union-find). Time O(E log E). "
        "Produces a forest that spans all connected components."
    ),
    example=(
        "Edges: (A-B,4),(A-C,2),(B-C,1),(B-D,5),(C-D,3). "
        "Sorted: (B-C,1),(A-C,2),(C-D,3),(A-B,4),(B-D,5). "
        "Add B-C(1), A-C(2), C-D(3). Skip A-B(cycle), B-D(cycle). "
        "MST weight = 6"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Kruskal's algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kruskal%27s_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dp_knapsack_trace",
    content=(
        "The 0/1 knapsack problem: given n items with weights and values "
        "and a capacity W, find the subset maximising total value without "
        "exceeding capacity. Dynamic programming solution builds a table "
        "dp[i][w] = max value using items 1..i with capacity w. "
        "Time O(nW), space O(nW) or O(W) with optimisation."
    ),
    example=(
        "Items: (w=1,v=6),(w=2,v=10),(w=3,v=12), capacity=5. "
        "dp[3][5]=22 (take items 1 and 3: weight=4, value=18; "
        "or items 2 and 3: weight=5, value=22). Optimal: items 2+3, value=22"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Knapsack problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Knapsack_problem",
    prerequisites=["coin_change"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="kmp_search",
    content=(
        "The Knuth-Morris-Pratt algorithm searches for a pattern in text "
        "by precomputing a failure function (partial match table) that "
        "indicates how far to shift the pattern on a mismatch, avoiding "
        "redundant comparisons. Time O(n+m) where n is text length and "
        "m is pattern length."
    ),
    example=(
        "Pattern 'ABAB', text 'ABABCABABD': "
        "failure function [0,0,1,2]. "
        "Match at position 0: ABAB matches. "
        "Shift by 2 (not 4). Match at position 4: ABAB matches."
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Knuth-Morris-Pratt algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm",
    prerequisites=["binary_search_trace"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="rabin_karp",
    content=(
        "Rabin-Karp uses a rolling hash to quickly filter candidate "
        "positions for pattern matching. Compute hash of the pattern and "
        "rolling hash of each text window; only compare characters when "
        "hashes match. Average O(n+m), worst O(nm). Supports multiple "
        "pattern search."
    ),
    example=(
        "Pattern 'abc' (hash=6), text 'aabcabc', base=26, mod=101: "
        "window 'aab' hash=3 (no match), 'abc' hash=6 (match, verify), "
        "found at position 1 and position 4"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Rabin-Karp algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm",
    prerequisites=["hash_chaining"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="suffix_array",
    content=(
        "A suffix array is a sorted array of all suffixes of a string, "
        "represented by their starting indices. Enables efficient substring "
        "search via binary search in O(m log n) time. Can be constructed "
        "in O(n log n) or O(n) time. Often paired with an LCP array."
    ),
    example=(
        "String 'banana$': suffixes sorted: "
        "$ (6), a$ (5), ana$ (3), anana$ (1), banana$ (0), "
        "na$ (4), nana$ (2). SA = [6,5,3,1,0,4,2]"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Suffix array', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Suffix_array",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="matrix_chain_dp",
    content=(
        "Matrix chain multiplication determines the optimal parenthesisation "
        "of a chain of matrices to minimise total scalar multiplications. "
        "DP recurrence: m[i,j] = min over k of (m[i,k] + m[k+1,j] + "
        "p_{i-1}*p_k*p_j). Time O(n^3), space O(n^2)."
    ),
    example=(
        "Matrices A1(10x30), A2(30x5), A3(5x60): "
        "m[1,2] = 10*30*5 = 1500, m[2,3] = 30*5*60 = 9000, "
        "m[1,3] = min(1500 + 10*5*60, 9000 + 10*30*60) = min(4500, 27000) = 4500. "
        "Optimal: (A1*A2)*A3"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Matrix chain multiplication', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matrix_chain_multiplication",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="longest_palindrome",
    content=(
        "Finding the longest palindromic substring in a string. Manacher's "
        "algorithm solves this in O(n) time by exploiting palindrome "
        "symmetry. The naive approach expands around each center in O(n^2). "
        "A palindrome reads the same forwards and backwards."
    ),
    example=(
        "String 'babad': expand around each center: "
        "b(1), a(1), bab(3), a(1), d(1), ba(2), ab(2), ba(2), ad(2). "
        "Longest: 'bab' (length 3) or 'aba' (length 3)"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Longest palindromic substring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Longest_palindromic_substring",
    prerequisites=["palindrome_check"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="topk_quickselect",
    content=(
        "Quickselect finds the k-th smallest element in an unordered list. "
        "Like quicksort, it partitions around a pivot but only recurses "
        "into the side containing the target. Average O(n), worst O(n^2). "
        "The median-of-medians variant guarantees O(n) worst case."
    ),
    example=(
        "Array [3,2,1,5,6,4], k=2 (2nd largest = 5): "
        "pivot=4, partition [3,2,1] | 4 | [5,6]. "
        "k=2 largest is in right partition. pivot=5, [6]|5. "
        "Answer: 5"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Quickselect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quickselect",
    prerequisites=["quicksort_partition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="tarjan_scc",
    content=(
        "Tarjan's algorithm finds all strongly connected components in a "
        "directed graph using a single DFS. It maintains a stack and "
        "assigns each node an index and lowlink value. When a node's "
        "lowlink equals its index, it is the root of an SCC. Time O(V+E)."
    ),
    example=(
        "Graph: 0->1, 1->2, 2->0, 1->3, 3->4, 4->3. "
        "SCCs: {0,1,2} (cycle), {3,4} (cycle). "
        "DFS from 0: stack [0,1,2] -> SCC {0,1,2}, then [3,4] -> SCC {3,4}"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Tarjan's strongly connected components algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm",
    prerequisites=["topo_sort"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="a_star_search",
    content=(
        "A* search finds the shortest path using a heuristic function "
        "h(n) that estimates the cost from node n to the goal. It "
        "expands nodes with lowest f(n) = g(n) + h(n), where g(n) is "
        "the cost from start. Optimal if h is admissible (never overestimates). "
        "Time depends on heuristic quality."
    ),
    example=(
        "Grid 4x4, start (0,0), goal (3,3), h=Manhattan distance. "
        "f(0,0) = 0+6 = 6. Expand (0,0) -> (1,0) f=1+5=6, (0,1) f=1+5=6. "
        "Shortest path length = 6 (no obstacles)"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'A* search algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/A*_search_algorithm",
    prerequisites=["dijkstra_trace"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="edit_distance_variants",
    content=(
        "Edit distance (Levenshtein distance) measures the minimum number "
        "of single-character edits (insertions, deletions, substitutions) "
        "to transform one string into another. DP recurrence: "
        "dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost). "
        "Variants include Damerau-Levenshtein (adds transposition)."
    ),
    example=(
        "Strings 'kitten' -> 'sitting': "
        "k->s (sub), e->i (sub), n->ng (insert 'g'). "
        "Edit distance = 3"
    ),
    tier=5,
    domain="algorithms",
    source="Wikipedia contributors, 'Edit distance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Edit_distance",
    prerequisites=["edit_distance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="interval_scheduling",
    content=(
        "Interval scheduling maximisation: given a set of intervals "
        "[s_i, f_i], find the maximum number of non-overlapping intervals. "
        "Greedy solution: sort by finish time, greedily select the earliest "
        "finishing interval that doesn't overlap. Optimal in O(n log n)."
    ),
    example=(
        "Intervals: [1,4], [3,5], [0,6], [5,7], [3,9], [5,9], [6,10], "
        "[8,11], [8,12], [2,14], [12,16]. "
        "Greedy: select [1,4], [5,7], [8,11], [12,16]. Maximum = 4"
    ),
    tier=4,
    domain="algorithms",
    source="Wikipedia contributors, 'Interval scheduling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Interval_scheduling",
    prerequisites=["sorting"],
))


# =========================================================================
# Chemistry -- advanced (tiers 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="ionic_strength",
    content=(
        "Ionic strength I of a solution is a measure of the total "
        "concentration of ions, accounting for their charge: "
        "I = 0.5 * sum(c_i * z_i^2), where c_i is the molar "
        "concentration and z_i is the charge of ion i. Important "
        "for Debye-Huckel theory and activity coefficients."
    ),
    example=(
        "0.1 M NaCl: I = 0.5*(0.1*1^2 + 0.1*1^2) = 0.1 M. "
        "0.1 M CaCl2: I = 0.5*(0.1*2^2 + 0.2*1^2) = 0.5*(0.4+0.2) = 0.3 M"
    ),
    tier=4,
    domain="chemistry",
    source="Wikipedia contributors, 'Ionic strength', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ionic_strength",
    prerequisites=["molarity"],
))

register_atom(Atom(
    atom_type="formula",
    name="activation_energy",
    content=(
        "The Arrhenius equation relates the rate constant k to temperature: "
        "k = A * exp(-Ea/(R*T)), where A is the pre-exponential factor, "
        "Ea is the activation energy, R = 8.314 J/(mol*K), and T is "
        "temperature in Kelvin. Taking ln: ln(k) = ln(A) - Ea/(R*T). "
        "Two-point form: ln(k2/k1) = (Ea/R)*(1/T1 - 1/T2)."
    ),
    example=(
        "k1 = 0.05 s^-1 at T1 = 300K, k2 = 0.50 s^-1 at T2 = 350K: "
        "Ea = R * ln(k2/k1) / (1/T1 - 1/T2) = "
        "8.314 * ln(10) / (1/300 - 1/350) = "
        "8.314 * 2.303 / (4.76e-4) = 40,200 J/mol = 40.2 kJ/mol"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Arrhenius equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arrhenius_equation",
    prerequisites=["arrhenius"],
))

register_atom(Atom(
    atom_type="formula",
    name="buffer_henderson",
    content=(
        "The Henderson-Hasselbalch equation relates pH of a buffer "
        "solution to pKa and the ratio of conjugate base to weak acid: "
        "pH = pKa + log10([A-]/[HA]). Valid when the buffer ratio "
        "is between 0.1 and 10 (pH within 1 unit of pKa)."
    ),
    example=(
        "Acetic acid buffer: pKa = 4.76, [CH3COO-] = 0.1 M, "
        "[CH3COOH] = 0.05 M: pH = 4.76 + log(0.1/0.05) = "
        "4.76 + log(2) = 4.76 + 0.301 = 5.061"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Henderson-Hasselbalch equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Henderson%E2%80%93Hasselbalch_equation",
    prerequisites=["ph_calculation", "equilibrium_constant"],
))

register_atom(Atom(
    atom_type="formula",
    name="galvanic_cell",
    content=(
        "A galvanic (voltaic) cell generates electrical energy from "
        "spontaneous redox reactions. The cell potential is: "
        "E_cell = E_cathode - E_anode (using standard reduction potentials). "
        "The Nernst equation gives non-standard conditions: "
        "E = E0 - (RT/nF) * ln(Q)."
    ),
    example=(
        "Zn/Cu cell: E0(Cu2+/Cu) = +0.34V, E0(Zn2+/Zn) = -0.76V. "
        "E_cell = 0.34 - (-0.76) = 1.10 V. "
        "Zn is anode (oxidised), Cu is cathode (reduced)"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Galvanic cell', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Galvanic_cell",
    prerequisites=["nernst_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="faraday_electrolysis",
    content=(
        "Faraday's laws of electrolysis: the mass of substance deposited "
        "at an electrode is proportional to the charge passed. "
        "m = (M * I * t) / (n * F), where M is molar mass, I is current, "
        "t is time, n is number of electrons transferred, and "
        "F = 96485 C/mol is Faraday's constant."
    ),
    example=(
        "Electroplate Cu (M=63.55, n=2): I=2A, t=3600s (1 hour): "
        "m = (63.55 * 2 * 3600) / (2 * 96485) = 457560 / 192970 = 2.37 g"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Faraday's laws of electrolysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Faraday%27s_laws_of_electrolysis",
    prerequisites=["molarity"],
))

register_atom(Atom(
    atom_type="formula",
    name="born_haber_cycle",
    content=(
        "The Born-Haber cycle applies Hess's law to determine lattice "
        "energy of an ionic compound by summing the enthalpy changes: "
        "sublimation, ionisation, dissociation, electron affinity, and "
        "formation. The cycle: dH_f = dH_sub + dH_IE + 0.5*dH_diss + "
        "dH_EA + U_lattice."
    ),
    example=(
        "NaCl: dH_f=-411, dH_sub(Na)=108, IE(Na)=496, "
        "0.5*dH_diss(Cl2)=122, EA(Cl)=-349. "
        "U_lattice = -411 - 108 - 496 - 122 + 349 = -788 kJ/mol"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Born-Haber cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Born%E2%80%93Haber_cycle",
    prerequisites=["gibbs_spontaneity"],
))

register_atom(Atom(
    atom_type="formula",
    name="solubility_ph",
    content=(
        "The solubility of sparingly soluble salts depends on pH when "
        "the anion is the conjugate base of a weak acid. For MA where "
        "A- is basic: Ksp = s * (s + [H+]*s/Ka). At low pH, increased "
        "H+ consumes A- via HA formation, increasing solubility."
    ),
    example=(
        "CaF2, Ksp = 3.9e-11, Ka(HF) = 6.8e-4, pH=3: "
        "[H+]=1e-3, alpha = 1 + [H+]/Ka = 1 + 1e-3/6.8e-4 = 2.47. "
        "s = (Ksp * alpha^2 / 4)^(1/3) = (3.9e-11 * 6.1 / 4)^(1/3) = "
        "3.9e-4 M (vs 2.1e-4 M at neutral pH)"
    ),
    tier=6,
    domain="chemistry",
    source="Wikipedia contributors, 'Solubility equilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Solubility_equilibrium",
    prerequisites=["equilibrium_constant", "ph_calculation"],
))

register_atom(Atom(
    atom_type="formula",
    name="reaction_mechanism_rate",
    content=(
        "For a multi-step reaction mechanism, the overall rate law is "
        "determined by the rate-determining step (slowest step). If a "
        "pre-equilibrium exists, intermediates are expressed in terms of "
        "reactants using the equilibrium constant of the fast step. "
        "The steady-state approximation sets d[intermediate]/dt = 0."
    ),
    example=(
        "Mechanism: (1) A + B <-> C (fast, K1), (2) C -> D (slow, k2). "
        "Rate = k2[C] = k2*K1*[A][B]. Overall: rate = k_obs*[A][B] "
        "where k_obs = k2*K1"
    ),
    tier=6,
    domain="chemistry",
    source="Wikipedia contributors, 'Rate-determining step', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rate-determining_step",
    prerequisites=["rate_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="complexation_equilibrium",
    content=(
        "Metal-ligand complexation equilibria are described by stepwise "
        "formation constants K_n: M + L <-> ML (K1), ML + L <-> ML2 (K2), "
        "etc. The overall formation constant beta_n = K1*K2*...*Kn. "
        "The fraction of each species depends on [L] and the K values."
    ),
    example=(
        "Cu2+ with NH3: K1=1e4, K2=2e3, K3=5e2, K4=1e2. "
        "beta_2 = K1*K2 = 2e7. At [NH3]=0.1M: "
        "[Cu(NH3)2^2+]/[Cu^2+] = beta_2 * [NH3]^2 = 2e7 * 0.01 = 2e5"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Stability constants of complexes', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stability_constants_of_complexes",
    prerequisites=["equilibrium_constant"],
))

register_atom(Atom(
    atom_type="formula",
    name="thermodynamic_cycle",
    content=(
        "Thermodynamic cycles (Carnot, Otto, Diesel, Rankine) are closed "
        "paths on a PV or TS diagram. The net work equals the enclosed "
        "area. Efficiency eta = W_net / Q_in = 1 - Q_out/Q_in. "
        "Hess's law: enthalpy change is path-independent, so "
        "dH_cycle = sum of all steps = 0."
    ),
    example=(
        "Hess's law: C(s) + O2(g) -> CO2(g), dH = -393.5 kJ. "
        "CO(g) + 0.5*O2(g) -> CO2(g), dH = -283.0 kJ. "
        "Therefore: C(s) + 0.5*O2(g) -> CO(g), "
        "dH = -393.5 - (-283.0) = -110.5 kJ"
    ),
    tier=5,
    domain="chemistry",
    source="Wikipedia contributors, 'Hess's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hess%27s_law",
    prerequisites=["gibbs_spontaneity"],
))
