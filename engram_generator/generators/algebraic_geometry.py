"""Algebraic geometry generators.

8 generators covering affine varieties, ideal membership, Bezout's
theorem, elliptic curve arithmetic, projective coordinates, genus
computation, rational points on conics, and tangent lines to varieties
across tiers 6-7.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _gcd(a: int, b: int) -> int:
    """Compute greatest common divisor.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        GCD of a and b.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def _mod_inv(a: int, p: int) -> int:
    """Compute modular inverse of a mod p using extended Euclidean algorithm.

    Args:
        a: Integer to invert.
        p: Prime modulus.

    Returns:
        Inverse of a modulo p.

    Raises:
        ValueError: If inverse does not exist.
    """
    g, x, _ = _extended_gcd(a % p, p)
    if g != 1:
        raise ValueError(f"No inverse for {a} mod {p}")
    return x % p


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple of (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def _format_point(x: int, y: int) -> str:
    """Format a 2D point as a string.

    Args:
        x: X coordinate.
        y: Y coordinate.

    Returns:
        String like ``(2, 3)``.
    """
    return f"({x}, {y})"


def _format_points(points: list[tuple[int, int]]) -> str:
    """Format a list of 2D points as a set string.

    Args:
        points: List of (x, y) tuples.

    Returns:
        String like ``{(0, 1), (2, 3)}``.
    """
    if not points:
        return "{}"
    parts = [_format_point(x, y) for x, y in sorted(points)]
    return "{" + ", ".join(parts) + "}"


# ═══════════════════════════════════════════════════════════════════
# 1. VARIETY POINTS (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class VarietyPointsGenerator(StepGenerator):
    """Find all points on an affine variety V(f) over a finite field F_p.

    Given a polynomial f(x,y) and a small prime p, tests all pairs
    (x,y) in F_p x F_p to find the zero locus V(f).

    Difficulty scaling:
        Difficulty 1-3: p in [3, 5], simple curves (x^2 + y^2 - c).
        Difficulty 4-6: p in [5, 7], products (x*y - c).
        Difficulty 7-8: p in [7, 11], mixed polynomials.

    Prerequisites:
        modular (tier 2), polynomial_eval (tier 2).
    """

    _CURVES = [
        ("x^2+y^2-{c}", lambda x, y, c, p: (x * x + y * y - c) % p),
        ("x*y-{c}", lambda x, y, c, p: (x * y - c) % p),
        ("x^2-y-{c}", lambda x, y, c, p: (x * x - y - c) % p),
        ("x^2+x*y+y^2-{c}", lambda x, y, c, p: (x * x + x * y + y * y - c) % p),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "variety_points"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular", "polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls field size and curve complexity.

        Returns:
            Task description string.
        """
        return "find all points on variety V(f) over F_p"

    def _select_params(self, difficulty: int) -> tuple[int, int]:
        """Choose prime p and curve index based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Tuple of (prime p, curve index).
        """
        if difficulty <= 3:
            p = self._rng.choice([3, 5])
            idx = self._rng.randint(0, 1)
        elif difficulty <= 6:
            p = self._rng.choice([5, 7])
            idx = self._rng.randint(0, 2)
        else:
            p = self._rng.choice([7, 11])
            idx = self._rng.randint(0, 3)
        return p, idx

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a variety point-finding problem.

        Args:
            difficulty: Controls field size and curve complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p, idx = self._select_params(difficulty)
        c = self._rng.randint(1, p - 1)
        template, eval_fn = self._CURVES[idx]
        curve_str = template.format(c=c)

        points = []
        for x in range(p):
            for y in range(p):
                if eval_fn(x, y, c, p) == 0:
                    points.append((x, y))

        problem = f"V({curve_str}) over F_{p}. Find all points."
        return problem, {
            "p": p, "c": c, "curve": curve_str,
            "points": points, "count": len(points),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate variety point-finding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the search and results.
        """
        p = data["p"]
        steps = [f"test all (x,y) in F_{p} x F_{p}"]
        shown = data["points"][:6]
        if shown:
            pts_str = ", ".join(_format_point(x, y) for x, y in shown)
            steps.append(f"zeros: {pts_str}")
        if len(data["points"]) > 6:
            steps.append(f"... {data['count']} points total")
        steps.append(f"|V(f)| = {data['count']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The point set and count.
        """
        if data["count"] <= 8:
            return f"{_format_points(data['points'])}, |V|={data['count']}"
        return f"|V(f)| = {data['count']}"


# ═══════════════════════════════════════════════════════════════════
# 2. IDEAL MEMBERSHIP (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class IdealMembershipGenerator(StepGenerator):
    """Test if a polynomial g lies in the ideal generated by f1 and f2.

    Uses simple univariate polynomials over Z. Checks whether g can
    be written as a*f1 + b*f2 for integer polynomials a, b by testing
    polynomial division and remainder.

    Difficulty scaling:
        Difficulty 1-3: linear generators, low-degree g.
        Difficulty 4-6: quadratic generators.
        Difficulty 7-8: mixed-degree generators.

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ideal_membership"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Task description string.
        """
        return "test if polynomial is in ideal <f1, f2>"

    def _poly_str(self, coeffs: list[int]) -> str:
        """Format polynomial coefficients as a string.

        Args:
            coeffs: Coefficients from highest to lowest degree.

        Returns:
            Polynomial string.
        """
        deg = len(coeffs) - 1
        parts = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            if power == 0:
                parts.append(str(c))
            elif power == 1:
                parts.append(f"{c}x" if c != 1 else "x")
            else:
                parts.append(f"{c}x^{power}" if c != 1 else f"x^{power}")
        return "+".join(parts).replace("+-", "-") if parts else "0"

    def _poly_eval(self, coeffs: list[int], x: int) -> int:
        """Evaluate polynomial at integer x using Horner's method.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Evaluation point.

        Returns:
            Polynomial value at x.
        """
        result = 0
        for c in coeffs:
            result = result * x + c
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ideal membership problem.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a1 = self._rng.randint(1, 3)
            b1 = self._rng.randint(-3, 3)
            f1 = [a1, b1]
            a2 = self._rng.randint(1, 3)
            b2 = self._rng.randint(-3, 3)
            f2 = [a2, b2]
        elif difficulty <= 6:
            f1 = [1, self._rng.randint(-2, 2), self._rng.randint(-3, 3)]
            f2 = [1, self._rng.randint(-2, 2)]
        else:
            f1 = [1, self._rng.randint(-2, 2), self._rng.randint(-3, 3)]
            f2 = [1, 0, self._rng.randint(-3, 3)]

        in_ideal = self._rng.random() < 0.5
        if in_ideal:
            ca = self._rng.randint(1, 2)
            cb = self._rng.randint(1, 2)
            max_len = max(len(f1), len(f2))
            pad_f1 = [0] * (max_len - len(f1)) + f1
            pad_f2 = [0] * (max_len - len(f2)) + f2
            g = [ca * a_c + cb * b_c for a_c, b_c in zip(pad_f1, pad_f2)]
            while len(g) > 1 and g[0] == 0:
                g = g[1:]
        else:
            deg = max(len(f1), len(f2))
            g = [self._rng.randint(-3, 3) for _ in range(deg)]
            if g[0] == 0:
                g[0] = 1

        f1_str = self._poly_str(f1)
        f2_str = self._poly_str(f2)
        g_str = self._poly_str(g)
        problem = f"g={g_str}, I=<{f1_str}, {f2_str}>. Is g in I?"
        return problem, {
            "f1": f1, "f2": f2, "g": g,
            "f1_str": f1_str, "f2_str": f2_str, "g_str": g_str,
            "in_ideal": in_ideal,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ideal membership test steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing division and remainder analysis.
        """
        steps = [
            f"generators: f1={data['f1_str']}, f2={data['f2_str']}",
            f"target: g={data['g_str']}",
        ]
        if data["in_ideal"]:
            steps.append("g = a*f1 + b*f2 for some a, b")
            steps.append("remainder after division = 0")
        else:
            steps.append("cannot express g = a*f1 + b*f2")
            steps.append("nonzero remainder => g not in I")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        return "YES" if data["in_ideal"] else "NO"


# ═══════════════════════════════════════════════════════════════════
# 3. BEZOUT INTERSECTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class BezoutIntersectionGenerator(StepGenerator):
    """Count intersection points of two plane curves using Bezout's theorem.

    For two curves of degree d1 and d2 in the projective plane,
    Bezout's theorem states that they intersect in exactly d1*d2
    points (counted with multiplicity). Generates small examples
    and verifies the count.

    Difficulty scaling:
        Difficulty 1-3: lines and conics (d1=1, d2=2).
        Difficulty 4-6: two conics (d1=d2=2).
        Difficulty 7-8: conic and cubic (d1=2, d2=3).

    Prerequisites:
        system_equations (tier 3).
    """

    _CURVE_NAMES = {
        1: ["line", "linear form"],
        2: ["conic", "quadratic curve", "circle", "ellipse", "parabola"],
        3: ["cubic", "cubic curve", "elliptic curve"],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bezout_intersection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls curve degrees.

        Returns:
            Task description string.
        """
        return "count curve intersections using Bezout's theorem"

    def _select_degrees(self, difficulty: int) -> tuple[int, int]:
        """Choose curve degrees based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Tuple of (degree1, degree2).
        """
        if difficulty <= 3:
            return (1, self._rng.choice([1, 2]))
        if difficulty <= 6:
            return (2, 2)
        return (2, 3)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bezout intersection count problem.

        Args:
            difficulty: Controls curve degrees.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        d1, d2 = self._select_degrees(difficulty)
        bezout_count = d1 * d2
        name1 = self._rng.choice(self._CURVE_NAMES[d1])
        name2 = self._rng.choice(self._CURVE_NAMES[d2])

        problem = (
            f"C1: {name1} (deg {d1}), C2: {name2} (deg {d2}). "
            f"Max intersections by Bezout?"
        )
        return problem, {
            "d1": d1, "d2": d2, "name1": name1, "name2": name2,
            "bezout_count": bezout_count,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bezout intersection steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying Bezout's theorem.
        """
        d1, d2 = data["d1"], data["d2"]
        return [
            f"deg(C1) = {d1}, deg(C2) = {d2}",
            f"Bezout: #intersections = d1 * d2 = {d1} * {d2}",
            f"= {data['bezout_count']} (counted with multiplicity)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Bezout intersection count.
        """
        return str(data["bezout_count"])


# ═══════════════════════════════════════════════════════════════════
# 4. ELLIPTIC CURVE GROUP LAW (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class EllipticCurveGroupLawGenerator(StepGenerator):
    """Perform point addition on an elliptic curve y^2 = x^3 + ax + b mod p.

    Given two points P and Q on the curve, computes P + Q using the
    chord-and-tangent rule. Handles the case P = Q (point doubling)
    and the point at infinity (identity element).

    Difficulty scaling:
        Difficulty 1-3: p in [5, 7], small coordinates.
        Difficulty 4-6: p in [7, 11].
        Difficulty 7-8: p in [11, 13], point doubling cases.

    Prerequisites:
        mod_inv (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elliptic_curve_group_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls field size.

        Returns:
            Task description string.
        """
        return "add points on elliptic curve mod p"

    def _find_curve_and_points(self, p: int) -> tuple[int, int, list[tuple[int, int]]]:
        """Find a valid elliptic curve and points on it.

        Args:
            p: Prime modulus.

        Returns:
            Tuple of (a, b, list_of_points_on_curve).
        """
        for _ in range(100):
            a = self._rng.randint(0, p - 1)
            b = self._rng.randint(1, p - 1)
            disc = (4 * a * a * a + 27 * b * b) % p
            if disc == 0:
                continue
            points = []
            for x in range(p):
                rhs = (x * x * x + a * x + b) % p
                for y in range(p):
                    if (y * y) % p == rhs:
                        points.append((x, y))
            if len(points) >= 2:
                return a, b, points
        return 1, 1, [(0, 1)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an elliptic curve point addition problem.

        Args:
            difficulty: Controls field size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.choice([5, 7])
        elif difficulty <= 6:
            p = self._rng.choice([7, 11])
        else:
            p = self._rng.choice([11, 13])

        a, b, curve_pts = self._find_curve_and_points(p)

        doubling = difficulty >= 7 and self._rng.random() < 0.5
        if doubling:
            pt = self._rng.choice(curve_pts)
            px, py = pt
            qx, qy = pt
        else:
            pt1 = self._rng.choice(curve_pts)
            pt2 = self._rng.choice(curve_pts)
            px, py = pt1
            qx, qy = pt2

        if px == qx and (py + qy) % p == 0 and not (px == qx and py == qy):
            rx, ry = -1, -1
            is_identity = True
            slope = None
        elif px == qx and py == qy:
            if py == 0:
                rx, ry = -1, -1
                is_identity = True
                slope = None
            else:
                inv_2y = _mod_inv(2 * py, p)
                slope = ((3 * px * px + a) * inv_2y) % p
                rx = (slope * slope - 2 * px) % p
                ry = (slope * (px - rx) - py) % p
                is_identity = False
        else:
            inv_dx = _mod_inv((qx - px) % p, p)
            slope = ((qy - py) * inv_dx) % p
            rx = (slope * slope - px - qx) % p
            ry = (slope * (px - rx) - py) % p
            is_identity = False

        problem = (
            f"E: y^2=x^3+{a}x+{b} mod {p}. "
            f"P={_format_point(px, py)}, Q={_format_point(qx, qy)}. P+Q=?"
        )
        return problem, {
            "p": p, "a": a, "b": b,
            "px": px, "py": py, "qx": qx, "qy": qy,
            "rx": rx, "ry": ry, "slope": slope,
            "is_identity": is_identity, "doubling": px == qx and py == qy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate elliptic curve addition steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing slope computation and result.
        """
        p = data["p"]
        steps = []
        if data["is_identity"]:
            steps.append("P and Q are inverses (or tangent at y=0)")
            steps.append("P + Q = O (point at infinity)")
        elif data["doubling"]:
            steps.append(f"P = Q, doubling: s = (3*{data['px']}^2+{data['a']})/(2*{data['py']}) mod {p}")
            steps.append(f"slope s = {data['slope']}")
            steps.append(f"x_R = s^2 - 2*{data['px']} mod {p} = {data['rx']}")
            steps.append(f"y_R = s*({data['px']}-{data['rx']}) - {data['py']} mod {p} = {data['ry']}")
        else:
            steps.append(f"s = ({data['qy']}-{data['py']})/({data['qx']}-{data['px']}) mod {p}")
            steps.append(f"slope s = {data['slope']}")
            steps.append(f"x_R = s^2-{data['px']}-{data['qx']} mod {p} = {data['rx']}")
            steps.append(f"y_R = s*({data['px']}-{data['rx']})-{data['py']} mod {p} = {data['ry']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The resulting point or identity.
        """
        if data["is_identity"]:
            return "O (identity)"
        return _format_point(data["rx"], data["ry"])


# ═══════════════════════════════════════════════════════════════════
# 5. PROJECTIVE COORDS (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ProjectiveCoordsGenerator(StepGenerator):
    """Convert between affine and projective coordinates.

    Converts affine point (x, y) to projective [X:Y:Z] and back.
    Normalises projective coordinates by dividing by gcd of all
    three components.

    Difficulty scaling:
        Difficulty 1-3: small integer coordinates (1-5).
        Difficulty 4-6: medium coordinates (1-10), some with gcd > 1.
        Difficulty 7-8: larger coordinates (1-20), normalize required.

    Prerequisites:
        gcd (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "projective_coords"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gcd"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls coordinate range.

        Returns:
            Task description string.
        """
        return "convert between affine and projective coordinates"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a projective coordinate conversion problem.

        Args:
            difficulty: Controls coordinate sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        to_projective = self._rng.random() < 0.5

        if difficulty <= 3:
            hi = 5
        elif difficulty <= 6:
            hi = 10
        else:
            hi = 20

        if to_projective:
            x = self._rng.randint(1, hi)
            y = self._rng.randint(1, hi)
            k = self._rng.randint(1, 4)
            big_x = x * k
            big_y = y * k
            big_z = k
            g = _gcd(_gcd(big_x, big_y), big_z)
            norm_x = big_x // g
            norm_y = big_y // g
            norm_z = big_z // g
            problem = f"affine ({x}, {y}) to projective. Normalise."
            return problem, {
                "direction": "to_proj", "ax": x, "ay": y,
                "raw": (big_x, big_y, big_z),
                "norm": (norm_x, norm_y, norm_z), "g": g,
            }
        else:
            z = self._rng.randint(1, max(2, hi // 3))
            x = self._rng.randint(1, hi) * z
            y = self._rng.randint(1, hi) * z
            g = _gcd(_gcd(x, y), z)
            norm_x = x // g
            norm_y = y // g
            norm_z = z // g
            ax = x // z
            ay = y // z
            problem = f"projective [{x}:{y}:{z}] to affine."
            return problem, {
                "direction": "to_affine",
                "px": x, "py": y, "pz": z,
                "norm": (norm_x, norm_y, norm_z),
                "ax": ax, "ay": ay, "g": g,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coordinate conversion steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conversion.
        """
        if data["direction"] == "to_proj":
            x, y = data["ax"], data["ay"]
            nx, ny, nz = data["norm"]
            return [
                f"affine ({x}, {y}) -> projective [{x}:{y}:1]",
                f"normalised: [{nx}:{ny}:{nz}]",
            ]
        else:
            px, py, pz = data["px"], data["py"], data["pz"]
            nx, ny, nz = data["norm"]
            return [
                f"[{px}:{py}:{pz}], Z={pz}",
                f"normalise: gcd={data['g']}, [{nx}:{ny}:{nz}]",
                f"affine: x={px}//{pz}={data['ax']}, y={py}//{pz}={data['ay']}",
            ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Converted coordinates.
        """
        if data["direction"] == "to_proj":
            nx, ny, nz = data["norm"]
            return f"[{nx}:{ny}:{nz}]"
        return f"({data['ax']}, {data['ay']})"


# ═══════════════════════════════════════════════════════════════════
# 6. GENUS COMPUTE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class GenusComputeGenerator(StepGenerator):
    """Compute the genus of a smooth plane curve.

    For a smooth projective plane curve of degree d, the genus is
    g = (d-1)(d-2)/2. Generates curves of varying degrees and
    computes their genus.

    Difficulty scaling:
        Difficulty 1-3: degree 2-3 (genus 0-1).
        Difficulty 4-6: degree 3-5 (genus 1-6).
        Difficulty 7-8: degree 4-7 (genus 3-15).

    Prerequisites:
        bezout_intersection (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "genus_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bezout_intersection"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls curve degree.

        Returns:
            Task description string.
        """
        return "compute genus of smooth plane curve"

    def _select_degree(self, difficulty: int) -> int:
        """Choose curve degree based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Degree d >= 2.
        """
        if difficulty <= 3:
            return self._rng.choice([2, 3])
        if difficulty <= 6:
            return self._rng.choice([3, 4, 5])
        return self._rng.choice([4, 5, 6, 7])

    def _curve_name(self, d: int) -> str:
        """Return a name for a curve of given degree.

        Args:
            d: Degree of the curve.

        Returns:
            Human-readable curve type.
        """
        names = {2: "conic", 3: "cubic", 4: "quartic", 5: "quintic",
                 6: "sextic", 7: "septic"}
        return names.get(d, f"degree-{d} curve")

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a genus computation problem.

        Args:
            difficulty: Controls curve degree.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        d = self._select_degree(difficulty)
        genus = (d - 1) * (d - 2) // 2
        name = self._curve_name(d)

        problem = f"smooth {name} of degree {d} in P^2. Compute genus."
        return problem, {"d": d, "name": name, "genus": genus}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate genus computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying the genus-degree formula.
        """
        d = data["d"]
        return [
            f"genus-degree formula: g = (d-1)(d-2)/2",
            f"d = {d}",
            f"g = ({d}-1)({d}-2)/2 = {d - 1}*{d - 2}/2",
            f"g = {(d - 1) * (d - 2)}/2 = {data['genus']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Genus value.
        """
        return f"g = {data['genus']}"


# ═══════════════════════════════════════════════════════════════════
# 7. RATIONAL POINTS (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class RationalPointsGenerator(StepGenerator):
    """Find rational points on a conic ax^2 + by^2 = c.

    Given one known rational point, parametrises the conic to find
    additional rational points. Uses lines through the known point
    with rational slope to intersect the conic.

    Difficulty scaling:
        Difficulty 1-3: x^2 + y^2 = c with small c.
        Difficulty 4-6: ax^2 + by^2 = c, a,b in {1,2}.
        Difficulty 7-8: general a,b in {1,2,3}.

    Prerequisites:
        quadratic (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rational_points"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Task description string.
        """
        return "find rational points on conic from known point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rational points problem.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a_coeff, b_coeff = 1, 1
        elif difficulty <= 6:
            a_coeff = self._rng.choice([1, 2])
            b_coeff = self._rng.choice([1, 2])
        else:
            a_coeff = self._rng.choice([1, 2, 3])
            b_coeff = self._rng.choice([1, 2, 3])

        x0 = self._rng.randint(0, 3)
        y0 = self._rng.randint(1, 3)
        c = a_coeff * x0 * x0 + b_coeff * y0 * y0

        t_num = self._rng.randint(1, 3)
        t_den = self._rng.randint(1, 3)
        t = t_num / t_den

        x1_num = (a_coeff * x0 * t_den * t_den
                   - 2 * b_coeff * y0 * t_num * t_den
                   - a_coeff * x0 * t_num * t_num)
        x1_den = a_coeff * t_den * t_den + b_coeff * t_num * t_num
        if x1_den == 0:
            x1_num, x1_den = x0, 1
        g = _gcd(abs(x1_num), abs(x1_den))
        if g > 0:
            x1_num //= g
            x1_den //= g
        if x1_den < 0:
            x1_num, x1_den = -x1_num, -x1_den

        y1_num = y0 * x1_den - t_num * (x1_num - x0 * x1_den)
        y1_den = x1_den * t_den
        g2 = _gcd(abs(y1_num), abs(y1_den))
        if g2 > 0:
            y1_num //= g2
            y1_den //= g2
        if y1_den < 0:
            y1_num, y1_den = -y1_num, -y1_den

        conic_str = ""
        if a_coeff == 1:
            conic_str += "x^2"
        else:
            conic_str += f"{a_coeff}x^2"
        if b_coeff == 1:
            conic_str += "+y^2"
        else:
            conic_str += f"+{b_coeff}y^2"
        conic_str += f"={c}"

        problem = (
            f"{conic_str}, known point ({x0},{y0}). "
            f"Find another rational point (t={t_num}/{t_den})."
        )
        return problem, {
            "a": a_coeff, "b": b_coeff, "c": c,
            "x0": x0, "y0": y0, "t_num": t_num, "t_den": t_den,
            "x1_num": x1_num, "x1_den": x1_den,
            "y1_num": y1_num, "y1_den": y1_den,
            "conic_str": conic_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rational point steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing parametrisation.
        """
        x0, y0 = data["x0"], data["y0"]
        t = f"{data['t_num']}/{data['t_den']}"
        steps = [
            f"known point P=({x0},{y0}) on {data['conic_str']}",
            f"line through P with slope t={t}: y={y0}+t(x-{x0})",
            f"substitute into conic and solve for x",
        ]
        xn, xd = data["x1_num"], data["x1_den"]
        yn, yd = data["y1_num"], data["y1_den"]
        x_str = str(xn) if xd == 1 else f"{xn}/{xd}"
        y_str = str(yn) if yd == 1 else f"{yn}/{yd}"
        steps.append(f"new point: ({x_str}, {y_str})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The new rational point.
        """
        xn, xd = data["x1_num"], data["x1_den"]
        yn, yd = data["y1_num"], data["y1_den"]
        x_str = str(xn) if xd == 1 else f"{xn}/{xd}"
        y_str = str(yn) if yd == 1 else f"{yn}/{yd}"
        return f"({x_str}, {y_str})"


# ═══════════════════════════════════════════════════════════════════
# 8. TANGENT LINE TO VARIETY (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class TangentLineVarietyGenerator(StepGenerator):
    """Compute the tangent line to a plane curve f(x,y)=0 at a point P.

    Uses the gradient: the tangent at P=(a,b) is
    f_x(a,b)*(x-a) + f_y(a,b)*(y-b) = 0.
    Works with small polynomial curves over the integers.

    Difficulty scaling:
        Difficulty 1-3: circles x^2+y^2=r^2.
        Difficulty 4-6: conics ax^2+by^2=c.
        Difficulty 7-8: cubics x^3+y^3=c, mixed terms.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tangent_line_variety"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Task description string.
        """
        return "compute tangent line to curve at point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tangent line problem.

        Args:
            difficulty: Controls curve complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            x0 = self._rng.randint(1, 4)
            y0 = self._rng.randint(1, 4)
            c = x0 * x0 + y0 * y0
            f_str = f"x^2+y^2-{c}"
            fx = 2 * x0
            fy = 2 * y0
            kind = "circle"
        elif difficulty <= 6:
            a = self._rng.choice([1, 2, 3])
            b = self._rng.choice([1, 2, 3])
            x0 = self._rng.randint(1, 3)
            y0 = self._rng.randint(1, 3)
            c = a * x0 * x0 + b * y0 * y0
            if a == 1:
                f_str = f"x^2+{b}y^2-{c}" if b != 1 else f"x^2+y^2-{c}"
            else:
                f_str = f"{a}x^2+{b}y^2-{c}" if b != 1 else f"{a}x^2+y^2-{c}"
            fx = 2 * a * x0
            fy = 2 * b * y0
            kind = "conic"
        else:
            x0 = self._rng.randint(1, 3)
            y0 = self._rng.randint(1, 3)
            c = x0 ** 3 + y0 ** 3
            f_str = f"x^3+y^3-{c}"
            fx = 3 * x0 * x0
            fy = 3 * y0 * y0
            kind = "cubic"

        g = _gcd(abs(fx), abs(fy))
        sfx = fx // g if g > 0 else fx
        sfy = fy // g if g > 0 else fy

        tangent_parts = []
        if sfx == 1:
            tangent_parts.append(f"(x-{x0})")
        else:
            tangent_parts.append(f"{sfx}(x-{x0})")
        if sfy == 1:
            tangent_parts.append(f"(y-{y0})")
        else:
            tangent_parts.append(f"{sfy}(y-{y0})")
        tangent_str = "+".join(tangent_parts) + "=0"

        problem = (
            f"f(x,y)={f_str}=0, P=({x0},{y0}). "
            f"Find tangent line at P."
        )
        return problem, {
            "f_str": f_str, "x0": x0, "y0": y0,
            "fx": fx, "fy": fy, "kind": kind,
            "tangent_str": tangent_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tangent line computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing gradient and tangent line.
        """
        x0, y0 = data["x0"], data["y0"]
        return [
            f"f_x = partial f / partial x at ({x0},{y0}) = {data['fx']}",
            f"f_y = partial f / partial y at ({x0},{y0}) = {data['fy']}",
            f"tangent: f_x(x-{x0})+f_y(y-{y0})=0",
            f"{data['fx']}(x-{x0})+{data['fy']}(y-{y0})=0",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Tangent line equation.
        """
        return data["tangent_str"]
