"""Advanced calculus, graduate mathematics, and signal processing generators.

Provides tier 5-6 generators for quotient rule differentiation, limits with
L'Hopital's rule, separable differential equations, divergence of vector
fields, Lagrange multipliers, quadratic residues, continued fractions,
Diophantine equations, linear recurrence evaluation, and polynomial
synthetic division. Each generator produces step-by-step solutions with
LaTeX formatting suitable for training sequence models.
"""
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class RationalFunction:
    """Represents a quotient f(x)/g(x) of two single-term polynomials.

    Stores numerator and denominator as (coefficient, exponent) pairs
    and computes derivatives via the power rule for use in quotient
    rule differentiation problems.

    Example:
        >>> rf = RationalFunction(3, 2, 2, 1)
        >>> rf.f_latex()
        '3x^{2}'
        >>> rf.g_latex()
        '2x'
    """

    def __init__(self, f_coeff: int, f_exp: int,
                 g_coeff: int, g_exp: int) -> None:
        """Initialise with numerator and denominator terms.

        Args:
            f_coeff: Numerator coefficient.
            f_exp: Numerator exponent.
            g_coeff: Denominator coefficient.
            g_exp: Denominator exponent.
        """
        self._f_coeff = f_coeff
        self._f_exp = f_exp
        self._g_coeff = g_coeff
        self._g_exp = g_exp

    def f_latex(self) -> str:
        """Format the numerator f(x) in LaTeX.

        Returns:
            LaTeX string for f(x).
        """
        return self._term_latex(self._f_coeff, self._f_exp)

    def g_latex(self) -> str:
        """Format the denominator g(x) in LaTeX.

        Returns:
            LaTeX string for g(x).
        """
        return self._term_latex(self._g_coeff, self._g_exp)

    def f_deriv_latex(self) -> str:
        """Format the derivative f'(x) in LaTeX.

        Returns:
            LaTeX string for f'(x).
        """
        coeff = self._f_coeff * self._f_exp
        exp = self._f_exp - 1
        return self._term_latex(coeff, exp)

    def g_deriv_latex(self) -> str:
        """Format the derivative g'(x) in LaTeX.

        Returns:
            LaTeX string for g'(x).
        """
        coeff = self._g_coeff * self._g_exp
        exp = self._g_exp - 1
        return self._term_latex(coeff, exp)

    def g_squared_latex(self) -> str:
        """Format g(x)^2 in LaTeX.

        Returns:
            LaTeX string for the squared denominator.
        """
        return f"({self.g_latex()})^{{2}}"

    def _term_latex(self, coeff: int, exp: int) -> str:
        """Format a single polynomial term as LaTeX.

        Args:
            coeff: Term coefficient.
            exp: Term exponent.

        Returns:
            LaTeX string for the term.
        """
        if exp == 0:
            return str(coeff)
        if exp == 1:
            return f"{coeff}x" if coeff != 1 else "x"
        if coeff == 1:
            return f"x^{{{exp}}}"
        return f"{coeff}x^{{{exp}}}"


class FactorablePolynomial:
    """Represents a polynomial that factors as (x - a)(x - b) for limit problems.

    Stores roots a and b and provides the expanded form, factored form,
    and evaluation methods needed for computing limits involving 0/0
    indeterminate forms resolved by factoring.

    Example:
        >>> fp = FactorablePolynomial(2, 3)
        >>> fp.expanded_coeffs()
        (1, -5, 6)
        >>> fp.eval_at(2)
        0
    """

    def __init__(self, root_a: int, root_b: int) -> None:
        """Initialise with two integer roots.

        Args:
            root_a: First root of the polynomial.
            root_b: Second root of the polynomial.
        """
        self._root_a = root_a
        self._root_b = root_b

    @property
    def root_a(self) -> int:
        """Return the first root."""
        return self._root_a

    @property
    def root_b(self) -> int:
        """Return the second root."""
        return self._root_b

    def expanded_coeffs(self) -> tuple[int, int, int]:
        """Return coefficients (a, b, c) of ax^2 + bx + c.

        Returns:
            Tuple of (leading, middle, constant) coefficients.
        """
        return (
            1,
            -(self._root_a + self._root_b),
            self._root_a * self._root_b,
        )

    def expanded_latex(self) -> str:
        """Format the expanded polynomial in LaTeX.

        Returns:
            LaTeX string like 'x^{2}-5x+6'.
        """
        _, b, c = self.expanded_coeffs()
        parts = ["x^{2}"]
        parts.append(self._signed_term(b, 1))
        parts.append(self._signed_const(c))
        return "".join(parts)

    def factored_latex(self) -> str:
        """Format the factored polynomial in LaTeX.

        Returns:
            LaTeX string like '(x-2)(x-3)'.
        """
        left = self._factor_str(self._root_a)
        right = self._factor_str(self._root_b)
        return f"({left})({right})"

    def eval_at(self, x: int) -> int:
        """Evaluate the polynomial at a given point.

        Args:
            x: Evaluation point.

        Returns:
            Polynomial value at x.
        """
        return (x - self._root_a) * (x - self._root_b)

    def _factor_str(self, root: int) -> str:
        """Format a single linear factor (x - root).

        Args:
            root: Root value.

        Returns:
            String like 'x-2' or 'x+3'.
        """
        if root == 0:
            return "x"
        if root > 0:
            return f"x-{root}"
        return f"x+{-root}"

    def _signed_term(self, coeff: int, exp: int) -> str:
        """Format a signed polynomial term.

        Args:
            coeff: Term coefficient.
            exp: Term exponent.

        Returns:
            Signed term string like '-5x' or '+3x'.
        """
        if coeff == 0:
            return ""
        var = "x" if exp == 1 else f"x^{{{exp}}}"
        if coeff == 1:
            return f"+{var}"
        if coeff == -1:
            return f"-{var}"
        if coeff > 0:
            return f"+{coeff}{var}"
        return f"{coeff}{var}"

    def _signed_const(self, val: int) -> str:
        """Format a signed constant term.

        Args:
            val: Constant value.

        Returns:
            Signed constant string like '+6' or '-2'.
        """
        if val == 0:
            return ""
        if val > 0:
            return f"+{val}"
        return str(val)


