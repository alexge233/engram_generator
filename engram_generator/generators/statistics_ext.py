"""Extended statistics generators -- hypothesis tests, ANOVA, regression diagnostics.

10 generators at tiers 5-6 covering one-way ANOVA, chi-square independence,
regression diagnostics, paired t-test, two-sample t-test, F-test, maximum
likelihood estimation, goodness-of-fit, correlation test, and power analysis.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt(value: float, places: int = 4) -> str:
    """Round a float and return its string representation.

    Args:
        value: Number to format.
        places: Decimal places.

    Returns:
        Rounded string.
    """
    return str(round(value, places))


def _phi(z: float) -> float:
    """Approximate the standard normal CDF Phi(z).

    Args:
        z: z-score.

    Returns:
        Probability P(Z <= z).
    """
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _phi_inv_approx(p: float) -> float:
    """Approximate inverse of the standard normal CDF (rational approx).

    Uses the Beasley-Springer-Moro approximation for 0.5 < p < 1.

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
    return t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)


# ---------------------------------------------------------------------------
# 1. One-way ANOVA
# ---------------------------------------------------------------------------

@register
class AnovaOneWayGenerator(StepGenerator):
    """Perform one-way ANOVA: compute SSB, SSW, MSB, MSW, and F statistic.

    SSB = sum n_i*(x_bar_i - x_bar)^2.
    SSW = sum sum (x_ij - x_bar_i)^2.
    F = MSB / MSW. Compare to critical value.

    Difficulty scaling:
        d1-2: 2 groups, 3-4 observations each.
        d3-4: 2-3 groups, 3-5 observations.
        d5-6: 3 groups, 4-6 observations.
        d7-8: 3-4 groups, 5-7 observations.

    Prerequisites:
        std_dev.
    """

    _PARAMS = {
        1: (2, 2, 3, 4), 2: (2, 2, 3, 4),
        3: (2, 3, 3, 5), 4: (2, 3, 3, 5),
        5: (3, 3, 4, 6), 6: (3, 3, 4, 6),
        7: (3, 4, 5, 7), 8: (3, 4, 5, 7),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "anova_one_way"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "perform one-way ANOVA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a one-way ANOVA problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        g_lo, g_hi, n_lo, n_hi = self._PARAMS.get(difficulty, self._PARAMS[1])
        k = self._rng.randint(g_lo, g_hi)
        groups = []
        for _ in range(k):
            ni = self._rng.randint(n_lo, n_hi)
            base = self._rng.randint(5, 10 + difficulty * 3)
            data = [base + self._rng.randint(-3, 3) for _ in range(ni)]
            groups.append(data)
        all_data = [x for g in groups for x in g]
        grand_mean = sum(all_data) / len(all_data)
        group_means = [sum(g) / len(g) for g in groups]
        ssb = sum(len(g) * (gm - grand_mean) ** 2 for g, gm in zip(groups, group_means))
        ssw = sum(sum((x - gm) ** 2 for x in g) for g, gm in zip(groups, group_means))
        n_total = len(all_data)
        df_b = k - 1
        df_w = n_total - k
        msb = ssb / df_b if df_b > 0 else 0.0
        msw = ssw / df_w if df_w > 0 else 1.0
        f_stat = msb / msw if msw > 0 else 0.0
        groups_str = "; ".join(
            f"G{i + 1}=[{','.join(str(x) for x in g)}]" for i, g in enumerate(groups)
        )
        problem = groups_str
        return problem, {
            "k": k, "groups": groups,
            "grand_mean": round(grand_mean, 4),
            "group_means": [round(m, 4) for m in group_means],
            "ssb": round(ssb, 4), "ssw": round(ssw, 4),
            "df_b": df_b, "df_w": df_w,
            "msb": round(msb, 4), "msw": round(msw, 4),
            "f_stat": round(f_stat, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing ANOVA table computation.
        """
        means_str = ", ".join(f"\\bar{{x}}_{i + 1}={m}" for i, m in enumerate(data["group_means"]))
        return [
            f"\\bar{{x}}={_fmt(data['grand_mean'])}, {means_str}",
            f"SSB={_fmt(data['ssb'])}, df_B={data['df_b']}",
            f"SSW={_fmt(data['ssw'])}, df_W={data['df_w']}",
            f"MSB={_fmt(data['msb'])}, MSW={_fmt(data['msw'])}",
            f"F=MSB/MSW={_fmt(data['f_stat'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the F statistic.

        Args:
            data: Solution data dict.

        Returns:
            F statistic as a decimal string.
        """
        return _fmt(data["f_stat"])


# ---------------------------------------------------------------------------
# 2. Chi-Square Independence Test
# ---------------------------------------------------------------------------

@register
class ChiSquareIndependenceGenerator(StepGenerator):
    """Perform chi-square test of independence on a contingency table.

    X^2 = sum (O-E)^2/E. E_ij = R_i*C_j/N. df = (r-1)(c-1).

    Difficulty scaling:
        d1-3: 2x2 table, counts 5-20.
        d4-6: 2x3 table, counts 5-30.
        d7-8: 3x3 table, counts 5-40.

    Prerequisites:
        division.
    """

    _SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 2), 4: (2, 3),
        5: (2, 3), 6: (2, 3), 7: (3, 3), 8: (3, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chi_square_independence"

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
        return "perform chi-square independence test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chi-square independence test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r, c = self._SIZES.get(difficulty, (2, 2))
        upper = 10 + difficulty * 4
        observed = [[self._rng.randint(5, upper) for _ in range(c)] for _ in range(r)]
        n_total = sum(x for row in observed for x in row)
        row_totals = [sum(row) for row in observed]
        col_totals = [sum(observed[i][j] for i in range(r)) for j in range(c)]
        expected = [[row_totals[i] * col_totals[j] / n_total for j in range(c)] for i in range(r)]
        chi2 = sum(
            (observed[i][j] - expected[i][j]) ** 2 / expected[i][j]
            for i in range(r) for j in range(c)
        )
        df = (r - 1) * (c - 1)
        table_str = "; ".join(
            f"R{i + 1}=[{','.join(str(x) for x in row)}]"
            for i, row in enumerate(observed)
        )
        problem = f"\\chi^2 test: {table_str}"
        return problem, {
            "r": r, "c": c, "observed": observed,
            "expected": [[round(e, 4) for e in row] for row in expected],
            "row_totals": row_totals, "col_totals": col_totals,
            "n": n_total, "chi2": round(chi2, 4), "df": df,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing expected values, chi-square statistic, and df.
        """
        steps = [f"N={data['n']}, rows={data['r']}, cols={data['c']}"]
        steps.append(f"row totals={data['row_totals']}, col totals={data['col_totals']}")
        e_parts = []
        for i in range(data["r"]):
            for j in range(data["c"]):
                e_parts.append(f"E_{{{i + 1}{j + 1}}}={data['expected'][i][j]}")
        steps.append(", ".join(e_parts[:4]) + ("..." if len(e_parts) > 4 else ""))
        steps.append(f"\\chi^2={_fmt(data['chi2'])}, df={data['df']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the chi-square statistic.

        Args:
            data: Solution data dict.

        Returns:
            Chi-square value as a decimal string.
        """
        return _fmt(data["chi2"])


# ---------------------------------------------------------------------------
# 3. Regression Diagnostics
# ---------------------------------------------------------------------------

@register
class RegressionDiagnosticsGenerator(StepGenerator):
    """Compute R^2 and adjusted R^2 for regression diagnostics.

    R^2 = 1 - SSR/SST. Adjusted R^2 = 1 - (1-R^2)*(n-1)/(n-p-1).

    Difficulty scaling:
        d1-2: 4-6 data points, 1 predictor.
        d3-4: 5-8 data points.
        d5-6: 6-10 data points, 1-2 predictors.
        d7-8: 8-12 data points, 2-3 predictors.

    Prerequisites:
        linear_regression.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regression_diagnostics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute R-squared and adjusted R-squared"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regression diagnostics problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            n = self._rng.randint(4, 6)
            p = 1
        elif difficulty <= 4:
            n = self._rng.randint(5, 8)
            p = 1
        elif difficulty <= 6:
            n = self._rng.randint(6, 10)
            p = self._rng.randint(1, 2)
        else:
            n = self._rng.randint(8, 12)
            p = self._rng.randint(2, 3)
        slope = self._rng.randint(1, 3 + difficulty)
        intercept = self._rng.randint(0, 5)
        xs = list(range(1, n + 1))
        noise = max(1, difficulty)
        ys = [slope * x + intercept + self._rng.randint(-noise, noise) for x in xs]
        y_bar = sum(ys) / n
        y_hat = [slope * x + intercept for x in xs]
        sst = sum((y - y_bar) ** 2 for y in ys)
        ssr = sum((y - yh) ** 2 for y, yh in zip(ys, y_hat))
        r2 = 1.0 - ssr / sst if sst > 0 else 0.0
        r2 = max(0.0, min(1.0, r2))
        adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1) if n > p + 1 else r2
        problem = f"n={n}, p={p}, SST={_fmt(sst)}, SSR={_fmt(ssr)}"
        return problem, {
            "n": n, "p": p,
            "sst": round(sst, 4), "ssr": round(ssr, 4),
            "r2": round(r2, 4), "adj_r2": round(adj_r2, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing R^2 and adjusted R^2 computation.
        """
        return [
            f"R^2=1-SSR/SST=1-{_fmt(data['ssr'])}/{_fmt(data['sst'])}={_fmt(data['r2'])}",
            f"adj R^2=1-(1-{_fmt(data['r2'])})*({data['n']}-1)/({data['n']}-{data['p']}-1)={_fmt(data['adj_r2'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return R^2 and adjusted R^2.

        Args:
            data: Solution data dict.

        Returns:
            Both values as a string.
        """
        return f"R^2={_fmt(data['r2'])}, adj_R^2={_fmt(data['adj_r2'])}"


# ---------------------------------------------------------------------------
# 4. Paired T-Test
# ---------------------------------------------------------------------------

@register
class PairedTTestGenerator(StepGenerator):
    """Perform a paired t-test on before/after data.

    d_bar = mean(differences), SE = s_d/sqrt(n).
    t = d_bar / SE.

    Difficulty scaling:
        d1-2: 4-5 pairs, small differences.
        d3-4: 5-7 pairs.
        d5-6: 6-9 pairs.
        d7-8: 8-12 pairs.

    Prerequisites:
        hypothesis_test.
    """

    _N_RANGES = {
        1: (4, 5), 2: (4, 5), 3: (5, 7), 4: (5, 7),
        5: (6, 9), 6: (6, 9), 7: (8, 12), 8: (8, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "paired_t_test"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "perform paired t-test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a paired t-test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (4, 5))
        n = self._rng.randint(n_lo, n_hi)
        base = self._rng.randint(10, 20 + difficulty * 5)
        before = [base + self._rng.randint(-5, 5) for _ in range(n)]
        effect = self._rng.randint(1, 3 + difficulty)
        after = [b + effect + self._rng.randint(-2, 2) for b in before]
        diffs = [a - b for a, b in zip(after, before)]
        d_bar = sum(diffs) / n
        s_d = math.sqrt(sum((d - d_bar) ** 2 for d in diffs) / (n - 1))
        se = s_d / math.sqrt(n) if n > 0 else 1.0
        t_stat = d_bar / se if se > 0 else 0.0
        df = n - 1
        pairs_str = ",".join(f"({b},{a})" for b, a in zip(before, after))
        problem = f"paired t: {pairs_str}"
        return problem, {
            "n": n, "diffs": diffs,
            "d_bar": round(d_bar, 4),
            "s_d": round(s_d, 4),
            "se": round(se, 4),
            "t_stat": round(t_stat, 4),
            "df": df,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the paired t-test computation.
        """
        return [
            f"d=[{','.join(str(d) for d in data['diffs'])}]",
            f"\\bar{{d}}={_fmt(data['d_bar'])}",
            f"s_d={_fmt(data['s_d'])}",
            f"SE=s_d/\\sqrt{{n}}={_fmt(data['s_d'])}/\\sqrt{{{data['n']}}}={_fmt(data['se'])}",
            f"t=\\bar{{d}}/SE={_fmt(data['d_bar'])}/{_fmt(data['se'])}={_fmt(data['t_stat'])}, df={data['df']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the t statistic.

        Args:
            data: Solution data dict.

        Returns:
            t statistic as a decimal string.
        """
        return _fmt(data["t_stat"])


# ---------------------------------------------------------------------------
# 5. Two-Sample T-Test (Welch's)
# ---------------------------------------------------------------------------

@register
class TwoSampleTTestGenerator(StepGenerator):
    """Perform Welch's two-sample t-test.

    t = (x1_bar - x2_bar) / sqrt(s1^2/n1 + s2^2/n2).
    Welch's df approximation for unequal variances.

    Difficulty scaling:
        d1-2: n1=n2=4-5.
        d3-4: n1=4-6, n2=4-6.
        d5-6: n1=5-8, n2=5-8.
        d7-8: n1=6-10, n2=6-10, unequal sizes.

    Prerequisites:
        hypothesis_test.
    """

    _N_RANGES = {
        1: (4, 5, 4, 5), 2: (4, 5, 4, 5),
        3: (4, 6, 4, 6), 4: (4, 6, 4, 6),
        5: (5, 8, 5, 8), 6: (5, 8, 5, 8),
        7: (6, 10, 6, 10), 8: (6, 10, 6, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_sample_t"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "perform two-sample Welch's t-test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a two-sample t-test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n1lo, n1hi, n2lo, n2hi = self._N_RANGES.get(difficulty, self._N_RANGES[1])
        n1 = self._rng.randint(n1lo, n1hi)
        n2 = self._rng.randint(n2lo, n2hi)
        mu1 = self._rng.randint(10, 20 + difficulty * 3)
        mu2 = mu1 + self._rng.randint(1, 3 + difficulty)
        s1_data = [mu1 + self._rng.randint(-4, 4) for _ in range(n1)]
        s2_data = [mu2 + self._rng.randint(-4, 4) for _ in range(n2)]
        x1_bar = sum(s1_data) / n1
        x2_bar = sum(s2_data) / n2
        s1_sq = sum((x - x1_bar) ** 2 for x in s1_data) / (n1 - 1) if n1 > 1 else 1.0
        s2_sq = sum((x - x2_bar) ** 2 for x in s2_data) / (n2 - 1) if n2 > 1 else 1.0
        se = math.sqrt(s1_sq / n1 + s2_sq / n2)
        t_stat = (x1_bar - x2_bar) / se if se > 0 else 0.0
        num_df = (s1_sq / n1 + s2_sq / n2) ** 2
        den_df = (s1_sq / n1) ** 2 / (n1 - 1) + (s2_sq / n2) ** 2 / (n2 - 1)
        welch_df = num_df / den_df if den_df > 0 else n1 + n2 - 2
        problem = f"S1=[{','.join(str(x) for x in s1_data)}]; S2=[{','.join(str(x) for x in s2_data)}]"
        return problem, {
            "n1": n1, "n2": n2,
            "x1_bar": round(x1_bar, 4), "x2_bar": round(x2_bar, 4),
            "s1_sq": round(s1_sq, 4), "s2_sq": round(s2_sq, 4),
            "se": round(se, 4), "t_stat": round(t_stat, 4),
            "df": round(welch_df, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the two-sample t-test computation.
        """
        return [
            f"\\bar{{x}}_1={_fmt(data['x1_bar'])}, \\bar{{x}}_2={_fmt(data['x2_bar'])}",
            f"s_1^2={_fmt(data['s1_sq'])}, s_2^2={_fmt(data['s2_sq'])}",
            f"SE=\\sqrt{{{_fmt(data['s1_sq'])}/{data['n1']}+{_fmt(data['s2_sq'])}/{data['n2']}}}={_fmt(data['se'])}",
            f"t=({_fmt(data['x1_bar'])}-{_fmt(data['x2_bar'])})/{_fmt(data['se'])}={_fmt(data['t_stat'])}",
            f"Welch df={_fmt(data['df'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the t statistic.

        Args:
            data: Solution data dict.

        Returns:
            t statistic as a decimal string.
        """
        return _fmt(data["t_stat"])


# ---------------------------------------------------------------------------
# 6. F-Test (Equality of Variances)
# ---------------------------------------------------------------------------

@register
class FTestGenerator(StepGenerator):
    """Perform F-test for equality of two population variances.

    F = s1^2/s2^2. df1 = n1-1, df2 = n2-1.

    Difficulty scaling:
        d1-2: n1=n2=4-5.
        d3-4: n1=5-7, n2=5-7.
        d5-6: n1=6-9, n2=6-9.
        d7-8: n1=8-12, n2=8-12.

    Prerequisites:
        std_dev.
    """

    _N_RANGES = {
        1: (4, 5), 2: (4, 5), 3: (5, 7), 4: (5, 7),
        5: (6, 9), 6: (6, 9), 7: (8, 12), 8: (8, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "f_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "perform F-test for equality of variances"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an F-test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (4, 5))
        n1 = self._rng.randint(n_lo, n_hi)
        n2 = self._rng.randint(n_lo, n_hi)
        mu1 = self._rng.randint(10, 20)
        mu2 = self._rng.randint(10, 20)
        spread1 = self._rng.randint(2, 4 + difficulty)
        spread2 = self._rng.randint(2, 4 + difficulty)
        s1_data = [mu1 + self._rng.randint(-spread1, spread1) for _ in range(n1)]
        s2_data = [mu2 + self._rng.randint(-spread2, spread2) for _ in range(n2)]
        x1_bar = sum(s1_data) / n1
        x2_bar = sum(s2_data) / n2
        s1_sq = sum((x - x1_bar) ** 2 for x in s1_data) / (n1 - 1) if n1 > 1 else 1.0
        s2_sq = sum((x - x2_bar) ** 2 for x in s2_data) / (n2 - 1) if n2 > 1 else 1.0
        if s2_sq == 0:
            s2_sq = 1.0
        f_stat = s1_sq / s2_sq
        df1 = n1 - 1
        df2 = n2 - 1
        problem = f"s_1^2={_fmt(s1_sq)}, s_2^2={_fmt(s2_sq)}, n_1={n1}, n_2={n2}"
        return problem, {
            "n1": n1, "n2": n2,
            "s1_sq": round(s1_sq, 4), "s2_sq": round(s2_sq, 4),
            "f_stat": round(f_stat, 4),
            "df1": df1, "df2": df2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the F-test computation.
        """
        return [
            f"H_0: \\sigma_1^2=\\sigma_2^2",
            f"F=s_1^2/s_2^2={_fmt(data['s1_sq'])}/{_fmt(data['s2_sq'])}={_fmt(data['f_stat'])}",
            f"df_1={data['df1']}, df_2={data['df2']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the F statistic.

        Args:
            data: Solution data dict.

        Returns:
            F statistic as a decimal string.
        """
        return _fmt(data["f_stat"])


# ---------------------------------------------------------------------------
# 7. Maximum Likelihood Estimation
# ---------------------------------------------------------------------------

@register
class MaximumLikelihoodGenerator(StepGenerator):
    """Compute maximum likelihood estimates for common distributions.

    Normal MLE: mu_hat = x_bar, sigma_hat^2 = sum(x_i - x_bar)^2/n.
    Poisson MLE: lambda_hat = x_bar.

    Difficulty scaling:
        d1-3: Poisson MLE with 4-6 observations.
        d4-6: Normal MLE with 5-8 observations.
        d7-8: Normal MLE with 8-12 observations.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "maximum_likelihood"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute maximum likelihood estimate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an MLE problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._build_poisson_mle(difficulty)
        return self._build_normal_mle(difficulty)

    def _build_poisson_mle(self, difficulty: int) -> tuple[str, dict]:
        """Build Poisson MLE problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(4, 6)
        true_lam = self._rng.randint(2, 5 + difficulty)
        data = [max(0, true_lam + self._rng.randint(-2, 3)) for _ in range(n)]
        lam_hat = sum(data) / n
        data_str = ",".join(str(x) for x in data)
        problem = f"Poisson MLE: [{data_str}]"
        return problem, {
            "dist": "poisson", "data": data, "n": n,
            "lam_hat": round(lam_hat, 4),
        }

    def _build_normal_mle(self, difficulty: int) -> tuple[str, dict]:
        """Build Normal MLE problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            n = self._rng.randint(5, 8)
        else:
            n = self._rng.randint(8, 12)
        mu_true = self._rng.randint(5, 20)
        sigma_true = self._rng.randint(2, 5)
        data = [mu_true + self._rng.randint(-sigma_true * 2, sigma_true * 2) for _ in range(n)]
        mu_hat = sum(data) / n
        sigma_sq_hat = sum((x - mu_hat) ** 2 for x in data) / n
        data_str = ",".join(str(x) for x in data)
        problem = f"Normal MLE: [{data_str}]"
        return problem, {
            "dist": "normal", "data": data, "n": n,
            "mu_hat": round(mu_hat, 4),
            "sigma_sq_hat": round(sigma_sq_hat, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the MLE derivation.
        """
        if data["dist"] == "poisson":
            return [
                f"L(\\lambda)=\\prod \\lambda^{{x_i}}*e^{{-\\lambda}}/x_i!",
                f"\\hat{{\\lambda}}=\\bar{{x}}={sum(data['data'])}/{data['n']}={_fmt(data['lam_hat'])}",
            ]
        return [
            f"\\hat{{\\mu}}=\\bar{{x}}={sum(data['data'])}/{data['n']}={_fmt(data['mu_hat'])}",
            f"\\hat{{\\sigma}}^2=\\sum(x_i-\\bar{{x}})^2/n={_fmt(data['sigma_sq_hat'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the MLE estimate.

        Args:
            data: Solution data dict.

        Returns:
            MLE parameter(s) as a string.
        """
        if data["dist"] == "poisson":
            return f"lambda_hat={_fmt(data['lam_hat'])}"
        return f"mu_hat={_fmt(data['mu_hat'])}, sigma_sq_hat={_fmt(data['sigma_sq_hat'])}"


# ---------------------------------------------------------------------------
# 8. Chi-Square Goodness of Fit
# ---------------------------------------------------------------------------

@register
class GoodnessOfFitGenerator(StepGenerator):
    """Perform chi-square goodness-of-fit test.

    X^2 = sum (O_i - E_i)^2 / E_i. df = k - 1 - p (p estimated params).

    Difficulty scaling:
        d1-2: k=3-4 categories, equal expected.
        d3-4: k=4-5.
        d5-6: k=5-6.
        d7-8: k=6-8.

    Prerequisites:
        division.
    """

    _K_RANGES = {
        1: (3, 4), 2: (3, 4), 3: (4, 5), 4: (4, 5),
        5: (5, 6), 6: (5, 6), 7: (6, 8), 8: (6, 8),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "goodness_of_fit"

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
        return "perform chi-square goodness-of-fit test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a goodness-of-fit problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k_lo, k_hi = self._K_RANGES.get(difficulty, (3, 4))
        k = self._rng.randint(k_lo, k_hi)
        total_obs = self._rng.randint(50, 100 + difficulty * 20)
        expected_each = total_obs / k
        observed = []
        remaining = total_obs
        for i in range(k - 1):
            oi = max(1, int(expected_each + self._rng.randint(-int(expected_each * 0.3), int(expected_each * 0.3))))
            oi = min(oi, remaining - (k - i - 1))
            observed.append(oi)
            remaining -= oi
        observed.append(remaining)
        expected = [total_obs / k] * k
        chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
        df = k - 1
        problem = f"GOF: O={observed}, E={[round(e, 2) for e in expected]}"
        return problem, {
            "observed": observed, "expected": [round(e, 4) for e in expected],
            "k": k, "chi2": round(chi2, 4), "df": df,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the GOF computation.
        """
        steps = [f"k={data['k']} categories"]
        components = []
        for i, (o, e) in enumerate(zip(data["observed"], data["expected"])):
            comp = round((o - e) ** 2 / e, 4) if e > 0 else 0.0
            components.append(f"({o}-{e})^2/{e}={_fmt(comp)}")
        steps.append(" + ".join(components[:4]) + ("..." if len(components) > 4 else ""))
        steps.append(f"\\chi^2={_fmt(data['chi2'])}, df={data['df']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the chi-square statistic.

        Args:
            data: Solution data dict.

        Returns:
            Chi-square value as a decimal string.
        """
        return _fmt(data["chi2"])


# ---------------------------------------------------------------------------
# 9. Correlation Significance Test
# ---------------------------------------------------------------------------

@register
class CorrelationTestGenerator(StepGenerator):
    """Test significance of Pearson correlation coefficient.

    t = r*sqrt(n-2)/sqrt(1-r^2). H_0: rho=0.

    Difficulty scaling:
        d1-2: 4-5 data pairs.
        d3-4: 5-7 pairs.
        d5-6: 7-10 pairs.
        d7-8: 10-15 pairs.

    Prerequisites:
        linear_regression.
    """

    _N_RANGES = {
        1: (4, 5), 2: (4, 5), 3: (5, 7), 4: (5, 7),
        5: (7, 10), 6: (7, 10), 7: (10, 15), 8: (10, 15),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "correlation_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "test significance of correlation"

    def _compute_r(self, xs: list[int], ys: list[int], n: int) -> float:
        """Compute Pearson correlation coefficient.

        Args:
            xs: x-values.
            ys: y-values.
            n: Number of pairs.

        Returns:
            Pearson r as a float.
        """
        sx = sum(xs)
        sy = sum(ys)
        sxy = sum(x * y for x, y in zip(xs, ys))
        sx2 = sum(x * x for x in xs)
        sy2 = sum(y * y for y in ys)
        numer = n * sxy - sx * sy
        denom_sq = (n * sx2 - sx ** 2) * (n * sy2 - sy ** 2)
        denom = math.sqrt(max(1, denom_sq))
        return numer / denom if denom > 0 else 0.0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a correlation significance test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (4, 5))
        n = self._rng.randint(n_lo, n_hi)
        slope = self._rng.randint(1, 3)
        intercept = self._rng.randint(0, 5)
        xs = list(range(1, n + 1))
        noise = max(1, difficulty // 2)
        ys = [slope * x + intercept + self._rng.randint(-noise, noise) for x in xs]
        r = self._compute_r(xs, ys, n)
        r2 = r * r
        denom = math.sqrt(1.0 - r2) if r2 < 1.0 else 0.001
        t_stat = r * math.sqrt(n - 2) / denom
        df = n - 2
        problem = f"r={_fmt(r)}, n={n}"
        return problem, {
            "r": round(r, 4), "n": n,
            "t_stat": round(t_stat, 4), "df": df,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the correlation test computation.
        """
        r = data["r"]
        n = data["n"]
        return [
            f"H_0: \\rho=0",
            f"t=r\\sqrt{{n-2}}/\\sqrt{{1-r^2}}={_fmt(r)}*\\sqrt{{{n - 2}}}/\\sqrt{{1-{_fmt(r)}^2}}",
            f"t={_fmt(data['t_stat'])}, df={data['df']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the t statistic.

        Args:
            data: Solution data dict.

        Returns:
            t statistic as a decimal string.
        """
        return _fmt(data["t_stat"])


# ---------------------------------------------------------------------------
# 10. Power Analysis
# ---------------------------------------------------------------------------

@register
class PowerAnalysisGenerator(StepGenerator):
    """Compute statistical power and required sample size.

    Power = P(reject H_0 | H_1 true).
    For z-test: power = Phi(z_alpha - delta*sqrt(n)/sigma).
    Solve for n given desired power.

    Difficulty scaling:
        d1-2: one-sided z-test, compute power for given n.
        d3-4: compute required n for given power.
        d5-6: two-sided test.
        d7-8: two-sided with smaller effect size.

    Prerequisites:
        hypothesis_test.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_analysis"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty <= 4:
            return "compute statistical power"
        return "compute required sample size for given power"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power analysis problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        sigma = self._rng.randint(2, 5 + difficulty)
        delta = self._rng.randint(1, max(1, sigma - 1))
        alpha = 0.05
        if difficulty <= 4:
            z_alpha = 1.6449
            n = self._rng.randint(10, 20 + difficulty * 5)
            z_power = z_alpha - delta * math.sqrt(n) / sigma
            power = 1.0 - _phi(z_power)
            problem = f"z-test: \\delta={delta}, \\sigma={sigma}, n={n}, \\alpha={alpha}"
            return problem, {
                "sigma": sigma, "delta": delta, "alpha": alpha,
                "n": n, "z_alpha": z_alpha,
                "power": round(power, 4), "mode": "compute_power",
            }
        target_power = self._rng.choice([0.8, 0.9, 0.95])
        z_alpha = 1.96
        z_beta = _phi_inv_approx(target_power)
        n_required = math.ceil(((z_alpha + z_beta) * sigma / delta) ** 2)
        problem = f"z-test: \\delta={delta}, \\sigma={sigma}, power={target_power}, \\alpha={alpha}"
        return problem, {
            "sigma": sigma, "delta": delta, "alpha": alpha,
            "target_power": target_power, "z_alpha": z_alpha,
            "z_beta": round(z_beta, 4),
            "n_required": n_required, "mode": "compute_n",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the power analysis computation.
        """
        if data["mode"] == "compute_power":
            n = data["n"]
            return [
                f"z_\\alpha={_fmt(data['z_alpha'])} (one-sided, \\alpha={data['alpha']})",
                f"z_power={_fmt(data['z_alpha'])}-{data['delta']}*\\sqrt{{{n}}}/{data['sigma']}",
                f"power=1-\\Phi(z_power)={_fmt(data['power'])}",
            ]
        return [
            f"z_\\alpha={_fmt(data['z_alpha'])} (two-sided, \\alpha={data['alpha']})",
            f"z_\\beta=\\Phi^{{-1}}({data['target_power']})={_fmt(data['z_beta'])}",
            f"n=((z_\\alpha+z_\\beta)*\\sigma/\\delta)^2=(({_fmt(data['z_alpha'])}+{_fmt(data['z_beta'])})*{data['sigma']}/{data['delta']})^2",
            f"n={data['n_required']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the power or required sample size.

        Args:
            data: Solution data dict.

        Returns:
            Power or n as a string.
        """
        if data["mode"] == "compute_power":
            return f"power={_fmt(data['power'])}"
        return f"n={data['n_required']}"
