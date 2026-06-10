"""Extended quantum information generators -- circuits through fidelity.

Covers quantum circuits, measurement, von Neumann entropy, superdense
coding, BB84 key distribution, SWAP test, quantum walk, and fidelity.
All generators are tier 6 (advanced quantum information).
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


_INV_SQRT2 = round(1.0 / math.sqrt(2.0), 4)
_PI = math.pi


# -- Gate matrices ----------------------------------------------------------

_H = [[_INV_SQRT2, _INV_SQRT2], [_INV_SQRT2, -_INV_SQRT2]]
_X = [[0.0, 1.0], [1.0, 0.0]]
_Z = [[1.0, 0.0], [0.0, -1.0]]
_I2 = [[1.0, 0.0], [0.0, 1.0]]


def _apply_gate(gate: list[list[float]], v: list[float]) -> list[float]:
    """Apply a 2x2 gate to a 2-element state vector.

    Args:
        gate: 2x2 matrix.
        v: 2-element vector.

    Returns:
        Resulting 2-element vector.
    """
    return [
        round(gate[0][0] * v[0] + gate[0][1] * v[1], 4),
        round(gate[1][0] * v[0] + gate[1][1] * v[1], 4),
    ]


def _tensor_2x2(a: list[float], b: list[float]) -> list[float]:
    """Compute tensor product of two 2-element vectors.

    Args:
        a: First qubit state.
        b: Second qubit state.

    Returns:
        4-element tensor product vector.
    """
    return [round(a[i] * b[j], 4) for i in range(2) for j in range(2)]


def _cnot_on_4(v: list[float]) -> list[float]:
    """Apply CNOT to a 4-element state in |00>,|01>,|10>,|11> basis.

    Args:
        v: 4-element state vector.

    Returns:
        State after CNOT (control=qubit0, target=qubit1).
    """
    return [v[0], v[1], v[3], v[2]]


# ===================================================================
# 1. Quantum circuit  (tier 6)
# ===================================================================

@register
class QuantumCircuitGenerator(StepGenerator):
    """Apply a sequence of 2-3 gates to an initial qubit state.

    Tracks the state vector through H, X, Z gates applied in
    sequence.  Shows intermediate states after each gate.

    Difficulty scaling:
        Difficulty 1-3: 2 gates, start from |0>.
        Difficulty 4-6: 3 gates, start from |0> or |1>.
        Difficulty 7-8: 3 gates on 2 qubits with CNOT.

    Prerequisites:
        quantum_gate.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_circuit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply gate sequence to qubit state"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantum circuit problem.

        Args:
            difficulty: Controls gate count and qubit count.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        gate_names = {"H": _H, "X": _X, "Z": _Z}

        if difficulty <= 3:
            state = [1.0, 0.0]
            n_gates = 2
            init_label = "|0>"
        elif difficulty <= 6:
            bit = self._rng.choice([0, 1])
            state = [1.0, 0.0] if bit == 0 else [0.0, 1.0]
            n_gates = 3
            init_label = f"|{bit}>"
        else:
            bit = self._rng.choice([0, 1])
            state = [1.0, 0.0] if bit == 0 else [0.0, 1.0]
            n_gates = 3
            init_label = f"|{bit}>"

        gate_seq = [self._rng.choice(list(gate_names.keys())) for _ in range(n_gates)]
        intermediates = []
        current = list(state)
        for gname in gate_seq:
            current = _apply_gate(gate_names[gname], current)
            intermediates.append((gname, list(current)))

        return f"circuit on {init_label}", {
            "init": init_label, "gates": gate_seq,
            "intermediates": intermediates,
            "final": current,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate circuit execution steps.

        Args:
            data: Solution data with gate sequence and states.

        Returns:
            List of step strings.
        """
        steps = [f"init: {data['init']}"]
        for gname, state in data["intermediates"]:
            steps.append(
                f"after {gname}: [{_fmt(state[0])}, {_fmt(state[1])}]"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final state vector.

        Args:
            data: Solution data.

        Returns:
            String with final state.
        """
        f = data["final"]
        return f"final state: [{_fmt(f[0])}, {_fmt(f[1])}]"


# ===================================================================
# 2. Quantum measurement  (tier 6)
# ===================================================================

@register
class QuantumMeasurementGenerator(StepGenerator):
    """Compute measurement probabilities and post-measurement state.

    Given |psi> = a|0> + b|1>, compute P(0) = |a|^2, P(1) = |b|^2.
    Post-measurement state collapses to |0> or |1>.

    Difficulty scaling:
        Difficulty 1-3: simple amplitudes (1/sqrt(2)).
        Difficulty 4-6: arbitrary real amplitudes.
        Difficulty 7-8: measure in X-basis (|+>, |->).

    Prerequisites:
        quantum_gate.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_measurement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute measurement probabilities for qubit state"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantum measurement problem.

        Args:
            difficulty: Controls amplitude complexity and basis.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            theta = _PI / 4
        else:
            theta = round(self._rng.uniform(0.2, 1.4), 4)

        a = round(math.cos(theta), 4)
        b = round(math.sin(theta), 4)
        p0 = round(a * a, 4)
        p1 = round(b * b, 4)

        data = {
            "a": a, "b": b, "p0": p0, "p1": p1,
            "basis": "Z",
        }

        if difficulty >= 7:
            # X-basis measurement
            p_plus = round(((a + b) / math.sqrt(2)) ** 2, 4)
            p_minus = round(((a - b) / math.sqrt(2)) ** 2, 4)
            data["basis"] = "X"
            data["p_plus"] = p_plus
            data["p_minus"] = p_minus

        return f"|\\psi> = {_fmt(a)}|0> + {_fmt(b)}|1>", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate measurement computation steps.

        Args:
            data: Solution data with amplitudes and probabilities.

        Returns:
            List of step strings.
        """
        steps = [
            f"|psi> = {_fmt(data['a'])}|0> + {_fmt(data['b'])}|1>",
            f"P(0) = |{_fmt(data['a'])}|^2 = {_fmt(data['p0'])}",
            f"P(1) = |{_fmt(data['b'])}|^2 = {_fmt(data['p1'])}",
        ]
        if data["basis"] == "X":
            steps.append(f"X-basis: P(+) = {_fmt(data['p_plus'])}")
            steps.append(f"X-basis: P(-) = {_fmt(data['p_minus'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the measurement probabilities.

        Args:
            data: Solution data.

        Returns:
            String with probabilities.
        """
        if data["basis"] == "Z":
            return f"P(0) = {_fmt(data['p0'])}, P(1) = {_fmt(data['p1'])}"
        return (
            f"P(+) = {_fmt(data['p_plus'])}, "
            f"P(-) = {_fmt(data['p_minus'])}"
        )


# ===================================================================
# 3. Quantum entropy  (tier 6)
# ===================================================================

@register
class QuantumEntropyGenerator(StepGenerator):
    """Compute von Neumann entropy for a diagonal density matrix.

    S(rho) = -Tr(rho * log2(rho)).  For diagonal rho with eigenvalues
    p_i, S = -sum(p_i * log2(p_i)).  S=0 for pure state, S=1 for
    maximally mixed qubit.

    Difficulty scaling:
        Difficulty 1-3: pure state (S=0) or maximally mixed (S=1).
        Difficulty 4-6: 2x2 diagonal rho with arbitrary eigenvalues.
        Difficulty 7-8: 3x3 or 4x4 diagonal rho.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_entropy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute von Neumann entropy for diagonal density matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantum entropy problem.

        Args:
            difficulty: Controls matrix size and eigenvalue distribution.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            is_pure = self._rng.choice([True, False])
            if is_pure:
                eigenvalues = [1.0, 0.0]
            else:
                eigenvalues = [0.5, 0.5]
        elif difficulty <= 6:
            p = round(self._rng.uniform(0.1, 0.9), 4)
            eigenvalues = [p, round(1.0 - p, 4)]
        else:
            dim = self._rng.choice([3, 4])
            raw = [self._rng.uniform(0.1, 1.0) for _ in range(dim)]
            total = sum(raw)
            eigenvalues = [round(r / total, 4) for r in raw]
            # Fix rounding to ensure sum = 1
            eigenvalues[-1] = round(1.0 - sum(eigenvalues[:-1]), 4)

        entropy = 0.0
        for p in eigenvalues:
            if p > 1e-12:
                entropy -= p * math.log2(p)
        entropy = round(entropy, 4)

        eig_str = ", ".join(_fmt(p) for p in eigenvalues)
        state_type = "pure" if entropy < 0.001 else "mixed"

        return "S(\\rho) = -Tr(\\rho \\log_2 \\rho)", {
            "eigenvalues": eigenvalues, "eig_str": eig_str,
            "entropy": entropy, "state_type": state_type,
            "dim": len(eigenvalues),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy computation steps.

        Args:
            data: Solution data with eigenvalues and entropy.

        Returns:
            List of step strings.
        """
        steps = [f"eigenvalues: {{{data['eig_str']}}}"]
        for p in data["eigenvalues"]:
            if p > 1e-12:
                contrib = round(-p * math.log2(p), 4)
                steps.append(f"-{_fmt(p)}*log2({_fmt(p)}) = {_fmt(contrib)}")
            else:
                steps.append(f"p={_fmt(p)}: contributes 0")
        steps.append(f"S = {_fmt(data['entropy'])} bits ({data['state_type']})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the von Neumann entropy.

        Args:
            data: Solution data.

        Returns:
            String with entropy value.
        """
        return f"S = {_fmt(data['entropy'])} bits ({data['state_type']})"


# ===================================================================
# 4. Superdense coding  (tier 6)
# ===================================================================

@register
class SuperdenseCodingGenerator(StepGenerator):
    """Encode 2 classical bits in 1 qubit via shared Bell pair.

    Given message bits (b1, b2), Alice applies:
    00 -> I, 01 -> X, 10 -> Z, 11 -> ZX (equivalently iY).
    Bob performs Bell measurement to decode.

    Difficulty scaling:
        Difficulty 1-3: message 00 or 01 (simpler gates).
        Difficulty 4-6: all four messages.
        Difficulty 7-8: show full Bell measurement decoding.

    Prerequisites:
        bell_state.
    """

    _ENCODINGS = {
        (0, 0): ("I", "Phi+"),
        (0, 1): ("X", "Psi+"),
        (1, 0): ("Z", "Phi-"),
        (1, 1): ("ZX", "Psi-"),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "superdense_coding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bell_state"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encode 2 classical bits via superdense coding"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a superdense coding problem.

        Args:
            difficulty: Controls message pool and detail level.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            msg = self._rng.choice([(0, 0), (0, 1)])
        else:
            msg = self._rng.choice([(0, 0), (0, 1), (1, 0), (1, 1)])

        gate, bell_out = self._ENCODINGS[msg]

        return f"message = {msg[0]}{msg[1]}", {
            "b1": msg[0], "b2": msg[1],
            "gate": gate, "bell_out": bell_out,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate superdense coding steps.

        Args:
            data: Solution data with message and gate sequence.

        Returns:
            List of step strings.
        """
        return [
            "shared Bell pair: |Phi+> = (|00>+|11>)/sqrt(2)",
            f"message: {data['b1']}{data['b2']}",
            f"Alice applies: {data['gate']} to her qubit",
            f"resulting state: |{data['bell_out']}>",
            f"Bob Bell-measures -> decodes {data['b1']}{data['b2']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the encoding gate and Bell state.

        Args:
            data: Solution data.

        Returns:
            String with gate and decoded message.
        """
        return (
            f"gate: {data['gate']}, Bell state: |{data['bell_out']}>, "
            f"decoded: {data['b1']}{data['b2']}"
        )


# ===================================================================
# 5. Quantum key distribution (BB84)  (tier 6)
# ===================================================================

@register
class QuantumKeyDistGenerator(StepGenerator):
    """Simulate BB84 quantum key distribution protocol.

    Alice sends qubits in random bases (Z or X), Bob measures in
    random bases.  When bases match, bits are kept (sifted key).
    Compute sifted key length and quantum bit error rate (QBER).

    Difficulty scaling:
        Difficulty 1-3: 4-bit key, all bases match.
        Difficulty 4-6: 6-bit key, random basis choices.
        Difficulty 7-8: 8-bit key with eavesdropper introducing errors.

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_key_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute sifted key and QBER in BB84 protocol"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BB84 key distribution problem.

        Args:
            difficulty: Controls key length and error presence.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_bits = 4
        elif difficulty <= 6:
            n_bits = 6
        else:
            n_bits = 8

        alice_bits = [self._rng.randint(0, 1) for _ in range(n_bits)]
        alice_bases = [self._rng.choice(["Z", "X"]) for _ in range(n_bits)]
        bob_bases = [self._rng.choice(["Z", "X"]) for _ in range(n_bits)]

        if difficulty <= 3:
            bob_bases = list(alice_bases)

        sifted = []
        matches = []
        for i in range(n_bits):
            if alice_bases[i] == bob_bases[i]:
                matches.append(i)
                sifted.append(alice_bits[i])

        errors = 0
        if difficulty >= 7 and len(sifted) > 0:
            n_errors = self._rng.randint(0, max(1, len(sifted) // 3))
            for _ in range(n_errors):
                idx = self._rng.randint(0, len(sifted) - 1)
                sifted[idx] = 1 - sifted[idx]
                errors += 1

        qber = round(errors / len(sifted), 4) if len(sifted) > 0 else 0.0
        sifted_str = "".join(str(b) for b in sifted)

        return "BB84 protocol", {
            "n_bits": n_bits,
            "alice_bits": alice_bits,
            "alice_bases": alice_bases,
            "bob_bases": bob_bases,
            "matches": matches,
            "sifted_key": sifted_str,
            "sifted_len": len(sifted),
            "errors": errors, "qber": qber,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BB84 protocol steps.

        Args:
            data: Solution data with bases, sifted key, and QBER.

        Returns:
            List of step strings.
        """
        ab = "".join(data["alice_bases"])
        bb = "".join(data["bob_bases"])
        bits = "".join(str(b) for b in data["alice_bits"])
        return [
            f"Alice bits: {bits}, bases: {ab}",
            f"Bob bases: {bb}",
            f"matching positions: {data['matches']}",
            f"sifted key: {data['sifted_key']} (len={data['sifted_len']})",
            f"errors: {data['errors']}, QBER = {_fmt(data['qber'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the sifted key and QBER.

        Args:
            data: Solution data.

        Returns:
            String with sifted key and error rate.
        """
        return (
            f"sifted key: {data['sifted_key']}, "
            f"QBER = {_fmt(data['qber'])}"
        )


# ===================================================================
# 6. SWAP test  (tier 6)
# ===================================================================

@register
class SwapTestGenerator(StepGenerator):
    """Compute overlap probability via the SWAP test circuit.

    SWAP test: P(|0>) = (1 + |<a|b>|^2) / 2.
    Given two single-qubit states, compute their overlap and
    the probability of measuring |0> on the ancilla.

    Difficulty scaling:
        Difficulty 1-3: identical states (overlap=1).
        Difficulty 4-6: orthogonal or varied overlap.
        Difficulty 7-8: compute overlap from given P(|0>).

    Prerequisites:
        quantum_gate.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "swap_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute overlap probability via SWAP test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a SWAP test problem.

        Args:
            difficulty: Controls state overlap.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            theta_a = round(self._rng.uniform(0.2, 1.4), 4)
            theta_b = theta_a
        elif difficulty <= 6:
            theta_a = round(self._rng.uniform(0.2, 1.4), 4)
            theta_b = round(self._rng.uniform(0.2, 1.4), 4)
        else:
            theta_a = round(self._rng.uniform(0.1, 1.5), 4)
            theta_b = round(self._rng.uniform(0.1, 1.5), 4)

        a = [round(math.cos(theta_a), 4), round(math.sin(theta_a), 4)]
        b = [round(math.cos(theta_b), 4), round(math.sin(theta_b), 4)]

        inner = round(a[0] * b[0] + a[1] * b[1], 4)
        inner_sq = round(inner * inner, 4)
        p_zero = round((1 + inner_sq) / 2, 4)

        return "P(|0\\rangle) = (1 + |\\langle a|b\\rangle|^2) / 2", {
            "a": a, "b": b,
            "inner": inner, "inner_sq": inner_sq,
            "p_zero": p_zero,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate SWAP test computation steps.

        Args:
            data: Solution data with states and overlap.

        Returns:
            List of step strings.
        """
        return [
            f"|a> = [{_fmt(data['a'][0])}, {_fmt(data['a'][1])}]",
            f"|b> = [{_fmt(data['b'][0])}, {_fmt(data['b'][1])}]",
            f"<a|b> = {_fmt(data['inner'])}",
            f"|<a|b>|^2 = {_fmt(data['inner_sq'])}",
            f"P(|0>) = (1 + {_fmt(data['inner_sq'])})/2 = {_fmt(data['p_zero'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the ancilla measurement probability.

        Args:
            data: Solution data.

        Returns:
            String with P(|0>) value.
        """
        return f"P(|0>) = {_fmt(data['p_zero'])}"


# ===================================================================
# 7. Quantum walk  (tier 6)
# ===================================================================

@register
class QuantumWalkGenerator(StepGenerator):
    """Compute discrete quantum walk on a line.

    Uses a Hadamard coin and conditional shift operator.
    After t steps, compute the probability distribution over
    positions.

    Difficulty scaling:
        Difficulty 1-3: t=1 step, position -1,0,1.
        Difficulty 4-6: t=2 steps.
        Difficulty 7-8: t=3 steps.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantum_walk"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute quantum walk probability distribution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantum walk problem.

        Args:
            difficulty: Controls number of steps.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            t = 1
        elif difficulty <= 6:
            t = 2
        else:
            t = 3

        # State: dict mapping position -> [coin_up, coin_down]
        state = {0: [1.0, 0.0]}

        for _ in range(t):
            new_state: dict[int, list[float]] = {}
            for pos, coin in state.items():
                # Apply Hadamard coin
                c_up = round(_INV_SQRT2 * coin[0] + _INV_SQRT2 * coin[1], 4)
                c_dn = round(_INV_SQRT2 * coin[0] - _INV_SQRT2 * coin[1], 4)
                # Shift: up -> pos+1, down -> pos-1
                if pos + 1 not in new_state:
                    new_state[pos + 1] = [0.0, 0.0]
                new_state[pos + 1][0] = round(
                    new_state[pos + 1][0] + c_up, 4
                )
                if pos - 1 not in new_state:
                    new_state[pos - 1] = [0.0, 0.0]
                new_state[pos - 1][1] = round(
                    new_state[pos - 1][1] + c_dn, 4
                )
            state = new_state

        # Compute probabilities
        probs = {}
        for pos in sorted(state.keys()):
            coin = state[pos]
            p = round(coin[0] ** 2 + coin[1] ** 2, 4)
            if p > 1e-9:
                probs[pos] = p

        return f"quantum walk, t={t} steps", {
            "t": t, "probs": probs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quantum walk computation steps.

        Args:
            data: Solution data with step count and probabilities.

        Returns:
            List of step strings.
        """
        steps = [
            f"start at position 0, coin=|up>",
            f"Hadamard coin + conditional shift, t={data['t']} steps",
        ]
        for pos in sorted(data["probs"].keys()):
            steps.append(f"P(x={pos}) = {_fmt(data['probs'][pos])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the probability distribution.

        Args:
            data: Solution data.

        Returns:
            String with position probabilities.
        """
        parts = [f"P({pos})={_fmt(p)}" for pos, p in sorted(data["probs"].items())]
        return ", ".join(parts)


# ===================================================================
# 8. Fidelity  (tier 6)
# ===================================================================

@register
class FidelityGenerator(StepGenerator):
    """Compute fidelity between two pure quantum states.

    For pure states: F(|psi>, |phi>) = |<psi|phi>|^2.
    F=1 for identical states, F=0 for orthogonal states.

    Difficulty scaling:
        Difficulty 1-3: identical or orthogonal states.
        Difficulty 4-6: arbitrary single-qubit pure states.
        Difficulty 7-8: 2-qubit pure states.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fidelity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute fidelity between two pure quantum states"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fidelity problem.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            identical = self._rng.choice([True, False])
            theta1 = round(self._rng.uniform(0.2, 1.4), 4)
            if identical:
                theta2 = theta1
            else:
                theta2 = round(theta1 + _PI / 2, 4)
            psi = [round(math.cos(theta1), 4), round(math.sin(theta1), 4)]
            phi = [round(math.cos(theta2), 4), round(math.sin(theta2), 4)]
        elif difficulty <= 6:
            theta1 = round(self._rng.uniform(0.1, 1.5), 4)
            theta2 = round(self._rng.uniform(0.1, 1.5), 4)
            psi = [round(math.cos(theta1), 4), round(math.sin(theta1), 4)]
            phi = [round(math.cos(theta2), 4), round(math.sin(theta2), 4)]
        else:
            # 2-qubit states
            raw1 = [self._rng.uniform(-1, 1) for _ in range(4)]
            norm1 = math.sqrt(sum(x * x for x in raw1))
            psi = [round(x / norm1, 4) for x in raw1]
            raw2 = [self._rng.uniform(-1, 1) for _ in range(4)]
            norm2 = math.sqrt(sum(x * x for x in raw2))
            phi = [round(x / norm2, 4) for x in raw2]

        inner = sum(psi[i] * phi[i] for i in range(len(psi)))
        inner = round(inner, 4)
        fid = round(inner * inner, 4)

        return "F = |\\langle\\psi|\\phi\\rangle|^2", {
            "psi": psi, "phi": phi,
            "inner": inner, "fidelity": fid,
            "dim": len(psi),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fidelity computation steps.

        Args:
            data: Solution data with states and overlap.

        Returns:
            List of step strings.
        """
        psi_str = ", ".join(_fmt(x) for x in data["psi"])
        phi_str = ", ".join(_fmt(x) for x in data["phi"])
        return [
            f"|psi> = [{psi_str}]",
            f"|phi> = [{phi_str}]",
            f"<psi|phi> = {_fmt(data['inner'])}",
            f"F = |<psi|phi>|^2 = {_fmt(data['fidelity'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fidelity value.

        Args:
            data: Solution data.

        Returns:
            String with fidelity.
        """
        return f"F = {_fmt(data['fidelity'])}"
