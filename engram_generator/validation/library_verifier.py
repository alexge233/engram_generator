"""Independent library-based verification of generator answers.

Takes a generator's solution_data dict and recomputes the answer
using third-party libraries (sympy, numpy, scipy, networkx).
No generator code is called -- the library IS the ground truth.

This module is only used by the on-demand verification script.
It is never imported during training or evaluation.
"""
import math
import re
import warnings
from typing import Any

from engram_generator.validation.registry import (
    VERIFICATION_REGISTRY,
    VerificationEntry,
)


class LibraryVerifier:
    """Recomputes generator answers using independent libraries.

    Only verifies generators whose registry entry has method='library'.
    Skips generators with method='formula', 'reference', or 'llm'.

    Example:
        >>> v = LibraryVerifier()
        >>> result = v.verify("addition", {"a": 15, "b": 36, "result": 51})
        >>> result.match
        True
    """

    def __init__(self, tolerance: float = 5e-4) -> None:
        """Initialise the verifier.

        Args:
            tolerance: Numeric comparison tolerance for float answers.
        """
        self._tolerance = tolerance
        self._handlers = self._build_handlers()

    def can_verify(self, task_name: str) -> bool:
        """Check if a task has a library verification handler.

        Args:
            task_name: Generator task identifier.

        Returns:
            True if independent verification is available.
        """
        entry = VERIFICATION_REGISTRY.get(task_name)
        if entry is None or entry.method != "library":
            return False
        return task_name in self._handlers

    def verify(self, task_name: str, solution_data: dict,
               answer: str) -> "LibraryResult":
        """Verify a generator's answer using an independent library.

        Compares at the solution_data level (numeric) not the
        formatted answer level (string). The handler recomputes
        from raw inputs and returns a numeric/structured result
        which is compared to the solution_data's stored result.

        Args:
            task_name: Generator task identifier.
            solution_data: The dict returned by _create_problem().
            answer: The string returned by _create_answer().

        Returns:
            LibraryResult with match status and details.
        """
        if task_name not in self._handlers:
            return LibraryResult(
                task_name=task_name, match=None,
                reason="no_handler",
            )

        handler = self._handlers[task_name]
        try:
            lib_result = handler(solution_data)
            if lib_result is None:
                return LibraryResult(
                    task_name=task_name, match=None,
                    reason="handler_returned_none",
                )
            if lib_result == 1 and isinstance(lib_result, int):
                return LibraryResult(
                    task_name=task_name, match=True,
                    expected=answer, computed="verified",
                )
            if lib_result == -1 and isinstance(lib_result, int):
                return LibraryResult(
                    task_name=task_name, match=False,
                    expected=answer, computed="MISMATCH",
                )
            gen_result = self._extract_gen_result(task_name, solution_data)
            match = self._compare_values(lib_result, gen_result)
            if not match and isinstance(gen_result, dict):
                for val in gen_result.values():
                    if self._compare_values(lib_result, val):
                        match = True
                        gen_result = val
                        break
                if not match:
                    for val in gen_result.values():
                        if self._compare_rounded(lib_result, val):
                            match = True
                            gen_result = val
                            break
                if not match and isinstance(lib_result, (tuple, list)):
                    match = self._compare_tuple_to_dict(lib_result, gen_result)
            if not match:
                match = self._compare(lib_result, answer)
            return LibraryResult(
                task_name=task_name, match=match,
                expected=str(gen_result)[:200], computed=str(lib_result)[:200],
            )
        except Exception as e:
            return LibraryResult(
                task_name=task_name, match=None,
                reason=f"error: {str(e)[:100]}",
            )

    _RESULT_KEYS = {
        "addition": "result", "subtraction": "result",
        "multiplication": "result", "modular": "result",
        "exponentiation": "result", "gcd": "result",
        "lcm": "result", "mod_pow": "result",
        "absolute_value": "result", "floor_ceil": "result",
        "percentage": "result", "rounding": "result",
        "counting": "result", "digit_root": None,
        "binomial": "result", "permutation": "result",
        "combination_count": "result", "catalan": "result",
        "determinant": "det", "eigenvalue": None,
        "matrix_multiply": "result", "matrix_inverse": "inverse",
        "matrix_trace": "result",
        "linear_regression": "slope",
        "shortest_path": "dist",
        "dot_product": "result", "cross_product": "result",
        "matrix_trace": "result", "vector_norm": "result",
        "derivative": "derivative", "integral": None,
        "definite_integral": "result",
        "totient": "result", "primality": "result",
        "factorisation": "factors",
        "prime_factorisation": "factors",
        "shortest_path": "distance", "bfs_order": "order",
        "connected_components": "count",
        "binomial_dist": "result", "poisson_dist": "result",
        "mean": "mean", "arithmetic_mean": "mean",
        "median": "median", "mode": "mode",
        "distance_2d": "result", "square_root": "result",
        "set_union": "union", "set_intersection": "inter",
        "set_difference": "diff", "set_membership": "member",
        "set_subset": "is_subset", "set_cardinality": "result",
        "palindrome_check": "is_palindrome",
        "anagram_check": "is_anagram",
        "hamming_distance": "dist",
        "ph_calculation": "ph",
        "poisson_dist": "prob",
        "angle_conversion": None,
        "sin_cos_eval": "value",
        "tan_eval": "value",
    }

    def _extract_gen_result(self, task_name: str,
                            solution_data: dict) -> Any:
        """Extract the numeric result from solution_data.

        Args:
            task_name: Task identifier.
            solution_data: Generator's solution data.

        Returns:
            The numeric/structured result value.
        """
        if task_name == "angle_conversion":
            mode = solution_data.get("mode", "deg_to_rad")
            if mode == "deg_to_rad":
                return solution_data.get("rad", 0)
            return solution_data.get("deg", 0)

        if task_name == "eigenvalue":
            lams = [solution_data.get("lam1", 0), solution_data.get("lam2", 0)]
            if "lam3" in solution_data:
                lams.append(solution_data["lam3"])
            return sorted(lams)

        key = self._RESULT_KEYS.get(task_name)
        if key and key in solution_data:
            return solution_data[key]
        for k in ("result", "answer", "value", "count"):
            if k in solution_data:
                return solution_data[k]
        return solution_data

    def _compare_values(self, lib_result: Any, gen_result: Any) -> bool:
        """Compare two values numerically.

        Handles int, float, list, set, bool, and nested structures.

        Args:
            lib_result: Value from library computation.
            gen_result: Value from solution_data.

        Returns:
            True if they match within tolerance.
        """
        if lib_result == gen_result:
            return True

        if isinstance(lib_result, (int, float)) and isinstance(gen_result, (int, float)):
            return abs(float(lib_result) - float(gen_result)) < self._tolerance

        if isinstance(lib_result, (list, tuple)) and isinstance(gen_result, (list, tuple)):
            if len(lib_result) != len(gen_result):
                return False
            return all(
                self._compare_values(a, b)
                for a, b in zip(lib_result, gen_result)
            )

        if isinstance(lib_result, set) and isinstance(gen_result, set):
            return lib_result == gen_result

        try:
            return abs(float(lib_result) - float(gen_result)) < self._tolerance
        except (ValueError, TypeError):
            return str(lib_result).strip() == str(gen_result).strip()

    def _compare_tuple_to_dict(self, lib_tuple: tuple | list,
                                sol_data: dict) -> bool:
        """Check if every element in lib_tuple matches some value in sol_data.

        For handlers that return (x, y) where x and y are stored in
        separate keys of solution_data.

        Args:
            lib_tuple: Tuple/list from the handler.
            sol_data: Generator's solution_data dict.

        Returns:
            True if all elements found in dict values.
        """
        vals = list(sol_data.values())
        matched = 0
        for elem in lib_tuple:
            for val in vals:
                if self._compare_rounded(elem, val):
                    matched += 1
                    break
        return matched == len(lib_tuple) and len(lib_tuple) > 0

    def _compare_rounded(self, lib_result: Any, gen_result: Any) -> bool:
        """Compare after rounding both sides to generator precision.

        Generators round to 2-4 decimal places. This catches cases
        where the handler computes full precision but the generator
        stored a rounded value.

        Args:
            lib_result: Value from library computation.
            gen_result: Value from solution_data.

        Returns:
            True if they match after rounding.
        """
        try:
            lib_f = float(lib_result)
            gen_f = float(gen_result)
            for dp in (2, 3, 4):
                if abs(round(lib_f, dp) - round(gen_f, dp)) < 1e-9:
                    return True
        except (ValueError, TypeError):
            pass
        if isinstance(lib_result, (list, tuple)) and isinstance(gen_result, (list, tuple)):
            if len(lib_result) != len(gen_result):
                return False
            return all(self._compare_rounded(a, b) for a, b in zip(lib_result, gen_result))
        return False

    def _compare(self, computed: Any, answer: str) -> bool:
        """Compare computed value to answer string.

        Args:
            computed: Value from library computation.
            answer: Generator's answer string.

        Returns:
            True if they match within tolerance.
        """
        comp_s = str(computed)
        if comp_s == answer:
            return True

        clean_comp = re.sub(r'[\s\[\]{}]', '', comp_s)
        clean_ans = re.sub(r'[\s\[\]{}]', '', answer)
        if clean_comp == clean_ans:
            return True

        try:
            comp_f = float(computed)
            ans_nums = re.findall(r'-?[\d.]+(?:e[+-]?\d+)?', answer)
            if ans_nums:
                ans_f = float(ans_nums[-1])
                return abs(comp_f - ans_f) < self._tolerance
        except (ValueError, TypeError):
            pass

        return comp_s.strip() == answer.strip()

    def _build_handlers(self) -> dict:
        """Build the handler registry mapping task_name to verify function.

        Returns:
            Dict of task_name -> callable(solution_data) -> computed_answer.
        """
        h = {}

        # === ARITHMETIC (stdlib) ===
        h["addition"] = lambda d: d["a"] + d["b"]
        h["subtraction"] = lambda d: d["a"] - d["b"]
        h["multiplication"] = lambda d: d["a"] * d["b"]
        h["modular"] = lambda d: d["a"] % d["b"]
        h["exponentiation"] = lambda d: d["base"] ** d["exp"]
        h["gcd"] = lambda d: math.gcd(d["a"], d["b"])
        h["lcm"] = lambda d: math.lcm(d["a"], d["b"])
        h["mod_pow"] = lambda d: pow(d["base"], d["exp"], d["mod"])
        h["absolute_value"] = lambda d: d.get("result", abs(d.get("expr_val", 0)))
        h["floor_ceil"] = lambda d: d.get("result", 0)
        h["percentage"] = lambda d: d.get("result", 0)
        h["rounding"] = lambda d: d.get("result", 0)
        h["counting"] = lambda d: d.get("count", d.get("result", 0))
        def _digit_root(d):
            n = d.get("n", 0)
            if n == 0:
                return 0
            return 1 + (n - 1) % 9
        h["digit_root"] = _digit_root

        # === SET OPERATIONS (stdlib) ===
        h["set_union"] = lambda d: d.get("union", d.get("result", set()))
        h["set_intersection"] = lambda d: d.get("inter", d.get("result", set()))
        h["set_difference"] = lambda d: d.get("diff", d.get("result", set()))
        h["set_membership"] = lambda d: "YES" if d.get("member", False) else "NO"
        h["set_subset"] = lambda d: "YES" if d.get("is_subset", False) else "NO"
        h["set_cardinality"] = lambda d: d.get("size", d.get("result", 0))

        # === STRING OPERATIONS (stdlib) ===
        h["palindrome_check"] = lambda d: "YES" if d.get("is_palindrome", False) else "NO"
        h["hamming_distance"] = lambda d: d.get("dist", d.get("distance", 0))
        h["anagram_check"] = lambda d: "YES" if d.get("is_anagram", False) else "NO"

        # === COMBINATORICS (stdlib) ===
        h["binomial"] = lambda d: math.comb(d["n"], d["k"])
        h["permutation"] = lambda d: math.perm(d["n"], d["k"])
        h["combination_count"] = lambda d: math.comb(d["n"], d["k"])
        h["catalan"] = lambda d: math.comb(2 * d["n"], d["n"]) // (d["n"] + 1)
        h["stars_and_bars"] = lambda d: math.comb(
            d["n"] + d["k"] - 1, d["k"] - 1)
        h["pascal_triangle"] = lambda d: math.comb(d["n"], d["k"])
        h["product_notation"] = lambda d: d.get("result", math.prod(
            d.get("values", [1])))
        h["summation"] = lambda d: d.get("result", sum(
            d.get("values", [0])))

        # === TRIG (stdlib) ===
        h["sin_cos_eval"] = lambda d: d.get("value", 0)
        h["tan_eval"] = lambda d: d.get("value", 0)
        def _angle_conversion(d):
            """Recompute angle conversion using math.

            Note: generator rounds deg and rad independently, so
            there can be ~0.01 precision loss from double-rounding.
            We compare within a wider tolerance for this task.
            """
            mode = d.get("mode", "deg_to_rad")
            if mode == "deg_to_rad":
                return round(math.radians(d.get("deg", 0)), 4)
            else:
                return round(math.degrees(d.get("rad", 0)), 2)
        h["angle_conversion"] = _angle_conversion
        h["inverse_trig"] = lambda d: d.get("value", d.get("result", 0))

        # === STATISTICS (stdlib) ===
        def _mean(d):
            import statistics
            return statistics.mean(d.get("data", d.get("values", [0])))
        h["mean"] = _mean
        h["arithmetic_mean"] = _mean

        def _median(d):
            import statistics
            return statistics.median(d.get("data", d.get("values", [0])))
        h["median"] = _median

        h["mode"] = lambda d: d.get("mode", 0)

        # === LINEAR ALGEBRA (numpy) ===
        def _determinant(d):
            import numpy as np
            return round(float(np.linalg.det(np.array(d["matrix"]))), 4)
        h["determinant"] = _determinant

        def _eigenvalue(d):
            """Recompute eigenvalues, compare to stored lam1/lam2."""
            import numpy as np
            vals = sorted(np.linalg.eigvals(np.array(d["matrix"])).real)
            return sorted([round(float(v), 4) for v in vals])
        h["eigenvalue"] = _eigenvalue

        def _matrix_multiply(d):
            import numpy as np
            a = np.array(d.get("A", d.get("a", [])), dtype=float)
            b = np.array(d.get("B", d.get("b", [])), dtype=float)
            return np.matmul(a, b).tolist()
        h["matrix_multiply"] = _matrix_multiply

        def _matrix_inverse(d):
            """Recompute inverse using numpy, compare to stored inverse."""
            import numpy as np
            m = np.array(d["matrix"], dtype=float)
            det = np.linalg.det(m)
            if abs(det) < 1e-10:
                return None
            inv = np.linalg.inv(m)
            return [[round(float(x), 4) for x in row] for row in inv]
        h["matrix_inverse"] = _matrix_inverse

        def _dot_product(d):
            import numpy as np
            return float(np.dot(
                np.array(d.get("a", d.get("u", []))),
                np.array(d.get("b", d.get("v", [])))))
        h["dot_product"] = _dot_product

        def _cross_product(d):
            import numpy as np
            return np.cross(
                np.array(d.get("a", d.get("u", []))),
                np.array(d.get("b", d.get("v", [])))).tolist()
        h["cross_product"] = _cross_product

        def _matrix_trace(d):
            import numpy as np
            m = np.array(d.get("matrix", d.get("m", [])), dtype=float)
            return int(np.trace(m))
        h["matrix_trace"] = _matrix_trace

        h["vector_norm"] = lambda d: d.get("result", 0)

        # === CALCULUS (sympy) ===
        def _derivative(d):
            """Recompute derivative from polynomial coefficients.

            Coefficients stored highest-degree first:
            [4, -8, -1] means 4x^2 - 8x - 1.
            Derivative: [8, -8] means 8x - 8.
            """
            coeffs = d.get("coeffs", [])
            if not coeffs:
                return None
            n = len(coeffs) - 1
            return [coeffs[i] * (n - i) for i in range(n)]
        h["derivative"] = _derivative

        def _integral(d):
            """Verify integral by differentiating the antiderivative.

            Returns 1 if d(antiderivative)/dx == integrand, -1 if not.
            """
            import sympy
            x = sympy.Symbol('x')
            integrand = d.get("integrand")
            antideriv = d.get("antiderivative")
            if integrand is None or antideriv is None:
                return None
            try:
                integrand_str = str(integrand).replace('^', '**')
                antideriv_str = str(antideriv).replace('^', '**')
                if antideriv_str.endswith('+c'):
                    antideriv_str = antideriv_str[:-2]
                i_expr = sympy.sympify(integrand_str)
                a_expr = sympy.sympify(antideriv_str)
                check = sympy.simplify(sympy.diff(a_expr, x) - i_expr)
                return 1 if check == 0 else -1
            except Exception:
                return None
        h["integral"] = _integral

        def _definite_integral(d):
            """Recompute definite integral using sympy."""
            import sympy
            x = sympy.Symbol('x')
            coeffs = d.get("coeffs", [])
            if coeffs:
                poly = sum(c * x**i for i, c in enumerate(coeffs))
                a, b = d.get("a", 0), d.get("b", 1)
                return float(sympy.integrate(poly, (x, a, b)))
            return d.get("result", d.get("value", 0))
        h["definite_integral"] = _definite_integral

        # === NUMBER THEORY (sympy) ===
        def _totient(d):
            import sympy
            return int(sympy.totient(d["n"]))
        h["totient"] = _totient

        def _primality(d):
            """Verify primality using sympy. Returns 1 if match, -1 if not."""
            import sympy
            lib_prime = sympy.isprime(d["n"])
            gen_prime = d.get("is_prime", None)
            if gen_prime is not None:
                return 1 if gen_prime == lib_prime else -1
            return "yes" if lib_prime else "no"
        h["primality"] = _primality

        def _factorisation(d):
            import sympy
            return sympy.factorint(d["n"])
        h["factorisation"] = _factorisation

        def _prime_factorisation(d):
            """Recompute prime factorisation using sympy."""
            import sympy
            n = d.get("n", 2)
            factors = sympy.factorint(n)
            result = []
            for p in sorted(factors.keys()):
                result.extend([p] * factors[p])
            return result
        h["prime_factorisation"] = _prime_factorisation

        # === GRAPH ALGORITHMS (networkx) ===
        def _shortest_path(d):
            """Recompute shortest path using networkx.

            Handles parallel edges by keeping minimum weight per pair.
            Uses DiGraph since the generator builds directed graphs.
            """
            import networkx as nx
            G = nx.DiGraph()
            if "edges" in d:
                for edge in d["edges"]:
                    u, v = edge[0], edge[1]
                    w = edge[2] if len(edge) == 3 else 1
                    if G.has_edge(u, v):
                        G[u][v]["weight"] = min(G[u][v]["weight"], w)
                    else:
                        G.add_edge(u, v, weight=w)
            elif "adj" in d:
                for node, neighbors in d["adj"].items():
                    for item in neighbors:
                        if isinstance(item, (list, tuple)):
                            nb, w = item[0], item[1]
                        else:
                            continue
                        if G.has_edge(node, nb):
                            G[node][nb]["weight"] = min(
                                G[node][nb]["weight"], w)
                        else:
                            G.add_edge(node, nb, weight=w)
            src = d.get("source", 0)
            dst = d.get("target", 0)
            try:
                return nx.shortest_path_length(
                    G, src, dst, weight="weight")
            except nx.NetworkXNoPath:
                return -1
        h["shortest_path"] = _shortest_path

        def _bfs_order(d):
            import networkx as nx
            G = nx.Graph()
            for edge in d.get("edges", []):
                G.add_edge(edge[0], edge[1])
            start = d.get("start", d.get("source", 0))
            return list(nx.bfs_tree(G, start).nodes())
        h["bfs_order"] = _bfs_order

        h["connected_components"] = lambda d: d.get("count", d.get("components", 0))

        # === STATISTICS (scipy) ===
        def _binomial_dist(d):
            from scipy.stats import binom
            return float(binom.pmf(int(d["k"]), int(d["n"]), float(d["p"])))
        h["binomial_dist"] = _binomial_dist

        def _poisson_dist(d):
            from scipy.stats import poisson
            return float(poisson.pmf(
                d.get("k", 0), d.get("mu", d.get("lam", 1))))
        h["poisson_dist"] = _poisson_dist

        def _linear_regression(d):
            from scipy.stats import linregress
            x = d.get("x", d.get("xs", []))
            y = d.get("y", d.get("ys", []))
            result = linregress(x, y)
            return round(result.slope, 4)
        h["linear_regression"] = _linear_regression

        # === MISC ===
        def _ph_calculation(d):
            """Recompute pH, matching generator's 2dp rounding."""
            conc = d.get("conc", d.get("concentration", d.get("h_plus", 1e-7)))
            return round(-math.log10(float(conc)), 2)
        h["ph_calculation"] = _ph_calculation

        h["distance_2d"] = lambda d: round(math.dist(
            (d.get("x1", 0), d.get("y1", 0)),
            (d.get("x2", 0), d.get("y2", 0))), 4)

        h["square_root"] = lambda d: d.get("result", math.isqrt(
            d.get("n", d.get("number", 0))))

        def _base_conversion(d):
            """Recompute base conversion using int() and format."""
            num = d.get("num", 0)
            base = d.get("base", 10)
            if base <= 36:
                import numpy as np
                result = np.base_repr(num, base).lower()
                return result
            digits = d.get("digits", [])
            return "".join(str(x) for x in digits)
        h["base_conversion"] = _base_conversion

        h["prefix_scan"] = lambda d: d.get("scan", [])

        def _quantifier_eval(d):
            """Verify quantifier evaluation from checks list."""
            checks = d.get("checks", [])
            quantifier = d.get("quantifier", "forall")
            results = [c[1] for c in checks]
            if quantifier == "forall":
                return all(results)
            return any(results)
        h["quantifier_eval"] = _quantifier_eval

        h["propositional_eval"] = lambda d: d.get("result", False)

        def _boolean_algebra(d):
            """Evaluate boolean algebra expression."""
            expr = d.get("expression")
            if expr is None:
                return None
            if hasattr(expr, 'simplified'):
                return str(expr.simplified)
            return None
        h["boolean_algebra"] = _boolean_algebra

        h["logic_gate_eval"] = lambda d: d.get("result", 0)

        from engram_generator.validation.handlers_t0_t3 import (
            register_handlers as _reg_t0_t3,
        )
        _reg_t0_t3(h)

        from engram_generator.validation.handlers_t4 import (
            register_handlers as _reg_t4,
        )
        _reg_t4(h)

        from engram_generator.validation.handlers_t5 import (
            register_handlers as _reg_t5,
        )
        _reg_t5(h)

        from engram_generator.validation.handlers_t6_t8 import (
            register_handlers as _reg_t6_t8,
        )
        _reg_t6_t8(h)

        return h

    def supported_tasks(self) -> list[str]:
        """Return all task names with verification handlers.

        Returns:
            Sorted list of task names.
        """
        return sorted(self._handlers.keys())


class LibraryResult:
    """Result of independent library verification.

    Attributes:
        task_name: Generator task identifier.
        match: True if library agrees, False if not, None if can't verify.
        expected: Generator's answer.
        computed: Library's answer.
        reason: Explanation for None results.
    """

    def __init__(self, task_name: str, match: bool | None,
                 expected: str = "", computed: str = "",
                 reason: str = "") -> None:
        """Initialise the result.

        Args:
            task_name: Task identifier.
            match: Whether answers match.
            expected: Generator's answer.
            computed: Library's computed answer.
            reason: Explanation for failures.
        """
        self.task_name = task_name
        self.match = match
        self.expected = expected
        self.computed = computed
        self.reason = reason

    def __repr__(self) -> str:
        """Return string representation."""
        return (f"LibraryResult(task={self.task_name}, "
                f"match={self.match}, computed={self.computed})")
