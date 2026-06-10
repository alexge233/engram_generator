"""Differential geometry generators for tiers 6-7.

Provides generators for curvature of parametric curves, arc length
computation, tangent/normal vectors, Christoffel symbols, geodesic
equations, and Gaussian curvature. Each generator produces step-by-step
solutions with LaTeX formatting suitable for training sequence models.
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


# ── Helper classes ────────────────────────────────────────────────────


class ParametricCurve:
    """A parametric curve (x(t), y(t)) with analytic derivatives.

    Supports polynomial and trigonometric curve families used by the
    curvature and arc length generators. Provides evaluation of position,
    first derivative, and second derivative at a given parameter value.

    Attributes:
        name: Human-readable curve name.
        kind: Curve family identifier.
        coeffs: Numeric coefficients controlling the curve shape.
    """

    def __init__(self, kind: str, coeffs: tuple) -> None:
        """Initialise the parametric curve.

        Args:
            kind: Curve family ('poly2', 'poly3', 'circle', 'ellipse',
                  'cycloid', 'lissajous').
            coeffs: Numeric parameters specific to the curve family.
        """
        self._kind = kind
        self._coeffs = coeffs

    @property
    def kind(self) -> str:
        """Return the curve family identifier."""
        return self._kind

    @property
    def coeffs(self) -> tuple:
        """Return the curve coefficients."""
        return self._coeffs

    def latex(self) -> str:
        """Format the curve as a LaTeX string.

        Returns:
            LaTeX representation of the parametric curve.
        """
        if self._kind == "poly2":
            a, b = self._coeffs
            return f"(t, {a}t^2+{b}t)"
        if self._kind == "poly3":
            a, b = self._coeffs
            return f"({a}t, {b}t^3)"
        if self._kind == "circle":
            r = self._coeffs[0]
            return f"({r}\\cos t, {r}\\sin t)"
        if self._kind == "ellipse":
            a, b = self._coeffs
            return f"({a}\\cos t, {b}\\sin t)"
        if self._kind == "cycloid":
            r = self._coeffs[0]
            return f"({r}(t-\\sin t), {r}(1-\\cos t))"
        # lissajous
        a, b, n = self._coeffs
        return f"({a}\\cos t, {b}\\sin({n}t))"

    def position(self, t: float) -> tuple[float, float]:
        """Evaluate (x(t), y(t)).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (x, y).
        """
        if self._kind == "poly2":
            a, b = self._coeffs
            return t, a * t ** 2 + b * t
        if self._kind == "poly3":
            a, b = self._coeffs
            return a * t, b * t ** 3
        if self._kind == "circle":
            r = self._coeffs[0]
            return r * math.cos(t), r * math.sin(t)
        if self._kind == "ellipse":
            a, b = self._coeffs
            return a * math.cos(t), b * math.sin(t)
        if self._kind == "cycloid":
            r = self._coeffs[0]
            return r * (t - math.sin(t)), r * (1 - math.cos(t))
        # lissajous
        a, b, n = self._coeffs
        return a * math.cos(t), b * math.sin(n * t)

    def velocity(self, t: float) -> tuple[float, float]:
        """Evaluate (x'(t), y'(t)).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (dx/dt, dy/dt).
        """
        if self._kind == "poly2":
            a, b = self._coeffs
            return 1.0, 2 * a * t + b
        if self._kind == "poly3":
            a, b = self._coeffs
            return float(a), 3 * b * t ** 2
        if self._kind == "circle":
            r = self._coeffs[0]
            return -r * math.sin(t), r * math.cos(t)
        if self._kind == "ellipse":
            a, b = self._coeffs
            return -a * math.sin(t), b * math.cos(t)
        if self._kind == "cycloid":
            r = self._coeffs[0]
            return r * (1 - math.cos(t)), r * math.sin(t)
        # lissajous
        a, b, n = self._coeffs
        return -a * math.sin(t), b * n * math.cos(n * t)

    def acceleration(self, t: float) -> tuple[float, float]:
        """Evaluate (x''(t), y''(t)).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (d^2x/dt^2, d^2y/dt^2).
        """
        if self._kind == "poly2":
            a, _ = self._coeffs
            return 0.0, 2.0 * a
        if self._kind == "poly3":
            _, b = self._coeffs
            return 0.0, 6 * b * t
        if self._kind == "circle":
            r = self._coeffs[0]
            return -r * math.cos(t), -r * math.sin(t)
        if self._kind == "ellipse":
            a, b = self._coeffs
            return -a * math.cos(t), -b * math.sin(t)
        if self._kind == "cycloid":
            r = self._coeffs[0]
            return r * math.sin(t), r * math.cos(t)
        # lissajous
        a, b, n = self._coeffs
        return -a * math.cos(t), -b * n ** 2 * math.sin(n * t)


class DiagonalMetric:
    """A 2D diagonal metric tensor g = diag(g_11, g_22).

    Each diagonal entry is a monomial in (x1, x2): c * x1^p * x2^q.
    This simple form allows analytic Christoffel symbol computation
    for pedagogical differential geometry problems.

    Attributes:
        g11: Tuple (c, p, q) for g_11 = c * x1^p * x2^q.
        g22: Tuple (c, p, q) for g_22 = c * x1^p * x2^q.
    """

    def __init__(self, g11: tuple[float, int, int],
                 g22: tuple[float, int, int]) -> None:
        """Initialise the diagonal metric.

        Args:
            g11: Coefficients (c, p, q) for g_11 = c * x1^p * x2^q.
            g22: Coefficients (c, p, q) for g_22 = c * x1^p * x2^q.
        """
        self._g11 = g11
        self._g22 = g22

    @property
    def g11(self) -> tuple[float, int, int]:
        """Return g_11 monomial coefficients."""
        return self._g11

    @property
    def g22(self) -> tuple[float, int, int]:
        """Return g_22 monomial coefficients."""
        return self._g22

    def eval_component(self, spec: tuple[float, int, int],
                       x1: float, x2: float) -> float:
        """Evaluate a monomial c * x1^p * x2^q.

        Args:
            spec: Tuple of (c, p, q).
            x1: First coordinate value.
            x2: Second coordinate value.

        Returns:
            Value of the monomial.
        """
        c, p, q = spec
        return c * (x1 ** p) * (x2 ** q)

    def eval_g(self, x1: float, x2: float) -> tuple[float, float]:
        """Evaluate (g_11, g_22) at a point.

        Args:
            x1: First coordinate.
            x2: Second coordinate.

        Returns:
            Tuple of (g_11, g_22) values.
        """
        return (self.eval_component(self._g11, x1, x2),
                self.eval_component(self._g22, x1, x2))

    def partial(self, spec: tuple[float, int, int],
                var: int, x1: float, x2: float) -> float:
        """Compute partial derivative of a monomial with respect to x_var.

        Args:
            spec: Monomial (c, p, q).
            var: Variable index (1 or 2).
            x1: First coordinate.
            x2: Second coordinate.

        Returns:
            Value of the partial derivative.
        """
        c, p, q = spec
        if var == 1:
            if p == 0:
                return 0.0
            return c * p * (x1 ** (p - 1)) * (x2 ** q)
        # var == 2
        if q == 0:
            return 0.0
        return c * (x1 ** p) * q * (x2 ** (q - 1))

    def latex(self) -> str:
        """Format the metric as a LaTeX string.

        Returns:
            LaTeX representation of the diagonal metric.
        """
        return (f"ds^2 = {self._mono_latex(self._g11)}(dx^1)^2 "
                f"+ {self._mono_latex(self._g22)}(dx^2)^2")

    def _mono_latex(self, spec: tuple[float, int, int]) -> str:
        """Format a monomial as LaTeX.

        Args:
            spec: Monomial (c, p, q).

        Returns:
            LaTeX string for the monomial.
        """
        c, p, q = spec
        parts: list[str] = []
        cs = _fmt(c)
        if cs != "1" or (p == 0 and q == 0):
            parts.append(cs)
        if p == 1:
            parts.append("x^1")
        elif p > 1:
            parts.append(f"(x^1)^{{{p}}}")
        if q == 1:
            parts.append("x^2")
        elif q > 1:
            parts.append(f"(x^2)^{{{q}}}")
        return "".join(parts) if parts else "1"


# ── 1. Curvature 2D (tier 6) ─────────────────────────────────────────


@register
class Curvature2DGenerator(StepGenerator):
    """Compute curvature of a parametric plane curve at a given parameter.

    Uses the formula kappa = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2) for
    parametric curves including parabolas, circles, ellipses, and
    cycloids. Each sample specifies the curve, evaluates derivatives at
    a random parameter value, and computes curvature step by step.

    Input format:
        ``compute curvature of parametric curve``

    Target format:
        ``r(t)=(t, 2t^2+t) at t=1 <step> x'=1, y'=5 <step>
        x''=0, y''=4 <step> num=|1*4-5*0|=4 <step>
        den=(1+25)^{3/2}=132.574 <step> kappa=0.0302``

    Difficulty scaling:
        Difficulty 1-3: simple parabolas (t, at^2+bt).
        Difficulty 4-6: circles and ellipses.
        Difficulty 7-8: cycloids and Lissajous curves.

    Prerequisites:
        derivative (tier 2), chain_rule (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "curvature_2d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "chain_rule"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Natural language description.
        """
        return "compute curvature of parametric curve"

    def _choose_curve(self, difficulty: int) -> ParametricCurve:
        """Select a parametric curve appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A ParametricCurve instance.
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(0, 2)
            return ParametricCurve("poly2", (a, b))
        if difficulty <= 6:
            if self._rng.random() < 0.5:
                r = self._rng.randint(1, 5)
                return ParametricCurve("circle", (r,))
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 4)
            if a == b:
                b = a + 1
            return ParametricCurve("ellipse", (a, b))
        # difficulty 7-8
        if self._rng.random() < 0.5:
            r = self._rng.randint(1, 3)
            return ParametricCurve("cycloid", (r,))
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        n = self._rng.randint(2, 3)
        return ParametricCurve("lissajous", (a, b, n))

    def _choose_t(self, curve: ParametricCurve) -> float:
        """Choose a suitable parameter value avoiding singularities.

        Args:
            curve: The parametric curve.

        Returns:
            Parameter value t.
        """
        if curve.kind in ("circle", "ellipse", "lissajous"):
            choices = [0.5, 1.0, 1.5, 2.0, 2.5]
            return self._rng.choice(choices)
        if curve.kind == "cycloid":
            choices = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
            return self._rng.choice(choices)
        return float(self._rng.randint(1, 4))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a curvature computation problem.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        curve = self._choose_curve(difficulty)
        t = self._choose_t(curve)

        xp, yp = curve.velocity(t)
        xpp, ypp = curve.acceleration(t)

        numerator = abs(xp * ypp - yp * xpp)
        speed_sq = xp ** 2 + yp ** 2
        denominator = speed_sq ** 1.5
        kappa = numerator / denominator if denominator > 1e-12 else 0.0

        problem = f"\\kappa(t={_fmt(t)}), r(t)={curve.latex()}"
        return problem, {
            "curve": curve, "t": t,
            "xp": xp, "yp": yp, "xpp": xpp, "ypp": ypp,
            "numerator": numerator, "speed_sq": speed_sq,
            "denominator": denominator, "kappa": kappa,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate curvature computation steps.

        Args:
            data: Solution data with derivatives and curvature.

        Returns:
            Steps showing derivative evaluation and kappa computation.
        """
        return [
            f"x'={_fmt(data['xp'])}, y'={_fmt(data['yp'])}",
            f"x''={_fmt(data['xpp'])}, y''={_fmt(data['ypp'])}",
            f"|x'y''-y'x''|={_fmt(data['numerator'])}",
            f"(x'^2+y'^2)^{{3/2}}={_fmt(data['denominator'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the curvature value.

        Args:
            data: Solution data.

        Returns:
            Formatted curvature string.
        """
        return f"kappa={_fmt(data['kappa'])}"


# ── 2. Arc length parametric (tier 6) ────────────────────────────────


@register
class ArcLengthParamGenerator(StepGenerator):
    """Compute arc length of a parametric curve over an interval.

    Uses L = integral_a^b sqrt(x'^2 + y'^2) dt, evaluated via
    numerical quadrature (Simpson's rule) for general curves, or
    analytically for circles and simple polynomials.

    Input format:
        ``compute arc length of parametric curve``

    Target format:
        ``L = int_0^{pi} sqrt(x'^2+y'^2) dt, r(t)=(3cos t, 3sin t)
        <step> x'=-3sin t, y'=3cos t <step>
        sqrt(x'^2+y'^2)=3 <step> L=3*pi=9.4248``

    Difficulty scaling:
        Difficulty 1-3: circles (exact result).
        Difficulty 4-6: ellipses, simple polynomial curves.
        Difficulty 7-8: cycloids, Lissajous curves.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "arc_length_param"

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
        return "compute arc length of parametric curve"

    def _choose_curve_and_bounds(self, difficulty: int
                                 ) -> tuple[ParametricCurve, float, float]:
        """Select a curve and integration bounds for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (curve, t_start, t_end).
        """
        if difficulty <= 3:
            r = self._rng.randint(1, 5)
            curve = ParametricCurve("circle", (r,))
            end = self._rng.choice([math.pi / 2, math.pi, 2 * math.pi])
            return curve, 0.0, end
        if difficulty <= 6:
            if self._rng.random() < 0.5:
                a = self._rng.randint(1, 3)
                b = self._rng.randint(0, 2)
                curve = ParametricCurve("poly2", (a, b))
                return curve, 0.0, float(self._rng.randint(1, 3))
            a = self._rng.randint(2, 4)
            b = self._rng.randint(1, 3)
            if a == b:
                b = a + 1
            curve = ParametricCurve("ellipse", (a, b))
            return curve, 0.0, math.pi / 2
        # difficulty 7-8
        if self._rng.random() < 0.5:
            r = self._rng.randint(1, 3)
            curve = ParametricCurve("cycloid", (r,))
            return curve, 0.0, 2 * math.pi
        a = self._rng.randint(1, 3)
        b = self._rng.choice([1, 2])
        curve = ParametricCurve("poly3", (a, b))
        return curve, 0.0, float(self._rng.randint(1, 2))

    def _simpson(self, curve: ParametricCurve,
                 t0: float, t1: float, n: int = 100) -> float:
        """Compute arc length numerically using Simpson's rule.

        Args:
            curve: The parametric curve.
            t0: Start parameter.
            t1: End parameter.
            n: Number of subintervals (must be even).

        Returns:
            Approximate arc length.
        """
        h = (t1 - t0) / n
        total = 0.0
        for i in range(n + 1):
            t = t0 + i * h
            xp, yp = curve.velocity(t)
            speed = math.sqrt(xp ** 2 + yp ** 2)
            if i == 0 or i == n:
                total += speed
            elif i % 2 == 1:
                total += 4 * speed
            else:
                total += 2 * speed
        return total * h / 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an arc length computation problem.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        curve, t0, t1 = self._choose_curve_and_bounds(difficulty)
        arc_length = self._simpson(curve, t0, t1)

        xp0, yp0 = curve.velocity(t0)
        speed0 = math.sqrt(xp0 ** 2 + yp0 ** 2)

        problem = (f"L=\\int_{{{_fmt(t0)}}}^{{{_fmt(t1)}}} "
                   f"\\sqrt{{x'^2+y'^2}}\\,dt, r(t)={curve.latex()}")
        return problem, {
            "curve": curve, "t0": t0, "t1": t1,
            "xp0": xp0, "yp0": yp0, "speed0": speed0,
            "arc_length": arc_length,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate arc length computation steps.

        Args:
            data: Solution data with derivatives and arc length.

        Returns:
            Steps showing speed computation and integration.
        """
        curve = data["curve"]
        steps = [
            f"r(t)={curve.latex()}, t in [{_fmt(data['t0'])},{_fmt(data['t1'])}]",
            f"x'({_fmt(data['t0'])})={_fmt(data['xp0'])}, "
            f"y'({_fmt(data['t0'])})={_fmt(data['yp0'])}",
            f"|r'({_fmt(data['t0'])})|={_fmt(data['speed0'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the arc length value.

        Args:
            data: Solution data.

        Returns:
            Formatted arc length string.
        """
        return f"L={_fmt(data['arc_length'])}"


# ── 3. Tangent and normal vectors (tier 6) ────────────────────────────


@register
class TangentNormalGenerator(StepGenerator):
    """Find unit tangent T and unit normal N for a parametric curve.

    Computes T = r'/|r'| and N by rotating T by 90 degrees (in 2D,
    N = (-T_y, T_x) choosing the inward-pointing normal).

    Input format:
        ``find unit tangent and normal vectors``

    Target format:
        ``r(t)=(2cos t, 2sin t) at t=1 <step> r'=(-1.6829, 1.0806)
        <step> |r'|=2 <step> T=(-0.8415, 0.5403)
        <step> N=(-0.5403, -0.8415)``

    Difficulty scaling:
        Difficulty 1-3: simple polynomial curves.
        Difficulty 4-6: circles and ellipses.
        Difficulty 7-8: cycloids and Lissajous curves.

    Prerequisites:
        gradient (tier 5), vector_norm (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tangent_normal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gradient", "vector_norm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Natural language description.
        """
        return "find unit tangent and normal vectors"

    def _choose_curve(self, difficulty: int) -> ParametricCurve:
        """Select a parametric curve for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A ParametricCurve instance.
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(0, 2)
            return ParametricCurve("poly2", (a, b))
        if difficulty <= 6:
            if self._rng.random() < 0.5:
                r = self._rng.randint(1, 5)
                return ParametricCurve("circle", (r,))
            a = self._rng.randint(2, 4)
            b = self._rng.randint(1, 3)
            if a == b:
                b = a + 1
            return ParametricCurve("ellipse", (a, b))
        if self._rng.random() < 0.5:
            r = self._rng.randint(1, 3)
            return ParametricCurve("cycloid", (r,))
        a = self._rng.randint(1, 3)
        b = self._rng.randint(1, 3)
        n = self._rng.randint(2, 3)
        return ParametricCurve("lissajous", (a, b, n))

    def _choose_t(self, curve: ParametricCurve) -> float:
        """Choose a parameter value avoiding zero-speed points.

        Args:
            curve: The parametric curve.

        Returns:
            Parameter value t.
        """
        if curve.kind in ("circle", "ellipse", "lissajous"):
            return self._rng.choice([0.5, 1.0, 1.5, 2.0])
        if curve.kind == "cycloid":
            return self._rng.choice([1.0, 1.5, 2.0, 2.5, 3.0])
        return float(self._rng.randint(1, 4))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tangent/normal vector problem.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        curve = self._choose_curve(difficulty)
        t = self._choose_t(curve)

        xp, yp = curve.velocity(t)
        speed = math.sqrt(xp ** 2 + yp ** 2)
        tx = xp / speed
        ty = yp / speed
        # Unit normal: rotate T by -90 degrees (inward for convex curves)
        nx = -ty
        ny = tx

        problem = f"T,N: r(t)={curve.latex()}, t={_fmt(t)}"
        return problem, {
            "curve": curve, "t": t,
            "xp": xp, "yp": yp, "speed": speed,
            "tx": tx, "ty": ty, "nx": nx, "ny": ny,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tangent/normal computation steps.

        Args:
            data: Solution data with velocity and unit vectors.

        Returns:
            Steps showing velocity, speed, T, and N.
        """
        return [
            f"r'=({_fmt(data['xp'])}, {_fmt(data['yp'])})",
            f"|r'|={_fmt(data['speed'])}",
            f"T=({_fmt(data['tx'])}, {_fmt(data['ty'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the unit tangent and normal vectors.

        Args:
            data: Solution data.

        Returns:
            Formatted T and N vectors.
        """
        return (f"T=({_fmt(data['tx'])},{_fmt(data['ty'])}), "
                f"N=({_fmt(data['nx'])},{_fmt(data['ny'])})")


# ── 4. Christoffel symbol (tier 7) ───────────────────────────────────


@register
class ChristoffelSymbolGenerator(StepGenerator):
    """Compute Christoffel symbols for a 2D diagonal metric.

    Uses Gamma^k_{ij} = 0.5 * g^{kl} (dg_{il}/dx^j + dg_{jl}/dx^i
    - dg_{ij}/dx^l) specialised to a diagonal metric where g^{kk} =
    1/g_{kk}. Evaluates at a specific coordinate point.

    Input format:
        ``compute Christoffel symbols for 2D diagonal metric``

    Target format:
        ``ds^2 = x^1(dx^1)^2 + (x^2)^2(dx^2)^2 at (2,1)
        <step> g_11=2, g_22=1 <step> dg_11/dx^1=1, ...
        <step> Gamma^1_{11}=0.25, ...``

    Difficulty scaling:
        Difficulty 1-3: constant or linear metric components.
        Difficulty 4-6: quadratic metric components.
        Difficulty 7-8: mixed-power metric components.

    Prerequisites:
        partial_derivative (tier 4), matrix_inverse (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "christoffel_symbol"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative", "matrix_inverse"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls metric complexity.

        Returns:
            Natural language description.
        """
        return "compute Christoffel symbols for 2D diagonal metric"

    def _choose_metric(self, difficulty: int) -> DiagonalMetric:
        """Select a diagonal metric appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A DiagonalMetric instance.
        """
        if difficulty <= 3:
            # Simple metrics: constants or linear
            kind = self._rng.choice(["const", "linear"])
            if kind == "const":
                c1 = float(self._rng.randint(1, 4))
                c2 = float(self._rng.randint(1, 4))
                return DiagonalMetric((c1, 0, 0), (c2, 0, 0))
            c1 = float(self._rng.randint(1, 3))
            c2 = float(self._rng.randint(1, 3))
            return DiagonalMetric((c1, 1, 0), (c2, 0, 1))
        if difficulty <= 6:
            c1 = float(self._rng.randint(1, 3))
            c2 = float(self._rng.randint(1, 3))
            p1 = self._rng.randint(1, 2)
            p2 = self._rng.randint(1, 2)
            return DiagonalMetric((c1, p1, 0), (c2, 0, p2))
        # difficulty 7-8: mixed powers
        c1 = float(self._rng.randint(1, 3))
        c2 = float(self._rng.randint(1, 3))
        p1 = self._rng.randint(1, 2)
        q1 = self._rng.randint(0, 1)
        p2 = self._rng.randint(0, 1)
        q2 = self._rng.randint(1, 2)
        return DiagonalMetric((c1, p1, q1), (c2, p2, q2))

    def _choose_point(self) -> tuple[float, float]:
        """Choose a coordinate point avoiding zero metric values.

        Returns:
            Tuple of (x1, x2) coordinate values.
        """
        x1 = float(self._rng.randint(1, 3))
        x2 = float(self._rng.randint(1, 3))
        return x1, x2

    def _compute_christoffel(self, metric: DiagonalMetric,
                             x1: float, x2: float) -> dict[str, float]:
        """Compute all Christoffel symbols for a 2D diagonal metric.

        For a diagonal metric, the non-zero Christoffel symbols are:
        Gamma^k_{ii} = -0.5 * g^{kk} * dg_{ii}/dx^k  (k != i)
        Gamma^k_{ik} = Gamma^k_{ki} = 0.5 * g^{kk} * dg_{kk}/dx^i

        Args:
            metric: The diagonal metric.
            x1: First coordinate.
            x2: Second coordinate.

        Returns:
            Dict mapping symbol name to value.
        """
        g11_val, g22_val = metric.eval_g(x1, x2)
        g_inv = [1.0 / g11_val, 1.0 / g22_val]

        # g components indexed 0=g11, 1=g22
        g_specs = [metric.g11, metric.g22]

        # Partial derivatives: dg_{aa}/dx^b
        dg = {}
        for a in range(2):
            for b in range(2):
                dg[(a, b)] = metric.partial(g_specs[a], b + 1, x1, x2)

        # Gamma^k_{ij} = 0.5 * g^{kk} * (dg_{ik}/dx^j + dg_{jk}/dx^i
        #                                  - dg_{ij}/dx^k)
        # For diagonal metric, g_{ab} = 0 when a != b, so:
        #   dg_{ik}/dx^j is nonzero only when i == k
        #   dg_{jk}/dx^i is nonzero only when j == k
        #   dg_{ij}/dx^k is nonzero only when i == j
        result: dict[str, float] = {}
        for k in range(2):
            for i in range(2):
                for j in range(i, 2):
                    dg_ik_dxj = dg[(i, j)] if i == k else 0.0
                    dg_jk_dxi = dg[(j, i)] if j == k else 0.0
                    dg_ij_dxk = dg[(i, k)] if i == j else 0.0

                    gamma = 0.5 * g_inv[k] * (
                        dg_ik_dxj + dg_jk_dxi - dg_ij_dxk
                    )
                    label = f"Gamma^{k+1}_{{{i+1}{j+1}}}"
                    result[label] = gamma

        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Christoffel symbol computation problem.

        Args:
            difficulty: Controls metric complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        metric = self._choose_metric(difficulty)
        x1, x2 = self._choose_point()

        g11_val, g22_val = metric.eval_g(x1, x2)
        symbols = self._compute_christoffel(metric, x1, x2)

        problem = (f"\\Gamma^k_{{ij}}: {metric.latex()}, "
                   f"(x^1,x^2)=({_fmt(x1)},{_fmt(x2)})")
        return problem, {
            "metric": metric, "x1": x1, "x2": x2,
            "g11": g11_val, "g22": g22_val,
            "symbols": symbols,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Christoffel symbol computation steps.

        Args:
            data: Solution data with metric values and symbols.

        Returns:
            Steps showing metric evaluation and symbol computation.
        """
        steps = [
            f"g_11={_fmt(data['g11'])}, g_22={_fmt(data['g22'])}",
            f"g^11={_fmt(1.0 / data['g11'])}, "
            f"g^22={_fmt(1.0 / data['g22'])}",
        ]
        for label, val in data["symbols"].items():
            if abs(val) > 1e-10:
                steps.append(f"{label}={_fmt(val)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the non-zero Christoffel symbols.

        Args:
            data: Solution data.

        Returns:
            Formatted non-zero Christoffel symbols.
        """
        nonzero = {k: v for k, v in data["symbols"].items()
                   if abs(v) > 1e-10}
        if not nonzero:
            return "all Gamma^k_{ij}=0"
        parts = [f"{k}={_fmt(v)}" for k, v in nonzero.items()]
        return ", ".join(parts)


# ── 5. Geodesic equation (tier 7) ────────────────────────────────────


@register
class GeodesicEquationGenerator(StepGenerator):
    """Write the geodesic equation for given Christoffel symbols.

    Expands d^2x^k/ds^2 + Gamma^k_{ij} dx^i/ds dx^j/ds = 0 for each
    coordinate k, substituting the provided Christoffel symbol values.
    Produces the explicit system of ODEs governing geodesic motion.

    Input format:
        ``write geodesic equations for given Christoffel symbols``

    Target format:
        ``Gamma^1_{11}=0.5, Gamma^1_{12}=0, ... <step>
        d^2x^1/ds^2 + 0.5*(dx^1/ds)^2 + ... = 0 <step>
        d^2x^2/ds^2 + ... = 0``

    Difficulty scaling:
        Difficulty 1-3: 1-2 non-zero symbols, simple values.
        Difficulty 4-6: 2-3 non-zero symbols.
        Difficulty 7-8: 3-4 non-zero symbols, non-integer values.

    Prerequisites:
        christoffel_symbol (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "geodesic_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["christoffel_symbol"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of non-zero symbols.

        Returns:
            Natural language description.
        """
        return "write geodesic equations for given Christoffel symbols"

    def _generate_symbols(self, difficulty: int) -> dict[str, float]:
        """Generate a set of Christoffel symbols for the problem.

        Args:
            difficulty: Controls number and complexity of symbols.

        Returns:
            Dict mapping symbol label to value.
        """
        all_labels = [
            "Gamma^1_{11}", "Gamma^1_{12}",
            "Gamma^1_{22}", "Gamma^2_{11}",
            "Gamma^2_{12}", "Gamma^2_{22}",
        ]
        if difficulty <= 3:
            n_nonzero = self._rng.randint(1, 2)
            val_choices = [0.5, 1.0, -0.5, -1.0, 2.0]
        elif difficulty <= 6:
            n_nonzero = self._rng.randint(2, 3)
            val_choices = [0.25, 0.5, 1.0, -0.5, 1.5, -1.0, 2.0]
        else:
            n_nonzero = self._rng.randint(3, 4)
            val_choices = [0.25, 0.5, 0.75, 1.0, 1.5, -0.25,
                           -0.5, -1.0, 2.0, -1.5]

        symbols: dict[str, float] = {label: 0.0 for label in all_labels}
        chosen = self._rng.sample(all_labels, n_nonzero)
        for label in chosen:
            symbols[label] = self._rng.choice(val_choices)

        return symbols

    def _build_geodesic_eq(self, k: int,
                           symbols: dict[str, float]) -> str:
        """Build the geodesic ODE string for coordinate k.

        Args:
            k: Coordinate index (1 or 2).
            symbols: Christoffel symbol values.

        Returns:
            String representation of the geodesic equation.
        """
        terms: list[str] = [f"d^2x^{k}/ds^2"]
        # (i, j) pairs with j >= i; factor 2 for off-diagonal
        for i in range(1, 3):
            for j in range(i, 3):
                label = f"Gamma^{k}_{{{i}{j}}}"
                val = symbols.get(label, 0.0)
                if abs(val) < 1e-10:
                    continue
                factor = 2.0 if i != j else 1.0
                coeff = val * factor
                if i == j:
                    vel = f"(dx^{i}/ds)^2"
                else:
                    vel = f"dx^{i}/ds*dx^{j}/ds"
                terms.append(f"{_fmt(coeff)}*{vel}")
        return " + ".join(terms) + " = 0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a geodesic equation problem.

        Args:
            difficulty: Controls symbol complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        symbols = self._generate_symbols(difficulty)
        nonzero = {k: v for k, v in symbols.items() if abs(v) > 1e-10}

        sym_str = ", ".join(f"{k}={_fmt(v)}" for k, v in nonzero.items())
        if not sym_str:
            sym_str = "all zero"

        eq1 = self._build_geodesic_eq(1, symbols)
        eq2 = self._build_geodesic_eq(2, symbols)

        problem = f"\\text{{geodesic: }}{sym_str}"
        return problem, {
            "symbols": symbols, "nonzero": nonzero,
            "eq1": eq1, "eq2": eq2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate geodesic equation derivation steps.

        Args:
            data: Solution data with symbols and equations.

        Returns:
            Steps listing non-zero symbols and the equations.
        """
        steps: list[str] = []
        for label, val in data["nonzero"].items():
            steps.append(f"{label}={_fmt(val)}")
        if not steps:
            steps.append("all Christoffel symbols vanish")
        steps.append(f"k=1: {data['eq1']}")
        steps.append(f"k=2: {data['eq2']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the geodesic equations.

        Args:
            data: Solution data.

        Returns:
            Both geodesic equations as a string.
        """
        return f"{data['eq1']}; {data['eq2']}"


# ── 6. Gaussian curvature (tier 7) ───────────────────────────────────


@register
class GaussianCurvatureGenerator(StepGenerator):
    """Compute Gaussian curvature from first and second fundamental forms.

    Uses K = (eg - f^2) / (EG - F^2) where E, F, G are first
    fundamental form coefficients and e, f, g are second fundamental
    form coefficients. Generates random coefficient values for simple
    surfaces and computes the curvature.

    Input format:
        ``compute Gaussian curvature from fundamental forms``

    Target format:
        ``I: E=1, F=0, G=4; II: e=2, f=0, g=-1 <step>
        EG-F^2=4 <step> eg-f^2=-2 <step> K=-2/4=-0.5``

    Difficulty scaling:
        Difficulty 1-3: F=0, f=0 (orthogonal parameterisation).
        Difficulty 4-6: F=0, f non-zero or small F.
        Difficulty 7-8: general F, f with larger coefficients.

    Prerequisites:
        christoffel_symbol (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gaussian_curvature"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["christoffel_symbol"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Natural language description.
        """
        return "compute Gaussian curvature from fundamental forms"

    def _generate_forms(self, difficulty: int) -> dict[str, float]:
        """Generate first and second fundamental form coefficients.

        Ensures EG - F^2 > 0 (positive definite first fundamental form).

        Args:
            difficulty: Controls coefficient ranges.

        Returns:
            Dict with keys E, F, G, e, f_coeff, g_coeff.
        """
        for _ in range(100):
            if difficulty <= 3:
                big_e = float(self._rng.randint(1, 4))
                big_f = 0.0
                big_g = float(self._rng.randint(1, 4))
                small_e = float(self._rng.randint(-3, 3))
                small_f = 0.0
                small_g = float(self._rng.randint(-3, 3))
            elif difficulty <= 6:
                big_e = float(self._rng.randint(1, 5))
                big_f = float(self._rng.randint(0, 1))
                big_g = float(self._rng.randint(1, 5))
                small_e = float(self._rng.randint(-3, 3))
                small_f = float(self._rng.randint(-2, 2))
                small_g = float(self._rng.randint(-3, 3))
            else:
                big_e = float(self._rng.randint(1, 6))
                big_f = float(self._rng.randint(-2, 2))
                big_g = float(self._rng.randint(1, 6))
                small_e = float(self._rng.randint(-4, 4))
                small_f = float(self._rng.randint(-3, 3))
                small_g = float(self._rng.randint(-4, 4))

            denom = big_e * big_g - big_f ** 2
            if denom > 0:
                return {
                    "E": big_e, "F": big_f, "G": big_g,
                    "e": small_e, "f_coeff": small_f, "g_coeff": small_g,
                    "denom": denom,
                }
        # Fallback: guaranteed valid
        return {
            "E": 1.0, "F": 0.0, "G": 1.0,
            "e": 1.0, "f_coeff": 0.0, "g_coeff": 1.0,
            "denom": 1.0,
        }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gaussian curvature problem.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        forms = self._generate_forms(difficulty)

        numerator = (forms["e"] * forms["g_coeff"]
                     - forms["f_coeff"] ** 2)
        gauss_k = numerator / forms["denom"]

        problem = (
            f"I: E={_fmt(forms['E'])}, F={_fmt(forms['F'])}, "
            f"G={_fmt(forms['G'])}; "
            f"II: e={_fmt(forms['e'])}, f={_fmt(forms['f_coeff'])}, "
            f"g={_fmt(forms['g_coeff'])}"
        )
        return problem, {
            "forms": forms, "numerator": numerator,
            "gauss_k": gauss_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gaussian curvature computation steps.

        Args:
            data: Solution data with form coefficients and curvature.

        Returns:
            Steps showing denominator, numerator, and K.
        """
        forms = data["forms"]
        return [
            f"EG-F^2={_fmt(forms['E'])}*{_fmt(forms['G'])}"
            f"-{_fmt(forms['F'])}^2={_fmt(forms['denom'])}",
            f"eg-f^2={_fmt(forms['e'])}*{_fmt(forms['g_coeff'])}"
            f"-{_fmt(forms['f_coeff'])}^2={_fmt(data['numerator'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Gaussian curvature value.

        Args:
            data: Solution data.

        Returns:
            Formatted Gaussian curvature string.
        """
        return f"K={_fmt(data['gauss_k'])}"
