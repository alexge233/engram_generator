"""Extended physical chemistry generators -- kinetics, quantum, electrochemistry.

10 generators across tiers 5-6 covering half-lives, integrated rate laws,
transition state theory, ICE tables, colligative properties, mechanisms,
phase equilibria, electrochemistry cells, quantum orbitals, and partition
functions.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PhysicalChemistryExtBase(StepGenerator):
    """Base class for extended physical chemistry generators.

    Provides universal constants shared across multiple generators.

    Attributes:
        R: Universal gas constant in J/(mol*K).
        F: Faraday constant in C/mol.
        k_B: Boltzmann constant in J/K.
        h: Planck constant in J*s.
    """

    R = 8.314       # J/(mol*K)
    F = 96485       # C/mol
    k_B = 1.3806e-23  # J/K
    h = 6.626e-34     # J*s


# ---------------------------------------------------------------------------
# 1. Reaction Half-Life (tier 5)
# ---------------------------------------------------------------------------

@register
class ReactionHalfLifeGenerator(PhysicalChemistryExtBase):
    """Compute half-life for zero, first, or second order reactions.

    Zero order: t_1/2 = [A]_0 / (2k).
    First order: t_1/2 = ln(2) / k.
    Second order: t_1/2 = 1 / (k * [A]_0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reaction_half_life"

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
        return "compute reaction half-life"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a half-life calculation problem.

        Randomly selects reaction order (0, 1, or 2) and generates
        appropriate parameters for the half-life formula.

        Args:
            difficulty: Controls parameter range and order availability.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        orders = [0, 1, 2] if difficulty >= 3 else [0, 1]
        order = self._rng.choice(orders)
        k = round(self._rng.uniform(0.001, 0.5), 4)
        a0 = round(self._rng.uniform(0.1, 5.0), 4)

        if order == 0:
            half_life = round(a0 / (2 * k), 4)
            formula = "t_1/2 = [A]_0 / (2k)"
            calc = f"{a0} / (2 * {k})"
        elif order == 1:
            half_life = round(math.log(2) / k, 4)
            formula = "t_1/2 = ln(2) / k"
            calc = f"ln(2) / {k}"
        else:
            half_life = round(1.0 / (k * a0), 4)
            formula = "t_1/2 = 1 / (k * [A]_0)"
            calc = f"1 / ({k} * {a0})"

        return (
            f"order {order}, k={k}, [A]_0={a0} M. Find t_1/2.",
            {"order": order, "k": k, "a0": a0,
             "half_life": half_life, "formula": formula, "calc": calc},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"reaction order: {sd['order']}",
            sd["formula"],
            f"t_1/2 = {sd['calc']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Half-life as string with units.
        """
        return f"{sd['half_life']} s"


# ---------------------------------------------------------------------------
# 2. Integrated Rate Law (tier 5)
# ---------------------------------------------------------------------------

@register
class IntegratedRateLawGenerator(PhysicalChemistryExtBase):
    """Compute concentration at time t using integrated rate laws.

    Zero order: [A] = [A]_0 - k*t.
    First order: ln[A] = ln[A]_0 - k*t.
    Second order: 1/[A] = 1/[A]_0 + k*t.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integrated_rate_law"

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
        return "compute concentration via integrated rate law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integrated rate law problem.

        Selects a reaction order and computes the concentration at a
        given time from initial concentration and rate constant.

        Args:
            difficulty: Controls order availability and time range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        orders = [0, 1, 2] if difficulty >= 3 else [0, 1]
        order = self._rng.choice(orders)
        k = round(self._rng.uniform(0.001, 0.1), 4)
        a0 = round(self._rng.uniform(0.5, 5.0), 4)
        t = self._rng.randint(1, 10 * max(difficulty, 1))

        if order == 0:
            conc = round(a0 - k * t, 4)
            conc = max(conc, 0.0)
            formula = "[A] = [A]_0 - k*t"
            calc = f"{a0} - {k}*{t}"
        elif order == 1:
            ln_a = math.log(a0) - k * t
            conc = round(math.exp(ln_a), 4)
            formula = "ln[A] = ln[A]_0 - k*t"
            calc = f"exp(ln({a0}) - {k}*{t})"
        else:
            inv_a = 1.0 / a0 + k * t
            conc = round(1.0 / inv_a, 4)
            formula = "1/[A] = 1/[A]_0 + k*t"
            calc = f"1/(1/{a0} + {k}*{t})"

        return (
            f"order {order}, k={k}, [A]_0={a0} M, t={t} s. Find [A].",
            {"order": order, "k": k, "a0": a0, "t": t,
             "conc": conc, "formula": formula, "calc": calc},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"reaction order: {sd['order']}",
            sd["formula"],
            f"[A] = {sd['calc']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Concentration as string with units.
        """
        return f"{sd['conc']} M"


# ---------------------------------------------------------------------------
# 3. Transition State Theory / Eyring Equation (tier 6)
# ---------------------------------------------------------------------------

@register
class TransitionStateGenerator(PhysicalChemistryExtBase):
    """Compute rate constant using the Eyring equation.

    k = (k_B * T / h) * exp(-dG_dagger / RT) where
    dG_dagger = dH_dagger - T * dS_dagger.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transition_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arrhenius"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute rate constant via Eyring equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transition state theory problem.

        Generates activation enthalpy and entropy, computes dG_dagger,
        and applies the Eyring equation to find k.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dh_dagger = round(
            self._rng.uniform(30, min(120, 30 + 12 * difficulty)) * 1000, 1,
        )
        ds_dagger = round(self._rng.uniform(-50, 50), 2)
        temp = self._rng.randint(273, 500)

        dg_dagger = dh_dagger - temp * ds_dagger
        dg_dagger = round(dg_dagger, 4)

        prefactor = self.k_B * temp / self.h
        k_val = prefactor * math.exp(-dg_dagger / (self.R * temp))
        k_val = round(k_val, 4)

        dh_kj = round(dh_dagger / 1000, 2)

        return (
            f"dH_dagger={dh_kj} kJ/mol, dS_dagger={ds_dagger} J/(mol*K), "
            f"T={temp} K. Find k (Eyring).",
            {"dh_dagger": dh_dagger, "dh_kj": dh_kj,
             "ds_dagger": ds_dagger, "temp": temp,
             "dg_dagger": dg_dagger, "k_val": k_val},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"dG_dagger = dH_dagger - T*dS_dagger = "
            f"{sd['dh_dagger']} - {sd['temp']}*{sd['ds_dagger']}",
            f"dG_dagger = {sd['dg_dagger']} J/mol",
            "k = (k_B*T/h)*exp(-dG_dagger/RT)",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Rate constant as string.
        """
        return f"{sd['k_val']:.4e} s^-1"


# ---------------------------------------------------------------------------
# 4. Equilibrium ICE Table (tier 5)
# ---------------------------------------------------------------------------

@register
class EquilibriumIceTableGenerator(PhysicalChemistryExtBase):
    """Solve for equilibrium concentrations using an ICE table.

    For A <-> B + C with known K and initial [A], sets up the ICE
    table and solves K = x^2 / ([A]_0 - x) for x.
    """

    REACTIONS = [
        {"equation": "HA <-> H+ + A-", "label": "weak acid"},
        {"equation": "NH3 + H2O <-> NH4+ + OH-", "label": "weak base"},
        {"equation": "AB <-> A + B", "label": "dissociation"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "equilibrium_ice_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["equilibrium_constant"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "solve equilibrium via ICE table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ICE table equilibrium problem.

        Sets up a simple 1:1:1 dissociation and solves the quadratic
        to find equilibrium concentrations.

        Args:
            difficulty: Controls initial concentration and K range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        rxn = self._rng.choice(self.REACTIONS)
        c0 = round(self._rng.uniform(0.05, 2.0), 4)
        k_eq = round(self._rng.uniform(1e-6, 0.01), 6)

        # Solve K = x^2/(c0 - x) via quadratic: x^2 + K*x - K*c0 = 0
        a_coeff = 1.0
        b_coeff = k_eq
        c_coeff = -k_eq * c0
        discriminant = b_coeff ** 2 - 4 * a_coeff * c_coeff
        x = (-b_coeff + math.sqrt(discriminant)) / (2 * a_coeff)
        x = round(x, 4)
        eq_a = round(c0 - x, 4)

        return (
            f"{rxn['equation']}, K={k_eq}, [A]_0={c0} M. "
            f"Find equilibrium [A] and [products].",
            {"rxn": rxn, "c0": c0, "k_eq": k_eq,
             "x": x, "eq_a": eq_a},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"I: [A]={sd['c0']}, [products]=0",
            "C: -x, +x, +x",
            f"E: [A]={sd['c0']}-x, [products]=x",
            f"K = x^2/({sd['c0']}-x) = {sd['k_eq']}",
            f"x = {sd['x']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Equilibrium concentrations.
        """
        return f"[A]={sd['eq_a']} M, [products]={sd['x']} M"


# ---------------------------------------------------------------------------
# 5. Colligative Properties (tier 5)
# ---------------------------------------------------------------------------

@register
class ColligativePropertiesGenerator(PhysicalChemistryExtBase):
    """Compute colligative property changes for solutions.

    Boiling point elevation: dT_b = i * K_b * m.
    Freezing point depression: dT_f = i * K_f * m.
    Osmotic pressure: pi = i * M * R * T.
    """

    SOLVENTS = [
        {"name": "water", "K_b": 0.512, "K_f": 1.86,
         "bp": 100.0, "fp": 0.0},
        {"name": "benzene", "K_b": 2.53, "K_f": 5.12,
         "bp": 80.1, "fp": 5.5},
        {"name": "acetic acid", "K_b": 3.07, "K_f": 3.90,
         "bp": 118.1, "fp": 16.6},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "colligative_properties"

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
        return "compute colligative property change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a colligative properties problem.

        Randomly selects boiling point elevation, freezing point
        depression, or osmotic pressure calculation.

        Args:
            difficulty: Controls solute complexity and property type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        solvent = self._rng.choice(self.SOLVENTS)
        i = self._rng.choice([1, 2, 3]) if difficulty >= 3 else 1
        m = round(self._rng.uniform(0.1, 3.0), 4)

        modes = ["bp_elevation", "fp_depression"]
        if difficulty >= 4:
            modes.append("osmotic_pressure")
        mode = self._rng.choice(modes)

        if mode == "bp_elevation":
            dt = round(i * solvent["K_b"] * m, 4)
            new_bp = round(solvent["bp"] + dt, 4)
            formula = "dT_b = i*K_b*m"
            calc = f"{i}*{solvent['K_b']}*{m}"
            answer_val = f"dT_b={dt} C, bp={new_bp} C"
        elif mode == "fp_depression":
            dt = round(i * solvent["K_f"] * m, 4)
            new_fp = round(solvent["fp"] - dt, 4)
            formula = "dT_f = i*K_f*m"
            calc = f"{i}*{solvent['K_f']}*{m}"
            answer_val = f"dT_f={dt} C, fp={new_fp} C"
        else:
            temp = self._rng.randint(273, 373)
            molarity = m
            pi_val = round(i * molarity * 0.08206 * temp, 4)
            formula = "pi = i*M*R*T"
            calc = f"{i}*{molarity}*0.08206*{temp}"
            answer_val = f"pi={pi_val} atm"

        return (
            f"solvent={solvent['name']}, i={i}, m={m} mol/kg. "
            f"Find {mode.replace('_', ' ')}.",
            {"solvent": solvent, "i": i, "m": m, "mode": mode,
             "formula": formula, "calc": calc, "answer_val": answer_val},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            sd["formula"],
            f"= {sd['calc']}",
            f"solvent: {sd['solvent']['name']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Colligative property result.
        """
        return sd["answer_val"]


# ---------------------------------------------------------------------------
# 6. Chemical Kinetics Mechanism (tier 6)
# ---------------------------------------------------------------------------

@register
class ChemicalKineticsMechanismGenerator(PhysicalChemistryExtBase):
    """Derive rate law from a 2-step mechanism using steady-state approximation.

    For a mechanism with a fast pre-equilibrium step forming an
    intermediate, applies d[intermediate]/dt = 0 to derive the
    overall rate law.
    """

    MECHANISMS = [
        {
            "step1": "A + B <-> I (fast, k1/k-1)",
            "step2": "I -> P (slow, k2)",
            "intermediate": "I",
            "rate_law": "rate = (k1*k2/k_-1)*[A][B]",
            "overall_order": 2,
        },
        {
            "step1": "A <-> I (fast, k1/k-1)",
            "step2": "I + B -> P (slow, k2)",
            "intermediate": "I",
            "rate_law": "rate = (k1*k2/k_-1)*[A][B]",
            "overall_order": 2,
        },
        {
            "step1": "2A <-> I (fast, k1/k-1)",
            "step2": "I -> P (slow, k2)",
            "intermediate": "I",
            "rate_law": "rate = (k1*k2/k_-1)*[A]^2",
            "overall_order": 2,
        },
        {
            "step1": "A <-> I (fast, k1/k-1)",
            "step2": "I + A -> P (slow, k2)",
            "intermediate": "I",
            "rate_law": "rate = (k1*k2/k_-1)*[A]^2",
            "overall_order": 2,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chemical_kinetics_mechanism"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["rate_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "derive rate law from mechanism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a kinetics mechanism problem.

        Selects a 2-step mechanism and asks for the overall rate law
        derived using the steady-state approximation.

        Args:
            difficulty: Controls mechanism pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.MECHANISMS), 2 + difficulty // 2)
        mech = self._rng.choice(self.MECHANISMS[:pool_size])

        return (
            f"Step 1: {mech['step1']}. Step 2: {mech['step2']}. "
            f"Derive overall rate law.",
            {"mech": mech},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        mech = sd["mech"]
        return [
            f"intermediate: {mech['intermediate']}",
            f"steady-state: d[{mech['intermediate']}]/dt = 0",
            f"solve for [{mech['intermediate']}] from step 1 equilibrium",
            f"substitute into rate of step 2",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Derived rate law string.
        """
        return sd["mech"]["rate_law"]


# ---------------------------------------------------------------------------
# 7. Phase Equilibria / Clausius-Clapeyron (tier 5)
# ---------------------------------------------------------------------------

@register
class PhaseEquilibriaGenerator(PhysicalChemistryExtBase):
    """Compute vapor pressure at a new temperature via Clausius-Clapeyron.

    Uses ln(P2/P1) = -dH_vap/R * (1/T2 - 1/T1) to find vapor
    pressure at T2 given P1 at T1.
    """

    SUBSTANCES = [
        {"name": "water", "dH_vap": 40700, "T1": 373, "P1": 101.325},
        {"name": "ethanol", "dH_vap": 38600, "T1": 351, "P1": 101.325},
        {"name": "acetone", "dH_vap": 31300, "T1": 329, "P1": 101.325},
        {"name": "diethyl ether", "dH_vap": 26520, "T1": 308, "P1": 101.325},
        {"name": "hexane", "dH_vap": 28850, "T1": 342, "P1": 101.325},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phase_equilibria"

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
        return "compute vapor pressure via Clausius-Clapeyron"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Clausius-Clapeyron problem.

        Given a substance with known boiling point and dH_vap, computes
        vapor pressure at a different temperature.

        Args:
            difficulty: Controls substance pool and temperature range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SUBSTANCES), 2 + difficulty)
        sub = self._rng.choice(self.SUBSTANCES[:pool_size])
        offset = self._rng.randint(-40, -5)
        t2 = sub["T1"] + offset

        exponent = -sub["dH_vap"] / self.R * (1.0 / t2 - 1.0 / sub["T1"])
        p2 = round(sub["P1"] * math.exp(exponent), 4)

        return (
            f"{sub['name']}: P1={sub['P1']} kPa at T1={sub['T1']} K, "
            f"dH_vap={sub['dH_vap']} J/mol. Find P at T2={t2} K.",
            {"sub": sub, "t2": t2, "exponent": round(exponent, 4),
             "p2": p2},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        sub = sd["sub"]
        return [
            "ln(P2/P1) = -dH_vap/R * (1/T2 - 1/T1)",
            f"= -{sub['dH_vap']}/8.314 * (1/{sd['t2']} - 1/{sub['T1']})",
            f"exponent = {sd['exponent']}",
            f"P2 = {sub['P1']} * exp({sd['exponent']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Vapor pressure as string with units.
        """
        return f"{sd['p2']} kPa"


# ---------------------------------------------------------------------------
# 8. Electrochemistry Cell Potential (tier 5)
# ---------------------------------------------------------------------------

@register
class ElectrochemistryCellGenerator(PhysicalChemistryExtBase):
    """Compute standard cell potential from half-reaction potentials.

    E_cell = E_cathode - E_anode. Identifies which half-reaction is
    the anode (more negative) and which is the cathode.
    """

    HALF_REACTIONS = [
        {"species": "Zn2+/Zn", "E0": -0.76},
        {"species": "Cu2+/Cu", "E0": 0.34},
        {"species": "Fe2+/Fe", "E0": -0.44},
        {"species": "Ag+/Ag", "E0": 0.80},
        {"species": "Ni2+/Ni", "E0": -0.26},
        {"species": "Pb2+/Pb", "E0": -0.13},
        {"species": "Sn2+/Sn", "E0": -0.14},
        {"species": "Al3+/Al", "E0": -1.66},
        {"species": "Mg2+/Mg", "E0": -2.37},
        {"species": "Cr3+/Cr", "E0": -0.74},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electrochemistry_cell"

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
        return "compute standard cell potential"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an electrochemistry cell problem.

        Picks two half-reactions, identifies anode and cathode, and
        computes the standard cell potential.

        Args:
            difficulty: Controls half-reaction pool size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.HALF_REACTIONS), 4 + difficulty)
        pair = self._rng.sample(self.HALF_REACTIONS[:pool_size], 2)

        if pair[0]["E0"] < pair[1]["E0"]:
            anode, cathode = pair[0], pair[1]
        else:
            anode, cathode = pair[1], pair[0]

        e_cell = round(cathode["E0"] - anode["E0"], 4)

        return (
            f"Half-reactions: {pair[0]['species']} (E0={pair[0]['E0']} V), "
            f"{pair[1]['species']} (E0={pair[1]['E0']} V). "
            f"Find E_cell and identify anode/cathode.",
            {"anode": anode, "cathode": cathode, "e_cell": e_cell},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"anode (oxidation): {sd['anode']['species']}, "
            f"E0={sd['anode']['E0']} V",
            f"cathode (reduction): {sd['cathode']['species']}, "
            f"E0={sd['cathode']['E0']} V",
            f"E_cell = {sd['cathode']['E0']} - ({sd['anode']['E0']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Cell potential and electrode identification.
        """
        return (
            f"E_cell={sd['e_cell']} V, "
            f"anode={sd['anode']['species']}, "
            f"cathode={sd['cathode']['species']}"
        )


# ---------------------------------------------------------------------------
# 9. Quantum Chemistry Orbitals (tier 5)
# ---------------------------------------------------------------------------

@register
class QuantumChemOrbitalGenerator(PhysicalChemistryExtBase):
    """Determine allowed quantum numbers and electron capacity for a shell.

    Given principal quantum number n, lists allowed values of l and
    m_l, and computes the maximum number of electrons = 2*n^2.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_chem_orbital"

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
        return "determine quantum numbers and electron capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantum numbers problem.

        Selects a principal quantum number and computes all allowed
        subshells and the total electron capacity.

        Args:
            difficulty: Controls which n values are available.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        max_n = min(4, 1 + difficulty)
        n = self._rng.randint(1, max_n)

        l_values = list(range(n))
        subshell_names = {0: "s", 1: "p", 2: "d", 3: "f"}
        subshells = [subshell_names[l] for l in l_values]
        ml_ranges = [list(range(-l, l + 1)) for l in l_values]
        max_electrons = 2 * n * n

        return (
            f"n={n}. List allowed l, m_l values and max electrons.",
            {"n": n, "l_values": l_values, "subshells": subshells,
             "ml_ranges": ml_ranges, "max_electrons": max_electrons},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [f"n={sd['n']}, l = 0 to {sd['n'] - 1}"]
        for l_val, sub, ml in zip(
            sd["l_values"], sd["subshells"], sd["ml_ranges"]
        ):
            steps.append(f"l={l_val} ({sub}): m_l={ml}")
        steps.append(f"max electrons = 2*{sd['n']}^2 = {sd['max_electrons']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Subshells and electron capacity.
        """
        subs = ", ".join(sd["subshells"])
        return f"subshells: {subs}, max electrons: {sd['max_electrons']}"


# ---------------------------------------------------------------------------
# 10. Partition Function (tier 6)
# ---------------------------------------------------------------------------

@register
class PartitionFunctionChemGenerator(PhysicalChemistryExtBase):
    """Compute molecular partition function and average energy.

    q = sum(g_i * exp(-E_i / kT)) for 2-3 discrete energy levels
    with given degeneracies g_i. Average energy
    <E> = sum(g_i * E_i * exp(-E_i / kT)) / q.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "partition_function_chem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute partition function and average energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a partition function problem.

        Creates 2-3 energy levels with degeneracies and computes the
        partition function and average energy at a given temperature.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_levels = 2 if difficulty <= 4 else 3
        temp = self._rng.randint(200, 1000)
        kt = self.k_B * temp

        energies = [0.0]
        degeneracies = [self._rng.randint(1, 3)]
        for _ in range(num_levels - 1):
            e = round(self._rng.uniform(0.5, 5.0) * kt, 4)
            energies.append(e)
            degeneracies.append(self._rng.randint(1, 5))

        q = 0.0
        e_avg_num = 0.0
        for g, e in zip(degeneracies, energies):
            boltz = g * math.exp(-e / kt)
            q += boltz
            e_avg_num += e * boltz

        q = round(q, 4)
        e_avg = round(e_avg_num / q, 4) if q > 0 else 0.0

        levels_str = "; ".join(
            f"E_{i}={e:.4e} J, g_{i}={g}"
            for i, (e, g) in enumerate(zip(energies, degeneracies))
        )

        return (
            f"T={temp} K. Levels: {levels_str}. Find q and <E>.",
            {"temp": temp, "energies": energies,
             "degeneracies": degeneracies, "q": q, "e_avg": e_avg},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["q = sum(g_i * exp(-E_i / kT))"]
        for i, (g, e) in enumerate(
            zip(sd["degeneracies"], sd["energies"])
        ):
            steps.append(f"level {i}: g={g}, E={e:.4e} J")
        steps.append(f"q = {sd['q']}")
        steps.append("<E> = sum(g_i*E_i*exp(-E_i/kT)) / q")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Partition function and average energy.
        """
        return f"q={sd['q']}, <E>={sd['e_avg']:.4e} J"
