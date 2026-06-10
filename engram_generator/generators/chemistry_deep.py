"""Deep chemistry generators -- reaction mechanisms, thermochemistry, electrochemistry.

10 generators across tiers 4-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ChemistryDeepBase(StepGenerator):
    """Base class for deep chemistry generators with shared constants.

    Provides thermodynamic constants, standard reduction potentials,
    and common buffer/solubility data used across generators.

    Attributes:
        R: Universal gas constant in J/(mol*K).
        F: Faraday constant in C/mol.
    """

    R = 8.314   # J/(mol*K)
    F = 96485   # C/mol


@register
class ReactionMechanismRateGenerator(ChemistryDeepBase):
    """Derive overall rate law from a multi-step mechanism.

    Given a mechanism with a rate-determining step (RDS), derives the
    overall rate law by applying the steady-state or pre-equilibrium
    approximation to eliminate intermediate concentrations.
    """

    MECHANISMS = [
        {
            "name": "SN1 hydrolysis",
            "steps": [
                "R-X -> R+ + X-  (slow)",
                "R+ + H2O -> R-OH + H+  (fast)",
            ],
            "rds": 0,
            "rate_law": "rate = k[R-X]",
            "species": "R-X",
            "order": 1,
        },
        {
            "name": "NO2 decomposition",
            "steps": [
                "2 NO2 -> NO3 + NO  (slow)",
                "NO3 + CO -> NO2 + CO2  (fast)",
            ],
            "rds": 0,
            "rate_law": "rate = k[NO2]^2",
            "species": "NO2",
            "order": 2,
        },
        {
            "name": "ozone decomposition",
            "steps": [
                "O3 <=> O2 + O  (fast equilibrium, K_eq)",
                "O + O3 -> 2 O2  (slow)",
            ],
            "rds": 1,
            "rate_law": "rate = k*K_eq[O3]^2/[O2]",
            "species": "O3",
            "order": 2,
        },
        {
            "name": "H2 + I2 formation",
            "steps": [
                "I2 <=> 2 I  (fast equilibrium, K_eq)",
                "2 I + H2 -> 2 HI  (slow)",
            ],
            "rds": 1,
            "rate_law": "rate = k*K_eq[I2][H2]",
            "species": "H2",
            "order": 1,
        },
        {
            "name": "enzyme catalysis",
            "steps": [
                "E + S <=> ES  (fast equilibrium, K_eq)",
                "ES -> E + P  (slow)",
            ],
            "rds": 1,
            "rate_law": "rate = k*K_eq[E][S]",
            "species": "S",
            "order": 1,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reaction_mechanism_rate"

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
        return "derive overall rate law from reaction mechanism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reaction mechanism rate law problem.

        Selects a mechanism and asks the student to identify the RDS
        and derive the overall rate law.

        Args:
            difficulty: Controls mechanism complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.MECHANISMS), 2 + difficulty)
        mech = self._rng.choice(self.MECHANISMS[:pool_size])

        k_val = round(self._rng.uniform(0.001, 0.5), 4)
        conc = round(self._rng.uniform(0.01, 2.0), 4)
        rate = round(k_val * conc ** mech["order"], 4)

        steps_str = "; ".join(mech["steps"])
        desc = (
            f"Mechanism ({mech['name']}): {steps_str}. "
            f"k={k_val}, [{mech['species']}]={conc} M. "
            f"Find overall rate law and rate."
        )
        return desc, {
            "mech": mech, "k_val": k_val, "conc": conc, "rate": rate,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        mech = sd["mech"]
        return [
            f"RDS: step {mech['rds'] + 1}: {mech['steps'][mech['rds']]}",
            f"overall rate law: {mech['rate_law']}",
            f"rate = {sd['k_val']} * {sd['conc']}^{mech['order']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rate law and computed rate.

        Args:
            sd: Solution data dict.

        Returns:
            Rate law and rate value.
        """
        return f"{sd['mech']['rate_law']}, rate = {sd['rate']} M/s"


