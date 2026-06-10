"""Deep calculus generators -- multivariable, vector calculus, advanced integration.

12 generators at tiers 5-6 covering Stokes' theorem, divergence theorem,
curl computation, Laplacian, Jacobian matrix, implicit function theorem,
integration by parts (definite), partial fraction integration, change of
variables, contour integral (real), directional derivative, and vector
potential.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ──────────────────────────────────────────────────


def _fmt(value: float, places: int = 4) -> str:
    """Round a float and return its string representation.

    Args:
        value: Number to format.
        places: Decimal places.

    Returns:
        Rounded string with trailing zeros stripped.
    """
    return f"{round(value, places):.{places}f}".rstrip("0").rstrip(".")


# ── 1. Stokes' theorem (tier 6) ────────────────────────────────────────


@register
class StokesTheoremGenerator(StepGenerator):
    """Verify Stokes' theorem: integral_C F.dr = integral_S (curl F).dS.

    Computes curl of a polynomial vector field over a disk in the xy-plane,
    evaluates the surface integral, and confirms equality with the line
    integral.

    Difficulty scaling:
        d1-3: F = (ay, -bx, 0) over disk of radius R.
        d4-6: F = (az*y, bz*x, cx^2) with non-trivial curl z-component.
        d7-8: F with all three components contributing to curl.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stokes_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls field complexity.

        Returns:
            Natural language description.
        """
        return "verify Stokes' theorem for the given vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Stokes' theorem problem.

        Args:
            difficulty: Controls vector field complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r = self._rng.randint(1, 3 + difficulty // 2)
        if difficulty <= 3:
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 4)
            curl_z = -(a + b)
            problem = f"F=({a}y, -{b}x, 0), disk r={r}"
            area = math.pi * r * r
            result = curl_z * area
        elif difficulty <= 6:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            curl_z = b - a
            problem = f"F=({a}y, {b}x, 0), disk r={r}"
            area = math.pi * r * r
            result = curl_z * area
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            c = self._rng.randint(1, 3)
            curl_z = b - a
            problem = f"F=({a}y, {b}x, {c}z), disk r={r}"
            area = math.pi * r * r
            result = curl_z * area
        return problem, {
            "r": r, "curl_z": curl_z, "area": area, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Stokes' theorem verification steps.

        Args:
            data: Solution data with curl and area.

        Returns:
            Steps showing curl, area, and integral.
        """
        return [
            f"curl(F).k = {data['curl_z']}",
            f"area = pi*{data['r']}^2 = {_fmt(data['area'])}",
            f"integral = {data['curl_z']} * {_fmt(data['area'])} = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the surface integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted integral value.
        """
        return _fmt(data["result"])


# ── 2. Divergence theorem (tier 6) ─────────────────────────────────────


@register
class DivergenceTheoremGenerator(StepGenerator):
    """Verify the divergence theorem: integral_S F.dS = integral_V div(F) dV.

    Computes divergence of a polynomial vector field, integrates over a
    cube or sphere, and evaluates the volume integral.

    Difficulty scaling:
        d1-3: F = (ax, by, cz) over cube [0,L]^3.
        d4-6: F with mixed terms over cube.
        d7-8: F over sphere of radius R.

    Prerequisites:
        divergence (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "divergence_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["divergence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls field complexity.

        Returns:
            Natural language description.
        """
        return "verify the divergence theorem for the given vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a divergence theorem problem.

        Args:
            difficulty: Controls vector field and region.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        b = self._rng.randint(1, 4)
        c = self._rng.randint(1, 4)
        div_val = a + b + c
        if difficulty <= 6:
            side = self._rng.randint(1, 2 + difficulty // 2)
            volume = side ** 3
            problem = f"F=({a}x,{b}y,{c}z), cube [0,{side}]^3"
            region = f"[0,{side}]^3"
        else:
            r = self._rng.randint(1, 3)
            volume = (4 / 3) * math.pi * r ** 3
            problem = f"F=({a}x,{b}y,{c}z), sphere r={r}"
            region = f"sphere r={r}"
        result = div_val * volume
        return problem, {
            "a": a, "b": b, "c": c, "div": div_val,
            "volume": volume, "result": result, "region": region,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate divergence theorem verification steps.

        Args:
            data: Solution data with divergence and volume.

        Returns:
            Steps showing divergence, volume, and integral.
        """
        return [
            f"div(F) = {data['a']}+{data['b']}+{data['c']} = {data['div']}",
            f"volume of {data['region']} = {_fmt(data['volume'])}",
            f"integral = {data['div']} * {_fmt(data['volume'])} = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the volume integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted integral value.
        """
        return _fmt(data["result"])


# ── 3. Curl computation (tier 5) ───────────────────────────────────────


@register
class CurlComputeGenerator(StepGenerator):
    """Compute the curl of a polynomial vector field.

    curl F = (dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy).
    Evaluates at a specific point.

    Difficulty scaling:
        d1-3: F = (ay, bx, 0). Only z-component non-zero.
        d4-6: F = (az, 0, cx). Two non-zero components.
        d7-8: F = (ay+bz, cx+dz, ex+fy). All components non-zero.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "curl_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls field complexity.

        Returns:
            Natural language description.
        """
        return "compute the curl of the vector field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a curl computation problem.

        Args:
            difficulty: Controls vector field type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            problem = f"F = ({a}y, {b}x, 0)"
            curl = (0, 0, b - a)
        elif difficulty <= 6:
            a = self._rng.randint(1, 4)
            c = self._rng.randint(1, 4)
            problem = f"F = ({a}z, 0, {c}x)"
            curl = (0, a - c, 0)
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            c = self._rng.randint(1, 3)
            d = self._rng.randint(1, 3)
            e = self._rng.randint(1, 3)
            f_ = self._rng.randint(1, 3)
            problem = f"F = ({a}y+{b}z, {c}x+{d}z, {e}x+{f_}y)"
            curl_x = f_ - d
            curl_y = b - e
            curl_z = c - a
            curl = (curl_x, curl_y, curl_z)
        return problem, {"curl": curl}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate curl computation steps.

        Args:
            data: Solution data with curl components.

        Returns:
            Steps showing each curl component.
        """
        cx, cy, cz = data["curl"]
        return [
            f"curl_x = dFz/dy - dFy/dz = {cx}",
            f"curl_y = dFx/dz - dFz/dx = {cy}",
            f"curl_z = dFy/dx - dFx/dy = {cz}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the curl vector.

        Args:
            data: Solution data.

        Returns:
            Curl as a tuple string.
        """
        return f"curl F = ({data['curl'][0]}, {data['curl'][1]}, {data['curl'][2]})"


# ── 4. Laplacian (tier 5) ──────────────────────────────────────────────


@register
class LaplacianGenerator(StepGenerator):
    """Compute the Laplacian of a scalar field.

    nabla^2 f = d^2f/dx^2 + d^2f/dy^2 + d^2f/dz^2.
    For polynomial scalar fields, evaluate at a point.

    Difficulty scaling:
        d1-3: f = ax^2 + by^2 + cz^2.
        d4-6: f = ax^2*y + by*z^2.
        d7-8: f = ax^3 + bx*y^2 + cy*z^2.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laplacian"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Natural language description.
        """
        return "compute the Laplacian of the scalar field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Laplacian problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 5)
            problem = f"f = {a}x^2 + {b}y^2 + {c}z^2"
            fxx = 2 * a
            fyy = 2 * b
            fzz = 2 * c
        elif difficulty <= 6:
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 4)
            problem = f"f = {a}x^2*y + {b}y*z^2"
            fxx = 2 * a
            fyy = 0
            fzz = 2 * b
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            c = self._rng.randint(1, 3)
            x0 = self._rng.randint(1, 3)
            problem = f"f = {a}x^3 + {b}x*y^2 + {c}y*z^2"
            fxx = 6 * a * x0
            fyy = 2 * b
            fzz = 2 * c
            laplacian = fxx + fyy + fzz
            return problem, {
                "fxx": fxx, "fyy": fyy, "fzz": fzz,
                "laplacian": laplacian, "at_point": f"x={x0}",
            }
        laplacian = fxx + fyy + fzz
        return problem, {
            "fxx": fxx, "fyy": fyy, "fzz": fzz,
            "laplacian": laplacian, "at_point": None,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Laplacian computation steps.

        Args:
            data: Solution data with second partial derivatives.

        Returns:
            Steps showing each second derivative and their sum.
        """
        steps = [
            f"d^2f/dx^2 = {data['fxx']}",
            f"d^2f/dy^2 = {data['fyy']}",
            f"d^2f/dz^2 = {data['fzz']}",
        ]
        point = data.get("at_point")
        if point:
            steps.append(f"at {point}: nabla^2 f = {data['laplacian']}")
        else:
            steps.append(
                f"nabla^2 f = {data['fxx']}+{data['fyy']}+{data['fzz']}"
                f" = {data['laplacian']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Laplacian value.

        Args:
            data: Solution data.

        Returns:
            Formatted Laplacian value.
        """
        return f"nabla^2 f = {data['laplacian']}"


# ── 5. Jacobian matrix (tier 5) ────────────────────────────────────────


@register
class JacobianMatrixGenerator(StepGenerator):
    """Compute the Jacobian matrix and its determinant.

    J = [[df1/dx, df1/dy],[df2/dx, df2/dy]]. Evaluates det(J) for
    a coordinate transformation.

    Difficulty scaling:
        d1-3: Linear transform f1=ax+by, f2=cx+dy.
        d4-6: Polar-like: f1=r*cos(theta), f2=r*sin(theta) at a point.
        d7-8: Quadratic: f1=x^2-y^2, f2=2xy at a point.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jacobian_matrix"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls transformation type.

        Returns:
            Natural language description.
        """
        return "compute the Jacobian matrix and its determinant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Jacobian matrix problem.

        Args:
            difficulty: Controls transformation complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 5)
            d = self._rng.randint(1, 5)
            problem = f"f1={a}x+{b}y, f2={c}x+{d}y"
            j = [[a, b], [c, d]]
            det = a * d - b * c
        elif difficulty <= 6:
            r = self._rng.randint(1, 4)
            theta_num = self._rng.choice([0, 1, 2, 3, 4, 6])
            theta = theta_num * math.pi / 6
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            j = [[round(cos_t, 4), round(-r * sin_t, 4)],
                 [round(sin_t, 4), round(r * cos_t, 4)]]
            det = r
            problem = f"x=r*cos(t), y=r*sin(t) at r={r}, t={theta_num}*pi/6"
        else:
            x0 = self._rng.randint(1, 3)
            y0 = self._rng.randint(1, 3)
            j = [[2 * x0, -2 * y0], [2 * y0, 2 * x0]]
            det = 4 * x0 * x0 + 4 * y0 * y0
            problem = f"f1=x^2-y^2, f2=2xy at ({x0},{y0})"
        return problem, {"J": j, "det": det}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Jacobian computation steps.

        Args:
            data: Solution data with Jacobian entries.

        Returns:
            Steps showing matrix entries and determinant.
        """
        j = data["J"]
        return [
            f"J = [[{_fmt(j[0][0])}, {_fmt(j[0][1])}], "
            f"[{_fmt(j[1][0])}, {_fmt(j[1][1])}]]",
            f"det(J) = {_fmt(j[0][0])}*{_fmt(j[1][1])} - "
            f"{_fmt(j[0][1])}*{_fmt(j[1][0])}",
            f"det(J) = {_fmt(data['det'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Jacobian determinant.

        Args:
            data: Solution data.

        Returns:
            Formatted determinant.
        """
        return f"det(J) = {_fmt(data['det'])}"


# ── 6. Implicit function theorem (tier 5) ──────────────────────────────


@register
class ImplicitFunctionGenerator(StepGenerator):
    """Apply the implicit function theorem to find dy/dx and d2y/dx2.

    Given F(x,y)=0, dy/dx = -Fx/Fy. Also computes the second derivative
    d2y/dx2 via implicit differentiation.

    Difficulty scaling:
        d1-3: F = x^2 + y^2 - r^2.
        d4-6: F = x^2*y + y^3 - c.
        d7-8: F = e^(xy) - x - y (approximated with polynomials).

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "implicit_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls equation type.

        Returns:
            Natural language description.
        """
        return "find dy/dx and d2y/dx2 using the implicit function theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an implicit function theorem problem.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            x0 = self._rng.randint(1, 4)
            y0 = self._rng.randint(1, 4)
            r_sq = x0 * x0 + y0 * y0
            fx = 2 * x0
            fy = 2 * y0
            dydx = -fx / fy
            # d2y/dx2 for circle: -(fy*fxx - fx*fxy*dydx + ...)
            # For x^2+y^2=r^2: d2y/dx2 = -r^2/y^3
            d2ydx2 = -r_sq / (y0 ** 3)
            problem = f"x^2 + y^2 = {r_sq} at ({x0},{y0})"
        elif difficulty <= 6:
            x0 = self._rng.randint(1, 2)
            y0 = self._rng.randint(1, 2)
            c = x0 * x0 * y0 + y0 ** 3
            fx = 2 * x0 * y0
            fy = x0 * x0 + 3 * y0 * y0
            dydx = -fx / fy if fy != 0 else 0.0
            # Simplified second derivative
            fxx = 2 * y0
            fxy = 2 * x0
            fyy = 6 * y0
            numer = -(fxx + 2 * fxy * dydx + fyy * dydx * dydx)
            d2ydx2 = numer / fy if fy != 0 else 0.0
            problem = f"x^2*y + y^3 = {c} at ({x0},{y0})"
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            x0 = 1
            y0 = 1
            c = a * x0 * x0 + b * x0 * y0 + y0 * y0
            fx = 2 * a * x0 + b * y0
            fy = b * x0 + 2 * y0
            dydx = -fx / fy if fy != 0 else 0.0
            fxx = 2 * a
            fxy = b
            fyy = 2
            numer = -(fxx + 2 * fxy * dydx + fyy * dydx * dydx)
            d2ydx2 = numer / fy if fy != 0 else 0.0
            problem = f"{a}x^2 + {b}xy + y^2 = {c} at ({x0},{y0})"
        return problem, {
            "fx": fx, "fy": fy, "x0": x0, "y0": y0,
            "dydx": dydx, "d2ydx2": d2ydx2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate implicit function steps.

        Args:
            data: Solution data with partial derivatives.

        Returns:
            Steps showing Fx, Fy, dy/dx, d2y/dx2.
        """
        return [
            f"F_x = {data['fx']}, F_y = {data['fy']}",
            f"dy/dx = -F_x/F_y = {_fmt(data['dydx'])}",
            f"d2y/dx2 = {_fmt(data['d2ydx2'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return dy/dx and d2y/dx2.

        Args:
            data: Solution data.

        Returns:
            Formatted derivatives.
        """
        return f"dy/dx={_fmt(data['dydx'])}, d2y/dx2={_fmt(data['d2ydx2'])}"


# ── 7. Integration by parts (definite) (tier 5) ────────────────────────


@register
class IntegrationByPartsDefiniteGenerator(StepGenerator):
    """Evaluate a definite integral using integration by parts.

    integral_a^b u*dv = [uv]_a^b - integral_a^b v*du.
    Evaluates both the boundary term and the remaining integral.

    Difficulty scaling:
        d1-3: integral x*e^x dx from 0 to a.
        d4-6: integral x*sin(x) dx from 0 to pi.
        d7-8: integral x^2*e^x dx from 0 to a (double IBP).

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integration_by_parts_definite"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand type.

        Returns:
            Natural language description.
        """
        return "evaluate the definite integral using integration by parts"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integration by parts definite integral problem.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a_val = self._rng.randint(1, 3)
            # integral_0^a x*e^x dx = [x*e^x - e^x]_0^a = a*e^a - e^a + 1
            uv_upper = a_val * math.exp(a_val) - math.exp(a_val)
            uv_lower = -1.0
            result = uv_upper - uv_lower
            problem = f"int_0^{a_val} x*e^x dx"
            u_str = "x"
            dv_str = "e^x dx"
            boundary = f"[x*e^x - e^x]_0^{a_val}"
        elif difficulty <= 6:
            # integral_0^pi x*sin(x) dx = [-x*cos(x) + sin(x)]_0^pi = pi
            result = math.pi
            problem = "int_0^pi x*sin(x) dx"
            u_str = "x"
            dv_str = "sin(x) dx"
            boundary = "[-x*cos(x) + sin(x)]_0^pi"
            a_val = "pi"
        else:
            a_val = self._rng.randint(1, 2)
            # integral_0^a x^2*e^x dx = [x^2*e^x - 2x*e^x + 2*e^x]_0^a
            ea = math.exp(a_val)
            result = (a_val ** 2 - 2 * a_val + 2) * ea - 2
            problem = f"int_0^{a_val} x^2*e^x dx"
            u_str = "x^2"
            dv_str = "e^x dx"
            boundary = f"[x^2*e^x - 2x*e^x + 2*e^x]_0^{a_val}"
        return problem, {
            "u": u_str, "dv": dv_str,
            "boundary": boundary, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate integration by parts steps.

        Args:
            data: Solution data with u, dv, boundary, result.

        Returns:
            Steps showing u, dv choice and evaluation.
        """
        return [
            f"u = {data['u']}, dv = {data['dv']}",
            f"evaluate {data['boundary']}",
            f"result = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted result.
        """
        return _fmt(data["result"])


# ── 8. Partial fraction integration (tier 5) ───────────────────────────


@register
class PartialFractionIntegrationGenerator(StepGenerator):
    """Integrate a rational function using partial fraction decomposition.

    Decomposes P(x)/Q(x) where Q has distinct linear factors, then
    integrates each term.

    Difficulty scaling:
        d1-3: 1/((x-a)(x-b)), distinct roots.
        d4-6: (cx+d)/((x-a)(x-b)), linear numerator.
        d7-8: 1/((x-a)(x-b)(x-c)), three factors.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "partial_fraction_integration"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls rational function complexity.

        Returns:
            Natural language description.
        """
        return "integrate using partial fraction decomposition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a partial fraction integration problem.

        Args:
            difficulty: Controls denominator complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 4)
            b = a + self._rng.randint(1, 3)
            # 1/((x-a)(x-b)) = A/(x-a) + B/(x-b)
            # A = 1/(a-b), B = 1/(b-a)
            coeff_a = 1.0 / (a - b)
            coeff_b = 1.0 / (b - a)
            lo = b + 1
            hi = lo + self._rng.randint(1, 3)
            result = coeff_a * math.log(abs(hi - a) / abs(lo - a)) + \
                coeff_b * math.log(abs(hi - b) / abs(lo - b))
            problem = f"int_{lo}^{hi} 1/((x-{a})(x-{b})) dx"
            decomp = f"{_fmt(coeff_a)}/(x-{a}) + {_fmt(coeff_b)}/(x-{b})"
        elif difficulty <= 6:
            a = self._rng.randint(0, 2)
            b = a + self._rng.randint(2, 4)
            c_num = self._rng.randint(1, 3)
            d_num = self._rng.randint(0, 2)
            # (cx+d)/((x-a)(x-b))
            coeff_a = (c_num * a + d_num) / (a - b)
            coeff_b = (c_num * b + d_num) / (b - a)
            lo = b + 1
            hi = lo + self._rng.randint(1, 3)
            result = coeff_a * math.log(abs(hi - a) / abs(lo - a)) + \
                coeff_b * math.log(abs(hi - b) / abs(lo - b))
            problem = f"int_{lo}^{hi} ({c_num}x+{d_num})/((x-{a})(x-{b})) dx"
            decomp = f"{_fmt(coeff_a)}/(x-{a}) + {_fmt(coeff_b)}/(x-{b})"
        else:
            a, b, c = 0, 1, 2
            # 1/((x)(x-1)(x-2))
            coeff_a = 1.0 / ((a - b) * (a - c))  # 1/((-1)*(-2)) = 0.5
            coeff_b = 1.0 / ((b - a) * (b - c))  # 1/((1)*(-1)) = -1
            coeff_c = 1.0 / ((c - a) * (c - b))  # 1/((2)*(1)) = 0.5
            lo = 3
            hi = lo + self._rng.randint(1, 3)
            result = (
                coeff_a * math.log(abs(hi) / abs(lo))
                + coeff_b * math.log(abs(hi - 1) / abs(lo - 1))
                + coeff_c * math.log(abs(hi - 2) / abs(lo - 2))
            )
            problem = f"int_{lo}^{hi} 1/(x(x-1)(x-2)) dx"
            decomp = (f"{_fmt(coeff_a)}/x + {_fmt(coeff_b)}/(x-1)"
                       f" + {_fmt(coeff_c)}/(x-2)")
        return problem, {"decomp": decomp, "result": result}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate partial fraction integration steps.

        Args:
            data: Solution data with decomposition and result.

        Returns:
            Steps showing decomposition and integral.
        """
        return [
            f"decompose: {data['decomp']}",
            f"integrate each term: ln|...| terms",
            f"result = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted result.
        """
        return _fmt(data["result"])


# ── 9. Change of variables (tier 6) ────────────────────────────────────


@register
class ChangeOfVariablesGenerator(StepGenerator):
    """Transform a double integral using a change of variables.

    Computes the Jacobian of the transformation, transforms the limits,
    and evaluates the integral. Uses polar and simple affine substitutions.

    Difficulty scaling:
        d1-3: Cartesian to polar for x^2+y^2 <= R^2.
        d4-6: Affine substitution u=x+y, v=x-y.
        d7-8: Cylindrical coordinates for volume integral.

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "change_of_variables"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls substitution type.

        Returns:
            Natural language description.
        """
        return "evaluate the integral using change of variables"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a change of variables problem.

        Args:
            difficulty: Controls coordinate system.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            r_max = self._rng.randint(1, 3)
            # int int (x^2+y^2) dA over disk = int_0^R int_0^2pi r^2 * r dr dt
            # = 2*pi * R^4/4 = pi*R^4/2
            result = math.pi * r_max ** 4 / 2
            problem = f"int int (x^2+y^2) dA, x^2+y^2<={r_max}^2"
            jacobian = "r"
            sub = "x=r*cos(t), y=r*sin(t)"
        elif difficulty <= 6:
            a = self._rng.randint(1, 3)
            # int int 1 dA over |x+y|<=a, |x-y|<=a using u=x+y, v=x-y
            # Jacobian = 1/2, area = (2a)^2/2 = 2a^2
            result = 2.0 * a * a
            problem = f"int int 1 dA, |x+y|<={a}, |x-y|<={a}"
            jacobian = "1/2"
            sub = "u=x+y, v=x-y"
        else:
            r_max = self._rng.randint(1, 3)
            h = self._rng.randint(1, 4)
            # Volume of cylinder: pi*R^2*h via cylindrical coords
            result = math.pi * r_max ** 2 * h
            problem = f"int int int 1 dV, cylinder r<={r_max}, 0<=z<={h}"
            jacobian = "r"
            sub = "cylindrical: x=r*cos(t), y=r*sin(t), z=z"
        return problem, {
            "sub": sub, "jacobian": jacobian, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate change of variables steps.

        Args:
            data: Solution data with substitution and Jacobian.

        Returns:
            Steps showing substitution, Jacobian, and result.
        """
        return [
            f"substitution: {data['sub']}",
            f"|J| = {data['jacobian']}",
            f"result = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted result.
        """
        return _fmt(data["result"])


# ── 10. Contour integral (real) (tier 6) ───────────────────────────────


@register
class ContourIntegralRealGenerator(StepGenerator):
    """Evaluate a real trigonometric integral via contour methods.

    Converts integral_0^2pi f(cos(t),sin(t)) dt using z=e^(it),
    cos(t)=(z+1/z)/2, sin(t)=(z-1/z)/(2i). Evaluates using residues.

    Difficulty scaling:
        d1-3: int_0^2pi 1/(a+cos(t)) dt = 2*pi/sqrt(a^2-1).
        d4-6: int_0^2pi 1/(a+b*cos(t)) dt with a>b>0.
        d7-8: int_0^2pi cos^2(t)/(a+cos(t)) dt (algebra reduction).

    Prerequisites:
        definite_integral (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "contour_integral_real"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand type.

        Returns:
            Natural language description.
        """
        return "evaluate the real integral using contour methods"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a contour integral problem for a real trig integral.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            a = self._rng.randint(2, 4 + difficulty)
            b = 1
            # int_0^2pi 1/(a+b*cos(t)) dt = 2*pi/sqrt(a^2-b^2)
            discriminant = a * a - b * b
            result = 2 * math.pi / math.sqrt(discriminant)
            if difficulty <= 3:
                problem = f"int_0^2pi 1/({a}+cos(t)) dt"
            else:
                b = self._rng.randint(1, a - 1)
                discriminant = a * a - b * b
                result = 2 * math.pi / math.sqrt(discriminant)
                problem = f"int_0^2pi 1/({a}+{b}*cos(t)) dt"
            sub = "z=e^(it)"
            formula = f"2*pi/sqrt({a}^2-{b}^2)"
        else:
            a = self._rng.randint(2, 5)
            # Reduce: int cos^2(t)/(a+cos(t)) dt
            # = int (1 - sin^2(t))/(a+cos(t)) dt ... use known formula
            # Result: 2*pi*(a - sqrt(a^2-1))/sqrt(a^2-1)
            disc = a * a - 1
            sq = math.sqrt(disc)
            result = 2 * math.pi * (a - sq) / sq
            problem = f"int_0^2pi cos^2(t)/({a}+cos(t)) dt"
            sub = "z=e^(it)"
            formula = f"2*pi*({a}-sqrt({a}^2-1))/sqrt({a}^2-1)"
        return problem, {
            "sub": sub, "formula": formula, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate contour integral steps.

        Args:
            data: Solution data with substitution and formula.

        Returns:
            Steps showing substitution and residue evaluation.
        """
        return [
            f"substitute {data['sub']}: cos(t)=(z+1/z)/2",
            f"apply residue theorem: {data['formula']}",
            f"result = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the integral value.

        Args:
            data: Solution data.

        Returns:
            Formatted result.
        """
        return _fmt(data["result"])


# ── 11. Directional derivative (tier 5) ────────────────────────────────


@register
class DirectionalDerivativeGenerator(StepGenerator):
    """Compute the directional derivative D_u f = grad(f) . u_hat.

    Computes the gradient, normalises the direction vector, and takes
    the dot product.

    Difficulty scaling:
        d1-3: f = ax+by, u = (1,0) or (0,1).
        d4-6: f = ax^2+by^2 at a point, u = (1,1)/sqrt(2).
        d7-8: f = ax^2+bxy+cy^2, u arbitrary direction.

    Prerequisites:
        gradient (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "directional_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gradient"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function and direction complexity.

        Returns:
            Natural language description.
        """
        return "compute the directional derivative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a directional derivative problem.

        Args:
            difficulty: Controls function and direction.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            grad = [a, b]
            u = self._rng.choice([(1, 0), (0, 1)])
            u_hat = list(u)
            result = grad[0] * u_hat[0] + grad[1] * u_hat[1]
            problem = f"f={a}x+{b}y, u=({u[0]},{u[1]})"
        elif difficulty <= 6:
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 4)
            x0 = self._rng.randint(1, 3)
            y0 = self._rng.randint(1, 3)
            grad = [2 * a * x0, 2 * b * y0]
            norm = math.sqrt(2)
            u_hat = [1 / norm, 1 / norm]
            result = grad[0] * u_hat[0] + grad[1] * u_hat[1]
            problem = f"f={a}x^2+{b}y^2 at ({x0},{y0}), u=(1,1)"
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            c = self._rng.randint(1, 3)
            x0 = self._rng.randint(1, 2)
            y0 = self._rng.randint(1, 2)
            grad = [2 * a * x0 + b * y0, b * x0 + 2 * c * y0]
            ux = self._rng.randint(1, 3)
            uy = self._rng.randint(1, 3)
            norm = math.sqrt(ux ** 2 + uy ** 2)
            u_hat = [ux / norm, uy / norm]
            result = grad[0] * u_hat[0] + grad[1] * u_hat[1]
            problem = f"f={a}x^2+{b}xy+{c}y^2 at ({x0},{y0}), u=({ux},{uy})"
        return problem, {
            "grad": grad, "u_hat": u_hat, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate directional derivative steps.

        Args:
            data: Solution data with gradient and unit vector.

        Returns:
            Steps showing gradient, normalisation, dot product.
        """
        g = data["grad"]
        u = data["u_hat"]
        return [
            f"grad(f) = ({_fmt(g[0])}, {_fmt(g[1])})",
            f"u_hat = ({_fmt(u[0])}, {_fmt(u[1])})",
            f"D_u f = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the directional derivative.

        Args:
            data: Solution data.

        Returns:
            Formatted result.
        """
        return f"D_u f = {_fmt(data['result'])}"


# ── 12. Vector potential (tier 6) ──────────────────────────────────────


@register
class VectorPotentialGenerator(StepGenerator):
    """Find a vector potential A such that curl(A) = B.

    For a uniform field B = (0, 0, B0), one standard gauge gives
    A = (-B0*y/2, B0*x/2, 0). Verifies by computing curl(A).

    Difficulty scaling:
        d1-3: B = (0, 0, B0) with integer B0.
        d4-6: B = (0, 0, B0), verify all three curl components.
        d7-8: B = (B1, 0, 0), A = (0, B1*z/2, -B1*y/2), verify.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vector_potential"

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
            difficulty: Controls field orientation.

        Returns:
            Natural language description.
        """
        return "find a vector potential A such that curl(A) = B"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vector potential problem.

        Args:
            difficulty: Controls field direction.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            b0 = self._rng.randint(1, 6 + difficulty)
            problem = f"B = (0, 0, {b0})"
            ax = f"-{b0}y/2"
            ay = f"{b0}x/2"
            az = "0"
            curl = (0, 0, b0)
        else:
            b1 = self._rng.randint(1, 6)
            problem = f"B = ({b1}, 0, 0)"
            ax = "0"
            ay = f"{b1}z/2"
            az = f"-{b1}y/2"
            curl = (b1, 0, 0)
        return problem, {
            "A": (ax, ay, az), "curl": curl, "B": problem,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate vector potential steps.

        Args:
            data: Solution data with A components and curl.

        Returns:
            Steps showing A and curl verification.
        """
        ax, ay, az = data["A"]
        cx, cy, cz = data["curl"]
        return [
            f"A = ({ax}, {ay}, {az})",
            f"curl(A) = ({cx}, {cy}, {cz})",
            f"curl(A) = B verified",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the vector potential.

        Args:
            data: Solution data.

        Returns:
            Formatted vector potential.
        """
        ax, ay, az = data["A"]
        return f"A = ({ax}, {ay}, {az})"
