"""Ecology generators -- population dynamics, diversity indices, trophic energy.

6 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class EcologyBase(StepGenerator):
    """Base class for ecology generators with shared constants.

    Provides common ecological constants and helper methods used
    across population dynamics and community ecology generators.
    """

    LN2 = round(math.log(2), 4)


@register
class LogisticGrowthGenerator(EcologyBase):
    """Compute population size using the logistic growth equation.

    Applies N(t) = K / (1 + ((K - N0) / N0) * e^(-r*t)) to compute
    population size at time t given carrying capacity K, initial
    population N0, and intrinsic growth rate r.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logistic_growth"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute population size using logistic growth model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logistic growth problem.

        Creates ecologically plausible parameter values: carrying
        capacity K, initial population N0 < K, growth rate r, and
        time t. Computes N(t) from the logistic equation.

        Args:
            difficulty: Controls parameter magnitude and time range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = self._rng.randint(100, 200 * difficulty)
        n0 = self._rng.randint(5, max(6, k // (2 + difficulty)))
        r = round(self._rng.uniform(0.05, 0.1 * difficulty), 4)
        t = self._rng.randint(1, 3 + difficulty)

        ratio = (k - n0) / n0
        exp_term = round(math.exp(-r * t), 4)
        denominator = round(1 + ratio * exp_term, 4)
        nt = round(k / denominator, 4)

        desc = f"K={k}, N0={n0}, r={r}, t={t}; find N(t)"
        return desc, {
            "k": k, "n0": n0, "r": r, "t": t,
            "ratio": round(ratio, 4), "exp_term": exp_term,
            "denominator": denominator, "nt": nt,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "N(t) = K / (1 + ((K-N0)/N0) * e^(-r*t))",
            f"(K-N0)/N0 = ({sd['k']}-{sd['n0']})/{sd['n0']} = {sd['ratio']}",
            f"e^(-{sd['r']}*{sd['t']}) = {sd['exp_term']}",
            f"denominator = 1 + {sd['ratio']}*{sd['exp_term']} = {sd['denominator']}",
            f"N(t) = {sd['k']} / {sd['denominator']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the population at time t.

        Args:
            sd: Solution data.

        Returns:
            N(t) as a string.
        """
        return f"N({sd['t']}) = {sd['nt']}"


@register
class LotkaVolterraGenerator(EcologyBase):
    """Compute one-step Lotka-Volterra predator-prey dynamics.

    Given prey population x, predator population y, and rate parameters
    a, b, c, d, computes the rates of change:
    dx/dt = a*x - b*x*y and dy/dt = -c*y + d*x*y.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lotka_volterra"

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
        return "compute Lotka-Volterra rates of change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lotka-Volterra one-step problem.

        Creates ecologically plausible parameter values and population
        sizes, then computes dx/dt and dy/dt.

        Args:
            difficulty: Controls parameter precision and population size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x = self._rng.randint(10, 50 * difficulty)
        y = self._rng.randint(5, 20 * difficulty)
        a = round(self._rng.uniform(0.1, 0.5), 4)
        b = round(self._rng.uniform(0.001, 0.02), 4)
        c = round(self._rng.uniform(0.1, 0.5), 4)
        d = round(self._rng.uniform(0.001, 0.02), 4)

        ax = round(a * x, 4)
        bxy = round(b * x * y, 4)
        cy = round(c * y, 4)
        dxy = round(d * x * y, 4)

        dx_dt = round(ax - bxy, 4)
        dy_dt = round(-cy + dxy, 4)

        desc = f"x={x}, y={y}, a={a}, b={b}, c={c}, d={d}"
        return desc, {
            "x": x, "y": y, "a": a, "b": b, "c": c, "d": d,
            "ax": ax, "bxy": bxy, "cy": cy, "dxy": dxy,
            "dx_dt": dx_dt, "dy_dt": dy_dt,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"a*x = {sd['a']}*{sd['x']} = {sd['ax']}",
            f"b*x*y = {sd['b']}*{sd['x']}*{sd['y']} = {sd['bxy']}",
            f"dx/dt = {sd['ax']} - {sd['bxy']} = {sd['dx_dt']}",
            f"c*y = {sd['c']}*{sd['y']} = {sd['cy']}",
            f"d*x*y = {sd['d']}*{sd['x']}*{sd['y']} = {sd['dxy']}",
            f"dy/dt = -{sd['cy']} + {sd['dxy']} = {sd['dy_dt']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return dx/dt and dy/dt.

        Args:
            sd: Solution data.

        Returns:
            Both rates of change as a string.
        """
        return f"dx/dt = {sd['dx_dt']}, dy/dt = {sd['dy_dt']}"


@register
class PopulationDoublingGenerator(EcologyBase):
    """Compute doubling time or growth rate from exponential growth.

    Uses the relationship t_double = ln(2) / r. Given one of the two
    values, computes the other.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "population_doubling"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute population doubling time or growth rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a population doubling problem.

        With equal probability, either gives r and asks for t_double,
        or gives t_double and asks for r.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mode = self._rng.choice(["find_t", "find_r"])

        if mode == "find_t":
            r = round(self._rng.uniform(0.01, 0.05 * difficulty), 4)
            t_double = round(self.LN2 / r, 4)
            desc = f"growth rate r = {r}; find doubling time"
        else:
            t_double = round(self._rng.uniform(1.0, 5.0 * difficulty), 4)
            r = round(self.LN2 / t_double, 4)
            desc = f"doubling time = {t_double}; find growth rate r"

        return desc, {
            "mode": mode, "r": r, "t_double": t_double,
            "ln2": self.LN2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["t_double = ln(2) / r", f"ln(2) = {sd['ln2']}"]
        if sd["mode"] == "find_t":
            steps.append(
                f"t_double = {sd['ln2']} / {sd['r']} = {sd['t_double']}"
            )
        else:
            steps.append(
                f"r = {sd['ln2']} / {sd['t_double']} = {sd['r']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the computed value.

        Args:
            sd: Solution data.

        Returns:
            Doubling time or growth rate as a string.
        """
        if sd["mode"] == "find_t":
            return f"t_double = {sd['t_double']}"
        return f"r = {sd['r']}"


@register
class TrophicEfficiencyGenerator(EcologyBase):
    """Compute energy at a trophic level using the 10% rule.

    Energy at level n = E_0 * (0.1)^n, where E_0 is the energy at
    the producer level (level 0). Given producer energy and a target
    trophic level, computes the available energy.
    """

    TROPHIC_NAMES = {
        0: "producers",
        1: "primary consumers",
        2: "secondary consumers",
        3: "tertiary consumers",
        4: "quaternary consumers",
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trophic_efficiency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute energy available at a trophic level"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trophic efficiency problem.

        Creates a producer energy value and a target trophic level,
        then computes energy transferred using the 10% rule.

        Args:
            difficulty: Controls trophic level depth and energy magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        e0 = self._rng.randint(1000, 10000 * max(1, difficulty))
        level = self._rng.randint(1, min(4, 1 + difficulty // 2))

        factor = round(0.1 ** level, 4 + level)
        energy = round(e0 * factor, 4)
        level_name = self.TROPHIC_NAMES.get(level, f"level {level}")

        desc = (
            f"producer energy E0 = {e0} kJ; "
            f"find energy at {level_name} (level {level})"
        )
        return desc, {
            "e0": e0, "level": level, "factor": factor,
            "energy": energy, "level_name": level_name,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"E(n) = E0 * (0.1)^n",
            f"E({sd['level']}) = {sd['e0']} * (0.1)^{sd['level']}",
            f"(0.1)^{sd['level']} = {sd['factor']}",
            f"E({sd['level']}) = {sd['e0']} * {sd['factor']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the energy at the target trophic level.

        Args:
            sd: Solution data.

        Returns:
            Energy value with units.
        """
        return f"E({sd['level']}) = {sd['energy']} kJ"


@register
class SpeciesDiversityGenerator(EcologyBase):
    """Compute the Shannon diversity index from species abundance data.

    Shannon index H' = -sum(p_i * ln(p_i)) where p_i is the proportion
    of each species in the community. Given raw counts, computes
    proportions and then H'.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "species_diversity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Shannon diversity index from species counts"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Shannon diversity index problem.

        Creates a community with 3-6 species and random abundance
        counts, then computes proportions and H'.

        Args:
            difficulty: Controls number of species and count magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_species = self._rng.randint(3, min(6, 2 + difficulty))
        species_names = [
            "species A", "species B", "species C",
            "species D", "species E", "species F",
        ][:num_species]

        counts = [
            self._rng.randint(1, 20 * max(1, difficulty))
            for _ in range(num_species)
        ]
        total = sum(counts)

        proportions = [round(c / total, 4) for c in counts]
        terms = []
        for p in proportions:
            if p > 0:
                terms.append(round(p * math.log(p), 4))
        h_prime = round(-sum(terms), 4)

        count_strs = [
            f"{name}: {c}" for name, c in zip(species_names, counts)
        ]
        desc = f"community counts: {', '.join(count_strs)}"

        return desc, {
            "counts": counts, "total": total,
            "proportions": proportions, "terms": terms,
            "h_prime": h_prime, "species_names": species_names,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"total individuals = {sd['total']}"]
        for name, c, p in zip(
            sd["species_names"], sd["counts"], sd["proportions"],
        ):
            steps.append(f"p({name}) = {c}/{sd['total']} = {p}")
        steps.append("H' = -sum(p_i * ln(p_i))")
        term_strs = [str(t) for t in sd["terms"]]
        steps.append(f"terms = [{', '.join(term_strs)}]")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Shannon diversity index.

        Args:
            sd: Solution data.

        Returns:
            H' value as a string.
        """
        return f"H' = {sd['h_prime']}"


@register
class CarryingCapacityGenerator(EcologyBase):
    """Estimate carrying capacity from two population measurements.

    Given two observations (N1 at t1, N2 at t2) under logistic growth
    with known growth rate r, estimates the carrying capacity K by
    rearranging the logistic equation.

    From N(t) = K / (1 + A*e^(-r*t)) where A = (K-N0)/N0, we can
    derive K from two data points using the ratio method.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carrying_capacity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logistic_growth"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "estimate carrying capacity from population data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a carrying capacity estimation problem.

        First generates a true K and growth parameters, simulates
        two population measurements at different times, then asks
        the student to recover K.

        The approach: from N = K / (1 + A*e^(-rt)), rearrange to
        1/N = 1/K + (A/K)*e^(-rt). With two measurements and known r,
        solve for K and A.

        Let u1 = 1/N1, u2 = 1/N2, e1 = e^(-r*t1), e2 = e^(-r*t2).
        Then A/K = (u1 - u2) / (e1 - e2) and 1/K = u1 - (A/K)*e1.

        Args:
            difficulty: Controls population size and time separation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k_true = self._rng.randint(200, 500 * max(1, difficulty))
        n0 = self._rng.randint(10, max(11, k_true // 10))
        r = round(self._rng.uniform(0.05, 0.1 * max(1, difficulty // 2)), 4)

        t1 = self._rng.randint(1, 3)
        t2 = t1 + self._rng.randint(2, 4 + difficulty)

        # Compute populations at t1 and t2 from true K
        a_true = (k_true - n0) / n0
        n1 = round(k_true / (1 + a_true * math.exp(-r * t1)), 4)
        n2 = round(k_true / (1 + a_true * math.exp(-r * t2)), 4)

        # Recover K from the two measurements
        u1 = round(1 / n1, 4) if n1 > 0 else 0
        u2 = round(1 / n2, 4) if n2 > 0 else 0
        e1 = round(math.exp(-r * t1), 4)
        e2 = round(math.exp(-r * t2), 4)

        if abs(e1 - e2) < 1e-10:
            # Degenerate case: fall back to simpler parameters
            t2 = t1 + 5
            n2 = round(k_true / (1 + a_true * math.exp(-r * t2)), 4)
            u2 = round(1 / n2, 4)
            e2 = round(math.exp(-r * t2), 4)

        a_over_k = round((u1 - u2) / (e1 - e2), 4)
        one_over_k = round(u1 - a_over_k * e1, 4)
        k_est = round(1 / one_over_k, 4) if abs(one_over_k) > 1e-10 else k_true

        desc = (
            f"N({t1})={n1}, N({t2})={n2}, r={r}; "
            f"estimate carrying capacity K"
        )

        return desc, {
            "n1": n1, "n2": n2, "t1": t1, "t2": t2, "r": r,
            "u1": u1, "u2": u2, "e1": e1, "e2": e2,
            "a_over_k": a_over_k, "one_over_k": one_over_k,
            "k_est": k_est,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "from N = K/(1+A*e^(-rt)), let u = 1/N",
            f"u1 = 1/{sd['n1']} = {sd['u1']}",
            f"u2 = 1/{sd['n2']} = {sd['u2']}",
            f"e^(-r*t1) = e^(-{sd['r']}*{sd['t1']}) = {sd['e1']}",
            f"e^(-r*t2) = e^(-{sd['r']}*{sd['t2']}) = {sd['e2']}",
            f"A/K = (u1-u2)/(e1-e2) = {sd['a_over_k']}",
            f"1/K = u1 - (A/K)*e1 = {sd['one_over_k']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the estimated carrying capacity.

        Args:
            sd: Solution data.

        Returns:
            K estimate as a string.
        """
        return f"K = {sd['k_est']}"
