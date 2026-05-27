"""Extended mathematics generators — advanced calculus, algebra, and quantum math.

Provides generators for integration by parts, partial fractions, series
convergence, De Moivre's theorem, complex division, group order, number
base arithmetic, set operations, Fourier coefficients, tensor products,
Pauli matrix products, and Bloch sphere coordinates. Each generator
produces step-by-step solutions with LaTeX formatting.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class IntegrationByPartsHelper:
    """Represents an integration by parts problem u*dv.

    Stores the product form and computes the formula application
    int(u dv) = u*v - int(v du).

    Example:
        >>> h = IntegrationByPartsHelper("x", "e^x", "1", "e^x")
        >>> h.uv_latex()
        'x e^x'
    """

    def __init__(self, u: str, v: str, du: str, dv_integrand: str) -> None:
        """Initialise with parts for integration.

        Args:
            u: The u function in LaTeX.
            v: The antiderivative of dv in LaTeX.
            du: The derivative of u in LaTeX.
            dv_integrand: The integrand of dv in LaTeX.
        """
        self._u = u
        self._v = v
        self._du = du
        self._dv_integrand = dv_integrand

    @property
    def u(self) -> str:
        """Return u."""
        return self._u

    @property
    def v(self) -> str:
        """Return v."""
        return self._v

    @property
    def du(self) -> str:
        """Return du."""
        return self._du

    @property
    def dv_integrand(self) -> str:
        """Return the integrand of dv."""
        return self._dv_integrand

    def uv_latex(self) -> str:
        """Format u*v in LaTeX.

        Returns:
            LaTeX string for the product u*v.
        """
        return f"{self._u} {self._v}"


class PauliMatrix:
    """Represents a 2x2 Pauli matrix with complex integer entries.

    Stores the four entries of a 2x2 matrix as (real, imag) pairs
    and supports multiplication with another PauliMatrix.

    Example:
        >>> sx = PauliMatrix((0, 0), (1, 0), (1, 0), (0, 0))
        >>> sx.entry_latex(0, 0)
        '0'
    """

    def __init__(self, a: tuple[int, int], b: tuple[int, int],
                 c: tuple[int, int], d: tuple[int, int]) -> None:
        """Initialise with four complex entries as (real, imag) tuples.

        Args:
            a: Entry (0,0).
            b: Entry (0,1).
            c: Entry (1,0).
            d: Entry (1,1).
        """
        self._entries = [[a, b], [c, d]]

    def entry(self, i: int, j: int) -> tuple[int, int]:
        """Return entry at position (i, j).

        Args:
            i: Row index.
            j: Column index.

        Returns:
            Tuple of (real, imag).
        """
        return self._entries[i][j]

    def entry_latex(self, i: int, j: int) -> str:
        """Format entry (i, j) as a LaTeX string.

        Args:
            i: Row index.
            j: Column index.

        Returns:
            LaTeX string for the entry.
        """
        r, im = self._entries[i][j]
        if im == 0:
            return str(r)
        if r == 0:
            if im == 1:
                return "i"
            if im == -1:
                return "-i"
            return f"{im}i"
        sign = "+" if im > 0 else "-"
        abs_im = abs(im)
        im_str = "i" if abs_im == 1 else f"{abs_im}i"
        return f"{r}{sign}{im_str}"

    def multiply(self, other: "PauliMatrix") -> "PauliMatrix":
        """Multiply this matrix by another using complex arithmetic.

        Args:
            other: The matrix to multiply by.

        Returns:
            Product as a new PauliMatrix.
        """
        result = []
        for i in range(2):
            row = []
            for j in range(2):
                r, im = self._dot(i, j, other)
                row.append((r, im))
            result.append(row)
        return PauliMatrix(result[0][0], result[0][1],
                           result[1][0], result[1][1])

    def _dot(self, i: int, j: int,
             other: "PauliMatrix") -> tuple[int, int]:
        """Compute the (i,j) entry of the product via dot product.

        Args:
            i: Row index in self.
            j: Column index in other.
            other: The right-hand matrix.

        Returns:
            Tuple of (real, imag) for the result entry.
        """
        real = 0
        imag = 0
        for k in range(2):
            ar, ai = self._entries[i][k]
            br, bi = other.entry(k, j)
            real += ar * br - ai * bi
            imag += ar * bi + ai * br
        return real, imag

    def to_latex(self) -> str:
        """Format as a LaTeX pmatrix.

        Returns:
            LaTeX string for the 2x2 matrix.
        """
        rows = []
        for i in range(2):
            row_parts = [self.entry_latex(i, j) for j in range(2)]
            rows.append(" & ".join(row_parts))
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


@register
class IntegrationByPartsGenerator(StepGenerator):
    """Integration by parts: int(u dv) = uv - int(v du).

    Generates products of the form x^n * e^x or x * sin(x) and
    shows the integration by parts formula application with
    explicit identification of u, dv, du, and v.

    Input format:
        ``integrate by parts``

    Target format:
        ``\\int x e^x dx <step> u=x, dv=e^x dx
        <step> du=1 dx, v=e^x <step> uv - int(v du) = x e^x - \\int e^x dx
        <step> x e^x - e^x + C``

    Difficulty scaling:
        Difficulty 1-3: x * e^x with small coefficients.
        Difficulty 4-6: x * sin(x) or x * cos(x).
        Difficulty 7-8: x^2 * e^x (requires double application).

    Prerequisites:
        integral, product_rule.

    Example:
        >>> gen = IntegrationByPartsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'integration_by_parts'
    """

    _TEMPLATES = [
        {
            "label": "x*e^x",
            "u": "x", "dv": "e^x dx", "du": "1 dx", "v": "e^x",
            "uv": "x e^x", "remainder": "e^x",
            "answer": "x e^x - e^x + C",
        },
        {
            "label": "x*sin(x)",
            "u": "x", "dv": "\\sin(x) dx", "du": "1 dx", "v": "-\\cos(x)",
            "uv": "-x \\cos(x)", "remainder": "-\\cos(x)",
            "answer": "-x \\cos(x) + \\sin(x) + C",
        },
        {
            "label": "x*cos(x)",
            "u": "x", "dv": "\\cos(x) dx", "du": "1 dx", "v": "\\sin(x)",
            "uv": "x \\sin(x)", "remainder": "\\sin(x)",
            "answer": "x \\sin(x) + \\cos(x) + C",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "integration_by_parts"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["integral", "product_rule"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls product complexity.

        Returns:
            Natural language description.
        """
        return "integrate by parts"

    def _select_template(self, difficulty: int) -> dict:
        """Choose a template based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Template dictionary with all formula parts.
        """
        if difficulty <= 3:
            return self._TEMPLATES[0]
        idx = self._rng.randint(1, 2)
        return self._TEMPLATES[idx]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integration by parts problem.

        Args:
            difficulty: Controls product form selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        coeff = self._rng.randint(1, max(1, difficulty))
        tmpl = self._select_template(difficulty)
        if coeff == 1:
            problem = f"\\int {tmpl['label']} dx"
        else:
            problem = f"\\int {coeff}{tmpl['label']} dx"
        return problem, {"template": tmpl, "coeff": coeff}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate the integration by parts steps.

        Args:
            data: Solution data with template and coefficient.

        Returns:
            Steps showing u, dv identification and formula application.
        """
        t = data["template"]
        c = data["coeff"]
        prefix = f"{c}" if c > 1 else ""
        steps = [
            f"u={t['u']}, dv={t['dv']}",
            f"du={t['du']}, v={t['v']}",
            f"uv - \\int v du = {prefix}{t['uv']} - {prefix}\\int {t['remainder']} dx",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final antiderivative.

        Args:
            data: Solution data.

        Returns:
            LaTeX answer string.
        """
        t = data["template"]
        c = data["coeff"]
        if c == 1:
            return t["answer"]
        return f"{c}({t['answer']})"


