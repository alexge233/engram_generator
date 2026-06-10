"""Climate science generators -- radiative forcing, energy balance, and carbon budgets.

6 generators covering radiative forcing from CO2, albedo energy absorption,
greenhouse effect temperature, carbon budget estimation, thermal sea level
rise, and equilibrium climate sensitivity across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _round4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


# Stefan-Boltzmann constant (W m^-2 K^-4)
_STEFAN_BOLTZMANN = 5.670374419e-8


# ===================================================================
# 1. RADIATIVE FORCING (tier 5)
# ===================================================================

@register
class RadiativeForcingGenerator(StepGenerator):
    """Compute radiative forcing from a change in CO2 concentration.

    Uses the simplified formula RF = 5.35 * ln(C / C_0) where C is
    the current CO2 concentration and C_0 is the reference
    (pre-industrial) concentration, both in ppm. Result in W/m^2.

    Difficulty scaling:
        Difficulty 1-3: C_0 = 280 ppm, C near doubling (400-560).
        Difficulty 4-6: C_0 = 280 ppm, C in [350, 700].
        Difficulty 7-8: C_0 = 280 ppm, C in [300, 1120] (up to 4x).

    Prerequisites:
        logarithm (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "radiative_forcing"

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
            difficulty: Controls concentration range.

        Returns:
            Task description string.
        """
        return "compute radiative forcing RF = 5.35 * ln(C/C_0) in W/m^2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a radiative forcing problem.

        Args:
            difficulty: Controls concentration range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c_0 = 280

        if difficulty <= 3:
            c = self._rng.randint(400, 560)
        elif difficulty <= 6:
            c = self._rng.randint(350, 700)
        else:
            c = self._rng.randint(300, 1120)

        ratio = _round4(c / c_0)
        ln_ratio = _round4(math.log(ratio))
        rf = _round4(5.35 * ln_ratio)

        problem = f"CO2: C_0={c_0} ppm, C={c} ppm. Compute RF (W/m^2)."
        return problem, {
            "c_0": c_0, "c": c, "ratio": ratio,
            "ln_ratio": ln_ratio, "rf": rf,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate radiative forcing computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the ratio, log, and final multiplication.
        """
        return [
            f"C/C_0 = {data['c']}/{data['c_0']} = {data['ratio']}",
            f"ln({data['ratio']}) = {data['ln_ratio']}",
            f"RF = 5.35 * {data['ln_ratio']} = {data['rf']} W/m^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the radiative forcing value.

        Args:
            data: Solution data.

        Returns:
            RF in W/m^2 as a string.
        """
        return f"RF = {data['rf']} W/m^2"


# ===================================================================
# 2. ALBEDO ENERGY (tier 4)
# ===================================================================

@register
class AlbedoEnergyGenerator(StepGenerator):
    """Compute absorbed solar energy from solar constant and albedo.

    Uses Absorbed = S_0 * (1 - alpha) / 4 where S_0 is the solar
    constant (W/m^2) and alpha is the planetary albedo. The factor
    of 4 accounts for the ratio of cross-sectional to surface area.

    Difficulty scaling:
        Difficulty 1-3: S_0 = 1361, simple alpha (0.3, 0.31, 0.29).
        Difficulty 4-6: S_0 in [1350, 1370], alpha in [0.2, 0.4].
        Difficulty 7-8: variable S_0, alpha to 2 decimal places.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "albedo_energy"

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
            difficulty: Controls parameter precision.

        Returns:
            Task description string.
        """
        return "compute absorbed solar energy from albedo"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an albedo energy absorption problem.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            s_0 = 1361
            alpha = self._rng.choice([0.29, 0.30, 0.31])
        elif difficulty <= 6:
            s_0 = self._rng.randint(1350, 1370)
            alpha = _round4(self._rng.uniform(0.2, 0.4))
        else:
            s_0 = self._rng.randint(1340, 1380)
            alpha = _round4(self._rng.uniform(0.15, 0.45))

        one_minus_alpha = _round4(1 - alpha)
        absorbed = _round4(s_0 * one_minus_alpha / 4)

        problem = (
            f"S_0={s_0} W/m^2, albedo={alpha}. "
            f"Compute absorbed energy (W/m^2)."
        )
        return problem, {
            "s_0": s_0, "alpha": alpha,
            "one_minus_alpha": one_minus_alpha, "absorbed": absorbed,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate albedo energy computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the absorption calculation.
        """
        return [
            f"1 - alpha = 1 - {data['alpha']} = {data['one_minus_alpha']}",
            f"absorbed = {data['s_0']} * {data['one_minus_alpha']} / 4 = {data['absorbed']} W/m^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the absorbed energy.

        Args:
            data: Solution data.

        Returns:
            Absorbed energy in W/m^2.
        """
        return f"absorbed = {data['absorbed']} W/m^2"


# ===================================================================
# 3. GREENHOUSE EFFECT (tier 5)
# ===================================================================

@register
class GreenhouseEffectGenerator(StepGenerator):
    """Compute effective radiative temperature using Stefan-Boltzmann law.

    T_eff = (S_0 * (1 - alpha) / (4 * sigma))^(1/4) where sigma is
    the Stefan-Boltzmann constant. This gives the equilibrium
    temperature a planet would have without greenhouse gases.

    Difficulty scaling:
        Difficulty 1-3: Earth-like S_0 and alpha.
        Difficulty 4-6: varied S_0 and alpha.
        Difficulty 7-8: other planet analogues.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "greenhouse_effect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls planetary parameters.

        Returns:
            Task description string.
        """
        return "compute effective temperature T_eff via Stefan-Boltzmann"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a greenhouse effect temperature problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            s_0 = 1361
            alpha = self._rng.choice([0.29, 0.30, 0.31])
        elif difficulty <= 6:
            s_0 = self._rng.randint(1300, 1400)
            alpha = _round4(self._rng.uniform(0.2, 0.4))
        else:
            s_0 = self._rng.randint(500, 2600)
            alpha = _round4(self._rng.uniform(0.1, 0.7))

        flux = _round4(s_0 * (1 - alpha) / 4)
        t_eff = _round4((flux / _STEFAN_BOLTZMANN) ** 0.25)
        t_celsius = _round4(t_eff - 273.15)

        problem = (
            f"S_0={s_0} W/m^2, alpha={alpha}. "
            f"Compute T_eff (K) using Stefan-Boltzmann."
        )
        return problem, {
            "s_0": s_0, "alpha": alpha, "flux": flux,
            "t_eff": t_eff, "t_celsius": t_celsius,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate greenhouse effect computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing flux and temperature computation.
        """
        return [
            f"flux = {data['s_0']}*(1-{data['alpha']})/4 = {data['flux']} W/m^2",
            f"T_eff = (flux/sigma)^(1/4) = ({data['flux']}/5.6704e-8)^0.25 = {data['t_eff']} K",
            f"T_eff = {data['t_eff']} K = {data['t_celsius']} C",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the effective temperature.

        Args:
            data: Solution data.

        Returns:
            Temperature in K and C.
        """
        return f"T_eff = {data['t_eff']} K ({data['t_celsius']} C)"


# ===================================================================
# 4. CARBON BUDGET (tier 4)
# ===================================================================

@register
class CarbonBudgetGenerator(StepGenerator):
    """Compute remaining carbon budget for a temperature target.

    Remaining budget = (T_target - T_current) / TCRE where TCRE is
    the transient climate response to cumulative emissions, typically
    around 1.65 K per 1000 GtCO2 (IPCC AR6 central estimate).

    Difficulty scaling:
        Difficulty 1-3: 1.5 C target, current warming 1.0-1.2 C.
        Difficulty 4-6: variable targets (1.5-2.0 C), varying TCRE.
        Difficulty 7-8: custom TCRE values, higher current warming.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carbon_budget"

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
            difficulty: Controls target and TCRE complexity.

        Returns:
            Task description string.
        """
        return "compute remaining carbon budget for temperature target"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a carbon budget problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # TCRE in K per 1000 GtCO2
        if difficulty <= 3:
            t_target = 1.5
            t_current = _round4(self._rng.uniform(1.0, 1.2))
            tcre = 1.65
        elif difficulty <= 6:
            t_target = self._rng.choice([1.5, 2.0])
            t_current = _round4(self._rng.uniform(1.0, 1.3))
            tcre = _round4(self._rng.uniform(1.4, 2.0))
        else:
            t_target = _round4(self._rng.uniform(1.5, 2.5))
            t_current = _round4(self._rng.uniform(1.1, 1.5))
            tcre = _round4(self._rng.uniform(1.0, 2.3))

        delta_t = _round4(t_target - t_current)
        # Budget in GtCO2: delta_T / (TCRE / 1000) = delta_T * 1000 / TCRE
        budget_gt = _round4(delta_t / tcre * 1000)

        problem = (
            f"T_target={t_target} C, T_current={t_current} C, "
            f"TCRE={tcre} K per 1000 GtCO2. Remaining budget?"
        )
        return problem, {
            "t_target": t_target, "t_current": t_current,
            "tcre": tcre, "delta_t": delta_t, "budget_gt": budget_gt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate carbon budget computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing temperature gap and budget calculation.
        """
        return [
            f"delta_T = {data['t_target']} - {data['t_current']} = {data['delta_t']} C",
            f"budget = {data['delta_t']} / {data['tcre']} * 1000 = {data['budget_gt']} GtCO2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the remaining carbon budget.

        Args:
            data: Solution data.

        Returns:
            Budget in GtCO2.
        """
        return f"budget = {data['budget_gt']} GtCO2"


# ===================================================================
# 5. SEA LEVEL RISE (tier 5)
# ===================================================================

@register
class SeaLevelRiseGenerator(StepGenerator):
    """Compute thermal expansion sea level rise.

    Uses dh = alpha_exp * h * dT where alpha_exp is the thermal
    expansion coefficient of seawater (typically ~2e-4 per K),
    h is the ocean depth affected, and dT is the temperature change.

    Difficulty scaling:
        Difficulty 1-3: standard alpha, shallow depth, small dT.
        Difficulty 4-6: varied alpha, moderate depth, moderate dT.
        Difficulty 7-8: full range of parameters.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sea_level_rise"

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
            difficulty: Controls parameter ranges.

        Returns:
            Task description string.
        """
        return "compute thermal expansion sea level rise dh = alpha * h * dT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sea level rise problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            alpha_exp = 0.0002
            h = self._rng.randint(100, 500)
            dt = _round4(self._rng.uniform(0.5, 1.5))
        elif difficulty <= 6:
            alpha_exp = _round4(self._rng.uniform(0.00015, 0.00025))
            h = self._rng.randint(200, 1000)
            dt = _round4(self._rng.uniform(0.5, 3.0))
        else:
            alpha_exp = _round4(self._rng.uniform(0.0001, 0.0003))
            h = self._rng.randint(300, 2000)
            dt = _round4(self._rng.uniform(1.0, 5.0))

        dh_m = _round4(alpha_exp * h * dt)
        dh_mm = _round4(dh_m * 1000)

        problem = (
            f"alpha={alpha_exp} /K, ocean depth h={h} m, "
            f"warming dT={dt} K. Sea level rise?"
        )
        return problem, {
            "alpha_exp": alpha_exp, "h": h, "dt": dt,
            "dh_m": dh_m, "dh_mm": dh_mm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sea level rise computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the multiplication and unit conversion.
        """
        return [
            f"dh = {data['alpha_exp']} * {data['h']} * {data['dt']} = {data['dh_m']} m",
            f"dh = {data['dh_m']} m = {data['dh_mm']} mm",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the sea level rise.

        Args:
            data: Solution data.

        Returns:
            Rise in metres and millimetres.
        """
        return f"dh = {data['dh_m']} m ({data['dh_mm']} mm)"


# ===================================================================
# 6. CLIMATE SENSITIVITY (tier 5)
# ===================================================================

@register
class ClimateSensitivityGenerator(StepGenerator):
    """Compute equilibrium climate sensitivity from forcing and feedback.

    ECS = RF_2x / lambda where RF_2x is the radiative forcing from
    CO2 doubling (~3.7 W/m^2) and lambda is the climate feedback
    parameter (W/m^2/K). A higher lambda means more negative feedback
    and lower sensitivity.

    Difficulty scaling:
        Difficulty 1-3: RF_2x = 3.7, lambda in [1.0, 2.0].
        Difficulty 4-6: varied RF_2x, lambda in [0.8, 2.5].
        Difficulty 7-8: full parameter ranges.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "climate_sensitivity"

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
            difficulty: Controls parameter ranges.

        Returns:
            Task description string.
        """
        return "compute equilibrium climate sensitivity ECS = RF_2x / lambda"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a climate sensitivity problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            rf_2x = 3.7
            lam = _round4(self._rng.uniform(1.0, 2.0))
        elif difficulty <= 6:
            rf_2x = _round4(self._rng.uniform(3.4, 4.0))
            lam = _round4(self._rng.uniform(0.8, 2.5))
        else:
            rf_2x = _round4(self._rng.uniform(3.0, 4.5))
            lam = _round4(self._rng.uniform(0.5, 3.0))

        ecs = _round4(rf_2x / lam)

        problem = (
            f"RF_2x={rf_2x} W/m^2, lambda={lam} W/m^2/K. "
            f"Compute ECS."
        )
        return problem, {
            "rf_2x": rf_2x, "lam": lam, "ecs": ecs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate climate sensitivity computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the division.
        """
        return [
            "ECS = RF_2x / lambda",
            f"ECS = {data['rf_2x']} / {data['lam']} = {data['ecs']} K",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the climate sensitivity.

        Args:
            data: Solution data.

        Returns:
            ECS in Kelvin as a string.
        """
        return f"ECS = {data['ecs']} K"
