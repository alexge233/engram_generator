"""Extended ecology generators -- competition, functional response, biogeography.

8 generators across tiers 4-5 deepening population and community ecology.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class EcologyExtBase(StepGenerator):
    """Base class for extended ecology generators.

    Provides shared ecological constants and helper methods for
    competition models, functional responses, and diversity indices.
    """

    pass


@register
class CompetitionModelGenerator(EcologyExtBase):
    """Compute Lotka-Volterra competition dynamics and predict outcomes.

    Applies dN1/dt = r1*N1*(K1 - N1 - alpha12*N2)/K1 to compute
    growth rate and uses competition coefficients to predict
    coexistence versus competitive exclusion.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "competition_model"

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
        return "compute Lotka-Volterra competition growth rate and predict outcome"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lotka-Volterra competition problem.

        Creates two competing species with growth rates, carrying
        capacities, and competition coefficients. Computes dN1/dt and
        predicts coexistence vs exclusion from alpha values.

        Args:
            difficulty: Controls parameter range and complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r1 = round(self._rng.uniform(0.1, 0.3 * difficulty), 4)
        n1 = self._rng.randint(10, 50 * max(1, difficulty))
        k1 = self._rng.randint(max(n1 + 20, 100), 500 * max(1, difficulty))
        n2 = self._rng.randint(10, 50 * max(1, difficulty))
        k2 = self._rng.randint(max(n2 + 20, 100), 500 * max(1, difficulty))
        alpha12 = round(self._rng.uniform(0.2, 1.8), 4)
        alpha21 = round(self._rng.uniform(0.2, 1.8), 4)

        effective = round(n1 + alpha12 * n2, 4)
        bracket = round(k1 - effective, 4)
        dn1_dt = round(r1 * n1 * bracket / k1, 4)

        # Coexistence condition: alpha12 < K1/K2 AND alpha21 < K2/K1
        ratio_12 = round(k1 / k2, 4)
        ratio_21 = round(k2 / k1, 4)
        coexist = alpha12 < ratio_12 and alpha21 < ratio_21

        if coexist:
            outcome = "coexistence"
        elif alpha12 >= ratio_12 and alpha21 >= ratio_21:
            outcome = "unstable (winner depends on initial conditions)"
        elif alpha12 >= ratio_12:
            outcome = "species 2 excludes species 1"
        else:
            outcome = "species 1 excludes species 2"

        desc = (
            f"r1={r1}, N1={n1}, K1={k1}, N2={n2}, K2={k2}, "
            f"a12={alpha12}, a21={alpha21}"
        )
        return desc, {
            "r1": r1, "n1": n1, "k1": k1, "n2": n2, "k2": k2,
            "alpha12": alpha12, "alpha21": alpha21,
            "effective": effective, "bracket": bracket,
            "dn1_dt": dn1_dt, "ratio_12": ratio_12,
            "ratio_21": ratio_21, "outcome": outcome,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "dN1/dt = r1*N1*(K1 - N1 - a12*N2)/K1",
            f"N1 + a12*N2 = {sd['n1']} + {sd['alpha12']}*{sd['n2']} = {sd['effective']}",
            f"K1 - effective = {sd['k1']} - {sd['effective']} = {sd['bracket']}",
            f"dN1/dt = {sd['r1']}*{sd['n1']}*{sd['bracket']}/{sd['k1']} = {sd['dn1_dt']}",
            f"K1/K2 = {sd['ratio_12']}, K2/K1 = {sd['ratio_21']}",
            f"a12={sd['alpha12']} vs K1/K2={sd['ratio_12']}, a21={sd['alpha21']} vs K2/K1={sd['ratio_21']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the growth rate and predicted outcome.

        Args:
            sd: Solution data.

        Returns:
            Growth rate and outcome string.
        """
        return f"dN1/dt = {sd['dn1_dt']}, {sd['outcome']}"


@register
class PredatorFunctionalResponseGenerator(EcologyExtBase):
    """Compute predator functional response (Type I, II, or III).

    Type I: f = a*N. Type II: f = a*N/(1 + a*h*N).
    Type III: f = a*N^2/(1 + a*h*N^2). Computes per-capita
    intake rate for a given prey density.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "predator_functional_response"

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
        return "compute predator functional response intake rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a functional response problem.

        Randomly selects Type I, II, or III response and computes
        the intake rate from prey density and predator parameters.

        Args:
            difficulty: Controls prey density range and type selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            resp_type = self._rng.choice([1, 2])
        else:
            resp_type = self._rng.choice([1, 2, 3])

        a = round(self._rng.uniform(0.01, 0.1), 4)
        n = self._rng.randint(5, 50 * max(1, difficulty))
        h = round(self._rng.uniform(0.01, 0.2), 4)

        if resp_type == 1:
            f_val = round(a * n, 4)
            formula = f"f = a*N = {a}*{n}"
            denom_val = None
        elif resp_type == 2:
            denom_val = round(1 + a * h * n, 4)
            numer = round(a * n, 4)
            f_val = round(numer / denom_val, 4)
            formula = f"f = a*N/(1+a*h*N) = {numer}/{denom_val}"
        else:
            n_sq = n * n
            numer = round(a * n_sq, 4)
            denom_val = round(1 + a * h * n_sq, 4)
            f_val = round(numer / denom_val, 4)
            formula = f"f = a*N^2/(1+a*h*N^2) = {numer}/{denom_val}"

        desc = f"Type {resp_type}: a={a}, N={n}, h={h}; find intake rate"
        return desc, {
            "resp_type": resp_type, "a": a, "n": n, "h": h,
            "f_val": f_val, "formula": formula,
            "denom_val": denom_val,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"Type {sd['resp_type']} functional response"]
        if sd["resp_type"] == 1:
            steps.append(f"f = a*N = {sd['a']}*{sd['n']}")
        elif sd["resp_type"] == 2:
            steps.append(f"denominator = 1 + {sd['a']}*{sd['h']}*{sd['n']} = {sd['denom_val']}")
            steps.append(sd["formula"])
        else:
            n_sq = sd["n"] * sd["n"]
            steps.append(f"N^2 = {n_sq}")
            steps.append(f"denominator = 1 + {sd['a']}*{sd['h']}*{n_sq} = {sd['denom_val']}")
            steps.append(sd["formula"])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the intake rate.

        Args:
            sd: Solution data.

        Returns:
            Intake rate as a string.
        """
        return f"f = {sd['f_val']} prey/predator/time"


@register
class IslandBiogeographyGenerator(EcologyExtBase):
    """Compute equilibrium species richness from island biogeography.

    Immigration I(S) = I_max*(1 - S/P) and extinction E(S) = E_max*S/P.
    At equilibrium I(S) = E(S), solving for S_eq = I_max*P/(I_max + E_max).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "island_biogeography"

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
        return "compute equilibrium species richness (island biogeography)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an island biogeography equilibrium problem.

        Creates mainland species pool P, maximum immigration and
        extinction rates, then solves for equilibrium species count.

        Args:
            difficulty: Controls species pool size and rate values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p = self._rng.randint(20, 50 * max(1, difficulty))
        i_max = round(self._rng.uniform(1.0, 5.0 * max(1, difficulty)), 4)
        e_max = round(self._rng.uniform(0.5, 4.0 * max(1, difficulty)), 4)

        s_eq = round(i_max * p / (i_max + e_max), 4)
        turnover = round(i_max * e_max / (i_max + e_max), 4)

        desc = f"P={p}, I_max={i_max}, E_max={e_max}; find S_eq"
        return desc, {
            "p": p, "i_max": i_max, "e_max": e_max,
            "s_eq": s_eq, "turnover": turnover,
            "denom": round(i_max + e_max, 4),
            "numer": round(i_max * p, 4),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "set I(S) = E(S): I_max*(1-S/P) = E_max*S/P",
            f"S_eq = I_max*P / (I_max + E_max)",
            f"numerator = {sd['i_max']}*{sd['p']} = {sd['numer']}",
            f"denominator = {sd['i_max']} + {sd['e_max']} = {sd['denom']}",
            f"S_eq = {sd['numer']} / {sd['denom']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium species count.

        Args:
            sd: Solution data.

        Returns:
            S_eq as a string.
        """
        return f"S_eq = {sd['s_eq']} species"


@register
class LifeHistoryTableGenerator(EcologyExtBase):
    """Compute net reproductive rate and generation time from a life table.

    R_0 = sum(l_x * m_x) gives the net reproductive rate.
    T = sum(x * l_x * m_x) / R_0 gives the mean generation time.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "life_history_table"

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
        return "compute R_0 and generation time from life table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a life history table problem.

        Creates age-specific survivorship l_x and fecundity m_x
        values, then computes R_0 and generation time T.

        Args:
            difficulty: Controls number of age classes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_ages = min(3 + difficulty // 2, 6)
        ages = list(range(n_ages))

        # Survivorship decreases with age
        lx_values = [1.0]
        for i in range(1, n_ages):
            surv = round(lx_values[-1] * self._rng.uniform(0.4, 0.9), 4)
            lx_values.append(surv)

        # Fecundity: zero for young, peaks mid-life
        mx_values = [0.0]
        for i in range(1, n_ages):
            mx = round(self._rng.uniform(0.0, 2.0 * max(1, difficulty)), 4)
            mx_values.append(mx)

        lx_mx = [round(lx * mx, 4) for lx, mx in zip(lx_values, mx_values)]
        r0 = round(sum(lx_mx), 4)

        x_lx_mx = [round(x * lm, 4) for x, lm in zip(ages, lx_mx)]
        sum_x_lx_mx = round(sum(x_lx_mx), 4)
        gen_time = round(sum_x_lx_mx / r0, 4) if r0 > 0 else 0.0

        table_str = "; ".join(
            f"x={x},l_x={lx},m_x={mx}"
            for x, lx, mx in zip(ages, lx_values, mx_values)
        )
        desc = f"life table: {table_str}; find R_0 and T"

        return desc, {
            "ages": ages, "lx": lx_values, "mx": mx_values,
            "lx_mx": lx_mx, "r0": r0,
            "x_lx_mx": x_lx_mx, "sum_x_lx_mx": sum_x_lx_mx,
            "gen_time": gen_time,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["R_0 = sum(l_x * m_x)"]
        for x, lm in zip(sd["ages"], sd["lx_mx"]):
            steps.append(f"x={x}: l_x*m_x = {lm}")
        steps.append(f"R_0 = {sd['r0']}")
        steps.append(f"T = sum(x*l_x*m_x)/R_0 = {sd['sum_x_lx_mx']}/{sd['r0']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return R_0 and generation time.

        Args:
            sd: Solution data.

        Returns:
            R_0 and T as a string.
        """
        return f"R_0 = {sd['r0']}, T = {sd['gen_time']}"


@register
class SuccessionModelGenerator(EcologyExtBase):
    """Compute ecological succession state after n steps using a Markov model.

    Given a transition matrix between states (bare, grass, shrub, forest),
    applies matrix-vector multiplication n times to predict the probability
    distribution over states.
    """

    STATES = ["bare", "grass", "shrub", "forest"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "succession_model"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "predict ecological succession state after n steps"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a succession Markov model problem.

        Creates a simplified transition matrix for ecological
        succession and computes state probabilities after n steps.

        Args:
            difficulty: Controls number of steps.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Simplified 4x4 transition matrix (rows = from, cols = to)
        # Each row sums to 1.0; succession tends forward
        matrix = [
            [0.3, 0.5, 0.15, 0.05],  # bare
            [0.05, 0.4, 0.4, 0.15],  # grass
            [0.0, 0.05, 0.5, 0.45],  # shrub
            [0.0, 0.0, 0.1, 0.9],    # forest
        ]

        # Start state: bare ground
        start_idx = 0
        state = [0.0, 0.0, 0.0, 0.0]
        state[start_idx] = 1.0

        n_steps = self._rng.randint(1, min(2 + difficulty, 5))

        history = [list(state)]
        for _ in range(n_steps):
            new_state = [0.0] * 4
            for j in range(4):
                for i in range(4):
                    new_state[j] += state[i] * matrix[i][j]
            state = [round(s, 4) for s in new_state]
            history.append(list(state))

        dominant = self.STATES[state.index(max(state))]

        desc = (
            f"start: {self.STATES[start_idx]}; "
            f"{n_steps} succession step(s); find state distribution"
        )
        return desc, {
            "start": self.STATES[start_idx], "n_steps": n_steps,
            "final_state": state, "dominant": dominant,
            "history": history,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"initial state: {sd['start']} (probability 1.0)"]
        for i, h in enumerate(sd["history"][1:], 1):
            state_str = ", ".join(
                f"{s}={p}" for s, p in zip(self.STATES, h)
            )
            steps.append(f"step {i}: {state_str}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final state distribution and dominant state.

        Args:
            sd: Solution data.

        Returns:
            State probabilities and dominant state.
        """
        dist = ", ".join(
            f"{s}={p}" for s, p in zip(self.STATES, sd["final_state"])
        )
        return f"{dist}; dominant = {sd['dominant']}"


@register
class MetapopulationGenerator(EcologyExtBase):
    """Compute Levins metapopulation equilibrium.

    Uses dp/dt = c*p*(1-p) - e*p where p is the fraction of occupied
    patches, c is the colonisation rate, and e is the extinction rate.
    Equilibrium: p* = 1 - e/c (when c > e).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "metapopulation"

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
        return "compute Levins metapopulation equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Levins metapopulation problem.

        Creates colonisation and extinction rates, computes the current
        rate of change dp/dt for a given occupancy p, and the equilibrium
        occupancy p*.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = round(self._rng.uniform(0.2, 0.5 * max(1, difficulty)), 4)
        e_upper = min(c - 0.01, 0.3 * max(1, difficulty))
        e = round(self._rng.uniform(0.05, max(0.06, e_upper)), 4)
        p = round(self._rng.uniform(0.1, 0.9), 4)

        colonisation = round(c * p * (1 - p), 4)
        extinction = round(e * p, 4)
        dp_dt = round(colonisation - extinction, 4)
        p_star = round(1 - e / c, 4)

        desc = f"c={c}, e={e}, p={p}; find dp/dt and p*"
        return desc, {
            "c": c, "e": e, "p": p,
            "colonisation": colonisation, "extinction": extinction,
            "dp_dt": dp_dt, "p_star": p_star,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "dp/dt = c*p*(1-p) - e*p",
            f"colonisation = {sd['c']}*{sd['p']}*(1-{sd['p']}) = {sd['colonisation']}",
            f"extinction = {sd['e']}*{sd['p']} = {sd['extinction']}",
            f"dp/dt = {sd['colonisation']} - {sd['extinction']} = {sd['dp_dt']}",
            f"p* = 1 - e/c = 1 - {sd['e']}/{sd['c']} = {sd['p_star']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return dp/dt and equilibrium p*.

        Args:
            sd: Solution data.

        Returns:
            Rate and equilibrium as a string.
        """
        return f"dp/dt = {sd['dp_dt']}, p* = {sd['p_star']}"


@register
class NutrientCyclingGenerator(EcologyExtBase):
    """Compute steady-state nutrient pool from a compartment model.

    Models soil nitrogen: dN_soil/dt = decomposition - uptake.
    At steady state, decomposition = uptake. Given flux rates and
    pool sizes, computes the steady-state nutrient concentration.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nutrient_cycling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute steady-state nutrient pool from compartment model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nutrient cycling compartment model problem.

        Creates decomposition rate, uptake rate, and current pool size.
        Computes dN/dt and the steady-state pool size where fluxes
        balance.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Rates are per unit time; pool-dependent fluxes
        decomp_rate = round(self._rng.uniform(0.5, 5.0 * max(1, difficulty)), 4)
        uptake_rate = round(self._rng.uniform(0.3, 4.0 * max(1, difficulty)), 4)
        litter_input = round(self._rng.uniform(1.0, 10.0 * max(1, difficulty)), 4)
        n_soil = round(self._rng.uniform(5.0, 50.0 * max(1, difficulty)), 4)

        # dN/dt = litter_input + decomp_rate - uptake_rate * N_soil / scaling
        # Simplified: decomp = litter_input (constant), uptake = uptake_rate
        decomp_flux = litter_input
        uptake_flux = uptake_rate
        dn_dt = round(decomp_flux - uptake_flux, 4)

        # Steady state: decomp = uptake => N_ss = litter_input / k_uptake
        k_uptake = round(self._rng.uniform(0.01, 0.1), 4)
        n_ss = round(litter_input / k_uptake, 4)
        current_dn = round(litter_input - k_uptake * n_soil, 4)

        desc = (
            f"litter input={litter_input} g/m2/yr, "
            f"k_uptake={k_uptake} /yr, N_soil={n_soil} g/m2; "
            f"find dN/dt and N_ss"
        )
        return desc, {
            "litter_input": litter_input, "k_uptake": k_uptake,
            "n_soil": n_soil, "current_dn": current_dn, "n_ss": n_ss,
            "uptake_current": round(k_uptake * n_soil, 4),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "dN/dt = litter_input - k_uptake * N_soil",
            f"uptake = {sd['k_uptake']} * {sd['n_soil']} = {sd['uptake_current']}",
            f"dN/dt = {sd['litter_input']} - {sd['uptake_current']} = {sd['current_dn']}",
            f"steady state: N_ss = litter_input / k_uptake",
            f"N_ss = {sd['litter_input']} / {sd['k_uptake']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return dN/dt and steady-state pool size.

        Args:
            sd: Solution data.

        Returns:
            Current rate and equilibrium pool.
        """
        return f"dN/dt = {sd['current_dn']} g/m2/yr, N_ss = {sd['n_ss']} g/m2"


@register
class BiodiversityIndexGenerator(EcologyExtBase):
    """Compute Simpson's diversity index and compare two communities.

    Simpson's D = sum(p_i^2). Diversity = 1 - D. Given species
    abundances for two communities, computes both indices and
    identifies the more diverse community.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "biodiversity_index"

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
        return "compute Simpson's diversity index and compare communities"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a biodiversity index comparison problem.

        Creates two communities with species abundance counts,
        computes Simpson's D and 1-D for each, and identifies the
        more diverse community.

        Args:
            difficulty: Controls number of species.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_species = self._rng.randint(3, min(5, 2 + difficulty))

        def _compute_simpson(counts: list[int]) -> tuple[list[float], float, float]:
            """Compute proportions and Simpson's D from counts."""
            total = sum(counts)
            props = [round(c / total, 4) for c in counts]
            d_val = round(sum(p * p for p in props), 4)
            diversity = round(1 - d_val, 4)
            return props, d_val, diversity

        counts_a = [
            self._rng.randint(1, 20 * max(1, difficulty))
            for _ in range(n_species)
        ]
        counts_b = [
            self._rng.randint(1, 20 * max(1, difficulty))
            for _ in range(n_species)
        ]

        props_a, d_a, div_a = _compute_simpson(counts_a)
        props_b, d_b, div_b = _compute_simpson(counts_b)

        if div_a > div_b:
            more_diverse = "community A"
        elif div_b > div_a:
            more_diverse = "community B"
        else:
            more_diverse = "equal diversity"

        desc = (
            f"A: {counts_a}; B: {counts_b}; "
            f"compare Simpson's diversity"
        )
        return desc, {
            "counts_a": counts_a, "counts_b": counts_b,
            "props_a": props_a, "props_b": props_b,
            "d_a": d_a, "d_b": d_b,
            "div_a": div_a, "div_b": div_b,
            "total_a": sum(counts_a), "total_b": sum(counts_b),
            "more_diverse": more_diverse,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"A total = {sd['total_a']}, proportions = {sd['props_a']}",
            f"D_A = sum(p_i^2) = {sd['d_a']}",
            f"diversity_A = 1 - {sd['d_a']} = {sd['div_a']}",
            f"B total = {sd['total_b']}, proportions = {sd['props_b']}",
            f"D_B = sum(p_i^2) = {sd['d_b']}",
            f"diversity_B = 1 - {sd['d_b']} = {sd['div_b']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return both diversity values and the comparison result.

        Args:
            sd: Solution data.

        Returns:
            Diversity values and which community is more diverse.
        """
        return (
            f"1-D_A = {sd['div_a']}, 1-D_B = {sd['div_b']}; "
            f"{sd['more_diverse']} is more diverse"
        )
