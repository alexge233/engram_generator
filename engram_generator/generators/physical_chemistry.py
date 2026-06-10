"""Physical chemistry generators — kinetics, thermodynamics, electrochemistry, equilibrium.

8 generators across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PhysicalChemistryBase(StepGenerator):
    """Base class for physical chemistry generators with shared constants.

    Provides universal gas constant, Faraday constant, and common
    thermodynamic data tables used across multiple generators.

    Attributes:
        R: Universal gas constant in J/(mol*K).
        F: Faraday constant in C/mol.
    """

    R = 8.314   # J/(mol*K)
    F = 96485   # C/mol


@register
class RateLawGenerator(PhysicalChemistryBase):
    """Compute reaction rate from rate law expression.

    Given rate = k[A]^m[B]^n with specific concentrations and rate
    constant, calculates the reaction rate.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rate_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute reaction rate from rate law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rate law calculation problem.

        Creates a rate law with 1-3 reactants, random orders, and
        concentrations. The rate constant is scaled to produce
        reasonable rate values.

        Args:
            difficulty: Controls number of reactants and order range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_species = min(1 + difficulty // 3, 3)
        labels = ["A", "B", "C"][:num_species]
        max_order = min(1 + difficulty // 2, 3)
        orders = [self._rng.randint(1, max_order) for _ in labels]
        concentrations = [
            round(self._rng.uniform(0.01, 2.0), 3) for _ in labels
        ]
        k = round(self._rng.uniform(0.001, 1.0), 4)

        rate = k
        for conc, order in zip(concentrations, orders):
            rate *= conc ** order
        rate = round(rate, 4)

        terms = "".join(
            f"[{lbl}]^{o}" for lbl, o in zip(labels, orders)
        )
        conc_strs = ", ".join(
            f"[{lbl}]={c} M" for lbl, c in zip(labels, concentrations)
        )

        return (
            f"rate = {k} * {terms}, {conc_strs}. Find rate.",
            {"k": k, "labels": labels, "orders": orders,
             "concentrations": concentrations, "rate": rate, "terms": terms},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [f"rate = k * {sd['terms']}"]
        parts = [str(sd["k"])]
        for c, o in zip(sd["concentrations"], sd["orders"]):
            parts.append(f"{c}^{o}")
        steps.append(f"rate = {' * '.join(parts)}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Reaction rate as string.
        """
        return f"{sd['rate']} M/s"


@register
class ArrheniusGenerator(PhysicalChemistryBase):
    """Compute rate constant or temperature using the Arrhenius equation.

    Uses k = A * exp(-Ea / RT) where R = 8.314 J/(mol*K). Asks for
    either k given T, or T given k.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "arrhenius"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation", "logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "Arrhenius equation calculation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Arrhenius equation problem.

        Randomly chooses to solve for k or T. Uses realistic activation
        energies (40-120 kJ/mol) and pre-exponential factors.

        Args:
            difficulty: Controls activation energy range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ea = self._rng.randint(40, min(120, 40 + 10 * difficulty)) * 1000.0
        ea_kj = ea / 1000.0
        a_factor = round(self._rng.uniform(1e8, 1e12), 2)
        mode = self._rng.choice(["find_k", "find_T"])

        if mode == "find_k":
            temp = self._rng.randint(250, 600)
            k = round(a_factor * math.exp(-ea / (self.R * temp)), 4)
            return (
                f"Ea={ea_kj} kJ/mol, A={a_factor:.2e}, T={temp} K. Find k.",
                {"ea": ea, "a": a_factor, "temp": temp, "k": k, "mode": mode},
            )
        else:
            temp = self._rng.randint(250, 600)
            k = a_factor * math.exp(-ea / (self.R * temp))
            solved_t = round(-ea / (self.R * math.log(k / a_factor)), 4)
            return (
                f"Ea={ea_kj} kJ/mol, A={a_factor:.2e}, k={k:.4e}. Find T.",
                {"ea": ea, "a": a_factor, "k": k, "temp": solved_t, "mode": mode},
            )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "find_k":
            return [
                "k = A * exp(-Ea / RT)",
                f"k = {sd['a']:.2e} * exp(-{sd['ea']:.0f} / (8.314 * {sd['temp']}))",
            ]
        return [
            "T = -Ea / (R * ln(k/A))",
            f"T = -{sd['ea']:.0f} / (8.314 * ln({sd['k']:.4e}/{sd['a']:.2e}))",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Rate constant or temperature string.
        """
        if sd["mode"] == "find_k":
            return f"{sd['k']:.4e}"
        return f"{sd['temp']} K"


@register
class EquilibriumConstantGenerator(PhysicalChemistryBase):
    """Compute equilibrium constant K from concentrations.

    Uses K = [products]^coefficients / [reactants]^coefficients
    for simple reversible reactions.
    """

    REACTIONS = [
        {
            "equation": "N2 + 3H2 <-> 2NH3",
            "products": [("NH3", 2)],
            "reactants": [("N2", 1), ("H2", 3)],
        },
        {
            "equation": "H2 + I2 <-> 2HI",
            "products": [("HI", 2)],
            "reactants": [("H2", 1), ("I2", 1)],
        },
        {
            "equation": "2SO2 + O2 <-> 2SO3",
            "products": [("SO3", 2)],
            "reactants": [("SO2", 2), ("O2", 1)],
        },
        {
            "equation": "PCl5 <-> PCl3 + Cl2",
            "products": [("PCl3", 1), ("Cl2", 1)],
            "reactants": [("PCl5", 1)],
        },
        {
            "equation": "CO + H2O <-> CO2 + H2",
            "products": [("CO2", 1), ("H2", 1)],
            "reactants": [("CO", 1), ("H2O", 1)],
        },
        {
            "equation": "2NO2 <-> N2O4",
            "products": [("N2O4", 1)],
            "reactants": [("NO2", 2)],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "equilibrium_constant"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation", "division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute equilibrium constant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an equilibrium constant problem.

        Assigns random equilibrium concentrations to each species
        and computes K.

        Args:
            difficulty: Controls reaction complexity and concentration range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REACTIONS), 2 + difficulty)
        rxn = self._rng.choice(self.REACTIONS[:pool_size])

        all_species = (
            [(s, c, "product") for s, c in rxn["products"]]
            + [(s, c, "reactant") for s, c in rxn["reactants"]]
        )
        concentrations = {}
        for species, _, _ in all_species:
            concentrations[species] = round(self._rng.uniform(0.05, 3.0), 3)

        numerator = 1.0
        for species, coeff in rxn["products"]:
            numerator *= concentrations[species] ** coeff
        denominator = 1.0
        for species, coeff in rxn["reactants"]:
            denominator *= concentrations[species] ** coeff
        k_eq = round(numerator / denominator, 4)

        conc_str = ", ".join(
            f"[{s}]={concentrations[s]}" for s, _, _ in all_species
        )
        return (
            f"{rxn['equation']}; {conc_str}. Find K.",
            {"rxn": rxn, "concentrations": concentrations, "k_eq": k_eq},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        rxn = sd["rxn"]
        conc = sd["concentrations"]
        num_parts = " * ".join(
            f"[{s}]^{c}" for s, c in rxn["products"]
        )
        den_parts = " * ".join(
            f"[{s}]^{c}" for s, c in rxn["reactants"]
        )
        num_vals = " * ".join(
            f"{conc[s]}^{c}" for s, c in rxn["products"]
        )
        den_vals = " * ".join(
            f"{conc[s]}^{c}" for s, c in rxn["reactants"]
        )
        return [
            f"K = ({num_parts}) / ({den_parts})",
            f"K = ({num_vals}) / ({den_vals})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Equilibrium constant as string.
        """
        return str(sd["k_eq"])


@register
class LeChatelierGenerator(PhysicalChemistryBase):
    """Predict equilibrium shift direction using Le Chatelier's principle.

    Given a reaction and a perturbation (add reactant, increase temperature,
    increase pressure), predicts the direction of shift.
    """

    SCENARIOS = [
        {
            "equation": "N2 + 3H2 <-> 2NH3",
            "dH": "exothermic",
            "moles_gas_left": 4, "moles_gas_right": 2,
            "perturbations": [
                ("add N2", "right"),
                ("remove NH3", "right"),
                ("increase pressure", "right"),
                ("increase temperature", "left"),
                ("add H2", "right"),
                ("decrease pressure", "left"),
            ],
        },
        {
            "equation": "2SO2 + O2 <-> 2SO3",
            "dH": "exothermic",
            "moles_gas_left": 3, "moles_gas_right": 2,
            "perturbations": [
                ("add SO2", "right"),
                ("increase pressure", "right"),
                ("increase temperature", "left"),
                ("remove O2", "left"),
            ],
        },
        {
            "equation": "H2 + I2 <-> 2HI",
            "dH": "exothermic",
            "moles_gas_left": 2, "moles_gas_right": 2,
            "perturbations": [
                ("add H2", "right"),
                ("increase temperature", "left"),
                ("increase pressure", "no shift"),
                ("remove HI", "right"),
            ],
        },
        {
            "equation": "PCl5 <-> PCl3 + Cl2",
            "dH": "endothermic",
            "moles_gas_left": 1, "moles_gas_right": 2,
            "perturbations": [
                ("add PCl5", "right"),
                ("increase temperature", "right"),
                ("increase pressure", "left"),
                ("remove Cl2", "right"),
            ],
        },
        {
            "equation": "CO + H2O <-> CO2 + H2",
            "dH": "exothermic",
            "moles_gas_left": 2, "moles_gas_right": 2,
            "perturbations": [
                ("add CO", "right"),
                ("increase temperature", "left"),
                ("increase pressure", "no shift"),
                ("remove H2", "right"),
            ],
        },
        {
            "equation": "CaCO3(s) <-> CaO(s) + CO2(g)",
            "dH": "endothermic",
            "moles_gas_left": 0, "moles_gas_right": 1,
            "perturbations": [
                ("increase temperature", "right"),
                ("increase pressure", "left"),
                ("remove CO2", "right"),
            ],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "le_chatelier"

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
        return "predict equilibrium shift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Le Chatelier's principle problem.

        Selects a reaction scenario and a random perturbation.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SCENARIOS), 2 + difficulty)
        scenario = self._rng.choice(self.SCENARIOS[:pool_size])
        perturbation, shift = self._rng.choice(scenario["perturbations"])
        return (
            f"{scenario['equation']}, {scenario['dH']}. "
            f"Perturbation: {perturbation}. Shift direction?",
            {"equation": scenario["equation"], "dH": scenario["dH"],
             "perturbation": perturbation, "shift": shift},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"reaction is {sd['dH']}",
            f"perturbation: {sd['perturbation']}",
            "system shifts to counteract the change",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Shift direction string.
        """
        return sd["shift"]


@register
class HessLawGenerator(PhysicalChemistryBase):
    """Compute reaction enthalpy using Hess's law.

    Uses standard enthalpies of formation:
    dH_rxn = sum(dH_f products) - sum(dH_f reactants).
    """

    FORMATION_ENTHALPIES = {
        "H2O(l)": -285.8, "H2O(g)": -241.8, "CO2(g)": -393.5,
        "NH3(g)": -45.9, "NO(g)": 91.3, "NO2(g)": 33.2,
        "SO2(g)": -296.8, "SO3(g)": -395.7, "HCl(g)": -92.3,
        "HBr(g)": -36.3, "CH4(g)": -74.6, "C2H6(g)": -84.0,
        "C2H4(g)": 52.4, "C2H2(g)": 226.7, "CH3OH(l)": -238.4,
        "C6H12O6(s)": -1273.0, "Fe2O3(s)": -824.2, "Al2O3(s)": -1675.7,
        "CaO(s)": -634.9, "CaCO3(s)": -1206.9,
    }

    REACTIONS = [
        {
            "equation": "CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)",
            "products": [("CO2(g)", 1), ("H2O(l)", 2)],
            "reactants": [("CH4(g)", 1)],
        },
        {
            "equation": "C2H6(g) + 7/2 O2(g) -> 2CO2(g) + 3H2O(l)",
            "products": [("CO2(g)", 2), ("H2O(l)", 3)],
            "reactants": [("C2H6(g)", 1)],
        },
        {
            "equation": "2NO(g) + O2(g) -> 2NO2(g)",
            "products": [("NO2(g)", 2)],
            "reactants": [("NO(g)", 2)],
        },
        {
            "equation": "CaCO3(s) -> CaO(s) + CO2(g)",
            "products": [("CaO(s)", 1), ("CO2(g)", 1)],
            "reactants": [("CaCO3(s)", 1)],
        },
        {
            "equation": "2SO2(g) + O2(g) -> 2SO3(g)",
            "products": [("SO3(g)", 2)],
            "reactants": [("SO2(g)", 2)],
        },
        {
            "equation": "NH3(g) + HCl(g) -> NH4Cl(s)",
            "products": [],
            "reactants": [("NH3(g)", 1), ("HCl(g)", 1)],
            "dh_products_override": -314.4,
        },
        {
            "equation": "C2H4(g) + H2(g) -> C2H6(g)",
            "products": [("C2H6(g)", 1)],
            "reactants": [("C2H4(g)", 1)],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hess_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute reaction enthalpy via Hess's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hess's law problem.

        Selects a reaction and computes dH from formation enthalpies.
        Elements in standard state have dH_f = 0.

        Args:
            difficulty: Controls reaction pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REACTIONS), 3 + difficulty)
        rxn = self._rng.choice(self.REACTIONS[:pool_size])

        if "dh_products_override" in rxn:
            sum_products = rxn["dh_products_override"]
        else:
            sum_products = sum(
                self.FORMATION_ENTHALPIES[s] * c for s, c in rxn["products"]
            )

        sum_reactants = sum(
            self.FORMATION_ENTHALPIES.get(s, 0.0) * c
            for s, c in rxn["reactants"]
        )
        dh_rxn = round(sum_products - sum_reactants, 1)

        return (
            f"dH_rxn for {rxn['equation']}?",
            {"equation": rxn["equation"], "sum_products": round(sum_products, 1),
             "sum_reactants": round(sum_reactants, 1), "dh_rxn": dh_rxn,
             "products": rxn["products"], "reactants": rxn["reactants"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "dH = sum(dH_f products) - sum(dH_f reactants)",
            f"sum products = {sd['sum_products']} kJ/mol",
            f"sum reactants = {sd['sum_reactants']} kJ/mol",
            f"dH = {sd['sum_products']} - {sd['sum_reactants']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Reaction enthalpy string.
        """
        return f"{sd['dh_rxn']} kJ/mol"


@register
class NernstEquationGenerator(PhysicalChemistryBase):
    """Compute cell potential at non-standard conditions using the Nernst equation.

    Uses E = E0 - (RT / nF) * ln(Q), where F = 96485 C/mol
    and R = 8.314 J/(mol*K).
    """

    HALF_CELLS = [
        {
            "cell": "Zn | Zn2+ || Cu2+ | Cu",
            "e0": 1.10, "n": 2,
            "anode_species": "Zn2+", "cathode_species": "Cu2+",
        },
        {
            "cell": "Fe | Fe2+ || Cu2+ | Cu",
            "e0": 0.78, "n": 2,
            "anode_species": "Fe2+", "cathode_species": "Cu2+",
        },
        {
            "cell": "Zn | Zn2+ || Ag+ | Ag",
            "e0": 1.56, "n": 2,
            "anode_species": "Zn2+", "cathode_species": "Ag+",
        },
        {
            "cell": "Mg | Mg2+ || Cu2+ | Cu",
            "e0": 2.71, "n": 2,
            "anode_species": "Mg2+", "cathode_species": "Cu2+",
        },
        {
            "cell": "Ni | Ni2+ || Cu2+ | Cu",
            "e0": 0.59, "n": 2,
            "anode_species": "Ni2+", "cathode_species": "Cu2+",
        },
        {
            "cell": "Pb | Pb2+ || Cu2+ | Cu",
            "e0": 0.47, "n": 2,
            "anode_species": "Pb2+", "cathode_species": "Cu2+",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nernst_equation"

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
            Short task description string.
        """
        return "compute cell potential via Nernst equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Nernst equation problem.

        Assigns random concentrations to anode and cathode species,
        a temperature, and computes the non-standard cell potential.

        Args:
            difficulty: Controls concentration and temperature ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.HALF_CELLS), 2 + difficulty)
        cell = self._rng.choice(self.HALF_CELLS[:pool_size])
        conc_anode = round(self._rng.uniform(0.001, 2.0), 4)
        conc_cathode = round(self._rng.uniform(0.001, 2.0), 4)
        temp = self._rng.randint(273, 373)

        q = conc_anode / conc_cathode
        e_cell = round(
            cell["e0"] - (self.R * temp / (cell["n"] * self.F)) * math.log(q),
            4,
        )

        return (
            f"{cell['cell']}, [{cell['anode_species']}]={conc_anode} M, "
            f"[{cell['cathode_species']}]={conc_cathode} M, T={temp} K. "
            f"Find E.",
            {"cell": cell, "conc_anode": conc_anode,
             "conc_cathode": conc_cathode, "temp": temp,
             "q": round(q, 4), "e_cell": e_cell},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        cell = sd["cell"]
        correction = round(
            self.R * sd["temp"] / (cell["n"] * self.F) * math.log(sd["q"]),
            4,
        )
        return [
            "E = E0 - (RT/nF)*ln(Q)",
            f"Q = [{cell['anode_species']}]/[{cell['cathode_species']}] = {sd['q']}",
            f"E = {cell['e0']} - {correction}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Cell potential string.
        """
        return f"{sd['e_cell']} V"


@register
class GibbsSpontaneityGenerator(PhysicalChemistryBase):
    """Determine spontaneity using dG = dH - T*dS.

    Computes Gibbs free energy change and classifies the reaction
    as spontaneous (dG < 0), non-spontaneous (dG > 0), or at
    equilibrium (dG = 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gibbs_spontaneity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "determine spontaneity via Gibbs free energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gibbs free energy problem.

        Randomly generates dH (kJ/mol) and dS (J/(mol*K)) with
        realistic magnitudes, then computes dG at a given temperature.

        Args:
            difficulty: Controls magnitude ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dh = round(self._rng.uniform(-300, 300), 1)
        ds_jmolk = round(self._rng.uniform(-200, 200), 1)
        temp = self._rng.randint(200, 600)

        ds_kjmolk = ds_jmolk / 1000.0
        dg = round(dh - temp * ds_kjmolk, 4)

        if abs(dg) < 0.01:
            classification = "at equilibrium"
        elif dg < 0:
            classification = "spontaneous"
        else:
            classification = "non-spontaneous"

        return (
            f"dH={dh} kJ/mol, dS={ds_jmolk} J/(mol*K), T={temp} K. "
            f"Is the reaction spontaneous?",
            {"dh": dh, "ds_jmolk": ds_jmolk, "ds_kjmolk": round(ds_kjmolk, 4),
             "temp": temp, "dg": dg, "classification": classification},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "dG = dH - T*dS",
            f"dS = {sd['ds_jmolk']} J/(mol*K) = {sd['ds_kjmolk']} kJ/(mol*K)",
            f"dG = {sd['dh']} - {sd['temp']}*{sd['ds_kjmolk']}",
            f"dG = {sd['dg']} kJ/mol",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Classification with dG value.
        """
        return f"{sd['dg']} kJ/mol, {sd['classification']}"


@register
class ReactionOrderGenerator(PhysicalChemistryBase):
    """Determine reaction order from initial rate data.

    Generates a set of experiments where one reactant concentration
    is varied while others are held constant, then computes the
    order by comparing rates using logarithmic ratios.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reaction_order"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm", "linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "determine reaction order from rate data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reaction order determination problem.

        Creates two experiments differing in one reactant concentration
        to isolate the order with respect to that reactant. Uses clean
        integer orders (0, 1, or 2).

        Args:
            difficulty: Controls which orders are possible.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        max_order = min(2, 1 + difficulty // 3)
        true_order = self._rng.randint(0, max_order)

        conc_1 = round(self._rng.uniform(0.1, 1.0), 3)
        multiplier = self._rng.choice([2, 3])
        conc_2 = round(conc_1 * multiplier, 3)

        k_eff = round(self._rng.uniform(0.01, 1.0), 4)
        rate_1 = round(k_eff * (conc_1 ** true_order), 4)
        rate_2 = round(k_eff * (conc_2 ** true_order), 4)

        if true_order == 0 and rate_1 == rate_2:
            computed_order = 0
        else:
            ratio_rate = rate_2 / rate_1 if rate_1 != 0 else 1.0
            ratio_conc = conc_2 / conc_1
            if ratio_conc > 0 and ratio_rate > 0:
                computed_order = round(
                    math.log(ratio_rate) / math.log(ratio_conc)
                )
            else:
                computed_order = 0

        return (
            f"Exp1: [A]={conc_1} M, rate={rate_1} M/s; "
            f"Exp2: [A]={conc_2} M, rate={rate_2} M/s. Order w.r.t. A?",
            {"conc_1": conc_1, "conc_2": conc_2,
             "rate_1": rate_1, "rate_2": rate_2,
             "true_order": true_order, "computed_order": computed_order,
             "multiplier": multiplier},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        ratio_conc = round(sd["conc_2"] / sd["conc_1"], 4)
        if sd["rate_1"] != 0:
            ratio_rate = round(sd["rate_2"] / sd["rate_1"], 4)
        else:
            ratio_rate = 1.0
        return [
            f"[A] ratio: {sd['conc_2']}/{sd['conc_1']} = {ratio_conc}",
            f"rate ratio: {sd['rate_2']}/{sd['rate_1']} = {ratio_rate}",
            f"n = log({ratio_rate})/log({ratio_conc})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Reaction order as string.
        """
        return f"order {sd['computed_order']}"
