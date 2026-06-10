"""Causal inference generators -- ATE, propensity scores, IV, DiD, RD, do-calculus.

Covers average treatment effect estimation, inverse probability weighting,
instrumental variables, difference-in-differences, regression discontinuity,
and do-calculus with d-separation. Tiers range from 5 to 7.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _CIFmt:
    """Formats numeric values for causal inference problems.

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


_f = _CIFmt.f


# ===================================================================
# 1. Average treatment effect  (tier 5)
# ===================================================================

@register
class ATEComputeGenerator(StepGenerator):
    """Average treatment effect: ATE = E[Y(1)] - E[Y(0)].

    Computes the ATE from experimental data where units are randomly
    assigned to treatment (T=1) or control (T=0).

    Difficulty scaling:
        Difficulty 1-3: 4-6 units per group, integer outcomes.
        Difficulty 4-6: 6-10 units, decimal outcomes, compute SE.
        Difficulty 7-8: 10-15 units, also compute 95% CI for ATE.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ate_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute average treatment effect from experimental data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate treatment and control outcomes, compute ATE.

        Args:
            difficulty: Controls sample size and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_t = self._rng.randint(4, 6)
            n_c = self._rng.randint(4, 6)
            y_treat = [float(self._rng.randint(5, 20)) for _ in range(n_t)]
            y_control = [float(self._rng.randint(3, 15)) for _ in range(n_c)]
        elif difficulty <= 6:
            n_t = self._rng.randint(6, 10)
            n_c = self._rng.randint(6, 10)
            y_treat = [round(self._rng.uniform(5, 25), 1) for _ in range(n_t)]
            y_control = [round(self._rng.uniform(3, 20), 1) for _ in range(n_c)]
        else:
            n_t = self._rng.randint(10, 15)
            n_c = self._rng.randint(10, 15)
            y_treat = [round(self._rng.uniform(5, 30), 1) for _ in range(n_t)]
            y_control = [round(self._rng.uniform(3, 25), 1) for _ in range(n_c)]

        mean_t = round(sum(y_treat) / n_t, 4)
        mean_c = round(sum(y_control) / n_c, 4)
        ate = round(mean_t - mean_c, 4)

        data = {
            "n_t": n_t, "n_c": n_c,
            "y_treat": y_treat, "y_control": y_control,
            "mean_t": mean_t, "mean_c": mean_c, "ATE": ate,
            "full": difficulty >= 4,
        }

        if difficulty >= 4:
            var_t = round(
                sum((y - mean_t) ** 2 for y in y_treat) / max(n_t - 1, 1), 4
            )
            var_c = round(
                sum((y - mean_c) ** 2 for y in y_control) / max(n_c - 1, 1), 4
            )
            se = round(math.sqrt(var_t / n_t + var_c / n_c), 4)
            data["var_t"] = var_t
            data["var_c"] = var_c
            data["SE"] = se

        if difficulty >= 7:
            ci_lo = round(ate - 1.96 * se, 4)
            ci_hi = round(ate + 1.96 * se, 4)
            data["CI_lo"] = ci_lo
            data["CI_hi"] = ci_hi

        return "ATE = E[Y(1)] - E[Y(0)]", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ATE computation steps.

        Args:
            data: Solution data with treatment and control means.

        Returns:
            List of step strings.
        """
        steps = [
            f"n_treat={data['n_t']}, n_control={data['n_c']}",
            f"E[Y(1)]={_f(data['mean_t'])}, E[Y(0)]={_f(data['mean_c'])}",
            f"ATE = {_f(data['mean_t'])} - {_f(data['mean_c'])} = {_f(data['ATE'])}",
        ]
        if data["full"]:
            steps.append(f"SE = {_f(data['SE'])}")
        if "CI_lo" in data:
            steps.append(
                f"95% CI = [{_f(data['CI_lo'])}, {_f(data['CI_hi'])}]"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ATE.

        Args:
            data: Solution data.

        Returns:
            String with ATE value.
        """
        result = f"ATE = {_f(data['ATE'])}"
        if data["full"]:
            result += f", SE = {_f(data['SE'])}"
        if "CI_lo" in data:
            result += f", CI=[{_f(data['CI_lo'])},{_f(data['CI_hi'])}]"
        return result


# ===================================================================
# 2. Propensity score / IPW  (tier 6)
# ===================================================================

@register
class PropensityScoreGenerator(StepGenerator):
    """Propensity score IPW: ATE = mean(Y*T/e - Y*(1-T)/(1-e)).

    Computes propensity scores e(x) from a simple logistic model
    and uses inverse probability weighting to estimate the ATE.

    Difficulty scaling:
        Difficulty 1-3: 4-6 units, given propensity scores.
        Difficulty 4-6: 6-8 units, compute e from logistic.
        Difficulty 7-8: 8-10 units, also compute Hajek estimator.

    Prerequisites:
        linear_regression.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "propensity_score"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute IPW estimate of ATE using propensity scores"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate units with covariates, propensity scores, and IPW estimate.

        Args:
            difficulty: Controls sample size and estimation method.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 8)
        else:
            n = self._rng.randint(8, 10)

        # Generate covariate and treatment assignment
        beta0 = round(self._rng.uniform(-1, 1), 2)
        beta1 = round(self._rng.uniform(-2, 2), 2)

        x_vals = [round(self._rng.uniform(-2, 2), 1) for _ in range(n)]
        logit = [beta0 + beta1 * x for x in x_vals]
        e_scores = [round(1.0 / (1.0 + math.exp(-lo)), 4) for lo in logit]

        # Clip propensity scores to avoid extreme weights
        e_scores = [round(max(0.05, min(0.95, e)), 4) for e in e_scores]

        treatment = [1 if self._rng.random() < e else 0 for e in e_scores]

        # Ensure at least one treated and one control
        if sum(treatment) == 0:
            treatment[0] = 1
        if sum(treatment) == n:
            treatment[-1] = 0

        # Outcomes
        y_vals = [
            round(self._rng.uniform(5, 20) + (3 if t == 1 else 0), 1)
            for t in treatment
        ]

        # Horvitz-Thompson IPW
        ipw_terms = []
        for i in range(n):
            t = treatment[i]
            e = e_scores[i]
            y = y_vals[i]
            term = round(y * t / e - y * (1 - t) / (1 - e), 4)
            ipw_terms.append(term)

        ate_ipw = round(sum(ipw_terms) / n, 4)

        data = {
            "n": n, "x": x_vals, "e": e_scores,
            "T": treatment, "Y": y_vals,
            "ipw_terms": ipw_terms, "ATE_IPW": ate_ipw,
            "beta0": beta0, "beta1": beta1,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            # Hajek estimator (normalised weights)
            w1_sum = round(sum(
                treatment[i] / e_scores[i] for i in range(n)
            ), 4)
            w0_sum = round(sum(
                (1 - treatment[i]) / (1 - e_scores[i]) for i in range(n)
            ), 4)
            hajek_t = round(sum(
                y_vals[i] * treatment[i] / e_scores[i] for i in range(n)
            ) / w1_sum if w1_sum > 0 else 0, 4)
            hajek_c = round(sum(
                y_vals[i] * (1 - treatment[i]) / (1 - e_scores[i]) for i in range(n)
            ) / w0_sum if w0_sum > 0 else 0, 4)
            ate_hajek = round(hajek_t - hajek_c, 4)
            data["ATE_Hajek"] = ate_hajek

        return "\\hat{ATE}_{IPW} = \\frac{1}{n}\\sum \\frac{Y_i T_i}{e_i} - \\frac{Y_i(1-T_i)}{1-e_i}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate IPW computation steps.

        Args:
            data: Solution data with propensity scores and IPW terms.

        Returns:
            List of step strings.
        """
        n = data["n"]
        e_str = ", ".join(_f(e) for e in data["e"][:4])
        if n > 4:
            e_str += ", ..."
        steps = [
            f"n={n}, e=[{e_str}]",
            f"sum(IPW terms) = {_f(sum(data['ipw_terms']))}",
            f"ATE_IPW = {_f(data['ATE_IPW'])}",
        ]
        if data["full"]:
            steps.append(f"ATE_Hajek = {_f(data['ATE_Hajek'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the IPW ATE estimate.

        Args:
            data: Solution data.

        Returns:
            String with ATE_IPW.
        """
        result = f"ATE_IPW = {_f(data['ATE_IPW'])}"
        if data["full"]:
            result += f", ATE_Hajek = {_f(data['ATE_Hajek'])}"
        return result


# ===================================================================
# 3. Instrumental variable  (tier 6)
# ===================================================================

@register
class InstrumentalVariableGenerator(StepGenerator):
    """IV estimator: beta_IV = Cov(Y,Z)/Cov(X,Z).

    Given data on outcome Y, endogenous regressor X, and instrument Z,
    computes the instrumental variable estimate of the causal effect.

    Difficulty scaling:
        Difficulty 1-3: 5-8 observations, integer values.
        Difficulty 4-6: 8-12 observations, decimal values.
        Difficulty 7-8: 12-15 observations, also compute Wald estimate.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "instrumental_variable"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute IV estimate of causal effect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Y, X, Z data and compute beta_IV = Cov(Y,Z)/Cov(X,Z).

        Args:
            difficulty: Controls sample size and data complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 8)
            z = [float(self._rng.randint(0, 1)) for _ in range(n)]
            x = [round(z[i] * self._rng.randint(2, 5) + self._rng.randint(0, 3), 1) for i in range(n)]
            beta_true = self._rng.randint(2, 6)
            y = [round(beta_true * x[i] + self._rng.randint(-2, 2), 1) for i in range(n)]
        elif difficulty <= 6:
            n = self._rng.randint(8, 12)
            z = [float(self._rng.randint(0, 1)) for _ in range(n)]
            x = [round(z[i] * self._rng.uniform(1, 4) + self._rng.uniform(0, 3), 2) for i in range(n)]
            beta_true = round(self._rng.uniform(1, 5), 1)
            y = [round(beta_true * x[i] + self._rng.uniform(-3, 3), 2) for i in range(n)]
        else:
            n = self._rng.randint(12, 15)
            z = [float(self._rng.randint(0, 1)) for _ in range(n)]
            x = [round(z[i] * self._rng.uniform(1, 5) + self._rng.uniform(0, 4), 2) for i in range(n)]
            beta_true = round(self._rng.uniform(1, 6), 1)
            y = [round(beta_true * x[i] + self._rng.uniform(-4, 4), 2) for i in range(n)]

        # Compute means
        y_bar = sum(y) / n
        x_bar = sum(x) / n
        z_bar = sum(z) / n

        # Covariances
        cov_yz = round(sum((y[i] - y_bar) * (z[i] - z_bar) for i in range(n)) / n, 4)
        cov_xz = round(sum((x[i] - x_bar) * (z[i] - z_bar) for i in range(n)) / n, 4)

        if abs(cov_xz) < 0.001:
            cov_xz = 0.1  # avoid division by zero

        beta_iv = round(cov_yz / cov_xz, 4)

        data = {
            "n": n, "Y": y, "X": x, "Z": z,
            "y_bar": round(y_bar, 4), "x_bar": round(x_bar, 4),
            "z_bar": round(z_bar, 4),
            "cov_yz": cov_yz, "cov_xz": cov_xz,
            "beta_IV": beta_iv,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            # Wald estimate (binary instrument): beta = (E[Y|Z=1]-E[Y|Z=0])/(E[X|Z=1]-E[X|Z=0])
            y_z1 = [y[i] for i in range(n) if z[i] == 1]
            y_z0 = [y[i] for i in range(n) if z[i] == 0]
            x_z1 = [x[i] for i in range(n) if z[i] == 1]
            x_z0 = [x[i] for i in range(n) if z[i] == 0]

            ey1 = round(sum(y_z1) / max(len(y_z1), 1), 4)
            ey0 = round(sum(y_z0) / max(len(y_z0), 1), 4)
            ex1 = round(sum(x_z1) / max(len(x_z1), 1), 4)
            ex0 = round(sum(x_z0) / max(len(x_z0), 1), 4)

            denom_wald = ex1 - ex0
            if abs(denom_wald) < 0.001:
                denom_wald = 0.1
            beta_wald = round((ey1 - ey0) / denom_wald, 4)
            data["beta_Wald"] = beta_wald

        return "\\hat{\\beta}_{IV} = \\frac{Cov(Y,Z)}{Cov(X,Z)}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate IV estimation steps.

        Args:
            data: Solution data with covariances and IV estimate.

        Returns:
            List of step strings.
        """
        steps = [
            f"n={data['n']}, y_bar={_f(data['y_bar'])}, x_bar={_f(data['x_bar'])}",
            f"Cov(Y,Z)={_f(data['cov_yz'])}, Cov(X,Z)={_f(data['cov_xz'])}",
            f"beta_IV = {_f(data['cov_yz'])}/{_f(data['cov_xz'])} = {_f(data['beta_IV'])}",
        ]
        if data["full"]:
            steps.append(f"Wald estimate = {_f(data['beta_Wald'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the IV estimate.

        Args:
            data: Solution data.

        Returns:
            String with beta_IV.
        """
        result = f"beta_IV = {_f(data['beta_IV'])}"
        if data["full"]:
            result += f", beta_Wald = {_f(data['beta_Wald'])}"
        return result


# ===================================================================
# 4. Difference-in-differences  (tier 5)
# ===================================================================

@register
class DiffInDiffGenerator(StepGenerator):
    """DiD: (Y_treat_post - Y_treat_pre) - (Y_control_post - Y_control_pre).

    Computes the difference-in-differences estimate from a 2x2 table
    of before/after outcomes for treatment and control groups.

    Difficulty scaling:
        Difficulty 1-3: integer outcomes, basic DiD.
        Difficulty 4-6: decimal outcomes, compute relative change.
        Difficulty 7-8: also compute group means and parallel trend check.

    Prerequisites:
        subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diff_in_diff"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute difference-in-differences estimate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2x2 before/after data and compute DiD.

        Args:
            difficulty: Controls value ranges and extras.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            y_tp = float(self._rng.randint(40, 80))
            y_t0 = float(self._rng.randint(30, 60))
            y_cp = float(self._rng.randint(35, 70))
            y_c0 = float(self._rng.randint(30, 60))
        elif difficulty <= 6:
            y_tp = round(self._rng.uniform(40, 90), 1)
            y_t0 = round(self._rng.uniform(30, 70), 1)
            y_cp = round(self._rng.uniform(35, 80), 1)
            y_c0 = round(self._rng.uniform(30, 65), 1)
        else:
            y_tp = round(self._rng.uniform(50, 100), 1)
            y_t0 = round(self._rng.uniform(30, 70), 1)
            y_cp = round(self._rng.uniform(40, 85), 1)
            y_c0 = round(self._rng.uniform(30, 70), 1)

        d_treat = round(y_tp - y_t0, 4)
        d_control = round(y_cp - y_c0, 4)
        did = round(d_treat - d_control, 4)

        data = {
            "Y_treat_post": y_tp, "Y_treat_pre": y_t0,
            "Y_control_post": y_cp, "Y_control_pre": y_c0,
            "D_treat": d_treat, "D_control": d_control, "DiD": did,
            "full": difficulty >= 4,
        }

        if difficulty >= 4:
            # Relative change
            rel_treat = round(d_treat / y_t0 * 100, 4) if y_t0 != 0 else 0.0
            rel_control = round(d_control / y_c0 * 100, 4) if y_c0 != 0 else 0.0
            data["rel_treat"] = rel_treat
            data["rel_control"] = rel_control

        if difficulty >= 7:
            # Parallel trends: pre-trends difference
            data["pre_gap"] = round(y_t0 - y_c0, 4)
            data["post_gap"] = round(y_tp - y_cp, 4)

        return "DiD = (Y^T_1 - Y^T_0) - (Y^C_1 - Y^C_0)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DiD computation steps.

        Args:
            data: Solution data with 2x2 table values.

        Returns:
            List of step strings.
        """
        steps = [
            f"treat: pre={_f(data['Y_treat_pre'])}, post={_f(data['Y_treat_post'])}",
            f"control: pre={_f(data['Y_control_pre'])}, post={_f(data['Y_control_post'])}",
            f"D_treat={_f(data['D_treat'])}, D_control={_f(data['D_control'])}",
            f"DiD = {_f(data['D_treat'])} - {_f(data['D_control'])} = {_f(data['DiD'])}",
        ]
        if data["full"]:
            steps.append(
                f"rel_treat={_f(data['rel_treat'])}%, rel_control={_f(data['rel_control'])}%"
            )
        if "pre_gap" in data:
            steps.append(
                f"pre_gap={_f(data['pre_gap'])}, post_gap={_f(data['post_gap'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the DiD estimate.

        Args:
            data: Solution data.

        Returns:
            String with DiD.
        """
        result = f"DiD = {_f(data['DiD'])}"
        if data["full"]:
            result += f", rel_treat={_f(data['rel_treat'])}%"
        return result


# ===================================================================
# 5. Regression discontinuity  (tier 6)
# ===================================================================

@register
class RegressionDiscontinuityGenerator(StepGenerator):
    """RD estimate: compare outcomes just above vs just below cutoff.

    Computes the local average treatment effect at a sharp cutoff
    by comparing mean outcomes in narrow bands above and below.

    Difficulty scaling:
        Difficulty 1-3: 3-4 units each side, integer outcomes.
        Difficulty 4-6: 5-7 units each side, decimal values, bandwidth.
        Difficulty 7-8: 7-10 units, fit local linear on each side.

    Prerequisites:
        linear_regression.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regression_discontinuity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute regression discontinuity treatment effect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate data near a cutoff and compute the RD estimate.

        Args:
            difficulty: Controls sample size and estimation method.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        cutoff = round(self._rng.uniform(40, 60), 1)

        if difficulty <= 3:
            n_below = self._rng.randint(3, 4)
            n_above = self._rng.randint(3, 4)
            bw = 5.0
        elif difficulty <= 6:
            n_below = self._rng.randint(5, 7)
            n_above = self._rng.randint(5, 7)
            bw = round(self._rng.uniform(3, 8), 1)
        else:
            n_below = self._rng.randint(7, 10)
            n_above = self._rng.randint(7, 10)
            bw = round(self._rng.uniform(2, 6), 1)

        # Running variable: below cutoff
        x_below = [round(cutoff - self._rng.uniform(0.1, bw), 2) for _ in range(n_below)]
        x_above = [round(cutoff + self._rng.uniform(0.1, bw), 2) for _ in range(n_above)]

        # Outcomes: jump at cutoff
        tau = round(self._rng.uniform(2, 10), 1)
        slope = round(self._rng.uniform(0.1, 0.5), 2)
        y_below = [round(slope * (x - cutoff) + self._rng.uniform(-1, 1), 2) for x in x_below]
        y_above = [round(tau + slope * (x - cutoff) + self._rng.uniform(-1, 1), 2) for x in x_above]

        mean_below = round(sum(y_below) / n_below, 4)
        mean_above = round(sum(y_above) / n_above, 4)
        rd_estimate = round(mean_above - mean_below, 4)

        data = {
            "cutoff": cutoff, "bw": bw,
            "n_below": n_below, "n_above": n_above,
            "mean_below": mean_below, "mean_above": mean_above,
            "RD": rd_estimate,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            # Local linear: simple OLS on each side
            # Below: y = a0 + b0*(x - cutoff)
            x_cent_b = [x - cutoff for x in x_below]
            sx2_b = sum(xc ** 2 for xc in x_cent_b)
            sxy_b = sum(x_cent_b[i] * y_below[i] for i in range(n_below))
            b0 = round(sxy_b / sx2_b, 4) if sx2_b > 0 else 0.0
            a0 = round(mean_below - b0 * sum(x_cent_b) / n_below, 4)

            x_cent_a = [x - cutoff for x in x_above]
            sx2_a = sum(xc ** 2 for xc in x_cent_a)
            sxy_a = sum(x_cent_a[i] * y_above[i] for i in range(n_above))
            b1 = round(sxy_a / sx2_a, 4) if sx2_a > 0 else 0.0
            a1 = round(mean_above - b1 * sum(x_cent_a) / n_above, 4)

            rd_ll = round(a1 - a0, 4)
            data["a0"] = a0
            data["a1"] = a1
            data["RD_local_linear"] = rd_ll

        return "\\hat{\\tau}_{RD} = \\lim_{x \\to c^+} E[Y|X] - \\lim_{x \\to c^-} E[Y|X]", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate RD computation steps.

        Args:
            data: Solution data with cutoff, means, and RD estimate.

        Returns:
            List of step strings.
        """
        steps = [
            f"cutoff={_f(data['cutoff'])}, bandwidth={_f(data['bw'])}",
            f"n_below={data['n_below']}, n_above={data['n_above']}",
            f"mean_below={_f(data['mean_below'])}, mean_above={_f(data['mean_above'])}",
            f"RD = {_f(data['mean_above'])} - {_f(data['mean_below'])} = {_f(data['RD'])}",
        ]
        if data["full"]:
            steps.append(
                f"local linear: a0={_f(data['a0'])}, a1={_f(data['a1'])}, "
                f"RD_ll={_f(data['RD_local_linear'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the RD estimate.

        Args:
            data: Solution data.

        Returns:
            String with RD estimate.
        """
        result = f"RD = {_f(data['RD'])}"
        if data["full"]:
            result += f", RD_local_linear = {_f(data['RD_local_linear'])}"
        return result


# ===================================================================
# 6. Do-calculus  (tier 7)
# ===================================================================

@register
class DoCalculusGenerator(StepGenerator):
    """Do-calculus: determine if P(Y|do(X)) = P(Y|X) via d-separation.

    Given a causal DAG from a template set, applies d-separation
    rules to determine whether the interventional distribution
    equals the observational one (no confounding) or requires
    adjustment. Identifies confounders and the adjustment formula.

    Difficulty scaling:
        Difficulty 1-3: 3-node DAG, simple chain or fork.
        Difficulty 4-6: 4-node DAG, one confounder.
        Difficulty 7-8: 4-5 node DAG, mediator + confounder.

    Prerequisites:
        conditional_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "do_calculus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conditional_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply d-separation to identify causal effect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a causal DAG template and determine identifiability.

        Args:
            difficulty: Controls DAG complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Template: chain X -> M -> Y or fork X <- C -> Y
            template = self._rng.choice(["chain", "fork", "direct"])
            if template == "chain":
                nodes = ["X", "M", "Y"]
                edges = [("X", "M"), ("M", "Y")]
                confounders = []
                identifiable = True
                formula = "P(Y|do(X)) = sum_M P(Y|M)P(M|X)"
            elif template == "fork":
                nodes = ["X", "Y", "C"]
                edges = [("C", "X"), ("C", "Y")]
                confounders = ["C"]
                identifiable = True
                formula = "P(Y|do(X)) = sum_C P(Y|X,C)P(C)"
            else:
                nodes = ["X", "Y"]
                edges = [("X", "Y")]
                confounders = []
                identifiable = True
                formula = "P(Y|do(X)) = P(Y|X)"
        elif difficulty <= 6:
            # Template: confounded X -> Y with X <- C -> Y
            template = self._rng.choice(["confounded", "mediator_conf"])
            if template == "confounded":
                nodes = ["X", "Y", "C", "Z"]
                edges = [("C", "X"), ("C", "Y"), ("X", "Y"), ("Z", "X")]
                confounders = ["C"]
                identifiable = True
                formula = "P(Y|do(X)) = sum_C P(Y|X,C)P(C)"
            else:
                nodes = ["X", "M", "Y", "C"]
                edges = [("X", "M"), ("M", "Y"), ("C", "X"), ("C", "Y")]
                confounders = ["C"]
                identifiable = True
                formula = "P(Y|do(X)) = sum_C P(Y|X,C)P(C)"
        else:
            # Template: front-door or complex
            template = self._rng.choice(["front_door", "complex"])
            if template == "front_door":
                nodes = ["X", "M", "Y", "U"]
                edges = [("U", "X"), ("U", "Y"), ("X", "M"), ("M", "Y")]
                confounders = ["U"]
                identifiable = True
                formula = "P(Y|do(X)) = sum_M P(M|X) sum_X' P(Y|X',M)P(X')"
            else:
                nodes = ["X", "Y", "C1", "C2", "M"]
                edges = [
                    ("C1", "X"), ("C1", "M"), ("C2", "M"),
                    ("C2", "Y"), ("X", "M"), ("M", "Y"),
                ]
                confounders = ["C1", "C2"]
                identifiable = True
                formula = "P(Y|do(X)) = sum_{C1,C2} P(Y|X,C1,C2)P(C1)P(C2)"

        edges_str = ", ".join(f"{a}->{b}" for a, b in edges)

        # Generate simple numeric probabilities for the answer
        p_yx = round(self._rng.uniform(0.2, 0.8), 4)

        data = {
            "template": template, "nodes": nodes,
            "edges": edges, "edges_str": edges_str,
            "confounders": confounders,
            "identifiable": identifiable,
            "formula": formula,
            "P_Y_do_X": p_yx,
            "full": difficulty >= 7,
        }

        return "P(Y|do(X)) \\neq P(Y|X) \\text{ if confounded}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate d-separation and identification steps.

        Args:
            data: Solution data with DAG structure and identification.

        Returns:
            List of step strings.
        """
        steps = [
            f"DAG: {data['edges_str']}",
            f"nodes: {', '.join(data['nodes'])}",
        ]

        if data["confounders"]:
            steps.append(f"confounders: {', '.join(data['confounders'])}")
            steps.append("X and Y are NOT d-separated (confounded)")
        else:
            steps.append("no confounders, X and Y d-separated given empty set")

        ident_str = "yes" if data["identifiable"] else "no"
        steps.append(f"identifiable: {ident_str}")
        steps.append(f"formula: {data['formula']}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the identification result and formula.

        Args:
            data: Solution data.

        Returns:
            String with identifiability and adjustment formula.
        """
        ident_str = "identifiable" if data["identifiable"] else "not identifiable"
        result = f"{ident_str}, {data['formula']}"
        if data["confounders"]:
            result = f"confounders={{{','.join(data['confounders'])}}}, {result}"
        return result
