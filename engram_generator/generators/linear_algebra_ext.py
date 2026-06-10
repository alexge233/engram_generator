"""Extended linear algebra generators -- null space, Jordan form, SVD, etc.

12 generators across tiers 4-6 deepening the linear algebra domain
with subspace computations, decompositions, and applications.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mat_mul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Multiply two matrices.

    Args:
        A: Left matrix (m x n).
        B: Right matrix (n x p).

    Returns:
        Product matrix (m x p).
    """
    m, n, p = len(A), len(A[0]), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(n))
             for j in range(p)] for i in range(m)]


def _mat_vec(A: list[list[float]], v: list[float]) -> list[float]:
    """Multiply matrix by column vector.

    Args:
        A: Matrix (m x n).
        v: Vector of length n.

    Returns:
        Result vector of length m.
    """
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _dot(u: list[float], v: list[float]) -> float:
    """Compute dot product of two vectors.

    Args:
        u: First vector.
        v: Second vector.

    Returns:
        Scalar dot product.
    """
    return sum(a * b for a, b in zip(u, v))


def _norm(u: list[float]) -> float:
    """Compute Euclidean norm of a vector.

    Args:
        u: Input vector.

    Returns:
        Euclidean norm.
    """
    return math.sqrt(_dot(u, u))


def _scale(s: float, u: list[float]) -> list[float]:
    """Scale a vector by a scalar.

    Args:
        s: Scalar factor.
        u: Input vector.

    Returns:
        Scaled vector.
    """
    return [s * x for x in u]


def _sub(u: list[float], v: list[float]) -> list[float]:
    """Subtract vector v from u.

    Args:
        u: First vector.
        v: Second vector.

    Returns:
        Difference vector.
    """
    return [a - b for a, b in zip(u, v)]


def _rref(matrix: list[list[float]]) -> tuple[list[list[float]], list[int]]:
    """Compute reduced row echelon form and pivot columns.

    Args:
        matrix: Input matrix as list of rows.

    Returns:
        Tuple of (rref_matrix, pivot_column_indices).
    """
    M = [row[:] for row in matrix]
    rows, cols = len(M), len(M[0])
    pivots = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        # Find pivot
        max_row = r
        for i in range(r + 1, rows):
            if abs(M[i][c]) > abs(M[max_row][c]):
                max_row = i
        if abs(M[max_row][c]) < 1e-10:
            continue
        M[r], M[max_row] = M[max_row], M[r]
        scale_val = M[r][c]
        M[r] = [x / scale_val for x in M[r]]
        for i in range(rows):
            if i != r and abs(M[i][c]) > 1e-10:
                factor = M[i][c]
                M[i] = [M[i][j] - factor * M[r][j] for j in range(cols)]
        pivots.append(c)
        r += 1
    return M, pivots


def _det2(A: list[list[float]]) -> float:
    """Compute determinant of a 2x2 matrix.

    Args:
        A: 2x2 matrix.

    Returns:
        Determinant value.
    """
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def _inv2(A: list[list[float]]) -> list[list[float]]:
    """Compute inverse of a 2x2 matrix.

    Args:
        A: 2x2 matrix.

    Returns:
        Inverse matrix.

    Raises:
        ValueError: If matrix is singular.
    """
    d = _det2(A)
    if abs(d) < 1e-10:
        raise ValueError("Singular matrix")
    return [[A[1][1] / d, -A[0][1] / d],
            [-A[1][0] / d, A[0][0] / d]]


def _transpose(A: list[list[float]]) -> list[list[float]]:
    """Compute matrix transpose.

    Args:
        A: Input matrix (m x n).

    Returns:
        Transposed matrix (n x m).
    """
    m, n = len(A), len(A[0])
    return [[A[i][j] for i in range(m)] for j in range(n)]


def _fmt(x: float) -> str:
    """Format a float, showing integer when exact.

    Args:
        x: Input value.

    Returns:
        Formatted string.
    """
    if abs(x - round(x)) < 1e-8:
        return str(int(round(x)))
    return str(round(x, 4))


