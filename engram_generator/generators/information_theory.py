"""Information theory task generators.

6 generators across tiers 5-6 covering channel capacity, Huffman coding,
Hamming encoding/decoding, source coding, and error rate computation.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _binary_entropy(p: float) -> float:
    """Compute the binary entropy function H(p).

    Args:
        p: Probability in (0, 1).

    Returns:
        H(p) = -p*log2(p) - (1-p)*log2(1-p), or 0.0 at the boundaries.
    """
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def _build_huffman_tree(symbols: list[str],
                        frequencies: list[float]) -> dict[str, str]:
    """Build a Huffman tree and return codeword assignments.

    Uses a greedy min-frequency merge. Ties are broken by symbol name
    to ensure deterministic output.

    Args:
        symbols: List of symbol names.
        frequencies: Corresponding frequencies (need not sum to 1).

    Returns:
        Dict mapping each symbol to its binary codeword string.
    """
    # Each node: (frequency, tie_breaker, symbol_or_none, left, right)
    nodes: list[list] = []
    for i, (sym, freq) in enumerate(zip(symbols, frequencies)):
        nodes.append([freq, i, sym, None, None])

    counter = len(nodes)
    while len(nodes) > 1:
        nodes.sort(key=lambda n: (n[0], n[1]))
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = [left[0] + right[0], counter, None, left, right]
        counter += 1
        nodes.append(merged)

    codes: dict[str, str] = {}
    _assign_codes(nodes[0], "", codes)
    return codes


def _assign_codes(node: list, prefix: str, codes: dict[str, str]) -> None:
    """Recursively assign binary codes from a Huffman tree node.

    Args:
        node: Tree node as [freq, tie, symbol, left, right].
        prefix: Current binary prefix.
        codes: Dict to populate with symbol -> codeword mappings.
    """
    if node[2] is not None:
        codes[node[2]] = prefix if prefix else "0"
        return
    if node[3] is not None:
        _assign_codes(node[3], prefix + "0", codes)
    if node[4] is not None:
        _assign_codes(node[4], prefix + "1", codes)


# ---------------------------------------------------------------------------
# Hamming(7,4) matrices
# ---------------------------------------------------------------------------

# Generator matrix rows (4 data bits -> 7 code bits)
_HAMMING_G = [
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
]

# Parity check matrix (3x7)
_HAMMING_H = [
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
]


# ---------------------------------------------------------------------------
# 1. Channel Capacity (BSC)
# ---------------------------------------------------------------------------

@register
class ChannelCapacityGenerator(StepGenerator):
    """Compute the capacity of a binary symmetric channel.

    Given crossover probability p, compute C = 1 - H(p) where
    H(p) = -p*log2(p) - (1-p)*log2(1-p) is the binary entropy.

    Difficulty scaling:
        Difficulty 1-3: p is a simple fraction (0.1, 0.2, ..., 0.4).
        Difficulty 4-6: p drawn from wider range with 2 decimal places.
        Difficulty 7-8: p drawn from fine-grained range with 3 decimal places.

    Prerequisites:
        mutual_information.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "channel_capacity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mutual_information"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute capacity of a binary symmetric channel"

    def _pick_probability(self, difficulty: int) -> float:
        """Choose a crossover probability appropriate for the difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Crossover probability p in (0, 0.5).
        """
        if difficulty <= 3:
            return self._rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
        if difficulty <= 6:
            return round(self._rng.uniform(0.01, 0.49), 2)
        return round(self._rng.uniform(0.001, 0.499), 3)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BSC channel capacity problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p = self._pick_probability(difficulty)
        h_p = round(_binary_entropy(p), 4)
        capacity = round(1.0 - _binary_entropy(p), 4)
        return (
            f"BSC with crossover probability p = {p}. "
            f"Compute C = 1 - H(p).",
            {"p": p, "h_p": h_p, "capacity": capacity},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for BSC capacity.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing H(p) and C computation.
        """
        p = data["p"]
        q = round(1.0 - p, 4)
        return [
            f"H(p) = -{p}*log2({p}) - {q}*log2({q})",
            f"H({p}) = {data['h_p']}",
            f"C = 1 - H({p}) = 1 - {data['h_p']} = {data['capacity']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the channel capacity.

        Args:
            data: Solution data dict.

        Returns:
            Capacity value as a string.
        """
        return f"C = {data['capacity']}"


# ---------------------------------------------------------------------------
# 2. Huffman Coding
# ---------------------------------------------------------------------------

@register
class HuffmanCodingGenerator(StepGenerator):
    """Build a Huffman code from symbol frequencies.

    Given 3-6 symbols with frequency counts, construct the Huffman tree,
    assign codewords, and compute the average code length.

    Difficulty scaling:
        Difficulty 1-3: 3 symbols, small frequencies.
        Difficulty 4-6: 4-5 symbols, moderate frequencies.
        Difficulty 7-8: 5-6 symbols, larger frequencies.

    Prerequisites:
        info_entropy.
    """

    _PARAMS = {
        1: {"n_lo": 3, "n_hi": 3, "freq_lo": 1, "freq_hi": 10},
        2: {"n_lo": 3, "n_hi": 3, "freq_lo": 1, "freq_hi": 15},
        3: {"n_lo": 3, "n_hi": 3, "freq_lo": 1, "freq_hi": 20},
        4: {"n_lo": 4, "n_hi": 4, "freq_lo": 1, "freq_hi": 30},
        5: {"n_lo": 4, "n_hi": 5, "freq_lo": 1, "freq_hi": 40},
        6: {"n_lo": 4, "n_hi": 5, "freq_lo": 1, "freq_hi": 50},
        7: {"n_lo": 5, "n_hi": 6, "freq_lo": 1, "freq_hi": 60},
        8: {"n_lo": 5, "n_hi": 6, "freq_lo": 1, "freq_hi": 80},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "huffman_coding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "build Huffman code and compute average code length"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Huffman coding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        n_symbols = self._rng.randint(params["n_lo"], params["n_hi"])
        symbols = [chr(ord("A") + i) for i in range(n_symbols)]
        freqs = [
            self._rng.randint(params["freq_lo"], params["freq_hi"])
            for _ in range(n_symbols)
        ]

        total = sum(freqs)
        probs = [f / total for f in freqs]
        codes = _build_huffman_tree(symbols, freqs)
        avg_len = round(
            sum(probs[i] * len(codes[s]) for i, s in enumerate(symbols)),
            4,
        )

        freq_str = ", ".join(f"{s}:{f}" for s, f in zip(symbols, freqs))
        return (
            f"Huffman code for symbols with frequencies {{{freq_str}}}.",
            {
                "symbols": symbols,
                "freqs": freqs,
                "total": total,
                "probs": probs,
                "codes": codes,
                "avg_len": avg_len,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Huffman coding.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing probabilities, codewords, and average length.
        """
        steps: list[str] = []
        prob_parts = ", ".join(
            f"P({s})={round(p, 4)}"
            for s, p in zip(data["symbols"], data["probs"])
        )
        steps.append(f"probabilities: {prob_parts}")

        code_parts = ", ".join(
            f"{s}->{data['codes'][s]}"
            for s in data["symbols"]
        )
        steps.append(f"codewords: {code_parts}")

        len_terms = " + ".join(
            f"{round(p, 4)}*{len(data['codes'][s])}"
            for s, p in zip(data["symbols"], data["probs"])
        )
        steps.append(f"L = {len_terms} = {data['avg_len']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the codewords and average code length.

        Args:
            data: Solution data dict.

        Returns:
            Codewords and average length as a string.
        """
        code_str = ", ".join(
            f"{s}:{data['codes'][s]}" for s in data["symbols"]
        )
        return f"codes={{{code_str}}}, avg_len={data['avg_len']}"


# ---------------------------------------------------------------------------
# 3. Hamming(7,4) Encode
# ---------------------------------------------------------------------------

@register
class HammingEncodeGenerator(StepGenerator):
    """Encode a 4-bit data word into a Hamming(7,4) codeword.

    Multiply the 4-bit data vector by the generator matrix G
    (mod 2) to produce the 7-bit encoded codeword. Shows parity
    bit computation for each of the three parity positions.

    Difficulty scaling:
        Difficulty 1-3: data words with at most two 1-bits.
        Difficulty 4-6: data words with two or three 1-bits.
        Difficulty 7-8: any 4-bit data word.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hamming_encode"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encode 4-bit data word using Hamming(7,4)"

    def _pick_data_word(self, difficulty: int) -> list[int]:
        """Choose a 4-bit data word scaled to difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            List of 4 bits (0 or 1).
        """
        if difficulty <= 3:
            max_ones = 2
        elif difficulty <= 6:
            max_ones = 3
        else:
            max_ones = 4

        word = [0, 0, 0, 0]
        n_ones = self._rng.randint(1, max_ones)
        positions = self._rng.sample(range(4), n_ones)
        for pos in positions:
            word[pos] = 1
        return word

    def _encode(self, data_word: list[int]) -> list[int]:
        """Encode a 4-bit word using the Hamming(7,4) generator matrix.

        Args:
            data_word: List of 4 data bits.

        Returns:
            List of 7 code bits.
        """
        codeword = [0] * 7
        for j in range(7):
            val = 0
            for i in range(4):
                val ^= data_word[i] * _HAMMING_G[i][j]
            codeword[j] = val
        return codeword

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hamming(7,4) encoding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        data_word = self._pick_data_word(difficulty)
        codeword = self._encode(data_word)

        # Compute parity bits explicitly (positions 4, 5, 6 in 0-indexed)
        p1 = (data_word[0] ^ data_word[1] ^ data_word[3]) % 2
        p2 = (data_word[0] ^ data_word[2] ^ data_word[3]) % 2
        p3 = (data_word[1] ^ data_word[2] ^ data_word[3]) % 2

        dw_str = "".join(str(b) for b in data_word)
        return (
            f"Hamming(7,4) encode: data = {dw_str}",
            {
                "data_word": data_word,
                "codeword": codeword,
                "p1": p1,
                "p2": p2,
                "p3": p3,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Hamming encoding.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing parity bit computation and final codeword.
        """
        d = data["data_word"]
        return [
            f"data bits: d1={d[0]}, d2={d[1]}, d3={d[2]}, d4={d[3]}",
            f"p1 = d1 XOR d2 XOR d4 = {d[0]}^{d[1]}^{d[3]} = {data['p1']}",
            f"p2 = d1 XOR d3 XOR d4 = {d[0]}^{d[2]}^{d[3]} = {data['p2']}",
            f"p3 = d2 XOR d3 XOR d4 = {d[1]}^{d[2]}^{d[3]} = {data['p3']}",
            f"codeword = {''.join(str(b) for b in data['codeword'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the encoded codeword.

        Args:
            data: Solution data dict.

        Returns:
            7-bit codeword as a string.
        """
        return "".join(str(b) for b in data["codeword"])


# ---------------------------------------------------------------------------
# 4. Hamming(7,4) Decode
# ---------------------------------------------------------------------------

@register
class HammingDecodeGenerator(StepGenerator):
    """Decode a 7-bit Hamming(7,4) codeword with possible single error.

    Compute the syndrome by multiplying the received word by the parity
    check matrix H^T. If the syndrome is non-zero, identify the error
    position and flip the bit to correct it.

    Difficulty scaling:
        Difficulty 1-3: no error introduced.
        Difficulty 4-6: single error at a random position.
        Difficulty 7-8: single error, data words with more 1-bits.

    Prerequisites:
        hamming_encode.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hamming_decode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hamming_encode"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "decode Hamming(7,4) codeword and correct single-bit error"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hamming(7,4) decoding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        # Generate a valid codeword first
        max_ones = 4 if difficulty >= 7 else (3 if difficulty >= 4 else 2)
        data_word = [0, 0, 0, 0]
        n_ones = self._rng.randint(1, max_ones)
        for pos in self._rng.sample(range(4), n_ones):
            data_word[pos] = 1

        codeword = [0] * 7
        for j in range(7):
            val = 0
            for i in range(4):
                val ^= data_word[i] * _HAMMING_G[i][j]
            codeword[j] = val

        # Introduce error for higher difficulties
        error_pos = -1
        received = list(codeword)
        if difficulty >= 4:
            error_pos = self._rng.randint(0, 6)
            received[error_pos] ^= 1

        # Compute syndrome
        syndrome = [0, 0, 0]
        for i in range(3):
            val = 0
            for j in range(7):
                val ^= _HAMMING_H[i][j] * received[j]
            syndrome[i] = val

        syndrome_val = syndrome[0] * 4 + syndrome[1] * 2 + syndrome[2]

        # Map syndrome to error position (1-indexed column of H)
        corrected_pos = -1
        corrected = list(received)
        if syndrome_val != 0:
            # Find which column of H matches the syndrome
            for col in range(7):
                h_col = [_HAMMING_H[row][col] for row in range(3)]
                if h_col == syndrome:
                    corrected_pos = col
                    corrected[col] ^= 1
                    break

        # Extract data bits from corrected codeword
        decoded_data = corrected[:4]

        recv_str = "".join(str(b) for b in received)
        return (
            f"Hamming(7,4) decode: received = {recv_str}",
            {
                "received": received,
                "codeword": codeword,
                "data_word": data_word,
                "error_pos": error_pos,
                "syndrome": syndrome,
                "syndrome_val": syndrome_val,
                "corrected_pos": corrected_pos,
                "corrected": corrected,
                "decoded_data": decoded_data,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Hamming decoding.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing syndrome computation, error location, correction.
        """
        s = data["syndrome"]
        steps = [
            f"syndrome = ({s[0]}, {s[1]}, {s[2]}) = {data['syndrome_val']}",
        ]
        if data["syndrome_val"] == 0:
            steps.append("syndrome = 0, no error detected")
        else:
            steps.append(
                f"error at position {data['corrected_pos']} (0-indexed)"
            )
            steps.append(
                f"flip bit {data['corrected_pos']}: "
                f"{''.join(str(b) for b in data['corrected'])}"
            )
        steps.append(
            f"decoded data = {''.join(str(b) for b in data['decoded_data'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the corrected codeword and decoded data.

        Args:
            data: Solution data dict.

        Returns:
            Decoded 4-bit data word as a string.
        """
        return "".join(str(b) for b in data["decoded_data"])


# ---------------------------------------------------------------------------
# 5. Source Coding (Expected Code Length + Kraft Inequality)
# ---------------------------------------------------------------------------

@register
class SourceCodingGenerator(StepGenerator):
    """Compute expected code length and verify Kraft inequality.

    Given symbol probabilities and assigned code lengths, compute
    L = sum(p_i * l_i) and check that sum(2^{-l_i}) <= 1.

    Difficulty scaling:
        Difficulty 1-3: 3 symbols, integer-friendly probabilities.
        Difficulty 4-6: 4 symbols, more varied probabilities.
        Difficulty 7-8: 5-6 symbols, fine-grained probabilities.

    Prerequisites:
        info_entropy.
    """

    _PARAMS = {
        1: {"n": 3, "max_len": 3},
        2: {"n": 3, "max_len": 3},
        3: {"n": 3, "max_len": 4},
        4: {"n": 4, "max_len": 4},
        5: {"n": 4, "max_len": 5},
        6: {"n": 4, "max_len": 5},
        7: {"n": 5, "max_len": 6},
        8: {"n": 6, "max_len": 6},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "source_coding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute expected code length and check Kraft inequality"

    def _generate_valid_code_lengths(self, n: int,
                                     max_len: int) -> list[int]:
        """Generate code lengths satisfying the Kraft inequality.

        Produces lengths sorted in non-decreasing order that satisfy
        sum(2^{-l_i}) <= 1.

        Args:
            n: Number of symbols.
            max_len: Maximum allowed code length.

        Returns:
            List of n code lengths.
        """
        for _ in range(100):
            lengths = sorted(
                self._rng.randint(1, max_len) for _ in range(n)
            )
            kraft = sum(2.0 ** (-l) for l in lengths)
            if kraft <= 1.0:
                return lengths
        # Fallback: use a simple valid assignment
        return [1] + [n] * (n - 1) if n > 1 else [1]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a source coding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        n = params["n"]
        max_len = params["max_len"]

        # Generate probabilities that sum to 1
        raw_weights = [self._rng.randint(1, 20) for _ in range(n)]
        total_weight = sum(raw_weights)
        probs = [round(w / total_weight, 4) for w in raw_weights]
        # Fix rounding to ensure sum = 1
        probs[-1] = round(1.0 - sum(probs[:-1]), 4)

        symbols = [chr(ord("A") + i) for i in range(n)]
        lengths = self._generate_valid_code_lengths(n, max_len)

        expected_len = round(sum(p * l for p, l in zip(probs, lengths)), 4)
        kraft_sum = round(sum(2.0 ** (-l) for l in lengths), 4)
        kraft_ok = kraft_sum <= 1.0

        sym_str = ", ".join(
            f"{s}: p={p}, l={l}"
            for s, p, l in zip(symbols, probs, lengths)
        )
        return (
            f"Source coding: {{{sym_str}}}. "
            f"Compute L and check Kraft inequality.",
            {
                "symbols": symbols,
                "probs": probs,
                "lengths": lengths,
                "expected_len": expected_len,
                "kraft_sum": kraft_sum,
                "kraft_ok": kraft_ok,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for source coding.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing L computation and Kraft check.
        """
        steps: list[str] = []
        l_terms = " + ".join(
            f"{p}*{l}"
            for p, l in zip(data["probs"], data["lengths"])
        )
        steps.append(f"L = {l_terms} = {data['expected_len']}")

        k_terms = " + ".join(
            f"2^(-{l})" for l in data["lengths"]
        )
        steps.append(f"Kraft: {k_terms} = {data['kraft_sum']}")
        steps.append(
            f"Kraft inequality satisfied: {data['kraft_ok']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the expected code length and Kraft result.

        Args:
            data: Solution data dict.

        Returns:
            Expected length and Kraft inequality status.
        """
        return (
            f"L = {data['expected_len']}, "
            f"Kraft = {data['kraft_sum']}, "
            f"valid = {data['kraft_ok']}"
        )


# ---------------------------------------------------------------------------
# 6. Error Rate (Channel Matrix)
# ---------------------------------------------------------------------------

@register
class ErrorRateGenerator(StepGenerator):
    """Compute probability of error for a discrete memoryless channel.

    Given input distribution P(X) and channel matrix P(Y|X), compute
    P(error) = sum_x P(x) * P(error|x) where
    P(error|x) = 1 - P(y=x|x) for a channel with matched outputs.

    Difficulty scaling:
        Difficulty 1-3: 2x2 channel matrix, simple probabilities.
        Difficulty 4-6: 3x3 channel matrix.
        Difficulty 7-8: 4x4 channel matrix.

    Prerequisites:
        basic_prob.
    """

    _SIZES = {
        1: 2, 2: 2, 3: 2,
        4: 3, 5: 3, 6: 3,
        7: 4, 8: 4,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "error_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute probability of error for a discrete channel"

    def _generate_channel_row(self, n: int) -> list[float]:
        """Generate a valid channel matrix row summing to 1.

        The diagonal entry is biased to be the largest so the channel
        is not purely noisy.

        Args:
            n: Number of output symbols.

        Returns:
            Row of conditional probabilities summing to 1.0.
        """
        raw = [self._rng.randint(1, 5) for _ in range(n)]
        # Bias diagonal to be dominant
        raw[0] = self._rng.randint(5, 15)
        total = sum(raw)
        row = [round(r / total, 4) for r in raw]
        # Fix rounding
        row[-1] = round(1.0 - sum(row[:-1]), 4)
        return row

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a channel error rate problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._SIZES.get(difficulty, 4)

        # Generate input distribution P(X)
        raw_px = [self._rng.randint(1, 10) for _ in range(n)]
        total_px = sum(raw_px)
        p_x = [round(r / total_px, 4) for r in raw_px]
        p_x[-1] = round(1.0 - sum(p_x[:-1]), 4)

        # Generate channel matrix P(Y|X), each row sums to 1
        # Row i represents P(Y|X=i), with diagonal biased higher
        channel: list[list[float]] = []
        for i in range(n):
            row = self._generate_channel_row(n)
            # Rotate so diagonal element is at position i
            rotated = row[-i:] + row[:-i] if i > 0 else row
            channel.append(rotated)

        # P(error|x_i) = 1 - P(Y=i|X=i) = 1 - channel[i][i]
        p_error_given_x = [round(1.0 - channel[i][i], 4) for i in range(n)]

        # P(error) = sum P(x_i) * P(error|x_i)
        p_error = round(
            sum(p_x[i] * p_error_given_x[i] for i in range(n)),
            4,
        )

        # Format channel matrix for problem statement
        rows_str = "; ".join(
            "[" + ", ".join(str(v) for v in row) + "]"
            for row in channel
        )
        px_str = ", ".join(f"P(x{i})={p_x[i]}" for i in range(n))
        return (
            f"Channel P(Y|X) = [{rows_str}], {px_str}. "
            f"Compute P(error).",
            {
                "n": n,
                "p_x": p_x,
                "channel": channel,
                "p_error_given_x": p_error_given_x,
                "p_error": p_error,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for error rate computation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing per-input error and total P(error).
        """
        steps: list[str] = []
        n = data["n"]
        for i in range(n):
            steps.append(
                f"P(error|x{i}) = 1 - {data['channel'][i][i]} "
                f"= {data['p_error_given_x'][i]}"
            )

        terms = " + ".join(
            f"{data['p_x'][i]}*{data['p_error_given_x'][i]}"
            for i in range(n)
        )
        steps.append(f"P(error) = {terms} = {data['p_error']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the probability of error.

        Args:
            data: Solution data dict.

        Returns:
            P(error) as a string.
        """
        return f"P(error) = {data['p_error']}"
