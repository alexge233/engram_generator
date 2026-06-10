"""Deep engineering generators -- control, signal, power, and materials.

10 generators across tiers 4-6 covering Nyquist stability, Kalman
filtering, FFT butterfly, PID tuning, DC power flow, fatigue life,
Butterworth filter design, impedance matching, vibration analysis,
and series-parallel reliability.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


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


def _comb(n: int, k: int) -> int:
    """Compute binomial coefficient C(n, k).

    Args:
        n: Total items.
        k: Items chosen.

    Returns:
        Binomial coefficient.
    """
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


# ===================================================================
# 1. Nyquist Stability  (tier 6)
# ===================================================================

@register
class NyquistStabilityGenerator(StepGenerator):
    """Determine closed-loop stability via the Nyquist criterion.

    Count encirclements of -1+0j in the Nyquist plot.  N = Z - P
    where Z = closed-loop RHP poles, P = open-loop RHP poles.
    If N = 0 and P = 0, the system is stable.

    Difficulty scaling:
        Difficulty 1-3: simple system, P=0, check N.
        Difficulty 4-6: system with open-loop RHP poles.
        Difficulty 7-8: higher-order system, compute gain at crossover.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nyquist_stability"

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
            Short task description string.
        """
        return "determine stability via Nyquist criterion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Nyquist stability problem.

        Args:
            difficulty: Controls system complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = 0
            n_encircle = self._rng.choice([0, 0, 1])
        elif difficulty <= 6:
            p = self._rng.randint(0, 2)
            n_encircle = self._rng.randint(-1, 2)
        else:
            p = self._rng.randint(0, 3)
            n_encircle = self._rng.randint(-2, 3)

        z = n_encircle + p  # Z = N + P
        stable = z == 0

        # Generate a gain K and phase crossover frequency
        k = round(self._rng.uniform(0.5, 10.0), 2)
        w_pc = round(self._rng.uniform(1.0, 20.0), 2)

        problem = (
            f"open-loop RHP poles P={p}, "
            f"encirclements N={n_encircle}, K={_fmt(k)}"
        )
        return problem, {
            "p": p, "n_encircle": n_encircle, "z": z,
            "stable": stable, "k": k, "w_pc": w_pc,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Nyquist stability analysis steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"open-loop RHP poles: P = {sd['p']}",
            f"encirclements of -1: N = {sd['n_encircle']}",
            f"Z = N + P = {sd['n_encircle']} + {sd['p']} = {sd['z']}",
            f"closed-loop RHP poles: Z = {sd['z']}",
            f"stable: {'yes' if sd['stable'] else 'no'} (Z={'0' if sd['stable'] else str(sd['z'])})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the stability verdict.

        Args:
            sd: Solution data.

        Returns:
            Stability result with Z value.
        """
        verdict = "stable" if sd["stable"] else "unstable"
        return f"Z={sd['z']}, {verdict}"


# ===================================================================
# 2. Kalman Gain  (tier 6)
# ===================================================================

