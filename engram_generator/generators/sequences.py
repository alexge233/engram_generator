"""Sequences and series generators.

5 generators across tiers 1-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class ArithmeticSequenceGenerator(StepGenerator):
    """Find the nth term or sum of an arithmetic sequence."""

    @property
    def task_name(self) -> str:
        return "arithmetic_sequence"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["addition", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "arithmetic sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a1 = self._rng.randint(1, 10 * difficulty)
        d = self._rng.randint(1, 5 * difficulty)
        n = self._rng.randint(5, 10 + 5 * difficulty)
        an = a1 + (n - 1) * d
        s = n * (a1 + an) // 2
        mode = self._rng.choice(["nth", "sum"])
        if mode == "nth":
            return f"a1={a1}, d={d}, find a_{n}", {"a1": a1, "d": d, "n": n, "an": an, "mode": "nth"}
        return f"a1={a1}, d={d}, sum of {n} terms", {"a1": a1, "d": d, "n": n, "an": an, "s": s, "mode": "sum"}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "nth":
            return [f"a_n = a1 + (n-1)*d", f"a_{sd['n']} = {sd['a1']} + {sd['n']-1}*{sd['d']}"]
        return [f"a_n = {sd['an']}", f"S = n*(a1+an)/2 = {sd['n']}*({sd['a1']}+{sd['an']})/2"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["an"] if sd["mode"] == "nth" else sd["s"])


@register
class GeometricSequenceGenerator(StepGenerator):
    """Find the nth term or sum of a geometric sequence."""

    @property
    def task_name(self) -> str:
        return "geometric_sequence"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        return "geometric sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a1 = self._rng.randint(1, 5)
        r = self._rng.randint(2, min(4, 2 + difficulty))
        n = self._rng.randint(3, min(8, 3 + difficulty))
        an = a1 * r ** (n - 1)
        s = a1 * (r ** n - 1) // (r - 1)
        mode = self._rng.choice(["nth", "sum"])
        if mode == "nth":
            return f"a1={a1}, r={r}, find a_{n}", {"a1": a1, "r": r, "n": n, "an": an, "mode": "nth"}
        return f"a1={a1}, r={r}, sum of {n} terms", {"a1": a1, "r": r, "n": n, "an": an, "s": s, "mode": "sum"}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "nth":
            return [f"a_n = a1 * r^(n-1) = {sd['a1']} * {sd['r']}^{sd['n']-1}"]
        return [f"S = a1*(r^n - 1)/(r - 1)"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["an"] if sd["mode"] == "nth" else sd["s"])


@register
class SequenceSumGenerator(StepGenerator):
    """Compute closed-form sums (natural numbers, squares, cubes)."""

    @property
    def task_name(self) -> str:
        return "sequence_sum"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["arithmetic_sequence"]

    def task_description(self, difficulty: int) -> str:
        return "compute sequence sum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(5, 10 + 10 * difficulty)
        mode = self._rng.choice(["natural", "squares", "cubes"])
        if mode == "natural":
            s = n * (n + 1) // 2
            formula = "n*(n+1)/2"
        elif mode == "squares":
            s = n * (n + 1) * (2 * n + 1) // 6
            formula = "n*(n+1)*(2n+1)/6"
        else:
            s = (n * (n + 1) // 2) ** 2
            formula = "[n*(n+1)/2]^2"
        return f"sum of {mode} 1..{n}", {"n": n, "mode": mode, "sum": s, "formula": formula}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"formula: {sd['formula']}", f"n = {sd['n']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["sum"])


@register
class ConvergentSeriesGenerator(StepGenerator):
    """Determine if an infinite series converges and find its sum."""

    @property
    def task_name(self) -> str:
        return "convergent_series"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["geometric_sequence"]

    def task_description(self, difficulty: int) -> str:
        return "analyse series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(1, 5 * difficulty)
        r_choices = [0.5, 0.25, 1.0 / 3, 0.75, 0.1, 2.0, 3.0]
        r = self._rng.choice(r_choices[:min(len(r_choices), 3 + difficulty)])
        converges = abs(r) < 1
        s = round(a / (1 - r), 4) if converges else None
        return (
            f"sum of {a} * {r}^n for n=0 to infinity",
            {"a": a, "r": r, "converges": converges, "sum": s},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"|r| = {abs(sd['r'])}"]
        if sd["converges"]:
            steps.append(f"|r| < 1, converges")
            steps.append(f"S = a/(1-r) = {sd['a']}/(1-{sd['r']})")
        else:
            steps.append(f"|r| >= 1, diverges")
        return steps

    def _create_answer(self, sd: dict) -> str:
        if sd["converges"]:
            return f"{sd['sum']}"
        return "diverges"


@register
class RecurrenceLinearGenerator(StepGenerator):
    """Solve a simple linear recurrence by unrolling."""

    @property
    def task_name(self) -> str:
        return "recurrence_linear"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["arithmetic_sequence"]

    def task_description(self, difficulty: int) -> str:
        return "solve linear recurrence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a0 = self._rng.randint(1, 10)
        c = self._rng.randint(1, 5)
        d = self._rng.randint(0, 10)
        n = self._rng.randint(3, min(8, 3 + difficulty))
        vals = [a0]
        for _ in range(n):
            vals.append(c * vals[-1] + d)
        return (
            f"a(0)={a0}, a(n) = {c}*a(n-1) + {d}, find a({n})",
            {"a0": a0, "c": c, "d": d, "n": n, "vals": vals},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"a({i}) = {sd['vals'][i]}" for i in range(len(sd["vals"]))]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["vals"][-1])
