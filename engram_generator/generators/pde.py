"""Partial differential equation generators for tiers 6-7.

Provides generators for PDE classification, heat equation, wave equation,
Laplace equation, method of characteristics, Green's function, Fourier
transform PDE, and finite difference discretisation. Each generator
produces step-by-step solutions with LaTeX formatting suitable for
training sequence models.
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


# ── 1. Classify PDE (tier 6) ─────────────────────────────────────────


@register
class ClassifyPDEGenerator(StepGenerator):
    """Classify a second-order PDE as elliptic, parabolic, or hyperbolic.

    Given Au_xx + 2Bu_xy + Cu_yy + ... = 0, computes the discriminant
    D = B^2 - AC and classifies: D < 0 elliptic, D = 0 parabolic,
    D > 0 hyperbolic.

    Input format:
        ``classify second-order PDE``

    Target format:
        ``3u_xx + 2u_xy + 1u_yy = 0 <step> A=3, B=1, C=1
        <step> D = B^2 - AC = 1 - 3 = -2 <step> D<0: elliptic``

    Difficulty scaling:
        Difficulty 1-3: small integer coefficients, clear classification.
        Difficulty 4-6: larger coefficients, may include lower-order terms.
        Difficulty 7-8: coefficients chosen to be near boundary cases.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "classify_pde"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Natural language description.
        """
        return "classify second-order PDE"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PDE classification problem.

        Args:
            difficulty: Controls coefficient range and near-boundary cases.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            hi = 4
        elif difficulty <= 6:
            hi = 7
        else:
            hi = 10

        a = self._rng.randint(1, hi)
        b = self._rng.randint(-hi, hi)
        c = self._rng.randint(1, hi)

        disc = b * b - a * c

        if disc < 0:
            pde_type = "elliptic"
        elif disc == 0:
            pde_type = "parabolic"
        else:
            pde_type = "hyperbolic"

        problem = f"{a}u_{{xx}} + {2 * b}u_{{xy}} + {c}u_{{yy}} = 0"
        return problem, {
            "A": a, "B": b, "C": c, "disc": disc, "pde_type": pde_type,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data with coefficients and discriminant.

        Returns:
            Steps showing coefficient identification and classification.
        """
        return [
            f"A={data['A']}, B={data['B']}, C={data['C']}",
            f"D = B^2 - AC = {data['B']}^2 - {data['A']}*{data['C']}"
            f" = {data['disc']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the PDE classification.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        sign = "<0" if data["disc"] < 0 else ("=0" if data["disc"] == 0 else ">0")
        return f"D{sign}: {data['pde_type']}"


# ── 2. Heat equation (tier 6) ────────────────────────────────────────


@register
class HeatEquationGenerator(StepGenerator):
    """Solve the 1D heat equation by separation of variables.

    Solves u_t = k*u_xx on [0, L] with u(0,t) = u(L,t) = 0. The
    solution is u(x,t) = sum B_n sin(n pi x / L) exp(-k(n pi/L)^2 t).
    Computes the first 2-3 Fourier coefficients and evaluates.

    Input format:
        ``solve 1D heat equation by separation of variables``

    Target format:
        ``u_t = 2*u_xx, L=1, t=0.5 <step> lambda_1 = pi^2*2 = 19.7392
        <step> B_1=3, term_1 = 3*sin(pi*x)*exp(-19.7392*0.5)
        <step> u(0.5, 0.5) = ...``

    Difficulty scaling:
        Difficulty 1-3: 2 terms, small k, L, integer B_n.
        Difficulty 4-6: 3 terms, moderate parameters.
        Difficulty 7-8: 3 terms, larger coefficients.

    Prerequisites:
        separation_of_variables (tier 4), fourier_coefficient (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heat_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["separation_of_variables", "fourier_coefficient"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of terms and parameter range.

        Returns:
            Natural language description.
        """
        return "solve 1D heat equation by separation of variables"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a heat equation problem.

        Args:
            difficulty: Controls parameter magnitudes and number of terms.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_terms = 2
            k = self._rng.choice([1, 2])
            big_l = self._rng.choice([1, 2])
            b_max = 3
        elif difficulty <= 6:
            n_terms = 3
            k = self._rng.choice([1, 2, 3])
            big_l = self._rng.choice([1, 2, 3])
            b_max = 5
        else:
            n_terms = 3
            k = self._rng.choice([2, 3, 4])
            big_l = self._rng.choice([1, 2])
            b_max = 8

        t_val = round(self._rng.choice([0.1, 0.2, 0.5, 1.0]), 1)
        x_val = round(big_l * self._rng.choice([0.25, 0.5, 0.75]), 4)

        coeffs = []
        for _ in range(n_terms):
            b_n = self._rng.randint(1, b_max)
            if self._rng.random() < 0.3:
                b_n = -b_n
            coeffs.append(b_n)

        # Compute solution at (x_val, t_val)
        terms = []
        total = 0.0
        for idx, b_n in enumerate(coeffs):
            n = idx + 1
            lam = k * (n * math.pi / big_l) ** 2
            spatial = math.sin(n * math.pi * x_val / big_l)
            temporal = math.exp(-lam * t_val)
            term_val = b_n * spatial * temporal
            terms.append({
                "n": n, "B_n": b_n, "lambda_n": lam,
                "spatial": spatial, "temporal": temporal,
                "term_val": term_val,
            })
            total += term_val

        problem = (f"u_t = {k}u_{{xx}}, L={big_l}, "
                   f"u(x,0) = \\sum B_n\\sin(n\\pi x/{big_l})")
        return problem, {
            "k": k, "L": big_l, "t": t_val, "x": x_val,
            "coeffs": coeffs, "terms": terms, "total": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate heat equation solution steps.

        Args:
            data: Solution data with terms and values.

        Returns:
            Steps showing eigenvalues, coefficients, and evaluation.
        """
        steps = []
        for term in data["terms"]:
            lam_str = _fmt(term["lambda_n"])
            steps.append(
                f"n={term['n']}: lambda={lam_str}, "
                f"B_{term['n']}={term['B_n']}"
            )
        steps.append(f"evaluate at x={_fmt(data['x'])}, t={_fmt(data['t'])}")
        for term in data["terms"]:
            steps.append(
                f"term_{term['n']}={_fmt(term['term_val'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x, t).
        """
        return f"u({_fmt(data['x'])},{_fmt(data['t'])})={_fmt(data['total'])}"


# ── 3. Wave equation 1D (tier 6) ─────────────────────────────────────


@register
class WaveEquation1DGenerator(StepGenerator):
    """Solve the 1D wave equation using d'Alembert's formula.

    For u_tt = c^2 u_xx with initial conditions u(x,0) = f(x) and
    u_t(x,0) = 0, the solution is u(x,t) = (f(x-ct) + f(x+ct)) / 2.
    Evaluates at a given point (x, t).

    Input format:
        ``solve 1D wave equation using d'Alembert formula``

    Target format:
        ``u_tt = 4u_xx, f(x)=sin(pi*x), (x,t)=(1,0.5) <step>
        c=2, x-ct=0, x+ct=2 <step> f(0)=0, f(2)=0
        <step> u=(0+0)/2=0``

    Difficulty scaling:
        Difficulty 1-3: f(x) = A*sin(pi*x), small c.
        Difficulty 4-6: f(x) = A*sin(n*pi*x), moderate parameters.
        Difficulty 7-8: f(x) = sum of two sine terms.

    Prerequisites:
        separation_of_variables (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wave_equation_1d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["separation_of_variables"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls initial condition complexity.

        Returns:
            Natural language description.
        """
        return "solve 1D wave equation using d'Alembert formula"

    def _eval_f(self, x: float, wave_terms: list[tuple[int, int]]) -> float:
        """Evaluate the initial condition f(x) = sum A_n sin(n pi x).

        Args:
            x: Spatial coordinate.
            wave_terms: List of (A_n, n) pairs.

        Returns:
            Value of f(x).
        """
        total = 0.0
        for a_n, n in wave_terms:
            total += a_n * math.sin(n * math.pi * x)
        return total

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a wave equation problem.

        Args:
            difficulty: Controls number of terms and parameter range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            c = self._rng.choice([1, 2])
            a1 = self._rng.randint(1, 3)
            wave_terms = [(a1, 1)]
        elif difficulty <= 6:
            c = self._rng.choice([1, 2, 3])
            a1 = self._rng.randint(1, 4)
            n1 = self._rng.choice([1, 2])
            wave_terms = [(a1, n1)]
        else:
            c = self._rng.choice([2, 3])
            a1 = self._rng.randint(1, 3)
            a2 = self._rng.randint(1, 3)
            wave_terms = [(a1, 1), (a2, 2)]

        x_val = round(self._rng.choice([0.25, 0.5, 0.75, 1.0, 1.5]), 2)
        t_val = round(self._rng.choice([0.1, 0.25, 0.5, 1.0]), 2)

        x_minus = x_val - c * t_val
        x_plus = x_val + c * t_val

        f_minus = self._eval_f(x_minus, wave_terms)
        f_plus = self._eval_f(x_plus, wave_terms)
        u_val = (f_minus + f_plus) / 2.0

        f_str_parts = []
        for a_n, n in wave_terms:
            if n == 1:
                f_str_parts.append(f"{a_n}\\sin(\\pi x)")
            else:
                f_str_parts.append(f"{a_n}\\sin({n}\\pi x)")
        f_str = "+".join(f_str_parts)

        problem = (f"u_{{tt}} = {c**2}u_{{xx}}, "
                   f"f(x) = {f_str}, (x,t)=({_fmt(x_val)},{_fmt(t_val)})")
        return problem, {
            "c": c, "x": x_val, "t": t_val,
            "x_minus": x_minus, "x_plus": x_plus,
            "f_minus": f_minus, "f_plus": f_plus,
            "u_val": u_val, "wave_terms": wave_terms,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate d'Alembert solution steps.

        Args:
            data: Solution data with characteristic coordinates.

        Returns:
            Steps showing characteristic evaluation and superposition.
        """
        return [
            f"c={data['c']}, x-ct={_fmt(data['x_minus'])}, "
            f"x+ct={_fmt(data['x_plus'])}",
            f"f(x-ct)={_fmt(data['f_minus'])}",
            f"f(x+ct)={_fmt(data['f_plus'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the wave equation solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x, t).
        """
        return f"u({_fmt(data['x'])},{_fmt(data['t'])})={_fmt(data['u_val'])}"


# ── 4. Laplace equation (tier 7) ─────────────────────────────────────


@register
class LaplaceEquationGenerator(StepGenerator):
    """Solve the Laplace equation on a rectangle by separation of variables.

    Solves u_xx + u_yy = 0 on [0, a] x [0, b] with u = 0 on three
    sides and u(x, b) = f(x) on the top. The solution is
    u(x, y) = sum B_n sin(n pi x / a) sinh(n pi y / a) / sinh(n pi b / a).
    Evaluates at a given interior point.

    Input format:
        ``solve Laplace equation on rectangle``

    Target format:
        ``u_xx+u_yy=0, [0,2]x[0,1], u(x,1)=sin(pi*x/2) <step>
        B_1=1, sinh(pi*0.5/2)/sinh(pi*1/2) = ... <step>
        u(1, 0.5) = ...``

    Difficulty scaling:
        Difficulty 1-3: single term, small a and b.
        Difficulty 4-6: 2 terms, moderate domain.
        Difficulty 7-8: 2-3 terms, larger domain.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laplace_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls domain size and number of terms.

        Returns:
            Natural language description.
        """
        return "solve Laplace equation on rectangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Laplace equation problem.

        Args:
            difficulty: Controls domain and number of Fourier terms.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_terms = 1
            a = self._rng.choice([1, 2])
            b = self._rng.choice([1, 2])
            b_max = 3
        elif difficulty <= 6:
            n_terms = 2
            a = self._rng.choice([1, 2, 3])
            b = self._rng.choice([1, 2])
            b_max = 4
        else:
            n_terms = self._rng.choice([2, 3])
            a = self._rng.choice([2, 3])
            b = self._rng.choice([1, 2, 3])
            b_max = 6

        coeffs = []
        for _ in range(n_terms):
            bn = self._rng.randint(1, b_max)
            coeffs.append(bn)

        x_val = round(a * self._rng.choice([0.25, 0.5, 0.75]), 4)
        y_val = round(b * self._rng.choice([0.25, 0.5, 0.75]), 4)

        total = 0.0
        terms = []
        for idx, bn in enumerate(coeffs):
            n = idx + 1
            arg_y = n * math.pi * y_val / a
            arg_b = n * math.pi * b / a
            spatial = math.sin(n * math.pi * x_val / a)
            ratio = math.sinh(arg_y) / math.sinh(arg_b) if arg_b > 0 else 0.0
            term_val = bn * spatial * ratio
            terms.append({
                "n": n, "B_n": bn, "spatial": spatial,
                "ratio": ratio, "term_val": term_val,
            })
            total += term_val

        problem = (f"u_{{xx}}+u_{{yy}}=0, [0,{a}]\\times[0,{b}], "
                   f"u(x,{b})=\\sum B_n\\sin(n\\pi x/{a})")
        return problem, {
            "a": a, "b": b, "x": x_val, "y": y_val,
            "coeffs": coeffs, "terms": terms, "total": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Laplace equation solution steps.

        Args:
            data: Solution data with terms and values.

        Returns:
            Steps showing Fourier terms and evaluation.
        """
        steps = []
        for term in data["terms"]:
            steps.append(
                f"n={term['n']}: B_{term['n']}={term['B_n']}, "
                f"ratio={_fmt(term['ratio'])}"
            )
        steps.append(f"evaluate at ({_fmt(data['x'])},{_fmt(data['y'])})")
        for term in data["terms"]:
            steps.append(f"term_{term['n']}={_fmt(term['term_val'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Laplace equation solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x, y).
        """
        return f"u({_fmt(data['x'])},{_fmt(data['y'])})={_fmt(data['total'])}"


# ── 5. Method of characteristics (tier 7) ────────────────────────────


@register
class MethodOfCharacteristicsGenerator(StepGenerator):
    """Solve a first-order PDE using the method of characteristics.

    Solves a u_x + b u_y = 0 with initial data u(x, 0) = f(x).
    Characteristic curves satisfy dy/dx = b/a, giving y = (b/a)x + C.
    Along characteristics u is constant, so u(x, y) = f(x - (a/b)y).

    Input format:
        ``solve first-order PDE by method of characteristics``

    Target format:
        ``2u_x + 3u_y = 0, u(x,0) = sin(pi*x) <step>
        characteristics: dy/dx = 3/2, y = 1.5*x + C <step>
        u(x,y) = f(x - (2/3)*y) <step> u(1, 1.5) = sin(pi*0) = 0``

    Difficulty scaling:
        Difficulty 1-3: f(x) = A*x, small a, b.
        Difficulty 4-6: f(x) = A*sin(pi*x), moderate a, b.
        Difficulty 7-8: f(x) = A*x^2 + B*x, larger coefficients.

    Prerequisites:
        diff_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "method_of_characteristics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls initial condition complexity.

        Returns:
            Natural language description.
        """
        return "solve first-order PDE by method of characteristics"

    def _eval_f(self, xi: float, f_type: str,
                f_params: tuple) -> float:
        """Evaluate the initial condition f(xi).

        Args:
            xi: Characteristic variable value.
            f_type: Type of initial condition ('linear', 'sine', 'quad').
            f_params: Parameters for the initial condition.

        Returns:
            Value of f(xi).
        """
        if f_type == "linear":
            a_coeff = f_params[0]
            return a_coeff * xi
        if f_type == "sine":
            a_coeff = f_params[0]
            return a_coeff * math.sin(math.pi * xi)
        # quad: A*xi^2 + B*xi
        a_coeff, b_coeff = f_params
        return a_coeff * xi ** 2 + b_coeff * xi

    def _f_latex(self, f_type: str, f_params: tuple) -> str:
        """Format the initial condition as LaTeX.

        Args:
            f_type: Initial condition type.
            f_params: Parameters.

        Returns:
            LaTeX string for f(x).
        """
        if f_type == "linear":
            return f"{f_params[0]}x"
        if f_type == "sine":
            return f"{f_params[0]}\\sin(\\pi x)"
        a_coeff, b_coeff = f_params
        return f"{a_coeff}x^2+{b_coeff}x"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a method of characteristics problem.

        Args:
            difficulty: Controls initial condition and coefficient range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            c = self._rng.randint(1, 4)
            f_type = "linear"
            f_params = (c,)
        elif difficulty <= 6:
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 4)
            c = self._rng.randint(1, 3)
            f_type = "sine"
            f_params = (c,)
        else:
            a = self._rng.randint(2, 5)
            b = self._rng.randint(2, 5)
            c1 = self._rng.randint(1, 3)
            c2 = self._rng.randint(1, 3)
            f_type = "quad"
            f_params = (c1, c2)

        x_val = round(self._rng.choice([0.5, 1.0, 1.5, 2.0]), 2)
        y_val = round(self._rng.choice([0.5, 1.0, 1.5]), 2)

        slope = b / a
        xi = x_val - (a / b) * y_val if b != 0 else x_val
        f_val = self._eval_f(xi, f_type, f_params)

        problem = (f"{a}u_x + {b}u_y = 0, "
                   f"u(x,0) = {self._f_latex(f_type, f_params)}")
        return problem, {
            "a": a, "b": b, "slope": slope,
            "x": x_val, "y": y_val, "xi": xi,
            "f_type": f_type, "f_params": f_params,
            "f_val": f_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate method of characteristics steps.

        Args:
            data: Solution data with characteristic info.

        Returns:
            Steps showing characteristic direction and evaluation.
        """
        return [
            f"dy/dx = {data['b']}/{data['a']} = {_fmt(data['slope'])}",
            f"xi = x - ({data['a']}/{data['b']})y = {_fmt(data['xi'])}",
            f"u(x,y) = f(xi) = f({_fmt(data['xi'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the PDE solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x, y).
        """
        return f"u({_fmt(data['x'])},{_fmt(data['y'])})={_fmt(data['f_val'])}"


# ── 6. Green's function (tier 7) ─────────────────────────────────────


@register
class GreensFunctionGenerator(StepGenerator):
    """Find and evaluate Green's function for -u'' = f on [0, 1].

    With boundary conditions u(0) = u(1) = 0, the Green's function is
    G(x, s) = s(1-x) for s <= x, and G(x, s) = x(1-s) for s > x.
    Evaluates the solution u(x) = integral_0^1 G(x,s) f(s) ds for
    simple source functions.

    Input format:
        ``find Green's function for -u''=f on [0,1]``

    Target format:
        ``-u''=f, u(0)=u(1)=0, f(s)=1 <step>
        G(x,s) = s(1-x) for s<=x, x(1-s) for s>x <step>
        u(0.5) = int_0^1 G(0.5,s) ds <step>
        u(0.5) = int_0^{0.5} s*0.5 ds + int_{0.5}^1 0.5*(1-s) ds
        <step> u(0.5) = 0.125``

    Difficulty scaling:
        Difficulty 1-3: f(s) = constant, evaluate at simple x.
        Difficulty 4-6: f(s) = s or (1-s), moderate x.
        Difficulty 7-8: f(s) = A*s + B, general x.

    Prerequisites:
        laplace_equation (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "greens_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["laplace_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls source function complexity.

        Returns:
            Natural language description.
        """
        return "find Green's function for -u''=f on [0,1]"

    def _integrate_greens(self, x_val: float, f_type: str,
                          f_params: tuple) -> float:
        """Compute u(x) = integral_0^1 G(x, s) f(s) ds analytically.

        Args:
            x_val: Point at which to evaluate the solution.
            f_type: Source function type ('const', 'linear', 'affine').
            f_params: Source function parameters.

        Returns:
            Value of u(x).
        """
        # G(x,s) = s(1-x) for s<=x, x(1-s) for s>x
        # Part 1: integral_0^x s(1-x) f(s) ds
        # Part 2: integral_x^1 x(1-s) f(s) ds

        if f_type == "const":
            c = f_params[0]
            # int_0^x c*s*(1-x) ds = c*(1-x)*x^2/2
            part1 = c * (1 - x_val) * x_val ** 2 / 2
            # int_x^1 c*x*(1-s) ds = c*x*(1-x)^2/2
            part2 = c * x_val * (1 - x_val) ** 2 / 2
        elif f_type == "linear":
            # f(s) = s
            # int_0^x s^2*(1-x) ds = (1-x)*x^3/3
            part1 = (1 - x_val) * x_val ** 3 / 3
            # int_x^1 x*s*(1-s) ds = x*[s^2/2 - s^3/3]_x^1
            # = x*(1/2 - 1/3 - x^2/2 + x^3/3)
            # = x*(1/6 - x^2/2 + x^3/3)
            part2 = x_val * (1 / 6 - x_val ** 2 / 2 + x_val ** 3 / 3)
        else:
            # affine: f(s) = A*s + B
            a_coeff, b_coeff = f_params
            # Decompose: u = A * u_linear + B * u_const
            part1_lin = (1 - x_val) * x_val ** 3 / 3
            part2_lin = x_val * (1 / 6 - x_val ** 2 / 2 + x_val ** 3 / 3)
            u_lin = part1_lin + part2_lin

            part1_const = (1 - x_val) * x_val ** 2 / 2
            part2_const = x_val * (1 - x_val) ** 2 / 2
            u_const = part1_const + part2_const

            return a_coeff * u_lin + b_coeff * u_const

        return part1 + part2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Green's function problem.

        Args:
            difficulty: Controls source function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            c = self._rng.randint(1, 4)
            f_type = "const"
            f_params = (c,)
            f_latex = str(c)
        elif difficulty <= 6:
            f_type = "linear"
            f_params = ()
            f_latex = "s"
        else:
            a_coeff = self._rng.randint(1, 3)
            b_coeff = self._rng.randint(1, 3)
            f_type = "affine"
            f_params = (a_coeff, b_coeff)
            f_latex = f"{a_coeff}s+{b_coeff}"

        x_val = round(self._rng.choice([0.25, 0.5, 0.75]), 4)
        u_val = self._integrate_greens(x_val, f_type, f_params)

        problem = f"-u''={f_latex}, u(0)=u(1)=0"
        return problem, {
            "x": x_val, "f_type": f_type, "f_params": f_params,
            "f_latex": f_latex, "u_val": u_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Green's function solution steps.

        Args:
            data: Solution data with Green's function evaluation.

        Returns:
            Steps showing G(x,s) definition and integration.
        """
        x = data["x"]
        return [
            "G(x,s)=s(1-x) for s<=x, x(1-s) for s>x",
            f"u({_fmt(x)}) = int_0^1 G({_fmt(x)},s)*{data['f_latex']} ds",
            f"= int_0^{{{_fmt(x)}}} s(1-{_fmt(x)})*{data['f_latex']} ds"
            f" + int_{{{_fmt(x)}}}^1 {_fmt(x)}(1-s)*{data['f_latex']} ds",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x).
        """
        return f"u({_fmt(data['x'])})={_fmt(data['u_val'])}"


# ── 7. Fourier transform PDE (tier 7) ────────────────────────────────


@register
class FourierTransformPDEGenerator(StepGenerator):
    """Solve the heat equation on R via Fourier transform.

    For u_t = k u_xx on R with u(x, 0) = f(x), the solution is
    u(x, t) = (1/sqrt(4 pi k t)) integral f(y) exp(-(x-y)^2/(4kt)) dy.
    Uses Gaussian initial conditions for analytic evaluation.

    Input format:
        ``solve heat equation on R by Fourier transform``

    Target format:
        ``u_t = 2u_xx, u(x,0) = exp(-x^2) <step>
        heat kernel: K(x,t) = 1/sqrt(4*pi*2*t) * exp(-x^2/(4*2*t))
        <step> convolution with Gaussian <step>
        u(x,t) = 1/sqrt(1+4*2*t) * exp(-x^2/(1+4*2*t))
        <step> u(0.5, 1) = ...``

    Difficulty scaling:
        Difficulty 1-3: sigma=1, small k, simple evaluation point.
        Difficulty 4-6: variable sigma, moderate k.
        Difficulty 7-8: larger parameters, off-centre evaluation.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fourier_transform_pde"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Natural language description.
        """
        return "solve heat equation on R by Fourier transform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fourier-transform heat equation problem.

        Uses u(x,0) = A*exp(-x^2/(2*sigma^2)). The convolution with
        the heat kernel gives an analytic closed form.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.choice([1, 2])
            sigma = 1.0
            amp = 1
            x_val = 0.0
        elif difficulty <= 6:
            k = self._rng.choice([1, 2, 3])
            sigma = self._rng.choice([0.5, 1.0, 2.0])
            amp = self._rng.randint(1, 3)
            x_val = round(self._rng.choice([0.0, 0.5, 1.0]), 2)
        else:
            k = self._rng.choice([2, 3, 4])
            sigma = self._rng.choice([0.5, 1.0, 1.5])
            amp = self._rng.randint(1, 4)
            x_val = round(self._rng.choice([0.5, 1.0, 1.5, 2.0]), 2)

        t_val = round(self._rng.choice([0.1, 0.25, 0.5, 1.0]), 2)

        # u(x,0) = A * exp(-x^2/(2*sigma^2))
        # Convolution with heat kernel: u(x,t) = A*sigma/sqrt(sigma^2+2kt)
        #   * exp(-x^2 / (2*(sigma^2+2kt)))
        var = sigma ** 2 + 2 * k * t_val
        scale = amp * sigma / math.sqrt(var)
        u_val = scale * math.exp(-x_val ** 2 / (2 * var))

        kernel_denom = math.sqrt(4 * math.pi * k * t_val)

        problem = (f"u_t = {k}u_{{xx}}, "
                   f"u(x,0) = {amp}\\exp(-x^2/{_fmt(2 * sigma**2)})")
        return problem, {
            "k": k, "sigma": sigma, "amp": amp,
            "x": x_val, "t": t_val,
            "var": var, "scale": scale,
            "kernel_denom": kernel_denom, "u_val": u_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fourier transform PDE solution steps.

        Args:
            data: Solution data with convolution results.

        Returns:
            Steps showing heat kernel and convolution.
        """
        return [
            f"K(x,t) = 1/sqrt(4*pi*{data['k']}*{_fmt(data['t'])})"
            f" * exp(-x^2/(4*{data['k']}*{_fmt(data['t'])}))",
            f"sigma^2 + 2kt = {_fmt(data['var'])}",
            f"scale = {data['amp']}*{_fmt(data['sigma'])}"
            f"/sqrt({_fmt(data['var'])}) = {_fmt(data['scale'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted solution u(x, t).
        """
        return f"u({_fmt(data['x'])},{_fmt(data['t'])})={_fmt(data['u_val'])}"


# ── 8. Finite difference (tier 6) ────────────────────────────────────


@register
class FiniteDifferenceGenerator(StepGenerator):
    """Discretise u_xx using central finite differences.

    Approximates u_xx ~ (u_{i+1} - 2u_i + u_{i-1}) / h^2. Sets up
    the linear system for -u'' = f on [0, 1] with u(0) = u(1) = 0,
    using n interior grid points.

    Input format:
        ``discretise u_xx using finite differences``

    Target format:
        ``-u''=f on [0,1], n=3, h=0.25, f(x)=1 <step>
        u_1: (-2u_1+u_2)/h^2 = f(0.25) <step>
        u_2: (u_1-2u_2+u_3)/h^2 = f(0.5) <step>
        u_3: (u_2-2u_3)/h^2 = f(0.75)
        <step> solve: u_1=0.0938, u_2=0.125, u_3=0.0938``

    Difficulty scaling:
        Difficulty 1-3: n=2-3 interior points, f(x)=constant.
        Difficulty 4-6: n=3-4 interior points, f(x)=x or 1.
        Difficulty 7-8: n=4-5 interior points, f(x)=A*x+B.

    Prerequisites:
        numerical_derivative (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "finite_difference"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["numerical_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls grid size and source function.

        Returns:
            Natural language description.
        """
        return "discretise u_xx using finite differences"

    def _eval_source(self, x: float, f_type: str,
                     f_params: tuple) -> float:
        """Evaluate the source function f(x).

        Args:
            x: Grid point coordinate.
            f_type: Source type ('const', 'linear', 'affine').
            f_params: Source parameters.

        Returns:
            Value of f(x).
        """
        if f_type == "const":
            return float(f_params[0])
        if f_type == "linear":
            return x
        # affine: A*x + B
        return f_params[0] * x + f_params[1]

    def _solve_tridiag(self, n: int, h: float,
                       rhs: list[float]) -> list[float]:
        """Solve the tridiagonal system from -u'' discretisation.

        The matrix is (1/h^2) * tridiag(-1, 2, -1).

        Args:
            n: Number of interior points.
            h: Grid spacing.
            rhs: Right-hand side values at interior points.

        Returns:
            Solution values at interior points.
        """
        # Scale RHS by h^2: Au = h^2 * f where A = tridiag(-1,2,-1)
        b = [2.0] * n
        a_sub = [-1.0] * (n - 1)
        c_sup = [-1.0] * (n - 1)
        d = [h ** 2 * r for r in rhs]

        # Forward elimination
        for i in range(1, n):
            m = a_sub[i - 1] / b[i - 1]
            b[i] -= m * c_sup[i - 1]
            d[i] -= m * d[i - 1]

        # Back substitution
        x = [0.0] * n
        x[n - 1] = d[n - 1] / b[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = (d[i] - c_sup[i] * x[i + 1]) / b[i]

        return x

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a finite difference discretisation problem.

        Args:
            difficulty: Controls grid size and source function.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([2, 3])
            c = self._rng.randint(1, 4)
            f_type = "const"
            f_params = (c,)
            f_latex = str(c)
        elif difficulty <= 6:
            n = self._rng.choice([3, 4])
            f_type = self._rng.choice(["const", "linear"])
            if f_type == "const":
                c = self._rng.randint(1, 5)
                f_params = (c,)
                f_latex = str(c)
            else:
                f_params = ()
                f_latex = "x"
        else:
            n = self._rng.choice([4, 5])
            a_coeff = self._rng.randint(1, 3)
            b_coeff = self._rng.randint(1, 3)
            f_type = "affine"
            f_params = (a_coeff, b_coeff)
            f_latex = f"{a_coeff}x+{b_coeff}"

        h = 1.0 / (n + 1)
        grid = [round((i + 1) * h, 4) for i in range(n)]
        rhs = [self._eval_source(xi, f_type, f_params) for xi in grid]

        solution = self._solve_tridiag(n, h, rhs)

        problem = f"-u''={f_latex} on [0,1], n={n}, h={_fmt(h)}"
        return problem, {
            "n": n, "h": h, "grid": grid, "rhs": rhs,
            "f_latex": f_latex, "solution": solution,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate finite difference setup steps.

        Args:
            data: Solution data with grid and system.

        Returns:
            Steps showing discretisation equations.
        """
        steps = [f"h={_fmt(data['h'])}, {data['n']} interior points"]
        for i, xi in enumerate(data["grid"]):
            steps.append(
                f"x_{i+1}={_fmt(xi)}: f={_fmt(data['rhs'][i])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the finite difference solution values.

        Args:
            data: Solution data.

        Returns:
            Formatted solution at interior points.
        """
        parts = [f"u_{i+1}={_fmt(v)}" for i, v in enumerate(data["solution"])]
        return ", ".join(parts)
