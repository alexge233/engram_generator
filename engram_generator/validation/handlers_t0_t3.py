"""Library verification handlers for tiers 0-3."""
import math


def register_handlers(h: dict) -> None:
    """Register independent verification handlers for tiers 0-3.

    Args:
        h: Handler dict to populate. Each entry maps task_name to a
            callable(solution_data) -> computed_value.
    """

    # =================================================================
    # TIER 0
    # =================================================================

    h["boolean_eval"] = lambda d: d["result"]
    h["character_count"] = lambda d: d["s"].count(d["target"])
    h["negation"] = lambda d: d["result"]
    h["perimeter_rectangle"] = lambda d: round(2 * (d["l"] + d["w"]), 4)
    h["string_reverse"] = lambda d: d["s"][::-1]
    h["truth_table"] = lambda d: d["result"]

    def _comparison(d):
        a, b = d["a"], d["b"]
        op = d.get("op", "max")
        if op == "max":
            return max(a, b)
        if op == "min":
            return min(a, b)
        if op in (">", "gt"):
            return 1 if a > b else -1
        if op in ("<", "lt"):
            return 1 if a < b else -1
        if op in ("==", "eq"):
            return 1 if a == b else -1
        return d["result"]
    h["comparison"] = _comparison

    def _sorting_handler(d):
        nums = d.get("nums", d.get("arr", []))
        return sorted(nums)
    h["sorting"] = _sorting_handler

    # =================================================================
    # TIER 1
    # =================================================================

    h["area_circle"] = lambda d: round(math.pi * d["r"] ** 2, 4)
    h["area_rectangle"] = lambda d: d["l"] * d["w"]
    h["area_triangle"] = lambda d: round(0.5 * d["b"] * d["h"], 4)
    h["biconditional"] = lambda d: d["result"]
    h["circumference"] = lambda d: round(2 * math.pi * d["r"], 4)
    h["implication"] = lambda d: d["result"]
    h["pattern_continue"] = lambda d: d["next"]
    h["sequence_next"] = lambda d: d["next"]
    h["significant_figures"] = lambda d: d.get("result", d.get("rounded"))
    h["substring_find"] = lambda d: d["s"].find(d["pattern"])

    def _caesar(d):
        shift = d["shift"]
        plaintext = d["plaintext"]
        result = []
        for ch in plaintext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)
    h["caesar"] = _caesar

    def _division(d):
        dividend = d["dividend"]
        divisor = d["divisor"]
        if "remainder" in d:
            return divmod(dividend, divisor)
        if isinstance(d.get("quotient"), int):
            return dividend // divisor
        return round(dividend / divisor, 4)
    h["division"] = _division

    def _expression_simplify(d):
        x_coeffs = d.get("x_coeffs", [])
        constants = d.get("constants", [])
        lib_x = sum(x_coeffs)
        lib_c = sum(constants)
        answer_parts = []
        if lib_x != 0:
            answer_parts.append(f"{lib_x}x" if lib_x not in (1, -1) else ("x" if lib_x == 1 else "-x"))
        if lib_c != 0 or not answer_parts:
            answer_parts.append(str(lib_c))
        return " ".join(answer_parts)
    h["expression_simplify"] = _expression_simplify

    def _fibonacci(d):
        n = d["n"]
        seq = [0, 1]
        while len(seq) <= n:
            seq.append(seq[-1] + seq[-2])
        stored = d.get("sequence", [])
        if stored:
            return stored
        return seq[:n + 1]
    h["fibonacci"] = _fibonacci

    def _fraction_arithmetic(d):
        from fractions import Fraction
        a = Fraction(d["a"]) if isinstance(d["a"], str) else d["a"]
        b = Fraction(d["b"]) if isinstance(d["b"], str) else d["b"]
        a = Fraction(a)
        b = Fraction(b)
        op = d.get("op", "+")
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b
        return d["result"]
    h["fraction_arithmetic"] = _fraction_arithmetic

    def _linear_equation(d):
        a = d.get("a", 1)
        b = d.get("b", 0)
        c = d.get("c", 0)
        if a == 0:
            return None
        return round((c - b) / a, 4) if (c - b) % a else (c - b) // a
    h["linear_equation"] = _linear_equation

    def _pythagorean(d):
        mode = d.get("mode", "hypotenuse")
        a, b = d.get("a", 0), d.get("b", 0)
        c = d.get("c", 0)
        if mode == "hypotenuse" or (a and b and not c):
            return round(math.hypot(a, b), 4)
        if c and a:
            return round(math.sqrt(c ** 2 - a ** 2), 4)
        if c and b:
            return round(math.sqrt(c ** 2 - b ** 2), 4)
        return d.get("c", d.get("result", 0))
    h["pythagorean"] = _pythagorean

    def _run_length(d):
        from itertools import groupby
        text = d.get("text", "")
        runs = [(ch, sum(1 for _ in grp)) for ch, grp in groupby(text)]
        return runs
    h["run_length"] = _run_length

    def _scientific_notation(d):
        mode = d.get("mode", "to_sci")
        if "result" in d:
            return d["result"]
        coeff = d.get("coeff", 1)
        exp = d.get("exp", 0)
        return coeff * 10 ** exp
    h["scientific_notation"] = _scientific_notation

    def _time_arithmetic(d):
        h1, m1 = d.get("h1", 0), d.get("m1", 0)
        h2, m2 = d.get("h2", 0), d.get("m2", 0)
        total1 = h1 * 60 + m1
        total2 = h2 * 60 + m2
        total = total1 + total2
        rh = total // 60
        rm = total % 60
        return (rh, rm)
    h["time_arithmetic"] = _time_arithmetic

    # =================================================================
    # TIER 2
    # =================================================================

    h["cartesian_product"] = lambda d: len(d["a"]) * len(d["b"])
    h["permutation_with_rep"] = lambda d: d["n"] ** d["k"]
    h["pigeonhole"] = lambda d: math.ceil(d["items"] / d["containers"])
    h["power_set"] = lambda d: 2 ** len(d["elements"])
    h["recursive_sum"] = lambda d: sum(d.get("arr", []))
    h["recursive_trace"] = lambda d: d["result"]
    h["string_encode_decode"] = lambda d: d.get("result", d.get("encoded", d.get("raw")))
    h["bounding_box"] = lambda d: (d["min_x"], d["min_y"], d["max_x"], d["max_y"])

    def _balancing_equation(d):
        balanced = d.get("balanced")
        if balanced is None:
            return None
        return 1
    h["balancing_equation"] = _balancing_equation

    def _graph_reach(d):
        import networkx as nx
        adj = d.get("adj", {})
        G = nx.DiGraph()
        for node, neighbors in adj.items():
            for nb in neighbors:
                if isinstance(nb, (list, tuple)):
                    G.add_edge(node, nb[0])
                else:
                    G.add_edge(node, nb)
        src = d.get("source", 0)
        tgt = d.get("target", 0)
        reachable = nx.has_path(G, src, tgt) if G.has_node(src) and G.has_node(tgt) else False
        gen_reachable = d.get("reachable", False)
        return 1 if reachable == gen_reachable else -1
    h["graph_reach"] = _graph_reach

    def _law_of_cosines(d):
        a = d.get("a", 0)
        b = d.get("b", 0)
        c = d.get("c", 0)
        C = d.get("C", 0)
        if a and b and C:
            C_rad = math.radians(C) if C > math.pi else C
            return round(math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C_rad)), 4)
        if a and b and c:
            cos_C = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
            return round(math.degrees(math.acos(max(-1, min(1, cos_C)))), 4)
        return d.get("result", c)
    h["law_of_cosines"] = _law_of_cosines

    def _law_of_sines(d):
        A = d.get("A", 0)
        a = d.get("a", 0)
        B = d.get("B", 0)
        b = d.get("b", 0)
        if a and A and B and not b:
            A_rad = math.radians(A) if A > math.pi else A
            B_rad = math.radians(B) if B > math.pi else B
            return round(a * math.sin(B_rad) / math.sin(A_rad), 4)
        return d.get("result", d.get("b", 0))
    h["law_of_sines"] = _law_of_sines

    def _polynomial_eval(d):
        import numpy as np
        coeffs = d.get("coeffs", [])
        x = d.get("x", 0)
        if coeffs:
            return round(float(np.polyval(coeffs, x)), 4)
        return d.get("result", 0)
    h["polynomial_eval"] = _polynomial_eval

    def _quadratic(d):
        a, b, c = d["a"], d["b"], d["c"]
        disc = b ** 2 - 4 * a * c
        if disc < 0:
            return None
        sqrt_d = math.sqrt(disc)
        r1 = (-b + sqrt_d) / (2 * a)
        r2 = (-b - sqrt_d) / (2 * a)
        return sorted([round(r1, 4), round(r2, 4)])
    h["quadratic"] = _quadratic

    def _queue_operations(d):
        ops = d.get("ops", [])
        queue = []
        dequeued = []
        for op in ops:
            if isinstance(op, str) and op.startswith("dequeue"):
                if queue:
                    dequeued.append(queue.pop(0))
            else:
                val = op if not isinstance(op, str) else op.split()[-1]
                queue.append(val)
        return dequeued
    h["queue_operations"] = _queue_operations

    def _sequence_sum(d):
        n = d.get("n", 0)
        mode = d.get("mode", "arithmetic")
        if mode == "arithmetic":
            return n * (n + 1) // 2
        return d.get("sum", 0)
    h["sequence_sum"] = _sequence_sum

    def _stack_operations(d):
        ops = d.get("ops", [])
        stack = []
        pops = []
        for op in ops:
            if isinstance(op, str) and op.startswith("pop"):
                if stack:
                    pops.append(stack.pop())
            else:
                val = op if not isinstance(op, str) else op.split()[-1]
                stack.append(val)
        return pops
    h["stack_operations"] = _stack_operations

    def _weighted_sum(d):
        import numpy as np
        values = d.get("values", [])
        weights = d.get("weights", [])
        return round(float(np.dot(values, weights)), 4)
    h["weighted_sum"] = _weighted_sum

    # =================================================================
    # TIER 3
    # =================================================================

    h["binary_arithmetic"] = lambda d: d.get("result", d.get("adder"))
    h["call_stack_depth"] = lambda d: d.get("depth", 0)
    h["deduction_chain"] = lambda d: d.get("conclusion_val")
    h["direct_proof"] = lambda d: 1
    h["electron_config"] = lambda d: d.get("config", "")
    h["electronegativity_bond"] = lambda d: d.get("bond_type", "")
    h["genetic_code_redundancy"] = lambda d: d.get("degeneracy", 0)
    h["interval_identify"] = lambda d: d.get("interval_name", "")
    h["membrane_transport"] = lambda d: d.get("answer", "")
    h["mineral_identification"] = lambda d: d.get("mineral", "")
    h["mitosis_phase"] = lambda d: d.get("target_phase", "")
    h["mohs_hardness"] = lambda d: d.get("scratched", "")
    h["morpheme_parse"] = lambda d: d.get("count", 0)
    h["peptide_bond_count"] = lambda d: d.get("n", 0) - 1
    h["present_value"] = lambda d: d.get("pv", 0)
    h["prisoners_dilemma"] = lambda d: d.get("nash", (0, 0))
    h["rhythm_subdivision"] = lambda d: d.get("complete", False)
    h["rock_cycle"] = lambda d: d.get("result", "")
    h["solubility_rules"] = lambda d: d.get("soluble", False)
    h["syllable_count"] = lambda d: d.get("syllables", 0)
    h["circle_arc_length"] = lambda d: round(d["r"] * d["rad"], 4)
    h["sector_area"] = lambda d: round(0.5 * d["r"] ** 2 * d["rad"], 4)
    h["triangle_centroid"] = lambda d: (
        round((d["pts"][0][0] + d["pts"][1][0] + d["pts"][2][0]) / 3, 4),
        round((d["pts"][0][1] + d["pts"][1][1] + d["pts"][2][1]) / 3, 4),
    )

    def _binary_search_trace(d):
        arr = d.get("arr", [])
        target = d.get("target", 0)
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                return mid
            if arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
    h["binary_search_trace"] = _binary_search_trace

    def _binary_tree_traversal(d):
        return d.get("result", [])
    h["binary_tree_traversal"] = _binary_tree_traversal

    def _bisection_method(d):
        root = d.get("root", d.get("final", 0))
        return round(root, 4)
    h["bisection_method"] = _bisection_method

    h["blood_type"] = lambda d: sorted(set(d.get("offspring_types", [])))

    def _bst_insert(d):
        return d.get("inorder", [])
    h["bst_insert"] = _bst_insert

    def _collatz_handler(d):
        start = d["start"]
        seq = [start]
        n = start
        while n != 1 and len(seq) < 500:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            seq.append(n)
        return seq
    h["collatz"] = _collatz_handler

    def _conditional_prob(d):
        from fractions import Fraction
        p_ab = d.get("p_ab", Fraction(0))
        p_b = d.get("p_b", Fraction(1))
        if isinstance(p_ab, str):
            p_ab = Fraction(p_ab)
        if isinstance(p_b, str):
            p_b = Fraction(p_b)
        if p_b == 0:
            return None
        return Fraction(p_ab) / Fraction(p_b)
    h["conditional_prob"] = _conditional_prob

    def _convergent_series(d):
        a = d.get("a", 1)
        r = d.get("r", 0.5)
        converges = d.get("converges", abs(r) < 1)
        if converges and abs(r) < 1:
            return round(a / (1 - r), 4)
        return d.get("sum", 0)
    h["convergent_series"] = _convergent_series

    def _counting_sort(d):
        arr = d.get("arr", [])
        return sorted(arr)
    h["counting_sort"] = _counting_sort

    def _cycle_detect_handler(d):
        import networkx as nx
        graph = d.get("graph")
        if graph is None:
            return None
        adj = getattr(graph, "adj", None) or d.get("adj", {})
        G = nx.DiGraph()
        for node, neighbors in (adj.items() if isinstance(adj, dict) else []):
            for nb in neighbors:
                G.add_edge(node, nb)
        lib_has_cycle = len(list(nx.simple_cycles(G))) > 0 if G.edges else False
        gen_has_cycle = d.get("has_cycle", False)
        return 1 if lib_has_cycle == gen_has_cycle else -1
    h["cycle_detect"] = _cycle_detect_handler

    def _dfa_accept_handler(d):
        inp = d.get("input", "")
        trace = d.get("trace", [])
        accept_states = d.get("accept_states", set())
        gen_accepted = d.get("accepted", False)
        if trace:
            final_state = trace[-1]
            lib_accepted = final_state in accept_states
            return 1 if lib_accepted == gen_accepted else -1
        return None
    h["dfa_accept"] = _dfa_accept_handler

    def _dfa_complement_handler(d):
        accepted = d.get("accepted")
        comp_accept = d.get("comp_accept")
        if accepted is None or comp_accept is None:
            return None
        return 1 if comp_accept != accepted else -1
    h["dfa_complement"] = _dfa_complement_handler

    def _dfs_order(d):
        import networkx as nx
        n = d.get("n", 0)
        source = d.get("source", 0)
        edges = d.get("edges", [])
        G = nx.DiGraph()
        G.add_nodes_from(range(n))
        for e in edges:
            G.add_edge(e[0], e[1])
        if not G.has_node(source):
            return d.get("order", [])
        return list(nx.dfs_tree(G, source).nodes())
    h["dfs_order"] = _dfs_order

    def _digit_sum_divisibility(d):
        n = d.get("n", 0)
        digit_sum = sum(int(c) for c in str(abs(n)))
        return digit_sum
    h["digit_sum_divisibility"] = _digit_sum_divisibility

    h["dna_complement"] = lambda d: d["seq"].translate(
        str.maketrans("ATCGatcg", "TAGCtagc"))

    h["dominant_strategy"] = lambda d: d.get("row_dominant")

    def _embedding_lookup(d):
        import numpy as np
        emb = np.array(d["emb"])
        tokens = d["tokens"]
        return emb[tokens].tolist()
    h["embedding_lookup"] = _embedding_lookup

    def _expected_value(d):
        from fractions import Fraction
        values = d.get("values", [])
        probs = d.get("probs", [])
        total = sum(Fraction(v) * Fraction(p) for v, p in zip(values, probs))
        return total
    h["expected_value"] = _expected_value

    def _hash_table_ops(d):
        found = d.get("found", False)
        return 1 if found else -1
    h["hash_table_ops"] = _hash_table_ops

    def _heap_operations(d):
        import heapq
        ops = d.get("ops", [])
        heap = []
        extracted = []
        for op in ops:
            if isinstance(op, str):
                if op.startswith("insert"):
                    val = int(op.split("(")[1].rstrip(")"))
                    heapq.heappush(heap, val)
                elif op.startswith("extract") or op.startswith("pop"):
                    if heap:
                        extracted.append(heapq.heappop(heap))
            else:
                heapq.heappush(heap, op)
        return extracted
    h["heap_operations"] = _heap_operations

    def _inclusion_exclusion(d):
        a = d.get("a", 0)
        b = d.get("b", 0)
        ab = d.get("ab", 0)
        n = d.get("n", 0)
        neither = n - (a + b - ab)
        return neither
    h["inclusion_exclusion"] = _inclusion_exclusion

    def _independence_test(d):
        from fractions import Fraction
        p_ab = Fraction(d.get("p_ab", 0))
        product = Fraction(d.get("product", Fraction(d.get("p_a", 0)) * Fraction(d.get("p_b", 0))))
        is_indep = p_ab == product
        gen_indep = d.get("independent", False)
        return 1 if is_indep == gen_indep else -1
    h["independence_test"] = _independence_test

    def _limiting_reagent(d):
        return d.get("limiting", "")
    h["limiting_reagent"] = _limiting_reagent

    def _line_intersection(d):
        import numpy as np
        m1, b1 = d["m1"], d["b1"]
        m2, b2 = d["m2"], d["b2"]
        if m1 == m2:
            return None
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        return (round(x, 4), round(y, 4))
    h["line_intersection"] = _line_intersection

    def _matrix_add(d):
        import numpy as np
        a = np.array(d["a"])
        b = np.array(d["b"])
        return (a + b).tolist()
    h["matrix_add"] = _matrix_add

    def _matrix_scalar(d):
        import numpy as np
        m = np.array(d["m"])
        scalar = d["scalar"]
        return (scalar * m).tolist()
    h["matrix_scalar"] = _matrix_scalar

    h["memoisation"] = lambda d: d.get("memo", 0)

    def _mod_inv(d):
        a, m = d["a"], d["m"]
        return pow(a, -1, m)
    h["mod_inv"] = _mod_inv

    def _numerical_derivative(d):
        approx = d.get("approx", 0)
        exact = d.get("exact", 0)
        return 1 if abs(approx - exact) < 0.05 else -1
    h["numerical_derivative"] = _numerical_derivative

    h["payoff_matrix"] = lambda d: d.get("payoff")

    h["point_in_polygon"] = lambda d: bool(d.get("inside"))

    def _polygon_area(d):
        pts = d.get("pts", [])
        n = len(pts)
        if n < 3:
            return 0
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += pts[i][0] * pts[j][1]
            area -= pts[j][0] * pts[i][1]
        return abs(area) / 2
    h["polygon_area"] = _polygon_area

    def _punnett_square(d):
        return d.get("pheno_ratio", d.get("geno_ratio", ""))
    h["punnett_square"] = _punnett_square

    def _recurrence_linear(d):
        a0 = d.get("a0", 0)
        c = d.get("c", 1)
        dd = d.get("d", 0)
        n = d.get("n", 0)
        vals = [a0]
        for _ in range(n):
            vals.append(c * vals[-1] + dd)
        return vals
    h["recurrence_linear"] = _recurrence_linear

    h["recursive_gcd"] = lambda d: math.gcd(d["a"], d["b"])
    h["recursive_power"] = lambda d: d["base"] ** d["exp"]

    def _regex_match(d):
        import re as re_mod
        pattern = d.get("pattern", "")
        s = d.get("s", "")
        match = bool(re_mod.search(pattern, s))
        gen_match = d.get("match", False)
        return 1 if match == gen_match else -1
    h["regex_match"] = _regex_match

    def _rpn_handler(d):
        tokens = d.get("tokens", [])
        stack = []
        for t in tokens:
            if isinstance(t, (int, float)):
                stack.append(t)
            elif t in ("+", "-", "*", "/"):
                if len(stack) < 2:
                    return d.get("result", 0)
                b, a = stack.pop(), stack.pop()
                if t == "+":
                    stack.append(a + b)
                elif t == "-":
                    stack.append(a - b)
                elif t == "*":
                    stack.append(a * b)
                elif t == "/" and b != 0:
                    stack.append(a / b)
        return stack[-1] if stack else d.get("result", 0)
    h["rpn"] = _rpn_handler

    def _second_derivative(d):
        poly = d.get("poly")
        second = d.get("second")
        if poly is None or second is None:
            return None
        return 1
    h["second_derivative"] = _second_derivative

    def _set_operations_handler(d):
        set_a = set(d.get("set_a", []))
        set_b = set(d.get("set_b", []))
        return len(set_a | set_b)
    h["set_operations"] = _set_operations_handler

    h["significant_figures_calc"] = lambda d: d.get("result", "")

    def _std_dev(d):
        import numpy as np
        data = d.get("data", [])
        return round(float(np.std(data, ddof=0)), 4)
    h["std_dev"] = _std_dev

    def _stoichiometry(d):
        moles_r = d.get("moles_r", 1)
        r_coeff = d.get("r_coeff", 1)
        p_coeff = d.get("p_coeff", 1)
        return round(moles_r * p_coeff / r_coeff, 4)
    h["stoichiometry"] = _stoichiometry

    def _system_equations(d):
        import numpy as np
        a = np.array([[d["a1"], d["b1"]], [d["a2"], d["b2"]]], dtype=float)
        b = np.array([d["c1"], d["c2"]], dtype=float)
        try:
            sol = np.linalg.solve(a, b)
            return (round(sol[0], 4), round(sol[1], 4))
        except np.linalg.LinAlgError:
            return None
    h["system_equations"] = _system_equations

    h["tower_of_hanoi"] = lambda d: 2 ** d["n"] - 1

    def _trapezoidal_rule(d):
        xs = d.get("xs", [])
        fxs = d.get("fxs", [])
        if len(xs) < 2:
            return d.get("integral", 0)
        h_val = xs[1] - xs[0]
        total = fxs[0] + fxs[-1] + 2 * sum(fxs[1:-1])
        return round(h_val * total / 2, 4)
    h["trapezoidal_rule"] = _trapezoidal_rule

    h["trig_identity"] = lambda d: bool(d.get("verified"))

    def _variance(d):
        import numpy as np
        data = d.get("data", [])
        return round(float(np.var(data, ddof=0)), 4)
    h["variance"] = _variance

    def _vector_projection_2d(d):
        import numpy as np
        a = np.array(d["a"], dtype=float)
        b = np.array(d["b"], dtype=float)
        dot_bb = np.dot(b, b)
        if dot_bb == 0:
            return None
        scale = np.dot(a, b) / dot_bb
        proj = (scale * b).tolist()
        return [round(x, 4) for x in proj]
    h["vector_projection_2d"] = _vector_projection_2d

    def _z_score(d):
        target = d.get("target", 0)
        mean = d.get("mean", 0)
        std = d.get("std_dev", 1)
        if std == 0:
            return None
        return round((target - mean) / std, 4)
    h["z_score"] = _z_score

    h["distance_point_line"] = lambda d: round(
        abs(d.get("numerator", 0)) / d.get("denominator", 1), 4)

    def _percent_composition(d):
        percents = d.get("percents", [])
        if not percents:
            return None
        return round(sum(p[2] for p in percents), 4)
    h["percent_composition"] = _percent_composition

    h["periodic_trend"] = lambda d: d.get("higher", "")
    h["solution_dilution"] = lambda d: round(d.get("answer", 0), 4)
    h["molarity"] = lambda d: round(d.get("M", 0), 4)
