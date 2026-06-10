"""Deep statistics generators -- Bayesian, regression, experimental design.

10 generators at tiers 4-6 covering multiple regression, logistic regression,
residual analysis, experimental design, Bayesian credible vs CI, effect size,
Fisher exact test, rank correlation, categorical analysis, and regression
prediction intervals.
"""
import math

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


def _phi_inv_approx(p: float) -> float:
    """Approximate inverse of the standard normal CDF.

    Uses the Beasley-Springer-Moro rational approximation.

    Args:
        p: Probability in (0, 1).

    Returns:
        Approximate z such that Phi(z) = p.
    """
    if p <= 0.5:
        return -_phi_inv_approx(1.0 - p)
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t * t) / (
        1.0 + d1 * t + d2 * t * t + d3 * t * t * t
    )


# ── 1. Multiple regression (tier 5) ────────────────────────────────────


@register
class MultipleRegressionGenerator(StepGenerator):
    """Compute multiple regression Y = b0 + b1*X1 + b2*X2.

    Uses normal equations for a small dataset (3-5 observations) to
    find coefficients and predicted values.

    Difficulty scaling:
        d1-3: 3 observations, integer data.
        d4-6: 4 observations.
        d7-8: 5 observations.

    Prerequisites:
        linear_regression (tier 4).
    """

    _N_OBS = {
        1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 5,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiple_regression"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        return "compute multiple regression coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multiple regression problem.

        Uses a known model to generate data so the exact solution is known.

        Args:
            difficulty: Controls number of observations.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._N_OBS.get(difficulty, 3)
        b0_true = self._rng.randint(1, 5)
        b1_true = self._rng.randint(1, 4)
        b2_true = self._rng.randint(1, 4)
        x1 = [self._rng.randint(1, 5) for _ in range(n)]
        x2 = [self._rng.randint(1, 5) for _ in range(n)]
        y = [b0_true + b1_true * x1[i] + b2_true * x2[i] for i in range(n)]
        # With exact data the normal equations recover the true coefficients
        y_hat = y[:]
        residuals = [0.0] * n
        data_str = "; ".join(
            f"({x1[i]},{x2[i]},{y[i]})" for i in range(n)
        )
        problem = f"(X1,X2,Y): {data_str}"
        return problem, {
            "b0": b0_true, "b1": b1_true, "b2": b2_true,
            "y_hat": y_hat, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiple regression steps.

        Args:
            data: Solution data with coefficients.

        Returns:
            Steps showing normal equations and coefficients.
        """
        return [
            "set up normal equations X'X*b = X'Y",
            f"b0 = {data['b0']}, b1 = {data['b1']}, b2 = {data['b2']}",
            f"Y = {data['b0']} + {data['b1']}*X1 + {data['b2']}*X2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the regression coefficients.

        Args:
            data: Solution data.

        Returns:
            Formatted coefficients.
        """
        return f"b0={data['b0']}, b1={data['b1']}, b2={data['b2']}"


# ── 2. Logistic regression compute (tier 5) ────────────────────────────


@register
class LogisticRegressionComputeGenerator(StepGenerator):
    """Compute logistic regression probability p = 1/(1+e^(-(b0+b1*x))).

    Given coefficients b0 and b1, computes the probability at a given x,
    the odds ratio, and the log-odds.

    Difficulty scaling:
        d1-3: Small integer coefficients, x in [0,3].
        d4-6: Larger coefficients, x in [0,5].
        d7-8: Two predictors p = 1/(1+e^(-(b0+b1*x1+b2*x2))).

    Prerequisites:
        logarithm (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logistic_regression_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls model complexity.

        Returns:
            Natural language description.
        """
        return "compute logistic regression probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logistic regression computation problem.

        Args:
            difficulty: Controls coefficient range and predictors.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        b0 = self._rng.randint(-3, 3)
        b1 = self._rng.randint(-2, 3)
        if b1 == 0:
            b1 = 1
        if difficulty <= 6:
            x_val = self._rng.randint(0, 3 + difficulty // 2)
            lin = b0 + b1 * x_val
            prob = 1.0 / (1.0 + math.exp(-lin))
            odds = prob / (1.0 - prob) if prob < 1.0 else float("inf")
            problem = f"b0={b0}, b1={b1}, x={x_val}"
        else:
            b2 = self._rng.randint(-2, 2)
            if b2 == 0:
                b2 = 1
            x1 = self._rng.randint(0, 3)
            x2 = self._rng.randint(0, 3)
            lin = b0 + b1 * x1 + b2 * x2
            prob = 1.0 / (1.0 + math.exp(-lin))
            odds = prob / (1.0 - prob) if prob < 1.0 else float("inf")
            problem = f"b0={b0}, b1={b1}, b2={b2}, x1={x1}, x2={x2}"
        return problem, {
            "linear": lin, "prob": prob, "odds": odds,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate logistic regression computation steps.

        Args:
            data: Solution data with linear predictor and probability.

        Returns:
            Steps showing linear combination, sigmoid, odds.
        """
        return [
            f"linear = {_fmt(data['linear'])}",
            f"p = 1/(1+e^(-{_fmt(data['linear'])})) = {_fmt(data['prob'])}",
            f"odds = p/(1-p) = {_fmt(data['odds'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the predicted probability.

        Args:
            data: Solution data.

        Returns:
            Formatted probability.
        """
        return f"p = {_fmt(data['prob'])}"


# ── 3. Residual analysis (tier 5) ──────────────────────────────────────


@register
class ResidualAnalysisGenerator(StepGenerator):
    """Compute residuals and Cook's distance for simple linear regression.

    Given a small dataset and fitted line, computes residuals e_i = y_i - y_hat_i,
    SSE, and leverage-based Cook's distance for the most influential point.

    Difficulty scaling:
        d1-3: 3 data points.
        d4-6: 4 data points.
        d7-8: 5 data points.

    Prerequisites:
        linear_regression (tier 4).
    """

    _N_OBS = {
        1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 5,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "residual_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        return "compute residuals and Cook's distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a residual analysis problem.

        Args:
            difficulty: Controls number of data points.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._N_OBS.get(difficulty, 3)
        # Generate data with known slope and intercept
        b0 = self._rng.randint(1, 5)
        b1 = self._rng.randint(1, 4)
        x_vals = [self._rng.randint(1, 6) for _ in range(n)]
        noise = [self._rng.randint(-2, 2) for _ in range(n)]
        y_vals = [b0 + b1 * x_vals[i] + noise[i] for i in range(n)]
        # Compute simple regression
        x_bar = sum(x_vals) / n
        y_bar = sum(y_vals) / n
        sxy = sum((x_vals[i] - x_bar) * (y_vals[i] - y_bar) for i in range(n))
        sxx = sum((x_vals[i] - x_bar) ** 2 for i in range(n))
        if sxx == 0:
            sxx = 1.0
        slope = sxy / sxx
        intercept = y_bar - slope * x_bar
        y_hat = [intercept + slope * x_vals[i] for i in range(n)]
        residuals = [y_vals[i] - y_hat[i] for i in range(n)]
        sse = sum(r ** 2 for r in residuals)
        mse = sse / (n - 2) if n > 2 else sse
        # Leverage h_i = 1/n + (x_i - x_bar)^2 / sxx
        h_vals = [1.0 / n + (x_vals[i] - x_bar) ** 2 / sxx for i in range(n)]
        # Cook's distance for the max-residual point
        max_idx = max(range(n), key=lambda i: abs(residuals[i]))
        p = 2  # number of parameters
        cook_d = (residuals[max_idx] ** 2 * h_vals[max_idx]) / (
            p * mse * (1 - h_vals[max_idx]) ** 2
        ) if mse > 0 and (1 - h_vals[max_idx]) > 0 else 0.0
        data_str = "; ".join(
            f"({x_vals[i]},{y_vals[i]})" for i in range(n)
        )
        problem = f"data: {data_str}"
        return problem, {
            "slope": slope, "intercept": intercept,
            "residuals": residuals, "sse": sse,
            "cook_d": cook_d, "max_idx": max_idx,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate residual analysis steps.

        Args:
            data: Solution data with residuals and Cook's distance.

        Returns:
            Steps showing fitted line, residuals, and Cook's D.
        """
        resid_str = ", ".join(_fmt(r) for r in data["residuals"])
        return [
            f"fitted: y = {_fmt(data['intercept'])} + {_fmt(data['slope'])}*x",
            f"residuals = [{resid_str}]",
            f"SSE = {_fmt(data['sse'])}",
            f"Cook's D (point {data['max_idx']+1}) = {_fmt(data['cook_d'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return SSE and Cook's distance.

        Args:
            data: Solution data.

        Returns:
            Formatted SSE and Cook's D.
        """
        return f"SSE={_fmt(data['sse'])}, Cook's D={_fmt(data['cook_d'])}"


# ── 4. Experimental design basic (tier 5) ──────────────────────────────


@register
class ExperimentalDesignBasicGenerator(StepGenerator):
    """Compute basic experimental design parameters.

    Calculates sample size for desired power, randomises assignments to
    treatment/control, and estimates treatment effect from a CRD or RBD.

    Difficulty scaling:
        d1-3: CRD with 2 groups, compute treatment effect.
        d4-6: Sample size computation for given effect and power.
        d7-8: RBD with blocking, compute block-adjusted effect.

    Prerequisites:
        hypothesis_test (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "experimental_design_basic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hypothesis_test"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls design complexity.

        Returns:
            Natural language description.
        """
        return "compute experimental design parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an experimental design problem.

        Args:
            difficulty: Controls design type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            # CRD: two groups, compute treatment effect
            n = self._rng.randint(3, 5)
            mu_t = self._rng.randint(10, 20)
            mu_c = self._rng.randint(5, 15)
            treatment = [mu_t + self._rng.randint(-2, 2) for _ in range(n)]
            control = [mu_c + self._rng.randint(-2, 2) for _ in range(n)]
            t_mean = sum(treatment) / n
            c_mean = sum(control) / n
            effect = t_mean - c_mean
            problem = (
                f"treatment={treatment}, control={control}"
            )
            return problem, {
                "design": "CRD", "t_mean": t_mean, "c_mean": c_mean,
                "effect": effect, "n": n,
            }
        elif difficulty <= 6:
            # Sample size: n = (z_alpha + z_beta)^2 * 2 * sigma^2 / delta^2
            sigma = self._rng.randint(2, 6)
            delta = self._rng.randint(1, 4)
            z_alpha = 1.96  # alpha=0.05
            z_beta = 0.8416  # power=0.8
            n_required = math.ceil(
                (z_alpha + z_beta) ** 2 * 2 * sigma ** 2 / delta ** 2
            )
            problem = f"sigma={sigma}, delta={delta}, alpha=0.05, power=0.8"
            return problem, {
                "design": "sample_size", "sigma": sigma, "delta": delta,
                "n_required": n_required,
            }
        else:
            # RBD: 2 blocks, 2 treatments
            blocks = 2
            n_per = self._rng.randint(2, 4)
            block_effects = [self._rng.randint(0, 5) for _ in range(blocks)]
            treat_effect = self._rng.randint(2, 8)
            data_list = []
            for b in range(blocks):
                for t in range(2):
                    vals = [
                        block_effects[b] + t * treat_effect
                        + self._rng.randint(-1, 1)
                        for _ in range(n_per)
                    ]
                    data_list.append((b, t, vals))
            # Compute adjusted effect
            t_vals = [v for (_, t, vs) in data_list if t == 1 for v in vs]
            c_vals = [v for (_, t, vs) in data_list if t == 0 for v in vs]
            effect = sum(t_vals) / len(t_vals) - sum(c_vals) / len(c_vals)
            problem = f"RBD: {blocks} blocks, effect={treat_effect}"
            return problem, {
                "design": "RBD", "effect": effect,
                "treat_effect": treat_effect, "blocks": blocks,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate experimental design steps.

        Args:
            data: Solution data with design parameters.

        Returns:
            Steps showing design type and computations.
        """
        design = data["design"]
        if design == "CRD":
            return [
                f"treatment mean = {_fmt(data['t_mean'])}",
                f"control mean = {_fmt(data['c_mean'])}",
                f"treatment effect = {_fmt(data['effect'])}",
            ]
        elif design == "sample_size":
            return [
                f"z_alpha = 1.96, z_beta = 0.8416",
                f"n = (1.96+0.8416)^2 * 2 * {data['sigma']}^2 / "
                f"{data['delta']}^2",
                f"n = {data['n_required']} per group",
            ]
        else:
            return [
                f"design = RBD with {data['blocks']} blocks",
                f"block-adjusted treatment effect = {_fmt(data['effect'])}",
            ]

    def _create_answer(self, data: dict) -> str:
        """Return the main result of the design computation.

        Args:
            data: Solution data.

        Returns:
            Formatted answer.
        """
        design = data["design"]
        if design == "CRD":
            return f"effect = {_fmt(data['effect'])}"
        elif design == "sample_size":
            return f"n = {data['n_required']} per group"
        else:
            return f"effect = {_fmt(data['effect'])}"


# ── 5. Bayesian credible vs CI (tier 6) ────────────────────────────────


@register
class BayesianCredibleVsCIGenerator(StepGenerator):
    """Compare frequentist CI with Bayesian credible interval.

    Computes a normal CI and a conjugate-prior Bayesian credible interval
    for a normal mean with known variance. Highlights interpretation
    differences.

    Difficulty scaling:
        d1-3: Uninformative prior, results coincide.
        d4-6: Informative prior shifts the interval.
        d7-8: Strong prior with small sample, large difference.

    Prerequisites:
        confidence_interval (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bayesian_credible_vs_ci"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["confidence_interval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls prior strength.

        Returns:
            Natural language description.
        """
        return "compare frequentist CI and Bayesian credible interval"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CI vs credible interval comparison problem.

        Args:
            difficulty: Controls prior informativeness.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(5, 10 + difficulty * 2)
        sigma = self._rng.randint(2, 6)
        x_bar = self._rng.randint(10, 30)
        z = 1.96  # 95%
        # Frequentist CI
        se = sigma / math.sqrt(n)
        ci_lo = x_bar - z * se
        ci_hi = x_bar + z * se
        # Bayesian: conjugate normal prior N(mu_0, tau_0^2)
        if difficulty <= 3:
            tau_0 = 1000.0  # uninformative
            mu_0 = x_bar
        elif difficulty <= 6:
            tau_0 = float(self._rng.randint(3, 8))
            mu_0 = x_bar + self._rng.randint(-5, 5)
        else:
            tau_0 = float(self._rng.randint(1, 3))
            mu_0 = x_bar + self._rng.randint(-8, 8)
        # Posterior: precision-weighted
        prec_prior = 1.0 / (tau_0 ** 2)
        prec_data = n / (sigma ** 2)
        prec_post = prec_prior + prec_data
        mu_post = (prec_prior * mu_0 + prec_data * x_bar) / prec_post
        sigma_post = 1.0 / math.sqrt(prec_post)
        cr_lo = mu_post - z * sigma_post
        cr_hi = mu_post + z * sigma_post
        problem = (
            f"n={n}, x_bar={x_bar}, sigma={sigma}, "
            f"prior: N({mu_0},{_fmt(tau_0)})"
        )
        return problem, {
            "ci": (ci_lo, ci_hi), "cr": (cr_lo, cr_hi),
            "mu_post": mu_post, "sigma_post": sigma_post,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate comparison steps.

        Args:
            data: Solution data with CI and credible interval.

        Returns:
            Steps showing both intervals.
        """
        ci = data["ci"]
        cr = data["cr"]
        return [
            f"95% CI = ({_fmt(ci[0])}, {_fmt(ci[1])})",
            f"posterior mean = {_fmt(data['mu_post'])}, "
            f"posterior sd = {_fmt(data['sigma_post'])}",
            f"95% credible = ({_fmt(cr[0])}, {_fmt(cr[1])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return both intervals.

        Args:
            data: Solution data.

        Returns:
            Formatted CI and credible interval.
        """
        ci = data["ci"]
        cr = data["cr"]
        return (
            f"CI=({_fmt(ci[0])},{_fmt(ci[1])}), "
            f"credible=({_fmt(cr[0])},{_fmt(cr[1])})"
        )


# ── 6. Effect size (tier 4) ────────────────────────────────────────────


@register
class EffectSizeGenerator(StepGenerator):
    """Compute Cohen's d effect size and classify magnitude.

    d = (mean1 - mean2) / s_pooled. Classifications: small (0.2),
    medium (0.5), large (0.8).

    Difficulty scaling:
        d1-3: Small samples (n=3-4), integer data.
        d4-6: Moderate samples (n=5-7).
        d7-8: Larger samples (n=8-10).

    Prerequisites:
        std_dev (tier 3).
    """

    _N_RANGE = {
        1: (3, 4), 2: (3, 4), 3: (3, 4),
        4: (5, 6), 5: (5, 7), 6: (5, 7),
        7: (8, 9), 8: (8, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "effect_size"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute Cohen's d effect size"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an effect size problem.

        Args:
            difficulty: Controls sample size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGE.get(difficulty, (3, 4))
        n1 = self._rng.randint(n_lo, n_hi)
        n2 = self._rng.randint(n_lo, n_hi)
        base1 = self._rng.randint(10, 20)
        base2 = base1 + self._rng.randint(1, 8)
        g1 = [base1 + self._rng.randint(-3, 3) for _ in range(n1)]
        g2 = [base2 + self._rng.randint(-3, 3) for _ in range(n2)]
        m1 = sum(g1) / n1
        m2 = sum(g2) / n2
        var1 = sum((x - m1) ** 2 for x in g1) / (n1 - 1)
        var2 = sum((x - m2) ** 2 for x in g2) / (n2 - 1)
        s_pooled = math.sqrt(
            ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
        )
        d = (m2 - m1) / s_pooled if s_pooled > 0 else 0.0
        abs_d = abs(d)
        if abs_d >= 0.8:
            classification = "large"
        elif abs_d >= 0.5:
            classification = "medium"
        else:
            classification = "small"
        problem = f"g1={g1}, g2={g2}"
        return problem, {
            "m1": m1, "m2": m2, "s_pooled": s_pooled,
            "d": d, "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate effect size computation steps.

        Args:
            data: Solution data with means and pooled SD.

        Returns:
            Steps showing means, pooled SD, and Cohen's d.
        """
        return [
            f"mean1 = {_fmt(data['m1'])}, mean2 = {_fmt(data['m2'])}",
            f"s_pooled = {_fmt(data['s_pooled'])}",
            f"d = ({_fmt(data['m2'])}-{_fmt(data['m1'])})/{_fmt(data['s_pooled'])} = {_fmt(data['d'])}",
            f"classification: {data['classification']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return Cohen's d and its classification.

        Args:
            data: Solution data.

        Returns:
            Formatted effect size.
        """
        return f"d = {_fmt(data['d'])}, {data['classification']}"


# ── 7. Fisher exact test (tier 5) ──────────────────────────────────────


@register
class FisherExactTestGenerator(StepGenerator):
    """Compute Fisher's exact test p-value for a 2x2 contingency table.

    p = C(a+b,a)*C(c+d,c)/C(n,a+c). The table is [[a,b],[c,d]].

    Difficulty scaling:
        d1-3: Small cell counts (1-5).
        d4-6: Moderate cell counts (3-8).
        d7-8: Larger cell counts (5-12).

    Prerequisites:
        basic_prob (tier 2).
    """

    _RANGE = {
        1: (1, 4), 2: (1, 5), 3: (1, 5),
        4: (3, 7), 5: (3, 8), 6: (3, 8),
        7: (5, 10), 8: (5, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fisher_exact_test"

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
            difficulty: Controls cell count range.

        Returns:
            Natural language description.
        """
        return "compute Fisher's exact test p-value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fisher's exact test problem.

        Args:
            difficulty: Controls table size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGE.get(difficulty, (1, 5))
        a = self._rng.randint(lo, hi)
        b = self._rng.randint(lo, hi)
        c = self._rng.randint(lo, hi)
        d = self._rng.randint(lo, hi)
        n = a + b + c + d
        # p = C(a+b,a) * C(c+d,c) / C(n,a+c)
        p_val = (
            math.comb(a + b, a) * math.comb(c + d, c) / math.comb(n, a + c)
        )
        problem = f"[[{a},{b}],[{c},{d}]]"
        return problem, {
            "a": a, "b": b, "c": c, "d": d, "n": n, "p": p_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fisher's exact test steps.

        Args:
            data: Solution data with cell counts and p-value.

        Returns:
            Steps showing combinatorial computation.
        """
        a, b, c, d = data["a"], data["b"], data["c"], data["d"]
        return [
            f"table: [[{a},{b}],[{c},{d}]], n={data['n']}",
            f"p = C({a+b},{a})*C({c+d},{c})/C({data['n']},{a+c})",
            f"p = {_fmt(data['p'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the p-value.

        Args:
            data: Solution data.

        Returns:
            Formatted p-value.
        """
        return f"p = {_fmt(data['p'])}"


# ── 8. Rank correlation (tier 5) ───────────────────────────────────────


@register
class RankCorrelationGenerator(StepGenerator):
    """Compute Spearman's rank correlation coefficient.

    rho = 1 - 6*sum(d_i^2)/(n*(n^2-1)) where d_i are rank differences.

    Difficulty scaling:
        d1-3: n=4-5 observations.
        d4-6: n=6-7 observations.
        d7-8: n=8-10 observations.

    Prerequisites:
        division (tier 1).
    """

    _N_RANGE = {
        1: (4, 5), 2: (4, 5), 3: (4, 5),
        4: (6, 6), 5: (6, 7), 6: (6, 7),
        7: (8, 9), 8: (8, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rank_correlation"

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
            difficulty: Controls sample size.

        Returns:
            Natural language description.
        """
        return "compute Spearman's rank correlation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Spearman rank correlation problem.

        Args:
            difficulty: Controls number of observations.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGE.get(difficulty, (4, 5))
        n = self._rng.randint(n_lo, n_hi)
        # Generate two permutations of ranks
        ranks_x = list(range(1, n + 1))
        ranks_y = list(range(1, n + 1))
        self._rng.shuffle(ranks_y)
        d_sq = sum((rx - ry) ** 2 for rx, ry in zip(ranks_x, ranks_y))
        rho = 1.0 - 6.0 * d_sq / (n * (n * n - 1))
        problem = f"ranks_x={ranks_x}, ranks_y={ranks_y}"
        return problem, {
            "ranks_x": ranks_x, "ranks_y": ranks_y,
            "d_sq": d_sq, "n": n, "rho": rho,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rank correlation steps.

        Args:
            data: Solution data with ranks and d^2.

        Returns:
            Steps showing rank differences and rho.
        """
        d_vals = [
            rx - ry for rx, ry in zip(data["ranks_x"], data["ranks_y"])
        ]
        d_str = ", ".join(str(d) for d in d_vals)
        return [
            f"d_i = [{d_str}]",
            f"sum(d_i^2) = {data['d_sq']}",
            f"rho = 1 - 6*{data['d_sq']}/({data['n']}*{data['n']**2-1}) = {_fmt(data['rho'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return Spearman's rho.

        Args:
            data: Solution data.

        Returns:
            Formatted correlation coefficient.
        """
        return f"rho = {_fmt(data['rho'])}"


# ── 9. Categorical analysis (tier 5) ───────────────────────────────────


@register
class CategoricalAnalysisGenerator(StepGenerator):
    """Analyse a contingency table: expected frequencies, chi-square, Cramer's V.

    Computes expected = row_total*col_total/n, chi^2 = sum (O-E)^2/E,
    and Cramer's V = sqrt(chi^2 / (n*min(r-1,c-1))).

    Difficulty scaling:
        d1-3: 2x2 table with small counts.
        d4-6: 2x3 table.
        d7-8: 3x3 table.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "categorical_analysis"

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
            difficulty: Controls table dimensions.

        Returns:
            Natural language description.
        """
        return "compute chi-square and Cramer's V for a contingency table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a categorical analysis problem.

        Args:
            difficulty: Controls table dimensions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            rows, cols = 2, 2
        elif difficulty <= 6:
            rows, cols = 2, 3
        else:
            rows, cols = 3, 3
        table = [
            [self._rng.randint(5, 15 + difficulty * 2) for _ in range(cols)]
            for _ in range(rows)
        ]
        n = sum(sum(row) for row in table)
        row_totals = [sum(row) for row in table]
        col_totals = [sum(table[r][c] for r in range(rows)) for c in range(cols)]
        # Expected frequencies
        expected = [
            [row_totals[r] * col_totals[c] / n for c in range(cols)]
            for r in range(rows)
        ]
        # Chi-square
        chi_sq = sum(
            (table[r][c] - expected[r][c]) ** 2 / expected[r][c]
            for r in range(rows) for c in range(cols)
            if expected[r][c] > 0
        )
        # Cramer's V
        k = min(rows - 1, cols - 1)
        v = math.sqrt(chi_sq / (n * k)) if n * k > 0 else 0.0
        table_str = "; ".join(
            f"[{','.join(str(x) for x in row)}]" for row in table
        )
        problem = f"table: [{table_str}]"
        return problem, {
            "table": table, "chi_sq": chi_sq, "v": v, "n": n,
            "rows": rows, "cols": cols,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate categorical analysis steps.

        Args:
            data: Solution data with chi-square and Cramer's V.

        Returns:
            Steps showing expected frequencies, chi^2, V.
        """
        return [
            f"n = {data['n']}, {data['rows']}x{data['cols']} table",
            f"compute expected = row_total*col_total/n",
            f"chi^2 = sum((O-E)^2/E) = {_fmt(data['chi_sq'])}",
            f"Cramer's V = {_fmt(data['v'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return chi-square and Cramer's V.

        Args:
            data: Solution data.

        Returns:
            Formatted statistics.
        """
        return f"chi^2={_fmt(data['chi_sq'])}, V={_fmt(data['v'])}"


# ── 10. Regression prediction interval (tier 5) ────────────────────────


@register
class RegressionPredictionIntervalGenerator(StepGenerator):
    """Compute a prediction interval for simple linear regression.

    PI = y_hat +/- t*s*sqrt(1 + 1/n + (x-x_bar)^2/Sxx).
    Uses z=1.96 as approximation to t for simplicity.

    Difficulty scaling:
        d1-3: 4 data points.
        d4-6: 6 data points.
        d7-8: 8 data points.

    Prerequisites:
        linear_regression (tier 4).
    """

    _N_OBS = {
        1: 4, 2: 4, 3: 4, 4: 6, 5: 6, 6: 6, 7: 8, 8: 8,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regression_prediction_interval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        return "compute a 95% prediction interval for regression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regression prediction interval problem.

        Args:
            difficulty: Controls number of data points.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._N_OBS.get(difficulty, 4)
        b0 = self._rng.randint(1, 5)
        b1 = self._rng.randint(1, 4)
        x_vals = [self._rng.randint(1, 8) for _ in range(n)]
        noise = [self._rng.randint(-2, 2) for _ in range(n)]
        y_vals = [b0 + b1 * x_vals[i] + noise[i] for i in range(n)]
        x_bar = sum(x_vals) / n
        y_bar = sum(y_vals) / n
        sxy = sum((x_vals[i] - x_bar) * (y_vals[i] - y_bar) for i in range(n))
        sxx = sum((x_vals[i] - x_bar) ** 2 for i in range(n))
        if sxx == 0:
            sxx = 1.0
        slope = sxy / sxx
        intercept = y_bar - slope * x_bar
        # Predict at a new x
        x_new = self._rng.randint(1, 10)
        y_hat = intercept + slope * x_new
        y_fitted = [intercept + slope * x_vals[i] for i in range(n)]
        sse = sum((y_vals[i] - y_fitted[i]) ** 2 for i in range(n))
        s = math.sqrt(sse / (n - 2)) if n > 2 else 1.0
        margin = 1.96 * s * math.sqrt(1.0 + 1.0 / n + (x_new - x_bar) ** 2 / sxx)
        pi_lo = y_hat - margin
        pi_hi = y_hat + margin
        data_str = "; ".join(f"({x_vals[i]},{y_vals[i]})" for i in range(n))
        problem = f"data: {data_str}, predict x={x_new}"
        return problem, {
            "slope": slope, "intercept": intercept,
            "x_new": x_new, "y_hat": y_hat, "s": s,
            "margin": margin, "pi": (pi_lo, pi_hi),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate prediction interval steps.

        Args:
            data: Solution data with fitted line and interval.

        Returns:
            Steps showing regression, prediction, and interval.
        """
        pi = data["pi"]
        return [
            f"y = {_fmt(data['intercept'])} + {_fmt(data['slope'])}*x",
            f"y_hat({data['x_new']}) = {_fmt(data['y_hat'])}",
            f"s = {_fmt(data['s'])}, margin = {_fmt(data['margin'])}",
            f"95% PI = ({_fmt(pi[0])}, {_fmt(pi[1])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the prediction interval.

        Args:
            data: Solution data.

        Returns:
            Formatted prediction interval.
        """
        pi = data["pi"]
        return f"PI = ({_fmt(pi[0])}, {_fmt(pi[1])})"
