"""Extended chemistry generators.

6 generators across tiers 3-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class IdealGasMixtureGenerator(StepGenerator):
    """Calculate partial and total pressure of an ideal gas mixture.

    Applies Dalton's law: P_total = sum(n_i * R * T / V) where each
    component contributes a partial pressure proportional to its moles.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ideal_gas_mixture"

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
            Short task description.
        """
        return "ideal gas mixture pressures"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ideal gas mixture problem.

        Args:
            difficulty: Controls number of gas components.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        gases = ["N2", "O2", "CO2", "He", "Ar", "H2"]
        n_gases = min(2 + difficulty // 2, 4)
        chosen = self._rng.sample(gases, n_gases)
        moles = [round(self._rng.uniform(0.5, 5.0), 2) for _ in range(n_gases)]
        temp = self._rng.randint(273, 400)
        volume = round(self._rng.uniform(5.0, 25.0), 1)
        r_const = 8.314

        partials: list[tuple[str, float, float]] = []
        total_p = 0.0
        for i, gas in enumerate(chosen):
            p = round(moles[i] * r_const * temp / (volume * 1000), 4)
            partials.append((gas, moles[i], p))
            total_p += p
        total_p = round(total_p, 4)

        gas_str = ", ".join(
            f"{moles[i]} mol {chosen[i]}" for i in range(n_gases)
        )
        problem = f"{gas_str} in {volume} L at {temp} K"
        return problem, {
            "gases": chosen, "moles": moles, "temp": temp,
            "volume": volume, "partials": partials,
            "total_p": total_p,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show partial pressure computations.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"PV = nRT, R = 8.314 J/(mol*K)"]
        for gas, n, p in sd["partials"]:
            steps.append(f"P({gas}) = {n}*8.314*{sd['temp']}/{sd['volume']*1000} = {p} kPa")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return total and partial pressures.

        Args:
            sd: Solution data dict.

        Returns:
            Total pressure.
        """
        return f"P_total = {sd['total_p']} kPa"


