"""Topology generators.

8 generators covering point-set topology, continuity, homeomorphisms,
Euler characteristic, connectedness, compactness, and fixed-point
theorems across tiers 5-7.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _format_set(elements: list | set) -> str:
    """Format a collection as a set string.

    Args:
        elements: Iterable of elements to format.

    Returns:
        String like ``{1, 2, 3}``.
    """
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


def _format_topology(tau: list[frozenset]) -> str:
    """Format a topology as a string of open sets.

    Args:
        tau: List of frozensets representing open sets.

    Returns:
        String representation of the topology.
    """
    parts = []
    for s in sorted(tau, key=lambda x: (len(x), sorted(x))):
        if len(s) == 0:
            parts.append("{}")
        else:
            parts.append("{" + ", ".join(str(e) for e in sorted(s)) + "}")
    return "{" + ", ".join(parts) + "}"


# ═══════════════════════════════════════════════════════════════════
# 1. OPEN / CLOSED SETS (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class OpenClosedSetsGenerator(StepGenerator):
    """Determine if a subset of R is open, closed, both, or neither.

    Given a subset of R (interval or finite set) and a topology
    (standard, discrete, or indiscrete), determines the topological
    classification of the subset.

    Difficulty scaling:
        Difficulty 1-3: simple intervals with standard topology.
        Difficulty 4-6: half-open intervals, finite sets, mixed topologies.
        Difficulty 7-8: singletons, unions, indiscrete topology.

    Prerequisites:
        set_membership (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "open_closed_sets"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_membership"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls subset and topology complexity.

        Returns:
            Task description string.
        """
        return "classify subset as open, closed, both, or neither"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an open/closed classification problem.

        Args:
            difficulty: Controls subset and topology complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            topology = "standard"
            kind = self._rng.choice(["open_interval", "closed_interval"])
        elif difficulty <= 6:
            topology = self._rng.choice(["standard", "discrete"])
            kind = self._rng.choice([
                "open_interval", "closed_interval",
                "half_open", "finite",
            ])
        else:
            topology = self._rng.choice(["standard", "discrete", "indiscrete"])
            kind = self._rng.choice([
                "open_interval", "closed_interval",
                "half_open", "singleton", "R",
            ])

        a = self._rng.randint(-5, 4)
        b = a + self._rng.randint(1, 5)

        if kind == "open_interval":
            subset_str = f"({a}, {b})"
            is_open_std = True
            is_closed_std = False
        elif kind == "closed_interval":
            subset_str = f"[{a}, {b}]"
            is_open_std = False
            is_closed_std = True
        elif kind == "half_open":
            if self._rng.random() < 0.5:
                subset_str = f"[{a}, {b})"
            else:
                subset_str = f"({a}, {b}]"
            is_open_std = False
            is_closed_std = False
        elif kind == "singleton":
            subset_str = "{" + str(a) + "}"
            is_open_std = False
            is_closed_std = True
        elif kind == "finite":
            n = self._rng.randint(2, 4)
            pts = sorted(self._rng.sample(range(-5, 10), n))
            subset_str = "{" + ", ".join(str(p) for p in pts) + "}"
            is_open_std = False
            is_closed_std = True
        else:
            subset_str = "R"
            is_open_std = True
            is_closed_std = True

        if topology == "discrete":
            is_open = True
            is_closed = True
        elif topology == "indiscrete":
            if kind == "R":
                is_open = True
                is_closed = True
            else:
                is_open = False
                is_closed = False
        else:
            is_open = is_open_std
            is_closed = is_closed_std

        if is_open and is_closed:
            classification = "clopen"
        elif is_open:
            classification = "open"
        elif is_closed:
            classification = "closed"
        else:
            classification = "neither"

        problem = f"S={subset_str} in ({topology} topology on R)"
        return problem, {
            "subset_str": subset_str, "topology": topology,
            "kind": kind, "is_open": is_open, "is_closed": is_closed,
            "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the classification reasoning.
        """
        top = data["topology"]
        kind = data["kind"]
        steps = []
        if top == "discrete":
            steps.append("discrete topology: every subset is open and closed")
        elif top == "indiscrete":
            if kind == "R":
                steps.append("R and {} are the only open sets; R is clopen")
            else:
                steps.append("indiscrete: only R and {} are open")
                steps.append("complement is not R or {}, so not open")
        else:
            if kind == "open_interval":
                steps.append("(a,b) contains a ball around each point")
                steps.append("complement (-inf,a]U[b,inf) is closed")
            elif kind == "closed_interval":
                steps.append("[a,b] contains its limit points")
                steps.append("not open: no ball around a stays inside")
            elif kind == "half_open":
                steps.append("missing one endpoint: not closed")
                steps.append("includes one endpoint: not open")
            elif kind == "singleton":
                steps.append("singleton is closed (complement is open)")
                steps.append("no open ball fits inside a point")
            elif kind == "finite":
                steps.append("finite subset of R is closed")
                steps.append("finite set has no interior points")
            else:
                steps.append("R is both open and closed by definition")
        steps.append(f"open={data['is_open']}, closed={data['is_closed']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        return data["classification"]


# ═══════════════════════════════════════════════════════════════════
# 2. CLOSURE AND INTERIOR (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ClosureInteriorGenerator(StepGenerator):
    """Compute the closure and interior of a subset of R.

    For intervals in the standard topology: int((a,b])=(a,b),
    cl((a,b))=[a,b], etc. For finite sets: interior is empty,
    closure is the set itself.

    Difficulty scaling:
        Difficulty 1-3: open or closed intervals.
        Difficulty 4-6: half-open intervals.
        Difficulty 7-8: finite sets, rationals in an interval.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "closure_interior"

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
            difficulty: Controls subset complexity.

        Returns:
            Task description string.
        """
        return "compute closure and interior of subset of R"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a closure/interior computation problem.

        Args:
            difficulty: Controls subset complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(-5, 4)
        b = a + self._rng.randint(1, 5)

        if difficulty <= 3:
            kind = self._rng.choice(["open", "closed"])
        elif difficulty <= 6:
            kind = self._rng.choice(["open", "closed", "half_open_left", "half_open_right"])
        else:
            kind = self._rng.choice([
                "open", "closed", "half_open_left",
                "half_open_right", "finite", "rationals",
            ])

        if kind == "open":
            subset_str = f"({a}, {b})"
            interior = f"({a}, {b})"
            closure = f"[{a}, {b}]"
        elif kind == "closed":
            subset_str = f"[{a}, {b}]"
            interior = f"({a}, {b})"
            closure = f"[{a}, {b}]"
        elif kind == "half_open_left":
            subset_str = f"[{a}, {b})"
            interior = f"({a}, {b})"
            closure = f"[{a}, {b}]"
        elif kind == "half_open_right":
            subset_str = f"({a}, {b}]"
            interior = f"({a}, {b})"
            closure = f"[{a}, {b}]"
        elif kind == "finite":
            n = self._rng.randint(2, 4)
            pts = sorted(self._rng.sample(range(-5, 10), n))
            subset_str = "{" + ", ".join(str(p) for p in pts) + "}"
            interior = "{}"
            closure = subset_str
        else:
            subset_str = f"Q ∩ ({a}, {b})"
            interior = "{}"
            closure = f"[{a}, {b}]"

        problem = f"S={subset_str} in standard topology. Find int(S) and cl(S)."
        return problem, {
            "subset_str": subset_str, "kind": kind,
            "a": a, "b": b,
            "interior": interior, "closure": closure,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate closure/interior computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the computation.
        """
        kind = data["kind"]
        steps = []
        if kind in ("open", "closed", "half_open_left", "half_open_right"):
            steps.append(f"interior = largest open subset = ({data['a']}, {data['b']})")
            steps.append(f"closure = smallest closed superset = [{data['a']}, {data['b']}]")
        elif kind == "finite":
            steps.append("finite set has empty interior in R")
            steps.append("finite set is closed, so cl(S) = S")
        else:
            steps.append("Q is dense in R, so cl(Q ∩ (a,b)) = [a,b]")
            steps.append("Q has empty interior (irrationals in every ball)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Interior and closure as a string.
        """
        return f"int(S)={data['interior']}, cl(S)={data['closure']}"


# ═══════════════════════════════════════════════════════════════════
# 3. CONTINUITY (TOPOLOGICAL) (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ContinuityTopologicalGenerator(StepGenerator):
    """Verify if a map between finite topological spaces is continuous.

    A map f: X -> Y is continuous iff the preimage of every open set
    in Y is open in X. Works on small finite spaces with explicitly
    listed topologies.

    Difficulty scaling:
        Difficulty 1-3: 2-3 element spaces, few open sets.
        Difficulty 4-6: 3-4 element spaces.
        Difficulty 7-8: 4-5 element spaces, richer topologies.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "continuity_topological"

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
            difficulty: Controls space size.

        Returns:
            Task description string.
        """
        return "check if map between finite topological spaces is continuous"

    def _make_topology(self, elements: list[int]) -> list[frozenset]:
        """Generate a valid topology on a finite set.

        Generates a topology by starting with empty set and full set,
        then adding random subsets and closing under union and finite
        intersection.

        Args:
            elements: Ground set elements.

        Returns:
            List of frozensets forming a valid topology.
        """
        full = frozenset(elements)
        tau = {frozenset(), full}
        n_extra = self._rng.randint(0, min(3, 2 ** len(elements) - 2))
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
        """Generate a topological continuity check problem.

        Args:
            difficulty: Controls space sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
        elif difficulty <= 6:
            n = self._rng.randint(3, 4)
        else:
            n = self._rng.randint(4, 5)

        x_elems = list(range(1, n + 1))
        m = self._rng.randint(2, n)
        y_elems = list(range(1, m + 1))

        tau_x = self._make_topology(x_elems)
        tau_y = self._make_topology(y_elems)

        f_map = {}
        for x in x_elems:
            f_map[x] = self._rng.choice(y_elems)

        continuous = True
        failing_set = None
        for v_set in tau_y:
            preimage = frozenset(x for x in x_elems if f_map[x] in v_set)
            if preimage not in set(tau_x):
                continuous = False
                failing_set = v_set
                break

        f_str = ", ".join(f"f({x})={f_map[x]}" for x in x_elems)
        problem = (
            f"X={_format_set(x_elems)}, tau_X={_format_topology(tau_x)}, "
            f"Y={_format_set(y_elems)}, tau_Y={_format_topology(tau_y)}, "
            f"{f_str}. Is f continuous?"
        )
        return problem, {
            "x_elems": x_elems, "y_elems": y_elems,
            "tau_x": tau_x, "tau_y": tau_y,
            "f_map": f_map, "continuous": continuous,
            "failing_set": failing_set,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate continuity check steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking preimages of open sets.
        """
        steps = []
        f_map = data["f_map"]
        x_elems = data["x_elems"]
        tau_x_set = set(data["tau_x"])
        for v_set in data["tau_y"]:
            preimage = frozenset(x for x in x_elems if f_map[x] in v_set)
            v_str = _format_set(v_set) if v_set else "{}"
            p_str = _format_set(preimage) if preimage else "{}"
            status = "open" if preimage in tau_x_set else "NOT open"
            steps.append(f"f^-1({v_str})={p_str} -> {status}")
            if preimage not in tau_x_set:
                break
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with explanation.
        """
        if data["continuous"]:
            return "YES, all preimages of open sets are open"
        fs = data["failing_set"]
        fs_str = _format_set(fs) if fs else "{}"
        return f"NO, f^-1({fs_str}) is not open in X"


# ═══════════════════════════════════════════════════════════════════
# 4. HOMEOMORPHISM CHECK (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class HomeomorphismCheckGenerator(StepGenerator):
    """Check if a bijection between finite topological spaces is a homeomorphism.

    Given a bijection f between two finite topological spaces, checks
    whether both f and f^-1 are continuous (preimage of every open set
    is open).

    Difficulty scaling:
        Difficulty 1-3: 2-3 element spaces.
        Difficulty 4-6: 3-4 element spaces.
        Difficulty 7-8: 4-5 element spaces.

    Prerequisites:
        continuity_topological (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "homeomorphism_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["continuity_topological"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls space size.

        Returns:
            Task description string.
        """
        return "check if bijection is a homeomorphism"

    def _make_topology(self, elements: list[int]) -> list[frozenset]:
        """Generate a valid topology on a finite set.

        Args:
            elements: Ground set elements.

        Returns:
            List of frozensets forming a valid topology.
        """
        full = frozenset(elements)
        tau = {frozenset(), full}
        n_extra = self._rng.randint(0, min(3, 2 ** len(elements) - 2))
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

    def _check_continuous(self, f_map: dict, domain_elems: list[int],
                          tau_domain: list[frozenset],
                          tau_codomain: list[frozenset]) -> tuple[bool, frozenset | None]:
        """Check if a map is continuous.

        Args:
            f_map: Mapping from domain to codomain.
            domain_elems: Elements of the domain.
            tau_domain: Topology on the domain.
            tau_codomain: Topology on the codomain.

        Returns:
            Tuple of (is_continuous, failing_open_set_or_None).
        """
        tau_set = set(tau_domain)
        for v_set in tau_codomain:
            preimage = frozenset(x for x in domain_elems if f_map[x] in v_set)
            if preimage not in tau_set:
                return False, v_set
        return True, None

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a homeomorphism check problem.

        Args:
            difficulty: Controls space sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
        elif difficulty <= 6:
            n = self._rng.randint(3, 4)
        else:
            n = self._rng.randint(4, 5)

        x_elems = list(range(1, n + 1))
        y_elems = list(range(1, n + 1))

        tau_x = self._make_topology(x_elems)
        tau_y = self._make_topology(y_elems)

        perm = list(range(1, n + 1))
        self._rng.shuffle(perm)
        f_map = {x_elems[i]: perm[i] for i in range(n)}
        f_inv = {v: k for k, v in f_map.items()}

        f_cont, f_fail = self._check_continuous(f_map, x_elems, tau_x, tau_y)
        f_inv_cont, fi_fail = self._check_continuous(f_inv, y_elems, tau_y, tau_x)
        is_homeo = f_cont and f_inv_cont

        f_str = ", ".join(f"f({k})={v}" for k, v in sorted(f_map.items()))
        problem = (
            f"X={_format_set(x_elems)}, tau_X={_format_topology(tau_x)}, "
            f"Y={_format_set(y_elems)}, tau_Y={_format_topology(tau_y)}, "
            f"{f_str}. Is f a homeomorphism?"
        )
        return problem, {
            "x_elems": x_elems, "y_elems": y_elems,
            "tau_x": tau_x, "tau_y": tau_y,
            "f_map": f_map, "f_inv": f_inv,
            "f_cont": f_cont, "f_inv_cont": f_inv_cont,
            "f_fail": f_fail, "fi_fail": fi_fail,
            "is_homeo": is_homeo,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate homeomorphism check steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking continuity of f and f^-1.
        """
        steps = [f"f is bijective (permutation)"]
        if data["f_cont"]:
            steps.append("f is continuous: all preimages of open sets are open")
        else:
            fs = data["f_fail"]
            fs_str = _format_set(fs) if fs else "{}"
            steps.append(f"f NOT continuous: f^-1({fs_str}) not open in X")
        if data["f_inv_cont"]:
            steps.append("f^-1 is continuous: all preimages are open")
        else:
            fs = data["fi_fail"]
            fs_str = _format_set(fs) if fs else "{}"
            steps.append(f"f^-1 NOT continuous: (f^-1)^-1({fs_str}) not open in Y")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with reason.
        """
        if data["is_homeo"]:
            return "YES, f and f^-1 are both continuous"
        reasons = []
        if not data["f_cont"]:
            reasons.append("f not continuous")
        if not data["f_inv_cont"]:
            reasons.append("f^-1 not continuous")
        return "NO, " + " and ".join(reasons)


# ═══════════════════════════════════════════════════════════════════
# 5. EULER CHARACTERISTIC (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class EulerCharacteristicGenerator(StepGenerator):
    """Compute V - E + F for polyhedra and planar graphs.

    Given the vertex, edge, and face counts of a convex polyhedron
    or a connected planar graph, computes the Euler characteristic
    chi = V - E + F.

    Difficulty scaling:
        Difficulty 1-3: standard polyhedra (tetrahedron, cube, etc.).
        Difficulty 4-6: more complex polyhedra (icosahedron, truncated).
        Difficulty 7-8: planar graphs with given V, E, F.

    Prerequisites:
        addition (tier 0), subtraction (tier 0).
    """

    _POLYHEDRA = [
        ("tetrahedron", 4, 6, 4),
        ("cube", 8, 12, 6),
        ("octahedron", 6, 12, 8),
        ("dodecahedron", 20, 30, 12),
        ("icosahedron", 12, 30, 20),
        ("triangular prism", 6, 9, 5),
        ("square pyramid", 5, 8, 5),
        ("pentagonal prism", 10, 15, 7),
        ("hexagonal prism", 12, 18, 8),
        ("truncated tetrahedron", 12, 18, 8),
        ("cuboctahedron", 12, 24, 14),
        ("truncated cube", 24, 36, 14),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "euler_characteristic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls polyhedra complexity.

        Returns:
            Task description string.
        """
        return "compute Euler characteristic V - E + F"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler characteristic problem.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._POLYHEDRA[:5]
            name, v, e, f = self._rng.choice(pool)
            chi = v - e + f
            problem = f"{name}: V={v}, E={e}, F={f}. Compute chi = V-E+F."
            return problem, {
                "name": name, "v": v, "e": e, "f": f,
                "chi": chi, "source": "polyhedron",
            }
        elif difficulty <= 6:
            pool = self._POLYHEDRA[5:]
            name, v, e, f = self._rng.choice(pool)
            chi = v - e + f
            problem = f"{name}: V={v}, E={e}, F={f}. Compute chi = V-E+F."
            return problem, {
                "name": name, "v": v, "e": e, "f": f,
                "chi": chi, "source": "polyhedron",
            }
        else:
            v = self._rng.randint(4, 12)
            max_e = v * (v - 1) // 2
            e = self._rng.randint(v - 1, min(max_e, 3 * v - 6))
            f = 2 - v + e
            chi = v - e + f
            problem = f"planar graph: V={v}, E={e}, F={f}. Compute chi = V-E+F."
            return problem, {
                "name": "planar graph", "v": v, "e": e, "f": f,
                "chi": chi, "source": "graph",
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler characteristic computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        v, e, f = data["v"], data["e"], data["f"]
        steps = [
            f"V - E + F = {v} - {e} + {f}",
            f"= {v - e} + {f}",
            f"= {data['chi']}",
        ]
        if data["source"] == "polyhedron":
            steps.append("Euler formula: chi=2 for convex polyhedra")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Euler characteristic value.
        """
        return str(data["chi"])


# ═══════════════════════════════════════════════════════════════════
# 6. CONNECTED CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ConnectedCheckGenerator(StepGenerator):
    """Determine if a finite topological space is connected.

    A topological space is connected if it cannot be partitioned into
    two non-empty disjoint open sets. Tests this on small finite spaces
    with explicitly listed topologies.

    Difficulty scaling:
        Difficulty 1-3: 2-3 element spaces.
        Difficulty 4-6: 3-4 element spaces.
        Difficulty 7-8: 4-5 element spaces.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "connected_check"

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
            difficulty: Controls space size.

        Returns:
            Task description string.
        """
        return "determine if finite topological space is connected"

    def _make_topology(self, elements: list[int]) -> list[frozenset]:
        """Generate a valid topology on a finite set.

        Args:
            elements: Ground set elements.

        Returns:
            List of frozensets forming a valid topology.
        """
        full = frozenset(elements)
        tau = {frozenset(), full}
        n_extra = self._rng.randint(0, min(3, 2 ** len(elements) - 2))
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
        """Generate a connectedness check problem.

        Args:
            difficulty: Controls space size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
        elif difficulty <= 6:
            n = self._rng.randint(3, 4)
        else:
            n = self._rng.randint(4, 5)

        elements = list(range(1, n + 1))
        tau = self._make_topology(elements)
        full = frozenset(elements)

        disconnection = None
        connected = True
        tau_set = set(tau)
        for u_set in tau:
            if not u_set or u_set == full:
                continue
            complement = full - u_set
            if complement in tau_set:
                connected = False
                disconnection = (u_set, complement)
                break

        problem = (
            f"X={_format_set(elements)}, "
            f"tau={_format_topology(tau)}. Is X connected?"
        )
        return problem, {
            "elements": elements, "tau": tau,
            "connected": connected, "disconnection": disconnection,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate connectedness check steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the reasoning.
        """
        steps = ["check for partition into two non-empty open sets"]
        if data["connected"]:
            steps.append("no non-trivial clopen subsets found")
            steps.append("space is connected")
        else:
            u, v = data["disconnection"]
            u_str = _format_set(u) if u else "{}"
            v_str = _format_set(v) if v else "{}"
            steps.append(f"U={u_str} and V={v_str} are both open")
            steps.append("U and V partition X => disconnected")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        if data["connected"]:
            return "YES, connected"
        u, v = data["disconnection"]
        u_str = _format_set(u) if u else "{}"
        v_str = _format_set(v) if v else "{}"
        return f"NO, {u_str} and {v_str} disconnect X"


# ═══════════════════════════════════════════════════════════════════
# 7. COMPACTNESS CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class CompactnessCheckGenerator(StepGenerator):
    """Determine if a subset of R is compact using Heine-Borel.

    A subset of R is compact iff it is closed and bounded. Generates
    various subsets (intervals, rays, finite sets, unions) and applies
    the Heine-Borel theorem.

    Difficulty scaling:
        Difficulty 1-3: closed intervals, open intervals.
        Difficulty 4-6: half-open intervals, finite sets, rays.
        Difficulty 7-8: unions of intervals, unbounded sets.

    Prerequisites:
        open_closed_sets (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compactness_check"

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
            difficulty: Controls subset complexity.

        Returns:
            Task description string.
        """
        return "determine if subset of R is compact (Heine-Borel)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compactness check problem.

        Args:
            difficulty: Controls subset complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(-5, 4)
        b = a + self._rng.randint(1, 5)

        if difficulty <= 3:
            kind = self._rng.choice(["closed_interval", "open_interval"])
        elif difficulty <= 6:
            kind = self._rng.choice([
                "closed_interval", "open_interval",
                "half_open", "finite", "ray",
            ])
        else:
            kind = self._rng.choice([
                "closed_interval", "open_interval",
                "half_open", "ray", "R", "union",
            ])

        if kind == "closed_interval":
            subset_str = f"[{a}, {b}]"
            is_closed = True
            is_bounded = True
        elif kind == "open_interval":
            subset_str = f"({a}, {b})"
            is_closed = False
            is_bounded = True
        elif kind == "half_open":
            if self._rng.random() < 0.5:
                subset_str = f"[{a}, {b})"
            else:
                subset_str = f"({a}, {b}]"
            is_closed = False
            is_bounded = True
        elif kind == "finite":
            n = self._rng.randint(2, 5)
            pts = sorted(self._rng.sample(range(-5, 10), n))
            subset_str = "{" + ", ".join(str(p) for p in pts) + "}"
            is_closed = True
            is_bounded = True
        elif kind == "ray":
            if self._rng.random() < 0.5:
                subset_str = f"[{a}, inf)"
            else:
                subset_str = f"(-inf, {a}]"
            is_closed = True
            is_bounded = False
        elif kind == "R":
            subset_str = "R"
            is_closed = True
            is_bounded = False
        else:
            c = b + self._rng.randint(1, 3)
            d = c + self._rng.randint(1, 3)
            subset_str = f"[{a}, {b}] U [{c}, {d}]"
            is_closed = True
            is_bounded = True

        is_compact = is_closed and is_bounded

        problem = f"S={subset_str}. Is S compact?"
        return problem, {
            "subset_str": subset_str, "kind": kind,
            "is_closed": is_closed, "is_bounded": is_bounded,
            "is_compact": is_compact,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate compactness check steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying Heine-Borel theorem.
        """
        steps = [
            "Heine-Borel: compact in R iff closed and bounded",
            f"closed: {'YES' if data['is_closed'] else 'NO'}",
            f"bounded: {'YES' if data['is_bounded'] else 'NO'}",
        ]
        if data["is_compact"]:
            steps.append("closed and bounded => compact")
        else:
            reasons = []
            if not data["is_closed"]:
                reasons.append("not closed")
            if not data["is_bounded"]:
                reasons.append("not bounded")
            steps.append(" and ".join(reasons) + " => not compact")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with reason.
        """
        if data["is_compact"]:
            return "YES, closed and bounded"
        reasons = []
        if not data["is_closed"]:
            reasons.append("not closed")
        if not data["is_bounded"]:
            reasons.append("not bounded")
        return "NO, " + " and ".join(reasons)


# ═══════════════════════════════════════════════════════════════════
# 8. FIXED POINT EXISTENCE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class FixedPointExistenceGenerator(StepGenerator):
    """Apply Brouwer/Banach fixed-point theorem to continuous maps.

    For f:[a,b]->[a,b] continuous, applies the intermediate value
    theorem to g(x) = f(x) - x to show a fixed point must exist.
    Generates polynomial f and verifies g(a) and g(b) have opposite
    signs.

    Difficulty scaling:
        Difficulty 1-3: linear functions f(x) = mx + c on [0,1].
        Difficulty 4-6: quadratic functions on [0, n].
        Difficulty 7-8: cubic functions, larger intervals.

    Prerequisites:
        continuity_topological (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fixed_point_existence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["continuity_topological"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Task description string.
        """
        return "prove fixed point exists using IVT on g(x)=f(x)-x"

    def _eval_poly(self, coeffs: list[float], x: float) -> float:
        """Evaluate polynomial using Horner's method.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Point of evaluation.

        Returns:
            f(x).
        """
        result = 0.0
        for c in coeffs:
            result = result * x + c
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fixed point existence problem.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a_val, b_val = 0, 1
            m = self._rng.randint(1, 8) / 10.0
            c = self._rng.randint(0, 2) / 10.0
            fa = m * a_val + c
            fb = m * b_val + c
            if fb > b_val:
                c = max(0.0, c - (fb - b_val))
                fb = m * b_val + c
                fa = m * a_val + c
            f_str = f"f(x) = {m}x + {c}"
            coeffs = [m, c]
            degree = "linear"
        elif difficulty <= 6:
            a_val = 0
            b_val = self._rng.randint(1, 3)
            aa = self._rng.randint(1, 3) / (10.0 * b_val)
            bb = self._rng.randint(0, 5) / 10.0
            cc = self._rng.randint(0, b_val * 10) / 10.0
            fb_test = aa * b_val ** 2 + bb * b_val + cc
            if fb_test > b_val:
                cc = max(0.0, cc - (fb_test - b_val) - 0.1)
            fa = aa * a_val ** 2 + bb * a_val + cc
            fb = aa * b_val ** 2 + bb * b_val + cc
            fa = max(a_val, min(b_val, fa))
            fb = max(a_val, min(b_val, fb))
            f_str = f"f(x) = {aa}x^2 + {bb}x + {cc}"
            coeffs = [aa, bb, cc]
            degree = "quadratic"
        else:
            a_val = 0
            b_val = self._rng.randint(1, 2)
            aa = self._rng.randint(1, 2) / (10.0 * max(1, b_val ** 2))
            bb = self._rng.randint(-2, 2) / (10.0 * max(1, b_val))
            cc = self._rng.randint(0, 5) / 10.0
            dd = self._rng.randint(0, b_val * 5) / 10.0
            fb_test = aa * b_val ** 3 + bb * b_val ** 2 + cc * b_val + dd
            if fb_test > b_val:
                dd = max(0.0, dd - (fb_test - b_val) - 0.1)
            fa = max(a_val, min(b_val, aa * a_val ** 3 + bb * a_val ** 2 + cc * a_val + dd))
            fb = max(a_val, min(b_val, aa * b_val ** 3 + bb * b_val ** 2 + cc * b_val + dd))
            f_str = f"f(x) = {aa}x^3 + {bb}x^2 + {cc}x + {dd}"
            coeffs = [aa, bb, cc, dd]
            degree = "cubic"

        ga = round(fa - a_val, 4)
        gb = round(fb - b_val, 4)

        problem = (
            f"{f_str}, f:[{a_val},{b_val}]->[{a_val},{b_val}]. "
            f"Show a fixed point exists."
        )
        return problem, {
            "f_str": f_str, "a": a_val, "b": b_val,
            "fa": round(fa, 4), "fb": round(fb, 4),
            "ga": ga, "gb": gb,
            "degree": degree, "coeffs": coeffs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fixed point existence proof steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying IVT to g(x) = f(x) - x.
        """
        a, b = data["a"], data["b"]
        steps = [
            f"define g(x) = f(x) - x",
            f"g({a}) = f({a}) - {a} = {data['fa']} - {a} = {data['ga']}",
            f"g({b}) = f({b}) - {b} = {data['fb']} - {b} = {data['gb']}",
        ]
        if data["ga"] == 0:
            steps.append(f"g({a})=0 so x={a} is a fixed point")
        elif data["gb"] == 0:
            steps.append(f"g({b})=0 so x={b} is a fixed point")
        elif (data["ga"] > 0 and data["gb"] < 0) or (data["ga"] < 0 and data["gb"] > 0):
            steps.append("g(a) and g(b) have opposite signs")
            steps.append("by IVT, exists c in (a,b) with g(c)=0, so f(c)=c")
        else:
            steps.append(f"f:[{a},{b}]->[{a},{b}] is continuous")
            steps.append("by Brouwer fixed-point theorem, a fixed point exists")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Confirmation of fixed point existence.
        """
        if data["ga"] == 0:
            return f"fixed point at x={data['a']}"
        if data["gb"] == 0:
            return f"fixed point at x={data['b']}"
        return "fixed point exists by IVT on g(x)=f(x)-x"
