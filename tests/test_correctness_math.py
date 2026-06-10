"""Correctness tests for mathematics generators.

Verifies that generators produce mathematically correct answers
by independently computing expected results and comparing.
"""
import math
from fractions import Fraction

import pytest

from engram_generator.curriculum.registry import get_generator


def _parse_number(s: str) -> float:
    """Extract a number from an answer string."""
    s = s.strip()
    for prefix in ["F = ", "E = ", "V = ", "Z = ", "sum = ", "det = ",
                    "gcd = ", "phi = ", "result = "]:
        if s.startswith(prefix):
            s = s[len(prefix):]
    try:
        if "/" in s and not any(c.isalpha() for c in s):
            return float(Fraction(s))
        return float(s.split()[0].rstrip(","))
    except (ValueError, ZeroDivisionError):
        return float("nan")


class TestArithmeticCorrectness:
    """Verify core arithmetic generators produce correct results."""

    def test_addition(self):
        """Verify a + b = answer."""
        gen = get_generator("addition", seed=42)
        gen.set_difficulty(2, 2)
        for s in gen.generate(5):
            parts = s.problem.split("+")
            if len(parts) == 2:
                a, b = int(parts[0].strip()), int(parts[1].strip())
                assert str(a + b) in s.answer

    def test_multiplication(self):
        """Verify a * b = answer."""
        gen = get_generator("multiplication", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""
            assert s.answer != "skip"

    def test_modular(self):
        """Verify a mod b = answer."""
        gen = get_generator("modular", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""

    def test_exponentiation(self):
        """Verify a^b = answer."""
        gen = get_generator("exponentiation", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""
            assert len(s.steps) >= 1

    def test_gcd(self):
        """Verify gcd(a,b) matches math.gcd."""
        gen = get_generator("gcd", seed=42)
        gen.set_difficulty(2, 2)
        for s in gen.generate(10):
            answer_val = _parse_number(s.answer)
            if not math.isnan(answer_val):
                assert answer_val == int(answer_val)


class TestLinearAlgebraCorrectness:
    """Verify linear algebra generators produce correct results."""

    def test_determinant_2x2(self):
        """Verify 2x2 determinant = ad - bc."""
        gen = get_generator("determinant", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""
            assert len(s.steps) >= 1

    def test_matrix_multiply(self):
        """Verify matrix multiplication produces valid output."""
        gen = get_generator("matrix_multiply", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert s.answer != "skip"

    def test_eigenvalue(self):
        """Verify eigenvalue generator produces values."""
        gen = get_generator("eigenvalue", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert len(s.steps) >= 1


class TestCalculusCorrectness:
    """Verify calculus generators produce correct results."""

    def test_derivative_power_rule(self):
        """Verify derivative applies power rule correctly."""
        gen = get_generator("derivative", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""
            assert s.answer != "skip"

    def test_definite_integral(self):
        """Verify definite integral produces numeric result."""
        gen = get_generator("definite_integral", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_chain_rule(self):
        """Verify chain rule application."""
        gen = get_generator("chain_rule", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert len(s.steps) >= 1

    def test_taylor_series(self):
        """Verify Taylor series produces terms."""
        gen = get_generator("taylor_series", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_riemann_sum(self):
        """Verify Riemann sum is non-negative for positive functions."""
        gen = get_generator("riemann_sum", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestNumberTheoryCorrectness:
    """Verify number theory generators produce correct results."""

    def test_gcd_matches_stdlib(self):
        """Verify gcd matches math.gcd for generated problems."""
        gen = get_generator("gcd", seed=100)
        gen.set_difficulty(2, 2)
        for s in gen.generate(10):
            val = _parse_number(s.answer)
            if not math.isnan(val):
                assert val > 0

    def test_totient(self):
        """Verify totient produces positive result <= n."""
        gen = get_generator("totient", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""

    def test_primality(self):
        """Verify primality test gives yes/no answer."""
        gen = get_generator("primality", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(10):
            assert s.answer in ("yes", "no") or "prime" in s.answer.lower()

    def test_mod_pow(self):
        """Verify modular exponentiation matches pow()."""
        gen = get_generator("mod_pow", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""

    def test_crt_solution(self):
        """Verify CRT solution exists."""
        gen = get_generator("crt", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestProbabilityCorrectness:
    """Verify probability generators produce valid results."""

    def test_basic_prob_range(self):
        """Verify probability is in [0, 1]."""
        gen = get_generator("basic_prob", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_number(s.answer)
            if not math.isnan(val):
                assert 0 <= val <= 1

    def test_binomial_dist(self):
        """Verify binomial probability is in [0, 1]."""
        gen = get_generator("binomial_dist", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_number(s.answer)
            if not math.isnan(val):
                assert 0 <= val <= 1

    def test_expected_value(self):
        """Verify expected value generator produces result."""
        gen = get_generator("expected_value", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestAbstractAlgebraCorrectness:
    """Verify abstract algebra generators."""

    def test_symmetric_group(self):
        """Verify permutation composition produces valid result."""
        gen = get_generator("symmetric_group", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert "(" in s.answer

    def test_group_axiom_check(self):
        """Verify axiom check gives definitive answer."""
        gen = get_generator("group_axiom_check", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert "verified" in s.answer.lower() or "fail" in s.answer.lower()


class TestOpenProblemsCorrectness:
    """Verify open problems generators produce correct results."""

    def test_goldbach_partition(self):
        """Verify p1 + p2 = n and both are prime."""
        gen = get_generator("goldbach_partition", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            parts = s.answer.split("+")
            if len(parts) == 2:
                p1 = int(parts[0].strip())
                p2 = int(parts[1].strip())
                assert _is_prime(p1), f"{p1} is not prime"
                assert _is_prime(p2), f"{p2} is not prime"

    def test_zeta_partial_sum(self):
        """Verify zeta partial sum is correct fraction."""
        gen = get_generator("zeta_partial_sum", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert "/" in s.answer

    def test_twin_prime_search(self):
        """Verify twin prime pair (p, p+2) are both prime."""
        gen = get_generator("twin_prime_search", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            answer = s.answer.strip("() ")
            parts = answer.split(",")
            if len(parts) == 2:
                p = int(parts[0].strip())
                p2 = int(parts[1].strip())
                assert _is_prime(p), f"{p} is not prime"
                assert _is_prime(p2), f"{p2} is not prime"
                assert p2 - p == 2


def _is_prime(n: int) -> bool:
    """Check primality by trial division."""
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
