"""Homological algebra generators.

10 generators across tiers 7-8 covering chain complexes, homology
computation, exact sequences, snake lemma, Ext/Tor functors, free
resolutions, Euler characteristic, Betti numbers, and Mayer-Vietoris.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _gcd(a: int, b: int) -> int:
    """Compute greatest common divisor.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        GCD of a and b.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def _mat_mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    """Multiply two integer matrices.

    Args:
        a: First matrix (rows x cols).
        b: Second matrix (cols x cols2).

    Returns:
        Product matrix.
    """
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result


def _is_zero_matrix(m: list[list[int]]) -> bool:
    """Check if a matrix is all zeros.

    Args:
        m: Integer matrix.

    Returns:
        True if every entry is zero.
    """
    return all(m[i][j] == 0 for i in range(len(m)) for j in range(len(m[0])))


def _mat_str(m: list[list[int]]) -> str:
    """Format matrix as a compact string.

    Args:
        m: Integer matrix.

    Returns:
        String like ``[[1, 0], [0, 1]]``.
    """
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in m) + "]"


def _rank_mod0(m: list[list[int]]) -> int:
    """Compute rank of an integer matrix over Q via row reduction.

    Args:
        m: Integer matrix.

    Returns:
        Rank of the matrix.
    """
    if not m or not m[0]:
        return 0
    rows = len(m)
    cols = len(m[0])
    mat = [row[:] for row in m]
    # Use float for elimination
    fmat = [[float(v) for v in row] for row in mat]
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if abs(fmat[row][col]) > 1e-9:
                pivot = row
                break
        if pivot is None:
            continue
        fmat[rank], fmat[pivot] = fmat[pivot], fmat[rank]
        scale = fmat[rank][col]
        for j in range(cols):
            fmat[rank][j] /= scale
        for row in range(rows):
            if row != rank and abs(fmat[row][col]) > 1e-9:
                factor = fmat[row][col]
                for j in range(cols):
                    fmat[row][j] -= factor * fmat[rank][j]
        rank += 1
    return rank


