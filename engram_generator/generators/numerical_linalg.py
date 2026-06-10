"""Numerical linear algebra generators.

6 generators across tiers 5-6 covering QR decomposition, SVD,
Cholesky factorisation, Jacobi iteration, Gauss-Seidel, and
least squares.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class QRDecompositionGenerator(StepGenerator):
    """Compute QR decomposition via Gram-Schmidt orthogonalisation.

    Decomposes a 2x2 or 3x2 matrix A into Q (orthonormal columns) and
    R (upper triangular) using the classical Gram-Schmidt process.
    Verifies Q^T * Q = I.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "qr_decomposition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dot_product", "vector_norm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "QR decomposition via Gram-Schmidt"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a QR decomposition problem.

        Args:
            difficulty: Controls matrix size and entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        rows = 3 if difficulty >= 4 else 2
        cols = 2
        mag = min(2 + difficulty, 6)
        A = [[self._rng.randint(-mag, mag) for _ in range(cols)]
             for _ in range(rows)]
        # Ensure columns are not zero or parallel
        while all(A[r][0] == 0 for r in range(rows)):
            A[0][0] = self._rng.randint(1, mag)

        # Gram-Schmidt
        def dot(u, v):
            return sum(a * b for a, b in zip(u, v))

        def norm(u):
            return math.sqrt(dot(u, u))

        def scale(s, u):
            return [s * x for x in u]

        def sub(u, v):
            return [a - b for a, b in zip(u, v)]

        col0 = [A[r][0] for r in range(rows)]
        col1 = [A[r][1] for r in range(rows)]

        u1 = list(col0)
        n1 = norm(u1)
        if n1 < 1e-12:
            u1[0] = 1.0
            n1 = 1.0
        e1 = scale(1.0 / n1, u1)

        proj = dot(col1, e1)
        u2 = sub(col1, scale(proj, e1))
        n2 = norm(u2)
        if n2 < 1e-12:
            u2 = [0.0] * rows
            u2[rows - 1] = 1.0
            n2 = 1.0
        e2 = scale(1.0 / n2, u2)

        r11 = round(n1, 4)
        r12 = round(proj, 4)
        r22 = round(n2, 4)

        Q = [[round(e1[r], 4), round(e2[r], 4)] for r in range(rows)]
        R = [[r11, r12], [0.0, r22]]

        # Verify Q^T Q = I
        qtq00 = round(dot(e1, e1), 4)
        qtq01 = round(dot(e1, e2), 4)
        qtq11 = round(dot(e2, e2), 4)

        steps_log = [
            f"u1 = col0 = {[round(x, 4) for x in col0]}",
            f"||u1|| = {r11}, e1 = {[round(x, 4) for x in e1]}",
            f"proj = <col1,e1> = {r12}",
            f"u2 = col1 - proj*e1 = {[round(x, 4) for x in u2]}",
            f"||u2|| = {r22}, e2 = {[round(x, 4) for x in e2]}",
            f"Q^T*Q diag = [{qtq00},{qtq11}], off = {qtq01}",
        ]

        A_str = str([[A[r][c] for c in range(cols)] for r in range(rows)])
        problem = f"QR decompose A = {A_str}"
        return problem, {
            "Q": Q, "R": R, "steps_log": steps_log,
            "qtq00": qtq00, "qtq01": qtq01, "qtq11": qtq11,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Q and R matrices as a string.
        """
        return f"Q={sd['Q']}, R={sd['R']}"


@register
class SVDComputeGenerator(StepGenerator):
    """Compute singular value decomposition of a 2x2 matrix.

    Finds A = U * S * V^T by computing eigenvalues of A^T * A to
    obtain singular values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "svd_compute"

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
            Short task description.
        """
        return "SVD of a 2x2 matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SVD problem for a 2x2 matrix.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 5)
        A = [[self._rng.randint(-mag, mag) for _ in range(2)] for _ in range(2)]

        # A^T * A
        AtA = [[0.0, 0.0], [0.0, 0.0]]
        for i in range(2):
            for j in range(2):
                AtA[i][j] = sum(A[r][i] * A[r][j] for r in range(2))

        # Eigenvalues of 2x2 symmetric matrix
        tr = AtA[0][0] + AtA[1][1]
        det = AtA[0][0] * AtA[1][1] - AtA[0][1] * AtA[1][0]
        disc = tr * tr - 4 * det
        disc = max(disc, 0.0)
        lam1 = (tr + math.sqrt(disc)) / 2
        lam2 = (tr - math.sqrt(disc)) / 2
        lam1 = max(lam1, 0.0)
        lam2 = max(lam2, 0.0)

        s1 = round(math.sqrt(lam1), 4)
        s2 = round(math.sqrt(lam2), 4)

        steps_log = [
            f"A^T*A = {[[round(AtA[i][j], 4) for j in range(2)] for i in range(2)]}",
            f"tr = {round(tr, 4)}, det = {round(det, 4)}",
            f"disc = {round(disc, 4)}",
            f"eigenvalues: lam1={round(lam1, 4)}, lam2={round(lam2, 4)}",
            f"sigma1={s1}, sigma2={s2}",
        ]

        problem = f"SVD of A = {A}"
        return problem, {"A": A, "s1": s1, "s2": s2, "steps_log": steps_log}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Singular values as a string.
        """
        return f"sigma = [{sd['s1']}, {sd['s2']}]"


@register
class CholeskyFactorGenerator(StepGenerator):
    """Compute the Cholesky factorisation of a symmetric positive definite matrix.

    Factors A = L * L^T where L is lower triangular. Uses the formula
    L_{ij} = (A_{ij} - sum_k L_{ik} * L_{jk}) / L_{jj} for 2x2 or 3x3.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cholesky_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gaussian_elimination"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Cholesky factorisation A = LL^T"

    def _build_spd(self, n: int, mag: int) -> list[list[int]]:
        """Build a symmetric positive definite matrix.

        Args:
            n: Matrix dimension.
            mag: Maximum magnitude of entries in the generating matrix.

        Returns:
            An n x n SPD matrix with integer entries.
        """
        # Generate B and compute A = B^T * B + n*I to ensure SPD
        B = [[self._rng.randint(-mag, mag) for _ in range(n)] for _ in range(n)]
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = sum(B[r][i] * B[r][j] for r in range(n))
                if i == j:
                    A[i][j] += n
        return A

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Cholesky factorisation problem.

        Args:
            difficulty: Controls matrix size and entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3 if difficulty >= 5 else 2
        mag = min(1 + difficulty // 2, 3)
        A = self._build_spd(n, mag)

        L = [[0.0] * n for _ in range(n)]
        steps_log = []
        for i in range(n):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    val = math.sqrt(max(A[i][i] - s, 0.0))
                    L[i][j] = round(val, 4)
                    steps_log.append(
                        f"L[{i}][{j}] = sqrt(A[{i}][{i}] - {round(s, 4)}) "
                        f"= {L[i][j]}"
                    )
                else:
                    denom = L[j][j] if abs(L[j][j]) > 1e-12 else 1.0
                    val = (A[i][j] - s) / denom
                    L[i][j] = round(val, 4)
                    steps_log.append(
                        f"L[{i}][{j}] = (A[{i}][{j}] - {round(s, 4)}) "
                        f"/ L[{j}][{j}] = {L[i][j]}"
                    )

        problem = f"Cholesky factor A = {A}"
        return problem, {"A": A, "L": L, "steps_log": steps_log}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Lower triangular factor L as a string.
        """
        return f"L = {sd['L']}"


@register
class JacobiIterationGenerator(StepGenerator):
    """Solve a linear system Ax = b using Jacobi iteration.

    Updates x_i^{new} = (b_i - sum_{j!=i} A_{ij} * x_j) / A_{ii}
    for 3-5 iterations on a diagonally dominant 2x2 or 3x3 system.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jacobi_iteration"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Jacobi iteration for Ax = b"

    def _build_diag_dominant(self, n: int, mag: int) -> tuple[list[list[int]], list[int]]:
        """Build a diagonally dominant system Ax = b.

        Args:
            n: System dimension.
            mag: Off-diagonal entry magnitude.

        Returns:
            Tuple of (A, b) with integer entries.
        """
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            row_sum = 0
            for j in range(n):
                if i != j:
                    A[i][j] = self._rng.randint(-mag, mag)
                    row_sum += abs(A[i][j])
            A[i][i] = row_sum + self._rng.randint(1, 3)
        b = [self._rng.randint(1, 5 * mag) for _ in range(n)]
        return A, b

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Jacobi iteration problem.

        Args:
            difficulty: Controls system size and iteration count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3 if difficulty >= 5 else 2
        mag = min(1 + difficulty, 4)
        A, b = self._build_diag_dominant(n, mag)
        n_iter = min(3 + difficulty // 2, 5)

        x = [0.0] * n
        trace = [f"x0 = {[round(v, 4) for v in x]}"]
        for it in range(n_iter):
            x_new = [0.0] * n
            for i in range(n):
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x_new[i] = round((b[i] - s) / A[i][i], 4)
            x = x_new
            trace.append(f"x{it + 1} = {[round(v, 4) for v in x]}")

        problem = f"Jacobi: A={A}, b={b}, {n_iter} iterations"
        return problem, {"trace": trace, "final": x}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Final iterate as a string.
        """
        return f"x = {[round(v, 4) for v in sd['final']]}"


@register
class GaussSeidelGenerator(StepGenerator):
    """Solve a linear system Ax = b using Gauss-Seidel iteration.

    Like Jacobi but uses updated values immediately within each
    iteration, giving faster convergence. Runs 3-5 iterations on
    a diagonally dominant 2x2 or 3x3 system.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gauss_seidel"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["jacobi_iteration"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Gauss-Seidel iteration for Ax = b"

    def _build_diag_dominant(self, n: int, mag: int) -> tuple[list[list[int]], list[int]]:
        """Build a diagonally dominant system Ax = b.

        Args:
            n: System dimension.
            mag: Off-diagonal entry magnitude.

        Returns:
            Tuple of (A, b) with integer entries.
        """
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            row_sum = 0
            for j in range(n):
                if i != j:
                    A[i][j] = self._rng.randint(-mag, mag)
                    row_sum += abs(A[i][j])
            A[i][i] = row_sum + self._rng.randint(1, 3)
        b = [self._rng.randint(1, 5 * mag) for _ in range(n)]
        return A, b

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gauss-Seidel iteration problem.

        Args:
            difficulty: Controls system size and iteration count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3 if difficulty >= 5 else 2
        mag = min(1 + difficulty, 4)
        A, b = self._build_diag_dominant(n, mag)
        n_iter = min(3 + difficulty // 2, 5)

        x = [0.0] * n
        trace = [f"x0 = {[round(v, 4) for v in x]}"]
        for it in range(n_iter):
            for i in range(n):
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x[i] = round((b[i] - s) / A[i][i], 4)
            trace.append(f"x{it + 1} = {[round(v, 4) for v in x]}")

        problem = f"Gauss-Seidel: A={A}, b={b}, {n_iter} iterations"
        return problem, {"trace": trace, "final": list(x)}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Final iterate as a string.
        """
        return f"x = {[round(v, 4) for v in sd['final']]}"


@register
class LeastSquaresGenerator(StepGenerator):
    """Solve an overdetermined system via the normal equations.

    Computes x = (A^T * A)^{-1} * A^T * b for an overdetermined
    3x2 system, then computes the residual ||Ax - b||.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "least_squares"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "least squares via normal equations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a least squares problem.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 5)
        A = [[self._rng.randint(-mag, mag) for _ in range(2)]
             for _ in range(3)]
        b = [self._rng.randint(-mag, mag) for _ in range(3)]

        # A^T * A (2x2)
        AtA = [[0.0, 0.0], [0.0, 0.0]]
        for i in range(2):
            for j in range(2):
                AtA[i][j] = sum(A[r][i] * A[r][j] for r in range(3))

        # A^T * b (2x1)
        Atb = [sum(A[r][i] * b[r] for r in range(3)) for i in range(2)]

        # Invert 2x2: [[a,b],[c,d]] -> 1/det * [[d,-b],[-c,a]]
        det = AtA[0][0] * AtA[1][1] - AtA[0][1] * AtA[1][0]
        if abs(det) < 1e-10:
            # Ensure non-singular by adjusting diagonal
            AtA[0][0] += 1
            AtA[1][1] += 1
            A[0][0] += 1
            A[2][1] += 1
            for i in range(2):
                for j in range(2):
                    AtA[i][j] = sum(A[r][i] * A[r][j] for r in range(3))
            Atb = [sum(A[r][i] * b[r] for r in range(3)) for i in range(2)]
            det = AtA[0][0] * AtA[1][1] - AtA[0][1] * AtA[1][0]

        inv = [[AtA[1][1] / det, -AtA[0][1] / det],
               [-AtA[1][0] / det, AtA[0][0] / det]]

        x_sol = [round(inv[i][0] * Atb[0] + inv[i][1] * Atb[1], 4)
                 for i in range(2)]

        # Residual
        Ax = [round(sum(A[r][j] * x_sol[j] for j in range(2)), 4)
              for r in range(3)]
        residual = round(math.sqrt(sum((Ax[r] - b[r]) ** 2
                                       for r in range(3))), 4)

        steps_log = [
            f"A^T*A = {[[round(AtA[i][j], 4) for j in range(2)] for i in range(2)]}",
            f"A^T*b = {[round(v, 4) for v in Atb]}",
            f"det(A^T*A) = {round(det, 4)}",
            f"x = {x_sol}",
            f"residual ||Ax-b|| = {residual}",
        ]

        problem = f"Least squares: A={A}, b={b}"
        return problem, {
            "x": x_sol, "residual": residual, "steps_log": steps_log,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Solution vector and residual as a string.
        """
        return f"x={sd['x']}, residual={sd['residual']}"
