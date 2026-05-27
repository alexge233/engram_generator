"""Graph algorithms, data structures, and recursion generators.

Adds 15 generators: 6 graph (tiers 3-4), 5 data structures (tiers 2-3),
4 recursion (tiers 2-3).
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# GRAPH ALGORITHMS (6 generators, tiers 3-4)
# ═══════════════════════════════════════════════════════════════════

def _random_graph(rng, n, edge_prob=0.4):
    """Generate a random undirected graph as adjacency list."""
    adj = {i: [] for i in range(n)}
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < edge_prob:
                adj[i].append(j)
                adj[j].append(i)
                edges.append((i, j))
    return adj, edges


@register
class BFSOrderGenerator(StepGenerator):
    """Produce BFS traversal order from a source vertex."""

    @property
    def task_name(self) -> str:
        return "bfs_order"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["graph_reach"]

    def task_description(self, difficulty: int) -> str:
        return "BFS traversal order"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 10)
        adj, edges = _random_graph(self._rng, n, 0.4)
        source = 0
        visited = []
        queue = [source]
        seen = {source}
        while queue:
            node = queue.pop(0)
            visited.append(node)
            for nb in sorted(adj[node]):
                if nb not in seen:
                    seen.add(nb)
                    queue.append(nb)
        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        return (
            f"BFS from {source}: vertices=0..{n-1} edges=[{edge_str}]",
            {"source": source, "order": visited, "n": n},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"visit {v}" for v in sd["order"]]

    def _create_answer(self, sd: dict) -> str:
        return " ".join(str(v) for v in sd["order"])


@register
class DFSOrderGenerator(StepGenerator):
    """Produce DFS traversal order from a source vertex."""

    @property
    def task_name(self) -> str:
        return "dfs_order"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["graph_reach"]

    def task_description(self, difficulty: int) -> str:
        return "DFS traversal order"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 10)
        adj, edges = _random_graph(self._rng, n, 0.4)
        source = 0
        visited = []
        stack = [source]
        seen = {source}
        while stack:
            node = stack.pop()
            visited.append(node)
            for nb in sorted(adj[node], reverse=True):
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        return (
            f"DFS from {source}: vertices=0..{n-1} edges=[{edge_str}]",
            {"source": source, "order": visited, "n": n},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"visit {v}" for v in sd["order"]]

    def _create_answer(self, sd: dict) -> str:
        return " ".join(str(v) for v in sd["order"])


@register
class ConnectedComponentsGenerator(StepGenerator):
    """Count connected components in an undirected graph."""

    @property
    def task_name(self) -> str:
        return "connected_components"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["bfs_order"]

    def task_description(self, difficulty: int) -> str:
        return "count connected components"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(5 + difficulty, 12)
        adj, edges = _random_graph(self._rng, n, 0.25)
        seen = set()
        components = []
        for v in range(n):
            if v not in seen:
                comp = []
                queue = [v]
                seen.add(v)
                while queue:
                    node = queue.pop(0)
                    comp.append(node)
                    for nb in adj[node]:
                        if nb not in seen:
                            seen.add(nb)
                            queue.append(nb)
                components.append(sorted(comp))
        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"n": n, "components": components, "count": len(components)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"component {i}: {c}" for i, c in enumerate(sd["components"])]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["count"])


@register
class MinimumSpanningTreeGenerator(StepGenerator):
    """Find MST weight using Kruskal's algorithm."""

    @property
    def task_name(self) -> str:
        return "minimum_spanning_tree"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["connected_components", "sorting"]

    def task_description(self, difficulty: int) -> str:
        return "find MST weight"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        weighted_edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < 0.5:
                    w = self._rng.randint(1, 10 * difficulty)
                    weighted_edges.append((w, i, j))
        for i in range(n - 1):
            if not any(e for e in weighted_edges if (e[1] == i and e[2] == i+1) or (e[1] == i+1 and e[2] == i)):
                weighted_edges.append((self._rng.randint(1, 10), i, i + 1))

        weighted_edges.sort()
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        mst_weight = 0
        mst_edges = []
        for w, u, v in weighted_edges:
            pu, pv = find(u), find(v)
            if pu != pv:
                parent[pu] = pv
                mst_weight += w
                mst_edges.append((u, v, w))
        edge_str = ", ".join(f"{u}-{v}(w={w})" for w, u, v in weighted_edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"mst_edges": mst_edges, "mst_weight": mst_weight},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"add {u}-{v} (w={w})" for u, v, w in sd["mst_edges"]]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["mst_weight"])


