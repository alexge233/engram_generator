"""Knowledge atoms for quantum mechanics (deep) and statistics (deep).

Registers formula and theorem atoms sourced from Wikipedia,
each with a worked example for independent verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Statistics Deep (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="multiple_regression",
    content=(
        "Multiple linear regression models the relationship between a "
        "dependent variable y and two or more independent variables "
        "x_1, x_2, ..., x_p. The model is y = b_0 + b_1*x_1 + "
        "b_2*x_2 + ... + b_p*x_p + epsilon. The coefficients are "
        "estimated by ordinary least squares: b = (X'X)^{-1}X'y, "
        "where X is the design matrix and y is the response vector."
    ),
    example=(
        "Given X = [[1,1,2],[1,2,3],[1,3,5]], y = [6,9,15]: "
        "b = (X'X)^{-1}X'y. X'X = [[3,6,10],[6,14,23],[10,23,38]], "
        "X'y = [30,69,115]. Solving gives b = [0, 1, 2.5] approx."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Linear regression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linear_regression",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="formula",
    name="logistic_regression_compute",
    content=(
        "Logistic regression models the probability of a binary outcome "
        "using the logistic function: P(y=1|x) = 1 / (1 + exp(-(b_0 + "
        "b_1*x_1 + ... + b_p*x_p))). The coefficients are estimated by "
        "maximum likelihood. The log-odds (logit) is a linear function: "
        "ln(P/(1-P)) = b_0 + b_1*x_1 + ... + b_p*x_p."
    ),
    example=(
        "Given b_0=-2, b_1=0.5, x=6: logit = -2 + 0.5*6 = 1. "
        "P = 1/(1+exp(-1)) = 1/1.3679 = 0.7311 (73.1% probability)."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Logistic regression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logistic_regression",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="definition",
    name="residual_analysis",
    content=(
        "In regression analysis, a residual is the difference between "
        "the observed value and the predicted value: e_i = y_i - y_hat_i. "
        "Residual analysis checks model assumptions by examining residual "
        "patterns: normality (Q-Q plot), homoscedasticity (constant "
        "variance), independence, and linearity. The sum of squared "
        "residuals is RSS = sum(e_i^2)."
    ),
    example=(
        "Given y = [3, 5, 7], y_hat = [2.8, 5.1, 7.1]: "
        "residuals = [0.2, -0.1, -0.1]. "
        "RSS = 0.04 + 0.01 + 0.01 = 0.06."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Errors and residuals', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Errors_and_residuals",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="definition",
    name="experimental_design_basic",
    content=(
        "Experimental design is the process of planning an experiment "
        "to ensure valid, defensible conclusions. Key principles include "
        "randomisation (assigning treatments randomly to reduce bias), "
        "replication (repeating measurements to estimate variability), "
        "and blocking (grouping similar units to reduce confounding). "
        "A completely randomised design assigns all treatments randomly, "
        "while a randomised complete block design groups units into blocks."
    ),
    example=(
        "Testing 3 fertilisers on 12 plots: CRD assigns 4 plots per "
        "fertiliser randomly. RCBD groups plots into 4 blocks of 3 "
        "(e.g. by soil type), each block gets all 3 treatments."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Design of experiments', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Design_of_experiments",
    prerequisites=["hypothesis_test"],
))

register_atom(Atom(
    atom_type="definition",
    name="bayesian_credible_vs_ci",
    content=(
        "A Bayesian credible interval is a range [a, b] such that the "
        "posterior probability P(a <= theta <= b | data) = 1 - alpha. "
        "Unlike a frequentist confidence interval, it directly states "
        "the probability that the parameter lies in the interval. A "
        "95% credible interval means: given the data, there is a 95% "
        "probability the parameter is in [a, b]. The highest density "
        "interval (HDI) is the narrowest such interval."
    ),
    example=(
        "Beta(10, 5) posterior for p: mean = 10/15 = 0.667. "
        "95% credible interval = [0.413, 0.876] (from beta quantiles). "
        "Interpretation: 95% probability that p is in [0.413, 0.876]."
    ),
    tier=6,
    domain="statistics",
    source="Wikipedia contributors, 'Credible interval', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Credible_interval",
    prerequisites=["confidence_interval", "bayes_theorem"],
))

register_atom(Atom(
    atom_type="formula",
    name="effect_size",
    content=(
        "Effect size quantifies the magnitude of a difference or "
        "relationship, independent of sample size. Cohen's d measures "
        "the standardised mean difference: d = (M1 - M2) / s_pooled, "
        "where s_pooled = sqrt(((n1-1)*s1^2 + (n2-1)*s2^2) / "
        "(n1+n2-2)). Conventions: d=0.2 small, d=0.5 medium, d=0.8 "
        "large. For correlations, r=0.1 small, r=0.3 medium, r=0.5 large."
    ),
    example=(
        "Group A: M=75, s=10, n=30. Group B: M=70, s=12, n=30. "
        "s_pooled = sqrt((29*100 + 29*144)/58) = sqrt(122) = 11.045. "
        "d = (75-70)/11.045 = 0.453 (medium effect)."
    ),
    tier=4,
    domain="statistics",
    source="Wikipedia contributors, 'Effect size', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Effect_size",
    prerequisites=["std_dev", "hypothesis_test"],
))

register_atom(Atom(
    atom_type="formula",
    name="fisher_exact_test",
    content=(
        "Fisher's exact test evaluates the association between two "
        "categorical variables in a 2x2 contingency table. It computes "
        "the exact probability under the null hypothesis of no "
        "association using the hypergeometric distribution: "
        "P = C(a+b,a)*C(c+d,c) / C(n,a+c), where the table is "
        "[[a,b],[c,d]] and n = a+b+c+d."
    ),
    example=(
        "Table: [[1,9],[11,3]]. a=1,b=9,c=11,d=3, n=24. "
        "P = C(10,1)*C(14,11)/C(24,12) = 10*364/2704156 = 0.001346. "
        "p-value = 0.0014 (significant at alpha=0.05)."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Fisher's exact test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fisher%27s_exact_test",
    prerequisites=["chi_square_independence"],
))

register_atom(Atom(
    atom_type="formula",
    name="rank_correlation",
    content=(
        "Spearman's rank correlation coefficient measures the monotonic "
        "relationship between two ranked variables. For n observations "
        "with rank differences d_i: rho_s = 1 - 6*sum(d_i^2) / "
        "(n*(n^2-1)). Values range from -1 (perfect negative monotonic) "
        "to +1 (perfect positive monotonic). Unlike Pearson's r, it "
        "does not assume linearity or normality."
    ),
    example=(
        "X ranks: [1,2,3,4,5], Y ranks: [2,1,3,5,4]. "
        "d = [-1,1,0,-1,1], d^2 = [1,1,0,1,1], sum(d^2) = 4. "
        "rho_s = 1 - 6*4/(5*24) = 1 - 24/120 = 1 - 0.2 = 0.8."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Spearman's rank correlation coefficient', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient",
    prerequisites=["correlation"],
))

register_atom(Atom(
    atom_type="definition",
    name="categorical_analysis",
    content=(
        "Categorical data analysis examines relationships between "
        "categorical variables using frequency counts. The chi-square "
        "test of independence tests whether two categorical variables "
        "are associated: chi^2 = sum((O-E)^2/E), where O is observed "
        "frequency and E = (row total * column total) / grand total. "
        "Cramér's V measures association strength: V = sqrt(chi^2 / "
        "(n * min(r-1, c-1)))."
    ),
    example=(
        "2x2 table: [[30,10],[20,40]], n=100. "
        "E = [[20,20],[30,30]]. chi^2 = 100/20 + 100/20 + 100/30 + "
        "100/30 = 5+5+3.33+3.33 = 16.67. V = sqrt(16.67/100) = 0.408."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Chi-squared test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chi-squared_test",
    prerequisites=["chi_square_independence"],
))

register_atom(Atom(
    atom_type="formula",
    name="regression_prediction_interval",
    content=(
        "A prediction interval for a new observation y_new at x_0 in "
        "simple linear regression is: y_hat_0 +/- t_{alpha/2,n-2} * "
        "s * sqrt(1 + 1/n + (x_0-x_bar)^2/S_xx), where s is the "
        "residual standard error, S_xx = sum((x_i-x_bar)^2), and "
        "t is the critical value. This is wider than a confidence "
        "interval for the mean because it accounts for individual "
        "observation variability."
    ),
    example=(
        "Given n=10, x_bar=5, S_xx=20, s=2, x_0=7, y_hat_0=15, "
        "t_{0.025,8}=2.306: width = 2.306*2*sqrt(1+0.1+(4/20)) = "
        "2.306*2*sqrt(1.3) = 2.306*2*1.140 = 5.26. "
        "Interval: [15-5.26, 15+5.26] = [9.74, 20.26]."
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Prediction interval', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prediction_interval",
    prerequisites=["linear_regression", "confidence_interval"],
))


# =========================================================================
# Quantum Deep (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="principle",
    name="born_rule",
    content=(
        "The Born rule states that the probability of measuring a "
        "quantum system in a particular state is given by the squared "
        "modulus of the inner product of the state vector with the "
        "eigenstate: P(a_n) = |<a_n|psi>|^2, where |psi> is the "
        "state vector and |a_n> is the eigenstate corresponding to "
        "eigenvalue a_n. This is the fundamental link between the "
        "mathematical formalism and experimental predictions."
    ),
    example=(
        "|psi> = (1/sqrt(2))|0> + (1/sqrt(2))|1>. "
        "P(0) = |1/sqrt(2)|^2 = 1/2 = 0.5. "
        "P(1) = |1/sqrt(2)|^2 = 1/2 = 0.5. Sum = 1 (normalised)."
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Born rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Born_rule",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="formula",
    name="time_evolution",
    content=(
        "The time evolution of a quantum state is governed by the "
        "Schrodinger equation: i*hbar*d|psi>/dt = H|psi>. For a "
        "time-independent Hamiltonian, the solution is "
        "|psi(t)> = exp(-iHt/hbar)|psi(0)>. For an energy eigenstate "
        "|E_n>, this simplifies to |psi(t)> = exp(-iE_n*t/hbar)|E_n>, "
        "giving a phase rotation at frequency omega_n = E_n/hbar."
    ),
    example=(
        "State |psi(0)> = |E_1> with E_1 = 2 eV. At t = 1 fs: "
        "phase = E_1*t/hbar = 2*1.602e-19*1e-15/1.055e-34 = 3.038 rad. "
        "|psi(t)> = exp(-i*3.038)|E_1>."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Schrödinger equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation",
    prerequisites=["born_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="ladder_operators",
    content=(
        "Ladder operators (raising and lowering operators) are used in "
        "quantum mechanics to move between eigenstates of an operator. "
        "For the quantum harmonic oscillator: a|n> = sqrt(n)|n-1> "
        "(lowering), a^dagger|n> = sqrt(n+1)|n+1> (raising). The "
        "number operator N = a^dagger*a satisfies N|n> = n|n>. The "
        "Hamiltonian is H = hbar*omega*(N + 1/2)."
    ),
    example=(
        "a^dagger|2> = sqrt(3)|3>. "
        "a|3> = sqrt(3)|2>. "
        "H|2> = hbar*omega*(2+1/2) = 2.5*hbar*omega."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Ladder operator', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ladder_operator",
    prerequisites=["born_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="hydrogen_orbitals",
    content=(
        "The hydrogen atom energy levels are given by "
        "E_n = -13.6 eV / n^2, where n is the principal quantum "
        "number (n = 1, 2, 3, ...). The orbital angular momentum "
        "quantum number l ranges from 0 to n-1, and the magnetic "
        "quantum number m_l ranges from -l to +l. The degeneracy "
        "of level n is n^2 (excluding spin) or 2n^2 (including spin)."
    ),
    example=(
        "n=3: E_3 = -13.6/9 = -1.511 eV. "
        "l can be 0, 1, 2 (s, p, d orbitals). "
        "Degeneracy = 3^2 = 9 states (18 with spin)."
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Hydrogen atom', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hydrogen_atom",
    prerequisites=["born_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="spin_half",
    content=(
        "A spin-1/2 particle has two spin states: |+> (spin up) and "
        "|-> (spin down), with eigenvalues +hbar/2 and -hbar/2 for "
        "the z-component S_z. The spin operators satisfy "
        "[S_x, S_y] = i*hbar*S_z (cyclic). In matrix representation: "
        "S_i = (hbar/2)*sigma_i, where sigma_i are the Pauli matrices. "
        "A general spin state is |psi> = alpha|+> + beta|->, with "
        "|alpha|^2 + |beta|^2 = 1."
    ),
    example=(
        "|psi> = (1/sqrt(2))|+> + (1/sqrt(2))|->. "
        "<S_z> = (1/2)(hbar/2) + (1/2)(-hbar/2) = 0. "
        "P(up) = 1/2, P(down) = 1/2."
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Spin-1/2', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spin-%C2%BD",
    prerequisites=["born_rule"],
))

register_atom(Atom(
    atom_type="theorem",
    name="wigner_eckart",
    content=(
        "The Wigner-Eckart theorem states that the matrix elements of "
        "a spherical tensor operator T^(k)_q between angular momentum "
        "eigenstates can be factored into a Clebsch-Gordan coefficient "
        "and a reduced matrix element: <j',m'|T^(k)_q|j,m> = "
        "<j,m;k,q|j',m'> * <j'||T^(k)||j> / sqrt(2j'+1). This "
        "separates the geometric (angular) part from the dynamical part."
    ),
    example=(
        "For a dipole operator (k=1): <1,0|T^(1)_0|1,0> = "
        "<1,0;1,0|1,0> * <1||T^(1)||1>/sqrt(3). "
        "CG coefficient <1,0;1,0|1,0> = 0, so the matrix element "
        "vanishes (selection rule: m' = m+q)."
    ),
    tier=7,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Wigner-Eckart theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wigner%E2%80%93Eckart_theorem",
    prerequisites=["spin_half", "ladder_operators"],
))

register_atom(Atom(
    atom_type="formula",
    name="variational_method",
    content=(
        "The variational principle states that for any normalised trial "
        "wavefunction |psi_trial>, the expectation value of the "
        "Hamiltonian provides an upper bound on the ground state energy: "
        "E_0 <= <psi_trial|H|psi_trial>. By minimising over a family "
        "of trial functions parameterised by alpha, one obtains the "
        "best variational estimate: dE/dalpha = 0."
    ),
    example=(
        "Hydrogen atom with trial psi = exp(-alpha*r). "
        "E(alpha) = alpha^2/2 - alpha (in atomic units). "
        "dE/dalpha = alpha - 1 = 0, so alpha = 1. "
        "E_var = 1/2 - 1 = -0.5 Ha = -13.6 eV (exact ground state)."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Variational method (quantum mechanics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Variational_method_(quantum_mechanics)",
    prerequisites=["born_rule", "hydrogen_orbitals"],
))

register_atom(Atom(
    atom_type="formula",
    name="degenerate_perturbation",
    content=(
        "When applying perturbation theory to degenerate energy levels, "
        "one must diagonalise the perturbation Hamiltonian H' within "
        "the degenerate subspace. The first-order energy corrections "
        "are the eigenvalues of the matrix W_ij = <psi_i|H'|psi_j> "
        "where |psi_i> span the degenerate subspace. The correct "
        "zeroth-order states are the eigenvectors of W."
    ),
    example=(
        "Two-fold degenerate states |a>, |b> with H' matrix "
        "W = [[1, 2],[2, 1]]. Eigenvalues: 1+2=3 and 1-2=-1. "
        "First-order corrections: E_+ = 3, E_- = -1. "
        "Degeneracy is lifted."
    ),
    tier=7,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Perturbation theory (quantum mechanics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perturbation_theory_(quantum_mechanics)",
    prerequisites=["variational_method"],
))

register_atom(Atom(
    atom_type="formula",
    name="scattering_cross_section",
    content=(
        "The differential scattering cross section d_sigma/d_Omega "
        "gives the probability of scattering into solid angle d_Omega. "
        "For Rutherford scattering: d_sigma/d_Omega = (Z1*Z2*e^2 / "
        "(4*E))^2 * 1/sin^4(theta/2). The total cross section is "
        "sigma = integral(d_sigma/d_Omega * d_Omega). In quantum "
        "mechanics, sigma = (4*pi/k^2) * sum((2l+1)*sin^2(delta_l))."
    ),
    example=(
        "Rutherford: Z1=2, Z2=79 (alpha on gold), E=5 MeV, theta=90deg. "
        "d_sigma/d_Omega = (2*79*1.44/(4*5))^2 / sin^4(45deg) "
        "= (22.776)^2 / 0.25 = 518.75/0.25 = 2075 fm^2/sr."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Cross section (physics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cross_section_(physics)",
    prerequisites=["born_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="wkb_approximation",
    content=(
        "The WKB (Wentzel-Kramers-Brillouin) approximation is a "
        "semiclassical method for solving the Schrodinger equation "
        "when the potential varies slowly. The wavefunction is "
        "psi(x) ~ (1/sqrt(p(x))) * exp(+/- i*integral(p(x')dx')/hbar), "
        "where p(x) = sqrt(2m(E-V(x))) is the local momentum. "
        "The Bohr-Sommerfeld quantisation condition is "
        "integral(p(x)dx) = (n + 1/2)*pi*hbar over one period."
    ),
    example=(
        "Infinite square well width L: p = sqrt(2mE) = const. "
        "integral_0^L p dx = p*L = (n+1/2)*pi*hbar. "
        "E_n = (n+1/2)^2*pi^2*hbar^2/(2mL^2). "
        "For n=0: E_0 = pi^2*hbar^2/(8mL^2)."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'WKB approximation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/WKB_approximation",
    prerequisites=["born_rule", "hydrogen_orbitals"],
))
