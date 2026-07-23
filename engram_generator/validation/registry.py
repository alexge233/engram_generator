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
_r("kinetic_energy", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="KE = 0.5*m*v^2",
   notes="Kinetic energy")
_r("potential_energy", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="PE = m*g*h",
   notes="Gravitational PE")
_r("ohms_law", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="V = I*R",
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
_r("arrhenius", "library", library="math", function="independent recomputation", pypi="(stdlib)",
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
_r("coulombs_law", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="F = k*q1*q2/r^2")
_r("electric_field", "formula", formula="E = k*Q/r^2")
_r("gauss_law", "formula", formula="Phi_E = Q_enc/epsilon_0")
_r("electric_potential", "formula", formula="V = k*Q/r")
_r("capacitance", "formula", formula="C = epsilon_0*A/d")
_r("magnetic_force", "formula", formula="F = q*v*B*sin(theta)")
_r("faraday_law", "formula", formula="emf = -d(Phi_B)/dt")
_r("inductance", "formula", formula="L = mu_0*N^2*A/l")

# Thermodynamics
_r("first_law_thermo", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="dU = Q - W")
_r("carnot_efficiency", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="eta = 1 - T_cold/T_hot")
_r("entropy_change", "formula", formula="dS = Q_rev/T")
_r("heat_capacity", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="Q = m*c*dT")

# Relativity
_r("lorentz_factor", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="gamma = 1/sqrt(1 - v^2/c^2)")
_r("time_dilation", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="t = gamma * t0")
_r("length_contraction", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="L = L0/gamma")
_r("relativistic_energy", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="E = gamma*m*c^2")

# Fluid mechanics
_r("bernoulli", "library", library="math", function="independent recomputation", pypi="(stdlib)",
   formula="P + 0.5*rho*v^2 + rho*g*h = const")
_r("reynolds_number", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="Re = rho*v*L/mu")
_r("drag_force", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="F_d = 0.5*C_d*rho*A*v^2")

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
_r("compound_interest", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="P*(1+r/n)^(nt)")
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
_r("momentum", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="p=m*v")
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
_r("thin_lens", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="1/f=1/do+1/di")
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
# TIER 5 -- Remaining (science, engineering, algorithms, ML)
# =========================================================================

# -- Tier 5: Abstract algebra
_r("group_axiom_check", "library", library="sympy", function="sympy.combinatorics.PermutationGroup",
   pypi="sympy>=1.12", notes="verify closure/identity/inverse/associativity")
_r("subgroup_test", "library", library="sympy", function="sympy.combinatorics.PermutationGroup",
   pypi="sympy>=1.12", notes="subgroup membership test")
_r("coset_enumerate", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12", notes="left/right coset enumeration")
_r("lagrange_verify", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12", notes="|H| divides |G|")
_r("symmetric_group", "library", library="sympy", function="sympy.combinatorics.SymmetricGroup",
   pypi="sympy>=1.12")
_r("dihedral_group", "library", library="sympy", function="sympy.combinatorics.DihedralGroup",
   pypi="sympy>=1.12")
_r("group_center", "library", library="sympy", function="sympy.combinatorics.PermutationGroup.center",
   pypi="sympy>=1.12")
_r("polynomial_ring", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12", notes="polynomial ring arithmetic")
_r("direct_product_group", "library", library="sympy", function="sympy.combinatorics.DirectProduct",
   pypi="sympy>=1.12")

# -- Tier 5: Actuarial science
_r("annuity_pv", "formula", formula="PV = PMT * (1 - (1+r)^-n) / r")
_r("insurance_premium", "formula", formula="P = PV(benefits) / PV(premiums)")
_r("life_table_actuarial", "formula", formula="lx, dx, qx actuarial life table")
_r("loss_distribution", "library", library="scipy", function="scipy.stats distributions",
   pypi="scipy>=1.11", notes="aggregate loss from frequency*severity")
_r("reserve_calculation", "formula", formula="V = PV(future_benefits) - PV(future_premiums)")

# -- Tier 5: Advanced analysis / calculus
_r("quotient_rule", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="d/dx[f/g] = (f'g - fg')/g^2")
_r("limit", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("divergence", "library", library="sympy", function="sympy.vector.divergence",
   pypi="sympy>=1.12")
_r("recurrence_solve", "library", library="sympy", function="sympy.solvers.recurr.rsolve",
   pypi="sympy>=1.12")
_r("polynomial_division", "library", library="sympy", function="sympy.div",
   pypi="sympy>=1.12")
_r("law_large_numbers", "formula", formula="sample mean converges to E[X]")

# -- Tier 5: Advanced economics
_r("cobb_douglas", "formula", formula="Y = A * L^alpha * K^beta")
_r("auction_revenue", "formula", formula="expected revenue from order statistics")

# -- Tier 5: Advanced graph theory
_r("eulerian_path", "library", library="networkx", function="networkx.eulerian_path",
   pypi="networkx>=3.1")
_r("graph_diameter", "library", library="networkx", function="networkx.diameter",
   pypi="networkx>=3.1")

# -- Tier 5: Advanced ML
_r("layer_norm", "library", library="numpy", function="(x - mean) / sqrt(var + eps) * gamma + beta",
   pypi="numpy>=1.24")
_r("positional_encoding", "library", library="numpy", function="sin/cos positional encoding",
   pypi="numpy>=1.24")
_r("beam_search_step", "formula", formula="top-k expansion by log-probability")
_r("lr_schedule", "formula", formula="lr scheduler step computation")
_r("weight_init", "formula", formula="Xavier/He/uniform init bounds")

# -- Tier 5: AI/ML computations
_r("momentum_sgd", "library", library="numpy", function="v=beta*v+grad; w=w-lr*v",
   pypi="numpy>=1.24")
_r("adam_step", "library", library="numpy", function="Adam m/v update",
   pypi="numpy>=1.24")
_r("bce_loss", "library", library="numpy", function="-y*log(p)-(1-y)*log(1-p)",
   pypi="numpy>=1.24")
_r("kl_divergence", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")
_r("batch_norm", "library", library="numpy", function="(x-mean)/sqrt(var+eps)*gamma+beta",
   pypi="numpy>=1.24")
_r("bias_variance", "formula", formula="MSE = bias^2 + variance + noise")
_r("discounted_return", "formula", formula="G = sum gamma^t * r_t")
_r("dropout_compute", "library", library="numpy", function="mask * x / (1-p)",
   pypi="numpy>=1.24")
_r("kl_from_distributions", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")
_r("markov_reward", "formula", formula="V = R + gamma * P * V")
_r("mutual_information", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11", notes="I(X;Y) = H(X) + H(Y) - H(X,Y)")
_r("roc_auc", "library", library="sklearn", function="sklearn.metrics.roc_auc_score",
   pypi="scikit-learn>=1.3")

# -- Tier 5: Aerospace
_r("thrust_equation", "formula", formula="F = m_dot * v_e + (p_e - p_a) * A_e")
_r("tsiolkovsky", "formula", formula="delta_v = v_e * ln(m0/mf)")
_r("orbital_velocity", "formula", formula="v = sqrt(GM/r)")
_r("drag_coefficient", "formula", formula="Cd = 2*F_d / (rho * v^2 * A)")
_r("lift_equation", "formula", formula="L = 0.5 * rho * v^2 * S * Cl")

# -- Tier 5: Algorithms
_r("divide_conquer_recurrence", "library", library="sympy", function="sympy.solvers.recurr",
   pypi="sympy>=1.12", notes="Master theorem / Akra-Bazzi")
_r("kmp_search", "formula", formula="failure function + pattern match")
_r("rabin_karp", "formula", formula="rolling hash comparison")
_r("suffix_array", "formula", formula="sorted suffixes by lexicographic order")
_r("matrix_chain_dp", "formula", formula="min multiplications DP")
_r("tarjan_scc", "library", library="networkx", function="networkx.strongly_connected_components",
   pypi="networkx>=3.1")
_r("a_star_search", "library", library="networkx", function="networkx.astar_path",
   pypi="networkx>=3.1")
_r("edit_distance_variants", "formula", formula="DP edit distance with custom costs")
_r("dijkstra_trace", "library", library="networkx", function="networkx.dijkstra_path",
   pypi="networkx>=3.1")
_r("kruskal_trace", "library", library="networkx", function="networkx.minimum_spanning_tree",
   pypi="networkx>=3.1")
_r("dp_knapsack_trace", "formula", formula="0/1 knapsack DP table")

# -- Tier 5: Analysis extensions
_r("limsup_liminf", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("riemann_sum", "library", library="numpy", function="numpy.sum for partition",
   pypi="numpy>=1.24")
_r("squeeze_theorem", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("mean_value_theorem", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="f'(c) = (f(b)-f(a))/(b-a)")
_r("lhopital_extended", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")

# -- Tier 5: Analytical mechanics
_r("lagrangian", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="L = T - V, Euler-Lagrange")

# -- Tier 5: Antenna theory
_r("antenna_directivity", "formula", formula="D = 4*pi*U_max / P_rad")
_r("antenna_gain_efficiency", "formula", formula="G = eta * D")
_r("friis_transmission", "formula", formula="Pr/Pt = Gt*Gr*(lambda/(4*pi*d))^2")
_r("dipole_radiation", "formula", formula="half-wave dipole pattern")
_r("effective_aperture", "formula", formula="Ae = G * lambda^2 / (4*pi)")

# -- Tier 5: Applied science
_r("kirchhoff", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24", notes="KCL/KVL linear system")
_r("convolution", "library", library="numpy", function="numpy.convolve",
   pypi="numpy>=1.24")
_r("polynomial_hash", "formula", formula="h = sum(c_i * p^i) mod m")

# -- Tier 5: Astronomy
_r("absolute_magnitude", "formula", formula="M = m - 5*log10(d/10)")
_r("doppler_velocity", "formula", formula="v = c * delta_lambda / lambda_0")
_r("tidal_force", "formula", formula="F_tidal = 2*G*M*m*r / d^3")
_r("luminosity_distance", "formula", formula="d_L = (1+z) * comoving_dist")
_r("mass_luminosity", "formula", formula="L/L_sun = (M/M_sun)^alpha")
_r("chandrasekhar_limit", "formula", formula="M_ch ~ 1.4 M_sun")
_r("virial_theorem", "formula", formula="2<T> + <V> = 0")

# -- Tier 5: Automata
_r("myhill_nerode", "reference", notes="equivalence classes -> minimal DFA states")
_r("dfa_minimization", "reference", notes="partition refinement algorithm")
_r("transducer", "reference", notes="Mealy/Moore machine simulation")
_r("two_stack_pda", "reference", notes="two-stack PDA simulation")

# -- Tier 5: Bayesian statistics
_r("map_estimate", "library", library="scipy", function="scipy.optimize.minimize",
   pypi="scipy>=1.11", notes="MAP = argmax posterior")

# -- Tier 5: Biochemistry
_r("amino_acid_property", "reference", notes="amino acid property lookup table")
_r("michaelis_menten", "formula", formula="v = Vmax * [S] / (Km + [S])")
_r("lineweaver_burk", "formula", formula="1/v = (Km/Vmax)(1/[S]) + 1/Vmax")
_r("henderson_hasselbalch", "formula", formula="pH = pKa + log([A-]/[HA])")
_r("gibbs_free_energy_biochem", "formula", formula="dG = dG0 + RT*ln(Q)")
_r("metabolic_pathway_energy", "formula", formula="total dG from pathway steps")
_r("nucleic_acid_melting", "formula", formula="Tm = 81.5 + 16.6*log[Na+] + 41*(%GC) - 600/N")
_r("redox_potential", "formula", formula="E = E0 - (RT/nF)*ln(Q)")

# -- Tier 5: Bioinformatics
_r("blast_evalue", "formula", formula="E = K*m*n*exp(-lambda*S)")
_r("phylo_distance", "formula", formula="Jukes-Cantor: d = -3/4*ln(1 - 4p/3)")
_r("open_reading_frame", "formula", formula="start codon to stop codon scan")

# -- Tier 5: Biology
_r("natural_selection_fitness", "formula", formula="p' = p*w / w_bar")
_r("phylogenetic_parsimony", "formula", formula="minimum substitutions on tree")
_r("population_growth_rate", "formula", formula="r = ln(Nt/N0)/t")
_r("allele_frequency_change", "formula", formula="Hardy-Weinberg delta_p")

# -- Tier 5: Biostatistics
_r("survival_analysis", "library", library="scipy", function="scipy.stats",
   pypi="scipy>=1.11", notes="Kaplan-Meier estimator")
_r("odds_ratio", "formula", formula="OR = (a*d)/(b*c)")
_r("sample_size", "formula", formula="n = (z*sigma/E)^2")

# -- Tier 5: Bridge / foundational
_r("joint_distribution", "library", library="numpy", function="numpy array marginals",
   pypi="numpy>=1.24")
_r("integrating_factor", "library", library="sympy", function="sympy.solvers.ode",
   pypi="sympy>=1.12")
_r("characteristic_equation", "library", library="sympy", function="sympy.solve",
   pypi="sympy>=1.12", notes="det(A - lambda*I) = 0")
_r("ring_arithmetic", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12")

# -- Tier 5: Calculus deep
_r("jacobian_matrix", "library", library="sympy", function="sympy.Matrix.jacobian",
   pypi="sympy>=1.12")
_r("implicit_function", "library", library="sympy", function="sympy.idiff",
   pypi="sympy>=1.12")
_r("integration_by_parts_definite", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("partial_fraction_integration", "library", library="sympy", function="sympy.apart + sympy.integrate",
   pypi="sympy>=1.12")
_r("directional_derivative", "library", library="sympy", function="sympy.diff + dot product",
   pypi="sympy>=1.12")

# -- Tier 5: Calculus extensions
_r("logarithmic_differentiation", "library", library="sympy", function="sympy.diff(sympy.log(f))",
   pypi="sympy>=1.12")
_r("arc_length", "library", library="sympy", function="sympy.integrate(sqrt(1+f'^2))",
   pypi="sympy>=1.12")
_r("volume_revolution", "library", library="sympy", function="sympy.integrate(pi*f^2)",
   pypi="sympy>=1.12")
_r("parametric_derivative", "library", library="sympy", function="dy/dt / dx/dt",
   pypi="sympy>=1.12")
_r("polar_area", "library", library="sympy", function="0.5*integrate(r^2, theta)",
   pypi="sympy>=1.12")
_r("multivariable_chain_rule", "library", library="sympy", function="sympy.diff with chain rule",
   pypi="sympy>=1.12")

# -- Tier 5: Causal inference
_r("ate_compute", "formula", formula="ATE = E[Y(1)] - E[Y(0)]")
_r("diff_in_diff", "formula", formula="DiD = (Y_T1-Y_T0) - (Y_C1-Y_C0)")

# -- Tier 5: Cell biology
_r("cell_signaling", "reference", notes="signaling pathway classification")
_r("gene_expression_regulation", "reference", notes="transcription factor binding")
_r("receptor_binding", "formula", formula="binding curve: B = Bmax*[L]/(Kd+[L])")

# -- Tier 5: Chemistry
_r("activation_energy", "formula", formula="Ea from Arrhenius: ln(k) = ln(A) - Ea/RT")
_r("buffer_henderson", "formula", formula="pH = pKa + log([A-]/[HA])")
_r("galvanic_cell", "formula", formula="E_cell = E_cathode - E_anode")
_r("faraday_electrolysis", "formula", formula="m = (M*I*t)/(n*F)")
_r("born_haber_cycle", "formula", formula="sum of enthalpy steps = 0")
_r("complexation_equilibrium", "formula", formula="Kf = [complex]/([M][L])")
_r("thermodynamic_cycle", "formula", formula="sum dH around cycle = 0")

# -- Tier 5: Classical mechanics
_r("elastic_collision", "formula", formula="conservation of momentum + KE")
_r("torque_rotation", "formula", formula="tau = I * alpha")
_r("moment_of_inertia_physics", "formula", formula="I = sum(m_i * r_i^2)")
_r("angular_momentum_conservation", "formula", formula="L = I * omega = const")
_r("damped_oscillation", "formula", formula="x(t) = A*e^(-bt/2m)*cos(omega_d*t)")

# -- Tier 5: Climate science
_r("radiative_forcing", "formula", formula="dF = 5.35 * ln(C/C0)")
_r("greenhouse_effect", "formula", formula="Te = (S(1-a)/(4*sigma))^0.25")
_r("sea_level_rise", "formula", formula="thermal expansion + ice melt")
_r("climate_sensitivity", "formula", formula="dT = lambda * dF")

# -- Tier 5: Coding theory
_r("linear_code", "library", library="numpy", function="numpy.matmul for generator matrix",
   pypi="numpy>=1.24", notes="codeword = message * G")
_r("syndrome_decode", "library", library="numpy", function="syndrome = H * r^T",
   pypi="numpy>=1.24")
_r("code_parameters", "formula", formula="[n, k, d] from generator/parity matrix")
_r("turbo_code_interleave", "formula", formula="interleaver permutation")

# -- Tier 5: Cognitive science
_r("signal_detection", "formula", formula="d' = z(hit_rate) - z(fa_rate)")
_r("memory_decay", "formula", formula="R = e^(-t/S) Ebbinghaus")
_r("reaction_time", "formula", formula="Hick's law: RT = a + b*log2(n)")
_r("rescorla_wagner", "formula", formula="dV = alpha*beta*(lambda - V)")

# -- Tier 5: Combinatorial optimization
_r("tsp_nearest_neighbor", "formula", formula="greedy nearest-neighbor heuristic")
_r("matching_bipartite", "library", library="networkx", function="networkx.bipartite.maximum_matching",
   pypi="networkx>=3.1")
_r("job_scheduling", "formula", formula="scheduling heuristic")
_r("set_cover_greedy", "formula", formula="greedy set cover")
_r("bin_packing", "formula", formula="first-fit / best-fit heuristic")

# -- Tier 5: Combinatorics
_r("recurrence_characteristic", "library", library="sympy", function="sympy.solvers.recurr.rsolve",
   pypi="sympy>=1.12")
_r("derangement_compute", "formula", formula="D_n = n! * sum(-1)^k/k!")
_r("twelvefold_way", "formula", formula="twelvefold way counting formulas")
_r("latin_square", "formula", formula="n x n array with unique row/col entries")
_r("ballot_problem", "formula", formula="P = (a-b)/(a+b)")

# -- Tier 5: Communication systems
_r("companding", "formula", formula="mu-law / A-law compression")
_r("constellation_diagram", "formula", formula="QAM/PSK signal point coordinates")

# -- Tier 5: Compilers
_r("recursive_descent", "reference", notes="LL(1) parser construction")
_r("first_follow_set", "reference", notes="FIRST/FOLLOW set computation")
_r("type_check", "reference", notes="type inference/checking rules")
_r("register_allocation", "reference", notes="graph coloring for register allocation")
_r("instruction_selection", "reference", notes="tree pattern matching")
_r("ssa_conversion", "reference", notes="SSA form with phi functions")
_r("loop_optimization", "reference", notes="loop invariant code motion")
_r("tail_call_optimization", "reference", notes="tail call elimination")

# -- Tier 5: Compressed sensing
_r("sparse_recovery", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11", notes="L1 minimisation")
_r("coherence", "library", library="numpy", function="max abs column inner product",
   pypi="numpy>=1.24")

# -- Tier 5: Computer architecture
_r("branch_prediction", "formula", formula="2-bit saturating counter")
_r("instruction_scheduling", "formula", formula="pipeline hazard resolution")

# -- Tier 5: Computer graphics
_r("matrix_transform_3d", "library", library="numpy", function="numpy.matmul for 4x4 transforms",
   pypi="numpy>=1.24")
_r("perspective_projection", "library", library="numpy", function="projection matrix multiply",
   pypi="numpy>=1.24")
_r("ray_sphere_intersect", "formula", formula="quadratic |o+td-c|^2 = r^2")
_r("barycentric_coords", "library", library="numpy", function="area ratios",
   pypi="numpy>=1.24")
_r("bezier_curve", "library", library="numpy", function="De Casteljau / Bernstein polynomials",
   pypi="numpy>=1.24")
_r("phong_shading", "formula", formula="I = Ia*ka + Id*kd*(N.L) + Is*ks*(R.V)^n")
_r("frustum_culling", "formula", formula="point vs plane half-space test")

# -- Tier 5: Continuum mechanics
_r("mohr_circle", "formula", formula="sigma_n, tau from transformation")
_r("elastic_moduli", "formula", formula="E, G, K, nu relationships")

# -- Tier 5: Control theory
_r("transfer_function_sys", "library", library="scipy", function="scipy.signal.TransferFunction",
   pypi="scipy>=1.11")
_r("pid_response", "library", library="scipy", function="scipy.signal.lsim",
   pypi="scipy>=1.11")
_r("bode_magnitude", "library", library="scipy", function="scipy.signal.bode",
   pypi="scipy>=1.11")
_r("feedback_gain", "library", library="scipy", function="scipy.signal.feedback",
   pypi="scipy>=1.11")
_r("steady_state_error", "formula", formula="e_ss from final value theorem")
_r("second_order_response", "formula", formula="omega_n, zeta, overshoot, settling")

# -- Tier 5: Cryptography
_r("hash_collision", "formula", formula="birthday bound: sqrt(pi*n/2)")
_r("feistel_round", "formula", formula="L=R, R=L xor F(R,K)")
_r("birthday_attack", "formula", formula="P(collision) ~ n^2/(2*H)")
_r("known_plaintext", "formula", formula="key recovery from P,C pairs")
_r("secret_sharing_threshold", "formula", formula="Shamir polynomial interpolation")
_r("commitment_pedersen", "formula", formula="C = g^m * h^r mod p")
_r("shamir_secret_share", "library", library="sympy", function="sympy.interpolate (Lagrange)",
   pypi="sympy>=1.12")
_r("commitment_scheme", "formula", formula="binding + hiding properties")
_r("merkle_tree", "formula", formula="hash(left || right) tree")
_r("stream_cipher", "formula", formula="C = P xor keystream")
_r("block_cipher_modes", "formula", formula="ECB/CBC/CTR mode transformations")

# -- Tier 5: CS foundations
_r("softmax_eval", "library", library="numpy", function="exp(x)/sum(exp(x))",
   pypi="numpy>=1.24")
_r("attention_score", "library", library="numpy", function="softmax(QK^T/sqrt(d))*V",
   pypi="numpy>=1.24")
_r("backprop_simple", "library", library="numpy", function="chain rule gradient",
   pypi="numpy>=1.24")

# -- Tier 5: CS theory
_r("time_complexity_compute", "formula", formula="counting operations / Master theorem")
_r("space_complexity", "formula", formula="memory usage analysis")
_r("streaming_algorithm", "formula", formula="space-accuracy tradeoff")

# -- Tier 5: Data structures
_r("avl_rotation", "reference", notes="AVL tree rotation rules")
_r("red_black_insert", "reference", notes="red-black tree insert with recolor/rotate")
_r("b_tree_insert", "reference", notes="B-tree split and insert")
_r("skip_list", "reference", notes="skip list level assignment")

# -- Tier 5: Decision theory
_r("expected_utility", "formula", formula="EU = sum p_i * u(x_i)")
_r("risk_dominance", "formula", formula="dominance comparison across states")
_r("multi_criteria", "formula", formula="weighted sum / Pareto ranking")

# -- Tier 5: Differential geometry
_r("surface_normal", "library", library="numpy", function="cross product of partials",
   pypi="numpy>=1.24")

# -- Tier 5: Digital electronics
_r("timing_analysis", "formula", formula="setup/hold time, clock-to-q")
_r("counter_design", "formula", formula="state machine next-state logic")

# -- Tier 5: Dimensionality reduction
_r("pca_compute", "library", library="numpy", function="numpy.linalg.eigh on covariance",
   pypi="numpy>=1.24")
_r("explained_variance", "library", library="numpy", function="eigenvalue ratios",
   pypi="numpy>=1.24")
_r("feature_selection", "formula", formula="information gain / correlation filter")

# -- Tier 5: Discrete math
_r("ramsey_number", "reference", notes="known Ramsey bounds R(s,t)")
_r("hall_marriage", "library", library="networkx", function="networkx.bipartite.maximum_matching",
   pypi="networkx>=3.1", notes="Hall's theorem: perfect matching iff |N(S)| >= |S|")
_r("flow_network", "library", library="networkx", function="networkx.maximum_flow",
   pypi="networkx>=3.1")
_r("planar_check", "library", library="networkx", function="networkx.check_planarity",
   pypi="networkx>=3.1")
_r("lattice_operations", "formula", formula="meet/join in lattice")

# -- Tier 5: Distributed systems
_r("lamport_clock", "formula", formula="max(local, received) + 1")
_r("vector_clock_compare", "formula", formula="component-wise comparison")
_r("cap_theorem", "reference", notes="consistency/availability/partition tolerance tradeoff")
_r("consistent_hash_rebalance", "formula", formula="hash ring rebalancing")
_r("crdt_merge", "formula", formula="commutative merge operation")
_r("quorum_systems", "formula", formula="read_quorum + write_quorum > n")
_r("eventual_consistency", "reference", notes="convergence guarantees")
_r("sharding_strategy", "formula", formula="hash/range partitioning")
_r("log_structured_merge", "reference", notes="LSM tree compaction")
_r("gossip_protocol", "formula", formula="infection spread: O(log n) rounds")
_r("snapshot_algorithm", "reference", notes="Chandy-Lamport algorithm")

# -- Tier 5: Ecology
_r("lotka_volterra", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="predator-prey ODE system")
_r("population_doubling", "formula", formula="t_d = ln(2) / r")
_r("species_diversity", "formula", formula="Shannon H = -sum(p_i * ln(p_i))")
_r("carrying_capacity", "formula", formula="logistic: dN/dt = rN(1-N/K)")
_r("competition_model", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="Lotka-Volterra competition")
_r("predator_functional_response", "formula", formula="Holling type II: f(N) = aN/(1+ahN)")
_r("island_biogeography", "formula", formula="S = cA^z species-area")
_r("life_history_table", "formula", formula="lx, mx, R0, Tc from life table")
_r("metapopulation", "formula", formula="dp/dt = cp(1-p) - ep Levins model")
_r("biodiversity_index", "formula", formula="Simpson D = 1 - sum(p_i^2)")

# -- Tier 5: Economics
_r("is_lm_model", "formula", formula="IS: Y=C+I+G, LM: M/P=L(r,Y)")
_r("solow_growth", "formula", formula="k_dot = sf(k) - (n+delta)k")
_r("oligopoly_bertrand", "formula", formula="price competition equilibrium")
_r("adverse_selection", "formula", formula="pooling/separating equilibrium")
_r("moral_hazard", "formula", formula="incentive compatibility constraint")
_r("consumer_surplus", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12", notes="integral of demand - price")
_r("production_function", "formula", formula="Q = f(L, K) marginal products")
_r("game_theory_market", "formula", formula="Nash equilibrium computation")

# -- Tier 5: Electromagnetism
_r("rc_circuit", "formula", formula="V(t) = V0 * e^(-t/RC)")
_r("electromagnetic_wave", "formula", formula="c = 1/sqrt(mu_0*eps_0)")
_r("electric_dipole", "formula", formula="E = kp/r^3 (axial), V = kp*cos(theta)/r^2")
_r("magnetic_field_wire", "formula", formula="B = mu_0*I/(2*pi*r)")
_r("ampere_law", "formula", formula="integral B.dl = mu_0 * I_enc")
_r("lenz_law", "formula", formula="induced EMF opposes flux change")
_r("lc_oscillation", "formula", formula="omega = 1/sqrt(LC)")
_r("gauss_sphere", "formula", formula="E * 4*pi*r^2 = Q/eps_0")
_r("capacitor_network", "formula", formula="series: 1/C = sum(1/Ci), parallel: C = sum(Ci)")
_r("rc_time_constant", "formula", formula="tau = RC")
_r("rl_circuit", "formula", formula="I(t) = I0*(1-e^(-t*R/L))")
_r("wheatstone_bridge", "formula", formula="Rx = R3*R2/R1 at balance")
_r("skin_depth", "formula", formula="delta = sqrt(2*rho/(omega*mu))")

# -- Tier 5: Engineering
_r("fft_butterfly", "library", library="numpy", function="numpy.fft.fft",
   pypi="numpy>=1.24")
_r("pid_tuning", "formula", formula="Ziegler-Nichols tuning rules")
_r("power_flow_dc", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24", notes="DC power flow: P = B * theta")
_r("fatigue_life", "formula", formula="S-N curve: N = (S/a)^(1/b)")
_r("filter_design", "library", library="scipy", function="scipy.signal.butter/cheby1",
   pypi="scipy>=1.11")
_r("impedance_matching", "formula", formula="Z_in = Z0*(ZL+jZ0*tan(beta*l))/(Z0+jZL*tan(beta*l))")
_r("vibration_analysis", "formula", formula="omega_n = sqrt(k/m), zeta = c/(2*sqrt(km))")

# -- Tier 5: Environmental
_r("bod_decay", "formula", formula="BOD(t) = L*(1-e^(-kt))")

# -- Tier 5: Epidemiology
_r("sir_model", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="dS/dt=-beta*S*I, dI/dt=beta*S*I-gamma*I")
_r("basic_reproduction", "formula", formula="R0 = beta/gamma")
_r("life_table", "formula", formula="lx, dx, qx life table computation")

# -- Tier 5: Expanded core
_r("implicit_diff", "library", library="sympy", function="sympy.idiff",
   pypi="sympy>=1.12")
_r("area_under_curve", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("related_rates", "library", library="sympy", function="sympy.diff + chain rule",
   pypi="sympy>=1.12")
_r("logarithm", "library", library="math", function="math.log",
   pypi="(stdlib)")

# -- Tier 5: Expert analysis
_r("newton_raphson", "library", library="sympy", function="sympy.nsolve",
   pypi="sympy>=1.12")
_r("gaussian_elimination", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24")
_r("laplace_transform", "library", library="sympy", function="sympy.integrals.transforms.laplace_transform",
   pypi="sympy>=1.12")
_r("sigmoid_eval", "library", library="numpy", function="1/(1+exp(-x))",
   pypi="numpy>=1.24")
_r("cross_entropy", "library", library="numpy", function="-sum(y*log(p))",
   pypi="numpy>=1.24")
_r("info_entropy", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")
_r("vigenere", "formula", formula="polyalphabetic shift cipher")

# -- Tier 5: Financial mathematics
_r("portfolio_variance", "library", library="numpy", function="w^T * Sigma * w",
   pypi="numpy>=1.24")
_r("sharpe_ratio", "formula", formula="(R_p - R_f) / sigma_p")
_r("var_computation", "library", library="scipy", function="scipy.stats.norm.ppf",
   pypi="scipy>=1.11", notes="Value at Risk")
_r("bond_pricing", "formula", formula="P = sum C/(1+r)^t + F/(1+r)^n")
_r("duration_bond", "formula", formula="D = sum t*CF/(1+r)^t / P")

# -- Tier 5: Fluid mechanics
_r("viscous_flow", "formula", formula="Navier-Stokes simplification")
_r("mach_number", "formula", formula="M = v / sqrt(gamma*R*T)")
_r("boundary_layer", "formula", formula="Blasius: delta = 5x/sqrt(Re_x)")
_r("water_hammer", "formula", formula="dp = rho * c * dv")
_r("pipe_flow", "formula", formula="Darcy-Weisbach: hf = f*L*v^2/(2*g*D)")
_r("venturi_meter", "formula", formula="Bernoulli + continuity: Q = Cd*A2*sqrt(2*dp/rho)")
_r("hydraulic_jump", "formula", formula="y2/y1 = 0.5*(sqrt(1+8*Fr^2) - 1)")
_r("open_channel", "formula", formula="Manning: Q = (1/n)*A*R^(2/3)*S^(1/2)")

# -- Tier 5: Formal languages
_r("nfa_to_dfa", "reference", notes="subset construction algorithm")
_r("regex_to_nfa", "reference", notes="Thompson's construction")
_r("cfg_derivation", "reference", notes="leftmost/rightmost derivation")
_r("pushdown_simulate", "reference", notes="PDA state transition simulation")

# -- Tier 5: Functional analysis
_r("norm_compute", "library", library="numpy", function="numpy.linalg.norm",
   pypi="numpy>=1.24")
_r("inner_product_verify", "library", library="numpy", function="numpy.dot",
   pypi="numpy>=1.24")
_r("lp_space_norm", "library", library="numpy", function="sum(|x|^p)^(1/p)",
   pypi="numpy>=1.24")

# -- Tier 5: Fuzzy logic
_r("fuzzy_inference", "formula", formula="min/max fuzzy rule evaluation")
_r("defuzzification", "formula", formula="centroid: sum(mu*x)/sum(mu)")

# -- Tier 5: Game theory
_r("mixed_strategy_ne", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11", notes="linear program for Nash equilibrium")
_r("backward_induction", "formula", formula="recursive subgame solution")
_r("auction_first_price", "formula", formula="bid = (n-1)/n * v")
_r("extensive_form", "formula", formula="game tree evaluation")
_r("repeated_game", "formula", formula="folk theorem / discount factor")
_r("shapley_value", "formula", formula="phi_i = sum |S|!(n-|S|-1)!/n! * marginal")

# -- Tier 5: General chemistry
_r("ideal_gas_stoich", "formula", formula="PV = nRT with stoichiometry")
_r("acid_base_titration", "formula", formula="equivalence point pH calculation")
_r("buffer_capacity", "formula", formula="beta = 2.3*C*Ka*[H+]/(Ka+[H+])^2")

# -- Tier 5: Genetics
_r("epistasis", "formula", formula="modified phenotypic ratios")
_r("genetic_drift", "formula", formula="p(fix) = 1/(2N) per generation")
_r("linkage_disequilibrium", "formula", formula="D = p_AB - p_A*p_B")
_r("quantitative_trait", "formula", formula="heritability h^2 = Vg/Vp")
_r("population_bottleneck", "formula", formula="He = 1 - (1 - 1/(2N))^t")
_r("inbreeding_coefficient", "formula", formula="F = sum((1/2)^(n+1) * (1+Fa))")

# -- Tier 5: Geology
_r("radiometric_dating", "formula", formula="t = (1/lambda)*ln(1 + D/N)")
_r("richter_magnitude", "formula", formula="M = log10(A) + corrections")
_r("earthquake_energy", "formula", formula="log10(E) = 1.5*M + 4.8")

# -- Tier 5: Geometry extensions
_r("circle_from_three_points", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24", notes="circumscribed circle from 3 points")
_r("plane_equation", "library", library="numpy", function="numpy.cross for normal",
   pypi="numpy>=1.24")
_r("conic_section", "library", library="sympy", function="sympy.geometry.Ellipse/Parabola",
   pypi="sympy>=1.12")

# -- Tier 5: Geophysics
_r("gravity_anomaly", "formula", formula="dg = G*M*d / (r^2 + d^2)^(3/2)")
_r("seismic_moment", "formula", formula="M0 = mu * A * D")
_r("isostasy", "formula", formula="rho_c * h = rho_m * d Airy model")
_r("heat_flow", "formula", formula="q = -k * dT/dz")

# -- Tier 5: Graphs
_r("graph_matching", "library", library="networkx", function="networkx.max_weight_matching",
   pypi="networkx>=3.1")
_r("topological_sort_dfs", "library", library="networkx", function="networkx.topological_sort",
   pypi="networkx>=3.1")

# -- Tier 5: Harmonic analysis
_r("sampling_reconstruction", "formula", formula="Nyquist: f_s >= 2*f_max")

# -- Tier 5: Heat transfer
_r("heat_exchanger", "formula", formula="Q = U*A*LMTD")
_r("fin_efficiency", "formula", formula="eta = tanh(mL)/(mL)")

# -- Tier 5: Information theory
_r("huffman_coding", "formula", formula="optimal prefix-free code from frequencies")
_r("hamming_encode", "library", library="numpy", function="G*m mod 2",
   pypi="numpy>=1.24")
_r("hamming_decode", "library", library="numpy", function="H*r mod 2 syndrome",
   pypi="numpy>=1.24")
_r("source_coding", "formula", formula="L >= H(X) Shannon source coding")
_r("error_rate", "formula", formula="BER = Q(sqrt(2*Eb/N0))")
_r("aep_property", "formula", formula="typical set probability ~ 2^(-nH)")
_r("entropy_rate", "formula", formula="H_rate = lim H(X_n|X_1..X_{n-1})")
_r("conditional_entropy", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11", notes="H(Y|X) = H(X,Y) - H(X)")
_r("joint_entropy", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")
_r("kraft_mcmillan", "formula", formula="sum 2^(-l_i) <= 1")

# -- Tier 5: Inorganic chemistry
_r("crystal_field", "formula", formula="CFSE = crystal field splitting energy")
_r("isomer_coordination", "reference", notes="coordination isomer enumeration")
_r("spectrochemical", "reference", notes="spectrochemical series ordering")
_r("magnetic_moment", "formula", formula="mu = sqrt(n(n+2)) BM")
_r("solubility_product", "formula", formula="Ksp = [cation]^m * [anion]^n")
_r("lattice_energy", "formula", formula="Born-Lande: U = -N*A*z+*z-*e^2/(4*pi*eps*r0)*(1-1/n)")
_r("band_theory_ext", "reference", notes="band structure classification")
_r("trans_effect", "reference", notes="trans effect series ordering")
_r("hard_soft_acid_base", "reference", notes="HSAB classification")
_r("molecular_orbital_diagram", "reference", notes="MO energy level diagram")
_r("redox_balancing", "formula", formula="half-reaction balancing")

# -- Tier 5: Linear algebra extensions
_r("gram_schmidt", "library", library="numpy", function="numpy.linalg.qr",
   pypi="numpy>=1.24")
_r("quadratic_form", "library", library="numpy", function="x^T A x",
   pypi="numpy>=1.24")
_r("projection_matrix", "library", library="numpy", function="P = A(A^TA)^{-1}A^T",
   pypi="numpy>=1.24")
_r("markov_steady_state", "library", library="numpy", function="numpy.linalg.eig",
   pypi="numpy>=1.24", notes="left eigenvector for eigenvalue 1")

# -- Tier 5: Linguistics
_r("chomsky_classify", "reference", notes="Chomsky hierarchy classification")
_r("language_entropy", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")

# -- Tier 5: Logic
_r("set_cardinality_infinite", "reference", notes="countable/uncountable classification")
_r("boolean_algebra_lattice", "formula", formula="lattice operations on Boolean algebra")
_r("cnf_conversion", "library", library="sympy", function="sympy.logic.boolalg.to_cnf",
   pypi="sympy>=1.12")
_r("dnf_conversion", "library", library="sympy", function="sympy.logic.boolalg.to_dnf",
   pypi="sympy>=1.12")
_r("logical_consequence", "library", library="sympy", function="sympy.logic.inference.satisfiable",
   pypi="sympy>=1.12")
_r("reductio_ad_absurdum", "reference", notes="proof by contradiction structure")

# -- Tier 5: Materials science
_r("crystal_structure", "reference", notes="crystal system classification")
_r("diffusion_fick", "formula", formula="J = -D * dC/dx (Fick's first law)")
_r("phase_diagram", "reference", notes="phase boundary / lever rule")
_r("fatigue_sn_curve", "formula", formula="S = a * N^b Basquin's law")
_r("creep_rate", "formula", formula="eps_dot = A * sigma^n * exp(-Q/RT)")
_r("fracture_toughness", "formula", formula="K_IC = sigma * sqrt(pi*a) * Y")
_r("grain_size", "formula", formula="Hall-Petch: sigma_y = sigma_0 + k/sqrt(d)")

# -- Tier 5: Measure theory
_r("probability_measure", "formula", formula="P(Omega)=1, countable additivity")

# -- Tier 5: Measurement
_r("error_propagation", "formula", formula="sigma_f^2 = sum (df/dx_i)^2 * sigma_i^2")
_r("calibration_curve", "library", library="numpy", function="numpy.polyfit",
   pypi="numpy>=1.24")
_r("logarithmic_scales", "formula", formula="dB = 10*log10(P2/P1)")

# -- Tier 5: Medical imaging
_r("mri_signal", "formula", formula="S = S0*(1-e^(-TR/T1))*e^(-TE/T2)")
_r("image_convolution", "library", library="scipy", function="scipy.signal.convolve2d",
   pypi="scipy>=1.11")

# -- Tier 5: ML deep
_r("batch_norm_forward", "library", library="numpy", function="(x-mean)/sqrt(var+eps)*gamma+beta",
   pypi="numpy>=1.24")
_r("conv2d_forward", "library", library="numpy", function="sliding window dot product",
   pypi="numpy>=1.24")
_r("gelu_compute", "library", library="numpy", function="x*0.5*(1+erf(x/sqrt(2)))",
   pypi="numpy>=1.24")
_r("gradient_clipping", "library", library="numpy", function="g * max_norm / norm(g)",
   pypi="numpy>=1.24")
_r("weight_decay_update", "formula", formula="w = w - lr*(grad + lambda*w)")
_r("sgd_momentum_step", "library", library="numpy", function="v=mu*v-lr*g; w+=v",
   pypi="numpy>=1.24")
_r("adam_full_step", "library", library="numpy", function="Adam with bias correction",
   pypi="numpy>=1.24")
_r("mixup_training", "library", library="numpy", function="x=lam*x1+(1-lam)*x2",
   pypi="numpy>=1.24")
_r("model_flops_compute", "formula", formula="FLOPs from layer dimensions")
_r("normalization_comparison", "formula", formula="LayerNorm vs BatchNorm vs GroupNorm")
_r("loss_function_comparison", "formula", formula="CE vs MSE vs focal loss")

# -- Tier 5: ML theory
_r("cross_validation_compute", "formula", formula="k-fold CV average")
_r("information_gain", "formula", formula="IG = H(parent) - sum(w*H(child))")

# -- Tier 5: Music theory
_r("chord_progression", "reference", notes="Roman numeral analysis")
_r("voice_leading", "reference", notes="voice leading rules")

# -- Tier 5: Network science
_r("degree_distribution", "library", library="networkx", function="networkx.degree_histogram",
   pypi="networkx>=3.1")
_r("clustering_coefficient", "library", library="networkx", function="networkx.clustering",
   pypi="networkx>=3.1")
_r("small_world_check", "library", library="networkx", function="networkx.average_shortest_path_length",
   pypi="networkx>=3.1")

# -- Tier 5: Networking
_r("tcp_window", "formula", formula="window size / RTT throughput")
_r("crc_check", "formula", formula="polynomial division mod 2")
_r("tcp_congestion", "formula", formula="AIMD: additive increase, multiplicative decrease")
_r("sliding_window", "formula", formula="window-based flow control")
_r("congestion_avoidance", "formula", formula="cwnd adjustment algorithms")
_r("bgp_routing", "reference", notes="BGP path selection rules")
_r("wifi_throughput", "formula", formula="channel capacity with overhead")
_r("packet_loss_retransmit", "formula", formula="retransmission timeout / exponential backoff")

# -- Tier 5: Neuroscience
_r("membrane_potential", "formula", formula="Nernst: E = (RT/zF)*ln([out]/[in])")
_r("goldman_equation", "formula", formula="Vm = RT/F * ln(sum P_i*[out]_i / sum P_i*[in]_i)")
_r("receptive_field", "formula", formula="Gaussian/Gabor filter response")
_r("neural_coding", "formula", formula="firing rate / tuning curve")
_r("synaptic_integration", "formula", formula="temporal/spatial summation")
_r("eeg_frequency", "formula", formula="frequency band classification")
_r("fmri_bold", "formula", formula="hemodynamic response function")

# -- Tier 5: NLP
_r("tf_idf", "formula", formula="tf*idf = freq(t,d) * log(N/df(t))")
_r("ngram_probability", "formula", formula="P(w|history) from counts")
_r("bleu_score", "formula", formula="BP * exp(sum w_n * log(p_n))")
_r("perplexity", "formula", formula="PP = 2^H = exp(-1/N * sum log P(w_i))")

# -- Tier 5: Nonlinear dynamics
_r("fixed_point_classify", "library", library="numpy", function="numpy.linalg.eigvals for Jacobian",
   pypi="numpy>=1.24")
_r("logistic_map", "formula", formula="x_{n+1} = r*x_n*(1-x_n)")

# -- Tier 5: Nonparametric statistics
_r("permutation_test", "library", library="scipy", function="scipy.stats.permutation_test",
   pypi="scipy>=1.11")
_r("bootstrap_ci", "library", library="numpy", function="numpy.percentile on resamples",
   pypi="numpy>=1.24")

# -- Tier 5: Nuclear physics
_r("mass_defect", "formula", formula="dm = Z*m_p + N*m_n - M_atom")
_r("binding_energy_per_nucleon", "formula", formula="BE/A = dm*c^2/A")
_r("radioactive_decay", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="N(t) = N0*e^(-lambda*t)")
_r("half_life", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="t_1/2 = ln(2)/lambda")
_r("decay_chain", "formula", formula="Bateman equations")
_r("activity", "formula", formula="A = lambda*N = A0*e^(-lambda*t)")
_r("carbon_dating", "formula", formula="t = -t_1/2 * log2(N/N0) / ln(2)")
_r("dose_calculation", "formula", formula="D = A * S-factor * t")
_r("neutron_moderation", "formula", formula="avg log energy decrement per collision")

# -- Tier 5: Number theory
_r("fermat_little", "library", library="sympy", function="pow(a, p-1, p) == 1",
   pypi="sympy>=1.12")
_r("perfect_power_test", "library", library="sympy", function="sympy.ntheory.perfect_power",
   pypi="sympy>=1.12")
_r("sum_of_four_squares", "library", library="sympy", function="sympy.ntheory.sum_of_four_squares",
   pypi="sympy>=1.12")
_r("modular_equation", "library", library="sympy", function="sympy.ntheory.solve_congruence",
   pypi="sympy>=1.12")

# -- Tier 5: Numerical methods
_r("newton_interpolation", "formula", formula="divided differences interpolation")
_r("numerical_integration_error", "formula", formula="error bounds for quadrature")
_r("jacobi_iteration", "library", library="numpy", function="iterative matrix solve",
   pypi="numpy>=1.24")
_r("gauss_seidel", "library", library="numpy", function="iterative matrix solve",
   pypi="numpy>=1.24")
_r("secant_method", "formula", formula="x_{n+1} = x_n - f(x_n)*(x_n-x_{n-1})/(f(x_n)-f(x_{n-1}))")
_r("fixed_point_iteration", "formula", formula="x_{n+1} = g(x_n)")
_r("simpson_rule", "library", library="scipy", function="scipy.integrate.simpson",
   pypi="scipy>=1.11")
_r("interpolation_lagrange", "library", library="scipy", function="scipy.interpolate.lagrange",
   pypi="scipy>=1.11")

# -- Tier 5: Oceanography
_r("coriolis_force", "formula", formula="f = 2*omega*sin(phi)")
_r("thermohaline", "formula", formula="density from T, S using equation of state")
_r("ekman_depth", "formula", formula="D_E = pi*sqrt(2*A_z/(f))")
_r("mixed_layer_depth", "formula", formula="TKE budget / Richardson number")

# -- Tier 5: Open problems
_r("zeta_partial_sum", "library", library="sympy", function="sum 1/n^s",
   pypi="sympy>=1.12")
_r("waring_representation", "formula", formula="n as sum of k-th powers")
_r("brocard_check", "formula", formula="n! + 1 = m^2 check")
_r("sat_verify", "formula", formula="evaluate CNF assignment")

# -- Tier 5: Operations research
_r("mm1_queue", "formula", formula="L=lambda/(mu-lambda), W=1/(mu-lambda)")
_r("newsvendor", "formula", formula="Q* = F^{-1}(Cu/(Cu+Co))")
_r("project_scheduling", "formula", formula="CPM critical path")
_r("reliability", "formula", formula="R(t) = e^(-lambda*t) series/parallel")

# -- Tier 5: Optics
_r("double_slit", "formula", formula="d*sin(theta) = m*lambda")
_r("brewster_angle", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="tan(theta_B) = n2/n1")
_r("diffraction_grating", "formula", formula="d*sin(theta) = m*lambda")
_r("michelson_interferometer", "formula", formula="delta = 2*d*cos(theta)")
_r("coherence_length", "formula", formula="l_c = c / delta_f")
_r("optical_fiber_modes", "formula", formula="V = (pi*d/lambda)*NA")
_r("jones_matrix", "library", library="numpy", function="2x2 matrix multiplication",
   pypi="numpy>=1.24")
_r("prism_dispersion", "formula", formula="Snell's law + angular deviation")
_r("lens_makers", "formula", formula="1/f = (n-1)*(1/R1 - 1/R2)")
_r("two_lens_system", "formula", formula="1/f_total = 1/f1 + 1/f2 - d/(f1*f2)")
_r("single_slit_diffraction", "formula", formula="a*sin(theta) = m*lambda")
_r("thin_film_interference", "formula", formula="2*n*t*cos(theta) = (m+1/2)*lambda")
_r("resolving_power", "formula", formula="Rayleigh: theta = 1.22*lambda/D")

# -- Tier 5: Optimization
_r("gradient_descent_convergence", "formula", formula="f(x_{k+1}) <= f(x_k) - alpha*||grad||^2")

# -- Tier 5: Organic chemistry
_r("stereocenter_count", "formula", formula="max stereoisomers = 2^n")
_r("sn1_vs_sn2", "reference", notes="substrate/nucleophile/solvent classification")
_r("polymer_repeat_unit", "formula", formula="monomer -> repeat unit structure")
_r("isomer_count", "formula", formula="structural isomer enumeration")
_r("markovnikov_rule", "reference", notes="regioselectivity of HX addition")
_r("zaitsev_rule", "reference", notes="most substituted alkene product")
_r("oxidation_reduction_organic", "reference", notes="oxidation state changes")
_r("fischer_projection", "reference", notes="Fischer projection rules")

# -- Tier 5: OS
_r("deadlock_detection", "formula", formula="resource allocation graph cycle check")
_r("semaphore_trace", "formula", formula="P/V operation trace")

# -- Tier 5: Particle physics
_r("conservation_laws", "reference", notes="charge/baryon/lepton number conservation")
_r("quark_content", "reference", notes="quark composition lookup")
_r("cms_energy", "formula", formula="sqrt(s) = 2*sqrt(E1*E2) for head-on")

# -- Tier 5: PDE
_r("diffusion_equation", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="u_t = D * u_xx")

# -- Tier 5: Persistent homology
_r("simplicial_complex", "formula", formula="simplex face/boundary relations")
_r("vietoris_rips", "formula", formula="distance threshold complex construction")

# -- Tier 5: Pharmacology
_r("half_life_drug", "formula", formula="t_1/2 = ln(2)/k_el")
_r("dose_response", "formula", formula="E = Emax*[D]^n / (EC50^n + [D]^n)")
_r("bioavailability", "formula", formula="F = AUC_oral / AUC_iv")
_r("clearance_rate", "formula", formula="Cl = dose / AUC")
_r("steady_state", "formula", formula="C_ss = dose/(Cl*tau)")
_r("drug_interaction", "formula", formula="enzyme inhibition Ki effect")
_r("receptor_occupancy", "formula", formula="f = [D]/(Kd + [D])")
_r("loading_dose", "formula", formula="LD = Vd * C_target / F")
_r("bioequivalence", "formula", formula="90% CI of AUC ratio within 80-125%")

# -- Tier 5: Photonics
_r("fiber_optics_na", "formula", formula="NA = sqrt(n1^2 - n2^2)")
_r("laser_gain", "formula", formula="g = sigma * (N2 - N1)")
_r("laser_threshold", "formula", formula="gain = loss at threshold")
_r("photonic_bandgap", "formula", formula="Bragg condition: 2*n*d = m*lambda")

# -- Tier 5: Physical chemistry
_r("le_chatelier", "reference", notes="equilibrium shift prediction")
_r("hess_law", "formula", formula="dH_rxn = sum(dH_f products) - sum(dH_f reactants)")
_r("reaction_order", "formula", formula="rate = k[A]^m[B]^n from experimental data")
_r("reaction_half_life", "formula", formula="t_1/2 = ln(2)/k (first order)")
_r("integrated_rate_law", "formula", formula="[A] vs t for 0th/1st/2nd order")
_r("equilibrium_ice_table", "formula", formula="ICE table for equilibrium concentrations")
_r("colligative_properties", "formula", formula="dT = i*K*m boiling/freezing point")
_r("phase_equilibria", "formula", formula="Clausius-Clapeyron: dP/dT = dH/(T*dV)")
_r("electrochemistry_cell", "formula", formula="Nernst: E = E0 - (RT/nF)*ln(Q)")
_r("quantum_chem_orbital", "reference", notes="orbital energy/shape classification")

# -- Tier 5: Physics
_r("redshift", "formula", formula="z = (lambda_obs - lambda_emit) / lambda_emit")

# -- Tier 5: Plasma physics
_r("debye_length", "formula", formula="lambda_D = sqrt(eps_0*kT/(n*e^2))")
_r("plasma_frequency", "formula", formula="omega_p = sqrt(n*e^2/(eps_0*m))")
_r("cyclotron_frequency", "formula", formula="omega_c = qB/m")
_r("plasma_beta", "formula", formula="beta = 2*mu_0*n*kT/B^2")
_r("coulomb_logarithm", "formula", formula="ln(Lambda) = ln(lambda_D/b_min)")
_r("mhd_alfven", "formula", formula="v_A = B/sqrt(mu_0*rho)")

# -- Tier 5: Polymer science
_r("molecular_weight_avg", "formula", formula="Mn = sum(Ni*Mi)/sum(Ni), Mw = sum(Ni*Mi^2)/sum(Ni*Mi)")
_r("end_to_end_distance", "formula", formula="<r^2> = n*l^2 freely jointed chain")
_r("viscosity_intrinsic", "formula", formula="[eta] = K * M^a Mark-Houwink")

# -- Tier 5: Power systems
_r("three_phase_power", "formula", formula="P = sqrt(3)*V_L*I_L*cos(phi)")

# -- Tier 5: Probability
_r("poisson_approximation", "formula", formula="Binomial -> Poisson when n large, p small")
_r("clt_application", "library", library="scipy", function="scipy.stats.norm",
   pypi="scipy>=1.11")
_r("mixture_distribution", "library", library="scipy", function="scipy.stats",
   pypi="scipy>=1.11", notes="weighted sum of component PDFs")
_r("hazard_rate", "formula", formula="h(t) = f(t) / (1 - F(t))")
_r("generating_function_prob", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")
_r("branching_process", "formula", formula="extinction probability from PGF")
_r("exponential_dist", "library", library="scipy", function="scipy.stats.expon",
   pypi="scipy>=1.11")
_r("normal_dist_compute", "library", library="scipy", function="scipy.stats.norm",
   pypi="scipy>=1.11")
_r("joint_probability", "library", library="numpy", function="joint probability table",
   pypi="numpy>=1.24")
_r("covariance_correlation", "library", library="numpy", function="numpy.cov / numpy.corrcoef",
   pypi="numpy>=1.24")
_r("order_statistics", "library", library="scipy", function="scipy.stats order stats",
   pypi="scipy>=1.11")
_r("transformation_rv", "library", library="sympy", function="change of variable formula",
   pypi="sympy>=1.12")
_r("gamma_dist", "library", library="scipy", function="scipy.stats.gamma",
   pypi="scipy>=1.11")

# -- Tier 5: Pure math
_r("complex_division", "library", library="builtins", function="complex division",
   pypi="(stdlib)")

# -- Tier 5: Quantum
_r("euler_formula", "formula", formula="e^(ix) = cos(x) + i*sin(x)")
_r("qubit_measure", "library", library="numpy", function="|alpha|^2 + |beta|^2 = 1",
   pypi="numpy>=1.24")
_r("born_rule", "formula", formula="P = |<psi|phi>|^2")
_r("hydrogen_orbitals", "formula", formula="E_n = -13.6/n^2 eV")
_r("spin_half", "formula", formula="Pauli matrices spin-1/2")
_r("angular_momentum_qn", "formula", formula="l=0..n-1, m=-l..l")
_r("hydrogen_energy", "formula", formula="E_n = -13.6/n^2 eV")

# -- Tier 5: Queuing theory
_r("erlang_b", "formula", formula="B(N,A) = A^N/N! / sum(A^k/k!)")
_r("erlang_c", "formula", formula="C(N,A) probability of queuing")
_r("priority_queue", "formula", formula="priority-based service discipline")

# -- Tier 5: Real analysis
_r("sequence_convergence", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("supremum_infimum", "library", library="sympy", function="sympy.calculus.util",
   pypi="sympy>=1.12")

# -- Tier 5: Relativity
_r("spacetime_interval", "formula", formula="ds^2 = -c^2*dt^2 + dx^2 + dy^2 + dz^2")
_r("velocity_addition", "formula", formula="u = (v+w)/(1+vw/c^2)")
_r("relativistic_momentum", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="p = gamma*m*v")
_r("mass_energy_equivalence", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="E = mc^2")
_r("relativistic_doppler", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="f = f0*sqrt((1+beta)/(1-beta))")
_r("relativistic_kinetic", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="KE = (gamma-1)*mc^2")
_r("photon_momentum", "library", library="math", function="independent recomputation", pypi="(stdlib)", formula="p = h/lambda = E/c")

# -- Tier 5: RL
_r("bandit_ucb", "formula", formula="UCB = Q(a) + c*sqrt(ln(t)/N(a))")

# -- Tier 5: Robotics
_r("forward_kinematics", "library", library="numpy", function="DH matrix chain multiply",
   pypi="numpy>=1.24")
_r("path_planning", "formula", formula="A*/RRT path search")
_r("pid_control_robot", "formula", formula="u = Kp*e + Ki*int(e) + Kd*de/dt")
_r("dh_transform", "library", library="numpy", function="4x4 DH matrix",
   pypi="numpy>=1.24")
_r("potential_field", "formula", formula="attractive + repulsive potential gradient")
_r("sensor_fusion", "library", library="numpy", function="Kalman filter fusion",
   pypi="numpy>=1.24")
_r("trajectory_planning", "formula", formula="polynomial trajectory coefficients")
_r("workspace_analysis", "formula", formula="reachable workspace from joint limits")

# -- Tier 5: Semiconductor
_r("pn_junction", "formula", formula="V_bi = (kT/q)*ln(Na*Nd/ni^2)")
_r("mosfet_threshold", "formula", formula="Vth = Vfb + 2*phi_f + sqrt(2*eps*q*Na*2*phi_f)/Cox")
_r("diode_iv", "formula", formula="I = Is*(exp(V/nVt) - 1)")
_r("carrier_concentration", "formula", formula="n*p = ni^2, n = Nd (n-type)")
_r("depletion_width", "formula", formula="W = sqrt(2*eps*(V_bi-V)*(1/Na+1/Nd)/q)")

# -- Tier 5: Sequences
_r("recurrence_second_order", "library", library="sympy", function="sympy.solvers.recurr.rsolve",
   pypi="sympy>=1.12")
_r("power_series_eval", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")

# -- Tier 5: Signal processing
_r("sampling_theorem", "formula", formula="f_s >= 2*f_max Nyquist")
_r("convolution_continuous", "library", library="scipy", function="scipy.signal.convolve",
   pypi="scipy>=1.11")
_r("correlation_signal", "library", library="scipy", function="scipy.signal.correlate",
   pypi="scipy>=1.11")
_r("bode_plot_compute", "library", library="scipy", function="scipy.signal.bode",
   pypi="scipy>=1.11")
_r("modulation_demod", "formula", formula="AM/FM modulation/demodulation")
_r("sigma_delta", "formula", formula="oversampling + noise shaping")

# -- Tier 5: Solid state
_r("bragg_diffraction", "formula", formula="2*d*sin(theta) = n*lambda")
_r("band_gap", "formula", formula="Eg from absorption edge")
_r("hall_effect", "formula", formula="V_H = I*B/(n*e*t)")
_r("effective_mass", "formula", formula="m* = hbar^2 / (d^2E/dk^2)")
_r("density_of_states", "formula", formula="g(E) = (2m*)^(3/2)*sqrt(E)/(2*pi^2*hbar^3)")
_r("semiconductor_doping", "formula", formula="n = Nd, p = ni^2/Nd")
_r("magnetic_susceptibility", "formula", formula="chi = M/H, Curie/Pauli")
_r("crystal_momentum", "formula", formula="p = hbar*k")
_r("lattice_vibration", "formula", formula="omega = 2*sqrt(C/m)*|sin(ka/2)|")
_r("superconductor_tc", "formula", formula="BCS: Tc ~ theta_D*exp(-1/N(0)*V)")

# -- Tier 5: Spatial
_r("minimum_bounding_circle", "library", library="scipy", function="scipy.spatial",
   pypi="scipy>=1.11")
_r("plane_line_intersection", "library", library="numpy", function="parametric line + plane eq",
   pypi="numpy>=1.24")
_r("spherical_distance", "formula", formula="haversine: d = 2R*asin(sqrt(...))")
_r("rotation_3d", "library", library="numpy", function="rotation matrix multiply",
   pypi="numpy>=1.24")
_r("voronoi_cell", "library", library="scipy", function="scipy.spatial.Voronoi",
   pypi="scipy>=1.11")
_r("convex_hull_2d", "library", library="scipy", function="scipy.spatial.ConvexHull",
   pypi="scipy>=1.11")
_r("affine_transform", "library", library="numpy", function="matrix multiply + translate",
   pypi="numpy>=1.24")
_r("closest_pair", "formula", formula="divide and conquer closest pair")

# -- Tier 5: Spectroscopy
_r("wavelength_energy", "formula", formula="E = hc/lambda")
_r("nmr_splitting", "formula", formula="n+1 rule for multiplet")
_r("mass_spec_fragment", "reference", notes="fragmentation pattern analysis")
_r("ir_functional_group", "reference", notes="IR absorption frequency lookup")
_r("emission_spectrum", "formula", formula="1/lambda = R*(1/n1^2 - 1/n2^2)")
_r("nmr_chemical_shift", "reference", notes="delta ppm from TMS reference")
_r("nmr_integration", "formula", formula="integral ratio = proton count ratio")
_r("ir_interpretation", "reference", notes="IR peak assignment")
_r("uv_vis_absorption", "formula", formula="A = epsilon*l*c Beer-Lambert")
_r("coupling_constant", "formula", formula="J coupling in Hz from splitting pattern")
_r("mass_spec_isotope", "formula", formula="isotope pattern from natural abundance")
_r("raman_vs_ir", "reference", notes="mutual exclusion / selection rules")

# -- Tier 5: Statistical mechanics
_r("partition_function_stat", "formula", formula="Z = sum exp(-E_i/kT)")
_r("boltzmann_probability", "formula", formula="P_i = exp(-E_i/kT) / Z")
_r("fermi_dirac", "formula", formula="f(E) = 1/(exp((E-mu)/kT) + 1)")
_r("bose_einstein", "formula", formula="n(E) = 1/(exp((E-mu)/kT) - 1)")
_r("entropy_stat_mech", "formula", formula="S = k*ln(W) or S = -k*sum(p_i*ln(p_i))")
_r("equipartition", "formula", formula="<E> = (f/2)*kT per degree of freedom")

# -- Tier 5: Statistics
_r("markov_chain", "library", library="numpy", function="numpy.linalg.matrix_power",
   pypi="numpy>=1.24")
_r("multiple_regression", "library", library="numpy", function="numpy.linalg.lstsq",
   pypi="numpy>=1.24")
_r("logistic_regression_compute", "library", library="scipy", function="scipy.optimize.minimize",
   pypi="scipy>=1.11")
_r("residual_analysis", "library", library="numpy", function="y - X*beta residuals",
   pypi="numpy>=1.24")
_r("experimental_design_basic", "formula", formula="factorial design / blocking")
_r("fisher_exact_test", "library", library="scipy", function="scipy.stats.fisher_exact",
   pypi="scipy>=1.11")
_r("rank_correlation", "library", library="scipy", function="scipy.stats.spearmanr",
   pypi="scipy>=1.11")
_r("regression_prediction_interval", "library", library="scipy", function="scipy.stats.t",
   pypi="scipy>=1.11")
_r("categorical_analysis", "library", library="scipy", function="scipy.stats.chi2_contingency",
   pypi="scipy>=1.11")
_r("regression_diagnostics", "library", library="numpy", function="leverage/Cook's D",
   pypi="numpy>=1.24")
_r("two_sample_t", "library", library="scipy", function="scipy.stats.ttest_ind",
   pypi="scipy>=1.11")
_r("f_test", "library", library="scipy", function="scipy.stats.f_oneway",
   pypi="scipy>=1.11")
_r("goodness_of_fit", "library", library="scipy", function="scipy.stats.chisquare",
   pypi="scipy>=1.11")
_r("correlation_test", "library", library="scipy", function="scipy.stats.pearsonr",
   pypi="scipy>=1.11")
_r("power_analysis", "formula", formula="power = P(reject H0 | H1 true)")

# -- Tier 5: Stochastic processes
_r("random_walk", "formula", formula="E[X_n] = 0, Var[X_n] = n")
_r("markov_stationary", "library", library="numpy", function="numpy.linalg.eig",
   pypi="numpy>=1.24", notes="stationary distribution from eigenvalue 1")
_r("poisson_process", "library", library="scipy", function="scipy.stats.poisson",
   pypi="scipy>=1.11")

# -- Tier 5: Structural engineering
_r("beam_deflection", "formula", formula="EI*d^4y/dx^4 = w(x)")
_r("truss_analysis", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24", notes="method of joints / sections")
_r("buckling_load", "formula", formula="P_cr = pi^2*EI/(KL)^2 Euler")
_r("shear_bending", "formula", formula="V and M diagrams from loading")

# -- Tier 5: Systems
_r("normalisation", "reference", notes="database normal form classification")
_r("sql_equivalence", "reference", notes="relational algebra equivalence")
_r("consistent_hashing", "formula", formula="hash ring mapping")
_r("vector_clock_update", "formula", formula="increment + merge rules")

# -- Tier 5: Systems biology
_r("hill_function", "formula", formula="f = x^n / (K^n + x^n)")
_r("metabolic_flux", "formula", formula="flux balance: S*v = 0")
_r("growth_rate_dilution", "formula", formula="mu = D at steady state")
_r("dose_response_hill", "formula", formula="E = Emax*D^n/(EC50^n+D^n)")

# -- Tier 5: Telecom
_r("shannon_limit", "formula", formula="C = B*log2(1 + SNR)")
_r("modulation_bpsk", "formula", formula="BER = Q(sqrt(2*Eb/N0))")
_r("link_budget", "formula", formula="P_rx = P_tx + G_tx - L_path + G_rx")
_r("antenna_gain", "formula", formula="G = 4*pi*Ae/lambda^2")
_r("ofdm_subcarrier", "formula", formula="subcarrier spacing = B/N")
_r("spread_spectrum", "formula", formula="processing gain = B_ss/B_info")

# -- Tier 5: Tensor analysis
_r("levi_civita", "formula", formula="epsilon_ijk = +1/-1/0 permutation symbol")

# -- Tier 5: Thermodynamics
_r("work_pv", "formula", formula="W = integral P dV")
_r("free_energy", "formula", formula="G = H - TS")
_r("adiabatic_process", "formula", formula="PV^gamma = const")
_r("stirling_cycle", "formula", formula="eta = 1 - T_cold/T_hot (ideal)")
_r("joule_expansion", "formula", formula="free expansion: dT = 0 (ideal gas)")
_r("debye_temperature", "formula", formula="C_v = 9Nk(T/theta_D)^3 * integral")
_r("availability_exergy", "formula", formula="Ex = (H-H0) - T0*(S-S0)")
_r("diesel_cycle", "formula", formula="eta = 1 - (1/r^(gamma-1))*(rc^gamma-1)/(gamma*(rc-1))")
_r("entropy_mixing", "formula", formula="dS_mix = -nR*sum(x_i*ln(x_i))")
_r("otto_cycle", "formula", formula="eta = 1 - 1/r^(gamma-1)")
_r("throttling_process", "formula", formula="h1 = h2 isenthalpic")
_r("van_der_waals", "formula", formula="(P + a/V^2)(V-b) = nRT")

# -- Tier 5: Time series
_r("autocorrelation", "library", library="numpy", function="numpy.correlate",
   pypi="numpy>=1.24")
_r("seasonal_decompose", "library", library="scipy", function="scipy.signal",
   pypi="scipy>=1.11")
_r("stationarity_check", "formula", formula="ADF test / KPSS test")

# -- Tier 5: Topology
_r("euler_characteristic", "formula", formula="chi = V - E + F")

# -- Tier 5: Tribology
_r("wear_rate", "formula", formula="Archard: V = K*W*L/H")
_r("lubrication_regime", "formula", formula="Stribeck curve / lambda ratio")
_r("hertz_contact", "formula", formula="a = (3FR/4E*)^(1/3)")

# -- Tier 5: Trigonometry
_r("hyperbolic_functions", "library", library="math", function="math.sinh/cosh/tanh",
   pypi="(stdlib)")
_r("inverse_hyperbolic", "library", library="math", function="math.asinh/acosh/atanh",
   pypi="(stdlib)")
_r("trig_substitution", "library", library="sympy", function="sympy.integrate with trig sub",
   pypi="sympy>=1.12")

# -- Tier 5: Wavelet theory
_r("haar_wavelet_decompose", "library", library="numpy", function="Haar DWT coefficients",
   pypi="numpy>=1.24")
_r("haar_reconstruct", "library", library="numpy", function="Haar IDWT",
   pypi="numpy>=1.24")
_r("thresholding", "formula", formula="hard/soft threshold on coefficients")
_r("wavelet_energy", "library", library="numpy", function="sum(c_j^2) per level",
   pypi="numpy>=1.24")


# =========================================================================
# TIER 6 -- Remaining (advanced science, pure math, graduate-level)
# =========================================================================

# -- Tier 6: Abstract algebra
_r("cyclic_group_gen", "library", library="sympy", function="sympy.combinatorics.CyclicGroup",
   pypi="sympy>=1.12")
_r("normal_subgroup", "library", library="sympy", function="sympy.combinatorics.PermutationGroup.is_normal",
   pypi="sympy>=1.12")
_r("quotient_group", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")
_r("kernel_compute", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12", notes="kernel of group homomorphism")
_r("isomorphism_check", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")
_r("ring_ideal_check", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12")
_r("field_extension", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12")
_r("conjugacy_class", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")
_r("group_action", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")
_r("chinese_remainder_rings", "library", library="sympy", function="sympy.ntheory.crt",
   pypi="sympy>=1.12")
_r("euclidean_domain", "library", library="sympy", function="sympy.polys.gcd",
   pypi="sympy>=1.12")
_r("free_group", "library", library="sympy", function="sympy.combinatorics.free_groups",
   pypi="sympy>=1.12")
_r("automorphism_group", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")

# -- Tier 6: Actuarial
_r("compound_poisson", "library", library="scipy", function="scipy.stats.poisson",
   pypi="scipy>=1.11", notes="N~Poisson, X_i~severity")

# -- Tier 6: Advanced analysis
_r("diff_equation", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12")
_r("lagrange_multiplier", "library", library="sympy", function="sympy.solve",
   pypi="sympy>=1.12")
_r("quadratic_residue", "library", library="sympy", function="sympy.ntheory.is_quad_residue",
   pypi="sympy>=1.12")
_r("continued_fraction", "library", library="sympy", function="sympy.ntheory.continued_fraction",
   pypi="sympy>=1.12")
_r("diophantine", "library", library="sympy", function="sympy.solvers.diophantine",
   pypi="sympy>=1.12")

# -- Tier 6: Advanced economics
_r("utility_maximise", "library", library="scipy", function="scipy.optimize.minimize",
   pypi="scipy>=1.11")

# -- Tier 6: Advanced graph theory
_r("graph_isomorphism", "library", library="networkx", function="networkx.is_isomorphic",
   pypi="networkx>=3.1")
_r("hamiltonian_check", "library", library="networkx", function="networkx.tournament.hamiltonian_path",
   pypi="networkx>=3.1")
_r("vertex_cover", "library", library="networkx", function="networkx.approximation.min_weighted_vertex_cover",
   pypi="networkx>=3.1")
_r("independent_set", "library", library="networkx", function="networkx.approximation.maximum_independent_set",
   pypi="networkx>=3.1")
_r("network_flow_mincut", "library", library="networkx", function="networkx.minimum_cut",
   pypi="networkx>=3.1")
_r("topological_ordering", "library", library="networkx", function="networkx.topological_sort",
   pypi="networkx>=3.1")

# -- Tier 6: Advanced ML
_r("attention_multihead", "library", library="numpy", function="multi-head QKV attention",
   pypi="numpy>=1.24")
_r("contrastive_loss", "formula", formula="-log(exp(sim(z_i,z_j)/tau) / sum(exp(sim/tau)))")
_r("transformer_flops", "formula", formula="12*L*H*d^2 + 6*L*H*n*d FLOPs")

# -- Tier 6: Advanced probability
_r("moment_generating", "library", library="sympy", function="sympy.integrate(exp(tx)*f(x))",
   pypi="sympy>=1.12")
_r("characteristic_function_prob", "library", library="sympy", function="sympy.integrate(exp(itx)*f(x))",
   pypi="sympy>=1.12")
_r("central_limit", "library", library="scipy", function="scipy.stats.norm",
   pypi="scipy>=1.11")
_r("conditional_expectation", "library", library="numpy", function="E[X|Y] computation",
   pypi="numpy>=1.24")
_r("concentration_inequality", "formula", formula="Hoeffding/Chebyshev/Markov bounds")

# -- Tier 6: Aerospace
_r("hohmann_transfer", "formula", formula="delta_v = sqrt(GM/r1)*(sqrt(2*r2/(r1+r2))-1) + ...")

# -- Tier 6: AI/ML
_r("bellman_equation", "formula", formula="V(s) = max_a [R(s,a) + gamma*sum P*V(s')]")
_r("q_value_update", "formula", formula="Q(s,a) += alpha*(r + gamma*max Q(s') - Q(s,a))")
_r("policy_gradient", "formula", formula="grad J = E[grad log pi * G_t]")

# -- Tier 6: Algebra deep
_r("sylow_theorem", "library", library="sympy", function="sympy.combinatorics.PermutationGroup.sylow_subgroup",
   pypi="sympy>=1.12")
_r("quotient_ring", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12")
_r("polynomial_irreducibility", "library", library="sympy", function="Poly.is_irreducible",
   pypi="sympy>=1.12")
_r("splitting_field", "library", library="sympy", function="sympy.polys.splitting_field",
   pypi="sympy>=1.12")
_r("group_presentation", "library", library="sympy", function="sympy.combinatorics.free_groups",
   pypi="sympy>=1.12")
_r("smith_normal_form", "library", library="sympy", function="sympy.matrices.Matrix.smith_normal_form",
   pypi="sympy>=1.12")
_r("tensor_product_modules", "library", library="sympy", function="sympy.physics.quantum.TensorProduct",
   pypi="sympy>=1.12")
_r("exterior_algebra", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12")

# -- Tier 6: Algebraic geometry
_r("variety_points", "library", library="sympy", function="sympy.solvers.solve",
   pypi="sympy>=1.12", notes="solutions of polynomial system")
_r("bezout_intersection", "formula", formula="deg(f)*deg(g) intersection count")
_r("elliptic_curve_group_law", "library", library="sympy", function="sympy.ntheory.ecm",
   pypi="sympy>=1.12")
_r("projective_coords", "formula", formula="[x:y:z] homogeneous coordinates")
_r("rational_points", "library", library="sympy", function="sympy.solvers",
   pypi="sympy>=1.12")
_r("tangent_line_variety", "library", library="sympy", function="sympy.diff + gradient",
   pypi="sympy>=1.12")

# -- Tier 6: Algebraic number theory
_r("norm_trace_field", "library", library="sympy", function="sympy.polys.numberfields",
   pypi="sympy>=1.12")
_r("ring_of_integers", "library", library="sympy", function="sympy.polys.numberfields",
   pypi="sympy>=1.12")
_r("p_adic_valuation", "library", library="sympy", function="sympy.ntheory.factorint",
   pypi="sympy>=1.12", notes="v_p(n) = exponent of p in factorisation")

# -- Tier 6: Algorithm patterns
_r("amortised_analysis", "formula", formula="aggregate / accounting / potential method")
_r("dp_optimal_substructure", "reference", notes="DP correctness proof structure")
_r("approximation_ratio", "formula", formula="ALG/OPT ratio bound")
_r("randomised_algorithm", "formula", formula="expected runtime / success probability")

# -- Tier 6: Analysis extensions
_r("bolzano_weierstrass", "reference", notes="bounded sequence has convergent subsequence")
_r("weierstrass_mtest", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12", notes="uniform convergence from M_n bound")
_r("abel_summation", "library", library="sympy", function="sympy.summation",
   pypi="sympy>=1.12")
_r("integral_test", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("contraction_mapping", "formula", formula="Lipschitz constant < 1 implies fixed point")

# -- Tier 6: Analytical mechanics
_r("euler_lagrange_mechanics", "library", library="sympy", function="sympy.physics.mechanics",
   pypi="sympy>=1.12")
_r("hamiltonian", "library", library="sympy", function="H = sum p_i*q_dot_i - L",
   pypi="sympy>=1.12")
_r("hamilton_equations", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12")
_r("phase_space", "formula", formula="(q, p) trajectory in phase space")
_r("normal_modes", "library", library="numpy", function="numpy.linalg.eigvals",
   pypi="numpy>=1.24", notes="eigenfrequencies of coupled oscillators")

# -- Tier 6: Antenna theory
_r("array_factor", "library", library="numpy", function="sum(exp(j*k*d*n*cos(theta)))",
   pypi="numpy>=1.24")

# -- Tier 6: Applied science
_r("magnitude_distance", "formula", formula="m - M = 5*log10(d/10)")
_r("gravitational_lensing", "formula", formula="Einstein radius: theta_E = sqrt(4GM/(c^2*D))")

# -- Tier 6: Astronomy
_r("saha_equation", "formula", formula="N_{i+1}/N_i = (2/n_e)*(2*pi*m_e*kT/h^2)^(3/2)*exp(-chi/kT)")

# -- Tier 6: Automata
_r("pumping_lemma_cfl", "reference", notes="CFL pumping lemma application")

# -- Tier 6: Bayesian statistics
_r("conjugate_prior", "library", library="scipy", function="scipy.stats",
   pypi="scipy>=1.11", notes="conjugate posterior computation")
_r("posterior_predictive", "library", library="scipy", function="scipy.stats",
   pypi="scipy>=1.11")
_r("credible_interval", "library", library="scipy", function="scipy.stats.*.ppf",
   pypi="scipy>=1.11")
_r("bayes_factor", "formula", formula="BF = P(D|M1)/P(D|M2)")
_r("empirical_bayes", "library", library="scipy", function="scipy.optimize",
   pypi="scipy>=1.11")

# -- Tier 6: Biochemistry
_r("enzyme_inhibition", "formula", formula="competitive/uncompetitive/noncompetitive Ki models")
_r("allosteric_regulation", "formula", formula="MWC model / Hill equation")
_r("enzyme_kinetics_inhibition_ext", "formula", formula="extended inhibition kinetics")
_r("protein_folding_energy", "formula", formula="dG_folding = dH - TdS")

# -- Tier 6: Bioinformatics
_r("sequence_alignment", "formula", formula="Needleman-Wunsch / Smith-Waterman DP")

# -- Tier 6: Biostatistics
_r("meta_analysis", "library", library="scipy", function="scipy.stats",
   pypi="scipy>=1.11", notes="fixed/random effects pooled estimate")

# -- Tier 6: Bridge deep
_r("bayes_chain", "formula", formula="sequential Bayesian updating")
_r("group_homomorphism", "library", library="sympy", function="sympy.combinatorics",
   pypi="sympy>=1.12")

# -- Tier 6: Calculus deep
_r("stokes_theorem", "library", library="sympy", function="sympy.vector.Curl + integrate",
   pypi="sympy>=1.12")
_r("change_of_variables", "library", library="sympy", function="sympy.integrate with substitution",
   pypi="sympy>=1.12")
_r("contour_integral_real", "library", library="sympy", function="sympy.integrals.transforms",
   pypi="sympy>=1.12")
_r("vector_potential", "library", library="sympy", function="curl(A) = B",
   pypi="sympy>=1.12")
_r("greens_theorem", "library", library="sympy", function="sympy.vector",
   pypi="sympy>=1.12")
_r("improper_integral", "library", library="sympy", function="sympy.integrate with limits",
   pypi="sympy>=1.12")
_r("line_integral", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("surface_area_revolution", "library", library="sympy", function="2*pi*integrate(f*sqrt(1+f'^2))",
   pypi="sympy>=1.12")

# -- Tier 6: Causal inference
_r("propensity_score", "library", library="scipy", function="scipy.optimize (logistic)",
   pypi="scipy>=1.11")
_r("instrumental_variable", "formula", formula="2SLS estimator")
_r("regression_discontinuity", "formula", formula="local polynomial at cutoff")

# -- Tier 6: Chemistry deep
_r("reaction_mechanism_rate", "formula", formula="rate-determining step analysis")
_r("solubility_ph", "formula", formula="Henderson-Hasselbalch + Ksp")

# -- Tier 6: Classical mechanics
_r("two_body_problem", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")

# -- Tier 6: Coding theory
_r("bch_encode", "library", library="numpy", function="BCH generator polynomial",
   pypi="numpy>=1.24")
_r("reed_solomon", "library", library="numpy", function="RS encoding over GF(2^m)",
   pypi="numpy>=1.24")

# -- Tier 6: Cognitive science
_r("information_processing", "formula", formula="capacity-limited processing model")

# -- Tier 6: Combinatorial optimization
_r("assignment_problem", "library", library="scipy", function="scipy.optimize.linear_sum_assignment",
   pypi="scipy>=1.11")
_r("integer_programming", "library", library="scipy", function="scipy.optimize.milp",
   pypi="scipy>=1.11")

# -- Tier 6: Combinatorics deep
_r("exponential_gf", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12", notes="EGF coefficient extraction")
_r("polya_enumeration", "formula", formula="1/|G| * sum fix(g) Burnside/Polya")
_r("catalan_application", "formula", formula="C_n = (2n choose n)/(n+1)")

# -- Tier 6: Compilers
_r("ll1_parse_table", "reference", notes="LL(1) parse table construction")
_r("lambda_reduce", "reference", notes="beta-reduction / normal form")

# -- Tier 6: Complex analysis
_r("cauchy_riemann", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="u_x=v_y, u_y=-v_x")
_r("complex_power_series", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")
_r("residue_compute", "library", library="sympy", function="sympy.residue",
   pypi="sympy>=1.12")
_r("analytic_check", "library", library="sympy", function="Cauchy-Riemann check",
   pypi="sympy>=1.12")
_r("mobius_transform", "library", library="sympy", function="(az+b)/(cz+d) composition",
   pypi="sympy>=1.12")

# -- Tier 6: Compressed sensing
_r("basis_pursuit", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11")
_r("rip_condition", "formula", formula="restricted isometry property check")

# -- Tier 6: Computability
_r("godel_number", "formula", formula="prime power encoding")

# -- Tier 6: Computer graphics
_r("quaternion_rotate", "library", library="numpy", function="q*v*q^{-1}",
   pypi="numpy>=1.24")

# -- Tier 6: Continuum mechanics
_r("stress_tensor", "library", library="numpy", function="3x3 symmetric tensor",
   pypi="numpy>=1.24")
_r("strain_tensor", "library", library="numpy", function="symmetric gradient of displacement",
   pypi="numpy>=1.24")
_r("hookes_law_3d", "library", library="numpy", function="sigma = C : epsilon",
   pypi="numpy>=1.24")
_r("von_mises", "formula", formula="sigma_vm = sqrt(0.5*((s1-s2)^2+(s2-s3)^2+(s3-s1)^2))")

# -- Tier 6: Control theory
_r("stability_routh", "formula", formula="Routh array sign changes = RHP poles")
_r("state_space", "library", library="scipy", function="scipy.signal.StateSpace",
   pypi="scipy>=1.11")
_r("root_locus", "library", library="scipy", function="scipy.signal.rlocus (via control)",
   pypi="scipy>=1.11")
_r("gain_margin", "library", library="scipy", function="scipy.signal.bode",
   pypi="scipy>=1.11")
_r("phase_margin", "library", library="scipy", function="scipy.signal.bode",
   pypi="scipy>=1.11")
_r("controllability", "library", library="numpy", function="rank of controllability matrix",
   pypi="numpy>=1.24")
_r("observability", "library", library="numpy", function="rank of observability matrix",
   pypi="numpy>=1.24")
_r("pole_placement", "library", library="scipy", function="scipy.signal.place_poles",
   pypi="scipy>=1.11")

# -- Tier 6: Convex optimization
_r("dual_problem", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11")
_r("proximal_operator", "formula", formula="prox_f(x) = argmin(f(z) + 0.5||z-x||^2)")
_r("strong_duality", "formula", formula="p* = d* under Slater's condition")
_r("subgradient", "formula", formula="g in partial f(x)")
_r("barrier_method", "formula", formula="min f(x) + (1/t)*sum(-log(-f_i(x)))")

# -- Tier 6: Cryptography
_r("elliptic_curve_add", "library", library="sympy", function="sympy.ntheory",
   pypi="sympy>=1.12", notes="point addition on elliptic curve")
_r("digital_signature", "formula", formula="sign with private key, verify with public")
_r("aes_mixcolumn", "library", library="numpy", function="GF(2^8) matrix multiply",
   pypi="numpy>=1.24")
_r("meet_in_middle", "formula", formula="time-space tradeoff: O(2^(n/2))")
_r("elgamal_encrypt", "formula", formula="(g^k, m*h^k) mod p")
_r("dsa_sign", "formula", formula="(r, s) = (g^k mod p mod q, k^-1(H+xr) mod q)")
_r("zero_knowledge_basic", "formula", formula="ZK proof protocol")
_r("lattice_svp", "formula", formula="shortest vector in lattice")
_r("lwe_encrypt", "formula", formula="(A, As+e) learning with errors")
_r("ntru_keygen", "formula", formula="f*h = g mod q in Z[x]/(x^n-1)")
_r("oblivious_transfer", "formula", formula="1-out-of-2 OT protocol")
_r("garbled_circuit", "reference", notes="Yao's garbled circuit construction")

# -- Tier 6: CS foundations
_r("neural_forward", "library", library="numpy", function="W*x + b -> activation",
   pypi="numpy>=1.24")

# -- Tier 6: CS theory
_r("complexity_class", "reference", notes="P/NP/PSPACE/EXP classification")
_r("circuit_complexity", "formula", formula="circuit size/depth lower bounds")
_r("communication_complexity", "formula", formula="bits exchanged lower bound")
_r("randomised_complexity", "formula", formula="BPP/RP/ZPP classification")

# -- Tier 6: Decision theory
_r("bayesian_updating", "library", library="numpy", function="posterior = prior * likelihood / evidence",
   pypi="numpy>=1.24")
_r("value_of_information", "formula", formula="VoI = EU_with_info - EU_without")
_r("prospect_theory", "formula", formula="v(x) = x^a (gains), -lambda*(-x)^b (losses)")
_r("sequential_decision", "formula", formula="backward induction / DP")

# -- Tier 6: Differential equations
_r("variation_of_parameters", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12")
_r("laplace_solve_ode", "library", library="sympy", function="sympy.integrals.transforms.laplace_transform",
   pypi="sympy>=1.12")
_r("system_ode_matrix", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("boundary_value", "library", library="scipy", function="scipy.integrate.solve_bvp",
   pypi="scipy>=1.11")
_r("stability_ode", "library", library="numpy", function="numpy.linalg.eigvals for Jacobian",
   pypi="numpy>=1.24")
_r("exact_ode", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12")

# -- Tier 6: Differential geometry
_r("curvature_2d", "library", library="sympy", function="kappa = |f''|/(1+f'^2)^(3/2)",
   pypi="sympy>=1.12")
_r("arc_length_param", "library", library="sympy", function="sympy.integrate(|r'(t)|)",
   pypi="sympy>=1.12")
_r("tangent_normal", "library", library="sympy", function="r'(t) / |r'(t)|",
   pypi="sympy>=1.12")
_r("frenet_serret", "library", library="sympy", function="T,N,B from r(t)",
   pypi="sympy>=1.12")
_r("first_fundamental_form", "library", library="sympy", function="E,F,G from surface partials",
   pypi="sympy>=1.12")

# -- Tier 6: Dimensionality reduction
_r("svd_truncated", "library", library="numpy", function="numpy.linalg.svd",
   pypi="numpy>=1.24")

# -- Tier 6: Discrete math
_r("generating_function", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")
_r("burnside_counting", "formula", formula="1/|G| * sum |Fix(g)|")
_r("matroid_check", "reference", notes="independence axioms / rank function")
_r("chromatic_polynomial", "library", library="sympy", function="deletion-contraction",
   pypi="sympy>=1.12")
_r("partition_function", "library", library="sympy", function="number of partitions",
   pypi="sympy>=1.12")

# -- Tier 6: Distributed systems
_r("consensus_round", "formula", formula="round-based consensus protocol")
_r("two_phase_commit", "formula", formula="prepare-commit protocol")
_r("raft_election", "formula", formula="term/vote/log rules")
_r("byzantine_generals", "formula", formula="3f+1 nodes for f faults")

# -- Tier 6: Economics
_r("option_greeks", "library", library="scipy", function="scipy.stats.norm",
   pypi="scipy>=1.11", notes="delta/gamma/theta/vega from Black-Scholes")

# -- Tier 6: Electromagnetism
_r("rlc_impedance", "formula", formula="Z = R + j(wL - 1/wC)")
_r("ac_power", "formula", formula="P = Vrms*Irms*cos(phi)")
_r("maxwell_displacement", "formula", formula="curl H = J + dD/dt")
_r("displacement_current", "formula", formula="J_d = eps_0 * dE/dt")
_r("poynting_vector", "formula", formula="S = (1/mu_0) * E x B")
_r("biot_savart", "formula", formula="dB = (mu_0/4pi) * I*dl x r_hat / r^2")
_r("mutual_inductance", "formula", formula="M = mu_0*N1*N2*A/l")
_r("waveguide_cutoff", "formula", formula="f_c = c/(2a) for TE10 mode")

# -- Tier 6: Engineering
_r("nyquist_stability", "library", library="scipy", function="scipy.signal.freqresp",
   pypi="scipy>=1.11")
_r("kalman_gain", "library", library="numpy", function="K = P*H^T*(H*P*H^T+R)^-1",
   pypi="numpy>=1.24")

# -- Tier 6: Expanded core
_r("partial_deriv_multi", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12")
_r("matrix_power", "library", library="numpy", function="numpy.linalg.matrix_power",
   pypi="numpy>=1.24")
_r("system_ode", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("conv_2d", "library", library="scipy", function="scipy.signal.convolve2d",
   pypi="scipy>=1.11")

# -- Tier 6: Financial mathematics
_r("binomial_option", "formula", formula="CRR binomial tree: u=exp(sigma*sqrt(dt))")

# -- Tier 6: Fluid dynamics
_r("isentropic_flow", "formula", formula="T/T0 = (1 + (gamma-1)/2 * M^2)^(-1)")
_r("normal_shock", "formula", formula="M2^2 = (1+(gamma-1)/2*M1^2)/(gamma*M1^2-(gamma-1)/2)")

# -- Tier 6: Formal languages
_r("cfg_ambiguity", "reference", notes="two distinct parse trees for same string")
_r("chomsky_normal", "reference", notes="CNF conversion rules")
_r("pumping_lemma", "reference", notes="pumping lemma for regular languages")
_r("language_classify", "reference", notes="Chomsky hierarchy classification")

# -- Tier 6: Formal verification
_r("hoare_triple", "reference", notes="{P} S {Q} precondition/postcondition")
_r("wp_calculus", "library", library="sympy", function="weakest precondition substitution",
   pypi="sympy>=1.12")
_r("bisimulation_check", "reference", notes="bisimulation relation verification")

# -- Tier 6: Functional analysis
_r("banach_space_check", "reference", notes="completeness under norm")
_r("orthogonal_projection", "library", library="numpy", function="P = A(A^TA)^{-1}A^T",
   pypi="numpy>=1.24")
_r("adjoint_operator", "library", library="numpy", function="numpy.conj().T",
   pypi="numpy>=1.24")
_r("spectral_decomposition", "library", library="numpy", function="numpy.linalg.eigh",
   pypi="numpy>=1.24")
_r("dual_space", "reference", notes="dual space characterisation")
_r("operator_norm", "library", library="numpy", function="numpy.linalg.norm(A, 2)",
   pypi="numpy>=1.24")
_r("spectrum_compute", "library", library="numpy", function="numpy.linalg.eigvals",
   pypi="numpy>=1.24")
_r("resolvent", "library", library="numpy", function="(A - zI)^{-1}",
   pypi="numpy>=1.24")
_r("trace_class", "library", library="numpy", function="sum of singular values",
   pypi="numpy>=1.24")
_r("weak_convergence", "reference", notes="weak convergence criterion")

# -- Tier 6: Game theory
_r("bayesian_game", "formula", formula="Bayesian Nash equilibrium")
_r("correlated_equilibrium", "formula", formula="correlated strategy + incentive constraints")
_r("evolutionary_stable", "formula", formula="ESS: u(x,x) > u(y,x) condition")

# -- Tier 6: General relativity
_r("schwarzschild_metric", "formula", formula="ds^2 = -(1-2GM/rc^2)c^2dt^2 + dr^2/(1-2GM/rc^2) + r^2*dOmega^2")
_r("gravitational_redshift_gr", "formula", formula="1+z = sqrt(1-2GM/(rc^2))")
_r("gravitational_wave_strain", "formula", formula="h ~ (4GM/c^4)*(v/r)*d^2I/dt^2")
_r("cosmic_distance", "formula", formula="distance measures in FRW cosmology")

# -- Tier 6: Genetics
_r("mutation_selection", "formula", formula="q_eq = sqrt(mu/s) mutation-selection balance")
_r("coalescent_time", "formula", formula="E[T_k] = 4Ne/(k(k-1))")

# -- Tier 6: Graduate foundations
_r("knapsack", "formula", formula="0/1 knapsack DP")
_r("lcs", "formula", formula="longest common subsequence DP")
_r("lis", "formula", formula="longest increasing subsequence DP/patience sort")
_r("polynomial_multiply", "library", library="numpy", function="numpy.polymul / numpy.convolve",
   pypi="numpy>=1.24")

# -- Tier 6: Graphs
_r("network_flow_detail", "library", library="networkx", function="networkx.maximum_flow",
   pypi="networkx>=3.1")

# -- Tier 6: Harmonic analysis
_r("fourier_series_compute", "library", library="sympy", function="sympy.fourier_series",
   pypi="sympy>=1.12")
_r("parseval_theorem", "library", library="numpy", function="sum|c_n|^2 = (1/T)*integral|f|^2",
   pypi="numpy>=1.24")
_r("convolution_theorem", "library", library="numpy", function="F(f*g) = F(f)*F(g)",
   pypi="numpy>=1.24")
_r("windowed_fourier", "library", library="scipy", function="scipy.signal.stft",
   pypi="scipy>=1.11")
_r("wavelet_haar", "library", library="numpy", function="Haar wavelet coefficients",
   pypi="numpy>=1.24")
_r("spectral_density", "library", library="scipy", function="scipy.signal.welch",
   pypi="scipy>=1.11")
_r("spectral_leakage", "formula", formula="windowing effect on DFT")

# -- Tier 6: Information theory
_r("channel_capacity", "formula", formula="C = max_p(X) I(X;Y)")
_r("slepian_wolf", "formula", formula="R1+R2 >= H(X,Y) distributed source coding")
_r("multiple_access_channel", "formula", formula="capacity region from mutual info")
_r("rate_distortion_binary", "formula", formula="R(D) = H(p) - H(D) for BSC")
_r("polar_code", "formula", formula="channel polarisation + code construction")
_r("data_processing_inequality", "formula", formula="I(X;Y) >= I(X;Z) for X->Y->Z")
_r("rate_distortion", "formula", formula="R(D) = min I(X;X_hat) s.t. E[d] <= D")
_r("typical_set", "formula", formula="|A_eps| ~ 2^(nH(X))")

# -- Tier 6: Information geometry
_r("fisher_information", "library", library="sympy", function="E[(d log f / d theta)^2]",
   pypi="sympy>=1.12")
_r("kl_geometry", "library", library="scipy", function="scipy.stats.entropy",
   pypi="scipy>=1.11")
_r("exponential_family", "library", library="sympy", function="natural parameters",
   pypi="sympy>=1.12")

# -- Tier 6: Linear algebra
_r("change_of_basis", "library", library="numpy", function="P^{-1}*A*P",
   pypi="numpy>=1.24")
_r("jordan_form", "library", library="sympy", function="sympy.matrices.Matrix.jordan_form",
   pypi="sympy>=1.12")
_r("matrix_exponential", "library", library="scipy", function="scipy.linalg.expm",
   pypi="scipy>=1.11")
_r("singular_value_decomp", "library", library="numpy", function="numpy.linalg.svd",
   pypi="numpy>=1.24")

# -- Tier 6: Linguistics
_r("regular_language_check", "reference", notes="regular language closure properties")

# -- Tier 6: Logic deep
_r("ordinal_arithmetic", "reference", notes="ordinal addition/multiplication rules")
_r("cardinal_arithmetic", "reference", notes="cardinal exponentiation / Cantor's theorem")
_r("well_ordering", "reference", notes="well-ordering principle application")

# -- Tier 6: Logic extensions
_r("proof_by_induction_ext", "reference", notes="strong/structural induction")
_r("predicate_logic_validity", "library", library="sympy", function="sympy.logic.inference",
   pypi="sympy>=1.12")
_r("tarski_truth", "reference", notes="Tarski's truth definition / model theory")

# -- Tier 6: Mathematical logic
_r("first_order_satisfaction", "library", library="sympy", function="sympy.logic",
   pypi="sympy>=1.12")
_r("prenex_normal_form", "library", library="sympy", function="quantifier extraction",
   pypi="sympy>=1.12")
_r("satisfiability_check", "library", library="sympy", function="sympy.logic.inference.satisfiable",
   pypi="sympy>=1.12")
_r("clause_resolution", "library", library="sympy", function="sympy.logic",
   pypi="sympy>=1.12")

# -- Tier 6: Mathematical physics
_r("action_principle", "library", library="sympy", function="sympy.integrate (action functional)",
   pypi="sympy>=1.12")
_r("fourier_heat_kernel", "library", library="sympy", function="sympy.fourier_series",
   pypi="sympy>=1.12")

# -- Tier 6: Measure theory
_r("sigma_algebra", "reference", notes="sigma-algebra axiom verification")
_r("measurable_function", "reference", notes="preimage of Borel set is measurable")
_r("lebesgue_measure", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("simple_function_integral", "formula", formula="sum a_i * mu(A_i)")
_r("borel_set", "reference", notes="Borel sigma-algebra membership")
_r("outer_measure", "formula", formula="inf sum |I_n| covering by intervals")
_r("product_measure", "library", library="sympy", function="Fubini: iterated integral",
   pypi="sympy>=1.12")
_r("convergence_modes", "reference", notes="a.e./L^p/measure/distribution convergence")

# -- Tier 6: Medical imaging
_r("ct_backprojection", "library", library="numpy", function="filtered backprojection",
   pypi="numpy>=1.24")
_r("fourier_kspace", "library", library="numpy", function="numpy.fft.fft2",
   pypi="numpy>=1.24")

# -- Tier 6: ML deep
_r("cross_attention", "library", library="numpy", function="softmax(Q*K_ext^T/sqrt(d))*V_ext",
   pypi="numpy>=1.24")
_r("loss_landscape_local", "library", library="numpy", function="Hessian eigenvalues",
   pypi="numpy>=1.24")
_r("knowledge_distillation", "formula", formula="L = alpha*L_hard + (1-alpha)*KL(soft)")
_r("sparse_attention", "formula", formula="sparse attention mask pattern")

# -- Tier 6: ML theory
_r("kernel_trick", "library", library="numpy", function="K(x,y) = phi(x).phi(y)",
   pypi="numpy>=1.24")
_r("regularisation_path", "library", library="numpy", function="LASSO/ridge path",
   pypi="numpy>=1.24")
_r("bias_variance_decompose", "formula", formula="MSE = bias^2 + variance + irreducible")
_r("gradient_flow", "library", library="numpy", function="dW/dt = -grad L(W)",
   pypi="numpy>=1.24")

# -- Tier 6: Network science
_r("community_detect", "library", library="networkx", function="networkx.community",
   pypi="networkx>=3.1")

# -- Tier 6: Neuroscience
_r("hodgkin_huxley_gate", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="HH gating ODE system")
_r("cable_equation", "formula", formula="lambda*d^2V/dx^2 = tau*dV/dt + V")

# -- Tier 6: Nonlinear dynamics
_r("bifurcation_detect", "library", library="numpy", function="eigenvalue sign change at equilibrium",
   pypi="numpy>=1.24")
_r("lyapunov_exponent", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="log divergence rate of nearby trajectories")
_r("strange_attractor", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="Lorenz/Rossler attractor trajectory")
_r("fractal_dimension", "formula", formula="box-counting: D = lim log(N)/log(1/eps)")
_r("chaos_sensitivity", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="nearby trajectory divergence")

# -- Tier 6: Nuclear physics
_r("nuclear_reaction", "formula", formula="Q = (sum m_reactants - sum m_products)*c^2")
_r("nuclear_fission", "formula", formula="fission products + energy release")
_r("nuclear_fusion", "formula", formula="fusion products + energy release")

# -- Tier 6: Number theory
_r("wilson_theorem", "library", library="sympy", function="(p-1)! mod p == p-1",
   pypi="sympy>=1.12")
_r("chinese_remainder_ext", "library", library="sympy", function="sympy.ntheory.crt",
   pypi="sympy>=1.12")
_r("carmichael_number", "library", library="sympy", function="sympy.ntheory.isprime",
   pypi="sympy>=1.12")
_r("discrete_logarithm", "library", library="sympy", function="sympy.ntheory.discrete_log",
   pypi="sympy>=1.12")
_r("miller_rabin", "library", library="sympy", function="sympy.ntheory.isprime",
   pypi="sympy>=1.12")
_r("multiplicative_function", "library", library="sympy", function="sympy.ntheory",
   pypi="sympy>=1.12")
_r("sum_of_divisors_formula", "library", library="sympy", function="sympy.ntheory.divisor_sigma",
   pypi="sympy>=1.12")
_r("quadratic_reciprocity", "library", library="sympy", function="sympy.ntheory.legendre_symbol",
   pypi="sympy>=1.12")
_r("sum_of_squares", "library", library="sympy", function="sympy.ntheory.sum_of_squares",
   pypi="sympy>=1.12")
_r("divisor_function", "library", library="sympy", function="sympy.ntheory.divisor_count",
   pypi="sympy>=1.12")
_r("pell_equation", "library", library="sympy", function="sympy.solvers.diophantine",
   pypi="sympy>=1.12")
_r("order_element", "library", library="sympy", function="sympy.ntheory.n_order",
   pypi="sympy>=1.12")
_r("continued_fraction_convergent", "library", library="sympy", function="sympy.ntheory.continued_fraction_convergents",
   pypi="sympy>=1.12")
_r("dirichlet_character", "library", library="sympy", function="sympy.ntheory",
   pypi="sympy>=1.12")
_r("hensel_lift_ext", "library", library="sympy", function="Hensel lifting mod p^k",
   pypi="sympy>=1.12")
_r("mobius_inversion", "library", library="sympy", function="sympy.ntheory.mobius",
   pypi="sympy>=1.12")
_r("prime_counting", "library", library="sympy", function="sympy.ntheory.primepi",
   pypi="sympy>=1.12")

# -- Tier 6: Numerical methods
_r("gaussian_quadrature", "library", library="scipy", function="scipy.integrate.quadrature",
   pypi="scipy>=1.11")
_r("adams_bashforth", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("eigenvalue_power_iteration", "library", library="numpy", function="power method convergence",
   pypi="numpy>=1.24")
_r("nonlinear_system", "library", library="scipy", function="scipy.optimize.fsolve",
   pypi="scipy>=1.11")
_r("least_squares", "library", library="numpy", function="numpy.linalg.lstsq",
   pypi="numpy>=1.24")
_r("runge_kutta", "library", library="scipy", function="scipy.integrate.solve_ivp(method='RK45')",
   pypi="scipy>=1.11")
_r("lu_decomposition", "library", library="scipy", function="scipy.linalg.lu",
   pypi="scipy>=1.11")
_r("power_method", "library", library="numpy", function="iterative eigenvector",
   pypi="numpy>=1.24")
_r("condition_number", "library", library="numpy", function="numpy.linalg.cond",
   pypi="numpy>=1.24")

# -- Tier 6: Open problems
_r("euler_product", "library", library="sympy", function="product over primes",
   pypi="sympy>=1.12")
_r("goldbach_partition", "formula", formula="n = p1 + p2 search")
_r("twin_prime_search", "library", library="sympy", function="sympy.ntheory.nextprime",
   pypi="sympy>=1.12")
_r("erdos_straus", "formula", formula="4/n = 1/x + 1/y + 1/z search")
_r("legendre_prime", "library", library="sympy", function="primes in [n^2, (n+1)^2]",
   pypi="sympy>=1.12")
_r("abc_triple", "formula", formula="rad(abc) < c check")
_r("beal_check", "formula", formula="A^x + B^y = C^z with GCD>1 search")

# -- Tier 6: Operations research
_r("mmc_queue", "formula", formula="M/M/c queue: Erlang C formula")
_r("markov_decision", "library", library="numpy", function="value iteration / policy iteration",
   pypi="numpy>=1.24")

# -- Tier 6: Optics
_r("fabry_perot", "formula", formula="T = 1/(1 + F*sin^2(delta/2))")
_r("gaussian_beam", "formula", formula="w(z) = w0*sqrt(1+(z/z_R)^2)")

# -- Tier 6: Optimization
_r("simplex_step", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11")
_r("dual_lp", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11")
_r("convex_check", "library", library="numpy", function="Hessian positive semidefinite check",
   pypi="numpy>=1.24")
_r("kkt_conditions", "library", library="sympy", function="sympy.solve KKT system",
   pypi="sympy>=1.12")

# -- Tier 6: Organic chemistry
_r("reaction_product", "reference", notes="reaction mechanism product prediction")
_r("grignard_reaction", "reference", notes="RMgX + carbonyl product")
_r("aromatic_substitution", "reference", notes="EAS/NAS mechanism and product")
_r("spectroscopy_interpretation", "reference", notes="combined spectral analysis")

# -- Tier 6: Particle physics
_r("feynman_vertex", "formula", formula="vertex factor from Feynman rules")
_r("decay_width", "formula", formula="Gamma = |M|^2 * phase_space / (2*m)")
_r("invariant_mass", "formula", formula="m^2 = (sum E)^2 - |sum p|^2")

# -- Tier 6: PDE
_r("classify_pde", "reference", notes="elliptic/parabolic/hyperbolic from discriminant")
_r("heat_equation", "library", library="sympy", function="separation of variables",
   pypi="sympy>=1.12")
_r("wave_equation_1d", "library", library="sympy", function="d'Alembert solution",
   pypi="sympy>=1.12")
_r("finite_difference", "library", library="numpy", function="FD stencil matrix",
   pypi="numpy>=1.24")
_r("schrodinger_pde", "library", library="sympy", function="sympy.physics.quantum",
   pypi="sympy>=1.12")
_r("wave_damped", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("fem_1d", "library", library="numpy", function="stiffness matrix assembly + solve",
   pypi="numpy>=1.24")
_r("stability_cfl", "formula", formula="CFL: c*dt/dx <= 1")
_r("poisson_equation", "library", library="scipy", function="scipy.sparse.linalg.spsolve",
   pypi="scipy>=1.11")
_r("helmholtz_equation", "library", library="scipy", function="scipy.sparse.linalg",
   pypi="scipy>=1.11")
_r("advection_equation", "formula", formula="u_t + c*u_x = 0 upwind scheme")
_r("boundary_conditions_pde", "reference", notes="Dirichlet/Neumann/Robin BC types")
_r("eigenfunction_expansion", "library", library="sympy", function="sympy.series + orthogonal eigenfunctions",
   pypi="sympy>=1.12")
_r("crank_nicolson", "library", library="numpy", function="implicit FD scheme",
   pypi="numpy>=1.24")

# -- Tier 6: Persistent homology
_r("boundary_operator", "library", library="numpy", function="boundary matrix from simplicial complex",
   pypi="numpy>=1.24")
_r("betti_from_complex", "library", library="numpy", function="rank(ker) - rank(im)",
   pypi="numpy>=1.24")
_r("persistence_diagram", "formula", formula="birth-death pairs from filtration")
_r("bottleneck_distance", "formula", formula="inf sup matching distance")

# -- Tier 6: Pharmacology
_r("two_compartment_model", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("pk_nonlinear", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11", notes="Michaelis-Menten PK")

# -- Tier 6: Physical chemistry
_r("transition_state", "formula", formula="Eyring: k = (kT/h)*exp(-dG_ddagger/RT)")
_r("chemical_kinetics_mechanism", "formula", formula="steady-state / pre-equilibrium approximation")
_r("partition_function_chem", "formula", formula="q = sum g_i*exp(-E_i/kT)")

# -- Tier 6: Physics
_r("orbital_period", "formula", formula="T = 2*pi*sqrt(a^3/(GM))")
_r("stellar_luminosity", "formula", formula="L = 4*pi*R^2*sigma*T^4")

# -- Tier 6: Polymer science
_r("flory_huggins", "formula", formula="dG_mix/NkT = phi*ln(phi)/N + (1-phi)*ln(1-phi) + chi*phi*(1-phi)")

# -- Tier 6: Power systems
_r("power_factor_correction", "formula", formula="Q_c = P*(tan(phi1) - tan(phi2))")
_r("load_flow", "library", library="numpy", function="Newton-Raphson power flow",
   pypi="numpy>=1.24")

# -- Tier 6: Probability
_r("extreme_value", "library", library="scipy", function="scipy.stats.genextreme",
   pypi="scipy>=1.11")
_r("renewal_reward", "formula", formula="long-run rate = E[reward]/E[cycle]")
_r("multivariate_normal", "library", library="scipy", function="scipy.stats.multivariate_normal",
   pypi="scipy>=1.11")

# -- Tier 6: Proof theory
_r("resolution_refutation", "library", library="sympy", function="sympy.logic",
   pypi="sympy>=1.12")
_r("horn_clause", "formula", formula="definite clause / SLD resolution")

# -- Tier 6: Pure math
_r("integration_by_parts", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12")
_r("partial_fractions", "library", library="sympy", function="sympy.apart",
   pypi="sympy>=1.12")
_r("series_convergence", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")
_r("de_moivre", "formula", formula="(cos theta + i sin theta)^n = cos(n*theta) + i sin(n*theta)")
_r("group_order", "library", library="sympy", function="sympy.combinatorics.PermutationGroup.order",
   pypi="sympy>=1.12")
_r("fourier_coefficient", "library", library="sympy", function="sympy.integrate (a_n, b_n)",
   pypi="sympy>=1.12")
_r("tensor_product", "library", library="numpy", function="numpy.kron",
   pypi="numpy>=1.24")
_r("pauli_product", "library", library="numpy", function="2x2 Pauli matrix multiplication",
   pypi="numpy>=1.24")
_r("bloch_coords", "formula", formula="(theta, phi) on Bloch sphere")

# -- Tier 6: QFT basics
_r("field_lagrangian", "library", library="sympy", function="sympy.diff for EOM",
   pypi="sympy>=1.12")
_r("dimensional_analysis_qft", "formula", formula="mass dimension counting")
_r("symmetry_and_conservation", "reference", notes="Noether's theorem in QFT")

# -- Tier 6: Quantum
_r("quantum_gate", "library", library="numpy", function="unitary matrix multiplication",
   pypi="numpy>=1.24")
_r("time_evolution", "library", library="scipy", function="scipy.linalg.expm(-iHt)",
   pypi="scipy>=1.11")
_r("ladder_operators", "library", library="sympy", function="sympy.physics.quantum",
   pypi="sympy>=1.12")
_r("variational_method", "library", library="scipy", function="scipy.optimize.minimize",
   pypi="scipy>=1.11")
_r("scattering_cross_section", "formula", formula="d sigma / d Omega from scattering amplitude")
_r("wkb_approximation", "library", library="sympy", function="sympy.integrate for WKB phase",
   pypi="sympy>=1.12")
_r("expectation_value", "library", library="numpy", function="<psi|A|psi> matrix element",
   pypi="numpy>=1.24")
_r("harmonic_oscillator_qm", "formula", formula="E_n = hbar*omega*(n+1/2)")
_r("selection_rules", "formula", formula="delta_l = +/-1, delta_m = 0,+/-1")
_r("tunneling_probability", "formula", formula="T ~ exp(-2*kappa*a)")
_r("density_operator", "library", library="numpy", function="rho = |psi><psi|",
   pypi="numpy>=1.24")
_r("identical_particles", "formula", formula="symmetrisation / antisymmetrisation")
_r("two_level_system", "library", library="numpy", function="2x2 Hamiltonian diagonalisation",
   pypi="numpy>=1.24")
_r("commutator_compute", "library", library="numpy", function="[A,B] = AB - BA",
   pypi="numpy>=1.24")
_r("spin_addition", "formula", formula="Clebsch-Gordan: j = |j1-j2| to j1+j2")

# -- Tier 6: Quantum error correction
_r("bit_flip_code", "library", library="numpy", function="3-qubit repetition code",
   pypi="numpy>=1.24")
_r("phase_flip_code", "library", library="numpy", function="3-qubit phase flip code",
   pypi="numpy>=1.24")

# -- Tier 6: Quantum info
_r("bell_state", "library", library="numpy", function="tensor product + CNOT",
   pypi="numpy>=1.24")
_r("grover_step", "library", library="numpy", function="oracle + diffusion operator",
   pypi="numpy>=1.24")
_r("error_syndrome", "library", library="numpy", function="syndrome measurement",
   pypi="numpy>=1.24")
_r("density_matrix", "library", library="numpy", function="rho = sum p_i |psi_i><psi_i|",
   pypi="numpy>=1.24")
_r("quantum_circuit", "library", library="numpy", function="gate matrix chain",
   pypi="numpy>=1.24")
_r("quantum_measurement", "library", library="numpy", function="M_m^dag M_m probabilities",
   pypi="numpy>=1.24")
_r("quantum_entropy", "library", library="numpy", function="-tr(rho*log(rho)) von Neumann",
   pypi="numpy>=1.24")
_r("superdense_coding", "library", library="numpy", function="Bell state manipulation",
   pypi="numpy>=1.24")
_r("quantum_key_dist", "formula", formula="BB84 protocol key rate")
_r("quantum_walk", "library", library="numpy", function="unitary walk operator",
   pypi="numpy>=1.24")
_r("fidelity", "library", library="numpy", function="F = (tr sqrt(sqrt(rho)*sigma*sqrt(rho)))^2",
   pypi="numpy>=1.24")
_r("swap_test", "library", library="numpy", function="SWAP test circuit",
   pypi="numpy>=1.24")

# -- Tier 6: Queuing theory
_r("mg1_queue", "formula", formula="Pollaczek-Khinchine: Lq = lambda^2*E[S^2]/(2*(1-rho))")
_r("jackson_network", "formula", formula="product-form solution for open networks")

# -- Tier 6: Real analysis
_r("epsilon_delta", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("cauchy_sequence", "library", library="sympy", function="sympy.limit",
   pypi="sympy>=1.12")
_r("uniform_convergence", "library", library="sympy", function="sup|f_n - f| -> 0",
   pypi="sympy>=1.12")
_r("pointwise_vs_uniform", "library", library="sympy", function="convergence mode check",
   pypi="sympy>=1.12")
_r("ratio_test", "library", library="sympy", function="sympy.limit(a_{n+1}/a_n)",
   pypi="sympy>=1.12")
_r("root_test", "library", library="sympy", function="sympy.limit(a_n^(1/n))",
   pypi="sympy>=1.12")
_r("comparison_test", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12")
_r("alternating_series", "library", library="sympy", function="Leibniz test",
   pypi="sympy>=1.12")
_r("intermediate_value", "library", library="sympy", function="sympy.solve for root in [a,b]",
   pypi="sympy>=1.12")
_r("power_series_radius", "library", library="sympy", function="sympy.limit for ratio/root test",
   pypi="sympy>=1.12")

# -- Tier 6: Relativity
_r("lorentz_transform", "formula", formula="x'=gamma*(x-vt), t'=gamma*(t-vx/c^2)")
_r("four_momentum", "formula", formula="p^mu = (E/c, p)")
_r("twin_paradox", "formula", formula="proper time difference from worldlines")
_r("compton_scattering", "formula", formula="lambda'-lambda = (h/mc)(1-cos theta)")
_r("invariant_mass_two_particle", "formula", formula="m^2 = (E1+E2)^2 - |p1+p2|^2")

# -- Tier 6: Representation theory
_r("character_compute", "library", library="numpy", function="tr(rho(g)) for each g",
   pypi="numpy>=1.24")

# -- Tier 6: RL
_r("td_lambda", "formula", formula="V(s) += alpha*(G_t^lambda - V(s))")
_r("sarsa_update", "formula", formula="Q(s,a) += alpha*(r + gamma*Q(s',a') - Q(s,a))")
_r("policy_gradient_reinforce", "formula", formula="grad J = E[sum grad log pi * G_t]")

# -- Tier 6: Robotics
_r("inverse_kinematics", "library", library="numpy", function="Jacobian pseudoinverse",
   pypi="numpy>=1.24")
_r("kalman_update", "library", library="numpy", function="Kalman filter predict+update",
   pypi="numpy>=1.24")
_r("mdp_policy", "library", library="numpy", function="value/policy iteration",
   pypi="numpy>=1.24")
_r("jacobian_robot", "library", library="numpy", function="differential kinematics J(q)",
   pypi="numpy>=1.24")
_r("reward_shaping", "formula", formula="F(s,s') = gamma*Phi(s') - Phi(s)")

# -- Tier 6: Signal processing
_r("transfer_function_signal", "library", library="scipy", function="scipy.signal.TransferFunction",
   pypi="scipy>=1.11")
_r("frequency_response", "library", library="scipy", function="scipy.signal.freqresp",
   pypi="scipy>=1.11")
_r("nyquist_diagram", "library", library="scipy", function="scipy.signal.freqresp",
   pypi="scipy>=1.11")
_r("matched_filter", "library", library="scipy", function="scipy.signal.correlate",
   pypi="scipy>=1.11")

# -- Tier 6: Solid state
_r("reciprocal_lattice", "library", library="numpy", function="2*pi * cross products",
   pypi="numpy>=1.24")
_r("fermi_level", "formula", formula="E_F from electron count / DOS")
_r("phonon_dispersion", "formula", formula="omega(k) from dynamical matrix")
_r("debye_model", "formula", formula="C_v = 9Nk(T/theta_D)^3 * Debye integral")

# -- Tier 6: Spatial
_r("delaunay_check", "library", library="scipy", function="scipy.spatial.Delaunay",
   pypi="scipy>=1.11")

# -- Tier 6: Statistical mechanics
_r("average_energy", "formula", formula="<E> = -d(ln Z)/d(beta)")
_r("ising_model", "formula", formula="Z = sum exp(-beta*H) nearest-neighbor")
_r("specific_heat", "formula", formula="C = d<E>/dT")

# -- Tier 6: Statistics
_r("bayesian_credible_vs_ci", "formula", formula="credible vs confidence interval comparison")
_r("maximum_likelihood", "library", library="scipy", function="scipy.optimize.minimize(-logL)",
   pypi="scipy>=1.11")

# -- Tier 6: Stochastic processes
_r("markov_absorption", "library", library="numpy", function="(I-Q)^{-1} fundamental matrix",
   pypi="numpy>=1.24")
_r("birth_death", "formula", formula="detailed balance: lambda_n*p_n = mu_{n+1}*p_{n+1}")
_r("brownian_motion", "library", library="numpy", function="cumsum(sqrt(dt)*randn)",
   pypi="numpy>=1.24")
_r("sde_euler", "library", library="numpy", function="Euler-Maruyama scheme",
   pypi="numpy>=1.24")

# -- Tier 6: Systems biology
_r("gene_regulation", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("toggle_switch", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("oscillator_repressilator", "library", library="scipy", function="scipy.integrate.solve_ivp",
   pypi="scipy>=1.11")
_r("flux_balance", "library", library="scipy", function="scipy.optimize.linprog",
   pypi="scipy>=1.11", notes="S*v=0, max c^T*v")

# -- Tier 6: Tensor analysis
_r("tensor_contraction", "library", library="numpy", function="numpy.einsum",
   pypi="numpy>=1.24")
_r("metric_tensor", "library", library="sympy", function="g_ij from coordinate basis",
   pypi="sympy>=1.12")
_r("index_gymnastics", "library", library="numpy", function="g^{ij} raising/lowering",
   pypi="numpy>=1.24")

# -- Tier 6: Thermodynamics
_r("clausius_inequality", "formula", formula="integral dQ/T <= 0")
_r("heat_engine_cycle", "formula", formula="eta = W/Q_h = 1 - Q_c/Q_h")
_r("phase_transition", "reference", notes="first/second order phase transition classification")
_r("chemical_potential", "formula", formula="mu = (dG/dn)_{T,P}")
_r("fugacity", "formula", formula="f = phi*P, phi from equation of state")
_r("rankine_cycle", "formula", formula="eta = (h1-h2)/(h1-h4) with pump work")
_r("maxwell_relations", "formula", formula="(dT/dV)_S = -(dP/dS)_V etc.")

# -- Tier 6: Time series
_r("arima_forecast", "library", library="scipy", function="scipy.signal / statsmodels",
   pypi="scipy>=1.11")

# -- Tier 6: Topology
_r("open_closed_sets", "reference", notes="open/closed set classification in topology")
_r("closure_interior", "reference", notes="closure/interior/boundary computation")
_r("continuity_topological", "reference", notes="preimage of open set is open")
_r("connected_check", "reference", notes="path/connected classification")
_r("compactness_check", "reference", notes="Heine-Borel / open cover argument")
_r("path_connected", "reference", notes="path exists between any two points")
_r("product_topology", "reference", notes="product topology basis")
_r("quotient_space_compute", "formula", formula="equivalence class identification")
_r("nerve_theorem", "reference", notes="nerve of covering homotopy equivalent to space")
_r("cw_complex_euler", "formula", formula="chi = sum (-1)^k * #(k-cells)")
_r("homology_sphere", "reference", notes="homology sphere classification")
_r("suspension", "formula", formula="SX has H_n(SX) = H_{n-1}(X)")
_r("borsuk_ulam", "reference", notes="Borsuk-Ulam theorem application")
_r("covering_degree", "formula", formula="degree = |p^{-1}(x)| sheets")
_r("contractible_check", "reference", notes="null-homotopic identity")
_r("quotient_topology", "reference", notes="quotient topology identification")

# -- Tier 6: Wavelet theory
_r("multiresolution", "formula", formula="MRA: V_j subset V_{j+1}, scaling function")
_r("filter_bank", "library", library="numpy", function="analysis/synthesis filter bank",
   pypi="numpy>=1.24")

# =========================================================================
# TIER 7 -- Advanced mathematics & theoretical CS
# =========================================================================

# Complex analysis
_r("contour_integral", "library", library="sympy", function="sympy.residue",
   pypi="sympy>=1.12", notes="residue theorem: 2*pi*i * sum(residues)")
_r("laurent_series", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12", notes="Laurent expansion at singularity")
_r("poles_classify", "library", library="sympy", function="sympy.singularities",
   pypi="sympy>=1.12", notes="pole order from p/q factorisation")

# Algebra & number theory
_r("galois_group", "library", library="sympy", function="Poly.galois_group",
   pypi="sympy>=1.12", notes="Galois group of polynomial splitting field")
_r("ideal_membership", "library", library="sympy", function="sympy.polys.groebner",
   pypi="sympy>=1.12", notes="Groebner basis membership test")
_r("genus_compute", "formula", formula="g = (d-1)(d-2)/2 for smooth plane curve of degree d")
_r("class_number", "library", library="sympy", function="sympy.ntheory",
   pypi="sympy>=1.12", notes="class number of imaginary quadratic field")
_r("hensel_lift", "library", library="sympy", function="polynomial mod p^k",
   pypi="sympy>=1.12", notes="Newton-Hensel lift of root mod p")
_r("ideal_factorisation", "library", library="sympy", function="sympy.ntheory.legendre_symbol",
   pypi="sympy>=1.12", notes="prime ideal splitting via Legendre symbol")

# Differential geometry
_r("christoffel_symbol", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="Christoffel symbols from metric")
_r("gaussian_curvature", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="Gauss curvature from first/second fundamental forms")
_r("geodesic_equation", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="geodesic ODE from Christoffel symbols")
_r("mean_curvature", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="H = (eG - 2fF + gE) / 2(EG - F^2)")
_r("parallel_transport", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="transport via connection coefficients")
_r("second_fundamental_form", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="e, f, g from surface normal derivatives")

# Stochastic calculus & probability
_r("black_scholes", "library", library="scipy", function="scipy.stats.norm.cdf",
   pypi="scipy>=1.11", notes="C = S*N(d1) - K*e^(-rT)*N(d2)")
_r("geometric_brownian", "library", library="scipy", function="scipy.stats.lognorm",
   pypi="scipy>=1.11", notes="S_t = S_0 * exp((mu-sigma^2/2)t + sigma*B_t)")
_r("ito_lemma", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="df = f'dX + 0.5*f''*(dX)^2")
_r("ornstein_uhlenbeck", "formula",
   formula="E[X_t] = mu + (x0-mu)*e^(-theta*t), Var = sigma^2/(2*theta)*(1-e^(-2*theta*t))")
_r("martingale_transform", "library", library="numpy", function="numpy.cumsum",
   pypi="numpy>=1.24", notes="(H.M)_n = sum h_k * (M_k - M_{k-1})")
_r("martingale_check", "formula", formula="E[X_{n+1}|F_n] = X_n")
_r("large_deviation", "formula", formula="P(S_n/n >= a) <= e^{-n*I(a)} Chernoff bound")
_r("coupling_argument", "formula", formula="d_TV(P,Q) <= P(X != Y) for coupling (X,Y)")
_r("renewal_theory", "formula", formula="m(t) ~ t/E[X] elementary renewal theorem")

# PDEs
_r("fourier_transform_pde", "library", library="sympy",
   function="sympy.integrals.transforms.fourier_transform",
   pypi="sympy>=1.12", notes="Fourier solution of diffusion/wave PDE")
_r("greens_function", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12", notes="Green's function for linear PDE")
_r("laplace_equation", "library", library="sympy", function="sympy.series",
   pypi="sympy>=1.12", notes="series solution of Laplace equation")
_r("method_of_characteristics", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12", notes="PDE to ODE along characteristic curves")
_r("laplace_cylindrical", "library", library="sympy", function="sympy.functions.special.bessel",
   pypi="sympy>=1.12", notes="Bessel function separation of variables")
_r("nonlinear_pde_burger", "formula", formula="shock speed = (u_l + u_r)/2 Rankine-Hugoniot")
_r("spectral_method", "formula", formula="spectral coefficients from eigenfunction expansion")
_r("burgers_equation", "formula", formula="shock speed = (u_l + u_r)/2 Rankine-Hugoniot")
_r("variational_pde", "library", library="sympy", function="sympy.calculus.euler_equations",
   pypi="sympy>=1.12", notes="Euler-Lagrange equation")

# Mathematical physics
_r("green_function_ode", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12", notes="Green's function for boundary-value ODE")
_r("sturm_liouville", "library", library="sympy", function="sympy.dsolve",
   pypi="sympy>=1.12", notes="eigenvalue problem on interval")
_r("path_integral_simple", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12", notes="Gaussian path integral evaluation")
_r("variational_derivative", "library", library="sympy",
   function="sympy.calculus.euler_equations",
   pypi="sympy>=1.12", notes="Euler-Lagrange functional derivative")
_r("symmetry_generator", "library", library="sympy", function="sympy.solvers.ode",
   pypi="sympy>=1.12", notes="Lie symmetry infinitesimal generator")
_r("group_representation_physics", "formula",
   formula="Clebsch-Gordan: j1 x j2 = |j1-j2| + ... + j1+j2")

# Measure theory
_r("fubini_compute", "library", library="sympy", function="sympy.integrate",
   pypi="sympy>=1.12", notes="double integral via iterated integration")
_r("dominated_convergence", "formula",
   formula="lim integral f_n = integral lim f_n under domination")
_r("monotone_convergence", "formula",
   formula="lim integral f_n = integral lim f_n for increasing f_n >= 0")
_r("conditional_expectation_measure", "library", library="numpy",
   function="numpy.average (weighted)", pypi="numpy>=1.24",
   notes="E[X|G] = weighted sum over atoms")
_r("radon_nikodym", "formula", formula="dnu/dmu density function verification")

# Harmonic analysis
_r("laplace_inversion", "library", library="sympy",
   function="sympy.integrals.transforms.inverse_laplace_transform",
   pypi="sympy>=1.12")
_r("hilbert_transform", "library", library="sympy", function="sympy.integrals",
   pypi="sympy>=1.12", notes="Hilbert transform pairs table")

# General relativity
_r("einstein_tensor", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="G_uv = R_uv - 0.5*g_uv*R")
_r("cosmological_expansion", "formula", formula="H^2 = 8*pi*G*rho/3 Friedmann equation")
_r("geodesic_schwarzschild", "formula",
   formula="V_eff = -GM/r + L^2/(2r^2) - GML^2/(c^2*r^3)")
_r("perihelion_precession", "formula",
   formula="delta_phi = 6*pi*G*M/(c^2*a*(1-e^2))")

# ML theory
_r("pac_bound", "formula", formula="m >= (1/eps)*(ln|H| + ln(1/delta))")
_r("vc_dimension", "formula", formula="growth function shattering bound")
_r("rademacher_complexity", "formula", formula="R_n(F) <= max||w||*sqrt(sum||x_i||^2)/n")
_r("attention_complexity", "formula", formula="self-attn O(n^2*d), linear-attn O(n*d^2)")

# Quantum mechanics
_r("degenerate_perturbation", "library", library="numpy",
   function="numpy.linalg.eigvalsh", pypi="numpy>=1.24",
   notes="eigenvalues of 2x2 perturbation matrix")
_r("perturbation_first_order", "formula", formula="E_n^(1) = <n|V|n>")
_r("wigner_eckart", "formula",
   formula="triangle inequality |j-k| <= j' <= j+k for allowed transitions")
_r("entanglement_measure", "library", library="numpy",
   function="numpy.linalg.eigvalsh", pypi="numpy>=1.24",
   notes="von Neumann entropy S = -tr(rho*log(rho))")
_r("qft_compute", "library", library="numpy", function="numpy.fft.fft",
   pypi="numpy>=1.24", notes="quantum Fourier transform via DFT matrix")
_r("feynman_propagator", "library", library="sympy", function="sympy.residue",
   pypi="sympy>=1.12", notes="propagator via residue at poles")
_r("quantum_teleportation", "formula",
   formula="Bell measurement -> correction: {00:I, 01:X, 10:Z, 11:XZ}")
_r("no_cloning_proof", "formula",
   formula="<a|b> = <a|b>^2 => <a|b> in {0,1} => only orthogonal states")

# Quantum error correction
_r("logical_operators", "formula",
   formula="[L, S_i] = 0 for all stabilizers, {L_X, L_Z} anticommute")
_r("shor_code", "reference", notes="9-qubit code: 3 blocks of 3 for bit+phase flip")
_r("stabilizer_check", "formula",
   formula="valid stabilizer group iff all generators commute")
_r("steane_code", "reference", notes="CSS [7,1,3] code syndrome tables")

# Statistical mechanics
_r("grand_canonical", "formula",
   formula="Xi = sum_{N=0}^{inf} z^N * Z_N, z = e^{mu/kT}")

# Homological algebra
_r("betti_number", "reference", notes="known Betti numbers for standard spaces")
_r("chain_complex", "library", library="numpy", function="numpy.matmul",
   pypi="numpy>=1.24", notes="verify d1 @ d0 = 0")
_r("euler_characteristic_chain", "formula", formula="chi = sum(-1)^k * rank(C_k)")
_r("exact_sequence", "formula", formula="im(f) = ker(g) exactness check")
_r("homology_compute", "library", library="numpy", function="numpy.linalg.matrix_rank",
   pypi="numpy>=1.24", notes="H_k = ker(d_k)/im(d_{k+1}) via rank")
_r("free_resolution", "formula", formula="resolution length from module structure")

# Functional analysis
_r("compact_operator", "library", library="numpy",
   function="numpy.linalg.svd", pypi="numpy>=1.24",
   notes="singular values -> 0 for compact operator")
_r("hahn_banach_apply", "library", library="numpy", function="numpy.linalg.norm",
   pypi="numpy>=1.24", notes="extension preserves norm")
_r("riesz_representation", "library", library="numpy", function="numpy.inner",
   pypi="numpy>=1.24", notes="f(x) = <y, x> for unique y")
_r("closed_graph", "reference", notes="closed graph theorem application")
_r("compact_integral_operator", "formula", formula="Hilbert-Schmidt norm finite => compact")

# Representation theory
_r("character_table", "reference", notes="character tables for small finite groups")
_r("decompose_rep", "library", library="numpy", function="numpy.inner",
   pypi="numpy>=1.24", notes="multiplicity = <chi_V, chi_i> inner product")
_r("irreducible_check", "library", library="numpy", function="numpy.inner",
   pypi="numpy>=1.24", notes="irreducible iff <chi, chi> = 1")
_r("schur_lemma_apply", "library", library="numpy", function="numpy.inner",
   pypi="numpy>=1.24", notes="Hom(V,W) dim from character inner product")
_r("tensor_rep", "formula", formula="chi_{V tensor W}(g) = chi_V(g) * chi_W(g)")

# Analytical mechanics
_r("canonical_transform", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="Poisson bracket {Q,P} = 1 check")
_r("noether_theorem", "library", library="sympy", function="sympy.diff",
   pypi="sympy>=1.12", notes="conserved quantity from symmetry of Lagrangian")

# Tensor analysis & curvature
_r("covariant_derivative", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="nabla_j v^i = dv^i/dx^j + Gamma^i_{jk} v^k")
_r("ricci_tensor", "library", library="sympy", function="sympy.diffgeom",
   pypi="sympy>=1.12", notes="R_{ij} = R^k_{ikj} contraction of Riemann")

# Topology
_r("knot_invariant", "formula", formula="writhe = #positive - #negative crossings")
_r("simplicial_homology", "library", library="numpy",
   function="numpy.linalg.matrix_rank", pypi="numpy>=1.24",
   notes="rank of boundary matrices")
_r("fundamental_group", "reference", notes="known pi_1 for standard spaces")
_r("covering_space", "reference", notes="number of sheets from index [pi_1 : p_*(pi_1)]")
_r("homotopy_equivalence", "reference", notes="standard homotopy equivalences")
_r("manifold_classify", "reference", notes="classification by genus + orientability")
_r("homeomorphism_check", "formula",
   formula="bijection + open map check on finite topology")
_r("fixed_point_existence", "formula",
   formula="f(a)*f(b) < 0 => fixed point by IVT on g(x) = f(x) - x")
_r("surface_classification", "formula", formula="chi = 2 - 2g (orientable), 2-g (non-orientable)")
_r("degree_of_map", "formula", formula="deg(f) = sum of local degrees at preimages")
_r("homotopy_group_compute", "reference", notes="known homotopy groups for spheres, tori, etc.")
_r("deformation_retract", "reference", notes="standard deformation retracts")
_r("lefschetz_fixed_point", "formula", formula="L(f) = sum (-1)^k tr(f_{*k})")
_r("mapping_cone", "formula", formula="long exact sequence of cone -> homology")
_r("van_kampen", "formula",
   formula="pi_1(X) = pi_1(U) *_{pi_1(U cap V)} pi_1(V) amalgamated product")

# Algebraic topology
_r("cellular_homology", "library", library="numpy",
   function="numpy.linalg.matrix_rank", pypi="numpy>=1.24",
   notes="CW boundary matrices")
_r("cup_product", "formula", formula="alpha ^ beta in H^{p+q} graded ring")
_r("excision", "reference", notes="H_n(X,A) = H_n(X\\U, A\\U) excision theorem")
_r("lefschetz_number", "formula", formula="L(f) = sum (-1)^k tr(f_{*k})")
_r("long_exact_sequence", "reference", notes="connecting homomorphism delta")
_r("universal_coefficient", "formula",
   formula="H^n(X;G) = Hom(H_n,G) + Ext(H_{n-1},G)")

# Category theory
_r("morphism_compose", "formula", formula="composition table lookup in finite category")
_r("functor_apply", "formula", formula="F(g . f) = F(g) . F(f) and F(id) = id check")
_r("natural_transform", "formula", formula="eta_B . F(f) = G(f) . eta_A naturality square")
_r("product_category", "formula", formula="universal property: unique morphism to product")
_r("coproduct_category", "formula", formula="universal property: unique morphism from coproduct")
_r("limit_compute", "formula", formula="limit cone universal property check")
_r("adjunction_unit_counit", "formula", formula="triangle identities: eF . Fe = id, Ge . eG = id")
_r("abelian_category", "reference", notes="abelian category axiom check")
_r("enriched_category", "reference", notes="enriched category structure verification")
_r("monad_compute", "formula", formula="mu . T(mu) = mu . mu_T and mu . eta_T = id = mu . T(eta)")

# Computability & complexity
_r("halting_problem", "reference", notes="undecidability by diagonalisation argument")
_r("kolmogorov_complexity", "formula", formula="K(x) <= log2(n) + c")
_r("recursive_enumerable", "reference", notes="r.e. set classification")
_r("reduction_computability", "reference", notes="many-one reduction A <=_m B")
_r("rice_theorem", "reference", notes="non-trivial semantic property undecidable")
_r("np_reduction", "formula", formula="polynomial transformation preserving yes/no instances")
_r("greedy_proof", "reference", notes="matroid / exchange argument structure")
_r("np_completeness_proof", "reference", notes="NP membership + reduction from known NP-complete")
_r("online_algorithm", "formula", formula="competitive ratio = ALG_cost / OPT_cost")

# Logic & proof theory
_r("natural_deduction", "reference", notes="derivation via introduction/elimination rules")
_r("modal_logic", "formula", formula="Kripke model evaluation at world w")
_r("intuitionistic_logic", "reference", notes="constructive validity, no excluded middle")
_r("temporal_logic", "formula", formula="trace model checking for LTL/CTL")
_r("herbrand_universe", "formula", formula="ground terms from constants + function symbols")
_r("skolemisation", "formula",
   formula="exists x. P(x) -> P(f(...)) Skolem function substitution")
_r("tableau_proof", "reference", notes="analytic tableaux branch closure")
_r("soundness_completeness", "reference", notes="metalogical property verification")
_r("axiom_of_choice_app", "reference", notes="Zorn's lemma / well-ordering equivalent")
_r("transfinite_induction", "reference", notes="ordinal induction: base + successor + limit")
_r("zfc_axiom_apply", "reference", notes="set-theoretic construction from ZFC axioms")
_r("definability", "formula", formula="formula evaluation on finite structure")
_r("elementary_equivalence", "formula", formula="same first-order theory check")
_r("structure_check", "formula", formula="sentence truth in finite structure")

# Formal verification
_r("abstraction_refinement", "reference", notes="CEGAR loop structure")
_r("ctl_model_check", "formula", formula="CTL semantics on finite Kripke structure")
_r("invariant_synthesis", "reference", notes="Hoare logic invariant generation")
_r("loop_invariant_verify", "formula", formula="wp/sp weakest precondition check")
_r("ltl_to_buchi", "reference", notes="LTL formula to Buchi automaton construction")

# Miscellaneous tier 7
_r("strong_induction", "reference", notes="strong induction proof structure")
_r("do_calculus", "formula", formula="Pearl's do-calculus rules for interventional distributions")
_r("mechanism_design", "formula", formula="VCG payment = externality imposed on others")
_r("nonlinear_dynamics", "formula", formula="Poincare-Bendixson / Lienard criterion")
_r("limit_cycle", "formula", formula="Poincare-Bendixson theorem conditions")
_r("cross_section", "formula", formula="sigma = |M|^2 * phase_space_factor")
_r("symmetry_group", "reference", notes="gauge group identification from interactions")
_r("retrosynthesis", "reference", notes="disconnection approach for synthesis planning")
_r("information_geometry", "formula", formula="natural gradient = F^{-1} * grad")
_r("natural_gradient", "library", library="numpy", function="numpy.linalg.solve",
   pypi="numpy>=1.24", notes="Fisher matrix inversion for natural gradient step")

# QFT basics
_r("tree_level_amplitude", "formula", formula="product of vertex factors and propagators")
_r("vertex_factor", "formula", formula="coupling constant * combinatorial factor per vertex")

# Meta-reasoning tier 7 (classification)
_r("error_detection", "classification", notes="identify error in reasoning chain")
_r("error_correction", "classification", notes="fix error in reasoning chain")
_r("constraint_optimisation", "classification", notes="identify constraints and optimise")
_r("derive_identity", "classification", notes="derive mathematical identity")
_r("problem_construction", "classification", notes="construct problem with given properties")
_r("construct_polynomial", "classification", notes="build polynomial with specified roots/properties")
_r("counterexample", "classification", notes="find counterexample to false claim")
_r("derive_formula", "classification", notes="derive formula from conditions")
_r("estimate_magnitude", "classification", notes="order-of-magnitude estimation")
_r("generalise_sequence", "classification", notes="find general term of sequence")
_r("inverse_problem", "classification", notes="recover parameters from observations")
_r("method_selection", "classification", notes="choose appropriate solution method")
_r("proof_by_induction", "classification", notes="complete induction proof")
_r("sufficiency_analysis", "classification", notes="analyse sufficient conditions")
_r("dimensional_analysis", "classification", notes="verify dimensional consistency")
_r("symmetry_detection", "classification", notes="identify symmetries in problem")
_r("verify_proof", "classification", notes="check proof validity")
_r("approximation_bound", "classification", notes="bound approximation error")
_r("dimensional_check", "classification", notes="dimensional consistency verification")
_r("proof_strategy", "classification", notes="select proof strategy")

# =========================================================================
# TIER 8 -- Abstract algebra & advanced meta-reasoning
# =========================================================================

# Category theory & homological algebra
_r("adjunction_check", "formula", formula="triangle identities for unit/counit")
_r("yoneda_apply", "formula", formula="Nat(Hom(A,-), F) = F(A) Yoneda lemma")
_r("ext_functor", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12", notes="Ext group computation from free resolution")
_r("mayer_vietoris", "formula",
   formula="... -> H_n(A cap B) -> H_n(A) + H_n(B) -> H_n(X) -> ...")
_r("snake_lemma", "formula", formula="connecting morphism delta: ker(c) -> coker(a)")
_r("tor_functor", "library", library="sympy", function="sympy.polys",
   pypi="sympy>=1.12", notes="Tor group computation from free resolution")
_r("kan_extension", "formula", formula="universal property of left/right Kan extension")
_r("topos_basics", "reference", notes="topos axiom verification (subobject classifier)")

# Mathematical logic
_r("craig_interpolation", "formula",
   formula="if A => B, exists C in shared language with A => C => B")
_r("godel_incompleteness", "reference",
   notes="Godel sentence construction for consistent theory")
_r("compactness_apply", "formula",
   formula="finite subset satisfiability => full satisfiability")
_r("ultraproduct", "formula", formula="Los theorem: ultraproduct satisfies phi iff almost all do")
_r("sequent_calculus", "reference", notes="Gentzen sequent calculus proof search")

# Meta-reasoning tier 8 (classification)
_r("analogy_completion", "classification", notes="complete mathematical analogy")
_r("complexity_reduction", "classification", notes="reduce problem complexity")
_r("conjecture_generation", "classification", notes="generate plausible conjecture")
_r("cross_domain_transfer", "classification", notes="transfer method across domains")
_r("equation_construction", "classification", notes="construct equation with properties")
_r("isomorphism_detection", "classification", notes="detect structural isomorphism")
_r("problem_transformation", "classification", notes="transform problem to solvable form")
_r("self_evaluation", "classification", notes="evaluate own solution quality")
_r("minimal_axioms", "classification", notes="find minimal axiom set")
_r("novel_problem", "classification", notes="solve novel problem type")
_r("solution_elegance", "classification", notes="rate solution elegance")
_r("theorem_dependency", "classification", notes="identify theorem dependencies")
_r("error_taxonomy", "classification", notes="classify error types in reasoning")
_r("method_comparison", "classification", notes="compare solution methods")
_r("proof_synthesis", "classification", notes="synthesise proof from components")
_r("abstraction_level", "classification", notes="identify appropriate abstraction level")
_r("debugging_strategy", "classification", notes="select debugging approach for proof")
_r("proof_complexity", "classification", notes="estimate proof complexity")

# =========================================================================
# TIER 9 -- Meta-reasoning (all classification)
# =========================================================================

_r("complexity_analysis", "classification", notes="analyse computational complexity")
_r("hypothesis_design", "classification", notes="design testable hypothesis")
_r("learning_bound", "classification", notes="derive learning-theoretic bound")
_r("meta_pattern", "classification", notes="identify meta-level pattern")
_r("reduction", "classification", notes="reduce problem to known problem")
_r("representation_choice", "classification", notes="choose problem representation")
_r("research_methodology", "classification", notes="select research methodology")
_r("algorithm_correctness", "classification", notes="prove algorithm correctness")
_r("computational_tradeoff", "classification", notes="analyse computational tradeoffs")
_r("conjecture_test", "classification", notes="test mathematical conjecture")
_r("benchmark_design", "classification", notes="design evaluation benchmark")
_r("experiment_design_ml", "classification", notes="design ML experiment")
_r("transfer_learning_strategy", "classification", notes="select transfer learning approach")
_r("algorithm_design", "classification", notes="design algorithm for problem")
_r("algorithm_improvement", "classification", notes="improve existing algorithm")
_r("complexity_comparison", "classification", notes="compare algorithm complexities")
_r("failure_analysis", "classification", notes="analyse algorithm failure modes")
_r("impossibility_proof", "classification", notes="prove impossibility result")
_r("invariant_discovery", "classification", notes="discover loop/system invariant")
_r("abstraction_identify", "classification", notes="identify useful abstraction")
_r("algorithm_adapt", "classification", notes="adapt algorithm to new setting")
_r("complexity_lower_bound", "classification", notes="prove complexity lower bound")
_r("experiment_interpret", "classification", notes="interpret experimental results")
_r("failure_predict", "classification", notes="predict failure conditions")
_r("literature_gap_identify", "classification", notes="identify gap in literature")
_r("proof_generalize", "classification", notes="generalise existing proof")
_r("research_question_formulate", "classification", notes="formulate research question")
_r("convergence_proof", "classification", notes="prove convergence of iterative method")
_r("information_bottleneck", "classification", notes="apply information bottleneck principle")

# =========================================================================
# TIER 10 -- ML meta-reasoning (all classification)
# =========================================================================

_r("data_prescription", "classification", notes="prescribe data for training objective")
_r("efficiency_analysis", "classification", notes="analyse model efficiency")
_r("emergent_capability", "classification", notes="predict emergent capabilities")
_r("failure_mode_classification", "classification", notes="classify model failure modes")
_r("training_diagnosis", "classification", notes="diagnose training issues")
_r("model_architecture_critique", "classification", notes="critique model architecture choices")
_r("scaling_law_extrapolate", "classification", notes="extrapolate scaling laws")
_r("architecture_analysis", "classification", notes="analyse neural architecture properties")
_r("capacity_bound", "classification", notes="bound model capacity")
_r("gradient_analysis", "classification", notes="analyse gradient flow properties")
_r("loss_design", "classification", notes="design loss function for objective")
_r("scaling_prediction", "classification", notes="predict scaling behaviour")
_r("successor_design", "classification", notes="design improved successor model")
_r("architecture_search", "classification", notes="search architecture space")
_r("curriculum_design", "classification", notes="design training curriculum")
_r("loss_landscape", "classification", notes="analyse loss landscape geometry")
_r("architecture_ablation_design", "classification", notes="design architecture ablation study")
_r("compute_budget_allocate", "classification", notes="allocate compute budget optimally")
_r("data_augmentation_strategy", "classification", notes="select data augmentation strategy")
_r("evaluation_metric_design", "classification", notes="design evaluation metrics")
_r("objective_function_critique", "classification", notes="critique objective function choice")
_r("self_improvement_propose", "classification", notes="propose self-improvement mechanism")
_r("bottleneck_identification", "classification", notes="identify performance bottleneck")
_r("regularisation_design", "classification", notes="design regularisation strategy")

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
