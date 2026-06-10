"""Cryptanalysis generators -- frequency analysis, known plaintext, MITM, birthday attack.

4 generators across tiers 4-6 covering classical cipher breaking
via frequency analysis, known-plaintext attacks on substitution
ciphers, meet-in-the-middle complexity reduction, and birthday
paradox collision probability.
"""
import math
import string

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Frequency Analysis
# ---------------------------------------------------------------------------

@register
class FrequencyAnalysisGenerator(StepGenerator):
    """Deduce a Caesar cipher shift from letter frequency analysis.

    Generates a ciphertext by Caesar-shifting a short plaintext,
    counts letter frequencies, identifies the most common ciphertext
    letter, assumes it maps to 'e', and deduces the shift.

    Difficulty scaling:
        Difficulty 1-3: plaintext 8-15 chars, shift 1-5.
        Difficulty 4-6: plaintext 15-25 chars, shift 1-15.
        Difficulty 7-8: plaintext 25-40 chars, shift 1-25.

    Prerequisites:
        division.
    """

    _WORDS = [
        "the", "be", "to", "of", "and", "in", "that", "have",
        "it", "for", "not", "on", "with", "he", "as", "you",
        "do", "at", "this", "but", "his", "by", "from", "they",
        "we", "say", "her", "she", "an", "my", "one", "all",
        "or", "up", "so", "if", "me", "no", "go", "see",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "frequency_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "deduce Caesar shift from letter frequencies"

    def _caesar_encrypt(self, text: str, shift: int) -> str:
        """Encrypt text with Caesar cipher.

        Args:
            text: Lowercase plaintext.
            shift: Shift amount (0-25).

        Returns:
            Ciphertext in lowercase.
        """
        result = []
        for ch in text:
            if ch in string.ascii_lowercase:
                result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(ch)
        return "".join(result)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a frequency analysis problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            target_len = self._rng.randint(8, 15)
            shift = self._rng.randint(1, 5)
        elif difficulty <= 6:
            target_len = self._rng.randint(15, 25)
            shift = self._rng.randint(1, 15)
        else:
            target_len = self._rng.randint(25, 40)
            shift = self._rng.randint(1, 25)

        words = []
        length = 0
        while length < target_len:
            w = self._rng.choice(self._WORDS)
            words.append(w)
            length += len(w)
        plaintext = "".join(words)[:target_len]
        ciphertext = self._caesar_encrypt(plaintext, shift)

        freq: dict[str, int] = {}
        for ch in ciphertext:
            if ch in string.ascii_lowercase:
                freq[ch] = freq.get(ch, 0) + 1
        total_letters = sum(freq.values())
        freq_pct = {ch: round(count / total_letters, 4)
                    for ch, count in freq.items()}

        most_common = max(freq, key=lambda c: freq[c])
        deduced_shift = (ord(most_common) - ord('e')) % 26

        top3 = sorted(freq.items(), key=lambda x: -x[1])[:3]
        top3_str = ", ".join(f"'{ch}':{cnt}" for ch, cnt in top3)

        problem = f"Frequency: ciphertext='{ciphertext}'"
        return problem, {
            "plaintext": plaintext, "ciphertext": ciphertext,
            "shift": shift, "freq": freq, "total_letters": total_letters,
            "freq_pct": freq_pct, "most_common": most_common,
            "deduced_shift": deduced_shift, "top3_str": top3_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for frequency analysis.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing frequency count and shift deduction.
        """
        return [
            f"count letters: {data['total_letters']} total",
            f"top frequencies: {data['top3_str']}",
            f"most common = '{data['most_common']}', "
            f"freq = {data['freq_pct'].get(data['most_common'], 0)}",
            f"assume '{data['most_common']}' -> 'e': "
            f"shift = ord('{data['most_common']}')-ord('e') = "
            f"{data['deduced_shift']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the deduced shift.

        Args:
            data: Solution data dict.

        Returns:
            Shift as a string.
        """
        correct = "correct" if data["deduced_shift"] == data["shift"] else "approximate"
        return f"shift = {data['deduced_shift']} ({correct})"


# ---------------------------------------------------------------------------
# 2. Known Plaintext Attack
# ---------------------------------------------------------------------------

@register
class KnownPlaintextGenerator(StepGenerator):
    """Deduce a substitution cipher key from a known plaintext-ciphertext pair.

    Given a plaintext and its ciphertext under a simple substitution
    cipher, extracts the partial key mapping from the known pair and
    applies it to decrypt additional ciphertext.

    Difficulty scaling:
        Difficulty 1-3: 4-6 char known pair, 3-5 char target.
        Difficulty 4-6: 6-10 char known pair, 5-8 char target.
        Difficulty 7-8: 10-15 char known pair, 8-12 char target.

    Prerequisites:
        caesar.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "known_plaintext"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["caesar"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "deduce substitution key from known plaintext"

    def _generate_key(self) -> dict[str, str]:
        """Generate a random substitution cipher key.

        Returns:
            Dict mapping each lowercase letter to its substitute.
        """
        alphabet = list(string.ascii_lowercase)
        shuffled = list(alphabet)
        self._rng.shuffle(shuffled)
        return dict(zip(alphabet, shuffled))

    def _encrypt(self, text: str, key: dict[str, str]) -> str:
        """Encrypt text using a substitution cipher key.

        Args:
            text: Lowercase plaintext.
            key: Substitution mapping.

        Returns:
            Ciphertext.
        """
        return "".join(key.get(ch, ch) for ch in text)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a known-plaintext attack problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            known_len = self._rng.randint(4, 6)
            target_len = self._rng.randint(3, 5)
        elif difficulty <= 6:
            known_len = self._rng.randint(6, 10)
            target_len = self._rng.randint(5, 8)
        else:
            known_len = self._rng.randint(10, 15)
            target_len = self._rng.randint(8, 12)

        key = self._generate_key()
        inv_key = {v: k for k, v in key.items()}

        known_plain = "".join(
            self._rng.choice(string.ascii_lowercase)
            for _ in range(known_len)
        )
        known_cipher = self._encrypt(known_plain, key)

        partial_key: dict[str, str] = {}
        for p, c in zip(known_plain, known_cipher):
            partial_key[c] = p

        target_chars = list(partial_key.values())
        if len(target_chars) < target_len:
            target_chars += self._rng.choices(
                list(partial_key.values()),
                k=target_len - len(target_chars),
            )
        self._rng.shuffle(target_chars)
        target_plain = "".join(target_chars[:target_len])
        target_cipher = self._encrypt(target_plain, key)

        decrypted = ""
        for ch in target_cipher:
            decrypted += partial_key.get(ch, "?")

        n_decoded = sum(1 for ch in decrypted if ch != "?")

        problem = (
            f"Known-plaintext: known='{known_plain}' -> '{known_cipher}', "
            f"decrypt '{target_cipher}'"
        )
        return problem, {
            "known_plain": known_plain, "known_cipher": known_cipher,
            "partial_key": partial_key, "n_mappings": len(partial_key),
            "target_cipher": target_cipher, "target_plain": target_plain,
            "decrypted": decrypted, "n_decoded": n_decoded,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for known-plaintext attack.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing key extraction and decryption.
        """
        mapping_str = ", ".join(
            f"'{c}'->'{p}'" for c, p in sorted(data["partial_key"].items())
        )
        steps = [
            f"extract {data['n_mappings']} mappings from known pair",
            f"key: {mapping_str}",
            f"apply to '{data['target_cipher']}'",
            f"decrypted: '{data['decrypted']}'",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decrypted text.

        Args:
            data: Solution data dict.

        Returns:
            Decrypted string.
        """
        return f"decrypted = '{data['decrypted']}'"


# ---------------------------------------------------------------------------
# 3. Meet-in-the-Middle Attack
# ---------------------------------------------------------------------------

@register
class MeetInTheMiddleGenerator(StepGenerator):
    """Demonstrate meet-in-the-middle attack on double encryption.

    Given E_k2(E_k1(P)) = C with small key space, compute forward
    encryptions E_k(P) for all k and backward decryptions D_k(C)
    for all k, then find the collision. Shows complexity reduction
    from 2^(2n) to 2^(n+1).

    Difficulty scaling:
        Difficulty 1-3: n=2 (4 keys).
        Difficulty 4-6: n=3 (8 keys).
        Difficulty 7-8: n=4 (16 keys).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "meet_in_middle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find keys using meet-in-the-middle attack"

    def _toy_encrypt(self, plaintext: int, key: int, modulus: int) -> int:
        """Apply a toy encryption: E_k(P) = (P + k) mod modulus.

        Args:
            plaintext: Input value.
            key: Key value.
            modulus: Modulus for the operation.

        Returns:
            Encrypted value.
        """
        return (plaintext + key) % modulus

    def _toy_decrypt(self, ciphertext: int, key: int, modulus: int) -> int:
        """Apply toy decryption: D_k(C) = (C - k) mod modulus.

        Args:
            ciphertext: Encrypted value.
            key: Key value.
            modulus: Modulus for the operation.

        Returns:
            Decrypted value.
        """
        return (ciphertext - key) % modulus

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a meet-in-the-middle problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = 3
        else:
            n = 4

        key_space = 2 ** n
        modulus = key_space * 4

        plaintext = self._rng.randint(0, modulus - 1)
        k1 = self._rng.randint(0, key_space - 1)
        k2 = self._rng.randint(0, key_space - 1)

        intermediate = self._toy_encrypt(plaintext, k1, modulus)
        ciphertext = self._toy_encrypt(intermediate, k2, modulus)

        forward = {}
        for k in range(key_space):
            forward[k] = self._toy_encrypt(plaintext, k, modulus)

        backward = {}
        for k in range(key_space):
            backward[k] = self._toy_decrypt(ciphertext, k, modulus)

        collisions = []
        for kf, val_f in forward.items():
            for kb, val_b in backward.items():
                if val_f == val_b:
                    collisions.append((kf, kb))

        brute_force = key_space ** 2
        mitm_ops = 2 * key_space

        problem = (
            f"MITM: E_k(P)=(P+k) mod {modulus}, "
            f"P={plaintext}, C={ciphertext}, key space=0..{key_space - 1}"
        )
        return problem, {
            "n": n, "key_space": key_space, "modulus": modulus,
            "plaintext": plaintext, "ciphertext": ciphertext,
            "k1": k1, "k2": k2, "intermediate": intermediate,
            "forward": forward, "backward": backward,
            "collisions": collisions,
            "brute_force": brute_force, "mitm_ops": mitm_ops,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for MITM.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing forward/backward tables and collision.
        """
        fwd_entries = ", ".join(
            f"E_{k}(P)={v}" for k, v in sorted(data["forward"].items())
        )
        bwd_entries = ", ".join(
            f"D_{k}(C)={v}" for k, v in sorted(data["backward"].items())
        )
        coll_str = ", ".join(
            f"(k1={kf},k2={kb})" for kf, kb in data["collisions"]
        )
        return [
            f"forward: {fwd_entries}",
            f"backward: {bwd_entries}",
            f"collisions: {coll_str}",
            f"brute force: {data['brute_force']} ops, "
            f"MITM: {data['mitm_ops']} ops",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the discovered keys and complexity.

        Args:
            data: Solution data dict.

        Returns:
            Keys and complexity as a string.
        """
        return (
            f"k1={data['k1']}, k2={data['k2']}, "
            f"reduction: 2^{2*data['n']} -> 2^{data['n']+1}"
        )


# ---------------------------------------------------------------------------
# 4. Birthday Attack
# ---------------------------------------------------------------------------

@register
class BirthdayAttackGenerator(StepGenerator):
    """Compute birthday attack collision probability and threshold.

    Given a hash function with N possible outputs, computes the
    probability of a collision after q queries using
    P ~ 1 - e^(-q^2 / (2*N)), and the number of queries needed
    for P = 0.5: q ~ sqrt(2 * N * ln(2)).

    Difficulty scaling:
        Difficulty 1-3: N in [100, 1000].
        Difficulty 4-6: N in [1000, 100000].
        Difficulty 7-8: N as powers of 2 (2^8 to 2^20).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "birthday_attack"

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
        return "compute birthday attack collision probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a birthday attack problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(100, 1000)
            q = self._rng.randint(5, min(50, int(math.sqrt(2 * n))))
        elif difficulty <= 6:
            n = self._rng.randint(1000, 100000)
            q = self._rng.randint(10, min(500, int(math.sqrt(2 * n))))
        else:
            bits = self._rng.randint(8, 20)
            n = 2 ** bits
            q = self._rng.randint(10, min(1000, int(math.sqrt(2 * n))))

        exponent = round(-q * q / (2 * n), 4)
        exp_val = round(math.exp(exponent), 4)
        prob = round(1 - exp_val, 4)

        ln2 = round(math.log(2), 4)
        q_half = round(math.sqrt(2 * n * ln2), 4)

        problem = f"Birthday: N={n} outputs, q={q} queries"
        return problem, {
            "n": n, "q": q, "exponent": exponent,
            "exp_val": exp_val, "prob": prob,
            "ln2": ln2, "q_half": q_half,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for birthday attack.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing probability computation and threshold.
        """
        return [
            f"-q^2/(2N) = -{data['q']}^2/(2*{data['n']}) = {data['exponent']}",
            f"e^({data['exponent']}) = {data['exp_val']}",
            f"P(collision) = 1 - {data['exp_val']} = {data['prob']}",
            f"for P=0.5: q = sqrt(2*{data['n']}*ln(2)) = "
            f"sqrt(2*{data['n']}*{data['ln2']}) = {data['q_half']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return collision probability and 50% threshold.

        Args:
            data: Solution data dict.

        Returns:
            Probability and threshold as a string.
        """
        return f"P = {data['prob']}, q_50% = {data['q_half']}"