class VectorField2D:
    """Represents a 2D vector field F = (f1, f2) for divergence computation.

    Each component is a monomial of the form c * x^a * y^b. Provides
    partial derivative computation and LaTeX formatting.

    Example:
        >>> vf = VectorField2D(3, 2, 1, 2, 1, 2)
        >>> vf.f1_latex()
        '3x^{2}y'
    """

    def __init__(self, c1: int, a1: int, b1: int,
                 c2: int, a2: int, b2: int) -> None:
        """Initialise with two monomial components.

        Args:
            c1: Coefficient of first component.
            a1: x-exponent of first component.
            b1: y-exponent of first component.
            c2: Coefficient of second component.
            a2: x-exponent of second component.
            b2: y-exponent of second component.
        """
        self._c1 = c1
        self._a1 = a1
        self._b1 = b1
        self._c2 = c2
        self._a2 = a2
        self._b2 = b2

    def f1_latex(self) -> str:
        """Format the first component f1(x,y) in LaTeX.

        Returns:
            LaTeX string for f1.
        """
        return self._monomial_latex(self._c1, self._a1, self._b1)

    def f2_latex(self) -> str:
        """Format the second component f2(x,y) in LaTeX.

        Returns:
            LaTeX string for f2.
        """
        return self._monomial_latex(self._c2, self._a2, self._b2)

    def df1_dx_latex(self) -> str:
        """Format the partial derivative df1/dx in LaTeX.

        Returns:
            LaTeX string for df1/dx.
        """
        coeff = self._c1 * self._a1
        exp_x = self._a1 - 1
        return self._monomial_latex(coeff, exp_x, self._b1)

    def df2_dy_latex(self) -> str:
        """Format the partial derivative df2/dy in LaTeX.

        Returns:
            LaTeX string for df2/dy.
        """
        coeff = self._c2 * self._b2
        exp_y = self._b2 - 1
        return self._monomial_latex(coeff, self._a2, exp_y)

    def _monomial_latex(self, coeff: int, x_exp: int,
                        y_exp: int) -> str:
        """Format a monomial c * x^a * y^b in LaTeX.

        Args:
            coeff: Monomial coefficient.
            x_exp: Exponent of x.
            y_exp: Exponent of y.

        Returns:
            LaTeX string for the monomial.
        """
        if coeff == 0:
            return "0"
        parts = str(coeff) if coeff != 1 else ""
        parts += self._var_part("x", x_exp)
        parts += self._var_part("y", y_exp)
        return parts if parts else str(coeff)

    def _var_part(self, var: str, exp: int) -> str:
        """Format a variable with exponent.

        Args:
            var: Variable name.
            exp: Exponent value.

        Returns:
            LaTeX string for the variable part.
        """
        if exp <= 0:
            return ""
        if exp == 1:
            return var
        return f"{var}^{{{exp}}}"


class ContinuedFractionComputer:
    """Computes the continued fraction representation of a rational number.

    Applies the Euclidean algorithm to extract integer parts iteratively,
    producing the sequence [a0; a1, a2, ...] where each a_i is the integer
    part at each step.

    Example:
        >>> cfc = ContinuedFractionComputer(17, 5)
        >>> cfc.compute()
        [3, 2, 2]
    """

    def __init__(self, numerator: int, denominator: int) -> None:
        """Initialise with a rational number p/q.

        Args:
            numerator: The numerator p.
            denominator: The denominator q.
        """
        self._numerator = numerator
        self._denominator = denominator

    @property
    def numerator(self) -> int:
        """Return the original numerator."""
        return self._numerator

    @property
    def denominator(self) -> int:
        """Return the original denominator."""
        return self._denominator

    def compute(self) -> list[int]:
        """Compute the continued fraction coefficients.

        Returns:
            List of continued fraction coefficients [a0, a1, ...].
        """
        coeffs: list[int] = []
        num = self._numerator
        den = self._denominator
        while den != 0:
            q = num // den
            coeffs.append(q)
            num, den = den, num - q * den
        return coeffs

    def steps(self) -> list[tuple[int, int, int]]:
        """Compute continued fraction with step details.

        Returns:
            List of (quotient, numerator, denominator) at each step.
        """
        result: list[tuple[int, int, int]] = []
        num = self._numerator
        den = self._denominator
        while den != 0:
            q = num // den
            result.append((q, num, den))
            num, den = den, num - q * den
        return result


class ExtendedEuclidean:
    """Solves ax + by = gcd(a, b) using the extended Euclidean algorithm.

    Records each step of the algorithm for step-by-step display,
    then performs back-substitution to find the Bezout coefficients
    x and y.

    Example:
        >>> ee = ExtendedEuclidean(35, 15)
        >>> ee.gcd()
        5
        >>> x, y = ee.solve()
        >>> 35 * x + 15 * y == 5
        True
    """

    def __init__(self, a: int, b: int) -> None:
        """Initialise with two positive integers.

        Args:
            a: First integer.
            b: Second integer.
        """
        self._a = a
        self._b = b
        self._steps: list[tuple[int, int, int, int]] = []
        self._compute()

    def _compute(self) -> None:
        """Run the Euclidean algorithm and record each division step."""
        a, b = self._a, self._b
        while b != 0:
            q = a // b
            r = a - q * b
            self._steps.append((a, b, q, r))
            a, b = b, r

    def gcd(self) -> int:
        """Return the greatest common divisor.

        Returns:
            The GCD of a and b.
        """
        if not self._steps:
            return self._a
        return self._steps[-1][1]

    def division_steps(self) -> list[tuple[int, int, int, int]]:
        """Return the recorded division steps.

        Returns:
            List of (dividend, divisor, quotient, remainder) tuples.
        """
        return self._steps

    def solve(self) -> tuple[int, int]:
        """Find Bezout coefficients x, y such that ax + by = gcd(a, b).

        Returns:
            Tuple (x, y) satisfying the Bezout identity.
        """
        if not self._steps:
            return (1, 0)
        x, y = 0, 1
        for i in range(len(self._steps) - 2, -1, -1):
            q = self._steps[i][2]
            x, y = y, x - q * y
        return (x, y)


