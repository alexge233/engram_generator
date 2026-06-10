"""Tensor analysis generators for tiers 5-7.

Provides generators for tensor contraction, covariant derivative,
metric tensor computation, Ricci tensor, Levi-Civita symbol evaluation,
and index raising/lowering. Each generator produces step-by-step
solutions with LaTeX formatting suitable for training sequence models.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ────────────────────────────────────────────────


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


# ── 1. Tensor contraction (tier 6) ───────────────────────────────────


@register
class TensorContractionGenerator(StepGenerator):
    """Contract indices of a rank-2 tensor T^i_i to compute its trace.

    For a square matrix T, the contraction T^i_i = sum_i T^i_i equals
    the trace. Generates 2x2 and 3x3 tensors with integer entries.

    Input format:
        ``compute tensor contraction (trace)``

    Target format:
        ``T = [[3,1],[2,5]] <step> T^1_1=3, T^2_2=5
        <step> T^i_i = 3+5 = 8``

    Difficulty scaling:
        Difficulty 1-3: 2x2 tensor, small entries.
        Difficulty 4-6: 3x3 tensor, moderate entries.
        Difficulty 7-8: 3x3 tensor, larger entries including negatives.

    Prerequisites:
        matrix_trace (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tensor_contraction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_trace"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls tensor size and entry range.

        Returns:
            Natural language description.
        """
        return "compute tensor contraction (trace)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tensor contraction problem.

        Args:
            difficulty: Controls tensor dimension and entry magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            dim = 2
            lo, hi = -3, 5
        elif difficulty <= 6:
            dim = 3
            lo, hi = -5, 7
        else:
            dim = 3
            lo, hi = -8, 10

        tensor = []
        for i in range(dim):
            row = [self._rng.randint(lo, hi) for _ in range(dim)]
            tensor.append(row)

        diag = [tensor[i][i] for i in range(dim)]
        trace = sum(diag)

        rows_str = ", ".join(
            "[" + ",".join(str(v) for v in row) + "]" for row in tensor
        )
        problem = f"T^i_j = [{rows_str}]"
        return problem, {
            "tensor": tensor, "dim": dim,
            "diag": diag, "trace": trace,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate contraction steps.

        Args:
            data: Solution data with tensor and diagonal values.

        Returns:
            Steps showing diagonal extraction and summation.
        """
        steps = []
        for i in range(data["dim"]):
            steps.append(f"T^{i+1}_{i+1}={data['diag'][i]}")
        sum_str = "+".join(str(v) for v in data["diag"])
        steps.append(f"T^i_i = {sum_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the tensor trace.

        Args:
            data: Solution data.

        Returns:
            Formatted trace value.
        """
        return f"T^i_i={data['trace']}"


# ── 2. Covariant derivative (tier 7) ─────────────────────────────────


@register
class CovariantDerivativeGenerator(StepGenerator):
    """Compute the covariant derivative of a vector field.

    Computes nabla_j V^i = dV^i/dx^j + Gamma^i_{jk} V^k for a 2D
    vector field V with given Christoffel symbol values at a point.

    Input format:
        ``compute covariant derivative of vector field``

    Target format:
        ``V=(2,3), dV^1/dx^1=1, Gamma^1_{11}=0.5, Gamma^1_{12}=0
        <step> nabla_1 V^1 = 1 + 0.5*2 + 0*3 = 2
        <step> nabla_1 V^2 = ...``

    Difficulty scaling:
        Difficulty 1-3: 1-2 non-zero Christoffel symbols.
        Difficulty 4-6: 2-3 non-zero symbols, larger values.
        Difficulty 7-8: 3-4 non-zero symbols.

    Prerequisites:
        christoffel_symbol (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "covariant_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["christoffel_symbol"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of non-zero symbols.

        Returns:
            Natural language description.
        """
        return "compute covariant derivative of vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a covariant derivative problem.

        Args:
            difficulty: Controls Christoffel symbol complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim = 2

        # Vector field components at the point
        v = [float(self._rng.randint(1, 5)) for _ in range(dim)]

        # Partial derivatives dV^i/dx^j
        dv = {}
        for i in range(dim):
            for j_idx in range(dim):
                dv[(i, j_idx)] = float(self._rng.randint(-3, 3))

        # Christoffel symbols Gamma^i_{jk}
        all_gamma_keys = []
        for i in range(dim):
            for j_idx in range(dim):
                for k_idx in range(dim):
                    all_gamma_keys.append((i, j_idx, k_idx))

        gamma = {key: 0.0 for key in all_gamma_keys}

        if difficulty <= 3:
            n_nonzero = self._rng.randint(1, 2)
            val_choices = [0.5, 1.0, -0.5, -1.0]
        elif difficulty <= 6:
            n_nonzero = self._rng.randint(2, 3)
            val_choices = [0.25, 0.5, 1.0, -0.5, 1.5, -1.0]
        else:
            n_nonzero = self._rng.randint(3, 4)
            val_choices = [0.25, 0.5, 0.75, 1.0, -0.5, -1.0, 1.5]

        chosen = self._rng.sample(all_gamma_keys, n_nonzero)
        for key in chosen:
            gamma[key] = self._rng.choice(val_choices)

        # Pick which direction j to differentiate along
        j_dir = self._rng.randint(0, dim - 1)

        # Compute nabla_j V^i for each i
        results = []
        for i in range(dim):
            val = dv[(i, j_dir)]
            connection_sum = 0.0
            for k_idx in range(dim):
                connection_sum += gamma[(i, j_dir, k_idx)] * v[k_idx]
            total = val + connection_sum
            results.append({
                "i": i, "partial": val,
                "connection": connection_sum, "total": total,
            })

        # Format non-zero gammas for display
        nonzero_gamma = {k: val for k, val in gamma.items() if abs(val) > 1e-10}
        gamma_str_parts = []
        for (gi, gj, gk), gval in nonzero_gamma.items():
            gamma_str_parts.append(
                f"\\Gamma^{gi+1}_{{{gj+1}{gk+1}}}={_fmt(gval)}"
            )

        v_str = ",".join(_fmt(vi) for vi in v)
        problem = (f"V=({v_str}), j={j_dir+1}, "
                   + ", ".join(gamma_str_parts[:4]))
        return problem, {
            "v": v, "dv": dv, "gamma": gamma, "j_dir": j_dir,
            "dim": dim, "results": results,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate covariant derivative computation steps.

        Args:
            data: Solution data with partial derivatives and connection.

        Returns:
            Steps showing partial + connection term evaluation.
        """
        steps = []
        j = data["j_dir"]
        for res in data["results"]:
            i = res["i"]
            steps.append(
                f"nabla_{j+1} V^{i+1} = "
                f"dV^{i+1}/dx^{j+1} + Gamma*V = "
                f"{_fmt(res['partial'])} + {_fmt(res['connection'])} "
                f"= {_fmt(res['total'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the covariant derivative components.

        Args:
            data: Solution data.

        Returns:
            Formatted covariant derivative values.
        """
        j = data["j_dir"]
        parts = [
            f"nabla_{j+1}V^{r['i']+1}={_fmt(r['total'])}"
            for r in data["results"]
        ]
        return ", ".join(parts)


# ── 3. Metric tensor (tier 6) ────────────────────────────────────────


@register
class MetricTensorGenerator(StepGenerator):
    """Compute the metric tensor for a coordinate transformation.

    Computes g_{ij} = sum_k (dx^k/du^i)(dx^k/du^j) for polar and
    cylindrical coordinate transformations. Evaluates at a given point.

    Input format:
        ``compute metric tensor for coordinate transformation``

    Target format:
        ``polar: x=r*cos(t), y=r*sin(t), at (r,t)=(2,pi/4) <step>
        dx/dr=cos(t)=0.7071, dx/dt=-r*sin(t)=-1.4142 <step>
        dy/dr=sin(t)=0.7071, dy/dt=r*cos(t)=1.4142 <step>
        g_11=cos^2+sin^2=1, g_12=0, g_22=r^2=4``

    Difficulty scaling:
        Difficulty 1-3: polar coordinates, simple angles.
        Difficulty 4-6: polar with general angles, or cylindrical.
        Difficulty 7-8: cylindrical with general coordinates.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "metric_tensor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coordinate system complexity.

        Returns:
            Natural language description.
        """
        return "compute metric tensor for coordinate transformation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a metric tensor problem.

        Args:
            difficulty: Controls coordinate type and parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            coord = "polar"
            r = float(self._rng.randint(1, 4))
            theta = self._rng.choice(
                [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]
            )
        elif difficulty <= 6:
            coord = self._rng.choice(["polar", "cylindrical"])
            r = float(self._rng.randint(1, 5))
            theta = round(
                self._rng.choice([math.pi / 6, math.pi / 4, math.pi / 3,
                                  math.pi / 2, math.pi]), 4
            )
        else:
            coord = "cylindrical"
            r = float(self._rng.randint(2, 6))
            theta = round(
                self._rng.choice([math.pi / 6, math.pi / 4, math.pi / 3,
                                  2 * math.pi / 3, math.pi]), 4
            )

        ct = math.cos(theta)
        st = math.sin(theta)

        if coord == "polar":
            # x = r*cos(t), y = r*sin(t)
            # Jacobian: [[cos(t), -r*sin(t)],
            #            [sin(t),  r*cos(t)]]
            jac = [[ct, -r * st],
                   [st, r * ct]]
            dim_u = 2
            dim_x = 2
            coord_names = ("r", "\\theta")
            problem = (f"polar: x=r\\cos\\theta, y=r\\sin\\theta, "
                       f"(r,\\theta)=({_fmt(r)},{_fmt(theta)})")
        else:
            # cylindrical: x=r*cos(t), y=r*sin(t), z=z
            # Jacobian (3x3 w.r.t. (r, theta, z)):
            # [[cos(t), -r*sin(t), 0],
            #  [sin(t),  r*cos(t), 0],
            #  [0,       0,        1]]
            z_val = float(self._rng.randint(1, 3))
            jac = [[ct, -r * st, 0.0],
                   [st, r * ct, 0.0],
                   [0.0, 0.0, 1.0]]
            dim_u = 3
            dim_x = 3
            coord_names = ("r", "\\theta", "z")
            problem = (f"cylindrical: x=r\\cos\\theta, y=r\\sin\\theta, z=z, "
                       f"(r,\\theta,z)=({_fmt(r)},{_fmt(theta)},{_fmt(z_val)})")

        # g_{ij} = sum_k jac[k][i] * jac[k][j]
        g = []
        for i in range(dim_u):
            row = []
            for j in range(dim_u):
                val = sum(jac[k][i] * jac[k][j] for k in range(dim_x))
                row.append(round(val, 4))
            g.append(row)

        return problem, {
            "coord": coord, "r": r, "theta": theta,
            "jac": jac, "g": g, "dim": dim_u,
            "coord_names": coord_names,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate metric tensor computation steps.

        Args:
            data: Solution data with Jacobian and metric entries.

        Returns:
            Steps showing Jacobian entries and g_{ij} computation.
        """
        steps = []
        dim = data["dim"]
        names = data["coord_names"]
        # Show Jacobian entries for first two coordinates
        for k in range(min(dim, 2)):
            row_str = ", ".join(
                f"dx^{k+1}/d{names[j]}={_fmt(data['jac'][k][j])}"
                for j in range(dim)
            )
            steps.append(row_str)
        # Show metric components
        for i in range(dim):
            for j in range(i, dim):
                steps.append(f"g_{{{i+1}{j+1}}}={_fmt(data['g'][i][j])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the metric tensor components.

        Args:
            data: Solution data.

        Returns:
            Formatted metric tensor entries.
        """
        dim = data["dim"]
        parts = []
        for i in range(dim):
            for j in range(i, dim):
                parts.append(f"g_{{{i+1}{j+1}}}={_fmt(data['g'][i][j])}")
        return ", ".join(parts)


# ── 4. Ricci tensor (tier 7) ─────────────────────────────────────────


@register
class RicciTensorGenerator(StepGenerator):
    """Compute Ricci tensor components from Riemann tensor values.

    Computes R_{ij} = R^k_{ikj} = sum_k R^k_{ikj} for a 2D space.
    Generates Riemann tensor components satisfying antisymmetry and
    contracts to obtain Ricci tensor.

    Input format:
        ``compute Ricci tensor from Riemann tensor``

    Target format:
        ``R^1_{121}=0.5, R^2_{122}=-0.3, ... <step>
        R_{11} = R^1_{111} + R^2_{112} = 0 + 0.2 = 0.2 <step>
        R_{12} = ... <step> R_{22} = ...``

    Difficulty scaling:
        Difficulty 1-3: 2D, 1-2 non-zero Riemann components.
        Difficulty 4-6: 2D, 2-3 non-zero components.
        Difficulty 7-8: 2D, 3-4 non-zero components, non-integer.

    Prerequisites:
        covariant_derivative (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ricci_tensor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["covariant_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of non-zero Riemann components.

        Returns:
            Natural language description.
        """
        return "compute Ricci tensor from Riemann tensor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Ricci tensor problem.

        For 2D, the independent Riemann components are limited by
        symmetries. We generate R^k_{lij} with antisymmetry in (i,j).

        Args:
            difficulty: Controls number and size of non-zero components.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim = 2

        # In 2D, R^k_{lij} is antisymmetric in i,j.
        # Independent components: k,l in {1,2}, (i,j) with i<j only.
        # For i<j only (1,2), so 4 independent components: R^k_{l12}
        all_keys = []
        for k in range(dim):
            for l_idx in range(dim):
                all_keys.append((k, l_idx))  # represents R^k_{l,1,2}

        riemann = {}
        for key in all_keys:
            riemann[key] = 0.0

        if difficulty <= 3:
            n_nonzero = self._rng.randint(1, 2)
            val_choices = [0.5, 1.0, -0.5, -1.0, 0.25]
        elif difficulty <= 6:
            n_nonzero = self._rng.randint(2, 3)
            val_choices = [0.25, 0.5, 1.0, -0.5, -1.0, 1.5, -0.25]
        else:
            n_nonzero = min(self._rng.randint(3, 4), len(all_keys))
            val_choices = [0.25, 0.5, 0.75, 1.0, -0.5, -0.75, -1.0, 1.5]

        chosen = self._rng.sample(all_keys, n_nonzero)
        for key in chosen:
            riemann[key] = self._rng.choice(val_choices)

        # Full Riemann tensor R^k_{l,i,j} with antisymmetry
        # R^k_{l,1,2} = riemann[(k,l)], R^k_{l,2,1} = -riemann[(k,l)]
        # R^k_{l,i,i} = 0

        # Ricci: R_{ij} = sum_k R^k_{ikj}
        ricci = {}
        ricci_steps = {}
        for i in range(dim):
            for j in range(dim):
                total = 0.0
                parts = []
                for k in range(dim):
                    # R^k_{i,k,j}: need to look up correctly
                    # This is R^k_{i,k,j}
                    # If k < j: R^k_{i,k,j} = riemann[(k,i)] when k=0,j=1
                    # If k > j: R^k_{i,k,j} = -riemann[(k,i)] when k=1,j=0
                    # If k == j: R^k_{i,k,j} = 0 (antisymmetry)
                    if k == j:
                        val = 0.0
                    elif k < j:
                        val = riemann.get((k, i), 0.0)
                    else:
                        val = -riemann.get((k, i), 0.0)
                    parts.append(f"R^{k+1}_{{{i+1}{k+1}{j+1}}}={_fmt(val)}")
                    total += val
                ricci[(i, j)] = round(total, 4)
                ricci_steps[(i, j)] = parts

        # Format problem
        nonzero_riemann = {k: v for k, v in riemann.items() if abs(v) > 1e-10}
        riem_str_parts = []
        for (k, l_idx), val in nonzero_riemann.items():
            riem_str_parts.append(
                f"R^{k+1}_{{{l_idx+1}12}}={_fmt(val)}"
            )
        problem = "R^k_{{lij}}: " + ", ".join(riem_str_parts[:4])

        return problem, {
            "dim": dim, "riemann": riemann,
            "ricci": ricci, "ricci_steps": ricci_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ricci tensor contraction steps.

        Args:
            data: Solution data with Riemann and Ricci components.

        Returns:
            Steps showing contraction for each R_{ij}.
        """
        steps = []
        dim = data["dim"]
        for i in range(dim):
            for j in range(dim):
                parts = data["ricci_steps"][(i, j)]
                steps.append(
                    f"R_{{{i+1}{j+1}}} = "
                    + " + ".join(parts)
                    + f" = {_fmt(data['ricci'][(i, j)])}"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Ricci tensor components.

        Args:
            data: Solution data.

        Returns:
            Formatted Ricci tensor entries.
        """
        dim = data["dim"]
        parts = []
        for i in range(dim):
            for j in range(i, dim):
                parts.append(
                    f"R_{{{i+1}{j+1}}}={_fmt(data['ricci'][(i, j)])}"
                )
        return ", ".join(parts)


# ── 5. Levi-Civita symbol (tier 5) ───────────────────────────────────


@register
class LeviCivitaGenerator(StepGenerator):
    """Evaluate the Levi-Civita symbol epsilon_{ijk} for a permutation.

    Returns +1 for even permutations, -1 for odd permutations, and 0
    if any indices are repeated. Covers 3D Levi-Civita symbol.

    Input format:
        ``evaluate Levi-Civita symbol``

    Target format:
        ``epsilon_{231} <step> permutation (2,3,1) <step>
        cycles: (1 2 3), 1 cycle of length 3 <step>
        inversions: 2 (even) <step> epsilon_{231} = +1``

    Difficulty scaling:
        Difficulty 1-3: identity and simple transpositions, some repeated.
        Difficulty 4-6: general permutations of (1,2,3).
        Difficulty 7-8: multiple evaluations or expressions using epsilon.

    Prerequisites:
        permutation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "levi_civita"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["permutation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of evaluations.

        Returns:
            Natural language description.
        """
        return "evaluate Levi-Civita symbol"

    def _count_inversions(self, perm: list[int]) -> int:
        """Count the number of inversions in a permutation.

        Args:
            perm: Permutation as a list of integers.

        Returns:
            Number of pairs (i, j) with i < j and perm[i] > perm[j].
        """
        count = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    count += 1
        return count

    def _eval_levi_civita(self, indices: list[int]) -> int:
        """Evaluate the Levi-Civita symbol for given indices.

        Args:
            indices: List of 3 indices (1-based).

        Returns:
            +1, -1, or 0.
        """
        if len(set(indices)) < len(indices):
            return 0
        inversions = self._count_inversions(indices)
        return 1 if inversions % 2 == 0 else -1

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Levi-Civita symbol evaluation problem.

        Args:
            difficulty: Controls number of evaluations and index patterns.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_evals = 1
            # Include some repeated-index cases
            candidates = [
                [1, 2, 3], [1, 1, 2], [2, 1, 3], [3, 2, 1],
                [1, 3, 2], [2, 2, 1],
            ]
        elif difficulty <= 6:
            n_evals = self._rng.choice([1, 2])
            candidates = [
                [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1],
                [3, 1, 2], [3, 2, 1], [1, 1, 3], [2, 2, 3],
            ]
        else:
            n_evals = self._rng.choice([2, 3])
            candidates = [
                [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1],
                [3, 1, 2], [3, 2, 1], [1, 1, 2], [3, 3, 1],
            ]

        chosen = self._rng.sample(candidates, min(n_evals, len(candidates)))
        evals = []
        for indices in chosen:
            val = self._eval_levi_civita(indices)
            inversions = self._count_inversions(indices)
            has_repeat = len(set(indices)) < 3
            evals.append({
                "indices": indices, "value": val,
                "inversions": inversions, "has_repeat": has_repeat,
            })

        idx_strs = [
            "\\epsilon_{" + "".join(str(i) for i in e["indices"]) + "}"
            for e in evals
        ]
        problem = ", ".join(idx_strs)
        return problem, {"evals": evals}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Levi-Civita evaluation steps.

        Args:
            data: Solution data with permutation analysis.

        Returns:
            Steps showing inversion count or repeat detection.
        """
        steps = []
        for ev in data["evals"]:
            idx_str = "".join(str(i) for i in ev["indices"])
            if ev["has_repeat"]:
                steps.append(
                    f"epsilon_{{{idx_str}}}: repeated index, = 0"
                )
            else:
                parity = "even" if ev["value"] == 1 else "odd"
                steps.append(
                    f"epsilon_{{{idx_str}}}: "
                    f"{ev['inversions']} inversions ({parity})"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Levi-Civita symbol values.

        Args:
            data: Solution data.

        Returns:
            Formatted epsilon values.
        """
        parts = []
        for ev in data["evals"]:
            idx_str = "".join(str(i) for i in ev["indices"])
            sign = "+" if ev["value"] >= 0 else ""
            parts.append(f"epsilon_{{{idx_str}}}={sign}{ev['value']}")
        return ", ".join(parts)


# ── 6. Index gymnastics (tier 6) ─────────────────────────────────────


@register
class IndexGymnasticsGenerator(StepGenerator):
    """Raise and lower tensor indices using a diagonal metric.

    Raises indices via V^i = g^{ij} V_j and lowers via V_i = g_{ij} V^j
    for a diagonal metric g_{ij} = diag(g_1, g_2, ...).

    Input format:
        ``raise/lower tensor indices with diagonal metric``

    Target format:
        ``V_i = (3, 5), g = diag(2, 4) <step>
        V^1 = g^{11}*V_1 = (1/2)*3 = 1.5 <step>
        V^2 = g^{22}*V_2 = (1/4)*5 = 1.25``

    Difficulty scaling:
        Difficulty 1-3: 2D, raise only, integer metric.
        Difficulty 4-6: 2D, raise or lower, moderate metric entries.
        Difficulty 7-8: 3D, both raise and lower.

    Prerequisites:
        metric_tensor (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "index_gymnastics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["metric_tensor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dimension and operation type.

        Returns:
            Natural language description.
        """
        return "raise/lower tensor indices with diagonal metric"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an index raising/lowering problem.

        Args:
            difficulty: Controls dimension and metric complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            dim = 2
            operation = "raise"
            g_diag = [float(self._rng.randint(1, 4)) for _ in range(dim)]
            v_lo, v_hi = -4, 5
        elif difficulty <= 6:
            dim = 2
            operation = self._rng.choice(["raise", "lower"])
            g_diag = [float(self._rng.randint(1, 5)) for _ in range(dim)]
            v_lo, v_hi = -5, 7
        else:
            dim = 3
            operation = self._rng.choice(["raise", "lower"])
            g_diag = [float(self._rng.randint(1, 4)) for _ in range(dim)]
            v_lo, v_hi = -6, 8

        v_in = [float(self._rng.randint(v_lo, v_hi)) for _ in range(dim)]

        if operation == "raise":
            # V^i = g^{ii} * V_i = (1/g_{ii}) * V_i
            v_out = [v_in[i] / g_diag[i] for i in range(dim)]
            in_label = "V_i"
            out_label = "V^i"
        else:
            # V_i = g_{ii} * V^i
            v_out = [g_diag[i] * v_in[i] for i in range(dim)]
            in_label = "V^i"
            out_label = "V_i"

        v_out = [round(v, 4) for v in v_out]

        g_str = ",".join(_fmt(g) for g in g_diag)
        v_str = ",".join(_fmt(v) for v in v_in)
        problem = (f"{operation} indices: {in_label}=({v_str}), "
                   f"g=diag({g_str})")
        return problem, {
            "dim": dim, "operation": operation,
            "g_diag": g_diag, "v_in": v_in, "v_out": v_out,
            "in_label": in_label, "out_label": out_label,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate index gymnastics steps.

        Args:
            data: Solution data with metric and vector entries.

        Returns:
            Steps showing each component computation.
        """
        steps = []
        for i in range(data["dim"]):
            g_val = data["g_diag"][i]
            v_val = data["v_in"][i]
            if data["operation"] == "raise":
                factor = 1.0 / g_val
                steps.append(
                    f"{data['out_label'][:-1]}{i+1} = "
                    f"g^{{{i+1}{i+1}}}*V_{i+1} = "
                    f"{_fmt(factor)}*{_fmt(v_val)} = {_fmt(data['v_out'][i])}"
                )
            else:
                steps.append(
                    f"{data['out_label'][:-1]}{i+1} = "
                    f"g_{{{i+1}{i+1}}}*V^{i+1} = "
                    f"{_fmt(g_val)}*{_fmt(v_val)} = {_fmt(data['v_out'][i])}"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the raised/lowered vector components.

        Args:
            data: Solution data.

        Returns:
            Formatted output vector.
        """
        v_str = ",".join(_fmt(v) for v in data["v_out"])
        return f"{data['out_label']}=({v_str})"