def _fmt_vec(v: list[float]) -> str:
    """Format a vector for display.

    Args:
        v: Input vector.

    Returns:
        Formatted string like [1, 2, 3].
    """
    return "[" + ", ".join(_fmt(x) for x in v) + "]"


def _fmt_mat(M: list[list[float]]) -> str:
    """Format a matrix for display.

    Args:
        M: Input matrix.

    Returns:
        Formatted string like [[1, 2], [3, 4]].
    """
    return "[" + ", ".join(_fmt_vec(row) for row in M) + "]"


# ---------------------------------------------------------------------------
# 1. Null Space (tier 5)
# ---------------------------------------------------------------------------

@register
class NullSpaceGenerator(StepGenerator):
    """Find null space basis of a matrix by RREF.

    Row-reduces an augmented [A|0] system to RREF, identifies free
    variables, and writes basis vectors for the null space.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "null_space"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gaussian_elimination"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find a basis for the null space of A"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a null space problem.

        Builds a matrix with a guaranteed non-trivial null space by
        constructing columns where at least one is a linear combination
        of others.

        Args:
            difficulty: Controls matrix size and entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            rows, cols = 2, 3
        else:
            rows, cols = 3, 4
        mag = min(2 + difficulty, 5)

        # Build independent columns then add dependent one
        indep = self._rng.randint(1, rows)
        A = [[0.0] * cols for _ in range(rows)]
        for c in range(indep):
            for r in range(rows):
                A[r][c] = float(self._rng.randint(-mag, mag))
        # Ensure first column non-zero
        if all(A[r][0] == 0 for r in range(rows)):
            A[0][0] = 1.0

        # Remaining columns as combinations
        for c in range(indep, cols):
            coeffs = [self._rng.randint(-2, 2) for _ in range(indep)]
            if all(co == 0 for co in coeffs):
                coeffs[0] = 1
            for r in range(rows):
                A[r][c] = sum(coeffs[k] * A[r][k] for k in range(indep))

        rref_mat, pivots = _rref(A)
        rank = len(pivots)
        free_cols = [c for c in range(cols) if c not in pivots]
        nullity = len(free_cols)

        # Build null space basis
        basis = []
        for fc in free_cols:
            vec = [0.0] * cols
            vec[fc] = 1.0
            for i, pc in enumerate(pivots):
                vec[pc] = -rref_mat[i][fc]
            basis.append([round(x, 4) for x in vec])

        A_int = [[int(round(A[r][c])) for c in range(cols)]
                  for r in range(rows)]
        problem = f"null space of A = {A_int}"
        return problem, {
            "A": A_int, "rref": [[round(x, 4) for x in row]
                                  for row in rref_mat],
            "pivots": pivots, "free_cols": free_cols,
            "rank": rank, "nullity": nullity, "basis": basis,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"row reduce to RREF",
            f"pivot columns: {sd['pivots']}",
            f"free columns: {sd['free_cols']}",
            f"rank = {sd['rank']}, nullity = {sd['nullity']}",
        ]
        for i, v in enumerate(sd["basis"]):
            steps.append(f"basis vector {i + 1}: {_fmt_vec(v)}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the null space basis.

        Args:
            sd: Solution data.

        Returns:
            Basis vectors as a string.
        """
        parts = [_fmt_vec(v) for v in sd["basis"]]
        return f"null space basis: {{{', '.join(parts)}}}"


# ---------------------------------------------------------------------------
# 2. Column Space (tier 5)
# ---------------------------------------------------------------------------