class SyntheticDivider:
    """Performs synthetic division of a polynomial by (x - a).

    Records the tableau row for step-by-step display. The polynomial
    is represented as a list of coefficients from highest to lowest degree.

    Example:
        >>> sd = SyntheticDivider([1, -6, 11, -6], 1)
        >>> sd.quotient_coeffs()
        [1, -5, 6]
        >>> sd.remainder()
        0
    """

    def __init__(self, coeffs: list[int], root: int) -> None:
        """Initialise with polynomial coefficients and divisor root.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            root: The value a in the divisor (x - a).
        """
        self._coeffs = coeffs
        self._root = root
        self._bottom: list[int] = []
        self._run()

    def _run(self) -> None:
        """Execute synthetic division and populate the bottom row."""
        self._bottom = [self._coeffs[0]]
        for i in range(1, len(self._coeffs)):
            val = self._bottom[-1] * self._root + self._coeffs[i]
            self._bottom.append(val)

    @property
    def root(self) -> int:
        """Return the divisor root."""
        return self._root

    def coefficients(self) -> list[int]:
        """Return the original polynomial coefficients.

        Returns:
            List of coefficients from highest to lowest degree.
        """
        return self._coeffs

    def bottom_row(self) -> list[int]:
        """Return the synthetic division bottom row.

        Returns:
            List of values in the bottom row of the tableau.
        """
        return self._bottom

    def quotient_coeffs(self) -> list[int]:
        """Return the quotient polynomial coefficients.

        Returns:
            Coefficients of the quotient from highest to lowest degree.
        """
        return self._bottom[:-1]

    def remainder(self) -> int:
        """Return the division remainder.

        Returns:
            Integer remainder.
        """
        return self._bottom[-1]

    def step_details(self) -> list[tuple[int, int, int]]:
        """Return per-column details for each synthetic division step.

        Returns:
            List of (multiply_value, add_value, result) for each column
            after the first.
        """
        details: list[tuple[int, int, int]] = []
        for i in range(1, len(self._coeffs)):
            mul = self._bottom[i - 1] * self._root
            add = self._coeffs[i]
            result = mul + add
            details.append((mul, add, result))
        return details