@register
class KalmanGainGenerator(StepGenerator):
    """Compute the Kalman gain and state update for a 1D system.

    K = P * H / (H * P * H + R).  Update: x = x + K*(z - H*x),
    P_new = (1 - K*H)*P.

    Difficulty scaling:
        Difficulty 1-3: scalar system (H=1), integer values.
        Difficulty 4-6: scalar with H != 1.
        Difficulty 7-8: 2D diagonal approximation.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kalman_gain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Kalman gain and state update"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kalman filter update problem.

        Args:
            difficulty: Controls system dimensionality.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            h = 1.0
            p_prior = float(self._rng.randint(1, 10))
            r = float(self._rng.randint(1, 10))
            x_prior = float(self._rng.randint(-10, 10))
            z_meas = float(self._rng.randint(-10, 10))
        elif difficulty <= 6:
            h = round(self._rng.uniform(0.5, 3.0), 2)
            p_prior = round(self._rng.uniform(1.0, 20.0), 2)
            r = round(self._rng.uniform(0.5, 15.0), 2)
            x_prior = round(self._rng.uniform(-10.0, 10.0), 2)
            z_meas = round(self._rng.uniform(-10.0, 10.0), 2)
        else:
            h = round(self._rng.uniform(0.1, 5.0), 2)
            p_prior = round(self._rng.uniform(1.0, 50.0), 2)
            r = round(self._rng.uniform(0.1, 20.0), 2)
            x_prior = round(self._rng.uniform(-20.0, 20.0), 2)
            z_meas = round(self._rng.uniform(-20.0, 20.0), 2)

        # K = P*H / (H*P*H + R)
        denom = h * p_prior * h + r
        k_gain = round(p_prior * h / denom, 4)
        innovation = round(z_meas - h * x_prior, 4)
        x_post = round(x_prior + k_gain * innovation, 4)
        p_post = round((1 - k_gain * h) * p_prior, 4)

        problem = (
            f"x={_fmt(x_prior)}, P={_fmt(p_prior)}, "
            f"H={_fmt(h)}, R={_fmt(r)}, z={_fmt(z_meas)}"
        )
        return problem, {
            "h": h, "p_prior": p_prior, "r": r,
            "x_prior": x_prior, "z_meas": z_meas,
            "denom": round(denom, 4), "k_gain": k_gain,
            "innovation": innovation,
            "x_post": x_post, "p_post": p_post,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Kalman filter computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"S = H*P*H + R = {_fmt(sd['h'])}*{_fmt(sd['p_prior'])}*{_fmt(sd['h'])} + {_fmt(sd['r'])} = {_fmt(sd['denom'])}",
            f"K = P*H/S = {_fmt(sd['p_prior'])}*{_fmt(sd['h'])}/{_fmt(sd['denom'])} = {_fmt(sd['k_gain'])}",
            f"innovation = z - H*x = {_fmt(sd['z_meas'])} - {_fmt(sd['h'])}*{_fmt(sd['x_prior'])} = {_fmt(sd['innovation'])}",
            f"x_post = x + K*innov = {_fmt(sd['x_post'])}",
            f"P_post = (1 - K*H)*P = {_fmt(sd['p_post'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Kalman gain and updated state.

        Args:
            sd: Solution data.

        Returns:
            Gain, posterior state, and posterior covariance.
        """
        return (
            f"K={_fmt(sd['k_gain'])}, "
            f"x={_fmt(sd['x_post'])}, "
            f"P={_fmt(sd['p_post'])}"
        )


# ===================================================================
# 3. FFT Butterfly  (tier 5)
# ===================================================================

