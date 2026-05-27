"""Atoms for graph algorithms, data structures, and recursion."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Graph Algorithms ────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="bfs_order",
    content="Breadth-first search (BFS) explores a graph level by level. Starting from a source "
    "node, visit all neighbours first, then neighbours of neighbours. Uses a queue: enqueue source, "
    "dequeue a node, enqueue its unvisited neighbours. BFS finds shortest paths in unweighted graphs.",
    tier=3, domain="graph_theory",
    source="Wikipedia contributors, 'Breadth-first search', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Breadth-first_search",
    prerequisites=["graph_reach"]))

register_atom(Atom(atom_type="algorithm", name="dfs_order",
    content="Depth-first search (DFS) explores as far as possible along each branch before "
    "backtracking. Uses a stack (or recursion): push source, pop a node, push its unvisited "
    "neighbours. DFS is used for topological sorting, cycle detection, and connected components.",
    tier=3, domain="graph_theory",
    source="Wikipedia contributors, 'Depth-first search', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Depth-first_search",
    prerequisites=["graph_reach"]))

register_atom(Atom(atom_type="algorithm", name="connected_components",
    content="A connected component is a maximal set of vertices where every pair is connected by "
    "a path. Algorithm: run BFS/DFS from each unvisited vertex; each run discovers one component. "
    "An undirected graph with n vertices and k components has at least n-k edges.",
    tier=3, domain="graph_theory",
    source="Wikipedia contributors, 'Component (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Component_(graph_theory)",
    prerequisites=["bfs_order"]))

register_atom(Atom(atom_type="algorithm", name="minimum_spanning_tree",
    content="A minimum spanning tree (MST) connects all vertices with minimum total edge weight. "
    "Kruskal's algorithm: sort edges by weight, add each edge if it doesn't create a cycle. "
    "Prim's algorithm: grow the tree from a start vertex, always adding the cheapest edge to "
    "an unvisited vertex. An MST of n vertices has exactly n-1 edges.",
    tier=4, domain="graph_theory",
    source="Wikipedia contributors, 'Minimum spanning tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Minimum_spanning_tree",
    prerequisites=["connected_components"]))

register_atom(Atom(atom_type="algorithm", name="graph_coloring",
    content="Graph coloring assigns colors to vertices such that no two adjacent vertices share "
    "a color. The chromatic number chi(G) is the minimum colors needed. Greedy coloring: process "
    "vertices in order, assign the smallest color not used by neighbours. Complete graph K_n needs "
    "n colors. Every planar graph needs at most 4 colors (four color theorem).",
    tier=4, domain="graph_theory",
    source="Wikipedia contributors, 'Graph coloring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Graph_coloring",
    prerequisites=["graph_reach"]))

register_atom(Atom(atom_type="algorithm", name="bipartite_check",
    content="A graph is bipartite if its vertices can be divided into two sets such that every "
    "edge connects vertices in different sets. Equivalently, a graph is bipartite iff it contains "
    "no odd-length cycle. Algorithm: BFS/DFS with 2-coloring; if a conflict arises, the graph is "
    "not bipartite.",
    tier=4, domain="graph_theory",
    source="Wikipedia contributors, 'Bipartite graph', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bipartite_graph",
    prerequisites=["bfs_order", "graph_coloring"]))

# ── Data Structures ─────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="stack_operations",
    content="A stack is a LIFO (last in, first out) data structure. Operations: push(x) adds to "
    "top, pop() removes and returns top, peek() returns top without removing. "
    "Applications: function call stack, expression evaluation (RPN), undo operations, DFS.",
    tier=2, domain="computer_science",
    source="Wikipedia contributors, 'Stack (abstract data type)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stack_(abstract_data_type)"))

register_atom(Atom(atom_type="algorithm", name="queue_operations",
    content="A queue is a FIFO (first in, first out) data structure. Operations: enqueue(x) adds "
    "to back, dequeue() removes and returns front. Applications: BFS, task scheduling, "
    "print spooling. A priority queue dequeues the highest-priority element.",
    tier=2, domain="computer_science",
    source="Wikipedia contributors, 'Queue (abstract data type)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Queue_(abstract_data_type)"))

register_atom(Atom(atom_type="algorithm", name="binary_tree_traversal",
    content="Three traversal orders for a binary tree: "
    "Inorder (left, root, right) — gives sorted order for BST. "
    "Preorder (root, left, right) — useful for copying/serialising. "
    "Postorder (left, right, root) — useful for deletion and expression evaluation.",
    tier=3, domain="computer_science",
    source="Wikipedia contributors, 'Tree traversal', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tree_traversal",
    prerequisites=["stack_operations"]))

register_atom(Atom(atom_type="algorithm", name="heap_operations",
    content="A binary min-heap is a complete binary tree where each node is <= its children. "
    "Insert: add at end, bubble up. Extract-min: remove root, move last to root, bubble down. "
    "Both operations are O(log n). Heapsort: build heap, then extract-min n times.",
    tier=3, domain="computer_science",
    source="Wikipedia contributors, 'Binary heap', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_heap",
    prerequisites=["sorting"]))

register_atom(Atom(atom_type="algorithm", name="hash_table_ops",
    content="A hash table maps keys to values using a hash function: index = hash(key) % size. "
    "Collision resolution: chaining (linked list at each index) or open addressing (probe next "
    "slot). Average O(1) lookup, insert, delete. Worst case O(n) if all keys collide.",
    tier=3, domain="computer_science",
    source="Wikipedia contributors, 'Hash table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hash_table"))

# ── Recursion ───────────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="recursive_trace",
    content="Tracing a recursive function: follow each call, noting the argument and return value. "
    "Each call creates a new stack frame. The base case terminates recursion. "
    "Example: factorial(3) calls factorial(2) calls factorial(1) returns 1, then 2*1=2, then 3*2=6.",
    tier=2, domain="computer_science",
    source="Wikipedia contributors, 'Recursion (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recursion_(computer_science)"))

register_atom(Atom(atom_type="algorithm", name="base_case_identify",
    content="Every recursive function needs a base case — a condition where it returns without "
    "making a recursive call. Without it, recursion is infinite. Identifying the base case: "
    "find the simplest input where the answer is known directly (e.g., factorial(0)=1, "
    "fibonacci(0)=0, fibonacci(1)=1, empty list = []).",
    tier=2, domain="computer_science",
    source="Wikipedia contributors, 'Recursion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recursion",
    prerequisites=["recursive_trace"]))

register_atom(Atom(atom_type="algorithm", name="call_stack_depth",
    content="The call stack depth equals the maximum number of nested recursive calls before "
    "a base case is reached. For factorial(n), depth is n. For fibonacci(n) with naive recursion, "
    "depth is n but total calls is O(2^n). Stack overflow occurs when depth exceeds system limit.",
    tier=3, domain="computer_science",
    source="Wikipedia contributors, 'Call stack', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Call_stack",
    prerequisites=["recursive_trace"]))

register_atom(Atom(atom_type="algorithm", name="memoisation",
    content="Memoisation stores results of expensive function calls and returns the cached result "
    "when the same inputs occur again. For fibonacci: without memo, fib(n) takes O(2^n); with memo, "
    "O(n). Applicable when a function has overlapping subproblems and optimal substructure.",
    tier=3, domain="computer_science",
    source="Wikipedia contributors, 'Memoization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Memoization",
    prerequisites=["recursive_trace", "call_stack_depth"]))
