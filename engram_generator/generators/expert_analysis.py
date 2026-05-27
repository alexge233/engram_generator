"""Tier 5 generators — expert/research level mathematics and ML foundations.

Unlocks when Tier 4 tasks are mastered. Introduces chain rule, product rule,
definite integrals, Taylor series, gradient vectors, Newton-Raphson root
finding, Gaussian elimination, Laplace transforms, sigmoid evaluation,
cross-entropy loss, information entropy, and Vigenere cipher decryption.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class CompositeFunction:
    """Represents a composition f(g(x)) for chain rule differentiation.

    Stores an outer function type and an inner polynomial of the form
    ax^n, providing derivative computation and LaTeX formatting for
    both the outer and inner functions.

    Example:
        >>> cf = CompositeFunction("sin", 2, 3)
        >>> cf.inner_latex()
        '2x^{3}'
        >>> cf.outer_deriv_latex()
        '\\\\cos(2x^{3})'
    """

    _OUTER_DERIVS = {
        "sin": "\\cos",
        "cos": "-\\sin",
        "power": "power_deriv",
        "sqrt": "sqrt_deriv",
    }

    def __init__(self, outer_type: str, a: int, n: int,
                 outer_exp: int = 0) -> None:
        """Initialise a composite function.

        Args:
            outer_type: Type of outer function (sin, cos, power, sqrt).
            a: Coefficient of inner polynomial ax^n.
            n: Exponent of inner polynomial ax^n.
            outer_exp: Exponent for power-type outer function.
        """
        self._outer_type = outer_type
        self._a = a
        self._n = n
        self._outer_exp = outer_exp

    def inner_latex(self) -> str:
        """Format the inner function g(x) = ax^n in LaTeX.

        Returns:
            LaTeX string for the inner function.
        """
        if self._n == 1:
            return f"{self._a}x"
        return f"{self._a}x^{{{self._n}}}"

    def inner_deriv_latex(self) -> str:
        """Format the derivative of the inner function g'(x).

        Returns:
            LaTeX string for the inner derivative.
        """
        coeff = self._a * self._n
        exp = self._n - 1
        if exp == 0:
            return str(coeff)
        if exp == 1:
            return f"{coeff}x"
        return f"{coeff}x^{{{exp}}}"

    def composite_latex(self) -> str:
        """Format the full composite function f(g(x)) in LaTeX.

        Returns:
            LaTeX string for the composite function.
        """
        inner = self.inner_latex()
        if self._outer_type == "sin":
            return f"\\sin({inner})"
        if self._outer_type == "cos":
            return f"\\cos({inner})"
        if self._outer_type == "sqrt":
            return f"\\sqrt{{{inner}}}"
        return f"({inner})^{{{self._outer_exp}}}"

    def outer_deriv_latex(self) -> str:
        """Format the derivative of the outer function f'(g(x)).

        Returns:
            LaTeX string for the outer derivative evaluated at g(x).
        """
        inner = self.inner_latex()
        if self._outer_type == "sin":
            return f"\\cos({inner})"
        if self._outer_type == "cos":
            return f"-\\sin({inner})"
        if self._outer_type == "sqrt":
            return f"\\frac{{1}}{{2\\sqrt{{{inner}}}}}"
        exp = self._outer_exp - 1
        return f"{self._outer_exp}({inner})^{{{exp}}}"


class PolynomialPair:
    """Represents two polynomials for product rule differentiation.

    Each polynomial is stored as a list of (coefficient, exponent) pairs.
    Provides derivative computation, LaTeX formatting, and symbolic
    product evaluation needed for the product rule.

    Example:
        >>> p = PolynomialPair([(2, 1), (3, 0)], [(1, 2), (-1, 0)])
        >>> p.f_latex()
        '2x+3'
    """

    def __init__(self, f_terms: list[tuple[int, int]],
                 g_terms: list[tuple[int, int]]) -> None:
        """Initialise with two sets of polynomial terms.

        Args:
            f_terms: Terms of f as (coefficient, exponent) pairs.
            g_terms: Terms of g as (coefficient, exponent) pairs.
        """
        self._f_terms = sorted(f_terms, key=lambda t: -t[1])
        self._g_terms = sorted(g_terms, key=lambda t: -t[1])

    def f_latex(self) -> str:
        """Format polynomial f in LaTeX.

        Returns:
            LaTeX string for f(x).
        """
        return self._format_poly(self._f_terms)

    def g_latex(self) -> str:
        """Format polynomial g in LaTeX.

        Returns:
            LaTeX string for g(x).
        """
        return self._format_poly(self._g_terms)

    def f_deriv_terms(self) -> list[tuple[int, int]]:
        """Compute derivative terms of f using power rule.

        Returns:
            List of (coefficient, exponent) pairs for f'(x).
        """
        return self._differentiate(self._f_terms)

    def g_deriv_terms(self) -> list[tuple[int, int]]:
        """Compute derivative terms of g using power rule.

        Returns:
            List of (coefficient, exponent) pairs for g'(x).
        """
        return self._differentiate(self._g_terms)

    def f_deriv_latex(self) -> str:
        """Format f'(x) in LaTeX.

        Returns:
            LaTeX string for the derivative of f.
        """
        return self._format_poly(self.f_deriv_terms())

    def g_deriv_latex(self) -> str:
        """Format g'(x) in LaTeX.

        Returns:
            LaTeX string for the derivative of g.
        """
        return self._format_poly(self.g_deriv_terms())

    def _differentiate(self, terms: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Apply power rule to each term.

        Args:
            terms: Polynomial terms as (coefficient, exponent) pairs.

        Returns:
            Differentiated terms with zero-exponent terms removed.
        """
        result: list[tuple[int, int]] = []
        for coeff, exp in terms:
            if exp > 0:
                result.append((coeff * exp, exp - 1))
        return result if result else [(0, 0)]

    def _format_poly(self, terms: list[tuple[int, int]]) -> str:
        """Format polynomial terms as a LaTeX string.

        Args:
            terms: List of (coefficient, exponent) pairs.

        Returns:
            Formatted polynomial string.
        """
        if not terms:
            return "0"
        parts: list[str] = []
        for i, (coeff, exp) in enumerate(terms):
            parts.append(self._format_term(coeff, exp, i == 0))
        return "".join(parts) if parts else "0"

    def _format_term(self, coeff: int, exp: int, is_first: bool) -> str:
        """Format a single polynomial term with sign handling.

        Args:
            coeff: Term coefficient.
            exp: Term exponent.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        if coeff == 0:
            return "0" if is_first else ""
        sign = self._sign_str(coeff, is_first)
        body = self._term_body(abs(coeff), exp)
        return f"{sign}{body}"

    def _sign_str(self, coeff: int, is_first: bool) -> str:
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
        """Format the body of a term without sign.

        Args:
            abs_coeff: Absolute coefficient value.
            exp: Exponent value.

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


