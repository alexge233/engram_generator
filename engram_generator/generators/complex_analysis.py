"""Complex analysis generators for tier 6-7.

Provides generators for Cauchy-Riemann verification, complex power series,
residue computation, contour integrals via the residue theorem, analyticity
checks, Mobius transforms, Laurent series, and pole classification. Each
generator produces step-by-step solutions with LaTeX formatting suitable
for training sequence models.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Helper classes ────────────────────────────────────────────────────


class ComplexPolynomial:
    """Represents f(z) = (a + bi)z^n for Cauchy-Riemann problems.

    Splits f(z) into real part u(x, y) and imaginary part v(x, y)
    and computes partial derivatives for CR equation verification.

    Attributes:
        a: Real coefficient.
        b: Imaginary coefficient.
        n: Exponent (1, 2, or 3).
    """

    def __init__(self, a: int, b: int, n: int) -> None:
        """Initialise with complex coefficient and exponent.

        Args:
            a: Real part of coefficient.
            b: Imaginary part of coefficient.
            n: Exponent of z.
        """
        self._a = a
        self._b = b
        self._n = n

    @property
    def a(self) -> int:
        """Return the real coefficient."""
        return self._a

    @property
    def b(self) -> int:
        """Return the imaginary coefficient."""
        return self._b

    @property
    def n(self) -> int:
        """Return the exponent."""
        return self._n

    def f_latex(self) -> str:
        """Format f(z) in LaTeX.

        Returns:
            LaTeX string for the function.
        """
        coeff = self._coeff_latex()
        if self._n == 1:
            return f"{coeff}z"
        return f"{coeff}z^{{{self._n}}}"

    def u_v_expressions(self, x_val: float,
                        y_val: float) -> tuple[float, float]:
        """Evaluate u and v at (x, y) by expanding (x + iy)^n.

        Args:
            x_val: Real part.
            y_val: Imaginary part.

        Returns:
            Tuple of (u, v) evaluated at the point.
        """
        zr, zi = self._power_xy(x_val, y_val)
        u = self._a * zr - self._b * zi
        v = self._a * zi + self._b * zr
        return u, v

    def partial_derivatives(self, x_val: float,
                            y_val: float) -> dict[str, float]:
        """Compute u_x, u_y, v_x, v_y numerically.

        Args:
            x_val: Real part.
            y_val: Imaginary part.

        Returns:
            Dict with keys u_x, u_y, v_x, v_y.
        """
        h = 1e-7
        u0, v0 = self.u_v_expressions(x_val, y_val)
        u_xh, v_xh = self.u_v_expressions(x_val + h, y_val)
        u_yh, v_yh = self.u_v_expressions(x_val, y_val + h)
        return {
            "u_x": (u_xh - u0) / h,
            "u_y": (u_yh - u0) / h,
            "v_x": (v_xh - v0) / h,
            "v_y": (v_yh - v0) / h,
        }

    def _power_xy(self, x: float, y: float) -> tuple[float, float]:
        """Compute (x + iy)^n as (real, imag).

        Args:
            x: Real part.
            y: Imaginary part.

        Returns:
            Tuple of (real_part, imag_part).
        """
        zr, zi = x, y
        rr, ri = 1.0, 0.0
        for _ in range(self._n):
            rr, ri = rr * zr - ri * zi, rr * zi + ri * zr
        return rr, ri

    def _coeff_latex(self) -> str:
        """Format the complex coefficient as LaTeX.

        Returns:
            LaTeX string for (a + bi).
        """
        if self._b == 0:
            return str(self._a)
        if self._a == 0:
            if self._b == 1:
                return "i"
            if self._b == -1:
                return "-i"
            return f"{self._b}i"
        sign = "+" if self._b > 0 else "-"
        bi = abs(self._b) if abs(self._b) != 1 else ""
        return f"({self._a}{sign}{bi}i)"


class RationalComplex:
    """Represents f(z) = P(z)/Q(z) with polynomial numerator and denominator.

    Stores P and Q as lists of (coefficient, exponent) pairs sorted by
    descending exponent. Provides evaluation, derivative computation,
    and LaTeX formatting for residue and contour integral problems.

    Attributes:
        p_terms: Numerator terms as (coeff, exp) pairs.
        q_terms: Denominator terms as (coeff, exp) pairs.
    """

    def __init__(self, p_terms: list[tuple[int, int]],
                 q_terms: list[tuple[int, int]]) -> None:
        """Initialise with numerator and denominator terms.

        Args:
            p_terms: Numerator as list of (coefficient, exponent).
            q_terms: Denominator as list of (coefficient, exponent).
        """
        self._p_terms = sorted(p_terms, key=lambda t: -t[1])
        self._q_terms = sorted(q_terms, key=lambda t: -t[1])

    @property
    def p_terms(self) -> list[tuple[int, int]]:
        """Return the numerator terms."""
        return list(self._p_terms)

    @property
    def q_terms(self) -> list[tuple[int, int]]:
        """Return the denominator terms."""
        return list(self._q_terms)

    def eval_poly(self, terms: list[tuple[int, int]],
                  zr: float, zi: float) -> tuple[float, float]:
        """Evaluate a polynomial at complex z = zr + zi*i.

        Args:
            terms: Polynomial as (coefficient, exponent) pairs.
            zr: Real part of z.
            zi: Imaginary part of z.

        Returns:
            Tuple of (real, imag) of the polynomial value.
        """
        result_r, result_i = 0.0, 0.0
        for coeff, exp in terms:
            pr, pi = self._complex_pow(zr, zi, exp)
            result_r += coeff * pr
            result_i += coeff * pi
        return result_r, result_i

    def eval_p(self, zr: float, zi: float) -> tuple[float, float]:
        """Evaluate numerator P(z).

        Args:
            zr: Real part of z.
            zi: Imaginary part of z.

        Returns:
            Tuple of (real, imag).
        """
        return self.eval_poly(self._p_terms, zr, zi)

    def eval_q(self, zr: float, zi: float) -> tuple[float, float]:
        """Evaluate denominator Q(z).

        Args:
            zr: Real part of z.
            zi: Imaginary part of z.

        Returns:
            Tuple of (real, imag).
        """
        return self.eval_poly(self._q_terms, zr, zi)

    def q_derivative_terms(self) -> list[tuple[int, int]]:
        """Compute Q'(z) by differentiating each term.

        Returns:
            Derivative terms as (coefficient, exponent) pairs.
        """
        deriv: list[tuple[int, int]] = []
        for coeff, exp in self._q_terms:
            if exp > 0:
                deriv.append((coeff * exp, exp - 1))
        return deriv

    def eval_q_prime(self, zr: float, zi: float) -> tuple[float, float]:
        """Evaluate Q'(z) at complex z.

        Args:
            zr: Real part of z.
            zi: Imaginary part of z.

        Returns:
            Tuple of (real, imag).
        """
        return self.eval_poly(self.q_derivative_terms(), zr, zi)

    def p_latex(self) -> str:
        """Format numerator P(z) in LaTeX.

        Returns:
            LaTeX string for P(z).
        """
        return self._poly_latex(self._p_terms)

    def q_latex(self) -> str:
        """Format denominator Q(z) in LaTeX.

        Returns:
            LaTeX string for Q(z).
        """
        return self._poly_latex(self._q_terms)

    def q_prime_latex(self) -> str:
        """Format Q'(z) in LaTeX.

        Returns:
            LaTeX string for Q'(z).
        """
        return self._poly_latex(self.q_derivative_terms())

    def _poly_latex(self, terms: list[tuple[int, int]]) -> str:
        """Format a polynomial in LaTeX from term pairs.

        Args:
            terms: List of (coefficient, exponent) pairs.

        Returns:
            LaTeX string for the polynomial.
        """
        if not terms:
            return "0"
        parts: list[str] = []
        for i, (coeff, exp) in enumerate(terms):
            if coeff == 0:
                continue
            parts.append(self._term_latex(coeff, exp, i == 0))
        return "".join(parts) if parts else "0"

    def _term_latex(self, coeff: int, exp: int,
                    is_first: bool) -> str:
        """Format a single polynomial term as LaTeX.

        Args:
            coeff: Term coefficient.
            exp: Term exponent.
            is_first: Whether this is the leading term.

        Returns:
            LaTeX string for the term.
        """
        if coeff == 0:
            return ""
        sign = "" if is_first and coeff > 0 else ("+" if coeff > 0 else "")
        if exp == 0:
            return f"{sign}{coeff}"
        abs_c = abs(coeff)
        neg = "-" if coeff < 0 else sign
        if exp == 1:
            body = "z" if abs_c == 1 else f"{abs_c}z"
        else:
            body = f"z^{{{exp}}}" if abs_c == 1 else f"{abs_c}z^{{{exp}}}"
        return f"{neg}{body}"

    def _complex_pow(self, zr: float, zi: float,
                     n: int) -> tuple[float, float]:
        """Compute (zr + zi*i)^n.

        Args:
            zr: Real part.
            zi: Imaginary part.
            n: Non-negative exponent.

        Returns:
            Tuple of (real, imag).
        """
        if n == 0:
            return 1.0, 0.0
        rr, ri = 1.0, 0.0
        for _ in range(n):
            rr, ri = rr * zr - ri * zi, rr * zi + ri * zr
        return rr, ri


# ── Formatting helpers ────────────────────────────────────────────────


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


def _fmt_complex(r: float, i: float) -> str:
    """Format a complex number as a string.

    Args:
        r: Real part.
        i: Imaginary part.

    Returns:
        String like '3+2i' or '-1-4i'.
    """
    rs = _fmt(r)
    i_val = round(i, 4)
    if abs(i_val) < 1e-10:
        return rs
    if abs(round(r, 4)) < 1e-10:
        if abs(i_val - 1.0) < 1e-10:
            return "i"
        if abs(i_val + 1.0) < 1e-10:
            return "-i"
        return f"{_fmt(i_val)}i"
    sign = "+" if i_val > 0 else "-"
    ai = abs(i_val)
    is_part = "i" if abs(ai - 1.0) < 1e-10 else f"{_fmt(ai)}i"
    return f"{rs}{sign}{is_part}"


def _complex_div(ar: float, ai: float,
                 br: float, bi: float) -> tuple[float, float]:
    """Divide complex (ar+ai*i) by (br+bi*i).

    Args:
        ar: Real part of numerator.
        ai: Imaginary part of numerator.
        br: Real part of denominator.
        bi: Imaginary part of denominator.

    Returns:
        Tuple of (real, imag) of the quotient.
    """
    denom = br * br + bi * bi
    return (ar * br + ai * bi) / denom, (ai * br - ar * bi) / denom


# ── Generators ────────────────────────────────────────────────────────


@register
class CauchyRiemannGenerator(StepGenerator):
    """Verify Cauchy-Riemann equations u_x=v_y, u_y=-v_x for f(z)=u+iv.

    Generates a complex polynomial f(z) = (a+bi)z^n, splits into real
    and imaginary parts, and verifies the CR equations numerically at
    a randomly chosen point (x, y).

    Input format:
        ``verify Cauchy-Riemann equations``

    Target format:
        ``f(z)=(2+i)z^{2} <step> evaluate at (1,2) <step>
        u_x=... v_y=... <step> u_y=... -v_x=... <step>
        u_x=v_y and u_y=-v_x: CR satisfied``

    Difficulty scaling:
        Difficulty 1-3: n=1, small coefficients.
        Difficulty 4-6: n=2, moderate coefficients.
        Difficulty 7-8: n=3, larger coefficients.

    Prerequisites:
        partial_derivative, complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cauchy_riemann"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative", "complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls exponent and coefficient range.

        Returns:
            Natural language description.
        """
        return "verify Cauchy-Riemann equations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complex polynomial and verify CR at a point.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, c_hi = self._params(difficulty)
        a = self._rng.randint(1, c_hi)
        b = self._rng.randint(-c_hi, c_hi)
        if b == 0:
            b = 1
        poly = ComplexPolynomial(a, b, n)
        x_val = self._rng.randint(1, 3)
        y_val = self._rng.randint(1, 3)
        partials = poly.partial_derivatives(float(x_val), float(y_val))
        problem = f"\\text{{CR: }} f(z)={poly.f_latex()}"
        return problem, {
            "poly": poly, "x": x_val, "y": y_val, "partials": partials,
        }

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to exponent and coefficient bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (exponent, max_coefficient).
        """
        if difficulty <= 3:
            return 1, 3
        if difficulty <= 6:
            return 2, 5
        return 3, 7

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CR verification steps.

        Args:
            data: Solution data with polynomial and partials.

        Returns:
            Steps showing partial derivatives and CR check.
        """
        x, y = data["x"], data["y"]
        p = data["partials"]
        return [
            f"evaluate at ({x},{y})",
            f"u_x={_fmt(p['u_x'])}, v_y={_fmt(p['v_y'])}",
            f"u_y={_fmt(p['u_y'])}, -v_x={_fmt(-p['v_x'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether CR equations are satisfied.

        Args:
            data: Solution data.

        Returns:
            'CR satisfied' or 'CR not satisfied'.
        """
        p = data["partials"]
        eq1 = abs(p["u_x"] - p["v_y"]) < 1e-4
        eq2 = abs(p["u_y"] + p["v_x"]) < 1e-4
        return "CR satisfied" if eq1 and eq2 else "CR not satisfied"


