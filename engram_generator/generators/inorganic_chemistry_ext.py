"""Extended inorganic chemistry generators -- lattice energy, band theory, HSAB, MO.

8 generators across tiers 4-5 covering lattice energy, ionic radius ratios,
band theory classification, complex nomenclature, trans effect, HSAB theory,
molecular orbital diagrams, and redox balancing.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Lattice Energy / Born-Lande (tier 5)
# ---------------------------------------------------------------------------

@register
class LatticeEnergyGenerator(StepGenerator):
    """Estimate lattice energy using the Born-Lande equation.

    U = -N_A * M * z+ * z- * e^2 / (4*pi*eps_0*r_0) * (1 - 1/n)
    where M is the Madelung constant and n is the Born exponent.
    """

    N_A = 6.022e23
    E_CHARGE = 1.602e-19
    EPS_0 = 8.854e-12
    PI = math.pi

    SALTS = [
        {"name": "NaCl", "M": 1.7476, "z_plus": 1, "z_minus": 1,
         "r0": 2.81e-10, "n": 8},
        {"name": "CsCl", "M": 1.7627, "z_plus": 1, "z_minus": 1,
         "r0": 3.56e-10, "n": 10.5},
        {"name": "MgO", "M": 1.7476, "z_plus": 2, "z_minus": 2,
         "r0": 2.10e-10, "n": 7},
        {"name": "CaF2", "M": 2.5194, "z_plus": 2, "z_minus": 1,
         "r0": 2.36e-10, "n": 8},
        {"name": "ZnS", "M": 1.6381, "z_plus": 2, "z_minus": 2,
         "r0": 2.36e-10, "n": 9},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lattice_energy"

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
        return "estimate lattice energy via Born-Lande equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lattice energy calculation problem.

        Selects a salt from the data table and computes the lattice
        energy using the Born-Lande equation.

        Args:
            difficulty: Controls salt pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SALTS), 2 + difficulty)
        salt = self._rng.choice(self.SALTS[:pool_size])

        coulomb = (
            self.N_A * salt["M"] * salt["z_plus"] * salt["z_minus"]
            * self.E_CHARGE ** 2
            / (4 * self.PI * self.EPS_0 * salt["r0"])
        )
        u = round(-coulomb * (1 - 1.0 / salt["n"]) / 1000, 4)  # kJ/mol

        return (
            f"{salt['name']}: M={salt['M']}, z+={salt['z_plus']}, "
            f"z-={salt['z_minus']}, r0={salt['r0']:.2e} m, n={salt['n']}. "
            f"Find lattice energy.",
            {"salt": salt, "u": u},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        s = sd["salt"]
        return [
            "U = -N_A*M*z+*z-*e^2/(4*pi*eps_0*r0)*(1-1/n)",
            f"M={s['M']}, z+={s['z_plus']}, z-={s['z_minus']}",
            f"r0={s['r0']:.2e} m, n={s['n']}",
            f"U = {sd['u']} kJ/mol",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Lattice energy as string.
        """
        return f"{sd['u']} kJ/mol"


# ---------------------------------------------------------------------------
# 2. Ionic Radius Ratio (tier 4)
# ---------------------------------------------------------------------------