@register
class ColumnSpaceGenerator(StepGenerator):
    """Find column space basis by identifying pivot columns after RREF.

    Row-reduces A to RREF, finds pivot columns, and returns the
    corresponding original columns of A as the basis.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "column_space"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gaussian_elimination"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find a basis for the column space of A"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a column space problem.

        Args:
            difficulty: Controls matrix size and entry range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            rows, cols = 3, 2
        elif difficulty <= 5:
            rows, cols = 3, 3
        else:
            rows, cols = 3, 4
        mag = min(2 + difficulty, 5)
        A = [[self._rng.randint(-mag, mag) for _ in range(cols)]
             for _ in range(rows)]
        if all(A[r][0] == 0 for r in range(rows)):
            A[0][0] = 1

        _, pivots = _rref(A)
        rank = len(pivots)
        basis_cols = [[A[r][c] for r in range(rows)] for c in pivots]

        problem = f"column space of A = {A}"
        return problem, {
            "A": A, "pivots": pivots, "rank": rank,
            "basis_cols": basis_cols,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            "row reduce A to RREF",
            f"pivot columns: {sd['pivots']}",
            f"rank = {sd['rank']}",
        ]
        for i, col in enumerate(sd["basis_cols"]):
            steps.append(f"basis col {i + 1} (original col {sd['pivots'][i]}): {col}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the column space basis.

        Args:
            sd: Solution data.

        Returns:
            Basis vectors as a string.
        """
        parts = [str(c) for c in sd["basis_cols"]]
        return f"col space basis: {{{', '.join(parts)}}}"


# ---------------------------------------------------------------------------
# 3. Rank-Nullity (tier 5)
# ---------------------------------------------------------------------------

@register
class RankNullityGenerator(StepGenerator):
    """Verify rank-nullity theorem: rank(A) + nullity(A) = n.

    Computes rank from RREF pivot count and nullity from free variable
    count, then verifies they sum to the number of columns.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rank_nullity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["null_space"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "verify the rank-nullity theorem for A"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rank-nullity verification problem.

        Constructs a matrix with a known rank by building dependent columns,
        then asks to verify rank + nullity = number of columns.

        Args:
            difficulty: Controls matrix dimensions.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            rows, cols = 2, 3
        elif difficulty <= 5:
            rows, cols = 3, 4
        else:
            rows, cols = 3, 5
        mag = min(2 + difficulty, 5)

        A = [[self._rng.randint(-mag, mag) for _ in range(cols)]
             for _ in range(rows)]
        if all(A[r][0] == 0 for r in range(rows)):
            A[0][0] = 1

        _, pivots = _rref(A)
        rank = len(pivots)
        nullity = cols - rank

        problem = f"verify rank-nullity for A = {A}"
        return problem, {
            "A": A, "rank": rank, "nullity": nullity,
            "n": cols, "pivots": pivots,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "row reduce A to RREF",
            f"pivot columns: {sd['pivots']}, rank = {sd['rank']}",
            f"free variables: {sd['n']} - {sd['rank']} = {sd['nullity']}",
            f"rank + nullity = {sd['rank']} + {sd['nullity']} = {sd['n']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rank-nullity verification.

        Args:
            sd: Solution data.

        Returns:
            Verification string.
        """
        return (
            f"rank={sd['rank']}, nullity={sd['nullity']}, "
            f"rank+nullity={sd['n']}"
        )


# ---------------------------------------------------------------------------
# 4. Change of Basis (tier 6)
# ---------------------------------------------------------------------------

