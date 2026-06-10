"""Stochastic process generators.

8 generators covering random walks, stationary distributions, absorption
probabilities, birth-death chains, Poisson processes, Brownian motion
properties, martingale verification, and renewal theory across tiers 5-7.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

class FractionHelper:
    """Formats fractions and decimals for stochastic generators.

    Provides consistent formatting of Fraction objects and floats
    throughout the stochastic process generator module.
    """

    def format(self, frac: Fraction) -> str:
        """Format a Fraction as a readable string.

        Args:
            frac: Fraction instance.

        Returns:
            Integer string if denominator is 1, else a/b notation.
        """
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"{frac.numerator}/{frac.denominator}"

    def format_decimal(self, value: float, places: int = 4) -> str:
        """Format a float rounded to given decimal places.

        Args:
            value: Floating point number.
            places: Number of decimal places.

        Returns:
            Rounded string representation.
        """
        return str(round(value, places))


class StochasticMatrixBuilder:
    """Builds small stochastic transition matrices with Fraction entries.

    Constructs matrices where each row sums to 1 using integer weights
    normalised to fractions, keeping arithmetic tractable.
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded random instance.
        """
        self._rng = rng

    def build(self, size: int) -> list[list[Fraction]]:
        """Build a stochastic transition matrix.

        Args:
            size: Number of states (matrix dimension).

        Returns:
            Square matrix of Fractions where each row sums to 1.
        """
        return [self._build_row(size) for _ in range(size)]

    def _build_row(self, size: int) -> list[Fraction]:
        """Build one row of transition probabilities summing to 1.

        Args:
            size: Number of entries in the row.

        Returns:
            List of Fractions summing to 1.
        """
        weights = [self._rng.randint(1, 5) for _ in range(size)]
        total = sum(weights)
        return [Fraction(w, total) for w in weights]

    def build_absorbing(self, num_transient: int,
                        num_absorbing: int) -> list[list[Fraction]]:
        """Build an absorbing Markov chain transition matrix.

        Transient states have non-zero transition to at least one
        absorbing state. Absorbing states loop to themselves.

        Args:
            num_transient: Number of transient states.
            num_absorbing: Number of absorbing states.

        Returns:
            Transition matrix with absorbing structure.
        """
        total_states = num_transient + num_absorbing
        matrix = []
        for i in range(num_transient):
            weights = [self._rng.randint(1, 3) for _ in range(total_states)]
            weights[i] = 0
            has_absorbing = False
            for j in range(num_transient, total_states):
                if weights[j] > 0:
                    has_absorbing = True
            if not has_absorbing:
                j_abs = self._rng.randint(num_transient, total_states - 1)
                weights[j_abs] = self._rng.randint(1, 3)
            total = sum(weights)
            matrix.append([Fraction(w, total) for w in weights])
        for i in range(num_absorbing):
            row = [Fraction(0)] * total_states
            row[num_transient + i] = Fraction(1)
            matrix.append(row)
        return matrix


def _binomial(n: int, k: int) -> int:
    """Compute the binomial coefficient C(n, k).

    Args:
        n: Total items.
        k: Items chosen.

    Returns:
        C(n, k).
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    result = 1
    for i in range(min(k, n - k)):
        result = result * (n - i) // (i + 1)
    return result


