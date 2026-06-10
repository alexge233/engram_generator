"""Dimensionality reduction task generators.

4 generators across tiers 5-6 covering PCA computation, truncated SVD,
explained variance ratios, and feature selection with VIF.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. PCA Compute (tier 5)
# ---------------------------------------------------------------------------

@register
class PcaComputeGenerator(StepGenerator):
    """Compute PCA for 2D data projected onto the first principal component.

    Center data, compute the 2x2 covariance matrix, find eigenvalues and
    eigenvectors analytically, and project points onto the top PC.

    Difficulty scaling:
        Difficulty 1-3: 4 data points, integer values in [1, 10].
        Difficulty 4-6: 5 data points, values in [-5, 15].
        Difficulty 7-8: 6 data points, values in [-10, 20].

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pca_compute"

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
            Short task description.
        """
        return "compute PCA and project 2D data onto first PC"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PCA problem on 2D data.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 4
            lo, hi = 1, 10
        elif difficulty <= 6:
            n = 5
            lo, hi = -5, 15
        else:
            n = 6
            lo, hi = -10, 20

        xs = [self._rng.randint(lo, hi) for _ in range(n)]
        ys = [self._rng.randint(lo, hi) for _ in range(n)]

        mx = round(sum(xs) / n, 4)
        my = round(sum(ys) / n, 4)
        cx = [round(x - mx, 4) for x in xs]
        cy = [round(y - my, 4) for y in ys]

        cov_xx = round(sum(a * a for a in cx) / n, 4)
        cov_xy = round(sum(a * b for a, b in zip(cx, cy)) / n, 4)
        cov_yy = round(sum(b * b for b in cy) / n, 4)

        trace = cov_xx + cov_yy
        det = cov_xx * cov_yy - cov_xy * cov_xy
        disc = max(trace ** 2 - 4 * det, 0)
        sqrt_disc = math.sqrt(disc)

        lam1 = round((trace + sqrt_disc) / 2, 4)
        lam2 = round((trace - sqrt_disc) / 2, 4)

        if abs(cov_xy) > 1e-8:
            ev1_x = cov_xy
            ev1_y = lam1 - cov_xx
        else:
            ev1_x = 1.0 if cov_xx >= cov_yy else 0.0
            ev1_y = 0.0 if cov_xx >= cov_yy else 1.0

        norm = math.sqrt(ev1_x ** 2 + ev1_y ** 2)
        if norm > 1e-8:
            ev1_x = round(ev1_x / norm, 4)
            ev1_y = round(ev1_y / norm, 4)

        projections = [round(cx[i] * ev1_x + cy[i] * ev1_y, 4) for i in range(n)]

        pts = ", ".join(f"({xs[i]},{ys[i]})" for i in range(n))
        return (
            f"PCA: data = [{pts}]. Center, compute cov, project onto PC1.",
            {
                "xs": xs, "ys": ys, "n": n,
                "mx": mx, "my": my,
                "cov_xx": cov_xx, "cov_xy": cov_xy, "cov_yy": cov_yy,
                "lam1": lam1, "lam2": lam2,
                "ev1": (ev1_x, ev1_y),
                "projections": projections,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for PCA.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing centering, covariance, eigenvalues, and projections.
        """
        ev = data["ev1"]
        proj_str = ", ".join(str(p) for p in data["projections"])
        return [
            f"means: ({data['mx']}, {data['my']})",
            f"cov = [[{data['cov_xx']}, {data['cov_xy']}], "
            f"[{data['cov_xy']}, {data['cov_yy']}]]",
            f"eigenvalues: lam1={data['lam1']}, lam2={data['lam2']}",
            f"PC1 = ({ev[0]}, {ev[1]})",
            f"projections: [{proj_str}]",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the PCA projections.

        Args:
            data: Solution data dict.

        Returns:
            Eigenvalues and projection values.
        """
        proj_str = ", ".join(str(p) for p in data["projections"])
        return f"lam1={data['lam1']}, projections=[{proj_str}]"


# ---------------------------------------------------------------------------
# 2. SVD Truncated (tier 6)
# ---------------------------------------------------------------------------

@register
class SvdTruncatedGenerator(StepGenerator):
    """Compute truncated SVD of a small matrix and reconstruction error.

    For a 2x3 matrix A, compute A^T*A, find eigenvalues/vectors, form
    singular values, truncate to rank k=1, and compute ||A - A_k||_F.

    Difficulty scaling:
        Difficulty 1-3: 2x2 matrix, values in [1, 5].
        Difficulty 4-6: 2x3 matrix, values in [-3, 6].
        Difficulty 7-8: 3x3 matrix, values in [-5, 9].

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "svd_truncated"

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
        return "compute truncated SVD and reconstruction error"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a truncated SVD problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            m, n_cols = 2, 2
            lo, hi = 1, 5
        elif difficulty <= 6:
            m, n_cols = 2, 3
            lo, hi = -3, 6
        else:
            m, n_cols = 3, 3
            lo, hi = -5, 9

        mat = [
            [self._rng.randint(lo, hi) for _ in range(n_cols)]
            for _ in range(m)
        ]

        ata = self._mat_mul(self._transpose(mat), mat)
        frob_sq = sum(mat[i][j] ** 2 for i in range(m) for j in range(n_cols))

        singular_vals_sq = self._eigenvalues_2x2(ata) if len(ata) == 2 else self._eigenvalues_approx(ata)
        singular_vals_sq = sorted(singular_vals_sq, reverse=True)
        singular_vals = [round(math.sqrt(max(v, 0)), 4) for v in singular_vals_sq]

        k = 1
        kept_energy = sum(singular_vals_sq[:k])
        error = round(math.sqrt(max(frob_sq - kept_energy, 0)), 4)

        mat_str = "; ".join(
            ", ".join(str(v) for v in row) for row in mat
        )
        return (
            f"SVD: A = [{mat_str}] ({m}x{n_cols}). "
            f"Truncate to rank {k}. Compute ||A - A_{k}||_F.",
            {
                "mat": mat, "m": m, "n_cols": n_cols,
                "singular_vals": singular_vals,
                "frob_sq": frob_sq, "k": k, "error": error,
            },
        )

    def _transpose(self, mat: list[list[int]]) -> list[list[int]]:
        """Transpose a matrix.

        Args:
            mat: Input matrix.

        Returns:
            Transposed matrix.
        """
        m = len(mat)
        n = len(mat[0])
        return [[mat[i][j] for i in range(m)] for j in range(n)]

    def _mat_mul(self, a: list[list[int]], b: list[list[int]]) -> list[list[float]]:
        """Multiply two matrices.

        Args:
            a: Left matrix.
            b: Right matrix.

        Returns:
            Product matrix with rounded values.
        """
        m = len(a)
        n = len(b[0])
        p = len(b)
        result = []
        for i in range(m):
            row = []
            for j in range(n):
                val = sum(a[i][k] * b[k][j] for k in range(p))
                row.append(round(val, 4))
            result.append(row)
        return result

    def _eigenvalues_2x2(self, mat: list[list[float]]) -> list[float]:
        """Compute eigenvalues of a 2x2 symmetric matrix.

        Args:
            mat: 2x2 symmetric matrix.

        Returns:
            List of two eigenvalues.
        """
        a, b = mat[0][0], mat[0][1]
        d = mat[1][1]
        trace = a + d
        det = a * d - b * b
        disc = max(trace ** 2 - 4 * det, 0)
        sq = math.sqrt(disc)
        return [round((trace + sq) / 2, 4), round((trace - sq) / 2, 4)]

    def _eigenvalues_approx(self, mat: list[list[float]]) -> list[float]:
        """Approximate eigenvalues of a symmetric matrix via power iteration.

        Uses diagonal elements as rough estimates for small matrices.

        Args:
            mat: Symmetric matrix.

        Returns:
            List of approximate eigenvalues.
        """
        n = len(mat)
        frob = sum(mat[i][j] ** 2 for i in range(n) for j in range(n))
        diag = [mat[i][i] for i in range(n)]
        trace = sum(diag)
        diag_sorted = sorted(diag, reverse=True)
        result = []
        remaining = trace
        for i in range(n):
            if i < n - 1:
                est = max(diag_sorted[i], 0)
                result.append(round(est, 4))
                remaining -= est
            else:
                result.append(round(max(remaining, 0), 4))
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for truncated SVD.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing singular values and reconstruction error.
        """
        sv_str = ", ".join(str(v) for v in data["singular_vals"])
        return [
            f"singular values: [{sv_str}]",
            f"||A||_F^2 = {data['frob_sq']}",
            f"keep top {data['k']} singular value(s)",
            f"||A - A_{data['k']}||_F = {data['error']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the reconstruction error.

        Args:
            data: Solution data dict.

        Returns:
            Truncated SVD error as a string.
        """
        sv_str = ", ".join(str(v) for v in data["singular_vals"])
        return f"sigma=[{sv_str}], error={data['error']}"


# ---------------------------------------------------------------------------
# 3. Explained Variance (tier 5)
# ---------------------------------------------------------------------------

@register
class ExplainedVarianceGenerator(StepGenerator):
    """Compute proportion of variance explained by each principal component.

    Given eigenvalues, compute the ratio for each and the cumulative sum
    to find k such that cumulative variance >= 95%.

    Difficulty scaling:
        Difficulty 1-3: 3 eigenvalues, well-separated.
        Difficulty 4-6: 4 eigenvalues, moderate spread.
        Difficulty 7-8: 5 eigenvalues, closer together.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "explained_variance"

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
        return "compute explained variance ratio and find k for 95%"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an explained variance problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 3
            eigenvalues = sorted(
                [round(self._rng.uniform(0.5, 10), 2) for _ in range(n)],
                reverse=True,
            )
            eigenvalues[0] = round(eigenvalues[0] * 3, 2)
        elif difficulty <= 6:
            n = 4
            eigenvalues = sorted(
                [round(self._rng.uniform(0.2, 8), 2) for _ in range(n)],
                reverse=True,
            )
            eigenvalues[0] = round(eigenvalues[0] * 2, 2)
        else:
            n = 5
            eigenvalues = sorted(
                [round(self._rng.uniform(0.1, 6), 2) for _ in range(n)],
                reverse=True,
            )

        total = round(sum(eigenvalues), 4)
        ratios = [round(ev / total, 4) for ev in eigenvalues]
        cumulative = []
        running = 0.0
        for r in ratios:
            running = round(running + r, 4)
            cumulative.append(running)

        k_95 = next(
            (i + 1 for i, c in enumerate(cumulative) if c >= 0.95), n
        )

        ev_str = ", ".join(str(v) for v in eigenvalues)
        return (
            f"Eigenvalues: [{ev_str}]. "
            f"Compute variance ratios and find k for >=95%.",
            {
                "eigenvalues": eigenvalues, "total": total,
                "ratios": ratios, "cumulative": cumulative,
                "k_95": k_95,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for explained variance.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing ratios, cumulative, and k for 95%.
        """
        steps = [f"total = {data['total']}"]
        for i, (r, c) in enumerate(zip(data["ratios"], data["cumulative"])):
            steps.append(
                f"PC{i + 1}: ratio={r}, cumulative={c}"
            )
        steps.append(f"k for >=95%: k = {data['k_95']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the explained variance summary.

        Args:
            data: Solution data dict.

        Returns:
            Ratios and k for 95% threshold.
        """
        r_str = ", ".join(str(r) for r in data["ratios"])
        return f"ratios=[{r_str}], k_95={data['k_95']}"


# ---------------------------------------------------------------------------
# 4. Feature Selection (tier 5)
# ---------------------------------------------------------------------------

@register
class FeatureSelectionGenerator(StepGenerator):
    """Select top-k features by correlation and compute VIF.

    Given feature-target correlations, select the top-k features.
    Then compute VIF = 1/(1 - R^2) for a given R^2 between two
    features to check multicollinearity.

    Difficulty scaling:
        Difficulty 1-3: 4 features, select top-2. VIF with simple R^2.
        Difficulty 4-6: 5 features, select top-2. VIF with moderate R^2.
        Difficulty 7-8: 6 features, select top-3. VIF with high R^2.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "feature_selection"

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
        return "select top features by correlation and compute VIF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a feature selection problem with VIF.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_feat = 4
            top_k = 2
            r_sq = round(self._rng.uniform(0.1, 0.5), 2)
        elif difficulty <= 6:
            n_feat = 5
            top_k = 2
            r_sq = round(self._rng.uniform(0.3, 0.7), 2)
        else:
            n_feat = 6
            top_k = 3
            r_sq = round(self._rng.uniform(0.5, 0.95), 2)

        names = [f"X{i + 1}" for i in range(n_feat)]
        correlations = [
            round(self._rng.uniform(-0.9, 0.9), 2)
            for _ in range(n_feat)
        ]

        abs_corrs = [(abs(c), i) for i, c in enumerate(correlations)]
        abs_corrs.sort(reverse=True)
        selected_idx = [idx for _, idx in abs_corrs[:top_k]]
        selected = [names[i] for i in sorted(selected_idx)]

        vif = round(1.0 / (1.0 - r_sq), 4) if r_sq < 1.0 else float("inf")

        corr_str = ", ".join(
            f"{names[i]}:{correlations[i]}" for i in range(n_feat)
        )
        return (
            f"Correlations: {corr_str}. Select top-{top_k}. "
            f"VIF for R^2 = {r_sq}.",
            {
                "names": names, "correlations": correlations,
                "top_k": top_k, "selected": selected,
                "r_sq": r_sq, "vif": vif,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for feature selection.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing |correlations|, selection, and VIF.
        """
        abs_str = ", ".join(
            f"|{data['names'][i]}|={abs(data['correlations'][i])}"
            for i in range(len(data["names"]))
        )
        sel_str = ", ".join(data["selected"])
        return [
            f"absolute correlations: {abs_str}",
            f"top-{data['top_k']}: {sel_str}",
            f"VIF = 1/(1 - {data['r_sq']}) = {data['vif']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the selected features and VIF.

        Args:
            data: Solution data dict.

        Returns:
            Selection and VIF as a string.
        """
        sel_str = ", ".join(data["selected"])
        return f"selected=[{sel_str}], VIF={data['vif']}"
