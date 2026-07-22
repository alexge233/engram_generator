"""Knowledge atoms for extension modules batch:
data_structures_ext, graphs_ext, economics_ext, topology_deep,
logic_ext, cs_theory_ext, pde_ext, inorganic_chemistry_ext,
general_chemistry_ext, thermodynamics_ext, optics_ext, robotics_ext.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Data Structures Extension ────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="bst_insert",
    content="Binary search tree insertion: compare key with current node, go left if smaller, right if larger, insert at leaf position. Time: O(h) where h is tree height.",
    example="Insert 5 into BST [3,7,1,4]: compare 5>3 (right), 5<7 (left), 5>4 (right). Node 5 becomes right child of 4.",
    tier=3, domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm", name="bst_delete",
    content="BST deletion has three cases: (1) leaf node - remove directly, (2) one child - replace with child, (3) two children - replace with inorder successor (smallest in right subtree) or predecessor.",
    example="Delete 3 from BST [5,3,7,2,4]: node 3 has two children (2,4). Inorder successor is 4. Replace 3 with 4, tree becomes [5,4,7,2].",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm", name="avl_rotation",
    content="AVL tree maintains balance factor (height difference) of at most 1 at every node. Four rotation cases: left-left (right rotate), right-right (left rotate), left-right (left-right rotate), right-left (right-left rotate).",
    example="Insert 3,2,1 into AVL: after inserting 1, node 3 is left-heavy (bf=2). Right rotate at 3: root becomes 2 with children 1,3.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'AVL tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/AVL_tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm", name="red_black_insert",
    content="Red-black tree insertion: insert as red node, then fix violations. Properties: root is black, red nodes have black children, all paths have equal black depth. Fix-up uses recoloring and rotations.",
    example="Insert 4 (red) into RB tree [7B,3R,nil]: no violation since parent 3 is red but uncle is nil (black). Left-rotate at 7, recolor: [3B,nil,7R,nil,nil,4R].",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'Red-black tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Red%E2%80%93black_tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm", name="b_tree_insert",
    content="B-tree of order m: each node has at most m children and at least ceil(m/2) children (except root). Insert into leaf; if leaf overflows (>m-1 keys), split at median and push median to parent.",
    example="B-tree order 3, insert 1,2,3: after inserting 3, leaf [1,2,3] overflows. Split: median 2 goes to parent, leaves [1] and [3].",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'B-tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/B-tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm", name="trie_operations",
    content="A trie (prefix tree) stores strings character by character. Insert: traverse/create nodes for each character, mark end. Search: traverse nodes for each character, check end marker. Time: O(L) where L is string length.",
    example="Insert 'cat','car' into empty trie: root->c->a->t(end), root->c->a->r(end). Shared prefix 'ca'.",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Trie', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trie",
    prerequisites=["string_reverse"],
))

register_atom(Atom(
    atom_type="algorithm", name="skip_list",
    content="Skip list is a probabilistic data structure with O(log n) expected search, insert, delete. Multiple levels of linked lists; each element is promoted to the next level with probability p (typically 1/2).",
    example="Search for 7 in skip list L0:[1,3,5,7,9], L1:[1,5,9], L2:[1,9]: Start L2: 1<7, 9>7 drop. L1: 5<7, 9>7 drop. L0: 7=7 found.",
    tier=5, domain="data_structures",
    source="Wikipedia contributors, 'Skip list', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Skip_list",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm", name="bloom_filter",
    content="Bloom filter is a probabilistic set membership test. Uses k hash functions and m-bit array. Insert: set bits h1(x)..hk(x). Query: check all bits. False positives possible, false negatives impossible. Optimal k = (m/n)*ln(2).",
    example="m=10 bits, k=3, insert 'hello': h1=2, h2=5, h3=8. Set bits 2,5,8. Query 'world': h1=1, h2=5, h3=7. Bit 1=0, so 'world' NOT in set.",
    tier=4, domain="data_structures",
    source="Wikipedia contributors, 'Bloom filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bloom_filter",
    prerequisites=["modular"],
))

# ── Graphs Extension ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="bellman_ford",
    content="Bellman-Ford finds shortest paths from a source in a weighted graph, handling negative weights. Relaxes all edges V-1 times. Time: O(VE). Detects negative cycles on the V-th pass.",
    example="Graph: A->B(4), A->C(2), C->B(-3). Init: d[A]=0, d[B]=inf, d[C]=inf. Pass 1: d[C]=2, d[B]=4. Pass 2: d[B]=min(4, 2+(-3))=-1. Shortest A->B = -1.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Bellman-Ford algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm", name="floyd_warshall",
    content="Floyd-Warshall computes all-pairs shortest paths. Dynamic programming: d[i][j] = min(d[i][j], d[i][k]+d[k][j]) for each intermediate vertex k. Time: O(V^3).",
    example="3 vertices, edges: 1->2(3), 2->3(1), 1->3(6). Init matrix. k=2: d[1][3] = min(6, 3+1) = 4. All-pairs: d[1][2]=3, d[1][3]=4, d[2][3]=1.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Floyd-Warshall algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm", name="articulation_point",
    content="An articulation point (cut vertex) is a vertex whose removal disconnects the graph. Found using DFS: vertex u is an articulation point if (1) u is root with 2+ children, or (2) u has child v with no back edge to ancestor of u (low[v] >= disc[u]).",
    example="Graph: A-B, B-C, C-A, B-D. DFS from A. B is articulation point: removing B disconnects D from {A,C}.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Biconnected component', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biconnected_component",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm", name="strongly_connected",
    content="Strongly connected components (SCCs) of a directed graph: maximal subsets where every vertex is reachable from every other. Tarjan's algorithm uses DFS with a stack, tracking discovery time and low-link values. Time: O(V+E).",
    example="Graph: A->B, B->C, C->A, C->D, D->E, E->D. SCCs: {A,B,C} and {D,E}.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Tarjan\\'s strongly connected components algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm",
    prerequisites=["graph_reach", "topo_sort"],
))

register_atom(Atom(
    atom_type="algorithm", name="graph_matching",
    content="Maximum matching in a bipartite graph: largest set of edges with no shared vertices. Hungarian algorithm or Hopcroft-Karp finds it in O(E*sqrt(V)). Konig's theorem: max matching = min vertex cover in bipartite graphs.",
    example="Bipartite graph L={a,b,c}, R={1,2,3}, edges: a-1, a-2, b-2, c-3. Max matching: {a-1, b-2, c-3}, size 3.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Matching (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matching_(graph_theory)",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm", name="network_flow_detail",
    content="Max-flow min-cut theorem: maximum flow from s to t equals minimum capacity of an s-t cut. Ford-Fulkerson: repeatedly find augmenting paths and push flow. Edmonds-Karp uses BFS for O(VE^2).",
    example="Network: s->a(10), s->b(5), a->b(2), a->t(6), b->t(8). Max flow: s->a->t(6), s->b->t(5), s->a->b->t(2). Total = 13.",
    tier=6, domain="graph_theory",
    source="Wikipedia contributors, 'Maximum flow problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_flow_problem",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm", name="topological_sort_dfs",
    content="Topological sort of a DAG: linear ordering of vertices such that for every edge (u,v), u comes before v. DFS-based: add vertex to front of result when DFS finishes (post-order reverse).",
    example="DAG: A->B, A->C, B->D, C->D. DFS from A: finish order D,B,C,A. Reverse: A,C,B,D (or A,B,C,D). Both valid topological orderings.",
    tier=5, domain="graph_theory",
    source="Wikipedia contributors, 'Topological sorting', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Topological_sorting",
    prerequisites=["topo_sort"],
))

register_atom(Atom(
    atom_type="algorithm", name="graph_coloring_greedy",
    content="Greedy graph coloring: process vertices in order, assign each the smallest color not used by its neighbors. Uses at most Delta+1 colors (where Delta is max degree). Not optimal in general.",
    example="Graph: A-B, B-C, C-A (triangle). Order A,B,C: A=1, B=2 (A is neighbor), C=3 (A,B are neighbors). Chromatic number = 3.",
    tier=4, domain="graph_theory",
    source="Wikipedia contributors, 'Greedy coloring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Greedy_coloring",
    prerequisites=["graph_reach"],
))

# ── Economics Extension ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="marginal_analysis",
    content="Marginal cost (MC) is the derivative of total cost: MC = dTC/dQ. Profit maximisation occurs where MC = MR (marginal revenue). For competitive firms, MR = P (price).",
    example="TC = 100 + 5Q + 0.5Q^2, P=15. MC = 5+Q. Set MC=P: 5+Q=15, Q=10. Profit = 15*10 - (100+50+50) = 150-200 = -50.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Marginal cost', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Marginal_cost",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula", name="consumer_surplus",
    content="Consumer surplus is the area between the demand curve and the market price: CS = integral(D(Q) dQ, 0, Q*) - P*Q*, where D(Q) is the inverse demand and Q* is equilibrium quantity.",
    example="Demand: P=20-2Q, market price P*=10, Q*=5. CS = integral(20-2Q, 0, 5) - 10*5 = [20Q-Q^2]_0^5 - 50 = (100-25) - 50 = 25.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Consumer surplus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Consumer_surplus",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula", name="multiplier_effect",
    content="The fiscal multiplier in Keynesian economics: multiplier = 1/(1-MPC), where MPC is the marginal propensity to consume. A government spending increase of dG leads to GDP increase of dG * multiplier.",
    example="MPC=0.8: multiplier = 1/(1-0.8) = 1/0.2 = 5. Government spends $100M extra: GDP increases by $500M.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Fiscal multiplier', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fiscal_multiplier",
    prerequisites=["geometric_sequence"],
))

register_atom(Atom(
    atom_type="formula", name="exchange_rate",
    content="Exchange rate conversion: amount_foreign = amount_domestic * exchange_rate. Purchasing power parity (PPP): exchange rate should equalise prices across countries. Real exchange rate: RER = e * P_foreign / P_domestic.",
    example="USD/EUR rate = 0.85. Convert $1000 to EUR: 1000 * 0.85 = 850 EUR.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Exchange rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exchange_rate",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula", name="inflation_real_rate",
    content="Fisher equation: real interest rate = nominal rate - inflation rate (approximate). Exact: (1+r) = (1+i)/(1+pi), where r is real rate, i is nominal, pi is inflation.",
    example="Nominal rate i=6%, inflation pi=2%: real rate r = 6-2 = 4% (approx). Exact: (1.06)/(1.02) - 1 = 0.0392 = 3.92%.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Fisher equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fisher_equation",
    prerequisites=["percentage"],
))

register_atom(Atom(
    atom_type="formula", name="production_function",
    content="Cobb-Douglas production function: Y = A * L^alpha * K^beta, where Y is output, L is labour, K is capital, A is total factor productivity, and alpha+beta determines returns to scale (=1: constant, >1: increasing, <1: decreasing).",
    example="A=2, L=100, K=50, alpha=0.7, beta=0.3: Y = 2 * 100^0.7 * 50^0.3 = 2 * 25.12 * 3.66 = 183.9.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Cobb-Douglas production function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="definition", name="game_theory_market",
    content="In a Cournot duopoly, two firms choose quantities simultaneously. Each firm maximises profit given the other's quantity. Nash equilibrium: q1* = q2* = (a-c)/(3b) for linear demand P = a - b(q1+q2) and constant marginal cost c.",
    example="a=100, b=1, c=10: q1*=q2*=(100-10)/3=30. P=100-60=40. Profit each: (40-10)*30=900.",
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Cournot competition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cournot_competition",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="formula", name="time_value_money",
    content="Future value: FV = PV * (1+r)^n. Present value: PV = FV / (1+r)^n. Annuity PV: PV = C * (1-(1+r)^{-n})/r, where C is periodic payment, r is interest rate, n is number of periods.",
    example="PV=$1000, r=5%, n=10: FV = 1000*(1.05)^10 = 1000*1.6289 = $1628.89.",
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Time value of money', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time_value_of_money",
    prerequisites=["exponentiation", "compound_interest"],
))

# ── Topology Deep ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition", name="path_connected",
    content="A topological space X is path-connected if for any two points a,b in X, there exists a continuous function f:[0,1]->X with f(0)=a and f(1)=b. Path-connected implies connected, but not conversely.",
    example="R^2 \\ {0} is path-connected: for any a,b, go around origin via arc. Topologist's sine curve {(x,sin(1/x)): x>0} union {(0,y): -1<=y<=1} is connected but not path-connected.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Connected space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Connected_space",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition", name="product_topology",
    content="The product topology on X x Y has basis {U x V : U open in X, V open in Y}. A function f:Z->X x Y is continuous iff both projections pi_X o f and pi_Y o f are continuous. Tychonoff's theorem: product of compact spaces is compact.",
    example="R x R with product topology = standard R^2 topology. Open set: (0,1)x(0,1) is open. {1/n} x R is not open.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Product topology', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Product_topology",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition", name="quotient_space_compute",
    content="Quotient space X/~ identifies points related by equivalence relation ~. The quotient topology: U is open in X/~ iff its preimage q^{-1}(U) is open in X, where q:X->X/~ is the quotient map.",
    example="[0,1]/~ where 0~1: quotient is a circle S^1. The interval with endpoints identified.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Quotient space (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quotient_space_(topology)",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="theorem", name="homotopy_group_compute",
    content="The fundamental group pi_1(X,x0) consists of homotopy classes of loops based at x0. pi_1(S^1) = Z, pi_1(S^n) = 0 for n>=2, pi_1(T^2) = Z x Z. Van Kampen's theorem computes pi_1 of unions.",
    example="pi_1(S^1) = Z: loops are classified by winding number. The loop going around once clockwise = generator 1, twice = 2, etc.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Fundamental group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fundamental_group",
    prerequisites=["path_connected"],
))

register_atom(Atom(
    atom_type="definition", name="deformation_retract",
    content="A deformation retract of X onto A is a continuous map H:X x [0,1]->X with H(x,0)=x, H(x,1) in A for all x, and H(a,t)=a for all a in A. If A is a deformation retract of X, then X and A have the same homotopy type.",
    example="R^2\\{0} deformation retracts onto S^1: H(x,t) = (1-t)x + t*x/|x|. At t=0: identity. At t=1: projects to unit circle.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Retract', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Retract",
    prerequisites=["path_connected"],
))

register_atom(Atom(
    atom_type="theorem", name="surface_classification",
    content="The classification theorem for compact surfaces: every compact connected surface is homeomorphic to either S^2, a connected sum of n tori (orientable, genus n), or a connected sum of n real projective planes (non-orientable). Euler characteristic: chi = 2-2g (orientable) or chi = 2-k (non-orientable).",
    example="Torus T^2: genus 1, chi = 2-2(1) = 0. Klein bottle: chi = 0 (non-orientable, k=2).",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Surface (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Surface_(topology)",
    prerequisites=["euler_characteristic"],
))

register_atom(Atom(
    atom_type="definition", name="degree_of_map",
    content="The degree of a continuous map f:S^n->S^n is the integer d such that f_*:H_n(S^n)->H_n(S^n) is multiplication by d. The degree counts (with sign) how many times f wraps the domain around the codomain. deg(id) = 1, deg(antipodal) = (-1)^{n+1}.",
    example="f:S^1->S^1 defined by f(z)=z^3 (complex multiplication): degree = 3. Each point has 3 preimages.",
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Degree of a continuous mapping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Degree_of_a_continuous_mapping",
    prerequisites=["homotopy_group_compute"],
))

register_atom(Atom(
    atom_type="theorem", name="nerve_theorem",
    content="The nerve theorem states that if U = {U_i} is a finite open cover of a paracompact space X, and every non-empty intersection of cover elements is contractible, then X is homotopy equivalent to the nerve of the cover (the simplicial complex whose simplices are non-empty intersections).",
    example="Cover of S^1 by three arcs U1,U2,U3 overlapping pairwise: nerve is a triangle (3 vertices, 3 edges), which is homotopy equivalent to S^1.",
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Nerve of a covering', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nerve_of_a_covering",
    prerequisites=["simplicial_complex"],
))

# ── Logic Extension ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="cnf_conversion",
    content="Conjunctive normal form (CNF): conjunction of clauses, each a disjunction of literals. Convert: (1) eliminate implications: A->B = ~A v B, (2) push negations inward (De Morgan), (3) distribute OR over AND.",
    example="(p -> q) ^ r: step 1: (~p v q) ^ r. Already CNF. Two clauses: {~p, q} and {r}.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Conjunctive normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjunctive_normal_form",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="algorithm", name="dnf_conversion",
    content="Disjunctive normal form (DNF): disjunction of conjunctive clauses. Convert: (1) eliminate implications, (2) push negations inward, (3) distribute AND over OR.",
    example="p ^ (q v r): already DNF. Equivalent: (p^q) v (p^r). Two terms.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Disjunctive normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Disjunctive_normal_form",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="definition", name="logical_consequence",
    content="Phi is a logical consequence of Gamma (Gamma |= phi) if every interpretation that satisfies all formulas in Gamma also satisfies phi. Equivalently, Gamma union {~phi} is unsatisfiable.",
    example="Gamma = {p, p->q}. q is a logical consequence: in any model where p=T and p->q=T, we must have q=T.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Logical consequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logical_consequence",
    prerequisites=["propositional_eval", "implication"],
))

register_atom(Atom(
    atom_type="theorem", name="proof_by_induction_ext",
    content="Mathematical induction: prove P(0) (base case), then prove P(n)->P(n+1) (inductive step). Strong induction: assume P(k) for all k<=n. Structural induction: for recursively defined structures.",
    example="Prove sum(1..n) = n(n+1)/2. Base: n=1, 1=1*2/2=1. Step: assume sum(1..n)=n(n+1)/2. sum(1..n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2.",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Mathematical induction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mathematical_induction",
    prerequisites=["proof_by_induction"],
))

register_atom(Atom(
    atom_type="definition", name="predicate_logic_validity",
    content="A first-order formula is valid if it is true in every interpretation. A formula is satisfiable if true in some interpretation. Validity checking is undecidable in general (Church's theorem), but semi-decidable.",
    example="forall x (P(x) -> P(x)) is valid: tautology regardless of interpretation. exists x (P(x) ^ ~P(x)) is unsatisfiable.",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Validity (logic)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Validity_(logic)",
    prerequisites=["quantifier_eval"],
))

register_atom(Atom(
    atom_type="theorem", name="reductio_ad_absurdum",
    content="Proof by contradiction (reductio ad absurdum): to prove P, assume ~P and derive a contradiction. Then P must be true. Equivalent to proving ~P -> False, which gives P by double negation elimination (in classical logic).",
    example="Prove sqrt(2) is irrational. Assume sqrt(2) = p/q (reduced). Then 2q^2 = p^2, so p is even. Let p=2k. Then 2q^2=4k^2, q^2=2k^2, so q is even. Contradiction: p/q was reduced.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Proof by contradiction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Proof_by_contradiction",
    prerequisites=["implication"],
))

register_atom(Atom(
    atom_type="theorem", name="soundness_completeness",
    content="Soundness: if Gamma |- phi then Gamma |= phi (provable implies true). Completeness (Godel): if Gamma |= phi then Gamma |- phi (true implies provable). Together: syntactic and semantic consequence coincide for first-order logic.",
    example="In propositional logic: {p, p->q} |- q (modus ponens). Soundness guarantees q is true in every model of {p, p->q}.",
    tier=7, domain="logic",
    source="Wikipedia contributors, 'Godel\\'s completeness theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/G%C3%B6del%27s_completeness_theorem",
    prerequisites=["logical_consequence"],
))

register_atom(Atom(
    atom_type="definition", name="tarski_truth",
    content="Tarski's definition of truth: a sentence phi is true in model M iff M |= phi, defined recursively on formula structure. Atomic: M |= R(a) iff a^M in R^M. Connectives: M |= phi^psi iff M|=phi and M|=psi. Quantifiers: M |= forall x phi iff M|=phi[a/x] for all a in domain.",
    example="Model M: domain {1,2}, P={1}. M |= exists x P(x): check P(1)=True. So M |= exists x P(x).",
    tier=6, domain="logic",
    source="Wikipedia contributors, 'Tarski\\'s undefinability theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tarski%27s_undefinability_theorem",
    prerequisites=["predicate_logic_validity"],
))

# ── CS Theory Extension ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="time_complexity_compute",
    content="Time complexity T(n) counts the number of basic operations as a function of input size n. Common classes: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n^2) quadratic, O(2^n) exponential.",
    example="Nested loops: for i in range(n): for j in range(n): O(1) work. T(n) = n * n * O(1) = O(n^2).",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Time complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time_complexity",
    prerequisites=["big_o"],
))

register_atom(Atom(
    atom_type="formula", name="space_complexity",
    content="Space complexity S(n) measures the memory used by an algorithm as a function of input size. Includes input space and auxiliary space. PSPACE: problems solvable with polynomial space.",
    example="Merge sort: T(n)=O(n log n), S(n)=O(n) auxiliary space for merging. In-place quicksort: S(n)=O(log n) stack depth.",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Space complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Space_complexity",
    prerequisites=["big_o"],
))

register_atom(Atom(
    atom_type="theorem", name="np_completeness_proof",
    content="A problem L is NP-complete if (1) L is in NP, and (2) every problem in NP is polynomial-time reducible to L. To prove NP-completeness: show L is in NP (give polynomial verifier), then reduce a known NP-complete problem to L.",
    example="3-SAT is NP-complete. To show VERTEX-COVER is NP-complete: (1) given cover set S, verify in O(E) that every edge has an endpoint in S. (2) Reduce 3-SAT to VERTEX-COVER.",
    tier=7, domain="computer_science",
    source="Wikipedia contributors, 'NP-completeness', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/NP-completeness",
    prerequisites=["time_complexity_compute"],
))

register_atom(Atom(
    atom_type="definition", name="complexity_class",
    content="Complexity classes: P (polynomial time), NP (nondeterministic polynomial), co-NP, PSPACE, EXPTIME. Key relationships: P subset NP subset PSPACE subset EXPTIME. P vs NP is open.",
    example="Sorting is in P: O(n log n). SAT is NP-complete. TQBF (true quantified boolean formula) is PSPACE-complete.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Complexity class', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Complexity_class",
    prerequisites=["time_complexity_compute"],
))

register_atom(Atom(
    atom_type="definition", name="circuit_complexity",
    content="Circuit complexity measures the size (number of gates) of boolean circuits computing a function. Circuit classes: AC^0 (constant depth, unbounded fan-in), NC (polylog depth, bounded fan-in), P/poly (polynomial-size circuits).",
    example="Parity of n bits requires depth Omega(log n) with bounded fan-in gates. PARITY is not in AC^0 (Furst-Saxe-Sipser theorem).",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Circuit complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circuit_complexity",
    prerequisites=["complexity_class"],
))

register_atom(Atom(
    atom_type="definition", name="communication_complexity",
    content="Communication complexity: Alice has input x, Bob has input y. They must compute f(x,y) by exchanging bits. Deterministic CC D(f): minimum worst-case bits. R(f): randomised. Key result: EQ (equality) has D(EQ) = n+1 but R(EQ) = O(log n).",
    example="Equality of n-bit strings: deterministic requires n+1 bits. Randomised: Alice sends hash h(x) of O(log n) bits, Bob checks h(x)=h(y), error prob 1/n.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Communication complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Communication_complexity",
    prerequisites=["complexity_class"],
))

register_atom(Atom(
    atom_type="algorithm", name="streaming_algorithm",
    content="Streaming algorithms process input in one pass with sublinear space. Count-Min Sketch: estimates frequency of items using hash functions and counters. Space O(1/epsilon * log(1/delta)) for epsilon-approximation with probability 1-delta.",
    example="Count distinct elements: Flajolet-Martin. Hash items, track max trailing zeros. Estimate = 2^max_zeros. 4 items hashed to binary: ...100 (2 zeros), ...010 (1 zero). Estimate = 2^2 = 4.",
    tier=5, domain="computer_science",
    source="Wikipedia contributors, 'Streaming algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Streaming_algorithm",
    prerequisites=["hash_function"],
))

register_atom(Atom(
    atom_type="definition", name="randomised_complexity",
    content="BPP: problems solvable by randomised algorithms in polynomial time with error probability < 1/3. RP: one-sided error (always correct on NO, may err on YES). ZPP = RP intersect co-RP: zero-error expected polynomial time.",
    example="Primality testing (Miller-Rabin): in co-RP. If composite, at least 3/4 of witnesses detect it. Repeat k times: error < (1/4)^k.",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'BPP (complexity)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BPP_(complexity)",
    prerequisites=["complexity_class"],
))

# ── PDE Extension ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="poisson_equation",
    content="Poisson's equation: nabla^2 u = f, where nabla^2 is the Laplacian. Solved by Green's function: u(x) = integral(G(x,y) f(y) dy). In 2D with f constant on a disk, u is radially symmetric.",
    example="nabla^2 u = -1 on unit disk, u=0 on boundary: u(r) = (1-r^2)/4. At center: u(0) = 1/4 = 0.25.",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Poisson\\'s equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Poisson%27s_equation",
    prerequisites=["laplacian"],
))

register_atom(Atom(
    atom_type="formula", name="helmholtz_equation",
    content="Helmholtz equation: nabla^2 u + k^2 u = 0, where k is the wavenumber. Arises from separating time from the wave equation. In 1D: u(x) = A*cos(kx) + B*sin(kx).",
    example="1D, k=pi, u(0)=1, u(1)=0: u(x) = cos(pi*x). Check: u''=-pi^2*cos(pi*x), k^2*u=pi^2*cos(pi*x). Sum = 0.",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Helmholtz equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Helmholtz_equation",
    prerequisites=["wave_equation_1d"],
))

register_atom(Atom(
    atom_type="formula", name="advection_equation",
    content="Advection equation: du/dt + c * du/dx = 0, where c is the advection speed. Solution: u(x,t) = u_0(x - ct), a right-travelling wave preserving the initial profile.",
    example="c=2, u_0(x) = exp(-x^2). At t=1: u(x,1) = exp(-(x-2)^2). Peak moves from x=0 to x=2.",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Advection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Advection",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="formula", name="burgers_equation",
    content="Burgers' equation: du/dt + u * du/dx = nu * d^2u/dx^2. Nonlinear advection with viscosity. Inviscid (nu=0): develops shocks. Can be linearised via Hopf-Cole transformation: u = -2*nu * (d/dx)(ln phi).",
    example="Inviscid Burgers, u(x,0) = 1-x for 0<x<1: characteristics x = x_0 + (1-x_0)*t. Shock forms at t=1 when characteristics cross.",
    tier=7, domain="pde",
    source="Wikipedia contributors, 'Burgers\\' equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Burgers%27_equation",
    prerequisites=["advection_equation"],
))

register_atom(Atom(
    atom_type="definition", name="boundary_conditions_pde",
    content="Common boundary conditions for PDEs: Dirichlet (u = g on boundary), Neumann (du/dn = g on boundary), Robin (alpha*u + beta*du/dn = g). Well-posedness depends on the PDE type and boundary conditions.",
    example="Heat equation on [0,1]: Dirichlet u(0,t)=0, u(1,t)=0 (fixed endpoints). Neumann du/dx(0,t)=0 (insulated endpoint).",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Boundary value problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Boundary_value_problem",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="formula", name="eigenfunction_expansion",
    content="Solution of linear PDE via eigenfunction expansion: expand u(x,t) = sum(c_n(t) * phi_n(x)) where phi_n are eigenfunctions of the spatial operator. Reduces PDE to ODEs for c_n(t).",
    example="Heat equation u_t = u_xx on [0,pi], u=0 at boundaries: phi_n = sin(nx), u(x,t) = sum(b_n * exp(-n^2*t) * sin(nx)).",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Eigenfunction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Eigenfunction",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="algorithm", name="crank_nicolson",
    content="Crank-Nicolson method for heat equation: average of explicit and implicit Euler. u_j^{n+1} - u_j^n = (r/2)(u_{j+1}^n - 2u_j^n + u_{j-1}^n + u_{j+1}^{n+1} - 2u_j^{n+1} + u_{j-1}^{n+1}), where r = k*dt/dx^2. Unconditionally stable, O(dt^2 + dx^2).",
    example="r=0.5, 3 interior points, u=[0,1,0] at t=0: tridiagonal system Au^{n+1} = Bu^n. A = [[3,-0.5,0],[-0.5,3,-0.5],[0,-0.5,3]], B*u = [0.25, 0.5, 0.25].",
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Crank-Nicolson method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Crank%E2%80%93Nicolson_method",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="definition", name="variational_pde",
    content="Variational formulation of PDE: find u in function space V such that a(u,v) = L(v) for all test functions v in V, where a is a bilinear form and L is a linear functional. The Lax-Milgram theorem guarantees existence and uniqueness when a is coercive and continuous.",
    example="Poisson -u''=f on [0,1], u(0)=u(1)=0: weak form integral(u'*v' dx) = integral(f*v dx) for all v in H^1_0([0,1]).",
    tier=7, domain="pde",
    source="Wikipedia contributors, 'Weak formulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weak_formulation",
    prerequisites=["poisson_equation"],
))

# ── Inorganic Chemistry Extension ───────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="lattice_energy",
    content="Lattice energy is the energy released when gaseous ions form an ionic crystal. Born-Lande equation: U = -(N_A * M * e^2 * z+ * z-)/(4*pi*epsilon_0*r_0) * (1 - 1/n), where M is Madelung constant, r_0 is interionic distance, n is Born exponent.",
    example="NaCl: M=1.748, z+=1, z-=1, r_0=2.81A, n=8. U = -(6.022e23 * 1.748 * (1.602e-19)^2)/(4*pi*8.854e-12*2.81e-10) * (1-1/8) = -786 kJ/mol.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Lattice energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lattice_energy",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="rule", name="ionic_radius_ratio",
    content="Radius ratio rule predicts coordination geometry of ionic crystals: r+/r- < 0.155: linear (CN=2), 0.155-0.225: triangular (CN=3), 0.225-0.414: tetrahedral (CN=4), 0.414-0.732: octahedral (CN=6), >0.732: cubic (CN=8).",
    example="NaCl: r(Na+)=1.02A, r(Cl-)=1.81A. Ratio = 1.02/1.81 = 0.564. Range 0.414-0.732: octahedral (CN=6). Correct.",
    tier=4, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Pauling\\'s rules', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pauling%27s_rules",
    prerequisites=["crystal_structure"],
))

register_atom(Atom(
    atom_type="definition", name="band_theory_ext",
    content="Band theory: in solids, atomic orbitals overlap to form continuous bands. Valence band (filled), conduction band (empty), band gap E_g between them. Metals: overlapping bands. Semiconductors: small E_g (0.1-3 eV). Insulators: large E_g (>3 eV).",
    example="Silicon: E_g = 1.12 eV. At 300K, kT = 0.026 eV. Intrinsic carrier concentration: n_i = sqrt(N_c*N_v)*exp(-E_g/(2kT)) = 1.5e10 cm^-3.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Electronic band structure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electronic_band_structure",
    prerequisites=["quantum_mechanics"],
))

register_atom(Atom(
    atom_type="rule", name="nomenclature_complex",
    content="IUPAC nomenclature for coordination compounds: [ligands in alphabetical order]-metal(oxidation state). Anionic ligands get -o suffix (chloro, cyano, hydroxo). Neutral ligands keep name (ammine for NH3, aqua for H2O). Prefixes: di, tri, tetra for number.",
    example="[Cu(NH3)4]^2+: tetraamminecopper(II). [Fe(CN)6]^4-: hexacyanoferrate(II).",
    tier=4, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'IUPAC nomenclature of inorganic chemistry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_inorganic_chemistry",
    prerequisites=["coordination_number"],
))

register_atom(Atom(
    atom_type="rule", name="trans_effect",
    content="The trans effect: ligands trans to strong trans-effect ligands are more easily substituted. Order: CO ~ CN- > NO2- > I- > Br- > Cl- > NH3 > OH-. Used to predict products of square planar substitution reactions.",
    example="[PtCl4]^2- + NH3: Cl trans to Cl replaced first, giving cis-[PtCl2(NH3)2] (cisplatin).",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Trans effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trans_effect",
    prerequisites=["coordination_number"],
))

register_atom(Atom(
    atom_type="rule", name="hard_soft_acid_base",
    content="HSAB principle: hard acids prefer hard bases, soft acids prefer soft bases. Hard: small, high charge, low polarisability (Li+, F-). Soft: large, low charge, high polarisability (Ag+, I-). Predicts stability of complexes.",
    example="AgI is insoluble (soft-soft, stable). AgF is soluble (soft-hard, less stable). LiF is very stable (hard-hard).",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'HSAB theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/HSAB_theory",
    prerequisites=["electronegativity_bond"],
))

register_atom(Atom(
    atom_type="formula", name="molecular_orbital_diagram",
    content="MO theory: atomic orbitals combine to form bonding (lower energy) and antibonding (higher energy) molecular orbitals. Bond order = (bonding electrons - antibonding electrons)/2. For homonuclear diatomics, pi-pi* crossing occurs at O2.",
    example="O2: 16 electrons. Config: (sigma_1s)^2(sigma*_1s)^2(sigma_2s)^2(sigma*_2s)^2(sigma_2p)^2(pi_2p)^4(pi*_2p)^2. Bond order = (10-6)/2 = 2. Two unpaired electrons: paramagnetic.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Molecular orbital diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molecular_orbital_diagram",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="algorithm", name="redox_balancing",
    content="Balance redox equations by half-reaction method: (1) split into oxidation and reduction half-reactions, (2) balance atoms other than O and H, (3) balance O with H2O, (4) balance H with H+, (5) balance charge with electrons, (6) multiply to equalise electrons, (7) add half-reactions.",
    example="Fe + Cu^2+ -> Fe^2+ + Cu. Oxidation: Fe -> Fe^2+ + 2e-. Reduction: Cu^2+ + 2e- -> Cu. Already balanced: Fe + Cu^2+ -> Fe^2+ + Cu.",
    tier=5, domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Redox', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Redox",
    prerequisites=["oxidation_state"],
))

# ── General Chemistry Extension ──────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="limiting_reagent",
    content="The limiting reagent is the reactant that is completely consumed first, determining the maximum product yield. Compare moles of each reactant divided by their stoichiometric coefficients; the smallest ratio is limiting.",
    example="2H2 + O2 -> 2H2O. Given 3 mol H2 and 2 mol O2: H2 ratio = 3/2 = 1.5, O2 ratio = 2/1 = 2. H2 is limiting. Max H2O = 3 mol.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Limiting reagent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limiting_reagent",
    prerequisites=["stoichiometry"],
))

register_atom(Atom(
    atom_type="formula", name="percent_composition",
    content="Mass percent of element X in compound = (n * M_X / M_compound) * 100%, where n is the number of atoms of X and M is molar mass.",
    example="H2O: M = 2(1.008) + 16.00 = 18.016 g/mol. %H = 2(1.008)/18.016 * 100 = 11.19%. %O = 16.00/18.016 * 100 = 88.81%.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Mass fraction (chemistry)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mass_fraction_(chemistry)",
    prerequisites=["molar_mass"],
))

register_atom(Atom(
    atom_type="algorithm", name="empirical_formula",
    content="Determine empirical formula: (1) convert mass percentages to moles by dividing by molar mass, (2) divide all by the smallest mole value, (3) round to nearest whole number. Multiply all by a common factor if needed.",
    example="40.0% C, 6.7% H, 53.3% O. Moles: C=40/12=3.33, H=6.7/1=6.7, O=53.3/16=3.33. Ratio: 1:2:1. Empirical formula: CH2O.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Empirical formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Empirical_formula",
    prerequisites=["molar_mass"],
))

register_atom(Atom(
    atom_type="formula", name="solution_dilution",
    content="Dilution equation: M1*V1 = M2*V2, where M is molarity and V is volume. Adding solvent decreases concentration but preserves total moles of solute.",
    example="Dilute 50 mL of 2 M HCl to 0.5 M: M1*V1 = M2*V2 -> 2*50 = 0.5*V2 -> V2 = 200 mL. Add 150 mL water.",
    tier=3, domain="general_chemistry",
    source="Wikipedia contributors, 'Dilution (equation)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dilution_(equation)",
    prerequisites=["molarity"],
))

register_atom(Atom(
    atom_type="formula", name="gas_law_combined",
    content="Combined gas law: P1*V1/T1 = P2*V2/T2, combining Boyle's, Charles's, and Gay-Lussac's laws. Temperature must be in Kelvin.",
    example="Gas at P1=1 atm, V1=2 L, T1=300 K. Find V2 at P2=2 atm, T2=600 K: V2 = P1*V1*T2/(T1*P2) = 1*2*600/(300*2) = 2 L.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Combined gas law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Combined_gas_law",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula", name="dalton_partial_pressure",
    content="Dalton's law: total pressure of a gas mixture equals the sum of partial pressures. P_total = P1 + P2 + ... + Pn. Partial pressure: P_i = x_i * P_total, where x_i is mole fraction.",
    example="Mixture: 2 mol N2, 1 mol O2, P_total = 3 atm. x_N2 = 2/3, x_O2 = 1/3. P_N2 = (2/3)*3 = 2 atm, P_O2 = (1/3)*3 = 1 atm.",
    tier=4, domain="general_chemistry",
    source="Wikipedia contributors, 'Dalton\\'s law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dalton%27s_law",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula", name="acid_base_titration",
    content="At equivalence point of acid-base titration: moles acid = moles base (for monoprotic). n_a * M_a * V_a = n_b * M_b * V_b. pH at equivalence depends on salt hydrolysis.",
    example="25 mL of 0.1 M HCl titrated with 0.1 M NaOH: V_eq = M_a*V_a/M_b = 0.1*25/0.1 = 25 mL NaOH needed. At equivalence: pH = 7 (strong-strong).",
    tier=5, domain="general_chemistry",
    source="Wikipedia contributors, 'Titration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Titration",
    prerequisites=["ph_calculation", "molarity"],
))

register_atom(Atom(
    atom_type="formula", name="buffer_capacity",
    content="Henderson-Hasselbalch equation: pH = pKa + log([A-]/[HA]). Buffer capacity beta = 2.303 * C * Ka * [H+] / (Ka + [H+])^2, where C is total buffer concentration. Maximum buffer capacity at pH = pKa.",
    example="Acetate buffer: pKa=4.76, [CH3COO-]=0.1M, [CH3COOH]=0.05M. pH = 4.76 + log(0.1/0.05) = 4.76 + 0.301 = 5.06.",
    tier=5, domain="general_chemistry",
    source="Wikipedia contributors, 'Buffer solution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Buffer_solution",
    prerequisites=["ph_calculation", "equilibrium_constant"],
))

# ── Thermodynamics Extension ─────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="otto_cycle",
    content="Otto cycle (ideal gasoline engine): two adiabatic and two isochoric processes. Efficiency: eta = 1 - 1/r^(gamma-1), where r is compression ratio and gamma = Cp/Cv.",
    example="r=8, gamma=1.4: eta = 1 - 1/8^0.4 = 1 - 1/2.297 = 1 - 0.435 = 0.565 (56.5%).",
    tier=5, domain="thermodynamics",
    source="Wikipedia contributors, 'Otto cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Otto_cycle",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula", name="diesel_cycle",
    content="Diesel cycle: two adiabatic, one isochoric, one isobaric process. Efficiency: eta = 1 - (1/r^(gamma-1)) * (rho^gamma - 1)/(gamma*(rho - 1)), where rho is cutoff ratio = V3/V2.",
    example="r=18, rho=2, gamma=1.4: eta = 1 - (1/18^0.4) * (2^1.4-1)/(1.4*(2-1)) = 1 - (1/3.178) * (2.639-1)/(1.4) = 1 - 0.315*1.171 = 1 - 0.369 = 0.631 (63.1%).",
    tier=5, domain="thermodynamics",
    source="Wikipedia contributors, 'Diesel cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diesel_cycle",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula", name="rankine_cycle",
    content="Rankine cycle (steam power plant): pump (isentropic), boiler (isobaric), turbine (isentropic), condenser (isobaric). Efficiency: eta = (h1-h2-(h4-h3))/(h1-h4), where h are specific enthalpies at each state point.",
    example="h1=3000 kJ/kg, h2=2000 kJ/kg, h3=200 kJ/kg, h4=210 kJ/kg: eta = (3000-2000-(210-200))/(3000-210) = 990/2790 = 0.355 (35.5%).",
    tier=6, domain="thermodynamics",
    source="Wikipedia contributors, 'Rankine cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rankine_cycle",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula", name="refrigeration_cop",
    content="Coefficient of performance: COP_refrigerator = Q_cold/W = Q_cold/(Q_hot - Q_cold). Carnot COP = T_cold/(T_hot - T_cold). For heat pump: COP_hp = Q_hot/W = COP_ref + 1.",
    example="Refrigerator: T_cold=250K, T_hot=300K. Carnot COP = 250/(300-250) = 250/50 = 5. For 1 kJ work, removes 5 kJ from cold reservoir.",
    tier=4, domain="thermodynamics",
    source="Wikipedia contributors, 'Coefficient of performance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coefficient_of_performance",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="definition", name="throttling_process",
    content="Throttling (Joule-Thomson expansion): isenthalpic process (h1 = h2) through a valve or porous plug. For ideal gas: no temperature change. For real gas: temperature may increase or decrease depending on Joule-Thomson coefficient mu_JT = (dT/dP)_H.",
    example="Ideal gas throttled from 10 atm to 1 atm: no temperature change (h depends only on T for ideal gas). Real gas (N2 at 300K): mu_JT > 0, gas cools.",
    tier=5, domain="thermodynamics",
    source="Wikipedia contributors, 'Joule-Thomson effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Joule%E2%80%93Thomson_effect",
    prerequisites=["first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula", name="maxwell_relations",
    content="Maxwell relations derived from thermodynamic potentials: (dT/dV)_S = -(dP/dS)_V, (dT/dP)_S = (dV/dS)_P, (dP/dT)_V = (dS/dV)_T, -(dV/dT)_P = (dS/dP)_T. Derived from equality of mixed partial derivatives.",
    example="From dU = TdS - PdV: (dT/dV)_S = -(dP/dS)_V. For ideal gas PV=nRT: (dP/dS)_V = (dP/dT)_V * (dT/dS)_V = (nR/V) * (T/Cv).",
    tier=6, domain="thermodynamics",
    source="Wikipedia contributors, 'Maxwell relations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maxwell_relations",
    prerequisites=["entropy_change"],
))

register_atom(Atom(
    atom_type="formula", name="van_der_waals",
    content="Van der Waals equation for real gases: (P + a/V^2)(V - b) = RT (per mole), where a accounts for intermolecular attractions and b for molecular volume. Reduces to ideal gas law when a=0, b=0.",
    example="CO2: a=3.59 L^2*atm/mol^2, b=0.0427 L/mol. At T=300K, V=1 L/mol: P = RT/(V-b) - a/V^2 = 0.08206*300/(1-0.0427) - 3.59/1 = 25.72 - 3.59 = 22.13 atm.",
    tier=5, domain="thermodynamics",
    source="Wikipedia contributors, 'Van der Waals equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Van_der_Waals_equation",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula", name="entropy_mixing",
    content="Entropy of mixing for ideal gases: delta_S_mix = -nR * sum(x_i * ln(x_i)), where x_i are mole fractions. Always positive (mixing is spontaneous for ideal solutions).",
    example="Mix 1 mol N2 with 1 mol O2: x1=x2=0.5. delta_S = -2*8.314*(0.5*ln(0.5) + 0.5*ln(0.5)) = -2*8.314*(-0.693) = 11.53 J/K.",
    tier=5, domain="thermodynamics",
    source="Wikipedia contributors, 'Entropy of mixing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Entropy_of_mixing",
    prerequisites=["entropy_change"],
))

# ── Optics Extension ─────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula", name="lens_makers",
    content="Lensmaker's equation: 1/f = (n-1)(1/R1 - 1/R2), where f is focal length, n is refractive index, R1 and R2 are radii of curvature. Sign convention: R positive if center of curvature is to the right.",
    example="Biconvex lens: n=1.5, R1=20cm, R2=-20cm. 1/f = (1.5-1)(1/20 - 1/(-20)) = 0.5*(1/20+1/20) = 0.5*0.1 = 0.05. f = 20 cm.",
    tier=5, domain="optics",
    source="Wikipedia contributors, 'Lensmaker\\'s equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lensmaker%27s_equation",
    prerequisites=["thin_lens"],
))

register_atom(Atom(
    atom_type="formula", name="two_lens_system",
    content="Two thin lenses in contact: 1/f_total = 1/f1 + 1/f2. Separated by distance d: 1/f_total = 1/f1 + 1/f2 - d/(f1*f2). Image from first lens becomes object for second.",
    example="f1=10cm, f2=20cm, in contact: 1/f = 1/10 + 1/20 = 3/20. f = 20/3 = 6.67 cm.",
    tier=5, domain="optics",
    source="Wikipedia contributors, 'Thin lens', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thin_lens",
    prerequisites=["thin_lens"],
))

register_atom(Atom(
    atom_type="formula", name="single_slit_diffraction",
    content="Single slit diffraction: minima at a*sin(theta) = m*lambda (m=1,2,3...), where a is slit width, lambda is wavelength. Central maximum has angular width 2*lambda/a. Intensity: I = I0*(sin(beta)/beta)^2, beta = pi*a*sin(theta)/lambda.",
    example="a=0.1mm, lambda=500nm, first minimum: sin(theta) = lambda/a = 500e-9/0.1e-3 = 0.005. theta = 0.29 degrees.",
    tier=5, domain="optics",
    source="Wikipedia contributors, 'Diffraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diffraction",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula", name="thin_film_interference",
    content="Thin film interference: constructive when 2*n*t = (m+1/2)*lambda (reflected, phase change at one surface), destructive when 2*n*t = m*lambda. Here n is film refractive index, t is thickness.",
    example="Soap film n=1.33, t=200nm, lambda=532nm (green). 2*1.33*200 = 532 nm = 1*532. Destructive interference: green light suppressed, film appears magenta.",
    tier=5, domain="optics",
    source="Wikipedia contributors, 'Thin-film interference', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thin-film_interference",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="definition", name="polarization",
    content="Light polarization: oscillation direction of the electric field. Unpolarized: random directions. Linear: fixed plane. Circular: rotating E-field. Malus's law: I = I0*cos^2(theta) for polarizer at angle theta to polarized light.",
    example="Polarized light I0=100 W/m^2 through polarizer at 30 degrees: I = 100*cos^2(30) = 100*0.75 = 75 W/m^2.",
    tier=4, domain="optics",
    source="Wikipedia contributors, 'Polarization (waves)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Polarization_(waves)",
    prerequisites=["wave_equation"],
))

register_atom(Atom(
    atom_type="formula", name="resolving_power",
    content="Rayleigh criterion: minimum resolvable angle theta = 1.22*lambda/D, where D is aperture diameter. For a telescope, smaller theta means better resolution. Resolving power of a grating: R = m*N, where m is order, N is number of slits.",
    example="Telescope D=10cm, lambda=550nm: theta = 1.22*550e-9/0.1 = 6.71e-6 rad = 1.38 arcsec.",
    tier=5, domain="optics",
    source="Wikipedia contributors, 'Angular resolution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Angular_resolution",
    prerequisites=["single_slit_diffraction"],
))

register_atom(Atom(
    atom_type="formula", name="optical_path_length",
    content="Optical path length OPL = n*d, where n is refractive index and d is geometric path. Two rays interfere constructively when their OPL difference = m*lambda. Fermat's principle: light follows the path of least OPL.",
    example="Glass slab n=1.5, thickness 2cm: OPL = 1.5*2 = 3 cm. Equivalent to 3 cm in vacuum.",
    tier=4, domain="optics",
    source="Wikipedia contributors, 'Optical path length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Optical_path_length",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula", name="mirror_equation",
    content="Mirror equation: 1/f = 1/do + 1/di, where f is focal length (f=R/2 for spherical mirror), do is object distance, di is image distance. Magnification m = -di/do. Concave: f>0, convex: f<0.",
    example="Concave mirror f=10cm, object at do=15cm: 1/di = 1/10 - 1/15 = 1/30. di = 30 cm. m = -30/15 = -2 (inverted, magnified 2x).",
    tier=4, domain="optics",
    source="Wikipedia contributors, 'Curved mirror', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Curved_mirror",
    prerequisites=["thin_lens"],
))

# ── Robotics Extension ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm", name="dh_transform",
    content="Denavit-Hartenberg (DH) convention: each joint is described by 4 parameters (theta, d, a, alpha). The transformation matrix T_i = Rot_z(theta) * Trans_z(d) * Trans_x(a) * Rot_x(alpha). Forward kinematics: T_0n = T_01 * T_12 * ... * T_{n-1,n}.",
    example="2-link planar arm: link 1 (theta1, d=0, a=L1, alpha=0), link 2 (theta2, d=0, a=L2, alpha=0). End-effector: x = L1*cos(theta1) + L2*cos(theta1+theta2).",
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Denavit-Hartenberg parameters', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula", name="jacobian_robot",
    content="The Jacobian matrix J relates joint velocities to end-effector velocities: v = J*dq/dt. For a 2-link planar arm: J = [[-L1*s1-L2*s12, -L2*s12], [L1*c1+L2*c12, L2*c12]], where s1=sin(theta1), c12=cos(theta1+theta2).",
    example="2-link, L1=L2=1, theta1=0, theta2=pi/2: J = [[0,-1],[1,0]]. det(J)=1 (not singular).",
    tier=6, domain="robotics",
    source="Wikipedia contributors, 'Jacobian matrix and determinant', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant",
    prerequisites=["dh_transform", "determinant"],
))

register_atom(Atom(
    atom_type="definition", name="workspace_analysis",
    content="Robot workspace: the set of all points reachable by the end-effector. For a 2-link planar arm with link lengths L1, L2: reachable workspace is annular region |L1-L2| <= r <= L1+L2. Dextrous workspace: points reachable with any orientation.",
    example="L1=3, L2=2: workspace is ring with inner radius 1, outer radius 5. Point at distance 4 is reachable.",
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Workspace (robotics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Workspace_(robotics)",
    prerequisites=["dh_transform"],
))

register_atom(Atom(
    atom_type="algorithm", name="trajectory_planning",
    content="Trajectory planning generates time-parameterised joint positions. Cubic polynomial: q(t) = a0 + a1*t + a2*t^2 + a3*t^3 with boundary conditions on position and velocity at start and end. Quintic polynomial adds acceleration constraints.",
    example="Move from q0=0 to qf=90deg in T=2s, zero velocity at endpoints: q(t) = 3*(90)*(t/2)^2 - 2*(90)*(t/2)^3 = 270*t^2/4 - 180*t^3/8. At t=1: q = 67.5 - 22.5 = 45 deg (halfway).",
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Trajectory planning', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Motion_planning",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="algorithm", name="potential_field",
    content="Artificial potential field for path planning: attractive potential pulls robot toward goal (U_att = 0.5*k_att*d_goal^2), repulsive potential pushes away from obstacles (U_rep = 0.5*k_rep*(1/d_obs - 1/d_0)^2 when d_obs < d_0). Robot follows negative gradient.",
    example="Goal at (10,10), robot at (0,0), k_att=1: F_att = -grad(U_att) = k_att*(goal-pos) = (10,10). Robot moves toward goal.",
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Artificial potential field', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Motion_planning#Artificial_potential_fields",
    prerequisites=["gradient"],
))

register_atom(Atom(
    atom_type="algorithm", name="sensor_fusion",
    content="Sensor fusion combines multiple sensor readings for better state estimation. Kalman filter: predict x_k|k-1 = F*x_{k-1}, update x_k = x_k|k-1 + K*(z_k - H*x_k|k-1), where K is Kalman gain balancing prediction uncertainty vs measurement noise.",
    example="1D position tracking: predict x=10, P=4. Measurement z=11, R=1. K = P/(P+R) = 4/5 = 0.8. Update: x = 10 + 0.8*(11-10) = 10.8.",
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Kalman filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kalman_filter",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="formula", name="odometry",
    content="Wheel odometry estimates robot pose from wheel encoder counts. For differential drive: v = (v_R + v_L)/2, omega = (v_R - v_L)/L, where L is wheel separation. Update: x += v*cos(theta)*dt, y += v*sin(theta)*dt, theta += omega*dt.",
    example="v_R=1 m/s, v_L=0.5 m/s, L=0.5m, dt=1s, initial theta=0: v=0.75, omega=1 rad/s. x=0.75, y=0, theta=1 rad.",
    tier=4, domain="robotics",
    source="Wikipedia contributors, 'Odometry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Odometry",
    prerequisites=["kinematics_velocity"],
))

register_atom(Atom(
    atom_type="formula", name="reward_shaping",
    content="Reward shaping modifies the reward function to accelerate RL learning while preserving optimal policy. Potential-based shaping: F(s,s') = gamma*Phi(s') - Phi(s), where Phi is a potential function. Guarantees same optimal policy as original reward (Ng et al. 1999).",
    example="Grid world, Phi(s) = -Manhattan_distance(s, goal). Moving closer: F = gamma*(-d+1) - (-d) = gamma*(-d+1)+d. Positive reward for approaching goal.",
    tier=6, domain="robotics",
    source="Wikipedia contributors, 'Reward shaping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reward_shaping",
    prerequisites=["q_value_update"],
))