@register
class QuotientRuleGenerator(StepGenerator):
    """Quotient rule differentiation d/dx(f/g) = (f'g - fg')/g^2.

    Generates two single-term polynomials f(x) = ax^n and g(x) = bx^m,
    then applies the quotient rule showing f'(x), g'(x), the numerator
    f'g - fg', and the denominator g^2.

    Input format:
        ``differentiate quotient of functions``

    Target format:
        ``\\frac{d}{dx}\\frac{3x^{2}}{2x} <step> f'(x)=6x <step>
        g'(x)=2 <step> f'g-fg'=(6x)(2x)-(3x^{2})(2) <step>
        \\frac{(6x)(2x)-(3x^{2})(2)}{(2x)^{2}}``

    Difficulty scaling:
        Difficulty 1-3: small coefficients (1-3), exponents 1-2.
        Difficulty 4-6: moderate coefficients (2-5), exponents 2-3.
        Difficulty 7-8: larger coefficients (3-8), exponents 3-4.

    Prerequisites:
        derivative, multiplication.

    Example:
        >>> gen = QuotientRuleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'quotient_rule'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "quotient_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient and exponent range.

        Returns:
            Natural language description.
        """
        return "differentiate quotient of functions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quotient of two monomials and set up the quotient rule.

        Args:
            difficulty: Controls coefficient and exponent magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rf = self._build_rational(difficulty)
        problem = (
            f"\\frac{{d}}{{dx}}"
            f"\\frac{{{rf.f_latex()}}}{{{rf.g_latex()}}}"
        )
        return problem, {"rf": rf}

    def _build_rational(self, difficulty: int) -> RationalFunction:
        """Build a rational function scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A RationalFunction instance.
        """
        coeff_hi, exp_hi = self._param_bounds(difficulty)
        f_coeff = self._rng.randint(1, coeff_hi)
        f_exp = self._rng.randint(1, exp_hi)
        g_coeff = self._rng.randint(1, coeff_hi)
        g_exp = self._rng.randint(1, max(1, exp_hi - 1))
        return RationalFunction(f_coeff, f_exp, g_coeff, g_exp)

    def _param_bounds(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to coefficient and exponent upper bounds.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (max_coefficient, max_exponent).
        """
        if difficulty <= 3:
            return 3, 2
        if difficulty <= 6:
            return 5, 3
        return 8, 4

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quotient rule application steps.

        Args:
            data: Solution data with the rational function.

        Returns:
            Steps showing f', g', and the quotient rule formula.
        """
        rf = data["rf"]
        return [
            f"f'(x)={rf.f_deriv_latex()}",
            f"g'(x)={rf.g_deriv_latex()}",
            (
                f"f'g-fg'="
                f"({rf.f_deriv_latex()})({rf.g_latex()})"
                f"-({rf.f_latex()})({rf.g_deriv_latex()})"
            ),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the quotient rule result in LaTeX.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for (f'g - fg') / g^2.
        """
        rf = data["rf"]
        numerator = (
            f"({rf.f_deriv_latex()})({rf.g_latex()})"
            f"-({rf.f_latex()})({rf.g_deriv_latex()})"
        )
        return f"\\frac{{{numerator}}}{{{rf.g_squared_latex()}}}"


@register
class LimitGenerator(StepGenerator):
    """Limits involving 0/0 indeterminate forms resolved by factoring.

    Generates a ratio p(x)/q(x) where both polynomials share a common
    root, creating a 0/0 form. The limit is computed by factoring out
    the common (x - a) term and evaluating the simplified expression.

    Input format:
        ``compute limit of rational function``

    Target format:
        ``\\lim_{x \\to 2} \\frac{x^{2}-5x+6}{x^{2}-4} <step>
        0/0 indeterminate <step> factor: \\frac{(x-2)(x-3)}{(x-2)(x+2)}
        <step> cancel (x-2): \\frac{x-3}{x+2} <step> \\frac{-1}{4}``

    Difficulty scaling:
        Difficulty 1-3: common root in [1, 3], other roots in [-3, 3].
        Difficulty 4-6: common root in [1, 5], other roots in [-5, 5].
        Difficulty 7-8: common root in [2, 7], other roots in [-7, 7].

    Prerequisites:
        derivative, division.

    Example:
        >>> gen = LimitGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'limit'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "limit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls root magnitude.

        Returns:
            Natural language description.
        """
        return "compute limit of rational function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 0/0 limit problem with factorable numerator and denominator.

        Args:
            difficulty: Controls root range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        common, r_num, r_den = self._choose_roots(difficulty)
        numer = FactorablePolynomial(common, r_num)
        denom = FactorablePolynomial(common, r_den)
        limit_val = Fraction(common - r_num, common - r_den)

        problem = (
            f"\\lim_{{x \\to {common}}} "
            f"\\frac{{{numer.expanded_latex()}}}"
            f"{{{denom.expanded_latex()}}}"
        )
        return problem, {
            "common": common, "r_num": r_num, "r_den": r_den,
            "numer": numer, "denom": denom, "limit_val": limit_val,
        }

    def _choose_roots(self, difficulty: int) -> tuple[int, int, int]:
        """Choose common root and distinct other roots for num/den.

        Args:
            difficulty: Controls root magnitude.

        Returns:
            Tuple of (common_root, numerator_other_root, denominator_other_root).
        """
        c_hi, r_hi = self._root_bounds(difficulty)
        common = self._rng.randint(1, c_hi)
        r_num = self._distinct_root(common, r_hi)
        r_den = self._distinct_root_pair(common, r_num, r_hi)
        return common, r_num, r_den

    def _root_bounds(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to root magnitude bounds.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (common_root_max, other_root_max).
        """
        if difficulty <= 3:
            return 3, 3
        if difficulty <= 6:
            return 5, 5
        return 7, 7

    def _distinct_root(self, exclude: int, bound: int) -> int:
        """Pick a root distinct from the excluded value.

        Args:
            exclude: Value to avoid.
            bound: Absolute value bound.

        Returns:
            Integer root distinct from exclude.
        """
        for _ in range(50):
            r = self._rng.randint(-bound, bound)
            if r != exclude:
                return r
        return exclude + 1

    def _distinct_root_pair(self, exclude1: int, exclude2: int,
                            bound: int) -> int:
        """Pick a root distinct from two excluded values.

        Args:
            exclude1: First value to avoid.
            exclude2: Second value to avoid.
            bound: Absolute value bound.

        Returns:
            Integer root distinct from both excluded values.
        """
        for _ in range(50):
            r = self._rng.randint(-bound, bound)
            if r != exclude1 and r != exclude2:
                return r
        return exclude1 + 2

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            val: Fraction value.

        Returns:
            LaTeX string for the fraction.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate factoring and cancellation steps.

        Args:
            data: Solution data with polynomials and limit value.

        Returns:
            Steps showing 0/0 detection, factoring, cancellation, and evaluation.
        """
        numer = data["numer"]
        denom = data["denom"]
        common = data["common"]
        r_num = data["r_num"]
        r_den = data["r_den"]
        limit_val = data["limit_val"]

        cancel_factor = self._factor_str(common)
        remaining_num = self._factor_str(r_num)
        remaining_den = self._factor_str(r_den)

        return [
            "0/0 indeterminate",
            (
                f"factor: \\frac{{{numer.factored_latex()}}}"
                f"{{{denom.factored_latex()}}}"
            ),
            (
                f"cancel ({cancel_factor}): "
                f"\\frac{{{remaining_num}}}{{{remaining_den}}}"
            ),
            f"x={common}: {self._format_fraction(limit_val)}",
        ]

    def _factor_str(self, root: int) -> str:
        """Format a linear factor (x - root).

        Args:
            root: Root value.

        Returns:
            String for the factor.
        """
        if root == 0:
            return "x"
        if root > 0:
            return f"x-{root}"
        return f"x+{-root}"

    def _create_answer(self, data: dict) -> str:
        """Return the limit value.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the limit.
        """
        return self._format_fraction(data["limit_val"])


@register
class DiffEquationGenerator(StepGenerator):
    """Solve separable ODE dy/dx = ky with exponential solutions.

    Generates a simple first-order separable ODE dy/dx = ky with
    initial condition y(0) = C. Shows separation of variables,
    integration, and the exponential solution y = C * e^{kx}.

    Input format:
        ``solve separable differential equation``

    Target format:
        ``\\frac{dy}{dx} = 3y, y(0)=2 <step> \\frac{dy}{y} = 3 dx
        <step> \\int \\frac{dy}{y} = \\int 3 dx <step>
        \\ln|y| = 3x + C_0 <step> y(0)=2: C_0=\\ln(2) <step>
        y = 2e^{3x}``

    Difficulty scaling:
        Difficulty 1-3: k in [1, 3], initial value in [1, 3].
        Difficulty 4-6: k in [-5, 5] (nonzero), initial value in [1, 5].
        Difficulty 7-8: k in [-8, 8] (nonzero), initial value in [1, 8].

    Prerequisites:
        integral, division.

    Example:
        >>> gen = DiffEquationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'diff_equation'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "diff_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["integral", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "solve separable differential equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a separable ODE dy/dx = ky with initial condition.

        Args:
            difficulty: Controls k and initial value ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k, y0 = self._choose_params(difficulty)
        problem = (
            f"\\frac{{dy}}{{dx}} = {k}y, y(0)={y0}"
        )
        return problem, {"k": k, "y0": y0}

    def _choose_params(self, difficulty: int) -> tuple[int, int]:
        """Choose ODE parameters based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (k, y0).
        """
        k_range, y0_range = self._param_ranges(difficulty)
        k = self._nonzero_randint(k_range[0], k_range[1])
        y0 = self._rng.randint(y0_range[0], y0_range[1])
        return k, y0

    def _param_ranges(self, difficulty: int) -> tuple[tuple[int, int], tuple[int, int]]:
        """Map difficulty to parameter ranges.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (k_range, y0_range).
        """
        if difficulty <= 3:
            return (1, 3), (1, 3)
        if difficulty <= 6:
            return (-5, 5), (1, 5)
        return (-8, 8), (1, 8)

    def _nonzero_randint(self, lo: int, hi: int) -> int:
        """Generate a random nonzero integer in [lo, hi].

        Args:
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Nonzero random integer.
        """
        for _ in range(50):
            val = self._rng.randint(lo, hi)
            if val != 0:
                return val
        return 1

    def _create_steps(self, data: dict) -> list[str]:
        """Generate separation, integration, and solution steps.

        Args:
            data: Solution data with k and y0.

        Returns:
            Steps showing the full ODE solution process.
        """
        k = data["k"]
        y0 = data["y0"]
        return [
            f"\\frac{{dy}}{{y}} = {k} \\, dx",
            f"\\int \\frac{{dy}}{{y}} = \\int {k} \\, dx",
            f"\\ln|y| = {k}x + C_0",
            f"y(0)={y0}: C_0=\\ln({y0})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the general solution.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for y = y0 * e^{kx}.
        """
        k = data["k"]
        y0 = data["y0"]
        return f"y = {y0}e^{{{k}x}}"


@register
class DivergenceGenerator(StepGenerator):
    """Divergence of a 2D vector field: div F = df1/dx + df2/dy.

    Generates a 2D vector field F = (f1(x,y), f2(x,y)) where each
    component is a monomial, computes the partial derivatives df1/dx
    and df2/dy, and sums them to produce the divergence.

    Input format:
        ``compute divergence of vector field``

    Target format:
        ``\\nabla \\cdot F, F=(3x^{2}y, 2xy^{2}) <step>
        \\frac{\\partial f_1}{\\partial x}=6xy <step>
        \\frac{\\partial f_2}{\\partial y}=4xy <step>
        \\nabla \\cdot F = 6xy+4xy``

    Difficulty scaling:
        Difficulty 1-3: coefficients 1-3, exponents 1-2.
        Difficulty 4-6: coefficients 2-5, exponents 1-3.
        Difficulty 7-8: coefficients 3-7, exponents 2-4.

    Prerequisites:
        partial_derivative, addition.

    Example:
        >>> gen = DivergenceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'divergence'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "divergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient and exponent range.

        Returns:
            Natural language description.
        """
        return "compute divergence of vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2D vector field and compute its divergence.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        vf = self._build_field(difficulty)
        problem = (
            f"\\nabla \\cdot F, "
            f"F=({vf.f1_latex()}, {vf.f2_latex()})"
        )
        return problem, {"vf": vf}

    def _build_field(self, difficulty: int) -> VectorField2D:
        """Build a vector field scaled by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A VectorField2D instance.
        """
        c_hi, e_lo, e_hi = self._field_bounds(difficulty)
        c1 = self._rng.randint(1, c_hi)
        a1 = self._rng.randint(e_lo, e_hi)
        b1 = self._rng.randint(e_lo, e_hi)
        c2 = self._rng.randint(1, c_hi)
        a2 = self._rng.randint(e_lo, e_hi)
        b2 = self._rng.randint(e_lo, e_hi)
        return VectorField2D(c1, a1, b1, c2, a2, b2)

    def _field_bounds(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to vector field parameter bounds.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (max_coeff, min_exp, max_exp).
        """
        if difficulty <= 3:
            return 3, 1, 2
        if difficulty <= 6:
            return 5, 1, 3
        return 7, 2, 4

    def _create_steps(self, data: dict) -> list[str]:
        """Generate partial derivative and summation steps.

        Args:
            data: Solution data with the vector field.

        Returns:
            Steps showing df1/dx, df2/dy, and their sum.
        """
        vf = data["vf"]
        return [
            f"\\frac{{\\partial f_1}}{{\\partial x}}={vf.df1_dx_latex()}",
            f"\\frac{{\\partial f_2}}{{\\partial y}}={vf.df2_dy_latex()}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the divergence expression.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for div F = df1/dx + df2/dy.
        """
        vf = data["vf"]
        return (
            f"\\nabla \\cdot F = "
            f"{vf.df1_dx_latex()}+{vf.df2_dy_latex()}"
        )


@register
class LagrangeMultiplierGenerator(StepGenerator):
    """Minimise f(x,y) = x^2 + y^2 subject to ax + by = c using Lagrange multipliers.

    Generates a quadratic objective with a linear constraint that has
    integer or simple rational solutions. Shows the gradient equations,
    the constraint, solving for lambda, and the optimal point.

    Input format:
        ``optimise with lagrange multiplier``

    Target format:
        ``\\min x^{2}+y^{2} \\text{ s.t. } 2x+3y=12 <step>
        \\nabla f = \\lambda \\nabla g <step> 2x=2\\lambda, 2y=3\\lambda
        <step> x=\\lambda, y=\\frac{3}{2}\\lambda <step>
        2\\lambda+\\frac{9}{2}\\lambda=12 <step> \\lambda=\\frac{24}{13}
        <step> x=\\frac{24}{13}, y=\\frac{36}{13}``

    Difficulty scaling:
        Difficulty 1-3: a, b in [1, 3], c chosen for integer lambda.
        Difficulty 4-6: a, b in [1, 5], c chosen for clean solutions.
        Difficulty 7-8: a, b in [2, 7], c chosen for clean solutions.

    Prerequisites:
        gradient, system_equations.

    Example:
        >>> gen = LagrangeMultiplierGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lagrange_multiplier'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lagrange_multiplier"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gradient", "system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Natural language description.
        """
        return "optimise with lagrange multiplier"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrange multiplier optimisation problem.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a, b, c = self._choose_coefficients(difficulty)
        lam = Fraction(2 * c, a * a + b * b)
        x_opt = Fraction(a, 2) * lam
        y_opt = Fraction(b, 2) * lam

        problem = (
            f"\\min x^{{2}}+y^{{2}} "
            f"\\text{{ s.t. }} {a}x+{b}y={c}"
        )
        return problem, {
            "a": a, "b": b, "c": c,
            "lam": lam, "x_opt": x_opt, "y_opt": y_opt,
        }

    def _choose_coefficients(self, difficulty: int) -> tuple[int, int, int]:
        """Choose constraint coefficients that yield clean solutions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (a, b, c) for the constraint ax + by = c.
        """
        hi = self._coeff_bound(difficulty)
        a = self._rng.randint(1, hi)
        b = self._rng.randint(1, hi)
        denom = a * a + b * b
        k = self._rng.randint(1, max(2, difficulty))
        c = k * denom
        return a, b, c

    def _coeff_bound(self, difficulty: int) -> int:
        """Map difficulty to coefficient upper bound.

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

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            val: Fraction value.

        Returns:
            LaTeX string for the fraction.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lagrange multiplier solution steps.

        Args:
            data: Solution data with coefficients and optimal values.

        Returns:
            Steps showing gradient equations, lambda, and optimal point.
        """
        a = data["a"]
        b = data["b"]
        c = data["c"]
        lam = data["lam"]
        x_opt = data["x_opt"]
        y_opt = data["y_opt"]

        return [
            "\\nabla f = \\lambda \\nabla g",
            f"2x={a}\\lambda, 2y={b}\\lambda",
            (
                f"x=\\frac{{{a}}}{{{2}}}\\lambda, "
                f"y=\\frac{{{b}}}{{{2}}}\\lambda"
            ),
            f"substitute: \\lambda={self._format_fraction(lam)}",
            (
                f"x={self._format_fraction(x_opt)}, "
                f"y={self._format_fraction(y_opt)}"
            ),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the optimal point.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the optimal (x, y).
        """
        x_str = self._format_fraction(data["x_opt"])
        y_str = self._format_fraction(data["y_opt"])
        return f"({x_str}, {y_str})"


@register
class QuadraticResidueGenerator(StepGenerator):
    """Determine if a is a quadratic residue mod p using Euler's criterion.

    Computes a^{(p-1)/2} mod p. If the result is 1, then a is a quadratic
    residue; otherwise it is not. Uses small primes p and values a < p.

    Input format:
        ``check quadratic residue``

    Target format:
        ``\\text{QR}(3, 7) <step> \\text{Euler: } a^{(p-1)/2} \\mod p
        <step> 3^{3} \\mod 7 <step> 27 \\mod 7 = 6 <step>
        6 \\neq 1: \\text{not a QR}``

    Difficulty scaling:
        Difficulty 1-3: primes from [5, 13].
        Difficulty 4-6: primes from [7, 23].
        Difficulty 7-8: primes from [11, 31].

    Prerequisites:
        mod_pow.

    Example:
        >>> gen = QuadraticResidueGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'quadratic_residue'
    """

    _PRIMES_BY_DIFFICULTY = {
        "low": [5, 7, 11, 13],
        "mid": [7, 11, 13, 17, 19, 23],
        "high": [11, 13, 17, 19, 23, 29, 31],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "quadratic_residue"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls prime size.

        Returns:
            Natural language description.
        """
        return "check quadratic residue"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic residue test problem.

        Args:
            difficulty: Controls prime selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._choose_prime(difficulty)
        a = self._rng.randint(2, p - 1)
        exp = (p - 1) // 2
        power_val = pow(a, exp, p)
        is_qr = (power_val == 1)

        problem = f"\\text{{QR}}({a}, {p})"
        return problem, {
            "a": a, "p": p, "exp": exp,
            "power_val": power_val, "is_qr": is_qr,
        }

    def _choose_prime(self, difficulty: int) -> int:
        """Select a prime based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            An odd prime.
        """
        pool = self._prime_pool(difficulty)
        return self._rng.choice(pool)

    def _prime_pool(self, difficulty: int) -> list[int]:
        """Map difficulty to available primes.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of primes.
        """
        if difficulty <= 3:
            return self._PRIMES_BY_DIFFICULTY["low"]
        if difficulty <= 6:
            return self._PRIMES_BY_DIFFICULTY["mid"]
        return self._PRIMES_BY_DIFFICULTY["high"]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler's criterion computation steps.

        Args:
            data: Solution data with a, p, exponent, and result.

        Returns:
            Steps showing the criterion, exponentiation, and conclusion.
        """
        a = data["a"]
        p = data["p"]
        exp = data["exp"]
        power_val = data["power_val"]

        return [
            f"\\text{{Euler: }} a^{{(p-1)/2}} \\mod p",
            f"{a}^{{{exp}}} \\mod {p}",
            f"result = {power_val}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether a is a quadratic residue.

        Args:
            data: Solution data.

        Returns:
            'yes' if QR, 'no' otherwise.
        """
        return "yes" if data["is_qr"] else "no"


@register
class ContinuedFractionGenerator(StepGenerator):
    """Express a rational number as a continued fraction.

    Generates a rational p/q and applies the Euclidean algorithm to
    extract the continued fraction representation [a0; a1, a2, ...].
    Each step shows the integer part extraction and remainder inversion.

    Input format:
        ``express as continued fraction``

    Target format:
        ``\\text{CF}(\\frac{17}{5}) <step> 17/5=3 remainder 2
        <step> 5/2=2 remainder 1 <step> 2/1=2 remainder 0
        <step> [3; 2, 2]``

    Difficulty scaling:
        Difficulty 1-3: numerator in [5, 20], denominator in [2, 7].
        Difficulty 4-6: numerator in [15, 60], denominator in [4, 15].
        Difficulty 7-8: numerator in [30, 120], denominator in [8, 30].

    Prerequisites:
        division, modular.

    Example:
        >>> gen = ContinuedFractionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'continued_fraction'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "continued_fraction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls magnitude of the rational.

        Returns:
            Natural language description.
        """
        return "express as continued fraction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rational number and compute its continued fraction.

        Args:
            difficulty: Controls numerator and denominator ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num, den = self._choose_rational(difficulty)
        computer = ContinuedFractionComputer(num, den)
        coeffs = computer.compute()
        step_details = computer.steps()

        problem = (
            f"\\text{{CF}}"
            f"(\\frac{{{num}}}{{{den}}})"
        )
        return problem, {
            "num": num, "den": den,
            "coeffs": coeffs, "step_details": step_details,
        }

    def _choose_rational(self, difficulty: int) -> tuple[int, int]:
        """Choose numerator and denominator for the rational.

        Ensures numerator > denominator and gcd != denominator
        for a non-trivial continued fraction.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (numerator, denominator).
        """
        n_lo, n_hi, d_lo, d_hi = self._range_bounds(difficulty)
        for _ in range(50):
            num = self._rng.randint(n_lo, n_hi)
            den = self._rng.randint(d_lo, d_hi)
            if num > den and num % den != 0:
                return num, den
        return n_hi, d_lo

    def _range_bounds(self, difficulty: int) -> tuple[int, int, int, int]:
        """Map difficulty to numerator/denominator ranges.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (num_lo, num_hi, den_lo, den_hi).
        """
        if difficulty <= 3:
            return 5, 20, 2, 7
        if difficulty <= 6:
            return 15, 60, 4, 15
        return 30, 120, 8, 30

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euclidean algorithm steps for continued fraction.

        Args:
            data: Solution data with step details.

        Returns:
            Steps showing each division and remainder.
        """
        steps: list[str] = []
        for q, num, den in data["step_details"]:
            remainder = num - q * den
            steps.append(
                f"{num}/{den}={q} remainder {remainder}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the continued fraction representation.

        Args:
            data: Solution data.

        Returns:
            String like '[3; 2, 2]'.
        """
        coeffs = data["coeffs"]
        if len(coeffs) == 1:
            return f"[{coeffs[0]}]"
        rest = ", ".join(str(c) for c in coeffs[1:])
        return f"[{coeffs[0]}; {rest}]"


@register
class DiophantineGenerator(StepGenerator):
    """Solve ax + by = gcd(a, b) using the extended Euclidean algorithm.

    Generates two positive integers a and b, runs the extended Euclidean
    algorithm to find x and y satisfying ax + by = gcd(a, b), and shows
    each division step and the back-substitution.

    Input format:
        ``solve diophantine equation``

    Target format:
        ``35x + 15y = \\gcd(35, 15) <step> 35=2*15+5 <step>
        15=3*5+0 <step> \\gcd=5 <step> back-sub: x=1, y=-2 <step>
        35(1)+15(-2)=5``

    Difficulty scaling:
        Difficulty 1-3: a, b in [6, 30].
        Difficulty 4-6: a, b in [20, 100].
        Difficulty 7-8: a, b in [50, 250].

    Prerequisites:
        gcd, mod_inv.

    Example:
        >>> gen = DiophantineGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'diophantine'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "diophantine"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gcd", "mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls operand magnitude.

        Returns:
            Natural language description.
        """
        return "solve diophantine equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Diophantine equation ax + by = gcd(a, b).

        Args:
            difficulty: Controls operand range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a, b = self._choose_operands(difficulty)
        ee = ExtendedEuclidean(a, b)
        g = ee.gcd()
        x, y = ee.solve()

        problem = f"{a}x + {b}y = \\gcd({a}, {b})"
        return problem, {
            "a": a, "b": b, "gcd": g,
            "x": x, "y": y, "ee": ee,
        }

    def _choose_operands(self, difficulty: int) -> tuple[int, int]:
        """Choose two positive integers with nontrivial GCD computation.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (a, b) with a > b.
        """
        lo, hi = self._operand_bounds(difficulty)
        a = self._rng.randint(lo, hi)
        b = self._rng.randint(lo, hi)
        if b > a:
            a, b = b, a
        if a == b:
            a += 1
        return a, b

    def _operand_bounds(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to operand bounds.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (lower, upper) bounds.
        """
        if difficulty <= 3:
            return 6, 30
        if difficulty <= 6:
            return 20, 100
        return 50, 250

    def _create_steps(self, data: dict) -> list[str]:
        """Generate extended Euclidean algorithm steps.

        Args:
            data: Solution data with the ExtendedEuclidean instance.

        Returns:
            Steps showing division chain and back-substitution.
        """
        ee = data["ee"]
        steps: list[str] = []

        for dividend, divisor, quotient, remainder in ee.division_steps():
            steps.append(
                f"{dividend}={quotient}*{divisor}+{remainder}"
            )

        steps.append(f"\\gcd={data['gcd']}")
        x = data["x"]
        y = data["y"]
        steps.append(f"back-sub: x={x}, y={y}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the verified Bezout identity.

        Args:
            data: Solution data.

        Returns:
            String showing a*x + b*y = gcd.
        """
        a = data["a"]
        b = data["b"]
        x = data["x"]
        y = data["y"]
        g = data["gcd"]
        return f"{a}({x})+{b}({y})={g}"


@register
class RecurrenceSolveGenerator(StepGenerator):
    """Compute the nth term of a first-order linear recurrence a_n = c1*a_{n-1} + c2.

    Generates initial value a_0, multiplier c1, and additive constant c2,
    then iterates to compute a_n for a target n. Each iteration is shown
    as a separate step.

    Input format:
        ``compute recurrence term``

    Target format:
        ``a_n = 2a_{n-1}+3, a_0=1, n=4 <step> a_1=2*1+3=5
        <step> a_2=2*5+3=13 <step> a_3=2*13+3=29
        <step> a_4=2*29+3=61 <step> 61``

    Difficulty scaling:
        Difficulty 1-3: n in [3, 5], c1 in [1, 3], c2 in [0, 5].
        Difficulty 4-6: n in [4, 7], c1 in [2, 5], c2 in [1, 8].
        Difficulty 7-8: n in [5, 8], c1 in [2, 4], c2 in [1, 10].

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = RecurrenceSolveGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'recurrence_solve'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "recurrence_solve"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls recurrence depth.

        Returns:
            Natural language description.
        """
        return "compute recurrence term"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear recurrence and compute the nth term.

        Args:
            difficulty: Controls parameter ranges and n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c1, c2, a0, n = self._choose_params(difficulty)
        sequence = self._iterate(c1, c2, a0, n)

        problem = (
            f"a_n = {c1}a_{{n-1}}+{c2}, a_0={a0}, n={n}"
        )
        return problem, {
            "c1": c1, "c2": c2, "a0": a0,
            "n": n, "sequence": sequence,
        }

    def _choose_params(self, difficulty: int) -> tuple[int, int, int, int]:
        """Choose recurrence parameters based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (c1, c2, a0, n).
        """
        n_lo, n_hi, c1_lo, c1_hi, c2_lo, c2_hi = self._param_ranges(difficulty)
        c1 = self._rng.randint(c1_lo, c1_hi)
        c2 = self._rng.randint(c2_lo, c2_hi)
        a0 = self._rng.randint(1, max(3, difficulty))
        n = self._rng.randint(n_lo, n_hi)
        return c1, c2, a0, n

    def _param_ranges(self, difficulty: int) -> tuple[int, int, int, int, int, int]:
        """Map difficulty to parameter ranges.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_lo, n_hi, c1_lo, c1_hi, c2_lo, c2_hi).
        """
        if difficulty <= 3:
            return 3, 5, 1, 3, 0, 5
        if difficulty <= 6:
            return 4, 7, 2, 5, 1, 8
        return 5, 8, 2, 4, 1, 10

    def _iterate(self, c1: int, c2: int, a0: int,
                 n: int) -> list[int]:
        """Compute the recurrence sequence from a_0 to a_n.

        Args:
            c1: Multiplier.
            c2: Additive constant.
            a0: Initial value.
            n: Number of iterations.

        Returns:
            List [a_0, a_1, ..., a_n].
        """
        seq = [a0]
        for _ in range(n):
            seq.append(c1 * seq[-1] + c2)
        return seq

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-iteration recurrence steps.

        Args:
            data: Solution data with parameters and sequence.

        Returns:
            Steps showing each a_i computation.
        """
        c1 = data["c1"]
        c2 = data["c2"]
        seq = data["sequence"]
        steps: list[str] = []

        for i in range(1, len(seq)):
            prev = seq[i - 1]
            cur = seq[i]
            steps.append(
                f"a_{{{i}}}={c1}*{prev}+{c2}={cur}"
            )

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the nth term.

        Args:
            data: Solution data.

        Returns:
            String representation of a_n.
        """
        return str(data["sequence"][-1])


@register
class PolynomialDivisionGenerator(StepGenerator):
    """Synthetic division of p(x) by (x - a).

    Generates a polynomial with known coefficients and a divisor root,
    then performs synthetic division showing the tableau step by step.
    The quotient and remainder are displayed at the end.

    Input format:
        ``perform polynomial synthetic division``

    Target format:
        ``(x^{3}-6x^{2}+11x-6) \\div (x-1) <step>
        bring down 1 <step> 1*1+(-6)=-5 <step> -5*1+11=6
        <step> 6*1+(-6)=0 <step> Q=x^{2}-5x+6, R=0``

    Difficulty scaling:
        Difficulty 1-3: degree 2-3 polynomial, root in [1, 3].
        Difficulty 4-6: degree 3-4 polynomial, root in [-3, 3].
        Difficulty 7-8: degree 4-5 polynomial, root in [-5, 5].

    Prerequisites:
        polynomial_eval, multiplication.

    Example:
        >>> gen = PolynomialDivisionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'polynomial_division'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "polynomial_division"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial degree and root range.

        Returns:
            Natural language description.
        """
        return "perform polynomial synthetic division"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial and divisor for synthetic division.

        Args:
            difficulty: Controls polynomial degree and root range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        degree, root_lo, root_hi = self._degree_and_root(difficulty)
        root = self._rng.randint(root_lo, root_hi)
        if root == 0:
            root = 1
        coeffs = self._random_coefficients(degree)
        divider = SyntheticDivider(coeffs, root)

        poly_str = self._format_poly(coeffs)
        divisor_str = self._format_divisor(root)
        problem = f"({poly_str}) \\div ({divisor_str})"
        return problem, {"divider": divider}

    def _degree_and_root(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to polynomial degree and root range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (degree, root_lo, root_hi).
        """
        if difficulty <= 3:
            return self._rng.randint(2, 3), 1, 3
        if difficulty <= 6:
            return self._rng.randint(3, 4), -3, 3
        return self._rng.randint(4, 5), -5, 5

    def _random_coefficients(self, degree: int) -> list[int]:
        """Generate random polynomial coefficients.

        The leading coefficient is always nonzero.

        Args:
            degree: Polynomial degree.

        Returns:
            List of coefficients from highest to lowest degree.
        """
        coeffs: list[int] = []
        for i in range(degree + 1):
            coeff = self._rng.randint(-5, 5)
            if i == 0 and coeff == 0:
                coeff = 1
            coeffs.append(coeff)
        return coeffs

    def _format_poly(self, coeffs: list[int]) -> str:
        """Format polynomial coefficients as LaTeX.

        Args:
            coeffs: Coefficients from highest to lowest degree.

        Returns:
            LaTeX polynomial string.
        """
        degree = len(coeffs) - 1
        parts: list[str] = []
        for i, coeff in enumerate(coeffs):
            exp = degree - i
            parts.append(self._format_term(coeff, exp, i == 0))
        result = "".join(parts)
        return result if result else "0"

    def _format_term(self, coeff: int, exp: int,
                     is_first: bool) -> str:
        """Format a single polynomial term.

        Args:
            coeff: Coefficient value.
            exp: Exponent.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        if coeff == 0:
            return ""
        sign = self._sign_prefix(coeff, is_first)
        body = self._term_body(abs(coeff), exp)
        return f"{sign}{body}"

    def _sign_prefix(self, coeff: int, is_first: bool) -> str:
        """Determine sign prefix for a term.

        Args:
            coeff: Coefficient value.
            is_first: Whether this is the leading term.

        Returns:
            Sign string.
        """
        if is_first:
            return "-" if coeff < 0 else ""
        return "-" if coeff < 0 else "+"

    def _term_body(self, abs_coeff: int, exp: int) -> str:
        """Format the body of a polynomial term.

        Args:
            abs_coeff: Absolute coefficient value.
            exp: Exponent.

        Returns:
            Term body string.
        """
        if exp == 0:
            return str(abs_coeff)
        if exp == 1:
            return "x" if abs_coeff == 1 else f"{abs_coeff}x"
        if abs_coeff == 1:
            return f"x^{{{exp}}}"
        return f"{abs_coeff}x^{{{exp}}}"

    def _format_divisor(self, root: int) -> str:
        """Format the divisor (x - root) as LaTeX.

        Args:
            root: Divisor root.

        Returns:
            LaTeX string for the divisor.
        """
        if root > 0:
            return f"x-{root}"
        if root < 0:
            return f"x+{-root}"
        return "x"

    def _format_quotient(self, coeffs: list[int]) -> str:
        """Format quotient polynomial from coefficients.

        Args:
            coeffs: Quotient coefficients from highest to lowest degree.

        Returns:
            LaTeX polynomial string.
        """
        return self._format_poly(coeffs)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate synthetic division tableau steps.

        Args:
            data: Solution data with the SyntheticDivider.

        Returns:
            Steps showing each column of the tableau.
        """
        divider = data["divider"]
        steps: list[str] = []
        coeffs = divider.coefficients()
        steps.append(f"bring down {coeffs[0]}")

        root = divider.root
        for mul, add, result in divider.step_details():
            steps.append(f"{mul}+({add})={result}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the quotient and remainder.

        Args:
            data: Solution data.

        Returns:
            String showing Q=quotient, R=remainder.
        """
        divider = data["divider"]
        q_str = self._format_quotient(divider.quotient_coeffs())
        r = divider.remainder()
        return f"Q={q_str}, R={r}"
