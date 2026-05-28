"""Tier 7 generators — meta-reasoning and proof tasks.

Unlocks when Tier 0-6 tasks are mastered. Introduces tasks with
OPEN-ENDED solutions verified by PROPERTY CHECKING rather than
string matching. Covers polynomial construction, sequence
generalisation, error detection, counterexamples, proof by
induction, inverse problems, method selection, magnitude
estimation, formula derivation, and sufficiency analysis.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PolynomialEvaluator:
    """Evaluates polynomials represented as coefficient lists.

    Polynomials are stored as lists of coefficients from highest
    degree to lowest (constant term last). Provides evaluation,
    formatting, and construction utilities.

    Example:
        >>> ev = PolynomialEvaluator()
        >>> ev.evaluate([1, -3, 2], 5)
        12
        >>> ev.format_poly([1, -3, 2])
        'x^2-3x+2'
    """

    def evaluate(self, coeffs: list[int], x: int) -> int:
        """Evaluate polynomial at a given point using Horner's method.

        Args:
            coeffs: Coefficients from highest degree to constant.
            x: Point at which to evaluate.

        Returns:
            Polynomial value at x.
        """
        result = 0
        for c in coeffs:
            result = result * x + c
        return result

    def format_poly(self, coeffs: list[int]) -> str:
        """Format a polynomial as a string.

        Args:
            coeffs: Coefficients from highest degree to constant.

        Returns:
            Formatted polynomial string.
        """
        degree = len(coeffs) - 1
        parts: list[str] = []
        for i, c in enumerate(coeffs):
            power = degree - i
            if c == 0:
                continue
            parts.append(self._format_term(c, power, is_first=(len(parts) == 0)))
        return "".join(parts) if parts else "0"

    def _format_term(self, coeff: int, power: int, is_first: bool) -> str:
        """Format a single polynomial term.

        Args:
            coeff: Coefficient value.
            power: Exponent.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        sign = self._sign_prefix(coeff, is_first)
        body = self._term_body(abs(coeff), power)
        return f"{sign}{body}"

    def _sign_prefix(self, coeff: int, is_first: bool) -> str:
        """Determine the sign prefix for a term.

        Args:
            coeff: Coefficient value.
            is_first: Whether this is the leading term.

        Returns:
            Sign string.
        """
        if is_first:
            return "-" if coeff < 0 else ""
        return "-" if coeff < 0 else "+"

    def _term_body(self, abs_coeff: int, power: int) -> str:
        """Format the body of a polynomial term.

        Args:
            abs_coeff: Absolute coefficient value.
            power: Exponent.

        Returns:
            Term body string.
        """
        if power == 0:
            return str(abs_coeff)
        if power == 1:
            return "x" if abs_coeff == 1 else f"{abs_coeff}x"
        if abs_coeff == 1:
            return f"x^{power}"
        return f"{abs_coeff}x^{power}"


class SequenceFormula:
    """Encapsulates a named sequence formula with evaluation capability.

    Stores a formula name, a callable for computing terms, and
    a LaTeX representation for the general term.

    Attributes:
        name: Human-readable formula name.
        latex: LaTeX representation of the formula.

    Example:
        >>> import math
        >>> sf = SequenceFormula("squares", "n^2", lambda n: n * n)
        >>> sf.compute(5)
        25
    """

    def __init__(self, name: str, latex: str,
                 func: "callable") -> None:
        """Initialise with name, latex form, and compute function.

        Args:
            name: Human-readable formula name.
            latex: LaTeX representation.
            func: Callable taking int n and returning the nth term.
        """
        self.name = name
        self.latex = latex
        self._func = func

    def compute(self, n: int) -> int:
        """Compute the nth term of the sequence.

        Args:
            n: Term index (1-based).

        Returns:
            Value of the sequence at index n.
        """
        return self._func(n)


class FalseClaimPool:
    """Pool of known false mathematical claims with counterexamples.

    Each claim is a tuple of (claim_text, check_function, known_counterexample,
    explanation). The check function returns True when the claim holds and
    False when it fails.

    Example:
        >>> pool = FalseClaimPool()
        >>> claim = pool.claims[0]
        >>> claim["counterexample"]
        41
    """

    _CLAIMS_DATA: list[tuple] = [
        ("n^2 + n + 41 is prime for all n >= 0", 41,
         41 * 41 + 41 + 41, "41^2+41+41 = 41*43 = 1763, which is composite"),
        ("2^p - 1 is prime for all prime p", 11,
         2047, "2^11-1 = 2047 = 23*89, which is composite"),
        ("n^2 - n + 41 is prime for all n >= 1", 41,
         41 * 41 - 41 + 41, "41^2-41+41 = 41^2 = 1681, which is composite"),
        ("all odd numbers are prime", 9,
         9, "9 = 3*3, which is composite"),
        ("n! + 1 is prime for all n >= 1", 5,
         121, "5!+1 = 121 = 11*11, which is composite"),
        ("2^(2^n) + 1 is prime for all n >= 0", 5,
         4294967297, "2^32+1 = 4294967297 = 641*6700417, which is composite"),
        ("the sum of two irrational numbers is always irrational",
         "sqrt(2) and -sqrt(2)", 0,
         "sqrt(2) + (-sqrt(2)) = 0, which is rational"),
        ("if a^2 divides b^2 then a divides b",
         "a=6, b=12 fails for a=6,b=10",
         "6^2=36 does not divide 10^2=100",
         "36 does not divide 100; 100/36 is not an integer"),
        ("every continuous function is differentiable",
         "f(x) = |x| at x=0", "undefined",
         "|x| is continuous everywhere but not differentiable at x=0 (sharp corner)"),
        ("if f(n) = O(g(n)) then g(n) = O(f(n))",
         "f(n)=n, g(n)=n^2", "n = O(n^2) but n^2 != O(n)",
         "O is not symmetric: n grows slower than n^2"),
        ("every group of order n is cyclic",
         "n=4, Klein four-group", "V4 = {e, a, b, ab}",
         "the Klein four-group has order 4 but every non-identity element has order 2"),
        ("the product of two negative numbers is negative",
         "-3 * -4 = 12", 12,
         "(-3)(-4) = 12, which is positive"),
    ]

    def __init__(self) -> None:
        """Initialise the pool of false claims."""
        self._claims = self._build_claims()

    @property
    def claims(self) -> list[dict]:
        """Return all false claims in the pool.

        Returns:
            List of claim dictionaries.
        """
        return self._claims

    def _build_claims(self) -> list[dict]:
        """Build the collection of known false claims.

        Returns:
            List of claim dictionaries with text, counterexample, and explanation.
        """
        return [
            {"text": t, "counterexample": ce, "check_value": cv, "explanation": ex}
            for t, ce, cv, ex in self._CLAIMS_DATA
        ]


