"""Quantum mechanics generators -- energy levels through spin addition.

Covers particle-in-a-box energy levels, Heisenberg uncertainty,
commutator computation for 2x2 matrices, angular momentum quantum
numbers, spin addition rules, and hydrogen atom energy/transitions.
Tiers range from 5 (introductory quantum) to 6 (commutators, spin).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class QuantumFormatter:
    """Formats numbers for quantum mechanics calculations.

    Provides scientific notation for very small physical constants
    and clean decimal formatting for energy values and wavelengths.
    """

    @staticmethod
    def format_sci(value: float, sig_figs: int = 4) -> str:
        """Format a number in LaTeX scientific notation.

        Args:
            value: Number to format.
            sig_figs: Significant figures to retain.

        Returns:
            LaTeX scientific notation string.
        """
        if value == 0:
            return "0"
        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = round(value / (10 ** exponent), sig_figs - 1)
        sign = "-" if value < 0 else ""
        return f"{sign}{abs(mantissa)} \\times 10^{{{exponent}}}"

    @staticmethod
    def format_value(value: float, decimals: int = 4) -> str:
        """Format a numeric value, removing unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


class PauliMatrix:
    """Represents a named 2x2 matrix for commutator calculations.

    Stores integer matrix entries and provides multiplication and
    subtraction operations needed for computing commutators [A,B].

    Attributes:
        name: Display name of the matrix.
        m: 2x2 integer matrix as nested lists.
    """

    def __init__(self, name: str, m: list[list[int]]) -> None:
        """Initialise with a name and 2x2 integer matrix.

        Args:
            name: Matrix display name (e.g. 'sigma_x').
            m: 2x2 matrix as [[a,b],[c,d]].
        """
        self._name = name
        self._m = m

    @property
    def name(self) -> str:
        """Return the matrix display name."""
        return self._name

    @property
    def m(self) -> list[list[int]]:
        """Return the 2x2 integer matrix."""
        return self._m

    def multiply(self, other: "PauliMatrix") -> list[list[int]]:
        """Multiply this matrix by another (2x2 integer multiplication).

        Args:
            other: The right-hand matrix.

        Returns:
            2x2 result matrix as nested lists.
        """
        a = self._m
        b = other.m
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0],
             a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0],
             a[1][0] * b[0][1] + a[1][1] * b[1][1]],
        ]

    def to_latex(self) -> str:
        """Format the matrix in LaTeX pmatrix notation.

        Returns:
            LaTeX string for the 2x2 matrix.
        """
        rows = [" & ".join(str(v) for v in row) for row in self._m]
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


