"""Extended real and complex analysis generators for tiers 5-6.

Provides 10 generators covering Bolzano-Weierstrass, Weierstrass M-test,
Abel summation, integral test, lim sup / lim inf, contraction mapping,
Riemann sums, squeeze theorem, mean value theorem, and extended
L'Hopital's rule.
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


# ── 1. Bolzano-Weierstrass (tier 6) ─────────────────────────────────


@register
class BolzanoWeierstrassGenerator(StepGenerator):
    """Apply the Bolzano-Weierstrass theorem to extract a convergent subsequence.

    Given a bounded sequence, identifies a monotone subsequence and
    shows convergence using the monotone convergence theorem.

    Input format:
        ``apply Bolzano-Weierstrass to find convergent subsequence``

    Target format:
        ``a_n = (-1)^n*(1-1/n), bounded by [-1,1] <step>
        even terms: a_{2k} = 1-1/(2k), increasing, bounded above
        <step> converges to 1``

    Difficulty scaling:
        Difficulty 1-3: a_n = (-1)^n / n, simple oscillation.
        Difficulty 4-6: a_n = (-1)^n * (1-1/n).
        Difficulty 7-8: a_n = sin(n) / n + cos(n).

    Prerequisites:
        supremum_infimum (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bolzano_weierstrass"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["supremum_infimum"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls sequence complexity.

        Returns:
            Natural language description.
        """
        return "apply Bolzano-Weierstrass to find convergent subsequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bolzano-Weierstrass problem.

        Args:
            difficulty: Controls sequence type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._osc_decay(difficulty)
        if difficulty <= 6:
            return self._osc_approach(difficulty)
        return self._trig_bounded(difficulty)

    def _osc_decay(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = (-1)^n / n problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "a_n = (-1)^n / n"
        return problem, {
            "seq_type": "osc_decay",
            "bound": "[-1, 1]",
            "subseq": "a_{2k} = 1/(2k), decreasing",
            "limit": 0.0,
        }

    def _osc_approach(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = (-1)^n * (1 - 1/n) problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "a_n = (-1)^n(1-1/n)"
        return problem, {
            "seq_type": "osc_approach",
            "bound": "[-1, 1]",
            "subseq": "a_{2k} = 1-1/(2k), increasing, bounded by 1",
            "limit": 1.0,
        }

    def _trig_bounded(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = cos(n*pi/k) for chosen k problem.

        Args:
            difficulty: Controls k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(2, 5)
        # cos(n*pi/k) is bounded in [-1,1]
        # Subsequence n = 2mk gives a_{2mk} = cos(2m*pi) = 1
        problem = f"a_n = \\cos(n\\pi/{k})"
        return problem, {
            "seq_type": "trig",
            "bound": "[-1, 1]",
            "subseq": f"a_{{n={2*k}m}} = cos(2m*pi) = 1, constant",
            "limit": 1.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bolzano-Weierstrass application steps.

        Args:
            data: Solution data with bound and subsequence.

        Returns:
            Steps showing boundedness and convergent subsequence.
        """
        return [
            f"sequence bounded in {data['bound']}",
            "by Bolzano-Weierstrass, convergent subsequence exists",
            f"subsequence: {data['subseq']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the subsequence limit.

        Args:
            data: Solution data.

        Returns:
            Limit of the convergent subsequence.
        """
        return f"subsequence converges to {_fmt(data['limit'])}"


# ── 2. Weierstrass M-test (tier 6) ──────────────────────────────────


@register
class WeierstrrassMTestGenerator(StepGenerator):
    """Apply the Weierstrass M-test for uniform convergence of series.

    If |f_n(x)| <= M_n for all x and sum M_n converges, then
    sum f_n converges uniformly.

    Input format:
        ``apply Weierstrass M-test for uniform convergence``

    Target format:
        ``sum x^n/n^2 on [-1,1] <step>
        |x^n/n^2| <= 1/n^2 = M_n <step>
        sum 1/n^2 = pi^2/6, converges
        <step> uniform convergence by M-test``

    Difficulty scaling:
        Difficulty 1-3: sum x^n / n^p with p > 1.
        Difficulty 4-6: sum sin(nx) / n^2.
        Difficulty 7-8: sum x^n / (2^n * n).

    Prerequisites:
        series_convergence (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weierstrass_mtest"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls series complexity.

        Returns:
            Natural language description.
        """
        return "apply Weierstrass M-test for uniform convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Weierstrass M-test problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._power_p(difficulty)
        if difficulty <= 6:
            return self._trig_series(difficulty)
        return self._geometric_log(difficulty)

    def _power_p(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum x^n/n^p on [-1,1].

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(2, 4)
        problem = f"\\sum x^n/n^{{{p}}} on [-1,1]"
        return problem, {
            "series_type": "power_p", "p": p,
            "bound": f"|x^n/n^{p}| <= 1/n^{p}",
            "M_n": f"1/n^{p}",
            "M_converges": f"sum 1/n^{p} converges (p={p}>1)",
            "uniform": True,
        }

    def _trig_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum sin(nx)/n^2 on R.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\sin(nx)/n^2 on \\mathbb{R}"
        return problem, {
            "series_type": "trig",
            "bound": "|sin(nx)/n^2| <= 1/n^2",
            "M_n": "1/n^2",
            "M_converges": "sum 1/n^2 = pi^2/6, converges",
            "uniform": True,
        }

    def _geometric_log(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum x^n/(2^n * n) on [-1,1].

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum x^n/(2^n n) on [-1,1]"
        return problem, {
            "series_type": "geom_log",
            "bound": "|x^n/(2^n*n)| <= 1/(2^n*n) <= 1/2^n",
            "M_n": "1/2^n",
            "M_converges": "sum 1/2^n = 1, converges (geometric)",
            "uniform": True,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Weierstrass M-test application steps.

        Args:
            data: Solution data with bounds and convergence.

        Returns:
            Steps showing bound, M_n, and conclusion.
        """
        return [
            data["bound"],
            f"M_n = {data['M_n']}",
            data["M_converges"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return uniform convergence verdict.

        Args:
            data: Solution data.

        Returns:
            Verdict string.
        """
        if data["uniform"]:
            return "uniformly convergent by M-test"
        return "M-test inconclusive"


# ── 3. Abel summation (tier 6) ──────────────────────────────────────


@register
class AbelSummationGenerator(StepGenerator):
    """Apply Abel's test for convergence of sum a_n * b_n.

    If {a_n} is monotone decreasing with a_n -> 0 and the partial
    sums of b_n are bounded, then sum a_n*b_n converges.

    Input format:
        ``apply Abel's test for series convergence``

    Target format:
        ``sum (-1)^n / n <step> a_n = 1/n decreasing to 0
        <step> b_n = (-1)^n, partial sums bounded by 1
        <step> converges by Abel's test``

    Difficulty scaling:
        Difficulty 1-3: sum (-1)^n / n.
        Difficulty 4-6: sum cos(n*theta) / n.
        Difficulty 7-8: sum sin(n) / n.

    Prerequisites:
        series_convergence (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "abel_summation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["series_convergence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls series complexity.

        Returns:
            Natural language description.
        """
        return "apply Abel's test for series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Abel summation test problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._alternating(difficulty)
        if difficulty <= 6:
            return self._cos_series(difficulty)
        return self._sin_series(difficulty)

    def _alternating(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum (-1)^n / n^p problem.

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.choice([1, 2])
        if p == 1:
            problem = "\\sum (-1)^n / n"
        else:
            problem = f"\\sum (-1)^n / n^{{{p}}}"
        return problem, {
            "series_type": "alternating", "p": p,
            "a_n": f"1/n^{p}", "a_n_prop": "decreasing to 0",
            "b_n": "(-1)^n", "b_n_bound": "partial sums bounded by 1",
        }

    def _cos_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum cos(n*theta)/n for theta != 0 mod 2pi.

        Args:
            difficulty: Controls theta.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        theta_num = self._rng.randint(1, 5)
        theta_den = self._rng.randint(2, 6)
        theta_str = f"{theta_num}\\pi/{theta_den}"
        problem = f"\\sum \\cos(n \\cdot {theta_str}) / n"
        return problem, {
            "series_type": "cos",
            "a_n": "1/n", "a_n_prop": "decreasing to 0",
            "b_n": f"cos(n*{theta_str})",
            "b_n_bound": "partial sums bounded (Dirichlet kernel bound)",
        }

    def _sin_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum sin(n)/n problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\sum \\sin(n) / n"
        return problem, {
            "series_type": "sin",
            "a_n": "1/n", "a_n_prop": "decreasing to 0",
            "b_n": "sin(n)",
            "b_n_bound": "partial sums bounded by 1/|sin(1/2)|",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Abel test application steps.

        Args:
            data: Solution data with sequence properties.

        Returns:
            Steps showing a_n, b_n properties and conclusion.
        """
        return [
            f"a_n = {data['a_n']}, {data['a_n_prop']}",
            f"b_n = {data['b_n']}, {data['b_n_bound']}",
            "conditions of Abel's test satisfied",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return convergence verdict.

        Args:
            data: Solution data.

        Returns:
            Convergence result.
        """
        return "converges by Abel's test"


# ── 4. Integral test (tier 6) ───────────────────────────────────────


@register
class IntegralTestGenerator(StepGenerator):
    """Apply the integral test for series convergence.

    If f is positive and decreasing on [1, inf), then sum f(n)
    converges iff integral_1^inf f(x) dx converges.

    Input format:
        ``apply integral test for series convergence``

    Target format:
        ``sum 1/n^p <step> f(x) = 1/x^p, positive, decreasing
        <step> int_1^inf 1/x^p dx = [x^{1-p}/(1-p)]_1^inf
        <step> converges iff p > 1``

    Difficulty scaling:
        Difficulty 1-3: sum 1/n^p for integer p.
        Difficulty 4-6: sum 1/(n*ln(n)^p).
        Difficulty 7-8: sum 1/(n*ln(n)*ln(ln(n))^p).

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integral_test"

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
            difficulty: Controls series complexity.

        Returns:
            Natural language description.
        """
        return "apply integral test for series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integral test problem.

        Args:
            difficulty: Controls series type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._p_series(difficulty)
        if difficulty <= 6:
            return self._log_series(difficulty)
        return self._loglog_series(difficulty)

    def _p_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum 1/n^p integral test.

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(1, 4)
        converges = p > 1
        if converges:
            int_value = 1.0 / (p - 1)
            int_result = f"1/{p-1}"
        else:
            int_value = float("inf")
            int_result = "inf (diverges)"
        problem = f"\\sum_{{n=1}}^{{\\infty}} 1/n^{{{p}}}"
        return problem, {
            "series_type": "p_series", "p": p,
            "f": f"1/x^{p}",
            "integral": f"int_1^inf 1/x^{p} dx",
            "int_result": int_result,
            "converges": converges,
        }

    def _log_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum 1/(n*ln(n)^p) for n >= 2.

        Converges iff p > 1.

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(1, 3)
        converges = p > 1
        if converges:
            int_result = f"1/((p-1)*ln(2)^{{{p-1}}})"
        else:
            int_result = "ln(ln(x)) -> inf, diverges"
        problem = f"\\sum_{{n=2}}^{{\\infty}} 1/(n \\ln^{{{p}}}(n))"
        return problem, {
            "series_type": "log_series", "p": p,
            "f": f"1/(x*ln^{p}(x))",
            "integral": f"int_2^inf 1/(x*ln^{p}(x)) dx",
            "int_result": int_result,
            "converges": converges,
        }

    def _loglog_series(self, difficulty: int) -> tuple[str, dict]:
        """Generate sum 1/(n*ln(n)*ln(ln(n))^p) for n >= 3.

        Converges iff p > 1.

        Args:
            difficulty: Controls p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(1, 3)
        converges = p > 1
        int_result = "converges" if converges else "diverges"
        problem = (f"\\sum_{{n=3}}^{{\\infty}} "
                   f"1/(n \\ln(n) \\ln^{{{p}}}(\\ln(n)))")
        return problem, {
            "series_type": "loglog", "p": p,
            "f": f"1/(x*ln(x)*ln^{p}(ln(x)))",
            "integral": f"int_3^inf f(x) dx",
            "int_result": int_result,
            "converges": converges,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate integral test application steps.

        Args:
            data: Solution data with function and integral.

        Returns:
            Steps showing f, positivity, integral evaluation.
        """
        return [
            f"f(x) = {data['f']}, positive and decreasing",
            f"{data['integral']}",
            f"= {data['int_result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return convergence verdict.

        Args:
            data: Solution data.

        Returns:
            'converges' or 'diverges'.
        """
        return "converges" if data["converges"] else "diverges"


# ── 5. Lim sup / lim inf (tier 5) ───────────────────────────────────


@register
class LimSupLimInfGenerator(StepGenerator):
    """Compute lim sup and lim inf of an oscillating sequence.

    lim sup a_n = inf_{n>=1} sup_{k>=n} a_k.
    lim inf a_n = sup_{n>=1} inf_{k>=n} a_k.

    Input format:
        ``find lim sup and lim inf of sequence``

    Target format:
        ``a_n = (-1)^n*(1+1/n) <step>
        even terms: (1+1/n) -> 1 from above
        <step> odd terms: -(1+1/n) -> -1 from below
        <step> lim sup = 1, lim inf = -1``

    Difficulty scaling:
        Difficulty 1-3: a_n = (-1)^n.
        Difficulty 4-6: a_n = (-1)^n * (1 + 1/n).
        Difficulty 7-8: a_n = sin(n*pi/k) for various k.

    Prerequisites:
        supremum_infimum (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "limsup_liminf"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["supremum_infimum"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls sequence complexity.

        Returns:
            Natural language description.
        """
        return "find lim sup and lim inf of sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lim sup/lim inf problem.

        Args:
            difficulty: Controls sequence type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._simple_osc(difficulty)
        if difficulty <= 6:
            return self._osc_decay(difficulty)
        return self._mod_osc(difficulty)

    def _simple_osc(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = (-1)^n * c problem.

        Args:
            difficulty: Controls c.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(1, 5)
        problem = f"a_n = (-1)^n \\cdot {c}"
        return problem, {
            "seq_type": "simple",
            "even_desc": f"even terms: {c}",
            "odd_desc": f"odd terms: -{c}",
            "limsup": float(c),
            "liminf": float(-c),
        }

    def _osc_decay(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = (-1)^n * (1 + 1/n) problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "a_n = (-1)^n (1 + 1/n)"
        return problem, {
            "seq_type": "osc_decay",
            "even_desc": "even: 1+1/n -> 1 from above",
            "odd_desc": "odd: -(1+1/n) -> -1 from below",
            "limsup": 1.0,
            "liminf": -1.0,
        }

    def _mod_osc(self, difficulty: int) -> tuple[str, dict]:
        """Generate a_n = (-1)^n * n / (n+1) problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "a_n = (-1)^n \\cdot n/(n+1)"
        return problem, {
            "seq_type": "mod_osc",
            "even_desc": "even: n/(n+1) -> 1 from below",
            "odd_desc": "odd: -n/(n+1) -> -1 from above",
            "limsup": 1.0,
            "liminf": -1.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lim sup/lim inf computation steps.

        Args:
            data: Solution data with subsequence descriptions.

        Returns:
            Steps showing even/odd analysis and result.
        """
        return [
            data["even_desc"],
            data["odd_desc"],
            f"lim sup = {_fmt(data['limsup'])}",
            f"lim inf = {_fmt(data['liminf'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return lim sup and lim inf.

        Args:
            data: Solution data.

        Returns:
            Formatted lim sup and lim inf.
        """
        return (f"lim sup = {_fmt(data['limsup'])}, "
                f"lim inf = {_fmt(data['liminf'])}")


# ── 6. Contraction mapping (tier 6) ─────────────────────────────────


@register
class ContractionMappingGenerator(StepGenerator):
    """Apply the Banach fixed point theorem via contraction mapping.

    Given f with |f(x) - f(y)| <= c|x - y| and c < 1, finds the
    fixed point by iterating x_{n+1} = f(x_n).

    Input format:
        ``find fixed point by contraction mapping``

    Target format:
        ``f(x) = x/2 + 1, c = 1/2 < 1 <step>
        x_0 = 0, x_1 = 1, x_2 = 1.5, x_3 = 1.75
        <step> converges to x* = 2``

    Difficulty scaling:
        Difficulty 1-3: f(x) = x/a + b, clear contraction.
        Difficulty 4-6: f(x) = cos(x), contraction on [0,1].
        Difficulty 7-8: f(x) = (x + a/x)/2, Babylonian method.

    Prerequisites:
        cauchy_sequence (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "contraction_mapping"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cauchy_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mapping complexity.

        Returns:
            Natural language description.
        """
        return "find fixed point by contraction mapping"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a contraction mapping fixed point problem.

        Args:
            difficulty: Controls mapping type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_contraction(difficulty)
        if difficulty <= 6:
            return self._cos_contraction(difficulty)
        return self._babylonian(difficulty)

    def _linear_contraction(self, difficulty: int) -> tuple[str, dict]:
        """Generate f(x) = x/a + b contraction.

        Fixed point: x* = b / (1 - 1/a) = ab / (a-1).

        Args:
            difficulty: Controls a and b.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 5)
        b = self._rng.randint(1, 4)
        c = 1.0 / a  # Contraction constant
        fixed_pt = a * b / (a - 1.0)
        x0 = 0.0
        iterations = []
        x = x0
        for _ in range(4):
            x = x / a + b
            iterations.append(round(x, 4))
        problem = f"f(x) = x/{a} + {b}"
        return problem, {
            "map_type": "linear", "c": c,
            "x0": x0, "iterations": iterations,
            "fixed_pt": fixed_pt,
        }

    def _cos_contraction(self, difficulty: int) -> tuple[str, dict]:
        """Generate f(x) = cos(x) contraction on [0, 1].

        Fixed point ~ 0.7391 (Dottie number).

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        x0 = 0.5
        iterations = []
        x = x0
        for _ in range(5):
            x = math.cos(x)
            iterations.append(round(x, 4))
        problem = "f(x) = \\cos(x) on [0, 1]"
        return problem, {
            "map_type": "cos", "c": 0.8415,
            "x0": x0, "iterations": iterations,
            "fixed_pt": round(iterations[-1], 4),
        }

    def _babylonian(self, difficulty: int) -> tuple[str, dict]:
        """Generate f(x) = (x + a/x)/2 Babylonian sqrt method.

        Converges to sqrt(a).

        Args:
            difficulty: Controls a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 10)
        x0 = float(a)
        iterations = []
        x = x0
        for _ in range(4):
            x = (x + a / x) / 2.0
            iterations.append(round(x, 4))
        fixed_pt = math.sqrt(a)
        problem = f"f(x) = (x + {a}/x)/2"
        return problem, {
            "map_type": "babylonian", "a": a,
            "c": 0.5, "x0": x0,
            "iterations": iterations,
            "fixed_pt": round(fixed_pt, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate contraction mapping iteration steps.

        Args:
            data: Solution data with iterations.

        Returns:
            Steps showing contraction constant and iterations.
        """
        iter_str = ", ".join(_fmt(v) for v in data["iterations"])
        return [
            f"contraction constant c = {_fmt(data['c'])} < 1",
            f"x_0 = {_fmt(data['x0'])}",
            f"iterations: {iter_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fixed point.

        Args:
            data: Solution data.

        Returns:
            Fixed point value.
        """
        return f"x* = {_fmt(data['fixed_pt'])}"


# ── 7. Riemann sum (tier 5) ─────────────────────────────────────────


@register
class RiemannSumGenerator(StepGenerator):
    """Compute Riemann sums and compare with the exact integral.

    Evaluates left, right, or midpoint Riemann sums for f on [a,b]
    with n subintervals.

    Input format:
        ``compute Riemann sum and compare to exact integral``

    Target format:
        ``f(x) = x^2 on [0,1], n=4, left <step>
        dx = 0.25, x_i = {0, 0.25, 0.5, 0.75}
        <step> sum = 0.25*(0 + 0.0625 + 0.25 + 0.5625) = 0.2188
        <step> exact = 1/3 = 0.3333, error = 0.1146``

    Difficulty scaling:
        Difficulty 1-3: f(x) = x on [0,1], n = 2-4.
        Difficulty 4-6: f(x) = x^2, n = 4-6.
        Difficulty 7-8: f(x) = sin(x), n = 4-8.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "riemann_sum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function and partition.

        Returns:
            Natural language description.
        """
        return "compute Riemann sum and compare to exact integral"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Riemann sum problem.

        Args:
            difficulty: Controls function, n, and method.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        method = self._rng.choice(["left", "right", "midpoint"])
        if difficulty <= 3:
            return self._linear_riemann(difficulty, method)
        if difficulty <= 6:
            return self._quadratic_riemann(difficulty, method)
        return self._trig_riemann(difficulty, method)

    def _linear_riemann(self, difficulty: int, method: str) -> tuple[str, dict]:
        """Generate Riemann sum for f(x) = x on [0, b].

        Args:
            difficulty: Controls n.
            method: left, right, or midpoint.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        b = self._rng.randint(1, 3)
        n = self._rng.randint(2, 4)
        dx = b / n
        exact = b * b / 2.0
        total = self._compute_sum(lambda x: x, 0, b, n, method)
        problem = f"f(x) = x on [0,{b}], n={n}, {method}"
        return problem, {
            "f_str": "x", "a": 0, "b": b, "n": n,
            "method": method, "dx": dx,
            "riemann": total, "exact": exact,
            "error": abs(exact - total),
        }

    def _quadratic_riemann(self, difficulty: int,
                           method: str) -> tuple[str, dict]:
        """Generate Riemann sum for f(x) = x^2 on [0, b].

        Args:
            difficulty: Controls n.
            method: left, right, or midpoint.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        b = self._rng.randint(1, 2)
        n = self._rng.randint(4, 6)
        dx = b / n
        exact = b ** 3 / 3.0
        total = self._compute_sum(lambda x: x * x, 0, b, n, method)
        problem = f"f(x) = x^2 on [0,{b}], n={n}, {method}"
        return problem, {
            "f_str": "x^2", "a": 0, "b": b, "n": n,
            "method": method, "dx": dx,
            "riemann": total, "exact": exact,
            "error": abs(exact - total),
        }

    def _trig_riemann(self, difficulty: int,
                      method: str) -> tuple[str, dict]:
        """Generate Riemann sum for f(x) = sin(x) on [0, pi].

        Args:
            difficulty: Controls n.
            method: left, right, or midpoint.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(4, 8)
        a_val = 0.0
        b_val = math.pi
        dx = (b_val - a_val) / n
        exact = 2.0  # integral of sin from 0 to pi
        total = self._compute_sum(math.sin, a_val, b_val, n, method)
        problem = f"f(x) = \\sin(x) on [0,\\pi], n={n}, {method}"
        return problem, {
            "f_str": "sin(x)", "a": a_val, "b": b_val, "n": n,
            "method": method, "dx": dx,
            "riemann": total, "exact": exact,
            "error": abs(exact - total),
        }

    def _compute_sum(self, f, a: float, b: float, n: int,
                     method: str) -> float:
        """Compute the Riemann sum numerically.

        Args:
            f: Function to evaluate.
            a: Left endpoint.
            b: Right endpoint.
            n: Number of subintervals.
            method: 'left', 'right', or 'midpoint'.

        Returns:
            Riemann sum value.
        """
        dx = (b - a) / n
        total = 0.0
        for i in range(n):
            if method == "left":
                x = a + i * dx
            elif method == "right":
                x = a + (i + 1) * dx
            else:
                x = a + (i + 0.5) * dx
            total += f(x) * dx
        return round(total, 4)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Riemann sum computation steps.

        Args:
            data: Solution data with sum and exact values.

        Returns:
            Steps showing partition, sum, and comparison.
        """
        return [
            f"dx = {_fmt(data['dx'])}, {data['method']} sum",
            f"Riemann sum = {_fmt(data['riemann'])}",
            f"exact integral = {_fmt(data['exact'])}",
            f"error = {_fmt(data['error'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Riemann sum and error.

        Args:
            data: Solution data.

        Returns:
            Sum and error values.
        """
        return (f"sum={_fmt(data['riemann'])}, "
                f"error={_fmt(data['error'])}")


# ── 8. Squeeze theorem (tier 5) ─────────────────────────────────────


@register
class SqueezeTheoremGenerator(StepGenerator):
    """Apply the squeeze theorem to evaluate a limit.

    Given g(x) <= f(x) <= h(x) with lim g = lim h = L,
    concludes lim f = L.

    Input format:
        ``apply squeeze theorem to find limit``

    Target format:
        ``lim_{x->0} x^2*sin(1/x) <step>
        -x^2 <= x^2*sin(1/x) <= x^2
        <step> lim x^2 = 0, lim -x^2 = 0
        <step> by squeeze, limit = 0``

    Difficulty scaling:
        Difficulty 1-3: x^2*sin(1/x) as x -> 0.
        Difficulty 4-6: sin(x)/x as x -> 0 (bounded by 1).
        Difficulty 7-8: n*sin(1/n) as n -> inf.

    Prerequisites:
        limit (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "squeeze_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "apply squeeze theorem to find limit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a squeeze theorem problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._x2_sin(difficulty)
        if difficulty <= 6:
            return self._cos_bound(difficulty)
        return self._n_sin(difficulty)

    def _x2_sin(self, difficulty: int) -> tuple[str, dict]:
        """Generate lim_{x->0} x^p * sin(1/x) problem.

        Args:
            difficulty: Controls exponent p.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(2, 4)
        problem = f"\\lim_{{x \\to 0}} x^{{{p}}} \\sin(1/x)"
        return problem, {
            "squeeze_type": "x_sin",
            "lower": f"-x^{p}", "upper": f"x^{p}",
            "lower_lim": "0", "upper_lim": "0",
            "limit": 0.0,
        }

    def _cos_bound(self, difficulty: int) -> tuple[str, dict]:
        """Generate lim_{x->0} x*cos(1/x) problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\lim_{x \\to 0} x \\cos(1/x)"
        return problem, {
            "squeeze_type": "x_cos",
            "lower": "-|x|", "upper": "|x|",
            "lower_lim": "0", "upper_lim": "0",
            "limit": 0.0,
        }

    def _n_sin(self, difficulty: int) -> tuple[str, dict]:
        """Generate lim_{n->inf} sin(n)/n problem.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        problem = "\\lim_{n \\to \\infty} \\sin(n)/n"
        return problem, {
            "squeeze_type": "sin_n",
            "lower": "-1/n", "upper": "1/n",
            "lower_lim": "0", "upper_lim": "0",
            "limit": 0.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate squeeze theorem application steps.

        Args:
            data: Solution data with bounds and limits.

        Returns:
            Steps showing bounds and conclusion.
        """
        return [
            f"{data['lower']} <= f(x) <= {data['upper']}",
            f"lim lower = {data['lower_lim']}, lim upper = {data['upper_lim']}",
            "by squeeze theorem, limit exists and equals both",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the limit.

        Args:
            data: Solution data.

        Returns:
            Limit value.
        """
        return f"limit = {_fmt(data['limit'])}"


# ── 9. Mean value theorem (tier 5) ──────────────────────────────────


@register
class MeanValueTheoremGenerator(StepGenerator):
    """Apply the mean value theorem to find c in (a, b).

    Given f continuous on [a,b] and differentiable on (a,b), finds
    c such that f'(c) = (f(b) - f(a)) / (b - a).

    Input format:
        ``apply mean value theorem to find c``

    Target format:
        ``f(x) = x^2 on [1, 3] <step>
        f(3) - f(1) = 9 - 1 = 8, b - a = 2
        <step> mean slope = 8/2 = 4
        <step> f'(x) = 2x = 4, c = 2``

    Difficulty scaling:
        Difficulty 1-3: f(x) = x^2 on integer intervals.
        Difficulty 4-6: f(x) = x^3 on integer intervals.
        Difficulty 7-8: f(x) = sqrt(x) on positive intervals.

    Prerequisites:
        limit (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mean_value_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "apply mean value theorem to find c"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mean value theorem problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._quadratic_mvt(difficulty)
        if difficulty <= 6:
            return self._cubic_mvt(difficulty)
        return self._sqrt_mvt(difficulty)

    def _quadratic_mvt(self, difficulty: int) -> tuple[str, dict]:
        """Generate MVT for f(x) = x^2 on [a, b].

        f'(c) = 2c = (b^2 - a^2)/(b-a) = a+b, so c = (a+b)/2.

        Args:
            difficulty: Controls interval.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(0, 4)
        b = a + self._rng.randint(1, 4)
        fa = a * a
        fb = b * b
        mean_slope = (fb - fa) / (b - a)
        c = mean_slope / 2.0  # f'(c) = 2c = mean_slope
        problem = f"f(x) = x^2 on [{a}, {b}]"
        return problem, {
            "func": "x^2", "a": a, "b": b,
            "fa": fa, "fb": fb,
            "mean_slope": mean_slope,
            "deriv": "2x", "c": c,
        }

    def _cubic_mvt(self, difficulty: int) -> tuple[str, dict]:
        """Generate MVT for f(x) = x^3 on [a, b].

        f'(c) = 3c^2 = (b^3-a^3)/(b-a) = a^2+ab+b^2.
        c = sqrt((a^2+ab+b^2)/3).

        Args:
            difficulty: Controls interval.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(0, 2)
        b = a + self._rng.randint(1, 3)
        fa = a ** 3
        fb = b ** 3
        mean_slope = (fb - fa) / (b - a)
        c = math.sqrt(mean_slope / 3.0)
        problem = f"f(x) = x^3 on [{a}, {b}]"
        return problem, {
            "func": "x^3", "a": a, "b": b,
            "fa": fa, "fb": fb,
            "mean_slope": mean_slope,
            "deriv": "3x^2", "c": c,
        }

    def _sqrt_mvt(self, difficulty: int) -> tuple[str, dict]:
        """Generate MVT for f(x) = sqrt(x) on [a, b].

        f'(c) = 1/(2*sqrt(c)) = (sqrt(b)-sqrt(a))/(b-a).
        c = ((b-a)/(2*(sqrt(b)-sqrt(a))))^2.

        Args:
            difficulty: Controls interval.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = a + self._rng.randint(1, 5)
        fa = math.sqrt(a)
        fb = math.sqrt(b)
        mean_slope = (fb - fa) / (b - a)
        # 1/(2*sqrt(c)) = mean_slope => c = 1/(4*mean_slope^2)
        c = 1.0 / (4.0 * mean_slope * mean_slope)
        problem = f"f(x) = \\sqrt{{x}} on [{a}, {b}]"
        return problem, {
            "func": "sqrt(x)", "a": a, "b": b,
            "fa": round(fa, 4), "fb": round(fb, 4),
            "mean_slope": mean_slope,
            "deriv": "1/(2sqrt(x))", "c": c,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate MVT application steps.

        Args:
            data: Solution data with function values and c.

        Returns:
            Steps showing slope computation and c.
        """
        return [
            f"f({data['a']})={_fmt(data['fa'])}, f({data['b']})={_fmt(data['fb'])}",
            f"mean slope = {_fmt(data['mean_slope'])}",
            f"f'(x) = {data['deriv']} = {_fmt(data['mean_slope'])}",
            f"c = {_fmt(data['c'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the c value.

        Args:
            data: Solution data.

        Returns:
            The value c satisfying MVT.
        """
        return f"c = {_fmt(data['c'])}"


# ── 10. L'Hopital extended (tier 5) ─────────────────────────────────


@register
class LHopitalExtendedGenerator(StepGenerator):
    """Apply L'Hopital's rule for 0/0, inf/inf, and converted forms.

    Handles 0/0 and inf/inf directly. Converts 0*inf to 0/0 or
    inf/inf form, and inf-inf to a common form before applying.

    Input format:
        ``apply L'Hopital's rule to evaluate limit``

    Target format:
        ``lim_{x->0+} x*ln(x) <step>
        form: 0*(-inf), rewrite as ln(x)/(1/x)
        <step> = inf/inf, apply L'Hopital
        <step> (1/x)/(-1/x^2) = -x -> 0``

    Difficulty scaling:
        Difficulty 1-3: 0/0 form, e.g. (e^x-1)/x.
        Difficulty 4-6: inf/inf form, e.g. ln(x)/x.
        Difficulty 7-8: 0*inf or inf-inf conversion.

    Prerequisites:
        limit (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lhopital_extended"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["limit"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls indeterminate form.

        Returns:
            Natural language description.
        """
        return "apply L'Hopital's rule to evaluate limit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an extended L'Hopital problem.

        Args:
            difficulty: Controls form type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._zero_over_zero(difficulty)
        if difficulty <= 6:
            return self._inf_over_inf(difficulty)
        return self._product_form(difficulty)

    def _zero_over_zero(self, difficulty: int) -> tuple[str, dict]:
        """Generate 0/0 L'Hopital problem.

        Args:
            difficulty: Controls function choice.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        form_type = self._rng.choice(["exp", "sin"])
        if form_type == "exp":
            a = self._rng.randint(1, 4)
            problem = f"\\lim_{{x \\to 0}} (e^{{{a}x}}-1)/({a}x)"
            return problem, {
                "form": "0/0", "approach": "x -> 0",
                "numer_deriv": f"{a}e^{{{a}x}}",
                "denom_deriv": f"{a}",
                "limit": 1.0,
            }
        a = self._rng.randint(1, 3)
        problem = f"\\lim_{{x \\to 0}} \\sin({a}x)/({a}x)"
        return problem, {
            "form": "0/0", "approach": "x -> 0",
            "numer_deriv": f"{a}cos({a}x)",
            "denom_deriv": f"{a}",
            "limit": 1.0,
        }

    def _inf_over_inf(self, difficulty: int) -> tuple[str, dict]:
        """Generate inf/inf L'Hopital problem.

        Args:
            difficulty: Controls function choice.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        form_type = self._rng.choice(["ln_x", "x_exp"])
        if form_type == "ln_x":
            problem = "\\lim_{x \\to \\infty} \\ln(x)/x"
            return problem, {
                "form": "inf/inf", "approach": "x -> inf",
                "numer_deriv": "1/x",
                "denom_deriv": "1",
                "limit": 0.0,
            }
        p = self._rng.randint(1, 3)
        problem = f"\\lim_{{x \\to \\infty}} x^{{{p}}}/e^x"
        return problem, {
            "form": "inf/inf", "approach": "x -> inf",
            "numer_deriv": f"{p}x^{{{p-1}}}",
            "denom_deriv": "e^x",
            "limit": 0.0,
        }

    def _product_form(self, difficulty: int) -> tuple[str, dict]:
        """Generate 0*inf form L'Hopital problem.

        lim_{x->0+} x*ln(x) = lim ln(x)/(1/x) = lim (1/x)/(-1/x^2)
        = lim -x = 0.

        Args:
            difficulty: Controls variant.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._rng.randint(1, 3)
        problem = f"\\lim_{{x \\to 0^+}} x^{{{p}}} \\ln(x)"
        # Rewrite as ln(x) / x^{-p}, inf/inf
        # Deriv: (1/x) / (-p*x^{-p-1}) = -x^p / p -> 0
        return problem, {
            "form": "0*(-inf)", "approach": "x -> 0+",
            "numer_deriv": "1/x",
            "denom_deriv": f"-{p}x^{{-{p+1}}}",
            "limit": 0.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate L'Hopital application steps.

        Args:
            data: Solution data with form and derivatives.

        Returns:
            Steps showing form identification and application.
        """
        return [
            f"indeterminate form: {data['form']} as {data['approach']}",
            f"numerator': {data['numer_deriv']}",
            f"denominator': {data['denom_deriv']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the limit value.

        Args:
            data: Solution data.

        Returns:
            Limit value.
        """
        return f"limit = {_fmt(data['limit'])}"
