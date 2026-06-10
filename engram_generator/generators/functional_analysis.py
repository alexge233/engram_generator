"""Functional analysis generators for tiers 5-7.

10 generators covering norms, Banach spaces, inner products, orthogonal
projections, adjoint operators, spectral decomposition, compact
operators, dual spaces, Hahn-Banach, and Riesz representation. Each
generator produces step-by-step solutions with LaTeX formatting.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ───────────────────────────────────────────────


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


def _vec_str(v: list[float]) -> str:
    """Format a vector as a parenthesised comma-separated string.

    Args:
        v: Vector components.

    Returns:
        Formatted vector string.
    """
    return "(" + ", ".join(_fmt(x) for x in v) + ")"


def _mat_str(m: list[list[float]]) -> str:
    """Format a matrix as a bracketed row-list string.

    Args:
        m: Matrix as list of rows.

    Returns:
        Formatted matrix string.
    """
    rows = [_vec_str(row) for row in m]
    return "[" + "; ".join(rows) + "]"


# ── Helper classes ───────────────────────────────────────────────────


class Vector:
    """A finite-dimensional real vector.

    Attributes:
        components: List of float components.
    """

    def __init__(self, components: list[float]) -> None:
        """Initialise the vector.

        Args:
            components: List of float components.
        """
        self._components = list(components)

    @property
    def dim(self) -> int:
        """Return the dimension."""
        return len(self._components)

    @property
    def components(self) -> list[float]:
        """Return the components."""
        return list(self._components)

    def l1_norm(self) -> float:
        """Compute the L1 norm.

        Returns:
            Sum of absolute values.
        """
        return sum(abs(x) for x in self._components)

    def l2_norm(self) -> float:
        """Compute the L2 (Euclidean) norm.

        Returns:
            Square root of sum of squares.
        """
        return math.sqrt(sum(x ** 2 for x in self._components))

    def linf_norm(self) -> float:
        """Compute the L-infinity norm.

        Returns:
            Maximum absolute value.
        """
        return max(abs(x) for x in self._components)

    def dot(self, other: "Vector") -> float:
        """Compute the dot product with another vector.

        Args:
            other: Another vector of the same dimension.

        Returns:
            Dot product value.
        """
        return sum(a * b for a, b in zip(self._components, other._components))

    def scale(self, c: float) -> "Vector":
        """Scale the vector by a constant.

        Args:
            c: Scalar multiplier.

        Returns:
            New scaled vector.
        """
        return Vector([c * x for x in self._components])

    def add(self, other: "Vector") -> "Vector":
        """Add another vector.

        Args:
            other: Another vector.

        Returns:
            New sum vector.
        """
        return Vector([a + b for a, b in zip(self._components, other._components)])

    def latex(self) -> str:
        """Format as LaTeX column vector.

        Returns:
            LaTeX string.
        """
        return _vec_str(self._components)


class Matrix:
    """A finite-dimensional real matrix.

    Attributes:
        rows: List of row vectors as lists of floats.
    """

    def __init__(self, rows: list[list[float]]) -> None:
        """Initialise the matrix.

        Args:
            rows: List of rows, each a list of floats.
        """
        self._rows = [list(r) for r in rows]
        self._n = len(rows)
        self._m = len(rows[0]) if rows else 0

    @property
    def shape(self) -> tuple[int, int]:
        """Return (rows, cols)."""
        return self._n, self._m

    @property
    def rows(self) -> list[list[float]]:
        """Return the matrix rows."""
        return [list(r) for r in self._rows]

    def entry(self, i: int, j: int) -> float:
        """Get entry at (i, j).

        Args:
            i: Row index (0-based).
            j: Column index (0-based).

        Returns:
            Matrix entry.
        """
        return self._rows[i][j]

    def transpose(self) -> "Matrix":
        """Compute the transpose.

        Returns:
            Transposed matrix.
        """
        return Matrix([[self._rows[i][j] for i in range(self._n)]
                       for j in range(self._m)])

    def mat_vec(self, v: Vector) -> Vector:
        """Multiply matrix by vector.

        Args:
            v: Input vector.

        Returns:
            Result vector.
        """
        return Vector([sum(self._rows[i][j] * v.components[j]
                           for j in range(self._m))
                       for i in range(self._n)])

    def trace(self) -> float:
        """Compute the trace.

        Returns:
            Sum of diagonal entries.
        """
        return sum(self._rows[i][i] for i in range(min(self._n, self._m)))

    def latex(self) -> str:
        """Format as a compact string.

        Returns:
            Matrix string.
        """
        return _mat_str(self._rows)


# ── 1. Norm compute (tier 5) ────────────────────────────────────────


@register
class NormComputeGenerator(StepGenerator):
    """Compute L1, L2, and L-infinity norms of a vector and compare.

    Given a vector in R^n, computes all three standard norms and
    identifies which is largest and smallest, verifying the norm
    inequality chain L_inf <= L_2 <= L_1.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "norm_compute"

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
            Task description string.
        """
        return "compute L1, L2, L-infinity norms of vector"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a norm computation problem.

        Args:
            difficulty: Controls vector dimension and component range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(5, 1 + difficulty))
        bound = 1 + difficulty
        components = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        v = Vector(components)

        l1 = round(v.l1_norm(), 4)
        l2 = round(v.l2_norm(), 4)
        linf = round(v.linf_norm(), 4)

        problem = f"v = {v.latex()}"
        return problem, {
            "v": v, "l1": l1, "l2": l2, "linf": linf,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate norm computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"||v||_1 = {_fmt(sd['l1'])}",
            f"||v||_2 = {_fmt(sd['l2'])}",
            f"||v||_inf = {_fmt(sd['linf'])}",
            f"inequality: {_fmt(sd['linf'])} <= {_fmt(sd['l2'])} <= {_fmt(sd['l1'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return all three norms.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"L1={_fmt(sd['l1'])}, L2={_fmt(sd['l2'])}, Linf={_fmt(sd['linf'])}"


# ── 2. Banach space check (tier 6) ──────────────────────────────────


@register
class BanachSpaceCheckGenerator(StepGenerator):
    """Verify completeness by checking if a Cauchy sequence converges.

    Given a sequence in a normed space, verifies the Cauchy property
    and finds the limit. Uses sequences in R^n with explicit terms.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "banach_space_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cauchy_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify Cauchy sequence converges in normed space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Banach space completeness check problem.

        Constructs a Cauchy sequence x_n = L + c/n^p in R^d and asks
        whether it converges and to what limit.

        Args:
            difficulty: Controls dimension and sequence parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        d = self._rng.randint(1, min(3, difficulty))
        p = self._rng.randint(1, min(2, difficulty))

        limit_comps = [float(self._rng.randint(-3, 3)) for _ in range(d)]
        c_comps = [float(self._rng.randint(1, 3)) for _ in range(d)]

        # x_n = limit + c/n^p
        n_check = self._rng.randint(5, 10)
        xn_comps = [round(limit_comps[i] + c_comps[i] / n_check ** p, 4)
                    for i in range(d)]

        limit_v = Vector(limit_comps)
        xn_v = Vector(xn_comps)
        diff_norm = round(Vector([c_comps[i] / n_check ** p for i in range(d)]).l2_norm(), 4)

        limit_str = _vec_str(limit_comps)
        c_str = _vec_str(c_comps)
        problem = f"x_n = {limit_str} + {c_str}/n^{{{p}}} in R^{{{d}}}"
        return problem, {
            "d": d, "p": p,
            "limit": limit_comps, "c": c_comps,
            "n_check": n_check, "xn": xn_comps,
            "diff_norm": diff_norm,
            "is_cauchy": True, "converges": True,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate completeness verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"x_n in R^{sd['d']}, perturbation O(1/n^{sd['p']})",
            f"||x_n - L|| at n={sd['n_check']}: {_fmt(sd['diff_norm'])}",
            f"||x_n - L|| -> 0 as n -> inf",
            f"limit = {_vec_str(sd['limit'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return convergence result.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"converges to {_vec_str(sd['limit'])}"


# ── 3. Inner product verify (tier 5) ────────────────────────────────


@register
class InnerProductVerifyGenerator(StepGenerator):
    """Compute inner product and verify axioms.

    Computes <x, y>, then checks linearity in the first argument,
    symmetry, and positive definiteness on concrete vectors.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inner_product_verify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dot_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute inner product and verify axioms"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inner product verification problem.

        Constructs two vectors and a scalar, computes the inner product,
        and verifies linearity, symmetry, and positive definiteness.

        Args:
            difficulty: Controls dimension and component range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(4, 1 + difficulty))
        bound = 1 + difficulty
        x_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        y_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        alpha = float(self._rng.randint(1, 3))

        x = Vector(x_comps)
        y = Vector(y_comps)

        ip_xy = round(x.dot(y), 4)
        ip_yx = round(y.dot(x), 4)
        ip_xx = round(x.dot(x), 4)
        ax = x.scale(alpha)
        ip_ax_y = round(ax.dot(y), 4)

        problem = f"x={x.latex()}, y={y.latex()}, \\alpha={_fmt(alpha)}"
        return problem, {
            "x": x, "y": y, "alpha": alpha,
            "ip_xy": ip_xy, "ip_yx": ip_yx,
            "ip_xx": ip_xx, "ip_ax_y": ip_ax_y,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate inner product verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"<x,y> = {_fmt(sd['ip_xy'])}",
            f"<y,x> = {_fmt(sd['ip_yx'])} (symmetry: {'yes' if abs(sd['ip_xy'] - sd['ip_yx']) < 1e-8 else 'no'})",
            f"<{_fmt(sd['alpha'])}x, y> = {_fmt(sd['ip_ax_y'])} = {_fmt(sd['alpha'])}*{_fmt(sd['ip_xy'])} (linearity: yes)",
            f"<x,x> = {_fmt(sd['ip_xx'])} >= 0 (positive definite: yes)",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the inner product value and axiom verification.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"<x,y>={_fmt(sd['ip_xy'])}, all axioms hold"


# ── 4. Orthogonal projection (tier 6) ───────────────────────────────


@register
class OrthogonalProjectionGenerator(StepGenerator):
    """Project a vector onto a subspace spanned by orthogonal vectors.

    Uses the formula proj_W(v) = sum(<v,w_i>/<w_i,w_i> * w_i) for an
    orthogonal basis {w_1, ..., w_k} of W.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "orthogonal_projection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["inner_product_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute orthogonal projection onto subspace"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an orthogonal projection problem.

        Creates a vector v and one or two orthogonal basis vectors for
        the subspace. Computes the projection using the formula.

        Args:
            difficulty: Controls dimension and number of basis vectors.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(4, 1 + difficulty))
        bound = 1 + min(4, difficulty)
        v_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        v = Vector(v_comps)

        # Generate orthogonal basis vectors
        if difficulty <= 4 or n < 3:
            # Single basis vector
            w_comps = [float(self._rng.randint(-3, 3)) for _ in range(n)]
            if all(c == 0 for c in w_comps):
                w_comps[0] = 1.0
            basis = [Vector(w_comps)]
        else:
            # Two orthogonal vectors via Gram-Schmidt on random vectors
            w1_comps = [float(self._rng.randint(-3, 3)) for _ in range(n)]
            if all(c == 0 for c in w1_comps):
                w1_comps[0] = 1.0
            w1 = Vector(w1_comps)

            u2_comps = [float(self._rng.randint(-3, 3)) for _ in range(n)]
            u2 = Vector(u2_comps)
            # Gram-Schmidt: w2 = u2 - <u2,w1>/<w1,w1> * w1
            coeff = u2.dot(w1) / w1.dot(w1) if w1.dot(w1) > 1e-10 else 0.0
            w2 = u2.add(w1.scale(-coeff))
            if w2.l2_norm() < 1e-10:
                w2_c = [0.0] * n
                w2_c[1 if n > 1 else 0] = 1.0
                w2 = Vector(w2_c)
            basis = [w1, w2]

        # Compute projection
        proj_comps = [0.0] * n
        coeffs: list[float] = []
        for w in basis:
            ww = w.dot(w)
            if ww < 1e-10:
                coeffs.append(0.0)
                continue
            c = round(v.dot(w) / ww, 4)
            coeffs.append(c)
            scaled = w.scale(c)
            proj_comps = [round(proj_comps[i] + scaled.components[i], 4) for i in range(n)]

        proj = Vector(proj_comps)
        basis_strs = ", ".join(f"w_{i+1}={w.latex()}" for i, w in enumerate(basis))
        problem = f"proj_W(v), v={v.latex()}, {basis_strs}"
        return problem, {
            "v": v, "basis": basis, "coeffs": coeffs, "proj": proj,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate projection computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = []
        for i, (w, c) in enumerate(zip(sd["basis"], sd["coeffs"])):
            vw = round(sd["v"].dot(w), 4)
            ww = round(w.dot(w), 4)
            steps.append(f"<v,w_{i+1}>={_fmt(vw)}, <w_{i+1},w_{i+1}>={_fmt(ww)}, coeff={_fmt(c)}")
        steps.append(f"proj = {sd['proj'].latex()}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the projection vector.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"proj={sd['proj'].latex()}"


# ── 5. Adjoint operator (tier 6) ────────────────────────────────────


@register
class AdjointOperatorGenerator(StepGenerator):
    """Compute the adjoint A* of a real matrix and verify <Ax,y>=<x,A*y>.

    For real matrices, A* = A^T. Verifies the identity with concrete
    vectors x, y.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adjoint_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_transpose"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute adjoint operator and verify inner product identity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an adjoint operator problem.

        Creates a matrix A, computes A^T, and verifies <Ax,y> = <x,A^Ty>
        with random vectors x, y.

        Args:
            difficulty: Controls matrix dimension and entry range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(3, 1 + difficulty))
        bound = 1 + min(3, difficulty)
        rows = [[float(self._rng.randint(-bound, bound)) for _ in range(n)]
                for _ in range(n)]
        mat = Matrix(rows)
        adj = mat.transpose()

        x_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        y_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]
        x = Vector(x_comps)
        y = Vector(y_comps)

        ax = mat.mat_vec(x)
        at_y = adj.mat_vec(y)

        ip_ax_y = round(ax.dot(y), 4)
        ip_x_aty = round(x.dot(at_y), 4)

        problem = f"A={mat.latex()}, x={x.latex()}, y={y.latex()}"
        return problem, {
            "mat": mat, "adj": adj, "x": x, "y": y,
            "ax": ax, "at_y": at_y,
            "ip_ax_y": ip_ax_y, "ip_x_aty": ip_x_aty,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate adjoint computation and verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        verified = abs(sd["ip_ax_y"] - sd["ip_x_aty"]) < 1e-6
        return [
            f"A* = A^T = {sd['adj'].latex()}",
            f"Ax = {sd['ax'].latex()}",
            f"A*y = {sd['at_y'].latex()}",
            f"<Ax,y> = {_fmt(sd['ip_ax_y'])}",
            f"<x,A*y> = {_fmt(sd['ip_x_aty'])}",
            f"identity holds: {'yes' if verified else 'no'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the adjoint and identity verification.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"A*={sd['adj'].latex()}, <Ax,y>=<x,A*y>={_fmt(sd['ip_ax_y'])}"


# ── 6. Spectral decomposition (tier 6) ──────────────────────────────


@register
class SpectralDecompositionGenerator(StepGenerator):
    """Decompose a symmetric matrix A = P*D*P^T using eigenvalues.

    Constructs a 2x2 symmetric matrix with known eigenvalues, computes
    eigenvectors, and writes the spectral decomposition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectral_decomposition"

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
            Task description string.
        """
        return "decompose symmetric matrix A = P D P^T"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectral decomposition problem.

        Constructs a 2x2 symmetric matrix from known eigenvalues and
        a rotation angle, then asks for the decomposition.

        Args:
            difficulty: Controls eigenvalue range and angle.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lam1 = float(self._rng.randint(-3, 3 + difficulty))
        lam2 = float(self._rng.randint(-3, 3 + difficulty))
        while lam2 == lam1:
            lam2 = float(self._rng.randint(-3, 3 + difficulty))

        # Rotation angle for eigenvector matrix
        angle_choices = [math.pi / 6, math.pi / 4, math.pi / 3]
        theta = self._rng.choice(angle_choices)

        c = math.cos(theta)
        s = math.sin(theta)

        # A = P D P^T where P = [[c, -s], [s, c]]
        a11 = round(lam1 * c ** 2 + lam2 * s ** 2, 4)
        a12 = round((lam1 - lam2) * c * s, 4)
        a22 = round(lam1 * s ** 2 + lam2 * c ** 2, 4)

        mat = Matrix([[a11, a12], [a12, a22]])
        p_mat = Matrix([[round(c, 4), round(-s, 4)],
                        [round(s, 4), round(c, 4)]])
        d_mat = Matrix([[lam1, 0.0], [0.0, lam2]])

        problem = f"A = {mat.latex()}"
        return problem, {
            "mat": mat, "p_mat": p_mat, "d_mat": d_mat,
            "lam1": lam1, "lam2": lam2, "theta": theta,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate spectral decomposition steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        tr = round(sd["lam1"] + sd["lam2"], 4)
        det = round(sd["lam1"] * sd["lam2"], 4)
        return [
            f"trace = {_fmt(tr)}, det = {_fmt(det)}",
            f"eigenvalues: {_fmt(sd['lam1'])}, {_fmt(sd['lam2'])}",
            f"P = {sd['p_mat'].latex()}",
            f"D = {sd['d_mat'].latex()}",
            f"A = P D P^T",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the eigenvalues and eigenvector matrix.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"lam1={_fmt(sd['lam1'])}, lam2={_fmt(sd['lam2'])}, P={sd['p_mat'].latex()}"


# ── 7. Compact operator (tier 7) ────────────────────────────────────


@register
class CompactOperatorGenerator(StepGenerator):
    """Verify compactness of a finite-dimensional linear operator.

    For a finite-dimensional operator, shows that the image of the unit
    ball is bounded and closed (hence compact in finite dimensions).
    Demonstrates by showing a bounded sequence in the domain maps to a
    sequence with a convergent subsequence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compact_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["spectral_decomposition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify operator compactness in finite dimensions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compact operator verification problem.

        Constructs a 2x2 matrix and a bounded sequence, maps the
        sequence, and shows the image has a convergent subsequence.

        Args:
            difficulty: Controls matrix entries and sequence.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        bound = 1 + min(3, difficulty)
        rows = [[float(self._rng.randint(-bound, bound)) for _ in range(2)]
                for _ in range(2)]
        mat = Matrix(rows)

        # Bounded sequence: x_k = (cos(k), sin(k)) on the unit circle
        n_terms = self._rng.randint(3, min(5, 2 + difficulty))
        seq_inputs: list[list[float]] = []
        seq_outputs: list[list[float]] = []

        for k in range(1, n_terms + 1):
            xk = Vector([round(math.cos(k), 4), round(math.sin(k), 4)])
            axk = mat.mat_vec(xk)
            seq_inputs.append(xk.components)
            seq_outputs.append([round(c, 4) for c in axk.components])

        # Compute operator norm bound (max singular value approximation)
        max_output_norm = max(
            math.sqrt(sum(c ** 2 for c in out)) for out in seq_outputs
        )

        problem = f"A = {mat.latex()}, x_k on unit circle"
        return problem, {
            "mat": mat, "n_terms": n_terms,
            "seq_inputs": seq_inputs, "seq_outputs": seq_outputs,
            "max_norm": round(max_output_norm, 4),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate compactness verification steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [
            f"A maps unit ball to bounded set",
            f"||Ax_k|| <= {_fmt(sd['max_norm'])} for all k",
        ]
        for k in range(min(3, sd["n_terms"])):
            steps.append(f"Ax_{k+1} = {_vec_str(sd['seq_outputs'][k])}")
        steps.append("bounded in R^2 => has convergent subsequence")
        steps.append("operator is compact (finite-dim)")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return compactness verdict.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return "compact (finite-dimensional operator)"


# ── 8. Dual space (tier 6) ──────────────────────────────────────────


@register
class DualSpaceGenerator(StepGenerator):
    """Compute the dual basis for R^n.

    Given a basis {e_1, ..., e_n} for R^n, finds the dual basis
    {e_1*, ..., e_n*} such that e_i*(e_j) = delta_{ij}. For the
    standard basis this is trivial; for non-standard bases it requires
    computing the inverse of the basis matrix.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dual_space"

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
            Task description string.
        """
        return "compute dual basis for R^n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dual basis computation problem.

        For low difficulty uses the standard basis. For higher difficulty
        uses a non-standard basis and computes the dual via matrix inverse.

        Args:
            difficulty: Controls basis complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(3, 1 + difficulty))

        if difficulty <= 3:
            return self._standard_basis(n)
        return self._nonstandard_basis(n, difficulty)

    def _standard_basis(self, n: int) -> tuple[str, dict]:
        """Generate a standard basis dual problem.

        Args:
            n: Dimension.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        basis: list[list[float]] = []
        for i in range(n):
            e = [0.0] * n
            e[i] = 1.0
            basis.append(e)

        # Dual basis = same as primal for standard basis
        problem = f"standard basis in R^{n}"
        return problem, {
            "n": n, "basis": basis, "dual": basis,
            "is_standard": True,
        }

    def _nonstandard_basis(self, n: int, difficulty: int) -> tuple[str, dict]:
        """Generate a non-standard basis dual problem.

        Uses a 2x2 basis matrix with integer entries and computes its
        inverse as the dual basis rows.

        Args:
            n: Dimension (2 or 3).
            difficulty: Controls entry range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        # For simplicity, use 2D with guaranteed invertible matrix
        for _ in range(50):
            rows = [[float(self._rng.randint(-3, 3)) for _ in range(2)]
                    for _ in range(2)]
            det = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
            if abs(det) >= 0.5:
                break
        else:
            rows = [[1.0, 0.0], [0.0, 1.0]]
            det = 1.0

        # Inverse: dual basis rows
        inv = [[round(rows[1][1] / det, 4), round(-rows[0][1] / det, 4)],
               [round(-rows[1][0] / det, 4), round(rows[0][0] / det, 4)]]

        basis_strs = ", ".join(f"e_{i+1}={_vec_str(rows[i])}" for i in range(2))
        problem = f"basis: {basis_strs}"
        return problem, {
            "n": 2, "basis": rows, "dual": inv,
            "is_standard": False, "det": det,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate dual basis computation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = []
        if sd["is_standard"]:
            steps.append("standard basis: dual = primal")
        else:
            steps.append(f"basis matrix B, det(B) = {_fmt(sd['det'])}")
            steps.append("dual basis = rows of B^{-1}")

        for i in range(sd["n"]):
            steps.append(f"e_{i+1}* = {_vec_str(sd['dual'][i])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the dual basis vectors.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        parts = [f"e_{i+1}*={_vec_str(sd['dual'][i])}" for i in range(sd["n"])]
        return ", ".join(parts)


# ── 9. Hahn-Banach application (tier 7) ─────────────────────────────


@register
class HahnBanachApplyGenerator(StepGenerator):
    """Apply the Hahn-Banach theorem to extend a functional.

    Given a functional defined on a subspace W of R^n, extends it to
    the full space while preserving the norm bound. Uses template-based
    problems with explicit computations in finite dimensions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hahn_banach_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dual_space"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply Hahn-Banach to extend functional from subspace"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hahn-Banach extension problem.

        Creates a functional on a 1D subspace of R^2 or R^3 and asks
        to extend it to the full space preserving the norm.

        Args:
            difficulty: Controls dimension and functional complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 4:
            return self._r2_extension(difficulty)
        return self._r3_extension(difficulty)

    def _r2_extension(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hahn-Banach problem in R^2.

        Subspace W = span{w}, functional f(alpha*w) = alpha*c.
        Extension: find f on R^2 with ||f|| = |c|/||w||.

        Args:
            difficulty: Controls component range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        w_comps = [float(self._rng.randint(1, 2 + difficulty)),
                    float(self._rng.randint(1, 2 + difficulty))]
        w = Vector(w_comps)
        c = float(self._rng.randint(1, 3))

        w_norm = w.l2_norm()
        func_norm = round(c / w_norm, 4)

        # Extension: f(x) = c * <x, w> / <w, w>
        ww = w.dot(w)
        rep_comps = [round(c * w_comps[i] / ww, 4) for i in range(2)]

        problem = (
            f"W = \\text{{span}}\\{{{w.latex()}\\}}, "
            f"f(\\alpha w) = {_fmt(c)}\\alpha"
        )
        return problem, {
            "dim": 2, "w": w, "c": c,
            "func_norm": func_norm, "rep": rep_comps,
            "w_norm": round(w_norm, 4),
        }

    def _r3_extension(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hahn-Banach problem in R^3.

        Args:
            difficulty: Controls component range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        w_comps = [float(self._rng.randint(1, 2 + difficulty)),
                    float(self._rng.randint(1, 2 + difficulty)),
                    float(self._rng.randint(1, 2 + difficulty))]
        w = Vector(w_comps)
        c = float(self._rng.randint(1, 3))

        w_norm = w.l2_norm()
        func_norm = round(c / w_norm, 4)

        ww = w.dot(w)
        rep_comps = [round(c * w_comps[i] / ww, 4) for i in range(3)]

        problem = (
            f"W = \\text{{span}}\\{{{w.latex()}\\}}, "
            f"f(\\alpha w) = {_fmt(c)}\\alpha"
        )
        return problem, {
            "dim": 3, "w": w, "c": c,
            "func_norm": func_norm, "rep": rep_comps,
            "w_norm": round(w_norm, 4),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Hahn-Banach extension steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        return [
            f"||w|| = {_fmt(sd['w_norm'])}",
            f"||f||_W = |c|/||w|| = {_fmt(sd['func_norm'])}",
            "Hahn-Banach: exists extension F with ||F|| = ||f||_W",
            f"representing vector: y = {_vec_str(sd['rep'])}",
            f"F(x) = <x, y>, ||F|| = ||y|| = {_fmt(sd['func_norm'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the extended functional.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"F(x)=<x,{_vec_str(sd['rep'])}>, ||F||={_fmt(sd['func_norm'])}"


# ── 10. Riesz representation (tier 7) ───────────────────────────────


@register
class RieszRepresentationGenerator(StepGenerator):
    """Find the representing element via the Riesz representation theorem.

    Given a bounded linear functional f on a Hilbert space, finds the
    unique y such that f(x) = <x, y> for all x. Computes y from the
    functional's values on the standard basis.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "riesz_representation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["inner_product_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find representing element via Riesz representation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Riesz representation problem.

        Defines a functional by its values on the standard basis
        f(e_i) = y_i, then the representing element is y = (y_1,...,y_n).

        Args:
            difficulty: Controls dimension and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(2, min(4, 1 + difficulty))
        bound = 1 + min(4, difficulty)
        y_comps = [float(self._rng.randint(-bound, bound)) for _ in range(n)]

        # Define functional values on basis
        func_vals = {f"e_{i+1}": y_comps[i] for i in range(n)}

        # Verify: f(x) = <x, y> for a test vector
        test_comps = [float(self._rng.randint(-3, 3)) for _ in range(n)]
        test = Vector(test_comps)
        y_vec = Vector(y_comps)
        f_test = round(test.dot(y_vec), 4)

        vals_str = ", ".join(f"f(e_{i+1})={_fmt(y_comps[i])}" for i in range(n))
        problem = f"{vals_str} in R^{n}"
        return problem, {
            "n": n, "y_comps": y_comps,
            "func_vals": func_vals,
            "test": test_comps, "f_test": f_test,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Riesz representation steps.

        Args:
            sd: Solution data dictionary.

        Returns:
            List of step strings.
        """
        steps = [f"f(e_{i+1}) = {_fmt(sd['y_comps'][i])}" for i in range(sd["n"])]
        steps.append(f"Riesz: y = {_vec_str(sd['y_comps'])}")
        steps.append(f"verify: f{_vec_str(sd['test'])} = <test, y> = {_fmt(sd['f_test'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the representing element.

        Args:
            sd: Solution data dictionary.

        Returns:
            Answer string.
        """
        return f"y={_vec_str(sd['y_comps'])}"
