"""Deep spectroscopy generators -- NMR depth, mass spec, Raman, UV-Vis.

8 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class SpectroscopyDeepBase(StepGenerator):
    """Base class for deep spectroscopy generators with shared data.

    Provides NMR chemical shift ranges, isotope abundance data,
    and IR/Raman selection rules used across multiple generators.
    """

    SHIFT_RANGES = [
        (0.0, 2.0, "alkyl (C-H)"),
        (2.0, 4.5, "next to heteroatom or carbonyl"),
        (4.5, 6.5, "alkene (=C-H)"),
        (6.0, 8.5, "aromatic"),
        (9.0, 10.0, "aldehyde (CHO)"),
        (10.0, 12.0, "carboxylic acid (COOH)"),
    ]

    IR_PEAKS = [
        (3200, 3550, "broad", "O-H stretch (alcohol/carboxylic acid)"),
        (3300, 3500, "medium", "N-H stretch (amine)"),
        (3300, 3320, "sharp", "alkyne C-H stretch"),
        (2850, 3000, "strong", "C-H stretch (alkane)"),
        (2100, 2260, "medium", "C#C or C#N stretch"),
        (1700, 1750, "strong", "C=O stretch (ester/carboxylic acid)"),
        (1680, 1710, "strong", "C=O stretch (amide/aldehyde/ketone)"),
        (1600, 1680, "variable", "C=C stretch"),
        (2500, 3300, "broad", "O-H stretch (carboxylic acid)"),
        (1000, 1300, "strong", "C-O stretch"),
    ]


@register
class NmrChemicalShiftGenerator(SpectroscopyDeepBase):
    """Compute and classify NMR chemical shift.

    delta = (nu_sample - nu_ref) / nu_ref * 10^6 ppm. Classifies
    the shift into functional group region (alkyl, heteroatom-adjacent,
    aromatic, aldehyde, etc.).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nmr_chemical_shift"

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
        return "compute NMR chemical shift and classify environment"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NMR chemical shift problem.

        Creates a sample frequency relative to a TMS reference,
        computes the chemical shift in ppm, and classifies it.

        Args:
            difficulty: Controls operating frequency and shift range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Operating frequency in MHz
        freq_mhz = self._rng.choice([60, 100, 200, 300, 400, 500, 600])
        nu_ref = freq_mhz * 1e6  # Hz

        pool_size = min(len(self.SHIFT_RANGES), 3 + difficulty)
        low, high, classification = self._rng.choice(
            self.SHIFT_RANGES[:pool_size]
        )
        target_ppm = round(self._rng.uniform(low + 0.1, high - 0.1), 4)

        nu_sample = round(nu_ref + target_ppm * nu_ref / 1e6, 2)
        delta_hz = round(nu_sample - nu_ref, 2)
        delta_ppm = round(delta_hz / nu_ref * 1e6, 4)

        desc = (
            f"Spectrometer: {freq_mhz} MHz. "
            f"nu_sample={nu_sample} Hz, nu_ref={nu_ref:.0f} Hz. "
            f"Find delta (ppm) and classify."
        )
        return desc, {
            "freq_mhz": freq_mhz, "nu_ref": nu_ref,
            "nu_sample": nu_sample, "delta_hz": delta_hz,
            "delta_ppm": delta_ppm,
            "classification": classification,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "delta = (nu_sample - nu_ref) / nu_ref * 10^6",
            f"delta_hz = {sd['nu_sample']} - {sd['nu_ref']:.0f} = {sd['delta_hz']}",
            f"delta = {sd['delta_hz']} / {sd['nu_ref']:.0f} * 10^6 = {sd['delta_ppm']} ppm",
            f"region: {sd['classification']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the chemical shift and classification.

        Args:
            sd: Solution data dict.

        Returns:
            Delta in ppm with region.
        """
        return f"delta = {sd['delta_ppm']} ppm, {sd['classification']}"


@register
class NmrIntegrationGenerator(SpectroscopyDeepBase):
    """Determine proton count per peak from NMR integral ratios.

    Given raw integration values for each peak, reduces to the
    simplest whole-number ratio and assigns H counts consistent
    with the molecular formula.
    """

    MOLECULES = [
        {"formula": "C2H6O", "total_H": 6, "n_peaks": 3,
         "ratios": [3, 2, 1], "groups": ["CH3", "CH2", "OH"]},
        {"formula": "C3H8O", "total_H": 8, "n_peaks": 3,
         "ratios": [6, 1, 1], "groups": ["2xCH3", "CH", "OH"]},
        {"formula": "C2H4O2", "total_H": 4, "n_peaks": 2,
         "ratios": [3, 1], "groups": ["CH3", "COOH"]},
        {"formula": "C3H6O", "total_H": 6, "n_peaks": 2,
         "ratios": [3, 3], "groups": ["CH3", "COCH3"]},
        {"formula": "C4H10", "total_H": 10, "n_peaks": 2,
         "ratios": [9, 1], "groups": ["3xCH3", "CH"]},
        {"formula": "C2H5Cl", "total_H": 5, "n_peaks": 2,
         "ratios": [3, 2], "groups": ["CH3", "CH2"]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nmr_integration"

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
        return "determine proton count from NMR integration ratios"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NMR integration problem.

        Selects a molecule, scales the ideal ratios by a random factor
        to create realistic raw integrals, then asks for the H count
        per peak.

        Args:
            difficulty: Controls molecule complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.MOLECULES), 3 + difficulty)
        mol = self._rng.choice(self.MOLECULES[:pool_size])

        scale = round(self._rng.uniform(5.0, 25.0), 2)
        raw_integrals = [round(r * scale, 2) for r in mol["ratios"]]

        gcd_val = mol["ratios"][0]
        for r in mol["ratios"][1:]:
            gcd_val = math.gcd(gcd_val, r)
        reduced = [r // gcd_val for r in mol["ratios"]]

        integral_str = ", ".join(
            f"peak {i + 1}: {v}" for i, v in enumerate(raw_integrals)
        )
        desc = (
            f"Molecule {mol['formula']} ({mol['total_H']} H). "
            f"Integrals: {integral_str}. Find H per peak."
        )
        return desc, {
            "formula": mol["formula"], "total_H": mol["total_H"],
            "raw_integrals": raw_integrals, "ratios": mol["ratios"],
            "reduced": reduced, "groups": mol["groups"],
            "scale": scale, "gcd": gcd_val,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        smallest = min(sd["raw_integrals"])
        norm = [round(v / smallest, 2) for v in sd["raw_integrals"]]
        steps = [
            f"normalise by smallest integral ({smallest})",
            f"ratios: {norm}",
            f"simplest whole-number ratio: {sd['reduced']}",
            f"total ratio units = {sum(sd['reduced'])}, total H = {sd['total_H']}",
        ]
        scale_h = sd["total_H"] / sum(sd["reduced"])
        h_counts = [round(r * scale_h) for r in sd["reduced"]]
        steps.append(f"H per peak: {h_counts}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the proton counts per peak.

        Args:
            sd: Solution data dict.

        Returns:
            H counts with group assignments.
        """
        pairs = ", ".join(
            f"{sd['ratios'][i]}H ({sd['groups'][i]})"
            for i in range(len(sd["ratios"]))
        )
        return pairs


@register
class MassSpecMolecularIonGenerator(SpectroscopyDeepBase):
    """Analyse molecular ion peak and apply the nitrogen rule.

    M+ peak gives the molecular weight. M+1 peak arises from 13C.
    Nitrogen rule: odd MW implies an odd number of nitrogen atoms.
    """

    COMPOUNDS = [
        {"name": "aniline", "formula": "C6H7N", "MW": 93, "N_count": 1},
        {"name": "acetone", "formula": "C3H6O", "MW": 58, "N_count": 0},
        {"name": "pyridine", "formula": "C5H5N", "MW": 79, "N_count": 1},
        {"name": "ethanol", "formula": "C2H6O", "MW": 46, "N_count": 0},
        {"name": "urea", "formula": "CH4N2O", "MW": 60, "N_count": 2},
        {"name": "glycine", "formula": "C2H5NO2", "MW": 75, "N_count": 1},
        {"name": "butane", "formula": "C4H10", "MW": 58, "N_count": 0},
        {"name": "dimethylamine", "formula": "C2H7N", "MW": 45, "N_count": 1},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_spec_molecular_ion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "analyse molecular ion peak and apply nitrogen rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a molecular ion mass spec problem.

        Gives the M+ peak and asks for molecular weight identification
        and nitrogen rule analysis.

        Args:
            difficulty: Controls compound pool size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPOUNDS), 4 + difficulty)
        comp = self._rng.choice(self.COMPOUNDS[:pool_size])

        mw = comp["MW"]
        odd_mw = mw % 2 == 1
        odd_n = comp["N_count"] % 2 == 1
        n_rule = "odd MW => odd number of N" if odd_mw else "even MW => even number of N (or zero)"

        # M+1 from 13C: approximate relative intensity
        n_carbons = comp["formula"].count("C")
        if "C" in comp["formula"]:
            idx = comp["formula"].index("C")
            # Parse carbon count
            rest = comp["formula"][idx + 1:]
            c_count_str = ""
            for ch in rest:
                if ch.isdigit():
                    c_count_str += ch
                else:
                    break
            n_carbons = int(c_count_str) if c_count_str else 1

        m_plus_1_pct = round(n_carbons * 1.1, 4)

        desc = (
            f"Mass spectrum: M+ = {mw}. "
            f"Apply nitrogen rule and predict M+1 intensity."
        )
        return desc, {
            "name": comp["name"], "formula": comp["formula"],
            "MW": mw, "N_count": comp["N_count"],
            "odd_mw": odd_mw, "n_rule": n_rule,
            "n_carbons": n_carbons, "m_plus_1_pct": m_plus_1_pct,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        parity = "odd" if sd["odd_mw"] else "even"
        return [
            f"M+ = {sd['MW']}, MW is {parity}",
            f"nitrogen rule: {sd['n_rule']}",
            f"N count = {sd['N_count']} (consistent: {'yes' if (sd['odd_mw'] == (sd['N_count'] % 2 == 1)) else 'no'})",
            f"M+1 ~ {sd['n_carbons']} * 1.1% = {sd['m_plus_1_pct']}%",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the MW and nitrogen rule conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            MW, N count, and M+1 intensity.
        """
        return (
            f"MW={sd['MW']}, {sd['N_count']} N atoms, "
            f"M+1={sd['m_plus_1_pct']}%"
        )


@register
class IrInterpretationGenerator(SpectroscopyDeepBase):
    """Identify functional groups from multiple IR absorption peaks.

    Given 2-4 IR peaks with their frequencies and intensities, assigns
    each to a functional group and identifies the compound class.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ir_interpretation"

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
        return "identify functional groups from IR spectrum peaks"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IR interpretation problem.

        Selects 2-4 IR peaks from the database and asks for
        functional group assignments.

        Args:
            difficulty: Controls number of peaks to interpret.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_peaks = min(2 + difficulty // 2, 4)
        pool_size = min(len(self.IR_PEAKS), 5 + difficulty)
        chosen = self._rng.sample(self.IR_PEAKS[:pool_size], n_peaks)

        peaks = []
        for low, high, intensity, group in chosen:
            freq = self._rng.randint(low, high)
            peaks.append({
                "freq": freq, "intensity": intensity, "group": group,
            })

        peak_str = ", ".join(
            f"{p['freq']} cm^-1 ({p['intensity']})" for p in peaks
        )
        desc = f"IR peaks: {peak_str}. Identify all functional groups."
        return desc, {"peaks": peaks}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = []
        for p in sd["peaks"]:
            steps.append(f"{p['freq']} cm^-1: {p['group']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return all identified functional groups.

        Args:
            sd: Solution data dict.

        Returns:
            Comma-separated functional groups.
        """
        groups = [p["group"] for p in sd["peaks"]]
        return "; ".join(groups)


@register
class UvVisAbsorptionGenerator(SpectroscopyDeepBase):
    """Compute UV-Vis absorption and concentration from Beer-Lambert.

    Estimates lambda_max from conjugation length (each additional
    conjugated double bond adds ~30 nm). Then applies Beer-Lambert
    to compute concentration from absorbance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "uv_vis_absorption"

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
        return "compute UV-Vis absorption wavelength and concentration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a UV-Vis absorption problem.

        At low difficulty, estimates lambda_max from conjugation.
        At higher difficulty, also applies Beer-Lambert to find
        concentration from measured absorbance.

        Args:
            difficulty: Controls whether Beer-Lambert is included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        base_lambda = 217  # nm for butadiene (2 conjugated C=C)
        extra_bonds = self._rng.randint(0, min(6, 1 + difficulty))
        increment = 30  # nm per additional conjugated C=C
        lambda_max = base_lambda + extra_bonds * increment
        total_bonds = 2 + extra_bonds

        sd = {
            "base_lambda": base_lambda, "extra_bonds": extra_bonds,
            "increment": increment, "lambda_max": lambda_max,
            "total_bonds": total_bonds, "mode": "conjugation",
        }

        if difficulty > 4:
            epsilon = round(self._rng.uniform(1000.0, 50000.0), 4)
            path_length = round(self._rng.uniform(0.5, 2.0), 4)
            absorbance = round(self._rng.uniform(0.1, 2.0), 4)
            concentration = round(absorbance / (epsilon * path_length), 4)

            sd.update({
                "mode": "beer_lambert",
                "epsilon": epsilon, "path_length": path_length,
                "absorbance": absorbance, "concentration": concentration,
            })
            desc = (
                f"Conjugated system: {total_bonds} C=C bonds. "
                f"A={absorbance}, epsilon={epsilon}, l={path_length} cm. "
                f"Find lambda_max and concentration."
            )
        else:
            desc = (
                f"Conjugated system with {total_bonds} conjugated C=C bonds "
                f"(base: butadiene at {base_lambda} nm, +{increment} nm/bond). "
                f"Find lambda_max."
            )

        return desc, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            f"base lambda_max = {sd['base_lambda']} nm (2 C=C)",
            f"extra bonds = {sd['extra_bonds']}",
            f"lambda_max = {sd['base_lambda']} + {sd['extra_bonds']} * {sd['increment']} = {sd['lambda_max']} nm",
        ]
        if sd["mode"] == "beer_lambert":
            steps.extend([
                "c = A / (epsilon * l)",
                f"c = {sd['absorbance']} / ({sd['epsilon']} * {sd['path_length']})",
            ])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return lambda_max and optionally concentration.

        Args:
            sd: Solution data dict.

        Returns:
            Lambda_max in nm, optionally with concentration.
        """
        ans = f"lambda_max = {sd['lambda_max']} nm"
        if sd["mode"] == "beer_lambert":
            ans += f", c = {sd['concentration']} M"
        return ans


@register
class CouplingConstantGenerator(SpectroscopyDeepBase):
    """Classify NMR J-coupling type from coupling constant value.

    3-bond vicinal coupling: 6-8 Hz typical. 2-bond geminal coupling:
    12-15 Hz. Long-range (4-bond): 1-3 Hz. Given J, identifies the
    coupling type and predicts structural relationship.
    """

    COUPLING_TYPES = [
        {"type": "geminal (2-bond)", "j_min": 12.0, "j_max": 15.0},
        {"type": "vicinal (3-bond)", "j_min": 6.0, "j_max": 8.0},
        {"type": "long-range (4-bond)", "j_min": 1.0, "j_max": 3.0},
        {"type": "trans-alkene vicinal", "j_min": 14.0, "j_max": 18.0},
        {"type": "cis-alkene vicinal", "j_min": 8.0, "j_max": 12.0},
        {"type": "ortho-aromatic", "j_min": 6.0, "j_max": 10.0},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coupling_constant"

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
        return "classify NMR J-coupling from coupling constant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coupling constant classification problem.

        Selects a coupling type, generates a J value within range,
        and asks for classification.

        Args:
            difficulty: Controls the variety of coupling types.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COUPLING_TYPES), 3 + difficulty)
        coupling = self._rng.choice(self.COUPLING_TYPES[:pool_size])

        j_val = round(
            self._rng.uniform(coupling["j_min"], coupling["j_max"]), 4
        )

        desc = f"NMR coupling constant J = {j_val} Hz. Identify coupling type."
        return desc, {
            "j_val": j_val, "coupling_type": coupling["type"],
            "j_min": coupling["j_min"], "j_max": coupling["j_max"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"J = {sd['j_val']} Hz",
            f"range {sd['j_min']}-{sd['j_max']} Hz",
            f"coupling type: {sd['coupling_type']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the coupling type classification.

        Args:
            sd: Solution data dict.

        Returns:
            Coupling type name.
        """
        return f"J = {sd['j_val']} Hz, {sd['coupling_type']}"


@register
class MassSpecIsotopeGenerator(SpectroscopyDeepBase):
    """Identify halogen from mass spectrum isotope pattern.

    Cl produces M and M+2 in ~3:1 ratio. Br produces M and M+2
    in ~1:1 ratio. Given isotope pattern intensities, identifies
    the halogen and counts atoms.
    """

    HALOGENS = [
        {"element": "Cl", "ratio_m": 3.0, "ratio_m2": 1.0, "mass_diff": 2},
        {"element": "Br", "ratio_m": 1.0, "ratio_m2": 1.0, "mass_diff": 2},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_spec_isotope"

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
        return "identify halogen from mass spectrum isotope pattern"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass spec isotope pattern problem.

        Creates M and M+2 peak intensities matching Cl or Br patterns
        and asks for halogen identification.

        Args:
            difficulty: Controls number of halogen atoms.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        halogen = self._rng.choice(self.HALOGENS)
        n_atoms = 1 if difficulty <= 4 else self._rng.randint(1, 2)

        base_mw = self._rng.randint(50, 150 + 20 * difficulty)

        # Scale intensities with noise
        noise = round(self._rng.uniform(0.9, 1.1), 2)
        if halogen["element"] == "Cl":
            m_intensity = round(100.0 * noise, 2)
            m2_intensity = round(100.0 / 3.0 * n_atoms * noise, 2)
            ideal_ratio = round(m_intensity / m2_intensity, 4)
        else:
            m_intensity = round(100.0 * noise, 2)
            m2_intensity = round(100.0 * n_atoms * noise, 2)
            ideal_ratio = round(m_intensity / m2_intensity, 4)

        desc = (
            f"Mass spectrum: M={base_mw} (intensity={m_intensity}), "
            f"M+2 (intensity={m2_intensity}). "
            f"Identify halogen."
        )
        return desc, {
            "element": halogen["element"], "n_atoms": n_atoms,
            "base_mw": base_mw,
            "m_intensity": m_intensity, "m2_intensity": m2_intensity,
            "ratio": ideal_ratio,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"M/M+2 intensity ratio = {sd['m_intensity']}/{sd['m2_intensity']} = {sd['ratio']}",
            f"Cl pattern: ~3:1, Br pattern: ~1:1",
            f"ratio {sd['ratio']} => {sd['element']}",
            f"number of {sd['element']} atoms: {sd['n_atoms']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the halogen identification.

        Args:
            sd: Solution data dict.

        Returns:
            Halogen element and count.
        """
        return f"{sd['n_atoms']} {sd['element']} atom(s)"


@register
class RamanVsIrGenerator(SpectroscopyDeepBase):
    """Determine IR and Raman activity using selection rules.

    IR active: dipole moment changes during vibration. Raman active:
    polarisability changes. For centrosymmetric molecules, mutual
    exclusion applies (no mode is both IR and Raman active).
    """

    VIBRATIONS = [
        {
            "molecule": "CO2", "mode": "asymmetric stretch",
            "centrosymmetric": True, "ir": True, "raman": False,
            "reason": "dipole changes, no polarisability change",
        },
        {
            "molecule": "CO2", "mode": "symmetric stretch",
            "centrosymmetric": True, "ir": False, "raman": True,
            "reason": "polarisability changes, no dipole change",
        },
        {
            "molecule": "CO2", "mode": "bending",
            "centrosymmetric": True, "ir": True, "raman": False,
            "reason": "dipole changes, no polarisability change",
        },
        {
            "molecule": "H2O", "mode": "symmetric stretch",
            "centrosymmetric": False, "ir": True, "raman": True,
            "reason": "both dipole and polarisability change",
        },
        {
            "molecule": "H2O", "mode": "asymmetric stretch",
            "centrosymmetric": False, "ir": True, "raman": True,
            "reason": "both dipole and polarisability change",
        },
        {
            "molecule": "N2", "mode": "stretch",
            "centrosymmetric": True, "ir": False, "raman": True,
            "reason": "homonuclear: no dipole change, polarisability changes",
        },
        {
            "molecule": "HCl", "mode": "stretch",
            "centrosymmetric": False, "ir": True, "raman": True,
            "reason": "heteronuclear diatomic: both change",
        },
        {
            "molecule": "C2H2", "mode": "symmetric C-H stretch",
            "centrosymmetric": True, "ir": False, "raman": True,
            "reason": "centrosymmetric: Raman active only",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "raman_vs_ir"

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
        return "determine IR and Raman activity for a vibrational mode"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IR vs Raman activity problem.

        Selects a molecular vibration and asks whether it is IR active,
        Raman active, or both.

        Args:
            difficulty: Controls the pool of vibrations.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.VIBRATIONS), 4 + difficulty)
        vib = self._rng.choice(self.VIBRATIONS[:pool_size])

        centrosym = "centrosymmetric" if vib["centrosymmetric"] else "non-centrosymmetric"
        desc = (
            f"{vib['molecule']} ({centrosym}), "
            f"{vib['mode']}. "
            f"Is this mode IR active, Raman active, or both?"
        )
        return desc, {
            "molecule": vib["molecule"], "mode": vib["mode"],
            "centrosymmetric": vib["centrosymmetric"],
            "ir": vib["ir"], "raman": vib["raman"],
            "reason": vib["reason"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            f"molecule: {sd['molecule']}, mode: {sd['mode']}",
        ]
        if sd["centrosymmetric"]:
            steps.append("centrosymmetric: mutual exclusion applies")
        else:
            steps.append("non-centrosymmetric: modes can be both IR and Raman active")
        steps.append(f"IR active: {'yes' if sd['ir'] else 'no'}")
        steps.append(f"Raman active: {'yes' if sd['raman'] else 'no'}")
        steps.append(f"reason: {sd['reason']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the activity classification.

        Args:
            sd: Solution data dict.

        Returns:
            IR and Raman activity status.
        """
        if sd["ir"] and sd["raman"]:
            activity = "both IR and Raman active"
        elif sd["ir"]:
            activity = "IR active only"
        elif sd["raman"]:
            activity = "Raman active only"
        else:
            activity = "neither IR nor Raman active"
        return activity
