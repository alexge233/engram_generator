"""Quantum information generators -- Bell states through no-cloning.

Covers Bell state construction, entanglement entropy, quantum
teleportation protocol, Grover iteration, quantum Fourier transform,
error syndrome detection, density matrices, and the no-cloning
proof.  Tiers range from 6 (Bell states, error codes) to 7
(teleportation, QFT, entanglement measure, no-cloning).
All quantum states use Dirac notation (|0>, |1>, |+>, |->).
Matrix computations stay at 2x2 or 4x4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class StateVector:
    """Represents a multi-qubit state as a list of amplitude coefficients.

    Stores amplitudes paired with their computational basis labels
    and provides formatting in Dirac notation.

    Attributes:
        amplitudes: List of (coefficient, basis_label) tuples.
    """

    def __init__(self, amplitudes: list[tuple[float, str]]) -> None:
        """Initialise with a list of (coefficient, ket_label) pairs.

        Args:
            amplitudes: List of (amplitude, ket_label) tuples.
        """
        self._amplitudes = amplitudes

    @property
    def amplitudes(self) -> list[tuple[float, str]]:
        """Return the amplitude list."""
        return list(self._amplitudes)

    def to_dirac(self) -> str:
        """Format the state in Dirac notation.

        Returns:
            String like '1/sqrt(2)(|00> + |11>)'.
        """
        nonzero = [(a, k) for a, k in self._amplitudes if abs(a) > 1e-9]
        if not nonzero:
            return "0"
        parts: list[str] = []
        for i, (amp, ket) in enumerate(nonzero):
            amp_r = round(amp, 4)
            if abs(amp_r - 1.0) < 1e-9:
                term = f"|{ket}>"
            elif abs(amp_r + 1.0) < 1e-9:
                term = f"-|{ket}>"
            elif amp_r < 0:
                term = f"{amp_r}|{ket}>"
            else:
                term = f"{amp_r}|{ket}>"
            if i > 0 and amp_r > 0:
                term = f" + {term}"
            elif i > 0 and amp_r < 0:
                term = f" - {abs(amp_r)}|{ket}>"
            parts.append(term)
        return "".join(parts)


class QInfoFormatter:
    """Formats numbers for quantum information calculations.

    Provides clean formatting for probabilities, small floats,
    and scientific notation used in quantum information theory.
    """

    @staticmethod
    def format_value(value: float, decimals: int = 4) -> str:
        """Format a numeric value cleanly.

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

    @staticmethod
    def format_matrix_2x2(m: list[list[float]]) -> str:
        """Format a 2x2 matrix in LaTeX pmatrix notation.

        Args:
            m: 2x2 matrix as nested lists.

        Returns:
            LaTeX pmatrix string.
        """
        rows = [
            " & ".join(QInfoFormatter.format_value(v) for v in row)
            for row in m
        ]
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"

    @staticmethod
    def format_matrix_4x4(m: list[list[float]]) -> str:
        """Format a 4x4 matrix in LaTeX pmatrix notation.

        Args:
            m: 4x4 matrix as nested lists.

        Returns:
            LaTeX pmatrix string.
        """
        rows = [
            " & ".join(QInfoFormatter.format_value(v) for v in row)
            for row in m
        ]
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


# -- Gate and operation constants -------------------------------------------

_INV_SQRT2 = 1.0 / math.sqrt(2.0)

# Hadamard gate
_H_GATE = [[_INV_SQRT2, _INV_SQRT2], [_INV_SQRT2, -_INV_SQRT2]]

# CNOT gate (4x4 in |00>,|01>,|10>,|11> basis)
_CNOT = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
]

# Pauli gates
_X_GATE = [[0, 1], [1, 0]]
_Z_GATE = [[1, 0], [0, -1]]


def _apply_2x2(gate: list[list[float]], vec: list[float]) -> list[float]:
    """Apply a 2x2 gate to a 2-element vector.

    Args:
        gate: 2x2 matrix.
        vec: 2-element vector.

    Returns:
        Result vector.
    """
    return [
        gate[0][0] * vec[0] + gate[0][1] * vec[1],
        gate[1][0] * vec[0] + gate[1][1] * vec[1],
    ]


def _apply_4x4(gate: list[list[float]], vec: list[float]) -> list[float]:
    """Apply a 4x4 gate to a 4-element vector.

    Args:
        gate: 4x4 matrix.
        vec: 4-element vector.

    Returns:
        Result vector.
    """
    result = []
    for row in gate:
        val = sum(row[j] * vec[j] for j in range(4))
        result.append(val)
    return result


def _outer_product(v: list[float]) -> list[list[float]]:
    """Compute the outer product |v><v| for a column vector.

    Args:
        v: Column vector as a list of floats.

    Returns:
        Square matrix |v><v|.
    """
    n = len(v)
    return [[v[i] * v[j] for j in range(n)] for i in range(n)]


