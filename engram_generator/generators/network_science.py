"""Network science generators.

6 generators across tiers 5-6 covering degree distribution, clustering
coefficient, betweenness centrality, PageRank, small-world check,
and community detection (modularity).
"""
from __future__ import annotations

import math
from collections import deque

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _all_shortest_paths_count(adj: dict[int, list[int]],
                              n: int) -> dict[tuple[int, int], int]:
    """Count shortest paths between all pairs via BFS.

    Args:
        adj: Adjacency list.
        n: Number of vertices.

    Returns:
        Dict mapping (s, t) to number of shortest paths.
    """
    sigma: dict[tuple[int, int], int] = {}
    for s in range(n):
        dist = [-1] * n
        count = [0] * n
        dist[s] = 0
        count[s] = 1
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    count[v] = count[u]
                    queue.append(v)
                elif dist[v] == dist[u] + 1:
                    count[v] += count[u]
        for t in range(n):
            sigma[(s, t)] = count[t]
    return sigma


def _shortest_path_through(adj: dict[int, list[int]], n: int,
                           v: int) -> dict[tuple[int, int], int]:
    """Count shortest paths between all pairs that pass through v.

    Args:
        adj: Adjacency list.
        n: Number of vertices.
        v: Intermediate vertex.

    Returns:
        Dict mapping (s, t) to count of shortest paths through v.
    """
    # BFS from v to get distances
    dist_v = [-1] * n
    dist_v[v] = 0
    queue = deque([v])
    while queue:
        u = queue.popleft()
        for nb in adj[u]:
            if dist_v[nb] == -1:
                dist_v[nb] = dist_v[u] + 1
                queue.append(nb)

    # For s-t pair, a shortest path goes through v iff
    # dist(s,v) + dist(v,t) == dist(s,t)
    # We need dist from each node
    all_dist: dict[int, list[int]] = {}
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for nb in adj[u]:
                if d[nb] == -1:
                    d[nb] = d[u] + 1
                    q.append(nb)
        all_dist[s] = d

    result: dict[tuple[int, int], int] = {}
    sigma = _all_shortest_paths_count(adj, n)

    for s in range(n):
        for t in range(n):
            if s == v or t == v or s == t:
                result[(s, t)] = 0
                continue
            d_st = all_dist[s][t]
            d_sv = all_dist[s][v]
            d_vt = all_dist[v][t]
            if d_st == -1 or d_sv == -1 or d_vt == -1:
                result[(s, t)] = 0
                continue
            if d_sv + d_vt == d_st:
                # Count paths s->v * v->t
                sigma_sv = sigma.get((s, v), 0)
                sigma_vt = sigma.get((v, t), 0)
                result[(s, t)] = sigma_sv * sigma_vt
            else:
                result[(s, t)] = 0
    return result


# ---------------------------------------------------------------------------
# 1. Degree Distribution (tier 5)
# ---------------------------------------------------------------------------

