"""Power systems generators -- three-phase power through load flow.

Covers three-phase power calculation, transformer turns ratio,
power factor correction, transmission line losses, generator
frequency, and simple load flow analysis. Tiers range from 4
(introductory) to 6 (power system analysis).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _PowerFormatter:
    """Formats numeric values for power systems problems.

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


_f = _PowerFormatter.fmt


# ===================================================================
# 1. Three-phase power  (tier 5)
# ===================================================================

@register
class ThreePhasePowerGenerator(StepGenerator):
    """Compute three-phase power: P = sqrt(3) * V_L * I_L * cos(phi).

    Given line voltage V_L, line current I_L, and power factor cos(phi),
    computes real power P, reactive power Q, and apparent power S.

    Difficulty scaling:
        Difficulty 1-3: compute P only, unity or 0.8 power factor.
        Difficulty 4-6: compute P, Q, S with varied power factors.
        Difficulty 7-8: given P and pf, solve for I_L.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "three_phase_power"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute three-phase power"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate three-phase power parameters and compute results.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        v_l = self._rng.choice([208, 240, 380, 415, 480, 690][:min(
            difficulty + 1, 6)])
        i_l = round(self._rng.uniform(5, 100 + difficulty * 50), 1)

        if difficulty <= 3:
            pf = self._rng.choice([1.0, 0.8])
        else:
            pf = round(self._rng.uniform(0.6, 1.0), 2)

        phi_rad = math.acos(pf)
        sin_phi = round(math.sin(phi_rad), 4)
        sqrt3 = round(math.sqrt(3), 4)

        s = round(sqrt3 * v_l * i_l, 4)
        p = round(s * pf, 4)
        q = round(s * sin_phi, 4)

        if difficulty >= 7:
            return "I_L = \\frac{P}{\\sqrt{3} V_L \\cos\\phi}", {
                "V_L": v_l, "I_L": i_l, "pf": pf,
                "sin_phi": sin_phi, "sqrt3": sqrt3,
                "S": s, "P": p, "Q": q,
                "target": "I_L",
            }

        return "P = \\sqrt{3} V_L I_L \\cos\\phi", {
            "V_L": v_l, "I_L": i_l, "pf": pf,
            "sin_phi": sin_phi, "sqrt3": sqrt3,
            "S": s, "P": p, "Q": q,
            "full": difficulty >= 4, "target": "P",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate three-phase power computation steps.

        Args:
            data: Solution data with V_L, I_L, power factor.

        Returns:
            List of step strings.
        """
        steps = [
            f"V_L={data['V_L']}V, I_L={_f(data['I_L'])}A, "
            f"pf={data['pf']}",
            f"S = sqrt(3)*V_L*I_L = {_f(data['S'])} VA",
            f"P = S*pf = {_f(data['P'])} W",
        ]
        if data.get("full") or data["target"] == "I_L":
            steps.append(f"Q = S*sin(phi) = {_f(data['Q'])} VAR")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the three-phase power result.

        Args:
            data: Solution data.

        Returns:
            String with power quantities.
        """
        if data["target"] == "I_L":
            return f"I_L = {_f(data['I_L'])} A"
        if data.get("full"):
            return (
                f"P = {_f(data['P'])} W, "
                f"Q = {_f(data['Q'])} VAR, "
                f"S = {_f(data['S'])} VA"
            )
        return f"P = {_f(data['P'])} W"


# ===================================================================
# 2. Transformer turns ratio  (tier 4)
# ===================================================================

@register
class TransformerRatioGenerator(StepGenerator):
    """Compute transformer voltages and currents from turns ratio.

    V1/V2 = N1/N2 = I2/I1. Given turns ratio and primary voltage,
    computes secondary voltage. At higher difficulty also computes
    currents from the ideal transformer relation.

    Difficulty scaling:
        Difficulty 1-3: integer turns ratio, compute V2 only.
        Difficulty 4-6: compute V2 and I2 from given I1.
        Difficulty 7-8: given V2 and power, find turns ratio.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transformer_ratio"

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
        return "compute transformer voltages and currents"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transformer parameters and compute outputs.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n1 = self._rng.randint(100, 1000 + difficulty * 200)
        n2 = self._rng.randint(50, max(51, n1 - 10))
        v1 = self._rng.choice([120, 230, 240, 480, 690][:min(
            difficulty + 1, 5)])

        ratio = round(n1 / n2, 4)
        v2 = round(v1 / ratio, 4)

        if difficulty <= 3:
            return "\\frac{V_1}{V_2} = \\frac{N_1}{N_2}", {
                "N1": n1, "N2": n2, "V1": v1, "V2": v2,
                "ratio": ratio, "mode": "voltage",
            }

        i1 = round(self._rng.uniform(1, 20 + difficulty * 5), 1)
        i2 = round(i1 * ratio, 4)
        power = round(v1 * i1, 4)

        if difficulty >= 7:
            return "\\frac{N_1}{N_2} = \\frac{V_1}{V_2}", {
                "N1": n1, "N2": n2, "V1": v1, "V2": v2,
                "I1": i1, "I2": i2, "ratio": ratio,
                "P": power, "mode": "find_ratio",
            }

        return "\\frac{V_1}{V_2} = \\frac{N_1}{N_2} = \\frac{I_2}{I_1}", {
            "N1": n1, "N2": n2, "V1": v1, "V2": v2,
            "I1": i1, "I2": i2, "ratio": ratio,
            "P": power, "mode": "full",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate transformer computation steps.

        Args:
            data: Solution data with turns, voltages, currents.

        Returns:
            List of step strings.
        """
        steps = [
            f"N1={data['N1']}, N2={data['N2']}",
            f"ratio = N1/N2 = {_f(data['ratio'])}",
        ]
        if data["mode"] == "voltage":
            steps.append(f"V2 = V1/ratio = {data['V1']}/{_f(data['ratio'])}")
        elif data["mode"] == "full":
            steps.append(f"V2 = {data['V1']}/{_f(data['ratio'])} = {_f(data['V2'])}V")
            steps.append(f"I2 = I1*ratio = {_f(data['I1'])}*{_f(data['ratio'])}")
        else:
            steps.append(f"V1={data['V1']}V, V2={_f(data['V2'])}V")
            steps.append(f"ratio = V1/V2 = {_f(data['ratio'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transformer result.

        Args:
            data: Solution data.

        Returns:
            String with voltages and/or currents.
        """
        if data["mode"] == "voltage":
            return f"V2 = {_f(data['V2'])} V"
        if data["mode"] == "full":
            return f"V2 = {_f(data['V2'])} V, I2 = {_f(data['I2'])} A"
        return f"N1/N2 = {_f(data['ratio'])}"


# ===================================================================
# 3. Power factor correction  (tier 6)
# ===================================================================

@register
class PowerFactorCorrectionGenerator(StepGenerator):
    """Compute capacitance for power factor correction.

    Q_c = P * (tan(phi1) - tan(phi2)),
    C = Q_c / (2 * pi * f * V^2).

    Difficulty scaling:
        Difficulty 1-3: simple power factor improvement (0.7 to 0.9).
        Difficulty 4-6: varied initial and target power factors.
        Difficulty 7-8: compute new line current after correction.

    Prerequisites:
        rlc_impedance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_factor_correction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["rlc_impedance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute capacitance for power factor correction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate power factor correction parameters.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        p = round(self._rng.uniform(1000, 50000 + difficulty * 10000), 1)
        v = self._rng.choice([230, 240, 380, 415, 480])
        freq = self._rng.choice([50, 60])

        if difficulty <= 3:
            pf1 = 0.7
            pf2 = 0.9
        else:
            pf1 = round(self._rng.uniform(0.5, 0.8), 2)
            pf2 = round(self._rng.uniform(max(pf1 + 0.05, 0.85), 0.99), 2)

        phi1 = math.acos(pf1)
        phi2 = math.acos(pf2)
        tan1 = round(math.tan(phi1), 4)
        tan2 = round(math.tan(phi2), 4)

        q_c = round(p * (tan1 - tan2), 4)
        cap = round(q_c / (2 * math.pi * freq * v ** 2), 4)

        if difficulty >= 7:
            # Also compute new line current
            s_old = round(p / pf1, 4)
            i_old = round(s_old / v, 4)
            s_new = round(p / pf2, 4)
            i_new = round(s_new / v, 4)
            return "C = \\frac{Q_c}{2\\pi f V^2}", {
                "P": p, "V": v, "f": freq,
                "pf1": pf1, "pf2": pf2,
                "tan1": tan1, "tan2": tan2,
                "Q_c": q_c, "C": cap,
                "I_old": i_old, "I_new": i_new,
                "show_current": True,
            }

        return "C = \\frac{Q_c}{2\\pi f V^2}", {
            "P": p, "V": v, "f": freq,
            "pf1": pf1, "pf2": pf2,
            "tan1": tan1, "tan2": tan2,
            "Q_c": q_c, "C": cap,
            "show_current": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate power factor correction steps.

        Args:
            data: Solution data with P, V, f, power factors.

        Returns:
            List of step strings.
        """
        steps = [
            f"P={_f(data['P'])}W, V={data['V']}V, f={data['f']}Hz",
            f"pf1={data['pf1']}, pf2={data['pf2']}",
            f"tan(phi1)={_f(data['tan1'])}, tan(phi2)={_f(data['tan2'])}",
            f"Q_c = P*(tan1-tan2) = {_f(data['Q_c'])} VAR",
            f"C = Q_c/(2*pi*f*V^2)",
        ]
        if data["show_current"]:
            steps.append(
                f"I_old={_f(data['I_old'])}A, I_new={_f(data['I_new'])}A"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the required capacitance.

        Args:
            data: Solution data.

        Returns:
            String with C in Farads.
        """
        result = f"C = {_f(data['C'])} F"
        if data["show_current"]:
            result += f", I_new = {_f(data['I_new'])} A"
        return result


# ===================================================================
# 4. Transmission line loss  (tier 4)
# ===================================================================

@register
class TransmissionLossGenerator(StepGenerator):
    """Compute transmission line power loss: P_loss = I^2 * R.

    Given power delivered P = V * I and line resistance R,
    computes the loss. At higher difficulty, compares losses
    at different transmission voltages.

    Difficulty scaling:
        Difficulty 1-3: single voltage, compute loss directly.
        Difficulty 4-6: compare loss at two different voltages.
        Difficulty 7-8: compute efficiency and optimal voltage.

    Prerequisites:
        ohms_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transmission_loss"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["ohms_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute transmission line power loss"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transmission parameters and compute losses.

        Args:
            difficulty: Controls whether comparison is included.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        power = self._rng.randint(1000, 10000 + difficulty * 5000)
        r = round(self._rng.uniform(0.5, 5.0 + difficulty), 2)
        v1 = self._rng.choice([240, 480, 1000, 11000, 33000][:min(
            difficulty + 1, 5)])

        i1 = round(power / v1, 4)
        loss1 = round(i1 ** 2 * r, 4)
        eff1 = round((power - loss1) / power * 100, 4)

        if difficulty >= 4:
            v2 = v1 * self._rng.choice([2, 5, 10])
            i2 = round(power / v2, 4)
            loss2 = round(i2 ** 2 * r, 4)
            eff2 = round((power - loss2) / power * 100, 4)
            return "P_{loss} = I^2 R", {
                "P": power, "R": r,
                "V1": v1, "I1": i1, "loss1": loss1, "eff1": eff1,
                "V2": v2, "I2": i2, "loss2": loss2, "eff2": eff2,
                "compare": True,
            }

        return "P_{loss} = I^2 R", {
            "P": power, "R": r,
            "V1": v1, "I1": i1, "loss1": loss1, "eff1": eff1,
            "compare": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate transmission loss computation steps.

        Args:
            data: Solution data with P, V, R, I, and losses.

        Returns:
            List of step strings.
        """
        steps = [
            f"P={data['P']}W, R={data['R']}ohm",
            f"V1={data['V1']}V, I1=P/V1={_f(data['I1'])}A",
            f"P_loss1 = I1^2*R = {_f(data['loss1'])}W",
        ]
        if data["compare"]:
            steps.append(
                f"V2={data['V2']}V, I2={_f(data['I2'])}A"
            )
            steps.append(f"P_loss2 = {_f(data['loss2'])}W")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transmission loss result.

        Args:
            data: Solution data.

        Returns:
            String with loss and efficiency.
        """
        if data["compare"]:
            return (
                f"P_loss1 = {_f(data['loss1'])} W ({_f(data['eff1'])}%), "
                f"P_loss2 = {_f(data['loss2'])} W ({_f(data['eff2'])}%)"
            )
        return f"P_loss = {_f(data['loss1'])} W, eff = {_f(data['eff1'])}%"


# ===================================================================
# 5. Generator frequency  (tier 4)
# ===================================================================

@register
class GeneratorFrequencyGenerator(StepGenerator):
    """Compute generator electrical frequency: f = (N * P) / 120.

    Where N is rotational speed in RPM and P is the number of poles.

    Difficulty scaling:
        Difficulty 1-3: common pole counts (2, 4), round RPM.
        Difficulty 4-6: varied pole counts, compute N for target f.
        Difficulty 7-8: given f and N, compute required poles.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "generator_frequency"

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
        return "compute generator electrical frequency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate generator parameters and compute frequency.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            poles = self._rng.choice([2, 4])
            target_f = self._rng.choice([50, 60])
            rpm = 120 * target_f // poles
        elif difficulty <= 6:
            poles = self._rng.choice([2, 4, 6, 8])
            rpm = self._rng.randint(300, 3600)
            target_f = round(rpm * poles / 120, 4)
        else:
            poles = self._rng.choice([2, 4, 6, 8, 10, 12])
            rpm = self._rng.randint(100, 3600)
            target_f = round(rpm * poles / 120, 4)

        freq = round(rpm * poles / 120, 4)

        if difficulty >= 7:
            return "P = \\frac{120 f}{N}", {
                "N": rpm, "P": poles, "f": freq,
                "target": "P",
            }

        if difficulty >= 4:
            if self._rng.random() < 0.5:
                return "N = \\frac{120 f}{P}", {
                    "N": rpm, "P": poles, "f": freq,
                    "target": "N",
                }

        return "f = \\frac{NP}{120}", {
            "N": rpm, "P": poles, "f": freq,
            "target": "f",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate generator frequency computation steps.

        Args:
            data: Solution data with N, P, f.

        Returns:
            List of step strings.
        """
        target = data["target"]
        if target == "f":
            np_prod = data["N"] * data["P"]
            return [
                f"N={data['N']}rpm, P={data['P']} poles",
                f"N*P = {np_prod}",
                f"f = {np_prod}/120",
            ]
        if target == "N":
            return [
                f"f={_f(data['f'])}Hz, P={data['P']} poles",
                f"N = 120*f/P = 120*{_f(data['f'])}/{data['P']}",
            ]
        # solve for P
        return [
            f"f={_f(data['f'])}Hz, N={data['N']}rpm",
            f"P = 120*f/N = 120*{_f(data['f'])}/{data['N']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the generator frequency, speed, or pole count.

        Args:
            data: Solution data.

        Returns:
            String with the target quantity.
        """
        target = data["target"]
        if target == "f":
            return f"f = {_f(data['f'])} Hz"
        if target == "N":
            return f"N = {data['N']} rpm"
        return f"P = {data['P']} poles"


# ===================================================================
# 6. Load flow (2-bus)  (tier 6)
# ===================================================================

@register
class LoadFlowGenerator(StepGenerator):
    """Compute load flow for a simple 2-bus system.

    P = (V1 * V2 * sin(delta)) / X. Given P, V1, V2, and X,
    computes the power angle delta.

    Difficulty scaling:
        Difficulty 1-3: small angles, integer voltages.
        Difficulty 4-6: varied voltages and reactance.
        Difficulty 7-8: compute maximum transferable power.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "load_flow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute load flow power angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2-bus system parameters and compute power angle.

        Args:
            difficulty: Controls voltage ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            v1 = 1.0  # per unit
            v2 = 1.0
            x = round(self._rng.uniform(0.1, 0.5), 2)
        else:
            v1 = round(self._rng.uniform(0.95, 1.05), 3)
            v2 = round(self._rng.uniform(0.95, 1.05), 3)
            x = round(self._rng.uniform(0.05, 0.5 + difficulty * 0.1), 3)

        p_max = round(v1 * v2 / x, 4)

        # Pick P < P_max to ensure valid angle
        p = round(self._rng.uniform(0.1, min(p_max * 0.8, p_max - 0.05)), 4)

        sin_delta = p * x / (v1 * v2)
        sin_delta = max(-1.0, min(1.0, sin_delta))
        delta_rad = math.asin(sin_delta)
        delta_deg = round(math.degrees(delta_rad), 4)

        if difficulty >= 7:
            return "P_{max} = \\frac{V_1 V_2}{X}", {
                "V1": v1, "V2": v2, "X": x,
                "P": p, "P_max": p_max,
                "sin_delta": round(sin_delta, 4),
                "delta_deg": delta_deg,
                "show_pmax": True,
            }

        return "P = \\frac{V_1 V_2 \\sin\\delta}{X}", {
            "V1": v1, "V2": v2, "X": x,
            "P": p, "P_max": p_max,
            "sin_delta": round(sin_delta, 4),
            "delta_deg": delta_deg,
            "show_pmax": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate load flow computation steps.

        Args:
            data: Solution data with V1, V2, X, P.

        Returns:
            List of step strings.
        """
        steps = [
            f"V1={_f(data['V1'])}pu, V2={_f(data['V2'])}pu, "
            f"X={_f(data['X'])}pu",
            f"P={_f(data['P'])}pu",
            f"sin(delta) = P*X/(V1*V2) = {_f(data['sin_delta'])}",
            f"delta = arcsin({_f(data['sin_delta'])})",
        ]
        if data["show_pmax"]:
            steps.append(f"P_max = V1*V2/X = {_f(data['P_max'])} pu")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the power angle.

        Args:
            data: Solution data.

        Returns:
            String with delta in degrees.
        """
        result = f"delta = {_f(data['delta_deg'])} deg"
        if data["show_pmax"]:
            result += f", P_max = {_f(data['P_max'])} pu"
        return result
