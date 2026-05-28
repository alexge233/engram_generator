"""Measurement and unit conversion generators.

6 generators across tiers 0-1.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class UnitConversionLengthGenerator(StepGenerator):
    """Convert between length units."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "unit_conversion_length"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "convert length units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        conversions = [
            ("m", "cm", 100), ("km", "m", 1000), ("cm", "mm", 10),
            ("m", "km", 0.001), ("inch", "cm", 2.54), ("foot", "m", 0.3048),
            ("mile", "km", 1.609),
        ]
        src, dst, factor = self._rng.choice(conversions[:min(len(conversions), 3 + difficulty)])
        val = self._rng.randint(1, 10 ** min(difficulty + 1, 4))
        result = round(val * factor, 4)
        return f"{val} {src} to {dst}", {"val": val, "src": src, "dst": dst, "factor": factor, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"1 {sd['src']} = {sd['factor']} {sd['dst']}", f"{sd['val']} * {sd['factor']}"]

    def _create_answer(self, sd: dict) -> str:
        r = sd["result"]
        return str(int(r)) if r == int(r) else f"{r}"


@register
class UnitConversionMassGenerator(StepGenerator):
    """Convert between mass units."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "unit_conversion_mass"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "convert mass units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        conversions = [
            ("kg", "g", 1000), ("g", "mg", 1000), ("kg", "mg", 1000000),
            ("lb", "kg", 0.4536), ("oz", "g", 28.35),
        ]
        src, dst, factor = self._rng.choice(conversions[:min(len(conversions), 3 + difficulty)])
        val = self._rng.randint(1, 10 ** min(difficulty, 3))
        result = round(val * factor, 4)
        return f"{val} {src} to {dst}", {"val": val, "src": src, "dst": dst, "factor": factor, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"1 {sd['src']} = {sd['factor']} {sd['dst']}"]

    def _create_answer(self, sd: dict) -> str:
        r = sd["result"]
        return str(int(r)) if r == int(r) else f"{r}"


@register
class UnitConversionTempGenerator(StepGenerator):
    """Convert between temperature units."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "unit_conversion_temp"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "convert temperature"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["C_to_F", "F_to_C", "C_to_K"])
        c = self._rng.randint(-40, 100 * difficulty)
        if mode == "C_to_F":
            result = round(c * 9 / 5 + 32, 2)
            return f"{c}°C to °F", {"val": c, "result": result, "mode": mode}
        elif mode == "F_to_C":
            f = c * 9 // 5 + 32
            result = round((f - 32) * 5 / 9, 2)
            return f"{f}°F to °C", {"val": f, "result": result, "mode": mode}
        else:
            result = round(c + 273.15, 2)
            return f"{c}°C to K", {"val": c, "result": result, "mode": mode}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "C_to_F":
            return [f"F = C * 9/5 + 32"]
        elif sd["mode"] == "F_to_C":
            return [f"C = (F - 32) * 5/9"]
        return [f"K = C + 273.15"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['result']}"


