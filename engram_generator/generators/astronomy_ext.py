"""Extended astronomy generators -- stellar classification through Saha equation.

Covers spectral classification via Wien's law, luminosity distance,
mass-luminosity relation, Chandrasekhar limit, Hubble time,
angular diameter, virial theorem, and the Saha ionisation equation.
Tiers range from 4 (introductory) to 6 (advanced astrophysics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fmt(value: float, decimals: int = 4) -> str:
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


# Physical constants
_PI = math.pi
_K_B = 1.381e-23       # Boltzmann constant (J/K)
_K_B_EV = 8.617e-5     # Boltzmann constant (eV/K)
_WIEN_B = 2.898e-3     # Wien displacement constant (m*K)
_L_SUN = 3.828e26      # Solar luminosity (W)
_M_SUN = 1.989e30      # Solar mass (kg)
_MPC_TO_M = 3.086e22   # 1 Mpc in metres
_H0_DEFAULT = 70.0     # Hubble constant (km/s/Mpc)


# Spectral classification boundaries (K)
_SPECTRAL_BOUNDS = [
    ("O", 30000, 100000),
    ("B", 10000, 30000),
    ("A", 7500, 10000),
    ("F", 6000, 7500),
    ("G", 5200, 6000),
    ("K", 3700, 5200),
    ("M", 2400, 3700),
]


# ===================================================================
# 1. Stellar classification  (tier 4)
# ===================================================================

@register
class StellarClassificationGenerator(StepGenerator):
    """Classify a star by spectral type and compute peak wavelength.

    Given surface temperature T, determine spectral type O/B/A/F/G/K/M
    and compute peak emission wavelength via Wien's displacement law:
    lambda_max = b / T.

    Difficulty scaling:
        Difficulty 1-3: common types (G, K, M).
        Difficulty 4-6: all spectral types.
        Difficulty 7-8: given lambda_max, determine T and classify.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stellar_classification"

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
        return "classify star by spectral type and compute peak wavelength"

    @staticmethod
    def _classify(temp: int) -> str:
        """Classify temperature into spectral type.

        Args:
            temp: Surface temperature in Kelvin.

        Returns:
            Spectral type letter.
        """
        for letter, t_lo, t_hi in _SPECTRAL_BOUNDS:
            if t_lo <= temp < t_hi:
                return letter
        if temp >= 100000:
            return "O"
        return "M"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stellar classification problem.

        Args:
            difficulty: Controls spectral type pool and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = [b for b in _SPECTRAL_BOUNDS if b[0] in ("G", "K", "M")]
        else:
            pool = list(_SPECTRAL_BOUNDS)

        letter, t_lo, t_hi = self._rng.choice(pool)
        temp = self._rng.randint(t_lo, min(t_hi - 1, t_lo + 10000))
        spectral = self._classify(temp)
        lambda_max = round(_WIEN_B / temp, 4)
        lambda_nm = round(lambda_max * 1e9, 4)

        return "\\lambda_{max} = b / T", {
            "T": temp, "spectral": spectral,
            "lambda_max": lambda_max, "lambda_nm": lambda_nm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data with temperature and wavelength.

        Returns:
            List of step strings.
        """
        return [
            f"T = {data['T']} K",
            f"lambda_max = {_WIEN_B:.4e} / {data['T']} = {data['lambda_max']:.4e} m",
            f"lambda_max = {_fmt(data['lambda_nm'])} nm",
            f"spectral type: {data['spectral']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the spectral type and peak wavelength.

        Args:
            data: Solution data.

        Returns:
            String with classification and wavelength.
        """
        return f"type {data['spectral']}, lambda_max = {_fmt(data['lambda_nm'])} nm"


# ===================================================================
# 2. Luminosity distance  (tier 5)
# ===================================================================

@register
class LuminosityDistanceGenerator(StepGenerator):
    """Compute luminosity distance from flux and luminosity.

    d_L = sqrt(L / (4*pi*F)).  Given observed flux F and intrinsic
    luminosity L, compute the distance to the source.

    Difficulty scaling:
        Difficulty 1-3: solar-type luminosities, nearby.
        Difficulty 4-6: varied luminosities, moderate distances.
        Difficulty 7-8: compute in parsecs and light-years.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "luminosity_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute luminosity distance from flux and luminosity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a luminosity distance problem.

        Args:
            difficulty: Controls luminosity and flux ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lum_ratio = round(self._rng.uniform(0.5, 100.0), 4)
        lum = lum_ratio * _L_SUN

        if difficulty <= 3:
            flux_exp = self._rng.randint(-10, -8)
        elif difficulty <= 6:
            flux_exp = self._rng.randint(-14, -10)
        else:
            flux_exp = self._rng.randint(-18, -14)

        flux_mantissa = round(self._rng.uniform(1.0, 9.0), 2)
        flux = flux_mantissa * (10 ** flux_exp)

        d_m = round(math.sqrt(lum / (4 * _PI * flux)), 4)
        d_pc = round(d_m / 3.086e16, 4)

        return "d_L = \\sqrt{L / (4\\pi F)}", {
            "L_ratio": lum_ratio, "L": lum,
            "F_mantissa": flux_mantissa, "F_exp": flux_exp, "F": flux,
            "d_m": d_m, "d_pc": d_pc,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate luminosity distance steps.

        Args:
            data: Solution data with luminosity, flux, and distance.

        Returns:
            List of step strings.
        """
        return [
            f"L = {_fmt(data['L_ratio'])} L_sun = {data['L']:.4e} W",
            f"F = {data['F_mantissa']}e{data['F_exp']} W/m^2",
            f"d = sqrt(L/(4*pi*F)) = {data['d_m']:.4e} m",
            f"d = {data['d_pc']:.4e} pc",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the luminosity distance.

        Args:
            data: Solution data.

        Returns:
            String with distance in parsecs.
        """
        return f"d = {data['d_pc']:.4e} pc"


# ===================================================================
# 3. Mass-luminosity relation  (tier 5)
# ===================================================================

@register
class MassLuminosityGenerator(StepGenerator):
    """Compute main-sequence luminosity from stellar mass.

    L/L_sun ~ (M/M_sun)^3.5 for main-sequence stars.
    Given mass in solar masses, compute luminosity.

    Difficulty scaling:
        Difficulty 1-3: M = 1-3 M_sun.
        Difficulty 4-6: M = 0.5-10 M_sun.
        Difficulty 7-8: given L, solve for M.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_luminosity"

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
        return "compute luminosity from mass using mass-luminosity relation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass-luminosity problem.

        Args:
            difficulty: Controls mass range and problem direction.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m_ratio = round(self._rng.uniform(1.0, 3.0), 4)
        elif difficulty <= 6:
            m_ratio = round(self._rng.uniform(0.5, 10.0), 4)
        else:
            m_ratio = round(self._rng.uniform(0.3, 20.0), 4)

        l_ratio = round(m_ratio ** 3.5, 4)

        target = "L" if difficulty < 7 else "M"

        return "L/L_{\\odot} = (M/M_{\\odot})^{3.5}", {
            "M_ratio": m_ratio, "L_ratio": l_ratio,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mass-luminosity computation steps.

        Args:
            data: Solution data with mass and luminosity ratios.

        Returns:
            List of step strings.
        """
        if data["target"] == "L":
            return [
                f"M = {_fmt(data['M_ratio'])} M_sun",
                f"L/L_sun = ({_fmt(data['M_ratio'])})^3.5",
                f"L = {_fmt(data['L_ratio'])} L_sun",
            ]
        return [
            f"L = {_fmt(data['L_ratio'])} L_sun",
            f"M/M_sun = (L/L_sun)^(1/3.5) = ({_fmt(data['L_ratio'])})^(2/7)",
            f"M = {_fmt(data['M_ratio'])} M_sun",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the luminosity or mass.

        Args:
            data: Solution data.

        Returns:
            String with result in solar units.
        """
        if data["target"] == "L":
            return f"L = {_fmt(data['L_ratio'])} L_sun"
        return f"M = {_fmt(data['M_ratio'])} M_sun"


# ===================================================================
# 4. Chandrasekhar limit  (tier 5)
# ===================================================================

@register
class ChandrasekharLimitGenerator(StepGenerator):
    """Determine if a white dwarf exceeds the Chandrasekhar limit.

    M_Ch ~ 1.4 M_sun.  If the white dwarf mass exceeds this limit,
    it will undergo gravitational collapse (Type Ia supernova).

    Difficulty scaling:
        Difficulty 1-3: clearly above or below the limit.
        Difficulty 4-6: masses near the boundary.
        Difficulty 7-8: accreting white dwarf approaching limit.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chandrasekhar_limit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine if white dwarf exceeds Chandrasekhar limit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Chandrasekhar limit problem.

        Args:
            difficulty: Controls mass proximity to limit.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m_ch = 1.4

        if difficulty <= 3:
            exceeds = self._rng.choice([True, False])
            if exceeds:
                mass = round(self._rng.uniform(1.6, 3.0), 4)
            else:
                mass = round(self._rng.uniform(0.4, 1.1), 4)
        elif difficulty <= 6:
            mass = round(self._rng.uniform(1.2, 1.6), 4)
        else:
            initial = round(self._rng.uniform(1.0, 1.35), 4)
            accretion = round(self._rng.uniform(0.01, 0.5), 4)
            mass = round(initial + accretion, 4)

        exceeds = mass > m_ch
        outcome = "collapse (Type Ia SN)" if exceeds else "stable white dwarf"

        data = {
            "mass": mass, "M_Ch": m_ch,
            "exceeds": exceeds, "outcome": outcome,
        }

        if difficulty >= 7:
            data["initial"] = initial
            data["accretion"] = accretion

        return "M_{Ch} \\approx 1.4 M_{\\odot}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Chandrasekhar limit comparison steps.

        Args:
            data: Solution data with mass and limit.

        Returns:
            List of step strings.
        """
        steps = [f"M_Ch = {_fmt(data['M_Ch'])} M_sun"]
        if "initial" in data:
            steps.append(
                f"initial = {_fmt(data['initial'])}, "
                f"accreted = {_fmt(data['accretion'])} M_sun"
            )
        steps.append(f"M_WD = {_fmt(data['mass'])} M_sun")
        cmp = ">" if data["exceeds"] else "<="
        steps.append(f"M_WD {cmp} M_Ch -> {data['outcome']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the stability determination.

        Args:
            data: Solution data.

        Returns:
            String with outcome.
        """
        return f"M = {_fmt(data['mass'])} M_sun: {data['outcome']}"


# ===================================================================
# 5. Hubble time  (tier 4)
# ===================================================================

@register
class HubbleTimeGenerator(StepGenerator):
    """Estimate the age of the universe from the Hubble constant.

    t_H = 1/H_0.  Convert H_0 from km/s/Mpc to 1/s, then compute
    the Hubble time in seconds and Gyr.

    Difficulty scaling:
        Difficulty 1-3: H_0 = 70 km/s/Mpc exactly.
        Difficulty 4-6: H_0 between 60-80 km/s/Mpc.
        Difficulty 7-8: compute lookback time at given redshift.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hubble_time"

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
        return "estimate age of universe from Hubble constant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hubble time problem.

        Args:
            difficulty: Controls H_0 precision and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            h0 = 70.0
        else:
            h0 = round(self._rng.uniform(60.0, 80.0), 4)

        # Convert km/s/Mpc to 1/s
        h0_si = h0 * 1e3 / _MPC_TO_M
        t_h_s = round(1.0 / h0_si, 4)
        t_h_gyr = round(t_h_s / (3.156e7 * 1e9), 4)

        return "t_H = 1 / H_0", {
            "H_0": h0, "H_0_si": h0_si,
            "t_H_s": t_h_s, "t_H_Gyr": t_h_gyr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hubble time computation steps.

        Args:
            data: Solution data with H_0 and Hubble time.

        Returns:
            List of step strings.
        """
        return [
            f"H_0 = {_fmt(data['H_0'])} km/s/Mpc",
            f"H_0 = {data['H_0_si']:.4e} s^-1",
            f"t_H = 1/H_0 = {data['t_H_s']:.4e} s",
            f"t_H = {_fmt(data['t_H_Gyr'])} Gyr",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Hubble time.

        Args:
            data: Solution data.

        Returns:
            String with Hubble time in Gyr.
        """
        return f"t_H = {_fmt(data['t_H_Gyr'])} Gyr"


# ===================================================================
# 6. Angular diameter  (tier 4)
# ===================================================================

@register
class AngularDiameterGenerator(StepGenerator):
    """Compute angular diameter using the small-angle approximation.

    theta = d / D (radians), where d is physical size and D is
    distance.  Convert to arcseconds: theta_arcsec = theta * 206265.

    Difficulty scaling:
        Difficulty 1-3: nearby objects, large angular size.
        Difficulty 4-6: distant objects, small angular size.
        Difficulty 7-8: given theta, solve for D or d.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "angular_diameter"

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
        return "compute angular diameter using small-angle formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an angular diameter problem.

        Args:
            difficulty: Controls distance range and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rad_to_arcsec = 206265.0

        if difficulty <= 3:
            d_km = round(self._rng.uniform(1e3, 1e5), 4)
            dist_km = round(self._rng.uniform(1e6, 1e8), 4)
        elif difficulty <= 6:
            d_km = round(self._rng.uniform(1e5, 1e7), 4)
            dist_km = round(self._rng.uniform(1e10, 1e14), 4)
        else:
            d_km = round(self._rng.uniform(1e4, 1e8), 4)
            dist_km = round(self._rng.uniform(1e12, 1e16), 4)

        theta_rad = round(d_km / dist_km, 4)
        theta_arcsec = round(theta_rad * rad_to_arcsec, 4)

        target = "theta" if difficulty < 7 else "D"

        return "\\theta = d / D", {
            "d": d_km, "D": dist_km,
            "theta_rad": theta_rad, "theta_arcsec": theta_arcsec,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate angular diameter steps.

        Args:
            data: Solution data with sizes and angle.

        Returns:
            List of step strings.
        """
        if data["target"] == "theta":
            return [
                f"d = {data['d']:.4e} km, D = {data['D']:.4e} km",
                f"theta = d/D = {data['theta_rad']:.4e} rad",
                f"theta = {_fmt(data['theta_arcsec'])} arcsec",
            ]
        return [
            f"d = {data['d']:.4e} km, theta = {data['theta_rad']:.4e} rad",
            f"D = d/theta = {data['D']:.4e} km",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the angular diameter or distance.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "theta":
            return f"theta = {_fmt(data['theta_arcsec'])} arcsec"
        return f"D = {data['D']:.4e} km"


# ===================================================================
# 7. Virial theorem  (tier 5)
# ===================================================================

@register
class VirialTheoremGenerator(StepGenerator):
    """Apply the virial theorem: 2<KE> + <PE> = 0.

    Given kinetic energy KE, compute potential energy PE = -2*KE
    and total energy E = KE + PE = -KE.

    Difficulty scaling:
        Difficulty 1-3: given KE directly.
        Difficulty 4-6: given velocity dispersion and mass, compute KE first.
        Difficulty 7-8: determine if system is bound (E<0) or unbound.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "virial_theorem"

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
        return "apply virial theorem to compute energy components"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a virial theorem problem.

        Args:
            difficulty: Controls input format and output detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            ke_exp = self._rng.randint(30, 40)
            ke_mantissa = round(self._rng.uniform(1.0, 9.0), 2)
            ke = ke_mantissa * (10 ** ke_exp)
        else:
            mass_exp = self._rng.randint(30, 35)
            mass = round(self._rng.uniform(1.0, 9.0), 2) * (10 ** mass_exp)
            v_km = round(self._rng.uniform(100, 1000), 4)
            v_m = v_km * 1e3
            ke = round(0.5 * mass * v_m ** 2, 4)

        pe = round(-2 * ke, 4)
        total_e = round(ke + pe, 4)  # = -ke
        bound = total_e < 0

        data = {
            "KE": ke, "PE": pe, "E_total": total_e,
            "bound": bound,
        }
        if difficulty > 3:
            data["mass"] = mass
            data["v_km"] = v_km

        return "2\\langle KE \\rangle + \\langle PE \\rangle = 0", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate virial theorem computation steps.

        Args:
            data: Solution data with energy components.

        Returns:
            List of step strings.
        """
        steps = []
        if "mass" in data:
            steps.append(f"M = {data['mass']:.4e} kg, v = {_fmt(data['v_km'])} km/s")
            steps.append(f"KE = 0.5*M*v^2 = {data['KE']:.4e} J")
        else:
            steps.append(f"KE = {data['KE']:.4e} J")
        steps.append(f"PE = -2*KE = {data['PE']:.4e} J")
        steps.append(f"E_total = KE + PE = {data['E_total']:.4e} J")
        status = "bound" if data["bound"] else "unbound"
        steps.append(f"system: {status}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the energy components and binding status.

        Args:
            data: Solution data.

        Returns:
            String with PE, E_total, and binding.
        """
        status = "bound" if data["bound"] else "unbound"
        return f"PE = {data['PE']:.4e} J, E = {data['E_total']:.4e} J ({status})"


# ===================================================================
# 8. Saha equation  (tier 6)
# ===================================================================

@register
class SahaEquationGenerator(StepGenerator):
    """Compute ionisation fraction using the Saha equation.

    n_{i+1}*n_e / n_i = (2/lambda_dB^3) * (g_{i+1}/g_i) * exp(-chi/kT).
    For hydrogen: g_0=2, g_1=1, chi=13.6 eV.
    Simplified form for hydrogen assuming n_e ~ n_i+1.

    Difficulty scaling:
        Difficulty 1-3: high T (mostly ionised).
        Difficulty 4-6: moderate T, compute ratio.
        Difficulty 7-8: compare ionisation at two temperatures.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "saha_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute ionisation fraction using Saha equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Saha equation problem.

        Args:
            difficulty: Controls temperature and detail level.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        chi_ev = 13.6  # ionisation energy of hydrogen (eV)
        g_0 = 2
        g_1 = 1

        if difficulty <= 3:
            temp = self._rng.randint(10000, 30000)
        elif difficulty <= 6:
            temp = self._rng.randint(5000, 15000)
        else:
            temp = self._rng.randint(4000, 20000)

        kt_ev = round(_K_B_EV * temp, 4)
        exponent = round(-chi_ev / kt_ev, 4)
        boltzmann_factor = round(math.exp(exponent), 4)
        ratio = round((2 * g_1 / g_0) * boltzmann_factor, 4)

        # Classify ionisation state
        if ratio > 10:
            state = "mostly ionised"
        elif ratio > 0.1:
            state = "partially ionised"
        else:
            state = "mostly neutral"

        data = {
            "T": temp, "chi": chi_ev,
            "g_0": g_0, "g_1": g_1,
            "kT": kt_ev, "exponent": exponent,
            "boltzmann": boltzmann_factor,
            "ratio": ratio, "state": state,
        }

        if difficulty >= 7:
            t2 = self._rng.randint(4000, 20000)
            kt2 = round(_K_B_EV * t2, 4)
            exp2 = round(-chi_ev / kt2, 4)
            bf2 = round(math.exp(exp2), 4)
            ratio2 = round((2 * g_1 / g_0) * bf2, 4)
            data["T2"] = t2
            data["ratio2"] = ratio2
            data["more_ionised"] = "T1" if ratio > ratio2 else "T2"

        return "\\frac{n_{i+1} n_e}{n_i} \\propto \\exp(-\\chi / kT)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Saha equation computation steps.

        Args:
            data: Solution data with temperature and ionisation ratio.

        Returns:
            List of step strings.
        """
        steps = [
            f"T = {data['T']} K, chi = {_fmt(data['chi'])} eV",
            f"kT = {_fmt(data['kT'])} eV",
            f"exp(-chi/kT) = exp({_fmt(data['exponent'])}) = {_fmt(data['boltzmann'])}",
            f"ionisation ratio ~ {_fmt(data['ratio'])}",
            f"state: {data['state']}",
        ]
        if "T2" in data:
            steps.append(f"T2 = {data['T2']} K -> ratio = {_fmt(data['ratio2'])}")
            steps.append(f"more ionised: {data['more_ionised']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ionisation ratio and state.

        Args:
            data: Solution data.

        Returns:
            String with ratio and classification.
        """
        ans = f"ratio = {_fmt(data['ratio'])}, {data['state']}"
        if "more_ionised" in data:
            ans += f", more ionised at {data['more_ionised']}"
        return ans