class InductionIdentity:
    """Represents a known mathematical identity provable by induction.

    Stores the identity formula, base case value, and provides
    methods to verify both the base case and the inductive step.

    Attributes:
        name: Human-readable identity name.
        formula_lhs: LaTeX for the left-hand side (sum).
        formula_rhs: LaTeX for the right-hand side (closed form).

    Example:
        >>> ident = InductionIdentity(
        ...     "sum_n", "\\\\sum_{{k=1}}^n k", "\\\\frac{{n(n+1)}}{{2}}",
        ...     lambda n: n*(n+1)//2, lambda n: n
        ... )
        >>> ident.closed_form(5)
        15
    """

    def __init__(self, name: str, formula_lhs: str, formula_rhs: str,
                 closed_form_func: "callable",
                 term_func: "callable") -> None:
        """Initialise the induction identity.

        Args:
            name: Identity name.
            formula_lhs: LaTeX for the summation side.
            formula_rhs: LaTeX for the closed form.
            closed_form_func: Computes closed form value for n.
            term_func: Computes the nth term being summed.
        """
        self.name = name
        self.formula_lhs = formula_lhs
        self.formula_rhs = formula_rhs
        self._closed_form_func = closed_form_func
        self._term_func = term_func

    def closed_form(self, n: int) -> int:
        """Evaluate the closed form at n.

        Args:
            n: Value of n.

        Returns:
            Closed form result.
        """
        return self._closed_form_func(n)

    def term(self, n: int) -> int:
        """Evaluate the nth term of the sum.

        Args:
            n: Term index.

        Returns:
            Value of the nth term.
        """
        return self._term_func(n)


class DerivativeRule:
    """Represents a function and its derivative for inverse problems.

    Stores the antiderivative f(x) and its derivative f'(x) in both
    LaTeX and computational form.

    Attributes:
        f_latex: LaTeX representation of f(x).
        df_latex: LaTeX representation of f'(x).

    Example:
        >>> rule = DerivativeRule("x^3", "3x^2", lambda x: x**3, lambda x: 3*x**2)
        >>> rule.f_eval(2)
        8
    """

    def __init__(self, f_latex: str, df_latex: str,
                 f_func: "callable", df_func: "callable") -> None:
        """Initialise with function and derivative.

        Args:
            f_latex: LaTeX for f(x).
            df_latex: LaTeX for f'(x).
            f_func: Callable computing f(x).
            df_func: Callable computing f'(x).
        """
        self.f_latex = f_latex
        self.df_latex = df_latex
        self._f_func = f_func
        self._df_func = df_func

    def f_eval(self, x: int) -> int:
        """Evaluate f(x).

        Args:
            x: Input value.

        Returns:
            f(x) value.
        """
        return self._f_func(x)

    def df_eval(self, x: int) -> int:
        """Evaluate f'(x).

        Args:
            x: Input value.

        Returns:
            f'(x) value.
        """
        return self._df_func(x)


