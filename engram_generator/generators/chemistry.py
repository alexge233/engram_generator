"""Chemistry generators — stoichiometry, molarity, pH, balancing.

5 generators across tiers 2-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ChemistryGenerator(StepGenerator):
    """Base class for chemistry generators with shared data.

    Attributes:
        ATOMIC_MASSES: Mapping of element symbols to molar masses.
    """

    ATOMIC_MASSES = {
        "H": 1.008, "He": 4.003, "C": 12.011, "N": 14.007,
        "O": 15.999, "Na": 22.990, "Cl": 35.453, "S": 32.065,
        "Ca": 40.078, "Fe": 55.845, "K": 39.098, "Mg": 24.305,
    }

    MOLECULES = [
        ("H2O", [("H", 2), ("O", 1)]),
        ("CO2", [("C", 1), ("O", 2)]),
        ("NaCl", [("Na", 1), ("Cl", 1)]),
        ("CaCO3", [("Ca", 1), ("C", 1), ("O", 3)]),
        ("H2SO4", [("H", 2), ("S", 1), ("O", 4)]),
        ("NaOH", [("Na", 1), ("O", 1), ("H", 1)]),
        ("Fe2O3", [("Fe", 2), ("O", 3)]),
        ("C6H12O6", [("C", 6), ("H", 12), ("O", 6)]),
    ]

    EQUATIONS = [
        ("H2 + O2 -> H2O", "2H2 + O2 -> 2H2O"),
        ("N2 + H2 -> NH3", "N2 + 3H2 -> 2NH3"),
        ("Fe + O2 -> Fe2O3", "4Fe + 3O2 -> 2Fe2O3"),
        ("CH4 + O2 -> CO2 + H2O", "CH4 + 2O2 -> CO2 + 2H2O"),
        ("Na + Cl2 -> NaCl", "2Na + Cl2 -> 2NaCl"),
        ("C3H8 + O2 -> CO2 + H2O", "C3H8 + 5O2 -> 3CO2 + 4H2O"),
    ]

    REACTIONS = [
        ("2H2 + O2 -> 2H2O", "H2", "H2O", 2, 2),
        ("N2 + 3H2 -> 2NH3", "N2", "NH3", 1, 2),
        ("CH4 + 2O2 -> CO2 + 2H2O", "CH4", "CO2", 1, 1),
    ]


@register
class MolarMassGenerator(ChemistryGenerator):
    """Calculate the molar mass of a molecule."""

    @property
    def task_name(self) -> str:
        return "molar_mass"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "calculate molar mass"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        formula, parts = self._rng.choice(
            self.MOLECULES[:min(len(self.MOLECULES), 3 + difficulty)]
        )
        mass = round(sum(self.ATOMIC_MASSES[e] * n for e, n in parts), 3)
        return f"molar mass of {formula}", {"formula": formula, "parts": parts, "mass": mass}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{e}: {self.ATOMIC_MASSES[e]} x {n} = {round(self.ATOMIC_MASSES[e] * n, 3)}"
            for e, n in sd["parts"]
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['mass']} g/mol"


@register
class BalancingEquationGenerator(ChemistryGenerator):
    """Balance a simple chemical equation."""

    @property
    def task_name(self) -> str:
        return "balancing_equation"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "balance chemical equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        unbalanced, balanced = self._rng.choice(
            self.EQUATIONS[:min(len(self.EQUATIONS), 2 + difficulty)]
        )
        return f"balance: {unbalanced}", {"unbalanced": unbalanced, "balanced": balanced}

    def _create_steps(self, sd: dict) -> list[str]:
        return ["count atoms each side", "adjust coefficients"]

    def _create_answer(self, sd: dict) -> str:
        return sd["balanced"]


@register
class StoichiometryGenerator(ChemistryGenerator):
    """Calculate amounts using mole ratios."""

    @property
    def task_name(self) -> str:
        return "stoichiometry"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["molar_mass", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "stoichiometry calculation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        eq, reactant, product, r_coeff, p_coeff = self._rng.choice(
            self.REACTIONS[:min(len(self.REACTIONS), 1 + difficulty)]
        )
        moles_r = self._rng.randint(1, 5 * difficulty)
        moles_p = round(moles_r * p_coeff / r_coeff, 2)
        return (
            f"{eq}: {moles_r} mol {reactant} produces how many mol {product}?",
            {"r_coeff": r_coeff, "p_coeff": p_coeff,
             "reactant": reactant, "product": product,
             "moles_r": moles_r, "moles_p": moles_p},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"ratio: {sd['r_coeff']}:{sd['p_coeff']}",
            f"{sd['moles_r']} * {sd['p_coeff']}/{sd['r_coeff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['moles_p']} mol"


@register
class MolarityGenerator(ChemistryGenerator):
    """Calculate molarity or dilution."""

    @property
    def task_name(self) -> str:
        return "molarity"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["molar_mass", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate molarity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["concentration", "dilution"])
        if mode == "concentration":
            moles = round(self._rng.uniform(0.1, 5.0 * difficulty), 2)
            litres = round(self._rng.uniform(0.1, 5.0), 2)
            m = round(moles / litres, 4)
            return f"{moles} mol in {litres} L", {"M": m, "mode": mode}
        m1 = round(self._rng.uniform(0.5, 5.0), 2)
        v1 = round(self._rng.uniform(0.05, 1.0), 3)
        v2 = round(v1 + self._rng.uniform(0.5, 3.0), 3)
        m2 = round(m1 * v1 / v2, 4)
        return f"dilute {m1}M ({v1}L) to {v2}L", {"m2": m2, "mode": mode}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "concentration":
            return ["M = moles / litres"]
        return ["M1*V1 = M2*V2"]

    def _create_answer(self, sd: dict) -> str:
        key = "M" if sd["mode"] == "concentration" else "m2"
        return f"{sd[key]} M"


@register
class PhCalculationGenerator(ChemistryGenerator):
    """Calculate pH from hydrogen ion concentration."""

    @property
    def task_name(self) -> str:
        return "ph_calculation"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        return "calculate pH"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        exp = -self._rng.randint(1, min(13, 2 + 2 * difficulty))
        conc = 10.0 ** exp
        return f"[H+] = {conc}", {"conc": conc, "ph": -exp}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"pH = -log10([H+])", f"pH = -log10({sd['conc']})"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["ph"])
