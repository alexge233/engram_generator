"""Environmental engineering generators -- BOD decay, dilution, AQI, carbon footprint.

4 generators across tiers 4-5 covering biochemical oxygen demand,
stream dilution mixing, air quality index interpolation, and carbon
footprint accounting.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# AQI breakpoint table (EPA standard simplified)
# ---------------------------------------------------------------------------

_AQI_BREAKPOINTS = [
    # (C_lo, C_hi, I_lo, I_hi)  for PM2.5 (ug/m3, 24h avg)
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 500.4, 301, 500),
]


# ---------------------------------------------------------------------------
# 1. BOD Decay
# ---------------------------------------------------------------------------

@register
class BODDecayGenerator(StepGenerator):
    """Compute biochemical oxygen demand using first-order decay.

    Applies BOD(t) = L_0 * (1 - e^(-k*t)) where L_0 is the ultimate
    BOD and k is the deoxygenation rate constant. Also computes the
    remaining BOD as L_0 * e^(-k*t).

    Difficulty scaling:
        Difficulty 1-3: L_0 in [50, 200], k in [0.1, 0.3], t in [1, 5].
        Difficulty 4-6: L_0 in [100, 500], k in [0.05, 0.4], t in [1, 10].
        Difficulty 7-8: L_0 in [200, 800], k in [0.02, 0.5], t in [1, 20].

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bod_decay"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute BOD exerted and remaining at time t"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BOD decay problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            l0 = self._rng.randint(50, 200)
            k = round(self._rng.uniform(0.1, 0.3), 2)
            t = self._rng.randint(1, 5)
        elif difficulty <= 6:
            l0 = self._rng.randint(100, 500)
            k = round(self._rng.uniform(0.05, 0.4), 2)
            t = self._rng.randint(1, 10)
        else:
            l0 = self._rng.randint(200, 800)
            k = round(self._rng.uniform(0.02, 0.5), 2)
            t = self._rng.randint(1, 20)

        exp_term = round(math.exp(-k * t), 4)
        bod_exerted = round(l0 * (1 - exp_term), 4)
        bod_remaining = round(l0 * exp_term, 4)

        problem = f"BOD: L_0={l0} mg/L, k={k} day^{{-1}}, t={t} days"
        return problem, {
            "l0": l0, "k": k, "t": t,
            "exp_term": exp_term,
            "bod_exerted": bod_exerted,
            "bod_remaining": bod_remaining,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for BOD decay.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the exponential decay computation.
        """
        return [
            f"e^(-k*t) = e^(-{data['k']}*{data['t']}) = {data['exp_term']}",
            f"BOD(t) = {data['l0']} * (1 - {data['exp_term']}) = "
            f"{data['bod_exerted']} mg/L",
            f"BOD_remaining = {data['l0']} * {data['exp_term']} = "
            f"{data['bod_remaining']} mg/L",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return BOD exerted and remaining.

        Args:
            data: Solution data dict.

        Returns:
            BOD values as a string.
        """
        return (
            f"BOD({data['t']}) = {data['bod_exerted']} mg/L, "
            f"remaining = {data['bod_remaining']} mg/L"
        )


# ---------------------------------------------------------------------------
# 2. Dilution Factor (Stream Mixing)
# ---------------------------------------------------------------------------

@register
class DilutionFactorGenerator(StepGenerator):
    """Compute mixed concentration from two merging streams.

    Applies C_mix = (Q_1 * C_1 + Q_2 * C_2) / (Q_1 + Q_2) where
    Q is flow rate and C is pollutant concentration.

    Difficulty scaling:
        Difficulty 1-3: Q in [10, 100], C in [1, 50].
        Difficulty 4-6: Q in [50, 500], C in [1, 200].
        Difficulty 7-8: Q in [100, 2000], C in [0.1, 500].

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dilution_factor"

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
        return "compute mixed concentration from two streams"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dilution/mixing problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            q1 = self._rng.randint(10, 100)
            q2 = self._rng.randint(10, 100)
            c1 = round(self._rng.uniform(1.0, 50.0), 2)
            c2 = round(self._rng.uniform(1.0, 50.0), 2)
        elif difficulty <= 6:
            q1 = self._rng.randint(50, 500)
            q2 = self._rng.randint(50, 500)
            c1 = round(self._rng.uniform(1.0, 200.0), 2)
            c2 = round(self._rng.uniform(1.0, 200.0), 2)
        else:
            q1 = self._rng.randint(100, 2000)
            q2 = self._rng.randint(100, 2000)
            c1 = round(self._rng.uniform(0.1, 500.0), 2)
            c2 = round(self._rng.uniform(0.1, 500.0), 2)

        q_total = q1 + q2
        mass_1 = round(q1 * c1, 4)
        mass_2 = round(q2 * c2, 4)
        mass_total = round(mass_1 + mass_2, 4)
        c_mix = round(mass_total / q_total, 4)
        dilution = round(q_total / q1, 4)

        problem = (
            f"Mixing: Q_1={q1} m^3/s, C_1={c1} mg/L, "
            f"Q_2={q2} m^3/s, C_2={c2} mg/L"
        )
        return problem, {
            "q1": q1, "q2": q2, "c1": c1, "c2": c2,
            "q_total": q_total, "mass_1": mass_1, "mass_2": mass_2,
            "mass_total": mass_total, "c_mix": c_mix,
            "dilution": dilution,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for stream mixing.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the mass balance computation.
        """
        return [
            f"Q_total = {data['q1']} + {data['q2']} = {data['q_total']} m^3/s",
            f"mass_1 = {data['q1']}*{data['c1']} = {data['mass_1']}",
            f"mass_2 = {data['q2']}*{data['c2']} = {data['mass_2']}",
            f"C_mix = ({data['mass_1']}+{data['mass_2']}) / "
            f"{data['q_total']} = {data['c_mix']} mg/L",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mixed concentration.

        Args:
            data: Solution data dict.

        Returns:
            Mixed concentration as a string.
        """
        return f"C_mix = {data['c_mix']} mg/L"


# ---------------------------------------------------------------------------
# 3. Air Quality Index
# ---------------------------------------------------------------------------

@register
class AirQualityIndexGenerator(StepGenerator):
    """Compute AQI from pollutant concentration using breakpoint interpolation.

    Uses EPA-style breakpoint table for PM2.5 (24-hour average).
    Linear interpolation: AQI = (I_hi - I_lo)/(C_hi - C_lo) * (C - C_lo) + I_lo.

    Difficulty scaling:
        Difficulty 1-3: concentration 0-35 (Good to Moderate).
        Difficulty 4-6: concentration 0-150 (Good to Unhealthy).
        Difficulty 7-8: concentration 0-500 (full range).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "air_quality_index"

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
        return "compute AQI from PM2.5 concentration"

    def _find_breakpoint(self, conc: float) -> tuple[float, float, int, int]:
        """Find the breakpoint bracket for a given concentration.

        Args:
            conc: Pollutant concentration.

        Returns:
            Tuple (C_lo, C_hi, I_lo, I_hi).
        """
        for c_lo, c_hi, i_lo, i_hi in _AQI_BREAKPOINTS:
            if c_lo <= conc <= c_hi:
                return c_lo, c_hi, i_lo, i_hi
        return _AQI_BREAKPOINTS[-1]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an AQI computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            max_idx = 1
        elif difficulty <= 6:
            max_idx = 3
        else:
            max_idx = len(_AQI_BREAKPOINTS) - 1

        bracket_idx = self._rng.randint(0, max_idx)
        c_lo, c_hi, i_lo, i_hi = _AQI_BREAKPOINTS[bracket_idx]
        conc = round(self._rng.uniform(c_lo + 0.1, c_hi - 0.1), 1)

        slope = round((i_hi - i_lo) / (c_hi - c_lo), 4)
        aqi = round(slope * (conc - c_lo) + i_lo, 4)

        problem = f"AQI: PM2.5 = {conc} ug/m^3"
        return problem, {
            "conc": conc, "c_lo": c_lo, "c_hi": c_hi,
            "i_lo": i_lo, "i_hi": i_hi,
            "slope": slope, "aqi": aqi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for AQI interpolation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing breakpoint lookup and interpolation.
        """
        return [
            f"breakpoint: C in [{data['c_lo']}, {data['c_hi']}], "
            f"I in [{data['i_lo']}, {data['i_hi']}]",
            f"slope = ({data['i_hi']}-{data['i_lo']}) / "
            f"({data['c_hi']}-{data['c_lo']}) = {data['slope']}",
            f"AQI = {data['slope']} * ({data['conc']}-{data['c_lo']}) "
            f"+ {data['i_lo']} = {data['aqi']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed AQI.

        Args:
            data: Solution data dict.

        Returns:
            AQI as a string.
        """
        return f"AQI = {data['aqi']}"


# ---------------------------------------------------------------------------
# 4. Carbon Footprint
# ---------------------------------------------------------------------------

@register
class CarbonFootprintGenerator(StepGenerator):
    """Compute total CO2-equivalent emissions from activities.

    Applies CO2_eq = sum(activity_i * emission_factor_i) for a set of
    activities. Compares the total to a per-capita target.

    Difficulty scaling:
        Difficulty 1-3: 2 activities, small factors.
        Difficulty 4-6: 3-4 activities, mixed factors.
        Difficulty 7-8: 5-6 activities, varied factors.

    Prerequisites:
        multiplication.
    """

    _ACTIVITIES = [
        ("electricity_kWh", 0.3, 0.9),
        ("natural_gas_m3", 1.5, 3.0),
        ("petrol_L", 2.0, 3.5),
        ("diesel_L", 2.5, 3.8),
        ("flight_km", 0.1, 0.3),
        ("beef_kg", 20.0, 30.0),
        ("dairy_kg", 1.5, 4.0),
        ("waste_kg", 0.5, 1.5),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carbon_footprint"

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
        return "compute total CO2-equivalent emissions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a carbon footprint problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_activities = min(2 + (difficulty - 1) // 2, 6)
        selected = self._rng.sample(self._ACTIVITIES, n_activities)

        items = []
        for name, ef_lo, ef_hi in selected:
            amount = round(self._rng.uniform(5.0, 50.0 * difficulty), 2)
            ef = round(self._rng.uniform(ef_lo, ef_hi), 4)
            co2 = round(amount * ef, 4)
            items.append({
                "name": name, "amount": amount, "ef": ef, "co2": co2,
            })

        total = round(sum(it["co2"] for it in items), 4)
        target = round(self._rng.uniform(500.0, 2000.0), 2)
        diff = round(total - target, 4)
        over = diff > 0

        parts = ", ".join(
            f"{it['name']}={it['amount']} (EF={it['ef']})" for it in items
        )
        problem = f"Carbon: {parts}, target={target} kg CO2"
        return problem, {
            "items": items, "total": total,
            "target": target, "diff": diff, "over": over,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for carbon footprint.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each activity's contribution and total.
        """
        steps = []
        for it in data["items"]:
            steps.append(
                f"{it['name']}: {it['amount']} * {it['ef']} = "
                f"{it['co2']} kg CO2"
            )
        steps.append(f"total = {data['total']} kg CO2")
        status = "over" if data["over"] else "under"
        steps.append(
            f"vs target {data['target']}: {status} by "
            f"{abs(data['diff'])} kg"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total emissions and target comparison.

        Args:
            data: Solution data dict.

        Returns:
            Total CO2 and comparison as a string.
        """
        status = "OVER" if data["over"] else "UNDER"
        return f"total = {data['total']} kg CO2, {status} target"
