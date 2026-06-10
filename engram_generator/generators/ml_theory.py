"""Machine learning theory generators.

10 generators across tiers 5-7 covering VC dimension, PAC bounds,
Rademacher complexity, kernel trick, regularisation path,
bias-variance decomposition, cross-validation, information gain,
gradient flow, and attention complexity.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. VC Dimension (tier 7)
# ---------------------------------------------------------------------------

@register
class VCDimensionGenerator(StepGenerator):
    """Compute VC dimension for simple hypothesis classes.

    Generates problems asking for VCdim of lines in R^2, intervals
    on R, axis-aligned rectangles, or convex polygons. Shows shattering
    arguments and growth function bounds.
    """

    _TEMPLATES: list[dict] = [
        {
            "hypothesis": "lines in R^2",
            "vcdim": 3,
            "shatter": "3 non-collinear points can be shattered",
            "growth": "sum_{i=0}^{3} C(n,i)",
            "fail": "4 points: convex hull has one inside, cannot shatter",
        },
        {
            "hypothesis": "intervals on R",
            "vcdim": 2,
            "shatter": "2 points: label (1,0) and (0,1) both achievable",
            "growth": "C(n,0)+C(n,1)+C(n,2)",
            "fail": "3 points: cannot label middle differently from ends",
        },
        {
            "hypothesis": "axis-aligned rectangles in R^2",
            "vcdim": 4,
            "shatter": "4 pts at compass positions shattered by rectangles",
            "growth": "sum_{i=0}^{4} C(n,i)",
            "fail": "5 points: one inside convex hull, cannot isolate negative",
        },
        {
            "hypothesis": "convex k-gons in R^2 (k>=n)",
            "vcdim": -1,
            "shatter": "any n points in convex position can be shattered",
            "growth": "2^n (infinite VCdim)",
            "fail": "VCdim is infinite (no finite upper bound)",
        },
        {
            "hypothesis": "threshold classifiers on R (h(x)=1 if x>=t)",
            "vcdim": 1,
            "shatter": "1 point: threshold left or right of it",
            "growth": "n+1",
            "fail": "2 points: cannot label (0,1) with x1<x2",
        },
        {
            "hypothesis": "circles in R^2 (inside vs outside)",
            "vcdim": 3,
            "shatter": "3 non-collinear points, circle through any subset",
            "growth": "sum_{i=0}^{3} C(n,i)",
            "fail": "4 points: collinear arrangement fails",
        },
        {
            "hypothesis": "sinusoidal classifiers h(x)=sign(sin(wx))",
            "vcdim": -1,
            "shatter": "for any n points, choose w to shatter them",
            "growth": "2^n (infinite VCdim)",
            "fail": "VCdim is infinite",
        },
        {
            "hypothesis": "conjunctions of d boolean literals",
            "vcdim": -2,
            "shatter": "d+1 points (d unit vectors + origin)",
            "growth": "at most 3^d hypotheses",
            "fail": "d+2 points cannot be shattered",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vc_dimension"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["big_o"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute VC dimension of hypothesis class"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a VC dimension problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        # For conjunction template, fill in concrete d
        if tmpl["vcdim"] == -2:
            d = self._rng.randint(2, min(3 + difficulty, 6))
            vcdim = d
            shatter = f"{d} unit vectors + origin = {d + 1} points"
            fail = f"{d + 2} points cannot be shattered"
            hypothesis = f"conjunctions of {d} boolean literals"
        elif tmpl["vcdim"] == -1:
            vcdim = "infinite"
            shatter = tmpl["shatter"]
            fail = tmpl["fail"]
            hypothesis = tmpl["hypothesis"]
        else:
            vcdim = tmpl["vcdim"]
            shatter = tmpl["shatter"]
            fail = tmpl["fail"]
            hypothesis = tmpl["hypothesis"]

        problem = f"VCdim of {hypothesis}"
        return problem, {
            "hypothesis": hypothesis,
            "vcdim": vcdim,
            "shatter": shatter,
            "growth": tmpl["growth"],
            "fail": fail,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate VC dimension reasoning steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"H = {d['hypothesis']}",
            f"shatter: {d['shatter']}",
            f"fail at VCdim+1: {d['fail']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the VC dimension.

        Args:
            solution_data: All computed solution information.

        Returns:
            VC dimension string.
        """
        return f"VCdim={solution_data['vcdim']}"