@register
class IonicRadiusRatioGenerator(StepGenerator):
    """Predict coordination number from ionic radius ratio.

    r+/r- ranges: <0.155 -> CN=2, 0.155-0.225 -> CN=3,
    0.225-0.414 -> CN=4, 0.414-0.732 -> CN=6, >0.732 -> CN=8.
    """

    ION_RADII = [
        {"cation": "Li+", "r_plus": 76, "anion": "F-", "r_minus": 133},
        {"cation": "Na+", "r_plus": 102, "anion": "Cl-", "r_minus": 181},
        {"cation": "K+", "r_plus": 138, "anion": "Br-", "r_minus": 196},
        {"cation": "Cs+", "r_plus": 167, "anion": "Cl-", "r_minus": 181},
        {"cation": "Mg2+", "r_plus": 72, "anion": "O2-", "r_minus": 140},
        {"cation": "Ca2+", "r_plus": 100, "anion": "F-", "r_minus": 133},
        {"cation": "Ba2+", "r_plus": 135, "anion": "O2-", "r_minus": 140},
        {"cation": "Zn2+", "r_plus": 74, "anion": "S2-", "r_minus": 184},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ionic_radius_ratio"

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
        return "predict coordination from radius ratio"

    @staticmethod
    def _classify_ratio(ratio: float) -> tuple[int, str]:
        """Classify radius ratio into coordination number and geometry.

        Args:
            ratio: Cation-to-anion radius ratio.

        Returns:
            Tuple of (coordination_number, geometry_name).
        """
        if ratio < 0.155:
            return 2, "linear"
        if ratio < 0.225:
            return 3, "trigonal planar"
        if ratio < 0.414:
            return 4, "tetrahedral"
        if ratio < 0.732:
            return 6, "octahedral"
        return 8, "cubic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a radius ratio problem.

        Picks an ion pair, computes the ratio, and classifies
        the predicted coordination geometry.

        Args:
            difficulty: Controls ion pair pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.ION_RADII), 3 + difficulty)
        pair = self._rng.choice(self.ION_RADII[:pool_size])
        ratio = round(pair["r_plus"] / pair["r_minus"], 4)
        cn, geometry = self._classify_ratio(ratio)

        return (
            f"{pair['cation']} (r+={pair['r_plus']} pm), "
            f"{pair['anion']} (r-={pair['r_minus']} pm). "
            f"Predict coordination.",
            {"pair": pair, "ratio": ratio, "cn": cn, "geometry": geometry},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"r+/r- = {sd['pair']['r_plus']}/{sd['pair']['r_minus']} "
            f"= {sd['ratio']}",
            "ranges: <0.155->2, 0.155-0.225->3, 0.225-0.414->4, "
            "0.414-0.732->6, >0.732->8",
            f"ratio {sd['ratio']} -> CN={sd['cn']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Coordination number and geometry.
        """
        return f"CN={sd['cn']}, {sd['geometry']}"


# ---------------------------------------------------------------------------
# 3. Band Theory Classification (tier 5)
# ---------------------------------------------------------------------------

@register
class BandTheoryExtGenerator(StepGenerator):
    """Classify material as conductor, semiconductor, or insulator from band gap.

    Conductor: overlapping bands (gap ~0 eV).
    Semiconductor: small gap (<3 eV).
    Insulator: large gap (>3 eV).
    """

    MATERIALS = [
        {"name": "copper", "gap_eV": 0.0, "type": "conductor"},
        {"name": "silicon", "gap_eV": 1.12, "type": "semiconductor"},
        {"name": "germanium", "gap_eV": 0.67, "type": "semiconductor"},
        {"name": "diamond", "gap_eV": 5.47, "type": "insulator"},
        {"name": "GaAs", "gap_eV": 1.42, "type": "semiconductor"},
        {"name": "SiO2", "gap_eV": 9.0, "type": "insulator"},
        {"name": "InP", "gap_eV": 1.34, "type": "semiconductor"},
        {"name": "aluminum", "gap_eV": 0.0, "type": "conductor"},
        {"name": "GaN", "gap_eV": 3.4, "type": "insulator"},
        {"name": "tin (grey)", "gap_eV": 0.08, "type": "semiconductor"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "band_theory_ext"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "classify material by band gap"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a band theory classification problem.

        Selects a material and asks for classification based on band gap.

        Args:
            difficulty: Controls material pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.MATERIALS), 4 + difficulty)
        mat = self._rng.choice(self.MATERIALS[:pool_size])

        return (
            f"{mat['name']}: band gap = {mat['gap_eV']} eV. Classify.",
            {"mat": mat},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        mat = sd["mat"]
        return [
            f"band gap = {mat['gap_eV']} eV",
            "0 eV: conductor, <3 eV: semiconductor, >3 eV: insulator",
            f"{mat['gap_eV']} eV -> {mat['type']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Material classification.
        """
        return sd["mat"]["type"]


# ---------------------------------------------------------------------------
# 4. Nomenclature of Coordination Compounds (tier 4)
# ---------------------------------------------------------------------------

@register
class NomenclatureComplexGenerator(StepGenerator):
    """Name coordination compounds following IUPAC nomenclature.

    Template-based: given a formula, constructs the systematic name
    using ligand prefixes, metal name, and oxidation state.
    """

    COMPLEXES = [
        {"formula": "[Fe(CN)6]4-", "name": "hexacyanoferrate(II)",
         "metal": "Fe", "ox": 2, "ligands": [("CN-", 6, "cyanido")]},
        {"formula": "[Co(NH3)6]3+", "name": "hexaamminecobalt(III)",
         "metal": "Co", "ox": 3, "ligands": [("NH3", 6, "ammine")]},
        {"formula": "[Cr(H2O)6]3+", "name": "hexaaquachromium(III)",
         "metal": "Cr", "ox": 3, "ligands": [("H2O", 6, "aqua")]},
        {"formula": "[PtCl4]2-", "name": "tetrachloridoplatinate(II)",
         "metal": "Pt", "ox": 2, "ligands": [("Cl-", 4, "chlorido")]},
        {"formula": "[Ni(CO)4]", "name": "tetracarbonylnickel(0)",
         "metal": "Ni", "ox": 0, "ligands": [("CO", 4, "carbonyl")]},
        {"formula": "[Cu(NH3)4]2+", "name": "tetraamminecopper(II)",
         "metal": "Cu", "ox": 2, "ligands": [("NH3", 4, "ammine")]},
        {"formula": "[Ag(NH3)2]+", "name": "diamminesilver(I)",
         "metal": "Ag", "ox": 1, "ligands": [("NH3", 2, "ammine")]},
        {"formula": "[Fe(H2O)6]2+", "name": "hexaaquairon(II)",
         "metal": "Fe", "ox": 2, "ligands": [("H2O", 6, "aqua")]},
    ]

    PREFIXES = {1: "", 2: "di", 3: "tri", 4: "tetra",
                5: "penta", 6: "hexa"}

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nomenclature_complex"

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
        return "name coordination compound (IUPAC)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nomenclature problem.

        Selects a coordination compound and asks for its IUPAC name.

        Args:
            difficulty: Controls compound pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPLEXES), 3 + difficulty)
        cplx = self._rng.choice(self.COMPLEXES[:pool_size])

        lig_parts = []
        for _, count, lig_name in cplx["ligands"]:
            prefix = self.PREFIXES.get(count, str(count))
            lig_parts.append(f"{prefix}{lig_name}")

        return (
            f"Name the compound: {cplx['formula']}",
            {"cplx": cplx, "lig_parts": lig_parts},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        cplx = sd["cplx"]
        steps = [f"metal: {cplx['metal']}, oxidation state: +{cplx['ox']}"]
        for lig, count, lig_name in cplx["ligands"]:
            steps.append(f"ligand: {count} x {lig} -> {lig_name}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            IUPAC name of the compound.
        """
        return sd["cplx"]["name"]


# ---------------------------------------------------------------------------
# 5. Trans Effect (tier 5)
# ---------------------------------------------------------------------------

@register
class TransEffectGenerator(StepGenerator):
    """Predict substitution position using the trans effect series.

    Trans effect ordering: CN- > CO > NO2- > NH3 > Cl- > H2O.
    The ligand with the strongest trans effect directs substitution
    trans to itself in square planar complexes.
    """

    TRANS_SERIES = ["H2O", "Cl-", "NH3", "NO2-", "CO", "CN-"]
    TRANS_RANK = {lig: i for i, lig in enumerate(TRANS_SERIES)}

    SCENARIOS = [
        {"complex": "cis-[Pt(NH3)2Cl2]",
         "incoming": "py",
         "trans_to": "Cl-",
         "replaced": "Cl-",
         "product": "[Pt(NH3)2(py)Cl]+",
         "reason": "Cl- has stronger trans effect than NH3"},
        {"complex": "trans-[Pt(NH3)2Cl2]",
         "incoming": "py",
         "trans_to": "Cl-",
         "replaced": "NH3",
         "product": "[Pt(NH3)(py)Cl2]",
         "reason": "Cl- trans directs; NH3 trans to Cl- is replaced"},
        {"complex": "[Pt(NH3)Cl3]-",
         "incoming": "NH3",
         "trans_to": "Cl-",
         "replaced": "Cl- trans to Cl-",
         "product": "cis-[Pt(NH3)2Cl2]",
         "reason": "Cl- has stronger trans effect, NH3 enters trans to Cl-"},
        {"complex": "[PtCl4]2-",
         "incoming": "NH3",
         "trans_to": "Cl-",
         "replaced": "Cl-",
         "product": "[Pt(NH3)Cl3]-",
         "reason": "all Cl-, one replaced by NH3"},
        {"complex": "cis-[Pt(NH3)2Cl2]",
         "incoming": "NO2-",
         "trans_to": "Cl-",
         "replaced": "Cl-",
         "product": "[Pt(NH3)2(NO2)Cl]",
         "reason": "Cl- has stronger trans effect than NH3"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trans_effect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "predict substitution via trans effect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trans effect problem.

        Selects a square planar complex and an incoming ligand, then
        predicts which ligand is replaced based on the trans effect.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SCENARIOS), 2 + difficulty)
        scenario = self._rng.choice(self.SCENARIOS[:pool_size])

        return (
            f"{scenario['complex']} + {scenario['incoming']}. "
            f"Predict product.",
            {"scenario": scenario},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        sc = sd["scenario"]
        return [
            "trans effect: CN- > CO > NO2- > NH3 > Cl- > H2O",
            f"strongest trans ligand directs substitution",
            sc["reason"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Product of the substitution.
        """
        return sd["scenario"]["product"]


# ---------------------------------------------------------------------------
# 6. Hard-Soft Acid-Base (HSAB) (tier 5)
# ---------------------------------------------------------------------------

@register
class HardSoftAcidBaseGenerator(StepGenerator):
    """Classify ions and predict reaction products using HSAB theory.

    Hard acids prefer hard bases, soft acids prefer soft bases.
    Given an acid and two bases (or vice versa), predicts which
    pair forms the more stable compound.
    """

    ACIDS = {
        "hard": ["Li+", "Na+", "K+", "Mg2+", "Ca2+", "Al3+",
                 "Ti4+", "Fe3+", "Cr3+", "H+"],
        "borderline": ["Fe2+", "Cu2+", "Zn2+", "Ni2+", "Pb2+"],
        "soft": ["Cu+", "Ag+", "Au+", "Hg2+", "Pd2+", "Pt2+", "Cd2+"],
    }

    BASES = {
        "hard": ["F-", "OH-", "H2O", "NH3", "Cl-", "NO3-", "SO4^2-"],
        "borderline": ["Br-", "NO2-", "N3-", "SO3^2-"],
        "soft": ["I-", "SCN-", "CN-", "CO", "S2-", "RS-", "PPh3"],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hard_soft_acid_base"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "classify and predict via HSAB theory"

    def _classify(self, species: str) -> str:
        """Classify a species as hard, borderline, or soft.

        Args:
            species: Ion or molecule name.

        Returns:
            Classification string.
        """
        for cat, members in self.ACIDS.items():
            if species in members:
                return cat
        for cat, members in self.BASES.items():
            if species in members:
                return cat
        return "unknown"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an HSAB prediction problem.

        Picks an acid and two bases of different hardness, and predicts
        which base forms the more stable product.

        Args:
            difficulty: Controls category mixing.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        acid_cat = self._rng.choice(["hard", "soft"])
        acid = self._rng.choice(self.ACIDS[acid_cat])

        matching_cat = acid_cat
        non_matching = "soft" if acid_cat == "hard" else "hard"

        base_match = self._rng.choice(self.BASES[matching_cat])
        base_other = self._rng.choice(self.BASES[non_matching])

        preferred = base_match
        reason = f"{acid_cat} acid {acid} prefers {matching_cat} base"

        return (
            f"acid: {acid} ({acid_cat}). "
            f"Bases: {base_match}, {base_other}. "
            f"Which forms more stable product?",
            {"acid": acid, "acid_cat": acid_cat,
             "base_match": base_match, "base_other": base_other,
             "preferred": preferred, "reason": reason},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"acid: {sd['acid']} -> {sd['acid_cat']}",
            f"base {sd['base_match']} -> {self._classify(sd['base_match'])}",
            f"base {sd['base_other']} -> {self._classify(sd['base_other'])}",
            "HSAB: like prefers like",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Preferred base and reason.
        """
        return f"{sd['preferred']}: {sd['reason']}"


# ---------------------------------------------------------------------------
# 7. Molecular Orbital Diagram (tier 5)
# ---------------------------------------------------------------------------

@register
class MolecularOrbitalDiagramGenerator(StepGenerator):
    """Construct MO diagram for homonuclear diatomics and find bond order.

    Bond order = (bonding electrons - antibonding electrons) / 2.
    Covers O2, N2, F2, C2, B2, Be2, Li2, Ne2.
    """

    # For Z <= 7 (up to N2): sigma_2s, sigma*_2s, pi_2p, sigma_2p, pi*_2p, sigma*_2p
    # For Z >= 8 (O2, F2): sigma_2s, sigma*_2s, sigma_2p, pi_2p, pi*_2p, sigma*_2p

    DIATOMICS = [
        {"molecule": "Li2", "total_e": 6,
         "bonding": 4, "antibonding": 2, "bond_order": 1.0,
         "magnetic": "diamagnetic"},
        {"molecule": "Be2", "total_e": 8,
         "bonding": 4, "antibonding": 4, "bond_order": 0.0,
         "magnetic": "diamagnetic"},
        {"molecule": "B2", "total_e": 10,
         "bonding": 6, "antibonding": 4, "bond_order": 1.0,
         "magnetic": "paramagnetic"},
        {"molecule": "C2", "total_e": 12,
         "bonding": 8, "antibonding": 4, "bond_order": 2.0,
         "magnetic": "diamagnetic"},
        {"molecule": "N2", "total_e": 14,
         "bonding": 10, "antibonding": 4, "bond_order": 3.0,
         "magnetic": "diamagnetic"},
        {"molecule": "O2", "total_e": 16,
         "bonding": 10, "antibonding": 6, "bond_order": 2.0,
         "magnetic": "paramagnetic"},
        {"molecule": "F2", "total_e": 18,
         "bonding": 10, "antibonding": 8, "bond_order": 1.0,
         "magnetic": "diamagnetic"},
        {"molecule": "Ne2", "total_e": 20,
         "bonding": 10, "antibonding": 10, "bond_order": 0.0,
         "magnetic": "diamagnetic"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "molecular_orbital_diagram"

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
        return "determine bond order from MO diagram"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a molecular orbital diagram problem.

        Selects a homonuclear diatomic and asks for bond order and
        magnetic character.

        Args:
            difficulty: Controls molecule pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.DIATOMICS), 3 + difficulty)
        mol = self._rng.choice(self.DIATOMICS[:pool_size])

        return (
            f"MO diagram of {mol['molecule']} "
            f"({mol['total_e']} electrons): "
            f"bond order and magnetism?",
            {"mol": mol},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        mol = sd["mol"]
        return [
            f"total electrons: {mol['total_e']}",
            f"bonding electrons: {mol['bonding']}",
            f"antibonding electrons: {mol['antibonding']}",
            f"BO = ({mol['bonding']} - {mol['antibonding']}) / 2",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Bond order and magnetic character.
        """
        mol = sd["mol"]
        return f"BO={mol['bond_order']}, {mol['magnetic']}"


# ---------------------------------------------------------------------------
# 8. Redox Balancing (tier 5)
# ---------------------------------------------------------------------------

@register
class RedoxBalancingGenerator(StepGenerator):
    """Balance redox reactions in acidic or basic solution.

    Splits the reaction into oxidation and reduction half-reactions,
    balances atoms and charge, then combines. Template-based with
    curated half-reaction pairs.
    """

    REDOX_REACTIONS = [
        {
            "medium": "acidic",
            "overall": "MnO4- + Fe2+ -> Mn2+ + Fe3+",
            "oxidation": "Fe2+ -> Fe3+ + e-",
            "reduction": "MnO4- + 8H+ + 5e- -> Mn2+ + 4H2O",
            "balanced": "MnO4- + 8H+ + 5Fe2+ -> Mn2+ + 5Fe3+ + 4H2O",
        },
        {
            "medium": "acidic",
            "overall": "Cr2O7^2- + Fe2+ -> Cr3+ + Fe3+",
            "oxidation": "Fe2+ -> Fe3+ + e-",
            "reduction": "Cr2O7^2- + 14H+ + 6e- -> 2Cr3+ + 7H2O",
            "balanced": "Cr2O7^2- + 14H+ + 6Fe2+ -> 2Cr3+ + 6Fe3+ + 7H2O",
        },
        {
            "medium": "basic",
            "overall": "MnO4- + I- -> MnO2 + IO3-",
            "oxidation": "I- + 6OH- -> IO3- + 3H2O + 6e-",
            "reduction": "MnO4- + 2H2O + 3e- -> MnO2 + 4OH-",
            "balanced": "2MnO4- + I- + H2O -> 2MnO2 + IO3- + 2OH-",
        },
        {
            "medium": "acidic",
            "overall": "Cu + NO3- -> Cu2+ + NO",
            "oxidation": "Cu -> Cu2+ + 2e-",
            "reduction": "NO3- + 4H+ + 3e- -> NO + 2H2O",
            "balanced": "3Cu + 2NO3- + 8H+ -> 3Cu2+ + 2NO + 4H2O",
        },
        {
            "medium": "basic",
            "overall": "Al + MnO4- -> Al(OH)4- + MnO2",
            "oxidation": "Al + 4OH- -> Al(OH)4- + 3e-",
            "reduction": "MnO4- + 2H2O + 3e- -> MnO2 + 4OH-",
            "balanced": "Al + MnO4- + 2H2O -> Al(OH)4- + MnO2",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "redox_balancing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "balance redox reaction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a redox balancing problem.

        Selects a redox reaction and asks for the balanced equation.

        Args:
            difficulty: Controls reaction pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REDOX_REACTIONS), 2 + difficulty)
        rxn = self._rng.choice(self.REDOX_REACTIONS[:pool_size])

        return (
            f"Balance in {rxn['medium']} solution: {rxn['overall']}",
            {"rxn": rxn},
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
            f"oxidation half: {rxn['oxidation']}",
            f"reduction half: {rxn['reduction']}",
            "balance electrons, combine half-reactions",
            f"medium: {rxn['medium']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Balanced equation.
        """
        return sd["rxn"]["balanced"]
