"""Photonics generators -- fiber optics, lasers, and photonic bandgaps.

Covers fiber optic numerical aperture, laser gain, photon energy,
total internal reflection, laser threshold, and photonic bandgap
(Bragg condition). Tiers range from 4 (introductory) to 5 (advanced).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _PhotonicsFormatter:
    """Formats numeric values for photonics problems.

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


_f = _PhotonicsFormatter.fmt

# Physical constants
_H = 6.626e-34       # Planck constant (J*s)
_C = 3.0e8           # speed of light (m/s)
_EV = 1.602e-19      # electron-volt (J)


# ===================================================================
# 1. Fiber optics NA  (tier 5)
# ===================================================================

@register
class FiberOpticsNAGenerator(StepGenerator):
    """Fiber optic numerical aperture: NA = sqrt(n_core^2 - n_clad^2).

    Computes the numerical aperture and acceptance angle
    theta = arcsin(NA) for a step-index optical fiber.

    Difficulty scaling:
        Difficulty 1-3: standard silica fiber values.
        Difficulty 4-6: varied core/cladding indices.
        Difficulty 7-8: compute V-number and number of modes.

    Prerequisites:
        snells_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fiber_optics_na"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["snells_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute fiber optic numerical aperture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fiber parameters and compute NA and acceptance angle.

        Args:
            difficulty: Controls index ranges and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_core = self._rng.choice([1.48, 1.49, 1.50])
            n_clad = self._rng.choice([1.46, 1.47])
        else:
            n_core = round(self._rng.uniform(1.45, 1.55), 3)
            n_clad = round(self._rng.uniform(1.43, n_core - 0.01), 3)

        na = round(math.sqrt(n_core ** 2 - n_clad ** 2), 4)
        theta = round(math.degrees(math.asin(min(na, 1.0))), 4)

        data = {
            "n_core": n_core, "n_clad": n_clad,
            "NA": na, "theta": theta,
        }

        if difficulty >= 7:
            # V-number: V = (pi*d/lambda)*NA
            d_um = self._rng.randint(5, 62)
            lam_nm = self._rng.randint(850, 1550)
            v_num = round(math.pi * d_um * 1e-6 / (lam_nm * 1e-9) * na, 4)
            n_modes = max(1, round(v_num ** 2 / 2))
            data["d_um"] = d_um
            data["lam_nm"] = lam_nm
            data["V"] = v_num
            data["N_modes"] = n_modes

        return "NA = \\sqrt{n_{core}^2 - n_{clad}^2}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate NA computation steps.

        Args:
            data: Solution data with fiber indices and NA.

        Returns:
            List of step strings.
        """
        n2_core = round(data["n_core"] ** 2, 4)
        n2_clad = round(data["n_clad"] ** 2, 4)
        diff = round(n2_core - n2_clad, 4)
        steps = [
            f"n_core={data['n_core']}, n_clad={data['n_clad']}",
            f"n_core^2 - n_clad^2 = {_f(n2_core)} - {_f(n2_clad)} = {_f(diff)}",
            f"NA = sqrt({_f(diff)}) = {_f(data['NA'])}",
            f"theta = arcsin({_f(data['NA'])}) = {_f(data['theta'])} deg",
        ]
        if "V" in data:
            steps.append(
                f"V = pi*{data['d_um']}um/{data['lam_nm']}nm*{_f(data['NA'])}"
                f" = {_f(data['V'])}, modes ~ {data['N_modes']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the NA and acceptance angle.

        Args:
            data: Solution data.

        Returns:
            String with NA and theta.
        """
        result = f"NA = {_f(data['NA'])}, theta = {_f(data['theta'])} deg"
        if "V" in data:
            result += f", V = {_f(data['V'])}"
        return result


# ===================================================================
# 2. Laser gain  (tier 5)
# ===================================================================

@register
class LaserGainGenerator(StepGenerator):
    """Laser gain: G = exp(g*L) where g = sigma*(N_2 - N_1).

    Computes single-pass gain for a laser medium given stimulated
    emission cross-section, population inversion, and medium length.

    Difficulty scaling:
        Difficulty 1-3: simple round parameters, compute G only.
        Difficulty 4-6: varied sigma values, compute gain in dB.
        Difficulty 7-8: multi-pass gain with mirror reflectivity.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laser_gain"

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
        return "compute laser single-pass gain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate laser medium parameters and compute gain.

        Args:
            difficulty: Controls parameter ranges and extras.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # sigma in cm^2 (typical: 1e-20 to 1e-18)
        sigma_exp = self._rng.randint(-20, -18)
        sigma_coeff = round(self._rng.uniform(1, 9), 1)
        sigma = sigma_coeff * 10 ** sigma_exp

        # Population inversion delta_N in cm^-3
        dn_exp = self._rng.randint(16, 19)
        dn_coeff = round(self._rng.uniform(1, 9), 1)
        delta_n = dn_coeff * 10 ** dn_exp

        # Medium length in cm
        length = round(self._rng.uniform(1, 20 + difficulty * 5), 1)

        g = sigma * delta_n  # gain coefficient (cm^-1)
        g_l = g * length
        gain = round(math.exp(g_l), 4)
        gain_db = round(10 * math.log10(max(gain, 1e-10)), 4)

        data = {
            "sigma": sigma, "sigma_str": f"{sigma_coeff}e{sigma_exp}",
            "delta_N": delta_n, "dN_str": f"{dn_coeff}e{dn_exp}",
            "L": length,
            "g": round(g, 4), "gL": round(g_l, 4),
            "G": gain, "G_dB": gain_db,
            "full": difficulty >= 4,
        }

        if difficulty >= 7:
            r1 = round(self._rng.uniform(0.95, 0.999), 3)
            r2 = round(self._rng.uniform(0.3, 0.7), 2)
            round_trip = round(gain ** 2 * r1 * r2, 4)
            data["R1"] = r1
            data["R2"] = r2
            data["round_trip"] = round_trip

        return "G = \\exp(\\sigma \\Delta N \\cdot L)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate laser gain computation steps.

        Args:
            data: Solution data with sigma, delta_N, L, and G.

        Returns:
            List of step strings.
        """
        steps = [
            f"sigma={data['sigma_str']} cm^2, dN={data['dN_str']} cm^-3",
            f"L={data['L']} cm",
            f"g = sigma*dN = {_f(data['g'])} cm^-1",
            f"gL = {_f(data['gL'])}",
            f"G = exp({_f(data['gL'])}) = {_f(data['G'])}",
        ]
        if data["full"]:
            steps.append(f"G_dB = {_f(data['G_dB'])} dB")
        if "R1" in data:
            steps.append(
                f"R1={data['R1']}, R2={data['R2']}, "
                f"round-trip = G^2*R1*R2 = {_f(data['round_trip'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the laser gain.

        Args:
            data: Solution data.

        Returns:
            String with G value.
        """
        result = f"G = {_f(data['G'])}"
        if data["full"]:
            result += f" ({_f(data['G_dB'])} dB)"
        if "round_trip" in data:
            result += f", round-trip = {_f(data['round_trip'])}"
        return result


# ===================================================================
# 3. Photon energy  (tier 4)
# ===================================================================

@register
class PhotonEnergyGenerator(StepGenerator):
    """Photon energy: E = hc/lambda. Compute energy in eV from wavelength.

    Given wavelength in nm, computes the photon energy using
    Planck's equation and converts joules to electron-volts.

    Difficulty scaling:
        Difficulty 1-3: visible light wavelengths.
        Difficulty 4-6: UV and IR wavelengths.
        Difficulty 7-8: compute frequency and momentum too.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "photon_energy"

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
        return "compute photon energy from wavelength"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate wavelength and compute photon energy in eV.

        Args:
            difficulty: Controls wavelength range and extras.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            lam_nm = self._rng.randint(400, 700)
        elif difficulty <= 6:
            lam_nm = self._rng.randint(100, 2000)
        else:
            lam_nm = self._rng.randint(10, 10000)

        lam_m = lam_nm * 1e-9
        e_j = _H * _C / lam_m
        e_ev = round(e_j / _EV, 4)
        freq = round(_C / lam_m, 4)

        data = {
            "lam_nm": lam_nm, "lam_m": lam_m,
            "E_J": round(e_j, 4), "E_eV": e_ev,
            "freq": freq,
        }

        if difficulty >= 7:
            momentum = round(_H / lam_m, 4)
            data["p"] = momentum

        return "E = \\frac{hc}{\\lambda}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate photon energy computation steps.

        Args:
            data: Solution data with wavelength and energy.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda = {data['lam_nm']} nm = {_f(data['lam_m'])} m",
            f"E = hc/lambda = (6.626e-34)(3e8)/{_f(data['lam_m'])}",
            f"E = {_f(data['E_J'])} J = {_f(data['E_eV'])} eV",
        ]
        if "p" in data:
            steps.append(f"f = c/lambda = {_f(data['freq'])} Hz")
            steps.append(f"p = h/lambda = {_f(data['p'])} kg*m/s")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the photon energy.

        Args:
            data: Solution data.

        Returns:
            String with energy in eV.
        """
        result = f"E = {_f(data['E_eV'])} eV"
        if "p" in data:
            result += f", p = {_f(data['p'])} kg*m/s"
        return result


# ===================================================================
# 4. Total internal reflection  (tier 4)
# ===================================================================

@register
class TotalInternalReflectionGenerator(StepGenerator):
    """Total internal reflection: theta_c = arcsin(n2/n1).

    Computes the critical angle and determines whether a given
    incidence angle exceeds it for total internal reflection.

    Difficulty scaling:
        Difficulty 1-3: common materials (glass-air, water-air).
        Difficulty 4-6: wider material range.
        Difficulty 7-8: compute evanescent wave penetration depth.

    Prerequisites:
        snells_law.
    """

    _MATERIALS = {
        "air": 1.0, "water": 1.33, "glass": 1.5,
        "crown_glass": 1.52, "flint_glass": 1.66, "diamond": 2.42,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "total_internal_reflection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["snells_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine total internal reflection condition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two media and an incidence angle, check for TIR.

        Args:
            difficulty: Controls material range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        names = list(self._MATERIALS.keys())
        if difficulty <= 3:
            pool = names[:3]
        else:
            pool = names

        # n1 must be denser than n2 for TIR to be possible
        m1 = self._rng.choice(pool[1:])  # skip air for n1
        m2 = self._rng.choice([n for n in pool if self._MATERIALS[n] < self._MATERIALS[m1]])
        if not m2:
            m1, m2 = "glass", "air"

        n1 = self._MATERIALS[m1]
        n2 = self._MATERIALS[m2]
        theta_c = round(math.degrees(math.asin(n2 / n1)), 4)

        # Pick test angle: sometimes above, sometimes below critical
        if self._rng.random() < 0.6:
            test_angle = self._rng.randint(int(theta_c) + 1, 89)
        else:
            test_angle = self._rng.randint(10, max(11, int(theta_c) - 1))

        tir = test_angle > theta_c

        return "\\theta_c = \\arcsin(n_2/n_1)", {
            "n1": n1, "n2": n2, "m1": m1, "m2": m2,
            "theta_c": theta_c, "test_angle": test_angle,
            "TIR": tir,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate TIR computation steps.

        Args:
            data: Solution data with indices, critical angle, and test.

        Returns:
            List of step strings.
        """
        ratio = round(data["n2"] / data["n1"], 4)
        return [
            f"n1={data['n1']} ({data['m1']}), n2={data['n2']} ({data['m2']})",
            f"n2/n1 = {_f(ratio)}",
            f"theta_c = arcsin({_f(ratio)}) = {_f(data['theta_c'])} deg",
            f"test angle = {data['test_angle']} deg",
            f"{'TIR occurs' if data['TIR'] else 'no TIR'}: "
            f"{data['test_angle']} {'>' if data['TIR'] else '<='} {_f(data['theta_c'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the critical angle and TIR verdict.

        Args:
            data: Solution data.

        Returns:
            String with theta_c and TIR result.
        """
        verdict = "yes" if data["TIR"] else "no"
        return f"theta_c = {_f(data['theta_c'])} deg, TIR = {verdict}"


# ===================================================================
# 5. Laser threshold  (tier 5)
# ===================================================================

@register
class LaserThresholdGenerator(StepGenerator):
    """Laser threshold: g_th = alpha + (1/2L)*ln(1/(R1*R2)).

    Computes the threshold gain coefficient for lasing given
    internal loss, cavity length, and mirror reflectivities.

    Difficulty scaling:
        Difficulty 1-3: simple parameters, compute g_th only.
        Difficulty 4-6: varied mirror reflectivities.
        Difficulty 7-8: also compute threshold pump power.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laser_threshold"

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
        return "compute laser threshold gain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate cavity parameters and compute threshold gain.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        alpha = round(self._rng.uniform(0.01, 0.5 + difficulty * 0.1), 3)
        length = round(self._rng.uniform(1, 30 + difficulty * 5), 1)

        if difficulty <= 3:
            r1 = round(self._rng.uniform(0.95, 0.999), 3)
            r2 = round(self._rng.uniform(0.95, 0.999), 3)
        else:
            r1 = round(self._rng.uniform(0.8, 0.999), 3)
            r2 = round(self._rng.uniform(0.3, 0.8), 3)

        mirror_loss = round(math.log(1 / (r1 * r2)) / (2 * length), 4)
        g_th = round(alpha + mirror_loss, 4)

        data = {
            "alpha": alpha, "L": length,
            "R1": r1, "R2": r2,
            "mirror_loss": mirror_loss, "g_th": g_th,
        }

        if difficulty >= 7:
            # Threshold population inversion
            sigma_exp = self._rng.randint(-20, -18)
            sigma_coeff = round(self._rng.uniform(1, 5), 1)
            sigma = sigma_coeff * 10 ** sigma_exp
            delta_n_th = round(g_th / sigma, 4)
            data["sigma"] = sigma
            data["sigma_str"] = f"{sigma_coeff}e{sigma_exp}"
            data["dN_th"] = delta_n_th

        return "g_{th} = \\alpha + \\frac{1}{2L}\\ln\\frac{1}{R_1 R_2}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate threshold gain computation steps.

        Args:
            data: Solution data with cavity parameters and g_th.

        Returns:
            List of step strings.
        """
        r_prod = round(data["R1"] * data["R2"], 4)
        ln_val = round(math.log(1 / r_prod), 4)
        steps = [
            f"alpha={data['alpha']} cm^-1, L={data['L']} cm",
            f"R1={data['R1']}, R2={data['R2']}",
            f"R1*R2 = {_f(r_prod)}, ln(1/{_f(r_prod)}) = {_f(ln_val)}",
            f"mirror loss = {_f(ln_val)}/(2*{data['L']}) = {_f(data['mirror_loss'])} cm^-1",
            f"g_th = {data['alpha']} + {_f(data['mirror_loss'])} = {_f(data['g_th'])} cm^-1",
        ]
        if "dN_th" in data:
            steps.append(
                f"dN_th = g_th/sigma = {_f(data['g_th'])}/{data['sigma_str']}"
                f" = {_f(data['dN_th'])} cm^-3"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the threshold gain.

        Args:
            data: Solution data.

        Returns:
            String with g_th.
        """
        result = f"g_th = {_f(data['g_th'])} cm^-1"
        if "dN_th" in data:
            result += f", dN_th = {_f(data['dN_th'])} cm^-3"
        return result


# ===================================================================
# 6. Photonic bandgap  (tier 5)
# ===================================================================

@register
class PhotonicBandgapGenerator(StepGenerator):
    """Bragg condition: lambda_B = 2 * n_eff * Lambda.

    Computes the center wavelength of the stop band for a
    photonic crystal or fiber Bragg grating.

    Difficulty scaling:
        Difficulty 1-3: simple grating period and index.
        Difficulty 4-6: compute bandwidth from index contrast.
        Difficulty 7-8: compute reflectivity for given grating length.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "photonic_bandgap"

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
        return "compute photonic bandgap center wavelength"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate grating parameters and compute Bragg wavelength.

        Args:
            difficulty: Controls parameter ranges and extras.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_eff = round(self._rng.uniform(1.44, 1.55), 4)

        # Grating period in nm
        target_lam = self._rng.randint(800, 1600)
        big_lambda = round(target_lam / (2 * n_eff), 4)

        lam_b = round(2 * n_eff * big_lambda, 4)

        data = {
            "n_eff": n_eff, "Lambda": big_lambda,
            "lam_B": lam_b,
        }

        if difficulty >= 4:
            # Bandwidth approximation: delta_lam ~ lam_B * delta_n / n_eff
            delta_n = round(self._rng.uniform(1e-4, 5e-3), 4)
            bw = round(lam_b * delta_n / n_eff, 4)
            data["delta_n"] = delta_n
            data["bandwidth"] = bw

        if difficulty >= 7:
            # Reflectivity: R = tanh^2(kappa * L_g)
            # kappa ~ pi * delta_n / lam_B
            delta_n = data.get("delta_n", round(self._rng.uniform(1e-4, 5e-3), 4))
            data["delta_n"] = delta_n
            kappa = round(math.pi * delta_n / (lam_b * 1e-9), 4)
            l_g_mm = round(self._rng.uniform(1, 10), 1)
            l_g = l_g_mm * 1e-3
            refl = round(math.tanh(kappa * l_g) ** 2, 4)
            data["kappa"] = kappa
            data["L_g_mm"] = l_g_mm
            data["reflectivity"] = refl

        return "\\lambda_B = 2 n_{eff} \\Lambda", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bragg condition computation steps.

        Args:
            data: Solution data with grating parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"n_eff = {_f(data['n_eff'])}, Lambda = {_f(data['Lambda'])} nm",
            f"lam_B = 2*{_f(data['n_eff'])}*{_f(data['Lambda'])} = {_f(data['lam_B'])} nm",
        ]
        if "bandwidth" in data:
            steps.append(
                f"delta_n = {_f(data['delta_n'])}, "
                f"BW = lam_B*delta_n/n_eff = {_f(data['bandwidth'])} nm"
            )
        if "reflectivity" in data:
            steps.append(
                f"kappa = {_f(data['kappa'])} m^-1, "
                f"L_g = {data['L_g_mm']} mm"
            )
            steps.append(f"R = tanh^2(kappa*L_g) = {_f(data['reflectivity'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Bragg wavelength.

        Args:
            data: Solution data.

        Returns:
            String with lambda_B.
        """
        result = f"lam_B = {_f(data['lam_B'])} nm"
        if "bandwidth" in data:
            result += f", BW = {_f(data['bandwidth'])} nm"
        if "reflectivity" in data:
            result += f", R = {_f(data['reflectivity'])}"
        return result
