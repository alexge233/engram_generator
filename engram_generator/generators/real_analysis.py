"""Real analysis generators.

12 generators at tiers 5-6 covering epsilon-delta proofs, Cauchy
sequences, convergence tests, supremum/infimum, uniform convergence,
power series, and the intermediate value theorem.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper classes
# ---------------------------------------------------------------------------


class LinearFunction:
    """Represents f(x) = m*x + b for epsilon-delta problems.

    Attributes:
        m: Slope coefficient.
        b: Intercept constant.
    """

    def __init__(self, m: int, b: int) -> None:
        """Initialise with slope and intercept.

        Args:
            m: Slope.
            b: Intercept.
        """
        self._m = m
        self._b = b

    @property
    def m(self) -> int:
        """Return the slope."""
        return self._m

    @property
    def b(self) -> int:
        """Return the intercept."""
        return self._b

    def eval_at(self, x: Fraction) -> Fraction:
        """Evaluate f(x) = m*x + b.

        Args:
            x: Input value.

        Returns:
            Function value as a Fraction.
        """
        return Fraction(self._m) * x + Fraction(self._b)

    def latex(self) -> str:
        """Format f(x) in LaTeX.

        Returns:
            LaTeX string for the function.
        """
        if self._b == 0:
            return f"{self._m}x"
        sign = "+" if self._b > 0 else "-"
        return f"{self._m}x{sign}{abs(self._b)}"


class QuadraticFunction:
    """Represents f(x) = a*x^2 + b*x + c for epsilon-delta problems.

    Attributes:
        a: Quadratic coefficient.
        b: Linear coefficient.
        c: Constant term.
    """

    def __init__(self, a: int, b: int, c: int) -> None:
        """Initialise with coefficients.

        Args:
            a: Quadratic coefficient.
            b: Linear coefficient.
            c: Constant term.
        """
        self._a = a
        self._b = b
        self._c = c

    @property
    def a(self) -> int:
        """Return the quadratic coefficient."""
        return self._a

    @property
    def b(self) -> int:
        """Return the linear coefficient."""
        return self._b

    @property
    def c(self) -> int:
        """Return the constant term."""
        return self._c

    def eval_at(self, x: Fraction) -> Fraction:
        """Evaluate f(x) = a*x^2 + b*x + c.

        Args:
            x: Input value.

        Returns:
            Function value as a Fraction.
        """
        return Fraction(self._a) * x * x + Fraction(self._b) * x + Fraction(self._c)

    def latex(self) -> str:
        """Format f(x) in LaTeX.

        Returns:
            LaTeX string for the function.
        """
        parts = []
        if self._a == 1:
            parts.append("x^{2}")
        elif self._a == -1:
            parts.append("-x^{2}")
        else:
            parts.append(f"{self._a}x^{{2}}")

        if self._b != 0:
            sign = "+" if self._b > 0 else "-"
            ab = abs(self._b)
            if ab == 1:
                parts.append(f"{sign}x")
            else:
                parts.append(f"{sign}{ab}x")

        if self._c != 0:
            sign = "+" if self._c > 0 else "-"
            parts.append(f"{sign}{abs(self._c)}")

        return "".join(parts)


class ContinuousPolynomial:
    """Represents a polynomial for intermediate value theorem problems.

    Stores coefficients from highest to lowest degree and provides
    evaluation at arbitrary Fraction inputs.

    Attributes:
        coeffs: Coefficients from highest to lowest degree.
    """

    def __init__(self, coeffs: list[int]) -> None:
        """Initialise with polynomial coefficients.

        Args:
            coeffs: Coefficients from highest to lowest degree.
        """
        self._coeffs = coeffs

    @property
    def degree(self) -> int:
        """Return the polynomial degree."""
        return len(self._coeffs) - 1

    def eval_at(self, x: Fraction) -> Fraction:
        """Evaluate the polynomial at x using Horner's method.

        Args:
            x: Input value.

        Returns:
            Polynomial value as a Fraction.
        """
        result = Fraction(0)
        for c in self._coeffs:
            result = result * x + Fraction(c)
        return result

    def latex(self) -> str:
        """Format the polynomial in LaTeX.

        Returns:
            LaTeX string for the polynomial.
        """
        deg = self.degree
        parts: list[str] = []
        for i, coeff in enumerate(self._coeffs):
            exp = deg - i
            if coeff == 0:
                continue
            is_first = len(parts) == 0
            if exp == 0:
                if is_first:
                    parts.append(str(coeff))
                else:
                    sign = "+" if coeff > 0 else "-"
                    parts.append(f"{sign}{abs(coeff)}")
            elif exp == 1:
                if is_first:
                    if coeff == 1:
                        parts.append("x")
                    elif coeff == -1:
                        parts.append("-x")
                    else:
                        parts.append(f"{coeff}x")
                else:
                    sign = "+" if coeff > 0 else "-"
                    ac = abs(coeff)
                    parts.append(f"{sign}{ac}x" if ac != 1 else f"{sign}x")
            else:
                if is_first:
                    if coeff == 1:
                        parts.append(f"x^{{{exp}}}")
                    elif coeff == -1:
                        parts.append(f"-x^{{{exp}}}")
                    else:
                        parts.append(f"{coeff}x^{{{exp}}}")
                else:
                    sign = "+" if coeff > 0 else "-"
                    ac = abs(coeff)
                    if ac == 1:
                        parts.append(f"{sign}x^{{{exp}}}")
                    else:
                        parts.append(f"{sign}{ac}x^{{{exp}}}")
        return "".join(parts) if parts else "0"


# ---------------------------------------------------------------------------
# 1. Epsilon-delta generator (tier 6)
# ---------------------------------------------------------------------------


@register
class EpsilonDeltaGenerator(StepGenerator):
    """Find delta for an epsilon-delta limit proof.

    Given f(x) and L = lim_{x->a} f(x), and epsilon > 0, find delta
    such that |f(x)-L| < epsilon whenever 0 < |x-a| < delta.
    Uses linear f(x) = mx+b and quadratic f(x) = x^2 near small a.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "epsilon_delta"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find delta for epsilon-delta proof"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an epsilon-delta problem.

        For linear f(x) = mx+b: |f(x)-L| = |m||x-a|, so delta = eps/|m|.
        For quadratic f(x) = x^2: |x^2-a^2| = |x+a||x-a|. Restrict
        delta <= 1 so |x+a| <= |a|+1, then delta = min(1, eps/(|a|+1)).

        Args:
            difficulty: Controls coefficient range and function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        use_quadratic = difficulty >= 5 and self._rng.random() < 0.5
        if use_quadratic:
            return self._quadratic_problem(difficulty)
        return self._linear_problem(difficulty)

    def _linear_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear epsilon-delta problem.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        m = self._rng.randint(1, 2 + difficulty)
        b = self._rng.randint(-5, 5)
        a = self._rng.randint(1, 3 + difficulty)
        f = LinearFunction(m, b)
        limit_val = f.eval_at(Fraction(a))
        eps_num = self._rng.randint(1, max(2, difficulty))
        eps = Fraction(eps_num, m)
        delta = eps / abs(m)

        problem = (
            f"|{f.latex()}-{limit_val}| < {eps} "
            f"when |x-{a}| < \\delta"
        )
        return problem, {
            "func_type": "linear", "m": m, "b": b, "a": a,
            "L": limit_val, "eps": eps, "delta": delta,
            "f_latex": f.latex(),
        }

    def _quadratic_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic epsilon-delta problem.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, min(4, difficulty))
        limit_val = Fraction(a * a)
        bound = abs(a) + 1
        eps_num = self._rng.randint(1, max(2, difficulty))
        eps = Fraction(eps_num)
        delta = min(Fraction(1), eps / bound)

        problem = (
            f"|x^{{2}}-{limit_val}| < {eps} "
            f"when |x-{a}| < \\delta"
        )
        return problem, {
            "func_type": "quadratic", "a": a,
            "L": limit_val, "eps": eps, "delta": delta,
            "bound": bound, "f_latex": "x^{2}",
        }

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            val: Fraction value.

        Returns:
            LaTeX string.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps for the epsilon-delta proof.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        if sd["func_type"] == "linear":
            m = sd["m"]
            return [
                f"|f(x)-L| = |{m}||x-{sd['a']}|",
                f"need |{m}||x-{sd['a']}| < {sd['eps']}",
                f"delta = eps/|{m}| = {self._format_fraction(sd['delta'])}",
            ]
        bound = sd["bound"]
        return [
            f"|x^2-{sd['L']}| = |x+{sd['a']}||x-{sd['a']}|",
            f"restrict delta<=1, |x+{sd['a']}|<={bound}",
            f"delta = min(1, eps/{bound}) = {self._format_fraction(sd['delta'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the delta value.

        Args:
            sd: Solution data dictionary.

        Returns:
            Delta as a string.
        """
        return self._format_fraction(sd["delta"])


# ---------------------------------------------------------------------------
# 2. Cauchy sequence (tier 6)
# ---------------------------------------------------------------------------


@register
class CauchySequenceGenerator(StepGenerator):
    """Check if a sequence is Cauchy.

    Given a_n = f(n), verify if |a_m - a_n| < epsilon for all m,n > N.
    Sequence types: 1/n, 1/n^2, (-1)^n/n.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cauchy_sequence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "check if sequence is Cauchy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Cauchy sequence verification problem.

        Args:
            difficulty: Controls sequence type and epsilon magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        seq_type = self._rng.choice(["1/n", "1/n^2", "(-1)^n/n"])
        eps_denom = self._rng.randint(2, 5 + difficulty * 2)
        eps = Fraction(1, eps_denom)

        if seq_type == "1/n":
            n_bound = int(math.ceil(2 / float(eps)))
            latex_an = "\\frac{1}{n}"
            bound_expr = f"|1/m - 1/n| <= 2/N < eps when N > {n_bound}"
        elif seq_type == "1/n^2":
            n_bound = int(math.ceil(math.sqrt(2 / float(eps))))
            latex_an = "\\frac{1}{n^{2}}"
            bound_expr = f"|1/m^2 - 1/n^2| <= 2/N^2 < eps when N > {n_bound}"
        else:
            n_bound = int(math.ceil(2 / float(eps)))
            latex_an = "\\frac{(-1)^{n}}{n}"
            bound_expr = f"|(-1)^m/m - (-1)^n/n| <= 2/N < eps when N > {n_bound}"

        problem = f"a_n = {latex_an}, \\epsilon = {self._format_fraction(eps)}"
        return problem, {
            "seq_type": seq_type, "eps": eps,
            "n_bound": n_bound, "latex_an": latex_an,
            "bound_expr": bound_expr, "is_cauchy": True,
        }

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            val: Fraction value.

        Returns:
            LaTeX string.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Cauchy sequence verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"a_n = {sd['latex_an']}",
            f"|a_m - a_n| bound: {sd['bound_expr']}",
            f"N = {sd['n_bound']} suffices",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the sequence is Cauchy with the N bound.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"yes, N={sd['n_bound']}"


# ---------------------------------------------------------------------------
# 3. Sequence convergence (tier 5)
# ---------------------------------------------------------------------------


@register
class SequenceConvergenceGenerator(StepGenerator):
    """Determine if a sequence converges and find its limit.

    Types: a_n = (n+a)/(n+b), a_n = c^n for |c|<1, a_n = n^(1/n).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sequence_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "determine sequence convergence and limit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequence convergence problem.

        Args:
            difficulty: Controls sequence type and parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        seq_type = self._rng.choice(["rational", "geometric", "nth_root"])
        if seq_type == "rational":
            return self._rational_seq(difficulty)
        if seq_type == "geometric":
            return self._geometric_seq(difficulty)
        return self._nth_root_seq(difficulty)

    def _rational_seq(self, difficulty: int) -> tuple[str, dict]:
        """Generate (n+a)/(n+b) convergence problem.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        while b == a:
            b = self._rng.randint(1, 3 + difficulty)
        limit_val = Fraction(1, 1)
        problem = f"a_n = \\frac{{n+{a}}}{{n+{b}}}"
        return problem, {
            "seq_type": "rational", "a": a, "b": b,
            "limit": limit_val, "converges": True,
        }

    def _geometric_seq(self, difficulty: int) -> tuple[str, dict]:
        """Generate c^n convergence problem with |c| < 1.

        Args:
            difficulty: Controls the ratio value.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        denom = self._rng.randint(2, 4 + difficulty)
        c = Fraction(1, denom)
        limit_val = Fraction(0)
        problem = f"a_n = \\left(\\frac{{1}}{{{denom}}}\\right)^{{n}}"
        return problem, {
            "seq_type": "geometric", "c": c, "denom": denom,
            "limit": limit_val, "converges": True,
        }

    def _nth_root_seq(self, difficulty: int) -> tuple[str, dict]:
        """Generate n^(1/n) convergence problem.

        Args:
            difficulty: Unused but required by interface.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        limit_val = Fraction(1)
        problem = "a_n = n^{1/n}"
        return problem, {
            "seq_type": "nth_root",
            "limit": limit_val, "converges": True,
        }

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as a string.

        Args:
            val: Fraction value.

        Returns:
            String representation.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate convergence analysis steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        if sd["seq_type"] == "rational":
            return [
                f"divide num/den by n",
                f"(1+{sd['a']}/n)/(1+{sd['b']}/n) -> 1/1 as n->inf",
            ]
        if sd["seq_type"] == "geometric":
            return [
                f"|1/{sd['denom']}| < 1",
                f"(1/{sd['denom']})^n -> 0 as n->inf",
            ]
        return [
            "ln(n^{1/n}) = ln(n)/n",
            "ln(n)/n -> 0 by L'Hopital",
            "n^{1/n} -> e^0 = 1",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the limit of the sequence.

        Args:
            sd: Solution data dictionary.

        Returns:
            Limit value as a string.
        """
        return f"converges to {self._format_fraction(sd['limit'])}"


# ---------------------------------------------------------------------------
# 4. Supremum and infimum (tier 5)
# ---------------------------------------------------------------------------


@register
class SupremumInfimumGenerator(StepGenerator):
    """Find the supremum and infimum of a set.

    Types: {1/n : n>=1}, {(-1)^n * (1-1/n)}, finite sets, intervals.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "supremum_infimum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find supremum and infimum of set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a supremum/infimum problem.

        Args:
            difficulty: Controls set type and complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            return self._finite_set(difficulty)
        if difficulty <= 4:
            return self._interval_set(difficulty)
        set_type = self._rng.choice(["1/n", "alternating"])
        if set_type == "1/n":
            return self._reciprocal_set(difficulty)
        return self._alternating_set(difficulty)

    def _finite_set(self, difficulty: int) -> tuple[str, dict]:
        """Generate a finite set sup/inf problem.

        Args:
            difficulty: Controls set size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        size = self._rng.randint(3, 5 + difficulty)
        elements = sorted(set(
            self._rng.randint(-10, 10) for _ in range(size * 2)
        ))[:size]
        if len(elements) < 2:
            elements = [-3, 0, 5]
        sup_val = Fraction(max(elements))
        inf_val = Fraction(min(elements))
        elems_str = ", ".join(str(e) for e in elements)
        problem = f"S = \\{{{elems_str}\\}}"
        return problem, {
            "set_type": "finite", "elements": elements,
            "sup": sup_val, "inf": inf_val,
        }

    def _interval_set(self, difficulty: int) -> tuple[str, dict]:
        """Generate an open interval sup/inf problem.

        Args:
            difficulty: Controls interval endpoints.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(-5, 3)
        b = a + self._rng.randint(1, 3 + difficulty)
        sup_val = Fraction(b)
        inf_val = Fraction(a)
        problem = f"S = ({a}, {b})"
        return problem, {
            "set_type": "interval", "a": a, "b": b,
            "sup": sup_val, "inf": inf_val,
        }

    def _reciprocal_set(self, difficulty: int) -> tuple[str, dict]:
        """Generate {1/n : n >= 1} sup/inf problem.

        Args:
            difficulty: Unused but required by interface.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        sup_val = Fraction(1)
        inf_val = Fraction(0)
        problem = "S = \\{1/n : n \\geq 1\\}"
        return problem, {
            "set_type": "1/n",
            "sup": sup_val, "inf": inf_val,
        }

    def _alternating_set(self, difficulty: int) -> tuple[str, dict]:
        """Generate {(-1)^n * (1-1/n)} sup/inf problem.

        Args:
            difficulty: Unused but required by interface.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        sup_val = Fraction(1)
        inf_val = Fraction(-1)
        problem = "S = \\{(-1)^{n}(1-1/n) : n \\geq 1\\}"
        return problem, {
            "set_type": "alternating",
            "sup": sup_val, "inf": inf_val,
        }

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as a string.

        Args:
            val: Fraction value.

        Returns:
            String representation.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate sup/inf solution steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        if sd["set_type"] == "finite":
            return [
                f"elements: {sd['elements']}",
                f"max = {self._format_fraction(sd['sup'])}",
                f"min = {self._format_fraction(sd['inf'])}",
            ]
        if sd["set_type"] == "interval":
            return [
                f"open interval ({sd['a']}, {sd['b']})",
                f"sup = {sd['b']} (not attained)",
                f"inf = {sd['a']} (not attained)",
            ]
        if sd["set_type"] == "1/n":
            return [
                "1/n decreasing, bounded below by 0",
                "sup = 1 (attained at n=1)",
                "inf = 0 (not attained)",
            ]
        return [
            "even n: (1-1/n) -> 1 from below",
            "odd n: -(1-1/n) -> -1 from above",
            "sup = 1, inf = -1",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return sup and inf values.

        Args:
            sd: Solution data dictionary.

        Returns:
            String with sup and inf.
        """
        return (
            f"sup={self._format_fraction(sd['sup'])}, "
            f"inf={self._format_fraction(sd['inf'])}"
        )


# ---------------------------------------------------------------------------
# 5. Uniform convergence (tier 6)
# ---------------------------------------------------------------------------


@register
class UniformConvergenceGenerator(StepGenerator):
    """Test if a function sequence converges uniformly.

    Tests f_n(x) = x^n on [0,1] or f_n(x) = x/n on bounded intervals.
    Computes sup|f_n(x) - f(x)| to determine uniform convergence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "uniform_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["epsilon_delta"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "test uniform convergence of function sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a uniform convergence problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        func_type = self._rng.choice(["x^n", "x/n"])
        if func_type == "x^n":
            return self._xn_problem(difficulty)
        return self._xn_div_problem(difficulty)

    def _xn_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate x^n on [0,1] uniform convergence problem.

        x^n -> 0 for x in [0,1), but x^n = 1 at x=1.
        Pointwise limit is discontinuous, so NOT uniformly convergent.
        sup|x^n - f(x)| = 1 at x approaching 1.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_val = self._rng.randint(2, 5 + difficulty)
        problem = f"f_n(x) = x^{{n}} on [0,1], n={n_val}"
        return problem, {
            "func_type": "x^n", "n": n_val,
            "uniform": False, "sup_diff": "1",
            "pointwise_limit": "0 for x in [0,1), 1 at x=1",
        }

    def _xn_div_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate x/n on [0,M] uniform convergence problem.

        f_n(x) = x/n -> 0 for all x. sup|x/n| on [0,M] = M/n -> 0.
        Uniformly convergent.

        Args:
            difficulty: Controls interval bound.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        bound = self._rng.randint(1, 3 + difficulty)
        n_val = self._rng.randint(2, 5 + difficulty)
        sup_val = round(bound / n_val, 4)
        problem = f"f_n(x) = x/n on [0,{bound}], n={n_val}"
        return problem, {
            "func_type": "x/n", "n": n_val, "bound": bound,
            "uniform": True, "sup_diff": str(sup_val),
            "pointwise_limit": "0",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate uniform convergence analysis steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        if sd["func_type"] == "x^n":
            return [
                f"pointwise: f(x) = {sd['pointwise_limit']}",
                "f is discontinuous at x=1",
                "sup|x^n - f(x)| does not -> 0",
                "not uniformly convergent",
            ]
        return [
            f"pointwise limit: f(x) = {sd['pointwise_limit']}",
            f"sup|x/{sd['n']}| on [0,{sd['bound']}] = {sd['bound']}/{sd['n']}",
            f"= {sd['sup_diff']} -> 0 as n->inf",
            "uniformly convergent",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether convergence is uniform.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        if sd["uniform"]:
            return f"uniform, sup={sd['sup_diff']}"
        return "not uniform"


# ---------------------------------------------------------------------------
# 6. Pointwise vs uniform (tier 6)
# ---------------------------------------------------------------------------


@register
class PointwiseVsUniformGenerator(StepGenerator):
    """Determine if convergence is pointwise-only or also uniform.

    Uses function sequences like f_n(x) = nx*e^{-nx} on [0,1],
    f_n(x) = x^n on [0,1], and f_n(x) = sin(x/n).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pointwise_vs_uniform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["uniform_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "classify convergence as pointwise or uniform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a pointwise vs uniform convergence problem.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        func_type = self._rng.choice(["x^n", "sin_x/n", "nx_exp"])
        if func_type == "x^n":
            return self._xn_problem()
        if func_type == "sin_x/n":
            return self._sin_problem()
        return self._nx_exp_problem()

    def _xn_problem(self) -> tuple[str, dict]:
        """Generate x^n on [0,1] classification problem.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "f_n(x) = x^{n} on [0,1]"
        return problem, {
            "func_type": "x^n", "is_uniform": False,
            "limit": "0 for x<1, 1 at x=1",
            "reason": "limit discontinuous",
        }

    def _sin_problem(self) -> tuple[str, dict]:
        """Generate sin(x/n) on [0, pi] classification problem.

        sin(x/n) -> 0, sup = sin(pi/n) -> 0. Uniform.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "f_n(x) = \\sin(x/n) on [0,\\pi]"
        return problem, {
            "func_type": "sin_x/n", "is_uniform": True,
            "limit": "0",
            "reason": "sup|sin(x/n)| <= pi/n -> 0",
        }

    def _nx_exp_problem(self) -> tuple[str, dict]:
        """Generate nx*e^{-nx} on [0,1] classification problem.

        Pointwise limit is 0 for all x in (0,1].
        But sup at x=1/n gives 1/e, so not uniform.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "f_n(x) = nxe^{-nx} on [0,1]"
        return problem, {
            "func_type": "nx_exp", "is_uniform": False,
            "limit": "0",
            "reason": "sup at x=1/n is 1/e != 0",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate classification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            f"pointwise limit: f(x) = {sd['limit']}",
            f"reason: {sd['reason']}",
        ]
        if sd["is_uniform"]:
            steps.append("convergence is uniform")
        else:
            steps.append("convergence is pointwise only")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the classification.

        Args:
            sd: Solution data dictionary.

        Returns:
            'uniform' or 'pointwise only'.
        """
        return "uniform" if sd["is_uniform"] else "pointwise only"


# ---------------------------------------------------------------------------
# 7. Ratio test (tier 6)
# ---------------------------------------------------------------------------


@register
class RatioTestGenerator(StepGenerator):
    """Apply the ratio test to determine series convergence.

    Computes lim |a_{n+1}/a_n|. Series types: n!/n^n, 2^n/n!, n^k/k^n.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ratio_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply ratio test for series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ratio test problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        series_type = self._rng.choice(["factorial_power", "exp_factorial", "poly_exp"])
        if series_type == "factorial_power":
            return self._factorial_power(difficulty)
        if series_type == "exp_factorial":
            return self._exp_factorial(difficulty)
        return self._poly_exp(difficulty)

    def _factorial_power(self, difficulty: int) -> tuple[str, dict]:
        """Generate n!/n^n ratio test problem.

        Ratio = (n/(n+1))^n -> 1/e < 1, converges.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\frac{n!}{n^{n}}"
        ratio_limit = round(1 / math.e, 4)
        return problem, {
            "series_type": "n!/n^n", "ratio_limit": ratio_limit,
            "converges": True,
            "ratio_expr": "(n/(n+1))^n -> 1/e",
        }

    def _exp_factorial(self, difficulty: int) -> tuple[str, dict]:
        """Generate k^n/n! ratio test problem.

        Ratio = k/(n+1) -> 0 < 1, converges.

        Args:
            difficulty: Controls base k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(2, 3 + difficulty)
        problem = f"\\sum \\frac{{{k}^{{n}}}}{{n!}}"
        return problem, {
            "series_type": "k^n/n!", "k": k,
            "ratio_limit": 0.0, "converges": True,
            "ratio_expr": f"{k}/(n+1) -> 0",
        }

    def _poly_exp(self, difficulty: int) -> tuple[str, dict]:
        """Generate n^k/k^n ratio test problem.

        Ratio = ((n+1)/n)^k * (1/k) -> 1/k. Converges if k >= 2.

        Args:
            difficulty: Controls exponent k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(2, 3 + difficulty)
        ratio_limit = round(1 / k, 4)
        problem = f"\\sum \\frac{{n^{{{k}}}}}{{{k}^{{n}}}}"
        return problem, {
            "series_type": "n^k/k^n", "k": k,
            "ratio_limit": ratio_limit, "converges": True,
            "ratio_expr": f"((n+1)/n)^{k} * 1/{k} -> 1/{k}",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate ratio test computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            "compute |a_{n+1}/a_n|",
            f"ratio = {sd['ratio_expr']}",
            f"L = {sd['ratio_limit']}",
        ]
        if sd["converges"]:
            steps.append("L < 1: converges")
        else:
            steps.append("L > 1: diverges")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return convergence result with ratio limit.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        verdict = "converges" if sd["converges"] else "diverges"
        return f"{verdict}, L={sd['ratio_limit']}"


# ---------------------------------------------------------------------------
# 8. Root test (tier 6)
# ---------------------------------------------------------------------------


@register
class RootTestGenerator(StepGenerator):
    """Apply the root test to determine series convergence.

    Computes lim |a_n|^{1/n}. Uses series like (k/(k+1))^n, (1/n)^n.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "root_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply root test for series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a root test problem.

        Args:
            difficulty: Controls series type and parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        series_type = self._rng.choice(["ratio_power", "inv_power", "mixed"])
        if series_type == "ratio_power":
            return self._ratio_power(difficulty)
        if series_type == "inv_power":
            return self._inv_power(difficulty)
        return self._mixed_power(difficulty)

    def _ratio_power(self, difficulty: int) -> tuple[str, dict]:
        """Generate (k/(k+m))^n root test problem.

        |a_n|^{1/n} = k/(k+m) < 1, converges.

        Args:
            difficulty: Controls k and m.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, 3 + difficulty)
        m = self._rng.randint(1, 2 + difficulty)
        root_limit = round(k / (k + m), 4)
        problem = (
            f"\\sum \\left(\\frac{{{k}}}{{{k + m}}}\\right)^{{n}}"
        )
        return problem, {
            "series_type": "ratio_power", "k": k, "m": m,
            "root_limit": root_limit, "converges": True,
            "root_expr": f"|a_n|^{{1/n}} = {k}/{k + m}",
        }

    def _inv_power(self, difficulty: int) -> tuple[str, dict]:
        """Generate (1/n)^n root test problem.

        |a_n|^{1/n} = 1/n -> 0 < 1, converges.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\left(\\frac{1}{n}\\right)^{n}"
        return problem, {
            "series_type": "inv_power",
            "root_limit": 0.0, "converges": True,
            "root_expr": "|a_n|^{1/n} = 1/n -> 0",
        }

    def _mixed_power(self, difficulty: int) -> tuple[str, dict]:
        """Generate (n/(n+1))^{n^2} root test problem.

        |a_n|^{1/n} = (n/(n+1))^n -> 1/e < 1, converges.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        root_limit = round(1 / math.e, 4)
        problem = "\\sum \\left(\\frac{n}{n+1}\\right)^{n^{2}}"
        return problem, {
            "series_type": "mixed",
            "root_limit": root_limit, "converges": True,
            "root_expr": "|a_n|^{1/n} = (n/(n+1))^n -> 1/e",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate root test computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            "compute limsup |a_n|^{1/n}",
            sd["root_expr"],
            f"L = {sd['root_limit']}",
        ]
        if sd["converges"]:
            steps.append("L < 1: converges")
        else:
            steps.append("L > 1: diverges")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return convergence result with root limit.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        verdict = "converges" if sd["converges"] else "diverges"
        return f"{verdict}, L={sd['root_limit']}"


# ---------------------------------------------------------------------------
# 9. Comparison test (tier 6)
# ---------------------------------------------------------------------------


@register
class ComparisonTestGenerator(StepGenerator):
    """Apply the direct comparison test for series convergence.

    Finds b_n such that a_n <= b_n and sum b_n converges (or a_n >= b_n
    and sum b_n diverges).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "comparison_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply comparison test for series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a comparison test problem.

        Args:
            difficulty: Controls series complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem_type = self._rng.choice(["converge_compare", "diverge_compare"])
        if problem_type == "converge_compare":
            return self._converge_compare(difficulty)
        return self._diverge_compare(difficulty)

    def _converge_compare(self, difficulty: int) -> tuple[str, dict]:
        """Generate a convergent comparison problem.

        1/(n^2+k) <= 1/n^2, and sum 1/n^2 converges.

        Args:
            difficulty: Controls k parameter.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, 3 + difficulty)
        problem = f"\\sum \\frac{{1}}{{n^{{2}}+{k}}}"
        return problem, {
            "type": "converge", "k": k,
            "a_n": f"1/(n^2+{k})",
            "b_n": "1/n^2",
            "b_converges": True,
            "inequality": f"1/(n^2+{k}) <= 1/n^2",
        }

    def _diverge_compare(self, difficulty: int) -> tuple[str, dict]:
        """Generate a divergent comparison problem.

        1/(n-k) >= 1/n for n > k, and sum 1/n diverges.

        Args:
            difficulty: Controls k parameter.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, min(3, difficulty))
        problem = f"\\sum_{{n>{k}}} \\frac{{1}}{{n-{k}}}"
        return problem, {
            "type": "diverge", "k": k,
            "a_n": f"1/(n-{k})",
            "b_n": "1/n",
            "b_converges": False,
            "inequality": f"1/(n-{k}) >= 1/n for n > {2 * k}",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate comparison test steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            f"a_n = {sd['a_n']}",
            f"compare with b_n = {sd['b_n']}",
            sd["inequality"],
        ]
        if sd["b_converges"]:
            steps.append(f"sum {sd['b_n']} converges (p-series, p=2)")
            steps.append("by comparison, sum a_n converges")
        else:
            steps.append(f"sum {sd['b_n']} diverges (harmonic)")
            steps.append("by comparison, sum a_n diverges")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return convergence/divergence verdict.

        Args:
            sd: Solution data dictionary.

        Returns:
            'converges' or 'diverges'.
        """
        return "converges" if sd["type"] == "converge" else "diverges"


# ---------------------------------------------------------------------------
# 10. Alternating series (tier 6)
# ---------------------------------------------------------------------------


@register
class AlternatingSeriesGenerator(StepGenerator):
    """Apply the Leibniz test for alternating series convergence.

    Checks that a_n is decreasing and a_n -> 0 for series
    sum (-1)^n * a_n.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "alternating_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply Leibniz test for alternating series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an alternating series Leibniz test problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        series_type = self._rng.choice(["1/n", "1/n^p", "1/ln_n"])
        if series_type == "1/n":
            return self._harmonic_alt(difficulty)
        if series_type == "1/n^p":
            return self._power_alt(difficulty)
        return self._log_alt(difficulty)

    def _harmonic_alt(self, difficulty: int) -> tuple[str, dict]:
        """Generate alternating harmonic series problem.

        sum (-1)^n / n: decreasing, -> 0, converges.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\frac{(-1)^{n}}{n}"
        return problem, {
            "series_type": "1/n", "a_n": "1/n",
            "decreasing": True, "limit_zero": True,
            "converges": True,
        }

    def _power_alt(self, difficulty: int) -> tuple[str, dict]:
        """Generate alternating p-series problem.

        sum (-1)^n / n^p with p > 0.

        Args:
            difficulty: Controls p value.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p_num = self._rng.randint(1, 2 + difficulty)
        p_den = self._rng.randint(1, max(1, p_num - 1)) if p_num > 1 else 1
        p = Fraction(p_num, p_den)
        p_str = str(p) if p.denominator == 1 else f"{p.numerator}/{p.denominator}"
        problem = f"\\sum \\frac{{(-1)^{{n}}}}{{n^{{{p_str}}}}}"
        converges = p > 0
        return problem, {
            "series_type": "1/n^p", "p": p_str,
            "a_n": f"1/n^{{{p_str}}}",
            "decreasing": True, "limit_zero": True,
            "converges": converges,
        }

    def _log_alt(self, difficulty: int) -> tuple[str, dict]:
        """Generate alternating 1/ln(n) series problem.

        sum (-1)^n / ln(n) for n >= 2: decreasing, -> 0, converges.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum_{n=2}^{\\infty} \\frac{(-1)^{n}}{\\ln(n)}"
        return problem, {
            "series_type": "1/ln_n", "a_n": "1/ln(n)",
            "decreasing": True, "limit_zero": True,
            "converges": True,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Leibniz test verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            f"a_n = {sd['a_n']}",
            f"a_n decreasing: {'yes' if sd['decreasing'] else 'no'}",
            f"a_n -> 0: {'yes' if sd['limit_zero'] else 'no'}",
        ]
        if sd["decreasing"] and sd["limit_zero"]:
            steps.append("Leibniz conditions met: converges")
        else:
            steps.append("Leibniz conditions not met")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return convergence verdict.

        Args:
            sd: Solution data dictionary.

        Returns:
            'converges' or 'diverges'.
        """
        return "converges" if sd["converges"] else "diverges"


# ---------------------------------------------------------------------------
# 11. Power series radius (tier 6)
# ---------------------------------------------------------------------------


@register
class PowerSeriesRadiusGenerator(StepGenerator):
    """Find the radius of convergence of a power series.

    Uses R = 1/lim|a_{n+1}/a_n| (ratio test) or
    R = 1/limsup|a_n|^{1/n} (root test).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_series_radius"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ratio_test"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find radius of convergence of power series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power series radius of convergence problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        series_type = self._rng.choice(["x^n/n!", "n*x^n", "x^n/n^p", "k^n*x^n"])
        if series_type == "x^n/n!":
            return self._exp_series(difficulty)
        if series_type == "n*x^n":
            return self._nx_series(difficulty)
        if series_type == "x^n/n^p":
            return self._np_series(difficulty)
        return self._kn_series(difficulty)

    def _exp_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate x^n/n! power series (R = infinity).

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\frac{x^{n}}{n!}"
        return problem, {
            "series_type": "x^n/n!",
            "radius": "inf",
            "method": "ratio",
            "ratio_expr": "|x|/(n+1) -> 0 < 1 for all x",
        }

    def _nx_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum n*x^n power series (R = 1).

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum n \\cdot x^{n}"
        return problem, {
            "series_type": "n*x^n",
            "radius": "1",
            "method": "ratio",
            "ratio_expr": "|a_{n+1}/a_n| = (n+1)/n * |x| -> |x|",
        }

    def _np_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum x^n/n^p power series (R = 1).

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(1, 2 + difficulty)
        problem = f"\\sum \\frac{{x^{{n}}}}{{n^{{{p}}}}}"
        return problem, {
            "series_type": "x^n/n^p", "p": p,
            "radius": "1",
            "method": "ratio",
            "ratio_expr": f"(n/(n+1))^{p} * |x| -> |x|",
        }

    def _kn_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum k^n * x^n power series (R = 1/k).

        Args:
            difficulty: Controls k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(2, 3 + difficulty)
        radius = Fraction(1, k)
        r_str = f"1/{k}"
        problem = f"\\sum {k}^{{n}} x^{{n}}"
        return problem, {
            "series_type": "k^n*x^n", "k": k,
            "radius": r_str,
            "method": "root",
            "ratio_expr": f"|a_n|^{{1/n}} = {k}|x|, converges when {k}|x| < 1",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate radius of convergence computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"method: {sd['method']} test",
            sd["ratio_expr"],
            f"R = {sd['radius']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the radius of convergence.

        Args:
            sd: Solution data dictionary.

        Returns:
            Radius as a string.
        """
        return f"R={sd['radius']}"


# ---------------------------------------------------------------------------
# 12. Intermediate value theorem (tier 6)
# ---------------------------------------------------------------------------


@register
class IntermediateValueGenerator(StepGenerator):
    """Apply the intermediate value theorem to show a root exists.

    Given f continuous on [a,b] with f(a)*f(b) < 0, shows a root exists
    in (a,b). Computes f at the midpoint to narrow the interval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "intermediate_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sequence_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply intermediate value theorem to find root"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an intermediate value theorem problem.

        Creates a polynomial with a known root and picks an interval
        [a,b] around it such that f(a)*f(b) < 0.

        Args:
            difficulty: Controls polynomial degree and coefficient range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        poly, a, b = self._build_polynomial(difficulty)
        fa = poly.eval_at(Fraction(a))
        fb = poly.eval_at(Fraction(b))

        mid = Fraction(a + b, 2)
        fmid = poly.eval_at(mid)

        if fmid == 0:
            new_a, new_b = a, b
            new_side = "exact root at midpoint"
        elif fa * fmid < 0:
            new_a, new_b = a, mid
            new_side = f"f({a})*f({mid}) < 0, root in ({a}, {mid})"
        else:
            new_a, new_b = mid, b
            new_side = f"f({mid})*f({b}) < 0, root in ({mid}, {b})"

        problem = f"f(x) = {poly.latex()}, [{a}, {b}]"
        return problem, {
            "poly": poly, "a": a, "b": b,
            "fa": fa, "fb": fb,
            "mid": mid, "fmid": fmid,
            "new_a": new_a, "new_b": new_b,
            "new_side": new_side,
        }

    def _build_polynomial(self, difficulty: int) -> tuple[ContinuousPolynomial, int, int]:
        """Build a polynomial guaranteed to have a sign change on [a,b].

        Constructs f(x) = x^2 - c for small difficulty or cubic for higher.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (polynomial, a, b).
        """
        if difficulty <= 4:
            return self._quadratic_ivt(difficulty)
        return self._cubic_ivt(difficulty)

    def _quadratic_ivt(self, difficulty: int) -> tuple[ContinuousPolynomial, int, int]:
        """Build x^2 - c with root between two integers.

        Args:
            difficulty: Controls c value.

        Returns:
            Tuple of (polynomial, a, b).
        """
        c = self._rng.randint(2, 5 + difficulty)
        root_approx = math.isqrt(c)
        a = root_approx
        b = root_approx + 1
        if a * a == c:
            c += 1
            b = a + 1
        poly = ContinuousPolynomial([1, 0, -c])
        fa = poly.eval_at(Fraction(a))
        fb = poly.eval_at(Fraction(b))
        if fa * fb >= 0:
            a = 0
            b = c
        return poly, a, b

    def _cubic_ivt(self, difficulty: int) -> tuple[ContinuousPolynomial, int, int]:
        """Build x^3 + px + q with sign change.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (polynomial, a, b).
        """
        p = self._rng.randint(-3, 3)
        q = self._rng.randint(-5, 5)
        poly = ContinuousPolynomial([1, 0, p, q])
        a, b = self._find_sign_change(poly, -10, 10)
        return poly, a, b

    def _find_sign_change(self, poly: ContinuousPolynomial,
                          lo: int, hi: int) -> tuple[int, int]:
        """Find integers a, b where f(a)*f(b) < 0.

        Args:
            poly: Polynomial to evaluate.
            lo: Lower search bound.
            hi: Upper search bound.

        Returns:
            Tuple of (a, b) with sign change.
        """
        for x in range(lo, hi):
            fx = poly.eval_at(Fraction(x))
            fx1 = poly.eval_at(Fraction(x + 1))
            if fx * fx1 < 0:
                return x, x + 1
        return 0, 2

    def _format_fraction(self, val: Fraction) -> str:
        """Format a Fraction as a string.

        Args:
            val: Fraction value.

        Returns:
            String representation.
        """
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate IVT application steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"f({sd['a']}) = {self._format_fraction(sd['fa'])}",
            f"f({sd['b']}) = {self._format_fraction(sd['fb'])}",
            f"f({sd['a']})*f({sd['b']}) < 0, IVT applies",
            f"midpoint: {self._format_fraction(sd['mid'])}",
            f"f({self._format_fraction(sd['mid'])}) = {self._format_fraction(sd['fmid'])}",
            sd["new_side"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the narrowed interval containing the root.

        Args:
            sd: Solution data dictionary.

        Returns:
            Interval string.
        """
        return (
            f"root in ({self._format_fraction(sd['new_a'])}, "
            f"{self._format_fraction(sd['new_b'])})"
        )