# ---------------------------------------------------------------------------
# 2. PAC Bound (tier 7)
# ---------------------------------------------------------------------------

@register
class PACBoundGenerator(StepGenerator):
    """Compute PAC learning sample complexity bound.

    Uses m >= (1/epsilon)(ln|H| + ln(1/delta)) to determine the
    number of training examples needed for PAC guarantees.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pac_bound"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vc_dimension"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute PAC sample complexity bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PAC bound problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        epsilon = self._rng.choice([0.1, 0.05, 0.01])
        delta = self._rng.choice([0.1, 0.05, 0.01])

        # Hypothesis space size grows with difficulty
        if difficulty <= 3:
            h_size = self._rng.choice([10, 20, 50])
        elif difficulty <= 6:
            h_size = self._rng.choice([100, 500, 1000])
        else:
            h_size = self._rng.choice([10000, 100000])

        ln_h = round(math.log(h_size), 4)
        ln_delta = round(math.log(1.0 / delta), 4)
        m_bound = round((1.0 / epsilon) * (ln_h + ln_delta), 4)
        m_ceil = math.ceil(m_bound)

        problem = f"|H|={h_size}, epsilon={epsilon}, delta={delta}"
        return problem, {
            "h_size": h_size,
            "epsilon": epsilon,
            "delta": delta,
            "ln_h": ln_h,
            "ln_delta": ln_delta,
            "m_bound": m_bound,
            "m_ceil": m_ceil,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate PAC bound computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"m >= (1/eps)(ln|H|+ln(1/delta))",
            f"ln({d['h_size']})={d['ln_h']}, ln(1/{d['delta']})={d['ln_delta']}",
            f"m >= (1/{d['epsilon']})*({d['ln_h']}+{d['ln_delta']}) = {d['m_bound']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the sample complexity.

        Args:
            solution_data: All computed solution information.

        Returns:
            Minimum sample size string.
        """
        return f"m>={solution_data['m_ceil']}"


# ---------------------------------------------------------------------------
# 3. Rademacher Complexity (tier 7)
# ---------------------------------------------------------------------------

@register
class RademacherComplexityGenerator(StepGenerator):
    """Bound Rademacher complexity for linear function classes.

    Computes R_n(F) <= max|w| * sqrt(sum|x_i|^2 / n) for bounded
    linear functions over a sample of n data points.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rademacher_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vc_dimension"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "bound Rademacher complexity for linear class"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Rademacher complexity problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(4, min(4 + difficulty * 2, 16))
        max_w = round(self._rng.uniform(0.5, 3.0), 2)

        # Generate x norms
        x_norms = [
            round(self._rng.uniform(0.1, 2.0), 2)
            for _ in range(n)
        ]
        sum_sq = round(sum(x ** 2 for x in x_norms), 4)
        avg_sq = round(sum_sq / n, 4)
        bound = round(max_w * math.sqrt(avg_sq), 4)

        norms_str = ", ".join(str(x) for x in x_norms)
        problem = (
            f"F={{w^Tx : |w|<={max_w}}}, n={n}, "
            f"|x_i|=[{norms_str}]"
        )
        return problem, {
            "n": n,
            "max_w": max_w,
            "x_norms": x_norms,
            "sum_sq": sum_sq,
            "avg_sq": avg_sq,
            "bound": bound,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate Rademacher complexity bound steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"R_n <= max|w|*sqrt(sum|x_i|^2/n)",
            f"sum|x_i|^2 = {d['sum_sq']}",
            f"avg = {d['sum_sq']}/{d['n']} = {d['avg_sq']}",
            f"R_n <= {d['max_w']}*sqrt({d['avg_sq']}) = {d['bound']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the Rademacher complexity bound.

        Args:
            solution_data: All computed solution information.

        Returns:
            Bound string.
        """
        return f"R_n<={solution_data['bound']}"


# ---------------------------------------------------------------------------
# 4. Kernel Trick (tier 6)
# ---------------------------------------------------------------------------

