"""Knowledge atoms for general relativity, decision theory, and numerical methods.

Registers atoms covering Schwarzschild geometry, cosmological expansion,
gravitational waves, expected utility, Bayesian updating, prospect theory,
numerical root-finding, integration, and matrix decomposition.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# -----------------------------------------------------------------------
# General Relativity (tier 6-7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="schwarzschild_metric",
    content=(
        "The Schwarzschild metric describes the geometry of spacetime "
        "around a spherically symmetric, non-rotating mass M. In "
        "Schwarzschild coordinates (t, r, theta, phi): "
        "ds^2 = -(1 - r_s/r)c^2 dt^2 + (1 - r_s/r)^{-1} dr^2 "
        "+ r^2 (d theta^2 + sin^2 theta d phi^2), where "
        "r_s = 2GM/c^2 is the Schwarzschild radius."
    ),
    example=(
        "Given M = 1 solar mass = 1.989e30 kg: "
        "r_s = 2 * 6.674e-11 * 1.989e30 / (3e8)^2 = 2954 m ~ 2.95 km"
    ),
    tier=6,
    domain="general_relativity",
    source="Wikipedia contributors, 'Schwarzschild metric', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Schwarzschild_metric",
    prerequisites=["gravitational_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="gravitational_redshift_gr",
    content=(
        "Gravitational redshift is the shift in frequency of light "
        "moving away from a gravitational source. For a photon emitted "
        "at radius r_e and observed at r_o in Schwarzschild geometry: "
        "1 + z = sqrt((1 - r_s/r_o) / (1 - r_s/r_e)), where "
        "r_s = 2GM/c^2. For weak fields: z ~ GM/(rc^2)."
    ),
    example=(
        "Given M = 1 solar mass, r_e = 6.96e8 m (surface), r_o -> inf: "
        "z = GM/(r_e c^2) = 6.674e-11 * 1.989e30 / (6.96e8 * 9e16) "
        "= 2.12e-6"
    ),
    tier=6,
    domain="general_relativity",
    source="Wikipedia contributors, 'Gravitational redshift', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gravitational_redshift",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="geodesic_schwarzschild",
    content=(
        "Geodesics in Schwarzschild spacetime describe the motion of "
        "freely falling particles and photons near a spherical mass. "
        "The effective potential for massive particles is "
        "V_eff(r) = -GM/r + L^2/(2r^2) - GML^2/(c^2 r^3), where "
        "L is specific angular momentum. Circular orbits require "
        "dV_eff/dr = 0; the innermost stable circular orbit (ISCO) "
        "is at r = 6GM/c^2 = 3 r_s."
    ),
    example=(
        "ISCO for M = 10 solar masses (black hole): "
        "r_ISCO = 6 * 6.674e-11 * 1.989e31 / (9e16) = 8.86e4 m = 88.6 km"
    ),
    tier=7,
    domain="general_relativity",
    source="Wikipedia contributors, 'Schwarzschild geodesics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Schwarzschild_geodesics",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="einstein_tensor",
    content=(
        "The Einstein field equations relate spacetime curvature to "
        "energy-momentum: G_{mu nu} + Lambda g_{mu nu} = "
        "(8 pi G / c^4) T_{mu nu}, where G_{mu nu} = R_{mu nu} - "
        "(1/2) R g_{mu nu} is the Einstein tensor, R_{mu nu} is the "
        "Ricci tensor, R is the scalar curvature, and T_{mu nu} is the "
        "stress-energy tensor."
    ),
    example=(
        "Vacuum solution (T_{mu nu} = 0, Lambda = 0): "
        "G_{mu nu} = 0, so R_{mu nu} = 0. The Schwarzschild metric "
        "is the unique spherically symmetric vacuum solution."
    ),
    tier=7,
    domain="general_relativity",
    source="Wikipedia contributors, 'Einstein field equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Einstein_field_equations",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="cosmological_expansion",
    content=(
        "The Friedmann equations describe the expansion of a "
        "homogeneous, isotropic universe. The first equation is "
        "(a_dot/a)^2 = (8 pi G / 3) rho - k c^2 / a^2 + Lambda c^2 / 3, "
        "where a(t) is the scale factor, rho is density, k is spatial "
        "curvature, and Lambda is the cosmological constant. "
        "The Hubble parameter H = a_dot / a."
    ),
    example=(
        "Current epoch: H_0 = 70 km/s/Mpc. Galaxy at d = 100 Mpc: "
        "recession velocity v = H_0 * d = 70 * 100 = 7000 km/s"
    ),
    tier=7,
    domain="general_relativity",
    source="Wikipedia contributors, 'Friedmann equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Friedmann_equations",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="gravitational_wave_strain",
    content=(
        "Gravitational waves are ripples in spacetime produced by "
        "accelerating masses. The strain amplitude for a compact "
        "binary system is h ~ (4 G M_c / c^4) * (pi f)^{2/3} / d, "
        "where M_c = (m1 m2)^{3/5} / (m1 + m2)^{1/5} is the chirp "
        "mass, f is the gravitational wave frequency, and d is the "
        "luminosity distance."
    ),
    example=(
        "Binary neutron stars (m1 = m2 = 1.4 M_sun) at d = 40 Mpc, "
        "f = 100 Hz: M_c = 1.22 M_sun, h ~ 1e-21"
    ),
    tier=6,
    domain="general_relativity",
    source="Wikipedia contributors, 'Gravitational wave', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gravitational_wave",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="perihelion_precession",
    content=(
        "General relativity predicts an additional precession of "
        "planetary orbits beyond Newtonian mechanics. The excess "
        "precession per orbit is delta_phi = 6 pi G M / (a (1 - e^2) c^2), "
        "where a is the semi-major axis and e is eccentricity. "
        "For Mercury: delta_phi = 42.98 arcseconds per century."
    ),
    example=(
        "Mercury: a = 5.79e10 m, e = 0.2056, M = 1.989e30 kg. "
        "delta_phi = 6 * pi * 6.674e-11 * 1.989e30 / "
        "(5.79e10 * (1 - 0.04227) * 9e16) = 5.02e-7 rad/orbit = "
        "42.98 arcsec/century"
    ),
    tier=7,
    domain="general_relativity",
    source="Wikipedia contributors, 'Tests of general relativity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tests_of_general_relativity",
    prerequisites=["schwarzschild_metric"],
))

register_atom(Atom(
    atom_type="formula",
    name="cosmic_distance",
    content=(
        "In an expanding universe, several distance measures exist. "
        "The luminosity distance is d_L = (1 + z) * d_C, where d_C "
        "is the comoving distance. For small z: d_L ~ cz/H_0. "
        "The angular diameter distance is d_A = d_C / (1 + z). "
        "These differ due to the expansion of space."
    ),
    example=(
        "Galaxy at z = 0.1, H_0 = 70 km/s/Mpc: "
        "d_L ~ c * 0.1 / H_0 = 3e5 * 0.1 / 70 = 428.6 Mpc"
    ),
    tier=6,
    domain="general_relativity",
    source="Wikipedia contributors, 'Distance measures (cosmology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Distance_measures_(cosmology)",
    prerequisites=["hubble_law"],
))


# -----------------------------------------------------------------------
# Decision Theory (tier 5-7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="expected_utility",
    content=(
        "The expected utility hypothesis states that a rational agent "
        "chooses the action that maximises EU(a) = sum_s P(s) * U(a, s), "
        "where P(s) is the probability of state s and U(a, s) is the "
        "utility of action a in state s. This framework underlies "
        "von Neumann-Morgenstern utility theory."
    ),
    example=(
        "Gamble: 60% chance of $100, 40% chance of $0 vs certain $50. "
        "EU(gamble) = 0.6 * 100 + 0.4 * 0 = 60. EU(certain) = 50. "
        "Risk-neutral agent chooses gamble (EU = 60 > 50)."
    ),
    tier=5,
    domain="decision_theory",
    source="Wikipedia contributors, 'Expected utility hypothesis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Expected_utility_hypothesis",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="definition",
    name="risk_dominance",
    content=(
        "Action A risk-dominates action B if A yields a higher expected "
        "payoff when the opponent's strategy is uncertain. In a 2x2 "
        "coordination game with equilibria (A,A) and (B,B), (A,A) "
        "risk-dominates if (a-c)(a-b) > (d-b)(d-c), where payoffs "
        "are u(A,A)=a, u(A,B)=b, u(B,A)=c, u(B,B)=d. Introduced by "
        "Harsanyi and Selten (1988)."
    ),
    example=(
        "Stag Hunt: u(Stag,Stag)=4, u(Stag,Hare)=0, u(Hare,Stag)=3, "
        "u(Hare,Hare)=3. (4-3)(4-0)=4 vs (3-0)(3-3)=0. "
        "Stag risk-dominates."
    ),
    tier=5,
    domain="decision_theory",
    source="Wikipedia contributors, 'Risk dominance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Risk_dominance",
    prerequisites=["expected_utility"],
))

register_atom(Atom(
    atom_type="formula",
    name="bayesian_updating",
    content=(
        "Bayesian updating revises beliefs upon observing evidence "
        "using Bayes' theorem: P(H|E) = P(E|H) * P(H) / P(E). "
        "Starting from a prior P(H), after observing data D, the "
        "posterior is proportional to the likelihood times the prior: "
        "P(H|D) proportional to P(D|H) * P(H)."
    ),
    example=(
        "Prior: P(disease) = 0.01. Test: sensitivity 0.95, "
        "specificity 0.90. P(+|disease) = 0.95, P(+|healthy) = 0.10. "
        "P(disease|+) = 0.95*0.01 / (0.95*0.01 + 0.10*0.99) = "
        "0.0095 / 0.1085 = 0.0876 (8.76%)"
    ),
    tier=6,
    domain="decision_theory",
    source="Wikipedia contributors, 'Bayesian inference', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bayesian_inference",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="formula",
    name="value_of_information",
    content=(
        "The value of perfect information (EVPI) is the maximum "
        "amount a decision maker should pay to learn the true state "
        "before deciding. EVPI = EU(with perfect info) - EU(without). "
        "EU(with perfect info) = sum_s P(s) * max_a U(a, s)."
    ),
    example=(
        "States: Rain (P=0.3), Sun (P=0.7). Actions: Umbrella "
        "(U=8 rain, U=6 sun), No umbrella (U=2 rain, U=10 sun). "
        "EU(umbrella) = 0.3*8 + 0.7*6 = 6.6. "
        "EU(no umbrella) = 0.3*2 + 0.7*10 = 7.6. Best = 7.6. "
        "EU(perfect) = 0.3*8 + 0.7*10 = 9.4. EVPI = 9.4 - 7.6 = 1.8"
    ),
    tier=6,
    domain="decision_theory",
    source="Wikipedia contributors, 'Value of information', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Value_of_information",
    prerequisites=["expected_utility"],
))

register_atom(Atom(
    atom_type="definition",
    name="multi_criteria",
    content=(
        "Multi-criteria decision analysis (MCDA) evaluates alternatives "
        "against multiple criteria. A weighted sum model scores each "
        "alternative as S(a) = sum_j w_j * v_j(a), where w_j is the "
        "weight of criterion j and v_j(a) is the normalised value of "
        "alternative a on criterion j. Weights sum to 1."
    ),
    example=(
        "Criteria: cost (w=0.4), quality (w=0.35), speed (w=0.25). "
        "Option A: cost=8, quality=6, speed=7. "
        "S(A) = 0.4*8 + 0.35*6 + 0.25*7 = 3.2 + 2.1 + 1.75 = 7.05"
    ),
    tier=5,
    domain="decision_theory",
    source="Wikipedia contributors, 'Multi-criteria decision analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multi-criteria_decision_analysis",
    prerequisites=["expected_utility"],
))

register_atom(Atom(
    atom_type="theorem",
    name="prospect_theory",
    content=(
        "Prospect theory (Kahneman and Tversky, 1979) models decisions "
        "under risk using a value function v(x) that is concave for "
        "gains, convex for losses, and steeper for losses (loss "
        "aversion). Decision weights pi(p) overweight small "
        "probabilities and underweight large ones. The value of a "
        "prospect is V = sum pi(p_i) * v(x_i)."
    ),
    example=(
        "Value function: v(x) = x^0.88 for gains, v(x) = -2.25*|x|^0.88 "
        "for losses. Gain of $100: v(100) = 100^0.88 = 57.5. "
        "Loss of $100: v(-100) = -2.25 * 100^0.88 = -129.5. "
        "Loss looms ~2.25x larger than equivalent gain."
    ),
    tier=6,
    domain="decision_theory",
    source="Wikipedia contributors, 'Prospect theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prospect_theory",
    prerequisites=["expected_utility"],
))

register_atom(Atom(
    atom_type="definition",
    name="sequential_decision",
    content=(
        "A sequential decision problem involves choices made over "
        "multiple stages where later decisions depend on earlier "
        "outcomes. Modelled as a decision tree or Markov decision "
        "process (MDP). Solved by backward induction: at each node, "
        "choose the action maximising expected value of subsequent "
        "subtree."
    ),
    example=(
        "Two-stage: invest (cost 10, then 50% chance of payoff 30, "
        "50% chance of 0) or don't invest (payoff 0). "
        "EU(invest) = -10 + 0.5*30 + 0.5*0 = 5. "
        "EU(don't) = 0. Choose invest."
    ),
    tier=6,
    domain="decision_theory",
    source="Wikipedia contributors, 'Decision tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Decision_tree",
    prerequisites=["expected_utility"],
))

register_atom(Atom(
    atom_type="definition",
    name="mechanism_design",
    content=(
        "Mechanism design is the study of designing rules (mechanisms) "
        "to achieve desired outcomes when agents have private "
        "information. A mechanism specifies a message space and an "
        "outcome function. Key results: the revelation principle "
        "(any mechanism can be replicated by a truthful direct "
        "mechanism) and the Vickrey-Clarke-Groves (VCG) mechanism "
        "for efficient allocation with dominant strategy incentive "
        "compatibility."
    ),
    example=(
        "Second-price auction (Vickrey): bidders submit sealed bids. "
        "Highest bidder wins but pays the second-highest bid. "
        "Bidder values: 10, 8, 5. Winner pays 8, not 10. "
        "Truthful bidding is a dominant strategy."
    ),
    tier=7,
    domain="decision_theory",
    source="Wikipedia contributors, 'Mechanism design', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mechanism_design",
    prerequisites=["expected_utility"],
))


# -----------------------------------------------------------------------
# Numerical Methods (tier 5-6)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="secant_method",
    content=(
        "The secant method finds roots of f(x) = 0 using two initial "
        "points. The iteration is x_{n+1} = x_n - f(x_n) * "
        "(x_n - x_{n-1}) / (f(x_n) - f(x_{n-1})). Unlike Newton's "
        "method, it does not require computing the derivative. "
        "The order of convergence is the golden ratio phi ~ 1.618."
    ),
    example=(
        "f(x) = x^2 - 2, x0 = 1, x1 = 2. "
        "x2 = 2 - 2*(2-1)/(2-(-1)) = 2 - 2/3 = 1.3333. "
        "x3 = 1.3333 - (-0.2222)*(1.3333-2)/((-0.2222)-2) = 1.4"
    ),
    tier=5,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Secant method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Secant_method",
    prerequisites=["newton_raphson"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="fixed_point_iteration",
    content=(
        "Fixed-point iteration solves x = g(x) by iterating "
        "x_{n+1} = g(x_n). Converges if |g'(x*)| < 1 at the fixed "
        "point x*. The rate of convergence is linear with ratio "
        "|g'(x*)|. To solve f(x) = 0, rewrite as x = g(x) = x - f(x)."
    ),
    example=(
        "Solve x = cos(x). g(x) = cos(x). x0 = 1. "
        "x1 = cos(1) = 0.5403. x2 = cos(0.5403) = 0.8576. "
        "x3 = cos(0.8576) = 0.6543. Converges to x* = 0.7391."
    ),
    tier=5,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Fixed-point iteration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fixed-point_iteration",
    prerequisites=["newton_raphson"],
))

register_atom(Atom(
    atom_type="formula",
    name="simpson_rule",
    content=(
        "Simpson's rule approximates a definite integral using "
        "quadratic interpolation. For n subintervals (n must be even): "
        "integral ~ (h/3) * [f(x_0) + 4*f(x_1) + 2*f(x_2) + "
        "4*f(x_3) + ... + f(x_n)], where h = (b-a)/n. "
        "Error is O(h^4), making it more accurate than the "
        "trapezoidal rule."
    ),
    example=(
        "Integrate x^2 from 0 to 1, n = 2. h = 0.5. "
        "S = (0.5/3) * [0 + 4*(0.25) + 1] = (0.5/3) * 2 = 0.3333. "
        "Exact = 1/3 = 0.3333."
    ),
    tier=5,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Simpson\\'s rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Simpson%27s_rule",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="runge_kutta",
    content=(
        "The classical fourth-order Runge-Kutta method (RK4) solves "
        "dy/dt = f(t, y) with steps: k1 = h*f(t, y), "
        "k2 = h*f(t+h/2, y+k1/2), k3 = h*f(t+h/2, y+k2/2), "
        "k4 = h*f(t+h, y+k3). Update: y_{n+1} = y_n + "
        "(k1 + 2*k2 + 2*k3 + k4)/6. Error per step is O(h^5)."
    ),
    example=(
        "dy/dt = y, y(0) = 1, h = 0.1. k1 = 0.1*1 = 0.1. "
        "k2 = 0.1*1.05 = 0.105. k3 = 0.1*1.0525 = 0.10525. "
        "k4 = 0.1*1.10525 = 0.110525. "
        "y(0.1) = 1 + (0.1 + 0.21 + 0.2105 + 0.110525)/6 = 1.10517. "
        "Exact: e^0.1 = 1.10517."
    ),
    tier=6,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Runge-Kutta methods', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods",
    prerequisites=["newton_raphson"],
))

register_atom(Atom(
    atom_type="formula",
    name="interpolation_lagrange",
    content=(
        "Lagrange interpolation constructs the unique polynomial of "
        "degree at most n passing through n+1 data points (x_i, y_i). "
        "P(x) = sum_{i=0}^{n} y_i * L_i(x), where "
        "L_i(x) = prod_{j != i} (x - x_j) / (x_i - x_j)."
    ),
    example=(
        "Points: (1,1), (2,4), (3,9). "
        "L_0(x) = (x-2)(x-3)/((1-2)(1-3)) = (x-2)(x-3)/2. "
        "L_1(x) = (x-1)(x-3)/((2-1)(2-3)) = -(x-1)(x-3). "
        "L_2(x) = (x-1)(x-2)/((3-1)(3-2)) = (x-1)(x-2)/2. "
        "P(x) = x^2 (interpolates y = x^2 exactly)."
    ),
    tier=5,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Lagrange polynomial', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lagrange_polynomial",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="lu_decomposition",
    content=(
        "LU decomposition factors a matrix A into a lower triangular "
        "matrix L and an upper triangular matrix U such that A = LU "
        "(or PA = LU with partial pivoting). Used to solve Ax = b "
        "efficiently: first solve Ly = b (forward substitution), "
        "then Ux = y (back substitution). Cost is O(n^3/3)."
    ),
    example=(
        "A = [[2, 1], [4, 3]]. "
        "L = [[1, 0], [2, 1]], U = [[2, 1], [0, 1]]. "
        "Check: LU = [[2, 1], [4, 3]] = A."
    ),
    tier=6,
    domain="numerical_methods",
    source="Wikipedia contributors, 'LU decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/LU_decomposition",
    prerequisites=["determinant"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="power_method",
    content=(
        "The power method finds the dominant eigenvalue and eigenvector "
        "of a matrix A by iterating x_{k+1} = A x_k / ||A x_k||. "
        "Converges if there is a dominant eigenvalue (|lambda_1| > "
        "|lambda_2|). The convergence rate is |lambda_2/lambda_1|."
    ),
    example=(
        "A = [[2, 1], [1, 2]], x0 = [1, 0]. "
        "x1 = [2, 1]/sqrt(5) = [0.894, 0.447]. "
        "x2 = [2.341, 2.236]/3.24 = [0.722, 0.690]. "
        "Converges to eigenvector [1, 1]/sqrt(2), eigenvalue 3."
    ),
    tier=6,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Power iteration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Power_iteration",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="formula",
    name="condition_number",
    content=(
        "The condition number of a matrix A measures its sensitivity "
        "to perturbations: kappa(A) = ||A|| * ||A^{-1}||. For the "
        "2-norm, kappa_2(A) = sigma_max / sigma_min, where sigma "
        "are singular values. A large condition number means the "
        "system Ax = b is ill-conditioned: small errors in b cause "
        "large errors in x."
    ),
    example=(
        "A = [[1, 0], [0, 0.001]]. sigma_max = 1, sigma_min = 0.001. "
        "kappa_2(A) = 1 / 0.001 = 1000. System is ill-conditioned."
    ),
    tier=6,
    domain="numerical_methods",
    source="Wikipedia contributors, 'Condition number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Condition_number",
    prerequisites=["eigenvalue"],
))
