"""Knowledge atoms for data structures ext, graphs ext, economics ext,
topology deep, logic ext, CS theory ext, PDE ext, inorganic chemistry ext,
and general chemistry ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Data Structures Ext ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="bst_insert",
    content="Binary search tree insertion: compare key with current node, go left if smaller, right if larger, insert as leaf. Time O(h) where h is height.",
    example="Insert 5 into BST [3,7,1,4]: compare 5>3 (right), 5<7 (left), 5>4 (right). Node 5 becomes right child of 4.",
    tier=3, domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree",
))

register_atom(Atom(
    atom_type="algorithm", name="bst_delete",
    content="BST deletion: if leaf, remove. If one child, replace with child. If two children, replace with in-order successor (smallest in right subtree), then delete successor.",
    example="Delete 3 from BST [3,1,7,4]: 3 has two children. In-order successor is 4. Replace 3 with 4, delete old 4.",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree#Deletion",
))

register_atom(Atom(
    atom_type="algorithm", name="avl_rotation",
    content="AVL tree rotation restores balance when |balance_factor| > 1. Left rotation for right-heavy, right rotation for left-heavy. Double rotations for zig-zag cases.",
    example="Right-heavy node (bf=-2), right child bf=-1: single left rotation. Move right child up, current node becomes its left child.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'AVL tree', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/AVL_tree",
))

register_atom(Atom(
    atom_type="algorithm", name="red_black_insert",
    content="Red-black tree insert: insert as red leaf, then fix violations. Cases: uncle red (recolor), uncle black + zig-zag (rotate+recolor), uncle black + straight (rotate+recolor). Root always black.",
    example="Insert 4 (red) as right child of 3 (red), uncle 7 is red: recolor parent 3 and uncle 7 black, grandparent 5 red. If 5 is root, recolor black.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'Red-black tree', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Red%E2%80%93black_tree",
))

register_atom(Atom(
    atom_type="algorithm", name="b_tree_insert",
    content="B-tree of order m: each node has at most m children and m-1 keys. Insert into leaf; if full (m-1 keys), split into two nodes and push median up. Splitting may propagate to root.",
    example="B-tree order 3, insert 8 into full leaf [5,7]: split at median 7, left=[5], right=[8], push 7 up to parent.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'B-tree', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/B-tree",
))

register_atom(Atom(
    atom_type="algorithm", name="trie_operations",
    content="A trie (prefix tree) stores strings character by character. Insert: traverse/create nodes for each character, mark end. Search: traverse nodes, return true if end marker found. O(m) for string of length m.",
    example="Insert 'cat': root->c->a->t(end). Search 'car': root->c->a->r not found, return false.",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Trie', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Trie",
))

register_atom(Atom(
    atom_type="algorithm", name="skip_list",
    content="A skip list is a probabilistic data structure with O(log n) search. Multiple layers of linked lists; each element promoted to next layer with probability p (typically 1/2).",
    example="Search 7 in skip list: start at top layer, go right until > 7, drop down, repeat. Levels: L2:[1->9], L1:[1->5->9], L0:[1->3->5->7->9]. Found at L0.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'Skip list', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Skip_list",
))

register_atom(Atom(
    atom_type="algorithm", name="bloom_filter",
    content="A Bloom filter is a probabilistic set membership test using k hash functions and a bit array of size m. Insert: set k bit positions. Query: check all k positions. False positives possible, false negatives impossible. Optimal k = (m/n)*ln(2).",
    example="m=10 bits, k=3 hash functions, insert 'hello': h1=2, h2=5, h3=8. Set bits [2,5,8]. Query 'world': h1=1, h2=5, h3=7. Bit 1 is 0, so 'world' is NOT in set.",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Bloom filter', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Bloom_filter",
))

# ── Graphs Ext ───────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="bellman_ford",
    content="Bellman-Ford finds shortest paths from a source in a weighted graph, handling negative edges. Relax all edges |V|-1 times. Detects negative cycles on the |V|th iteration.",
    example="Graph: A->B(4), A->C(5), B->C(-3). After relaxation: d(A)=0, d(B)=4, d(C)=1 (via A->B->C, 4+(-3)=1).",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Bellman-Ford algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm",
))

register_atom(Atom(
    atom_type="algorithm", name="floyd_warshall",
    content="Floyd-Warshall computes all-pairs shortest paths in O(V^3). d[i][j] = min(d[i][j], d[i][k] + d[k][j]) for each intermediate vertex k.",
    example="3 vertices, edges: 1->2(3), 2->3(1), 1->3(6). After k=2: d[1][3] = min(6, 3+1) = 4.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Floyd-Warshall algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm",
))

register_atom(Atom(
    atom_type="algorithm", name="articulation_point",
    content="An articulation point (cut vertex) is a vertex whose removal disconnects the graph. Found via DFS: vertex u is an articulation point if it has a child v with no back edge to an ancestor of u. Uses low[] and disc[] arrays.",
    example="Graph: A-B, B-C, C-D, B-D. Articulation points: {B} (removing B disconnects A from {C,D}).",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Biconnected component', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Biconnected_component",
))

register_atom(Atom(
    atom_type="algorithm", name="strongly_connected",
    content="Strongly connected components (SCCs) of a directed graph are maximal subsets where every vertex is reachable from every other. Kosaraju's algorithm: DFS to get finish order, transpose graph, DFS in reverse finish order.",
    example="Directed graph: A->B, B->C, C->A, C->D. SCCs: {A,B,C} and {D}.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Strongly connected component', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Strongly_connected_component",
))

register_atom(Atom(
    atom_type="algorithm", name="graph_matching",
    content="A matching in a graph is a set of edges with no shared vertices. Maximum matching: largest such set. In bipartite graphs, found via augmenting paths (Hopcroft-Karp, O(E*sqrt(V))).",
    example="Bipartite graph: {A,B,C} to {1,2,3}, edges A-1, A-2, B-1, C-3. Maximum matching: {A-2, B-1, C-3} (size 3).",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Matching (graph theory)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Matching_(graph_theory)",
))

register_atom(Atom(
    atom_type="algorithm", name="network_flow_detail",
    content="Max-flow min-cut theorem: the maximum flow from source to sink equals the minimum cut capacity. Ford-Fulkerson: find augmenting paths in residual graph, add flow along path, repeat until no path exists.",
    example="Network: s->A(10), s->B(5), A->B(3), A->t(7), B->t(8). Max flow = 12: s->A->t(7), s->B->t(5).",
    tier=6, domain="graph_theory",
    source="Wikipedia contributors, 'Maximum flow problem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Maximum_flow_problem",
))

register_atom(Atom(
    atom_type="algorithm", name="topological_sort_dfs",
    content="Topological sort of a DAG: DFS-based, push vertex to stack after all descendants visited. Result is reverse post-order. Only exists for directed acyclic graphs.",
    example="DAG: A->B, A->C, B->D, C->D. DFS from A: visit B->D (push D, push B), visit C (push C), push A. Order: A, C, B, D.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Topological sorting', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Topological_sorting",
))

register_atom(Atom(
    atom_type="algorithm", name="graph_coloring_greedy",
    content="Greedy graph coloring: process vertices in order, assign each the smallest color not used by its neighbours. Uses at most Delta+1 colors where Delta is max degree. Not always optimal.",
    example="Graph: A-B, B-C, A-C (triangle). Order A,B,C: A=1, B=2 (A is neighbour), C=3 (A,B are neighbours). Chromatic number = 3.",
    tier=4, domain="graph_theory",
    source="Wikipedia contributors, 'Greedy coloring', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Greedy_coloring",
))

# ── Economics Ext ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="marginal_analysis",
    content="Marginal analysis: the additional benefit or cost of one more unit. Marginal cost MC = dTC/dQ, marginal revenue MR = dTR/dQ. Profit maximised where MR = MC.",
    example="TC = 100 + 5Q + 0.1Q^2, TR = 20Q. MC = 5 + 0.2Q, MR = 20. Set MR=MC: 20 = 5 + 0.2Q, Q = 75.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Marginal cost', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Marginal_cost",
))

register_atom(Atom(
    atom_type="formula", name="consumer_surplus",
    content="Consumer surplus is the area between the demand curve and the market price. CS = integral from 0 to Q* of [D(Q) - P*] dQ, where D(Q) is the demand function and P* is the market price.",
    example="Demand: P = 100 - 2Q, market price P* = 40. Q* = (100-40)/2 = 30. CS = 0.5 * 30 * (100-40) = 900.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Consumer surplus', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Economic_surplus",
))

register_atom(Atom(
    atom_type="formula", name="multiplier_effect",
    content="The fiscal multiplier: a change in government spending dG produces a change in GDP of dY = dG / (1 - MPC), where MPC is the marginal propensity to consume.",
    example="MPC = 0.8, dG = 100. Multiplier = 1/(1-0.8) = 5. dY = 100 * 5 = 500.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Fiscal multiplier', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fiscal_multiplier",
))

register_atom(Atom(
    atom_type="formula", name="exchange_rate",
    content="Exchange rate conversion: Amount_B = Amount_A * Rate_AB. Purchasing power parity: Rate = Price_domestic / Price_foreign. Real exchange rate: RER = e * P_foreign / P_domestic.",
    example="USD/EUR = 1.10, convert 500 EUR: 500 * 1.10 = 550 USD.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Exchange rate', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Exchange_rate",
))

register_atom(Atom(
    atom_type="formula", name="inflation_real_rate",
    content="Fisher equation: (1+i) = (1+r)(1+pi), approximately i = r + pi, where i is nominal rate, r is real rate, pi is inflation rate.",
    example="Nominal rate i = 6%, inflation pi = 2%. Real rate r = i - pi = 6% - 2% = 4% (approximate).",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Fisher equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fisher_equation",
))

register_atom(Atom(
    atom_type="formula", name="production_function",
    content="Cobb-Douglas production function: Y = A * K^alpha * L^(1-alpha), where Y is output, A is total factor productivity, K is capital, L is labour, alpha is capital share.",
    example="A=1, K=100, L=200, alpha=0.3: Y = 1 * 100^0.3 * 200^0.7 = 3.981 * 47.59 = 189.5.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Cobb-Douglas production function', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function",
))

register_atom(Atom(
    atom_type="definition", name="game_theory_market",
    content="Game-theoretic market models: Cournot (firms choose quantities simultaneously), Bertrand (firms choose prices), Stackelberg (sequential quantity choice). Nash equilibrium determines market outcome.",
    example="Cournot duopoly: P = 100 - Q, MC = 10. Each firm: qi = (100-10)/(2+1) = 30. P = 100 - 60 = 40.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Cournot competition', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Cournot_competition",
))

register_atom(Atom(
    atom_type="formula", name="time_value_money",
    content="Future value: FV = PV * (1+r)^n. Present value: PV = FV / (1+r)^n. Annuity PV: PV = PMT * [1 - (1+r)^{-n}] / r.",
    example="PV = 1000, r = 5%, n = 10: FV = 1000 * 1.05^10 = 1000 * 1.6289 = 1628.89.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Time value of money', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Time_value_of_money",
))

# ── Topology Deep ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition", name="path_connected",
    content="A space X is path-connected if for any two points a, b in X, there exists a continuous function f: [0,1] -> X with f(0)=a and f(1)=b. Path-connected implies connected but not conversely.",
    example="R^n \\ {0} for n>=2 is path-connected: any two points can be connected by a path avoiding the origin. R \\ {0} is NOT path-connected.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Connected space', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Connected_space#Path_connectedness",
))

register_atom(Atom(
    atom_type="definition", name="product_topology",
    content="The product topology on X x Y has basis {U x V : U open in X, V open in Y}. For infinite products, use the box topology (all opens) or product topology (finitely many non-trivial factors).",
    example="R x R with product topology = R^2 with standard topology. Open sets are unions of open rectangles (a,b) x (c,d).",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Product topology', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Product_topology",
))

register_atom(Atom(
    atom_type="definition", name="quotient_space_compute",
    content="A quotient space X/~ identifies points related by ~. The quotient topology makes the projection continuous. Examples: [0,1]/(0~1) = S^1, R/Z = S^1, D^2/S^1 = S^2.",
    example="[0,1] x [0,1] with (x,0)~(x,1): identifying top and bottom gives a cylinder S^1 x [0,1].",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Quotient space (topology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Quotient_space_(topology)",
))

register_atom(Atom(
    atom_type="theorem", name="homotopy_group_compute",
    content="Higher homotopy groups pi_n(X) generalise the fundamental group. pi_n(S^n) = Z, pi_n(S^m) = 0 for n < m. Long exact sequence of a fibration: ... -> pi_n(F) -> pi_n(E) -> pi_n(B) -> pi_{n-1}(F) -> ...",
    example="pi_2(S^2) = Z. pi_3(S^2) = Z (Hopf fibration). pi_1(S^2) = 0.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Homotopy group', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Homotopy_group",
))

register_atom(Atom(
    atom_type="definition", name="deformation_retract",
    content="A deformation retraction of X onto A is a continuous map H: X x [0,1] -> X with H(x,0)=x, H(x,1) in A for all x, and H(a,t)=a for all a in A. A is then a deformation retract of X.",
    example="Cylinder S^1 x [0,1] deformation retracts onto S^1 x {0}: H((theta,s),t) = (theta, s(1-t)).",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Deformation retract', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Deformation_retract",
))

register_atom(Atom(
    atom_type="theorem", name="surface_classification",
    content="Classification of compact surfaces: every compact connected surface is homeomorphic to either S^2 (sphere), T^2#...#T^2 (connected sum of g tori, orientable genus g), or RP^2#...#RP^2 (connected sum of k projective planes, non-orientable).",
    example="Genus 2 orientable surface: chi = 2 - 2*2 = -2, 4 handles. Klein bottle: chi = 0, non-orientable genus 2.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Surface (topology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Surface_(topology)",
))

register_atom(Atom(
    atom_type="definition", name="degree_of_map",
    content="The degree of a continuous map f: S^n -> S^n is an integer measuring how many times f wraps the sphere around itself. deg(f) = sum of local degrees at preimages of a regular value. deg(id) = 1, deg(antipodal) = (-1)^{n+1}.",
    example="f: S^1 -> S^1, f(z) = z^3 (complex multiplication): deg(f) = 3. Each point has 3 preimages.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Degree of a continuous mapping', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Degree_of_a_continuous_mapping",
))

register_atom(Atom(
    atom_type="theorem", name="nerve_theorem",
    content="The Nerve Theorem: if U = {U_i} is a finite open cover of a paracompact space X such that every non-empty intersection of cover elements is contractible, then X is homotopy equivalent to the nerve of U.",
    example="Cover R^2 with 3 overlapping discs forming a triangle pattern: if all pairwise and triple intersections are contractible, the nerve is a triangle (simplicial complex), and the union is homotopy equivalent to it.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Nerve of a covering', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Nerve_of_a_covering",
))

# ── Logic Ext ────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="cnf_conversion",
    content="Conjunctive Normal Form: a conjunction of disjunctions (AND of ORs). Convert by: eliminate biconditionals, eliminate implications, push NOT inward (De Morgan), distribute OR over AND.",
    example="(p -> q) AND r: eliminate ->: (NOT p OR q) AND r. Already in CNF: two clauses {NOT p, q} and {r}.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Conjunctive normal form', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Conjunctive_normal_form",
))

register_atom(Atom(
    atom_type="algorithm", name="dnf_conversion",
    content="Disjunctive Normal Form: a disjunction of conjunctions (OR of ANDs). Convert by: eliminate biconditionals, eliminate implications, push NOT inward, distribute AND over OR.",
    example="(p AND q) OR r: already in DNF. Two terms: (p AND q) and (r).",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Disjunctive normal form', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Disjunctive_normal_form",
))

register_atom(Atom(
    atom_type="definition", name="logical_consequence",
    content="A formula phi is a logical consequence of a set of formulas Gamma (Gamma |= phi) if every interpretation that satisfies all formulas in Gamma also satisfies phi. Equivalently, Gamma union {NOT phi} is unsatisfiable.",
    example="Gamma = {p, p -> q}. phi = q. Every model where p=T and p->q=T has q=T. So {p, p->q} |= q.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Logical consequence', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Logical_consequence",
))

register_atom(Atom(
    atom_type="theorem", name="proof_by_induction_ext",
    content="Mathematical induction: prove P(0) (base case), then prove P(n) -> P(n+1) (inductive step). Strong induction: assume P(k) for all k <= n, prove P(n+1). Structural induction: induction on recursive structure.",
    example="Prove sum(1..n) = n(n+1)/2. Base: n=1, 1 = 1*2/2 = 1. Step: assume sum(1..n) = n(n+1)/2, then sum(1..n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2.",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Mathematical induction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mathematical_induction",
))

register_atom(Atom(
    atom_type="definition", name="predicate_logic_validity",
    content="A first-order formula is valid if it is true in every interpretation. It is satisfiable if true in some interpretation. Valid formulas include: forall x (P(x) -> P(x)), forall x P(x) -> exists x P(x).",
    example="forall x (P(x) OR NOT P(x)) is valid (law of excluded middle). exists x P(x) AND exists x NOT P(x) is satisfiable but not valid.",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Validity (logic)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Validity_(logic)",
))

register_atom(Atom(
    atom_type="algorithm", name="reductio_ad_absurdum",
    content="Proof by contradiction (reductio ad absurdum): assume the negation of the statement, derive a contradiction, conclude the original statement is true.",
    example="Prove sqrt(2) is irrational. Assume sqrt(2) = p/q (lowest terms). Then 2q^2 = p^2, so p is even. Let p=2k, then 2q^2 = 4k^2, q^2 = 2k^2, so q is even. Contradiction: both even, not lowest terms.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Proof by contradiction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Proof_by_contradiction",
))

register_atom(Atom(
    atom_type="theorem", name="soundness_completeness",
    content="Soundness: if Gamma |- phi then Gamma |= phi (provable implies true). Completeness (Goedel): if Gamma |= phi then Gamma |- phi (true implies provable). First-order logic is both sound and complete.",
    example="In propositional logic: {p, p->q} |- q (by modus ponens). Soundness guarantees {p, p->q} |= q. Completeness guarantees the converse.",
    tier=7, domain="logic",
    source="Wikipedia contributors, 'Godel completeness theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/G%C3%B6del%27s_completeness_theorem",
))

register_atom(Atom(
    atom_type="definition", name="tarski_truth",
    content="Tarski's definition of truth: a sentence phi is true in a model M (M |= phi) iff the recursive semantic conditions are satisfied. For atomic: M |= R(a) iff the interpretation of a is in the extension of R.",
    example="Model M with domain {1,2,3}, P = {1,3}. M |= P(1) (true, 1 in P). M |= forall x P(x) (false, 2 not in P).",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Semantic theory of truth', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Semantic_theory_of_truth",
))

# ── CS Theory Ext ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition", name="time_complexity_compute",
    content="Time complexity T(n) counts the number of basic operations as a function of input size n. Common classes: O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n). Determined by counting loops, recursions, and operations.",
    example="Nested loops: for i in range(n): for j in range(n): O(1) operation. T(n) = n * n = O(n^2).",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Time complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Time_complexity",
))

register_atom(Atom(
    atom_type="definition", name="space_complexity",
    content="Space complexity S(n) measures the memory used by an algorithm as a function of input size. Includes input space and auxiliary space. In-place algorithms use O(1) auxiliary space.",
    example="Merge sort: S(n) = O(n) auxiliary space (temporary arrays). Quicksort: S(n) = O(log n) auxiliary (recursion stack, in-place partitioning).",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Space complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Space_complexity",
))

register_atom(Atom(
    atom_type="theorem", name="np_completeness_proof",
    content="To prove problem X is NP-complete: 1) show X is in NP (solution verifiable in polynomial time), 2) reduce a known NP-complete problem Y to X in polynomial time (Y <=_p X).",
    example="3-SAT is NP-complete. To prove CLIQUE is NP-complete: show CLIQUE in NP (verify clique in O(k^2)), then reduce 3-SAT to CLIQUE in polynomial time.",
    tier=7, domain="computer_science",
    source="Wikipedia contributors, 'NP-completeness', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/NP-completeness",
))

register_atom(Atom(
    atom_type="definition", name="complexity_class",
    content="Complexity classes: P (polynomial time), NP (nondeterministic polynomial), co-NP, PSPACE, EXP. P subset NP subset PSPACE subset EXP. Whether P = NP is open.",
    example="SAT is in NP: given an assignment, verify in O(n). SAT is NP-complete (Cook-Levin theorem). If P = NP, all NP problems solvable in polynomial time.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Complexity class', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Complexity_class",
))

register_atom(Atom(
    atom_type="definition", name="circuit_complexity",
    content="Circuit complexity measures the size (number of gates) of Boolean circuits computing a function. Circuit classes: AC^0 (constant depth, unbounded fan-in), NC (polylog depth), P/poly (polynomial size). Parity is not in AC^0.",
    example="AND of n bits: circuit size 1 (single AND gate with n inputs in AC^0). Parity of n bits: requires depth Omega(log n) in bounded fan-in circuits.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Circuit complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Circuit_complexity",
))

register_atom(Atom(
    atom_type="definition", name="communication_complexity",
    content="Communication complexity measures bits exchanged between parties to compute a function of their combined inputs. Deterministic, randomised, and quantum variants exist. EQ (equality) requires Omega(n) deterministic bits but O(log n) randomised.",
    example="Equality EQ(x,y): Alice has x, Bob has y, both n-bit strings. Deterministic: Omega(n) bits. Randomised: O(1) with hash: Alice sends h(x), Bob checks h(x)=h(y).",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Communication complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Communication_complexity",
))

register_atom(Atom(
    atom_type="algorithm", name="streaming_algorithm",
    content="Streaming algorithms process input in one pass with limited memory. Count-Min Sketch estimates frequency with d hash functions and w counters. Morris counter estimates count n using O(log log n) bits.",
    example="Count-Min Sketch: w=10, d=3. Insert 'apple' 5 times. Query 'apple': min of 3 counter values = 5 (exact if no collision).",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Streaming algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Streaming_algorithm",
))

register_atom(Atom(
    atom_type="definition", name="randomised_complexity",
    content="Randomised complexity classes: BPP (bounded-error probabilistic polynomial), RP (one-sided error), ZPP (zero-error probabilistic polynomial) = RP intersect co-RP. BPP is believed to equal P.",
    example="Primality testing (Miller-Rabin): in RP. If composite, witnesses exist with probability >= 3/4. k rounds: error probability <= (1/4)^k.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'BPP (complexity)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/BPP_(complexity)",
))

# ── PDE Ext ──────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="poisson_equation",
    content="Poisson's equation: nabla^2 u = f, where f is a source term. In 1D: u''(x) = f(x). Solution via Green's function or finite differences. Laplace equation is the special case f=0.",
    example="u''(x) = -2 on [0,1], u(0)=u(1)=0. Solution: u(x) = x(1-x). Check: u'' = -2.",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Poisson equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Poisson%27s_equation",
))

register_atom(Atom(
    atom_type="formula", name="helmholtz_equation",
    content="Helmholtz equation: nabla^2 u + k^2 u = 0, where k is the wavenumber. Arises from separating time in the wave equation. Solutions are eigenfunctions of the Laplacian.",
    example="1D: u''+ k^2 u = 0. General solution: u(x) = A*cos(kx) + B*sin(kx). With u(0)=0: u(x) = B*sin(kx).",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Helmholtz equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Helmholtz_equation",
))

register_atom(Atom(
    atom_type="formula", name="advection_equation",
    content="Advection equation: du/dt + c * du/dx = 0, where c is the wave speed. Solution: u(x,t) = f(x - ct), a rightward-travelling wave preserving its initial shape.",
    example="c=2, initial condition u(x,0) = exp(-x^2). At t=3: u(x,3) = exp(-(x-6)^2). Peak shifted from 0 to 6.",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Advection', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Advection",
))

register_atom(Atom(
    atom_type="formula", name="burgers_equation",
    content="Burgers' equation: du/dt + u * du/dx = nu * d^2u/dx^2. Inviscid (nu=0): develops shock waves. Viscous (nu>0): shocks are smoothed. Exact solution via Hopf-Cole transformation.",
    example="Inviscid Burgers with u(x,0) = 1-x for 0<x<1: characteristics cross at t=1, forming a shock. Shock speed = (u_L + u_R)/2.",
    tier=7, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Burgers equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Burgers%27_equation",
))

register_atom(Atom(
    atom_type="definition", name="boundary_conditions_pde",
    content="PDE boundary conditions: Dirichlet (u = g on boundary), Neumann (du/dn = g on boundary), Robin (a*u + b*du/dn = g). Mixed conditions use different types on different parts of the boundary.",
    example="Heat equation on [0,L]: Dirichlet u(0,t)=0, u(L,t)=0 (fixed endpoints). Neumann u_x(0,t)=0 (insulated end).",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Boundary value problem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Boundary_value_problem",
))

register_atom(Atom(
    atom_type="algorithm", name="eigenfunction_expansion",
    content="Eigenfunction expansion solves linear PDEs by expressing the solution as a sum of eigenfunctions: u(x,t) = sum c_n * phi_n(x) * T_n(t), where phi_n are eigenfunctions of the spatial operator.",
    example="Heat equation u_t = u_xx on [0,pi], u=0 at boundaries. phi_n = sin(nx), T_n = exp(-n^2 t). u = sum c_n sin(nx) exp(-n^2 t).",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Eigenfunction expansion', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Eigenfunction",
))

register_atom(Atom(
    atom_type="algorithm", name="crank_nicolson",
    content="Crank-Nicolson method: implicit finite difference scheme for parabolic PDEs. Average of forward and backward Euler: (u^{n+1} - u^n)/dt = 0.5*(L*u^{n+1} + L*u^n). Unconditionally stable, second-order in time and space.",
    example="Heat equation dt=0.01, dx=0.1: A*u^{n+1} = B*u^n where A,B are tridiagonal matrices. Solve tridiagonal system each timestep.",
    tier=6, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Crank-Nicolson method', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Crank%E2%80%93Nicolson_method",
))

register_atom(Atom(
    atom_type="theorem", name="variational_pde",
    content="Variational formulation: many PDEs arise as Euler-Lagrange equations of a functional J[u] = integral L(x, u, u') dx. The weak form: find u such that a(u,v) = L(v) for all test functions v. Basis of finite element method.",
    example="Poisson -u'' = f: multiply by test v, integrate by parts: integral u'v' dx = integral fv dx. This is the weak form.",
    tier=7, domain="partial_differential_equations",
    source="Wikipedia contributors, 'Calculus of variations', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Calculus_of_variations",
))

# ── Inorganic Chemistry Ext ──────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="lattice_energy",
    content="Lattice energy is the energy released when gaseous ions form an ionic solid. Born-Lande equation: U = -(N_A * M * e^2 * z+ * z-)/(4*pi*eps_0*r_0) * (1 - 1/n), where M is the Madelung constant and n is the Born exponent.",
    example="NaCl: M=1.7476, z+=1, z-=1, r_0=2.81A, n=8. U = -786 kJ/mol (experimental: -787 kJ/mol).",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Lattice energy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Lattice_energy",
))

register_atom(Atom(
    atom_type="formula", name="ionic_radius_ratio",
    content="The radius ratio rule predicts coordination geometry from r_cation/r_anion. Ratios: <0.155 linear, 0.155-0.225 trigonal planar, 0.225-0.414 tetrahedral, 0.414-0.732 octahedral, >0.732 cubic.",
    example="NaCl: r(Na+)=1.02A, r(Cl-)=1.81A. Ratio = 1.02/1.81 = 0.564. Falls in 0.414-0.732 range: octahedral coordination (correct).",
    tier=4, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Radius ratio', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Goldschmidt_tolerance_factor",
))

register_atom(Atom(
    atom_type="definition", name="band_theory_ext",
    content="Band theory: electron energy levels in solids form continuous bands. Valence band (filled), conduction band (empty). Band gap E_g determines: metal (no gap), semiconductor (small gap ~1eV), insulator (large gap >4eV).",
    example="Silicon: E_g = 1.12 eV (semiconductor). Diamond: E_g = 5.47 eV (insulator). Copper: overlapping bands (metal, E_g = 0).",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Electronic band structure', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Electronic_band_structure",
))

register_atom(Atom(
    atom_type="rule", name="nomenclature_complex",
    content="IUPAC nomenclature for coordination compounds: [cation][anion]. In complex: ligands alphabetically before metal, with prefixes (di, tri, tetra). Anionic complex: metal name ends in -ate. Oxidation state in Roman numerals.",
    example="[Co(NH3)5Cl]Cl2: pentaamminechloridocobalt(III) chloride. 5 NH3 (ammine) + 1 Cl (chlorido) + Co(III).",
    tier=4, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'IUPAC nomenclature of inorganic chemistry', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_inorganic_chemistry",
))

register_atom(Atom(
    atom_type="rule", name="trans_effect",
    content="The trans effect is the tendency of a ligand to direct the substitution of the ligand trans to itself. Trans effect series (increasing): H2O < NH3 < py < Cl- < Br- < I- < NO2- < CO ~ CN- ~ C2H4.",
    example="[PtCl4]^2- + NH3: Cl- has moderate trans effect. First NH3 replaces any Cl. Second NH3 goes trans to Cl (not trans to NH3), giving cis-[PtCl2(NH3)2].",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Trans effect', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Trans_effect",
))

register_atom(Atom(
    atom_type="rule", name="hard_soft_acid_base",
    content="HSAB principle: hard acids prefer hard bases, soft acids prefer soft bases. Hard: small, high charge, low polarisability (H+, Li+, F-, OH-). Soft: large, low charge, high polarisability (Cu+, Ag+, I-, RS-).",
    example="AgI is stable (soft-soft). LiF is stable (hard-hard). AgF is less stable than AgI. LiI is less stable than LiF.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'HSAB theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/HSAB_theory",
))

register_atom(Atom(
    atom_type="definition", name="molecular_orbital_diagram",
    content="Molecular orbital (MO) theory: atomic orbitals combine to form bonding (lower energy) and antibonding (higher energy) MOs. Bond order = (bonding electrons - antibonding electrons) / 2. For homonuclear diatomics, pi before sigma for Z <= 7.",
    example="O2: (sigma_2s)^2 (sigma*_2s)^2 (sigma_2p)^2 (pi_2p)^4 (pi*_2p)^2. Bond order = (8-4)/2 = 2. Two unpaired electrons: paramagnetic.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Molecular orbital diagram', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Molecular_orbital_diagram",
))

register_atom(Atom(
    atom_type="algorithm", name="redox_balancing",
    content="Balance redox equations by half-reaction method: 1) separate into oxidation and reduction half-reactions, 2) balance atoms other than O and H, 3) balance O with H2O, 4) balance H with H+, 5) balance charge with e-, 6) equalise electrons and add.",
    example="Fe^2+ + MnO4- -> Fe^3+ + Mn^2+ (acidic). Oxidation: Fe^2+ -> Fe^3+ + e-. Reduction: MnO4- + 8H+ + 5e- -> Mn^2+ + 4H2O. Multiply oxidation by 5: 5Fe^2+ + MnO4- + 8H+ -> 5Fe^3+ + Mn^2+ + 4H2O.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Redox', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Redox",
))

# ── General Chemistry Ext ────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="limiting_reagent",
    content="The limiting reagent is the reactant that is completely consumed first, determining the maximum product yield. Compare moles available / stoichiometric coefficient for each reactant; smallest ratio is limiting.",
    example="2H2 + O2 -> 2H2O. Given 3 mol H2, 2 mol O2. H2: 3/2 = 1.5. O2: 2/1 = 2. H2 is limiting. Product: 3 mol H2O.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Limiting reagent', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Limiting_reagent",
))

register_atom(Atom(
    atom_type="formula", name="percent_composition",
    content="Percent composition: mass percentage of each element in a compound. %(element) = (n * atomic_mass / molar_mass) * 100, where n is the number of atoms of that element.",
    example="H2O: M = 2(1.008) + 16.00 = 18.016. %H = 2*1.008/18.016 * 100 = 11.19%. %O = 16.00/18.016 * 100 = 88.81%.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Mass fraction (chemistry)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mass_fraction_(chemistry)",
))

register_atom(Atom(
    atom_type="algorithm", name="empirical_formula",
    content="Empirical formula from percent composition: 1) assume 100g sample, 2) convert mass to moles, 3) divide all by smallest mole value, 4) round to nearest whole numbers (or multiply to clear fractions).",
    example="40.0% C, 6.7% H, 53.3% O. Moles: C=3.33, H=6.67, O=3.33. Divide by 3.33: C=1, H=2, O=1. Empirical formula: CH2O.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Empirical formula', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Empirical_formula",
))

register_atom(Atom(
    atom_type="formula", name="solution_dilution",
    content="Dilution equation: M1*V1 = M2*V2, where M1, V1 are initial molarity and volume, M2, V2 are final molarity and volume. Adding solvent decreases concentration.",
    example="Dilute 50 mL of 6M HCl to 2M: 6*50 = 2*V2. V2 = 150 mL. Add 100 mL water.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Dilution (equation)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Dilution_(equation)",
))

register_atom(Atom(
    atom_type="formula", name="gas_law_combined",
    content="Combined gas law: P1*V1/T1 = P2*V2/T2. Relates pressure, volume, and temperature for a fixed amount of gas. Special cases: Boyle (T const), Charles (P const), Gay-Lussac (V const).",
    example="P1=2atm, V1=3L, T1=300K, T2=600K, V2=4L. P2 = P1*V1*T2/(T1*V2) = 2*3*600/(300*4) = 3 atm.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Combined gas law', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Combined_gas_law",
))

register_atom(Atom(
    atom_type="formula", name="dalton_partial_pressure",
    content="Dalton's law: total pressure equals the sum of partial pressures. P_total = sum(P_i). Partial pressure of gas i: P_i = x_i * P_total, where x_i is the mole fraction.",
    example="Mixture: 2 mol N2, 1 mol O2, P_total = 3 atm. x_N2 = 2/3, x_O2 = 1/3. P_N2 = 2 atm, P_O2 = 1 atm.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Dalton law', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Dalton%27s_law",
))

register_atom(Atom(
    atom_type="algorithm", name="acid_base_titration",
    content="Acid-base titration: add base (or acid) until equivalence point where moles acid = moles base. At equivalence: n_acid * V_acid * valence_acid = n_base * V_base * valence_base. pH at equivalence depends on salt hydrolysis.",
    example="Titrate 25 mL of 0.1M HCl with 0.1M NaOH. At equivalence: 0.1*25 = 0.1*V_NaOH, V_NaOH = 25 mL. pH = 7 (strong acid + strong base).",
    tier=5, domain="general_chemistry",
    source="Wikipedia contributors, 'Titration', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Titration",
))

register_atom(Atom(
    atom_type="formula", name="buffer_capacity",
    content="Henderson-Hasselbalch equation for buffer pH: pH = pKa + log([A-]/[HA]). Buffer capacity is maximum when [A-] = [HA] (pH = pKa). Effective buffering range: pKa +/- 1.",
    example="Acetic acid buffer: pKa = 4.76, [CH3COO-] = 0.1M, [CH3COOH] = 0.05M. pH = 4.76 + log(0.1/0.05) = 4.76 + 0.301 = 5.06.",
    tier=5, domain="general_chemistry",
    source="Wikipedia contributors, 'Henderson-Hasselbalch equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Henderson%E2%80%93Hasselbalch_equation",
))