def _mat_add(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Add two matrices element-wise.

    Args:
        a: First matrix.
        b: Second matrix.

    Returns:
        Element-wise sum.
    """
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def _mat_scale(s: float, m: list[list[float]]) -> list[list[float]]:
    """Scale a matrix by a scalar.

    Args:
        s: Scalar multiplier.
        m: Matrix.

    Returns:
        Scaled matrix.
    """
    n = len(m)
    return [[s * m[i][j] for j in range(n)] for i in range(n)]


def _trace(m: list[list[float]]) -> float:
    """Compute the trace of a square matrix.

    Args:
        m: Square matrix.

    Returns:
        Sum of diagonal elements.
    """
    return sum(m[i][i] for i in range(len(m)))


def _partial_trace_b(rho_4x4: list[list[float]]) -> list[list[float]]:
    """Compute the partial trace over subsystem B for a 2-qubit state.

    Traces out the second qubit from a 4x4 density matrix in the
    computational basis {|00>, |01>, |10>, |11>}.

    Args:
        rho_4x4: 4x4 density matrix.

    Returns:
        2x2 reduced density matrix for subsystem A.
    """
    rho_a = [[0.0, 0.0], [0.0, 0.0]]
    rho_a[0][0] = rho_4x4[0][0] + rho_4x4[1][1]
    rho_a[0][1] = rho_4x4[0][2] + rho_4x4[1][3]
    rho_a[1][0] = rho_4x4[2][0] + rho_4x4[3][1]
    rho_a[1][1] = rho_4x4[2][2] + rho_4x4[3][3]
    return rho_a


def _eigenvalues_2x2(m: list[list[float]]) -> list[float]:
    """Compute eigenvalues of a 2x2 real symmetric matrix.

    Args:
        m: 2x2 real symmetric matrix.

    Returns:
        List of two eigenvalues sorted descending.
    """
    a, b = m[0][0], m[0][1]
    c, d = m[1][0], m[1][1]
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    if disc < 0:
        disc = 0.0
    sqrt_disc = math.sqrt(disc)
    l1 = (tr + sqrt_disc) / 2.0
    l2 = (tr - sqrt_disc) / 2.0
    return sorted([l1, l2], reverse=True)


# ---------------------------------------------------------------------------
# Generator 1: Bell state construction
# ---------------------------------------------------------------------------
@register
class BellStateGenerator(StepGenerator):
    """Construct Bell states from H and CNOT on basis states.

    Applies Hadamard to the first qubit, then CNOT, starting from
    one of |00>, |01>, |10>, |11>. Shows the state after each gate.

    Input format:
        ``construct Bell state from |ab>``

    Target format:
        ``|00> <step> H|0>=(1/sqrt(2))(|0>+|1>)
        <step> state=(1/sqrt(2))(|00>+|10>)
        <step> CNOT: (1/sqrt(2))(|00>+|11>)
        <step> |Phi+>=(1/sqrt(2))(|00>+|11>)``

    Difficulty scaling:
        Difficulty 1-3: |00> and |10> inputs (simpler Bell states).
        Difficulty 4-6: all four inputs.
        Difficulty 7-8: all four inputs with explicit amplitude tracking.

    Prerequisites:
        quantum_gate.

    Example:
        >>> gen = BellStateGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bell_state'
    """

    _BELL_NAMES = {
        (0, 0): "|\\Phi^+\\rangle",
        (0, 1): "|\\Psi^+\\rangle",
        (1, 0): "|\\Phi^-\\rangle",
        (1, 1): "|\\Psi^-\\rangle",
    }

    _BELL_STATES = {
        (0, 0): "(|00> + |11>)",
        (0, 1): "(|01> + |10>)",
        (1, 0): "(|00> - |11>)",
        (1, 1): "(|01> - |10>)",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bell_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls input state selection.

        Returns:
            Natural language description.
        """
        return "construct Bell state from basis input"

    def _select_input(self, difficulty: int) -> tuple[int, int]:
        """Select input qubit values (a, b).

        Args:
            difficulty: Controls input pool.

        Returns:
            Tuple of (a, b) each 0 or 1.
        """
        if difficulty <= 3:
            pool = [(0, 0), (1, 0)]
        else:
            pool = [(0, 0), (0, 1), (1, 0), (1, 1)]
        return self._rng.choice(pool)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bell state construction problem.

        Args:
            difficulty: Controls input selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a, b = self._select_input(difficulty)

        # Initial 4-vector in {|00>,|01>,|10>,|11>} basis
        idx = a * 2 + b
        initial = [0.0, 0.0, 0.0, 0.0]
        initial[idx] = 1.0

        # Apply H to first qubit: H tensor I
        # |0> -> (|0>+|1>)/sqrt(2), |1> -> (|0>-|1>)/sqrt(2)
        after_h = [0.0, 0.0, 0.0, 0.0]
        after_h[0 * 2 + b] += _INV_SQRT2 * (1.0 if a == 0 else 1.0)
        after_h[1 * 2 + b] += _INV_SQRT2 * (1.0 if a == 0 else -1.0)

        # Apply CNOT
        after_cnot = _apply_4x4(_CNOT, after_h)

        bell_name = self._BELL_NAMES[(a, b)]
        bell_expr = self._BELL_STATES[(a, b)]

        problem = f"|{a}{b}\\rangle"
        return problem, {
            "a": a, "b": b,
            "after_h": after_h, "after_cnot": after_cnot,
            "bell_name": bell_name, "bell_expr": bell_expr,
        }

    def _format_state(self, vec: list[float]) -> str:
        """Format a 4-element state vector in Dirac notation.

        Args:
            vec: 4-element amplitude vector.

        Returns:
            Dirac notation string.
        """
        labels = ["00", "01", "10", "11"]
        sv = StateVector([(vec[i], labels[i]) for i in range(4)])
        return sv.to_dirac()

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bell state construction steps.

        Args:
            data: Solution data with intermediate states.

        Returns:
            Steps showing H application, intermediate, and CNOT result.
        """
        a, b = data["a"], data["b"]
        h_sign = "+" if a == 0 else "-"
        return [
            f"input: |{a}{b}>",
            f"H|{a}> = (1/sqrt(2))(|0> {h_sign} |1>)",
            f"after H x I: (1/sqrt(2))(|0{b}> {h_sign} |1{b}>)",
            f"CNOT: {data['bell_expr']} / sqrt(2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Bell state name and expression.

        Args:
            data: Solution data.

        Returns:
            String with Bell state name.
        """
        return (
            f"{data['bell_name']} = "
            f"(1/sqrt(2)){data['bell_expr']}"
        )


# ---------------------------------------------------------------------------
# Generator 2: Entanglement measure (von Neumann entropy)
# ---------------------------------------------------------------------------
@register
class EntanglementMeasureGenerator(StepGenerator):
    """Von Neumann entropy S = -Tr(rho log rho) for a reduced state.

    Constructs a 2-qubit pure state, computes the reduced density
    matrix by tracing out one qubit, finds its eigenvalues, and
    evaluates the von Neumann entropy.

    Input format:
        ``compute entanglement entropy of a 2-qubit state``

    Target format:
        ``|psi> = a|00> + b|11> <step>
        rho = |psi><psi| <step>
        rho_A = Tr_B(rho) <step>
        eigenvalues: {0.5, 0.5} <step>
        S = -sum(p log p) = 0.6931``

    Difficulty scaling:
        Difficulty 1-3: maximally entangled (a=b=1/sqrt(2)).
        Difficulty 4-6: varied entanglement (random a,b).
        Difficulty 7-8: general 2-qubit states with 3-4 terms.

    Prerequisites:
        eigenvalue.

    Example:
        >>> gen = EntanglementMeasureGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'entanglement_measure'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "entanglement_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Natural language description.
        """
        return "compute entanglement entropy of a 2-qubit state"

    def _sample_state(self, difficulty: int) -> list[float]:
        """Sample a normalised 2-qubit state vector.

        Args:
            difficulty: Controls number of non-zero amplitudes.

        Returns:
            4-element normalised amplitude vector.
        """
        if difficulty <= 3:
            # Maximally entangled: (|00> + |11>)/sqrt(2)
            return [_INV_SQRT2, 0.0, 0.0, _INV_SQRT2]
        if difficulty <= 6:
            # a|00> + b|11> with random split
            theta = self._rng.uniform(0.2, 1.3)
            a = math.cos(theta)
            b = math.sin(theta)
            return [round(a, 4), 0.0, 0.0, round(b, 4)]
        # General: a|00> + b|01> + c|10> + d|11>, normalised
        raw = [self._rng.uniform(-1, 1) for _ in range(4)]
        norm = math.sqrt(sum(x * x for x in raw))
        return [round(x / norm, 4) for x in raw]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an entanglement entropy problem.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        psi = self._sample_state(difficulty)
        rho = _outer_product(psi)
        rho_a = _partial_trace_b(rho)
        eigs = _eigenvalues_2x2(rho_a)
        eigs_clean = [max(0.0, e) for e in eigs]

        entropy = 0.0
        for e in eigs_clean:
            if e > 1e-12:
                entropy -= e * math.log(e)
        entropy = round(entropy, 4)

        labels = ["00", "01", "10", "11"]
        sv = StateVector([(psi[i], labels[i]) for i in range(4)])
        problem = f"|\\psi\\rangle = {sv.to_dirac()}"

        return problem, {
            "psi": psi, "rho_a": rho_a,
            "eigenvalues": [round(e, 4) for e in eigs_clean],
            "entropy": entropy, "state_str": sv.to_dirac(),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy computation steps.

        Args:
            data: Solution data with state, rho_A, eigenvalues, entropy.

        Returns:
            Steps showing rho, partial trace, eigenvalues, and entropy.
        """
        fmt = QInfoFormatter
        eigs = data["eigenvalues"]
        eig_str = ", ".join(fmt.format_value(e) for e in eigs)
        return [
            f"\\rho = |\\psi\\rangle\\langle\\psi|",
            f"\\rho_A = Tr_B(\\rho) = {fmt.format_matrix_2x2(data['rho_a'])}",
            f"eigenvalues: {{{eig_str}}}",
            f"S = -\\sum p_i \\ln(p_i)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the von Neumann entropy.

        Args:
            data: Solution data.

        Returns:
            String with entropy value.
        """
        return f"S = {QInfoFormatter.format_value(data['entropy'])}"


# ---------------------------------------------------------------------------
# Generator 3: Quantum teleportation protocol
# ---------------------------------------------------------------------------
@register
class QuantumTeleportationGenerator(StepGenerator):
    """Step through the quantum teleportation protocol.

    Shows the full protocol: Alice and Bob share a Bell pair,
    Alice performs a Bell measurement on her qubit and the unknown
    state, sends classical bits, and Bob applies corrections.

    Input format:
        ``step through quantum teleportation protocol``

    Target format:
        ``|psi> = a|0> + b|1> <step>
        Bell pair: (|00>+|11>)/sqrt(2)
        <step> Alice CNOT + H -> measurement
        <step> classical bits: (m1,m2)
        <step> Bob correction: X^m2 Z^m1
        <step> Bob has |psi>``

    Difficulty scaling:
        Difficulty 1-3: fixed |psi> = |0> or |1>.
        Difficulty 4-6: |psi> = cos(t)|0> + sin(t)|1>.
        Difficulty 7-8: random measurement outcome shown explicitly.

    Prerequisites:
        bell_state.

    Example:
        >>> gen = QuantumTeleportationGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'quantum_teleportation'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "quantum_teleportation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bell_state"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Natural language description.
        """
        return "step through quantum teleportation protocol"

    def _sample_state(
        self, difficulty: int
    ) -> tuple[float, float, str]:
        """Sample coefficients for the state to teleport.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Tuple of (alpha, beta, state_label).
        """
        if difficulty <= 3:
            choice = self._rng.choice(["0", "1"])
            if choice == "0":
                return 1.0, 0.0, "|0>"
            return 0.0, 1.0, "|1>"
        theta = round(self._rng.uniform(0.3, 1.2), 4)
        alpha = round(math.cos(theta), 4)
        beta = round(math.sin(theta), 4)
        return alpha, beta, f"{alpha}|0> + {beta}|1>"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a teleportation protocol problem.

        Args:
            difficulty: Controls state and measurement detail.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        alpha, beta, state_label = self._sample_state(difficulty)
        m1 = self._rng.randint(0, 1)
        m2 = self._rng.randint(0, 1)
        correction = ""
        if m2 == 1:
            correction += "X"
        if m1 == 1:
            correction += "Z"
        if not correction:
            correction = "I"

        problem = f"|\\psi\\rangle = {state_label}"
        return problem, {
            "alpha": alpha, "beta": beta,
            "state_label": state_label,
            "m1": m1, "m2": m2,
            "correction": correction,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate teleportation protocol steps.

        Args:
            data: Solution data with state, measurement, correction.

        Returns:
            Steps showing shared pair, Bell measurement, and correction.
        """
        return [
            f"|\\psi> = {data['state_label']}",
            "Bell pair shared: (1/sqrt(2))(|00> + |11>)",
            "Alice: CNOT(psi, her_half), then H(psi)",
            f"measurement: m1={data['m1']}, m2={data['m2']}",
            f"Bob applies: {data['correction']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the teleportation result.

        Args:
            data: Solution data.

        Returns:
            String confirming Bob recovers the state.
        """
        return (
            f"Bob: {data['correction']} -> "
            f"|\\psi> = {data['state_label']}"
        )


# ---------------------------------------------------------------------------
# Generator 4: Grover iteration step
# ---------------------------------------------------------------------------
@register
class GroverStepGenerator(StepGenerator):
    """One Grover iteration: oracle + diffusion on a 2-qubit system.

    Starts from the uniform superposition |s> = (1/2)(|00>+|01>+|10>+|11>),
    applies the oracle O_f that flips the marked state, then the
    diffusion operator D = 2|s><s| - I. Shows amplitude changes.

    Input format:
        ``perform one Grover iteration on 2-qubit system``

    Target format:
        ``|s> = (1/2)(|00>+|01>+|10>+|11>) <step>
        marked=|10> <step>
        after oracle: amplitudes (0.5, 0.5, -0.5, 0.5) <step>
        after diffusion: amplitudes (0, 0, 1, 0)``

    Difficulty scaling:
        Difficulty 1-4: 2-qubit system (4 states), one iteration.
        Difficulty 5-6: 2-qubit, show intermediate amplitudes.
        Difficulty 7-8: 2-qubit, two iterations.

    Prerequisites:
        quantum_gate.

    Example:
        >>> gen = GroverStepGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'grover_step'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "grover_step"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of iterations.

        Returns:
            Natural language description.
        """
        return "perform one Grover iteration on 2-qubit system"

    def _grover_iteration(
        self, amplitudes: list[float], marked: int
    ) -> tuple[list[float], list[float]]:
        """Perform one Grover iteration.

        Args:
            amplitudes: Current amplitude vector.
            marked: Index of the marked state.

        Returns:
            Tuple of (after_oracle, after_diffusion) amplitude vectors.
        """
        n = len(amplitudes)
        # Oracle: flip sign of marked state
        after_oracle = list(amplitudes)
        after_oracle[marked] = -after_oracle[marked]
        # Diffusion: D = 2|s><s| - I
        mean = sum(after_oracle) / n
        after_diff = [round(2 * mean - a, 4) for a in after_oracle]
        return after_oracle, after_diff

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Grover iteration problem.

        Args:
            difficulty: Controls iteration count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = 4  # 2-qubit system
        labels = ["00", "01", "10", "11"]
        marked_idx = self._rng.randint(0, 3)
        amp = 1.0 / math.sqrt(n)
        amplitudes = [round(amp, 4)] * n

        iterations = 1 if difficulty <= 6 else 2
        history: list[tuple[list[float], list[float]]] = []

        current = list(amplitudes)
        for _ in range(iterations):
            after_o, after_d = self._grover_iteration(current, marked_idx)
            history.append(([round(a, 4) for a in after_o],
                            [round(a, 4) for a in after_d]))
            current = after_d

        problem = f"marked state: |{labels[marked_idx]}>"
        return problem, {
            "labels": labels, "marked_idx": marked_idx,
            "marked_label": labels[marked_idx],
            "initial": amplitudes, "history": history,
            "final": current, "iterations": iterations,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Grover iteration steps.

        Args:
            data: Solution data with amplitudes and history.

        Returns:
            Steps showing initial, oracle, and diffusion.
        """
        labels = data["labels"]
        init_str = ", ".join(
            f"{a}|{l}>" for a, l in zip(data["initial"], labels)
        )
        steps = [f"|s> = {init_str}", f"marked: |{data['marked_label']}>"]

        for i, (after_o, after_d) in enumerate(data["history"], 1):
            o_str = ", ".join(str(a) for a in after_o)
            d_str = ", ".join(str(a) for a in after_d)
            steps.append(f"iter {i} oracle: ({o_str})")
            steps.append(f"iter {i} diffusion: ({d_str})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final amplitudes.

        Args:
            data: Solution data.

        Returns:
            String with final amplitude vector.
        """
        amp_str = ", ".join(str(a) for a in data["final"])
        return f"amplitudes: ({amp_str})"


# ---------------------------------------------------------------------------
# Generator 5: 2-qubit QFT
# ---------------------------------------------------------------------------
@register
class QFTComputeGenerator(StepGenerator):
    """2-qubit quantum Fourier transform.

    Applies the QFT circuit to a 2-qubit computational basis state:
    H on qubit 1, controlled-R2 (phase pi/2), swap, H on qubit 2.
    Shows the output state after each gate.

    Input format:
        ``compute 2-qubit QFT of |ab>``

    Target format:
        ``input: |10> <step> H on q1 -> (|0>-|1>)/sqrt(2) x |0>
        <step> CR2 -> phase shift <step> swap qubits
        <step> H on q2 <step> output state``

    Difficulty scaling:
        Difficulty 1-3: input |00> or |01>.
        Difficulty 4-6: input |10> or |11>.
        Difficulty 7-8: all four inputs with full amplitude tracking.

    Prerequisites:
        quantum_gate.

    Example:
        >>> gen = QFTComputeGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'qft_compute'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "qft_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls input state.

        Returns:
            Natural language description.
        """
        return "compute 2-qubit QFT"

    def _select_input(self, difficulty: int) -> int:
        """Select input basis state index.

        Args:
            difficulty: Controls pool of inputs.

        Returns:
            Integer 0-3 representing |00> through |11>.
        """
        if difficulty <= 3:
            return self._rng.choice([0, 1])
        if difficulty <= 6:
            return self._rng.choice([2, 3])
        return self._rng.randint(0, 3)

    def _qft_2qubit(self, k: int) -> list[complex]:
        """Compute the 2-qubit QFT output for input |k>.

        The 2-qubit QFT maps |k> to (1/2) sum_j omega^{jk} |j>
        where omega = e^{2 pi i / 4}.

        Args:
            k: Input state index (0-3).

        Returns:
            4-element complex amplitude vector.
        """
        n = 4
        omega = complex(math.cos(2 * math.pi / n),
                        math.sin(2 * math.pi / n))
        result = []
        for j in range(n):
            amp = (omega ** (j * k)) / 2.0
            result.append(amp)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-qubit QFT problem.

        Args:
            difficulty: Controls input state.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._select_input(difficulty)
        labels = ["00", "01", "10", "11"]
        output = self._qft_2qubit(k)
        output_real = [round(c.real, 4) for c in output]
        output_imag = [round(c.imag, 4) for c in output]

        problem = f"QFT|{labels[k]}\\rangle"
        return problem, {
            "k": k, "label": labels[k], "labels": labels,
            "output": output,
            "output_real": output_real,
            "output_imag": output_imag,
        }

    def _format_complex(self, re: float, im: float) -> str:
        """Format a complex amplitude cleanly.

        Args:
            re: Real part.
            im: Imaginary part.

        Returns:
            String representation of the complex number.
        """
        fmt = QInfoFormatter.format_value
        if abs(im) < 1e-9:
            return fmt(re)
        if abs(re) < 1e-9:
            return f"{fmt(im)}i"
        sign = "+" if im >= 0 else "-"
        return f"{fmt(re)}{sign}{fmt(abs(im))}i"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate QFT circuit steps.

        Args:
            data: Solution data with input and output amplitudes.

        Returns:
            Steps showing each gate application.
        """
        k = data["k"]
        labels = data["labels"]
        q1 = k // 2
        q2 = k % 2
        h_sign = "+" if q1 == 0 else "-"
        steps = [
            f"input: |{data['label']}>",
            f"H on q1: (1/sqrt(2))(|0> {h_sign} |1>) x |{q2}>",
            f"controlled-R2: phase e^{{i*pi*{q2}/2}} on |1{q2}>",
            "swap qubits",
        ]
        amp_strs = []
        for j in range(4):
            amp = self._format_complex(
                data["output_real"][j], data["output_imag"][j]
            )
            amp_strs.append(f"{amp}|{labels[j]}>")
        steps.append("output: (1/2)(" + " + ".join(amp_strs) + ")")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the QFT output state.

        Args:
            data: Solution data.

        Returns:
            Dirac notation string for the output.
        """
        labels = data["labels"]
        parts = []
        for j in range(4):
            amp = self._format_complex(
                data["output_real"][j], data["output_imag"][j]
            )
            parts.append(f"{amp}|{labels[j]}>")
        return "(1/2)(" + " + ".join(parts) + ")"


# ---------------------------------------------------------------------------
# Generator 6: 3-qubit bit-flip error syndrome
# ---------------------------------------------------------------------------
@register
class ErrorSyndromeGenerator(StepGenerator):
    """3-qubit bit-flip code: encode, introduce error, detect syndrome.

    Encodes a logical qubit |psi> = a|0> + b|1> into three physical
    qubits (a|000> + b|111>), introduces a single bit-flip error,
    and detects which qubit flipped from the syndrome measurement.

    Input format:
        ``detect error syndrome in 3-qubit bit-flip code``

    Target format:
        ``|psi> = a|0>+b|1> <step>
        encode: a|000>+b|111> <step>
        error on qubit 2: a|010>+b|101> <step>
        syndrome Z1Z2=(-1), Z2Z3=(+1) <step>
        error on qubit 2``

    Difficulty scaling:
        Difficulty 1-3: error on qubit 1 or 3 (edges).
        Difficulty 4-6: any single qubit error.
        Difficulty 7-8: includes no-error case.

    Prerequisites:
        quantum_gate.

    Example:
        >>> gen = ErrorSyndromeGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'error_syndrome'
    """

    _SYNDROME_TABLE = {
        0: ("Z1Z2=+1, Z2Z3=+1", "no error"),
        1: ("Z1Z2=-1, Z2Z3=+1", "error on qubit 1"),
        2: ("Z1Z2=-1, Z2Z3=-1", "error on qubit 2"),
        3: ("Z1Z2=+1, Z2Z3=-1", "error on qubit 3"),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "error_syndrome"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls error position.

        Returns:
            Natural language description.
        """
        return "detect error syndrome in 3-qubit bit-flip code"

    def _select_error(self, difficulty: int) -> int:
        """Select which qubit has the error (0 = no error).

        Args:
            difficulty: Controls error pool.

        Returns:
            Error position: 0=none, 1-3=qubit index.
        """
        if difficulty <= 3:
            return self._rng.choice([1, 3])
        if difficulty <= 6:
            return self._rng.choice([1, 2, 3])
        return self._rng.choice([0, 1, 2, 3])

    def _flip_bit(self, bitstring: str, pos: int) -> str:
        """Flip a single bit in a 3-bit string.

        Args:
            bitstring: 3-character string of '0' and '1'.
            pos: 1-indexed position to flip (0 means no flip).

        Returns:
            Modified bitstring.
        """
        if pos == 0:
            return bitstring
        bits = list(bitstring)
        idx = pos - 1
        bits[idx] = "1" if bits[idx] == "0" else "0"
        return "".join(bits)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bit-flip error syndrome problem.

        Args:
            difficulty: Controls error position.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        error_pos = self._select_error(difficulty)
        encoded_0 = "000"
        encoded_1 = "111"
        errored_0 = self._flip_bit(encoded_0, error_pos)
        errored_1 = self._flip_bit(encoded_1, error_pos)
        syndrome_str, diagnosis = self._SYNDROME_TABLE[error_pos]

        problem = "|\\psi\\rangle = a|0\\rangle + b|1\\rangle"
        return problem, {
            "error_pos": error_pos,
            "encoded_0": encoded_0, "encoded_1": encoded_1,
            "errored_0": errored_0, "errored_1": errored_1,
            "syndrome": syndrome_str, "diagnosis": diagnosis,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate encoding, error, and syndrome detection steps.

        Args:
            data: Solution data with encoded states and syndrome.

        Returns:
            Steps showing encoding, error application, and syndrome.
        """
        steps = [
            f"encode: a|{data['encoded_0']}> + b|{data['encoded_1']}>",
        ]
        if data["error_pos"] > 0:
            steps.append(
                f"X on qubit {data['error_pos']}: "
                f"a|{data['errored_0']}> + b|{data['errored_1']}>"
            )
        else:
            steps.append("no error applied")
        steps.append(f"syndrome: {data['syndrome']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the syndrome diagnosis.

        Args:
            data: Solution data.

        Returns:
            String identifying the error location.
        """
        return data["diagnosis"]


# ---------------------------------------------------------------------------
# Generator 7: Density matrix
# ---------------------------------------------------------------------------
@register
class DensityMatrixGenerator(StepGenerator):
    """Compute rho = |psi><psi| or rho = sum p_i |psi_i><psi_i|.

    For pure states, computes the outer product. For mixed states,
    combines multiple pure-state density matrices with classical
    probabilities.

    Input format:
        ``compute density matrix for a quantum state``

    Target format:
        ``|psi> = a|0> + b|1> <step>
        rho = |psi><psi| <step>
        rho = [[a^2, ab], [ab, b^2]]``

    Difficulty scaling:
        Difficulty 1-3: pure state with real amplitudes.
        Difficulty 4-6: pure state with varied amplitudes.
        Difficulty 7-8: mixed state (2-component mixture).

    Prerequisites:
        matrix_multiply.

    Example:
        >>> gen = DensityMatrixGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'density_matrix'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "density_matrix"

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
            difficulty: Controls pure vs mixed state.

        Returns:
            Natural language description.
        """
        return "compute density matrix for a quantum state"

    def _sample_pure_state(self, difficulty: int) -> tuple[float, float]:
        """Sample normalised amplitudes (a, b) for a|0> + b|1>.

        Args:
            difficulty: Controls amplitude complexity.

        Returns:
            Tuple of (a, b).
        """
        if difficulty <= 3:
            pool = [
                (1.0, 0.0), (0.0, 1.0),
                (_INV_SQRT2, _INV_SQRT2),
            ]
            a, b = self._rng.choice(pool)
        else:
            theta = round(self._rng.uniform(0.2, 1.4), 4)
            a = round(math.cos(theta), 4)
            b = round(math.sin(theta), 4)
        return a, b

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a density matrix problem.

        Args:
            difficulty: Controls pure vs mixed state.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            a, b = self._sample_pure_state(difficulty)
            rho = [
                [round(a * a, 4), round(a * b, 4)],
                [round(b * a, 4), round(b * b, 4)],
            ]
            state_str = self._format_state(a, b)
            problem = f"|\\psi\\rangle = {state_str}"
            return problem, {
                "mode": "pure", "a": a, "b": b,
                "rho": rho, "state_str": state_str,
            }

        # Mixed state: p|psi1><psi1| + (1-p)|psi2><psi2|
        p = round(self._rng.uniform(0.2, 0.8), 4)
        a1, b1 = self._sample_pure_state(4)
        a2, b2 = self._sample_pure_state(4)
        rho1 = [[a1 * a1, a1 * b1], [b1 * a1, b1 * b1]]
        rho2 = [[a2 * a2, a2 * b2], [b2 * a2, b2 * b2]]
        rho = _mat_add(_mat_scale(p, rho1), _mat_scale(1 - p, rho2))
        rho = [[round(rho[i][j], 4) for j in range(2)] for i in range(2)]

        s1 = self._format_state(a1, b1)
        s2 = self._format_state(a2, b2)
        problem = (
            f"\\rho = {QInfoFormatter.format_value(p)}|\\psi_1\\rangle"
            f"\\langle\\psi_1| + "
            f"{QInfoFormatter.format_value(1 - p)}|\\psi_2\\rangle"
            f"\\langle\\psi_2|"
        )
        return problem, {
            "mode": "mixed", "p": p,
            "a1": a1, "b1": b1, "a2": a2, "b2": b2,
            "s1": s1, "s2": s2, "rho": rho,
        }

    def _format_state(self, a: float, b: float) -> str:
        """Format a single-qubit state in Dirac notation.

        Args:
            a: Amplitude of |0>.
            b: Amplitude of |1>.

        Returns:
            Dirac notation string.
        """
        fmt = QInfoFormatter.format_value
        if abs(b) < 1e-9:
            return "|0>"
        if abs(a) < 1e-9:
            return "|1>"
        return f"{fmt(a)}|0> + {fmt(b)}|1>"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate density matrix computation steps.

        Args:
            data: Solution data with state(s) and rho.

        Returns:
            Steps showing outer product or mixture computation.
        """
        fmt = QInfoFormatter
        if data["mode"] == "pure":
            a, b = data["a"], data["b"]
            return [
                f"|\\psi> = {data['state_str']}",
                f"\\rho = |\\psi><\\psi|",
                f"\\rho_{{00}} = {fmt.format_value(a)}^2"
                f" = {fmt.format_value(round(a * a, 4))}",
                f"\\rho = {fmt.format_matrix_2x2(data['rho'])}",
            ]
        return [
            f"|\\psi_1> = {data['s1']}",
            f"|\\psi_2> = {data['s2']}",
            f"\\rho_1 = |\\psi_1><\\psi_1|",
            f"\\rho_2 = |\\psi_2><\\psi_2|",
            f"\\rho = {fmt.format_value(data['p'])}\\rho_1"
            f" + {fmt.format_value(round(1 - data['p'], 4))}\\rho_2",
            f"\\rho = {fmt.format_matrix_2x2(data['rho'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the density matrix.

        Args:
            data: Solution data.

        Returns:
            LaTeX matrix string for rho.
        """
        return f"\\rho = {QInfoFormatter.format_matrix_2x2(data['rho'])}"


# ---------------------------------------------------------------------------
# Generator 8: No-cloning theorem proof
# ---------------------------------------------------------------------------
@register
class NoCloningProofGenerator(StepGenerator):
    """Show that a universal cloning operator leads to contradiction.

    Assumes a unitary U with U|psi>|0> = |psi>|psi> for all |psi>.
    Applies U to two different states |a> and |b>, takes the inner
    product, and shows <a|b> = <a|b>^2, which forces <a|b> to be
    0 or 1 -- contradicting the assumption that |a> and |b> are
    arbitrary non-orthogonal states.

    Input format:
        ``prove no-cloning theorem by contradiction``

    Target format:
        ``assume U|psi>|0> = |psi>|psi> <step>
        U|a>|0> = |a>|a>, U|b>|0> = |b>|b> <step>
        <a|b> = <a|b>^2 <step>
        x = x^2 -> x=0 or x=1 <step>
        contradiction for 0 < <a|b> < 1``

    Difficulty scaling:
        Difficulty 1-3: |a>=|0>, |b>=|+>, explicit inner product.
        Difficulty 4-6: |a>=cos(t)|0>+sin(t)|1>, |b>=|0>.
        Difficulty 7-8: general |a> and |b> with symbolic proof.

    Prerequisites:
        quantum_gate.

    Example:
        >>> gen = NoCloningProofGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'no_cloning_proof'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "no_cloning_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls proof concreteness.

        Returns:
            Natural language description.
        """
        return "prove no-cloning theorem by contradiction"

    def _sample_states(
        self, difficulty: int
    ) -> tuple[str, str, float]:
        """Sample two non-orthogonal states and their inner product.

        Args:
            difficulty: Controls state choice.

        Returns:
            Tuple of (state_a_label, state_b_label, inner_product).
        """
        if difficulty <= 3:
            return "|0>", "(1/sqrt(2))(|0>+|1>)", round(_INV_SQRT2, 4)
        if difficulty <= 6:
            theta = round(self._rng.uniform(0.3, 1.2), 4)
            cos_t = round(math.cos(theta), 4)
            label_a = f"{cos_t}|0> + {round(math.sin(theta), 4)}|1>"
            return label_a, "|0>", cos_t
        # General symbolic
        theta = round(self._rng.uniform(0.2, 1.4), 4)
        ip = round(math.cos(theta), 4)
        return "|a>", "|b>", ip

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a no-cloning proof problem.

        Args:
            difficulty: Controls proof concreteness.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        label_a, label_b, inner_prod = self._sample_states(difficulty)
        ip_sq = round(inner_prod * inner_prod, 4)

        problem = "U|\\psi\\rangle|0\\rangle = |\\psi\\rangle|\\psi\\rangle"
        return problem, {
            "label_a": label_a, "label_b": label_b,
            "inner_product": inner_prod, "ip_squared": ip_sq,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate the no-cloning contradiction steps.

        Args:
            data: Solution data with states and inner product.

        Returns:
            Steps showing U application and inner product contradiction.
        """
        fmt = QInfoFormatter.format_value
        ip = data["inner_product"]
        ip_sq = data["ip_squared"]
        return [
            f"assume U|psi>|0> = |psi>|psi> for all |psi>",
            f"|a> = {data['label_a']}, |b> = {data['label_b']}",
            f"<a|b><0|0> = (<a|b>)^2",
            f"<a|b> = {fmt(ip)}, (<a|b>)^2 = {fmt(ip_sq)}",
            f"{fmt(ip)} != {fmt(ip_sq)} since 0 < <a|b> < 1",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the no-cloning conclusion.

        Args:
            data: Solution data.

        Returns:
            String stating the contradiction and conclusion.
        """
        return (
            "contradiction: <a|b> = <a|b>^2 forces "
            "<a|b> in {0,1}, no universal cloner exists"
        )