@register
class EnthalpyReactionGenerator(StepGenerator):
    """Calculate enthalpy of reaction using Hess's law.

    dH_rxn = sum(dH_f products) - sum(dH_f reactants) using
    standard formation enthalpies.
    """

    FORMATION_ENTHALPIES = {
        "H2O(l)": -285.8, "CO2(g)": -393.5, "NH3(g)": -45.9,
        "CH4(g)": -74.6, "C2H6(g)": -84.0, "NO2(g)": 33.2,
        "SO2(g)": -296.8, "HCl(g)": -92.3, "NaCl(s)": -411.2,
        "CaCO3(s)": -1206.9, "Fe2O3(s)": -824.2,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "enthalpy_reaction"

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
            Short task description.
        """
        return "calculate reaction enthalpy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an enthalpy of reaction problem.

        Args:
            difficulty: Controls number of species.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        compounds = list(self.FORMATION_ENTHALPIES.keys())
        n_prod = self._rng.randint(1, min(3, 1 + difficulty // 2))
        n_react = self._rng.randint(1, min(3, 1 + difficulty // 2))
        all_chosen = self._rng.sample(compounds, n_prod + n_react)
        products = all_chosen[:n_prod]
        reactants = all_chosen[n_prod:]

        prod_coeffs = [self._rng.randint(1, 3) for _ in range(n_prod)]
        react_coeffs = [self._rng.randint(1, 3) for _ in range(n_react)]

        sum_prod = sum(
            prod_coeffs[i] * self.FORMATION_ENTHALPIES[products[i]]
            for i in range(n_prod)
        )
        sum_react = sum(
            react_coeffs[i] * self.FORMATION_ENTHALPIES[reactants[i]]
            for i in range(n_react)
        )
        dh = round(sum_prod - sum_react, 4)

        react_str = " + ".join(
            f"{react_coeffs[i]} {reactants[i]}" for i in range(n_react)
        )
        prod_str = " + ".join(
            f"{prod_coeffs[i]} {products[i]}" for i in range(n_prod)
        )
        problem = f"{react_str} -> {prod_str}. dH_rxn?"
        return problem, {
            "products": products, "reactants": reactants,
            "prod_coeffs": prod_coeffs, "react_coeffs": react_coeffs,
            "sum_prod": round(sum_prod, 4),
            "sum_react": round(sum_react, 4), "dh": dh,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show Hess's law computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = ["dH = sum(dH_f products) - sum(dH_f reactants)"]
        for i, p in enumerate(sd["products"]):
            steps.append(
                f"{sd['prod_coeffs'][i]}*dH_f({p}) = "
                f"{round(sd['prod_coeffs'][i] * self.FORMATION_ENTHALPIES[p], 4)}"
            )
        for i, r in enumerate(sd["reactants"]):
            steps.append(
                f"{sd['react_coeffs'][i]}*dH_f({r}) = "
                f"{round(sd['react_coeffs'][i] * self.FORMATION_ENTHALPIES[r], 4)}"
            )
        steps.append(f"dH = {sd['sum_prod']} - {sd['sum_react']} = {sd['dh']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the reaction enthalpy.

        Args:
            sd: Solution data dict.

        Returns:
            dH in kJ/mol.
        """
        return f"dH = {sd['dh']} kJ/mol"


@register
class SolubilityRulesGenerator(StepGenerator):
    """Determine if an ionic compound is soluble or insoluble.

    Applies standard solubility rules for common ionic compounds.
    """

    RULES: list[tuple[str, str, str, bool]] = [
        ("Na", "Cl", "NaCl", True),
        ("K", "NO3", "KNO3", True),
        ("Ag", "Cl", "AgCl", False),
        ("Ba", "SO4", "BaSO4", False),
        ("Ca", "CO3", "CaCO3", False),
        ("Na", "OH", "NaOH", True),
        ("Fe", "OH", "Fe(OH)3", False),
        ("Pb", "I", "PbI2", False),
        ("K", "Cl", "KCl", True),
        ("Na", "SO4", "Na2SO4", True),
        ("Ca", "OH", "Ca(OH)2", False),
        ("Mg", "Cl", "MgCl2", True),
        ("Ag", "NO3", "AgNO3", True),
        ("Pb", "Cl", "PbCl2", False),
        ("Ba", "Cl", "BaCl2", True),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "solubility_rules"

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
            Short task description.
        """
        return "apply solubility rules"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a solubility problem.

        Args:
            difficulty: Controls which compounds are tested.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = self._rng.randint(0, min(len(self.RULES) - 1, 4 + difficulty * 2))
        cation, anion, formula, soluble = self.RULES[idx]

        if soluble:
            reason = f"{cation} compounds with {anion} are generally soluble"
        else:
            reason = f"{formula} is an exception: insoluble"

        problem = f"Is {formula} soluble in water?"
        return problem, {
            "cation": cation, "anion": anion,
            "formula": formula, "soluble": soluble,
            "reason": reason,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the solubility rule applied.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"compound: {sd['formula']}",
            f"cation: {sd['cation']}, anion: {sd['anion']}",
            sd["reason"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return soluble or insoluble.

        Args:
            sd: Solution data dict.

        Returns:
            SOLUBLE or INSOLUBLE.
        """
        return "SOLUBLE" if sd["soluble"] else "INSOLUBLE"


@register
class OxidationNumberChangeGenerator(StepGenerator):
    """Identify oxidation and reduction in a redox reaction.

    Given a reaction, determines which element is oxidised (ON increases)
    and which is reduced (ON decreases).
    """

    REACTIONS: list[dict] = [
        {"eq": "2Fe + 3Cl2 -> 2FeCl3",
         "oxidised": "Fe", "ox_from": 0, "ox_to": 3,
         "reduced": "Cl", "red_from": 0, "red_to": -1},
        {"eq": "Zn + CuSO4 -> ZnSO4 + Cu",
         "oxidised": "Zn", "ox_from": 0, "ox_to": 2,
         "reduced": "Cu", "red_from": 2, "red_to": 0},
        {"eq": "2Na + 2H2O -> 2NaOH + H2",
         "oxidised": "Na", "ox_from": 0, "ox_to": 1,
         "reduced": "H", "red_from": 1, "red_to": 0},
        {"eq": "2Mg + O2 -> 2MgO",
         "oxidised": "Mg", "ox_from": 0, "ox_to": 2,
         "reduced": "O", "red_from": 0, "red_to": -2},
        {"eq": "Cu + 2AgNO3 -> Cu(NO3)2 + 2Ag",
         "oxidised": "Cu", "ox_from": 0, "ox_to": 2,
         "reduced": "Ag", "red_from": 1, "red_to": 0},
        {"eq": "2Al + 3H2SO4 -> Al2(SO4)3 + 3H2",
         "oxidised": "Al", "ox_from": 0, "ox_to": 3,
         "reduced": "H", "red_from": 1, "red_to": 0},
        {"eq": "Fe2O3 + 3CO -> 2Fe + 3CO2",
         "oxidised": "C", "ox_from": 2, "ox_to": 4,
         "reduced": "Fe", "red_from": 3, "red_to": 0},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oxidation_number_change"

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
            Short task description.
        """
        return "identify redox changes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an oxidation number change problem.

        Args:
            difficulty: Controls reaction complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = self._rng.randint(
            0, min(len(self.REACTIONS) - 1, 2 + difficulty)
        )
        rxn = self.REACTIONS[idx]
        problem = f"{rxn['eq']}. oxidised? reduced?"
        return problem, dict(rxn)

    def _create_steps(self, sd: dict) -> list[str]:
        """Show oxidation number changes.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"{sd['oxidised']}: ON {sd['ox_from']} -> {sd['ox_to']} (oxidised, loses electrons)",
            f"{sd['reduced']}: ON {sd['red_from']} -> {sd['red_to']} (reduced, gains electrons)",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return oxidised and reduced elements.

        Args:
            sd: Solution data dict.

        Returns:
            Oxidised and reduced element names.
        """
        return f"oxidised={sd['oxidised']}, reduced={sd['reduced']}"


@register
class GasEffusionGenerator(StepGenerator):
    """Compare effusion rates using Graham's law.

    rate1/rate2 = sqrt(M2/M1) where M is the molar mass.
    """

    GASES: dict[str, float] = {
        "H2": 2.016, "He": 4.003, "N2": 28.014, "O2": 31.998,
        "Ar": 39.948, "CO2": 44.009, "CH4": 16.043, "Ne": 20.180,
        "Cl2": 70.906, "SO2": 64.066,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gas_effusion"

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
            Short task description.
        """
        return "Graham's law effusion rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gas effusion problem.

        Args:
            difficulty: Controls gas selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        gas_names = list(self.GASES.keys())
        g1, g2 = self._rng.sample(gas_names, 2)
        m1 = self.GASES[g1]
        m2 = self.GASES[g2]
        ratio = round(math.sqrt(m2 / m1), 4)

        problem = (
            f"Graham's law: rate of {g1} vs {g2}? "
            f"M({g1})={m1}, M({g2})={m2}"
        )
        return problem, {
            "g1": g1, "g2": g2, "m1": m1, "m2": m2,
            "ratio": ratio,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show Graham's law computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"rate({sd['g1']})/rate({sd['g2']}) = sqrt(M2/M1)",
            f"= sqrt({sd['m2']}/{sd['m1']})",
            f"= {sd['ratio']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the effusion rate ratio.

        Args:
            sd: Solution data dict.

        Returns:
            Rate ratio.
        """
        return f"rate({sd['g1']})/rate({sd['g2']}) = {sd['ratio']}"


@register
class CalorimetryGenerator(StepGenerator):
    """Solve a calorimetry mixing problem.

    When hot and cold water are mixed: m_h*c*dT_h = m_c*c*dT_c.
    Finds the final equilibrium temperature.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "calorimetry"

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
            Short task description.
        """
        return "calorimetry mixing problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a calorimetry problem.

        Args:
            difficulty: Controls mass and temperature ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m_hot = round(self._rng.uniform(50, 200 + 50 * difficulty), 1)
        m_cold = round(self._rng.uniform(50, 200 + 50 * difficulty), 1)
        t_hot = self._rng.randint(60, 95)
        t_cold = self._rng.randint(5, 25)
        c = 4.184

        t_final = round(
            (m_hot * t_hot + m_cold * t_cold) / (m_hot + m_cold), 4
        )
        q = round(m_hot * c * (t_hot - t_final), 4)

        problem = (
            f"mix {m_hot}g water at {t_hot}C with "
            f"{m_cold}g water at {t_cold}C. T_final?"
        )
        return problem, {
            "m_hot": m_hot, "m_cold": m_cold,
            "t_hot": t_hot, "t_cold": t_cold,
            "c": c, "t_final": t_final, "q": q,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show calorimetry computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            "m_h*c*(T_h - T_f) = m_c*c*(T_f - T_c)",
            f"T_f = (m_h*T_h + m_c*T_c)/(m_h + m_c)",
            f"= ({sd['m_hot']}*{sd['t_hot']} + {sd['m_cold']}*{sd['t_cold']})"
            f"/({sd['m_hot']}+{sd['m_cold']})",
            f"= {sd['t_final']} C",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final temperature.

        Args:
            sd: Solution data dict.

        Returns:
            Final temperature in degrees C.
        """
        return f"T_final = {sd['t_final']} C"
