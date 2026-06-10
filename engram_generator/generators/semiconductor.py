"""Semiconductor generators -- junctions, MOSFETs, diodes, and carriers.

Covers PN junction built-in potential, MOSFET threshold voltage,
diode I-V characteristic, LED wavelength, carrier concentration,
and depletion width. All generators are tier 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _SemiFormatter:
    """Formats numeric values for semiconductor problems.

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


_f = _SemiFormatter.fmt

# Physical constants
_K = 1.381e-23       # Boltzmann constant (J/K)
_Q = 1.602e-19       # electron charge (C)
_H = 6.626e-34       # Planck constant (J*s)
_C = 3.0e8           # speed of light (m/s)
_EV = 1.602e-19      # electron-volt (J)
_EPSILON_SI = 11.7 * 8.854e-12  # Si permittivity (F/m)


# ===================================================================
# 1. PN junction built-in potential  (tier 5)
# ===================================================================

@register
class PNJunctionGenerator(StepGenerator):
    """PN junction built-in potential: V_bi = (kT/q)*ln(N_A*N_D/n_i^2).

    Computes the built-in potential for a silicon PN junction
    given donor and acceptor doping concentrations.

    Difficulty scaling:
        Difficulty 1-3: standard doping (1e15-1e17), T=300K.
        Difficulty 4-6: wider doping range (1e14-1e19).
        Difficulty 7-8: non-standard temperature.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pn_junction"

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
        return "compute PN junction built-in potential"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate doping concentrations and compute V_bi.

        Args:
            difficulty: Controls doping ranges and temperature.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            na_exp = self._rng.randint(15, 17)
            nd_exp = self._rng.randint(15, 17)
            temp = 300
        elif difficulty <= 6:
            na_exp = self._rng.randint(14, 19)
            nd_exp = self._rng.randint(14, 19)
            temp = 300
        else:
            na_exp = self._rng.randint(14, 19)
            nd_exp = self._rng.randint(14, 19)
            temp = self._rng.choice([250, 300, 350, 400])

        na_coeff = round(self._rng.uniform(1, 9), 1)
        nd_coeff = round(self._rng.uniform(1, 9), 1)
        na = na_coeff * 10 ** na_exp
        nd = nd_coeff * 10 ** nd_exp

        # Intrinsic carrier concentration for Si at given T
        # Approximate: n_i(T) = n_i(300) * (T/300)^1.5 * exp(...)
        # Simplified: use 1.5e10 at 300K
        ni_300 = 1.5e10
        if temp == 300:
            ni = ni_300
        else:
            # Simplified temperature dependence
            ni = ni_300 * (temp / 300) ** 1.5 * math.exp(
                -6884 * (1 / temp - 1 / 300)
            )

        vt = round(_K * temp / _Q, 4)
        ln_arg = na * nd / (ni ** 2)
        v_bi = round(vt * math.log(ln_arg), 4)

        return "V_{bi} = \\frac{kT}{q}\\ln\\frac{N_A N_D}{n_i^2}", {
            "NA": na, "NA_str": f"{na_coeff}e{na_exp}",
            "ND": nd, "ND_str": f"{nd_coeff}e{nd_exp}",
            "T": temp, "ni": ni,
            "VT": vt, "ln_arg": round(ln_arg, 4),
            "V_bi": v_bi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate V_bi computation steps.

        Args:
            data: Solution data with doping and potential.

        Returns:
            List of step strings.
        """
        ln_val = round(math.log(data["ln_arg"]), 4)
        steps = [
            f"NA={data['NA_str']} cm^-3, ND={data['ND_str']} cm^-3",
            f"T={data['T']}K, VT=kT/q={_f(data['VT'])} V",
            f"NA*ND/ni^2 = {_f(data['ln_arg'])}",
            f"ln({_f(data['ln_arg'])}) = {_f(ln_val)}",
            f"V_bi = {_f(data['VT'])}*{_f(ln_val)} = {_f(data['V_bi'])} V",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the built-in potential.

        Args:
            data: Solution data.

        Returns:
            String with V_bi.
        """
        return f"V_bi = {_f(data['V_bi'])} V"


# ===================================================================
# 2. MOSFET threshold voltage  (tier 5)
# ===================================================================

@register
class MOSFETThresholdGenerator(StepGenerator):
    """MOSFET threshold voltage (simplified).

    V_th = V_FB + 2*phi_F + Q_dep/C_ox where phi_F = (kT/q)*ln(N_A/n_i)
    and Q_dep = sqrt(4*epsilon*q*N_A*phi_F).

    Difficulty scaling:
        Difficulty 1-3: given phi_F and C_ox directly.
        Difficulty 4-6: compute phi_F from doping.
        Difficulty 7-8: include flat-band voltage shift.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mosfet_threshold"

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
        return "compute MOSFET threshold voltage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate MOSFET parameters and compute V_th.

        Args:
            difficulty: Controls whether phi_F is given or computed.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        na_exp = self._rng.randint(15, 18)
        na_coeff = round(self._rng.uniform(1, 9), 1)
        na = na_coeff * 10 ** na_exp

        ni = 1.5e10  # at 300K
        temp = 300
        vt = round(_K * temp / _Q, 4)
        phi_f = round(vt * math.log(na / ni), 4)

        # C_ox = epsilon_ox / t_ox
        t_ox_nm = self._rng.randint(2, 20 + difficulty * 2)
        t_ox = t_ox_nm * 1e-9
        eps_ox = 3.9 * 8.854e-12  # SiO2 permittivity
        c_ox = round(eps_ox / t_ox, 4)

        # Q_dep = sqrt(4 * epsilon_si * q * N_A * phi_F)
        q_dep = round(math.sqrt(4 * _EPSILON_SI * _Q * na * phi_f), 4)

        v_fb = 0.0
        if difficulty >= 7:
            v_fb = round(self._rng.uniform(-1.0, -0.2), 2)

        v_th = round(v_fb + 2 * phi_f + q_dep / c_ox, 4)

        return "V_{th} = V_{FB} + 2\\phi_F + Q_{dep}/C_{ox}", {
            "NA": na, "NA_str": f"{na_coeff}e{na_exp}",
            "T": temp, "VT": vt,
            "phi_F": phi_f, "t_ox_nm": t_ox_nm,
            "C_ox": c_ox, "Q_dep": q_dep,
            "V_FB": v_fb, "V_th": v_th,
            "compute_phi": difficulty >= 4,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate V_th computation steps.

        Args:
            data: Solution data with MOSFET parameters.

        Returns:
            List of step strings.
        """
        steps = [f"NA={data['NA_str']} cm^-3, t_ox={data['t_ox_nm']} nm"]
        if data["compute_phi"]:
            steps.append(f"phi_F = VT*ln(NA/ni) = {_f(data['phi_F'])} V")
        else:
            steps.append(f"phi_F = {_f(data['phi_F'])} V (given)")
        steps.append(f"Q_dep = sqrt(4*eps*q*NA*phi_F) = {_f(data['Q_dep'])} C/cm^2")
        steps.append(f"C_ox = {_f(data['C_ox'])} F/cm^2")
        q_over_c = round(data["Q_dep"] / data["C_ox"], 4)
        steps.append(
            f"V_th = {_f(data['V_FB'])} + 2*{_f(data['phi_F'])} + "
            f"{_f(q_over_c)} = {_f(data['V_th'])} V"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the threshold voltage.

        Args:
            data: Solution data.

        Returns:
            String with V_th.
        """
        return f"V_th = {_f(data['V_th'])} V"


# ===================================================================
# 3. Diode I-V  (tier 5)
# ===================================================================

@register
class DiodeIVGenerator(StepGenerator):
    """Diode I-V: I = I_0*(exp(V/(n*V_T)) - 1), V_T = kT/q.

    Computes diode current for given forward or reverse bias.

    Difficulty scaling:
        Difficulty 1-3: n=1 (ideal), forward bias only.
        Difficulty 4-6: n=1 or 2, forward and reverse.
        Difficulty 7-8: compute dynamic resistance r_d = nV_T/I.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diode_iv"

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
        return "compute diode current from Shockley equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate diode parameters and compute I for given V.

        Args:
            difficulty: Controls ideality factor and bias range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = 300
        vt = round(_K * temp / _Q, 4)  # ~0.0259V

        if difficulty <= 3:
            n = 1
            v = round(self._rng.uniform(0.3, 0.7), 2)
        elif difficulty <= 6:
            n = self._rng.choice([1, 2])
            if self._rng.random() < 0.7:
                v = round(self._rng.uniform(0.2, 0.8), 2)
            else:
                v = round(self._rng.uniform(-2.0, -0.1), 2)
        else:
            n = self._rng.choice([1, 2])
            v = round(self._rng.uniform(0.4, 0.75), 2)

        # I_0 in Amps (reverse saturation current)
        i0_exp = self._rng.randint(-14, -10)
        i0_coeff = round(self._rng.uniform(1, 9), 1)
        i0 = i0_coeff * 10 ** i0_exp

        exp_arg = round(v / (n * vt), 4)
        # Clamp to avoid overflow
        exp_arg_clamped = min(exp_arg, 100)
        exp_val = round(math.exp(exp_arg_clamped), 4)
        current = round(i0 * (exp_val - 1), 4)

        data = {
            "T": temp, "VT": vt, "n": n,
            "V": v, "I0": i0,
            "I0_str": f"{i0_coeff}e{i0_exp}",
            "exp_arg": exp_arg, "exp_val": exp_val,
            "I": current,
        }

        if difficulty >= 7 and current > 0:
            r_d = round(n * vt / current, 4)
            data["r_d"] = r_d

        return "I = I_0(e^{V/nV_T} - 1)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate diode I-V computation steps.

        Args:
            data: Solution data with V, I_0, and computed I.

        Returns:
            List of step strings.
        """
        steps = [
            f"V={data['V']}V, I0={data['I0_str']}A, n={data['n']}",
            f"VT = kT/q = {_f(data['VT'])} V",
            f"V/(nVT) = {_f(data['exp_arg'])}",
            f"exp({_f(data['exp_arg'])}) = {_f(data['exp_val'])}",
            f"I = {data['I0_str']}*({_f(data['exp_val'])}-1) = {_f(data['I'])} A",
        ]
        if "r_d" in data:
            steps.append(f"r_d = nVT/I = {_f(data['r_d'])} ohm")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the diode current.

        Args:
            data: Solution data.

        Returns:
            String with I value.
        """
        result = f"I = {_f(data['I'])} A"
        if "r_d" in data:
            result += f", r_d = {_f(data['r_d'])} ohm"
        return result


# ===================================================================
# 4. LED wavelength  (tier 4)
# ===================================================================

@register
class LEDWavelengthGenerator(StepGenerator):
    """LED emission: lambda = hc/E_g. Compute wavelength and color.

    Given the band gap energy in eV, computes the peak emission
    wavelength and identifies the approximate color.

    Difficulty scaling:
        Difficulty 1-3: common visible LEDs (1.8-3.1 eV).
        Difficulty 4-6: include infrared and UV LEDs.
        Difficulty 7-8: compute photon flux from power.

    Prerequisites:
        division.
    """

    _COLOR_MAP = [
        (380, 450, "violet"), (450, 495, "blue"),
        (495, 570, "green"), (570, 590, "yellow"),
        (590, 620, "orange"), (620, 750, "red"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "led_wavelength"

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
        return "compute LED emission wavelength from band gap"

    def _classify_color(self, lam_nm: float) -> str:
        """Classify wavelength into a color name.

        Args:
            lam_nm: Wavelength in nanometers.

        Returns:
            Color name string.
        """
        for lo, hi, name in self._COLOR_MAP:
            if lo <= lam_nm < hi:
                return name
        if lam_nm >= 750:
            return "infrared"
        return "ultraviolet"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate band gap and compute emission wavelength.

        Args:
            difficulty: Controls band gap range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            eg = round(self._rng.uniform(1.8, 3.1), 2)
        elif difficulty <= 6:
            eg = round(self._rng.uniform(0.7, 4.0), 2)
        else:
            eg = round(self._rng.uniform(0.5, 6.0), 2)

        eg_j = eg * _EV
        lam_m = _H * _C / eg_j
        lam_nm = round(lam_m * 1e9, 4)
        color = self._classify_color(lam_nm)

        data = {
            "Eg": eg, "Eg_J": round(eg_j, 4),
            "lam_nm": lam_nm, "color": color,
        }

        if difficulty >= 7:
            power_mw = round(self._rng.uniform(1, 100), 1)
            power_w = power_mw * 1e-3
            flux = round(power_w / eg_j, 4)
            data["power_mW"] = power_mw
            data["flux"] = flux

        return "\\lambda = \\frac{hc}{E_g}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate LED wavelength computation steps.

        Args:
            data: Solution data with band gap and wavelength.

        Returns:
            List of step strings.
        """
        steps = [
            f"E_g = {data['Eg']} eV = {_f(data['Eg_J'])} J",
            f"lambda = hc/E_g = (6.626e-34)(3e8)/{_f(data['Eg_J'])}",
            f"lambda = {_f(data['lam_nm'])} nm ({data['color']})",
        ]
        if "flux" in data:
            steps.append(
                f"P = {data['power_mW']} mW, "
                f"flux = P/E = {_f(data['flux'])} photons/s"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the emission wavelength and color.

        Args:
            data: Solution data.

        Returns:
            String with lambda and color.
        """
        result = f"lambda = {_f(data['lam_nm'])} nm, color = {data['color']}"
        if "flux" in data:
            result += f", flux = {_f(data['flux'])} s^-1"
        return result


# ===================================================================
# 5. Carrier concentration  (tier 5)
# ===================================================================

@register
class CarrierConcentrationGenerator(StepGenerator):
    """Carrier concentration: n*p = n_i^2 (mass action law).

    Given intrinsic concentration n_i and doping (N_D or N_A),
    computes majority and minority carrier concentrations.

    Difficulty scaling:
        Difficulty 1-3: n-type only, simple doping.
        Difficulty 4-6: n-type or p-type, varied doping.
        Difficulty 7-8: compensated semiconductor (both dopants).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carrier_concentration"

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
        return "compute majority and minority carrier concentrations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate doping and compute carrier concentrations.

        Args:
            difficulty: Controls doping type and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        ni = 1.5e10  # Si at 300K

        if difficulty <= 3:
            dtype = "n"
            nd_exp = self._rng.randint(15, 17)
            nd_coeff = round(self._rng.uniform(1, 9), 1)
            nd = nd_coeff * 10 ** nd_exp
            n = nd  # majority
            p = round(ni ** 2 / n, 4)  # minority
            return "np = n_i^2", {
                "ni": ni, "type": dtype,
                "ND": nd, "ND_str": f"{nd_coeff}e{nd_exp}",
                "n": n, "p": p,
                "majority": "n", "minority": "p",
                "compensated": False,
            }

        if difficulty <= 6:
            dtype = self._rng.choice(["n", "p"])
            dop_exp = self._rng.randint(14, 18)
            dop_coeff = round(self._rng.uniform(1, 9), 1)
            dop = dop_coeff * 10 ** dop_exp

            if dtype == "n":
                n = dop
                p = round(ni ** 2 / n, 4)
                return "np = n_i^2", {
                    "ni": ni, "type": dtype,
                    "ND": dop, "ND_str": f"{dop_coeff}e{dop_exp}",
                    "n": n, "p": p,
                    "majority": "n", "minority": "p",
                    "compensated": False,
                }
            p_val = dop
            n_val = round(ni ** 2 / p_val, 4)
            return "np = n_i^2", {
                "ni": ni, "type": dtype,
                "NA": dop, "NA_str": f"{dop_coeff}e{dop_exp}",
                "n": n_val, "p": p_val,
                "majority": "p", "minority": "n",
                "compensated": False,
            }

        # Compensated semiconductor
        nd_exp = self._rng.randint(15, 18)
        nd_coeff = round(self._rng.uniform(1, 9), 1)
        nd = nd_coeff * 10 ** nd_exp

        na_exp = self._rng.randint(14, nd_exp - 1)
        na_coeff = round(self._rng.uniform(1, 9), 1)
        na = na_coeff * 10 ** na_exp

        if nd > na:
            n_eff = nd - na
            n = n_eff
            p = round(ni ** 2 / n, 4)
            majority = "n"
        else:
            p_eff = na - nd
            p = p_eff
            n = round(ni ** 2 / p, 4)
            majority = "p"

        return "np = n_i^2", {
            "ni": ni, "type": "compensated",
            "ND": nd, "ND_str": f"{nd_coeff}e{nd_exp}",
            "NA": na, "NA_str": f"{na_coeff}e{na_exp}",
            "n": n, "p": p,
            "majority": majority, "minority": "p" if majority == "n" else "n",
            "compensated": True,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate carrier concentration computation steps.

        Args:
            data: Solution data with doping and carriers.

        Returns:
            List of step strings.
        """
        steps = [f"ni = 1.5e10 cm^-3, ni^2 = 2.25e20"]
        if data["compensated"]:
            steps.append(
                f"ND={data['ND_str']}, NA={data['NA_str']}"
            )
            if data["majority"] == "n":
                n_eff = data["ND"] - data["NA"]
                steps.append(f"n = ND-NA = {_f(n_eff)} cm^-3")
            else:
                p_eff = data["NA"] - data["ND"]
                steps.append(f"p = NA-ND = {_f(p_eff)} cm^-3")
        elif data["type"] == "n":
            steps.append(f"ND={data['ND_str']} cm^-3")
            steps.append(f"n ~ ND = {_f(data['n'])} (majority)")
        else:
            steps.append(f"NA={data['NA_str']} cm^-3")
            steps.append(f"p ~ NA = {_f(data['p'])} (majority)")

        minority_val = data["p"] if data["majority"] == "n" else data["n"]
        steps.append(
            f"{data['minority']} = ni^2/{data['majority']} = {_f(minority_val)} cm^-3"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the carrier concentrations.

        Args:
            data: Solution data.

        Returns:
            String with n and p.
        """
        return f"n = {_f(data['n'])} cm^-3, p = {_f(data['p'])} cm^-3"


# ===================================================================
# 6. Depletion width  (tier 5)
# ===================================================================

@register
class DepletionWidthGenerator(StepGenerator):
    """Depletion width: W = sqrt(2*eps*(V_bi+V_R)/q * (1/N_A + 1/N_D)).

    Computes the total depletion region width for a PN junction
    under reverse bias.

    Difficulty scaling:
        Difficulty 1-3: zero reverse bias, standard doping.
        Difficulty 4-6: non-zero reverse bias.
        Difficulty 7-8: also compute junction capacitance.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "depletion_width"

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
        return "compute PN junction depletion width"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate junction parameters and compute depletion width.

        Args:
            difficulty: Controls reverse bias and doping ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        na_exp = self._rng.randint(15, 18)
        na_coeff = round(self._rng.uniform(1, 9), 1)
        na = na_coeff * 10 ** na_exp

        nd_exp = self._rng.randint(15, 18)
        nd_coeff = round(self._rng.uniform(1, 9), 1)
        nd = nd_coeff * 10 ** nd_exp

        # Convert to m^-3 for SI calculation
        na_si = na * 1e6
        nd_si = nd * 1e6

        ni = 1.5e10
        vt = round(_K * 300 / _Q, 4)
        v_bi = round(vt * math.log(na * nd / ni ** 2), 4)

        if difficulty <= 3:
            v_r = 0
        else:
            v_r = round(self._rng.uniform(1, 5 + difficulty), 1)

        # W = sqrt(2 * eps_si * (V_bi + V_R) / q * (1/N_A + 1/N_D))
        inv_sum = 1 / na_si + 1 / nd_si
        w = round(math.sqrt(2 * _EPSILON_SI * (v_bi + v_r) / _Q * inv_sum), 4)
        w_um = round(w * 1e6, 4)

        data = {
            "NA": na, "NA_str": f"{na_coeff}e{na_exp}",
            "ND": nd, "ND_str": f"{nd_coeff}e{nd_exp}",
            "V_bi": v_bi, "V_R": v_r,
            "W": w, "W_um": w_um,
        }

        if difficulty >= 7:
            # Junction capacitance C_j = eps_si * A / W
            # Per unit area: C_j = eps_si / W
            c_j = round(_EPSILON_SI / w, 4)
            data["C_j"] = c_j

        return "W = \\sqrt{\\frac{2\\epsilon(V_{bi}+V_R)}{q}\\left(\\frac{1}{N_A}+\\frac{1}{N_D}\\right)}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate depletion width computation steps.

        Args:
            data: Solution data with junction parameters and W.

        Returns:
            List of step strings.
        """
        v_total = round(data["V_bi"] + data["V_R"], 4)
        steps = [
            f"NA={data['NA_str']} cm^-3, ND={data['ND_str']} cm^-3",
            f"V_bi={_f(data['V_bi'])} V, V_R={_f(data['V_R'])} V",
            f"V_bi+V_R = {_f(v_total)} V",
            f"W = {_f(data['W'])} m = {_f(data['W_um'])} um",
        ]
        if "C_j" in data:
            steps.append(f"C_j = eps/W = {_f(data['C_j'])} F/m^2")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the depletion width.

        Args:
            data: Solution data.

        Returns:
            String with W value.
        """
        result = f"W = {_f(data['W_um'])} um"
        if "C_j" in data:
            result += f", C_j = {_f(data['C_j'])} F/m^2"
        return result
