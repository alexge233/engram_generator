"""Extended control theory generators.

8 generators across tiers 5-6 covering root locus, gain margin,
phase margin, controllability, observability, pole placement,
steady-state error, and second-order response characteristics.
"""
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


# ---------------------------------------------------------------------------
# 1. Root Locus (tier 6)
# ---------------------------------------------------------------------------

@register
class RootLocusGenerator(StepGenerator):
    """Find the breakaway point on the real axis for a root locus.

    For H(s) = K / (s(s + a)), the breakaway point is at s = -a/2,
    found by solving dK/ds = 0 where K = -s(s+a).

    Difficulty scaling:
        d1-3: small integer a, poles at 0 and -a.
        d4-6: medium a values.
        d7-8: decimal a values and gain computation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "root_locus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["feedback_gain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find root locus breakaway point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a second-order system and find the breakaway point.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(2, 6)
        elif difficulty <= 6:
            a = self._rng.randint(4, 15)
        else:
            a = round(self._rng.uniform(2.0, 20.0), 1)
        breakaway = round(-a / 2, 4)
        # K at breakaway: K = -s(s+a) = -(s^2 + as) at s = -a/2
        k_break = round((a / 2) * (a / 2 + a) - (a / 2) ** 2, 4)
        # Simplify: K = (-a/2)^2 + a*(a/2) = a^2/4
        k_break = round(a * a / 4, 4)
        return (
            f"H(s) = K / (s(s + {_fmt(a)})). Find breakaway point.",
            {
                "a": a, "breakaway": breakaway, "k_break": k_break,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate root locus breakaway computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing derivative and breakaway point.
        """
        a = sd["a"]
        return [
            f"poles at s = 0 and s = {_fmt(-a)}",
            f"K = -s(s + {_fmt(a)}) = -(s^2 + {_fmt(a)}s)",
            f"dK/ds = -(2s + {_fmt(a)}) = 0",
            f"s = {_fmt(sd['breakaway'])}",
            f"K at breakaway = {_fmt(sd['k_break'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the breakaway point and gain.

        Args:
            sd: Solution data dict.

        Returns:
            Breakaway point and K value.
        """
        return f"s = {_fmt(sd['breakaway'])}, K = {_fmt(sd['k_break'])}"


# ---------------------------------------------------------------------------
# 2. Gain Margin (tier 6)
# ---------------------------------------------------------------------------

@register
class GainMarginGenerator(StepGenerator):
    """Compute the gain margin of a first-order system with delay.

    For H(s) = K / (s + a), find the phase crossover frequency where
    phase = -180 degrees. For a simple first-order system without
    delay, phase never reaches -180, so we use H(s) = K / (s+a)(s+b)
    which reaches -180 at w = sqrt(ab). GM = 1/|H(jw_pc)| in dB.

    Difficulty scaling:
        d1-3: integer a, b, K.
        d4-6: medium values.
        d7-8: decimal coefficients.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gain_margin"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bode_magnitude"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute gain margin"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a system and compute the gain margin.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.randint(1, 5)
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
        elif difficulty <= 6:
            k = self._rng.randint(1, 10)
            a = self._rng.randint(1, 10)
            b = self._rng.randint(1, 10)
        else:
            k = round(self._rng.uniform(1.0, 10.0), 1)
            a = round(self._rng.uniform(1.0, 10.0), 1)
            b = round(self._rng.uniform(1.0, 10.0), 1)
        # For H(s) = K/((s+a)(s+b)), phase crossover at w_pc = sqrt(a*b)
        w_pc = round(math.sqrt(a * b), 4)
        # |H(jw_pc)| = K / sqrt((w_pc^2 + a^2)(w_pc^2 + b^2))
        mag_den = math.sqrt((w_pc ** 2 + a ** 2) * (w_pc ** 2 + b ** 2))
        h_mag = round(k / mag_den, 4) if mag_den > 1e-10 else 0.0
        gm_linear = round(1 / h_mag, 4) if h_mag > 1e-10 else float("inf")
        gm_db = round(20 * math.log10(gm_linear), 4) if gm_linear > 0 and gm_linear != float("inf") else float("inf")
        return (
            f"H(s) = {_fmt(k)}/((s+{_fmt(a)})(s+{_fmt(b)})). Gain margin?",
            {
                "k": k, "a": a, "b": b,
                "w_pc": w_pc, "h_mag": h_mag,
                "gm_linear": gm_linear, "gm_db": gm_db,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate gain margin computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing phase crossover frequency and GM.
        """
        return [
            f"phase crossover: w_pc = sqrt({_fmt(sd['a'])}*{_fmt(sd['b'])}) = {_fmt(sd['w_pc'])}",
            f"|H(jw_pc)| = {_fmt(sd['h_mag'])}",
            f"GM = 1/{_fmt(sd['h_mag'])} = {_fmt(sd['gm_linear'])}",
            f"GM = 20*log10({_fmt(sd['gm_linear'])}) = {_fmt(sd['gm_db'])} dB",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the gain margin.

        Args:
            sd: Solution data dict.

        Returns:
            GM in dB.
        """
        return f"GM = {_fmt(sd['gm_db'])} dB"


# ---------------------------------------------------------------------------
# 3. Phase Margin (tier 6)
# ---------------------------------------------------------------------------

@register
class PhaseMarginGenerator(StepGenerator):
    """Compute the phase margin of a system.

    For H(s) = K / (s+a), find w_gc where |H(jw)| = 1, then
    PM = 180 + angle(H(jw_gc)).

    Difficulty scaling:
        d1-3: simple first-order, integer K, a.
        d4-6: medium values.
        d7-8: decimal K, a.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phase_margin"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bode_magnitude"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute phase margin"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a first-order system and compute the phase margin.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.randint(2, 8)
            a = self._rng.randint(1, 5)
        elif difficulty <= 6:
            k = self._rng.randint(5, 20)
            a = self._rng.randint(1, 10)
        else:
            k = round(self._rng.uniform(5.0, 30.0), 1)
            a = round(self._rng.uniform(1.0, 10.0), 1)
        # |H(jw)| = K / sqrt(w^2 + a^2) = 1 => w_gc = sqrt(K^2 - a^2)
        k_sq = k * k
        a_sq = a * a
        if k_sq <= a_sq:
            # Gain too low for unity crossover, margin is infinite
            w_gc = 0.0
            pm = 180.0
        else:
            w_gc = round(math.sqrt(k_sq - a_sq), 4)
            # phase(H(jw)) = -arctan(w/a) for first-order
            phase_deg = round(-math.degrees(math.atan2(w_gc, a)), 4)
            pm = round(180 + phase_deg, 4)
        return (
            f"H(s) = {_fmt(k)}/(s+{_fmt(a)}). Phase margin?",
            {
                "k": k, "a": a, "w_gc": w_gc, "pm": pm,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate phase margin computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing gain crossover and phase computation.
        """
        if sd["w_gc"] == 0:
            return [
                f"|H(jw)| < 1 for all w (K < a)",
                f"PM = 180 degrees (always stable)",
            ]
        phase = round(sd["pm"] - 180, 4)
        return [
            f"|H(jw)| = 1: {_fmt(sd['k'])}/sqrt(w^2+{_fmt(sd['a'])}^2) = 1",
            f"w_gc = sqrt({_fmt(sd['k'])}^2 - {_fmt(sd['a'])}^2) = {_fmt(sd['w_gc'])}",
            f"phase = -arctan({_fmt(sd['w_gc'])}/{_fmt(sd['a'])}) = {_fmt(phase)} deg",
            f"PM = 180 + ({_fmt(phase)}) = {_fmt(sd['pm'])} deg",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the phase margin.

        Args:
            sd: Solution data dict.

        Returns:
            PM in degrees.
        """
        return f"PM = {_fmt(sd['pm'])} deg"


# ---------------------------------------------------------------------------
# 4. Controllability (tier 6)
# ---------------------------------------------------------------------------

@register
class ControllabilityGenerator(StepGenerator):
    """Check controllability of a 2x2 state-space system.

    Builds the controllability matrix C = [B, AB] and checks if
    its rank equals 2 (full rank) for the system to be controllable.

    Difficulty scaling:
        d1-3: small integer A, B matrices.
        d4-6: medium integer values.
        d7-8: values that may produce rank-deficient matrices.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "controllability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["state_space"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check controllability of 2x2 system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate A and B matrices and check controllability.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 2 + difficulty
        a = [[self._rng.randint(-r, r) for _ in range(2)] for _ in range(2)]
        b = [[self._rng.randint(-r, r)] for _ in range(2)]
        # AB = A * B
        ab = [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0]],
        ]
        # Controllability matrix C_mat = [B | AB]
        c_mat = [
            [b[0][0], ab[0][0]],
            [b[1][0], ab[1][0]],
        ]
        # Determinant
        det = c_mat[0][0] * c_mat[1][1] - c_mat[0][1] * c_mat[1][0]
        controllable = abs(det) > 1e-10
        a_str = f"[[{a[0][0]},{a[0][1]}],[{a[1][0]},{a[1][1]}]]"
        b_str = f"[[{b[0][0]}],[{b[1][0]}]]"
        return (
            f"A={a_str}, B={b_str}. Controllable?",
            {
                "A": a, "B": b, "AB": ab,
                "C_mat": c_mat, "det": det,
                "controllable": controllable,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate controllability check steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing AB computation, controllability matrix, and rank.
        """
        ab = sd["AB"]
        c_m = sd["C_mat"]
        return [
            f"AB = [[{ab[0][0]}],[{ab[1][0]}]]",
            f"C = [B|AB] = [[{c_m[0][0]},{c_m[0][1]}],[{c_m[1][0]},{c_m[1][1]}]]",
            f"det(C) = {c_m[0][0]}*{c_m[1][1]} - {c_m[0][1]}*{c_m[1][0]} = {_fmt(sd['det'])}",
            f"rank = {'2 (full)' if sd['controllable'] else '< 2 (deficient)'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the controllability verdict.

        Args:
            sd: Solution data dict.

        Returns:
            Controllable or not.
        """
        return "controllable" if sd["controllable"] else "not controllable"


# ---------------------------------------------------------------------------
# 5. Observability (tier 6)
# ---------------------------------------------------------------------------

@register
class ObservabilityGenerator(StepGenerator):
    """Check observability of a 2x2 state-space system.

    Builds the observability matrix O = [C; CA] and checks if
    its rank equals 2 for the system to be observable.

    Difficulty scaling:
        d1-3: small integer A, C matrices.
        d4-6: medium integer values.
        d7-8: values that may produce rank-deficient matrices.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "observability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["state_space"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check observability of 2x2 system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate A and C matrices and check observability.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 2 + difficulty
        a = [[self._rng.randint(-r, r) for _ in range(2)] for _ in range(2)]
        c = [[self._rng.randint(-r, r), self._rng.randint(-r, r)]]
        # CA = C * A
        ca = [[
            c[0][0] * a[0][0] + c[0][1] * a[1][0],
            c[0][0] * a[0][1] + c[0][1] * a[1][1],
        ]]
        # Observability matrix O = [C; CA] (2x2)
        o_mat = [
            [c[0][0], c[0][1]],
            [ca[0][0], ca[0][1]],
        ]
        det = o_mat[0][0] * o_mat[1][1] - o_mat[0][1] * o_mat[1][0]
        observable = abs(det) > 1e-10
        a_str = f"[[{a[0][0]},{a[0][1]}],[{a[1][0]},{a[1][1]}]]"
        c_str = f"[{c[0][0]},{c[0][1]}]"
        return (
            f"A={a_str}, C={c_str}. Observable?",
            {
                "A": a, "C": c, "CA": ca,
                "O_mat": o_mat, "det": det,
                "observable": observable,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate observability check steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing CA computation, observability matrix, and rank.
        """
        ca = sd["CA"]
        o_m = sd["O_mat"]
        return [
            f"CA = [{ca[0][0]},{ca[0][1]}]",
            f"O = [C; CA] = [[{o_m[0][0]},{o_m[0][1]}],[{o_m[1][0]},{o_m[1][1]}]]",
            f"det(O) = {o_m[0][0]}*{o_m[1][1]} - {o_m[0][1]}*{o_m[1][0]} = {_fmt(sd['det'])}",
            f"rank = {'2 (full)' if sd['observable'] else '< 2 (deficient)'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the observability verdict.

        Args:
            sd: Solution data dict.

        Returns:
            Observable or not.
        """
        return "observable" if sd["observable"] else "not observable"


# ---------------------------------------------------------------------------
# 6. Pole Placement (tier 6)
# ---------------------------------------------------------------------------

@register
class PolePlacementGenerator(StepGenerator):
    """Design state feedback gain K for desired pole placement.

    For a 2x2 system with A and B, find K = [k1, k2] such that
    the eigenvalues of (A - BK) match desired poles.

    Difficulty scaling:
        d1-3: diagonal A, desired poles as negative integers.
        d4-6: general A, integer desired poles.
        d7-8: general A, decimal desired poles.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pole_placement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "design state feedback for desired poles"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate system matrices and desired poles, solve for K.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Use controllable canonical form for clean solution
        if difficulty <= 3:
            a0 = self._rng.randint(1, 5)
            a1 = self._rng.randint(1, 5)
            p1 = -self._rng.randint(1, 5)
            p2 = -self._rng.randint(1, 5)
        elif difficulty <= 6:
            a0 = self._rng.randint(1, 10)
            a1 = self._rng.randint(1, 10)
            p1 = -self._rng.randint(1, 10)
            p2 = -self._rng.randint(1, 10)
        else:
            a0 = round(self._rng.uniform(1.0, 10.0), 1)
            a1 = round(self._rng.uniform(1.0, 10.0), 1)
            p1 = round(-self._rng.uniform(1.0, 10.0), 1)
            p2 = round(-self._rng.uniform(1.0, 10.0), 1)
        # A in controllable canonical form: [[0, 1], [-a0, -a1]], B = [[0],[1]]
        a_mat = [[0, 1], [-a0, -a1]]
        b_mat = [[0], [1]]
        # Desired char poly: (s-p1)(s-p2) = s^2 - (p1+p2)s + p1*p2
        # = s^2 + alpha1*s + alpha0
        alpha1 = round(-(p1 + p2), 4)
        alpha0 = round(p1 * p2, 4)
        # For CCF: K = [alpha0 - a0, alpha1 - a1]
        k1 = round(alpha0 - (-a0), 4)  # alpha0 + a0
        k2 = round(alpha1 - (-a1), 4)  # alpha1 + a1
        # Correct: det(sI - A + BK) desired coefficients
        # A-BK = [[0,1],[-a0-k1, -a1-k2]]
        # char poly: s^2 + (a1+k2)s + (a0+k1) = s^2 + alpha1*s + alpha0
        k1 = round(alpha0 - a0, 4)
        k2 = round(alpha1 - a1, 4)
        return (
            f"A=[[0,1],[{_fmt(-a0)},{_fmt(-a1)}]], B=[[0],[1]]. "
            f"Desired poles: {_fmt(p1)}, {_fmt(p2)}.",
            {
                "A": a_mat, "a0": a0, "a1": a1,
                "p1": p1, "p2": p2,
                "alpha0": alpha0, "alpha1": alpha1,
                "k1": k1, "k2": k2,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate pole placement computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing desired characteristic polynomial and K.
        """
        return [
            f"desired poly: (s-{_fmt(sd['p1'])})(s-{_fmt(sd['p2'])}) = s^2 + {_fmt(sd['alpha1'])}s + {_fmt(sd['alpha0'])}",
            f"current poly: s^2 + {_fmt(sd['a1'])}s + {_fmt(sd['a0'])}",
            f"K = [{_fmt(sd['alpha0'])} - {_fmt(sd['a0'])}, {_fmt(sd['alpha1'])} - {_fmt(sd['a1'])}]",
            f"K = [{_fmt(sd['k1'])}, {_fmt(sd['k2'])}]",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the feedback gain vector.

        Args:
            sd: Solution data dict.

        Returns:
            K as a vector.
        """
        return f"K = [{_fmt(sd['k1'])}, {_fmt(sd['k2'])}]"


# ---------------------------------------------------------------------------
# 7. Steady-State Error (tier 5)
# ---------------------------------------------------------------------------

@register
class SteadyStateErrorGenerator(StepGenerator):
    """Compute steady-state error for step and ramp inputs.

    For a type-N system: e_ss = 1/(1+Kp) for step input,
    e_ss = 1/Kv for ramp input. System type determined by number
    of free integrators.

    Difficulty scaling:
        d1-3: type 0 system, step input only.
        d4-6: type 1 system, step and ramp inputs.
        d7-8: type 0 or 1, decimal gain values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "steady_state_error"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["feedback_gain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute steady-state error"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a system and compute steady-state error.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Type 0: G(s) = K / (s + a)
            sys_type = 0
            k = self._rng.randint(2, 10)
            a = self._rng.randint(1, 5)
            kp = round(k / a, 4)  # position error constant
            e_step = round(1 / (1 + kp), 4)
            e_ramp = float("inf")
            problem = f"G(s) = {k}/(s+{a}), unity feedback. e_ss for step?"
        elif difficulty <= 6:
            # Type 1: G(s) = K / (s(s + a))
            sys_type = 1
            k = self._rng.randint(2, 15)
            a = self._rng.randint(1, 10)
            kp = float("inf")
            kv = round(k / a, 4)  # velocity error constant
            e_step = 0.0
            e_ramp = round(1 / kv, 4)
            problem = f"G(s) = {k}/(s(s+{a})), unity feedback. e_ss for step and ramp?"
        else:
            sys_type = self._rng.choice([0, 1])
            k = round(self._rng.uniform(2.0, 20.0), 1)
            a = round(self._rng.uniform(1.0, 10.0), 1)
            if sys_type == 0:
                kp = round(k / a, 4)
                e_step = round(1 / (1 + kp), 4)
                e_ramp = float("inf")
                problem = f"G(s) = {_fmt(k)}/(s+{_fmt(a)}), unity feedback. e_ss?"
            else:
                kp = float("inf")
                kv = round(k / a, 4)
                e_step = 0.0
                e_ramp = round(1 / kv, 4)
                problem = f"G(s) = {_fmt(k)}/(s(s+{_fmt(a)})), unity feedback. e_ss?"
        sd = {
            "sys_type": sys_type, "k": k, "a": a,
            "e_step": e_step, "e_ramp": e_ramp,
        }
        if sys_type == 0:
            sd["kp"] = kp
        else:
            sd["kv"] = kv
        return problem, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate steady-state error computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing system type and error constants.
        """
        steps = [f"system type = {sd['sys_type']}"]
        if sd["sys_type"] == 0:
            steps.append(f"Kp = lim s->0 G(s) = {_fmt(sd['k'])}/{_fmt(sd['a'])} = {_fmt(sd['kp'])}")
            steps.append(f"e_step = 1/(1+{_fmt(sd['kp'])}) = {_fmt(sd['e_step'])}")
            steps.append("e_ramp = inf (type 0)")
        else:
            steps.append(f"Kv = lim s->0 s*G(s) = {_fmt(sd['k'])}/{_fmt(sd['a'])} = {_fmt(sd['kv'])}")
            steps.append("e_step = 0 (type 1)")
            steps.append(f"e_ramp = 1/{_fmt(sd['kv'])} = {_fmt(sd['e_ramp'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the steady-state errors.

        Args:
            sd: Solution data dict.

        Returns:
            Step and ramp errors.
        """
        e_r = "inf" if sd["e_ramp"] == float("inf") else _fmt(sd["e_ramp"])
        return f"e_step = {_fmt(sd['e_step'])}, e_ramp = {e_r}"


# ---------------------------------------------------------------------------
# 8. Second Order Response (tier 5)
# ---------------------------------------------------------------------------

@register
class SecondOrderResponseGenerator(StepGenerator):
    """Extract second-order response characteristics.

    From denominator s^2 + 2*zeta*omega_n*s + omega_n^2, compute
    natural frequency, damping ratio, percent overshoot, settling
    time (2% criterion), and peak time.

    Difficulty scaling:
        d1-3: integer omega_n, zeta < 1 (underdamped).
        d4-6: decimal omega_n, wider zeta range.
        d7-8: zeta near critical damping boundary.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "second_order_response"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["transfer_function_sys"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "extract second-order response characteristics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate second-order coefficients and compute response metrics.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            wn = float(self._rng.randint(2, 10))
            zeta = round(self._rng.uniform(0.1, 0.7), 2)
        elif difficulty <= 6:
            wn = round(self._rng.uniform(2.0, 20.0), 1)
            zeta = round(self._rng.uniform(0.1, 0.9), 2)
        else:
            wn = round(self._rng.uniform(2.0, 30.0), 1)
            zeta = round(self._rng.uniform(0.3, 0.99), 2)
        # Coefficients: s^2 + 2*zeta*wn*s + wn^2
        coeff_s = round(2 * zeta * wn, 4)
        coeff_0 = round(wn * wn, 4)
        # Response characteristics (underdamped: zeta < 1)
        if zeta < 1:
            wd = round(wn * math.sqrt(1 - zeta * zeta), 4)
            overshoot = round(100 * math.exp(-math.pi * zeta / math.sqrt(1 - zeta * zeta)), 4)
            t_peak = round(math.pi / wd, 4)
            t_settle = round(4 / (zeta * wn), 4)
        else:
            wd = 0.0
            overshoot = 0.0
            t_peak = 0.0
            t_settle = round(4 / (zeta * wn), 4)
        return (
            f"s^2 + {_fmt(coeff_s)}s + {_fmt(coeff_0)} = 0. Response characteristics?",
            {
                "wn": wn, "zeta": zeta, "wd": wd,
                "overshoot": overshoot, "t_peak": t_peak,
                "t_settle": t_settle,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate response characteristics computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing extraction and computation.
        """
        steps = [
            f"omega_n = {_fmt(sd['wn'])}, zeta = {_fmt(sd['zeta'])}",
        ]
        if sd["zeta"] < 1:
            steps.append(f"omega_d = {_fmt(sd['wn'])}*sqrt(1-{_fmt(sd['zeta'])}^2) = {_fmt(sd['wd'])}")
            steps.append(f"overshoot = 100*exp(-pi*{_fmt(sd['zeta'])}/sqrt(1-{_fmt(sd['zeta'])}^2)) = {_fmt(sd['overshoot'])}%")
            steps.append(f"t_peak = pi/{_fmt(sd['wd'])} = {_fmt(sd['t_peak'])} s")
        else:
            steps.append("overdamped: no overshoot")
        steps.append(f"t_settle (2%) = 4/({_fmt(sd['zeta'])}*{_fmt(sd['wn'])}) = {_fmt(sd['t_settle'])} s")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the response characteristics.

        Args:
            sd: Solution data dict.

        Returns:
            Key response metrics.
        """
        return (
            f"wn={_fmt(sd['wn'])}, zeta={_fmt(sd['zeta'])}, "
            f"OS={_fmt(sd['overshoot'])}%, Ts={_fmt(sd['t_settle'])}s"
        )