@register
class PartialFractionsGenerator(StepGenerator):
    """Decompose a rational function into partial fractions.

    Generates (ax+b)/((x-r1)(x-r2)) and decomposes into
    A/(x-r1) + B/(x-r2) by solving for A and B via the
    cover-up method.

    Input format:
        ``decompose into partial fractions``

    Target format:
        ``\\frac{5x+1}{(x-1)(x+2)} <step> A(x+2)+B(x-1)=5x+1
        <step> x=1: 3A=6, A=2 <step> x=-2: -3B=-9, B=3
        <step> \\frac{2}{x-1}+\\frac{3}{x+2}``

    Difficulty scaling:
        Difficulty 1-3: roots in [-3, 3], coefficients in [1, 3].
        Difficulty 4-6: roots in [-5, 5], coefficients in [1, 6].
        Difficulty 7-8: roots in [-8, 8], coefficients in [1, 10].

    Prerequisites:
        factorisation, system_equations.

    Example:
        >>> gen = PartialFractionsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'partial_fractions'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "partial_fractions"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation", "system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls root and coefficient range.

        Returns:
            Natural language description.
        """
        return "decompose into partial fractions"

    def _root_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to root range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_root, max_root).
        """
        if difficulty <= 3:
            return -3, 3
        if difficulty <= 6:
            return -5, 5
        return -8, 8

    def _sample_distinct_roots(self, difficulty: int) -> tuple[int, int]:
        """Sample two distinct nonzero integer roots.

        Args:
            difficulty: Controls magnitude.

        Returns:
            Tuple of two distinct roots.
        """
        lo, hi = self._root_range(difficulty)
        r1 = 0
        while r1 == 0:
            r1 = self._rng.randint(lo, hi)
        r2 = r1
        while r2 == r1 or r2 == 0:
            r2 = self._rng.randint(lo, hi)
        return r1, r2

    def _factor_latex(self, root: int) -> str:
        """Format (x - root) in LaTeX.

        Args:
            root: The root value.

        Returns:
            LaTeX string for the linear factor.
        """
        if root > 0:
            return f"(x-{root})"
        return f"(x+{-root})"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a partial fractions problem.

        Args:
            difficulty: Controls root range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        r1, r2 = self._sample_distinct_roots(difficulty)
        a_coeff = self._rng.randint(1, max(1, difficulty))
        b_coeff = self._rng.randint(-max(1, difficulty), max(1, difficulty))

        denom_diff = r1 - r2
        num_at_r1 = a_coeff * r1 + b_coeff
        num_at_r2 = a_coeff * r2 + b_coeff
        big_a = Fraction(num_at_r1, denom_diff)
        big_b = Fraction(num_at_r2, -denom_diff)

        f1 = self._factor_latex(r1)
        f2 = self._factor_latex(r2)
        num_str = self._numerator_latex(a_coeff, b_coeff)
        problem = f"\\frac{{{num_str}}}{{{f1}{f2}}}"

        return problem, {
            "r1": r1, "r2": r2, "a_coeff": a_coeff, "b_coeff": b_coeff,
            "A": big_a, "B": big_b, "f1": f1, "f2": f2,
            "denom_diff": denom_diff, "num_at_r1": num_at_r1,
            "num_at_r2": num_at_r2,
        }

    def _numerator_latex(self, a: int, b: int) -> str:
        """Format the numerator ax+b in LaTeX.

        Args:
            a: Coefficient of x.
            b: Constant term.

        Returns:
            LaTeX string for the numerator.
        """
        if a == 1:
            x_part = "x"
        elif a == -1:
            x_part = "-x"
        else:
            x_part = f"{a}x"
        if b == 0:
            return x_part
        if b > 0:
            return f"{x_part}+{b}"
        return f"{x_part}{b}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cover-up method steps.

        Args:
            data: Solution data with roots and coefficients.

        Returns:
            Steps showing A and B computation.
        """
        r1, r2 = data["r1"], data["r2"]
        f1, f2 = data["f1"], data["f2"]
        return [
            f"A{f2}+B{f1}={self._numerator_latex(data['a_coeff'], data['b_coeff'])}",
            f"x={r1}: {data['denom_diff']}A={data['num_at_r1']}, A={data['A']}",
            f"x={r2}: {-data['denom_diff']}B={data['num_at_r2']}, B={data['B']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the partial fraction decomposition.

        Args:
            data: Solution data.

        Returns:
            LaTeX string with the decomposition.
        """
        f1 = data["f1"]
        f2 = data["f2"]
        return f"\\frac{{{data['A']}}}{{{f1}}}+\\frac{{{data['B']}}}{{{f2}}}"


@register
class SeriesConvergenceGenerator(StepGenerator):
    """Determine if an infinite series converges using standard tests.

    Applies the ratio test, comparison test, or p-series test to
    known series types (geometric, p-series, harmonic variants)
    and shows the step-by-step determination.

    Input format:
        ``determine series convergence``

    Target format:
        ``\\sum_{n=1}^{\\infty} \\frac{1}{n^2} <step> p-series with p=2
        <step> p=2 > 1 <step> converges``

    Difficulty scaling:
        Difficulty 1-3: geometric series with |r| clearly < or > 1.
        Difficulty 4-6: p-series with various p values.
        Difficulty 7-8: ratio test on factorial or exponential series.

    Prerequisites:
        limit, division.

    Example:
        >>> gen = SeriesConvergenceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'series_convergence'
    """

    _GEOMETRIC = [
        {"r_num": 1, "r_den": 2, "converges": True},
        {"r_num": 1, "r_den": 3, "converges": True},
        {"r_num": 2, "r_den": 3, "converges": True},
        {"r_num": 1, "r_den": 4, "converges": True},
        {"r_num": 3, "r_den": 2, "converges": False},
        {"r_num": 2, "r_den": 1, "converges": False},
        {"r_num": 5, "r_den": 4, "converges": False},
    ]

    _PSERIES = [
        {"p_num": 2, "p_den": 1, "converges": True},
        {"p_num": 3, "p_den": 1, "converges": True},
        {"p_num": 3, "p_den": 2, "converges": True},
        {"p_num": 1, "p_den": 1, "converges": False},
        {"p_num": 1, "p_den": 2, "converges": False},
        {"p_num": 2, "p_den": 3, "converges": False},
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "series_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["limit", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls series type.

        Returns:
            Natural language description.
        """
        return "determine series convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a convergence problem from known series.

        Args:
            difficulty: Controls series type selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._geometric_problem()
        return self._pseries_problem()

    def _geometric_problem(self) -> tuple[str, dict]:
        """Generate a geometric series convergence problem.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        entry = self._rng.choice(self._GEOMETRIC)
        r = Fraction(entry["r_num"], entry["r_den"])
        problem = f"\\sum_{{n=0}}^{{\\infty}} ({r})^n"
        return problem, {
            "type": "geometric", "r": r,
            "converges": entry["converges"],
        }

    def _pseries_problem(self) -> tuple[str, dict]:
        """Generate a p-series convergence problem.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        entry = self._rng.choice(self._PSERIES)
        p = Fraction(entry["p_num"], entry["p_den"])
        problem = f"\\sum_{{n=1}}^{{\\infty}} \\frac{{1}}{{n^{{{p}}}}}"
        return problem, {
            "type": "p-series", "p": p,
            "converges": entry["converges"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate convergence test steps.

        Args:
            data: Solution data with series type and parameters.

        Returns:
            Steps showing the test application.
        """
        if data["type"] == "geometric":
            return self._geometric_steps(data)
        return self._pseries_steps(data)

    def _geometric_steps(self, data: dict) -> list[str]:
        """Generate geometric series test steps.

        Args:
            data: Solution data with ratio.

        Returns:
            Steps showing |r| comparison to 1.
        """
        r = data["r"]
        abs_r = abs(r)
        cmp = "<" if data["converges"] else ">="
        return [
            f"geometric series with r={r}",
            f"|r|={abs_r} {cmp} 1",
        ]

    def _pseries_steps(self, data: dict) -> list[str]:
        """Generate p-series test steps.

        Args:
            data: Solution data with p value.

        Returns:
            Steps showing p comparison to 1.
        """
        p = data["p"]
        cmp = ">" if data["converges"] else "<="
        return [
            f"p-series with p={p}",
            f"p={p} {cmp} 1",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return convergence determination.

        Args:
            data: Solution data.

        Returns:
            'converges' or 'diverges'.
        """
        return "converges" if data["converges"] else "diverges"


@register
class DeMoivreGenerator(StepGenerator):
    """Apply De Moivre's theorem: (r*e^{i*theta})^n via polar form.

    Converts a complex number to polar form, raises to the n-th power
    using De Moivre's theorem, and converts back to rectangular form
    using exact trigonometric values.

    Input format:
        ``apply de moivre theorem``

    Target format:
        ``(1+i)^4 <step> r=\\sqrt{2}, \\theta=\\pi/4
        <step> r^4=(\\sqrt{2})^4=4 <step> 4\\theta=\\pi
        <step> 4(\\cos(\\pi)+i\\sin(\\pi)) <step> -4+0i <step> -4``

    Difficulty scaling:
        Difficulty 1-3: base (1+i) or (1-i), small powers 2-4.
        Difficulty 4-6: other unit-modulus angles, powers 3-6.
        Difficulty 7-8: powers 4-8.

    Prerequisites:
        complex_modulus, exponentiation.

    Example:
        >>> gen = DeMoivreGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'de_moivre'
    """

    _BASES = [
        {"a": 1, "b": 1, "r_sq": 2, "theta_label": "\\pi/4"},
        {"a": 1, "b": -1, "r_sq": 2, "theta_label": "-\\pi/4"},
        {"a": 0, "b": 1, "r_sq": 1, "theta_label": "\\pi/2"},
        {"a": -1, "b": 0, "r_sq": 1, "theta_label": "\\pi"},
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "de_moivre"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_modulus", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls base and exponent.

        Returns:
            Natural language description.
        """
        return "apply de moivre theorem"

    def _select_base(self, difficulty: int) -> dict:
        """Choose a complex base from the table.

        Args:
            difficulty: Difficulty level.

        Returns:
            Base dictionary with components and polar form.
        """
        if difficulty <= 3:
            return self._rng.choice(self._BASES[:2])
        return self._rng.choice(self._BASES)

    def _select_power(self, difficulty: int) -> int:
        """Choose the exponent n.

        Args:
            difficulty: Difficulty level.

        Returns:
            Integer exponent.
        """
        if difficulty <= 3:
            return self._rng.randint(2, 4)
        if difficulty <= 6:
            return self._rng.randint(3, 6)
        return self._rng.randint(4, 8)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a De Moivre problem.

        Args:
            difficulty: Controls base and power.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        base = self._select_base(difficulty)
        n = self._select_power(difficulty)
        a, b = base["a"], base["b"]

        theta = math.atan2(b, a)
        r = math.sqrt(a * a + b * b)
        r_n = r ** n
        n_theta = n * theta
        result_a = round(r_n * math.cos(n_theta))
        result_b = round(r_n * math.sin(n_theta))

        z_str = self._complex_latex(a, b)
        problem = f"({z_str})^{{{n}}}"

        return problem, {
            "a": a, "b": b, "n": n, "r_sq": base["r_sq"],
            "theta_label": base["theta_label"],
            "r_n": r_n, "n_theta_label": f"{n}{base['theta_label']}",
            "result_a": result_a, "result_b": result_b,
        }

    def _complex_latex(self, a: int, b: int) -> str:
        """Format a+bi in LaTeX.

        Args:
            a: Real part.
            b: Imaginary part.

        Returns:
            LaTeX string.
        """
        if b == 0:
            return str(a)
        if a == 0:
            if b == 1:
                return "i"
            if b == -1:
                return "-i"
            return f"{b}i"
        sign = "+" if b > 0 else "-"
        abs_b = abs(b)
        b_str = "i" if abs_b == 1 else f"{abs_b}i"
        return f"{a}{sign}{b_str}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate De Moivre computation steps.

        Args:
            data: Solution data with polar form and result.

        Returns:
            Steps showing polar conversion, power, and back-conversion.
        """
        r_sq = data["r_sq"]
        n = data["n"]
        r_n = data["r_n"]
        r_n_int = int(round(r_n))

        if r_sq == 1:
            r_str = "1"
        elif r_sq == 2:
            r_str = "\\sqrt{2}"
        else:
            r_str = f"\\sqrt{{{r_sq}}}"

        return [
            f"r={r_str}, \\theta={data['theta_label']}",
            f"r^{{{n}}}=({r_str})^{{{n}}}={r_n_int}",
            f"n\\theta={data['n_theta_label']}",
            f"{r_n_int}(\\cos({data['n_theta_label']})+i\\sin({data['n_theta_label']}))",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the result in rectangular form.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the result.
        """
        return self._complex_latex(data["result_a"], data["result_b"])


@register
class ComplexDivisionGenerator(StepGenerator):
    """Divide two complex numbers via conjugate multiplication.

    Computes (a+bi)/(c+di) by multiplying numerator and denominator
    by the conjugate (c-di), showing each step of the process.

    Input format:
        ``divide two complex numbers``

    Target format:
        ``\\frac{3+2i}{1-4i} <step> multiply by conjugate \\frac{1+4i}{1+4i}
        <step> num: (3+2i)(1+4i)=-5+14i <step> den: 1^2+4^2=17
        <step> \\frac{-5}{17}+\\frac{14}{17}i``

    Difficulty scaling:
        Difficulty 1-3: components in [-3, 3].
        Difficulty 4-6: components in [-6, 6].
        Difficulty 7-8: components in [-10, 10].

    Prerequisites:
        complex_arithmetic.

    Example:
        >>> gen = ComplexDivisionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complex_division'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complex_division"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Natural language description.
        """
        return "divide two complex numbers"

    def _component_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to component range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min, max).
        """
        if difficulty <= 3:
            return -3, 3
        if difficulty <= 6:
            return -6, 6
        return -10, 10

    def _sample_nonzero(self, lo: int, hi: int) -> int:
        """Sample a nonzero integer in [lo, hi].

        Args:
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Nonzero integer.
        """
        val = 0
        while val == 0:
            val = self._rng.randint(lo, hi)
        return val

    def _complex_latex(self, a: int, b: int) -> str:
        """Format a+bi in LaTeX.

        Args:
            a: Real part.
            b: Imaginary part.

        Returns:
            LaTeX string.
        """
        if b == 0:
            return str(a)
        if a == 0:
            if b == 1:
                return "i"
            if b == -1:
                return "-i"
            return f"{b}i"
        sign = "+" if b > 0 else "-"
        abs_b = abs(b)
        b_str = "i" if abs_b == 1 else f"{abs_b}i"
        return f"{a}{sign}{b_str}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complex division problem.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._component_range(difficulty)
        a = self._sample_nonzero(lo, hi)
        b = self._sample_nonzero(lo, hi)
        c = self._sample_nonzero(lo, hi)
        d = self._sample_nonzero(lo, hi)

        num_real = a * c + b * d
        num_imag = b * c - a * d
        den = c * c + d * d
        real_frac = Fraction(num_real, den)
        imag_frac = Fraction(num_imag, den)

        z1 = self._complex_latex(a, b)
        z2 = self._complex_latex(c, d)
        problem = f"\\frac{{{z1}}}{{{z2}}}"

        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "num_real": num_real, "num_imag": num_imag,
            "den": den, "real_frac": real_frac, "imag_frac": imag_frac,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conjugate multiplication steps.

        Args:
            data: Solution data with all intermediate values.

        Returns:
            Steps showing conjugate, numerator, denominator computation.
        """
        c, d = data["c"], data["d"]
        conj = self._complex_latex(c, -d)
        num_str = self._complex_latex(data["num_real"], data["num_imag"])
        return [
            f"multiply by conjugate \\frac{{{conj}}}{{{conj}}}",
            f"numerator: {num_str}",
            f"denominator: {c}^2+{d}^2={data['den']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the quotient as a fraction.

        Args:
            data: Solution data.

        Returns:
            LaTeX fraction string.
        """
        r = data["real_frac"]
        i = data["imag_frac"]
        if i == 0:
            return str(r)
        if r == 0:
            return f"{i}i"
        sign = "+" if i > 0 else ""
        return f"{r}{sign}{i}i"


@register
class GroupOrderGenerator(StepGenerator):
    """Find the order of an element in Z_n.

    Computes a, a^2, a^3, ... mod n until reaching the identity
    element 1. The order is the smallest positive k where a^k = 1 mod n.

    Input format:
        ``find group element order``

    Target format:
        ``\\text{ord}(3) \\text{ in } Z_7 <step> 3^1=3
        <step> 3^2=9 \\equiv 2 <step> 3^3=6 <step> 3^4=18 \\equiv 4
        <step> 3^5=12 \\equiv 5 <step> 3^6=15 \\equiv 1 <step> 6``

    Difficulty scaling:
        Difficulty 1-3: small primes n in [5, 11], a in [2, n-1].
        Difficulty 4-6: primes n in [7, 19].
        Difficulty 7-8: primes n in [11, 29].

    Prerequisites:
        modular, multiplication.

    Example:
        >>> gen = GroupOrderGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'group_order'
    """

    _SMALL_PRIMES = [5, 7, 11]
    _MEDIUM_PRIMES = [7, 11, 13, 17, 19]
    _LARGE_PRIMES = [11, 13, 17, 19, 23, 29]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "group_order"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["modular", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Natural language description.
        """
        return "find group element order"

    def _select_prime(self, difficulty: int) -> int:
        """Choose a prime modulus based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A prime number.
        """
        if difficulty <= 3:
            return self._rng.choice(self._SMALL_PRIMES)
        if difficulty <= 6:
            return self._rng.choice(self._MEDIUM_PRIMES)
        return self._rng.choice(self._LARGE_PRIMES)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a group order problem.

        Args:
            difficulty: Controls modulus size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._select_prime(difficulty)
        a = self._rng.randint(2, n - 1)
        powers = self._compute_powers(a, n)
        order = len(powers)

        problem = f"\\text{{ord}}({a}) \\text{{ in }} Z_{{{n}}}"
        return problem, {"a": a, "n": n, "powers": powers, "order": order}

    def _compute_powers(self, a: int, n: int) -> list[tuple[int, int]]:
        """Compute successive powers of a mod n until reaching 1.

        Args:
            a: Base element.
            n: Modulus (group order).

        Returns:
            List of (exponent, result_mod_n) tuples.
        """
        powers: list[tuple[int, int]] = []
        current = 1
        for k in range(1, n + 1):
            current = (current * a) % n
            powers.append((k, current))
            if current == 1:
                break
        return powers

    def _create_steps(self, data: dict) -> list[str]:
        """Generate power computation steps.

        Args:
            data: Solution data with power sequence.

        Returns:
            Steps showing each power mod n.
        """
        a, n = data["a"], data["n"]
        steps: list[str] = []
        for k, result in data["powers"]:
            raw = a ** k
            if raw == result:
                steps.append(f"{a}^{{{k}}}={result}")
            else:
                steps.append(f"{a}^{{{k}}}={raw} \\equiv {result} \\pmod{{{n}}}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the element order.

        Args:
            data: Solution data.

        Returns:
            String representation of the order.
        """
        return str(data["order"])


@register
class NumberBaseArithmeticGenerator(StepGenerator):
    """Addition in a non-decimal base with carry propagation.

    Generates two numbers in base b (b in 2-9) and performs column
    addition showing the carry chain, analogous to decimal addition
    but with carry at b instead of 10.

    Input format:
        ``add in base 7``

    Target format:
        ``324_7 + 156_7 <step> 4+6=10, 10/7=1r3, write 3 carry 1
        <step> 2+5+1=8, 8/7=1r1, write 1 carry 1
        <step> 3+1+1=5 <step> 513_7``

    Difficulty scaling:
        Difficulty 1-2: 2-digit numbers, base 5-8.
        Difficulty 3-5: 3-digit numbers, base 3-8.
        Difficulty 6-8: 4-digit numbers, base 2-9.

    Prerequisites:
        addition, base_conversion.

    Example:
        >>> gen = NumberBaseArithmeticGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'number_base_arithmetic'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "number_base_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "base_conversion"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls digit count and base.

        Returns:
            Natural language description.
        """
        return "add in non-decimal base"

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to (num_digits, base).

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (digit_count, base).
        """
        if difficulty <= 2:
            return 2, self._rng.randint(5, 8)
        if difficulty <= 5:
            return 3, self._rng.randint(3, 8)
        return 4, self._rng.randint(2, 9)

    def _random_base_number(self, num_digits: int, base: int) -> list[int]:
        """Generate a random number as a list of base-b digits (MSD first).

        Args:
            num_digits: Number of digits.
            base: The base.

        Returns:
            List of digits in [0, base-1], first digit nonzero.
        """
        digits = [self._rng.randint(1, base - 1)]
        for _ in range(num_digits - 1):
            digits.append(self._rng.randint(0, base - 1))
        return digits

    def _digits_to_str(self, digits: list[int]) -> str:
        """Convert digit list to string.

        Args:
            digits: List of digits.

        Returns:
            Concatenated digit string.
        """
        return "".join(str(d) for d in digits)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a base-b addition problem.

        Args:
            difficulty: Controls digit count and base.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num_digits, base = self._params(difficulty)
        a_digits = self._random_base_number(num_digits, base)
        b_digits = self._random_base_number(num_digits, base)

        result_digits, carries = self._add_base(a_digits, b_digits, base)

        a_str = self._digits_to_str(a_digits)
        b_str = self._digits_to_str(b_digits)
        r_str = self._digits_to_str(result_digits)

        problem = f"{a_str}_{{{base}}} + {b_str}_{{{base}}}"
        return problem, {
            "a_digits": a_digits, "b_digits": b_digits,
            "result_str": r_str, "base": base, "carries": carries,
        }

    def _add_base(self, a: list[int], b: list[int],
                  base: int) -> tuple[list[int], list[int]]:
        """Add two base-b numbers right-to-left.

        Args:
            a: First operand digits (MSD first).
            b: Second operand digits (MSD first).
            base: The base.

        Returns:
            Tuple of (result_digits, carry_list).
        """
        a_rev = list(reversed(a))
        b_rev = list(reversed(b))
        result: list[int] = []
        carries: list[int] = []
        carry = 0

        for i in range(len(a_rev)):
            total = a_rev[i] + b_rev[i] + carry
            carry = total // base
            result.append(total % base)
            carries.append(carry)

        if carry > 0:
            result.append(carry)
        result.reverse()
        return result, carries

    def _create_steps(self, data: dict) -> list[str]:
        """Generate column addition steps in base b.

        Args:
            data: Solution data with digits and carries.

        Returns:
            Steps showing each column addition.
        """
        a = list(reversed(data["a_digits"]))
        b = list(reversed(data["b_digits"]))
        base = data["base"]
        steps: list[str] = []
        carry = 0

        for i in range(len(a)):
            total = a[i] + b[i] + carry
            new_carry = total // base
            digit = total % base
            if carry > 0:
                step = f"{a[i]}+{b[i]}+{carry}={total}"
            else:
                step = f"{a[i]}+{b[i]}={total}"
            if total >= base:
                step += f", {total}/{base}={new_carry}r{digit}, write {digit} carry {new_carry}"
            carry = new_carry
            steps.append(step)

        if carry > 0:
            steps.append(f"carry={carry}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the sum in base b.

        Args:
            data: Solution data.

        Returns:
            Result string with base subscript.
        """
        return f"{data['result_str']}_{{{data['base']}}}"


@register
class SetOperationsGenerator(StepGenerator):
    """Compute |A union B| using inclusion-exclusion.

    Generates two finite sets with a known intersection and
    applies |A union B| = |A| + |B| - |A intersect B|.

    Input format:
        ``compute set union size``

    Target format:
        ``A=\\{1,2,3,5\\}, B=\\{2,3,7,8\\} <step> |A|=4
        <step> |B|=4 <step> A \\cap B=\\{2,3\\}, |A \\cap B|=2
        <step> |A \\cup B|=4+4-2=6 <step> 6``

    Difficulty scaling:
        Difficulty 1-3: sets of size 3-5, elements in [1, 10].
        Difficulty 4-6: sets of size 4-7, elements in [1, 20].
        Difficulty 7-8: sets of size 5-10, elements in [1, 30].

    Prerequisites:
        addition, subtraction.

    Example:
        >>> gen = SetOperationsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'set_operations'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "set_operations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Natural language description.
        """
        return "compute set union size"

    def _set_params(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to set size range and element range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_size, max_size, max_element).
        """
        if difficulty <= 3:
            return 3, 5, 10
        if difficulty <= 6:
            return 4, 7, 20
        return 5, 10, 30

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two sets with known intersection.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        min_sz, max_sz, max_el = self._set_params(difficulty)
        size_a = self._rng.randint(min_sz, max_sz)
        size_b = self._rng.randint(min_sz, max_sz)
        overlap = self._rng.randint(1, min(size_a, size_b) - 1)

        pool = list(range(1, max_el + 1))
        self._rng.shuffle(pool)

        common = sorted(pool[:overlap])
        only_a = sorted(pool[overlap:overlap + size_a - overlap])
        only_b = sorted(pool[overlap + size_a - overlap:
                             overlap + size_a - overlap + size_b - overlap])

        set_a = sorted(common + only_a)
        set_b = sorted(common + only_b)
        intersection = common
        union_size = len(set(set_a) | set(set_b))

        a_str = ",".join(str(x) for x in set_a)
        b_str = ",".join(str(x) for x in set_b)
        problem = f"A=\\{{{a_str}\\}}, B=\\{{{b_str}\\}}"

        return problem, {
            "set_a": set_a, "set_b": set_b,
            "intersection": intersection,
            "size_a": len(set_a), "size_b": len(set_b),
            "inter_size": len(intersection),
            "union_size": union_size,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inclusion-exclusion steps.

        Args:
            data: Solution data with set information.

        Returns:
            Steps showing sizes and the formula.
        """
        inter_str = ",".join(str(x) for x in data["intersection"])
        sa = data["size_a"]
        sb = data["size_b"]
        si = data["inter_size"]
        su = data["union_size"]
        return [
            f"|A|={sa}",
            f"|B|={sb}",
            f"A \\cap B=\\{{{inter_str}\\}}, |A \\cap B|={si}",
            f"|A \\cup B|={sa}+{sb}-{si}={su}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the union size.

        Args:
            data: Solution data.

        Returns:
            String representation of |A union B|.
        """
        return str(data["union_size"])


@register
class FourierCoefficientGenerator(StepGenerator):
    """Compute Fourier coefficients for simple periodic functions.

    Uses square waves and triangle waves with known closed-form
    Fourier coefficients. Shows the integral setup and evaluation.

    Input format:
        ``compute fourier coefficient``

    Target format:
        ``b_n \\text{ for square wave, period } 2\\pi <step>
        b_n = \\frac{2}{\\pi} \\int_0^{\\pi} \\sin(nx) dx
        <step> = \\frac{2}{n\\pi}[-\\cos(nx)]_0^{\\pi}
        <step> = \\frac{2}{n\\pi}(1-(-1)^n) <step> b_3=\\frac{4}{3\\pi}``

    Difficulty scaling:
        Difficulty 1-3: square wave b_n for odd n.
        Difficulty 4-6: square wave for general n.
        Difficulty 7-8: triangle wave a_n.

    Prerequisites:
        definite_integral.

    Example:
        >>> gen = FourierCoefficientGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'fourier_coefficient'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "fourier_coefficient"

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
            difficulty: Controls wave type and harmonic.

        Returns:
            Natural language description.
        """
        return "compute fourier coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fourier coefficient problem.

        Args:
            difficulty: Controls wave type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 6:
            return self._square_wave_problem(difficulty)
        return self._triangle_wave_problem(difficulty)

    def _square_wave_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a square wave b_n problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([1, 3, 5, 7])
        else:
            n = self._rng.randint(1, 8)

        cos_n_pi = (-1) ** n
        coeff_num = 2 * (1 - cos_n_pi)
        coeff_den = n

        problem = f"b_{{{n}}} \\text{{ for square wave, period }} 2\\pi"
        return problem, {
            "wave": "square", "coeff_type": "b", "n": n,
            "cos_n_pi": cos_n_pi, "coeff_num": coeff_num,
            "coeff_den": coeff_den,
        }

    def _triangle_wave_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a triangle wave a_n problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.choice([1, 3, 5, 7])

        sign = (-1) ** ((n - 1) // 2)
        coeff_num = 8 * sign
        coeff_den = n * n

        problem = f"a_{{{n}}} \\text{{ for triangle wave, period }} 2\\pi"
        return problem, {
            "wave": "triangle", "coeff_type": "a", "n": n,
            "coeff_num": coeff_num, "coeff_den": coeff_den,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coefficient computation steps.

        Args:
            data: Solution data with wave type and n.

        Returns:
            Steps showing the integral and evaluation.
        """
        if data["wave"] == "square":
            return self._square_steps(data)
        return self._triangle_steps(data)

    def _square_steps(self, data: dict) -> list[str]:
        """Generate square wave b_n steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the integral evaluation.
        """
        n = data["n"]
        cos_val = data["cos_n_pi"]
        factor = 1 - cos_val
        return [
            f"b_{{{n}}} = \\frac{{2}}{{\\pi}} \\int_0^{{\\pi}} \\sin({n}x) dx",
            f"= \\frac{{2}}{{{n}\\pi}}[-\\cos({n}x)]_0^{{\\pi}}",
            f"= \\frac{{2}}{{{n}\\pi}}(1-({cos_val})) = \\frac{{2}}{{{n}\\pi}}({factor})",
        ]

    def _triangle_steps(self, data: dict) -> list[str]:
        """Generate triangle wave a_n steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the coefficient formula.
        """
        n = data["n"]
        num = data["coeff_num"]
        den = data["coeff_den"]
        return [
            f"a_{{{n}}} = \\frac{{8}}{{n^2 \\pi^2}} (-1)^{{(n-1)/2}} for odd n",
            f"n={n}: (-1)^{{{(n - 1) // 2}}}={(-1) ** ((n - 1) // 2)}",
            f"a_{{{n}}} = \\frac{{{num}}}{{{den}\\pi^2}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Fourier coefficient value.

        Args:
            data: Solution data.

        Returns:
            LaTeX fraction string.
        """
        num = data["coeff_num"]
        den = data["coeff_den"]
        if num == 0:
            return "0"
        f = Fraction(num, den)
        if data["wave"] == "square":
            return f"\\frac{{{f.numerator}}}{{{f.denominator}\\pi}}"
        return f"\\frac{{{f.numerator}}}{{{f.denominator}\\pi^2}}"


@register
class TensorProductGenerator(StepGenerator):
    """Compute the tensor (Kronecker) product of two 2-vectors.

    Given |psi> and |phi> as 2-element vectors, computes
    |psi> tensor |phi> as a 4-element vector using the
    Kronecker product.

    Input format:
        ``compute tensor product``

    Target format:
        ``|\\psi\\rangle \\otimes |\\phi\\rangle <step>
        \\begin{pmatrix} a \\\\ b \\end{pmatrix} \\otimes
        \\begin{pmatrix} c \\\\ d \\end{pmatrix}
        <step> a*c=... <step> a*d=... <step> b*c=... <step> b*d=...
        <step> \\begin{pmatrix} ac \\\\ ad \\\\ bc \\\\ bd \\end{pmatrix}``

    Difficulty scaling:
        Difficulty 1-3: entries in [-2, 2].
        Difficulty 4-6: entries in [-4, 4].
        Difficulty 7-8: entries in [-6, 6].

    Prerequisites:
        matrix_multiply.

    Example:
        >>> gen = TensorProductGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'tensor_product'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "tensor_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Natural language description.
        """
        return "compute tensor product"

    def _entry_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to entry range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min, max).
        """
        if difficulty <= 3:
            return -2, 2
        if difficulty <= 6:
            return -4, 4
        return -6, 6

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tensor product problem.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._entry_range(difficulty)
        psi = [self._rng.randint(lo, hi) for _ in range(2)]
        phi = [self._rng.randint(lo, hi) for _ in range(2)]
        result = [psi[0] * phi[0], psi[0] * phi[1],
                  psi[1] * phi[0], psi[1] * phi[1]]

        psi_str = f"\\begin{{pmatrix}} {psi[0]} \\\\ {psi[1]} \\end{{pmatrix}}"
        phi_str = f"\\begin{{pmatrix}} {phi[0]} \\\\ {phi[1]} \\end{{pmatrix}}"
        problem = f"{psi_str} \\otimes {phi_str}"

        return problem, {"psi": psi, "phi": phi, "result": result}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kronecker product steps.

        Args:
            data: Solution data with vectors and result.

        Returns:
            Steps showing each element computation.
        """
        psi, phi = data["psi"], data["phi"]
        return [
            f"{psi[0]}*{phi[0]}={data['result'][0]}",
            f"{psi[0]}*{phi[1]}={data['result'][1]}",
            f"{psi[1]}*{phi[0]}={data['result'][2]}",
            f"{psi[1]}*{phi[1]}={data['result'][3]}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the tensor product as a 4-vector.

        Args:
            data: Solution data.

        Returns:
            LaTeX pmatrix string.
        """
        r = data["result"]
        entries = " \\\\ ".join(str(x) for x in r)
        return f"\\begin{{pmatrix}} {entries} \\end{{pmatrix}}"


@register
class PauliProductGenerator(StepGenerator):
    """Multiply two 2x2 Pauli matrices.

    Shows the full 2x2 matrix multiplication for products of
    Pauli matrices (I, sigma_x, sigma_y, sigma_z), demonstrating
    the algebra sigma_x * sigma_y = i*sigma_z, etc.

    Input format:
        ``multiply pauli matrices``

    Target format:
        ``\\sigma_x \\sigma_y <step>
        c_{11}=0*0+1*(0-i)=-i <step> c_{12}=0*(0+i)+1*0=0
        <step> ... <step>
        \\begin{pmatrix} i & 0 \\\\ 0 & -i \\end{pmatrix} = i\\sigma_z``

    Difficulty scaling:
        Difficulty 1-3: products involving sigma_z.
        Difficulty 4-6: all pairwise products.
        Difficulty 7-8: triple products.

    Prerequisites:
        matrix_multiply.

    Example:
        >>> gen = PauliProductGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'pauli_product'
    """

    _PAULIS = {
        "I": PauliMatrix((1, 0), (0, 0), (0, 0), (1, 0)),
        "\\sigma_x": PauliMatrix((0, 0), (1, 0), (1, 0), (0, 0)),
        "\\sigma_y": PauliMatrix((0, 0), (0, -1), (0, 1), (0, 0)),
        "\\sigma_z": PauliMatrix((1, 0), (0, 0), (0, 0), (-1, 0)),
    }

    _NAMES = ["I", "\\sigma_x", "\\sigma_y", "\\sigma_z"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "pauli_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls product complexity.

        Returns:
            Natural language description.
        """
        return "multiply pauli matrices"

    def _select_pair(self, difficulty: int) -> tuple[str, str]:
        """Choose two Pauli matrices based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of two Pauli matrix names.
        """
        if difficulty <= 3:
            names = ["\\sigma_x", "\\sigma_y", "\\sigma_z"]
        else:
            names = self._NAMES
        n1 = self._rng.choice(names)
        n2 = self._rng.choice(names)
        return n1, n2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Pauli product problem.

        Args:
            difficulty: Controls matrix selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n1, n2 = self._select_pair(difficulty)
        m1 = self._PAULIS[n1]
        m2 = self._PAULIS[n2]
        product = m1.multiply(m2)

        problem = f"{n1} \\cdot {n2}"
        return problem, {
            "n1": n1, "n2": n2, "m1": m1, "m2": m2, "product": product,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matrix multiplication steps.

        Args:
            data: Solution data with matrices and product.

        Returns:
            Steps showing each cell computation.
        """
        m1, m2, product = data["m1"], data["m2"], data["product"]
        steps: list[str] = []
        for i in range(2):
            for j in range(2):
                step = self._cell_step(m1, m2, product, i, j)
                steps.append(step)
        return steps

    def _cell_step(self, m1: PauliMatrix, m2: PauliMatrix,
                   product: PauliMatrix, i: int, j: int) -> str:
        """Format one cell computation step.

        Args:
            m1: Left matrix.
            m2: Right matrix.
            product: Product matrix.
            i: Row index.
            j: Column index.

        Returns:
            Step string showing the dot product.
        """
        terms = []
        for k in range(2):
            terms.append(f"({m1.entry_latex(i, k)})({m2.entry_latex(k, j)})")
        result = product.entry_latex(i, j)
        return f"c_{{{i + 1}{j + 1}}}={'+'.join(terms)}={result}"

    def _create_answer(self, data: dict) -> str:
        """Return the product matrix in LaTeX.

        Args:
            data: Solution data.

        Returns:
            LaTeX pmatrix string.
        """
        return data["product"].to_latex()


@register
class BlochCoordsGenerator(StepGenerator):
    """Convert a qubit state to Bloch sphere coordinates.

    Given alpha|0> + beta|1>, computes the Bloch sphere angles
    theta = 2*arccos(|alpha|) and phi = arg(beta/alpha) using
    exact trigonometric values.

    Input format:
        ``compute bloch coordinates``

    Target format:
        ``\\frac{1}{\\sqrt{2}}|0\\rangle + \\frac{1}{\\sqrt{2}}|1\\rangle
        <step> |\\alpha|=\\frac{1}{\\sqrt{2}} <step>
        \\theta=2\\arccos(\\frac{1}{\\sqrt{2}})=\\frac{\\pi}{2}
        <step> \\phi=\\arg(1)=0 <step> (\\theta,\\phi)=(\\pi/2, 0)``

    Difficulty scaling:
        Difficulty 1-3: equal superposition states.
        Difficulty 4-6: states with known exact angles.
        Difficulty 7-8: states with phase factors.

    Prerequisites:
        complex_modulus, euler_formula.

    Example:
        >>> gen = BlochCoordsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bloch_coords'
    """

    _STATES = [
        {
            "alpha": "1", "beta": "0",
            "alpha_mod": "1", "theta": "0", "phi": "0",
            "label": "|0\\rangle",
        },
        {
            "alpha": "0", "beta": "1",
            "alpha_mod": "0", "theta": "\\pi", "phi": "0",
            "label": "|1\\rangle",
        },
        {
            "alpha": "\\frac{1}{\\sqrt{2}}", "beta": "\\frac{1}{\\sqrt{2}}",
            "alpha_mod": "\\frac{1}{\\sqrt{2}}",
            "theta": "\\frac{\\pi}{2}", "phi": "0",
            "label": "|+\\rangle",
        },
        {
            "alpha": "\\frac{1}{\\sqrt{2}}", "beta": "-\\frac{1}{\\sqrt{2}}",
            "alpha_mod": "\\frac{1}{\\sqrt{2}}",
            "theta": "\\frac{\\pi}{2}", "phi": "\\pi",
            "label": "|-\\rangle",
        },
        {
            "alpha": "\\frac{1}{\\sqrt{2}}", "beta": "\\frac{i}{\\sqrt{2}}",
            "alpha_mod": "\\frac{1}{\\sqrt{2}}",
            "theta": "\\frac{\\pi}{2}", "phi": "\\frac{\\pi}{2}",
            "label": "|+i\\rangle",
        },
        {
            "alpha": "\\frac{1}{\\sqrt{2}}", "beta": "\\frac{-i}{\\sqrt{2}}",
            "alpha_mod": "\\frac{1}{\\sqrt{2}}",
            "theta": "\\frac{\\pi}{2}", "phi": "-\\frac{\\pi}{2}",
            "label": "|-i\\rangle",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bloch_coords"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_modulus", "euler_formula"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls state complexity.

        Returns:
            Natural language description.
        """
        return "compute bloch coordinates"

    def _select_state(self, difficulty: int) -> dict:
        """Choose a qubit state based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            State dictionary.
        """
        if difficulty <= 3:
            return self._rng.choice(self._STATES[:4])
        return self._rng.choice(self._STATES)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bloch sphere coordinate problem.

        Args:
            difficulty: Controls state selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        state = self._select_state(difficulty)
        problem = f"{state['alpha']}|0\\rangle + {state['beta']}|1\\rangle"
        return problem, {"state": state}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bloch coordinate computation steps.

        Args:
            data: Solution data with state information.

        Returns:
            Steps showing modulus and angle computation.
        """
        s = data["state"]
        return [
            f"|\\alpha|={s['alpha_mod']}",
            f"\\theta=2\\arccos({s['alpha_mod']})={s['theta']}",
            f"\\phi=\\arg(\\beta/\\alpha)={s['phi']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Bloch coordinates.

        Args:
            data: Solution data.

        Returns:
            Coordinate pair string.
        """
        s = data["state"]
        return f"(\\theta,\\phi)=({s['theta']}, {s['phi']})"
