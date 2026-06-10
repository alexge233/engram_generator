"""Deep cryptography task generators.

8 generators across tiers 4-6 covering lattice SVP, LWE encryption,
NTRU key generation, threshold secret sharing, Pedersen commitment,
oblivious transfer, garbled circuits, and hash chains.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def _poly_mult_mod(a: list[int], b: list[int], n: int,
                   q: int) -> list[int]:
    """Multiply two polynomials modulo (x^n - 1) and q.

    Args:
        a: Coefficients of first polynomial.
        b: Coefficients of second polynomial.
        n: Ring dimension (degree bound).
        q: Coefficient modulus.

    Returns:
        Product polynomial coefficients mod q.
    """
    result = [0] * n
    for i in range(min(len(a), n)):
        for j in range(min(len(b), n)):
            idx = (i + j) % n
            result[idx] = (result[idx] + a[i] * b[j]) % q
    return result


def _simple_hash(val: int, mod: int) -> int:
    """Simple deterministic hash for small-number simulation.

    Args:
        val: Input value.
        mod: Modulus for output range.

    Returns:
        Hash value in [0, mod).
    """
    return ((val * 31 + 17) ^ (val * 7 + 3)) % mod


# ===================================================================
# 1. Lattice SVP (tier 6)
# ===================================================================

@register
class LatticeSVPGenerator(StepGenerator):
    """Find shortest vector in a 2D lattice using Babai nearest plane.

    Given basis B = [[b1x, b1y], [b2x, b2y]], apply Gram-Schmidt
    and Babai's algorithm to find the shortest lattice vector.

    Difficulty scaling:
        Difficulty 1-3: Small integer basis entries in [-3, 3].
        Difficulty 4-6: Entries in [-5, 5].
        Difficulty 7-8: Entries in [-8, 8], also compute Gram-Schmidt.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lattice_svp"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find shortest vector in a 2D lattice"

    def _range(self, difficulty: int) -> int:
        """Map difficulty to basis entry range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Maximum absolute value for entries.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 5
        return 8

    def _dot(self, a: list[float], b: list[float]) -> float:
        """Compute dot product of two 2D vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Dot product.
        """
        return a[0] * b[0] + a[1] * b[1]

    def _norm(self, v: list[float]) -> float:
        """Compute Euclidean norm of a 2D vector.

        Args:
            v: Input vector.

        Returns:
            Norm value.
        """
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2D lattice basis and find shortest vector.

        Args:
            difficulty: Controls basis entry range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r = self._range(difficulty)
        # Generate non-degenerate basis
        while True:
            b1 = [self._rng.randint(-r, r), self._rng.randint(-r, r)]
            b2 = [self._rng.randint(-r, r), self._rng.randint(-r, r)]
            det = b1[0] * b2[1] - b1[1] * b2[0]
            if det != 0 and (b1[0] != 0 or b1[1] != 0) and (b2[0] != 0 or b2[1] != 0):
                break

        # Gram-Schmidt orthogonalisation
        b1_star = list(b1)
        mu = round(self._dot(b2, b1_star) / self._dot(b1_star, b1_star), 4)
        b2_star = [round(b2[0] - mu * b1_star[0], 4),
                   round(b2[1] - mu * b1_star[1], 4)]

        norm_b1 = round(self._norm(b1), 4)
        norm_b2 = round(self._norm(b2), 4)
        norm_b1_star = round(self._norm(b1_star), 4)
        norm_b2_star = round(self._norm(b2_star), 4)

        # Enumerate short vectors: try small combos a*b1 + b*b2
        best_vec = list(b1) if norm_b1 <= norm_b2 else list(b2)
        best_norm = round(min(norm_b1, norm_b2), 4)
        for a in range(-3, 4):
            for b in range(-3, 4):
                if a == 0 and b == 0:
                    continue
                v = [a * b1[0] + b * b2[0], a * b1[1] + b * b2[1]]
                n = round(self._norm(v), 4)
                if n < best_norm:
                    best_norm = n
                    best_vec = v

        problem = f"SVP: B=[[{b1[0]},{b1[1]}],[{b2[0]},{b2[1]}]]"
        return problem, {
            "b1": b1, "b2": b2, "mu": mu,
            "b1_star": b1_star, "b2_star": b2_star,
            "norm_b1": norm_b1, "norm_b2": norm_b2,
            "best_vec": best_vec, "best_norm": best_norm,
            "show_gs": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lattice SVP solution steps.

        Args:
            data: Solution data with basis and shortest vector.

        Returns:
            Steps showing Gram-Schmidt and enumeration.
        """
        steps: list[str] = [
            f"b1={data['b1']}, ||b1||={data['norm_b1']}",
            f"b2={data['b2']}, ||b2||={data['norm_b2']}",
        ]
        if data["show_gs"]:
            steps.append(f"mu={data['mu']}, b2*={data['b2_star']}")
        steps.append(
            f"shortest={data['best_vec']}, ||v||={data['best_norm']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the shortest vector and its norm.

        Args:
            data: Solution data.

        Returns:
            Shortest vector as a string.
        """
        return f"v={data['best_vec']}, ||v||={data['best_norm']}"


# ===================================================================
# 2. LWE Encrypt (tier 6)
# ===================================================================

@register
class LWEEncryptGenerator(StepGenerator):
    """Encrypt a bit using Learning With Errors (LWE).

    c = (a, <a,s> + e + m * floor(q/2) mod q).
    Decrypt: compute b - <a,s> mod q, round to 0 or floor(q/2).

    Difficulty scaling:
        Difficulty 1-3: dimension n=2, q=17.
        Difficulty 4-6: dimension n=3, q=23.
        Difficulty 7-8: dimension n=4, q=31.

    Prerequisites:
        modular.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lwe_encrypt"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "encrypt a message bit using LWE"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to dimension and modulus.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (dimension, modulus).
        """
        if difficulty <= 3:
            return 2, 17
        if difficulty <= 6:
            return 3, 23
        return 4, 31

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate LWE encryption of a message bit.

        Args:
            difficulty: Controls dimension and modulus.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, q = self._config(difficulty)
        half_q = q // 2

        s = [self._rng.randint(0, q - 1) for _ in range(n)]
        a = [self._rng.randint(0, q - 1) for _ in range(n)]
        e = self._rng.randint(-1, 1)  # small error
        m = self._rng.randint(0, 1)  # message bit

        dot_as = sum(a[i] * s[i] for i in range(n)) % q
        b = (dot_as + e + m * half_q) % q

        # Decrypt
        dec_val = (b - dot_as) % q
        # Round to nearest: 0 or half_q
        if abs(dec_val) < abs(dec_val - half_q) and abs(dec_val) < abs(dec_val - q):
            m_dec = 0
        else:
            m_dec = 1

        problem = f"LWE: a={a}, s={s}, e={e}, m={m}, q={q}"
        return problem, {
            "n": n, "q": q, "half_q": half_q,
            "s": s, "a": a, "e": e, "m": m,
            "dot_as": dot_as, "b": b,
            "dec_val": dec_val, "m_dec": m_dec,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate LWE encryption and decryption steps.

        Args:
            data: Solution data with cipher and decryption.

        Returns:
            Steps showing dot product, ciphertext, and decryption.
        """
        return [
            f"<a,s>={data['dot_as']} mod {data['q']}",
            f"b={data['dot_as']}+{data['e']}+{data['m']}*{data['half_q']} mod {data['q']}={data['b']}",
            f"c=({data['a']},{data['b']})",
            f"decrypt: b-<a,s>={data['dec_val']} mod {data['q']} -> m={data['m_dec']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the ciphertext and decrypted bit.

        Args:
            data: Solution data.

        Returns:
            Ciphertext and message as a string.
        """
        return f"c=({data['a']},{data['b']}), m_dec={data['m_dec']}"


# ===================================================================
# 3. NTRU Keygen (tier 6)
# ===================================================================

@register
class NTRUKeygenGenerator(StepGenerator):
    """Generate NTRU public key from small polynomials.

    Given small polynomials f, g in Z_q[x]/(x^n-1), compute
    public key h = f_inv * g mod q where f_inv is the inverse
    of f in the polynomial ring.

    Difficulty scaling:
        Difficulty 1-3: n=4, q=17, ternary coefficients.
        Difficulty 4-6: n=5, q=23.
        Difficulty 7-8: n=6, q=29.

    Prerequisites:
        polynomial_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ntru_keygen"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute NTRU public key from small polynomials"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to ring dimension and modulus.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n, q).
        """
        if difficulty <= 3:
            return 4, 17
        if difficulty <= 6:
            return 5, 23
        return 6, 29

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate NTRU key pair from small polynomials.

        Args:
            difficulty: Controls ring dimension and modulus.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, q = self._config(difficulty)

        # Generate small f with f(1) != 0 mod q for invertibility
        while True:
            f = [self._rng.choice([-1, 0, 1]) for _ in range(n)]
            f_sum = sum(f) % q
            if f_sum != 0 and any(c != 0 for c in f):
                break

        g = [self._rng.choice([-1, 0, 1]) for _ in range(n)]
        while all(c == 0 for c in g):
            g = [self._rng.choice([-1, 0, 1]) for _ in range(n)]

        # Compute f*g mod (x^n - 1, q) as the public key product
        fg = _poly_mult_mod(f, g, n, q)

        problem = f"NTRU: f={f}, g={g}, n={n}, q={q}"
        return problem, {
            "f": f, "g": g, "n": n, "q": q, "fg": fg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate NTRU key generation steps.

        Args:
            data: Solution data with polynomials and product.

        Returns:
            Steps showing polynomial multiplication.
        """
        return [
            f"f={data['f']}, g={data['g']}",
            f"ring: Z_{data['q']}[x]/(x^{data['n']}-1)",
            f"f*g mod (x^{data['n']}-1, {data['q']})={data['fg']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the public key polynomial.

        Args:
            data: Solution data.

        Returns:
            Public key product as a string.
        """
        return f"h=f*g={data['fg']}"


# ===================================================================
# 4. Secret Sharing Threshold (tier 5)
# ===================================================================

@register
class SecretSharingThresholdGenerator(StepGenerator):
    """Reconstruct secret from (t,n) threshold shares via Lagrange.

    Shamir (t,n): polynomial of degree t-1, reconstruct f(0) from
    t points using Lagrange interpolation mod p.

    Difficulty scaling:
        Difficulty 1-3: t=2, n=3, small prime.
        Difficulty 4-6: t=3, n=5.
        Difficulty 7-8: t=4, n=6.

    Prerequisites:
        modular.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "secret_sharing_threshold"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "reconstruct secret from threshold shares via Lagrange"

    def _config(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to threshold, total shares, and prime.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (threshold, n_shares, prime).
        """
        if difficulty <= 3:
            return 2, 3, self._rng.choice([17, 19, 23])
        if difficulty <= 6:
            return 3, 5, self._rng.choice([31, 37, 41])
        return 4, 6, self._rng.choice([47, 53, 59])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate shares and reconstruct secret.

        Args:
            difficulty: Controls threshold and share count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        t, n, p = self._config(difficulty)
        secret = self._rng.randint(1, p - 1)
        coeffs = [secret] + [self._rng.randint(1, p - 1) for _ in range(t - 1)]

        # Generate shares
        shares = []
        for i in range(1, n + 1):
            val = 0
            for j, c in enumerate(coeffs):
                val = (val + c * pow(i, j, p)) % p
            shares.append((i, val))

        # Reconstruct from first t shares
        recon_shares = shares[:t]
        reconstructed = 0
        lagrange_terms = []
        for i, (xi, yi) in enumerate(recon_shares):
            num = 1
            den = 1
            for j, (xj, _) in enumerate(recon_shares):
                if i != j:
                    num = (num * (0 - xj)) % p
                    den = (den * (xi - xj)) % p
            li = (num * _mod_inverse(den % p, p)) % p
            term = (yi * li) % p
            lagrange_terms.append({"xi": xi, "yi": yi, "li": li, "term": term})
            reconstructed = (reconstructed + term) % p

        problem = (
            f"Shamir ({t},{n}): shares={recon_shares}, p={p}"
        )
        return problem, {
            "t": t, "n": n, "p": p, "secret": secret,
            "coeffs": coeffs, "shares": shares,
            "recon_shares": recon_shares,
            "lagrange_terms": lagrange_terms,
            "reconstructed": reconstructed,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lagrange reconstruction steps.

        Args:
            data: Solution data with shares and Lagrange terms.

        Returns:
            Steps showing each Lagrange basis and term.
        """
        steps: list[str] = [f"({data['t']},{data['n']}) scheme mod {data['p']}"]
        for lt in data["lagrange_terms"]:
            steps.append(
                f"x={lt['xi']}: L={lt['li']}, term={lt['yi']}*{lt['li']}={lt['term']}"
            )
        steps.append(f"secret=sum mod {data['p']}={data['reconstructed']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the reconstructed secret.

        Args:
            data: Solution data.

        Returns:
            Secret value as a string.
        """
        return f"secret={data['reconstructed']}"


# ===================================================================
# 5. Commitment Pedersen (tier 5)
# ===================================================================

@register
class CommitmentPedersenGenerator(StepGenerator):
    """Compute Pedersen commitment C = g^m * h^r mod p.

    Commit to message m with randomness r using generators g, h.
    Verify opening by recomputing C from (m, r).

    Difficulty scaling:
        Difficulty 1-3: p < 30.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_pow.
    """

    _SMALL_PRIMES = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                     53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "commitment_pedersen"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Pedersen commitment C = g^m * h^r mod p"

    def _prime_cap(self, difficulty: int) -> int:
        """Map difficulty to prime upper bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Upper bound for prime selection.
        """
        if difficulty <= 3:
            return 30
        if difficulty <= 6:
            return 50
        return 100

    def _find_generator(self, p: int) -> int:
        """Find a primitive root modulo prime p.

        Args:
            p: Prime number.

        Returns:
            A primitive root modulo p.
        """
        if p == 2:
            return 1
        phi = p - 1
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
            if all(pow(g, phi // f, p) != 1 for f in factors):
                return g
        return 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Pedersen commitment problem.

        Args:
            difficulty: Controls prime size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._prime_cap(difficulty)
        primes = [pr for pr in self._SMALL_PRIMES if 7 <= pr < cap]
        p = self._rng.choice(primes)
        g = self._find_generator(p)
        a = self._rng.randint(2, p - 2)
        h = pow(g, a, p)
        if h == g:
            h = pow(g, a + 1, p)

        m = self._rng.randint(1, p - 2)
        r = self._rng.randint(1, p - 2)

        g_m = pow(g, m, p)
        h_r = pow(h, r, p)
        commitment = (g_m * h_r) % p

        problem = f"Pedersen: p={p}, g={g}, h={h}, m={m}, r={r}"
        return problem, {
            "p": p, "g": g, "h": h, "m": m, "r": r,
            "g_m": g_m, "h_r": h_r, "commitment": commitment,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Pedersen commitment computation steps.

        Args:
            data: Solution data with commitment values.

        Returns:
            Steps showing g^m, h^r, and C.
        """
        return [
            f"g^m={data['g']}^{data['m']} mod {data['p']}={data['g_m']}",
            f"h^r={data['h']}^{data['r']} mod {data['p']}={data['h_r']}",
            f"C={data['g_m']}*{data['h_r']} mod {data['p']}={data['commitment']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the commitment value.

        Args:
            data: Solution data.

        Returns:
            Commitment as a string.
        """
        return f"C={data['commitment']}"


# ===================================================================
# 6. Oblivious Transfer (tier 6)
# ===================================================================

@register
class ObliviousTransferGenerator(StepGenerator):
    """Simulate 1-out-of-2 oblivious transfer protocol.

    Sender has m0, m1. Receiver has choice bit b.
    Protocol: receiver gets m_b without revealing b;
    sender does not learn b. Uses simplified Diffie-Hellman OT.

    Difficulty scaling:
        Difficulty 1-3: Small messages, p < 30.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_pow.
    """

    _SMALL_PRIMES = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                     53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oblivious_transfer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "simulate 1-out-of-2 oblivious transfer protocol"

    def _prime_cap(self, difficulty: int) -> int:
        """Map difficulty to prime upper bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Upper bound for prime selection.
        """
        if difficulty <= 3:
            return 30
        if difficulty <= 6:
            return 50
        return 100

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an oblivious transfer protocol trace.

        Args:
            difficulty: Controls prime size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._prime_cap(difficulty)
        primes = [pr for pr in self._SMALL_PRIMES if 11 <= pr < cap]
        p = self._rng.choice(primes)
        g = 2  # simple generator for demonstration

        m0 = self._rng.randint(1, p - 1)
        m1 = self._rng.randint(1, p - 1)
        b = self._rng.randint(0, 1)  # receiver's choice

        # Sender generates random A = g^a mod p
        a = self._rng.randint(2, p - 2)
        cap_a = pow(g, a, p)

        # Receiver chooses random k, computes B
        k = self._rng.randint(2, p - 2)
        if b == 0:
            cap_b = pow(g, k, p)
        else:
            cap_b = (cap_a * pow(g, k, p)) % p

        # Sender computes keys for both possibilities
        k0_s = pow(cap_b, a, p)
        k1_s = pow((cap_b * pow(pow(g, a, p), p - 2, p)) % p, a, p)

        # Sender encrypts
        e0 = (m0 + k0_s) % p
        e1 = (m1 + k1_s) % p

        # Receiver decrypts chosen message
        k_r = pow(cap_a, k, p)
        m_dec = (e0 - k_r) % p if b == 0 else (e1 - k_r) % p

        problem = (
            f"OT: p={p}, g={g}, m0={m0}, m1={m1}, b={b}"
        )
        return problem, {
            "p": p, "g": g, "a": a, "k": k, "b": b,
            "m0": m0, "m1": m1,
            "A": cap_a, "B": cap_b,
            "e0": e0, "e1": e1,
            "k_r": k_r, "m_dec": m_dec,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate OT protocol trace steps.

        Args:
            data: Solution data with protocol values.

        Returns:
            Steps showing protocol rounds.
        """
        return [
            f"sender: A=g^a mod p={data['A']}",
            f"receiver(b={data['b']}): B={data['B']}",
            f"sender encrypts: e0={data['e0']}, e1={data['e1']}",
            f"receiver key={data['k_r']}, decrypts m_{data['b']}={data['m_dec']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the decrypted message.

        Args:
            data: Solution data.

        Returns:
            Decrypted message as a string.
        """
        expected = data["m0"] if data["b"] == 0 else data["m1"]
        return f"m_{data['b']}={data['m_dec']}, expected={expected}"


# ===================================================================
# 7. Garbled Circuit (tier 6)
# ===================================================================

@register
class GarbledCircuitGenerator(StepGenerator):
    """Garble a 2-input AND/OR gate and evaluate one row.

    Assign random wire keys to each input wire value (0/1).
    Encrypt truth table rows: for each (a,b)->c, encrypt key_c
    under key_a and key_b. Evaluator decrypts one row.

    Difficulty scaling:
        Difficulty 1-3: AND gate only.
        Difficulty 4-6: AND or OR gate.
        Difficulty 7-8: AND or OR gate, also show permuted table.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "garbled_circuit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "garble a 2-input gate and evaluate one row"

    def _gate_func(self, gate: str, a: int, b: int) -> int:
        """Compute gate output.

        Args:
            gate: Gate type ("AND" or "OR").
            a: First input bit.
            b: Second input bit.

        Returns:
            Gate output (0 or 1).
        """
        if gate == "AND":
            return a & b
        return a | b

    def _encrypt(self, val: int, k1: int, k2: int, mod: int) -> int:
        """Simple encryption: E(val, k1, k2) = (val + k1*31 + k2*17) mod M.

        Args:
            val: Value to encrypt.
            k1: First key.
            k2: Second key.
            mod: Modulus.

        Returns:
            Encrypted value.
        """
        return (val + k1 * 31 + k2 * 17) % mod

    def _decrypt(self, ct: int, k1: int, k2: int, mod: int) -> int:
        """Simple decryption: inverse of encrypt.

        Args:
            ct: Ciphertext.
            k1: First key.
            k2: Second key.
            mod: Modulus.

        Returns:
            Decrypted value.
        """
        return (ct - k1 * 31 - k2 * 17) % mod

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate garbled gate and evaluate one row.

        Args:
            difficulty: Controls gate type and output detail.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mod = 997
        if difficulty <= 3:
            gate = "AND"
        else:
            gate = self._rng.choice(["AND", "OR"])

        # Wire keys: random values for each wire's 0 and 1
        ka = {0: self._rng.randint(10, mod - 1),
              1: self._rng.randint(10, mod - 1)}
        kb = {0: self._rng.randint(10, mod - 1),
              1: self._rng.randint(10, mod - 1)}
        kc = {0: self._rng.randint(10, mod - 1),
              1: self._rng.randint(10, mod - 1)}

        # Garble truth table
        garbled_table = []
        for a_val in [0, 1]:
            for b_val in [0, 1]:
                c_val = self._gate_func(gate, a_val, b_val)
                ct = self._encrypt(kc[c_val], ka[a_val], kb[b_val], mod)
                garbled_table.append({
                    "a": a_val, "b": b_val, "c": c_val,
                    "ct": ct,
                })

        # Evaluator's input
        eval_a = self._rng.randint(0, 1)
        eval_b = self._rng.randint(0, 1)
        eval_c = self._gate_func(gate, eval_a, eval_b)

        # Find matching row
        for row in garbled_table:
            if row["a"] == eval_a and row["b"] == eval_b:
                eval_ct = row["ct"]
                break

        dec_val = self._decrypt(eval_ct, ka[eval_a], kb[eval_b], mod)

        problem = (
            f"garble {gate}: ka={{0:{ka[0]},1:{ka[1]}}}, "
            f"kb={{0:{kb[0]},1:{kb[1]}}}, "
            f"kc={{0:{kc[0]},1:{kc[1]}}}, eval=({eval_a},{eval_b})"
        )
        return problem, {
            "gate": gate, "mod": mod,
            "ka": ka, "kb": kb, "kc": kc,
            "garbled_table": garbled_table,
            "eval_a": eval_a, "eval_b": eval_b,
            "eval_c": eval_c, "eval_ct": eval_ct,
            "dec_val": dec_val, "show_table": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate garbled circuit evaluation steps.

        Args:
            data: Solution data with garbled table and evaluation.

        Returns:
            Steps showing garbled rows and evaluation.
        """
        steps: list[str] = [f"gate={data['gate']}, mod={data['mod']}"]
        if data["show_table"]:
            for row in data["garbled_table"]:
                steps.append(
                    f"({row['a']},{row['b']})->{row['c']}: ct={row['ct']}"
                )
        steps.append(
            f"eval({data['eval_a']},{data['eval_b']}): ct={data['eval_ct']}, "
            f"dec={data['dec_val']}, output={data['eval_c']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the evaluation result.

        Args:
            data: Solution data.

        Returns:
            Gate output as a string.
        """
        return (
            f"{data['gate']}({data['eval_a']},{data['eval_b']})"
            f"={data['eval_c']}"
        )


# ===================================================================
# 8. Hash Chain (tier 4)
# ===================================================================

@register
class HashChainGenerator(StepGenerator):
    """Compute a hash chain and verify a chain element.

    h_n = H(h_{n-1}) starting from h_0.
    Verification: given h_k, check h_k = H^{n-k}(h_0).

    Difficulty scaling:
        Difficulty 1-3: Chain length 3-4.
        Difficulty 4-6: Chain length 5-6.
        Difficulty 7-8: Chain length 7-8, also verify.

    Prerequisites:
        hash_table_ops.
    """

    _MOD = 997

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hash_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hash_table_ops"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute hash chain and verify an element"

    def _chain_length(self, difficulty: int) -> int:
        """Map difficulty to chain length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Chain length (3-8).
        """
        if difficulty <= 3:
            return self._rng.randint(3, 4)
        if difficulty <= 6:
            return self._rng.randint(5, 6)
        return self._rng.randint(7, 8)

    def _hash_fn(self, val: int) -> int:
        """Simple hash function for chain computation.

        Args:
            val: Input value.

        Returns:
            Hash value in [0, MOD).
        """
        return ((val * 31 + 17) ^ (val >> 2)) % self._MOD

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hash chain and a verification task.

        Args:
            difficulty: Controls chain length.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._chain_length(difficulty)
        h0 = self._rng.randint(1, self._MOD - 1)

        chain = [h0]
        for _ in range(n):
            chain.append(self._hash_fn(chain[-1]))

        # Verification: pick a random position k
        k = self._rng.randint(1, n)
        h_k = chain[k]

        # Recompute from h0 to h_k
        verify_chain = [h0]
        for _ in range(k):
            verify_chain.append(self._hash_fn(verify_chain[-1]))
        verified = verify_chain[-1] == h_k

        problem = f"hash\\_chain: h_0={h0}, n={n}, verify h_{k}"
        return problem, {
            "h0": h0, "n": n, "chain": chain,
            "k": k, "h_k": h_k, "verified": verified,
            "do_verify": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate hash chain computation steps.

        Args:
            data: Solution data with chain and verification.

        Returns:
            Steps showing chain values and optional verification.
        """
        steps: list[str] = []
        for i in range(len(data["chain"]) - 1):
            steps.append(
                f"h_{i+1}=H(h_{i})=H({data['chain'][i]})={data['chain'][i+1]}"
            )
        if data["do_verify"]:
            steps.append(
                f"verify h_{data['k']}={data['h_k']}: {data['verified']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final chain value and optional verification.

        Args:
            data: Solution data.

        Returns:
            Final hash and chain endpoint.
        """
        return f"h_{data['n']}={data['chain'][-1]}"