def _factorial(n: int) -> int:
    """Compute n factorial.

    Args:
        n: Non-negative integer.

    Returns:
        n! as an integer.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def _mat_inverse_2x2(m: list[list[Fraction]]) -> list[list[Fraction]]:
    """Compute the inverse of a 2x2 matrix of Fractions.

    Args:
        m: 2x2 matrix of Fractions.

    Returns:
        Inverse matrix.

    Raises:
        ValueError: If matrix is singular.
    """
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if det == 0:
        raise ValueError("Singular matrix")
    return [
        [m[1][1] / det, -m[0][1] / det],
        [-m[1][0] / det, m[0][0] / det],
    ]


def _identity_matrix(n: int) -> list[list[Fraction]]:
    """Create an n x n identity matrix of Fractions.

    Args:
        n: Matrix dimension.

    Returns:
        Identity matrix.
    """
    return [
        [Fraction(1) if i == j else Fraction(0) for j in range(n)]
        for i in range(n)
    ]


def _mat_subtract(a: list[list[Fraction]],
                  b: list[list[Fraction]]) -> list[list[Fraction]]:
    """Subtract matrix b from matrix a.

    Args:
        a: First matrix.
        b: Second matrix.

    Returns:
        a - b as a new matrix.
    """
    n = len(a)
    m = len(a[0])
    return [
        [a[i][j] - b[i][j] for j in range(m)]
        for i in range(n)
    ]


def _mat_multiply(a: list[list[Fraction]],
                  b: list[list[Fraction]]) -> list[list[Fraction]]:
    """Multiply two matrices of Fractions.

    Args:
        a: Left matrix (n x m).
        b: Right matrix (m x p).

    Returns:
        Product matrix (n x p).
    """
    n = len(a)
    m = len(b[0])
    k = len(b)
    return [
        [sum(a[i][l] * b[l][j] for l in range(k)) for j in range(m)]
        for i in range(n)
    ]


def _format_matrix_row(row: list[Fraction], fmt: FractionHelper) -> str:
    """Format a matrix row as a readable string.

    Args:
        row: List of Fraction values.
        fmt: Fraction formatter.

    Returns:
        Comma-separated string of formatted values.
    """
    return ", ".join(fmt.format(v) for v in row)


# ═══════════════════════════════════════════════════════════════════
# 1. RANDOM WALK (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class RandomWalkGenerator(StepGenerator):
    """Compute probability of reaching state k in n steps on a 1D random walk.

    Starting at origin, each step goes +1 with probability p or -1 with
    probability 1-p. Uses the binomial distribution to compute
    P(S_n = k) where reaching k in n steps requires (n+k)/2 right steps.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 4], symmetric walk (p=1/2).
        Difficulty 4-6: n in [4, 6], symmetric walk.
        Difficulty 7-8: n in [4, 8], asymmetric walk (p=1/3, 2/3).

    Prerequisites:
        basic_prob (tier 2).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "random_walk"

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
            difficulty: Controls walk parameters.

        Returns:
            Task description string.
        """
        return "compute P(reach state k in n steps) for 1D random walk"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a random walk probability problem.

        Args:
            difficulty: Controls walk length and symmetry.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 4)
            p = Fraction(1, 2)
        elif difficulty <= 6:
            n = self._rng.randint(4, 6)
            p = Fraction(1, 2)
        else:
            n = self._rng.randint(4, 8)
            p = self._rng.choice([Fraction(1, 3), Fraction(2, 3)])

        possible_k = [k for k in range(-n, n + 1, 2)]
        k = self._rng.choice(possible_k)

        right_steps = (n + k) // 2
        if right_steps < 0 or right_steps > n:
            prob = Fraction(0)
        else:
            coeff = _binomial(n, right_steps)
            prob = Fraction(coeff) * p ** right_steps * (1 - p) ** (n - right_steps)

        prob_float = round(float(prob), 4)

        problem = (
            f"1D walk, n={n} steps, p(right)={self._fmt.format(p)}: "
            f"P(S_{n}={k})?"
        )
        return problem, {
            "n": n, "k": k, "p": p, "right_steps": right_steps,
            "coeff": _binomial(n, right_steps), "prob": prob,
            "prob_float": prob_float,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate random walk computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing binomial computation.
        """
        n = data["n"]
        k = data["k"]
        r = data["right_steps"]
        return [
            f"need (n+k)/2 = ({n}+{k})/2 = {r} right steps",
            f"C({n},{r}) = {data['coeff']}",
            f"P = C({n},{r}) * p^{r} * (1-p)^{n - r} = {data['prob_float']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the walk probability.

        Args:
            data: Solution data.

        Returns:
            Probability as a decimal.
        """
        return str(data["prob_float"])


# ═══════════════════════════════════════════════════════════════════
# 2. MARKOV STATIONARY (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class MarkovStationaryGenerator(StepGenerator):
    """Find the stationary distribution of a Markov chain.

    Given a stochastic transition matrix P, finds the row vector pi
    satisfying pi * P = pi and sum(pi) = 1. Solves for 2x2 or 3x3
    transition matrices using direct algebra.

    Difficulty scaling:
        Difficulty 1-3: 2x2 matrix.
        Difficulty 4-6: 2x2 matrix with varied weights.
        Difficulty 7-8: 3x3 matrix.

    Prerequisites:
        markov_chain (tier 5).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with matrix builder and fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = StochasticMatrixBuilder(self._rng)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "markov_stationary"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["markov_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls matrix size.

        Returns:
            Task description string.
        """
        return "find stationary distribution pi*P = pi"

    def _select_size(self, difficulty: int) -> int:
        """Choose matrix dimension based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            2 or 3.
        """
        if difficulty <= 6:
            return 2
        return 3

    def _solve_stationary_2x2(self, p: list[list[Fraction]]) -> list[Fraction]:
        """Solve for stationary distribution of a 2x2 chain.

        For P = [[a, b], [c, d]], pi_0 = c/(b+c), pi_1 = b/(b+c).

        Args:
            p: 2x2 transition matrix.

        Returns:
            Stationary distribution as a list of Fractions.
        """
        b = p[0][1]
        c = p[1][0]
        denom = b + c
        return [c / denom, b / denom]

    def _solve_stationary_3x3(self, p: list[list[Fraction]]) -> list[Fraction]:
        """Solve for stationary distribution of a 3x3 chain.

        Uses the system pi*P = pi with sum(pi) = 1. Reduces to
        solving two independent equations plus the normalisation.

        Args:
            p: 3x3 transition matrix.

        Returns:
            Stationary distribution as a list of Fractions.
        """
        a00 = p[0][0] - 1
        a01 = p[1][0]
        a02 = p[2][0]
        a10 = p[0][1]
        a11 = p[1][1] - 1
        a12 = p[2][1]

        det = a00 * a11 - a01 * a10
        if det == 0:
            return [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]

        rhs0 = -a02
        rhs1 = -a12

        pi0_ratio = (rhs0 * a11 - rhs1 * a01) / det
        pi1_ratio = (a00 * rhs1 - a10 * rhs0) / det

        total = pi0_ratio + pi1_ratio + 1
        return [pi0_ratio / total, pi1_ratio / total, Fraction(1) / total]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stationary distribution problem.

        Args:
            difficulty: Controls matrix size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        size = self._select_size(difficulty)
        p = self._builder.build(size)

        if size == 2:
            pi = self._solve_stationary_2x2(p)
        else:
            pi = self._solve_stationary_3x3(p)

        rows_str = "; ".join(
            "[" + _format_matrix_row(row, self._fmt) + "]"
            for row in p
        )
        problem = f"P = [{rows_str}]. Find stationary distribution."
        return problem, {"size": size, "P": p, "pi": pi}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate stationary distribution computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the system setup and solution.
        """
        pi = data["pi"]
        steps = ["solve pi*P = pi, sum(pi) = 1"]
        pi_str = ", ".join(self._fmt.format(v) for v in pi)
        steps.append(f"pi = [{pi_str}]")
        total = sum(pi)
        steps.append(f"verify sum = {self._fmt.format(total)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the stationary distribution.

        Args:
            data: Solution data.

        Returns:
            Formatted distribution vector.
        """
        return "[" + ", ".join(self._fmt.format(v) for v in data["pi"]) + "]"


# ═══════════════════════════════════════════════════════════════════
# 3. MARKOV ABSORPTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class MarkovAbsorptionGenerator(StepGenerator):
    """Compute absorption probabilities for an absorbing Markov chain.

    Given a chain with transient and absorbing states, computes the
    fundamental matrix N = (I - Q)^{-1} and absorption probability
    matrix B = N * R, where Q is the transient-to-transient submatrix
    and R is the transient-to-absorbing submatrix.

    Difficulty scaling:
        Difficulty 1-3: 1 transient + 2 absorbing states.
        Difficulty 4-6: 2 transient + 1 absorbing state.
        Difficulty 7-8: 2 transient + 2 absorbing states.

    Prerequisites:
        markov_stationary (tier 5).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with matrix builder and fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = StochasticMatrixBuilder(self._rng)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "markov_absorption"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["markov_stationary"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls chain complexity.

        Returns:
            Task description string.
        """
        return "compute absorption probabilities for absorbing chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an absorption probability problem.

        Args:
            difficulty: Controls number of transient/absorbing states.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            nt, na = 1, 2
        elif difficulty <= 6:
            nt, na = 2, 1
        else:
            nt, na = 2, 2

        p = self._builder.build_absorbing(nt, na)
        q = [[p[i][j] for j in range(nt)] for i in range(nt)]
        r = [[p[i][j] for j in range(nt, nt + na)] for i in range(nt)]

        identity = _identity_matrix(nt)
        i_minus_q = _mat_subtract(identity, q)

        if nt == 1:
            if i_minus_q[0][0] == 0:
                n_mat = [[Fraction(1)]]
            else:
                n_mat = [[Fraction(1) / i_minus_q[0][0]]]
        else:
            n_mat = _mat_inverse_2x2(i_minus_q)

        b_mat = _mat_multiply(n_mat, r)

        rows_str = "; ".join(
            "[" + _format_matrix_row(row, self._fmt) + "]"
            for row in p
        )
        problem = (
            f"Absorbing chain ({nt} transient, {na} absorbing), "
            f"P = [{rows_str}]. Absorption probs?"
        )
        return problem, {
            "nt": nt, "na": na, "P": p, "Q": q, "R": r,
            "N": n_mat, "B": b_mat,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate absorption probability computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing Q, R extraction and N, B computation.
        """
        nt = data["nt"]
        q_str = "; ".join(
            "[" + _format_matrix_row(row, self._fmt) + "]"
            for row in data["Q"]
        )
        r_str = "; ".join(
            "[" + _format_matrix_row(row, self._fmt) + "]"
            for row in data["R"]
        )
        steps = [
            f"Q (transient block) = [{q_str}]",
            f"R (absorbing block) = [{r_str}]",
            "N = (I - Q)^(-1)",
        ]
        for i in range(nt):
            b_row = ", ".join(self._fmt.format(v) for v in data["B"][i])
            steps.append(f"B[{i}] = [{b_row}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the absorption probability matrix.

        Args:
            data: Solution data.

        Returns:
            Formatted absorption matrix B.
        """
        rows = []
        for row in data["B"]:
            rows.append("[" + ", ".join(self._fmt.format(v) for v in row) + "]")
        return "B = [" + "; ".join(rows) + "]"


# ═══════════════════════════════════════════════════════════════════
# 4. BIRTH-DEATH CHAIN (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class BirthDeathGenerator(StepGenerator):
    """Compute steady-state of a birth-death chain.

    For birth rates lambda_i and death rates mu_i, the steady-state is
    pi_n = (lambda_0 * ... * lambda_{n-1}) / (mu_1 * ... * mu_n) * pi_0
    with pi_0 chosen so the distribution sums to 1.

    Difficulty scaling:
        Difficulty 1-3: 3 states, integer rates.
        Difficulty 4-6: 4 states, integer rates.
        Difficulty 7-8: 5 states, integer rates.

    Prerequisites:
        markov_stationary (tier 5).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "birth_death"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["markov_stationary"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls chain size.

        Returns:
            Task description string.
        """
        return "compute steady-state of birth-death chain"

    def _select_num_states(self, difficulty: int) -> int:
        """Choose number of states based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Number of states (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a birth-death chain problem.

        Args:
            difficulty: Controls chain size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num = self._select_num_states(difficulty)
        lambdas = [Fraction(self._rng.randint(1, 4)) for _ in range(num - 1)]
        mus = [Fraction(self._rng.randint(1, 4)) for _ in range(num - 1)]

        ratios = [Fraction(1)]
        for i in range(num - 1):
            ratios.append(ratios[-1] * lambdas[i] / mus[i])

        total = sum(ratios)
        pi = [r / total for r in ratios]

        lam_str = ", ".join(str(l) for l in lambdas)
        mu_str = ", ".join(str(m) for m in mus)
        problem = (
            f"Birth-death chain, {num} states: "
            f"lambda=[{lam_str}], mu=[{mu_str}]. Steady-state?"
        )
        return problem, {
            "num_states": num, "lambdas": lambdas, "mus": mus,
            "ratios": ratios, "pi": pi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate birth-death chain computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing ratio computation and normalisation.
        """
        num = data["num_states"]
        steps = []
        for i in range(1, num):
            r = data["ratios"][i]
            steps.append(f"pi_{i}/pi_0 = {self._fmt.format(r)}")
        total = sum(data["ratios"])
        steps.append(f"sum of ratios = {self._fmt.format(total)}")
        pi_str = ", ".join(self._fmt.format(v) for v in data["pi"])
        steps.append(f"pi = [{pi_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the steady-state distribution.

        Args:
            data: Solution data.

        Returns:
            Formatted distribution vector.
        """
        return "[" + ", ".join(self._fmt.format(v) for v in data["pi"]) + "]"


# ═══════════════════════════════════════════════════════════════════
# 5. POISSON PROCESS (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class PoissonProcessGenerator(StepGenerator):
    """Compute Poisson process probabilities and expected inter-arrival time.

    Computes P(N(t) = k) = (lambda*t)^k * e^{-lambda*t} / k! and the
    expected inter-arrival time 1/lambda for a Poisson process with
    rate lambda observed over interval [0, t].

    Difficulty scaling:
        Difficulty 1-3: lambda in [1, 2], t in [1, 2], k in [0, 3].
        Difficulty 4-6: lambda in [1, 3], t in [1, 3], k in [0, 5].
        Difficulty 7-8: lambda in [2, 5], t in [1, 4], k in [0, 7].

    Prerequisites:
        poisson_dist (tier 5).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "poisson_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["poisson_dist"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls process parameters.

        Returns:
            Task description string.
        """
        return "compute Poisson process P(N(t)=k) and E[inter-arrival]"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Poisson process probability problem.

        Args:
            difficulty: Controls rate, time, and count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam = self._rng.randint(1, 2)
            t = self._rng.randint(1, 2)
            k = self._rng.randint(0, 3)
        elif difficulty <= 6:
            lam = self._rng.randint(1, 3)
            t = self._rng.randint(1, 3)
            k = self._rng.randint(0, 5)
        else:
            lam = self._rng.randint(2, 5)
            t = self._rng.randint(1, 4)
            k = self._rng.randint(0, 7)

        mu = lam * t
        prob = round((mu ** k) * math.exp(-mu) / _factorial(k), 4)
        inter_arrival = round(1.0 / lam, 4)

        problem = (
            f"Poisson process: lambda={lam}, t={t}. "
            f"P(N({t})={k})? E[inter-arrival]?"
        )
        return problem, {
            "lam": lam, "t": t, "k": k, "mu": mu,
            "prob": prob, "inter_arrival": inter_arrival,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poisson process computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the probability formula evaluation.
        """
        lam = data["lam"]
        t = data["t"]
        k = data["k"]
        mu = data["mu"]
        return [
            f"lambda*t = {lam}*{t} = {mu}",
            f"P(N({t})={k}) = {mu}^{k} * e^(-{mu}) / {k}! = {data['prob']}",
            f"E[inter-arrival] = 1/{lam} = {data['inter_arrival']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the probability and inter-arrival time.

        Args:
            data: Solution data.

        Returns:
            Formatted probability and expected time.
        """
        return f"P={data['prob']}, E[T]={data['inter_arrival']}"


# ═══════════════════════════════════════════════════════════════════
# 6. BROWNIAN MOTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class BrownianMotionGenerator(StepGenerator):
    """Compute properties of standard Brownian motion.

    Evaluates fundamental properties: E[B_t] = 0, Var(B_t) = t,
    and Cov(B_s, B_t) = E[B_s * B_t] = min(s, t) for given time
    values s and t.

    Difficulty scaling:
        Difficulty 1-3: integer times, s and t in [1, 3].
        Difficulty 4-6: integer times, s and t in [1, 5].
        Difficulty 7-8: fractional times (multiples of 0.5).

    Prerequisites:
        std_dev (tier 3).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "brownian_motion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls time parameters.

        Returns:
            Task description string.
        """
        return "compute E[B_t], Var(B_t), E[B_s*B_t] for Brownian motion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Brownian motion properties problem.

        Args:
            difficulty: Controls time values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            s = self._rng.randint(1, 3)
            t = self._rng.randint(1, 3)
        elif difficulty <= 6:
            s = self._rng.randint(1, 5)
            t = self._rng.randint(1, 5)
        else:
            s = round(self._rng.randint(1, 10) * 0.5, 4)
            t = round(self._rng.randint(1, 10) * 0.5, 4)

        if s > t:
            s, t = t, s

        var_t = t
        cov_st = s
        std_t = round(math.sqrt(t), 4)

        problem = (
            f"BM: s={s}, t={t}. "
            f"E[B_t]? Var(B_t)? E[B_s*B_t]?"
        )
        return problem, {
            "s": s, "t": t, "var_t": var_t,
            "cov_st": cov_st, "std_t": std_t,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Brownian motion property steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each BM property computation.
        """
        t = data["t"]
        s = data["s"]
        return [
            f"E[B_{t}] = 0 (BM has zero mean)",
            f"Var(B_{t}) = {data['var_t']} (variance equals t)",
            f"Std(B_{t}) = sqrt({t}) = {data['std_t']}",
            f"E[B_{s}*B_{t}] = min({s},{t}) = {data['cov_st']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the BM properties.

        Args:
            data: Solution data.

        Returns:
            Formatted BM property values.
        """
        return (
            f"E[B_t]=0, Var(B_t)={data['var_t']}, "
            f"E[B_s*B_t]={data['cov_st']}"
        )


# ═══════════════════════════════════════════════════════════════════
# 7. MARTINGALE CHECK (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class MartingaleCheckGenerator(StepGenerator):
    """Verify the martingale property E[X_{n+1}|F_n] = X_n.

    Tests whether a given stochastic process is a martingale by
    checking the conditional expectation property. Uses simple
    random walks (martingale) and gambler's ruin variants
    (sometimes not a martingale if biased).

    Difficulty scaling:
        Difficulty 1-3: symmetric random walk (always martingale).
        Difficulty 4-6: random walk with drift (not martingale if drift != 0).
        Difficulty 7-8: squared walk or transformed processes.

    Prerequisites:
        expected_value (tier 3).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "martingale_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls process complexity.

        Returns:
            Task description string.
        """
        return "verify martingale property E[X_{n+1}|F_n] = X_n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a martingale verification problem.

        Args:
            difficulty: Controls process type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._symmetric_walk()
        if difficulty <= 6:
            return self._walk_with_drift()
        return self._squared_walk()

    def _symmetric_walk(self) -> tuple[str, dict]:
        """Generate a symmetric random walk martingale check.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x_n = self._rng.randint(0, 10)
        p = Fraction(1, 2)
        e_next = x_n * 1 + Fraction(1, 2) * 1 + Fraction(1, 2) * (-1)
        e_next_val = Fraction(x_n)
        is_martingale = True
        problem = (
            f"S_n = sum of +/-1, p(+1)=1/2. "
            f"X_n = S_n, X_n={x_n}. Martingale?"
        )
        return problem, {
            "process": "symmetric walk", "x_n": x_n,
            "e_next": self._fmt.format(e_next_val),
            "is_martingale": is_martingale,
            "explanation": "E[X_{n+1}|F_n] = X_n + E[step] = X_n + 0 = X_n",
        }

    def _walk_with_drift(self) -> tuple[str, dict]:
        """Generate a random walk with drift martingale check.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x_n = self._rng.randint(1, 10)
        p = self._rng.choice([Fraction(1, 3), Fraction(2, 3)])
        drift = p * 1 + (1 - p) * (-1)
        is_martingale = (drift == 0)
        e_next = Fraction(x_n) + drift

        problem = (
            f"Walk +1 w.p. {self._fmt.format(p)}, "
            f"-1 w.p. {self._fmt.format(1 - p)}. "
            f"X_n={x_n}. Martingale?"
        )
        return problem, {
            "process": "biased walk", "x_n": x_n,
            "e_next": self._fmt.format(e_next),
            "drift": self._fmt.format(drift),
            "is_martingale": is_martingale,
            "explanation": (
                f"E[step] = {self._fmt.format(drift)}, "
                f"E[X_{{n+1}}|F_n] = {x_n} + {self._fmt.format(drift)} "
                f"= {self._fmt.format(e_next)}"
            ),
        }

    def _squared_walk(self) -> tuple[str, dict]:
        """Generate a squared walk martingale check.

        X_n = S_n^2 - n where S_n is a symmetric random walk.
        This is a martingale since E[S_{n+1}^2 - (n+1)|F_n] = S_n^2 - n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(2, 6)
        s_n = self._rng.randint(-3, 3)
        x_n = s_n ** 2 - n
        e_s_sq = s_n ** 2 + 1
        e_next = e_s_sq - (n + 1)
        is_martingale = (e_next == x_n)

        problem = (
            f"S_n symmetric walk, X_n = S_n^2 - n. "
            f"S_{n}={s_n}, n={n}. Martingale?"
        )
        return problem, {
            "process": "squared walk", "x_n": x_n, "s_n": s_n, "n": n,
            "e_next": str(e_next),
            "is_martingale": is_martingale,
            "explanation": (
                f"E[S_{{n+1}}^2|F_n] = S_n^2 + 1 = {e_s_sq}, "
                f"E[X_{{n+1}}|F_n] = {e_s_sq} - {n + 1} = {e_next} = X_n"
            ),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate martingale verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conditional expectation check.
        """
        return [
            f"process: {data['process']}",
            f"X_n = {data['x_n']}",
            data["explanation"],
            f"E[X_{{n+1}}|F_n] = {data['e_next']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the martingale verdict.

        Args:
            data: Solution data.

        Returns:
            YES or NO with explanation.
        """
        if data["is_martingale"]:
            return "YES, martingale"
        return f"NO, not martingale (E[X_{{n+1}}|F_n] = {data['e_next']} != X_n)"


# ═══════════════════════════════════════════════════════════════════
# 8. RENEWAL THEORY (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class RenewalTheoryGenerator(StepGenerator):
    """Compute the renewal function m(t) for simple inter-arrival distributions.

    For geometric inter-arrivals (discrete) or exponential inter-arrivals
    (continuous), computes m(t) = sum_{n>=1} P(S_n <= t) where S_n is
    the n-th renewal time. For exponential(lambda), m(t) = lambda*t.
    For geometric(p), uses convolution.

    Difficulty scaling:
        Difficulty 1-3: exponential inter-arrival, small t.
        Difficulty 4-6: exponential inter-arrival, larger t.
        Difficulty 7-8: geometric inter-arrival (discrete renewal).

    Prerequisites:
        poisson_process (tier 5).
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction helper.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionHelper()

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "renewal_theory"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["poisson_process"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls distribution type.

        Returns:
            Task description string.
        """
        return "compute renewal function m(t)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a renewal theory problem.

        Args:
            difficulty: Controls distribution type and parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            return self._exponential_renewal(difficulty)
        return self._geometric_renewal()

    def _exponential_renewal(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exponential inter-arrival renewal problem.

        For Exp(lambda) inter-arrivals, the renewal process is Poisson
        and m(t) = lambda * t.

        Args:
            difficulty: Controls rate and time values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam = self._rng.randint(1, 3)
            t = self._rng.randint(1, 3)
        else:
            lam = self._rng.randint(1, 5)
            t = self._rng.randint(2, 5)

        m_t = round(lam * t, 4)
        e_inter = round(1.0 / lam, 4)

        problem = (
            f"Renewal process, Exp(lambda={lam}) inter-arrivals. "
            f"Compute m({t})."
        )
        return problem, {
            "distribution": "exponential", "lam": lam, "t": t,
            "m_t": m_t, "e_inter": e_inter,
            "terms": [
                f"m(t) = lambda*t (Poisson renewal)",
                f"m({t}) = {lam}*{t} = {m_t}",
            ],
        }

    def _geometric_renewal(self) -> tuple[str, dict]:
        """Generate a geometric inter-arrival renewal problem.

        For Geom(p) inter-arrivals, m(t) = sum_{n=1}^{floor(t)} P(S_n<=t)
        where S_n ~ NegBin(n, p). For small t, computed by convolution.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p = self._rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)])
        t = self._rng.randint(2, 5)

        terms = []
        m_t = Fraction(0)
        for n in range(1, t + 1):
            prob_sn_le_t = Fraction(0)
            for s in range(n, t + 1):
                coeff = _binomial(s - 1, n - 1)
                prob_exact = Fraction(coeff) * p ** n * (1 - p) ** (s - n)
                prob_sn_le_t += prob_exact
            m_t += prob_sn_le_t
            terms.append(f"P(S_{n}<={t})={self._fmt.format(prob_sn_le_t)}")

        m_t_float = round(float(m_t), 4)

        problem = (
            f"Renewal, Geom(p={self._fmt.format(p)}) inter-arrivals. "
            f"Compute m({t})."
        )
        return problem, {
            "distribution": "geometric", "p": p, "t": t,
            "m_t": m_t_float, "e_inter": self._fmt.format(Fraction(1) / p),
            "terms": terms,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate renewal function computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each term of the renewal function.
        """
        steps = [f"inter-arrival: {data['distribution']}"]
        steps.extend(data["terms"])
        steps.append(f"m({data['t']}) = {data['m_t']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the renewal function value.

        Args:
            data: Solution data.

        Returns:
            Formatted renewal function value.
        """
        return f"m({data['t']}) = {data['m_t']}"
