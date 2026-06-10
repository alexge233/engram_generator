"""Extended graph algorithm generators.

8 generators across tiers 4-6 covering Bellman-Ford, Floyd-Warshall,
articulation points, strongly connected components, bipartite matching,
network flow, DFS-based topological sort, and greedy graph coloring.
"""
from __future__ import annotations

from collections import deque

from engram_generator.base_domains import GraphGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Bellman-Ford (tier 5)
# ---------------------------------------------------------------------------


@register
class BellmanFordGenerator(GraphGenerator):
    """Relax all edges V-1 times and detect negative cycles on V-th pass.

    Difficulty scaling:
        d1-3: 4 vertices, no negative edges.
        d4-6: 5 vertices, some negative edges.
        d7-8: 5 vertices, possible negative cycle.

    Prerequisites:
        shortest_path.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bellman_ford"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["shortest_path"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "Bellman-Ford shortest paths"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a weighted directed graph and run Bellman-Ford.

        Args:
            difficulty: Controls graph size and negative weights.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4 if difficulty <= 3 else 5
        allow_neg = difficulty >= 4
        neg_cycle = difficulty >= 7 and self._rng.random() < 0.4

        edges: list[tuple[int, int, int]] = []
        for i in range(n):
            for j in range(n):
                if i != j and self._rng.random() < 0.35:
                    lo = -5 if allow_neg else 1
                    w = self._rng.randint(lo, 10)
                    edges.append((i, j, w))

        # Ensure connectivity from source
        source = 0
        for i in range(1, n):
            if not any(e[0] == i - 1 and e[1] == i for e in edges):
                w = self._rng.randint(1, 8)
                edges.append((i - 1, i, w))

        if neg_cycle and n >= 3:
            # Force negative cycle: 1->2->3->1 with negative total
            for e in list(edges):
                if (e[0], e[1]) in [(1, 2), (2, 3 % n), (3 % n, 1)]:
                    edges.remove(e)
            edges.extend([(1, 2, 2), (2, 3 % n, 1), (3 % n, 1, -5)])

        # Run Bellman-Ford
        INF = 10**9
        dist = [INF] * n
        dist[source] = 0
        steps_log = [f"init: dist={[0 if i == source else 'inf' for i in range(n)]}"]

        for iteration in range(n - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            readable = [dist[i] if dist[i] != INF else "inf" for i in range(n)]
            steps_log.append(f"pass {iteration + 1}: dist={readable}")
            if not updated:
                break

        # Check negative cycle
        has_neg_cycle = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                has_neg_cycle = True
                break
        if has_neg_cycle:
            steps_log.append("pass V: negative cycle detected")

        edge_str = ", ".join(f"{u}->{v}(w={w})" for u, v, w in edges)
        readable_dist = [dist[i] if dist[i] != INF else "inf" for i in range(n)]
        return (
            f"Bellman-Ford from {source}: V=0..{n-1}, edges=[{edge_str}]",
            {
                "dist": readable_dist, "has_neg_cycle": has_neg_cycle,
                "steps_log": steps_log, "source": source,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return relaxation pass steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return distances or negative cycle detection.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        if sd["has_neg_cycle"]:
            return "negative cycle detected"
        return f"dist={sd['dist']}"


# ---------------------------------------------------------------------------
# 2. Floyd-Warshall (tier 5)
# ---------------------------------------------------------------------------


@register
class FloydWarshallGenerator(GraphGenerator):
    """All-pairs shortest paths via DP for 4 nodes.

    Shows distance matrix after each intermediate vertex k.

    Difficulty scaling:
        d1-4: 4 nodes, positive weights only.
        d5-8: 4 nodes, some negative weights.

    Prerequisites:
        shortest_path.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "floyd_warshall"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["shortest_path"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "Floyd-Warshall all-pairs shortest paths"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 4-node graph and run Floyd-Warshall.

        Args:
            difficulty: Controls whether negative weights appear.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4
        INF = 999
        allow_neg = difficulty >= 5
        lo = -3 if allow_neg else 1

        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0

        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and self._rng.random() < 0.45:
                    w = self._rng.randint(lo, 8)
                    dist[i][j] = w
                    edges.append((i, j, w))

        # Ensure reachability along chain
        for i in range(n - 1):
            if dist[i][i + 1] == INF:
                w = self._rng.randint(1, 6)
                dist[i][i + 1] = w
                edges.append((i, i + 1, w))

        def fmt_row(row: list[int]) -> str:
            """Format a distance matrix row."""
            return "[" + ", ".join("inf" if x == INF else str(x) for x in row) + "]"

        updates = []
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        old = dist[i][j]
                        dist[i][j] = dist[i][k] + dist[k][j]
                        updates.append(f"k={k}: d[{i}][{j}]={dist[i][j]}")
        steps_log = updates[:6] if len(updates) > 6 else updates
        steps_log.append(f"final: {[fmt_row(r) for r in dist]}")

        final = [[dist[i][j] if dist[i][j] != INF else "inf"
                   for j in range(n)] for i in range(n)]
        edge_str = ", ".join(f"{u}->{v}(w={w})" for u, v, w in edges)
        return (
            f"Floyd-Warshall: V=0..{n-1}, edges=[{edge_str}]",
            {"final": final, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return DP iteration steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final distance matrix.

        Args:
            sd: Solution data.

        Returns:
            Matrix string.
        """
        return str(sd["final"])


# ---------------------------------------------------------------------------
# 3. Articulation points (tier 5)
# ---------------------------------------------------------------------------


@register
class ArticulationPointGenerator(GraphGenerator):
    """Find articulation points using DFS discovery/low values.

    A vertex v is an AP if low[child] >= disc[v].

    Difficulty scaling:
        d1-4: 5 vertices.
        d5-8: 6-7 vertices.

    Prerequisites:
        dfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "articulation_point"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find articulation points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a connected graph and find articulation points.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 5 if difficulty <= 4 else self._rng.randint(6, 7)
        # Ensure connectivity by building a spanning path first
        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges = []
        for i in range(n - 1):
            adj[i].append(i + 1)
            adj[i + 1].append(i)
            edges.append((i, i + 1))
        # Add some random edges
        for i in range(n):
            for j in range(i + 2, n):
                if self._rng.random() < 0.25:
                    adj[i].append(j)
                    adj[j].append(i)
                    edges.append((i, j))

        # Find articulation points via DFS
        disc = [-1] * n
        low = [-1] * n
        parent = [-1] * n
        ap_set: set[int] = set()
        timer = [0]

        def dfs(u: int) -> None:
            """DFS to find articulation points."""
            children = 0
            disc[u] = low[u] = timer[0]
            timer[0] += 1
            for v in sorted(adj[u]):
                if disc[v] == -1:
                    children += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    if parent[u] == -1 and children > 1:
                        ap_set.add(u)
                    if parent[u] != -1 and low[v] >= disc[u]:
                        ap_set.add(u)
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])

        dfs(0)
        ap_list = sorted(ap_set)

        steps_log = []
        for v in range(n):
            if disc[v] != -1:
                steps_log.append(f"v{v}: disc={disc[v]}, low={low[v]}")
        for v in ap_list:
            steps_log.append(f"v{v} is articulation point")

        edge_str = self._format_edges(edges)
        return (
            f"V=0..{n-1}, edges=[{edge_str}]",
            {"ap_list": ap_list, "disc": disc, "low": low,
             "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return DFS discovery/low steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the articulation points.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        if not sd["ap_list"]:
            return "no articulation points"
        return f"AP: {sd['ap_list']}"


# ---------------------------------------------------------------------------
# 4. Strongly connected components (tier 5)
# ---------------------------------------------------------------------------


@register
class StronglyConnectedGenerator(GraphGenerator):
    """Kosaraju's algorithm: DFS finish order, transpose, DFS in reverse order.

    Difficulty scaling:
        d1-4: 4-5 vertices.
        d5-8: 5-6 vertices, denser graph.

    Prerequisites:
        dfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "strongly_connected"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find strongly connected components (Kosaraju)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a directed graph and find SCCs via Kosaraju.

        Args:
            difficulty: Controls graph size and density.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(4, 5)
            prob = 0.35
        else:
            n = self._rng.randint(5, 6)
            prob = 0.4

        # Build directed graph
        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and self._rng.random() < prob:
                    adj[i].append(j)
                    edges.append((i, j))

        # Ensure at least one SCC of size > 1
        if n >= 3 and not any(
            j in adj.get(i, [])
            for i in range(min(3, n)) for j in range(min(3, n)) if i != j
        ):
            adj[0].append(1)
            adj[1].append(0)
            edges.extend([(0, 1), (1, 0)])

        # Pass 1: DFS finish order
        visited: set[int] = set()
        finish_order: list[int] = []

        def dfs1(u: int) -> None:
            """First DFS pass collecting finish order."""
            visited.add(u)
            for v in sorted(adj[u]):
                if v not in visited:
                    dfs1(v)
            finish_order.append(u)

        for v in range(n):
            if v not in visited:
                dfs1(v)

        # Transpose
        adj_t: dict[int, list[int]] = {i: [] for i in range(n)}
        for u in range(n):
            for v in adj[u]:
                adj_t[v].append(u)

        # Pass 2: DFS on transpose in reverse finish order
        visited2: set[int] = set()
        sccs: list[list[int]] = []

        def dfs2(u: int, comp: list[int]) -> None:
            """Second DFS pass on transposed graph."""
            visited2.add(u)
            comp.append(u)
            for v in sorted(adj_t[u]):
                if v not in visited2:
                    dfs2(v, comp)

        for v in reversed(finish_order):
            if v not in visited2:
                comp: list[int] = []
                dfs2(v, comp)
                sccs.append(sorted(comp))

        steps_log = [
            f"DFS finish order: {finish_order}",
            "transpose graph",
        ]
        for i, scc in enumerate(sccs):
            steps_log.append(f"SCC {i}: {scc}")

        edge_str = ", ".join(f"{u}->{v}" for u, v in edges)
        return (
            f"Directed graph V=0..{n-1}, edges=[{edge_str}]",
            {"sccs": sccs, "steps_log": steps_log, "n_sccs": len(sccs)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return Kosaraju algorithm steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the SCCs.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"{sd['n_sccs']} SCCs: {sd['sccs']}"


# ---------------------------------------------------------------------------
# 5. Graph matching -- bipartite (tier 5)
# ---------------------------------------------------------------------------


@register
class GraphMatchingGenerator(GraphGenerator):
    """Maximum bipartite matching via augmenting paths.

    Difficulty scaling:
        d1-4: 3+3 bipartite graph.
        d5-8: 4+4 bipartite graph.

    Prerequisites:
        bfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "graph_matching"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "maximum bipartite matching"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bipartite graph and find maximum matching.

        Args:
            difficulty: Controls partition sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = 3 if difficulty <= 4 else 4
        # Left vertices: 0..k-1, Right vertices: k..2k-1
        edges = []
        adj: dict[int, list[int]] = {i: [] for i in range(2 * k)}
        for u in range(k):
            for v in range(k, 2 * k):
                if self._rng.random() < 0.5:
                    adj[u].append(v)
                    adj[v].append(u)
                    edges.append((u, v))
            # Ensure each left vertex has at least one edge
            if not adj[u]:
                v = self._rng.randint(k, 2 * k - 1)
                adj[u].append(v)
                adj[v].append(u)
                edges.append((u, v))

        # Hungarian / augmenting path matching
        match_r: dict[int, int] = {}  # right -> left

        def try_augment(u: int, visited: set[int]) -> bool:
            """Try to find augmenting path from left vertex u.

            Args:
                u: Left vertex.
                visited: Already visited right vertices.

            Returns:
                True if augmenting path found.
            """
            for v in adj[u]:
                if v < k:
                    continue
                if v in visited:
                    continue
                visited.add(v)
                if v not in match_r or try_augment(match_r[v], visited):
                    match_r[v] = u
                    return True
            return False

        steps_log = []
        for u in range(k):
            found = try_augment(u, set())
            if found:
                matched_edge = [(match_r[v], v) for v in match_r if match_r[v] == u]
                if matched_edge:
                    steps_log.append(f"augment from L{u}: match {matched_edge[0]}")
            else:
                steps_log.append(f"augment from L{u}: no path")

        matching = [(match_r[v], v) for v in sorted(match_r)]
        size = len(matching)

        edge_str = ", ".join(f"L{u}-R{v - k}" for u, v in edges)
        return (
            f"Bipartite L={{0..{k-1}}}, R={{{k}..{2*k-1}}}, edges=[{edge_str}]",
            {"matching": matching, "size": size, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return augmenting path steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return matching size and edges.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        pairs = [(u, v) for u, v in sd["matching"]]
        return f"size={sd['size']}, matching={pairs}"


# ---------------------------------------------------------------------------
# 6. Network flow -- Edmonds-Karp (tier 6)
# ---------------------------------------------------------------------------


@register
class NetworkFlowDetailGenerator(GraphGenerator):
    """Ford-Fulkerson with BFS (Edmonds-Karp) showing augmenting paths.

    Difficulty scaling:
        d1-4: 4 nodes.
        d5-8: 5 nodes.

    Prerequisites:
        bfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "network_flow_detail"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "Edmonds-Karp max flow"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a flow network and compute max flow via Edmonds-Karp.

        Args:
            difficulty: Controls network size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4 if difficulty <= 4 else 5
        source, sink = 0, n - 1
        # Build capacity graph
        cap = [[0] * n for _ in range(n)]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < 0.5:
                    c = self._rng.randint(1, 10)
                    cap[i][j] = c
                    edges.append((i, j, c))
        # Ensure path from source to sink
        for i in range(n - 1):
            if cap[i][i + 1] == 0:
                c = self._rng.randint(1, 8)
                cap[i][i + 1] = c
                edges.append((i, i + 1, c))

        # Edmonds-Karp (BFS-based Ford-Fulkerson)
        residual = [row[:] for row in cap]
        total_flow = 0
        steps_log = []

        while True:
            # BFS to find augmenting path
            parent = [-1] * n
            visited = [False] * n
            visited[source] = True
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v in range(n):
                    if not visited[v] and residual[u][v] > 0:
                        visited[v] = True
                        parent[v] = u
                        if v == sink:
                            break
                        queue.append(v)

            if not visited[sink]:
                break

            # Find bottleneck
            path_flow = float("inf")
            v = sink
            path = []
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, residual[u][v])
                path.append(v)
                v = u
            path.append(source)
            path.reverse()
            path_flow = int(path_flow)

            # Update residual
            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                v = u

            total_flow += path_flow
            steps_log.append(f"path {'->'.join(str(x) for x in path)}, flow={path_flow}")

        steps_log.append(f"no more augmenting paths")

        edge_str = ", ".join(f"{u}->{v}(cap={c})" for u, v, c in edges)
        return (
            f"Flow network V=0..{n-1}, s={source}, t={sink}, edges=[{edge_str}]",
            {"total_flow": total_flow, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return augmenting path steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the maximum flow value.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"max_flow={sd['total_flow']}"


# ---------------------------------------------------------------------------
# 7. Topological sort DFS (tier 5)
# ---------------------------------------------------------------------------


@register
class TopologicalSortDFSGenerator(GraphGenerator):
    """DFS-based topological sort showing discovery and finish times.

    Processes in reverse finish order.

    Difficulty scaling:
        d1-4: 4-5 vertices.
        d5-8: 5-6 vertices.

    Prerequisites:
        dfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "topological_sort_dfs"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "DFS-based topological sort"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DAG and compute topological sort via DFS.

        Args:
            difficulty: Controls number of vertices.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(4, 5)
        else:
            n = self._rng.randint(5, 6)

        # Build a DAG: edges only go from lower to higher vertex index
        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < 0.4:
                    adj[i].append(j)
                    edges.append((i, j))

        # DFS with discovery/finish times
        disc = [-1] * n
        finish = [-1] * n
        timer = [0]
        visited: set[int] = set()
        finish_order: list[int] = []

        def dfs(u: int) -> None:
            """DFS recording discovery and finish times."""
            visited.add(u)
            disc[u] = timer[0]
            timer[0] += 1
            for v in sorted(adj[u]):
                if v not in visited:
                    dfs(v)
            finish[u] = timer[0]
            timer[0] += 1
            finish_order.append(u)

        for v in range(n):
            if v not in visited:
                dfs(v)

        topo_order = list(reversed(finish_order))
        steps_log = []
        for v in range(n):
            steps_log.append(f"v{v}: disc={disc[v]}, finish={finish[v]}")
        steps_log.append(f"reverse finish order: {topo_order}")

        edge_str = ", ".join(f"{u}->{v}" for u, v in edges)
        return (
            f"DAG V=0..{n-1}, edges=[{edge_str}]",
            {"topo_order": topo_order, "disc": disc, "finish": finish,
             "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return DFS timing steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the topological ordering.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return "topo: " + " ".join(str(v) for v in sd["topo_order"])


# ---------------------------------------------------------------------------
# 8. Greedy graph coloring (tier 4)
# ---------------------------------------------------------------------------


@register
class GraphColoringGreedyGenerator(GraphGenerator):
    """Greedy coloring: assign smallest available color to each vertex in order.

    Difficulty scaling:
        d1-3: 4-5 vertices.
        d4-6: 5-6 vertices.
        d7-8: 6-7 vertices.

    Prerequisites:
        connected_components.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "graph_coloring_greedy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["connected_components"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "greedy graph coloring with vertex ordering"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph and apply greedy coloring.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 5)
        elif difficulty <= 6:
            n = self._rng.randint(5, 6)
        else:
            n = self._rng.randint(6, 7)

        adj, edges = self._random_graph(n, 0.45)

        # Greedy coloring
        colors: dict[int, int] = {}
        steps_log = []
        for v in range(n):
            used = {colors[nb] for nb in adj[v] if nb in colors}
            c = 0
            while c in used:
                c += 1
            colors[v] = c
            steps_log.append(f"v{v}: neighbours use {used}, assign color {c}")

        n_colors = max(colors.values()) + 1 if colors else 0
        edge_str = self._format_edges(edges)
        return (
            f"V=0..{n-1}, edges=[{edge_str}]",
            {"colors": colors, "n_colors": n_colors, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return coloring steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return coloring assignment and count.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        assignment = ", ".join(f"v{v}=c{c}" for v, c in sorted(sd["colors"].items()))
        return f"{sd['n_colors']} colors: {assignment}"
