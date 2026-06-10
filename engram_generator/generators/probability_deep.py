"""Deep probability generators -- stochastic, extreme value, queuing.

10 generators at tiers 5-6 covering Weibull distribution, beta distribution,
Poisson approximation, CLT application, mixture distribution, hazard rate,
generating function, extreme value, renewal reward, and branching process.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ──────────────────────────────────────────────────


def _fmt(value: float, places: int = 4) -> str:
    """Round a float and return its string representation.

    Args:
        value: Number to format.
        places: Decimal places.

    Returns:
        Rounded string with trailing zeros stripped.
    """
    return f"{round(value, places):.{places}f}".rstrip("0").rstrip(".")


def _phi(z: float) -> float:
    """Approximate the standard normal CDF Phi(z).

    Args:
        z: z-score.

    Returns:
        Probability P(Z <= z).
    """
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# ── 1. Weibull distribution (tier 5) ───────────────────────────────────


@register
class WeibullDistributionGenerator(StepGenerator):
    """Compute Weibull distribution properties.

    f(x) = (k/lam)*(x/lam)^(k-1)*exp(-(x/lam)^k).
    E[X] = lam*Gamma(1+1/k). Var[X] from Gamma values.
    Computes P(X > t) = exp(-(t/lam)^k).

    Difficulty scaling:
        d1-3: k=1 (exponential special case).
        d4-6: k=2 (Rayleigh-like).
        d7-8: k=3-5, general Weibull.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weibull_distribution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls shape parameter.

        Returns:
            Natural language description.
        """
        return "compute Weibull distribution properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Weibull distribution problem.

        Args:
            difficulty: Controls shape parameter k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            k = 1
        elif difficulty <= 6:
            k = 2
        else:
            k = self._rng.randint(3, 5)
        lam = self._rng.randint(2, 6)
        t = self._rng.randint(1, lam + 2)
        # P(X > t) = exp(-(t/lam)^k)
        survival = math.exp(-(t / lam) ** k)
        # E[X] = lam * Gamma(1 + 1/k)
        mean = lam * math.gamma(1 + 1.0 / k)
        problem = f"Weibull(k={k}, lambda={lam}), P(X>{t})"
        return problem, {
            "k": k, "lam": lam, "t": t,
            "survival": survival, "mean": mean,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Weibull computation steps.

        Args:
            data: Solution data with parameters and results.

        Returns:
            Steps showing survival and mean.
        """
        return [
            f"P(X>{data['t']}) = exp(-({data['t']}/{data['lam']})^{data['k']})",
            f"P(X>{data['t']}) = {_fmt(data['survival'])}",
            f"E[X] = {data['lam']}*Gamma(1+1/{data['k']}) = {_fmt(data['mean'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the survival probability and mean.

        Args:
            data: Solution data.

        Returns:
            Formatted survival probability.
        """
        return f"P(X>{data['t']})={_fmt(data['survival'])}, E[X]={_fmt(data['mean'])}"


# ── 2. Beta distribution (tier 5) ──────────────────────────────────────


@register
class BetaDistributionGenerator(StepGenerator):
    """Compute beta distribution properties.

    E[X] = a/(a+b). Var[X] = ab/((a+b)^2*(a+b+1)). Mode = (a-1)/(a+b-2)
    for a,b > 1.

    Difficulty scaling:
        d1-3: a,b in [1,3] (symmetric or near-symmetric).
        d4-6: a,b in [2,6].
        d7-8: a,b in [3,10].

    Prerequisites:
        division (tier 1).
    """

    _RANGE = {
        1: (1, 3), 2: (1, 3), 3: (1, 3),
        4: (2, 5), 5: (2, 6), 6: (2, 6),
        7: (3, 8), 8: (3, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "beta_distribution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Natural language description.
        """
        return "compute beta distribution mean and variance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a beta distribution problem.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGE.get(difficulty, (1, 3))
        a = self._rng.randint(lo, hi)
        b = self._rng.randint(lo, hi)
        mean = a / (a + b)
        var = (a * b) / ((a + b) ** 2 * (a + b + 1))
        mode = (a - 1) / (a + b - 2) if a > 1 and b > 1 else None
        problem = f"Beta(a={a}, b={b})"
        return problem, {
            "a": a, "b": b, "mean": mean, "var": var, "mode": mode,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate beta distribution steps.

        Args:
            data: Solution data with moments.

        Returns:
            Steps showing mean, variance, and mode.
        """
        steps = [
            f"E[X] = {data['a']}/({data['a']}+{data['b']}) = {_fmt(data['mean'])}",
            f"Var[X] = {data['a']}*{data['b']}/(({data['a']}+{data['b']})^2"
            f"*({data['a']}+{data['b']}+1)) = {_fmt(data['var'])}",
        ]
        if data["mode"] is not None:
            steps.append(
                f"mode = ({data['a']}-1)/({data['a']}+{data['b']}-2) = {_fmt(data['mode'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the mean and variance.

        Args:
            data: Solution data.

        Returns:
            Formatted mean and variance.
        """
        return f"E[X]={_fmt(data['mean'])}, Var={_fmt(data['var'])}"


# ── 3. Poisson approximation (tier 5) ──────────────────────────────────


@register
class PoissonApproximationGenerator(StepGenerator):
    """Compare exact binomial with Poisson approximation.

    Binomial(n,p) ~ Poisson(np) when n is large and p is small.
    Computes both P(X=k) values and the absolute error.

    Difficulty scaling:
        d1-3: n=20, p=0.05.
        d4-6: n=50, p=0.02.
        d7-8: n=100, p=0.01.

    Prerequisites:
        poisson_dist (tier 5).
    """

    _PARAMS = {
        1: (20, 0.05), 2: (20, 0.05), 3: (20, 0.05),
        4: (50, 0.02), 5: (50, 0.02), 6: (50, 0.02),
        7: (100, 0.01), 8: (100, 0.01),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "poisson_approximation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["poisson_dist"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n and p.

        Returns:
            Natural language description.
        """
        return "compare binomial with Poisson approximation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Poisson approximation problem.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, p = self._PARAMS.get(difficulty, (20, 0.05))
        lam = n * p
        k = self._rng.randint(0, min(int(lam) + 2, 5))
        # Exact binomial
        binom_p = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        # Poisson approximation
        poisson_p = math.exp(-lam) * lam ** k / math.factorial(k)
        error = abs(binom_p - poisson_p)
        problem = f"Bin(n={n}, p={p}), P(X={k})"
        return problem, {
            "n": n, "p": p, "k": k, "lam": lam,
            "binom_p": binom_p, "poisson_p": poisson_p, "error": error,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poisson approximation steps.

        Args:
            data: Solution data with exact and approximate values.

        Returns:
            Steps showing both computations and error.
        """
        return [
            f"lambda = {data['n']}*{data['p']} = {_fmt(data['lam'])}",
            f"exact Bin P(X={data['k']}) = {_fmt(data['binom_p'])}",
            f"Poisson P(X={data['k']}) = {_fmt(data['poisson_p'])}",
            f"|error| = {_fmt(data['error'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Poisson approximation and error.

        Args:
            data: Solution data.

        Returns:
            Formatted results.
        """
        return (
            f"Poisson={_fmt(data['poisson_p'])}, "
            f"error={_fmt(data['error'])}"
        )


# ── 4. CLT application (tier 5) ────────────────────────────────────────


@register
class CLTApplicationGenerator(StepGenerator):
    """Apply the Central Limit Theorem to compute sample mean probabilities.

    X_bar ~ N(mu, sigma^2/n). Computes P(X_bar > a) using Z-score and
    the standard normal CDF.

    Difficulty scaling:
        d1-3: n=25, integer mu, sigma.
        d4-6: n=36-64.
        d7-8: n=100+, compute probability of range.

    Prerequisites:
        std_dev (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "clt_application"

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
            difficulty: Controls sample size.

        Returns:
            Natural language description.
        """
        return "apply the CLT to compute P(X_bar > a)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CLT application problem.

        Args:
            difficulty: Controls sample size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 25
        elif difficulty <= 6:
            n = self._rng.choice([36, 49, 64])
        else:
            n = self._rng.choice([100, 144, 169])
        mu = self._rng.randint(50, 100)
        sigma = self._rng.randint(5, 15)
        se = sigma / math.sqrt(n)
        # Set threshold near mean for reasonable probability
        offset = self._rng.randint(1, 3)
        a = mu + offset
        z = (a - mu) / se
        prob_gt = 1.0 - _phi(z)
        problem = f"mu={mu}, sigma={sigma}, n={n}, P(X_bar>{a})"
        return problem, {
            "mu": mu, "sigma": sigma, "n": n, "se": se,
            "a": a, "z": z, "prob": prob_gt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CLT steps.

        Args:
            data: Solution data with Z-score and probability.

        Returns:
            Steps showing SE, Z-score, and probability.
        """
        return [
            f"SE = {data['sigma']}/sqrt({data['n']}) = {_fmt(data['se'])}",
            f"Z = ({data['a']}-{data['mu']})/{_fmt(data['se'])} = {_fmt(data['z'])}",
            f"P(X_bar>{data['a']}) = 1 - Phi({_fmt(data['z'])}) = {_fmt(data['prob'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability.

        Args:
            data: Solution data.

        Returns:
            Formatted probability.
        """
        return f"P(X_bar>{data['a']}) = {_fmt(data['prob'])}"


# ── 5. Mixture distribution (tier 5) ───────────────────────────────────


@register
class MixtureDistributionGenerator(StepGenerator):
    """Compute mean and variance of a mixture distribution.

    f(x) = p*f1(x) + (1-p)*f2(x).
    E[X] = p*mu1 + (1-p)*mu2.
    Var[X] = p*(sig1^2+mu1^2) + (1-p)*(sig2^2+mu2^2) - E[X]^2.

    Difficulty scaling:
        d1-3: Two normals with integer parameters.
        d4-6: Three-component mixture (weights sum to 1).
        d7-8: Two components with varying weights.

    Prerequisites:
        expected_value (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mixture_distribution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of components.

        Returns:
            Natural language description.
        """
        return "compute mean and variance of a mixture distribution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mixture distribution problem.

        Args:
            difficulty: Controls mixture complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3 or difficulty >= 7:
            # Two-component mixture
            p = Fraction(self._rng.randint(1, 4), 5)
            p_f = float(p)
            mu1 = self._rng.randint(0, 10)
            mu2 = self._rng.randint(10, 20)
            s1 = self._rng.randint(1, 4)
            s2 = self._rng.randint(1, 4)
            mean = p_f * mu1 + (1 - p_f) * mu2
            var = (
                p_f * (s1 ** 2 + mu1 ** 2)
                + (1 - p_f) * (s2 ** 2 + mu2 ** 2)
                - mean ** 2
            )
            problem = (
                f"p={p}, N({mu1},{s1}^2) + (1-p)*N({mu2},{s2}^2)"
            )
        else:
            # Three-component mixture
            w1 = Fraction(1, 3)
            w2 = Fraction(1, 3)
            w3 = Fraction(1, 3)
            mus = [self._rng.randint(0, 10) for _ in range(3)]
            sigs = [self._rng.randint(1, 3) for _ in range(3)]
            weights = [float(w1), float(w2), float(w3)]
            mean = sum(w * m for w, m in zip(weights, mus))
            var = (
                sum(w * (s ** 2 + m ** 2) for w, m, s in zip(weights, mus, sigs))
                - mean ** 2
            )
            p_f = weights[0]
            problem = (
                f"w=[1/3,1/3,1/3], mu={mus}, sigma={sigs}"
            )
        return problem, {"mean": mean, "var": var}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mixture distribution steps.

        Args:
            data: Solution data with mean and variance.

        Returns:
            Steps showing mean and variance computation.
        """
        return [
            f"E[X] = sum(p_i * mu_i) = {_fmt(data['mean'])}",
            f"E[X^2] = sum(p_i * (sigma_i^2 + mu_i^2))",
            f"Var[X] = E[X^2] - (E[X])^2 = {_fmt(data['var'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mixture mean and variance.

        Args:
            data: Solution data.

        Returns:
            Formatted mean and variance.
        """
        return f"E[X]={_fmt(data['mean'])}, Var={_fmt(data['var'])}"


# ── 6. Hazard rate (tier 5) ────────────────────────────────────────────


@register
class HazardRateGenerator(StepGenerator):
    """Compute the hazard rate h(t) = f(t)/S(t) = f(t)/(1-F(t)).

    For exponential distribution: h(t) = lambda (constant).
    For Weibull: h(t) = (k/lambda)*(t/lambda)^(k-1).

    Difficulty scaling:
        d1-3: Exponential with rate lambda.
        d4-6: Weibull with k=2.
        d7-8: Weibull with k=3.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hazard_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Natural language description.
        """
        return "compute the hazard rate function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hazard rate problem.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            lam = self._rng.randint(1, 5)
            t = self._rng.randint(1, 6)
            # Exponential: h(t) = lambda, constant
            h_val = float(lam)
            f_val = lam * math.exp(-lam * t)
            s_val = math.exp(-lam * t)
            problem = f"Exp(lambda={lam}), h(t={t})"
            dist = "exponential"
        else:
            if difficulty <= 6:
                k = 2
            else:
                k = 3
            lam = self._rng.randint(2, 5)
            t = self._rng.randint(1, lam + 1)
            # Weibull hazard: h(t) = (k/lam)*(t/lam)^(k-1)
            h_val = (k / lam) * (t / lam) ** (k - 1)
            f_val = (k / lam) * (t / lam) ** (k - 1) * math.exp(-(t / lam) ** k)
            s_val = math.exp(-(t / lam) ** k)
            problem = f"Weibull(k={k}, lam={lam}), h(t={t})"
            dist = "weibull"
        return problem, {
            "dist": dist, "t": t, "h": h_val, "f": f_val, "S": s_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate hazard rate steps.

        Args:
            data: Solution data with f(t), S(t), h(t).

        Returns:
            Steps showing f, S, and h computation.
        """
        return [
            f"f({data['t']}) = {_fmt(data['f'])}",
            f"S({data['t']}) = {_fmt(data['S'])}",
            f"h({data['t']}) = f/S = {_fmt(data['h'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the hazard rate.

        Args:
            data: Solution data.

        Returns:
            Formatted hazard rate.
        """
        return f"h({data['t']}) = {_fmt(data['h'])}"


# ── 7. Probability generating function (tier 5) ────────────────────────


@register
class GeneratingFunctionProbGenerator(StepGenerator):
    """Compute mean from a probability generating function.

    G(z) = E[z^X] = sum P(X=k)*z^k. E[X] = G'(1).
    For Poisson(lambda): G(z) = e^(lambda*(z-1)), G'(1) = lambda.

    Difficulty scaling:
        d1-3: Bernoulli G(z) = 1-p+pz.
        d4-6: Poisson G(z) = e^(lam*(z-1)).
        d7-8: Binomial G(z) = (1-p+pz)^n.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "generating_function_prob"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Natural language description.
        """
        return "compute E[X] from the probability generating function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PGF problem.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            # Bernoulli
            p = Fraction(self._rng.randint(1, 4), 5)
            pf = float(p)
            gf = f"G(z) = {1-pf} + {pf}*z"
            mean = pf
            var = pf * (1 - pf)
            problem = f"Bernoulli(p={p}), G(z) = (1-p)+p*z"
        elif difficulty <= 6:
            # Poisson
            lam = self._rng.randint(1, 6)
            gf = f"G(z) = e^({lam}*(z-1))"
            mean = float(lam)
            var = float(lam)
            problem = f"Poisson(lam={lam}), G(z) = e^(lam*(z-1))"
        else:
            # Binomial
            n = self._rng.randint(3, 8)
            p = Fraction(1, self._rng.randint(2, 5))
            pf = float(p)
            gf = f"G(z) = ({1-pf} + {pf}*z)^{n}"
            mean = n * pf
            var = n * pf * (1 - pf)
            problem = f"Bin(n={n}, p={p}), G(z) = (1-p+p*z)^n"
        return problem, {"gf": gf, "mean": mean, "var": var}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate PGF computation steps.

        Args:
            data: Solution data with G(z), mean, variance.

        Returns:
            Steps showing G(z), G'(1), and G''(1).
        """
        return [
            f"{data['gf']}",
            f"E[X] = G'(1) = {_fmt(data['mean'])}",
            f"Var[X] = G''(1) + G'(1) - (G'(1))^2 = {_fmt(data['var'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mean.

        Args:
            data: Solution data.

        Returns:
            Formatted mean.
        """
        return f"E[X] = {_fmt(data['mean'])}"


# ── 8. Extreme value (tier 6) ──────────────────────────────────────────


@register
class ExtremeValueGenerator(StepGenerator):
    """Compute extreme value distributions for order statistics.

    P(M_n <= x) = F(x)^n. For Uniform(0,1): P(max <= x) = x^n,
    E[max] = n/(n+1). For min: P(min > x) = (1-F(x))^n.

    Difficulty scaling:
        d1-3: Uniform(0,1) max, small n.
        d4-6: Uniform(0,1) min.
        d7-8: Exponential max/min.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "extreme_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distribution and statistic.

        Returns:
            Natural language description.
        """
        return "compute extreme value distribution properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an extreme value problem.

        Args:
            difficulty: Controls distribution and n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, 4 + difficulty)
        if difficulty <= 3:
            # Uniform(0,1) max
            # E[max] = n/(n+1)
            e_max = n / (n + 1)
            x = Fraction(self._rng.randint(1, 4), 5)
            xf = float(x)
            p_val = xf ** n  # P(max <= x)
            problem = f"Unif(0,1), n={n}, P(max<={x}), E[max]"
            stat = "max"
        elif difficulty <= 6:
            # Uniform(0,1) min
            # E[min] = 1/(n+1)
            e_max = 1.0 / (n + 1)
            x = Fraction(self._rng.randint(1, 4), 5)
            xf = float(x)
            p_val = 1.0 - (1.0 - xf) ** n  # P(min <= x) = 1 - (1-x)^n
            problem = f"Unif(0,1), n={n}, P(min<={x}), E[min]"
            stat = "min"
        else:
            # Exponential max
            lam = self._rng.randint(1, 3)
            # E[max] for Exp(lam): H_n / lam where H_n = sum 1/k
            h_n = sum(1.0 / k for k in range(1, n + 1))
            e_max = h_n / lam
            t = self._rng.randint(1, 3)
            # P(max <= t) = (1 - e^(-lam*t))^n
            p_val = (1.0 - math.exp(-lam * t)) ** n
            problem = f"Exp(lam={lam}), n={n}, P(max<={t})"
            stat = "max"
            x = t
        return problem, {
            "n": n, "stat": stat, "p": p_val, "e_stat": e_max,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate extreme value steps.

        Args:
            data: Solution data with probability and expectation.

        Returns:
            Steps showing CDF power and expectation.
        """
        return [
            f"P({data['stat']} <= x) = F(x)^{data['n']}" if data["stat"] == "max"
            else f"P(min <= x) = 1 - (1-F(x))^{data['n']}",
            f"P = {_fmt(data['p'])}",
            f"E[{data['stat']}] = {_fmt(data['e_stat'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability and expectation.

        Args:
            data: Solution data.

        Returns:
            Formatted results.
        """
        return f"P={_fmt(data['p'])}, E[{data['stat']}]={_fmt(data['e_stat'])}"


# ── 9. Renewal reward (tier 6) ─────────────────────────────────────────


@register
class RenewalRewardGenerator(StepGenerator):
    """Compute the long-run reward rate via the renewal reward theorem.

    Long-run rate = E[reward per cycle] / E[cycle length].
    Given distributions for inter-renewal times and rewards per cycle.

    Difficulty scaling:
        d1-3: Constant cycle length, random reward.
        d4-6: Random cycle length (exponential), constant reward.
        d7-8: Both random.

    Prerequisites:
        expected_value (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "renewal_reward"

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
            difficulty: Controls variability.

        Returns:
            Natural language description.
        """
        return "compute the long-run reward rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a renewal reward problem.

        Args:
            difficulty: Controls variability of cycle and reward.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            e_cycle = float(self._rng.randint(2, 6))
            e_reward = float(self._rng.randint(5, 20))
            problem = f"cycle={int(e_cycle)} (const), E[reward]={int(e_reward)}"
        elif difficulty <= 6:
            lam = self._rng.randint(1, 4)
            e_cycle = 1.0 / lam
            e_reward = float(self._rng.randint(3, 15))
            problem = f"Exp(lam={lam}) cycle, reward={int(e_reward)} (const)"
        else:
            lam = self._rng.randint(1, 3)
            e_cycle = 1.0 / lam
            mu_r = self._rng.randint(5, 20)
            e_reward = float(mu_r)
            problem = f"Exp(lam={lam}) cycle, E[reward]={mu_r}"
        rate = e_reward / e_cycle if e_cycle > 0 else 0.0
        return problem, {
            "e_cycle": e_cycle, "e_reward": e_reward, "rate": rate,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate renewal reward steps.

        Args:
            data: Solution data with cycle length, reward, and rate.

        Returns:
            Steps showing the renewal reward theorem.
        """
        return [
            f"E[cycle] = {_fmt(data['e_cycle'])}",
            f"E[reward] = {_fmt(data['e_reward'])}",
            f"rate = E[reward]/E[cycle] = {_fmt(data['rate'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the long-run rate.

        Args:
            data: Solution data.

        Returns:
            Formatted rate.
        """
        return f"rate = {_fmt(data['rate'])}"


# ── 10. Branching process (tier 5) ─────────────────────────────────────


@register
class BranchingProcessGenerator(StepGenerator):
    """Analyse a Galton-Watson branching process.

    Z_{n+1} = sum_{i=1}^{Z_n} X_i. E[Z_n] = mu^n.
    Extinction probability is the smallest root of G(s) = s where
    G is the PGF of the offspring distribution.

    Difficulty scaling:
        d1-3: Offspring ~ Bernoulli-like (0 or 2 children).
        d4-6: Offspring ~ Poisson(mu) with mu in [0.5, 1.5].
        d7-8: Offspring with P(0)=a, P(1)=b, P(2)=c.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "branching_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls offspring distribution.

        Returns:
            Natural language description.
        """
        return "analyse a branching process"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a branching process problem.

        Args:
            difficulty: Controls offspring distribution.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_gen = self._rng.randint(2, 4 + difficulty // 2)
        if difficulty <= 3:
            # P(X=0) = q, P(X=2) = 1-q
            q = Fraction(self._rng.randint(1, 4), 5)
            qf = float(q)
            mu = 2 * (1 - qf)
            e_zn = mu ** n_gen
            # Extinction: G(s) = q + (1-q)*s^2 = s
            # (1-q)*s^2 - s + q = 0 => s = q/(1-q) if mu>1, else 1
            if mu > 1:
                ext = qf / (1 - qf)
            else:
                ext = 1.0
            problem = f"P(0)={q}, P(2)={1-q}, n={n_gen}"
        elif difficulty <= 6:
            # Poisson offspring
            lam_choices = [Fraction(1, 2), Fraction(3, 4), Fraction(1, 1),
                           Fraction(5, 4), Fraction(3, 2)]
            lam = self._rng.choice(lam_choices)
            mu = float(lam)
            e_zn = mu ** n_gen
            # For Poisson: G(s) = e^(lam*(s-1)) = s, hard to solve analytically
            # Extinction prob = 1 if mu <= 1, approximate for mu > 1
            if mu <= 1:
                ext = 1.0
            else:
                # Newton's method: G(s) = e^(mu*(s-1)), solve G(s)=s
                s = 0.5
                for _ in range(50):
                    gs = math.exp(mu * (s - 1))
                    gps = mu * gs
                    s = s - (gs - s) / (gps - 1) if abs(gps - 1) > 1e-12 else s
                ext = max(0.0, min(1.0, s))
            problem = f"Poisson(mu={lam}), n={n_gen}"
        else:
            # General 3-point distribution
            p0_num = self._rng.randint(1, 3)
            p2_num = self._rng.randint(1, 3)
            total = p0_num + p2_num + 1  # P(1) gets the rest
            p0 = Fraction(p0_num, total)
            p1 = Fraction(1, total)
            p2 = Fraction(p2_num, total)
            mu = float(p1) + 2 * float(p2)
            e_zn = mu ** n_gen
            # G(s) = p0 + p1*s + p2*s^2 = s
            # p2*s^2 + (p1-1)*s + p0 = 0
            a_coeff = float(p2)
            b_coeff = float(p1) - 1.0
            c_coeff = float(p0)
            disc = b_coeff ** 2 - 4 * a_coeff * c_coeff
            if disc >= 0 and a_coeff != 0:
                s1 = (-b_coeff - math.sqrt(disc)) / (2 * a_coeff)
                s2 = (-b_coeff + math.sqrt(disc)) / (2 * a_coeff)
                roots = [s for s in [s1, s2] if 0 <= s <= 1]
                ext = min(roots) if roots else 1.0
            else:
                ext = 1.0
            problem = f"P(0)={p0}, P(1)={p1}, P(2)={p2}, n={n_gen}"
        return problem, {
            "mu": mu, "n": n_gen, "e_zn": e_zn, "ext": ext,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate branching process steps.

        Args:
            data: Solution data with mean and extinction probability.

        Returns:
            Steps showing E[Z_n] and extinction probability.
        """
        return [
            f"mu = E[offspring] = {_fmt(data['mu'])}",
            f"E[Z_{data['n']}] = mu^{data['n']} = {_fmt(data['e_zn'])}",
            f"extinction prob = {_fmt(data['ext'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return E[Z_n] and extinction probability.

        Args:
            data: Solution data.

        Returns:
            Formatted results.
        """
        return f"E[Z_{data['n']}]={_fmt(data['e_zn'])}, ext={_fmt(data['ext'])}"