@register
class FFTButterflyGenerator(StepGenerator):
    """Compute one stage of radix-2 FFT butterfly operations.

    Butterfly: X[k] = X_even[k] + W_N^k * X_odd[k], where
    W_N = exp(-2*pi*i/N) is the N-th root of unity (twiddle factor).

    Difficulty scaling:
        Difficulty 1-3: N=4, show first butterfly stage.
        Difficulty 4-6: N=4, full computation.
        Difficulty 7-8: N=8, first stage.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fft_butterfly"

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
            Short task description string.
        """
        return "compute FFT butterfly stage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an FFT butterfly computation problem.

        Args:
            difficulty: Controls FFT size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            n = 4
        else:
            n = 8

        # Generate input sequence
        x = [self._rng.randint(-4, 4) for _ in range(n)]

        # Split into even and odd
        x_even = [x[i] for i in range(0, n, 2)]
        x_odd = [x[i] for i in range(1, n, 2)]

        # Compute twiddle factors W_N^k for first stage
        half = n // 2
        results_re = []
        results_im = []
        for k in range(half):
            angle = -2 * math.pi * k / n
            w_re = round(math.cos(angle), 4)
            w_im = round(math.sin(angle), 4)
            # X[k] = X_even[k] + W * X_odd[k] (real input)
            prod_re = round(w_re * x_odd[k], 4)
            prod_im = round(w_im * x_odd[k], 4)
            res_re = round(x_even[k] + prod_re, 4)
            res_im = round(prod_im, 4)
            results_re.append(res_re)
            results_im.append(res_im)

        x_str = ", ".join(str(v) for v in x)
        problem = f"radix-2 FFT first stage, x = [{x_str}], N={n}"

        return problem, {
            "n": n, "x": x, "x_even": x_even, "x_odd": x_odd,
            "results_re": results_re, "results_im": results_im,
            "half": half,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate FFT butterfly computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        even_str = ", ".join(str(v) for v in sd["x_even"])
        odd_str = ", ".join(str(v) for v in sd["x_odd"])
        steps = [
            f"N={sd['n']}, split: even=[{even_str}], odd=[{odd_str}]",
        ]
        for k in range(sd["half"]):
            angle = -2 * math.pi * k / sd["n"]
            w_re = round(math.cos(angle), 4)
            w_im = round(math.sin(angle), 4)
            steps.append(
                f"k={k}: W_{sd['n']}^{k}={_fmt(w_re)}+{_fmt(w_im)}i, "
                f"X[{k}]={_fmt(sd['results_re'][k])}+{_fmt(sd['results_im'][k])}i"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the first-stage butterfly outputs.

        Args:
            sd: Solution data.

        Returns:
            Butterfly output values.
        """
        parts = [
            f"X[{k}]={_fmt(sd['results_re'][k])}+{_fmt(sd['results_im'][k])}i"
            for k in range(sd["half"])
        ]
        return ", ".join(parts)


# ===================================================================
# 4. PID Tuning (Ziegler-Nichols)  (tier 5)
# ===================================================================

@register
class PIDTuningGenerator(StepGenerator):
    """Compute PID parameters via Ziegler-Nichols tuning.

    From ultimate gain K_u and ultimate period T_u:
    P:  Kp = 0.5*K_u
    PI: Kp = 0.45*K_u, Ki = 1.2*Kp/T_u
    PID: Kp = 0.6*K_u, Ki = 2*Kp/T_u, Kd = Kp*T_u/8.

    Difficulty scaling:
        Difficulty 1-3: P controller only.
        Difficulty 4-6: PI controller.
        Difficulty 7-8: full PID controller.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pid_tuning"

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
            Short task description string.
        """
        return "compute PID gains via Ziegler-Nichols method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PID tuning problem.

        Args:
            difficulty: Controls controller type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k_u = round(self._rng.uniform(1.0, 20.0), 2)
        t_u = round(self._rng.uniform(0.5, 10.0), 2)

        if difficulty <= 3:
            ctrl = "P"
            kp = round(0.5 * k_u, 4)
            ki = 0.0
            kd = 0.0
        elif difficulty <= 6:
            ctrl = "PI"
            kp = round(0.45 * k_u, 4)
            ki = round(1.2 * kp / t_u, 4)
            kd = 0.0
        else:
            ctrl = "PID"
            kp = round(0.6 * k_u, 4)
            ki = round(2 * kp / t_u, 4)
            kd = round(kp * t_u / 8, 4)

        problem = f"K_u={_fmt(k_u)}, T_u={_fmt(t_u)}, design {ctrl} controller"
        return problem, {
            "k_u": k_u, "t_u": t_u, "ctrl": ctrl,
            "kp": kp, "ki": ki, "kd": kd,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate PID tuning computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"K_u = {_fmt(sd['k_u'])}, T_u = {_fmt(sd['t_u'])}"]
        ctrl = sd["ctrl"]
        if ctrl == "P":
            steps.append(f"Kp = 0.5*K_u = 0.5*{_fmt(sd['k_u'])} = {_fmt(sd['kp'])}")
        elif ctrl == "PI":
            steps.append(f"Kp = 0.45*K_u = {_fmt(sd['kp'])}")
            steps.append(f"Ki = 1.2*Kp/T_u = {_fmt(sd['ki'])}")
        else:
            steps.append(f"Kp = 0.6*K_u = {_fmt(sd['kp'])}")
            steps.append(f"Ki = 2*Kp/T_u = {_fmt(sd['ki'])}")
            steps.append(f"Kd = Kp*T_u/8 = {_fmt(sd['kd'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the PID gains.

        Args:
            sd: Solution data.

        Returns:
            Controller gains.
        """
        if sd["ctrl"] == "P":
            return f"Kp={_fmt(sd['kp'])}"
        elif sd["ctrl"] == "PI":
            return f"Kp={_fmt(sd['kp'])}, Ki={_fmt(sd['ki'])}"
        return f"Kp={_fmt(sd['kp'])}, Ki={_fmt(sd['ki'])}, Kd={_fmt(sd['kd'])}"


# ===================================================================
# 5. DC Power Flow  (tier 5)
# ===================================================================

@register
class PowerFlowDCGenerator(StepGenerator):
    """Solve DC power flow equations P = B * theta.

    Given the susceptance matrix B and power injections P, solve
    for voltage angles theta.  For a 2-bus system: theta_2 = P_2 / B_22.
    For 3-bus: solve 2x2 linear system.

    Difficulty scaling:
        Difficulty 1-3: 2-bus system, scalar equation.
        Difficulty 4-6: 3-bus system, 2x2 solve.
        Difficulty 7-8: 3-bus with varied susceptances.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_flow_dc"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "solve DC power flow for voltage angles"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DC power flow problem.

        Args:
            difficulty: Controls system size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # 2-bus: bus 1 = slack, solve for theta_2
            b = self._rng.randint(5, 30)
            p2 = round(self._rng.uniform(-5.0, 5.0), 2)
            theta2 = round(p2 / b, 4)
            problem = f"2-bus: B_22={b}, P_2={_fmt(p2)}"
            return problem, {
                "mode": "2bus", "b22": b, "p2": p2,
                "theta2": theta2,
            }
        else:
            # 3-bus: B = [[b11, b12], [b12, b22]], P = [p2, p3]
            b12 = -self._rng.randint(3, 15)
            b13 = -self._rng.randint(3, 15) if difficulty > 6 else 0
            b23 = -self._rng.randint(3, 15)
            b11 = -b12 - b13
            b22 = -b12 - b23
            p2 = round(self._rng.uniform(-3.0, 3.0), 2)
            p3 = round(self._rng.uniform(-3.0, 3.0), 2)

            # Solve [[b11, b12+b13], [b12+b23 ...]] -- simplified for 2x2
            # Actually B_red = [[b11, b12], [b12, b22]] when b13=0
            # For simplicity: use Cramer's rule
            det_b = b11 * b22 - b12 * b12
            if det_b == 0:
                det_b = 1  # Safety
            theta2 = round((p2 * b22 - p3 * b12) / det_b, 4)
            theta3 = round((b11 * p3 - b12 * p2) / det_b, 4)

            problem = (
                f"3-bus: B=[[{b11},{b12}],[{b12},{b22}]], "
                f"P=[{_fmt(p2)},{_fmt(p3)}]"
            )
            return problem, {
                "mode": "3bus",
                "b11": b11, "b12": b12, "b22": b22,
                "p2": p2, "p3": p3, "det_b": det_b,
                "theta2": theta2, "theta3": theta3,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate DC power flow computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "2bus":
            return [
                f"P = B * theta => theta_2 = P_2 / B_22",
                f"theta_2 = {_fmt(sd['p2'])} / {sd['b22']} = {_fmt(sd['theta2'])} rad",
            ]
        return [
            f"B = [[{sd['b11']}, {sd['b12']}], [{sd['b12']}, {sd['b22']}]]",
            f"det(B) = {sd['b11']}*{sd['b22']} - ({sd['b12']})^2 = {sd['det_b']}",
            f"theta_2 = ({_fmt(sd['p2'])}*{sd['b22']} - {_fmt(sd['p3'])}*{sd['b12']}) / {sd['det_b']} = {_fmt(sd['theta2'])}",
            f"theta_3 = ({sd['b11']}*{_fmt(sd['p3'])} - {sd['b12']}*{_fmt(sd['p2'])}) / {sd['det_b']} = {_fmt(sd['theta3'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the voltage angles.

        Args:
            sd: Solution data.

        Returns:
            Angle values in radians.
        """
        if sd["mode"] == "2bus":
            return f"theta_2={_fmt(sd['theta2'])} rad"
        return (
            f"theta_2={_fmt(sd['theta2'])}, "
            f"theta_3={_fmt(sd['theta3'])} rad"
        )


# ===================================================================
# 6. Fatigue Life (Miner's Rule)  (tier 5)
# ===================================================================

@register
class FatigueLifeGenerator(StepGenerator):
    """Compute fatigue damage fraction via Miner's rule.

    Miner's rule: D = sum(n_i / N_i).  Failure at D = 1.
    Given a load spectrum {stress_i, n_i} and S-N curve
    N = C / S^m, compute the damage fraction.

    Difficulty scaling:
        Difficulty 1-3: 2 load levels.
        Difficulty 4-6: 3 load levels.
        Difficulty 7-8: 4 load levels.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fatigue_life"

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
            Short task description string.
        """
        return "compute fatigue damage fraction via Miner's rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fatigue life problem.

        Args:
            difficulty: Controls number of load levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_levels = 2
        elif difficulty <= 6:
            n_levels = 3
        else:
            n_levels = 4

        c = self._rng.randint(10**6, 10**8)
        m = self._rng.choice([3, 4, 5])

        stresses = []
        cycles = []
        for _ in range(n_levels):
            s = self._rng.randint(100, 500)
            n = self._rng.randint(1000, 50000)
            stresses.append(s)
            cycles.append(n)

        # N_i = C / S_i^m
        n_fail = [round(c / (s ** m), 4) for s in stresses]
        damage_fracs = [round(cycles[i] / n_fail[i], 4)
                        for i in range(n_levels)]
        total_damage = round(sum(damage_fracs), 4)

        loads_str = "; ".join(
            f"S={stresses[i]} MPa, n={cycles[i]}"
            for i in range(n_levels)
        )
        problem = f"S-N: N=C/S^m, C={c}, m={m}. Loads: {loads_str}"

        return problem, {
            "n_levels": n_levels, "c": c, "m": m,
            "stresses": stresses, "cycles": cycles,
            "n_fail": n_fail, "damage_fracs": damage_fracs,
            "total_damage": total_damage,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate fatigue life computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"S-N curve: N = {sd['c']} / S^{sd['m']}"]
        for i in range(sd["n_levels"]):
            steps.append(
                f"S={sd['stresses'][i]}: N={_fmt(sd['n_fail'][i])}, "
                f"d={sd['cycles'][i]}/{_fmt(sd['n_fail'][i])}="
                f"{_fmt(sd['damage_fracs'][i])}"
            )
        steps.append(f"D_total = {_fmt(sd['total_damage'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the total damage fraction.

        Args:
            sd: Solution data.

        Returns:
            Damage fraction and failure assessment.
        """
        status = "failure" if sd["total_damage"] >= 1.0 else "safe"
        return f"D={_fmt(sd['total_damage'])}, {status}"


# ===================================================================
# 7. Butterworth Filter Design  (tier 5)
# ===================================================================

@register
class FilterDesignGenerator(StepGenerator):
    """Compute Butterworth filter magnitude response.

    |H(jw)|^2 = 1 / (1 + (w/w_c)^{2n}).  -3 dB at w = w_c.
    Roll-off: -20*n dB/decade.  Compute attenuation at a given
    frequency.

    Difficulty scaling:
        Difficulty 1-3: order n=1 or n=2, single frequency.
        Difficulty 4-6: order n=2 to n=4.
        Difficulty 7-8: order n=4 to n=8, multiple frequencies.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "filter_design"

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
            Short task description string.
        """
        return "compute Butterworth filter attenuation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Butterworth filter design problem.

        Args:
            difficulty: Controls filter order.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([1, 2])
        elif difficulty <= 6:
            n = self._rng.choice([2, 3, 4])
        else:
            n = self._rng.choice([4, 5, 6, 8])

        w_c = self._rng.choice([100, 500, 1000, 2000, 5000])
        w = self._rng.choice([
            w_c // 2, w_c, w_c * 2, w_c * 5, w_c * 10
        ])

        ratio = w / w_c
        h_sq = 1.0 / (1.0 + ratio ** (2 * n))
        h_mag = round(math.sqrt(h_sq), 4)
        h_db = round(10 * math.log10(h_sq), 4) if h_sq > 0 else -999.0
        rolloff = -20 * n

        problem = (
            f"Butterworth n={n}, w_c={w_c} rad/s, "
            f"compute |H| at w={w} rad/s"
        )
        return problem, {
            "n": n, "w_c": w_c, "w": w, "ratio": round(ratio, 4),
            "h_sq": round(h_sq, 4), "h_mag": h_mag, "h_db": h_db,
            "rolloff": rolloff,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate filter design computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"n={sd['n']}, w_c={sd['w_c']}, w={sd['w']}",
            f"w/w_c = {_fmt(sd['ratio'])}",
            f"|H|^2 = 1/(1+({_fmt(sd['ratio'])})^{2 * sd['n']}) = {_fmt(sd['h_sq'])}",
            f"|H| = {_fmt(sd['h_mag'])}",
            f"|H| dB = {_fmt(sd['h_db'])} dB",
            f"roll-off = {sd['rolloff']} dB/decade",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the filter magnitude and dB value.

        Args:
            sd: Solution data.

        Returns:
            Magnitude and dB attenuation.
        """
        return f"|H|={_fmt(sd['h_mag'])}, {_fmt(sd['h_db'])} dB"


# ===================================================================
# 8. Impedance Matching (L-network)  (tier 5)
# ===================================================================

@register
class ImpedanceMatchingGenerator(StepGenerator):
    """Design an L-network for impedance matching.

    Q = sqrt(R_L/R_S - 1) where R_L > R_S.
    X_L = Q * R_S (series reactance).
    X_C = R_L / Q (shunt reactance).

    Difficulty scaling:
        Difficulty 1-3: integer resistances, small ratio.
        Difficulty 4-6: wider range, compute component values.
        Difficulty 7-8: frequency-dependent component sizing.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "impedance_matching"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "design L-network for impedance matching"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an impedance matching problem.

        Args:
            difficulty: Controls resistance range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            r_s = self._rng.choice([25, 50, 75])
            r_l = self._rng.choice([100, 150, 200])
        elif difficulty <= 6:
            r_s = self._rng.randint(10, 100)
            r_l = self._rng.randint(r_s + 50, 500)
        else:
            r_s = self._rng.randint(5, 75)
            r_l = self._rng.randint(r_s + 50, 1000)

        q_factor = round(math.sqrt(r_l / r_s - 1), 4)
        x_l = round(q_factor * r_s, 4)
        x_c = round(r_l / q_factor, 4) if q_factor > 0 else 0.0

        problem = f"R_S={r_s} ohm, R_L={r_l} ohm"
        return problem, {
            "r_s": r_s, "r_l": r_l,
            "q_factor": q_factor, "x_l": x_l, "x_c": x_c,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate impedance matching computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"R_L/R_S = {sd['r_l']}/{sd['r_s']} = {_fmt(round(sd['r_l'] / sd['r_s'], 4))}",
            f"Q = sqrt(R_L/R_S - 1) = {_fmt(sd['q_factor'])}",
            f"X_L = Q*R_S = {_fmt(sd['q_factor'])}*{sd['r_s']} = {_fmt(sd['x_l'])} ohm",
            f"X_C = R_L/Q = {sd['r_l']}/{_fmt(sd['q_factor'])} = {_fmt(sd['x_c'])} ohm",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the L-network reactances.

        Args:
            sd: Solution data.

        Returns:
            Q factor and reactance values.
        """
        return (
            f"Q={_fmt(sd['q_factor'])}, "
            f"X_L={_fmt(sd['x_l'])}, "
            f"X_C={_fmt(sd['x_c'])} ohm"
        )


# ===================================================================
# 9. Vibration Analysis  (tier 5)
# ===================================================================

@register
class VibrationAnalysisGenerator(StepGenerator):
    """Compute forced vibration amplitude and resonance frequency.

    Amplitude: X = F_0 / sqrt((k - m*w^2)^2 + (c*w)^2).
    Natural frequency: w_n = sqrt(k/m).
    Damping ratio: zeta = c / (2*sqrt(k*m)).

    Difficulty scaling:
        Difficulty 1-3: undamped (c=0), integer k, m.
        Difficulty 4-6: lightly damped, compute amplitude.
        Difficulty 7-8: sweep multiple frequencies.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vibration_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute forced vibration amplitude"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vibration analysis problem.

        Args:
            difficulty: Controls damping and forcing.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.choice([100, 200, 400, 500])
            m_val = self._rng.choice([1, 2, 4, 5])
            c = 0.0
        elif difficulty <= 6:
            k = self._rng.randint(50, 500)
            m_val = self._rng.randint(1, 10)
            c = round(self._rng.uniform(1.0, 20.0), 2)
        else:
            k = self._rng.randint(50, 1000)
            m_val = self._rng.randint(1, 20)
            c = round(self._rng.uniform(5.0, 50.0), 2)

        f_0 = round(self._rng.uniform(10.0, 100.0), 2)
        w_n = round(math.sqrt(k / m_val), 4)

        # Forcing frequency
        w = round(self._rng.uniform(0.5 * w_n, 1.5 * w_n), 2)

        denom_sq = (k - m_val * w * w) ** 2 + (c * w) ** 2
        denom = round(math.sqrt(max(denom_sq, 1e-10)), 4)
        amplitude = round(f_0 / denom, 4)

        zeta = round(c / (2 * math.sqrt(k * m_val)), 4)

        problem = (
            f"k={k}, m={m_val}, c={_fmt(c)}, "
            f"F_0={_fmt(f_0)}, w={_fmt(w)}"
        )
        return problem, {
            "k": k, "m": m_val, "c": c, "f_0": f_0,
            "w": w, "w_n": w_n, "zeta": zeta,
            "amplitude": amplitude,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate vibration analysis computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"w_n = sqrt(k/m) = sqrt({sd['k']}/{sd['m']}) = {_fmt(sd['w_n'])} rad/s",
            f"zeta = c/(2*sqrt(k*m)) = {_fmt(sd['zeta'])}",
            f"w = {_fmt(sd['w'])} rad/s, w/w_n = {_fmt(round(sd['w'] / sd['w_n'], 4))}",
            f"X = F_0/sqrt((k-m*w^2)^2 + (c*w)^2) = {_fmt(sd['amplitude'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the vibration amplitude and natural frequency.

        Args:
            sd: Solution data.

        Returns:
            Amplitude and resonance frequency.
        """
        return (
            f"X={_fmt(sd['amplitude'])}, "
            f"w_n={_fmt(sd['w_n'])} rad/s"
        )


# ===================================================================
# 10. Reliability (Series-Parallel)  (tier 4)
# ===================================================================

@register
class ReliabilitySeriesParallelGenerator(StepGenerator):
    """Compute system reliability for series and parallel configurations.

    Series: R = prod(R_i).
    Parallel: R = 1 - prod(1 - R_i).
    k-out-of-n: R = sum_{i=k}^{n} C(n,i) * p^i * (1-p)^{n-i}.

    Difficulty scaling:
        Difficulty 1-3: 2-3 components, series or parallel.
        Difficulty 4-6: mixed series-parallel.
        Difficulty 7-8: k-out-of-n redundancy.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reliability_series_parallel"

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
            Short task description string.
        """
        return "compute system reliability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reliability computation problem.

        Args:
            difficulty: Controls configuration complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            config = self._rng.choice(["series", "parallel"])
            n_comp = self._rng.randint(2, 3)
            reliabilities = [round(self._rng.uniform(0.8, 0.99), 4)
                             for _ in range(n_comp)]
            if config == "series":
                result = 1.0
                for r in reliabilities:
                    result *= r
                result = round(result, 4)
            else:
                fail_prod = 1.0
                for r in reliabilities:
                    fail_prod *= (1 - r)
                result = round(1 - fail_prod, 4)

            r_str = ", ".join(_fmt(r) for r in reliabilities)
            problem = f"{config}: R = [{r_str}]"
            return problem, {
                "mode": config, "reliabilities": reliabilities,
                "result": result, "n_comp": n_comp,
            }
        elif difficulty <= 6:
            # Series-parallel: parallel subsystem in series
            r_series = [round(self._rng.uniform(0.85, 0.99), 4)
                        for _ in range(2)]
            r_par = [round(self._rng.uniform(0.8, 0.95), 4)
                     for _ in range(2)]
            par_result = round(1 - (1 - r_par[0]) * (1 - r_par[1]), 4)
            total = round(r_series[0] * r_series[1] * par_result, 4)

            problem = (
                f"series-parallel: S1={_fmt(r_series[0])}, "
                f"S2={_fmt(r_series[1])}, "
                f"parallel({_fmt(r_par[0])},{_fmt(r_par[1])})"
            )
            return problem, {
                "mode": "series_parallel",
                "r_series": r_series, "r_par": r_par,
                "par_result": par_result, "result": total,
            }
        else:
            # k-out-of-n
            n_comp = self._rng.randint(3, 5)
            k = self._rng.randint(2, n_comp)
            p = round(self._rng.uniform(0.8, 0.99), 4)

            result = 0.0
            terms = []
            for i in range(k, n_comp + 1):
                coeff = _comb(n_comp, i)
                term = coeff * (p ** i) * ((1 - p) ** (n_comp - i))
                terms.append(round(term, 4))
                result += term
            result = round(result, 4)

            problem = f"{k}-out-of-{n_comp}: p={_fmt(p)}"
            return problem, {
                "mode": "k_of_n", "n_comp": n_comp, "k": k,
                "p": p, "terms": terms, "result": result,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate reliability computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        mode = sd["mode"]
        if mode == "series":
            r_str = " * ".join(_fmt(r) for r in sd["reliabilities"])
            return [
                f"series: R = prod(R_i)",
                f"R = {r_str} = {_fmt(sd['result'])}",
            ]
        elif mode == "parallel":
            f_str = " * ".join(
                f"(1-{_fmt(r)})" for r in sd["reliabilities"]
            )
            return [
                f"parallel: R = 1 - prod(1-R_i)",
                f"R = 1 - {f_str} = {_fmt(sd['result'])}",
            ]
        elif mode == "series_parallel":
            return [
                f"parallel subsystem: 1-(1-{_fmt(sd['r_par'][0])})*(1-{_fmt(sd['r_par'][1])}) = {_fmt(sd['par_result'])}",
                f"total = {_fmt(sd['r_series'][0])}*{_fmt(sd['r_series'][1])}*{_fmt(sd['par_result'])} = {_fmt(sd['result'])}",
            ]
        else:  # k_of_n
            steps = [f"{sd['k']}-out-of-{sd['n_comp']}, p={_fmt(sd['p'])}"]
            for i, t in enumerate(sd["terms"]):
                idx = sd["k"] + i
                steps.append(
                    f"C({sd['n_comp']},{idx})*{_fmt(sd['p'])}^{idx}*"
                    f"{_fmt(round(1 - sd['p'], 4))}^{sd['n_comp'] - idx} = {_fmt(t)}"
                )
            steps.append(f"R = {_fmt(sd['result'])}")
            return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the system reliability.

        Args:
            sd: Solution data.

        Returns:
            Reliability value.
        """
        return f"R={_fmt(sd['result'])}"
