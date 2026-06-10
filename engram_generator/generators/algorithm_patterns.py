"""Algorithm patterns generators.

8 generators across tiers 5-7 covering divide-and-conquer recurrences,
amortised analysis, greedy proofs, DP optimal substructure, NP reductions,
approximation ratios, randomised algorithms, and online algorithms.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Divide-and-Conquer Recurrence (tier 5)
# ---------------------------------------------------------------------------

@register
class DivideConquerRecurrenceGenerator(StepGenerator):
    """Solve T(n) = aT(n/b) + f(n) using the Master theorem.

    Generates recurrences with random a, b, and f(n) parameters, then
    applies one of the three Master theorem cases by comparing
    log_b(a) with the exponent of f(n).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "divide_conquer_recurrence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recurrence_solve"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "solve divide-and-conquer recurrence using Master theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Master theorem recurrence problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        b = self._rng.choice([2, 3, 4])
        # Choose case by varying a and c (exponent of f(n) = n^c)
        case = self._rng.choice([1, 2, 3])

        if case == 1:
            # Case 1: c < log_b(a), so T(n) = Theta(n^log_b(a))
            a = b ** 2  # log_b(a) = 2
            c = self._rng.choice([0, 1])
            log_ba = round(math.log(a) / math.log(b), 4)
            result = f"Theta(n^{log_ba})"
            reason = f"c={c} < log_{b}({a})={log_ba} => Case 1"
        elif case == 2:
            # Case 2: c = log_b(a), so T(n) = Theta(n^c * log n)
            c = self._rng.choice([1, 2])
            a = b ** c  # log_b(a) = c
            log_ba = float(c)
            result = f"Theta(n^{c}*log(n))"
            reason = f"c={c} = log_{b}({a})={log_ba} => Case 2"
        else:
            # Case 3: c > log_b(a), so T(n) = Theta(n^c)
            a = self._rng.choice([1, 2])
            c = self._rng.randint(2, 3)
            log_ba = round(math.log(a) / math.log(b), 4)
            result = f"Theta(n^{c})"
            reason = f"c={c} > log_{b}({a})={log_ba} => Case 3"

        f_str = f"n^{c}" if c > 0 else "1"
        problem = f"T(n) = {a}T(n/{b}) + {f_str}"

        return problem, {
            "a": a,
            "b": b,
            "c": c,
            "log_ba": log_ba,
            "case": case,
            "reason": reason,
            "result": result,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate Master theorem analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"a={d['a']}, b={d['b']}, f(n)=n^{d['c']}",
            f"log_{d['b']}({d['a']}) = {d['log_ba']}",
            d["reason"],
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the asymptotic solution.

        Args:
            solution_data: All computed solution information.

        Returns:
            Asymptotic complexity string.
        """
        return solution_data["result"]


# ---------------------------------------------------------------------------
# 2. Amortised Analysis (tier 6)
# ---------------------------------------------------------------------------

@register
class AmortisedAnalysisGenerator(StepGenerator):
    """Compute amortised cost using the aggregate method.

    Demonstrates dynamic array doubling: total cost of n insertions
    is n + sum of doubling copies, divided by n for amortised cost.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "amortised_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute amortised cost via aggregate method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an amortised analysis problem on dynamic arrays.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.choice([8, 16, 32, 64])
        if difficulty >= 5:
            n = self._rng.choice([32, 64, 128])

        # Each insertion costs 1, doubling at powers of 2 adds copy cost
        insert_cost = n
        copy_cost = 0
        doublings = []
        k = 1
        while k < n:
            copy_cost += k
            doublings.append(k)
            k *= 2

        total_cost = insert_cost + copy_cost
        amortised = round(total_cost / n, 4)

        problem = f"dynamic array: {n} insertions, initial capacity 1"
        return problem, {
            "n": n,
            "insert_cost": insert_cost,
            "copy_cost": copy_cost,
            "doublings": doublings,
            "total_cost": total_cost,
            "amortised": amortised,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate aggregate method steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        dbl_str = "+".join(str(x) for x in d["doublings"])
        return [
            f"insert cost = {d['n']} (1 per op)",
            f"copy cost = {dbl_str} = {d['copy_cost']}",
            f"total = {d['insert_cost']}+{d['copy_cost']} = {d['total_cost']}",
            f"amortised = {d['total_cost']}/{d['n']} = {d['amortised']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the amortised cost per operation.

        Args:
            solution_data: All computed solution information.

        Returns:
            Amortised cost string.
        """
        return f"amortised_cost={solution_data['amortised']}"


# ---------------------------------------------------------------------------
# 3. Greedy Proof (tier 7)
# ---------------------------------------------------------------------------

@register
class GreedyProofGenerator(StepGenerator):
    """Prove greedy choice property via exchange argument.

    Uses activity selection template: show that choosing the earliest
    finishing activity keeps at least as many activities as optimal.
    """

    _TEMPLATES: list[dict] = [
        {
            "name": "activity selection",
            "activities": [(1, 3), (2, 5), (4, 7), (6, 9), (8, 10)],
            "greedy_rule": "earliest finish time",
            "proof_sketch": "exchange: replace OPT first with greedy first, no conflict",
        },
        {
            "name": "activity selection",
            "activities": [(0, 2), (1, 4), (3, 5), (5, 8), (6, 9)],
            "greedy_rule": "earliest finish time",
            "proof_sketch": "exchange: replace OPT first with greedy first, no conflict",
        },
        {
            "name": "fractional knapsack",
            "items": [(60, 10), (100, 20), (120, 30)],
            "greedy_rule": "highest value/weight ratio",
            "proof_sketch": "exchange: swap suboptimal fraction with higher ratio item",
        },
        {
            "name": "fractional knapsack",
            "items": [(40, 5), (80, 10), (50, 15), (90, 20)],
            "greedy_rule": "highest value/weight ratio",
            "proof_sketch": "exchange: swap suboptimal fraction with higher ratio item",
        },
        {
            "name": "coin change (canonical)",
            "denoms": [1, 5, 10, 25],
            "greedy_rule": "largest denomination first",
            "proof_sketch": "exchange: fewer large coins => more small coins => worse",
        },
        {
            "name": "interval scheduling",
            "activities": [(0, 6), (1, 4), (3, 5), (5, 7), (8, 9)],
            "greedy_rule": "earliest finish time",
            "proof_sketch": "stays-ahead: greedy finish <= OPT finish at each step",
        },
        {
            "name": "interval scheduling",
            "activities": [(1, 2), (2, 4), (3, 6), (5, 7), (7, 9)],
            "greedy_rule": "earliest finish time",
            "proof_sketch": "stays-ahead: greedy finish <= OPT finish at each step",
        },
        {
            "name": "Huffman coding",
            "freqs": [5, 9, 12, 13, 16, 45],
            "greedy_rule": "merge two lowest-frequency nodes",
            "proof_sketch": "exchange: swapping deeper node with lower freq reduces cost",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "greedy_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "prove greedy choice property via exchange argument"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a greedy proof problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        if "activities" in tmpl:
            acts = tmpl["activities"]
            # Greedy selection by earliest finish
            selected = []
            last_end = -1
            for start, end in sorted(acts, key=lambda x: x[1]):
                if start >= last_end:
                    selected.append((start, end))
                    last_end = end
            data_str = ", ".join(f"({s},{e})" for s, e in acts)
            sel_str = ", ".join(f"({s},{e})" for s, e in selected)
            answer = f"greedy selects {len(selected)}: {sel_str}"
        elif "items" in tmpl:
            items = tmpl["items"]
            ratios = [(v / w, v, w) for v, w in items]
            ratios.sort(reverse=True)
            data_str = ", ".join(f"(v={v},w={w})" for v, w in items)
            ratio_str = ", ".join(
                f"{round(r, 4)}" for r, _, _ in ratios
            )
            answer = f"ratios=[{ratio_str}], sort desc, fill greedily"
        else:
            data_str = f"denoms={tmpl['denoms']}"
            answer = f"use largest denom first: {tmpl['denoms'][::-1]}"

        problem = f"{tmpl['name']}: {data_str}"
        return problem, {
            "name": tmpl["name"],
            "rule": tmpl["greedy_rule"],
            "proof": tmpl["proof_sketch"],
            "answer": answer,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate greedy proof steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"problem: {d['name']}",
            f"greedy rule: {d['rule']}",
            f"proof: {d['proof']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the greedy solution and proof sketch.

        Args:
            solution_data: All computed solution information.

        Returns:
            Greedy result string.
        """
        return solution_data["answer"]


# ---------------------------------------------------------------------------
# 4. DP Optimal Substructure (tier 6)
# ---------------------------------------------------------------------------

@register
class DPOptimalSubstructureGenerator(StepGenerator):
    """Identify optimal substructure in dynamic programming problems.

    Shows that OPT(n) depends on OPT(smaller) using rod cutting and
    matrix chain multiplication examples.
    """

    _TEMPLATES: list[dict] = [
        {
            "name": "rod cutting",
            "prices": [1, 5, 8, 9],
            "length": 4,
            "recurrence": "OPT(n) = max(p[i] + OPT(n-i)) for i=1..n",
        },
        {
            "name": "rod cutting",
            "prices": [2, 5, 7, 8, 10],
            "length": 5,
            "recurrence": "OPT(n) = max(p[i] + OPT(n-i)) for i=1..n",
        },
        {
            "name": "rod cutting",
            "prices": [1, 5, 8, 9, 10, 17],
            "length": 6,
            "recurrence": "OPT(n) = max(p[i] + OPT(n-i)) for i=1..n",
        },
        {
            "name": "matrix chain",
            "dims": [10, 30, 5, 60],
            "recurrence": "OPT(i,j) = min(OPT(i,k)+OPT(k+1,j)+d[i]*d[k+1]*d[j+1])",
        },
        {
            "name": "matrix chain",
            "dims": [5, 10, 3, 12, 5],
            "recurrence": "OPT(i,j) = min(OPT(i,k)+OPT(k+1,j)+d[i]*d[k+1]*d[j+1])",
        },
        {
            "name": "matrix chain",
            "dims": [40, 20, 30, 10, 30],
            "recurrence": "OPT(i,j) = min(OPT(i,k)+OPT(k+1,j)+d[i]*d[k+1]*d[j+1])",
        },
        {
            "name": "0-1 knapsack",
            "items": [(60, 10), (100, 20), (120, 30)],
            "capacity": 50,
            "recurrence": "OPT(i,w) = max(OPT(i-1,w), v[i]+OPT(i-1,w-w[i]))",
        },
        {
            "name": "0-1 knapsack",
            "items": [(40, 5), (50, 10), (70, 15)],
            "capacity": 25,
            "recurrence": "OPT(i,w) = max(OPT(i-1,w), v[i]+OPT(i-1,w-w[i]))",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dp_optimal_substructure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["memoisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify optimal substructure in DP problem"

    def _solve_rod(self, prices: list[int], length: int) -> int:
        """Solve the rod cutting problem via bottom-up DP.

        Args:
            prices: Price list indexed by piece length (1-indexed).
            length: Total rod length.

        Returns:
            Maximum revenue.
        """
        dp = [0] * (length + 1)
        for j in range(1, length + 1):
            for i in range(1, min(j, len(prices)) + 1):
                dp[j] = max(dp[j], prices[i - 1] + dp[j - i])
        return dp[length]

    def _solve_mcm(self, dims: list[int]) -> int:
        """Solve matrix chain multiplication via DP.

        Args:
            dims: Dimension array of length n+1 for n matrices.

        Returns:
            Minimum scalar multiplications.
        """
        n = len(dims) - 1
        dp = [[0] * n for _ in range(n)]
        for chain_len in range(2, n + 1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                dp[i][j] = float("inf")
                for k in range(i, j):
                    cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                    dp[i][j] = min(dp[i][j], cost)
        return dp[0][n - 1]

    def _solve_knapsack(self, items: list[tuple[int, int]],
                        capacity: int) -> int:
        """Solve 0-1 knapsack via DP.

        Args:
            items: List of (value, weight) tuples.
            capacity: Knapsack capacity.

        Returns:
            Maximum value.
        """
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            v, w = items[i - 1]
            for c in range(capacity + 1):
                dp[i][c] = dp[i - 1][c]
                if w <= c:
                    dp[i][c] = max(dp[i][c], v + dp[i - 1][c - w])
        return dp[n][capacity]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DP optimal substructure problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        if tmpl["name"] == "rod cutting":
            opt_val = self._solve_rod(tmpl["prices"], tmpl["length"])
            data_str = f"prices={tmpl['prices']}, length={tmpl['length']}"
        elif tmpl["name"] == "matrix chain":
            opt_val = self._solve_mcm(tmpl["dims"])
            data_str = f"dims={tmpl['dims']}"
        else:
            opt_val = self._solve_knapsack(tmpl["items"], tmpl["capacity"])
            items_str = ", ".join(f"(v={v},w={w})" for v, w in tmpl["items"])
            data_str = f"items=[{items_str}], cap={tmpl['capacity']}"

        problem = f"{tmpl['name']}: {data_str}"
        return problem, {
            "name": tmpl["name"],
            "recurrence": tmpl["recurrence"],
            "opt_val": opt_val,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate DP substructure identification steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"problem: {d['name']}",
            f"recurrence: {d['recurrence']}",
            f"OPT depends on smaller subproblems",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the optimal value.

        Args:
            solution_data: All computed solution information.

        Returns:
            Optimal value string.
        """
        return f"OPT={solution_data['opt_val']}"


# ---------------------------------------------------------------------------
# 5. NP Reduction (tier 7)
# ---------------------------------------------------------------------------

@register
class NPReductionGenerator(StepGenerator):
    """Demonstrate polynomial-time reduction between NP-complete problems.

    Uses template reductions: SAT to 3-SAT, CLIQUE to VERTEX-COVER,
    and VERTEX-COVER to SET-COVER with small concrete instances.
    """

    _TEMPLATES: list[dict] = [
        {
            "from_prob": "SAT",
            "to_prob": "3-SAT",
            "instance": "(x1 OR x2) AND (x3)",
            "transform": "pad short clauses: (x1 OR x2 OR x2), (x3 OR x3 OR x3)",
            "result_size": "2 clauses, 3 literals each",
            "poly": "O(m) where m = #clauses",
        },
        {
            "from_prob": "SAT",
            "to_prob": "3-SAT",
            "instance": "(x1 OR x2 OR x3 OR x4)",
            "transform": "split: (x1 OR x2 OR y) AND (NOT y OR x3 OR x4)",
            "result_size": "2 clauses from 1 long clause",
            "poly": "O(k) per clause of length k",
        },
        {
            "from_prob": "CLIQUE",
            "to_prob": "VERTEX-COVER",
            "instance": "G=(V={a,b,c,d}, E={(a,b),(b,c),(c,d)}), k=2",
            "transform": "complement G, ask VC of size |V|-k=2",
            "result_size": "|V|-k = 4-2 = 2",
            "poly": "O(|V|^2) to complement edges",
        },
        {
            "from_prob": "CLIQUE",
            "to_prob": "VERTEX-COVER",
            "instance": "G=(V={1,2,3,4,5}, E={(1,2),(2,3),(3,4),(4,5),(1,5)}), k=3",
            "transform": "complement G, ask VC of size |V|-k=2",
            "result_size": "|V|-k = 5-3 = 2",
            "poly": "O(|V|^2) to complement edges",
        },
        {
            "from_prob": "VERTEX-COVER",
            "to_prob": "SET-COVER",
            "instance": "G=(V={a,b,c}, E={(a,b),(b,c)}), k=1",
            "transform": "universe=E, set S_v={edges incident to v}",
            "result_size": "S_b covers both edges, k=1 set",
            "poly": "O(|V|*|E|) to build sets",
        },
        {
            "from_prob": "3-SAT",
            "to_prob": "CLIQUE",
            "instance": "(x1 OR x2 OR x3) AND (NOT x1 OR x2 OR x3)",
            "transform": "node per literal per clause, edge if compatible",
            "result_size": "6 nodes, clique of size 2 = #clauses",
            "poly": "O(m^2 * k^2) nodes and edges",
        },
        {
            "from_prob": "VERTEX-COVER",
            "to_prob": "SET-COVER",
            "instance": "G=(V={1,2,3,4}, E={(1,2),(2,3),(3,4)}), k=2",
            "transform": "universe=E, S_v={edges incident to v}",
            "result_size": "S_2 and S_3 cover all edges, k=2",
            "poly": "O(|V|*|E|) to build sets",
        },
        {
            "from_prob": "3-SAT",
            "to_prob": "INDEPENDENT-SET",
            "instance": "(x1 OR x2 OR NOT x3) AND (NOT x1 OR x3 OR x2)",
            "transform": "triangle per clause, edges between contradictions",
            "result_size": "6 nodes, IS of size 2 = #clauses",
            "poly": "O(m^2 * k^2)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "np_reduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sat_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "show polynomial reduction between NP-complete problems"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NP reduction problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = (
            f"reduce {tmpl['from_prob']} to {tmpl['to_prob']}: "
            f"{tmpl['instance']}"
        )
        return problem, {
            "from_prob": tmpl["from_prob"],
            "to_prob": tmpl["to_prob"],
            "transform": tmpl["transform"],
            "result_size": tmpl["result_size"],
            "poly": tmpl["poly"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate reduction steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"{d['from_prob']} <= {d['to_prob']}",
            f"transform: {d['transform']}",
            f"output size: {d['result_size']}",
            f"time: {d['poly']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the reduction summary.

        Args:
            solution_data: All computed solution information.

        Returns:
            Reduction result string.
        """
        d = solution_data
        return f"{d['from_prob']}<=p{d['to_prob']}, poly={d['poly']}"


# ---------------------------------------------------------------------------
# 6. Approximation Ratio (tier 6)
# ---------------------------------------------------------------------------

@register
class ApproximationRatioGenerator(StepGenerator):
    """Compute approximation ratio for classic approximation algorithms.

    Covers vertex cover (2-approx), set cover (ln n), and bin packing
    (11/9 + epsilon) with concrete numerical instances.
    """

    _TEMPLATES: list[dict] = [
        {
            "algo": "vertex cover (greedy matching)",
            "instance": "edges={(a,b),(b,c),(c,d),(d,e)}",
            "alg_size": 4,
            "opt_size": 2,
            "ratio": 2.0,
            "bound": "2-approx",
        },
        {
            "algo": "vertex cover (greedy matching)",
            "instance": "edges={(1,2),(2,3),(3,4),(4,5),(5,6)}",
            "alg_size": 4,
            "opt_size": 2,
            "ratio": 2.0,
            "bound": "2-approx",
        },
        {
            "algo": "vertex cover (greedy matching)",
            "instance": "edges={(a,b),(a,c),(b,d),(c,d)}",
            "alg_size": 4,
            "opt_size": 2,
            "ratio": 2.0,
            "bound": "2-approx",
        },
        {
            "algo": "set cover (greedy)",
            "instance": "U={1..6}, S1={1,2,3}, S2={3,4,5}, S3={5,6}",
            "alg_size": 3,
            "opt_size": 2,
            "ratio": 1.5,
            "bound": "ln(n)-approx, ln(6)=1.7918",
        },
        {
            "algo": "set cover (greedy)",
            "instance": "U={1..8}, S1={1,2,3,4}, S2={3,4,5,6}, S3={5,6,7,8}",
            "alg_size": 3,
            "opt_size": 2,
            "ratio": 1.5,
            "bound": "ln(n)-approx, ln(8)=2.0794",
        },
        {
            "algo": "bin packing (first fit decreasing)",
            "instance": "items=[0.7,0.5,0.4,0.3,0.2,0.1], cap=1.0",
            "alg_size": 3,
            "opt_size": 2,
            "ratio": 1.5,
            "bound": "11/9*OPT+6/9",
        },
        {
            "algo": "bin packing (first fit decreasing)",
            "instance": "items=[0.8,0.5,0.4,0.3,0.2], cap=1.0",
            "alg_size": 3,
            "opt_size": 2,
            "ratio": 1.5,
            "bound": "11/9*OPT+6/9",
        },
        {
            "algo": "TSP (2-approx via MST)",
            "instance": "4 cities, metric distances",
            "alg_size": 20,
            "opt_size": 12,
            "ratio": 1.6667,
            "bound": "2-approx (metric TSP)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "approximation_ratio"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute approximation ratio ALG/OPT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an approximation ratio problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = f"{tmpl['algo']}: {tmpl['instance']}"
        ratio = round(tmpl["alg_size"] / tmpl["opt_size"], 4)
        return problem, {
            "algo": tmpl["algo"],
            "alg_size": tmpl["alg_size"],
            "opt_size": tmpl["opt_size"],
            "ratio": ratio,
            "bound": tmpl["bound"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate approximation analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"ALG = {d['alg_size']}",
            f"OPT = {d['opt_size']}",
            f"ratio = {d['alg_size']}/{d['opt_size']} = {d['ratio']}",
            f"guarantee: {d['bound']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the approximation ratio.

        Args:
            solution_data: All computed solution information.

        Returns:
            Ratio string with bound.
        """
        d = solution_data
        return f"ratio={d['ratio']}, bound={d['bound']}"


# ---------------------------------------------------------------------------
# 7. Randomised Algorithm (tier 6)
# ---------------------------------------------------------------------------

@register
class RandomisedAlgorithmGenerator(StepGenerator):
    """Analyze expected runtime of randomised algorithms.

    Demonstrates randomised QuickSort expected runtime O(n log n) via
    linearity of expectation, and randomised selection (QuickSelect).
    """

    _TEMPLATES: list[dict] = [
        {
            "algo": "randomised QuickSort",
            "n": 8,
            "analysis": "E[comparisons] = sum_{i<j} 2/(j-i+1)",
            "bound": "O(n*log(n))",
        },
        {
            "algo": "randomised QuickSort",
            "n": 16,
            "analysis": "E[comparisons] = sum_{i<j} 2/(j-i+1)",
            "bound": "O(n*log(n))",
        },
        {
            "algo": "randomised QuickSort",
            "n": 32,
            "analysis": "E[comparisons] = sum_{i<j} 2/(j-i+1)",
            "bound": "O(n*log(n))",
        },
        {
            "algo": "QuickSelect (median)",
            "n": 8,
            "analysis": "E[T(n)] = n + E[T(3n/4)] (good pivot prob >= 1/2)",
            "bound": "O(n)",
        },
        {
            "algo": "QuickSelect (median)",
            "n": 16,
            "analysis": "E[T(n)] = n + E[T(3n/4)] (good pivot prob >= 1/2)",
            "bound": "O(n)",
        },
        {
            "algo": "randomised min-cut (Karger)",
            "n": 6,
            "analysis": "P[success] >= 2/(n*(n-1)), repeat n^2*ln(n) times",
            "bound": "O(n^4*log(n))",
        },
        {
            "algo": "randomised min-cut (Karger)",
            "n": 10,
            "analysis": "P[success] >= 2/(n*(n-1)), repeat n^2*ln(n) times",
            "bound": "O(n^4*log(n))",
        },
        {
            "algo": "Miller-Rabin primality",
            "n": 100,
            "analysis": "P[error] <= (1/4)^k after k rounds",
            "bound": "O(k*log^2(n))",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "randomised_algorithm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "analyze expected runtime of randomised algorithm"

    def _compute_expected_comparisons(self, n: int) -> float:
        """Compute expected comparisons for randomised QuickSort.

        Args:
            n: Number of elements.

        Returns:
            Expected number of comparisons.
        """
        total = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                total += 2.0 / (j - i + 1)
        return round(total, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a randomised algorithm analysis problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        n = tmpl["n"]

        if "QuickSort" in tmpl["algo"]:
            expected = self._compute_expected_comparisons(n)
            nlogn = round(n * math.log2(n), 4)
            detail = f"E[comp]={expected}, n*log2(n)={nlogn}"
        elif "QuickSelect" in tmpl["algo"]:
            expected = round(4.0 * n, 4)
            detail = f"E[ops] <= 4n = {expected}"
        elif "Karger" in tmpl["algo"]:
            prob = round(2.0 / (n * (n - 1)), 4)
            repeats = round(n * n * math.log(n), 4)
            detail = f"P[success]={prob}, repeats~{repeats}"
            expected = repeats
        else:
            k = 10
            error = round((0.25) ** k, 4)
            detail = f"k={k} rounds, P[error]={error}"
            expected = k

        problem = f"{tmpl['algo']}, n={n}"
        return problem, {
            "algo": tmpl["algo"],
            "n": n,
            "analysis": tmpl["analysis"],
            "bound": tmpl["bound"],
            "detail": detail,
            "expected": expected,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate randomised analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"algo: {d['algo']}, n={d['n']}",
            f"analysis: {d['analysis']}",
            d["detail"],
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the expected complexity.

        Args:
            solution_data: All computed solution information.

        Returns:
            Bound string.
        """
        return solution_data["bound"]


# ---------------------------------------------------------------------------
# 8. Online Algorithm (tier 7)
# ---------------------------------------------------------------------------

@register
class OnlineAlgorithmGenerator(StepGenerator):
    """Compute competitive ratio for online algorithms.

    Covers ski rental (2-competitive), paging/LRU (k-competitive),
    and online load balancing (2-1/m competitive).
    """

    _TEMPLATES: list[dict] = [
        {
            "algo": "ski rental",
            "buy_cost": 10,
            "rent_cost": 1,
            "days": 15,
            "strategy": "rent until day b=buy_cost, then buy",
        },
        {
            "algo": "ski rental",
            "buy_cost": 20,
            "rent_cost": 1,
            "days": 25,
            "strategy": "rent until day b=buy_cost, then buy",
        },
        {
            "algo": "ski rental",
            "buy_cost": 5,
            "rent_cost": 1,
            "days": 8,
            "strategy": "rent until day b=buy_cost, then buy",
        },
        {
            "algo": "paging (LRU)",
            "cache_size": 3,
            "pages": [1, 2, 3, 4, 1, 2, 5, 1],
            "strategy": "evict least recently used page",
        },
        {
            "algo": "paging (LRU)",
            "cache_size": 4,
            "pages": [1, 2, 3, 4, 5, 1, 2, 3],
            "strategy": "evict least recently used page",
        },
        {
            "algo": "load balancing (greedy)",
            "machines": 3,
            "jobs": [5, 3, 7, 2, 4, 6],
            "strategy": "assign job to least loaded machine",
        },
        {
            "algo": "load balancing (greedy)",
            "machines": 2,
            "jobs": [4, 3, 5, 2, 6],
            "strategy": "assign job to least loaded machine",
        },
        {
            "algo": "paging (FIFO)",
            "cache_size": 3,
            "pages": [1, 2, 3, 1, 4, 2, 5, 3],
            "strategy": "evict oldest cached page",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "online_algorithm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["approximation_ratio"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute competitive ratio for online algorithm"

    def _solve_ski_rental(self, buy: int, rent: int,
                          days: int) -> tuple[list[str], float, float, float]:
        """Compute ski rental costs.

        Args:
            buy: One-time purchase cost.
            rent: Daily rental cost.
            days: Total skiing days.

        Returns:
            Tuple of (steps, alg_cost, opt_cost, ratio).
        """
        # Online: rent until day buy, then buy (if still skiing)
        if days <= buy:
            alg_cost = float(days * rent)
        else:
            alg_cost = float((buy - 1) * rent + buy)
        opt_cost = float(min(days * rent, buy))
        ratio = round(alg_cost / opt_cost, 4) if opt_cost > 0 else 1.0
        steps = [
            f"online: rent {min(days, buy - 1)} days + buy if needed",
            f"ALG cost = {alg_cost}",
            f"OPT cost = {opt_cost}",
        ]
        return steps, alg_cost, opt_cost, ratio

    def _solve_paging(self, cache_size: int,
                      pages: list[int],
                      policy: str) -> tuple[list[str], int]:
        """Simulate paging with given policy.

        Args:
            cache_size: Number of cache slots.
            pages: Page request sequence.
            policy: Eviction policy name (LRU or FIFO).

        Returns:
            Tuple of (steps, fault_count).
        """
        cache: list[int] = []
        faults = 0
        steps = []
        for p in pages:
            if p in cache:
                if policy == "LRU":
                    cache.remove(p)
                    cache.append(p)
                steps.append(f"req {p}: hit")
            else:
                faults += 1
                if len(cache) >= cache_size:
                    evicted = cache.pop(0)
                    steps.append(f"req {p}: fault, evict {evicted}")
                else:
                    steps.append(f"req {p}: fault, load")
                cache.append(p)
        return steps, faults

    def _solve_load_balance(self, machines: int,
                            jobs: list[int]) -> tuple[list[str], int, int]:
        """Simulate greedy load balancing.

        Args:
            machines: Number of machines.
            jobs: Job sizes.

        Returns:
            Tuple of (steps, makespan_alg, makespan_opt).
        """
        loads = [0] * machines
        steps = []
        for j in jobs:
            idx = loads.index(min(loads))
            loads[idx] += j
            steps.append(f"job {j} -> M{idx} (load={loads[idx]})")
        makespan_alg = max(loads)
        makespan_opt = max(sum(jobs) // machines, max(jobs))
        return steps, makespan_alg, makespan_opt

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an online algorithm problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        if tmpl["algo"] == "ski rental":
            steps, alg, opt, ratio = self._solve_ski_rental(
                tmpl["buy_cost"], tmpl["rent_cost"], tmpl["days"]
            )
            cr = "2-competitive"
            problem = (
                f"ski rental: buy={tmpl['buy_cost']}, "
                f"rent={tmpl['rent_cost']}/day, days={tmpl['days']}"
            )
        elif "paging" in tmpl["algo"]:
            policy = "LRU" if "LRU" in tmpl["algo"] else "FIFO"
            pages_str = ",".join(str(p) for p in tmpl["pages"])
            steps, faults = self._solve_paging(
                tmpl["cache_size"], tmpl["pages"], policy
            )
            k = tmpl["cache_size"]
            alg = float(faults)
            opt = 1.0  # lower bound placeholder
            ratio = round(alg / max(opt, 1), 4)
            cr = f"k={k}-competitive"
            problem = (
                f"{tmpl['algo']}: cache={k}, "
                f"pages=[{pages_str}]"
            )
        else:
            m = tmpl["machines"]
            jobs_str = ",".join(str(j) for j in tmpl["jobs"])
            steps, alg_ms, opt_ms = self._solve_load_balance(
                m, tmpl["jobs"]
            )
            alg = float(alg_ms)
            opt = float(opt_ms)
            ratio = round(alg / max(opt, 1), 4)
            cr_bound = round(2.0 - 1.0 / m, 4)
            cr = f"{cr_bound}-competitive"
            problem = (
                f"load balance: m={m}, "
                f"jobs=[{jobs_str}]"
            )

        return problem, {
            "steps": steps,
            "strategy": tmpl["strategy"],
            "alg": alg,
            "opt": opt,
            "ratio": ratio,
            "competitive_ratio": cr,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the online algorithm simulation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the competitive ratio.

        Args:
            solution_data: All computed solution information.

        Returns:
            Competitive ratio string.
        """
        d = solution_data
        return f"ALG={d['alg']}, OPT={d['opt']}, CR={d['competitive_ratio']}"