@register
class GraphColoringGenerator(StepGenerator):
    """Greedy-color a graph and report the number of colors used."""

    @property
    def task_name(self) -> str:
        return "graph_coloring"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["graph_reach"]

    def task_description(self, difficulty: int) -> str:
        return "greedy graph coloring"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        adj, edges = _random_graph(self._rng, n, 0.45)
        colors = {}
        for v in range(n):
            used = {colors[nb] for nb in adj[v] if nb in colors}
            c = 0
            while c in used:
                c += 1
            colors[v] = c
        n_colors = max(colors.values()) + 1 if colors else 0
        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"colors": colors, "n_colors": n_colors},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"vertex {v}: color {c}" for v, c in sorted(sd["colors"].items())]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['n_colors']} colors"


@register
class BipartiteCheckGenerator(StepGenerator):
    """Check if a graph is bipartite via 2-coloring."""

    @property
    def task_name(self) -> str:
        return "bipartite_check"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["bfs_order"]

    def task_description(self, difficulty: int) -> str:
        return "check if bipartite"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        adj, edges = _random_graph(self._rng, n, 0.35)
        color = [-1] * n
        bipartite = True
        for start in range(n):
            if color[start] != -1:
                continue
            queue = [start]
            color[start] = 0
            while queue and bipartite:
                node = queue.pop(0)
                for nb in adj[node]:
                    if color[nb] == -1:
                        color[nb] = 1 - color[node]
                        queue.append(nb)
                    elif color[nb] == color[node]:
                        bipartite = False
        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"bipartite": bipartite, "coloring": color},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"vertex {i}: side {c}" for i, c in enumerate(sd["coloring"]) if c >= 0]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["bipartite"] else "NO"


# ═══════════════════════════════════════════════════════════════════
# DATA STRUCTURES (5 generators, tiers 2-3)
# ═══════════════════════════════════════════════════════════════════

@register
class StackOperationsGenerator(StepGenerator):
    """Simulate a sequence of stack push/pop operations."""

    @property
    def task_name(self) -> str:
        return "stack_operations"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate stack"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(4 + difficulty * 2, 12)
        ops = []
        stack = []
        pops = []
        for _ in range(n_ops):
            if not stack or self._rng.random() < 0.6:
                val = self._rng.randint(1, 50)
                ops.append(f"push({val})")
                stack.append(val)
            else:
                v = stack.pop()
                ops.append("pop()")
                pops.append(v)
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "stack": stack, "pops": pops}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        top = sd["stack"][-1] if sd["stack"] else "empty"
        return f"top={top}, popped={sd['pops']}"


@register
class QueueOperationsGenerator(StepGenerator):
    """Simulate a sequence of queue enqueue/dequeue operations."""

    @property
    def task_name(self) -> str:
        return "queue_operations"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate queue"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(4 + difficulty * 2, 12)
        ops = []
        queue = []
        dequeued = []
        for _ in range(n_ops):
            if not queue or self._rng.random() < 0.6:
                val = self._rng.randint(1, 50)
                ops.append(f"enq({val})")
                queue.append(val)
            else:
                v = queue.pop(0)
                ops.append("deq()")
                dequeued.append(v)
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "queue": queue, "dequeued": dequeued}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        front = sd["queue"][0] if sd["queue"] else "empty"
        return f"front={front}, dequeued={sd['dequeued']}"


