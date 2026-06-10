"""Quantum error correction generators.

6 generators across tiers 6-7 covering the bit-flip code, phase-flip
code, Shor 9-qubit code, stabilizer checks, the Steane [[7,1,3]] code,
and logical operator identification.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Pauli helpers
# ---------------------------------------------------------------------------

_PAULI_LABELS = {"I": 0, "X": 1, "Y": 2, "Z": 3}

_PAULI_COMMUTE = [
    # I  X  Y  Z
    [0, 0, 0, 0],  # I
    [0, 0, 1, 1],  # X
    [0, 1, 0, 1],  # Y
    [0, 1, 1, 0],  # Z
]


def _paulis_commute(s1: str, s2: str) -> bool:
    """Check if two Pauli strings commute.

    Two n-qubit Pauli strings commute iff the number of
    positions where they anti-commute is even.

    Args:
        s1: First Pauli string (e.g. "XZI").
        s2: Second Pauli string (same length).

    Returns:
        True if the operators commute.
    """
    anticommute_count = 0
    for c1, c2 in zip(s1, s2):
        idx1 = _PAULI_LABELS[c1]
        idx2 = _PAULI_LABELS[c2]
        anticommute_count += _PAULI_COMMUTE[idx1][idx2]
    return anticommute_count % 2 == 0


def _flip_bit(bitstring: str, pos: int) -> str:
    """Flip a single bit in a bitstring.

    Args:
        bitstring: String of '0' and '1'.
        pos: 0-indexed position to flip.

    Returns:
        Modified bitstring.
    """
    bits = list(bitstring)
    bits[pos] = "1" if bits[pos] == "0" else "0"
    return "".join(bits)


# ---------------------------------------------------------------------------
# 1. Bit-flip code (tier 6)
# ---------------------------------------------------------------------------

@register
class BitFlipCodeGenerator(StepGenerator):
    """Encode a qubit in the 3-qubit bit-flip code and correct errors.

    Encodes |psi> = a|0> + b|1> into a|000> + b|111>. Introduces a
    single bit-flip error on qubit i, computes the syndrome from
    Z1Z2 and Z2Z3 measurements, and identifies/corrects the error.

    Difficulty scaling:
        Difficulty 1-3: error on qubit 1 or 3.
        Difficulty 4-6: error on any single qubit.
        Difficulty 7-8: includes no-error case.

    Prerequisites:
        quantum_gate (tier 6).
    """

    _SYNDROME_TABLE = {
        0: ("Z1Z2=+1, Z2Z3=+1", "no error"),
        1: ("Z1Z2=-1, Z2Z3=+1", "error on qubit 1"),
        2: ("Z1Z2=-1, Z2Z3=-1", "error on qubit 2"),
        3: ("Z1Z2=+1, Z2Z3=-1", "error on qubit 3"),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bit_flip_code"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encode, detect, and correct bit-flip error"

    def _select_error(self, difficulty: int) -> int:
        """Select which qubit has the error.

        Args:
            difficulty: Controls error position pool.

        Returns:
            Error qubit (0=none, 1-3=qubit index).
        """
        if difficulty <= 3:
            return self._rng.choice([1, 3])
        if difficulty <= 6:
            return self._rng.choice([1, 2, 3])
        return self._rng.choice([0, 1, 2, 3])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bit-flip code problem.

        Args:
            difficulty: Controls error position.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        err = self._select_error(difficulty)
        enc0 = "000"
        enc1 = "111"
        err0 = _flip_bit(enc0, err - 1) if err > 0 else enc0
        err1 = _flip_bit(enc1, err - 1) if err > 0 else enc1
        syn_str, diagnosis = self._SYNDROME_TABLE[err]
        corrected0 = enc0
        corrected1 = enc1
        problem = (
            "|psi> = a|0>+b|1>. Encode in 3-qubit bit-flip code. "
            f"Error on qubit {err if err > 0 else 'none'}. "
            "Detect and correct."
        )
        return problem, {
            "err": err, "enc0": enc0, "enc1": enc1,
            "err0": err0, "err1": err1,
            "syndrome": syn_str, "diagnosis": diagnosis,
            "corrected0": corrected0, "corrected1": corrected1,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"encode: a|{sd['enc0']}> + b|{sd['enc1']}>",
        ]
        if sd["err"] > 0:
            steps.append(
                f"X on qubit {sd['err']}: "
                f"a|{sd['err0']}> + b|{sd['err1']}>"
            )
        else:
            steps.append("no error applied")
        steps.append(f"syndrome: {sd['syndrome']}")
        steps.append(f"diagnosis: {sd['diagnosis']}")
        if sd["err"] > 0:
            steps.append(
                f"apply X on qubit {sd['err']}: "
                f"a|{sd['corrected0']}> + b|{sd['corrected1']}>"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Diagnosis and corrected state.
        """
        return f"{sd['diagnosis']}, corrected: a|000>+b|111>"