@register
class ChangeOfBasisGenerator(StepGenerator):
    """Convert a vector from one basis to another using a transition matrix.

    Given bases B1 and B2 in R^2 and a vector expressed in B1 coordinates,
    computes the transition matrix P = B2^{-1} * B1 and multiplies.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "change_of_basis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_inverse"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find the vector's representation in the new basis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a change of basis problem in R^2.

        Constructs two invertible 2x2 bases and a coordinate vector,
        then computes the transition matrix and new coordinates.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 4)

        def make_basis():
            while True:
                B = [[self._rng.randint(-mag, mag) for _ in range(2)]
                     for _ in range(2)]
                if abs(_det2(B)) > 0.5:
                    return B

        B1 = make_basis()
        B2 = make_basis()
        v_b1 = [float(self._rng.randint(-3, 3)) for _ in range(2)]
        if all(x == 0 for x in v_b1):
            v_b1[0] = 1.0

        # Standard coordinates: x = B1 * v_b1
        x_std = _mat_vec(B1, v_b1)

        # New coordinates: v_b2 = B2^{-1} * x_std
        B2_inv = _inv2(B2)
        v_b2 = _mat_vec(B2_inv, x_std)
        v_b2 = [round(x, 4) for x in v_b2]

        # Transition matrix P = B2^{-1} * B1
        P = _mat_mul(B2_inv, B1)
        P = [[round(x, 4) for x in row] for row in P]

        B1_int = [[int(x) for x in row] for row in B1]
        B2_int = [[int(x) for x in row] for row in B2]
        v_b1_int = [int(x) for x in v_b1]

        problem = (
            f"B1={B1_int}, B2={B2_int}, "
            f"[v]_B1={v_b1_int}"
        )
        return problem, {
            "B1": B1_int, "B2": B2_int, "v_b1": v_b1_int,
            "x_std": [round(x, 4) for x in x_std],
            "P": P, "v_b2": v_b2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"standard coords: x = B1 * v_B1 = {sd['x_std']}",
            f"P = B2^(-1) * B1 = {_fmt_mat(sd['P'])}",
            f"[v]_B2 = B2^(-1) * x = {_fmt_vec(sd['v_b2'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the vector in the new basis.

        Args:
            sd: Solution data.

        Returns:
            Coordinate vector string.
        """
        return f"[v]_B2 = {_fmt_vec(sd['v_b2'])}"


# ---------------------------------------------------------------------------
# 5. Jordan Form (tier 6)
# ---------------------------------------------------------------------------

@register
class JordanFormGenerator(StepGenerator):
    """Find Jordan normal form of a 2x2 matrix.

    For 2x2 matrices with repeated eigenvalues, determines whether the
    matrix is diagonalisable or has a Jordan block by checking the
    geometric multiplicity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jordan_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find the Jordan normal form of the matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Jordan form problem for a 2x2 matrix.

        Constructs either a diagonalisable matrix (lambda*I) or a
        non-diagonalisable matrix (lambda*I + nilpotent) with repeated
        eigenvalues.

        Args:
            difficulty: Controls eigenvalue magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        lam = self._rng.randint(-3, 3)
        is_diag = self._rng.choice([True, False])

        if is_diag:
            # lambda * I: already diagonal
            A = [[lam, 0], [0, lam]]
            J = [[lam, 0], [0, lam]]
            geo_mult = 2
            diag_str = "yes"
        else:
            # Jordan block: [[lam, 1], [0, lam]]
            # Construct as P * J * P^{-1} with simple P
            A = [[lam, 1], [0, lam]]
            J = [[lam, 1], [0, lam]]
            geo_mult = 1
            diag_str = "no"

        tr = A[0][0] + A[1][1]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        disc = tr * tr - 4 * det

        problem = f"Jordan form of A = {A}"
        return problem, {
            "A": A, "eigenvalue": lam, "alg_mult": 2,
            "geo_mult": geo_mult, "J": J,
            "diagonalisable": diag_str,
            "trace": tr, "det": det, "disc": disc,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"char poly: t^2 - {sd['trace']}t + {sd['det']} = 0",
            f"disc = {sd['disc']}, repeated eigenvalue = {sd['eigenvalue']}",
            f"alg multiplicity = {sd['alg_mult']}, geo multiplicity = {sd['geo_mult']}",
            f"diagonalisable: {sd['diagonalisable']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Jordan form.

        Args:
            sd: Solution data.

        Returns:
            Jordan matrix string.
        """
        return f"J = {sd['J']}"


# ---------------------------------------------------------------------------
# 6. Gram-Schmidt (tier 5)
# ---------------------------------------------------------------------------