@register
class TimeArithmeticGenerator(StepGenerator):
    """Add or subtract times with hour/minute carrying."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "time_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "add/subtract times"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        h1 = self._rng.randint(0, 23)
        m1 = self._rng.randint(0, 59)
        h2 = self._rng.randint(0, min(12, 4 * difficulty))
        m2 = self._rng.randint(0, 59)
        total_min = (h1 * 60 + m1) + (h2 * 60 + m2)
        rh = (total_min // 60) % 24
        rm = total_min % 60
        return (
            f"{h1:02d}:{m1:02d} + {h2}h {m2}m",
            {"h1": h1, "m1": m1, "h2": h2, "m2": m2, "rh": rh, "rm": rm},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        total_m = sd["m1"] + sd["m2"]
        carry = total_m // 60
        return [
            f"minutes: {sd['m1']} + {sd['m2']} = {total_m}" + (f" (carry {carry}h)" if carry else ""),
            f"hours: {sd['h1']} + {sd['h2']} + {carry} = {sd['rh']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['rh']:02d}:{sd['rm']:02d}"


@register
class SignificantFiguresGenerator(StepGenerator):
    """Count significant figures in a number."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "significant_figures"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count significant figures"

    _PATTERNS: list[str] = [
        "integer", "decimal", "leading_zeros", "trailing_decimal",
        "scientific", "trailing_zeros_decimal",
    ]

    def _gen_random_digits(self, count: int, first_nonzero: bool = True) -> str:
        """Generate a string of random digits.

        Args:
            count: Number of digits to generate.
            first_nonzero: If True, first digit is 1-9.

        Returns:
            String of random digits.
        """
        return "".join(
            str(self._rng.randint(1, 9)) if (i == 0 and first_nonzero)
            else str(self._rng.randint(0, 9))
            for i in range(count)
        )

    def _sigfig_integer(self, difficulty: int) -> tuple[str, int]:
        """Generate an integer pattern for significant figures.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        sig = self._rng.randint(1, min(3 + difficulty, 6))
        trailing = self._rng.randint(0, 3)
        return self._gen_random_digits(sig) + "0" * trailing, sig

    def _sigfig_decimal(self, difficulty: int) -> tuple[str, int]:
        """Generate a decimal pattern for significant figures.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        sig = self._rng.randint(2, min(3 + difficulty, 7))
        return f"{self._rng.randint(1, 9)}.{self._gen_random_digits(sig - 1, False)}", sig

    def _sigfig_leading_zeros(self, difficulty: int) -> tuple[str, int]:
        """Generate a leading-zeros decimal pattern.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        leading = self._rng.randint(1, 4)
        sig = self._rng.randint(1, min(2 + difficulty, 4))
        return "0." + "0" * leading + self._gen_random_digits(sig), sig

    def _sigfig_trailing_decimal(self, difficulty: int) -> tuple[str, int]:
        """Generate a trailing-decimal-point pattern.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        sig = self._rng.randint(1, min(2 + difficulty, 4))
        return self._gen_random_digits(sig) + ".", sig

    def _sigfig_trailing_zeros_decimal(self, difficulty: int) -> tuple[str, int]:
        """Generate a trailing-zeros-after-decimal pattern.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        int_part = str(self._rng.randint(1, 9))
        trailing = self._rng.randint(1, 3)
        mid = self._gen_random_digits(self._rng.randint(0, 2), first_nonzero=False)
        return f"{int_part}.{mid}" + "0" * trailing, 1 + len(mid) + trailing

    def _sigfig_scientific(self, difficulty: int) -> tuple[str, int]:
        """Generate a scientific notation pattern.

        Args:
            difficulty: Controls digit count range.

        Returns:
            Tuple of (number_string, sig_fig_count).
        """
        sig = self._rng.randint(2, min(3 + difficulty, 5))
        coeff_dec = self._gen_random_digits(sig - 1, first_nonzero=False)
        exp = self._rng.randint(-4, 6)
        return f"{self._rng.randint(1, 9)}.{coeff_dec}e{exp}", sig

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a significant figures counting problem.

        Args:
            difficulty: Controls the complexity of the number format.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        pattern = self._rng.choice(self._PATTERNS)
        builders = {
            "integer": self._sigfig_integer,
            "decimal": self._sigfig_decimal,
            "leading_zeros": self._sigfig_leading_zeros,
            "trailing_decimal": self._sigfig_trailing_decimal,
            "trailing_zeros_decimal": self._sigfig_trailing_zeros_decimal,
            "scientific": self._sigfig_scientific,
        }
        num_str, sig_figs = builders[pattern](difficulty)
        return f"sig figs in {num_str}", {"num": num_str, "sig_figs": sig_figs}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"apply sig fig rules to {sd['num']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["sig_figs"])


@register
class ScientificNotationGenerator(StepGenerator):
    """Convert to/from scientific notation."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "scientific_notation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "convert scientific notation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["to_sci", "from_sci"])
        coeff = round(self._rng.uniform(1.0, 9.99), min(difficulty, 3))
        exp = self._rng.randint(-difficulty - 2, difficulty + 2)
        value = coeff * 10 ** exp

        if mode == "to_sci":
            if exp >= 0:
                val_str = str(int(value)) if value == int(value) else f"{value:.4f}"
            else:
                val_str = f"{value:.{abs(exp) + 2}f}"
            return f"{val_str} to scientific notation", {"coeff": coeff, "exp": exp, "mode": mode}
        else:
            return f"{coeff} × 10^{exp} to standard", {"coeff": coeff, "exp": exp, "value": value, "mode": mode}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"coefficient: {sd['coeff']}", f"exponent: {sd['exp']}"]

    def _create_answer(self, sd: dict) -> str:
        if sd["mode"] == "to_sci":
            return f"{sd['coeff']} × 10^{sd['exp']}"
        v = sd["value"]
        return str(int(v)) if v == int(v) else f"{v}"
