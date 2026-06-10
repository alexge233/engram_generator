"""Optics generators -- refraction, lenses, interference, and diffraction.

Covers Snell's law, the thin lens equation, magnification, double-slit
interference, Brewster's angle, and diffraction gratings. Tiers range
from 4 (introductory geometric optics) to 5 (wave optics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _OpticsFormatter:
    """Formats numeric values for optics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
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


_f = _OpticsFormatter.fmt


# ===================================================================
# 1. Snell's law  (tier 4)
# ===================================================================

@register
class SnellsLawGenerator(StepGenerator):
    """Snell's law: n1 * sin(theta1) = n2 * sin(theta2).

    Given three of the four quantities (n1, theta1, n2, theta2),
    computes the missing one. Angles are in degrees.

    Difficulty scaling:
        Difficulty 1-3: simple indices (1.0, 1.33, 1.5), small angles.
        Difficulty 4-6: wider index range, larger angles.
        Difficulty 7-8: near-critical-angle scenarios.

    Prerequisites:
        sin_cos_eval.
    """

    _INDICES = [1.0, 1.33, 1.5, 1.52, 1.66, 2.42]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "snells_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply Snell's law of refraction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate refraction parameters and choose which to solve for.

        Args:
            difficulty: Controls index and angle ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n1 = self._rng.choice(self._INDICES[:3 + min(difficulty, 3)])
        n2 = self._rng.choice(self._INDICES[:3 + min(difficulty, 3)])
        while n2 == n1:
            n2 = self._rng.choice(self._INDICES[:3 + min(difficulty, 3)])

        max_angle = min(40 + difficulty * 5, 80)
        theta1 = self._rng.randint(10, max_angle)
        sin_t2 = n1 * math.sin(math.radians(theta1)) / n2
        sin_t2 = min(sin_t2, 0.999)
        theta2 = round(math.degrees(math.asin(sin_t2)), 4)

        target = self._rng.choice(["n1", "n2", "theta1", "theta2"])

        return "n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2", {
            "n1": n1, "n2": n2,
            "theta1": theta1, "theta2": theta2,
            "sin_t1": round(math.sin(math.radians(theta1)), 4),
            "sin_t2": round(sin_t2, 4),
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and solving steps.

        Args:
            data: Solution data with indices and angles.

        Returns:
            List of step strings.
        """
        target = data["target"]
        if target == "theta2":
            return [
                f"n_1 \\sin\\theta_1 = ({data['n1']})\\sin({data['theta1']})"
                f" = ({data['n1']})({_f(data['sin_t1'])})"
                f" = {_f(data['n1'] * data['sin_t1'])}",
                f"\\sin\\theta_2 = {_f(data['sin_t2'])}",
                f"\\theta_2 = \\arcsin({_f(data['sin_t2'])})",
            ]
        if target == "theta1":
            return [
                f"\\sin\\theta_1 = n_2 \\sin\\theta_2 / n_1"
                f" = ({data['n2']})({_f(data['sin_t2'])})/{data['n1']}",
                f"\\sin\\theta_1 = {_f(data['sin_t1'])}",
                f"\\theta_1 = \\arcsin({_f(data['sin_t1'])})",
            ]
        if target == "n2":
            product = round(data["n1"] * data["sin_t1"], 4)
            return [
                f"n_2 = n_1 \\sin\\theta_1 / \\sin\\theta_2",
                f"n_2 = ({data['n1']})({_f(data['sin_t1'])})/"
                f"{_f(data['sin_t2'])}",
                f"n_2 = {_f(product)}/{_f(data['sin_t2'])}",
            ]
        # target == "n1"
        product = round(data["n2"] * data["sin_t2"], 4)
        return [
            f"n_1 = n_2 \\sin\\theta_2 / \\sin\\theta_1",
            f"n_1 = ({data['n2']})({_f(data['sin_t2'])})/"
            f"{_f(data['sin_t1'])}",
            f"n_1 = {_f(product)}/{_f(data['sin_t1'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved quantity.

        Args:
            data: Solution data.

        Returns:
            String representation of the target variable.
        """
        target = data["target"]
        if target == "theta2":
            return f"\\theta_2 = {_f(data['theta2'])} deg"
        if target == "theta1":
            return f"\\theta_1 = {data['theta1']} deg"
        if target == "n2":
            return f"n_2 = {_f(data['n2'])}"
        return f"n_1 = {_f(data['n1'])}"


# ===================================================================
# 2. Thin lens equation  (tier 4)
# ===================================================================

@register
class ThinLensGenerator(StepGenerator):
    """Thin lens equation: 1/f = 1/do + 1/di.

    Given two of the three quantities (focal length f, object
    distance do, image distance di), computes the missing one.

    Difficulty scaling:
        Difficulty 1-3: convex lens, integer distances 5-50 cm.
        Difficulty 4-6: convex or concave, distances 5-100 cm.
        Difficulty 7-8: virtual images, negative values.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thin_lens"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply thin lens equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate lens parameters and choose which to solve for.

        Args:
            difficulty: Controls distance ranges and lens type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        max_dist = 20 + difficulty * 10
        f = self._rng.randint(5, max(6, max_dist // 2))
        do = self._rng.randint(f + 1, max(f + 2, max_dist))

        if difficulty >= 5 and self._rng.random() < 0.4:
            f = -f

        di = round(1.0 / (1.0 / f - 1.0 / do), 4)
        target = self._rng.choice(["f", "do", "di"])

        return "\\frac{1}{f} = \\frac{1}{d_o} + \\frac{1}{d_i}", {
            "f": f, "do": do, "di": di, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rearrangement and computation steps.

        Args:
            data: Solution data with f, do, di.

        Returns:
            List of step strings.
        """
        target = data["target"]
        f, do, di = data["f"], data["do"], data["di"]
        if target == "di":
            inv_f = round(1.0 / f, 4)
            inv_do = round(1.0 / do, 4)
            inv_di = round(inv_f - inv_do, 4)
            return [
                f"1/f = {_f(inv_f)}, 1/d_o = {_f(inv_do)}",
                f"1/d_i = 1/f - 1/d_o = {_f(inv_di)}",
            ]
        if target == "do":
            inv_f = round(1.0 / f, 4)
            inv_di = round(1.0 / di, 4)
            inv_do = round(inv_f - inv_di, 4)
            return [
                f"1/f = {_f(inv_f)}, 1/d_i = {_f(inv_di)}",
                f"1/d_o = 1/f - 1/d_i = {_f(inv_do)}",
            ]
        # target == "f"
        inv_do = round(1.0 / do, 4)
        inv_di = round(1.0 / di, 4)
        inv_f = round(inv_do + inv_di, 4)
        return [
            f"1/d_o = {_f(inv_do)}, 1/d_i = {_f(inv_di)}",
            f"1/f = 1/d_o + 1/d_i = {_f(inv_f)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved quantity.

        Args:
            data: Solution data.

        Returns:
            String representation of the target variable with units.
        """
        target = data["target"]
        return f"{target.replace('do', 'd_o').replace('di', 'd_i')} = {_f(data[target])} cm"


# ===================================================================
# 3. Magnification  (tier 4)
# ===================================================================

@register
class MagnificationGenerator(StepGenerator):
    """Lateral magnification: M = -di/do = hi/ho.

    Computes magnification from image and object distances, or
    from image and object heights.

    Difficulty scaling:
        Difficulty 1-3: integer distances, positive magnification.
        Difficulty 4-6: fractional magnification, decimal heights.
        Difficulty 7-8: virtual images, compute missing height.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnification"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute lateral magnification"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate magnification problem parameters.

        Args:
            difficulty: Controls value ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4:
            do = self._rng.randint(5, 20 + difficulty * 5)
            di = self._rng.randint(5, 20 + difficulty * 5)
            m = round(-di / do, 4)
            return "M = -d_i / d_o", {
                "do": do, "di": di, "M": m, "mode": "distance",
            }
        ho = round(self._rng.uniform(1.0, 10.0), 1)
        m_val = round(self._rng.uniform(-3.0, 3.0), 2)
        while abs(m_val) < 0.1:
            m_val = round(self._rng.uniform(-3.0, 3.0), 2)
        hi = round(ho * m_val, 4)
        return "M = h_i / h_o", {
            "ho": ho, "hi": hi, "M": m_val, "mode": "height",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate magnification computation steps.

        Args:
            data: Solution data with distances or heights.

        Returns:
            List of step strings.
        """
        if data["mode"] == "distance":
            return [
                f"d_o = {data['do']}, d_i = {data['di']}",
                f"M = -{data['di']}/{data['do']}",
            ]
        return [
            f"h_o = {data['ho']}, h_i = {_f(data['hi'])}",
            f"M = {_f(data['hi'])}/{data['ho']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the magnification.

        Args:
            data: Solution data.

        Returns:
            String representation of M.
        """
        return f"M = {_f(data['M'])}"


# ===================================================================
# 4. Double slit interference  (tier 5)
# ===================================================================

@register
class DoubleSlitGenerator(StepGenerator):
    """Double slit interference fringe position: y = m * lambda * L / d.

    Computes the position of the m-th bright fringe on a screen at
    distance L from slits separated by d, illuminated by wavelength
    lambda.

    Difficulty scaling:
        Difficulty 1-3: m=1 or 2, visible light, standard geometry.
        Difficulty 4-6: higher orders, varied wavelengths.
        Difficulty 7-8: compute fringe spacing or solve for lambda.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "double_slit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute double slit fringe position"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate double slit parameters and compute fringe position.

        Args:
            difficulty: Controls parameter ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        d_mm = round(self._rng.uniform(0.1, 0.5 + difficulty * 0.1), 2)
        d = d_mm * 1e-3
        l_m = round(self._rng.uniform(0.5, 2.0 + difficulty * 0.5), 1)

        if difficulty <= 3:
            m = self._rng.randint(1, 2)
        else:
            m = self._rng.randint(1, min(5, difficulty))

        y = round(m * lam * l_m / d, 4)

        if difficulty >= 7:
            # Solve for lambda given y
            return "y = \\frac{m \\lambda L}{d}", {
                "lam_nm": lam_nm, "lam": lam, "d_mm": d_mm, "d": d,
                "L": l_m, "m": m, "y": y, "target": "lambda",
            }

        return "y = \\frac{m \\lambda L}{d}", {
            "lam_nm": lam_nm, "lam": lam, "d_mm": d_mm, "d": d,
            "L": l_m, "m": m, "y": y, "target": "y",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate double slit computation steps.

        Args:
            data: Solution data with slit parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "y":
            num = round(data["m"] * data["lam"] * data["L"], 4)
            return [
                f"lambda={data['lam_nm']}nm, d={data['d_mm']}mm, "
                f"L={data['L']}m, m={data['m']}",
                f"m*lambda*L = {data['m']}*{data['lam_nm']}e-9*{data['L']}"
                f" = {_f(num)}",
                f"y = {_f(num)}/{_f(data['d'])}",
            ]
        # solve for lambda
        return [
            f"y={_f(data['y'])}m, d={data['d_mm']}mm, "
            f"L={data['L']}m, m={data['m']}",
            f"lambda = y*d/(m*L) = {_f(data['y'])}*{_f(data['d'])}/"
            f"({data['m']}*{data['L']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fringe position or wavelength.

        Args:
            data: Solution data.

        Returns:
            String with the computed result and units.
        """
        if data["target"] == "y":
            return f"y = {_f(data['y'])} m"
        return f"lambda = {data['lam_nm']} nm"


# ===================================================================
# 5. Brewster's angle  (tier 5)
# ===================================================================

@register
class BrewsterAngleGenerator(StepGenerator):
    """Brewster's angle: tan(theta_B) = n2 / n1.

    Computes the Brewster angle for polarisation by reflection
    at a dielectric interface.

    Difficulty scaling:
        Difficulty 1-3: common materials (air-glass, air-water).
        Difficulty 4-6: wider material range.
        Difficulty 7-8: solve for n2 given Brewster angle.

    Prerequisites:
        snells_law.
    """

    _MATERIALS = {
        "air": 1.0, "water": 1.33, "glass": 1.5,
        "crown_glass": 1.52, "flint_glass": 1.66, "diamond": 2.42,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "brewster_angle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["snells_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Brewster's angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Brewster angle problem parameters.

        Args:
            difficulty: Controls material range and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        names = list(self._MATERIALS.keys())
        if difficulty <= 3:
            pool = names[:3]
        else:
            pool = names

        m1 = self._rng.choice(pool)
        m2 = self._rng.choice(pool)
        while m2 == m1:
            m2 = self._rng.choice(pool)

        n1 = self._MATERIALS[m1]
        n2 = self._MATERIALS[m2]
        ratio = n2 / n1
        theta_b = round(math.degrees(math.atan(ratio)), 4)

        if difficulty >= 7:
            return "\\tan\\theta_B = n_2 / n_1", {
                "n1": n1, "n2": n2, "m1": m1, "m2": m2,
                "ratio": round(ratio, 4), "theta_B": theta_b,
                "target": "n2",
            }

        return "\\tan\\theta_B = n_2 / n_1", {
            "n1": n1, "n2": n2, "m1": m1, "m2": m2,
            "ratio": round(ratio, 4), "theta_B": theta_b,
            "target": "theta_B",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Brewster angle computation steps.

        Args:
            data: Solution data with indices and angle.

        Returns:
            List of step strings.
        """
        if data["target"] == "theta_B":
            return [
                f"n_1={data['n1']} ({data['m1']}), "
                f"n_2={data['n2']} ({data['m2']})",
                f"\\tan\\theta_B = {data['n2']}/{data['n1']}"
                f" = {_f(data['ratio'])}",
                f"\\theta_B = \\arctan({_f(data['ratio'])})",
            ]
        # solve for n2
        return [
            f"\\theta_B = {_f(data['theta_B'])} deg, n_1 = {data['n1']}",
            f"n_2 = n_1 \\tan\\theta_B"
            f" = {data['n1']}*\\tan({_f(data['theta_B'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Brewster angle or refractive index.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        if data["target"] == "theta_B":
            return f"\\theta_B = {_f(data['theta_B'])} deg"
        return f"n_2 = {_f(data['n2'])}"


# ===================================================================
# 6. Diffraction grating  (tier 5)
# ===================================================================

@register
class DiffractionGratingGenerator(StepGenerator):
    """Diffraction grating equation: d * sin(theta) = m * lambda.

    Computes the diffraction angle or wavelength for a given order
    m and grating spacing d.

    Difficulty scaling:
        Difficulty 1-3: first order, visible light, standard grating.
        Difficulty 4-6: higher orders, solve for lambda or d.
        Difficulty 7-8: maximum observable order computation.

    Prerequisites:
        snells_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diffraction_grating"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["snells_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply diffraction grating equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate diffraction grating parameters.

        Args:
            difficulty: Controls order and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        lines_per_mm = self._rng.randint(300, 600 + difficulty * 100)
        d = 1.0 / (lines_per_mm * 1e3)

        if difficulty <= 3:
            m = 1
        else:
            max_order = max(1, int(d / lam))
            m = self._rng.randint(1, min(max_order, difficulty))

        sin_theta = m * lam / d
        if sin_theta > 1.0:
            m = max(1, int(d / lam))
            sin_theta = m * lam / d

        theta = round(math.degrees(math.asin(min(sin_theta, 0.999))), 4)

        if difficulty >= 6:
            target = self._rng.choice(["theta", "lambda"])
        else:
            target = "theta"

        return "d \\sin\\theta = m\\lambda", {
            "lam_nm": lam_nm, "lam": lam,
            "lines_per_mm": lines_per_mm, "d": d,
            "m": m, "sin_theta": round(sin_theta, 4),
            "theta": theta, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate diffraction grating computation steps.

        Args:
            data: Solution data with grating parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "theta":
            return [
                f"d = 1/{data['lines_per_mm']}e3 m = {_f(data['d'])} m",
                f"\\sin\\theta = m\\lambda/d"
                f" = {data['m']}*{data['lam_nm']}e-9/{_f(data['d'])}",
                f"\\sin\\theta = {_f(data['sin_theta'])}",
                f"\\theta = \\arcsin({_f(data['sin_theta'])})",
            ]
        # solve for lambda
        return [
            f"d = 1/{data['lines_per_mm']}e3 m, "
            f"\\theta = {_f(data['theta'])} deg, m = {data['m']}",
            f"\\lambda = d \\sin\\theta / m",
            f"\\lambda = {_f(data['d'])}*{_f(data['sin_theta'])}/"
            f"{data['m']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the diffraction angle or wavelength.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        if data["target"] == "theta":
            return f"\\theta = {_f(data['theta'])} deg"
        return f"\\lambda = {data['lam_nm']} nm"