@register
class GramSchmidtGenerator(StepGenerator):
    """Apply Gram-Schmidt orthogonalisation to vectors in R^3.

    Takes 2-3 linearly independent vectors and produces an orthonormal
    set by iterative projection subtraction and normalisation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gram_schmidt"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dot_product", "vector_norm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "apply Gram-Schmidt orthogonalisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gram-Schmidt problem in R^3.

        Creates 2 or 3 linearly independent vectors with small integer
        entries and orthogonalises then normalises them.

        Args:
            difficulty: Controls number of vectors and entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_vecs = 2 if difficulty <= 4 else 3
        mag = min(2 + difficulty, 5)

        vecs: list[list[float]] = []
        for _ in range(n_vecs):
            v = [float(self._rng.randint(-mag, mag)) for _ in range(3)]
            if all(x == 0 for x in v):
                v[0] = 1.0
            vecs.append(v)

        # Orthogonalise
        u_vecs: list[list[float]] = []
        e_vecs: list[list[float]] = []
        steps_log: list[str] = []

        for i, v in enumerate(vecs):
            u = list(v)
            for j in range(i):
                proj = _dot(v, e_vecs[j])
                u = _sub(u, _scale(proj, e_vecs[j]))
                steps_log.append(
                    f"proj(v{i + 1}, e{j + 1}) = {round(proj, 4)}"
                )
            n_val = _norm(u)
            if n_val < 1e-10:
                u = [0.0, 0.0, 0.0]
                u[i % 3] = 1.0
                n_val = 1.0
            e = _scale(1.0 / n_val, u)
            u_vecs.append([round(x, 4) for x in u])
            e_vecs.append([round(x, 4) for x in e])
            steps_log.append(
                f"u{i + 1} = {_fmt_vec(u_vecs[-1])}, "
                f"||u{i + 1}|| = {round(n_val, 4)}"
            )
            steps_log.append(f"e{i + 1} = {_fmt_vec(e_vecs[-1])}")

        vecs_int = [[int(x) for x in v] for v in vecs]
        problem = f"Gram-Schmidt on {vecs_int}"
        return problem, {
            "vecs": vecs_int, "u_vecs": u_vecs,
            "e_vecs": e_vecs, "steps_log": steps_log,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the orthonormal set.

        Args:
            sd: Solution data.

        Returns:
            Orthonormal vectors as a string.
        """
        parts = [_fmt_vec(e) for e in sd["e_vecs"]]
        return f"orthonormal: {{{', '.join(parts)}}}"


# ---------------------------------------------------------------------------
# 7. Quadratic Form (tier 5)
# ---------------------------------------------------------------------------

@register
class QuadraticFormGenerator(StepGenerator):
    """Write and classify a quadratic form from a symmetric matrix.

    Given a symmetric matrix A, writes x^T A x in expanded form and
    classifies it as positive/negative definite, semidefinite, or
    indefinite from the eigenvalues.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quadratic_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "write the quadratic form and classify definiteness"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic form classification problem.

        Builds a 2x2 symmetric matrix and computes its eigenvalues
        to classify the form.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 4)
        a = self._rng.randint(-mag, mag)
        b = self._rng.randint(-mag, mag)
        d = self._rng.randint(-mag, mag)
        A = [[a, b], [b, d]]

        # Quadratic form: a*x1^2 + 2b*x1*x2 + d*x2^2
        qf_str = f"{a}*x1^2 + {2 * b}*x1*x2 + {d}*x2^2"

        # Eigenvalues of 2x2 symmetric: (a+d)/2 +/- sqrt(((a-d)/2)^2 + b^2)
        tr = a + d
        det_val = a * d - b * b
        disc = tr * tr - 4 * det_val
        if disc < 0:
            disc = 0.0
        sqrt_disc = math.sqrt(disc)
        lam1 = round((tr + sqrt_disc) / 2, 4)
        lam2 = round((tr - sqrt_disc) / 2, 4)

        if lam1 > 0 and lam2 > 0:
            classification = "positive definite"
        elif lam1 >= 0 and lam2 >= 0:
            classification = "positive semidefinite"
        elif lam1 < 0 and lam2 < 0:
            classification = "negative definite"
        elif lam1 <= 0 and lam2 <= 0:
            classification = "negative semidefinite"
        else:
            classification = "indefinite"

        problem = f"classify quadratic form for A = {A}"
        return problem, {
            "A": A, "qf": qf_str, "lam1": lam1, "lam2": lam2,
            "classification": classification,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"Q(x) = x^T A x = {sd['qf']}",
            f"eigenvalues: lam1 = {sd['lam1']}, lam2 = {sd['lam2']}",
            f"sign pattern -> {sd['classification']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the classification.

        Args:
            sd: Solution data.

        Returns:
            Classification string.
        """
        return sd["classification"]


