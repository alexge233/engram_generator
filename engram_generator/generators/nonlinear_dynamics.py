"""Nonlinear dynamics generators -- fixed points through chaos sensitivity.

Covers fixed point classification, bifurcation detection, Lyapunov
exponents, logistic map iteration, limit cycle detection, strange
attractors, fractal dimension, and chaos sensitivity analysis.
All tiers are 5-7 (intermediate to advanced).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ===================================================================
# 1. Fixed point classification  (tier 5)
# ===================================================================

@register
class FixedPointClassifyGenerator(StepGenerator):
    """Find and classify fixed points of a 1D or 2D system.

    For 1D: dx/dt = ax + b or ax^2 + bx + c.  Fixed points where
    f(x)=0, stability from f'(x*).
    For 2D: uses a linear system dx/dt = Ax, classified via eigenvalues.

    Difficulty scaling:
        Difficulty 1-3: 1D linear system, single fixed point.
        Difficulty 4-6: 1D nonlinear (quadratic), two fixed points.
        Difficulty 7-8: 2D linear system, eigenvalue classification.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fixed_point_classify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find and classify fixed points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dynamical system and classify its fixed points.

        Args:
            difficulty: Controls system dimensionality.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # 1D linear: dx/dt = a*x + b
            a = self._rng.choice([-3, -2, -1, 1, 2, 3])
            b = self._rng.randint(-5, 5)
            if a == 0:
                a = -1
            x_star = round(-b / a, 4)
            stability = "stable" if a < 0 else "unstable"
            return f"dx/dt = {a}x + {b}", {
                "mode": "1d_linear", "a": a, "b": b,
                "fixed_points": [x_star],
                "stabilities": [stability],
                "deriv_at_fp": [a],
            }

        if difficulty <= 6:
            # 1D nonlinear: dx/dt = a*x^2 + b*x
            a = self._rng.choice([-2, -1, 1, 2])
            b = self._rng.choice([-4, -3, -2, 2, 3, 4])
            # Fixed points: x=0 and x=-b/a
            fp1 = 0.0
            fp2 = round(-b / a, 4)
            # f'(x) = 2*a*x + b
            deriv1 = b
            deriv2 = round(2 * a * fp2 + b, 4)
            stab1 = "stable" if deriv1 < 0 else "unstable"
            stab2 = "stable" if deriv2 < 0 else "unstable"
            return f"dx/dt = {a}x^2 + {b}x", {
                "mode": "1d_nonlinear", "a": a, "b": b,
                "fixed_points": [fp1, fp2],
                "stabilities": [stab1, stab2],
                "deriv_at_fp": [deriv1, deriv2],
            }

        # 2D linear system: dx/dt = Ax
        # Sample 2x2 matrix with known eigenvalue structure
        tr = self._rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        det_val = self._rng.choice([1, 2, 3, 4, 5])
        disc = tr * tr - 4 * det_val
        if disc >= 0:
            lam1 = round((tr + math.sqrt(disc)) / 2, 4)
            lam2 = round((tr - math.sqrt(disc)) / 2, 4)
            if lam1 < 0 and lam2 < 0:
                fp_type = "stable node"
            elif lam1 > 0 and lam2 > 0:
                fp_type = "unstable node"
            else:
                fp_type = "saddle"
        else:
            lam1 = round(tr / 2, 4)
            lam2 = round(math.sqrt(-disc) / 2, 4)
            if tr < 0:
                fp_type = "stable spiral"
            elif tr > 0:
                fp_type = "unstable spiral"
            else:
                fp_type = "centre"

        return f"dx/dt = Ax, tr(A)={tr}, det(A)={det_val}", {
            "mode": "2d_linear", "trace": tr, "det": det_val,
            "disc": disc,
            "eigenvalues": [lam1, lam2],
            "fp_type": fp_type,
            "fixed_points": [(0, 0)],
            "stabilities": [fp_type],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fixed point classification steps.

        Args:
            data: Solution data with fixed points and stability.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "1d_linear":
            return [
                f"f(x) = {data['a']}x + {data['b']}",
                f"x* = {_fmt(data['fixed_points'][0])}",
                f"f'(x*) = {data['a']}",
                f"classification: {data['stabilities'][0]}",
            ]
        if mode == "1d_nonlinear":
            steps = [f"f(x) = {data['a']}x^2 + {data['b']}x"]
            for i, (fp, stab, d) in enumerate(zip(
                data["fixed_points"], data["stabilities"], data["deriv_at_fp"]
            )):
                steps.append(
                    f"x*_{i + 1} = {_fmt(fp)}, f'={_fmt(d)}: {stab}"
                )
            return steps
        # 2d_linear
        return [
            f"tr(A) = {data['trace']}, det(A) = {data['det']}",
            f"disc = {data['trace']}^2 - 4*{data['det']} = {data['disc']}",
            f"eigenvalues: {_fmt(data['eigenvalues'][0])}, "
            f"{_fmt(data['eigenvalues'][1])}",
            f"classification: {data['fp_type']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fixed points and their classification.

        Args:
            data: Solution data.

        Returns:
            String with fixed points and stability.
        """
        if data["mode"] == "2d_linear":
            return f"origin: {data['fp_type']}"
        fps = ", ".join(
            f"x*={_fmt(fp)} ({stab})"
            for fp, stab in zip(data["fixed_points"], data["stabilities"])
        )
        return fps


# ===================================================================
# 2. Bifurcation detection  (tier 6)
# ===================================================================

@register
class BifurcationDetectGenerator(StepGenerator):
    """Detect bifurcation value for parameterised 1D systems.

    Pitchfork: dx/dt = rx - x^3, bifurcation at r=0.
    Saddle-node: dx/dt = r + x^2, bifurcation at r=0.
    Transcritical: dx/dt = rx - x^2, bifurcation at r=0.

    Difficulty scaling:
        Difficulty 1-3: saddle-node with shifted parameter.
        Difficulty 4-6: pitchfork bifurcation.
        Difficulty 7-8: transcritical, classify fixed point exchange.

    Prerequisites:
        fixed_point_classify.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bifurcation_detect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["fixed_point_classify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find bifurcation value of parameter"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bifurcation detection problem.

        Args:
            difficulty: Controls bifurcation type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        shift = self._rng.choice([-2, -1, 0, 1, 2])

        if difficulty <= 3:
            # Saddle-node: dx/dt = (r - shift) + x^2
            bif_type = "saddle-node"
            r_bif = shift
            eq_str = f"dx/dt = (r - {shift}) + x^2" if shift != 0 else "dx/dt = r + x^2"
            formula = f"(r - {shift}) + x^2 = 0 \\text{{ has tangent at }} x=0"
            return formula, {
                "bif_type": bif_type, "r_bif": r_bif,
                "shift": shift, "eq_str": eq_str,
                "explanation": "fixed points collide and annihilate",
            }

        if difficulty <= 6:
            # Pitchfork: dx/dt = (r - shift)*x - x^3
            bif_type = "pitchfork"
            r_bif = shift
            eq_str = (f"dx/dt = (r - {shift})*x - x^3" if shift != 0
                      else "dx/dt = r*x - x^3")
            formula = f"(r - {shift})x - x^3 = 0"
            return formula, {
                "bif_type": bif_type, "r_bif": r_bif,
                "shift": shift, "eq_str": eq_str,
                "explanation": "origin loses stability, two new branches appear",
            }

        # Transcritical: dx/dt = (r - shift)*x - x^2
        bif_type = "transcritical"
        r_bif = shift
        eq_str = (f"dx/dt = (r - {shift})*x - x^2" if shift != 0
                  else "dx/dt = r*x - x^2")
        formula = f"(r - {shift})x - x^2 = 0"
        return formula, {
            "bif_type": bif_type, "r_bif": r_bif,
            "shift": shift, "eq_str": eq_str,
            "explanation": "two fixed points exchange stability",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bifurcation detection steps.

        Args:
            data: Solution data with bifurcation type and value.

        Returns:
            List of step strings.
        """
        return [
            f"system: {data['eq_str']}",
            f"type: {data['bif_type']}",
            f"set f(x)=0 and f'(x)=0 simultaneously",
            f"r_bif = {data['r_bif']}",
            data["explanation"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the bifurcation value and type.

        Args:
            data: Solution data.

        Returns:
            String with r_bif and bifurcation type.
        """
        return f"r_bif = {data['r_bif']} ({data['bif_type']})"


# ===================================================================
# 3. Lyapunov exponent  (tier 6)
# ===================================================================

@register
class LyapunovExponentGenerator(StepGenerator):
    """Compute Lyapunov exponent for 1D map.

    lambda = (1/n) * sum(ln|f'(x_i)|) for logistic map f(x) = r*x*(1-x).
    f'(x) = r*(1 - 2x).  Positive lambda indicates chaos.

    Difficulty scaling:
        Difficulty 1-3: 5 iterations, r in stable regime.
        Difficulty 4-6: 8 iterations, r near onset of chaos.
        Difficulty 7-8: 10 iterations, r in chaotic regime.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lyapunov_exponent"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Lyapunov exponent of 1D map"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lyapunov exponent computation.

        Args:
            difficulty: Controls number of iterations and r value.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_iter = 5
            r = round(self._rng.uniform(2.5, 3.2), 4)
        elif difficulty <= 6:
            n_iter = 8
            r = round(self._rng.uniform(3.4, 3.6), 4)
        else:
            n_iter = 10
            r = round(self._rng.uniform(3.8, 4.0), 4)

        x = round(self._rng.uniform(0.1, 0.9), 4)
        trajectory = [x]
        log_derivs = []

        for _ in range(n_iter):
            deriv = abs(r * (1 - 2 * x))
            if deriv > 0:
                log_derivs.append(round(math.log(deriv), 4))
            else:
                log_derivs.append(-10.0)
            x = round(r * x * (1 - x), 4)
            trajectory.append(x)

        lyap = round(sum(log_derivs) / len(log_derivs), 4) if log_derivs else 0.0
        classification = "chaotic" if lyap > 0 else "non-chaotic"

        return "\\lambda = \\frac{1}{n} \\sum \\ln|f'(x_i)|", {
            "r": r, "x0": trajectory[0], "n_iter": n_iter,
            "trajectory": trajectory[:4],
            "log_derivs": log_derivs[:4],
            "lyapunov": lyap, "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lyapunov exponent computation steps.

        Args:
            data: Solution data with trajectory and derivatives.

        Returns:
            List of step strings.
        """
        steps = [
            f"f(x) = {_fmt(data['r'])}*x*(1-x), x0 = {_fmt(data['x0'])}",
            f"f'(x) = {_fmt(data['r'])}*(1 - 2x)",
        ]
        for i, (x, ld) in enumerate(zip(data["trajectory"], data["log_derivs"])):
            steps.append(f"x_{i}: {_fmt(x)}, ln|f'| = {_fmt(ld)}")
        steps.append(f"lambda = {_fmt(data['lyapunov'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Lyapunov exponent and classification.

        Args:
            data: Solution data.

        Returns:
            String with lambda value and chaos indicator.
        """
        return f"lambda = {_fmt(data['lyapunov'])} ({data['classification']})"


# ===================================================================
# 4. Logistic map  (tier 5)
# ===================================================================

@register
class LogisticMapGenerator(StepGenerator):
    """Iterate logistic map and classify behaviour.

    x_{n+1} = r*x_n*(1-x_n).  Classification: fixed point (r<3),
    period-2 (3<r<3.449), chaotic (r>3.57).

    Difficulty scaling:
        Difficulty 1-3: 3-4 iterations, r in fixed-point regime.
        Difficulty 4-6: 5-6 iterations, r in period-2 regime.
        Difficulty 7-8: 7-8 iterations, r in chaotic regime.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logistic_map"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "iterate logistic map and classify behaviour"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logistic map iteration problem.

        Args:
            difficulty: Controls r value and iteration count.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_iter = self._rng.randint(3, 4)
            r = round(self._rng.uniform(1.5, 2.9), 4)
            regime = "fixed point"
        elif difficulty <= 6:
            n_iter = self._rng.randint(5, 6)
            r = round(self._rng.uniform(3.1, 3.4), 4)
            regime = "period-2"
        else:
            n_iter = self._rng.randint(7, 8)
            r = round(self._rng.uniform(3.6, 4.0), 4)
            regime = "chaotic"

        x = round(self._rng.uniform(0.1, 0.9), 4)
        trajectory = [x]
        for _ in range(n_iter):
            x = round(r * x * (1 - x), 4)
            trajectory.append(x)

        return "x_{n+1} = r x_n (1 - x_n)", {
            "r": r, "n_iter": n_iter,
            "trajectory": trajectory,
            "regime": regime,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate logistic map iteration steps.

        Args:
            data: Solution data with trajectory.

        Returns:
            List of step strings.
        """
        steps = [f"r = {_fmt(data['r'])}, x_0 = {_fmt(data['trajectory'][0])}"]
        for i in range(min(len(data["trajectory"]) - 1, 5)):
            steps.append(
                f"x_{i + 1} = {_fmt(data['r'])}*{_fmt(data['trajectory'][i])}"
                f"*(1 - {_fmt(data['trajectory'][i])})"
                f" = {_fmt(data['trajectory'][i + 1])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return final value and regime classification.

        Args:
            data: Solution data.

        Returns:
            String with x_n and regime.
        """
        return (
            f"x_{data['n_iter']} = {_fmt(data['trajectory'][-1])}"
            f" ({data['regime']})"
        )


# ===================================================================
# 5. Limit cycle  (tier 7)
# ===================================================================

@register
class LimitCycleGenerator(StepGenerator):
    """Determine if a 2D system has a limit cycle.

    Uses template-based approach: Van der Pol oscillator (mu>0 has
    limit cycle), simple harmonic (no limit cycle), and Lienard
    systems.  Check Poincare-Bendixson conditions.

    Difficulty scaling:
        Difficulty 1-3: Van der Pol with mu>0 (always has limit cycle).
        Difficulty 4-6: determine if trapping region exists.
        Difficulty 7-8: Lienard system, check sufficient conditions.

    Prerequisites:
        fixed_point_classify.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "limit_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["fixed_point_classify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine if system has a limit cycle"

    _SYSTEMS = [
        {
            "name": "Van der Pol",
            "equation": "x'' - mu*(1-x^2)*x' + x = 0",
            "has_cycle": True,
            "condition": "mu > 0, unique unstable fixed point at origin",
            "category": "easy",
        },
        {
            "name": "simple harmonic",
            "equation": "x'' + omega^2*x = 0",
            "has_cycle": False,
            "condition": "conservative system, centre not limit cycle",
            "category": "easy",
        },
        {
            "name": "damped oscillator",
            "equation": "x'' + b*x' + k*x = 0 (b>0)",
            "has_cycle": False,
            "condition": "dissipative, spirals inward",
            "category": "medium",
        },
        {
            "name": "Rayleigh oscillator",
            "equation": "x'' - mu*(1-x'^2)*x' + x = 0",
            "has_cycle": True,
            "condition": "equivalent to Van der Pol, Poincare-Bendixson applies",
            "category": "medium",
        },
        {
            "name": "Lienard (f odd, xF>0)",
            "equation": "x'' + f(x)*x' + g(x) = 0",
            "has_cycle": True,
            "condition": "Lienard theorem: f odd, F(x)->inf, unique zero",
            "category": "hard",
        },
        {
            "name": "gradient system",
            "equation": "dx/dt = -dV/dx (V convex)",
            "has_cycle": False,
            "condition": "gradient systems have no closed orbits",
            "category": "hard",
        },
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a limit cycle detection problem.

        Args:
            difficulty: Controls system complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = [s for s in self._SYSTEMS if s["category"] == "easy"]
        elif difficulty <= 6:
            pool = [s for s in self._SYSTEMS if s["category"] in ("easy", "medium")]
        else:
            pool = self._SYSTEMS

        system = self._rng.choice(pool)
        mu = round(self._rng.uniform(0.5, 5.0), 4) if "mu" in system["equation"] else None

        return system["equation"], {
            "name": system["name"],
            "equation": system["equation"],
            "has_cycle": system["has_cycle"],
            "condition": system["condition"],
            "mu": mu,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate limit cycle analysis steps.

        Args:
            data: Solution data with system properties.

        Returns:
            List of step strings.
        """
        steps = [
            f"system: {data['name']}",
            f"equation: {data['equation']}",
        ]
        if data["mu"] is not None:
            steps.append(f"mu = {_fmt(data['mu'])} > 0")
        steps.append(f"condition: {data['condition']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return whether a limit cycle exists.

        Args:
            data: Solution data.

        Returns:
            String indicating presence or absence of limit cycle.
        """
        if data["has_cycle"]:
            return f"{data['name']}: limit cycle exists"
        return f"{data['name']}: no limit cycle"


# ===================================================================
# 6. Strange attractor  (tier 6)
# ===================================================================

@register
class StrangeAttractorGenerator(StepGenerator):
    """Iterate Henon map and track trajectory.

    x_{n+1} = 1 - a*x_n^2 + y_n, y_{n+1} = b*x_n.
    Classic parameters: a=1.4, b=0.3.

    Difficulty scaling:
        Difficulty 1-3: 5 iterations, classic parameters.
        Difficulty 4-6: 7 iterations, varied a near 1.4.
        Difficulty 7-8: 10 iterations, varied a and b.

    Prerequisites:
        logistic_map.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "strange_attractor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logistic_map"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "iterate Henon map and track trajectory"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Henon map trajectory.

        Args:
            difficulty: Controls iteration count and parameters.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_iter = 5
            a = 1.4
            b = 0.3
        elif difficulty <= 6:
            n_iter = 7
            a = round(self._rng.uniform(1.2, 1.5), 4)
            b = 0.3
        else:
            n_iter = 10
            a = round(self._rng.uniform(1.2, 1.5), 4)
            b = round(self._rng.uniform(0.2, 0.4), 4)

        x = round(self._rng.uniform(-0.5, 0.5), 4)
        y = round(self._rng.uniform(-0.5, 0.5), 4)
        trajectory = [(x, y)]

        for _ in range(n_iter):
            x_new = round(1 - a * x ** 2 + y, 4)
            y_new = round(b * x, 4)
            x, y = x_new, y_new
            trajectory.append((x, y))

        # Only keep first 6 points for compact output
        shown = trajectory[:6]

        return "x_{n+1} = 1 - a x_n^2 + y_n, \\; y_{n+1} = b x_n", {
            "a": a, "b": b, "n_iter": n_iter,
            "trajectory": shown,
            "x_final": trajectory[-1][0],
            "y_final": trajectory[-1][1],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Henon map iteration steps.

        Args:
            data: Solution data with trajectory.

        Returns:
            List of step strings.
        """
        steps = [f"a={_fmt(data['a'])}, b={_fmt(data['b'])}"]
        for i, (x, y) in enumerate(data["trajectory"]):
            steps.append(f"({_fmt(x)}, {_fmt(y)})")
            if i >= 4:
                break
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final point on the trajectory.

        Args:
            data: Solution data.

        Returns:
            String with final (x, y) coordinates.
        """
        return (
            f"(x, y) = ({_fmt(data['x_final'])}, "
            f"{_fmt(data['y_final'])})"
        )


# ===================================================================
# 7. Fractal dimension  (tier 6)
# ===================================================================

@register
class FractalDimensionGenerator(StepGenerator):
    """Compute box-counting fractal dimension.

    D = log(N(eps)) / log(1/eps).  Uses known fractals: Koch curve
    (D=log4/log3), Sierpinski triangle (D=log3/log2), Cantor set
    (D=log2/log3), Sierpinski carpet (D=log8/log3).

    Difficulty scaling:
        Difficulty 1-3: Cantor set (D = log2/log3).
        Difficulty 4-6: Koch curve or Sierpinski triangle.
        Difficulty 7-8: Sierpinski carpet, compute from N and scale.

    Prerequisites:
        logarithm.
    """

    _FRACTALS = [
        {"name": "Cantor set", "N": 2, "scale": 3,
         "D": round(math.log(2) / math.log(3), 4), "level": "easy"},
        {"name": "Koch curve", "N": 4, "scale": 3,
         "D": round(math.log(4) / math.log(3), 4), "level": "medium"},
        {"name": "Sierpinski triangle", "N": 3, "scale": 2,
         "D": round(math.log(3) / math.log(2), 4), "level": "medium"},
        {"name": "Sierpinski carpet", "N": 8, "scale": 3,
         "D": round(math.log(8) / math.log(3), 4), "level": "hard"},
        {"name": "Menger sponge", "N": 20, "scale": 3,
         "D": round(math.log(20) / math.log(3), 4), "level": "hard"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fractal_dimension"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute fractal dimension via box counting"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fractal dimension problem.

        Args:
            difficulty: Controls fractal complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = [f for f in self._FRACTALS if f["level"] == "easy"]
        elif difficulty <= 6:
            pool = [f for f in self._FRACTALS if f["level"] in ("easy", "medium")]
        else:
            pool = self._FRACTALS

        fractal = self._rng.choice(pool)
        n_copies = fractal["N"]
        scale = fractal["scale"]
        log_n = round(math.log(n_copies), 4)
        log_s = round(math.log(scale), 4)
        dim = round(log_n / log_s, 4)

        return "D = \\frac{\\log N}{\\log s}", {
            "name": fractal["name"],
            "N": n_copies, "scale": scale,
            "log_N": log_n, "log_s": log_s,
            "D": dim,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fractal dimension computation steps.

        Args:
            data: Solution data with N, scale, and dimension.

        Returns:
            List of step strings.
        """
        return [
            f"{data['name']}: N={data['N']} copies, scale={data['scale']}",
            f"log(N) = log({data['N']}) = {_fmt(data['log_N'])}",
            f"log(s) = log({data['scale']}) = {_fmt(data['log_s'])}",
            f"D = {_fmt(data['log_N'])}/{_fmt(data['log_s'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fractal dimension.

        Args:
            data: Solution data.

        Returns:
            String with dimension value.
        """
        return f"D({data['name']}) = {_fmt(data['D'])}"


# ===================================================================
# 8. Chaos sensitivity  (tier 6)
# ===================================================================

@register
class ChaosSensitivityGenerator(StepGenerator):
    """Measure sensitivity to initial conditions in logistic map.

    Start two trajectories at x0 and x0+delta, iterate logistic map,
    measure |x_n - x_n'| divergence.

    Difficulty scaling:
        Difficulty 1-3: delta=0.01, 5 iterations, r in stable regime.
        Difficulty 4-6: delta=0.001, 7 iterations, r near chaos.
        Difficulty 7-8: delta=0.0001, 10 iterations, r in chaotic regime.

    Prerequisites:
        lyapunov_exponent.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chaos_sensitivity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lyapunov_exponent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "measure sensitivity to initial conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chaos sensitivity measurement.

        Args:
            difficulty: Controls delta, iterations, and r value.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            delta = 0.01
            n_iter = 5
            r = round(self._rng.uniform(2.5, 3.0), 4)
        elif difficulty <= 6:
            delta = 0.001
            n_iter = 7
            r = round(self._rng.uniform(3.4, 3.6), 4)
        else:
            delta = 0.0001
            n_iter = 10
            r = round(self._rng.uniform(3.8, 4.0), 4)

        x0 = round(self._rng.uniform(0.2, 0.8), 4)
        x0_prime = round(x0 + delta, 4)

        x = x0
        x_p = x0_prime
        separations = [round(abs(x - x_p), 4)]

        for _ in range(n_iter):
            x = round(r * x * (1 - x), 4)
            x_p = round(r * x_p * (1 - x_p), 4)
            separations.append(round(abs(x - x_p), 4))

        grew = separations[-1] > separations[0]

        return "|x_n - x'_n| \\text{ divergence}", {
            "r": r, "x0": x0, "delta": delta,
            "n_iter": n_iter,
            "separations": separations[:6],
            "final_sep": separations[-1],
            "initial_sep": separations[0],
            "sensitive": grew,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate chaos sensitivity analysis steps.

        Args:
            data: Solution data with separations.

        Returns:
            List of step strings.
        """
        steps = [
            f"r={_fmt(data['r'])}, x0={_fmt(data['x0'])}, "
            f"delta={_fmt(data['delta'])}",
        ]
        for i, sep in enumerate(data["separations"]):
            steps.append(f"|x_{i} - x'_{i}| = {_fmt(sep)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final separation and sensitivity verdict.

        Args:
            data: Solution data.

        Returns:
            String with final separation and sensitivity.
        """
        label = "sensitive" if data["sensitive"] else "insensitive"
        return (
            f"|x_n - x'_n| = {_fmt(data['final_sep'])} ({label})"
        )
