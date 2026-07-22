"""Knowledge atoms for QFT, telecommunications, robotics, oceanography, geophysics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── QFT basics (tier 6-7) ────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="field_lagrangian",
    content=(
        "The Lagrangian density for a real scalar field phi with mass m is "
        "L = (1/2)(d_mu phi)(d^mu phi) - (1/2)m^2 phi^2. The action is "
        "S = integral L d^4x. The Euler-Lagrange equation yields the "
        "Klein-Gordon equation: (d_mu d^mu + m^2) phi = 0."
    ),
    example=(
        "Scalar field L = (1/2)(dphi/dt)^2 - (1/2)(dphi/dx)^2 - (1/2)m^2 phi^2. "
        "E-L equation: d^2 phi/dt^2 - d^2 phi/dx^2 + m^2 phi = 0 (Klein-Gordon)."
    ),
    tier=6, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Scalar field theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Scalar_field_theory",
    prerequisites=["lagrangian"],
))

register_atom(Atom(
    atom_type="formula",
    name="feynman_propagator",
    content=(
        "The Feynman propagator for a scalar field is "
        "D_F(p) = i / (p^2 - m^2 + i*epsilon), where p is the four-momentum, "
        "m is the particle mass, and epsilon -> 0+ is the Feynman prescription "
        "for handling the poles."
    ),
    example=(
        "For a massless scalar (m=0): D_F(p) = i / (p^2 + i*epsilon). "
        "At p^2 = 0 the propagator has a pole (on-shell particle)."
    ),
    tier=7, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Propagator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Propagator",
    prerequisites=["field_lagrangian"],
))

register_atom(Atom(
    atom_type="formula",
    name="vertex_factor",
    content=(
        "In Feynman diagram calculations, each interaction vertex contributes "
        "a vertex factor. For phi^4 theory with interaction L_int = -lambda/4! phi^4, "
        "each 4-point vertex contributes a factor of -i*lambda. For QED, each "
        "electron-photon vertex contributes -i*e*gamma^mu."
    ),
    example=(
        "phi^4 theory, lambda=0.1: single vertex diagram contributes "
        "-i*0.1 = -0.1i to the amplitude."
    ),
    tier=7, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Feynman diagram', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Feynman_diagram",
    prerequisites=["feynman_propagator"],
))

register_atom(Atom(
    atom_type="formula",
    name="tree_level_amplitude",
    content=(
        "A tree-level scattering amplitude is computed by summing over all "
        "tree-level Feynman diagrams. For 2->2 scattering in phi^4 theory, "
        "the tree-level amplitude is M = -lambda (a single vertex). The "
        "differential cross section is d sigma/d Omega = |M|^2 / (64 pi^2 s)."
    ),
    example=(
        "phi^4, lambda=0.1, s=100 GeV^2: |M|^2 = 0.01, "
        "d sigma/d Omega = 0.01 / (64*pi^2*100) = 1.58e-7 GeV^-2."
    ),
    tier=7, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Scattering amplitude', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Scattering_amplitude",
    prerequisites=["vertex_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="dimensional_analysis_qft",
    content=(
        "In natural units (hbar=c=1), [mass] = [energy] = [length]^-1 = [time]^-1. "
        "A scalar field has dimension [phi] = 1 in 4D. A coupling lambda in phi^4 "
        "theory is dimensionless in 4D. The Lagrangian density has dimension [L] = 4."
    ),
    example=(
        "In 4D: [phi] = 1, [d_mu] = 1, [L] = [d_mu phi]^2 = 4. "
        "phi^4 coupling: [lambda * phi^4] = [lambda] + 4 = 4, so [lambda] = 0 (dimensionless)."
    ),
    tier=6, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Dimensional analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Natural_units",
    prerequisites=["dimensional_analysis_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="symmetry_and_conservation",
    content=(
        "Noether's theorem: every continuous symmetry of the action yields a "
        "conserved current j^mu with d_mu j^mu = 0. Time translation symmetry "
        "gives energy conservation, spatial translation gives momentum "
        "conservation, rotational symmetry gives angular momentum conservation."
    ),
    example=(
        "Complex scalar field L = |d_mu phi|^2 - m^2|phi|^2 has U(1) symmetry "
        "phi -> e^(i*alpha)*phi. Conserved current: j^mu = i(phi* d^mu phi - phi d^mu phi*). "
        "Conserved charge: Q = integral j^0 d^3x (particle number)."
    ),
    tier=6, domain="quantum_field_theory",
    source="Wikipedia contributors, 'Noether\\'s theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Noether%27s_theorem",
    prerequisites=["lagrangian"],
))

# ── Telecommunications (tier 5) ──────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="shannon_limit",
    content=(
        "The Shannon-Hartley theorem gives the maximum data rate (channel capacity) "
        "of a communication channel: C = B * log2(1 + SNR), where C is capacity "
        "in bits/s, B is bandwidth in Hz, and SNR is the signal-to-noise ratio."
    ),
    example=(
        "Given B=1 MHz, SNR=100 (20 dB): C = 1e6 * log2(1 + 100) = "
        "1e6 * 6.658 = 6.658 Mbps."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Shannon-Hartley theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem",
    prerequisites=["channel_capacity"],
))

register_atom(Atom(
    atom_type="formula",
    name="modulation_bpsk",
    content=(
        "Binary Phase Shift Keying (BPSK) maps bits to phases: 0 -> 0 rad, "
        "1 -> pi rad. The bit error rate is BER = Q(sqrt(2*Eb/N0)), where "
        "Q is the Q-function and Eb/N0 is the energy per bit to noise ratio."
    ),
    example=(
        "Given Eb/N0 = 10 dB = 10: BER = Q(sqrt(20)) = Q(4.47) = 3.87e-6."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Phase-shift keying', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Phase-shift_keying",
    prerequisites=["shannon_limit"],
))

register_atom(Atom(
    atom_type="formula",
    name="link_budget",
    content=(
        "A link budget accounts for all gains and losses from transmitter to "
        "receiver: P_rx = P_tx + G_tx - L_path + G_rx - L_misc, all in dB. "
        "Free-space path loss: L_path = 20*log10(4*pi*d*f/c) dB."
    ),
    example=(
        "Given P_tx=30 dBm, G_tx=10 dBi, d=10 km, f=2.4 GHz, G_rx=5 dBi: "
        "L_path = 20*log10(4*pi*10000*2.4e9/3e8) = 120.0 dB. "
        "P_rx = 30 + 10 - 120 + 5 = -75 dBm."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Link budget', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Link_budget",
    prerequisites=["antenna_gain"],
))

register_atom(Atom(
    atom_type="formula",
    name="antenna_gain",
    content=(
        "Antenna gain relates to directivity and efficiency: G = eta * D, "
        "where eta is the antenna efficiency and D is the directivity. "
        "For a half-wave dipole, D = 1.64 (2.15 dBi). Effective aperture: "
        "A_eff = G * lambda^2 / (4*pi)."
    ),
    example=(
        "Half-wave dipole, eta=0.9, f=300 MHz (lambda=1 m): "
        "G = 0.9 * 1.64 = 1.476 (1.69 dBi). "
        "A_eff = 1.476 * 1^2 / (4*pi) = 0.1175 m^2."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Antenna gain', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Antenna_gain",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="ofdm_subcarrier",
    content=(
        "Orthogonal Frequency Division Multiplexing (OFDM) divides a wideband "
        "channel into N narrowband subcarriers. Subcarrier spacing: "
        "delta_f = 1/T_symbol. Total bandwidth: B = N * delta_f. Each subcarrier "
        "carries independent data, enabling parallel transmission."
    ),
    example=(
        "Given N=64 subcarriers, T_symbol=3.2 us: delta_f = 1/3.2e-6 = 312.5 kHz. "
        "Total bandwidth: B = 64 * 312.5e3 = 20 MHz."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Orthogonal frequency-division multiplexing', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Orthogonal_frequency-division_multiplexing",
    prerequisites=["dft_compute"],
))

register_atom(Atom(
    atom_type="formula",
    name="spread_spectrum",
    content=(
        "In Direct Sequence Spread Spectrum (DSSS), the data signal is multiplied "
        "by a spreading code with chip rate R_c >> data rate R_b. Processing gain: "
        "G_p = R_c / R_b = B_spread / B_data. This provides interference rejection "
        "and multiple access capability."
    ),
    example=(
        "Given R_b=10 kbps, R_c=1 Mcps: G_p = 1e6/1e4 = 100 (20 dB). "
        "A jammer needs 100x more power to disrupt the signal."
    ),
    tier=5, domain="telecommunications",
    source="Wikipedia contributors, 'Spread spectrum', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Spread_spectrum",
    prerequisites=["shannon_limit"],
))

# ── Robotics (tier 5-6) ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="forward_kinematics",
    content=(
        "Forward kinematics computes the end-effector position and orientation "
        "from joint angles. For an n-DOF robot arm, the transformation is "
        "T_0n = T_01 * T_12 * ... * T_(n-1)n, where each T_ij is a 4x4 "
        "homogeneous transformation matrix from Denavit-Hartenberg parameters."
    ),
    example=(
        "2-link planar arm, L1=1, L2=1, theta1=30 deg, theta2=45 deg: "
        "x = L1*cos(30) + L2*cos(75) = 0.866 + 0.259 = 1.125. "
        "y = L1*sin(30) + L2*sin(75) = 0.5 + 0.966 = 1.466."
    ),
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Forward kinematics', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Forward_kinematics",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="inverse_kinematics",
    content=(
        "Inverse kinematics finds joint angles that place the end-effector at "
        "a desired position. For a 2-link planar arm: theta2 = acos((x^2+y^2-L1^2-L2^2)/(2*L1*L2)), "
        "theta1 = atan2(y,x) - atan2(L2*sin(theta2), L1+L2*cos(theta2)). "
        "Multiple solutions may exist (elbow up/down)."
    ),
    example=(
        "2-link arm, L1=L2=1, target (1, 1): "
        "theta2 = acos((1+1-1-1)/2) = acos(0) = 90 deg. "
        "theta1 = atan2(1,1) - atan2(sin(90), 1+cos(90)) = 45 - 45 = 0 deg."
    ),
    tier=6, domain="robotics",
    source="Wikipedia contributors, 'Inverse kinematics', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Inverse_kinematics",
    prerequisites=["forward_kinematics"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="path_planning",
    content=(
        "Path planning finds a collision-free path from start to goal in a "
        "configuration space. Common algorithms: A* (optimal on grids), RRT "
        "(Rapidly-exploring Random Trees for high-dimensional spaces), and "
        "PRM (Probabilistic Roadmap for multi-query planning). A* uses "
        "f(n) = g(n) + h(n) with an admissible heuristic."
    ),
    example=(
        "A* on 5x5 grid, start=(0,0), goal=(4,4), Manhattan heuristic: "
        "h(0,0) = |4-0|+|4-0| = 8. Optimal path length = 8 steps."
    ),
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'Motion planning', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Motion_planning",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="formula",
    name="pid_control_robot",
    content=(
        "A PID controller computes control output: "
        "u(t) = Kp*e(t) + Ki*integral(e(t)dt) + Kd*de(t)/dt, where "
        "e(t) is the error (setpoint - measurement). Kp is proportional gain, "
        "Ki is integral gain, Kd is derivative gain."
    ),
    example=(
        "Given Kp=2, Ki=0.5, Kd=1, e=3, integral_e=4, de/dt=-1: "
        "u = 2*3 + 0.5*4 + 1*(-1) = 6 + 2 - 1 = 7."
    ),
    tier=5, domain="robotics",
    source="Wikipedia contributors, 'PID controller', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/PID_controller",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="kalman_update",
    content=(
        "The Kalman filter update step: given prior estimate x_hat and covariance P, "
        "measurement z with noise R, and observation matrix H: "
        "K = P*H^T*(H*P*H^T + R)^-1 (Kalman gain), "
        "x_hat_new = x_hat + K*(z - H*x_hat), "
        "P_new = (I - K*H)*P."
    ),
    example=(
        "1D: x_hat=5, P=2, H=1, R=1, z=6: "
        "K = 2*1/(1*2*1+1) = 2/3. x_hat_new = 5 + (2/3)*(6-5) = 5.667. "
        "P_new = (1-2/3)*2 = 0.667."
    ),
    tier=6, domain="robotics",
    source="Wikipedia contributors, 'Kalman filter', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Kalman_filter",
    prerequisites=["matrix_inverse"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="mdp_policy",
    content=(
        "A Markov Decision Process (MDP) is defined by (S, A, T, R, gamma). "
        "The optimal value function satisfies V*(s) = max_a [R(s,a) + gamma * "
        "sum_s' T(s'|s,a) * V*(s')]. Value iteration updates V(s) until convergence. "
        "The optimal policy is pi*(s) = argmax_a [R(s,a) + gamma * sum_s' T(s'|s,a) * V(s')]."
    ),
    example=(
        "2-state MDP, gamma=0.9, R(s1,a1)=10, T(s1|s1,a1)=1: "
        "V*(s1) = 10 + 0.9*V*(s1), V*(s1) = 10/0.1 = 100."
    ),
    tier=6, domain="robotics",
    source="Wikipedia contributors, 'Markov decision process', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Markov_decision_process",
    prerequisites=["markov_stationary"],
))

# ── Oceanography (tier 4-5) ──────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="coriolis_force",
    content=(
        "The Coriolis force is a pseudo-force in rotating reference frames: "
        "F_cor = -2*m*(Omega x v), where Omega is Earth's angular velocity "
        "(7.292e-5 rad/s) and v is velocity. The Coriolis parameter: "
        "f = 2*Omega*sin(latitude)."
    ),
    example=(
        "At latitude 45 deg N: f = 2*7.292e-5*sin(45) = 1.031e-4 rad/s. "
        "For v=10 m/s eastward, F_cor/m = f*v = 1.031e-3 m/s^2 (deflects right in NH)."
    ),
    tier=5, domain="oceanography",
    source="Wikipedia contributors, 'Coriolis force', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Coriolis_force",
    prerequisites=["circular_motion"],
))

register_atom(Atom(
    atom_type="formula",
    name="ocean_wave_speed",
    content=(
        "Deep water wave phase speed: c = sqrt(g*lambda/(2*pi)), where lambda "
        "is wavelength. Shallow water wave speed: c = sqrt(g*h), where h is "
        "water depth. The transition occurs at depth h ~ lambda/2."
    ),
    example=(
        "Deep water, lambda=100 m: c = sqrt(9.81*100/(2*pi)) = sqrt(156.1) = 12.49 m/s. "
        "Shallow water, h=2 m: c = sqrt(9.81*2) = 4.43 m/s."
    ),
    tier=4, domain="oceanography",
    source="Wikipedia contributors, 'Wind wave', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Wind_wave",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="thermohaline",
    content=(
        "Thermohaline circulation is driven by density differences from "
        "temperature and salinity. Seawater density approximation: "
        "rho = rho_0*(1 - alpha*(T-T0) + beta*(S-S0)), where alpha is the "
        "thermal expansion coefficient (~2e-4 /K) and beta is the haline "
        "contraction coefficient (~7.6e-4 /PSU)."
    ),
    example=(
        "Given rho_0=1025 kg/m^3, T=5 C, T0=10 C, S=35 PSU, S0=35 PSU: "
        "rho = 1025*(1 - 2e-4*(-5) + 0) = 1025*(1 + 0.001) = 1026.025 kg/m^3."
    ),
    tier=5, domain="oceanography",
    source="Wikipedia contributors, 'Thermohaline circulation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Thermohaline_circulation",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="ekman_depth",
    content=(
        "The Ekman depth is the depth at which wind-driven current velocity "
        "decays to exp(-pi) ~ 4.3% of the surface value: "
        "D_E = pi * sqrt(2*A_z / f), where A_z is the vertical eddy viscosity "
        "and f is the Coriolis parameter."
    ),
    example=(
        "Given A_z=0.05 m^2/s, latitude 45 deg N (f=1.03e-4): "
        "D_E = pi * sqrt(2*0.05/1.03e-4) = pi * sqrt(970.9) = pi * 31.16 = 97.9 m."
    ),
    tier=5, domain="oceanography",
    source="Wikipedia contributors, 'Ekman layer', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Ekman_layer",
    prerequisites=["coriolis_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="tidal_range",
    content=(
        "Tidal range is the difference between high and low tide levels. "
        "The equilibrium tide theory gives the tidal potential from the Moon: "
        "tidal acceleration ~ G*M_moon*r / d^3, where d is the Earth-Moon "
        "distance. Spring tides (Moon+Sun aligned) are ~20% larger than average; "
        "neap tides (Moon perpendicular to Sun) are ~20% smaller."
    ),
    example=(
        "Average tidal range = 2 m. Spring tide: 2 * 1.2 = 2.4 m. "
        "Neap tide: 2 * 0.8 = 1.6 m."
    ),
    tier=4, domain="oceanography",
    source="Wikipedia contributors, 'Tidal range', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Tidal_range",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="mixed_layer_depth",
    content=(
        "The ocean mixed layer depth (MLD) is the depth where temperature or "
        "density deviates from the surface value by a threshold. Common criteria: "
        "delta_T = 0.2 C or delta_sigma = 0.03 kg/m^3. Wind mixing deepens the "
        "mixed layer; solar heating shoals it. MLD scales with wind stress: "
        "MLD ~ u*^2 / (alpha*g*Q_net/(rho*c_p)), where u* is friction velocity."
    ),
    example=(
        "Surface T=25 C, threshold delta_T=0.2 C. Profile: 25, 25, 24.9, 24.7 "
        "at depths 0, 10, 20, 30 m. MLD ~ 20 m (where T drops below 24.8 C)."
    ),
    tier=5, domain="oceanography",
    source="Wikipedia contributors, 'Mixed layer', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mixed_layer",
    prerequisites=[],
))

# ── Geophysics (tier 4-5) ────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="gravity_anomaly",
    content=(
        "A gravity anomaly is the difference between observed and theoretical "
        "gravity. Free-air anomaly: delta_g_FA = g_obs - g_theoretical + FAC, "
        "where FAC = 0.3086 * h mGal (h in metres). Bouguer anomaly adds a "
        "correction for rock mass: delta_g_B = delta_g_FA - 2*pi*G*rho*h."
    ),
    example=(
        "At h=1000 m, g_obs=980100 mGal, g_theoretical=980000 mGal: "
        "FAC = 0.3086 * 1000 = 308.6 mGal. "
        "delta_g_FA = 100 + 308.6 = 408.6 mGal."
    ),
    tier=5, domain="geophysics",
    source="Wikipedia contributors, 'Gravity anomaly', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Gravity_anomaly",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="magnetic_declination",
    content=(
        "Magnetic declination is the angle between magnetic north and true north. "
        "It varies with location and time due to changes in Earth's magnetic field. "
        "True bearing = magnetic bearing + declination (positive east, negative west). "
        "The International Geomagnetic Reference Field (IGRF) model provides "
        "declination values worldwide."
    ),
    example=(
        "Magnetic bearing = 45 deg, declination = -10 deg (west): "
        "True bearing = 45 + (-10) = 35 deg."
    ),
    tier=4, domain="geophysics",
    source="Wikipedia contributors, 'Magnetic declination', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Magnetic_declination",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="plate_velocity",
    content=(
        "Tectonic plate velocity can be calculated from magnetic anomaly "
        "spacing on the seafloor: v = distance / age. Spreading rates are "
        "typically 2-16 cm/year. Full spreading rate = 2 * half-spreading rate. "
        "Euler's theorem describes plate motion as rotation about an Euler pole."
    ),
    example=(
        "Magnetic anomaly at 100 km from ridge, age 5 Ma: "
        "half-spreading rate = 100 km / 5 Ma = 20 km/Ma = 2.0 cm/yr. "
        "Full rate = 4.0 cm/yr."
    ),
    tier=4, domain="geophysics",
    source="Wikipedia contributors, 'Plate tectonics', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Plate_tectonics",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="seismic_moment",
    content=(
        "Seismic moment quantifies earthquake size: M_0 = mu * A * D, where "
        "mu is the shear modulus (~30 GPa for crust), A is the fault rupture "
        "area, and D is the average slip. Moment magnitude: "
        "M_w = (2/3) * log10(M_0) - 10.7 (M_0 in dyne-cm) or "
        "M_w = (2/3) * (log10(M_0) - 9.1) (M_0 in N-m)."
    ),
    example=(
        "Given mu=30 GPa, A=10 km x 5 km = 5e7 m^2, D=1 m: "
        "M_0 = 30e9 * 5e7 * 1 = 1.5e18 N-m. "
        "M_w = (2/3)*(log10(1.5e18) - 9.1) = (2/3)*(18.176 - 9.1) = 6.05."
    ),
    tier=5, domain="geophysics",
    source="Wikipedia contributors, 'Seismic moment', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Seismic_moment",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="isostasy",
    content=(
        "Isostasy is the gravitational equilibrium of Earth's lithosphere "
        "floating on the asthenosphere. Airy model: crustal root depth "
        "t_root = h * rho_crust / (rho_mantle - rho_crust), where h is "
        "elevation. Pratt model: density varies with elevation to maintain "
        "equal pressure at the compensation depth."
    ),
    example=(
        "Mountain h=3 km, rho_crust=2700 kg/m^3, rho_mantle=3300 kg/m^3: "
        "t_root = 3 * 2700 / (3300 - 2700) = 3 * 2700/600 = 13.5 km."
    ),
    tier=5, domain="geophysics",
    source="Wikipedia contributors, 'Isostasy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Isostasy",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_flow",
    content=(
        "Geothermal heat flow is the rate of heat energy transfer through "
        "Earth's surface: q = -k * dT/dz, where k is thermal conductivity "
        "(W/(m*K)) and dT/dz is the geothermal gradient (typically 25-30 C/km "
        "in continental crust). Global average heat flow is ~87 mW/m^2."
    ),
    example=(
        "Given k=2.5 W/(m*K), dT/dz=30 C/km = 0.03 C/m: "
        "q = 2.5 * 0.03 = 0.075 W/m^2 = 75 mW/m^2."
    ),
    tier=5, domain="geophysics",
    source="Wikipedia contributors, 'Earth\\'s internal heat budget', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Earth%27s_internal_heat_budget",
    prerequisites=[],
))
