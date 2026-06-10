"""Algebraic topology generators.

6 generators at tier 7 covering long exact sequences in homology,
cup products, Lefschetz numbers, cellular homology, excision, and
the universal coefficient theorem.
"""
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


def _group_str(rank: int, torsion: list[int] | None = None) -> str:
    """Format an abelian group as a string.

    Args:
        rank: Free rank (number of Z summands).
        torsion: List of torsion orders (e.g. [2, 3] for Z/2 + Z/3).

    Returns:
        String representation like 'Z^2 + Z/3Z' or '0'.
    """
    parts: list[str] = []
    if rank > 1:
        parts.append(f"Z^{rank}")
    elif rank == 1:
        parts.append("Z")
    if torsion:
        for t in torsion:
            parts.append(f"Z/{t}Z")
    if not parts:
        return "0"
    return " + ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 1. LONG EXACT SEQUENCE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class LongExactSequenceGenerator(StepGenerator):
    """Write the long exact sequence in homology from a short exact sequence.

    Given 0 -> A -> B -> C -> 0 of chain complexes (template:
    0 -> Z -> Z -> Z/nZ -> 0), produce the long exact sequence of
    homology groups and identify the connecting homomorphism.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 4], list H_0 and H_1 terms.
        Difficulty 4-6: n in [3, 7], include H_2 term.
        Difficulty 7-8: n in [4, 10], full three-level sequence.

    Prerequisites:
        group_homomorphism (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "long_exact_sequence"

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
            difficulty: Controls sequence length and n.

        Returns:
            Task description string.
        """
        return "write long exact sequence in homology from short exact sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a long exact sequence problem.

        Uses the standard SES 0 -> Z --*n--> Z --> Z/nZ -> 0 viewed
        as chain complexes concentrated in degree 0.

        Args:
            difficulty: Controls n and number of displayed levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 4)
            levels = 2
        elif difficulty <= 6:
            n = self._rng.randint(3, 7)
            levels = 3
        else:
            n = self._rng.randint(4, 10)
            levels = 3

        # For complexes concentrated in degree 0:
        # H_0(A) = Z, H_0(B) = Z, H_0(C) = Z/nZ, higher H_k = 0
        # Long exact: ... -> H_1(C) --delta--> H_0(A) -> H_0(B) -> H_0(C) -> 0
        # delta: H_1(C) -> H_0(A) is the connecting map
        # Since H_k = 0 for k >= 1 (concentrated in deg 0), sequence collapses

        problem = (
            f"SES: 0 -> Z --*{n}--> Z --mod {n}--> Z/{n}Z -> 0. "
            f"Write the long exact sequence in homology (first {levels} levels)."
        )
        return problem, {
            "n": n,
            "levels": levels,
            "delta_desc": f"delta: H_1(Z/{n}Z) -> H_0(Z)",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate long exact sequence construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps building the LES from the SES.
        """
        n = data["n"]
        steps = [
            f"SES: 0 -> Z --*{n}--> Z --mod {n}--> Z/{n}Z -> 0",
            f"H_0: ... -> H_0(Z) --*{n}--> H_0(Z) --pi--> H_0(Z/{n}Z) -> 0",
            f"H_0(Z) = Z, so: ... -> Z --*{n}--> Z --pi--> Z/{n}Z -> 0",
            f"connecting map delta: H_1(Z/{n}Z) -> H_0(Z) is zero (H_1 = 0)",
        ]
        if data["levels"] >= 3:
            steps.append("H_k = 0 for k >= 1 (complexes in degree 0)")
            steps.append("LES collapses to 0 -> Z --*n--> Z -> Z/nZ -> 0")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the long exact sequence.

        Args:
            data: Solution data.

        Returns:
            The LES as a string.
        """
        n = data["n"]
        return f"... -> 0 --delta--> Z --*{n}--> Z --pi--> Z/{n}Z -> 0"


# ═══════════════════════════════════════════════════════════════════
# 2. CUP PRODUCT (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class CupProductGenerator(StepGenerator):
    """Compute cup product of cohomology classes on standard spaces.

    Template-based computation for torus T^2 and real projective
    plane RP^2. On T^2: H^1 x H^1 -> H^2 is the wedge product
    of the two generators. On RP^2: a^2 = 0 in H^2(RP^2; Z).

    Difficulty scaling:
        Difficulty 1-3: T^2, alpha cup alpha = 0.
        Difficulty 4-6: T^2, alpha cup beta = generator of H^2.
        Difficulty 7-8: RP^2, a cup a with Z/2Z coefficients.

    Prerequisites:
        fundamental_group (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cup_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fundamental_group"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space and class choice.

        Returns:
            Task description string.
        """
        return "compute cup product of cohomology classes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cup product computation problem.

        Args:
            difficulty: Controls the space and cohomology classes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # T^2, alpha cup alpha
            space = "T^2"
            cls_a = "alpha"
            cls_b = "alpha"
            deg_a = 1
            deg_b = 1
            result = "0"
            reason = "alpha cup alpha = 0 (graded commutativity)"
        elif difficulty <= 6:
            # T^2, alpha cup beta
            space = "T^2"
            cls_a = "alpha"
            cls_b = "beta"
            deg_a = 1
            deg_b = 1
            result = "gamma (generator of H^2(T^2))"
            reason = "alpha, beta generate H^1(T^2); alpha cup beta = generator of H^2 = Z"
        else:
            # RP^2 with Z/2Z coefficients
            coeff = self._rng.choice(["Z", "Z/2Z"])
            space = "RP^2"
            cls_a = "a"
            cls_b = "a"
            deg_a = 1
            deg_b = 1
            if coeff == "Z/2Z":
                result = "generator of H^2(RP^2; Z/2Z)"
                reason = "H^*(RP^2; Z/2) = Z/2[a]/(a^3), so a^2 != 0"
            else:
                result = "0"
                reason = "H^1(RP^2; Z) = 0, so cup product is trivially 0"

        problem = (
            f"Space: {space}. Compute {cls_a} cup {cls_b} "
            f"where {cls_a} in H^{deg_a}, {cls_b} in H^{deg_b}."
        )
        return problem, {
            "space": space, "cls_a": cls_a, "cls_b": cls_b,
            "deg_a": deg_a, "deg_b": deg_b,
            "result_deg": deg_a + deg_b,
            "result": result, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cup product computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the cup product computation.
        """
        return [
            f"space: {data['space']}",
            f"{data['cls_a']} in H^{data['deg_a']}, {data['cls_b']} in H^{data['deg_b']}",
            f"cup product lands in H^{data['result_deg']}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the cup product result.

        Args:
            data: Solution data.

        Returns:
            The cup product value.
        """
        return f"{data['cls_a']} cup {data['cls_b']} = {data['result']}"


# ═══════════════════════════════════════════════════════════════════
# 3. LEFSCHETZ NUMBER (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class LefschetzNumberGenerator(StepGenerator):
    """Compute the Lefschetz number L(f) = sum (-1)^n tr(f_*: H_n -> H_n).

    Uses template spaces (S^1, S^2, T^2) with standard maps (degree-d
    maps, identity, antipodal). L(f) != 0 implies f has a fixed point.

    Difficulty scaling:
        Difficulty 1-3: S^1 with degree-d map, d in [-2, 3].
        Difficulty 4-6: S^2 with degree-d map.
        Difficulty 7-8: T^2 with linear map on H_1.

    Prerequisites:
        matrix_multiply (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lefschetz_number"

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
            difficulty: Controls the space and map.

        Returns:
            Task description string.
        """
        return "compute Lefschetz number and determine fixed point existence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lefschetz number problem.

        Args:
            difficulty: Controls space and map complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # S^1: H_0 = Z, H_1 = Z. Degree d map: f_* on H_0 is id, on H_1 is *d
            d = self._rng.randint(-2, 3)
            tr_0 = 1
            tr_1 = d
            lef = tr_0 - tr_1
            space = "S^1"
            map_desc = f"degree {d} map"
            traces = {0: tr_0, 1: tr_1}
        elif difficulty <= 6:
            # S^2: H_0 = Z, H_1 = 0, H_2 = Z. Degree d map
            d = self._rng.randint(-2, 3)
            tr_0 = 1
            tr_2 = d
            lef = tr_0 + tr_2  # (-1)^0 * 1 + (-1)^2 * d = 1 + d
            space = "S^2"
            map_desc = f"degree {d} map"
            traces = {0: tr_0, 2: tr_2}
        else:
            # T^2: H_0 = Z, H_1 = Z^2, H_2 = Z
            # Linear map A on H_1 (2x2 integer matrix)
            a = self._rng.randint(-2, 2)
            b = self._rng.randint(-2, 2)
            c = self._rng.randint(-2, 2)
            d_val = self._rng.randint(-2, 2)
            tr_0 = 1
            tr_1 = a + d_val  # trace of [[a,b],[c,d]]
            det_a = a * d_val - b * c
            tr_2 = det_a  # induced map on H_2 is det(A)
            lef = tr_0 - tr_1 + tr_2
            space = "T^2"
            map_desc = f"induced by [[{a},{b}],[{c},{d_val}]] on H_1"
            traces = {0: tr_0, 1: tr_1, 2: tr_2}

        has_fp = (lef != 0)
        problem = (
            f"f: {space} -> {space}, {map_desc}. "
            f"Compute L(f) = sum(-1)^n tr(f_* on H_n)."
        )
        return problem, {
            "space": space, "map_desc": map_desc,
            "traces": traces, "lef": lef, "has_fp": has_fp,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lefschetz number computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps computing traces and alternating sum.
        """
        steps = [f"space: {data['space']}, map: {data['map_desc']}"]
        terms = []
        for n, tr in sorted(data["traces"].items()):
            sign = "+" if (-1) ** n > 0 else "-"
            steps.append(f"(-1)^{n} * tr(f_* on H_{n}) = {(-1)**n * tr}")
            terms.append((-1) ** n * tr)
        steps.append(f"L(f) = {' + '.join(str(t) for t in terms)} = {data['lef']}")
        if data["has_fp"]:
            steps.append("L(f) != 0 => f has a fixed point")
        else:
            steps.append("L(f) = 0 => theorem inconclusive")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Lefschetz number and fixed point conclusion.

        Args:
            data: Solution data.

        Returns:
            Lefschetz number and whether a fixed point is guaranteed.
        """
        fp = "fixed point exists" if data["has_fp"] else "inconclusive"
        return f"L(f) = {data['lef']}, {fp}"


# ═══════════════════════════════════════════════════════════════════
# 4. CELLULAR HOMOLOGY (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class CellularHomologyGenerator(StepGenerator):
    """Compute cellular homology from CW complex structure.

    Template-based for standard spaces: S^n (two cells), T^2
    (one 0-cell, two 1-cells, one 2-cell), RP^2 (one cell in each
    dimension with degree-2 attaching map).

    Difficulty scaling:
        Difficulty 1-3: S^1 or S^2.
        Difficulty 4-6: T^2.
        Difficulty 7-8: RP^2 or Klein bottle.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _SPACES = [
        {
            "name": "S^1", "desc": "circle",
            "cells": {0: 1, 1: 1},
            "attaching": "1-cell attached at both ends to the 0-cell",
            "homology": {0: (1, []), 1: (1, [])},
        },
        {
            "name": "S^2", "desc": "2-sphere",
            "cells": {0: 1, 2: 1},
            "attaching": "2-cell attached to 0-cell via constant map",
            "homology": {0: (1, []), 1: (0, []), 2: (1, [])},
        },
        {
            "name": "T^2", "desc": "torus",
            "cells": {0: 1, 1: 2, 2: 1},
            "attaching": "2-cell attached via aba^{-1}b^{-1}",
            "homology": {0: (1, []), 1: (2, []), 2: (1, [])},
        },
        {
            "name": "RP^2", "desc": "real projective plane",
            "cells": {0: 1, 1: 1, 2: 1},
            "attaching": "2-cell attached via degree-2 map to 1-cell",
            "homology": {0: (1, []), 1: (0, [2]), 2: (0, [])},
        },
        {
            "name": "Klein bottle", "desc": "Klein bottle",
            "cells": {0: 1, 1: 2, 2: 1},
            "attaching": "2-cell attached via aba^{-1}b",
            "homology": {0: (1, []), 1: (1, [2]), 2: (0, [])},
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cellular_homology"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "compute cellular homology from CW complex structure"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cellular homology problem.

        Args:
            difficulty: Controls which space is chosen.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            space = self._rng.choice(self._SPACES[:2])
        elif difficulty <= 6:
            space = self._SPACES[2]  # torus
        else:
            space = self._rng.choice(self._SPACES[3:])

        cells_str = ", ".join(
            f"{count} {dim}-cell{'s' if count > 1 else ''}"
            for dim, count in sorted(space["cells"].items())
        )
        problem = (
            f"CW complex for {space['name']} ({space['desc']}): {cells_str}. "
            f"Attaching: {space['attaching']}. Compute H_n."
        )
        return problem, {
            "name": space["name"], "desc": space["desc"],
            "cells": space["cells"],
            "attaching": space["attaching"],
            "homology": space["homology"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cellular homology computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing cell structure and boundary maps.
        """
        steps = [f"CW structure of {data['name']}:"]
        for dim, count in sorted(data["cells"].items()):
            steps.append(f"  {count} cell(s) in dimension {dim}")
        steps.append(f"attaching map: {data['attaching']}")

        for n, (rank, torsion) in sorted(data["homology"].items()):
            h_str = _group_str(rank, torsion)
            steps.append(f"H_{n}({data['name']}) = {h_str}")

        chi = sum(
            (-1) ** n * (r + len(t))
            for n, (r, t) in data["homology"].items()
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the homology groups.

        Args:
            data: Solution data.

        Returns:
            All homology groups as a string.
        """
        parts = []
        for n, (rank, torsion) in sorted(data["homology"].items()):
            h_str = _group_str(rank, torsion)
            parts.append(f"H_{n}={h_str}")
        return ", ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 5. EXCISION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class ExcisionGenerator(StepGenerator):
    """Apply the excision theorem to compute relative homology.

    Excision: if U is open in A and cl(U) is contained in int(A),
    then H_n(X, A) = H_n(X \\ U, A \\ U). Template-based for
    standard pairs (disk/boundary, sphere/hemisphere).

    Difficulty scaling:
        Difficulty 1-3: (D^2, S^1) -> excise interior point.
        Difficulty 4-6: (S^2, D^2_+) -> excise open cap.
        Difficulty 7-8: (D^n, S^{n-1}) for n in [2, 4].

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _PAIRS = [
        {
            "x": "D^2", "a": "S^1", "u": "interior point of D^2",
            "x_minus_u": "D^2 \\ {pt}", "a_minus_u": "S^1",
            "h_rel": {0: "0", 1: "0", 2: "Z"},
            "reason": "H_n(D^2, S^1) = H_n(S^2) by collapsing A",
        },
        {
            "x": "S^2", "a": "D^2_+ (upper hemisphere)",
            "u": "open northern cap",
            "x_minus_u": "D^2_- (closed lower)", "a_minus_u": "equator S^1",
            "h_rel": {0: "0", 1: "0", 2: "Z"},
            "reason": "excision reduces to H_n(D^2, S^1) = H_n(S^2) relative",
        },
        {
            "x": "D^3", "a": "S^2", "u": "interior point of D^3",
            "x_minus_u": "D^3 \\ {pt}", "a_minus_u": "S^2",
            "h_rel": {0: "0", 1: "0", 2: "0", 3: "Z"},
            "reason": "H_n(D^3, S^2) = H_n(S^3)",
        },
        {
            "x": "D^4", "a": "S^3", "u": "interior point of D^4",
            "x_minus_u": "D^4 \\ {pt}", "a_minus_u": "S^3",
            "h_rel": {0: "0", 1: "0", 2: "0", 3: "0", 4: "Z"},
            "reason": "H_n(D^4, S^3) = H_n(S^4)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "excision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls pair complexity.

        Returns:
            Task description string.
        """
        return "apply excision theorem to compute relative homology"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an excision problem.

        Args:
            difficulty: Controls which pair (X, A) is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pair = self._PAIRS[0]
        elif difficulty <= 6:
            pair = self._PAIRS[1]
        else:
            pair = self._rng.choice(self._PAIRS[2:])

        problem = (
            f"X = {pair['x']}, A = {pair['a']}. "
            f"Excise U = {pair['u']}. "
            f"Compute H_n(X, A) using excision."
        )
        return problem, {
            "x": pair["x"], "a": pair["a"], "u": pair["u"],
            "x_minus_u": pair["x_minus_u"],
            "a_minus_u": pair["a_minus_u"],
            "h_rel": pair["h_rel"],
            "reason": pair["reason"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate excision steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying excision and computing relative homology.
        """
        steps = [
            f"pair: (X, A) = ({data['x']}, {data['a']})",
            f"excise U = {data['u']} (cl(U) in int(A))",
            f"H_n(X, A) = H_n(X\\U, A\\U) = H_n({data['x_minus_u']}, {data['a_minus_u']})",
            data["reason"],
        ]
        for n, h in sorted(data["h_rel"].items()):
            steps.append(f"H_{n}({data['x']}, {data['a']}) = {h}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the relative homology groups.

        Args:
            data: Solution data.

        Returns:
            Relative homology groups as a string.
        """
        parts = []
        for n, h in sorted(data["h_rel"].items()):
            parts.append(f"H_{n}={h}")
        return ", ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 6. UNIVERSAL COEFFICIENT THEOREM (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class UniversalCoefficientGenerator(StepGenerator):
    """Apply the universal coefficient theorem for cohomology.

    UCT: H^n(X; G) = Hom(H_n(X), G) + Ext^1(H_{n-1}(X), G).
    Compute for spaces with known homology (S^1, S^2, T^2, RP^2)
    and coefficient groups G = Z or Z/pZ.

    Difficulty scaling:
        Difficulty 1-3: S^1 or S^2 with G = Z.
        Difficulty 4-6: T^2 with G = Z or Z/pZ.
        Difficulty 7-8: RP^2 with G = Z/pZ (non-trivial Ext).

    Prerequisites:
        group_homomorphism (tier 6).
    """

    _SPACES = {
        "S^1": {0: (1, []), 1: (1, [])},
        "S^2": {0: (1, []), 1: (0, []), 2: (1, [])},
        "T^2": {0: (1, []), 1: (2, []), 2: (1, [])},
        "RP^2": {0: (1, []), 1: (0, [2]), 2: (0, [])},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "universal_coefficient"

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
            difficulty: Controls space and coefficient group.

        Returns:
            Task description string.
        """
        return "compute cohomology via universal coefficient theorem"

    def _hom_group(self, rank: int, torsion: list[int], g_type: str,
                   g_val: int) -> str:
        """Compute Hom(H, G) for abelian H and G.

        Args:
            rank: Free rank of H.
            torsion: Torsion orders of H.
            g_type: 'Z' or 'Z/pZ'.
            g_val: p for Z/pZ, 0 for Z.

        Returns:
            String describing the Hom group.
        """
        parts: list[str] = []
        if g_type == "Z":
            # Hom(Z, Z) = Z, Hom(Z/nZ, Z) = 0
            if rank > 1:
                parts.append(f"Z^{rank}")
            elif rank == 1:
                parts.append("Z")
        else:
            # Hom(Z, Z/pZ) = Z/pZ, Hom(Z/nZ, Z/pZ) = Z/gcd(n,p)Z
            for _ in range(rank):
                parts.append(f"Z/{g_val}Z")
            for t in torsion:
                g = _gcd(t, g_val)
                if g > 1:
                    parts.append(f"Z/{g}Z")
        if not parts:
            return "0"
        return " + ".join(parts)

    def _ext_group(self, rank: int, torsion: list[int], g_type: str,
                   g_val: int) -> str:
        """Compute Ext^1(H, G) for abelian H and G.

        Args:
            rank: Free rank of H.
            torsion: Torsion orders of H.
            g_type: 'Z' or 'Z/pZ'.
            g_val: p for Z/pZ, 0 for Z.

        Returns:
            String describing the Ext group.
        """
        # Ext^1(Z, G) = 0, Ext^1(Z/nZ, Z) = Z/nZ, Ext^1(Z/nZ, Z/pZ) = Z/gcd(n,p)Z
        parts: list[str] = []
        for t in torsion:
            if g_type == "Z":
                parts.append(f"Z/{t}Z")
            else:
                g = _gcd(t, g_val)
                if g > 1:
                    parts.append(f"Z/{g}Z")
        if not parts:
            return "0"
        return " + ".join(parts)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a UCT problem.

        Args:
            difficulty: Controls space and coefficient group.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            space_name = self._rng.choice(["S^1", "S^2"])
            g_type = "Z"
            g_val = 0
        elif difficulty <= 6:
            space_name = "T^2"
            if self._rng.random() < 0.5:
                g_type = "Z"
                g_val = 0
            else:
                g_val = self._rng.choice([2, 3, 5])
                g_type = "Z/pZ"
        else:
            space_name = "RP^2"
            g_val = self._rng.choice([2, 3, 5, 7])
            g_type = "Z/pZ"

        g_str = "Z" if g_type == "Z" else f"Z/{g_val}Z"
        homology = self._SPACES[space_name]

        # Compute H^n for each n
        max_n = max(homology.keys())
        cohomology: dict[int, str] = {}
        for n in range(max_n + 1):
            h_n_rank, h_n_torsion = homology.get(n, (0, []))
            hom_part = self._hom_group(h_n_rank, h_n_torsion, g_type, g_val)

            if n > 0:
                h_nm1_rank, h_nm1_torsion = homology.get(n - 1, (0, []))
                ext_part = self._ext_group(h_nm1_rank, h_nm1_torsion, g_type, g_val)
            else:
                ext_part = "0"

            if hom_part == "0" and ext_part == "0":
                cohomology[n] = "0"
            elif hom_part == "0":
                cohomology[n] = ext_part
            elif ext_part == "0":
                cohomology[n] = hom_part
            else:
                cohomology[n] = f"{hom_part} + {ext_part}"

        # Pick a specific n to ask about
        ask_n = self._rng.randint(0, max_n)

        problem = (
            f"X = {space_name}, G = {g_str}. "
            f"Compute H^{ask_n}(X; G) via UCT."
        )
        return problem, {
            "space": space_name, "g_str": g_str, "g_type": g_type,
            "g_val": g_val, "ask_n": ask_n,
            "cohomology": cohomology, "homology": homology,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate UCT computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying the UCT formula.
        """
        n = data["ask_n"]
        g_str = data["g_str"]
        space = data["space"]
        homology = data["homology"]

        h_n_rank, h_n_torsion = homology.get(n, (0, []))
        h_n_str = _group_str(h_n_rank, h_n_torsion)

        steps = [
            f"UCT: H^{n}(X; G) = Hom(H_{n}(X), G) + Ext^1(H_{{{n}-1}}(X), G)",
            f"H_{n}({space}) = {h_n_str}",
        ]

        hom_val = self._hom_group(h_n_rank, h_n_torsion, data["g_type"], data["g_val"])
        steps.append(f"Hom({h_n_str}, {g_str}) = {hom_val}")

        if n > 0:
            h_nm1_rank, h_nm1_torsion = homology.get(n - 1, (0, []))
            h_nm1_str = _group_str(h_nm1_rank, h_nm1_torsion)
            ext_val = self._ext_group(h_nm1_rank, h_nm1_torsion, data["g_type"], data["g_val"])
            steps.append(f"H_{{{n}-1}}({space}) = {h_nm1_str}")
            steps.append(f"Ext^1({h_nm1_str}, {g_str}) = {ext_val}")
        else:
            steps.append("n=0: Ext^1 term is 0")

        steps.append(f"H^{n}({space}; {g_str}) = {data['cohomology'][n]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cohomology group.

        Args:
            data: Solution data.

        Returns:
            The computed cohomology group.
        """
        n = data["ask_n"]
        return f"H^{n}({data['space']}; {data['g_str']}) = {data['cohomology'][n]}"
