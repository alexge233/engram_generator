"""Knowledge atoms for data structures, graph algorithms, and economics extensions.

Covers BST operations, balanced trees, graph algorithms (Bellman-Ford,
Floyd-Warshall, articulation points, SCC), and economics concepts
(marginal analysis, consumer surplus, multiplier effect).
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Data Structures (tiers 3-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="bst_insert",
    content=(
        "Binary search tree insertion places a new key by comparing it "
        "with the current node: if smaller, recurse left; if larger, "
        "recurse right; insert at the first empty position. Average "
        "time complexity is O(log n), worst case O(n) for a skewed tree."
    ),
    example=(
        "Insert 5 into BST [3, 7, 1, 4]: compare 5 > 3 (go right), "
        "5 < 7 (go left), 5 > 4 (go right of 4). Result: 4.right = 5."
    ),
    tier=3,
    domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bst_delete",
    content=(
        "BST deletion has three cases: (1) leaf node: remove directly; "
        "(2) one child: replace node with its child; (3) two children: "
        "replace with in-order successor (smallest in right subtree) or "
        "in-order predecessor (largest in left subtree), then delete "
        "the successor/predecessor from its original position."
    ),
    example=(
        "Delete 3 from BST [5, 3, 7, 1, 4]: node 3 has two children "
        "(1 and 4). In-order successor is 4. Replace 3 with 4, remove "
        "old 4. Result: [5, 4, 7, 1]."
    ),
    tier=4,
    domain="data_structures",
    source="Wikipedia contributors, 'Binary search tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_tree#Deletion",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="avl_rotation",
    content=(
        "An AVL tree maintains balance by ensuring the height difference "
        "between left and right subtrees (balance factor) is at most 1. "
        "When insertion or deletion causes imbalance, rotations restore "
        "balance: left rotation, right rotation, left-right (double), "
        "and right-left (double). A right rotation on node q with left "
        "child p: p becomes the new root, q becomes p's right child, "
        "and p's old right child becomes q's left child."
    ),
    example=(
        "Insert 1, 2, 3 into AVL: after inserting 3, node 1 has "
        "balance factor -2. Left rotation on 1: 2 becomes root, "
        "1 becomes left child, 3 stays right child. Result: [2, 1, 3]."
    ),
    tier=5,
    domain="data_structures",
    source="Wikipedia contributors, 'AVL tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/AVL_tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="red_black_insert",
    content=(
        "A red-black tree is a self-balancing BST with properties: "
        "(1) every node is red or black; (2) root is black; (3) all "
        "leaves (NIL) are black; (4) red nodes have only black children; "
        "(5) every path from root to leaf has the same number of black "
        "nodes. After insertion (new node is red), fix violations by "
        "recoloring and rotations. Three cases based on the uncle's color."
    ),
    example=(
        "Insert 4 into RB tree [2(B), 1(B), 3(B)]: 4 is red, parent 3 "
        "is black, no violation. Result: [2(B), 1(B), 3(B), -, -, -, 4(R)]."
    ),
    tier=5,
    domain="data_structures",
    source="Wikipedia contributors, 'Red-black tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Red%E2%80%93black_tree",
    prerequisites=["bst_insert", "avl_rotation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="b_tree_insert",
    content=(
        "A B-tree of order m is a self-balancing tree where each node "
        "has at most m children and at least ceil(m/2) children (except "
        "root). Insertion: find the correct leaf, insert the key; if the "
        "node overflows (more than m-1 keys), split it into two nodes "
        "and push the median key up to the parent. Splits may propagate "
        "up to the root, increasing tree height."
    ),
    example=(
        "B-tree order 3, insert keys 1,2,3: after inserting 3, leaf "
        "[1,2,3] overflows. Split: left=[1], right=[3], push 2 up. "
        "New root: [2] with children [1] and [3]."
    ),
    tier=5,
    domain="data_structures",
    source="Wikipedia contributors, 'B-tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/B-tree",
    prerequisites=["bst_insert"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="trie_operations",
    content=(
        "A trie (prefix tree) stores strings character by character, "
        "with each node representing a prefix. Insertion traverses the "
        "trie creating nodes for new characters. Search follows the "
        "path matching the query string. Lookup is O(m) where m is the "
        "string length, independent of the number of stored strings."
    ),
    example=(
        "Insert 'cat', 'car', 'do' into empty trie: root -> c -> a -> "
        "t (end), root -> c -> a -> r (end), root -> d -> o (end). "
        "Search 'car': follow c -> a -> r, found. Search 'cab': follow "
        "c -> a, no 'b' child, not found."
    ),
    tier=4,
    domain="data_structures",
    source="Wikipedia contributors, 'Trie', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trie",
    prerequisites=["string_reverse"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="skip_list",
    content=(
        "A skip list is a probabilistic data structure that allows "
        "O(log n) average search, insertion, and deletion. It consists "
        "of multiple layers of sorted linked lists. The bottom layer "
        "contains all elements; each higher layer contains a random "
        "subset. Search starts at the top layer and drops down when "
        "the next element exceeds the target."
    ),
    example=(
        "Skip list with elements [1, 3, 5, 7, 9]. Level 2: [1, 5, 9]. "
        "Level 1: [1, 3, 5, 7, 9]. Search for 7: start at L2, 1 < 7, "
        "5 < 7, 9 > 7 drop to L1 at 5, 7 = 7 found."
    ),
    tier=5,
    domain="data_structures",
    source="Wikipedia contributors, 'Skip list', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Skip_list",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bloom_filter",
    content=(
        "A Bloom filter is a space-efficient probabilistic data structure "
        "that tests set membership. It uses k hash functions mapping "
        "elements to positions in a bit array of size m. Insert: set "
        "all k positions to 1. Query: check if all k positions are 1. "
        "False positives are possible; false negatives are not. The "
        "false positive rate is approximately (1 - e^(-kn/m))^k where "
        "n is the number of inserted elements."
    ),
    example=(
        "Bloom filter m=10, k=2, h1(x)=x mod 10, h2(x)=(3x+1) mod 10. "
        "Insert 'cat' (hash 3,7): set bits 3,7. Query 'dog' (hash 5,2): "
        "bits 5,2 are 0, definitely not in set."
    ),
    tier=4,
    domain="data_structures",
    source="Wikipedia contributors, 'Bloom filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bloom_filter",
    prerequisites=["polynomial_hash"],
))


# ---------------------------------------------------------------------------
# Graph Algorithms (tiers 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="bellman_ford",
    content=(
        "The Bellman-Ford algorithm computes shortest paths from a single "
        "source to all vertices in a weighted directed graph. Unlike "
        "Dijkstra's, it handles negative edge weights. It relaxes all "
        "edges |V|-1 times. If any edge can still be relaxed after |V|-1 "
        "iterations, the graph contains a negative-weight cycle. Time "
        "complexity: O(|V| * |E|)."
    ),
    example=(
        "Graph: A->B(4), A->C(2), B->C(-3), C->D(1). Source A. "
        "Init: d(A)=0, d(B)=inf, d(C)=inf, d(D)=inf. "
        "Iter 1: d(B)=4, d(C)=min(2, 4-3)=1, d(D)=2. "
        "Shortest: A=0, B=4, C=1, D=2."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Bellman-Ford algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="floyd_warshall",
    content=(
        "The Floyd-Warshall algorithm finds shortest paths between all "
        "pairs of vertices in a weighted graph. It uses dynamic "
        "programming with the recurrence: dist[i][j] = min(dist[i][j], "
        "dist[i][k] + dist[k][j]) for each intermediate vertex k. "
        "Time complexity: O(|V|^3). Handles negative weights but not "
        "negative cycles."
    ),
    example=(
        "3 vertices, edges: 1->2(3), 1->3(8), 2->3(2). "
        "Init: d[1][2]=3, d[1][3]=8, d[2][3]=2. "
        "k=2: d[1][3] = min(8, 3+2) = 5. "
        "Result: d[1][2]=3, d[1][3]=5, d[2][3]=2."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Floyd-Warshall algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="articulation_point",
    content=(
        "An articulation point (cut vertex) is a vertex whose removal "
        "disconnects the graph. Found using DFS: a vertex u is an "
        "articulation point if (1) u is the root of the DFS tree and has "
        "two or more children, or (2) u is not root and has a child v "
        "such that no vertex in the subtree rooted at v has a back edge "
        "to an ancestor of u (low[v] >= disc[u])."
    ),
    example=(
        "Graph: 0-1, 1-2, 2-0, 1-3, 3-4. DFS from 0: disc=[0,1,2,3,4], "
        "low=[0,0,0,3,3]. Vertex 1: child 3 has low[3]=3 >= disc[1]=1, "
        "so 1 is an articulation point. Vertex 3: child 4 has low[4]=3 "
        ">= disc[3]=3, so 3 is an articulation point."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Biconnected component', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biconnected_component",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="strongly_connected",
    content=(
        "A strongly connected component (SCC) of a directed graph is a "
        "maximal set of vertices such that there is a path from each "
        "vertex to every other vertex in the set. Tarjan's algorithm "
        "finds all SCCs in O(|V| + |E|) using a single DFS pass. It "
        "maintains a stack and assigns each vertex a 'lowlink' value "
        "indicating the smallest reachable index."
    ),
    example=(
        "Directed graph: 0->1, 1->2, 2->0, 2->3, 3->4, 4->3. "
        "SCCs: {0,1,2} (cycle 0->1->2->0) and {3,4} (cycle 3->4->3)."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Tarjan's strongly connected components algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm",
    prerequisites=["graph_reach", "topo_sort"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="graph_matching",
    content=(
        "A matching in a graph is a set of edges without common vertices. "
        "A maximum matching has the largest possible number of edges. "
        "In bipartite graphs, the Hungarian algorithm finds a maximum "
        "matching in O(|V|^3). The Hopcroft-Karp algorithm achieves "
        "O(|E| * sqrt(|V|)). By Konig's theorem, the size of the maximum "
        "matching in a bipartite graph equals the size of the minimum "
        "vertex cover."
    ),
    example=(
        "Bipartite graph: L={a,b,c}, R={1,2,3}. Edges: a-1, a-2, b-2, "
        "c-3. Maximum matching: {a-1, b-2, c-3} (size 3, perfect matching)."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Matching (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matching_(graph_theory)",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="network_flow_detail",
    content=(
        "The maximum flow problem finds the greatest flow from source s "
        "to sink t in a flow network without exceeding edge capacities. "
        "The Ford-Fulkerson method repeatedly finds augmenting paths in "
        "the residual graph and pushes flow along them. The max-flow "
        "min-cut theorem states that the maximum flow equals the minimum "
        "cut capacity. The Edmonds-Karp variant uses BFS for augmenting "
        "paths, achieving O(|V| * |E|^2)."
    ),
    example=(
        "Network: s->a(10), s->b(5), a->b(15), a->t(5), b->t(10). "
        "Path s->a->t: flow 5. Path s->b->t: flow 5. Path s->a->b->t: "
        "flow 5. Max flow = 15."
    ),
    tier=6,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Maximum flow problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_flow_problem",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="topological_sort_dfs",
    content=(
        "Topological sort of a directed acyclic graph (DAG) produces a "
        "linear ordering of vertices such that for every directed edge "
        "u->v, u comes before v. The DFS-based algorithm visits each "
        "vertex, recursively processes all neighbors, then prepends the "
        "vertex to the result. A graph has a topological order iff it "
        "is a DAG (no cycles)."
    ),
    example=(
        "DAG: A->C, B->C, C->D. DFS from A: visit C, visit D (no "
        "neighbors, push D), push C, push A. DFS from B: push B. "
        "Topological order: [B, A, C, D]."
    ),
    tier=5,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Topological sorting', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Topological_sorting",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="graph_coloring_greedy",
    content=(
        "Graph coloring assigns colors to vertices such that no two "
        "adjacent vertices share a color. The greedy algorithm processes "
        "vertices in order, assigning the smallest color not used by "
        "any neighbor. The greedy algorithm uses at most d+1 colors "
        "where d is the maximum degree. The chromatic number chi(G) is "
        "the minimum number of colors needed."
    ),
    example=(
        "Graph: A-B, B-C, C-A, C-D. Greedy order [A,B,C,D]: "
        "A=1, B=2 (A is neighbor), C=3 (A,B are neighbors), "
        "D=1 (only C is neighbor, C=3). Uses 3 colors = chi(K3) = 3."
    ),
    tier=4,
    domain="graph_algorithms",
    source="Wikipedia contributors, 'Greedy coloring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Greedy_coloring",
    prerequisites=["graph_reach"],
))


# ---------------------------------------------------------------------------
# Economics (tiers 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="marginal_analysis",
    content=(
        "Marginal analysis examines the additional benefit or cost of "
        "one more unit. Marginal cost (MC) is the derivative of total "
        "cost with respect to quantity: MC = dTC/dQ. Marginal revenue "
        "(MR) is the derivative of total revenue: MR = dTR/dQ. Profit "
        "is maximized where MR = MC."
    ),
    example=(
        "TC(Q) = 100 + 5Q + 0.5Q^2. MC = dTC/dQ = 5 + Q. "
        "TR(Q) = 20Q. MR = 20. Profit max: 20 = 5 + Q, Q = 15."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Marginal cost', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Marginal_cost",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="consumer_surplus",
    content=(
        "Consumer surplus is the difference between what consumers are "
        "willing to pay and what they actually pay. For a linear demand "
        "curve P = a - bQ and market price P*, consumer surplus = "
        "0.5 * (a - P*) * Q*, forming a triangle above the price line "
        "and below the demand curve."
    ),
    example=(
        "Demand: P = 100 - 2Q. Market price P* = 40. "
        "Q* = (100 - 40) / 2 = 30. "
        "CS = 0.5 * (100 - 40) * 30 = 0.5 * 60 * 30 = 900."
    ),
    tier=5,
    domain="economics",
    source="Wikipedia contributors, 'Consumer surplus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Consumer_surplus",
    prerequisites=["area_triangle"],
))

register_atom(Atom(
    atom_type="formula",
    name="multiplier_effect",
    content=(
        "The fiscal multiplier measures the total change in output "
        "resulting from a change in government spending or taxation. "
        "The simple Keynesian multiplier is k = 1/(1 - MPC), where "
        "MPC is the marginal propensity to consume. A change in "
        "spending deltaG produces a total output change of k * deltaG."
    ),
    example=(
        "MPC = 0.8. Multiplier k = 1/(1 - 0.8) = 1/0.2 = 5. "
        "Government spending increases by 100. Total output change = "
        "5 * 100 = 500."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Fiscal multiplier', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fiscal_multiplier",
    prerequisites=["geometric_sequence"],
))

register_atom(Atom(
    atom_type="formula",
    name="exchange_rate",
    content=(
        "Exchange rate conversion transforms a value from one currency "
        "to another. If the exchange rate from currency A to B is r, "
        "then amount_B = amount_A * r. The real exchange rate adjusts "
        "for price levels: e_real = e_nominal * (P_domestic / P_foreign)."
    ),
    example=(
        "USD/EUR rate = 0.85. Convert 1000 USD to EUR: "
        "1000 * 0.85 = 850 EUR. Convert back: 850 / 0.85 = 1000 USD."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Exchange rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exchange_rate",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="inflation_real_rate",
    content=(
        "The Fisher equation relates nominal interest rate (i), real "
        "interest rate (r), and inflation rate (pi): 1 + i = (1 + r)(1 + pi), "
        "or approximately i = r + pi for small rates. The real interest "
        "rate measures the return after adjusting for inflation."
    ),
    example=(
        "Nominal rate i = 8%, inflation pi = 3%. "
        "Real rate r = (1.08/1.03) - 1 = 0.0485 = 4.85%. "
        "Approximation: r = 8% - 3% = 5%."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Fisher equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fisher_equation",
    prerequisites=["percentage"],
))

register_atom(Atom(
    atom_type="formula",
    name="production_function",
    content=(
        "A production function relates inputs to output. The Cobb-Douglas "
        "production function is Y = A * L^alpha * K^beta, where Y is "
        "output, A is total factor productivity, L is labor, K is capital, "
        "and alpha + beta indicates returns to scale (= 1 for constant "
        "returns). Marginal product of labor: MPL = alpha * Y / L."
    ),
    example=(
        "Y = 2 * L^0.6 * K^0.4. Given L=100, K=50: "
        "Y = 2 * 100^0.6 * 50^0.4 = 2 * 15.849 * 6.31 = 200.0."
    ),
    tier=5,
    domain="economics",
    source="Wikipedia contributors, 'Cobb-Douglas production function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="game_theory_market",
    content=(
        "In Cournot competition, firms simultaneously choose quantities. "
        "With two firms, inverse demand P = a - b(q1 + q2), and constant "
        "marginal cost c, each firm's best response is qi = (a - c - b*qj)/(2b). "
        "The Nash equilibrium has q1 = q2 = (a - c)/(3b)."
    ),
    example=(
        "P = 100 - (q1 + q2), MC = 10. Best response: qi = (100 - 10 - qj)/2 "
        "= (90 - qj)/2. Nash: q1 = q2 = 90/3 = 30. P = 100 - 60 = 40."
    ),
    tier=5,
    domain="economics",
    source="Wikipedia contributors, 'Cournot competition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cournot_competition",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="formula",
    name="time_value_money",
    content=(
        "The time value of money states that a sum of money today is "
        "worth more than the same sum in the future due to its potential "
        "earning capacity. Future value: FV = PV * (1 + r)^n. Present "
        "value: PV = FV / (1 + r)^n. Annuity present value: "
        "PV = PMT * [1 - (1 + r)^(-n)] / r."
    ),
    example=(
        "PV = 1000, r = 5% = 0.05, n = 10 years. "
        "FV = 1000 * (1.05)^10 = 1000 * 1.6289 = 1628.89."
    ),
    tier=4,
    domain="economics",
    source="Wikipedia contributors, 'Time value of money', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time_value_of_money",
    prerequisites=["compound_interest"],
))
