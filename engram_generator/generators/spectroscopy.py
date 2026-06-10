"""Spectroscopy generators -- Beer-Lambert, NMR, mass spec, IR, emission.

6 generators at tier 5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class SpectroscopyBase(StepGenerator):
    """Base class for spectroscopy generators with shared constants.

    Provides fundamental physical constants and spectroscopy data
    tables used across multiple spectroscopy generators.

    Attributes:
        H_PLANCK: Planck's constant in J*s.
        C_LIGHT: Speed of light in m/s.
        EV_PER_JOULE: Conversion factor from joules to electronvolts.
        RYDBERG: Rydberg constant in m^-1.
    """

    H_PLANCK = 6.626e-34   # J*s
    C_LIGHT = 3.0e8        # m/s
    EV_PER_JOULE = 6.242e18

    RYDBERG = 1.097e7      # m^-1

    COMMON_LOSSES = {
        15: "CH3",
        17: "OH",
        18: "H2O",
        28: "CO",
        29: "CHO",
        31: "OCH3",
        44: "CO2",
        45: "OC2H5",
        46: "NO2",
    }

    IR_RANGES = [
        (3200, 3600, "O-H stretch (broad) or N-H stretch"),
        (2850, 3000, "C-H stretch (alkane)"),
        (3000, 3100, "C-H stretch (alkene/aromatic)"),
        (2100, 2260, "C#C or C#N stretch (triple bond)"),
        (1650, 1750, "C=O stretch (carbonyl)"),
        (1600, 1680, "C=C stretch"),
        (1000, 1300, "C-O stretch"),
        (500, 800, "C-Cl or C-Br stretch (halide)"),
    ]

    NMR_MULTIPLICITY = {
        0: "singlet",
        1: "doublet",
        2: "triplet",
        3: "quartet",
        4: "quintet",
        5: "sextet",
        6: "septet",
    }

    EMISSION_SERIES = {
        1: "Lyman",
        2: "Balmer",
        3: "Paschen",
        4: "Brackett",
        5: "Pfund",
    }


@register
class BeerLambertGenerator(SpectroscopyBase):
    """Apply Beer-Lambert law: A = epsilon * l * c, or A = -log10(T).

    Given three of the four variables (absorbance A, molar absorptivity
    epsilon, path length l, concentration c), computes the fourth.
    Also handles conversion between absorbance and transmittance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "beer_lambert"

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
        return "apply Beer-Lambert law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Beer-Lambert law problem.

        Randomly selects which variable to solve for or asks for
        absorbance-transmittance conversion.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mode = self._rng.choice(["find_A", "find_c", "find_epsilon",
                                  "find_l", "transmittance"])

        epsilon = round(self._rng.uniform(50, 5000 + 500 * difficulty), 4)
        path_length = round(self._rng.uniform(0.5, 5.0), 4)
        concentration = round(self._rng.uniform(1e-5, 1e-2), 4)
        absorbance = round(epsilon * path_length * concentration, 4)

        if mode == "transmittance":
            transmittance = round(10 ** (-absorbance), 4)
            return (
                f"A = {absorbance}. Find transmittance T.",
                {"mode": mode, "absorbance": absorbance,
                 "transmittance": transmittance,
                 "epsilon": epsilon, "l": path_length,
                 "c": concentration},
            )

        if mode == "find_A":
            return (
                f"epsilon = {epsilon} L/(mol*cm), l = {path_length} cm, "
                f"c = {concentration} M. Find A.",
                {"mode": mode, "epsilon": epsilon, "l": path_length,
                 "c": concentration, "absorbance": absorbance},
            )
        if mode == "find_c":
            return (
                f"A = {absorbance}, epsilon = {epsilon} L/(mol*cm), "
                f"l = {path_length} cm. Find c.",
                {"mode": mode, "epsilon": epsilon, "l": path_length,
                 "c": concentration, "absorbance": absorbance},
            )
        if mode == "find_epsilon":
            return (
                f"A = {absorbance}, l = {path_length} cm, "
                f"c = {concentration} M. Find epsilon.",
                {"mode": mode, "epsilon": epsilon, "l": path_length,
                 "c": concentration, "absorbance": absorbance},
            )
        # find_l
        return (
            f"A = {absorbance}, epsilon = {epsilon} L/(mol*cm), "
            f"c = {concentration} M. Find l.",
            {"mode": mode, "epsilon": epsilon, "l": path_length,
             "c": concentration, "absorbance": absorbance},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "transmittance":
            return [
                "A = -log10(T), so T = 10^(-A)",
                f"T = 10^(-{sd['absorbance']})",
            ]
        if sd["mode"] == "find_A":
            return [
                "A = epsilon * l * c",
                f"A = {sd['epsilon']} * {sd['l']} * {sd['c']}",
            ]
        if sd["mode"] == "find_c":
            return [
                "c = A / (epsilon * l)",
                f"c = {sd['absorbance']} / ({sd['epsilon']} * {sd['l']})",
            ]
        if sd["mode"] == "find_epsilon":
            return [
                "epsilon = A / (l * c)",
                f"epsilon = {sd['absorbance']} / ({sd['l']} * {sd['c']})",
            ]
        return [
            "l = A / (epsilon * c)",
            f"l = {sd['absorbance']} / ({sd['epsilon']} * {sd['c']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Computed value with units.
        """
        if sd["mode"] == "transmittance":
            return f"T = {sd['transmittance']}"
        if sd["mode"] == "find_A":
            return f"A = {sd['absorbance']}"
        if sd["mode"] == "find_c":
            return f"c = {sd['c']} M"
        if sd["mode"] == "find_epsilon":
            return f"epsilon = {sd['epsilon']} L/(mol*cm)"
        return f"l = {sd['l']} cm"


@register
class WavelengthEnergyGenerator(SpectroscopyBase):
    """Convert between wavelength and photon energy using E = hc/lambda.

    Given a wavelength in nanometres, computes the photon energy in
    both joules and electronvolts, or vice versa.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wavelength_energy"

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
        return "convert between wavelength and photon energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a wavelength-energy conversion problem.

        Randomly asks to convert wavelength to energy or energy to
        wavelength across UV, visible, and IR ranges.

        Args:
            difficulty: Controls wavelength range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mode = self._rng.choice(["lambda_to_E", "E_to_lambda"])

        # Wavelength in nm
        if difficulty <= 3:
            lam_nm = self._rng.randint(400, 700)
        elif difficulty <= 6:
            lam_nm = self._rng.randint(100, 1000)
        else:
            lam_nm = self._rng.randint(10, 2000)

        lam_m = lam_nm * 1e-9
        energy_j = self.H_PLANCK * self.C_LIGHT / lam_m
        energy_ev = round(energy_j * self.EV_PER_JOULE, 4)
        energy_j = round(energy_j, 4)

        if mode == "lambda_to_E":
            return (
                f"wavelength = {lam_nm} nm. Find energy in eV.",
                {"mode": mode, "lam_nm": lam_nm, "lam_m": lam_m,
                 "energy_j": energy_j, "energy_ev": energy_ev},
            )
        return (
            f"photon energy = {energy_ev} eV. Find wavelength in nm.",
            {"mode": mode, "lam_nm": lam_nm, "lam_m": lam_m,
             "energy_j": energy_j, "energy_ev": energy_ev},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "lambda_to_E":
            return [
                "E = hc/lambda",
                f"E = 6.626e-34 * 3e8 / ({sd['lam_nm']}e-9)",
                f"E = {sd['energy_j']:.4e} J",
                f"E = {sd['energy_ev']} eV",
            ]
        return [
            "lambda = hc/E",
            f"E = {sd['energy_ev']} eV = {sd['energy_j']:.4e} J",
            f"lambda = 6.626e-34 * 3e8 / {sd['energy_j']:.4e}",
            f"lambda = {sd['lam_nm']} nm",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Energy or wavelength string.
        """
        if sd["mode"] == "lambda_to_E":
            return f"E = {sd['energy_ev']} eV"
        return f"lambda = {sd['lam_nm']} nm"


@register
class NmrSplittingGenerator(SpectroscopyBase):
    """Predict NMR splitting pattern using the n+1 rule.

    Given the number of equivalent neighbouring hydrogens, predicts
    the multiplicity of the NMR signal (singlet, doublet, triplet,
    quartet, etc.).
    """

    NMR_ENVIRONMENTS = [
        {"group": "CH3 adjacent to CH2", "neighbours": 2,
         "description": "methyl group next to a methylene"},
        {"group": "CH2 adjacent to CH3", "neighbours": 3,
         "description": "methylene group next to a methyl"},
        {"group": "CH adjacent to 2 CH3", "neighbours": 6,
         "description": "methine with two adjacent methyls"},
        {"group": "CH3 (isolated)", "neighbours": 0,
         "description": "methyl group with no H neighbours"},
        {"group": "CH2 adjacent to CH", "neighbours": 1,
         "description": "methylene next to a methine"},
        {"group": "CH adjacent to CH2 + CH3", "neighbours": 5,
         "description": "methine between methylene and methyl"},
        {"group": "CH2 adjacent to 2 CH2", "neighbours": 4,
         "description": "methylene flanked by two methylenes"},
        {"group": "CH3 adjacent to CH", "neighbours": 1,
         "description": "methyl next to a methine"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nmr_splitting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functional_group_id"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "predict NMR splitting pattern using n+1 rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NMR splitting pattern problem.

        Selects an H environment and asks for the multiplicity.

        Args:
            difficulty: Controls environment complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.NMR_ENVIRONMENTS), 3 + difficulty)
        env = self._rng.choice(self.NMR_ENVIRONMENTS[:pool_size])

        n = env["neighbours"]
        multiplicity_num = n + 1
        multiplicity_name = self.NMR_MULTIPLICITY.get(
            n, f"{multiplicity_num}-plet"
        )

        return (
            f"{env['description']}: {n} equivalent neighbouring H. "
            f"Predict splitting.",
            {"group": env["group"], "description": env["description"],
             "n": n, "multiplicity_num": multiplicity_num,
             "multiplicity_name": multiplicity_name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"group: {sd['group']}",
            f"equivalent neighbouring H: n = {sd['n']}",
            f"n+1 rule: {sd['n']}+1 = {sd['multiplicity_num']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Multiplicity name string.
        """
        return sd["multiplicity_name"]


@register
class MassSpecFragmentGenerator(SpectroscopyBase):
    """Identify the lost group from a mass spectrum fragmentation.

    Given the molecular ion peak M and a fragment peak m/z, computes
    the mass difference and identifies the most likely lost group
    from a table of common neutral losses.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_spec_fragment"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "identify the lost group from mass spectrum fragmentation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass spectrum fragmentation problem.

        Picks a common neutral loss, generates a plausible molecular
        weight, and asks for the identity of the lost fragment.

        Args:
            difficulty: Controls molecular weight range and loss variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        losses = list(self.COMMON_LOSSES.items())
        pool_size = min(len(losses), 4 + difficulty)
        mass_diff, lost_group = self._rng.choice(losses[:pool_size])

        # Generate molecular weight
        mol_weight = self._rng.randint(
            max(50, mass_diff + 20),
            150 + 30 * difficulty,
        )
        fragment = mol_weight - mass_diff

        return (
            f"M+ = {mol_weight}, fragment m/z = {fragment}. "
            f"Identify the lost group.",
            {"mol_weight": mol_weight, "fragment": fragment,
             "mass_diff": mass_diff, "lost_group": lost_group},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"M+ = {sd['mol_weight']}, fragment = {sd['fragment']}",
            f"loss = {sd['mol_weight']} - {sd['fragment']}"
            f" = {sd['mass_diff']}",
            f"mass {sd['mass_diff']}: {sd['lost_group']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Lost group identity.
        """
        return f"lost group: {sd['lost_group']} (mass {sd['mass_diff']})"


@register
class IrFunctionalGroupGenerator(SpectroscopyBase):
    """Identify functional group from IR absorption frequency.

    Given an IR absorption frequency or range, identifies the most
    likely functional group responsible for the absorption based
    on characteristic frequency ranges.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ir_functional_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functional_group_id"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "identify functional group from IR absorption frequency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IR functional group identification problem.

        Picks a characteristic IR range and generates a frequency
        within that range, then asks for the functional group.

        Args:
            difficulty: Controls variety of IR ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.IR_RANGES), 3 + difficulty)
        low, high, group = self._rng.choice(self.IR_RANGES[:pool_size])

        frequency = self._rng.randint(low, high)

        return (
            f"IR absorption at {frequency} cm^-1. "
            f"Identify the functional group.",
            {"frequency": frequency, "range_low": low,
             "range_high": high, "group": group},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"observed frequency: {sd['frequency']} cm^-1",
            f"range {sd['range_low']}-{sd['range_high']} cm^-1",
            f"assignment: {sd['group']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Functional group assignment.
        """
        return sd["group"]


@register
class EmissionSpectrumGenerator(SpectroscopyBase):
    """Compute emission wavelength using the Rydberg formula.

    Computes the wavelength of a photon emitted during a hydrogen
    atom transition from n2 to n1 using 1/lambda = R(1/n1^2 - 1/n2^2).
    Identifies the spectral series (Lyman, Balmer, Paschen, etc.).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "emission_spectrum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hydrogen_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute emission wavelength and identify series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an emission spectrum problem.

        Selects a hydrogen transition n2 -> n1 and computes the
        emitted wavelength using the Rydberg formula.

        Args:
            difficulty: Controls energy level range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n1 = self._rng.randint(1, 2)
            n2 = self._rng.randint(n1 + 1, min(n1 + 2, 4))
        elif difficulty <= 6:
            n1 = self._rng.randint(1, 3)
            n2 = self._rng.randint(n1 + 1, min(n1 + 3, 6))
        else:
            n1 = self._rng.randint(1, 5)
            n2 = self._rng.randint(n1 + 1, min(n1 + 4, 8))

        inv_lam = self.RYDBERG * (1.0 / (n1 ** 2) - 1.0 / (n2 ** 2))
        wavelength_m = 1.0 / inv_lam
        wavelength_nm = round(wavelength_m * 1e9, 4)

        series = self.EMISSION_SERIES.get(n1, f"n1={n1}")

        return (
            f"hydrogen transition n={n2} -> n={n1}. "
            f"Find emission wavelength.",
            {"n1": n1, "n2": n2, "inv_lam": round(inv_lam, 4),
             "wavelength_m": wavelength_m,
             "wavelength_nm": wavelength_nm, "series": series},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        n1, n2 = sd["n1"], sd["n2"]
        inv_n1_sq = round(1.0 / (n1 ** 2), 4)
        inv_n2_sq = round(1.0 / (n2 ** 2), 4)
        return [
            f"1/lambda = R(1/{n1}^2 - 1/{n2}^2)",
            f"1/lambda = 1.097e7 * ({inv_n1_sq} - {inv_n2_sq})",
            f"lambda = {sd['wavelength_nm']} nm",
            f"series: {sd['series']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Wavelength and series name.
        """
        return f"lambda = {sd['wavelength_nm']} nm, {sd['series']} series"
