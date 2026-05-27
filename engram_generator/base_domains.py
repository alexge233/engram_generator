"""Domain-specific base classes for generator families.

Each base class encapsulates a common generation pattern so that
concrete generators only need to supply their data, not repeat
the generation machinery.
"""
from abc import abstractmethod

from engram_generator.base import StepGenerator


class FormulaGenerator(StepGenerator):
    """Base for generators that evaluate a formula with random inputs.

    Subclasses define the formula, input ranges, and computation.
    The base class handles difficulty scaling and answer formatting.
    """

    @abstractmethod
    def _input_range(self, difficulty: int) -> tuple[int, int]:
        """Return (low, high) range for random inputs at this difficulty.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Tuple of (min_value, max_value).
        """
        ...

    @abstractmethod
    def _compute(self, **inputs) -> dict:
        """Compute the answer from named inputs.

        Args:
            **inputs: Named numeric inputs.

        Returns:
            Solution dict with at least 'result' key.
        """
        ...

    @abstractmethod
    def _format_problem(self, **inputs) -> str:
        """Format the problem string from inputs.

        Args:
            **inputs: Named numeric inputs.

        Returns:
            Problem string.
        """
        ...

    @abstractmethod
    def _format_steps(self, sd: dict) -> list[str]:
        """Format solution steps from the solution dict.

        Args:
            sd: Solution data from _compute.

        Returns:
            List of step strings.
        """
        ...

    def _round(self, value: float, places: int = 4) -> str:
        """Format a numeric answer, dropping trailing zeros.

        Args:
            value: The computed result.
            places: Decimal places to round to.

        Returns:
            Formatted string.
        """
        r = round(value, places)
        if r == int(r):
            return str(int(r))
        return f"{r}"


class ScenarioGenerator(StepGenerator):
    """Base for generators that pick from a pool of curated scenarios.

    Subclasses define the scenario pool. The base class handles
    difficulty-gated selection, step formatting, and answer extraction.
    """

    @abstractmethod
    def _scenarios(self, difficulty: int) -> list[dict]:
        """Return the scenario pool for the given difficulty.

        Each scenario dict must have at least 'problem', 'steps',
        and 'answer' keys.

        Args:
            difficulty: Current difficulty level.

        Returns:
            List of scenario dicts.
        """
        ...

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Select a scenario from the pool.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Tuple of (problem_text, scenario_dict).
        """
        pool = self._scenarios(difficulty)
        scenario = self._rng.choice(pool)
        return scenario["problem"], scenario

    def _create_steps(self, sd: dict) -> list[str]:
        """Extract steps from the scenario dict.

        Args:
            sd: The selected scenario.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the answer from the scenario dict.

        Args:
            sd: The selected scenario.

        Returns:
            Answer string.
        """
        return sd["answer"]


class GraphGenerator(StepGenerator):
    """Base for generators that operate on random graphs.

    Provides utility methods for graph construction that subclasses
    can use without reimplementing adjacency list generation.
    """

    def _random_graph(self, n: int, edge_prob: float = 0.4) -> tuple[dict, list]:
        """Generate a random undirected graph.

        Args:
            n: Number of vertices (labelled 0..n-1).
            edge_prob: Probability of each edge existing.

        Returns:
            Tuple of (adjacency_list_dict, edge_list).
        """
        adj = {i: [] for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._rng.random() < edge_prob:
                    adj[i].append(j)
                    adj[j].append(i)
                    edges.append((i, j))
        return adj, edges

    def _format_edges(self, edges: list[tuple]) -> str:
        """Format edge list as a string.

        Args:
            edges: List of (u, v) tuples.

        Returns:
            Comma-separated edge string.
        """
        return ", ".join(f"{u}-{v}" for u, v in edges)

    def _bfs(self, adj: dict, source: int) -> list[int]:
        """Run BFS from source, return visit order.

        Args:
            adj: Adjacency list.
            source: Starting vertex.

        Returns:
            List of vertices in BFS order.
        """
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
        return visited

    def _dfs(self, adj: dict, source: int) -> list[int]:
        """Run DFS from source, return visit order.

        Args:
            adj: Adjacency list.
            source: Starting vertex.

        Returns:
            List of vertices in DFS order.
        """
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
        return visited

    def _components(self, adj: dict, n: int) -> list[list[int]]:
        """Find all connected components.

        Args:
            adj: Adjacency list.
            n: Number of vertices.

        Returns:
            List of components, each a sorted list of vertices.
        """
        seen = set()
        components = []
        for v in range(n):
            if v not in seen:
                comp = self._bfs(adj, v)
                seen.update(comp)
                components.append(sorted(comp))
        return components
