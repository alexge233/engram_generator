"""Spatial reasoning generators.

3 generators across tiers 2-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class BoundingBoxGenerator(StepGenerator):
    """Find the axis-aligned bounding box of a point set."""

    @property
    def task_name(self) -> str:
        return "bounding_box"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        return "find bounding box"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty * 2, 12)
        r = 10 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
        min_x = min(x for x, y in pts)
        max_x = max(x for x, y in pts)
        min_y = min(y for x, y in pts)
        max_y = max(y for x, y in pts)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return pts_str, {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"x range: [{sd['min_x']}, {sd['max_x']}]",
            f"y range: [{sd['min_y']}, {sd['max_y']}]",
        ]

    def _create_answer(self, sd: dict) -> str:
        w = sd["max_x"] - sd["min_x"]
        h = sd["max_y"] - sd["min_y"]
        return f"[{sd['min_x']},{sd['min_y']}]-[{sd['max_x']},{sd['max_y']}] ({w}×{h})"


@register
class PointInPolygonGenerator(StepGenerator):
    """Test if a point is inside a convex polygon."""

    @property
    def task_name(self) -> str:
        return "point_in_polygon"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["line_intersection"]

    def task_description(self, difficulty: int) -> str:
        return "point in polygon test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = 5 * difficulty
        n = min(3 + difficulty, 6)
        angles = sorted(self._rng.uniform(0, 2 * math.pi) for _ in range(n))
        poly = [(round(r * math.cos(a)), round(r * math.sin(a))) for a in angles]

        if self._rng.random() < 0.5:
            px = self._rng.randint(-r // 3, r // 3)
            py = self._rng.randint(-r // 3, r // 3)
        else:
            px = r * 2
            py = r * 2

        crossings = 0
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if (y1 <= py < y2 or y2 <= py < y1):
                xint = x1 + (py - y1) * (x2 - x1) / (y2 - y1 + 1e-10)
                if px < xint:
                    crossings += 1
        inside = crossings % 2 == 1

        poly_str = " ".join(f"({x},{y})" for x, y in poly)
        return (
            f"point ({px},{py}) in polygon {poly_str}?",
            {"px": px, "py": py, "poly": poly, "inside": inside, "crossings": crossings},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"ray casting: {sd['crossings']} crossings", f"{'odd' if sd['inside'] else 'even'} = {'inside' if sd['inside'] else 'outside'}"]

    def _create_answer(self, sd: dict) -> str:
        return "INSIDE" if sd["inside"] else "OUTSIDE"


@register
class ConvexHullCheckGenerator(StepGenerator):
    """Check if a set of points forms a convex polygon."""

    @property
    def task_name(self) -> str:
        return "convex_hull_check"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["polygon_area"]

    def task_description(self, difficulty: int) -> str:
        return "check convexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        r = 5 * difficulty

        if self._rng.random() < 0.5:
            angles = sorted(self._rng.uniform(0, 2 * math.pi) for _ in range(n))
            pts = [(round(r * math.cos(a)), round(r * math.sin(a))) for a in angles]
            is_convex = True
        else:
            pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
            cross_signs = []
            for i in range(n):
                o = pts[i]
                a = pts[(i + 1) % n]
                b = pts[(i + 2) % n]
                cross = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
                cross_signs.append(cross > 0)
            is_convex = len(set(cross_signs)) <= 1

        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return f"convex? {pts_str}", {"pts": pts, "is_convex": is_convex}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"check cross products of consecutive edges"]

    def _create_answer(self, sd: dict) -> str:
        return "CONVEX" if sd["is_convex"] else "NOT CONVEX"
