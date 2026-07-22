"""Step-level normalisation for reasoning chain comparison.

Handles commutativity (3*9=27 matches 9*3=27), numeric equivalence
(125.0 matches 125), whitespace, and common formatting variations.
"""
import re


class OperationNormaliser:
    """Normalises arithmetic steps for comparison.

    Commutative operators (+, *) get sorted operands.
    Non-commutative operators (-, /, div, mod) stay ordered.
    Numeric values are canonicalised (floats to ints where exact).

    Example:
        >>> n = OperationNormaliser()
        >>> n.normalise("9*3=27")
        '3*9=27'
        >>> n.normalise("2+1+1=4")
        '1+1+2=4'
        >>> n.normalise("125.0")
        '125'
        >>> n.normalise("48 \\\\mod 18=12")
        '48\\\\mod18=12'
    """

    COMMUTATIVE_OPS = {'+', '*'}

    def normalise(self, text: str) -> str:
        """Normalise a single step string for comparison.

        Args:
            text: Raw step string (e.g. "3*9=27" or "125.0").

        Returns:
            Canonical form for comparison.
        """
        cleaned = text.strip().lower().replace(" ", "").replace(",", "")

        if not cleaned:
            return cleaned

        numeric = self._try_numeric(cleaned)
        if numeric is not None:
            return numeric

        expr = self._try_expression(cleaned)
        if expr is not None:
            return expr

        return cleaned

    def normalise_chain(self, steps: list[str]) -> list[str]:
        """Normalise a list of step strings.

        Args:
            steps: List of raw step strings.

        Returns:
            List of normalised step strings.
        """
        return [self.normalise(s) for s in steps]

    def steps_match(self, expected: str, predicted: str) -> bool:
        """Check if two steps are semantically equivalent.

        Args:
            expected: Ground truth step.
            predicted: Model output step.

        Returns:
            True if the steps are equivalent after normalisation.
        """
        return self.normalise(expected) == self.normalise(predicted)

    def _try_numeric(self, text: str) -> str | None:
        """Try to parse as a pure numeric value.

        Converts floats that are exact integers to int strings.

        Args:
            text: Cleaned string.

        Returns:
            Canonical numeric string, or None if not a number.
        """
        try:
            value = float(text)
            if value == int(value) and 'e' not in text:
                return str(int(value))
            return text
        except ValueError:
            return None

    def _try_expression(self, text: str) -> str | None:
        """Try to parse as an expression with operator and result.

        Sorts operands for commutative operators.

        Args:
            text: Cleaned string.

        Returns:
            Canonical expression string, or None if not parseable.
        """
        eq_match = re.match(r'^(.+)=([^=]+)$', text)
        if not eq_match:
            return None

        lhs = eq_match.group(1)
        result = eq_match.group(2)

        for op in ('*', '+'):
            if op in lhs and not self._has_mixed_ops(lhs, op):
                operands = lhs.split(op)
                sorted_ops = sorted(operands)
                return op.join(sorted_ops) + '=' + result

        return None

    @staticmethod
    def _has_mixed_ops(lhs: str, target_op: str) -> bool:
        """Check if the LHS contains operators other than the target.

        Prevents sorting operands in mixed expressions like "3+4*2".

        Args:
            lhs: Left-hand side of the expression.
            target_op: The operator we're checking for purity.

        Returns:
            True if other operators are present.
        """
        other_ops = {'+', '-', '*', '/'} - {target_op}
        return any(op in lhs for op in other_ops)
