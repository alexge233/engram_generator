"""Cryptography task generators.

10 generators across tiers 4-6 covering RSA, Diffie-Hellman,
elliptic curves, hashing, digital signatures, OTP, Feistel,
and AES MixColumns.
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


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular inverse of a mod m.

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


def _gf256_mul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) with AES irreducible polynomial.

    Uses the polynomial x^8 + x^4 + x^3 + x + 1  (0x11B).

    Args:
        a: First byte (0-255).
        b: Second byte (0-255).

    Returns:
        Product in GF(2^8).
    """
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B  # x^8 reduced by x^4+x^3+x+1
        b >>= 1
    return result


# ---------------------------------------------------------------------------
# 1. RSA Key Generation
# ---------------------------------------------------------------------------

@register
class RSAKeygenGenerator(StepGenerator):
    """Generate an RSA key pair from two small primes.

    Given primes p and q, compute n = p*q, phi = (p-1)*(q-1),
    choose e coprime to phi, and compute d = e^{-1} mod phi.

    Difficulty scaling:
        Difficulty 1-3: p, q < 20.
        Difficulty 4-6: p, q < 50.
        Difficulty 7-8: p, q < 100.

    Prerequisites:
        totient, mod_inv.
    """

    _PRIME_CAPS = {
        1: 20, 2: 20, 3: 20,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rsa_keygen"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["totient", "mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "generate RSA key pair from two primes"

    def _pick_primes(self, cap: int) -> tuple[int, int]:
        """Pick two distinct primes below the cap.

        Args:
            cap: Upper bound for primes.

        Returns:
            Tuple (p, q) with p != q.
        """
        pool = [p for p in _SMALL_PRIMES if p < cap and p > 2]
        p = self._rng.choice(pool)
        q = self._rng.choice([x for x in pool if x != p])
        return p, q

    def _choose_e(self, phi: int) -> int:
        """Choose a small public exponent coprime to phi.

        Args:
            phi: Euler's totient of n.

        Returns:
            Public exponent e.
        """
        for candidate in [3, 5, 7, 11, 13, 17, 19, 23]:
            if candidate < phi and math.gcd(candidate, phi) == 1:
                return candidate
        # Fallback: search upward
        for candidate in range(3, phi, 2):
            if math.gcd(candidate, phi) == 1:
                return candidate
        return 65537  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RSA keygen problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._PRIME_CAPS.get(difficulty, 100)
        p, q = self._pick_primes(cap)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = self._choose_e(phi)
        d = _mod_inverse(e, phi)
        return (
            f"RSA keygen: p={p}, q={q}",
            {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for RSA keygen.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing n, phi, e selection, and d computation.
        """
        return [
            f"n = {data['p']}*{data['q']} = {data['n']}",
            f"phi = ({data['p']}-1)*({data['q']}-1) = {data['phi']}",
            f"choose e = {data['e']}, gcd({data['e']},{data['phi']}) = 1",
            f"d = {data['e']}^{{-1}} mod {data['phi']} = {data['d']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the RSA key pair.

        Args:
            data: Solution data dict.

        Returns:
            Public and private key as a string.
        """
        return f"public=({data['e']},{data['n']}), private=({data['d']},{data['n']})"


# ---------------------------------------------------------------------------
# 2. RSA Encryption
# ---------------------------------------------------------------------------

@register
class RSAEncryptGenerator(StepGenerator):
    """Encrypt a message using RSA: c = m^e mod n.

    Given plaintext m, public exponent e, and modulus n, compute
    the ciphertext via modular exponentiation.

    Difficulty scaling:
        Difficulty 1-3: p, q < 20, m < 20.
        Difficulty 4-6: p, q < 50, m < 50.
        Difficulty 7-8: p, q < 100, m < 100.

    Prerequisites:
        mod_pow.
    """

    _PRIME_CAPS = {
        1: 20, 2: 20, 3: 20,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rsa_encrypt"

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
        return "encrypt message using RSA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RSA encryption problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._PRIME_CAPS.get(difficulty, 100)
        pool = [p for p in _SMALL_PRIMES if 2 < p < cap]
        p = self._rng.choice(pool)
        q = self._rng.choice([x for x in pool if x != p])
        n = p * q
        phi = (p - 1) * (q - 1)
        # Choose small e
        e = 3
        for candidate in [3, 5, 7, 11, 13, 17]:
            if candidate < phi and math.gcd(candidate, phi) == 1:
                e = candidate
                break
        m = self._rng.randint(2, min(n - 1, cap - 1))
        c = pow(m, e, n)
        return (
            f"RSA encrypt: m={m}, e={e}, n={n}",
            {"m": m, "e": e, "n": n, "c": c},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for RSA encryption.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the modular exponentiation.
        """
        m, e, n, c = data["m"], data["e"], data["n"], data["c"]
        raw = data["m"] ** data["e"]
        return [
            f"c = {m}^{{{e}}} mod {n}",
            f"{m}^{{{e}}} = {raw}",
            f"{raw} mod {n} = {c}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the ciphertext.

        Args:
            data: Solution data dict.

        Returns:
            Ciphertext as a string.
        """
        return str(data["c"])


# ---------------------------------------------------------------------------
# 3. RSA Decryption
# ---------------------------------------------------------------------------

@register
class RSADecryptGenerator(StepGenerator):
    """Decrypt an RSA ciphertext: m = c^d mod n.

    Given ciphertext c, private exponent d, and modulus n, recover
    the plaintext via modular exponentiation.

    Difficulty scaling:
        Difficulty 1-3: p, q < 20.
        Difficulty 4-6: p, q < 50.
        Difficulty 7-8: p, q < 100.

    Prerequisites:
        mod_pow.
    """

    _PRIME_CAPS = {
        1: 20, 2: 20, 3: 20,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rsa_decrypt"

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
        return "decrypt RSA ciphertext"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RSA decryption problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._PRIME_CAPS.get(difficulty, 100)
        pool = [p for p in _SMALL_PRIMES if 2 < p < cap]
        p = self._rng.choice(pool)
        q = self._rng.choice([x for x in pool if x != p])
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 3
        for candidate in [3, 5, 7, 11, 13, 17]:
            if candidate < phi and math.gcd(candidate, phi) == 1:
                e = candidate
                break
        d = _mod_inverse(e, phi)
        m = self._rng.randint(2, min(n - 1, cap - 1))
        c = pow(m, e, n)
        return (
            f"RSA decrypt: c={c}, d={d}, n={n}",
            {"c": c, "d": d, "n": n, "m": m, "e": e, "p": p, "q": q},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for RSA decryption.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the modular exponentiation.
        """
        c, d, n, m = data["c"], data["d"], data["n"], data["m"]
        return [
            f"m = {c}^{{{d}}} mod {n}",
            f"compute via repeated squaring",
            f"{c}^{{{d}}} mod {n} = {m}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the recovered plaintext.

        Args:
            data: Solution data dict.

        Returns:
            Plaintext as a string.
        """
        return str(data["m"])


# ---------------------------------------------------------------------------
# 4. Diffie-Hellman Key Exchange
# ---------------------------------------------------------------------------

@register
class DiffieHellmanGenerator(StepGenerator):
    """Diffie-Hellman key exchange computation.

    Given prime p, generator g, and private keys a, b, compute
    A = g^a mod p, B = g^b mod p, and shared secret = B^a mod p.

    Difficulty scaling:
        Difficulty 1-3: p < 23, g < 5, exponents < 10.
        Difficulty 4-6: p < 50, g < 10, exponents < 20.
        Difficulty 7-8: p < 100, g < 15, exponents < 30.

    Prerequisites:
        mod_pow.
    """

    _PARAMS = {
        1: {"p_cap": 23, "g_cap": 5, "exp_cap": 10},
        2: {"p_cap": 23, "g_cap": 5, "exp_cap": 10},
        3: {"p_cap": 23, "g_cap": 5, "exp_cap": 10},
        4: {"p_cap": 50, "g_cap": 10, "exp_cap": 20},
        5: {"p_cap": 50, "g_cap": 10, "exp_cap": 20},
        6: {"p_cap": 50, "g_cap": 10, "exp_cap": 20},
        7: {"p_cap": 100, "g_cap": 15, "exp_cap": 30},
        8: {"p_cap": 100, "g_cap": 15, "exp_cap": 30},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diffie_hellman"

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
        return "compute Diffie-Hellman key exchange"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Diffie-Hellman problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        primes = [x for x in _SMALL_PRIMES if x >= 5 and x < params["p_cap"]]
        p = self._rng.choice(primes)
        g = self._rng.randint(2, min(params["g_cap"], p - 1))
        a = self._rng.randint(2, params["exp_cap"])
        b = self._rng.randint(2, params["exp_cap"])
        big_a = pow(g, a, p)
        big_b = pow(g, b, p)
        shared = pow(big_b, a, p)
        return (
            f"DH: p={p}, g={g}, a={a}, b={b}",
            {"p": p, "g": g, "a": a, "b": b,
             "A": big_a, "B": big_b, "shared": shared},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Diffie-Hellman.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing A, B, and shared secret computation.
        """
        return [
            f"A = {data['g']}^{{{data['a']}}} mod {data['p']} = {data['A']}",
            f"B = {data['g']}^{{{data['b']}}} mod {data['p']} = {data['B']}",
            f"shared = {data['B']}^{{{data['a']}}} mod {data['p']} = {data['shared']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the shared secret.

        Args:
            data: Solution data dict.

        Returns:
            Shared secret as a string.
        """
        return str(data["shared"])


# ---------------------------------------------------------------------------
# 5. Elliptic Curve Point Addition
# ---------------------------------------------------------------------------

@register
class EllipticCurveAddGenerator(StepGenerator):
    """Point addition on an elliptic curve y^2 = x^3 + ax + b mod p.

    Given two points on the curve, compute the slope and the resulting
    sum point using modular arithmetic.

    Difficulty scaling:
        Difficulty 1-3: p < 30.
        Difficulty 4-6: p < 50.
        Difficulty 7-8: p < 100.

    Prerequisites:
        mod_inv.
    """

    _P_CAPS = {
        1: 30, 2: 30, 3: 30,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elliptic_curve_add"

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
        return "add two points on an elliptic curve"

    def _find_curve_and_points(self, p: int) -> tuple[int, int, int, int, int, int]:
        """Find curve parameters and two distinct points on the curve.

        Searches for y^2 = x^3 + ax + b mod p with valid points.

        Args:
            p: Prime modulus.

        Returns:
            Tuple (a, b, x1, y1, x2, y2).

        Raises:
            ValueError: If no suitable curve is found.
        """
        for _ in range(200):
            a_coeff = self._rng.randint(0, p - 1)
            b_coeff = self._rng.randint(1, p - 1)
            # Check discriminant: 4a^3 + 27b^2 != 0 mod p
            disc = (4 * pow(a_coeff, 3, p) + 27 * pow(b_coeff, 2, p)) % p
            if disc == 0:
                continue
            points: list[tuple[int, int]] = []
            for x in range(p):
                rhs = (pow(x, 3, p) + a_coeff * x + b_coeff) % p
                for y in range(p):
                    if (y * y) % p == rhs:
                        points.append((x, y))
                        if len(points) >= 10:
                            break
                if len(points) >= 10:
                    break
            if len(points) >= 2:
                # Pick two distinct points
                self._rng.shuffle(points)
                p1 = points[0]
                p2 = points[1]
                # Ensure we can compute slope (different x or same point for doubling)
                if p1[0] != p2[0]:
                    return a_coeff, b_coeff, p1[0], p1[1], p2[0], p2[1]
        raise ValueError("Could not find suitable curve and points")

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an elliptic curve point addition problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p_cap = self._P_CAPS.get(difficulty, 100)
        primes = [x for x in _SMALL_PRIMES if x >= 5 and x < p_cap]
        p = self._rng.choice(primes)
        a, b, x1, y1, x2, y2 = self._find_curve_and_points(p)

        # Compute addition: P1 + P2
        dx = (x2 - x1) % p
        dy = (y2 - y1) % p
        inv_dx = _mod_inverse(dx, p)
        slope = (dy * inv_dx) % p
        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p

        return (
            f"EC: y^2=x^3+{a}x+{b} mod {p}, P=({x1},{y1}), Q=({x2},{y2})",
            {"a": a, "b": b, "p": p,
             "x1": x1, "y1": y1, "x2": x2, "y2": y2,
             "slope": slope, "x3": x3, "y3": y3},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for EC point addition.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing slope, x3, and y3 computation.
        """
        p = data["p"]
        return [
            f"slope = ({data['y2']}-{data['y1']})"
            f"*({data['x2']}-{data['x1']})^{{-1}} mod {p} = {data['slope']}",
            f"x3 = {data['slope']}^2 - {data['x1']} - {data['x2']}"
            f" mod {p} = {data['x3']}",
            f"y3 = {data['slope']}*({data['x1']}-{data['x3']})"
            f" - {data['y1']} mod {p} = {data['y3']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the resulting point.

        Args:
            data: Solution data dict.

        Returns:
            Point (x3, y3) as a string.
        """
        return f"({data['x3']},{data['y3']})"


# ---------------------------------------------------------------------------
# 6. Hash Collision
# ---------------------------------------------------------------------------

@register
class HashCollisionGenerator(StepGenerator):
    """Find two inputs that collide under h(x) = x mod m.

    Given a hash function h(x) = x mod m and a target hash value,
    find two distinct inputs that produce the same hash.

    Difficulty scaling:
        Difficulty 1-3: m in [3, 10], inputs < 50.
        Difficulty 4-6: m in [7, 20], inputs < 100.
        Difficulty 7-8: m in [11, 30], inputs < 200.

    Prerequisites:
        modular.
    """

    _PARAMS = {
        1: {"m_lo": 3, "m_hi": 10, "cap": 50},
        2: {"m_lo": 3, "m_hi": 10, "cap": 50},
        3: {"m_lo": 3, "m_hi": 10, "cap": 50},
        4: {"m_lo": 7, "m_hi": 20, "cap": 100},
        5: {"m_lo": 7, "m_hi": 20, "cap": 100},
        6: {"m_lo": 7, "m_hi": 20, "cap": 100},
        7: {"m_lo": 11, "m_hi": 30, "cap": 200},
        8: {"m_lo": 11, "m_hi": 30, "cap": 200},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hash_collision"

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
        return "find two inputs with same hash"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hash collision problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        m = self._rng.randint(params["m_lo"], params["m_hi"])
        x1 = self._rng.randint(1, m - 1)
        # x2 is another value with the same hash: x2 = x1 + k*m
        k = self._rng.randint(1, max(1, (params["cap"] - x1) // m))
        x2 = x1 + k * m
        h = x1 % m
        return (
            f"h(x) = x mod {m}; find x1, x2 with h(x1)=h(x2)",
            {"m": m, "x1": x1, "x2": x2, "h": h},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for hash collision.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing both hash computations.
        """
        return [
            f"h({data['x1']}) = {data['x1']} mod {data['m']} = {data['h']}",
            f"h({data['x2']}) = {data['x2']} mod {data['m']} = {data['h']}",
            f"{data['x2']} - {data['x1']} = {data['x2'] - data['x1']}"
            f" = {(data['x2'] - data['x1']) // data['m']}*{data['m']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the colliding pair.

        Args:
            data: Solution data dict.

        Returns:
            Pair (x1, x2) as a string.
        """
        return f"x1={data['x1']}, x2={data['x2']}"


# ---------------------------------------------------------------------------
# 7. Digital Signature (RSA)
# ---------------------------------------------------------------------------

@register
class DigitalSignatureGenerator(StepGenerator):
    """RSA digital signature: sign and verify.

    Sign a message m by computing s = m^d mod n, then verify
    by checking s^e mod n == m.

    Difficulty scaling:
        Difficulty 1-3: p, q < 20.
        Difficulty 4-6: p, q < 50.
        Difficulty 7-8: p, q < 100.

    Prerequisites:
        rsa_keygen.
    """

    _PRIME_CAPS = {
        1: 20, 2: 20, 3: 20,
        4: 50, 5: 50, 6: 50,
        7: 100, 8: 100,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "digital_signature"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["rsa_keygen"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "sign and verify RSA digital signature"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a digital signature problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._PRIME_CAPS.get(difficulty, 100)
        pool = [p for p in _SMALL_PRIMES if 2 < p < cap]
        p = self._rng.choice(pool)
        q = self._rng.choice([x for x in pool if x != p])
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 3
        for candidate in [3, 5, 7, 11, 13, 17]:
            if candidate < phi and math.gcd(candidate, phi) == 1:
                e = candidate
                break
        d = _mod_inverse(e, phi)
        m = self._rng.randint(2, min(n - 1, cap - 1))
        s = pow(m, d, n)
        v = pow(s, e, n)  # Should equal m
        return (
            f"RSA sign: m={m}, d={d}, e={e}, n={n}",
            {"m": m, "d": d, "e": e, "n": n, "s": s, "v": v},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for digital signature.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing signing and verification.
        """
        return [
            f"sign: s = {data['m']}^{{{data['d']}}} mod {data['n']} = {data['s']}",
            f"verify: {data['s']}^{{{data['e']}}} mod {data['n']} = {data['v']}",
            f"valid: {data['v']} == {data['m']}: {data['v'] == data['m']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the signature and verification result.

        Args:
            data: Solution data dict.

        Returns:
            Signature value and validity as a string.
        """
        return f"s={data['s']}, valid=True"


# ---------------------------------------------------------------------------
# 8. One-Time Pad Encryption
# ---------------------------------------------------------------------------

@register
class OTPEncryptGenerator(StepGenerator):
    """One-time pad encryption via XOR.

    XOR each byte of the plaintext with the corresponding key byte
    to produce the ciphertext.

    Difficulty scaling:
        Difficulty 1-3: 2-4 bytes, values < 16.
        Difficulty 4-6: 4-6 bytes, values < 64.
        Difficulty 7-8: 6-8 bytes, values < 256.

    Prerequisites:
        binary_arithmetic.
    """

    _PARAMS = {
        1: {"len_lo": 2, "len_hi": 3, "val_cap": 16},
        2: {"len_lo": 2, "len_hi": 3, "val_cap": 16},
        3: {"len_lo": 3, "len_hi": 4, "val_cap": 16},
        4: {"len_lo": 4, "len_hi": 5, "val_cap": 64},
        5: {"len_lo": 4, "len_hi": 5, "val_cap": 64},
        6: {"len_lo": 5, "len_hi": 6, "val_cap": 64},
        7: {"len_lo": 6, "len_hi": 7, "val_cap": 256},
        8: {"len_lo": 7, "len_hi": 8, "val_cap": 256},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "otp_encrypt"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "encrypt plaintext with one-time pad XOR"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an OTP encryption problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAMS.get(difficulty, self._PARAMS[8])
        length = self._rng.randint(params["len_lo"], params["len_hi"])
        cap = params["val_cap"]
        plaintext = [self._rng.randint(0, cap - 1) for _ in range(length)]
        key = [self._rng.randint(0, cap - 1) for _ in range(length)]
        ciphertext = [p ^ k for p, k in zip(plaintext, key)]
        return (
            f"OTP: P={plaintext}, K={key}",
            {"plaintext": plaintext, "key": key, "ciphertext": ciphertext},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for OTP encryption.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each byte XOR operation.
        """
        steps: list[str] = []
        for i, (p, k, c) in enumerate(zip(
            data["plaintext"], data["key"], data["ciphertext"]
        )):
            steps.append(f"byte {i}: {p} XOR {k} = {c}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ciphertext.

        Args:
            data: Solution data dict.

        Returns:
            Ciphertext bytes as a string.
        """
        return str(data["ciphertext"])


# ---------------------------------------------------------------------------
# 9. Feistel Round
# ---------------------------------------------------------------------------

@register
class FeistelRoundGenerator(StepGenerator):
    """One round of a Feistel cipher.

    Compute L' = R and R' = L XOR f(R, K), where f(R, K) = (R + K) mod 256.

    Difficulty scaling:
        Difficulty 1-3: values < 16.
        Difficulty 4-6: values < 64.
        Difficulty 7-8: values < 256.

    Prerequisites:
        binary_arithmetic.
    """

    _CAPS = {
        1: 16, 2: 16, 3: 16,
        4: 64, 5: 64, 6: 64,
        7: 256, 8: 256,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "feistel_round"

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
        return "compute one Feistel cipher round"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Feistel round problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._CAPS.get(difficulty, 256)
        left = self._rng.randint(0, cap - 1)
        right = self._rng.randint(0, cap - 1)
        key = self._rng.randint(0, cap - 1)
        f_val = (right + key) % 256
        new_left = right
        new_right = left ^ f_val
        return (
            f"Feistel: L={left}, R={right}, K={key}",
            {"L": left, "R": right, "K": key,
             "f": f_val, "L_new": new_left, "R_new": new_right},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Feistel round.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing f computation and XOR.
        """
        return [
            f"f(R,K) = ({data['R']}+{data['K']}) mod 256 = {data['f']}",
            f"L' = R = {data['L_new']}",
            f"R' = L XOR f = {data['L']} XOR {data['f']} = {data['R_new']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the output half-blocks.

        Args:
            data: Solution data dict.

        Returns:
            New (L', R') as a string.
        """
        return f"L'={data['L_new']}, R'={data['R_new']}"


# ---------------------------------------------------------------------------
# 10. AES MixColumns
# ---------------------------------------------------------------------------

@register
class AESMixColumnGenerator(StepGenerator):
    """One AES MixColumns step in GF(2^8).

    Multiply a 4-byte column by the fixed AES MixColumns matrix
    in GF(2^8) with irreducible polynomial x^8+x^4+x^3+x+1.

    The fixed matrix is:
        [[2, 3, 1, 1],
         [1, 2, 3, 1],
         [1, 1, 2, 3],
         [3, 1, 1, 2]]

    Difficulty scaling:
        Difficulty 1-3: input bytes < 16.
        Difficulty 4-6: input bytes < 64.
        Difficulty 7-8: input bytes < 256.

    Prerequisites:
        polynomial_multiply.
    """

    _CAPS = {
        1: 16, 2: 16, 3: 16,
        4: 64, 5: 64, 6: 64,
        7: 256, 8: 256,
    }

    _MIX_MATRIX = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2],
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "aes_mixcolumn"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute AES MixColumns on a column"

    def _mix_column(self, col: list[int]) -> list[int]:
        """Apply the MixColumns transformation to a 4-byte column.

        Args:
            col: List of 4 input bytes.

        Returns:
            List of 4 output bytes after MixColumns.
        """
        result: list[int] = []
        for row in self._MIX_MATRIX:
            val = 0
            for j in range(4):
                val ^= _gf256_mul(row[j], col[j])
            result.append(val)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an AES MixColumns problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        cap = self._CAPS.get(difficulty, 256)
        col = [self._rng.randint(0, cap - 1) for _ in range(4)]
        output = self._mix_column(col)
        # Pre-compute intermediate GF products for steps
        products: list[list[int]] = []
        for row in self._MIX_MATRIX:
            row_products = [_gf256_mul(row[j], col[j]) for j in range(4)]
            products.append(row_products)
        return (
            f"MixColumns: [{col[0]:02x},{col[1]:02x},"
            f"{col[2]:02x},{col[3]:02x}]",
            {"col": col, "output": output, "products": products},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for AES MixColumns.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each output byte computation in GF(2^8).
        """
        steps: list[str] = []
        col = data["col"]
        for i, (row, prods) in enumerate(
            zip(self._MIX_MATRIX, data["products"])
        ):
            terms = " ^ ".join(
                f"{row[j]}*0x{col[j]:02x}=0x{prods[j]:02x}"
                for j in range(4)
            )
            steps.append(f"out[{i}]: {terms} = 0x{data['output'][i]:02x}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the MixColumns output.

        Args:
            data: Solution data dict.

        Returns:
            Output column in hex format.
        """
        out = data["output"]
        return f"[0x{out[0]:02x},0x{out[1]:02x},0x{out[2]:02x},0x{out[3]:02x}]"