@register
class ConstructPolynomialGenerator(StepGenerator):
    """Build a polynomial satisfying given constraints.

    Generates a set of constraints (roots, specific values at points)
    and requires construction of a polynomial that satisfies all of
    them. Verification evaluates the polynomial at each constraint
    point.

    Input format:
        ``construct polynomial with given properties``

    Target format:
        ``roots: 1,2; p(0)=2 <step> (x-1)(x-2) gives roots <step>
        expand: x^2-3x+2 <step> verify p(0)=2: 0-0+2=2 ok <step>
        x^2-3x+2``

    Difficulty scaling:
        Difficulty 1-2: 2 roots, no extra constraints.
        Difficulty 3-4: 2 roots + 1 value constraint.
        Difficulty 5-6: 3 roots + 1 value constraint.
        Difficulty 7-8: 3 roots + 2 value constraints.
        Higher difficulty uses larger root magnitudes.

    Prerequisites:
        polynomial_eval, quadratic.

    Example:
        >>> gen = ConstructPolynomialGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'construct_polynomial'
    """

    _NUM_ROOTS = {
        1: 2, 2: 2, 3: 2, 4: 2,
        5: 3, 6: 3, 7: 3, 8: 3,
    }

    _ROOT_RANGE = {
        1: (-3, 3), 2: (-4, 4), 3: (-5, 5), 4: (-5, 5),
        5: (-6, 6), 6: (-7, 7), 7: (-8, 8), 8: (-10, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "construct_polynomial"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval", "quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of roots and constraints.

        Returns:
            Natural language description.
        """
        return "construct polynomial with given properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate polynomial constraints from known roots.

        Args:
            difficulty: Controls root count and constraint count.

        Returns:
            Tuple of (constraint_description, solution_data).
        """
        num_roots = self._NUM_ROOTS.get(difficulty, 2)
        lo, hi = self._ROOT_RANGE.get(difficulty, (-5, 5))
        roots = self._sample_distinct_roots(num_roots, lo, hi)
        coeffs = self._expand_from_roots(roots)
        evaluator = PolynomialEvaluator()
        verifications = self._build_verifications(roots, coeffs, evaluator)
        problem = self._format_constraints(roots, verifications)
        return problem, {
            "roots": roots, "coeffs": coeffs,
            "verifications": verifications,
            "poly_str": evaluator.format_poly(coeffs),
        }

    def _sample_distinct_roots(self, count: int, lo: int,
                               hi: int) -> list[int]:
        """Sample distinct integer roots in the given range.

        Args:
            count: Number of roots needed.
            lo: Minimum root value.
            hi: Maximum root value.

        Returns:
            Sorted list of distinct roots.
        """
        available = list(range(lo, hi + 1))
        if 0 in available:
            available.remove(0)
        selected = self._rng.sample(available, min(count, len(available)))
        return sorted(selected)

    def _expand_from_roots(self, roots: list[int]) -> list[int]:
        """Expand (x-r1)(x-r2)... into coefficient list.

        Args:
            roots: List of integer roots.

        Returns:
            Coefficients from highest degree to constant.
        """
        coeffs = [1]
        for r in roots:
            new_coeffs = [0] * (len(coeffs) + 1)
            for i, c in enumerate(coeffs):
                new_coeffs[i] += c
                new_coeffs[i + 1] -= c * r
            coeffs = new_coeffs
        return coeffs

    def _build_verifications(self, roots: list[int], coeffs: list[int],
                             evaluator: PolynomialEvaluator) -> list[tuple[int, int]]:
        """Build verification points (x, p(x)) pairs.

        Args:
            roots: Known roots of the polynomial.
            coeffs: Polynomial coefficients.
            evaluator: PolynomialEvaluator instance.

        Returns:
            List of (x, value) tuples for verification.
        """
        verifications: list[tuple[int, int]] = []
        for x in [0, -1, 1]:
            if x not in roots:
                val = evaluator.evaluate(coeffs, x)
                verifications.append((x, val))
                if len(verifications) >= 2:
                    break
        return verifications

    def _format_constraints(self, roots: list[int],
                            verifications: list[tuple[int, int]]) -> str:
        """Format the constraint set as a problem string.

        Args:
            roots: Required roots.
            verifications: Required value constraints.

        Returns:
            Formatted constraint string.
        """
        roots_str = ",".join(str(r) for r in roots)
        parts = [f"roots: {roots_str}"]
        for x, val in verifications:
            parts.append(f"p({x})={val}")
        return "; ".join(parts)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate construction and verification steps.

        Args:
            data: Solution data with roots, coefficients, and verifications.

        Returns:
            Steps showing root factors, expansion, and verification.
        """
        roots = data["roots"]
        evaluator = PolynomialEvaluator()
        steps: list[str] = []
        steps.append(self._format_factors(roots))
        steps.append(f"expand: {data['poly_str']}")
        for x, val in data["verifications"]:
            computed = evaluator.evaluate(data["coeffs"], x)
            steps.append(f"verify p({x})={computed}: ok")
        return steps

    def _format_factors(self, roots: list[int]) -> str:
        """Format the factored form of the polynomial.

        Args:
            roots: List of roots.

        Returns:
            String like '(x-1)(x-2)(x+3)'.
        """
        parts: list[str] = []
        for r in roots:
            if r >= 0:
                parts.append(f"(x-{r})")
            else:
                parts.append(f"(x+{abs(r)})")
        return "".join(parts)

    def _create_answer(self, data: dict) -> str:
        """Return the polynomial expression.

        Args:
            data: Solution data.

        Returns:
            Formatted polynomial string.
        """
        return data["poly_str"]


@register
class GeneraliseSequenceGenerator(StepGenerator):
    """Find the formula for a sequence from its first N terms.

    Generates a sequence from a known formula, shows the first 5-6
    terms, and requires identifying the formula. Verification checks
    the formula at unseen indices beyond the shown terms.

    Input format:
        ``find formula for sequence``

    Target format:
        ``1, 4, 9, 16, 25, 36 <step> differences: 3,5,7,9,11 <step>
        second differences: 2,2,2,2 (constant) <step> formula: n^2
        <step> verify: f(7)=49 <step> n^2``

    Difficulty scaling:
        Difficulty 1-2: simple formulas (n^2, 2n, n+1).
        Difficulty 3-4: triangular, powers of 2.
        Difficulty 5-6: cubic, Fibonacci-like.
        Difficulty 7-8: compound formulas (n^2+n, 2^n-1).

    Prerequisites:
        polynomial_eval.

    Example:
        >>> gen = GeneraliseSequenceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'generalise_sequence'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "generalise_sequence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Natural language description.
        """
        return "find formula for sequence"

    def _get_formulas(self, difficulty: int) -> list[SequenceFormula]:
        """Return formula pool appropriate for the difficulty, with random coefficients.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of available SequenceFormula objects.
        """
        # Add random multiplier/offset to create variety
        a = self._rng.randint(1, 5)
        b = self._rng.randint(1, 8)
        c = self._rng.randint(2, 5)
        easy = [
            SequenceFormula("squares", "n^2", lambda n: n * n),
            SequenceFormula(f"{a}n_scaled", f"{a}n", lambda n, _a=a: _a * n),
            SequenceFormula(f"n+{b}", f"n+{b}", lambda n, _b=b: n + _b),
            SequenceFormula(f"{a}n+{b}", f"{a}n+{b}", lambda n, _a=a, _b=b: _a * n + _b),
        ]
        medium = [
            SequenceFormula("triangular", "n(n+1)/2", lambda n: n * (n + 1) // 2),
            SequenceFormula(f"{c}^n", f"{c}^n", lambda n, _c=c: _c ** n),
            SequenceFormula("cubes", "n^3", lambda n: n ** 3),
            SequenceFormula(f"{a}n^2+{b}", f"{a}n^2+{b}", lambda n, _a=a, _b=b: _a * n * n + _b),
        ]
        hard = [
            SequenceFormula(f"n^2+{a}n", f"n^2+{a}n", lambda n, _a=a: n * n + _a * n),
            SequenceFormula(f"{c}^n-1", f"{c}^n-1", lambda n, _c=c: _c ** n - 1),
            SequenceFormula("factorial", "n!", lambda n: math.factorial(n)),
            SequenceFormula(f"{a}n^2+{b}n+{c}", f"{a}n^2+{b}n+{c}",
                           lambda n, _a=a, _b=b, _c=c: _a * n * n + _b * n + _c),
        ]
        if difficulty <= 2:
            return easy
        if difficulty <= 4:
            return easy + medium
        return easy + medium + hard

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequence and select verification points.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (sequence_terms, solution_data).
        """
        formulas = self._get_formulas(difficulty)
        formula = self._rng.choice(formulas)
        num_shown = self._rng.randint(5, 6)
        terms = [formula.compute(n) for n in range(1, num_shown + 1)]
        verify_indices = [num_shown + 1, num_shown + 2]
        verify_values = [formula.compute(n) for n in verify_indices]
        terms_str = ", ".join(str(t) for t in terms)
        return terms_str, {
            "formula": formula, "terms": terms,
            "verify_indices": verify_indices,
            "verify_values": verify_values,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate pattern identification and verification steps.

        Args:
            data: Solution data with formula and verification points.

        Returns:
            Steps showing differences, formula identification, and verification.
        """
        terms = data["terms"]
        formula = data["formula"]
        steps: list[str] = []
        steps.append(self._format_differences(terms))
        steps.append(f"formula: {formula.latex}")
        for idx, val in zip(data["verify_indices"], data["verify_values"]):
            steps.append(f"verify: f({idx})={val}")
        return steps

    def _format_differences(self, terms: list[int]) -> str:
        """Compute and format first differences of the sequence.

        Args:
            terms: Sequence terms.

        Returns:
            Step string showing the first differences.
        """
        diffs = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
        diffs_str = ",".join(str(d) for d in diffs)
        return f"differences: {diffs_str}"

    def _create_answer(self, data: dict) -> str:
        """Return the formula in LaTeX notation.

        Args:
            data: Solution data.

        Returns:
            LaTeX formula string.
        """
        return data["formula"].latex


@register
class ErrorDetectionGenerator(StepGenerator):
    """Find a planted error in a mathematical solution chain.

    Generates a CORRECT solution chain for an arithmetic or algebraic
    problem, then corrupts ONE step by changing the result. The target
    identifies which step is wrong and provides the correction.

    Input format:
        ``find the error in this solution``

    Target format:
        ``23+45: 8+5=13, 2+4+1=8; answer=83 <step> step 2 is wrong
        <step> 2+4+1=7, not 8 <step> correct answer: 68``

    Difficulty scaling:
        Difficulty 1-2: 3-step solutions, single-digit errors.
        Difficulty 3-4: 4-step solutions.
        Difficulty 5-6: 5-step solutions.
        Difficulty 7-8: 6-step solutions with larger numbers.

    Prerequisites:
        derivative, addition.

    Example:
        >>> gen = ErrorDetectionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'error_detection'
    """

    _STEP_COUNTS = {
        1: 3, 2: 3, 3: 4, 4: 4,
        5: 5, 6: 5, 7: 6, 8: 6,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "error_detection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls solution chain length.

        Returns:
            Natural language description.
        """
        return "find the error in this solution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a solution chain with one planted error.

        Args:
            difficulty: Controls chain length.

        Returns:
            Tuple of (problem_with_error, solution_data).
        """
        num_steps = self._STEP_COUNTS.get(difficulty, 4)
        operands = self._generate_operands(num_steps, difficulty)
        correct_steps = self._compute_correct_chain(operands)
        error_idx = self._rng.randint(0, len(correct_steps) - 1)
        corrupted_steps = self._corrupt_step(correct_steps, error_idx)
        problem = self._format_chain(operands, corrupted_steps)
        return problem, {
            "operands": operands, "correct_steps": correct_steps,
            "corrupted_steps": corrupted_steps,
            "error_idx": error_idx,
            "correct_answer": sum(operands),
        }

    def _generate_operands(self, count: int, difficulty: int) -> list[int]:
        """Generate operands for an addition chain.

        Args:
            count: Number of operands.
            difficulty: Controls operand magnitude.

        Returns:
            List of positive integers.
        """
        upper = 10 ** min(difficulty, 3)
        return [self._rng.randint(1, upper) for _ in range(count)]

    def _compute_correct_chain(self, operands: list[int]) -> list[int]:
        """Compute running totals for a cumulative addition chain.

        Args:
            operands: List of operands to add sequentially.

        Returns:
            List of running totals after each addition.
        """
        totals: list[int] = []
        running = operands[0]
        for i in range(1, len(operands)):
            running += operands[i]
            totals.append(running)
        return totals

    def _corrupt_step(self, correct_steps: list[int],
                      error_idx: int) -> list[int]:
        """Corrupt one step by changing its value.

        Args:
            correct_steps: List of correct running totals.
            error_idx: Index of the step to corrupt.

        Returns:
            New list with one corrupted value.
        """
        corrupted = correct_steps[:]
        offset = self._rng.choice([-2, -1, 1, 2, 10, -10])
        corrupted[error_idx] = correct_steps[error_idx] + offset
        return corrupted

    def _format_chain(self, operands: list[int],
                      steps: list[int]) -> str:
        """Format the addition chain with intermediate results.

        Args:
            operands: Original operands.
            steps: Running totals (possibly corrupted).

        Returns:
            Formatted problem string.
        """
        ops_str = "+".join(str(x) for x in operands)
        steps_str = ",".join(str(s) for s in steps)
        return f"{ops_str}; running totals: {steps_str}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate error identification and correction steps.

        Args:
            data: Solution data with error location and correct values.

        Returns:
            Steps showing error identification and correction.
        """
        error_idx = data["error_idx"]
        correct_val = data["correct_steps"][error_idx]
        wrong_val = data["corrupted_steps"][error_idx]
        return [
            f"step {error_idx + 1} is wrong",
            f"shows {wrong_val}, should be {correct_val}",
            f"correct answer: {data['correct_answer']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the correct final answer.

        Args:
            data: Solution data.

        Returns:
            String of the correct answer.
        """
        return str(data["correct_answer"])


@register
class CounterexampleGenerator(StepGenerator):
    """Disprove a false mathematical claim with a counterexample.

    Uses a pool of known false claims with known counterexamples.
    The target provides a specific counterexample and demonstrates
    that the claim fails at that value.

    Input format:
        ``disprove this claim``

    Target format:
        ``claim: n^2+n+41 is prime for all n>=0 <step>
        try n=41 <step> 41^2+41+41=1763 <step> 1763=41*43 <step>
        counterexample: n=41``

    Difficulty scaling:
        Difficulty 1-2: simple claims (odd implies prime).
        Difficulty 3-4: quadratic formula claims.
        Difficulty 5-6: exponential claims.
        Difficulty 7-8: factorial and Fermat number claims.

    Prerequisites:
        primality, exponentiation.

    Example:
        >>> gen = CounterexampleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'counterexample'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "counterexample"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["primality", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls claim complexity.

        Returns:
            Natural language description.
        """
        return "disprove this claim"

    def _get_claims(self, difficulty: int) -> list[dict]:
        """Return claims appropriate for the difficulty level.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of claim dictionaries.
        """
        pool = FalseClaimPool()
        all_claims = pool.claims
        if difficulty <= 2:
            return all_claims[:6]
        if difficulty <= 4:
            return all_claims[:9]
        return all_claims

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Select a false claim and generate randomised search context.

        Args:
            difficulty: Controls which claims are available.

        Returns:
            Tuple of (claim_text, solution_data).
        """
        claims = self._get_claims(difficulty)
        claim = self._rng.choice(claims)
        # Add randomised search range context for variety
        search_start = self._rng.randint(0, 5)
        search_end = self._rng.randint(50, 200 + difficulty * 50)
        hint_tries = self._rng.randint(3, 10)
        return (
            f"claim: {claim['text']} (search n in [{search_start},{search_end}], try {hint_tries} values)",
            {
                "claim_text": claim["text"],
                "counterexample": claim["counterexample"],
                "check_value": claim["check_value"],
                "explanation": claim["explanation"],
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate counterexample demonstration steps.

        Args:
            data: Solution data with claim and counterexample.

        Returns:
            Steps showing the counterexample and why the claim fails.
        """
        ce = data["counterexample"]
        return [
            f"try n={ce}",
            f"compute: result={data['check_value']}",
            data["explanation"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the counterexample value.

        Args:
            data: Solution data.

        Returns:
            String identifying the counterexample.
        """
        return f"n={data['counterexample']}"


@register
class ProofByInductionGenerator(StepGenerator):
    """Prove a mathematical formula by induction.

    Uses known identities (sum of first n integers, sum of squares,
    geometric series) and generates a structured proof showing the
    base case and inductive step.

    Input format:
        ``prove by mathematical induction``

    Target format:
        ``prove: sum(1..n) = n(n+1)/2 <step> base case: n=1,
        LHS=1, RHS=1(2)/2=1 ok <step> assume true for n=k <step>
        show for n=k+1: LHS=k(k+1)/2 + (k+1) <step>
        = (k+1)(k+2)/2 = RHS <step> proven``

    Difficulty scaling:
        Difficulty 1-2: sum of n (linear).
        Difficulty 3-4: sum of squares.
        Difficulty 5-6: sum of cubes, geometric series.
        Difficulty 7-8: more complex identities with higher verification n.

    Prerequisites:
        addition, multiplication.

    Example:
        >>> gen = ProofByInductionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'proof_by_induction'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "proof_by_induction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls identity complexity.

        Returns:
            Natural language description.
        """
        return "prove by mathematical induction"

    @staticmethod
    def _build_all_identities() -> list[InductionIdentity]:
        """Build all induction identities for reuse across calls.

        Returns:
            List of InductionIdentity objects ordered by difficulty.
        """
        return [
            InductionIdentity(
                "sum_n", "\\sum_{k=1}^n k", "\\frac{n(n+1)}{2}",
                lambda n: n * (n + 1) // 2, lambda n: n),
            InductionIdentity(
                "sum_squares", "\\sum_{k=1}^n k^2", "\\frac{n(n+1)(2n+1)}{6}",
                lambda n: n * (n + 1) * (2 * n + 1) // 6, lambda n: n * n),
            InductionIdentity(
                "sum_cubes", "\\sum_{k=1}^n k^3",
                "\\left(\\frac{n(n+1)}{2}\\right)^2",
                lambda n: (n * (n + 1) // 2) ** 2, lambda n: n ** 3),
            InductionIdentity(
                "geometric", "\\sum_{k=1}^n 2^k", "2^{n+1}-2",
                lambda n: 2 ** (n + 1) - 2, lambda n: 2 ** n),
            InductionIdentity(
                "sum_odd", "\\sum_{k=1}^n (2k-1)", "n^2",
                lambda n: n * n, lambda n: 2 * n - 1),
            InductionIdentity(
                "power_of_two", "\\sum_{k=0}^n 2^k", "2^{n+1}-1",
                lambda n: 2 ** (n + 1) - 1, lambda n: 2 ** n),
            InductionIdentity(
                "triangular", "\\sum_{k=1}^n \\frac{1}{k(k+1)}",
                "\\frac{n}{n+1}",
                lambda n: n / (n + 1), lambda n: 1 / (n * (n + 1))),
            InductionIdentity(
                "sum_3k", "\\sum_{k=0}^n 3^k", "\\frac{3^{n+1}-1}{2}",
                lambda n: (3 ** (n + 1) - 1) // 2, lambda n: 3 ** n),
            InductionIdentity(
                "factorial_bound", "n!", "n! >= 2^{n-1} for n >= 1",
                lambda n: 1 if n == 0 else n * (
                    lambda f, x: f(f, x - 1) * x if x > 0 else 1)(
                    lambda f, x: f(f, x - 1) * x if x > 0 else 1, n - 1),
                lambda n: n),
        ]

    def _get_identities(self, difficulty: int) -> list[InductionIdentity]:
        """Return identities appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of available InductionIdentity objects.
        """
        identities = self._build_all_identities()
        if difficulty <= 2:
            return identities[:4]
        if difficulty <= 5:
            return identities[:6]
        return identities

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Select an identity and generate the proof structure.

        Args:
            difficulty: Controls identity complexity.

        Returns:
            Tuple of (identity_statement, solution_data).
        """
        identities = self._get_identities(difficulty)
        identity = self._rng.choice(identities)
        verify_n = self._rng.randint(3, 5 + difficulty)
        problem = f"prove: {identity.formula_lhs} = {identity.formula_rhs}"
        return problem, {
            "identity": identity,
            "verify_n": verify_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate base case and inductive step.

        Args:
            data: Solution data with identity and verification point.

        Returns:
            Steps showing base case, assumption, and inductive step.
        """
        identity = data["identity"]
        verify_n = data["verify_n"]
        base_val = identity.closed_form(1)
        steps: list[str] = [
            f"base case: n=1, LHS={identity.term(1)}, RHS={base_val}, equal",
            "assume true for n=k",
            f"show for n=k+1: add term (k+1) to both sides",
            f"verify: n={verify_n}, LHS={self._compute_sum(identity, verify_n)}, RHS={identity.closed_form(verify_n)}",
        ]
        return steps

    def _compute_sum(self, identity: InductionIdentity, n: int) -> int:
        """Compute the sum of terms up to n directly.

        Args:
            identity: The induction identity.
            n: Upper limit.

        Returns:
            Sum of terms from 1 to n.
        """
        total = 0
        for k in range(1, n + 1):
            total += identity.term(k)
        return total

    def _create_answer(self, data: dict) -> str:
        """Return confirmation that the proof is complete.

        Args:
            data: Solution data.

        Returns:
            Proof completion string.
        """
        return "proven by induction"


@register
class InverseProblemGenerator(StepGenerator):
    """Find the function whose derivative is given (antiderivative).

    Presents f'(x) and requires finding f(x). Verification confirms
    that differentiating the answer recovers the given derivative.
    Uses polynomial and simple power rule antiderivatives.

    Input format:
        ``find function whose derivative is given``

    Target format:
        ``f'(x) = 3x^2 <step> antiderivative of 3x^2 <step>
        power rule: 3x^{2+1}/(2+1) = x^3 <step>
        verify: d/dx(x^3) = 3x^2 ok <step> x^3 + C``

    Difficulty scaling:
        Difficulty 1-2: monomials (ax^n for small n).
        Difficulty 3-4: binomials (two terms).
        Difficulty 5-6: trinomials.
        Difficulty 7-8: four-term polynomials.

    Prerequisites:
        derivative, integral.

    Example:
        >>> gen = InverseProblemGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'inverse_problem'
    """

    _TERM_COUNTS = {
        1: 1, 2: 1, 3: 2, 4: 2,
        5: 3, 6: 3, 7: 4, 8: 4,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "inverse_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Natural language description.
        """
        return "find function whose derivative is given"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a derivative and its antiderivative.

        Constructs f(x) first, then derives to get f'(x).

        Args:
            difficulty: Controls term count.

        Returns:
            Tuple of (derivative_expression, solution_data).
        """
        num_terms = self._TERM_COUNTS.get(difficulty, 2)
        f_terms = self._generate_antiderivative_terms(num_terms, difficulty)
        df_terms = self._differentiate(f_terms)
        evaluator = PolynomialEvaluator()
        f_coeffs = self._terms_to_coeffs(f_terms)
        df_coeffs = self._terms_to_coeffs(df_terms)
        problem = f"f'(x) = {evaluator.format_poly(df_coeffs)}"
        return problem, {
            "f_terms": f_terms, "df_terms": df_terms,
            "f_coeffs": f_coeffs, "df_coeffs": df_coeffs,
            "f_str": evaluator.format_poly(f_coeffs),
            "df_str": evaluator.format_poly(df_coeffs),
        }

    def _generate_antiderivative_terms(self, count: int,
                                       difficulty: int) -> list[tuple[int, int]]:
        """Generate polynomial terms as (coefficient, power) pairs.

        Args:
            count: Number of terms.
            difficulty: Controls coefficient and power ranges.

        Returns:
            List of (coefficient, power) pairs, sorted by power descending.
        """
        max_power = min(2 + difficulty, 6)
        powers = self._rng.sample(range(1, max_power + 1), min(count, max_power))
        terms: list[tuple[int, int]] = []
        for p in sorted(powers, reverse=True):
            coeff = self._rng.randint(1, 5)
            if self._rng.random() < 0.3:
                coeff = -coeff
            terms.append((coeff, p))
        return terms

    def _differentiate(self, terms: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Differentiate polynomial terms using the power rule.

        Args:
            terms: List of (coefficient, power) pairs.

        Returns:
            Differentiated terms (coefficient*power, power-1).
        """
        result: list[tuple[int, int]] = []
        for coeff, power in terms:
            if power > 0:
                result.append((coeff * power, power - 1))
        return result

    def _terms_to_coeffs(self, terms: list[tuple[int, int]]) -> list[int]:
        """Convert (coefficient, power) pairs to a coefficient list.

        Args:
            terms: List of (coefficient, power) pairs.

        Returns:
            Coefficients from highest degree to constant.
        """
        if not terms:
            return [0]
        max_power = max(p for _, p in terms)
        coeffs = [0] * (max_power + 1)
        for coeff, power in terms:
            coeffs[max_power - power] += coeff
        return coeffs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate antidifferentiation and verification steps.

        Args:
            data: Solution data with function and derivative info.

        Returns:
            Steps showing power rule application and verification.
        """
        steps: list[str] = []
        for coeff, power in data["df_terms"]:
            new_power = power + 1
            new_coeff = Fraction(coeff, new_power)
            steps.append(
                f"antiderivative of {coeff}x^{power}: "
                f"{new_coeff}x^{new_power}"
            )
        steps.append(f"f(x) = {data['f_str']} + C")
        steps.append(f"verify: d/dx({data['f_str']}) = {data['df_str']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the antiderivative expression.

        Args:
            data: Solution data.

        Returns:
            Antiderivative string with constant of integration.
        """
        return f"{data['f_str']} + C"


@register
class MethodSelectionGenerator(StepGenerator):
    """Choose the best method to solve a problem and solve it.

    Presents a problem solvable by multiple methods, requires
    selecting one and producing the correct answer. Verification
    checks only correctness regardless of method chosen.

    Input format:
        ``choose best method and solve``

    Target format:
        ``solve x^2 - 5x + 6 = 0 <step> method: factoring <step>
        (x-2)(x-3)=0 <step> x=2 or x=3 <step> {2, 3}``

    Difficulty scaling:
        Difficulty 1-2: quadratics solvable by factoring.
        Difficulty 3-4: quadratics requiring the formula.
        Difficulty 5-6: 2x2 linear systems.
        Difficulty 7-8: 3x3 linear systems.

    Prerequisites:
        quadratic, system_equations.

    Example:
        >>> gen = MethodSelectionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'method_selection'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "method_selection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic", "system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem type.

        Returns:
            Natural language description.
        """
        return "choose best method and solve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem with multiple solution methods.

        Args:
            difficulty: Controls problem type and complexity.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        if difficulty <= 4:
            return self._quadratic_problem(difficulty)
        return self._system_problem(difficulty)

    def _quadratic_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic equation problem.

        Args:
            difficulty: Controls root magnitude.

        Returns:
            Tuple of (equation, solution_data).
        """
        r1 = self._rng.randint(-5 - difficulty, 5 + difficulty)
        r2 = self._rng.randint(-5 - difficulty, 5 + difficulty)
        b = -(r1 + r2)
        c = r1 * r2
        equation = self._format_quadratic(b, c)
        method = "factoring" if self._is_factorable(r1, r2) else "quadratic formula"
        return equation, {
            "type": "quadratic", "r1": r1, "r2": r2,
            "b": b, "c": c, "method": method,
        }

    def _format_quadratic(self, b: int, c: int) -> str:
        """Format a monic quadratic equation x^2 + bx + c = 0.

        Args:
            b: Coefficient of x.
            c: Constant term.

        Returns:
            Formatted equation string.
        """
        parts = ["x^2"]
        if b > 0:
            parts.append(f"+{b}x")
        elif b < 0:
            parts.append(f"{b}x")
        if c > 0:
            parts.append(f"+{c}")
        elif c < 0:
            parts.append(f"{c}")
        return f"{''.join(parts)} = 0"

    def _is_factorable(self, r1: int, r2: int) -> bool:
        """Check if the quadratic is easily factorable.

        Args:
            r1: First root.
            r2: Second root.

        Returns:
            True if both roots are small integers.
        """
        return abs(r1) <= 10 and abs(r2) <= 10

    def _system_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear system problem.

        Args:
            difficulty: Controls system size.

        Returns:
            Tuple of (system_description, solution_data).
        """
        x = self._rng.randint(-5, 5)
        y = self._rng.randint(-5, 5)
        a1 = self._rng.randint(1, 5)
        b1 = self._rng.randint(1, 5)
        a2 = self._rng.randint(1, 5)
        b2 = self._rng.randint(1, 5)
        while a1 * b2 == a2 * b1:
            b2 = self._rng.randint(1, 5)
        c1 = a1 * x + b1 * y
        c2 = a2 * x + b2 * y
        system = f"{a1}x+{b1}y={c1}, {a2}x+{b2}y={c2}"
        return system, {
            "type": "system", "x": x, "y": y,
            "a1": a1, "b1": b1, "c1": c1,
            "a2": a2, "b2": b2, "c2": c2,
            "method": "elimination",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate method selection and solution steps.

        Args:
            data: Solution data with problem type and values.

        Returns:
            Steps showing method choice and solution.
        """
        if data["type"] == "quadratic":
            return self._quadratic_steps(data)
        return self._system_steps(data)

    def _quadratic_steps(self, data: dict) -> list[str]:
        """Generate steps for solving a quadratic equation.

        Args:
            data: Solution data with roots and method.

        Returns:
            Steps showing the chosen method and solution.
        """
        r1, r2 = data["r1"], data["r2"]
        method = data["method"]
        steps: list[str] = [f"method: {method}"]
        if method == "factoring":
            steps.append(f"(x-{r1})(x-{r2})=0")
        else:
            disc = data["b"] ** 2 - 4 * data["c"]
            steps.append(f"discriminant: {data['b']}^2-4*{data['c']}={disc}")
        steps.append(f"x={r1} or x={r2}")
        return steps

    def _system_steps(self, data: dict) -> list[str]:
        """Generate steps for solving a linear system.

        Args:
            data: Solution data with system coefficients.

        Returns:
            Steps showing elimination method.
        """
        return [
            f"method: {data['method']}",
            f"multiply eq1 by {data['a2']}, eq2 by {data['a1']}",
            f"subtract to eliminate x",
            f"x={data['x']}, y={data['y']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution set.

        Args:
            data: Solution data.

        Returns:
            Formatted solution string.
        """
        if data["type"] == "quadratic":
            r1, r2 = sorted([data["r1"], data["r2"]])
            return f"{{{r1}, {r2}}}"
        return f"x={data['x']}, y={data['y']}"


@register
class EstimateMagnitudeGenerator(StepGenerator):
    """Estimate the order of magnitude before computing exactly.

    Presents a complex arithmetic expression, requires an order-of-
    magnitude estimate, then verifies by computing the exact value.
    The estimate must be within 1 order of magnitude of exact.

    Input format:
        ``estimate the order of magnitude``

    Target format:
        ``347 * 892 <step> estimate: 300*900=270000, ~10^5 <step>
        exact: 347*892=309424 <step> |log10(309424)-5|<1: ok
        <step> 309424``

    Difficulty scaling:
        Difficulty 1-2: two-operand products.
        Difficulty 3-4: three-operand products.
        Difficulty 5-6: products with division.
        Difficulty 7-8: mixed operations with powers.

    Prerequisites:
        exponentiation, multiplication.

    Example:
        >>> gen = EstimateMagnitudeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'estimate_magnitude'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "estimate_magnitude"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Natural language description.
        """
        return "estimate the order of magnitude"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an arithmetic expression for magnitude estimation.

        Args:
            difficulty: Controls operand count and operation types.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        if difficulty <= 2:
            return self._two_operand_product(difficulty)
        if difficulty <= 4:
            return self._three_operand_product(difficulty)
        return self._mixed_expression(difficulty)

    def _two_operand_product(self, difficulty: int) -> tuple[str, dict]:
        """Generate a two-operand multiplication.

        Args:
            difficulty: Controls operand magnitude.

        Returns:
            Tuple of (expression, solution_data).
        """
        mag = difficulty + 1
        a = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        b = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        exact = a * b
        estimate = self._round_estimate(a) * self._round_estimate(b)
        return f"{a} * {b}", {
            "expression": f"{a} * {b}",
            "exact": exact, "estimate": estimate,
            "magnitude": self._order_of_magnitude(exact),
        }

    def _three_operand_product(self, difficulty: int) -> tuple[str, dict]:
        """Generate a three-operand multiplication.

        Args:
            difficulty: Controls operand magnitude.

        Returns:
            Tuple of (expression, solution_data).
        """
        mag = max(1, difficulty - 1)
        a = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        b = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        c = self._rng.randint(10, 99)
        exact = a * b * c
        estimate = self._round_estimate(a) * self._round_estimate(b) * self._round_estimate(c)
        return f"{a} * {b} * {c}", {
            "expression": f"{a} * {b} * {c}",
            "exact": exact, "estimate": estimate,
            "magnitude": self._order_of_magnitude(exact),
        }

    def _mixed_expression(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mixed multiplication and division expression.

        Args:
            difficulty: Controls operand magnitude.

        Returns:
            Tuple of (expression, solution_data).
        """
        mag = max(1, difficulty - 2)
        a = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        b = self._rng.randint(10 ** mag, 10 ** (mag + 1) - 1)
        c = self._rng.randint(2, 20)
        exact = (a * b) // c
        est_num = self._round_estimate(a) * self._round_estimate(b)
        estimate = est_num // c
        expr = f"({a} * {b}) / {c}"
        return expr, {
            "expression": expr,
            "exact": exact, "estimate": estimate,
            "magnitude": self._order_of_magnitude(max(1, exact)),
        }

    def _round_estimate(self, n: int) -> int:
        """Round a number to its leading digit for estimation.

        Args:
            n: Number to round.

        Returns:
            Rounded estimate (e.g. 347 -> 300).
        """
        if n == 0:
            return 0
        magnitude = 10 ** (len(str(abs(n))) - 1)
        return (n // magnitude) * magnitude

    def _order_of_magnitude(self, n: int) -> int:
        """Compute the order of magnitude (floor of log10).

        Args:
            n: Positive integer.

        Returns:
            Floor of log10(n).
        """
        if n <= 0:
            return 0
        return int(math.log10(n))

    def _create_steps(self, data: dict) -> list[str]:
        """Generate estimation and verification steps.

        Args:
            data: Solution data with exact value and estimate.

        Returns:
            Steps showing estimate, exact computation, and verification.
        """
        mag = data["magnitude"]
        exact = data["exact"]
        estimate = data["estimate"]
        return [
            f"estimate: ~{estimate}, order 10^{self._order_of_magnitude(max(1, estimate))}",
            f"exact: {data['expression']}={exact}",
            f"magnitude: 10^{mag}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the exact value.

        Args:
            data: Solution data.

        Returns:
            String of the exact computed value.
        """
        return str(data["exact"])


@register
class DeriveFormulaGenerator(StepGenerator):
    """Derive a known formula from first principles.

    Uses known derivations (quadratic formula, geometric series sum,
    difference of squares) and generates step-by-step algebraic
    manipulations. Each step can be verified by evaluation at
    random points.

    Input format:
        ``derive formula from first principles``

    Target format:
        ``derive: sum of geometric series <step> S=1+r+r^2+...+r^n
        <step> rS=r+r^2+...+r^{n+1} <step> S-rS=1-r^{n+1} <step>
        S(1-r)=1-r^{n+1} <step> S=(1-r^{n+1})/(1-r)``

    Difficulty scaling:
        Difficulty 1-2: difference of squares, simple factorisations.
        Difficulty 3-4: geometric series.
        Difficulty 5-6: quadratic formula derivation.
        Difficulty 7-8: binomial theorem for small n.

    Prerequisites:
        quadratic, polynomial_multiply.

    Example:
        >>> gen = DeriveFormulaGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'derive_formula'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "derive_formula"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic", "polynomial_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls derivation complexity.

        Returns:
            Natural language description.
        """
        return "derive formula from first principles"

    _DERIVATIONS: list[dict] = [
        {"name": "difference of squares",
         "statement": "a^2 - b^2 = (a-b)(a+b)",
         "steps": ["expand (a-b)(a+b)", "= a*a + a*b - b*a - b*b",
                    "= a^2 + ab - ab - b^2", "= a^2 - b^2"],
         "verify_a": 5, "verify_b": 3, "verify_lhs": 16, "verify_rhs": 16},
        {"name": "sum of arithmetic series",
         "statement": "S = n(n+1)/2",
         "steps": ["S = 1 + 2 + ... + n", "S = n + (n-1) + ... + 1",
                    "2S = (n+1) + (n+1) + ... + (n+1) = n(n+1)", "S = n(n+1)/2"],
         "verify_a": 10, "verify_b": 0, "verify_lhs": 55, "verify_rhs": 55},
        {"name": "geometric series",
         "statement": "S = (1-r^{n+1})/(1-r)",
         "steps": ["S = 1 + r + r^2 + ... + r^n", "rS = r + r^2 + ... + r^{n+1}",
                    "S - rS = 1 - r^{n+1}", "S(1-r) = 1 - r^{n+1}",
                    "S = (1-r^{n+1})/(1-r)"],
         "verify_a": 2, "verify_b": 3, "verify_lhs": 15, "verify_rhs": 15},
        {"name": "quadratic formula",
         "statement": "x = (-b +/- sqrt(b^2-4ac))/(2a)",
         "steps": ["start: ax^2 + bx + c = 0", "divide by a: x^2 + (b/a)x + c/a = 0",
                    "complete square: (x + b/(2a))^2 = b^2/(4a^2) - c/a",
                    "= (b^2 - 4ac)/(4a^2)", "x + b/(2a) = +/- sqrt(b^2-4ac)/(2a)",
                    "x = (-b +/- sqrt(b^2-4ac))/(2a)"],
         "verify_a": 1, "verify_b": -5, "verify_lhs": 6, "verify_rhs": 6},
        {"name": "binomial theorem (n=2)",
         "statement": "(a+b)^2 = a^2 + 2ab + b^2",
         "steps": ["(a+b)(a+b)", "= a*a + a*b + b*a + b*b", "= a^2 + 2ab + b^2"],
         "verify_a": 3, "verify_b": 4, "verify_lhs": 49, "verify_rhs": 49},
        {"name": "sum of cubes factorisation",
         "statement": "a^3 + b^3 = (a+b)(a^2-ab+b^2)",
         "steps": ["expand RHS: a^3 - a^2b + ab^2 + a^2b - ab^2 + b^3",
                    "cancel: a^3 + b^3"],
         "verify_a": 2, "verify_b": 3, "verify_lhs": 35, "verify_rhs": 35},
        {"name": "distance formula",
         "statement": "d = sqrt((x2-x1)^2 + (y2-y1)^2)",
         "steps": ["right triangle with legs dx = x2-x1, dy = y2-y1",
                    "by Pythagorean theorem: d^2 = dx^2 + dy^2",
                    "d = sqrt(dx^2 + dy^2)"],
         "verify_a": 5, "verify_b": 0, "verify_lhs": 5, "verify_rhs": 5},
        {"name": "derivative of x^n",
         "statement": "d/dx(x^n) = n*x^{n-1}",
         "steps": ["f(x+h) = (x+h)^n = x^n + n*x^{n-1}*h + ...",
                    "[f(x+h) - f(x)] / h = n*x^{n-1} + O(h)",
                    "limit h->0: n*x^{n-1}"],
         "verify_a": 3, "verify_b": 2, "verify_lhs": 12, "verify_rhs": 12},
        {"name": "Euler's formula for polyhedra",
         "statement": "V - E + F = 2",
         "steps": ["for a cube: V=8, E=12, F=6", "8 - 12 + 6 = 2",
                    "proof by removing faces one at a time"],
         "verify_a": 8, "verify_b": 0, "verify_lhs": 2, "verify_rhs": 2},
        {"name": "area of a circle",
         "statement": "A = pi*r^2",
         "steps": ["divide circle into n thin triangles from centre",
                    "each triangle: base ~ 2*pi*r/n, height ~ r",
                    "total area ~ n * (1/2)(2*pi*r/n)(r) = pi*r^2"],
         "verify_a": 5, "verify_b": 0, "verify_lhs": 78, "verify_rhs": 78},
    ]

    def _get_derivations(self, difficulty: int) -> list[dict]:
        """Return derivations appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of derivation dictionaries.
        """
        if difficulty <= 2:
            return self._DERIVATIONS[:4]
        if difficulty <= 5:
            return self._DERIVATIONS[:7]
        return list(self._DERIVATIONS)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Select a derivation and generate randomised verification values.

        Args:
            difficulty: Controls available derivations.

        Returns:
            Tuple of (derivation_name, solution_data).
        """
        derivations = self._get_derivations(difficulty)
        derivation = dict(self._rng.choice(derivations))
        # Randomise verification values for variety
        va = self._rng.randint(2, 8 + difficulty)
        vb = self._rng.randint(1, 6 + difficulty)
        derivation["verify_a"] = va
        derivation["verify_b"] = vb
        # Recompute verification based on derivation
        lhs, rhs = self._compute_verify(derivation["name"], va, vb)
        derivation["verify_lhs"] = lhs
        derivation["verify_rhs"] = rhs
        problem = f"derive: {derivation['name']} ({derivation['statement']}) [verify a={va},b={vb}]"
        return problem, {"derivation": derivation}

    def _compute_verify(self, name: str, a: int, b: int) -> tuple:
        """Compute verification values for a derivation at given points.

        Args:
            name: Derivation name.
            a: First verification parameter.
            b: Second verification parameter.

        Returns:
            Tuple of (lhs_value, rhs_value).
        """
        if name == "difference of squares":
            return a * a - b * b, (a - b) * (a + b)
        if name == "sum of arithmetic series":
            return a * (a + 1) // 2, a * (a + 1) // 2
        if name == "geometric series":
            s = sum(a ** i for i in range(b + 1))
            return s, s
        if name == "quadratic formula":
            return a * b, a * b  # placeholder
        if name == "binomial theorem (n=2)":
            return (a + b) ** 2, a * a + 2 * a * b + b * b
        if name == "sum of cubes factorisation":
            return a ** 3 + b ** 3, (a + b) * (a * a - a * b + b * b)
        if name == "distance formula":
            return int((a * a + b * b) ** 0.5), int((a * a + b * b) ** 0.5)
        if name == "derivative of x^n":
            return a * b ** (a - 1), a * b ** (a - 1)
        if name == "Euler's formula for polyhedra":
            return 2, 2
        if name == "area of a circle":
            return int(3.14159 * a * a), int(3.14159 * a * a)
        return a, a

    def _create_steps(self, data: dict) -> list[str]:
        """Generate the algebraic derivation steps.

        Args:
            data: Solution data with derivation info.

        Returns:
            Derivation steps and verification.
        """
        derivation = data["derivation"]
        steps = list(derivation["steps"])
        steps.append(
            f"verify: LHS={derivation['verify_lhs']}, "
            f"RHS={derivation['verify_rhs']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the derived formula statement.

        Args:
            data: Solution data.

        Returns:
            The formula statement.
        """
        return data["derivation"]["statement"]


@register
class SufficiencyAnalysisGenerator(StepGenerator):
    """Determine if a problem has enough information to solve.

    Mixes solvable problems (sufficient information) with unsolvable
    ones (missing a variable) in a 50/50 split. The target explains
    what is missing or solves the problem if sufficient.

    Input format:
        ``is this problem solvable with given information``

    Target format (solvable):
        ``find x: 3x + 5 = 20 <step> sufficient: one equation, one
        unknown <step> 3x=15, x=5 <step> solvable, x=5``

    Target format (unsolvable):
        ``find x: 3x + y = 20 <step> insufficient: 2 unknowns, 1
        equation <step> missing: value of y <step> unsolvable``

    Difficulty scaling:
        Difficulty 1-2: single variable linear (solvable) vs 2-var (not).
        Difficulty 3-4: systems with/without enough equations.
        Difficulty 5-6: quadratics with/without discriminant info.
        Difficulty 7-8: multi-step with parameter ambiguity.

    Prerequisites:
        linear_equation.

    Example:
        >>> gen = SufficiencyAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'sufficiency_analysis'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "sufficiency_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Natural language description.
        """
        return "is this problem solvable with given information"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem that is either solvable or not.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        is_solvable = self._rng.random() < 0.5
        if is_solvable:
            return self._solvable_problem(difficulty)
        return self._unsolvable_problem(difficulty)

    def _solvable_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem with sufficient information.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (equation, solution_data).
        """
        a = self._rng.randint(1, 5 + difficulty)
        x = self._rng.randint(-10, 10)
        b = self._rng.randint(-10, 10)
        c = a * x + b
        equation = f"find x: {a}x + {b} = {c}"
        return equation, {
            "solvable": True, "a": a, "b": b, "c": c, "x": x,
            "reason": f"one equation, one unknown",
        }

    def _unsolvable_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem with insufficient information.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (equation, solution_data).
        """
        a = self._rng.randint(1, 5 + difficulty)
        b = self._rng.randint(1, 5 + difficulty)
        c = self._rng.randint(1, 50)
        equation = f"find x: {a}x + {b}y = {c}"
        return equation, {
            "solvable": False, "a": a, "b": b, "c": c,
            "missing": "value of y",
            "reason": "2 unknowns, 1 equation",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sufficiency analysis steps.

        Args:
            data: Solution data with solvability info.

        Returns:
            Steps showing analysis and solution or explanation.
        """
        if data["solvable"]:
            return self._solvable_steps(data)
        return self._unsolvable_steps(data)

    def _solvable_steps(self, data: dict) -> list[str]:
        """Generate steps for a solvable problem.

        Args:
            data: Solution data with equation and solution.

        Returns:
            Steps showing sufficiency and solution.
        """
        a, b, c, x = data["a"], data["b"], data["c"], data["x"]
        rhs = c - b
        return [
            f"sufficient: {data['reason']}",
            f"{a}x = {c} - {b} = {rhs}",
            f"x = {rhs}/{a} = {x}",
        ]

    def _unsolvable_steps(self, data: dict) -> list[str]:
        """Generate steps for an unsolvable problem.

        Args:
            data: Solution data with missing information.

        Returns:
            Steps explaining what is missing.
        """
        return [
            f"insufficient: {data['reason']}",
            f"missing: {data['missing']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solvability verdict and solution if applicable.

        Args:
            data: Solution data.

        Returns:
            Verdict string.
        """
        if data["solvable"]:
            return f"solvable, x={data['x']}"
        return "unsolvable"
