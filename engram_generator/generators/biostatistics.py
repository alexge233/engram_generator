"""Biostatistics generators -- survival analysis, clinical trials, and meta-analysis.

6 generators covering Kaplan-Meier survival estimation, odds ratios with
confidence intervals, number needed to treat, sensitivity/specificity with
predictive values, sample size calculations, and fixed-effect meta-analysis
across tiers 4-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _round4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


# ===================================================================
# 1. SURVIVAL ANALYSIS (tier 5)
# ===================================================================

@register
class SurvivalAnalysisGenerator(StepGenerator):
    """Compute Kaplan-Meier survival probability from a small dataset.

    At each event time t_i, S(t_i) = S(t_{i-1}) * (1 - d_i / n_i)
    where d_i is the number of deaths and n_i is the number at risk.
    Censored observations reduce n_i but do not contribute events.

    Difficulty scaling:
        Difficulty 1-3: 3 event times, no censoring.
        Difficulty 4-6: 4 event times, 1-2 censored.
        Difficulty 7-8: 5 event times, 2-3 censored.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "survival_analysis"

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
            difficulty: Controls dataset complexity.

        Returns:
            Task description string.
        """
        return "compute Kaplan-Meier survival estimate S(t)"

    def _select_num_events(self, difficulty: int) -> int:
        """Choose number of event times based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Number of event time points.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kaplan-Meier survival problem.

        Args:
            difficulty: Controls number of events and censoring.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_events = self._select_num_events(difficulty)
        initial_n = self._rng.randint(15, 30 + difficulty * 5)

        # Generate sorted event times
        times = sorted(self._rng.sample(range(1, 20 + difficulty * 5), num_events))

        # Generate deaths and censored at each time
        n_at_risk = initial_n
        events = []
        survival = 1.0
        km_steps = []

        for t in times:
            # Some censored before this event (only at higher difficulty)
            censored = 0
            if difficulty > 3 and self._rng.random() < 0.4:
                censored = self._rng.randint(1, max(1, n_at_risk // 6))
                n_at_risk -= censored

            deaths = self._rng.randint(1, max(1, n_at_risk // 4))
            if n_at_risk <= 0:
                break

            factor = _round4(1 - deaths / n_at_risk)
            survival = _round4(survival * factor)

            events.append({
                "time": t, "n_at_risk": n_at_risk,
                "deaths": deaths, "censored": censored,
                "factor": factor, "survival": survival,
            })

            km_steps.append(
                f"t={t}: n={n_at_risk}, d={deaths}, "
                f"S(t) = {_round4(survival / factor)} * (1-{deaths}/{n_at_risk}) = {survival}"
            )

            n_at_risk -= deaths

        final_survival = events[-1]["survival"] if events else 1.0

        events_str = "; ".join(
            f"t={e['time']}(n={e['n_at_risk']},d={e['deaths']})"
            for e in events
        )
        problem = f"KM: N_0={initial_n}, events: {events_str}. S(t)?"
        return problem, {
            "initial_n": initial_n, "events": events,
            "km_steps": km_steps, "final_survival": final_survival,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kaplan-Meier computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each time point's survival calculation.
        """
        steps = [f"initial N = {data['initial_n']}"]
        steps.extend(data["km_steps"])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final survival probability.

        Args:
            data: Solution data.

        Returns:
            S(t) as a string.
        """
        return f"S(t) = {data['final_survival']}"


# ===================================================================
# 2. ODDS RATIO (tier 5)
# ===================================================================

@register
class OddsRatioGenerator(StepGenerator):
    """Compute odds ratio and 95% confidence interval from a 2x2 table.

    OR = (a * d) / (b * c). The 95% CI uses the log method:
    CI = exp(ln(OR) +/- 1.96 * SE) where SE = sqrt(1/a + 1/b + 1/c + 1/d).

    Difficulty scaling:
        Difficulty 1-3: small cell counts (5-20).
        Difficulty 4-6: moderate cell counts (10-50).
        Difficulty 7-8: larger cell counts (20-100).

    Prerequisites:
        logarithm (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "odds_ratio"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls cell count range.

        Returns:
            Task description string.
        """
        return "compute odds ratio and 95% CI from 2x2 table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an odds ratio problem.

        Args:
            difficulty: Controls cell count magnitudes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lo, hi = 5, 20
        elif difficulty <= 6:
            lo, hi = 10, 50
        else:
            lo, hi = 20, 100

        a = self._rng.randint(lo, hi)
        b = self._rng.randint(lo, hi)
        c = self._rng.randint(lo, hi)
        d = self._rng.randint(lo, hi)

        or_val = _round4((a * d) / (b * c))
        ln_or = _round4(math.log(or_val))
        se = _round4(math.sqrt(1 / a + 1 / b + 1 / c + 1 / d))
        ci_lower = _round4(math.exp(ln_or - 1.96 * se))
        ci_upper = _round4(math.exp(ln_or + 1.96 * se))

        problem = (
            f"2x2 table: a={a}, b={b}, c={c}, d={d}. "
            f"Compute OR and 95% CI."
        )
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "or_val": or_val, "ln_or": ln_or, "se": se,
            "ci_lower": ci_lower, "ci_upper": ci_upper,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate odds ratio computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing OR, ln(OR), SE, and CI.
        """
        return [
            f"OR = ({data['a']}*{data['d']})/({data['b']}*{data['c']}) = {data['or_val']}",
            f"ln(OR) = {data['ln_or']}",
            f"SE = sqrt(1/{data['a']}+1/{data['b']}+1/{data['c']}+1/{data['d']}) = {data['se']}",
            f"95% CI = exp({data['ln_or']} +/- 1.96*{data['se']}) = [{data['ci_lower']}, {data['ci_upper']}]",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the odds ratio and CI.

        Args:
            data: Solution data.

        Returns:
            OR and CI as a string.
        """
        return f"OR={data['or_val']}, 95% CI=[{data['ci_lower']}, {data['ci_upper']}]"


# ===================================================================
# 3. NUMBER NEEDED TO TREAT (tier 4)
# ===================================================================

@register
class NumberNeededTreatGenerator(StepGenerator):
    """Compute the number needed to treat from treatment and control rates.

    NNT = 1 / ARR = 1 / |p_treatment - p_control| where ARR is the
    absolute risk reduction. The NNT represents how many patients
    must be treated for one to benefit.

    Difficulty scaling:
        Difficulty 1-3: simple rates (multiples of 0.05).
        Difficulty 4-6: decimal rates, moderate difference.
        Difficulty 7-8: small ARR (large NNT).

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "number_needed_treat"

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
            difficulty: Controls rate precision.

        Returns:
            Task description string.
        """
        return "compute NNT = 1 / |p_treatment - p_control|"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a number needed to treat problem.

        Args:
            difficulty: Controls rate precision and ARR magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p_control = _round4(self._rng.choice(
                [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
            ))
            p_treatment = _round4(p_control - self._rng.choice(
                [0.05, 0.1, 0.15]
            ))
        elif difficulty <= 6:
            p_control = _round4(self._rng.uniform(0.1, 0.5))
            p_treatment = _round4(p_control - self._rng.uniform(0.02, 0.15))
        else:
            p_control = _round4(self._rng.uniform(0.05, 0.4))
            p_treatment = _round4(p_control - self._rng.uniform(0.01, 0.05))

        p_treatment = max(0.001, p_treatment)
        arr = _round4(abs(p_treatment - p_control))
        nnt = _round4(1 / arr) if arr > 0 else 0

        problem = (
            f"p_treatment={p_treatment}, p_control={p_control}. "
            f"Compute ARR and NNT."
        )
        return problem, {
            "p_treatment": p_treatment, "p_control": p_control,
            "arr": arr, "nnt": nnt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate NNT computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing ARR and NNT calculation.
        """
        return [
            f"ARR = |{data['p_treatment']} - {data['p_control']}| = {data['arr']}",
            f"NNT = 1 / {data['arr']} = {data['nnt']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the NNT value.

        Args:
            data: Solution data.

        Returns:
            ARR and NNT as a string.
        """
        return f"ARR={data['arr']}, NNT={data['nnt']}"


# ===================================================================
# 4. SENSITIVITY AND SPECIFICITY (tier 4)
# ===================================================================

@register
class SensitivitySpecificityGenerator(StepGenerator):
    """Compute sensitivity, specificity, PPV, and NPV from test data.

    Sensitivity = TP / (TP + FN), Specificity = TN / (TN + FP).
    PPV = TP / (TP + FP), NPV = TN / (TN + FN).
    Also computes prevalence-adjusted PPV and NPV using Bayes' theorem.

    Difficulty scaling:
        Difficulty 1-3: small counts, compute Sens and Spec only.
        Difficulty 4-6: moderate counts, add PPV and NPV.
        Difficulty 7-8: larger counts, prevalence-adjusted values.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sensitivity_specificity"

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
            difficulty: Controls which measures to compute.

        Returns:
            Task description string.
        """
        if difficulty <= 3:
            return "compute sensitivity and specificity"
        return "compute sensitivity, specificity, PPV, and NPV"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sensitivity/specificity problem.

        Args:
            difficulty: Controls cell counts and computed measures.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            scale = 10
        elif difficulty <= 6:
            scale = 25
        else:
            scale = 50

        tp = self._rng.randint(5, 3 * scale)
        fn = self._rng.randint(1, scale)
        fp = self._rng.randint(1, scale)
        tn = self._rng.randint(5, 3 * scale)

        sens = _round4(tp / (tp + fn))
        spec = _round4(tn / (tn + fp))
        ppv = _round4(tp / (tp + fp))
        npv = _round4(tn / (tn + fn))

        total = tp + fn + fp + tn
        prevalence = _round4((tp + fn) / total)

        problem = (
            f"TP={tp}, FN={fn}, FP={fp}, TN={tn}. "
            f"Compute Sens, Spec, PPV, NPV."
        )
        return problem, {
            "tp": tp, "fn": fn, "fp": fp, "tn": tn,
            "sens": sens, "spec": spec, "ppv": ppv, "npv": npv,
            "prevalence": prevalence,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sensitivity/specificity computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each measure's calculation.
        """
        steps = [
            f"Sens = {data['tp']}/({data['tp']}+{data['fn']}) = {data['sens']}",
            f"Spec = {data['tn']}/({data['tn']}+{data['fp']}) = {data['spec']}",
            f"PPV = {data['tp']}/({data['tp']}+{data['fp']}) = {data['ppv']}",
            f"NPV = {data['tn']}/({data['tn']}+{data['fn']}) = {data['npv']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return all diagnostic measures.

        Args:
            data: Solution data.

        Returns:
            All measures as a string.
        """
        return (
            f"Sens={data['sens']}, Spec={data['spec']}, "
            f"PPV={data['ppv']}, NPV={data['npv']}"
        )


# ===================================================================
# 5. SAMPLE SIZE (tier 5)
# ===================================================================

@register
class SampleSizeGenerator(StepGenerator):
    """Compute required sample size for a two-group comparison.

    Uses n = (z_alpha/2 + z_beta)^2 * 2 * sigma^2 / delta^2 where
    z_alpha/2 and z_beta are standard normal quantiles for the
    significance level and power, sigma is the population standard
    deviation, and delta is the minimum detectable effect size.

    Difficulty scaling:
        Difficulty 1-3: alpha=0.05, power=0.8, simple sigma and delta.
        Difficulty 4-6: varied alpha, power=0.8 or 0.9.
        Difficulty 7-8: custom alpha and power levels.

    Prerequisites:
        hypothesis_test (tier 5).
    """

    # Standard z-values for common alpha and power levels
    _Z_VALUES = {
        0.01: 2.576, 0.025: 1.96, 0.05: 1.645,
        0.8: 0.842, 0.9: 1.282, 0.95: 1.645,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sample_size"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hypothesis_test"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Task description string.
        """
        return "compute sample size per group for two-group comparison"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sample size calculation problem.

        Args:
            difficulty: Controls alpha, power, sigma, and delta.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            alpha = 0.05
            power = 0.8
            sigma = _round4(self._rng.uniform(1.0, 5.0))
            delta = _round4(self._rng.uniform(0.5, 2.0))
        elif difficulty <= 6:
            alpha = self._rng.choice([0.01, 0.05])
            power = self._rng.choice([0.8, 0.9])
            sigma = _round4(self._rng.uniform(1.0, 10.0))
            delta = _round4(self._rng.uniform(0.5, 3.0))
        else:
            alpha = self._rng.choice([0.01, 0.05])
            power = self._rng.choice([0.8, 0.9, 0.95])
            sigma = _round4(self._rng.uniform(2.0, 15.0))
            delta = _round4(self._rng.uniform(0.3, 2.0))

        z_alpha = self._Z_VALUES.get(alpha / 2, 1.96)
        z_beta = self._Z_VALUES.get(power, 0.842)
        z_sum = _round4(z_alpha + z_beta)
        z_sum_sq = _round4(z_sum ** 2)
        numerator = _round4(z_sum_sq * 2 * sigma ** 2)
        denominator = _round4(delta ** 2)
        n_raw = _round4(numerator / denominator)
        n_ceil = math.ceil(n_raw)

        problem = (
            f"alpha={alpha}, power={power}, sigma={sigma}, "
            f"delta={delta}. Sample size per group?"
        )
        return problem, {
            "alpha": alpha, "power": power,
            "sigma": sigma, "delta": delta,
            "z_alpha": z_alpha, "z_beta": z_beta,
            "z_sum": z_sum, "z_sum_sq": z_sum_sq,
            "numerator": numerator, "denominator": denominator,
            "n_raw": n_raw, "n_ceil": n_ceil,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sample size computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the formula evaluation.
        """
        return [
            f"z_alpha/2 = {data['z_alpha']}, z_beta = {data['z_beta']}",
            f"(z_alpha/2 + z_beta)^2 = ({data['z_sum']})^2 = {data['z_sum_sq']}",
            f"n = {data['z_sum_sq']} * 2 * {data['sigma']}^2 / {data['delta']}^2 = {data['n_raw']}",
            f"n (ceiling) = {data['n_ceil']} per group",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the required sample size.

        Args:
            data: Solution data.

        Returns:
            Sample size per group.
        """
        return f"n = {data['n_ceil']} per group"


# ===================================================================
# 6. META-ANALYSIS (tier 6)
# ===================================================================

@register
class MetaAnalysisGenerator(StepGenerator):
    """Compute a fixed-effect meta-analysis pooled estimate.

    Weights each study by w_i = 1 / SE_i^2. The pooled effect is
    theta_hat = sum(w_i * theta_i) / sum(w_i) and its SE is
    1 / sqrt(sum(w_i)). Computes the 95% CI for the pooled estimate.

    Difficulty scaling:
        Difficulty 1-3: 3 studies, simple effect sizes.
        Difficulty 4-6: 4 studies, varied SE values.
        Difficulty 7-8: 5 studies, wider parameter ranges.

    Prerequisites:
        arithmetic_mean (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "meta_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls number of studies.

        Returns:
            Task description string.
        """
        return "compute fixed-effect meta-analysis pooled estimate and CI"

    def _select_num_studies(self, difficulty: int) -> int:
        """Choose number of studies based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Number of studies.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a meta-analysis problem.

        Args:
            difficulty: Controls number of studies and ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = self._select_num_studies(difficulty)

        effects = []
        se_values = []
        for _ in range(k):
            effect = _round4(self._rng.uniform(0.1, 2.0))
            se = _round4(self._rng.uniform(0.1, 0.8))
            effects.append(effect)
            se_values.append(se)

        weights = [_round4(1 / (se ** 2)) for se in se_values]
        sum_w = _round4(sum(weights))
        weighted_sum = _round4(sum(w * e for w, e in zip(weights, effects)))
        pooled = _round4(weighted_sum / sum_w)
        pooled_se = _round4(1 / math.sqrt(sum_w))
        ci_lower = _round4(pooled - 1.96 * pooled_se)
        ci_upper = _round4(pooled + 1.96 * pooled_se)

        studies_str = "; ".join(
            f"theta_{i + 1}={effects[i]}, SE_{i + 1}={se_values[i]}"
            for i in range(k)
        )
        problem = f"Meta ({k} studies): {studies_str}. Pooled estimate?"
        return problem, {
            "k": k, "effects": effects, "se_values": se_values,
            "weights": weights, "sum_w": sum_w,
            "weighted_sum": weighted_sum, "pooled": pooled,
            "pooled_se": pooled_se,
            "ci_lower": ci_lower, "ci_upper": ci_upper,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate meta-analysis computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing weight calculation and pooling.
        """
        steps = []
        for i in range(data["k"]):
            steps.append(
                f"w_{i + 1} = 1/{data['se_values'][i]}^2 = {data['weights'][i]}"
            )
        steps.append(f"sum(w) = {data['sum_w']}")
        steps.append(f"pooled = {data['weighted_sum']}/{data['sum_w']} = {data['pooled']}")
        steps.append(f"SE_pooled = 1/sqrt({data['sum_w']}) = {data['pooled_se']}")
        steps.append(f"95% CI = [{data['ci_lower']}, {data['ci_upper']}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the pooled estimate and CI.

        Args:
            data: Solution data.

        Returns:
            Pooled effect and CI as a string.
        """
        return (
            f"pooled={data['pooled']}, "
            f"95% CI=[{data['ci_lower']}, {data['ci_upper']}]"
        )