# ---------------------------------------------------------------------------
# 8. Matrix Exponential (tier 6)
# ---------------------------------------------------------------------------

@register
class MatrixExponentialGenerator(StepGenerator):
    """Compute e^{At} for a 2x2 diagonal or nilpotent matrix.

    For diagonal matrices, e^{Dt} = diag(e^{d1*t}, e^{d2*t}).
    For nilpotent matrices N with N^2 = 0, e^{Nt} = I + Nt.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matrix_exponential"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the matrix exponential e^{At}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matrix exponential problem.

        Randomly chooses between diagonal and nilpotent 2x2 matrix.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mat_type = self._rng.choice(["diagonal", "nilpotent"])
        t = self._rng.randint(1, 3)

        if mat_type == "diagonal":
            d1 = self._rng.randint(-2, 2)
            d2 = self._rng.randint(-2, 2)
            A = [[d1, 0], [0, d2]]
            e_d1t = round(math.exp(d1 * t), 4)
            e_d2t = round(math.exp(d2 * t), 4)
            result = [[e_d1t, 0.0], [0.0, e_d2t]]
            method = "diagonal"
            detail = f"e^{{d1*t}} = e^{{{d1}*{t}}} = {e_d1t}"
            detail2 = f"e^{{d2*t}} = e^{{{d2}*{t}}} = {e_d2t}"
        else:
            c = self._rng.randint(1, 3)
            A = [[0, c], [0, 0]]
            result = [[1.0, round(c * t, 4)], [0.0, 1.0]]
            method = "nilpotent (N^2 = 0)"
            detail = f"e^{{Nt}} = I + Nt"
            detail2 = f"Nt = [[0, {c * t}], [0, 0]]"

        problem = f"e^{{At}} for A = {A}, t = {t}"
        return problem, {
            "A": A, "t": t, "result": result,
            "method": method, "detail": detail, "detail2": detail2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"A = {sd['A']}, type: {sd['method']}",
            sd["detail"],
            sd["detail2"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the matrix exponential.

        Args:
            sd: Solution data.

        Returns:
            Result matrix string.
        """
        return f"e^{{At}} = {_fmt_mat(sd['result'])}"


# ---------------------------------------------------------------------------
# 9. Projection Matrix (tier 5)
# ---------------------------------------------------------------------------