@register
class ComplexPowerSeriesGenerator(StepGenerator):
    """Taylor series of e^z, sin(z), cos(z) about a point z_0.

    Computes the first n terms of the Taylor expansion of a standard
    complex function about a given complex centre z_0. Each step shows
    the coefficient computation and partial sum.

    Input format:
        ``compute complex power series``

    Target format:
        ``Taylor(e^z, z_0=1+i, n=4) <step> c_0=e^{z_0}=...
        <step> c_1=e^{z_0}=... <step> ... <step> sum=...``

    Difficulty scaling:
        Difficulty 1-3: n=3, z_0 real integer.
        Difficulty 4-6: n=4, z_0 complex with small imaginary part.
        Difficulty 7-8: n=5, z_0 complex.

    Prerequisites:
        taylor_series, complex_arithmetic.
    """

    _FUNCTIONS = ["exp", "sin", "cos"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "complex_power_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["taylor_series", "complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of terms and centre complexity.

        Returns:
            Natural language description.
        """
        return "compute complex power series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Taylor series problem for a complex function.

        Args:
            difficulty: Controls number of terms and z_0.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_terms, z0r, z0i = self._params(difficulty)
        func = self._rng.choice(self._FUNCTIONS)
        coeffs = self._compute_coeffs(func, z0r, z0i, n_terms)
        z0_str = _fmt_complex(z0r, z0i)
        problem = f"Taylor({func}(z), z_0={z0_str}, n={n_terms})"
        return problem, {
            "func": func, "z0r": z0r, "z0i": z0i,
            "n_terms": n_terms, "coeffs": coeffs,
        }

    def _params(self, difficulty: int) -> tuple[int, float, float]:
        """Map difficulty to number of terms and z_0 components.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_terms, z0_real, z0_imag).
        """
        if difficulty <= 3:
            n = 3
            z0r = float(self._rng.randint(0, 2))
            z0i = 0.0
        elif difficulty <= 6:
            n = 4
            z0r = float(self._rng.randint(-1, 2))
            z0i = float(self._rng.randint(0, 1))
        else:
            n = 5
            z0r = float(self._rng.randint(-2, 2))
            z0i = float(self._rng.randint(-1, 1))
            if z0i == 0:
                z0i = 1.0
        return n, z0r, z0i

    def _compute_coeffs(self, func: str, z0r: float, z0i: float,
                        n: int) -> list[tuple[float, float]]:
        """Compute Taylor coefficients c_k = f^(k)(z_0) / k!.

        For exp, sin, cos the k-th derivative cycles through known patterns.

        Args:
            func: Function name ('exp', 'sin', or 'cos').
            z0r: Real part of centre.
            z0i: Imaginary part of centre.
            n: Number of terms.

        Returns:
            List of (real, imag) coefficient tuples.
        """
        coeffs: list[tuple[float, float]] = []
        for k in range(n):
            dr, di = self._kth_derivative(func, z0r, z0i, k)
            fac = math.factorial(k)
            coeffs.append((dr / fac, di / fac))
        return coeffs

    def _kth_derivative(self, func: str, zr: float, zi: float,
                        k: int) -> tuple[float, float]:
        """Compute f^(k)(z) for the standard functions.

        Args:
            func: Function name.
            zr: Real part.
            zi: Imaginary part.
            k: Derivative order.

        Returns:
            Tuple of (real, imag) of the k-th derivative value.
        """
        if func == "exp":
            return self._complex_exp(zr, zi)
        if func == "sin":
            phase = k % 4
            sr, si = self._complex_sin(zr, zi)
            cr, ci = self._complex_cos(zr, zi)
            if phase == 0:
                return sr, si
            if phase == 1:
                return cr, ci
            if phase == 2:
                return -sr, -si
            return -cr, -ci
        # cos
        phase = k % 4
        cr, ci = self._complex_cos(zr, zi)
        sr, si = self._complex_sin(zr, zi)
        if phase == 0:
            return cr, ci
        if phase == 1:
            return -sr, -si
        if phase == 2:
            return -cr, -ci
        return sr, si

    def _complex_exp(self, zr: float, zi: float) -> tuple[float, float]:
        """Compute e^z for complex z.

        Args:
            zr: Real part.
            zi: Imaginary part.

        Returns:
            Tuple of (real, imag).
        """
        mag = math.exp(zr)
        return mag * math.cos(zi), mag * math.sin(zi)

    def _complex_sin(self, zr: float, zi: float) -> tuple[float, float]:
        """Compute sin(z) for complex z.

        Args:
            zr: Real part.
            zi: Imaginary part.

        Returns:
            Tuple of (real, imag).
        """
        return (math.sin(zr) * math.cosh(zi),
                math.cos(zr) * math.sinh(zi))

    def _complex_cos(self, zr: float, zi: float) -> tuple[float, float]:
        """Compute cos(z) for complex z.

        Args:
            zr: Real part.
            zi: Imaginary part.

        Returns:
            Tuple of (real, imag).
        """
        return (math.cos(zr) * math.cosh(zi),
                -math.sin(zr) * math.sinh(zi))

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-coefficient steps.

        Args:
            data: Solution data with coefficients.

        Returns:
            Steps showing each Taylor coefficient.
        """
        steps: list[str] = []
        for k, (cr, ci) in enumerate(data["coeffs"]):
            steps.append(f"c_{{{k}}}={_fmt_complex(cr, ci)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the partial sum as a formatted complex number.

        Args:
            data: Solution data.

        Returns:
            String showing the sum of computed coefficients.
        """
        total_r = sum(c[0] for c in data["coeffs"])
        total_i = sum(c[1] for c in data["coeffs"])
        return f"sum={_fmt_complex(total_r, total_i)}"


@register
class ResidueComputeGenerator(StepGenerator):
    """Compute residue of f(z)=P(z)/Q(z) at a simple pole z_0.

    Uses the formula Res(f, z_0) = P(z_0) / Q'(z_0) for simple poles.
    Generates rational functions with known simple poles and computes
    the residue step by step.

    Input format:
        ``compute residue at simple pole``

    Target format:
        ``Res(f, z_0=2) where f(z)=z/(z^{2}-4) <step>
        P(z_0)=2 <step> Q'(z)=2z <step> Q'(z_0)=4 <step>
        Res=P(z_0)/Q'(z_0)=0.5``

    Difficulty scaling:
        Difficulty 1-3: linear P, quadratic Q with integer roots.
        Difficulty 4-6: quadratic P, cubic Q.
        Difficulty 7-8: cubic P, degree-4 Q.

    Prerequisites:
        complex_power_series.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "residue_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_power_series"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial degrees.

        Returns:
            Natural language description.
        """
        return "compute residue at simple pole"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rational function with a known simple pole.

        Constructs Q(z) as a product of distinct linear factors so
        that each root is a simple pole.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        roots, p_terms = self._build_problem(difficulty)
        z0 = roots[0]
        q_terms = self._roots_to_poly(roots)
        rc = RationalComplex(p_terms, q_terms)

        pr, pi = rc.eval_p(float(z0), 0.0)
        qpr, qpi = rc.eval_q_prime(float(z0), 0.0)
        res_r, res_i = _complex_div(pr, pi, qpr, qpi)

        problem = (
            f"Res(f, z_0={z0}), "
            f"f(z)=\\frac{{{rc.p_latex()}}}{{{rc.q_latex()}}}"
        )
        return problem, {
            "rc": rc, "z0": z0,
            "p_val": (pr, pi), "qp_val": (qpr, qpi),
            "residue": (res_r, res_i),
        }

    def _build_problem(self, difficulty: int) -> tuple[list[int],
                                                       list[tuple[int, int]]]:
        """Choose roots for Q and terms for P based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (roots_list, p_terms).
        """
        if difficulty <= 3:
            n_roots = 2
            p_deg = 0
            bound = 3
        elif difficulty <= 6:
            n_roots = 3
            p_deg = 1
            bound = 4
        else:
            n_roots = 4
            p_deg = 2
            bound = 5
        roots = self._distinct_roots(n_roots, bound)
        p_terms = self._random_p(p_deg, bound)
        return roots, p_terms

    def _distinct_roots(self, n: int, bound: int) -> list[int]:
        """Generate n distinct integer roots in [-bound, bound].

        Args:
            n: Number of roots.
            bound: Absolute value bound.

        Returns:
            List of distinct integer roots.
        """
        roots: list[int] = []
        for _ in range(200):
            r = self._rng.randint(-bound, bound)
            if r not in roots:
                roots.append(r)
            if len(roots) == n:
                break
        return roots

    def _random_p(self, deg: int, bound: int) -> list[tuple[int, int]]:
        """Generate random numerator polynomial terms.

        Args:
            deg: Maximum degree.
            bound: Coefficient bound.

        Returns:
            List of (coefficient, exponent) pairs.
        """
        terms: list[tuple[int, int]] = []
        for e in range(deg, -1, -1):
            c = self._rng.randint(1, bound)
            terms.append((c, e))
        return terms

    def _roots_to_poly(self, roots: list[int]) -> list[tuple[int, int]]:
        """Expand product of (z - r_i) into polynomial terms.

        Args:
            roots: List of integer roots.

        Returns:
            Polynomial as list of (coefficient, exponent) pairs.
        """
        coeffs = [1]
        for r in roots:
            new_coeffs = [0] * (len(coeffs) + 1)
            for i, c in enumerate(coeffs):
                new_coeffs[i] += c
                new_coeffs[i + 1] -= c * r
            coeffs = new_coeffs
        deg = len(coeffs) - 1
        return [(c, deg - i) for i, c in enumerate(coeffs) if c != 0]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate residue computation steps.

        Args:
            data: Solution data with P, Q', and residue values.

        Returns:
            Steps showing P(z_0), Q'(z_0), and the residue.
        """
        z0 = data["z0"]
        pr, pi = data["p_val"]
        qpr, qpi = data["qp_val"]
        rc = data["rc"]
        return [
            f"P({z0})={_fmt_complex(pr, pi)}",
            f"Q'(z)={rc.q_prime_latex()}",
            f"Q'({z0})={_fmt_complex(qpr, qpi)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the residue value.

        Args:
            data: Solution data.

        Returns:
            Formatted residue string.
        """
        rr, ri = data["residue"]
        return f"Res={_fmt_complex(rr, ri)}"


@register
class ContourIntegralGenerator(StepGenerator):
    """Evaluate contour integral using the residue theorem.

    Computes the integral of P(z)/Q(z) around a circle |z|=R using
    2*pi*i * sum(residues inside the contour). Identifies which poles
    lie inside the contour and sums their residues.

    Input format:
        ``evaluate contour integral via residue theorem``

    Target format:
        ``\\oint_{|z|=R} f(z)dz <step> poles: z=... <step>
        inside |z|=R: z=... <step> Res(f,z_k)=... <step>
        integral=2*pi*i*sum``

    Difficulty scaling:
        Difficulty 1-3: 2 poles, R chosen so 1 is inside.
        Difficulty 4-6: 3 poles, R chosen so 1-2 are inside.
        Difficulty 7-8: 4 poles, R chosen so 2-3 are inside.

    Prerequisites:
        residue_compute.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "contour_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["residue_compute"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of poles.

        Returns:
            Natural language description.
        """
        return "evaluate contour integral via residue theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a contour integral problem with known poles.

        Args:
            difficulty: Controls number of poles and contour radius.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_poles, bound = self._params(difficulty)
        roots = self._distinct_roots(n_poles, bound)
        p_terms = [(1, 0)]
        q_terms = self._roots_to_poly(roots)
        rc = RationalComplex(p_terms, q_terms)

        radius = self._choose_radius(roots)
        inside = [r for r in roots if abs(r) < radius]

        residues: list[tuple[int, float, float]] = []
        for r in inside:
            pr, pi = rc.eval_p(float(r), 0.0)
            qpr, qpi = rc.eval_q_prime(float(r), 0.0)
            rr, ri = _complex_div(pr, pi, qpr, qpi)
            residues.append((r, rr, ri))

        sum_r = sum(res[1] for res in residues)
        sum_i = sum(res[2] for res in residues)
        int_r = -2 * math.pi * sum_i
        int_i = 2 * math.pi * sum_r

        problem = (
            f"\\oint_{{|z|={radius}}} "
            f"\\frac{{{rc.p_latex()}}}{{{rc.q_latex()}}} dz"
        )
        return problem, {
            "rc": rc, "roots": roots, "radius": radius,
            "inside": inside, "residues": residues,
            "sum_res": (sum_r, sum_i), "integral": (int_r, int_i),
        }

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to number of poles and root bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_poles, bound).
        """
        if difficulty <= 3:
            return 2, 3
        if difficulty <= 6:
            return 3, 4
        return 4, 5

    def _distinct_roots(self, n: int, bound: int) -> list[int]:
        """Generate n distinct nonzero integer roots.

        Args:
            n: Number of roots.
            bound: Absolute value bound.

        Returns:
            List of distinct nonzero roots.
        """
        roots: list[int] = []
        for _ in range(200):
            r = self._rng.randint(-bound, bound)
            if r != 0 and r not in roots:
                roots.append(r)
            if len(roots) == n:
                break
        return roots

    def _roots_to_poly(self, roots: list[int]) -> list[tuple[int, int]]:
        """Expand product of (z - r_i) into polynomial terms.

        Args:
            roots: List of integer roots.

        Returns:
            Polynomial as list of (coefficient, exponent) pairs.
        """
        coeffs = [1]
        for r in roots:
            new_coeffs = [0] * (len(coeffs) + 1)
            for i, c in enumerate(coeffs):
                new_coeffs[i] += c
                new_coeffs[i + 1] -= c * r
            coeffs = new_coeffs
        deg = len(coeffs) - 1
        return [(c, deg - i) for i, c in enumerate(coeffs) if c != 0]

    def _choose_radius(self, roots: list[int]) -> int:
        """Choose a contour radius that includes some but not all poles.

        Args:
            roots: List of pole locations (real integers).

        Returns:
            Integer radius for |z| = R.
        """
        abs_roots = sorted(set(abs(r) for r in roots))
        if len(abs_roots) >= 2:
            cutoff_idx = self._rng.randint(0, len(abs_roots) - 2)
            return abs_roots[cutoff_idx] + 1
        return abs_roots[0] + 1

    def _create_steps(self, data: dict) -> list[str]:
        """Generate residue theorem application steps.

        Args:
            data: Solution data with poles, residues, and integral.

        Returns:
            Steps showing pole identification and residue summation.
        """
        roots_str = ", ".join(str(r) for r in data["roots"])
        inside_str = ", ".join(str(r) for r in data["inside"])
        steps = [
            f"poles: z={roots_str}",
            f"inside |z|={data['radius']}: z={inside_str}",
        ]
        for r, rr, ri in data["residues"]:
            steps.append(f"Res(f,{r})={_fmt_complex(rr, ri)}")
        sr, si = data["sum_res"]
        steps.append(f"sum(Res)={_fmt_complex(sr, si)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the contour integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted integral value as 2*pi*i * sum(Res).
        """
        ir, ii = data["integral"]
        return f"integral={_fmt_complex(ir, ii)}"


@register
class AnalyticCheckGenerator(StepGenerator):
    """Determine if a function satisfies the CR equations (is analytic).

    Tests functions of the form f(z) = (a+bi)z^n (analytic) or
    f(z) = a*conj(z) (not analytic) by computing partial derivatives
    and checking the Cauchy-Riemann conditions.

    Input format:
        ``check if function is analytic``

    Target format:
        ``f(z)=conj(z) <step> u=x, v=-y <step>
        u_x=1, v_y=-1 <step> u_x != v_y <step> not analytic``

    Difficulty scaling:
        Difficulty 1-3: simple z^n or conj(z).
        Difficulty 4-6: (a+bi)z^n or a*conj(z)+b.
        Difficulty 7-8: mixed forms with larger coefficients.

    Prerequisites:
        cauchy_riemann.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "analytic_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cauchy_riemann"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "check if function is analytic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a function and test analyticity via CR equations.

        Args:
            difficulty: Controls function form.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        use_analytic = self._rng.choice([True, False])
        c_hi = self._coeff_bound(difficulty)
        x_val, y_val = float(self._rng.randint(1, 3)), float(self._rng.randint(1, 3))

        if use_analytic:
            n = 1 if difficulty <= 3 else self._rng.randint(1, 2)
            a = self._rng.randint(1, c_hi)
            b = self._rng.randint(-c_hi, c_hi)
            if b == 0:
                b = 1
            func_str = ComplexPolynomial(a, b, n).f_latex()
            u_x, u_y, v_x, v_y = self._analytic_partials(a, b, n, x_val, y_val)
        else:
            a = self._rng.randint(1, c_hi)
            func_str = f"{a}\\overline{{z}}" if a != 1 else "\\overline{z}"
            u_x = float(a)
            u_y = 0.0
            v_x = 0.0
            v_y = float(-a)

        is_analytic = abs(u_x - v_y) < 1e-4 and abs(u_y + v_x) < 1e-4
        problem = f"\\text{{analytic? }} f(z)={func_str}"
        return problem, {
            "func_str": func_str, "x": x_val, "y": y_val,
            "u_x": u_x, "u_y": u_y, "v_x": v_x, "v_y": v_y,
            "is_analytic": is_analytic,
        }

    def _coeff_bound(self, difficulty: int) -> int:
        """Map difficulty to coefficient bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Maximum coefficient value.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 5
        return 7

    def _analytic_partials(self, a: int, b: int, n: int,
                           x: float, y: float) -> tuple[float, float,
                                                         float, float]:
        """Compute CR partials for (a+bi)z^n.

        Args:
            a: Real coefficient.
            b: Imaginary coefficient.
            n: Exponent.
            x: Real evaluation point.
            y: Imaginary evaluation point.

        Returns:
            Tuple of (u_x, u_y, v_x, v_y).
        """
        poly = ComplexPolynomial(a, b, n)
        p = poly.partial_derivatives(x, y)
        return p["u_x"], p["u_y"], p["v_x"], p["v_y"]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate analyticity check steps.

        Args:
            data: Solution data with partial derivatives.

        Returns:
            Steps showing CR equation evaluation.
        """
        return [
            f"at ({_fmt(data['x'])},{_fmt(data['y'])})",
            f"u_x={_fmt(data['u_x'])}, v_y={_fmt(data['v_y'])}",
            f"u_y={_fmt(data['u_y'])}, -v_x={_fmt(-data['v_x'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether the function is analytic.

        Args:
            data: Solution data.

        Returns:
            'analytic' or 'not analytic'.
        """
        return "analytic" if data["is_analytic"] else "not analytic"


@register
class MobiusTransformGenerator(StepGenerator):
    """Apply Mobius transformation (az+b)/(cz+d) to a complex number.

    Generates integer coefficients a, b, c, d with ad-bc != 0 and
    a complex input z, then computes the image w = (az+b)/(cz+d)
    step by step.

    Input format:
        ``apply Mobius transformation``

    Target format:
        ``T(z)=(2z+1)/(z+3), z=1+i <step> num=2(1+i)+1=3+2i
        <step> den=(1+i)+3=4+i <step> w=(3+2i)/(4+i)=...``

    Difficulty scaling:
        Difficulty 1-3: real z, small coefficients.
        Difficulty 4-6: complex z, moderate coefficients.
        Difficulty 7-8: complex z, larger coefficients.

    Prerequisites:
        complex_division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mobius_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient and input complexity.

        Returns:
            Natural language description.
        """
        return "apply Mobius transformation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mobius transformation and compute its image.

        Args:
            difficulty: Controls coefficient range and input complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        for _ in range(100):
            a, b, c, d = self._choose_coefficients(difficulty)
            zr, zi = self._choose_input(difficulty)
            den_r = c * zr + d
            den_i = c * zi
            if den_r * den_r + den_i * den_i > 1e-12:
                break

        num_r = a * zr + b
        num_i = a * zi
        den_r = c * zr + d
        den_i = c * zi

        wr, wi = _complex_div(num_r, num_i, den_r, den_i)

        z_str = _fmt_complex(zr, zi)
        problem = (
            f"T(z)=\\frac{{{a}z+{b}}}{{{c}z+{d}}}, z={z_str}"
        )
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "zr": zr, "zi": zi,
            "num": (num_r, num_i), "den": (den_r, den_i),
            "w": (wr, wi),
        }

    def _choose_coefficients(self, difficulty: int) -> tuple[int, int,
                                                             int, int]:
        """Choose Mobius coefficients with ad - bc != 0.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (a, b, c, d).
        """
        hi = self._coeff_bound(difficulty)
        for _ in range(100):
            a = self._rng.randint(1, hi)
            b = self._rng.randint(-hi, hi)
            c = self._rng.randint(1, hi)
            d = self._rng.randint(-hi, hi)
            if a * d - b * c != 0:
                return a, b, c, d
        return 1, 0, 0, 1

    def _coeff_bound(self, difficulty: int) -> int:
        """Map difficulty to coefficient bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Upper bound for coefficients.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 5
        return 7

    def _choose_input(self, difficulty: int) -> tuple[float, float]:
        """Choose the input complex number z.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (real, imag) parts of z.
        """
        if difficulty <= 3:
            return float(self._rng.randint(1, 3)), 0.0
        return (float(self._rng.randint(-3, 3)),
                float(self._rng.randint(1, 3)))

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Mobius transformation steps.

        Args:
            data: Solution data with numerator, denominator, and result.

        Returns:
            Steps showing numerator, denominator, and division.
        """
        nr, ni = data["num"]
        dr, di = data["den"]
        return [
            f"num={data['a']}*{_fmt_complex(data['zr'], data['zi'])}+{data['b']}={_fmt_complex(nr, ni)}",
            f"den={data['c']}*{_fmt_complex(data['zr'], data['zi'])}+{data['d']}={_fmt_complex(dr, di)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Mobius transformation image.

        Args:
            data: Solution data.

        Returns:
            Formatted complex number.
        """
        wr, wi = data["w"]
        return f"T(z)={_fmt_complex(wr, wi)}"


@register
class LaurentSeriesGenerator(StepGenerator):
    """Find Laurent series at a singularity using partial fractions.

    Decomposes P(z)/Q(z) into partial fractions around a singularity
    z_0, extracting the principal part (negative powers of (z-z_0))
    and the regular part.

    Input format:
        ``find Laurent series at singularity``

    Target format:
        ``f(z)=1/((z-1)(z-2)) at z_0=1 <step>
        PF: A/(z-1)+B/(z-2) <step> A=..., B=... <step>
        principal: A/(z-1) <step> regular: B/(z-2) expanded``

    Difficulty scaling:
        Difficulty 1-3: 2 simple poles, constant numerator.
        Difficulty 4-6: 3 simple poles, linear numerator.
        Difficulty 7-8: 3-4 poles, quadratic numerator.

    Prerequisites:
        complex_power_series.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laurent_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_power_series"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of poles.

        Returns:
            Natural language description.
        """
        return "find Laurent series at singularity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rational function and compute its Laurent series.

        Uses partial fraction decomposition to find the principal part
        at the target singularity.

        Args:
            difficulty: Controls number of poles and numerator degree.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_poles, p_deg, bound = self._params(difficulty)
        roots = self._distinct_roots(n_poles, bound)
        z0 = roots[0]

        p_terms = self._random_p(p_deg, bound)
        q_terms = self._roots_to_poly(roots)
        rc = RationalComplex(p_terms, q_terms)

        pf_coeffs = self._partial_fractions(rc, roots)

        roots_str = ", ".join(str(r) for r in roots)
        problem = (
            f"Laurent(\\frac{{{rc.p_latex()}}}{{{rc.q_latex()}}}, z_0={z0})"
        )
        return problem, {
            "rc": rc, "z0": z0, "roots": roots,
            "pf_coeffs": pf_coeffs,
        }

    def _params(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to number of poles, numerator degree, and bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_poles, p_degree, bound).
        """
        if difficulty <= 3:
            return 2, 0, 3
        if difficulty <= 6:
            return 3, 1, 4
        return self._rng.randint(3, 4), 2, 5

    def _distinct_roots(self, n: int, bound: int) -> list[int]:
        """Generate n distinct nonzero integer roots.

        Args:
            n: Number of roots.
            bound: Absolute value bound.

        Returns:
            List of distinct nonzero integer roots.
        """
        roots: list[int] = []
        for _ in range(200):
            r = self._rng.randint(-bound, bound)
            if r != 0 and r not in roots:
                roots.append(r)
            if len(roots) == n:
                break
        return roots

    def _random_p(self, deg: int, bound: int) -> list[tuple[int, int]]:
        """Generate random numerator polynomial terms.

        Args:
            deg: Maximum degree.
            bound: Coefficient bound.

        Returns:
            List of (coefficient, exponent) pairs.
        """
        terms: list[tuple[int, int]] = []
        for e in range(deg, -1, -1):
            c = self._rng.randint(1, bound)
            terms.append((c, e))
        return terms

    def _roots_to_poly(self, roots: list[int]) -> list[tuple[int, int]]:
        """Expand product of (z - r_i) into polynomial terms.

        Args:
            roots: List of integer roots.

        Returns:
            Polynomial as list of (coefficient, exponent) pairs.
        """
        coeffs = [1]
        for r in roots:
            new_coeffs = [0] * (len(coeffs) + 1)
            for i, c in enumerate(coeffs):
                new_coeffs[i] += c
                new_coeffs[i + 1] -= c * r
            coeffs = new_coeffs
        deg = len(coeffs) - 1
        return [(c, deg - i) for i, c in enumerate(coeffs) if c != 0]

    def _partial_fractions(self, rc: RationalComplex,
                           roots: list[int]) -> list[tuple[int, float]]:
        """Compute partial fraction coefficients A_k = P(r_k) / Q'(r_k).

        Args:
            rc: Rational complex function.
            roots: Simple poles of Q.

        Returns:
            List of (root, coefficient) pairs.
        """
        result: list[tuple[int, float]] = []
        for r in roots:
            pr, _ = rc.eval_p(float(r), 0.0)
            qpr, _ = rc.eval_q_prime(float(r), 0.0)
            if abs(qpr) > 1e-12:
                result.append((r, pr / qpr))
            else:
                result.append((r, 0.0))
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Laurent series decomposition steps.

        Args:
            data: Solution data with partial fraction coefficients.

        Returns:
            Steps showing PF decomposition and principal part.
        """
        z0 = data["z0"]
        pf = data["pf_coeffs"]
        pf_parts = " + ".join(
            f"{_fmt(c)}/(z-{r})" for r, c in pf
        )
        steps = [f"PF: {pf_parts}"]
        for r, c in pf:
            steps.append(f"A(z={r})={_fmt(c)}")
        principal_coeff = next(c for r, c in pf if r == z0)
        steps.append(f"principal: {_fmt(principal_coeff)}/(z-{z0})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Laurent series principal part coefficient.

        Args:
            data: Solution data.

        Returns:
            String showing the principal part.
        """
        z0 = data["z0"]
        coeff = next(c for r, c in data["pf_coeffs"] if r == z0)
        return f"a_{{-1}}={_fmt(coeff)}"


@register
class PolesClassifyGenerator(StepGenerator):
    """Classify a singularity as removable, pole (with order), or essential.

    Examines the Laurent expansion of P(z)/Q(z) near a singularity z_0
    to determine the nature of the singularity. For this generator,
    singularities are either removable (numerator also vanishes),
    simple poles, or higher-order poles (repeated root in denominator).

    Input format:
        ``classify singularity``

    Target format:
        ``f(z)=(z-1)/(z-1)^2 at z_0=1 <step> factor: 1/(z-1)
        <step> order of zero in P: 1, in Q: 2 <step>
        pole of order 2-1=1 <step> simple pole``

    Difficulty scaling:
        Difficulty 1-3: simple pole or removable.
        Difficulty 4-6: pole of order 1-2.
        Difficulty 7-8: pole of order 1-3 or removable.

    Prerequisites:
        laurent_series.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "poles_classify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["laurent_series"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls singularity type complexity.

        Returns:
            Natural language description.
        """
        return "classify singularity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rational function with a known singularity type.

        Constructs P(z) and Q(z) with controlled vanishing orders at z_0
        to produce a specific singularity classification.

        Args:
            difficulty: Controls pole order and function complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        z0, p_order, q_order, extra_roots = self._build(difficulty)
        pole_order = q_order - p_order

        p_latex, q_latex = self._build_latex(z0, p_order, q_order,
                                             extra_roots)

        if pole_order <= 0:
            classification = "removable"
        elif pole_order == 1:
            classification = "simple pole"
        else:
            classification = f"pole of order {pole_order}"

        problem = f"\\text{{classify }} f(z)=\\frac{{{p_latex}}}{{{q_latex}}} \\text{{ at }} z_0={z0}"
        return problem, {
            "z0": z0, "p_order": p_order, "q_order": q_order,
            "pole_order": pole_order, "classification": classification,
            "extra_roots": extra_roots,
        }

    def _build(self, difficulty: int) -> tuple[int, int, int, list[int]]:
        """Choose z_0, vanishing orders, and extra roots.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (z0, p_order, q_order, extra_roots).
        """
        z0 = self._rng.randint(1, 3)

        if difficulty <= 3:
            is_removable = self._rng.choice([True, False])
            if is_removable:
                order = self._rng.randint(1, 2)
                p_order, q_order = order, order
            else:
                p_order, q_order = 0, 1
        elif difficulty <= 6:
            q_order = self._rng.randint(1, 2)
            p_order = self._rng.randint(0, max(0, q_order - 1))
        else:
            q_order = self._rng.randint(1, 3)
            p_order = self._rng.randint(0, max(0, q_order - 1))

        n_extra = self._rng.randint(0, min(2, difficulty // 3))
        extra_roots: list[int] = []
        for _ in range(n_extra):
            r = self._rng.randint(-3, 3)
            if r != z0 and r != 0 and r not in extra_roots:
                extra_roots.append(r)

        return z0, p_order, q_order, extra_roots

    def _build_latex(self, z0: int, p_order: int, q_order: int,
                     extra_roots: list[int]) -> tuple[str, str]:
        """Build LaTeX strings for numerator and denominator.

        Args:
            z0: Singularity location.
            p_order: Vanishing order of P at z0.
            q_order: Vanishing order of Q at z0.
            extra_roots: Additional roots in the denominator.

        Returns:
            Tuple of (numerator_latex, denominator_latex).
        """
        p_str = self._factor_power_latex(z0, p_order) if p_order > 0 else "1"
        q_parts = [self._factor_power_latex(z0, q_order)]
        for r in extra_roots:
            q_parts.append(self._factor_power_latex(r, 1))
        q_str = "".join(q_parts)
        return p_str, q_str

    def _factor_power_latex(self, root: int, power: int) -> str:
        """Format (z - root)^power as LaTeX.

        Args:
            root: Root value.
            power: Power of the factor.

        Returns:
            LaTeX string for the factor.
        """
        if root == 0:
            base = "z"
        elif root > 0:
            base = f"(z-{root})"
        else:
            base = f"(z+{-root})"
        if power == 1:
            return base
        return f"{base}^{{{power}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data with vanishing orders.

        Returns:
            Steps showing order analysis and classification.
        """
        z0 = data["z0"]
        return [
            f"zero of P at z_0={z0}: order {data['p_order']}",
            f"zero of Q at z_0={z0}: order {data['q_order']}",
            f"pole order = {data['q_order']}-{data['p_order']}={data['pole_order']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the singularity classification.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        return data["classification"]
