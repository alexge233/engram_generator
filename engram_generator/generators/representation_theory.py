"""Representation theory generators.

6 generators covering character computation, character tables, irreducibility
checks, representation decomposition, tensor product of representations,
and Schur's lemma application across tiers 6-7. Works with small finite
groups (Z_2, Z_3, Z_4, S_3) and their matrix representations.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _mat_trace(matrix: list[list[complex]]) -> complex:
    """Compute the trace of a square matrix.

    Args:
        matrix: Square matrix as a list of lists.

    Returns:
        Sum of diagonal elements.
    """
    return sum(matrix[i][i] for i in range(len(matrix)))


def _format_complex(z: complex, places: int = 4) -> str:
    """Format a complex number as a readable string.

    Args:
        z: Complex number.
        places: Decimal places for rounding.

    Returns:
        String like '1', '-1', '0.5+0.866i', etc.
    """
    re = round(z.real, places)
    im = round(z.imag, places)
    if im == 0:
        if re == int(re):
            return str(int(re))
        return str(re)
    if re == 0:
        if im == 1:
            return "i"
        if im == -1:
            return "-i"
        if im == int(im):
            return f"{int(im)}i"
        return f"{im}i"
    im_str = f"+{im}i" if im > 0 else f"{im}i"
    if re == int(re):
        return f"{int(re)}{im_str}"
    return f"{re}{im_str}"


def _root_of_unity(k: int, n: int) -> complex:
    """Compute e^{2*pi*i*k/n}.

    Args:
        k: Exponent numerator.
        n: Root order.

    Returns:
        Complex root of unity.
    """
    theta = 2 * math.pi * k / n
    return complex(round(math.cos(theta), 8), round(math.sin(theta), 8))


def _zn_rep_matrix(g: int, irrep_index: int, n: int) -> list[list[complex]]:
    """Build 1x1 matrix representation of g in Z_n irrep j.

    The j-th irreducible representation of Z_n maps g to
    omega^{j*g} where omega = e^{2*pi*i/n}.

    Args:
        g: Group element (0 to n-1).
        irrep_index: Index of the irreducible representation.
        n: Order of the cyclic group.

    Returns:
        1x1 matrix [[omega^{j*g}]].
    """
    val = _root_of_unity(irrep_index * g, n)
    return [[val]]


def _s3_elements() -> list[tuple[str, list[list[complex]]]]:
    """Return S_3 elements with their 2D standard representation matrices.

    The standard (2D) representation of S_3 uses the matrices for the
    generators s = (1 2 3) and t = (1 2), then derives all 6 elements.

    Returns:
        List of (label, 2x2_matrix) tuples for all 6 elements of S_3.
    """
    s30 = 0.5 * math.sqrt(3)
    e = [[1, 0], [0, 1]]
    r = [[-0.5, -s30], [s30, -0.5]]
    r2 = [[-0.5, s30], [-s30, -0.5]]
    t = [[1, 0], [0, -1]]
    tr = [[-0.5, s30], [s30, 0.5]]
    tr2 = [[-0.5, -s30], [-s30, 0.5]]
    elements = [
        ("e", [[complex(c) for c in row] for row in e]),
        ("r", [[complex(c) for c in row] for row in r]),
        ("r2", [[complex(c) for c in row] for row in r2]),
        ("t", [[complex(c) for c in row] for row in t]),
        ("tr", [[complex(c) for c in row] for row in tr]),
        ("tr2", [[complex(c) for c in row] for row in tr2]),
    ]
    return elements


# ═══════════════════════════════════════════════════════════════════
# 1. CHARACTER COMPUTE (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class CharacterComputeGenerator(StepGenerator):
    """Compute the character chi(g) = Tr(rho(g)) for a matrix representation.

    Given a group element g from a small group (Z_2, Z_3, or S_3) and
    a matrix representation rho, computes the character value by taking
    the trace of the representation matrix.

    Difficulty scaling:
        Difficulty 1-3: Z_2 (1x1 matrices).
        Difficulty 4-6: Z_3 (1x1 matrices, roots of unity).
        Difficulty 7-8: S_3 (2x2 real matrices).

    Prerequisites:
        matrix_trace (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "character_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "compute character chi(g) = Tr(rho(g))"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a character computation problem.

        Args:
            difficulty: Controls which group is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._z2_problem()
        if difficulty <= 6:
            return self._z3_problem()
        return self._s3_problem()

    def _z2_problem(self) -> tuple[str, dict]:
        """Generate a Z_2 character computation problem.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        g = self._rng.randint(0, 1)
        j = self._rng.randint(0, 1)
        mat = _zn_rep_matrix(g, j, 2)
        trace = _mat_trace(mat)
        problem = f"Z_2, irrep {j}, g={g}: compute chi(g)=Tr(rho(g))"
        return problem, {
            "group": "Z_2", "g_label": str(g), "irrep": j,
            "matrix": mat, "trace": trace,
        }

    def _z3_problem(self) -> tuple[str, dict]:
        """Generate a Z_3 character computation problem.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        g = self._rng.randint(0, 2)
        j = self._rng.randint(0, 2)
        mat = _zn_rep_matrix(g, j, 3)
        trace = _mat_trace(mat)
        problem = f"Z_3, irrep {j}, g={g}: compute chi(g)=Tr(rho(g))"
        return problem, {
            "group": "Z_3", "g_label": str(g), "irrep": j,
            "matrix": mat, "trace": trace,
        }

    def _s3_problem(self) -> tuple[str, dict]:
        """Generate an S_3 character computation problem.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        elements = _s3_elements()
        label, mat = self._rng.choice(elements)
        trace = _mat_trace(mat)
        problem = f"S_3, standard rep, g={label}: compute chi(g)=Tr(rho(g))"
        return problem, {
            "group": "S_3", "g_label": label, "irrep": "std",
            "matrix": mat, "trace": trace,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate character computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the matrix and trace computation.
        """
        mat = data["matrix"]
        n = len(mat)
        diag_parts = []
        for i in range(n):
            diag_parts.append(_format_complex(mat[i][i]))
        diag_str = " + ".join(diag_parts)
        trace_str = _format_complex(data["trace"])
        return [
            f"rho({data['g_label']}) diagonal: {diag_str}",
            f"chi({data['g_label']}) = Tr = {trace_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the character value.

        Args:
            data: Solution data.

        Returns:
            Formatted character value.
        """
        return _format_complex(data["trace"])


# ═══════════════════════════════════════════════════════════════════
# 2. CHARACTER TABLE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class CharacterTableGenerator(StepGenerator):
    """Build the character table for Z_n (n=2,3,4).

    Rows correspond to irreducible representations, columns to conjugacy
    classes (which are singleton sets in abelian groups). Entries are
    roots of unity omega^{j*g} where omega = e^{2*pi*i/n}.

    Difficulty scaling:
        Difficulty 1-3: Z_2 (2x2 table).
        Difficulty 4-6: Z_3 (3x3 table).
        Difficulty 7-8: Z_4 (4x4 table).

    Prerequisites:
        character_compute (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "character_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["character_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        n = self._select_n(difficulty)
        return f"build character table for Z_{n}"

    def _select_n(self, difficulty: int) -> int:
        """Choose cyclic group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n in {2, 3, 4}.
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a character table problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        table = []
        for j in range(n):
            row = []
            for g in range(n):
                row.append(_root_of_unity(j * g, n))
            table.append(row)

        problem = f"Z_{n}: build the full character table"
        return problem, {"n": n, "table": table}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate character table construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each row of the character table.
        """
        n = data["n"]
        steps = [f"omega = e^{{2*pi*i/{n}}}"]
        for j in range(n):
            entries = [_format_complex(data["table"][j][g]) for g in range(n)]
            steps.append(f"chi_{j}: [{', '.join(entries)}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the character table in compact form.

        Args:
            data: Solution data.

        Returns:
            Semicolon-separated rows of the character table.
        """
        n = data["n"]
        rows = []
        for j in range(n):
            entries = [_format_complex(data["table"][j][g]) for g in range(n)]
            rows.append(",".join(entries))
        return "; ".join(rows)


# ═══════════════════════════════════════════════════════════════════
# 3. IRREDUCIBLE CHECK (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class IrreducibleCheckGenerator(StepGenerator):
    """Check if a representation is irreducible using the inner product test.

    A representation with character chi is irreducible iff
    <chi, chi> = (1/|G|) * sum_{g in G} chi(g) * conj(chi(g)) = 1.

    Generates either a single irrep (irreducible) or a direct sum of
    two irreps (reducible) for Z_n groups.

    Difficulty scaling:
        Difficulty 1-3: Z_2, single irrep (always irreducible).
        Difficulty 4-6: Z_3, sometimes reducible (direct sum of two irreps).
        Difficulty 7-8: Z_4, sometimes reducible.

    Prerequisites:
        character_table (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "irreducible_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["character_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "check if representation is irreducible via <chi,chi>=1"

    def _select_n(self, difficulty: int) -> int:
        """Choose cyclic group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n in {2, 3, 4}.
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an irreducibility check problem.

        Args:
            difficulty: Controls group size and reducibility.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        make_reducible = difficulty > 3 and self._rng.random() < 0.5

        if make_reducible:
            j1 = self._rng.randint(0, n - 1)
            j2 = self._rng.randint(0, n - 1)
            chi = []
            for g in range(n):
                val = _root_of_unity(j1 * g, n) + _root_of_unity(j2 * g, n)
                chi.append(val)
            label = f"chi_{j1}+chi_{j2}"
        else:
            j1 = self._rng.randint(0, n - 1)
            j2 = None
            chi = [_root_of_unity(j1 * g, n) for g in range(n)]
            label = f"chi_{j1}"

        inner = sum(c * c.conjugate() for c in chi) / n
        inner_real = round(inner.real, 4)
        is_irreducible = abs(inner_real - 1.0) < 1e-6

        chi_str = ", ".join(_format_complex(c) for c in chi)
        problem = f"Z_{n}, chi=[{chi_str}]: is this irreducible?"
        return problem, {
            "n": n, "chi": chi, "label": label,
            "inner_product": inner_real,
            "is_irreducible": is_irreducible,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate irreducibility check steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing inner product computation.
        """
        n = data["n"]
        chi = data["chi"]
        products = []
        for g in range(n):
            val = chi[g] * chi[g].conjugate()
            products.append(_format_complex(val))
        sum_str = " + ".join(products)
        ip = data["inner_product"]
        return [
            f"|chi(g)|^2 for each g: {sum_str}",
            f"<chi,chi> = ({sum_str})/{n} = {round(ip, 4)}",
            f"{'= 1 => irreducible' if data['is_irreducible'] else '!= 1 => reducible'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the irreducibility verdict.

        Args:
            data: Solution data.

        Returns:
            YES or NO with the inner product value.
        """
        ip = round(data["inner_product"], 4)
        if data["is_irreducible"]:
            return f"YES, <chi,chi>={ip}"
        return f"NO, <chi,chi>={ip}"


# ═══════════════════════════════════════════════════════════════════
# 4. DECOMPOSE REPRESENTATION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class DecomposeRepGenerator(StepGenerator):
    """Decompose a representation into irreducible components.

    Given a character chi of a representation of Z_n, computes the
    multiplicity of each irreducible: n_i = <chi, chi_i> =
    (1/|G|) * sum_{g} chi(g) * conj(chi_i(g)).

    Difficulty scaling:
        Difficulty 1-3: Z_2, sum of 2 irreps.
        Difficulty 4-6: Z_3, sum of 2 irreps.
        Difficulty 7-8: Z_3 or Z_4, sum of 2-3 irreps.

    Prerequisites:
        irreducible_check (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "decompose_rep"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["irreducible_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "decompose representation into irreducibles"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a representation decomposition problem.

        Args:
            difficulty: Controls group size and number of components.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
            num_parts = 2
        elif difficulty <= 6:
            n = 3
            num_parts = 2
        else:
            n = self._rng.choice([3, 4])
            num_parts = self._rng.randint(2, 3)

        components = [self._rng.randint(0, n - 1) for _ in range(num_parts)]
        chi = [complex(0)] * n
        for g in range(n):
            for j in components:
                chi[g] += _root_of_unity(j * g, n)

        multiplicities = []
        for j in range(n):
            inner = sum(
                chi[g] * _root_of_unity(-j * g, n) for g in range(n)
            ) / n
            multiplicities.append(round(inner.real))

        chi_str = ", ".join(_format_complex(c) for c in chi)
        problem = f"Z_{n}, chi=[{chi_str}]: decompose into irreducibles"
        return problem, {
            "n": n, "chi": chi, "components": components,
            "multiplicities": multiplicities,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate decomposition steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing multiplicity computation for each irrep.
        """
        n = data["n"]
        steps = []
        for j in range(n):
            m = data["multiplicities"][j]
            steps.append(f"n_{j} = <chi, chi_{j}> = {m}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decomposition as a direct sum.

        Args:
            data: Solution data.

        Returns:
            String like 'chi_0 + 2*chi_1'.
        """
        n = data["n"]
        parts = []
        for j in range(n):
            m = data["multiplicities"][j]
            if m == 0:
                continue
            if m == 1:
                parts.append(f"chi_{j}")
            else:
                parts.append(f"{m}*chi_{j}")
        return " + ".join(parts) if parts else "0"


# ═══════════════════════════════════════════════════════════════════
# 5. TENSOR PRODUCT OF REPRESENTATIONS (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class TensorRepGenerator(StepGenerator):
    """Compute the tensor product of two representations via characters.

    For representations V and W of Z_n, the character of their tensor
    product satisfies chi_{V tensor W}(g) = chi_V(g) * chi_W(g).

    Difficulty scaling:
        Difficulty 1-3: Z_2, two 1D irreps.
        Difficulty 4-6: Z_3, two 1D irreps.
        Difficulty 7-8: Z_4, two 1D irreps with complex roots.

    Prerequisites:
        tensor_product (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tensor_rep"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["tensor_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "compute tensor product of representations via characters"

    def _select_n(self, difficulty: int) -> int:
        """Choose cyclic group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n in {2, 3, 4}.
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tensor product of representations problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        j_v = self._rng.randint(0, n - 1)
        j_w = self._rng.randint(0, n - 1)

        chi_v = [_root_of_unity(j_v * g, n) for g in range(n)]
        chi_w = [_root_of_unity(j_w * g, n) for g in range(n)]
        chi_prod = [chi_v[g] * chi_w[g] for g in range(n)]

        j_result = (j_v + j_w) % n

        v_str = ", ".join(_format_complex(c) for c in chi_v)
        w_str = ", ".join(_format_complex(c) for c in chi_w)
        problem = (
            f"Z_{n}: V=chi_{j_v} [{v_str}], W=chi_{j_w} [{w_str}]. "
            f"Compute chi_{{V tensor W}}"
        )
        return problem, {
            "n": n, "j_v": j_v, "j_w": j_w, "j_result": j_result,
            "chi_v": chi_v, "chi_w": chi_w, "chi_prod": chi_prod,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tensor product computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing pointwise multiplication.
        """
        n = data["n"]
        steps = []
        for g in range(n):
            v_str = _format_complex(data["chi_v"][g])
            w_str = _format_complex(data["chi_w"][g])
            p_str = _format_complex(data["chi_prod"][g])
            steps.append(f"g={g}: {v_str} * {w_str} = {p_str}")
        steps.append(
            f"chi_{{V tensor W}} = chi_{data['j_result']} "
            f"(irrep {data['j_result']} of Z_{n})"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the tensor product character.

        Args:
            data: Solution data.

        Returns:
            String identifying the resulting irrep.
        """
        prod_str = ", ".join(_format_complex(c) for c in data["chi_prod"])
        return f"chi_{data['j_result']} = [{prod_str}]"


# ═══════════════════════════════════════════════════════════════════
# 6. SCHUR'S LEMMA APPLICATION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class SchurLemmaApplyGenerator(StepGenerator):
    """Apply Schur's lemma to determine if a morphism is zero or iso.

    Schur's lemma states that a G-equivariant map f: V -> W between
    irreducible representations is either zero (if V not iso to W) or
    a scalar multiple of identity (if V iso to W). This generator
    presents two irreps of Z_n and asks for the conclusion.

    Difficulty scaling:
        Difficulty 1-3: Z_2, two irreps.
        Difficulty 4-6: Z_3, two irreps.
        Difficulty 7-8: Z_4, two irreps.

    Prerequisites:
        irreducible_check (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "schur_lemma_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["irreducible_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "apply Schur's lemma to morphism between irreps"

    def _select_n(self, difficulty: int) -> int:
        """Choose cyclic group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n in {2, 3, 4}.
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Schur's lemma application problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        j_v = self._rng.randint(0, n - 1)
        j_w = self._rng.randint(0, n - 1)

        is_isomorphic = (j_v == j_w)

        chi_v = [_root_of_unity(j_v * g, n) for g in range(n)]
        chi_w = [_root_of_unity(j_w * g, n) for g in range(n)]

        inner = sum(
            chi_v[g] * chi_w[g].conjugate() for g in range(n)
        ) / n
        inner_real = round(inner.real, 4)

        problem = (
            f"Z_{n}: f: V(chi_{j_v}) -> W(chi_{j_w}), "
            f"both irreducible. Apply Schur's lemma."
        )
        return problem, {
            "n": n, "j_v": j_v, "j_w": j_w,
            "is_isomorphic": is_isomorphic,
            "chi_v": chi_v, "chi_w": chi_w,
            "inner_product": inner_real,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Schur's lemma application steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the inner product and conclusion.
        """
        j_v = data["j_v"]
        j_w = data["j_w"]
        ip = data["inner_product"]
        steps = [
            f"V = chi_{j_v} (irreducible), W = chi_{j_w} (irreducible)",
            f"<chi_V, chi_W> = {ip}",
        ]
        if data["is_isomorphic"]:
            steps.append(
                f"V ~ W (same irrep {j_v}): f = lambda*Id (scalar)"
            )
        else:
            steps.append(
                f"V not iso to W ({j_v} != {j_w}): f = 0"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Schur's lemma conclusion.

        Args:
            data: Solution data.

        Returns:
            'isomorphism (scalar)' or 'zero map'.
        """
        if data["is_isomorphic"]:
            return "isomorphism (scalar multiple of identity)"
        return "zero map"