@register
class BinaryTreeTraversalGenerator(StepGenerator):
    """Produce inorder/preorder/postorder traversal of a binary tree."""

    @property
    def task_name(self) -> str:
        return "binary_tree_traversal"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["stack_operations"]

    def task_description(self, difficulty: int) -> str:
        return "binary tree traversal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 7)
        values = self._rng.sample(range(1, 50), n)
        root = values[0]
        tree = {root: [None, None]}
        nodes = [root]
        for v in values[1:]:
            parent = self._rng.choice(nodes)
            side = 0 if tree[parent][0] is None else (1 if tree[parent][1] is None else -1)
            if side == -1:
                parent = self._rng.choice([p for p in nodes if tree[p][0] is None or tree[p][1] is None])
                side = 0 if tree[parent][0] is None else 1
            tree[parent][side] = v
            tree[v] = [None, None]
            nodes.append(v)

        def inorder(node):
            if node is None: return []
            return inorder(tree[node][0]) + [node] + inorder(tree[node][1])
        def preorder(node):
            if node is None: return []
            return [node] + preorder(tree[node][0]) + preorder(tree[node][1])
        def postorder(node):
            if node is None: return []
            return postorder(tree[node][0]) + postorder(tree[node][1]) + [node]

        mode = self._rng.choice(["inorder", "preorder", "postorder"])
        if mode == "inorder": result = inorder(root)
        elif mode == "preorder": result = preorder(root)
        else: result = postorder(root)

        tree_str = ", ".join(f"{k}:[{tree[k][0]},{tree[k][1]}]" for k in sorted(tree.keys()))
        return (
            f"{mode} of tree root={root}: {tree_str}",
            {"mode": mode, "result": result, "root": root},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"{sd['mode']}: visit {v}" for v in sd["result"]]

    def _create_answer(self, sd: dict) -> str:
        return " ".join(str(v) for v in sd["result"])


@register
class HeapOperationsGenerator(StepGenerator):
    """Simulate insert and extract-min on a min-heap."""

    @property
    def task_name(self) -> str:
        return "heap_operations"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate min-heap"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        import heapq
        n_ops = min(4 + difficulty * 2, 10)
        heap = []
        ops = []
        extracted = []
        for _ in range(n_ops):
            if not heap or self._rng.random() < 0.6:
                val = self._rng.randint(1, 100)
                heapq.heappush(heap, val)
                ops.append(f"insert({val})")
            else:
                v = heapq.heappop(heap)
                extracted.append(v)
                ops.append("extract_min()")
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "heap": sorted(heap), "extracted": extracted}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        top = sd["heap"][0] if sd["heap"] else "empty"
        return f"min={top}, extracted={sd['extracted']}"


@register
class HashTableOpsGenerator(StepGenerator):
    """Simulate hash table insert and lookup."""

    @property
    def task_name(self) -> str:
        return "hash_table_ops"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        return "simulate hash table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = min(5 + difficulty, 11)
        n_inserts = min(3 + difficulty, 8)
        table = [None] * size
        ops = []
        for _ in range(n_inserts):
            key = self._rng.randint(1, 100)
            idx = key % size
            ops.append(f"insert({key}) -> slot {idx}")
            if table[idx] is None:
                table[idx] = [key]
            else:
                table[idx].append(key)
        query = self._rng.choice([op.split("(")[1].split(")")[0] for op in ops])
        query = int(query)
        found = any(query in (slot or []) for slot in table)
        return (
            f"size={size}, ops: {'; '.join(ops)}. lookup({query})?",
            {"table": table, "query": query, "found": found, "slot": query % size},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"hash({sd['query']}) = {sd['query']} % {len(sd['table'])} = {sd['slot']}",
                f"check slot {sd['slot']}: {sd['table'][sd['slot']]}"]

    def _create_answer(self, sd: dict) -> str:
        return "FOUND" if sd["found"] else "NOT FOUND"


# ═══════════════════════════════════════════════════════════════════
# RECURSION (4 generators, tiers 2-3)
# ═══════════════════════════════════════════════════════════════════