@register
class ActivationEnergyGenerator(ChemistryDeepBase):
    """Compute activation energy from two (T, k) data points.

    Uses the two-point Arrhenius form:
    Ea = R * ln(k2/k1) / (1/T1 - 1/T2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "activation_energy"

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
        return "compute activation energy from two temperature-rate pairs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an activation energy problem.

        Creates two (T, k) data points from a known Ea, then asks
        the student to recover Ea.

        Args:
            difficulty: Controls temperature separation and Ea range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ea_true = self._rng.randint(30, 30 + 15 * min(difficulty, 6)) * 1000.0
        a_factor = round(self._rng.uniform(1e6, 1e10), 2)

        t1 = self._rng.randint(280, 350)
        t2 = t1 + self._rng.randint(20, 20 + 10 * min(difficulty, 4))

        k1 = a_factor * math.exp(-ea_true / (self.R * t1))
        k2 = a_factor * math.exp(-ea_true / (self.R * t2))

        inv_t1 = round(1.0 / t1, 6)
        inv_t2 = round(1.0 / t2, 6)
        ln_ratio = round(math.log(k2 / k1), 4)
        inv_diff = round(inv_t1 - inv_t2, 6)
        ea_calc = round(self.R * ln_ratio / inv_diff, 4)
        ea_kj = round(ea_calc / 1000.0, 4)

        desc = (
            f"T1={t1} K, k1={k1:.4e}; "
            f"T2={t2} K, k2={k2:.4e}. Find Ea."
        )
        return desc, {
            "t1": t1, "t2": t2, "k1": k1, "k2": k2,
            "inv_t1": inv_t1, "inv_t2": inv_t2,
            "ln_ratio": ln_ratio, "inv_diff": inv_diff,
            "ea_calc": ea_calc, "ea_kj": ea_kj,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "Ea = R * ln(k2/k1) / (1/T1 - 1/T2)",
            f"ln(k2/k1) = {sd['ln_ratio']}",
            f"1/T1 - 1/T2 = {sd['inv_t1']} - {sd['inv_t2']} = {sd['inv_diff']}",
            f"Ea = 8.314 * {sd['ln_ratio']} / {sd['inv_diff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the activation energy.

        Args:
            sd: Solution data dict.

        Returns:
            Ea in kJ/mol.
        """
        return f"Ea = {sd['ea_kj']} kJ/mol"


