"""Extended general chemistry generators -- stoichiometry, gas laws, acid-base.

8 generators across tiers 3-5 covering limiting reagent, percent composition,
empirical formula, solution dilution, combined gas law, Dalton's law,
acid-base titration, and buffer capacity.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Shared data for general chemistry extensions
# ---------------------------------------------------------------------------

MOLAR_MASSES = {
    "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
    "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Br": 79.904, "Ag": 107.868,
    "I": 126.904, "Ba": 137.327,
}


# ---------------------------------------------------------------------------
# 1. Limiting Reagent (tier 3)
# ---------------------------------------------------------------------------

@register
class LimitingReagentGenerator(StepGenerator):
    """Identify limiting reagent and compute theoretical yield.

    Given masses of two reactants and a balanced equation, determines
    which reactant is limiting and the theoretical yield of product.
    """

    REACTIONS = [
        {
            "equation": "2H2 + O2 -> 2H2O",
            "r1": "H2", "r1_mm": 2.016, "r1_coeff": 2,
            "r2": "O2", "r2_mm": 32.0, "r2_coeff": 1,
            "product": "H2O", "p_mm": 18.015, "p_coeff": 2,
        },
        {
            "equation": "N2 + 3H2 -> 2NH3",
            "r1": "N2", "r1_mm": 28.014, "r1_coeff": 1,
            "r2": "H2", "r2_mm": 2.016, "r2_coeff": 3,
            "product": "NH3", "p_mm": 17.031, "p_coeff": 2,
        },
        {
            "equation": "Fe2O3 + 3CO -> 2Fe + 3CO2",
            "r1": "Fe2O3", "r1_mm": 159.69, "r1_coeff": 1,
            "r2": "CO", "r2_mm": 28.01, "r2_coeff": 3,
            "product": "Fe", "p_mm": 55.845, "p_coeff": 2,
        },
        {
            "equation": "CH4 + 2O2 -> CO2 + 2H2O",
            "r1": "CH4", "r1_mm": 16.043, "r1_coeff": 1,
            "r2": "O2", "r2_mm": 32.0, "r2_coeff": 2,
            "product": "CO2", "p_mm": 44.01, "p_coeff": 1,
        },
        {
            "equation": "2Al + 3Cl2 -> 2AlCl3",
            "r1": "Al", "r1_mm": 26.982, "r1_coeff": 2,
            "r2": "Cl2", "r2_mm": 70.906, "r2_coeff": 3,
            "product": "AlCl3", "p_mm": 133.34, "p_coeff": 2,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "limiting_reagent"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["stoichiometry"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "identify limiting reagent and theoretical yield"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a limiting reagent problem.

        Selects a reaction, generates random masses, and determines
        which reactant is consumed first.

        Args:
            difficulty: Controls mass range and reaction pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.REACTIONS), 2 + difficulty)
        rxn = self._rng.choice(self.REACTIONS[:pool_size])

        m1 = round(self._rng.uniform(1.0, 10.0 * difficulty), 2)
        m2 = round(self._rng.uniform(1.0, 10.0 * difficulty), 2)

        mol1 = m1 / rxn["r1_mm"]
        mol2 = m2 / rxn["r2_mm"]

        ratio1 = mol1 / rxn["r1_coeff"]
        ratio2 = mol2 / rxn["r2_coeff"]

        if ratio1 <= ratio2:
            limiting = rxn["r1"]
            mol_product = mol1 * rxn["p_coeff"] / rxn["r1_coeff"]
        else:
            limiting = rxn["r2"]
            mol_product = mol2 * rxn["p_coeff"] / rxn["r2_coeff"]

        yield_g = round(mol_product * rxn["p_mm"], 4)
        mol1 = round(mol1, 4)
        mol2 = round(mol2, 4)

        return (
            f"{rxn['equation']}. {m1}g {rxn['r1']}, {m2}g {rxn['r2']}. "
            f"Find limiting reagent and yield of {rxn['product']}.",
            {"rxn": rxn, "m1": m1, "m2": m2,
             "mol1": mol1, "mol2": mol2,
             "limiting": limiting, "yield_g": yield_g},
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
            f"mol {rxn['r1']} = {sd['m1']}/{rxn['r1_mm']} = {sd['mol1']}",
            f"mol {rxn['r2']} = {sd['m2']}/{rxn['r2_mm']} = {sd['mol2']}",
            f"limiting reagent: {sd['limiting']}",
            f"yield = {sd['yield_g']} g {rxn['product']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Limiting reagent and yield.
        """
        return (
            f"limiting: {sd['limiting']}, "
            f"yield: {sd['yield_g']} g"
        )


