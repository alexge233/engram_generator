"""Genetics generators -- Mendelian inheritance, population genetics, linkage.

6 generators across tiers 3-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class GeneticsGenerator(StepGenerator):
    """Base class for genetics generators with shared allele utilities.

    Provides common allele and genotype manipulation helpers used
    by Mendelian and population genetics generators.
    """

    DOMINANT_TRAITS = [
        ("A", "a", "round seeds", "wrinkled seeds"),
        ("B", "b", "purple flowers", "white flowers"),
        ("C", "c", "tall plant", "short plant"),
        ("D", "d", "free earlobes", "attached earlobes"),
        ("E", "e", "brown eyes", "blue eyes"),
        ("W", "w", "widow's peak", "straight hairline"),
    ]

    def _genotype_label(self, g1: str, g2: str) -> str:
        """Return sorted genotype string (dominant first).

        Args:
            g1: First allele.
            g2: Second allele.

        Returns:
            Two-character genotype with uppercase first.
        """
        if g1.isupper():
            return g1 + g2
        return g2 + g1

    def _phenotype(self, genotype: str, dominant_name: str,
                   recessive_name: str) -> str:
        """Return phenotype name for a genotype.

        Args:
            genotype: Two-character genotype string.
            dominant_name: Name when at least one dominant allele.
            recessive_name: Name when homozygous recessive.

        Returns:
            Phenotype name string.
        """
        if genotype[0].isupper() or genotype[1].isupper():
            return dominant_name
        return recessive_name


@register
class PunnettSquareGenerator(GeneticsGenerator):
    """Complete a Punnett square for a monohybrid cross.

    Generates crosses between two heterozygous parents or between
    a heterozygote and a homozygote, computing genotype and phenotype
    ratios from the resulting 2x2 grid.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "punnett_square"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "complete Punnett square for monohybrid cross"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a monohybrid cross problem.

        Selects a trait and parent genotypes based on difficulty.
        Lower difficulties use Aa x Aa; higher may use Aa x aa
        or Aa x AA.

        Args:
            difficulty: Controls cross complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dom, rec, dom_name, rec_name = self._rng.choice(self.DOMINANT_TRAITS)

        cross_types = [(dom + rec, dom + rec)]
        if difficulty >= 3:
            cross_types.append((dom + rec, rec + rec))
        if difficulty >= 5:
            cross_types.append((dom + rec, dom + dom))

        p1, p2 = self._rng.choice(cross_types)

        # Build the 2x2 grid
        p1_alleles = [p1[0], p1[1]]
        p2_alleles = [p2[0], p2[1]]

        offspring = []
        for a1 in p1_alleles:
            for a2 in p2_alleles:
                offspring.append(self._genotype_label(a1, a2))

        # Count genotypes
        geno_counts: dict[str, int] = {}
        for g in offspring:
            geno_counts[g] = geno_counts.get(g, 0) + 1

        # Count phenotypes
        pheno_counts: dict[str, int] = {}
        for g in offspring:
            p = self._phenotype(g, dom_name, rec_name)
            pheno_counts[p] = pheno_counts.get(p, 0) + 1

        geno_ratio = ":".join(
            f"{geno_counts[k]}" for k in sorted(geno_counts.keys())
        )
        pheno_ratio = ":".join(
            f"{pheno_counts[k]}" for k in sorted(pheno_counts.keys())
        )

        return (
            f"cross {p1} x {p2} ({dom_name} dominant)",
            {
                "p1": p1, "p2": p2,
                "offspring": offspring,
                "geno_counts": geno_counts,
                "pheno_counts": pheno_counts,
                "geno_ratio": geno_ratio,
                "pheno_ratio": pheno_ratio,
                "dom_name": dom_name,
                "rec_name": rec_name,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"parent alleles: {sd['p1'][0]},{sd['p1'][1]} x "
            f"{sd['p2'][0]},{sd['p2'][1]}",
            f"offspring: {', '.join(sd['offspring'])}",
        ]
        geno_parts = [f"{k}={v}" for k, v in sorted(sd["geno_counts"].items())]
        steps.append(f"genotype counts: {', '.join(geno_parts)}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the genotype and phenotype ratios.

        Args:
            sd: Solution data.

        Returns:
            Answer string with both ratios.
        """
        pheno_parts = [
            f"{k}={v}" for k, v in sorted(sd["pheno_counts"].items())
        ]
        return f"genotype {sd['geno_ratio']}; phenotype {', '.join(pheno_parts)}"


@register
class DihybridCrossGenerator(GeneticsGenerator):
    """Compute phenotype ratios for a dihybrid cross.

    Generates AaBb x AaBb style crosses with two independent traits,
    producing the classic 9:3:3:1 phenotype ratio or variants when
    different parental genotypes are used.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dihybrid_cross"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["punnett_square"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "compute phenotype ratios for dihybrid cross"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dihybrid cross problem.

        Picks two traits and crosses two double-heterozygous parents.
        Uses the product rule on individual monohybrid ratios.

        Args:
            difficulty: Controls trait selection variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self._rng.sample(
            self.DOMINANT_TRAITS,
            min(2, len(self.DOMINANT_TRAITS)),
        )
        t1 = pool[0]
        t2 = pool[1] if len(pool) > 1 else self.DOMINANT_TRAITS[1]
        d1, r1, dn1, rn1 = t1
        d2, r2, dn2, rn2 = t2

        # Both parents are double heterozygous
        p1 = f"{d1}{r1}{d2}{r2}"
        p2 = f"{d1}{r1}{d2}{r2}"

        # Classic 9:3:3:1
        phenotypes = {
            f"{dn1}, {dn2}": 9,
            f"{dn1}, {rn2}": 3,
            f"{rn1}, {dn2}": 3,
            f"{rn1}, {rn2}": 1,
        }
        ratio = "9:3:3:1"

        return (
            f"cross {p1} x {p2}",
            {
                "p1": p1, "p2": p2,
                "trait1": (d1, r1, dn1, rn1),
                "trait2": (d2, r2, dn2, rn2),
                "phenotypes": phenotypes,
                "ratio": ratio,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps for dihybrid cross.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        d1, r1, dn1, rn1 = sd["trait1"]
        d2, r2, dn2, rn2 = sd["trait2"]
        return [
            f"trait 1: {d1}{r1} x {d1}{r1} -> 3 {dn1} : 1 {rn1}",
            f"trait 2: {d2}{r2} x {d2}{r2} -> 3 {dn2} : 1 {rn2}",
            "combine by product rule: 9:3:3:1",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the phenotype ratio answer.

        Args:
            sd: Solution data.

        Returns:
            Phenotype ratio string.
        """
        parts = [f"{v} {k}" for k, v in sd["phenotypes"].items()]
        return f"{sd['ratio']} = {'; '.join(parts)}"


@register
class HardyWeinbergGenerator(GeneticsGenerator):
    """Compute Hardy-Weinberg equilibrium frequencies.

    Given an allele frequency p (or a genotype frequency), computes
    p, q, p^2, 2pq, and q^2 using the Hardy-Weinberg equation
    p + q = 1.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hardy_weinberg"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "compute Hardy-Weinberg equilibrium frequencies"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hardy-Weinberg problem.

        At lower difficulties gives p directly. At higher difficulties
        gives a genotype frequency (e.g. q^2) and requires deriving p
        and q first.

        Args:
            difficulty: Controls whether p is given or must be derived.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = round(self._rng.uniform(0.1, 0.9), 2)
            q = round(1.0 - p, 4)
            p2 = round(p ** 2, 4)
            two_pq = round(2 * p * q, 4)
            q2 = round(q ** 2, 4)
            problem = f"p = {p}, find genotype frequencies"
            mode = "given_p"
        else:
            q = round(self._rng.uniform(0.1, 0.5), 2)
            q2 = round(q ** 2, 4)
            p = round(1.0 - q, 4)
            p2 = round(p ** 2, 4)
            two_pq = round(2 * p * q, 4)
            problem = f"q^2 = {q2}, find all frequencies"
            mode = "given_q2"

        return problem, {
            "p": p, "q": q, "p2": p2, "two_pq": two_pq, "q2": q2,
            "mode": mode,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        if sd["mode"] == "given_q2":
            steps.append(f"q = sqrt(q^2) = sqrt({sd['q2']}) = {sd['q']}")
        steps.append(f"p + q = 1, so q = {sd['q']}, p = {sd['p']}")
        steps.append(f"p^2 = {sd['p2']}, 2pq = {sd['two_pq']}, q^2 = {sd['q2']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return all Hardy-Weinberg frequencies.

        Args:
            sd: Solution data.

        Returns:
            Formatted frequency string.
        """
        return (
            f"p={sd['p']}, q={sd['q']}, "
            f"p^2={sd['p2']}, 2pq={sd['two_pq']}, q^2={sd['q2']}"
        )


@register
class ChiSquareGeneticsGenerator(GeneticsGenerator):
    """Chi-square goodness-of-fit test for Mendelian ratios.

    Computes X^2 = sum((O - E)^2 / E) from observed and expected
    counts, then compares to a critical value to accept or reject
    the null hypothesis of Mendelian inheritance.
    """

    CHI_SQUARE_CRITICAL = {
        1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chi_square_genetics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hypothesis_test"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "chi-square test for Mendelian ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chi-square genetics problem.

        Creates observed counts near a Mendelian ratio with random
        deviation, computes expected counts, and performs the test.

        Args:
            difficulty: Controls total offspring count and deviation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ratio_sets = [
            ([3, 1], "3:1 monohybrid"),
            ([1, 1], "1:1 testcross"),
        ]
        if difficulty >= 4:
            ratio_sets.append(([9, 3, 3, 1], "9:3:3:1 dihybrid"))

        expected_ratio, label = self._rng.choice(ratio_sets)
        ratio_sum = sum(expected_ratio)
        df = len(expected_ratio) - 1

        total = self._rng.randint(40, 60 + difficulty * 20)

        expected = [round(total * r / ratio_sum, 2) for r in expected_ratio]

        # Generate observed with some deviation
        deviation = self._rng.uniform(0.05, 0.15 + difficulty * 0.02)
        observed = []
        remaining = total
        for i, e in enumerate(expected):
            if i == len(expected) - 1:
                observed.append(remaining)
            else:
                noise = int(e * self._rng.uniform(-deviation, deviation))
                obs = max(1, int(e) + noise)
                observed.append(obs)
                remaining -= obs

        # Compute chi-square
        chi_sq = 0.0
        components = []
        for o, e in zip(observed, expected):
            comp = (o - e) ** 2 / e
            components.append(round(comp, 4))
            chi_sq += comp
        chi_sq = round(chi_sq, 4)

        critical = self.CHI_SQUARE_CRITICAL.get(df, 3.841)
        reject = chi_sq > critical

        obs_str = ",".join(str(o) for o in observed)
        return (
            f"observed [{obs_str}] for {label} (n={total}), test fit",
            {
                "observed": observed, "expected": expected,
                "components": components, "chi_sq": chi_sq,
                "df": df, "critical": critical,
                "reject": reject, "label": label,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate chi-square calculation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"expected: {sd['expected']}"]
        for i, (o, e, c) in enumerate(
            zip(sd["observed"], sd["expected"], sd["components"])
        ):
            steps.append(f"({o}-{e})^2/{e} = {c}")
        steps.append(f"X^2 = {sd['chi_sq']}, df={sd['df']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the chi-square result and decision.

        Args:
            sd: Solution data.

        Returns:
            Chi-square value and accept/reject decision.
        """
        decision = "reject" if sd["reject"] else "fail to reject"
        return (
            f"X^2 = {sd['chi_sq']}, critical = {sd['critical']}, "
            f"{decision} {sd['label']}"
        )


@register
class LinkedGenesGenerator(GeneticsGenerator):
    """Compute recombination frequency from test cross results.

    From a test cross with linked genes, counts parental and
    recombinant offspring to compute the recombination frequency
    as recombinants / total.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "linked_genes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "compute recombination frequency from test cross"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linked genes problem.

        Creates parental and recombinant counts for a test cross,
        with recombination frequency between 1% and 45%.

        Args:
            difficulty: Controls total offspring count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        total = self._rng.randint(100, 200 + difficulty * 100)
        recomb_freq = round(self._rng.uniform(0.01, 0.45), 2)
        recombinants = int(total * recomb_freq)
        parentals = total - recombinants

        # Split into two classes each
        p1 = parentals // 2
        p2 = parentals - p1
        r1 = recombinants // 2
        r2 = recombinants - r1

        actual_freq = round(recombinants / total, 4)
        map_dist = round(actual_freq * 100, 2)

        gene1_d, gene1_r = "A", "a"
        gene2_d, gene2_r = "B", "b"

        return (
            f"test cross: {gene1_d}{gene1_r}{gene2_d}{gene2_r} x "
            f"{gene1_r}{gene1_r}{gene2_r}{gene2_r}; "
            f"offspring: {gene1_d}{gene1_r}{gene2_d}{gene2_r}={p1}, "
            f"{gene1_r}{gene1_r}{gene2_r}{gene2_r}={p2}, "
            f"{gene1_d}{gene1_r}{gene2_r}{gene2_r}={r1}, "
            f"{gene1_r}{gene1_r}{gene2_d}{gene2_r}={r2}",
            {
                "parentals": parentals, "recombinants": recombinants,
                "total": total, "freq": actual_freq,
                "map_dist": map_dist,
                "p1": p1, "p2": p2, "r1": r1, "r2": r2,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"parental types: {sd['p1']} + {sd['p2']} = {sd['parentals']}",
            f"recombinant types: {sd['r1']} + {sd['r2']} = {sd['recombinants']}",
            f"RF = {sd['recombinants']} / {sd['total']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return recombination frequency and map distance.

        Args:
            sd: Solution data.

        Returns:
            Recombination frequency and map distance.
        """
        return f"RF = {sd['freq']}, map distance = {sd['map_dist']} cM"


@register
class BloodTypeGenerator(GeneticsGenerator):
    """Determine possible offspring blood types from parental genotypes.

    Uses the ABO blood group system with three alleles: IA, IB, and i.
    IA and IB are codominant; both are dominant over i.
    """

    BLOOD_GENOTYPES = {
        "A": [("IA", "IA"), ("IA", "i")],
        "B": [("IB", "IB"), ("IB", "i")],
        "AB": [("IA", "IB")],
        "O": [("i", "i")],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "blood_type"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["punnett_square"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "determine possible offspring blood types"

    def _genotype_to_blood(self, a1: str, a2: str) -> str:
        """Convert allele pair to blood type phenotype.

        Args:
            a1: First allele (IA, IB, or i).
            a2: Second allele (IA, IB, or i).

        Returns:
            Blood type string (A, B, AB, or O).
        """
        alleles = {a1, a2}
        if "IA" in alleles and "IB" in alleles:
            return "AB"
        if "IA" in alleles:
            return "A"
        if "IB" in alleles:
            return "B"
        return "O"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a blood type inheritance problem.

        Selects parental blood types and genotypes, then computes
        all possible offspring blood types.

        Args:
            difficulty: Controls genotype variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        blood_types = list(self.BLOOD_GENOTYPES.keys())
        bt1 = self._rng.choice(blood_types)
        bt2 = self._rng.choice(blood_types)

        gt1 = self._rng.choice(self.BLOOD_GENOTYPES[bt1])
        gt2 = self._rng.choice(self.BLOOD_GENOTYPES[bt2])

        # Cross all allele combinations
        offspring_types: set[str] = set()
        offspring_genotypes: list[str] = []
        for a1 in gt1:
            for a2 in gt2:
                bt = self._genotype_to_blood(a1, a2)
                offspring_types.add(bt)
                pair = sorted([a1, a2], key=lambda x: (x != "IA", x != "IB", x))
                offspring_genotypes.append(f"{pair[0]}{pair[1]}")

        sorted_types = sorted(offspring_types)

        gt1_str = f"{gt1[0]}{gt1[1]}"
        gt2_str = f"{gt2[0]}{gt2[1]}"

        return (
            f"parents: {gt1_str} (type {bt1}) x {gt2_str} (type {bt2})",
            {
                "gt1": gt1_str, "gt2": gt2_str,
                "bt1": bt1, "bt2": bt2,
                "offspring_genotypes": offspring_genotypes,
                "offspring_types": sorted_types,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"parent 1: {sd['gt1']} (type {sd['bt1']})",
            f"parent 2: {sd['gt2']} (type {sd['bt2']})",
            f"offspring genotypes: {', '.join(sd['offspring_genotypes'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return possible offspring blood types.

        Args:
            sd: Solution data.

        Returns:
            Comma-separated list of blood types.
        """
        return f"possible types: {', '.join(sd['offspring_types'])}"
