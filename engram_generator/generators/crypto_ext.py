"""Extended cryptography task generators.

8 generators across tiers 5-6 covering ElGamal encryption, DSA signing,
Shamir secret sharing, Pedersen commitment, Schnorr zero-knowledge proof,
Merkle tree, stream cipher (LFSR), and block cipher modes.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
]


def _is_prime(n: int) -> bool:
    """Check primality by trial division.

    Args:
        n: Integer to test.

    Returns:
        True if n is prime.
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular inverse of a mod m using extended GCD.

    Args:
        a: Value to invert.
        m: Modulus.

    Returns:
        a^{-1} mod m.

    Raises:
        ValueError: If inverse does not exist.
    """
    g, x, _ = _extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"No inverse: gcd({a},{m})={g}")
    return x % m


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple (gcd, x, y) such that a*x + b*y == gcd.
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def _find_generator(p: int) -> int:
    """Find a primitive root modulo prime p.

    Args:
        p: Prime number.

    Returns:
        A primitive root modulo p.
    """
    if p == 2:
        return 1
    phi = p - 1
    # Find prime factors of phi
    factors = set()
    n = phi
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)

    for g in range(2, p):
        is_gen = True
        for f in factors:
            if pow(g, phi // f, p) == 1:
                is_gen = False
                break
        if is_gen:
            return g
    return 2  # fallback


def _simple_hash(m: int, q: int) -> int:
    """Simple deterministic hash for small-number DSA simulation.

    Args:
        m: Message (integer).
        q: Modulus for hash output.

    Returns:
        Hash value in [1, q-1].
    """
    h = ((m * 31 + 17) % q)
    return max(1, h)


# ---------------------------------------------------------------------------
# 1. ElGamal Encryption (tier 6)
# ---------------------------------------------------------------------------

@register
class ElGamalEncryptGenerator(StepGenerator):
    """ElGamal public-key encryption and decryption.

    Choose random k, compute c1 = g^k mod p, c2 = m * h^k mod p.
    Decrypt: m = c2 * (c1^x)^{-1} mod p where h = g^x mod p.

    Difficulty scaling:
        Difficulty 1-3: p < 30, small exponents.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_pow.
    """

    _P_CAPS = {
        1: 30, 2: 30, 3: 30,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elgamal_encrypt"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encrypt and decrypt using ElGamal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ElGamal encryption problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._P_CAPS.get(difficulty, 100)
        primes = [p for p in _SMALL_PRIMES if 7 <= p < cap]
        p = self._rng.choice(primes)
        g = _find_generator(p)
        x = self._rng.randint(2, p - 2)  # private key
        h = pow(g, x, p)  # public key
        m = self._rng.randint(1, p - 1)  # message
        k = self._rng.randint(2, p - 2)  # random nonce

        c1 = pow(g, k, p)
        c2 = (m * pow(h, k, p)) % p

        # Decryption: s = c1^x mod p, m_dec = c2 * s^{-1} mod p
        s = pow(c1, x, p)
        s_inv = _mod_inverse(s, p)
        m_dec = (c2 * s_inv) % p

        return (
            f"ElGamal: p={p}, g={g}, h={h}, m={m}, k={k}",
            {"p": p, "g": g, "x": x, "h": h, "m": m, "k": k,
             "c1": c1, "c2": c2, "s": s, "s_inv": s_inv, "m_dec": m_dec},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for ElGamal.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing encryption and decryption.
        """
        return [
            f"c1 = {data['g']}^{{{data['k']}}} mod {data['p']} = {data['c1']}",
            f"c2 = {data['m']}*{data['h']}^{{{data['k']}}} mod {data['p']} = {data['c2']}",
            f"decrypt: s = {data['c1']}^{{{data['x']}}} mod {data['p']} = {data['s']}",
            f"m = {data['c2']}*{data['s']}^{{-1}} mod {data['p']} = {data['m_dec']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the ciphertext and recovered plaintext.

        Args:
            data: Solution data dict.

        Returns:
            Ciphertext pair and decrypted message.
        """
        return f"c=({data['c1']},{data['c2']}), m={data['m_dec']}"


# ---------------------------------------------------------------------------
# 2. DSA Sign (tier 6)
# ---------------------------------------------------------------------------

@register
class DSASignGenerator(StepGenerator):
    """Digital Signature Algorithm (DSA) signing and verification.

    Sign: choose k, r = (g^k mod p) mod q, s = k^{-1}*(H(m)+xr) mod q.
    Verify: w = s^{-1} mod q, u1 = H(m)*w mod q, u2 = r*w mod q.

    Difficulty scaling:
        Difficulty 1-3: p < 30, q < 15.
        Difficulty 4-6: p < 50, q < 25.
        Difficulty 7-8: p < 100, q < 50.

    Prerequisites:
        mod_inv.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dsa_sign"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "sign message using DSA and verify"

    def _find_dsa_params(self, cap: int) -> tuple[int, int, int]:
        """Find DSA parameters (p, q, g) where q divides p-1.

        Args:
            cap: Upper bound for p.

        Returns:
            Tuple (p, q, g).
        """
        for q in _SMALL_PRIMES:
            if q < 5 or q >= cap // 2:
                continue
            for multiplier in range(2, cap // q + 1):
                p = q * multiplier + 1
                if p < cap and _is_prime(p):
                    # Find g of order q mod p
                    for h in range(2, p):
                        g = pow(h, (p - 1) // q, p)
                        if g > 1:
                            return p, q, g
        # Fallback to small known params
        return 23, 11, pow(2, (23 - 1) // 11, 23)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DSA signing problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            cap = 30
        elif difficulty <= 6:
            cap = 50
        else:
            cap = 100

        p, q, g = self._find_dsa_params(cap)
        x = self._rng.randint(1, q - 1)  # private key
        y = pow(g, x, p)  # public key
        m = self._rng.randint(1, 100)  # message
        h_m = _simple_hash(m, q)

        # Sign: choose k coprime to q
        for k_try in range(2, q):
            if math.gcd(k_try, q) == 1:
                k = k_try
                break
        else:
            k = 2

        r = pow(g, k, p) % q
        if r == 0:
            r = 1
        k_inv = _mod_inverse(k, q)
        s = (k_inv * (h_m + x * r)) % q
        if s == 0:
            s = 1

        # Verify
        w = _mod_inverse(s, q)
        u1 = (h_m * w) % q
        u2 = (r * w) % q

        return (
            f"DSA: p={p}, q={q}, g={g}, x={x}, m={m}",
            {"p": p, "q": q, "g": g, "x": x, "y": y, "m": m,
             "h_m": h_m, "k": k, "r": r, "s": s,
             "w": w, "u1": u1, "u2": u2},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for DSA.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing signing and verification.
        """
        return [
            f"H(m) = {data['h_m']}",
            f"r = ({data['g']}^{{{data['k']}}} mod {data['p']}) mod {data['q']} = {data['r']}",
            f"s = {data['k']}^{{-1}}*({data['h_m']}+{data['x']}*{data['r']}) mod {data['q']} = {data['s']}",
            f"verify: w={data['w']}, u1={data['u1']}, u2={data['u2']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the DSA signature.

        Args:
            data: Solution data dict.

        Returns:
            Signature (r, s) as a string.
        """
        return f"sig=({data['r']},{data['s']})"


# ---------------------------------------------------------------------------
# 3. Shamir Secret Sharing (tier 5)
# ---------------------------------------------------------------------------

@register
class ShamirSecretShareGenerator(StepGenerator):
    """Split a secret using Shamir's (t,n) threshold scheme.

    Construct polynomial f(x) of degree t-1 with f(0) = secret.
    Compute n shares as f(1), f(2), ..., f(n). Reconstruct using
    Lagrange interpolation over t shares.

    Difficulty scaling:
        Difficulty 1-3: t=2, n=3, small prime.
        Difficulty 4-6: t=3, n=4-5.
        Difficulty 7-8: t=4, n=5-6.

    Prerequisites:
        modular.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "shamir_secret_share"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "split and reconstruct secret using Shamir sharing"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Shamir secret sharing problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            t, n = 2, 3
            p = self._rng.choice([17, 19, 23, 29, 31])
        elif difficulty <= 6:
            t = 3
            n = self._rng.randint(4, 5)
            p = self._rng.choice([31, 37, 41, 43, 47])
        else:
            t = 4
            n = self._rng.randint(5, 6)
            p = self._rng.choice([47, 53, 59, 61, 67])

        secret = self._rng.randint(1, p - 1)
        # Random coefficients for polynomial: a_0 = secret, a_1..a_{t-1} random
        coeffs = [secret] + [self._rng.randint(1, p - 1) for _ in range(t - 1)]

        # Compute shares
        shares = []
        for i in range(1, n + 1):
            val = 0
            for j, c in enumerate(coeffs):
                val = (val + c * pow(i, j, p)) % p
            shares.append((i, val))

        # Reconstruct from first t shares using Lagrange
        recon_shares = shares[:t]
        reconstructed = 0
        for i, (xi, yi) in enumerate(recon_shares):
            numerator = 1
            denominator = 1
            for j, (xj, _) in enumerate(recon_shares):
                if i != j:
                    numerator = (numerator * (0 - xj)) % p
                    denominator = (denominator * (xi - xj)) % p
            lagrange = (yi * numerator * _mod_inverse(denominator, p)) % p
            reconstructed = (reconstructed + lagrange) % p

        return (
            f"Shamir ({t},{n}): secret={secret}, p={p}",
            {"t": t, "n": n, "p": p, "secret": secret, "coeffs": coeffs,
             "shares": shares, "recon_shares": recon_shares,
             "reconstructed": reconstructed},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Shamir sharing.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing polynomial, shares, and reconstruction.
        """
        coeff_str = " + ".join(
            f"{c}*x^{i}" if i > 0 else str(c)
            for i, c in enumerate(data["coeffs"])
        )
        steps = [f"f(x) = {coeff_str} mod {data['p']}"]

        share_str = ", ".join(f"({x},{y})" for x, y in data["shares"])
        steps.append(f"shares: {share_str}")

        recon_str = ", ".join(f"({x},{y})" for x, y in data["recon_shares"])
        steps.append(f"reconstruct from {data['t']} shares: {recon_str}")
        steps.append(f"f(0) = {data['reconstructed']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the shares and reconstructed secret.

        Args:
            data: Solution data dict.

        Returns:
            Shares and secret as a string.
        """
        share_str = ", ".join(f"({x},{y})" for x, y in data["shares"])
        return f"shares=[{share_str}], secret={data['reconstructed']}"


# ---------------------------------------------------------------------------
# 4. Commitment Scheme (tier 5)
# ---------------------------------------------------------------------------

@register
class CommitmentSchemeGenerator(StepGenerator):
    """Pedersen commitment scheme: C = g^m * h^r mod p.

    Commit to message m with randomness r. Verify by checking
    C == g^m * h^r mod p given the opening (m, r).

    Difficulty scaling:
        Difficulty 1-3: p < 30, small values.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_pow.
    """

    _P_CAPS = {
        1: 30, 2: 30, 3: 30,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "commitment_scheme"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute and verify Pedersen commitment"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Pedersen commitment problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._P_CAPS.get(difficulty, 100)
        primes = [p for p in _SMALL_PRIMES if 7 <= p < cap]
        p = self._rng.choice(primes)
        g = _find_generator(p)
        # h must be another generator (g^a for unknown a)
        a = self._rng.randint(2, p - 2)
        h = pow(g, a, p)
        if h == g:
            h = pow(g, a + 1, p)

        m = self._rng.randint(1, p - 2)
        r = self._rng.randint(1, p - 2)

        g_m = pow(g, m, p)
        h_r = pow(h, r, p)
        commitment = (g_m * h_r) % p

        # Verify
        verify = (pow(g, m, p) * pow(h, r, p)) % p

        return (
            f"Pedersen: p={p}, g={g}, h={h}, m={m}, r={r}",
            {"p": p, "g": g, "h": h, "m": m, "r": r,
             "g_m": g_m, "h_r": h_r, "commitment": commitment,
             "verify": verify, "valid": commitment == verify},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Pedersen commitment.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing commitment computation and verification.
        """
        return [
            f"g^m = {data['g']}^{{{data['m']}}} mod {data['p']} = {data['g_m']}",
            f"h^r = {data['h']}^{{{data['r']}}} mod {data['p']} = {data['h_r']}",
            f"C = {data['g_m']}*{data['h_r']} mod {data['p']} = {data['commitment']}",
            f"verify: {data['commitment']} == {data['verify']}: {data['valid']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the commitment value.

        Args:
            data: Solution data dict.

        Returns:
            Commitment value as a string.
        """
        return f"C={data['commitment']}, valid={data['valid']}"


# ---------------------------------------------------------------------------
# 5. Zero-Knowledge Basic (Schnorr Protocol) (tier 6)
# ---------------------------------------------------------------------------

@register
class ZeroKnowledgeBasicGenerator(StepGenerator):
    """Schnorr identification protocol (zero-knowledge proof of discrete log).

    Prover knows x such that y = g^x mod p. Protocol:
    1. Prover sends t = g^r mod p for random r.
    2. Verifier sends challenge c.
    3. Prover sends s = r + c*x (mod q).
    Verify: g^s == t * y^c mod p.

    Difficulty scaling:
        Difficulty 1-3: p < 30.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_pow.
    """

    _P_CAPS = {
        1: 30, 2: 30, 3: 30,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "zero_knowledge_basic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "execute Schnorr zero-knowledge identification protocol"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Schnorr protocol problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._P_CAPS.get(difficulty, 100)
        primes = [p for p in _SMALL_PRIMES if 7 <= p < cap]
        p = self._rng.choice(primes)
        g = _find_generator(p)
        q = p - 1  # working modulo p-1 for exponents

        x = self._rng.randint(2, p - 2)  # secret
        y = pow(g, x, p)  # public key

        r = self._rng.randint(1, p - 2)  # commitment randomness
        t = pow(g, r, p)  # commitment

        c = self._rng.randint(1, min(10, p - 2))  # challenge
        s = (r + c * x) % q  # response

        # Verify: g^s mod p == t * y^c mod p
        lhs = pow(g, s, p)
        rhs = (t * pow(y, c, p)) % p

        return (
            f"Schnorr: p={p}, g={g}, y={y}, r={r}, c={c}",
            {"p": p, "g": g, "x": x, "y": y, "r": r, "t": t,
             "c": c, "s": s, "q": q, "lhs": lhs, "rhs": rhs,
             "valid": lhs == rhs},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Schnorr protocol.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the protocol rounds.
        """
        return [
            f"prover sends t = {data['g']}^{{{data['r']}}} mod {data['p']} = {data['t']}",
            f"verifier sends c = {data['c']}",
            f"prover sends s = {data['r']}+{data['c']}*{data['x']} mod {data['q']} = {data['s']}",
            f"verify: g^s={data['lhs']}, t*y^c={data['rhs']}, valid={data['valid']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the protocol outcome.

        Args:
            data: Solution data dict.

        Returns:
            Verification result as a string.
        """
        return f"t={data['t']}, s={data['s']}, valid={data['valid']}"


# ---------------------------------------------------------------------------
# 6. Merkle Tree (tier 5)
# ---------------------------------------------------------------------------

@register
class MerkleTreeGenerator(StepGenerator):
    """Build a binary Merkle hash tree and generate membership proofs.

    Given 4-8 leaf values, compute internal node hashes using a simple
    hash function h(a,b) = (a*31 + b*17) mod M. Generate root hash
    and a membership proof (path + siblings).

    Difficulty scaling:
        Difficulty 1-3: 4 leaves.
        Difficulty 4-6: 4-8 leaves.
        Difficulty 7-8: 8 leaves, verify proof.

    Prerequisites:
        hash_table_ops.
    """

    _MOD = 997  # small prime for hash

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "merkle_tree"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hash_table_ops"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "build Merkle tree and generate membership proof"

    def _hash_pair(self, a: int, b: int) -> int:
        """Compute hash of two values.

        Args:
            a: Left child hash.
            b: Right child hash.

        Returns:
            Combined hash value.
        """
        return (a * 31 + b * 17) % self._MOD

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Merkle tree problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_leaves = 4
        elif difficulty <= 6:
            n_leaves = self._rng.choice([4, 8])
        else:
            n_leaves = 8

        leaves = [self._rng.randint(1, 200) for _ in range(n_leaves)]

        # Build tree bottom-up
        current_level = list(leaves)
        levels = [list(current_level)]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else current_level[i]
                next_level.append(self._hash_pair(left, right))
            current_level = next_level
            levels.append(list(current_level))

        root = current_level[0]

        # Generate membership proof for a random leaf
        proof_idx = self._rng.randint(0, n_leaves - 1)
        proof_path = []
        idx = proof_idx
        for level in levels[:-1]:
            if idx % 2 == 0:
                sibling_idx = idx + 1 if idx + 1 < len(level) else idx
                proof_path.append(("right", level[sibling_idx]))
            else:
                proof_path.append(("left", level[idx - 1]))
            idx //= 2

        return (
            f"Merkle tree: leaves={leaves}",
            {"leaves": leaves, "n_leaves": n_leaves, "levels": levels,
             "root": root, "proof_idx": proof_idx,
             "proof_leaf": leaves[proof_idx], "proof_path": proof_path},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Merkle tree.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing tree construction and proof.
        """
        steps = [f"leaves: {data['leaves']}"]
        for lvl_num, level in enumerate(data["levels"][1:], 1):
            steps.append(f"level {lvl_num}: {level}")
        steps.append(f"root = {data['root']}")

        proof_str = ", ".join(f"{side}:{val}" for side, val in data["proof_path"])
        steps.append(f"proof for leaf[{data['proof_idx']}]={data['proof_leaf']}: [{proof_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the root hash and proof.

        Args:
            data: Solution data dict.

        Returns:
            Root hash as a string.
        """
        return f"root={data['root']}"


# ---------------------------------------------------------------------------
# 7. Stream Cipher (LFSR) (tier 5)
# ---------------------------------------------------------------------------

@register
class StreamCipherGenerator(StepGenerator):
    """Linear feedback shift register (LFSR) stream cipher.

    Given tap positions and initial state, generate keystream bits
    and XOR with plaintext bits to encrypt.

    Difficulty scaling:
        Difficulty 1-3: 4-bit LFSR, 4-6 output bits.
        Difficulty 4-6: 5-bit LFSR, 6-8 output bits.
        Difficulty 7-8: 6-bit LFSR, 8-10 output bits.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stream_cipher"

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
        return "generate LFSR keystream and encrypt plaintext"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an LFSR stream cipher problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            reg_size = 4
            n_bits = self._rng.randint(4, 6)
        elif difficulty <= 6:
            reg_size = 5
            n_bits = self._rng.randint(6, 8)
        else:
            reg_size = 6
            n_bits = self._rng.randint(8, 10)

        # Initial state (non-zero)
        state = [self._rng.randint(0, 1) for _ in range(reg_size)]
        while all(b == 0 for b in state):
            state = [self._rng.randint(0, 1) for _ in range(reg_size)]

        # Choose 2 tap positions (0-indexed from MSB)
        taps = sorted(self._rng.sample(range(reg_size), 2))

        # Plaintext bits
        plaintext = [self._rng.randint(0, 1) for _ in range(n_bits)]

        # Generate keystream
        reg = list(state)
        keystream = []
        for _ in range(n_bits):
            keystream.append(reg[-1])  # output is rightmost bit
            feedback = 0
            for tap in taps:
                feedback ^= reg[tap]
            reg = [feedback] + reg[:-1]

        # Encrypt
        ciphertext = [p ^ k for p, k in zip(plaintext, keystream)]

        state_str = "".join(str(b) for b in state)
        plain_str = "".join(str(b) for b in plaintext)

        return (
            f"LFSR: state={state_str}, taps={taps}, plaintext={plain_str}",
            {"reg_size": reg_size, "state": state, "taps": taps,
             "plaintext": plaintext, "keystream": keystream,
             "ciphertext": ciphertext, "n_bits": n_bits},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for LFSR encryption.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing keystream generation and XOR.
        """
        ks_str = "".join(str(b) for b in data["keystream"])
        pt_str = "".join(str(b) for b in data["plaintext"])
        ct_str = "".join(str(b) for b in data["ciphertext"])
        steps = [
            f"LFSR taps at positions {data['taps']}",
            f"keystream: {ks_str}",
            f"plaintext:  {pt_str}",
            f"XOR: {pt_str} ^ {ks_str} = {ct_str}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ciphertext.

        Args:
            data: Solution data dict.

        Returns:
            Ciphertext bits as a string.
        """
        return "".join(str(b) for b in data["ciphertext"])


# ---------------------------------------------------------------------------
# 8. Block Cipher Modes (tier 5)
# ---------------------------------------------------------------------------

@register
class BlockCipherModesGenerator(StepGenerator):
    """Compare ECB and CBC block cipher modes of operation.

    ECB encrypts each block independently: c_i = E(p_i).
    CBC chains: c_i = E(p_i XOR c_{i-1}), with c_0 = IV.
    Uses a simple E(x) = (x * key + 13) mod 256 for demonstration.

    Difficulty scaling:
        Difficulty 1-3: 2 blocks, values < 64.
        Difficulty 4-6: 3 blocks, values < 128.
        Difficulty 7-8: 3-4 blocks, values < 256.

    Prerequisites:
        binary_arithmetic.
    """

    _PARAMS = {
        1: {"n_blocks": 2, "cap": 64},
        2: {"n_blocks": 2, "cap": 64},
        3: {"n_blocks": 2, "cap": 64},
        4: {"n_blocks": 3, "cap": 128},
        5: {"n_blocks": 3, "cap": 128},
        6: {"n_blocks": 3, "cap": 128},
        7: {"n_blocks": 3, "cap": 256},
        8: {"n_blocks": 4, "cap": 256},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "block_cipher_modes"

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
        return "encrypt blocks in ECB and CBC modes and compare"

    def _encrypt_block(self, block: int, key: int) -> int:
        """Simple block cipher: E(x) = (x * key + 13) mod 256.

        Args:
            block: Plaintext block (0-255).
            key: Key value.

        Returns:
            Encrypted block.
        """
        return (block * key + 13) % 256

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a block cipher modes problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        n_blocks = params["n_blocks"]
        cap = params["cap"]

        plaintext = [self._rng.randint(0, cap - 1) for _ in range(n_blocks)]
        key = self._rng.choice([3, 5, 7, 9, 11, 13, 15])
        iv = self._rng.randint(0, cap - 1)

        # ECB mode
        ecb = [self._encrypt_block(p, key) for p in plaintext]

        # CBC mode
        cbc = []
        prev = iv
        for p in plaintext:
            xored = p ^ prev
            c = self._encrypt_block(xored, key)
            cbc.append(c)
            prev = c

        # Check if ECB shows pattern (duplicate blocks)
        ecb_has_pattern = len(set(ecb)) < len(ecb) if len(plaintext) == len(set(plaintext)) else True

        return (
            f"E(x)=(x*{key}+13) mod 256, blocks={plaintext}, IV={iv}",
            {"plaintext": plaintext, "key": key, "iv": iv,
             "n_blocks": n_blocks, "ecb": ecb, "cbc": cbc,
             "ecb_has_pattern": ecb_has_pattern},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for block cipher modes.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing ECB and CBC computations.
        """
        steps = []
        for i, (p, c) in enumerate(zip(data["plaintext"], data["ecb"])):
            steps.append(f"ECB[{i}]: E({p}) = {c}")

        prev = data["iv"]
        for i, (p, c) in enumerate(zip(data["plaintext"], data["cbc"])):
            xored = p ^ prev
            steps.append(f"CBC[{i}]: {p} XOR {prev}={xored}, E({xored})={c}")
            prev = c

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return both mode outputs.

        Args:
            data: Solution data dict.

        Returns:
            ECB and CBC ciphertexts as a string.
        """
        return f"ECB={data['ecb']}, CBC={data['cbc']}"
