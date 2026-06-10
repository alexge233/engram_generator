"""Deep electromagnetic theory generators -- plates, Gauss, networks, transients.

Extends the electromagnetism domain with parallel plate fields, Gauss's
law for spheres, capacitor networks, RC/RL transients, Wheatstone bridge,
Biot-Savart, mutual inductance, skin depth, and waveguide cutoff.
Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.physics import ScientificFormatter

_fmt = ScientificFormatter.format_sci
_fval = ScientificFormatter.format_value

# Physical constants
_EPSILON_0 = 8.854e-12       # vacuum permittivity (F/m)
_MU_0 = 4 * math.pi * 1e-7  # vacuum permeability (H/m)
_C = 3e8                     # speed of light (m/s)

# Conductivities (S/m) for skin depth problems
_SIGMA_COPPER = 5.96e7
_SIGMA_ALUMINUM = 3.77e7


# ===================================================================
# 1. Parallel plate field  (tier 4)
# ===================================================================

@register
class ParallelPlateFieldGenerator(StepGenerator):
    """Compute electric field between parallel plates.

    E = sigma / epsilon_0 = V / d. Given plate voltage and separation,
    compute the field and the force on a test charge placed between
    the plates.

    Difficulty scaling:
        Difficulty 1-3: compute E = V/d only with integer values.
        Difficulty 4-6: compute E and force F = qE with decimal charge.
        Difficulty 7-8: given sigma, compute E and then V for given d.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parallel_plate_field"

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
        return "compute electric field between parallel plates"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate plate parameters and compute field.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            v = self._rng.randint(10, 500)
            d_mm = self._rng.randint(1, 10)
            d = d_mm * 1e-3
            e_field = round(v / d, 4)
            return "E = V/d", {
                "V": v, "d_mm": d_mm, "d": d,
                "E": e_field, "mode": "simple",
            }
        if difficulty <= 6:
            v = self._rng.randint(50, 1000)
            d_mm = self._rng.randint(1, 10)
            d = d_mm * 1e-3
            q_uC = round(self._rng.uniform(0.1, 5.0), 1)
            q = q_uC * 1e-6
            e_field = round(v / d, 4)
            force = round(q * e_field, 4)
            return "E = V/d, F = qE", {
                "V": v, "d_mm": d_mm, "d": d,
                "q_uC": q_uC, "q": q,
                "E": e_field, "F": force, "mode": "force",
            }
        # From surface charge density
        sigma_nCm2 = self._rng.randint(1, 50)
        sigma = sigma_nCm2 * 1e-9
        d_mm = self._rng.randint(1, 10)
        d = d_mm * 1e-3
        e_field = round(sigma / _EPSILON_0, 4)
        voltage = round(e_field * d, 4)
        return "E = sigma/epsilon_0", {
            "sigma_nCm2": sigma_nCm2, "sigma": sigma,
            "d_mm": d_mm, "d": d,
            "E": e_field, "V": voltage, "mode": "sigma",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "simple":
            return [
                f"V={data['V']}V, d={data['d_mm']}mm={_fval(data['d'])}m",
                f"E = {data['V']}/{_fval(data['d'])}",
            ]
        if data["mode"] == "force":
            return [
                f"V={data['V']}V, d={data['d_mm']}mm",
                f"E = V/d = {_fval(data['E'])} V/m",
                f"F = qE = {data['q_uC']}e-6 * {_fval(data['E'])}",
            ]
        return [
            f"sigma={data['sigma_nCm2']} nC/m^2",
            f"E = sigma/eps_0 = {_fval(data['E'])} V/m",
            f"V = E*d = {_fval(data['E'])}*{_fval(data['d'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed field or voltage.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "force":
            return f"E = {_fval(data['E'])} V/m, F = {_fmt(data['F'])} N"
        if data["mode"] == "sigma":
            return f"E = {_fval(data['E'])} V/m, V = {_fval(data['V'])} V"
        return f"E = {_fval(data['E'])} V/m"


# ===================================================================
# 2. Gauss sphere  (tier 5)
# ===================================================================

@register
class GaussSphereGenerator(StepGenerator):
    """Apply Gauss's law for point charges and uniform spheres.

    E * 4 * pi * r^2 = Q_enc / epsilon_0. For a point charge,
    Q_enc = Q always. For a uniform sphere of radius R, Q_enc depends
    on whether r < R (inside) or r > R (outside).

    Difficulty scaling:
        Difficulty 1-3: point charge, compute E at distance r.
        Difficulty 4-6: uniform sphere, compute E outside (r > R).
        Difficulty 7-8: uniform sphere, compute E inside (r < R).

    Prerequisites:
        electric_field.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gauss_sphere"

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
        return "apply Gauss's law for spherical symmetry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Gauss sphere problem parameters.

        Args:
            difficulty: Controls geometry variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            q_uC = self._rng.randint(1, 10)
            r = round(self._rng.uniform(0.1, 2.0), 2)
            q = q_uC * 1e-6
            e_field = round(q / (4 * math.pi * _EPSILON_0 * r ** 2), 4)
            return "E = Q/(4pi*eps_0*r^2)", {
                "q_uC": q_uC, "r": r, "E": e_field, "mode": "point",
            }
        # Uniform sphere
        q_uC = self._rng.randint(1, 20)
        q = q_uC * 1e-6
        r_sphere = round(self._rng.uniform(0.05, 0.5), 2)
        if difficulty <= 6:
            r = round(self._rng.uniform(r_sphere + 0.01, 2.0), 2)
            e_field = round(q / (4 * math.pi * _EPSILON_0 * r ** 2), 4)
            return "E = Q/(4pi*eps_0*r^2) for r>R", {
                "q_uC": q_uC, "R": r_sphere, "r": r,
                "E": e_field, "mode": "outside",
            }
        r = round(self._rng.uniform(0.01, r_sphere - 0.005), 2)
        q_enc = q * (r / r_sphere) ** 3
        e_field = round(q_enc / (4 * math.pi * _EPSILON_0 * r ** 2), 4)
        return "E = Q*r/(4pi*eps_0*R^3) for r<R", {
            "q_uC": q_uC, "R": r_sphere, "r": r,
            "q_enc": round(q_enc, 4),
            "E": e_field, "mode": "inside",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gauss sphere computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "point":
            return [
                f"Q={data['q_uC']}uC, r={data['r']}m",
                f"E = Q/(4pi*eps_0*r^2)",
            ]
        if data["mode"] == "outside":
            return [
                f"Q={data['q_uC']}uC, R={data['R']}m, r={data['r']}m (r>R)",
                f"Q_enc = Q = {data['q_uC']}uC",
                f"E = Q/(4pi*eps_0*r^2)",
            ]
        return [
            f"Q={data['q_uC']}uC, R={data['R']}m, r={data['r']}m (r<R)",
            f"Q_enc = Q*(r/R)^3 = {_fmt(data['q_enc'])} C",
            f"E = Q_enc/(4pi*eps_0*r^2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the electric field.

        Args:
            data: Solution data.

        Returns:
            E as a string with units.
        """
        return f"E = {_fval(data['E'])} N/C"


# ===================================================================
# 3. Capacitor network  (tier 5)
# ===================================================================

@register
class CapacitorNetworkGenerator(StepGenerator):
    """Reduce a complex series-parallel capacitor network step by step.

    Generates networks of 3-5 capacitors in mixed series-parallel
    configurations and reduces them to a single equivalent capacitance.

    Difficulty scaling:
        Difficulty 1-3: 3 capacitors (2 parallel + 1 series).
        Difficulty 4-6: 4 capacitors (nested combinations).
        Difficulty 7-8: 5 capacitors with deep nesting.

    Prerequisites:
        capacitance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "capacitor_network"

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
        return "reduce capacitor network to equivalent capacitance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a capacitor network and reduce it.

        Args:
            difficulty: Controls network size.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._three_cap()
        if difficulty <= 6:
            return self._four_cap()
        return self._five_cap()

    def _three_cap(self) -> tuple[str, dict]:
        """Generate a 3-capacitor network: C1 || C2, then series with C3.

        Returns:
            Tuple of (formula, solution_data).
        """
        c1 = self._rng.randint(1, 20)
        c2 = self._rng.randint(1, 20)
        c3 = self._rng.randint(1, 20)
        c12 = c1 + c2  # parallel (uF)
        c_eq = round(1.0 / (1.0 / c12 + 1.0 / c3), 4)
        return "C1||C2 series C3", {
            "caps": [c1, c2, c3], "c12": c12,
            "C_eq": c_eq, "n": 3,
        }

    def _four_cap(self) -> tuple[str, dict]:
        """Generate a 4-capacitor network: (C1||C2) series (C3||C4).

        Returns:
            Tuple of (formula, solution_data).
        """
        c1 = self._rng.randint(1, 20)
        c2 = self._rng.randint(1, 20)
        c3 = self._rng.randint(1, 20)
        c4 = self._rng.randint(1, 20)
        c12 = c1 + c2
        c34 = c3 + c4
        c_eq = round(1.0 / (1.0 / c12 + 1.0 / c34), 4)
        return "(C1||C2) series (C3||C4)", {
            "caps": [c1, c2, c3, c4], "c12": c12, "c34": c34,
            "C_eq": c_eq, "n": 4,
        }

    def _five_cap(self) -> tuple[str, dict]:
        """Generate a 5-capacitor network: ((C1||C2) series C3) || (C4 series C5).

        Returns:
            Tuple of (formula, solution_data).
        """
        caps = [self._rng.randint(1, 20) for _ in range(5)]
        c12 = caps[0] + caps[1]
        c123 = 1.0 / (1.0 / c12 + 1.0 / caps[2])
        c45 = 1.0 / (1.0 / caps[3] + 1.0 / caps[4])
        c_eq = round(c123 + c45, 4)
        return "((C1||C2) ser C3) || (C4 ser C5)", {
            "caps": caps, "c12": c12,
            "c123": round(c123, 4), "c45": round(c45, 4),
            "C_eq": c_eq, "n": 5,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate network reduction steps.

        Args:
            data: Solution data with capacitor values.

        Returns:
            List of step strings.
        """
        caps = data["caps"]
        steps = [f"Capacitors (uF): {', '.join(str(c) for c in caps)}"]
        if data["n"] == 3:
            steps.append(f"C12 = {caps[0]}+{caps[1]} = {data['c12']} uF")
            steps.append(f"1/C = 1/{data['c12']}+1/{caps[2]}")
        elif data["n"] == 4:
            steps.append(f"C12 = {data['c12']} uF, C34 = {data['c34']} uF")
            steps.append(f"1/C = 1/{data['c12']}+1/{data['c34']}")
        else:
            steps.append(f"C12 = {data['c12']} uF")
            steps.append(f"C123 = {_fval(data['c123'])} uF")
            steps.append(f"C45 = {_fval(data['c45'])} uF")
            steps.append(f"C_eq = C123 + C45")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the equivalent capacitance.

        Args:
            data: Solution data.

        Returns:
            C_eq as a string with units.
        """
        return f"C_eq = {_fval(data['C_eq'])} uF"


# ===================================================================
# 4. RC time constant  (tier 5)
# ===================================================================

@register
class RCTimeConstantGenerator(StepGenerator):
    """Compute voltage across a capacitor during RC charging/discharging.

    Charging: V(t) = V_0 * (1 - e^(-t/RC)).
    Discharging: V(t) = V_0 * e^(-t/RC).
    Given R, C, V_0, and t, compute V(t).

    Difficulty scaling:
        Difficulty 1-3: charging, t given as multiple of tau.
        Difficulty 4-6: discharging, arbitrary t.
        Difficulty 7-8: find time t for V to reach given fraction.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rc_time_constant"

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
        return "compute RC transient voltage at given time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate RC parameters and compute V(t).

        Args:
            difficulty: Controls charging vs discharging.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_kohm = self._rng.randint(1, 10 + difficulty)
        c_uF = self._rng.randint(1, 10 + difficulty)
        r = r_kohm * 1e3
        c = c_uF * 1e-6
        tau = r * c
        v0 = self._rng.randint(5, 24)

        if difficulty <= 3:
            n_tau = self._rng.choice([1, 2, 3])
            t = round(n_tau * tau, 4)
            vt = round(v0 * (1 - math.exp(-n_tau)), 4)
            return "V(t) = V_0(1 - e^{-t/RC})", {
                "R_kohm": r_kohm, "C_uF": c_uF, "tau": round(tau, 4),
                "V0": v0, "t": t, "V_t": vt, "mode": "charge",
            }
        if difficulty <= 6:
            t = round(self._rng.uniform(0.5 * tau, 4 * tau), 4)
            vt = round(v0 * math.exp(-t / tau), 4)
            return "V(t) = V_0 e^{-t/RC}", {
                "R_kohm": r_kohm, "C_uF": c_uF, "tau": round(tau, 4),
                "V0": v0, "t": t, "V_t": vt, "mode": "discharge",
            }
        # Find time for V to reach fraction of V0
        frac = round(self._rng.uniform(0.1, 0.9), 2)
        t_needed = round(-tau * math.log(1 - frac), 4)
        return "t = -RC ln(1 - V/V_0)", {
            "R_kohm": r_kohm, "C_uF": c_uF, "tau": round(tau, 4),
            "V0": v0, "frac": frac, "t": t_needed, "mode": "find_t",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate RC transient steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"R={data['R_kohm']}kohm, C={data['C_uF']}uF",
            f"tau = RC = {_fval(data['tau'])} s",
        ]
        if data["mode"] == "charge":
            steps.append(f"V({_fval(data['t'])}) = {data['V0']}*(1-e^(-{_fval(data['t'])}/{_fval(data['tau'])}))")
        elif data["mode"] == "discharge":
            steps.append(f"V({_fval(data['t'])}) = {data['V0']}*e^(-{_fval(data['t'])}/{_fval(data['tau'])})")
        else:
            steps.append(f"target = {data['frac']}*{data['V0']}V")
            steps.append(f"t = -tau*ln(1-{data['frac']})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the voltage or time.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "find_t":
            return f"t = {_fval(data['t'])} s"
        return f"V(t) = {_fval(data['V_t'])} V"


# ===================================================================
# 5. RL circuit  (tier 5)
# ===================================================================

@register
class RLCircuitGenerator(StepGenerator):
    """Compute current in an RL circuit during transient response.

    I(t) = (V/R) * (1 - e^(-Rt/L)). Time constant tau = L/R.
    Given V, R, L, and t, compute I(t).

    Difficulty scaling:
        Difficulty 1-3: compute tau = L/R only.
        Difficulty 4-6: compute I(t) at given time.
        Difficulty 7-8: find time for I to reach given fraction of I_max.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rl_circuit"

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
        return "compute RL circuit transient current"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate RL circuit parameters and compute current.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r = self._rng.randint(10, 100 + difficulty * 20)
        l_mH = self._rng.randint(10, 100 + difficulty * 20)
        l_val = l_mH * 1e-3
        tau = round(l_val / r, 4)
        v = self._rng.randint(5, 24)
        i_max = round(v / r, 4)

        if difficulty <= 3:
            return "tau = L/R", {
                "R": r, "L_mH": l_mH, "tau": tau,
                "V": v, "I_max": i_max, "mode": "tau",
            }
        if difficulty <= 6:
            t = round(self._rng.uniform(0.5 * tau, 4 * tau), 4)
            i_t = round(i_max * (1 - math.exp(-t / tau)), 4)
            return "I(t) = (V/R)(1 - e^{-Rt/L})", {
                "R": r, "L_mH": l_mH, "tau": tau,
                "V": v, "I_max": i_max,
                "t": t, "I_t": i_t, "mode": "current",
            }
        frac = round(self._rng.uniform(0.1, 0.9), 2)
        t_needed = round(-tau * math.log(1 - frac), 4)
        return "t = -(L/R) ln(1 - I/I_max)", {
            "R": r, "L_mH": l_mH, "tau": tau,
            "V": v, "I_max": i_max,
            "frac": frac, "t": t_needed, "mode": "find_t",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate RL circuit computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"R={data['R']}ohm, L={data['L_mH']}mH",
            f"tau = L/R = {_fval(data['tau'])} s",
            f"I_max = V/R = {data['V']}/{data['R']} = {_fval(data['I_max'])} A",
        ]
        if data["mode"] == "current":
            steps.append(
                f"I({_fval(data['t'])}) = {_fval(data['I_max'])}*(1-e^(-{_fval(data['t'])}/{_fval(data['tau'])}))"
            )
        elif data["mode"] == "find_t":
            steps.append(f"target = {data['frac']}*I_max")
            steps.append(f"t = -tau*ln(1-{data['frac']})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the time constant, current, or time.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "tau":
            return f"tau = {_fval(data['tau'])} s"
        if data["mode"] == "find_t":
            return f"t = {_fval(data['t'])} s"
        return f"I(t) = {_fval(data['I_t'])} A"


# ===================================================================
# 6. Wheatstone bridge  (tier 5)
# ===================================================================

@register
class WheatsoneBridgeGenerator(StepGenerator):
    """Compute the unknown resistance in a balanced Wheatstone bridge.

    Balanced condition: R1/R2 = R3/R4. Given three resistances,
    find the fourth.

    Difficulty scaling:
        Difficulty 1-3: integer resistances, find R4.
        Difficulty 4-6: decimal resistances, find any one of R1-R4.
        Difficulty 7-8: given all four, determine if balanced and
            compute galvanometer current if not.

    Prerequisites:
        ohms_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wheatstone_bridge"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "find unknown resistance in Wheatstone bridge"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Wheatstone bridge parameters.

        Args:
            difficulty: Controls precision and target.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            r1 = self._rng.randint(10, 100)
            r2 = self._rng.randint(10, 100)
            r3 = self._rng.randint(10, 100)
            r4 = round(r2 * r3 / r1, 4)
            return "R1/R2 = R3/R4", {
                "R1": r1, "R2": r2, "R3": r3, "R4": r4,
                "target": "R4",
            }
        if difficulty <= 6:
            r1 = round(self._rng.uniform(10, 200), 1)
            r2 = round(self._rng.uniform(10, 200), 1)
            r3 = round(self._rng.uniform(10, 200), 1)
            target = self._rng.choice(["R1", "R2", "R3", "R4"])
            r4 = round(r2 * r3 / r1, 4)
            return "R1/R2 = R3/R4", {
                "R1": r1, "R2": r2, "R3": r3, "R4": r4,
                "target": target,
            }
        # Check balance
        r1 = self._rng.randint(10, 100)
        r2 = self._rng.randint(10, 100)
        r3 = self._rng.randint(10, 100)
        r4 = self._rng.randint(10, 100)
        ratio_left = round(r1 / r2, 4)
        ratio_right = round(r3 / r4, 4)
        balanced = abs(ratio_left - ratio_right) < 0.001
        r4_balanced = round(r2 * r3 / r1, 4)
        return "R1/R2 = R3/R4 ?", {
            "R1": r1, "R2": r2, "R3": r3, "R4": r4,
            "ratio_left": ratio_left, "ratio_right": ratio_right,
            "balanced": balanced, "R4_balanced": r4_balanced,
            "target": "check",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Wheatstone bridge computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["target"] == "check":
            return [
                f"R1={data['R1']}, R2={data['R2']}, R3={data['R3']}, R4={data['R4']}",
                f"R1/R2 = {_fval(data['ratio_left'])}",
                f"R3/R4 = {_fval(data['ratio_right'])}",
                f"Balanced: {data['balanced']}",
            ]
        return [
            f"R1={_fval(data['R1'])}, R2={_fval(data['R2'])}, R3={_fval(data['R3'])}",
            f"R1/R2 = R3/R4 => R4 = R2*R3/R1",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the unknown resistance or balance check.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["target"] == "check":
            if data["balanced"]:
                return "Bridge is balanced"
            return f"Not balanced. R4 for balance = {_fval(data['R4_balanced'])} ohm"
        return f"{data['target']} = {_fval(data[data['target']])} ohm"


# ===================================================================
# 7. Biot-Savart  (tier 6)
# ===================================================================

@register
class BiotSavartGenerator(StepGenerator):
    """Compute magnetic field at the center of a circular current loop.

    B = mu_0 * I / (2 * R) for a single loop. For N turns,
    B = mu_0 * N * I / (2 * R).

    Difficulty scaling:
        Difficulty 1-3: single loop, integer current and radius.
        Difficulty 4-6: N turns, compute B.
        Difficulty 7-8: compute B on axis at distance z from center.

    Prerequisites:
        definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "biot_savart"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute B field at center of circular loop via Biot-Savart"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate current loop parameters and compute B.

        Args:
            difficulty: Controls number of turns and geometry.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        i_amps = round(self._rng.uniform(0.5, 10.0), 1)
        r_cm = self._rng.randint(1, 10 + difficulty)
        r = r_cm * 1e-2

        if difficulty <= 3:
            n = 1
            b = round(_MU_0 * i_amps / (2 * r), 4)
            return "B = mu_0*I/(2R)", {
                "I": i_amps, "R_cm": r_cm, "R": r,
                "N": n, "B": b, "mode": "center",
            }
        if difficulty <= 6:
            n = self._rng.randint(5, 50 + difficulty * 10)
            b = round(_MU_0 * n * i_amps / (2 * r), 4)
            return "B = mu_0*N*I/(2R)", {
                "I": i_amps, "R_cm": r_cm, "R": r,
                "N": n, "B": b, "mode": "center",
            }
        # On-axis field at distance z
        n = self._rng.randint(5, 50)
        z_cm = self._rng.randint(1, 10)
        z = z_cm * 1e-2
        b = round(_MU_0 * n * i_amps * r ** 2 / (2 * (r ** 2 + z ** 2) ** 1.5), 4)
        return "B = mu_0*N*I*R^2/(2(R^2+z^2)^{3/2})", {
            "I": i_amps, "R_cm": r_cm, "R": r,
            "N": n, "z_cm": z_cm, "z": z,
            "B": b, "mode": "axis",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Biot-Savart computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"I={data['I']}A, R={data['R_cm']}cm, N={data['N']}",
        ]
        if data["mode"] == "center":
            steps.append(f"B = mu_0*{data['N']}*{data['I']}/(2*{_fval(data['R'])})")
        else:
            steps.append(f"z={data['z_cm']}cm = {_fval(data['z'])}m")
            steps.append(
                f"B = mu_0*{data['N']}*{data['I']}*{_fval(data['R'])}^2"
                f"/(2*({_fval(data['R'])}^2+{_fval(data['z'])}^2)^(3/2))"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the magnetic field.

        Args:
            data: Solution data.

        Returns:
            B as a string with units.
        """
        return f"B = {_fmt(data['B'])} T"


# ===================================================================
# 8. Mutual inductance  (tier 6)
# ===================================================================

@register
class MutualInductanceGenerator(StepGenerator):
    """Compute mutual inductance and induced EMF for coupled solenoids.

    M = mu_0 * N1 * N2 * A / l for a solenoid. The induced EMF in
    the secondary is EMF = -M * dI/dt.

    Difficulty scaling:
        Difficulty 1-3: compute M from N1, N2, A, l.
        Difficulty 4-6: compute M and EMF for given dI/dt.
        Difficulty 7-8: compute M with a magnetic core (mu_r given).

    Prerequisites:
        faraday_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mutual_inductance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["faraday_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute mutual inductance and induced EMF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate solenoid parameters and compute M and EMF.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n1 = self._rng.randint(50, 500)
        n2 = self._rng.randint(50, 500)
        a_cm2 = self._rng.randint(1, 10 + difficulty * 2)
        a = a_cm2 * 1e-4
        l_cm = self._rng.randint(5, 30 + difficulty * 5)
        l = l_cm * 1e-2

        mu_r = 1
        if difficulty >= 7:
            mu_r = self._rng.randint(100, 2000)

        m_val = round(_MU_0 * mu_r * n1 * n2 * a / l, 4)

        if difficulty <= 3:
            return "M = mu_0*N1*N2*A/l", {
                "N1": n1, "N2": n2, "A_cm2": a_cm2, "l_cm": l_cm,
                "mu_r": mu_r, "M": m_val, "mode": "M_only",
            }
        di_dt = round(self._rng.uniform(1.0, 50.0), 1)
        emf = round(-m_val * di_dt, 4)
        return "EMF = -M dI/dt", {
            "N1": n1, "N2": n2, "A_cm2": a_cm2, "l_cm": l_cm,
            "mu_r": mu_r, "M": m_val,
            "dI_dt": di_dt, "EMF": emf, "mode": "full",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mutual inductance computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"N1={data['N1']}, N2={data['N2']}, "
            f"A={data['A_cm2']}cm^2, l={data['l_cm']}cm",
        ]
        if data["mu_r"] > 1:
            steps.append(f"mu_r = {data['mu_r']}")
        steps.append(f"M = {_fmt(data['M'])} H")
        if data["mode"] == "full":
            steps.append(f"dI/dt = {data['dI_dt']} A/s")
            steps.append(f"EMF = -M*dI/dt")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return mutual inductance and optionally EMF.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "full":
            return f"M = {_fmt(data['M'])} H, EMF = {_fval(data['EMF'])} V"
        return f"M = {_fmt(data['M'])} H"


# ===================================================================
# 9. Skin depth  (tier 5)
# ===================================================================

@register
class SkinDepthGenerator(StepGenerator):
    """Compute skin depth for electromagnetic wave penetration.

    delta = sqrt(2 / (omega * mu * sigma)) where omega = 2*pi*f.
    Compute for copper or aluminum at a given frequency.

    Difficulty scaling:
        Difficulty 1-3: copper at common power frequency (50/60 Hz).
        Difficulty 4-6: copper or aluminum at RF frequencies.
        Difficulty 7-8: compute attenuation factor e^(-d/delta).

    Prerequisites:
        division.
    """

    _MATERIALS = {
        "copper": _SIGMA_COPPER,
        "aluminum": _SIGMA_ALUMINUM,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "skin_depth"

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
        return "compute skin depth for conductor at given frequency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate frequency and material parameters for skin depth.

        Args:
            difficulty: Controls frequency range and material choice.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            material = "copper"
            f_hz = self._rng.choice([50, 60])
        else:
            material = self._rng.choice(["copper", "aluminum"])
            exp = self._rng.randint(3, 6 + difficulty)
            f_hz = self._rng.randint(1, 9) * (10 ** exp)

        sigma = self._MATERIALS[material]
        omega = 2 * math.pi * f_hz
        delta = round(math.sqrt(2 / (omega * _MU_0 * sigma)), 4)

        if difficulty <= 6:
            return "delta = sqrt(2/(omega*mu*sigma))", {
                "material": material, "f_Hz": f_hz,
                "sigma": sigma, "omega": round(omega, 4),
                "delta": delta, "mode": "depth",
            }
        # Attenuation at depth d
        d_mm = round(self._rng.uniform(0.1, 5.0), 1)
        d = d_mm * 1e-3
        attenuation = round(math.exp(-d / delta), 4)
        return "A = e^{-d/delta}", {
            "material": material, "f_Hz": f_hz,
            "sigma": sigma, "omega": round(omega, 4),
            "delta": delta, "d_mm": d_mm, "d": d,
            "attenuation": attenuation, "mode": "atten",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate skin depth computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"Material: {data['material']}, f={_fval(data['f_Hz'])} Hz",
            f"omega = 2*pi*f = {_fval(data['omega'])} rad/s",
            f"delta = sqrt(2/(omega*mu_0*sigma))",
        ]
        if data["mode"] == "atten":
            steps.append(f"delta = {_fmt(data['delta'])} m")
            steps.append(f"d = {data['d_mm']}mm, A = e^(-d/delta)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the skin depth and optionally attenuation.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "atten":
            return (
                f"delta = {_fmt(data['delta'])} m, "
                f"A = {_fval(data['attenuation'])}"
            )
        return f"delta = {_fmt(data['delta'])} m"


# ===================================================================
# 10. Waveguide cutoff  (tier 6)
# ===================================================================

@register
class WaveguideCutoffGenerator(StepGenerator):
    """Compute cutoff frequency for a rectangular waveguide.

    For TE10 mode: f_c = c / (2a) where a is the broad wall dimension.
    For general TE_mn: f_c = (c/2) * sqrt((m/a)^2 + (n/b)^2).

    Difficulty scaling:
        Difficulty 1-3: TE10 mode, integer dimension in cm.
        Difficulty 4-6: TE10 mode, decimal dimension, also compute
            guide wavelength.
        Difficulty 7-8: general TE_mn mode with both a and b.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "waveguide_cutoff"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute cutoff frequency for rectangular waveguide"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate waveguide dimensions and compute cutoff frequency.

        Args:
            difficulty: Controls mode and dimensions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a_cm = self._rng.randint(1, 5)
            a = a_cm * 1e-2
            f_c = round(_C / (2 * a), 4)
            return "f_c = c/(2a)", {
                "a_cm": a_cm, "a": a, "f_c": f_c,
                "mode": "TE10", "m": 1, "n": 0,
            }
        if difficulty <= 6:
            a_cm = round(self._rng.uniform(1.0, 5.0), 1)
            a = a_cm * 1e-2
            f_c = round(_C / (2 * a), 4)
            f_op = round(f_c * self._rng.uniform(1.1, 2.0), 4)
            lam_g = round(_C / math.sqrt(f_op ** 2 - f_c ** 2), 4)
            return "f_c = c/(2a)", {
                "a_cm": a_cm, "a": a, "f_c": f_c,
                "f_op": f_op, "lambda_g": lam_g,
                "mode": "guide_wl", "m": 1, "n": 0,
            }
        # General TE_mn
        a_cm = round(self._rng.uniform(1.0, 5.0), 1)
        b_cm = round(self._rng.uniform(0.5, a_cm - 0.1), 1)
        a = a_cm * 1e-2
        b = b_cm * 1e-2
        m = self._rng.choice([1, 2])
        n = self._rng.choice([0, 1])
        f_c = round((_C / 2) * math.sqrt((m / a) ** 2 + (n / b) ** 2), 4)
        return "f_c = (c/2) sqrt((m/a)^2 + (n/b)^2)", {
            "a_cm": a_cm, "b_cm": b_cm, "a": a, "b": b,
            "m": m, "n": n, "f_c": f_c, "mode": "general",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate waveguide cutoff computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "TE10":
            return [
                f"a = {data['a_cm']}cm = {_fval(data['a'])}m",
                f"f_c = c/(2a) = {_fmt(_C)}/(2*{_fval(data['a'])})",
            ]
        if data["mode"] == "guide_wl":
            return [
                f"a = {data['a_cm']}cm",
                f"f_c = {_fmt(data['f_c'])} Hz",
                f"f_op = {_fmt(data['f_op'])} Hz",
                f"lambda_g = c/sqrt(f_op^2 - f_c^2)",
            ]
        return [
            f"a={data['a_cm']}cm, b={data['b_cm']}cm",
            f"TE_{data['m']}{data['n']} mode",
            f"f_c = (c/2)*sqrt(({data['m']}/{_fval(data['a'])})^2"
            f"+({data['n']}/{_fval(data['b'])})^2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the cutoff frequency.

        Args:
            data: Solution data.

        Returns:
            f_c as a string with units.
        """
        if data["mode"] == "guide_wl":
            return (
                f"f_c = {_fmt(data['f_c'])} Hz, "
                f"lambda_g = {_fval(data['lambda_g'])} m"
            )
        return f"f_c = {_fmt(data['f_c'])} Hz"