@register
class DegreeDistributionGenerator(StepGenerator):
    """Compute degree sequence and degree distribution of a small graph.

    Given an adjacency list, compute each vertex's degree, the degree
    distribution P(k) = fraction of nodes with degree k, and the
    average degree.

    Difficulty scaling:
        Difficulty 1-3: 4-5 vertices, sparse.
        Difficulty 4-6: 5-7 vertices, moderate density.
        Difficulty 7-8: 6-8 vertices, higher density.

    Prerequisites:
        connected_components.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "degree_distribution"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute degree distribution and average degree"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a degree distribution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 5)
            prob = 0.3
        elif difficulty <= 6:
            n = self._rng.randint(5, 7)
            prob = 0.4
        else:
            n = self._rng.randint(6, 8)
            prob = 0.5

        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges: list[tuple[int, int]] = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < prob:
                    adj[i].append(j)
                    adj[j].append(i)
                    edges.append((i, j))

        degrees = [len(adj[v]) for v in range(n)]
        avg_deg = round(sum(degrees) / n, 4)

        # Degree distribution P(k)
        max_k = max(degrees) if degrees else 0
        dist: dict[int, float] = {}
        for k in range(max_k + 1):
            count = degrees.count(k)
            if count > 0:
                dist[k] = round(count / n, 4)

        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        problem = f"vertices=0..{n-1}, edges=[{edge_str}]. degree distribution?"
        return problem, {
            "n": n, "degrees": degrees, "avg_deg": avg_deg, "dist": dist,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate degree distribution computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing degree sequence and distribution.
        """
        steps = [
            f"degrees: {sd['degrees']}",
        ]
        for k, pk in sorted(sd["dist"].items()):
            steps.append(f"P({k}) = {pk}")
        steps.append(f"avg degree = {sd['avg_deg']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the average degree and distribution summary.

        Args:
            sd: Solution data dict.

        Returns:
            Average degree and P(k) values.
        """
        dist_str = ", ".join(
            f"P({k})={v}" for k, v in sorted(sd["dist"].items())
        )
        return f"avg={sd['avg_deg']}; {dist_str}"


# ---------------------------------------------------------------------------
# 2. Clustering Coefficient (tier 5)
# ---------------------------------------------------------------------------

@register
class ClusteringCoefficientGenerator(StepGenerator):
    """Compute local and global clustering coefficients.

    Local CC(v) = 2*triangles(v) / (deg(v)*(deg(v)-1)).
    Global CC = average of all local CCs (excluding deg <= 1 nodes).

    Difficulty scaling:
        Difficulty 1-3: 4-5 vertices.
        Difficulty 4-6: 5-6 vertices.
        Difficulty 7-8: 6-8 vertices.

    Prerequisites:
        connected_components.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "clustering_coefficient"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute local and global clustering coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a clustering coefficient problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 5)
        elif difficulty <= 6:
            n = self._rng.randint(5, 6)
        else:
            n = self._rng.randint(6, 8)

        adj: dict[int, set[int]] = {i: set() for i in range(n)}
        edges: list[tuple[int, int]] = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < 0.45:
                    adj[i].add(j)
                    adj[j].add(i)
                    edges.append((i, j))

        local_cc: dict[int, float] = {}
        for v in range(n):
            deg = len(adj[v])
            if deg < 2:
                local_cc[v] = 0.0
                continue
            neighbours = list(adj[v])
            triangles = 0
            for i in range(len(neighbours)):
                for j in range(i + 1, len(neighbours)):
                    if neighbours[j] in adj[neighbours[i]]:
                        triangles += 1
            local_cc[v] = round(
                2.0 * triangles / (deg * (deg - 1)), 4
            )

        eligible = [v for v in range(n) if len(adj[v]) >= 2]
        if eligible:
            global_cc = round(
                sum(local_cc[v] for v in eligible) / len(eligible), 4
            )
        else:
            global_cc = 0.0

        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        problem = f"vertices=0..{n-1}, edges=[{edge_str}]. clustering?"
        return problem, {
            "n": n, "local_cc": local_cc, "global_cc": global_cc,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate clustering coefficient computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing each local CC and the global average.
        """
        steps = []
        for v in range(sd["n"]):
            steps.append(f"CC({v}) = {sd['local_cc'][v]}")
        steps.append(f"global CC = {sd['global_cc']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the global clustering coefficient.

        Args:
            sd: Solution data dict.

        Returns:
            Global CC value.
        """
        return f"global CC = {sd['global_cc']}"


# ---------------------------------------------------------------------------
# 3. Betweenness Centrality (tier 6)
# ---------------------------------------------------------------------------

@register
class BetweennessCentralityGenerator(StepGenerator):
    """Compute betweenness centrality for a small graph.

    BC(v) = sum_{s!=v!=t} sigma_st(v) / sigma_st where sigma_st is
    the number of shortest s-t paths and sigma_st(v) is the number
    of those paths passing through v.

    Difficulty scaling:
        Difficulty 1-4: 4 vertices.
        Difficulty 5-6: 5 vertices.
        Difficulty 7-8: 6 vertices.

    Prerequisites:
        shortest_path.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "betweenness_centrality"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["shortest_path"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute betweenness centrality for each vertex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a betweenness centrality problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        # Build a connected graph
        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges: list[tuple[int, int]] = []
        # Ensure connectivity with a spanning path
        for i in range(n - 1):
            adj[i].append(i + 1)
            adj[i + 1].append(i)
            edges.append((i, i + 1))
        # Add random extra edges
        for i in range(n):
            for j in range(i + 2, n):
                if self._rng.random() < 0.3:
                    if j not in adj[i]:
                        adj[i].append(j)
                        adj[j].append(i)
                        edges.append((i, j))

        sigma = _all_shortest_paths_count(adj, n)

        bc: dict[int, float] = {}
        for v in range(n):
            through = _shortest_path_through(adj, n, v)
            total = 0.0
            for s in range(n):
                for t in range(n):
                    if s == v or t == v or s == t:
                        continue
                    sigma_st = sigma.get((s, t), 0)
                    sigma_st_v = through.get((s, t), 0)
                    if sigma_st > 0:
                        total += sigma_st_v / sigma_st
            bc[v] = round(total, 4)

        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        problem = f"vertices=0..{n-1}, edges=[{edge_str}]. betweenness?"
        return problem, {"n": n, "bc": bc}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate betweenness centrality steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing BC for each vertex.
        """
        return [f"BC({v}) = {sd['bc'][v]}" for v in range(sd["n"])]

    def _create_answer(self, sd: dict) -> str:
        """Return betweenness centrality values.

        Args:
            sd: Solution data dict.

        Returns:
            BC values for all vertices.
        """
        parts = ", ".join(f"BC({v})={sd['bc'][v]}" for v in range(sd["n"]))
        return parts


# ---------------------------------------------------------------------------
# 4. PageRank Compute (tier 5)
# ---------------------------------------------------------------------------

@register
class PageRankComputeGenerator(StepGenerator):
    """Compute one iteration of PageRank.

    PR(v) = (1-d)/N + d * sum_{u->v} PR(u)/deg_out(u).
    Uses damping factor d=0.85.

    Difficulty scaling:
        Difficulty 1-3: 3-4 vertices.
        Difficulty 4-6: 4-5 vertices.
        Difficulty 7-8: 5-6 vertices.

    Prerequisites:
        markov_chain.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pagerank_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["markov_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute one iteration of PageRank (d=0.85)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PageRank computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 4)
        elif difficulty <= 6:
            n = self._rng.randint(4, 5)
        else:
            n = self._rng.randint(5, 6)

        d = 0.85
        # Build directed graph
        out_edges: dict[int, list[int]] = {i: [] for i in range(n)}
        in_edges: dict[int, list[int]] = {i: [] for i in range(n)}
        edges: list[tuple[int, int]] = []

        for i in range(n):
            # Each node has at least one outgoing edge
            targets = set()
            n_out = self._rng.randint(1, min(n - 1, 3))
            candidates = [j for j in range(n) if j != i]
            chosen = self._rng.sample(candidates, min(n_out, len(candidates)))
            for j in chosen:
                if j not in targets:
                    targets.add(j)
                    out_edges[i].append(j)
                    in_edges[j].append(i)
                    edges.append((i, j))

        # Initial PR = 1/N for all
        pr_old = {v: round(1.0 / n, 4) for v in range(n)}

        # One iteration
        pr_new: dict[int, float] = {}
        for v in range(n):
            incoming_sum = 0.0
            for u in in_edges[v]:
                deg_out_u = len(out_edges[u])
                if deg_out_u > 0:
                    incoming_sum += pr_old[u] / deg_out_u
            pr_new[v] = round((1.0 - d) / n + d * incoming_sum, 4)

        edge_str = ", ".join(f"{u}->{v}" for u, v in edges)
        problem = (
            f"directed: vertices=0..{n-1}, edges=[{edge_str}]; "
            f"PR_0=1/{n}; one iteration, d=0.85?"
        )
        return problem, {
            "n": n, "d": d, "pr_old": pr_old, "pr_new": pr_new,
            "in_edges": in_edges, "out_edges": out_edges,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate PageRank iteration steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing each vertex's updated PR.
        """
        steps = []
        n = sd["n"]
        d = sd["d"]
        for v in range(n):
            in_parts = []
            for u in sd["in_edges"][v]:
                deg = len(sd["out_edges"][u])
                in_parts.append(f"{sd['pr_old'][u]}/{deg}")
            if in_parts:
                sum_str = " + ".join(in_parts)
                steps.append(
                    f"PR({v}) = {round((1-d)/n, 4)} + {d}*({sum_str}) "
                    f"= {sd['pr_new'][v]}"
                )
            else:
                steps.append(
                    f"PR({v}) = {round((1-d)/n, 4)} + 0 = {sd['pr_new'][v]}"
                )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return updated PageRank values.

        Args:
            sd: Solution data dict.

        Returns:
            PR values for all vertices.
        """
        parts = ", ".join(
            f"PR({v})={sd['pr_new'][v]}" for v in range(sd["n"])
        )
        return parts


# ---------------------------------------------------------------------------
# 5. Small-World Check (tier 5)
# ---------------------------------------------------------------------------

@register
class SmallWorldCheckGenerator(StepGenerator):
    """Check if a graph satisfies small-world properties.

    A graph is small-world if it has high clustering coefficient
    (> 0.3) AND low average path length (< ln(N)).

    Difficulty scaling:
        Difficulty 1-3: 5-6 vertices.
        Difficulty 4-6: 6-8 vertices.
        Difficulty 7-8: 8-10 vertices.

    Prerequisites:
        clustering_coefficient.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "small_world_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["clustering_coefficient"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check small-world: high clustering AND low avg path length"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a small-world check problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 8)
        else:
            n = self._rng.randint(8, 10)

        # Build graph with moderate density for interesting results
        adj: dict[int, set[int]] = {i: set() for i in range(n)}
        edges: list[tuple[int, int]] = []
        # Ring lattice base
        for i in range(n):
            j = (i + 1) % n
            adj[i].add(j)
            adj[j].add(i)
            if (min(i, j), max(i, j)) not in [(u, v) for u, v in edges]:
                edges.append((min(i, j), max(i, j)))
        # Add some shortcuts
        for i in range(n):
            for j in range(i + 2, n):
                if self._rng.random() < 0.2:
                    if j not in adj[i]:
                        adj[i].add(j)
                        adj[j].add(i)
                        edges.append((i, j))

        # Clustering coefficient
        cc_values = []
        for v in range(n):
            deg = len(adj[v])
            if deg < 2:
                continue
            neighbours = list(adj[v])
            triangles = 0
            for a in range(len(neighbours)):
                for b in range(a + 1, len(neighbours)):
                    if neighbours[b] in adj[neighbours[a]]:
                        triangles += 1
            cc_values.append(2.0 * triangles / (deg * (deg - 1)))
        avg_cc = round(sum(cc_values) / len(cc_values), 4) if cc_values else 0.0

        # Average path length (BFS from each node)
        total_dist = 0
        pair_count = 0
        for s in range(n):
            dist = [-1] * n
            dist[s] = 0
            queue = deque([s])
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        queue.append(v)
            for t in range(s + 1, n):
                if dist[t] > 0:
                    total_dist += dist[t]
                    pair_count += 1

        avg_path = round(total_dist / pair_count, 4) if pair_count > 0 else 0.0
        threshold = round(math.log(n), 4)
        high_cc = avg_cc > 0.3
        low_path = avg_path < threshold
        is_small_world = high_cc and low_path

        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        problem = f"vertices=0..{n-1}, edges=[{edge_str}]. small-world?"
        return problem, {
            "n": n, "avg_cc": avg_cc, "avg_path": avg_path,
            "threshold": threshold, "high_cc": high_cc,
            "low_path": low_path, "is_small_world": is_small_world,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate small-world check steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing CC, path length, and criteria evaluation.
        """
        return [
            f"avg clustering = {sd['avg_cc']} (> 0.3? {sd['high_cc']})",
            f"avg path length = {sd['avg_path']}",
            f"ln({sd['n']}) = {sd['threshold']}",
            f"low path? {sd['avg_path']} < {sd['threshold']} = {sd['low_path']}",
            f"small-world: {'YES' if sd['is_small_world'] else 'NO'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the graph is small-world.

        Args:
            sd: Solution data dict.

        Returns:
            YES or NO with supporting values.
        """
        sw = "YES" if sd["is_small_world"] else "NO"
        return f"{sw} (CC={sd['avg_cc']}, L={sd['avg_path']})"


# ---------------------------------------------------------------------------
# 6. Community Detection / Modularity (tier 6)
# ---------------------------------------------------------------------------

@register
class CommunityDetectGenerator(StepGenerator):
    """Compute modularity Q for a given graph partition.

    Q = (1/2m) * sum_{i,j} [A_ij - k_i*k_j/(2m)] * delta(c_i, c_j)
    where m = number of edges, k_i = degree of i, c_i = community of i.

    Difficulty scaling:
        Difficulty 1-3: 4-5 vertices, 2 communities.
        Difficulty 4-6: 5-7 vertices, 2 communities.
        Difficulty 7-8: 6-8 vertices, 3 communities.

    Prerequisites:
        pagerank_compute.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "community_detect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["pagerank_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute modularity Q for given partition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modularity computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 5)
            n_comm = 2
        elif difficulty <= 6:
            n = self._rng.randint(5, 7)
            n_comm = 2
        else:
            n = self._rng.randint(6, 8)
            n_comm = 3

        # Assign communities
        communities = [self._rng.randint(0, n_comm - 1) for _ in range(n)]
        # Ensure all communities used
        for c in range(n_comm):
            if c not in communities:
                communities[self._rng.randint(0, n - 1)] = c

        # Build adjacency matrix (higher intra-community edge probability)
        adj_matrix = [[0] * n for _ in range(n)]
        edges: list[tuple[int, int]] = []
        for i in range(n):
            for j in range(i + 1, n):
                if communities[i] == communities[j]:
                    p = 0.6
                else:
                    p = 0.2
                if self._rng.random() < p:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
                    edges.append((i, j))

        m = len(edges)
        if m == 0:
            # Force at least one edge
            i, j = 0, 1
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
            edges.append((i, j))
            m = 1

        degrees = [sum(adj_matrix[i]) for i in range(n)]

        # Compute modularity
        q_sum = 0.0
        for i in range(n):
            for j in range(n):
                if communities[i] == communities[j]:
                    q_sum += adj_matrix[i][j] - degrees[i] * degrees[j] / (2.0 * m)
        modularity = round(q_sum / (2.0 * m), 4)

        edge_str = ", ".join(f"{u}-{v}" for u, v in edges)
        comm_str = ", ".join(f"{i}:c{communities[i]}" for i in range(n))
        problem = (
            f"vertices=0..{n-1}, edges=[{edge_str}]; "
            f"partition: {{{comm_str}}}. Q?"
        )
        return problem, {
            "n": n, "m": m, "communities": communities,
            "degrees": degrees, "modularity": modularity,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate modularity computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the modularity calculation.
        """
        return [
            f"m = {sd['m']} edges",
            f"degrees: {sd['degrees']}",
            f"communities: {sd['communities']}",
            f"Q = (1/{2*sd['m']}) * sum [A_ij - k_i*k_j/{2*sd['m']}] * delta",
            f"Q = {sd['modularity']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the modularity value.

        Args:
            sd: Solution data dict.

        Returns:
            Modularity Q as string.
        """
        return f"Q = {sd['modularity']}"
