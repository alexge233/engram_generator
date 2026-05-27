"""Graph algorithm generators.

6 generators across tiers 3-4.
"""
from engram_generator.curriculum.registry import register
from engram_generator.base_domains import GraphGenerator



@register
class BFSOrderGenerator(GraphGenerator):
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
        adj, edges = self._random_graph(n, 0.4)
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
class DFSOrderGenerator(GraphGenerator):
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
        adj, edges = self._random_graph(n, 0.4)
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
class ConnectedComponentsGenerator(GraphGenerator):
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
        adj, edges = self._random_graph(n, 0.25)
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
class MinimumSpanningTreeGenerator(GraphGenerator):
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
class GraphColoringGenerator(GraphGenerator):
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
        adj, edges = self._random_graph(n, 0.45)
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
class BipartiteCheckGenerator(GraphGenerator):
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
        adj, edges = self._random_graph(n, 0.35)
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