@register
class KernelTrickGenerator(StepGenerator):
    """Compute kernel evaluations and show explicit feature maps.

    Demonstrates polynomial kernel K(x,y) = (1 + x.y)^d with explicit
    feature map expansion for small d and low-dimensional inputs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kernel_trick"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dot_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute kernel evaluation and show feature map"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a kernel trick problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dim = 2 if difficulty <= 5 else 3
        d = self._rng.choice([2, 3]) if difficulty >= 4 else 2

        x = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]
        y = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]

        dot_xy = round(sum(a * b for a, b in zip(x, y)), 4)
        kernel_val = round((1 + dot_xy) ** d, 4)

        # Feature map for d=2, dim=2: phi(x) = [1, sqrt(2)*x1, sqrt(2)*x2, x1^2, sqrt(2)*x1*x2, x2^2]
        if d == 2 and dim == 2:
            s2 = round(math.sqrt(2), 4)
            phi_x = [
                1.0,
                round(s2 * x[0], 4),
                round(s2 * x[1], 4),
                round(x[0] ** 2, 4),
                round(s2 * x[0] * x[1], 4),
                round(x[1] ** 2, 4),
            ]
            feature_map = f"phi(x) = [1, sqrt(2)*x1, sqrt(2)*x2, x1^2, sqrt(2)*x1*x2, x2^2]"
        else:
            phi_x = []
            feature_map = f"(1+x.y)^{d} implicit feature map"

        x_str = ", ".join(str(v) for v in x)
        y_str = ", ".join(str(v) for v in y)
        problem = f"K(x,y) = (1+x.y)^{d}, x=[{x_str}], y=[{y_str}]"

        return problem, {
            "x": x,
            "y": y,
            "d": d,
            "dot_xy": dot_xy,
            "kernel_val": kernel_val,
            "phi_x": phi_x,
            "feature_map": feature_map,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate kernel computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        sd = solution_data
        steps = [
            f"x.y = {sd['dot_xy']}",
            f"K = (1+{sd['dot_xy']})^{sd['d']} = {sd['kernel_val']}",
            f"map: {sd['feature_map']}",
        ]
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the kernel value.

        Args:
            solution_data: All computed solution information.

        Returns:
            Kernel evaluation string.
        """
        return f"K={solution_data['kernel_val']}"


# ---------------------------------------------------------------------------
# 5. Regularisation Path (tier 6)
# ---------------------------------------------------------------------------

@register
class RegularisationPathGenerator(StepGenerator):
    """Trace the L2 regularisation path as lambda varies.

    Computes w* = (X^T X + lambda I)^{-1} X^T y for small 2x2 systems
    and shows how weights change with different lambda values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regularisation_path"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gradient_descent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace L2 regularisation path as lambda varies"

    def _solve_ridge_2d(self, xtx: list[list[float]],
                        xty: list[float],
                        lam: float) -> list[float]:
        """Solve 2x2 ridge regression (X^TX + lambda*I)^{-1} X^Ty.

        Args:
            xtx: 2x2 matrix X^T X.
            xty: 2-vector X^T y.
            lam: Regularisation parameter.

        Returns:
            Weight vector w* as list of 2 floats.
        """
        a = xtx[0][0] + lam
        b = xtx[0][1]
        c = xtx[1][0]
        d = xtx[1][1] + lam
        det = a * d - b * c
        if abs(det) < 1e-10:
            return [0.0, 0.0]
        w0 = round((d * xty[0] - b * xty[1]) / det, 4)
        w1 = round((-c * xty[0] + a * xty[1]) / det, 4)
        return [w0, w1]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regularisation path problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Generate a small X^TX and X^Ty
        a11 = round(self._rng.uniform(2.0, 8.0), 2)
        a12 = round(self._rng.uniform(-1.0, 1.0), 2)
        a22 = round(self._rng.uniform(2.0, 8.0), 2)
        xtx = [[a11, a12], [a12, a22]]

        b0 = round(self._rng.uniform(1.0, 5.0), 2)
        b1 = round(self._rng.uniform(1.0, 5.0), 2)
        xty = [b0, b1]

        # Compute weights for multiple lambda values
        lambdas = [0.0, 0.1, 1.0, 10.0]
        if difficulty >= 5:
            lambdas = [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]

        path = []
        for lam in lambdas:
            w = self._solve_ridge_2d(xtx, xty, lam)
            path.append({"lambda": lam, "w": w})

        xtx_str = f"[[{a11},{a12}],[{a12},{a22}]]"
        problem = f"X^TX={xtx_str}, X^Ty=[{b0},{b1}]"

        return problem, {
            "xtx": xtx,
            "xty": xty,
            "path": path,
            "lambdas": lambdas,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate regularisation path steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        steps = ["w* = (X^TX + lambda*I)^{-1} X^Ty"]
        for entry in solution_data["path"]:
            steps.append(
                f"lambda={entry['lambda']}: w={entry['w']}"
            )
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the regularisation path summary.

        Args:
            solution_data: All computed solution information.

        Returns:
            Path showing w->0 as lambda grows.
        """
        first = solution_data["path"][0]
        last = solution_data["path"][-1]
        return (
            f"lam=0: w={first['w']}, "
            f"lam={last['lambda']}: w={last['w']} (shrinks to 0)"
        )