class AugmentedMatrix:
    """Represents an augmented matrix [A|b] for Gaussian elimination.

    Stores the coefficient matrix and right-hand-side vector,
    providing row operations, LaTeX formatting, and back-substitution.

    Example:
        >>> am = AugmentedMatrix([[2, 1], [1, 3]], [5, 10])
        >>> am.to_latex()  # doctest: +SKIP
        '\\\\left(\\\\begin{array}...'
    """

    def __init__(self, matrix: list[list[Fraction]],
                 rhs: list[Fraction]) -> None:
        """Initialise with coefficient matrix and right-hand side.

        Args:
            matrix: Coefficient matrix as nested lists.
            rhs: Right-hand-side vector.
        """
        self._matrix = [row[:] for row in matrix]
        self._rhs = rhs[:]
        self._n = len(matrix)

    @property
    def n(self) -> int:
        """Return the system dimension."""
        return self._n

    def swap_rows(self, i: int, j: int) -> str:
        """Swap two rows and return a description.

        Args:
            i: First row index.
            j: Second row index.

        Returns:
            Step string describing the swap.
        """
        self._matrix[i], self._matrix[j] = self._matrix[j], self._matrix[i]
        self._rhs[i], self._rhs[j] = self._rhs[j], self._rhs[i]
        return f"R{i+1} \\leftrightarrow R{j+1}"

    def eliminate(self, pivot_row: int, target_row: int) -> str:
        """Eliminate an entry using row operations.

        Swaps rows if the pivot is zero before eliminating.

        Args:
            pivot_row: Row containing the pivot.
            target_row: Row to eliminate from.

        Returns:
            Step string describing the operation.
        """
        pivot_val = self._matrix[pivot_row][pivot_row]
        if pivot_val == Fraction(0):
            swap_row = self._find_nonzero_row(pivot_row)
            if swap_row is not None:
                self.swap_rows(pivot_row, swap_row)
                pivot_val = self._matrix[pivot_row][pivot_row]
        target_val = self._matrix[target_row][pivot_row]
        if target_val == Fraction(0):
            return f"R{target_row+1}: already zero"
        if pivot_val == Fraction(0):
            return f"R{target_row+1}: zero pivot, skip"
        factor = target_val / pivot_val
        self._apply_row_op(pivot_row, target_row, factor)
        return self._format_row_op(pivot_row, target_row, factor)

    def _find_nonzero_row(self, col: int) -> int | None:
        """Find a row below col with a nonzero entry in that column.

        Args:
            col: Column index to check.

        Returns:
            Row index with nonzero entry, or None.
        """
        for row in range(col + 1, self._n):
            if self._matrix[row][col] != Fraction(0):
                return row
        return None

    def _apply_row_op(self, pivot_row: int, target_row: int,
                      factor: Fraction) -> None:
        """Apply R_target = R_target - factor * R_pivot.

        Args:
            pivot_row: Pivot row index.
            target_row: Target row index.
            factor: Elimination factor.
        """
        for col in range(self._n):
            self._matrix[target_row][col] -= factor * self._matrix[pivot_row][col]
        self._rhs[target_row] -= factor * self._rhs[pivot_row]

    def _format_row_op(self, pivot_row: int, target_row: int,
                       factor: Fraction) -> str:
        """Format a row operation as a step string.

        Args:
            pivot_row: Pivot row index.
            target_row: Target row index.
            factor: Elimination factor.

        Returns:
            Formatted operation string.
        """
        f_str = self._format_fraction(factor)
        return f"R{target_row+1} = R{target_row+1} - {f_str}R{pivot_row+1}"

    def back_substitute(self) -> list[Fraction]:
        """Perform back substitution on the upper triangular system.

        Returns:
            Solution vector as a list of Fractions.
        """
        solution = [Fraction(0)] * self._n
        for i in range(self._n - 1, -1, -1):
            solution[i] = self._solve_row(i, solution)
        return solution

    def _solve_row(self, row: int, solution: list[Fraction]) -> Fraction:
        """Solve a single row during back substitution.

        Args:
            row: Row index.
            solution: Partially filled solution vector.

        Returns:
            Value of the variable for this row.
        """
        total = self._rhs[row]
        for col in range(row + 1, self._n):
            total -= self._matrix[row][col] * solution[col]
        return total / self._matrix[row][row]

    def to_latex(self) -> str:
        """Format the augmented matrix in LaTeX.

        Returns:
            LaTeX string for the augmented matrix.
        """
        cols = "c" * self._n + "|c"
        rows: list[str] = []
        for i in range(self._n):
            entries = [self._format_fraction(v) for v in self._matrix[i]]
            entries.append(self._format_fraction(self._rhs[i]))
            rows.append(" & ".join(entries))
        body = " \\\\ ".join(rows)
        return f"\\left(\\begin{{array}}{{{cols}}} {body} \\end{{array}}\\right)"

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as a clean string.

        Args:
            val: Fraction value.

        Returns:
            Integer string if whole, otherwise fraction string.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"


class TaylorTermComputer:
    """Computes Taylor series terms for standard functions at x=0.

    Provides the nth derivative evaluated at zero and the factorial
    denominator for e^x, sin(x), and cos(x), enabling step-by-step
    Taylor expansion.

    Example:
        >>> tc = TaylorTermComputer("exp")
        >>> tc.nth_deriv_at_zero(3)
        1
        >>> tc.term_latex(3)
        '\\\\frac{1}{6}x^{3}'
    """

    def __init__(self, func_type: str) -> None:
        """Initialise for a specific function type.

        Args:
            func_type: One of 'exp', 'sin', 'cos'.
        """
        self._func_type = func_type

    def nth_deriv_at_zero(self, n: int) -> int:
        """Compute f^{(n)}(0) for the chosen function.

        Args:
            n: Derivative order.

        Returns:
            Value of the nth derivative at zero.
        """
        if self._func_type == "exp":
            return 1
        if self._func_type == "sin":
            return self._sin_deriv(n)
        return self._cos_deriv(n)

    def _sin_deriv(self, n: int) -> int:
        """Compute the nth derivative of sin(x) at x=0.

        Args:
            n: Derivative order.

        Returns:
            Value from the cycle [0, 1, 0, -1, ...].
        """
        cycle = [0, 1, 0, -1]
        return cycle[n % 4]

    def _cos_deriv(self, n: int) -> int:
        """Compute the nth derivative of cos(x) at x=0.

        Args:
            n: Derivative order.

        Returns:
            Value from the cycle [1, 0, -1, 0, ...].
        """
        cycle = [1, 0, -1, 0]
        return cycle[n % 4]

    def term_latex(self, n: int) -> str:
        """Format the nth Taylor term as LaTeX.

        Args:
            n: Term index.

        Returns:
            LaTeX string for f^{(n)}(0)/n! * x^n, or empty if zero.
        """
        deriv = self.nth_deriv_at_zero(n)
        if deriv == 0:
            return ""
        factorial = math.factorial(n)
        frac = Fraction(deriv, factorial)
        return self._format_term(frac, n)

    def _format_term(self, frac: Fraction, n: int) -> str:
        """Format a fraction times x^n as LaTeX.

        Args:
            frac: Coefficient as a Fraction.
            n: Exponent.

        Returns:
            LaTeX string for the term.
        """
        if n == 0:
            return self._format_coeff(frac)
        x_part = "x" if n == 1 else f"x^{{{n}}}"
        coeff = self._format_coeff(frac)
        if coeff == "1":
            return x_part
        if coeff == "-1":
            return f"-{x_part}"
        return f"{coeff}{x_part}"

    def _format_coeff(self, frac: Fraction) -> str:
        """Format a Fraction coefficient as LaTeX.

        Args:
            frac: Fraction value.

        Returns:
            LaTeX string for the coefficient.
        """
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"

    def func_latex(self) -> str:
        """Return the LaTeX representation of the function.

        Returns:
            LaTeX function name string.
        """
        if self._func_type == "exp":
            return "e^x"
        if self._func_type == "sin":
            return "\\sin(x)"
        return "\\cos(x)"

    def step_detail(self, n: int) -> str:
        """Format the detailed step showing f^{(n)}(0)/n!.

        Args:
            n: Term index.

        Returns:
            Step string showing the derivative and factorial.
        """
        deriv = self.nth_deriv_at_zero(n)
        factorial = math.factorial(n)
        return f"f^{{({n})}}(0)={deriv}, {n}!={factorial}"


