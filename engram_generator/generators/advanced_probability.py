"""Advanced probability generators -- MGF, CLT, large deviations, coupling.

Spans tiers 5-7. Covers moment generating functions, characteristic
functions, central limit theorem, law of large numbers, conditional
expectation, large deviation bounds, coupling arguments, and
concentration inequalities.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class DecimalFormatter:
    """Formats floating point values with controlled precision.

    Provides consistent rounding and string formatting for probability
    computations that involve transcendental functions.
    """

    def format(self, value: float, places: int = 4) -> str:
        """Format a float to a fixed number of decimal places.

        Args:
            value: Floating point number.
            places: Number of decimal places.

        Returns:
            Rounded string representation.
        """
        return str(round(value, places))

    def format_fraction(self, frac: Fraction) -> str:
        """Format a Fraction as LaTeX or integer string.

        Args:
            frac: Fraction instance.

        Returns:
            Integer string if denominator is 1, else \\frac{}{} notation.
        """
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"


class DistributionParameters:
    """Generates random distribution parameters scaled by difficulty.

    Provides parameter ranges for Bernoulli, Poisson, normal, and
    uniform distributions appropriate for each difficulty level.
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded random instance.
        """
        self._rng = rng

    def bernoulli_p(self, difficulty: int) -> Fraction:
        """Generate a Bernoulli probability parameter.

        Args:
            difficulty: Controls denominator complexity.

        Returns:
            Probability p as a Fraction in (0, 1).
        """
        denoms = [2, 3, 4, 5, 6, 8, 10]
        d = self._rng.choice(denoms[:min(difficulty + 2, len(denoms))])
        n = self._rng.randint(1, d - 1)
        return Fraction(n, d)

    def poisson_lambda(self, difficulty: int) -> int:
        """Generate a Poisson rate parameter.

        Args:
            difficulty: Controls magnitude.

        Returns:
            Integer lambda value.
        """
        return self._rng.randint(1, 2 + difficulty)

    def normal_params(self, difficulty: int) -> tuple[int, int]:
        """Generate normal distribution mean and variance.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (mu, sigma_squared).
        """
        mu = self._rng.randint(0, 3 + difficulty)
        sigma_sq = self._rng.randint(1, 2 + difficulty)
        return mu, sigma_sq

    def uniform_params(self, difficulty: int) -> tuple[int, int]:
        """Generate uniform distribution bounds.

        Args:
            difficulty: Controls range width.

        Returns:
            Tuple of (a, b) with a < b.
        """
        a = self._rng.randint(0, difficulty)
        b = a + self._rng.randint(1, 3 + difficulty)
        return a, b


@register
class MomentGeneratingGenerator(StepGenerator):
    """Compute moment generating function and derive moments.

    Generates MGF M(t) = E[e^{tX}] for Bernoulli, Poisson, or normal
    distributions. Derives mean = M'(0) and variance = M''(0) - (M'(0))^2.

    Input format:
        ``compute MGF and derive moments``

    Target format:
        ``Bernoulli(p=1/3) <step> M(t)=(1-p)+p*e^t=2/3+1/3*e^t
        <step> M'(0)=1/3 <step> M''(0)=1/3
        <step> Var=1/3-(1/3)^2=2/9 <step> mean=0.3333, var=0.2222``

    Difficulty scaling:
        d1-2: Bernoulli with simple p.
        d3-4: Poisson with small lambda.
        d5-6: normal with integer params.
        d7-8: Bernoulli or Poisson with larger params.

    Prerequisites:
        expected_value.

    Example:
        >>> gen = MomentGeneratingGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'moment_generating'
    """

    _DIST_TYPES = {
        1: "bernoulli", 2: "bernoulli",
        3: "poisson", 4: "poisson",
        5: "normal", 6: "normal",
        7: "bernoulli", 8: "poisson",
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with distribution parameter generator and formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._params = DistributionParameters(self._rng)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "moment_generating"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Natural language description.
        """
        return "compute MGF and derive moments"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an MGF problem for a chosen distribution.

        Args:
            difficulty: Controls distribution type and parameters.

        Returns:
            Tuple of (distribution_spec, solution_data).
        """
        dist = self._DIST_TYPES.get(difficulty, "bernoulli")
        builder = {
            "bernoulli": self._build_bernoulli,
            "poisson": self._build_poisson,
            "normal": self._build_normal,
        }[dist]
        return builder(difficulty)

    def _build_bernoulli(self, difficulty: int) -> tuple[str, dict]:
        """Build an MGF problem for Bernoulli distribution.

        Args:
            difficulty: Controls p complexity.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        p = self._params.bernoulli_p(difficulty)
        q = Fraction(1) - p
        mean = float(p)
        variance = float(p * q)
        p_str = self._fmt.format_fraction(p)
        q_str = self._fmt.format_fraction(q)
        problem = f"Bernoulli(p={p_str})"
        mgf_expr = f"M(t)={q_str}+{p_str}*e^t"
        return problem, {
            "dist": "bernoulli", "p": p, "q": q,
            "mgf_expr": mgf_expr,
            "m_prime_0": mean, "m_double_prime_0": mean,
            "mean": mean, "variance": variance,
        }

    def _build_poisson(self, difficulty: int) -> tuple[str, dict]:
        """Build an MGF problem for Poisson distribution.

        Args:
            difficulty: Controls lambda magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        lam = self._params.poisson_lambda(difficulty)
        mean = float(lam)
        variance = float(lam)
        problem = f"Poisson(\\lambda={lam})"
        mgf_expr = f"M(t)=e^{{{lam}(e^t-1)}}"
        m_double = lam + lam * lam
        return problem, {
            "dist": "poisson", "lam": lam,
            "mgf_expr": mgf_expr,
            "m_prime_0": mean,
            "m_double_prime_0": float(m_double),
            "mean": mean, "variance": variance,
        }

    def _build_normal(self, difficulty: int) -> tuple[str, dict]:
        """Build an MGF problem for normal distribution.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        mu, sigma_sq = self._params.normal_params(difficulty)
        mean = float(mu)
        variance = float(sigma_sq)
        problem = f"Normal(\\mu={mu}, \\sigma^2={sigma_sq})"
        mgf_expr = f"M(t)=e^{{{mu}t+{sigma_sq}t^2/2}}"
        m_double = sigma_sq + mu * mu
        return problem, {
            "dist": "normal", "mu": mu, "sigma_sq": sigma_sq,
            "mgf_expr": mgf_expr,
            "m_prime_0": mean,
            "m_double_prime_0": float(m_double),
            "mean": mean, "variance": variance,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate MGF derivation and moment extraction steps.

        Args:
            data: Solution data with MGF expression and moments.

        Returns:
            Steps showing MGF, M'(0), M''(0), and variance derivation.
        """
        mean_str = self._fmt.format(data["mean"])
        var_str = self._fmt.format(data["variance"])
        m2_str = self._fmt.format(data["m_double_prime_0"])
        return [
            data["mgf_expr"],
            f"M'(0)={mean_str}",
            f"M''(0)={m2_str}",
            f"Var=M''(0)-(M'(0))^2={m2_str}-{mean_str}^2={var_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the derived moments.

        Args:
            data: Solution data.

        Returns:
            String with mean and variance.
        """
        mean_str = self._fmt.format(data["mean"])
        var_str = self._fmt.format(data["variance"])
        return f"mean={mean_str}, var={var_str}"


@register
class CharacteristicFunctionProbGenerator(StepGenerator):
    """Compute characteristic function phi(t) = E[e^{itX}].

    Generates characteristic functions for uniform and Bernoulli
    distributions and evaluates at specific t values.

    Input format:
        ``compute characteristic function``

    Target format:
        ``Bernoulli(p=1/2) <step> phi(t)=(1-p)+p*e^{it}
        <step> phi(t)=1/2+1/2*e^{it}
        <step> |phi(t)|^2=1/2+1/2*cos(t)
        <step> phi(t)=1/2+1/2*e^{it}``

    Difficulty scaling:
        d1-3: Bernoulli with simple p.
        d4-6: Uniform on [a, b].
        d7-8: Bernoulli with larger denominator.

    Prerequisites:
        expected_value.

    Example:
        >>> gen = CharacteristicFunctionProbGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'characteristic_function_prob'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with distribution parameter generator and formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._params = DistributionParameters(self._rng)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "characteristic_function_prob"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Natural language description.
        """
        return "compute characteristic function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a characteristic function problem.

        Args:
            difficulty: Controls distribution type and parameters.

        Returns:
            Tuple of (distribution_spec, solution_data).
        """
        if difficulty <= 3 or difficulty >= 7:
            return self._build_bernoulli_cf(difficulty)
        return self._build_uniform_cf(difficulty)

    def _build_bernoulli_cf(self, difficulty: int) -> tuple[str, dict]:
        """Build a characteristic function for Bernoulli distribution.

        Args:
            difficulty: Controls p complexity.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        p = self._params.bernoulli_p(difficulty)
        q = Fraction(1) - p
        p_str = self._fmt.format_fraction(p)
        q_str = self._fmt.format_fraction(q)
        problem = f"Bernoulli(p={p_str})"
        cf_expr = f"phi(t)={q_str}+{p_str}*e^{{it}}"
        mod_sq = f"|phi(t)|^2={float(q)}+{float(p)}*cos(t)"
        return problem, {
            "dist": "bernoulli", "p": p, "q": q,
            "cf_expr": cf_expr, "mod_sq": mod_sq,
        }

    def _build_uniform_cf(self, difficulty: int) -> tuple[str, dict]:
        """Build a characteristic function for uniform distribution.

        Args:
            difficulty: Controls range width.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a, b = self._params.uniform_params(difficulty)
        problem = f"Uniform[{a},{b}]"
        width = b - a
        cf_expr = f"phi(t)=(e^{{i{b}t}}-e^{{i{a}t}})/(i{width}t)"
        mod_sq_val = round(2.0 * (1.0 - math.cos(width)) / (width * width), 4)
        mod_sq = f"|phi(1)|^2={mod_sq_val}"
        return problem, {
            "dist": "uniform", "a": a, "b": b, "width": width,
            "cf_expr": cf_expr, "mod_sq": mod_sq,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate characteristic function derivation steps.

        Args:
            data: Solution data with CF expression.

        Returns:
            Steps showing the CF formula and modulus squared.
        """
        steps = [
            f"E[e^{{itX}}] for {data['dist']}",
            data["cf_expr"],
            data["mod_sq"],
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the characteristic function expression.

        Args:
            data: Solution data.

        Returns:
            CF expression string.
        """
        return data["cf_expr"]


@register
class CentralLimitGenerator(StepGenerator):
    """Approximate tail probability using the central limit theorem.

    Given n i.i.d. variables with known mean and variance, approximates
    P(sum X_i > k) using the CLT normal approximation
    Z = (sum - n*mu) / (sigma * sqrt(n)).

    Input format:
        ``approximate P(sum > k) using CLT``

    Target format:
        ``n=25, mu=10, sigma^2=4, k=260 <step>
        E[sum]=250, Var[sum]=100 <step>
        Z=(260-250)/10=1.0 <step>
        P(Z>1.0)=0.1587 <step> 0.1587``

    Difficulty scaling:
        d1-2: n=10-20, small mu and sigma.
        d3-4: n=20-50.
        d5-6: n=50-100.
        d7-8: n=100-200.

    Prerequisites:
        std_dev.

    Example:
        >>> gen = CentralLimitGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'central_limit'
    """

    _N_RANGES = {
        1: (10, 20), 2: (10, 20),
        3: (20, 50), 4: (20, 50),
        5: (50, 100), 6: (50, 100),
        7: (100, 200), 8: (100, 200),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "central_limit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls sample size.

        Returns:
            Natural language description.
        """
        return "approximate P(sum > k) using CLT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CLT approximation problem.

        Args:
            difficulty: Controls n and parameter ranges.

        Returns:
            Tuple of (problem_spec, solution_data).
        """
        lo, hi = self._N_RANGES.get(difficulty, (10, 20))
        n = self._rng.randint(lo, hi)
        mu = self._rng.randint(2, 5 + difficulty)
        sigma_sq = self._rng.randint(1, 3 + difficulty)
        sigma = math.sqrt(sigma_sq)
        e_sum = n * mu
        var_sum = n * sigma_sq
        std_sum = math.sqrt(var_sum)
        offset = self._rng.randint(1, max(1, int(std_sum)))
        k = e_sum + offset
        z = (k - e_sum) / std_sum if std_sum > 0 else 0.0
        tail_prob = 0.5 * math.erfc(z / math.sqrt(2))
        problem = f"n={n}, \\mu={mu}, \\sigma^2={sigma_sq}, k={k}"
        return problem, {
            "n": n, "mu": mu, "sigma_sq": sigma_sq,
            "e_sum": e_sum, "var_sum": var_sum,
            "std_sum": round(std_sum, 4), "k": k,
            "z": round(z, 4), "tail_prob": round(tail_prob, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CLT computation steps.

        Args:
            data: Solution data with sums, z-score, and tail probability.

        Returns:
            Steps showing expected sum, variance, z-score, and probability.
        """
        z_str = self._fmt.format(data["z"])
        prob_str = self._fmt.format(data["tail_prob"])
        return [
            f"E[sum]={data['n']}*{data['mu']}={data['e_sum']}",
            f"Var[sum]={data['n']}*{data['sigma_sq']}={data['var_sum']}",
            f"Z=({data['k']}-{data['e_sum']})/{data['std_sum']}={z_str}",
            f"P(Z>{z_str})={prob_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the tail probability.

        Args:
            data: Solution data.

        Returns:
            Probability as a rounded decimal string.
        """
        return self._fmt.format(data["tail_prob"])


@register
class LawLargeNumbersGenerator(StepGenerator):
    """Bound deviation probability using Chebyshev's inequality.

    Computes P(|X_bar - mu| > eps) <= sigma^2 / (n * eps^2) and shows
    how the bound tightens as n increases.

    Input format:
        ``bound P(|X_bar - mu| > eps) using Chebyshev``

    Target format:
        ``mu=5, sigma^2=4, eps=1 <step>
        n=10: bound=4/(10*1)=0.4 <step>
        n=100: bound=4/(100*1)=0.04 <step>
        n=1000: bound=4/(1000*1)=0.004 <step> 0.004``

    Difficulty scaling:
        d1-2: 2 sample sizes, small sigma.
        d3-4: 3 sample sizes.
        d5-6: 3 sample sizes, smaller eps.
        d7-8: 4 sample sizes, tight eps.

    Prerequisites:
        std_dev.

    Example:
        >>> gen = LawLargeNumbersGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'law_large_numbers'
    """

    _NUM_SIZES = {
        1: 2, 2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4,
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "law_large_numbers"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of sample sizes shown.

        Returns:
            Natural language description.
        """
        return "bound P(|X_bar - mu| > eps) using Chebyshev"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Chebyshev bound problem.

        Args:
            difficulty: Controls eps and number of sample sizes.

        Returns:
            Tuple of (parameter_spec, solution_data).
        """
        mu = self._rng.randint(2, 5 + difficulty)
        sigma_sq = self._rng.randint(1, 3 + difficulty)
        eps_choices = [Fraction(1), Fraction(1, 2), Fraction(2)]
        if difficulty >= 5:
            eps_choices = [Fraction(1, 2), Fraction(1, 4), Fraction(1)]
        eps = self._rng.choice(eps_choices)
        num_sizes = self._NUM_SIZES.get(difficulty, 2)
        base_n = self._rng.choice([10, 20, 50])
        sample_sizes = [base_n * (10 ** i) for i in range(num_sizes)]
        bounds = []
        for n in sample_sizes:
            bound = Fraction(sigma_sq, 1) / (n * eps * eps)
            bounds.append(min(bound, Fraction(1)))
        eps_str = self._fmt.format_fraction(eps)
        problem = f"\\mu={mu}, \\sigma^2={sigma_sq}, \\epsilon={eps_str}"
        return problem, {
            "mu": mu, "sigma_sq": sigma_sq, "eps": eps,
            "sample_sizes": sample_sizes, "bounds": bounds,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bound computation steps for each sample size.

        Args:
            data: Solution data with sample sizes and bounds.

        Returns:
            Steps showing the Chebyshev bound at each n.
        """
        eps = data["eps"]
        sigma_sq = data["sigma_sq"]
        eps_str = self._fmt.format_fraction(eps)
        steps = []
        for n, bound in zip(data["sample_sizes"], data["bounds"]):
            bound_str = self._fmt.format(float(bound))
            denom = f"{n}*{eps_str}^2"
            steps.append(f"n={n}: bound={sigma_sq}/({denom})={bound_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the tightest (last) bound.

        Args:
            data: Solution data.

        Returns:
            Smallest bound as a decimal string.
        """
        return self._fmt.format(float(data["bounds"][-1]))


@register
class ConditionalExpectationGenerator(StepGenerator):
    """Compute conditional expectation and verify the tower property.

    Generates a joint distribution over (X, Y) as a small table,
    computes E[X|Y=y] for each y, and verifies E[X] = E[E[X|Y]].

    Input format:
        ``compute conditional expectation E[X|Y]``

    Target format:
        ``P(X=1,Y=0)=1/6, P(X=2,Y=0)=1/6, P(X=1,Y=1)=1/3, P(X=2,Y=1)=1/3
        <step> P(Y=0)=1/3, P(Y=1)=2/3
        <step> E[X|Y=0]=(1*1/2+2*1/2)=3/2
        <step> E[X|Y=1]=(1*1/2+2*1/2)=3/2
        <step> E[E[X|Y]]=3/2*1/3+3/2*2/3=3/2
        <step> E[X]=3/2 (tower property verified)
        <step> E[X]=3/2``

    Difficulty scaling:
        d1-2: 2x2 joint table.
        d3-4: 2x3 joint table.
        d5-6: 3x2 joint table.
        d7-8: 3x3 joint table.

    Prerequisites:
        expected_value.

    Example:
        >>> gen = ConditionalExpectationGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conditional_expectation'
    """

    _TABLE_SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 3), 4: (2, 3),
        5: (3, 2), 6: (3, 2), 7: (3, 3), 8: (3, 3),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conditional_expectation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls table size.

        Returns:
            Natural language description.
        """
        return "compute conditional expectation E[X|Y]"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a joint distribution table and compute conditional expectations.

        Args:
            difficulty: Controls table dimensions.

        Returns:
            Tuple of (joint_distribution_string, solution_data).
        """
        nx, ny = self._TABLE_SIZES.get(difficulty, (2, 2))
        x_vals = list(range(1, nx + 1))
        y_vals = list(range(ny))
        joint = self._build_joint_table(nx, ny)
        marginal_y = self._marginal_y(joint, nx, ny)
        cond_exp = self._conditional_expectations(joint, x_vals, y_vals,
                                                   marginal_y, nx, ny)
        e_x = sum(
            Fraction(x_vals[i]) * sum(joint[i][j] for j in range(ny))
            for i in range(nx)
        )
        tower = sum(cond_exp[j] * marginal_y[j] for j in range(ny))
        entries = []
        for i in range(nx):
            for j in range(ny):
                p_str = self._fmt.format_fraction(joint[i][j])
                entries.append(f"P(X={x_vals[i]},Y={y_vals[j]})={p_str}")
        problem = ", ".join(entries)
        return problem, {
            "x_vals": x_vals, "y_vals": y_vals,
            "joint": joint, "marginal_y": marginal_y,
            "cond_exp": cond_exp, "e_x": e_x, "tower": tower,
            "nx": nx, "ny": ny,
        }

    def _build_joint_table(self, nx: int, ny: int) -> list[list[Fraction]]:
        """Build a joint probability table summing to 1.

        Args:
            nx: Number of X values.
            ny: Number of Y values.

        Returns:
            2D list of Fractions summing to 1.
        """
        weights = [
            [self._rng.randint(1, 4) for _ in range(ny)]
            for _ in range(nx)
        ]
        total = sum(w for row in weights for w in row)
        return [
            [Fraction(weights[i][j], total) for j in range(ny)]
            for i in range(nx)
        ]

    def _marginal_y(self, joint: list[list[Fraction]],
                     nx: int, ny: int) -> list[Fraction]:
        """Compute marginal distribution of Y.

        Args:
            joint: Joint probability table.
            nx: Number of X values.
            ny: Number of Y values.

        Returns:
            List of P(Y=y) for each y.
        """
        return [sum(joint[i][j] for i in range(nx)) for j in range(ny)]

    def _conditional_expectations(self, joint: list[list[Fraction]],
                                   x_vals: list[int], y_vals: list[int],
                                   marginal_y: list[Fraction],
                                   nx: int, ny: int) -> list[Fraction]:
        """Compute E[X|Y=y] for each y value.

        Args:
            joint: Joint probability table.
            x_vals: Possible X values.
            y_vals: Possible Y values.
            marginal_y: Marginal distribution of Y.
            nx: Number of X values.
            ny: Number of Y values.

        Returns:
            List of conditional expectations E[X|Y=y].
        """
        result = []
        for j in range(ny):
            if marginal_y[j] == 0:
                result.append(Fraction(0))
                continue
            cond = sum(
                Fraction(x_vals[i]) * joint[i][j] / marginal_y[j]
                for i in range(nx)
            )
            result.append(cond)
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conditional expectation and tower property steps.

        Args:
            data: Solution data with joint table and expectations.

        Returns:
            Steps showing marginals, conditional expectations, and tower check.
        """
        steps = []
        marginal_parts = []
        for j, y in enumerate(data["y_vals"]):
            my_str = self._fmt.format_fraction(data["marginal_y"][j])
            marginal_parts.append(f"P(Y={y})={my_str}")
        steps.append(", ".join(marginal_parts))
        for j, y in enumerate(data["y_vals"]):
            ce_str = self._fmt.format_fraction(data["cond_exp"][j])
            steps.append(f"E[X|Y={y}]={ce_str}")
        tower_str = self._fmt.format_fraction(data["tower"])
        ex_str = self._fmt.format_fraction(data["e_x"])
        steps.append(f"E[E[X|Y]]={tower_str}")
        steps.append(f"E[X]={ex_str} (tower property verified)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the unconditional expectation.

        Args:
            data: Solution data.

        Returns:
            E[X] as a fraction string.
        """
        return self._fmt.format_fraction(data["e_x"])


@register
class LargeDeviationGenerator(StepGenerator):
    """Compute Chernoff bound on tail probability.

    Uses P(X > a) <= min_t e^{-ta} * M(t) with the MGF of a
    Bernoulli sum (binomial). Finds the optimal t and computes bound.

    Input format:
        ``compute Chernoff bound P(X > a)``

    Target format:
        ``X~Binomial(n=10, p=1/3), a=5 <step>
        M(t)=(2/3+1/3*e^t)^10 <step>
        optimal t=ln((a/n-p)/(p*(1-a/n))) (approx) <step>
        t*=0.4055 <step>
        bound=e^{-0.4055*5}*(2/3+1/3*e^{0.4055})^10=0.2131
        <step> 0.2131``

    Difficulty scaling:
        d1-2: small n (5-10), moderate a.
        d3-4: n=10-20.
        d5-6: n=20-50.
        d7-8: n=50-100.

    Prerequisites:
        moment_generating.

    Example:
        >>> gen = LargeDeviationGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'large_deviation'
    """

    _N_RANGES = {
        1: (5, 10), 2: (5, 10),
        3: (10, 20), 4: (10, 20),
        5: (20, 50), 6: (20, 50),
        7: (50, 100), 8: (50, 100),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "large_deviation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["moment_generating"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n range.

        Returns:
            Natural language description.
        """
        return "compute Chernoff bound P(X > a)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Chernoff bound problem for a binomial sum.

        Args:
            difficulty: Controls n and threshold a.

        Returns:
            Tuple of (problem_spec, solution_data).
        """
        lo, hi = self._N_RANGES.get(difficulty, (5, 10))
        n = self._rng.randint(lo, hi)
        p = self._rng.choice([Fraction(1, 4), Fraction(1, 3),
                               Fraction(1, 2), Fraction(2, 5)])
        mean = float(p) * n
        a = int(mean) + self._rng.randint(1, max(1, int(n * 0.2)))
        a = min(a, n - 1)
        p_float = float(p)
        q_float = 1.0 - p_float
        ratio = a / n
        if ratio <= 0 or ratio >= 1 or p_float <= 0 or p_float >= 1:
            t_star = 0.5
        else:
            t_star = math.log((ratio * q_float) / (p_float * (1 - ratio)))
            t_star = max(0.001, t_star)
        mgf_at_t = (q_float + p_float * math.exp(t_star)) ** n
        bound = math.exp(-t_star * a) * mgf_at_t
        bound = min(bound, 1.0)
        p_str = self._fmt.format_fraction(p)
        problem = f"X~Binomial(n={n}, p={p_str}), a={a}"
        return problem, {
            "n": n, "p": p, "a": a,
            "t_star": round(t_star, 4),
            "mgf_at_t": round(mgf_at_t, 4),
            "bound": round(bound, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Chernoff bound derivation steps.

        Args:
            data: Solution data with optimal t and bound.

        Returns:
            Steps showing MGF, optimal t, and final bound.
        """
        p_str = self._fmt.format_fraction(data["p"])
        q_str = self._fmt.format_fraction(Fraction(1) - data["p"])
        t_str = self._fmt.format(data["t_star"])
        bound_str = self._fmt.format(data["bound"])
        return [
            f"M(t)=({q_str}+{p_str}*e^t)^{data['n']}",
            f"optimize: t*={t_str}",
            f"bound=e^{{-{t_str}*{data['a']}}}*M({t_str})={bound_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Chernoff bound value.

        Args:
            data: Solution data.

        Returns:
            Bound as a decimal string.
        """
        return self._fmt.format(data["bound"])


@register
class CouplingArgumentGenerator(StepGenerator):
    """Prove total variation distance bound via coupling construction.

    Constructs a coupling between two coin flip distributions and
    shows P(X != Y) <= d_TV(mu, nu). Uses template-based problems
    with explicit coupling construction.

    Input format:
        ``construct coupling to bound P(X != Y)``

    Target format:
        ``mu: coin p=1/2, nu: coin p=2/3 <step>
        d_TV=|1/2-2/3|/2+|1/2-1/3|/2=1/6
        <step> coupling: draw U~Uniform[0,1],
        X=1 if U<1/2, Y=1 if U<2/3
        <step> P(X!=Y)=|1/2-2/3|=1/6
        <step> P(X!=Y)<=d_TV verified <step> 1/6``

    Difficulty scaling:
        d1-2: two Bernoulli with nearby p values.
        d3-4: two Bernoulli with moderate separation.
        d5-6: two distributions with 3 outcomes.
        d7-8: two distributions with 4 outcomes.

    Prerequisites:
        basic_prob.

    Example:
        >>> gen = CouplingArgumentGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'coupling_argument'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "coupling_argument"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

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
        return "construct coupling to bound P(X != Y)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coupling argument problem.

        Args:
            difficulty: Controls number of outcomes and separation.

        Returns:
            Tuple of (distribution_pair, solution_data).
        """
        if difficulty <= 4:
            return self._build_bernoulli_coupling(difficulty)
        return self._build_multi_outcome_coupling(difficulty)

    def _build_bernoulli_coupling(self, difficulty: int) -> tuple[str, dict]:
        """Build a Bernoulli coupling problem.

        Args:
            difficulty: Controls p separation.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        denoms = [3, 4, 5, 6, 8, 10]
        d = self._rng.choice(denoms[:min(difficulty + 2, len(denoms))])
        p1_num = self._rng.randint(1, d - 2)
        p2_num = p1_num + self._rng.randint(1, d - p1_num - 1)
        p1 = Fraction(p1_num, d)
        p2 = Fraction(p2_num, d)
        d_tv = abs(p1 - p2)
        p1_str = self._fmt.format_fraction(p1)
        p2_str = self._fmt.format_fraction(p2)
        problem = f"\\mu: coin p={p1_str}, \\nu: coin p={p2_str}"
        return problem, {
            "type": "bernoulli", "p1": p1, "p2": p2,
            "d_tv": d_tv,
            "coupling_desc": (
                f"draw U~Uniform[0,1], "
                f"X=1 if U<{p1_str}, Y=1 if U<{p2_str}"
            ),
        }

    def _build_multi_outcome_coupling(self, difficulty: int) -> tuple[str, dict]:
        """Build a multi-outcome coupling problem.

        Args:
            difficulty: Controls number of outcomes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        k = 3 if difficulty <= 6 else 4
        weights_mu = [self._rng.randint(1, 5) for _ in range(k)]
        weights_nu = [self._rng.randint(1, 5) for _ in range(k)]
        total_mu = sum(weights_mu)
        total_nu = sum(weights_nu)
        mu = [Fraction(w, total_mu) for w in weights_mu]
        nu = [Fraction(w, total_nu) for w in weights_nu]
        d_tv = sum(abs(mu[i] - nu[i]) for i in range(k)) / 2
        mu_strs = [self._fmt.format_fraction(m) for m in mu]
        nu_strs = [self._fmt.format_fraction(n) for n in nu]
        problem = (
            f"\\mu=({','.join(mu_strs)}), "
            f"\\nu=({','.join(nu_strs)})"
        )
        return problem, {
            "type": "multi", "mu": mu, "nu": nu, "k": k,
            "d_tv": d_tv,
            "coupling_desc": "optimal coupling via min matching",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coupling construction and bound verification steps.

        Args:
            data: Solution data with distributions and d_TV.

        Returns:
            Steps showing d_TV computation, coupling, and verification.
        """
        d_tv_str = self._fmt.format_fraction(data["d_tv"])
        steps = [
            f"d_TV(mu,nu)={d_tv_str}",
            f"coupling: {data['coupling_desc']}",
            f"P(X!=Y)<={d_tv_str}",
            "coupling bound verified",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total variation distance.

        Args:
            data: Solution data.

        Returns:
            d_TV as a fraction string.
        """
        return self._fmt.format_fraction(data["d_tv"])


@register
class ConcentrationInequalityGenerator(StepGenerator):
    """Compute Hoeffding's inequality bound on sample mean deviation.

    Applies Hoeffding: P(|X_bar - mu| > t) <= 2*exp(-2*n*t^2/(b-a)^2)
    for n i.i.d. bounded random variables in [a, b].

    Input format:
        ``compute Hoeffding bound``

    Target format:
        ``n=50, t=0.5, [a,b]=[0,1] <step>
        exponent=-2*50*0.25/1=-25.0 <step>
        bound=2*exp(-25.0)=0.0 <step> 0.0``

    Difficulty scaling:
        d1-2: [0,1] bounds, moderate n.
        d3-4: [0,1] bounds, larger n.
        d5-6: [a,b] with b-a>1.
        d7-8: tight t, large n.

    Prerequisites:
        logarithm.

    Example:
        >>> gen = ConcentrationInequalityGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'concentration_inequality'
    """

    _N_RANGES = {
        1: (10, 30), 2: (10, 30),
        3: (30, 100), 4: (30, 100),
        5: (50, 200), 6: (50, 200),
        7: (100, 500), 8: (100, 500),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = DecimalFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "concentration_inequality"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n and bound range.

        Returns:
            Natural language description.
        """
        return "compute Hoeffding bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hoeffding inequality problem.

        Args:
            difficulty: Controls n, t, and [a, b] ranges.

        Returns:
            Tuple of (parameter_spec, solution_data).
        """
        lo, hi = self._N_RANGES.get(difficulty, (10, 30))
        n = self._rng.randint(lo, hi)
        if difficulty <= 4:
            a, b = 0, 1
        else:
            a = self._rng.randint(0, 2)
            b = a + self._rng.randint(1, 3 + difficulty)
        t_choices = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
        t = self._rng.choice(t_choices[:min(difficulty + 1, len(t_choices))])
        width = b - a
        exponent = -2.0 * n * t * t / (width * width)
        bound = 2.0 * math.exp(exponent)
        bound = min(bound, 1.0)
        problem = f"n={n}, t={t}, [a,b]=[{a},{b}]"
        return problem, {
            "n": n, "t": t, "a": a, "b": b,
            "width": width, "exponent": round(exponent, 4),
            "bound": round(bound, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hoeffding bound computation steps.

        Args:
            data: Solution data with exponent and bound.

        Returns:
            Steps showing exponent computation and final bound.
        """
        n = data["n"]
        t = data["t"]
        w = data["width"]
        exp_str = self._fmt.format(data["exponent"])
        bound_str = self._fmt.format(data["bound"])
        return [
            f"Hoeffding: P(|X_bar-mu|>{t}) <= 2*exp(-2n*t^2/(b-a)^2)",
            f"exponent=-2*{n}*{t}^2/{w}^2={exp_str}",
            f"bound=2*exp({exp_str})={bound_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Hoeffding bound.

        Args:
            data: Solution data.

        Returns:
            Bound as a decimal string.
        """
        return self._fmt.format(data["bound"])
