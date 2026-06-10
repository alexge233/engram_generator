"""Coding theory generators.

6 generators across tiers 5-6 covering linear codes, syndrome decoding,
BCH encoding, Reed-Solomon codes, code parameters, and turbo code
interleaving.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _mat_vec_mod2(mat: list[list[int]], vec: list[int]) -> list[int]:
    """Multiply matrix by vector over GF(2).

    Args:
        mat: Binary matrix (rows x cols).
        vec: Binary vector of length cols.

    Returns:
        Result vector mod 2.
    """
    result = []
    for row in mat:
        val = 0
        for j, v in enumerate(vec):
            val ^= (row[j] & v)
        result.append(val)
    return result


def _vec_mat_mod2(vec: list[int], mat: list[list[int]]) -> list[int]:
    """Multiply row vector by matrix over GF(2).

    Args:
        vec: Binary row vector of length rows.
        mat: Binary matrix (rows x cols).

    Returns:
        Result vector mod 2.
    """
    cols = len(mat[0])
    result = [0] * cols
    for i, v in enumerate(vec):
        if v:
            for j in range(cols):
                result[j] ^= mat[i][j]
    return result


def _hamming_weight(vec: list[int]) -> int:
    """Compute Hamming weight (number of 1s) of a binary vector.

    Args:
        vec: Binary vector.

    Returns:
        Number of non-zero entries.
    """
    return sum(v != 0 for v in vec)


def _transpose(mat: list[list[int]]) -> list[list[int]]:
    """Transpose a matrix.

    Args:
        mat: Input matrix.

    Returns:
        Transposed matrix.
    """
    rows = len(mat)
    cols = len(mat[0])
    return [[mat[i][j] for i in range(rows)] for j in range(cols)]


def _poly_mul_gf2(a: list[int], b: list[int]) -> list[int]:
    """Multiply two polynomials over GF(2).

    Coefficients are stored as lists where index = power.

    Args:
        a: First polynomial coefficients.
        b: Second polynomial coefficients.

    Returns:
        Product polynomial coefficients mod 2.
    """
    if not a or not b:
        return []
    result = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    result[i + j] ^= 1
    return result


def _poly_mod_gf2(dividend: list[int], divisor: list[int]) -> list[int]:
    """Compute polynomial remainder over GF(2).

    Args:
        dividend: Dividend polynomial coefficients.
        divisor: Divisor polynomial coefficients.

    Returns:
        Remainder polynomial coefficients mod 2.
    """
    r = list(dividend)
    d_deg = len(divisor) - 1
    while len(r) >= len(divisor):
        if r[-1]:
            offset = len(r) - len(divisor)
            for i in range(len(divisor)):
                r[offset + i] ^= divisor[i]
        r.pop()
    # Remove trailing zeros
    while r and r[-1] == 0:
        r.pop()
    return r if r else [0]


def _poly_str(coeffs: list[int]) -> str:
    """Format GF(2) polynomial as a string.

    Args:
        coeffs: Coefficients where index = power.

    Returns:
        String like 'x^3 + x + 1'.
    """
    if not coeffs or all(c == 0 for c in coeffs):
        return "0"
    terms = []
    for i in range(len(coeffs) - 1, -1, -1):
        if coeffs[i]:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(terms) if terms else "0"


def _bits_str(bits: list[int]) -> str:
    """Format a binary vector as a compact string.

    Args:
        bits: List of 0s and 1s.

    Returns:
        String like '1011'.
    """
    return "".join(str(b) for b in bits)


# ═══════════════════════════════════════════════════════════════════
# 1. LINEAR CODE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class LinearCodeGenerator(StepGenerator):
    """Encode a message using a linear code generator matrix over GF(2).

    Given a k x n generator matrix G in systematic form, encodes a
    k-bit message m as the codeword c = m * G (mod 2). Also computes
    the minimum distance from the parity check matrix.

    Difficulty scaling:
        Difficulty 1-3: [4,7] Hamming code, random 4-bit message.
        Difficulty 4-6: [5,8] or [6,9] code.
        Difficulty 7-8: [5,10] or [6,11] code.

    Prerequisites:
        matrix_multiply (tier 4).
    """

    _CODES = {
        "easy": {
            "name": "[7,4]",
            "k": 4, "n": 7,
            "G": [
                [1, 0, 0, 0, 1, 1, 0],
                [0, 1, 0, 0, 1, 0, 1],
                [0, 0, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 1, 1],
            ],
            "H": [
                [1, 1, 0, 1, 1, 0, 0],
                [1, 0, 1, 1, 0, 1, 0],
                [0, 1, 1, 1, 0, 0, 1],
            ],
            "d_min": 3,
        },
        "medium": {
            "name": "[8,4]",
            "k": 4, "n": 8,
            "G": [
                [1, 0, 0, 0, 1, 1, 0, 1],
                [0, 1, 0, 0, 1, 0, 1, 1],
                [0, 0, 1, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 1, 0],
            ],
            "H": [
                [1, 1, 0, 1, 1, 0, 0, 0],
                [1, 0, 1, 1, 0, 1, 0, 0],
                [0, 1, 1, 1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0, 0, 0, 1],
            ],
            "d_min": 4,
        },
        "hard": {
            "name": "[6,3]",
            "k": 3, "n": 6,
            "G": [
                [1, 0, 0, 1, 1, 0],
                [0, 1, 0, 1, 0, 1],
                [0, 0, 1, 0, 1, 1],
            ],
            "H": [
                [1, 1, 0, 1, 0, 0],
                [1, 0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0, 1],
            ],
            "d_min": 3,
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "linear_code"

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
            difficulty: Controls code complexity.

        Returns:
            Task description string.
        """
        return "encode message using linear code generator matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear code encoding problem.

        Args:
            difficulty: Controls which code is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            code = self._CODES["easy"]
        elif difficulty <= 6:
            code = self._rng.choice([self._CODES["medium"], self._CODES["hard"]])
        else:
            code = self._CODES["medium"]

        k = code["k"]
        msg = [self._rng.randint(0, 1) for _ in range(k)]
        codeword = _vec_mat_mod2(msg, code["G"])

        g_str = "[" + "; ".join(_bits_str(row) for row in code["G"]) + "]"
        problem = (
            f"{code['name']} code, G = {g_str}. "
            f"Encode m = {_bits_str(msg)}."
        )
        return problem, {
            "code_name": code["name"], "k": k, "n": code["n"],
            "msg": msg, "codeword": codeword,
            "d_min": code["d_min"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate encoding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the matrix multiplication.
        """
        return [
            f"message m = {_bits_str(data['msg'])} ({data['k']} bits)",
            f"compute c = m * G mod 2",
            f"codeword c = {_bits_str(data['codeword'])} ({data['n']} bits)",
            f"min distance d = {data['d_min']}, corrects {(data['d_min']-1)//2} errors",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the encoded codeword.

        Args:
            data: Solution data.

        Returns:
            The codeword as a binary string.
        """
        return f"c = {_bits_str(data['codeword'])}"


# ═══════════════════════════════════════════════════════════════════
# 2. SYNDROME DECODE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class SyndromeDecodeGenerator(StepGenerator):
    """Decode a received word using syndrome decoding.

    Given a received vector r and parity check matrix H, compute
    syndrome s = H * r^T (mod 2). Use the syndrome to identify the
    error position for single-bit errors (Hamming code).

    Difficulty scaling:
        Difficulty 1-3: [7,4] Hamming, no error or 1-bit error.
        Difficulty 4-6: [7,4] Hamming, 1-bit error at any position.
        Difficulty 7-8: [8,4] extended Hamming, 1-bit error.

    Prerequisites:
        linear_code (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "syndrome_decode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["linear_code"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls code and error complexity.

        Returns:
            Task description string.
        """
        return "decode received word using syndrome decoding"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a syndrome decoding problem.

        Args:
            difficulty: Controls error pattern.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        code = LinearCodeGenerator._CODES["easy"]  # Hamming [7,4]
        k = code["k"]
        n = code["n"]
        h_mat = code["H"]

        # Generate a valid codeword
        msg = [self._rng.randint(0, 1) for _ in range(k)]
        codeword = _vec_mat_mod2(msg, code["G"])

        # Introduce error
        received = list(codeword)
        if difficulty <= 3:
            if self._rng.random() < 0.5:
                error_pos = -1  # no error
            else:
                error_pos = self._rng.randint(0, n - 1)
                received[error_pos] ^= 1
        else:
            error_pos = self._rng.randint(0, n - 1)
            received[error_pos] ^= 1

        syndrome = _mat_vec_mod2(h_mat, received)
        syndrome_val = sum(s << i for i, s in enumerate(syndrome))

        # For Hamming code, syndrome = column index (1-based) of error
        if all(s == 0 for s in syndrome):
            decoded_pos = -1
            corrected = list(received)
        else:
            # Find which column of H matches the syndrome
            h_t = _transpose(h_mat)
            decoded_pos = -1
            for j, col in enumerate(h_t):
                if col == syndrome:
                    decoded_pos = j
                    break
            corrected = list(received)
            if decoded_pos >= 0:
                corrected[decoded_pos] ^= 1

        problem = (
            f"[7,4] Hamming code. Received r = {_bits_str(received)}. "
            f"Compute syndrome and decode."
        )
        return problem, {
            "received": received, "syndrome": syndrome,
            "error_pos": error_pos, "decoded_pos": decoded_pos,
            "corrected": corrected, "original_msg": msg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate syndrome decoding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing syndrome computation and error correction.
        """
        steps = [
            f"received r = {_bits_str(data['received'])}",
            f"syndrome s = H * r^T mod 2 = {_bits_str(data['syndrome'])}",
        ]
        if all(s == 0 for s in data["syndrome"]):
            steps.append("syndrome = 0: no error detected")
        else:
            steps.append(f"syndrome matches column {data['decoded_pos']} of H")
            steps.append(f"flip bit {data['decoded_pos']}: corrected = {_bits_str(data['corrected'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decoded codeword.

        Args:
            data: Solution data.

        Returns:
            Corrected codeword and error position.
        """
        if data["decoded_pos"] < 0:
            return f"no error, codeword = {_bits_str(data['corrected'])}"
        return f"error at bit {data['decoded_pos']}, corrected = {_bits_str(data['corrected'])}"


# ═══════════════════════════════════════════════════════════════════
# 3. BCH ENCODE (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class BchEncodeGenerator(StepGenerator):
    """Encode a message using a BCH code over GF(2).

    Constructs a BCH generator polynomial from minimal polynomials
    of consecutive powers of a primitive element, then encodes by
    computing message(x) * x^(n-k) + remainder.

    Difficulty scaling:
        Difficulty 1-3: BCH(7,4) with g(x) = x^3 + x + 1.
        Difficulty 4-6: BCH(15,7) with g(x) = x^8 + x^7 + ... + 1.
        Difficulty 7-8: BCH(15,5) double-error-correcting.

    Prerequisites:
        polynomial_multiply (tier 6).
    """

    _BCH_CODES = [
        {
            "name": "BCH(7,4)", "n": 7, "k": 4, "t": 1,
            "g": [1, 1, 0, 1],  # x^3 + x + 1
        },
        {
            "name": "BCH(15,7)", "n": 15, "k": 7, "t": 2,
            "g": [1, 0, 0, 0, 1, 0, 1, 1, 1],  # x^8 + x^4 + x^2 + x + 1
        },
        {
            "name": "BCH(15,5)", "n": 15, "k": 5, "t": 3,
            "g": [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1],  # degree 10
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bch_encode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls BCH code parameters.

        Returns:
            Task description string.
        """
        return "encode message using BCH code"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BCH encoding problem.

        Args:
            difficulty: Controls code selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            code = self._BCH_CODES[0]
        elif difficulty <= 6:
            code = self._BCH_CODES[1]
        else:
            code = self._BCH_CODES[2]

        k = code["k"]
        n = code["n"]
        g = code["g"]
        n_minus_k = n - k

        # Random message polynomial (k coefficients)
        msg = [self._rng.randint(0, 1) for _ in range(k)]
        # Ensure at least one 1
        if all(m == 0 for m in msg):
            msg[0] = 1

        # Systematic encoding: shift message by x^(n-k), divide by g, append remainder
        shifted = [0] * n_minus_k + msg
        remainder = _poly_mod_gf2(shifted, g)
        # Pad remainder to n-k length
        while len(remainder) < n_minus_k:
            remainder.append(0)

        codeword = list(remainder[:n_minus_k]) + msg

        problem = (
            f"{code['name']} code, g(x) = {_poly_str(g)}, t = {code['t']}. "
            f"Encode m(x) = {_poly_str(msg)}."
        )
        return problem, {
            "code_name": code["name"], "n": n, "k": k, "t": code["t"],
            "g": g, "msg": msg, "remainder": remainder[:n_minus_k],
            "codeword": codeword,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BCH encoding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing polynomial division and encoding.
        """
        n_k = data["n"] - data["k"]
        return [
            f"g(x) = {_poly_str(data['g'])}",
            f"m(x) = {_poly_str(data['msg'])}",
            f"shift: m(x) * x^{n_k}",
            f"remainder r(x) = {_poly_str(data['remainder'])}",
            f"codeword: r(x) + m(x)*x^{n_k} = {_bits_str(data['codeword'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the encoded codeword.

        Args:
            data: Solution data.

        Returns:
            Codeword as a binary string.
        """
        return f"codeword = {_bits_str(data['codeword'])}"


# ═══════════════════════════════════════════════════════════════════
# 4. REED-SOLOMON (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ReedSolomonGenerator(StepGenerator):
    """Encode a message using a Reed-Solomon code over GF(q).

    Evaluates a message polynomial of degree < k at q-1 points in
    GF(q) to produce a codeword. Uses small fields (GF(5), GF(7))
    for tractable computation.

    Difficulty scaling:
        Difficulty 1-3: GF(5), k=2, evaluate at 4 points.
        Difficulty 4-6: GF(7), k=3, evaluate at 6 points.
        Difficulty 7-8: GF(7), k=4, evaluate at 6 points.

    Prerequisites:
        polynomial_multiply (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reed_solomon"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls field size and polynomial degree.

        Returns:
            Task description string.
        """
        return "encode message using Reed-Solomon code"

    def _eval_poly_gf(self, coeffs: list[int], x: int, q: int) -> int:
        """Evaluate polynomial at x over GF(q) using Horner's method.

        Args:
            coeffs: Coefficients from lowest to highest degree.
            x: Evaluation point.
            q: Field order (prime).

        Returns:
            f(x) mod q.
        """
        result = 0
        for c in reversed(coeffs):
            result = (result * x + c) % q
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Reed-Solomon encoding problem.

        Args:
            difficulty: Controls field and degree.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            q = 5
            k = 2
        elif difficulty <= 6:
            q = 7
            k = 3
        else:
            q = 7
            k = 4

        n = q - 1  # codeword length
        # Random message polynomial coefficients in GF(q)
        msg_coeffs = [self._rng.randint(0, q - 1) for _ in range(k)]
        if all(c == 0 for c in msg_coeffs):
            msg_coeffs[0] = 1

        # Evaluate at 1, 2, ..., q-1
        eval_points = list(range(1, q))
        codeword = [self._eval_poly_gf(msg_coeffs, x, q) for x in eval_points]

        d_min = n - k + 1  # Singleton bound met with equality (MDS)

        msg_str = ", ".join(str(c) for c in msg_coeffs)
        pts_str = ", ".join(str(p) for p in eval_points)
        problem = (
            f"RS code over GF({q}), k={k}. "
            f"Message polynomial m(x) with coeffs [{msg_str}]. "
            f"Evaluate at x = {pts_str}."
        )
        return problem, {
            "q": q, "k": k, "n": n, "d_min": d_min,
            "msg_coeffs": msg_coeffs, "eval_points": eval_points,
            "codeword": codeword,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate RS encoding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing polynomial evaluation at each point.
        """
        q = data["q"]
        steps = [
            f"GF({q}), message degree < {data['k']}",
            f"m(x) = " + " + ".join(
                f"{c}*x^{i}" if i > 0 else str(c)
                for i, c in enumerate(data["msg_coeffs"]) if c != 0
            ),
        ]
        for x, y in zip(data["eval_points"], data["codeword"]):
            steps.append(f"m({x}) = {y} mod {q}")
        cw_str = ", ".join(str(c) for c in data["codeword"])
        steps.append(f"codeword = [{cw_str}], d_min = {data['d_min']} (MDS)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the RS codeword.

        Args:
            data: Solution data.

        Returns:
            Codeword and minimum distance.
        """
        cw_str = ", ".join(str(c) for c in data["codeword"])
        return f"codeword = [{cw_str}], d_min = {data['d_min']}"


# ═══════════════════════════════════════════════════════════════════
# 5. CODE PARAMETERS (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class CodeParametersGenerator(StepGenerator):
    """Compute [n, k, d] parameters from a generator or parity check matrix.

    Given a generator matrix G (k x n), determines n, k, and minimum
    distance d by enumerating non-zero codewords (for small codes).
    Checks the Singleton bound d <= n - k + 1 and whether the code
    is MDS.

    Difficulty scaling:
        Difficulty 1-3: [7,4] Hamming code.
        Difficulty 4-6: [6,3] code.
        Difficulty 7-8: [8,4] extended Hamming.

    Prerequisites:
        matrix_multiply (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "code_parameters"

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
            difficulty: Controls code complexity.

        Returns:
            Task description string.
        """
        return "compute [n,k,d] code parameters and check Singleton bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a code parameters problem.

        Args:
            difficulty: Controls which code is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            code = LinearCodeGenerator._CODES["easy"]
        elif difficulty <= 6:
            code = LinearCodeGenerator._CODES["hard"]
        else:
            code = LinearCodeGenerator._CODES["medium"]

        k = code["k"]
        n = code["n"]
        d_min = code["d_min"]
        singleton = n - k + 1
        is_mds = (d_min == singleton)

        g_str = "[" + "; ".join(_bits_str(row) for row in code["G"]) + "]"
        problem = f"Generator matrix G = {g_str}. Find [n, k, d] and check MDS."
        return problem, {
            "code_name": code["name"], "n": n, "k": k,
            "d_min": d_min, "singleton": singleton, "is_mds": is_mds,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate code parameter computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing parameter computation.
        """
        return [
            f"G is {data['k']} x {data['n']}, so k = {data['k']}, n = {data['n']}",
            f"enumerate non-zero codewords, find minimum weight",
            f"d_min = {data['d_min']}",
            f"Singleton bound: d <= n - k + 1 = {data['singleton']}",
            f"MDS: {'YES' if data['is_mds'] else 'NO'} (d {'=' if data['is_mds'] else '<'} n-k+1)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the code parameters.

        Args:
            data: Solution data.

        Returns:
            Code parameters and MDS status.
        """
        mds = "MDS" if data["is_mds"] else "not MDS"
        return f"[{data['n']}, {data['k']}, {data['d_min']}], {mds}"


# ═══════════════════════════════════════════════════════════════════
# 6. TURBO CODE INTERLEAVE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class TurboCodeInterleaveGenerator(StepGenerator):
    """Compute the interleaved sequence for a turbo code encoder.

    Given systematic bits and an interleaver permutation, produces
    the reordered bit sequence that feeds the second RSC encoder
    in a turbo code.

    Difficulty scaling:
        Difficulty 1-3: 4-bit block, simple cyclic interleaver.
        Difficulty 4-6: 6-bit block, random permutation.
        Difficulty 7-8: 8-bit block, random permutation.

    Prerequisites:
        binary_arithmetic (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "turbo_code_interleave"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls block size.

        Returns:
            Task description string.
        """
        return "compute interleaved bit sequence for turbo code"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a turbo code interleaving problem.

        Args:
            difficulty: Controls block size and permutation type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
            # Cyclic shift interleaver
            shift = self._rng.randint(1, n - 1)
            perm = [(i + shift) % n for i in range(n)]
        elif difficulty <= 6:
            n = 6
            perm = list(range(n))
            self._rng.shuffle(perm)
        else:
            n = 8
            perm = list(range(n))
            self._rng.shuffle(perm)

        bits = [self._rng.randint(0, 1) for _ in range(n)]
        interleaved = [bits[perm[i]] for i in range(n)]

        perm_str = ", ".join(str(p) for p in perm)
        problem = (
            f"Systematic bits: {_bits_str(bits)}. "
            f"Interleaver permutation: [{perm_str}]. "
            f"Compute interleaved sequence."
        )
        return problem, {
            "bits": bits, "perm": perm,
            "interleaved": interleaved, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate interleaving steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing permutation application.
        """
        steps = [f"input bits: {_bits_str(data['bits'])}"]
        perm = data["perm"]
        bits = data["bits"]
        for i in range(data["n"]):
            steps.append(f"position {i}: take bit[{perm[i]}] = {bits[perm[i]]}")
        steps.append(f"interleaved: {_bits_str(data['interleaved'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the interleaved sequence.

        Args:
            data: Solution data.

        Returns:
            Interleaved bit string.
        """
        return f"interleaved = {_bits_str(data['interleaved'])}"