# ---------------------------------------------------------------------------
# 2. Phase-flip code (tier 6)
# ---------------------------------------------------------------------------

@register
class PhaseFlipCodeGenerator(StepGenerator):
    """Encode in the 3-qubit phase-flip code and detect phase errors.

    Encodes in the Hadamard basis: |0_L> = |+++>, |1_L> = |--->.
    A phase flip Z on qubit i is detected by measuring in the
    X-basis and computing syndrome bits.

    Difficulty scaling:
        Difficulty 1-3: error on qubit 1 or 3.
        Difficulty 4-6: error on any single qubit.
        Difficulty 7-8: includes no-error case.

    Prerequisites:
        bit_flip_code (tier 6).
    """

    _SYNDROME_TABLE = {
        0: ("X1X2=+1, X2X3=+1", "no error"),
        1: ("X1X2=-1, X2X3=+1", "phase error on qubit 1"),
        2: ("X1X2=-1, X2X3=-1", "phase error on qubit 2"),
        3: ("X1X2=+1, X2X3=-1", "phase error on qubit 3"),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phase_flip_code"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bit_flip_code"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "detect and correct phase-flip error"

    def _select_error(self, difficulty: int) -> int:
        """Select which qubit has the phase error.

        Args:
            difficulty: Controls error pool.

        Returns:
            Error qubit (0=none, 1-3=qubit index).
        """
        if difficulty <= 3:
            return self._rng.choice([1, 3])
        if difficulty <= 6:
            return self._rng.choice([1, 2, 3])
        return self._rng.choice([0, 1, 2, 3])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a phase-flip code problem.

        Args:
            difficulty: Controls error position.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        err = self._select_error(difficulty)
        syn_str, diagnosis = self._SYNDROME_TABLE[err]
        # In Hadamard basis: |+> = (|0>+|1>)/sqrt(2), |-> = (|0>-|1>)/sqrt(2)
        # Z|+> = |->, Z|-> = |+>
        enc_0L = "+++"
        enc_1L = "---"
        if err > 0:
            e0 = list(enc_0L)
            e1 = list(enc_1L)
            e0[err - 1] = "-" if e0[err - 1] == "+" else "+"
            e1[err - 1] = "-" if e1[err - 1] == "+" else "+"
            err_0L = "".join(e0)
            err_1L = "".join(e1)
        else:
            err_0L = enc_0L
            err_1L = enc_1L

        problem = (
            "|psi> = a|0>+b|1>. Phase-flip code. "
            f"Z error on qubit {err if err > 0 else 'none'}. "
            "Detect and correct."
        )
        return problem, {
            "err": err, "enc_0L": enc_0L, "enc_1L": enc_1L,
            "err_0L": err_0L, "err_1L": err_1L,
            "syndrome": syn_str, "diagnosis": diagnosis,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"encode in H-basis: a|{sd['enc_0L']}> + b|{sd['enc_1L']}>",
        ]
        if sd["err"] > 0:
            steps.append(
                f"Z on qubit {sd['err']}: "
                f"a|{sd['err_0L']}> + b|{sd['err_1L']}>"
            )
        else:
            steps.append("no error applied")
        steps.append(f"syndrome: {sd['syndrome']}")
        steps.append(f"diagnosis: {sd['diagnosis']}")
        if sd["err"] > 0:
            steps.append(f"apply Z on qubit {sd['err']} to correct")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Diagnosis and correction.
        """
        return f"{sd['diagnosis']}, corrected: a|+++>+b|--->"


# ---------------------------------------------------------------------------
# 3. Shor code (tier 7)
# ---------------------------------------------------------------------------

@register
class ShorCodeGenerator(StepGenerator):
    """Show the 9-qubit Shor code encoding.

    The Shor code concatenates the phase-flip code with the bit-flip
    code: each logical qubit is encoded into 3 blocks of 3 physical
    qubits. Shows the encoding of |0_L> and |1_L>.

    Difficulty scaling:
        Difficulty 1-3: show encoding of |0_L> only.
        Difficulty 4-6: show encoding of both |0_L> and |1_L>.
        Difficulty 7-8: introduce a single error and identify syndrome.

    Prerequisites:
        phase_flip_code (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "shor_code"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["phase_flip_code"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encode in 9-qubit Shor code"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Shor code encoding problem.

        Args:
            difficulty: Controls detail level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # |0_L> = (|000>+|111>)(|000>+|111>)(|000>+|111>) / 2sqrt(2)
        # |1_L> = (|000>-|111>)(|000>-|111>)(|000>-|111>) / 2sqrt(2)
        enc_0 = "(|000>+|111>)^{x3} / 2sqrt(2)"
        enc_1 = "(|000>-|111>)^{x3} / 2sqrt(2)"

        if difficulty <= 3:
            show_both = False
            err_qubit = 0
            err_type = "none"
        elif difficulty <= 6:
            show_both = True
            err_qubit = 0
            err_type = "none"
        else:
            show_both = True
            err_qubit = self._rng.randint(1, 9)
            err_type = self._rng.choice(["X", "Z"])

        # Determine which block and position for the error
        block = (err_qubit - 1) // 3 + 1 if err_qubit > 0 else 0
        pos_in_block = (err_qubit - 1) % 3 + 1 if err_qubit > 0 else 0

        problem = f"|psi> = a|0>+b|1>. Show Shor code encoding."
        return problem, {
            "enc_0": enc_0, "enc_1": enc_1,
            "show_both": show_both,
            "err_qubit": err_qubit, "err_type": err_type,
            "block": block, "pos_in_block": pos_in_block,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            "phase-flip: |0> -> |+++>, |1> -> |--->",
            "bit-flip each: |+> -> (|000>+|111>)/sqrt(2)",
            "|0_L> = (|000>+|111>)^3 / 2sqrt(2)",
        ]
        if sd["show_both"]:
            steps.append("|1_L> = (|000>-|111>)^3 / 2sqrt(2)")
        if sd["err_qubit"] > 0:
            steps.append(
                f"{sd['err_type']} error on qubit {sd['err_qubit']} "
                f"(block {sd['block']}, pos {sd['pos_in_block']})"
            )
            if sd["err_type"] == "X":
                steps.append("bit-flip detected by Z-syndrome in block")
            else:
                steps.append("phase-flip detected by X-syndrome across blocks")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Encoding summary.
        """
        if sd["err_qubit"] > 0:
            return (
                f"9-qubit Shor code, {sd['err_type']} error on "
                f"qubit {sd['err_qubit']} detectable"
            )
        return "9-qubit Shor code encodes 1 logical qubit"


# ---------------------------------------------------------------------------
# 4. Stabilizer check (tier 7)
# ---------------------------------------------------------------------------

@register
class StabilizerCheckGenerator(StepGenerator):
    """Verify that stabilizer generators commute and check code space.

    Given a set of Pauli string stabilizer generators, verifies they
    all mutually commute (required for a valid stabilizer code) and
    checks whether a given error commutes with or anti-commutes with
    each generator (to determine syndrome).

    Difficulty scaling:
        Difficulty 1-3: 2 generators on 3 qubits.
        Difficulty 4-6: 3 generators on 5 qubits.
        Difficulty 7-8: 4 generators on 7 qubits.

    Prerequisites:
        quantum_gate (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stabilizer_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantum_gate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify stabilizer generators commute, compute syndrome"

    def _make_pauli_string(self, n: int) -> str:
        """Generate a random Pauli string of length n.

        Args:
            n: Number of qubits.

        Returns:
            String of I, X, Y, Z characters.
        """
        return "".join(self._rng.choice(["I", "X", "Y", "Z"])
                       for _ in range(n))

    def _make_stabilizer_set(self, n_qubits: int,
                             n_gens: int) -> list[str]:
        """Generate mutually commuting Pauli string generators.

        Generates random Pauli strings and keeps them if they commute
        with all previously accepted generators.

        Args:
            n_qubits: Number of qubits.
            n_gens: Number of generators to produce.

        Returns:
            List of commuting Pauli strings.
        """
        gens: list[str] = []
        attempts = 0
        while len(gens) < n_gens and attempts < 200:
            candidate = self._make_pauli_string(n_qubits)
            if candidate == "I" * n_qubits:
                attempts += 1
                continue
            if all(_paulis_commute(candidate, g) for g in gens):
                gens.append(candidate)
            attempts += 1
        return gens

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stabilizer check problem.

        Args:
            difficulty: Controls generator and qubit count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_qubits, n_gens = 3, 2
        elif difficulty <= 6:
            n_qubits, n_gens = 5, 3
        else:
            n_qubits, n_gens = 7, 4

        generators = self._make_stabilizer_set(n_qubits, n_gens)

        # Pad if we didn't get enough (rare)
        while len(generators) < n_gens:
            filler = "Z" + "I" * (n_qubits - 1)
            if filler not in generators:
                generators.append(filler)
            else:
                generators.append("X" + "I" * (n_qubits - 1))
                break

        # Check all pairs commute
        all_commute = True
        non_commuting_pair = None
        for i in range(len(generators)):
            for j in range(i + 1, len(generators)):
                if not _paulis_commute(generators[i], generators[j]):
                    all_commute = False
                    non_commuting_pair = (generators[i], generators[j])
                    break
            if not all_commute:
                break

        # Generate an error and compute syndrome
        error_pos = self._rng.randint(0, n_qubits - 1)
        error_op = self._rng.choice(["X", "Y", "Z"])
        error_str = "I" * error_pos + error_op + "I" * (n_qubits - 1 - error_pos)
        syndrome = []
        for g in generators:
            syndrome.append(0 if _paulis_commute(error_str, g) else 1)

        gen_str = ", ".join(generators)
        problem = (
            f"generators: {gen_str}. "
            f"Error: {error_str}. Verify and find syndrome."
        )
        return problem, {
            "generators": generators,
            "n_qubits": n_qubits,
            "all_commute": all_commute,
            "non_commuting_pair": non_commuting_pair,
            "error_str": error_str,
            "syndrome": syndrome,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        gens = sd["generators"]
        steps = []
        # Check commutativity
        for i in range(len(gens)):
            for j in range(i + 1, len(gens)):
                c = _paulis_commute(gens[i], gens[j])
                steps.append(
                    f"[{gens[i]}, {gens[j]}]: "
                    f"{'commute' if c else 'anti-commute'}"
                )
        if sd["all_commute"]:
            steps.append("all generators commute: valid stabilizer")
        else:
            steps.append("NOT all commute: invalid stabilizer")
        # Syndrome
        for i, g in enumerate(gens):
            c = _paulis_commute(sd["error_str"], g)
            steps.append(
                f"E vs g{i + 1}: {'commute(0)' if c else 'anti-commute(1)'}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Commutativity result and syndrome.
        """
        syn = "".join(str(b) for b in sd["syndrome"])
        valid = "valid" if sd["all_commute"] else "invalid"
        return f"{valid} stabilizer, syndrome={syn}"


# ---------------------------------------------------------------------------
# 5. Steane code (tier 7)
# ---------------------------------------------------------------------------

@register
class SteaneCodeGenerator(StepGenerator):
    """Compute the syndrome for the [[7,1,3]] Steane code.

    The Steane code is derived from the classical [7,4,3] Hamming code.
    Given a specific error pattern, computes the syndrome using the
    Steane code's X-type and Z-type stabilizer generators.

    Difficulty scaling:
        Difficulty 1-3: single X error.
        Difficulty 4-6: single Z error.
        Difficulty 7-8: single Y error (triggers both syndromes).

    Prerequisites:
        stabilizer_check (tier 7).
    """

    # Steane code stabilizer generators
    _X_STABS = [
        "IIIXXXX",
        "IXXIIXX",
        "XIXIXIX",
    ]
    _Z_STABS = [
        "IIIZZZZ",
        "IZZIIZZ",
        "ZIZIZIZ",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "steane_code"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["stabilizer_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Steane [[7,1,3]] code syndrome"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Steane code syndrome problem.

        Args:
            difficulty: Controls error type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        err_pos = self._rng.randint(0, 6)  # 0-indexed qubit

        if difficulty <= 3:
            err_type = "X"
        elif difficulty <= 6:
            err_type = "Z"
        else:
            err_type = "Y"

        error_str = "I" * err_pos + err_type + "I" * (6 - err_pos)

        # X-syndrome: from Z stabilizers (detect X and Y errors)
        x_syndrome = []
        for zs in self._Z_STABS:
            x_syndrome.append(0 if _paulis_commute(error_str, zs) else 1)

        # Z-syndrome: from X stabilizers (detect Z and Y errors)
        z_syndrome = []
        for xs in self._X_STABS:
            z_syndrome.append(0 if _paulis_commute(error_str, xs) else 1)

        problem = (
            f"Steane [[7,1,3]] code. Error: {err_type} on "
            f"qubit {err_pos + 1}. Compute syndrome."
        )
        return problem, {
            "err_pos": err_pos, "err_type": err_type,
            "error_str": error_str,
            "x_syndrome": x_syndrome,
            "z_syndrome": z_syndrome,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"error: {sd['err_type']} on qubit {sd['err_pos'] + 1}",
            f"error string: {sd['error_str']}",
        ]
        # X-type syndrome
        for i, zs in enumerate(self._Z_STABS):
            c = _paulis_commute(sd["error_str"], zs)
            steps.append(
                f"Z-stab {i + 1} ({zs}): {'0' if c else '1'}"
            )
        # Z-type syndrome
        for i, xs in enumerate(self._X_STABS):
            c = _paulis_commute(sd["error_str"], xs)
            steps.append(
                f"X-stab {i + 1} ({xs}): {'0' if c else '1'}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Syndrome string.
        """
        xs = "".join(str(b) for b in sd["x_syndrome"])
        zs = "".join(str(b) for b in sd["z_syndrome"])
        return f"X-syndrome={xs}, Z-syndrome={zs}"


# ---------------------------------------------------------------------------
# 6. Logical operators (tier 7)
# ---------------------------------------------------------------------------

@register
class LogicalOperatorsGenerator(StepGenerator):
    """Find logical X and Z operators for a stabilizer code.

    Logical operators must commute with all stabilizer generators but
    not be in the stabilizer group. For the 3-qubit bit-flip code,
    logical X = XXX and logical Z = ZII (or any single Z). Verifies
    the commutation properties.

    Difficulty scaling:
        Difficulty 1-3: 3-qubit bit-flip code.
        Difficulty 4-6: 3-qubit phase-flip code.
        Difficulty 7-8: 5-qubit code with given generators.

    Prerequisites:
        stabilizer_check (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logical_operators"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["stabilizer_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find logical X and Z for stabilizer code"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logical operator identification problem.

        Args:
            difficulty: Controls code type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._bit_flip_case()
        if difficulty <= 6:
            return self._phase_flip_case()
        return self._five_qubit_case()

    def _bit_flip_case(self) -> tuple[str, dict]:
        """Generate logical operators for the 3-qubit bit-flip code.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        stabs = ["ZZI", "IZZ"]
        log_x = "XXX"
        log_z = "ZII"
        # Verify: log_x commutes with all stabs
        x_commutes = [_paulis_commute(log_x, s) for s in stabs]
        z_commutes = [_paulis_commute(log_z, s) for s in stabs]
        # log_x and log_z must anti-commute with each other
        xz_anticommute = not _paulis_commute(log_x, log_z)
        problem = (
            f"3-qubit bit-flip code. Stabilizers: {', '.join(stabs)}. "
            f"Find logical X_L and Z_L."
        )
        return problem, {
            "code": "bit_flip_3", "stabs": stabs,
            "log_x": log_x, "log_z": log_z,
            "x_commutes": x_commutes, "z_commutes": z_commutes,
            "xz_anticommute": xz_anticommute,
        }

    def _phase_flip_case(self) -> tuple[str, dict]:
        """Generate logical operators for the 3-qubit phase-flip code.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        stabs = ["XXI", "IXX"]
        log_x = "XII"
        log_z = "ZZZ"
        x_commutes = [_paulis_commute(log_x, s) for s in stabs]
        z_commutes = [_paulis_commute(log_z, s) for s in stabs]
        xz_anticommute = not _paulis_commute(log_x, log_z)
        problem = (
            f"3-qubit phase-flip code. Stabilizers: {', '.join(stabs)}. "
            f"Find logical X_L and Z_L."
        )
        return problem, {
            "code": "phase_flip_3", "stabs": stabs,
            "log_x": log_x, "log_z": log_z,
            "x_commutes": x_commutes, "z_commutes": z_commutes,
            "xz_anticommute": xz_anticommute,
        }

    def _five_qubit_case(self) -> tuple[str, dict]:
        """Generate logical operators for the [[5,1,3]] code.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        stabs = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
        log_x = "XXXXX"
        log_z = "ZZZZZ"
        x_commutes = [_paulis_commute(log_x, s) for s in stabs]
        z_commutes = [_paulis_commute(log_z, s) for s in stabs]
        xz_anticommute = not _paulis_commute(log_x, log_z)
        problem = (
            f"[[5,1,3]] code. Stabilizers: {', '.join(stabs)}. "
            f"Find logical X_L and Z_L."
        )
        return problem, {
            "code": "five_qubit", "stabs": stabs,
            "log_x": log_x, "log_z": log_z,
            "x_commutes": x_commutes, "z_commutes": z_commutes,
            "xz_anticommute": xz_anticommute,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"code: {sd['code']}"]
        for i, s in enumerate(sd["stabs"]):
            cx = "commute" if sd["x_commutes"][i] else "anti-commute"
            cz = "commute" if sd["z_commutes"][i] else "anti-commute"
            steps.append(f"X_L vs {s}: {cx}, Z_L vs {s}: {cz}")
        xz = "anti-commute" if sd["xz_anticommute"] else "commute"
        steps.append(f"X_L vs Z_L: {xz}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Logical operators.
        """
        return f"X_L={sd['log_x']}, Z_L={sd['log_z']}"
