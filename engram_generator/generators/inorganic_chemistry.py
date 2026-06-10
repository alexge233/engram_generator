"""Inorganic chemistry generators -- crystal field theory, coordination, isomers, Ksp.

6 generators at tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class InorganicChemistryBase(StepGenerator):
    """Base class for inorganic chemistry generators with shared data.

    Provides d-electron counts, coordination geometries, ligand
    spectrochemical ordering, and solubility product data used
    across multiple inorganic chemistry generators.

    Attributes:
        TRANSITION_METALS: Mapping of metal ion label to d-electron count.
        SPECTROCHEMICAL_SERIES: Ordered list of ligands from weak to strong field.
        LIGAND_RANK: Mapping of ligand name to its rank in the spectrochemical series.
    """

    TRANSITION_METALS = {
        "Ti3+": {"d_electrons": 1, "symbol": "Ti"},
        "V3+": {"d_electrons": 2, "symbol": "V"},
        "Cr3+": {"d_electrons": 3, "symbol": "Cr"},
        "Mn2+": {"d_electrons": 5, "symbol": "Mn"},
        "Mn3+": {"d_electrons": 4, "symbol": "Mn"},
        "Fe2+": {"d_electrons": 6, "symbol": "Fe"},
        "Fe3+": {"d_electrons": 5, "symbol": "Fe"},
        "Co2+": {"d_electrons": 7, "symbol": "Co"},
        "Co3+": {"d_electrons": 6, "symbol": "Co"},
        "Ni2+": {"d_electrons": 8, "symbol": "Ni"},
        "Cu2+": {"d_electrons": 9, "symbol": "Cu"},
    }

    SPECTROCHEMICAL_SERIES = [
        "I-", "Br-", "Cl-", "F-", "OH-", "H2O",
        "NH3", "en", "NO2-", "CN-", "CO",
    ]

    LIGAND_RANK = {lig: i for i, lig in enumerate(SPECTROCHEMICAL_SERIES)}

    COMMON_LIGANDS = {
        "NH3": {"name": "ammine", "denticity": 1},
        "H2O": {"name": "aqua", "denticity": 1},
        "Cl-": {"name": "chlorido", "denticity": 1},
        "CN-": {"name": "cyanido", "denticity": 1},
        "en": {"name": "ethylenediamine", "denticity": 2},
        "NO2-": {"name": "nitro", "denticity": 1},
        "CO": {"name": "carbonyl", "denticity": 1},
        "OH-": {"name": "hydroxido", "denticity": 1},
        "F-": {"name": "fluorido", "denticity": 1},
        "Br-": {"name": "bromido", "denticity": 1},
    }

    SOLUBILITY_PRODUCTS = [
        {"salt": "AgCl", "ions": [("Ag+", 1), ("Cl-", 1)],
         "ksp": 1.77e-10, "dissociation": "AgCl -> Ag+ + Cl-"},
        {"salt": "BaSO4", "ions": [("Ba2+", 1), ("SO4^2-", 1)],
         "ksp": 1.08e-10, "dissociation": "BaSO4 -> Ba2+ + SO4^2-"},
        {"salt": "PbCl2", "ions": [("Pb2+", 1), ("Cl-", 2)],
         "ksp": 1.70e-5, "dissociation": "PbCl2 -> Pb2+ + 2Cl-"},
        {"salt": "CaF2", "ions": [("Ca2+", 1), ("F-", 2)],
         "ksp": 3.45e-11, "dissociation": "CaF2 -> Ca2+ + 2F-"},
        {"salt": "Ag2CrO4", "ions": [("Ag+", 2), ("CrO4^2-", 1)],
         "ksp": 1.12e-12, "dissociation": "Ag2CrO4 -> 2Ag+ + CrO4^2-"},
        {"salt": "Fe(OH)3", "ions": [("Fe3+", 1), ("OH-", 3)],
         "ksp": 2.79e-39, "dissociation": "Fe(OH)3 -> Fe3+ + 3OH-"},
    ]


@register
class CrystalFieldGenerator(InorganicChemistryBase):
    """Determine d-orbital splitting and CFSE in octahedral or tetrahedral field.

    Given a transition metal ion and field geometry, determines the
    t2g/eg (or e/t2) filling for high-spin and low-spin configurations
    and computes the crystal field stabilisation energy in units of Dq.
    """

    # Octahedral filling: (t2g, eg) for high-spin and low-spin
    # CFSE = -0.4 * t2g + 0.6 * eg (in units of Dq)
    # For tetrahedral: e has -0.6 Dt, t2 has +0.4 Dt (but Dt ~ 4/9 Do)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crystal_field"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "determine d-orbital splitting and CFSE"

    def _fill_octahedral(self, d_count: int,
                         high_spin: bool) -> tuple[int, int, int, float]:
        """Fill octahedral d-orbitals and compute CFSE.

        Args:
            d_count: Number of d electrons.
            high_spin: Whether to use high-spin filling.

        Returns:
            Tuple of (t2g, eg, unpaired, cfse_in_dq).
        """
        if high_spin:
            # Fill all singly first, then pair
            if d_count <= 3:
                t2g, eg = d_count, 0
            elif d_count <= 5:
                t2g, eg = 3, d_count - 3
            elif d_count <= 8:
                t2g, eg = d_count - 2, 2
            else:
                t2g, eg = 6, d_count - 6
        else:
            # Fill t2g completely before eg
            if d_count <= 6:
                t2g, eg = d_count, 0
            else:
                t2g, eg = 6, d_count - 6

        # Unpaired electrons
        if high_spin:
            if d_count <= 5:
                unpaired = d_count
            else:
                unpaired = 10 - d_count
        else:
            # t2g fills: paired at >3
            t2g_unpaired = t2g if t2g <= 3 else max(0, 6 - t2g)
            eg_unpaired = eg if eg <= 2 else max(0, 4 - eg)
            unpaired = t2g_unpaired + eg_unpaired

        cfse = round(-0.4 * t2g + 0.6 * eg, 4)
        return t2g, eg, unpaired, cfse

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a crystal field splitting problem.

        Selects a metal ion and field geometry, then determines the
        electron configuration and CFSE.

        Args:
            difficulty: Controls metal ion variety and spin state.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ions = list(self.TRANSITION_METALS.keys())
        if difficulty <= 3:
            pool = [i for i in ions
                    if self.TRANSITION_METALS[i]["d_electrons"] <= 5]
        else:
            pool = ions
        ion = self._rng.choice(pool)
        d_count = self.TRANSITION_METALS[ion]["d_electrons"]

        geometry = self._rng.choice(["octahedral", "tetrahedral"])
        # Low-spin only meaningful for octahedral d4-d7
        if geometry == "octahedral" and 4 <= d_count <= 7:
            high_spin = self._rng.choice([True, False])
        else:
            high_spin = True

        spin_label = "high-spin" if high_spin else "low-spin"

        if geometry == "octahedral":
            t2g, eg, unpaired, cfse = self._fill_octahedral(d_count, high_spin)
            config_str = f"t2g^{t2g} eg^{eg}"
        else:
            # Tetrahedral is always high-spin
            if d_count <= 2:
                e_count, t2_count = d_count, 0
            elif d_count <= 4:
                e_count, t2_count = 2, d_count - 2
            elif d_count <= 7:
                e_count, t2_count = min(4, d_count - (d_count - 4)),\
                    max(0, d_count - 4)
                e_count = 4 if d_count >= 7 else d_count - t2_count
                # Simple approach
                if d_count <= 4:
                    e_count, t2_count = min(d_count, 2), max(0, d_count - 2)
                else:
                    e_count = min(4, d_count)
                    t2_count = d_count - e_count
            else:
                e_count = 4
                t2_count = d_count - 4
            # Correct tetrahedral filling
            if d_count <= 2:
                e_count, t2_count = d_count, 0
            elif d_count == 3:
                e_count, t2_count = 2, 1
            elif d_count == 4:
                e_count, t2_count = 2, 2
            elif d_count == 5:
                e_count, t2_count = 2, 3
            elif d_count == 6:
                e_count, t2_count = 3, 3
            elif d_count == 7:
                e_count, t2_count = 4, 3
            elif d_count == 8:
                e_count, t2_count = 4, 4
            elif d_count == 9:
                e_count, t2_count = 4, 5
            else:
                e_count, t2_count = 4, 6
            unpaired = d_count if d_count <= 5 else 10 - d_count
            cfse = round(-0.6 * e_count + 0.4 * t2_count, 4)
            config_str = f"e^{e_count} t2^{t2_count}"

        return (
            f"{ion} ({d_count} d-electrons) in {geometry} field",
            {"ion": ion, "d_count": d_count, "geometry": geometry,
             "high_spin": high_spin, "spin_label": spin_label,
             "config": config_str, "unpaired": unpaired, "cfse": cfse},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"{sd['ion']}: {sd['d_count']} d-electrons",
            f"field: {sd['geometry']}, {sd['spin_label']}",
            f"configuration: {sd['config']}",
            f"unpaired electrons: {sd['unpaired']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Configuration and CFSE string.
        """
        return f"{sd['config']}, CFSE = {sd['cfse']} Dq"


