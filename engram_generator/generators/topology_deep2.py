"""Deep algebraic topology generators (second set).

8 generators covering CW complex Euler characteristic, van Kampen
theorem, homology of spheres, suspension, mapping cone, Borsuk-Ulam
theorem, Lefschetz fixed point theorem, and covering degree across
tiers 6-7.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. CW COMPLEX EULER (tier 6)
# ===================================================================

@register
class CWComplexEulerGenerator(StepGenerator):
    """Compute the Euler characteristic of a CW complex from cell counts.

    Given cell counts c_0 (vertices), c_1 (edges), c_2 (faces), c_3
    (3-cells), computes chi = sum (-1)^n * c_n. Includes standard
    surfaces: torus, Klein bottle, RP^2.

    Difficulty scaling:
        Difficulty 1-3: 2D complexes (vertices, edges, faces).
        Difficulty 4-6: standard surfaces with known CW structures.
        Difficulty 7-8: 3D complexes with 3-cells.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _COMPLEXES_EASY = [
        ("triangle boundary", [3, 3, 0, 0], 0,
         "3 vertices - 3 edges = 0 (circle)"),
        ("filled triangle", [3, 3, 1, 0], 1,
         "3 - 3 + 1 = 1 (disk)"),
        ("tetrahedron surface", [4, 6, 4, 0], 2,
         "4 - 6 + 4 = 2 (sphere S^2)"),
    ]

    _COMPLEXES_MED = [
        ("torus", [1, 2, 1, 0], 0,
         "1 - 2 + 1 = 0 (genus 1 orientable)"),
        ("Klein bottle", [1, 2, 1, 0], 0,
         "1 - 2 + 1 = 0 (non-orientable genus 2)"),
        ("RP^2", [1, 1, 1, 0], 1,
         "1 - 1 + 1 = 1 (non-orientable)"),
        ("genus-2 surface", [1, 4, 1, 0], -2,
         "1 - 4 + 1 = -2 (genus 2 orientable)"),
    ]

    _COMPLEXES_HARD = [
        ("3-ball D^3", [1, 0, 0, 1], 0,
         "1 - 0 + 0 - 1 = 0 (contractible)"),
        ("S^3 (suspension of S^2)", [2, 0, 0, 2], 0,
         "2 - 0 + 0 - 2 = 0 (3-sphere)"),
        ("torus x [0,1]", [2, 6, 5, 1], 0,
         "2 - 6 + 5 - 1 = 0"),
        ("wedge of two tori", [1, 4, 2, 0], -1,
         "1 - 4 + 2 = -1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cw_complex_euler"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls complex type.

        Returns:
            Task description string.
        """
        return "compute Euler characteristic of CW complex from cell counts"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CW complex Euler characteristic problem.

        Args:
            difficulty: Controls complex type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._COMPLEXES_EASY
        elif difficulty <= 6:
            pool = self._COMPLEXES_EASY + self._COMPLEXES_MED
        else:
            pool = self._COMPLEXES_EASY + self._COMPLEXES_MED + self._COMPLEXES_HARD

        name, cells, chi, reason = self._rng.choice(pool)
        cells_str = ", ".join(
            f"c_{i}={cells[i]}" for i in range(len(cells)) if cells[i] > 0
        )
        problem = f"CW complex ({name}): {cells_str}. Compute chi."
        return problem, {
            "name": name, "cells": cells, "chi": chi, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler characteristic computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        cells = data["cells"]
        terms = [f"({'-' if i % 2 else '+'}){cells[i]}" for i in range(len(cells))
                 if cells[i] > 0]
        return [
            f"CW complex: {data['name']}",
            f"chi = sum (-1)^n * c_n = {' '.join(terms)}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Euler characteristic value.
        """
        return f"chi = {data['chi']}"


# ===================================================================
# 2. VAN KAMPEN (tier 7)
# ===================================================================

@register
class VanKampenGenerator(StepGenerator):
    """Compute fundamental group using the van Kampen theorem.

    For X = U union V with U, V, U cap V path-connected, computes
    pi_1(X) from pi_1(U), pi_1(V), and pi_1(U cap V). Template-based
    for standard spaces.

    Difficulty scaling:
        Difficulty 1-3: wedge of two circles.
        Difficulty 4-6: torus, Klein bottle.
        Difficulty 7-8: connected sums, more complex identifications.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _SPACES_EASY = [
        ("S^1 v S^1 (wedge of 2 circles)",
         "Z", "Z", "0",
         "Z * Z (free group on 2 generators)",
         "free product, trivial amalgamation"),
        ("S^1 v S^1 v S^1 (wedge of 3 circles)",
         "Z * Z", "Z", "0",
         "Z * Z * Z (free group on 3 generators)",
         "free product of free groups"),
    ]

    _SPACES_MED = [
        ("torus T^2",
         "Z", "Z", "Z",
         "Z x Z (abelian, two commuting generators)",
         "aba^{-1}b^{-1} = 1 from overlap"),
        ("Klein bottle K",
         "Z", "Z", "Z",
         "<a,b | abab^{-1} = 1>",
         "non-abelian identification in overlap"),
        ("RP^2",
         "Z", "0", "Z",
         "Z/2Z",
         "inclusion doubles generator, so 2a = 0"),
    ]

    _SPACES_HARD = [
        ("genus-2 surface",
         "Z * Z", "Z * Z", "Z",
         "<a,b,c,d | [a,b][c,d]=1>",
         "surface group of genus 2"),
        ("S^2 (cover by hemispheres)",
         "0", "0", "Z",
         "0 (trivial)",
         "both U, V contractible, S^1 overlap killed"),
        ("S^1 x S^1 v S^1",
         "Z x Z", "Z", "0",
         "(Z x Z) * Z",
         "free product, wedge point overlap is trivial"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "van_kampen"

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
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "compute fundamental group via van Kampen theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a van Kampen theorem problem.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._SPACES_EASY
        elif difficulty <= 6:
            pool = self._SPACES_EASY + self._SPACES_MED
        else:
            pool = self._SPACES_EASY + self._SPACES_MED + self._SPACES_HARD

        space, pi_u, pi_v, pi_uv, result, reason = self._rng.choice(pool)
        problem = (
            f"X = {space}. pi_1(U) = {pi_u}, pi_1(V) = {pi_v}, "
            f"pi_1(U cap V) = {pi_uv}. Compute pi_1(X)."
        )
        return problem, {
            "space": space, "pi_u": pi_u, "pi_v": pi_v,
            "pi_uv": pi_uv, "result": result, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate van Kampen computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        return [
            f"X = {data['space']}",
            "van Kampen: pi_1(X) = pi_1(U) *_{pi_1(UcapV)} pi_1(V)",
            f"pi_1(U)={data['pi_u']}, pi_1(V)={data['pi_v']}, "
            f"pi_1(UcapV)={data['pi_uv']}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Fundamental group.
        """
        return f"pi_1(X) = {data['result']}"


# ===================================================================
# 3. HOMOLOGY SPHERE (tier 6)
# ===================================================================

@register
class HomologySphereGenerator(StepGenerator):
    """Compute the homology groups of S^n.

    H_0(S^n) = Z, H_n(S^n) = Z, all other H_k(S^n) = 0.
    Verifies via Euler characteristic: chi = 1 + (-1)^n.

    Difficulty scaling:
        Difficulty 1-3: S^1, S^2.
        Difficulty 4-6: S^3, S^4.
        Difficulty 7-8: S^5 through S^8, verify chi.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "homology_sphere"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls n for S^n.

        Returns:
            Task description string.
        """
        return "compute homology groups of S^n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a homology of spheres problem.

        Args:
            difficulty: Controls which sphere.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([1, 2])
        elif difficulty <= 6:
            n = self._rng.choice([2, 3, 4])
        else:
            n = self._rng.randint(3, 8)

        chi = 1 + (-1) ** n
        k = self._rng.randint(0, n + 1)

        if k == 0 or k == n:
            h_k = "Z"
        else:
            h_k = "0"

        problem = f"Compute H_{k}(S^{n}) and verify chi(S^{n})."
        return problem, {
            "n": n, "k": k, "h_k": h_k, "chi": chi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate homology computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        n = data["n"]
        groups = []
        for i in range(n + 1):
            val = "Z" if i == 0 or i == n else "0"
            groups.append(f"H_{i} = {val}")
        return [
            f"S^{n}: H_0 = Z, H_{n} = Z, all others = 0",
            ", ".join(groups),
            f"chi = sum (-1)^k rank(H_k) = 1 + (-1)^{n} = {data['chi']}",
            f"H_{data['k']}(S^{n}) = {data['h_k']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Homology group and Euler characteristic.
        """
        return f"H_{data['k']}(S^{data['n']}) = {data['h_k']}, chi = {data['chi']}"


# ===================================================================
# 4. SUSPENSION (tier 6)
# ===================================================================

@register
class SuspensionGenerator(StepGenerator):
    """Compute homology of the suspension Sigma(X).

    For the suspension: H_n(Sigma X) = H_{n-1}(X) for n >= 1, and
    H_0(Sigma X) = Z. Applies to X = S^k, torus, etc.

    Difficulty scaling:
        Difficulty 1-3: Sigma(S^1), Sigma(S^0).
        Difficulty 4-6: Sigma(S^2), Sigma(S^3).
        Difficulty 7-8: Sigma(T^2), iterated suspensions.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _SPACES_EASY = [
        ("S^0", {0: "Z+Z"},
         {0: "Z", 1: "Z+Z"},
         "Sigma(S^0) = S^1"),
        ("S^1", {0: "Z", 1: "Z"},
         {0: "Z", 1: "Z", 2: "Z"},
         "Sigma(S^1) = S^2"),
    ]

    _SPACES_MED = [
        ("S^2", {0: "Z", 2: "Z"},
         {0: "Z", 1: "0", 2: "0", 3: "Z"},
         "Sigma(S^2) = S^3"),
        ("S^3", {0: "Z", 3: "Z"},
         {0: "Z", 1: "0", 2: "0", 3: "0", 4: "Z"},
         "Sigma(S^3) = S^4"),
    ]

    _SPACES_HARD = [
        ("T^2", {0: "Z", 1: "Z+Z", 2: "Z"},
         {0: "Z", 1: "Z", 2: "Z+Z", 3: "Z"},
         "shifts all homology up by 1"),
        ("S^1 v S^1", {0: "Z", 1: "Z+Z"},
         {0: "Z", 1: "0", 2: "Z+Z"},
         "Sigma shifts rank-1 free group up"),
        ("Sigma(S^1) = S^2", {0: "Z", 2: "Z"},
         {0: "Z", 1: "0", 2: "0", 3: "Z"},
         "Sigma^2(S^1) = S^3"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "suspension"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute homology of suspension Sigma(X)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a suspension homology problem.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._SPACES_EASY
        elif difficulty <= 6:
            pool = self._SPACES_EASY + self._SPACES_MED
        else:
            pool = self._SPACES_EASY + self._SPACES_MED + self._SPACES_HARD

        name, h_x, h_sx, reason = self._rng.choice(pool)
        max_k = max(h_sx.keys())
        query_k = self._rng.randint(0, max_k)
        h_val = h_sx.get(query_k, "0")

        problem = f"X = {name}. Compute H_{query_k}(Sigma X)."
        return problem, {
            "name": name, "h_x": h_x, "h_sx": h_sx,
            "query_k": query_k, "h_val": h_val, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate suspension computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the suspension isomorphism.
        """
        h_x_str = ", ".join(
            f"H_{k}={v}" for k, v in sorted(data["h_x"].items())
        )
        h_sx_str = ", ".join(
            f"H_{k}={v}" for k, v in sorted(data["h_sx"].items())
        )
        return [
            f"X = {data['name']}: {h_x_str}",
            "Sigma: H_n(Sigma X) = H_{n-1}(X) for n >= 1, H_0 = Z",
            f"Sigma X: {h_sx_str}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Homology group of suspension.
        """
        return f"H_{data['query_k']}(Sigma({data['name']})) = {data['h_val']}"


# ===================================================================
# 5. MAPPING CONE (tier 7)
# ===================================================================

@register
class MappingConeGenerator(StepGenerator):
    """Compute homology of the mapping cone of f: X -> Y.

    Uses the long exact sequence of the pair (Cf, Y) to determine
    H_n(Cf). Template-based for standard maps f: S^n -> S^n.

    Difficulty scaling:
        Difficulty 1-3: f: S^1 -> S^1 of degree d.
        Difficulty 4-6: f: S^2 -> S^2 of degree d.
        Difficulty 7-8: f: S^1 -> point (cone = S^2), general degrees.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _MAPS_EASY = [
        ("f: S^1 -> S^1, deg=2", 1, 2,
         {0: "Z", 1: "0", 2: "Z/2Z"},
         "long exact seq gives H_2(Cf) = Z/dZ"),
        ("f: S^1 -> S^1, deg=3", 1, 3,
         {0: "Z", 1: "0", 2: "Z/3Z"},
         "mapping cone of degree-3 map"),
        ("f: S^1 -> S^1, deg=1 (identity)", 1, 1,
         {0: "Z", 1: "0", 2: "0"},
         "cone of identity is contractible rel Y"),
    ]

    _MAPS_MED = [
        ("f: S^2 -> S^2, deg=2", 2, 2,
         {0: "Z", 1: "0", 2: "0", 3: "Z/2Z"},
         "H_3(Cf) = coker(f_*) = Z/2Z"),
        ("f: S^2 -> S^2, deg=0 (constant)", 2, 0,
         {0: "Z", 1: "0", 2: "Z", 3: "Z"},
         "constant map: Cf ~ Y v Sigma X"),
    ]

    _MAPS_HARD = [
        ("f: S^1 -> pt (constant)", 1, 0,
         {0: "Z", 1: "0", 2: "Z"},
         "Cf = Sigma S^1 = S^2 when Y = pt"),
        ("f: S^3 -> S^3, deg=2", 3, 2,
         {0: "Z", 1: "0", 2: "0", 3: "0", 4: "Z/2Z"},
         "H_4(Cf) = Z/2Z from long exact sequence"),
        ("f: S^1 -> S^1, deg=-1", 1, -1,
         {0: "Z", 1: "0", 2: "Z/2Z"},
         "absolute degree gives Z/2Z in top"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mapping_cone"

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
            difficulty: Controls map complexity.

        Returns:
            Task description string.
        """
        return "compute homology of mapping cone"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mapping cone homology problem.

        Args:
            difficulty: Controls map complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._MAPS_EASY
        elif difficulty <= 6:
            pool = self._MAPS_EASY + self._MAPS_MED
        else:
            pool = self._MAPS_EASY + self._MAPS_MED + self._MAPS_HARD

        desc, dim, deg, homology, reason = self._rng.choice(pool)
        max_k = max(homology.keys())
        query_k = self._rng.randint(0, max_k)
        h_val = homology.get(query_k, "0")

        problem = f"{desc}. Compute H_{query_k}(Cf)."
        return problem, {
            "desc": desc, "dim": dim, "deg": deg,
            "homology": homology, "query_k": query_k,
            "h_val": h_val, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mapping cone computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the long exact sequence.
        """
        h_str = ", ".join(
            f"H_{k}={v}" for k, v in sorted(data["homology"].items())
        )
        return [
            f"map: {data['desc']}",
            "long exact seq: ... -> H_n(X) -> H_n(Y) -> H_n(Cf) -> H_{n-1}(X) -> ...",
            f"H_*(Cf): {h_str}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Homology group of mapping cone.
        """
        return f"H_{data['query_k']}(Cf) = {data['h_val']}"


# ===================================================================
# 6. BORSUK-ULAM (tier 6)
# ===================================================================

@register
class BorsukUlamGenerator(StepGenerator):
    """Apply the Borsuk-Ulam theorem and its consequences.

    For f: S^n -> R^n continuous, there exists x with f(x) = f(-x).
    Applications include the ham sandwich theorem in R^2 and temperature
    on the equator. Template-based.

    Difficulty scaling:
        Difficulty 1-3: n=1, antipodal temperature result.
        Difficulty 4-6: n=2, ham sandwich theorem.
        Difficulty 7-8: general n, Lusternik-Schnirelmann.

    Prerequisites:
        comparison (tier 0).
    """

    _APPLICATIONS_EASY = [
        ("f: S^1 -> R continuous", 1,
         "exists antipodal pair with f(x) = f(-x)",
         "two opposite points on equator have same temperature"),
        ("g: S^1 -> R, g(x) = f(x) - f(-x)", 1,
         "g is continuous and g(-x) = -g(x), so g has a zero",
         "intermediate value theorem on odd function"),
    ]

    _APPLICATIONS_MED = [
        ("ham sandwich theorem in R^2", 2,
         "exists line bisecting two bounded measurable sets",
         "Borsuk-Ulam for n=2 gives simultaneous bisection"),
        ("f: S^2 -> R^2 continuous", 2,
         "exists x in S^2 with f(x) = f(-x)",
         "two antipodal points on Earth share temperature and pressure"),
        ("S^2 cannot be covered by 2 closed sets", 2,
         "each missing at least one antipodal pair",
         "corollary of Borsuk-Ulam: need at least 3 closed sets"),
    ]

    _APPLICATIONS_HARD = [
        ("Borsuk-Ulam for S^n -> R^n", 3,
         "exists antipodal pair mapped to same point",
         "generalises: no odd map S^n -> S^{n-1} exists"),
        ("Lusternik-Schnirelmann: S^n covered by n+2 open sets", 3,
         "at least one set contains an antipodal pair",
         "minimum closed cover of S^n without antipodal pairs = n+1"),
        ("no continuous injection S^2 -> R^2", 2,
         "injection would give f(x) != f(-x) for all x, contradiction",
         "topological dimension: S^2 does not embed in R^1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "borsuk_ulam"

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
            difficulty: Controls application depth.

        Returns:
            Task description string.
        """
        return "apply Borsuk-Ulam theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Borsuk-Ulam application problem.

        Args:
            difficulty: Controls application depth.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._APPLICATIONS_EASY
        elif difficulty <= 6:
            pool = self._APPLICATIONS_EASY + self._APPLICATIONS_MED
        else:
            pool = self._APPLICATIONS_EASY + self._APPLICATIONS_MED + self._APPLICATIONS_HARD

        context, n, conclusion, reason = self._rng.choice(pool)
        problem = f"{context}. What does Borsuk-Ulam imply?"
        return problem, {
            "context": context, "n": n,
            "conclusion": conclusion, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Borsuk-Ulam application steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the application.
        """
        return [
            f"setting: {data['context']}",
            f"Borsuk-Ulam (n={data['n']}): for f: S^n -> R^n, "
            f"exists x with f(x) = f(-x)",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Conclusion of the application.
        """
        return data["conclusion"]


# ===================================================================
# 7. LEFSCHETZ FIXED POINT (tier 7)
# ===================================================================

@register
class LefschetzFixedPointGenerator(StepGenerator):
    """Compute the Lefschetz number and determine fixed point existence.

    L(f) = sum (-1)^n * tr(f_*: H_n -> H_n). If L(f) != 0, then f
    has a fixed point. Computes for identity, rotations, reflections.

    Difficulty scaling:
        Difficulty 1-3: identity on S^n, D^n.
        Difficulty 4-6: degree-d maps on S^n.
        Difficulty 7-8: maps on torus, projective space.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _MAPS_EASY = [
        ("identity on S^2", [1, 0, 1], 2,
         "L(id) = chi(S^2) = 2 != 0, has fixed point"),
        ("identity on D^2", [1], 1,
         "L(id) = 1 != 0, disk is contractible"),
        ("identity on S^1", [1, 1], 0,
         "L(id) = 1 - 1 = 0, no conclusion (S^1 rotation is fixed-point-free)"),
    ]

    _MAPS_MED = [
        ("antipodal on S^2", [1, 0, -1], 0,
         "L = 1 + 0 + (-1) = 0, no conclusion (indeed no fixed point)"),
        ("degree-2 map on S^2", [1, 0, 2], 3,
         "L = 1 - 0 + 2 = 3 != 0, has fixed point"),
        ("degree-(-1) map on S^2 (reflection)", [1, 0, -1], 0,
         "L = 1 + (-1) = 0, no forced fixed point"),
    ]

    _MAPS_HARD = [
        ("identity on T^2", [1, 2, 1], 0,
         "L(id) = 1 - 2 + 1 = 0, chi(T^2) = 0"),
        ("constant map on S^2", [1, 0, 0], 1,
         "L = 1, constant map always has fixed point"),
        ("identity on RP^2", [1, 0, 1], 1,
         "L(id) = chi(RP^2) = 1 != 0, has fixed point"),
        ("(x,y) -> (-x,-y) on T^2", [1, -2, 1], 4,
         "L = 1 + 2 + 1 = 4 != 0, has fixed points"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lefschetz_fixed_point"

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
            difficulty: Controls map complexity.

        Returns:
            Task description string.
        """
        return "compute Lefschetz number and determine fixed points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lefschetz fixed point problem.

        Args:
            difficulty: Controls map complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._MAPS_EASY
        elif difficulty <= 6:
            pool = self._MAPS_EASY + self._MAPS_MED
        else:
            pool = self._MAPS_EASY + self._MAPS_MED + self._MAPS_HARD

        desc, traces, lefschetz, reason = self._rng.choice(pool)
        problem = f"f: {desc}. Compute L(f) and determine if f has a fixed point."
        return problem, {
            "desc": desc, "traces": traces,
            "lefschetz": lefschetz, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lefschetz number computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        traces = data["traces"]
        terms = []
        for i, t in enumerate(traces):
            sign = "+" if i % 2 == 0 else "-"
            terms.append(f"({sign}){t}")
        has_fp = "yes (L != 0)" if data["lefschetz"] != 0 else "inconclusive (L = 0)"
        return [
            f"map: {data['desc']}",
            f"L(f) = sum (-1)^n * tr(f_*|H_n)",
            f"traces: {', '.join(terms)}",
            f"L(f) = {data['lefschetz']}, fixed point: {has_fp}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Lefschetz number and fixed point conclusion.
        """
        has_fp = "has fixed point" if data["lefschetz"] != 0 else "no conclusion"
        return f"L(f) = {data['lefschetz']}, {has_fp}"


# ===================================================================
# 8. COVERING DEGREE (tier 6)
# ===================================================================

@register
class CoveringDegreeGenerator(StepGenerator):
    """Compute the degree of a covering space.

    For an n-fold cover p: Xtilde -> X, the index
    |pi_1(X) / p_*(pi_1(Xtilde))| = n. Includes standard coverings
    R -> S^1, S^1 -> S^1 (z -> z^n), and universal covers.

    Difficulty scaling:
        Difficulty 1-3: R -> S^1 (infinite), S^1 -> S^1 (z->z^2).
        Difficulty 4-6: higher degree covers, S^n -> RP^n.
        Difficulty 7-8: torus covers, composition of covers.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _COVERS_EASY = [
        ("R -> S^1 (exponential map)", "infinite",
         "pi_1(R) = 0, pi_1(S^1) = Z, index = |Z/0| = infinite",
         "universal cover of S^1"),
        ("S^1 -> S^1 (z -> z^2)", "2",
         "|Z / 2Z| = 2, double cover",
         "wraps circle twice around"),
        ("S^1 -> S^1 (z -> z^3)", "3",
         "|Z / 3Z| = 3, triple cover",
         "wraps circle three times"),
    ]

    _COVERS_MED = [
        ("S^n -> RP^n (n >= 1)", "2",
         "pi_1(RP^n) = Z/2Z, universal cover S^n (n>=2)",
         "antipodal identification gives 2-fold cover"),
        ("S^1 -> S^1 (z -> z^n), n=4", "4",
         "|Z / 4Z| = 4",
         "4-fold cover of the circle"),
        ("R^2 -> T^2 (quotient by Z^2)", "infinite",
         "pi_1(T^2) = Z^2, pi_1(R^2) = 0, infinite index",
         "universal cover of the torus"),
    ]

    _COVERS_HARD = [
        ("T^2 -> T^2 (2x3 lattice)", "6",
         "sublattice of index 6 in Z^2",
         "finite cover of torus by torus"),
        ("S^3 -> SO(3)", "2",
         "pi_1(SO(3)) = Z/2Z, S^3 simply connected",
         "universal cover, double cover"),
        ("composition: R -> S^1 -> S^1 (z->z^2)", "infinite",
         "R -> S^1 is infinite, composing with finite cover stays infinite",
         "composition of universal cover with finite cover"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "covering_degree"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["euler_characteristic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls covering complexity.

        Returns:
            Task description string.
        """
        return "compute degree of covering space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a covering degree problem.

        Args:
            difficulty: Controls covering complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._COVERS_EASY
        elif difficulty <= 6:
            pool = self._COVERS_EASY + self._COVERS_MED
        else:
            pool = self._COVERS_EASY + self._COVERS_MED + self._COVERS_HARD

        cover, degree, computation, reason = self._rng.choice(pool)
        problem = f"p: {cover}. What is the degree of the covering?"
        return problem, {
            "cover": cover, "degree": degree,
            "computation": computation, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate covering degree computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the degree computation.
        """
        return [
            f"covering: {data['cover']}",
            "degree = |pi_1(X) / p_*(pi_1(Xtilde))|",
            data["computation"],
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Degree of the covering.
        """
        return f"degree = {data['degree']}"
