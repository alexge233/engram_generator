"""Extended information theory task generators.

6 generators across tiers 5-6 covering conditional entropy,
data processing inequality, rate-distortion, typical sets,
Kraft-McMillan inequality, and joint entropy.
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


def _entropy_from_dist(dist: list[float]) -> float:
    """Compute Shannon entropy of a probability distribution.

    Args:
        dist: List of probabilities summing to 1.

    Returns:
        H(X) = -sum p_i * log2(p_i).
    """
    h = 0.0
    for p in dist:
        if p > 0.0:
            h -= p * math.log2(p)
    return h


# ---------------------------------------------------------------------------
# 1. Conditional Entropy (tier 5)
# ---------------------------------------------------------------------------

@register
class ConditionalEntropyGenerator(StepGenerator):
    """Compute conditional entropy H(X|Y) from a joint distribution.

    H(X|Y) = H(X,Y) - H(Y), or equivalently H(X|Y) = sum P(y)*H(X|Y=y).
    Given a small joint probability table, compute the conditional entropy.

    Difficulty scaling:
        Difficulty 1-3: 2x2 joint distribution, simple fractions.
        Difficulty 4-6: 2x3 or 3x2 distribution.
        Difficulty 7-8: 3x3 distribution.

    Prerequisites:
        info_entropy.
    """

    _SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 2),
        4: (2, 3), 5: (3, 2), 6: (2, 3),
        7: (3, 3), 8: (3, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conditional_entropy"

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
        return "compute conditional entropy H(X|Y) from joint distribution"

    def _generate_joint(self, rows: int, cols: int) -> list[list[float]]:
        """Generate a valid joint probability distribution.

        Args:
            rows: Number of X values.
            cols: Number of Y values.

        Returns:
            2D list of probabilities summing to 1.
        """
        raw = [[self._rng.randint(1, 10) for _ in range(cols)] for _ in range(rows)]
        total = sum(sum(row) for row in raw)
        joint = [[round(v / total, 4) for v in row] for row in raw]
        # Fix rounding: adjust last cell
        current_sum = sum(sum(row) for row in joint) - joint[-1][-1]
        joint[-1][-1] = round(1.0 - current_sum, 4)
        return joint

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conditional entropy problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rows, cols = self._SIZES.get(difficulty, (3, 3))
        joint = self._generate_joint(rows, cols)

        # H(X,Y) = -sum sum P(x,y) log2 P(x,y)
        h_xy = 0.0
        for row in joint:
            for p in row:
                if p > 0:
                    h_xy -= p * math.log2(p)
        h_xy = round(h_xy, 4)

        # P(Y) marginal
        p_y = [round(sum(joint[i][j] for i in range(rows)), 4) for j in range(cols)]

        # H(Y) = -sum P(y) log2 P(y)
        h_y = 0.0
        for p in p_y:
            if p > 0:
                h_y -= p * math.log2(p)
        h_y = round(h_y, 4)

        # H(X|Y) = H(X,Y) - H(Y)
        h_x_given_y = round(h_xy - h_y, 4)

        # Format joint table
        table_str = "; ".join(
            "[" + ", ".join(str(v) for v in row) + "]"
            for row in joint
        )

        return (
            f"P(X,Y) = [{table_str}], compute H(X|Y)",
            {"joint": joint, "rows": rows, "cols": cols,
             "p_y": p_y, "h_xy": h_xy, "h_y": h_y,
             "h_x_given_y": h_x_given_y},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for conditional entropy.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing H(X,Y), H(Y), and H(X|Y) computation.
        """
        return [
            f"P(Y) marginals: {data['p_y']}",
            f"H(X,Y) = {data['h_xy']}",
            f"H(Y) = {data['h_y']}",
            f"H(X|Y) = H(X,Y) - H(Y) = {data['h_xy']} - {data['h_y']} = {data['h_x_given_y']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conditional entropy.

        Args:
            data: Solution data dict.

        Returns:
            H(X|Y) as a string.
        """
        return f"H(X|Y) = {data['h_x_given_y']}"


# ---------------------------------------------------------------------------
# 2. Data Processing Inequality (tier 6)
# ---------------------------------------------------------------------------

@register
class DataProcessingInequalityGenerator(StepGenerator):
    """Verify the data processing inequality on a Markov chain.

    If X -> Y -> Z forms a Markov chain, then I(X;Z) <= I(X;Y).
    Given small joint distributions for (X,Y) and transition Y->Z,
    compute both mutual informations and verify the inequality.

    Difficulty scaling:
        Difficulty 1-3: 2x2 distributions.
        Difficulty 4-6: 2x3 distributions.
        Difficulty 7-8: 3x3 distributions.

    Prerequisites:
        mutual_information.
    """

    _SIZES = {
        1: 2, 2: 2, 3: 2,
        4: 2, 5: 3, 6: 3,
        7: 3, 8: 3,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "data_processing_inequality"

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
        return "verify data processing inequality I(X;Z) <= I(X;Y)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a data processing inequality problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._SIZES.get(difficulty, 3)

        # Generate P(X,Y) joint
        raw_xy = [[self._rng.randint(1, 10) for _ in range(n)] for _ in range(n)]
        total_xy = sum(sum(row) for row in raw_xy)
        p_xy = [[round(v / total_xy, 4) for v in row] for row in raw_xy]
        s = sum(sum(row) for row in p_xy) - p_xy[-1][-1]
        p_xy[-1][-1] = round(1.0 - s, 4)

        # Marginals
        p_x = [round(sum(p_xy[i][j] for j in range(n)), 4) for i in range(n)]
        p_y = [round(sum(p_xy[i][j] for i in range(n)), 4) for j in range(n)]

        # I(X;Y) = H(X) + H(Y) - H(X,Y)
        h_x = round(_entropy_from_dist(p_x), 4)
        h_y = round(_entropy_from_dist(p_y), 4)
        h_xy = 0.0
        for row in p_xy:
            for p in row:
                if p > 0:
                    h_xy -= p * math.log2(p)
        h_xy = round(h_xy, 4)
        i_xy = round(h_x + h_y - h_xy, 4)

        # Generate noisy channel Y -> Z (adds noise, reducing info)
        # P(Z|Y) is a noisy identity
        noise = round(self._rng.uniform(0.1, 0.4), 2)
        p_z_given_y = []
        for i in range(n):
            row = [round(noise / (n - 1), 4)] * n
            row[i] = round(1.0 - noise, 4)
            p_z_given_y.append(row)

        # P(X,Z) = sum_y P(X,Y=y) * P(Z|Y=y)
        p_xz = [[0.0] * n for _ in range(n)]
        for xi in range(n):
            for zi in range(n):
                val = 0.0
                for yi in range(n):
                    val += p_xy[xi][yi] * p_z_given_y[yi][zi]
                p_xz[xi][zi] = round(val, 4)

        # Marginals for Z
        p_z = [round(sum(p_xz[i][j] for i in range(n)), 4) for j in range(n)]

        # I(X;Z)
        h_z = round(_entropy_from_dist(p_z), 4)
        h_xz = 0.0
        for row in p_xz:
            for p in row:
                if p > 0:
                    h_xz -= p * math.log2(p)
        h_xz = round(h_xz, 4)
        i_xz = round(h_x + h_z - h_xz, 4)

        holds = i_xz <= i_xy + 0.0001  # small tolerance

        return (
            f"Markov X->Y->Z, noise={noise}",
            {"n": n, "p_xy": p_xy, "p_x": p_x, "p_y": p_y,
             "p_z_given_y": p_z_given_y, "p_xz": p_xz, "p_z": p_z,
             "h_x": h_x, "h_y": h_y, "h_z": h_z,
             "i_xy": i_xy, "i_xz": i_xz, "holds": holds, "noise": noise},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for data processing inequality.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing I(X;Y) and I(X;Z) comparison.
        """
        return [
            f"H(X)={data['h_x']}, H(Y)={data['h_y']}, H(Z)={data['h_z']}",
            f"I(X;Y) = {data['i_xy']}",
            f"noisy channel Y->Z with noise={data['noise']}",
            f"I(X;Z) = {data['i_xz']}",
            f"I(X;Z)={data['i_xz']} <= I(X;Y)={data['i_xy']}: {data['holds']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the inequality verification.

        Args:
            data: Solution data dict.

        Returns:
            Both mutual informations and result as a string.
        """
        return f"I(X;Y)={data['i_xy']}, I(X;Z)={data['i_xz']}, DPI holds={data['holds']}"


# ---------------------------------------------------------------------------
# 3. Rate-Distortion (tier 6)
# ---------------------------------------------------------------------------

@register
class RateDistortionGenerator(StepGenerator):
    """Compute rate-distortion function for a binary source.

    For binary source with P(X=1)=p under Hamming distortion:
    R(D) = H(p) - H(D) for 0 <= D <= min(p, 1-p), else R(D) = 0.

    Difficulty scaling:
        Difficulty 1-3: p = 0.5 (symmetric), D simple fractions.
        Difficulty 4-6: p varies, D = 0.01 to 0.2.
        Difficulty 7-8: fine-grained p and D values.

    Prerequisites:
        info_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rate_distortion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute rate-distortion R(D) for binary source"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rate-distortion problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            p = 0.5
            d = self._rng.choice([0.05, 0.1, 0.15, 0.2])
        elif difficulty <= 6:
            p = round(self._rng.uniform(0.2, 0.8), 2)
            d = round(self._rng.uniform(0.01, 0.2), 2)
        else:
            p = round(self._rng.uniform(0.1, 0.9), 3)
            d = round(self._rng.uniform(0.01, 0.15), 3)

        d_max = min(p, 1.0 - p)
        h_p = round(_binary_entropy(p), 4)
        h_d = round(_binary_entropy(d), 4)

        if d <= d_max:
            r_d = round(max(0.0, h_p - h_d), 4)
        else:
            r_d = 0.0

        return (
            f"Binary source P(1)={p}, Hamming distortion D={d}. R(D)=?",
            {"p": p, "d": d, "d_max": round(d_max, 4),
             "h_p": h_p, "h_d": h_d, "r_d": r_d},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for rate-distortion.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing H(p), H(D), and R(D) computation.
        """
        steps = [
            f"H(p) = H({data['p']}) = {data['h_p']}",
            f"H(D) = H({data['d']}) = {data['h_d']}",
            f"D_max = min({data['p']}, {round(1.0 - data['p'], 4)}) = {data['d_max']}",
        ]
        if data["d"] <= data["d_max"]:
            steps.append(f"R(D) = H(p) - H(D) = {data['h_p']} - {data['h_d']} = {data['r_d']}")
        else:
            steps.append(f"D={data['d']} > D_max={data['d_max']}, so R(D) = 0")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the rate-distortion value.

        Args:
            data: Solution data dict.

        Returns:
            R(D) as a string.
        """
        return f"R(D) = {data['r_d']}"


# ---------------------------------------------------------------------------
# 4. Typical Set (tier 6)
# ---------------------------------------------------------------------------

@register
class TypicalSetGenerator(StepGenerator):
    """Compute typical set size for a binary source.

    For binary source with P(1)=p, the typical set A_eps^n contains
    sequences with empirical entropy close to H(p).
    |A_eps^n| is approximately 2^{nH(p)}.

    Difficulty scaling:
        Difficulty 1-3: n=5-10, p=0.5.
        Difficulty 4-6: n=10-20, p varies.
        Difficulty 7-8: n=20-50, fine p values.

    Prerequisites:
        info_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "typical_set"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute typical set size for binary source"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a typical set problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 10)
            p = 0.5
        elif difficulty <= 6:
            n = self._rng.randint(10, 20)
            p = round(self._rng.uniform(0.2, 0.8), 2)
        else:
            n = self._rng.randint(20, 50)
            p = round(self._rng.uniform(0.1, 0.9), 3)

        h_p = round(_binary_entropy(p), 4)
        # |A_eps^n| ~ 2^{nH(p)}
        n_h = round(n * h_p, 4)
        typical_size = round(2.0 ** n_h, 4)
        total_sequences = 2 ** n
        fraction = round(typical_size / total_sequences, 4) if total_sequences > 0 else 0.0

        return (
            f"Binary source P(1)={p}, n={n}. Typical set size?",
            {"p": p, "n": n, "h_p": h_p, "n_h": n_h,
             "typical_size": typical_size,
             "total_sequences": total_sequences,
             "fraction": fraction},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for typical set.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing entropy and typical set computation.
        """
        return [
            f"H(p) = H({data['p']}) = {data['h_p']} bits",
            f"nH(p) = {data['n']}*{data['h_p']} = {data['n_h']}",
            f"|A_eps| ~ 2^{{{data['n_h']}}} ~ {data['typical_size']}",
            f"total 2^{data['n']} = {data['total_sequences']}",
            f"fraction of total: {data['fraction']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the typical set size.

        Args:
            data: Solution data dict.

        Returns:
            Typical set size as a string.
        """
        return f"|A_eps| ~ {data['typical_size']}"


# ---------------------------------------------------------------------------
# 5. Kraft-McMillan Inequality (tier 5)
# ---------------------------------------------------------------------------

@register
class KraftMcMillanGenerator(StepGenerator):
    """Verify Kraft-McMillan inequality for uniquely decodable codes.

    Given code lengths l_1, ..., l_n, check sum 2^{-l_i} <= 1.
    Also: given desired prefix-free code, determine valid lengths.

    Difficulty scaling:
        Difficulty 1-3: 3 codewords, verify only.
        Difficulty 4-6: 4-5 codewords, verify and check boundary.
        Difficulty 7-8: 5-6 codewords, find valid assignment.

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kraft_mcmillan"

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
        return "verify Kraft-McMillan inequality for code lengths"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kraft-McMillan inequality problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 3
            max_len = 4
        elif difficulty <= 6:
            n = self._rng.randint(4, 5)
            max_len = 5
        else:
            n = self._rng.randint(5, 6)
            max_len = 6

        # Generate lengths (sometimes valid, sometimes not)
        if self._rng.random() < 0.6:
            # Generate valid code lengths
            lengths = self._generate_valid_lengths(n, max_len)
        else:
            # Generate potentially invalid code lengths
            lengths = sorted([self._rng.randint(1, max_len) for _ in range(n)])

        # Compute Kraft sum
        terms = [round(2.0 ** (-l), 4) for l in lengths]
        kraft_sum = round(sum(terms), 4)
        is_valid = kraft_sum <= 1.0

        return (
            f"Code lengths: {lengths}. Verify Kraft inequality.",
            {"lengths": lengths, "n": n, "terms": terms,
             "kraft_sum": kraft_sum, "is_valid": is_valid},
        )

    def _generate_valid_lengths(self, n: int, max_len: int) -> list[int]:
        """Generate code lengths satisfying Kraft inequality.

        Args:
            n: Number of codewords.
            max_len: Maximum code length.

        Returns:
            Sorted list of valid code lengths.
        """
        for _ in range(100):
            lengths = sorted([self._rng.randint(1, max_len) for _ in range(n)])
            kraft = sum(2.0 ** (-l) for l in lengths)
            if kraft <= 1.0:
                return lengths
        return [1] + [max_len] * (n - 1)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Kraft-McMillan.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the Kraft sum computation.
        """
        term_strs = " + ".join(
            f"2^(-{l})={t}" for l, t in zip(data["lengths"], data["terms"])
        )
        return [
            f"lengths: {data['lengths']}",
            f"Kraft sum: {term_strs}",
            f"sum = {data['kraft_sum']}",
            f"sum <= 1.0: {data['is_valid']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Kraft inequality result.

        Args:
            data: Solution data dict.

        Returns:
            Kraft sum and validity as a string.
        """
        return f"Kraft={data['kraft_sum']}, valid={data['is_valid']}"


# ---------------------------------------------------------------------------
# 6. Joint Entropy (tier 5)
# ---------------------------------------------------------------------------

@register
class JointEntropyGenerator(StepGenerator):
    """Compute joint entropy H(X,Y) and verify subadditivity.

    H(X,Y) = -sum sum P(x,y)*log2(P(x,y)).
    Property: H(X,Y) <= H(X) + H(Y) with equality iff independent.

    Difficulty scaling:
        Difficulty 1-3: 2x2 joint distribution.
        Difficulty 4-6: 2x3 or 3x2 distribution.
        Difficulty 7-8: 3x3 distribution.

    Prerequisites:
        info_entropy.
    """

    _SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 2),
        4: (2, 3), 5: (3, 2), 6: (2, 3),
        7: (3, 3), 8: (3, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "joint_entropy"

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
        return "compute joint entropy H(X,Y) and check subadditivity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a joint entropy problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rows, cols = self._SIZES.get(difficulty, (3, 3))

        # Generate joint distribution
        raw = [[self._rng.randint(1, 10) for _ in range(cols)] for _ in range(rows)]
        total = sum(sum(row) for row in raw)
        joint = [[round(v / total, 4) for v in row] for row in raw]
        # Fix rounding
        s = sum(sum(row) for row in joint) - joint[-1][-1]
        joint[-1][-1] = round(1.0 - s, 4)

        # Marginals
        p_x = [round(sum(joint[i][j] for j in range(cols)), 4) for i in range(rows)]
        p_y = [round(sum(joint[i][j] for i in range(rows)), 4) for j in range(cols)]

        # H(X), H(Y), H(X,Y)
        h_x = round(_entropy_from_dist(p_x), 4)
        h_y = round(_entropy_from_dist(p_y), 4)

        h_xy = 0.0
        for row in joint:
            for p in row:
                if p > 0:
                    h_xy -= p * math.log2(p)
        h_xy = round(h_xy, 4)

        h_sum = round(h_x + h_y, 4)
        gap = round(h_sum - h_xy, 4)  # mutual information
        independent = abs(gap) < 0.001

        table_str = "; ".join(
            "[" + ", ".join(str(v) for v in row) + "]"
            for row in joint
        )

        return (
            f"P(X,Y) = [{table_str}]. H(X,Y)=?",
            {"joint": joint, "rows": rows, "cols": cols,
             "p_x": p_x, "p_y": p_y,
             "h_x": h_x, "h_y": h_y, "h_xy": h_xy,
             "h_sum": h_sum, "gap": gap, "independent": independent},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for joint entropy.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing H(X), H(Y), H(X,Y), and subadditivity.
        """
        return [
            f"P(X) = {data['p_x']}, P(Y) = {data['p_y']}",
            f"H(X) = {data['h_x']}, H(Y) = {data['h_y']}",
            f"H(X) + H(Y) = {data['h_sum']}",
            f"H(X,Y) = {data['h_xy']}",
            f"gap = H(X)+H(Y)-H(X,Y) = {data['gap']} (= I(X;Y))",
            f"independent: {data['independent']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the joint entropy and subadditivity check.

        Args:
            data: Solution data dict.

        Returns:
            H(X,Y) and gap as a string.
        """
        return f"H(X,Y)={data['h_xy']}, I(X;Y)={data['gap']}"
