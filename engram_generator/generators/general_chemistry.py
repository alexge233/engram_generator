"""General chemistry generators — electron config, periodic trends, bonding, geometry.

8 generators across tiers 3-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class GeneralChemistryBase(StepGenerator):
    """Base class for general chemistry generators with shared element data.

    Provides electron configuration data, electronegativity values,
    and molecule geometry tables used by multiple generators.

    Attributes:
        ELEMENT_SYMBOLS: Ordered list of element symbols Z=1 to Z=36.
        ELECTRONEGATIVITIES: Pauling electronegativity values for common elements.
        ORBITAL_ORDER: Aufbau filling order for electron configurations.
        ORBITAL_CAPACITY: Maximum electrons per subshell type.
    """

    ELEMENT_SYMBOLS = [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr",
    ]

    ORBITAL_ORDER = [
        (1, "s"), (2, "s"), (2, "p"), (3, "s"), (3, "p"), (4, "s"),
        (3, "d"), (4, "p"),
    ]

    ORBITAL_CAPACITY = {"s": 2, "p": 6, "d": 10}

    # Exceptions: Cr (Z=24) and Cu (Z=29) prefer half/full d shells
    ELECTRON_CONFIG_EXCEPTIONS = {
        24: "1s2 2s2 2p6 3s2 3p6 4s1 3d5",
        29: "1s2 2s2 2p6 3s2 3p6 4s1 3d10",
    }

    ELECTRONEGATIVITIES = {
        "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55,
        "N": 3.04, "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31,
        "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
        "K": 0.82, "Ca": 1.00, "Br": 2.96, "I": 2.66, "Cs": 0.79,
        "Ba": 0.89, "Sr": 0.95, "Rb": 0.82,
    }

    # Ionisation energies in kJ/mol for trend comparison
    IONISATION_ENERGIES = {
        "H": 1312, "He": 2372, "Li": 520, "Be": 900, "B": 801,
        "C": 1086, "N": 1402, "O": 1314, "F": 1681, "Ne": 2081,
        "Na": 496, "Mg": 738, "Al": 578, "Si": 786, "P": 1012,
        "S": 1000, "Cl": 1251, "Ar": 1521, "K": 419, "Ca": 590,
    }

    # Atomic radii in pm for trend comparison
    ATOMIC_RADII = {
        "H": 53, "He": 31, "Li": 167, "Be": 112, "B": 87,
        "C": 77, "N": 75, "O": 73, "F": 71, "Ne": 69,
        "Na": 190, "Mg": 145, "Al": 118, "Si": 111, "P": 98,
        "S": 88, "Cl": 79, "Ar": 71, "K": 243, "Ca": 194,
    }

    SIMPLE_MOLECULES = {
        "H2O": {"central": "O", "bonds": 2, "lone_pairs": 2, "geometry": "bent",
                "hybridisation": "sp3", "atoms": [("H", 2)]},
        "NH3": {"central": "N", "bonds": 3, "lone_pairs": 1, "geometry": "trigonal pyramidal",
                "hybridisation": "sp3", "atoms": [("H", 3)]},
        "CH4": {"central": "C", "bonds": 4, "lone_pairs": 0, "geometry": "tetrahedral",
                "hybridisation": "sp3", "atoms": [("H", 4)]},
        "CO2": {"central": "C", "bonds": 2, "lone_pairs": 0, "geometry": "linear",
                "hybridisation": "sp", "atoms": [("O", 2)]},
        "BF3": {"central": "B", "bonds": 3, "lone_pairs": 0, "geometry": "trigonal planar",
                "hybridisation": "sp2", "atoms": [("F", 3)]},
        "PCl5": {"central": "P", "bonds": 5, "lone_pairs": 0,
                 "geometry": "trigonal bipyramidal", "hybridisation": "sp3d",
                 "atoms": [("Cl", 5)]},
        "SF6": {"central": "S", "bonds": 6, "lone_pairs": 0, "geometry": "octahedral",
                "hybridisation": "sp3d2", "atoms": [("F", 6)]},
        "SO2": {"central": "S", "bonds": 2, "lone_pairs": 1, "geometry": "bent",
                "hybridisation": "sp2", "atoms": [("O", 2)]},
        "HCN": {"central": "C", "bonds": 2, "lone_pairs": 0, "geometry": "linear",
                "hybridisation": "sp", "atoms": [("H", 1), ("N", 1)]},
        "H2S": {"central": "S", "bonds": 2, "lone_pairs": 2, "geometry": "bent",
                "hybridisation": "sp3", "atoms": [("H", 2)]},
        "ClF3": {"central": "Cl", "bonds": 3, "lone_pairs": 2, "geometry": "T-shaped",
                 "hybridisation": "sp3d", "atoms": [("F", 3)]},
        "XeF2": {"central": "Xe", "bonds": 2, "lone_pairs": 3, "geometry": "linear",
                 "hybridisation": "sp3d", "atoms": [("F", 2)]},
    }

    OXIDATION_COMPOUNDS = [
        ("NaCl", [("Na", +1), ("Cl", -1)]),
        ("MgO", [("Mg", +2), ("O", -2)]),
        ("Fe2O3", [("Fe", +3), ("O", -2)]),
        ("H2SO4", [("H", +1), ("S", +6), ("O", -2)]),
        ("KMnO4", [("K", +1), ("Mn", +7), ("O", -2)]),
        ("Na2CO3", [("Na", +1), ("C", +4), ("O", -2)]),
        ("HNO3", [("H", +1), ("N", +5), ("O", -2)]),
        ("CaCl2", [("Ca", +2), ("Cl", -1)]),
        ("K2Cr2O7", [("K", +1), ("Cr", +6), ("O", -2)]),
        ("CuSO4", [("Cu", +2), ("S", +6), ("O", -2)]),
        ("Al2O3", [("Al", +3), ("O", -2)]),
        ("CO2", [("C", +4), ("O", -2)]),
        ("SO3", [("S", +6), ("O", -2)]),
        ("P2O5", [("P", +5), ("O", -2)]),
        ("NO2", [("N", +4), ("O", -2)]),
        ("Cr2O3", [("Cr", +3), ("O", -2)]),
    ]

    def _build_electron_config(self, z: int) -> str:
        """Build the electron configuration string for atomic number z.

        Follows Aufbau principle with exceptions for Cr (Z=24) and Cu (Z=29).

        Args:
            z: Atomic number (1-36).

        Returns:
            Electron configuration string in standard notation.
        """
        if z in self.ELECTRON_CONFIG_EXCEPTIONS:
            return self.ELECTRON_CONFIG_EXCEPTIONS[z]

        remaining = z
        parts = []
        for n, sublevel in self.ORBITAL_ORDER:
            if remaining <= 0:
                break
            cap = self.ORBITAL_CAPACITY[sublevel]
            electrons = min(remaining, cap)
            parts.append(f"{n}{sublevel}{electrons}")
            remaining -= electrons
        return " ".join(parts)


@register
class ElectronConfigGenerator(GeneralChemistryBase):
    """Write the electron configuration for elements Z=1 to Z=36.

    Uses Aufbau principle with standard orbital filling order and
    handles the Cr/Cu exceptions. Output uses 1s2 2s2 2p6 notation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electron_config"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "write electron configuration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an electron configuration problem.

        Selects an element with atomic number scaled by difficulty.

        Args:
            difficulty: Controls which elements are available.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        max_z = min(36, 2 + 4 * difficulty)
        z = self._rng.randint(1, max_z)
        symbol = self.ELEMENT_SYMBOLS[z - 1]
        config = self._build_electron_config(z)
        return f"electron configuration of {symbol} (Z={z})", {
            "symbol": symbol, "z": z, "config": config,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [f"{sd['symbol']} has {sd['z']} electrons"]
        if sd["z"] in self.ELECTRON_CONFIG_EXCEPTIONS:
            steps.append("exception: half/full d subshell preferred")
        steps.append(f"fill orbitals: {sd['config']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Electron configuration string.
        """
        return sd["config"]


@register
class PeriodicTrendGenerator(GeneralChemistryBase):
    """Compare two elements on ionisation energy, electronegativity, or atomic radius.

    Uses actual Pauling electronegativities, first ionisation energies,
    and atomic radii for elements in the first four periods.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "periodic_trend"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compare periodic trend"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a periodic trend comparison problem.

        Picks two distinct elements and a property to compare.

        Args:
            difficulty: Controls which property tables are used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        properties = [
            ("ionisation_energy", self.IONISATION_ENERGIES, "kJ/mol", True),
            ("electronegativity", self.ELECTRONEGATIVITIES, "", True),
            ("atomic_radius", self.ATOMIC_RADII, "pm", True),
        ]
        prop_name, table, unit, _ = self._rng.choice(properties)
        elements = list(table.keys())
        a, b = self._rng.sample(elements, 2)
        val_a = table[a]
        val_b = table[b]
        higher = a if val_a > val_b else b
        return (
            f"which has higher {prop_name.replace('_', ' ')}: {a} or {b}?",
            {"a": a, "b": b, "val_a": val_a, "val_b": val_b,
             "prop": prop_name, "unit": unit, "higher": higher},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        u = f" {sd['unit']}" if sd["unit"] else ""
        return [
            f"{sd['a']}: {sd['val_a']}{u}",
            f"{sd['b']}: {sd['val_b']}{u}",
            f"{sd['val_a']} vs {sd['val_b']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Element symbol with higher value.
        """
        return sd["higher"]


@register
class LewisStructureGenerator(GeneralChemistryBase):
    """Count bonding pairs and lone pairs for simple molecules.

    Uses a curated set of molecules with known Lewis structures.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lewis_structure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["electron_config"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "count bonding and lone pairs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lewis structure counting problem.

        Selects a molecule from the curated set, with harder molecules
        available at higher difficulty.

        Args:
            difficulty: Controls molecule complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        easy = ["H2O", "NH3", "CH4", "CO2", "BF3", "HCN", "H2S"]
        hard = ["PCl5", "SF6", "SO2", "ClF3", "XeF2"]
        pool = easy if difficulty <= 4 else easy + hard
        mol_name = self._rng.choice(pool)
        mol = self.SIMPLE_MOLECULES[mol_name]
        return (
            f"bonding pairs and lone pairs on {mol['central']} in {mol_name}",
            {"molecule": mol_name, "central": mol["central"],
             "bonds": mol["bonds"], "lone_pairs": mol["lone_pairs"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        total_groups = sd["bonds"] + sd["lone_pairs"]
        return [
            f"central atom: {sd['central']}",
            f"bonding pairs: {sd['bonds']}",
            f"lone pairs: {sd['lone_pairs']}",
            f"total electron groups: {total_groups}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Bonding and lone pair counts.
        """
        return f"{sd['bonds']} bonding, {sd['lone_pairs']} lone"


@register
class VseprGeometryGenerator(GeneralChemistryBase):
    """Predict molecular geometry from electron group count using VSEPR theory.

    Determines geometry from the number of bonding pairs and lone pairs
    around the central atom.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vsepr_geometry"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lewis_structure"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "predict molecular geometry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a VSEPR geometry prediction problem.

        Args:
            difficulty: Controls molecule complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        easy = ["H2O", "NH3", "CH4", "CO2", "BF3", "HCN"]
        hard = ["PCl5", "SF6", "SO2", "ClF3", "XeF2", "H2S"]
        pool = easy if difficulty <= 4 else easy + hard
        mol_name = self._rng.choice(pool)
        mol = self.SIMPLE_MOLECULES[mol_name]
        return (
            f"molecular geometry of {mol_name}",
            {"molecule": mol_name, "central": mol["central"],
             "bonds": mol["bonds"], "lone_pairs": mol["lone_pairs"],
             "geometry": mol["geometry"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        total = sd["bonds"] + sd["lone_pairs"]
        return [
            f"central atom: {sd['central']}",
            f"bonding regions: {sd['bonds']}, lone pairs: {sd['lone_pairs']}",
            f"electron groups: {total}",
            f"geometry: {sd['geometry']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Molecular geometry string.
        """
        return sd["geometry"]


@register
class HybridisationGenerator(GeneralChemistryBase):
    """Determine hybridisation from molecular geometry.

    Maps electron group geometry to the corresponding orbital
    hybridisation (sp, sp2, sp3, sp3d, sp3d2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hybridisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vsepr_geometry"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "determine hybridisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hybridisation problem.

        Args:
            difficulty: Controls molecule complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        easy = ["H2O", "NH3", "CH4", "CO2", "BF3", "HCN"]
        hard = ["PCl5", "SF6", "SO2", "ClF3", "XeF2", "H2S"]
        pool = easy if difficulty <= 4 else easy + hard
        mol_name = self._rng.choice(pool)
        mol = self.SIMPLE_MOLECULES[mol_name]
        return (
            f"hybridisation of {mol['central']} in {mol_name}, "
            f"bonds={mol['bonds']}, lone_pairs={mol['lone_pairs']}",
            {"molecule": mol_name, "central": mol["central"],
             "bonds": mol["bonds"], "lone_pairs": mol["lone_pairs"],
             "geometry": mol["geometry"],
             "hybridisation": mol["hybridisation"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        total = sd["bonds"] + sd["lone_pairs"]
        return [
            f"electron groups: {total}",
            f"geometry: {sd['geometry']}",
            f"hybridisation: {sd['hybridisation']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Hybridisation string.
        """
        return sd["hybridisation"]


@register
class OxidationStateGenerator(GeneralChemistryBase):
    """Assign oxidation states to each atom in a compound.

    Uses common inorganic compounds with known oxidation states,
    applying standard rules (O = -2, H = +1, sum = 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oxidation_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["balancing_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "assign oxidation states"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an oxidation state assignment problem.

        Selects a compound and asks for oxidation states of all atoms.

        Args:
            difficulty: Controls compound complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.OXIDATION_COMPOUNDS), 4 + 2 * difficulty)
        compound, states = self._rng.choice(
            self.OXIDATION_COMPOUNDS[:pool_size]
        )
        return f"oxidation states in {compound}", {
            "compound": compound, "states": states,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["sum of oxidation states = 0"]
        for elem, ox in sd["states"]:
            sign = "+" if ox > 0 else ""
            steps.append(f"{elem}: {sign}{ox}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Formatted oxidation states string.
        """
        parts = []
        for elem, ox in sd["states"]:
            sign = "+" if ox > 0 else ""
            parts.append(f"{elem}={sign}{ox}")
        return ", ".join(parts)


@register
class ElectronegativityBondGenerator(GeneralChemistryBase):
    """Classify a bond as ionic, polar covalent, or nonpolar covalent.

    Uses the Pauling electronegativity difference: ionic (>1.7),
    polar covalent (0.4-1.7), nonpolar covalent (<0.4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electronegativity_bond"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "classify bond type"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bond classification problem.

        Picks two elements and classifies based on electronegativity difference.

        Args:
            difficulty: Controls element pool diversity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        elements = list(self.ELECTRONEGATIVITIES.keys())
        a, b = self._rng.sample(elements, 2)
        en_a = self.ELECTRONEGATIVITIES[a]
        en_b = self.ELECTRONEGATIVITIES[b]
        diff = round(abs(en_a - en_b), 2)
        if diff > 1.7:
            bond_type = "ionic"
        elif diff >= 0.4:
            bond_type = "polar covalent"
        else:
            bond_type = "nonpolar covalent"
        return (
            f"classify the {a}-{b} bond",
            {"a": a, "b": b, "en_a": en_a, "en_b": en_b,
             "diff": diff, "bond_type": bond_type},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"EN({sd['a']}) = {sd['en_a']}, EN({sd['b']}) = {sd['en_b']}",
            f"|{sd['en_a']} - {sd['en_b']}| = {sd['diff']}",
            ">1.7: ionic, 0.4-1.7: polar covalent, <0.4: nonpolar",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Bond type classification string.
        """
        return sd["bond_type"]


@register
class IdealGasStoichGenerator(GeneralChemistryBase):
    """Gas stoichiometry combining PV=nRT with mole ratios.

    Computes the volume of a gaseous product at given T and P from
    a known mass of reactant, using molar mass, stoichiometry, and
    the ideal gas law.
    """

    REACTIONS = [
        {
            "equation": "2H2 + O2 -> 2H2O",
            "reactant": "H2", "product": "H2O",
            "r_coeff": 2, "p_coeff": 2,
            "r_molar_mass": 2.016,
        },
        {
            "equation": "N2 + 3H2 -> 2NH3",
            "reactant": "N2", "product": "NH3",
            "r_coeff": 1, "p_coeff": 2,
            "r_molar_mass": 28.014,
        },
        {
            "equation": "CH4 + 2O2 -> CO2 + 2H2O",
            "reactant": "CH4", "product": "CO2",
            "r_coeff": 1, "p_coeff": 1,
            "r_molar_mass": 16.043,
        },
        {
            "equation": "2C2H6 + 7O2 -> 4CO2 + 6H2O",
            "reactant": "C2H6", "product": "CO2",
            "r_coeff": 2, "p_coeff": 4,
            "r_molar_mass": 30.069,
        },
        {
            "equation": "CaCO3 -> CaO + CO2",
            "reactant": "CaCO3", "product": "CO2",
            "r_coeff": 1, "p_coeff": 1,
            "r_molar_mass": 100.086,
        },
    ]

    R_CONST = 0.08206  # L*atm/(mol*K)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ideal_gas_stoich"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ideal_gas", "stoichiometry"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "gas stoichiometry with ideal gas law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gas stoichiometry problem.

        Given mass of reactant, temperature, and pressure, compute the
        volume of gaseous product.

        Args:
            difficulty: Controls mass range and reaction complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REACTIONS), 2 + difficulty)
        rxn = self._rng.choice(self.REACTIONS[:pool_size])
        mass = round(self._rng.uniform(1.0, 10.0 * difficulty), 2)
        temp_k = self._rng.randint(273, 500)
        pressure = round(self._rng.uniform(0.5, 3.0), 2)

        moles_r = mass / rxn["r_molar_mass"]
        moles_p = moles_r * rxn["p_coeff"] / rxn["r_coeff"]
        volume = round(moles_p * self.R_CONST * temp_k / pressure, 4)
        moles_r = round(moles_r, 4)
        moles_p = round(moles_p, 4)

        return (
            f"{rxn['equation']}: {mass}g {rxn['reactant']} at {temp_k}K, {pressure} atm. "
            f"Volume of {rxn['product']}?",
            {"rxn": rxn, "mass": mass, "temp_k": temp_k, "pressure": pressure,
             "moles_r": moles_r, "moles_p": moles_p, "volume": volume},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        rxn = sd["rxn"]
        return [
            f"moles {rxn['reactant']} = {sd['mass']}/{rxn['r_molar_mass']} = {sd['moles_r']}",
            f"ratio {rxn['r_coeff']}:{rxn['p_coeff']}, moles {rxn['product']} = {sd['moles_p']}",
            f"V = nRT/P = {sd['moles_p']}*0.08206*{sd['temp_k']}/{sd['pressure']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Volume in litres.
        """
        return f"{sd['volume']} L"
