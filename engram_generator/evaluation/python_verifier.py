"""Python-based computational verification of reasoning steps.

Fallback evaluator for steps that fail string match and similarity.
Parses arithmetic expressions from steps and evaluates them in Python
to check mathematical correctness regardless of formatting.

Only runs on steps that failed levels 1 (exact match) and 2
(similarity), so the overhead is proportional to the number of
failures, not the total sample count.
"""
import re
import math


class PythonVerifier:
    """Verifies reasoning steps by evaluating arithmetic in Python.

    Parses expressions like "4+5=9", "48 mod 18=12", "3^4=81" and
    checks if the arithmetic is correct. Does NOT execute arbitrary
    code -- only evaluates parsed numeric expressions through a
    whitelist of safe operations.

    Example:
        >>> v = PythonVerifier()
        >>> v.verify_step("4+5=9")
        VerifyResult(valid=True, expected=9.0, computed=9.0)
        >>> v.verify_step("4+5=10")
        VerifyResult(valid=False, expected=10.0, computed=9.0)
    """

    _SAFE_NAMES = {
        "gcd": math.gcd,
        "abs": abs,
        "sqrt": math.sqrt,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    def verify_step(self, step: str) -> "VerifyResult":
        """Verify a single reasoning step computationally.

        Attempts to parse the step as an arithmetic expression
        with a result, then evaluates the expression in Python
        and compares against the stated result.

        Args:
            step: Raw step string (e.g. "4+5=9" or "48 mod 18=12").

        Returns:
            VerifyResult with verification outcome.
        """
        cleaned = step.strip()

        for parser in (
            self._parse_simple_arithmetic,
            self._parse_mod_expression,
            self._parse_div_with_remainder,
            self._parse_power_expression,
            self._parse_gcd_expression,
        ):
            result = parser(cleaned)
            if result is not None:
                return result

        return VerifyResult(
            valid=None,
            expected=None,
            computed=None,
            reason="unparseable",
        )

    def verify_chain(
        self,
        steps: list[str],
        only_failures: list[int] | None = None,
    ) -> list["VerifyResult"]:
        """Verify multiple steps, optionally only checking failures.

        Args:
            steps: List of step strings.
            only_failures: If provided, only verify steps at these
                indices. Steps not in the list get a skipped result.

        Returns:
            List of VerifyResult, one per step.
        """
        results = []
        for i, step in enumerate(steps):
            if only_failures is not None and i not in only_failures:
                results.append(VerifyResult(
                    valid=None, expected=None, computed=None,
                    reason="skipped",
                ))
            else:
                results.append(self.verify_step(step))
        return results

    def _parse_simple_arithmetic(self, text: str) -> "VerifyResult | None":
        """Parse simple arithmetic: 4+5=9, 3*9=27, 10-3=7.

        Args:
            text: Cleaned step string.

        Returns:
            VerifyResult or None if not parseable.
        """
        match = re.match(
            r'^([\d\.\+\-\*/\(\)]+)\s*=\s*([\-\d\.]+)$', text,
        )
        if not match:
            return None

        expr = match.group(1)
        stated = match.group(2)

        try:
            computed = self._safe_eval(expr)
            expected = float(stated)
            valid = abs(computed - expected) < 1e-9
            return VerifyResult(
                valid=valid, expected=expected, computed=computed,
            )
        except (ValueError, SyntaxError, ZeroDivisionError):
            return None

    def _parse_mod_expression(self, text: str) -> "VerifyResult | None":
        """Parse modular arithmetic: 48 mod 18=12, 381 mod 125=6.

        Handles both "mod" and "\\mod" notation.

        Args:
            text: Cleaned step string.

        Returns:
            VerifyResult or None if not parseable.
        """
        match = re.match(
            r'^(\d+)\s*\\?mod\s*(\d+)\s*=\s*([\-\d]+)$', text,
        )
        if not match:
            return None

        a = int(match.group(1))
        b = int(match.group(2))
        stated = int(match.group(3))
        computed = a % b
        return VerifyResult(
            valid=computed == stated,
            expected=float(stated),
            computed=float(computed),
        )

    def _parse_div_with_remainder(self, text: str) -> "VerifyResult | None":
        """Parse division with remainder: 52/13=4r0, 267/214=1r53.

        Args:
            text: Cleaned step string.

        Returns:
            VerifyResult or None if not parseable.
        """
        match = re.match(
            r'^(\d+)\s*/\s*(\d+)\s*=\s*(\d+)r(\d+)$', text,
        )
        if not match:
            return None

        a = int(match.group(1))
        b = int(match.group(2))
        quotient = int(match.group(3))
        remainder = int(match.group(4))

        computed_q = a // b
        computed_r = a % b
        valid = computed_q == quotient and computed_r == remainder
        return VerifyResult(
            valid=valid,
            expected=float(quotient),
            computed=float(computed_q),
            reason=f"remainder: stated={remainder}, computed={computed_r}"
            if computed_r != remainder else None,
        )

    def _parse_power_expression(self, text: str) -> "VerifyResult | None":
        """Parse exponentiation: 2^4=16, 3^3=27.

        Args:
            text: Cleaned step string.

        Returns:
            VerifyResult or None if not parseable.
        """
        match = re.match(
            r'^(\d+)\s*\^\s*(\{?\d+\}?)\s*=\s*([\-\d\.]+)$', text,
        )
        if not match:
            return None

        base = int(match.group(1))
        exp = int(match.group(2).strip("{}"))
        stated = float(match.group(3))
        computed = float(base ** exp)
        return VerifyResult(
            valid=abs(computed - stated) < 1e-9,
            expected=stated,
            computed=computed,
        )

    def _parse_gcd_expression(self, text: str) -> "VerifyResult | None":
        """Parse GCD: gcd(48,18)=6, \\gcd(216739,126225)=1.

        Args:
            text: Cleaned step string.

        Returns:
            VerifyResult or None if not parseable.
        """
        match = re.match(
            r'^\\?gcd\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*=\s*(\d+)$',
            text,
        )
        if not match:
            return None

        a = int(match.group(1))
        b = int(match.group(2))
        stated = int(match.group(3))
        computed = math.gcd(a, b)
        return VerifyResult(
            valid=computed == stated,
            expected=float(stated),
            computed=float(computed),
        )

    @staticmethod
    def _safe_eval(expr: str) -> float:
        """Evaluate a simple arithmetic expression safely.

        Only allows digits, operators (+, -, *, /), parentheses,
        and decimal points. No function calls, no variable access.

        Args:
            expr: Arithmetic expression string.

        Returns:
            Numeric result.

        Raises:
            ValueError: If expression contains unsafe characters.
            SyntaxError: If expression is malformed.
        """
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            raise ValueError(f"Unsafe characters in expression: {expr}")
        return float(eval(expr, {"__builtins__": {}}, {}))


class VerifyResult:
    """Result of computational verification for one step.

    Attributes:
        valid: True if computation matches, False if wrong,
            None if step was unparseable or skipped.
        expected: The value stated in the step.
        computed: The value computed by Python.
        reason: Explanation for failures or skips.
    """

    def __init__(
        self,
        valid: bool | None,
        expected: float | None,
        computed: float | None,
        reason: str | None = None,
    ):
        """Initialise the verification result.

        Args:
            valid: Whether the step is computationally correct.
            expected: Stated value.
            computed: Python-computed value.
            reason: Optional explanation.
        """
        self.valid = valid
        self.expected = expected
        self.computed = computed
        self.reason = reason

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"VerifyResult(valid={self.valid}, "
            f"expected={self.expected}, computed={self.computed})"
        )
