"""Advanced graph theory generators.

8 generators across tiers 5-6 covering graph isomorphism, Eulerian
paths, Hamiltonian cycle detection, graph diameter, vertex cover,
independent set, network flow min-cut, and topological ordering
enumeration.
"""
from __future__ import annotations

from itertools import permutations

from engram_generator.base_domains import GraphGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Graph isomorphism  (tier 6)
# ---------------------------------------------------------------------------


@register
class GraphIsomorphismGenerator(GraphGenerator):
    """Check if two small graphs are isomorphic by degree sequence and adjacency.

    Generates two random graphs on 3-5 nodes, computes their degree
    sequences, and if degree sequences match, tries all vertex
    permutations to find an adjacency-preserving bijection.

    Input format:
        ``check graph isomorphism``

    Target format:
        ``G1: edges=[...], G2: edges=[...] <step>
        deg(G1) = [...], deg(G2) = [...] <step>
        mapping: ... <step> isomorphic / not isomorphic``

    Difficulty scaling:
        d1-3: 3 nodes, low edge probability.
        d4-6: 4 nodes, moderate edge probability.
        d7-8: 5 nodes, higher edge probability.

    Prerequisites:
        connected_components.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "graph_isomorphism"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["connected_components"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "check graph isomorphism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two graphs and check isomorphism.

        Args:
            difficulty: Controls number of nodes and edge density.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            prob = 0.4
        elif difficulty <= 6:
            n = 4
            prob = 0.45
        else:
            n = 5
            prob = 0.5

        adj1, edges1 = self._random_graph(n, prob)
        # Build second graph: sometimes isomorphic, sometimes not
        if self._rng.random() < 0.5:
            # Create isomorphic copy by permuting vertices
            perm = list(range(n))
            self._rng.shuffle(perm)
            adj2 = {i: [] for i in range(n)}
            edges2 = []
            for u, v in edges1:
                pu, pv = perm[u], perm[v]
                a, b = min(pu, pv), max(pu, pv)
                adj2[a].append(b)
                adj2[b].append(a)
                edges2.append((a, b))
            edges2.sort()
        else:
            adj2, edges2 = self._random_graph(n, prob)

        deg1 = sorted(len(adj1[v]) for v in range(n))
        deg2 = sorted(len(adj2[v]) for v in range(n))

        iso = False
        mapping = None
        if deg1 == deg2:
            edge_set2 = set(edges2) | {(v, u) for u, v in edges2}
            for perm in permutations(range(n)):
                match = True
                for u, v in edges1:
                    pu, pv = perm[u], perm[v]
                    if (pu, pv) not in edge_set2 and (pv, pu) not in edge_set2:
                        match = False
                        break
                # Also verify no extra edges
                if match:
                    for u2, v2 in edges2:
                        found = False
                        for u1, v1 in edges1:
                            if perm[u1] == u2 and perm[v1] == v2:
                                found = True
                                break
                            if perm[u1] == v2 and perm[v1] == u2:
                                found = True
                                break
                        if not found:
                            match = False
                            break
                if match:
                    iso = True
                    mapping = {i: perm[i] for i in range(n)}
                    break

        e1_str = self._format_edges(edges1)
        e2_str = self._format_edges(edges2)
        return (
            f"G1: n={n} edges=[{e1_str}], G2: n={n} edges=[{e2_str}]",
            {
                "n": n, "edges1": edges1, "edges2": edges2,
                "deg1": deg1, "deg2": deg2,
                "iso": iso, "mapping": mapping,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate isomorphism checking steps.

        Args:
            sd: Solution data with degree sequences and mapping.

        Returns:
            Steps showing degree comparison and mapping result.
        """
        steps = [
            f"deg(G1) = {sd['deg1']}",
            f"deg(G2) = {sd['deg2']}",
        ]
        if sd["deg1"] != sd["deg2"]:
            steps.append("degree sequences differ")
        elif sd["iso"]:
            m = sd["mapping"]
            steps.append(f"mapping: {m}")
        else:
            steps.append("no valid mapping found")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the isomorphism verdict.

        Args:
            sd: Solution data.

        Returns:
            YES or NO.
        """
        return "YES" if sd["iso"] else "NO"


# ---------------------------------------------------------------------------
# 2. Eulerian path  (tier 5)
# ---------------------------------------------------------------------------


@register
class EulerianPathGenerator(GraphGenerator):
    """Check Euler circuit/path existence and find path by Hierholzer's algorithm.

    Checks vertex degrees: all even means Euler circuit, exactly two
    odd means Euler path, otherwise neither. If one exists, traces
    it using Hierholzer's algorithm.

    Input format:
        ``find Eulerian path or circuit``

    Target format:
        ``edges=[...] <step> degrees: [...] <step>
        odd-degree vertices: ... <step> path: ...``

    Difficulty scaling:
        d1-3: 4 nodes, sparse (likely path/circuit).
        d4-6: 5-6 nodes, moderate density.
        d7-8: 6-7 nodes.

    Prerequisites:
        connected_components.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "eulerian_path"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["connected_components"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "find Eulerian path or circuit"

    def _build_eulerian_graph(self, n: int, circuit: bool) -> tuple[dict, list]:
        """Build a connected graph guaranteed to have an Euler circuit or path.

        Args:
            n: Number of vertices.
            circuit: If True, build circuit; if False, build path.

        Returns:
            Tuple of (adjacency_list, edge_list).
        """
        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges: list[tuple[int, int]] = []

        # Start with a cycle through all vertices for connectivity
        for i in range(n):
            j = (i + 1) % n
            adj[i].append(j)
            adj[j].append(i)
            edges.append((min(i, j), max(i, j)))

        # Add some extra edges (pairs to keep degrees even for circuit)
        extra_pairs = self._rng.randint(0, min(n - 1, 3))
        for _ in range(extra_pairs):
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v:
                a, b = min(u, v), max(u, v)
                # Add two copies to keep degrees even (or remove later)
                adj[a].append(b)
                adj[b].append(a)
                edges.append((a, b))

        if not circuit:
            # Add one extra edge to create exactly 2 odd-degree vertices
            u = self._rng.randint(0, n - 1)
            v = (u + 2) % n
            a, b = min(u, v), max(u, v)
            adj[a].append(b)
            adj[b].append(a)
            edges.append((a, b))

        # Deduplicate edge list for display (but adj has multigraph)
        return adj, edges

    def _hierholzer(self, adj: dict[int, list[int]], start: int) -> list[int]:
        """Trace an Eulerian path/circuit using Hierholzer's algorithm.

        Args:
            adj: Adjacency list (modified in place).
            start: Starting vertex.

        Returns:
            List of vertices in Euler path/circuit order.
        """
        # Work on copies
        local_adj: dict[int, list[int]] = {v: list(nbs) for v, nbs in adj.items()}
        stack = [start]
        path: list[int] = []
        while stack:
            v = stack[-1]
            if local_adj[v]:
                u = local_adj[v].pop()
                local_adj[u].remove(v)
                stack.append(u)
            else:
                path.append(stack.pop())
        return path

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph and check for Euler path/circuit.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = self._rng.choice([5, 6])
        else:
            n = self._rng.choice([6, 7])

        # Decide what to build
        choice = self._rng.choice(["circuit", "path", "neither"])
        if choice == "circuit":
            adj, edges = self._build_eulerian_graph(n, circuit=True)
        elif choice == "path":
            adj, edges = self._build_eulerian_graph(n, circuit=False)
        else:
            adj, edges = self._random_graph(n, 0.5)

        degrees = {v: len(adj[v]) for v in range(n)}
        odd_vertices = [v for v in range(n) if degrees[v] % 2 == 1]
        n_odd = len(odd_vertices)

        # Check connectivity among vertices with edges
        has_edges = [v for v in range(n) if degrees[v] > 0]
        connected = True
        if has_edges:
            visited = set()
            queue = [has_edges[0]]
            visited.add(has_edges[0])
            while queue:
                node = queue.pop(0)
                for nb in adj[node]:
                    if nb not in visited:
                        visited.add(nb)
                        queue.append(nb)
            connected = all(v in visited for v in has_edges)

        if connected and n_odd == 0 and edges:
            euler_type = "circuit"
            path = self._hierholzer(adj, 0)
        elif connected and n_odd == 2 and edges:
            euler_type = "path"
            path = self._hierholzer(adj, odd_vertices[0])
        else:
            euler_type = "none"
            path = []

        edge_str = self._format_edges(edges)
        deg_str = ", ".join(f"{v}:{degrees[v]}" for v in range(n))
        return (
            f"n={n} edges=[{edge_str}]",
            {
                "n": n, "degrees": degrees, "deg_str": deg_str,
                "odd_vertices": odd_vertices, "n_odd": n_odd,
                "euler_type": euler_type, "path": path,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Eulerian path/circuit checking steps.

        Args:
            sd: Solution data with degrees and path.

        Returns:
            Steps showing degree analysis and result.
        """
        steps = [
            f"degrees: {sd['deg_str']}",
            f"odd-degree vertices: {sd['odd_vertices']} (count={sd['n_odd']})",
        ]
        if sd["euler_type"] == "circuit":
            steps.append("all even -> Euler circuit exists")
            path_str = "->".join(str(v) for v in sd["path"][:10])
            steps.append(f"circuit: {path_str}")
        elif sd["euler_type"] == "path":
            steps.append("exactly 2 odd -> Euler path exists")
            path_str = "->".join(str(v) for v in sd["path"][:10])
            steps.append(f"path: {path_str}")
        else:
            steps.append("no Euler path or circuit")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Eulerian path/circuit verdict.

        Args:
            sd: Solution data.

        Returns:
            Type of Euler path found.
        """
        return sd["euler_type"]


# ---------------------------------------------------------------------------
# 3. Hamiltonian check  (tier 6)
# ---------------------------------------------------------------------------


@register
class HamiltonianCheckGenerator(GraphGenerator):
    """Determine if a Hamiltonian cycle exists in a small graph.

    Uses exhaustive search over all permutations starting from vertex 0
    to check if any permutation forms a valid Hamiltonian cycle.

    Input format:
        ``check for Hamiltonian cycle``

    Target format:
        ``vertices=0..n-1 edges=[...] <step>
        try permutation ... <step>
        Hamiltonian cycle: ... / no Hamiltonian cycle``

    Difficulty scaling:
        d1-3: 4 nodes.
        d4-6: 5 nodes.
        d7-8: 6 nodes.

    Prerequisites:
        cycle_detect.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hamiltonian_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cycle_detect"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "check for Hamiltonian cycle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph and check for Hamiltonian cycle.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        adj, edges = self._random_graph(n, 0.5)
        edge_set = set()
        for u, v in edges:
            edge_set.add((u, v))
            edge_set.add((v, u))

        ham_cycle: list[int] | None = None
        others = list(range(1, n))
        for perm in permutations(others):
            path = [0] + list(perm)
            valid = True
            for i in range(len(path)):
                u = path[i]
                v = path[(i + 1) % len(path)]
                if (u, v) not in edge_set:
                    valid = False
                    break
            if valid:
                ham_cycle = path
                break

        edge_str = self._format_edges(edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"n": n, "edges": edges, "ham_cycle": ham_cycle},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Hamiltonian cycle checking steps.

        Args:
            sd: Solution data with cycle or None.

        Returns:
            Steps showing the search result.
        """
        steps = [f"n={sd['n']}, |E|={len(sd['edges'])}"]
        if sd["ham_cycle"] is not None:
            cycle = sd["ham_cycle"]
            cycle_str = "->".join(str(v) for v in cycle) + f"->{cycle[0]}"
            steps.append(f"found cycle: {cycle_str}")
        else:
            steps.append("exhaustive search: no Hamiltonian cycle")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return Hamiltonian cycle verdict.

        Args:
            sd: Solution data.

        Returns:
            The cycle or NO.
        """
        if sd["ham_cycle"] is not None:
            c = sd["ham_cycle"]
            return "->".join(str(v) for v in c) + f"->{c[0]}"
        return "NO"


# ---------------------------------------------------------------------------
# 4. Graph diameter  (tier 5)
# ---------------------------------------------------------------------------


@register
class GraphDiameterGenerator(GraphGenerator):
    """Compute the diameter of a connected graph.

    Runs BFS from each vertex to compute all-pairs shortest paths,
    then takes the maximum distance as the diameter.

    Input format:
        ``compute graph diameter``

    Target format:
        ``vertices=0..n-1 edges=[...] <step>
        BFS from 0: max dist = ... <step>
        ... <step> diameter = ...``

    Difficulty scaling:
        d1-3: 4-5 nodes, high connectivity.
        d4-6: 6-7 nodes.
        d7-8: 8 nodes.

    Prerequisites:
        shortest_path.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "graph_diameter"

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
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "compute graph diameter"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a connected graph and compute its diameter.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([4, 5])
        elif difficulty <= 6:
            n = self._rng.choice([6, 7])
        else:
            n = 8

        # Generate connected graph by ensuring a spanning path
        adj, edges = self._random_graph(n, 0.45)
        # Force connectivity
        for i in range(n - 1):
            has_edge = any(
                (min(i, i + 1), max(i, i + 1)) == (min(u, v), max(u, v))
                for u, v in edges
            )
            if not has_edge:
                adj[i].append(i + 1)
                adj[i + 1].append(i)
                edges.append((i, i + 1))

        max_dists: list[tuple[int, int]] = []
        diameter = 0
        for s in range(n):
            bfs_order = self._bfs(adj, s)
            dist = {s: 0}
            queue = [s]
            seen = {s}
            while queue:
                node = queue.pop(0)
                for nb in sorted(adj[node]):
                    if nb not in seen:
                        seen.add(nb)
                        dist[nb] = dist[node] + 1
                        queue.append(nb)
            farthest = max(dist.values()) if dist else 0
            max_dists.append((s, farthest))
            diameter = max(diameter, farthest)

        edge_str = self._format_edges(edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {"n": n, "max_dists": max_dists, "diameter": diameter},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate diameter computation steps.

        Args:
            sd: Solution data with BFS distances.

        Returns:
            Steps showing BFS from each vertex and max distance.
        """
        steps = []
        for s, d in sd["max_dists"]:
            steps.append(f"BFS from {s}: max dist = {d}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the graph diameter.

        Args:
            sd: Solution data.

        Returns:
            Diameter value as string.
        """
        return f"diameter = {sd['diameter']}"


# ---------------------------------------------------------------------------
# 5. Vertex cover  (tier 6)
# ---------------------------------------------------------------------------


@register
class VertexCoverGenerator(GraphGenerator):
    """Find a minimum vertex cover of a small graph.

    Tries all subsets of vertices in increasing size to find the
    smallest set that covers every edge.

    Input format:
        ``find minimum vertex cover``

    Target format:
        ``vertices=0..n-1 edges=[...] <step>
        try size 1: ... <step>
        try size 2: ... <step>
        min vertex cover: {...}``

    Difficulty scaling:
        d1-3: 4 nodes.
        d4-6: 5 nodes.
        d7-8: 6 nodes.

    Prerequisites:
        graph_coloring.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vertex_cover"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["graph_coloring"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "find minimum vertex cover"

    @staticmethod
    def _subsets_of_size(n: int, k: int) -> list[list[int]]:
        """Generate all subsets of {0..n-1} with exactly k elements.

        Args:
            n: Universe size.
            k: Subset size.

        Returns:
            List of sorted subsets.
        """
        if k == 0:
            return [[]]
        if k > n:
            return []
        result: list[list[int]] = []

        def _backtrack(start: int, current: list[int]) -> None:
            if len(current) == k:
                result.append(list(current))
                return
            for i in range(start, n):
                current.append(i)
                _backtrack(i + 1, current)
                current.pop()

        _backtrack(0, [])
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph and find its minimum vertex cover.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        adj, edges = self._random_graph(n, 0.45)
        if not edges:
            edges = [(0, 1)]
            adj[0].append(1)
            adj[1].append(0)

        min_cover: list[int] | None = None
        search_log: list[str] = []
        for size in range(n + 1):
            subsets = self._subsets_of_size(n, size)
            for subset in subsets:
                s = set(subset)
                covers_all = all(u in s or v in s for u, v in edges)
                if covers_all:
                    min_cover = subset
                    search_log.append(f"size {size}: {subset} covers all")
                    break
            if min_cover is not None:
                break
            search_log.append(f"size {size}: no valid cover")

        edge_str = self._format_edges(edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {
                "n": n, "edges": edges,
                "min_cover": min_cover,
                "cover_size": len(min_cover) if min_cover else 0,
                "search_log": search_log,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate vertex cover search steps.

        Args:
            sd: Solution data with search log and cover.

        Returns:
            Steps showing the search process.
        """
        return sd["search_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the minimum vertex cover.

        Args:
            sd: Solution data.

        Returns:
            String with cover vertices and size.
        """
        return f"cover = {sd['min_cover']} (size {sd['cover_size']})"


# ---------------------------------------------------------------------------
# 6. Independent set  (tier 6)
# ---------------------------------------------------------------------------


@register
class IndependentSetGenerator(GraphGenerator):
    """Find a maximum independent set of a small graph.

    An independent set is a set of vertices with no edges between them.
    Uses the complement relationship: max independent set = V minus
    min vertex cover.

    Input format:
        ``find maximum independent set``

    Target format:
        ``vertices=0..n-1 edges=[...] <step>
        min vertex cover = {...} <step>
        independent set = V \\ cover = {...}``

    Difficulty scaling:
        d1-3: 4 nodes.
        d4-6: 5 nodes.
        d7-8: 6 nodes.

    Prerequisites:
        vertex_cover.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "independent_set"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vertex_cover"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "find maximum independent set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph and find max independent set via vertex cover.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        adj, edges = self._random_graph(n, 0.4)
        if not edges:
            edges = [(0, 1)]
            adj[0].append(1)
            adj[1].append(0)

        # Find min vertex cover by brute force
        min_cover: set[int] = set()
        for size in range(n + 1):
            found = False
            for subset in VertexCoverGenerator._subsets_of_size(n, size):
                s = set(subset)
                if all(u in s or v in s for u, v in edges):
                    min_cover = s
                    found = True
                    break
            if found:
                break

        ind_set = sorted(set(range(n)) - min_cover)
        edge_str = self._format_edges(edges)
        return (
            f"vertices=0..{n-1} edges=[{edge_str}]",
            {
                "n": n, "edges": edges,
                "min_cover": sorted(min_cover),
                "ind_set": ind_set,
                "ind_size": len(ind_set),
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate independent set derivation steps.

        Args:
            sd: Solution data with cover and independent set.

        Returns:
            Steps showing vertex cover and complement.
        """
        return [
            f"min vertex cover = {sd['min_cover']}",
            f"V = {{0..{sd['n']-1}}}",
            f"independent set = V \\ cover = {sd['ind_set']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the maximum independent set.

        Args:
            sd: Solution data.

        Returns:
            String with independent set and size.
        """
        return f"ind set = {sd['ind_set']} (size {sd['ind_size']})"


# ---------------------------------------------------------------------------
# 7. Network flow min-cut  (tier 6)
# ---------------------------------------------------------------------------


@register
class NetworkFlowMincutGenerator(GraphGenerator):
    """Find min-cut from max-flow using the max-flow min-cut theorem.

    Builds a small directed capacity network, computes max flow using
    BFS-based augmenting paths (Edmonds-Karp), then identifies the
    min-cut edges by finding reachable vertices in the residual graph.

    Input format:
        ``find min-cut via max-flow``

    Target format:
        ``s=0 t=n-1 capacities=[...] <step>
        augment path ... flow ... <step>
        max flow = ... <step>
        min-cut edges: ...``

    Difficulty scaling:
        d1-3: 4 nodes.
        d4-6: 5 nodes.
        d7-8: 6 nodes.

    Prerequisites:
        bfs_order.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "network_flow_mincut"

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
            difficulty: Controls network size.

        Returns:
            Natural language description.
        """
        return "find min-cut via max-flow"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a flow network and compute max-flow / min-cut.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        source, sink = 0, n - 1

        # Build directed capacity graph
        cap: dict[tuple[int, int], int] = {}
        cap_edges: list[tuple[int, int, int]] = []
        for u in range(n):
            for v in range(n):
                if u != v and u != sink and v != source:
                    if self._rng.random() < 0.4:
                        c = self._rng.randint(1, 5 + difficulty)
                        cap[(u, v)] = c
                        cap_edges.append((u, v, c))

        # Ensure path from source to sink
        if not any(cap.get((source, v), 0) > 0 for v in range(n)):
            mid = self._rng.randint(1, n - 2) if n > 2 else 1
            c = self._rng.randint(1, 5)
            cap[(source, mid)] = c
            cap_edges.append((source, mid, c))
        if not any(cap.get((v, sink), 0) > 0 for v in range(n)):
            mid = self._rng.randint(1, n - 2) if n > 2 else 1
            c = self._rng.randint(1, 5)
            cap[(mid, sink)] = c
            cap_edges.append((mid, sink, c))

        # Edmonds-Karp max-flow
        residual: dict[tuple[int, int], int] = {}
        for (u, v), c in cap.items():
            residual[(u, v)] = residual.get((u, v), 0) + c
            if (v, u) not in residual:
                residual[(v, u)] = 0

        max_flow = 0
        aug_paths: list[str] = []
        while True:
            # BFS to find augmenting path
            parent: dict[int, int] = {source: -1}
            queue = [source]
            while queue and sink not in parent:
                node = queue.pop(0)
                for v in range(n):
                    if v not in parent and residual.get((node, v), 0) > 0:
                        parent[v] = node
                        queue.append(v)
            if sink not in parent:
                break
            # Find bottleneck
            path_nodes = []
            v = sink
            bottleneck = float("inf")
            while v != source:
                u = parent[v]
                bottleneck = min(bottleneck, residual[(u, v)])
                path_nodes.append(v)
                v = u
            path_nodes.append(source)
            path_nodes.reverse()
            bottleneck = int(bottleneck)
            # Update residual
            for i in range(len(path_nodes) - 1):
                u, v = path_nodes[i], path_nodes[i + 1]
                residual[(u, v)] -= bottleneck
                residual[(v, u)] = residual.get((v, u), 0) + bottleneck
            max_flow += bottleneck
            p_str = "->".join(str(x) for x in path_nodes)
            aug_paths.append(f"path {p_str} flow {bottleneck}")

        # Find min-cut: reachable from source in residual
        reachable = set()
        queue = [source]
        reachable.add(source)
        while queue:
            node = queue.pop(0)
            for v in range(n):
                if v not in reachable and residual.get((node, v), 0) > 0:
                    reachable.add(v)
                    queue.append(v)

        cut_edges = []
        for (u, v), c in cap.items():
            if u in reachable and v not in reachable and c > 0:
                cut_edges.append((u, v, c))

        cap_str = ", ".join(f"{u}->{v}({c})" for u, v, c in cap_edges)
        return (
            f"s={source} t={sink} caps=[{cap_str}]",
            {
                "max_flow": max_flow, "aug_paths": aug_paths,
                "cut_edges": cut_edges, "reachable": sorted(reachable),
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate max-flow / min-cut computation steps.

        Args:
            sd: Solution data with augmenting paths and cut.

        Returns:
            Steps showing flow augmentation and cut identification.
        """
        steps = list(sd["aug_paths"])
        steps.append(f"max flow = {sd['max_flow']}")
        cut_str = ", ".join(f"{u}->{v}({c})" for u, v, c in sd["cut_edges"])
        steps.append(f"min-cut edges: [{cut_str}]")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the max-flow and min-cut.

        Args:
            sd: Solution data.

        Returns:
            String with max flow value.
        """
        return f"max flow = min cut = {sd['max_flow']}"


# ---------------------------------------------------------------------------
# 8. Topological ordering enumeration  (tier 6)
# ---------------------------------------------------------------------------


@register
class TopologicalOrderingGenerator(GraphGenerator):
    """Find all valid topological orderings of a small DAG and count them.

    Generates a random DAG, then uses backtracking with in-degree
    tracking to enumerate all valid topological sorts.

    Input format:
        ``find all topological orderings``

    Target format:
        ``DAG: edges=[...] <step>
        in-degrees: ... <step>
        ordering 1: ... <step>
        ordering 2: ... <step>
        count = ...``

    Difficulty scaling:
        d1-3: 3-4 nodes, sparse.
        d4-6: 4-5 nodes.
        d7-8: 5-6 nodes.

    Prerequisites:
        topo_sort.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "topological_ordering"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["topo_sort"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls DAG size.

        Returns:
            Natural language description.
        """
        return "find all topological orderings"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DAG and enumerate all topological orderings.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([3, 4])
            prob = 0.35
        elif difficulty <= 6:
            n = self._rng.choice([4, 5])
            prob = 0.4
        else:
            n = self._rng.choice([5, 6])
            prob = 0.35

        # Build DAG: only edges from lower to higher index
        edges: list[tuple[int, int]] = []
        children: dict[int, list[int]] = {i: [] for i in range(n)}
        in_degree: dict[int, int] = {i: 0 for i in range(n)}
        for u in range(n):
            for v in range(u + 1, n):
                if self._rng.random() < prob:
                    edges.append((u, v))
                    children[u].append(v)
                    in_degree[v] += 1

        # Enumerate all topological orderings via backtracking
        all_orderings: list[list[int]] = []
        current_in = dict(in_degree)

        def _backtrack(order: list[int]) -> None:
            if len(order) == n:
                all_orderings.append(list(order))
                return
            for v in range(n):
                if v not in order and current_in[v] == 0:
                    order.append(v)
                    for w in children[v]:
                        current_in[w] -= 1
                    _backtrack(order)
                    order.pop()
                    for w in children[v]:
                        current_in[w] += 1

        _backtrack([])

        edge_str = ", ".join(f"{u}->{v}" for u, v in edges)
        in_deg_str = ", ".join(f"{v}:{in_degree[v]}" for v in range(n))
        return (
            f"DAG: n={n} edges=[{edge_str}]",
            {
                "n": n, "edges": edges, "in_degrees": in_deg_str,
                "orderings": all_orderings[:8],  # cap display
                "count": len(all_orderings),
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate topological ordering enumeration steps.

        Args:
            sd: Solution data with orderings.

        Returns:
            Steps showing in-degrees and each ordering.
        """
        steps = [f"in-degrees: {sd['in_degrees']}"]
        for i, order in enumerate(sd["orderings"]):
            steps.append(f"ordering {i+1}: {order}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the count of topological orderings.

        Args:
            sd: Solution data.

        Returns:
            Count of valid orderings.
        """
        return f"count = {sd['count']}"
