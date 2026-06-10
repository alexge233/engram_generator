"""Extended spatial reasoning generators.

6 generators across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class Rotation3DGenerator(StepGenerator):
    """Apply a 3D rotation matrix to a point.

    Applies Rx(theta), Ry(theta), or Rz(theta) to a 3D point
    and returns the rotated coordinates.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rotation_3d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply 3D rotation matrix to point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 3D point and rotation, compute the result.

        Args:
            difficulty: Difficulty level controlling coordinate range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 5 * difficulty
        x = self._rng.randint(-r, r)
        y = self._rng.randint(-r, r)
        z = self._rng.randint(-r, r)
        # Pick angle as a multiple of pi/6 for clean values
        angle_idx = self._rng.randint(1, 6)
        theta = angle_idx * math.pi / 6
        theta_label = f"{angle_idx}pi/6"
        axis = self._rng.choice(["x", "y", "z"])
        c = round(math.cos(theta), 4)
        s = round(math.sin(theta), 4)

        if axis == "x":
            rx = round(x, 4)
            ry = round(c * y - s * z, 4)
            rz = round(s * y + c * z, 4)
        elif axis == "y":
            rx = round(c * x + s * z, 4)
            ry = round(y, 4)
            rz = round(-s * x + c * z, 4)
        else:
            rx = round(c * x - s * y, 4)
            ry = round(s * x + c * y, 4)
            rz = round(z, 4)

        problem = (
            f"R{axis}({theta_label}) applied to ({x},{y},{z})?"
        )
        return problem, {
            "axis": axis, "theta": theta_label,
            "point": (x, y, z), "cos": c, "sin": s,
            "result": (rx, ry, rz),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the rotation computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"cos({sd['theta']}) = {sd['cos']}, sin({sd['theta']}) = {sd['sin']}",
            f"apply R{sd['axis']} to {sd['point']}",
            f"result = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rotated point.

        Args:
            sd: Solution data dict.

        Returns:
            Rotated coordinates.
        """
        rx, ry, rz = sd["result"]
        return f"({rx}, {ry}, {rz})"


@register
class VoronoiCellGenerator(StepGenerator):
    """Determine which Voronoi cell a query point falls in.

    Given 3-5 seed points in 2D, finds the nearest seed point to
    the query point (i.e., which Voronoi cell it belongs to).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "voronoi_cell"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["distance_2d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find Voronoi cell for query point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate seed points and a query, find nearest seed.

        Args:
            difficulty: Difficulty level controlling point count and range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n = min(3 + difficulty // 2, 5)
        r = 10 * difficulty
        seeds = [
            (self._rng.randint(-r, r), self._rng.randint(-r, r))
            for _ in range(n)
        ]
        qx = self._rng.randint(-r, r)
        qy = self._rng.randint(-r, r)
        dists = []
        for i, (sx, sy) in enumerate(seeds):
            d = round(math.sqrt((qx - sx) ** 2 + (qy - sy) ** 2), 4)
            dists.append((i, d))
        nearest = min(dists, key=lambda t: t[1])
        seeds_str = " ".join(f"S{i}=({x},{y})" for i, (x, y) in enumerate(seeds))
        problem = f"seeds: {seeds_str}. query ({qx},{qy}). which cell?"
        return problem, {
            "seeds": seeds, "query": (qx, qy),
            "dists": dists, "nearest_idx": nearest[0],
            "nearest_dist": nearest[1],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show distance computations.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = []
        for idx, d in sd["dists"]:
            steps.append(f"d(query, S{idx}) = {d}")
        steps.append(f"nearest: S{sd['nearest_idx']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Voronoi cell index.

        Args:
            sd: Solution data dict.

        Returns:
            Cell identifier.
        """
        return f"S{sd['nearest_idx']} (d={sd['nearest_dist']})"


@register
class DelaunayCheckGenerator(StepGenerator):
    """Check the Delaunay condition for a triangulation of 4 points.

    Verifies that no point lies inside the circumcircle of any
    triangle in the triangulation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "delaunay_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["distance_2d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check Delaunay condition for triangulation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 4 points, form two triangles, check circumcircle.

        Args:
            difficulty: Difficulty level controlling coordinate range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 5 + 3 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(4)]
        # Triangle formed by pts[0], pts[1], pts[2]; check if pts[3] is inside circumcircle
        ax, ay = pts[0]
        bx, by = pts[1]
        cx, cy = pts[2]
        dx, dy = pts[3]
        # Circumcircle test using determinant sign
        # Point d is inside circumcircle of abc if det > 0 (assuming ccw ordering)
        mat_val = (
            (ax - dx) * ((by - dy) * ((cx - dx) ** 2 + (cy - dy) ** 2) -
                         (cy - dy) * ((bx - dx) ** 2 + (by - dy) ** 2))
            - (bx - dx) * ((ay - dy) * ((cx - dx) ** 2 + (cy - dy) ** 2) -
                           (cy - dy) * ((ax - dx) ** 2 + (ay - dy) ** 2))
            + (cx - dx) * ((ay - dy) * ((bx - dx) ** 2 + (by - dy) ** 2) -
                           (by - dy) * ((ax - dx) ** 2 + (ay - dy) ** 2))
        )
        # Check orientation of abc
        orient = ((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))
        if orient < 0:
            mat_val = -mat_val
        inside = mat_val > 0
        is_delaunay = not inside

        pts_str = " ".join(f"P{i}=({x},{y})" for i, (x, y) in enumerate(pts))
        problem = (
            f"points: {pts_str}. triangle P0P1P2. "
            f"is P3 outside circumcircle?"
        )
        return problem, {
            "pts": pts, "det": mat_val, "orient": orient,
            "inside": inside, "is_delaunay": is_delaunay,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show circumcircle determinant test.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"orient(P0,P1,P2) = {sd['orient']}",
            f"circumcircle det = {sd['det']}",
            f"P3 {'inside' if sd['inside'] else 'outside'} circumcircle",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the Delaunay condition holds.

        Args:
            sd: Solution data dict.

        Returns:
            DELAUNAY or NOT DELAUNAY.
        """
        return "DELAUNAY" if sd["is_delaunay"] else "NOT DELAUNAY"


@register
class ConvexHull2DGenerator(StepGenerator):
    """Compute convex hull of 2D points using gift wrapping.

    Lists hull vertices in counterclockwise order using the
    Jarvis march algorithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convex_hull_2d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cross_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute convex hull using gift wrapping"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2D points and compute convex hull.

        Args:
            difficulty: Difficulty level controlling point count.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n = min(4 + difficulty, 8)
        r = 10 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
        # Jarvis march (gift wrapping)
        hull = []
        start = min(range(n), key=lambda i: (pts[i][0], pts[i][1]))
        current = start
        while True:
            hull.append(current)
            candidate = 0
            for j in range(n):
                if j == current:
                    continue
                if candidate == current:
                    candidate = j
                    continue
                # Cross product to determine turn direction
                ox, oy = pts[current]
                ax, ay = pts[candidate]
                bx, by = pts[j]
                cross = (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)
                if cross < 0:
                    candidate = j
                elif cross == 0:
                    # Collinear: pick the farther point
                    da = (ax - ox) ** 2 + (ay - oy) ** 2
                    db = (bx - ox) ** 2 + (by - oy) ** 2
                    if db > da:
                        candidate = j
            current = candidate
            if current == start:
                break
            if len(hull) > n:
                break

        hull_pts = [pts[i] for i in hull]
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        problem = f"points: {pts_str}. convex hull?"
        return problem, {"pts": pts, "hull_indices": hull, "hull_pts": hull_pts}

    def _create_steps(self, sd: dict) -> list[str]:
        """Show gift wrapping steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"start at leftmost point {sd['hull_pts'][0]}"]
        for i in range(1, len(sd["hull_pts"])):
            steps.append(f"wrap to {sd['hull_pts'][i]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the hull vertices.

        Args:
            sd: Solution data dict.

        Returns:
            Hull vertices in order.
        """
        hull_str = " ".join(f"({x},{y})" for x, y in sd["hull_pts"])
        return f"hull: {hull_str}"


@register
class AffineTransformGenerator(StepGenerator):
    """Apply and compose 2D affine transforms.

    Computes [x',y'] = A*[x,y] + t for one or two transforms
    and returns the final result.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "affine_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply 2D affine transform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an affine transform and apply to a 2D point.

        Args:
            difficulty: Difficulty level controlling value range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 3 + difficulty
        # First transform
        a1 = [[self._rng.randint(-r, r) for _ in range(2)] for _ in range(2)]
        t1 = [self._rng.randint(-r, r), self._rng.randint(-r, r)]
        px = self._rng.randint(-r, r)
        py = self._rng.randint(-r, r)

        # Apply first transform
        x1 = a1[0][0] * px + a1[0][1] * py + t1[0]
        y1 = a1[1][0] * px + a1[1][1] * py + t1[1]

        compose = difficulty >= 4
        if compose:
            # Second transform
            a2 = [[self._rng.randint(-r // 2, r // 2) for _ in range(2)] for _ in range(2)]
            t2 = [self._rng.randint(-r, r), self._rng.randint(-r, r)]
            x2 = a2[0][0] * x1 + a2[0][1] * y1 + t2[0]
            y2 = a2[1][0] * x1 + a2[1][1] * y1 + t2[1]
            final = (x2, y2)
            a2_str = f"A2=[{a2[0]},{a2[1]}], t2={t2}"
            problem = (
                f"A1=[{a1[0]},{a1[1]}], t1={t1}; {a2_str}. "
                f"compose on ({px},{py})?"
            )
        else:
            final = (x1, y1)
            problem = (
                f"A=[{a1[0]},{a1[1]}], t={t1}. "
                f"apply to ({px},{py})?"
            )

        return problem, {
            "point": (px, py), "a1": a1, "t1": t1,
            "mid": (x1, y1), "compose": compose,
            "final": final,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show affine transform computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [
            f"A1*p + t1 = ({sd['mid'][0]}, {sd['mid'][1]})",
        ]
        if sd["compose"]:
            steps.append(f"A2*mid + t2 = ({sd['final'][0]}, {sd['final'][1]})")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the transformed point.

        Args:
            sd: Solution data dict.

        Returns:
            Final coordinates.
        """
        return f"({sd['final'][0]}, {sd['final'][1]})"


@register
class ClosestPairGenerator(StepGenerator):
    """Find the closest pair of points in a 2D point set.

    Uses brute force over 4-8 points to find the pair with
    minimum Euclidean distance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "closest_pair"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["distance_2d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find closest pair of points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2D points and find the closest pair.

        Args:
            difficulty: Difficulty level controlling point count and range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n = min(4 + difficulty, 8)
        r = 10 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
        best_d = float("inf")
        best_i = 0
        best_j = 1
        for i in range(n):
            for j in range(i + 1, n):
                d = math.sqrt((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2)
                if d < best_d:
                    best_d = d
                    best_i = i
                    best_j = j
        best_d = round(best_d, 4)
        pts_str = " ".join(f"P{i}=({x},{y})" for i, (x, y) in enumerate(pts))
        problem = f"points: {pts_str}. closest pair?"
        return problem, {
            "pts": pts, "best_i": best_i, "best_j": best_j,
            "best_d": best_d,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show brute force distance comparisons.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        pi = sd["pts"][sd["best_i"]]
        pj = sd["pts"][sd["best_j"]]
        return [
            f"check all {len(sd['pts']) * (len(sd['pts']) - 1) // 2} pairs",
            f"min: P{sd['best_i']}={pi} and P{sd['best_j']}={pj}",
            f"distance = {sd['best_d']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the closest pair and distance.

        Args:
            sd: Solution data dict.

        Returns:
            Closest pair with distance.
        """
        return f"P{sd['best_i']},P{sd['best_j']} d={sd['best_d']}"
