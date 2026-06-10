"""Extended calculus generators for tiers 5-6.

Provides 15 generators covering implicit differentiation, logarithmic
differentiation, u-substitution, trig substitution, improper integrals,
arc length, surface area of revolution, volume of revolution, parametric
derivatives, polar area, multivariable chain rule, double integrals,
triple integrals, line integrals, and Green's theorem.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ────────────────────────────────────────────────


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


# ── 1. Implicit differentiation (tier 5) ─────────────────────────────


@register
class ImplicitDifferentiationGenerator(StepGenerator):
    """Find dy/dx by implicit differentiation of F(x,y)=0.

    Given an implicit equation such as a circle, ellipse, or cubic,
    computes dy/dx = -F_x / F_y and evaluates at a specific point.

    Input format:
        ``find dy/dx by implicit differentiation``

    Target format:
        ``x^2 + y^2 = 25 <step> F_x = 2x, F_y = 2y
        <step> dy/dx = -2x/(2y) = -x/y
        <step> at (3,4): dy/dx = -3/4``

    Difficulty scaling:
        Difficulty 1-3: circles x^2 + y^2 = r^2.
        Difficulty 4-6: ellipses ax^2 + by^2 = c.
        Difficulty 7-8: cubics x^3 + y^3 = cxy.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "implicit_differentiation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Natural language description.
        """
        return "find dy/dx by implicit differentiation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an implicit differentiation problem.

        Args:
            difficulty: Controls curve type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._circle_problem(difficulty)
        if difficulty <= 6:
            return self._ellipse_problem(difficulty)
        return self._cubic_problem(difficulty)

    def _circle_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a circle implicit differentiation problem.

        Args:
            difficulty: Controls radius.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r = self._rng.randint(2, 5 + difficulty)
        # Pick a Pythagorean-friendly point
        triples = [(3, 4), (5, 12), (8, 15), (6, 8)]
        x0, y0 = self._rng.choice(triples)
        r_sq = x0 * x0 + y0 * y0
        dydx = -x0 / y0
        problem = f"x^2 + y^2 = {r_sq}"
        return problem, {
            "curve": "circle", "x0": x0, "y0": y0,
            "fx": f"2x", "fy": f"2y",
            "dydx_expr": "-x/y",
            "dydx_val": dydx,
        }

    def _ellipse_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ellipse implicit differentiation problem.

        Args:
            difficulty: Controls coefficients.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        x0 = self._rng.randint(1, 3)
        y0 = self._rng.randint(1, 3)
        c = a * x0 * x0 + b * y0 * y0
        dydx = -(a * x0) / (b * y0) if b * y0 != 0 else 0.0
        problem = f"{a}x^2 + {b}y^2 = {c}"
        return problem, {
            "curve": "ellipse", "a": a, "b": b, "x0": x0, "y0": y0,
            "fx": f"{2*a}x", "fy": f"{2*b}y",
            "dydx_expr": f"-{a}x/({b}y)",
            "dydx_val": dydx,
        }

    def _cubic_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cubic implicit differentiation problem.

        Uses x^3 + y^3 = k*x*y. dy/dx = (k*y - 3x^2) / (3y^2 - k*x).

        Args:
            difficulty: Controls coefficient k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(2, 6)
        x0 = self._rng.randint(1, 3)
        y0 = self._rng.randint(1, 3)
        denom = 3 * y0 * y0 - k * x0
        if denom == 0:
            y0 += 1
            denom = 3 * y0 * y0 - k * x0
        numer = k * y0 - 3 * x0 * x0
        dydx = numer / denom
        problem = f"x^3 + y^3 = {k}xy"
        return problem, {
            "curve": "cubic", "k": k, "x0": x0, "y0": y0,
            "fx": f"3x^2 - {k}y", "fy": f"3y^2 - {k}x",
            "dydx_expr": f"({k}y - 3x^2)/(3y^2 - {k}x)",
            "dydx_val": dydx,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate implicit differentiation steps.

        Args:
            data: Solution data with partial derivatives.

        Returns:
            Steps showing F_x, F_y, and dy/dx evaluation.
        """
        return [
            f"F_x = {data['fx']}, F_y = {data['fy']}",
            f"dy/dx = {data['dydx_expr']}",
            f"at ({data['x0']},{data['y0']}): dy/dx = {_fmt(data['dydx_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the dy/dx value.

        Args:
            data: Solution data.

        Returns:
            Formatted dy/dx.
        """
        return f"dy/dx = {_fmt(data['dydx_val'])}"


# ── 2. Logarithmic differentiation (tier 5) ──────────────────────────


@register
class LogarithmicDifferentiationGenerator(StepGenerator):
    """Differentiate using logarithmic differentiation.

    Takes ln of both sides of y = x^x or y = (product)^n, then
    differentiates to find dy/dx.

    Input format:
        ``find dy/dx using logarithmic differentiation``

    Target format:
        ``y = x^x <step> ln(y) = x*ln(x)
        <step> (1/y)*dy/dx = ln(x) + 1
        <step> dy/dx = x^x*(ln(x)+1) <step> at x=2: dy/dx = ...``

    Difficulty scaling:
        Difficulty 1-3: y = x^a for integer a.
        Difficulty 4-6: y = x^x.
        Difficulty 7-8: y = (x^a * (x+b))^n.

    Prerequisites:
        logarithm (tier 5), derivative (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logarithmic_differentiation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm", "derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "find dy/dx using logarithmic differentiation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logarithmic differentiation problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._power_problem(difficulty)
        if difficulty <= 6:
            return self._xx_problem(difficulty)
        return self._product_problem(difficulty)

    def _power_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate y = x^a logarithmic differentiation.

        Args:
            difficulty: Controls exponent.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 5)
        x0 = self._rng.randint(1, 4)
        y_val = x0 ** a
        dydx = a * x0 ** (a - 1)
        problem = f"y = x^{{{a}}}"
        return problem, {
            "func_type": "power", "a": a, "x0": x0,
            "ln_expr": f"{a}*ln(x)",
            "deriv_expr": f"{a}/x",
            "dydx_formula": f"{a}*x^{{{a-1}}}",
            "dydx_val": float(dydx),
        }

    def _xx_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate y = x^x logarithmic differentiation.

        Args:
            difficulty: Controls evaluation point.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        x0 = self._rng.randint(1, 4)
        y_val = x0 ** x0
        dydx = y_val * (math.log(x0) + 1)
        problem = "y = x^{x}"
        return problem, {
            "func_type": "xx", "x0": x0,
            "ln_expr": "x*ln(x)",
            "deriv_expr": "ln(x) + 1",
            "dydx_formula": "x^x*(ln(x)+1)",
            "dydx_val": dydx,
        }

    def _product_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate y = x^a * (x+b) logarithmic differentiation.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 4)
        b = self._rng.randint(1, 5)
        x0 = self._rng.randint(1, 3)
        y_val = (x0 ** a) * (x0 + b)
        dydx = a * x0 ** (a - 1) * (x0 + b) + x0 ** a
        problem = f"y = x^{{{a}}}(x+{b})"
        return problem, {
            "func_type": "product", "a": a, "b": b, "x0": x0,
            "ln_expr": f"{a}*ln(x) + ln(x+{b})",
            "deriv_expr": f"{a}/x + 1/(x+{b})",
            "dydx_formula": f"y*({a}/x + 1/(x+{b}))",
            "dydx_val": float(dydx),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate logarithmic differentiation steps.

        Args:
            data: Solution data with ln expressions.

        Returns:
            Steps showing ln, differentiation, and evaluation.
        """
        return [
            f"ln(y) = {data['ln_expr']}",
            f"(1/y)*dy/dx = {data['deriv_expr']}",
            f"dy/dx = {data['dydx_formula']}",
            f"at x={data['x0']}: dy/dx = {_fmt(data['dydx_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the derivative value.

        Args:
            data: Solution data.

        Returns:
            Formatted dy/dx.
        """
        return f"dy/dx = {_fmt(data['dydx_val'])}"


# ── 3. Integration by substitution (tier 5) ──────────────────────────


@register
class IntegrationBySubstitutionGenerator(StepGenerator):
    """Evaluate an integral using u-substitution.

    Identifies u = g(x), computes du = g'(x) dx, transforms the
    integral, and evaluates.

    Input format:
        ``evaluate integral using u-substitution``

    Target format:
        ``int 2x*(x^2+1)^3 dx <step> u = x^2+1, du = 2x dx
        <step> int u^3 du = u^4/4
        <step> = (x^2+1)^4/4 + C``

    Difficulty scaling:
        Difficulty 1-3: int a*x*(x^2+c)^n dx.
        Difficulty 4-6: int cos(x)*sin(x)^n dx or similar.
        Difficulty 7-8: int x*exp(x^2) dx.

    Prerequisites:
        chain_rule (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integration_by_substitution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["chain_rule"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Natural language description.
        """
        return "evaluate integral using u-substitution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a u-substitution integral problem.

        Args:
            difficulty: Controls integrand type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._poly_sub(difficulty)
        if difficulty <= 6:
            return self._trig_sub(difficulty)
        return self._exp_sub(difficulty)

    def _poly_sub(self, difficulty: int) -> tuple[str, dict]:
        """Generate polynomial u-substitution problem.

        Args:
            difficulty: Controls exponent.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(1, 5)
        n = self._rng.randint(2, 4)
        # int 2x*(x^2+c)^n dx, u = x^2+c
        problem = f"\\int 2x(x^2+{c})^{{{n}}} dx"
        return problem, {
            "sub_type": "poly", "c": c, "n": n,
            "u": f"x^2+{c}", "du": "2x dx",
            "transformed": f"\\int u^{{{n}}} du",
            "antideriv": f"u^{{{n+1}}}/{n+1}",
            "answer": f"(x^2+{c})^{{{n+1}}}/{n+1} + C",
        }

    def _trig_sub(self, difficulty: int) -> tuple[str, dict]:
        """Generate trig u-substitution problem.

        Args:
            difficulty: Controls exponent.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, 4)
        problem = f"\\int \\cos(x)\\sin^{{{n}}}(x) dx"
        return problem, {
            "sub_type": "trig", "n": n,
            "u": "\\sin(x)", "du": "\\cos(x) dx",
            "transformed": f"\\int u^{{{n}}} du",
            "antideriv": f"u^{{{n+1}}}/{n+1}",
            "answer": f"\\sin^{{{n+1}}}(x)/{n+1} + C",
        }

    def _exp_sub(self, difficulty: int) -> tuple[str, dict]:
        """Generate exponential u-substitution problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        problem = f"\\int {2*a}x e^{{{a}x^2}} dx"
        return problem, {
            "sub_type": "exp", "a": a,
            "u": f"{a}x^2", "du": f"{2*a}x dx",
            "transformed": "\\int e^{u} du",
            "antideriv": "e^{u}",
            "answer": f"e^{{{a}x^2}} + C",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate u-substitution steps.

        Args:
            data: Solution data with substitution details.

        Returns:
            Steps showing u, du, transform, and result.
        """
        return [
            f"let u = {data['u']}, du = {data['du']}",
            f"integral becomes {data['transformed']}",
            f"= {data['antideriv']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the antiderivative.

        Args:
            data: Solution data.

        Returns:
            Antiderivative expression.
        """
        return data["answer"]


# ── 4. Trigonometric substitution (tier 5) ────────────────────────────


@register
class IntegrationTrigSubGenerator(StepGenerator):
    """Evaluate integrals using trigonometric substitution.

    For sqrt(a^2 - x^2): use x = a*sin(t).
    For sqrt(x^2 + a^2): use x = a*tan(t).
    Transforms and simplifies to a trig integral.

    Input format:
        ``evaluate integral using trig substitution``

    Target format:
        ``int 1/sqrt(9-x^2) dx <step> x = 3*sin(t), dx = 3*cos(t) dt
        <step> sqrt(9-9sin^2(t)) = 3cos(t)
        <step> int dt = t = arcsin(x/3) + C``

    Difficulty scaling:
        Difficulty 1-3: int 1/sqrt(a^2-x^2) dx.
        Difficulty 4-6: int sqrt(a^2-x^2) dx.
        Difficulty 7-8: int 1/sqrt(x^2+a^2) dx.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integration_trig_sub"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand form.

        Returns:
            Natural language description.
        """
        return "evaluate integral using trig substitution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trig substitution integral problem.

        Args:
            difficulty: Controls integral form.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 5)
        a2 = a * a
        if difficulty <= 3:
            problem = f"\\int \\frac{{1}}{{\\sqrt{{{a2}-x^2}}}} dx"
            return problem, {
                "sub_type": "arcsin", "a": a,
                "sub": f"x = {a}\\sin(t)",
                "dx": f"{a}\\cos(t) dt",
                "simplify": f"\\sqrt{{{a2}-{a2}\\sin^2(t)}} = {a}\\cos(t)",
                "result": f"\\arcsin(x/{a}) + C",
            }
        if difficulty <= 6:
            problem = f"\\int \\sqrt{{{a2}-x^2}} dx"
            return problem, {
                "sub_type": "sin_area", "a": a,
                "sub": f"x = {a}\\sin(t)",
                "dx": f"{a}\\cos(t) dt",
                "simplify": f"{a}^2\\cos^2(t) dt",
                "result": f"({a2}/2)(\\arcsin(x/{a}) + x\\sqrt{{{a2}-x^2}}/{a2}) + C",
            }
        problem = f"\\int \\frac{{1}}{{\\sqrt{{x^2+{a2}}}}} dx"
        return problem, {
            "sub_type": "tan", "a": a,
            "sub": f"x = {a}\\tan(t)",
            "dx": f"{a}\\sec^2(t) dt",
            "simplify": f"\\sqrt{{{a2}\\tan^2(t)+{a2}}} = {a}\\sec(t)",
            "result": f"\\ln|x + \\sqrt{{x^2+{a2}}}| + C",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trig substitution steps.

        Args:
            data: Solution data with substitution details.

        Returns:
            Steps showing substitution, simplification, and result.
        """
        return [
            f"let {data['sub']}, dx = {data['dx']}",
            f"{data['simplify']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the antiderivative.

        Args:
            data: Solution data.

        Returns:
            Antiderivative expression.
        """
        return data["result"]


# ── 5. Improper integral (tier 6) ────────────────────────────────────


@register
class ImproperIntegralGenerator(StepGenerator):
    """Evaluate improper integrals and test convergence.

    Computes integral from a to infinity of f(x) dx as the limit of
    the definite integral from a to b as b approaches infinity.

    Input format:
        ``evaluate improper integral and test convergence``

    Target format:
        ``int_1^inf 1/x^2 dx <step> lim_{b->inf} [-1/x]_1^b
        <step> lim_{b->inf} (-1/b + 1) = 1 <step> converges to 1``

    Difficulty scaling:
        Difficulty 1-3: int_1^inf 1/x^p dx for p > 1.
        Difficulty 4-6: int_1^inf e^{-ax} dx.
        Difficulty 7-8: int_0^inf x*e^{-x} dx.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "improper_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand type.

        Returns:
            Natural language description.
        """
        return "evaluate improper integral and test convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an improper integral problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._power_integral(difficulty)
        if difficulty <= 6:
            return self._exp_integral(difficulty)
        return self._xexp_integral(difficulty)

    def _power_integral(self, difficulty: int) -> tuple[str, dict]:
        """Generate int_1^inf 1/x^p dx problem.

        Args:
            difficulty: Controls p value.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(2, 4)
        value = 1.0 / (p - 1)
        problem = f"\\int_1^{{\\infty}} \\frac{{1}}{{x^{{{p}}}}} dx"
        return problem, {
            "int_type": "power", "p": p,
            "antideriv": f"-1/({p-1})x^{{{p-1}}}",
            "limit_expr": f"lim_{{b->inf}} [-1/(({p-1})x^{{{p-1}}})]_1^b",
            "converges": True, "value": value,
        }

    def _exp_integral(self, difficulty: int) -> tuple[str, dict]:
        """Generate int_0^inf e^{-ax} dx problem.

        Args:
            difficulty: Controls a value.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 5)
        value = 1.0 / a
        problem = f"\\int_0^{{\\infty}} e^{{-{a}x}} dx"
        return problem, {
            "int_type": "exp", "a": a,
            "antideriv": f"-1/{a} e^{{-{a}x}}",
            "limit_expr": f"lim_{{b->inf}} [-1/{a} e^{{-{a}b}} + 1/{a}]",
            "converges": True, "value": value,
        }

    def _xexp_integral(self, difficulty: int) -> tuple[str, dict]:
        """Generate int_0^inf x*e^{-x} dx problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\int_0^{\\infty} x e^{-x} dx"
        return problem, {
            "int_type": "xexp",
            "antideriv": "-(x+1)e^{-x}",
            "limit_expr": "lim_{b->inf} [-(b+1)e^{-b} + 1]",
            "converges": True, "value": 1.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate improper integral evaluation steps.

        Args:
            data: Solution data with limit computation.

        Returns:
            Steps showing antiderivative, limit, and convergence.
        """
        return [
            f"antiderivative: {data['antideriv']}",
            data["limit_expr"],
            f"= {_fmt(data['value'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return convergence result and value.

        Args:
            data: Solution data.

        Returns:
            Convergence verdict and value.
        """
        if data["converges"]:
            return f"converges to {_fmt(data['value'])}"
        return "diverges"


# ── 6. Arc length (tier 5) ───────────────────────────────────────────


@register
class ArcLengthGenerator(StepGenerator):
    """Compute the arc length of a curve.

    Uses L = integral sqrt(1 + (dy/dx)^2) dx over an interval.

    Input format:
        ``compute arc length of curve``

    Target format:
        ``y = x^2 on [0,1] <step> dy/dx = 2x
        <step> sqrt(1+4x^2) <step> L = int_0^1 sqrt(1+4x^2) dx
        <step> L = 1.4789``

    Difficulty scaling:
        Difficulty 1-3: y = ax (straight line, L = sqrt(1+a^2)*interval).
        Difficulty 4-6: y = x^{3/2}, clean formula.
        Difficulty 7-8: y = x^2, numerical evaluation.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "arc_length"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Natural language description.
        """
        return "compute arc length of curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an arc length problem.

        Args:
            difficulty: Controls curve type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_arc(difficulty)
        if difficulty <= 6:
            return self._power_32_arc(difficulty)
        return self._quadratic_arc(difficulty)

    def _linear_arc(self, difficulty: int) -> tuple[str, dict]:
        """Generate arc length of y = ax on [0, b].

        Args:
            difficulty: Controls slope.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        length = math.sqrt(1 + a * a) * b
        problem = f"y = {a}x on [0, {b}]"
        return problem, {
            "curve": "linear", "dydx": f"{a}",
            "integrand": f"\\sqrt{{1+{a*a}}}",
            "length": length,
        }

    def _power_32_arc(self, difficulty: int) -> tuple[str, dict]:
        """Generate arc length of y = (2/3)*x^{3/2} on [0, a].

        dy/dx = x^{1/2}, sqrt(1+x) integrates to (2/3)(1+x)^{3/2}.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        length = (2.0 / 3.0) * ((1 + a) ** 1.5 - 1.0)
        problem = f"y = (2/3)x^{{3/2}} on [0, {a}]"
        return problem, {
            "curve": "x^{3/2}", "dydx": "x^{1/2}",
            "integrand": "\\sqrt{1+x}",
            "length": length,
        }

    def _quadratic_arc(self, difficulty: int) -> tuple[str, dict]:
        """Generate arc length of y = x^2 on [0, a].

        Uses numerical formula: L = (a*sqrt(1+4a^2) + arcsinh(2a)/2) / 2.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        length = (a * math.sqrt(1 + 4 * a * a)
                  + math.asinh(2 * a) / 2.0) / 2.0
        # Corrected arc length formula: integrate sqrt(1+4x^2) from 0 to a
        # = [x*sqrt(1+4x^2)/2 + (1/4)*arcsinh(2x)]_0^a
        length = (a * math.sqrt(1 + 4 * a * a)
                  + math.asinh(2 * a) / 4.0) / 1.0
        # Exact: L = (x*sqrt(1+4x^2) + (1/4)*ln(2x+sqrt(1+4x^2)))/2 evaluated 0 to a
        # Simpler: numerical integration for display
        n_steps = 1000
        dx = a / n_steps
        total = 0.0
        for i in range(n_steps):
            x = (i + 0.5) * dx
            total += math.sqrt(1 + 4 * x * x) * dx
        length = total
        problem = f"y = x^2 on [0, {a}]"
        return problem, {
            "curve": "x^2", "dydx": "2x",
            "integrand": "\\sqrt{1+4x^2}",
            "length": length,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate arc length computation steps.

        Args:
            data: Solution data with integrand and length.

        Returns:
            Steps showing dy/dx, integrand, and result.
        """
        return [
            f"dy/dx = {data['dydx']}",
            f"integrand = {data['integrand']}",
            f"L = {_fmt(data['length'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the arc length.

        Args:
            data: Solution data.

        Returns:
            Formatted arc length.
        """
        return f"L = {_fmt(data['length'])}"


# ── 7. Surface area of revolution (tier 6) ───────────────────────────


@register
class SurfaceAreaRevolutionGenerator(StepGenerator):
    """Compute surface area of a curve rotated about the x-axis.

    Uses SA = 2*pi*integral y*sqrt(1+(dy/dx)^2) dx for rotation
    about the x-axis.

    Input format:
        ``compute surface area of revolution about x-axis``

    Target format:
        ``y = x on [0,1], rotate about x-axis <step>
        dy/dx = 1, sqrt(1+1) = sqrt(2)
        <step> SA = 2*pi*int_0^1 x*sqrt(2) dx
        <step> = 2*pi*sqrt(2)/2 = pi*sqrt(2)``

    Difficulty scaling:
        Difficulty 1-3: y = ax on [0, b].
        Difficulty 4-6: y = sqrt(x) on [0, a].
        Difficulty 7-8: y = x^2 on [0, a], numerical.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "surface_area_revolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Natural language description.
        """
        return "compute surface area of revolution about x-axis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a surface area of revolution problem.

        Args:
            difficulty: Controls curve type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_sa(difficulty)
        if difficulty <= 6:
            return self._sqrt_sa(difficulty)
        return self._quad_sa(difficulty)

    def _linear_sa(self, difficulty: int) -> tuple[str, dict]:
        """Generate SA for y = ax rotated about x-axis on [0, b].

        SA = 2*pi*int_0^b ax*sqrt(1+a^2) dx = pi*a*b^2*sqrt(1+a^2).

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        sa = math.pi * a * b * b * math.sqrt(1 + a * a)
        problem = f"y = {a}x on [0, {b}], rotate about x-axis"
        return problem, {
            "curve": "linear", "a": a, "b": b,
            "dydx": f"{a}",
            "integrand": f"2\\pi \\cdot {a}x \\cdot \\sqrt{{{1+a*a}}}",
            "sa": sa,
        }

    def _sqrt_sa(self, difficulty: int) -> tuple[str, dict]:
        """Generate SA for y = sqrt(x) rotated about x-axis on [1, a].

        dy/dx = 1/(2*sqrt(x)), so 1+(dy/dx)^2 = 1+1/(4x).

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 4)
        # Numerical integration
        n_steps = 1000
        dx = (a - 1.0) / n_steps
        total = 0.0
        for i in range(n_steps):
            x = 1.0 + (i + 0.5) * dx
            y = math.sqrt(x)
            dydx = 0.5 / math.sqrt(x)
            total += y * math.sqrt(1 + dydx * dydx) * dx
        sa = 2 * math.pi * total
        problem = f"y = \\sqrt{{x}} on [1, {a}], rotate about x-axis"
        return problem, {
            "curve": "sqrt(x)", "a": a,
            "dydx": "1/(2\\sqrt{x})",
            "integrand": "2\\pi\\sqrt{x}\\sqrt{1+1/(4x)}",
            "sa": sa,
        }

    def _quad_sa(self, difficulty: int) -> tuple[str, dict]:
        """Generate SA for y = x^2 rotated about x-axis on [0, a].

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 2)
        n_steps = 1000
        dx = a / n_steps
        total = 0.0
        for i in range(n_steps):
            x = (i + 0.5) * dx
            y = x * x
            dydx = 2 * x
            total += y * math.sqrt(1 + dydx * dydx) * dx
        sa = 2 * math.pi * total
        problem = f"y = x^2 on [0, {a}], rotate about x-axis"
        return problem, {
            "curve": "x^2", "a": a,
            "dydx": "2x",
            "integrand": "2\\pi x^2 \\sqrt{1+4x^2}",
            "sa": sa,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate surface area computation steps.

        Args:
            data: Solution data with integrand and SA.

        Returns:
            Steps showing dy/dx, integrand, and result.
        """
        return [
            f"dy/dx = {data['dydx']}",
            f"SA = {data['integrand']}",
            f"SA = {_fmt(data['sa'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the surface area.

        Args:
            data: Solution data.

        Returns:
            Formatted surface area.
        """
        return f"SA = {_fmt(data['sa'])}"


# ── 8. Volume of revolution (tier 5) ─────────────────────────────────


@register
class VolumeRevolutionGenerator(StepGenerator):
    """Compute volume of solid of revolution using disk or shell method.

    Disk: V = pi*integral y^2 dx.
    Shell: V = 2*pi*integral x*y dx.

    Input format:
        ``compute volume of revolution``

    Target format:
        ``y = x^2 on [0,2], disk method <step>
        V = pi*int_0^2 x^4 dx <step> = pi*[x^5/5]_0^2
        <step> = 32*pi/5``

    Difficulty scaling:
        Difficulty 1-3: y = ax, disk method.
        Difficulty 4-6: y = x^2, disk method.
        Difficulty 7-8: y = sqrt(x), shell method.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "volume_revolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls method and curve.

        Returns:
            Natural language description.
        """
        return "compute volume of revolution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a volume of revolution problem.

        Args:
            difficulty: Controls curve and method.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_disk(difficulty)
        if difficulty <= 6:
            return self._quad_disk(difficulty)
        return self._sqrt_shell(difficulty)

    def _linear_disk(self, difficulty: int) -> tuple[str, dict]:
        """Generate disk method volume for y = ax on [0, b].

        V = pi*int_0^b a^2*x^2 dx = pi*a^2*b^3/3.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        vol = math.pi * a * a * b ** 3 / 3.0
        problem = f"y = {a}x on [0, {b}], disk method about x-axis"
        return problem, {
            "method": "disk", "curve": "linear",
            "integrand": f"\\pi \\cdot {a*a}x^2",
            "volume": vol,
        }

    def _quad_disk(self, difficulty: int) -> tuple[str, dict]:
        """Generate disk method volume for y = x^2 on [0, a].

        V = pi*int_0^a x^4 dx = pi*a^5/5.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        vol = math.pi * a ** 5 / 5.0
        problem = f"y = x^2 on [0, {a}], disk method about x-axis"
        return problem, {
            "method": "disk", "curve": "x^2",
            "integrand": "\\pi x^4",
            "volume": vol,
        }

    def _sqrt_shell(self, difficulty: int) -> tuple[str, dict]:
        """Generate shell method volume for y = sqrt(x) on [0, a].

        V = 2*pi*int_0^a x*sqrt(x) dx = 2*pi*int x^{3/2} dx
        = 2*pi*(2/5)*a^{5/2}.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        vol = 2 * math.pi * (2.0 / 5.0) * a ** 2.5
        problem = f"y = \\sqrt{{x}} on [0, {a}], shell method about y-axis"
        return problem, {
            "method": "shell", "curve": "sqrt(x)",
            "integrand": "2\\pi x^{3/2}",
            "volume": vol,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate volume computation steps.

        Args:
            data: Solution data with integrand and volume.

        Returns:
            Steps showing method, integrand, and result.
        """
        return [
            f"method: {data['method']}",
            f"V = \\int {data['integrand']} dx",
            f"V = {_fmt(data['volume'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the volume.

        Args:
            data: Solution data.

        Returns:
            Formatted volume.
        """
        return f"V = {_fmt(data['volume'])}"


# ── 9. Parametric derivative (tier 5) ────────────────────────────────


@register
class ParametricDerivativeGenerator(StepGenerator):
    """Compute dy/dx for parametrically defined curves.

    For x = f(t), y = g(t): dy/dx = (dy/dt) / (dx/dt).
    Also computes d2y/dx2 = (d/dt(dy/dx)) / (dx/dt).

    Input format:
        ``find dy/dx for parametric curve``

    Target format:
        ``x = t^2, y = t^3 <step> dx/dt = 2t, dy/dt = 3t^2
        <step> dy/dx = 3t/2 <step> at t=2: dy/dx = 3``

    Difficulty scaling:
        Difficulty 1-3: x = at, y = bt^2.
        Difficulty 4-6: x = t^2, y = t^3.
        Difficulty 7-8: x = cos(t), y = sin(t), also d2y/dx2.

    Prerequisites:
        derivative (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parametric_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parametric curve complexity.

        Returns:
            Natural language description.
        """
        return "find dy/dx for parametric curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a parametric derivative problem.

        Args:
            difficulty: Controls curve type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_quad(difficulty)
        if difficulty <= 6:
            return self._poly_param(difficulty)
        return self._trig_param(difficulty)

    def _linear_quad(self, difficulty: int) -> tuple[str, dict]:
        """Generate parametric derivative for x=at, y=bt^2.

        Args:
            difficulty: Controls coefficients.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        t0 = self._rng.randint(1, 4)
        dxdt = a
        dydt = 2 * b * t0
        dydx = dydt / dxdt
        problem = f"x = {a}t, y = {b}t^2"
        return problem, {
            "param_type": "lin_quad", "t0": t0,
            "dxdt_expr": f"{a}", "dydt_expr": f"{2*b}t",
            "dydx_expr": f"{2*b}t/{a}",
            "dydx_val": dydx,
        }

    def _poly_param(self, difficulty: int) -> tuple[str, dict]:
        """Generate parametric derivative for x=t^2, y=t^3.

        Args:
            difficulty: Controls evaluation point.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        t0 = self._rng.randint(1, 4)
        dxdt = 2 * t0
        dydt = 3 * t0 * t0
        dydx = dydt / dxdt
        problem = "x = t^2, y = t^3"
        return problem, {
            "param_type": "poly", "t0": t0,
            "dxdt_expr": "2t", "dydt_expr": "3t^2",
            "dydx_expr": "3t/2",
            "dydx_val": dydx,
        }

    def _trig_param(self, difficulty: int) -> tuple[str, dict]:
        """Generate parametric derivative for x=a*cos(t), y=b*sin(t).

        Args:
            difficulty: Controls coefficients.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        t0 = round(self._rng.choice([0.5, 1.0, math.pi / 4, math.pi / 3]), 4)
        dxdt = -a * math.sin(t0)
        dydt = b * math.cos(t0)
        dydx = dydt / dxdt if abs(dxdt) > 1e-10 else 0.0
        problem = f"x = {a}\\cos(t), y = {b}\\sin(t)"
        return problem, {
            "param_type": "trig", "a": a, "b": b, "t0": t0,
            "dxdt_expr": f"-{a}\\sin(t)", "dydt_expr": f"{b}\\cos(t)",
            "dydx_expr": f"-{b}\\cos(t)/({a}\\sin(t))",
            "dydx_val": dydx,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate parametric derivative steps.

        Args:
            data: Solution data with dx/dt and dy/dt.

        Returns:
            Steps showing derivatives and dy/dx.
        """
        return [
            f"dx/dt = {data['dxdt_expr']}, dy/dt = {data['dydt_expr']}",
            f"dy/dx = {data['dydx_expr']}",
            f"at t={_fmt(data['t0'])}: dy/dx = {_fmt(data['dydx_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the dy/dx value.

        Args:
            data: Solution data.

        Returns:
            Formatted dy/dx.
        """
        return f"dy/dx = {_fmt(data['dydx_val'])}"


# ── 10. Polar area (tier 5) ──────────────────────────────────────────


@register
class PolarAreaGenerator(StepGenerator):
    """Compute the area enclosed by a polar curve.

    Uses A = (1/2)*integral r^2 d(theta) for cardioid, rose, or
    circle polar curves.

    Input format:
        ``compute area enclosed by polar curve``

    Target format:
        ``r = 2+2cos(t) (cardioid) <step>
        A = (1/2)*int_0^{2pi} (2+2cos(t))^2 dt
        <step> expand: 4+8cos(t)+4cos^2(t)
        <step> A = 6*pi``

    Difficulty scaling:
        Difficulty 1-3: r = a (circle), A = pi*a^2.
        Difficulty 4-6: r = a(1+cos(t)) cardioid, A = 3*pi*a^2/2.
        Difficulty 7-8: r = a*cos(n*t) rose.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polar_area"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polar curve type.

        Returns:
            Natural language description.
        """
        return "compute area enclosed by polar curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polar area problem.

        Args:
            difficulty: Controls curve type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._circle_polar(difficulty)
        if difficulty <= 6:
            return self._cardioid_polar(difficulty)
        return self._rose_polar(difficulty)

    def _circle_polar(self, difficulty: int) -> tuple[str, dict]:
        """Generate polar area for r = a (circle).

        Args:
            difficulty: Controls radius.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 5)
        area = math.pi * a * a
        problem = f"r = {a}"
        return problem, {
            "curve": "circle", "a": a,
            "integral_expr": f"(1/2)\\int_0^{{2\\pi}} {a*a} d\\theta",
            "area": area,
        }

    def _cardioid_polar(self, difficulty: int) -> tuple[str, dict]:
        """Generate polar area for r = a(1+cos(theta)) cardioid.

        A = (3/2)*pi*a^2.

        Args:
            difficulty: Controls a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        area = 1.5 * math.pi * a * a
        problem = f"r = {a}(1+\\cos(\\theta))"
        return problem, {
            "curve": "cardioid", "a": a,
            "integral_expr": (f"(1/2)\\int_0^{{2\\pi}} "
                              f"{a}^2(1+\\cos(\\theta))^2 d\\theta"),
            "area": area,
        }

    def _rose_polar(self, difficulty: int) -> tuple[str, dict]:
        """Generate polar area for r = a*cos(n*theta) rose.

        For n petals (n odd): A = pi*a^2/(2n) * n = pi*a^2/2.

        Args:
            difficulty: Controls petals.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        n = self._rng.choice([2, 3, 4])
        # Full area of n-petal rose:
        # n odd: n petals, each petal area = pi*a^2/(4n), total = pi*a^2/4
        # n even: 2n petals, total = pi*a^2/2
        if n % 2 == 0:
            area = math.pi * a * a / 2.0
        else:
            area = math.pi * a * a / 4.0
        problem = f"r = {a}\\cos({n}\\theta)"
        return problem, {
            "curve": "rose", "a": a, "n": n,
            "integral_expr": (f"(1/2)\\int r^2 d\\theta"),
            "area": area,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate polar area computation steps.

        Args:
            data: Solution data with integral and area.

        Returns:
            Steps showing integral setup and result.
        """
        return [
            f"curve: {data['curve']}",
            f"A = {data['integral_expr']}",
            f"A = {_fmt(data['area'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the area.

        Args:
            data: Solution data.

        Returns:
            Formatted area.
        """
        return f"A = {_fmt(data['area'])}"


# ── 11. Multivariable chain rule (tier 5) ────────────────────────────


@register
class MultivariableChainRuleGenerator(StepGenerator):
    """Apply the multivariable chain rule.

    For z = f(x, y) with x = g(t), y = h(t):
    dz/dt = (dz/dx)(dx/dt) + (dz/dy)(dy/dt).

    Input format:
        ``apply multivariable chain rule``

    Target format:
        ``z = x^2*y, x = 2t, y = t^2 <step>
        dz/dx = 2xy, dz/dy = x^2, dx/dt = 2, dy/dt = 2t
        <step> dz/dt = 2xy*2 + x^2*2t
        <step> at t=1: dz/dt = 4*1*1*2 + 4*2 = 16``

    Difficulty scaling:
        Difficulty 1-3: z = x*y, x = at, y = bt.
        Difficulty 4-6: z = x^2*y, x = at, y = t^2.
        Difficulty 7-8: z = x^2 + y^2, x = cos(t), y = sin(t).

    Prerequisites:
        partial_derivative (tier 4), chain_rule (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multivariable_chain_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative", "chain_rule"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "apply multivariable chain rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multivariable chain rule problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_chain(difficulty)
        if difficulty <= 6:
            return self._poly_chain(difficulty)
        return self._trig_chain(difficulty)

    def _linear_chain(self, difficulty: int) -> tuple[str, dict]:
        """Generate chain rule for z = xy, x = at, y = bt.

        Args:
            difficulty: Controls coefficients.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        t0 = self._rng.randint(1, 3)
        x0 = a * t0
        y0 = b * t0
        dzdt = a * y0 + b * x0  # dz/dx=y, dx/dt=a, dz/dy=x, dy/dt=b
        problem = f"z = xy, x = {a}t, y = {b}t"
        return problem, {
            "func_type": "linear", "t0": t0,
            "dzdx": "y", "dzdy": "x",
            "dxdt": f"{a}", "dydt": f"{b}",
            "dzdt_expr": f"y*{a} + x*{b}",
            "dzdt_val": float(dzdt),
        }

    def _poly_chain(self, difficulty: int) -> tuple[str, dict]:
        """Generate chain rule for z = x^2*y, x = at, y = t^2.

        Args:
            difficulty: Controls coefficient a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        t0 = self._rng.randint(1, 3)
        x0 = a * t0
        y0 = t0 * t0
        dzdx = 2 * x0 * y0
        dzdy = x0 * x0
        dxdt = a
        dydt = 2 * t0
        dzdt = dzdx * dxdt + dzdy * dydt
        problem = f"z = x^2 y, x = {a}t, y = t^2"
        return problem, {
            "func_type": "poly", "t0": t0,
            "dzdx": "2xy", "dzdy": "x^2",
            "dxdt": f"{a}", "dydt": "2t",
            "dzdt_expr": f"2xy*{a} + x^2*2t",
            "dzdt_val": float(dzdt),
        }

    def _trig_chain(self, difficulty: int) -> tuple[str, dict]:
        """Generate chain rule for z = x^2+y^2, x=cos(t), y=sin(t).

        dz/dt = 2x*(-sin(t)) + 2y*(cos(t)) = 0.

        Args:
            difficulty: Controls evaluation point.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        t0 = round(self._rng.choice([0.5, 1.0, math.pi / 4]), 4)
        x0 = math.cos(t0)
        y0 = math.sin(t0)
        dzdt = 2 * x0 * (-math.sin(t0)) + 2 * y0 * math.cos(t0)
        problem = "z = x^2+y^2, x = \\cos(t), y = \\sin(t)"
        return problem, {
            "func_type": "trig", "t0": t0,
            "dzdx": "2x", "dzdy": "2y",
            "dxdt": "-\\sin(t)", "dydt": "\\cos(t)",
            "dzdt_expr": "2x(-\\sin(t)) + 2y(\\cos(t))",
            "dzdt_val": dzdt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multivariable chain rule steps.

        Args:
            data: Solution data with partial derivatives.

        Returns:
            Steps showing partials, chain rule, and evaluation.
        """
        return [
            f"dz/dx={data['dzdx']}, dz/dy={data['dzdy']}",
            f"dx/dt={data['dxdt']}, dy/dt={data['dydt']}",
            f"dz/dt = {data['dzdt_expr']}",
            f"at t={_fmt(data['t0'])}: dz/dt = {_fmt(data['dzdt_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the dz/dt value.

        Args:
            data: Solution data.

        Returns:
            Formatted dz/dt.
        """
        return f"dz/dt = {_fmt(data['dzdt_val'])}"


# ── 12. Double integral (tier 6) ─────────────────────────────────────


@register
class DoubleIntegralGenerator(StepGenerator):
    """Evaluate a double integral over a rectangular or triangular region.

    Computes integral integral f(x,y) dA by evaluating iterated integrals.

    Input format:
        ``evaluate double integral``

    Target format:
        ``int_0^1 int_0^2 xy dx dy <step>
        inner: int_0^2 xy dx = y*[x^2/2]_0^2 = 2y
        <step> outer: int_0^1 2y dy = [y^2]_0^1 = 1``

    Difficulty scaling:
        Difficulty 1-3: f = c over rectangle.
        Difficulty 4-6: f = xy over rectangle.
        Difficulty 7-8: f = x+y over triangle.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "double_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand and region.

        Returns:
            Natural language description.
        """
        return "evaluate double integral"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a double integral problem.

        Args:
            difficulty: Controls function and region.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._const_rect(difficulty)
        if difficulty <= 6:
            return self._xy_rect(difficulty)
        return self._triangle_region(difficulty)

    def _const_rect(self, difficulty: int) -> tuple[str, dict]:
        """Generate double integral of constant over rectangle.

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(1, 5)
        ax, bx = 0, self._rng.randint(1, 4)
        ay, by = 0, self._rng.randint(1, 4)
        value = float(c * (bx - ax) * (by - ay))
        problem = (f"\\int_{{{ay}}}^{{{by}}} \\int_{{{ax}}}^{{{bx}}} "
                   f"{c} \\, dx \\, dy")
        return problem, {
            "region": "rectangle", "f": f"{c}",
            "inner": f"{c}*({bx}-{ax}) = {c*(bx-ax)}",
            "outer": f"{c*(bx-ax)}*({by}-{ay}) = {_fmt(value)}",
            "value": value,
        }

    def _xy_rect(self, difficulty: int) -> tuple[str, dict]:
        """Generate double integral of xy over rectangle.

        int_0^b int_0^a xy dx dy = (a^2/2)*(b^2/2).

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        value = (a * a / 2.0) * (b * b / 2.0)
        problem = (f"\\int_0^{{{b}}} \\int_0^{{{a}}} xy \\, dx \\, dy")
        return problem, {
            "region": "rectangle", "f": "xy",
            "inner": f"y*[x^2/2]_0^{a} = {a*a/2.0}y",
            "outer": f"{a*a/2.0}*[y^2/2]_0^{b} = {_fmt(value)}",
            "value": value,
        }

    def _triangle_region(self, difficulty: int) -> tuple[str, dict]:
        """Generate double integral of (x+y) over triangle 0<=x<=a, 0<=y<=x.

        int_0^a int_0^x (x+y) dy dx = int_0^a [xy+y^2/2]_0^x dx
        = int_0^a (3x^2/2) dx = a^3/2.

        Args:
            difficulty: Controls bound a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        value = a ** 3 / 2.0
        problem = (f"\\int_0^{{{a}}} \\int_0^x (x+y) \\, dy \\, dx")
        return problem, {
            "region": "triangle 0<=y<=x", "f": "x+y",
            "inner": f"[xy+y^2/2]_0^x = 3x^2/2",
            "outer": f"[x^3/2]_0^{a} = {_fmt(value)}",
            "value": value,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate double integral evaluation steps.

        Args:
            data: Solution data with inner and outer integrals.

        Returns:
            Steps showing iterated integration.
        """
        return [
            f"f(x,y) = {data['f']}, region: {data['region']}",
            f"inner integral: {data['inner']}",
            f"outer integral: {data['outer']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the double integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted value.
        """
        return _fmt(data["value"])


# ── 13. Triple integral (tier 6) ─────────────────────────────────────


@register
class TripleIntegralGenerator(StepGenerator):
    """Evaluate a triple integral over a box region.

    Computes integral integral integral f(x,y,z) dV by evaluating
    iterated integrals from innermost to outermost.

    Input format:
        ``evaluate triple integral over box region``

    Target format:
        ``int_0^1 int_0^2 int_0^3 xyz dx dy dz <step>
        inner: int_0^3 xyz dx = yz*9/2
        <step> middle: int_0^2 9yz/2 dy = 9z/2*2 = 9z
        <step> outer: int_0^1 9z dz = 9/2``

    Difficulty scaling:
        Difficulty 1-3: f = c over box [0,a]x[0,b]x[0,c].
        Difficulty 4-6: f = xyz over box.
        Difficulty 7-8: f = x^2 + y + z over box.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "triple_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand and region.

        Returns:
            Natural language description.
        """
        return "evaluate triple integral over box region"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a triple integral problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._const_box(difficulty)
        if difficulty <= 6:
            return self._xyz_box(difficulty)
        return self._mixed_box(difficulty)

    def _const_box(self, difficulty: int) -> tuple[str, dict]:
        """Generate triple integral of constant over box.

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(1, 5)
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        d = self._rng.randint(1, 3)
        value = float(c * a * b * d)
        problem = (f"\\int_0^{{{d}}} \\int_0^{{{b}}} "
                   f"\\int_0^{{{a}}} {c} \\, dx \\, dy \\, dz")
        return problem, {
            "f": f"{c}", "a": a, "b": b, "d": d,
            "inner": f"{c}*{a} = {c*a}",
            "middle": f"{c*a}*{b} = {c*a*b}",
            "outer": f"{c*a*b}*{d} = {_fmt(value)}",
            "value": value,
        }

    def _xyz_box(self, difficulty: int) -> tuple[str, dict]:
        """Generate triple integral of xyz over box.

        int_0^a x dx * int_0^b y dy * int_0^d z dz = (a^2/2)(b^2/2)(d^2/2).

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        d = self._rng.randint(1, 3)
        value = (a ** 2 / 2.0) * (b ** 2 / 2.0) * (d ** 2 / 2.0)
        problem = (f"\\int_0^{{{d}}} \\int_0^{{{b}}} "
                   f"\\int_0^{{{a}}} xyz \\, dx \\, dy \\, dz")
        return problem, {
            "f": "xyz", "a": a, "b": b, "d": d,
            "inner": f"yz*{a**2}/2",
            "middle": f"z*{a**2}/2*{b**2}/2",
            "outer": f"{_fmt(value)}",
            "value": value,
        }

    def _mixed_box(self, difficulty: int) -> tuple[str, dict]:
        """Generate triple integral of (x^2+y+z) over box.

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 2)
        b = self._rng.randint(1, 2)
        d = self._rng.randint(1, 2)
        # int x^2 dx from 0 to a = a^3/3
        # int y dy from 0 to b = b^2/2
        # int z dz from 0 to d = d^2/2
        # int (x^2+y+z) over box = b*d*a^3/3 + a*d*b^2/2 + a*b*d^2/2
        value = (b * d * a ** 3 / 3.0
                 + a * d * b ** 2 / 2.0
                 + a * b * d ** 2 / 2.0)
        problem = (f"\\int_0^{{{d}}} \\int_0^{{{b}}} "
                   f"\\int_0^{{{a}}} (x^2+y+z) \\, dx \\, dy \\, dz")
        return problem, {
            "f": "x^2+y+z", "a": a, "b": b, "d": d,
            "inner": f"[x^3/3+yx+zx]_0^{a}",
            "middle": f"integrate over y from 0 to {b}",
            "outer": f"integrate over z from 0 to {d}",
            "value": value,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate triple integral evaluation steps.

        Args:
            data: Solution data with iterated results.

        Returns:
            Steps showing innermost to outermost integration.
        """
        return [
            f"f = {data['f']} over [0,{data['a']}]x[0,{data['b']}]x[0,{data['d']}]",
            f"inner: {data['inner']}",
            f"middle: {data['middle']}",
            f"outer: {data['outer']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the triple integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted value.
        """
        return _fmt(data["value"])


# ── 14. Line integral (tier 6) ───────────────────────────────────────


@register
class LineIntegralGenerator(StepGenerator):
    """Evaluate a line integral of a vector field along a parametric curve.

    Computes integral_C F.dr = integral F(r(t)).r'(t) dt for a
    vector field F along a parametric path r(t).

    Input format:
        ``evaluate line integral of vector field``

    Target format:
        ``F = (y, x), r(t) = (t, t^2) on [0,1] <step>
        F(r(t)) = (t^2, t), r'(t) = (1, 2t)
        <step> F.r' = t^2 + 2t^2 = 3t^2
        <step> int_0^1 3t^2 dt = 1``

    Difficulty scaling:
        Difficulty 1-3: F = (a, b), straight line path.
        Difficulty 4-6: F = (y, x), parabolic path.
        Difficulty 7-8: F = (x^2, xy), general path.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "line_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector field and path complexity.

        Returns:
            Natural language description.
        """
        return "evaluate line integral of vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a line integral problem.

        Args:
            difficulty: Controls field and path type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._const_line(difficulty)
        if difficulty <= 6:
            return self._yx_field(difficulty)
        return self._poly_field(difficulty)

    def _const_line(self, difficulty: int) -> tuple[str, dict]:
        """Generate line integral of constant field along segment.

        F = (a, b), r(t) = (t, ct) for t in [0, d].
        int = (a + bc)*d.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        c = self._rng.randint(1, 3)
        d = self._rng.randint(1, 3)
        # r'(t) = (1, c), F.r' = a + bc
        value = float((a + b * c) * d)
        problem = f"F=({a},{b}), r(t)=(t,{c}t), t in [0,{d}]"
        return problem, {
            "field_type": "const",
            "f_at_r": f"({a},{b})", "r_prime": f"(1,{c})",
            "dot": f"{a}+{b*c} = {a+b*c}",
            "integral": f"{a+b*c}*{d}",
            "value": value,
        }

    def _yx_field(self, difficulty: int) -> tuple[str, dict]:
        """Generate line integral of F=(y,x) along r(t)=(t,t^2), [0,a].

        F(r) = (t^2, t), r'(t) = (1, 2t).
        F.r' = t^2 + 2t^2 = 3t^2. int = a^3.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        value = float(a ** 3)
        problem = f"F=(y,x), r(t)=(t,t^2), t in [0,{a}]"
        return problem, {
            "field_type": "yx",
            "f_at_r": "(t^2, t)", "r_prime": "(1, 2t)",
            "dot": "t^2 + 2t^2 = 3t^2",
            "integral": f"[t^3]_0^{a}",
            "value": value,
        }

    def _poly_field(self, difficulty: int) -> tuple[str, dict]:
        """Generate line integral of F=(x,y) along r(t)=(t^2,t), [0,a].

        F(r) = (t^2, t), r'(t) = (2t, 1).
        F.r' = 2t^3 + t. int_0^a = a^4/2 + a^2/2.

        Args:
            difficulty: Controls upper bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        value = a ** 4 / 2.0 + a ** 2 / 2.0
        problem = f"F=(x,y), r(t)=(t^2,t), t in [0,{a}]"
        return problem, {
            "field_type": "poly",
            "f_at_r": "(t^2, t)", "r_prime": "(2t, 1)",
            "dot": "2t^3 + t",
            "integral": f"[t^4/2+t^2/2]_0^{a}",
            "value": value,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate line integral computation steps.

        Args:
            data: Solution data with field, path, and dot product.

        Returns:
            Steps showing substitution, dot product, and integration.
        """
        return [
            f"F(r(t)) = {data['f_at_r']}, r'(t) = {data['r_prime']}",
            f"F.r' = {data['dot']}",
            f"int = {data['integral']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the line integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted value.
        """
        return _fmt(data["value"])


# ── 15. Green's theorem (tier 6) ─────────────────────────────────────


@register
class GreensTheoremGenerator(StepGenerator):
    """Apply Green's theorem to convert a line integral to a double integral.

    Uses integral_C (P dx + Q dy) = integral integral (dQ/dx - dP/dy) dA
    to convert a circulation integral around a closed curve into a
    double integral over the enclosed region.

    Input format:
        ``apply Green's theorem``

    Target format:
        ``int_C (x^2 dx + xy dy), C = boundary of [0,a]x[0,b]
        <step> P = x^2, Q = xy
        <step> dQ/dx - dP/dy = y - 0 = y
        <step> int_0^b int_0^a y dx dy = a*b^2/2``

    Difficulty scaling:
        Difficulty 1-3: P = ax, Q = by, rectangle.
        Difficulty 4-6: P = x^2, Q = xy, rectangle.
        Difficulty 7-8: P = -y^2, Q = x^2, disk of radius r.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "greens_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls field and region complexity.

        Returns:
            Natural language description.
        """
        return "apply Green's theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Green's theorem problem.

        Args:
            difficulty: Controls field and region type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_rect(difficulty)
        if difficulty <= 6:
            return self._quad_rect(difficulty)
        return self._disk_region(difficulty)

    def _linear_rect(self, difficulty: int) -> tuple[str, dict]:
        """Generate Green's theorem for P=0, Q=x over rectangle.

        dQ/dx - dP/dy = 1. Double integral = area = a*b.

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        value = float(a * b)
        problem = (f"\\oint_C (0 \\, dx + x \\, dy), "
                   f"C = \\partial[0,{a}]\\times[0,{b}]")
        return problem, {
            "P": "0", "Q": "x",
            "dQdx": "1", "dPdy": "0",
            "curl": "1",
            "region": f"[0,{a}]x[0,{b}]",
            "double_int": f"int int 1 dA = {a}*{b}",
            "value": value,
        }

    def _quad_rect(self, difficulty: int) -> tuple[str, dict]:
        """Generate Green's theorem for P=x^2, Q=xy over rectangle.

        dQ/dx = y, dP/dy = 0, curl = y.
        int int y dA over [0,a]x[0,b] = a*b^2/2.

        Args:
            difficulty: Controls bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        value = a * b * b / 2.0
        problem = (f"\\oint_C (x^2 \\, dx + xy \\, dy), "
                   f"C = \\partial[0,{a}]\\times[0,{b}]")
        return problem, {
            "P": "x^2", "Q": "xy",
            "dQdx": "y", "dPdy": "0",
            "curl": "y",
            "region": f"[0,{a}]x[0,{b}]",
            "double_int": f"int_0^{b} int_0^{a} y dx dy = {a}*{b}^2/2",
            "value": value,
        }

    def _disk_region(self, difficulty: int) -> tuple[str, dict]:
        """Generate Green's theorem for P=-y, Q=x over disk of radius r.

        dQ/dx - dP/dy = 1 + 1 = 2.
        int int 2 dA = 2*pi*r^2.

        Args:
            difficulty: Controls radius.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r = self._rng.randint(1, 4)
        value = 2.0 * math.pi * r * r
        problem = (f"\\oint_C (-y \\, dx + x \\, dy), "
                   f"C = circle r={r}")
        return problem, {
            "P": "-y", "Q": "x",
            "dQdx": "1", "dPdy": "-1",
            "curl": "2",
            "region": f"disk r={r}",
            "double_int": f"2*pi*{r}^2",
            "value": value,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Green's theorem steps.

        Args:
            data: Solution data with curl and double integral.

        Returns:
            Steps showing P, Q, curl, and double integral.
        """
        return [
            f"P={data['P']}, Q={data['Q']}",
            f"dQ/dx={data['dQdx']}, dP/dy={data['dPdy']}",
            f"curl = dQ/dx - dP/dy = {data['curl']}",
            f"double integral: {data['double_int']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the line integral value via Green's theorem.

        Args:
            data: Solution data.

        Returns:
            Formatted value.
        """
        return _fmt(data["value"])
