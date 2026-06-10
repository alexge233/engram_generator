"""Extended genetics generators -- epistasis, drift, linkage, quantitative traits.

8 generators across tiers 5-6 deepening population and molecular genetics.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class GeneticsExtBase(StepGenerator):
    """Base class for extended genetics generators.

    Provides shared helpers for population genetics computations
    including allele frequency sampling and fitness calculations.
    """

    @staticmethod
    def _binomial_coeff(n: int, k: int) -> int:
        """Compute binomial coefficient C(n, k).

        Args:
            n: Total items.
            k: Items chosen.

        Returns:
            Integer binomial coefficient.
        """
        if k < 0 or k > n:
            return 0
        return math.comb(n, k)


@register
class EpistasisGenerator(GeneticsExtBase):
    """Compute modified dihybrid ratios from epistatic interactions.

    Models recessive epistasis (9:3:4), dominant epistasis (12:3:1),
    and duplicate recessive epistasis (9:7). Given the epistasis type,
    computes expected phenotype counts from a total offspring number.
    """

    EPISTASIS_TYPES = {
        "recessive": {"ratio": [9, 3, 4], "label": "9:3:4"},
        "dominant": {"ratio": [12, 3, 1], "label": "12:3:1"},
        "duplicate_recessive": {"ratio": [9, 7], "label": "9:7"},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "epistasis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["punnett_square"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute modified dihybrid ratios from epistasis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an epistasis ratio problem.

        Selects an epistasis type, generates a total offspring count,
        and computes expected counts for each phenotype class.

        Args:
            difficulty: Controls offspring count and epistasis type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ep_type = self._rng.choice(list(self.EPISTASIS_TYPES.keys()))
        info = self.EPISTASIS_TYPES[ep_type]
        ratio = info["ratio"]
        ratio_sum = sum(ratio)

        total = self._rng.randint(16 * max(1, difficulty), 160 * max(1, difficulty))
        expected = [round(total * r / ratio_sum, 4) for r in ratio]

        desc = f"{ep_type} epistasis, total offspring={total}; find expected counts"
        return desc, {
            "ep_type": ep_type, "ratio": ratio,
            "ratio_label": info["label"],
            "ratio_sum": ratio_sum, "total": total,
            "expected": expected,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"epistasis type: {sd['ep_type']}",
            f"modified ratio: {sd['ratio_label']} (sum = {sd['ratio_sum']})",
        ]
        for i, (r, e) in enumerate(zip(sd["ratio"], sd["expected"])):
            steps.append(f"class {i+1}: {sd['total']}*{r}/{sd['ratio_sum']} = {e}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return expected phenotype counts.

        Args:
            sd: Solution data.

        Returns:
            Ratio and expected counts as a string.
        """
        counts = ", ".join(str(e) for e in sd["expected"])
        return f"{sd['ratio_label']}; expected = [{counts}]"


