"""Nonparametric statistics task generators.

4 generators at tier 5 covering Mann-Whitney U, Kruskal-Wallis H,
permutation tests, and bootstrap confidence intervals.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _rank(values: list[float]) -> list[float]:
    """Assign ranks to a list of values, handling ties with average ranks.

    Args:
        values: List of numeric values.

    Returns:
        List of ranks (1-based) corresponding to each value.
    """
    indexed = sorted(enumerate(values), key=lambda p: p[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


# ---------------------------------------------------------------------------
# 1. Mann-Whitney U (tier 5)
# ---------------------------------------------------------------------------

@register
class MannWhitneyUGenerator(StepGenerator):
    """Compute the Mann-Whitney U statistic for two small samples.

    Rank all observations together, compute R1, then
    U = n1*n2 + n1*(n1+1)/2 - R1.

    Difficulty scaling:
        Difficulty 1-3: n1=3, n2=3, values in [1, 15].
        Difficulty 4-6: n1=4, n2=4, values in [1, 25].
        Difficulty 7-8: n1=5, n2=5, values in [1, 40].

    Prerequisites:
        sorting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mann_whitney_u"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Mann-Whitney U statistic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mann-Whitney U problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n1, n2 = 3, 3
            hi = 15
        elif difficulty <= 6:
            n1, n2 = 4, 4
            hi = 25
        else:
            n1, n2 = 5, 5
            hi = 40

        s1 = [self._rng.randint(1, hi) for _ in range(n1)]
        s2 = [self._rng.randint(1, hi) for _ in range(n2)]
        combined = s1 + s2
        ranks = _rank([float(v) for v in combined])
        r1 = round(sum(ranks[:n1]), 4)
        u = round(n1 * n2 + n1 * (n1 + 1) / 2 - r1, 4)

        s1_str = ", ".join(str(v) for v in s1)
        s2_str = ", ".join(str(v) for v in s2)
        return (
            f"U = n_1 n_2 + \\frac{{n_1(n_1+1)}}{{2}} - R_1. "
            f"Sample 1: [{s1_str}], Sample 2: [{s2_str}].",
            {
                "s1": s1, "s2": s2, "n1": n1, "n2": n2,
                "combined": combined, "ranks": ranks,
                "r1": r1, "u": u,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Mann-Whitney U.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing combined ranks, R1, and U.
        """
        r_str = ", ".join(str(r) for r in data["ranks"])
        return [
            f"combined ranks: [{r_str}]",
            f"R1 = sum of first {data['n1']} ranks = {data['r1']}",
            f"U = {data['n1']}*{data['n2']} + "
            f"{data['n1']}*{data['n1'] + 1}/2 - {data['r1']} = {data['u']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the U statistic.

        Args:
            data: Solution data dict.

        Returns:
            U value as a string.
        """
        return f"U = {data['u']}"


# ---------------------------------------------------------------------------
# 2. Kruskal-Wallis H (tier 5)
# ---------------------------------------------------------------------------

@register
class KruskalWallisGenerator(StepGenerator):
    """Compute the Kruskal-Wallis H statistic for 3 small groups.

    H = 12/(N(N+1)) * sum(R_i^2 / n_i) - 3*(N+1).

    Difficulty scaling:
        Difficulty 1-3: 3 groups of size 3, values in [1, 15].
        Difficulty 4-6: 3 groups of size 4, values in [1, 25].
        Difficulty 7-8: 3 groups of size 5, values in [1, 40].

    Prerequisites:
        sorting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kruskal_wallis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Kruskal-Wallis H statistic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kruskal-Wallis problem with 3 groups.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            g_size = 3
            hi = 15
        elif difficulty <= 6:
            g_size = 4
            hi = 25
        else:
            g_size = 5
            hi = 40

        groups = [
            [self._rng.randint(1, hi) for _ in range(g_size)]
            for _ in range(3)
        ]
        combined = []
        for g in groups:
            combined.extend(g)

        big_n = len(combined)
        ranks = _rank([float(v) for v in combined])

        rank_sums = []
        offset = 0
        for g in groups:
            n_i = len(g)
            r_i = round(sum(ranks[offset: offset + n_i]), 4)
            rank_sums.append(r_i)
            offset += n_i

        h_sum = sum(r ** 2 / len(g) for r, g in zip(rank_sums, groups))
        h = round(12.0 / (big_n * (big_n + 1)) * h_sum - 3 * (big_n + 1), 4)

        g_strs = [", ".join(str(v) for v in g) for g in groups]
        problem = (
            f"H = \\frac{{12}}{{N(N+1)}} \\sum \\frac{{R_i^2}}{{n_i}} - 3(N+1). "
            f"G1=[{g_strs[0]}], G2=[{g_strs[1]}], G3=[{g_strs[2]}]."
        )
        return (
            problem,
            {
                "groups": groups, "combined": combined,
                "ranks": ranks, "rank_sums": rank_sums,
                "big_n": big_n, "h": h,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Kruskal-Wallis.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing ranks, rank sums, and H.
        """
        steps = [f"N = {data['big_n']}"]
        for i, rs in enumerate(data["rank_sums"]):
            steps.append(f"R_{i + 1} = {rs}")
        steps.append(f"H = {data['h']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the H statistic.

        Args:
            data: Solution data dict.

        Returns:
            H value as a string.
        """
        return f"H = {data['h']}"


# ---------------------------------------------------------------------------
# 3. Permutation Test (tier 5)
# ---------------------------------------------------------------------------

@register
class PermutationTestGenerator(StepGenerator):
    """Perform a simple permutation test on two small groups.

    Compute the observed difference in means, enumerate all permutations
    (or a subset), and compute the p-value as the fraction of permutations
    at least as extreme.

    Difficulty scaling:
        Difficulty 1-3: n1=2, n2=2 (C(4,2)=6 permutations).
        Difficulty 4-6: n1=2, n2=3 (C(5,2)=10 permutations).
        Difficulty 7-8: n1=3, n2=3 (C(6,3)=20 permutations).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "permutation_test"

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
        return "perform permutation test for difference in means"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a permutation test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n1, n2 = 2, 2
        elif difficulty <= 6:
            n1, n2 = 2, 3
        else:
            n1, n2 = 3, 3

        s1 = [self._rng.randint(1, 20) for _ in range(n1)]
        s2 = [self._rng.randint(1, 20) for _ in range(n2)]
        combined = s1 + s2
        obs_diff = round(abs(sum(s1) / n1 - sum(s2) / n2), 4)

        total_perms = math.comb(n1 + n2, n1)
        extreme_count = 0
        perms_shown = []
        for indices in self._combinations(list(range(n1 + n2)), n1):
            g1 = [combined[i] for i in indices]
            g2 = [combined[i] for i in range(n1 + n2) if i not in indices]
            diff = round(abs(sum(g1) / n1 - sum(g2) / n2), 4)
            is_extreme = diff >= obs_diff
            if is_extreme:
                extreme_count += 1
            if len(perms_shown) < 6:
                perms_shown.append({"g1": g1, "diff": diff, "extreme": is_extreme})

        p_value = round(extreme_count / total_perms, 4)

        s1_str = ", ".join(str(v) for v in s1)
        s2_str = ", ".join(str(v) for v in s2)
        return (
            f"Permutation test: S1=[{s1_str}], S2=[{s2_str}]. "
            f"Observed |mean diff| = {obs_diff}.",
            {
                "s1": s1, "s2": s2, "obs_diff": obs_diff,
                "total_perms": total_perms,
                "extreme_count": extreme_count,
                "p_value": p_value, "perms_shown": perms_shown,
            },
        )

    def _combinations(self, pool: list[int], r: int) -> list[list[int]]:
        """Generate all r-combinations from pool.

        Args:
            pool: List of indices.
            r: Combination size.

        Returns:
            List of index lists.
        """
        if r == 0:
            return [[]]
        if not pool:
            return []
        result = []
        for i, val in enumerate(pool):
            for rest in self._combinations(pool[i + 1:], r - 1):
                result.append([val] + rest)
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for permutation test.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing observed diff, permutation count, and p-value.
        """
        steps = [f"observed |diff| = {data['obs_diff']}"]
        steps.append(f"total permutations = {data['total_perms']}")
        steps.append(
            f"permutations >= observed = {data['extreme_count']}"
        )
        steps.append(
            f"p-value = {data['extreme_count']}/{data['total_perms']} "
            f"= {data['p_value']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the permutation test p-value.

        Args:
            data: Solution data dict.

        Returns:
            p-value as a string.
        """
        return f"p-value = {data['p_value']}"


# ---------------------------------------------------------------------------
# 4. Bootstrap CI (tier 5)
# ---------------------------------------------------------------------------

@register
class BootstrapCIGenerator(StepGenerator):
    """Compute a bootstrap confidence interval for the mean.

    Resample with replacement B=5 times, compute the mean of each
    resample, sort the bootstrap means, and find the percentile CI.

    Difficulty scaling:
        Difficulty 1-3: sample size 4, values in [1, 15].
        Difficulty 4-6: sample size 5, values in [1, 25].
        Difficulty 7-8: sample size 6, values in [1, 40].

    Prerequisites:
        sorting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bootstrap_ci"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute bootstrap confidence interval for the mean"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bootstrap CI problem with B=5.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 4
            hi = 15
        elif difficulty <= 6:
            n = 5
            hi = 25
        else:
            n = 6
            hi = 40

        sample = [self._rng.randint(1, hi) for _ in range(n)]
        b_count = 5
        boot_means = []
        boot_samples = []
        for _ in range(b_count):
            resample = [self._rng.choice(sample) for _ in range(n)]
            boot_mean = round(sum(resample) / n, 4)
            boot_samples.append(resample)
            boot_means.append(boot_mean)

        sorted_means = sorted(boot_means)
        ci_lo = sorted_means[0]
        ci_hi = sorted_means[-1]

        s_str = ", ".join(str(v) for v in sample)
        return (
            f"Bootstrap CI (B=5): sample = [{s_str}]. "
            f"Resample with replacement, compute mean each time.",
            {
                "sample": sample, "n": n,
                "boot_samples": boot_samples,
                "boot_means": boot_means,
                "sorted_means": sorted_means,
                "ci_lo": ci_lo, "ci_hi": ci_hi,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for bootstrap CI.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each resample mean and the CI.
        """
        steps = []
        for i, (bs, bm) in enumerate(
            zip(data["boot_samples"], data["boot_means"])
        ):
            bs_str = ", ".join(str(v) for v in bs)
            steps.append(f"B{i + 1}: [{bs_str}] -> mean = {bm}")
        sm_str = ", ".join(str(v) for v in data["sorted_means"])
        steps.append(f"sorted means: [{sm_str}]")
        steps.append(f"CI = [{data['ci_lo']}, {data['ci_hi']}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the bootstrap confidence interval.

        Args:
            data: Solution data dict.

        Returns:
            CI bounds as a string.
        """
        return f"CI = [{data['ci_lo']}, {data['ci_hi']}]"
