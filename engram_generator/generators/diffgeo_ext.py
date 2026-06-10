"""Extended differential geometry generators for tiers 5-7.

6 generators covering Frenet-Serret frames, surface normals, first and
second fundamental forms, mean curvature, and parallel transport. Each
produces step-by-step solutions with LaTeX formatting.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


# ── Helper classes ──────────────────────────────────────────────────


class HelixCurve:
    """A helix r(t) = (a*cos t, a*sin t, b*t) in 3D.

    Provides position, velocity, acceleration, and derived quantities
    for Frenet-Serret frame computation.

    Attributes:
        a: Radius of the helix.
        b: Pitch parameter (rise per radian).
    """

    def __init__(self, a: float, b: float) -> None:
        """Initialise the helix.

        Args:
            a: Radius (positive).
            b: Pitch parameter.
        """
        self._a = a
        self._b = b

    @property
    def a(self) -> float:
        """Return the helix radius."""
        return self._a

    @property
    def b(self) -> float:
        """Return the pitch parameter."""
        return self._b

    def position(self, t: float) -> tuple[float, float, float]:
        """Evaluate r(t).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (x, y, z).
        """
        return (self._a * math.cos(t),
                self._a * math.sin(t),
                self._b * t)

    def velocity(self, t: float) -> tuple[float, float, float]:
        """Evaluate r'(t).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (x', y', z').
        """
        return (-self._a * math.sin(t),
                self._a * math.cos(t),
                self._b)

    def acceleration(self, t: float) -> tuple[float, float, float]:
        """Evaluate r''(t).

        Args:
            t: Parameter value.

        Returns:
            Tuple of (x'', y'', z'').
        """
        return (-self._a * math.cos(t),
                -self._a * math.sin(t),
                0.0)

    def speed(self, t: float) -> float:
        """Compute |r'(t)|.

        Args:
            t: Parameter value.

        Returns:
            Speed (magnitude of velocity).
        """
        vx, vy, vz = self.velocity(t)
        return math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

    def curvature(self) -> float:
        """Compute curvature kappa = a / (a^2 + b^2).

        Returns:
            Curvature value (constant for a helix).
        """
        return self._a / (self._a ** 2 + self._b ** 2)

    def torsion(self) -> float:
        """Compute torsion tau = b / (a^2 + b^2).

        Returns:
            Torsion value (constant for a helix).
        """
        return self._b / (self._a ** 2 + self._b ** 2)

    def latex(self) -> str:
        """Format the helix as LaTeX.

        Returns:
            LaTeX string.
        """
        return f"({_fmt(self._a)}\\cos t, {_fmt(self._a)}\\sin t, {_fmt(self._b)}t)"


class ParametricSurface:
    """A parametric surface r(u, v) with analytic partial derivatives.

    Supports sphere and cylinder families used by surface normal and
    fundamental form generators.

    Attributes:
        kind: Surface type identifier.
        params: Numeric parameters controlling the surface.
    """

    def __init__(self, kind: str, params: tuple) -> None:
        """Initialise the parametric surface.

        Args:
            kind: Surface type ('sphere', 'cylinder', 'cone', 'paraboloid').
            params: Numeric parameters specific to the surface type.
        """
        self._kind = kind
        self._params = params

    @property
    def kind(self) -> str:
        """Return the surface type."""
        return self._kind

    def position(self, u: float, v: float) -> tuple[float, float, float]:
        """Evaluate r(u, v).

        Args:
            u: First parameter.
            v: Second parameter.

        Returns:
            Tuple of (x, y, z).
        """
        if self._kind == "sphere":
            r = self._params[0]
            return (r * math.sin(u) * math.cos(v),
                    r * math.sin(u) * math.sin(v),
                    r * math.cos(u))
        if self._kind == "cylinder":
            r = self._params[0]
            return (r * math.cos(v), r * math.sin(v), u)
        if self._kind == "cone":
            # r(u, v) = (u*cos v, u*sin v, u)
            return (u * math.cos(v), u * math.sin(v), u)
        # paraboloid: r(u,v) = (u*cos v, u*sin v, u^2)
        return (u * math.cos(v), u * math.sin(v), u ** 2)

    def r_u(self, u: float, v: float) -> tuple[float, float, float]:
        """Evaluate dr/du.

        Args:
            u: First parameter.
            v: Second parameter.

        Returns:
            Tuple of partial derivatives w.r.t. u.
        """
        if self._kind == "sphere":
            r = self._params[0]
            return (r * math.cos(u) * math.cos(v),
                    r * math.cos(u) * math.sin(v),
                    -r * math.sin(u))
        if self._kind == "cylinder":
            return (0.0, 0.0, 1.0)
        if self._kind == "cone":
            return (math.cos(v), math.sin(v), 1.0)
        # paraboloid
        return (math.cos(v), math.sin(v), 2.0 * u)

    def r_v(self, u: float, v: float) -> tuple[float, float, float]:
        """Evaluate dr/dv.

        Args:
            u: First parameter.
            v: Second parameter.

        Returns:
            Tuple of partial derivatives w.r.t. v.
        """
        if self._kind == "sphere":
            r = self._params[0]
            return (-r * math.sin(u) * math.sin(v),
                    r * math.sin(u) * math.cos(v),
                    0.0)
        if self._kind == "cylinder":
            r = self._params[0]
            return (-r * math.sin(v), r * math.cos(v), 0.0)
        if self._kind == "cone":
            return (-u * math.sin(v), u * math.cos(v), 0.0)
        # paraboloid
        return (-u * math.sin(v), u * math.cos(v), 0.0)

    def latex(self) -> str:
        """Format the surface as LaTeX.

        Returns:
            LaTeX string.
        """
        if self._kind == "sphere":
            r = self._params[0]
            return (f"({_fmt(r)}\\sin u\\cos v, "
                    f"{_fmt(r)}\\sin u\\sin v, "
                    f"{_fmt(r)}\\cos u)")
        if self._kind == "cylinder":
            r = self._params[0]
            return f"({_fmt(r)}\\cos v, {_fmt(r)}\\sin v, u)"
        if self._kind == "cone":
            return "(u\\cos v, u\\sin v, u)"
        return "(u\\cos v, u\\sin v, u^2)"


def _cross(a: tuple[float, float, float],
           b: tuple[float, float, float]) -> tuple[float, float, float]:
    """Compute cross product a x b.

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Cross product vector.
    """
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _dot(a: tuple[float, float, float],
         b: tuple[float, float, float]) -> float:
    """Compute dot product a . b.

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Scalar dot product.
    """
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a: tuple[float, float, float]) -> float:
    """Compute |a|.

    Args:
        a: Vector.

    Returns:
        Euclidean norm.
    """
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def _normalize(a: tuple[float, float, float]) -> tuple[float, float, float]:
    """Normalise a vector to unit length.

    Args:
        a: Vector (must be non-zero).

    Returns:
        Unit vector in the same direction.
    """
    n = _norm(a)
    if n < 1e-12:
        return (0.0, 0.0, 0.0)
    return (a[0] / n, a[1] / n, a[2] / n)


def _fmt3(v: tuple[float, float, float]) -> str:
    """Format a 3-vector as a string.

    Args:
        v: 3-tuple of floats.

    Returns:
        Formatted string.
    """
    return f"({_fmt(v[0])}, {_fmt(v[1])}, {_fmt(v[2])})"


# ── 1. Frenet-Serret frame (tier 6) ───────────────────────────────


@register
class FrenetSerretGenerator(StepGenerator):
    """Compute the Frenet-Serret frame (T, N, B) and curvature/torsion for a helix.

    For a helix r(t) = (a*cos t, a*sin t, b*t), computes the unit
    tangent T, principal normal N, binormal B = T x N, curvature
    kappa = a/(a^2+b^2), and torsion tau = b/(a^2+b^2).

    Input format:
        ``compute Frenet-Serret frame for helix``

    Target format:
        ``r(t) = (2cos t, 2sin t, t) at t=1 <step>
        r' = (-2sin 1, 2cos 1, 1) <step>
        |r'| = sqrt(5) <step> T = r'/|r'| <step>
        r'' = (-2cos 1, -2sin 1, 0) <step>
        kappa = 2/5 <step> tau = 1/5 <step>
        N = (-cos 1, -sin 1, 0) <step> B = T x N``

    Difficulty scaling:
        Difficulty 1-3: integer a, b=1.
        Difficulty 4-6: larger a and b.
        Difficulty 7-8: non-integer ratios.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "frenet_serret"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls helix parameters.

        Returns:
            Natural language description.
        """
        return "compute Frenet-Serret frame (T, N, B), curvature, and torsion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Frenet-Serret frame problem.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (helix_description, solution_data).
        """
        a = float(self._rng.randint(1, 2 + difficulty))
        b = float(self._rng.randint(1, 1 + difficulty))
        helix = HelixCurve(a, b)
        t = self._rng.choice([0.0, 0.5, 1.0, 1.5, 2.0])

        vel = helix.velocity(t)
        spd = helix.speed(t)
        tangent = _normalize(vel)

        acc = helix.acceleration(t)
        kappa = helix.curvature()
        tau = helix.torsion()

        # N = (r'' - (r''.T)*T) / |r'' - (r''.T)*T|
        # For helix: N = (-cos t, -sin t, 0)
        normal = _normalize((-math.cos(t), -math.sin(t), 0.0))
        binormal = _cross(tangent, normal)

        problem = f"Frenet-Serret: r(t)={helix.latex()}, t={_fmt(t)}"
        return problem, {
            "helix": helix, "t": t,
            "vel": vel, "speed": spd,
            "tangent": tangent, "normal": normal, "binormal": binormal,
            "kappa": kappa, "tau": tau,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Frenet-Serret computation steps.

        Args:
            data: Solution data with frame vectors.

        Returns:
            Steps showing velocity, T, N, B, kappa, tau.
        """
        return [
            f"r'={_fmt3(data['vel'])}",
            f"|r'|={_fmt(data['speed'])}",
            f"T={_fmt3(data['tangent'])}",
            f"kappa={_fmt(data['kappa'])}",
            f"tau={_fmt(data['tau'])}",
            f"N={_fmt3(data['normal'])}",
            f"B=TxN={_fmt3(data['binormal'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return curvature and torsion.

        Args:
            data: Solution data.

        Returns:
            Formatted kappa and tau.
        """
        return f"kappa={_fmt(data['kappa'])}, tau={_fmt(data['tau'])}"


# ── 2. Surface normal (tier 5) ────────────────────────────────────


@register
class SurfaceNormalGenerator(StepGenerator):
    """Compute the unit normal N = (r_u x r_v) / |r_u x r_v| for a parametric surface.

    Evaluates partial derivatives r_u and r_v at a given point, takes
    their cross product, and normalises to get the unit surface normal.

    Input format:
        ``compute surface normal at point``

    Target format:
        ``r(u,v) = (R sin u cos v, R sin u sin v, R cos u) at (pi/4, 0)
        <step> r_u = (R cos u cos v, R cos u sin v, -R sin u) <step>
        r_v = (-R sin u sin v, R sin u cos v, 0) <step>
        r_u x r_v = (...) <step> |r_u x r_v| = R^2 sin u <step>
        N = (sin u cos v, sin u sin v, cos u)``

    Difficulty scaling:
        Difficulty 1-3: sphere with easy angles.
        Difficulty 4-6: cylinder.
        Difficulty 7-8: cone or paraboloid.

    Prerequisites:
        cross_product.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "surface_normal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cross_product"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls surface type.

        Returns:
            Natural language description.
        """
        return "compute unit surface normal at given point"

    def _choose_surface(self, difficulty: int) -> ParametricSurface:
        """Select a surface appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A ParametricSurface instance.
        """
        if difficulty <= 3:
            r = float(self._rng.randint(1, 4))
            return ParametricSurface("sphere", (r,))
        if difficulty <= 6:
            r = float(self._rng.randint(1, 4))
            return ParametricSurface("cylinder", (r,))
        kind = self._rng.choice(["cone", "paraboloid"])
        return ParametricSurface(kind, ())

    def _choose_point(self, surface: ParametricSurface) -> tuple[float, float]:
        """Choose a parameter point avoiding singularities.

        Args:
            surface: The parametric surface.

        Returns:
            Tuple of (u, v).
        """
        if surface.kind == "sphere":
            u = self._rng.choice([0.5, 1.0, 1.5])
            v = self._rng.choice([0.0, 0.5, 1.0, 1.5])
            return u, v
        if surface.kind == "cylinder":
            u = float(self._rng.randint(0, 3))
            v = self._rng.choice([0.0, 0.5, 1.0, 1.5])
            return u, v
        # cone/paraboloid: avoid u=0
        u = self._rng.choice([0.5, 1.0, 1.5, 2.0])
        v = self._rng.choice([0.0, 0.5, 1.0, 1.5])
        return u, v

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a surface normal computation problem.

        Args:
            difficulty: Controls surface type.

        Returns:
            Tuple of (surface_description, solution_data).
        """
        surface = self._choose_surface(difficulty)
        u, v = self._choose_point(surface)

        ru = surface.r_u(u, v)
        rv = surface.r_v(u, v)
        cross = _cross(ru, rv)
        cross_norm = _norm(cross)
        normal = _normalize(cross)

        problem = (f"N: r(u,v)={surface.latex()}, "
                   f"(u,v)=({_fmt(u)},{_fmt(v)})")
        return problem, {
            "surface": surface, "u": u, "v": v,
            "ru": ru, "rv": rv,
            "cross": cross, "cross_norm": cross_norm,
            "normal": normal,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate surface normal computation steps.

        Args:
            data: Solution data with partial derivatives and normal.

        Returns:
            Steps showing r_u, r_v, cross product, normalisation.
        """
        return [
            f"r_u={_fmt3(data['ru'])}",
            f"r_v={_fmt3(data['rv'])}",
            f"r_u x r_v={_fmt3(data['cross'])}",
            f"|r_u x r_v|={_fmt(data['cross_norm'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the unit normal vector.

        Args:
            data: Solution data.

        Returns:
            Formatted unit normal.
        """
        return f"N={_fmt3(data['normal'])}"


# ── 3. First fundamental form (tier 6) ────────────────────────────


@register
class FirstFundamentalFormGenerator(StepGenerator):
    """Compute first fundamental form coefficients E, F, G.

    I = E*du^2 + 2F*du*dv + G*dv^2 where E = r_u . r_u,
    F = r_u . r_v, G = r_v . r_v. Evaluates at a given point.

    Input format:
        ``compute first fundamental form coefficients``

    Target format:
        ``r(u,v) = sphere of radius 3 at (pi/4, 0) <step>
        r_u = (...), r_v = (...) <step>
        E = r_u . r_u = 9 <step> F = r_u . r_v = 0 <step>
        G = r_v . r_v = 4.5 <step>
        I = 9 du^2 + 0 du dv + 4.5 dv^2``

    Difficulty scaling:
        Difficulty 1-3: sphere (F=0).
        Difficulty 4-6: cylinder (F=0).
        Difficulty 7-8: paraboloid (F may be non-zero).

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "first_fundamental_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls surface type.

        Returns:
            Natural language description.
        """
        return "compute first fundamental form coefficients E, F, G"

    def _choose_surface(self, difficulty: int) -> ParametricSurface:
        """Select a surface for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A ParametricSurface instance.
        """
        if difficulty <= 3:
            r = float(self._rng.randint(1, 4))
            return ParametricSurface("sphere", (r,))
        if difficulty <= 6:
            r = float(self._rng.randint(1, 4))
            return ParametricSurface("cylinder", (r,))
        return ParametricSurface(self._rng.choice(["cone", "paraboloid"]), ())

    def _choose_point(self, surface: ParametricSurface) -> tuple[float, float]:
        """Choose a parameter point.

        Args:
            surface: The parametric surface.

        Returns:
            Tuple of (u, v).
        """
        if surface.kind == "sphere":
            u = self._rng.choice([0.5, 1.0, 1.5])
            v = self._rng.choice([0.0, 0.5, 1.0])
        elif surface.kind == "cylinder":
            u = float(self._rng.randint(0, 3))
            v = self._rng.choice([0.0, 0.5, 1.0])
        else:
            u = self._rng.choice([0.5, 1.0, 1.5, 2.0])
            v = self._rng.choice([0.0, 0.5, 1.0])
        return u, v

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a first fundamental form problem.

        Args:
            difficulty: Controls surface type.

        Returns:
            Tuple of (surface_description, solution_data).
        """
        surface = self._choose_surface(difficulty)
        u, v = self._choose_point(surface)

        ru = surface.r_u(u, v)
        rv = surface.r_v(u, v)

        big_e = round(_dot(ru, ru), 4)
        big_f = round(_dot(ru, rv), 4)
        big_g = round(_dot(rv, rv), 4)

        problem = (f"I: r(u,v)={surface.latex()}, "
                   f"(u,v)=({_fmt(u)},{_fmt(v)})")
        return problem, {
            "surface": surface, "u": u, "v": v,
            "ru": ru, "rv": rv,
            "E": big_e, "F": big_f, "G": big_g,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate first fundamental form computation steps.

        Args:
            data: Solution data with E, F, G.

        Returns:
            Steps showing dot products.
        """
        return [
            f"r_u={_fmt3(data['ru'])}",
            f"r_v={_fmt3(data['rv'])}",
            f"E = r_u.r_u = {_fmt(data['E'])}",
            f"F = r_u.r_v = {_fmt(data['F'])}",
            f"G = r_v.r_v = {_fmt(data['G'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the first fundamental form.

        Args:
            data: Solution data.

        Returns:
            Formatted I = E du^2 + 2F du dv + G dv^2.
        """
        return f"E={_fmt(data['E'])}, F={_fmt(data['F'])}, G={_fmt(data['G'])}"


# ── 4. Second fundamental form (tier 7) ──────────────────────────


@register
class SecondFundamentalFormGenerator(StepGenerator):
    """Compute second fundamental form coefficients e, f, g.

    II = e*du^2 + 2f*du*dv + g*dv^2 where e = r_uu . N,
    f = r_uv . N, g = r_vv . N, and N is the unit surface normal.

    For simplicity, uses surfaces where second derivatives can be
    computed analytically: sphere and cylinder.

    Input format:
        ``compute second fundamental form coefficients``

    Target format:
        ``sphere of radius R at (u, v) <step>
        N = (sin u cos v, sin u sin v, cos u) <step>
        r_uu = (...), r_uv = (...), r_vv = (...) <step>
        e = r_uu.N = -R, f = r_uv.N = 0, g = r_vv.N = -R sin^2 u``

    Difficulty scaling:
        Difficulty 1-3: sphere (constant principal curvatures).
        Difficulty 4-6: cylinder (one zero curvature direction).
        Difficulty 7-8: paraboloid.

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "second_fundamental_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls surface type.

        Returns:
            Natural language description.
        """
        return "compute second fundamental form coefficients e, f, g"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a second fundamental form problem.

        Computes r_uu, r_uv, r_vv analytically for known surfaces,
        then dots with the unit normal N.

        Args:
            difficulty: Controls surface type.

        Returns:
            Tuple of (surface_description, solution_data).
        """
        if difficulty <= 4:
            return self._sphere_problem(difficulty)
        if difficulty <= 6:
            return self._cylinder_problem(difficulty)
        return self._paraboloid_problem(difficulty)

    def _sphere_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate second fundamental form for a sphere.

        For sphere r(u,v) = (R sin u cos v, R sin u sin v, R cos u):
        e = -R, f = 0, g = -R sin^2 u.

        Args:
            difficulty: Controls radius.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        big_r = float(self._rng.randint(1, 3 + difficulty))
        u = self._rng.choice([0.5, 1.0, 1.5])
        v = self._rng.choice([0.0, 0.5, 1.0])

        # Analytic results for sphere
        small_e = round(-big_r, 4)
        small_f = 0.0
        small_g = round(-big_r * math.sin(u) ** 2, 4)
        normal = (math.sin(u) * math.cos(v),
                  math.sin(u) * math.sin(v),
                  math.cos(u))

        surface = ParametricSurface("sphere", (big_r,))
        problem = (f"II: r(u,v)={surface.latex()}, "
                   f"(u,v)=({_fmt(u)},{_fmt(v)})")
        return problem, {
            "surface_kind": "sphere", "R": big_r, "u": u, "v": v,
            "normal": normal,
            "e": small_e, "f": small_f, "g": small_g,
        }

    def _cylinder_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate second fundamental form for a cylinder.

        For cylinder r(u,v) = (R cos v, R sin v, u):
        e = 0, f = 0, g = -R.

        Args:
            difficulty: Controls radius.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        big_r = float(self._rng.randint(1, 3 + difficulty))
        u = float(self._rng.randint(0, 3))
        v = self._rng.choice([0.0, 0.5, 1.0, 1.5])

        small_e = 0.0
        small_f = 0.0
        small_g = round(-big_r, 4)
        normal = (math.cos(v), math.sin(v), 0.0)

        surface = ParametricSurface("cylinder", (big_r,))
        problem = (f"II: r(u,v)={surface.latex()}, "
                   f"(u,v)=({_fmt(u)},{_fmt(v)})")
        return problem, {
            "surface_kind": "cylinder", "R": big_r, "u": u, "v": v,
            "normal": normal,
            "e": small_e, "f": small_f, "g": small_g,
        }

    def _paraboloid_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate second fundamental form for a paraboloid.

        For r(u,v) = (u cos v, u sin v, u^2):
        r_uu = (0, 0, 2), r_uv = (-sin v, cos v, 0),
        r_vv = (-u cos v, -u sin v, 0).

        Args:
            difficulty: Controls parameter values.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        u = self._rng.choice([0.5, 1.0, 1.5, 2.0])
        v = self._rng.choice([0.0, 0.5, 1.0])

        surface = ParametricSurface("paraboloid", ())
        ru = surface.r_u(u, v)
        rv = surface.r_v(u, v)
        cross = _cross(ru, rv)
        normal = _normalize(cross)

        # Second derivatives for paraboloid
        r_uu = (0.0, 0.0, 2.0)
        r_uv = (-math.sin(v), math.cos(v), 0.0)
        r_vv = (-u * math.cos(v), -u * math.sin(v), 0.0)

        small_e = round(_dot(r_uu, normal), 4)
        small_f = round(_dot(r_uv, normal), 4)
        small_g = round(_dot(r_vv, normal), 4)

        problem = (f"II: r(u,v)={surface.latex()}, "
                   f"(u,v)=({_fmt(u)},{_fmt(v)})")
        return problem, {
            "surface_kind": "paraboloid", "u": u, "v": v,
            "normal": normal,
            "e": small_e, "f": small_f, "g": small_g,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate second fundamental form steps.

        Args:
            data: Solution data with coefficients.

        Returns:
            Steps showing normal and coefficients.
        """
        return [
            f"N={_fmt3(data['normal'])}",
            f"e = r_uu.N = {_fmt(data['e'])}",
            f"f = r_uv.N = {_fmt(data['f'])}",
            f"g = r_vv.N = {_fmt(data['g'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the second fundamental form coefficients.

        Args:
            data: Solution data.

        Returns:
            Formatted e, f, g.
        """
        return f"e={_fmt(data['e'])}, f={_fmt(data['f'])}, g={_fmt(data['g'])}"


# ── 5. Mean curvature (tier 7) ───────────────────────────────────


@register
class MeanCurvatureGenerator(StepGenerator):
    """Compute mean curvature H from fundamental form coefficients.

    H = (eG - 2fF + gE) / (2(EG - F^2)). Generates random first and
    second fundamental form coefficients and computes H.

    Input format:
        ``compute mean curvature from fundamental forms``

    Target format:
        ``I: E=1, F=0, G=4; II: e=2, f=0, g=-1 <step>
        EG - F^2 = 4 <step> eG - 2fF + gE = 2*4 - 0 + (-1)*1 = 7
        <step> H = 7 / (2*4) = 0.875``

    Difficulty scaling:
        Difficulty 1-3: F=0, f=0 (simple).
        Difficulty 4-6: F=0, f non-zero.
        Difficulty 7-8: general coefficients.

    Prerequisites:
        christoffel_symbol.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mean_curvature"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["christoffel_symbol"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Natural language description.
        """
        return "compute mean curvature from fundamental form coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mean curvature problem.

        Generates valid fundamental form coefficients (EG - F^2 > 0)
        and computes H = (eG - 2fF + gE) / (2(EG - F^2)).

        Args:
            difficulty: Controls coefficient ranges.

        Returns:
            Tuple of (coefficients_description, solution_data).
        """
        for _ in range(100):
            if difficulty <= 3:
                big_e = float(self._rng.randint(1, 4))
                big_f = 0.0
                big_g = float(self._rng.randint(1, 4))
                small_e = float(self._rng.randint(-3, 3))
                small_f = 0.0
                small_g = float(self._rng.randint(-3, 3))
            elif difficulty <= 6:
                big_e = float(self._rng.randint(1, 5))
                big_f = 0.0
                big_g = float(self._rng.randint(1, 5))
                small_e = float(self._rng.randint(-3, 3))
                small_f = float(self._rng.randint(-2, 2))
                small_g = float(self._rng.randint(-3, 3))
            else:
                big_e = float(self._rng.randint(1, 6))
                big_f = float(self._rng.randint(-2, 2))
                big_g = float(self._rng.randint(1, 6))
                small_e = float(self._rng.randint(-4, 4))
                small_f = float(self._rng.randint(-3, 3))
                small_g = float(self._rng.randint(-4, 4))

            denom = big_e * big_g - big_f ** 2
            if denom > 0:
                break
        else:
            big_e, big_f, big_g = 1.0, 0.0, 1.0
            small_e, small_f, small_g = 1.0, 0.0, -1.0
            denom = 1.0

        numerator = small_e * big_g - 2 * small_f * big_f + small_g * big_e
        mean_h = round(numerator / (2 * denom), 4)

        problem = (f"I: E={_fmt(big_e)}, F={_fmt(big_f)}, G={_fmt(big_g)}; "
                   f"II: e={_fmt(small_e)}, f={_fmt(small_f)}, g={_fmt(small_g)}")
        return problem, {
            "E": big_e, "F": big_f, "G": big_g,
            "e": small_e, "f": small_f, "g": small_g,
            "denom": denom, "numerator": numerator,
            "H": mean_h,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean curvature computation steps.

        Args:
            data: Solution data with coefficients and curvature.

        Returns:
            Steps showing the computation.
        """
        return [
            f"EG - F^2 = {_fmt(data['E'])}*{_fmt(data['G'])} - "
            f"{_fmt(data['F'])}^2 = {_fmt(data['denom'])}",
            f"eG - 2fF + gE = {_fmt(data['e'])}*{_fmt(data['G'])} - "
            f"2*{_fmt(data['f'])}*{_fmt(data['F'])} + "
            f"{_fmt(data['g'])}*{_fmt(data['E'])} = {_fmt(data['numerator'])}",
            f"H = {_fmt(data['numerator'])} / (2*{_fmt(data['denom'])}) = {_fmt(data['H'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mean curvature.

        Args:
            data: Solution data.

        Returns:
            Formatted H value.
        """
        return f"H={_fmt(data['H'])}"


# ── 6. Parallel transport (tier 7) ───────────────────────────────


@register
class ParallelTransportGenerator(StepGenerator):
    """Transport a vector along a curve on a surface using Christoffel symbols.

    Computes the change in vector components via
    dV^i = -Gamma^i_{jk} V^j dx^k for one discrete step. Uses simple
    Christoffel symbol values and a small step along one coordinate.

    Input format:
        ``parallel transport vector along curve``

    Target format:
        ``V = (V1, V2) at point, step dx^1 = h <step>
        Gamma^1_{11} = a, Gamma^1_{12} = b, ... <step>
        dV^1 = -(a*V1 + b*V2)*h <step>
        dV^2 = -(c*V1 + d*V2)*h <step>
        V_new = (V1 + dV1, V2 + dV2)``

    Difficulty scaling:
        Difficulty 1-3: step along x^1 only, few non-zero Gammas.
        Difficulty 4-6: step along x^2, more Gammas.
        Difficulty 7-8: step in both directions.

    Prerequisites:
        christoffel_symbol.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parallel_transport"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["christoffel_symbol"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls transport complexity.

        Returns:
            Natural language description.
        """
        return "parallel transport vector along curve on surface"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a parallel transport problem.

        Creates Christoffel symbol values, initial vector, and step
        direction, then computes the transported vector.

        Args:
            difficulty: Controls number of non-zero symbols and step direction.

        Returns:
            Tuple of (transport_description, solution_data).
        """
        v1 = round(self._rng.uniform(0.5, 3.0), 2)
        v2 = round(self._rng.uniform(0.5, 3.0), 2)
        h = round(self._rng.choice([0.1, 0.2, 0.5]), 4)

        # Generate Christoffel symbols
        gamma_values = [0.5, 1.0, -0.5, -1.0, 0.25, -0.25, 0.0, 0.0]
        self._rng.shuffle(gamma_values)

        gammas = {
            "1_11": gamma_values[0], "1_12": gamma_values[1],
            "1_22": gamma_values[2], "2_11": gamma_values[3],
            "2_12": gamma_values[4], "2_22": gamma_values[5],
        }

        if difficulty <= 3:
            # Step along x^1 only
            dx1, dx2 = h, 0.0
            # Zero out most gammas
            gammas["1_22"] = 0.0
            gammas["2_22"] = 0.0
            gammas["1_12"] = 0.0
            gammas["2_12"] = 0.0
        elif difficulty <= 6:
            # Step along x^2 only
            dx1, dx2 = 0.0, h
            gammas["1_11"] = 0.0
            gammas["2_11"] = 0.0
        else:
            # Step in both directions
            dx1, dx2 = h, h

        # dV^i = -sum_jk Gamma^i_jk V^j dx^k
        dv1 = -(gammas["1_11"] * v1 * dx1 + gammas["1_12"] * v1 * dx2 +
                 gammas["1_12"] * v2 * dx1 + gammas["1_22"] * v2 * dx2)
        dv2 = -(gammas["2_11"] * v1 * dx1 + gammas["2_12"] * v1 * dx2 +
                 gammas["2_12"] * v2 * dx1 + gammas["2_22"] * v2 * dx2)

        dv1 = round(dv1, 4)
        dv2 = round(dv2, 4)
        v1_new = round(v1 + dv1, 4)
        v2_new = round(v2 + dv2, 4)

        nonzero_gammas = {k: v for k, v in gammas.items() if abs(v) > 1e-10}
        gamma_str = ", ".join(f"G^{k}={_fmt(v)}" for k, v in nonzero_gammas.items())

        problem = (f"V=({_fmt(v1)},{_fmt(v2)}), "
                   f"dx=({_fmt(dx1)},{_fmt(dx2)}); {gamma_str}")
        return problem, {
            "v1": v1, "v2": v2,
            "dx1": dx1, "dx2": dx2,
            "gammas": gammas,
            "dv1": dv1, "dv2": dv2,
            "v1_new": v1_new, "v2_new": v2_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate parallel transport computation steps.

        Args:
            data: Solution data with vector changes.

        Returns:
            Steps showing dV^i computation and result.
        """
        nonzero = {k: v for k, v in data["gammas"].items() if abs(v) > 1e-10}
        steps = [f"Gamma: {', '.join(f'G^{k}={_fmt(v)}' for k, v in nonzero.items())}"]
        steps.append(f"dV^1 = {_fmt(data['dv1'])}")
        steps.append(f"dV^2 = {_fmt(data['dv2'])}")
        steps.append(
            f"V_new = ({_fmt(data['v1'])}+{_fmt(data['dv1'])}, "
            f"{_fmt(data['v2'])}+{_fmt(data['dv2'])})"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transported vector.

        Args:
            data: Solution data.

        Returns:
            Formatted new vector.
        """
        return f"V_new=({_fmt(data['v1_new'])},{_fmt(data['v2_new'])})"
