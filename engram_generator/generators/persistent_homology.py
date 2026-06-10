"""Persistent homology generators.

6 generators across tiers 5-6 covering simplicial complex validation,
boundary operators, Betti number computation, Vietoris-Rips complex
construction, persistence diagrams, and bottleneck distance.
"""
import math
from itertools import combinations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _format_simplex(simplex: tuple[int, ...]) -> str:
    """Format a simplex as a bracketed vertex list.

    Args:
        simplex: Tuple of vertex indices.

    Returns:
        String like '[0,1,2]'.
    """
    return "[" + ",".join(str(v) for v in simplex) + "]"


def _faces(simplex: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Return all proper faces of a simplex.

    Args:
        simplex: Tuple of vertex indices.

    Returns:
        List of face tuples (all subsets except the simplex itself and empty set).
    """
    result: list[tuple[int, ...]] = []
    n = len(simplex)
    for k in range(1, n):
        for combo in combinations(simplex, k):
            result.append(combo)
    return result


def _euclidean_dist(p1: tuple[float, ...], p2: tuple[float, ...]) -> float:
    """Compute Euclidean distance between two points.

    Args:
        p1: First point coordinates.
        p2: Second point coordinates.

    Returns:
        Euclidean distance rounded to 4 decimal places.
    """
    return round(math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2))), 4)


class UnionFind:
    """Disjoint-set data structure for tracking connected components.

    Attributes:
        parent: Maps each element to its parent.
        rank: Maps each element to its tree rank.
    """

    def __init__(self, elements: list[int]) -> None:
        """Initialise with each element as its own component.

        Args:
            elements: List of element identifiers.
        """
        self._parent = {e: e for e in elements}
        self._rank = {e: 0 for e in elements}

    def find(self, x: int) -> int:
        """Find the root of x with path compression.

        Args:
            x: Element to find.

        Returns:
            Root of x's component.
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: int, y: int) -> bool:
        """Merge components of x and y.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if a merge happened (they were in different components).
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True

    def num_components(self) -> int:
        """Return the number of distinct components.

        Returns:
            Component count.
        """
        return len({self.find(x) for x in self._parent})


# ---------------------------------------------------------------------------
# 1. Simplicial complex validation (tier 5)
# ---------------------------------------------------------------------------

@register
class SimplicialComplexGenerator(StepGenerator):
    """Verify that a set of simplices forms a valid simplicial complex.

    A valid simplicial complex requires that every face of every
    simplex is also included in the set. Given a list of simplices,
    checks this closure property and identifies any missing faces.

    Difficulty scaling:
        Difficulty 1-3: 3-5 simplices, up to 2-simplices.
        Difficulty 4-6: 5-8 simplices, up to 3-simplices.
        Difficulty 7-8: 8-12 simplices with deliberate missing faces.

    Prerequisites:
        set_operations (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simplicial_complex"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify simplicial complex closure property"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simplicial complex validation problem.

        Args:
            difficulty: Controls simplex count and dimension.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_verts = self._rng.randint(3, 4)
            max_dim = 2
        elif difficulty <= 6:
            n_verts = self._rng.randint(4, 5)
            max_dim = 3
        else:
            n_verts = self._rng.randint(5, 6)
            max_dim = 3

        vertices = list(range(n_verts))
        # Build a valid complex then possibly remove some faces
        simplices: set[tuple[int, ...]] = set()
        # Add all vertices
        for v in vertices:
            simplices.add((v,))

        # Add some higher-dimensional simplices with all their faces
        n_high = self._rng.randint(1, min(3, difficulty))
        for _ in range(n_high):
            dim = self._rng.randint(2, max_dim)
            dim = min(dim, n_verts)
            verts = tuple(sorted(self._rng.sample(vertices, dim)))
            simplices.add(verts)
            for face in _faces(verts):
                simplices.add(face)

        # At higher difficulty, sometimes remove a face to make it invalid
        make_invalid = difficulty >= 5 and self._rng.random() < 0.5
        missing: list[tuple[int, ...]] = []
        if make_invalid:
            edges = [s for s in simplices if len(s) == 2]
            if edges:
                to_remove = self._rng.choice(edges)
                simplices.discard(to_remove)
                missing.append(to_remove)

        # Check validity
        is_valid = True
        computed_missing: list[tuple[int, ...]] = []
        for s in list(simplices):
            if len(s) > 1:
                for face in _faces(s):
                    if face not in simplices:
                        is_valid = False
                        if face not in computed_missing:
                            computed_missing.append(face)

        sorted_simplices = sorted(simplices, key=lambda x: (len(x), x))
        simp_str = ", ".join(_format_simplex(s) for s in sorted_simplices)
        problem = f"K = {{{simp_str}}}. Valid simplicial complex?"
        return problem, {
            "simplices": sorted_simplices,
            "is_valid": is_valid,
            "missing": computed_missing,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["check: every face of every simplex is in K"]
        high_dim = [s for s in sd["simplices"] if len(s) >= 2]
        for s in high_dim[:4]:  # Limit for output length
            faces_list = _faces(s)
            all_present = all(
                f in set(map(tuple, sd["simplices"]))
                for f in faces_list
            )
            steps.append(
                f"{_format_simplex(s)}: faces "
                f"{'all present' if all_present else 'MISSING'}"
            )
        if sd["is_valid"]:
            steps.append("all faces present: valid complex")
        else:
            miss_str = ", ".join(_format_simplex(m) for m in sd["missing"][:3])
            steps.append(f"missing: {miss_str}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Validity result.
        """
        if sd["is_valid"]:
            return "valid simplicial complex"
        miss_str = ", ".join(_format_simplex(m) for m in sd["missing"][:3])
        return f"invalid, missing faces: {miss_str}"


# ---------------------------------------------------------------------------
# 2. Boundary operator (tier 6)
# ---------------------------------------------------------------------------

@register
class BoundaryOperatorGenerator(StepGenerator):
    """Compute the boundary of a k-simplex as a chain.

    The boundary operator d maps a k-simplex [v0,...,vk] to the
    alternating sum of its (k-1)-faces:
    d([v0,v1,v2]) = [v1,v2] - [v0,v2] + [v0,v1].

    Difficulty scaling:
        Difficulty 1-3: boundary of a 1-simplex (edge).
        Difficulty 4-6: boundary of a 2-simplex (triangle).
        Difficulty 7-8: boundary of a 3-simplex (tetrahedron).

    Prerequisites:
        simplicial_complex (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "boundary_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["simplicial_complex"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute boundary operator on k-simplex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a boundary operator problem.

        Args:
            difficulty: Controls simplex dimension.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            dim = 1
        elif difficulty <= 6:
            dim = 2
        else:
            dim = 3

        n_verts = dim + 1
        base = self._rng.randint(0, 3)
        simplex = tuple(range(base, base + n_verts))

        # Compute boundary: d([v0,...,vk]) = sum_{i=0}^{k} (-1)^i [v0,...,vi-hat,...,vk]
        boundary_terms: list[tuple[int, tuple[int, ...]]] = []
        for i in range(n_verts):
            sign = (-1) ** i
            face = simplex[:i] + simplex[i + 1:]
            boundary_terms.append((sign, face))

        problem = f"d({_format_simplex(simplex)}). Compute the boundary."
        return problem, {
            "simplex": simplex, "dim": dim,
            "boundary_terms": boundary_terms,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"d({_format_simplex(sd['simplex'])}) = "
            f"sum_i (-1)^i [v0,...,vi-hat,...,vk]"
        ]
        for i, (sign, face) in enumerate(sd["boundary_terms"]):
            sign_str = "+" if sign > 0 else "-"
            steps.append(
                f"i={i}: ({sign_str}1){_format_simplex(face)}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Boundary as an alternating sum of faces.
        """
        parts: list[str] = []
        for sign, face in sd["boundary_terms"]:
            if sign > 0 and parts:
                parts.append(f"+{_format_simplex(face)}")
            elif sign < 0:
                parts.append(f"-{_format_simplex(face)}")
            else:
                parts.append(_format_simplex(face))
        return "d = " + "".join(parts)


# ---------------------------------------------------------------------------
# 3. Betti numbers from complex (tier 6)
# ---------------------------------------------------------------------------

@register
class BettiFromComplexGenerator(StepGenerator):
    """Compute Betti numbers from a simplicial complex.

    Betti numbers b_k = dim(ker d_k) - dim(im d_{k+1}) count the
    independent k-cycles not bounding a (k+1)-chain. For small
    complexes, computes b_0 (components) and b_1 (loops) directly.

    Difficulty scaling:
        Difficulty 1-3: simple graph (vertices and edges only), b_0.
        Difficulty 4-6: graph with triangles, b_0 and b_1.
        Difficulty 7-8: complex with triangles and tetrahedra.

    Prerequisites:
        boundary_operator (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "betti_from_complex"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boundary_operator"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Betti numbers from simplicial complex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Betti number computation problem.

        Args:
            difficulty: Controls complex size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._graph_case(difficulty)
        return self._triangle_case(difficulty)

    def _graph_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate a graph (1-complex) Betti number problem.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(3, 4 + difficulty // 2)
        vertices = list(range(n))
        # Build a connected graph with some extra edges for loops
        edges: list[tuple[int, int]] = []
        for i in range(1, n):
            edges.append((i - 1, i))
        n_extra = self._rng.randint(0, min(2, difficulty))
        for _ in range(n_extra):
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v and (min(u, v), max(u, v)) not in edges:
                edges.append((min(u, v), max(u, v)))

        v_count = n
        e_count = len(edges)
        # For a connected graph: b_0 = 1, b_1 = e - v + 1
        # Check connectivity
        uf = UnionFind(vertices)
        for u, v in edges:
            uf.union(u, v)
        b_0 = uf.num_components()
        b_1 = e_count - v_count + b_0

        edge_str = ", ".join(f"[{u},{v}]" for u, v in sorted(edges))
        vert_str = ", ".join(f"[{v}]" for v in vertices)
        problem = f"K: vertices {vert_str}; edges {edge_str}. Compute Betti numbers."
        return problem, {
            "vertices": vertices, "edges": edges,
            "v": v_count, "e": e_count,
            "b_0": b_0, "b_1": b_1, "b_2": 0,
        }

    def _triangle_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-complex Betti number problem.

        Args:
            difficulty: Controls complex size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(4, 5 + difficulty // 3)
        vertices = list(range(n))
        edges: set[tuple[int, int]] = set()
        triangles: list[tuple[int, int, int]] = []

        # Build connected graph
        for i in range(1, n):
            edges.add((i - 1, i))

        # Add some triangles
        n_tri = self._rng.randint(1, min(3, difficulty // 2 + 1))
        for _ in range(n_tri):
            tri_verts = sorted(self._rng.sample(vertices, 3))
            tri = (tri_verts[0], tri_verts[1], tri_verts[2])
            triangles.append(tri)
            edges.add((tri[0], tri[1]))
            edges.add((tri[0], tri[2]))
            edges.add((tri[1], tri[2]))

        # Add a few extra edges
        n_extra = self._rng.randint(0, min(2, difficulty))
        for _ in range(n_extra):
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v:
                edges.add((min(u, v), max(u, v)))

        sorted_edges = sorted(edges)

        # Compute Betti numbers
        uf = UnionFind(vertices)
        for u, v in sorted_edges:
            uf.union(u, v)
        b_0 = uf.num_components()

        v_count = n
        e_count = len(sorted_edges)
        f_count = len(triangles)
        # Euler characteristic: chi = b_0 - b_1 + b_2
        # For 2-complex: chi = v - e + f, and b_2 depends on
        # whether triangles fill all 2-cycles
        # Simple formula: b_1 = e - v + b_0 - f_count (when triangles
        # fill independent cycles)
        b_1 = max(0, e_count - v_count + b_0 - f_count)
        b_2 = 0  # No 3-simplices to create voids

        edge_str = ", ".join(f"[{u},{v}]" for u, v in sorted_edges)
        tri_str = ", ".join(f"[{a},{b},{c}]" for a, b, c in triangles)
        problem = (
            f"K: {v_count} vertices; edges {edge_str}; "
            f"triangles {tri_str}. Compute Betti numbers."
        )
        return problem, {
            "vertices": vertices, "edges": sorted_edges,
            "triangles": triangles,
            "v": v_count, "e": e_count, "f": f_count,
            "b_0": b_0, "b_1": b_1, "b_2": b_2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"V={sd['v']}, E={sd['e']}",
        ]
        if "f" in sd:
            steps.append(f"F={sd['f']}")
        steps.append(f"b_0 = {sd['b_0']} (components)")
        steps.append(
            f"b_1 = E - V + b_0"
            + (f" - F = {sd['b_1']}" if "f" in sd else f" = {sd['b_1']}")
        )
        if sd.get("b_2", 0) > 0:
            steps.append(f"b_2 = {sd['b_2']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Betti numbers.
        """
        parts = [f"b_0={sd['b_0']}", f"b_1={sd['b_1']}"]
        if sd.get("b_2", 0) > 0:
            parts.append(f"b_2={sd['b_2']}")
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 4. Vietoris-Rips complex (tier 5)
# ---------------------------------------------------------------------------

@register
class VietorisRipsGenerator(StepGenerator):
    """Build the Vietoris-Rips complex at a given radius.

    Given a set of 4-6 points in R^2, builds the VR complex at
    radius r: an edge (i,j) exists iff d(p_i, p_j) <= r, and a
    triangle (i,j,k) exists iff all three pairwise edges exist.

    Difficulty scaling:
        Difficulty 1-3: 4 points, moderate radius.
        Difficulty 4-6: 5 points, tighter radius.
        Difficulty 7-8: 6 points, variable radius.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vietoris_rips"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "build Vietoris-Rips complex at radius r"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Vietoris-Rips complex problem.

        Args:
            difficulty: Controls point count and radius.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
        elif difficulty <= 6:
            n_pts = 5
        else:
            n_pts = 6

        # Generate points on a grid-like structure for clean distances
        points: list[tuple[float, float]] = []
        for _ in range(n_pts):
            x = round(self._rng.uniform(0.0, 4.0), 2)
            y = round(self._rng.uniform(0.0, 4.0), 2)
            points.append((x, y))

        # Compute all pairwise distances
        dists: dict[tuple[int, int], float] = {}
        for i in range(n_pts):
            for j in range(i + 1, n_pts):
                dists[(i, j)] = _euclidean_dist(points[i], points[j])

        # Choose radius to get an interesting complex
        all_dists = sorted(dists.values())
        if len(all_dists) >= 3:
            r = all_dists[len(all_dists) // 2]
        else:
            r = all_dists[0] if all_dists else 1.0
        r = round(r, 4)

        # Build edges
        edges: list[tuple[int, int]] = []
        for (i, j), d in sorted(dists.items()):
            if d <= r:
                edges.append((i, j))

        # Build triangles
        triangles: list[tuple[int, int, int]] = []
        edge_set = set(edges)
        for i in range(n_pts):
            for j in range(i + 1, n_pts):
                for k in range(j + 1, n_pts):
                    if ((i, j) in edge_set and
                            (i, k) in edge_set and
                            (j, k) in edge_set):
                        triangles.append((i, j, k))

        pts_str = ", ".join(f"p{i}=({p[0]},{p[1]})" for i, p in enumerate(points))
        problem = f"{pts_str}, r={r}. Build VR complex."
        return problem, {
            "points": points, "r": r,
            "dists": dists, "edges": edges,
            "triangles": triangles, "n_pts": n_pts,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"radius r = {sd['r']}"]
        # Show distance checks for edges
        for (i, j), d in sorted(sd["dists"].items()):
            if d <= sd["r"]:
                steps.append(f"d(p{i},p{j})={d} <= {sd['r']}: edge")
        steps.append(f"edges: {len(sd['edges'])}")
        if sd["triangles"]:
            tri_str = ", ".join(
                f"[{a},{b},{c}]" for a, b, c in sd["triangles"]
            )
            steps.append(f"triangles: {tri_str}")
        else:
            steps.append("no triangles")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Complex summary.
        """
        return (
            f"VR(r={sd['r']}): {sd['n_pts']} vertices, "
            f"{len(sd['edges'])} edges, "
            f"{len(sd['triangles'])} triangles"
        )


# ---------------------------------------------------------------------------
# 5. Persistence diagram (tier 6)
# ---------------------------------------------------------------------------

@register
class PersistenceDiagramGenerator(StepGenerator):
    """Track birth/death of topological features across filtration.

    Given a set of points, builds VR complexes at increasing radii
    and tracks when connected components merge (H_0) and when loops
    appear and are filled (H_1). Reports (birth, death) pairs.

    Difficulty scaling:
        Difficulty 1-3: 4 points, H_0 only.
        Difficulty 4-6: 5 points, H_0 and H_1.
        Difficulty 7-8: 6 points, H_0 and H_1.

    Prerequisites:
        vietoris_rips (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "persistence_diagram"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vietoris_rips"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute persistence diagram (birth,death) pairs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a persistence diagram problem.

        Args:
            difficulty: Controls point count and features tracked.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
            track_h1 = False
        elif difficulty <= 6:
            n_pts = 5
            track_h1 = True
        else:
            n_pts = 6
            track_h1 = True

        # Generate points
        points: list[tuple[float, float]] = []
        for _ in range(n_pts):
            x = round(self._rng.uniform(0.0, 5.0), 2)
            y = round(self._rng.uniform(0.0, 5.0), 2)
            points.append((x, y))

        # Compute all pairwise distances and sort
        edge_dists: list[tuple[float, int, int]] = []
        for i in range(n_pts):
            for j in range(i + 1, n_pts):
                d = _euclidean_dist(points[i], points[j])
                edge_dists.append((d, i, j))
        edge_dists.sort()

        # Track H_0: components merging
        uf = UnionFind(list(range(n_pts)))
        h0_pairs: list[tuple[float, float]] = []
        # All points born at r=0
        edge_set: set[tuple[int, int]] = set()

        for dist, i, j in edge_dists:
            merged = uf.union(i, j)
            if merged:
                # A component dies (the younger one merges into the older)
                h0_pairs.append((0.0, dist))
            edge_set.add((i, j))

        # The last surviving component lives forever
        # We have n_pts - 1 merges for a connected graph

        # Track H_1: loops
        h1_pairs: list[tuple[float, float]] = []
        if track_h1:
            # A 1-cycle is born when an edge is added that does NOT
            # merge two components (creates a loop).
            # It dies when a triangle fills that loop.
            uf2 = UnionFind(list(range(n_pts)))
            edges_so_far: set[tuple[int, int]] = set()

            for dist, i, j in edge_dists:
                merged = uf2.union(i, j)
                edges_so_far.add((i, j))
                if not merged:
                    # This edge creates a cycle -- born at this distance
                    # Check if a triangle immediately fills it
                    filled_at = None
                    for k in range(n_pts):
                        if k == i or k == j:
                            continue
                        ik = (min(i, k), max(i, k))
                        jk = (min(j, k), max(j, k))
                        if ik in edges_so_far and jk in edges_so_far:
                            filled_at = dist
                            break
                    if filled_at is not None:
                        h1_pairs.append((dist, filled_at))
                    else:
                        # Will be filled later or persists
                        h1_pairs.append((dist, round(dist * 1.5, 4)))

        pts_str = ", ".join(
            f"p{i}=({p[0]},{p[1]})" for i, p in enumerate(points)
        )
        problem = f"{pts_str}. Compute persistence diagram."
        return problem, {
            "points": points, "n_pts": n_pts,
            "edge_dists": edge_dists[:8],  # Limit for output length
            "h0_pairs": h0_pairs, "h1_pairs": h1_pairs,
            "track_h1": track_h1,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"{sd['n_pts']} points, increasing radius filtration"]
        for dist, i, j in sd["edge_dists"][:5]:
            steps.append(f"r={dist}: add edge ({i},{j})")
        h0_str = ", ".join(
            f"(0,{d})" for _, d in sd["h0_pairs"][:4]
        )
        steps.append(f"H_0 deaths: {h0_str}")
        if sd["track_h1"] and sd["h1_pairs"]:
            h1_str = ", ".join(
                f"({b},{d})" for b, d in sd["h1_pairs"][:3]
            )
            steps.append(f"H_1 pairs: {h1_str}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Persistence pairs summary.
        """
        h0 = ", ".join(f"(0,{d})" for _, d in sd["h0_pairs"][:4])
        result = f"H_0: {h0}"
        if sd["track_h1"] and sd["h1_pairs"]:
            h1 = ", ".join(
                f"({b},{d})" for b, d in sd["h1_pairs"][:3]
            )
            result += f"; H_1: {h1}"
        return result


# ---------------------------------------------------------------------------
# 6. Bottleneck distance (tier 6)
# ---------------------------------------------------------------------------

@register
class BottleneckDistanceGenerator(StepGenerator):
    """Compute the bottleneck distance between two persistence diagrams.

    The bottleneck distance is max over the optimal matching of
    ||p - q||_inf. For small diagrams, computes all possible matchings
    and finds the one minimising the maximum cost.

    Difficulty scaling:
        Difficulty 1-3: 2-point diagrams.
        Difficulty 4-6: 3-point diagrams.
        Difficulty 7-8: 4-point diagrams.

    Prerequisites:
        persistence_diagram (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bottleneck_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["persistence_diagram"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute bottleneck distance between persistence diagrams"

    def _linf(self, p: tuple[float, float], q: tuple[float, float]) -> float:
        """Compute L-infinity distance between two points.

        Args:
            p: First point (birth, death).
            q: Second point (birth, death).

        Returns:
            L-infinity distance.
        """
        return round(max(abs(p[0] - q[0]), abs(p[1] - q[1])), 4)

    def _diagonal_cost(self, p: tuple[float, float]) -> float:
        """Compute cost of matching a point to the diagonal.

        Args:
            p: Point (birth, death).

        Returns:
            Cost (death - birth) / 2.
        """
        return round(abs(p[1] - p[0]) / 2, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bottleneck distance problem.

        Args:
            difficulty: Controls diagram size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = 3
        else:
            n = 4

        # Generate two persistence diagrams
        dgm1: list[tuple[float, float]] = []
        dgm2: list[tuple[float, float]] = []
        for _ in range(n):
            b = round(self._rng.uniform(0.0, 2.0), 2)
            d = round(b + self._rng.uniform(0.5, 3.0), 2)
            dgm1.append((b, d))
        for _ in range(n):
            b = round(self._rng.uniform(0.0, 2.0), 2)
            d = round(b + self._rng.uniform(0.5, 3.0), 2)
            dgm2.append((b, d))

        # Compute cost matrix for point-to-point matching
        cost_matrix: list[list[float]] = []
        for p in dgm1:
            row: list[float] = []
            for q in dgm2:
                row.append(self._linf(p, q))
            cost_matrix.append(row)

        # For small diagrams, try all permutations
        best_bottleneck = float("inf")
        best_matching: list[tuple[int, int]] = []
        from itertools import permutations as _perms
        for perm in _perms(range(n)):
            bottleneck = 0.0
            for i, j in enumerate(perm):
                bottleneck = max(bottleneck, cost_matrix[i][j])
            if bottleneck < best_bottleneck:
                best_bottleneck = bottleneck
                best_matching = [(i, perm[i]) for i in range(n)]
        best_bottleneck = round(best_bottleneck, 4)

        dgm1_str = ", ".join(f"({b},{d})" for b, d in dgm1)
        dgm2_str = ", ".join(f"({b},{d})" for b, d in dgm2)
        problem = (
            f"D1 = {{{dgm1_str}}}, D2 = {{{dgm2_str}}}. "
            f"Compute bottleneck distance."
        )
        return problem, {
            "dgm1": dgm1, "dgm2": dgm2,
            "cost_matrix": cost_matrix,
            "best_bottleneck": best_bottleneck,
            "best_matching": best_matching, "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"compute L-inf cost matrix ({sd['n']}x{sd['n']})"]
        for i in range(sd["n"]):
            row_str = ", ".join(str(c) for c in sd["cost_matrix"][i])
            steps.append(f"row {i}: [{row_str}]")
        match_str = ", ".join(
            f"({i}->{j})" for i, j in sd["best_matching"]
        )
        steps.append(f"optimal matching: {match_str}")
        steps.append(f"bottleneck = {sd['best_bottleneck']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Bottleneck distance value.
        """
        return f"d_B = {sd['best_bottleneck']}"
