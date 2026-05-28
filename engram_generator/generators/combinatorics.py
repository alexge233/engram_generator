"""Combinatorics generators.

5 generators across tiers 2-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class CombinationCountGenerator(StepGenerator):
    """Compute C(n, k)."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "combination_count"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "compute C(n,k)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(3, min(15, 3 + 3 * difficulty))
        k = self._rng.randint(1, n)
        result = 1
        for i in range(min(k, n - k)):
            result = result * (n - i) // (i + 1)
        return f"C({n},{k})", {"n": n, "k": k, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"C({sd['n']},{sd['k']}) = {sd['n']}! / ({sd['k']}! * {sd['n']-sd['k']}!)"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class PermutationWithRepGenerator(StepGenerator):
    """Compute permutations with or without repetition."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "permutation_with_rep"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count permutations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["with_rep", "without_rep"])
        if mode == "with_rep":
            n = self._rng.randint(2, min(6, 2 + difficulty))
            k = self._rng.randint(2, min(5, 2 + difficulty))
            result = n ** k
            return f"{n}^{k} (with repetition)", {"n": n, "k": k, "result": result, "mode": mode}
        else:
            n = self._rng.randint(3, min(10, 3 + difficulty))
            k = self._rng.randint(2, n)
            result = 1
            for i in range(k):
                result *= (n - i)
            return f"P({n},{k})", {"n": n, "k": k, "result": result, "mode": mode}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "with_rep":
            return [f"n^k = {sd['n']}^{sd['k']}"]
        return [f"P(n,k) = n!/(n-k)! = {sd['n']}!/({sd['n']}-{sd['k']})!"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class PigeonholeGenerator(StepGenerator):
    """Apply the pigeonhole principle."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pigeonhole"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "apply pigeonhole principle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        containers = self._rng.randint(3, 5 + 3 * difficulty)
        items = containers + self._rng.randint(1, 3 * difficulty)
        import math as m
        min_in_one = m.ceil(items / containers)
        return (
            f"{items} items into {containers} containers. min in one?",
            {"items": items, "containers": containers, "min": min_in_one},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"pigeonhole: ceil({sd['items']} / {sd['containers']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["min"])


@register
class InclusionExclusionGenerator(StepGenerator):
    """Count using inclusion-exclusion with overlapping properties."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inclusion_exclusion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["combination_count", "venn_diagram_count"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count by inclusion-exclusion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(20, 50 * difficulty)
        a = self._rng.randint(n // 4, n // 2)
        b = self._rng.randint(n // 4, n // 2)
        ab = self._rng.randint(0, min(a, b) // 2)
        neither = n - (a + b - ab)
        return (
            f"total={n}, A={a}, B={b}, A∩B={ab}. How many in neither?",
            {"n": n, "a": a, "b": b, "ab": ab, "neither": neither},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        union = sd["a"] + sd["b"] - sd["ab"]
        return [
            f"|A ∪ B| = {sd['a']} + {sd['b']} - {sd['ab']} = {union}",
            f"neither = {sd['n']} - {union}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["neither"])


@register
class StarsAndBarsGenerator(StepGenerator):
    """Count distributions using stars and bars."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stars_and_bars"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["combination_count"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count distributions (stars and bars)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(3, 5 + 3 * difficulty)
        k = self._rng.randint(2, min(5, 2 + difficulty))
        result = 1
        top = n + k - 1
        bot = k - 1
        for i in range(min(bot, top - bot)):
            result = result * (top - i) // (i + 1)
        return (
            f"distribute {n} identical items into {k} bins",
            {"n": n, "k": k, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"C(n+k-1, k-1) = C({sd['n']+sd['k']-1}, {sd['k']-1})"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])
