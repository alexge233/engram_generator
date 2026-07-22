"""Verification registry mapping generators to independent verification methods.

Each entry maps a task_name to:
- method: 'library', 'formula', 'reference', or 'llm'
- library: PyPI package name (e.g. 'sympy', 'numpy')
- function: specific function path (e.g. 'sympy.diff', 'numpy.linalg.eigvals')
- formula: canonical formula string for formula-only generators
- notes: any additional context

This registry is the single source of truth for how each generator's
output can be independently verified without circularity.
"""
from dataclasses import dataclass, field


@dataclass
class VerificationEntry:
    """Verification metadata for one generator.

    Attributes:
        task_name: Generator task identifier.
        method: Verification approach (library/formula/reference/llm).
        library: PyPI package name, if applicable.
        function: Specific library function path.
        formula: Canonical formula for formula-only verification.
        pypi: PyPI install target (e.g. 'scipy>=1.11').
        notes: Additional context.
    """

    task_name: str
    method: str
    library: str = ""
    function: str = ""
    formula: str = ""
    pypi: str = ""
    notes: str = ""


# Master registry: task_name -> VerificationEntry
VERIFICATION_REGISTRY: dict[str, VerificationEntry] = {}


def _r(task_name: str, method: str, **kwargs) -> None:
    """Register a verification entry."""
    VERIFICATION_REGISTRY[task_name] = VerificationEntry(
        task_name=task_name, method=method, **kwargs,
    )


# =========================================================================
# TIER 0 -- Foundations
# =========================================================================

_r("addition", "library", library="math", function="operator.add",
   pypi="(stdlib)", notes="a + b")
_r("subtraction", "library", library="math", function="operator.sub",
   pypi="(stdlib)", notes="a - b with borrow chain")
_r("sorting", "library", library="builtins", function="sorted()",
   pypi="(stdlib)")
_r("digit_root", "library", library="math", function="iterative sum",
   pypi="(stdlib)", formula="dr(n) = 1 + (n-1) % 9")
_r("multiplication", "library", library="math", function="operator.mul",
   pypi="(stdlib)")
_r("division", "library", library="math", function="divmod()",
   pypi="(stdlib)")
_r("fibonacci", "library", library="math", function="iterative",
   pypi="(stdlib)")
_r("caesar", "library", library="builtins", function="chr/ord shift",
   pypi="(stdlib)")
_r("run_length", "library", library="itertools", function="groupby()",
   pypi="(stdlib)")
_r("linear_equation", "library", library="sympy", function="sympy.solve",
   pypi="sympy>=1.12")
_r("expression_simplify", "library", library="sympy",
   function="sympy.simplify", pypi="sympy>=1.12")
_r("modular", "library", library="math", function="operator.mod",
   pypi="(stdlib)")
_r("exponentiation", "library", library="math", function="pow()",
   pypi="(stdlib)")
_r("gcd", "library", library="math", function="math.gcd",
   pypi="(stdlib)")
_r("polynomial_eval", "library", library="numpy",
   function="numpy.polyval", pypi="numpy>=1.24")
_r("boolean_eval", "library", library="builtins",
   function="eval(bool expr)", pypi="(stdlib)")
_r("truth_table", "library", library="builtins",
   function="eval(bool expr)", pypi="(stdlib)")
_r("negation", "library", library="builtins", function="not",
   pypi="(stdlib)")
_r("comparison", "library", library="builtins", function="max/min",
   pypi="(stdlib)")
_r("string_reverse", "library", library="builtins", function="[::-1]",
   pypi="(stdlib)")
_r("character_count", "library", library="builtins", function="len()",
   pypi="(stdlib)")

# =========================================================================
# TIER 1 -- Basic operations
# =========================================================================