class LaplaceEntry:
    """Represents a Laplace transform table entry.

    Stores the time-domain function, its Laplace transform formula,
    parameter values, and the resulting s-domain expression.

    Example:
        >>> entry = LaplaceEntry("t^n", "\\\\frac{n!}{s^{n+1}}", {"n": 3})
        >>> entry.func_latex()
        't^{3}'
    """

    _TEMPLATES = {
        "power": ("t^{{{n}}}", "\\frac{{{n}!}}{{s^{{{ns1}}}}}"),
        "exp": ("e^{{{a}t}}", "\\frac{{1}}{{s-{a}}}"),
        "sin": ("\\sin({a}t)", "\\frac{{{a}}}{{s^2+{asq}}}"),
    }

    def __init__(self, entry_type: str, params: dict) -> None:
        """Initialise a Laplace transform entry.

        Args:
            entry_type: Type of entry (power, exp, sin).
            params: Parameter dictionary for the template.
        """
        self._entry_type = entry_type
        self._params = params

    def func_latex(self) -> str:
        """Format the time-domain function in LaTeX.

        Returns:
            LaTeX string for f(t).
        """
        template = self._TEMPLATES[self._entry_type][0]
        return template.format(**self._params)

    def transform_formula(self) -> str:
        """Format the general Laplace transform formula.

        Returns:
            LaTeX string for the transform formula.
        """
        if self._entry_type == "power":
            return "L\\{t^n\\} = \\frac{n!}{s^{n+1}}"
        if self._entry_type == "exp":
            return "L\\{e^{at}\\} = \\frac{1}{s-a}"
        return "L\\{\\sin(at)\\} = \\frac{a}{s^2+a^2}"

    def result_latex(self) -> str:
        """Format the specific Laplace transform result.

        Returns:
            LaTeX string for the evaluated transform.
        """
        template = self._TEMPLATES[self._entry_type][1]
        return template.format(**self._params)


@register
class ChainRuleGenerator(StepGenerator):
    """Chain rule differentiation of composite functions f(g(x)).

    Generates compositions of simple functions (sin, cos, power, sqrt)
    with inner polynomials of the form ax^n. Shows the outer derivative
    evaluated at g(x) multiplied by the inner derivative g'(x).

    Input format:
        ``differentiate composite function``

    Target format:
        ``\\frac{d}{dx}\\sin(3x^{2}) <step> f'(g(x))=\\cos(3x^{2})
        <step> g'(x)=6x <step> \\cos(3x^{2}) \\cdot 6x``

    Difficulty scaling:
        Difficulty 1-3: sin/cos with small coefficients and exponents.
        Difficulty 4-6: power compositions with moderate exponents.
        Difficulty 7-8: sqrt compositions with larger inner polynomials.

    Prerequisites:
        derivative.

    Example:
        >>> gen = ChainRuleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'chain_rule'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "chain_rule"

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
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "differentiate composite function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a composite function and compute its chain rule derivative.

        Args:
            difficulty: Controls outer function type and inner complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        comp = self._build_composite(difficulty)
        problem = f"\\frac{{d}}{{dx}}{comp.composite_latex()}"
        return problem, {"composite": comp}

    def _build_composite(self, difficulty: int) -> CompositeFunction:
        """Build a composite function appropriate for the difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A CompositeFunction instance.
        """
        a = self._rng.randint(1, max(2, difficulty))
        n = self._rng.randint(1, min(3, 1 + difficulty // 2))
        outer_type = self._select_outer_type(difficulty)
        outer_exp = self._rng.randint(2, 4) if outer_type == "power" else 0
        return CompositeFunction(outer_type, a, n, outer_exp)

    def _select_outer_type(self, difficulty: int) -> str:
        """Select the outer function type based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Outer function type string.
        """
        if difficulty <= 3:
            return self._rng.choice(["sin", "cos"])
        if difficulty <= 6:
            return self._rng.choice(["sin", "cos", "power"])
        return self._rng.choice(["sin", "cos", "power", "sqrt"])

    def _create_steps(self, data: dict) -> list[str]:
        """Generate chain rule application steps.

        Args:
            data: Solution data with the composite function.

        Returns:
            Steps showing outer derivative, inner derivative, and product.
        """
        comp = data["composite"]
        return [
            f"f'(g(x))={comp.outer_deriv_latex()}",
            f"g'(x)={comp.inner_deriv_latex()}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the chain rule result.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for f'(g(x)) * g'(x).
        """
        comp = data["composite"]
        return f"{comp.outer_deriv_latex()} \\cdot {comp.inner_deriv_latex()}"


