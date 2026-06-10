"""Epidemiology generators -- disease dynamics, risk measures, life tables.

6 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class EpidemiologyBase(StepGenerator):
    """Base class for epidemiology generators with shared helpers.

    Provides common epidemiological constants and utility methods
    used across disease modelling and risk calculation generators.
    """


@register
class SirModelGenerator(EpidemiologyBase):
    """Compute one Euler step of the SIR compartmental model.

    Applies dS/dt = -beta*S*I/N, dI/dt = beta*S*I/N - gamma*I,
    dR/dt = gamma*I with a fixed time step dt to advance the
    susceptible, infected, and recovered compartments.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sir_model"

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
        return "compute one Euler step of the SIR model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SIR Euler step problem.

        Creates epidemiologically plausible parameter values for
        population size N, initial compartments S, I, R, transmission
        rate beta, recovery rate gamma, and time step dt. Computes
        the derivatives and new compartment values after one step.

        Args:
            difficulty: Controls population size and parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(500, 1000 * difficulty)
        i = self._rng.randint(1, max(2, n // (10 + difficulty)))
        r = self._rng.randint(0, max(1, n // (20 + difficulty)))
        s = n - i - r

        beta = round(self._rng.uniform(0.1, 0.5), 4)
        gamma = round(self._rng.uniform(0.02, 0.15), 4)
        dt = round(self._rng.uniform(0.1, 1.0), 2)

        si_over_n = round(beta * s * i / n, 4)
        gamma_i = round(gamma * i, 4)

        ds = round(-si_over_n * dt, 4)
        di = round((si_over_n - gamma_i) * dt, 4)
        dr = round(gamma_i * dt, 4)

        s_new = round(s + ds, 4)
        i_new = round(i + di, 4)
        r_new = round(r + dr, 4)

        desc = (
            f"N={n}, S={s}, I={i}, R={r}, "
            f"beta={beta}, gamma={gamma}, dt={dt}"
        )
        return desc, {
            "n": n, "s": s, "i": i, "r": r,
            "beta": beta, "gamma": gamma, "dt": dt,
            "si_over_n": si_over_n, "gamma_i": gamma_i,
            "ds": ds, "di": di, "dr": dr,
            "s_new": s_new, "i_new": i_new, "r_new": r_new,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"beta*S*I/N = {sd['beta']}*{sd['s']}*{sd['i']}/{sd['n']} = {sd['si_over_n']}",
            f"gamma*I = {sd['gamma']}*{sd['i']} = {sd['gamma_i']}",
            f"dS = -{sd['si_over_n']}*{sd['dt']} = {sd['ds']}",
            f"dI = ({sd['si_over_n']}-{sd['gamma_i']})*{sd['dt']} = {sd['di']}",
            f"dR = {sd['gamma_i']}*{sd['dt']} = {sd['dr']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the updated compartment values.

        Args:
            sd: Solution data.

        Returns:
            New S, I, R values as a string.
        """
        return f"S={sd['s_new']}, I={sd['i_new']}, R={sd['r_new']}"


@register
class BasicReproductionGenerator(EpidemiologyBase):
    """Compute the basic reproduction number R_0 and classify epidemic fate.

    Calculates R_0 = beta / gamma from given transmission and recovery
    rates, then classifies whether the epidemic grows (R_0 > 1) or
    dies out (R_0 < 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "basic_reproduction"

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
        return "compute R_0 and classify epidemic outcome"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a basic reproduction number problem.

        Creates plausible beta and gamma values, ensuring a mix of
        growing and dying epidemics across generated samples.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        beta = round(self._rng.uniform(0.05, 0.2 * difficulty), 4)
        gamma = round(self._rng.uniform(0.02, 0.3), 4)

        r0 = round(beta / gamma, 4)
        classification = "epidemic grows" if r0 > 1 else "epidemic dies out"

        desc = f"beta={beta}, gamma={gamma}; compute R_0 and classify"
        return desc, {
            "beta": beta, "gamma": gamma,
            "r0": r0, "classification": classification,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "R_0 = beta / gamma",
            f"R_0 = {sd['beta']} / {sd['gamma']} = {sd['r0']}",
            f"R_0 {'>' if sd['r0'] > 1 else '<'} 1 => {sd['classification']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return R_0 and classification.

        Args:
            sd: Solution data.

        Returns:
            R_0 value and epidemic fate.
        """
        return f"R_0 = {sd['r0']}, {sd['classification']}"


@register
class IncidenceRateGenerator(EpidemiologyBase):
    """Compute incidence rate and prevalence from case data.

    Incidence rate = new_cases / population_at_risk / time_period.
    Prevalence = total_cases / population. Generates both measures
    from a set of epidemiological data.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "incidence_rate"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute incidence rate and prevalence from case data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an incidence rate and prevalence problem.

        Creates population size, new case count, total case count,
        population at risk, and observation time period. Computes
        both incidence rate and point prevalence.

        Args:
            difficulty: Controls population magnitude and case numbers.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        population = self._rng.randint(1000, 5000 * difficulty)
        new_cases = self._rng.randint(5, max(6, population // (20 + difficulty)))
        total_cases = new_cases + self._rng.randint(0, max(1, new_cases * 2))
        pop_at_risk = population - total_cases + new_cases
        time_period = self._rng.randint(1, 2 + difficulty)

        incidence = round(new_cases / pop_at_risk / time_period, 4)
        prevalence = round(total_cases / population, 4)

        desc = (
            f"population={population}, new_cases={new_cases}, "
            f"total_cases={total_cases}, pop_at_risk={pop_at_risk}, "
            f"time={time_period} years"
        )
        return desc, {
            "population": population, "new_cases": new_cases,
            "total_cases": total_cases, "pop_at_risk": pop_at_risk,
            "time_period": time_period,
            "incidence": incidence, "prevalence": prevalence,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "incidence = new_cases / pop_at_risk / time",
            f"incidence = {sd['new_cases']} / {sd['pop_at_risk']} / {sd['time_period']} = {sd['incidence']}",
            "prevalence = total_cases / population",
            f"prevalence = {sd['total_cases']} / {sd['population']} = {sd['prevalence']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return incidence rate and prevalence.

        Args:
            sd: Solution data.

        Returns:
            Both measures as a string.
        """
        return f"incidence = {sd['incidence']}, prevalence = {sd['prevalence']}"


@register
class RelativeRiskGenerator(EpidemiologyBase):
    """Compute relative risk and odds ratio from a 2x2 contingency table.

    Given cells a, b, c, d where a = exposed+disease, b = exposed+no disease,
    c = unexposed+disease, d = unexposed+no disease, computes:
    RR = (a/(a+b)) / (c/(c+d)) and OR = (a*d) / (b*c).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relative_risk"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute relative risk and odds ratio from contingency table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a relative risk and odds ratio problem.

        Creates a 2x2 contingency table with plausible cell counts
        and computes RR and OR.

        Args:
            difficulty: Controls cell count magnitudes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        scale = 5 * max(1, difficulty)
        a = self._rng.randint(5, 10 * scale)
        b = self._rng.randint(10, 20 * scale)
        c = self._rng.randint(3, 8 * scale)
        d = self._rng.randint(15, 30 * scale)

        risk_exposed = round(a / (a + b), 4)
        risk_unexposed = round(c / (c + d), 4)
        rr = round(risk_exposed / risk_unexposed, 4)
        odds_ratio = round((a * d) / (b * c), 4)

        desc = (
            f"2x2 table: a={a} (exposed+disease), b={b} (exposed+no disease), "
            f"c={c} (unexposed+disease), d={d} (unexposed+no disease)"
        )
        return desc, {
            "a": a, "b": b, "c": c, "d": d,
            "risk_exposed": risk_exposed,
            "risk_unexposed": risk_unexposed,
            "rr": rr, "odds_ratio": odds_ratio,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"risk_exposed = {sd['a']}/({sd['a']}+{sd['b']}) = {sd['risk_exposed']}",
            f"risk_unexposed = {sd['c']}/({sd['c']}+{sd['d']}) = {sd['risk_unexposed']}",
            f"RR = {sd['risk_exposed']}/{sd['risk_unexposed']} = {sd['rr']}",
            f"OR = ({sd['a']}*{sd['d']})/({sd['b']}*{sd['c']}) = {sd['odds_ratio']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return RR and OR.

        Args:
            sd: Solution data.

        Returns:
            Both risk measures as a string.
        """
        return f"RR = {sd['rr']}, OR = {sd['odds_ratio']}"


@register
class HerdImmunityGenerator(EpidemiologyBase):
    """Compute herd immunity threshold from R_0.

    The critical vaccination threshold is p_c = 1 - 1/R_0. Given
    R_0, computes the percentage of the population that must be
    immune to prevent sustained transmission.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "herd_immunity"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute herd immunity threshold from R_0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a herd immunity threshold problem.

        Creates an R_0 value greater than 1 (since herd immunity
        only applies to growing epidemics) and computes the critical
        proportion for herd immunity.

        Args:
            difficulty: Controls R_0 range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r0 = round(self._rng.uniform(1.2, 2.0 + difficulty * 1.5), 4)
        one_over_r0 = round(1 / r0, 4)
        threshold = round(1 - one_over_r0, 4)
        percentage = round(threshold * 100, 4)

        desc = f"R_0 = {r0}; compute herd immunity threshold"
        return desc, {
            "r0": r0, "one_over_r0": one_over_r0,
            "threshold": threshold, "percentage": percentage,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "p_c = 1 - 1/R_0",
            f"1/R_0 = 1/{sd['r0']} = {sd['one_over_r0']}",
            f"p_c = 1 - {sd['one_over_r0']} = {sd['threshold']}",
            f"percentage = {sd['percentage']}%",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the herd immunity threshold.

        Args:
            sd: Solution data.

        Returns:
            Threshold as fraction and percentage.
        """
        return f"p_c = {sd['threshold']} ({sd['percentage']}%)"


@register
class LifeTableGenerator(EpidemiologyBase):
    """Compute life expectancy from a simplified life table.

    Generates a 3-5 age group abridged life table with l_x values
    (survivors at age x), computes person-years lived L_x = (l_x +
    l_{x+1}) / 2, and derives life expectancy e_x = sum(L_x) / l_x
    for the first age group.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "life_table"

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
            Short task description string.
        """
        return "compute life expectancy from a life table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a life table problem.

        Creates a declining sequence of l_x values representing
        survivors at each age group boundary, computes L_x for
        each interval, and derives life expectancy at the first
        age group.

        Args:
            difficulty: Controls number of age groups.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_groups = self._rng.randint(3, min(5, 2 + difficulty))
        interval = self._rng.choice([5, 10])

        # Generate declining l_x values (survivors)
        l_x = [1000]
        for _ in range(num_groups):
            mortality = self._rng.uniform(0.05, 0.25)
            survivors = max(0, round(l_x[-1] * (1 - mortality)))
            l_x.append(survivors)

        # Compute L_x for each interval
        big_l_x = []
        for idx in range(num_groups):
            val = round((l_x[idx] + l_x[idx + 1]) / 2, 4)
            big_l_x.append(val)

        sum_l = round(sum(big_l_x), 4)
        e_0 = round(sum_l / l_x[0], 4)

        # Build age group labels
        ages = [idx * interval for idx in range(num_groups + 1)]
        age_labels = [
            f"{ages[idx]}-{ages[idx + 1]}" for idx in range(num_groups)
        ]

        lx_str = ", ".join(
            f"l_{ages[idx]}={l_x[idx]}" for idx in range(num_groups + 1)
        )
        desc = f"life table ({interval}-yr intervals): {lx_str}"

        return desc, {
            "l_x": l_x, "big_l_x": big_l_x,
            "sum_l": sum_l, "e_0": e_0,
            "ages": ages, "age_labels": age_labels,
            "interval": interval, "num_groups": num_groups,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["L_x = (l_x + l_{x+1}) / 2"]
        for idx in range(sd["num_groups"]):
            steps.append(
                f"L_{sd['age_labels'][idx]} = "
                f"({sd['l_x'][idx]} + {sd['l_x'][idx + 1]}) / 2 = "
                f"{sd['big_l_x'][idx]}"
            )
        steps.append(f"sum(L_x) = {sd['sum_l']}")
        steps.append(f"e_0 = {sd['sum_l']} / {sd['l_x'][0]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the life expectancy at the first age group.

        Args:
            sd: Solution data.

        Returns:
            Life expectancy value as a string.
        """
        return f"e_0 = {sd['e_0']}"