@register
class GeneticDriftGenerator(GeneticsExtBase):
    """Compute expected heterozygosity decline from genetic drift.

    Uses H_t = H_0 * (1 - 1/(2N))^t to model heterozygosity loss
    over t generations in a finite population of size N.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "genetic_drift"

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
            Short task description string.
        """
        return "compute expected heterozygosity after genetic drift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a genetic drift heterozygosity problem.

        Creates initial heterozygosity H_0, population size N, and
        number of generations t. Computes H_t from the drift formula.

        Args:
            difficulty: Controls population size and generations.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(5, 50 * max(1, difficulty))
        t = self._rng.randint(1, 5 * max(1, difficulty))
        h0 = round(self._rng.uniform(0.2, 0.5), 4)

        decay_factor = round(1 - 1 / (2 * n), 4)
        decay_power = round(decay_factor ** t, 4)
        h_t = round(h0 * decay_power, 4)

        desc = f"N={n}, H_0={h0}, t={t} generations; find H_t"
        return desc, {
            "n": n, "t": t, "h0": h0,
            "decay_factor": decay_factor,
            "decay_power": decay_power, "h_t": h_t,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "H_t = H_0 * (1 - 1/(2N))^t",
            f"1 - 1/(2*{sd['n']}) = {sd['decay_factor']}",
            f"({sd['decay_factor']})^{sd['t']} = {sd['decay_power']}",
            f"H_t = {sd['h0']} * {sd['decay_power']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return expected heterozygosity at generation t.

        Args:
            sd: Solution data.

        Returns:
            H_t as a string.
        """
        return f"H_t = {sd['h_t']}"


@register
class MutationSelectionGenerator(GeneticsExtBase):
    """Compute mutation-selection equilibrium allele frequency.

    For recessive deleterious alleles: q* = sqrt(mu/s).
    For dominant deleterious alleles: q* = mu/s.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mutation_selection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute mutation-selection equilibrium frequency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mutation-selection balance problem.

        Creates a mutation rate mu and selection coefficient s, then
        computes the equilibrium allele frequency q* for either
        recessive or dominant deleterious alleles.

        Args:
            difficulty: Controls which model is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mu = round(self._rng.uniform(1e-6, 1e-4), 8)
        s = round(self._rng.uniform(0.01, 0.5), 4)

        if difficulty <= 4:
            mode = "recessive"
            q_star = round(math.sqrt(mu / s), 8)
            formula = "q* = sqrt(mu/s)"
        else:
            mode = self._rng.choice(["recessive", "dominant"])
            if mode == "recessive":
                q_star = round(math.sqrt(mu / s), 8)
                formula = "q* = sqrt(mu/s)"
            else:
                q_star = round(mu / s, 8)
                formula = "q* = mu/s"

        ratio = round(mu / s, 8)

        desc = f"mu={mu}, s={s}, {mode} deleterious; find q*"
        return desc, {
            "mu": mu, "s": s, "mode": mode,
            "ratio": ratio, "q_star": q_star,
            "formula": formula,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"{sd['mode']} deleterious allele",
            sd["formula"],
            f"mu/s = {sd['mu']}/{sd['s']} = {sd['ratio']}",
        ]
        if sd["mode"] == "recessive":
            steps.append(f"q* = sqrt({sd['ratio']}) = {sd['q_star']}")
        else:
            steps.append(f"q* = {sd['ratio']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium allele frequency.

        Args:
            sd: Solution data.

        Returns:
            q* as a string.
        """
        return f"q* = {sd['q_star']}"


@register
class LinkageDisequilibriumGenerator(GeneticsExtBase):
    """Compute linkage disequilibrium statistics D, D', and r-squared.

    D = f(AB) - f(A)*f(B). D' = D/D_max.
    r^2 = D^2 / (f(A)*f(a)*f(B)*f(b)).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "linkage_disequilibrium"

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
            Short task description string.
        """
        return "compute linkage disequilibrium D, D', and r^2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linkage disequilibrium problem.

        Creates haplotype frequencies that sum to 1.0, derives
        allele frequencies, and computes D, D', and r^2.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Generate four haplotype frequencies summing to 1
        f_ab = round(self._rng.uniform(0.1, 0.4), 4)
        f_aB = round(self._rng.uniform(0.05, min(0.3, 1 - f_ab - 0.15)), 4)
        f_Ab = round(self._rng.uniform(0.05, min(0.3, 1 - f_ab - f_aB - 0.1)), 4)
        f_ab_lower = round(max(0.01, 1 - f_ab - f_aB - f_Ab), 4)

        # Allele frequencies
        f_A = round(f_ab + f_Ab, 4)  # f(AB) + f(Ab)
        f_a = round(1 - f_A, 4)
        f_B = round(f_ab + f_aB, 4)  # f(AB) + f(aB)
        f_b = round(1 - f_B, 4)

        # D = f(AB) - f(A)*f(B)
        expected_ab = round(f_A * f_B, 4)
        d_val = round(f_ab - expected_ab, 4)

        # D_max
        if d_val >= 0:
            d_max = round(min(f_A * f_b, f_a * f_B), 4)
        else:
            d_max = round(min(f_A * f_B, f_a * f_b), 4)

        d_prime = round(d_val / d_max, 4) if abs(d_max) > 1e-10 else 0.0

        # r^2
        denom = f_A * f_a * f_B * f_b
        r_sq = round(d_val ** 2 / denom, 4) if abs(denom) > 1e-10 else 0.0

        desc = (
            f"f(AB)={f_ab}, f(aB)={f_aB}, f(Ab)={f_Ab}, "
            f"f(ab)={f_ab_lower}; compute D, D', r^2"
        )
        return desc, {
            "f_AB": f_ab, "f_aB": f_aB, "f_Ab": f_Ab,
            "f_ab": f_ab_lower, "f_A": f_A, "f_a": f_a,
            "f_B": f_B, "f_b": f_b, "expected_ab": expected_ab,
            "d_val": d_val, "d_max": d_max,
            "d_prime": d_prime, "r_sq": r_sq,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"f(A) = f(AB)+f(Ab) = {sd['f_AB']}+{sd['f_Ab']} = {sd['f_A']}",
            f"f(B) = f(AB)+f(aB) = {sd['f_AB']}+{sd['f_aB']} = {sd['f_B']}",
            f"D = f(AB) - f(A)*f(B) = {sd['f_AB']} - {sd['expected_ab']} = {sd['d_val']}",
            f"D_max = {sd['d_max']}",
            f"D' = D/D_max = {sd['d_val']}/{sd['d_max']} = {sd['d_prime']}",
            f"r^2 = D^2/(f(A)*f(a)*f(B)*f(b)) = {sd['r_sq']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return D, D', and r^2.

        Args:
            sd: Solution data.

        Returns:
            LD statistics as a string.
        """
        return f"D = {sd['d_val']}, D' = {sd['d_prime']}, r^2 = {sd['r_sq']}"


@register
class CoalescentTimeGenerator(GeneticsExtBase):
    """Compute expected coalescent time for k lineages.

    For 2 lineages: E[T_2] = 2*N_e generations.
    For k lineages: E[T_k] = 4*N_e / (k*(k-1)) generations.
    Total expected time to MRCA = sum over k from n to 2.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coalescent_time"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute expected coalescent time for k lineages"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coalescent time problem.

        Creates an effective population size N_e and a number of
        lineages k. Computes expected time for k lineages to coalesce
        to k-1 and the total expected time to MRCA.

        Args:
            difficulty: Controls number of lineages.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ne = self._rng.randint(100, 1000 * max(1, difficulty))
        k = self._rng.randint(2, min(3 + difficulty, 8))

        # E[T_k] for each k down to 2
        coalescent_times = []
        total_time = 0.0
        for ki in range(k, 1, -1):
            t_ki = round(4 * ne / (ki * (ki - 1)), 4)
            coalescent_times.append((ki, t_ki))
            total_time += t_ki
        total_time = round(total_time, 4)

        desc = f"N_e={ne}, k={k} lineages; find total time to MRCA"
        return desc, {
            "ne": ne, "k": k,
            "coalescent_times": coalescent_times,
            "total_time": total_time,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"E[T_k] = 4*N_e / (k*(k-1))"]
        for ki, t_ki in sd["coalescent_times"]:
            steps.append(
                f"E[T_{ki}] = 4*{sd['ne']}/({ki}*{ki-1}) = {t_ki} gen"
            )
        steps.append(f"total = sum = {sd['total_time']} generations")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return total expected time to MRCA.

        Args:
            sd: Solution data.

        Returns:
            Total coalescent time as a string.
        """
        return f"E[T_MRCA] = {sd['total_time']} generations"


@register
class QuantitativeTraitGenerator(GeneticsExtBase):
    """Compute heritability and response to selection.

    V_P = V_G + V_E. Heritability h^2 = V_G / V_P.
    Response to selection R = h^2 * S where S is the selection
    differential.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantitative_trait"

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
            Short task description string.
        """
        return "compute heritability and response to selection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantitative genetics problem.

        Creates phenotypic, genetic, and environmental variance
        components. Computes heritability and selection response.

        Args:
            difficulty: Controls variance magnitudes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vg = round(self._rng.uniform(1.0, 10.0 * max(1, difficulty)), 4)
        ve = round(self._rng.uniform(1.0, 10.0 * max(1, difficulty)), 4)
        vp = round(vg + ve, 4)
        h2 = round(vg / vp, 4)

        s_diff = round(self._rng.uniform(0.5, 5.0 * max(1, difficulty)), 4)
        response = round(h2 * s_diff, 4)

        desc = f"V_G={vg}, V_E={ve}, S={s_diff}; find h^2 and R"
        return desc, {
            "vg": vg, "ve": ve, "vp": vp,
            "h2": h2, "s_diff": s_diff, "response": response,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"V_P = V_G + V_E = {sd['vg']} + {sd['ve']} = {sd['vp']}",
            f"h^2 = V_G/V_P = {sd['vg']}/{sd['vp']} = {sd['h2']}",
            f"R = h^2 * S = {sd['h2']} * {sd['s_diff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return heritability and selection response.

        Args:
            sd: Solution data.

        Returns:
            h^2 and R as a string.
        """
        return f"h^2 = {sd['h2']}, R = {sd['response']}"


@register
class PopulationBottleneckGenerator(GeneticsExtBase):
    """Compute expected heterozygosity loss from a population bottleneck.

    Heterozygosity loss per generation in bottleneck: 1/(2*N_b).
    H_after = H_before * (1 - 1/(2*N_b))^t_bottleneck.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "population_bottleneck"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute heterozygosity loss from population bottleneck"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a population bottleneck problem.

        Creates a bottleneck population size, duration, and initial
        heterozygosity. Computes remaining heterozygosity after the
        bottleneck event.

        Args:
            difficulty: Controls bottleneck severity and duration.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        nb = self._rng.randint(2, 20 * max(1, difficulty))
        t_bottle = self._rng.randint(1, 3 + difficulty)
        h_before = round(self._rng.uniform(0.3, 0.5), 4)

        loss_per_gen = round(1 / (2 * nb), 4)
        retention = round(1 - loss_per_gen, 4)
        retention_power = round(retention ** t_bottle, 4)
        h_after = round(h_before * retention_power, 4)
        fraction_lost = round(1 - retention_power, 4)

        desc = (
            f"N_b={nb}, t={t_bottle} gen, H_before={h_before}; "
            f"find H_after"
        )
        return desc, {
            "nb": nb, "t_bottle": t_bottle, "h_before": h_before,
            "loss_per_gen": loss_per_gen, "retention": retention,
            "retention_power": retention_power,
            "h_after": h_after, "fraction_lost": fraction_lost,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"loss per gen = 1/(2*{sd['nb']}) = {sd['loss_per_gen']}",
            f"retention = 1 - {sd['loss_per_gen']} = {sd['retention']}",
            f"({sd['retention']})^{sd['t_bottle']} = {sd['retention_power']}",
            f"H_after = {sd['h_before']} * {sd['retention_power']}",
            f"fraction lost = {sd['fraction_lost']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return heterozygosity after bottleneck.

        Args:
            sd: Solution data.

        Returns:
            H_after as a string.
        """
        return f"H_after = {sd['h_after']}"


@register
class InbreedingCoefficientGenerator(GeneticsExtBase):
    """Compute inbreeding coefficient and inbreeding depression.

    F is the probability of identity by descent. For self-fertilisation
    F = 0.5, for full-sib mating F = 0.25. Fitness with inbreeding
    depression: w = 1 - B*F where B is the inbreeding load.
    """

    MATING_TYPES = {
        "self-fertilisation": 0.5,
        "full-sib": 0.25,
        "half-sib": 0.125,
        "first-cousin": 0.0625,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inbreeding_coefficient"

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
            Short task description string.
        """
        return "compute inbreeding coefficient and fitness depression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inbreeding coefficient problem.

        Selects a mating type, assigns the inbreeding coefficient F,
        and computes fitness with inbreeding depression.

        Args:
            difficulty: Controls mating type complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            mating_pool = ["self-fertilisation", "full-sib"]
        else:
            mating_pool = list(self.MATING_TYPES.keys())

        mating = self._rng.choice(mating_pool)
        f_val = self.MATING_TYPES[mating]

        # Inbreeding load B (number of lethal equivalents)
        b_load = round(self._rng.uniform(0.5, 3.0), 4)
        fitness = round(1 - b_load * f_val, 4)

        # Multiple generations of same mating
        n_gen = self._rng.randint(1, min(3, 1 + difficulty // 2))
        # F after n generations: F_n = 1 - (1-F)^n (simplified)
        f_cumulative = round(1 - (1 - f_val) ** n_gen, 4)
        fitness_cumul = round(1 - b_load * f_cumulative, 4)

        desc = (
            f"mating: {mating}, B={b_load}, "
            f"generations={n_gen}; find F and fitness"
        )
        return desc, {
            "mating": mating, "f_val": f_val, "b_load": b_load,
            "fitness": fitness, "n_gen": n_gen,
            "f_cumulative": f_cumulative,
            "fitness_cumul": fitness_cumul,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"mating type: {sd['mating']}, F = {sd['f_val']}",
            f"single-gen fitness: w = 1 - B*F = 1 - {sd['b_load']}*{sd['f_val']} = {sd['fitness']}",
        ]
        if sd["n_gen"] > 1:
            steps.append(
                f"F after {sd['n_gen']} gen = 1-(1-{sd['f_val']})^{sd['n_gen']} = {sd['f_cumulative']}"
            )
            steps.append(
                f"fitness = 1 - {sd['b_load']}*{sd['f_cumulative']} = {sd['fitness_cumul']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the inbreeding coefficient and fitness.

        Args:
            sd: Solution data.

        Returns:
            F and fitness as a string.
        """
        if sd["n_gen"] > 1:
            return f"F = {sd['f_cumulative']}, fitness = {sd['fitness_cumul']}"
        return f"F = {sd['f_val']}, fitness = {sd['fitness']}"
