"""Control theory task generators.

6 generators across tiers 5-6 covering transfer functions from ODEs,
PID controller response, Routh stability criterion, Bode magnitude plots,
state-space conversion, and closed-loop feedback gain.
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


def _poly_str(coeffs: list[float], var: str = "s") -> str:
    """Format a polynomial as a string.

    Args:
        coeffs: Coefficients from highest power to constant.
        var: Variable name (default 's').

    Returns:
        Polynomial string like '2*s^2 + 3*s + 1'.
    """
    degree = len(coeffs) - 1
    parts = []
    for i, c in enumerate(coeffs):
        power = degree - i
        if c == 0:
            continue
        c_str = _fmt(c)
        if power == 0:
            parts.append(c_str)
        elif power == 1:
            parts.append(f"{c_str}*{var}")
        else:
            parts.append(f"{c_str}*{var}^{power}")
    return " + ".join(parts).replace("+ -", "- ") if parts else "0"


def _quadratic_roots(a: float, b: float, c: float) -> list[tuple[float, float]]:
    """Compute roots of a*x^2 + b*x + c = 0 as (real, imag) pairs.

    Args:
        a: Coefficient of x^2.
        b: Coefficient of x.
        c: Constant term.

    Returns:
        List of roots as (real_part, imag_part) tuples.
    """
    disc = b * b - 4 * a * c
    if disc >= 0:
        sqrt_disc = math.sqrt(disc)
        r1 = round((-b + sqrt_disc) / (2 * a), 4)
        r2 = round((-b - sqrt_disc) / (2 * a), 4)
        return [(r1, 0.0), (r2, 0.0)]
    sqrt_disc = math.sqrt(-disc)
    re = round(-b / (2 * a), 4)
    im = round(sqrt_disc / (2 * a), 4)
    return [(re, im), (re, -im)]


def _root_fmt(root: tuple[float, float]) -> str:
    """Format a complex root as a string.

    Args:
        root: Root as (real_part, imag_part).

    Returns:
        Formatted string like '-2.0' or '-1.0 + 2.0j'.
    """
    re, im = root
    if im == 0.0:
        return _fmt(re)
    if im > 0:
        return f"{_fmt(re)} + {_fmt(im)}j"
    return f"{_fmt(re)} - {_fmt(abs(im))}j"


# ---------------------------------------------------------------------------
# 1. Transfer Function (System) (tier 5)
# ---------------------------------------------------------------------------

@register
class TransferFunctionSysGenerator(StepGenerator):
    """Compute H(s) from a linear ODE.

    Given a*y'' + b*y' + c*y = d*u, derive H(s) = d/(a*s^2 + b*s + c)
    using the Laplace transform.

    Difficulty scaling:
        Difficulty 1-3: first-order ODE b*y' + c*y = d*u (a=0), small integers.
        Difficulty 4-6: second-order with integer coefficients.
        Difficulty 7-8: second-order with decimal coefficients.

    Prerequisites:
        laplace_transform.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transfer_function_sys"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["laplace_transform"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute transfer function H(s) from an ODE"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transfer function derivation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = 0
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 5)
            d = self._rng.randint(1, 5)
        elif difficulty <= 6:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 10)
            c = self._rng.randint(1, 10)
            d = self._rng.randint(1, 5)
        else:
            a = round(self._rng.uniform(0.5, 5.0), 1)
            b = round(self._rng.uniform(1.0, 10.0), 1)
            c = round(self._rng.uniform(1.0, 10.0), 1)
            d = round(self._rng.uniform(0.5, 5.0), 1)

        # Build ODE string
        terms = []
        if a != 0:
            terms.append(f"{_fmt(a)}*y''")
        terms.append(f"{_fmt(b)}*y'")
        terms.append(f"{_fmt(c)}*y")
        ode_str = " + ".join(terms) + f" = {_fmt(d)}*u"

        # Build denominator polynomial
        if a != 0:
            den_coeffs = [a, b, c]
            den_str = _poly_str([a, b, c])
        else:
            den_coeffs = [b, c]
            den_str = _poly_str([b, c])

        h_str = f"{_fmt(d)}/({den_str})"

        return (
            f"ODE: {ode_str}. Compute H(s) = Y(s)/U(s).",
            {
                "a": a, "b": b, "c": c, "d": d,
                "den_coeffs": den_coeffs,
                "den_str": den_str,
                "h_str": h_str,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for transfer function derivation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Laplace transform and rearrangement.
        """
        steps = []
        a, b, c, d = data["a"], data["b"], data["c"], data["d"]
        if a != 0:
            steps.append(
                f"Laplace: {_fmt(a)}*s^2*Y + {_fmt(b)}*s*Y + {_fmt(c)}*Y "
                f"= {_fmt(d)}*U"
            )
            steps.append(
                f"Y*({data['den_str']}) = {_fmt(d)}*U"
            )
        else:
            steps.append(
                f"Laplace: {_fmt(b)}*s*Y + {_fmt(c)}*Y = {_fmt(d)}*U"
            )
            steps.append(
                f"Y*({data['den_str']}) = {_fmt(d)}*U"
            )
        steps.append(f"H(s) = {data['h_str']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transfer function.

        Args:
            data: Solution data dict.

        Returns:
            H(s) as a string.
        """
        return f"H(s) = {data['h_str']}"


# ---------------------------------------------------------------------------
# 2. PID Response (tier 5)
# ---------------------------------------------------------------------------

@register
class PidResponseGenerator(StepGenerator):
    """Compute PID controller output from error values.

    Given error sequence e(t) at discrete time steps, compute
    u(t) = Kp*e(t) + Ki*integral(e) + Kd*de/dt using simple
    numerical approximations (rectangular integration, forward difference).

    Difficulty scaling:
        Difficulty 1-3: P-only or PD, 3 time steps, integer gains.
        Difficulty 4-6: full PID, 4 time steps, decimal gains.
        Difficulty 7-8: full PID, 5 time steps, larger error magnitudes.

    Prerequisites:
        derivative, integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pid_response"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["derivative", "integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute PID controller output from error values"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PID response problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_steps = 3
            kp = self._rng.randint(1, 5)
            ki = 0
            kd = self._rng.randint(0, 3)
            errors = [self._rng.randint(1, 10) for _ in range(n_steps)]
            dt = 1.0
        elif difficulty <= 6:
            n_steps = 4
            kp = round(self._rng.uniform(0.5, 5.0), 1)
            ki = round(self._rng.uniform(0.1, 2.0), 1)
            kd = round(self._rng.uniform(0.1, 2.0), 1)
            errors = [round(self._rng.uniform(-5.0, 10.0), 1)
                      for _ in range(n_steps)]
            dt = round(self._rng.choice([0.1, 0.5, 1.0]), 1)
        else:
            n_steps = 5
            kp = round(self._rng.uniform(0.5, 8.0), 1)
            ki = round(self._rng.uniform(0.1, 3.0), 1)
            kd = round(self._rng.uniform(0.1, 3.0), 1)
            errors = [round(self._rng.uniform(-10.0, 15.0), 1)
                      for _ in range(n_steps)]
            dt = round(self._rng.choice([0.1, 0.2, 0.5, 1.0]), 1)

        # Compute at the last time step
        t_idx = n_steps - 1

        # P term
        p_term = round(kp * errors[t_idx], 4)

        # I term (rectangular integration)
        integral_sum = round(sum(errors[:t_idx + 1]) * dt, 4)
        i_term = round(ki * integral_sum, 4)

        # D term (backward difference)
        if t_idx > 0:
            de_dt = round((errors[t_idx] - errors[t_idx - 1]) / dt, 4)
        else:
            de_dt = 0.0
        d_term = round(kd * de_dt, 4)

        u = round(p_term + i_term + d_term, 4)

        e_str = ", ".join(str(v) for v in errors)
        return (
            f"PID: Kp={_fmt(kp)}, Ki={_fmt(ki)}, Kd={_fmt(kd)}, dt={_fmt(dt)}. "
            f"e(t) = [{e_str}]. Compute u at t={t_idx}.",
            {
                "kp": kp, "ki": ki, "kd": kd, "dt": dt,
                "errors": errors, "t_idx": t_idx,
                "p_term": p_term, "integral_sum": integral_sum,
                "i_term": i_term, "de_dt": de_dt, "d_term": d_term,
                "u": u,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for PID computation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing P, I, D terms and total output.
        """
        steps = [
            f"P = Kp*e = {_fmt(data['kp'])}*{_fmt(data['errors'][data['t_idx']])} "
            f"= {_fmt(data['p_term'])}",
        ]
        if data["ki"] != 0:
            steps.append(
                f"I = Ki*sum(e)*dt = {_fmt(data['ki'])}*{_fmt(data['integral_sum'])} "
                f"= {_fmt(data['i_term'])}"
            )
        if data["kd"] != 0:
            steps.append(
                f"D = Kd*de/dt = {_fmt(data['kd'])}*{_fmt(data['de_dt'])} "
                f"= {_fmt(data['d_term'])}"
            )
        steps.append(
            f"u = P + I + D = {_fmt(data['p_term'])} + {_fmt(data['i_term'])} "
            f"+ {_fmt(data['d_term'])} = {_fmt(data['u'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the PID output.

        Args:
            data: Solution data dict.

        Returns:
            u(t) value as a string.
        """
        return f"u = {_fmt(data['u'])}"


# ---------------------------------------------------------------------------
# 3. Routh Stability (tier 6)
# ---------------------------------------------------------------------------

@register
class StabilityRouthGenerator(StepGenerator):
    """Build Routh array and count sign changes for stability.

    For a polynomial a*s^3 + b*s^2 + c*s + d, construct the Routh
    array and count sign changes in the first column to determine
    the number of right-half-plane roots.

    Difficulty scaling:
        Difficulty 1-3: positive integer coefficients (all stable).
        Difficulty 4-6: mixed signs, 1-2 sign changes possible.
        Difficulty 7-8: coefficients that produce zero rows or edge cases.

    Prerequisites:
        polynomial_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stability_routh"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "build Routh array and determine stability"

    def _build_routh(self, a: float, b: float, c: float,
                     d: float) -> tuple[list[list[float]], int]:
        """Build the Routh array for a third-order polynomial.

        Constructs the 4-row Routh array for a*s^3 + b*s^2 + c*s + d
        and counts sign changes in the first column.

        Args:
            a: Coefficient of s^3.
            b: Coefficient of s^2.
            c: Coefficient of s.
            d: Constant term.

        Returns:
            Tuple of (routh_array, sign_change_count).
        """
        # Row 0 (s^3): a, c
        # Row 1 (s^2): b, d
        # Row 2 (s^1): (b*c - a*d)/b
        # Row 3 (s^0): d
        if abs(b) < 1e-10:
            b = 0.001  # Avoid division by zero

        r2_0 = round((b * c - a * d) / b, 4)
        r3_0 = d

        array = [
            [a, c],
            [b, d],
            [r2_0, 0.0],
            [r3_0, 0.0],
        ]

        # Count sign changes in first column
        first_col = [a, b, r2_0, r3_0]
        changes = 0
        for i in range(1, len(first_col)):
            if first_col[i - 1] * first_col[i] < 0:
                changes += 1

        return array, changes

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Routh stability problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 10)
            d = self._rng.randint(1, 5)
        elif difficulty <= 6:
            a = self._rng.randint(1, 5)
            b = self._rng.choice([-3, -2, -1, 1, 2, 3, 4, 5])
            c = self._rng.randint(-5, 10)
            d = self._rng.choice([-4, -2, -1, 1, 2, 3, 5])
        else:
            a = self._rng.randint(1, 5)
            b = self._rng.choice([-5, -3, -1, 1, 2, 4])
            c = self._rng.randint(-8, 8)
            d = self._rng.choice([-5, -3, -1, 1, 3, 5])

        array, changes = self._build_routh(
            float(a), float(b), float(c), float(d)
        )
        stable = changes == 0

        poly = _poly_str([a, b, c, d])
        return (
            f"Routh criterion for {poly} = 0. "
            f"Build array, count sign changes.",
            {
                "a": a, "b": b, "c": c, "d": d,
                "poly": poly,
                "array": array,
                "changes": changes,
                "stable": stable,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Routh array construction.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each row and the sign-change count.
        """
        arr = data["array"]
        steps = [
            f"s^3: {_fmt(arr[0][0])}, {_fmt(arr[0][1])}",
            f"s^2: {_fmt(arr[1][0])}, {_fmt(arr[1][1])}",
            f"s^1: ({_fmt(data['b'])}*{_fmt(data['c'])} - "
            f"{_fmt(data['a'])}*{_fmt(data['d'])})/{_fmt(data['b'])} "
            f"= {_fmt(arr[2][0])}",
            f"s^0: {_fmt(arr[3][0])}",
            f"first column: [{_fmt(arr[0][0])}, {_fmt(arr[1][0])}, "
            f"{_fmt(arr[2][0])}, {_fmt(arr[3][0])}]",
            f"sign changes = {data['changes']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the stability verdict.

        Args:
            data: Solution data dict.

        Returns:
            Sign change count and stability status.
        """
        status = "stable" if data["stable"] else "unstable"
        return f"sign_changes = {data['changes']}, {status}"


# ---------------------------------------------------------------------------
# 4. Bode Magnitude (tier 5)
# ---------------------------------------------------------------------------

@register
class BodeMagnitudeGenerator(StepGenerator):
    """Compute Bode magnitude |H(jw)| in dB for a system.

    For a first-order H(s) = K/(s + a) or second-order
    H(s) = K/(s^2 + 2*zeta*wn*s + wn^2), compute
    |H(jw)| in dB = 20*log10(|H(jw)|) at a given frequency.

    Difficulty scaling:
        Difficulty 1-3: first-order, w in {1, 10, 100}, K and a integers.
        Difficulty 4-6: first-order, decimal K, a, and w.
        Difficulty 7-8: second-order system.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bode_magnitude"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Bode magnitude in dB at a given frequency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bode magnitude problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            # First order: H(s) = K / (s + a)
            if difficulty <= 3:
                k = self._rng.randint(1, 10)
                a = self._rng.randint(1, 10)
                w = self._rng.choice([1, 10, 100])
            else:
                k = round(self._rng.uniform(0.5, 10.0), 1)
                a = round(self._rng.uniform(0.5, 20.0), 1)
                w = round(self._rng.uniform(0.1, 100.0), 1)

            # |H(jw)| = K / sqrt(w^2 + a^2)
            mag = round(k / math.sqrt(w ** 2 + a ** 2), 4)
            mag_db = round(20 * math.log10(mag), 4) if mag > 0 else -999.0

            h_str = f"H(s) = {_fmt(k)}/(s + {_fmt(a)})"
            return (
                f"{h_str}. Compute |H(jw)| in dB at w = {_fmt(w)}.",
                {
                    "order": 1, "K": k, "a": a, "w": w,
                    "mag": mag, "mag_db": mag_db, "h_str": h_str,
                },
            )

        # Second order: H(s) = K / (s^2 + 2*zeta*wn*s + wn^2)
        k = round(self._rng.uniform(1.0, 10.0), 1)
        wn = round(self._rng.uniform(1.0, 20.0), 1)
        zeta = round(self._rng.uniform(0.1, 1.5), 2)
        w = round(self._rng.uniform(0.1, 50.0), 1)

        # |H(jw)| = K / sqrt((wn^2 - w^2)^2 + (2*zeta*wn*w)^2)
        real_part = wn ** 2 - w ** 2
        imag_part = 2 * zeta * wn * w
        den_mag = math.sqrt(real_part ** 2 + imag_part ** 2)
        mag = round(k / den_mag, 4) if den_mag > 1e-10 else 0.0
        mag_db = round(20 * math.log10(mag), 4) if mag > 0 else -999.0

        h_str = (f"H(s) = {_fmt(k)}/(s^2 + {_fmt(round(2 * zeta * wn, 4))}*s "
                 f"+ {_fmt(round(wn ** 2, 4))})")
        return (
            f"{h_str}. Compute |H(jw)| in dB at w = {_fmt(w)}.",
            {
                "order": 2, "K": k, "wn": wn, "zeta": zeta, "w": w,
                "mag": mag, "mag_db": mag_db, "h_str": h_str,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Bode magnitude.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing substitution and dB conversion.
        """
        steps = []
        w = data["w"]
        if data["order"] == 1:
            a = data["a"]
            k = data["K"]
            den = round(math.sqrt(w ** 2 + a ** 2), 4)
            steps.append(f"H(jw) = {_fmt(k)}/(j{_fmt(w)} + {_fmt(a)})")
            steps.append(f"|H(jw)| = {_fmt(k)}/sqrt({_fmt(w)}^2 + {_fmt(a)}^2) "
                         f"= {_fmt(k)}/{_fmt(den)} = {_fmt(data['mag'])}")
        else:
            k = data["K"]
            wn = data["wn"]
            zeta = data["zeta"]
            real_part = round(wn ** 2 - w ** 2, 4)
            imag_part = round(2 * zeta * wn * w, 4)
            den = round(math.sqrt(real_part ** 2 + imag_part ** 2), 4)
            steps.append(f"den = ({_fmt(real_part)})^2 + ({_fmt(imag_part)})^2")
            steps.append(f"|den| = {_fmt(den)}")
            steps.append(f"|H(jw)| = {_fmt(k)}/{_fmt(den)} = {_fmt(data['mag'])}")

        steps.append(
            f"|H(jw)|_dB = 20*log10({_fmt(data['mag'])}) = {_fmt(data['mag_db'])} dB"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Bode magnitude in dB.

        Args:
            data: Solution data dict.

        Returns:
            Magnitude in dB as a string.
        """
        return f"|H(jw)| = {_fmt(data['mag_db'])} dB"


# ---------------------------------------------------------------------------
# 5. State Space (tier 6)
# ---------------------------------------------------------------------------

@register
class StateSpaceGenerator(StepGenerator):
    """Convert a transfer function to controllable canonical form.

    Given H(s) = b/(s^2 + a1*s + a0), produce the state-space
    matrices A, B, C, D in controllable canonical form:
    A = [[0, 1], [-a0, -a1]], B = [[0], [1]], C = [b, 0], D = [0].

    Difficulty scaling:
        Difficulty 1-3: small integer a0, a1, b.
        Difficulty 4-6: larger integer coefficients.
        Difficulty 7-8: decimal coefficients.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "state_space"

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
            Short task description.
        """
        return "convert transfer function to controllable canonical form"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a state-space conversion problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a0 = self._rng.randint(1, 5)
            a1 = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
        elif difficulty <= 6:
            a0 = self._rng.randint(1, 20)
            a1 = self._rng.randint(1, 15)
            b = self._rng.randint(1, 10)
        else:
            a0 = round(self._rng.uniform(0.5, 20.0), 1)
            a1 = round(self._rng.uniform(0.5, 15.0), 1)
            b = round(self._rng.uniform(0.5, 10.0), 1)

        den_str = _poly_str([1, a1, a0])
        h_str = f"{_fmt(b)}/({den_str})"

        # Controllable canonical form
        a_mat = [[0, 1], [round(-a0, 4), round(-a1, 4)]]
        b_mat = [[0], [1]]
        c_mat = [b, 0]
        d_mat = [0]

        return (
            f"H(s) = {h_str}. Convert to controllable canonical form [A,B,C,D].",
            {
                "a0": a0, "a1": a1, "b": b,
                "h_str": h_str,
                "A": a_mat, "B": b_mat, "C": c_mat, "D": d_mat,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for state-space conversion.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the canonical form construction.
        """
        a0, a1, b = data["a0"], data["a1"], data["b"]
        return [
            f"den = s^2 + {_fmt(a1)}*s + {_fmt(a0)}",
            f"A = [[0, 1], [{_fmt(-a0)}, {_fmt(-a1)}]]",
            f"B = [[0], [1]]",
            f"C = [{_fmt(b)}, 0]",
            f"D = [0]",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the state-space matrices.

        Args:
            data: Solution data dict.

        Returns:
            A, B, C, D matrices as a string.
        """
        a = data["A"]
        return (
            f"A = [[{_fmt(a[0][0])}, {_fmt(a[0][1])}], "
            f"[{_fmt(a[1][0])}, {_fmt(a[1][1])}]], "
            f"B = [[0], [1]], "
            f"C = [{_fmt(data['b'])}, 0], D = [0]"
        )


# ---------------------------------------------------------------------------
# 6. Feedback Gain (tier 5)
# ---------------------------------------------------------------------------

@register
class FeedbackGainGenerator(StepGenerator):
    """Compute closed-loop transfer function and poles.

    Given G(s) = Kg/(s + pg) and H(s) = Kh/(s + ph), compute the
    closed-loop TF = G/(1+G*H), find its poles, and compute DC gain.

    Difficulty scaling:
        Difficulty 1-3: H(s) = 1 (unity feedback), integer coefficients.
        Difficulty 4-6: first-order H(s), integer coefficients.
        Difficulty 7-8: first-order H(s), decimal coefficients.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "feedback_gain"

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
        return "compute closed-loop transfer function, poles, and DC gain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a feedback gain problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            kg = self._rng.randint(1, 10)
            pg = self._rng.randint(1, 5)
            kh = 1
            ph = 0
            unity = True
        elif difficulty <= 6:
            kg = self._rng.randint(1, 10)
            pg = self._rng.randint(1, 10)
            kh = self._rng.randint(1, 5)
            ph = self._rng.randint(1, 5)
            unity = False
        else:
            kg = round(self._rng.uniform(1.0, 10.0), 1)
            pg = round(self._rng.uniform(0.5, 10.0), 1)
            kh = round(self._rng.uniform(0.5, 5.0), 1)
            ph = round(self._rng.uniform(0.5, 5.0), 1)
            unity = False

        if unity:
            # CL = Kg/(s + pg + Kg)
            # G/(1+G) = Kg/(s+pg) / (1 + Kg/(s+pg)) = Kg/(s + pg + Kg)
            cl_num = kg
            cl_den_coeffs = [1.0, pg + kg]
            poles = [round(-(pg + kg), 4)]
            dc_gain = round(kg / (pg + kg), 4)
            g_str = f"G(s) = {_fmt(kg)}/(s + {_fmt(pg)})"
            h_str = "H(s) = 1"
            cl_str = f"{_fmt(kg)}/(s + {_fmt(round(pg + kg, 4))})"
        else:
            # G(s) = Kg/(s+pg), H(s) = Kh/(s+ph)
            # GH = Kg*Kh / ((s+pg)(s+ph))
            # 1 + GH = ((s+pg)(s+ph) + Kg*Kh) / ((s+pg)(s+ph))
            # CL = G/(1+GH) = Kg*(s+ph) / ((s+pg)(s+ph) + Kg*Kh)
            # den = s^2 + (pg+ph)*s + (pg*ph + Kg*Kh)
            cl_num_str = f"{_fmt(kg)}*(s + {_fmt(ph)})"
            den_a = 1.0
            den_b = round(pg + ph, 4)
            den_c = round(pg * ph + kg * kh, 4)
            cl_den_coeffs = [den_a, den_b, den_c]
            poles_raw = _quadratic_roots(den_a, den_b, den_c)
            poles = poles_raw
            # DC gain: set s=0: Kg*ph / (pg*ph + Kg*Kh)
            dc_gain = round(kg * ph / den_c, 4) if abs(den_c) > 1e-10 else 0.0
            g_str = f"G(s) = {_fmt(kg)}/(s + {_fmt(pg)})"
            h_str = f"H(s) = {_fmt(kh)}/(s + {_fmt(ph)})"
            cl_str = (f"{cl_num_str}/({_poly_str(cl_den_coeffs)})")

        return (
            f"{g_str}, {h_str}. Compute CL = G/(1+GH), poles, DC gain.",
            {
                "kg": kg, "pg": pg, "kh": kh, "ph": ph,
                "unity": unity,
                "cl_str": cl_str,
                "cl_den_coeffs": cl_den_coeffs,
                "poles": poles,
                "dc_gain": dc_gain,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for feedback gain.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing CL derivation, pole computation, and DC gain.
        """
        steps = []
        if data["unity"]:
            steps.append(
                f"CL = G/(1+G) = {_fmt(data['kg'])}/"
                f"(s + {_fmt(data['pg'])} + {_fmt(data['kg'])})"
            )
            steps.append(f"pole: s = {_fmt(data['poles'][0])}")
        else:
            kg, pg, kh, ph = (data["kg"], data["pg"],
                              data["kh"], data["ph"])
            steps.append(
                f"GH = {_fmt(kg)}*{_fmt(kh)}/((s+{_fmt(pg)})(s+{_fmt(ph)}))"
            )
            den = data["cl_den_coeffs"]
            steps.append(f"CL den = {_poly_str(den)}")
            pole_strs = [_root_fmt(p) for p in data["poles"]]
            steps.append(f"poles: {', '.join(pole_strs)}")

        steps.append(f"DC gain (s=0): {_fmt(data['dc_gain'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the closed-loop result.

        Args:
            data: Solution data dict.

        Returns:
            CL transfer function, poles, and DC gain.
        """
        if data["unity"]:
            pole_str = _fmt(data["poles"][0])
        else:
            pole_str = ", ".join(_root_fmt(p) for p in data["poles"])
        return f"CL = {data['cl_str']}, poles = [{pole_str}], DC = {_fmt(data['dc_gain'])}"