@register
class ProjectionMatrixGenerator(StepGenerator):
    """Compute projection matrix P = A(A^T A)^{-1} A^T and project a vector.

    Given a column vector (or matrix) A defining a subspace, computes the
    projection matrix onto col(A) and projects a given vector.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "projection_matrix"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the projection matrix and project the vector"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a projection matrix problem.

        Uses a single column vector a in R^2 or R^3 to form
        P = a(a^T a)^{-1} a^T = (a a^T) / (a^T a).

        Args:
            difficulty: Controls vector dimension and magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dim = 2 if difficulty <= 4 else 3
        mag = min(1 + difficulty, 4)

        a = [float(self._rng.randint(-mag, mag)) for _ in range(dim)]
        if all(x == 0 for x in a):
            a[0] = 1.0

        b = [float(self._rng.randint(-mag, mag)) for _ in range(dim)]
        if all(x == 0 for x in b):
            b[0] = 1.0

        ata = _dot(a, a)
        # P = (a a^T) / (a^T a)
        P = [[round(a[i] * a[j] / ata, 4)
              for j in range(dim)] for i in range(dim)]

        # Projection: Pb
        proj = [round(sum(P[i][j] * b[j] for j in range(dim)), 4)
                for i in range(dim)]

        a_int = [int(x) for x in a]
        b_int = [int(x) for x in b]
        problem = f"project b = {b_int} onto span(a), a = {a_int}"
        return problem, {
            "a": a_int, "b": b_int, "ata": round(ata, 4),
            "P": P, "proj": proj,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"a^T a = {sd['ata']}",
            f"P = (a a^T) / (a^T a) = {_fmt_mat(sd['P'])}",
            f"proj = P * b = {_fmt_vec(sd['proj'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the projection.

        Args:
            sd: Solution data.

        Returns:
            Projection vector string.
        """
        return f"projection = {_fmt_vec(sd['proj'])}"


# ---------------------------------------------------------------------------
# 10. Cross Product / Triple Product (tier 4)
# ---------------------------------------------------------------------------

@register
class CrossProductTripleGenerator(StepGenerator):
    """Compute scalar triple product and vector triple product.

    Scalar triple product: a . (b x c) = det[a|b|c].
    Vector triple product: a x (b x c) = b(a.c) - c(a.b) (BAC-CAB rule).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cross_product_triple"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["determinant"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the scalar and vector triple products"

    def _cross(self, u: list[int], v: list[int]) -> list[int]:
        """Compute cross product of two 3-vectors.

        Args:
            u: First vector.
            v: Second vector.

        Returns:
            Cross product vector.
        """
        return [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a triple product problem.

        Creates three random vectors in R^3 and computes both the
        scalar triple product and vector triple product.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 4)
        a = [self._rng.randint(-mag, mag) for _ in range(3)]
        b = [self._rng.randint(-mag, mag) for _ in range(3)]
        c = [self._rng.randint(-mag, mag) for _ in range(3)]

        bxc = self._cross(b, c)
        scalar_tp = sum(a[i] * bxc[i] for i in range(3))

        # BAC-CAB: a x (b x c) = b(a.c) - c(a.b)
        a_dot_c = sum(a[i] * c[i] for i in range(3))
        a_dot_b = sum(a[i] * b[i] for i in range(3))
        vec_tp = [b[i] * a_dot_c - c[i] * a_dot_b for i in range(3)]

        problem = f"a={a}, b={b}, c={c}"
        return problem, {
            "a": a, "b": b, "c": c,
            "bxc": bxc, "scalar_tp": scalar_tp,
            "a_dot_c": a_dot_c, "a_dot_b": a_dot_b,
            "vec_tp": vec_tp,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"b x c = {sd['bxc']}",
            f"a . (b x c) = {sd['scalar_tp']}",
            f"a.c = {sd['a_dot_c']}, a.b = {sd['a_dot_b']}",
            f"a x (b x c) = b(a.c) - c(a.b) = {sd['vec_tp']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return both triple products.

        Args:
            sd: Solution data.

        Returns:
            Triple product values as a string.
        """
        return (
            f"scalar triple = {sd['scalar_tp']}, "
            f"vector triple = {sd['vec_tp']}"
        )


# ---------------------------------------------------------------------------
# 11. Markov Steady State (tier 5)
# ---------------------------------------------------------------------------

