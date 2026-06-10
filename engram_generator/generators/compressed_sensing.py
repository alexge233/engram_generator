"""Compressed sensing generators.

4 generators across tiers 5-6 covering the restricted isometry
property, sparse recovery via matching pursuit, basis pursuit,
and mutual coherence.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class RIPConditionGenerator(StepGenerator):
    """Verify the restricted isometry property for a given matrix.

    Checks (1-delta)*||x||^2 <= ||Ax||^2 <= (1+delta)*||x||^2
    for an s-sparse vector x and measurement matrix A.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rip_condition"

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
        return "verify restricted isometry property"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a RIP verification problem.

        Args:
            difficulty: Controls matrix size and delta precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = min(2 + difficulty // 2, 4)  # rows (measurements)
        n = m + min(1 + difficulty // 2, 3)  # cols (signal dim)
        sparsity = min(1 + difficulty // 3, 3)
        mag = min(2 + difficulty, 5)

        # Measurement matrix
        A = [[round(self._rng.uniform(-1, 1), 4) for _ in range(n)]
             for _ in range(m)]

        # Sparse vector
        x = [0.0] * n
        nonzero_idx = self._rng.sample(range(n), min(sparsity, n))
        for idx in nonzero_idx:
            x[idx] = round(self._rng.uniform(-mag, mag), 4)

        # ||x||^2
        x_norm_sq = round(sum(v * v for v in x), 4)

        # Ax
        Ax = [round(sum(A[i][j] * x[j] for j in range(n)), 4)
              for i in range(m)]

        # ||Ax||^2
        Ax_norm_sq = round(sum(v * v for v in Ax), 4)

        # Compute effective delta
        if x_norm_sq > 1e-12:
            ratio = Ax_norm_sq / x_norm_sq
            delta_lower = round(1.0 - ratio, 4)
            delta_upper = round(ratio - 1.0, 4)
            delta = round(max(abs(delta_lower), abs(delta_upper)), 4)
        else:
            ratio = 0.0
            delta = 0.0

        satisfied = delta <= 1.0

        steps = [
            f"x = {x}, sparsity = {len(nonzero_idx)}",
            f"||x||^2 = {x_norm_sq}",
            f"Ax = {Ax}",
            f"||Ax||^2 = {Ax_norm_sq}",
            f"ratio ||Ax||^2/||x||^2 = {round(ratio, 4)}",
            f"delta = {delta}, RIP satisfied = {satisfied}",
        ]

        problem = f"RIP check: A ({m}x{n}), x {sparsity}-sparse"
        return problem, {
            "delta": delta, "satisfied": satisfied,
            "ratio": round(ratio, 4), "steps_log": steps,
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
            Delta value and whether RIP holds.
        """
        return f"delta={sd['delta']}, RIP={sd['satisfied']}"


@register
class SparseRecoveryGenerator(StepGenerator):
    """Recover a sparse signal using matching pursuit.

    Given y = Ax where x is k-sparse, iteratively finds the column
    of A most correlated with the residual and updates the estimate.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sparse_recovery"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vector_norm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "sparse recovery via matching pursuit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matching pursuit recovery problem.

        Args:
            difficulty: Controls matrix size and sparsity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = min(2 + difficulty // 2, 4)
        n = m + min(1 + difficulty // 2, 3)
        sparsity = min(1 + difficulty // 4, 2)
        n_iter = min(sparsity + difficulty // 3, 3)

        # Create measurement matrix with unit-norm columns
        A = [[round(self._rng.uniform(-1, 1), 4) for _ in range(n)]
             for _ in range(m)]
        # Normalise columns
        for j in range(n):
            col_norm = math.sqrt(sum(A[i][j] ** 2 for i in range(m)))
            if col_norm > 1e-12:
                for i in range(m):
                    A[i][j] = round(A[i][j] / col_norm, 4)

        # True sparse signal
        x_true = [0.0] * n
        nonzero_idx = self._rng.sample(range(n), min(sparsity, n))
        for idx in nonzero_idx:
            x_true[idx] = round(self._rng.uniform(-3, 3), 4)

        # Measurements
        y = [round(sum(A[i][j] * x_true[j] for j in range(n)), 4)
             for i in range(m)]

        # Matching pursuit
        residual = list(y)
        x_est = [0.0] * n
        steps = []

        for it in range(n_iter):
            # Correlations
            corrs = [round(abs(sum(A[i][j] * residual[i]
                                   for i in range(m))), 4)
                     for j in range(n)]
            best_j = max(range(n), key=lambda j: corrs[j])
            proj = round(sum(A[i][best_j] * residual[i]
                             for i in range(m)), 4)
            x_est[best_j] = round(x_est[best_j] + proj, 4)

            # Update residual
            for i in range(m):
                residual[i] = round(residual[i] - proj * A[i][best_j], 4)

            res_norm = round(math.sqrt(sum(r * r for r in residual)), 4)
            steps.append(
                f"iter {it + 1}: best_col={best_j}, proj={proj}, "
                f"||r||={res_norm}"
            )

        problem = f"Matching pursuit: A ({m}x{n}), y={y}"
        return problem, {
            "x_est": [round(v, 4) for v in x_est],
            "x_true": x_true, "steps_log": steps,
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
            Recovered sparse signal estimate.
        """
        return f"x_est = {sd['x_est']}"


@register
class BasisPursuitGenerator(StepGenerator):
    """Find the sparsest solution via basis pursuit.

    Solves min ||x||_1 subject to Ax = y for a small (2x4) system
    by evaluating candidate sparse solutions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "basis_pursuit"

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
        return "basis pursuit L1 minimisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a basis pursuit problem for a 2x4 system.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m, n = 2, 4
        mag = min(1 + difficulty, 4)

        # Create A (2x4)
        A = [[self._rng.randint(-mag, mag) for _ in range(n)]
             for _ in range(m)]

        # Create a 1-sparse true solution
        true_idx = self._rng.randint(0, n - 1)
        x_true = [0.0] * n
        x_true[true_idx] = round(self._rng.uniform(1, mag), 4)

        # y = A * x_true
        y = [round(sum(A[i][j] * x_true[j] for j in range(n)), 4)
             for i in range(m)]

        # Check all pairs of columns for 2x2 subsystems
        best_x = None
        best_l1 = float("inf")
        steps = []
        candidates_checked = 0

        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                # Solve 2x2 system: A[:, [j1,j2]] * c = y
                a11 = A[0][j1]
                a12 = A[0][j2]
                a21 = A[1][j1]
                a22 = A[1][j2]
                det = a11 * a22 - a12 * a21
                if abs(det) < 1e-10:
                    continue
                c1 = round((a22 * y[0] - a12 * y[1]) / det, 4)
                c2 = round((-a21 * y[0] + a11 * y[1]) / det, 4)
                l1 = round(abs(c1) + abs(c2), 4)

                x_cand = [0.0] * n
                x_cand[j1] = c1
                x_cand[j2] = c2

                if l1 < best_l1:
                    best_l1 = l1
                    best_x = list(x_cand)

                candidates_checked += 1
                if candidates_checked <= 4:
                    steps.append(
                        f"cols({j1},{j2}): c=[{c1},{c2}], L1={l1}"
                    )

        if best_x is None:
            best_x = list(x_true)
            best_l1 = round(sum(abs(v) for v in x_true), 4)

        steps.append(f"best L1 = {best_l1}")
        steps.append(f"x* = {best_x}")

        problem = f"Basis pursuit: A={A}, y={y}"
        return problem, {
            "x_opt": best_x, "l1": best_l1, "steps_log": steps,
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
            Optimal solution and its L1 norm.
        """
        return f"x*={sd['x_opt']}, ||x||_1={sd['l1']}"


@register
class CoherenceGenerator(StepGenerator):
    """Compute mutual coherence of a measurement matrix.

    mu(A) = max_{i!=j} |<a_i, a_j>| / (||a_i|| * ||a_j||).
    Also checks recovery guarantee: k < (1 + 1/mu) / 2.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coherence"

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
        return "mutual coherence of measurement matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coherence computation problem.

        Args:
            difficulty: Controls matrix size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = min(2 + difficulty // 2, 4)
        n = m + min(1 + difficulty // 2, 3)
        mag = min(2 + difficulty, 5)

        A = [[round(self._rng.uniform(-mag, mag), 4) for _ in range(n)]
             for _ in range(m)]

        # Compute column norms
        col_norms = []
        for j in range(n):
            cn = math.sqrt(sum(A[i][j] ** 2 for i in range(m)))
            col_norms.append(round(cn, 4) if cn > 1e-12 else 1.0)

        # Compute coherence
        max_coh = 0.0
        max_pair = (0, 1)
        steps = []

        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                dot = sum(A[i][j1] * A[i][j2] for i in range(m))
                coh = abs(dot) / (col_norms[j1] * col_norms[j2])
                coh = round(coh, 4)
                if coh > max_coh:
                    max_coh = coh
                    max_pair = (j1, j2)

        steps.append(f"column norms = {col_norms}")
        steps.append(f"max coherence pair = ({max_pair[0]},{max_pair[1]})")
        steps.append(f"mu(A) = {max_coh}")

        # Recovery guarantee
        if max_coh > 1e-12:
            k_max = (1 + 1.0 / max_coh) / 2
            k_max = round(k_max, 4)
        else:
            k_max = float("inf")
        steps.append(f"recovery guarantee: k < {k_max}")

        problem = f"Coherence of A ({m}x{n})"
        return problem, {
            "mu": max_coh, "k_max": k_max,
            "pair": max_pair, "steps_log": steps,
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
            Coherence value and sparsity bound.
        """
        return f"mu={sd['mu']}, k_max={sd['k_max']}"
