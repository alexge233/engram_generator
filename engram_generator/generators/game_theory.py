"""Game theory generators.

4 generators across tiers 3-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class PayoffMatrixGenerator(StepGenerator):
    """Read payoffs from a game matrix."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "payoff_matrix"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "read payoff matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        matrix = [[
            (self._rng.randint(-5, 10), self._rng.randint(-5, 10))
            for _ in range(n)
        ] for _ in range(n)]
        r = self._rng.randint(0, n - 1)
        c = self._rng.randint(0, n - 1)
        payoff = matrix[r][c]
        mat_str = "; ".join(
            "[" + ", ".join(f"({a},{b})" for a, b in row) + "]"
            for row in matrix
        )
        return (
            f"matrix: {mat_str}. Payoff at row {r}, col {c}?",
            {"matrix": matrix, "r": r, "c": c, "payoff": payoff},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"row {sd['r']}, col {sd['c']}: {sd['payoff']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"({sd['payoff'][0]},{sd['payoff'][1]})"


@register
class DominantStrategyGenerator(StepGenerator):
    """Find dominant strategies in a 2x2 game."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dominant_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["payoff_matrix"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find dominant strategy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m = [[(self._rng.randint(0, 10), self._rng.randint(0, 10)) for _ in range(2)] for _ in range(2)]
        row_dom = None
        if m[0][0][0] >= m[1][0][0] and m[0][1][0] >= m[1][1][0]:
            if m[0][0][0] > m[1][0][0] or m[0][1][0] > m[1][1][0]:
                row_dom = "row 0"
        if m[1][0][0] >= m[0][0][0] and m[1][1][0] >= m[0][1][0]:
            if m[1][0][0] > m[0][0][0] or m[1][1][0] > m[0][1][0]:
                row_dom = "row 1"
        mat_str = f"[({m[0][0][0]},{m[0][0][1]}),({m[0][1][0]},{m[0][1][1]})];" \
                  f"[({m[1][0][0]},{m[1][0][1]}),({m[1][1][0]},{m[1][1][1]})]"
        return (
            f"row player dominant? matrix: {mat_str}",
            {"matrix": m, "row_dominant": row_dom},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        m = sd["matrix"]
        return [
            f"row 0 payoffs: {m[0][0][0]},{m[0][1][0]}",
            f"row 1 payoffs: {m[1][0][0]},{m[1][1][0]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["row_dominant"] if sd["row_dominant"] else "none"


@register
class NashEquilibriumGenerator(StepGenerator):
    """Find Nash equilibria in a 2x2 game."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nash_equilibrium"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dominant_strategy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find Nash equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m = [[(self._rng.randint(0, 10), self._rng.randint(0, 10)) for _ in range(2)] for _ in range(2)]
        ne = []
        for r in range(2):
            for c in range(2):
                row_best = m[r][c][0] >= m[1 - r][c][0]
                col_best = m[r][c][1] >= m[r][1 - c][1]
                if row_best and col_best:
                    ne.append((r, c))
        mat_str = f"[({m[0][0][0]},{m[0][0][1]}),({m[0][1][0]},{m[0][1][1]})];" \
                  f"[({m[1][0][0]},{m[1][0][1]}),({m[1][1][0]},{m[1][1][1]})]"
        return mat_str, {"matrix": m, "ne": ne}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for r in range(2):
            for c in range(2):
                steps.append(f"({r},{c}): check best responses")
        return steps

    def _create_answer(self, sd: dict) -> str:
        if not sd["ne"]:
            return "no pure NE"
        return ", ".join(f"({r},{c})" for r, c in sd["ne"])


@register
class MinimaxGenerator(StepGenerator):
    """Find the minimax value of a zero-sum game."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "minimax"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["payoff_matrix"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find minimax value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        matrix = [[self._rng.randint(-5, 10) for _ in range(n)] for _ in range(n)]
        row_mins = [min(row) for row in matrix]
        maximin = max(row_mins)
        col_maxs = [max(matrix[r][c] for r in range(n)) for c in range(n)]
        minimax = min(col_maxs)
        mat_str = "; ".join("[" + ",".join(str(v) for v in row) + "]" for row in matrix)
        return (
            f"zero-sum: {mat_str}",
            {"matrix": matrix, "maximin": maximin, "minimax": minimax},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"row mins: {[min(row) for row in sd['matrix']]}",
            f"maximin = {sd['maximin']}",
            f"col maxs: {[max(sd['matrix'][r][c] for r in range(len(sd['matrix']))) for c in range(len(sd['matrix'][0]))]}",
            f"minimax = {sd['minimax']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"maximin={sd['maximin']}, minimax={sd['minimax']}"
