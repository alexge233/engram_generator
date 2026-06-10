"""Heat transfer generators -- conduction, convection, radiation, exchangers, fins.

Covers Fourier's law of conduction, Newton's law of cooling,
Stefan-Boltzmann radiation, LMTD heat exchangers, fin efficiency,
and thermal resistance networks. Tiers range from 4 (single-mode)
to 5 (multi-mode and composite systems).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _HeatFormatter:
    """Formats numeric values for heat transfer problems.

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


_f = _HeatFormatter.fmt

_SIGMA = 5.67e-8  # Stefan-Boltzmann constant (W/m^2*K^4)


# ===================================================================
# 1. Fourier conduction  (tier 4)
# ===================================================================

@register
class FourierConductionGenerator(StepGenerator):
    """Fourier's law of heat conduction: q = -k * A * dT / dx.

    Given thermal conductivity k, cross-sectional area A, thickness dx,
    and surface temperatures, computes the heat flux. Multi-layer walls
    at higher difficulty.

    Difficulty scaling:
        Difficulty 1-3: single layer, integer values.
        Difficulty 4-6: single layer with varied materials.
        Difficulty 7-8: multi-layer (2-3 layers) wall.

    Prerequisites:
        division.
    """

    _MATERIALS = {
        "copper": 385.0,
        "aluminum": 205.0,
        "steel": 50.0,
        "brick": 0.72,
        "glass": 1.05,
        "wood": 0.15,
        "concrete": 1.4,
        "insulation": 0.04,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fourier_conduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        if difficulty <= 6:
            return "compute heat flux using Fourier's law"
        return "compute heat flux through multi-layer wall"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate conduction problem parameters and compute heat flux.

        Args:
            difficulty: Controls number of layers.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        area = round(self._rng.uniform(0.5, 3.0 + difficulty * 0.5), 2)
        t_hot = self._rng.randint(80, 200 + difficulty * 30)
        t_cold = self._rng.randint(10, 40 + difficulty * 5)
        dt = t_hot - t_cold

        if difficulty <= 6:
            # Single layer
            mat_names = list(self._MATERIALS.keys())
            mat = self._rng.choice(mat_names)
            k = self._MATERIALS[mat]
            dx = round(
                self._rng.uniform(0.01, 0.1 + difficulty * 0.05), 3
            )
            q = round(k * area * dt / dx, 4)

            formula = "q = k A \\frac{\\Delta T}{\\Delta x}"
            return formula, {
                "mode": "single",
                "material": mat, "k": k,
                "A": area, "dx": dx,
                "T_hot": t_hot, "T_cold": t_cold, "dT": dt,
                "q": q,
            }

        # Multi-layer
        num_layers = self._rng.randint(2, 3)
        layers = []
        r_total = 0.0
        for _ in range(num_layers):
            mat = self._rng.choice(list(self._MATERIALS.keys()))
            k = self._MATERIALS[mat]
            dx = round(self._rng.uniform(0.02, 0.15), 3)
            r = round(dx / (k * area), 4)
            r_total += r
            layers.append({"material": mat, "k": k, "dx": dx, "R": r})

        r_total = round(r_total, 4)
        q = round(dt / r_total, 4)

        formula = "q = \\frac{\\Delta T}{\\sum R_i}"
        return formula, {
            "mode": "multi",
            "A": area, "layers": layers,
            "T_hot": t_hot, "T_cold": t_cold, "dT": dt,
            "R_total": r_total, "q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conduction computation steps.

        Args:
            data: Solution data with material properties and temperatures.

        Returns:
            List of step strings.
        """
        if data["mode"] == "single":
            return [
                f"{data['material']}: k={data['k']}W/mK, "
                f"A={data['A']}m^2, dx={data['dx']}m",
                f"dT = {data['T_hot']}-{data['T_cold']} = {data['dT']}K",
                f"q = {data['k']}*{data['A']}*{data['dT']}/{data['dx']}",
                f"q = {_f(data['q'])} W",
            ]

        steps = [
            f"dT = {data['T_hot']}-{data['T_cold']} = {data['dT']}K, "
            f"A={data['A']}m^2",
        ]
        for i, layer in enumerate(data["layers"]):
            steps.append(
                f"L{i+1}: {layer['material']} k={layer['k']}, "
                f"dx={layer['dx']}m, R={_f(layer['R'])} K/W"
            )
        steps.append(f"R_total = {_f(data['R_total'])} K/W")
        steps.append(f"q = {data['dT']}/{_f(data['R_total'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the heat flux.

        Args:
            data: Solution data.

        Returns:
            String with heat flux value and units.
        """
        return f"q = {_f(data['q'])} W"


# ===================================================================
# 2. Newton's law of cooling  (tier 4)
# ===================================================================

@register
class NewtonCoolingGenerator(StepGenerator):
    """Newton's law of cooling: q = h * A * (T_s - T_inf).

    Given convection coefficient h, surface area A, surface temperature
    T_s, and ambient temperature T_inf, computes the convective heat
    transfer rate.

    Difficulty scaling:
        Difficulty 1-3: simple geometry, integer values.
        Difficulty 4-6: varied h values, compute missing T.
        Difficulty 7-8: solve for h given q, or compare surfaces.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "newton_cooling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute convective heat transfer rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate convection parameters and compute heat transfer.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        h = self._rng.randint(5, 50 + difficulty * 20)
        area = round(self._rng.uniform(0.1, 2.0 + difficulty * 0.5), 2)
        t_s = self._rng.randint(60, 200 + difficulty * 30)
        t_inf = self._rng.randint(15, 35 + difficulty * 5)
        dt = t_s - t_inf
        q = round(h * area * dt, 4)

        if difficulty >= 7:
            target = self._rng.choice(["q", "h"])
        else:
            target = "q"

        formula = "q = h A (T_s - T_{\\infty})"
        return formula, {
            "h": h, "A": area,
            "T_s": t_s, "T_inf": t_inf, "dT": dt,
            "q": q, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate convection computation steps.

        Args:
            data: Solution data with convection parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "q":
            return [
                f"h={data['h']}W/m^2K, A={data['A']}m^2",
                f"T_s={data['T_s']}C, T_inf={data['T_inf']}C",
                f"dT = {data['T_s']}-{data['T_inf']} = {data['dT']}K",
                f"q = {data['h']}*{data['A']}*{data['dT']}",
                f"q = {_f(data['q'])} W",
            ]
        return [
            f"q={_f(data['q'])}W, A={data['A']}m^2",
            f"dT = {data['T_s']}-{data['T_inf']} = {data['dT']}K",
            f"h = q/(A*dT) = {_f(data['q'])}/({data['A']}*{data['dT']})",
            f"h = {data['h']} W/m^2K",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat transfer rate or convection coefficient.

        Args:
            data: Solution data.

        Returns:
            String with result and units.
        """
        if data["target"] == "q":
            return f"q = {_f(data['q'])} W"
        return f"h = {data['h']} W/m^2K"


# ===================================================================
# 3. Stefan-Boltzmann radiation  (tier 5)
# ===================================================================

@register
class StefanBoltzmannGenerator(StepGenerator):
    """Stefan-Boltzmann radiation: q = epsilon * sigma * A * (Ts^4 - Tsur^4).

    sigma = 5.67e-8 W/m^2*K^4. Computes radiative heat transfer
    between a surface and its surroundings.

    Difficulty scaling:
        Difficulty 1-3: blackbody (epsilon=1), simple temperatures.
        Difficulty 4-6: grey body (epsilon<1), higher temperatures.
        Difficulty 7-8: compute equilibrium temperature (solve for Ts).

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stefan_boltzmann"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute radiative heat transfer"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate radiation parameters and compute heat transfer.

        Args:
            difficulty: Controls emissivity and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            epsilon = 1.0
        else:
            epsilon = round(self._rng.uniform(0.1, 0.95), 2)

        area = round(self._rng.uniform(0.5, 3.0 + difficulty * 0.5), 2)
        t_s_c = self._rng.randint(100, 400 + difficulty * 50)
        t_sur_c = self._rng.randint(10, 40 + difficulty * 5)
        t_s_k = t_s_c + 273.15
        t_sur_k = t_sur_c + 273.15

        t_s4 = round(t_s_k ** 4, 4)
        t_sur4 = round(t_sur_k ** 4, 4)
        dt4 = round(t_s4 - t_sur4, 4)
        q = round(epsilon * _SIGMA * area * dt4, 4)

        formula = ("q = \\epsilon \\sigma A "
                   "(T_s^4 - T_{sur}^4)")

        return formula, {
            "epsilon": epsilon, "A": area,
            "T_s_C": t_s_c, "T_sur_C": t_sur_c,
            "T_s_K": round(t_s_k, 2), "T_sur_K": round(t_sur_k, 2),
            "T_s4": t_s4, "T_sur4": t_sur4,
            "dT4": dt4, "q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate radiation computation steps.

        Args:
            data: Solution data with temperatures and emissivity.

        Returns:
            List of step strings.
        """
        return [
            f"eps={data['epsilon']}, A={data['A']}m^2, "
            f"sigma=5.67e-8",
            f"T_s={data['T_s_C']}C={data['T_s_K']}K, "
            f"T_sur={data['T_sur_C']}C={data['T_sur_K']}K",
            f"T_s^4={_f(data['T_s4'])}, T_sur^4={_f(data['T_sur4'])}",
            f"dT^4 = {_f(data['dT4'])}",
            f"q = {data['epsilon']}*5.67e-8*{data['A']}*{_f(data['dT4'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the radiative heat transfer rate.

        Args:
            data: Solution data.

        Returns:
            String with heat flux and units.
        """
        return f"q = {_f(data['q'])} W"


# ===================================================================
# 4. Heat exchanger (LMTD)  (tier 5)
# ===================================================================

@register
class HeatExchangerGenerator(StepGenerator):
    """Heat exchanger analysis using LMTD method.

    LMTD = (dT1 - dT2) / ln(dT1/dT2). Q = U * A * LMTD.
    Handles parallel-flow and counter-flow configurations.

    Difficulty scaling:
        Difficulty 1-3: counter-flow, simple temperatures.
        Difficulty 4-6: parallel-flow, varied U values.
        Difficulty 7-8: solve for required area given Q target.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heat_exchanger"

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
        return "compute heat exchanger transfer using LMTD"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate heat exchanger parameters and compute Q.

        Args:
            difficulty: Controls flow configuration and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Hot fluid
        t_h_in = self._rng.randint(120, 250 + difficulty * 20)
        t_h_out = self._rng.randint(60, min(t_h_in - 10, 120))

        # Cold fluid
        t_c_in = self._rng.randint(15, 40 + difficulty * 5)
        t_c_out = self._rng.randint(
            t_c_in + 10, min(t_h_out - 5, t_c_in + 60)
        )

        if difficulty <= 3:
            flow = "counter"
        else:
            flow = self._rng.choice(["counter", "parallel"])

        if flow == "counter":
            dt1 = t_h_in - t_c_out
            dt2 = t_h_out - t_c_in
        else:
            dt1 = t_h_in - t_c_in
            dt2 = t_h_out - t_c_out

        # Ensure valid LMTD (both dT positive and not equal)
        if dt1 <= 0 or dt2 <= 0:
            dt1 = max(dt1, 5)
            dt2 = max(dt2, 5)

        if abs(dt1 - dt2) < 0.01:
            lmtd = round(float(dt1), 4)
        else:
            lmtd = round((dt1 - dt2) / math.log(dt1 / dt2), 4)

        u = self._rng.randint(50, 300 + difficulty * 50)
        area = round(self._rng.uniform(1.0, 10.0 + difficulty), 1)
        q = round(u * area * lmtd, 4)

        formula = ("LMTD = \\frac{\\Delta T_1 - \\Delta T_2}"
                   "{\\ln(\\Delta T_1/\\Delta T_2)}")

        return formula, {
            "flow": flow,
            "T_h_in": t_h_in, "T_h_out": t_h_out,
            "T_c_in": t_c_in, "T_c_out": t_c_out,
            "dT1": dt1, "dT2": dt2,
            "LMTD": lmtd, "U": u, "A": area, "Q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate LMTD computation steps.

        Args:
            data: Solution data with temperatures and coefficients.

        Returns:
            List of step strings.
        """
        ratio = round(data["dT1"] / data["dT2"], 4) if data["dT2"] != 0 else 0
        ln_ratio = round(math.log(ratio), 4) if ratio > 0 else 0
        return [
            f"{data['flow']}-flow: "
            f"Th={data['T_h_in']}/{data['T_h_out']}C, "
            f"Tc={data['T_c_in']}/{data['T_c_out']}C",
            f"dT1={data['dT1']}K, dT2={data['dT2']}K",
            f"ln(dT1/dT2) = ln({_f(ratio)}) = {_f(ln_ratio)}",
            f"LMTD = ({data['dT1']}-{data['dT2']})/{_f(ln_ratio)} "
            f"= {_f(data['LMTD'])}K",
            f"Q = U*A*LMTD = {data['U']}*{data['A']}*"
            f"{_f(data['LMTD'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat transfer rate.

        Args:
            data: Solution data.

        Returns:
            String with Q value and units.
        """
        return f"Q = {_f(data['Q'])} W"


# ===================================================================
# 5. Fin efficiency  (tier 5)
# ===================================================================

@register
class FinEfficiencyGenerator(StepGenerator):
    """Fin efficiency and heat transfer.

    eta = tanh(mL) / (mL) where m = sqrt(h * P / (k * A_c)).
    Fin heat transfer: q_fin = eta * h * A_fin * theta_b.

    Difficulty scaling:
        Difficulty 1-3: rectangular fin, simple values.
        Difficulty 4-6: varied fin geometry, compute m first.
        Difficulty 7-8: compare fins, or solve for required length.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fin_efficiency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute fin efficiency and heat transfer"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fin parameters and compute efficiency.

        Args:
            difficulty: Controls fin complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Rectangular fin: width w, thickness t, length L
        w_mm = self._rng.randint(20, 60 + difficulty * 10)
        t_mm = self._rng.randint(2, 5 + difficulty)
        l_mm = self._rng.randint(20, 50 + difficulty * 10)

        w = w_mm / 1000.0
        t = t_mm / 1000.0
        length = l_mm / 1000.0

        # Cross section area and perimeter
        a_c = w * t
        perimeter = 2 * (w + t)

        # Fin surface area (approximate: 2 * w * L for thin fin)
        a_fin = round(2 * w * length, 4)

        # Material and convection
        k = self._rng.choice(
            [385.0, 205.0, 50.0, 120.0][:min(difficulty, 4)]
        )
        h = self._rng.randint(10, 50 + difficulty * 15)

        # Temperature excess
        t_b = self._rng.randint(50, 150 + difficulty * 20)
        t_inf = self._rng.randint(20, 35)
        theta_b = t_b - t_inf

        # Compute m
        m = round(math.sqrt(h * perimeter / (k * a_c)), 4)
        ml = round(m * length, 4)
        eta = round(math.tanh(ml) / ml, 4) if ml > 0 else 1.0
        q_fin = round(eta * h * a_fin * theta_b, 4)

        formula = ("\\eta = \\frac{\\tanh(mL)}{mL}, "
                   "m = \\sqrt{\\frac{hP}{kA_c}}")

        return formula, {
            "w_mm": w_mm, "t_mm": t_mm, "L_mm": l_mm,
            "w": round(w, 4), "t": round(t, 4), "L": round(length, 4),
            "A_c": round(a_c, 4), "P": round(perimeter, 4),
            "A_fin": a_fin,
            "k": k, "h": h,
            "T_b": t_b, "T_inf": t_inf, "theta_b": theta_b,
            "m": m, "mL": ml, "eta": eta, "q_fin": q_fin,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fin efficiency computation steps.

        Args:
            data: Solution data with fin parameters.

        Returns:
            List of step strings.
        """
        tanh_ml = round(math.tanh(data["mL"]), 4)
        return [
            f"w={data['w_mm']}mm, t={data['t_mm']}mm, "
            f"L={data['L_mm']}mm",
            f"A_c={_f(data['A_c'])}m^2, P={_f(data['P'])}m",
            f"k={data['k']}W/mK, h={data['h']}W/m^2K",
            f"m = sqrt({data['h']}*{_f(data['P'])}"
            f"/({data['k']}*{_f(data['A_c'])})) = {_f(data['m'])}",
            f"mL = {_f(data['mL'])}, tanh(mL)={_f(tanh_ml)}",
            f"eta = {_f(tanh_ml)}/{_f(data['mL'])} = {_f(data['eta'])}",
            f"q = {_f(data['eta'])}*{data['h']}*{_f(data['A_fin'])}"
            f"*{data['theta_b']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fin efficiency and heat transfer.

        Args:
            data: Solution data.

        Returns:
            String with eta and q_fin values.
        """
        return (f"eta = {_f(data['eta'])}, "
                f"q_fin = {_f(data['q_fin'])} W")


# ===================================================================
# 6. Thermal resistance network  (tier 4)
# ===================================================================

@register
class ThermalResistanceGenerator(StepGenerator):
    """Thermal resistance network for series heat transfer.

    Conduction: R = L / (k * A). Convection: R = 1 / (h * A).
    Series total: R_total = sum(R_i). Q = dT / R_total.

    Difficulty scaling:
        Difficulty 1-3: conduction only, 1-2 layers.
        Difficulty 4-6: conduction + convection on both sides.
        Difficulty 7-8: 3 conduction layers + 2 convection layers.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thermal_resistance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute heat transfer through thermal resistance network"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate resistance network and compute heat transfer.

        Args:
            difficulty: Controls number and type of resistances.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        area = round(self._rng.uniform(0.5, 3.0 + difficulty * 0.5), 2)
        t_hot = self._rng.randint(80, 200 + difficulty * 30)
        t_cold = self._rng.randint(10, 35 + difficulty * 5)
        dt = t_hot - t_cold

        resistances = []
        r_total = 0.0

        if difficulty >= 4:
            # Inner convection
            h_inner = self._rng.randint(20, 100 + difficulty * 20)
            r_conv_in = round(1.0 / (h_inner * area), 4)
            resistances.append({
                "type": "convection",
                "label": "inner",
                "h": h_inner, "R": r_conv_in,
            })
            r_total += r_conv_in

        # Conduction layers
        if difficulty <= 3:
            num_layers = self._rng.randint(1, 2)
        elif difficulty <= 6:
            num_layers = self._rng.randint(1, 2)
        else:
            num_layers = self._rng.randint(2, 3)

        materials = ["brick", "insulation", "concrete", "steel", "wood"]
        k_values = {"brick": 0.72, "insulation": 0.04, "concrete": 1.4,
                     "steel": 50.0, "wood": 0.15}

        for i in range(num_layers):
            mat = self._rng.choice(materials)
            k = k_values[mat]
            dx = round(self._rng.uniform(0.02, 0.2), 3)
            r_cond = round(dx / (k * area), 4)
            resistances.append({
                "type": "conduction",
                "label": mat,
                "k": k, "dx": dx, "R": r_cond,
            })
            r_total += r_cond

        if difficulty >= 4:
            # Outer convection
            h_outer = self._rng.randint(5, 30 + difficulty * 5)
            r_conv_out = round(1.0 / (h_outer * area), 4)
            resistances.append({
                "type": "convection",
                "label": "outer",
                "h": h_outer, "R": r_conv_out,
            })
            r_total += r_conv_out

        r_total = round(r_total, 4)
        q = round(dt / r_total, 4)

        formula = "Q = \\frac{\\Delta T}{\\sum R_i}"

        return formula, {
            "A": area, "T_hot": t_hot, "T_cold": t_cold, "dT": dt,
            "resistances": resistances,
            "R_total": r_total, "Q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thermal resistance computation steps.

        Args:
            data: Solution data with resistances.

        Returns:
            List of step strings.
        """
        steps = [
            f"A={data['A']}m^2, "
            f"dT={data['T_hot']}-{data['T_cold']}={data['dT']}K",
        ]
        for res in data["resistances"]:
            if res["type"] == "convection":
                steps.append(
                    f"R_{res['label']} = 1/(h*A) = "
                    f"1/({res['h']}*{data['A']}) = {_f(res['R'])} K/W"
                )
            else:
                steps.append(
                    f"R_{res['label']} = dx/(k*A) = "
                    f"{res['dx']}/({res['k']}*{data['A']}) "
                    f"= {_f(res['R'])} K/W"
                )
        steps.append(f"R_total = {_f(data['R_total'])} K/W")
        steps.append(
            f"Q = {data['dT']}/{_f(data['R_total'])} = {_f(data['Q'])} W"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the overall heat transfer rate.

        Args:
            data: Solution data.

        Returns:
            String with Q value and units.
        """
        return f"Q = {_f(data['Q'])} W"