# ---------------------------------------------------------------------------
# 6. Bias-Variance Decomposition (tier 6)
# ---------------------------------------------------------------------------

@register
class BiasVarianceDecomposeGenerator(StepGenerator):
    """Decompose expected loss into bias^2 + variance + noise.

    Given model predictions from multiple runs, computes the
    bias, variance, and irreducible noise terms.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bias_variance_decompose"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bias_variance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "decompose expected loss into bias^2 + variance + noise"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bias-variance decomposition problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_runs = self._rng.randint(3, min(3 + difficulty, 8))
        true_val = round(self._rng.uniform(1.0, 5.0), 2)
        noise_std = round(self._rng.uniform(0.1, 0.5), 2)

        # Simulate model predictions with systematic bias and variance
        bias_offset = round(self._rng.uniform(-1.0, 1.0), 2)
        predictions = [
            round(true_val + bias_offset + self._rng.gauss(0, 0.3), 4)
            for _ in range(n_runs)
        ]

        mean_pred = round(sum(predictions) / n_runs, 4)
        bias_sq = round((mean_pred - true_val) ** 2, 4)
        variance = round(
            sum((p - mean_pred) ** 2 for p in predictions) / n_runs, 4
        )
        noise = round(noise_std ** 2, 4)
        total = round(bias_sq + variance + noise, 4)

        preds_str = ", ".join(str(p) for p in predictions)
        problem = (
            f"y_true={true_val}, noise_var={noise}, "
            f"preds=[{preds_str}]"
        )

        return problem, {
            "true_val": true_val,
            "predictions": predictions,
            "mean_pred": mean_pred,
            "bias_sq": bias_sq,
            "variance": variance,
            "noise": noise,
            "total": total,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate decomposition steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"E[pred] = {d['mean_pred']}",
            f"bias^2 = ({d['mean_pred']}-{d['true_val']})^2 = {d['bias_sq']}",
            f"variance = E[(pred-E[pred])^2] = {d['variance']}",
            f"noise = {d['noise']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the decomposition.

        Args:
            solution_data: All computed solution information.

        Returns:
            Loss decomposition string.
        """
        d = solution_data
        return (
            f"bias^2={d['bias_sq']}+var={d['variance']}"
            f"+noise={d['noise']}={d['total']}"
        )


# ---------------------------------------------------------------------------
# 7. Cross-Validation Compute (tier 5)
# ---------------------------------------------------------------------------

@register
class CrossValidationComputeGenerator(StepGenerator):
    """Compute k-fold cross-validation error.

    Splits data into k folds, computes train and validation error
    per fold, and averages across folds.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cross_validation_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute k-fold cross-validation error"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cross-validation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = self._rng.choice([3, 4, 5])
        if difficulty >= 5:
            k = self._rng.choice([5, 10])

        # Generate per-fold errors
        train_errors = [
            round(self._rng.uniform(0.01, 0.15), 4)
            for _ in range(k)
        ]
        val_errors = [
            round(self._rng.uniform(0.05, 0.3), 4)
            for _ in range(k)
        ]

        avg_train = round(sum(train_errors) / k, 4)
        avg_val = round(sum(val_errors) / k, 4)
        gap = round(avg_val - avg_train, 4)

        te_str = ", ".join(str(e) for e in train_errors)
        ve_str = ", ".join(str(e) for e in val_errors)
        problem = f"{k}-fold CV: train_err=[{te_str}], val_err=[{ve_str}]"

        return problem, {
            "k": k,
            "train_errors": train_errors,
            "val_errors": val_errors,
            "avg_train": avg_train,
            "avg_val": avg_val,
            "gap": gap,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate cross-validation computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        fold_steps = []
        for i in range(d["k"]):
            fold_steps.append(
                f"fold {i + 1}: train={d['train_errors'][i]}, val={d['val_errors'][i]}"
            )
        # Limit to first 4 folds to stay within char budget
        steps = fold_steps[:4]
        steps.append(
            f"avg: train={d['avg_train']}, val={d['avg_val']}"
        )
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the CV summary.

        Args:
            solution_data: All computed solution information.

        Returns:
            Average validation error and gap.
        """
        d = solution_data
        return f"CV_val={d['avg_val']}, gap={d['gap']}"