@register
class CoordinationNumberGenerator(InorganicChemistryBase):
    """Determine coordination number and geometry of a complex ion.

    Given a coordination compound formula, counts the total number
    of donor atoms around the central metal to find the coordination
    number, then identifies the expected geometry.
    """

    COMPLEXES = [
        {"formula": "[Co(NH3)6]3+", "metal": "Co3+", "cn": 6,
         "geometry": "octahedral", "ligands": [("NH3", 6)]},
        {"formula": "[Ni(CN)4]2-", "metal": "Ni2+", "cn": 4,
         "geometry": "square planar", "ligands": [("CN-", 4)]},
        {"formula": "[CoCl4]2-", "metal": "Co2+", "cn": 4,
         "geometry": "tetrahedral", "ligands": [("Cl-", 4)]},
        {"formula": "[Fe(CN)6]4-", "metal": "Fe2+", "cn": 6,
         "geometry": "octahedral", "ligands": [("CN-", 6)]},
        {"formula": "[Cu(NH3)4]2+", "metal": "Cu2+", "cn": 4,
         "geometry": "square planar", "ligands": [("NH3", 4)]},
        {"formula": "[Cr(H2O)6]3+", "metal": "Cr3+", "cn": 6,
         "geometry": "octahedral", "ligands": [("H2O", 6)]},
        {"formula": "[PtCl4]2-", "metal": "Pt2+", "cn": 4,
         "geometry": "square planar", "ligands": [("Cl-", 4)]},
        {"formula": "[Zn(OH)4]2-", "metal": "Zn2+", "cn": 4,
         "geometry": "tetrahedral", "ligands": [("OH-", 4)]},
        {"formula": "[Co(en)3]3+", "metal": "Co3+", "cn": 6,
         "geometry": "octahedral", "ligands": [("en", 3)]},
        {"formula": "[Fe(H2O)6]2+", "metal": "Fe2+", "cn": 6,
         "geometry": "octahedral", "ligands": [("H2O", 6)]},
        {"formula": "[Mn(H2O)6]2+", "metal": "Mn2+", "cn": 6,
         "geometry": "octahedral", "ligands": [("H2O", 6)]},
        {"formula": "[Ni(NH3)6]2+", "metal": "Ni2+", "cn": 6,
         "geometry": "octahedral", "ligands": [("NH3", 6)]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coordination_number"

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
        return "determine coordination number and geometry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coordination number problem.

        Selects a complex from the table, with more exotic complexes
        available at higher difficulty.

        Args:
            difficulty: Controls complex pool size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPLEXES), 4 + difficulty)
        cplx = self._rng.choice(self.COMPLEXES[:pool_size])

        lig_desc = ", ".join(
            f"{count} {lig}" for lig, count in cplx["ligands"]
        )
        return (
            f"coordination number and geometry of {cplx['formula']}",
            {"formula": cplx["formula"], "metal": cplx["metal"],
             "cn": cplx["cn"], "geometry": cplx["geometry"],
             "lig_desc": lig_desc},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"central metal: {sd['metal']}",
            f"ligands: {sd['lig_desc']}",
            f"coordination number: {sd['cn']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Coordination number and geometry.
        """
        return f"CN = {sd['cn']}, geometry = {sd['geometry']}"


@register
class IsomerCoordinationGenerator(InorganicChemistryBase):
    """Count geometric isomers for coordination compounds.

    For square planar MA2B2 determines cis/trans isomers. For
    octahedral MA3B3 determines fac/mer isomers. Uses curated
    examples of known isomer counts.
    """

    ISOMER_CASES = [
        {"formula": "[Pt(NH3)2Cl2]", "geometry": "square planar",
         "ligand_a": "NH3", "count_a": 2, "ligand_b": "Cl-", "count_b": 2,
         "isomers": ["cis", "trans"], "num_isomers": 2},
        {"formula": "[Co(NH3)4Cl2]+", "geometry": "octahedral",
         "ligand_a": "NH3", "count_a": 4, "ligand_b": "Cl-", "count_b": 2,
         "isomers": ["cis", "trans"], "num_isomers": 2},
        {"formula": "[Co(NH3)3Cl3]", "geometry": "octahedral",
         "ligand_a": "NH3", "count_a": 3, "ligand_b": "Cl-", "count_b": 3,
         "isomers": ["fac", "mer"], "num_isomers": 2},
        {"formula": "[Cr(en)2Cl2]+", "geometry": "octahedral",
         "ligand_a": "en", "count_a": 2, "ligand_b": "Cl-", "count_b": 2,
         "isomers": ["cis", "trans"], "num_isomers": 2},
        {"formula": "[Pt(NH3)2(NO2)2]", "geometry": "square planar",
         "ligand_a": "NH3", "count_a": 2, "ligand_b": "NO2-", "count_b": 2,
         "isomers": ["cis", "trans"], "num_isomers": 2},
        {"formula": "[Ir(NH3)3Cl3]", "geometry": "octahedral",
         "ligand_a": "NH3", "count_a": 3, "ligand_b": "Cl-", "count_b": 3,
         "isomers": ["fac", "mer"], "num_isomers": 2},
        {"formula": "[Ru(NH3)4Cl2]+", "geometry": "octahedral",
         "ligand_a": "NH3", "count_a": 4, "ligand_b": "Cl-", "count_b": 2,
         "isomers": ["cis", "trans"], "num_isomers": 2},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "isomer_coordination"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["coordination_number"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "count geometric isomers of the coordination compound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an isomer counting problem.

        Selects a coordination compound from the curated cases.

        Args:
            difficulty: Controls pool size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.ISOMER_CASES), 3 + difficulty)
        case = self._rng.choice(self.ISOMER_CASES[:pool_size])

        return (
            f"geometric isomers of {case['formula']} ({case['geometry']})",
            {"formula": case["formula"], "geometry": case["geometry"],
             "ligand_a": case["ligand_a"], "count_a": case["count_a"],
             "ligand_b": case["ligand_b"], "count_b": case["count_b"],
             "isomers": case["isomers"],
             "num_isomers": case["num_isomers"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        isomer_names = ", ".join(sd["isomers"])
        return [
            f"geometry: {sd['geometry']}",
            f"ligands: {sd['count_a']} {sd['ligand_a']}"
            f" + {sd['count_b']} {sd['ligand_b']}",
            f"possible arrangements: {isomer_names}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Number and names of isomers.
        """
        isomer_names = ", ".join(sd["isomers"])
        return f"{sd['num_isomers']} isomers: {isomer_names}"


@register
class SpectrochemicalGenerator(InorganicChemistryBase):
    """Order ligands by spectrochemical series and predict spin state.

    Given a set of ligands, orders them from weakest to strongest
    field and predicts whether a given metal complex would be
    high-spin or low-spin based on ligand field strength.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectrochemical"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["crystal_field"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "order ligands by field strength and predict spin"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectrochemical series ordering problem.

        Picks a subset of ligands to order and a metal ion to predict
        spin state for.

        Args:
            difficulty: Controls number of ligands and ion complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_ligands = min(self._rng.randint(3, 3 + difficulty // 2),
                          len(self.SPECTROCHEMICAL_SERIES))
        chosen = self._rng.sample(self.SPECTROCHEMICAL_SERIES, num_ligands)
        ordered = sorted(chosen, key=lambda x: self.LIGAND_RANK[x])

        # Pick an ion for spin prediction
        spin_ions = [k for k, v in self.TRANSITION_METALS.items()
                     if 4 <= v["d_electrons"] <= 7]
        ion = self._rng.choice(spin_ions)
        # Use the last (strongest) chosen ligand for prediction
        strongest = ordered[-1]
        rank = self.LIGAND_RANK[strongest]
        # Rough threshold: rank >= 6 (NH3 and above) -> low-spin
        predicted_spin = "low-spin" if rank >= 6 else "high-spin"

        ligand_str = ", ".join(chosen)
        return (
            f"order by field strength: {ligand_str}. "
            f"Predict spin for {ion} with {strongest}.",
            {"chosen": chosen, "ordered": ordered,
             "ion": ion, "strongest": strongest,
             "predicted_spin": predicted_spin},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        order_str = " < ".join(sd["ordered"])
        return [
            f"spectrochemical order: {order_str}",
            f"strongest field ligand: {sd['strongest']}",
            f"{sd['ion']} with {sd['strongest']}: {sd['predicted_spin']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Ordered ligands and spin prediction.
        """
        order_str = " < ".join(sd["ordered"])
        return f"order: {order_str}, spin: {sd['predicted_spin']}"


@register
class MagneticMomentGenerator(InorganicChemistryBase):
    """Compute spin-only magnetic moment from unpaired electron count.

    Uses the formula mu = sqrt(n(n+2)) Bohr magnetons where n is
    the number of unpaired electrons determined from the d-electron
    configuration and spin state.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnetic_moment"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["crystal_field"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute spin-only magnetic moment"

    def _unpaired_electrons(self, d_count: int,
                            high_spin: bool) -> int:
        """Count unpaired electrons for an octahedral complex.

        Args:
            d_count: Number of d electrons.
            high_spin: Whether the complex is high-spin.

        Returns:
            Number of unpaired electrons.
        """
        if high_spin:
            if d_count <= 5:
                return d_count
            return 10 - d_count
        # Low-spin: fill t2g first (capacity 6)
        if d_count <= 3:
            return d_count
        if d_count == 4:
            return 2
        if d_count == 5:
            return 1
        if d_count == 6:
            return 0
        if d_count == 7:
            return 1
        return 10 - d_count

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a magnetic moment calculation problem.

        Selects a metal ion and spin state, then computes the
        spin-only magnetic moment.

        Args:
            difficulty: Controls ion variety and spin state.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ions = list(self.TRANSITION_METALS.keys())
        ion = self._rng.choice(ions)
        d_count = self.TRANSITION_METALS[ion]["d_electrons"]

        if 4 <= d_count <= 7:
            high_spin = self._rng.choice([True, False])
        else:
            high_spin = True

        spin_label = "high-spin" if high_spin else "low-spin"
        n = self._unpaired_electrons(d_count, high_spin)
        mu = round(math.sqrt(n * (n + 2)), 4)

        return (
            f"spin-only magnetic moment of {ion} "
            f"({spin_label}, octahedral)",
            {"ion": ion, "d_count": d_count, "spin_label": spin_label,
             "n": n, "mu": mu},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"{sd['ion']}: {sd['d_count']} d-electrons, {sd['spin_label']}",
            f"unpaired electrons n = {sd['n']}",
            f"mu = sqrt(n(n+2)) = sqrt({sd['n']}*{sd['n'] + 2})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Magnetic moment in Bohr magnetons.
        """
        return f"mu = {sd['mu']} BM"


@register
class SolubilityProductGenerator(InorganicChemistryBase):
    """Compute Ksp from ion concentrations and predict precipitation.

    Given ion concentrations, computes the reaction quotient Q and
    compares it to Ksp to predict whether precipitation occurs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "solubility_product"

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
        return "compute Ksp and predict precipitation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a solubility product problem.

        Selects a salt, generates ion concentrations, computes Q,
        and compares to Ksp.

        Args:
            difficulty: Controls salt complexity and concentration range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SOLUBILITY_PRODUCTS), 2 + difficulty)
        entry = self._rng.choice(self.SOLUBILITY_PRODUCTS[:pool_size])

        # Generate concentrations that sometimes exceed Ksp
        concentrations = []
        q_value = 1.0
        for ion_name, stoich in entry["ions"]:
            # Scale concentration so Q is in the right ballpark of Ksp
            base_conc = entry["ksp"] ** (1.0 / sum(
                s for _, s in entry["ions"]
            ))
            factor = self._rng.uniform(0.3, 3.0)
            conc = round(base_conc * factor, 4)
            if conc < 1e-15:
                conc = round(self._rng.uniform(1e-6, 1e-3), 4)
            concentrations.append((ion_name, stoich, conc))
            q_value *= conc ** stoich

        q_value = round(q_value, 4)
        ksp = entry["ksp"]
        precipitates = q_value > ksp

        conc_parts = ", ".join(
            f"[{name}] = {conc}" for name, _, conc in concentrations
        )
        return (
            f"{entry['dissociation']}. {conc_parts}. "
            f"Ksp = {ksp:.2e}. Will it precipitate?",
            {"salt": entry["salt"], "dissociation": entry["dissociation"],
             "ksp": ksp, "concentrations": concentrations,
             "q_value": q_value, "precipitates": precipitates},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        q_parts = " * ".join(
            f"[{name}]^{stoich}" for name, stoich, _ in sd["concentrations"]
        )
        q_calc = " * ".join(
            f"{conc}^{stoich}"
            for _, stoich, conc in sd["concentrations"]
        )
        verdict = "precipitates" if sd["precipitates"] else "no precipitate"
        return [
            f"Q = {q_parts}",
            f"Q = {q_calc} = {sd['q_value']:.4e}",
            f"Ksp = {sd['ksp']:.2e}",
            f"Q {'>' if sd['precipitates'] else '<='} Ksp: {verdict}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Q value and precipitation verdict.
        """
        verdict = "precipitates" if sd["precipitates"] else "no precipitate"
        return f"Q = {sd['q_value']:.4e}, {verdict}"
