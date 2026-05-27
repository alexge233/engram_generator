"""Geometry generators — shapes, coordinates, transformations.

Adds 20 generators across tiers 0-4 covering area, perimeter, volume,
coordinate geometry, and 2D transformations.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── TIER 0 ─────────────────────────────────────────────────────────

@register
class AreaRectangleGenerator(StepGenerator):
    """Compute the area of a rectangle given length and width."""

    @property
    def task_name(self) -> str:
        return "area_rectangle"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find area of rectangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        upper = 10 ** min(difficulty + 1, 5)
        l = self._rng.randint(1, upper)
        w = self._rng.randint(1, upper)
        area = l * w
        return f"rectangle l={l} w={w}", {"l": l, "w": w, "area": area}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"A = l * w", f"A = {sd['l']} * {sd['w']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["area"])


@register
class PerimeterRectangleGenerator(StepGenerator):
    """Compute the perimeter of a rectangle."""

    @property
    def task_name(self) -> str:
        return "perimeter_rectangle"

    @property
    def tier(self) -> int:
        return 0

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "find perimeter of rectangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        upper = 10 ** min(difficulty + 1, 5)
        l = self._rng.randint(1, upper)
        w = self._rng.randint(1, upper)
        p = 2 * (l + w)
        return f"rectangle l={l} w={w}", {"l": l, "w": w, "perimeter": p}

    def _create_steps(self, sd: dict) -> list[str]:
        s = sd["l"] + sd["w"]
        return [f"P = 2(l + w)", f"l + w = {s}", f"P = 2 * {s}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["perimeter"])


@register
class PythagoreanGenerator(StepGenerator):
    """Find the hypotenuse or missing side of a right triangle."""

    @property
    def task_name(self) -> str:
        return "pythagorean"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["addition", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find missing side of right triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        triples = [
            (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
            (9, 40, 41), (11, 60, 61), (20, 21, 29), (12, 35, 37),
        ]
        scale = self._rng.randint(1, max(1, difficulty))
        a, b, c = self._rng.choice(triples[:min(difficulty + 1, len(triples))])
        a, b, c = a * scale, b * scale, c * scale

        mode = self._rng.choice(["hypotenuse", "leg"])
        if mode == "hypotenuse":
            problem = f"right triangle a={a} b={b}, find c"
            sd = {"a": a, "b": b, "c": c, "mode": "hypotenuse"}
        else:
            problem = f"right triangle a={a} c={c}, find b"
            sd = {"a": a, "b": b, "c": c, "mode": "leg"}
        return problem, sd

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "hypotenuse":
            a2 = sd["a"] ** 2
            b2 = sd["b"] ** 2
            return [
                f"c^2 = a^2 + b^2",
                f"c^2 = {a2} + {b2} = {a2 + b2}",
                f"c = sqrt({a2 + b2})",
            ]
        a2 = sd["a"] ** 2
        c2 = sd["c"] ** 2
        return [
            f"b^2 = c^2 - a^2",
            f"b^2 = {c2} - {a2} = {c2 - a2}",
            f"b = sqrt({c2 - a2})",
        ]

    def _create_answer(self, sd: dict) -> str:
        if sd["mode"] == "hypotenuse":
            return str(sd["c"])
        return str(sd["b"])


# ── TIER 1 ─────────────────────────────────────────────────────────

@register
class AreaTriangleGenerator(StepGenerator):
    """Compute area of a triangle from base and height."""

    @property
    def task_name(self) -> str:
        return "area_triangle"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["area_rectangle"]

    def task_description(self, difficulty: int) -> str:
        return "find area of triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        upper = 10 ** min(difficulty + 1, 4)
        b = self._rng.randint(1, upper)
        h = self._rng.randint(1, upper)
        area = b * h / 2
        return f"triangle base={b} height={h}", {"b": b, "h": h, "area": area}

    def _create_steps(self, sd: dict) -> list[str]:
        prod = sd["b"] * sd["h"]
        return [f"A = (1/2) * b * h", f"A = (1/2) * {prod}"]

    def _create_answer(self, sd: dict) -> str:
        a = sd["area"]
        return str(int(a)) if a == int(a) else f"{a:.1f}"


@register
class AreaCircleGenerator(StepGenerator):
    """Compute area of a circle from radius."""

    @property
    def task_name(self) -> str:
        return "area_circle"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find area of circle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 10 * difficulty)
        area = math.pi * r * r
        return f"circle r={r}", {"r": r, "area": round(area, 2)}

    def _create_steps(self, sd: dict) -> list[str]:
        r2 = sd["r"] ** 2
        return [f"A = pi * r^2", f"A = pi * {r2}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['area']}"


@register
class CircumferenceGenerator(StepGenerator):
    """Compute circumference of a circle."""

    @property
    def task_name(self) -> str:
        return "circumference"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find circumference of circle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 10 * difficulty)
        c = round(2 * math.pi * r, 2)
        return f"circle r={r}", {"r": r, "circumference": c}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"C = 2 * pi * r", f"C = 2 * pi * {sd['r']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['circumference']}"


@register
class VolumeBoxGenerator(StepGenerator):
    """Compute volume of a rectangular box."""

    @property
    def task_name(self) -> str:
        return "volume_box"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["area_rectangle"]

    def task_description(self, difficulty: int) -> str:
        return "find volume of box"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        upper = 10 ** min(difficulty, 4)
        l = self._rng.randint(1, upper)
        w = self._rng.randint(1, upper)
        h = self._rng.randint(1, upper)
        v = l * w * h
        return f"box l={l} w={w} h={h}", {"l": l, "w": w, "h": h, "volume": v}

    def _create_steps(self, sd: dict) -> list[str]:
        lw = sd["l"] * sd["w"]
        return [f"V = l * w * h", f"l * w = {lw}", f"V = {lw} * {sd['h']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["volume"])


# ── TIER 2 ─────────────────────────────────────────────────────────

@register
class Distance2DGenerator(StepGenerator):
    """Compute Euclidean distance between two points."""

    @property
    def task_name(self) -> str:
        return "distance_2d"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["pythagorean"]

    def task_description(self, difficulty: int) -> str:
        return "find distance between two points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = 10 * difficulty
        x1 = self._rng.randint(-r, r)
        y1 = self._rng.randint(-r, r)
        x2 = self._rng.randint(-r, r)
        y2 = self._rng.randint(-r, r)
        dx = x2 - x1
        dy = y2 - y1
        dist = round(math.sqrt(dx * dx + dy * dy), 4)
        return (
            f"distance ({x1},{y1}) to ({x2},{y2})",
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
             "dx": dx, "dy": dy, "dist": dist},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        dx2 = sd["dx"] ** 2
        dy2 = sd["dy"] ** 2
        return [
            f"dx = {sd['x2']} - {sd['x1']} = {sd['dx']}",
            f"dy = {sd['y2']} - {sd['y1']} = {sd['dy']}",
            f"d = sqrt({dx2} + {dy2}) = sqrt({dx2 + dy2})",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['dist']}"


@register
class MidpointGenerator(StepGenerator):
    """Find the midpoint of a line segment."""

    @property
    def task_name(self) -> str:
        return "midpoint"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["addition", "division"]

    def task_description(self, difficulty: int) -> str:
        return "find midpoint of segment"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = 10 * difficulty
        x1 = self._rng.randint(-r, r)
        y1 = self._rng.randint(-r, r)
        x2 = self._rng.randint(-r, r)
        y2 = self._rng.randint(-r, r)
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        return (
            f"midpoint ({x1},{y1}) to ({x2},{y2})",
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "mx": mx, "my": my},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"mx = ({sd['x1']} + {sd['x2']}) / 2 = {sd['mx']}",
            f"my = ({sd['y1']} + {sd['y2']}) / 2 = {sd['my']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        def fmt(v):
            return str(int(v)) if v == int(v) else f"{v:.1f}"
        return f"({fmt(sd['mx'])},{fmt(sd['my'])})"


@register
class SlopeGenerator(StepGenerator):
    """Compute the slope of a line through two points."""

    @property
    def task_name(self) -> str:
        return "slope"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        return "find slope of line"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = 10 * difficulty
        x1 = self._rng.randint(-r, r)
        y1 = self._rng.randint(-r, r)
        x2 = x1 + self._rng.randint(1, r)
        y2 = self._rng.randint(-r, r)
        dy = y2 - y1
        dx = x2 - x1
        slope = round(dy / dx, 4)
        return (
            f"slope ({x1},{y1}) to ({x2},{y2})",
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
             "dy": dy, "dx": dx, "slope": slope},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"dy = {sd['y2']} - {sd['y1']} = {sd['dy']}",
            f"dx = {sd['x2']} - {sd['x1']} = {sd['dx']}",
            f"m = {sd['dy']} / {sd['dx']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['slope']}"


@register
class AngleSumTriangleGenerator(StepGenerator):
    """Find the missing angle of a triangle given two angles."""

    @property
    def task_name(self) -> str:
        return "angle_sum_triangle"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        return "find missing angle in triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(10, 80)
        b = self._rng.randint(10, 170 - a)
        c = 180 - a - b
        return (
            f"triangle angles: {a}, {b}, ?",
            {"a": a, "b": b, "c": c},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        s = sd["a"] + sd["b"]
        return [
            f"sum of angles = 180",
            f"{sd['a']} + {sd['b']} = {s}",
            f"missing = 180 - {s}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["c"])


@register
class SimilarTrianglesGenerator(StepGenerator):
    """Find a missing side using similar triangle ratios."""

    @property
    def task_name(self) -> str:
        return "similar_triangles"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["division", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find missing side of similar triangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(2, 5 * difficulty)
        b = self._rng.randint(2, 5 * difficulty)
        c = self._rng.randint(2, 5 * difficulty)
        k = self._rng.randint(2, max(2, difficulty + 1))
        d = a * k
        e = b * k
        f_val = c * k
        return (
            f"ABC sides {a},{b},{c} ~ DEF with DE={d}, find EF and DF",
            {"a": a, "b": b, "c": c, "k": k, "d": d, "e": e, "f": f_val},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"scale = DE / AB = {sd['d']} / {sd['a']} = {sd['k']}",
            f"EF = BC * {sd['k']} = {sd['b']} * {sd['k']} = {sd['e']}",
            f"DF = AC * {sd['k']} = {sd['c']} * {sd['k']} = {sd['f']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"EF={sd['e']}, DF={sd['f']}"


# ── TIER 3 ─────────────────────────────────────────────────────────

@register
class LineIntersectionGenerator(StepGenerator):
    """Find where two lines y=mx+b intersect."""

    @property
    def task_name(self) -> str:
        return "line_intersection"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["slope", "linear_equation"]

    def task_description(self, difficulty: int) -> str:
        return "find intersection of two lines"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m1 = self._rng.randint(-5 * difficulty, 5 * difficulty)
        m2 = m1 + self._rng.randint(1, 5)
        b1 = self._rng.randint(-10 * difficulty, 10 * difficulty)
        b2 = self._rng.randint(-10 * difficulty, 10 * difficulty)
        x = round((b2 - b1) / (m1 - m2), 4)
        y = round(m1 * x + b1, 4)
        return (
            f"y = {m1}x + {b1} and y = {m2}x + {b2}",
            {"m1": m1, "m2": m2, "b1": b1, "b2": b2, "x": x, "y": y},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['m1']}x + {sd['b1']} = {sd['m2']}x + {sd['b2']}",
            f"({sd['m1']} - {sd['m2']})x = {sd['b2']} - {sd['b1']}",
            f"x = {sd['x']}",
            f"y = {sd['m1']} * {sd['x']} + {sd['b1']} = {sd['y']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"({sd['x']},{sd['y']})"


@register
class PolygonAreaGenerator(StepGenerator):
    """Compute area of a polygon using the shoelace formula."""

    @property
    def task_name(self) -> str:
        return "polygon_area"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["area_triangle", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "find area of polygon (shoelace)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 8)
        r = 5 * difficulty
        pts = []
        for _ in range(n):
            pts.append((self._rng.randint(-r, r), self._rng.randint(-r, r)))
        s = 0
        for i in range(n):
            j = (i + 1) % n
            s += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
        area = round(abs(s) / 2, 2)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return pts_str, {"pts": pts, "area": area, "cross_sum": s}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        pts = sd["pts"]
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            cross = pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
            steps.append(
                f"({pts[i][0]}*{pts[j][1]}) - ({pts[j][0]}*{pts[i][1]}) = {cross}"
            )
        steps.append(f"A = |{sd['cross_sum']}| / 2")
        return steps

    def _create_answer(self, sd: dict) -> str:
        a = sd["area"]
        return str(int(a)) if a == int(a) else f"{a}"


@register
class CircleArcLengthGenerator(StepGenerator):
    """Compute arc length of a circular sector."""

    @property
    def task_name(self) -> str:
        return "circle_arc_length"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["circumference"]

    def task_description(self, difficulty: int) -> str:
        return "find arc length"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 10 * difficulty)
        deg = self._rng.choice([30, 45, 60, 90, 120, 135, 150, 180, 270])
        rad = deg * math.pi / 180
        arc = round(r * rad, 4)
        return (
            f"r={r} angle={deg} degrees",
            {"r": r, "deg": deg, "rad": round(rad, 4), "arc": arc},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"theta = {sd['deg']} * pi/180 = {sd['rad']} rad",
            f"s = r * theta = {sd['r']} * {sd['rad']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['arc']}"


@register
class SectorAreaGenerator(StepGenerator):
    """Compute area of a circular sector."""

    @property
    def task_name(self) -> str:
        return "sector_area"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["area_circle"]

    def task_description(self, difficulty: int) -> str:
        return "find sector area"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 10 * difficulty)
        deg = self._rng.choice([30, 45, 60, 90, 120, 150, 180, 270])
        rad = deg * math.pi / 180
        area = round(0.5 * r * r * rad, 4)
        return (
            f"sector r={r} angle={deg} degrees",
            {"r": r, "deg": deg, "rad": round(rad, 4), "area": area},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        r2 = sd["r"] ** 2
        return [
            f"theta = {sd['deg']} * pi/180 = {sd['rad']}",
            f"A = (1/2) * r^2 * theta = (1/2) * {r2} * {sd['rad']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['area']}"


# ── TIER 4 ─────────────────────────────────────────────────────────

@register
class CoordinateRotationGenerator(StepGenerator):
    """Rotate a point about the origin."""

    @property
    def task_name(self) -> str:
        return "coordinate_rotation"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["distance_2d"]

    def task_description(self, difficulty: int) -> str:
        return "rotate point about origin"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        x = self._rng.randint(-10 * difficulty, 10 * difficulty)
        y = self._rng.randint(-10 * difficulty, 10 * difficulty)
        deg = self._rng.choice([90, 180, 270])
        rad = math.radians(deg)
        xp = round(x * math.cos(rad) - y * math.sin(rad), 4)
        yp = round(x * math.sin(rad) + y * math.cos(rad), 4)
        return (
            f"rotate ({x},{y}) by {deg} degrees",
            {"x": x, "y": y, "deg": deg, "xp": xp, "yp": yp},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"x' = x*cos({sd['deg']}) - y*sin({sd['deg']})",
            f"y' = x*sin({sd['deg']}) + y*cos({sd['deg']})",
            f"({sd['x']},{sd['y']}) -> ({sd['xp']},{sd['yp']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        def fmt(v):
            return str(int(v)) if abs(v - round(v)) < 1e-9 else f"{v}"
        return f"({fmt(sd['xp'])},{fmt(sd['yp'])})"


@register
class Reflection2DGenerator(StepGenerator):
    """Reflect a point across an axis."""

    @property
    def task_name(self) -> str:
        return "reflection_2d"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["distance_2d"]

    def task_description(self, difficulty: int) -> str:
        return "reflect point across axis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        x = self._rng.randint(-10 * difficulty, 10 * difficulty)
        y = self._rng.randint(-10 * difficulty, 10 * difficulty)
        axis = self._rng.choice(["x-axis", "y-axis", "y=x"])
        if axis == "x-axis":
            rx, ry = x, -y
        elif axis == "y-axis":
            rx, ry = -x, y
        else:
            rx, ry = y, x
        return (
            f"reflect ({x},{y}) across {axis}",
            {"x": x, "y": y, "axis": axis, "rx": rx, "ry": ry},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        axis = sd["axis"]
        if axis == "x-axis":
            rule = "(x, y) -> (x, -y)"
        elif axis == "y-axis":
            rule = "(x, y) -> (-x, y)"
        else:
            rule = "(x, y) -> (y, x)"
        return [f"rule: {rule}", f"({sd['x']},{sd['y']}) -> ({sd['rx']},{sd['ry']})"]

    def _create_answer(self, sd: dict) -> str:
        return f"({sd['rx']},{sd['ry']})"


@register
class VolumeSphereGenerator(StepGenerator):
    """Compute volume of a sphere."""

    @property
    def task_name(self) -> str:
        return "volume_sphere"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["area_circle"]

    def task_description(self, difficulty: int) -> str:
        return "find volume of sphere"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 5 * difficulty)
        v = round((4 / 3) * math.pi * r ** 3, 2)
        return f"sphere r={r}", {"r": r, "volume": v}

    def _create_steps(self, sd: dict) -> list[str]:
        r3 = sd["r"] ** 3
        return [
            f"V = (4/3) * pi * r^3",
            f"V = (4/3) * pi * {r3}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['volume']}"


@register
class VolumeCylinderGenerator(StepGenerator):
    """Compute volume of a cylinder."""

    @property
    def task_name(self) -> str:
        return "volume_cylinder"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["area_circle"]

    def task_description(self, difficulty: int) -> str:
        return "find volume of cylinder"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(1, 5 * difficulty)
        h = self._rng.randint(1, 10 * difficulty)
        v = round(math.pi * r ** 2 * h, 2)
        return f"cylinder r={r} h={h}", {"r": r, "h": h, "volume": v}

    def _create_steps(self, sd: dict) -> list[str]:
        r2 = sd["r"] ** 2
        return [
            f"V = pi * r^2 * h",
            f"V = pi * {r2} * {sd['h']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['volume']}"
