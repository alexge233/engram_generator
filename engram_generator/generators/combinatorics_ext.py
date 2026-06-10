"""Extended combinatorics generators.

8 generators across tiers 4-5 covering multinomial coefficients,
derangements, Stirling numbers, Bell numbers, the twelvefold way,
inclusion-exclusion principle, Latin squares, and the ballot problem.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Multinomial coefficient (tier 4)
# ---------------------------------------------------------------------------


@register
class MultinomialCoefficientGenerator(StepGenerator):
    """Compute the multinomial coefficient (n; k1, k2, ...) = n! / (k1!*k2!*...).

    Counts arrangements of a multiset.

    Difficulty scaling:
        d1-3: 2 groups, n <= 8.
        d4-6: 3 groups, n <= 10.
        d7-8: 3-4 groups, n <= 12.

    Prerequisites:
        permutation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multinomial_coefficient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["permutation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute multinomial coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multinomial coefficient problem.

        Args:
            difficulty: Controls number of groups and total size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_groups = 2
            n_max = 8
        elif difficulty <= 6:
            n_groups = 3
            n_max = 10
        else:
            n_groups = self._rng.randint(3, 4)
            n_max = 12

        # Generate group sizes that sum to a reasonable n
        parts = [self._rng.randint(1, n_max // n_groups) for _ in range(n_groups)]
        n = sum(parts)

        # Compute multinomial
        numerator = math.factorial(n)
        denominator = 1
        for k in parts:
            denominator *= math.factorial(k)
        result = numerator // denominator

        parts_str = ", ".join(str(k) for k in parts)
        return (
            f"Multinomial ({n}; {parts_str})",
            {"n": n, "parts": parts, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        parts_fac = " * ".join(f"{k}!" for k in sd["parts"])
        return [
            f"{sd['n']}! = {math.factorial(sd['n'])}",
            f"denominator = {parts_fac}",
            f"= {sd['n']}! / ({parts_fac}) = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the multinomial coefficient.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return str(sd["result"])


# ---------------------------------------------------------------------------
# 2. Derangement (tier 5)
# ---------------------------------------------------------------------------


@register
class DerangementComputeGenerator(StepGenerator):
    """Compute the number of derangements D_n and the probability D_n/n!.

    D_n = n! * sum (-1)^k / k! for k=0..n.

    Difficulty scaling:
        d1-4: n in 3..5.
        d5-8: n in 5..8.

    Prerequisites:
        permutation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "derangement_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["permutation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute derangement count"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a derangement computation problem.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(3, 5)
        else:
            n = self._rng.randint(5, 8)

        # D_n = n! * sum (-1)^k / k! for k=0..n
        n_fac = math.factorial(n)
        series_sum = sum((-1) ** k / math.factorial(k) for k in range(n + 1))
        d_n = round(n_fac * series_sum)
        prob = round(d_n / n_fac, 4)

        terms = [f"(-1)^{k}/{k}!" for k in range(n + 1)]

        return (
            f"D_{n}: derangements of {n} elements",
            {"n": n, "d_n": d_n, "n_fac": n_fac,
             "prob": prob, "terms": terms},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        shown = sd["terms"][:5]
        series = " + ".join(shown)
        if len(sd["terms"]) > 5:
            series += " + ..."
        return [
            f"{sd['n']}! = {sd['n_fac']}",
            f"sum = {series}",
            f"D_{sd['n']} = {sd['n_fac']} * sum = {sd['d_n']}",
            f"P(no fixed point) = {sd['d_n']}/{sd['n_fac']} = {sd['prob']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the derangement count and probability.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"D_{sd['n']}={sd['d_n']}, prob={sd['prob']}"


# ---------------------------------------------------------------------------
# 3. Stirling numbers of the second kind (tier 5)
# ---------------------------------------------------------------------------


@register
class StirlingSecondGenerator(StepGenerator):
    """Compute S(n, k) via recurrence: S(n, k) = k*S(n-1, k) + S(n-1, k-1).

    Number of ways to partition n elements into k non-empty subsets.

    Difficulty scaling:
        d1-4: n in 3..5, k in 2..3.
        d5-8: n in 5..7, k in 2..4.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stirling_second"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute Stirling number S(n,k)"

    def _stirling(self, n: int, k: int) -> int:
        """Compute S(n, k) via DP.

        Args:
            n: Number of elements.
            k: Number of non-empty subsets.

        Returns:
            Stirling number of the second kind.
        """
        if n == 0 and k == 0:
            return 1
        if n == 0 or k == 0:
            return 0
        if k > n:
            return 0
        # DP table
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
        return dp[n][k]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Stirling number computation problem.

        Args:
            difficulty: Controls n and k ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(3, 5)
            k = self._rng.randint(2, min(3, n))
        else:
            n = self._rng.randint(5, 7)
            k = self._rng.randint(2, min(4, n))

        # Build DP table for steps
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        steps_log = ["S(0,0) = 1"]
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
                steps_log.append(
                    f"S({i},{j}) = {j}*S({i-1},{j}) + S({i-1},{j-1})"
                    f" = {j}*{dp[i-1][j]} + {dp[i-1][j-1]} = {dp[i][j]}"
                )

        result = dp[n][k]
        return (
            f"S({n},{k}): partition {n} elements into {k} non-empty subsets",
            {"n": n, "k": k, "result": result, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return DP computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        # Show only last few steps to stay under 512 chars
        return sd["steps_log"][-6:]

    def _create_answer(self, sd: dict) -> str:
        """Return S(n, k).

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"S({sd['n']},{sd['k']}) = {sd['result']}"


# ---------------------------------------------------------------------------
# 4. Bell number (tier 5)
# ---------------------------------------------------------------------------


@register
class BellNumberGenerator(StepGenerator):
    """Compute the Bell number B_n = sum S(n, k) for k=0..n.

    Total number of partitions of a set of n elements.

    Difficulty scaling:
        d1-4: n in 3..5.
        d5-8: n in 5..7.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bell_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute Bell number"

    def _stirling(self, n: int, k: int) -> int:
        """Compute S(n, k) via DP.

        Args:
            n: Number of elements.
            k: Number of non-empty subsets.

        Returns:
            Stirling number of the second kind.
        """
        if n == 0 and k == 0:
            return 1
        if n == 0 or k == 0 or k > n:
            return 0
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
        return dp[n][k]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bell number computation problem.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(3, 5)
        else:
            n = self._rng.randint(5, 7)

        stirling_vals = []
        for k in range(n + 1):
            s = self._stirling(n, k)
            stirling_vals.append(s)

        bell = sum(stirling_vals)

        return (
            f"B_{n}: total partitions of {n} elements",
            {"n": n, "stirling_vals": stirling_vals, "bell": bell},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return summation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        terms = [f"S({sd['n']},{k})={sd['stirling_vals'][k]}"
                 for k in range(sd["n"] + 1) if sd["stirling_vals"][k] > 0]
        return [
            f"B_{sd['n']} = sum S({sd['n']},k) for k=0..{sd['n']}",
            ", ".join(terms),
            f"sum = {sd['bell']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Bell number.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"B_{sd['n']} = {sd['bell']}"


# ---------------------------------------------------------------------------
# 5. Twelvefold way (tier 5)
# ---------------------------------------------------------------------------


@register
class TwelvefoldWayGenerator(StepGenerator):
    """Classify a counting problem in the twelvefold way framework.

    Balls (distinguishable/identical) into boxes (distinguishable/identical)
    with constraints (any/injective/surjective). Template-based.

    Difficulty scaling:
        d1-4: 6 simpler cases.
        d5-8: all 12 cases.

    Prerequisites:
        binomial.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "twelvefold_way"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "classify twelvefold way problem"

    def _comb(self, n: int, k: int) -> int:
        """Compute C(n, k).

        Args:
            n: Total items.
            k: Items to choose.

        Returns:
            Binomial coefficient.
        """
        if k < 0 or k > n:
            return 0
        return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

    def _perm(self, n: int, k: int) -> int:
        """Compute P(n, k) = n!/(n-k)!.

        Args:
            n: Total items.
            k: Items to arrange.

        Returns:
            Permutation count.
        """
        if k > n:
            return 0
        return math.factorial(n) // math.factorial(n - k)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a twelvefold way classification problem.

        Args:
            difficulty: Controls which cases are included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(3, 6)
        k = self._rng.randint(2, min(5, n + 1))

        cases = [
            ("dist", "dist", "any", f"k^n = {k}^{n} = {k ** n}", k ** n),
            ("dist", "dist", "injective", f"P({k},{n}) = {self._perm(k, n)}", self._perm(k, n)),
            ("dist", "dist", "surjective", f"k!*S(n,k)", None),
            ("ident", "dist", "any", f"C(n+k-1,k-1) = C({n+k-1},{k-1}) = {self._comb(n + k - 1, k - 1)}", self._comb(n + k - 1, k - 1)),
            ("ident", "dist", "injective", f"C({k},{n}) = {self._comb(k, n)}", self._comb(k, n)),
            ("dist", "ident", "any", "sum of S(n,j) for j=1..k", None),
        ]

        if difficulty >= 5:
            cases.extend([
                ("ident", "dist", "surjective", f"C(n-1,k-1) = C({n-1},{k-1}) = {self._comb(n - 1, k - 1)}", self._comb(n - 1, k - 1)),
                ("ident", "ident", "any", f"p({n},{k}) partitions", None),
                ("dist", "ident", "injective", "1 if n<=k else 0", 1 if n <= k else 0),
                ("dist", "ident", "surjective", "S(n,k)", None),
                ("ident", "ident", "injective", "1 if n<=k else 0", 1 if n <= k else 0),
                ("ident", "ident", "surjective", "1 if n>=k else 0", 1 if n >= k else 0),
            ])

        chosen = self._rng.choice(cases)
        balls, boxes, constraint, formula, value = chosen
        value_str = str(value) if value is not None else formula

        return (
            f"{n} {balls} balls into {k} {boxes} boxes, constraint={constraint}",
            {
                "n": n, "k": k, "balls": balls, "boxes": boxes,
                "constraint": constraint, "formula": formula,
                "value": value_str,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return classification steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return [
            f"balls: {sd['balls']}, boxes: {sd['boxes']}",
            f"constraint: {sd['constraint']}",
            f"formula: {sd['formula']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the formula and count.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return sd["value"]


# ---------------------------------------------------------------------------
# 6. Principle of inclusion-exclusion (tier 4)
# ---------------------------------------------------------------------------


@register
class PrincipleInclusionExclusionGenerator(StepGenerator):
    """Compute |A1 U A2 U A3| via inclusion-exclusion for 2-3 sets.

    Difficulty scaling:
        d1-4: 2 sets.
        d5-8: 3 sets.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "principle_inclusion_exclusion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "inclusion-exclusion principle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inclusion-exclusion problem.

        Args:
            difficulty: Controls number of sets.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            # 2 sets
            a = self._rng.randint(10, 40)
            b = self._rng.randint(10, 40)
            ab = self._rng.randint(1, min(a, b))
            union_val = a + b - ab
            steps = [
                f"|A|={a}, |B|={b}, |A∩B|={ab}",
                f"|A∪B| = {a} + {b} - {ab} = {union_val}",
            ]
            return (
                f"|A|={a}, |B|={b}, |A∩B|={ab}. Find |A∪B|.",
                {"union": union_val, "steps": steps},
            )
        else:
            # 3 sets
            a = self._rng.randint(10, 30)
            b = self._rng.randint(10, 30)
            c = self._rng.randint(10, 30)
            ab = self._rng.randint(1, min(a, b) // 2 + 1)
            ac = self._rng.randint(1, min(a, c) // 2 + 1)
            bc = self._rng.randint(1, min(b, c) // 2 + 1)
            abc = self._rng.randint(0, min(ab, ac, bc))
            union_val = a + b + c - ab - ac - bc + abc
            steps = [
                f"|A|={a}, |B|={b}, |C|={c}",
                f"|A∩B|={ab}, |A∩C|={ac}, |B∩C|={bc}, |A∩B∩C|={abc}",
                f"|A∪B∪C| = {a}+{b}+{c} - {ab}-{ac}-{bc} + {abc} = {union_val}",
            ]
            return (
                f"|A|={a}, |B|={b}, |C|={c}, |A∩B|={ab}, |A∩C|={ac}, "
                f"|B∩C|={bc}, |A∩B∩C|={abc}. Find |A∪B∪C|.",
                {"union": union_val, "steps": steps},
            )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return inclusion-exclusion steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the union cardinality.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return str(sd["union"])


# ---------------------------------------------------------------------------
# 7. Latin square (tier 5)
# ---------------------------------------------------------------------------


@register
class LatinSquareGenerator(StepGenerator):
    """Verify or complete a Latin square for n=3 or n=4.

    An n x n grid with n symbols, each appearing once per row and column.

    Difficulty scaling:
        d1-4: n=3, verify or complete with 1-2 blanks.
        d5-8: n=4, verify or complete with 2-3 blanks.

    Prerequisites:
        permutation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "latin_square"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["permutation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "complete or verify Latin square"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Latin square problem.

        Args:
            difficulty: Controls grid size and number of blanks.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3 if difficulty <= 4 else 4
        n_blanks = self._rng.randint(1, 2) if n == 3 else self._rng.randint(2, 3)

        # Generate a valid Latin square by permutation
        symbols = list(range(1, n + 1))
        grid = []
        for i in range(n):
            row = symbols[i:] + symbols[:i]
            grid.append(row)
        # Shuffle columns
        col_perm = list(range(n))
        self._rng.shuffle(col_perm)
        grid = [[row[col_perm[j]] for j in range(n)] for row in grid]

        full_grid = [row[:] for row in grid]

        # Create blanks
        positions = [(r, c) for r in range(n) for c in range(n)]
        blank_positions = self._rng.sample(positions, n_blanks)
        for r, c in blank_positions:
            grid[r][c] = 0

        grid_str = "; ".join(
            "[" + ", ".join("?" if x == 0 else str(x) for x in row) + "]"
            for row in grid
        )

        steps = [f"grid: {grid_str}"]
        for r, c in blank_positions:
            row_vals = {grid[r][j] for j in range(n) if grid[r][j] != 0}
            col_vals = {grid[i][c] for i in range(n) if grid[i][c] != 0}
            missing = set(symbols) - row_vals - col_vals
            val = full_grid[r][c]
            steps.append(
                f"({r},{c}): row has {row_vals}, col has {col_vals}, fill {val}"
            )

        full_str = "; ".join(
            "[" + ", ".join(str(x) for x in row) + "]"
            for row in full_grid
        )

        return (
            f"Complete {n}x{n} Latin square: {grid_str}",
            {"grid": full_grid, "steps": steps, "full_str": full_str, "n": n},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return completion steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the completed Latin square.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return sd["full_str"]


# ---------------------------------------------------------------------------
# 8. Ballot problem (tier 5)
# ---------------------------------------------------------------------------


@register
class BallotProblemGenerator(StepGenerator):
    """Compute P(A always ahead) = (a - b) / (a + b) where a > b.

    Verify with small cases when feasible.

    Difficulty scaling:
        d1-4: a,b small (a in 3..6, b in 1..a-1).
        d5-8: a,b larger (a in 6..12, b in 1..a-1).

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ballot_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "ballot problem probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ballot problem.

        Args:
            difficulty: Controls vote count ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            a = self._rng.randint(3, 6)
        else:
            a = self._rng.randint(6, 12)
        b = self._rng.randint(1, a - 1)

        prob = round((a - b) / (a + b), 4)
        total = a + b

        steps = [
            f"A gets {a} votes, B gets {b} votes",
            f"P(A always ahead) = (a-b)/(a+b)",
            f"= ({a}-{b})/({a}+{b}) = {a - b}/{total}",
            f"= {prob}",
        ]

        return (
            f"Ballot: A={a} votes, B={b} votes. P(A always strictly ahead)?",
            {"a": a, "b": b, "prob": prob, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the probability.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"P = {sd['prob']}"
