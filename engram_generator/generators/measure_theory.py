"""Measure theory generators for tiers 6-7.

8 generators covering sigma-algebras, measurable functions, Lebesgue
measure, simple function integration, dominated convergence, monotone
convergence, Fubini's theorem, and Borel sets. Each generator produces
step-by-step solutions with LaTeX formatting.
"""
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ───────────────────────────────────────────────


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


# ── 1. Sigma-algebra (tier 6) ───────────────────────────────────────


@register
class SigmaAlgebraGenerator(StepGenerator):
    """Verify whether a collection of subsets forms a sigma-algebra.

    Given a base set {1, ..., n} and a collection of subsets, checks
    three axioms: contains the empty set, closed under complement, and
    closed under finite union. Generates collections that either satisfy
    or violate one of these axioms.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sigma_algebra"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify if collection of subsets is a sigma-algebra"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sigma-algebra verification problem.

        Constructs a base set and a collection of subsets. For valid
        sigma-algebras, builds the trivial or power set algebra. For
        invalid ones, omits a complement or union.

        Args:
            difficulty: Controls base set size and collection complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(4, 1 + difficulty))
        base = set(range(1, n + 1))
        is_valid = self._rng.random() < 0.5

        if is_valid:
            collection = self._build_valid(base, difficulty)
            reason = "all axioms satisfied"
            failing_axiom = None
        else:
            collection, failing_axiom = self._build_invalid(base, difficulty)
            reason = f"fails: {failing_axiom}"

        base_str = "\\{" + ",".join(str(x) for x in sorted(base)) + "\\}"
        coll_strs = []
        for s in collection:
            if len(s) == 0:
                coll_strs.append("\\emptyset")
            else:
                coll_strs.append("\\{" + ",".join(str(x) for x in sorted(s)) + "\\}")
        coll_latex = "\\{" + ", ".join(coll_strs) + "\\}"

        problem = f"X={base_str}, \\mathcal{{F}}={coll_latex}"
        return problem, {
            "base": base, "collection": collection,
            "is_valid": is_valid, "reason": reason,
            "failing_axiom": failing_axiom,
        }

    def _build_valid(self, base: set, difficulty: int) -> list[frozenset]:
        """Build a valid sigma-algebra over the base set.

        Args:
            base: The base set.
            difficulty: Controls whether trivial or power set.

        Returns:
            List of frozensets forming a valid sigma-algebra.
        """
        if difficulty <= 3:
            return [frozenset(), frozenset(base)]
        # Power set for higher difficulty
        elements = sorted(base)
        result: list[frozenset] = []
        for mask in range(2 ** len(elements)):
            subset = frozenset(elements[i] for i in range(len(elements)) if mask & (1 << i))
            result.append(subset)
        return result

    def _build_invalid(self, base: set, difficulty: int) -> tuple[list[frozenset], str]:
        """Build an invalid collection missing one sigma-algebra axiom.

        Args:
            base: The base set.
            difficulty: Controls which axiom to violate.

        Returns:
            Tuple of (collection, failing_axiom_description).
        """
        choice = self._rng.choice(["no_empty", "no_complement", "no_union"])
        elements = sorted(base)

        if choice == "no_empty":
            a = frozenset(elements[:1])
            comp_a = frozenset(base - a)
            collection = [a, comp_a, frozenset(base)]
            return collection, "empty set not in collection"

        if choice == "no_complement":
            a = frozenset(elements[:1])
            collection = [frozenset(), a, frozenset(base)]
            return collection, f"complement of {set(a)} not in collection"

        # no_union
        a = frozenset(elements[:1])
        b_elems = elements[1:2] if len(elements) > 1 else elements[:1]
        b = frozenset(b_elems)
        comp_a = frozenset(base - a)
        comp_b = frozenset(base - b)
        collection = [frozenset(), a, comp_a, b, comp_b, frozenset(base)]
        return collection, f"union {set(a)} ∪ {set(b)} = {set(a | b)} not in collection"

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate sigma-algebra verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        has_empty = frozenset() in sd["collection"]
        steps = [f"empty set in F: {'yes' if has_empty else 'no'}"]

        if has_empty:
            steps.append("check complements and unions")

        if sd["is_valid"]:
            steps.append("all axioms satisfied")
        else:
            steps.append(sd["reason"])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the collection is a sigma-algebra.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        if sd["is_valid"]:
            return "yes, valid sigma-algebra"
        return f"no, {sd['failing_axiom']}"


# ── 2. Measurable function (tier 6) ─────────────────────────────────


@register
class MeasurableFunctionGenerator(StepGenerator):
    """Check if a function on a finite set is measurable.

    Given f: X -> R on a finite set X with sigma-algebra F, verifies
    that the preimage f^{-1}(B) is in F for each relevant subset B.
    Uses simple functions mapping small finite sets to integers.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "measurable_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sigma_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "check if function is measurable w.r.t. sigma-algebra"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a measurable function verification problem.

        Builds a small finite set, a sigma-algebra on it, and a
        function mapping elements to integers. Checks if all preimages
        of singletons belong to the sigma-algebra.

        Args:
            difficulty: Controls set size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(4, 1 + difficulty))
        base = list(range(1, n + 1))

        # Build sigma-algebra: power set for simplicity at low difficulty
        sigma = self._build_sigma(base, difficulty)

        # Define function
        codomain_vals = list(range(0, min(3, difficulty) + 1))
        mapping = {x: self._rng.choice(codomain_vals) for x in base}

        # Check measurability: preimage of each singleton value
        preimages: dict[int, frozenset] = {}
        for val in set(mapping.values()):
            pre = frozenset(x for x in base if mapping[x] == val)
            preimages[val] = pre

        is_measurable = all(pre in sigma for pre in preimages.values())
        failing_pre = None
        if not is_measurable:
            for val, pre in preimages.items():
                if pre not in sigma:
                    failing_pre = (val, pre)
                    break

        map_str = ", ".join(f"f({x})={mapping[x]}" for x in base)
        sigma_strs = []
        for s in sorted(sigma, key=lambda s: (len(s), tuple(sorted(s)))):
            if len(s) == 0:
                sigma_strs.append("\\emptyset")
            else:
                sigma_strs.append("\\{" + ",".join(str(x) for x in sorted(s)) + "\\}")

        problem = f"{map_str}; \\mathcal{{F}}=\\{{{', '.join(sigma_strs)}\\}}"
        return problem, {
            "mapping": mapping, "sigma": sigma,
            "preimages": preimages, "is_measurable": is_measurable,
            "failing_pre": failing_pre,
        }

    def _build_sigma(self, base: list, difficulty: int) -> set[frozenset]:
        """Build a sigma-algebra for the measurability check.

        At low difficulty returns the power set (always measurable).
        At higher difficulty returns a proper sub-sigma-algebra that
        may cause the function to fail measurability.

        Args:
            base: List of elements in X.
            difficulty: Controls sigma-algebra complexity.

        Returns:
            Set of frozensets forming a sigma-algebra.
        """
        base_set = frozenset(base)
        if difficulty <= 3:
            # Power set
            result: set[frozenset] = set()
            for mask in range(2 ** len(base)):
                subset = frozenset(base[i] for i in range(len(base)) if mask & (1 << i))
                result.add(subset)
            return result
        # Proper sub-sigma-algebra: {empty, A, A^c, X}
        split = self._rng.randint(1, max(1, len(base) - 1))
        a = frozenset(base[:split])
        comp_a = frozenset(base_set - a)
        return {frozenset(), a, comp_a, base_set}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate measurability verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = []
        for val, pre in sd["preimages"].items():
            in_sigma = pre in sd["sigma"]
            pre_str = set(sorted(pre)) if pre else "emptyset"
            steps.append(f"f^{{-1}}({{{val}}})={pre_str}, in F: {'yes' if in_sigma else 'no'}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the function is measurable.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        if sd["is_measurable"]:
            return "measurable"
        val, pre = sd["failing_pre"]
        return f"not measurable, f^{{-1}}({{{val}}})={set(sorted(pre))} not in F"


# ── 3. Lebesgue measure (tier 6) ────────────────────────────────────


@register
class LebesgueMeasureGenerator(StepGenerator):
    """Compute the Lebesgue measure of sets in R.

    Handles intervals, finite unions of disjoint intervals, and simple
    set-theoretic combinations. Uses m([a,b]) = b - a and additivity
    over disjoint unions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lebesgue_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["open_closed_sets"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute Lebesgue measure of set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lebesgue measure computation problem.

        Produces single intervals at low difficulty and disjoint unions
        at higher difficulty. All intervals have rational endpoints.

        Args:
            difficulty: Controls number of intervals.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._single_interval(difficulty)
        return self._disjoint_union(difficulty)

    def _single_interval(self, difficulty: int) -> tuple[str, dict]:
        """Generate a single interval measure problem.

        Args:
            difficulty: Controls endpoint range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = Fraction(self._rng.randint(-5, 5))
        length = Fraction(self._rng.randint(1, 3 + difficulty))
        b = a + length

        problem = f"m([{_fmt_frac(a)}, {_fmt_frac(b)}])"
        return problem, {
            "set_type": "single",
            "intervals": [(a, b)],
            "measure": length,
        }

    def _disjoint_union(self, difficulty: int) -> tuple[str, dict]:
        """Generate a disjoint union of intervals measure problem.

        Args:
            difficulty: Controls number of intervals.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_intervals = self._rng.randint(2, min(3, difficulty))
        intervals: list[tuple[Fraction, Fraction]] = []
        cursor = Fraction(self._rng.randint(0, 3))

        for _ in range(n_intervals):
            gap = Fraction(self._rng.randint(1, 3))
            cursor += gap
            a = cursor
            length = Fraction(self._rng.randint(1, 2 + difficulty))
            b = a + length
            intervals.append((a, b))
            cursor = b

        total = sum(b - a for a, b in intervals)
        parts = " \\cup ".join(
            f"[{_fmt_frac(a)}, {_fmt_frac(b)}]" for a, b in intervals
        )
        problem = f"m({parts})"
        return problem, {
            "set_type": "union",
            "intervals": intervals,
            "measure": total,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Lebesgue measure computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = []
        for a, b in sd["intervals"]:
            steps.append(f"m([{_fmt_frac(a)},{_fmt_frac(b)}]) = {_fmt_frac(b - a)}")
        if len(sd["intervals"]) > 1:
            steps.append(f"disjoint union: sum = {_fmt_frac(sd['measure'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Lebesgue measure.

        Args:
            sd: Solution data dictionary.

        Returns:
            Measure as a string.
        """
        return f"m={_fmt_frac(sd['measure'])}"


# ── 4. Simple function integral (tier 6) ────────────────────────────


@register
class SimpleFunctionIntegralGenerator(StepGenerator):
    """Integrate a simple function over a measurable set.

    A simple function has the form sum(a_i * 1_{A_i}) where the A_i
    are disjoint measurable sets. The integral is sum(a_i * m(A_i)).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simple_function_integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lebesgue_measure"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "integrate simple function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple function integration problem.

        Builds disjoint intervals with constant values on each, then
        computes the integral as the sum of value times measure.

        Args:
            difficulty: Controls number of pieces.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_pieces = self._rng.randint(2, min(4, 1 + difficulty))
        pieces: list[dict] = []
        cursor = Fraction(0)

        for _ in range(n_pieces):
            a = cursor
            length = Fraction(self._rng.randint(1, 2 + difficulty))
            b = a + length
            coeff = Fraction(self._rng.randint(1, 3 + difficulty))
            pieces.append({"a": a, "b": b, "coeff": coeff, "measure": length})
            cursor = b + Fraction(self._rng.randint(0, 2))

        integral = sum(p["coeff"] * p["measure"] for p in pieces)

        terms = " + ".join(
            f"{_fmt_frac(p['coeff'])} \\cdot 1_{{[{_fmt_frac(p['a'])},{_fmt_frac(p['b'])}]}}"
            for p in pieces
        )
        problem = f"\\int ({terms})\\,d\\mu"
        return problem, {
            "pieces": pieces,
            "integral": integral,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate integration steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = []
        for p in sd["pieces"]:
            val = p["coeff"] * p["measure"]
            steps.append(
                f"{_fmt_frac(p['coeff'])} * m([{_fmt_frac(p['a'])},"
                f"{_fmt_frac(p['b'])}]) = {_fmt_frac(p['coeff'])} * "
                f"{_fmt_frac(p['measure'])} = {_fmt_frac(val)}"
            )
        steps.append(f"sum = {_fmt_frac(sd['integral'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the integral value.

        Args:
            sd: Solution data dictionary.

        Returns:
            Integral as a string.
        """
        return f"integral={_fmt_frac(sd['integral'])}"


# ── 5. Dominated convergence theorem (tier 7) ───────────────────────


@register
class DominatedConvergenceGenerator(StepGenerator):
    """Apply the Dominated Convergence Theorem.

    Given a sequence f_n converging pointwise to f with |f_n| <= g
    and integral(g) < infinity, concludes that integral(f_n) converges
    to integral(f). Uses template-based problems with concrete
    dominating functions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dominated_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

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
        return "apply dominated convergence theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DCT application problem.

        Selects from template families of function sequences with
        known pointwise limits and explicit dominating functions.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        template = self._rng.choice(["exp_decay", "rational", "sin_over_n"])

        if template == "exp_decay":
            return self._exp_decay(difficulty)
        if template == "rational":
            return self._rational(difficulty)
        return self._sin_over_n(difficulty)

    def _exp_decay(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n(x) = x^a * e^{-nx} on [0, inf), a >= 0.

        Pointwise limit: 0. Dominated by g(x) = x^a * e^{-x}.
        integral(f_n) = Gamma(a+1)/n^{a+1}.

        Args:
            difficulty: Controls exponent a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(0, min(3, difficulty))
        limit_integral = 0.0
        problem = (
            f"f_n(x) = x^{{{a}}}e^{{-nx}} on [0,\\infty), "
            f"g(x) = x^{{{a}}}e^{{-x}}"
        )
        return problem, {
            "template": "exp_decay", "a": a,
            "fn_latex": f"x^{a}e^{{-nx}}",
            "limit_fn": "0",
            "dominator": f"x^{a}e^{{-x}}",
            "dom_integrable": True,
            "limit_integral": limit_integral,
        }

    def _rational(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n(x) = x/(1+nx^2) on [0,1].

        Pointwise limit: 0. |f_n(x)| <= 1/(2*sqrt(n)) <= x for large n.
        Dominated by g(x) = x. integral(g) = 1/2.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = (
            "f_n(x) = \\frac{x}{1+nx^2} on [0,1], "
            "g(x) = x"
        )
        return problem, {
            "template": "rational",
            "fn_latex": "x/(1+nx^2)",
            "limit_fn": "0",
            "dominator": "x",
            "dom_integrable": True,
            "limit_integral": 0.0,
        }

    def _sin_over_n(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n(x) = sin(x/n) on [0, pi].

        Pointwise limit: 0. |sin(x/n)| <= 1. Dominated by g(x) = 1.
        integral(g) = pi.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = (
            "f_n(x) = \\sin(x/n) on [0,\\pi], "
            "g(x) = 1"
        )
        return problem, {
            "template": "sin_over_n",
            "fn_latex": "sin(x/n)",
            "limit_fn": "0",
            "dominator": "1",
            "dom_integrable": True,
            "limit_integral": 0.0,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate DCT application steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"f_n -> {sd['limit_fn']} pointwise",
            f"|f_n| <= g = {sd['dominator']}",
            f"integral(g) < inf: {'yes' if sd['dom_integrable'] else 'no'}",
            "DCT applies: lim integral(f_n) = integral(lim f_n)",
            f"= integral({sd['limit_fn']}) = {_fmt(sd['limit_integral'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the limit of the integrals.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"lim integral(f_n)={_fmt(sd['limit_integral'])}"


# ── 6. Monotone convergence theorem (tier 7) ────────────────────────


@register
class MonotoneConvergenceGenerator(StepGenerator):
    """Apply the Monotone Convergence Theorem.

    Given 0 <= f_1 <= f_2 <= ... with pointwise limit f, computes
    lim integral(f_n) = integral(f). Uses concrete increasing sequences
    with known integrals.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "monotone_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

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
        return "apply monotone convergence theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an MCT application problem.

        Selects from template families of non-decreasing non-negative
        function sequences with known limits.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        template = self._rng.choice(["indicator", "truncation", "power"])

        if template == "indicator":
            return self._indicator(difficulty)
        if template == "truncation":
            return self._truncation(difficulty)
        return self._power(difficulty)

    def _indicator(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n = 1_{[0,n]} increasing to 1_{[0,inf)}.

        integral(f_n) = n -> inf. Limit integral = inf.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "f_n(x) = 1_{[0,n]} on [0,\\infty)"
        return problem, {
            "template": "indicator",
            "fn_latex": "1_{[0,n]}",
            "limit_fn": "1_{[0,inf)}",
            "limit_integral": "inf",
            "monotone": True,
            "nonneg": True,
        }

    def _truncation(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n = min(f, n) for f(x) = 1/sqrt(x) on (0,1].

        integral(f) = 2. f_n increases to f, integral(f_n) -> 2.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = (
            "f_n(x) = \\min(1/\\sqrt{x}, n) on (0,1], "
            "f(x) = 1/\\sqrt{x}"
        )
        return problem, {
            "template": "truncation",
            "fn_latex": "min(1/sqrt(x), n)",
            "limit_fn": "1/sqrt(x)",
            "limit_integral": "2",
            "monotone": True,
            "nonneg": True,
        }

    def _power(self, difficulty: int) -> tuple[str, dict]:
        """Generate f_n(x) = x * (1 - x^n) on [0,1].

        0 <= f_1 <= f_2 <= ..., limit f(x) = x on [0,1).
        integral(f) = 1/2.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "f_n(x) = x(1-x^{n}) on [0,1]"
        return problem, {
            "template": "power",
            "fn_latex": "x(1-x^n)",
            "limit_fn": "x on [0,1)",
            "limit_integral": "1/2",
            "monotone": True,
            "nonneg": True,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate MCT application steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"f_n = {sd['fn_latex']}",
            f"0 <= f_1 <= f_2 <= ...: {'yes' if sd['monotone'] else 'no'}",
            f"non-negative: {'yes' if sd['nonneg'] else 'no'}",
            f"pointwise limit: {sd['limit_fn']}",
            "MCT: lim integral(f_n) = integral(lim f_n)",
            f"= {sd['limit_integral']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the limit integral.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"lim integral(f_n)={sd['limit_integral']}"


# ── 7. Fubini computation (tier 7) ──────────────────────────────────


@register
class FubiniComputeGenerator(StepGenerator):
    """Apply Fubini's theorem to compute double integrals.

    Computes a double integral over a rectangle by switching the order
    of integration. Uses simple polynomial integrands where both orders
    yield the same result, verifying Fubini's theorem.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fubini_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute double integral using Fubini's theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fubini double integral problem.

        Creates an integrand of the form c * x^a * y^b over the
        rectangle [0, p] x [0, q]. Computes the integral both ways.

        Args:
            difficulty: Controls exponents and bounds.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(0, min(3, difficulty))
        b = self._rng.randint(0, min(3, difficulty))
        c = Fraction(self._rng.randint(1, 2 + difficulty))
        p = Fraction(self._rng.randint(1, min(3, 1 + difficulty)))
        q = Fraction(self._rng.randint(1, min(3, 1 + difficulty)))

        # integral of c * x^a * y^b over [0,p]x[0,q]
        # = c * p^{a+1}/(a+1) * q^{b+1}/(b+1)
        x_integral = c * (p ** (a + 1)) / Fraction(a + 1)
        result = x_integral * (q ** (b + 1)) / Fraction(b + 1)

        integrand = f"{_fmt_frac(c)}x^{{{a}}}y^{{{b}}}"
        problem = (
            f"\\int_0^{{{_fmt_frac(q)}}} \\int_0^{{{_fmt_frac(p)}}} "
            f"{integrand}\\,dx\\,dy"
        )
        return problem, {
            "a": a, "b": b, "c": c, "p": p, "q": q,
            "integrand": integrand, "result": result,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Fubini computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        a, b, c, p, q = sd["a"], sd["b"], sd["c"], sd["p"], sd["q"]
        inner_x = c * (p ** (a + 1)) / Fraction(a + 1)
        inner_y = c * (q ** (b + 1)) / Fraction(b + 1)

        return [
            "Fubini: switch order of integration",
            f"inner x: int_0^{_fmt_frac(p)} {_fmt_frac(c)}x^{a} dx = {_fmt_frac(inner_x)}",
            f"outer y: int_0^{_fmt_frac(q)} {_fmt_frac(inner_x)}*y^{b} dy = {_fmt_frac(sd['result'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the double integral value.

        Args:
            sd: Solution data dictionary.

        Returns:
            Integral value as a string.
        """
        return f"integral={_fmt_frac(sd['result'])}"


# ── 8. Borel set (tier 6) ───────────────────────────────────────────


@register
class BorelSetGenerator(StepGenerator):
    """Identify whether a set is a Borel set.

    A Borel set is any set constructible from open sets via countable
    unions, countable intersections, and complements. Generates sets
    described in natural language and determines their Borel status with
    a construction proof.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "borel_set"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["open_closed_sets"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "determine if set is a Borel set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Borel set identification problem.

        Selects from a catalog of common sets in R with known Borel
        status and construction paths.

        Args:
            difficulty: Controls set complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            return self._open_interval()
        if difficulty <= 4:
            return self._closed_interval()
        if difficulty <= 6:
            return self._singleton_or_countable()
        return self._gdelta_or_fsigma()

    def _open_interval(self) -> tuple[str, dict]:
        """Generate an open interval Borel check.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(-5, 5)
        b = a + self._rng.randint(1, 5)
        problem = f"S = ({a}, {b})"
        return problem, {
            "set_desc": f"({a},{b})",
            "is_borel": True,
            "construction": "open set, hence Borel",
            "set_type": "open",
        }

    def _closed_interval(self) -> tuple[str, dict]:
        """Generate a closed interval Borel check.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(-5, 5)
        b = a + self._rng.randint(1, 5)
        problem = f"S = [{a}, {b}]"
        return problem, {
            "set_desc": f"[{a},{b}]",
            "is_borel": True,
            "construction": "closed = complement of open, hence Borel",
            "set_type": "closed",
        }

    def _singleton_or_countable(self) -> tuple[str, dict]:
        """Generate a singleton or countable set Borel check.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        choice = self._rng.choice(["singleton", "rationals", "integers"])

        if choice == "singleton":
            x = self._rng.randint(-10, 10)
            problem = f"S = \\{{{x}\\}}"
            construction = f"{{{x}}} = intersection of (x-1/n, x+1/n), countable intersection of open"
        elif choice == "rationals":
            problem = "S = \\mathbb{Q}"
            construction = "Q = countable union of singletons, each Borel"
        else:
            problem = "S = \\mathbb{Z}"
            construction = "Z = countable union of singletons, each Borel"

        return problem, {
            "set_desc": choice,
            "is_borel": True,
            "construction": construction,
            "set_type": "countable",
        }

    def _gdelta_or_fsigma(self) -> tuple[str, dict]:
        """Generate a G-delta or F-sigma set Borel check.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        choice = self._rng.choice(["irrationals", "cantor"])

        if choice == "irrationals":
            problem = "S = \\mathbb{R} \\setminus \\mathbb{Q}"
            construction = "complement of Q (F-sigma), so G-delta, hence Borel"
        else:
            problem = "S = \\text{Cantor set}"
            construction = "closed subset of [0,1], hence Borel"

        return problem, {
            "set_desc": choice,
            "is_borel": True,
            "construction": construction,
            "set_type": "gdelta_fsigma",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Borel set identification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"set type: {sd['set_type']}",
            sd["construction"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the set is Borel.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        if sd["is_borel"]:
            return "yes, Borel"
        return "not Borel"
