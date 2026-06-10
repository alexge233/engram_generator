"""Deep computational topology generators.

8 generators covering path-connectedness, product topology, quotient
space computation, homotopy groups, deformation retracts, surface
classification, degree of map, and nerve theorem across tiers 6-7.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _format_set(elements: list | set | frozenset) -> str:
    """Format a collection as a set string.

    Args:
        elements: Iterable of elements to format.

    Returns:
        String like ``{1, 2, 3}``.
    """
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


# ===================================================================
# 1. PATH CONNECTED (tier 6)
# ===================================================================

@register
class PathConnectedGenerator(StepGenerator):
    """Determine if a subset of R^n is path-connected.

    Template-based: intervals and convex sets are path-connected,
    disjoint unions of open sets are not. Distinguishes path-connected
    from merely connected for subtle cases.

    Difficulty scaling:
        Difficulty 1-3: intervals, single convex sets.
        Difficulty 4-6: unions, annuli, punctured disks.
        Difficulty 7-8: topologist's sine curve, surface subsets.

    Prerequisites:
        connected_check (tier 6).
    """

    _SPACES_EASY = [
        ("(0, 1)", True,
         "open interval is convex, hence path-connected"),
        ("[0, 1]", True,
         "closed interval is convex, hence path-connected"),
        ("R^n", True,
         "R^n is convex, hence path-connected"),
        ("D^2 (open disk)", True,
         "open disk is convex, hence path-connected"),
    ]

    _SPACES_MED = [
        ("(0, 1) U (2, 3)", False,
         "disjoint open intervals, no path between them"),
        ("R^2 \\ {0} (punctured plane)", True,
         "punctured plane is path-connected (go around the hole)"),
        ("annulus {(x,y) : 1 < x^2+y^2 < 4}", True,
         "annulus is path-connected (arc paths)"),
        ("{(x,y) : x^2+y^2 <= 1} U {(x,y) : (x-3)^2+y^2 <= 1}", False,
         "two disjoint closed disks, not path-connected"),
    ]

    _SPACES_HARD = [
        ("topologist's sine curve", False,
         "connected but NOT path-connected: no path to origin"),
        ("S^n (n >= 1)", True,
         "S^n is path-connected for n >= 1"),
        ("GL(n, R) (n >= 2)", False,
         "two components: det > 0 and det < 0"),
        ("SO(n) (n >= 1)", True,
         "SO(n) is connected and path-connected"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "path_connected"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["connected_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Task description string.
        """
        return "determine if a subset is path-connected"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a path-connectedness problem.

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

        space, pc, reason = self._rng.choice(pool)
        problem = f"X = {space}. Is X path-connected?"
        return problem, {
            "space": space, "path_connected": pc, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate path-connectedness steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the reasoning.
        """
        return [
            f"space: {data['space']}",
            "path-connected: for all x, y, exists continuous gamma: [0,1] -> X",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with reason.
        """
        if data["path_connected"]:
            return f"YES, {data['reason']}"
        return f"NO, {data['reason']}"


# ===================================================================
# 2. PRODUCT TOPOLOGY (tier 6)
# ===================================================================

@register
class ProductTopologyGenerator(StepGenerator):
    """Compute the product topology on X x Y from finite topologies.

    Given topologies tau_X and tau_Y on small finite sets, constructs
    the basis {U x V : U in tau_X, V in tau_Y} and lists all open
    sets in the product topology.

    Difficulty scaling:
        Difficulty 1-3: |X| = |Y| = 2.
        Difficulty 4-6: |X| = 2, |Y| = 3 or vice versa.
        Difficulty 7-8: |X| = |Y| = 3.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "product_topology"

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
            difficulty: Controls space sizes.

        Returns:
            Task description string.
        """
        return "compute basis of product topology on X x Y"

    def _make_topology(self, elements: list[int]) -> list[frozenset]:
        """Generate a valid topology on a finite set.

        Args:
            elements: Ground set elements.

        Returns:
            List of frozensets forming a valid topology.
        """
        full = frozenset(elements)
        tau = {frozenset(), full}
        n_extra = self._rng.randint(0, min(2, 2 ** len(elements) - 2))
        for _ in range(n_extra):
            size = self._rng.randint(1, len(elements) - 1)
            subset = frozenset(self._rng.sample(elements, size))
            tau.add(subset)

        changed = True
        while changed:
            changed = False
            current = list(tau)
            for i in range(len(current)):
                for j in range(i, len(current)):
                    union = current[i] | current[j]
                    inter = current[i] & current[j]
                    if union not in tau:
                        tau.add(union)
                        changed = True
                    if inter not in tau:
                        tau.add(inter)
                        changed = True
        return sorted(tau, key=lambda x: (len(x), sorted(x)))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a product topology problem.

        Args:
            difficulty: Controls space sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            nx, ny = 2, 2
        elif difficulty <= 6:
            nx = self._rng.choice([2, 3])
            ny = 3 if nx == 2 else 2
        else:
            nx, ny = 3, 3

        x_elems = list(range(1, nx + 1))
        y_elems = list(range(1, ny + 1))
        tau_x = self._make_topology(x_elems)
        tau_y = self._make_topology(y_elems)

        basis = []
        for u in tau_x:
            for v in tau_y:
                product = frozenset((a, b) for a in u for b in v)
                if product:
                    basis.append(product)

        basis_count = len(basis)

        tx_str = "{" + ", ".join(
            _format_set(s) if s else "{}" for s in tau_x
        ) + "}"
        ty_str = "{" + ", ".join(
            _format_set(s) if s else "{}" for s in tau_y
        ) + "}"

        problem = (
            f"X={_format_set(x_elems)}, tau_X={tx_str}, "
            f"Y={_format_set(y_elems)}, tau_Y={ty_str}. "
            f"List basis of product topology."
        )
        return problem, {
            "x_elems": x_elems, "y_elems": y_elems,
            "tau_x_size": len(tau_x), "tau_y_size": len(tau_y),
            "basis_count": basis_count,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate product topology steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the construction.
        """
        return [
            "basis = {U x V : U in tau_X, V in tau_Y}",
            f"|tau_X| = {data['tau_x_size']}, |tau_Y| = {data['tau_y_size']}",
            f"|basis| = {data['basis_count']} non-empty products",
            "product topology = all unions of basis elements",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Basis count.
        """
        return f"|basis| = {data['basis_count']}"


# ===================================================================
# 3. QUOTIENT SPACE COMPUTE (tier 6)
# ===================================================================

@register
class QuotientSpaceComputeGenerator(StepGenerator):
    """Identify a quotient space from an equivalence relation.

    Template-based identification of quotient constructions such as
    [0,1]/{0~1} = S^1, square with sides identified, etc. Includes
    reasoning about the identification map.

    Difficulty scaling:
        Difficulty 1-3: interval identifications.
        Difficulty 4-6: square identifications.
        Difficulty 7-8: higher-dimensional identifications.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    _QUOTIENTS_EASY = [
        ("[0,1] with 0 ~ 1", "S^1",
         "gluing endpoints of interval gives a circle"),
        ("R with x ~ x+1 for all x", "S^1",
         "quotient R/Z is the circle"),
        ("[0,2pi] with 0 ~ 2pi", "S^1",
         "identifying endpoints gives S^1"),
    ]

    _QUOTIENTS_MED = [
        ("I^2 with (x,0) ~ (x,1) and (0,y) ~ (1,y)", "T^2",
         "both pairs of opposite sides identified same direction = torus"),
        ("I^2 with (x,0) ~ (x,1) and (0,y) ~ (1,1-y)", "Klein bottle",
         "one pair same, one pair reversed = Klein bottle"),
        ("D^2 with all boundary points identified", "S^2",
         "collapsing boundary to point gives sphere"),
        ("I^2 with (x,0) ~ (1-x,1)", "Mobius band",
         "one pair reversed = Mobius band (if only one pair identified)"),
    ]

    _QUOTIENTS_HARD = [
        ("S^n with x ~ -x (antipodal)", "RP^n",
         "antipodal identification gives real projective space"),
        ("I^2 with (x,0) ~ (x,1) only (one pair)", "cylinder",
         "one pair same direction = cylinder"),
        ("S^1 x S^1 with (z,w) ~ (-z,-w)", "T^2/Z_2",
         "quotient torus by Z_2 involution"),
        ("C \\ {0} with z ~ lambda*z, |lambda|=1", "R_{>0}",
         "quotient by rotation gives positive reals"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quotient_space_compute"

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
        return "identify quotient space from equivalence relation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quotient space identification problem.

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
        problem = f"X/~ where X = {construction}. Identify X/~."
        return problem, {
            "construction": construction, "result": result, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quotient space identification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the identification.
        """
        return [
            f"space and relation: {data['construction']}",
            data["reason"],
            f"X/~ = {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Quotient space.
        """
        return data["result"]


# ===================================================================
# 4. HOMOTOPY GROUP COMPUTE (tier 7)
# ===================================================================

@register
class HomotopyGroupComputeGenerator(StepGenerator):
    """Compute pi_n(S^k) for specific n and k.

    Template-based lookup of homotopy groups of spheres with reasoning.
    Covers the stable and low-dimensional range.

    Difficulty scaling:
        Difficulty 1-3: pi_1(S^1) = Z, pi_1(S^2) = 0.
        Difficulty 4-6: pi_2(S^2), pi_n(S^1) for n >= 2.
        Difficulty 7-8: pi_3(S^2) = Z (Hopf), pi_4(S^3).

    Prerequisites:
        fundamental_group (tier 7).
    """

    _GROUPS_EASY = [
        ("pi_1(S^1)", "Z",
         "generator: loop around equator, universal cover R"),
        ("pi_1(S^2)", "0",
         "S^2 is simply connected: every loop is contractible"),
        ("pi_1(S^n) for n >= 2", "0",
         "S^n is simply connected for n >= 2"),
        ("pi_0(S^0)", "Z",
         "S^0 = two points, pi_0 counts components = Z (or Z_2)"),
    ]

    _GROUPS_MED = [
        ("pi_2(S^2)", "Z",
         "identity map generates pi_2(S^2); degree detects it"),
        ("pi_2(S^1)", "0",
         "universal cover R is contractible, so pi_n(S^1) = 0 for n >= 2"),
        ("pi_n(S^n)", "Z",
         "identity map is a generator; detected by degree"),
        ("pi_1(T^2)", "Z x Z",
         "torus = S^1 x S^1, so pi_1 = Z x Z"),
    ]

    _GROUPS_HARD = [
        ("pi_3(S^2)", "Z",
         "Hopf fibration S^3 -> S^2 generates pi_3(S^2) = Z"),
        ("pi_4(S^3)", "Z_2",
         "suspension of Hopf map; first non-trivial higher group"),
        ("pi_3(S^3)", "Z",
         "identity map generates; detected by degree"),
        ("pi_2(S^3)", "0",
         "by Hurewicz and cellular approximation"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "homotopy_group_compute"

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
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "compute homotopy group pi_n(X)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a homotopy group computation problem.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._GROUPS_EASY
        elif difficulty <= 6:
            pool = self._GROUPS_EASY + self._GROUPS_MED
        else:
            pool = self._GROUPS_EASY + self._GROUPS_MED + self._GROUPS_HARD

        notation, group, reason = self._rng.choice(pool)
        problem = f"Compute {notation}."
        return problem, {
            "notation": notation, "group": group, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate homotopy group computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        return [
            f"compute {data['notation']}",
            data["reason"],
            f"{data['notation']} = {data['group']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Homotopy group.
        """
        return f"{data['notation']} = {data['group']}"


# ===================================================================
# 5. DEFORMATION RETRACT (tier 7)
# ===================================================================

@register
class DeformationRetractGenerator(StepGenerator):
    """Identify deformation retracts of standard spaces.

    Template-based: punctured plane retracts to S^1, Mobius strip
    retracts to S^1, solid torus retracts to S^1, cylinder retracts
    to S^1, etc.

    Difficulty scaling:
        Difficulty 1-3: simple retracts (cylinder, disk minus point).
        Difficulty 4-6: Mobius strip, solid torus.
        Difficulty 7-8: more complex spaces and non-retracts.

    Prerequisites:
        homeomorphism_check (tier 7).
    """

    _RETRACTS_EASY = [
        ("R^n \\ {0}", "S^{n-1}",
         "radial projection r(x) = x/|x| is deformation retraction"),
        ("cylinder S^1 x [0,1]", "S^1",
         "project to S^1 x {0} by collapsing [0,1]"),
        ("D^2 \\ {0}", "S^1",
         "punctured disk retracts radially to boundary circle"),
    ]

    _RETRACTS_MED = [
        ("Mobius band", "S^1",
         "core circle S^1 is a deformation retract"),
        ("solid torus D^2 x S^1", "S^1",
         "collapse D^2 to center, retract to core circle"),
        ("R^2 \\ {(0,0), (1,0)}", "S^1 v S^1",
         "twice-punctured plane retracts to figure-eight"),
        ("cone minus apex CX \\ {apex}", "X",
         "retract to base X by sliding down"),
    ]

    _RETRACTS_HARD = [
        ("S^1 x R", "S^1",
         "project onto S^1 factor (R is contractible)"),
        ("R^3 \\ (line)", "S^1",
         "complement of a line retracts to a circle around it"),
        ("S^2", "point (NO)",
         "S^2 does NOT retract to a point (pi_2 != 0)"),
        ("Klein bottle minus disk", "S^1 v S^1",
         "punctured Klein bottle retracts to wedge of circles"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "deformation_retract"

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
        return "identify deformation retract of a topological space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a deformation retract identification problem.

        Args:
            difficulty: Controls space complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._RETRACTS_EASY
        elif difficulty <= 6:
            pool = self._RETRACTS_EASY + self._RETRACTS_MED
        else:
            pool = self._RETRACTS_EASY + self._RETRACTS_MED + self._RETRACTS_HARD

        space, retract, reason = self._rng.choice(pool)
        problem = f"X = {space}. Identify a deformation retract of X."
        return problem, {
            "space": space, "retract": retract, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate deformation retract steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the retraction.
        """
        return [
            f"space: {data['space']}",
            "deformation retract: A subset A with H: X x [0,1] -> X, "
            "H(x,0) = x, H(x,1) in A, H(a,t) = a",
            data["reason"],
            f"retract: {data['retract']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Deformation retract space.
        """
        return data["retract"]


# ===================================================================
# 6. SURFACE CLASSIFICATION (tier 7)
# ===================================================================

@register
class SurfaceClassificationGenerator(StepGenerator):
    """Classify a closed surface from its polygon presentation.

    Given a polygon word (e.g., aba^{-1}b^{-1} for torus), determines
    genus, orientability, and Euler characteristic using the
    classification theorem for compact surfaces.

    Difficulty scaling:
        Difficulty 1-3: sphere (aa^{-1}), torus (aba^{-1}b^{-1}).
        Difficulty 4-6: Klein bottle (abab), RP^2 (aa).
        Difficulty 7-8: genus 2+, connected sums.

    Prerequisites:
        euler_characteristic (tier 5).
    """

    _SURFACES_EASY = [
        ("aa^{-1}", "S^2", True, 0, 2,
         "word cancels completely: sphere"),
        ("aba^{-1}b^{-1}", "T^2", True, 1, 0,
         "standard torus word: genus 1, orientable"),
    ]

    _SURFACES_MED = [
        ("abab", "Klein bottle", False, 0, 0,
         "non-orientable, chi = 0, 2 crosscaps"),
        ("aa", "RP^2", False, 0, 1,
         "non-orientable, 1 crosscap, chi = 1"),
        ("aba^{-1}b^{-1}cdc^{-1}d^{-1}", "genus-2 surface", True, 2, -2,
         "two torus words: genus 2, chi = -2"),
    ]

    _SURFACES_HARD = [
        ("aba^{-1}b^{-1}cdc^{-1}d^{-1}efe^{-1}f^{-1}",
         "genus-3 surface", True, 3, -4,
         "three torus words: genus 3, chi = -4"),
        ("aabb", "Klein bottle # RP^2", False, 0, -1,
         "non-orientable, 3 crosscaps, chi = -1"),
        ("abcabc", "non-orientable genus-3", False, 0, -1,
         "non-orientable surface with chi = -1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "surface_classification"

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
        return "classify surface from polygon word presentation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a surface classification problem.

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

        word, name, orientable, genus, chi, reason = self._rng.choice(pool)
        problem = f"polygon word: {word}. Classify the surface."
        return problem, {
            "word": word, "name": name, "orientable": orientable,
            "genus": genus, "chi": chi, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate surface classification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the classification.
        """
        orient_str = "orientable" if data["orientable"] else "non-orientable"
        steps = [
            f"polygon word: {data['word']}",
            data["reason"],
            f"orientable: {orient_str}",
        ]
        if data["orientable"]:
            steps.append(f"genus = {data['genus']}, chi = 2 - 2g = {data['chi']}")
        else:
            steps.append(f"chi = {data['chi']}")
        steps.append(f"surface: {data['name']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Surface name and invariants.
        """
        orient_str = "orientable" if data["orientable"] else "non-orientable"
        return f"{data['name']}, {orient_str}, chi = {data['chi']}"


# ===================================================================
# 7. DEGREE OF MAP (tier 7)
# ===================================================================

@register
class DegreeOfMapGenerator(StepGenerator):
    """Compute the degree of a map f: S^1 -> S^1 (or S^n -> S^n).

    Template-based: f(z) = z^n has degree n, antipodal map has degree
    (-1)^{n+1}, constant map has degree 0, identity has degree 1.

    Difficulty scaling:
        Difficulty 1-3: z^n for small n, identity, constant.
        Difficulty 4-6: antipodal, compositions.
        Difficulty 7-8: suspensions, reflections.

    Prerequisites:
        fundamental_group (tier 7).
    """

    _MAPS_EASY = [
        ("f(z) = z (identity)", 1,
         "identity has degree 1"),
        ("f(z) = z^2", 2,
         "z -> z^2 winds twice around S^1"),
        ("f(z) = z^3", 3,
         "z -> z^3 winds three times"),
        ("f(z) = c (constant map)", 0,
         "constant map has degree 0"),
    ]

    _MAPS_MED = [
        ("f(z) = z^{-1} (conjugation on S^1)", -1,
         "reflection reverses orientation: degree -1"),
        ("f(z) = z^4", 4,
         "z -> z^4 winds four times"),
        ("f = g . h where deg(g)=2, deg(h)=3", 6,
         "deg(g . h) = deg(g) * deg(h) = 2 * 3 = 6"),
        ("f(z) = z^{-2}", -2,
         "winds twice in reverse: degree -2"),
    ]

    _MAPS_HARD = [
        ("antipodal map on S^n (n even)", -1,
         "deg(antipodal) = (-1)^{n+1} = -1 for even n"),
        ("antipodal map on S^n (n odd)", 1,
         "deg(antipodal) = (-1)^{n+1} = 1 for odd n"),
        ("f(z) = z^5", 5,
         "z -> z^5: degree 5"),
        ("reflection on S^2", -1,
         "single coordinate reflection has degree -1"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "degree_of_map"

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
        return "compute degree of map between spheres"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a degree of map problem.

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

        description, degree, reason = self._rng.choice(pool)
        problem = f"{description}. Compute deg(f)."
        return problem, {
            "description": description, "degree": degree, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate degree computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the degree computation.
        """
        return [
            f"map: {data['description']}",
            "deg(f) = induced map on H_n: f_*: Z -> Z is multiplication by deg(f)",
            data["reason"],
            f"deg(f) = {data['degree']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Degree value.
        """
        return f"deg(f) = {data['degree']}"


# ===================================================================
# 8. NERVE THEOREM (tier 6)
# ===================================================================

@register
class NerveTheoremGenerator(StepGenerator):
    """Build the nerve of a cover and count simplices.

    Given a cover of a finite set by subsets, constructs the nerve
    simplicial complex where k-simplices correspond to (k+1)-fold
    intersections. Counts vertices, edges, and triangles.

    Difficulty scaling:
        Difficulty 1-3: 3-4 sets with simple overlaps.
        Difficulty 4-6: 4-5 sets with richer intersections.
        Difficulty 7-8: 5-6 sets with triple intersections.

    Prerequisites:
        set_operations (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nerve_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls cover complexity.

        Returns:
            Task description string.
        """
        return "build nerve of cover and count simplices"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nerve theorem problem.

        Args:
            difficulty: Controls cover complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_sets = self._rng.randint(3, 4)
            universe_size = 5
        elif difficulty <= 6:
            n_sets = self._rng.randint(4, 5)
            universe_size = 7
        else:
            n_sets = self._rng.randint(5, 6)
            universe_size = 9

        universe = list(range(1, universe_size + 1))
        cover = []
        for _ in range(n_sets):
            size = self._rng.randint(2, max(2, universe_size // 2 + 1))
            subset = frozenset(self._rng.sample(universe, size))
            cover.append(subset)

        vertices = list(range(n_sets))
        edges = []
        for i in range(n_sets):
            for j in range(i + 1, n_sets):
                if cover[i] & cover[j]:
                    edges.append((i, j))

        triangles = []
        for i in range(n_sets):
            for j in range(i + 1, n_sets):
                for k in range(j + 1, n_sets):
                    if cover[i] & cover[j] & cover[k]:
                        triangles.append((i, j, k))

        cover_strs = []
        for idx, s in enumerate(cover):
            cover_strs.append(f"U{idx} = {_format_set(s)}")

        problem = (
            f"cover: {'; '.join(cover_strs)}. "
            f"Build the nerve complex."
        )
        return problem, {
            "n_sets": n_sets, "cover_strs": cover_strs,
            "n_vertices": len(vertices),
            "n_edges": len(edges),
            "n_triangles": len(triangles),
            "edges": edges, "triangles": triangles,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate nerve construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps building the nerve.
        """
        steps = [
            "nerve: vertex for each set, edge for pairwise intersection",
            f"0-simplices (vertices): {data['n_vertices']}",
        ]
        if data["edges"]:
            edge_strs = [f"({i},{j})" for i, j in data["edges"][:6]]
            steps.append(
                f"1-simplices (edges): {data['n_edges']} "
                f"[{', '.join(edge_strs)}{'...' if len(data['edges']) > 6 else ''}]"
            )
        else:
            steps.append("1-simplices (edges): 0")
        steps.append(f"2-simplices (triangles): {data['n_triangles']}")
        euler = data["n_vertices"] - data["n_edges"] + data["n_triangles"]
        steps.append(
            f"chi(nerve) = {data['n_vertices']} - {data['n_edges']} "
            f"+ {data['n_triangles']} = {euler}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Simplex counts and Euler characteristic.
        """
        euler = data["n_vertices"] - data["n_edges"] + data["n_triangles"]
        return (
            f"V={data['n_vertices']}, E={data['n_edges']}, "
            f"F={data['n_triangles']}, chi={euler}"
        )
