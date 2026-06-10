"""Extended geometry generators -- deeper coordinate and analytic geometry.

12 generators across tiers 3-5 covering centroids, circumcenters, circle
equations, line-circle intersections, vector projections, rotations,
reflections, shoelace area, parametric lines, planes, point-line distance,
and conic section classification.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if isinstance(rounded, float) and rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ---------------------------------------------------------------------------
# 1. Triangle Centroid (tier 3)
# ---------------------------------------------------------------------------

@register
class TriangleCentroidGenerator(StepGenerator):
    """Compute the centroid of a triangle from three vertices.

    The centroid is the arithmetic mean of the vertices:
    G = ((x1+x2+x3)/3, (y1+y2+y3)/3).

    Difficulty scaling:
        d1-3: coordinates in [-10, 10].
        d4-6: coordinates in [-50, 50].
        d7-8: coordinates in [-100, 100].
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "triangle_centroid"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["midpoint"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find centroid of triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate three vertices and compute the centroid.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 10 * min(difficulty, 3) if difficulty <= 3 else 10 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r))
               for _ in range(3)]
        cx = round((pts[0][0] + pts[1][0] + pts[2][0]) / 3, 4)
        cy = round((pts[0][1] + pts[1][1] + pts[2][1]) / 3, 4)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return (
            f"centroid of triangle {pts_str}",
            {"pts": pts, "cx": cx, "cy": cy},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate centroid computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing coordinate averaging.
        """
        pts = sd["pts"]
        sx = pts[0][0] + pts[1][0] + pts[2][0]
        sy = pts[0][1] + pts[1][1] + pts[2][1]
        return [
            f"Gx = ({pts[0][0]} + {pts[1][0]} + {pts[2][0]}) / 3 = {sx} / 3",
            f"Gy = ({pts[0][1]} + {pts[1][1]} + {pts[2][1]}) / 3 = {sy} / 3",
            f"G = ({_fmt(sd['cx'])}, {_fmt(sd['cy'])})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the centroid coordinates.

        Args:
            sd: Solution data dict.

        Returns:
            Centroid as a coordinate pair.
        """
        return f"({_fmt(sd['cx'])},{_fmt(sd['cy'])})"


# ---------------------------------------------------------------------------
# 2. Triangle Circumcenter (tier 4)
# ---------------------------------------------------------------------------

@register
class TriangleCircumcenterGenerator(StepGenerator):
    """Compute the circumcenter of a right triangle.

    For a right triangle the circumcenter is the midpoint of the
    hypotenuse. Generates a right triangle from Pythagorean triples.

    Difficulty scaling:
        d1-3: small triples (3-4-5 family), origin vertex.
        d4-6: larger triples with offset origin.
        d7-8: scaled triples with arbitrary origin.
    """

    _TRIPLES = [
        (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "triangle_circumcenter"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find circumcenter of right triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a right triangle and compute circumcenter.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = min(difficulty - 1, len(self._TRIPLES) - 1)
        a, b, _ = self._TRIPLES[idx]
        scale = max(1, difficulty // 3)
        a, b = a * scale, b * scale
        if difficulty <= 3:
            ox, oy = 0, 0
        else:
            ox = self._rng.randint(-10, 10)
            oy = self._rng.randint(-10, 10)
        p1 = (ox, oy)
        p2 = (ox + a, oy)
        p3 = (ox, oy + b)
        # Circumcenter = midpoint of hypotenuse (p2-p3)
        cx = round((p2[0] + p3[0]) / 2, 4)
        cy = round((p2[1] + p3[1]) / 2, 4)
        pts_str = f"({p1[0]},{p1[1]}) ({p2[0]},{p2[1]}) ({p3[0]},{p3[1]})"
        return (
            f"circumcenter of right triangle {pts_str}",
            {"p1": p1, "p2": p2, "p3": p3, "cx": cx, "cy": cy},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate circumcenter computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing hypotenuse midpoint computation.
        """
        p2, p3 = sd["p2"], sd["p3"]
        return [
            "right triangle: circumcenter = midpoint of hypotenuse",
            f"hypotenuse: ({p2[0]},{p2[1]}) to ({p3[0]},{p3[1]})",
            f"Cx = ({p2[0]} + {p3[0]}) / 2 = {_fmt(sd['cx'])}",
            f"Cy = ({p2[1]} + {p3[1]}) / 2 = {_fmt(sd['cy'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the circumcenter coordinates.

        Args:
            sd: Solution data dict.

        Returns:
            Circumcenter as a coordinate pair.
        """
        return f"({_fmt(sd['cx'])},{_fmt(sd['cy'])})"


# ---------------------------------------------------------------------------
# 3. Circle From Three Points (tier 5)
# ---------------------------------------------------------------------------

@register
class CircleFromThreePointsGenerator(StepGenerator):
    """Find the circle passing through three non-collinear points.

    Solves the system (x-h)^2 + (y-k)^2 = r^2 for center (h,k)
    and radius r using the general form x^2+y^2+Dx+Ey+F=0.

    Difficulty scaling:
        d1-3: integer points on small circles.
        d4-6: points on medium circles.
        d7-8: points on larger circles.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "circle_from_three_points"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find circle through three points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate three points on a circle and recover (h,k,r).

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = self._rng.randint(2, 3 + 2 * difficulty)
        h = self._rng.randint(-5 * difficulty, 5 * difficulty)
        k = self._rng.randint(-5 * difficulty, 5 * difficulty)
        # Pick 3 angles well separated
        angles = sorted(self._rng.sample(range(0, 360, 15), 3))
        pts = []
        for a in angles:
            rad = math.radians(a)
            px = round(h + r * math.cos(rad), 4)
            py = round(k + r * math.sin(rad), 4)
            pts.append((px, py))
        pts_str = " ".join(f"({_fmt(x)},{_fmt(y)})" for x, y in pts)
        return (
            f"circle through {pts_str}",
            {"pts": pts, "h": h, "k": k, "r": r},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate circle-fitting computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing general form and center/radius extraction.
        """
        h, k, r = sd["h"], sd["k"], sd["r"]
        d_val = -2 * h
        e_val = -2 * k
        f_val = h * h + k * k - r * r
        return [
            "general form: x^2 + y^2 + Dx + Ey + F = 0",
            f"D = {_fmt(d_val)}, E = {_fmt(e_val)}, F = {_fmt(f_val)}",
            f"h = -D/2 = {_fmt(h)}, k = -E/2 = {_fmt(k)}",
            f"r = sqrt(h^2 + k^2 - F) = {_fmt(r)}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the circle equation parameters.

        Args:
            sd: Solution data dict.

        Returns:
            Center and radius.
        """
        return f"center=({_fmt(sd['h'])},{_fmt(sd['k'])}), r={_fmt(sd['r'])}"


# ---------------------------------------------------------------------------
# 4. Line-Circle Intersection (tier 4)
# ---------------------------------------------------------------------------

@register
class LineCircleIntersectionGenerator(StepGenerator):
    """Find intersections of a line y=mx+b with a circle (x-h)^2+(y-k)^2=r^2.

    Substitutes the line into the circle equation and solves the
    resulting quadratic. The discriminant determines the number of
    intersection points (0, 1, or 2).

    Difficulty scaling:
        d1-3: circle at origin, integer slope and intercept.
        d4-6: circle offset from origin.
        d7-8: decimal parameters.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "line_circle_intersection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find line-circle intersection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a line and circle and find their intersections.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = self._rng.randint(2, 3 + difficulty)
        if difficulty <= 3:
            h, k = 0, 0
        else:
            h = self._rng.randint(-5, 5)
            k = self._rng.randint(-5, 5)
        m = self._rng.randint(-3, 3)
        b = self._rng.randint(-r - 2, r + 2)
        # Substitute y = mx + b into (x-h)^2 + (y-k)^2 = r^2
        # (x-h)^2 + (mx+b-k)^2 = r^2
        # (1+m^2)x^2 + (-2h + 2m(b-k))x + (h^2 + (b-k)^2 - r^2) = 0
        a_coeff = 1 + m * m
        b_coeff = -2 * h + 2 * m * (b - k)
        c_coeff = h * h + (b - k) ** 2 - r * r
        disc = b_coeff * b_coeff - 4 * a_coeff * c_coeff
        disc = round(disc, 4)
        if disc < 0:
            n_intersections = 0
            points = []
        elif abs(disc) < 1e-9:
            n_intersections = 1
            x1 = round(-b_coeff / (2 * a_coeff), 4)
            y1 = round(m * x1 + b, 4)
            points = [(x1, y1)]
        else:
            n_intersections = 2
            sqrt_disc = math.sqrt(disc)
            x1 = round((-b_coeff + sqrt_disc) / (2 * a_coeff), 4)
            x2 = round((-b_coeff - sqrt_disc) / (2 * a_coeff), 4)
            y1 = round(m * x1 + b, 4)
            y2 = round(m * x2 + b, 4)
            points = [(x1, y1), (x2, y2)]
        problem = (
            f"line y={m}x+{b}, circle (x-{h})^2+(y-{k})^2={r**2}"
        )
        return problem, {
            "m": m, "b": b, "h": h, "k": k, "r": r,
            "a_coeff": a_coeff, "b_coeff": b_coeff,
            "c_coeff": c_coeff, "disc": disc,
            "n": n_intersections, "points": points,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate intersection computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing substitution, quadratic, and discriminant.
        """
        steps = [
            f"substitute y={sd['m']}x+{sd['b']} into circle",
            f"quadratic: {_fmt(sd['a_coeff'])}x^2 + {_fmt(sd['b_coeff'])}x + {_fmt(sd['c_coeff'])} = 0",
            f"discriminant = {_fmt(sd['disc'])}",
        ]
        if sd["n"] == 0:
            steps.append("disc < 0: no intersection")
        elif sd["n"] == 1:
            steps.append(f"tangent at ({_fmt(sd['points'][0][0])},{_fmt(sd['points'][0][1])})")
        else:
            steps.append(
                f"2 points: ({_fmt(sd['points'][0][0])},{_fmt(sd['points'][0][1])}) "
                f"and ({_fmt(sd['points'][1][0])},{_fmt(sd['points'][1][1])})"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the intersection result.

        Args:
            sd: Solution data dict.

        Returns:
            Number of intersections and coordinates.
        """
        if sd["n"] == 0:
            return "no intersection"
        pts_str = ", ".join(f"({_fmt(x)},{_fmt(y)})" for x, y in sd["points"])
        return f"{sd['n']} point(s): {pts_str}"


# ---------------------------------------------------------------------------
# 5. Vector Projection 2D (tier 3)
# ---------------------------------------------------------------------------

@register
class VectorProjection2DGenerator(StepGenerator):
    """Compute the scalar and vector projection of a onto b.

    proj_b(a) = (a.b / b.b) * b.  The scalar projection is
    a.b / |b|.

    Difficulty scaling:
        d1-3: small integer vectors.
        d4-6: medium integer vectors.
        d7-8: larger vectors.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vector_projection_2d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "compute vector projection of a onto b"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two vectors and compute the projection.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + 2 * difficulty
        a = (self._rng.randint(-r, r), self._rng.randint(-r, r))
        b = (self._rng.randint(1, r), self._rng.randint(1, r))
        dot_ab = a[0] * b[0] + a[1] * b[1]
        dot_bb = b[0] * b[0] + b[1] * b[1]
        scalar_proj = round(dot_ab / math.sqrt(dot_bb), 4)
        scale = round(dot_ab / dot_bb, 4)
        vec_proj = (round(scale * b[0], 4), round(scale * b[1], 4))
        return (
            f"proj_b(a): a=({a[0]},{a[1]}), b=({b[0]},{b[1]})",
            {
                "a": a, "b": b,
                "dot_ab": dot_ab, "dot_bb": dot_bb,
                "scalar_proj": scalar_proj,
                "scale": scale, "vec_proj": vec_proj,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate projection computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing dot products and scaling.
        """
        return [
            f"a.b = {sd['a'][0]}*{sd['b'][0]} + {sd['a'][1]}*{sd['b'][1]} = {sd['dot_ab']}",
            f"b.b = {sd['b'][0]}^2 + {sd['b'][1]}^2 = {sd['dot_bb']}",
            f"scalar proj = a.b/|b| = {_fmt(sd['scalar_proj'])}",
            f"vector proj = ({sd['dot_ab']}/{sd['dot_bb']})*b = ({_fmt(sd['vec_proj'][0])},{_fmt(sd['vec_proj'][1])})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the projection results.

        Args:
            sd: Solution data dict.

        Returns:
            Scalar and vector projection.
        """
        return (
            f"scalar={_fmt(sd['scalar_proj'])}, "
            f"vector=({_fmt(sd['vec_proj'][0])},{_fmt(sd['vec_proj'][1])})"
        )


# ---------------------------------------------------------------------------
# 6. Rotation 2D (tier 4)
# ---------------------------------------------------------------------------

@register
class Rotation2DGenerator(StepGenerator):
    """Rotate a point (x,y) by angle theta about the origin.

    x' = x*cos(theta) - y*sin(theta),
    y' = x*sin(theta) + y*cos(theta).

    Difficulty scaling:
        d1-3: multiples of 90 degrees.
        d4-6: multiples of 45 degrees.
        d7-8: multiples of 30 degrees.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rotation_2d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "rotate point by angle theta"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a point and rotation angle, compute rotated coordinates.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 5 * difficulty
        x = self._rng.randint(-r, r)
        y = self._rng.randint(-r, r)
        if difficulty <= 3:
            deg = self._rng.choice([90, 180, 270])
        elif difficulty <= 6:
            deg = self._rng.choice([45, 90, 135, 180, 225, 270, 315])
        else:
            deg = self._rng.choice([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
        rad = math.radians(deg)
        cos_t = round(math.cos(rad), 4)
        sin_t = round(math.sin(rad), 4)
        xp = round(x * cos_t - y * sin_t, 4)
        yp = round(x * sin_t + y * cos_t, 4)
        return (
            f"rotate ({x},{y}) by {deg} degrees",
            {
                "x": x, "y": y, "deg": deg,
                "cos_t": cos_t, "sin_t": sin_t,
                "xp": xp, "yp": yp,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate rotation computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing trig values and coordinate computation.
        """
        return [
            f"cos({sd['deg']}) = {_fmt(sd['cos_t'])}, sin({sd['deg']}) = {_fmt(sd['sin_t'])}",
            f"x' = {sd['x']}*{_fmt(sd['cos_t'])} - {sd['y']}*{_fmt(sd['sin_t'])} = {_fmt(sd['xp'])}",
            f"y' = {sd['x']}*{_fmt(sd['sin_t'])} + {sd['y']}*{_fmt(sd['cos_t'])} = {_fmt(sd['yp'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rotated point.

        Args:
            sd: Solution data dict.

        Returns:
            Rotated coordinates.
        """
        return f"({_fmt(sd['xp'])},{_fmt(sd['yp'])})"


# ---------------------------------------------------------------------------
# 7. Reflection Across Line (tier 4)
# ---------------------------------------------------------------------------

@register
class ReflectionLineGenerator(StepGenerator):
    """Reflect a point across an arbitrary line ax+by+c=0.

    P' = P - 2*(aP_x + bP_y + c)/(a^2 + b^2) * (a, b).

    Difficulty scaling:
        d1-3: reflect across y=x or axes (a,b in {0,1,-1}).
        d4-6: integer line coefficients.
        d7-8: larger coefficients.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reflection_line"

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
        return "reflect point across line ax+by+c=0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a point and line, compute the reflection.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 5 * difficulty
        px = self._rng.randint(-r, r)
        py = self._rng.randint(-r, r)
        if difficulty <= 3:
            a, b, c = self._rng.choice([(1, -1, 0), (0, 1, 0), (1, 0, 0)])
        else:
            a = self._rng.randint(-3, 3)
            b = self._rng.randint(-3, 3)
            if a == 0 and b == 0:
                b = 1
            c = self._rng.randint(-5, 5)
        denom = a * a + b * b
        dist_num = a * px + b * py + c
        t = 2 * dist_num / denom
        rx = round(px - t * a, 4)
        ry = round(py - t * b, 4)
        return (
            f"reflect ({px},{py}) across {a}x+{b}y+{c}=0",
            {
                "px": px, "py": py,
                "a": a, "b": b, "c": c,
                "denom": denom, "dist_num": dist_num,
                "rx": rx, "ry": ry,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate reflection computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing distance computation and reflection formula.
        """
        t = round(2 * sd["dist_num"] / sd["denom"], 4)
        return [
            f"a*Px + b*Py + c = {sd['a']}*{sd['px']} + {sd['b']}*{sd['py']} + {sd['c']} = {sd['dist_num']}",
            f"a^2 + b^2 = {sd['denom']}",
            f"t = 2*{sd['dist_num']}/{sd['denom']} = {_fmt(t)}",
            f"P' = ({sd['px']} - {_fmt(t)}*{sd['a']}, {sd['py']} - {_fmt(t)}*{sd['b']}) = ({_fmt(sd['rx'])},{_fmt(sd['ry'])})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the reflected point.

        Args:
            sd: Solution data dict.

        Returns:
            Reflected coordinates.
        """
        return f"({_fmt(sd['rx'])},{_fmt(sd['ry'])})"


# ---------------------------------------------------------------------------
# 8. Area Polygon Shoelace (tier 4)
# ---------------------------------------------------------------------------

@register
class AreaPolygonShoelaceGenerator(StepGenerator):
    """Compute the area of a polygon using the shoelace formula.

    A = 0.5 * |sum(x_i*y_{i+1} - x_{i+1}*y_i)|. Generates convex
    polygons with 4-6 vertices.

    Difficulty scaling:
        d1-3: 4 vertices, small coordinates.
        d4-6: 5 vertices, medium coordinates.
        d7-8: 6 vertices, larger coordinates.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "area_polygon_shoelace"

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
        return "compute polygon area using shoelace formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate polygon vertices and compute the shoelace area.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6
        r = 3 + 2 * difficulty
        # Generate points around a circle for a convex polygon
        angles = sorted(self._rng.sample(range(0, 360, 10), n))
        pts = []
        for a in angles:
            rad = math.radians(a)
            dist = self._rng.randint(r // 2, r)
            pts.append((round(dist * math.cos(rad)), round(dist * math.sin(rad))))
        cross_sum = 0
        for i in range(n):
            j = (i + 1) % n
            cross_sum += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
        area = round(abs(cross_sum) / 2, 4)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return (
            f"shoelace: {pts_str}",
            {"pts": pts, "cross_sum": cross_sum, "area": area, "n": n},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate shoelace computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing cross products and final area.
        """
        pts = sd["pts"]
        n = sd["n"]
        steps = []
        for i in range(n):
            j = (i + 1) % n
            cross = pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
            steps.append(f"{pts[i][0]}*{pts[j][1]} - {pts[j][0]}*{pts[i][1]} = {cross}")
        steps.append(f"sum = {sd['cross_sum']}, A = |{sd['cross_sum']}|/2 = {_fmt(sd['area'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the polygon area.

        Args:
            sd: Solution data dict.

        Returns:
            Area value.
        """
        return f"A = {_fmt(sd['area'])}"


# ---------------------------------------------------------------------------
# 9. Parametric Line 3D (tier 4)
# ---------------------------------------------------------------------------

@register
class ParametricLine3DGenerator(StepGenerator):
    """Find a point on a parametric line P(t) = P0 + t*d in 3D.

    Given a base point and direction vector, compute the point at
    a specific parameter value and verify it satisfies the equation.

    Difficulty scaling:
        d1-3: small integer components, t in [0, 5].
        d4-6: medium components, t can be negative.
        d7-8: larger components, fractional t.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parametric_line_3d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find point on parametric line in 3D"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 3D parametric line and evaluate at parameter t.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + 2 * difficulty
        p0 = (self._rng.randint(-r, r), self._rng.randint(-r, r), self._rng.randint(-r, r))
        d = (self._rng.randint(-r, r), self._rng.randint(-r, r), self._rng.randint(-r, r))
        if d == (0, 0, 0):
            d = (1, 0, 0)
        if difficulty <= 3:
            t = self._rng.randint(1, 5)
        elif difficulty <= 6:
            t = self._rng.randint(-5, 5)
        else:
            t = round(self._rng.uniform(-3.0, 3.0), 1)
        pt = (
            round(p0[0] + t * d[0], 4),
            round(p0[1] + t * d[1], 4),
            round(p0[2] + t * d[2], 4),
        )
        return (
            f"P(t) = ({p0[0]},{p0[1]},{p0[2]}) + t*({d[0]},{d[1]},{d[2]}), t={_fmt(t)}",
            {"p0": p0, "d": d, "t": t, "pt": pt},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate parametric evaluation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing component-wise computation.
        """
        p0, d, t = sd["p0"], sd["d"], sd["t"]
        return [
            f"x = {p0[0]} + {_fmt(t)}*{d[0]} = {_fmt(sd['pt'][0])}",
            f"y = {p0[1]} + {_fmt(t)}*{d[1]} = {_fmt(sd['pt'][1])}",
            f"z = {p0[2]} + {_fmt(t)}*{d[2]} = {_fmt(sd['pt'][2])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the point on the line.

        Args:
            sd: Solution data dict.

        Returns:
            3D coordinates.
        """
        pt = sd["pt"]
        return f"({_fmt(pt[0])},{_fmt(pt[1])},{_fmt(pt[2])})"


# ---------------------------------------------------------------------------
# 10. Plane Equation (tier 5)
# ---------------------------------------------------------------------------

@register
class PlaneEquationGenerator(StepGenerator):
    """Find the equation of a plane through three points.

    Computes the normal n = (P1P2) x (P1P3) and forms
    n.(r - P1) = 0, producing ax + by + cz = d.

    Difficulty scaling:
        d1-3: small integer coordinates.
        d4-6: medium coordinates.
        d7-8: larger coordinates.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "plane_equation"

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
        return "find plane equation through three points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate three 3D points and compute the plane equation.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + 2 * difficulty
        p1 = tuple(self._rng.randint(-r, r) for _ in range(3))
        p2 = tuple(self._rng.randint(-r, r) for _ in range(3))
        p3 = tuple(self._rng.randint(-r, r) for _ in range(3))
        # Vectors
        v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
        # Cross product n = v1 x v2
        nx = v1[1] * v2[2] - v1[2] * v2[1]
        ny = v1[2] * v2[0] - v1[0] * v2[2]
        nz = v1[0] * v2[1] - v1[1] * v2[0]
        if nx == 0 and ny == 0 and nz == 0:
            # Degenerate: force non-collinear
            p3 = (p3[0] + 1, p3[1], p3[2] + 1)
            v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
            nx = v1[1] * v2[2] - v1[2] * v2[1]
            ny = v1[2] * v2[0] - v1[0] * v2[2]
            nz = v1[0] * v2[1] - v1[1] * v2[0]
        d_val = nx * p1[0] + ny * p1[1] + nz * p1[2]
        pts_str = (
            f"({p1[0]},{p1[1]},{p1[2]}) ({p2[0]},{p2[1]},{p2[2]}) "
            f"({p3[0]},{p3[1]},{p3[2]})"
        )
        return (
            f"plane through {pts_str}",
            {
                "p1": p1, "p2": p2, "p3": p3,
                "v1": v1, "v2": v2,
                "n": (nx, ny, nz), "d": d_val,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate plane equation computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing vectors, cross product, and equation.
        """
        v1, v2, n = sd["v1"], sd["v2"], sd["n"]
        return [
            f"v1 = P2-P1 = ({v1[0]},{v1[1]},{v1[2]})",
            f"v2 = P3-P1 = ({v2[0]},{v2[1]},{v2[2]})",
            f"n = v1 x v2 = ({n[0]},{n[1]},{n[2]})",
            f"{n[0]}x + {n[1]}y + {n[2]}z = {sd['d']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the plane equation.

        Args:
            sd: Solution data dict.

        Returns:
            Plane equation string.
        """
        n = sd["n"]
        return f"{n[0]}x + {n[1]}y + {n[2]}z = {sd['d']}"


# ---------------------------------------------------------------------------
# 11. Distance Point to Line (tier 3)
# ---------------------------------------------------------------------------

@register
class DistancePointLineGenerator(StepGenerator):
    """Compute the distance from a point to a line ax+by+c=0.

    d = |ax0 + by0 + c| / sqrt(a^2 + b^2).

    Difficulty scaling:
        d1-3: small integer coefficients.
        d4-6: medium coefficients.
        d7-8: larger coefficients.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "distance_point_line"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "find distance from point to line"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a point and line, compute the distance.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + 2 * difficulty
        x0 = self._rng.randint(-r, r)
        y0 = self._rng.randint(-r, r)
        a = self._rng.randint(-r, r)
        b = self._rng.randint(-r, r)
        if a == 0 and b == 0:
            a = 1
        c = self._rng.randint(-r, r)
        numerator = abs(a * x0 + b * y0 + c)
        denominator = math.sqrt(a * a + b * b)
        dist = round(numerator / denominator, 4)
        return (
            f"distance from ({x0},{y0}) to {a}x+{b}y+{c}=0",
            {
                "x0": x0, "y0": y0,
                "a": a, "b": b, "c": c,
                "numerator": numerator, "denominator": round(denominator, 4),
                "dist": dist,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate point-to-line distance computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing formula application.
        """
        return [
            f"|{sd['a']}*{sd['x0']} + {sd['b']}*{sd['y0']} + {sd['c']}| = {sd['numerator']}",
            f"sqrt({sd['a']}^2 + {sd['b']}^2) = {_fmt(sd['denominator'])}",
            f"d = {sd['numerator']} / {_fmt(sd['denominator'])} = {_fmt(sd['dist'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the distance.

        Args:
            sd: Solution data dict.

        Returns:
            Distance value.
        """
        return f"d = {_fmt(sd['dist'])}"


# ---------------------------------------------------------------------------
# 12. Conic Section Classification (tier 5)
# ---------------------------------------------------------------------------

@register
class ConicSectionGenerator(StepGenerator):
    """Classify a conic section Ax^2+Bxy+Cy^2+Dx+Ey+F=0.

    Uses the discriminant Delta = B^2 - 4AC:
    Delta < 0 -> ellipse, Delta = 0 -> parabola, Delta > 0 -> hyperbola.

    Difficulty scaling:
        d1-3: B=0 (axis-aligned conics), small coefficients.
        d4-6: nonzero B, medium coefficients.
        d7-8: larger coefficients with mixed signs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conic_section"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify conic section"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate conic coefficients and classify by discriminant.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 2 + difficulty
        a_val = self._rng.randint(1, r)
        c_val = self._rng.randint(-r, r)
        if c_val == 0:
            c_val = 1
        if difficulty <= 3:
            b_val = 0
        else:
            b_val = self._rng.randint(-r, r)
        d_val = self._rng.randint(-r, r)
        e_val = self._rng.randint(-r, r)
        f_val = self._rng.randint(-r, r)
        disc = b_val * b_val - 4 * a_val * c_val
        if disc < 0:
            conic_type = "ellipse"
        elif disc == 0:
            conic_type = "parabola"
        else:
            conic_type = "hyperbola"
        eq = (
            f"{a_val}x^2 + {b_val}xy + {c_val}y^2 "
            f"+ {d_val}x + {e_val}y + {f_val} = 0"
        )
        return (
            f"classify: {eq}",
            {
                "A": a_val, "B": b_val, "C": c_val,
                "D": d_val, "E": e_val, "F": f_val,
                "disc": disc, "conic_type": conic_type,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate conic classification steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing discriminant computation and classification.
        """
        return [
            f"A={sd['A']}, B={sd['B']}, C={sd['C']}",
            f"B^2 - 4AC = {sd['B']}^2 - 4*{sd['A']}*{sd['C']} = {sd['disc']}",
            f"disc {'< 0' if sd['disc'] < 0 else '= 0' if sd['disc'] == 0 else '> 0'} -> {sd['conic_type']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the conic section type.

        Args:
            sd: Solution data dict.

        Returns:
            Classification string.
        """
        return sd["conic_type"]
