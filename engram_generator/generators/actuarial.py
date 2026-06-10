"""Actuarial science generators -- life tables, annuities, insurance premiums.

6 generators across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _r4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


@register
class LifeTableActuarialGenerator(StepGenerator):
    """Compute life table quantities from mortality probabilities.

    Given q_x (probability of death at age x), compute l_x (number of
    survivors), d_x (number of deaths), and curtate life expectancy e_x
    from a radix population.

    Difficulty scaling:
        Difficulty 1-3: 3 age rows.
        Difficulty 4-6: 4 age rows.
        Difficulty 7-8: 5 age rows.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "life_table_actuarial"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute life table values l_x, d_x, and life expectancy e_x"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a life table problem.

        Args:
            difficulty: Controls number of age rows.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_ages = 3
        elif difficulty <= 6:
            n_ages = 4
        else:
            n_ages = 5

        l0 = 1000
        q_values = [_r4(self._rng.uniform(0.01, 0.15)) for _ in range(n_ages)]

        l_values = [l0]
        d_values = []
        for q in q_values:
            d = _r4(l_values[-1] * q)
            d_values.append(d)
            l_values.append(_r4(l_values[-1] - d))

        # Curtate life expectancy: e_x = sum(l_{x+k} for k=1..n) / l_x
        e_x = _r4(sum(l_values[1:]) / l_values[0])

        q_str = ", ".join(f"q_{i}={q_values[i]}" for i in range(n_ages))
        problem = f"l_0={l0}, {q_str}"
        return problem, {
            "l0": l0, "n_ages": n_ages, "q_values": q_values,
            "l_values": l_values, "d_values": d_values, "e_x": e_x,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for i in range(sd["n_ages"]):
            steps.append(
                f"d_{i} = l_{i}*q_{i} = {sd['l_values'][i]}*{sd['q_values'][i]}"
                f" = {sd['d_values'][i]}"
            )
            steps.append(f"l_{i + 1} = {sd['l_values'][i]} - {sd['d_values'][i]} = {sd['l_values'][i + 1]}")
        l_sum = _r4(sum(sd["l_values"][1:]))
        steps.append(f"e_x = sum(l_1..l_n)/l_0 = {l_sum}/{sd['l0']} = {sd['e_x']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Life expectancy as a string.
        """
        return f"e_x={sd['e_x']}"


@register
class AnnuityPVGenerator(StepGenerator):
    """Compute the present value of an annuity-immediate.

    PV = a_n = (1 - v^n) / i where v = 1 / (1 + i), for a given
    number of periods n and interest rate i.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 5].
        Difficulty 4-6: n in [6, 10].
        Difficulty 7-8: n in [11, 20].
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "annuity_pv"

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
            Task description string.
        """
        return "compute present value of annuity-immediate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an annuity PV problem.

        Args:
            difficulty: Controls number of periods.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 5)
        elif difficulty <= 6:
            n = self._rng.randint(6, 10)
        else:
            n = self._rng.randint(11, 20)

        i = _r4(self._rng.uniform(0.02, 0.12))
        v = _r4(1.0 / (1.0 + i))
        v_n = _r4(v ** n)
        a_n = _r4((1.0 - v_n) / i)

        problem = f"n={n}, i={i}"
        return problem, {
            "n": n, "i": i, "v": v, "v_n": v_n, "a_n": a_n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"v = 1/(1+i) = 1/(1+{sd['i']}) = {sd['v']}",
            f"v^n = {sd['v']}^{sd['n']} = {sd['v_n']}",
            f"a_n = (1 - v^n)/i = (1 - {sd['v_n']})/{sd['i']} = {sd['a_n']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Annuity PV as a string.
        """
        return str(sd["a_n"])


@register
class InsurancePremiumGenerator(StepGenerator):
    """Compute the net single premium for a term life insurance.

    A_x = sum_{k=0}^{n-1} v^(k+1) * k_p_x * q_{x+k} for a term of
    n years, where v = 1/(1+i) is the discount factor, k_p_x is the
    probability of surviving k years, and q_{x+k} is the mortality rate.

    Difficulty scaling:
        Difficulty 1-4: 3-year term.
        Difficulty 5-8: 4 or 5-year term.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "insurance_premium"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute net single premium for term life insurance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an insurance premium problem.

        Args:
            difficulty: Controls term length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = 3
        else:
            n = self._rng.choice([4, 5])

        i = _r4(self._rng.uniform(0.03, 0.08))
        v = _r4(1.0 / (1.0 + i))

        q_values = [_r4(self._rng.uniform(0.005, 0.06)) for _ in range(n)]

        # Compute k_p_x (probability of surviving k years from age x)
        k_p_x = [1.0]
        for k in range(1, n):
            k_p_x.append(_r4(k_p_x[-1] * (1.0 - q_values[k - 1])))

        # NSP: A_x = sum v^(k+1) * k_p_x * q_{x+k}
        terms = []
        for k in range(n):
            term = _r4((v ** (k + 1)) * k_p_x[k] * q_values[k])
            terms.append(term)
        a_x = _r4(sum(terms))

        q_str = ", ".join(f"q_{k}={q_values[k]}" for k in range(n))
        problem = f"i={i}, term={n} years, {q_str}"
        return problem, {
            "n": n, "i": i, "v": v, "q_values": q_values,
            "k_p_x": k_p_x, "terms": terms, "a_x": a_x,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"v = 1/(1+{sd['i']}) = {sd['v']}"]
        for k in range(sd["n"]):
            steps.append(
                f"k={k}: v^{k + 1}*{sd['k_p_x'][k]}*{sd['q_values'][k]}"
                f" = {sd['terms'][k]}"
            )
        steps.append(f"A_x = sum = {sd['a_x']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Net single premium as a string.
        """
        return str(sd["a_x"])


@register
class LossDistributionGenerator(StepGenerator):
    """Compute expected loss above a deductible for a given distribution.

    For an exponential distribution with mean mu and deductible d,
    E[X|X>d] - d = mu (memoryless property). For a Pareto distribution
    with alpha and theta, the excess loss is theta / (alpha - 1).

    Difficulty scaling:
        Difficulty 1-4: exponential distribution.
        Difficulty 5-8: Pareto distribution.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loss_distribution"

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
            Task description string.
        """
        return "compute expected loss above deductible"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loss distribution problem.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            return self._build_exponential(difficulty)
        return self._build_pareto(difficulty)

    def _build_exponential(self, difficulty: int) -> tuple[str, dict]:
        """Build an exponential loss distribution problem.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mu = self._rng.randint(100, 500 * max(1, difficulty))
        d = self._rng.randint(50, mu)
        # Memoryless: E[X-d | X>d] = mu
        excess = mu
        prob_exceed = _r4(math.exp(-d / mu))

        problem = f"Exponential(mu={mu}), deductible d={d}"
        return problem, {
            "dist": "exponential", "mu": mu, "d": d,
            "excess": excess, "prob_exceed": prob_exceed,
        }

    def _build_pareto(self, difficulty: int) -> tuple[str, dict]:
        """Build a Pareto loss distribution problem.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        alpha = _r4(self._rng.uniform(1.5, 4.0))
        theta = self._rng.randint(100, 1000)
        d = self._rng.randint(50, theta)
        # Mean excess: theta / (alpha - 1) for standard Pareto
        excess = _r4(theta / (alpha - 1.0))
        prob_exceed = _r4((theta / (theta + d)) ** alpha)

        problem = f"Pareto(alpha={alpha}, theta={theta}), deductible d={d}"
        return problem, {
            "dist": "pareto", "alpha": alpha, "theta": theta,
            "d": d, "excess": excess, "prob_exceed": prob_exceed,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["dist"] == "exponential":
            return [
                f"Exponential is memoryless: E[X-d|X>d] = mu = {sd['mu']}",
                f"P(X>{sd['d']}) = exp(-{sd['d']}/{sd['mu']}) = {sd['prob_exceed']}",
                f"expected excess loss = {sd['excess']}",
            ]
        return [
            f"Pareto mean excess: theta/(alpha-1) = {sd['theta']}/({sd['alpha']}-1)",
            f"= {sd['theta']}/{_r4(sd['alpha'] - 1.0)} = {sd['excess']}",
            f"P(X>{sd['d']}) = ({sd['theta']}/({sd['theta']}+{sd['d']}))^{sd['alpha']} = {sd['prob_exceed']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Expected excess loss as a string.
        """
        return str(sd["excess"])


@register
class CompoundPoissonGenerator(StepGenerator):
    """Compute mean and variance of a compound Poisson sum.

    S = sum_{i=1}^{N} X_i where N ~ Poisson(lambda) and X_i are iid.
    E[S] = lambda * E[X], Var[S] = lambda * E[X^2].

    Difficulty scaling:
        Difficulty 1-3: uniform X_i.
        Difficulty 4-6: exponential X_i.
        Difficulty 7-8: discrete X_i with given pmf.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compound_poisson"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute mean and variance of compound Poisson sum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compound Poisson problem.

        Args:
            difficulty: Controls claim distribution type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        lam = _r4(self._rng.uniform(1.0, 10.0 * max(1, difficulty // 2)))

        if difficulty <= 3:
            return self._build_uniform(lam)
        if difficulty <= 6:
            return self._build_exponential(lam)
        return self._build_discrete(lam)

    def _build_uniform(self, lam: float) -> tuple[str, dict]:
        """Build compound Poisson with uniform severities.

        Args:
            lam: Poisson rate parameter.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(0, 50)
        b = self._rng.randint(a + 10, a + 200)
        ex = _r4((a + b) / 2.0)
        ex2 = _r4((a * a + a * b + b * b) / 3.0)
        e_s = _r4(lam * ex)
        var_s = _r4(lam * ex2)
        problem = f"N~Poisson({lam}), X~Uniform({a},{b})"
        return problem, {
            "lam": lam, "dist": "uniform", "a": a, "b": b,
            "ex": ex, "ex2": ex2, "e_s": e_s, "var_s": var_s,
        }

    def _build_exponential(self, lam: float) -> tuple[str, dict]:
        """Build compound Poisson with exponential severities.

        Args:
            lam: Poisson rate parameter.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mu = _r4(self._rng.uniform(10.0, 500.0))
        ex = mu
        ex2 = _r4(2.0 * mu * mu)
        e_s = _r4(lam * ex)
        var_s = _r4(lam * ex2)
        problem = f"N~Poisson({lam}), X~Exp(mu={mu})"
        return problem, {
            "lam": lam, "dist": "exponential", "mu": mu,
            "ex": ex, "ex2": ex2, "e_s": e_s, "var_s": var_s,
        }

    def _build_discrete(self, lam: float) -> tuple[str, dict]:
        """Build compound Poisson with discrete severities.

        Args:
            lam: Poisson rate parameter.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_vals = self._rng.randint(2, 4)
        values = sorted(self._rng.sample(range(10, 200), n_vals))
        raw_p = [self._rng.randint(1, 10) for _ in range(n_vals)]
        total_p = sum(raw_p)
        probs = [_r4(p / total_p) for p in raw_p]
        probs[-1] = _r4(1.0 - sum(probs[:-1]))

        ex = _r4(sum(v * p for v, p in zip(values, probs)))
        ex2 = _r4(sum(v * v * p for v, p in zip(values, probs)))
        e_s = _r4(lam * ex)
        var_s = _r4(lam * ex2)

        pmf_str = ", ".join(f"P(X={v})={p}" for v, p in zip(values, probs))
        problem = f"N~Poisson({lam}), {pmf_str}"
        return problem, {
            "lam": lam, "dist": "discrete", "values": values,
            "probs": probs, "ex": ex, "ex2": ex2,
            "e_s": e_s, "var_s": var_s,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"E[X] = {sd['ex']}",
            f"E[X^2] = {sd['ex2']}",
            f"E[S] = lambda*E[X] = {sd['lam']}*{sd['ex']} = {sd['e_s']}",
            f"Var[S] = lambda*E[X^2] = {sd['lam']}*{sd['ex2']} = {sd['var_s']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Mean and variance as a string.
        """
        return f"E[S]={sd['e_s']}, Var[S]={sd['var_s']}"


@register
class ReserveCalculationGenerator(StepGenerator):
    """Compute the prospective reserve for a whole life insurance policy.

    _tV = A_{x+t} - P * a_ddot_{x+t} where A_{x+t} is the net single
    premium at attained age and a_ddot is the annuity-due. Uses simplified
    mortality and interest assumptions.

    Difficulty scaling:
        Difficulty 1-3: t=1 year.
        Difficulty 4-6: t=2-3 years.
        Difficulty 7-8: t=4-5 years.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reserve_calculation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["annuity_pv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute prospective reserve for life insurance policy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reserve calculation problem.

        Args:
            difficulty: Controls policy duration.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            t = 1
        elif difficulty <= 6:
            t = self._rng.randint(2, 3)
        else:
            t = self._rng.randint(4, 5)

        i = _r4(self._rng.uniform(0.03, 0.08))
        v = _r4(1.0 / (1.0 + i))

        # Simplified: A_{x+t} from a short mortality table
        n_future = self._rng.randint(3, 5)
        q_vals = [_r4(self._rng.uniform(0.01, 0.08)) for _ in range(n_future)]

        # Compute A_{x+t}
        k_p = 1.0
        a_xt = 0.0
        for k in range(n_future):
            term = (v ** (k + 1)) * k_p * q_vals[k]
            a_xt += term
            k_p *= (1.0 - q_vals[k])
        a_xt = _r4(a_xt)

        # Compute a_ddot_{x+t} (annuity-due for n_future periods)
        a_ddot = 0.0
        k_p = 1.0
        for k in range(n_future):
            a_ddot += (v ** k) * k_p
            k_p *= (1.0 - q_vals[k])
        a_ddot = _r4(a_ddot)

        # Premium P (level annual premium)
        p_premium = _r4(a_xt / a_ddot) if a_ddot != 0 else 0.0

        # Reserve
        reserve = _r4(a_xt - p_premium * a_ddot)

        q_str = ", ".join(f"q_{k}={q_vals[k]}" for k in range(n_future))
        problem = f"i={i}, t={t}, future mortality: {q_str}"
        return problem, {
            "i": i, "v": v, "t": t, "q_vals": q_vals,
            "n_future": n_future, "a_xt": a_xt,
            "a_ddot": a_ddot, "p_premium": p_premium,
            "reserve": reserve,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"v = 1/(1+{sd['i']}) = {sd['v']}",
            f"A_{{x+{sd['t']}}} = {sd['a_xt']}",
            f"a_ddot_{{x+{sd['t']}}} = {sd['a_ddot']}",
            f"P = A/a_ddot = {sd['a_xt']}/{sd['a_ddot']} = {sd['p_premium']}",
            f"_tV = A - P*a_ddot = {sd['a_xt']} - {sd['p_premium']}*{sd['a_ddot']} = {sd['reserve']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Reserve value as a string.
        """
        return str(sd["reserve"])
