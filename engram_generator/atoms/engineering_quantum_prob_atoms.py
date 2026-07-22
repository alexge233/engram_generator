"""Knowledge atoms for engineering, quantum mechanics, and probability.

Covers control systems, signal processing, structural/electrical
engineering, quantum operators and states, and advanced probability
distributions and processes.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# Engineering deep (tier 4-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="nyquist_stability",
    content=(
        "The Nyquist stability criterion determines the stability of a "
        "feedback system by examining the open-loop transfer function's "
        "frequency response. The number of unstable closed-loop poles "
        "equals the number of unstable open-loop poles plus the number "
        "of clockwise encirclements of the critical point (-1, 0) in "
        "the Nyquist plot: Z = N + P."
    ),
    example=(
        "Open-loop TF with P=0 unstable poles. Nyquist plot encircles "
        "(-1,0) zero times clockwise: N=0. Z = 0+0 = 0, system is stable."
    ),
    tier=6,
    domain="control_engineering",
    source="Wikipedia contributors, 'Nyquist stability criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nyquist_stability_criterion",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="kalman_gain",
    content=(
        "The Kalman gain determines how much the predictions of a "
        "Kalman filter are corrected by new measurements. "
        "K_k = P_k^- H^T (H P_k^- H^T + R)^{-1}, where P_k^- is "
        "the prior error covariance, H is the observation matrix, and "
        "R is the measurement noise covariance."
    ),
    example=(
        "Scalar case: P_k^- = 4, H = 1, R = 1. "
        "K = 4*1/(1*4*1 + 1) = 4/5 = 0.8."
    ),
    tier=6,
    domain="control_engineering",
    source="Wikipedia contributors, 'Kalman filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kalman_filter",
    prerequisites=["matrix_inverse"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="fft_butterfly",
    content=(
        "The Cooley-Tukey FFT algorithm computes the discrete Fourier "
        "transform in O(N log N) time by recursively splitting the DFT "
        "into smaller DFTs. The butterfly operation combines pairs of "
        "sub-DFT results: X[k] = E[k] + W_N^k * O[k] and "
        "X[k+N/2] = E[k] - W_N^k * O[k], where W_N = e^{-2*pi*i/N} "
        "is the twiddle factor."
    ),
    example=(
        "N=4 DFT of [1,0,1,0]: Even=[1,1], Odd=[0,0]. "
        "DFT(Even)=[2,0], DFT(Odd)=[0,0]. "
        "X[0]=2+W4^0*0=2, X[1]=0+W4^1*0=0, X[2]=2-0=2, X[3]=0-0=0. "
        "Result: [2, 0, 2, 0]."
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Cooley-Tukey FFT algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm",
    prerequisites=["dft_compute"],
))

register_atom(Atom(
    atom_type="formula",
    name="pid_tuning",
    content=(
        "A PID controller computes a control signal from the error "
        "e(t) as u(t) = K_p*e(t) + K_i*integral(e) + K_d*de/dt, "
        "where K_p is the proportional gain, K_i the integral gain, "
        "and K_d the derivative gain. Ziegler-Nichols tuning sets "
        "gains from the ultimate gain K_u and ultimate period T_u: "
        "K_p = 0.6*K_u, K_i = 2*K_p/T_u, K_d = K_p*T_u/8."
    ),
    example=(
        "Ziegler-Nichols: K_u=10, T_u=2s. "
        "K_p = 0.6*10 = 6, K_i = 2*6/2 = 6, K_d = 6*2/8 = 1.5."
    ),
    tier=5,
    domain="control_engineering",
    source="Wikipedia contributors, 'Ziegler-Nichols method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="power_flow_dc",
    content=(
        "DC power flow approximation for AC power systems linearises "
        "the power flow equations by assuming flat voltage magnitudes "
        "and small angle differences: P_ij = (theta_i - theta_j)/X_ij, "
        "where P_ij is real power flow from bus i to j, theta are "
        "voltage angles, and X_ij is the line reactance."
    ),
    example=(
        "Line reactance X=0.1 pu, theta_1=5 deg=0.0873 rad, "
        "theta_2=0 rad. P_12 = 0.0873/0.1 = 0.873 pu."
    ),
    tier=5,
    domain="power_systems",
    source="Wikipedia contributors, 'Power-flow study', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Power-flow_study",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="fatigue_life",
    content=(
        "The Basquin relation (S-N curve) relates stress amplitude S "
        "to the number of cycles to failure N: S = a * N^b, where a "
        "and b are material constants. Alternatively, N = (S/a)^(1/b). "
        "Miner's rule for cumulative damage: sum(n_i/N_i) = 1 at failure."
    ),
    example=(
        "Material with a=1000 MPa, b=-0.1. At S=500 MPa: "
        "N = (500/1000)^(1/(-0.1)) = 0.5^(-10) = 1024 cycles."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Fatigue (material)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fatigue_(material)",
    prerequisites=["stress_strain"],
))

register_atom(Atom(
    atom_type="formula",
    name="filter_design",
    content=(
        "A first-order low-pass filter has transfer function "
        "H(s) = 1/(1 + s/(2*pi*f_c)), where f_c is the cutoff "
        "frequency. The magnitude response is |H(jw)| = 1/sqrt(1 + "
        "(f/f_c)^2). At f = f_c, the gain is -3 dB (1/sqrt(2))."
    ),
    example=(
        "Cutoff f_c = 1 kHz. At f = 1 kHz: "
        "|H| = 1/sqrt(1 + 1) = 1/sqrt(2) = 0.7071 = -3.01 dB."
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Low-pass filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Low-pass_filter",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="impedance_matching",
    content=(
        "Maximum power transfer occurs when the load impedance equals "
        "the complex conjugate of the source impedance: Z_L = Z_S*. "
        "For a transmission line, the reflection coefficient is "
        "Gamma = (Z_L - Z_0)/(Z_L + Z_0), where Z_0 is the "
        "characteristic impedance. VSWR = (1+|Gamma|)/(1-|Gamma|)."
    ),
    example=(
        "Z_0 = 50 ohm, Z_L = 75 ohm. "
        "Gamma = (75-50)/(75+50) = 25/125 = 0.2. "
        "VSWR = 1.2/0.8 = 1.5."
    ),
    tier=5,
    domain="electrical_engineering",
    source="Wikipedia contributors, 'Impedance matching', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Impedance_matching",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="vibration_analysis",
    content=(
        "A single-degree-of-freedom damped oscillator has equation of "
        "motion m*x'' + c*x' + k*x = 0. The natural frequency is "
        "w_n = sqrt(k/m), the damping ratio zeta = c/(2*sqrt(k*m)), "
        "and the damped frequency w_d = w_n*sqrt(1 - zeta^2)."
    ),
    example=(
        "m=1 kg, k=100 N/m, c=4 Ns/m. "
        "w_n = sqrt(100/1) = 10 rad/s. "
        "zeta = 4/(2*sqrt(100)) = 4/20 = 0.2. "
        "w_d = 10*sqrt(1-0.04) = 10*0.9798 = 9.798 rad/s."
    ),
    tier=5,
    domain="mechanical_engineering",
    source="Wikipedia contributors, 'Vibration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vibration",
    prerequisites=["pendulum_period"],
))

register_atom(Atom(
    atom_type="formula",
    name="reliability_series_parallel",
    content=(
        "For independent components in series, system reliability is "
        "R_sys = R_1 * R_2 * ... * R_n (all must work). For parallel "
        "redundancy, R_sys = 1 - (1-R_1)*(1-R_2)*...*(1-R_n) (at "
        "least one must work)."
    ),
    example=(
        "Two components R_1=0.9, R_2=0.8. "
        "Series: R = 0.9*0.8 = 0.72. "
        "Parallel: R = 1 - (0.1)*(0.2) = 1 - 0.02 = 0.98."
    ),
    tier=4,
    domain="reliability_engineering",
    source="Wikipedia contributors, 'Reliability engineering', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reliability_engineering",
    prerequisites=["basic_prob"],
))


# ===================================================================
# Quantum mechanics ext (tier 6-7)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="expectation_value",
    content=(
        "The expectation value of an observable A in quantum mechanics "
        "is <A> = <psi|A|psi> = integral(psi* A psi dx). For a "
        "discrete basis, <A> = sum_i |c_i|^2 * a_i, where a_i are "
        "eigenvalues and c_i are expansion coefficients."
    ),
    example=(
        "State |psi> = (1/sqrt(2))|0> + (1/sqrt(2))|1>, observable "
        "with eigenvalues a_0=0, a_1=1. "
        "<A> = (1/2)*0 + (1/2)*1 = 0.5."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Expectation value (quantum mechanics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Expectation_value_(quantum_mechanics)",
    prerequisites=["inner_product_verify"],
))

register_atom(Atom(
    atom_type="formula",
    name="harmonic_oscillator_qm",
    content=(
        "The quantum harmonic oscillator has energy eigenvalues "
        "E_n = hbar*omega*(n + 1/2), where n = 0, 1, 2, ... "
        "The ground state energy E_0 = hbar*omega/2 is the zero-point "
        "energy. The ladder operators a and a_dagger satisfy "
        "a|n> = sqrt(n)|n-1> and a_dagger|n> = sqrt(n+1)|n+1>."
    ),
    example=(
        "omega = 2*pi*1e12 rad/s, hbar = 1.055e-34 J*s. "
        "E_0 = 1.055e-34 * 2*pi*1e12 / 2 = 3.313e-22 J. "
        "E_1 = 3*E_0 = 9.939e-22 J."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Quantum harmonic oscillator', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator",
    prerequisites=["schrodinger_1d"],
))

register_atom(Atom(
    atom_type="formula",
    name="perturbation_first_order",
    content=(
        "First-order perturbation theory gives the energy correction "
        "E_n^(1) = <n^(0)|H'|n^(0)>, where H' is the perturbation "
        "Hamiltonian and |n^(0)> are the unperturbed eigenstates. "
        "The corrected energy is E_n = E_n^(0) + lambda*E_n^(1)."
    ),
    example=(
        "Particle in a box with perturbation H' = V_0 (constant). "
        "E_n^(1) = <n|V_0|n> = V_0 * <n|n> = V_0. "
        "All levels shift up by V_0."
    ),
    tier=7,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Perturbation theory (quantum mechanics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perturbation_theory_(quantum_mechanics)",
    prerequisites=["expectation_value"],
))

register_atom(Atom(
    atom_type="rule",
    name="selection_rules",
    content=(
        "Selection rules determine which transitions between quantum "
        "states are allowed. For electric dipole transitions in atoms: "
        "Delta_l = +/-1 (orbital angular momentum changes by 1), "
        "Delta_m = 0, +/-1, and Delta_s = 0 (spin unchanged). "
        "Transitions violating these rules are 'forbidden'."
    ),
    example=(
        "Hydrogen: transition 2p -> 1s has Delta_l = 1-0 = 1. "
        "Allowed. Transition 2s -> 1s has Delta_l = 0-0 = 0. "
        "Forbidden (electric dipole)."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Selection rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Selection_rule",
    prerequisites=["angular_momentum_qn"],
))

register_atom(Atom(
    atom_type="formula",
    name="tunneling_probability",
    content=(
        "Quantum tunneling through a rectangular barrier of height V_0 "
        "and width L has transmission coefficient "
        "T = exp(-2*kappa*L) for E << V_0, where "
        "kappa = sqrt(2*m*(V_0 - E))/hbar."
    ),
    example=(
        "Electron (m=9.11e-31 kg), V_0=5 eV, E=3 eV, L=1 nm. "
        "kappa = sqrt(2*9.11e-31*2*1.6e-19)/1.055e-34 = 7.24e9 m^-1. "
        "T = exp(-2*7.24e9*1e-9) = exp(-14.48) = 5.2e-7."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Quantum tunnelling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_tunnelling",
    prerequisites=["schrodinger_1d"],
))

register_atom(Atom(
    atom_type="formula",
    name="density_operator",
    content=(
        "The density operator (density matrix) rho describes mixed "
        "quantum states: rho = sum_i p_i |psi_i><psi_i|, where p_i "
        "are classical probabilities. For a pure state, rho = "
        "|psi><psi| and Tr(rho^2) = 1. For a mixed state, "
        "Tr(rho^2) < 1."
    ),
    example=(
        "Equal mixture of |0> and |1>: "
        "rho = 0.5*|0><0| + 0.5*|1><1| = [[0.5, 0], [0, 0.5]]. "
        "Tr(rho^2) = 0.25 + 0.25 = 0.5 < 1 (mixed state)."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Density matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Density_matrix",
    prerequisites=["expectation_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="two_level_system",
    content=(
        "A two-level quantum system (qubit) has Hamiltonian "
        "H = (E_1|1><1| + E_2|2><2|) + V(|1><2| + |2><1|). "
        "The Rabi frequency is Omega_R = V/hbar and the energy "
        "splitting is Delta_E = sqrt(delta^2 + Omega_R^2)*hbar, "
        "where delta = (E_2 - E_1)/hbar is the detuning."
    ),
    example=(
        "E_1 = 0, E_2 = 2 eV, V = 0.5 eV (resonant coupling). "
        "delta = 2/hbar, Omega_R = 0.5/hbar. "
        "At resonance (delta=0): Rabi oscillation period = 2*pi/Omega_R."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Two-state quantum system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Two-state_quantum_system",
    prerequisites=["expectation_value"],
))

register_atom(Atom(
    atom_type="principle",
    name="identical_particles",
    content=(
        "Identical particles in quantum mechanics are either bosons "
        "(integer spin, symmetric wavefunction) or fermions (half-integer "
        "spin, antisymmetric wavefunction). For two fermions, "
        "psi(r1,r2) = (1/sqrt(2))[phi_a(r1)*phi_b(r2) - phi_a(r2)*phi_b(r1)]. "
        "The Pauli exclusion principle follows: two identical fermions "
        "cannot occupy the same quantum state."
    ),
    example=(
        "Two electrons in states phi_1 and phi_2: "
        "psi = (1/sqrt(2))[phi_1(r1)*phi_2(r2) - phi_1(r2)*phi_2(r1)]. "
        "If phi_1 = phi_2, psi = 0 (forbidden by Pauli exclusion)."
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Identical particles', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Identical_particles",
    prerequisites=["expectation_value"],
))


# ===================================================================
# Probability deep (tier 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="weibull_distribution",
    content=(
        "The Weibull distribution has PDF f(x; k, lambda) = "
        "(k/lambda)*(x/lambda)^(k-1)*exp(-(x/lambda)^k) for x >= 0, "
        "where k is the shape parameter and lambda the scale parameter. "
        "Mean = lambda * Gamma(1 + 1/k)."
    ),
    example=(
        "k=2 (Rayleigh), lambda=5. f(3) = (2/5)*(3/5)^1*exp(-(3/5)^2) "
        "= 0.4*0.6*exp(-0.36) = 0.24*0.6977 = 0.1674."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Weibull distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weibull_distribution",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="beta_distribution",
    content=(
        "The Beta distribution has PDF f(x; alpha, beta) = "
        "x^(alpha-1)*(1-x)^(beta-1)/B(alpha, beta) for x in [0,1], "
        "where B(alpha, beta) = Gamma(alpha)*Gamma(beta)/Gamma(alpha+beta). "
        "Mean = alpha/(alpha+beta)."
    ),
    example=(
        "Alpha=2, beta=5. Mean = 2/(2+5) = 2/7 = 0.2857. "
        "Mode = (2-1)/(2+5-2) = 1/5 = 0.2."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Beta distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Beta_distribution",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="theorem",
    name="poisson_approximation",
    content=(
        "The Poisson limit theorem states that for n Bernoulli trials "
        "with success probability p, if n -> infinity and p -> 0 such "
        "that np -> lambda, then Binomial(n,p) -> Poisson(lambda). "
        "Rule of thumb: use Poisson when n >= 20 and p <= 0.05."
    ),
    example=(
        "n=100, p=0.02, lambda=np=2. "
        "P(X=3) via Poisson: e^{-2}*2^3/3! = 0.1353*8/6 = 0.1804. "
        "Exact binomial: C(100,3)*0.02^3*0.98^97 = 0.1823."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Poisson limit theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Poisson_limit_theorem",
    prerequisites=["binomial_dist", "poisson_dist"],
))

register_atom(Atom(
    atom_type="theorem",
    name="clt_application",
    content=(
        "The Central Limit Theorem states that the sum (or mean) of n "
        "independent, identically distributed random variables with "
        "mean mu and variance sigma^2 converges in distribution to "
        "N(n*mu, n*sigma^2) as n -> infinity. The sample mean X_bar "
        "is approximately N(mu, sigma^2/n)."
    ),
    example=(
        "X_i ~ Uniform(0,1), mu=0.5, sigma^2=1/12, n=36. "
        "X_bar ~ N(0.5, 1/(12*36)) = N(0.5, 1/432). "
        "P(X_bar > 0.55) = P(Z > (0.55-0.5)/sqrt(1/432)) = P(Z > 1.04) = 0.149."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Central limit theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Central_limit_theorem",
    prerequisites=["variance", "expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="mixture_distribution",
    content=(
        "A mixture distribution combines K component distributions "
        "with weights w_i: f(x) = sum_{i=1}^K w_i * f_i(x), where "
        "sum(w_i) = 1. Mean = sum(w_i * mu_i). "
        "Variance = sum(w_i*(sigma_i^2 + mu_i^2)) - (sum(w_i*mu_i))^2."
    ),
    example=(
        "Mixture of N(0,1) and N(3,1) with w=[0.7, 0.3]. "
        "Mean = 0.7*0 + 0.3*3 = 0.9. "
        "Var = 0.7*(1+0) + 0.3*(1+9) - 0.81 = 0.7+3-0.81 = 2.89."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Mixture distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mixture_distribution",
    prerequisites=["expected_value", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="hazard_rate",
    content=(
        "The hazard function (failure rate) is h(t) = f(t)/R(t), "
        "where f(t) is the PDF and R(t) = 1 - F(t) is the survival "
        "function. For the exponential distribution with rate lambda: "
        "h(t) = lambda (constant hazard). The cumulative hazard is "
        "H(t) = -ln(R(t))."
    ),
    example=(
        "Exponential with lambda=0.01/hour. "
        "h(t) = 0.01 (constant). R(100) = exp(-0.01*100) = exp(-1) = 0.3679. "
        "H(100) = -ln(0.3679) = 1."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Failure rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Failure_rate",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="generating_function_prob",
    content=(
        "The probability generating function of a discrete random "
        "variable X is G(z) = E[z^X] = sum_{k=0}^inf P(X=k)*z^k. "
        "Properties: G(1) = 1, G'(1) = E[X], G''(1) = E[X(X-1)]."
    ),
    example=(
        "Poisson(lambda=2): G(z) = exp(lambda*(z-1)) = exp(2z-2). "
        "G'(z) = 2*exp(2z-2), G'(1) = 2 = E[X]. "
        "G''(1) = 4, so Var(X) = 4 + 2 - 4 = 2."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Probability-generating function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Probability-generating_function",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="extreme_value",
    content=(
        "The Gumbel distribution (Type I extreme value) for maxima "
        "has CDF F(x) = exp(-exp(-(x-mu)/beta)), with mean "
        "mu + beta*gamma_EM (gamma_EM = 0.5772 is the Euler-Mascheroni "
        "constant) and variance pi^2*beta^2/6."
    ),
    example=(
        "Gumbel with mu=0, beta=1. "
        "Mean = 0 + 1*0.5772 = 0.5772. "
        "Var = pi^2/6 = 1.6449. P(X < 2) = exp(-exp(-2)) = exp(-0.1353) = 0.8734."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Gumbel distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gumbel_distribution",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="renewal_reward",
    content=(
        "The renewal-reward theorem states that for a renewal process "
        "with inter-arrival times X_i and rewards R_i, the long-run "
        "average reward rate is E[R]/E[X]. This holds when E[X] < inf "
        "and E[|R|] < inf."
    ),
    example=(
        "Machine runs for X ~ Exp(mean=100 hours), earns R=$500 per cycle. "
        "Long-run rate = E[R]/E[X] = 500/100 = $5/hour."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Renewal theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Renewal_theory",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="branching_process",
    content=(
        "A Galton-Watson branching process models population growth "
        "where each individual independently produces a random number "
        "of offspring. The extinction probability q is the smallest "
        "non-negative root of q = G(q), where G(z) is the offspring "
        "PGF. Extinction is certain iff the mean offspring mu <= 1."
    ),
    example=(
        "Offspring distribution: P(0)=0.4, P(1)=0.3, P(2)=0.3. "
        "Mean mu = 0*0.4 + 1*0.3 + 2*0.3 = 0.9 < 1. "
        "Extinction is certain (q = 1)."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Branching process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Branching_process",
    prerequisites=["generating_function_prob"],
))
