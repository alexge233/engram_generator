"""Extended probability generators -- deeper distribution theory and transforms.

12 generators at tiers 4-6 covering negative binomial, hypergeometric,
geometric, uniform continuous, exponential, normal z-score, joint
probability, covariance/correlation, order statistics, gamma, multivariate
normal, and random variable transformations.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _comb(n: int, k: int) -> int:
    """Compute binomial coefficient C(n, k).

    Args:
        n: Total items.
        k: Items to choose.

    Returns:
        The binomial coefficient.
    """
    return math.comb(n, k)


def _fmt(value: float, places: int = 4) -> str:
    """Round a float and return its string representation.

    Args:
        value: Number to format.
        places: Decimal places.

    Returns:
        Rounded string.
    """
    return str(round(value, places))


def _fmt_frac(frac: Fraction) -> str:
    """Format a Fraction as LaTeX or integer string.

    Args:
        frac: Fraction instance.

    Returns:
        Integer string if denominator is 1, else \\frac{}{} notation.
    """
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"


def _factorial(n: int) -> int:
    """Compute n factorial.

    Args:
        n: Non-negative integer.

    Returns:
        n! as an integer.
    """
    return math.factorial(n)


# ---------------------------------------------------------------------------
# Standard normal CDF approximation
# ---------------------------------------------------------------------------

def _phi(z: float) -> float:
    """Approximate the standard normal CDF Phi(z).

    Args:
        z: z-score.

    Returns:
        Probability P(Z <= z).
    """
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# ---------------------------------------------------------------------------
# 1. Negative Binomial Distribution
# ---------------------------------------------------------------------------

@register
class NegativeBinomialGenerator(StepGenerator):
    """Compute P(X=k) for the negative binomial distribution.

    P(X=k) = C(k-1, r-1) * p^r * (1-p)^(k-r), waiting for the r-th
    success. Also computes E[X] = r/p.

    Difficulty scaling:
        d1-2: r=2, small k, p from {1/2, 1/3}.
        d3-4: r=2-3, moderate k.
        d5-6: r=3-4, larger k.
        d7-8: r=4-5, larger k and smaller p.

    Prerequisites:
        binomial_dist.
    """

    _R_RANGES = {
        1: (2, 2), 2: (2, 2), 3: (2, 3), 4: (2, 3),
        5: (3, 4), 6: (3, 4), 7: (4, 5), 8: (4, 5),
    }
    _P_CHOICES = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4),
                  Fraction(2, 5), Fraction(1, 5), Fraction(2, 3)]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "negative_binomial"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial_dist"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute negative binomial probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a negative binomial problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r_lo, r_hi = self._R_RANGES.get(difficulty, (2, 2))
        r = self._rng.randint(r_lo, r_hi)
        p = self._rng.choice(self._P_CHOICES[:min(difficulty + 1, len(self._P_CHOICES))])
        q = Fraction(1) - p
        k = r + self._rng.randint(0, 2 + difficulty)
        binom_coeff = _comb(k - 1, r - 1)
        prob = Fraction(binom_coeff) * p ** r * q ** (k - r)
        e_x = Fraction(r, 1) / p
        p_str = _fmt_frac(p)
        problem = f"NegBin(r={r}, p={p_str}), X={k}"
        return problem, {
            "r": r, "k": k, "p": p, "q": q,
            "binom": binom_coeff, "prob": prob, "e_x": e_x,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        r, k = data["r"], data["k"]
        p_str = _fmt_frac(data["p"])
        q_str = _fmt_frac(data["q"])
        prob_str = _fmt_frac(data["prob"])
        e_str = _fmt_frac(data["e_x"])
        return [
            f"C({k - 1},{r - 1})={data['binom']}",
            f"p^r=({p_str})^{r}={_fmt_frac(data['p'] ** r)}",
            f"(1-p)^(k-r)=({q_str})^{k - r}={_fmt_frac(data['q'] ** (k - r))}",
            f"P(X={k})={data['binom']}*{_fmt_frac(data['p'] ** r)}*{_fmt_frac(data['q'] ** (k - r))}={prob_str}",
            f"E[X]=r/p={r}/{p_str}={e_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability.

        Args:
            data: Solution data dict.

        Returns:
            Probability as a string.
        """
        return _fmt_frac(data["prob"])