# ---------------------------------------------------------------------------
# 2. Percent Composition (tier 3)
# ---------------------------------------------------------------------------

@register
class PercentCompositionGenerator(StepGenerator):
    """Compute mass percent of each element in a compound.

    Mass percent = (n * atomic_mass / molar_mass) * 100 for each
    element in the molecular formula.
    """

    COMPOUNDS = [
        {"formula": "H2O", "elements": [("H", 2), ("O", 1)]},
        {"formula": "CO2", "elements": [("C", 1), ("O", 2)]},
        {"formula": "NaCl", "elements": [("Na", 1), ("Cl", 1)]},
        {"formula": "CaCO3", "elements": [("Ca", 1), ("C", 1), ("O", 3)]},
        {"formula": "H2SO4", "elements": [("H", 2), ("S", 1), ("O", 4)]},
        {"formula": "C6H12O6", "elements": [("C", 6), ("H", 12), ("O", 6)]},
        {"formula": "NH3", "elements": [("N", 1), ("H", 3)]},
        {"formula": "Fe2O3", "elements": [("Fe", 2), ("O", 3)]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "percent_composition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["molar_mass"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute percent composition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a percent composition problem.

        Selects a compound and computes mass percent for each element.

        Args:
            difficulty: Controls compound pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.COMPOUNDS), 3 + difficulty)
        compound = self._rng.choice(self.COMPOUNDS[:pool_size])

        mm = sum(
            n * MOLAR_MASSES[elem] for elem, n in compound["elements"]
        )
        mm = round(mm, 4)

        percents = []
        for elem, n in compound["elements"]:
            pct = round(n * MOLAR_MASSES[elem] / mm * 100, 4)
            percents.append((elem, n, pct))

        return (
            f"percent composition of {compound['formula']}",
            {"formula": compound["formula"], "mm": mm,
             "percents": percents},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [f"molar mass of {sd['formula']} = {sd['mm']} g/mol"]
        for elem, n, pct in sd["percents"]:
            steps.append(
                f"{elem}: {n}*{MOLAR_MASSES[elem]}/{sd['mm']}*100 = {pct}%"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Percent composition for all elements.
        """
        parts = [f"{elem}={pct}%" for elem, _, pct in sd["percents"]]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 3. Empirical Formula (tier 4)
# ---------------------------------------------------------------------------

@register
class EmpiricalFormulaGenerator(StepGenerator):
    """Derive empirical formula from mass percentages.

    Converts mass percentages to moles, divides by the smallest
    mole count to get the simplest whole-number ratio.
    """

    FORMULAS = [
        {"formula": "CH2O", "elements": [("C", 1), ("H", 2), ("O", 1)]},
        {"formula": "NO2", "elements": [("N", 1), ("O", 2)]},
        {"formula": "CH4", "elements": [("C", 1), ("H", 4)]},
        {"formula": "P2O5", "elements": [("P", 2), ("O", 5)]},
        {"formula": "Fe2O3", "elements": [("Fe", 2), ("O", 3)]},
        {"formula": "Na2O", "elements": [("Na", 2), ("O", 1)]},
        {"formula": "CaO", "elements": [("Ca", 1), ("O", 1)]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "empirical_formula"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["molar_mass"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "derive empirical formula from mass percentages"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an empirical formula problem.

        Starts from a known formula, computes mass percentages,
        then asks the student to work backward to the empirical formula.

        Args:
            difficulty: Controls formula pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.FORMULAS), 3 + difficulty)
        entry = self._rng.choice(self.FORMULAS[:pool_size])

        mm = sum(
            n * MOLAR_MASSES[elem] for elem, n in entry["elements"]
        )
        percents = []
        for elem, n in entry["elements"]:
            pct = round(n * MOLAR_MASSES[elem] / mm * 100, 2)
            percents.append((elem, pct))

        # Work backward: moles from 100g sample
        moles = [(elem, round(pct / MOLAR_MASSES[elem], 4))
                  for elem, pct in percents]
        min_mol = min(m for _, m in moles)
        ratios = [(elem, round(m / min_mol, 1))
                  for elem, m in moles]

        pct_str = ", ".join(f"{elem}={pct}%" for elem, pct in percents)

        return (
            f"mass%: {pct_str}. Find empirical formula.",
            {"percents": percents, "moles": moles,
             "ratios": ratios, "formula": entry["formula"]},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["assume 100g sample"]
        for elem, mol in sd["moles"]:
            steps.append(f"mol {elem} = {mol}")
        steps.append("divide by smallest mole value")
        ratio_str = ", ".join(
            f"{elem}:{r}" for elem, r in sd["ratios"]
        )
        steps.append(f"ratios: {ratio_str}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Empirical formula.
        """
        return sd["formula"]


# ---------------------------------------------------------------------------
# 4. Solution Dilution (tier 3)
# ---------------------------------------------------------------------------

@register
class SolutionDilutionGenerator(StepGenerator):
    """Apply the dilution equation C1*V1 = C2*V2.

    Given three of the four variables, computes the fourth. At higher
    difficulty, mixes two solutions of different concentrations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "solution_dilution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "compute dilution via C1V1=C2V2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dilution problem.

        At low difficulty, solves for one missing variable. At high
        difficulty, mixes two solutions to find final concentration.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            c1 = round(self._rng.uniform(0.5, 6.0), 4)
            v1 = round(self._rng.uniform(10, 500), 2)
            v2 = round(self._rng.uniform(v1, v1 * 5), 2)
            c2 = round(c1 * v1 / v2, 4)
            unknown = self._rng.choice(["C2", "V2"])

            if unknown == "C2":
                return (
                    f"C1={c1} M, V1={v1} mL, V2={v2} mL. Find C2.",
                    {"c1": c1, "v1": v1, "c2": c2, "v2": v2,
                     "unknown": "C2", "answer": c2},
                )
            else:
                return (
                    f"C1={c1} M, V1={v1} mL, C2={c2} M. Find V2.",
                    {"c1": c1, "v1": v1, "c2": c2, "v2": v2,
                     "unknown": "V2", "answer": v2},
                )
        else:
            c1 = round(self._rng.uniform(1.0, 6.0), 4)
            v1 = round(self._rng.uniform(50, 300), 2)
            c2 = round(self._rng.uniform(0.1, c1), 4)
            v2 = round(self._rng.uniform(50, 300), 2)
            c_final = round(
                (c1 * v1 + c2 * v2) / (v1 + v2), 4
            )
            return (
                f"Mix: {v1} mL of {c1} M + {v2} mL of {c2} M. "
                f"Find final concentration.",
                {"c1": c1, "v1": v1, "c2": c2, "v2": v2,
                 "unknown": "C_mix", "answer": c_final},
            )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        if sd["unknown"] == "C_mix":
            return [
                f"moles1 = {sd['c1']}*{sd['v1']}/1000",
                f"moles2 = {sd['c2']}*{sd['v2']}/1000",
                f"C_final = total moles / total volume",
            ]
        return [
            "C1*V1 = C2*V2",
            f"{sd['unknown']} = solve for unknown",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Computed value with units.
        """
        if sd["unknown"] == "V2":
            return f"{sd['answer']} mL"
        return f"{sd['answer']} M"


# ---------------------------------------------------------------------------
# 5. Combined Gas Law (tier 4)
# ---------------------------------------------------------------------------

@register
class GasLawCombinedGenerator(StepGenerator):
    """Apply the combined gas law P1V1/T1 = P2V2/T2.

    Given five of the six variables, computes the sixth.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gas_law_combined"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ideal_gas"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "apply combined gas law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a combined gas law problem.

        Creates two states of a gas and asks for one missing variable.

        Args:
            difficulty: Controls variable ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p1 = round(self._rng.uniform(0.5, 5.0), 4)
        v1 = round(self._rng.uniform(1.0, 20.0), 4)
        t1 = self._rng.randint(200, 500)
        p2 = round(self._rng.uniform(0.5, 5.0), 4)
        t2 = self._rng.randint(200, 500)
        v2 = round(p1 * v1 * t2 / (t1 * p2), 4)

        unknowns = ["P2", "V2", "T2"]
        unknown = self._rng.choice(unknowns)

        if unknown == "P2":
            answer = round(p1 * v1 * t2 / (t1 * v2), 4)
            problem = (
                f"P1={p1} atm, V1={v1} L, T1={t1} K, "
                f"V2={v2} L, T2={t2} K. Find P2."
            )
        elif unknown == "V2":
            answer = v2
            problem = (
                f"P1={p1} atm, V1={v1} L, T1={t1} K, "
                f"P2={p2} atm, T2={t2} K. Find V2."
            )
        else:
            answer = round(t1 * p2 * v2 / (p1 * v1), 4)
            problem = (
                f"P1={p1} atm, V1={v1} L, T1={t1} K, "
                f"P2={p2} atm, V2={v2} L. Find T2."
            )

        return (
            problem,
            {"p1": p1, "v1": v1, "t1": t1,
             "p2": p2, "v2": v2, "t2": t2,
             "unknown": unknown, "answer": answer},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "P1*V1/T1 = P2*V2/T2",
            f"rearrange to solve for {sd['unknown']}",
            f"{sd['unknown']} = {sd['answer']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Computed value with units.
        """
        units = {"P2": "atm", "V2": "L", "T2": "K"}
        return f"{sd['answer']} {units[sd['unknown']]}"


# ---------------------------------------------------------------------------
# 6. Dalton's Law of Partial Pressures (tier 4)
# ---------------------------------------------------------------------------

@register
class DaltonPartialPressureGenerator(StepGenerator):
    """Compute partial pressures using Dalton's law.

    P_total = sum(P_i). P_i = x_i * P_total where x_i is the
    mole fraction of gas i.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dalton_partial_pressure"

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
        return "compute partial pressures via Dalton's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Dalton's law problem.

        Creates a gas mixture with 2-4 components, assigns mole fractions,
        and computes partial pressures.

        Args:
            difficulty: Controls number of gases.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        gases = ["N2", "O2", "CO2", "He", "Ar", "H2"]
        num_gases = min(2 + difficulty // 2, 4)
        chosen = self._rng.sample(gases, num_gases)
        p_total = round(self._rng.uniform(0.5, 5.0), 4)

        # Generate random moles and derive fractions
        moles = [self._rng.uniform(0.5, 5.0) for _ in chosen]
        total_moles = sum(moles)
        fractions = [round(m / total_moles, 4) for m in moles]

        partials = [round(x * p_total, 4) for x in fractions]

        gas_str = ", ".join(
            f"{g}: x={x}" for g, x in zip(chosen, fractions)
        )

        return (
            f"P_total={p_total} atm. {gas_str}. Find partial pressures.",
            {"gases": chosen, "fractions": fractions,
             "p_total": p_total, "partials": partials},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = ["P_i = x_i * P_total"]
        for g, x, p in zip(sd["gases"], sd["fractions"], sd["partials"]):
            steps.append(f"P_{g} = {x} * {sd['p_total']} = {p} atm")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Partial pressures of all gases.
        """
        parts = [
            f"P_{g}={p} atm"
            for g, p in zip(sd["gases"], sd["partials"])
        ]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 7. Acid-Base Titration (tier 5)
# ---------------------------------------------------------------------------

@register
class AcidBaseTitrationGenerator(StepGenerator):
    """Compute equivalence point volume and pH during titration.

    At equivalence: moles acid = moles base. For strong acid-strong
    base, pH = 7. For weak acid-strong base, pH > 7 at equivalence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "acid_base_titration"

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
        return "compute titration equivalence volume and pH"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an acid-base titration problem.

        For strong-strong: computes equivalence volume and pH = 7.
        For weak-strong: computes equivalence volume and pH using Kb
        of the conjugate base.

        Args:
            difficulty: Controls acid type and complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c_acid = round(self._rng.uniform(0.05, 1.0), 4)
        v_acid = round(self._rng.uniform(10, 100), 2)
        c_base = round(self._rng.uniform(0.05, 1.0), 4)

        moles_acid = c_acid * v_acid / 1000
        v_eq = round(moles_acid / c_base * 1000, 4)

        if difficulty <= 4:
            # Strong acid-strong base
            ph_eq = 7.0
            acid_type = "strong"
        else:
            # Weak acid-strong base
            ka = round(self._rng.uniform(1e-6, 1e-3), 6)
            kb = 1e-14 / ka
            # At equivalence, all acid converted to conjugate base
            conc_cb = moles_acid / ((v_acid + v_eq) / 1000)
            oh = math.sqrt(kb * conc_cb)
            poh = -math.log10(oh) if oh > 0 else 7.0
            ph_eq = round(14.0 - poh, 4)
            acid_type = "weak"

        return (
            f"{acid_type} acid: C={c_acid} M, V={v_acid} mL. "
            f"Base: C={c_base} M. Find V_eq and pH at equivalence.",
            {"c_acid": c_acid, "v_acid": v_acid, "c_base": c_base,
             "v_eq": v_eq, "ph_eq": ph_eq, "acid_type": acid_type},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            f"moles acid = {sd['c_acid']}*{sd['v_acid']}/1000",
            f"V_eq = moles_acid/C_base * 1000 = {sd['v_eq']} mL",
            f"acid type: {sd['acid_type']}",
        ]
        if sd["acid_type"] == "strong":
            steps.append("strong-strong: pH = 7.0 at equivalence")
        else:
            steps.append("weak-strong: pH > 7 at equivalence (conjugate base)")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Equivalence volume and pH.
        """
        return f"V_eq={sd['v_eq']} mL, pH={sd['ph_eq']}"


# ---------------------------------------------------------------------------
# 8. Buffer Capacity / Henderson-Hasselbalch (tier 5)
# ---------------------------------------------------------------------------

@register
class BufferCapacityGenerator(StepGenerator):
    """Compute buffer pH using the Henderson-Hasselbalch equation.

    pH = pKa + log([A-]/[HA]). After adding strong acid or base,
    recalculates the ratio and new pH.
    """

    BUFFERS = [
        {"acid": "CH3COOH", "base": "CH3COO-", "pKa": 4.76,
         "name": "acetate"},
        {"acid": "H2CO3", "base": "HCO3-", "pKa": 6.35,
         "name": "bicarbonate"},
        {"acid": "H2PO4-", "base": "HPO4^2-", "pKa": 7.20,
         "name": "phosphate"},
        {"acid": "NH4+", "base": "NH3", "pKa": 9.25,
         "name": "ammonium"},
        {"acid": "HF", "base": "F-", "pKa": 3.17,
         "name": "fluoride"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "buffer_capacity"

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
        return "compute buffer pH via Henderson-Hasselbalch"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a buffer pH problem.

        Creates a buffer solution, optionally adds strong acid or base,
        and computes the resulting pH.

        Args:
            difficulty: Controls whether acid/base is added.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.BUFFERS), 2 + difficulty)
        buf = self._rng.choice(self.BUFFERS[:pool_size])

        vol = round(self._rng.uniform(100, 1000), 1)  # mL
        c_ha = round(self._rng.uniform(0.1, 1.0), 4)  # M
        c_a = round(self._rng.uniform(0.1, 1.0), 4)   # M

        mol_ha = c_ha * vol / 1000
        mol_a = c_a * vol / 1000

        if difficulty >= 5:
            # Add strong acid or base
            add_type = self._rng.choice(["acid", "base"])
            add_mol = round(self._rng.uniform(0.001, min(mol_ha, mol_a) * 0.5), 4)

            if add_type == "acid":
                mol_ha_new = mol_ha + add_mol
                mol_a_new = mol_a - add_mol
            else:
                mol_ha_new = mol_ha - add_mol
                mol_a_new = mol_a + add_mol

            if mol_a_new <= 0 or mol_ha_new <= 0:
                # Fallback: no addition
                add_type = "none"
                add_mol = 0
                mol_ha_new = mol_ha
                mol_a_new = mol_a
        else:
            add_type = "none"
            add_mol = 0
            mol_ha_new = mol_ha
            mol_a_new = mol_a

        ratio = mol_a_new / mol_ha_new if mol_ha_new > 0 else 1.0
        ph = round(buf["pKa"] + math.log10(ratio), 4)

        if add_type == "none":
            problem = (
                f"{buf['name']} buffer: [{buf['acid']}]={c_ha} M, "
                f"[{buf['base']}]={c_a} M, V={vol} mL. Find pH."
            )
        else:
            problem = (
                f"{buf['name']} buffer: [{buf['acid']}]={c_ha} M, "
                f"[{buf['base']}]={c_a} M, V={vol} mL. "
                f"Add {add_mol} mol strong {add_type}. Find pH."
            )

        return (
            problem,
            {"buf": buf, "c_ha": c_ha, "c_a": c_a, "vol": vol,
             "add_type": add_type, "add_mol": add_mol,
             "ratio": round(ratio, 4), "ph": ph},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            "pH = pKa + log([A-]/[HA])",
            f"pKa = {sd['buf']['pKa']}",
        ]
        if sd["add_type"] != "none":
            steps.append(
                f"after adding {sd['add_mol']} mol {sd['add_type']}: "
                f"adjust [HA] and [A-]"
            )
        steps.append(f"[A-]/[HA] ratio = {sd['ratio']}")
        steps.append(
            f"pH = {sd['buf']['pKa']} + log({sd['ratio']})"
        )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data dict.

        Returns:
            Buffer pH.
        """
        return f"pH = {sd['ph']}"
