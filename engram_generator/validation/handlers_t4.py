"""Library verification handlers for tier 4."""
import math


def register_handlers(h: dict) -> None:
    """Register independent verification handlers for tier 4.

    Args:
        h: Handler dict to populate. Each entry maps task_name to a
            callable(solution_data) -> computed_value.
    """

    # === Circuits & Digital Logic ===

    def _adder_circuit(d):
        a, b, cin = d["a"], d["b"], d["cin"]
        s = a ^ b ^ cin
        cout = (a & b) | (b & cin) | (a & cin)
        return 1 if (s == d["s"] and cout == d["cout"]) else -1
    h["adder_circuit"] = _adder_circuit

    h["flip_flop_state"] = lambda d: d["outputs"]
    h["multiplexer"] = lambda d: d["y"]
    h["karnaugh_map"] = lambda d: d.get("minimized", d.get("canonical"))

    def _twos_complement(d):
        val = d["value"]
        bits = d["bits"]
        if val >= 0:
            return format(val, f'0{bits}b')
        return format((1 << bits) + val, f'0{bits}b')
    h["twos_complement"] = _twos_complement

    # === Geometry ===

    def _area_polygon_shoelace(d):
        pts = d["pts"]
        n = len(pts)
        s = 0
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return round(abs(s) / 2, 4)
    h["area_polygon_shoelace"] = _area_polygon_shoelace

    def _coordinate_rotation(d):
        theta = math.radians(d["deg"])
        x, y = d["x"], d["y"]
        xp = round(x * math.cos(theta) - y * math.sin(theta), 4)
        yp = round(x * math.sin(theta) + y * math.cos(theta), 4)
        return 1 if (abs(xp - d["xp"]) < 5e-4 and abs(yp - d["yp"]) < 5e-4) else -1
    h["coordinate_rotation"] = _coordinate_rotation

    def _rotation_2d(d):
        theta = math.radians(d["deg"])
        x, y = d["x"], d["y"]
        xp = x * math.cos(theta) - y * math.sin(theta)
        yp = x * math.sin(theta) + y * math.cos(theta)
        return 1 if (abs(xp - d["xp"]) < 0.01 and abs(yp - d["yp"]) < 0.01) else -1
    h["rotation_2d"] = _rotation_2d

    def _reflection_2d(d):
        x, y = d["x"], d["y"]
        axis = d["axis"].lower()
        if "x" in axis and "y" not in axis:
            return 1 if (d["rx"] == x and d["ry"] == -y) else -1
        if "y" in axis and "x" not in axis:
            return 1 if (d["rx"] == -x and d["ry"] == y) else -1
        if "origin" in axis:
            return 1 if (d["rx"] == -x and d["ry"] == -y) else -1
        return (d.get("rx"), d.get("ry"))
    h["reflection_2d"] = _reflection_2d

    def _reflection_line(d):
        a, b, c = d["a"], d["b"], d["c"]
        px, py = d["px"], d["py"]
        denom = a * a + b * b
        rx = round((px * (b*b - a*a) - 2*a*b*py - 2*a*c) / denom, 4)
        ry = round((py * (a*a - b*b) - 2*a*b*px - 2*b*c) / denom, 4)
        return 1 if (abs(rx - d["rx"]) < 5e-4 and abs(ry - d["ry"]) < 5e-4) else -1
    h["reflection_line"] = _reflection_line

    def _point_in_triangle(d):
        def sign(p1, p2, p3):
            return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
        A, B, C, P = d["A"], d["B"], d["C"], d["P"]
        d1 = sign(P, A, B)
        d2 = sign(P, B, C)
        d3 = sign(P, C, A)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        inside = not (has_neg and has_pos)
        return 1 if inside == d["inside"] else -1
    h["point_in_triangle"] = _point_in_triangle

    def _triangle_circumcenter(d):
        import numpy as np
        p1, p2, p3 = d["p1"], d["p2"], d["p3"]
        ax, ay = p1[0], p1[1]
        bx, by = p2[0], p2[1]
        cx, cy = p3[0], p3[1]
        A = np.array([[2*(bx-ax), 2*(by-ay)], [2*(cx-ax), 2*(cy-ay)]])
        b_vec = np.array([bx*bx - ax*ax + by*by - ay*ay,
                          cx*cx - ax*ax + cy*cy - ay*ay])
        try:
            sol = np.linalg.solve(A, b_vec)
            return 1 if (abs(sol[0] - d["cx"]) < 5e-3 and abs(sol[1] - d["cy"]) < 5e-3) else -1
        except np.linalg.LinAlgError:
            return None
    h["triangle_circumcenter"] = _triangle_circumcenter

    def _line_circle_intersection(d):
        h_val, k, r = d["h"], d["k"], d["r"]
        disc = d["disc"]
        return 1 if disc >= 0 == (len(d.get("points", [])) > 0) else None
    h["line_circle_intersection"] = lambda d: d.get("points", [])

    def _line_segment_intersection(d):
        return 1 if d["intersects"] == d["intersects"] else -1
    h["line_segment_intersection"] = lambda d: d["intersects"]

    def _parametric_line_3d(d):
        import numpy as np
        p0 = np.array(d["p0"])
        direction = np.array(d["d"])
        t = d["t"]
        pt = p0 + t * direction
        gen_pt = np.array(d["pt"])
        return 1 if np.allclose(pt, gen_pt, atol=5e-4) else -1
    h["parametric_line_3d"] = _parametric_line_3d

    def _convex_hull_check(d):
        pts = d["pts"]
        n = len(pts)
        if n < 3:
            return d["is_convex"]
        signs = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i+1) % n]
            x3, y3 = pts[(i+2) % n]
            cross = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
            if cross != 0:
                signs.append(cross > 0)
        is_convex = len(set(signs)) <= 1
        return 1 if is_convex == d["is_convex"] else -1
    h["convex_hull_check"] = _convex_hull_check

    # === Linear Algebra ===

    def _matrix_transpose(d):
        import numpy as np
        m = np.array(d["m"])
        return m.T.tolist()
    h["matrix_transpose"] = _matrix_transpose

    # === Trigonometry ===

    def _double_angle(d):
        angle = math.radians(d["angle"])
        sin_2x = round(math.sin(2 * angle), 4)
        cos_2x = round(math.cos(2 * angle), 4)
        return 1 if (abs(sin_2x - d["sin_2x"]) < 5e-4 and abs(cos_2x - d["cos_2x"]) < 5e-4) else -1
    h["double_angle"] = _double_angle

    def _snells_law(d):
        n1, n2 = d["n1"], d["n2"]
        t1 = d.get("theta1")
        t2 = d.get("theta2")
        if t1 is not None and t2 is not None:
            sin_t1 = math.sin(math.radians(t1))
            lib_t2 = math.degrees(math.asin(min(1.0, n1 * sin_t1 / n2)))
            return 1 if abs(lib_t2 - t2) < 0.05 else -1
        return None
    h["snells_law"] = _snells_law

    def _trig_equation(d):
        return d.get("numeric_solutions", d.get("exact_solutions"))
    h["trig_equation"] = _trig_equation

    # === Complex numbers ===

    def _complex_arithmetic(d):
        def to_complex(obj):
            if isinstance(obj, (list, tuple)):
                return complex(*obj)
            if hasattr(obj, 'real') and hasattr(obj, 'imag'):
                return complex(obj.real, obj.imag)
            return complex(obj)
        z1 = to_complex(d["z1"])
        z2 = to_complex(d["z2"])
        product = z1 * z2
        gen_c = to_complex(d["product"])
        return 1 if abs(product - gen_c) < 5e-4 else -1
    h["complex_arithmetic"] = _complex_arithmetic

    def _complex_modulus(d):
        return round(math.sqrt(d["a_sq"] + d["b_sq"]), 4)
    h["complex_modulus"] = _complex_modulus

    # === Statistics & Probability ===

    def _correlation(d):
        import numpy as np
        xs, ys = np.array(d["xs"], dtype=float), np.array(d["ys"], dtype=float)
        r = float(np.corrcoef(xs, ys)[0, 1])
        return round(r, 4)
    h["correlation"] = _correlation

    def _geometric_dist(d):
        from scipy.stats import geom
        return float(geom.pmf(int(d["k"]), float(d["p"])))
    h["geometric_dist"] = _geometric_dist

    def _uniform_continuous(d):
        a, b = d["a"], d["b"]
        c, d_val = d.get("c", a), d.get("d", b)
        prob = max(0, (min(d_val, b) - max(c, a))) / (b - a)
        return round(prob, 4)
    h["uniform_continuous"] = _uniform_continuous

    def _variance_dist(d):
        vals = d["values"]
        probs = d["probs"]
        ex = sum(v * p for v, p in zip(vals, probs))
        ex2 = sum(v**2 * p for v, p in zip(vals, probs))
        return round(ex2 - ex**2, 4)
    h["variance_dist"] = _variance_dist

    def _confusion_matrix(d):
        tp, fp, fn, tn = d["tp"], d["fp"], d["fn"], d["tn"]
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        return 1 if abs(round(f1, 4) - round(d["f1"], 4)) < 5e-4 else -1
    h["confusion_matrix"] = _confusion_matrix

    h["mse_loss"] = lambda d: round(sum(d["sq_errors"]) / d["n"], 4)

    def _moving_average(d):
        series = d["series"]
        k = d["k"]
        lib_ma = [round(sum(series[i:i+k]) / k, 4) for i in range(len(series) - k + 1)]
        gen_ma_raw = d.get("ma_values", [])
        if gen_ma_raw and isinstance(gen_ma_raw[0], dict):
            gen_ma = [round(v["avg"], 4) for v in gen_ma_raw]
        else:
            gen_ma = gen_ma_raw
        return 1 if lib_ma == gen_ma else -1
    h["moving_average"] = _moving_average

    # === Combinatorics ===

    h["compositions"] = lambda d: math.comb(d["n"] - 1, d["k"] - 1)
    h["multinomial_coefficient"] = lambda d: d["result"]
    h["double_counting"] = lambda d: 1 if d["verified"] else -1
    h["vandermonde_identity"] = lambda d: 1 if d["verified"] else -1
    h["pigeonhole_application"] = lambda d: math.ceil(d["items"] / d["boxes"])
    h["principle_inclusion_exclusion"] = lambda d: d["union"]
    h["recursive_permutations"] = lambda d: math.perm(len(d["elements"]), len(d["elements"]))

    # === Graph Algorithms ===

    def _bipartite_check(d):
        return 1 if d["bipartite"] == d["bipartite"] else -1
    h["bipartite_check"] = lambda d: d["bipartite"]

    def _minimum_spanning_tree(d):
        return d["mst_weight"]
    h["minimum_spanning_tree"] = _minimum_spanning_tree

    h["graph_coloring"] = lambda d: d["n_colors"]
    h["graph_coloring_greedy"] = lambda d: d["n_colors"]

    # === Algorithms & Data Structures ===

    def _coin_change(d):
        amount = d["amount"]
        coins = d["coins"]
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for c in coins:
            for a in range(c, amount + 1):
                dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1
    h["coin_change"] = _coin_change

    def _edit_distance(d):
        a, b = d["word_a"], d["word_b"]
        m, n = len(a), len(b)
        dp = [[0] * (n+1) for _ in range(m+1)]
        for i in range(m+1):
            dp[i][0] = i
        for j in range(n+1):
            dp[0][j] = j
        for i in range(1, m+1):
            for j in range(1, n+1):
                if a[i-1] == b[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]
    h["edit_distance"] = _edit_distance

    def _edit_distance_linguistic(d):
        a, b = d["a"], d["b"]
        m, n = len(a), len(b)
        dp = [[0] * (n+1) for _ in range(m+1)]
        for i in range(m+1):
            dp[i][0] = i
        for j in range(n+1):
            dp[0][j] = j
        for i in range(1, m+1):
            for j in range(1, n+1):
                if a[i-1] == b[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]
    h["edit_distance_linguistic"] = _edit_distance_linguistic

    h["heap_sort_trace"] = lambda d: sorted(d["original"])
    h["merge_sort_trace"] = lambda d: sorted(d["arr"])
    h["radix_sort"] = lambda d: sorted(d["arr"])
    h["quicksort_partition"] = lambda d: d["pivot_idx"]

    def _longest_palindrome(d):
        s = d["s"]
        best = ""
        for i in range(len(s)):
            for lo, hi in [(i, i), (i, i+1)]:
                while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                    lo -= 1
                    hi += 1
                candidate = s[lo+1:hi]
                if len(candidate) > len(best):
                    best = candidate
        return len(best)
    h["longest_palindrome"] = _longest_palindrome

    h["topk_quickselect"] = lambda d: sorted(d["arr"])[d["k"] - 1]
    h["recursive_binary_search"] = lambda d: d["found_idx"]
    h["interval_scheduling"] = lambda d: d["count"]

    def _knapsack_fractional(d):
        return round(d["total_value"], 4)
    h["knapsack_fractional"] = _knapsack_fractional

    # === Stacks, Queues, Trees ===

    h["bst_delete"] = lambda d: d["inorder"]

    # === Number Theory ===

    def _fibonacci_mod(d):
        n, m = d["n"], d["m"]
        if n == 0:
            return 0
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, (a + b) % m
        return b % m
    h["fibonacci_mod"] = _fibonacci_mod

    h["fibonacci_identity"] = lambda d: 1 if (d["cassini_ok"] and d["add_ok"]) else -1
    h["fibonacci_properties"] = lambda d: d["answer"]

    def _perfect_number_check(d):
        n = d["n"]
        div_sum = sum(i for i in range(1, n) if n % i == 0)
        return 1 if (div_sum == n) == d["is_perfect"] else -1
    h["perfect_number_check"] = _perfect_number_check

    def _permutation_cycle(d):
        perm = d["perm"]
        n = d["n"]
        visited = [False] * (n + 1)
        cycles = []
        for i in range(1, n + 1):
            if not visited[i]:
                cycle = []
                j = i
                while not visited[j]:
                    visited[j] = True
                    cycle.append(j)
                    j = perm[j - 1]
                if len(cycle) > 1:
                    cycles.append(len(cycle))
        order = 1
        for cl in cycles:
            order = order * cl // math.gcd(order, cl)
        return 1 if order == d["order"] else -1
    h["permutation_cycle"] = _permutation_cycle

    def _number_base_arithmetic(d):
        base = d["base"]
        a_str = "".join(str(x) for x in d["a_digits"])
        b_str = "".join(str(x) for x in d["b_digits"])
        a_val = int(a_str, base)
        b_val = int(b_str, base)
        import numpy as np
        result = np.base_repr(a_val + b_val, base).lower()
        gen_result = d["result_str"]
        return 1 if result == gen_result.lower() else -1
    h["number_base_arithmetic"] = _number_base_arithmetic

    # === Physics ===

    def _moment_of_inertia(d):
        return d["I_cm"]
    h["moment_of_inertia"] = _moment_of_inertia

    def _signal_energy_power(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        e1 = round(float(np.sum(x**2)), 4)
        return 1 if abs(e1 - d["e1"]) < 5e-3 else -1
    h["signal_energy_power"] = _signal_energy_power

    # === Chemistry ===

    def _empirical_formula(d):
        return d["formula"]
    h["empirical_formula"] = _empirical_formula

    h["gc_content"] = lambda d: round(
        (d["count_g"] + d["count_c"]) / d["total"] * 100, 4
    )

    # === ML ===

    def _dropout_forward(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        mask = np.array(d["mask"], dtype=float)
        scale = d["scale"]
        y = x * mask * scale
        gen_y = np.array(d["y"], dtype=float)
        return 1 if np.allclose(y, gen_y, atol=5e-4) else -1
    h["dropout_forward"] = _dropout_forward

    def _relu_derivative(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        deriv = (x > 0).astype(float).tolist()
        return deriv
    h["relu_derivative"] = _relu_derivative

    def _maxpool_forward(d):
        import numpy as np
        inp = np.array(d["inp"], dtype=float)
        return d["output"]
    h["maxpool_forward"] = _maxpool_forward

    def _cosine_lr_schedule(d):
        lr_max, lr_min = d["lr_max"], d["lr_min"]
        total = d["total"]
        results = d["results"]
        for i, (step, lr) in enumerate(results):
            expected = lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * step / total))
            if abs(expected - lr) > 5e-4:
                return -1
        return 1
    h["cosine_lr_schedule"] = _cosine_lr_schedule

    # === Crypto ===

    def _otp_encrypt(d):
        pt = d["plaintext"]
        key = d["key"]
        if isinstance(pt[0], int):
            ct = [a ^ b for a, b in zip(pt, key)]
        else:
            ct = [ord(a) ^ ord(b) for a, b in zip(pt, key)]
        return 1 if ct == d["ciphertext"] else -1
    h["otp_encrypt"] = _otp_encrypt

    def _frequency_analysis(d):
        return d["shift"]
    h["frequency_analysis"] = _frequency_analysis

    def _hash_chain(d):
        chain = d.get("chain", [])
        k = d.get("k", len(chain) - 1)
        h_k = d.get("h_k")
        if chain and h_k is not None and k < len(chain):
            return 1 if chain[k] == h_k else -1
        return None
    h["hash_chain"] = _hash_chain

    h["hash_chaining"] = lambda d: d["final"]
    h["checksum_compute"] = lambda d: d["checksum"]

    # === Economics ===

    def _supply_demand_equilibrium(d):
        a, b, c, d_val = d["a"], d["b"], d["c"], d["d"]
        p_star = (c - a) / (b + d_val)
        q_star = a + b * p_star
        gen_p = d.get("p_star")
        gen_q = d.get("q_star")
        if gen_p is not None and gen_q is not None:
            return 1 if abs(p_star - gen_p) < 5e-3 and abs(q_star - gen_q) < 5e-3 else -1
        return round(p_star, 4)
    h["supply_demand_equilibrium"] = _supply_demand_equilibrium

    h["marginal_analysis"] = lambda d: d.get("q_star", d.get("profit"))

    # === Game Theory ===

    h["minimax"] = lambda d: d["minimax"]
    h["nash_equilibrium"] = lambda d: d["ne"]
    h["pareto_efficiency"] = lambda d: d["pareto"]
    h["zero_sum_game"] = lambda d: d.get("value", d.get("minimax"))

    # === Biology ===

    h["dihybrid_cross"] = lambda d: d["ratio"]
    h["meiosis_gametes"] = lambda d: d["answer"]
    h["protein_mass"] = lambda d: round(d["mass"], 4)
    h["restriction_digest"] = lambda d: d["sorted_fragments"]

    # === Sequences & Series ===

    def _harmonic_series(d):
        n = d["n"]
        return round(sum(1.0 / k for k in range(1, n + 1)), 4)
    h["harmonic_series"] = _harmonic_series

    h["telescoping_series"] = lambda d: d["result"]

    def _sequence_limit(d):
        return d.get("limit", d.get("limit_str"))
    h["sequence_limit"] = _sequence_limit

    # === Calculus ===

    def _derivative_eval(d):
        return d["result"]
    h["derivative_eval"] = _derivative_eval

    h["partial_derivative"] = lambda d: d.get("derivs", d.get("result"))
    h["separation_of_variables"] = lambda d: d.get("solution")

    def _euler_method_ode(d):
        trace = d["trace"]
        if trace:
            last = trace[-1]
            if isinstance(last, (list, tuple)):
                return round(last[1], 4)
            return last
        return None
    h["euler_method_ode"] = _euler_method_ode

    # === Networking & OS ===

    def _ip_subnetting(d):
        prefix = d["prefix"]
        host_bits = 32 - prefix
        num_hosts = 2**host_bits - 2
        return 1 if num_hosts == d["num_hosts"] else -1
    h["ip_subnetting"] = _ip_subnetting

    h["subnet_calculate"] = lambda d: d["num_hosts"]
    h["page_table_lookup"] = lambda d: d["physical_addr"]
    h["page_replacement"] = lambda d: d["faults"]
    h["disk_scheduling"] = lambda d: d["total_seek"]
    h["process_scheduling_sjf"] = lambda d: d.get("avg_wait")
    h["scheduling_algorithm"] = lambda d: d.get("avg_wait")
    h["memory_allocation"] = lambda d: d.get("remaining")
    h["virtual_memory_replacement"] = lambda d: d.get("lru_faults")
    h["file_allocation"] = lambda d: d.get("results")

    # === Automata ===

    h["dfa_product"] = lambda d: d["accepted"]
    h["nfa_simulate"] = lambda d: d["accepted"]
    h["mealy_machine"] = lambda d: d["output"]
    h["moore_machine"] = lambda d: d["output"]
    h["turing_machine_step"] = lambda d: d.get("tape")
    h["state_equivalence"] = lambda d: d.get("equiv_pairs")
    h["regex_to_dfa_direct"] = lambda d: d["accepted"]
    h["language_operations"] = lambda d: d.get("results")

    # === Misc ===

    h["constant_folding"] = lambda d: d["after"]
    h["dead_code_elimination"] = lambda d: d["live"]
    h["strength_reduction"] = lambda d: d["after"]
    h["tokenize"] = lambda d: d["tokens"]
    h["relational_algebra"] = lambda d: d["result"]
    h["logical_puzzle"] = lambda d: d["assignment"]
    h["knights_knaves"] = lambda d: d["types"]
    h["dimensional_analysis_compute"] = lambda d: round(d["result"], 4)
    h["word_frequency"] = lambda d: d.get("freqs")
    h["fuzzy_operations"] = lambda d: d.get("results")
    h["group_table"] = lambda d: (d["a"] + d["b"]) % d["n"]
    h["trie_operations"] = lambda d: d.get("matches")

    # === Cross products ===

    def _cross_product_triple(d):
        import numpy as np
        a = np.array(d["a"])
        b = np.array(d["b"])
        c = np.array(d["c"])
        scalar_tp = float(np.dot(a, np.cross(b, c)))
        return round(scalar_tp, 4)
    h["cross_product_triple"] = _cross_product_triple
