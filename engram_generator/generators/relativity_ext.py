"""Extended special relativity generators.

8 generators across tiers 5-6 covering relativistic momentum,
mass-energy equivalence, relativistic Doppler effect, twin paradox,
Compton scattering, relativistic kinetic energy, invariant mass of
two-particle systems, and photon momentum.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.relativity import (
    RelativityFormatter,
    VelocitySampler,
    _compute_gamma,
)


def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if isinstance(rounded, float) and rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# Physical constants
_C = 3e8          # speed of light in m/s
_H = 6.626e-34    # Planck constant in J*s
_ME = 9.109e-31   # electron mass in kg
_MEV_PER_J = 6.242e12  # MeV per Joule


# ---------------------------------------------------------------------------
# 1. Relativistic Momentum (tier 5)
# ---------------------------------------------------------------------------

@register
class RelativisticMomentumGenerator(StepGenerator):
    """Compute relativistic momentum p = gamma * m * v.

    Compares with classical momentum p_classical = m * v to show
    the relativistic correction factor.

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], mass ~ 1e-27 kg.
        d4-6: beta in [0.5, 0.9], mass ~ 1e-27 to 1e-20 kg.
        d7-8: beta in [0.9, 0.99], mass ~ 1e-27 to 1e-15 kg.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relativistic_momentum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute relativistic momentum"

    def _sample_mass(self, difficulty: int) -> float:
        """Sample a rest mass in kg scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Rest mass in kg.
        """
        if difficulty <= 3:
            exponent = -27
        elif difficulty <= 6:
            exponent = self._rng.randint(-27, -20)
        else:
            exponent = self._rng.randint(-27, -15)
        mantissa = self._rng.randint(1, 9)
        return float(mantissa) * (10 ** exponent)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and velocity, compute relativistic momentum.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        mass = self._sample_mass(difficulty)
        v = beta * _C
        gamma = round(_compute_gamma(beta), 4)
        p_rel = gamma * mass * v
        p_class = mass * v
        return "p = \\gamma m v", {
            "beta": beta, "gamma": gamma, "mass": mass,
            "v": v, "p_rel": p_rel, "p_class": p_class,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate relativistic momentum computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing gamma, relativistic and classical momentum.
        """
        m_str = RelativityFormatter.format_sci(sd["mass"])
        v_str = RelativityFormatter.format_sci(sd["v"])
        p_rel_str = RelativityFormatter.format_sci(sd["p_rel"])
        p_class_str = RelativityFormatter.format_sci(sd["p_class"])
        return [
            f"\\beta = {sd['beta']}, \\gamma = {sd['gamma']}",
            f"p_rel = {sd['gamma']} * {m_str} * {v_str} = {p_rel_str} kg m/s",
            f"p_class = {m_str} * {v_str} = {p_class_str} kg m/s",
            f"ratio = {sd['gamma']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the relativistic momentum.

        Args:
            sd: Solution data dict.

        Returns:
            Momentum in scientific notation.
        """
        return f"p = {RelativityFormatter.format_sci(sd['p_rel'])} kg m/s"


# ---------------------------------------------------------------------------
# 2. Mass-Energy Equivalence (tier 5)
# ---------------------------------------------------------------------------

@register
class MassEnergyEquivalenceGenerator(StepGenerator):
    """Compute rest energy E = mc^2 in Joules and MeV.

    Converts a given rest mass to energy using E_rest = mc^2 and
    expresses the result in both Joules and MeV.

    Difficulty scaling:
        d1-3: electron mass scale (~1e-30 kg).
        d4-6: proton mass scale (~1e-27 kg).
        d7-8: heavier particles (~1e-25 to 1e-20 kg).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_energy_equivalence"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute rest energy E=mc^2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass and compute E=mc^2 in J and MeV.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            exponent = self._rng.randint(-31, -29)
        elif difficulty <= 6:
            exponent = self._rng.randint(-28, -26)
        else:
            exponent = self._rng.randint(-25, -20)
        mantissa = self._rng.randint(1, 9)
        mass = float(mantissa) * (10 ** exponent)
        c_sq = _C ** 2
        energy_j = mass * c_sq
        energy_mev = energy_j * _MEV_PER_J
        m_str = RelativityFormatter.format_sci(mass)
        return (
            f"E = mc^2 for m = {m_str} kg",
            {
                "mass": mass, "energy_j": energy_j,
                "energy_mev": energy_mev,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate mass-energy computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing mc^2 in Joules and MeV conversion.
        """
        m_str = RelativityFormatter.format_sci(sd["mass"])
        e_j_str = RelativityFormatter.format_sci(sd["energy_j"])
        e_mev_str = RelativityFormatter.format_sci(sd["energy_mev"])
        return [
            f"E = mc^2 = ({m_str})(9 \\times 10^{{16}})",
            f"E = {e_j_str} J",
            f"E = {e_mev_str} MeV",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rest energy.

        Args:
            sd: Solution data dict.

        Returns:
            Energy in Joules and MeV.
        """
        e_j = RelativityFormatter.format_sci(sd["energy_j"])
        e_mev = RelativityFormatter.format_sci(sd["energy_mev"])
        return f"E = {e_j} J = {e_mev} MeV"


# ---------------------------------------------------------------------------
# 3. Relativistic Doppler (tier 5)
# ---------------------------------------------------------------------------

@register
class RelativisticDopplerGenerator(StepGenerator):
    """Compute the relativistic Doppler shifted frequency.

    f_obs = f_source * sqrt((1+beta)/(1-beta)) for approaching,
    f_obs = f_source * sqrt((1-beta)/(1+beta)) for receding.

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], visible light frequencies.
        d4-6: beta in [0.5, 0.9].
        d7-8: beta in [0.9, 0.99].
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relativistic_doppler"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute relativistic Doppler shift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate source frequency and velocity, compute observed frequency.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        direction = self._rng.choice(["approaching", "receding"])
        # Visible light frequency ~ 4e14 to 8e14 Hz
        f_source = round(self._rng.uniform(4e14, 8e14), 0)
        if direction == "approaching":
            factor = math.sqrt((1 + beta) / (1 - beta))
        else:
            factor = math.sqrt((1 - beta) / (1 + beta))
        factor = round(factor, 4)
        f_obs = round(f_source * factor, 4)
        f_src_str = RelativityFormatter.format_sci(f_source)
        return (
            f"f_source = {f_src_str} Hz, beta = {beta}, {direction}",
            {
                "beta": beta, "direction": direction,
                "f_source": f_source, "factor": factor,
                "f_obs": f_obs,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Doppler shift computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing ratio computation and frequency scaling.
        """
        beta = sd["beta"]
        if sd["direction"] == "approaching":
            ratio_str = f"(1+{beta})/(1-{beta})"
        else:
            ratio_str = f"(1-{beta})/(1+{beta})"
        f_src_str = RelativityFormatter.format_sci(sd["f_source"])
        f_obs_str = RelativityFormatter.format_sci(sd["f_obs"])
        return [
            f"direction: {sd['direction']}",
            f"factor = sqrt({ratio_str}) = {_fmt(sd['factor'])}",
            f"f_obs = {f_src_str} * {_fmt(sd['factor'])} = {f_obs_str} Hz",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the observed frequency.

        Args:
            sd: Solution data dict.

        Returns:
            Frequency in scientific notation.
        """
        return f"f_obs = {RelativityFormatter.format_sci(sd['f_obs'])} Hz"


# ---------------------------------------------------------------------------
# 4. Twin Paradox (tier 6)
# ---------------------------------------------------------------------------

@register
class TwinParadoxGenerator(StepGenerator):
    """Compute the proper time for a relativistic traveler vs Earth observer.

    The traveler's proper time tau = T / gamma, where T is the
    coordinate time (Earth time). Computes the age difference.

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], trip of 1-10 years.
        d4-6: beta in [0.5, 0.9], trip of 1-20 years.
        d7-8: beta in [0.9, 0.99], trip of 1-50 years.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "twin_paradox"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute twin paradox age difference"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate travel parameters and compute proper time difference.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        if difficulty <= 3:
            earth_time = float(self._rng.randint(1, 10))
        elif difficulty <= 6:
            earth_time = float(self._rng.randint(1, 20))
        else:
            earth_time = float(self._rng.randint(1, 50))
        proper_time = round(earth_time / gamma, 4)
        age_diff = round(earth_time - proper_time, 4)
        return (
            f"twin travels at beta={beta} for T={_fmt(earth_time)} years (Earth)",
            {
                "beta": beta, "gamma": gamma,
                "earth_time": earth_time,
                "proper_time": proper_time,
                "age_diff": age_diff,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate twin paradox computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing gamma, proper time, and age difference.
        """
        return [
            f"\\beta = {sd['beta']}, \\gamma = {sd['gamma']}",
            f"\\tau = T/\\gamma = {_fmt(sd['earth_time'])}/{sd['gamma']} = {_fmt(sd['proper_time'])} years",
            f"age difference = {_fmt(sd['earth_time'])} - {_fmt(sd['proper_time'])} = {_fmt(sd['age_diff'])} years",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the proper time and age difference.

        Args:
            sd: Solution data dict.

        Returns:
            Traveler age and difference.
        """
        return f"tau = {_fmt(sd['proper_time'])} yr, diff = {_fmt(sd['age_diff'])} yr"


# ---------------------------------------------------------------------------
# 5. Compton Scattering (tier 6)
# ---------------------------------------------------------------------------

@register
class ComptonScatteringGenerator(StepGenerator):
    """Compute the wavelength shift in Compton scattering.

    lambda' - lambda = (h / m_e c)(1 - cos(theta)).  The Compton
    wavelength of the electron is h/(m_e c) = 2.426e-12 m.

    Difficulty scaling:
        d1-3: theta in {90, 180} degrees, simple angles.
        d4-6: theta in {30, 45, 60, 90, 120, 150, 180}.
        d7-8: arbitrary theta from 10 to 170 degrees.
    """

    _COMPTON_WL = 2.426e-12  # h / (m_e * c) in metres

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compton_scattering"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute Compton scattering wavelength shift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate scattering angle and compute wavelength shift.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            theta_deg = self._rng.choice([90, 180])
        elif difficulty <= 6:
            theta_deg = self._rng.choice([30, 45, 60, 90, 120, 150, 180])
        else:
            theta_deg = self._rng.randint(10, 170)
        theta_rad = math.radians(theta_deg)
        cos_theta = round(math.cos(theta_rad), 4)
        delta_lambda = round(self._compton_shift(cos_theta), 4)
        # Initial wavelength: X-ray range (1e-11 to 1e-10 m)
        lambda_init = round(self._rng.uniform(1e-11, 1e-10), 4)
        lambda_final = round(lambda_init + delta_lambda, 4)
        return (
            f"Compton scattering: lambda={RelativityFormatter.format_sci(lambda_init)} m, theta={theta_deg} deg",
            {
                "theta_deg": theta_deg, "cos_theta": cos_theta,
                "delta_lambda": delta_lambda,
                "lambda_init": lambda_init,
                "lambda_final": lambda_final,
            },
        )

    def _compton_shift(self, cos_theta: float) -> float:
        """Compute the Compton wavelength shift.

        Args:
            cos_theta: Cosine of the scattering angle.

        Returns:
            Wavelength shift in metres.
        """
        return self._COMPTON_WL * (1 - cos_theta)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Compton scattering computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing Compton formula application.
        """
        dl_str = RelativityFormatter.format_sci(sd["delta_lambda"])
        lf_str = RelativityFormatter.format_sci(sd["lambda_final"])
        return [
            f"cos({sd['theta_deg']}) = {_fmt(sd['cos_theta'])}",
            f"Delta lambda = (h/m_e c)(1 - cos theta) = 2.426e-12 * (1 - {_fmt(sd['cos_theta'])})",
            f"Delta lambda = {dl_str} m",
            f"lambda' = {RelativityFormatter.format_sci(sd['lambda_init'])} + {dl_str} = {lf_str} m",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the shifted wavelength.

        Args:
            sd: Solution data dict.

        Returns:
            Wavelength shift and final wavelength.
        """
        dl = RelativityFormatter.format_sci(sd["delta_lambda"])
        lf = RelativityFormatter.format_sci(sd["lambda_final"])
        return f"Delta lambda = {dl} m, lambda' = {lf} m"


# ---------------------------------------------------------------------------
# 6. Relativistic Kinetic Energy (tier 5)
# ---------------------------------------------------------------------------

@register
class RelativisticKineticGenerator(StepGenerator):
    """Compute relativistic kinetic energy KE = (gamma-1)*mc^2.

    Compares with classical KE = 0.5*mv^2 to show the relativistic
    correction at different velocities.

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], mass ~ 1e-27 kg.
        d4-6: beta in [0.5, 0.9].
        d7-8: beta in [0.9, 0.99].
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relativistic_kinetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["relativistic_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute relativistic vs classical kinetic energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and velocity, compute both kinetic energies.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        exponent = self._rng.randint(-27, -25)
        mantissa = self._rng.randint(1, 9)
        mass = float(mantissa) * (10 ** exponent)
        v = beta * _C
        mc2 = mass * _C ** 2
        ke_rel = (gamma - 1) * mc2
        ke_class = 0.5 * mass * v * v
        ratio = round(ke_rel / ke_class, 4) if ke_class > 0 else 0.0
        return (
            f"KE: m={RelativityFormatter.format_sci(mass)} kg, beta={beta}",
            {
                "beta": beta, "gamma": gamma, "mass": mass,
                "mc2": mc2, "ke_rel": ke_rel, "ke_class": ke_class,
                "ratio": ratio,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate kinetic energy comparison steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing both KE computations and ratio.
        """
        mc2_str = RelativityFormatter.format_sci(sd["mc2"])
        ke_rel_str = RelativityFormatter.format_sci(sd["ke_rel"])
        ke_class_str = RelativityFormatter.format_sci(sd["ke_class"])
        gamma_m1 = round(sd["gamma"] - 1, 4)
        return [
            f"\\gamma = {sd['gamma']}, \\gamma - 1 = {_fmt(gamma_m1)}",
            f"KE_rel = {_fmt(gamma_m1)} * {mc2_str} = {ke_rel_str} J",
            f"KE_class = 0.5 * m * v^2 = {ke_class_str} J",
            f"ratio KE_rel/KE_class = {_fmt(sd['ratio'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return both kinetic energies.

        Args:
            sd: Solution data dict.

        Returns:
            Relativistic and classical KE.
        """
        ke_r = RelativityFormatter.format_sci(sd["ke_rel"])
        ke_c = RelativityFormatter.format_sci(sd["ke_class"])
        return f"KE_rel = {ke_r} J, KE_class = {ke_c} J"


# ---------------------------------------------------------------------------
# 7. Invariant Mass Two Particle (tier 6)
# ---------------------------------------------------------------------------

@register
class InvariantMassTwoParticleGenerator(StepGenerator):
    """Compute the invariant mass of a two-particle system.

    M^2*c^4 = (E1+E2)^2 - (p1+p2)^2*c^2.  Given energies and
    momenta of decay products, compute the parent particle mass.

    Difficulty scaling:
        d1-3: both particles at rest (p=0), simple mass addition.
        d4-6: one particle moving.
        d7-8: both particles moving with different momenta.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "invariant_mass_two_particle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["four_momentum"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute invariant mass from decay products"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two particle energies and momenta, compute invariant mass.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c_sq = _C ** 2
        # Particle masses in electron mass units
        m1_kg = self._rng.randint(1, 5) * _ME
        m2_kg = self._rng.randint(1, 5) * _ME
        if difficulty <= 3:
            # Both at rest
            e1 = m1_kg * c_sq
            e2 = m2_kg * c_sq
            p1, p2 = 0.0, 0.0
        elif difficulty <= 6:
            sampler = VelocitySampler(self._rng)
            beta1 = sampler.sample_beta(3)
            gamma1 = _compute_gamma(beta1)
            e1 = gamma1 * m1_kg * c_sq
            p1 = gamma1 * m1_kg * beta1 * _C
            e2 = m2_kg * c_sq
            p2 = 0.0
        else:
            sampler = VelocitySampler(self._rng)
            beta1 = sampler.sample_beta(difficulty)
            beta2 = sampler.sample_beta(difficulty)
            gamma1 = _compute_gamma(beta1)
            gamma2 = _compute_gamma(beta2)
            e1 = gamma1 * m1_kg * c_sq
            p1 = gamma1 * m1_kg * beta1 * _C
            e2 = gamma2 * m2_kg * c_sq
            # Opposite direction
            p2 = -gamma2 * m2_kg * beta2 * _C
        e_total = e1 + e2
        p_total = p1 + p2
        m_sq_c4 = e_total ** 2 - (p_total * _C) ** 2
        # Protect against floating point issues
        if m_sq_c4 < 0:
            m_sq_c4 = abs(m_sq_c4)
        m_inv = math.sqrt(m_sq_c4) / c_sq
        return (
            f"E1={RelativityFormatter.format_sci(e1)} J, "
            f"E2={RelativityFormatter.format_sci(e2)} J, "
            f"p1={RelativityFormatter.format_sci(p1)}, "
            f"p2={RelativityFormatter.format_sci(p2)} kg m/s",
            {
                "e1": e1, "e2": e2, "p1": p1, "p2": p2,
                "e_total": e_total, "p_total": p_total,
                "m_sq_c4": m_sq_c4, "m_inv": m_inv,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate invariant mass computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing energy sum, momentum sum, and invariant mass.
        """
        e_tot_str = RelativityFormatter.format_sci(sd["e_total"])
        p_tot_str = RelativityFormatter.format_sci(sd["p_total"])
        m_str = RelativityFormatter.format_sci(sd["m_inv"])
        return [
            f"E_total = E1 + E2 = {e_tot_str} J",
            f"p_total = p1 + p2 = {p_tot_str} kg m/s",
            f"M^2 c^4 = E_total^2 - (p_total c)^2",
            f"M = {m_str} kg",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the invariant mass.

        Args:
            sd: Solution data dict.

        Returns:
            Invariant mass in scientific notation.
        """
        return f"M = {RelativityFormatter.format_sci(sd['m_inv'])} kg"


# ---------------------------------------------------------------------------
# 8. Photon Momentum (tier 5)
# ---------------------------------------------------------------------------

@register
class PhotonMomentumGenerator(StepGenerator):
    """Compute photon momentum from wavelength: p = h / lambda.

    Also computes energy E = hc / lambda and verifies p = E / c.

    Difficulty scaling:
        d1-3: radio/microwave wavelengths (1e-3 to 1 m).
        d4-6: visible/UV wavelengths (1e-7 to 1e-6 m).
        d7-8: X-ray/gamma wavelengths (1e-12 to 1e-10 m).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "photon_momentum"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute photon momentum from wavelength"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a wavelength and compute photon momentum and energy.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            exp = self._rng.randint(-3, 0)
        elif difficulty <= 6:
            exp = self._rng.randint(-7, -6)
        else:
            exp = self._rng.randint(-12, -10)
        mantissa = self._rng.randint(1, 9)
        wavelength = float(mantissa) * (10 ** exp)
        momentum = _H / wavelength
        energy = _H * _C / wavelength
        p_check = energy / _C
        return (
            f"photon wavelength = {RelativityFormatter.format_sci(wavelength)} m",
            {
                "wavelength": wavelength,
                "momentum": momentum,
                "energy": energy,
                "p_check": p_check,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate photon momentum computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing h/lambda and E/c computations.
        """
        wl_str = RelativityFormatter.format_sci(sd["wavelength"])
        p_str = RelativityFormatter.format_sci(sd["momentum"])
        e_str = RelativityFormatter.format_sci(sd["energy"])
        return [
            f"p = h/lambda = 6.626e-34 / {wl_str}",
            f"p = {p_str} kg m/s",
            f"E = hc/lambda = {e_str} J",
            f"verify: E/c = {p_str} kg m/s",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the photon momentum.

        Args:
            sd: Solution data dict.

        Returns:
            Momentum in scientific notation.
        """
        return f"p = {RelativityFormatter.format_sci(sd['momentum'])} kg m/s"