@register
class BufferHendersonGenerator(ChemistryDeepBase):
    """Compute buffer pH using the Henderson-Hasselbalch equation.

    pH = pKa + log([A-]/[HA]). At higher difficulty, adds strong
    acid or base to the buffer and computes the new pH.
    """

    BUFFERS = [
        {"name": "acetic acid/acetate", "pKa": 4.76},
        {"name": "NH4+/NH3", "pKa": 9.25},
        {"name": "H2CO3/HCO3-", "pKa": 6.35},
        {"name": "H2PO4-/HPO4^2-", "pKa": 7.20},
        {"name": "formic acid/formate", "pKa": 3.75},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "buffer_henderson"

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
        if difficulty <= 4:
            return "compute buffer pH using Henderson-Hasselbalch"
        return "compute new buffer pH after adding acid or base"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a buffer pH problem.

        At low difficulty, computes pH directly. At high difficulty,
        adds strong acid or base and recomputes.

        Args:
            difficulty: Controls whether acid/base addition is included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        buf = self._rng.choice(self.BUFFERS)
        ha = round(self._rng.uniform(0.05, 0.5), 4)
        a_minus = round(self._rng.uniform(0.05, 0.5), 4)

        if difficulty <= 4:
            ratio = round(a_minus / ha, 4)
            log_ratio = round(math.log10(ratio), 4)
            ph = round(buf["pKa"] + log_ratio, 4)
            desc = (
                f"Buffer: {buf['name']}, pKa={buf['pKa']}, "
                f"[HA]={ha} M, [A-]={a_minus} M. Find pH."
            )
            return desc, {
                "buf": buf["name"], "pKa": buf["pKa"],
                "ha": ha, "a_minus": a_minus,
                "ratio": ratio, "log_ratio": log_ratio,
                "ph": ph, "mode": "simple",
            }

        # Add strong acid or base
        add_type = self._rng.choice(["acid", "base"])
        add_mol = round(self._rng.uniform(0.01, min(ha, a_minus) * 0.4), 4)

        if add_type == "acid":
            new_ha = round(ha + add_mol, 4)
            new_a = round(a_minus - add_mol, 4)
        else:
            new_ha = round(ha - add_mol, 4)
            new_a = round(a_minus + add_mol, 4)

        ratio = round(new_a / new_ha, 4)
        log_ratio = round(math.log10(ratio), 4)
        ph = round(buf["pKa"] + log_ratio, 4)

        desc = (
            f"Buffer: {buf['name']}, pKa={buf['pKa']}, "
            f"[HA]={ha} M, [A-]={a_minus} M. "
            f"Add {add_mol} mol/L strong {add_type}. New pH?"
        )
        return desc, {
            "buf": buf["name"], "pKa": buf["pKa"],
            "ha": ha, "a_minus": a_minus,
            "add_type": add_type, "add_mol": add_mol,
            "new_ha": new_ha, "new_a": new_a,
            "ratio": ratio, "log_ratio": log_ratio,
            "ph": ph, "mode": "addition",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["pH = pKa + log([A-]/[HA])"]
        if sd["mode"] == "addition":
            if sd["add_type"] == "acid":
                steps.append(
                    f"acid neutralises A-: new [HA]={sd['new_ha']}, "
                    f"new [A-]={sd['new_a']}"
                )
            else:
                steps.append(
                    f"base neutralises HA: new [HA]={sd['new_ha']}, "
                    f"new [A-]={sd['new_a']}"
                )
        steps.append(f"[A-]/[HA] = {sd['ratio']}")
        steps.append(f"log({sd['ratio']}) = {sd['log_ratio']}")
        steps.append(f"pH = {sd['pKa']} + {sd['log_ratio']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the buffer pH.

        Args:
            sd: Solution data dict.

        Returns:
            pH value.
        """
        return f"pH = {sd['ph']}"


@register
class GalvanicCellGenerator(ChemistryDeepBase):
    """Compute standard cell potential for a galvanic cell.

    E_cell = E_cathode - E_anode. Given two half-reactions with standard
    reduction potentials, identifies cathode and anode and computes E.
    """

    HALF_CELLS = [
        {"species": "Cu2+/Cu", "E0": 0.34},
        {"species": "Zn2+/Zn", "E0": -0.76},
        {"species": "Ag+/Ag", "E0": 0.80},
        {"species": "Fe2+/Fe", "E0": -0.44},
        {"species": "Ni2+/Ni", "E0": -0.26},
        {"species": "Sn2+/Sn", "E0": -0.14},
        {"species": "Pb2+/Pb", "E0": -0.13},
        {"species": "H+/H2", "E0": 0.00},
        {"species": "Au3+/Au", "E0": 1.50},
        {"species": "Cr3+/Cr", "E0": -0.74},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "galvanic_cell"

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
        return "compute galvanic cell potential from half-reactions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a galvanic cell problem.

        Selects two half-cells, identifies cathode and anode, and
        computes the standard cell potential.

        Args:
            difficulty: Controls the pool of half-cells.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.HALF_CELLS), 4 + difficulty)
        pair = self._rng.sample(self.HALF_CELLS[:pool_size], 2)

        if pair[0]["E0"] >= pair[1]["E0"]:
            cathode, anode = pair[0], pair[1]
        else:
            cathode, anode = pair[1], pair[0]

        e_cell = round(cathode["E0"] - anode["E0"], 4)

        desc = (
            f"Half-cells: {pair[0]['species']} (E0={pair[0]['E0']} V), "
            f"{pair[1]['species']} (E0={pair[1]['E0']} V). "
            f"Find E_cell."
        )
        return desc, {
            "cathode": cathode["species"], "anode": anode["species"],
            "e_cathode": cathode["E0"], "e_anode": anode["E0"],
            "e_cell": e_cell,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"cathode (reduction): {sd['cathode']}, E0={sd['e_cathode']} V",
            f"anode (oxidation): {sd['anode']}, E0={sd['e_anode']} V",
            "E_cell = E_cathode - E_anode",
            f"E_cell = {sd['e_cathode']} - {sd['e_anode']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the cell potential.

        Args:
            sd: Solution data dict.

        Returns:
            E_cell in volts.
        """
        return f"E_cell = {sd['e_cell']} V"


@register
class FaradayElectrolysisGenerator(ChemistryDeepBase):
    """Compute mass deposited during electrolysis using Faraday's law.

    m = (M * I * t) / (n * F) where M is molar mass, I is current,
    t is time, n is electron count, F is Faraday's constant.
    """

    METALS = [
        {"name": "Cu", "M": 63.55, "n": 2},
        {"name": "Ag", "M": 107.87, "n": 1},
        {"name": "Au", "M": 196.97, "n": 3},
        {"name": "Ni", "M": 58.69, "n": 2},
        {"name": "Zn", "M": 65.38, "n": 2},
        {"name": "Cr", "M": 52.00, "n": 3},
        {"name": "Al", "M": 26.98, "n": 3},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "faraday_electrolysis"

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
        return "compute mass deposited during electrolysis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Faraday electrolysis problem.

        Selects a metal, generates current and time, then computes
        the mass deposited.

        Args:
            difficulty: Controls current/time ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.METALS), 3 + difficulty)
        metal = self._rng.choice(self.METALS[:pool_size])

        current = round(self._rng.uniform(0.5, 5.0 * max(1, difficulty)), 2)
        time_s = self._rng.randint(600, 600 + 600 * min(difficulty, 6))

        numerator = round(metal["M"] * current * time_s, 4)
        denominator = round(metal["n"] * self.F, 4)
        mass = round(numerator / denominator, 4)

        desc = (
            f"Electrolysis of {metal['name']}^{metal['n']}+: "
            f"M={metal['M']} g/mol, n={metal['n']}, "
            f"I={current} A, t={time_s} s. Find mass deposited."
        )
        return desc, {
            "metal": metal["name"], "M": metal["M"], "n_e": metal["n"],
            "current": current, "time_s": time_s,
            "numerator": numerator, "denominator": denominator,
            "mass": mass,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "m = (M * I * t) / (n * F)",
            f"numerator = {sd['M']} * {sd['current']} * {sd['time_s']} = {sd['numerator']}",
            f"denominator = {sd['n_e']} * 96485 = {sd['denominator']}",
            f"m = {sd['numerator']} / {sd['denominator']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the mass deposited.

        Args:
            sd: Solution data dict.

        Returns:
            Mass in grams.
        """
        return f"m = {sd['mass']} g"


@register
class BornHaberCycleGenerator(ChemistryDeepBase):
    """Compute lattice energy from a Born-Haber thermodynamic cycle.

    dH_f = dH_sub + IE + dH_diss/2 + EA + U, solving for U (lattice
    energy) from the other known quantities.
    """

    COMPOUNDS = [
        {
            "name": "NaCl", "dH_f": -411.2,
            "dH_sub": 107.3, "IE": 495.8,
            "dH_diss": 242.0, "EA": -349.0,
        },
        {
            "name": "KBr", "dH_f": -393.8,
            "dH_sub": 89.0, "IE": 418.8,
            "dH_diss": 193.0, "EA": -324.6,
        },
        {
            "name": "LiF", "dH_f": -616.0,
            "dH_sub": 159.3, "IE": 520.2,
            "dH_diss": 155.0, "EA": -328.0,
        },
        {
            "name": "NaBr", "dH_f": -361.1,
            "dH_sub": 107.3, "IE": 495.8,
            "dH_diss": 193.0, "EA": -324.6,
        },
        {
            "name": "KCl", "dH_f": -436.7,
            "dH_sub": 89.0, "IE": 418.8,
            "dH_diss": 242.0, "EA": -349.0,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "born_haber_cycle"

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
        return "compute lattice energy from Born-Haber cycle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Born-Haber cycle problem.

        Selects a compound and asks for the lattice energy U.

        Args:
            difficulty: Controls the pool of compounds.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPOUNDS), 2 + difficulty)
        comp = self._rng.choice(self.COMPOUNDS[:pool_size])

        half_diss = round(comp["dH_diss"] / 2.0, 4)
        sum_other = round(
            comp["dH_sub"] + comp["IE"] + half_diss + comp["EA"], 4
        )
        lattice_u = round(comp["dH_f"] - sum_other, 4)

        desc = (
            f"{comp['name']}: dH_f={comp['dH_f']}, "
            f"dH_sub={comp['dH_sub']}, IE={comp['IE']}, "
            f"dH_diss={comp['dH_diss']}, EA={comp['EA']} kJ/mol. "
            f"Find lattice energy U."
        )
        return desc, {
            "compound": comp["name"], "dH_f": comp["dH_f"],
            "dH_sub": comp["dH_sub"], "IE": comp["IE"],
            "half_diss": half_diss, "EA": comp["EA"],
            "sum_other": sum_other, "lattice_u": lattice_u,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "dH_f = dH_sub + IE + dH_diss/2 + EA + U",
            "U = dH_f - (dH_sub + IE + dH_diss/2 + EA)",
            f"dH_diss/2 = {sd['half_diss']}",
            f"sum = {sd['dH_sub']} + {sd['IE']} + {sd['half_diss']} + {sd['EA']} = {sd['sum_other']}",
            f"U = {sd['dH_f']} - {sd['sum_other']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the lattice energy.

        Args:
            sd: Solution data dict.

        Returns:
            Lattice energy in kJ/mol.
        """
        return f"U = {sd['lattice_u']} kJ/mol"


@register
class SolubilityPhGenerator(ChemistryDeepBase):
    """Compute solubility from Ksp and analyse pH effects.

    For a salt M_aA_b: Ksp = [M]^a * [A]^b. Computes molar solubility
    S from Ksp. At higher difficulty, discusses pH effects on
    salts with basic anions.
    """

    SALTS = [
        {"formula": "AgCl", "a": 1, "b": 1, "Ksp": 1.77e-10, "basic_anion": False},
        {"formula": "BaSO4", "a": 1, "b": 1, "Ksp": 1.08e-10, "basic_anion": False},
        {"formula": "CaF2", "a": 1, "b": 2, "Ksp": 3.45e-11, "basic_anion": True},
        {"formula": "PbI2", "a": 1, "b": 2, "Ksp": 9.8e-9, "basic_anion": False},
        {"formula": "Ag2CrO4", "a": 2, "b": 1, "Ksp": 1.12e-12, "basic_anion": False},
        {"formula": "Ca(OH)2", "a": 1, "b": 2, "Ksp": 4.68e-6, "basic_anion": True},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "solubility_ph"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        if difficulty <= 4:
            return "compute molar solubility from Ksp"
        return "compute solubility from Ksp and analyse pH effect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a solubility/pH problem.

        Computes molar solubility S from Ksp. At higher difficulty,
        adds pH effect analysis for salts with basic anions.

        Args:
            difficulty: Controls whether pH analysis is included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.SALTS), 3 + difficulty)
        salt = self._rng.choice(self.SALTS[:pool_size])

        a, b = salt["a"], salt["b"]
        # Ksp = (a*S)^a * (b*S)^b = a^a * b^b * S^(a+b)
        coeff = (a ** a) * (b ** b)
        total_power = a + b
        s = round((salt["Ksp"] / coeff) ** (1.0 / total_power), 4)

        ph_effect = "no significant pH effect"
        if salt["basic_anion"] and difficulty > 4:
            ph_effect = "solubility increases at lower pH (anion is basic)"

        desc = (
            f"{salt['formula']}, Ksp={salt['Ksp']:.2e}. "
            f"Find molar solubility S."
        )
        if difficulty > 4 and salt["basic_anion"]:
            desc += " Predict pH effect on solubility."

        return desc, {
            "formula": salt["formula"], "Ksp": salt["Ksp"],
            "a": a, "b": b, "coeff": coeff,
            "total_power": total_power, "s": s,
            "ph_effect": ph_effect,
            "include_ph": difficulty > 4 and salt["basic_anion"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            f"Ksp = {sd['a']}^{sd['a']} * {sd['b']}^{sd['b']} * S^{sd['total_power']}",
            f"coeff = {sd['coeff']}",
            f"S = (Ksp/{sd['coeff']})^(1/{sd['total_power']})",
            f"S = ({sd['Ksp']:.2e}/{sd['coeff']})^(1/{sd['total_power']})",
        ]
        if sd["include_ph"]:
            steps.append(f"pH effect: {sd['ph_effect']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the molar solubility.

        Args:
            sd: Solution data dict.

        Returns:
            S in mol/L with optional pH effect.
        """
        ans = f"S = {sd['s']} M"
        if sd["include_ph"]:
            ans += f"; {sd['ph_effect']}"
        return ans


@register
class ComplexationEquilibriumGenerator(ChemistryDeepBase):
    """Compute complex ion concentration from formation constant.

    Kf = [ML] / ([M][L]). Given Kf and initial concentrations,
    computes [ML]. At higher difficulty, uses sequential formation
    constants: beta_n = K1 * K2 * ... * Kn.
    """

    COMPLEXES = [
        {"metal": "Cu2+", "ligand": "NH3", "Kf": 1.1e13, "n_ligands": 4},
        {"metal": "Ag+", "ligand": "NH3", "Kf": 1.7e7, "n_ligands": 2},
        {"metal": "Fe3+", "ligand": "SCN-", "Kf": 890.0, "n_ligands": 1},
        {"metal": "Zn2+", "ligand": "OH-", "Kf": 2.0e15, "n_ligands": 4},
        {"metal": "Ni2+", "ligand": "NH3", "Kf": 5.5e8, "n_ligands": 6},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "complexation_equilibrium"

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
        if difficulty <= 4:
            return "compute complex ion concentration from Kf"
        return "compute sequential formation constant beta_n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complexation equilibrium problem.

        At low difficulty, computes [ML] from Kf and concentrations.
        At high difficulty, computes beta_n from stepwise K values.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPLEXES), 2 + difficulty)
        cpx = self._rng.choice(self.COMPLEXES[:pool_size])

        if difficulty <= 4:
            m_conc = round(self._rng.uniform(0.001, 0.1), 4)
            l_conc = round(self._rng.uniform(0.01, 1.0), 4)
            # For very large Kf, essentially all M goes to ML
            kf_simple = round(self._rng.uniform(100.0, 5000.0), 4)
            ml_conc = round(
                kf_simple * m_conc * l_conc / (1 + kf_simple * l_conc), 4
            )

            desc = (
                f"M={cpx['metal']}, L={cpx['ligand']}, "
                f"Kf={kf_simple}, [{cpx['metal']}]={m_conc} M, "
                f"[{cpx['ligand']}]={l_conc} M. Find [ML]."
            )
            return desc, {
                "metal": cpx["metal"], "ligand": cpx["ligand"],
                "Kf": kf_simple, "m_conc": m_conc, "l_conc": l_conc,
                "ml_conc": ml_conc, "mode": "simple",
            }

        # Sequential: beta_n = K1 * K2 * ... * Kn
        n = min(cpx["n_ligands"], 2 + difficulty // 2)
        k_values = [
            round(self._rng.uniform(10.0, 1000.0), 4) for _ in range(n)
        ]
        beta_n = 1.0
        for k in k_values:
            beta_n *= k
        beta_n = round(beta_n, 4)

        k_str = ", ".join(f"K{i + 1}={k}" for i, k in enumerate(k_values))
        desc = (
            f"{cpx['metal']} + {n}{cpx['ligand']}: {k_str}. "
            f"Find beta_{n}."
        )
        return desc, {
            "metal": cpx["metal"], "ligand": cpx["ligand"],
            "n": n, "k_values": k_values, "beta_n": beta_n,
            "mode": "sequential",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "simple":
            return [
                "Kf = [ML] / ([M][L])",
                f"[ML] = Kf*[M]*[L] / (1 + Kf*[L])",
                f"[ML] = {sd['Kf']}*{sd['m_conc']}*{sd['l_conc']} / (1 + {sd['Kf']}*{sd['l_conc']})",
            ]
        steps = [f"beta_{sd['n']} = K1 * K2 * ... * K{sd['n']}"]
        product = 1.0
        for i, k in enumerate(sd["k_values"]):
            product *= k
            steps.append(f"after K{i + 1}={k}: product = {round(product, 4)}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the complex concentration or beta_n.

        Args:
            sd: Solution data dict.

        Returns:
            [ML] or beta_n value.
        """
        if sd["mode"] == "simple":
            return f"[ML] = {sd['ml_conc']} M"
        return f"beta_{sd['n']} = {sd['beta_n']}"


@register
class ThermodynamicCycleGenerator(ChemistryDeepBase):
    """Apply Hess's law to construct a thermodynamic cycle.

    Given a set of known reactions with their enthalpies, constructs
    the target reaction by reversing and scaling steps, then sums
    enthalpies.
    """

    REACTION_SETS = [
        {
            "target": "C(s) + O2(g) -> CO2(g)",
            "given": [
                ("C(s) + 0.5 O2(g) -> CO(g)", -110.5),
                ("CO(g) + 0.5 O2(g) -> CO2(g)", -283.0),
            ],
            "operations": ["use as is", "use as is"],
            "dH_target": -393.5,
        },
        {
            "target": "N2(g) + O2(g) -> 2 NO(g)",
            "given": [
                ("0.5 N2(g) + O2(g) -> NO2(g)", 33.2),
                ("NO(g) + 0.5 O2(g) -> NO2(g)", -57.1),
            ],
            "operations": ["multiply by 2", "reverse and multiply by 2"],
            "dH_target": round(2 * 33.2 - 2 * (-57.1), 4),
        },
        {
            "target": "CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)",
            "given": [
                ("C(s) + O2(g) -> CO2(g)", -393.5),
                ("H2(g) + 0.5 O2(g) -> H2O(l)", -285.8),
                ("C(s) + 2 H2(g) -> CH4(g)", -74.6),
            ],
            "operations": ["use as is", "multiply by 2", "reverse"],
            "dH_target": round(-393.5 + 2 * (-285.8) - (-74.6), 4),
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thermodynamic_cycle"

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
        return "apply Hess's law to compute reaction enthalpy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hess's law thermodynamic cycle problem.

        Selects a reaction set and asks for the enthalpy of the
        target reaction.

        Args:
            difficulty: Controls the pool of reaction sets.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REACTION_SETS), 1 + difficulty // 2)
        rxn_set = self._rng.choice(self.REACTION_SETS[:pool_size])

        given_str = "; ".join(
            f"({i + 1}) {rxn} dH={dh} kJ"
            for i, (rxn, dh) in enumerate(rxn_set["given"])
        )
        desc = f"Target: {rxn_set['target']}. Given: {given_str}. Find dH."
        return desc, {
            "target": rxn_set["target"],
            "given": rxn_set["given"],
            "operations": rxn_set["operations"],
            "dH_target": rxn_set["dH_target"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["Hess's law: dH_target = sum of manipulated dH values"]
        for i, (rxn, dh) in enumerate(sd["given"]):
            steps.append(f"step {i + 1}: {sd['operations'][i]}, dH={dh}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the target reaction enthalpy.

        Args:
            sd: Solution data dict.

        Returns:
            dH in kJ/mol.
        """
        return f"dH = {sd['dH_target']} kJ/mol"


@register
class IonicStrengthGenerator(ChemistryDeepBase):
    """Compute ionic strength and activity coefficient.

    I = 0.5 * sum(c_i * z_i^2). Then applies the Debye-Huckel
    limiting law: log(gamma) = -A * z^2 * sqrt(I), where A = 0.509
    at 25 C for water.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ionic_strength"

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
        if difficulty <= 4:
            return "compute ionic strength of a solution"
        return "compute ionic strength and activity coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ionic strength / Debye-Huckel problem.

        Creates a solution with 2-4 ions, computes ionic strength,
        and optionally applies the Debye-Huckel law for gamma.

        Args:
            difficulty: Controls number of ions and whether DH is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ion_pool = [
            ("Na+", 1), ("Cl-", 1), ("Ca2+", 2), ("SO4^2-", 2),
            ("K+", 1), ("Mg2+", 2), ("NO3-", 1), ("Al3+", 3),
        ]
        n_ions = min(2 + difficulty // 2, 4)
        chosen = self._rng.sample(ion_pool, n_ions)

        concentrations = [
            round(self._rng.uniform(0.01, 0.2), 4) for _ in range(n_ions)
        ]

        ionic_str = 0.0
        ion_terms = []
        for i, (ion, z) in enumerate(chosen):
            term = concentrations[i] * z ** 2
            ion_terms.append((ion, concentrations[i], z, round(term, 4)))
            ionic_str += term
        ionic_str = round(0.5 * ionic_str, 4)

        ion_desc = ", ".join(
            f"[{ion}]={c} M" for (ion, c, _, _) in ion_terms
        )
        desc = f"Solution: {ion_desc}. Find ionic strength I."

        sd = {
            "ion_terms": ion_terms, "ionic_str": ionic_str,
            "mode": "simple",
        }

        if difficulty > 4:
            # Debye-Huckel for a target ion
            target_ion, target_z = self._rng.choice(chosen)
            a_const = 0.509
            sqrt_i = round(math.sqrt(ionic_str), 4)
            log_gamma = round(-a_const * target_z ** 2 * sqrt_i, 4)
            gamma = round(10 ** log_gamma, 4)

            desc += f" Find gamma for {target_ion}."
            sd.update({
                "mode": "debye_huckel",
                "target_ion": target_ion, "target_z": target_z,
                "a_const": a_const, "sqrt_i": sqrt_i,
                "log_gamma": log_gamma, "gamma": gamma,
            })

        return desc, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["I = 0.5 * sum(c_i * z_i^2)"]
        for ion, c, z, term in sd["ion_terms"]:
            steps.append(f"{ion}: {c} * {z}^2 = {term}")
        steps.append(f"I = 0.5 * sum = {sd['ionic_str']}")

        if sd["mode"] == "debye_huckel":
            steps.append(
                f"log(gamma) = -0.509 * {sd['target_z']}^2 * sqrt({sd['ionic_str']})"
            )
            steps.append(f"log(gamma) = {sd['log_gamma']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the ionic strength and optionally gamma.

        Args:
            sd: Solution data dict.

        Returns:
            I value, optionally with activity coefficient.
        """
        ans = f"I = {sd['ionic_str']}"
        if sd["mode"] == "debye_huckel":
            ans += f", gamma({sd['target_ion']}) = {sd['gamma']}"
        return ans
