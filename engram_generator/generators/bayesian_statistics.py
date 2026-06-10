"""Bayesian statistics generators -- conjugate priors, credible intervals, Bayes factors.

Covers Beta-Binomial conjugate updating, posterior predictive distributions,
credible intervals, Bayes factors, MAP estimation, and empirical Bayes.
All generators are tier 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _BayesFmt:
    """Formats numeric values for Bayesian statistics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def f(value: float, decimals: int = 4) -> str:
        """Format a numeric value, stripping unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


_f = _BayesFmt.f


# ===================================================================
# 1. Conjugate prior (Beta-Binomial)  (tier 6)
# ===================================================================

@register
class ConjugatePriorGenerator(StepGenerator):
    """Beta-Binomial conjugate prior: Beta(a,b) + k successes in n trials = Beta(a+k, b+n-k).

    Computes posterior parameters and posterior mean after observing
    binomial data with a Beta prior.

    Difficulty scaling:
        Difficulty 1-3: small a,b (1-3), small n (5-10).
        Difficulty 4-6: varied priors, moderate n (10-30).
        Difficulty 7-8: large n (30-100), also compute posterior variance.

    Prerequisites:
        bayes_theorem.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conjugate_prior"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bayes_theorem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Beta-Binomial posterior"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate prior parameters and observed data, compute posterior.

        Args:
            difficulty: Controls prior and sample size.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            n = self._rng.randint(5, 10)
        elif difficulty <= 6:
            a = self._rng.randint(1, 10)
            b = self._rng.randint(1, 10)
            n = self._rng.randint(10, 30)
        else:
            a = self._rng.randint(1, 20)
            b = self._rng.randint(1, 20)
            n = self._rng.randint(30, 100)

        k = self._rng.randint(0, n)

        a_post = a + k
        b_post = b + n - k
        post_mean = round(a_post / (a_post + b_post), 4)
        prior_mean = round(a / (a + b), 4)

        data = {
            "a": a, "b": b, "n": n, "k": k,
            "a_post": a_post, "b_post": b_post,
            "prior_mean": prior_mean, "post_mean": post_mean,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            post_var = round(
                (a_post * b_post) /
                ((a_post + b_post) ** 2 * (a_post + b_post + 1)), 4
            )
            data["post_var"] = post_var

        return "\\text{Beta}(a+k,\\; b+n-k)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conjugate prior update steps.

        Args:
            data: Solution data with prior and posterior parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"prior: Beta({data['a']},{data['b']}), prior mean={_f(data['prior_mean'])}",
            f"data: k={data['k']} successes in n={data['n']} trials",
            f"posterior: Beta({data['a_post']},{data['b_post']})",
            f"posterior mean = {data['a_post']}/({data['a_post']}+{data['b_post']}) = {_f(data['post_mean'])}",
        ]
        if data["full"]:
            steps.append(f"posterior var = {_f(data['post_var'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the posterior parameters and mean.

        Args:
            data: Solution data.

        Returns:
            String with posterior Beta parameters and mean.
        """
        result = f"Beta({data['a_post']},{data['b_post']}), mean={_f(data['post_mean'])}"
        if data["full"]:
            result += f", var={_f(data['post_var'])}"
        return result


# ===================================================================
# 2. Posterior predictive  (tier 6)
# ===================================================================

@register
class PosteriorPredictiveGenerator(StepGenerator):
    """Posterior predictive for Beta-Bernoulli: P(x_new=1|data) = (a+k)/(a+b+n).

    After Beta-Binomial updating, computes the predictive probability
    for the next observation.

    Difficulty scaling:
        Difficulty 1-3: small parameters, compute P(x=1).
        Difficulty 4-6: larger parameters, also compare to MLE.
        Difficulty 7-8: compute predictive for multiple future observations.

    Prerequisites:
        conjugate_prior.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "posterior_predictive"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conjugate_prior"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute posterior predictive probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate posterior and compute predictive probability.

        Args:
            difficulty: Controls parameter ranges and variants.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            n = self._rng.randint(5, 10)
        elif difficulty <= 6:
            a = self._rng.randint(1, 10)
            b = self._rng.randint(1, 10)
            n = self._rng.randint(10, 30)
        else:
            a = self._rng.randint(1, 15)
            b = self._rng.randint(1, 15)
            n = self._rng.randint(20, 60)

        k = self._rng.randint(0, n)

        a_post = a + k
        b_post = b + n - k
        pred = round(a_post / (a_post + b_post), 4)
        mle = round(k / n, 4) if n > 0 else 0.0

        data = {
            "a": a, "b": b, "n": n, "k": k,
            "a_post": a_post, "b_post": b_post,
            "pred": pred, "mle": mle,
            "full": difficulty >= 4,
        }

        if difficulty >= 7:
            # P(next m observations have exactly j successes)
            # = Beta-Binomial PMF, but keep it simple: P for 2 new obs
            m = 2
            # P(both success) = E[theta^2] = a'(a'+1)/((a'+b')(a'+b'+1))
            p_both = round(
                a_post * (a_post + 1) /
                ((a_post + b_post) * (a_post + b_post + 1)), 4
            )
            data["m"] = m
            data["p_both"] = p_both

        return "P(x_{new}=1|data) = \\frac{a+k}{a+b+n}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate posterior predictive computation steps.

        Args:
            data: Solution data with posterior and predictive.

        Returns:
            List of step strings.
        """
        steps = [
            f"prior: Beta({data['a']},{data['b']}), data: k={data['k']}, n={data['n']}",
            f"posterior: Beta({data['a_post']},{data['b_post']})",
            f"P(x_new=1) = {data['a_post']}/{data['a_post']+data['b_post']} = {_f(data['pred'])}",
        ]
        if data["full"]:
            steps.append(f"MLE = k/n = {_f(data['mle'])}")
        if "p_both" in data:
            steps.append(f"P(next {data['m']} both success) = {_f(data['p_both'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the predictive probability.

        Args:
            data: Solution data.

        Returns:
            String with predictive P(x_new=1).
        """
        result = f"P(x_new=1) = {_f(data['pred'])}"
        if data["full"]:
            result += f", MLE = {_f(data['mle'])}"
        if "p_both" in data:
            result += f", P(both) = {_f(data['p_both'])}"
        return result


# ===================================================================
# 3. Credible interval  (tier 6)
# ===================================================================

@register
class CredibleIntervalGenerator(StepGenerator):
    """95% credible interval for Beta posterior using normal approximation.

    For Beta(a,b), uses the normal approximation mean +/- 1.96*sd
    when a+b is large enough, providing an equal-tailed interval.

    Difficulty scaling:
        Difficulty 1-3: small posterior, simple interval.
        Difficulty 4-6: larger posterior, verify coverage.
        Difficulty 7-8: compare 90% and 95% intervals.

    Prerequisites:
        conjugate_prior.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "credible_interval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conjugate_prior"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute credible interval for Beta posterior"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Beta posterior and compute approximate credible interval.

        Args:
            difficulty: Controls posterior parameters.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(3, 10)
            b = self._rng.randint(3, 10)
        elif difficulty <= 6:
            a = self._rng.randint(5, 30)
            b = self._rng.randint(5, 30)
        else:
            a = self._rng.randint(10, 60)
            b = self._rng.randint(10, 60)

        mean = round(a / (a + b), 4)
        var = round(a * b / ((a + b) ** 2 * (a + b + 1)), 4)
        sd = round(math.sqrt(var), 4)

        z_95 = 1.96
        lo_95 = round(max(0.0, mean - z_95 * sd), 4)
        hi_95 = round(min(1.0, mean + z_95 * sd), 4)
        width_95 = round(hi_95 - lo_95, 4)

        data = {
            "a": a, "b": b, "mean": mean, "var": var, "sd": sd,
            "lo_95": lo_95, "hi_95": hi_95, "width_95": width_95,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            z_90 = 1.645
            lo_90 = round(max(0.0, mean - z_90 * sd), 4)
            hi_90 = round(min(1.0, mean + z_90 * sd), 4)
            width_90 = round(hi_90 - lo_90, 4)
            data["lo_90"] = lo_90
            data["hi_90"] = hi_90
            data["width_90"] = width_90

        return "CI_{95} \\approx \\mu \\pm 1.96\\sigma", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate credible interval computation steps.

        Args:
            data: Solution data with posterior and interval bounds.

        Returns:
            List of step strings.
        """
        steps = [
            f"Beta({data['a']},{data['b']}), mean={_f(data['mean'])}",
            f"var={_f(data['var'])}, sd={_f(data['sd'])}",
            f"95% CI = [{_f(data['lo_95'])}, {_f(data['hi_95'])}], width={_f(data['width_95'])}",
        ]
        if data["full"]:
            steps.append(
                f"90% CI = [{_f(data['lo_90'])}, {_f(data['hi_90'])}], width={_f(data['width_90'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the credible interval.

        Args:
            data: Solution data.

        Returns:
            String with 95% CI bounds.
        """
        result = f"95% CI = [{_f(data['lo_95'])}, {_f(data['hi_95'])}]"
        if data["full"]:
            result += f", 90% CI = [{_f(data['lo_90'])}, {_f(data['hi_90'])}]"
        return result


# ===================================================================
# 4. Bayes factor  (tier 6)
# ===================================================================

@register
class BayesFactorGenerator(StepGenerator):
    """Bayes factor: BF = P(data|M1)/P(data|M2) for simple models.

    Computes marginal likelihoods for two competing Bernoulli models
    with Beta priors and interprets the evidence strength.
    BF > 10: strong, 3-10: moderate, 1-3: weak.

    Difficulty scaling:
        Difficulty 1-3: two point hypotheses, small data.
        Difficulty 4-6: Beta-Bernoulli marginal likelihoods.
        Difficulty 7-8: also compute posterior model probabilities.

    Prerequisites:
        bayes_theorem.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bayes_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bayes_theorem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Bayes factor comparing two models"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two models and data, compute Bayes factor.

        Args:
            difficulty: Controls model complexity and data size.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Point hypotheses: M1: theta=p1, M2: theta=p2
            p1 = round(self._rng.choice([0.3, 0.4, 0.5, 0.6, 0.7]), 1)
            p2_choices = [x for x in [0.3, 0.4, 0.5, 0.6, 0.7] if x != p1]
            p2 = round(self._rng.choice(p2_choices), 1)
            n = self._rng.randint(5, 10)
            k = self._rng.randint(0, n)

            # P(data|M1) = p1^k * (1-p1)^(n-k)
            ml1 = round(p1 ** k * (1 - p1) ** (n - k), 4)
            ml2 = round(p2 ** k * (1 - p2) ** (n - k), 4)

            data = {
                "model_type": "point", "p1": p1, "p2": p2,
                "n": n, "k": k, "ML1": ml1, "ML2": ml2,
            }
        else:
            # Beta-Bernoulli: M1 ~ Beta(a1,b1), M2 ~ Beta(a2,b2)
            a1 = self._rng.randint(1, 5)
            b1 = self._rng.randint(1, 5)
            a2 = self._rng.randint(1, 5)
            b2 = self._rng.randint(1, 5)
            n = self._rng.randint(8, 20 + difficulty * 3)
            k = self._rng.randint(0, n)

            # Marginal likelihood: Beta(a,b)->Bernoulli
            # P(data|M) = B(a+k, b+n-k) / B(a,b)
            # where B is the Beta function
            def log_beta(x: float, y: float) -> float:
                return math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)

            log_ml1 = log_beta(a1 + k, b1 + n - k) - log_beta(a1, b1)
            log_ml2 = log_beta(a2 + k, b2 + n - k) - log_beta(a2, b2)

            ml1 = round(math.exp(log_ml1), 4)
            ml2 = round(math.exp(log_ml2), 4)

            data = {
                "model_type": "beta",
                "a1": a1, "b1": b1, "a2": a2, "b2": b2,
                "n": n, "k": k, "ML1": ml1, "ML2": ml2,
            }

        bf = round(ml1 / ml2, 4) if ml2 > 0 else float("inf")

        if bf > 10:
            interpretation = "strong for M1"
        elif bf > 3:
            interpretation = "moderate for M1"
        elif bf > 1:
            interpretation = "weak for M1"
        elif bf > 1 / 3:
            interpretation = "weak for M2"
        elif bf > 1 / 10:
            interpretation = "moderate for M2"
        else:
            interpretation = "strong for M2"

        data["BF"] = bf
        data["interpretation"] = interpretation
        data["full"] = difficulty >= 7

        if difficulty >= 7:
            # Posterior model probs with equal prior
            p_m1 = round(bf / (1 + bf), 4) if bf < float("inf") else 1.0
            p_m2 = round(1 - p_m1, 4)
            data["P_M1"] = p_m1
            data["P_M2"] = p_m2

        return "BF_{12} = \\frac{P(data|M_1)}{P(data|M_2)}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bayes factor computation steps.

        Args:
            data: Solution data with marginal likelihoods and BF.

        Returns:
            List of step strings.
        """
        steps = [f"data: k={data['k']} in n={data['n']}"]

        if data["model_type"] == "point":
            steps.append(f"M1: theta={_f(data['p1'])}, M2: theta={_f(data['p2'])}")
        else:
            steps.append(
                f"M1: Beta({data['a1']},{data['b1']}), "
                f"M2: Beta({data['a2']},{data['b2']})"
            )

        steps.append(f"P(data|M1)={_f(data['ML1'])}, P(data|M2)={_f(data['ML2'])}")
        steps.append(f"BF = {_f(data['BF'])}, {data['interpretation']}")

        if data["full"]:
            steps.append(f"P(M1|data)={_f(data['P_M1'])}, P(M2|data)={_f(data['P_M2'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Bayes factor and interpretation.

        Args:
            data: Solution data.

        Returns:
            String with BF and evidence interpretation.
        """
        result = f"BF = {_f(data['BF'])}, {data['interpretation']}"
        if data["full"]:
            result += f", P(M1|data) = {_f(data['P_M1'])}"
        return result


# ===================================================================
# 5. MAP estimate  (tier 5)
# ===================================================================

@register
class MAPEstimateGenerator(StepGenerator):
    """MAP estimate: argmax P(theta|data) for normal prior + normal likelihood.

    For a normal prior N(mu_0, sigma_0^2) and n observations from
    N(theta, sigma^2), the MAP is a precision-weighted average of the
    prior mean and the sample mean.

    Difficulty scaling:
        Difficulty 1-3: known variance, small n, integer params.
        Difficulty 4-6: larger n, decimal params, also compute posterior sd.
        Difficulty 7-8: compare MAP to MLE and prior mean.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "map_estimate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute MAP estimate for normal model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate normal prior and likelihood, compute MAP.

        Args:
            difficulty: Controls parameter ranges and extras.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mu_0 = float(self._rng.randint(0, 10))
            sigma_0_sq = float(self._rng.randint(1, 5))
            sigma_sq = float(self._rng.randint(1, 5))
            n = self._rng.randint(3, 8)
        elif difficulty <= 6:
            mu_0 = round(self._rng.uniform(-5, 15), 1)
            sigma_0_sq = round(self._rng.uniform(0.5, 10), 1)
            sigma_sq = round(self._rng.uniform(0.5, 8), 1)
            n = self._rng.randint(5, 20)
        else:
            mu_0 = round(self._rng.uniform(-10, 20), 1)
            sigma_0_sq = round(self._rng.uniform(1, 15), 1)
            sigma_sq = round(self._rng.uniform(0.5, 10), 1)
            n = self._rng.randint(10, 40)

        # Sample mean
        x_bar = round(self._rng.uniform(mu_0 - 5, mu_0 + 5), 2)

        # Posterior precision = 1/sigma_0^2 + n/sigma^2
        prior_prec = round(1.0 / sigma_0_sq, 4)
        lik_prec = round(n / sigma_sq, 4)
        post_prec = round(prior_prec + lik_prec, 4)
        post_var = round(1.0 / post_prec, 4)

        # MAP = (prior_prec * mu_0 + lik_prec * x_bar) / post_prec
        theta_map = round(
            (prior_prec * mu_0 + lik_prec * x_bar) / post_prec, 4
        )

        data = {
            "mu_0": mu_0, "sigma_0_sq": sigma_0_sq,
            "sigma_sq": sigma_sq, "n": n, "x_bar": x_bar,
            "prior_prec": prior_prec, "lik_prec": lik_prec,
            "post_prec": post_prec, "post_var": post_var,
            "MAP": theta_map,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            data["post_sd"] = round(math.sqrt(post_var), 4)
            data["MLE"] = x_bar

        return "\\hat{\\theta}_{MAP} = \\frac{\\sigma^{-2}_0 \\mu_0 + n\\sigma^{-2}\\bar{x}}{\\sigma^{-2}_0 + n\\sigma^{-2}}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate MAP estimation steps.

        Args:
            data: Solution data with prior, likelihood, and MAP.

        Returns:
            List of step strings.
        """
        steps = [
            f"prior: N({_f(data['mu_0'])},{_f(data['sigma_0_sq'])}), "
            f"likelihood var={_f(data['sigma_sq'])}, n={data['n']}",
            f"x_bar={_f(data['x_bar'])}",
            f"prec_prior={_f(data['prior_prec'])}, prec_lik={_f(data['lik_prec'])}",
            f"MAP = ({_f(data['prior_prec'])}*{_f(data['mu_0'])} + "
            f"{_f(data['lik_prec'])}*{_f(data['x_bar'])}) / {_f(data['post_prec'])} = {_f(data['MAP'])}",
        ]
        if data["full"]:
            steps.append(
                f"post_sd={_f(data['post_sd'])}, MLE={_f(data['MLE'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the MAP estimate.

        Args:
            data: Solution data.

        Returns:
            String with MAP value.
        """
        result = f"MAP = {_f(data['MAP'])}, post_var = {_f(data['post_var'])}"
        if data["full"]:
            result += f", MLE = {_f(data['MLE'])}"
        return result


# ===================================================================
# 6. Empirical Bayes  (tier 6)
# ===================================================================

@register
class EmpiricalBayesGenerator(StepGenerator):
    """Empirical Bayes: estimate prior hyperparameters from data, then update.

    Uses method of moments on group-level proportions to estimate
    Beta(a,b) hyperparameters, then computes posterior for each group.
    Two-stage procedure: (1) estimate a,b from data, (2) shrink.

    Difficulty scaling:
        Difficulty 1-3: 3 groups, small counts.
        Difficulty 4-6: 4-5 groups, moderate counts.
        Difficulty 7-8: 5-6 groups, compare raw vs shrunk estimates.

    Prerequisites:
        arithmetic_mean.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "empirical_bayes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "estimate prior via empirical Bayes and compute shrinkage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate group data, estimate hyperparameters, compute shrinkage.

        Args:
            difficulty: Controls number and size of groups.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_groups = 3
            trials = [self._rng.randint(5, 15) for _ in range(n_groups)]
        elif difficulty <= 6:
            n_groups = self._rng.randint(4, 5)
            trials = [self._rng.randint(10, 30) for _ in range(n_groups)]
        else:
            n_groups = self._rng.randint(5, 6)
            trials = [self._rng.randint(15, 50) for _ in range(n_groups)]

        # True proportions drawn from a hidden Beta, then sample counts
        true_p = [round(self._rng.uniform(0.2, 0.8), 2) for _ in range(n_groups)]
        successes = [self._rng.randint(0, t) for t in trials]
        raw_rates = [round(successes[i] / trials[i], 4) for i in range(n_groups)]

        # Method of moments for Beta hyperparameters
        p_bar = round(sum(raw_rates) / n_groups, 4)
        p_var = round(
            sum((r - p_bar) ** 2 for r in raw_rates) / max(n_groups - 1, 1), 4
        )

        # Ensure valid: need p_var < p_bar*(1-p_bar)
        max_var = p_bar * (1 - p_bar)
        if p_var >= max_var or p_var <= 0:
            p_var = round(max_var * 0.5, 4)

        # Method of moments: a + b = p_bar*(1-p_bar)/p_var - 1
        ab_sum = round(p_bar * (1 - p_bar) / p_var - 1, 4)
        if ab_sum <= 0:
            ab_sum = 2.0
        a_est = round(p_bar * ab_sum, 4)
        b_est = round((1 - p_bar) * ab_sum, 4)

        # Posterior means (shrinkage estimates)
        shrunk = []
        for i in range(n_groups):
            s = round(
                (a_est + successes[i]) / (a_est + b_est + trials[i]), 4
            )
            shrunk.append(s)

        data = {
            "n_groups": n_groups, "trials": trials, "successes": successes,
            "raw_rates": raw_rates, "p_bar": p_bar, "p_var": p_var,
            "a_est": a_est, "b_est": b_est, "shrunk": shrunk,
            "full": difficulty >= 7,
        }

        return "\\hat{a} = \\bar{p}(\\bar{p}(1-\\bar{p})/s^2 - 1)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate empirical Bayes computation steps.

        Args:
            data: Solution data with estimated hyperparameters and shrinkage.

        Returns:
            List of step strings.
        """
        n = data["n_groups"]
        raw_str = ", ".join(_f(r) for r in data["raw_rates"])
        steps = [
            f"groups={n}, raw rates=[{raw_str}]",
            f"p_bar={_f(data['p_bar'])}, p_var={_f(data['p_var'])}",
            f"estimated prior: Beta({_f(data['a_est'])},{_f(data['b_est'])})",
        ]
        shrunk_str = ", ".join(_f(s) for s in data["shrunk"])
        steps.append(f"shrunk=[{shrunk_str}]")

        if data["full"]:
            diffs = [
                round(abs(data["raw_rates"][i] - data["shrunk"][i]), 4)
                for i in range(n)
            ]
            diff_str = ", ".join(_f(d) for d in diffs)
            steps.append(f"|raw-shrunk|=[{diff_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the estimated hyperparameters and first shrunk estimate.

        Args:
            data: Solution data.

        Returns:
            String with a, b estimates and shrinkage.
        """
        result = (
            f"Beta({_f(data['a_est'])},{_f(data['b_est'])}), "
            f"shrunk_1={_f(data['shrunk'][0])}"
        )
        if data["full"]:
            shrunk_str = ", ".join(_f(s) for s in data["shrunk"])
            result = (
                f"Beta({_f(data['a_est'])},{_f(data['b_est'])}), "
                f"shrunk=[{shrunk_str}]"
            )
        return result
