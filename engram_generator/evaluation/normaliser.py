"""Step-level normalisation for reasoning chain comparison.

Handles commutativity (3*9=27 matches 9*3=27), numeric equivalence
(125.0 matches 125), whitespace, and common formatting variations.

Only applies commutativity sorting to simple numeric expressions.
Complex expressions (assignments, function calls, LaTeX) are left
as-is to prevent incorrect reordering.
"""
import math
import re


class OperationNormaliser:
    """Normalises arithmetic steps for comparison.

    Commutative operators (+, *) get sorted operands, but ONLY
    for simple numeric expressions (e.g. "3*9=27"). Expressions
    with variables, function calls, parentheses, or chained
    equalities are left ordered.

    Example:
        >>> n = OperationNormaliser()
        >>> n.normalise("9*3=27")
        '3*9=27'
        >>> n.normalise("n = 3*5 = 15")
        'n=3*5=15'
        >>> n.normalise("f'(0.667) = 2*B_t = 1.334")
        "f'(0.667)=2*b_t=1.334"
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
            if not math.isfinite(value):
                return text
            if value == int(value) and 'e' not in text:
                return str(int(value))
            return text
        except (ValueError, OverflowError):
            return None

    def _try_expression(self, text: str) -> str | None:
        """Try to parse as a simple arithmetic expression and sort operands.

        Only sorts operands for simple numeric expressions like
        "3*9=27" or "2+1+1=4". Rejects expressions with variables,
        function calls, parentheses, LaTeX, or chained equalities.

        Args:
            text: Cleaned string.

        Returns:
            Canonical expression string, or None if not sortable.
        """
        eq_match = re.match(r'^(.+)=([^=]+)$', text)
        if not eq_match:
            return None

        lhs = eq_match.group(1)
        result = eq_match.group(2)

        if not self._is_simple_numeric(lhs):
            return None

        for op in ('*', '+'):
            if op in lhs and not self._has_mixed_ops(lhs, op):
                operands = lhs.split(op)
                sorted_ops = sorted(operands)
                return op.join(sorted_ops) + '=' + result

        return None

    @staticmethod
    def _is_simple_numeric(lhs: str) -> bool:
        """Check if the LHS contains only digits and arithmetic operators.

        Returns False for variables, function calls, parentheses,
        LaTeX commands, or anything that isn't pure digit arithmetic.
        Allows 'r' for remainder notation (e.g. "0r5").

        Args:
            lhs: Left-hand side of the expression.

        Returns:
            True if safe to sort operands.
        """
        if '(' in lhs or ')' in lhs:
            return False
        if '\\' in lhs:
            return False
        allowed = set('0123456789+-*/r.')
        return all(c in allowed for c in lhs)

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

    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        """Compute Levenshtein edit distance between two strings.

        Args:
            a: First string.
            b: Second string.

        Returns:
            Minimum number of single-character edits.
        """
        if len(a) < len(b):
            return OperationNormaliser.levenshtein(b, a)
        if not b:
            return len(a)
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a):
            curr = [i + 1]
            for j, cb in enumerate(b):
                cost = 0 if ca == cb else 1
                curr.append(min(
                    curr[j] + 1,
                    prev[j + 1] + 1,
                    prev[j] + cost,
                ))
            prev = curr
        return prev[-1]

    def step_similarity(self, a: str, b: str) -> float:
        """Compute normalised similarity between two steps.

        Returns 1.0 for exact match, 0.0 for completely different.
        Based on Levenshtein distance over the longer string.

        Args:
            a: First step string.
            b: Second step string.

        Returns:
            Similarity score in [0.0, 1.0].
        """
        na = self.normalise(a)
        nb = self.normalise(b)
        if na == nb:
            return 1.0
        max_len = max(len(na), len(nb))
        if max_len == 0:
            return 1.0
        dist = self.levenshtein(na, nb)
        return 1.0 - (dist / max_len)

    @staticmethod
    def rouge_l(expected: list[str], predicted: list[str]) -> float:
        """Compute ROUGE-L F1 score between two step sequences.

        Uses longest common subsequence (LCS) over step lists,
        not characters. Measures structural overlap of reasoning
        chains even when steps are reordered or missing.

        Args:
            expected: Ground truth step list.
            predicted: Predicted step list.

        Returns:
            ROUGE-L F1 score in [0.0, 1.0].
        """
        if not expected or not predicted:
            return 0.0

        m = len(expected)
        n = len(predicted)
        table = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if expected[i - 1] == predicted[j - 1]:
                    table[i][j] = table[i - 1][j - 1] + 1
                else:
                    table[i][j] = max(table[i - 1][j], table[i][j - 1])

        lcs_len = table[m][n]
        precision = lcs_len / n
        recall = lcs_len / m
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)
