"""Tests for the Python verification fallback."""
import pytest

from engram_generator.evaluation.python_verifier import PythonVerifier, VerifyResult


class TestSimpleArithmetic:
    """Tests for basic arithmetic verification."""

    def setup_method(self):
        """Create a verifier for each test."""
        self.v = PythonVerifier()

    def test_addition_correct(self):
        """Correct addition is valid."""
        r = self.v.verify_step("4+5=9")
        assert r.valid is True

    def test_addition_wrong(self):
        """Wrong addition result is invalid."""
        r = self.v.verify_step("4+5=10")
        assert r.valid is False
        assert r.computed == 9.0

    def test_subtraction_correct(self):
        """Correct subtraction is valid."""
        r = self.v.verify_step("10-3=7")
        assert r.valid is True

    def test_multiplication_correct(self):
        """Correct multiplication is valid."""
        r = self.v.verify_step("3*9=27")
        assert r.valid is True

    def test_multiplication_wrong(self):
        """Wrong multiplication is invalid."""
        r = self.v.verify_step("3*9=28")
        assert r.valid is False

    def test_division_correct(self):
        """Correct division is valid."""
        r = self.v.verify_step("10/2=5")
        assert r.valid is True

    def test_multi_operand(self):
        """Multi-operand expressions work."""
        r = self.v.verify_step("1+2+1=4")
        assert r.valid is True

    def test_parentheses(self):
        """Parenthesised expressions work."""
        r = self.v.verify_step("(3+4)*2=14")
        assert r.valid is True

    def test_negative_result(self):
        """Negative results work."""
        r = self.v.verify_step("3-10=-7")
        assert r.valid is True

    def test_decimal_result(self):
        """Decimal results work."""
        r = self.v.verify_step("7/2=3.5")
        assert r.valid is True


class TestModExpression:
    """Tests for modular arithmetic verification."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_mod_correct(self):
        """Correct mod expression is valid."""
        r = self.v.verify_step("48 mod 18=12")
        assert r.valid is True

    def test_mod_latex_correct(self):
        """Correct LaTeX mod expression is valid."""
        r = self.v.verify_step("48 \\mod 18=12")
        assert r.valid is True

    def test_mod_wrong(self):
        """Wrong mod result is invalid."""
        r = self.v.verify_step("48 mod 18=13")
        assert r.valid is False
        assert r.computed == 12.0

    def test_large_mod(self):
        """Large modular arithmetic works."""
        r = self.v.verify_step("216739 \\mod 13114=6915")
        assert r.valid is True


class TestDivWithRemainder:
    """Tests for division with remainder verification."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_div_correct(self):
        """Correct division with remainder is valid."""
        r = self.v.verify_step("52/13=4r0")
        assert r.valid is True

    def test_div_with_remainder(self):
        """Division with non-zero remainder works."""
        r = self.v.verify_step("267/214=1r53")
        assert r.valid is True

    def test_div_wrong_quotient(self):
        """Wrong quotient is invalid."""
        r = self.v.verify_step("52/13=3r0")
        assert r.valid is False

    def test_div_wrong_remainder(self):
        """Wrong remainder is invalid."""
        r = self.v.verify_step("267/214=1r54")
        assert r.valid is False


class TestPowerExpression:
    """Tests for exponentiation verification."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_power_correct(self):
        """Correct exponentiation is valid."""
        r = self.v.verify_step("2^4=16")
        assert r.valid is True

    def test_power_braces(self):
        """Exponent with braces works."""
        r = self.v.verify_step("2^{4}=16")
        assert r.valid is True

    def test_power_wrong(self):
        """Wrong exponentiation is invalid."""
        r = self.v.verify_step("2^4=15")
        assert r.valid is False

    def test_large_power(self):
        """Large exponentiation works."""
        r = self.v.verify_step("3^5=243")
        assert r.valid is True


class TestGCDExpression:
    """Tests for GCD verification."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_gcd_correct(self):
        """Correct GCD is valid."""
        r = self.v.verify_step("gcd(48,18)=6")
        assert r.valid is True

    def test_gcd_latex_correct(self):
        """Correct LaTeX GCD is valid."""
        r = self.v.verify_step("\\gcd(48,18)=6")
        assert r.valid is True

    def test_gcd_wrong(self):
        """Wrong GCD result is invalid."""
        r = self.v.verify_step("gcd(48,18)=9")
        assert r.valid is False
        assert r.computed == 6.0

    def test_gcd_large(self):
        """Large GCD works."""
        r = self.v.verify_step("\\gcd(216739,126225)=1")
        assert r.valid is True


class TestUnparseable:
    """Tests for steps that can't be verified computationally."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_text_step(self):
        """Non-arithmetic step returns unparseable."""
        r = self.v.verify_step("visit 0")
        assert r.valid is None
        assert r.reason == "unparseable"

    def test_variable_assignment(self):
        """Variable assignment returns unparseable."""
        r = self.v.verify_step("n = 3*5 = 15")
        assert r.valid is None

    def test_latex_formula(self):
        """LaTeX formula returns unparseable."""
        r = self.v.verify_step("s = v_0 t + \\frac{1}{2}at^2")
        assert r.valid is None

    def test_empty_string(self):
        """Empty string returns unparseable."""
        r = self.v.verify_step("")
        assert r.valid is None


class TestSafety:
    """Tests for safe evaluation."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_no_builtins(self):
        """Cannot access builtins."""
        r = self.v.verify_step("__import__('os').system('ls')=0")
        assert r.valid is None

    def test_no_functions(self):
        """Cannot call arbitrary functions."""
        r = self.v.verify_step("open('/etc/passwd')=0")
        assert r.valid is None


class TestVerifyChain:
    """Tests for chain verification."""

    def setup_method(self):
        self.v = PythonVerifier()

    def test_full_chain(self):
        """Verify all steps in a chain."""
        results = self.v.verify_chain([
            "4+5=9", "1+2=3", "2+1=3",
        ])
        assert len(results) == 3
        assert all(r.valid is True for r in results)

    def test_only_failures(self):
        """Only verify specified failure indices."""
        results = self.v.verify_chain(
            ["4+5=9", "1+2=4", "2+1=3"],
            only_failures=[1],
        )
        assert results[0].reason == "skipped"
        assert results[1].valid is False
        assert results[2].reason == "skipped"

    def test_mixed_chain(self):
        """Chain with mixed parseable and unparseable steps."""
        results = self.v.verify_chain([
            "4+5=9",
            "visit node 3",
            "2+1=3",
        ])
        assert results[0].valid is True
        assert results[1].valid is None
        assert results[2].valid is True
