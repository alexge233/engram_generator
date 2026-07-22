"""Knowledge atoms for nonlinear dynamics, solid state physics, and analytical mechanics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# =========================================================================
# Nonlinear Dynamics (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="fixed_point_classify",
    content=(
        "A fixed point x* of a dynamical system dx/dt = f(x) satisfies "
        "f(x*) = 0. Classification depends on eigenvalues of the Jacobian "
        "at x*: all negative real parts = stable node/focus, all positive "
        "= unstable, mixed = saddle. For 1D: f'(x*) < 0 is stable, "
        "f'(x*) > 0 is unstable."
    ),
    example=(
        "f(x) = x^2 - 4: fixed points at x* = -2 and x* = 2. "
        "f'(x) = 2x. f'(-2) = -4 < 0 (stable), f'(2) = 4 > 0 (unstable)."
    ),
    tier=5,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Fixed point (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fixed_point_(mathematics)",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="definition",
    name="bifurcation_detect",
    content=(
        "A bifurcation occurs when a small change in a parameter causes a "
        "qualitative change in the system's behavior. Saddle-node: two fixed "
        "points collide and annihilate. Pitchfork: one fixed point becomes "
        "three. Hopf: fixed point loses stability and a limit cycle appears. "
        "Detected when eigenvalues of the Jacobian cross the imaginary axis."
    ),
    example=(
        "dx/dt = r - x^2: saddle-node bifurcation at r = 0. "
        "r < 0: no fixed points. r = 0: one at x* = 0. r > 0: two at x* = +/-sqrt(r)."
    ),
    tier=6,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Bifurcation theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bifurcation_theory",
    prerequisites=["fixed_point_classify"],
))

register_atom(Atom(
    atom_type="formula",
    name="lyapunov_exponent",
    content=(
        "The Lyapunov exponent measures the rate of separation of "
        "infinitesimally close trajectories. For a 1D map x_{n+1} = f(x_n), "
        "the Lyapunov exponent is lambda = lim (1/N) sum_{i=0}^{N-1} "
        "ln|f'(x_i)|. Positive lambda indicates chaos, negative indicates "
        "convergence to a fixed point, zero indicates marginal stability."
    ),
    example=(
        "Logistic map f(x) = 4x(1-x) at r=4: f'(x) = 4 - 8x. "
        "Starting x0=0.1, iterate 1000 times, lambda approx ln(2) = 0.693 (chaotic)."
    ),
    tier=6,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Lyapunov exponent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lyapunov_exponent",
    prerequisites=["fixed_point_classify"],
))

register_atom(Atom(
    atom_type="formula",
    name="logistic_map",
    content=(
        "The logistic map is the recurrence x_{n+1} = r * x_n * (1 - x_n), "
        "where r is a parameter in [0, 4] and x in [0, 1]. It exhibits "
        "period-doubling cascade to chaos as r increases. Fixed points: "
        "x* = 0 (unstable for r > 1) and x* = (r-1)/r (stable for 1 < r < 3)."
    ),
    example=(
        "r=2.5, x0=0.4: x1 = 2.5*0.4*0.6 = 0.6, x2 = 2.5*0.6*0.4 = 0.6. "
        "Fixed point x* = (2.5-1)/2.5 = 0.6."
    ),
    tier=5,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Logistic map', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logistic_map",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="definition",
    name="limit_cycle",
    content=(
        "A limit cycle is an isolated closed trajectory in phase space. "
        "Trajectories nearby spiral toward it (stable) or away (unstable). "
        "Existence is often shown via the Poincare-Bendixson theorem: if a "
        "trajectory is confined to a bounded region with no fixed points, "
        "it must approach a limit cycle."
    ),
    example=(
        "Van der Pol oscillator: x'' - mu*(1-x^2)*x' + x = 0 with mu=1. "
        "The limit cycle has approximate amplitude 2 and period T approx 2*pi."
    ),
    tier=7,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Limit cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limit_cycle",
    prerequisites=["fixed_point_classify"],
))

register_atom(Atom(
    atom_type="definition",
    name="strange_attractor",
    content=(
        "A strange attractor is an attractor with a fractal structure and "
        "sensitive dependence on initial conditions. The Lorenz attractor "
        "arises from dx/dt = sigma*(y-x), dy/dt = x*(rho-z)-y, "
        "dz/dt = x*y - beta*z with sigma=10, rho=28, beta=8/3. "
        "Trajectories never repeat but remain bounded."
    ),
    example=(
        "Lorenz system with sigma=10, rho=28, beta=8/3, initial (1,1,1): "
        "correlation dimension approx 2.05, largest Lyapunov exponent approx 0.9."
    ),
    tier=6,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Lorenz system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lorenz_system",
    prerequisites=["lyapunov_exponent"],
))

register_atom(Atom(
    atom_type="formula",
    name="fractal_dimension",
    content=(
        "The box-counting (Minkowski-Bouligand) dimension is "
        "D = lim_{eps->0} log(N(eps)) / log(1/eps), where N(eps) is the "
        "number of boxes of side eps needed to cover the set. For the "
        "Cantor set D = log(2)/log(3) approx 0.631, Koch curve D = log(4)/log(3) "
        "approx 1.262, Sierpinski triangle D = log(3)/log(2) approx 1.585."
    ),
    example=(
        "Koch curve: at each iteration, each segment produces 4 copies "
        "scaled by 1/3. D = log(4)/log(3) = 1.2619."
    ),
    tier=6,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Fractal dimension', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fractal_dimension",
    prerequisites=["logistic_map"],
))

register_atom(Atom(
    atom_type="definition",
    name="chaos_sensitivity",
    content=(
        "Sensitive dependence on initial conditions (the butterfly effect) "
        "means that nearby trajectories diverge exponentially: "
        "|delta(t)| approx |delta(0)| * exp(lambda * t), where lambda is "
        "the largest Lyapunov exponent. A system is chaotic if lambda > 0, "
        "bounded, and has dense periodic orbits."
    ),
    example=(
        "Logistic map r=4: two orbits starting at x0=0.5 and x0=0.5001 "
        "diverge completely after ~20 iterations. lambda = ln(2) approx 0.693."
    ),
    tier=6,
    domain="nonlinear_dynamics",
    source="Wikipedia contributors, 'Butterfly effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Butterfly_effect",
    prerequisites=["lyapunov_exponent"],
))

# =========================================================================
# Solid State Physics (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="law",
    name="bragg_diffraction",
    content=(
        "Bragg's law gives the condition for constructive interference of "
        "X-rays scattered by crystal planes: n*lambda = 2*d*sin(theta), "
        "where n is the order, lambda is the wavelength, d is the "
        "interplanar spacing, and theta is the angle of incidence."
    ),
    example=(
        "Cu K-alpha radiation lambda=1.5406 A, d=2.0 A, n=1: "
        "sin(theta) = lambda/(2*d) = 1.5406/4.0 = 0.3852, theta = 22.68 deg."
    ),
    tier=5,
    domain="solid_state",
    source="Wikipedia contributors, 'Bragg's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bragg%27s_law",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="definition",
    name="miller_indices",
    content=(
        "Miller indices (hkl) describe planes in a crystal lattice. "
        "To find them: take the plane's intercepts on the axes (a, b, c), "
        "take reciprocals (1/a, 1/b, 1/c), and reduce to smallest integers. "
        "A bar over an index means a negative intercept."
    ),
    example=(
        "Plane intercepts at a=2, b=3, c=6: reciprocals (1/2, 1/3, 1/6), "
        "multiply by 6: (3, 2, 1). Miller indices: (321)."
    ),
    tier=4,
    domain="solid_state",
    source="Wikipedia contributors, 'Miller index', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Miller_index",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="reciprocal_lattice",
    content=(
        "The reciprocal lattice is defined by vectors b1 = 2*pi*(a2 x a3) / "
        "(a1 . (a2 x a3)), and cyclic permutations. A reciprocal lattice "
        "vector G = h*b1 + k*b2 + l*b3 is perpendicular to the (hkl) "
        "crystal plane with |G| = 2*pi/d_{hkl}."
    ),
    example=(
        "Simple cubic lattice a=3 A: b1 = 2*pi/a * x_hat = 2.094 A^{-1} x_hat. "
        "G_{100} = b1, |G| = 2*pi/3 = 2.094 A^{-1}, d_{100} = 3 A."
    ),
    tier=6,
    domain="solid_state",
    source="Wikipedia contributors, 'Reciprocal lattice', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reciprocal_lattice",
    prerequisites=["miller_indices"],
))

register_atom(Atom(
    atom_type="formula",
    name="band_gap",
    content=(
        "The band gap E_g is the energy difference between the top of the "
        "valence band and the bottom of the conduction band. Semiconductors "
        "have E_g in the range 0.1-4 eV. The relationship between band gap "
        "and absorption edge wavelength is lambda = hc/E_g."
    ),
    example=(
        "Silicon E_g = 1.12 eV: lambda = (6.626e-34 * 3e8) / (1.12 * 1.602e-19) "
        "= 1.988e-25 / 1.794e-19 = 1108 nm (infrared)."
    ),
    tier=5,
    domain="solid_state",
    source="Wikipedia contributors, 'Band gap', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Band_gap",
    prerequisites=["wavelength_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="fermi_level",
    content=(
        "The Fermi level E_F is the energy at which the probability of "
        "electron occupation is 1/2, given by the Fermi-Dirac distribution: "
        "f(E) = 1 / (1 + exp((E - E_F) / (k_B * T))). At T=0, all states "
        "below E_F are filled and all above are empty."
    ),
    example=(
        "E_F = 5.0 eV, T = 300 K, E = 5.1 eV: f = 1/(1 + exp(0.1/(8.617e-5*300))) "
        "= 1/(1 + exp(3.868)) = 1/(1 + 47.85) = 0.0205."
    ),
    tier=6,
    domain="solid_state",
    source="Wikipedia contributors, 'Fermi level', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fermi_level",
    prerequisites=["boltzmann_probability"],
))

register_atom(Atom(
    atom_type="formula",
    name="phonon_dispersion",
    content=(
        "In a 1D monatomic chain of atoms with mass m, spring constant K, "
        "and lattice constant a, the phonon dispersion relation is "
        "omega(k) = 2*sqrt(K/m) * |sin(k*a/2)|. The maximum frequency "
        "(Debye cutoff) is omega_max = 2*sqrt(K/m) at the zone boundary k = pi/a."
    ),
    example=(
        "K = 10 N/m, m = 1e-26 kg, a = 3e-10 m: omega_max = 2*sqrt(10/1e-26) "
        "= 2*sqrt(1e27) = 2*3.162e13 = 6.325e13 rad/s."
    ),
    tier=6,
    domain="solid_state",
    source="Wikipedia contributors, 'Phonon', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phonon",
    prerequisites=["bragg_diffraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="hall_effect",
    content=(
        "The Hall voltage arises when a current-carrying conductor is placed "
        "in a magnetic field perpendicular to the current: "
        "V_H = I*B / (n*e*t), where I is the current, B is the magnetic "
        "field, n is the carrier density, e is the electron charge, and t "
        "is the thickness. The Hall coefficient R_H = 1/(n*e)."
    ),
    example=(
        "I = 10 mA, B = 0.5 T, n = 8.5e28 /m^3, e = 1.6e-19 C, t = 1 mm: "
        "V_H = 0.01*0.5 / (8.5e28*1.6e-19*0.001) = 0.005/13600 = 3.676e-7 V."
    ),
    tier=5,
    domain="solid_state",
    source="Wikipedia contributors, 'Hall effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hall_effect",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="debye_model",
    content=(
        "The Debye model treats the crystal as a continuum with a cutoff "
        "frequency omega_D. The Debye temperature is Theta_D = h_bar*omega_D/k_B. "
        "The heat capacity approaches 3Nk_B at high T (Dulong-Petit) and "
        "varies as T^3 at low T: C_V = (12/5)*pi^4*N*k_B*(T/Theta_D)^3."
    ),
    example=(
        "Copper: Theta_D = 343 K. At T = 50 K: T/Theta_D = 0.1458. "
        "C_V/Nk_B = (12/5)*pi^4*(0.1458)^3 = 233.2*0.003099 = 0.7224."
    ),
    tier=6,
    domain="solid_state",
    source="Wikipedia contributors, 'Debye model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Debye_model",
    prerequisites=["heat_capacity"],
))

# =========================================================================
# Analytical Mechanics (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="lagrangian",
    content=(
        "The Lagrangian is L = T - V, where T is the kinetic energy and "
        "V is the potential energy. For a particle of mass m in a potential "
        "V(q), L = (1/2)*m*q_dot^2 - V(q). The equations of motion follow "
        "from the Euler-Lagrange equation."
    ),
    example=(
        "Simple pendulum: T = (1/2)*m*l^2*theta_dot^2, V = -m*g*l*cos(theta). "
        "L = (1/2)*m*l^2*theta_dot^2 + m*g*l*cos(theta)."
    ),
    tier=5,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Lagrangian mechanics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lagrangian_mechanics",
    prerequisites=["kinetic_energy", "potential_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="euler_lagrange_mechanics",
    content=(
        "The Euler-Lagrange equation is d/dt (dL/dq_dot) - dL/dq = 0, "
        "where L(q, q_dot, t) is the Lagrangian. This is equivalent to "
        "Newton's second law but generalises to arbitrary coordinate systems "
        "and constraints."
    ),
    example=(
        "Free particle: L = (1/2)*m*x_dot^2. dL/dx_dot = m*x_dot, dL/dx = 0. "
        "Euler-Lagrange: d/dt(m*x_dot) = 0, so m*x_ddot = 0 (Newton's first law)."
    ),
    tier=6,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Euler-Lagrange equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler%E2%80%93Lagrange_equation",
    prerequisites=["lagrangian"],
))

register_atom(Atom(
    atom_type="formula",
    name="hamiltonian",
    content=(
        "The Hamiltonian is H = sum(p_i * q_dot_i) - L, where p_i = dL/dq_dot_i "
        "is the conjugate momentum. For systems where L has no explicit time "
        "dependence, H = T + V = total energy. Hamilton's equations: "
        "dq/dt = dH/dp, dp/dt = -dH/dq."
    ),
    example=(
        "Harmonic oscillator: L = (1/2)*m*x_dot^2 - (1/2)*k*x^2. "
        "p = m*x_dot. H = p^2/(2m) + (1/2)*k*x^2."
    ),
    tier=6,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Hamiltonian mechanics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamiltonian_mechanics",
    prerequisites=["lagrangian"],
))

register_atom(Atom(
    atom_type="formula",
    name="hamilton_equations",
    content=(
        "Hamilton's equations of motion are: dq_i/dt = dH/dp_i and "
        "dp_i/dt = -dH/dq_i. These are 2N first-order ODEs equivalent "
        "to the N second-order Euler-Lagrange equations. They preserve "
        "the symplectic structure of phase space."
    ),
    example=(
        "H = p^2/(2m) + (1/2)*k*x^2: dq/dt = dH/dp = p/m, "
        "dp/dt = -dH/dq = -k*x. Combined: m*x_ddot = -k*x (SHM)."
    ),
    tier=6,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Hamilton's equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamiltonian_mechanics#Hamilton's_equations",
    prerequisites=["hamiltonian"],
))

register_atom(Atom(
    atom_type="theorem",
    name="noether_theorem",
    content=(
        "Noether's theorem states that every continuous symmetry of the "
        "action corresponds to a conserved quantity. Time translation "
        "invariance gives energy conservation, spatial translation gives "
        "momentum conservation, rotational symmetry gives angular "
        "momentum conservation."
    ),
    example=(
        "L = (1/2)*m*(x_dot^2 + y_dot^2) - V(r): rotational symmetry about z-axis. "
        "Conserved quantity: L_z = m*(x*y_dot - y*x_dot) (angular momentum)."
    ),
    tier=7,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Noether's theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Noether%27s_theorem",
    prerequisites=["lagrangian"],
))

register_atom(Atom(
    atom_type="definition",
    name="phase_space",
    content=(
        "Phase space is the space of all possible states of a system, "
        "with coordinates (q_1, ..., q_N, p_1, ..., p_N). Each point "
        "represents a complete state. Trajectories in phase space never "
        "cross (uniqueness of solutions). Liouville's theorem: phase space "
        "volume is conserved under Hamiltonian flow."
    ),
    example=(
        "1D harmonic oscillator: phase space is (x, p) plane. Trajectories "
        "are ellipses: x^2/(2E/k) + p^2/(2mE) = 1."
    ),
    tier=6,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Phase space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phase_space",
    prerequisites=["hamiltonian"],
))

register_atom(Atom(
    atom_type="formula",
    name="normal_modes",
    content=(
        "Normal modes are independent oscillation patterns of a coupled "
        "system. For N coupled oscillators with mass matrix M and stiffness "
        "matrix K, the normal mode frequencies satisfy det(K - omega^2*M) = 0. "
        "Each mode has a characteristic frequency and eigenvector."
    ),
    example=(
        "Two masses m on springs k-2k-k: omega_1 = sqrt(k/m), "
        "omega_2 = sqrt(3k/m). Mode 1: in-phase. Mode 2: out-of-phase."
    ),
    tier=6,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Normal mode', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal_mode",
    prerequisites=["eigenvalue", "lagrangian"],
))

register_atom(Atom(
    atom_type="definition",
    name="canonical_transform",
    content=(
        "A canonical transformation is a change of phase space coordinates "
        "(q, p) -> (Q, P) that preserves Hamilton's equations. The "
        "transformation is canonical if it preserves the Poisson bracket "
        "structure: {Q_i, P_j} = delta_ij. Generated by generating "
        "functions F(q, Q), F(q, P), F(p, Q), or F(p, P)."
    ),
    example=(
        "Point transformation Q = q^2, P = p/(2q): {Q, P} = dQ/dq * dP/dp "
        "- dQ/dp * dP/dq = 2q * 1/(2q) - 0 = 1. Canonical."
    ),
    tier=7,
    domain="analytical_mechanics",
    source="Wikipedia contributors, 'Canonical transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Canonical_transformation",
    prerequisites=["hamiltonian", "hamilton_equations"],
))
