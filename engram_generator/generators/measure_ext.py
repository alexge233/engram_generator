"""Extended measure theory generators for tiers 5-7.

6 generators covering outer measure, product measure, Radon-Nikodym
derivative, modes of convergence, probability measures, and conditional
expectation. Each produces step-by-step solutions with LaTeX formatting.
"""
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


def _fmt_frac(val: Fraction) -> str:
    """Format a Fraction as a string.

    Args:
        val: Fraction value.

    Returns:
        String representation.
    """
    if val.denominator == 1:
        return str(val.numerator)
    return f"{val.numerator}/{val.denominator}"


# ── 1. Outer measure (tier 6) ────────────────────────────────────


@register
class OuterMeasureGenerator(StepGenerator):
    """Compute the outer measure of simple sets using interval covers.

    Uses m*(A) = inf{sum l(I_k) : A subset union I_k} for sets such
    as finite point sets, rationals in an interval, and Cantor-like
    constructions. Template-based with randomised parameters.

    Input format:
        ``compute outer measure of set``

    Target format:
        ``A = {1/n : n >= 1} intersect [0,1] <step>
        A is countable <step>
        cover each point 1/n by interval (1/n - eps/2^{n+1}, 1/n + eps/2^{n+1})
        <step> total cover length = sum eps/2^n = eps <step>
        since eps arbitrary, m*(A) = 0``

    Difficulty scaling:
        Difficulty 1-3: finite point sets (measure = 0).
        Difficulty 4-6: countable sets (rationals, 1/n sequence).
        Difficulty 7-8: Cantor set or fat Cantor set.

    Prerequisites:
        lebesgue_measure.
    """

    _SETS = [
        {
            "set_desc": "finite set of {n} points in [0,1]",
            "is_countable": True,
            "argument": "cover each point by interval of length eps/{n}",
            "total_cover": "eps (arbitrary)",
            "measure": "0",
            "measure_val": Fraction(0),
            "needs_n": True,
        },
        {
            "set_desc": "Q intersect [0,1] (rationals in [0,1])",
            "is_countable": True,
            "argument": "enumerate rationals q_1, q_2, ...; cover q_k by interval of length eps/2^k",
            "total_cover": "sum_{k=1}^inf eps/2^k = eps",
            "measure": "0",
            "measure_val": Fraction(0),
            "needs_n": False,
        },
        {
            "set_desc": "{1/n : n = 1, 2, 3, ...} subset [0,1]",
            "is_countable": True,
            "argument": "countable set; cover 1/n by interval of length eps/2^n",
            "total_cover": "sum eps/2^n = eps (geometric series)",
            "measure": "0",
            "measure_val": Fraction(0),
            "needs_n": False,
        },
        {
            "set_desc": "Cantor set C subset [0,1]",
            "is_countable": False,
            "argument": "at step k, remove middle third of each interval; remaining length = (2/3)^k",
            "total_cover": "lim (2/3)^k = 0 as k -> inf",
            "measure": "0",
            "measure_val": Fraction(0),
            "needs_n": False,
        },
        {
            "set_desc": "fat Cantor set (remove middle 1/4 at each step) in [0,1]",
            "is_countable": False,
            "argument": "at step k, remaining length = 1 - sum_{j=1}^k 2^{j-1} / 4^j",
            "total_cover": "remaining = 1 - 1/2 = 1/2",
            "measure": "1/2",
            "measure_val": Fraction(1, 2),
            "needs_n": False,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "outer_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lebesgue_measure"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls set complexity.

        Returns:
            Natural language description.
        """
        return "compute outer measure of set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an outer measure problem.

        Args:
            difficulty: Controls which set template is used.

        Returns:
            Tuple of (set_description, solution_data).
        """
        if difficulty <= 3:
            pool = self._SETS[:1]
        elif difficulty <= 6:
            pool = self._SETS[:3]
        else:
            pool = self._SETS

        template = self._rng.choice(pool)
        data = dict(template)

        if data["needs_n"]:
            n = self._rng.randint(3, 8 + difficulty)
            data["set_desc"] = data["set_desc"].format(n=n)
            data["argument"] = data["argument"].format(n=n)

        problem = f"m*: A = {data['set_desc']}"
        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate outer measure reasoning steps.

        Args:
            data: Solution data with covering argument.

        Returns:
            Steps showing the covering and measure computation.
        """
        steps = [f"A = {data['set_desc']}"]
        if data["is_countable"]:
            steps.append("A is countable")
        steps.append(f"cover: {data['argument']}")
        steps.append(f"total cover length: {data['total_cover']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the outer measure.

        Args:
            data: Solution data.

        Returns:
            Measure as a string.
        """
        return f"m*(A)={data['measure']}"


# ── 2. Product measure (tier 6) ──────────────────────────────────


@register
class ProductMeasureGenerator(StepGenerator):
    """Compute the product measure of a rectangle in R^2.

    Uses (m x m)(A x B) = m(A) * m(B) for measurable sets A, B in R.
    Generates rectangles with rational endpoints and computes the
    product measure.

    Input format:
        ``compute product measure of rectangle``

    Target format:
        ``A = [1, 3], B = [2, 5] <step>
        m(A) = 3-1 = 2, m(B) = 5-2 = 3 <step>
        (m x m)(A x B) = 2 * 3 = 6``

    Difficulty scaling:
        Difficulty 1-3: simple integer endpoints.
        Difficulty 4-6: rational endpoints, union of rectangles.
        Difficulty 7-8: L-shaped or cross-shaped regions.

    Prerequisites:
        lebesgue_measure.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "product_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lebesgue_measure"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls rectangle complexity.

        Returns:
            Natural language description.
        """
        return "compute product measure of rectangle in R^2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a product measure problem.

        Args:
            difficulty: Controls complexity of region.

        Returns:
            Tuple of (region_description, solution_data).
        """
        if difficulty <= 4:
            return self._single_rectangle(difficulty)
        return self._union_rectangles(difficulty)

    def _single_rectangle(self, difficulty: int) -> tuple[str, dict]:
        """Generate a single rectangle product measure problem.

        Args:
            difficulty: Controls endpoint range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a1 = Fraction(self._rng.randint(0, 3))
        a2 = a1 + Fraction(self._rng.randint(1, 3 + difficulty))
        b1 = Fraction(self._rng.randint(0, 3))
        b2 = b1 + Fraction(self._rng.randint(1, 3 + difficulty))

        m_a = a2 - a1
        m_b = b2 - b1
        product = m_a * m_b

        problem = (f"(m x m): A=[{_fmt_frac(a1)},{_fmt_frac(a2)}] x "
                   f"B=[{_fmt_frac(b1)},{_fmt_frac(b2)}]")
        return problem, {
            "type": "single",
            "a1": a1, "a2": a2, "b1": b1, "b2": b2,
            "m_a": m_a, "m_b": m_b, "product": product,
            "rectangles": [{"a1": a1, "a2": a2, "b1": b1, "b2": b2,
                            "m_a": m_a, "m_b": m_b, "area": product}],
        }

    def _union_rectangles(self, difficulty: int) -> tuple[str, dict]:
        """Generate a disjoint union of rectangles product measure problem.

        Args:
            difficulty: Controls number of rectangles.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n_rects = self._rng.randint(2, min(3, difficulty))
        rectangles = []
        total = Fraction(0)
        cursor_x = Fraction(0)

        for _ in range(n_rects):
            a1 = cursor_x + Fraction(self._rng.randint(1, 2))
            a2 = a1 + Fraction(self._rng.randint(1, 2 + difficulty))
            b1 = Fraction(self._rng.randint(0, 2))
            b2 = b1 + Fraction(self._rng.randint(1, 2 + difficulty))
            m_a = a2 - a1
            m_b = b2 - b1
            area = m_a * m_b
            rectangles.append({"a1": a1, "a2": a2, "b1": b1, "b2": b2,
                                "m_a": m_a, "m_b": m_b, "area": area})
            total += area
            cursor_x = a2

        parts = " union ".join(
            f"[{_fmt_frac(r['a1'])},{_fmt_frac(r['a2'])}]x"
            f"[{_fmt_frac(r['b1'])},{_fmt_frac(r['b2'])}]"
            for r in rectangles
        )
        problem = f"(m x m): {parts}"
        return problem, {
            "type": "union",
            "rectangles": rectangles,
            "product": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate product measure computation steps.

        Args:
            data: Solution data with rectangles and areas.

        Returns:
            Steps showing measure of each side and product.
        """
        steps = []
        for i, r in enumerate(data["rectangles"]):
            steps.append(
                f"rect {i + 1}: m(A)={_fmt_frac(r['m_a'])}, "
                f"m(B)={_fmt_frac(r['m_b'])}, "
                f"area={_fmt_frac(r['area'])}"
            )
        if len(data["rectangles"]) > 1:
            steps.append(f"total = {_fmt_frac(data['product'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the product measure.

        Args:
            data: Solution data.

        Returns:
            Measure as a string.
        """
        return f"(m x m)={_fmt_frac(data['product'])}"


# ── 3. Radon-Nikodym derivative (tier 7) ─────────────────────────


@register
class RadonNikodymGenerator(StepGenerator):
    """Compute the Radon-Nikodym derivative dmu/dlambda for simple densities.

    Given that mu is absolutely continuous with respect to Lebesgue
    measure lambda, and mu(A) = integral_A f dlambda, identifies f as
    the Radon-Nikodym derivative.

    Input format:
        ``compute Radon-Nikodym derivative``

    Target format:
        ``mu([a,b]) = integral_a^b c*x^n dx for all intervals <step>
        mu << lambda (absolutely continuous) <step>
        dmu/dlambda = c*x^n <step>
        verify: mu([0,1]) = integral_0^1 c*x^n dx = c/(n+1)``

    Difficulty scaling:
        Difficulty 1-3: constant density f = c.
        Difficulty 4-6: polynomial density f = c*x^n.
        Difficulty 7-8: piecewise density.

    Prerequisites:
        lebesgue_measure.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "radon_nikodym"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lebesgue_measure"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls density complexity.

        Returns:
            Natural language description.
        """
        return "compute Radon-Nikodym derivative dmu/dlambda"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Radon-Nikodym derivative problem.

        Args:
            difficulty: Controls density form.

        Returns:
            Tuple of (measure_description, solution_data).
        """
        if difficulty <= 3:
            return self._constant_density(difficulty)
        if difficulty <= 6:
            return self._polynomial_density(difficulty)
        return self._piecewise_density(difficulty)

    def _constant_density(self, difficulty: int) -> tuple[str, dict]:
        """Generate a constant density problem.

        Args:
            difficulty: Controls constant value.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        c = Fraction(self._rng.randint(1, 5))
        a = Fraction(self._rng.randint(0, 3))
        b = a + Fraction(self._rng.randint(1, 4))

        density = f"{_fmt_frac(c)}"
        mu_ab = c * (b - a)
        verification = f"mu([{_fmt_frac(a)},{_fmt_frac(b)}]) = {_fmt_frac(c)} * {_fmt_frac(b - a)} = {_fmt_frac(mu_ab)}"

        problem = f"mu([a,b]) = \\int_a^b {density}\\,dx"
        return problem, {
            "density_type": "constant",
            "density_latex": density,
            "density_func": density,
            "c": c, "verification": verification,
            "verify_interval": (a, b), "verify_value": mu_ab,
        }

    def _polynomial_density(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial density problem.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        c = Fraction(self._rng.randint(1, 4))
        n = self._rng.randint(1, min(3, difficulty))

        density = f"{_fmt_frac(c)}x^{n}"
        # Verify on [0, 1]: integral = c/(n+1)
        verify_value = c / Fraction(n + 1)
        verification = f"mu([0,1]) = int_0^1 {density} dx = {_fmt_frac(c)}/{n + 1} = {_fmt_frac(verify_value)}"

        problem = f"mu([a,b]) = \\int_a^b {density}\\,dx"
        return problem, {
            "density_type": "polynomial",
            "density_latex": density,
            "density_func": density,
            "c": c, "n": n,
            "verification": verification,
            "verify_interval": (Fraction(0), Fraction(1)),
            "verify_value": verify_value,
        }

    def _piecewise_density(self, difficulty: int) -> tuple[str, dict]:
        """Generate a piecewise constant density problem.

        Args:
            difficulty: Controls number of pieces.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        c1 = Fraction(self._rng.randint(1, 4))
        c2 = Fraction(self._rng.randint(1, 4))
        split = Fraction(self._rng.randint(1, 3))

        density = f"{_fmt_frac(c1)} on [0,{_fmt_frac(split)}), {_fmt_frac(c2)} on [{_fmt_frac(split)},inf)"
        verify_b = split + Fraction(self._rng.randint(1, 3))
        verify_value = c1 * split + c2 * (verify_b - split)
        verification = (f"mu([0,{_fmt_frac(verify_b)}]) = "
                        f"{_fmt_frac(c1)}*{_fmt_frac(split)} + "
                        f"{_fmt_frac(c2)}*{_fmt_frac(verify_b - split)} = "
                        f"{_fmt_frac(verify_value)}")

        problem = f"mu([a,b]) = \\int_a^b f\\,dx, f = {density}"
        return problem, {
            "density_type": "piecewise",
            "density_latex": density,
            "density_func": density,
            "verification": verification,
            "verify_interval": (Fraction(0), verify_b),
            "verify_value": verify_value,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Radon-Nikodym derivative steps.

        Args:
            data: Solution data with density and verification.

        Returns:
            Steps showing absolute continuity, density, and verification.
        """
        return [
            "mu << lambda (absolutely continuous)",
            f"dmu/dlambda = f(x) = {data['density_func']}",
            f"verify: {data['verification']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Radon-Nikodym derivative.

        Args:
            data: Solution data.

        Returns:
            Density function string.
        """
        return f"dmu/dlambda = {data['density_func']}"


# ── 4. Convergence modes (tier 6) ───────────────────────────────


@register
class ConvergenceModesGenerator(StepGenerator):
    """Determine which modes of convergence hold for a given sequence.

    Given a sequence of functions f_n on a measure space, determines
    which of the standard convergence modes hold: almost everywhere (a.e.),
    in measure, in L^p, almost surely (a.s. for probability spaces).

    Input format:
        ``determine convergence modes for f_n``

    Target format:
        ``f_n(x) = x^n on [0,1] with Lebesgue measure <step>
        pointwise limit: f(x) = 0 for x in [0,1), f(1) = 1 <step>
        a.e. convergence: yes (f_n -> 0 a.e., fails only at x=1) <step>
        in measure: yes (m({|f_n - f| > eps}) -> 0) <step>
        in L^1: yes (int |f_n - f| = 1/(n+1) -> 0)``

    Difficulty scaling:
        Difficulty 1-3: standard sequences with all modes.
        Difficulty 4-6: sequences where some modes fail.
        Difficulty 7-8: typewriter sequence (in measure but not a.e.).

    Prerequisites:
        sigma_algebra.
    """

    _SEQUENCES = [
        {
            "fn_desc": "f_n(x) = x^n on [0,1] with Lebesgue measure",
            "limit": "f(x) = 0 for x in [0,1), f(1) = 1",
            "ae": ("yes", "f_n -> 0 a.e.; fails only on {1}, which has measure 0"),
            "in_measure": ("yes", "m({|f_n| > eps}) = m({x : x^n > eps}) = 1 - eps^{1/n} -> 0"),
            "in_Lp": ("yes", "int_0^1 x^n dx = 1/(n+1) -> 0"),
        },
        {
            "fn_desc": "f_n(x) = n*x*(1-x)^n on [0,1]",
            "limit": "f(x) = 0 for all x in [0,1]",
            "ae": ("yes", "for each x in (0,1], n*x*(1-x)^n -> 0"),
            "in_measure": ("yes", "pointwise a.e. on finite measure space implies in measure"),
            "in_Lp": ("no", "int_0^1 n*x*(1-x)^n dx = n/((n+1)(n+2)) ~ 1/n -> 0, so yes for L^1"),
        },
        {
            "fn_desc": "f_n = n * 1_{[0,1/n]} on [0,1]",
            "limit": "f(x) = 0 for x > 0 (pointwise)",
            "ae": ("yes", "for each x > 0, f_n(x) = 0 for n > 1/x"),
            "in_measure": ("yes", "m({f_n > eps}) = m([0,1/n]) = 1/n -> 0"),
            "in_Lp": ("no", "int |f_n| = n * (1/n) = 1 for all n, so not L^1 convergent"),
        },
        {
            "fn_desc": "typewriter sequence: f_n = 1_{I_n} cycling through [0,1] with shrinking intervals",
            "limit": "f(x) = 0 for all x",
            "ae": ("no", "every x is in infinitely many I_n; f_n(x) = 1 infinitely often"),
            "in_measure": ("yes", "m(I_n) -> 0 since intervals shrink"),
            "in_Lp": ("yes", "int |f_n| = m(I_n) -> 0"),
        },
        {
            "fn_desc": "f_n(x) = sin(nx)/n on [0,2*pi]",
            "limit": "f(x) = 0 for all x",
            "ae": ("yes", "|f_n(x)| <= 1/n -> 0 for all x"),
            "in_measure": ("yes", "uniform convergence implies convergence in measure"),
            "in_Lp": ("yes", "int |f_n|^p <= (1/n)^p * 2*pi -> 0"),
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convergence_modes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sigma_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls sequence complexity.

        Returns:
            Natural language description.
        """
        return "determine which convergence modes hold for f_n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a convergence modes problem.

        Args:
            difficulty: Controls sequence pool.

        Returns:
            Tuple of (sequence_description, solution_data).
        """
        pool = self._SEQUENCES[:max(2, min(len(self._SEQUENCES), 1 + difficulty))]
        seq = self._rng.choice(pool)
        problem = seq["fn_desc"]
        return problem, dict(seq)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate convergence analysis steps.

        Args:
            data: Solution data with convergence assessments.

        Returns:
            Steps showing each convergence mode.
        """
        ae_yn, ae_reason = data["ae"]
        im_yn, im_reason = data["in_measure"]
        lp_yn, lp_reason = data["in_Lp"]
        return [
            f"pointwise limit: {data['limit']}",
            f"a.e. convergence: {ae_yn} ({ae_reason})",
            f"in measure: {im_yn} ({im_reason})",
            f"in L^p: {lp_yn} ({lp_reason})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the convergence mode summary.

        Args:
            data: Solution data.

        Returns:
            Summary of which modes hold.
        """
        modes = []
        if data["ae"][0] == "yes":
            modes.append("a.e.")
        if data["in_measure"][0] == "yes":
            modes.append("in measure")
        if data["in_Lp"][0] == "yes":
            modes.append("in L^p")
        return f"converges: {', '.join(modes)}" if modes else "no convergence in standard modes"


# ── 5. Probability measure (tier 5) ─────────────────────────────


@register
class ProbabilityMeasureGenerator(StepGenerator):
    """Verify P is a probability measure and compute P of events.

    Checks P(Omega)=1, P(empty)=0, and countable additivity on a
    finite sample space. Then computes P of specific events using
    additivity.

    Input format:
        ``verify probability measure and compute P(A)``

    Target format:
        ``Omega = {1,2,3,4}, P({1})=1/4, P({2})=1/4, P({3})=1/4, P({4})=1/4
        <step> P(Omega) = 1: yes <step> P(empty) = 0: yes <step>
        A = {1,3}, P(A) = P({1}) + P({3}) = 1/4 + 1/4 = 1/2``

    Difficulty scaling:
        Difficulty 1-3: uniform distribution on small set.
        Difficulty 4-6: non-uniform distribution.
        Difficulty 7-8: verify a non-probability measure (negative or sum != 1).

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "probability_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution complexity.

        Returns:
            Natural language description.
        """
        return "verify probability measure and compute P(A)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a probability measure problem.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Tuple of (measure_description, solution_data).
        """
        n = self._rng.randint(3, min(6, 2 + difficulty))
        elements = list(range(1, n + 1))

        if difficulty <= 3:
            # Uniform distribution
            probs = {e: Fraction(1, n) for e in elements}
            is_valid = True
        elif difficulty <= 6:
            # Non-uniform but valid
            probs = self._generate_valid_probs(elements)
            is_valid = True
        else:
            # Possibly invalid
            if self._rng.random() < 0.5:
                probs = self._generate_valid_probs(elements)
                is_valid = True
            else:
                probs = self._generate_invalid_probs(elements)
                is_valid = False

        # Choose event A
        k = self._rng.randint(1, max(1, n - 1))
        event_a = sorted(self._rng.sample(elements, k))
        p_a = sum(probs[e] for e in event_a)

        total = sum(probs.values())

        prob_str = ", ".join(f"P({{{e}}})={_fmt_frac(probs[e])}" for e in elements)
        problem = f"Omega={{{','.join(str(e) for e in elements)}}}, {prob_str}"
        return problem, {
            "elements": elements, "probs": probs,
            "is_valid": is_valid, "total": total,
            "event_a": event_a, "p_a": p_a,
        }

    def _generate_valid_probs(self, elements: list[int]) -> dict[int, Fraction]:
        """Generate valid probability weights summing to 1.

        Args:
            elements: List of sample space elements.

        Returns:
            Dict mapping element to probability.
        """
        n = len(elements)
        # Generate random integer weights and normalise
        weights = [self._rng.randint(1, 5) for _ in elements]
        total = sum(weights)
        return {e: Fraction(w, total) for e, w in zip(elements, weights)}

    def _generate_invalid_probs(self, elements: list[int]) -> dict[int, Fraction]:
        """Generate invalid probability weights (sum != 1 or negative).

        Args:
            elements: List of sample space elements.

        Returns:
            Dict mapping element to probability.
        """
        choice = self._rng.choice(["sum_wrong", "negative"])
        if choice == "sum_wrong":
            weights = [self._rng.randint(1, 5) for _ in elements]
            total = sum(weights)
            # Add 1 to denominator to make sum < 1
            return {e: Fraction(w, total + 1) for e, w in zip(elements, weights)}
        # negative
        probs = self._generate_valid_probs(elements)
        # Make one negative
        target = elements[0]
        probs[target] = -probs[target]
        return probs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate probability measure verification steps.

        Args:
            data: Solution data with probabilities and event.

        Returns:
            Steps showing axiom checks and event probability.
        """
        steps = []
        total = data["total"]
        steps.append(f"P(Omega) = {_fmt_frac(total)}: {'yes' if total == 1 else 'no, should be 1'}")

        all_nonneg = all(p >= 0 for p in data["probs"].values())
        steps.append(f"all P >= 0: {'yes' if all_nonneg else 'no'}")

        if data["is_valid"]:
            steps.append("valid probability measure")
        else:
            steps.append("NOT a valid probability measure")

        event_str = "{" + ",".join(str(e) for e in data["event_a"]) + "}"
        p_parts = " + ".join(
            f"P({{{e}}})={_fmt_frac(data['probs'][e])}" for e in data["event_a"]
        )
        steps.append(f"P({event_str}) = {p_parts} = {_fmt_frac(data['p_a'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the verification result and P(A).

        Args:
            data: Solution data.

        Returns:
            Answer string.
        """
        event_str = "{" + ",".join(str(e) for e in data["event_a"]) + "}"
        valid = "valid" if data["is_valid"] else "invalid"
        return f"{valid}; P({event_str})={_fmt_frac(data['p_a'])}"


# ── 6. Conditional expectation (tier 7) ──────────────────────────


@register
class ConditionalExpectationMeasureGenerator(StepGenerator):
    """Compute conditional expectation E[X|F] for a simple sigma-algebra.

    For a finite probability space with sub-sigma-algebra F, computes
    E[X|F] as the F-measurable function that equals the conditional
    average on each atom of F.

    Input format:
        ``compute E[X|F] on finite space``

    Target format:
        ``Omega = {1,2,3,4}, P uniform, X = (2,4,6,8) <step>
        F = {empty, {1,2}, {3,4}, Omega} <step>
        atom {1,2}: E[X|F] = (2+4)/(2) = 3 on {1,2} <step>
        atom {3,4}: E[X|F] = (6+8)/(2) = 7 on {3,4} <step>
        E[X|F] = (3, 3, 7, 7)``

    Difficulty scaling:
        Difficulty 1-3: 2 atoms, uniform probability.
        Difficulty 4-6: 2-3 atoms, non-uniform probability.
        Difficulty 7-8: 3-4 atoms, non-uniform.

    Prerequisites:
        sigma_algebra.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conditional_expectation_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sigma_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls space and sigma-algebra complexity.

        Returns:
            Natural language description.
        """
        return "compute conditional expectation E[X|F] on finite space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conditional expectation problem.

        Constructs a finite probability space, a sub-sigma-algebra F
        partitioning Omega into atoms, and a random variable X. Computes
        E[X|F] on each atom.

        Args:
            difficulty: Controls number of atoms and uniformity.

        Returns:
            Tuple of (space_description, solution_data).
        """
        if difficulty <= 3:
            n = 4
            n_atoms = 2
        elif difficulty <= 6:
            n = self._rng.choice([4, 6])
            n_atoms = self._rng.randint(2, 3)
        else:
            n = self._rng.choice([6, 8])
            n_atoms = self._rng.randint(3, min(4, n))

        elements = list(range(1, n + 1))

        # Generate probabilities
        if difficulty <= 3:
            probs = {e: Fraction(1, n) for e in elements}
        else:
            weights = [self._rng.randint(1, 4) for _ in elements]
            total = sum(weights)
            probs = {e: Fraction(w, total) for e, w in zip(elements, weights)}

        # Generate X values
        x_values = {e: Fraction(self._rng.randint(1, 10)) for e in elements}

        # Partition into atoms
        atoms = self._partition(elements, n_atoms)

        # Compute E[X|F] on each atom
        cond_exp = {}
        atom_results = []
        for atom in atoms:
            p_atom = sum(probs[e] for e in atom)
            if p_atom == 0:
                val = Fraction(0)
            else:
                val = sum(probs[e] * x_values[e] for e in atom) / p_atom
            for e in atom:
                cond_exp[e] = val
            atom_results.append({
                "atom": atom,
                "p_atom": p_atom,
                "value": val,
            })

        # Format problem
        x_str = ",".join(f"X({e})={_fmt_frac(x_values[e])}" for e in elements)
        p_str = ",".join(f"P({e})={_fmt_frac(probs[e])}" for e in elements)
        atom_str = "; ".join(
            "{" + ",".join(str(e) for e in a) + "}" for a in atoms
        )

        problem = f"Omega={{{','.join(str(e) for e in elements)}}}, {p_str}; {x_str}; F atoms: {atom_str}"
        return problem, {
            "elements": elements, "probs": probs,
            "x_values": x_values, "atoms": atoms,
            "atom_results": atom_results, "cond_exp": cond_exp,
        }

    def _partition(self, elements: list[int], n_parts: int) -> list[list[int]]:
        """Partition elements into n_parts roughly equal groups.

        Args:
            elements: List to partition.
            n_parts: Number of partitions.

        Returns:
            List of lists forming the partition.
        """
        shuffled = elements[:]
        self._rng.shuffle(shuffled)
        parts: list[list[int]] = [[] for _ in range(n_parts)]
        for i, e in enumerate(shuffled):
            parts[i % n_parts].append(e)
        return [sorted(p) for p in parts if p]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conditional expectation computation steps.

        Args:
            data: Solution data with atom results.

        Returns:
            Steps showing computation on each atom.
        """
        steps = []
        for ar in data["atom_results"]:
            atom_str = "{" + ",".join(str(e) for e in ar["atom"]) + "}"
            steps.append(
                f"atom {atom_str}: P(atom)={_fmt_frac(ar['p_atom'])}, "
                f"E[X|F]={_fmt_frac(ar['value'])}"
            )
        result_str = ",".join(
            _fmt_frac(data["cond_exp"][e]) for e in data["elements"]
        )
        steps.append(f"E[X|F] = ({result_str})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the conditional expectation values.

        Args:
            data: Solution data.

        Returns:
            Formatted conditional expectation.
        """
        result_str = ",".join(
            _fmt_frac(data["cond_exp"][e]) for e in data["elements"]
        )
        return f"E[X|F]=({result_str})"
