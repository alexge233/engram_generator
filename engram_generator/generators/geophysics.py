"""Geophysics generators -- gravity, magnetics, plates, seismicity, isostasy, heat flow.

6 generators covering Bouguer gravity anomaly, magnetic declination
correction, plate velocity from hotspot tracks, seismic moment and
moment magnitude, Airy isostasy, and geothermal heat flow. Tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _GeoFormatter:
    """Formats numeric values for geophysics problems.

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


_f = _GeoFormatter.fmt


# ===================================================================
# 1. Gravity anomaly (Bouguer)  (tier 5)
# ===================================================================

@register
class GravityAnomalyGenerator(StepGenerator):
    """Compute Bouguer gravity anomaly step by step.

    Bouguer anomaly = g_obs - g_theo + FAC - BC
    where FAC = 0.3086 * h (mGal) is the free-air correction and
    BC = 0.04193 * rho * h (mGal) is the Bouguer correction,
    with h in metres and rho in kg/m^3.

    Difficulty scaling:
        Difficulty 1-3: integer elevations (100-500 m), rho = 2670.
        Difficulty 4-6: decimal elevations, varied rho.
        Difficulty 7-8: precise values, negative elevations (below sea level).

    Prerequisites:
        subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gravity_anomaly"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Bouguer gravity anomaly"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate gravity observations and compute Bouguer anomaly.

        Args:
            difficulty: Controls parameter ranges and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            h = float(self._rng.randint(100, 500))
            rho = 2670.0
            g_obs = round(self._rng.uniform(978000, 982000), 1)
        elif difficulty <= 6:
            h = round(self._rng.uniform(50, 2000), 1)
            rho = round(self._rng.uniform(2500, 2800), 0)
            g_obs = round(self._rng.uniform(978000, 982000), 2)
        else:
            h = round(self._rng.uniform(-100, 3000), 2)
            rho = round(self._rng.uniform(2400, 3000), 0)
            g_obs = round(self._rng.uniform(977000, 983000), 2)

        g_theo = round(self._rng.uniform(978000, 982000), 2)
        fac = round(0.3086 * h, 4)
        bc = round(0.04193 * rho * h, 4)
        bouguer = round(g_obs - g_theo + fac - bc, 4)

        problem = (
            f"g_obs = {g_obs} mGal, g_theo = {g_theo} mGal, "
            f"h = {h} m, rho = {rho} kg/m^3"
        )
        return problem, {
            "g_obs": g_obs, "g_theo": g_theo, "h": h, "rho": rho,
            "FAC": fac, "BC": bc, "bouguer": bouguer,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bouguer anomaly computation steps.

        Args:
            data: Solution data with observations and corrections.

        Returns:
            List of step strings.
        """
        diff = round(data["g_obs"] - data["g_theo"], 4)
        return [
            f"g_obs - g_theo = {_f(data['g_obs'])} - "
            f"{_f(data['g_theo'])} = {_f(diff)}",
            f"FAC = 0.3086 * {_f(data['h'])} = {_f(data['FAC'])} mGal",
            f"BC = 0.04193 * {_f(data['rho'])} * {_f(data['h'])} "
            f"= {_f(data['BC'])} mGal",
            f"Bouguer = {_f(diff)} + {_f(data['FAC'])} - {_f(data['BC'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Bouguer anomaly.

        Args:
            data: Solution data.

        Returns:
            String with anomaly in mGal.
        """
        return f"Bouguer anomaly = {_f(data['bouguer'])} mGal"


# ===================================================================
# 2. Magnetic declination  (tier 4)
# ===================================================================

@register
class MagneticDeclinationGenerator(StepGenerator):
    """Compute true bearing from magnetic bearing and declination.

    True bearing = magnetic bearing + declination (east positive,
    west negative). Result normalised to [0, 360) degrees.

    Difficulty scaling:
        Difficulty 1-3: small positive declination (0-15 deg).
        Difficulty 4-6: positive or negative declination (-20 to 20).
        Difficulty 7-8: large declination, bearings near 0/360 wrap.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnetic_declination"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute true bearing from magnetic bearing and declination"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate magnetic bearing and declination, compute true bearing.

        Args:
            difficulty: Controls declination range and wrap scenarios.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            mag_bearing = float(self._rng.randint(10, 350))
            decl = float(self._rng.randint(1, 15))
        elif difficulty <= 6:
            mag_bearing = float(self._rng.randint(0, 359))
            decl = float(self._rng.randint(-20, 20))
        else:
            mag_bearing = round(self._rng.uniform(0, 359.9), 1)
            decl = round(self._rng.uniform(-30, 30), 1)

        raw = round(mag_bearing + decl, 4)
        true_bearing = round(raw % 360, 4)

        problem = (
            f"magnetic bearing = {mag_bearing} deg, "
            f"declination = {decl} deg; find true bearing"
        )
        return problem, {
            "mag_bearing": mag_bearing, "decl": decl,
            "raw": raw, "true_bearing": true_bearing,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate declination correction steps.

        Args:
            data: Solution data with bearings and declination.

        Returns:
            List of step strings.
        """
        steps = [
            f"magnetic bearing = {_f(data['mag_bearing'])} deg",
            f"declination = {_f(data['decl'])} deg",
            f"true = {_f(data['mag_bearing'])} + ({_f(data['decl'])}) "
            f"= {_f(data['raw'])}",
        ]
        if data["raw"] < 0 or data["raw"] >= 360:
            steps.append(f"normalise: {_f(data['raw'])} mod 360 "
                         f"= {_f(data['true_bearing'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the true bearing.

        Args:
            data: Solution data.

        Returns:
            String with true bearing in degrees.
        """
        return f"true bearing = {_f(data['true_bearing'])} deg"


# ===================================================================
# 3. Plate velocity  (tier 4)
# ===================================================================

@register
class PlateVelocityGenerator(StepGenerator):
    """Compute plate velocity from hotspot track distance and age.

    v = d / t where d is the distance between volcanic features (km)
    and t is the age difference (Myr). Result in cm/yr.

    Difficulty scaling:
        Difficulty 1-3: integer distances (100-1000 km) and ages (1-50 Myr).
        Difficulty 4-6: decimal distances and ages.
        Difficulty 7-8: precise measurements, convert km/Myr to cm/yr.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "plate_velocity"

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
        return "compute plate velocity from hotspot track"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate distance and age, compute plate velocity.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            d_km = float(self._rng.randint(100, 1000))
            t_myr = float(self._rng.randint(1, 50))
        elif difficulty <= 6:
            d_km = round(self._rng.uniform(50, 2000), 1)
            t_myr = round(self._rng.uniform(1, 100), 1)
        else:
            d_km = round(self._rng.uniform(20, 5000), 2)
            t_myr = round(self._rng.uniform(0.5, 200), 2)

        v_km_myr = round(d_km / t_myr, 4)
        # 1 km/Myr = 0.1 cm/yr
        v_cm_yr = round(v_km_myr * 0.1, 4)

        problem = (
            f"distance = {d_km} km, age difference = {t_myr} Myr; "
            f"compute plate velocity in cm/yr"
        )
        return problem, {
            "d_km": d_km, "t_myr": t_myr,
            "v_km_myr": v_km_myr, "v_cm_yr": v_cm_yr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate plate velocity computation steps.

        Args:
            data: Solution data with distance, age, and velocity.

        Returns:
            List of step strings.
        """
        return [
            f"d = {_f(data['d_km'])} km, t = {_f(data['t_myr'])} Myr",
            f"v = d/t = {_f(data['d_km'])}/{_f(data['t_myr'])} "
            f"= {_f(data['v_km_myr'])} km/Myr",
            f"v = {_f(data['v_km_myr'])} * 0.1 = {_f(data['v_cm_yr'])} cm/yr",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the plate velocity.

        Args:
            data: Solution data.

        Returns:
            String with velocity in cm/yr.
        """
        return f"v = {_f(data['v_cm_yr'])} cm/yr"


# ===================================================================
# 4. Seismic moment  (tier 5)
# ===================================================================

@register
class SeismicMomentGenerator(StepGenerator):
    """Compute seismic moment M_0 and moment magnitude M_w.

    M_0 = mu * A * d (N*m) where mu is rigidity, A is fault area,
    d is slip. Moment magnitude: M_w = (2/3)*log10(M_0) - 10.7.

    Difficulty scaling:
        Difficulty 1-3: small fault (A < 100 km^2), integer slip.
        Difficulty 4-6: moderate fault, decimal parameters.
        Difficulty 7-8: large fault, precise mu values.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "seismic_moment"

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
        return "compute seismic moment and moment magnitude"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fault parameters and compute M_0 and M_w.

        Args:
            difficulty: Controls fault size and parameter precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mu = 3.0e10  # Pa (typical crustal rigidity)
            a_km2 = float(self._rng.randint(10, 100))
            slip_m = float(self._rng.randint(1, 5))
        elif difficulty <= 6:
            mu = round(self._rng.uniform(2.5e10, 4.0e10), 4)
            a_km2 = round(self._rng.uniform(10, 1000), 1)
            slip_m = round(self._rng.uniform(0.5, 10), 1)
        else:
            mu = round(self._rng.uniform(2.0e10, 5.0e10), 4)
            a_km2 = round(self._rng.uniform(50, 10000), 2)
            slip_m = round(self._rng.uniform(0.1, 20), 2)

        a_m2 = round(a_km2 * 1e6, 4)  # km^2 -> m^2
        m_0 = round(mu * a_m2 * slip_m, 4)
        log_m0 = round(math.log10(m_0), 4)
        m_w = round((2.0 / 3.0) * log_m0 - 10.7, 4)

        problem = (
            f"mu = {mu} Pa, A = {a_km2} km^2, "
            f"slip = {slip_m} m; compute M_0 and M_w"
        )
        return problem, {
            "mu": mu, "A_km2": a_km2, "A_m2": a_m2,
            "slip": slip_m, "M_0": m_0,
            "log_M0": log_m0, "M_w": m_w,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate seismic moment computation steps.

        Args:
            data: Solution data with fault parameters and magnitudes.

        Returns:
            List of step strings.
        """
        return [
            f"A = {_f(data['A_km2'])} km^2 = {_f(data['A_m2'])} m^2",
            f"M_0 = {_f(data['mu'])} * {_f(data['A_m2'])} * "
            f"{_f(data['slip'])} = {_f(data['M_0'])} N*m",
            f"log10(M_0) = {_f(data['log_M0'])}",
            f"M_w = (2/3)*{_f(data['log_M0'])} - 10.7 = {_f(data['M_w'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the seismic moment and moment magnitude.

        Args:
            data: Solution data.

        Returns:
            String with M_0 and M_w.
        """
        return f"M_0 = {_f(data['M_0'])} N*m, M_w = {_f(data['M_w'])}"


# ===================================================================
# 5. Isostasy (Airy model)  (tier 5)
# ===================================================================

@register
class IsostasyGenerator(StepGenerator):
    """Compute Airy isostatic root depth.

    Root depth r = (rho_c / (rho_m - rho_c)) * h where rho_c is
    crustal density, rho_m is mantle density, and h is the
    elevation above the reference level.

    Difficulty scaling:
        Difficulty 1-3: standard densities (2700, 3300), integer h.
        Difficulty 4-6: varied densities, decimal h.
        Difficulty 7-8: precise densities, large h values.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "isostasy"

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
        return "compute Airy isostatic root depth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate densities and elevation, compute root depth.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            rho_c = 2700.0
            rho_m = 3300.0
            h = float(self._rng.randint(500, 5000))
        elif difficulty <= 6:
            rho_c = round(self._rng.uniform(2600, 2800), 0)
            rho_m = round(self._rng.uniform(3200, 3400), 0)
            h = round(self._rng.uniform(200, 8000), 1)
        else:
            rho_c = round(self._rng.uniform(2500, 2900), 0)
            rho_m = round(self._rng.uniform(3100, 3500), 0)
            h = round(self._rng.uniform(100, 10000), 2)

        delta_rho = round(rho_m - rho_c, 4)
        ratio = round(rho_c / delta_rho, 4)
        root = round(ratio * h, 4)

        problem = (
            f"rho_c = {rho_c} kg/m^3, rho_m = {rho_m} kg/m^3, "
            f"h = {h} m; compute root depth"
        )
        return problem, {
            "rho_c": rho_c, "rho_m": rho_m, "h": h,
            "delta_rho": delta_rho, "ratio": ratio, "root": root,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate isostasy computation steps.

        Args:
            data: Solution data with densities and root depth.

        Returns:
            List of step strings.
        """
        return [
            f"rho_m - rho_c = {_f(data['rho_m'])} - {_f(data['rho_c'])} "
            f"= {_f(data['delta_rho'])}",
            f"rho_c/(rho_m-rho_c) = {_f(data['rho_c'])}/"
            f"{_f(data['delta_rho'])} = {_f(data['ratio'])}",
            f"r = {_f(data['ratio'])} * {_f(data['h'])} = {_f(data['root'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the root depth.

        Args:
            data: Solution data.

        Returns:
            String with root in metres.
        """
        return f"root = {_f(data['root'])} m"


# ===================================================================
# 6. Heat flow  (tier 5)
# ===================================================================

@register
class HeatFlowGenerator(StepGenerator):
    """Compute geothermal heat flow q = -k * dT/dz.

    Given thermal conductivity k (W/(m*K)) and temperature gradient
    dT/dz (K/m or degC/km), computes the surface heat flow in mW/m^2.

    Difficulty scaling:
        Difficulty 1-3: k in [2, 4], dT/dz in [20, 40] degC/km.
        Difficulty 4-6: k in [1, 5], dT/dz in [10, 60] degC/km.
        Difficulty 7-8: varied k and gradient, convert units.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heat_flow"

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
        return "compute geothermal heat flow"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate k and dT/dz, compute heat flow.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = float(self._rng.randint(2, 4))
            dt_dz_km = float(self._rng.randint(20, 40))
        elif difficulty <= 6:
            k = round(self._rng.uniform(1.0, 5.0), 1)
            dt_dz_km = round(self._rng.uniform(10, 60), 1)
        else:
            k = round(self._rng.uniform(0.5, 6.0), 2)
            dt_dz_km = round(self._rng.uniform(5, 100), 2)

        # Convert degC/km to K/m: divide by 1000
        dt_dz_m = round(dt_dz_km / 1000.0, 4)
        # q = k * dT/dz (W/m^2), report as mW/m^2
        q_wm2 = round(k * dt_dz_m, 4)
        q_mwm2 = round(q_wm2 * 1000.0, 4)

        problem = (
            f"k = {k} W/(m*K), dT/dz = {dt_dz_km} degC/km; "
            f"compute heat flow in mW/m^2"
        )
        return problem, {
            "k": k, "dT_dz_km": dt_dz_km, "dT_dz_m": dt_dz_m,
            "q_Wm2": q_wm2, "q_mWm2": q_mwm2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate heat flow computation steps.

        Args:
            data: Solution data with conductivity and gradient.

        Returns:
            List of step strings.
        """
        return [
            f"dT/dz = {_f(data['dT_dz_km'])} degC/km "
            f"= {_f(data['dT_dz_m'])} K/m",
            f"q = k * dT/dz = {_f(data['k'])} * {_f(data['dT_dz_m'])} "
            f"= {_f(data['q_Wm2'])} W/m^2",
            f"q = {_f(data['q_Wm2'])} * 1000 = {_f(data['q_mWm2'])} mW/m^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat flow.

        Args:
            data: Solution data.

        Returns:
            String with q in mW/m^2.
        """
        return f"q = {_f(data['q_mWm2'])} mW/m^2"