def _mat_subtract(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    """Subtract two 2x2 integer matrices element-wise.

    Args:
        a: First 2x2 matrix.
        b: Second 2x2 matrix.

    Returns:
        Element-wise difference a - b.
    """
    return [
        [a[0][0] - b[0][0], a[0][1] - b[0][1]],
        [a[1][0] - b[1][0], a[1][1] - b[1][1]],
    ]


def _mat_latex(m: list[list[int]]) -> str:
    """Format a 2x2 integer matrix in LaTeX pmatrix notation.

    Args:
        m: 2x2 matrix as nested lists.

    Returns:
        LaTeX pmatrix string.
    """
    rows = [" & ".join(str(v) for v in row) for row in m]
    body = " \\\\ ".join(rows)
    return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


# ---------------------------------------------------------------------------
# Generator 1: Particle in a box (Schrodinger 1D)
# ---------------------------------------------------------------------------
@register
class Schrodinger1DGenerator(StepGenerator):
    """Particle-in-a-box energy: E_n = n^2 h^2 / (8 m L^2).

    Computes energy levels for a quantum particle confined to a
    one-dimensional box of length L using Planck's constant
    h = 6.626e-34 J s and electron mass m = 9.109e-31 kg.

    Input format:
        ``compute particle-in-a-box energy level``

    Target format:
        ``E_n = \\frac{n^2 h^2}{8mL^2} <step> n=2, L=1e-10 m
        <step> n^2=4 <step> h^2=4.3904e-67
        <step> 8mL^2=7.2872e-50
        <step> E_n=2.4109e-17 J``

    Difficulty scaling:
        Difficulty 1-3: n in [1,3], L in [1e-10, 5e-10].
        Difficulty 4-6: n in [1,5], L in [5e-11, 5e-10].
        Difficulty 7-8: n in [1,8], L in [1e-11, 5e-10].

    Prerequisites:
        exponentiation.

    Example:
        >>> gen = Schrodinger1DGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'schrodinger_1d'
    """

    _H = 6.626e-34
    _M = 9.109e-31

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "schrodinger_1d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls quantum number and box size.

        Returns:
            Natural language description.
        """
        return "compute particle-in-a-box energy level"

    def _sample_parameters(self, difficulty: int) -> tuple[int, float]:
        """Sample quantum number n and box length L.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n, L_metres).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 3)
            l_exp = self._rng.choice([-10, -10, -10])
            l_mantissa = self._rng.randint(1, 5)
        elif difficulty <= 6:
            n = self._rng.randint(1, 5)
            l_exp = self._rng.choice([-11, -10])
            l_mantissa = self._rng.randint(1, 9)
        else:
            n = self._rng.randint(1, 8)
            l_exp = self._rng.choice([-11, -10])
            l_mantissa = self._rng.randint(1, 9)
        length = l_mantissa * (10.0 ** l_exp)
        return n, length

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a particle-in-a-box energy problem.

        Args:
            difficulty: Controls n and L ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n, length = self._sample_parameters(difficulty)
        n_sq = n * n
        h_sq = self._H ** 2
        l_sq = length ** 2
        denominator = 8.0 * self._M * l_sq
        energy = n_sq * h_sq / denominator

        return "E_n = \\frac{n^2 h^2}{8mL^2}", {
            "n": n, "L": length, "n_sq": n_sq,
            "h_sq": h_sq, "l_sq": l_sq,
            "denominator": denominator, "energy": energy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for the energy level.

        Args:
            data: Solution data with n, L, and intermediates.

        Returns:
            Steps showing squaring, numerator, denominator, and result.
        """
        fmt = QuantumFormatter
        return [
            f"n={data['n']}, L={fmt.format_sci(data['L'])} m",
            f"n^2={data['n_sq']}",
            f"h^2={fmt.format_sci(data['h_sq'])}",
            f"8mL^2={fmt.format_sci(data['denominator'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the energy level.

        Args:
            data: Solution data.

        Returns:
            String representation of E_n with units.
        """
        return f"E_n={QuantumFormatter.format_sci(data['energy'])} J"


# ---------------------------------------------------------------------------
# Generator 2: Heisenberg uncertainty
# ---------------------------------------------------------------------------
@register
class UncertaintyComputeGenerator(StepGenerator):
    """Heisenberg uncertainty: dx * dp >= hbar/2.

    Given a position uncertainty dx, computes the minimum momentum
    uncertainty dp_min = hbar / (2 * dx) using hbar = 1.055e-34 J s.
    Alternatively verifies whether a given (dx, dp) pair satisfies
    the uncertainty relation.

    Input format:
        ``compute minimum momentum uncertainty``

    Target format:
        ``\\Delta x \\Delta p \\geq \\frac{\\hbar}{2} <step>
        \\Delta x = 1e-10 m <step>
        \\hbar/2 = 5.2750e-35 <step>
        \\Delta p_{min} = 5.2750e-25 kg m/s``

    Difficulty scaling:
        Difficulty 1-3: dx in [1e-10, 9e-10] (atomic scale).
        Difficulty 4-6: dx in [1e-11, 9e-11] (sub-atomic).
        Difficulty 7-8: dx in [1e-12, 9e-12] (nuclear scale).

    Prerequisites:
        division.

    Example:
        >>> gen = UncertaintyComputeGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'uncertainty_compute'
    """

    _HBAR = 1.055e-34

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "uncertainty_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls position uncertainty scale.

        Returns:
            Natural language description.
        """
        return "compute minimum momentum uncertainty"

    def _sample_dx(self, difficulty: int) -> float:
        """Sample a position uncertainty based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Position uncertainty in metres.
        """
        if difficulty <= 3:
            exp = -10
        elif difficulty <= 6:
            exp = -11
        else:
            exp = -12
        mantissa = self._rng.randint(1, 9)
        return mantissa * (10.0 ** exp)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an uncertainty relation problem.

        Args:
            difficulty: Controls dx scale.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        dx = self._sample_dx(difficulty)
        hbar_half = self._HBAR / 2.0
        dp_min = hbar_half / dx

        formula = "\\Delta x \\Delta p \\geq \\frac{\\hbar}{2}"
        return formula, {
            "dx": dx, "hbar_half": hbar_half, "dp_min": dp_min,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for minimum dp.

        Args:
            data: Solution data with dx and dp_min.

        Returns:
            Steps showing hbar/2, dx, and dp_min.
        """
        fmt = QuantumFormatter
        return [
            f"\\Delta x = {fmt.format_sci(data['dx'])} m",
            f"\\hbar/2 = {fmt.format_sci(data['hbar_half'])}",
            f"\\Delta p_{{min}} = \\frac{{\\hbar/2}}{{\\Delta x}}"
            f" = \\frac{{{fmt.format_sci(data['hbar_half'])}}}"
            f"{{{fmt.format_sci(data['dx'])}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the minimum momentum uncertainty.

        Args:
            data: Solution data.

        Returns:
            String representation of dp_min with units.
        """
        return (
            f"\\Delta p_{{min}}="
            f"{QuantumFormatter.format_sci(data['dp_min'])} kg m/s"
        )


# ---------------------------------------------------------------------------
# Generator 3: Commutator of 2x2 matrices
# ---------------------------------------------------------------------------
@register
class CommutatorComputeGenerator(StepGenerator):
    """Commutator [A,B] = AB - BA for 2x2 matrices.

    Computes the commutator of two 2x2 matrices chosen from the
    Pauli matrices (sigma_x, sigma_y, sigma_z) and simple operators.
    Shows both products AB and BA before subtracting.

    Input format:
        ``compute matrix commutator [A,B]``

    Target format:
        ``[A,B] = AB - BA <step> A=sigma_x, B=sigma_y
        <step> AB = (0 -1 ; 1 0) <step> BA = (0 1 ; -1 0)
        <step> [A,B] = (0 -2 ; 2 0)``

    Difficulty scaling:
        Difficulty 1-3: Pauli pairs (sigma_x, sigma_y, sigma_z).
        Difficulty 4-6: includes identity and diagonal matrices.
        Difficulty 7-8: random 2x2 integer matrices with entries in [-3,3].

    Prerequisites:
        matrix_multiply.

    Example:
        >>> gen = CommutatorComputeGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'commutator_compute'
    """

    _PAULI_POOL: list[tuple[str, list[list[int]]]] = [
        ("\\sigma_x", [[0, 1], [1, 0]]),
        ("\\sigma_y", [[0, -1], [1, 0]]),
        ("\\sigma_z", [[1, 0], [0, -1]]),
    ]

    _EXTRA_POOL: list[tuple[str, list[list[int]]]] = [
        ("I", [[1, 0], [0, 1]]),
        ("D", [[1, 0], [0, 2]]),
        ("T", [[0, 1], [0, 0]]),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "commutator_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls matrix selection.

        Returns:
            Natural language description.
        """
        return "compute matrix commutator [A,B]"

    def _select_matrices(
        self, difficulty: int
    ) -> tuple[PauliMatrix, PauliMatrix]:
        """Select two distinct matrices for the commutator.

        Args:
            difficulty: Controls pool of available matrices.

        Returns:
            Tuple of two PauliMatrix instances.
        """
        if difficulty <= 3:
            pool = list(self._PAULI_POOL)
        elif difficulty <= 6:
            pool = list(self._PAULI_POOL) + list(self._EXTRA_POOL)
        else:
            name_a = "A"
            name_b = "B"
            mat_a = [
                [self._rng.randint(-3, 3), self._rng.randint(-3, 3)],
                [self._rng.randint(-3, 3), self._rng.randint(-3, 3)],
            ]
            mat_b = [
                [self._rng.randint(-3, 3), self._rng.randint(-3, 3)],
                [self._rng.randint(-3, 3), self._rng.randint(-3, 3)],
            ]
            return PauliMatrix(name_a, mat_a), PauliMatrix(name_b, mat_b)

        a_name, a_mat = self._rng.choice(pool)
        remaining = [(n, m) for n, m in pool if n != a_name]
        if not remaining:
            remaining = pool
        b_name, b_mat = self._rng.choice(remaining)
        return PauliMatrix(a_name, a_mat), PauliMatrix(b_name, b_mat)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a commutator problem for two 2x2 matrices.

        Args:
            difficulty: Controls matrix selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mat_a, mat_b = self._select_matrices(difficulty)
        ab = mat_a.multiply(mat_b)
        ba = mat_b.multiply(mat_a)
        comm = _mat_subtract(ab, ba)

        problem = f"[{mat_a.name},{mat_b.name}]"
        return problem, {
            "A": mat_a, "B": mat_b,
            "AB": ab, "BA": ba, "comm": comm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matrix multiplication and subtraction steps.

        Args:
            data: Solution data with A, B, AB, BA, commutator.

        Returns:
            Steps showing AB, BA, and AB - BA.
        """
        mat_a = data["A"]
        mat_b = data["B"]
        return [
            f"A={mat_a.name}={mat_a.to_latex()}",
            f"B={mat_b.name}={mat_b.to_latex()}",
            f"AB={_mat_latex(data['AB'])}",
            f"BA={_mat_latex(data['BA'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the commutator matrix.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for [A,B].
        """
        return f"[A,B]={_mat_latex(data['comm'])}"


# ---------------------------------------------------------------------------
# Generator 4: Angular momentum quantum numbers
# ---------------------------------------------------------------------------
@register
class AngularMomentumQNGenerator(StepGenerator):
    """Angular momentum: L^2 = l(l+1) hbar^2, L_z = m hbar.

    Given orbital quantum number l, computes the magnitude squared
    L^2 and lists all allowed L_z values for m in {-l, ..., +l}.
    Uses hbar = 1.055e-34 J s.

    Input format:
        ``compute angular momentum quantum numbers``

    Target format:
        ``l=2 <step> L^2 = l(l+1)hbar^2 = 6 hbar^2 = 6.6782e-68
        <step> m = {-2,-1,0,1,2}
        <step> L_z = m*hbar for each m``

    Difficulty scaling:
        Difficulty 1-3: l in [0, 2].
        Difficulty 4-6: l in [0, 4].
        Difficulty 7-8: l in [0, 6].

    Prerequisites:
        exponentiation.

    Example:
        >>> gen = AngularMomentumQNGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'angular_momentum_qn'
    """

    _HBAR = 1.055e-34

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "angular_momentum_qn"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls l range.

        Returns:
            Natural language description.
        """
        return "compute angular momentum quantum numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an angular momentum problem for a given l.

        Args:
            difficulty: Controls l range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            l_val = self._rng.randint(0, 2)
        elif difficulty <= 6:
            l_val = self._rng.randint(0, 4)
        else:
            l_val = self._rng.randint(0, 6)

        l_l_plus_1 = l_val * (l_val + 1)
        hbar_sq = self._HBAR ** 2
        l_squared = l_l_plus_1 * hbar_sq
        m_values = list(range(-l_val, l_val + 1))
        lz_values = [round(m * self._HBAR, 4) for m in m_values]

        problem = f"l={l_val}"
        return problem, {
            "l": l_val, "l_l_plus_1": l_l_plus_1,
            "hbar_sq": hbar_sq, "L_squared": l_squared,
            "m_values": m_values, "Lz_values": lz_values,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate angular momentum computation steps.

        Args:
            data: Solution data with l, L^2, and m values.

        Returns:
            Steps showing L^2 and L_z values.
        """
        fmt = QuantumFormatter
        l_val = data["l"]
        ll1 = data["l_l_plus_1"]
        m_str = ",".join(str(m) for m in data["m_values"])
        return [
            f"L^2 = l(l+1)\\hbar^2 = {l_val}({l_val + 1})\\hbar^2"
            f" = {ll1}\\hbar^2",
            f"L^2 = {fmt.format_sci(data['L_squared'])} J^2 s^2",
            f"m \\in {{{m_str}}}",
            f"L_z = m\\hbar for each m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return L^2 and the set of m values.

        Args:
            data: Solution data.

        Returns:
            String with L^2 and allowed m values.
        """
        fmt = QuantumFormatter
        m_str = ",".join(str(m) for m in data["m_values"])
        return (
            f"L^2={fmt.format_sci(data['L_squared'])}, "
            f"m={{{m_str}}}"
        )


# ---------------------------------------------------------------------------
# Generator 5: Spin addition
# ---------------------------------------------------------------------------
@register
class SpinAdditionGenerator(StepGenerator):
    """Addition of angular momenta: j from |j1-j2| to j1+j2.

    Given two angular momentum quantum numbers j1 and j2, computes
    the range of total angular momentum j values and the total
    number of states sum(2j+1).

    Input format:
        ``compute spin addition j1+j2``

    Target format:
        ``j1=1, j2=1/2 <step> j_min=|1-1/2|=1/2
        <step> j_max=1+1/2=3/2 <step> j in {1/2, 3/2}
        <step> states: (2*1/2+1)+(2*3/2+1)=2+4=6``

    Difficulty scaling:
        Difficulty 1-3: half-integer j values up to 3/2.
        Difficulty 4-6: j values up to 5/2.
        Difficulty 7-8: j values up to 7/2.

    Prerequisites:
        angular_momentum_qn.

    Example:
        >>> gen = SpinAdditionGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'spin_addition'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "spin_addition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["angular_momentum_qn"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls j value ranges.

        Returns:
            Natural language description.
        """
        return "compute spin addition j1+j2"

    def _format_half_int(self, val: float) -> str:
        """Format a half-integer as a fraction string.

        Args:
            val: Value that may be half-integer.

        Returns:
            String like '1/2', '3/2', or '2'.
        """
        if val == int(val):
            return str(int(val))
        numerator = int(val * 2)
        return f"{numerator}/2"

    def _sample_j(self, difficulty: int) -> tuple[float, float]:
        """Sample j1 and j2 based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (j1, j2) as floats.
        """
        if difficulty <= 3:
            pool = [0.5, 1.0, 1.5]
        elif difficulty <= 6:
            pool = [0.5, 1.0, 1.5, 2.0, 2.5]
        else:
            pool = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        j1 = self._rng.choice(pool)
        j2 = self._rng.choice(pool)
        return j1, j2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spin addition problem.

        Args:
            difficulty: Controls j ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        j1, j2 = self._sample_j(difficulty)
        j_min = abs(j1 - j2)
        j_max = j1 + j2

        j_values: list[float] = []
        j_cur = j_min
        while j_cur <= j_max + 1e-9:
            j_values.append(j_cur)
            j_cur += 1.0

        state_counts = [int(2 * j + 1) for j in j_values]
        total_states = sum(state_counts)

        problem = f"j_1={self._format_half_int(j1)}, j_2={self._format_half_int(j2)}"
        return problem, {
            "j1": j1, "j2": j2, "j_min": j_min, "j_max": j_max,
            "j_values": j_values, "state_counts": state_counts,
            "total_states": total_states,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spin addition steps.

        Args:
            data: Solution data with j1, j2, j range, and state counts.

        Returns:
            Steps showing j_min, j_max, j set, and state counting.
        """
        j1_s = self._format_half_int(data["j1"])
        j2_s = self._format_half_int(data["j2"])
        jmin_s = self._format_half_int(data["j_min"])
        jmax_s = self._format_half_int(data["j_max"])
        j_set = ", ".join(self._format_half_int(j) for j in data["j_values"])
        counts = "+".join(str(c) for c in data["state_counts"])
        return [
            f"j_{{min}}=|{j1_s}-{j2_s}|={jmin_s}",
            f"j_{{max}}={j1_s}+{j2_s}={jmax_s}",
            f"j \\in {{{j_set}}}",
            f"states: {counts}={data['total_states']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the set of j values and total state count.

        Args:
            data: Solution data.

        Returns:
            String with j values and total states.
        """
        j_set = ", ".join(self._format_half_int(j) for j in data["j_values"])
        return f"j={{{j_set}}}, total={data['total_states']}"


# ---------------------------------------------------------------------------
# Generator 6: Hydrogen atom energy levels
# ---------------------------------------------------------------------------
@register
class HydrogenEnergyGenerator(StepGenerator):
    """Hydrogen energy levels: E_n = -13.6/n^2 eV.

    Computes hydrogen atom energy for a given n, or the photon
    wavelength for a transition between levels n1 and n2 using
    the Rydberg formula 1/lambda = R (1/n1^2 - 1/n2^2) with
    R = 1.097e7 m^-1.

    Input format:
        ``compute hydrogen energy level or transition wavelength``

    Target format:
        ``E_n = -13.6/n^2 eV <step> n=3
        <step> E_3 = -13.6/9 = -1.5111 eV
        <step> transition 2->3: 1/lambda = R(1/4-1/9)
        <step> lambda = 6.5646e-7 m``

    Difficulty scaling:
        Difficulty 1-3: n in [1,3], transition within n<=3.
        Difficulty 4-6: n in [1,5], transitions across wider range.
        Difficulty 7-8: n in [1,8].

    Prerequisites:
        division.

    Example:
        >>> gen = HydrogenEnergyGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'hydrogen_energy'
    """

    _RYDBERG = 1.097e7

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hydrogen_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n range.

        Returns:
            Natural language description.
        """
        return "compute hydrogen energy level or transition wavelength"

    def _sample_levels(self, difficulty: int) -> tuple[int, int]:
        """Sample two distinct energy levels n1 < n2.

        Args:
            difficulty: Controls maximum n.

        Returns:
            Tuple of (n1, n2) with n1 < n2.
        """
        if difficulty <= 3:
            n_max = 3
        elif difficulty <= 6:
            n_max = 5
        else:
            n_max = 8
        n1 = self._rng.randint(1, max(1, n_max - 1))
        n2 = self._rng.randint(n1 + 1, n_max)
        return n1, n2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hydrogen energy / transition problem.

        Args:
            difficulty: Controls n ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n1, n2 = self._sample_levels(difficulty)
        e_n1 = round(-13.6 / (n1 * n1), 4)
        e_n2 = round(-13.6 / (n2 * n2), 4)
        inv_lam = self._RYDBERG * (1.0 / (n1 * n1) - 1.0 / (n2 * n2))
        wavelength = 1.0 / inv_lam if inv_lam != 0 else float("inf")

        formula = "E_n = -13.6/n^2 eV"
        return formula, {
            "n1": n1, "n2": n2,
            "E_n1": e_n1, "E_n2": e_n2,
            "inv_lam": inv_lam, "wavelength": wavelength,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate energy level and wavelength computation steps.

        Args:
            data: Solution data with n1, n2, energies, and wavelength.

        Returns:
            Steps showing E_n values and Rydberg formula.
        """
        n1, n2 = data["n1"], data["n2"]
        fmt = QuantumFormatter
        inv_n1_sq = round(1.0 / (n1 * n1), 4)
        inv_n2_sq = round(1.0 / (n2 * n2), 4)
        return [
            f"E_{{{n1}}} = -13.6/{n1}^2 = {data['E_n1']} eV",
            f"E_{{{n2}}} = -13.6/{n2}^2 = {data['E_n2']} eV",
            f"1/\\lambda = R(1/{n1}^2 - 1/{n2}^2)"
            f" = R({inv_n1_sq} - {inv_n2_sq})",
            f"\\lambda = {fmt.format_sci(data['wavelength'])} m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the energy and transition wavelength.

        Args:
            data: Solution data.

        Returns:
            String with E_n1, E_n2, and wavelength.
        """
        fmt = QuantumFormatter
        return (
            f"E_{{{data['n1']}}}={data['E_n1']} eV, "
            f"\\lambda={fmt.format_sci(data['wavelength'])} m"
        )