@register
class ProductRuleGenerator(StepGenerator):
    """Product rule differentiation d/dx(f*g) = f'g + fg'.

    Generates two polynomial functions and applies the product rule,
    showing f'(x), g'(x), and the two terms f'g + fg'. Uses polynomials
    only (no trigonometric functions) for verifiability.

    Input format:
        ``differentiate product of functions``

    Target format:
        ``\\frac{d}{dx}[(2x+3)(x^{2}-1)] <step> f'(x)=2 <step>
        g'(x)=2x <step> f'g+fg'=(2)(x^{2}-1)+(2x+3)(2x)``

    Difficulty scaling:
        Difficulty 1-3: linear times linear (degree 1 each).
        Difficulty 4-6: linear times quadratic.
        Difficulty 7-8: quadratic times quadratic.

    Prerequisites:
        derivative, multiplication.

    Example:
        >>> gen = ProductRuleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'product_rule'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "product_rule"

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
            difficulty: Controls polynomial degree.

        Returns:
            Natural language description.
        """
        return "differentiate product of functions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two polynomials and set up the product rule.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pair = self._build_pair(difficulty)
        problem = f"\\frac{{d}}{{dx}}[({pair.f_latex()})({pair.g_latex()})]"
        return problem, {"pair": pair}

    def _build_pair(self, difficulty: int) -> PolynomialPair:
        """Build a pair of polynomials scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A PolynomialPair instance.
        """
        f_deg, g_deg = self._select_degrees(difficulty)
        f_terms = self._random_poly(f_deg)
        g_terms = self._random_poly(g_deg)
        return PolynomialPair(f_terms, g_terms)

    def _select_degrees(self, difficulty: int) -> tuple[int, int]:
        """Select polynomial degrees based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (f_degree, g_degree).
        """
        if difficulty <= 3:
            return 1, 1
        if difficulty <= 6:
            return 1, 2
        return 2, 2

    def _random_poly(self, degree: int) -> list[tuple[int, int]]:
        """Generate random polynomial terms with given degree.

        Args:
            degree: Maximum exponent.

        Returns:
            List of (coefficient, exponent) pairs.
        """
        terms: list[tuple[int, int]] = []
        for exp in range(degree, -1, -1):
            coeff = self._rng.randint(-5, 5)
            if coeff == 0:
                coeff = 1
            terms.append((coeff, exp))
        return terms

    def _create_steps(self, data: dict) -> list[str]:
        """Generate product rule application steps.

        Args:
            data: Solution data with the polynomial pair.

        Returns:
            Steps showing f', g', and the product rule formula.
        """
        pair = data["pair"]
        return [
            f"f'(x)={pair.f_deriv_latex()}",
            f"g'(x)={pair.g_deriv_latex()}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the product rule result.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for f'g + fg'.
        """
        pair = data["pair"]
        return (
            f"({pair.f_deriv_latex()})({pair.g_latex()})"
            f"+({pair.f_latex()})({pair.g_deriv_latex()})"
        )


@register
class DefiniteIntegralGenerator(StepGenerator):
    """Definite integral of polynomials with integer bounds.

    Generates a polynomial integrand with integer bounds, computes
    the antiderivative using the power rule, and evaluates F(b)-F(a)
    for a clean integer result.

    Input format:
        ``compute definite integral``

    Target format:
        ``\\int_1^3 2x^2 dx <step> F(x)=\\frac{2}{3}x^{3} <step>
        F(3)-F(1)=18-\\frac{2}{3} <step> \\frac{52}{3}``

    Difficulty scaling:
        Difficulty 1-3: single-term integrand, small bounds.
        Difficulty 4-6: two-term integrand, wider bounds.
        Difficulty 7-8: three-term integrand, larger bounds.

    Prerequisites:
        integral, subtraction.

    Example:
        >>> gen = DefiniteIntegralGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'definite_integral'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "definite_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["integral", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Natural language description.
        """
        return "compute definite integral"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate integrand, bounds, and compute the definite integral.

        Args:
            difficulty: Controls term count and bound magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        terms = self._generate_terms(difficulty)
        a, b = self._generate_bounds(difficulty)
        antideriv = self._antiderivative(terms)
        fa = self._evaluate_antideriv(antideriv, a)
        fb = self._evaluate_antideriv(antideriv, b)
        result = fb - fa

        integrand_latex = self._format_integrand(terms)
        problem = f"\\int_{{{a}}}^{{{b}}} {integrand_latex} \\, dx"
        return problem, {
            "terms": terms, "antideriv": antideriv,
            "a": a, "b": b, "fa": fa, "fb": fb, "result": result,
        }

    def _generate_terms(self, difficulty: int) -> list[tuple[int, int]]:
        """Generate polynomial integrand terms.

        Args:
            difficulty: Controls number of terms.

        Returns:
            List of (coefficient, exponent) pairs.
        """
        num_terms = min(1 + difficulty // 3, 3)
        terms: list[tuple[int, int]] = []
        for i in range(num_terms):
            coeff = self._rng.randint(1, max(2, difficulty))
            exp = num_terms - i
            terms.append((coeff, exp))
        return terms

    def _generate_bounds(self, difficulty: int) -> tuple[int, int]:
        """Generate integer integration bounds.

        Args:
            difficulty: Controls bound magnitude.

        Returns:
            Tuple of (lower_bound, upper_bound).
        """
        a = self._rng.randint(0, max(1, difficulty // 2))
        b = a + self._rng.randint(1, max(2, difficulty))
        return a, b

    def _antiderivative(self, terms: list[tuple[int, int]]) -> list[tuple[Fraction, int]]:
        """Compute the antiderivative terms using the power rule.

        Args:
            terms: Integrand terms as (coefficient, exponent) pairs.

        Returns:
            Antiderivative terms as (Fraction_coefficient, new_exponent).
        """
        result: list[tuple[Fraction, int]] = []
        for coeff, exp in terms:
            new_exp = exp + 1
            new_coeff = Fraction(coeff, new_exp)
            result.append((new_coeff, new_exp))
        return result

    def _evaluate_antideriv(self, terms: list[tuple[Fraction, int]],
                            x: int) -> Fraction:
        """Evaluate the antiderivative at a point.

        Args:
            terms: Antiderivative terms as (Fraction, exponent) pairs.
            x: Point to evaluate at.

        Returns:
            Evaluated Fraction value.
        """
        total = Fraction(0)
        for coeff, exp in terms:
            total += coeff * Fraction(x ** exp)
        return total

    def _format_integrand(self, terms: list[tuple[int, int]]) -> str:
        """Format integrand terms as a LaTeX polynomial.

        Args:
            terms: List of (coefficient, exponent) pairs.

        Returns:
            LaTeX polynomial string.
        """
        parts: list[str] = []
        for i, (coeff, exp) in enumerate(terms):
            sign = "" if i == 0 else "+"
            if exp == 0:
                parts.append(f"{sign}{coeff}")
            elif exp == 1:
                parts.append(f"{sign}{coeff}x")
            else:
                parts.append(f"{sign}{coeff}x^{{{exp}}}")
        return "".join(parts)

    def _format_antideriv(self, terms: list[tuple[Fraction, int]]) -> str:
        """Format antiderivative terms as LaTeX.

        Args:
            terms: Antiderivative terms as (Fraction, exponent) pairs.

        Returns:
            LaTeX antiderivative string.
        """
        parts: list[str] = []
        for i, (coeff, exp) in enumerate(terms):
            sign = "" if i == 0 else "+"
            coeff_str = self._format_frac(coeff)
            if exp == 1:
                parts.append(f"{sign}{coeff_str}x")
            else:
                parts.append(f"{sign}{coeff_str}x^{{{exp}}}")
        return "".join(parts)

    def _format_frac(self, val: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            val: Fraction value.

        Returns:
            LaTeX string.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate antiderivative and evaluation steps.

        Args:
            data: Solution data with antiderivative, bounds, and values.

        Returns:
            Steps showing F(x), F(b)-F(a), and the result.
        """
        antideriv_latex = self._format_antideriv(data["antideriv"])
        fb_str = self._format_frac(data["fb"])
        fa_str = self._format_frac(data["fa"])
        return [
            f"F(x)={antideriv_latex}",
            f"F({data['b']})-F({data['a']})={fb_str}-{fa_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the definite integral result.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return self._format_frac(data["result"])


@register
class TaylorSeriesGenerator(StepGenerator):
    """Taylor series expansion for standard functions at x=0.

    Generates Taylor series expansions for e^x, sin(x), or cos(x)
    centered at zero, showing f^{(n)}(0)/n! for each term. The
    number of terms scales with difficulty.

    Input format:
        ``compute taylor series terms``

    Target format:
        ``T(e^x, 3 terms) <step> f^{(0)}(0)=1, 0!=1: 1 <step>
        f^{(1)}(0)=1, 1!=1: x <step> f^{(2)}(0)=1, 2!=2:
        \\frac{1}{2}x^{2} <step> 1+x+\\frac{1}{2}x^{2}``

    Difficulty scaling:
        Difficulty 1-2: 3 terms.
        Difficulty 3-5: 5 terms.
        Difficulty 6-8: 7 terms.

    Prerequisites:
        derivative, factorial via permutation.

    Example:
        >>> gen = TaylorSeriesGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'taylor_series'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "taylor_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "permutation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Natural language description.
        """
        return "compute taylor series terms"

    def _num_terms(self, difficulty: int) -> int:
        """Map difficulty to number of Taylor terms.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Number of terms to compute (3, 5, or 7).
        """
        if difficulty <= 2:
            return 3
        if difficulty <= 5:
            return 5
        return 7

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Taylor series expansion problem.

        Args:
            difficulty: Controls term count and function choice.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        func_type = self._rng.choice(["exp", "sin", "cos"])
        num_terms = self._num_terms(difficulty)
        computer = TaylorTermComputer(func_type)

        problem = f"T({computer.func_latex()}, {num_terms} terms)"
        return problem, {"computer": computer, "num_terms": num_terms}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-term Taylor expansion steps.

        Args:
            data: Solution data with the term computer and count.

        Returns:
            Steps showing f^{(n)}(0)/n! for each term.
        """
        computer = data["computer"]
        num_terms = data["num_terms"]
        steps: list[str] = []

        for n in range(num_terms):
            term_latex = computer.term_latex(n)
            detail = computer.step_detail(n)
            display = term_latex if term_latex else "0"
            steps.append(f"{detail}: {display}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Taylor series as a sum of terms.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the Taylor polynomial.
        """
        computer = data["computer"]
        num_terms = data["num_terms"]
        nonzero: list[str] = []

        for n in range(num_terms):
            term = computer.term_latex(n)
            if term:
                nonzero.append(term)

        return "+".join(nonzero) if nonzero else "0"


@register
class GradientGenerator(StepGenerator):
    """Gradient vector computation for bivariate functions f(x,y).

    Generates a polynomial in x and y, computes both partial
    derivatives, and assembles them into the gradient vector
    nabla f = (df/dx, df/dy).

    Input format:
        ``compute gradient vector``

    Target format:
        ``\\nabla f = (\\frac{\\partial f}{\\partial x},
        \\frac{\\partial f}{\\partial y}) <step>
        \\frac{\\partial f}{\\partial x}=6xy <step>
        \\frac{\\partial f}{\\partial y}=3x^{2} <step>
        \\nabla f = (6xy, 3x^{2})``

    Difficulty scaling:
        Difficulty 1-3: 2 terms, small exponents.
        Difficulty 4-6: 3 terms, moderate exponents.
        Difficulty 7-8: 4 terms, higher exponents.

    Prerequisites:
        partial_derivative.

    Example:
        >>> gen = GradientGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gradient'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gradient"

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
            difficulty: Controls polynomial complexity.

        Returns:
            Natural language description.
        """
        return "compute gradient vector"

    def _num_terms(self, difficulty: int) -> int:
        """Map difficulty to term count.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of terms (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bivariate polynomial and compute its gradient.

        Args:
            difficulty: Controls term count and exponent range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        terms = self._generate_terms(difficulty)
        dx_terms = self._partial_x(terms)
        dy_terms = self._partial_y(terms)

        poly_latex = "+".join(self._term_latex(t) for t in terms)
        problem = f"\\nabla f(x,y) \\text{{ where }} f={poly_latex}"
        return problem, {
            "terms": terms, "dx_terms": dx_terms, "dy_terms": dy_terms,
        }

    def _generate_terms(self, difficulty: int) -> list[tuple[int, int, int]]:
        """Generate bivariate polynomial terms as (coeff, x_exp, y_exp).

        Args:
            difficulty: Controls exponent range and count.

        Returns:
            List of (coefficient, x_exponent, y_exponent) triples.
        """
        n = self._num_terms(difficulty)
        max_exp = min(2 + difficulty // 2, 4)
        terms: list[tuple[int, int, int]] = []

        for _ in range(n):
            coeff = self._rng.randint(1, max(3, difficulty))
            x_exp = self._rng.randint(1, max_exp)
            y_exp = self._rng.randint(1, max_exp)
            terms.append((coeff, x_exp, y_exp))

        return terms

    def _partial_x(self, terms: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
        """Compute partial derivative with respect to x for all terms.

        Args:
            terms: Bivariate polynomial terms.

        Returns:
            Differentiated terms (zero-coefficient terms excluded).
        """
        result: list[tuple[int, int, int]] = []
        for coeff, x_exp, y_exp in terms:
            if x_exp > 0:
                result.append((coeff * x_exp, x_exp - 1, y_exp))
        return result

    def _partial_y(self, terms: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
        """Compute partial derivative with respect to y for all terms.

        Args:
            terms: Bivariate polynomial terms.

        Returns:
            Differentiated terms (zero-coefficient terms excluded).
        """
        result: list[tuple[int, int, int]] = []
        for coeff, x_exp, y_exp in terms:
            if y_exp > 0:
                result.append((coeff * y_exp, x_exp, y_exp - 1))
        return result

    def _term_latex(self, term: tuple[int, int, int]) -> str:
        """Format a single bivariate term in LaTeX.

        Args:
            term: Tuple of (coefficient, x_exponent, y_exponent).

        Returns:
            LaTeX string for the term.
        """
        coeff, x_exp, y_exp = term
        parts = str(coeff) if coeff != 1 else ""
        parts += self._var_latex("x", x_exp)
        parts += self._var_latex("y", y_exp)
        return parts if parts else str(coeff)

    def _var_latex(self, var: str, exp: int) -> str:
        """Format a variable with exponent in LaTeX.

        Args:
            var: Variable name.
            exp: Exponent value.

        Returns:
            LaTeX variable string.
        """
        if exp == 0:
            return ""
        if exp == 1:
            return var
        return f"{var}^{{{exp}}}"

    def _terms_latex(self, terms: list[tuple[int, int, int]]) -> str:
        """Format a list of bivariate terms as a LaTeX sum.

        Args:
            terms: List of (coefficient, x_exp, y_exp) triples.

        Returns:
            LaTeX polynomial string.
        """
        if not terms:
            return "0"
        return "+".join(self._term_latex(t) for t in terms)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate partial derivative steps for both variables.

        Args:
            data: Solution data with terms and partial derivatives.

        Returns:
            Steps showing df/dx and df/dy.
        """
        dx_latex = self._terms_latex(data["dx_terms"])
        dy_latex = self._terms_latex(data["dy_terms"])
        return [
            f"\\frac{{\\partial f}}{{\\partial x}}={dx_latex}",
            f"\\frac{{\\partial f}}{{\\partial y}}={dy_latex}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the gradient vector.

        Args:
            data: Solution data.

        Returns:
            LaTeX gradient vector string.
        """
        dx_latex = self._terms_latex(data["dx_terms"])
        dy_latex = self._terms_latex(data["dy_terms"])
        return f"\\nabla f = ({dx_latex}, {dy_latex})"


@register
class NewtonRaphsonGenerator(StepGenerator):
    """Newton-Raphson iterative root finding method.

    Generates a simple polynomial with a known root, picks a
    starting point near that root, and shows 3-5 iterations of
    x_{n+1} = x_n - f(x_n)/f'(x_n) converging toward the root.

    Input format:
        ``find root using newton raphson method``

    Target format:
        ``x^2-4, x_0=3 <step> f(3)=5, f'(3)=6 <step>
        x_1=3-5/6=2.1667 <step> ... <step> x_n=2.0000``

    Difficulty scaling:
        Difficulty 1-3: quadratic, 3 iterations.
        Difficulty 4-6: cubic, 4 iterations.
        Difficulty 7-8: cubic, 5 iterations.

    Prerequisites:
        derivative, division.

    Example:
        >>> gen = NewtonRaphsonGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'newton_raphson'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "newton_raphson"

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
            difficulty: Controls polynomial degree and iteration count.

        Returns:
            Natural language description.
        """
        return "find root using newton raphson method"

    def _num_iterations(self, difficulty: int) -> int:
        """Map difficulty to iteration count.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of Newton-Raphson iterations (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial root-finding problem.

        Args:
            difficulty: Controls polynomial type and iterations.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        root = self._rng.randint(1, max(3, difficulty))
        coeffs, poly_latex = self._build_polynomial(difficulty, root)
        x0 = float(root + self._rng.randint(1, 3))
        iterations = self._run_iterations(coeffs, x0, self._num_iterations(difficulty))

        problem = f"{poly_latex}, x_0={self._fmt(x0)}"
        return problem, {
            "coeffs": coeffs, "poly_latex": poly_latex,
            "x0": x0, "root": root, "iterations": iterations,
        }

    def _build_polynomial(self, difficulty: int,
                          root: int) -> tuple[list[int], str]:
        """Build a polynomial with a known root.

        Args:
            difficulty: Controls degree (quadratic or cubic).
            root: A known integer root.

        Returns:
            Tuple of (coefficient_list, latex_string).
        """
        if difficulty <= 3:
            return self._quadratic(root)
        return self._cubic(root)

    def _quadratic(self, root: int) -> tuple[list[int], str]:
        """Build x^2 - root^2 (roots at +/-root).

        Args:
            root: Positive integer root.

        Returns:
            Tuple of (coefficients, latex_string).
        """
        c = root * root
        return [1, 0, -c], f"x^2-{c}"

    def _cubic(self, root: int) -> tuple[list[int], str]:
        """Build x^3 - root^3 (one real root at x=root).

        Args:
            root: Positive integer root.

        Returns:
            Tuple of (coefficients, latex_string).
        """
        c = root ** 3
        return [1, 0, 0, -c], f"x^3-{c}"

    def _eval_poly(self, coeffs: list[int], x: float) -> float:
        """Evaluate a polynomial at x using Horner's method.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Evaluation point.

        Returns:
            Polynomial value at x.
        """
        result = 0.0
        for c in coeffs:
            result = result * x + c
        return result

    def _eval_deriv(self, coeffs: list[int], x: float) -> float:
        """Evaluate the derivative of a polynomial at x.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Evaluation point.

        Returns:
            Derivative value at x.
        """
        n = len(coeffs) - 1
        deriv_coeffs = [coeffs[i] * (n - i) for i in range(n)]
        return self._eval_poly(deriv_coeffs, x)

    def _run_iterations(self, coeffs: list[int], x0: float,
                        num_iter: int) -> list[dict]:
        """Run Newton-Raphson iterations and record each step.

        Args:
            coeffs: Polynomial coefficients.
            x0: Starting point.
            num_iter: Number of iterations.

        Returns:
            List of dicts with x, fx, fpx, and x_next for each iteration.
        """
        iterations: list[dict] = []
        x = x0
        for _ in range(num_iter):
            fx = self._eval_poly(coeffs, x)
            fpx = self._eval_deriv(coeffs, x)
            x_next = x - fx / fpx if fpx != 0 else x
            iterations.append({
                "x": x, "fx": round(fx, 4),
                "fpx": round(fpx, 4), "x_next": round(x_next, 4),
            })
            x = x_next
        return iterations

    def _fmt(self, val: float) -> str:
        """Format a float, removing trailing zeros.

        Args:
            val: Float value.

        Returns:
            Clean string representation.
        """
        if val == int(val):
            return str(int(val))
        return f"{val:.4f}".rstrip("0").rstrip(".")

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-iteration Newton-Raphson steps.

        Args:
            data: Solution data with iteration records.

        Returns:
            Steps showing f(x_n), f'(x_n), and x_{n+1}.
        """
        iterations = data["iterations"]
        steps: list[str] = []

        for i, it in enumerate(iterations):
            x_str = self._fmt(it["x"])
            fx_str = self._fmt(it["fx"])
            fpx_str = self._fmt(it["fpx"])
            xn_str = self._fmt(it["x_next"])
            steps.append(
                f"f({x_str})={fx_str}, f'({x_str})={fpx_str}, "
                f"x_{{{i+1}}}={x_str}-{fx_str}/{fpx_str}={xn_str}"
            )

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final Newton-Raphson approximation.

        Args:
            data: Solution data.

        Returns:
            String representation of the last x value.
        """
        return self._fmt(data["iterations"][-1]["x_next"])


@register
class GaussianEliminationGenerator(StepGenerator):
    """Solve linear systems by Gaussian elimination with row reduction.

    Generates 2x2 or 3x3 linear systems with integer solutions,
    constructs the augmented matrix in LaTeX, and shows step-by-step
    row operations followed by back substitution.

    Input format:
        ``solve system by gaussian elimination``

    Target format:
        ``\\left(\\begin{array}{cc|c} 2 & 1 & 5 \\\\ 1 & 3 & 10
        \\end{array}\\right) <step> R2 = R2 - \\frac{1}{2}R1 <step>
        back sub: x_2=3, x_1=1 <step> x=[1, 3]``

    Difficulty scaling:
        Difficulty 1-4: 2x2 systems.
        Difficulty 5-8: 3x3 systems.
        Coefficients scale with difficulty.

    Prerequisites:
        matrix_multiply, division.

    Example:
        >>> gen = GaussianEliminationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gaussian_elimination'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gaussian_elimination"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system size.

        Returns:
            Natural language description.
        """
        return "solve system by gaussian elimination"

    def _system_size(self, difficulty: int) -> int:
        """Determine system size from difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            System dimension (2 or 3).
        """
        return 3 if difficulty >= 5 else 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear system with integer solutions.

        Args:
            difficulty: Controls system size and coefficient range.

        Returns:
            Tuple of (latex_augmented_matrix, solution_data).
        """
        n = self._system_size(difficulty)
        solution = self._random_solution(n, difficulty)
        matrix, rhs = self._build_system(n, solution, difficulty)
        aug = AugmentedMatrix(
            [[Fraction(v) for v in row] for row in matrix],
            [Fraction(v) for v in rhs],
        )

        return aug.to_latex(), {
            "aug": aug, "solution": solution, "n": n,
            "matrix": matrix, "rhs": rhs,
        }

    def _random_solution(self, n: int, difficulty: int) -> list[int]:
        """Generate a random integer solution vector.

        Args:
            n: System dimension.
            difficulty: Controls solution magnitude.

        Returns:
            List of integer solution values.
        """
        bound = max(3, difficulty * 2)
        return [self._rng.randint(-bound, bound) for _ in range(n)]

    def _build_system(self, n: int, solution: list[int],
                      difficulty: int) -> tuple[list[list[int]], list[int]]:
        """Build Ax=b with known integer solution x.

        Args:
            n: System dimension.
            solution: Known solution vector.
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (coefficient_matrix, rhs_vector).
        """
        bound = max(2, difficulty)
        matrix = self._random_nonsingular_matrix(n, bound)
        rhs = self._compute_rhs(matrix, solution)
        return matrix, rhs

    def _random_nonsingular_matrix(self, n: int,
                                   bound: int) -> list[list[int]]:
        """Generate a random nonsingular integer matrix.

        Args:
            n: Matrix dimension.
            bound: Absolute value bound for entries.

        Returns:
            Nonsingular integer matrix.
        """
        for _ in range(100):
            matrix = [
                [self._rng.randint(-bound, bound) for _ in range(n)]
                for _ in range(n)
            ]
            if self._is_nonsingular(matrix):
                return matrix
        return self._identity_matrix(n)

    def _is_nonsingular(self, matrix: list[list[int]]) -> bool:
        """Check if a matrix is nonsingular using Fraction determinant.

        Args:
            matrix: Square integer matrix.

        Returns:
            True if determinant is nonzero.
        """
        n = len(matrix)
        work = [[Fraction(v) for v in row] for row in matrix]
        det = Fraction(1)

        for col in range(n):
            pivot = self._find_pivot(work, col)
            if pivot is None:
                return False
            if pivot != col:
                work[col], work[pivot] = work[pivot], work[col]
                det = -det
            det *= work[col][col]
            self._eliminate_column(work, col)

        return det != 0

    def _find_pivot(self, matrix: list[list[Fraction]],
                    col: int) -> int | None:
        """Find a nonzero pivot in the given column.

        Args:
            matrix: Working matrix.
            col: Column index.

        Returns:
            Row index of nonzero pivot, or None.
        """
        for row in range(col, len(matrix)):
            if matrix[row][col] != 0:
                return row
        return None

    def _eliminate_column(self, matrix: list[list[Fraction]],
                          col: int) -> None:
        """Eliminate entries below the pivot in a column.

        Args:
            matrix: Working matrix to modify.
            col: Pivot column index.
        """
        n = len(matrix)
        for row in range(col + 1, n):
            if matrix[row][col] != 0:
                factor = matrix[row][col] / matrix[col][col]
                for k in range(col, n):
                    matrix[row][k] -= factor * matrix[col][k]

    def _identity_matrix(self, n: int) -> list[list[int]]:
        """Generate an identity matrix as a fallback.

        Args:
            n: Matrix dimension.

        Returns:
            Identity matrix.
        """
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def _compute_rhs(self, matrix: list[list[int]],
                     solution: list[int]) -> list[int]:
        """Compute b = A * x for the right-hand side.

        Args:
            matrix: Coefficient matrix.
            solution: Solution vector.

        Returns:
            Right-hand-side vector.
        """
        n = len(matrix)
        rhs: list[int] = []
        for i in range(n):
            val = sum(matrix[i][j] * solution[j] for j in range(n))
            rhs.append(val)
        return rhs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate row reduction and back substitution steps.

        Args:
            data: Solution data with augmented matrix.

        Returns:
            Steps showing each row operation and back substitution.
        """
        aug = data["aug"]
        steps: list[str] = []

        for col in range(aug.n - 1):
            for row in range(col + 1, aug.n):
                step = aug.eliminate(col, row)
                steps.append(step)

        steps.append(f"upper triangular: {aug.to_latex()}")
        solution = data["solution"]
        var_strs = [f"x_{{{i+1}}}={solution[i]}" for i in range(len(solution))]
        steps.append(f"back sub: {', '.join(var_strs)}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solution vector.

        Args:
            data: Solution data.

        Returns:
            String representation of the solution.
        """
        return f"x={data['solution']}"


@register
class LaplaceTransformGenerator(StepGenerator):
    """Laplace transform of simple time-domain functions.

    Generates problems using standard Laplace transform table entries:
    L{t^n} = n!/s^{n+1}, L{e^{at}} = 1/(s-a), L{sin(at)} = a/(s^2+a^2).
    Shows the formula lookup and parameter substitution.

    Input format:
        ``compute laplace transform``

    Target format:
        ``L\\{t^3\\} <step> L\\{t^n\\} = \\frac{n!}{s^{n+1}} <step>
        n=3: \\frac{3!}{s^{4}} <step> \\frac{6}{s^{4}}``

    Difficulty scaling:
        Difficulty 1-3: power functions with small n.
        Difficulty 4-6: exponential functions with moderate a.
        Difficulty 7-8: sinusoidal functions with larger a.

    Prerequisites:
        integral.

    Example:
        >>> gen = LaplaceTransformGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'laplace_transform'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "laplace_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function type.

        Returns:
            Natural language description.
        """
        return "compute laplace transform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Laplace transform problem.

        Args:
            difficulty: Controls function type and parameter magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        entry = self._build_entry(difficulty)
        problem = f"L\\{{{entry.func_latex()}\\}}"
        return problem, {"entry": entry}

    def _build_entry(self, difficulty: int) -> LaplaceEntry:
        """Build a Laplace transform entry based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A LaplaceEntry instance.
        """
        entry_type = self._select_type(difficulty)
        if entry_type == "power":
            return self._power_entry(difficulty)
        if entry_type == "exp":
            return self._exp_entry(difficulty)
        return self._sin_entry(difficulty)

    def _select_type(self, difficulty: int) -> str:
        """Select the transform type based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Transform type string.
        """
        if difficulty <= 3:
            return "power"
        if difficulty <= 6:
            return self._rng.choice(["power", "exp"])
        return self._rng.choice(["power", "exp", "sin"])

    def _power_entry(self, difficulty: int) -> LaplaceEntry:
        """Build a power function Laplace entry.

        Args:
            difficulty: Controls exponent.

        Returns:
            LaplaceEntry for t^n.
        """
        n = self._rng.randint(1, min(5, 1 + difficulty))
        ns1 = n + 1
        return LaplaceEntry("power", {"n": n, "ns1": ns1})

    def _exp_entry(self, difficulty: int) -> LaplaceEntry:
        """Build an exponential function Laplace entry.

        Args:
            difficulty: Controls parameter a.

        Returns:
            LaplaceEntry for e^{at}.
        """
        a = self._rng.randint(-max(3, difficulty), max(3, difficulty))
        if a == 0:
            a = 1
        return LaplaceEntry("exp", {"a": a})

    def _sin_entry(self, difficulty: int) -> LaplaceEntry:
        """Build a sinusoidal function Laplace entry.

        Args:
            difficulty: Controls parameter a.

        Returns:
            LaplaceEntry for sin(at).
        """
        a = self._rng.randint(1, max(3, difficulty))
        asq = a * a
        return LaplaceEntry("sin", {"a": a, "asq": asq})

    def _create_steps(self, data: dict) -> list[str]:
        """Generate formula lookup and substitution steps.

        Args:
            data: Solution data with the Laplace entry.

        Returns:
            Steps showing formula and parameter substitution.
        """
        entry = data["entry"]
        return [
            entry.transform_formula(),
            f"substitution: {entry.result_latex()}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Laplace transform result.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the transform.
        """
        return data["entry"].result_latex()


@register
class SigmoidEvalGenerator(StepGenerator):
    """Evaluate the sigmoid function sigma(x) = 1/(1+e^{-x}).

    Generates integer or simple inputs, computes e^{-x}, the
    denominator 1+e^{-x}, and the final sigmoid value step by step.
    Uses pre-computed e^{-x} approximations for clean output.

    Input format:
        ``evaluate sigmoid function``

    Target format:
        ``\\sigma(2) = \\frac{1}{1+e^{-2}} <step> e^{-2}=0.1353
        <step> 1+0.1353=1.1353 <step> 1/1.1353=0.8808``

    Difficulty scaling:
        Difficulty 1-3: inputs in [-2, 2].
        Difficulty 4-6: inputs in [-5, 5].
        Difficulty 7-8: inputs in [-8, 8].

    Prerequisites:
        exponentiation, division.

    Example:
        >>> gen = SigmoidEvalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'sigmoid_eval'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "sigmoid_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls input magnitude.

        Returns:
            Natural language description.
        """
        return "evaluate sigmoid function"

    def _input_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to input range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_input, max_input).
        """
        if difficulty <= 3:
            return -2, 2
        if difficulty <= 6:
            return -5, 5
        return -8, 8

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sigmoid evaluation problem.

        Args:
            difficulty: Controls input magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._input_range(difficulty)
        x = self._rng.randint(lo, hi)
        exp_neg_x = round(math.exp(-x), 4)
        denom = round(1 + exp_neg_x, 4)
        sigmoid = round(1 / denom, 4)

        problem = f"\\sigma({x}) = \\frac{{1}}{{1+e^{{{-x}}}}}"
        return problem, {
            "x": x, "exp_neg_x": exp_neg_x,
            "denom": denom, "sigmoid": sigmoid,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step sigmoid computation.

        Args:
            data: Solution data with intermediate values.

        Returns:
            Steps showing e^{-x}, denominator, and final division.
        """
        x = data["x"]
        exp_val = data["exp_neg_x"]
        denom = data["denom"]
        return [
            f"e^{{{-x}}}={exp_val}",
            f"1+{exp_val}={denom}",
            f"1/{denom}={data['sigmoid']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the sigmoid value.

        Args:
            data: Solution data.

        Returns:
            String representation of the sigmoid.
        """
        return str(data["sigmoid"])


@register
class CrossEntropyGenerator(StepGenerator):
    """Compute cross-entropy loss H(p,q) = -sum(p_i * log(q_i)).

    Generates small probability distributions (2-4 classes) with
    simple fractions for clean logarithm values. Shows each term
    -p_i * log(q_i) and the final sum.

    Input format:
        ``compute cross entropy loss``

    Target format:
        ``H(p,q) = -\\sum p_i \\log q_i <step>
        -1 \\cdot \\log(0.5)=0.6931 <step>
        -0 \\cdot \\log(0.5)=0 <step> 0.6931``

    Difficulty scaling:
        Difficulty 1-3: 2 classes (binary cross-entropy).
        Difficulty 4-6: 3 classes.
        Difficulty 7-8: 4 classes.

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = CrossEntropyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'cross_entropy'
    """

    _Q_VALUES = [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "cross_entropy"

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
            difficulty: Controls number of classes.

        Returns:
            Natural language description.
        """
        return "compute cross entropy loss"

    def _num_classes(self, difficulty: int) -> int:
        """Map difficulty to number of distribution classes.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of classes (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate true and predicted distributions for cross-entropy.

        Args:
            difficulty: Controls number of classes.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_classes(difficulty)
        p = self._one_hot_distribution(n)
        q = self._predicted_distribution(n)
        terms = self._compute_terms(p, q)
        total = round(sum(terms), 4)

        p_str = ",".join(str(v) for v in p)
        q_str = ",".join(str(v) for v in q)
        problem = f"H(p,q) = -\\sum p_i \\log q_i, p=[{p_str}], q=[{q_str}]"
        return problem, {"p": p, "q": q, "terms": terms, "total": total}

    def _one_hot_distribution(self, n: int) -> list[float]:
        """Generate a one-hot true distribution.

        Args:
            n: Number of classes.

        Returns:
            One-hot probability vector.
        """
        p = [0.0] * n
        idx = self._rng.randint(0, n - 1)
        p[idx] = 1.0
        return p

    def _predicted_distribution(self, n: int) -> list[float]:
        """Generate a predicted distribution with simple values.

        Args:
            n: Number of classes.

        Returns:
            Probability vector summing to 1.0 (approximately).
        """
        raw = [self._rng.choice(self._Q_VALUES) for _ in range(n)]
        total = sum(raw)
        return [round(v / total, 4) for v in raw]

    def _compute_terms(self, p: list[float], q: list[float]) -> list[float]:
        """Compute each -p_i * log(q_i) term.

        Args:
            p: True distribution.
            q: Predicted distribution.

        Returns:
            List of per-class cross-entropy terms.
        """
        terms: list[float] = []
        for pi, qi in zip(p, q):
            if pi == 0.0:
                terms.append(0.0)
            else:
                terms.append(round(-pi * math.log(qi), 4))
        return terms

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-class cross-entropy term steps.

        Args:
            data: Solution data with p, q, and terms.

        Returns:
            Steps showing each -p_i * log(q_i).
        """
        p, q, terms = data["p"], data["q"], data["terms"]
        steps: list[str] = []

        for i, (pi, qi, ti) in enumerate(zip(p, q, terms)):
            steps.append(f"-{pi} \\cdot \\log({qi})={ti}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cross-entropy loss value.

        Args:
            data: Solution data.

        Returns:
            String representation of the total loss.
        """
        return str(data["total"])


@register
class InfoEntropyGenerator(StepGenerator):
    """Shannon entropy H(X) = -sum(p_i * log2(p_i)) in bits.

    Generates probability distributions using simple fractions
    (1/2, 1/4, 1/8, etc.) that yield clean base-2 logarithm values.
    Shows each term -p_i * log2(p_i) and the total in bits.

    Input format:
        ``compute information entropy``

    Target format:
        ``H(X) = -\\sum p_i \\log_2 p_i, p=[0.5, 0.25, 0.25]
        <step> -0.5 \\log_2(0.5)=0.5 <step>
        -0.25 \\log_2(0.25)=0.5 <step>
        -0.25 \\log_2(0.25)=0.5 <step> 1.5 bits``

    Difficulty scaling:
        Difficulty 1-3: 2 outcomes with power-of-2 fractions.
        Difficulty 4-6: 3-4 outcomes.
        Difficulty 7-8: 4-5 outcomes.

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = InfoEntropyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'info_entropy'
    """

    _CLEAN_PROBS = [
        Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "info_entropy"

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
            difficulty: Controls number of outcomes.

        Returns:
            Natural language description.
        """
        return "compute information entropy"

    def _num_outcomes(self, difficulty: int) -> int:
        """Map difficulty to number of distribution outcomes.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of outcomes (2-5).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return self._rng.randint(3, 4)
        return self._rng.randint(4, 5)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a probability distribution and compute its entropy.

        Args:
            difficulty: Controls number of outcomes.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_outcomes(difficulty)
        probs = self._build_distribution(n)
        terms = self._compute_terms(probs)
        total = sum(terms)

        prob_strs = [str(float(p)) for p in probs]
        problem = (
            f"H(X) = -\\sum p_i \\log_2 p_i, "
            f"p=[{', '.join(prob_strs)}]"
        )
        return problem, {"probs": probs, "terms": terms, "total": total}

    def _build_distribution(self, n: int) -> list[Fraction]:
        """Build a distribution of n outcomes summing to 1 using power-of-2 fractions.

        Args:
            n: Number of outcomes.

        Returns:
            List of Fraction probabilities summing to 1.
        """
        probs: list[Fraction] = []
        remaining = Fraction(1)

        for i in range(n - 1):
            candidates = [p for p in self._CLEAN_PROBS if p <= remaining - Fraction(1, 16) * (n - i - 1)]
            if not candidates:
                candidates = [remaining / (n - i)]
            prob = self._rng.choice(candidates)
            probs.append(prob)
            remaining -= prob

        probs.append(remaining)
        return probs

    def _compute_terms(self, probs: list[Fraction]) -> list[float]:
        """Compute each -p_i * log2(p_i) term.

        Args:
            probs: Probability values as Fractions.

        Returns:
            List of entropy contributions.
        """
        terms: list[float] = []
        for p in probs:
            p_float = float(p)
            if p_float > 0:
                terms.append(round(-p_float * math.log2(p_float), 4))
            else:
                terms.append(0.0)
        return terms

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-outcome entropy term steps.

        Args:
            data: Solution data with probabilities and terms.

        Returns:
            Steps showing each -p_i * log2(p_i).
        """
        probs, terms = data["probs"], data["terms"]
        steps: list[str] = []

        for p, t in zip(probs, terms):
            p_float = float(p)
            steps.append(f"-{p_float} \\log_2({p_float})={t}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total entropy in bits.

        Args:
            data: Solution data.

        Returns:
            String representation of entropy in bits.
        """
        return f"{round(data['total'], 4)} bits"


@register
class VigenereGenerator(StepGenerator):
    """Vigenere cipher decryption with rotating key.

    Generates an encrypted word and a repeating key, then shows
    per-character decryption by subtracting the key character's
    shift value modulo 26. The key rotates through its characters
    as each plaintext character is decrypted.

    Input format:
        ``decrypt vigenere cipher``

    Target format:
        ``LXFOP,KEY <step> L-K(10)=B <step> X-E(4)=T <step>
        F-Y(24)=G <step> O-K(10)=E <step> P-E(4)=L <step> BTGEL``

    Difficulty scaling:
        Difficulty 1-3: 4-6 character plaintext, 3 character key.
        Difficulty 4-6: 7-10 character plaintext, 4 character key.
        Difficulty 7-8: 11-15 character plaintext, 5 character key.

    Prerequisites:
        caesar.

    Example:
        >>> gen = VigenereGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'vigenere'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "vigenere"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["caesar"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls plaintext and key length.

        Returns:
            Natural language description.
        """
        return "decrypt vigenere cipher"

    def _plaintext_length(self, difficulty: int) -> int:
        """Map difficulty to plaintext character count.

        Args:
            difficulty: Difficulty level.

        Returns:
            Plaintext length.
        """
        if difficulty <= 3:
            return self._rng.randint(4, 6)
        if difficulty <= 6:
            return self._rng.randint(7, 10)
        return self._rng.randint(11, 15)

    def _key_length(self, difficulty: int) -> int:
        """Map difficulty to key length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Key length (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Vigenere cipher decryption problem.

        Args:
            difficulty: Controls plaintext and key lengths.

        Returns:
            Tuple of (ciphertext_with_key, solution_data).
        """
        pt_len = self._plaintext_length(difficulty)
        key_len = self._key_length(difficulty)
        plaintext = self._random_uppercase(pt_len)
        key = self._random_uppercase(key_len)
        ciphertext = self._encrypt(plaintext, key)

        problem = f"{ciphertext},{key}"
        return problem, {
            "plaintext": plaintext, "ciphertext": ciphertext, "key": key,
        }

    def _random_uppercase(self, length: int) -> str:
        """Generate a random uppercase string.

        Args:
            length: Number of characters.

        Returns:
            Random string of uppercase letters.
        """
        return "".join(chr(self._rng.randint(65, 90)) for _ in range(length))

    def _encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt plaintext using Vigenere cipher.

        Args:
            plaintext: Uppercase plaintext string.
            key: Uppercase key string.

        Returns:
            Encrypted uppercase string.
        """
        result: list[str] = []
        for i, ch in enumerate(plaintext):
            shift = ord(key[i % len(key)]) - 65
            encrypted = chr((ord(ch) - 65 + shift) % 26 + 65)
            result.append(encrypted)
        return "".join(result)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-character Vigenere decryption steps.

        Args:
            data: Solution data with ciphertext, key, and plaintext.

        Returns:
            Steps showing each character shift.
        """
        ct = data["ciphertext"]
        key = data["key"]
        pt = data["plaintext"]
        steps: list[str] = []

        for i in range(len(ct)):
            key_ch = key[i % len(key)]
            shift = ord(key_ch) - 65
            steps.append(f"{ct[i]}-{key_ch}({shift})={pt[i]}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decrypted plaintext.

        Args:
            data: Solution data.

        Returns:
            Decrypted uppercase string.
        """
        return data["plaintext"]
