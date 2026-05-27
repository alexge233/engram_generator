"""Trigonometry, measurement/units, sequences, and combinatorics generators.

Adds 33 generators across tiers 0-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# TRIGONOMETRY (6 generators, tiers 1-3)
# ═══════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════
# MEASUREMENT / UNITS (6 generators, tiers 0-1)
# ═══════════════════════════════════════════════════════════════════

@register
class UnitConversionLengthGenerator(StepGenerator):
    """Convert between length units."""

    @property
    def task_name(self) -> str:
        return "unit_conversion_length"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
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
        return "unit_conversion_mass"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
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
        return "unit_conversion_temp"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
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
        return "time_arithmetic"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
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
        return "significant_figures"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        return "count significant figures"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cases = [
            ("123", 3), ("1200", 2), ("0.0045", 2), ("10.0", 3),
            ("5.00", 3), ("0.020", 2), ("3.14159", 6), ("100.", 3),
            ("0.001", 1), ("2.0e3", 2), ("45000", 2), ("1.050", 4),
        ]
        num_str, sig_figs = self._rng.choice(cases[:min(len(cases), 4 + difficulty)])
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
        return "scientific_notation"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
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


# ═══════════════════════════════════════════════════════════════════
# SEQUENCES & SERIES (5 generators, tiers 1-3)
# ═══════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════
# COMBINATORICS (5 generators, tiers 2-3)
# ═══════════════════════════════════════════════════════════════════

@register
class CombinationCountGenerator(StepGenerator):
    """Compute C(n, k)."""

    @property
    def task_name(self) -> str:
        return "combination_count"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
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
        return "permutation_with_rep"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
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
        return "pigeonhole"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["division"]

    def task_description(self, difficulty: int) -> str:
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
        return "inclusion_exclusion"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["combination_count", "venn_diagram_count"]

    def task_description(self, difficulty: int) -> str:
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
        return "stars_and_bars"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["combination_count"]

    def task_description(self, difficulty: int) -> str:
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
