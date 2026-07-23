"""Knowledge atoms for physics and engineering generators (batch 3).

Covers: electromagnetism_ext, continuum_mechanics, plasma_physics,
heat_transfer, structural_engineering, semiconductor, photonics,
antenna_theory, polymer_science, tribology, fluid_ext,
digital_electronics, geology, environmental_engineering.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Electromagnetism (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="rc_circuit",
    content=(
        "An RC circuit consists of a resistor R and capacitor C in series. "
        "The voltage across the capacitor during charging is "
        "V(t) = V0 * (1 - exp(-t / (R*C))), where tau = R*C is the time "
        "constant. During discharging, V(t) = V0 * exp(-t / tau). The "
        "capacitor reaches ~63.2% of final voltage after one time constant."
    ),
    example=(
        "R = 1000 Ohm, C = 1e-6 F, V0 = 5 V. tau = 1000 * 1e-6 = 1e-3 s. "
        "At t = 1e-3 s: V = 5 * (1 - exp(-1)) = 5 * 0.6321 = 3.1606 V."
    ),
    tier=4,
    domain="electromagnetism",
    source="Wikipedia contributors, 'RC circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RC_circuit",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="rlc_impedance",
    content=(
        "The impedance of a series RLC circuit is Z = sqrt(R^2 + (XL - XC)^2), "
        "where XL = omega * L is inductive reactance and XC = 1 / (omega * C) is "
        "capacitive reactance. The phase angle is phi = arctan((XL - XC) / R). "
        "At resonance, XL = XC and Z = R (minimum impedance)."
    ),
    example=(
        "R = 100 Ohm, L = 0.1 H, C = 10e-6 F, f = 50 Hz. "
        "omega = 2*pi*50 = 314.16. XL = 31.42 Ohm, XC = 318.31 Ohm. "
        "Z = sqrt(100^2 + (31.42 - 318.31)^2) = sqrt(10000 + 82342) = 303.8 Ohm."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'RLC circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RLC_circuit",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="ac_power",
    content=(
        "In an AC circuit, real power P = V_rms * I_rms * cos(phi), "
        "reactive power Q = V_rms * I_rms * sin(phi), and apparent power "
        "S = V_rms * I_rms. The power factor is PF = cos(phi) = P / S. "
        "P is measured in watts, Q in VAR, and S in VA."
    ),
    example=(
        "V_rms = 120 V, I_rms = 5 A, phi = 30 deg. "
        "P = 120 * 5 * cos(30) = 600 * 0.866 = 519.6 W. "
        "Q = 600 * sin(30) = 600 * 0.5 = 300 VAR. S = 600 VA."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'AC power', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/AC_power",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="electromagnetic_wave",
    content=(
        "Electromagnetic waves travel at the speed of light c = 3e8 m/s in "
        "vacuum. The wavelength lambda, frequency f, and speed are related by "
        "c = lambda * f. The energy of a photon is E = h * f, where "
        "h = 6.626e-34 J*s is Planck's constant."
    ),
    example=(
        "f = 5e14 Hz (green light). lambda = 3e8 / 5e14 = 6e-7 m = 600 nm. "
        "E = 6.626e-34 * 5e14 = 3.313e-19 J = 2.07 eV."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Electromagnetic radiation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electromagnetic_radiation",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Electromagnetism ext (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="electric_dipole",
    content=(
        "An electric dipole consists of two equal and opposite charges +q and -q "
        "separated by distance d. The dipole moment is p = q * d. The electric "
        "field on the axis at distance r >> d is E = 2*k*p / r^3, and on the "
        "perpendicular bisector is E = k*p / r^3."
    ),
    example=(
        "q = 1e-9 C, d = 0.01 m. p = 1e-9 * 0.01 = 1e-11 C*m. "
        "At r = 0.1 m on axis: E = 2 * 8.99e9 * 1e-11 / 0.001 = 0.1798 V/m."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Electric dipole moment', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electric_dipole_moment",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="capacitor_energy",
    content=(
        "The energy stored in a capacitor is U = 0.5 * C * V^2, equivalently "
        "U = Q^2 / (2*C) or U = 0.5 * Q * V, where C is capacitance, V is "
        "voltage, and Q = C*V is the stored charge."
    ),
    example=(
        "C = 100e-6 F, V = 12 V. U = 0.5 * 100e-6 * 144 = 7.2e-3 J = 7.2 mJ."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Capacitor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Capacitor#Energy_stored_in_a_capacitor",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="magnetic_field_wire",
    content=(
        "The magnetic field at distance r from a long straight wire carrying "
        "current I is B = mu_0 * I / (2 * pi * r), where mu_0 = 4*pi*1e-7 "
        "T*m/A is the permeability of free space. The field forms concentric "
        "circles around the wire (right-hand rule)."
    ),
    example=(
        "I = 10 A, r = 0.05 m. B = 4*pi*1e-7 * 10 / (2*pi*0.05) "
        "= 4e-6 / 0.1 = 4e-5 T = 40 uT."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Biot-Savart law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biot%E2%80%93Savart_law",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="ampere_law",
    content=(
        "Ampere's circuital law states that the line integral of B around a "
        "closed loop equals mu_0 times the enclosed current: "
        "integral(B . dl) = mu_0 * I_enc. For a solenoid with n turns per "
        "unit length, B = mu_0 * n * I inside the solenoid."
    ),
    example=(
        "Solenoid: n = 1000 turns/m, I = 2 A. "
        "B = 4*pi*1e-7 * 1000 * 2 = 2.513e-3 T = 2.513 mT."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Ampere's circuital law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amp%C3%A8re%27s_circuital_law",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="displacement_current",
    content=(
        "Maxwell's addition to Ampere's law: the displacement current density "
        "J_d = epsilon_0 * dE/dt. The total current in Ampere's law becomes "
        "I_enc + epsilon_0 * d(Phi_E)/dt, allowing electromagnetic wave "
        "propagation in free space."
    ),
    example=(
        "A parallel plate capacitor with area A = 0.01 m^2, dV/dt = 1e6 V/s, "
        "d = 0.001 m. dE/dt = dV/dt / d = 1e9 V/(m*s). "
        "J_d = 8.854e-12 * 1e9 = 8.854e-3 A/m^2."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Displacement current', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Displacement_current",
    prerequisites=["ampere_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="lc_oscillation",
    content=(
        "An LC circuit oscillates at angular frequency omega = 1 / sqrt(L*C), "
        "or frequency f = 1 / (2*pi*sqrt(L*C)). The energy oscillates between "
        "the inductor (0.5*L*I^2) and capacitor (0.5*C*V^2), with total "
        "energy constant (no resistance)."
    ),
    example=(
        "L = 0.1 H, C = 100e-6 F. omega = 1 / sqrt(0.1*1e-4) = 1 / sqrt(1e-5) "
        "= 316.2 rad/s. f = 316.2 / (2*pi) = 50.3 Hz."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'LC circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/LC_circuit",
    prerequisites=["square_root"],
))

# ---------------------------------------------------------------------------
# Continuum mechanics (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="stress_tensor",
    content=(
        "The Cauchy stress tensor sigma_ij describes the state of stress at a "
        "point in a deformable body. It is a symmetric 3x3 tensor where "
        "sigma_ii are normal stresses and sigma_ij (i != j) are shear stresses. "
        "The traction vector on a surface with normal n is t = sigma . n."
    ),
    example=(
        "sigma = [[100, 50, 0], [50, -30, 0], [0, 0, 20]] MPa. "
        "On surface n = [1, 0, 0]: t = [100, 50, 0] MPa."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Cauchy stress tensor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cauchy_stress_tensor",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="strain_tensor",
    content=(
        "The infinitesimal strain tensor epsilon_ij = 0.5 * (du_i/dx_j + du_j/dx_i) "
        "where u is the displacement vector. Normal strains epsilon_ii represent "
        "elongation/compression; shear strains epsilon_ij (i != j) represent angular "
        "distortion. Engineering shear strain gamma = 2 * epsilon_ij."
    ),
    example=(
        "Displacement field u = [0.001*x, -0.0005*y, 0]. "
        "epsilon_xx = 0.001, epsilon_yy = -0.0005, epsilon_xy = 0."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Infinitesimal strain theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Infinitesimal_strain_theory",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="law",
    name="hookes_law_3d",
    content=(
        "Generalised Hooke's law relates stress and strain via the elasticity "
        "tensor: sigma_ij = C_ijkl * epsilon_kl. For isotropic materials, "
        "sigma_ij = lambda * delta_ij * epsilon_kk + 2*mu * epsilon_ij, "
        "where lambda and mu are Lame parameters. Young's modulus E and "
        "Poisson's ratio nu relate: mu = E / (2*(1+nu)), "
        "lambda = E*nu / ((1+nu)*(1-2*nu))."
    ),
    example=(
        "E = 200 GPa, nu = 0.3, epsilon_xx = 0.001, epsilon_yy = epsilon_zz = 0. "
        "lambda = 115.4 GPa, mu = 76.9 GPa. "
        "sigma_xx = 115.4*0.001 + 2*76.9*0.001 = 269.2 MPa."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Hooke's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hooke%27s_law#Isotropic_materials",
    prerequisites=["stress_tensor", "strain_tensor"],
))

register_atom(Atom(
    atom_type="method",
    name="mohr_circle",
    content=(
        "Mohr's circle is a graphical method to find principal stresses and "
        "maximum shear stress from a 2D stress state. Centre C = (sigma_x + sigma_y)/2, "
        "radius R = sqrt(((sigma_x - sigma_y)/2)^2 + tau_xy^2). Principal stresses "
        "are sigma_1,2 = C +/- R. Max shear stress = R."
    ),
    example=(
        "sigma_x = 80 MPa, sigma_y = -40 MPa, tau_xy = 30 MPa. "
        "C = (80 + (-40))/2 = 20 MPa. R = sqrt(60^2 + 30^2) = sqrt(4500) = 67.1 MPa. "
        "sigma_1 = 87.1 MPa, sigma_2 = -47.1 MPa."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Mohr's circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mohr%27s_circle",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="von_mises",
    content=(
        "The von Mises yield criterion predicts yielding when the von Mises "
        "stress sigma_vm reaches the yield strength sigma_y. For 3D: "
        "sigma_vm = sqrt(0.5*((s1-s2)^2 + (s2-s3)^2 + (s3-s1)^2)), where "
        "s1, s2, s3 are principal stresses. Yielding occurs when sigma_vm >= sigma_y."
    ),
    example=(
        "s1 = 100 MPa, s2 = 50 MPa, s3 = 0. "
        "sigma_vm = sqrt(0.5*(50^2 + 50^2 + 100^2)) = sqrt(0.5*12500) = 86.6 MPa. "
        "If sigma_y = 250 MPa: safe (86.6 < 250)."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Von Mises yield criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Von_Mises_yield_criterion",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="elastic_moduli",
    content=(
        "Elastic moduli relate stress to strain in isotropic materials. "
        "Young's modulus E = sigma / epsilon (uniaxial). Shear modulus "
        "G = tau / gamma. Bulk modulus K = -V * dP/dV. They are related: "
        "E = 2*G*(1+nu) = 3*K*(1-2*nu), where nu is Poisson's ratio."
    ),
    example=(
        "E = 200 GPa, nu = 0.3. G = 200 / (2*1.3) = 76.9 GPa. "
        "K = 200 / (3*0.4) = 166.7 GPa."
    ),
    tier=5,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Elastic modulus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Elastic_modulus",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Plasma physics (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="debye_length",
    content=(
        "The Debye length lambda_D = sqrt(epsilon_0 * k_B * T / (n_e * e^2)) "
        "is the distance over which charge carriers screen out electric fields "
        "in a plasma. Beyond lambda_D, the plasma is quasi-neutral. "
        "k_B = 1.381e-23 J/K, e = 1.602e-19 C."
    ),
    example=(
        "T = 1e4 K, n_e = 1e18 m^-3. lambda_D = sqrt(8.854e-12 * 1.381e-23 * 1e4 "
        "/ (1e18 * (1.602e-19)^2)) = sqrt(4.76e-6) = 2.18e-3 m = 2.18 mm."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Debye length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Debye_length",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="plasma_frequency",
    content=(
        "The electron plasma frequency omega_pe = sqrt(n_e * e^2 / (epsilon_0 * m_e)) "
        "is the natural oscillation frequency of electrons in a plasma. "
        "Electromagnetic waves with omega < omega_pe cannot propagate. "
        "f_pe = omega_pe / (2*pi) ~ 9 * sqrt(n_e) Hz (with n_e in m^-3)."
    ),
    example=(
        "n_e = 1e12 m^-3. f_pe ~ 9 * sqrt(1e12) = 9 * 1e6 = 9 MHz."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Plasma oscillation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Plasma_oscillation",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="cyclotron_frequency",
    content=(
        "The cyclotron frequency omega_c = q*B / m is the angular frequency "
        "at which a charged particle gyrates around a magnetic field line. "
        "The cyclotron radius (Larmor radius) is r_L = m*v_perp / (q*B). "
        "For electrons: f_ce = e*B / (2*pi*m_e) ~ 28 GHz/T."
    ),
    example=(
        "B = 0.1 T, electron. f_ce = 1.602e-19 * 0.1 / (2*pi*9.109e-31) "
        "= 1.602e-20 / 5.725e-30 = 2.799e9 Hz ~ 2.8 GHz."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Cyclotron resonance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclotron_resonance",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="plasma_beta",
    content=(
        "The plasma beta is the ratio of plasma (thermal) pressure to magnetic "
        "pressure: beta = n*k_B*T / (B^2 / (2*mu_0)). Beta < 1 means the "
        "magnetic field dominates; beta > 1 means thermal pressure dominates. "
        "In fusion plasmas, beta ~ 0.01-0.1."
    ),
    example=(
        "n = 1e20 m^-3, T = 1e7 K, B = 5 T. "
        "P_thermal = 1e20 * 1.381e-23 * 1e7 = 1.381e4 Pa. "
        "P_magnetic = 5^2 / (2 * 4*pi*1e-7) = 9.947e6 Pa. "
        "beta = 1.381e4 / 9.947e6 = 0.00139."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Beta (plasma physics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Beta_(plasma_physics)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="coulomb_logarithm",
    content=(
        "The Coulomb logarithm ln(Lambda) = ln(lambda_D / b_min) characterises "
        "the ratio of maximum to minimum impact parameters in plasma collisions. "
        "b_min ~ e^2 / (4*pi*epsilon_0*k_B*T) (classical) or the de Broglie "
        "wavelength (quantum). Typical values: ln(Lambda) ~ 10-20."
    ),
    example=(
        "T = 1e6 K, n = 1e20 m^-3. lambda_D ~ 7.43e-5 m. "
        "b_min ~ 1.67e-12 m. ln(Lambda) ~ ln(7.43e-5 / 1.67e-12) ~ ln(4.45e7) ~ 17.6."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Coulomb logarithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coulomb_logarithm",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="mhd_alfven",
    content=(
        "The Alfven speed is v_A = B / sqrt(mu_0 * rho), where B is the "
        "magnetic field strength and rho is the mass density. Alfven waves "
        "are transverse MHD waves propagating along field lines at this speed. "
        "They are incompressible and carry energy without compression."
    ),
    example=(
        "B = 0.01 T, rho = 1e-12 kg/m^3 (solar corona). "
        "v_A = 0.01 / sqrt(4*pi*1e-7 * 1e-12) = 0.01 / 3.54e-10 ~ 2.82e7 m/s."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Alfven wave', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Alfv%C3%A9n_wave",
    prerequisites=["square_root"],
))

# ---------------------------------------------------------------------------
# Heat transfer (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="fourier_conduction",
    content=(
        "Fourier's law of heat conduction: q = -k * dT/dx, where q is heat "
        "flux (W/m^2), k is thermal conductivity (W/(m*K)), and dT/dx is the "
        "temperature gradient. For a slab: Q = k * A * (T1 - T2) / L, "
        "where L is thickness and A is area."
    ),
    example=(
        "k = 50 W/(m*K), A = 2 m^2, T1 = 100 C, T2 = 20 C, L = 0.1 m. "
        "Q = 50 * 2 * 80 / 0.1 = 80000 W = 80 kW."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Thermal conduction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thermal_conduction",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="newton_cooling",
    content=(
        "Newton's law of cooling: Q = h * A * (T_s - T_inf), where h is the "
        "convective heat transfer coefficient (W/(m^2*K)), A is surface area, "
        "T_s is surface temperature, and T_inf is fluid temperature. Transient: "
        "T(t) = T_inf + (T_0 - T_inf) * exp(-h*A*t / (m*c))."
    ),
    example=(
        "h = 25 W/(m^2*K), A = 0.5 m^2, T_s = 80 C, T_inf = 20 C. "
        "Q = 25 * 0.5 * 60 = 750 W."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Newton's law of cooling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="law",
    name="stefan_boltzmann",
    content=(
        "The Stefan-Boltzmann law gives the total power radiated by a "
        "black body: P = sigma * A * T^4, where sigma = 5.670e-8 W/(m^2*K^4). "
        "For a grey body with emissivity epsilon: P = epsilon * sigma * A * T^4. "
        "Net heat exchange: Q = epsilon * sigma * A * (T1^4 - T2^4)."
    ),
    example=(
        "A = 1 m^2, T = 500 K, epsilon = 0.8. "
        "P = 0.8 * 5.67e-8 * 1 * 500^4 = 0.8 * 5.67e-8 * 6.25e10 = 2835 W."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Stefan-Boltzmann law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_exchanger",
    content=(
        "The log mean temperature difference (LMTD) method for heat exchangers: "
        "Q = U * A * LMTD, where U is overall heat transfer coefficient, "
        "LMTD = (dT1 - dT2) / ln(dT1/dT2), and dT1, dT2 are temperature "
        "differences at each end. For counter-flow: dT1 = T_h,in - T_c,out, "
        "dT2 = T_h,out - T_c,in."
    ),
    example=(
        "dT1 = 80 C, dT2 = 20 C. LMTD = (80 - 20) / ln(80/20) "
        "= 60 / ln(4) = 60 / 1.386 = 43.3 C. "
        "With U = 500 W/(m^2*K), A = 10 m^2: Q = 500*10*43.3 = 216.5 kW."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Heat exchanger', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heat_exchanger",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="fin_efficiency",
    content=(
        "A fin extends a surface to increase heat transfer. Fin efficiency "
        "eta_f = tanh(m*L) / (m*L), where m = sqrt(h*P / (k*A_c)), "
        "h is convection coefficient, P is fin perimeter, k is thermal "
        "conductivity, A_c is cross-sectional area, and L is fin length."
    ),
    example=(
        "h = 50 W/(m^2*K), P = 0.04 m, k = 200 W/(m*K), A_c = 1e-4 m^2, L = 0.05 m. "
        "m = sqrt(50*0.04 / (200*1e-4)) = sqrt(100) = 10. "
        "m*L = 0.5. eta_f = tanh(0.5)/0.5 = 0.4621/0.5 = 0.924."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Fin (extended surface)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fin_(extended_surface)",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="thermal_resistance",
    content=(
        "Thermal resistance R_th = L / (k*A) for conduction through a slab, "
        "or R_th = 1 / (h*A) for convection. For resistances in series: "
        "R_total = R1 + R2 + ... In parallel: 1/R_total = 1/R1 + 1/R2 + ... "
        "Heat flow Q = (T1 - T2) / R_total, analogous to Ohm's law."
    ),
    example=(
        "Wall: L = 0.2 m, k = 1 W/(m*K), A = 10 m^2. "
        "R_cond = 0.2 / (1*10) = 0.02 K/W. "
        "Convection inside h = 10: R_conv = 1/(10*10) = 0.01 K/W. "
        "R_total = 0.03 K/W. If dT = 30 K: Q = 30/0.03 = 1000 W."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Thermal resistance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thermal_resistance",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Structural engineering (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="beam_deflection",
    content=(
        "The maximum deflection of a simply supported beam with a central "
        "point load P is delta = P*L^3 / (48*E*I), where L is span length, "
        "E is Young's modulus, and I is moment of inertia. For a uniformly "
        "distributed load w: delta = 5*w*L^4 / (384*E*I)."
    ),
    example=(
        "P = 10 kN, L = 4 m, E = 200 GPa, I = 1e-4 m^4. "
        "delta = 10e3 * 64 / (48 * 200e9 * 1e-4) = 640000 / 960000 = 0.667 mm."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Deflection (engineering)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deflection_(engineering)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="truss_analysis",
    content=(
        "Truss analysis uses the method of joints or method of sections to "
        "find member forces. At each joint, sum of forces = 0 in x and y. "
        "Members carry only axial forces (tension or compression). "
        "Statical determinacy requires m + r = 2*j, where m = members, "
        "r = reactions, j = joints."
    ),
    example=(
        "Simple truss: 3 members, 3 joints, 3 reactions. "
        "3 + 3 = 6 = 2*3: statically determinate."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Truss', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Truss",
    prerequisites=["system_equations"],
))

register_atom(Atom(
    atom_type="formula",
    name="buckling_load",
    content=(
        "Euler's critical buckling load for a column: P_cr = pi^2 * E * I / L_e^2, "
        "where E is Young's modulus, I is minimum moment of inertia, and L_e is "
        "effective length. L_e depends on end conditions: pinned-pinned L_e = L, "
        "fixed-free L_e = 2L, fixed-pinned L_e = 0.7L, fixed-fixed L_e = 0.5L."
    ),
    example=(
        "E = 200 GPa, I = 5e-6 m^4, L = 3 m (pinned-pinned). "
        "P_cr = pi^2 * 200e9 * 5e-6 / 9 = 1.097e6 N ~ 1097 kN."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Euler's critical load', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler%27s_critical_load",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="moment_of_inertia",
    content=(
        "The second moment of area (moment of inertia) about an axis: "
        "I = integral(y^2 dA). For a rectangle b*h about the centroidal axis: "
        "I = b*h^3/12. For a circle of radius r: I = pi*r^4/4. "
        "Parallel axis theorem: I = I_cm + A*d^2."
    ),
    example=(
        "Rectangle: b = 0.1 m, h = 0.2 m. I = 0.1 * 0.2^3 / 12 "
        "= 0.1 * 0.008 / 12 = 6.667e-5 m^4."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Second moment of area', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Second_moment_of_area",
    prerequisites=["integration_by_parts"],
))

register_atom(Atom(
    atom_type="formula",
    name="shear_bending",
    content=(
        "The bending stress in a beam is sigma = M*y / I, where M is bending "
        "moment, y is distance from neutral axis, and I is moment of inertia. "
        "Maximum stress occurs at y = c (outermost fibre). Shear stress "
        "tau = V*Q / (I*b), where V is shear force, Q is first moment, "
        "b is width at the point."
    ),
    example=(
        "M = 50 kN*m, I = 1e-4 m^4, y = 0.15 m. "
        "sigma = 50e3 * 0.15 / 1e-4 = 75e6 Pa = 75 MPa."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Bending', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bending",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="section_modulus",
    content=(
        "The section modulus S = I / c relates bending moment to maximum stress: "
        "sigma_max = M / S. For a rectangular section: S = b*h^2/6. "
        "For a circular section: S = pi*d^3/32. The plastic section modulus "
        "Z is used for plastic analysis: Z = b*h^2/4 (rectangle)."
    ),
    example=(
        "Rectangle b = 0.1 m, h = 0.3 m. S = 0.1 * 0.09 / 6 = 1.5e-3 m^3. "
        "If M = 100 kN*m: sigma = 100e3 / 1.5e-3 = 66.7 MPa."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Section modulus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Section_modulus",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Semiconductor (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="pn_junction",
    content=(
        "A pn junction forms at the interface between p-type and n-type "
        "semiconductors. The built-in potential V_bi = (k_B*T/q) * ln(N_A*N_D/n_i^2), "
        "where N_A, N_D are acceptor and donor concentrations, n_i is intrinsic "
        "carrier concentration. The depletion width W = sqrt(2*epsilon*V_bi*(1/N_A + 1/N_D)/q)."
    ),
    example=(
        "N_A = 1e17 cm^-3, N_D = 1e16 cm^-3, n_i = 1.5e10 cm^-3, T = 300 K. "
        "V_bi = 0.02585 * ln(1e17*1e16 / (1.5e10)^2) = 0.02585 * ln(4.44e12) = 0.754 V."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'p-n junction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/P%E2%80%93n_junction",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="mosfet_threshold",
    content=(
        "The MOSFET threshold voltage V_T = V_FB + 2*phi_F + sqrt(2*epsilon_s*q*N_A*2*phi_F)/C_ox, "
        "where V_FB is flat-band voltage, phi_F = (k_B*T/q)*ln(N_A/n_i) is Fermi "
        "potential, and C_ox = epsilon_ox/t_ox is oxide capacitance. Above V_T, "
        "a conducting channel forms."
    ),
    example=(
        "phi_F = 0.42 V, N_A = 1e17 cm^-3, t_ox = 5 nm, epsilon_ox = 3.45e-11 F/m. "
        "C_ox = 3.45e-11 / 5e-9 = 6.9e-3 F/m^2."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'Threshold voltage', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Threshold_voltage",
    prerequisites=["pn_junction"],
))

register_atom(Atom(
    atom_type="formula",
    name="diode_iv",
    content=(
        "The ideal diode equation (Shockley equation): I = I_s * (exp(V/(n*V_T)) - 1), "
        "where I_s is reverse saturation current, n is ideality factor (1-2), "
        "and V_T = k_B*T/q ~ 25.85 mV at 300 K. Forward bias: exponential increase. "
        "Reverse bias: I ~ -I_s."
    ),
    example=(
        "I_s = 1e-12 A, n = 1, V = 0.6 V, T = 300 K. "
        "I = 1e-12 * (exp(0.6/0.02585) - 1) = 1e-12 * (exp(23.2) - 1) ~ 1e-12 * 1.19e10 = 0.0119 A."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'Shockley diode equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shockley_diode_equation",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="led_wavelength",
    content=(
        "An LED emits photons when electrons recombine across the bandgap. "
        "The emitted wavelength lambda = h*c / E_g, where E_g is the bandgap "
        "energy. GaAs: E_g = 1.42 eV (infrared, 874 nm). GaN: E_g = 3.4 eV "
        "(blue, 365 nm). InGaN varies with composition."
    ),
    example=(
        "E_g = 2.0 eV (red LED). lambda = 6.626e-34 * 3e8 / (2.0 * 1.602e-19) "
        "= 1.988e-25 / 3.204e-19 = 620.5 nm."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'Light-emitting diode', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Light-emitting_diode",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="carrier_concentration",
    content=(
        "In an intrinsic semiconductor, n = p = n_i = sqrt(N_c * N_v) * exp(-E_g/(2*k_B*T)). "
        "For doped semiconductors: n-type n ~ N_D, p = n_i^2/N_D. "
        "p-type p ~ N_A, n = n_i^2/N_A. The mass action law: n*p = n_i^2."
    ),
    example=(
        "Si at 300 K: n_i = 1.5e10 cm^-3. N_D = 1e16 cm^-3 (n-type). "
        "n = 1e16 cm^-3, p = (1.5e10)^2 / 1e16 = 2.25e4 cm^-3."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'Charge carrier density', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Charge_carrier_density",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="depletion_width",
    content=(
        "The depletion width of a pn junction is "
        "W = sqrt(2*epsilon_s*(V_bi - V)*(1/N_A + 1/N_D) / q), "
        "where V_bi is built-in potential and V is applied voltage "
        "(negative for reverse bias). The width increases with reverse bias."
    ),
    example=(
        "V_bi = 0.7 V, V = -5 V (reverse), N_A = 1e17, N_D = 1e16 cm^-3, "
        "epsilon_s = 1.04e-12 F/cm. W = sqrt(2*1.04e-12*5.7*(1e-17+1e-16)/1.6e-19) ~ 0.87 um."
    ),
    tier=5,
    domain="semiconductor",
    source="Wikipedia contributors, 'Depletion region', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Depletion_region",
    prerequisites=["pn_junction"],
))

# ---------------------------------------------------------------------------
# Photonics (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="fiber_optics_na",
    content=(
        "The numerical aperture of an optical fibre is NA = sqrt(n_core^2 - n_clad^2), "
        "where n_core and n_clad are refractive indices of core and cladding. "
        "The acceptance angle theta_max = arcsin(NA). Typical single-mode fibre: "
        "NA ~ 0.12, multi-mode: NA ~ 0.2-0.5."
    ),
    example=(
        "n_core = 1.48, n_clad = 1.46. "
        "NA = sqrt(1.48^2 - 1.46^2) = sqrt(2.1904 - 2.1316) = sqrt(0.0588) = 0.2425. "
        "theta_max = arcsin(0.2425) = 14.03 degrees."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Numerical aperture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Numerical_aperture",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="laser_gain",
    content=(
        "The small-signal gain coefficient of a laser medium is "
        "g = sigma * (N_2 - (g_2/g_1)*N_1), where sigma is the stimulated "
        "emission cross section, N_2 and N_1 are upper and lower state "
        "populations, and g_1, g_2 are degeneracies. Population inversion "
        "requires N_2 > (g_2/g_1)*N_1."
    ),
    example=(
        "sigma = 3e-20 cm^2, N_2 = 5e17 cm^-3, N_1 = 1e17 cm^-3, g_1 = g_2 = 1. "
        "g = 3e-20 * (5e17 - 1e17) = 3e-20 * 4e17 = 0.012 cm^-1."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Laser', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laser#Gain_medium_and_cavity",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="photon_energy",
    content=(
        "The energy of a photon is E = h*f = h*c/lambda, where h = 6.626e-34 J*s "
        "is Planck's constant, f is frequency, c = 3e8 m/s, and lambda is "
        "wavelength. In electron volts: E(eV) = 1240 / lambda(nm)."
    ),
    example=(
        "lambda = 500 nm (green). E = 1240/500 = 2.48 eV = 2.48 * 1.602e-19 = 3.973e-19 J."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Photon energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Photon_energy",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="total_internal_reflection",
    content=(
        "Total internal reflection occurs when light passes from a denser to "
        "less dense medium at an angle exceeding the critical angle: "
        "theta_c = arcsin(n_2 / n_1), where n_1 > n_2. Above theta_c, "
        "all light is reflected with no transmission."
    ),
    example=(
        "Glass to air: n_1 = 1.5, n_2 = 1.0. "
        "theta_c = arcsin(1.0/1.5) = arcsin(0.667) = 41.8 degrees."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Total internal reflection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Total_internal_reflection",
    prerequisites=["inverse_trig"],
))

register_atom(Atom(
    atom_type="formula",
    name="laser_threshold",
    content=(
        "The laser threshold condition requires the round-trip gain to equal "
        "losses: 2*g*L = -ln(R1*R2) + 2*alpha*L, where g is gain coefficient, "
        "L is cavity length, R1 and R2 are mirror reflectivities, and alpha "
        "is internal loss. The threshold gain: g_th = alpha + ln(1/(R1*R2))/(2*L)."
    ),
    example=(
        "L = 0.3 m, R1 = 1.0, R2 = 0.95, alpha = 0.01 cm^-1. "
        "g_th = 0.01 + ln(1/0.95)/(2*30) = 0.01 + 0.0513/60 = 0.01 + 0.000855 = 0.0109 cm^-1."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Laser threshold', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laser#Threshold_condition",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="photonic_bandgap",
    content=(
        "A photonic crystal has a photonic bandgap: a range of frequencies "
        "where light cannot propagate. The mid-gap frequency is approximately "
        "f ~ c / (2*n_eff*a), where a is the lattice period and n_eff is the "
        "effective refractive index. The gap width depends on the dielectric contrast."
    ),
    example=(
        "a = 500 nm, n_eff = 2.5. f ~ 3e8 / (2*2.5*500e-9) = 1.2e14 Hz. "
        "lambda ~ 2.5 um (mid-infrared)."
    ),
    tier=5,
    domain="photonics",
    source="Wikipedia contributors, 'Photonic crystal', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Photonic_crystal",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Antenna theory (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="antenna_directivity",
    content=(
        "Antenna directivity D = 4*pi*U_max / P_rad, where U_max is the "
        "maximum radiation intensity (W/sr) and P_rad is total radiated power. "
        "For a short dipole D = 1.5 (1.76 dBi). For a half-wave dipole D = 1.64 (2.15 dBi)."
    ),
    example=(
        "U_max = 10 W/sr, P_rad = 50 W. D = 4*pi*10/50 = 125.66/50 = 2.513 (4.0 dBi)."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Directivity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Directivity",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="antenna_gain_efficiency",
    content=(
        "Antenna gain G = eta * D, where eta is radiation efficiency (0 to 1) "
        "and D is directivity. In dBi: G(dBi) = 10*log10(G). The effective "
        "area A_e = G * lambda^2 / (4*pi) relates gain to capture area."
    ),
    example=(
        "D = 6 (7.78 dBi), eta = 0.9. G = 0.9*6 = 5.4 (7.33 dBi). "
        "At f = 1 GHz (lambda = 0.3 m): A_e = 5.4 * 0.09 / (4*pi) = 0.0387 m^2."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Antenna gain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Antenna_gain",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="friis_transmission",
    content=(
        "The Friis transmission equation relates received to transmitted power: "
        "P_r/P_t = G_t * G_r * (lambda / (4*pi*d))^2, where G_t, G_r are "
        "antenna gains and d is distance. In dB: P_r = P_t + G_t + G_r - FSPL, "
        "where FSPL = 20*log10(4*pi*d/lambda) is free-space path loss."
    ),
    example=(
        "P_t = 1 W, G_t = G_r = 10 dBi, f = 2.4 GHz, d = 100 m. "
        "lambda = 0.125 m. FSPL = 20*log10(4*pi*100/0.125) = 20*log10(10053) = 80.0 dB. "
        "P_r = 0 + 10 + 10 - 80 = -60 dBW = 1 uW."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Friis transmission equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Friis_transmission_equation",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="dipole_radiation",
    content=(
        "A Hertzian (short) dipole of length dl << lambda radiates with "
        "pattern E(theta) proportional to sin(theta). Total radiated power "
        "P = eta_0 * (pi/3) * (I*dl/lambda)^2, where eta_0 = 120*pi Ohm "
        "is free-space impedance. Radiation resistance R_r = 80*pi^2*(dl/lambda)^2."
    ),
    example=(
        "dl = 0.01 m, lambda = 1 m, I = 1 A. "
        "R_r = 80*pi^2*0.0001 = 0.0789 Ohm. P = 0.5*1^2*0.0789 = 0.0395 W."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Dipole antenna', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dipole_antenna",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="array_factor",
    content=(
        "The array factor of a uniform linear array of N elements with spacing d "
        "and progressive phase shift alpha is AF = sin(N*psi/2) / sin(psi/2), "
        "where psi = k*d*cos(theta) + alpha, k = 2*pi/lambda. Main beam direction: "
        "psi = 0, i.e., cos(theta_0) = -alpha/(k*d)."
    ),
    example=(
        "N = 4, d = lambda/2, alpha = 0 (broadside). "
        "At theta = 90 deg: psi = 0. AF = N = 4 (maximum)."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Phased array', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phased_array",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="effective_aperture",
    content=(
        "The effective aperture of an antenna is A_e = G * lambda^2 / (4*pi), "
        "relating the antenna gain to the area that captures incoming power. "
        "For a parabolic dish of physical area A: G = eta_a * 4*pi*A/lambda^2, "
        "where eta_a ~ 0.55-0.7 is aperture efficiency."
    ),
    example=(
        "Dish diameter 1 m, f = 10 GHz (lambda = 0.03 m), eta_a = 0.6. "
        "A = pi*0.25 = 0.785 m^2. G = 0.6*4*pi*0.785/0.0009 = 6597 (38.2 dBi)."
    ),
    tier=5,
    domain="antenna_theory",
    source="Wikipedia contributors, 'Antenna aperture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Antenna_aperture",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Polymer science (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="degree_polymerisation",
    content=(
        "The degree of polymerisation DP = M_n / M_0, where M_n is the "
        "number-average molecular weight and M_0 is the molecular weight "
        "of the repeat unit. For condensation polymerisation: "
        "DP = 1/(1-p), where p is extent of reaction."
    ),
    example=(
        "M_n = 50000 g/mol, M_0 = 100 g/mol. DP = 50000/100 = 500. "
        "Alternatively, p = 0.998: DP = 1/(1-0.998) = 500."
    ),
    tier=5,
    domain="polymer_science",
    source="Wikipedia contributors, 'Degree of polymerization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Degree_of_polymerization",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="molecular_weight_avg",
    content=(
        "Number-average MW: M_n = sum(N_i*M_i)/sum(N_i). "
        "Weight-average MW: M_w = sum(N_i*M_i^2)/sum(N_i*M_i). "
        "Polydispersity index PDI = M_w/M_n >= 1. PDI = 1 for monodisperse, "
        "PDI = 2 for most probable distribution."
    ),
    example=(
        "Species: 100 chains at 10 kDa, 50 chains at 20 kDa. "
        "M_n = (100*10 + 50*20)/(100+50) = 2000/150 = 13.33 kDa. "
        "M_w = (100*100 + 50*400)/(100*10+50*20) = 30000/2000 = 15 kDa. PDI = 1.125."
    ),
    tier=5,
    domain="polymer_science",
    source="Wikipedia contributors, 'Molar mass distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molar_mass_distribution",
    prerequisites=["arithmetic_mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="glass_transition",
    content=(
        "The glass transition temperature T_g is where a polymer transitions "
        "from glassy to rubbery state. The Fox equation for copolymers: "
        "1/T_g = w_1/T_g1 + w_2/T_g2, where w_i are weight fractions. "
        "T_g increases with crosslinking, stiffness, and intermolecular forces."
    ),
    example=(
        "Copolymer: w_1 = 0.6 (T_g1 = 373 K), w_2 = 0.4 (T_g2 = 233 K). "
        "1/T_g = 0.6/373 + 0.4/233 = 0.001609 + 0.001717 = 0.003326. "
        "T_g = 300.7 K = 27.7 C."
    ),
    tier=5,
    domain="polymer_science",
    source="Wikipedia contributors, 'Glass transition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Glass_transition",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="end_to_end_distance",
    content=(
        "The root-mean-square end-to-end distance of an ideal polymer chain is "
        "R = l * sqrt(N), where l is bond length and N is number of bonds. "
        "For a freely jointed chain: <R^2> = N*l^2. With bond angle theta: "
        "<R^2> = N*l^2*(1+cos(theta))/(1-cos(theta))."
    ),
    example=(
        "N = 1000 bonds, l = 1.54 Angstrom (C-C). "
        "R = 1.54 * sqrt(1000) = 1.54 * 31.62 = 48.7 Angstrom = 4.87 nm."
    ),
    tier=5,
    domain="polymer_science",
    source="Wikipedia contributors, 'Ideal chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ideal_chain",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="viscosity_intrinsic",
    content=(
        "The Mark-Houwink equation relates intrinsic viscosity to molecular "
        "weight: [eta] = K * M^a, where K and a are polymer-solvent dependent "
        "constants. a = 0.5 for theta solvent, 0.6-0.8 for good solvents, "
        "a = 2 for rigid rods."
    ),
    example=(
        "K = 1.1e-4 dL/g, a = 0.725, M = 100000 g/mol. "
        "[eta] = 1.1e-4 * 100000^0.725 = 1.1e-4 * 5623 = 0.619 dL/g."
    ),
    tier=5,
    domain="polymer_science",
    source="Wikipedia contributors, 'Mark-Houwink equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mark%E2%80%93Houwink_equation",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="flory_huggins",
    content=(
        "The Flory-Huggins free energy of mixing per lattice site: "
        "dG_mix/(k_B*T*N) = phi*ln(phi)/N_1 + (1-phi)*ln(1-phi)/N_2 + chi*phi*(1-phi), "
        "where phi is volume fraction, N_1, N_2 are degrees of polymerisation, "
        "and chi is the Flory-Huggins interaction parameter."
    ),
    example=(
        "N_1 = 100, N_2 = 1 (polymer + solvent), phi = 0.1, chi = 0.4. "
        "dG/(kT*N) = 0.1*ln(0.1)/100 + 0.9*ln(0.9)/1 + 0.4*0.1*0.9 "
        "= -0.0023 + (-0.0948) + 0.036 = -0.0611."
    ),
    tier=6,
    domain="polymer_science",
    source="Wikipedia contributors, 'Flory-Huggins solution theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Flory%E2%80%93Huggins_solution_theory",
    prerequisites=["logarithm"],
))

# ---------------------------------------------------------------------------
# Tribology (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="friction_force",
    content=(
        "Coulomb's law of friction: the friction force F_f = mu * N, where "
        "mu is the coefficient of friction and N is the normal force. "
        "Static friction: F_f <= mu_s * N. Kinetic friction: F_f = mu_k * N. "
        "Generally mu_s > mu_k."
    ),
    example=(
        "mu_k = 0.3, N = 100 N. F_f = 0.3 * 100 = 30 N."
    ),
    tier=4,
    domain="tribology",
    source="Wikipedia contributors, 'Friction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Friction",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="wear_rate",
    content=(
        "Archard's wear equation: V = K * F * s / H, where V is wear volume, "
        "K is dimensionless wear coefficient, F is normal load, s is sliding "
        "distance, and H is hardness. Specific wear rate k = K/H = V/(F*s)."
    ),
    example=(
        "K = 1e-3, F = 50 N, s = 1000 m, H = 1 GPa. "
        "V = 1e-3 * 50 * 1000 / 1e9 = 5e-8 m^3 = 50 mm^3."
    ),
    tier=5,
    domain="tribology",
    source="Wikipedia contributors, 'Archard equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Archard_equation",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="concept",
    name="lubrication_regime",
    content=(
        "The Stribeck curve identifies three lubrication regimes based on the "
        "Hersey number eta*v/(P): (1) boundary lubrication (direct surface "
        "contact, high friction), (2) mixed lubrication (partial film), "
        "(3) hydrodynamic lubrication (full film separation, low friction). "
        "The lambda ratio = h_min/sigma determines the regime."
    ),
    example=(
        "h_min = 0.5 um, sigma = 0.3 um. lambda = 0.5/0.3 = 1.67. "
        "lambda < 1: boundary. 1 < lambda < 3: mixed. lambda > 3: hydrodynamic. "
        "Result: mixed lubrication."
    ),
    tier=5,
    domain="tribology",
    source="Wikipedia contributors, 'Stribeck curve', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stribeck_curve",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="hertz_contact",
    content=(
        "Hertzian contact theory gives the contact area and pressure between "
        "two elastic spheres. Contact radius a = (3*F*R/(4*E*))^(1/3), "
        "where R = R1*R2/(R1+R2) is effective radius and "
        "1/E* = (1-nu1^2)/E1 + (1-nu2^2)/E2 is effective modulus. "
        "Max pressure p_0 = 3*F/(2*pi*a^2)."
    ),
    example=(
        "F = 100 N, R1 = R2 = 0.01 m (R = 0.005 m), E1 = E2 = 200 GPa, nu = 0.3. "
        "E* = 200e9/(2*(1-0.09)) = 109.9 GPa. "
        "a = (3*100*0.005/(4*109.9e9))^(1/3) = (3.41e-9)^(1/3) = 1.506e-3 m ~ 1.5 mm."
    ),
    tier=5,
    domain="tribology",
    source="Wikipedia contributors, 'Contact mechanics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Contact_mechanics#Hertzian_theory_of_non-adhesive_elastic_contact",
    prerequisites=["exponentiation"],
))

# ---------------------------------------------------------------------------
# Fluid mechanics ext (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="pipe_flow",
    content=(
        "For fully developed laminar flow in a pipe (Re < 2300), the "
        "Hagen-Poiseuille equation gives Q = pi*d^4*dP/(128*mu*L), "
        "where d is diameter, dP is pressure drop, mu is dynamic viscosity, "
        "and L is pipe length. Friction factor f = 64/Re."
    ),
    example=(
        "d = 0.02 m, L = 10 m, dP = 5000 Pa, mu = 0.001 Pa*s. "
        "Q = pi*0.02^4*5000/(128*0.001*10) = pi*8e-7*5000/1.28 = 9.82e-3 m^3/s."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Hagen-Poiseuille equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hagen%E2%80%93Poiseuille_equation",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="venturi_meter",
    content=(
        "A Venturi meter measures flow rate using Bernoulli's equation: "
        "Q = A_2 * sqrt(2*dP / (rho*(1-(A_2/A_1)^2))), where A_1 and A_2 "
        "are cross-sectional areas at the inlet and throat, and dP is the "
        "pressure difference. A discharge coefficient C_d accounts for losses."
    ),
    example=(
        "A_1 = 0.01 m^2, A_2 = 0.005 m^2, dP = 2000 Pa, rho = 1000 kg/m^3. "
        "Q = 0.005 * sqrt(2*2000/(1000*(1-0.25))) = 0.005 * sqrt(5.333) = 0.01155 m^3/s."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Venturi effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Venturi_effect",
    prerequisites=["bernoulli"],
))

register_atom(Atom(
    atom_type="formula",
    name="stokes_drag",
    content=(
        "Stokes' law gives the drag force on a sphere in creeping flow (Re << 1): "
        "F_d = 6*pi*mu*r*v, where mu is dynamic viscosity, r is sphere radius, "
        "and v is velocity. Terminal velocity: v_t = 2*r^2*(rho_s-rho_f)*g/(9*mu)."
    ),
    example=(
        "r = 0.001 m, mu = 0.001 Pa*s, v = 0.01 m/s. "
        "F_d = 6*pi*0.001*0.001*0.01 = 1.885e-7 N."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Stokes' law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stokes%27_law",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="hydraulic_jump",
    content=(
        "A hydraulic jump is a transition from supercritical to subcritical "
        "flow in open channels. The conjugate depth ratio: "
        "y_2/y_1 = 0.5*(-1 + sqrt(1 + 8*Fr_1^2)), where Fr_1 = v_1/sqrt(g*y_1) "
        "is the upstream Froude number. Energy is dissipated in the jump."
    ),
    example=(
        "y_1 = 0.1 m, v_1 = 5 m/s. Fr_1 = 5/sqrt(9.81*0.1) = 5/0.99 = 5.05. "
        "y_2/y_1 = 0.5*(-1+sqrt(1+8*25.5)) = 0.5*(-1+sqrt(205)) = 0.5*(-1+14.32) = 6.66. "
        "y_2 = 0.666 m."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Hydraulic jump', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hydraulic_jump",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="open_channel",
    content=(
        "Manning's equation for open channel flow: v = (1/n)*R_h^(2/3)*S^(1/2), "
        "where n is Manning's roughness coefficient, R_h = A/P is hydraulic "
        "radius (area/wetted perimeter), and S is channel slope. "
        "Flow rate Q = v * A."
    ),
    example=(
        "Rectangular channel: width b = 2 m, depth y = 0.5 m, n = 0.013, S = 0.001. "
        "A = 1 m^2, P = 3 m, R_h = 0.333 m. "
        "v = (1/0.013)*0.333^(2/3)*0.001^(1/2) = 76.92*0.481*0.0316 = 1.17 m/s."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Manning formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Manning_formula",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="pump_power",
    content=(
        "The hydraulic power required by a pump: P_h = rho*g*Q*H, where Q is "
        "volume flow rate and H is total head. Shaft power: P_s = P_h / eta, "
        "where eta is pump efficiency. Total head H = (P2-P1)/(rho*g) + "
        "(v2^2-v1^2)/(2*g) + (z2-z1) + h_f, where h_f is friction head loss."
    ),
    example=(
        "Q = 0.01 m^3/s, H = 20 m, rho = 1000 kg/m^3, eta = 0.75. "
        "P_h = 1000*9.81*0.01*20 = 1962 W. P_s = 1962/0.75 = 2616 W = 2.6 kW."
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Pump', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pump#Pump_power",
    prerequisites=["multiplication"],
))

# ---------------------------------------------------------------------------
# Geology (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="radiometric_dating",
    content=(
        "Radiometric dating uses radioactive decay to determine age: "
        "t = (1/lambda) * ln(1 + D/P), where lambda is decay constant, "
        "D is number of daughter atoms, P is number of parent atoms. "
        "For carbon-14: t_1/2 = 5730 years, lambda = ln(2)/5730."
    ),
    example=(
        "C-14: remaining fraction = 0.25 (25%). "
        "t = -5730/ln(2) * ln(0.25) = -8267 * (-1.386) = 11460 years (2 half-lives)."
    ),
    tier=5,
    domain="geology",
    source="Wikipedia contributors, 'Radiometric dating', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radiometric_dating",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="seismic_velocity",
    content=(
        "P-wave velocity in rocks: V_p = sqrt((K + 4G/3) / rho), where K is "
        "bulk modulus, G is shear modulus, and rho is density. S-wave velocity: "
        "V_s = sqrt(G / rho). S-waves cannot travel through liquids (G = 0)."
    ),
    example=(
        "K = 50 GPa, G = 30 GPa, rho = 2700 kg/m^3. "
        "V_p = sqrt((50e9 + 40e9)/2700) = sqrt(3.33e7) = 5774 m/s. "
        "V_s = sqrt(30e9/2700) = sqrt(1.11e7) = 3333 m/s."
    ),
    tier=5,
    domain="geology",
    source="Wikipedia contributors, 'Seismic wave', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Seismic_wave",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="reference",
    name="mohs_hardness",
    content=(
        "The Mohs hardness scale ranks minerals by scratch resistance from "
        "1 (talc) to 10 (diamond). Each mineral can scratch those below it. "
        "1-Talc, 2-Gypsum, 3-Calcite, 4-Fluorite, 5-Apatite, 6-Orthoclase, "
        "7-Quartz, 8-Topaz, 9-Corundum, 10-Diamond."
    ),
    example=(
        "A mineral scratches fluorite (4) but not apatite (5). "
        "Mohs hardness is between 4 and 5."
    ),
    tier=4,
    domain="geology",
    source="Wikipedia contributors, 'Mohs scale of mineral hardness', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mohs_scale_of_mineral_hardness",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="richter_magnitude",
    content=(
        "The Richter magnitude scale (local magnitude M_L) is logarithmic: "
        "M_L = log10(A) - log10(A_0), where A is maximum trace amplitude "
        "and A_0 is a reference amplitude. Each whole number increase "
        "corresponds to 10x amplitude and ~31.6x energy."
    ),
    example=(
        "A = 10 mm at 100 km distance. log10(A_0) = -3 at this distance. "
        "M_L = log10(10) - (-3) = 1 + 3 = 4.0."
    ),
    tier=4,
    domain="geology",
    source="Wikipedia contributors, 'Richter magnitude scale', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Richter_magnitude_scale",
    prerequisites=["logarithm"],
))

# ---------------------------------------------------------------------------
# Environmental engineering (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="bod_decay",
    content=(
        "Biochemical oxygen demand (BOD) follows first-order decay: "
        "BOD_t = BOD_u * (1 - exp(-k*t)), where BOD_u is ultimate BOD, "
        "k is deoxygenation rate constant (~0.1-0.5 day^-1), and t is time. "
        "BOD_5 is the standard 5-day measurement."
    ),
    example=(
        "BOD_u = 300 mg/L, k = 0.23 day^-1. "
        "BOD_5 = 300 * (1 - exp(-0.23*5)) = 300 * (1 - 0.316) = 300 * 0.684 = 205.2 mg/L."
    ),
    tier=5,
    domain="environmental_engineering",
    source="Wikipedia contributors, 'Biochemical oxygen demand', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biochemical_oxygen_demand",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="dilution_factor",
    content=(
        "The dilution factor is DF = V_final / V_sample. Concentration after "
        "dilution: C_2 = C_1 * V_1 / V_2 (from C_1*V_1 = C_2*V_2). "
        "Serial dilution: total DF = DF_1 * DF_2 * ... * DF_n."
    ),
    example=(
        "C_1 = 500 mg/L, V_1 = 10 mL, V_2 = 250 mL. "
        "C_2 = 500 * 10/250 = 20 mg/L. DF = 250/10 = 25."
    ),
    tier=4,
    domain="environmental_engineering",
    source="Wikipedia contributors, 'Dilution (equation)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dilution_(equation)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="concept",
    name="air_quality_index",
    content=(
        "The Air Quality Index (AQI) converts pollutant concentrations to a "
        "0-500 scale. AQI = ((I_hi - I_lo)/(C_hi - C_lo)) * (C - C_lo) + I_lo, "
        "where C is concentration, C_lo/C_hi are breakpoint concentrations, "
        "and I_lo/I_hi are corresponding index values. "
        "0-50: Good, 51-100: Moderate, 101-150: Unhealthy for sensitive."
    ),
    example=(
        "PM2.5 = 35.5 ug/m^3. Breakpoints: C_lo=12.1, C_hi=35.4, I_lo=51, I_hi=100. "
        "AQI = ((100-51)/(35.4-12.1))*(35.5-12.1)+51 = (49/23.3)*23.4+51 = 100.2."
    ),
    tier=5,
    domain="environmental_engineering",
    source="Wikipedia contributors, 'Air quality index', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Air_quality_index",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="concept",
    name="carbon_footprint",
    content=(
        "A carbon footprint is the total greenhouse gas emissions caused by an "
        "entity, expressed in CO2 equivalents (CO2e). Calculated as: "
        "CF = sum(activity_data * emission_factor). Common factors: "
        "electricity ~0.5 kg CO2/kWh (varies), gasoline 2.31 kg CO2/L, "
        "natural gas 2.0 kg CO2/m^3."
    ),
    example=(
        "Monthly: 500 kWh electricity (0.5 kg/kWh) + 100 L gasoline (2.31 kg/L). "
        "CF = 500*0.5 + 100*2.31 = 250 + 231 = 481 kg CO2e."
    ),
    tier=5,
    domain="environmental_engineering",
    source="Wikipedia contributors, 'Carbon footprint', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Carbon_footprint",
    prerequisites=["multiplication"],
))

# ---------------------------------------------------------------------------
# Digital electronics (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="method",
    name="karnaugh_map",
    content=(
        "A Karnaugh map is a visual method for simplifying Boolean expressions. "
        "Adjacent cells differing by one variable are grouped in powers of 2 "
        "(1, 2, 4, 8). Each group yields a product term with the varying "
        "variable eliminated. The minimal expression is the OR of all groups."
    ),
    example=(
        "f(A,B) with minterms {1,3}: K-map groups B column. "
        "Simplified: f = B."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Karnaugh map', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Karnaugh_map",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="flip_flop_state",
    content=(
        "A flip-flop is a bistable circuit that stores one bit. Types: "
        "SR (set-reset), D (data, Q follows D at clock edge), "
        "JK (toggle when J=K=1), T (toggle, complement Q). "
        "Characteristic equations: D: Q+ = D. JK: Q+ = J*Q' + K'*Q. T: Q+ = T XOR Q."
    ),
    example=(
        "D flip-flop: D=1 at rising clock edge -> Q=1. "
        "D=0 at next edge -> Q=0."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Flip-flop (electronics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Flip-flop_(electronics)",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="timing_analysis",
    content=(
        "Static timing analysis checks if signals arrive within clock period. "
        "Setup time: data must be stable t_setup before clock edge. "
        "Hold time: data must be stable t_hold after clock edge. "
        "Max clock frequency: f_max = 1 / (t_cq + t_logic + t_setup), "
        "where t_cq is clock-to-Q delay."
    ),
    example=(
        "t_cq = 2 ns, t_logic = 5 ns, t_setup = 1 ns. "
        "T_min = 2+5+1 = 8 ns. f_max = 1/8e-9 = 125 MHz."
    ),
    tier=5,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Static timing analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Static_timing_analysis",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="adder_circuit",
    content=(
        "A binary adder computes the sum of two binary numbers. Half adder: "
        "S = A XOR B, C = A AND B. Full adder adds carry-in: "
        "S = A XOR B XOR Cin, Cout = (A AND B) OR (Cin AND (A XOR B)). "
        "Ripple-carry adder chains n full adders for n-bit addition."
    ),
    example=(
        "Full adder: A=1, B=1, Cin=0. S = 1^1^0 = 0. "
        "Cout = (1&1) | (0&(1^1)) = 1|0 = 1. Result: 10 (binary 2)."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Adder (electronics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Adder_(electronics)",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="counter_design",
    content=(
        "A digital counter increments (or decrements) on each clock pulse. "
        "An n-bit binary counter counts from 0 to 2^n - 1. "
        "Synchronous counters: all flip-flops clock together (faster). "
        "Asynchronous (ripple): each FF clocks the next (simpler but slower). "
        "Modulus-N counter resets at count N."
    ),
    example=(
        "3-bit binary counter: counts 000->001->010->011->100->101->110->111->000. "
        "Modulus = 2^3 = 8."
    ),
    tier=5,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Counter (digital)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Counter_(digital)",
    prerequisites=["flip_flop_state"],
))

register_atom(Atom(
    atom_type="concept",
    name="multiplexer",
    content=(
        "A multiplexer (MUX) selects one of N input lines and routes it to "
        "a single output, controlled by select lines. A 2^n-to-1 MUX uses "
        "n select lines. Any Boolean function of n+1 variables can be "
        "implemented with a 2^n-to-1 MUX."
    ),
    example=(
        "4-to-1 MUX: inputs I0-I3, select S1,S0. "
        "S1=1, S0=0 -> output = I2."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Multiplexer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiplexer",
    prerequisites=["boolean_eval"],
))
