"""Extended discrete mathematics generators.

10 generators across tiers 5-6 covering generating functions,
Ramsey numbers, Burnside counting, Hall's marriage theorem,
matroid verification, chromatic polynomials, flow networks,
planarity checking, lattice operations, and partition functions.
"""
import math
from itertools import combinations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _format_set(elements) -> str:
    """Format a collection as a set string.

    Args:
        elements: Iterable of elements to format.

    Returns:
        String like ``{1, 2, 3}``.
    """
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


def _binom(n: int, k: int) -> int:
    """Compute binomial coefficient C(n, k).

    Args:
        n: Total items.
        k: Items to choose.

    Returns:
        C(n, k) as an integer.
    """
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


# ═══════════════════════════════════════════════════════════════════
# 1. GENERATING FUNCTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class GeneratingFunctionGenerator(StepGenerator):
    """Find OGF for a sequence and extract a coefficient.

    Given a sequence type (geometric, linear, binomial), derives the
    ordinary generating function and extracts the coefficient [x^k].

    Difficulty scaling:
        Difficulty 1-3: geometric a_n = c^n.
        Difficulty 4-6: linear a_n = n.
        Difficulty 7-8: binomial a_n = C(m, n).

    Prerequisites:
        series_convergence (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "generating_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls sequence type complexity.

        Returns:
            Task description string.
        """
        return "find OGF and extract coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a generating function problem.

        Args:
            difficulty: Controls sequence type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            c = self._rng.randint(2, 5)
            k = self._rng.randint(1, 4)
            coeff = c ** k
            ogf = f"1/(1 - {c}x)"
            seq_desc = f"a_n = {c}^n"
            steps_detail = [
                f"OGF of a_n = {c}^n is sum({c}x)^n = {ogf}",
                f"[x^{k}] = {c}^{k} = {coeff}",
            ]
        elif difficulty <= 6:
            k = self._rng.randint(2, 6)
            coeff = k
            ogf = "x/(1 - x)^2"
            seq_desc = "a_n = n"
            steps_detail = [
                f"OGF of a_n = n is {ogf}",
                f"[x^{k}] = {k}",
            ]
        else:
            m = self._rng.randint(4, 8)
            k = self._rng.randint(1, m)
            coeff = _binom(m, k)
            ogf = f"(1 + x)^{m}"
            seq_desc = f"a_n = C({m}, n)"
            steps_detail = [
                f"OGF of a_n = C({m},n) is {ogf}",
                f"[x^{k}] = C({m},{k}) = {coeff}",
            ]
        problem = f"Find [x^{k}] of OGF for {seq_desc}"
        return problem, {
            "ogf": ogf,
            "k": k,
            "coeff": coeff,
            "steps_detail": steps_detail,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            The coefficient as a string.
        """
        return str(sd["coeff"])


# ═══════════════════════════════════════════════════════════════════
# 2. RAMSEY NUMBER (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class RamseyNumberGenerator(StepGenerator):
    """Compute R(s, t) for small cases.

    Uses known Ramsey numbers: R(2, n) = n, R(3, 3) = 6, R(3, 4) = 9,
    R(3, 5) = 14, R(4, 4) = 18. Verifies by stating the combinatorial
    argument or impossibility.

    Difficulty scaling:
        Difficulty 1-3: R(2, n) for n in [2..6].
        Difficulty 4-6: R(3, 3) or R(3, 4).
        Difficulty 7-8: R(3, 5) or R(4, 4).

    Prerequisites:
        pigeonhole (tier 2).
    """

    # Known exact Ramsey numbers
    _KNOWN = {
        (2, 2): 2, (2, 3): 3, (2, 4): 4, (2, 5): 5, (2, 6): 6,
        (3, 3): 6, (3, 4): 9, (3, 5): 14, (4, 4): 18,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ramsey_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["pigeonhole"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls which Ramsey pair.

        Returns:
            Task description string.
        """
        return "compute Ramsey number R(s,t)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Ramsey number problem.

        Args:
            difficulty: Controls pair complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            t = self._rng.randint(2, 6)
            s, t = 2, t
        elif difficulty <= 6:
            s, t = self._rng.choice([(3, 3), (3, 4)])
        else:
            s, t = self._rng.choice([(3, 5), (4, 4)])
        val = self._KNOWN[(s, t)]

        if s == 2:
            reason = f"any 2-coloring of K_{t} has a monochromatic edge"
        else:
            reason = (
                f"K_{val} guarantees monochromatic K_{s} or K_{t} "
                f"by pigeonhole on vertex neighborhoods"
            )
        problem = f"R({s},{t}) = ?"
        return problem, {"s": s, "t": t, "val": val, "reason": reason}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        return [
            f"R({sd['s']},{sd['t']}): {sd['reason']}",
            f"R({sd['s']},{sd['t']}) = {sd['val']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            The Ramsey number as a string.
        """
        return str(sd["val"])


# ═══════════════════════════════════════════════════════════════════
# 3. BURNSIDE COUNTING (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class BurnsideCountingGenerator(StepGenerator):
    """Count distinct colorings under group action via Burnside's lemma.

    Computes |X/G| = (1/|G|) * sum |Fix(g)| for necklace colorings
    under rotation.

    Difficulty scaling:
        Difficulty 1-3: n=3 beads, 2 colors.
        Difficulty 4-6: n=4 beads, 2-3 colors.
        Difficulty 7-8: n=5-6 beads, 2-3 colors.

    Prerequisites:
        group_order (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "burnside_counting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls bead/color count.

        Returns:
            Task description string.
        """
        return "count distinct necklace colorings via Burnside"

    def _gcd(self, a: int, b: int) -> int:
        """Compute greatest common divisor.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            GCD of a and b.
        """
        while b:
            a, b = b, a % b
        return a

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Burnside counting problem.

        Args:
            difficulty: Controls necklace size and color count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n, c = 3, 2
        elif difficulty <= 6:
            n = 4
            c = self._rng.choice([2, 3])
        else:
            n = self._rng.choice([5, 6])
            c = self._rng.choice([2, 3])

        # Burnside: for rotation group Z_n, Fix(rot by k) = c^gcd(n,k)
        fix_sum = 0
        fix_details = []
        for k in range(n):
            g = self._gcd(n, k)
            fixed = c ** g
            fix_sum += fixed
            fix_details.append(f"rot {k}: gcd({n},{k})={g}, fix={fixed}")
        distinct = fix_sum // n

        problem = f"Necklace: {n} beads, {c} colors, rotations only"
        return problem, {
            "n": n, "c": c,
            "fix_details": fix_details,
            "fix_sum": fix_sum,
            "distinct": distinct,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        steps = sd["fix_details"][:3]  # Keep compact
        steps.append(
            f"sum = {sd['fix_sum']}, |G| = {sd['n']}, "
            f"distinct = {sd['fix_sum']}/{sd['n']} = {sd['distinct']}"
        )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            Number of distinct colorings as a string.
        """
        return str(sd["distinct"])


# ═══════════════════════════════════════════════════════════════════
# 4. HALL MARRIAGE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class HallMarriageGenerator(StepGenerator):
    """Verify Hall's marriage condition on a bipartite graph.

    For all subsets S of left vertices, checks |N(S)| >= |S|. Reports
    whether the condition holds and identifies a violating subset if not.

    Difficulty scaling:
        Difficulty 1-3: 3 left vertices, condition satisfied.
        Difficulty 4-6: 4 left vertices, may or may not satisfy.
        Difficulty 7-8: 5 left vertices, condition often violated.

    Prerequisites:
        bipartite_check (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hall_marriage"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bipartite_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Task description string.
        """
        return "verify Hall's marriage condition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hall's condition verification problem.

        Args:
            difficulty: Controls number of left vertices.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_left = 3
        elif difficulty <= 6:
            n_left = 4
        else:
            n_left = 5
        n_right = n_left + self._rng.randint(0, 1)

        # Build adjacency: each left vertex maps to subset of right vertices
        adj = {}
        for i in range(n_left):
            num_neighbors = self._rng.randint(1, n_right)
            adj[i] = sorted(self._rng.sample(range(n_right), num_neighbors))

        # Check Hall's condition for all subsets of left
        satisfied = True
        violating = None
        for size in range(1, n_left + 1):
            for subset in combinations(range(n_left), size):
                neighbors = set()
                for v in subset:
                    neighbors.update(adj[v])
                if len(neighbors) < len(subset):
                    satisfied = False
                    violating = list(subset)
                    break
            if not satisfied:
                break

        adj_str = ", ".join(f"{k}->{adj[k]}" for k in sorted(adj))
        problem = f"L={{0..{n_left-1}}}, R={{0..{n_right-1}}}, adj: {adj_str}"
        return problem, {
            "n_left": n_left, "n_right": n_right,
            "adj": adj, "satisfied": satisfied,
            "violating": violating,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        if sd["satisfied"]:
            return [
                f"check all 2^{sd['n_left']}-1 subsets of L",
                "for all S: |N(S)| >= |S|",
                "Hall's condition satisfied",
            ]
        viol = sd["violating"]
        neighbors = set()
        for v in viol:
            neighbors.update(sd["adj"][v])
        return [
            f"S = {_format_set(viol)}: |N(S)| = {len(neighbors)} < |S| = {len(viol)}",
            "Hall's condition violated",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            'yes' if Hall's condition holds, 'no' otherwise.
        """
        return "yes" if sd["satisfied"] else "no"


# ═══════════════════════════════════════════════════════════════════
# 5. MATROID CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class MatroidCheckGenerator(StepGenerator):
    """Verify matroid axioms on a collection of independent sets.

    Checks three axioms: (I1) empty set in I, (I2) hereditary property,
    (I3) augmentation property. Reports which axioms hold.

    Difficulty scaling:
        Difficulty 1-3: ground set size 3, valid matroid.
        Difficulty 4-6: ground set size 4, may violate one axiom.
        Difficulty 7-8: ground set size 5, often invalid.

    Prerequisites:
        set_operations (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matroid_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls ground set size.

        Returns:
            Task description string.
        """
        return "verify matroid axioms on independent sets"

    def _build_uniform_matroid(self, n: int, r: int) -> list[frozenset]:
        """Build independent sets of uniform matroid U(r, n).

        Args:
            n: Ground set size.
            r: Rank.

        Returns:
            List of independent sets as frozensets.
        """
        ind_sets = [frozenset()]
        ground = list(range(n))
        for size in range(1, r + 1):
            for combo in combinations(ground, size):
                ind_sets.append(frozenset(combo))
        return ind_sets

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matroid axiom verification problem.

        Args:
            difficulty: Controls ground set size and validity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            r = self._rng.randint(1, 2)
            ind_sets = self._build_uniform_matroid(n, r)
            valid = True
        elif difficulty <= 6:
            n = 4
            r = self._rng.randint(1, 3)
            ind_sets = self._build_uniform_matroid(n, r)
            # Sometimes break hereditary by removing a subset
            if self._rng.random() < 0.4 and len(ind_sets) > 3:
                # Remove a random singleton to break hereditary
                singletons = [s for s in ind_sets if len(s) == 1]
                if singletons:
                    ind_sets.remove(self._rng.choice(singletons))
                    valid = False
                else:
                    valid = True
            else:
                valid = True
        else:
            n = 5
            r = self._rng.randint(1, 3)
            ind_sets = self._build_uniform_matroid(n, r)
            # Break augmentation by removing a maximal set
            maximal = [s for s in ind_sets if len(s) == r]
            if maximal and self._rng.random() < 0.5:
                ind_sets.remove(self._rng.choice(maximal))
                valid = False
            else:
                valid = True

        # Check axioms
        has_empty = frozenset() in ind_sets
        hereditary = True
        for s in ind_sets:
            for elem in s:
                subset = s - {elem}
                if subset not in ind_sets:
                    hereditary = False
                    break
            if not hereditary:
                break

        augmentation = True
        for a in ind_sets:
            for b in ind_sets:
                if len(a) < len(b):
                    found = False
                    for e in b - a:
                        if (a | {e}) in ind_sets:
                            found = True
                            break
                    if not found:
                        augmentation = False
                        break
            if not augmentation:
                break

        valid = has_empty and hereditary and augmentation

        ind_str = "; ".join(
            _format_set(s) if s else "{}" for s in sorted(ind_sets, key=lambda x: (len(x), sorted(x)))
        )
        problem = f"E={{0..{n-1}}}, I={{{ind_str}}}"
        return problem, {
            "n": n, "has_empty": has_empty,
            "hereditary": hereditary, "augmentation": augmentation,
            "valid": valid,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        return [
            f"I1 (empty set): {'pass' if sd['has_empty'] else 'FAIL'}",
            f"I2 (hereditary): {'pass' if sd['hereditary'] else 'FAIL'}",
            f"I3 (augmentation): {'pass' if sd['augmentation'] else 'FAIL'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            'yes' if valid matroid, 'no' otherwise.
        """
        return "yes" if sd["valid"] else "no"


# ═══════════════════════════════════════════════════════════════════
# 6. CHROMATIC POLYNOMIAL (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ChromaticPolynomialGenerator(StepGenerator):
    """Compute chromatic polynomial P(G, k) for small graphs.

    Handles path graphs P_n, cycle graphs C_n, and complete graphs K_n.
    Evaluates P(G, k) for a specific k value.

    Difficulty scaling:
        Difficulty 1-3: path P_n (n=3..4).
        Difficulty 4-6: cycle C_n (n=3..5).
        Difficulty 7-8: complete K_n (n=3..4).

    Prerequisites:
        graph_coloring (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chromatic_polynomial"

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
            difficulty: Controls graph type.

        Returns:
            Task description string.
        """
        return "compute chromatic polynomial P(G,k)"

    def _path_chromatic(self, n: int, k: int) -> int:
        """Compute P(P_n, k) = k * (k-1)^(n-1).

        Args:
            n: Number of vertices in the path.
            k: Number of colors.

        Returns:
            Number of proper colorings.
        """
        return k * (k - 1) ** (n - 1)

    def _cycle_chromatic(self, n: int, k: int) -> int:
        """Compute P(C_n, k) = (k-1)^n + (-1)^n * (k-1).

        Args:
            n: Number of vertices in the cycle.
            k: Number of colors.

        Returns:
            Number of proper colorings.
        """
        return (k - 1) ** n + ((-1) ** n) * (k - 1)

    def _complete_chromatic(self, n: int, k: int) -> int:
        """Compute P(K_n, k) = k * (k-1) * ... * (k-n+1).

        Args:
            n: Number of vertices.
            k: Number of colors.

        Returns:
            Number of proper colorings.
        """
        result = 1
        for i in range(n):
            result *= (k - i)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chromatic polynomial problem.

        Args:
            difficulty: Controls graph type and size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = self._rng.randint(3, 5)

        if difficulty <= 3:
            n = self._rng.randint(3, 4)
            graph_type = "path"
            val = self._path_chromatic(n, k)
            formula = f"k(k-1)^{n-1} = {k}*{k-1}^{n-1}"
        elif difficulty <= 6:
            n = self._rng.randint(3, 5)
            graph_type = "cycle"
            val = self._cycle_chromatic(n, k)
            sign = "+" if n % 2 == 0 else "-"
            formula = f"(k-1)^{n} {sign} (k-1) = {(k-1)**n} {sign} {k-1}"
        else:
            n = self._rng.randint(3, 4)
            graph_type = "complete"
            val = self._complete_chromatic(n, k)
            factors = " * ".join(f"({k}-{i})" for i in range(n))
            formula = factors

        problem = f"P({graph_type.upper()[0]}_{n}, {k}) = ?"
        return problem, {
            "graph_type": graph_type, "n": n, "k": k,
            "val": val, "formula": formula,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        return [
            f"graph: {sd['graph_type']} on {sd['n']} vertices",
            f"P(G,{sd['k']}) = {sd['formula']} = {sd['val']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            The chromatic polynomial value as a string.
        """
        return str(sd["val"])


# ═══════════════════════════════════════════════════════════════════
# 7. FLOW NETWORK (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class FlowNetworkGenerator(StepGenerator):
    """Compute max flow via augmenting paths on a small network.

    Builds a directed network with 3-5 nodes and computes the maximum
    flow from source to sink using augmenting path method (Ford-Fulkerson).

    Difficulty scaling:
        Difficulty 1-3: 3 nodes.
        Difficulty 4-6: 4 nodes.
        Difficulty 7-8: 5 nodes.

    Prerequisites:
        bfs_order (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "flow_network"

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
            difficulty: Controls network size.

        Returns:
            Task description string.
        """
        return "compute max flow in network"

    def _find_path_bfs(self, capacity: dict, source: int,
                       sink: int, n: int) -> list[int] | None:
        """Find an augmenting path via BFS.

        Args:
            capacity: Dict mapping (u, v) to residual capacity.
            source: Source node.
            sink: Sink node.
            n: Number of nodes.

        Returns:
            List of nodes in the path, or None if no path exists.
        """
        visited = {source}
        queue = [(source, [source])]
        while queue:
            node, path = queue.pop(0)
            for v in range(n):
                if v not in visited and capacity.get((node, v), 0) > 0:
                    if v == sink:
                        return path + [v]
                    visited.add(v)
                    queue.append((v, path + [v]))
        return None

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a max flow problem.

        Args:
            difficulty: Controls network size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
        elif difficulty <= 6:
            n = 4
        else:
            n = 5

        source, sink = 0, n - 1

        # Build random capacities ensuring path from source to sink
        capacity = {}
        edges = []
        # Ensure at least one path
        for i in range(n - 1):
            cap = self._rng.randint(1, 5 + difficulty)
            capacity[(i, i + 1)] = cap
            edges.append((i, i + 1, cap))
        # Add some extra edges
        for _ in range(n - 1):
            u = self._rng.randint(0, n - 2)
            v = self._rng.randint(u + 1, n - 1)
            if (u, v) not in capacity:
                cap = self._rng.randint(1, 5 + difficulty)
                capacity[(u, v)] = cap
                edges.append((u, v, cap))

        # Ford-Fulkerson
        residual = dict(capacity)
        max_flow = 0
        aug_paths = []
        while True:
            path = self._find_path_bfs(residual, source, sink, n)
            if path is None:
                break
            # Find bottleneck
            bottleneck = min(
                residual[(path[i], path[i + 1])]
                for i in range(len(path) - 1)
            )
            max_flow += bottleneck
            aug_paths.append((path, bottleneck))
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                residual[(u, v)] -= bottleneck
                residual[(v, u)] = residual.get((v, u), 0) + bottleneck

        edge_str = ", ".join(f"{u}->{v}:{c}" for u, v, c in edges)
        problem = f"network: nodes=0..{n-1}, edges=[{edge_str}], s=0, t={sink}"
        return problem, {
            "max_flow": max_flow,
            "aug_paths": aug_paths,
            "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        steps = []
        for path, bn in sd["aug_paths"][:3]:  # Cap steps for length
            path_str = "->".join(str(v) for v in path)
            steps.append(f"path {path_str}, bottleneck={bn}")
        steps.append(f"max flow = {sd['max_flow']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            The max flow value as a string.
        """
        return str(sd["max_flow"])


# ═══════════════════════════════════════════════════════════════════
# 8. PLANAR CHECK (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class PlanarCheckGenerator(StepGenerator):
    """Check planarity using necessary conditions.

    Verifies E <= 3V - 6 (necessary condition for planarity). For
    complete and complete bipartite graphs, identifies K_5 or K_{3,3}
    as obstructions.

    Difficulty scaling:
        Difficulty 1-3: sparse graph (clearly planar).
        Difficulty 4-6: denser graph, may fail E <= 3V-6.
        Difficulty 7-8: K_5 or K_{3,3} detection.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "planar_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls graph type.

        Returns:
            Task description string.
        """
        return "check planarity of graph"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a planarity checking problem.

        Args:
            difficulty: Controls graph density and type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Sparse planar graph (tree + a few edges)
            n = self._rng.randint(4, 6)
            edges = set()
            for i in range(1, n):
                edges.add((min(0, i), max(0, i)) if self._rng.random() < 0.5
                          else (min(i - 1, i), max(i - 1, i)))
            # Ensure tree
            for i in range(1, n):
                edges.add((i - 1, i))
            e_count = len(edges)
            bound = 3 * n - 6
            planar = True
            reason = f"E={e_count} <= 3V-6={bound}"
            obstruction = None
        elif difficulty <= 6:
            # Dense graph that may fail condition
            n = self._rng.randint(4, 6)
            edges = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if self._rng.random() < 0.7:
                        edges.add((i, j))
            e_count = len(edges)
            bound = 3 * n - 6
            planar = e_count <= bound
            reason = f"E={e_count} {'<=' if planar else '>'} 3V-6={bound}"
            obstruction = None if planar else "too many edges"
        else:
            # K_5 or K_{3,3}
            graph_type = self._rng.choice(["K5", "K33"])
            if graph_type == "K5":
                n = 5
                edges = set()
                for i in range(5):
                    for j in range(i + 1, 5):
                        edges.add((i, j))
                e_count = 10
                bound = 3 * 5 - 6  # 9
                planar = False
                reason = f"E={e_count} > 3V-6={bound}"
                obstruction = "contains K_5"
            else:
                n = 6
                edges = set()
                for i in range(3):
                    for j in range(3, 6):
                        edges.add((i, j))
                e_count = 9
                bound = 3 * 6 - 6  # 12
                # K_{3,3} is not planar despite E <= 3V-6
                planar = False
                reason = f"E={e_count} <= 3V-6={bound} but contains K_{{3,3}}"
                obstruction = "contains K_{3,3}"

        edge_str = ", ".join(f"{u}-{v}" for u, v in sorted(edges))
        problem = f"V={n}, edges=[{edge_str}]"
        return problem, {
            "n": n, "e_count": e_count, "bound": bound,
            "planar": planar, "reason": reason,
            "obstruction": obstruction,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        steps = [
            f"V={sd['n']}, E={sd['e_count']}, 3V-6={sd['bound']}",
            sd["reason"],
        ]
        if sd["obstruction"]:
            steps.append(f"obstruction: {sd['obstruction']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            'planar' or 'not planar'.
        """
        return "planar" if sd["planar"] else "not planar"


# ═══════════════════════════════════════════════════════════════════
# 9. LATTICE OPERATIONS (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class LatticeOperationsGenerator(StepGenerator):
    """Compute meet and join in a finite lattice.

    Given a Hasse diagram of a divisor lattice, computes the greatest
    lower bound (meet) and least upper bound (join) of two elements.

    Difficulty scaling:
        Difficulty 1-3: divisor lattice of 6 or 12.
        Difficulty 4-6: divisor lattice of 30 or 36.
        Difficulty 7-8: divisor lattice of 60 or 72.

    Prerequisites:
        set_operations (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lattice_operations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls lattice size.

        Returns:
            Task description string.
        """
        return "compute meet and join in divisor lattice"

    def _divisors(self, n: int) -> list[int]:
        """Return sorted divisors of n.

        Args:
            n: Positive integer.

        Returns:
            Sorted list of all positive divisors.
        """
        divs = []
        for i in range(1, n + 1):
            if n % i == 0:
                divs.append(i)
        return divs

    def _gcd(self, a: int, b: int) -> int:
        """Compute greatest common divisor.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            GCD of a and b.
        """
        while b:
            a, b = b, a % b
        return a

    def _lcm(self, a: int, b: int) -> int:
        """Compute least common multiple.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            LCM of a and b.
        """
        return a * b // self._gcd(a, b)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lattice operations problem.

        Args:
            difficulty: Controls lattice size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([6, 12])
        elif difficulty <= 6:
            n = self._rng.choice([30, 36])
        else:
            n = self._rng.choice([60, 72])

        divs = self._divisors(n)
        # Pick two distinct divisors (not 1 and not n for interest)
        candidates = [d for d in divs if d != 1 and d != n]
        if len(candidates) < 2:
            candidates = divs
        a, b = self._rng.sample(candidates, 2)

        meet = self._gcd(a, b)
        join = self._lcm(a, b)
        # Ensure join divides n (it must for a divisor lattice)
        if n % join != 0:
            join = n  # Fallback: LUB is n itself

        problem = f"divisor lattice of {n}: meet and join of {a} and {b}"
        return problem, {
            "n": n, "a": a, "b": b,
            "meet": meet, "join": join,
            "divs": divs,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        return [
            f"lattice: divisors of {sd['n']} = {sd['divs']}",
            f"meet({sd['a']},{sd['b']}) = gcd = {sd['meet']}",
            f"join({sd['a']},{sd['b']}) = lcm = {sd['join']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            Meet and join as a string.
        """
        return f"meet={sd['meet']}, join={sd['join']}"


# ═══════════════════════════════════════════════════════════════════
# 10. PARTITION FUNCTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class PartitionFunctionGenerator(StepGenerator):
    """Count integer partitions of n for small n.

    Uses the recursive definition where p(n) counts the number of ways
    to write n as a sum of positive integers (order does not matter).
    Known values: p(1)=1, p(2)=2, p(3)=3, p(4)=5, p(5)=7, p(6)=11,
    p(7)=15, p(8)=22, p(9)=30, p(10)=42, p(11)=56, p(12)=77.

    Difficulty scaling:
        Difficulty 1-3: n in [1, 4].
        Difficulty 4-6: n in [5, 8].
        Difficulty 7-8: n in [9, 12].

    Prerequisites:
        catalan (tier 6).
    """

    # Precomputed partition counts
    _P = {
        0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 11, 7: 15,
        8: 22, 9: 30, 10: 42, 11: 56, 12: 77,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "partition_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["catalan"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls n.

        Returns:
            Task description string.
        """
        return "count integer partitions of n"

    def _partitions_list(self, n: int, max_val: int | None = None) -> list[list[int]]:
        """Generate all partitions of n with parts <= max_val.

        Args:
            n: Integer to partition.
            max_val: Maximum part value (defaults to n).

        Returns:
            List of partitions, each a sorted list of parts.
        """
        if max_val is None:
            max_val = n
        if n == 0:
            return [[]]
        if n < 0 or max_val <= 0:
            return []
        result = []
        for first in range(min(n, max_val), 0, -1):
            for rest in self._partitions_list(n - first, first):
                result.append([first] + rest)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a partition counting problem.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 4)
        elif difficulty <= 6:
            n = self._rng.randint(5, 8)
        else:
            n = self._rng.randint(9, 12)

        count = self._P[n]

        # Show a few example partitions for small n
        if n <= 6:
            parts = self._partitions_list(n)
            examples = ["+".join(str(p) for p in part) for part in parts[:4]]
        else:
            examples = [str(n), f"1+...+1 ({n} ones)"]

        problem = f"p({n}) = ? (number of integer partitions)"
        return problem, {
            "n": n, "count": count, "examples": examples,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            Step strings in execution order.
        """
        steps = [f"partitions of {sd['n']}: {', '.join(sd['examples'])}..."]
        steps.append(f"p({sd['n']}) = {sd['count']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data dictionary.

        Returns:
            The partition count as a string.
        """
        return str(sd["count"])