@register
class RecursiveTraceGenerator(StepGenerator):
    """Trace the execution of a recursive function."""

    @property
    def task_name(self) -> str:
        return "recursive_trace"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "trace recursive function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["factorial", "sum_to_n", "power"])
        n = self._rng.randint(2, min(6, 2 + difficulty))
        if fn == "factorial":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = 1
            for i in range(1, n + 1):
                result *= i
            desc = f"f(n) = n * f(n-1), f(0) = 1"
        elif fn == "sum_to_n":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = n * (n + 1) // 2
            desc = f"f(n) = n + f(n-1), f(0) = 0"
        else:
            base = self._rng.randint(2, 4)
            calls = [f"f({base},{i})" for i in range(n, -1, -1)]
            result = base ** n
            desc = f"f(b,n) = b * f(b,n-1), f(b,0) = 1"
        return f"{desc}, compute f({n})", {"fn": fn, "n": n, "calls": calls, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class BaseCaseIdentifyGenerator(StepGenerator):
    """Identify the base case of a recursive definition."""

    @property
    def task_name(self) -> str:
        return "base_case_identify"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        return "identify base case"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        defs = [
            ("f(n) = n * f(n-1)", "f(0) = 1", "factorial"),
            ("f(n) = f(n-1) + f(n-2)", "f(0) = 0, f(1) = 1", "fibonacci"),
            ("f(n) = 2 * f(n-1)", "f(0) = 1", "powers of 2"),
            ("f(lst) = f(lst[1:]) + [lst[0]]", "f([]) = []", "reverse list"),
            ("f(n) = 1 + f(n//2)", "f(1) = 0", "log base 2"),
            ("f(a,b) = f(b, a%b)", "f(a, 0) = a", "GCD"),
        ]
        recursive, base, name = self._rng.choice(defs[:min(len(defs), 2 + difficulty)])
        return (
            f"recursive: {recursive}. What is the base case?",
            {"recursive": recursive, "base": base, "name": name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"function: {sd['name']}", f"recursion: {sd['recursive']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["base"]


@register
class CallStackDepthGenerator(StepGenerator):
    """Compute the maximum call stack depth for a recursive call."""

    @property
    def task_name(self) -> str:
        return "call_stack_depth"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        return "find call stack depth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["factorial", "binary_search", "fibonacci"])
        n = self._rng.randint(4, min(20, 4 + 4 * difficulty))
        if fn == "factorial":
            depth = n
            desc = f"factorial({n})"
        elif fn == "binary_search":
            import math
            depth = math.ceil(math.log2(n + 1))
            desc = f"binary_search(array of {n})"
        else:
            depth = n
            desc = f"fibonacci({n}) naive"
        return desc, {"fn": fn, "n": n, "depth": depth}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["fn"] == "factorial":
            return [f"each call reduces n by 1, depth = n = {sd['n']}"]
        elif sd["fn"] == "binary_search":
            return [f"halves search space each call, depth = ceil(log2({sd['n']}+1))"]
        return [f"linear chain of calls, depth = n = {sd['n']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["depth"])


@register
class MemoisationGenerator(StepGenerator):
    """Compare call counts with and without memoisation."""

    @property
    def task_name(self) -> str:
        return "memoisation"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace", "fibonacci"]

    def task_description(self, difficulty: int) -> str:
        return "count calls with memoisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(5, min(15, 5 + 3 * difficulty))
        without_memo = [0]
        def fib_count(k):
            without_memo[0] += 1
            if k <= 1: return k
            return fib_count(k - 1) + fib_count(k - 2)
        fib_count(n)
        naive_calls = without_memo[0]
        memo_calls = n + 1
        return (
            f"fibonacci({n}): calls without vs with memo",
            {"n": n, "naive": naive_calls, "memo": memo_calls},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"without memo: ~O(2^n) calls = {sd['naive']}",
            f"with memo: O(n) calls = {sd['memo']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"naive={sd['naive']}, memo={sd['memo']}"