# ═══════════════════════════════════════════════════════════════════
# 1. CHAIN COMPLEX (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class ChainComplexGenerator(StepGenerator):
    """Verify d_{n-1} . d_n = 0 for maps between Z^k spaces.

    Given two integer matrices representing boundary maps in a chain
    complex, verify that their composition is the zero matrix. Matrices
    are chosen so the property always holds.

    Difficulty scaling:
        Difficulty 1-3: 2x2 and 2x2 matrices.
        Difficulty 4-6: 2x3 and 3x2 matrices.
        Difficulty 7-8: 3x3 and 3x3 matrices.

    Prerequisites:
        matrix_multiply (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chain_complex"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls matrix dimensions.

        Returns:
            Task description string.
        """
        return "verify chain complex condition d_{n-1} . d_n = 0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chain complex verification problem.

        The matrices are constructed so d_{n-1} . d_n = 0 always.

        Args:
            difficulty: Controls matrix size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # d1: 2x2, d0: 2x2, ensure d0 * d1 = 0
            a = self._rng.randint(-3, 3)
            b = self._rng.randint(-3, 3)
            d1 = [[a, b], [-b, a]]
            d0 = [[b, -a], [a, b]] if (a == 0 and b == 0) else [[b, -a], [-a, -b]]
            # Force d0 * d1 = 0 by construction
            d0 = [[0, 0], [0, 0]] if not _is_zero_matrix(_mat_mul(d0, d1)) else d0
            if not _is_zero_matrix(_mat_mul(d0, d1)):
                d0 = [[-b, a], [0, 0]]
                if not _is_zero_matrix(_mat_mul(d0, d1)):
                    d1 = [[1, 0], [0, 0]]
                    d0 = [[0, 1], [0, 0]]
        elif difficulty <= 6:
            # Use kernel trick: d0 rows are in left null space of d1
            c = self._rng.randint(1, 3)
            d1 = [[c, 0], [0, c], [0, 0]]
            d0 = [[0, 0, 1], [0, 0, 0]]
            if not _is_zero_matrix(_mat_mul(d0, d1)):
                d0 = [[0, 0, 1], [0, 0, 0]]
                d1 = [[0, 0], [0, 0], [0, 0]]
        else:
            v = self._rng.randint(1, 3)
            d1 = [[v, 0, 0], [0, v, 0], [0, 0, 0]]
            d0 = [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
            if not _is_zero_matrix(_mat_mul(d0, d1)):
                d0 = [[0, 0, v], [0, 0, 0], [0, 0, 0]]
                d1 = [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
                if not _is_zero_matrix(_mat_mul(d0, d1)):
                    d1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        product = _mat_mul(d0, d1)
        problem = (
            f"Chain complex: C_2 --d1--> C_1 --d0--> C_0. "
            f"d1 = {_mat_str(d1)}, d0 = {_mat_str(d0)}. "
            f"Verify d0 . d1 = 0."
        )
        return problem, {
            "d0": d0, "d1": d1, "product": product,
            "is_zero": _is_zero_matrix(product),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the matrix product and zero check.
        """
        return [
            f"d0 = {_mat_str(data['d0'])}",
            f"d1 = {_mat_str(data['d1'])}",
            f"d0 . d1 = {_mat_str(data['product'])}",
            f"all entries zero: {data['is_zero']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the verification result.

        Args:
            data: Solution data.

        Returns:
            Whether chain complex condition holds.
        """
        return "d0 . d1 = 0, chain complex verified" if data["is_zero"] else "FAIL"


# ═══════════════════════════════════════════════════════════════════
# 2. HOMOLOGY COMPUTE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class HomologyComputeGenerator(StepGenerator):
    """Compute homology H_n = ker(d_n) / im(d_{n+1}).

    For a simple chain complex with small integer matrices, compute
    the rank of the kernel and image to determine the homology group.

    Difficulty scaling:
        Difficulty 1-3: trivial maps (zero matrices), H_n = Z^k.
        Difficulty 4-6: one non-trivial map, compute kernel rank.
        Difficulty 7-8: both maps non-trivial, full computation.

    Prerequisites:
        chain_complex (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "homology_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["chain_complex"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls chain complex complexity.

        Returns:
            Task description string.
        """
        return "compute homology group H_n from chain complex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a homology computation problem.

        Args:
            difficulty: Controls map complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # 0 -> Z^2 --0--> Z^2 -> 0, so H = Z^2
            dim = 2
            d_out = [[0] * dim for _ in range(dim)]
            d_in = [[0] * dim for _ in range(dim)]
        elif difficulty <= 6:
            # Z^2 --d_in--> Z^2 --0--> Z^2
            n = self._rng.randint(2, 4)
            d_in = [[n, 0], [0, 0]]
            d_out = [[0, 0], [0, 0]]
        else:
            n = self._rng.randint(2, 4)
            d_in = [[n, 0], [0, n]]
            d_out = [[0, 0], [0, 0]]

        dim_c = len(d_out)
        rank_d_out = _rank_mod0(d_out)
        rank_d_in = _rank_mod0(d_in)
        ker_rank = dim_c - rank_d_out
        h_rank = ker_rank - rank_d_in

        problem = (
            f"Chain: C_{{n+1}} --d_in={_mat_str(d_in)}--> "
            f"C_n (Z^{dim_c}) --d_out={_mat_str(d_out)}--> C_{{n-1}}. "
            f"Compute H_n."
        )
        return problem, {
            "d_in": d_in, "d_out": d_out, "dim": dim_c,
            "rank_d_out": rank_d_out, "rank_d_in": rank_d_in,
            "ker_rank": ker_rank, "h_rank": h_rank,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate homology computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing kernel, image, and quotient.
        """
        return [
            f"dim(C_n) = {data['dim']}",
            f"rank(d_out) = {data['rank_d_out']}",
            f"ker(d_out) rank = {data['dim']} - {data['rank_d_out']} = {data['ker_rank']}",
            f"rank(d_in) = im(d_in) rank = {data['rank_d_in']}",
            f"H_n rank = {data['ker_rank']} - {data['rank_d_in']} = {data['h_rank']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the homology group.

        Args:
            data: Solution data.

        Returns:
            Homology group description.
        """
        r = data["h_rank"]
        if r == 0:
            return "H_n = 0"
        return f"H_n = Z^{r}" if r > 1 else "H_n = Z"


# ═══════════════════════════════════════════════════════════════════
# 3. EXACT SEQUENCE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class ExactSequenceGenerator(StepGenerator):
    """Verify that a short exact sequence 0 -> A -> B -> C -> 0 is exact.

    For small abelian groups (Z, Z_n), checks that im(f) = ker(g) at
    each position. Uses the inclusion-quotient pattern.

    Difficulty scaling:
        Difficulty 1-3: 0 -> Z --*n--> Z --mod n--> Z/nZ -> 0, n in [2,4].
        Difficulty 4-6: n in [3,6].
        Difficulty 7-8: n in [4,8].

    Prerequisites:
        kernel_compute (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exact_sequence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["kernel_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls n.

        Returns:
            Task description string.
        """
        return "verify short exact sequence is exact at each position"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exact sequence verification problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            n = self._rng.randint(3, 6)
        else:
            n = self._rng.randint(4, 8)

        problem = (
            f"0 -> Z --f(*{n})--> Z --g(mod {n})--> Z/{n}Z -> 0. "
            f"Verify exactness at each position."
        )
        return problem, {
            "n": n,
            "f_desc": f"f(x) = {n}x",
            "g_desc": f"g(x) = x mod {n}",
            "ker_g": f"{n}Z",
            "im_f": f"{n}Z",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate exactness verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking exactness at each node.
        """
        n = data["n"]
        return [
            f"at Z (left): ker(f) = {{0}} (f injective), im(0->Z) = {{0}}. exact.",
            f"at Z (middle): im(f) = {n}Z, ker(g) = {n}Z. im(f) = ker(g). exact.",
            f"at Z/{n}Z: im(g) = Z/{n}Z (g surjective), ker(Z/{n}Z->0) = Z/{n}Z. exact.",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the exactness result.

        Args:
            data: Solution data.

        Returns:
            Confirmation of exactness.
        """
        return f"sequence is exact: im = ker at all positions"


# ═══════════════════════════════════════════════════════════════════
# 4. SNAKE LEMMA (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class SnakeLemmaGenerator(StepGenerator):
    """Apply the snake lemma to a commutative diagram with exact rows.

    Given two short exact sequences connected by vertical maps, identify
    the connecting homomorphism and the induced long exact sequence on
    kernels and cokernels. Template-based using Z-module maps.

    Difficulty scaling:
        Difficulty 1-4: multiplication-by-n maps, small n.
        Difficulty 5-6: larger n.
        Difficulty 7-8: composite maps.

    Prerequisites:
        exact_sequence (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "snake_lemma"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exact_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls map complexity.

        Returns:
            Task description string.
        """
        return "identify connecting homomorphism via the snake lemma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a snake lemma problem.

        Uses 0 -> Z --*m--> Z --mod m--> Z/mZ -> 0 with vertical
        multiplication-by-n maps.

        Args:
            difficulty: Controls m, n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            m = self._rng.randint(2, 4)
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            m = self._rng.randint(3, 6)
            n = self._rng.randint(3, 6)
        else:
            m = self._rng.randint(4, 8)
            n = self._rng.randint(4, 8)

        g = _gcd(m, n)
        # Connecting map delta: ker(coker(alpha)) -> coker(ker(alpha))
        # For *n maps: delta: Z/gcd(m,n)Z -> Z/gcd(m,n)Z
        problem = (
            f"Rows: 0->Z--*{m}-->Z--mod {m}-->Z/{m}Z->0. "
            f"Vertical maps: *{n}. Apply snake lemma."
        )
        return problem, {
            "m": m, "n": n, "g": g,
            "ker_alpha": "0", "ker_beta": "0", "ker_gamma": f"Z/{g}Z" if g > 1 else "0",
            "coker_alpha": f"Z/{n}Z", "coker_beta": f"Z/{n}Z",
            "coker_gamma": f"Z/{(m // g)}Z" if m // g > 1 else "0",
            "delta": f"Z/{g}Z -> Z/{n}Z" if g > 1 else "0 -> Z/{n}Z",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate snake lemma steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing kernels, cokernels, and connecting map.
        """
        m, n, g = data["m"], data["n"], data["g"]
        return [
            f"ker(*{n} on Z) = 0, ker(*{n} on Z) = 0, ker(*{n} on Z/{m}Z) = {data['ker_gamma']}",
            f"coker(*{n} on Z) = Z/{n}Z, coker(*{n} on Z/{m}Z) = {data['coker_gamma']}",
            f"snake: 0 -> 0 -> 0 -> {data['ker_gamma']} --delta--> Z/{n}Z -> Z/{n}Z -> {data['coker_gamma']} -> 0",
            f"connecting map delta: {data['delta']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the connecting homomorphism.

        Args:
            data: Solution data.

        Returns:
            Description of the connecting map.
        """
        return f"delta: {data['delta']}"


# ═══════════════════════════════════════════════════════════════════
# 5. EXT FUNCTOR (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class ExtFunctorGenerator(StepGenerator):
    """Compute Ext^1(Z/nZ, Z) using a projective resolution.

    Uses the standard resolution 0 -> Z --*n--> Z -> Z/nZ -> 0
    and applies Hom(-, Z) to compute Ext^1(Z/nZ, Z) = Z/nZ.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 4].
        Difficulty 4-6: n in [3, 8].
        Difficulty 7-8: n in [5, 12].

    Prerequisites:
        exact_sequence (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ext_functor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exact_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls n.

        Returns:
            Task description string.
        """
        return "compute Ext^1(Z/nZ, Z) via projective resolution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ext functor problem.

        Args:
            difficulty: Controls n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            n = self._rng.randint(3, 8)
        else:
            n = self._rng.randint(5, 12)

        problem = (
            f"Projective resolution: 0 -> Z --*{n}--> Z -> Z/{n}Z -> 0. "
            f"Compute Ext^1(Z/{n}Z, Z)."
        )
        return problem, {
            "n": n,
            "resolution": f"0 -> Z --*{n}--> Z -> Z/{n}Z -> 0",
            "hom_complex": f"0 -> Hom(Z,Z) --*{n}--> Hom(Z,Z) -> 0",
            "result": f"Z/{n}Z",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ext computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing resolution and Hom application.
        """
        n = data["n"]
        return [
            f"resolution: {data['resolution']}",
            f"apply Hom(-, Z): {data['hom_complex']}",
            f"Hom(Z, Z) = Z, so complex is: 0 -> Z --*{n}--> Z -> 0",
            f"Ext^1 = coker(*{n}) = Z/{n}Z",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Ext group.

        Args:
            data: Solution data.

        Returns:
            The computed Ext^1 group.
        """
        return f"Ext^1(Z/{data['n']}Z, Z) = {data['result']}"


# ═══════════════════════════════════════════════════════════════════
# 6. TOR FUNCTOR (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class TorFunctorGenerator(StepGenerator):
    """Compute Tor_1(Z/mZ, Z/nZ) = Z/gcd(m,n)Z.

    Uses the resolution 0 -> Z --*m--> Z -> Z/mZ -> 0 and tensors
    with Z/nZ. Template-based with varying m, n.

    Difficulty scaling:
        Difficulty 1-3: m, n in [2, 4].
        Difficulty 4-6: m, n in [3, 8].
        Difficulty 7-8: m, n in [4, 12].

    Prerequisites:
        exact_sequence (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tor_functor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exact_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls m, n.

        Returns:
            Task description string.
        """
        return "compute Tor_1(Z/mZ, Z/nZ) via tensor product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Tor functor problem.

        Args:
            difficulty: Controls m, n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m = self._rng.randint(2, 4)
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            m = self._rng.randint(3, 8)
            n = self._rng.randint(3, 8)
        else:
            m = self._rng.randint(4, 12)
            n = self._rng.randint(4, 12)

        g = _gcd(m, n)
        problem = (
            f"Compute Tor_1(Z/{m}Z, Z/{n}Z). "
            f"Resolution: 0 -> Z --*{m}--> Z -> Z/{m}Z -> 0."
        )
        return problem, {
            "m": m, "n": n, "g": g,
            "result": f"Z/{g}Z" if g > 1 else "0",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Tor computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing tensor product and kernel.
        """
        m, n, g = data["m"], data["n"], data["g"]
        return [
            f"resolution: 0 -> Z --*{m}--> Z -> Z/{m}Z -> 0",
            f"tensor with Z/{n}Z: 0 -> Z/{n}Z --*{m}--> Z/{n}Z -> 0",
            f"*{m} on Z/{n}Z: ker = elements x where {m}x = 0 mod {n}",
            f"gcd({m}, {n}) = {g}",
            f"Tor_1(Z/{m}Z, Z/{n}Z) = {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Tor group.

        Args:
            data: Solution data.

        Returns:
            The computed Tor_1 group.
        """
        return f"Tor_1(Z/{data['m']}Z, Z/{data['n']}Z) = {data['result']}"


# ═══════════════════════════════════════════════════════════════════
# 7. FREE RESOLUTION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class FreeResolutionGenerator(StepGenerator):
    """Write a free resolution of Z/nZ.

    Constructs the standard free resolution:
    ... -> Z --*n--> Z --*n--> Z -> Z/nZ -> 0. Verifies that each
    composition is zero and that exactness holds.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 4], length 2.
        Difficulty 4-6: n in [3, 6], length 3.
        Difficulty 7-8: n in [4, 8], length 4.

    Prerequisites:
        group_homomorphism (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "free_resolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_homomorphism"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls n and resolution length.

        Returns:
            Task description string.
        """
        return "write free resolution of Z/nZ"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a free resolution problem.

        Args:
            difficulty: Controls n and length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 4)
            length = 2
        elif difficulty <= 6:
            n = self._rng.randint(3, 6)
            length = 3
        else:
            n = self._rng.randint(4, 8)
            length = 4

        maps = []
        for i in range(length):
            if i % 2 == 0:
                maps.append(f"*{n}")
            else:
                maps.append("*1 (projection)")

        problem = f"Write free resolution of Z/{n}Z of length {length}."
        return problem, {
            "n": n, "length": length, "maps": maps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate resolution construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the resolution.
        """
        n = data["n"]
        length = data["length"]
        steps = [f"target module: Z/{n}Z"]
        chain_parts = []
        for i in range(length):
            chain_parts.append(f"Z --*{n if i % 2 == 0 else 1}-->")
        chain = " ".join(chain_parts) + f" Z/{n}Z -> 0"
        steps.append(f"resolution: ... -> {chain}")
        steps.append(f"each *{n} followed by projection: composition = 0")
        steps.append(f"exactness: ker(*{n}) = {n}Z = im(projection)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the resolution.

        Args:
            data: Solution data.

        Returns:
            The free resolution string.
        """
        n = data["n"]
        return f"... -> Z --*{n}--> Z --*{n}--> Z -> Z/{n}Z -> 0"


# ═══════════════════════════════════════════════════════════════════
# 8. EULER CHARACTERISTIC (CHAIN) (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class EulerCharacteristicChainGenerator(StepGenerator):
    """Compute Euler characteristic from chain complex ranks.

    Verifies chi = sum(-1)^n * rank(C_n) = sum(-1)^n * rank(H_n)
    for a simple chain complex.

    Difficulty scaling:
        Difficulty 1-3: 2-term complex (C_0, C_1).
        Difficulty 4-6: 3-term complex (C_0, C_1, C_2).
        Difficulty 7-8: 4-term complex.

    Prerequisites:
        chain_complex (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "euler_characteristic_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["chain_complex"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls complex length.

        Returns:
            Task description string.
        """
        return "compute Euler characteristic of chain complex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler characteristic problem.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            ranks = [self._rng.randint(1, 3) for _ in range(2)]
        elif difficulty <= 6:
            ranks = [self._rng.randint(1, 4) for _ in range(3)]
        else:
            ranks = [self._rng.randint(1, 5) for _ in range(4)]

        chi = sum((-1) ** i * r for i, r in enumerate(ranks))

        rank_str = ", ".join(f"rank(C_{i})={r}" for i, r in enumerate(ranks))
        problem = f"Chain complex with {rank_str}. Compute chi."
        return problem, {
            "ranks": ranks, "chi": chi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler characteristic steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing alternating sum.
        """
        ranks = data["ranks"]
        steps = []
        terms = []
        for i, r in enumerate(ranks):
            sign = "+" if (-1) ** i > 0 else "-"
            terms.append(f"({sign}{r})")
            steps.append(f"(-1)^{i} * rank(C_{i}) = {(-1)**i * r}")
        steps.append(f"chi = {' + '.join(str((-1)**i * r) for i, r in enumerate(ranks))} = {data['chi']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Euler characteristic.

        Args:
            data: Solution data.

        Returns:
            The computed Euler characteristic.
        """
        return f"chi = {data['chi']}"


# ═══════════════════════════════════════════════════════════════════
# 9. BETTI NUMBER (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class BettiNumberGenerator(StepGenerator):
    """Compute Betti numbers for simple topological spaces.

    Template-based: uses known homology groups for circle (S^1),
    sphere (S^2), torus (T^2), Klein bottle, and point. Reports
    b_n = rank(H_n).

    Difficulty scaling:
        Difficulty 1-3: point or circle.
        Difficulty 4-6: sphere or torus.
        Difficulty 7-8: Klein bottle or RP^2.

    Prerequisites:
        homology_compute (tier 7).
    """

    SPACES: list[dict] = [
        {"name": "point", "betti": [1], "desc": "single point"},
        {"name": "S^1", "betti": [1, 1], "desc": "circle"},
        {"name": "S^2", "betti": [1, 0, 1], "desc": "2-sphere"},
        {"name": "T^2", "betti": [1, 2, 1], "desc": "torus"},
        {"name": "Klein bottle", "betti": [1, 1, 0], "desc": "Klein bottle"},
        {"name": "RP^2", "betti": [1, 0, 0], "desc": "real projective plane"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "betti_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["homology_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "compute Betti numbers of topological space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Betti number problem.

        Args:
            difficulty: Controls which space is chosen.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            space = self._rng.choice(self.SPACES[:2])
        elif difficulty <= 6:
            space = self._rng.choice(self.SPACES[2:4])
        else:
            space = self._rng.choice(self.SPACES[4:])

        problem = f"Compute Betti numbers b_n for the {space['desc']} ({space['name']})."
        return problem, {
            "name": space["name"],
            "desc": space["desc"],
            "betti": space["betti"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Betti number steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing each Betti number.
        """
        steps = [f"space: {data['desc']} ({data['name']})"]
        for i, b in enumerate(data["betti"]):
            steps.append(f"b_{i} = rank(H_{i}) = {b}")
        chi = sum((-1) ** i * b for i, b in enumerate(data["betti"]))
        steps.append(f"Euler characteristic = {chi}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Betti numbers.

        Args:
            data: Solution data.

        Returns:
            Comma-separated Betti numbers.
        """
        betti_str = ", ".join(f"b_{i}={b}" for i, b in enumerate(data["betti"]))
        return betti_str


# ═══════════════════════════════════════════════════════════════════
# 10. MAYER-VIETORIS (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class MayerVietorisGenerator(StepGenerator):
    """Apply the Mayer-Vietoris sequence.

    Template-based: decompose a space X = A union B and use the long
    exact sequence to compute H_n(X). Covers circle (two arcs),
    sphere (two hemispheres), and torus.

    Difficulty scaling:
        Difficulty 1-3: circle = two overlapping arcs.
        Difficulty 4-6: sphere = two hemispheres.
        Difficulty 7-8: torus decomposition.

    Prerequisites:
        exact_sequence (tier 7).
    """

    DECOMPOSITIONS: list[dict] = [
        {
            "space": "S^1", "desc": "circle",
            "a": "arc A (contractible)", "b": "arc B (contractible)",
            "a_cap_b": "two points",
            "h_x": {0: 1, 1: 1},
            "explanation": "H_0(A cap B)=Z^2, H_0(A)+H_0(B)=Z^2, connecting map gives H_1(S^1)=Z",
        },
        {
            "space": "S^2", "desc": "2-sphere",
            "a": "upper hemisphere", "b": "lower hemisphere",
            "a_cap_b": "equator (S^1)",
            "h_x": {0: 1, 1: 0, 2: 1},
            "explanation": "H_1(S^1)=Z maps to H_1(A)+H_1(B)=0, so H_2(S^2)=Z",
        },
        {
            "space": "T^2", "desc": "torus",
            "a": "cylinder A", "b": "cylinder B",
            "a_cap_b": "two circles",
            "h_x": {0: 1, 1: 2, 2: 1},
            "explanation": "H_1(A cap B)=Z^2, H_1(A)+H_1(B)=Z^2, get H_1(T^2)=Z^2, H_2(T^2)=Z",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mayer_vietoris"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exact_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls decomposition complexity.

        Returns:
            Task description string.
        """
        return "compute homology via Mayer-Vietoris sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mayer-Vietoris problem.

        Args:
            difficulty: Controls which space is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            decomp = self.DECOMPOSITIONS[0]
        elif difficulty <= 6:
            decomp = self.DECOMPOSITIONS[1]
        else:
            decomp = self.DECOMPOSITIONS[2]

        problem = (
            f"X = {decomp['space']} ({decomp['desc']}). "
            f"A = {decomp['a']}, B = {decomp['b']}, "
            f"A cap B = {decomp['a_cap_b']}. "
            f"Use Mayer-Vietoris to compute H_*(X)."
        )
        return problem, {
            "space": decomp["space"],
            "a": decomp["a"],
            "b": decomp["b"],
            "a_cap_b": decomp["a_cap_b"],
            "h_x": decomp["h_x"],
            "explanation": decomp["explanation"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Mayer-Vietoris steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the long exact sequence application.
        """
        steps = [
            f"decompose {data['space']}: A = {data['a']}, B = {data['b']}",
            f"A cap B = {data['a_cap_b']}",
            "Mayer-Vietoris: ... -> H_n(A cap B) -> H_n(A)+H_n(B) -> H_n(X) -> H_{{n-1}}(A cap B) -> ...",
            data["explanation"],
        ]
        for n, rank in sorted(data["h_x"].items()):
            if rank == 0:
                steps.append(f"H_{n}({data['space']}) = 0")
            elif rank == 1:
                steps.append(f"H_{n}({data['space']}) = Z")
            else:
                steps.append(f"H_{n}({data['space']}) = Z^{rank}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the homology groups.

        Args:
            data: Solution data.

        Returns:
            Homology groups of the space.
        """
        parts = []
        for n, rank in sorted(data["h_x"].items()):
            if rank == 0:
                parts.append(f"H_{n}=0")
            elif rank == 1:
                parts.append(f"H_{n}=Z")
            else:
                parts.append(f"H_{n}=Z^{rank}")
        return ", ".join(parts)