@register
class MarkovSteadyStateGenerator(StepGenerator):
    """Find the steady-state distribution of a stochastic matrix.

    Solves pi * P = pi with sum(pi) = 1 for 2x2 stochastic matrices.
    Rewrites as (P^T - I) pi = 0 plus the normalisation constraint.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "markov_steady_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find the steady-state distribution of the Markov chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Markov steady-state problem for a 2x2 matrix.

        Constructs a row-stochastic matrix with entries as simple
        fractions, then solves for the stationary distribution.

        Args:
            difficulty: Controls denominator complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Generate p in (0,1) as k/10 for nice fractions
        denom = max(4, min(10, 3 + difficulty))
        p = self._rng.randint(1, denom - 1) / denom
        q = self._rng.randint(1, denom - 1) / denom
        p = round(p, 4)
        q = round(q, 4)

        # P = [[1-p, p], [q, 1-q]]
        P = [[round(1 - p, 4), p], [q, round(1 - q, 4)]]

        # Steady state: pi1 = q/(p+q), pi2 = p/(p+q)
        total = p + q
        pi1 = round(q / total, 4)
        pi2 = round(p / total, 4)

        problem = f"steady state of P = {P}"
        return problem, {
            "P": P, "p": p, "q": q,
            "pi": [pi1, pi2],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        p, q = sd["p"], sd["q"]
        return [
            f"P = {sd['P']}",
            f"pi*P = pi and pi1 + pi2 = 1",
            f"-{p}*pi1 + {q}*pi2 = 0 => pi1/pi2 = {q}/{p}",
            f"pi1 = {sd['pi'][0]}, pi2 = {sd['pi'][1]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the steady-state distribution.

        Args:
            sd: Solution data.

        Returns:
            Distribution vector string.
        """
        return f"pi = {sd['pi']}"


# ---------------------------------------------------------------------------
# 12. Singular Value Decomposition (tier 6)
# ---------------------------------------------------------------------------

@register
class SingularValueDecompGenerator(StepGenerator):
    """Compute singular values of a 2x2 matrix.

    Computes A^T A, finds its eigenvalues, and takes square roots
    to obtain the singular values sigma_1 >= sigma_2 >= 0.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "singular_value_decomp"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the singular values of A"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SVD singular values problem for a 2x2 matrix.

        Builds A, computes A^T A, finds eigenvalues of A^T A, and
        takes square roots for singular values.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 4)
        A = [[self._rng.randint(-mag, mag) for _ in range(2)]
             for _ in range(2)]
        if all(A[r][c] == 0 for r in range(2) for c in range(2)):
            A[0][0] = 1

        # A^T A
        At = _transpose(A)
        AtA = _mat_mul(At, A)
        AtA = [[round(x, 4) for x in row] for row in AtA]

        # Eigenvalues of AtA (symmetric 2x2)
        a11, a12 = AtA[0][0], AtA[0][1]
        a22 = AtA[1][1]
        tr = a11 + a22
        det_val = a11 * a22 - a12 * a12
        disc = tr * tr - 4 * det_val
        if disc < 0:
            disc = 0.0
        sqrt_disc = math.sqrt(disc)
        eig1 = round((tr + sqrt_disc) / 2, 4)
        eig2 = round((tr - sqrt_disc) / 2, 4)

        # Singular values
        sig1 = round(math.sqrt(max(eig1, 0)), 4)
        sig2 = round(math.sqrt(max(eig2, 0)), 4)
        if sig1 < sig2:
            sig1, sig2 = sig2, sig1

        problem = f"singular values of A = {A}"
        return problem, {
            "A": A, "AtA": AtA,
            "eig1": eig1, "eig2": eig2,
            "sigma1": sig1, "sigma2": sig2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"A^T A = {_fmt_mat(sd['AtA'])}",
            f"eigenvalues of A^T A: {sd['eig1']}, {sd['eig2']}",
            f"sigma1 = sqrt({sd['eig1']}) = {sd['sigma1']}",
            f"sigma2 = sqrt({sd['eig2']}) = {sd['sigma2']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the singular values.

        Args:
            sd: Solution data.

        Returns:
            Singular values string.
        """
        return f"sigma = [{sd['sigma1']}, {sd['sigma2']}]"
