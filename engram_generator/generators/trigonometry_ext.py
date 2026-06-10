"""Extended trigonometry generators.

6 generators covering inverse trigonometric functions, hyperbolic
functions, trigonometric equations, double angle formulas, inverse
hyperbolic functions, and trigonometric substitution across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. INVERSE TRIG (tier 4)
# ===================================================================

@register
class InverseTrigGenerator(StepGenerator):
    """Compute arcsin, arccos, arctan for standard values.

    Evaluates inverse trigonometric functions at standard inputs
    (0, 1/2, sqrt(2)/2, sqrt(3)/2, 1) and returns results in radians
    as multiples of pi.

    Difficulty scaling:
        Difficulty 1-3: arcsin and arccos at 0, 1/2, 1.
        Difficulty 4-6: arctan, values including sqrt(2)/2, sqrt(3)/2.
        Difficulty 7-8: negative arguments, compositions.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    _ARCSIN_TABLE = [
        (0, 0.0, "0"),
        (0.5, round(math.pi / 6, 4), "pi/6"),
        (round(math.sqrt(2) / 2, 4), round(math.pi / 4, 4), "pi/4"),
        (round(math.sqrt(3) / 2, 4), round(math.pi / 3, 4), "pi/3"),
        (1, round(math.pi / 2, 4), "pi/2"),
    ]

    _ARCCOS_TABLE = [
        (1, 0.0, "0"),
        (round(math.sqrt(3) / 2, 4), round(math.pi / 6, 4), "pi/6"),
        (round(math.sqrt(2) / 2, 4), round(math.pi / 4, 4), "pi/4"),
        (0.5, round(math.pi / 3, 4), "pi/3"),
        (0, round(math.pi / 2, 4), "pi/2"),
    ]

    _ARCTAN_TABLE = [
        (0, 0.0, "0"),
        (round(1 / math.sqrt(3), 4), round(math.pi / 6, 4), "pi/6"),
        (1, round(math.pi / 4, 4), "pi/4"),
        (round(math.sqrt(3), 4), round(math.pi / 3, 4), "pi/3"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inverse_trig"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls function and argument variety.

        Returns:
            Task description string.
        """
        return "compute inverse trig function at standard value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inverse trig evaluation problem.

        Args:
            difficulty: Controls function and argument variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            fn = self._rng.choice(["arcsin", "arccos"])
            table = self._ARCSIN_TABLE if fn == "arcsin" else self._ARCCOS_TABLE
            arg, val, exact = self._rng.choice(table)
            negate = False
        elif difficulty <= 6:
            fn = self._rng.choice(["arcsin", "arccos", "arctan"])
            if fn == "arcsin":
                table = self._ARCSIN_TABLE
            elif fn == "arccos":
                table = self._ARCCOS_TABLE
            else:
                table = self._ARCTAN_TABLE
            arg, val, exact = self._rng.choice(table)
            negate = False
        else:
            fn = self._rng.choice(["arcsin", "arccos", "arctan"])
            if fn == "arcsin":
                table = self._ARCSIN_TABLE
            elif fn == "arccos":
                table = self._ARCCOS_TABLE
            else:
                table = self._ARCTAN_TABLE
            arg, val, exact = self._rng.choice(table)
            negate = self._rng.choice([True, False]) and arg != 0

        if negate:
            neg_arg = round(-arg, 4)
            if fn == "arcsin":
                neg_val = round(-val, 4)
                neg_exact = f"-{exact}"
            elif fn == "arccos":
                neg_val = round(math.pi - val, 4)
                neg_exact = f"pi - {exact}"
            else:
                neg_val = round(-val, 4)
                neg_exact = f"-{exact}"
            problem = f"{fn}({neg_arg})"
            return problem, {
                "fn": fn, "arg": neg_arg,
                "value": neg_val, "exact": neg_exact,
            }

        problem = f"{fn}({arg})"
        return problem, {
            "fn": fn, "arg": arg, "value": val, "exact": exact,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inverse trig computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the evaluation.
        """
        return [
            f"{data['fn']}({data['arg']})",
            f"= {data['exact']} rad",
            f"= {data['value']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Result in radians.
        """
        return f"{data['exact']} = {data['value']}"


# ===================================================================
# 2. HYPERBOLIC FUNCTIONS (tier 5)
# ===================================================================

@register
class HyperbolicFunctionsGenerator(StepGenerator):
    """Compute sinh, cosh, tanh for given x values.

    Uses definitions sinh(x) = (e^x - e^{-x})/2,
    cosh(x) = (e^x + e^{-x})/2, tanh(x) = sinh(x)/cosh(x).

    Difficulty scaling:
        Difficulty 1-3: x in {0, 1, -1}.
        Difficulty 4-6: x in {0.5, 1.5, 2, -2}.
        Difficulty 7-8: larger |x|, all three functions asked.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hyperbolic_functions"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls input range and function variety.

        Returns:
            Task description string.
        """
        return "compute hyperbolic function value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hyperbolic function evaluation problem.

        Args:
            difficulty: Controls input range and function variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            x = self._rng.choice([0, 1, -1])
            fn = self._rng.choice(["sinh", "cosh", "tanh"])
        elif difficulty <= 6:
            x = self._rng.choice([0.5, 1, 1.5, 2, -1, -2])
            fn = self._rng.choice(["sinh", "cosh", "tanh"])
        else:
            x = self._rng.choice([0.5, 1, 1.5, 2, 2.5, 3, -1, -2, -3])
            fn = self._rng.choice(["sinh", "cosh", "tanh"])

        ex = round(math.exp(x), 4)
        emx = round(math.exp(-x), 4)
        sinh_val = round((ex - emx) / 2, 4)
        cosh_val = round((ex + emx) / 2, 4)
        tanh_val = round(sinh_val / cosh_val, 4) if cosh_val != 0 else 0.0

        if fn == "sinh":
            result = sinh_val
            formula = f"(e^{x} - e^{-x})/2 = ({ex} - {emx})/2"
        elif fn == "cosh":
            result = cosh_val
            formula = f"(e^{x} + e^{-x})/2 = ({ex} + {emx})/2"
        else:
            result = tanh_val
            formula = f"sinh({x})/cosh({x}) = {sinh_val}/{cosh_val}"

        problem = f"{fn}({x})"
        return problem, {
            "fn": fn, "x": x, "result": result,
            "formula": formula, "ex": ex, "emx": emx,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate hyperbolic function steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        return [
            f"e^{data['x']} = {data['ex']}",
            f"e^{-data['x']} = {data['emx']}",
            data["formula"],
            f"{data['fn']}({data['x']}) = {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The computed value.
        """
        return str(data["result"])


# ===================================================================
# 3. TRIG EQUATION (tier 4)
# ===================================================================

@register
class TrigEquationGenerator(StepGenerator):
    """Solve sin(x) = a or cos(x) = a on [0, 2*pi].

    Lists all solutions of a basic trigonometric equation in the
    interval [0, 2*pi] using standard angle values.

    Difficulty scaling:
        Difficulty 1-3: sin(x) = 0, 1, -1 or cos(x) = 0, 1, -1.
        Difficulty 4-6: sin(x) or cos(x) = 1/2, sqrt(2)/2, sqrt(3)/2.
        Difficulty 7-8: negative fractional values, tan equations.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    _SIN_SOLUTIONS = [
        (0, ["0", "pi"], [0.0, round(math.pi, 4)]),
        (1, ["pi/2"], [round(math.pi / 2, 4)]),
        (-1, ["3pi/2"], [round(3 * math.pi / 2, 4)]),
        (0.5, ["pi/6", "5pi/6"],
         [round(math.pi / 6, 4), round(5 * math.pi / 6, 4)]),
        (round(math.sqrt(2) / 2, 4), ["pi/4", "3pi/4"],
         [round(math.pi / 4, 4), round(3 * math.pi / 4, 4)]),
        (round(math.sqrt(3) / 2, 4), ["pi/3", "2pi/3"],
         [round(math.pi / 3, 4), round(2 * math.pi / 3, 4)]),
        (-0.5, ["7pi/6", "11pi/6"],
         [round(7 * math.pi / 6, 4), round(11 * math.pi / 6, 4)]),
    ]

    _COS_SOLUTIONS = [
        (1, ["0"], [0.0]),
        (-1, ["pi"], [round(math.pi, 4)]),
        (0, ["pi/2", "3pi/2"],
         [round(math.pi / 2, 4), round(3 * math.pi / 2, 4)]),
        (0.5, ["pi/3", "5pi/3"],
         [round(math.pi / 3, 4), round(5 * math.pi / 3, 4)]),
        (round(math.sqrt(2) / 2, 4), ["pi/4", "7pi/4"],
         [round(math.pi / 4, 4), round(7 * math.pi / 4, 4)]),
        (round(math.sqrt(3) / 2, 4), ["pi/6", "11pi/6"],
         [round(math.pi / 6, 4), round(11 * math.pi / 6, 4)]),
        (-0.5, ["2pi/3", "4pi/3"],
         [round(2 * math.pi / 3, 4), round(4 * math.pi / 3, 4)]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trig_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Task description string.
        """
        return "solve trig equation on [0, 2pi]"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trigonometric equation problem.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        fn = self._rng.choice(["sin", "cos"])
        table = self._SIN_SOLUTIONS if fn == "sin" else self._COS_SOLUTIONS

        if difficulty <= 3:
            pool = table[:3]
        elif difficulty <= 6:
            pool = table[:6]
        else:
            pool = table

        a, exact_sols, num_sols = self._rng.choice(pool)
        problem = f"{fn}(x) = {a}, x in [0, 2pi]. Find all solutions."
        return problem, {
            "fn": fn, "a": a,
            "exact_solutions": exact_sols,
            "numeric_solutions": num_sols,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trig equation solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing the solutions.
        """
        steps = [f"{data['fn']}(x) = {data['a']}"]
        for exact, num in zip(data["exact_solutions"], data["numeric_solutions"]):
            steps.append(f"x = {exact} ({num})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            All solutions as a string.
        """
        return "x = " + ", ".join(data["exact_solutions"])


# ===================================================================
# 4. DOUBLE ANGLE (tier 4)
# ===================================================================

@register
class DoubleAngleGenerator(StepGenerator):
    """Apply double angle formulas given sin(x) and cos(x).

    Computes sin(2x) = 2*sin(x)*cos(x) and
    cos(2x) = cos^2(x) - sin^2(x) from given sin(x), cos(x) values.

    Difficulty scaling:
        Difficulty 1-3: standard angle values (30, 45, 60 degrees).
        Difficulty 4-6: supplementary angles, quadrant II.
        Difficulty 7-8: given sin and cos directly (non-standard).

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "double_angle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls angle complexity.

        Returns:
            Task description string.
        """
        return "compute sin(2x) and cos(2x) using double angle formulas"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a double angle formula problem.

        Args:
            difficulty: Controls angle complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            angle = self._rng.choice([30, 45, 60])
        elif difficulty <= 6:
            angle = self._rng.choice([30, 45, 60, 120, 135, 150])
        else:
            # Give sin and cos directly as fractions
            choices = [
                (3 / 5, 4 / 5),
                (5 / 13, 12 / 13),
                (8 / 17, 15 / 17),
                (7 / 25, 24 / 25),
            ]
            sin_x, cos_x = self._rng.choice(choices)
            if self._rng.choice([True, False]):
                cos_x = -cos_x  # quadrant II
            sin_x = round(sin_x, 4)
            cos_x = round(cos_x, 4)
            sin_2x = round(2 * sin_x * cos_x, 4)
            cos_2x = round(cos_x ** 2 - sin_x ** 2, 4)
            problem = (
                f"sin(x) = {sin_x}, cos(x) = {cos_x}. "
                f"Find sin(2x) and cos(2x)."
            )
            return problem, {
                "sin_x": sin_x, "cos_x": cos_x,
                "sin_2x": sin_2x, "cos_2x": cos_2x,
                "angle": None,
            }

        rad = math.radians(angle)
        sin_x = round(math.sin(rad), 4)
        cos_x = round(math.cos(rad), 4)
        sin_2x = round(2 * sin_x * cos_x, 4)
        cos_2x = round(cos_x ** 2 - sin_x ** 2, 4)

        problem = (
            f"x = {angle} degrees. "
            f"Compute sin(2x) and cos(2x)."
        )
        return problem, {
            "sin_x": sin_x, "cos_x": cos_x,
            "sin_2x": sin_2x, "cos_2x": cos_2x,
            "angle": angle,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate double angle computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the formulas applied.
        """
        steps = [
            f"sin(x) = {data['sin_x']}, cos(x) = {data['cos_x']}",
            f"sin(2x) = 2*sin(x)*cos(x) = 2*{data['sin_x']}*{data['cos_x']} = {data['sin_2x']}",
            f"cos(2x) = cos^2(x) - sin^2(x) = {round(data['cos_x'] ** 2, 4)} - {round(data['sin_x'] ** 2, 4)} = {data['cos_2x']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            sin(2x) and cos(2x) values.
        """
        return f"sin(2x) = {data['sin_2x']}, cos(2x) = {data['cos_2x']}"


# ===================================================================
# 5. INVERSE HYPERBOLIC (tier 5)
# ===================================================================

@register
class InverseHyperbolicGenerator(StepGenerator):
    """Compute arcsinh, arccosh, arctanh using logarithmic formulas.

    arcsinh(x) = ln(x + sqrt(x^2 + 1)),
    arccosh(x) = ln(x + sqrt(x^2 - 1)) for x >= 1,
    arctanh(x) = ln((1+x)/(1-x))/2 for |x| < 1.

    Difficulty scaling:
        Difficulty 1-3: arcsinh at 0, 1, -1.
        Difficulty 4-6: arccosh at 1, 2, 3; arctanh at 0, 0.5.
        Difficulty 7-8: larger values, all three functions.

    Prerequisites:
        logarithm (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inverse_hyperbolic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls function and argument variety.

        Returns:
            Task description string.
        """
        return "compute inverse hyperbolic function value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inverse hyperbolic function problem.

        Args:
            difficulty: Controls function and argument variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            fn = "arcsinh"
            x = self._rng.choice([0, 1, -1, 2])
        elif difficulty <= 6:
            fn = self._rng.choice(["arcsinh", "arccosh", "arctanh"])
            if fn == "arcsinh":
                x = self._rng.choice([0, 1, -1, 2, 3])
            elif fn == "arccosh":
                x = self._rng.choice([1, 2, 3, 4])
            else:
                x = self._rng.choice([0, 0.25, 0.5, -0.5])
        else:
            fn = self._rng.choice(["arcsinh", "arccosh", "arctanh"])
            if fn == "arcsinh":
                x = self._rng.choice([0, 1, -1, 2, 3, 5, -3])
            elif fn == "arccosh":
                x = self._rng.choice([1, 2, 3, 5, 10])
            else:
                x = self._rng.choice([0, 0.25, 0.5, -0.5, 0.75, -0.75])

        if fn == "arcsinh":
            inner = round(math.sqrt(x * x + 1), 4)
            result = round(math.log(x + inner), 4)
            formula = f"ln({x} + sqrt({x}^2+1)) = ln({x} + {inner})"
        elif fn == "arccosh":
            inner = round(math.sqrt(x * x - 1), 4)
            result = round(math.log(x + inner), 4)
            formula = f"ln({x} + sqrt({x}^2-1)) = ln({x} + {inner})"
        else:
            ratio = round((1 + x) / (1 - x), 4)
            result = round(math.log(ratio) / 2, 4)
            formula = f"ln((1+{x})/(1-{x}))/2 = ln({ratio})/2"

        problem = f"{fn}({x})"
        return problem, {
            "fn": fn, "x": x, "result": result, "formula": formula,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inverse hyperbolic steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the logarithmic formula.
        """
        return [
            f"{data['fn']}({data['x']})",
            data["formula"],
            f"= {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Computed value.
        """
        return str(data["result"])


# ===================================================================
# 6. TRIG SUBSTITUTION (tier 5)
# ===================================================================

@register
class TrigSubstitutionGenerator(StepGenerator):
    """Show trigonometric substitution for integrals with radicals.

    For sqrt(a^2 - x^2), substitute x = a*sin(theta).
    For sqrt(a^2 + x^2), substitute x = a*tan(theta).
    For sqrt(x^2 - a^2), substitute x = a*sec(theta).

    Difficulty scaling:
        Difficulty 1-3: sqrt(a^2 - x^2) with small a.
        Difficulty 4-6: sqrt(a^2 + x^2) patterns.
        Difficulty 7-8: sqrt(x^2 - a^2), completing the square.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trig_substitution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls radical type.

        Returns:
            Task description string.
        """
        return "identify trig substitution for integral with radical"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trig substitution identification problem.

        Args:
            difficulty: Controls radical type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 5)
        a2 = a * a

        if difficulty <= 3:
            form = "a2_minus_x2"
        elif difficulty <= 6:
            form = self._rng.choice(["a2_minus_x2", "a2_plus_x2"])
        else:
            form = self._rng.choice(["a2_minus_x2", "a2_plus_x2", "x2_minus_a2"])

        if form == "a2_minus_x2":
            radical = f"sqrt({a2} - x^2)"
            sub = f"x = {a}*sin(theta)"
            dx = f"dx = {a}*cos(theta)*dtheta"
            simplified = f"{a}*cos(theta)"
            identity = f"{a2} - {a2}*sin^2(theta) = {a2}*cos^2(theta)"
        elif form == "a2_plus_x2":
            radical = f"sqrt({a2} + x^2)"
            sub = f"x = {a}*tan(theta)"
            dx = f"dx = {a}*sec^2(theta)*dtheta"
            simplified = f"{a}*sec(theta)"
            identity = f"{a2} + {a2}*tan^2(theta) = {a2}*sec^2(theta)"
        else:
            radical = f"sqrt(x^2 - {a2})"
            sub = f"x = {a}*sec(theta)"
            dx = f"dx = {a}*sec(theta)*tan(theta)*dtheta"
            simplified = f"{a}*tan(theta)"
            identity = f"{a2}*sec^2(theta) - {a2} = {a2}*tan^2(theta)"

        problem = f"integral with {radical}. Show substitution."
        return problem, {
            "radical": radical, "a": a, "form": form,
            "substitution": sub, "dx": dx,
            "simplified": simplified, "identity": identity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trig substitution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing substitution and simplification.
        """
        return [
            f"radical: {data['radical']}",
            f"substitute: {data['substitution']}",
            f"{data['dx']}",
            f"identity: {data['identity']}",
            f"{data['radical']} -> {data['simplified']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Substitution and simplified form.
        """
        return f"{data['substitution']}, {data['radical']} = {data['simplified']}"
