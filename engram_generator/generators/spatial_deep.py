"""Deep spatial reasoning generators.

6 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class LineSegmentIntersectionGenerator(StepGenerator):
    """Check if two line segments intersect using cross product sign test.

    Uses the orientation test: segments P1P2 and P3P4 intersect if and
    only if the orientations of (P1,P2,P3) and (P1,P2,P4) differ, and
    the orientations of (P3,P4,P1) and (P3,P4,P2) differ.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "line_segment_intersection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "check line segment intersection"

    @staticmethod
    def _orient(px: int, py: int, qx: int, qy: int,
                rx: int, ry: int) -> int:
        """Compute orientation of triplet (P, Q, R).

        Args:
            px: P x-coordinate.
            py: P y-coordinate.
            qx: Q x-coordinate.
            qy: Q y-coordinate.
            rx: R x-coordinate.
            ry: R y-coordinate.

        Returns:
            Positive for CCW, negative for CW, 0 for collinear.
        """
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a line segment intersection problem.

        Args:
            difficulty: Controls coordinate range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 5 * difficulty
        p1 = (self._rng.randint(-r, r), self._rng.randint(-r, r))
        p2 = (self._rng.randint(-r, r), self._rng.randint(-r, r))
        p3 = (self._rng.randint(-r, r), self._rng.randint(-r, r))
        p4 = (self._rng.randint(-r, r), self._rng.randint(-r, r))

        d1 = self._orient(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        d2 = self._orient(p1[0], p1[1], p2[0], p2[1], p4[0], p4[1])
        d3 = self._orient(p3[0], p3[1], p4[0], p4[1], p1[0], p1[1])
        d4 = self._orient(p3[0], p3[1], p4[0], p4[1], p2[0], p2[1])

        intersects = False
        if d1 * d2 < 0 and d3 * d4 < 0:
            intersects = True

        problem = (
            f"segments ({p1[0]},{p1[1]})-({p2[0]},{p2[1]}) and "
            f"({p3[0]},{p3[1]})-({p4[0]},{p4[1]}). intersect?"
        )
        return problem, {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4,
            "d1": d1, "d2": d2, "d3": d3, "d4": d4,
            "intersects": intersects,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show orientation tests.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"orient(P1,P2,P3) = {sd['d1']}",
            f"orient(P1,P2,P4) = {sd['d2']}",
            f"orient(P3,P4,P1) = {sd['d3']}",
            f"orient(P3,P4,P2) = {sd['d4']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether segments intersect.

        Args:
            sd: Solution data dict.

        Returns:
            INTERSECT or NO INTERSECT.
        """
        return "INTERSECT" if sd["intersects"] else "NO INTERSECT"


@register
class PointInTriangleGenerator(StepGenerator):
    """Test if a point is inside a triangle using cross product method.

    A point P is inside triangle ABC if the cross products of
    (AB x AP), (BC x BP), and (CA x CP) all have the same sign.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "point_in_triangle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "point in triangle test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a point-in-triangle problem.

        Args:
            difficulty: Controls coordinate range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 5 * difficulty
        ax = self._rng.randint(-r, r)
        ay = self._rng.randint(-r, r)
        bx = self._rng.randint(-r, r)
        by = self._rng.randint(-r, r)
        cx = self._rng.randint(-r, r)
        cy = self._rng.randint(-r, r)

        if self._rng.random() < 0.5:
            t1 = self._rng.uniform(0.05, 0.9)
            t2 = self._rng.uniform(0.05, 1.0 - t1)
            px = round(ax + t1 * (bx - ax) + t2 * (cx - ax))
            py = round(ay + t1 * (by - ay) + t2 * (cy - ay))
        else:
            px = self._rng.randint(-r * 2, r * 2)
            py = self._rng.randint(-r * 2, r * 2)

        c1 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        c2 = (cx - bx) * (py - by) - (cy - by) * (px - bx)
        c3 = (ax - cx) * (py - cy) - (ay - cy) * (px - cx)

        all_pos = c1 >= 0 and c2 >= 0 and c3 >= 0
        all_neg = c1 <= 0 and c2 <= 0 and c3 <= 0
        inside = all_pos or all_neg

        problem = (
            f"triangle A=({ax},{ay}), B=({bx},{by}), C=({cx},{cy}). "
            f"point P=({px},{py}). inside?"
        )
        return problem, {
            "A": (ax, ay), "B": (bx, by), "C": (cx, cy),
            "P": (px, py), "c1": c1, "c2": c2, "c3": c3,
            "inside": inside,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show cross product computations.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"AB x AP = {sd['c1']}",
            f"BC x BP = {sd['c2']}",
            f"CA x CP = {sd['c3']}",
            f"same sign: {sd['inside']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether point is inside triangle.

        Args:
            sd: Solution data dict.

        Returns:
            INSIDE or OUTSIDE.
        """
        return "INSIDE" if sd["inside"] else "OUTSIDE"


@register
class PolygonCentroidGenerator(StepGenerator):
    """Compute the centroid of a simple polygon.

    Uses the formula C = (1/(6A)) * sum((x_i + x_{i+1}) * cross_i)
    where cross_i = x_i*y_{i+1} - x_{i+1}*y_i.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polygon_centroid"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute polygon centroid"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polygon centroid problem.

        Args:
            difficulty: Controls vertex count (4-5).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(4 + difficulty // 4, 5)
        r = 3 * difficulty + 5
        angles = sorted(self._rng.uniform(0, 2 * math.pi) for _ in range(n))
        vertices = [
            (round(r * math.cos(a)), round(r * math.sin(a)))
            for a in angles
        ]

        area_sum = 0.0
        cx_sum = 0.0
        cy_sum = 0.0
        cross_terms: list[str] = []
        for i in range(n):
            j = (i + 1) % n
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            cross = xi * yj - xj * yi
            area_sum += cross
            cx_sum += (xi + xj) * cross
            cy_sum += (yi + yj) * cross
            cross_terms.append(
                f"({xi},{yi})-({xj},{yj}): cross={cross}"
            )

        area = area_sum / 2.0
        if abs(area) < 1e-10:
            area = 1.0
        cx = round(cx_sum / (6 * area), 4)
        cy = round(cy_sum / (6 * area), 4)
        area = round(abs(area), 4)

        verts_str = " ".join(f"({x},{y})" for x, y in vertices)
        problem = f"centroid of polygon {verts_str}"
        return problem, {
            "vertices": vertices, "cross_terms": cross_terms,
            "area": area, "cx": cx, "cy": cy,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show cross product and area computations.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = sd["cross_terms"]
        steps.append(f"area = {sd['area']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the centroid coordinates.

        Args:
            sd: Solution data dict.

        Returns:
            Centroid (cx, cy).
        """
        return f"centroid = ({sd['cx']}, {sd['cy']})"


@register
class MinimumBoundingCircleGenerator(StepGenerator):
    """Find the smallest circle enclosing a set of 2D points.

    Checks whether a 2-point diameter circle suffices, otherwise
    computes the circumscribed circle of 3 points.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "minimum_bounding_circle"

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
        return "find minimum bounding circle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a minimum bounding circle problem.

        Args:
            difficulty: Controls point count (3-5).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(3 + difficulty // 2, 5)
        r = 5 * difficulty
        pts = [
            (self._rng.randint(-r, r), self._rng.randint(-r, r))
            for _ in range(n)
        ]

        best_cx = 0.0
        best_cy = 0.0
        best_r = float("inf")

        for i in range(n):
            for j in range(i + 1, n):
                cx = (pts[i][0] + pts[j][0]) / 2.0
                cy = (pts[i][1] + pts[j][1]) / 2.0
                radius = math.sqrt(
                    (pts[i][0] - pts[j][0]) ** 2 +
                    (pts[i][1] - pts[j][1]) ** 2
                ) / 2.0
                if all(
                    math.sqrt((p[0] - cx) ** 2 + (p[1] - cy) ** 2) <= radius + 1e-9
                    for p in pts
                ):
                    if radius < best_r:
                        best_r = radius
                        best_cx = cx
                        best_cy = cy

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    ax, ay = pts[i]
                    bx, by = pts[j]
                    cx_p, cy_p = pts[k]
                    d = 2 * (ax * (by - cy_p) + bx * (cy_p - ay) + cx_p * (ay - by))
                    if abs(d) < 1e-10:
                        continue
                    ux = ((ax ** 2 + ay ** 2) * (by - cy_p) +
                          (bx ** 2 + by ** 2) * (cy_p - ay) +
                          (cx_p ** 2 + cy_p ** 2) * (ay - by)) / d
                    uy = ((ax ** 2 + ay ** 2) * (cx_p - bx) +
                          (bx ** 2 + by ** 2) * (ax - cx_p) +
                          (cx_p ** 2 + cy_p ** 2) * (bx - ax)) / d
                    radius = math.sqrt((ax - ux) ** 2 + (ay - uy) ** 2)
                    if all(
                        math.sqrt((p[0] - ux) ** 2 + (p[1] - uy) ** 2) <= radius + 1e-9
                        for p in pts
                    ):
                        if radius < best_r:
                            best_r = radius
                            best_cx = ux
                            best_cy = uy

        best_cx = round(best_cx, 4)
        best_cy = round(best_cy, 4)
        best_r = round(best_r, 4)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        problem = f"minimum bounding circle for {pts_str}"
        return problem, {
            "pts": pts, "cx": best_cx, "cy": best_cy,
            "radius": best_r,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the bounding circle computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"check 2-point and 3-point circles",
            f"center = ({sd['cx']}, {sd['cy']})",
            f"radius = {sd['radius']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the bounding circle.

        Args:
            sd: Solution data dict.

        Returns:
            Center and radius.
        """
        return f"center=({sd['cx']},{sd['cy']}), r={sd['radius']}"


@register
class PlaneLineIntersectionGenerator(StepGenerator):
    """Compute the intersection of a line and a plane in 3D.

    Line: P = P0 + t*D. Plane: n dot P = d.
    Intersection at t = (d - n dot P0) / (n dot D).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "plane_line_intersection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dot_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute plane-line intersection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a plane-line intersection problem.

        Args:
            difficulty: Controls coordinate range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + difficulty
        p0 = [self._rng.randint(-r, r) for _ in range(3)]
        d_vec = [self._rng.randint(-r, r) for _ in range(3)]
        while all(v == 0 for v in d_vec):
            d_vec = [self._rng.randint(-r, r) for _ in range(3)]
        n = [self._rng.randint(-r, r) for _ in range(3)]
        while all(v == 0 for v in n):
            n = [self._rng.randint(-r, r) for _ in range(3)]
        d_val = self._rng.randint(-r * 2, r * 2)

        n_dot_d = sum(n[i] * d_vec[i] for i in range(3))
        n_dot_p0 = sum(n[i] * p0[i] for i in range(3))

        if abs(n_dot_d) < 1e-10:
            d_vec[0] = n[0] + 1
            n_dot_d = sum(n[i] * d_vec[i] for i in range(3))

        t = round((d_val - n_dot_p0) / n_dot_d, 4)
        intersection = [round(p0[i] + t * d_vec[i], 4) for i in range(3)]

        problem = (
            f"line P={p0}+t*{d_vec}, plane n={n} dot P={d_val}. "
            f"find intersection"
        )
        return problem, {
            "p0": p0, "d_vec": d_vec, "n": n, "d_val": d_val,
            "n_dot_d": n_dot_d, "n_dot_p0": n_dot_p0,
            "t": t, "intersection": intersection,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show intersection computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"n dot D = {sd['n_dot_d']}",
            f"n dot P0 = {sd['n_dot_p0']}",
            f"t = ({sd['d_val']} - {sd['n_dot_p0']}) / {sd['n_dot_d']} = {sd['t']}",
            f"P = P0 + t*D = {sd['intersection']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the intersection point.

        Args:
            sd: Solution data dict.

        Returns:
            3D intersection coordinates.
        """
        p = sd["intersection"]
        return f"({p[0]}, {p[1]}, {p[2]})"


@register
class SphericalDistanceGenerator(StepGenerator):
    """Compute great circle distance between two points on a sphere.

    Uses d = R * arccos(sin(lat1)*sin(lat2) +
    cos(lat1)*cos(lat2)*cos(dlon)).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spherical_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute great circle distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spherical distance problem.

        Args:
            difficulty: Controls coordinate precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        lat1_deg = self._rng.randint(-80, 80)
        lon1_deg = self._rng.randint(-170, 170)
        lat2_deg = self._rng.randint(-80, 80)
        lon2_deg = self._rng.randint(-170, 170)
        radius = 6371.0

        lat1 = math.radians(lat1_deg)
        lat2 = math.radians(lat2_deg)
        dlon = math.radians(lon2_deg - lon1_deg)

        cos_d = (math.sin(lat1) * math.sin(lat2) +
                 math.cos(lat1) * math.cos(lat2) * math.cos(dlon))
        cos_d = max(-1.0, min(1.0, cos_d))
        dist = round(radius * math.acos(cos_d), 4)

        problem = (
            f"great circle: ({lat1_deg},{lon1_deg}) to "
            f"({lat2_deg},{lon2_deg}), R={radius} km"
        )
        return problem, {
            "lat1": lat1_deg, "lon1": lon1_deg,
            "lat2": lat2_deg, "lon2": lon2_deg,
            "radius": radius, "cos_d": round(cos_d, 4),
            "dist": dist,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show great circle distance computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"convert to radians",
            f"cos(d) = sin({sd['lat1']})*sin({sd['lat2']}) + "
            f"cos({sd['lat1']})*cos({sd['lat2']})*cos({sd['lon2'] - sd['lon1']})",
            f"cos(d) = {sd['cos_d']}",
            f"d = {sd['radius']} * arccos({sd['cos_d']}) = {sd['dist']} km",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the great circle distance.

        Args:
            sd: Solution data dict.

        Returns:
            Distance in km.
        """
        return f"{sd['dist']} km"
