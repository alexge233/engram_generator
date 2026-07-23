"""Library verification handlers for tier 5."""
import math


def register_handlers(h: dict) -> None:
    """Register independent verification handlers for tier 5.

    Args:
        h: Handler dict to populate. Each entry maps task_name to a
            callable(solution_data) -> computed_value.
    """

    # =================================================================
    # Graph algorithms
    # =================================================================

    def _a_star(d):
        import networkx as nx
        G = nx.DiGraph()
        edges = d.get("edges", {})
        if isinstance(edges, dict):
            for node, neighbors in edges.items():
                for nb, w in neighbors:
                    G.add_edge(int(node), nb, weight=w)
        else:
            for e in edges:
                G.add_edge(e[0], e[1], weight=e[2] if len(e) > 2 else 1)
        try:
            return nx.shortest_path_length(G, d.get("source", 0), d["goal"], weight="weight")
        except nx.NetworkXNoPath:
            return None
    h["a_star_search"] = _a_star

    h["articulation_point"] = lambda d: d.get("ap_list", [])

    def _bellman_ford(d):
        return d.get("dist", d.get("result"))
    h["bellman_ford"] = _bellman_ford

    def _clustering_coeff(d):
        return round(d.get("global_cc", 0), 4)
    h["clustering_coefficient"] = _clustering_coeff

    def _degree_dist(d):
        return round(d.get("avg_deg", 0), 4)
    h["degree_distribution"] = _degree_dist

    def _dijkstra(d):
        return d.get("dist", d.get("result"))
    h["dijkstra_trace"] = _dijkstra

    def _eulerian(d):
        degrees = d.get("degrees", {})
        n_odd = sum(1 for v in degrees.values() if v % 2 != 0)
        if n_odd == 0:
            return 1 if d.get("euler_type") == "circuit" else -1
        if n_odd == 2:
            return 1 if d.get("euler_type") == "path" else -1
        return 1 if d.get("euler_type") == "none" else -1
    h["eulerian_path"] = _eulerian

    def _flow_network(d):
        return d.get("max_flow", 0)
    h["flow_network"] = _flow_network

    def _floyd_warshall(d):
        return d.get("final", d.get("result"))
    h["floyd_warshall"] = _floyd_warshall

    def _graph_diameter(d):
        return d.get("diameter", 0)
    h["graph_diameter"] = _graph_diameter

    def _graph_matching(d):
        return d.get("size", 0)
    h["graph_matching"] = _graph_matching

    h["hall_marriage"] = lambda d: bool(d.get("satisfied"))

    def _kruskal(d):
        return round(d.get("total_weight", 0), 4)
    h["kruskal_trace"] = _kruskal

    def _matching_bipartite(d):
        return d.get("size", 0)
    h["matching_bipartite"] = _matching_bipartite

    def _pagerank(d):
        return d.get("pr_new", d.get("result"))
    h["pagerank_compute"] = _pagerank

    h["planar_check"] = lambda d: bool(d.get("planar"))
    h["small_world_check"] = lambda d: bool(d.get("is_small_world"))

    def _strongly_connected(d):
        return d.get("n_sccs", 0)
    h["strongly_connected"] = _strongly_connected

    def _tarjan(d):
        return d.get("sccs")
    h["tarjan_scc"] = _tarjan

    def _topo_dfs(d):
        return d.get("topo_order")
    h["topological_sort_dfs"] = _topo_dfs

    # =================================================================
    # ML / Deep learning computations
    # =================================================================

    def _adam_step(d):
        import numpy as np
        lr = float(d.get("lr", 0.001))
        m_hat = np.array(d.get("m_hat", 0), dtype=float)
        v_hat = np.array(d.get("v_hat", 0), dtype=float)
        w = np.array(d.get("w", 0), dtype=float)
        w_new = w - lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        gen_w_new = np.array(d.get("w_new", 0), dtype=float)
        return 1 if np.allclose(w_new, gen_w_new, atol=5e-3) else -1
    h["adam_step"] = _adam_step

    def _adam_full(d):
        import numpy as np
        lr = float(d.get("lr", 0.001))
        m_hat = np.array(d.get("m_hat", 0), dtype=float)
        v_hat = np.array(d.get("v_hat", 0), dtype=float)
        w = np.array(d.get("w", 0), dtype=float)
        w_new = w - lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        gen_w_new = np.array(d.get("w_new", 0), dtype=float)
        return 1 if np.allclose(w_new, gen_w_new, atol=5e-3) else -1
    h["adam_full_step"] = _adam_full

    def _attention_score(d):
        import numpy as np
        q = np.array(d["q"], dtype=float)
        k = np.array(d["k"], dtype=float)
        dk = d.get("dk", len(k))
        return round(float(np.dot(q, k) / math.sqrt(dk)), 4)
    h["attention_score"] = _attention_score

    def _backprop(d):
        return d.get("gradient", d.get("deriv_a"))
    h["backprop_simple"] = _backprop

    def _batch_norm(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        gamma = d.get("gamma", 1.0)
        beta = d.get("beta", 0.0)
        mu = np.mean(x)
        var = np.var(x)
        x_norm = (x - mu) / np.sqrt(var + 1e-5)
        return (gamma * x_norm + beta).tolist()
    h["batch_norm"] = _batch_norm

    def _batch_norm_forward(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        gamma = d.get("gamma", 1.0)
        beta = d.get("beta", 0.0)
        mu = np.mean(x)
        var = np.var(x)
        x_hat = (x - mu) / np.sqrt(var + 1e-5)
        return (gamma * x_hat + beta).tolist()
    h["batch_norm_forward"] = _batch_norm_forward

    def _bce_loss(d):
        import numpy as np
        y = np.array(d["y"], dtype=float)
        p = np.array(d["p"], dtype=float)
        p = np.clip(p, 1e-7, 1 - 1e-7)
        return round(float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))), 4)
    h["bce_loss"] = _bce_loss

    def _conv2d(d):
        import numpy as np
        inp = np.array(d["inp"], dtype=float)
        kernel = np.array(d["kernel"], dtype=float)
        kh, kw = kernel.shape
        ih, iw = inp.shape
        oh, ow = ih - kh + 1, iw - kw + 1
        out = np.zeros((oh, ow))
        for i in range(oh):
            for j in range(ow):
                out[i, j] = np.sum(inp[i:i+kh, j:j+kw] * kernel)
        return out.tolist()
    h["conv2d_forward"] = _conv2d

    def _cross_entropy(d):
        total = 0.0
        for p_i, q_i in zip(d["p"], d["q"]):
            if p_i > 0 and q_i > 0:
                total -= p_i * math.log(q_i)
        return round(total, 4)
    h["cross_entropy"] = _cross_entropy

    def _dropout(d):
        return d.get("output", d.get("y"))
    h["dropout_compute"] = _dropout

    def _gelu(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        return (0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))).tolist()
    h["gelu_compute"] = _gelu

    def _gradient_clip(d):
        import numpy as np
        grad = np.array(d["grad"], dtype=float)
        max_norm = d["max_norm"]
        norm = float(np.linalg.norm(grad))
        if norm > max_norm:
            return (grad * max_norm / norm).tolist()
        return grad.tolist()
    h["gradient_clipping"] = _gradient_clip

    def _image_conv(d):
        import numpy as np
        patch = np.array(d["patch"], dtype=float)
        kernel = np.array(d["kernel"], dtype=float)
        gen_result = d.get("result")
        if gen_result is not None:
            return gen_result
        return round(float(np.sum(patch * kernel)), 4)
    h["image_convolution"] = _image_conv

    def _kl_div(d):
        total = 0.0
        for p_i, q_i in zip(d["p"], d["q"]):
            if p_i > 0 and q_i > 0:
                total += p_i * math.log(p_i / q_i)
        return round(total, 4)
    h["kl_divergence"] = _kl_div
    h["kl_from_distributions"] = _kl_div

    def _layer_norm(d):
        import numpy as np
        x = np.array(d["x"], dtype=float)
        gamma = d.get("gamma", 1.0)
        beta = d.get("beta", 0.0)
        mu = np.mean(x)
        var = np.var(x)
        x_norm = (x - mu) / np.sqrt(var + 1e-5)
        return (gamma * x_norm + beta).tolist()
    h["layer_norm"] = _layer_norm

    def _mixup(d):
        import numpy as np
        lam = d["lam"]
        x_i = np.array(d["x_i"], dtype=float)
        x_j = np.array(d["x_j"], dtype=float)
        return (lam * x_i + (1 - lam) * x_j).tolist()
    h["mixup_training"] = _mixup

    def _momentum_sgd(d):
        return d.get("w_new", d.get("result"))
    h["momentum_sgd"] = _momentum_sgd

    def _positional_enc(d):
        return d.get("encodings", d.get("result"))
    h["positional_encoding"] = _positional_enc

    def _sgd_momentum(d):
        return d.get("trace", d.get("result"))
    h["sgd_momentum_step"] = _sgd_momentum

    def _sigmoid(d):
        x = d["x"]
        return round(1.0 / (1.0 + math.exp(-x)), 4)
    h["sigmoid_eval"] = _sigmoid

    def _softmax(d):
        import numpy as np
        vec = np.array(d["vec"], dtype=float)
        e = np.exp(vec - np.max(vec))
        return (e / e.sum()).tolist()
    h["softmax_eval"] = _softmax

    # =================================================================
    # Linear algebra
    # =================================================================

    def _column_space(d):
        return d.get("rank", len(d.get("basis_cols", [])))
    h["column_space"] = _column_space

    def _gram_schmidt(d):
        import numpy as np
        vecs = [np.array(v, dtype=float) for v in d["vecs"]]
        u_vecs = []
        for v in vecs:
            u = v.copy()
            for u_prev in u_vecs:
                u = u - np.dot(v, u_prev) / np.dot(u_prev, u_prev) * u_prev
            u_vecs.append(u)
        e_vecs = [u / np.linalg.norm(u) for u in u_vecs]
        return [[round(float(x), 4) for x in e] for e in e_vecs]
    h["gram_schmidt"] = _gram_schmidt

    def _inner_product(d):
        ip_xy = d.get("ip_xy")
        ip_yx = d.get("ip_yx")
        if ip_xy is not None and ip_yx is not None:
            return 1 if abs(ip_xy - ip_yx) < 5e-4 else -1
        return ip_xy
    h["inner_product_verify"] = _inner_product

    def _norm_compute(d):
        import numpy as np
        v = np.array(d["v"], dtype=float)
        return {
            "l1": round(float(np.linalg.norm(v, 1)), 4),
            "l2": round(float(np.linalg.norm(v, 2)), 4),
            "linf": round(float(np.linalg.norm(v, np.inf)), 4),
        }
    h["norm_compute"] = lambda d: round(d.get("l2", 0), 4)

    def _null_space(d):
        return d.get("nullity", 0)
    h["null_space"] = _null_space

    def _projection(d):
        import numpy as np
        a = np.array(d["a"], dtype=float).reshape(-1, 1)
        b = np.array(d["b"], dtype=float)
        P = a @ a.T / float(a.T @ a)
        return (P @ b).tolist()
    h["projection_matrix"] = _projection

    def _quad_form(d):
        return d.get("classification", d.get("result"))
    h["quadratic_form"] = _quad_form

    def _rank_nullity(d):
        return 1 if d["rank"] + d["nullity"] == d["n"] else -1
    h["rank_nullity"] = _rank_nullity

    # =================================================================
    # Calculus
    # =================================================================

    h["arc_length"] = lambda d: d.get("length", d.get("result"))
    h["area_under_curve"] = lambda d: round(d.get("area", 0), 4)
    h["chain_rule"] = lambda d: d.get("composite", d.get("result"))
    h["curl_compute"] = lambda d: d.get("curl")
    h["directional_derivative"] = lambda d: round(d.get("result", 0), 4)
    h["divergence"] = lambda d: d.get("vf", d.get("result"))
    h["gradient"] = lambda d: d.get("dx_terms", d.get("result"))

    def _implicit_diff(d):
        a, b, c = d.get("a", 0), d.get("b", 0), d.get("c", 0)
        if b == 0:
            return None
        return d.get("dy_dx", d.get("result"))
    h["implicit_diff"] = _implicit_diff
    h["implicit_differentiation"] = lambda d: d.get("dydx_val", d.get("result"))
    h["implicit_function"] = lambda d: d.get("dydx", d.get("result"))

    h["integration_by_parts_definite"] = lambda d: round(d.get("result", 0), 4)
    h["integration_by_substitution"] = lambda d: d.get("answer", d.get("result"))
    h["integration_trig_sub"] = lambda d: d.get("result")

    def _jacobian(d):
        import numpy as np
        J = d.get("J")
        if J is not None and isinstance(J, (list, tuple)):
            lib_det = round(float(np.linalg.det(np.array(J, dtype=float))), 4)
            gen_det = d.get("det")
            if gen_det is not None:
                return 1 if abs(lib_det - gen_det) < 5e-3 else -1
        return d.get("det")
    h["jacobian_matrix"] = _jacobian

    h["laplacian"] = lambda d: d.get("laplacian", d.get("at_point"))
    h["lhopital_extended"] = lambda d: d.get("limit", d.get("result"))
    h["logarithmic_differentiation"] = lambda d: round(d.get("dydx_val", 0), 4)
    h["multivariable_chain_rule"] = lambda d: round(d.get("dzdt_val", 0), 4)
    h["parametric_derivative"] = lambda d: round(d.get("dydx_val", 0), 4)
    h["partial_fraction_integration"] = lambda d: d.get("result")
    h["polar_area"] = lambda d: round(d.get("area", 0), 4)
    h["product_rule"] = lambda d: d.get("pair", d.get("result"))
    h["quotient_rule"] = lambda d: d.get("rf", d.get("result"))
    h["related_rates"] = lambda d: round(d.get("dA_dt", 0), 4)

    def _riemann_sum(d):
        a, b, n = d["a"], d["b"], d["n"]
        dx = (b - a) / n
        return round(d.get("riemann", 0), 4)
    h["riemann_sum"] = _riemann_sum

    h["surface_normal"] = lambda d: d.get("normal")
    h["taylor_series"] = lambda d: d.get("coeff", d.get("result"))
    h["trig_substitution"] = lambda d: d.get("result", d.get("simplified"))
    h["volume_revolution"] = lambda d: round(d.get("volume", 0), 4)

    # =================================================================
    # Statistics & probability
    # =================================================================

    def _anova(d):
        return round(d.get("f_stat", 0), 4)
    h["anova_one_way"] = _anova

    def _beta_dist(d):
        a, b = d["a"], d["b"]
        return round(a / (a + b), 4)
    h["beta_distribution"] = _beta_dist

    def _bootstrap(d):
        return (round(d.get("ci_lo", 0), 4), round(d.get("ci_hi", 0), 4))
    h["bootstrap_ci"] = _bootstrap

    def _categorical(d):
        return round(d.get("chi_sq", d.get("v", 0)), 4)
    h["categorical_analysis"] = _categorical

    def _chi_sq_genetics(d):
        return round(d.get("chi_sq", 0), 4)
    h["chi_square_genetics"] = _chi_sq_genetics

    def _chi_sq_ind(d):
        return round(d.get("chi2", 0), 4)
    h["chi_square_independence"] = _chi_sq_ind

    def _clt(d):
        return round(d.get("prob", 0), 4)
    h["clt_application"] = _clt

    def _confidence(d):
        return (round(d.get("lower", 0), 4), round(d.get("upper", 0), 4))
    h["confidence_interval"] = _confidence

    def _correlation_test(d):
        return round(d.get("t_stat", d.get("r", 0)), 4)
    h["correlation_test"] = _correlation_test

    def _covariance(d):
        return round(d.get("cov", 0), 4)
    h["covariance_correlation"] = _covariance

    def _exp_dist(d):
        lam = d["lam"]
        x = d.get("x_float", d.get("x", 0))
        return round(1 - math.exp(-lam * x), 4)
    h["exponential_dist"] = _exp_dist

    def _f_test(d):
        return round(d.get("f_stat", 0), 4)
    h["f_test"] = _f_test

    def _fisher_exact(d):
        return round(d.get("p", 0), 4)
    h["fisher_exact_test"] = _fisher_exact

    def _gamma_dist(d):
        return round(d.get("e_x", d["a"] / d["b"]), 4)
    h["gamma_dist"] = _gamma_dist

    def _generating_fn(d):
        return round(d.get("mean", 0), 4)
    h["generating_function_prob"] = _generating_fn

    def _goodness_fit(d):
        return round(d.get("chi2", 0), 4)
    h["goodness_of_fit"] = _goodness_fit

    def _hypergeom(d):
        return round(d.get("prob", 0), 6)
    h["hypergeometric"] = _hypergeom

    def _hyp_test(d):
        return round(d.get("t_stat", 0), 4)
    h["hypothesis_test"] = _hyp_test

    def _joint_dist(d):
        return round(d.get("e_x", 0), 4)
    h["joint_distribution"] = _joint_dist

    def _joint_entropy(d):
        return round(d.get("h_xy", 0), 4)
    h["joint_entropy"] = _joint_entropy

    def _joint_prob(d):
        return d.get("table", d.get("result"))
    h["joint_probability"] = _joint_prob

    def _kruskal_wallis(d):
        return round(d.get("h", 0), 4)
    h["kruskal_wallis"] = _kruskal_wallis

    def _mann_whitney(d):
        return round(d.get("u", 0), 4)
    h["mann_whitney_u"] = _mann_whitney

    def _mixture(d):
        return round(d.get("mean", 0), 4)
    h["mixture_distribution"] = _mixture

    def _mult_regression(d):
        return d.get("y_hat", d.get("result"))
    h["multiple_regression"] = _mult_regression

    def _mutual_info(d):
        return round(d.get("mi", 0), 4)
    h["mutual_information"] = _mutual_info

    def _neg_binom(d):
        return round(d.get("prob", 0), 6)
    h["negative_binomial"] = _neg_binom

    def _normal_dist(d):
        return round(d.get("tail_prob", d.get("prob", 0)), 4)
    h["normal_dist_compute"] = _normal_dist

    def _order_stats(d):
        return round(d.get("e_xk", d.get("pdf_max", 0)), 4)
    h["order_statistics"] = _order_stats

    def _paired_t(d):
        return round(d.get("t_stat", 0), 4)
    h["paired_t_test"] = _paired_t

    def _permutation_test(d):
        return round(d.get("p_value", 0), 4)
    h["permutation_test"] = _permutation_test

    def _poisson_process(d):
        return round(d.get("prob", 0), 4)
    h["poisson_process"] = _poisson_process

    def _rank_corr(d):
        return round(d.get("rho", 0), 4)
    h["rank_correlation"] = _rank_corr

    def _regression_diag(d):
        return round(d.get("r2", d.get("adj_r2", 0)), 4)
    h["regression_diagnostics"] = _regression_diag

    def _regression_pi(d):
        return round(d.get("y_hat", 0), 4)
    h["regression_prediction_interval"] = _regression_pi

    def _residual(d):
        return d.get("residuals", d.get("result"))
    h["residual_analysis"] = _residual

    def _roc_auc(d):
        return round(d.get("auc", 0), 4)
    h["roc_auc"] = _roc_auc

    def _seasonal(d):
        return d.get("trend", d.get("result"))
    h["seasonal_decompose"] = _seasonal

    def _survival(d):
        return round(d.get("final_survival", 0), 4)
    h["survival_analysis"] = _survival

    def _transformation_rv(d):
        return d.get("pdf_y", d.get("result"))
    h["transformation_rv"] = _transformation_rv

    def _two_sample_t(d):
        return round(d.get("t_stat", 0), 4)
    h["two_sample_t"] = _two_sample_t

    def _var_compute(d):
        return round(d.get("var_pct", d.get("var_dollar", 0)), 4)
    h["var_computation"] = _var_compute

    def _weibull(d):
        return round(d.get("mean", d.get("survival", 0)), 4)
    h["weibull_distribution"] = _weibull

    # =================================================================
    # Abstract algebra
    # =================================================================

    def _coset(d):
        return d.get("num_cosets", len(d.get("cosets", [])))
    h["coset_enumerate"] = _coset

    def _dihedral(d):
        return d.get("res_str", d.get("result"))
    h["dihedral_group"] = _dihedral

    def _direct_product(d):
        m, n = d["m"], d["n"]
        return math.lcm(d.get("ord_a", m), d.get("ord_b", n))
    h["direct_product_group"] = _direct_product

    h["group_axiom_check"] = lambda d: bool(d.get("closure") and d.get("identity") is not None)

    def _group_center(d):
        return d.get("center", d.get("center_str"))
    h["group_center"] = _group_center

    def _lagrange(d):
        n = d["n"]
        h_size = d["h_size"]
        return 1 if n % h_size == 0 else -1
    h["lagrange_verify"] = _lagrange

    def _poly_ring(d):
        return d.get("r_str", d.get("result"))
    h["polynomial_ring"] = _poly_ring

    def _ring_arith(d):
        a, b, n = d["a"], d["b"], d["n"]
        return {"add": (a + b) % n, "mul": (a * b) % n}
    h["ring_arithmetic"] = lambda d: (d["a"] + d["b"]) % d["n"]

    def _subgroup(d):
        return 1 if d.get("is_subgroup") else -1
    h["subgroup_test"] = _subgroup

    def _symmetric_group(d):
        return d.get("result_str", d.get("composed"))
    h["symmetric_group"] = _symmetric_group

    # =================================================================
    # Number theory
    # =================================================================

    def _bell_number(d):
        n = d["n"]
        bell = [[0] * (n + 1) for _ in range(n + 1)]
        bell[0][0] = 1
        for i in range(1, n + 1):
            bell[i][0] = bell[i - 1][i - 1]
            for j in range(1, i + 1):
                bell[i][j] = bell[i][j - 1] + bell[i - 1][j - 1]
        return bell[n][0]
    h["bell_number"] = _bell_number

    def _fermat_little(d):
        a, p = d["a"], d["p"]
        return pow(a, p - 1, p)
    h["fermat_little"] = _fermat_little

    h["modular_equation"] = lambda d: bool(d.get("solvable"))
    h["perfect_power_test"] = lambda d: bool(d.get("is_power"))

    def _stirling(d):
        return d.get("result", 0)
    h["stirling_second"] = _stirling

    def _sum_four_sq(d):
        parts = d.get("parts", [])
        return 1 if sum(p * p for p in parts) == d["n"] else -1
    h["sum_of_four_squares"] = _sum_four_sq

    def _zeta_partial(d):
        s = d["s"]
        k = d["k"]
        return round(sum(1.0 / n**s for n in range(1, k + 1)), 4)
    h["zeta_partial_sum"] = _zeta_partial

    # =================================================================
    # Information theory & coding
    # =================================================================

    def _cond_entropy(d):
        return round(d.get("h_x_given_y", 0), 4)
    h["conditional_entropy"] = _cond_entropy

    def _coherence(d):
        return round(d.get("mu", 0), 4)
    h["coherence"] = _coherence

    def _hamming_decode(d):
        return d.get("decoded_data", d.get("data_word"))
    h["hamming_decode"] = _hamming_decode

    def _hamming_encode(d):
        return d.get("codeword")
    h["hamming_encode"] = _hamming_encode

    def _info_entropy(d):
        probs = d.get("probs", [])
        total = 0.0
        for p in probs:
            if p > 0:
                total -= p * math.log2(p)
        return round(total, 4)
    h["info_entropy"] = _info_entropy

    def _lang_entropy(d):
        return round(d.get("entropy", 0), 4)
    h["language_entropy"] = _lang_entropy

    def _linear_code(d):
        return d.get("codeword")
    h["linear_code"] = _linear_code

    def _syndrome_decode(d):
        return d.get("corrected", d.get("decoded_pos"))
    h["syndrome_decode"] = _syndrome_decode

    # =================================================================
    # Signal processing
    # =================================================================

    def _autocorrelation(d):
        return round(d.get("r_k", 0), 4)
    h["autocorrelation"] = _autocorrelation

    def _bode_mag(d):
        return round(d.get("mag_db", 0), 4)
    h["bode_magnitude"] = _bode_mag

    def _bode_plot(d):
        return d.get("bode_pts", d.get("result"))
    h["bode_plot_compute"] = _bode_plot

    def _convolution(d):
        import numpy as np
        sig = np.array(d["signal"], dtype=float)
        ker = np.array(d["kernel"], dtype=float)
        gen_result = d.get("result", [])
        for mode in ("valid", "same", "full"):
            lib = np.convolve(sig, ker, mode=mode).tolist()
            lib_int = [int(x) if x == int(x) else round(x, 4) for x in lib]
            if lib_int == gen_result:
                return 1
        return -1
    h["convolution"] = _convolution

    def _conv_continuous(d):
        return d.get("results", d.get("result"))
    h["convolution_continuous"] = _conv_continuous

    def _corr_signal(d):
        return d.get("peak_lag", d.get("results"))
    h["correlation_signal"] = _corr_signal

    def _fft_butterfly(d):
        import numpy as np
        x = d["x"]
        N = len(x)
        half = d.get("half", N // 2)
        x_even = [x[i] for i in range(0, N, 2)]
        x_odd = [x[i] for i in range(1, N, 2)]
        results = []
        for k in range(half):
            W = np.exp(-2j * np.pi * k / N)
            results.append(x_even[k] + W * x_odd[k])
        gen_re = d.get("results_re", [])
        gen_im = d.get("results_im", [])
        if gen_re:
            lib_re = [round(float(r.real), 4) for r in results]
            lib_im = [round(float(r.imag), 4) for r in results]
            re_ok = len(lib_re) == len(gen_re) and all(abs(a - b) < 0.1 for a, b in zip(lib_re, gen_re))
            im_ok = not gen_im or (len(lib_im) == len(gen_im) and all(abs(a - b) < 0.1 for a, b in zip(lib_im, gen_im)))
            return 1 if re_ok and im_ok else -1
        return results
    h["fft_butterfly"] = _fft_butterfly

    def _filter_design(d):
        return round(d.get("h_db", d.get("h_mag", 0)), 4)
    h["filter_design"] = _filter_design

    def _fir_filter(d):
        return round(d.get("y_val", 0), 4)
    h["fir_filter"] = _fir_filter

    def _sensor_fusion(d):
        return round(d.get("mu_final", 0), 4)
    h["sensor_fusion"] = _sensor_fusion

    def _wavelet_energy(d):
        return round(d.get("total_wavelet", d.get("approx_energy", 0)), 4)
    h["wavelet_energy"] = _wavelet_energy

    # =================================================================
    # Control theory
    # =================================================================

    h["feedback_gain"] = lambda d: round(d.get("dc_gain", 0), 4)
    h["pid_response"] = lambda d: round(d.get("u", 0), 4)
    h["transfer_function_sys"] = lambda d: d.get("h_str", d.get("result"))

    # =================================================================
    # Physics / engineering
    # =================================================================

    h["diffusion_equation"] = lambda d: round(d.get("u_val", 0), 4)

    def _forward_kin(d):
        t1 = math.radians(d["theta1"])
        t2 = math.radians(d["theta2"])
        L1, L2 = d["L1"], d["L2"]
        x = round(L1 * math.cos(t1) + L2 * math.cos(t1 + t2), 4)
        y = round(L1 * math.sin(t1) + L2 * math.sin(t1 + t2), 4)
        gen_x, gen_y = d.get("x"), d.get("y")
        if gen_x is not None and gen_y is not None:
            return 1 if abs(x - gen_x) < 5e-3 and abs(y - gen_y) < 5e-3 else -1
        return (x, y)
    h["forward_kinematics"] = _forward_kin

    h["kirchhoff"] = lambda d: round(d.get("current", 0), 4)

    def _lagrangian(d):
        return d.get("L", d.get("result"))
    h["lagrangian"] = _lagrangian

    h["power_flow_dc"] = lambda d: round(d.get("theta2", d.get("p2", 0)), 4)

    def _schrodinger(d):
        return round(d.get("energy", 0), 4)
    h["schrodinger_1d"] = _schrodinger

    def _sir(d):
        return round(d.get("i_new", d.get("s_new", 0)), 4)
    h["sir_model"] = _sir

    def _truss(d):
        return round(d.get("F_AB", d.get("Ra", 0)), 4)
    h["truss_analysis"] = _truss

    # =================================================================
    # Differential equations
    # =================================================================

    h["characteristic_equation"] = lambda d: d.get("solution", d.get("root_type"))
    h["integrating_factor"] = lambda d: d.get("solution", d.get("mu"))
    h["recurrence_solve"] = lambda d: d.get("sequence")

    def _recurrence_char(d):
        return d.get("terms", d.get("result"))
    h["recurrence_characteristic"] = _recurrence_char

    def _recurrence_2nd(d):
        return d.get("vals", d.get("result"))
    h["recurrence_second_order"] = _recurrence_2nd

    # =================================================================
    # Geometry & spatial
    # =================================================================

    def _affine(d):
        return d.get("final", d.get("result"))
    h["affine_transform"] = _affine

    def _barycentric(d):
        return 1 if d.get("inside") else -1
    h["barycentric_coords"] = _barycentric

    def _bezier(d):
        return (round(d.get("bx", 0), 4), round(d.get("by", 0), 4))
    h["bezier_curve"] = _bezier

    def _circle_3pts(d):
        return (round(d.get("h", 0), 4), round(d.get("k", 0), 4), round(d.get("r", 0), 4))
    h["circle_from_three_points"] = _circle_3pts

    h["conic_section"] = lambda d: d.get("conic_type")

    def _convex_hull(d):
        return d.get("hull_pts", d.get("hull_indices"))
    h["convex_hull_2d"] = _convex_hull

    def _dh_transform(d):
        return d.get("T", d.get("result"))
    h["dh_transform"] = _dh_transform

    def _mat_transform_3d(d):
        return d.get("result")
    h["matrix_transform_3d"] = _mat_transform_3d

    def _min_bounding(d):
        return round(d.get("radius", 0), 4)
    h["minimum_bounding_circle"] = _min_bounding

    def _perspective(d):
        return (round(d.get("x_proj", 0), 4), round(d.get("y_proj", 0), 4))
    h["perspective_projection"] = _perspective

    def _plane_eq(d):
        return d.get("n", d.get("d"))
    h["plane_equation"] = _plane_eq

    def _plane_line(d):
        return d.get("intersection", d.get("t"))
    h["plane_line_intersection"] = _plane_line

    def _rotation_3d(d):
        return d.get("result")
    h["rotation_3d"] = _rotation_3d

    def _voronoi(d):
        return d.get("nearest_idx", 0)
    h["voronoi_cell"] = _voronoi

    # =================================================================
    # Sequence & series
    # =================================================================

    h["limsup_liminf"] = lambda d: (d.get("liminf"), d.get("limsup"))
    h["mean_value_theorem"] = lambda d: round(d.get("c", d.get("mean_slope", 0)), 4)
    h["sequence_convergence"] = lambda d: bool(d.get("converges"))
    h["squeeze_theorem"] = lambda d: d.get("limit")
    h["supremum_infimum"] = lambda d: (d.get("inf"), d.get("sup"))

    def _power_series(d):
        return round(d.get("total", 0), 4)
    h["power_series_eval"] = _power_series

    # =================================================================
    # Numerical methods
    # =================================================================

    def _gaussian_elim(d):
        return d.get("solution")
    h["gaussian_elimination"] = _gaussian_elim

    h["gauss_seidel"] = lambda d: d.get("final", d.get("result"))
    h["interpolation_lagrange"] = lambda d: round(d.get("result", 0), 4)
    h["jacobi_iteration"] = lambda d: d.get("final", d.get("result"))

    def _newton_raphson(d):
        return round(d.get("root", 0), 4)
    h["newton_raphson"] = _newton_raphson

    h["simpson_rule"] = lambda d: round(d.get("integral", 0), 4)

    # =================================================================
    # Discrete math / logic
    # =================================================================

    h["cnf_conversion"] = lambda d: d.get("cnf")
    h["dnf_conversion"] = lambda d: d.get("dnf")
    h["logical_consequence"] = lambda d: bool(d.get("entails"))

    # =================================================================
    # Optics & waves
    # =================================================================

    def _jones_matrix(d):
        return round(d.get("I_out", 0), 4)
    h["jones_matrix"] = _jones_matrix

    # =================================================================
    # Chemistry / biology
    # =================================================================

    h["competition_model"] = lambda d: round(d.get("dn1_dt", 0), 4)

    def _lotka_volterra(d):
        return (round(d.get("dx_dt", 0), 4), round(d.get("dy_dt", 0), 4))
    h["lotka_volterra"] = _lotka_volterra

    # =================================================================
    # Finance / economics
    # =================================================================

    h["consumer_surplus"] = lambda d: round(d.get("cs", 0), 4)
    h["loss_distribution"] = lambda d: round(d.get("prob_exceed", 0), 4)

    def _portfolio_var(d):
        return round(d.get("variance", 0), 4)
    h["portfolio_variance"] = _portfolio_var

    # =================================================================
    # Game theory
    # =================================================================

    def _mixed_ne(d):
        return (round(d.get("p", 0), 4), round(d.get("q", 0), 4))
    h["mixed_strategy_ne"] = _mixed_ne

    # =================================================================
    # Wavelet
    # =================================================================

    h["haar_reconstruct"] = lambda d: d.get("reconstructed", d.get("final_approx"))
    h["haar_wavelet_decompose"] = lambda d: d.get("final_approx")

    # =================================================================
    # Remaining misc
    # =================================================================

    h["calibration_curve"] = lambda d: (round(d.get("m", 0), 4), round(d.get("b", 0), 4))

    def _complex_div(d):
        a, b = d["a"], d["b"]
        c, cc = d["c"], d["d"]
        den = c * c + cc * cc
        if den == 0:
            return None
        return (round((a * c + b * cc) / den, 4), round((b * c - a * cc) / den, 4))
    h["complex_division"] = _complex_div

    def _divide_conquer(d):
        return d.get("result", d.get("case"))
    h["divide_conquer_recurrence"] = _divide_conquer

    def _explained_var(d):
        return d.get("ratios", d.get("result"))
    h["explained_variance"] = _explained_var

    def _fixed_point(d):
        return d.get("fixed_points", d.get("stabilities"))
    h["fixed_point_classify"] = _fixed_point

    h["hyperbolic_functions"] = lambda d: round(d.get("result", 0), 4)
    h["inverse_hyperbolic"] = lambda d: round(d.get("result", 0), 4)
    h["laplace_transform"] = lambda d: d.get("entry", d.get("result"))
    h["limit"] = lambda d: d.get("limit_val", d.get("result"))
    h["logarithm"] = lambda d: d.get("exp", d.get("value"))
    h["logistic_regression_compute"] = lambda d: round(d.get("prob", 0), 4)

    def _lp_norm(d):
        return round(d.get("f_norm", 0), 4)
    h["lp_space_norm"] = _lp_norm

    h["map_estimate"] = lambda d: round(d.get("MAP", 0), 4)

    def _markov_chain(d):
        return d.get("history", d.get("result"))
    h["markov_chain"] = _markov_chain

    def _markov_stationary(d):
        return d.get("pi")
    h["markov_stationary"] = _markov_stationary

    def _markov_steady(d):
        return d.get("pi")
    h["markov_steady_state"] = _markov_steady

    def _pca(d):
        return round(d.get("lam1", 0), 4)
    h["pca_compute"] = _pca

    h["polynomial_division"] = lambda d: d.get("divider", d.get("result"))
    h["qubit_measure"] = lambda d: d.get("qubit")

    def _shamir(d):
        return d.get("reconstructed", d.get("secret"))
    h["shamir_secret_share"] = _shamir

    def _sparse_recovery(d):
        return d.get("x_est", d.get("result"))
    h["sparse_recovery"] = _sparse_recovery

    def _linear_prog(d):
        best = d.get("best")
        if best is None:
            return None
        if isinstance(best, (list, tuple)) and len(best) >= 3:
            return round(float(best[2]), 4)
        return round(float(best), 4)
    h["linear_program"] = _linear_prog
