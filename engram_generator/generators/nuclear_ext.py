"""Extended nuclear physics generators -- activity, dating, fission, fusion, dose.

Deepens the nuclear physics domain with activity calculations,
carbon dating, nuclear fission and fusion energy, radiation dose
calculations, and neutron moderation. Tiers range from 5 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _NuclearExtFormatter:
    """Formats numeric values for extended nuclear physics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
        """Format a numeric value, stripping unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


_f = _NuclearExtFormatter.fmt

_C2_MEV = 931.5  # c^2 in MeV/u


# ===================================================================
# 1. Activity  (tier 5)
# ===================================================================

@register
class ActivityGenerator(StepGenerator):
    """Radioactive activity: A = A_0 * exp(-lambda*t).

    Computes the activity at time t given initial activity A_0
    and decay constant lambda. Converts between Bq and Ci.
    (1 Ci = 3.7e10 Bq.)

    Difficulty scaling:
        Difficulty 1-3: compute A(t), integer half-lives.
        Difficulty 4-6: fractional times, convert Bq to Ci.
        Difficulty 7-8: given A(t), find elapsed time.

    Prerequisites:
        radioactive_decay.
    """

    _CI_TO_BQ = 3.7e10

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "activity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["radioactive_decay"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute radioactive activity at time t"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate activity parameters and compute A(t).

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        half_life = round(self._rng.uniform(5.0, 500.0), 1)
        lam = round(math.log(2) / half_life, 4)
        a0 = self._rng.randint(1000, 100000)

        if difficulty <= 3:
            n_halves = self._rng.randint(1, 3)
            t = round(n_halves * half_life, 1)
        else:
            t = round(self._rng.uniform(0.5, 3.0) * half_life, 1)

        exp_val = round(-lam * t, 4)
        a_t = round(a0 * math.exp(exp_val), 4)
        a_t_ci = round(a_t / self._CI_TO_BQ, 4)

        if difficulty >= 7:
            target = "time"
        else:
            target = "activity"

        return "A(t) = A_0 e^{-\\lambda t}", {
            "A0": a0, "half_life": half_life, "lambda": lam,
            "t": t, "exp_val": exp_val,
            "A_t": a_t, "A_t_Ci": a_t_ci,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate activity computation steps.

        Args:
            data: Solution data with A0, lambda, t.

        Returns:
            List of step strings.
        """
        if data["target"] == "activity":
            return [
                f"A0={data['A0']} Bq, lambda={_f(data['lambda'])}/s, t={data['t']}s",
                f"-lambda*t = {_f(data['exp_val'])}",
                f"A(t) = {data['A0']}*e^{{{_f(data['exp_val'])}}}",
                f"A(t) in Ci: {_f(data['A_t'])}/3.7e10",
            ]
        return [
            f"A0={data['A0']} Bq, A(t)={_f(data['A_t'])} Bq",
            f"lambda = {_f(data['lambda'])}/s",
            f"t = -ln(A/A0)/lambda = -ln({_f(data['A_t'])}/{data['A0']})/{_f(data['lambda'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the activity or elapsed time.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "activity":
            return f"A(t) = {_f(data['A_t'])} Bq = {_f(data['A_t_Ci'])} Ci"
        return f"t = {_f(data['t'])} s"


# ===================================================================
# 2. Carbon dating  (tier 5)
# ===================================================================

@register
class CarbonDatingGenerator(StepGenerator):
    """Carbon-14 dating: t = -t_half * ln(A/A_0) / ln(2).

    Given the ratio of current to original C-14 activity (or the
    fraction remaining), computes the age of the sample.
    C-14 half-life = 5730 years.

    Difficulty scaling:
        Difficulty 1-3: simple fractions (0.5, 0.25).
        Difficulty 4-6: arbitrary fractions.
        Difficulty 7-8: given activity in dpm, compute ratio first.

    Prerequisites:
        half_life.
    """

    _HALF_LIFE = 5730.0  # years

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carbon_dating"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["half_life"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine age using carbon-14 dating"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate C-14 dating parameters and compute age.

        Args:
            difficulty: Controls fraction complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_halves = self._rng.randint(1, 3)
            ratio = round(1.0 / (2 ** n_halves), 4)
        else:
            ratio = round(self._rng.uniform(0.05, 0.9), 4)

        ln_ratio = round(math.log(ratio), 4)
        ln_2 = round(math.log(2), 4)
        age = round(-self._HALF_LIFE * ln_ratio / ln_2, 4)

        data = {
            "half_life": self._HALF_LIFE,
            "ratio": ratio, "ln_ratio": ln_ratio,
            "ln_2": ln_2, "age": age,
        }

        if difficulty >= 7:
            a0_dpm = round(self._rng.uniform(13.0, 16.0), 1)
            a_dpm = round(a0_dpm * ratio, 2)
            data["A0_dpm"] = a0_dpm
            data["A_dpm"] = a_dpm

        return "t = -\\frac{t_{1/2} \\ln(A/A_0)}{\\ln 2}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate carbon dating computation steps.

        Args:
            data: Solution data with ratio and half-life.

        Returns:
            List of step strings.
        """
        steps = []
        if "A_dpm" in data:
            steps.append(f"A={data['A_dpm']} dpm, A0={data['A0_dpm']} dpm")
            steps.append(f"A/A0 = {data['A_dpm']}/{data['A0_dpm']} = {_f(data['ratio'])}")
        else:
            steps.append(f"A/A0 = {_f(data['ratio'])}")

        steps.extend([
            f"ln({_f(data['ratio'])}) = {_f(data['ln_ratio'])}",
            f"t = -{data['half_life']}*{_f(data['ln_ratio'])}/{_f(data['ln_2'])}",
        ])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the sample age.

        Args:
            data: Solution data.

        Returns:
            String with age in years.
        """
        return f"age = {_f(data['age'])} years"


# ===================================================================
# 3. Nuclear fission  (tier 6)
# ===================================================================

@register
class NuclearFissionGenerator(StepGenerator):
    """Nuclear fission energy: U-235 + n -> products + neutrons + energy.

    Computes energy released from the mass difference between
    reactants and products using E = dm * 931.5 MeV/u.

    Difficulty scaling:
        Difficulty 1-3: standard U-235 fission, fixed products.
        Difficulty 4-6: varied fission product pairs.
        Difficulty 7-8: compute energy per kg of fuel.

    Prerequisites:
        mass_defect.
    """

    _FISSIONS = [
        {
            "fuel": "U-235", "m_fuel": 235.04393,
            "prod1": "Ba-141", "m1": 140.9144, "z1": 56, "a1": 141,
            "prod2": "Kr-92", "m2": 91.9262, "z2": 36, "a2": 92,
            "neutrons": 3,
        },
        {
            "fuel": "U-235", "m_fuel": 235.04393,
            "prod1": "Xe-140", "m1": 139.9216, "z1": 54, "a1": 140,
            "prod2": "Sr-94", "m2": 93.9154, "z2": 38, "a2": 94,
            "neutrons": 2,
        },
        {
            "fuel": "U-235", "m_fuel": 235.04393,
            "prod1": "Cs-137", "m1": 136.9071, "z1": 55, "a1": 137,
            "prod2": "Rb-96", "m2": 95.9343, "z2": 37, "a2": 96,
            "neutrons": 3,
        },
    ]
    _MN = 1.008665  # neutron mass (u)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nuclear_fission"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mass_defect"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute energy released in nuclear fission"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fission reaction and compute energy.

        Args:
            difficulty: Controls product selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            rxn = self._FISSIONS[0]
        else:
            rxn = self._rng.choice(self._FISSIONS)

        m_react = round(rxn["m_fuel"] + self._MN, 4)
        m_prod = round(rxn["m1"] + rxn["m2"] + rxn["neutrons"] * self._MN, 4)
        dm = round(m_react - m_prod, 4)
        energy = round(dm * _C2_MEV, 4)

        data = {
            "fuel": rxn["fuel"],
            "prod1": rxn["prod1"], "prod2": rxn["prod2"],
            "neutrons": rxn["neutrons"],
            "m_react": m_react, "m_prod": m_prod,
            "dm": dm, "energy_MeV": energy,
        }

        if difficulty >= 7:
            energy_j = round(energy * 1.602e-13, 4)
            atoms_per_kg = round(6.022e23 / 0.235, 4)
            energy_per_kg = round(energy_j * atoms_per_kg, 4)
            data["energy_J"] = energy_j
            data["energy_per_kg"] = energy_per_kg

        return f"{rxn['fuel']} + n \\to {rxn['prod1']} + {rxn['prod2']} + {rxn['neutrons']}n", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fission energy computation steps.

        Args:
            data: Solution data with masses.

        Returns:
            List of step strings.
        """
        steps = [
            f"m_react = m({data['fuel']}) + m(n) = {_f(data['m_react'])} u",
            f"m_prod = m({data['prod1']}) + m({data['prod2']}) + {data['neutrons']}*m(n) = {_f(data['m_prod'])} u",
            f"dm = {_f(data['m_react'])} - {_f(data['m_prod'])} = {_f(data['dm'])} u",
            f"E = {_f(data['dm'])}*{_C2_MEV}",
        ]
        if "energy_per_kg" in data:
            steps.append(f"E/kg = E_per_atom * N_A/M")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the fission energy.

        Args:
            data: Solution data.

        Returns:
            String with energy in MeV.
        """
        ans = f"E = {_f(data['energy_MeV'])} MeV"
        if "energy_per_kg" in data:
            ans += f", E/kg = {_f(data['energy_per_kg'])} J/kg"
        return ans


# ===================================================================
# 4. Nuclear fusion  (tier 6)
# ===================================================================

@register
class NuclearFusionGenerator(StepGenerator):
    """Nuclear fusion energy: D + T -> He-4 + n + 17.6 MeV.

    Computes energy per reaction from mass difference and energy
    per kilogram of fuel for various fusion reactions.

    Difficulty scaling:
        Difficulty 1-3: D-T fusion only.
        Difficulty 4-6: D-D or D-He3 reactions.
        Difficulty 7-8: compute energy per kg of fuel mixture.

    Prerequisites:
        mass_defect.
    """

    _REACTIONS = [
        {
            "name": "D-T", "fuel": "D + T",
            "m_react": 2.014102 + 3.016049,
            "m_prod": 4.002602 + 1.008665,
            "fuel_mass_kg": (2 + 3) * 1e-3 / 6.022e23,
        },
        {
            "name": "D-D(n)", "fuel": "D + D",
            "m_react": 2.014102 + 2.014102,
            "m_prod": 3.016029 + 1.008665,
            "fuel_mass_kg": (2 + 2) * 1e-3 / 6.022e23,
        },
        {
            "name": "D-He3", "fuel": "D + He-3",
            "m_react": 2.014102 + 3.016029,
            "m_prod": 4.002602 + 1.007276,
            "fuel_mass_kg": (2 + 3) * 1e-3 / 6.022e23,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nuclear_fusion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mass_defect"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute energy released in nuclear fusion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fusion reaction and compute energy.

        Args:
            difficulty: Controls reaction selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            rxn = self._REACTIONS[0]
        else:
            rxn = self._rng.choice(self._REACTIONS)

        m_react = round(rxn["m_react"], 4)
        m_prod = round(rxn["m_prod"], 4)
        dm = round(m_react - m_prod, 4)
        energy = round(dm * _C2_MEV, 4)
        energy_j = round(energy * 1.602e-13, 4)

        data = {
            "name": rxn["name"], "fuel": rxn["fuel"],
            "m_react": m_react, "m_prod": m_prod,
            "dm": dm, "energy_MeV": energy,
            "energy_J": energy_j,
        }

        if difficulty >= 7:
            fuel_kg = rxn["fuel_mass_kg"]
            reactions_per_kg = round(1.0 / fuel_kg, 4)
            energy_per_kg = round(energy_j * reactions_per_kg, 4)
            data["reactions_per_kg"] = reactions_per_kg
            data["energy_per_kg"] = energy_per_kg

        return f"{rxn['fuel']} \\to products", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fusion energy computation steps.

        Args:
            data: Solution data with masses.

        Returns:
            List of step strings.
        """
        steps = [
            f"{data['name']}: {data['fuel']}",
            f"m_react = {_f(data['m_react'])} u",
            f"m_prod = {_f(data['m_prod'])} u",
            f"dm = {_f(data['dm'])} u",
            f"E = {_f(data['dm'])}*{_C2_MEV} = {_f(data['energy_MeV'])} MeV",
        ]
        if "energy_per_kg" in data:
            steps.append(f"E/kg = {_f(data['energy_J'])}*{_f(data['reactions_per_kg'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the fusion energy.

        Args:
            data: Solution data.

        Returns:
            String with energy in MeV.
        """
        ans = f"E = {_f(data['energy_MeV'])} MeV/reaction"
        if "energy_per_kg" in data:
            ans += f", E/kg = {_f(data['energy_per_kg'])} J/kg"
        return ans


# ===================================================================
# 5. Dose calculation  (tier 5)
# ===================================================================

@register
class DoseCalculationGenerator(StepGenerator):
    """Radiation dose: absorbed dose D = E/m (Gy), equivalent dose H = D*w_R (Sv).

    Computes absorbed dose from deposited energy and mass, then
    applies radiation weighting factor to get equivalent dose.

    Difficulty scaling:
        Difficulty 1-3: gamma radiation (w_R=1).
        Difficulty 4-6: alpha or neutron radiation (w_R=5 or 20).
        Difficulty 7-8: mixed radiation, sum contributions.

    Prerequisites:
        division.
    """

    _RADIATION_TYPES = [
        ("gamma", 1),
        ("beta", 1),
        ("alpha", 20),
        ("neutron_fast", 10),
        ("neutron_thermal", 5),
        ("proton", 2),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dose_calculation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute absorbed and equivalent radiation dose"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate dose parameters and compute D and H.

        Args:
            difficulty: Controls radiation type and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        mass = round(self._rng.uniform(1.0, 80.0), 1)

        if difficulty <= 3:
            types = [self._rng.choice(self._RADIATION_TYPES[:2])]
        elif difficulty <= 6:
            types = [self._rng.choice(self._RADIATION_TYPES)]
        else:
            n_types = self._rng.randint(2, 3)
            types = [self._rng.choice(self._RADIATION_TYPES) for _ in range(n_types)]

        contributions = []
        total_h = 0.0
        total_d = 0.0
        for rad_name, w_r in types:
            energy_mj = round(self._rng.uniform(0.1, 10.0), 2)
            energy_j = energy_mj * 1e-3
            d = round(energy_j / mass, 4)
            h = round(d * w_r, 4)
            contributions.append({
                "type": rad_name, "w_R": w_r,
                "E_mJ": energy_mj, "E_J": energy_j,
                "D": d, "H": h,
            })
            total_d += d
            total_h += h

        total_d = round(total_d, 4)
        total_h = round(total_h, 4)

        return "D = E/m, H = D \\cdot w_R", {
            "mass": mass, "contributions": contributions,
            "D_total": total_d, "H_total": total_h,
            "n_types": len(types),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dose computation steps.

        Args:
            data: Solution data with radiation contributions.

        Returns:
            List of step strings.
        """
        steps = [f"mass = {data['mass']} kg"]
        for c in data["contributions"]:
            steps.append(
                f"{c['type']}: E={c['E_mJ']}mJ, D={_f(c['D'])}Gy, "
                f"w_R={c['w_R']}, H={_f(c['H'])}Sv"
            )
        if data["n_types"] > 1:
            steps.append(f"total D = {_f(data['D_total'])} Gy")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total dose.

        Args:
            data: Solution data.

        Returns:
            String with D and H.
        """
        return f"D = {_f(data['D_total'])} Gy, H = {_f(data['H_total'])} Sv"


# ===================================================================
# 6. Neutron moderation  (tier 5)
# ===================================================================

@register
class NeutronModerationGenerator(StepGenerator):
    """Neutron moderation: average log energy loss per collision.

    xi = 1 + ((A-1)^2 / (2A)) * ln((A-1)/(A+1)).
    Number of collisions to thermalise from E_fast to E_thermal:
    n = ln(E_fast/E_thermal) / xi.

    Difficulty scaling:
        Difficulty 1-3: hydrogen (A=1, xi=1).
        Difficulty 4-6: common moderators (C, D2O).
        Difficulty 7-8: heavy moderators, compute n collisions.

    Prerequisites:
        logarithm.
    """

    _MODERATORS = [
        ("hydrogen", 1),
        ("deuterium", 2),
        ("carbon", 12),
        ("oxygen", 16),
        ("beryllium", 9),
        ("iron", 56),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "neutron_moderation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute neutron moderation collisions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate moderator parameters and compute collisions.

        Args:
            difficulty: Controls moderator selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            name, a = self._MODERATORS[0]
        elif difficulty <= 6:
            name, a = self._rng.choice(self._MODERATORS[:4])
        else:
            name, a = self._rng.choice(self._MODERATORS)

        if a == 1:
            xi = 1.0
        else:
            ratio = (a - 1) / (a + 1)
            xi = round(1 + ((a - 1) ** 2 / (2 * a)) * math.log(ratio), 4)

        e_fast = 2e6  # 2 MeV fast neutron
        e_thermal = 0.025  # 0.025 eV thermal
        ln_ratio = round(math.log(e_fast / e_thermal), 4)
        n_collisions = round(ln_ratio / xi, 4) if xi > 0 else float("inf")

        return "\\xi = 1 + \\frac{(A-1)^2}{2A}\\ln\\frac{A-1}{A+1}", {
            "moderator": name, "A": a, "xi": xi,
            "E_fast": e_fast, "E_thermal": e_thermal,
            "ln_ratio": ln_ratio,
            "n_collisions": n_collisions,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate neutron moderation steps.

        Args:
            data: Solution data with moderator and xi.

        Returns:
            List of step strings.
        """
        a = data["A"]
        steps = [f"moderator: {data['moderator']}, A={a}"]
        if a == 1:
            steps.append("A=1: xi = 1 (special case)")
        else:
            steps.append(
                f"(A-1)^2/(2A) = {(a-1)**2}/(2*{a}) = {_f((a-1)**2/(2*a))}"
            )
            steps.append(
                f"ln((A-1)/(A+1)) = ln({a-1}/{a+1}) = {_f(math.log((a-1)/(a+1)))}"
            )
        steps.append(f"xi = {_f(data['xi'])}")
        steps.append(
            f"n = ln(E_fast/E_therm)/xi = {_f(data['ln_ratio'])}/{_f(data['xi'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return xi and number of collisions.

        Args:
            data: Solution data.

        Returns:
            String with xi and n.
        """
        return (
            f"xi = {_f(data['xi'])}, "
            f"n = {_f(data['n_collisions'])} collisions"
        )