# ---------------------------------------------------------------------------
# 8. Information Gain (tier 5)
# ---------------------------------------------------------------------------

@register
class InformationGainGenerator(StepGenerator):
    """Compute information gain for a decision tree split.

    Applies IG = H(S) - sum(|S_v|/|S|) * H(S_v) to determine the best
    attribute for splitting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "information_gain"

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
            Task instruction string.
        """
        return "compute information gain for decision tree split"

    def _entropy(self, counts: list[int]) -> float:
        """Compute entropy from class counts.

        Args:
            counts: Number of examples per class.

        Returns:
            Shannon entropy in bits.
        """
        total = sum(counts)
        if total == 0:
            return 0.0
        ent = 0.0
        for c in counts:
            if c > 0:
                p = c / total
                ent -= p * math.log2(p)
        return round(ent, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an information gain problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Total examples with binary classification
        n_pos = self._rng.randint(3, 8)
        n_neg = self._rng.randint(3, 8)
        total = n_pos + n_neg
        h_s = self._entropy([n_pos, n_neg])

        # Generate 2-3 attribute values splitting the data
        n_vals = 2 if difficulty <= 4 else 3
        # Distribute positives and negatives across values
        splits = []
        remaining_pos = n_pos
        remaining_neg = n_neg
        for i in range(n_vals - 1):
            sp = self._rng.randint(0, remaining_pos)
            sn = self._rng.randint(0, remaining_neg)
            if sp + sn == 0:
                sp = 1
            splits.append((sp, sn))
            remaining_pos -= sp
            remaining_neg -= sn
        splits.append((remaining_pos, remaining_neg))

        # Compute weighted entropy after split
        weighted_h = 0.0
        split_details = []
        for sp, sn in splits:
            sv_size = sp + sn
            if sv_size > 0:
                h_sv = self._entropy([sp, sn])
                weighted_h += (sv_size / total) * h_sv
                split_details.append({
                    "pos": sp, "neg": sn, "size": sv_size,
                    "h": h_sv,
                })
            else:
                split_details.append({
                    "pos": 0, "neg": 0, "size": 0, "h": 0.0,
                })
        weighted_h = round(weighted_h, 4)
        ig = round(h_s - weighted_h, 4)

        splits_str = ", ".join(
            f"({d['pos']}+/{d['neg']}-)" for d in split_details
        )
        problem = (
            f"S: {n_pos}+/{n_neg}-, "
            f"split -> [{splits_str}]"
        )

        return problem, {
            "n_pos": n_pos,
            "n_neg": n_neg,
            "total": total,
            "h_s": h_s,
            "splits": split_details,
            "weighted_h": weighted_h,
            "ig": ig,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate information gain computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        steps = [f"H(S) = {d['h_s']}"]
        for i, s in enumerate(d["splits"]):
            if s["size"] > 0:
                steps.append(
                    f"S_{i}: {s['size']} examples, H={s['h']}"
                )
        steps.append(f"weighted H = {d['weighted_h']}")
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the information gain.

        Args:
            solution_data: All computed solution information.

        Returns:
            Information gain string.
        """
        return f"IG={solution_data['ig']}"


# ---------------------------------------------------------------------------
# 9. Gradient Flow (tier 6)
# ---------------------------------------------------------------------------

@register
class GradientFlowGenerator(StepGenerator):
    """Trace gradient through a computation graph.

    Builds a small expression graph (e.g., f = (x+y)*z) and computes
    partial derivatives using the chain rule via reverse-mode autodiff.
    """

    _TEMPLATES: list[dict] = [
        {
            "expr": "f = (x+y)*z",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {"x": z, "y": z, "z": x + y},
            "desc": "(x+y)*z",
        },
        {
            "expr": "f = x*y + y*z",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {"x": y, "y": x + z, "z": y},
            "desc": "x*y+y*z",
        },
        {
            "expr": "f = (x*y)*(y+z)",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {
                "x": y * (y + z),
                "y": x * (y + z) + x * y,
                "z": x * y,
            },
            "desc": "(x*y)*(y+z)",
        },
        {
            "expr": "f = x^2 + 2*x*y",
            "vars": ["x", "y"],
            "grad_fn": lambda x, y: {"x": 2 * x + 2 * y, "y": 2 * x},
            "desc": "x^2+2xy",
        },
        {
            "expr": "f = x*y*z",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {"x": y * z, "y": x * z, "z": x * y},
            "desc": "x*y*z",
        },
        {
            "expr": "f = (x+y)^2",
            "vars": ["x", "y"],
            "grad_fn": lambda x, y: {"x": 2 * (x + y), "y": 2 * (x + y)},
            "desc": "(x+y)^2",
        },
        {
            "expr": "f = x^2*y + y^2*z",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {
                "x": 2 * x * y,
                "y": x ** 2 + 2 * y * z,
                "z": y ** 2,
            },
            "desc": "x^2*y+y^2*z",
        },
        {
            "expr": "f = (x-y)*(x+z)",
            "vars": ["x", "y", "z"],
            "grad_fn": lambda x, y, z: {
                "x": (x + z) + (x - y),
                "y": -(x + z),
                "z": x - y,
            },
            "desc": "(x-y)*(x+z)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gradient_flow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["backprop_simple"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace gradient through computation graph"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gradient flow problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        # Generate random values for variables
        vals = {}
        for v in tmpl["vars"]:
            vals[v] = round(self._rng.uniform(-3.0, 3.0), 2)

        # Compute gradients
        grads = tmpl["grad_fn"](*[vals[v] for v in tmpl["vars"]])
        grads = {k: round(v, 4) for k, v in grads.items()}

        vals_str = ", ".join(f"{v}={vals[v]}" for v in tmpl["vars"])
        problem = f"{tmpl['expr']}, {vals_str}"

        return problem, {
            "expr": tmpl["expr"],
            "desc": tmpl["desc"],
            "vals": vals,
            "grads": grads,
            "vars": tmpl["vars"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate gradient computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        steps = [f"f = {d['desc']}"]
        for v in d["vars"]:
            steps.append(f"df/d{v} = {d['grads'][v]}")
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the gradient vector.

        Args:
            solution_data: All computed solution information.

        Returns:
            Gradient string.
        """
        d = solution_data
        parts = [f"df/d{v}={d['grads'][v]}" for v in d["vars"]]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 10. Attention Complexity (tier 7)
# ---------------------------------------------------------------------------

@register
class AttentionComplexityGenerator(StepGenerator):
    """Compare self-attention vs linear attention complexity.

    Self-attention: O(n^2 * d) time, O(n^2) space.
    Linear attention: O(n * d^2) time, O(n * d) space.
    Computes concrete operation counts for given n and d values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "attention_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["big_o"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compare self-attention vs linear attention complexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an attention complexity comparison problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([64, 128, 256])
            d = self._rng.choice([32, 64])
        elif difficulty <= 6:
            n = self._rng.choice([512, 1024])
            d = self._rng.choice([64, 128])
        else:
            n = self._rng.choice([2048, 4096])
            d = self._rng.choice([128, 256])

        # Self-attention
        sa_time = n * n * d
        sa_space = n * n

        # Linear attention
        la_time = n * d * d
        la_space = n * d

        # Which is better?
        if sa_time < la_time:
            winner_time = "self-attention"
        elif la_time < sa_time:
            winner_time = "linear attention"
        else:
            winner_time = "tie"

        speedup = round(sa_time / la_time, 4) if la_time > 0 else 0.0

        problem = f"n={n}, d={d}: self-attention vs linear attention"

        return problem, {
            "n": n,
            "d": d,
            "sa_time": sa_time,
            "sa_space": sa_space,
            "la_time": la_time,
            "la_space": la_space,
            "winner_time": winner_time,
            "speedup": speedup,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate complexity comparison steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"self-attn: O(n^2*d) = {d['sa_time']}, space O(n^2) = {d['sa_space']}",
            f"linear: O(n*d^2) = {d['la_time']}, space O(n*d) = {d['la_space']}",
            f"faster: {d['winner_time']} (ratio={d['speedup']})",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the complexity comparison result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Winner and ratio string.
        """
        d = solution_data
        return f"SA={d['sa_time']}, LA={d['la_time']}, ratio={d['speedup']}"
