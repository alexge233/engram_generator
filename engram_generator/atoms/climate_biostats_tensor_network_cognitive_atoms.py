"""Knowledge atoms for climate science, biostatistics, tensor analysis,
network science, and cognitive science domains.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Climate Science ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="radiative_forcing",
    content=(
        "Radiative forcing is the change in net downward radiative flux "
        "at the tropopause due to a change in an external driver of "
        "climate change, such as CO2 concentration. For CO2: "
        "dF = 5.35 * ln(C/C0) W/m^2, where C is the current "
        "concentration and C0 is the pre-industrial reference."
    ),
    example=(
        "Given C=560 ppm, C0=280 ppm: "
        "dF = 5.35 * ln(560/280) = 5.35 * 0.6931 = 3.708 W/m^2"
    ),
    tier=5, domain="climate_science",
    source="Wikipedia contributors, 'Radiative forcing', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Radiative_forcing",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="albedo_energy",
    content=(
        "Planetary albedo determines the fraction of incoming solar "
        "radiation reflected back to space. The absorbed energy is "
        "E_abs = S * (1 - alpha) * pi * R^2, where S is the solar "
        "constant (~1361 W/m^2), alpha is the albedo, and R is the "
        "planet's radius."
    ),
    example=(
        "Given S=1361 W/m^2, alpha=0.3, R=6.371e6 m: "
        "E_abs = 1361 * 0.7 * pi * (6.371e6)^2 = 1.215e17 W"
    ),
    tier=4, domain="climate_science",
    source="Wikipedia contributors, 'Albedo', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Albedo",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="greenhouse_effect",
    content=(
        "The greenhouse effect warms Earth's surface because greenhouse "
        "gases absorb and re-emit longwave radiation. The effective "
        "temperature without greenhouse gases is T_e = (S(1-a)/(4*sigma))^(1/4), "
        "where sigma is the Stefan-Boltzmann constant. The greenhouse "
        "effect raises the surface temperature above T_e by ~33 K."
    ),
    example=(
        "Given S=1361, a=0.3, sigma=5.67e-8: "
        "T_e = (1361*0.7/(4*5.67e-8))^0.25 = (238.175/2.268e-7)^0.25 = 255 K. "
        "Actual surface ~288 K, so greenhouse effect = 33 K."
    ),
    tier=5, domain="climate_science",
    source="Wikipedia contributors, 'Greenhouse effect', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Greenhouse_effect",
    prerequisites=["stefan_boltzmann"],
))

register_atom(Atom(
    atom_type="formula",
    name="carbon_budget",
    content=(
        "The carbon budget is the cumulative amount of CO2 emissions "
        "permitted to keep global warming below a specified temperature "
        "target. Remaining budget = total budget - cumulative emissions. "
        "The TCRE (transient climate response to cumulative emissions) "
        "relates temperature change to cumulative CO2: dT = TCRE * C_cum."
    ),
    example=(
        "Given TCRE=0.45 degC/TtCO2, target dT=1.5 degC, emitted=2.39 TtCO2: "
        "total budget = 1.5/0.45 = 3.33 TtCO2. "
        "Remaining = 3.33 - 2.39 = 0.94 TtCO2 = 940 GtCO2."
    ),
    tier=4, domain="climate_science",
    source="Wikipedia contributors, 'Carbon budget', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Carbon_budget",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="sea_level_rise",
    content=(
        "Thermal expansion of ocean water contributes to sea level rise. "
        "For a column of water of depth h and temperature change dT, "
        "the sea level rise is dh = beta * h * dT, where beta is the "
        "thermal expansion coefficient (~2.1e-4 /K for seawater)."
    ),
    example=(
        "Given beta=2.1e-4 /K, h=3700 m, dT=1 K: "
        "dh = 2.1e-4 * 3700 * 1 = 0.777 m"
    ),
    tier=5, domain="climate_science",
    source="Wikipedia contributors, 'Sea level rise', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Sea_level_rise",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="climate_sensitivity",
    content=(
        "Equilibrium climate sensitivity (ECS) is the global mean "
        "temperature increase for a doubling of atmospheric CO2 "
        "concentration after the climate system reaches equilibrium. "
        "dT_2x = dF_2x / lambda, where dF_2x = 3.7 W/m^2 is the "
        "forcing from CO2 doubling and lambda is the climate feedback "
        "parameter (W/m^2/K)."
    ),
    example=(
        "Given dF_2x=3.7 W/m^2, lambda=1.23 W/m^2/K: "
        "ECS = 3.7/1.23 = 3.0 K"
    ),
    tier=5, domain="climate_science",
    source="Wikipedia contributors, 'Climate sensitivity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Climate_sensitivity",
    prerequisites=["division"],
))

# ── Biostatistics ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="survival_analysis",
    content=(
        "The Kaplan-Meier estimator estimates the survival function "
        "S(t) from lifetime data. At each event time t_i: "
        "S(t) = product over i of (1 - d_i/n_i), where d_i is the "
        "number of events and n_i is the number at risk just before t_i."
    ),
    example=(
        "Times: 1, 2, 3. At t=1: d=1, n=5, S=4/5=0.8. "
        "At t=2: d=1, n=4, S=0.8*3/4=0.6. "
        "At t=3: d=1, n=3, S=0.6*2/3=0.4."
    ),
    tier=5, domain="biostatistics",
    source="Wikipedia contributors, 'Kaplan-Meier estimator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="odds_ratio",
    content=(
        "The odds ratio (OR) measures association between exposure and "
        "outcome. For a 2x2 table with cells a, b, c, d: "
        "OR = (a*d)/(b*c). OR=1 means no association, OR>1 means "
        "positive association, OR<1 means negative association."
    ),
    example=(
        "Given a=30, b=70, c=10, d=90 (exposed cases / controls): "
        "OR = (30*90)/(70*10) = 2700/700 = 3.857"
    ),
    tier=5, domain="biostatistics",
    source="Wikipedia contributors, 'Odds ratio', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Odds_ratio",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="number_needed_treat",
    content=(
        "Number needed to treat (NNT) is the number of patients who "
        "need to be treated to prevent one additional bad outcome. "
        "NNT = 1/ARR, where ARR = |CER - EER| is the absolute risk "
        "reduction, CER is the control event rate, and EER is the "
        "experimental event rate."
    ),
    example=(
        "Given CER=0.40, EER=0.30: ARR = 0.40 - 0.30 = 0.10. "
        "NNT = 1/0.10 = 10 patients."
    ),
    tier=4, domain="biostatistics",
    source="Wikipedia contributors, 'Number needed to treat', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Number_needed_to_treat",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="sensitivity_specificity",
    content=(
        "Sensitivity (true positive rate) = TP/(TP+FN). "
        "Specificity (true negative rate) = TN/(TN+FP). "
        "A perfect test has sensitivity=1 and specificity=1. "
        "PPV = TP/(TP+FP). NPV = TN/(TN+FN)."
    ),
    example=(
        "Given TP=80, FP=10, FN=20, TN=90: "
        "Sensitivity = 80/100 = 0.80. Specificity = 90/100 = 0.90. "
        "PPV = 80/90 = 0.889. NPV = 90/110 = 0.818."
    ),
    tier=4, domain="biostatistics",
    source="Wikipedia contributors, 'Sensitivity and specificity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Sensitivity_and_specificity",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="sample_size",
    content=(
        "For estimating a proportion with margin of error E at "
        "confidence level z_alpha/2: n = (z^2 * p * (1-p)) / E^2. "
        "For comparing two means: n per group = 2*(z_alpha/2 + z_beta)^2 * sigma^2 / delta^2."
    ),
    example=(
        "Given z=1.96 (95% CI), p=0.5, E=0.05: "
        "n = (1.96^2 * 0.25) / 0.0025 = 0.9604/0.0025 = 384.16, round to 385."
    ),
    tier=5, domain="biostatistics",
    source="Wikipedia contributors, 'Sample size determination', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Sample_size_determination",
    prerequisites=["z_score"],
))

register_atom(Atom(
    atom_type="formula",
    name="meta_analysis",
    content=(
        "Meta-analysis combines results from multiple studies. The "
        "fixed-effect model uses inverse-variance weighting: "
        "theta_hat = sum(w_i * theta_i) / sum(w_i), where "
        "w_i = 1/sigma_i^2 is the weight for study i."
    ),
    example=(
        "Study 1: theta=0.5, sigma=0.2 (w=25). Study 2: theta=0.3, sigma=0.1 (w=100). "
        "theta_hat = (25*0.5 + 100*0.3)/(25+100) = (12.5+30)/125 = 0.34."
    ),
    tier=6, domain="biostatistics",
    source="Wikipedia contributors, 'Meta-analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Meta-analysis",
    prerequisites=["weighted_sum"],
))

# ── Tensor Analysis ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="tensor_contraction",
    content=(
        "Tensor contraction sums over one upper and one lower index, "
        "reducing the rank by 2. For a rank-(1,1) tensor T^i_j, "
        "contraction gives the trace: T^i_i = sum_i T^i_i."
    ),
    example=(
        "Given T^i_j = [[2,1],[3,4]]: "
        "contraction T^i_i = T^0_0 + T^1_1 = 2 + 4 = 6."
    ),
    tier=6, domain="tensor_analysis",
    source="Wikipedia contributors, 'Tensor contraction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Tensor_contraction",
    prerequisites=["matrix_trace"],
))

register_atom(Atom(
    atom_type="formula",
    name="covariant_derivative",
    content=(
        "The covariant derivative generalises the directional "
        "derivative to curved spaces. For a vector field V^i: "
        "nabla_j V^i = partial_j V^i + Gamma^i_jk V^k, "
        "where Gamma^i_jk are the Christoffel symbols."
    ),
    example=(
        "In 2D polar, V=(V^r, V^theta), Gamma^r_theta_theta=-r: "
        "nabla_theta V^r = dV^r/dtheta + Gamma^r_theta_theta * V^theta "
        "= dV^r/dtheta - r*V^theta."
    ),
    tier=7, domain="tensor_analysis",
    source="Wikipedia contributors, 'Covariant derivative', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Covariant_derivative",
    prerequisites=["christoffel_symbol"],
))

register_atom(Atom(
    atom_type="formula",
    name="metric_tensor",
    content=(
        "The metric tensor g_ij defines distances and angles on a "
        "manifold. The line element ds^2 = g_ij dx^i dx^j. "
        "For Euclidean 2D in polar coordinates: "
        "ds^2 = dr^2 + r^2 dtheta^2, so g = diag(1, r^2)."
    ),
    example=(
        "Spherical coordinates: "
        "ds^2 = dr^2 + r^2 dtheta^2 + r^2 sin^2(theta) dphi^2. "
        "g = diag(1, r^2, r^2 sin^2(theta)). "
        "det(g) = r^4 sin^2(theta)."
    ),
    tier=6, domain="tensor_analysis",
    source="Wikipedia contributors, 'Metric tensor', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Metric_tensor_(general_relativity)",
    prerequisites=["determinant"],
))

register_atom(Atom(
    atom_type="formula",
    name="ricci_tensor",
    content=(
        "The Ricci tensor R_ij is a contraction of the Riemann "
        "curvature tensor: R_ij = R^k_ikj. It appears in Einstein's "
        "field equations: R_ij - (1/2)*R*g_ij = (8*pi*G/c^4)*T_ij."
    ),
    example=(
        "For a 2-sphere of radius a: R_theta_theta = 1, "
        "R_phi_phi = sin^2(theta). Ricci scalar R = 2/a^2."
    ),
    tier=7, domain="tensor_analysis",
    source="Wikipedia contributors, 'Ricci curvature', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Ricci_curvature",
    prerequisites=["christoffel_symbol", "metric_tensor"],
))

register_atom(Atom(
    atom_type="formula",
    name="levi_civita",
    content=(
        "The Levi-Civita symbol epsilon_ijk is the totally "
        "antisymmetric tensor. In 3D: epsilon_123=1, and any "
        "even permutation gives +1, odd gives -1, repeated index gives 0. "
        "Used in cross products: (A x B)_i = epsilon_ijk A_j B_k."
    ),
    example=(
        "Cross product A=(1,0,0), B=(0,1,0): "
        "(AxB)_3 = epsilon_312*A_1*B_2 = 1*1*1 = 1. "
        "AxB = (0,0,1)."
    ),
    tier=5, domain="tensor_analysis",
    source="Wikipedia contributors, 'Levi-Civita symbol', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Levi-Civita_symbol",
    prerequisites=["cross_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="index_gymnastics",
    content=(
        "Index raising and lowering uses the metric tensor: "
        "V^i = g^ij V_j (raising), V_i = g_ij V^j (lowering). "
        "g^ij is the inverse metric. This converts between "
        "contravariant and covariant components."
    ),
    example=(
        "In 2D with g = diag(1, r^2), g_inv = diag(1, 1/r^2): "
        "Given V_theta = r^2, V^theta = (1/r^2)*r^2 = 1."
    ),
    tier=6, domain="tensor_analysis",
    source="Wikipedia contributors, 'Raising and lowering indices', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Raising_and_lowering_indices",
    prerequisites=["metric_tensor"],
))

# ── Network Science ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="degree_distribution",
    content=(
        "The degree distribution P(k) gives the probability that a "
        "randomly chosen node has degree k. For scale-free networks, "
        "P(k) ~ k^(-gamma) with gamma typically between 2 and 3."
    ),
    example=(
        "Graph with degrees [2,2,3,3,3,4,5]: "
        "P(2)=2/7, P(3)=3/7, P(4)=1/7, P(5)=1/7. "
        "Mean degree = (2+2+3+3+3+4+5)/7 = 22/7 = 3.143."
    ),
    tier=5, domain="network_science",
    source="Wikipedia contributors, 'Degree distribution', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Degree_distribution",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="clustering_coefficient",
    content=(
        "The local clustering coefficient C_i of node i is the "
        "fraction of possible edges between its neighbours that exist: "
        "C_i = 2*e_i / (k_i*(k_i-1)), where e_i is the number of "
        "edges among neighbours and k_i is the degree."
    ),
    example=(
        "Node with degree k=4, and 3 edges among its 4 neighbours: "
        "C = 2*3/(4*3) = 6/12 = 0.5."
    ),
    tier=5, domain="network_science",
    source="Wikipedia contributors, 'Clustering coefficient', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Clustering_coefficient",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="betweenness_centrality",
    content=(
        "Betweenness centrality measures how often a node lies on "
        "shortest paths between other nodes: "
        "C_B(v) = sum_{s!=v!=t} sigma_st(v)/sigma_st, "
        "where sigma_st is the total number of shortest paths from "
        "s to t and sigma_st(v) is those passing through v."
    ),
    example=(
        "Star graph with centre node C and 4 leaves: "
        "All shortest paths between leaves pass through C. "
        "C_B(C) = C(4,2) = 6. Normalised: 6/((5-1)*(5-2)/2) = 6/6 = 1.0."
    ),
    tier=6, domain="network_science",
    source="Wikipedia contributors, 'Betweenness centrality', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Betweenness_centrality",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="formula",
    name="pagerank_compute",
    content=(
        "PageRank assigns importance scores to nodes in a directed "
        "graph. PR(i) = (1-d)/N + d * sum_{j->i} PR(j)/L(j), "
        "where d is the damping factor (typically 0.85), N is the "
        "number of nodes, and L(j) is the out-degree of j."
    ),
    example=(
        "Two-node graph: A->B, B->A. d=0.85, N=2. "
        "By symmetry PR(A)=PR(B)=1/2=0.5."
    ),
    tier=5, domain="network_science",
    source="Wikipedia contributors, 'PageRank', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/PageRank",
    prerequisites=["markov_chain"],
))

register_atom(Atom(
    atom_type="definition",
    name="small_world_check",
    content=(
        "A small-world network has high clustering coefficient (like a "
        "lattice) but short average path length (like a random graph). "
        "Formally: C >> C_random and L ~ L_random, where C_random ~ k/N "
        "and L_random ~ ln(N)/ln(k)."
    ),
    example=(
        "Watts-Strogatz graph N=1000, k=10, p=0.1: "
        "C=0.35 >> C_random=0.01. L=3.2 ~ L_random=3.0. "
        "Small-world: yes."
    ),
    tier=5, domain="network_science",
    source="Wikipedia contributors, 'Small-world network', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Small-world_network",
    prerequisites=["clustering_coefficient"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="community_detect",
    content=(
        "Community detection partitions a network into groups of "
        "densely connected nodes. Modularity Q measures partition "
        "quality: Q = (1/2m) sum_ij [A_ij - k_i*k_j/(2m)] delta(c_i, c_j), "
        "where m is total edges, A is adjacency, k is degree."
    ),
    example=(
        "Graph with two cliques of 3 nodes each, connected by one edge: "
        "Partitioning into the two cliques gives high Q. "
        "m=7, within-community edges=6, Q = 6/7 - (6*6)/(2*7)^2 ~ 0.408."
    ),
    tier=6, domain="network_science",
    source="Wikipedia contributors, 'Community structure', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Community_structure",
    prerequisites=["clustering_coefficient"],
))

# ── Cognitive Science ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="signal_detection",
    content=(
        "Signal detection theory measures the ability to discriminate "
        "signal from noise. d' (d-prime) = z(hit rate) - z(false alarm rate), "
        "where z is the inverse normal CDF. Higher d' means better "
        "discrimination."
    ),
    example=(
        "Hit rate=0.85, false alarm rate=0.15: "
        "z(0.85)=1.036, z(0.15)=-1.036. "
        "d' = 1.036 - (-1.036) = 2.073."
    ),
    tier=5, domain="cognitive_science",
    source="Wikipedia contributors, 'Detection theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Detection_theory",
    prerequisites=["z_score"],
))

register_atom(Atom(
    atom_type="formula",
    name="memory_decay",
    content=(
        "Ebbinghaus forgetting curve models memory retention over time: "
        "R(t) = e^(-t/S), where R is retention (0-1), t is time, "
        "and S is the stability (time constant). After time S, "
        "retention drops to 1/e ~ 0.368."
    ),
    example=(
        "Given S=24 hours, t=48 hours: "
        "R = e^(-48/24) = e^(-2) = 0.1353. "
        "Only 13.5% retained after 2 days."
    ),
    tier=5, domain="cognitive_science",
    source="Wikipedia contributors, 'Forgetting curve', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Forgetting_curve",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="reaction_time",
    content=(
        "Hick's law predicts choice reaction time as a function of "
        "the number of alternatives: RT = a + b * log2(n), "
        "where a is base reaction time, b is the increment per bit "
        "of information, and n is the number of choices."
    ),
    example=(
        "Given a=200ms, b=150ms, n=8 choices: "
        "RT = 200 + 150 * log2(8) = 200 + 150 * 3 = 650 ms."
    ),
    tier=5, domain="cognitive_science",
    source="Wikipedia contributors, 'Hick\\'s law', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hick%27s_law",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="weber_fraction",
    content=(
        "Weber's law states that the just noticeable difference (JND) "
        "is proportional to the stimulus magnitude: dI/I = k, "
        "where dI is the JND, I is the stimulus intensity, "
        "and k is the Weber fraction (constant for a given sense)."
    ),
    example=(
        "Weight discrimination k=0.02, holding 500g: "
        "JND = 0.02 * 500 = 10g. "
        "You can just notice a difference of 10g."
    ),
    tier=4, domain="cognitive_science",
    source="Wikipedia contributors, 'Weber-Fechner law', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="information_processing",
    content=(
        "The human information processing rate can be measured in "
        "bits/second. Channel capacity C = max I(X;Y) where I is "
        "mutual information. Miller's law suggests working memory "
        "capacity is 7 +/- 2 chunks."
    ),
    example=(
        "Absolute judgement of tones: 5 distinguishable levels = "
        "log2(5) = 2.32 bits. Processing rate with 500ms per trial: "
        "C = 2.32/0.5 = 4.64 bits/second."
    ),
    tier=6, domain="cognitive_science",
    source="Wikipedia contributors, 'Information processing', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Human_information_processing",
    prerequisites=["information_theory"],
))

register_atom(Atom(
    atom_type="formula",
    name="rescorla_wagner",
    content=(
        "The Rescorla-Wagner model of associative learning updates "
        "associative strength V on each trial: "
        "dV = alpha * beta * (lambda - V_total), "
        "where alpha is salience, beta is learning rate, "
        "lambda is the maximum conditioning, and V_total is the "
        "sum of all cue strengths."
    ),
    example=(
        "alpha=0.5, beta=0.3, lambda=1, V_total=0.4: "
        "dV = 0.5 * 0.3 * (1 - 0.4) = 0.15 * 0.6 = 0.09. "
        "New V = 0.4 + 0.09 = 0.49."
    ),
    tier=5, domain="cognitive_science",
    source="Wikipedia contributors, 'Rescorla-Wagner model', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Rescorla%E2%80%93Wagner_model",
    prerequisites=["multiplication"],
))
