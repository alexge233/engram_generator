"""Computer graphics task generators.

8 generators across tiers 5-6 covering 3D matrix transforms, perspective
projection, ray-sphere intersection, barycentric coordinates, Bezier
curves, Phong shading, frustum culling, and quaternion rotation.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _f(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ===================================================================
# 1. 3D Matrix Transform (tier 5)
# ===================================================================

@register
class MatrixTransform3dGenerator(StepGenerator):
    """Apply a 3D rotation/scaling/translation matrix to point [x,y,z,1].

    Generates a 4x4 affine transform matrix (combination of scaling and
    translation) and multiplies it by a homogeneous point vector.

    Difficulty scaling:
        Difficulty 1-3: translation only, integer values.
        Difficulty 4-6: scaling + translation, small decimals.
        Difficulty 7-8: rotation (90-degree increments) + scaling + translation.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matrix_transform_3d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply 3D affine transform matrix to a point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 4x4 transform matrix and a 3D point.

        Args:
            difficulty: Controls transform complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        px = round(self._rng.uniform(-5, 5), 2)
        py = round(self._rng.uniform(-5, 5), 2)
        pz = round(self._rng.uniform(-5, 5), 2)
        point = [px, py, pz, 1.0]

        if difficulty <= 3:
            tx = self._rng.randint(-10, 10)
            ty = self._rng.randint(-10, 10)
            tz = self._rng.randint(-10, 10)
            mat = [
                [1, 0, 0, tx],
                [0, 1, 0, ty],
                [0, 0, 1, tz],
                [0, 0, 0, 1],
            ]
            mode = "translate"
        elif difficulty <= 6:
            sx = round(self._rng.uniform(0.5, 3.0), 2)
            sy = round(self._rng.uniform(0.5, 3.0), 2)
            sz = round(self._rng.uniform(0.5, 3.0), 2)
            tx = round(self._rng.uniform(-5, 5), 2)
            ty = round(self._rng.uniform(-5, 5), 2)
            tz = round(self._rng.uniform(-5, 5), 2)
            mat = [
                [sx, 0, 0, tx],
                [0, sy, 0, ty],
                [0, 0, sz, tz],
                [0, 0, 0, 1],
            ]
            mode = "scale+translate"
        else:
            # 90-degree rotation about Z axis
            angle = self._rng.choice([0, 90, 180, 270])
            rad = math.radians(angle)
            c = round(math.cos(rad), 4)
            s = round(math.sin(rad), 4)
            sx = round(self._rng.uniform(0.5, 2.0), 2)
            sy = round(self._rng.uniform(0.5, 2.0), 2)
            sz = round(self._rng.uniform(0.5, 2.0), 2)
            tx = round(self._rng.uniform(-3, 3), 2)
            ty = round(self._rng.uniform(-3, 3), 2)
            tz = round(self._rng.uniform(-3, 3), 2)
            mat = [
                [round(c * sx, 4), round(-s * sy, 4), 0, tx],
                [round(s * sx, 4), round(c * sy, 4), 0, ty],
                [0, 0, sz, tz],
                [0, 0, 0, 1],
            ]
            mode = "rotate+scale+translate"

        result = []
        for row in mat:
            val = sum(row[j] * point[j] for j in range(4))
            result.append(round(val, 4))

        return "P' = M \\cdot P", {
            "point": point,
            "mat": mat,
            "result": result,
            "mode": mode,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matrix-vector multiplication steps.

        Args:
            data: Solution data with matrix, point, and result.

        Returns:
            List of step strings.
        """
        p = data["point"]
        steps = [
            f"P = [{_f(p[0])}, {_f(p[1])}, {_f(p[2])}, 1]",
            f"mode: {data['mode']}",
        ]
        labels = ["x'", "y'", "z'", "w'"]
        for i in range(3):
            row = data["mat"][i]
            steps.append(
                f"{labels[i]} = {_f(row[0])}*{_f(p[0])} + {_f(row[1])}*{_f(p[1])}"
                f" + {_f(row[2])}*{_f(p[2])} + {_f(row[3])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transformed point.

        Args:
            data: Solution data.

        Returns:
            Transformed coordinates as a string.
        """
        r = data["result"]
        return f"P' = [{_f(r[0])}, {_f(r[1])}, {_f(r[2])}]"


# ===================================================================
# 2. Perspective Projection (tier 5)
# ===================================================================

@register
class PerspectiveProjectionGenerator(StepGenerator):
    """Project a 3D point to 2D: x' = f*x/z, y' = f*y/z.

    Given a 3D point (x, y, z) and focal length f, compute the
    perspective-projected 2D coordinates.

    Difficulty scaling:
        Difficulty 1-3: integer coordinates, z > 0.
        Difficulty 4-6: decimal coordinates, varied focal lengths.
        Difficulty 7-8: near-plane clipping check, solve for z given x'.

    Prerequisites:
        matrix_transform_3d.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "perspective_projection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_transform_3d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute perspective projection of a 3D point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 3D point and focal length for projection.

        Args:
            difficulty: Controls coordinate ranges and variants.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            x = self._rng.randint(-10, 10)
            y = self._rng.randint(-10, 10)
            z = self._rng.randint(1, 20)
            f = self._rng.randint(1, 5)
        elif difficulty <= 6:
            x = round(self._rng.uniform(-10, 10), 2)
            y = round(self._rng.uniform(-10, 10), 2)
            z = round(self._rng.uniform(0.5, 30), 2)
            f = round(self._rng.uniform(0.5, 10), 2)
        else:
            x = round(self._rng.uniform(-20, 20), 2)
            y = round(self._rng.uniform(-20, 20), 2)
            z = round(self._rng.uniform(0.1, 50), 2)
            f = round(self._rng.uniform(1, 15), 2)

        x_proj = round(f * x / z, 4)
        y_proj = round(f * y / z, 4)

        near = round(self._rng.uniform(0.1, 1.0), 2) if difficulty >= 7 else 0.1
        visible = z >= near

        return "x' = \\frac{f \\cdot x}{z}, \\quad y' = \\frac{f \\cdot y}{z}", {
            "x": x, "y": y, "z": z, "f": f,
            "x_proj": x_proj, "y_proj": y_proj,
            "near": near, "visible": visible,
            "check_clip": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate perspective projection steps.

        Args:
            data: Solution data with coordinates and focal length.

        Returns:
            List of step strings.
        """
        steps = [
            f"point = ({_f(data['x'])}, {_f(data['y'])}, {_f(data['z'])}), f = {_f(data['f'])}",
            f"x' = {_f(data['f'])}*{_f(data['x'])}/{_f(data['z'])} = {_f(data['x_proj'])}",
            f"y' = {_f(data['f'])}*{_f(data['y'])}/{_f(data['z'])} = {_f(data['y_proj'])}",
        ]
        if data["check_clip"]:
            steps.append(f"near={_f(data['near'])}, z={_f(data['z'])}, visible={data['visible']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the projected 2D point.

        Args:
            data: Solution data.

        Returns:
            Projected coordinates as a string.
        """
        return f"({_f(data['x_proj'])}, {_f(data['y_proj'])})"


# ===================================================================
# 3. Ray-Sphere Intersection (tier 5)
# ===================================================================

@register
class RaySphereIntersectGenerator(StepGenerator):
    """Solve |O + tD - C|^2 = r^2 for t using the quadratic formula.

    Expands to at^2 + bt + c = 0 where a = D.D, b = 2*D.(O-C),
    c = (O-C).(O-C) - r^2. Discriminant determines hit or miss.

    Difficulty scaling:
        Difficulty 1-3: 2D (x,y), small integer coords, guaranteed hit.
        Difficulty 4-6: 3D, decimal coords, may miss.
        Difficulty 7-8: 3D, find nearest intersection point coordinates.

    Prerequisites:
        quadratic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ray_sphere_intersect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find ray-sphere intersection"

    def _dot(self, a: list[float], b: list[float]) -> float:
        """Compute dot product of two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Dot product rounded to 4 dp.
        """
        return round(sum(ai * bi for ai, bi in zip(a, b)), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate ray origin, direction, sphere center, and radius.

        Args:
            difficulty: Controls dimensionality and coordinate range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            dim = 2
            o = [float(self._rng.randint(-3, 3)) for _ in range(dim)]
            d = [float(self._rng.randint(1, 3)) for _ in range(dim)]
            c = [float(self._rng.randint(-2, 5)) for _ in range(dim)]
            r = float(self._rng.randint(2, 5))
        else:
            dim = 3
            o = [round(self._rng.uniform(-5, 5), 2) for _ in range(dim)]
            d = [round(self._rng.uniform(-3, 3), 2) for _ in range(dim)]
            if all(v == 0 for v in d):
                d[0] = 1.0
            c = [round(self._rng.uniform(-5, 5), 2) for _ in range(dim)]
            r = round(self._rng.uniform(1, 5), 2)

        oc = [round(o[i] - c[i], 4) for i in range(dim)]
        a_coeff = self._dot(d, d)
        b_coeff = round(2.0 * self._dot(d, oc), 4)
        c_coeff = round(self._dot(oc, oc) - r * r, 4)
        disc = round(b_coeff * b_coeff - 4 * a_coeff * c_coeff, 4)

        hit = disc >= 0
        t1 = None
        t2 = None
        if hit:
            sqrt_disc = round(math.sqrt(disc), 4)
            t1 = round((-b_coeff - sqrt_disc) / (2 * a_coeff), 4)
            t2 = round((-b_coeff + sqrt_disc) / (2 * a_coeff), 4)

        return "|O + tD - C|^2 = r^2", {
            "O": o, "D": d, "C": c, "r": r, "dim": dim,
            "oc": oc, "a": a_coeff, "b": b_coeff, "c": c_coeff,
            "disc": disc, "hit": hit, "t1": t1, "t2": t2,
            "find_point": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ray-sphere intersection steps.

        Args:
            data: Solution data with ray, sphere, and quadratic coefficients.

        Returns:
            List of step strings.
        """
        steps = [
            f"O-C = {data['oc']}",
            f"a = D.D = {_f(data['a'])}",
            f"b = 2*D.(O-C) = {_f(data['b'])}",
            f"c = |O-C|^2 - r^2 = {_f(data['c'])}",
            f"disc = b^2 - 4ac = {_f(data['disc'])}",
        ]
        if data["hit"]:
            steps.append(f"t1 = {_f(data['t1'])}, t2 = {_f(data['t2'])}")
        else:
            steps.append("disc < 0: no intersection")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the intersection result.

        Args:
            data: Solution data.

        Returns:
            Hit/miss result with t values.
        """
        if not data["hit"]:
            return "miss"
        if data["find_point"] and data["t1"] is not None:
            t = data["t1"] if data["t1"] >= 0 else data["t2"]
            pt = [round(data["O"][i] + t * data["D"][i], 4)
                  for i in range(data["dim"])]
            pt_str = ", ".join(_f(v) for v in pt)
            return f"hit at t = {_f(t)}, P = ({pt_str})"
        return f"hit: t1 = {_f(data['t1'])}, t2 = {_f(data['t2'])}"


# ===================================================================
# 4. Barycentric Coordinates (tier 5)
# ===================================================================

@register
class BarycentricCoordsGenerator(StepGenerator):
    """Compute barycentric coordinates (u, v, w) for point P in triangle ABC.

    Uses the area method: u = area(PBC)/area(ABC), v = area(APC)/area(ABC),
    w = 1 - u - v. Constraint: u + v + w = 1.

    Difficulty scaling:
        Difficulty 1-3: integer vertices, P is centroid.
        Difficulty 4-6: decimal vertices, P inside triangle.
        Difficulty 7-8: P may be outside triangle (negative coordinates).

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "barycentric_coords"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute barycentric coordinates of a point in a triangle"

    def _tri_area_2d(self, a: list[float], b: list[float],
                     c: list[float]) -> float:
        """Compute signed area of triangle via cross product.

        Args:
            a: First vertex [x, y].
            b: Second vertex [x, y].
            c: Third vertex [x, y].

        Returns:
            Signed area (positive if CCW).
        """
        return round(
            0.5 * ((b[0] - a[0]) * (c[1] - a[1])
                    - (c[0] - a[0]) * (b[1] - a[1])),
            4,
        )

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate triangle vertices and a query point.

        Args:
            difficulty: Controls vertex ranges and point placement.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            ax, ay = 0, 0
            bx = self._rng.randint(2, 6)
            by = 0
            cx = self._rng.randint(0, 4)
            cy = self._rng.randint(2, 6)
            # Centroid
            px = round((ax + bx + cx) / 3.0, 4)
            py = round((ay + by + cy) / 3.0, 4)
        elif difficulty <= 6:
            ax = round(self._rng.uniform(-5, 5), 2)
            ay = round(self._rng.uniform(-5, 5), 2)
            bx = round(self._rng.uniform(-5, 5), 2)
            by = round(self._rng.uniform(-5, 5), 2)
            cx = round(self._rng.uniform(-5, 5), 2)
            cy = round(self._rng.uniform(-5, 5), 2)
            u_rand = self._rng.uniform(0.1, 0.8)
            v_rand = self._rng.uniform(0.1, min(0.8, 1.0 - u_rand))
            w_rand = 1.0 - u_rand - v_rand
            px = round(u_rand * ax + v_rand * bx + w_rand * cx, 4)
            py = round(u_rand * ay + v_rand * by + w_rand * cy, 4)
        else:
            ax = round(self._rng.uniform(-5, 5), 2)
            ay = round(self._rng.uniform(-5, 5), 2)
            bx = round(self._rng.uniform(-5, 5), 2)
            by = round(self._rng.uniform(-5, 5), 2)
            cx = round(self._rng.uniform(-5, 5), 2)
            cy = round(self._rng.uniform(-5, 5), 2)
            px = round(self._rng.uniform(-8, 8), 2)
            py = round(self._rng.uniform(-8, 8), 2)

        a_v = [float(ax), float(ay)]
        b_v = [float(bx), float(by)]
        c_v = [float(cx), float(cy)]
        p_v = [float(px), float(py)]

        area_abc = self._tri_area_2d(a_v, b_v, c_v)
        if abs(area_abc) < 1e-8:
            # Degenerate triangle fallback
            a_v = [0.0, 0.0]
            b_v = [4.0, 0.0]
            c_v = [2.0, 3.0]
            p_v = [2.0, 1.0]
            area_abc = self._tri_area_2d(a_v, b_v, c_v)

        area_pbc = self._tri_area_2d(p_v, b_v, c_v)
        area_apc = self._tri_area_2d(a_v, p_v, c_v)

        u = round(area_pbc / area_abc, 4)
        v = round(area_apc / area_abc, 4)
        w = round(1.0 - u - v, 4)

        inside = (u >= 0) and (v >= 0) and (w >= 0)

        return "u + v + w = 1, \\quad P = u A + v B + w C", {
            "A": a_v, "B": b_v, "C": c_v, "P": p_v,
            "area_abc": area_abc, "area_pbc": area_pbc,
            "area_apc": area_apc,
            "u": u, "v": v, "w": w, "inside": inside,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate barycentric coordinate computation steps.

        Args:
            data: Solution data with vertices, areas, and coordinates.

        Returns:
            List of step strings.
        """
        return [
            f"A={data['A']}, B={data['B']}, C={data['C']}, P={data['P']}",
            f"area(ABC) = {_f(data['area_abc'])}",
            f"area(PBC) = {_f(data['area_pbc'])}",
            f"area(APC) = {_f(data['area_apc'])}",
            f"u = {_f(data['u'])}, v = {_f(data['v'])}, w = {_f(data['w'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return barycentric coordinates and inside/outside status.

        Args:
            data: Solution data.

        Returns:
            Coordinates and containment result.
        """
        status = "inside" if data["inside"] else "outside"
        return f"({_f(data['u'])}, {_f(data['v'])}, {_f(data['w'])}), {status}"


# ===================================================================
# 5. Bezier Curve (tier 5)
# ===================================================================

@register
class BezierCurveGenerator(StepGenerator):
    """Evaluate cubic Bezier B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3.

    Given four 2D control points and a parameter t in [0, 1],
    compute the point on the curve.

    Difficulty scaling:
        Difficulty 1-3: t in {0, 0.5, 1}, integer control points.
        Difficulty 4-6: arbitrary t, decimal control points.
        Difficulty 7-8: compute tangent vector B'(t) as well.

    Prerequisites:
        polynomial_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bezier_curve"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "evaluate cubic Bezier curve point and tangent"
        return "evaluate cubic Bezier curve at parameter t"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate control points and parameter t.

        Args:
            difficulty: Controls t values and coordinate ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pts = [[self._rng.randint(-5, 5), self._rng.randint(-5, 5)]
                   for _ in range(4)]
            t = self._rng.choice([0.0, 0.5, 1.0])
        else:
            pts = [[round(self._rng.uniform(-5, 5), 2),
                     round(self._rng.uniform(-5, 5), 2)]
                    for _ in range(4)]
            t = round(self._rng.uniform(0.1, 0.9), 2)

        s = 1.0 - t
        b0 = s ** 3
        b1 = 3.0 * s ** 2 * t
        b2 = 3.0 * s * t ** 2
        b3 = t ** 3

        bx = round(b0 * pts[0][0] + b1 * pts[1][0] + b2 * pts[2][0] + b3 * pts[3][0], 4)
        by = round(b0 * pts[0][1] + b1 * pts[1][1] + b2 * pts[2][1] + b3 * pts[3][1], 4)

        # Tangent: B'(t) = 3[(1-t)^2(P1-P0) + 2(1-t)t(P2-P1) + t^2(P3-P2)]
        tx_val = round(3.0 * (s ** 2 * (pts[1][0] - pts[0][0])
                               + 2 * s * t * (pts[2][0] - pts[1][0])
                               + t ** 2 * (pts[3][0] - pts[2][0])), 4)
        ty_val = round(3.0 * (s ** 2 * (pts[1][1] - pts[0][1])
                               + 2 * s * t * (pts[2][1] - pts[1][1])
                               + t ** 2 * (pts[3][1] - pts[2][1])), 4)

        return ("B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1"
                " + 3(1-t) t^2 P_2 + t^3 P_3"), {
            "pts": pts, "t": t,
            "b0": round(b0, 4), "b1": round(b1, 4),
            "b2": round(b2, 4), "b3": round(b3, 4),
            "bx": bx, "by": by,
            "tx": tx_val, "ty": ty_val,
            "show_tangent": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bezier evaluation steps.

        Args:
            data: Solution data with basis values and result.

        Returns:
            List of step strings.
        """
        pts = data["pts"]
        steps = [
            f"P0={pts[0]}, P1={pts[1]}, P2={pts[2]}, P3={pts[3]}",
            f"t = {_f(data['t'])}",
            f"basis: {_f(data['b0'])}, {_f(data['b1'])}, {_f(data['b2'])}, {_f(data['b3'])}",
            f"B(t) = ({_f(data['bx'])}, {_f(data['by'])})",
        ]
        if data["show_tangent"]:
            steps.append(f"B'(t) = ({_f(data['tx'])}, {_f(data['ty'])})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the point on the Bezier curve.

        Args:
            data: Solution data.

        Returns:
            Curve point (and tangent if high difficulty).
        """
        ans = f"B(t) = ({_f(data['bx'])}, {_f(data['by'])})"
        if data["show_tangent"]:
            ans += f", B'(t) = ({_f(data['tx'])}, {_f(data['ty'])})"
        return ans


# ===================================================================
# 6. Phong Shading (tier 5)
# ===================================================================

@register
class PhongShadingGenerator(StepGenerator):
    """Compute Phong illumination: I = ka*Ia + kd*(N.L)*Id + ks*(R.V)^n*Is.

    Given surface normal N, light direction L, view direction V, and
    material coefficients, compute ambient + diffuse + specular terms.

    Difficulty scaling:
        Difficulty 1-3: N and L are axis-aligned, n = 1.
        Difficulty 4-6: arbitrary unit vectors, n in [2, 16].
        Difficulty 7-8: compute reflection vector R = 2(N.L)N - L.

    Prerequisites:
        dot_product, vector_norm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phong_shading"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["dot_product", "vector_norm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Phong shading intensity"

    def _normalize(self, v: list[float]) -> list[float]:
        """Normalize a 3D vector to unit length.

        Args:
            v: Input vector.

        Returns:
            Unit vector rounded to 4 dp.
        """
        mag = math.sqrt(sum(x * x for x in v))
        if mag < 1e-10:
            return [0.0, 0.0, 1.0]
        return [round(x / mag, 4) for x in v]

    def _dot3(self, a: list[float], b: list[float]) -> float:
        """Dot product of two 3D vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Dot product rounded to 4 dp.
        """
        return round(sum(ai * bi for ai, bi in zip(a, b)), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate shading parameters and compute Phong illumination.

        Args:
            difficulty: Controls vector complexity and shininess.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_vec = [0.0, 0.0, 1.0]
            l_vec = [0.0, 0.0, 1.0]
            v_vec = [0.0, 0.0, 1.0]
            shininess = 1
        else:
            n_vec = self._normalize(
                [round(self._rng.uniform(-1, 1), 2) for _ in range(3)]
            )
            l_vec = self._normalize(
                [round(self._rng.uniform(-1, 1), 2) for _ in range(3)]
            )
            v_vec = self._normalize(
                [round(self._rng.uniform(-1, 1), 2) for _ in range(3)]
            )
            shininess = self._rng.choice([2, 4, 8, 16])

        ka = round(self._rng.uniform(0.05, 0.3), 2)
        kd = round(self._rng.uniform(0.3, 0.7), 2)
        ks = round(self._rng.uniform(0.1, 0.5), 2)
        ia = round(self._rng.uniform(0.1, 0.5), 2)
        i_d = round(self._rng.uniform(0.5, 1.0), 2)
        i_s = round(self._rng.uniform(0.5, 1.0), 2)

        n_dot_l = max(self._dot3(n_vec, l_vec), 0.0)

        # R = 2(N.L)N - L
        r_vec = [round(2.0 * n_dot_l * n_vec[i] - l_vec[i], 4) for i in range(3)]
        r_dot_v = max(self._dot3(r_vec, v_vec), 0.0)

        ambient = round(ka * ia, 4)
        diffuse = round(kd * n_dot_l * i_d, 4)
        specular = round(ks * (r_dot_v ** shininess) * i_s, 4)
        intensity = round(ambient + diffuse + specular, 4)

        return "I = k_a I_a + k_d (N \\cdot L) I_d + k_s (R \\cdot V)^n I_s", {
            "N": n_vec, "L": l_vec, "V": v_vec, "R": r_vec,
            "ka": ka, "kd": kd, "ks": ks,
            "Ia": ia, "Id": i_d, "Is": i_s, "n": shininess,
            "NdotL": n_dot_l, "RdotV": r_dot_v,
            "ambient": ambient, "diffuse": diffuse,
            "specular": specular, "I": intensity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Phong shading computation steps.

        Args:
            data: Solution data with vectors, coefficients, and terms.

        Returns:
            List of step strings.
        """
        return [
            f"N.L = {_f(data['NdotL'])}",
            f"R = 2(N.L)N - L = {[_f(v) for v in data['R']]}",
            f"R.V = {_f(data['RdotV'])}",
            f"ambient = {_f(data['ka'])}*{_f(data['Ia'])} = {_f(data['ambient'])}",
            f"diffuse = {_f(data['kd'])}*{_f(data['NdotL'])}*{_f(data['Id'])} = {_f(data['diffuse'])}",
            f"specular = {_f(data['ks'])}*{_f(data['RdotV'])}^{data['n']}*{_f(data['Is'])} = {_f(data['specular'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the total Phong shading intensity.

        Args:
            data: Solution data.

        Returns:
            Total intensity value.
        """
        return f"I = {_f(data['I'])}"


# ===================================================================
# 7. Frustum Culling (tier 5)
# ===================================================================

@register
class FrustumCullingGenerator(StepGenerator):
    """Test if a 3D point is inside a view frustum defined by 6 plane inequalities.

    Each plane is defined by a normal vector and offset: N.P + d >= 0.
    A point is inside the frustum only if it satisfies all 6 inequalities.

    Difficulty scaling:
        Difficulty 1-3: axis-aligned box frustum, integer point.
        Difficulty 4-6: tilted near/far planes, decimal point.
        Difficulty 7-8: count how many planes the point violates.

    Prerequisites:
        dot_product.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "frustum_culling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["dot_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "test if point is inside view frustum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 6 frustum planes and a test point.

        Args:
            difficulty: Controls plane complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            lo = self._rng.randint(-10, -2)
            hi = self._rng.randint(2, 10)
            planes = [
                {"normal": [1, 0, 0], "d": -lo, "label": "left"},
                {"normal": [-1, 0, 0], "d": hi, "label": "right"},
                {"normal": [0, 1, 0], "d": -lo, "label": "bottom"},
                {"normal": [0, -1, 0], "d": hi, "label": "top"},
                {"normal": [0, 0, 1], "d": -lo, "label": "near"},
                {"normal": [0, 0, -1], "d": hi, "label": "far"},
            ]
            px = self._rng.randint(lo - 3, hi + 3)
            py = self._rng.randint(lo - 3, hi + 3)
            pz = self._rng.randint(lo - 3, hi + 3)
        else:
            lo = round(self._rng.uniform(-8, -1), 2)
            hi = round(self._rng.uniform(1, 8), 2)
            near_d = round(self._rng.uniform(0.5, 3), 2)
            far_d = round(self._rng.uniform(5, 20), 2)
            planes = [
                {"normal": [1, 0, 0], "d": round(-lo, 4), "label": "left"},
                {"normal": [-1, 0, 0], "d": round(hi, 4), "label": "right"},
                {"normal": [0, 1, 0], "d": round(-lo, 4), "label": "bottom"},
                {"normal": [0, -1, 0], "d": round(hi, 4), "label": "top"},
                {"normal": [0, 0, 1], "d": round(-near_d, 4), "label": "near"},
                {"normal": [0, 0, -1], "d": round(far_d, 4), "label": "far"},
            ]
            px = round(self._rng.uniform(lo - 3, hi + 3), 2)
            py = round(self._rng.uniform(lo - 3, hi + 3), 2)
            pz = round(self._rng.uniform(near_d - 2, far_d + 2), 2)

        point = [float(px), float(py), float(pz)]
        results = []
        violations = 0
        for pl in planes:
            n = pl["normal"]
            d = pl["d"]
            val = round(n[0] * point[0] + n[1] * point[1] + n[2] * point[2] + d, 4)
            inside = val >= 0
            if not inside:
                violations += 1
            results.append({
                "label": pl["label"],
                "val": val,
                "inside": inside,
            })

        all_inside = violations == 0

        return "N_i \\cdot P + d_i \\geq 0 \\quad \\forall i \\in [1,6]", {
            "point": point,
            "planes": planes,
            "results": results,
            "inside": all_inside,
            "violations": violations,
            "count_violations": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate frustum culling test steps.

        Args:
            data: Solution data with plane tests and results.

        Returns:
            List of step strings.
        """
        p = data["point"]
        steps = [f"P = ({_f(p[0])}, {_f(p[1])}, {_f(p[2])})"]
        for r in data["results"]:
            status = "pass" if r["inside"] else "FAIL"
            steps.append(f"{r['label']}: {_f(r['val'])} -> {status}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return whether the point is inside the frustum.

        Args:
            data: Solution data.

        Returns:
            Inside/outside result.
        """
        if data["count_violations"]:
            if data["inside"]:
                return "inside (0 violations)"
            return f"outside ({data['violations']} violations)"
        return "inside" if data["inside"] else "outside"


# ===================================================================
# 8. Quaternion Rotation (tier 6)
# ===================================================================

@register
class QuaternionRotateGenerator(StepGenerator):
    """Rotate a 3D vector using unit quaternion: v' = q * v * q^{-1}.

    Constructs a unit quaternion from axis-angle, computes the conjugate
    q* = (w, -x, -y, -z), and performs quaternion-vector-quaternion
    multiplication.

    Difficulty scaling:
        Difficulty 1-3: rotation about a coordinate axis, 90-degree angle.
        Difficulty 4-6: arbitrary axis (normalised), angle multiple of 45.
        Difficulty 7-8: arbitrary angle, verify |v'| = |v|.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quaternion_rotate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "rotate 3D vector using unit quaternion"

    def _qmul(self, a: list[float], b: list[float]) -> list[float]:
        """Multiply two quaternions [w, x, y, z].

        Args:
            a: First quaternion.
            b: Second quaternion.

        Returns:
            Product quaternion rounded to 4 dp.
        """
        w = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
        x = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
        y = a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1]
        z = a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]
        return [round(w, 4), round(x, 4), round(y, 4), round(z, 4)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quaternion rotation problem.

        Args:
            difficulty: Controls axis and angle complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Generate rotation axis and angle
        if difficulty <= 3:
            axis_choice = self._rng.choice(["x", "y", "z"])
            axis = {"x": [1.0, 0.0, 0.0], "y": [0.0, 1.0, 0.0],
                    "z": [0.0, 0.0, 1.0]}[axis_choice]
            angle_deg = 90
        elif difficulty <= 6:
            raw = [round(self._rng.uniform(-1, 1), 2) for _ in range(3)]
            mag = math.sqrt(sum(x * x for x in raw))
            if mag < 1e-8:
                raw = [1.0, 0.0, 0.0]
                mag = 1.0
            axis = [round(x / mag, 4) for x in raw]
            angle_deg = self._rng.choice([45, 90, 135, 180])
        else:
            raw = [round(self._rng.uniform(-1, 1), 2) for _ in range(3)]
            mag = math.sqrt(sum(x * x for x in raw))
            if mag < 1e-8:
                raw = [0.0, 1.0, 0.0]
                mag = 1.0
            axis = [round(x / mag, 4) for x in raw]
            angle_deg = self._rng.randint(10, 350)

        angle_rad = math.radians(angle_deg)
        half = angle_rad / 2.0
        qw = round(math.cos(half), 4)
        s = round(math.sin(half), 4)
        qx = round(s * axis[0], 4)
        qy = round(s * axis[1], 4)
        qz = round(s * axis[2], 4)
        q = [qw, qx, qy, qz]
        q_conj = [qw, -qx, -qy, -qz]

        # Vector to rotate
        vx = round(self._rng.uniform(-5, 5), 2)
        vy = round(self._rng.uniform(-5, 5), 2)
        vz = round(self._rng.uniform(-5, 5), 2)
        v_quat = [0.0, vx, vy, vz]

        # q * v * q_conj
        qv = self._qmul(q, v_quat)
        qvq = self._qmul(qv, q_conj)

        v_rot = [qvq[1], qvq[2], qvq[3]]

        v_mag = round(math.sqrt(vx ** 2 + vy ** 2 + vz ** 2), 4)
        vr_mag = round(math.sqrt(sum(x ** 2 for x in v_rot)), 4)

        return "v' = q v q^{-1}", {
            "axis": axis, "angle_deg": angle_deg,
            "q": q, "q_conj": q_conj,
            "v": [vx, vy, vz], "v_quat": v_quat,
            "qv": qv, "v_rot": v_rot,
            "v_mag": v_mag, "vr_mag": vr_mag,
            "verify_norm": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quaternion rotation steps.

        Args:
            data: Solution data with quaternion and vector.

        Returns:
            List of step strings.
        """
        q = data["q"]
        steps = [
            f"axis={data['axis']}, angle={data['angle_deg']}deg",
            f"q = [{_f(q[0])}, {_f(q[1])}, {_f(q[2])}, {_f(q[3])}]",
            f"v = {[_f(x) for x in data['v']]}",
            f"q*v = [{_f(data['qv'][0])}, {_f(data['qv'][1])}, "
            f"{_f(data['qv'][2])}, {_f(data['qv'][3])}]",
            f"v' = ({_f(data['v_rot'][0])}, {_f(data['v_rot'][1])}, "
            f"{_f(data['v_rot'][2])})",
        ]
        if data["verify_norm"]:
            steps.append(f"|v| = {_f(data['v_mag'])}, |v'| = {_f(data['vr_mag'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the rotated vector.

        Args:
            data: Solution data.

        Returns:
            Rotated vector coordinates.
        """
        r = data["v_rot"]
        return f"v' = ({_f(r[0])}, {_f(r[1])}, {_f(r[2])})"