_r("derivative", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12")
_r("quadratic", "library", library="sympy", function="sympy.solve",
   pypi="sympy>=1.12")
_r("binomial", "library", library="math", function="math.comb",
   pypi="(stdlib)")
_r("lcm", "library", library="math", function="math.lcm",
   pypi="(stdlib)")
_r("integral", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("second_derivative", "library", library="sympy",
   function="sympy.diff(f, x, 2)", pypi="sympy>=1.12")
_r("system_equations", "library", library="sympy",
   function="sympy.solve([eq1,eq2])", pypi="sympy>=1.12")
_r("determinant", "library", library="numpy",
   function="numpy.linalg.det", pypi="numpy>=1.24")
_r("permutation", "library", library="math", function="math.perm",
   pypi="(stdlib)")
_r("area_rectangle", "library", library="math",
   function="l * w", pypi="(stdlib)")
_r("perimeter_rectangle", "library", library="math",
   function="2*(l+w)", pypi="(stdlib)")
_r("pythagorean", "library", library="math", function="math.hypot",
   pypi="(stdlib)")
_r("area_triangle", "library", library="math",
   function="0.5*b*h", pypi="(stdlib)")
_r("area_circle", "library", library="math",
   function="math.pi*r**2", pypi="(stdlib)")
_r("circumference", "library", library="math",
   function="2*math.pi*r", pypi="(stdlib)")
_r("implication", "library", library="builtins",
   function="not p or q", pypi="(stdlib)")
_r("biconditional", "library", library="builtins",
   function="p == q", pypi="(stdlib)")

# =========================================================================
# TIER 2 -- Intermediate
# =========================================================================

_r("mod_pow", "library", library="math", function="pow(base, exp, mod)",
   pypi="(stdlib)")
_r("mod_inv", "library", library="math", function="pow(a, -1, m)",
   pypi="(stdlib)")
_r("definite_integral", "library", library="sympy",
   function="sympy.integrate(f, (x, a, b))", pypi="sympy>=1.12")
_r("chain_rule", "library", library="sympy",
   function="sympy.diff(f(g(x)), x)", pypi="sympy>=1.12")
_r("product_rule", "library", library="sympy",
   function="sympy.diff(f*g, x)", pypi="sympy>=1.12")
_r("taylor_series", "library", library="sympy",
   function="sympy.series(f, x, n=k)", pypi="sympy>=1.12")
_r("gradient", "library", library="sympy",
   function="[sympy.diff(f, v) for v in vars]", pypi="sympy>=1.12")
_r("matrix_multiply", "library", library="numpy",
   function="numpy.matmul", pypi="numpy>=1.24")
_r("matrix_inverse", "library", library="numpy",
   function="numpy.linalg.inv", pypi="numpy>=1.24")
_r("eigenvalue", "library", library="numpy",
   function="numpy.linalg.eigvals", pypi="numpy>=1.24")
_r("edit_distance", "library", library="builtins",
   function="DP algorithm", pypi="(stdlib)",
   notes="Levenshtein distance via dynamic programming")
_r("shortest_path", "library", library="networkx",
   function="networkx.shortest_path_length", pypi="networkx>=3.0")
_r("graph_reach", "library", library="networkx",
   function="networkx.has_path", pypi="networkx>=3.0")
_r("topo_sort", "library", library="networkx",
   function="networkx.topological_sort", pypi="networkx>=3.0")
_r("totient", "library", library="sympy",
   function="sympy.totient", pypi="sympy>=1.12")
_r("crt", "library", library="sympy",
   function="sympy.ntheory.crt", pypi="sympy>=1.12")
_r("primality", "library", library="sympy",
   function="sympy.isprime", pypi="sympy>=1.12")
_r("factorisation", "library", library="sympy",
   function="sympy.factorint", pypi="sympy>=1.12")

# =========================================================================
# TIER 3 -- Applied science & statistics
# =========================================================================

_r("bayes_theorem", "library", library="math",
   function="p_ba * p_a / p_b", pypi="(stdlib)",
   formula="P(A|B) = P(B|A)*P(A)/P(B)")
_r("binomial_dist", "library", library="scipy",
   function="scipy.stats.binom.pmf", pypi="scipy>=1.11")
_r("poisson_dist", "library", library="scipy",
   function="scipy.stats.poisson.pmf", pypi="scipy>=1.11")
_r("expected_value", "library", library="numpy",
   function="numpy.dot(values, probs)", pypi="numpy>=1.24")
_r("variance", "library", library="numpy",
   function="numpy.var", pypi="numpy>=1.24")
_r("std_dev", "library", library="numpy",
   function="numpy.std", pypi="numpy>=1.24")
_r("z_score", "library", library="scipy",
   function="scipy.stats.zscore", pypi="scipy>=1.11")
_r("linear_regression", "library", library="scipy",
   function="scipy.stats.linregress", pypi="scipy>=1.11")
_r("correlation", "library", library="numpy",
   function="numpy.corrcoef", pypi="numpy>=1.24")
_r("hypothesis_test", "library", library="scipy",
   function="scipy.stats.ttest_1samp", pypi="scipy>=1.11")
_r("confidence_interval", "library", library="scipy",
   function="scipy.stats.norm.interval", pypi="scipy>=1.11")
_r("chi_square_genetics", "library", library="scipy",
   function="scipy.stats.chisquare", pypi="scipy>=1.11")

# Physics -- tier 3-4
_r("kinematics_velocity", "formula", formula="v = v0 + a*t",
   notes="SUVAT equation")
_r("kinematics_s", "formula", formula="s = v0*t + 0.5*a*t^2",
   notes="SUVAT equation")
_r("kinetic_energy", "formula", formula="KE = 0.5*m*v^2",
   notes="Kinetic energy")
_r("potential_energy", "formula", formula="PE = m*g*h",
   notes="Gravitational PE")
_r("ohms_law", "formula", formula="V = I*R",
   notes="Ohm's law")
_r("ideal_gas", "formula", formula="PV = nRT",
   notes="Ideal gas law")
_r("gravitational_force", "formula",
   formula="F = G*m1*m2/r^2", notes="Newton's law of gravitation")
_r("escape_velocity", "formula",
   formula="v_esc = sqrt(2*G*M/r)", notes="Escape velocity")
_r("pendulum_period", "formula",
   formula="T = 2*pi*sqrt(L/g)", notes="Simple pendulum")

# Chemistry -- tier 3-4
_r("molar_mass", "reference", notes="Lookup atomic masses from periodic table")
_r("stoichiometry", "library", library="sympy",
   function="sympy.Matrix.nullspace", pypi="sympy>=1.12",
   notes="Balance equations via null space of stoichiometric matrix")
_r("molarity", "formula", formula="M = n/V",
   notes="Moles per litre")
_r("ph_calculation", "library", library="math",
   function="-math.log10(concentration)", pypi="(stdlib)")
_r("nernst_equation", "formula",
   formula="E = E0 - (RT/nF)*ln(Q)", notes="Electrochemical potential")
_r("gibbs_spontaneity", "formula",
   formula="dG = dH - T*dS", notes="Gibbs free energy")
_r("arrhenius", "formula",
   formula="k = A*exp(-Ea/(R*T))", notes="Arrhenius equation")
_r("equilibrium_constant", "formula",
   formula="K = products/reactants", notes="Law of mass action")
_r("beer_lambert", "formula",
   formula="A = epsilon*l*c", notes="Beer-Lambert law")
_r("rate_law", "formula",
   formula="rate = k*[A]^m*[B]^n", notes="Rate law")

# =========================================================================
# TIER 4-5 -- Advanced maths, physics, algorithms
# =========================================================================

# Linear algebra
_r("null_space", "library", library="numpy",
   function="scipy.linalg.null_space", pypi="scipy>=1.11")
_r("column_space", "library", library="numpy",
   function="numpy.linalg.qr", pypi="numpy>=1.24")
_r("rank_nullity", "library", library="numpy",
   function="numpy.linalg.matrix_rank", pypi="numpy>=1.24")
_r("svd_compute", "library", library="numpy",
   function="numpy.linalg.svd", pypi="numpy>=1.24")
_r("qr_decomposition", "library", library="numpy",
   function="numpy.linalg.qr", pypi="numpy>=1.24")
_r("cholesky_factor", "library", library="numpy",
   function="numpy.linalg.cholesky", pypi="numpy>=1.24")

# Number theory
_r("jacobi_symbol", "library", library="sympy",
   function="sympy.jacobi_symbol", pypi="sympy>=1.12")
_r("euler_criterion", "library", library="sympy",
   function="pow(a, (p-1)//2, p)", pypi="(stdlib)")
_r("legendre_symbol_compute", "library", library="sympy",
   function="sympy.legendre_symbol", pypi="sympy>=1.12")
_r("primitive_root", "library", library="sympy",
   function="sympy.primitive_root", pypi="sympy>=1.12")
_r("mobius_function", "library", library="sympy",
   function="sympy.mobius", pypi="sympy>=1.12")

# Graph algorithms
_r("bellman_ford", "library", library="networkx",
   function="networkx.bellman_ford_path_length", pypi="networkx>=3.0")
_r("floyd_warshall", "library", library="networkx",
   function="networkx.floyd_warshall", pypi="networkx>=3.0")
_r("articulation_point", "library", library="networkx",
   function="networkx.articulation_points", pypi="networkx>=3.0")
_r("strongly_connected", "library", library="networkx",
   function="networkx.strongly_connected_components",
   pypi="networkx>=3.0")
_r("minimum_spanning_tree", "library", library="networkx",
   function="networkx.minimum_spanning_tree", pypi="networkx>=3.0")
_r("graph_coloring", "library", library="networkx",
   function="networkx.greedy_color", pypi="networkx>=3.0")
_r("betweenness_centrality", "library", library="networkx",
   function="networkx.betweenness_centrality", pypi="networkx>=3.0")
_r("pagerank_compute", "library", library="networkx",
   function="networkx.pagerank", pypi="networkx>=3.0")

# Signal processing
_r("dft_compute", "library", library="numpy",
   function="numpy.fft.fft", pypi="numpy>=1.24")
_r("fir_filter", "library", library="scipy",
   function="scipy.signal.lfilter", pypi="scipy>=1.11")
_r("z_transform", "library", library="scipy",
   function="scipy.signal.tf2zpk", pypi="scipy>=1.11")

# Statistics
_r("anova_one_way", "library", library="scipy",
   function="scipy.stats.f_oneway", pypi="scipy>=1.11")
_r("chi_square_independence", "library", library="scipy",
   function="scipy.stats.chi2_contingency", pypi="scipy>=1.11")
_r("mann_whitney_u", "library", library="scipy",
   function="scipy.stats.mannwhitneyu", pypi="scipy>=1.11")
_r("kruskal_wallis", "library", library="scipy",
   function="scipy.stats.kruskal", pypi="scipy>=1.11")
_r("paired_t_test", "library", library="scipy",
   function="scipy.stats.ttest_rel", pypi="scipy>=1.11")

# Calculus (sympy)
_r("implicit_differentiation", "library", library="sympy",
   function="sympy.idiff", pypi="sympy>=1.12")
_r("integration_by_substitution", "library", library="sympy",
   function="sympy.integrate", pypi="sympy>=1.12")
_r("integration_trig_sub", "library", library="sympy",
   function="sympy.integrate", pypi="sympy>=1.12")
_r("double_integral", "library", library="sympy",
   function="sympy.integrate(f, (x,a,b), (y,c,d))", pypi="sympy>=1.12")
_r("triple_integral", "library", library="sympy",
   function="sympy.integrate(f, (x,..), (y,..), (z,..))",
   pypi="sympy>=1.12")
_r("laplacian", "library", library="sympy",
   function="sum(sympy.diff(f, v, 2) for v in vars)", pypi="sympy>=1.12")
_r("curl_compute", "library", library="sympy",
   function="sympy.vector.curl", pypi="sympy>=1.12")
_r("divergence_theorem", "library", library="sympy",
   function="sympy.vector.divergence", pypi="sympy>=1.12")

# Stochastic / probability
_r("negative_binomial", "library", library="scipy",
   function="scipy.stats.nbinom.pmf", pypi="scipy>=1.11")
_r("hypergeometric", "library", library="scipy",
   function="scipy.stats.hypergeom.pmf", pypi="scipy>=1.11")
_r("geometric_dist", "library", library="scipy",
   function="scipy.stats.geom.pmf", pypi="scipy>=1.11")
_r("weibull_distribution", "library", library="scipy",
   function="scipy.stats.weibull_min.pdf", pypi="scipy>=1.11")
_r("beta_distribution", "library", library="scipy",
   function="scipy.stats.beta.pdf", pypi="scipy>=1.11")

# Cryptography
_r("rsa_keygen", "library", library="sympy",
   function="sympy.nextprime, pow(e,-1,phi)", pypi="sympy>=1.12")
_r("rsa_encrypt", "library", library="math",
   function="pow(m, e, n)", pypi="(stdlib)")
_r("rsa_decrypt", "library", library="math",
   function="pow(c, d, n)", pypi="(stdlib)")
_r("diffie_hellman", "library", library="math",
   function="pow(g, a, p)", pypi="(stdlib)")

# Combinatorics
_r("catalan", "library", library="math",
   function="math.comb(2*n, n) // (n+1)", pypi="(stdlib)")
_r("derangement", "library", library="math",
   function="subfactorial formula", pypi="(stdlib)",
   formula="D(n) = n! * sum((-1)^k/k!, k=0..n)")
_r("stirling_second", "library", library="sympy",
   function="sympy.functions.combinatorial.numbers.stirling",
   pypi="sympy>=1.12")
_r("bell_number", "library", library="sympy",
   function="sympy.bell", pypi="sympy>=1.12")
_r("multinomial_coefficient", "library", library="math",
   function="math.factorial(n) / prod(math.factorial(k))",
   pypi="(stdlib)")

# Optimisation
_r("linear_program", "library", library="scipy",
   function="scipy.optimize.linprog", pypi="scipy>=1.11")
_r("convex_conjugate", "library", library="sympy",
   function="Legendre transform via sympy", pypi="sympy>=1.12")

# =========================================================================
# Physics formulas (no library, well-known)
# =========================================================================

# Electromagnetism
_r("coulombs_law", "formula", formula="F = k*q1*q2/r^2")
_r("electric_field", "formula", formula="E = k*Q/r^2")
_r("gauss_law", "formula", formula="Phi_E = Q_enc/epsilon_0")
_r("electric_potential", "formula", formula="V = k*Q/r")
_r("capacitance", "formula", formula="C = epsilon_0*A/d")
_r("magnetic_force", "formula", formula="F = q*v*B*sin(theta)")
_r("faraday_law", "formula", formula="emf = -d(Phi_B)/dt")
_r("inductance", "formula", formula="L = mu_0*N^2*A/l")

# Thermodynamics
_r("first_law_thermo", "formula", formula="dU = Q - W")
_r("carnot_efficiency", "formula", formula="eta = 1 - T_cold/T_hot")
_r("entropy_change", "formula", formula="dS = Q_rev/T")
_r("heat_capacity", "formula", formula="Q = m*c*dT")

# Relativity
_r("lorentz_factor", "formula", formula="gamma = 1/sqrt(1 - v^2/c^2)")
_r("time_dilation", "formula", formula="t = gamma * t0")
_r("length_contraction", "formula", formula="L = L0/gamma")
_r("relativistic_energy", "formula", formula="E = gamma*m*c^2")

# Fluid mechanics
_r("bernoulli", "formula",
   formula="P + 0.5*rho*v^2 + rho*g*h = const")
_r("reynolds_number", "formula", formula="Re = rho*v*L/mu")
_r("drag_force", "formula", formula="F_d = 0.5*C_d*rho*A*v^2")

# Quantum
_r("schrodinger_1d", "library", library="sympy",
   function="sympy.physics.quantum", pypi="sympy>=1.12",
   notes="Symbolic Schrodinger equation")
_r("uncertainty_compute", "formula",
   formula="dx*dp >= hbar/2")

# Astrophysics
_r("schwarzschild_radius", "formula", formula="r_s = 2*G*M/c^2")
_r("hubble_law", "formula", formula="v = H0*d")
_r("parallax_distance", "formula", formula="d = 1/p (parsecs)")
_r("stefan_boltzmann", "formula", formula="L = 4*pi*R^2*sigma*T^4")


# =========================================================================
# TIER 0 -- remaining
# =========================================================================

_r("counting", "library", library="math", function="math.comb/math.perm", pypi="(stdlib)")
_r("rounding", "library", library="builtins", function="round()", pypi="(stdlib)")
_r("unit_conversion_length", "formula", formula="val * factor")
_r("unit_conversion_mass", "formula", formula="val * factor")
_r("unit_conversion_temp", "formula", formula="C->F: 9/5*C+32, F->C: 5/9*(F-32)")
_r("set_intersection", "library", library="builtins", function="set.intersection", pypi="(stdlib)")
_r("set_membership", "library", library="builtins", function="in operator", pypi="(stdlib)")
_r("set_union", "library", library="builtins", function="set.union", pypi="(stdlib)")
_r("palindrome_check", "library", library="builtins", function="s == s[::-1]", pypi="(stdlib)")

# =========================================================================
# TIER 1 -- remaining
# =========================================================================

_r("roi", "formula", formula="(gain-cost)/cost * 100")
_r("simple_interest", "formula", formula="I = P*r*t")
_r("absolute_value", "library", library="builtins", function="abs()", pypi="(stdlib)")
_r("floor_ceil", "library", library="math", function="math.floor/math.ceil", pypi="(stdlib)")
_r("fraction_arithmetic", "library", library="fractions", function="fractions.Fraction", pypi="(stdlib)")
_r("percentage", "formula", formula="p/100 * base")
_r("sequence_next", "library", library="builtins", function="pattern extrapolation", pypi="(stdlib)")
_r("volume_box", "formula", formula="l*w*h")
_r("syllogism", "reference", notes="logical deduction rule lookup")
_r("scientific_notation", "library", library="builtins", function="float formatting", pypi="(stdlib)")
_r("significant_figures", "library", library="builtins", function="rounding", pypi="(stdlib)")
_r("time_arithmetic", "library", library="builtins", function="divmod(seconds, 60)", pypi="(stdlib)")
_r("arithmetic_sequence", "formula", formula="a_n = a_1 + (n-1)*d")
_r("set_cardinality", "library", library="builtins", function="len(set)", pypi="(stdlib)")
_r("set_difference", "library", library="builtins", function="set.difference", pypi="(stdlib)")
_r("set_subset", "library", library="builtins", function="set.issubset", pypi="(stdlib)")
_r("anagram_check", "library", library="builtins", function="sorted(a)==sorted(b)", pypi="(stdlib)")
_r("pattern_continue", "library", library="builtins", function="sequence extrapolation", pypi="(stdlib)")
_r("substring_find", "library", library="builtins", function="str.find", pypi="(stdlib)")
_r("angle_conversion", "library", library="math", function="math.radians/math.degrees", pypi="(stdlib)")
_r("sin_cos_eval", "library", library="math", function="math.sin/math.cos", pypi="(stdlib)")
_r("tan_eval", "library", library="math", function="math.tan", pypi="(stdlib)")

# =========================================================================
# TIER 2 -- remaining
# =========================================================================

_r("balancing_equation", "library", library="sympy", function="sympy.Matrix.nullspace", pypi="sympy>=1.12")
_r("combination_count", "library", library="math", function="math.comb", pypi="(stdlib)")
_r("permutation_with_rep", "library", library="math", function="n**r", pypi="(stdlib)")
_r("pigeonhole", "library", library="math", function="math.ceil(n/k)", pypi="(stdlib)")
_r("queue_operations", "library", library="builtins", function="list append/pop(0)", pypi="(stdlib)")
_r("stack_operations", "library", library="builtins", function="list append/pop", pypi="(stdlib)")
_r("break_even", "formula", formula="FC/(P-VC)")
_r("compound_interest", "formula", formula="P*(1+r/n)^(nt)")
_r("depreciation", "formula", formula="(cost-salvage)/life")
_r("arithmetic_mean", "library", library="statistics", function="statistics.mean", pypi="(stdlib)")
_r("prime_factorisation", "library", library="sympy", function="sympy.factorint", pypi="sympy>=1.12")
_r("square_root", "library", library="math", function="math.isqrt/math.sqrt", pypi="(stdlib)")
_r("weighted_sum", "library", library="numpy", function="numpy.dot", pypi="numpy>=1.24")
_r("angle_sum_triangle", "formula", formula="A+B+C=180")
_r("distance_2d", "library", library="math", function="math.dist", pypi="(stdlib)")
_r("midpoint", "formula", formula="((x1+x2)/2, (y1+y2)/2)")
_r("similar_triangles", "formula", formula="a1/a2 = b1/b2 = c1/c2")
_r("slope", "formula", formula="(y2-y1)/(x2-x1)")
_r("contrapositive", "reference", notes="logical equivalence rule")
_r("logical_equivalence", "reference", notes="truth table comparison")
_r("propositional_eval", "library", library="builtins", function="eval(bool expr)", pypi="(stdlib)")
_r("base_case_identify", "reference", notes="pattern recognition")
_r("recursive_trace", "library", library="builtins", function="simulate recursion", pypi="(stdlib)")
_r("recursive_sum", "library", library="builtins", function="sum(range(n+1))", pypi="(stdlib)")
_r("geometric_sequence", "formula", formula="a_n = a_1 * r^(n-1)")
_r("sequence_sum", "library", library="sympy", function="sympy.summation", pypi="sympy>=1.12")
_r("cartesian_product", "library", library="itertools", function="itertools.product", pypi="(stdlib)")
_r("power_set", "library", library="itertools", function="itertools.combinations", pypi="(stdlib)")
_r("venn_diagram_count", "formula", formula="|A union B| = |A|+|B|-|A intersect B|")
_r("bounding_box", "library", library="builtins", function="min/max", pypi="(stdlib)")
_r("basic_prob", "formula", formula="favorable/total")
_r("mean", "library", library="statistics", function="statistics.mean", pypi="(stdlib)")
_r("median", "library", library="statistics", function="statistics.median", pypi="(stdlib)")
_r("mode", "library", library="statistics", function="statistics.mode", pypi="(stdlib)")
_r("hamming_distance", "library", library="builtins", function="sum(a!=b for a,b in zip)", pypi="(stdlib)")
_r("string_encode_decode", "library", library="builtins", function="encode/decode", pypi="(stdlib)")
_r("law_of_cosines", "library", library="math", function="math.acos", pypi="(stdlib)", formula="c^2=a^2+b^2-2ab*cos(C)")
_r("law_of_sines", "library", library="math", function="math.asin", pypi="(stdlib)", formula="a/sin(A)=b/sin(B)")

# =========================================================================
# TIER 3 -- remaining
# =========================================================================

_r("base_conversion", "library", library="builtins", function="int(s,base)/format", pypi="(stdlib)")
_r("collatz", "library", library="builtins", function="iterative 3n+1", pypi="(stdlib)")
_r("cycle_detect", "library", library="builtins", function="Floyd's algorithm", pypi="(stdlib)")
_r("prefix_scan", "library", library="itertools", function="itertools.accumulate", pypi="(stdlib)")
_r("rpn", "library", library="builtins", function="stack-based eval", pypi="(stdlib)")
_r("binary_search_trace", "library", library="builtins", function="bisect", pypi="(stdlib)")
_r("counting_sort", "library", library="builtins", function="sorted()", pypi="(stdlib)")
_r("independence_test", "library", library="scipy", function="scipy.stats.chi2_contingency", pypi="scipy>=1.11")
_r("dfa_accept", "library", library="builtins", function="simulate DFA", pypi="(stdlib)")
_r("dfa_complement", "library", library="builtins", function="flip accept states", pypi="(stdlib)")
_r("dna_complement", "library", library="builtins", function="str.translate", pypi="(stdlib)")
_r("peptide_bond_count", "formula", formula="n_amino_acids - 1")
_r("genetic_code_redundancy", "reference", notes="codon table lookup")
_r("direct_proof", "reference", notes="logical deduction")
_r("membrane_transport", "reference", notes="biology classification")
_r("mitosis_phase", "reference", notes="biology classification")
_r("solubility_rules", "reference", notes="chemistry rules lookup")
_r("inclusion_exclusion", "library", library="builtins", function="set operations", pypi="(stdlib)")
_r("stars_and_bars", "library", library="math", function="math.comb(n+k-1, k-1)", pypi="(stdlib)")
_r("pascal_triangle", "library", library="math", function="math.comb(n,k)", pypi="(stdlib)")
_r("binary_arithmetic", "library", library="builtins", function="int(s,2)/bin()", pypi="(stdlib)")
_r("boolean_algebra", "library", library="builtins", function="eval(bool expr)", pypi="(stdlib)")
_r("logic_gate_eval", "library", library="builtins", function="and/or/not/xor", pypi="(stdlib)")
_r("binary_tree_traversal", "library", library="builtins", function="recursive traversal", pypi="(stdlib)")
_r("hash_table_ops", "library", library="builtins", function="dict operations", pypi="(stdlib)")
_r("heap_operations", "library", library="heapq", function="heapq.heappush/pop", pypi="(stdlib)")
_r("bst_insert", "library", library="builtins", function="BST insert algorithm", pypi="(stdlib)")
_r("present_value", "formula", formula="FV/(1+r)^n")
_r("dot_product", "library", library="numpy", function="numpy.dot", pypi="numpy>=1.24")
_r("matrix_add", "library", library="numpy", function="numpy.add", pypi="numpy>=1.24")
_r("matrix_scalar", "library", library="numpy", function="scalar * matrix", pypi="numpy>=1.24")
_r("product_notation", "library", library="math", function="math.prod", pypi="(stdlib)")
_r("summation", "library", library="builtins", function="sum()", pypi="(stdlib)")
_r("dominant_strategy", "library", library="builtins", function="argmax per row", pypi="(stdlib)")
_r("payoff_matrix", "library", library="builtins", function="matrix lookup", pypi="(stdlib)")
_r("prisoners_dilemma", "reference", notes="game theory payoff lookup")
_r("electron_config", "reference", notes="periodic table lookup")
_r("electronegativity_bond", "reference", notes="Pauling scale lookup")
_r("periodic_trend", "reference", notes="periodic table pattern")
_r("limiting_reagent", "library", library="sympy", function="stoichiometric ratio", pypi="sympy>=1.12")
_r("percent_composition", "formula", formula="(mass_element/molar_mass)*100")
_r("solution_dilution", "formula", formula="M1*V1=M2*V2")
_r("blood_type", "reference", notes="genetics lookup table")
_r("punnett_square", "library", library="itertools", function="itertools.product(alleles)", pypi="(stdlib)")
_r("mohs_hardness", "reference", notes="mineral hardness lookup")
_r("mineral_identification", "reference", notes="mineral properties lookup")
_r("rock_cycle", "reference", notes="geological process classification")
_r("circle_arc_length", "formula", formula="r*theta")
_r("line_intersection", "library", library="numpy", function="numpy.linalg.solve", pypi="numpy>=1.24")
_r("polygon_area", "library", library="builtins", function="shoelace formula", pypi="(stdlib)")
_r("sector_area", "formula", formula="0.5*r^2*theta")
_r("distance_point_line", "formula", formula="|ax+by+c|/sqrt(a^2+b^2)")
_r("triangle_centroid", "formula", formula="((x1+x2+x3)/3, (y1+y2+y3)/3)")
_r("vector_projection_2d", "library", library="numpy", function="numpy.dot(a,b)/numpy.dot(b,b)*b", pypi="numpy>=1.24")
_r("bfs_order", "library", library="networkx", function="networkx.bfs_tree", pypi="networkx>=3.0")
_r("connected_components", "library", library="networkx", function="networkx.connected_components", pypi="networkx>=3.0")
_r("dfs_order", "library", library="networkx", function="networkx.dfs_tree", pypi="networkx>=3.0")
_r("morpheme_parse", "reference", notes="linguistics lookup")
_r("syllable_count", "library", library="builtins", function="vowel counting heuristic", pypi="(stdlib)")
_r("deduction_chain", "reference", notes="logical inference")
_r("quantifier_eval", "library", library="builtins", function="all()/any()", pypi="(stdlib)")
_r("significant_figures_calc", "library", library="builtins", function="rounding", pypi="(stdlib)")
_r("embedding_lookup", "library", library="numpy", function="matrix[index]", pypi="numpy>=1.24")
_r("interval_identify", "reference", notes="music theory lookup")
_r("rhythm_subdivision", "formula", formula="beat division")
_r("digit_sum_divisibility", "library", library="builtins", function="sum(int(d) for d in str(n))", pypi="(stdlib)")
_r("bisection_method", "library", library="scipy", function="scipy.optimize.brentq", pypi="scipy>=1.11")
_r("numerical_derivative", "library", library="scipy", function="scipy.misc.derivative", pypi="scipy>=1.11")
_r("trapezoidal_rule", "library", library="scipy", function="scipy.integrate.trapezoid", pypi="scipy>=1.11")
_r("set_operations", "library", library="builtins", function="set union/intersection/diff", pypi="(stdlib)")
_r("call_stack_depth", "library", library="builtins", function="recursive count", pypi="(stdlib)")
_r("memoisation", "library", library="functools", function="functools.lru_cache", pypi="(stdlib)")
_r("recursive_gcd", "library", library="math", function="math.gcd", pypi="(stdlib)")
_r("recursive_power", "library", library="builtins", function="pow()", pypi="(stdlib)")
_r("tower_of_hanoi", "library", library="builtins", function="2^n - 1 moves", pypi="(stdlib)")
_r("convergent_series", "library", library="sympy", function="sympy.Sum.doit()", pypi="sympy>=1.12")
_r("recurrence_linear", "library", library="sympy", function="sympy.rsolve", pypi="sympy>=1.12")
_r("point_in_polygon", "library", library="builtins", function="ray casting", pypi="(stdlib)")
_r("conditional_prob", "formula", formula="P(A|B) = P(A and B)/P(B)")
_r("regex_match", "library", library="re", function="re.match", pypi="(stdlib)")
_r("trig_identity", "library", library="sympy", function="sympy.trigsimp", pypi="sympy>=1.12")

# =========================================================================
# TIER 4 -- remaining (bulk)
# =========================================================================

# Algebra & number theory
_r("permutation_cycle", "library", library="sympy", function="sympy.combinatorics.Permutation", pypi="sympy>=1.12")
_r("number_base_arithmetic", "library", library="builtins", function="int(s,base)", pypi="(stdlib)")
_r("fibonacci_mod", "library", library="builtins", function="iterative fib % m", pypi="(stdlib)")
_r("compositions", "library", library="math", function="math.comb(n-1,k-1)", pypi="(stdlib)")
_r("double_counting", "library", library="math", function="combinatorial identity", pypi="(stdlib)")
_r("fibonacci_identity", "library", library="builtins", function="verify F(m+n)=F(m)*F(n+1)+F(m-1)*F(n)", pypi="(stdlib)")
_r("pigeonhole_application", "library", library="math", function="math.ceil", pypi="(stdlib)")
_r("vandermonde_identity", "library", library="math", function="math.comb", pypi="(stdlib)")
_r("principle_inclusion_exclusion", "library", library="builtins", function="set operations", pypi="(stdlib)")

# Economics & finance
_r("comparative_advantage", "formula", formula="opportunity cost comparison")
_r("elasticity", "formula", formula="(%dQ/%dP)")
_r("supply_demand_equilibrium", "library", library="sympy", function="sympy.solve", pypi="sympy>=1.12")
_r("option_payoff", "formula", formula="max(S-K,0) for call")
_r("portfolio_return", "formula", formula="sum(w_i * r_i)")
_r("present_value_annuity", "formula", formula="PMT*(1-(1+r)^-n)/r")
_r("exchange_rate", "formula", formula="amount * rate")
_r("inflation_real_rate", "formula", formula="(1+nom)/(1+inf)-1")
_r("marginal_analysis", "library", library="sympy", function="sympy.diff", pypi="sympy>=1.12")
_r("multiplier_effect", "formula", formula="1/(1-MPC)")
_r("time_value_money", "formula", formula="PV*(1+r)^n")
_r("phillips_curve", "formula", formula="inflation vs unemployment tradeoff")

# ML & AI
_r("confusion_matrix", "library", library="builtins", function="TP/FP/TN/FN counts", pypi="(stdlib)")
_r("conv_output_size", "formula", formula="(W-K+2P)/S+1")
_r("gradient_descent", "formula", formula="w = w - lr*grad")
_r("lr_decay", "formula", formula="lr = lr0 * gamma^(t/step)")
_r("mse_loss", "library", library="numpy", function="numpy.mean((y-yhat)**2)", pypi="numpy>=1.24")
_r("dropout_forward", "library", library="numpy", function="mask * x / (1-p)", pypi="numpy>=1.24")
_r("learning_rate_warmup", "formula", formula="lr * min(1, step/warmup)")
_r("maxpool_forward", "library", library="numpy", function="numpy.max over windows", pypi="numpy>=1.24")
_r("relu_derivative", "library", library="numpy", function="numpy.where(x>0, 1, 0)", pypi="numpy>=1.24")
_r("cosine_lr_schedule", "library", library="math", function="lr_min+(lr_max-lr_min)*(1+cos(pi*t/T))/2", pypi="(stdlib)")
_r("gradient_accumulation", "formula", formula="sum(grads)/n_accum")

# Algorithms & data structures
_r("interval_scheduling", "library", library="builtins", function="greedy sort by end", pypi="(stdlib)")
_r("longest_palindrome", "library", library="builtins", function="expand around center", pypi="(stdlib)")
_r("topk_quickselect", "library", library="builtins", function="quickselect", pypi="(stdlib)")
_r("hash_chaining", "library", library="builtins", function="hash % size", pypi="(stdlib)")
_r("heap_sort_trace", "library", library="heapq", function="heapq", pypi="(stdlib)")
_r("merge_sort_trace", "library", library="builtins", function="merge sort", pypi="(stdlib)")
_r("quicksort_partition", "library", library="builtins", function="partition around pivot", pypi="(stdlib)")
_r("radix_sort", "library", library="builtins", function="digit-by-digit sort", pypi="(stdlib)")
_r("bloom_filter", "formula", formula="FP rate = (1-e^(-kn/m))^k")
_r("bst_delete", "library", library="builtins", function="BST delete algorithm", pypi="(stdlib)")
_r("trie_operations", "library", library="builtins", function="trie insert/search", pypi="(stdlib)")

# Physics
_r("projectile_motion", "formula", formula="x=v0*cos(t)*t, y=v0*sin(t)*t-0.5*g*t^2")
_r("circular_motion", "formula", formula="F=mv^2/r")
_r("inelastic_collision", "formula", formula="m1*v1+m2*v2=(m1+m2)*vf")
_r("spring_oscillation", "formula", formula="T=2*pi*sqrt(m/k)")
_r("conservation_energy", "formula", formula="KE+PE=const")
_r("kinematics_displacement", "formula", formula="s=v0*t+0.5*a*t^2")
_r("momentum", "formula", formula="p=m*v")
_r("wave_equation", "formula", formula="v=f*lambda")
_r("parallel_plate_field", "formula", formula="E=sigma/epsilon_0")
_r("capacitor_energy", "formula", formula="U=0.5*C*V^2")

# Chemistry
_r("ionic_strength", "formula", formula="I=0.5*sum(c_i*z_i^2)")
_r("calorimetry", "formula", formula="q=m*c*dT")
_r("enthalpy_reaction", "formula", formula="dH=sum(dHf_products)-sum(dHf_reactants)")
_r("gas_effusion", "formula", formula="rate1/rate2=sqrt(M2/M1)")
_r("ideal_gas_mixture", "formula", formula="P_total=sum(P_i)")
_r("oxidation_number_change", "reference", notes="oxidation rules")
_r("dalton_partial_pressure", "formula", formula="P_i=x_i*P_total")
_r("empirical_formula", "library", library="math", function="divide by min, round", pypi="(stdlib)")
_r("gas_law_combined", "formula", formula="P1V1/T1=P2V2/T2")
_r("hybridisation", "reference", notes="VSEPR rules")
_r("lewis_structure", "reference", notes="electron counting rules")
_r("oxidation_state", "reference", notes="oxidation rules")
_r("vsepr_geometry", "reference", notes="electron pair geometry lookup")

# Biology
_r("dna_replication_fork", "reference", notes="biology process")
_r("immune_response", "reference", notes="biology classification")
_r("protein_structure", "reference", notes="biology classification")
_r("transcription_process", "reference", notes="biology process")
_r("translation_elongation", "reference", notes="biology process")
_r("codon_translate", "reference", notes="codon table lookup")
_r("protein_mass", "library", library="builtins", function="sum(amino_acid_masses)", pypi="(stdlib)")
_r("gc_content", "library", library="builtins", function="(G+C)/len(seq)", pypi="(stdlib)")
_r("restriction_digest", "library", library="builtins", function="string find + split", pypi="(stdlib)")
_r("atp_yield", "formula", formula="substrate level + oxidative phosphorylation")
_r("cell_cycle_duration", "formula", formula="sum(phase_durations)")
_r("meiosis_gametes", "library", library="itertools", function="itertools.product", pypi="(stdlib)")
_r("osmolarity", "formula", formula="n*C*phi")
_r("number_needed_treat", "formula", formula="1/ARR")
_r("sensitivity_specificity", "formula", formula="TP/(TP+FN), TN/(TN+FP)")
_r("apoptosis_pathway", "reference", notes="biology process")
_r("cell_cycle_checkpoint", "reference", notes="biology classification")
_r("pcr_amplification", "formula", formula="N=N0*2^n")
_r("logistic_growth", "formula", formula="dN/dt=rN(1-N/K)")
_r("trophic_efficiency", "formula", formula="energy_out/energy_in*100")
_r("herd_immunity", "formula", formula="1-1/R0")
_r("incidence_rate", "formula", formula="new_cases/population*time")
_r("relative_risk", "formula", formula="(a/(a+b))/(c/(c+d))")

# Optics & waves
_r("snells_law", "library", library="math", function="n1*sin(t1)=n2*sin(t2)", pypi="(stdlib)")
_r("thin_lens", "formula", formula="1/f=1/do+1/di")
_r("magnification", "formula", formula="M=-di/do")
_r("mirror_equation", "formula", formula="1/f=1/do+1/di")
_r("optical_path_length", "formula", formula="n*d")
_r("polarization", "formula", formula="I=I0*cos^2(theta)")
_r("abbe_diffraction_limit", "formula", formula="d=lambda/(2*NA)")
_r("photon_energy", "formula", formula="E=h*f=hc/lambda")
_r("total_internal_reflection", "formula", formula="theta_c=arcsin(n2/n1)")

# Fluids
_r("buoyancy", "formula", formula="F_b=rho*g*V")
_r("continuity_equation", "formula", formula="A1*v1=A2*v2")
_r("froude_number", "formula", formula="Fr=v/sqrt(g*h)")
_r("orifice_flow", "formula", formula="Q=Cd*A*sqrt(2*g*h)")
_r("weir_flow", "formula", formula="Q=Cd*L*H^(3/2)")
_r("pump_power", "formula", formula="P=rho*g*Q*H/eta")
_r("stokes_drag", "formula", formula="F=6*pi*mu*r*v")

# Thermo
_r("heat_pump", "formula", formula="COP=Q_h/W")
_r("gibbs_phase_rule", "formula", formula="F=C-P+2")
_r("refrigeration_cop", "formula", formula="COP=Q_c/W")

# Materials & engineering
_r("stress_strain", "formula", formula="sigma=F/A, epsilon=dL/L")
_r("thermal_expansion", "formula", formula="dL=alpha*L*dT")
_r("youngs_modulus", "formula", formula="E=sigma/epsilon")
_r("composite_rule_mixtures", "formula", formula="E_c=V_f*E_f+V_m*E_m")
_r("corrosion_rate", "formula", formula="CR=K*W/(A*t*rho)")
_r("hardness_test", "reference", notes="hardness scale lookup")
_r("heat_treatment", "reference", notes="materials process")
_r("moment_of_inertia", "library", library="sympy", function="sympy.integrate(r^2*dm)", pypi="sympy>=1.12")
_r("section_modulus", "formula", formula="S=I/c")
_r("friction_force", "formula", formula="f=mu*N")
_r("fourier_conduction", "formula", formula="q=-k*A*dT/dx")
_r("newton_cooling", "formula", formula="q=h*A*(T_s-T_inf)")
_r("thermal_resistance", "formula", formula="R=L/(k*A)")
_r("reliability_series_parallel", "formula", formula="R_s=prod(R_i), R_p=1-prod(1-R_i)")

# Geology & earth science
_r("seismic_velocity", "formula", formula="v=d/t")
_r("geologic_time", "reference", notes="stratigraphy lookup")
_r("porosity_permeability", "formula", formula="phi=V_void/V_total")
_r("stratigraphy", "reference", notes="geology classification")
_r("magnetic_declination", "reference", notes="geophysics lookup")
_r("plate_velocity", "formula", formula="v=d/t")
_r("albedo_energy", "formula", formula="absorbed=(1-albedo)*incoming")
_r("carbon_budget", "formula", formula="emissions-removals")
_r("ocean_wave_speed", "formula", formula="c=sqrt(g*d) or c=g*T/(2*pi)")
_r("tidal_range", "formula", formula="high-low")

# Geometry ext
_r("area_polygon_shoelace", "library", library="builtins", function="shoelace", pypi="(stdlib)")
_r("line_circle_intersection", "library", library="sympy", function="sympy.solve", pypi="sympy>=1.12")
_r("parametric_line_3d", "library", library="numpy", function="parametric evaluation", pypi="numpy>=1.24")
_r("reflection_line", "library", library="numpy", function="reflection matrix", pypi="numpy>=1.24")
_r("rotation_2d", "library", library="math", function="math.cos/sin rotation", pypi="(stdlib)")
_r("triangle_circumcenter", "library", library="numpy", function="numpy.linalg.solve", pypi="numpy>=1.24")
_r("coordinate_rotation", "library", library="math", function="cos/sin matrix", pypi="(stdlib)")
_r("reflection_2d", "library", library="numpy", function="reflection matrix", pypi="numpy>=1.24")
_r("volume_cylinder", "formula", formula="pi*r^2*h")
_r("volume_sphere", "formula", formula="4/3*pi*r^3")

# Graphs ext
_r("bipartite_check", "library", library="networkx", function="networkx.is_bipartite", pypi="networkx>=3.0")
_r("graph_coloring_greedy", "library", library="networkx", function="networkx.greedy_color", pypi="networkx>=3.0")

# Spatial
_r("convex_hull_check", "library", library="scipy", function="scipy.spatial.ConvexHull", pypi="scipy>=1.11")
_r("line_segment_intersection", "library", library="builtins", function="cross product test", pypi="(stdlib)")
_r("point_in_triangle", "library", library="builtins", function="barycentric coords", pypi="(stdlib)")
_r("polygon_centroid", "formula", formula="(sum(x)/n, sum(y)/n)")

# Automata & formal languages
_r("nfa_simulate", "library", library="builtins", function="state set simulation", pypi="(stdlib)")
_r("turing_machine_step", "library", library="builtins", function="transition function", pypi="(stdlib)")
_r("dfa_product", "library", library="builtins", function="state pair construction", pypi="(stdlib)")
_r("language_operations", "library", library="builtins", function="set operations", pypi="(stdlib)")
_r("regex_to_dfa_direct", "library", library="re", function="re.compile", pypi="(stdlib)")
_r("state_equivalence", "library", library="builtins", function="partition refinement", pypi="(stdlib)")
_r("mealy_machine", "library", library="builtins", function="transition+output", pypi="(stdlib)")
_r("moore_machine", "library", library="builtins", function="transition+output", pypi="(stdlib)")

# Logic
_r("knights_knaves", "library", library="builtins", function="brute force truth assignment", pypi="(stdlib)")
_r("logical_puzzle", "library", library="itertools", function="itertools.permutations + constraint check", pypi="(stdlib)")

# Networking & systems
_r("network_delay", "formula", formula="propagation+transmission+queuing")
_r("routing_table", "reference", notes="next-hop lookup")
_r("arp_resolution", "reference", notes="protocol process")
_r("checksum_compute", "library", library="builtins", function="ones complement sum", pypi="(stdlib)")
_r("dns_resolution", "reference", notes="protocol process")
_r("ip_subnetting", "library", library="builtins", function="bitwise AND", pypi="(stdlib)")
_r("dhcp_process", "reference", notes="protocol process")
_r("load_balancing", "formula", formula="round robin / weighted")
_r("nat_translation", "reference", notes="protocol process")
_r("tcp_handshake", "reference", notes="protocol process")
_r("page_replacement", "library", library="builtins", function="FIFO/LRU simulation", pypi="(stdlib)")
_r("relational_algebra", "library", library="builtins", function="set operations on tuples", pypi="(stdlib)")
_r("scheduling_algorithm", "library", library="builtins", function="FCFS/SJF simulation", pypi="(stdlib)")
_r("subnet_calculate", "library", library="builtins", function="bitwise operations", pypi="(stdlib)")

# OS & compilers
_r("disk_scheduling", "library", library="builtins", function="SCAN/SSTF simulation", pypi="(stdlib)")
_r("file_allocation", "library", library="builtins", function="block allocation", pypi="(stdlib)")
_r("memory_allocation", "library", library="builtins", function="first-fit/best-fit", pypi="(stdlib)")
_r("page_table_lookup", "library", library="builtins", function="address translation", pypi="(stdlib)")
_r("process_scheduling_sjf", "library", library="builtins", function="sort by burst time", pypi="(stdlib)")
_r("virtual_memory_replacement", "library", library="builtins", function="LRU/FIFO", pypi="(stdlib)")
_r("tokenize", "library", library="builtins", function="lexer rules", pypi="(stdlib)")
_r("constant_folding", "library", library="builtins", function="eval constant exprs", pypi="(stdlib)")
_r("dead_code_elimination", "library", library="builtins", function="reachability analysis", pypi="(stdlib)")
_r("strength_reduction", "library", library="builtins", function="replace mul with shift", pypi="(stdlib)")

# Computer architecture
_r("amdahl_speedup", "formula", formula="1/((1-p)+p/s)")
_r("cache_hit_ratio", "formula", formula="hits/accesses")
_r("memory_hierarchy", "reference", notes="latency lookup table")
_r("pipeline_throughput", "formula", formula="n/(k+n-1) * 1/cycle_time")

# Digital electronics
_r("adder_circuit", "library", library="builtins", function="binary addition", pypi="(stdlib)")
_r("flip_flop_state", "library", library="builtins", function="state transition", pypi="(stdlib)")
_r("karnaugh_map", "library", library="builtins", function="minterm grouping", pypi="(stdlib)")
_r("multiplexer", "library", library="builtins", function="select line indexing", pypi="(stdlib)")

# Misc tier 4
_r("cross_product", "library", library="numpy", function="numpy.cross", pypi="numpy>=1.24")
_r("matrix_trace", "library", library="numpy", function="numpy.trace", pypi="numpy>=1.24")
_r("matrix_transpose", "library", library="numpy", function="numpy.transpose", pypi="numpy>=1.24")
_r("vector_norm", "library", library="numpy", function="numpy.linalg.norm", pypi="numpy>=1.24")
_r("cross_product_triple", "library", library="numpy", function="numpy.dot(a, numpy.cross(b,c))", pypi="numpy>=1.24")
_r("perfect_number_check", "library", library="sympy", function="sympy.divisor_sigma", pypi="sympy>=1.12")
_r("inventory_eoq", "formula", formula="sqrt(2*D*S/H)")
_r("simulation_lcg", "formula", formula="x_n+1 = (a*x_n+c) mod m")
_r("weber_fraction", "formula", formula="dI/I = k")
_r("knapsack_fractional", "library", library="builtins", function="greedy by value/weight", pypi="(stdlib)")
_r("am_modulation", "formula", formula="s(t)=(1+m*cos(2pi*fm*t))*cos(2pi*fc*t)")
_r("quantization", "formula", formula="step_size = (max-min)/levels")
_r("frequency_analysis", "library", library="builtins", function="Counter(text)", pypi="(stdlib)")
_r("hash_chain", "library", library="hashlib", function="hashlib.sha256", pypi="(stdlib)")
_r("otp_encrypt", "library", library="builtins", function="xor", pypi="(stdlib)")
_r("twos_complement", "library", library="builtins", function="bitwise complement", pypi="(stdlib)")
_r("replication_factor", "formula", formula="copies = RF * shards")
_r("nutrient_cycling", "formula", formula="input-output=storage")
_r("succession_model", "reference", notes="ecology process")
_r("air_quality_index", "formula", formula="linear interpolation from breakpoints")
_r("carbon_footprint", "formula", formula="activity * emission_factor")
_r("dilution_factor", "formula", formula="C1*V1=C2*V2")

# Remaining reference/formula tier 4
_r("conditional_independence", "formula", formula="P(A,B|C)=P(A|C)*P(B|C)")
_r("group_table", "library", library="builtins", function="Cayley table construction", pypi="(stdlib)")
_r("proof_by_cases", "reference", notes="logical proof structure")
_r("proof_by_contradiction", "reference", notes="logical proof structure")
_r("separation_of_variables", "library", library="sympy", function="sympy.dsolve", pypi="sympy>=1.12")
_r("hr_diagram", "reference", notes="stellar classification lookup")
_r("drake_equation", "formula", formula="N=R*fp*ne*fl*fi*fc*L")
_r("angular_diameter", "formula", formula="delta=2*arctan(d/(2*D))")
_r("hubble_time", "formula", formula="t=1/H0")
_r("stellar_classification", "reference", notes="spectral type lookup")
_r("led_wavelength", "formula", formula="lambda=hc/E_g")
_r("degree_polymerisation", "formula", formula="DP=M_n/M_0")
_r("glass_transition", "reference", notes="materials property lookup")
_r("generator_frequency", "formula", formula="f=N*P/(120)")
_r("transformer_ratio", "formula", formula="V1/V2=N1/N2")
_r("transmission_loss", "formula", formula="P_loss=I^2*R")
_r("uniform_continuous", "library", library="scipy", function="scipy.stats.uniform", pypi="scipy>=1.11")
_r("complex_arithmetic", "library", library="cmath", function="complex operations", pypi="(stdlib)")
_r("complex_modulus", "library", library="builtins", function="abs(complex)", pypi="(stdlib)")
_r("littles_law", "formula", formula="L=lambda*W")
_r("recursive_binary_search", "library", library="builtins", function="bisect", pypi="(stdlib)")
_r("recursive_permutations", "library", library="itertools", function="itertools.permutations", pypi="(stdlib)")
_r("odometry", "formula", formula="x+=v*cos(theta)*dt, y+=v*sin(theta)*dt")
_r("dielectric_constant", "formula", formula="C=eps_r*eps_0*A/d")
_r("fibonacci_properties", "library", library="builtins", function="iterative fib", pypi="(stdlib)")
_r("harmonic_series", "library", library="builtins", function="sum(1/k for k in range(1,n+1))", pypi="(stdlib)")
_r("sequence_limit", "library", library="sympy", function="sympy.limit", pypi="sympy>=1.12")
_r("telescoping_series", "library", library="sympy", function="sympy.Sum", pypi="sympy>=1.12")
_r("signal_energy_power", "library", library="numpy", function="numpy.sum(x**2)", pypi="numpy>=1.24")
_r("miller_indices", "reference", notes="crystallography lookup")
_r("hounsfield_unit", "formula", formula="HU=1000*(mu-mu_water)/(mu_water-mu_air)")
_r("snr_calculation", "formula", formula="SNR=signal/noise")
_r("mass_spec_molecular_ion", "reference", notes="spectroscopy lookup")
_r("effect_size", "formula", formula="d=(M1-M2)/s_pooled")
_r("exponential_smoothing", "formula", formula="s_t=alpha*x_t+(1-alpha)*s_{t-1}")
_r("moving_average", "library", library="numpy", function="numpy.convolve", pypi="numpy>=1.24")
_r("accuracy_precision", "formula", formula="accuracy=correct/total, precision=TP/(TP+FP)")
_r("dimensional_analysis_compute", "library", library="builtins", function="unit conversion chain", pypi="(stdlib)")
_r("coordination_number", "reference", notes="crystal structure lookup")
_r("ionic_radius_ratio", "formula", formula="r_cation/r_anion")
_r("nomenclature_complex", "reference", notes="IUPAC naming rules")
_r("iupac_naming", "reference", notes="IUPAC naming rules")
_r("functional_group_id", "reference", notes="organic chemistry lookup")
_r("degree_unsaturation", "formula", formula="DoU=(2C+2+N-H-X)/2")
_r("dihybrid_cross", "library", library="itertools", function="itertools.product(alleles)", pypi="(stdlib)")
_r("hardy_weinberg", "formula", formula="p^2+2pq+q^2=1")
_r("linked_genes", "formula", formula="recombination frequency")
_r("phonetic_features", "reference", notes="phonetics lookup")
_r("syntax_tree", "reference", notes="linguistics parse rules")
_r("edit_distance_linguistic", "library", library="builtins", function="DP Levenshtein", pypi="(stdlib)")
_r("ipa_transcription", "reference", notes="phonetics lookup")
_r("morphological_analysis", "reference", notes="morphology rules")
_r("word_frequency", "library", library="builtins", function="Counter", pypi="(stdlib)")
_r("coin_change", "library", library="builtins", function="DP algorithm", pypi="(stdlib)")
_r("derivative_eval", "library", library="sympy", function="sympy.diff then subs", pypi="sympy>=1.12")
_r("partial_derivative", "library", library="sympy", function="sympy.diff(f, x)", pypi="sympy>=1.12")
_r("big_o", "reference", notes="complexity classification")
_r("total_probability", "formula", formula="P(A)=sum(P(A|Bi)*P(Bi))")
_r("variance_dist", "library", library="numpy", function="numpy.var", pypi="numpy>=1.24")
_r("minimax", "library", library="builtins", function="recursive minimax", pypi="(stdlib)")
_r("nash_equilibrium", "library", library="builtins", function="best response check", pypi="(stdlib)")
_r("battle_of_sexes", "reference", notes="game theory payoff lookup")
_r("chicken_game", "reference", notes="game theory payoff lookup")
_r("pareto_efficiency", "library", library="builtins", function="dominance check", pypi="(stdlib)")
_r("zero_sum_game", "library", library="scipy", function="scipy.optimize.linprog", pypi="scipy>=1.11")
_r("euler_method_ode", "library", library="scipy", function="scipy.integrate.solve_ivp", pypi="scipy>=1.11")
_r("therapeutic_index", "formula", formula="TI=TD50/ED50")
_r("inverse_trig", "library", library="math", function="math.asin/acos/atan", pypi="(stdlib)")
_r("double_angle", "library", library="math", function="sin(2x)=2sin(x)cos(x)", pypi="(stdlib)")
_r("trig_equation", "library", library="sympy", function="sympy.solve", pypi="sympy>=1.12")
_r("chord_construct", "reference", notes="music theory interval rules")
_r("frequency_ratio", "formula", formula="f2/f1 = 2^(semitones/12)")
_r("spike_rate", "formula", formula="spikes/time_window")
_r("membership_function", "formula", formula="mu(x) piecewise linear")
_r("fuzzy_operations", "library", library="builtins", function="min/max for AND/OR", pypi="(stdlib)")

# =========================================================================
# Helper functions
# =========================================================================

def get_verification(task_name: str) -> VerificationEntry | None:
    """Look up the verification entry for a task.

    Args:
        task_name: Generator task identifier.

    Returns:
        VerificationEntry or None if not registered.
    """
    return VERIFICATION_REGISTRY.get(task_name)


def get_all_library_verifiable() -> list[VerificationEntry]:
    """Return all generators that can be verified by a library.

    Returns:
        List of entries with method='library'.
    """
    return [e for e in VERIFICATION_REGISTRY.values()
            if e.method == "library"]


def get_required_packages() -> set[str]:
    """Return all PyPI packages needed for library verification.

    Returns:
        Set of PyPI install targets.
    """
    packages = set()
    for entry in VERIFICATION_REGISTRY.values():
        if entry.pypi and entry.pypi != "(stdlib)":
            packages.add(entry.pypi)
    return packages


def coverage_report() -> dict:
    """Generate a coverage report.

    Returns:
        Dict with counts by method and list of unregistered generators.
    """
    from engram_generator.curriculum.registry import get_all_generators

    all_tasks = {g.task_name for g in get_all_generators()}
    registered = set(VERIFICATION_REGISTRY.keys())
    unregistered = all_tasks - registered

    by_method: dict[str, int] = {}
    for entry in VERIFICATION_REGISTRY.values():
        by_method[entry.method] = by_method.get(entry.method, 0) + 1

    return {
        "total_generators": len(all_tasks),
        "registered": len(registered),
        "unregistered": len(unregistered),
        "by_method": by_method,
        "unregistered_tasks": sorted(unregistered),
        "required_packages": sorted(get_required_packages()),
    }