# ---------------------------------------------------------------------------
# 2. Hypergeometric Distribution
# ---------------------------------------------------------------------------

@register
class HypergeometricGenerator(StepGenerator):
    """Compute P(X=k) for the hypergeometric distribution.

    P(X=k) = C(K,k)*C(N-K,n-k)/C(N,n) for sampling without
    replacement from a population of N with K successes, drawing n.

    Difficulty scaling:
        d1-2: N=10-15, K=3-5, n=3-5.
        d3-4: N=15-25, K=4-8, n=4-6.
        d5-6: N=20-40, K=5-12, n=5-8.
        d7-8: N=30-50, K=8-15, n=6-10.

    Prerequisites:
        binomial_dist.
    """

    _PARAMS = {
        1: (10, 15, 3, 5, 3, 5), 2: (10, 15, 3, 5, 3, 5),
        3: (15, 25, 4, 8, 4, 6), 4: (15, 25, 4, 8, 4, 6),
        5: (20, 40, 5, 12, 5, 8), 6: (20, 40, 5, 12, 5, 8),
        7: (30, 50, 8, 15, 6, 10), 8: (30, 50, 8, 15, 6, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hypergeometric"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial_dist"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute hypergeometric probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hypergeometric problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        nlo, nhi, klo, khi, slo, shi = self._PARAMS.get(difficulty, self._PARAMS[1])
        big_n = self._rng.randint(nlo, nhi)
        big_k = self._rng.randint(klo, min(khi, big_n - 1))
        n = self._rng.randint(slo, min(shi, big_n))
        k_min = max(0, n - (big_n - big_k))
        k_max = min(n, big_k)
        k = self._rng.randint(k_min, k_max)
        c_kk = _comb(big_k, k)
        c_rest = _comb(big_n - big_k, n - k)
        c_total = _comb(big_n, n)
        prob = Fraction(c_kk * c_rest, c_total)
        problem = f"Hyper(N={big_n}, K={big_k}, n={n}), X={k}"
        return problem, {
            "N": big_n, "K": big_k, "n": n, "k": k,
            "c_kk": c_kk, "c_rest": c_rest, "c_total": c_total,
            "prob": prob,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        return [
            f"C({data['K']},{data['k']})={data['c_kk']}",
            f"C({data['N'] - data['K']},{data['n'] - data['k']})={data['c_rest']}",
            f"C({data['N']},{data['n']})={data['c_total']}",
            f"P(X={data['k']})={data['c_kk']}*{data['c_rest']}/{data['c_total']}={_fmt_frac(data['prob'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability.

        Args:
            data: Solution data dict.

        Returns:
            Probability as a fraction string.
        """
        return _fmt_frac(data["prob"])


# ---------------------------------------------------------------------------
# 3. Geometric Distribution
# ---------------------------------------------------------------------------

@register
class GeometricDistGenerator(StepGenerator):
    """Compute P(X=k) for the geometric distribution.

    P(X=k) = (1-p)^(k-1)*p. E[X] = 1/p. The distribution is
    memoryless: P(X>s+t|X>s) = P(X>t).

    Difficulty scaling:
        d1-2: p from {1/2, 1/3}, k=1-4.
        d3-4: p from {1/4, 1/5, 1/6}, k=2-6.
        d5-6: p from {1/6, 1/8, 1/10}, k=3-8.
        d7-8: p from {1/8, 1/10, 1/12}, k=4-10.

    Prerequisites:
        basic_prob.
    """

    _P_POOLS = {
        1: [Fraction(1, 2), Fraction(1, 3)],
        2: [Fraction(1, 2), Fraction(1, 3)],
        3: [Fraction(1, 4), Fraction(1, 5), Fraction(1, 6)],
        4: [Fraction(1, 4), Fraction(1, 5), Fraction(1, 6)],
        5: [Fraction(1, 6), Fraction(1, 8), Fraction(1, 10)],
        6: [Fraction(1, 6), Fraction(1, 8), Fraction(1, 10)],
        7: [Fraction(1, 8), Fraction(1, 10), Fraction(1, 12)],
        8: [Fraction(1, 8), Fraction(1, 10), Fraction(1, 12)],
    }
    _K_RANGES = {
        1: (1, 4), 2: (1, 4), 3: (2, 6), 4: (2, 6),
        5: (3, 8), 6: (3, 8), 7: (4, 10), 8: (4, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "geometric_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute geometric distribution probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a geometric distribution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._P_POOLS.get(difficulty, self._P_POOLS[1])
        p = self._rng.choice(pool)
        q = Fraction(1) - p
        k_lo, k_hi = self._K_RANGES.get(difficulty, (1, 4))
        k = self._rng.randint(k_lo, k_hi)
        prob = q ** (k - 1) * p
        e_x = Fraction(1, 1) / p
        p_str = _fmt_frac(p)
        problem = f"Geom(p={p_str}), X={k}"
        return problem, {
            "p": p, "q": q, "k": k, "prob": prob, "e_x": e_x,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        p_str = _fmt_frac(data["p"])
        q_str = _fmt_frac(data["q"])
        k = data["k"]
        return [
            f"(1-p)^(k-1)=({q_str})^{k - 1}={_fmt_frac(data['q'] ** (k - 1))}",
            f"P(X={k})={_fmt_frac(data['q'] ** (k - 1))}*{p_str}={_fmt_frac(data['prob'])}",
            f"E[X]=1/p=1/{p_str}={_fmt_frac(data['e_x'])}",
            f"memoryless: P(X>s+t|X>s)=P(X>t)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability.

        Args:
            data: Solution data dict.

        Returns:
            Probability as a fraction string.
        """
        return _fmt_frac(data["prob"])


# ---------------------------------------------------------------------------
# 4. Uniform Continuous Distribution
# ---------------------------------------------------------------------------

@register
class UniformContinuousGenerator(StepGenerator):
    """Compute probabilities for the uniform continuous distribution.

    f(x) = 1/(b-a) on [a,b]. E[X] = (a+b)/2, Var = (b-a)^2/12.
    Computes P(c < X < d) = (d-c)/(b-a) for a sub-interval [c,d].

    Difficulty scaling:
        d1-2: [0, b] with b in 2-5.
        d3-4: [a, b] with small integers.
        d5-6: wider ranges.
        d7-8: larger ranges with tighter sub-intervals.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "uniform_continuous"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute uniform continuous probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a uniform continuous distribution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            a = 0
            b = self._rng.randint(2, 5)
        elif difficulty <= 4:
            a = self._rng.randint(0, 3)
            b = a + self._rng.randint(2, 6)
        elif difficulty <= 6:
            a = self._rng.randint(0, 5)
            b = a + self._rng.randint(4, 10)
        else:
            a = self._rng.randint(0, 10)
            b = a + self._rng.randint(5, 15)
        width = b - a
        c = a + self._rng.randint(0, width - 1)
        d = c + self._rng.randint(1, b - c)
        prob = Fraction(d - c, width)
        e_x = Fraction(a + b, 2)
        var = Fraction((b - a) ** 2, 12)
        problem = f"Uniform[{a},{b}], P({c}<X<{d})"
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "prob": prob, "e_x": e_x, "var": var,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        a, b = data["a"], data["b"]
        c, d = data["c"], data["d"]
        return [
            f"f(x)=1/({b}-{a})=1/{b - a}",
            f"E[X]=({a}+{b})/2={_fmt_frac(data['e_x'])}",
            f"Var=(({b}-{a})^2)/12={_fmt_frac(data['var'])}",
            f"P({c}<X<{d})=({d}-{c})/({b}-{a})={_fmt_frac(data['prob'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability.

        Args:
            data: Solution data dict.

        Returns:
            Probability as a fraction string.
        """
        return _fmt_frac(data["prob"])


# ---------------------------------------------------------------------------
# 5. Exponential Distribution
# ---------------------------------------------------------------------------

@register
class ExponentialDistGenerator(StepGenerator):
    """Compute CDF and probabilities for the exponential distribution.

    f(x) = lambda*e^(-lambda*x). CDF = 1-e^(-lambda*x).
    Memoryless property: P(X>s+t|X>s) = P(X>t).

    Difficulty scaling:
        d1-2: lambda in {1, 2}, x in 1-3.
        d3-4: lambda in {1, 2, 3}, x real-valued.
        d5-6: lambda in {1,...,5}, moderate x.
        d7-8: lambda in {1,...,8}, larger x.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exponential_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute exponential distribution CDF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exponential distribution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lam = self._rng.randint(1, max(1, difficulty))
        x_num = self._rng.randint(1, 2 + difficulty)
        x_den = self._rng.choice([1, 2, 4])
        x = Fraction(x_num, x_den)
        x_float = float(x)
        cdf = 1.0 - math.exp(-lam * x_float)
        survival = math.exp(-lam * x_float)
        e_x = 1.0 / lam
        problem = f"Exp(\\lambda={lam}), P(X<={_fmt_frac(x)})"
        return problem, {
            "lam": lam, "x": x, "x_float": x_float,
            "cdf": round(cdf, 4), "survival": round(survival, 4),
            "e_x": round(e_x, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        lam = data["lam"]
        x_str = _fmt_frac(data["x"])
        return [
            f"f(x)={lam}*e^(-{lam}*x)",
            f"CDF=1-e^(-{lam}*{x_str})=1-{_fmt(data['survival'])}={_fmt(data['cdf'])}",
            f"E[X]=1/{lam}={_fmt(data['e_x'])}",
            f"memoryless: P(X>s+t|X>s)=P(X>t)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the CDF value.

        Args:
            data: Solution data dict.

        Returns:
            CDF value as a decimal string.
        """
        return _fmt(data["cdf"])


# ---------------------------------------------------------------------------
# 6. Normal Distribution Z-Score
# ---------------------------------------------------------------------------

@register
class NormalDistComputeGenerator(StepGenerator):
    """Compute probabilities using the normal distribution and z-scores.

    Z = (X-mu)/sigma. Given mu, sigma, and a threshold a, computes
    P(X > a) using the standard normal CDF. Also solves the inverse
    problem: given a percentile, find X.

    Difficulty scaling:
        d1-2: small mu and sigma, integer a.
        d3-4: moderate mu, sigma.
        d5-6: larger mu, sigma up to 10.
        d7-8: larger ranges.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "normal_dist_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute normal distribution probability via z-score"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a normal distribution z-score problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mu = self._rng.randint(10, 10 * (1 + difficulty))
        sigma = self._rng.randint(1, 2 + difficulty)
        offset = self._rng.randint(1, 2 * sigma)
        a = mu + offset
        z = (a - mu) / sigma
        tail_prob = round(1.0 - _phi(z), 4)
        problem = f"N(\\mu={mu}, \\sigma={sigma}), P(X>{a})"
        return problem, {
            "mu": mu, "sigma": sigma, "a": a,
            "z": round(z, 4), "tail_prob": tail_prob,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing z-score and probability lookup.
        """
        mu, sigma, a = data["mu"], data["sigma"], data["a"]
        z_str = _fmt(data["z"])
        return [
            f"Z=(X-\\mu)/\\sigma=({a}-{mu})/{sigma}={z_str}",
            f"P(Z>{z_str})=1-\\Phi({z_str})={_fmt(data['tail_prob'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the tail probability.

        Args:
            data: Solution data dict.

        Returns:
            Probability as a decimal string.
        """
        return _fmt(data["tail_prob"])


# ---------------------------------------------------------------------------
# 7. Joint Probability
# ---------------------------------------------------------------------------

@register
class JointProbabilityGenerator(StepGenerator):
    """Compute joint, marginal, and check independence from a joint table.

    Given P(X=x, Y=y) from a joint probability table, computes
    marginals P(X=x) = sum_y P(x,y) and checks independence:
    P(x,y) = P(x)*P(y).

    Difficulty scaling:
        d1-2: 2x2 table.
        d3-4: 2x3 table.
        d5-6: 3x2 table.
        d7-8: 3x3 table.

    Prerequisites:
        conditional_prob.
    """

    _SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 3), 4: (2, 3),
        5: (3, 2), 6: (3, 2), 7: (3, 3), 8: (3, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "joint_probability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["conditional_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute joint probability and check independence"

    def _build_joint_table(self, rx: int, ry: int) -> list[list[Fraction]]:
        """Build a joint probability table summing to 1.

        Args:
            rx: Number of rows (X values).
            ry: Number of columns (Y values).

        Returns:
            2D list of Fractions summing to 1.
        """
        weights = [[self._rng.randint(1, 5) for _ in range(ry)] for _ in range(rx)]
        total = sum(w for row in weights for w in row)
        return [[Fraction(weights[i][j], total) for j in range(ry)] for i in range(rx)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a joint probability problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rx, ry = self._SIZES.get(difficulty, (2, 2))
        table = self._build_joint_table(rx, ry)
        marg_x = [sum(table[i][j] for j in range(ry)) for i in range(rx)]
        marg_y = [sum(table[i][j] for i in range(rx)) for j in range(ry)]
        independent = all(
            table[i][j] == marg_x[i] * marg_y[j]
            for i in range(rx) for j in range(ry)
        )
        entries = []
        for i in range(rx):
            for j in range(ry):
                entries.append(f"P(X={i},Y={j})={_fmt_frac(table[i][j])}")
        problem = ", ".join(entries[:4])
        if len(entries) > 4:
            problem += ", ..."
        return problem, {
            "table": table, "rx": rx, "ry": ry,
            "marg_x": marg_x, "marg_y": marg_y,
            "independent": independent,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing marginals and independence check.
        """
        steps = []
        marg_x_parts = [f"P(X={i})={_fmt_frac(data['marg_x'][i])}"
                        for i in range(data["rx"])]
        steps.append(", ".join(marg_x_parts))
        marg_y_parts = [f"P(Y={j})={_fmt_frac(data['marg_y'][j])}"
                        for j in range(data["ry"])]
        steps.append(", ".join(marg_y_parts))
        result = "independent" if data["independent"] else "not independent"
        steps.append(f"independence check: {result}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the independence check result.

        Args:
            data: Solution data dict.

        Returns:
            'independent' or 'not independent'.
        """
        return "independent" if data["independent"] else "not independent"


# ---------------------------------------------------------------------------
# 8. Covariance and Correlation
# ---------------------------------------------------------------------------

@register
class CovarianceCorrelationGenerator(StepGenerator):
    """Compute covariance and Pearson correlation from paired data.

    Cov(X,Y) = E[XY] - E[X]*E[Y].
    rho = Cov(X,Y) / (sigma_X * sigma_Y).

    Difficulty scaling:
        d1-2: 3-4 data pairs.
        d3-4: 4-5 data pairs.
        d5-6: 5-7 data pairs.
        d7-8: 7-9 data pairs.

    Prerequisites:
        expected_value.
    """

    _N_RANGES = {
        1: (3, 4), 2: (3, 4), 3: (4, 5), 4: (4, 5),
        5: (5, 7), 6: (5, 7), 7: (7, 9), 8: (7, 9),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "covariance_correlation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute covariance and correlation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a covariance/correlation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (3, 4))
        n = self._rng.randint(n_lo, n_hi)
        xs = [self._rng.randint(1, 5 + difficulty) for _ in range(n)]
        slope = self._rng.randint(1, 3)
        ys = [slope * x + self._rng.randint(-2, 2) for x in xs]
        e_x = sum(xs) / n
        e_y = sum(ys) / n
        e_xy = sum(x * y for x, y in zip(xs, ys)) / n
        cov = e_xy - e_x * e_y
        var_x = sum((x - e_x) ** 2 for x in xs) / n
        var_y = sum((y - e_y) ** 2 for y in ys) / n
        sigma_x = math.sqrt(var_x) if var_x > 0 else 1.0
        sigma_y = math.sqrt(var_y) if var_y > 0 else 1.0
        rho = cov / (sigma_x * sigma_y) if sigma_x > 0 and sigma_y > 0 else 0.0
        pairs_str = ",".join(f"({x},{y})" for x, y in zip(xs, ys))
        problem = f"Cov,\\rho: {pairs_str}"
        return problem, {
            "xs": xs, "ys": ys, "n": n,
            "e_x": round(e_x, 4), "e_y": round(e_y, 4),
            "e_xy": round(e_xy, 4), "cov": round(cov, 4),
            "sigma_x": round(sigma_x, 4), "sigma_y": round(sigma_y, 4),
            "rho": round(rho, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing covariance and correlation computation.
        """
        return [
            f"E[X]={_fmt(data['e_x'])}, E[Y]={_fmt(data['e_y'])}",
            f"E[XY]={_fmt(data['e_xy'])}",
            f"Cov={_fmt(data['e_xy'])}-{_fmt(data['e_x'])}*{_fmt(data['e_y'])}={_fmt(data['cov'])}",
            f"\\sigma_X={_fmt(data['sigma_x'])}, \\sigma_Y={_fmt(data['sigma_y'])}",
            f"\\rho={_fmt(data['cov'])}/({_fmt(data['sigma_x'])}*{_fmt(data['sigma_y'])})={_fmt(data['rho'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the correlation coefficient.

        Args:
            data: Solution data dict.

        Returns:
            rho as a decimal string.
        """
        return _fmt(data["rho"])


# ---------------------------------------------------------------------------
# 9. Order Statistics
# ---------------------------------------------------------------------------

@register
class OrderStatisticsGenerator(StepGenerator):
    """Compute expected values and PDF of order statistics.

    For n iid Uniform[0,1]: E[X_(k)] = k/(n+1).
    PDF of maximum: f(x_(n)) = n*x^(n-1).

    Difficulty scaling:
        d1-2: n=2-3, compute E[X_(k)] for specific k.
        d3-4: n=3-5.
        d5-6: n=4-7, compute PDF of max at a point.
        d7-8: n=6-10.

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "order_statistics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute order statistic expected value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an order statistics problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            n = self._rng.randint(2, 3)
        elif difficulty <= 4:
            n = self._rng.randint(3, 5)
        elif difficulty <= 6:
            n = self._rng.randint(4, 7)
        else:
            n = self._rng.randint(6, 10)
        k = self._rng.randint(1, n)
        e_xk = Fraction(k, n + 1)
        x_val = self._rng.choice([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)])
        pdf_max = n * float(x_val) ** (n - 1)
        problem = f"n={n} iid Uniform[0,1], E[X_({k})]"
        return problem, {
            "n": n, "k": k, "e_xk": e_xk,
            "x_val": x_val, "pdf_max": round(pdf_max, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing expected value and PDF of max.
        """
        n, k = data["n"], data["k"]
        x_str = _fmt_frac(data["x_val"])
        return [
            f"E[X_({k})]={k}/({n}+1)={_fmt_frac(data['e_xk'])}",
            f"f(x_({n}))={n}*x^({n - 1})",
            f"f({x_str})={n}*{x_str}^{n - 1}={_fmt(data['pdf_max'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the expected value of the k-th order statistic.

        Args:
            data: Solution data dict.

        Returns:
            Expected value as a fraction string.
        """
        return _fmt_frac(data["e_xk"])


# ---------------------------------------------------------------------------
# 10. Gamma Distribution
# ---------------------------------------------------------------------------

@register
class GammaDistGenerator(StepGenerator):
    """Compute properties of the gamma distribution.

    f(x) = x^(a-1)*e^(-x/b)/(b^a*Gamma(a)). E[X] = a*b, Var = a*b^2.
    For integer a, Gamma(a) = (a-1)!.

    Difficulty scaling:
        d1-2: a=2, b=1-2.
        d3-4: a=2-3, b=1-3.
        d5-6: a=3-5, b=1-4.
        d7-8: a=4-6, b=2-5.

    Prerequisites:
        exponentiation.
    """

    _PARAMS = {
        1: (2, 2, 1, 2), 2: (2, 2, 1, 2),
        3: (2, 3, 1, 3), 4: (2, 3, 1, 3),
        5: (3, 5, 1, 4), 6: (3, 5, 1, 4),
        7: (4, 6, 2, 5), 8: (4, 6, 2, 5),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gamma_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute gamma distribution properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gamma distribution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a_lo, a_hi, b_lo, b_hi = self._PARAMS.get(difficulty, self._PARAMS[1])
        a = self._rng.randint(a_lo, a_hi)
        b = self._rng.randint(b_lo, b_hi)
        gamma_a = _factorial(a - 1)
        e_x = a * b
        var_x = a * b * b
        x_eval = self._rng.randint(1, 2 + difficulty)
        pdf_val = (x_eval ** (a - 1)) * math.exp(-x_eval / b) / (b ** a * gamma_a)
        problem = f"Gamma(a={a}, b={b}), evaluate at x={x_eval}"
        return problem, {
            "a": a, "b": b, "gamma_a": gamma_a,
            "e_x": e_x, "var_x": var_x,
            "x_eval": x_eval, "pdf_val": round(pdf_val, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Gamma function, mean, variance, and PDF evaluation.
        """
        a, b = data["a"], data["b"]
        return [
            f"\\Gamma({a})=({a - 1})!={data['gamma_a']}",
            f"E[X]={a}*{b}={data['e_x']}",
            f"Var={a}*{b}^2={data['var_x']}",
            f"f({data['x_eval']})={data['x_eval']}^{a - 1}*e^(-{data['x_eval']}/{b})/({b}^{a}*{data['gamma_a']})={_fmt(data['pdf_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the PDF value.

        Args:
            data: Solution data dict.

        Returns:
            PDF value as a decimal string.
        """
        return _fmt(data["pdf_val"])


# ---------------------------------------------------------------------------
# 11. Multivariate Normal (2D)
# ---------------------------------------------------------------------------

@register
class MultivariateNormalGenerator(StepGenerator):
    """Evaluate the 2D multivariate normal PDF at a given point.

    f(x) = 1/(2*pi*|Sigma|^0.5) * exp(-0.5*(x-mu)^T * Sigma^{-1} * (x-mu)).
    Uses a 2x2 covariance matrix with controllable correlation.

    Difficulty scaling:
        d1-3: diagonal Sigma (uncorrelated).
        d4-6: Sigma with small off-diagonal.
        d7-8: Sigma with larger off-diagonal correlation.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multivariate_normal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "evaluate 2D multivariate normal PDF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2D multivariate normal problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mu1 = self._rng.randint(0, 3 + difficulty)
        mu2 = self._rng.randint(0, 3 + difficulty)
        s1 = self._rng.randint(1, 2 + difficulty)
        s2 = self._rng.randint(1, 2 + difficulty)
        if difficulty <= 3:
            s12 = 0
        elif difficulty <= 6:
            max_cov = int(math.sqrt(s1 * s2) * 0.5)
            s12 = self._rng.randint(0, max(0, max_cov))
        else:
            max_cov = int(math.sqrt(s1 * s2) * 0.8)
            s12 = self._rng.randint(0, max(0, max_cov))
        det = s1 * s2 - s12 * s12
        if det <= 0:
            s12 = 0
            det = s1 * s2
        x1 = mu1 + self._rng.randint(-1, 1)
        x2 = mu2 + self._rng.randint(-1, 1)
        dx1 = x1 - mu1
        dx2 = x2 - mu2
        inv_det = 1.0 / det
        quad_form = inv_det * (s2 * dx1 * dx1 - 2 * s12 * dx1 * dx2 + s1 * dx2 * dx2)
        norm_const = 1.0 / (2.0 * math.pi * math.sqrt(det))
        pdf_val = norm_const * math.exp(-0.5 * quad_form)
        problem = f"N_2(\\mu=({mu1},{mu2}), \\Sigma=[{s1},{s12};{s12},{s2}]), x=({x1},{x2})"
        return problem, {
            "mu1": mu1, "mu2": mu2, "s1": s1, "s2": s2, "s12": s12,
            "det": det, "x1": x1, "x2": x2,
            "quad_form": round(quad_form, 4),
            "norm_const": round(norm_const, 4),
            "pdf_val": round(pdf_val, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing determinant, quadratic form, and PDF.
        """
        return [
            f"|\\Sigma|={data['s1']}*{data['s2']}-{data['s12']}^2={data['det']}",
            f"(x-\\mu)^T \\Sigma^{{-1}} (x-\\mu)={_fmt(data['quad_form'])}",
            f"1/(2\\pi\\sqrt{{{data['det']}}})={_fmt(data['norm_const'])}",
            f"f(x)={_fmt(data['norm_const'])}*exp(-0.5*{_fmt(data['quad_form'])})={_fmt(data['pdf_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the PDF value.

        Args:
            data: Solution data dict.

        Returns:
            PDF value as a decimal string.
        """
        return _fmt(data["pdf_val"])


# ---------------------------------------------------------------------------
# 12. Transformation of Random Variables
# ---------------------------------------------------------------------------

@register
class TransformationRVGenerator(StepGenerator):
    """Compute PDF of transformed random variable Y=g(X).

    Uses the change-of-variable formula:
    f_Y(y) = f_X(g^{-1}(y)) * |dg^{-1}/dy|.
    Covers Y=aX+b, Y=X^2, Y=e^X.

    Difficulty scaling:
        d1-3: Y=aX+b (linear transform).
        d4-6: Y=X^2 (quadratic, X >= 0).
        d7-8: Y=e^X (exponential transform).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transformation_rv"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find PDF of transformed random variable"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transformation of RV problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._build_linear(difficulty)
        if difficulty <= 6:
            return self._build_quadratic(difficulty)
        return self._build_exponential(difficulty)

    def _build_linear(self, difficulty: int) -> tuple[str, dict]:
        """Build a linear transformation Y=aX+b problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(2, 3 + difficulty)
        b = self._rng.randint(0, 5)
        y_val = a * self._rng.randint(1, 5) + b
        x_inv = Fraction(y_val - b, a)
        jacobian = Fraction(1, a)
        problem = f"X~Uniform[0,1], Y={a}X+{b}, f_Y({y_val})"
        pdf_x = 1.0 if 0 <= float(x_inv) <= 1 else 0.0
        pdf_y = pdf_x * float(jacobian)
        return problem, {
            "type": "linear", "a": a, "b": b, "y_val": y_val,
            "x_inv": x_inv, "jacobian": jacobian,
            "pdf_y": round(pdf_y, 4),
            "formula": f"f_Y(y)=f_X((y-{b})/{a})*1/{a}",
        }

    def _build_quadratic(self, difficulty: int) -> tuple[str, dict]:
        """Build a quadratic transformation Y=X^2 problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        y_choices = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]
        y_val = self._rng.choice(y_choices)
        x_inv = Fraction(math.isqrt(y_val.numerator * 10000), 100)
        x_inv_float = math.sqrt(float(y_val))
        jacobian = 0.5 / x_inv_float if x_inv_float > 0 else 0.0
        pdf_x = 1.0 if 0 <= x_inv_float <= 1 else 0.0
        pdf_y = pdf_x * jacobian
        problem = f"X~Uniform[0,1], Y=X^2, f_Y({_fmt_frac(y_val)})"
        return problem, {
            "type": "quadratic", "y_val": y_val,
            "x_inv_float": round(x_inv_float, 4),
            "jacobian": round(jacobian, 4),
            "pdf_y": round(pdf_y, 4),
            "formula": "f_Y(y)=f_X(sqrt(y))*1/(2*sqrt(y))",
        }

    def _build_exponential(self, difficulty: int) -> tuple[str, dict]:
        """Build an exponential transformation Y=e^X problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        y_val = self._rng.choice([Fraction(3, 2), Fraction(2, 1), Fraction(5, 2)])
        y_float = float(y_val)
        x_inv = math.log(y_float)
        jacobian = 1.0 / y_float
        pdf_x = 1.0 if 0 <= x_inv <= 1 else 0.0
        pdf_y = pdf_x * jacobian
        problem = f"X~Uniform[0,1], Y=e^X, f_Y({_fmt_frac(y_val)})"
        return problem, {
            "type": "exponential", "y_val": y_val,
            "x_inv": round(x_inv, 4),
            "jacobian": round(jacobian, 4),
            "pdf_y": round(pdf_y, 4),
            "formula": "f_Y(y)=f_X(ln(y))*1/y",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the change-of-variable computation.
        """
        steps = [data["formula"]]
        if data["type"] == "linear":
            steps.append(f"g^{{-1}}({data['y_val']})={_fmt_frac(data['x_inv'])}")
            steps.append(f"|dg^{{-1}}/dy|={_fmt_frac(data['jacobian'])}")
        elif data["type"] == "quadratic":
            steps.append(f"g^{{-1}}(y)=sqrt(y)={_fmt(data['x_inv_float'])}")
            steps.append(f"|dg^{{-1}}/dy|=1/(2*sqrt(y))={_fmt(data['jacobian'])}")
        else:
            steps.append(f"g^{{-1}}(y)=ln(y)={_fmt(data['x_inv'])}")
            steps.append(f"|dg^{{-1}}/dy|=1/y={_fmt(data['jacobian'])}")
        steps.append(f"f_Y={_fmt(data['pdf_y'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transformed PDF value.

        Args:
            data: Solution data dict.

        Returns:
            PDF value as a decimal string.
        """
        return _fmt(data["pdf_y"])
