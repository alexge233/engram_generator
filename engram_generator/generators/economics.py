"""Economics and finance generators.

6 generators across tiers 1-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class FinanceGenerator(StepGenerator):
    """Base class for finance generators with shared formatting."""

    def _fmt_money(self, value: float) -> str:
        """Format a monetary value.

        Args:
            value: Numeric amount.

        Returns:
            Formatted string.
        """
        return str(int(value)) if value == int(value) else f"{value:.2f}"


@register
class SimpleInterestGenerator(FinanceGenerator):
    """Calculate simple interest."""

    @property
    def task_name(self) -> str:
        return "simple_interest"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "calculate simple interest"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.randint(100, 1000 * difficulty) * 10
        r = round(self._rng.uniform(0.01, 0.15), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        interest = round(p * r * t, 2)
        total = round(p + interest, 2)
        return (
            f"P={p}, r={r*100}%, t={t} years",
            {"P": p, "r": r, "t": t, "interest": interest, "total": total},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"I = P*r*t = {sd['P']}*{sd['r']}*{sd['t']}", "A = P + I"]

    def _create_answer(self, sd: dict) -> str:
        return f"I={sd['interest']}, A={sd['total']}"


@register
class CompoundInterestGenerator(FinanceGenerator):
    """Calculate compound interest."""

    @property
    def task_name(self) -> str:
        return "compound_interest"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["simple_interest", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        return "calculate compound interest"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.randint(100, 500 * difficulty) * 10
        r = round(self._rng.uniform(0.02, 0.12), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        n = self._rng.choice([1, 4, 12])
        a = round(p * (1 + r / n) ** (n * t), 2)
        return (
            f"P={p}, r={r*100}%, t={t}y, n={n}/year",
            {"P": p, "r": r, "t": t, "n": n, "A": a},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"A = P(1 + r/n)^(nt)", f"A = {sd['P']}(1 + {sd['r']}/{sd['n']})^({sd['n']}*{sd['t']})"]

    def _create_answer(self, sd: dict) -> str:
        return self._fmt_money(sd["A"])


@register
class ROIGenerator(FinanceGenerator):
    """Calculate return on investment."""

    @property
    def task_name(self) -> str:
        return "roi"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate ROI"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cost = self._rng.randint(100, 500 * difficulty) * 10
        gain = round(cost * (1 + self._rng.uniform(-0.3, 0.8)))
        roi = round((gain - cost) / cost * 100, 2)
        return f"cost={cost}, return={gain}", {"cost": cost, "gain": gain, "roi": roi}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"ROI = (gain - cost) / cost * 100"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['roi']}%"


@register
class BreakEvenGenerator(FinanceGenerator):
    """Calculate break-even point."""

    @property
    def task_name(self) -> str:
        return "break_even"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        return "find break-even point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fixed = self._rng.randint(1000, 10000 * difficulty)
        price = self._rng.randint(20, 100 * difficulty)
        variable = self._rng.randint(5, price - 1)
        units = math.ceil(fixed / (price - variable))
        return (
            f"fixed={fixed}, price={price}, variable_cost={variable}",
            {"fixed": fixed, "price": price, "variable": variable, "units": units},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        margin = sd["price"] - sd["variable"]
        return [f"margin = {margin}", f"units = {sd['fixed']} / {margin}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['units']} units"


@register
class DepreciationGenerator(FinanceGenerator):
    """Calculate straight-line depreciation."""

    @property
    def task_name(self) -> str:
        return "depreciation"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate depreciation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cost = self._rng.randint(1000, 10000 * difficulty)
        salvage = self._rng.randint(0, cost // 3)
        life = self._rng.randint(3, min(15, 3 + difficulty))
        annual = round((cost - salvage) / life, 2)
        year = self._rng.randint(1, life)
        book_value = round(cost - annual * year, 2)
        return (
            f"cost={cost}, salvage={salvage}, life={life}y, year {year}",
            {"annual": annual, "year": year, "cost": cost, "book_value": book_value},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"annual = {sd['annual']}", f"value = {sd['cost']} - {sd['annual']}*{sd['year']}"]

    def _create_answer(self, sd: dict) -> str:
        return self._fmt_money(sd["book_value"])


@register
class PresentValueGenerator(FinanceGenerator):
    """Calculate present value of a future amount."""

    @property
    def task_name(self) -> str:
        return "present_value"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["compound_interest"]

    def task_description(self, difficulty: int) -> str:
        return "calculate present value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fv = self._rng.randint(1000, 10000 * difficulty)
        r = round(self._rng.uniform(0.03, 0.12), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        pv = round(fv / (1 + r) ** t, 2)
        return f"FV={fv}, r={r*100}%, t={t}y", {"pv": pv}

    def _create_steps(self, sd: dict) -> list[str]:
        return ["PV = FV / (1+r)^t"]

    def _create_answer(self, sd: dict) -> str:
        return self._fmt_money(sd["pv"])
