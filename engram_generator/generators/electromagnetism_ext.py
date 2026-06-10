"""Electromagnetism extension generators -- dipoles through LC oscillations.

Deepens the existing electromagnetism domain with electric dipoles,
capacitor energy, magnetic field of wires/solenoids, Ampere's law,
Lenz's law, displacement current, Poynting vector, and LC oscillations.
Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.physics import ScientificFormatter

_fmt = ScientificFormatter.format_sci
_fval = ScientificFormatter.format_value

# Physical constants
_K = 8.99e9             # Coulomb constant (N m^2/C^2)
_EPSILON_0 = 8.854e-12  # vacuum permittivity (F/m)
_MU_0 = 4 * math.pi * 1e-7  # vacuum permeability (H/m)


# ===================================================================
# 1. Electric dipole (tier 5)
# ===================================================================

@register
class ElectricDipoleGenerator(StepGenerator):
    """Compute electric dipole moment, field, and potential.

    p = q*d. Field on axis: E = 2kp/r^3. On perpendicular bisector:
    E = kp/r^3. Potential V = kp*cos(theta)/r^2.

    Difficulty scaling:
        Difficulty 1-3: compute p and axial field only.
        Difficulty 4-6: compute axial and bisector fields.
        Difficulty 7-8: compute all including potential at angle.

    Prerequisites:
        electric_field.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electric_dipole"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["electric_field"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute electric dipole field and potential"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate dipole parameters and compute field/potential.

        Args:
            difficulty: Controls what quantities to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        q_nC = self._rng.randint(1, 5 + difficulty * 2)
        d_cm = round(self._rng.uniform(0.5, 5.0), 1)
        r = round(self._rng.uniform(0.1, 2.0 + difficulty * 0.5), 2)

        q = q_nC * 1e-9  # C
        d = d_cm * 1e-2  # m
        p = q * d  # dipole moment

        e_axis = round(2 * _K * p / r ** 3, 4)
        e_bisect = round(_K * p / r ** 3, 4)

        if difficulty >= 7:
            theta_deg = self._rng.choice([30, 45, 60])
        else:
            theta_deg = 0

        cos_theta = round(math.cos(math.radians(theta_deg)), 4)
        v_pot = round(_K * p * cos_theta / r ** 2, 4)

        return "p = qd, E_{axis} = 2kp/r^3", {
            "q_nC": q_nC, "d_cm": d_cm, "r": r,
            "q": q, "d": d, "p": p,
            "E_axis": e_axis, "E_bisect": e_bisect,
            "theta_deg": theta_deg, "cos_theta": cos_theta,
            "V": v_pot, "full": difficulty >= 4,
            "with_potential": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate electric dipole computation steps.

        Args:
            data: Solution data with q, d, r, fields, potential.

        Returns:
            List of step strings.
        """
        steps = [
            f"q={data['q_nC']}nC, d={data['d_cm']}cm, r={data['r']}m",
            f"p = qd = {_fmt(data['p'])} C*m",
            f"E_axis = 2kp/r^3 = {_fval(data['E_axis'])} N/C",
        ]
        if data["full"]:
            steps.append(
                f"E_bisect = kp/r^3 = {_fval(data['E_bisect'])} N/C"
            )
        if data["with_potential"]:
            steps.append(
                f"V = kp*cos({data['theta_deg']})/r^2"
                f" = {_fval(data['V'])} V"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the dipole results.

        Args:
            data: Solution data.

        Returns:
            Dipole moment and field as a string.
        """
        parts = [f"p={_fmt(data['p'])}C*m", f"E_axis={_fval(data['E_axis'])}N/C"]
        if data["full"]:
            parts.append(f"E_bisect={_fval(data['E_bisect'])}N/C")
        return ", ".join(parts)


# ===================================================================
# 2. Capacitor energy (tier 4)
# ===================================================================

@register
class CapacitorEnergyGenerator(StepGenerator):
    """Compute energy stored in a capacitor.

    U = (1/2)*C*V^2 = Q^2/(2C) = QV/2. Given two of C, V, Q,
    compute the energy using the appropriate formula.

    Difficulty scaling:
        Difficulty 1-3: C in [1,10] uF, V in [5,50] V.
        Difficulty 4-6: C in [1,100] uF, V in [5,200] V.
        Difficulty 7-8: C in [1,1000] uF, V in [5,500] V.

    Prerequisites:
        capacitance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "capacitor_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["capacitance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute energy stored in a capacitor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate capacitor parameters and compute stored energy.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            c_uF = self._rng.randint(1, 10)
            v = self._rng.randint(5, 50)
        elif difficulty <= 6:
            c_uF = self._rng.randint(1, 100)
            v = self._rng.randint(5, 200)
        else:
            c_uF = self._rng.randint(1, 1000)
            v = self._rng.randint(5, 500)

        c = c_uF * 1e-6
        q = round(c * v, 4)
        energy = round(0.5 * c * v ** 2, 4)

        given = self._rng.choice(["CV", "QC", "QV"])
        return "U = \\frac{1}{2}CV^2", {
            "C_uF": c_uF, "C": c, "V": v, "Q": q,
            "U": energy, "given": given,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate capacitor energy computation steps.

        Args:
            data: Solution data with C, V, Q, and U.

        Returns:
            List of step strings.
        """
        given = data["given"]
        if given == "CV":
            return [
                f"C={data['C_uF']}uF, V={data['V']}V",
                f"U = (1/2)*{data['C_uF']}e-6*{data['V']}^2",
            ]
        if given == "QC":
            return [
                f"Q={_fmt(data['Q'])}C, C={data['C_uF']}uF",
                f"U = Q^2/(2C) = ({_fmt(data['Q'])})^2/(2*{data['C_uF']}e-6)",
            ]
        return [
            f"Q={_fmt(data['Q'])}C, V={data['V']}V",
            f"U = QV/2 = {_fmt(data['Q'])}*{data['V']}/2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the stored energy.

        Args:
            data: Solution data.

        Returns:
            U as a string with units.
        """
        return f"U = {_fmt(data['U'])} J"


# ===================================================================
# 3. Magnetic field of wire (tier 5)
# ===================================================================

@register
class MagneticFieldWireGenerator(StepGenerator):
    """Compute magnetic field from infinite wire or solenoid.

    Infinite wire: B = mu_0*I/(2*pi*r).
    Solenoid: B = mu_0*n*I where n = N/L.

    Difficulty scaling:
        Difficulty 1-3: infinite wire, I in [1,10] A.
        Difficulty 4-6: infinite wire, I in [1,50] A.
        Difficulty 7-8: solenoid with N turns and length L.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnetic_field_wire"

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
        return "compute magnetic field from wire or solenoid"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate magnetic field parameters.

        Args:
            difficulty: Controls problem type and ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 6:
            # Infinite wire
            i_val = self._rng.randint(1, 10 + difficulty * 7)
            r_cm = round(self._rng.uniform(1.0, 20.0), 1)
            r = r_cm * 1e-2
            b = round(_MU_0 * i_val / (2 * math.pi * r), 4)
            return "B = \\mu_0 I/(2\\pi r)", {
                "mode": "wire", "I": i_val, "r_cm": r_cm,
                "r": r, "B": b,
            }

        # Solenoid
        i_val = self._rng.randint(1, 20)
        n_turns = self._rng.randint(100, 2000)
        length_cm = self._rng.randint(10, 100)
        length = length_cm * 1e-2
        n_density = n_turns / length
        b = round(_MU_0 * n_density * i_val, 4)
        return "B = \\mu_0 n I", {
            "mode": "solenoid", "I": i_val,
            "N": n_turns, "L_cm": length_cm, "L": length,
            "n": round(n_density, 4), "B": b,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate magnetic field computation steps.

        Args:
            data: Solution data with mode and parameters.

        Returns:
            List of step strings.
        """
        if data["mode"] == "wire":
            return [
                f"I={data['I']}A, r={data['r_cm']}cm",
                f"B = mu_0*{data['I']}/(2pi*{data['r_cm']}e-2)",
            ]
        return [
            f"I={data['I']}A, N={data['N']}, L={data['L_cm']}cm",
            f"n = N/L = {data['N']}/{data['L_cm']}e-2"
            f" = {_fval(data['n'])} turns/m",
            f"B = mu_0*{_fval(data['n'])}*{data['I']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the magnetic field.

        Args:
            data: Solution data.

        Returns:
            B as a string with units.
        """
        return f"B = {_fmt(data['B'])} T"


# ===================================================================
# 4. Ampere's law (tier 5)
# ===================================================================

@register
class AmpereLawGenerator(StepGenerator):
    """Apply Ampere's law to wire, solenoid, and toroid.

    Integral B.dl = mu_0*I_enc. For a toroid B = mu_0*N*I/(2*pi*r).

    Difficulty scaling:
        Difficulty 1-3: single wire (B from Ampere's law).
        Difficulty 4-6: solenoid of N turns.
        Difficulty 7-8: toroid with inner/outer radius.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ampere_law"

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
        return "apply Ampere's law to compute magnetic field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Ampere's law problem parameters.

        Args:
            difficulty: Controls geometry selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._wire_problem(difficulty)
        if difficulty <= 6:
            return self._solenoid_problem(difficulty)
        return self._toroid_problem(difficulty)

    def _wire_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ampere's law wire problem.

        Args:
            difficulty: Controls current magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        i_val = self._rng.randint(1, 10 + difficulty * 3)
        r_cm = round(self._rng.uniform(1.0, 10.0), 1)
        r = r_cm * 1e-2
        b = round(_MU_0 * i_val / (2 * math.pi * r), 4)
        return "\\oint B \\cdot dl = \\mu_0 I_{enc}", {
            "geometry": "wire", "I": i_val,
            "r_cm": r_cm, "r": r, "B": b,
        }

    def _solenoid_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ampere's law solenoid problem.

        Args:
            difficulty: Controls turn count and current.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_per_m = self._rng.randint(100, 500 + difficulty * 100)
        i_val = self._rng.randint(1, 10 + difficulty * 3)
        b = round(_MU_0 * n_per_m * i_val, 4)
        return "B = \\mu_0 n I", {
            "geometry": "solenoid", "n": n_per_m,
            "I": i_val, "B": b,
        }

    def _toroid_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ampere's law toroid problem.

        Args:
            difficulty: Controls turns and radius.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_turns = self._rng.randint(200, 2000)
        i_val = self._rng.randint(1, 15)
        r_cm = round(self._rng.uniform(5.0, 30.0), 1)
        r = r_cm * 1e-2
        b = round(_MU_0 * n_turns * i_val / (2 * math.pi * r), 4)
        return "B = \\mu_0 NI/(2\\pi r)", {
            "geometry": "toroid", "N": n_turns,
            "I": i_val, "r_cm": r_cm, "r": r, "B": b,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ampere's law computation steps.

        Args:
            data: Solution data with geometry and parameters.

        Returns:
            List of step strings.
        """
        geom = data["geometry"]
        if geom == "wire":
            return [
                f"I={data['I']}A, r={data['r_cm']}cm",
                f"B = mu_0*I/(2pi*r)",
            ]
        if geom == "solenoid":
            return [
                f"n={data['n']} turns/m, I={data['I']}A",
                f"B = mu_0*n*I",
            ]
        return [
            f"N={data['N']}, I={data['I']}A, r={data['r_cm']}cm",
            f"B = mu_0*N*I/(2pi*r)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the magnetic field from Ampere's law.

        Args:
            data: Solution data.

        Returns:
            B as a string with units.
        """
        return f"B = {_fmt(data['B'])} T"


# ===================================================================
# 5. Lenz's law (tier 5)
# ===================================================================

@register
class LenzLawGenerator(StepGenerator):
    """Determine direction of induced current via Lenz's law.

    Induced current opposes the change in magnetic flux. Given B
    increasing/decreasing and loop orientation, determine whether
    the induced current is clockwise or counterclockwise.

    Difficulty scaling:
        Difficulty 1-3: B increasing through loop, perpendicular.
        Difficulty 4-6: B increasing or decreasing, two orientations.
        Difficulty 7-8: additional external field direction combinations.

    Prerequisites:
        multiplication.
    """

    _B_CHANGES = ["increasing", "decreasing"]
    _ORIENTATIONS = ["into_page", "out_of_page"]
    _DIRECTION_MAP = {
        ("increasing", "into_page"): "counterclockwise",
        ("increasing", "out_of_page"): "clockwise",
        ("decreasing", "into_page"): "clockwise",
        ("decreasing", "out_of_page"): "counterclockwise",
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lenz_law"

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
        return "determine induced current direction using Lenz's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Lenz's law problem parameters.

        Args:
            difficulty: Controls scenario complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        b_change = self._rng.choice(self._B_CHANGES)
        orientation = self._rng.choice(self._ORIENTATIONS)
        direction = self._DIRECTION_MAP[(b_change, orientation)]

        b_initial = round(self._rng.uniform(0.1, 2.0), 2)
        if b_change == "increasing":
            b_final = round(b_initial + self._rng.uniform(0.5, 3.0), 2)
        else:
            b_final = round(max(0.01, b_initial - self._rng.uniform(0.5, b_initial * 0.9)), 2)

        dt = round(self._rng.uniform(0.01, 1.0), 2)

        return "\\text{Lenz: opposes change in } \\Phi_B", {
            "b_change": b_change, "orientation": orientation,
            "direction": direction,
            "B_i": b_initial, "B_f": b_final, "dt": dt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lenz's law reasoning steps.

        Args:
            data: Solution data with B change and orientation.

        Returns:
            List of step strings.
        """
        orient_str = data["orientation"].replace("_", " ")
        return [
            f"B is {data['b_change']}: "
            f"{data['B_i']}T -> {data['B_f']}T in {data['dt']}s",
            f"B direction: {orient_str}",
            f"flux {data['b_change']} => induced B opposes change",
            f"induced current: {data['direction']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the induced current direction.

        Args:
            data: Solution data.

        Returns:
            Direction as a string.
        """
        return f"I_induced = {data['direction']}"


# ===================================================================
# 6. Displacement current (tier 6)
# ===================================================================

@register
class DisplacementCurrentGenerator(StepGenerator):
    """Compute displacement current for a parallel plate capacitor.

    I_d = epsilon_0 * dPhi_E/dt. For a capacitor being charged,
    dPhi_E/dt = (1/epsilon_0) * dQ/dt * (1/A) * A = I_charge/1.
    Equivalently I_d = epsilon_0 * A * dE/dt.

    Difficulty scaling:
        Difficulty 1-3: given dE/dt directly, A in [1,10] cm^2.
        Difficulty 4-6: compute dE/dt from dV/dt and plate separation.
        Difficulty 7-8: given charging current, verify I_d = I_charge.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "displacement_current"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute displacement current in charging capacitor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate displacement current problem parameters.

        Args:
            difficulty: Controls problem formulation.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_cm2 = self._rng.randint(1, 10 + difficulty * 5)
        a = a_cm2 * 1e-4  # m^2

        if difficulty <= 3:
            de_dt = float(self._rng.randint(1000, 10000 + difficulty * 5000))
            i_d = round(_EPSILON_0 * a * de_dt, 4)
            return "I_d = \\varepsilon_0 A \\frac{dE}{dt}", {
                "mode": "direct", "a_cm2": a_cm2, "A": a,
                "dE_dt": de_dt, "I_d": i_d,
            }

        if difficulty <= 6:
            d_mm = round(self._rng.uniform(0.5, 5.0), 1)
            d = d_mm * 1e-3
            dv_dt = float(self._rng.randint(10, 100 + difficulty * 50))
            de_dt = round(dv_dt / d, 4)
            i_d = round(_EPSILON_0 * a * de_dt, 4)
            return "I_d = \\varepsilon_0 A \\frac{dE}{dt}", {
                "mode": "from_voltage", "a_cm2": a_cm2, "A": a,
                "d_mm": d_mm, "d": d, "dV_dt": dv_dt,
                "dE_dt": de_dt, "I_d": i_d,
            }

        # From charging current
        i_charge = round(self._rng.uniform(0.001, 1.0), 4)
        i_d = i_charge
        de_dt = round(i_charge / (_EPSILON_0 * a), 4)
        return "I_d = \\varepsilon_0 \\frac{d\\Phi_E}{dt} = I_{charge}", {
            "mode": "charging", "a_cm2": a_cm2, "A": a,
            "I_charge": i_charge, "dE_dt": de_dt, "I_d": i_d,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate displacement current computation steps.

        Args:
            data: Solution data with mode and parameters.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "direct":
            return [
                f"A={data['a_cm2']}cm^2={_fmt(data['A'])}m^2",
                f"dE/dt={_fval(data['dE_dt'])} V/(m*s)",
                f"I_d = eps_0 * A * dE/dt",
            ]
        if mode == "from_voltage":
            return [
                f"A={data['a_cm2']}cm^2, d={data['d_mm']}mm",
                f"dV/dt={data['dV_dt']} V/s",
                f"dE/dt = dV/dt / d = {_fval(data['dE_dt'])} V/(m*s)",
                f"I_d = eps_0 * A * dE/dt",
            ]
        return [
            f"A={data['a_cm2']}cm^2",
            f"I_charge={data['I_charge']}A",
            f"I_d = I_charge (Maxwell's correction)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the displacement current.

        Args:
            data: Solution data.

        Returns:
            I_d as a string with units.
        """
        return f"I_d = {_fmt(data['I_d'])} A"


# ===================================================================
# 7. Poynting vector (tier 6)
# ===================================================================

@register
class PoyntingVectorGenerator(StepGenerator):
    """Compute Poynting vector and intensity for EM wave.

    S = (1/mu_0)*E x B. Average intensity I = E_0*B_0/(2*mu_0)
    = E_0^2/(2*mu_0*c).

    Difficulty scaling:
        Difficulty 1-3: given E_0, compute B_0 and intensity.
        Difficulty 4-6: given intensity, compute E_0.
        Difficulty 7-8: given power and area, compute E_0 and B_0.

    Prerequisites:
        multiplication.
    """

    _C = 3e8  # speed of light

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "poynting_vector"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute Poynting vector and EM wave intensity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Poynting vector problem parameters.

        Args:
            difficulty: Controls problem direction.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            e0 = self._rng.randint(100, 5000)
            b0 = round(e0 / self._C, 4)
            intensity = round(e0 * b0 / (2 * _MU_0), 4)
            return "S = \\frac{1}{\\mu_0}E \\times B", {
                "mode": "from_E", "E0": e0, "B0": b0,
                "intensity": intensity,
            }

        if difficulty <= 6:
            intensity = float(self._rng.randint(100, 10000))
            e0 = round(math.sqrt(2 * _MU_0 * self._C * intensity), 4)
            b0 = round(e0 / self._C, 4)
            return "I = E_0^2/(2\\mu_0 c)", {
                "mode": "from_I", "E0": e0, "B0": b0,
                "intensity": intensity,
            }

        power = float(self._rng.randint(10, 1000))
        area_cm2 = self._rng.randint(1, 50)
        area = area_cm2 * 1e-4
        intensity = round(power / area, 4)
        e0 = round(math.sqrt(2 * _MU_0 * self._C * intensity), 4)
        b0 = round(e0 / self._C, 4)
        return "I = P/A = E_0 B_0/(2\\mu_0)", {
            "mode": "from_P", "P": power, "A_cm2": area_cm2,
            "A": area, "E0": e0, "B0": b0,
            "intensity": intensity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poynting vector computation steps.

        Args:
            data: Solution data with mode and field values.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "from_E":
            return [
                f"E_0={data['E0']} V/m",
                f"B_0 = E_0/c = {_fmt(data['B0'])} T",
                f"I = E_0*B_0/(2*mu_0)",
            ]
        if mode == "from_I":
            return [
                f"I={_fval(data['intensity'])} W/m^2",
                f"E_0 = sqrt(2*mu_0*c*I) = {_fval(data['E0'])} V/m",
                f"B_0 = E_0/c = {_fmt(data['B0'])} T",
            ]
        return [
            f"P={data['P']}W, A={data['A_cm2']}cm^2",
            f"I = P/A = {_fval(data['intensity'])} W/m^2",
            f"E_0 = sqrt(2*mu_0*c*I) = {_fval(data['E0'])} V/m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the intensity and field amplitudes.

        Args:
            data: Solution data.

        Returns:
            I and E_0 as a string.
        """
        return (
            f"I={_fval(data['intensity'])}W/m^2, "
            f"E_0={_fval(data['E0'])}V/m"
        )


# ===================================================================
# 8. LC oscillation (tier 5)
# ===================================================================

@register
class LCOscillationGenerator(StepGenerator):
    """Compute LC circuit oscillation parameters.

    omega = 1/sqrt(LC). Q(t) = Q_0*cos(omega*t).
    I(t) = -Q_0*omega*sin(omega*t). Energy oscillates between
    capacitor (U_C = Q^2/(2C)) and inductor (U_L = LI^2/2).

    Difficulty scaling:
        Difficulty 1-3: compute omega and period only.
        Difficulty 4-6: compute Q(t) and I(t) at a given time.
        Difficulty 7-8: compute energy partition at a given time.

    Prerequisites:
        capacitance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lc_oscillation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["capacitance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute LC oscillation frequency and charge/current"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate LC oscillation parameters and compute results.

        Args:
            difficulty: Controls what quantities to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        l_mH = self._rng.randint(1, 50 + difficulty * 20)
        c_uF = self._rng.randint(1, 50 + difficulty * 20)
        l_val = l_mH * 1e-3
        c_val = c_uF * 1e-6

        omega = round(1.0 / math.sqrt(l_val * c_val), 4)
        period = round(2 * math.pi / omega, 4)

        q0_uC = self._rng.randint(1, 10 + difficulty * 5)
        q0 = q0_uC * 1e-6

        if difficulty <= 3:
            return "\\omega = 1/\\sqrt{LC}", {
                "L_mH": l_mH, "C_uF": c_uF,
                "L": l_val, "C": c_val,
                "omega": omega, "T": period,
                "Q0_uC": q0_uC, "Q0": q0,
                "mode": "freq",
            }

        t_mult = round(self._rng.uniform(0.1, 2.0), 2)
        t = round(t_mult * period, 4)
        q_t = round(q0 * math.cos(omega * t), 4)
        i_t = round(-q0 * omega * math.sin(omega * t), 4)

        if difficulty <= 6:
            return "Q(t) = Q_0 \\cos(\\omega t)", {
                "L_mH": l_mH, "C_uF": c_uF,
                "L": l_val, "C": c_val,
                "omega": omega, "T": period,
                "Q0_uC": q0_uC, "Q0": q0,
                "t": t, "Q_t": q_t, "I_t": i_t,
                "mode": "time",
            }

        u_c = round(q_t ** 2 / (2 * c_val), 4)
        u_l = round(l_val * i_t ** 2 / 2, 4)
        u_total = round(q0 ** 2 / (2 * c_val), 4)
        return "U_C + U_L = Q_0^2/(2C)", {
            "L_mH": l_mH, "C_uF": c_uF,
            "L": l_val, "C": c_val,
            "omega": omega, "T": period,
            "Q0_uC": q0_uC, "Q0": q0,
            "t": t, "Q_t": q_t, "I_t": i_t,
            "U_C": u_c, "U_L": u_l, "U_total": u_total,
            "mode": "energy",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate LC oscillation computation steps.

        Args:
            data: Solution data with L, C, omega, and mode.

        Returns:
            List of step strings.
        """
        steps = [
            f"L={data['L_mH']}mH, C={data['C_uF']}uF",
            f"omega = 1/sqrt(LC) = {_fval(data['omega'])} rad/s",
            f"T = 2pi/omega = {_fval(data['T'])} s",
        ]
        if data["mode"] == "freq":
            return steps
        steps.append(
            f"Q0={data['Q0_uC']}uC, t={_fval(data['t'])}s"
        )
        steps.append(
            f"Q(t) = {_fmt(data['Q_t'])} C"
        )
        if data["mode"] == "energy":
            steps.append(
                f"U_C={_fmt(data['U_C'])}J, U_L={_fmt(data['U_L'])}J"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the LC oscillation result.

        Args:
            data: Solution data.

        Returns:
            Result appropriate to the mode.
        """
        if data["mode"] == "freq":
            return (
                f"omega={_fval(data['omega'])}rad/s, "
                f"T={_fval(data['T'])}s"
            )
        if data["mode"] == "time":
            return (
                f"Q(t)={_fmt(data['Q_t'])}C, "
                f"I(t)={_fmt(data['I_t'])}A"
            )
        return (
            f"U_C={_fmt(data['U_C'])}J, "
            f"U_L={_fmt(data['U_L'])}J, "
            f"U_total={_fmt(data['U_total'])}J"
        )
