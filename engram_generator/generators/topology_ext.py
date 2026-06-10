"""Extended topology generators.

8 generators covering knot invariants, fundamental groups, covering
spaces, homotopy equivalence, simplicial homology, manifold
classification, quotient topology, and contractibility across tiers 6-7.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. KNOT INVARIANT (tier 7)
# ===================================================================

@register
class KnotInvariantGenerator(StepGenerator):
    """Compute crossing number and writhe for simple knots.

    Given a knot type (trefoil, figure-8, unknot, cinquefoil, etc.),
    counts positive and negative crossings from a diagram encoding
    and computes the writhe as the difference.

    Difficulty scaling:
        Difficulty 1-3: unknot and trefoil.
        Difficulty 4-6: figure-8, cinquefoil.
        Difficulty 7-8: composite knots, multiple invariants.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _KNOTS = [
        # (name, crossing_number, positive_crossings, negative_crossings)
        ("unknot", 0, 0, 0),
        ("trefoil (right)", 3, 3, 0),
        ("trefoil (left)", 3, 0, 3),
        ("figure-8", 4, 2, 2),
        ("cinquefoil", 5, 5, 0),
        ("three-twist knot", 5, 2, 3),
        ("stevedore knot", 6, 3, 3),
        ("granny knot", 6, 6, 0),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "knot_invariant"

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
            difficulty: Controls knot complexity.

        Returns:
            Task description string.
        """
        return "compute crossing number and writhe of a knot"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a knot invariant computation problem.

        Args:
            difficulty: Controls knot complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._KNOTS[:3]
        elif difficulty <= 6:
            pool = self._KNOTS[:6]
        else:
            pool = self._KNOTS

        name, cn, pos, neg = self._rng.choice(pool)
        writhe = pos - neg

        problem = (
            f"knot: {name}. "
            f"Diagram has {pos} positive and {neg} negative crossings. "
            f"Compute crossing number and writhe."
        )
        return problem, {
            "name": name, "crossing_number": cn,
            "positive": pos, "negative": neg, "writhe": writhe,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate knot invariant computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        steps = [
            f"crossing number = min crossings in any diagram = {data['crossing_number']}",
            f"positive crossings = {data['positive']}",
            f"negative crossings = {data['negative']}",
            f"writhe = n+ - n- = {data['positive']} - {data['negative']} = {data['writhe']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Crossing number and writhe.
        """
        return f"crossing_number={data['crossing_number']}, writhe={data['writhe']}"


# ===================================================================
# 2. FUNDAMENTAL GROUP (tier 7)
# ===================================================================

@register
class FundamentalGroupGenerator(StepGenerator):
    """Identify the fundamental group pi_1 for standard topological spaces.

    Uses template-based identification: pi_1(S^1) = Z, pi_1(S^2) = 0,
    pi_1(T^2) = Z x Z, pi_1(RP^2) = Z/2Z, etc.

    Difficulty scaling:
        Difficulty 1-3: S^1, S^2, R^n.
        Difficulty 4-6: torus, Klein bottle, RP^2.
        Difficulty 7-8: wedge sums, higher products.

    Prerequisites:
        homeomorphism_check (tier 7).
    """

    _SPACES_EASY = [
        ("S^1", "Z", "loop around circle generates Z"),
        ("S^2", "0", "every loop on S^2 is contractible"),
        ("R^n", "0", "R^n is contractible"),
        ("D^2 (disk)", "0", "disk is contractible"),
    ]

    _SPACES_MED = [
        ("T^2 (torus)", "Z x Z", "torus = S^1 x S^1, pi_1 = Z x Z"),
        ("RP^2", "Z/2Z", "double cover S^2 -> RP^2 gives Z/2Z"),
        ("Klein bottle", "Z x_{-1} Z", "non-orientable, semidirect product"),
        ("S^1 x R", "Z", "deformation retracts to S^1"),
    ]

    _SPACES_HARD = [
        ("S^1 v S^1 (wedge)", "Z * Z", "van Kampen: free product"),
        ("T^2 # T^2 (genus 2)", "<a,b,c,d | [a,b][c,d]=1>", "genus-2 surface"),
        ("S^1 x S^1 x S^1", "Z x Z x Z", "product of circles"),
        ("Mobius band", "Z", "deformation retracts to S^1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fundamental_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["homeomorphism_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "identify the fundamental group pi_1 of a topological space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fundamental group identification problem.

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

        space, group, reason = self._rng.choice(pool)
        problem = f"X = {space}. Determine pi_1(X)."
        return problem, {
            "space": space, "group": group, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fundamental group identification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the identification.
        """
        return [
            f"space: {data['space']}",
            data["reason"],
            f"pi_1({data['space']}) = {data['group']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The fundamental group.
        """
        return f"pi_1 = {data['group']}"


# ===================================================================
# 3. COVERING SPACE (tier 7)
# ===================================================================

@register
class CoveringSpaceGenerator(StepGenerator):
    """Count the number of sheets in a covering map.

    Template-based: R covers S^1 with infinite sheets, S^2 covers
    RP^2 with 2 sheets, S^1 covers S^1 via z^n with n sheets, etc.

    Difficulty scaling:
        Difficulty 1-3: standard 2-fold and infinite covers.
        Difficulty 4-6: n-fold circle covers, torus covers.
        Difficulty 7-8: universal covers, quotient covers.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _COVERS_EASY = [
        ("R -> S^1", "infinite", "R is universal cover of S^1"),
        ("S^2 -> RP^2", "2", "antipodal identification, 2-fold"),
        ("S^1 -> S^1 (z^2)", "2", "z -> z^2 is 2-fold cover"),
    ]

    _COVERS_MED = [
        ("S^1 -> S^1 (z^3)", "3", "z -> z^3 is 3-fold cover"),
        ("S^1 -> S^1 (z^4)", "4", "z -> z^4 is 4-fold cover"),
        ("R^2 -> T^2", "infinite", "R^2 is universal cover of torus"),
        ("S^3 -> RP^3", "2", "antipodal map, 2-fold"),
    ]

    _COVERS_HARD = [
        ("S^n -> RP^n", "2", "antipodal identification, 2-fold"),
        ("R^2 -> Klein bottle", "infinite", "universal cover"),
        ("T^2 -> T^2 (2x1)", "2", "double cover along one factor"),
        ("S^1 -> S^1 (z^6)", "6", "z -> z^6 is 6-fold cover"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "covering_space"

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
            difficulty: Controls covering complexity.

        Returns:
            Task description string.
        """
        return "count sheets of a covering map"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a covering space problem.

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

        cover, sheets, reason = self._rng.choice(pool)
        problem = f"covering map: {cover}. How many sheets?"
        return problem, {
            "cover": cover, "sheets": sheets, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate covering space steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the sheet count.
        """
        return [
            f"covering: {data['cover']}",
            data["reason"],
            f"number of sheets = {data['sheets']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Number of sheets.
        """
        return f"sheets = {data['sheets']}"


# ===================================================================
# 4. HOMOTOPY EQUIVALENCE (tier 7)
# ===================================================================

@register
class HomotopyEquivalenceGenerator(StepGenerator):
    """Determine if two topological spaces are homotopy equivalent.

    Template-based identification using deformation retracts and
    standard results: Mobius band ~ S^1, punctured plane ~ S^1,
    R^n ~ point, cylinder ~ S^1, etc.

    Difficulty scaling:
        Difficulty 1-3: obvious contractible or circle-equivalent.
        Difficulty 4-6: standard non-trivial equivalences.
        Difficulty 7-8: non-equivalent pairs, subtler reasoning.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _PAIRS_EASY = [
        ("R^n", "point", True, "R^n is contractible"),
        ("D^2", "point", True, "disk is contractible"),
        ("(0,1)", "point", True, "open interval is contractible"),
    ]

    _PAIRS_MED = [
        ("Mobius band", "S^1", True, "deformation retract to core circle"),
        ("R^2 \\ {0}", "S^1", True, "punctured plane retracts to S^1"),
        ("cylinder S^1 x [0,1]", "S^1", True, "deformation retract"),
        ("S^1", "S^2", False, "pi_1(S^1)=Z != pi_1(S^2)=0"),
    ]

    _PAIRS_HARD = [
        ("S^1 v S^1", "figure-8", True, "same space (wedge of two circles)"),
        ("S^2", "point", False, "pi_2(S^2)=Z != pi_2(point)=0"),
        ("T^2", "S^1 v S^1", False, "pi_1 differs: Z^2 vs Z*Z"),
        ("solid torus", "S^1", True, "deformation retract to core S^1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "homotopy_equivalence"

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
            difficulty: Controls pair complexity.

        Returns:
            Task description string.
        """
        return "determine if two spaces are homotopy equivalent"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a homotopy equivalence problem.

        Args:
            difficulty: Controls pair complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._PAIRS_EASY
        elif difficulty <= 6:
            pool = self._PAIRS_EASY + self._PAIRS_MED
        else:
            pool = self._PAIRS_EASY + self._PAIRS_MED + self._PAIRS_HARD

        space_a, space_b, equiv, reason = self._rng.choice(pool)
        problem = f"X = {space_a}, Y = {space_b}. Are X and Y homotopy equivalent?"
        return problem, {
            "space_a": space_a, "space_b": space_b,
            "equivalent": equiv, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate homotopy equivalence steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the reasoning.
        """
        steps = [
            f"X = {data['space_a']}, Y = {data['space_b']}",
            data["reason"],
        ]
        if data["equivalent"]:
            steps.append("X ~ Y (homotopy equivalent)")
        else:
            steps.append("X not homotopy equivalent to Y")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with reason.
        """
        if data["equivalent"]:
            return f"YES, {data['reason']}"
        return f"NO, {data['reason']}"


# ===================================================================
# 5. SIMPLICIAL HOMOLOGY (tier 7)
# ===================================================================

@register
class SimplicialHomologyGenerator(StepGenerator):
    """Compute H_0 and H_1 for small simplicial complexes.

    Uses boundary matrices for triangles, squares, and small tori.
    H_0 counts connected components, H_1 counts independent cycles.

    Difficulty scaling:
        Difficulty 1-3: single triangle, line segment.
        Difficulty 4-6: filled square, annulus.
        Difficulty 7-8: torus, Klein bottle boundaries.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _COMPLEXES_EASY = [
        ("triangle boundary (3 vertices, 3 edges, 0 faces)",
         "Z", "0", "1 component, no cycles filled"),
        ("line segment (2 vertices, 1 edge)",
         "Z", "0", "1 component, contractible"),
        ("filled triangle (3 vertices, 3 edges, 1 face)",
         "Z", "0", "1 component, face fills the cycle"),
    ]

    _COMPLEXES_MED = [
        ("square boundary (4 vertices, 4 edges)",
         "Z", "Z", "1 component, 1 cycle = 4 edges - 3 tree edges"),
        ("two disjoint triangles",
         "Z^2", "0", "2 components, no 1-cycles"),
        ("figure-8 (1 vertex, 2 edges)",
         "Z", "Z^2", "1 component, 2 independent loops"),
    ]

    _COMPLEXES_HARD = [
        ("torus triangulation (V=9, E=27, F=18)",
         "Z", "Z^2", "chi=0, connected, 2 independent 1-cycles"),
        ("RP^2 minimal (V=6, E=15, F=10)",
         "Z", "Z/2Z", "chi=1, torsion in H_1"),
        ("Klein bottle (V=9, E=27, F=18)",
         "Z", "Z + Z/2Z", "chi=0, non-orientable torsion"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simplicial_homology"

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
            difficulty: Controls complex complexity.

        Returns:
            Task description string.
        """
        return "compute H_0 and H_1 of a simplicial complex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simplicial homology problem.

        Args:
            difficulty: Controls complex complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._COMPLEXES_EASY
        elif difficulty <= 6:
            pool = self._COMPLEXES_EASY + self._COMPLEXES_MED
        else:
            pool = self._COMPLEXES_EASY + self._COMPLEXES_MED + self._COMPLEXES_HARD

        desc, h0, h1, reason = self._rng.choice(pool)
        problem = f"complex: {desc}. Compute H_0 and H_1."
        return problem, {
            "desc": desc, "h0": h0, "h1": h1, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate simplicial homology steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        return [
            f"complex: {data['desc']}",
            data["reason"],
            f"H_0 = {data['h0']}",
            f"H_1 = {data['h1']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            H_0 and H_1 values.
        """
        return f"H_0 = {data['h0']}, H_1 = {data['h1']}"


# ===================================================================
# 6. MANIFOLD CLASSIFY (tier 7)
# ===================================================================

@register
class ManifoldClassifyGenerator(StepGenerator):
    """Classify a compact 2-manifold by genus and orientability.

    Uses the classification theorem for compact surfaces. For orientable
    surfaces, chi = 2 - 2g. For non-orientable, chi = 2 - k where k
    is the number of crosscaps.

    Difficulty scaling:
        Difficulty 1-3: sphere (g=0), torus (g=1).
        Difficulty 4-6: genus 2-3 surfaces, RP^2, Klein bottle.
        Difficulty 7-8: higher genus, connected sums.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _SURFACES_EASY = [
        ("S^2", 2, True, 0, "sphere, genus 0"),
        ("T^2", 0, True, 1, "torus, genus 1"),
    ]

    _SURFACES_MED = [
        ("genus-2 surface", -2, True, 2, "chi = 2 - 2*2 = -2"),
        ("genus-3 surface", -4, True, 3, "chi = 2 - 2*3 = -4"),
        ("RP^2", 1, False, 0, "1 crosscap, non-orientable"),
        ("Klein bottle", 0, False, 0, "2 crosscaps, non-orientable"),
    ]

    _SURFACES_HARD = [
        ("genus-4 surface", -6, True, 4, "chi = 2 - 2*4 = -6"),
        ("genus-5 surface", -8, True, 5, "chi = 2 - 2*5 = -8"),
        ("RP^2 # RP^2", 0, False, 0, "Klein bottle = 2 crosscaps"),
        ("T^2 # T^2", -2, True, 2, "connected sum, genus adds"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "manifold_classify"

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
            difficulty: Controls surface complexity.

        Returns:
            Task description string.
        """
        return "classify compact 2-manifold by genus and orientability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a manifold classification problem.

        Args:
            difficulty: Controls surface complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._SURFACES_EASY
        elif difficulty <= 6:
            pool = self._SURFACES_EASY + self._SURFACES_MED
        else:
            pool = self._SURFACES_EASY + self._SURFACES_MED + self._SURFACES_HARD

        name, chi, orientable, genus, reason = self._rng.choice(pool)
        problem = f"surface: {name}, chi = {chi}. Classify by genus and orientability."
        return problem, {
            "name": name, "chi": chi, "orientable": orientable,
            "genus": genus, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate manifold classification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the classification.
        """
        steps = [f"surface: {data['name']}, chi = {data['chi']}"]
        if data["orientable"]:
            steps.append(f"orientable: chi = 2 - 2g => g = {data['genus']}")
        else:
            steps.append("non-orientable surface")
        steps.append(data["reason"])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        orient_str = "orientable" if data["orientable"] else "non-orientable"
        if data["orientable"]:
            return f"{orient_str}, genus={data['genus']}, chi={data['chi']}"
        return f"{orient_str}, chi={data['chi']}"


# ===================================================================
# 7. QUOTIENT TOPOLOGY (tier 6)
# ===================================================================

@register
class QuotientTopologyGenerator(StepGenerator):
    """Identify the quotient space resulting from an equivalence relation.

    Template-based identification: [0,1]/{0~1} = S^1, square with
    opposite sides identified = torus or Klein bottle, etc.

    Difficulty scaling:
        Difficulty 1-3: interval identifications (circle, figure-8).
        Difficulty 4-6: square identifications (torus, Klein bottle).
        Difficulty 7-8: higher-dimensional, projective spaces.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    _QUOTIENTS_EASY = [
        ("[0,1] / {0 ~ 1}", "S^1", "endpoints identified gives circle"),
        ("R / Z", "S^1", "integer translates identified gives circle"),
        ("[0,1] / {0 ~ 1/2 ~ 1}", "figure-8",
         "three points identified gives wedge of two loops"),
    ]

    _QUOTIENTS_MED = [
        ("square, opposite sides same direction", "T^2 (torus)",
         "aa^{-1}bb^{-1} word gives torus"),
        ("square, opposite sides reversed", "Klein bottle",
         "aba^{-1}b word gives Klein bottle"),
        ("D^2 / boundary", "S^2",
         "collapsing boundary of disk to point gives sphere"),
    ]

    _QUOTIENTS_HARD = [
        ("S^n / antipodal", "RP^n",
         "antipodal identification gives real projective space"),
        ("square, one pair opposite sides", "cylinder",
         "one pair identified gives cylinder"),
        ("S^1 x [0,1] / (z,0)~(z,1)", "T^2 (torus)",
         "cylinder with ends identified gives torus"),
        ("R^2 / Z^2", "T^2 (torus)",
         "lattice quotient gives torus"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quotient_topology"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["open_closed_sets"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls quotient complexity.

        Returns:
            Task description string.
        """
        return "identify the quotient space from an equivalence relation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quotient topology identification problem.

        Args:
            difficulty: Controls quotient complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._QUOTIENTS_EASY
        elif difficulty <= 6:
            pool = self._QUOTIENTS_EASY + self._QUOTIENTS_MED
        else:
            pool = self._QUOTIENTS_EASY + self._QUOTIENTS_MED + self._QUOTIENTS_HARD

        construction, result, reason = self._rng.choice(pool)
        problem = f"quotient: {construction}. Identify the resulting space."
        return problem, {
            "construction": construction, "result": result, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quotient topology steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the identification.
        """
        return [
            f"construction: {data['construction']}",
            data["reason"],
            f"result: {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The resulting quotient space.
        """
        return data["result"]


# ===================================================================
# 8. CONTRACTIBLE CHECK (tier 6)
# ===================================================================

@register
class ContractibleCheckGenerator(StepGenerator):
    """Determine if a topological space is contractible.

    A space is contractible if it is homotopy equivalent to a point.
    R^n, D^n, cones, and star-shaped sets are contractible.
    S^n (n >= 1), torus, and Klein bottle are not.

    Difficulty scaling:
        Difficulty 1-3: R^n, D^n, S^1.
        Difficulty 4-6: cones, cylinders, Mobius band.
        Difficulty 7-8: wedges, products, CW complexes.

    Prerequisites:
        continuity_topological (tier 6).
    """

    _SPACES_EASY = [
        ("R^n", True, "R^n deformation retracts to the origin"),
        ("D^2 (disk)", True, "disk contracts to center"),
        ("S^1", False, "pi_1(S^1) = Z != 0"),
        ("[0,1]", True, "interval is contractible"),
    ]

    _SPACES_MED = [
        ("cone over X", True, "any cone is contractible (retract to apex)"),
        ("S^2", False, "pi_2(S^2) = Z, not contractible"),
        ("cylinder S^1 x [0,1]", False, "pi_1 = Z, not contractible"),
        ("star-shaped subset of R^n", True, "star-shaped implies contractible"),
    ]

    _SPACES_HARD = [
        ("S^1 v S^1", False, "pi_1 = Z * Z != 0"),
        ("T^2 (torus)", False, "pi_1 = Z x Z != 0"),
        ("R^n \\ {0} (n >= 2)", False, "homotopy equivalent to S^{n-1}"),
        ("cone over S^1", True, "cone is always contractible"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "contractible_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["continuity_topological"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "determine if a topological space is contractible"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a contractibility check problem.

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

        space, contractible, reason = self._rng.choice(pool)
        problem = f"X = {space}. Is X contractible?"
        return problem, {
            "space": space, "contractible": contractible, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate contractibility check steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the reasoning.
        """
        steps = [
            f"space: {data['space']}",
            "contractible iff homotopy equivalent to a point",
            data["reason"],
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with reason.
        """
        if data["contractible"]:
            return f"YES, {data['reason']}"
        return f"NO, {data['reason']}"
