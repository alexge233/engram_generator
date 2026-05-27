"""Trigonometry generators.

6 generators across tiers 1-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class SinCosEvalGenerator(StepGenerator):
    """Evaluate sine or cosine at standard angles."""

    @property
    def task_name(self) -> str:
        return "sin_cos_eval"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate sin or cos"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
        angle = self._rng.choice(angles[:min(len(angles), 4 + difficulty)])
        fn = self._rng.choice(["sin", "cos"])
        rad = math.radians(angle)
        val = round(math.sin(rad) if fn == "sin" else math.cos(rad), 4)
        return f"{fn}({angle}°)", {"fn": fn, "angle": angle, "value": val}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"{sd['fn']}({sd['angle']}°) = {sd['value']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['value']}"


@register
class TanEvalGenerator(StepGenerator):
    """Evaluate tangent at standard angles."""

    @property
    def task_name(self) -> str:
        return "tan_eval"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate tan"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        angles = [0, 30, 45, 60, 120, 135, 150, 180]
        angle = self._rng.choice(angles[:min(len(angles), 3 + difficulty)])
        rad = math.radians(angle)
        val = round(math.tan(rad), 4) if abs(math.cos(rad)) > 1e-10 else "undefined"
        return f"tan({angle}°)", {"angle": angle, "value": val}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"tan = sin/cos", f"tan({sd['angle']}°) = {sd['value']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["value"])


@register
class AngleConversionGenerator(StepGenerator):
    """Convert between degrees and radians."""

    @property
    def task_name(self) -> str:
        return "angle_conversion"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        return "convert angle units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["deg_to_rad", "rad_to_deg"])
        if mode == "deg_to_rad":
            deg = self._rng.choice([30, 45, 60, 90, 120, 180, 270, 360])
            rad = round(deg * math.pi / 180, 4)
            return f"{deg}° to radians", {"deg": deg, "rad": rad, "mode": mode}
        else:
            fracs = [(1, 6), (1, 4), (1, 3), (1, 2), (2, 3), (1, 1), (3, 2), (2, 1)]
            num, den = self._rng.choice(fracs)
            rad = num * math.pi / den
            deg = round(rad * 180 / math.pi, 2)
            rad_str = f"{num}pi/{den}" if den > 1 else f"{num}pi"
            return f"{rad_str} to degrees", {"deg": deg, "rad": round(rad, 4), "mode": mode}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "deg_to_rad":
            return [f"{sd['deg']} * pi/180 = {sd['rad']}"]
        return [f"{sd['rad']} * 180/pi = {sd['deg']}"]

    def _create_answer(self, sd: dict) -> str:
        if sd["mode"] == "deg_to_rad":
            return f"{sd['rad']}"
        return f"{sd['deg']}"


@register
class LawOfSinesGenerator(StepGenerator):
    """Solve a triangle using the law of sines."""

    @property
    def task_name(self) -> str:
        return "law_of_sines"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sin_cos_eval", "angle_sum_triangle"]

    def task_description(self, difficulty: int) -> str:
        return "apply law of sines"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        A = self._rng.randint(30, 80)
        B = self._rng.randint(30, 150 - A)
        C = 180 - A - B
        a = self._rng.randint(3, 5 * difficulty)
        b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 2)
        return (
            f"triangle: A={A}°, B={B}°, a={a}. Find b",
            {"A": A, "B": B, "C": C, "a": a, "b": b},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"a/sin(A) = b/sin(B)",
            f"b = {sd['a']} * sin({sd['B']}°) / sin({sd['A']}°)",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['b']}"


@register
class LawOfCosinesGenerator(StepGenerator):
    """Find a side or angle using the law of cosines."""

    @property
    def task_name(self) -> str:
        return "law_of_cosines"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sin_cos_eval", "pythagorean"]

    def task_description(self, difficulty: int) -> str:
        return "apply law of cosines"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(3, 5 * difficulty)
        b = self._rng.randint(3, 5 * difficulty)
        C = self._rng.randint(30, 120)
        c2 = a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(C))
        c = round(math.sqrt(max(0, c2)), 2)
        return (
            f"triangle a={a}, b={b}, C={C}°. Find c",
            {"a": a, "b": b, "C": C, "c": c},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        a2 = sd["a"] ** 2
        b2 = sd["b"] ** 2
        cos_val = round(math.cos(math.radians(sd["C"])), 4)
        return [
            f"c^2 = a^2 + b^2 - 2ab*cos(C)",
            f"c^2 = {a2} + {b2} - 2*{sd['a']}*{sd['b']}*{cos_val}",
            f"c = {sd['c']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['c']}"


@register
class TrigIdentityGenerator(StepGenerator):
    """Verify or simplify a trigonometric identity."""

    @property
    def task_name(self) -> str:
        return "trig_identity"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["sin_cos_eval", "tan_eval"]

    def task_description(self, difficulty: int) -> str:
        return "verify trig identity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        angle = self._rng.randint(10, 80)
        rad = math.radians(angle)
        s, c = math.sin(rad), math.cos(rad)

        identities = [
            (f"sin^2({angle}°) + cos^2({angle}°)", round(s**2 + c**2, 4), "Pythagorean"),
            (f"sin(2*{angle}°) vs 2*sin({angle}°)*cos({angle}°)",
             round(math.sin(2 * rad) - 2 * s * c, 6), "double angle"),
            (f"tan({angle}°) vs sin({angle}°)/cos({angle}°)",
             round(math.tan(rad) - s / c, 6), "tan definition"),
        ]
        expr, diff, name = self._rng.choice(identities[:min(len(identities), difficulty + 1)])
        verified = abs(diff) < 1e-4
        return expr, {"name": name, "verified": verified, "diff": diff}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"identity: {sd['name']}", f"difference: {sd['diff']}"]

    def _create_answer(self, sd: dict) -> str:
        return "VERIFIED" if sd["verified"] else f"DIFFERS by {sd['diff']}"
