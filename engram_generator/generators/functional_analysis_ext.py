"""Extended functional analysis generators for tiers 5-7.

8 generators covering operator norm, spectrum computation, resolvent,
compact integral operators, trace class, weak convergence, closed
graph theorem, and Lp space norms.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# -- Formatting helpers -----------------------------------------------


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


# =====================================================================
# 1. OPERATOR NORM (tier 6)
# =====================================================================

@register
class OperatorNormGenerator(StepGenerator):
    """Compute the operator norm of a 2x2 real matrix.

    ||A|| = sup ||Ax||/||x|| = max singular value = sqrt(max eigenvalue
    of A^T A). Computes for concrete 2x2 matrices.

    Difficulty scaling:
        Difficulty 1-3: diagonal matrices.
        Difficulty 4-6: upper triangular matrices.
        Difficulty 7-8: general 2x2 matrices.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "operator_norm"

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
            difficulty: Controls matrix type.

        Returns:
            Task description string.
        """
        return "compute operator norm of 2x2 matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an operator norm problem.

        Args:
            difficulty: Controls matrix type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a = float(self._rng.randint(1, 4))
            b = float(self._rng.randint(1, 4))
            mat = [[a, 0.0], [0.0, b]]
        elif difficulty <= 6:
            a = float(self._rng.randint(1, 4))
            b = float(self._rng.randint(1, 4))
            c = float(self._rng.randint(-3, 3))
            mat = [[a, c], [0.0, b]]
        else:
            bound = 1 + min(4, difficulty)
            mat = [[float(self._rng.randint(-bound, bound)) for _ in range(2)]
                   for _ in range(2)]

        ata = [
            [mat[0][0] ** 2 + mat[1][0] ** 2,
             mat[0][0] * mat[0][1] + mat[1][0] * mat[1][1]],
            [mat[0][0] * mat[0][1] + mat[1][0] * mat[1][1],
             mat[0][1] ** 2 + mat[1][1] ** 2],
        ]

        tr = ata[0][0] + ata[1][1]
        det = ata[0][0] * ata[1][1] - ata[0][1] * ata[1][0]
        disc = max(0.0, tr ** 2 - 4 * det)
        lam_max = (tr + math.sqrt(disc)) / 2.0
        op_norm = math.sqrt(max(0.0, lam_max))

        problem = f"A = {_mat_str(mat)}. Compute ||A||."
        return problem, {
            "mat": mat, "ata_trace": tr, "ata_det": det,
            "lam_max": lam_max, "op_norm": op_norm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate operator norm computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing A^T A eigenvalue computation.
        """
        return [
            f"A = {_mat_str(data['mat'])}",
            "||A|| = sqrt(max eigenvalue of A^T A)",
            f"tr(A^T A) = {_fmt(data['ata_trace'])}, "
            f"det(A^T A) = {_fmt(data['ata_det'])}",
            f"lam_max = {_fmt(data['lam_max'])}",
            f"||A|| = {_fmt(data['op_norm'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the operator norm.

        Args:
            data: Solution data.

        Returns:
            Operator norm value.
        """
        return f"||A|| = {_fmt(data['op_norm'])}"


# =====================================================================
# 2. SPECTRUM COMPUTE (tier 6)
# =====================================================================

@register
class SpectrumComputeGenerator(StepGenerator):
    """Compute the spectrum of a linear operator.

    sigma(A) = {lambda : A - lambda*I not invertible}. For matrices,
    these are the eigenvalues. Also covers shift property:
    sigma(A + cI) = sigma(A) + c.

    Difficulty scaling:
        Difficulty 1-3: diagonal 2x2 matrix.
        Difficulty 4-6: 2x2 matrix, compute via characteristic polynomial.
        Difficulty 7-8: shift operator, spectral mapping theorem.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectrum_compute"

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
            difficulty: Controls matrix complexity.

        Returns:
            Task description string.
        """
        return "compute spectrum of linear operator"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectrum computation problem.

        Args:
            difficulty: Controls matrix type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam1 = float(self._rng.randint(-3, 5))
            lam2 = float(self._rng.randint(-3, 5))
            mat = [[lam1, 0.0], [0.0, lam2]]
            eigenvalues = sorted(set([lam1, lam2]))
            shift = 0.0
        elif difficulty <= 6:
            a = float(self._rng.randint(-3, 3))
            b = float(self._rng.randint(-3, 3))
            c = float(self._rng.randint(-3, 3))
            d = float(self._rng.randint(-3, 3))
            mat = [[a, b], [c, d]]
            tr = a + d
            det = a * d - b * c
            disc = tr ** 2 - 4 * det
            if disc >= 0:
                lam1 = (tr + math.sqrt(disc)) / 2.0
                lam2 = (tr - math.sqrt(disc)) / 2.0
                eigenvalues = sorted(set([round(lam1, 4), round(lam2, 4)]))
            else:
                re = tr / 2.0
                im = math.sqrt(-disc) / 2.0
                eigenvalues = [round(re, 4)]
                lam1 = re
                lam2 = re
            shift = 0.0
        else:
            lam1 = float(self._rng.randint(-3, 5))
            lam2 = float(self._rng.randint(-3, 5))
            shift = float(self._rng.randint(1, 4))
            mat = [[lam1 + shift, 0.0], [0.0, lam2 + shift]]
            eigenvalues = sorted(set([lam1 + shift, lam2 + shift]))

        problem = f"A = {_mat_str(mat)}. Compute sigma(A)."
        return problem, {
            "mat": mat, "eigenvalues": eigenvalues, "shift": shift,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spectrum computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing eigenvalue computation.
        """
        eig_str = ", ".join(_fmt(e) for e in data["eigenvalues"])
        steps = [
            f"A = {_mat_str(data['mat'])}",
            "sigma(A) = eigenvalues of A",
            f"sigma(A) = {{{eig_str}}}",
        ]
        if data["shift"] != 0:
            shifted = [round(e - data["shift"], 4) for e in data["eigenvalues"]]
            orig_str = ", ".join(_fmt(e) for e in shifted)
            steps.append(
                f"shift: sigma(A-{_fmt(data['shift'])}I) = {{{orig_str}}}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the spectrum.

        Args:
            data: Solution data.

        Returns:
            Set of eigenvalues.
        """
        eig_str = ", ".join(_fmt(e) for e in data["eigenvalues"])
        return f"sigma(A) = {{{eig_str}}}"


# =====================================================================
# 3. RESOLVENT (tier 6)
# =====================================================================

@register
class ResolventGenerator(StepGenerator):
    """Compute the resolvent R(lambda, A) = (A - lambda*I)^{-1}.

    For a 2x2 matrix A and lambda not in sigma(A), computes the
    inverse explicitly using the 2x2 inverse formula.

    Difficulty scaling:
        Difficulty 1-3: diagonal A.
        Difficulty 4-6: triangular A.
        Difficulty 7-8: general 2x2 A.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "resolvent"

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
            difficulty: Controls matrix type.

        Returns:
            Task description string.
        """
        return "compute resolvent (A - lambda I)^{-1}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a resolvent computation problem.

        Args:
            difficulty: Controls matrix type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a11 = float(self._rng.randint(1, 4))
            a22 = float(self._rng.randint(1, 4))
            mat = [[a11, 0.0], [0.0, a22]]
            eigenvalues = [a11, a22]
        elif difficulty <= 6:
            a11 = float(self._rng.randint(1, 4))
            a12 = float(self._rng.randint(1, 3))
            a22 = float(self._rng.randint(1, 4))
            mat = [[a11, a12], [0.0, a22]]
            eigenvalues = [a11, a22]
        else:
            bound = 3
            mat = [[float(self._rng.randint(-bound, bound)) for _ in range(2)]
                   for _ in range(2)]
            tr = mat[0][0] + mat[1][1]
            det_a = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
            disc = tr ** 2 - 4 * det_a
            if disc >= 0:
                eigenvalues = [
                    round((tr + math.sqrt(disc)) / 2, 4),
                    round((tr - math.sqrt(disc)) / 2, 4),
                ]
            else:
                eigenvalues = [round(tr / 2, 4)]

        for _ in range(20):
            lam = float(self._rng.randint(-5, 5))
            if all(abs(lam - e) > 0.5 for e in eigenvalues):
                break

        b = [[mat[0][0] - lam, mat[0][1]],
             [mat[1][0], mat[1][1] - lam]]
        det_b = b[0][0] * b[1][1] - b[0][1] * b[1][0]

        if abs(det_b) < 1e-10:
            inv = [[0.0, 0.0], [0.0, 0.0]]
        else:
            inv = [[round(b[1][1] / det_b, 4), round(-b[0][1] / det_b, 4)],
                   [round(-b[1][0] / det_b, 4), round(b[0][0] / det_b, 4)]]

        problem = (
            f"A = {_mat_str(mat)}, lambda = {_fmt(lam)}. "
            f"Compute R(lambda, A)."
        )
        return problem, {
            "mat": mat, "lam": lam, "det_b": det_b, "inv": inv,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate resolvent computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing matrix inversion.
        """
        return [
            f"A - lambda*I, lambda = {_fmt(data['lam'])}",
            f"det(A - lambda*I) = {_fmt(data['det_b'])}",
            f"R(lambda, A) = {_mat_str(data['inv'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the resolvent matrix.

        Args:
            data: Solution data.

        Returns:
            Resolvent entries.
        """
        return f"R = {_mat_str(data['inv'])}"


# =====================================================================
# 4. COMPACT INTEGRAL OPERATOR (tier 7)
# =====================================================================

@register
class CompactIntegralOperatorGenerator(StepGenerator):
    """Apply a compact integral operator K[f](x) = integral K(x,y)*f(y) dy.

    Template-based for simple kernels on [0,1]. For K(x,y) = xy:
    K[1](x) = x/2. For K(x,y) = x+y: K[1](x) = x + 1/2.

    Difficulty scaling:
        Difficulty 1-3: K(x,y) = c (constant kernel).
        Difficulty 4-6: K(x,y) = xy or x+y.
        Difficulty 7-8: K(x,y) = min(x,y), Green's function.

    Prerequisites:
        definite_integral (tier 5).
    """

    _KERNELS_EASY = [
        ("K(x,y) = 1, f(y) = 1", "1", "K[f](x) = 1",
         "integral_0^1 1*1 dy = 1"),
        ("K(x,y) = 2, f(y) = y", "1", "K[f](x) = 1",
         "integral_0^1 2*y dy = 2*(1/2) = 1"),
        ("K(x,y) = 1, f(y) = y^2", "1/3", "K[f](x) = 1/3",
         "integral_0^1 y^2 dy = 1/3"),
    ]

    _KERNELS_MED = [
        ("K(x,y) = xy, f(y) = 1", "x/2", "K[f](x) = x/2",
         "integral_0^1 xy*1 dy = x*[y^2/2]_0^1 = x/2"),
        ("K(x,y) = x+y, f(y) = 1", "x+1/2", "K[f](x) = x + 1/2",
         "integral_0^1 (x+y) dy = x + 1/2"),
        ("K(x,y) = xy, f(y) = y", "x/3", "K[f](x) = x/3",
         "integral_0^1 xy^2 dy = x/3"),
    ]

    _KERNELS_HARD = [
        ("K(x,y) = min(x,y), f(y) = 1", "x - x^2/2", "K[f](x) = x - x^2/2",
         "integral_0^x y dy + integral_x^1 x dy = x^2/2 + x(1-x) = x - x^2/2"),
        ("K(x,y) = e^{xy}, f(y) = 1", "(e^x-1)/x", "K[f](x) = (e^x-1)/x",
         "integral_0^1 e^{xy} dy = (e^x-1)/x"),
        ("K(x,y) = x^2*y, f(y) = 1", "x^2/2", "K[f](x) = x^2/2",
         "integral_0^1 x^2*y dy = x^2/2"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compact_integral_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls kernel complexity.

        Returns:
            Task description string.
        """
        return "apply integral operator K[f](x) = integral K(x,y)*f(y) dy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compact integral operator problem.

        Args:
            difficulty: Controls kernel type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._KERNELS_EASY
        elif difficulty <= 6:
            pool = self._KERNELS_EASY + self._KERNELS_MED
        else:
            pool = self._KERNELS_EASY + self._KERNELS_MED + self._KERNELS_HARD

        desc, result_expr, result_full, computation = self._rng.choice(pool)
        problem = f"{desc} on [0,1]. Compute K[f](x)."
        return problem, {
            "desc": desc, "result_expr": result_expr,
            "result_full": result_full, "computation": computation,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate integral operator application steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the integration.
        """
        return [
            f"K[f](x) = integral_0^1 K(x,y)*f(y) dy",
            f"kernel and input: {data['desc']}",
            data["computation"],
            data["result_full"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the result function.

        Args:
            data: Solution data.

        Returns:
            Result of operator application.
        """
        return data["result_full"]


# =====================================================================
# 5. TRACE CLASS (tier 6)
# =====================================================================

@register
class TraceClassGenerator(StepGenerator):
    """Compute trace and nuclear norm of a matrix.

    Tr(A) = sum of eigenvalues. For a positive operator, the nuclear
    norm ||A||_1 = Tr(A). For general A, ||A||_1 = sum of singular values.

    Difficulty scaling:
        Difficulty 1-3: diagonal matrix, trace = sum of diagonal.
        Difficulty 4-6: symmetric matrix, trace from eigenvalues.
        Difficulty 7-8: general matrix, nuclear norm from singular values.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trace_class"

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
            difficulty: Controls matrix type.

        Returns:
            Task description string.
        """
        return "compute trace and nuclear norm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trace class computation problem.

        Args:
            difficulty: Controls matrix type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            d1 = float(self._rng.randint(1, 5))
            d2 = float(self._rng.randint(1, 5))
            mat = [[d1, 0.0], [0.0, d2]]
            eigenvalues = sorted([d1, d2])
            singular_values = sorted([abs(d1), abs(d2)], reverse=True)
        elif difficulty <= 6:
            a = float(self._rng.randint(-3, 3))
            b = float(self._rng.randint(-3, 3))
            mat = [[a, b], [b, a]]
            eigenvalues = sorted([a + b, a - b])
            singular_values = sorted([abs(a + b), abs(a - b)], reverse=True)
        else:
            mat = [[float(self._rng.randint(-3, 3)) for _ in range(2)]
                   for _ in range(2)]
            ata = [
                [mat[0][0] ** 2 + mat[1][0] ** 2,
                 mat[0][0] * mat[0][1] + mat[1][0] * mat[1][1]],
                [mat[0][0] * mat[0][1] + mat[1][0] * mat[1][1],
                 mat[0][1] ** 2 + mat[1][1] ** 2],
            ]
            tr_ata = ata[0][0] + ata[1][1]
            det_ata = ata[0][0] * ata[1][1] - ata[0][1] * ata[1][0]
            disc = max(0.0, tr_ata ** 2 - 4 * det_ata)
            s1 = math.sqrt(max(0.0, (tr_ata + math.sqrt(disc)) / 2.0))
            s2 = math.sqrt(max(0.0, (tr_ata - math.sqrt(disc)) / 2.0))
            singular_values = sorted([round(s1, 4), round(s2, 4)], reverse=True)
            eigenvalues = []

        trace = mat[0][0] + mat[1][1]
        nuclear_norm = sum(singular_values)

        problem = f"A = {_mat_str(mat)}. Compute Tr(A) and ||A||_1."
        return problem, {
            "mat": mat, "trace": trace, "eigenvalues": eigenvalues,
            "singular_values": singular_values,
            "nuclear_norm": nuclear_norm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trace and nuclear norm steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing computation.
        """
        sv_str = ", ".join(_fmt(s) for s in data["singular_values"])
        steps = [
            f"A = {_mat_str(data['mat'])}",
            f"Tr(A) = {_fmt(data['trace'])}",
            f"singular values: {sv_str}",
            f"||A||_1 = sum(sv) = {_fmt(data['nuclear_norm'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return trace and nuclear norm.

        Args:
            data: Solution data.

        Returns:
            Trace and nuclear norm values.
        """
        return f"Tr={_fmt(data['trace'])}, ||A||_1={_fmt(data['nuclear_norm'])}"


# =====================================================================
# 6. WEAK CONVERGENCE (tier 6)
# =====================================================================

@register
class WeakConvergenceGenerator(StepGenerator):
    """Determine weak convergence of a sequence in a Hilbert space.

    x_n -> x weakly iff f(x_n) -> f(x) for all f in the dual.
    Template-based examples: e_n in l^2 converges weakly to 0 but not
    strongly. Sequence 1/n converges both weakly and strongly to 0.

    Difficulty scaling:
        Difficulty 1-3: norm-convergent sequences (hence also weak).
        Difficulty 4-6: weak but not strong convergence.
        Difficulty 7-8: distinguish weak, weak*, and strong.

    Prerequisites:
        comparison (tier 0).
    """

    _SEQUENCES_EASY = [
        ("x_n = (1/n, 0, 0, ...) in l^2", "0",
         True, True,
         "||x_n|| = 1/n -> 0, so strong (hence weak)"),
        ("x_n = (1/n^2)*e_1 in l^2", "0",
         True, True,
         "||x_n|| -> 0, strong convergence to 0"),
    ]

    _SEQUENCES_MED = [
        ("e_n (standard basis) in l^2", "0",
         True, False,
         "<e_n, y> = y_n -> 0 for all y in l^2, but ||e_n|| = 1"),
        ("x_n = sin(n*t)/n in L^2[0,2pi]", "0",
         True, True,
         "||x_n||_2 = 1/(n*sqrt(2)) -> 0, strong convergence"),
        ("x_n = e_n/sqrt(n) in l^2", "0",
         True, True,
         "||x_n|| = 1/sqrt(n) -> 0, strong"),
    ]

    _SEQUENCES_HARD = [
        ("sin(n*t) in L^2[0,2pi]", "0",
         True, False,
         "Riemann-Lebesgue: <sin(nt), f> -> 0, but ||sin(nt)|| = sqrt(pi)"),
        ("chi_{[0,1/n]} * sqrt(n) in L^2[0,1]", "0",
         True, False,
         "<x_n, f> -> 0 by dominated convergence, ||x_n|| = 1"),
        ("constant sequence x_n = x", "x",
         True, True,
         "trivially converges both strongly and weakly"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weak_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls sequence complexity.

        Returns:
            Task description string.
        """
        return "determine weak and strong convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a weak convergence problem.

        Args:
            difficulty: Controls sequence type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._SEQUENCES_EASY
        elif difficulty <= 6:
            pool = self._SEQUENCES_EASY + self._SEQUENCES_MED
        else:
            pool = self._SEQUENCES_EASY + self._SEQUENCES_MED + self._SEQUENCES_HARD

        desc, limit, weak, strong, reason = self._rng.choice(pool)
        problem = f"{desc}. Weak/strong convergence?"
        return problem, {
            "desc": desc, "limit": limit,
            "weak": weak, "strong": strong, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate convergence analysis steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining weak and strong convergence.
        """
        weak_str = "YES" if data["weak"] else "NO"
        strong_str = "YES" if data["strong"] else "NO"
        return [
            f"sequence: {data['desc']}",
            f"limit: {data['limit']}",
            data["reason"],
            f"weak convergence: {weak_str}, strong convergence: {strong_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return convergence classification.

        Args:
            data: Solution data.

        Returns:
            Weak and strong convergence status.
        """
        if data["strong"]:
            return f"strong (and weak) to {data['limit']}"
        if data["weak"]:
            return f"weak to {data['limit']}, NOT strong"
        return "does not converge"


# =====================================================================
# 7. CLOSED GRAPH (tier 7)
# =====================================================================

@register
class ClosedGraphGenerator(StepGenerator):
    """Apply the closed graph theorem to verify boundedness.

    If A: X -> Y is closed (graph closed in X x Y) and X, Y are
    Banach spaces, then A is bounded. Template-based verification
    for concrete operators.

    Difficulty scaling:
        Difficulty 1-3: bounded operators (obviously closed graph).
        Difficulty 4-6: differential operators on appropriate domains.
        Difficulty 7-8: unbounded operators with non-closed graph.

    Prerequisites:
        comparison (tier 0).
    """

    _OPERATORS_EASY = [
        ("A: R^n -> R^n, matrix multiplication",
         True, True,
         "finite-dim linear operator, always bounded, graph always closed"),
        ("A: l^2 -> l^2, A(x)_n = a_n*x_n with sup|a_n| < inf",
         True, True,
         "bounded diagonal operator, ||A|| = sup|a_n|"),
    ]

    _OPERATORS_MED = [
        ("d/dx: C^1[0,1] -> C[0,1] (both with sup norm)",
         True, True,
         "graph is closed: x_n -> x, x_n' -> y implies x' = y. "
         "C^1 is Banach, so d/dx is bounded on C^1"),
        ("A: L^2 -> L^2, Af(x) = x*f(x)",
         True, True,
         "multiplication operator, ||Af|| <= ||f||, bounded hence closed"),
        ("integration: C[0,1] -> C[0,1], Af(x) = int_0^x f(t) dt",
         True, True,
         "integral operator is bounded, ||Af|| <= ||f||, closed graph"),
    ]

    _OPERATORS_HARD = [
        ("d/dx: L^2[0,1] -> L^2[0,1] (on domain H^1)",
         True, True,
         "closed on H^1 domain, CGT applies: d/dx: H^1 -> L^2 bounded"),
        ("A(x)_n = n*x_n on l^2 (domain = finite sequences)",
         False, False,
         "unbounded: ||Ae_n|| = n, domain not complete, CGT does not apply"),
        ("A: l^2 -> l^2, A(x)_n = x_n/n",
         True, True,
         "compact (hence bounded), ||A|| = 1, graph closed"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "closed_graph"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls operator complexity.

        Returns:
            Task description string.
        """
        return "apply closed graph theorem to verify boundedness"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a closed graph theorem problem.

        Args:
            difficulty: Controls operator type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._OPERATORS_EASY
        elif difficulty <= 6:
            pool = self._OPERATORS_EASY + self._OPERATORS_MED
        else:
            pool = self._OPERATORS_EASY + self._OPERATORS_MED + self._OPERATORS_HARD

        desc, closed, bounded, reason = self._rng.choice(pool)
        problem = f"{desc}. Is A bounded (via closed graph theorem)?"
        return problem, {
            "desc": desc, "closed": closed,
            "bounded": bounded, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate closed graph theorem steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the application.
        """
        closed_str = "YES" if data["closed"] else "NO"
        bounded_str = "YES" if data["bounded"] else "NO"
        return [
            f"operator: {data['desc']}",
            "CGT: closed graph + Banach spaces => bounded",
            f"graph closed: {closed_str}",
            data["reason"],
            f"bounded: {bounded_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return boundedness verdict.

        Args:
            data: Solution data.

        Returns:
            Whether the operator is bounded.
        """
        if data["bounded"]:
            return "bounded (closed graph theorem)"
        return "NOT bounded (CGT hypotheses not met)"


# =====================================================================
# 8. LP SPACE NORM (tier 5)
# =====================================================================

@register
class LpSpaceNormGenerator(StepGenerator):
    """Compute Lp norms and verify Holder's inequality.

    ||f||_p = (integral |f|^p)^{1/p}. Computes for step functions on
    [0,1]. Verifies Holder: ||fg||_1 <= ||f||_p * ||g||_q with
    1/p + 1/q = 1.

    Difficulty scaling:
        Difficulty 1-3: p=1 or p=2, simple step function.
        Difficulty 4-6: p=2, two functions, verify Holder.
        Difficulty 7-8: general p, Holder verification.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lp_space_norm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls p and function complexity.

        Returns:
            Task description string.
        """
        return "compute Lp norm and verify Holder inequality"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Lp norm computation problem.

        Step function: f(x) = a_i on [x_{i-1}, x_i] for uniform
        partition.

        Args:
            difficulty: Controls p and number of steps.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.choice([1, 2])
            n_steps = 2
        elif difficulty <= 6:
            p = 2
            n_steps = self._rng.randint(2, 3)
        else:
            p = self._rng.choice([2, 3, 4])
            n_steps = self._rng.randint(3, 4)

        q = round(p / (p - 1), 4) if p > 1 else float('inf')
        dx = 1.0 / n_steps
        f_vals = [float(self._rng.randint(1, 4)) for _ in range(n_steps)]
        g_vals = [float(self._rng.randint(1, 4)) for _ in range(n_steps)]

        f_p_integral = sum(abs(v) ** p * dx for v in f_vals)
        f_norm = round(f_p_integral ** (1.0 / p), 4)

        if q != float('inf'):
            g_q_integral = sum(abs(v) ** q * dx for v in g_vals)
            g_norm = round(g_q_integral ** (1.0 / q), 4)
        else:
            g_norm = round(max(abs(v) for v in g_vals), 4)

        fg_integral = round(sum(abs(f_vals[i] * g_vals[i]) * dx
                                for i in range(n_steps)), 4)
        holder_rhs = round(f_norm * g_norm, 4)
        holder_ok = fg_integral <= holder_rhs + 1e-8

        f_str = ", ".join(_fmt(v) for v in f_vals)
        g_str = ", ".join(_fmt(v) for v in g_vals)
        problem = (
            f"f = [{f_str}], g = [{g_str}] (step functions on [0,1]), "
            f"p={p}. Compute ||f||_p and verify Holder."
        )
        return problem, {
            "p": p, "q": q, "n_steps": n_steps, "dx": dx,
            "f_vals": f_vals, "g_vals": g_vals,
            "f_norm": f_norm, "g_norm": g_norm,
            "fg_integral": fg_integral, "holder_rhs": holder_rhs,
            "holder_ok": holder_ok,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lp norm computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing norm and Holder verification.
        """
        q_str = "inf" if data["q"] == float('inf') else _fmt(data["q"])
        return [
            f"p={data['p']}, q={q_str}, 1/p+1/q=1",
            f"||f||_p = {_fmt(data['f_norm'])}",
            f"||g||_q = {_fmt(data['g_norm'])}",
            f"||fg||_1 = {_fmt(data['fg_integral'])}",
            f"||f||_p * ||g||_q = {_fmt(data['holder_rhs'])}",
            f"Holder: {_fmt(data['fg_integral'])} <= "
            f"{_fmt(data['holder_rhs'])}? "
            f"{'YES' if data['holder_ok'] else 'NO'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Lp norm and Holder verification.

        Args:
            data: Solution data.

        Returns:
            Norm value and Holder status.
        """
        return (
            f"||f||_{data['p']} = {_fmt(data['f_norm'])}, "
            f"Holder: {'verified' if data['holder_ok'] else 'failed'}"
        )
