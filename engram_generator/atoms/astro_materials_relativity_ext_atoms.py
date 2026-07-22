"""Knowledge atoms for astronomy_ext, materials_ext, and relativity_ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── ASTRONOMY EXT ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="stellar_classification",
    content=(
        "The Morgan-Keenan (MK) system classifies stars by spectral "
        "type (O, B, A, F, G, K, M) based on surface temperature, and "
        "luminosity class (I-V) based on absolute magnitude. O stars "
        "are hottest (>30,000 K), M stars coolest (<3,500 K). The Sun "
        "is classified as G2V."
    ),
    example=(
        "A star with T=5,800 K and luminosity class V: spectral type "
        "G (5,200-6,000 K range), luminosity class V (main sequence). "
        "Classification: G2V."
    ),
    tier=4, domain="astronomy",
    source="Wikipedia contributors, 'Stellar classification', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Stellar_classification",
    prerequisites=["temperature"],
))

register_atom(Atom(
    atom_type="formula",
    name="luminosity_distance",
    content=(
        "Luminosity distance relates the apparent luminosity of an "
        "astronomical object to its absolute luminosity: "
        "d_L = sqrt(L / (4*pi*F)), where L is absolute luminosity, "
        "F is observed flux. For cosmological redshift z: "
        "d_L = (1+z) * d_comoving."
    ),
    example=(
        "Given L = 3.828e26 W, F = 1361 W/m^2: "
        "d_L = sqrt(3.828e26 / (4*pi*1361)) = sqrt(2.24e22) = "
        "1.496e11 m = 1 AU."
    ),
    tier=5, domain="astronomy",
    source="Wikipedia contributors, 'Luminosity distance', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Luminosity_distance",
    prerequisites=["parallax_distance"],
))

register_atom(Atom(
    atom_type="formula",
    name="mass_luminosity",
    content=(
        "The mass-luminosity relation for main-sequence stars: "
        "L/L_sun ~ (M/M_sun)^a, where a ~ 3.5 for most stars. "
        "More massive stars are much more luminous but burn fuel faster."
    ),
    example=(
        "Given M = 2 M_sun: L = L_sun * (2)^3.5 = L_sun * 11.31. "
        "A 2 solar mass star is about 11.3 times as luminous as the Sun."
    ),
    tier=5, domain="astronomy",
    source="Wikipedia contributors, 'Mass-luminosity relation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation",
    prerequisites=["stellar_luminosity"],
))

register_atom(Atom(
    atom_type="formula",
    name="chandrasekhar_limit",
    content=(
        "The Chandrasekhar limit is the maximum mass of a stable white "
        "dwarf star: M_Ch ~ 1.4 M_sun = 5.83 / (mu_e)^2 * M_sun, "
        "where mu_e is the mean molecular weight per electron. Above "
        "this limit, electron degeneracy pressure cannot support the star."
    ),
    example=(
        "For pure carbon-12 (mu_e = 2): M_Ch = 5.83 / 4 * M_sun = "
        "1.457 M_sun ~ 1.4 M_sun."
    ),
    tier=5, domain="astronomy",
    source="Wikipedia contributors, 'Chandrasekhar limit', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Chandrasekhar_limit",
    prerequisites=["stellar_luminosity"],
))

register_atom(Atom(
    atom_type="formula",
    name="hubble_time",
    content=(
        "The Hubble time is the reciprocal of the Hubble constant, "
        "giving an estimate of the age of the universe: "
        "t_H = 1/H_0. For H_0 = 70 km/s/Mpc, t_H ~ 14.0 Gyr."
    ),
    example=(
        "Given H_0 = 70 km/s/Mpc: t_H = 1/H_0 = 1/(70 km/s/Mpc). "
        "Converting: 1 Mpc = 3.086e19 km, so t_H = 3.086e19/70 s = "
        "4.409e17 s = 13.97 Gyr."
    ),
    tier=4, domain="astronomy",
    source="Wikipedia contributors, 'Hubble time', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hubble%27s_law#Hubble_time",
    prerequisites=["hubble_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="angular_diameter",
    content=(
        "The angular diameter (or angular size) of an object as seen "
        "from a given point: delta = 2 * arctan(d / (2*D)), where d "
        "is the physical diameter and D is the distance. For small "
        "angles: delta ~ d/D (in radians)."
    ),
    example=(
        "Given d = 3474 km (Moon diameter), D = 384400 km: "
        "delta = 3474/384400 = 0.00904 rad = 0.518 deg ~ 31 arcmin."
    ),
    tier=4, domain="astronomy",
    source="Wikipedia contributors, 'Angular diameter', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Angular_diameter",
    prerequisites=["parallax_distance"],
))

register_atom(Atom(
    atom_type="theorem",
    name="virial_theorem",
    content=(
        "The virial theorem states that for a stable, "
        "self-gravitating system: 2<K> + <V> = 0, where <K> is the "
        "time-averaged kinetic energy and <V> is the time-averaged "
        "gravitational potential energy. Equivalently: <K> = -<V>/2."
    ),
    example=(
        "Given a galaxy cluster with <V> = -4e46 J: "
        "<K> = -(-4e46)/2 = 2e46 J. Total energy E = <K> + <V> = "
        "2e46 - 4e46 = -2e46 J (bound system)."
    ),
    tier=5, domain="astronomy",
    source="Wikipedia contributors, 'Virial theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Virial_theorem",
    prerequisites=["kinetic_energy", "gravitational_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="saha_equation",
    content=(
        "The Saha equation relates the ionisation state of an element "
        "to temperature and electron density: "
        "n_{i+1}*n_e / n_i = (2/lambda^3) * (g_{i+1}/g_i) * "
        "exp(-chi/(k_B*T)), where chi is the ionisation energy, "
        "lambda is the thermal de Broglie wavelength, and g are "
        "statistical weights."
    ),
    example=(
        "For hydrogen at T=10000 K, n_e=1e14 cm^-3: "
        "n_II/n_I ~ 2.4e15/1e14 * exp(-13.6*1.6e-19/(1.38e-23*10000)) "
        "~ 24 * exp(-15.8) ~ 3.3e-6. Mostly neutral at this temperature."
    ),
    tier=6, domain="astronomy",
    source="Wikipedia contributors, 'Saha ionization equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Saha_ionization_equation",
    prerequisites=["boltzmann_probability"],
))


# ── MATERIALS EXT ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="hardness_test",
    content=(
        "Brinell hardness number (BHN) is measured by pressing a "
        "hardened steel ball into a material: "
        "BHN = 2F / (pi*D*(D - sqrt(D^2 - d^2))), where F is the "
        "applied force (N), D is ball diameter (mm), and d is "
        "indentation diameter (mm)."
    ),
    example=(
        "Given F=29420 N (3000 kgf), D=10 mm, d=4 mm: "
        "BHN = 2*29420 / (pi*10*(10 - sqrt(100-16))) = "
        "58840 / (31.416*(10-9.165)) = 58840/26.23 = 2243 BHN."
    ),
    tier=4, domain="materials_science",
    source="Wikipedia contributors, 'Brinell scale', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Brinell_scale",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="fatigue_sn_curve",
    content=(
        "The S-N curve (Wohler curve) relates stress amplitude S to "
        "the number of cycles to failure N: S = a * N^b (power law), "
        "or equivalently log(N) = c - m*log(S). The endurance limit "
        "is the stress below which failure never occurs."
    ),
    example=(
        "Given a = 1000 MPa, b = -0.1: at S = 500 MPa: "
        "500 = 1000 * N^(-0.1), N^(-0.1) = 0.5, "
        "N = 0.5^(-10) = 1024 cycles."
    ),
    tier=5, domain="materials_science",
    source="Wikipedia contributors, 'Fatigue (material)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fatigue_(material)#Characteristics_of_fatigue",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="creep_rate",
    content=(
        "Steady-state creep rate follows the Arrhenius-type power law: "
        "d_epsilon/dt = A * sigma^n * exp(-Q/(R*T)), where A is a "
        "material constant, sigma is applied stress, n is the stress "
        "exponent, Q is the activation energy, R is the gas constant, "
        "and T is absolute temperature."
    ),
    example=(
        "Given A=2e-10, sigma=100 MPa, n=3, Q=200 kJ/mol, T=800 K: "
        "rate = 2e-10 * 100^3 * exp(-200000/(8.314*800)) = "
        "2e-10 * 1e6 * exp(-30.1) = 2e-4 * 8.2e-14 = 1.64e-17 /s."
    ),
    tier=5, domain="materials_science",
    source="Wikipedia contributors, 'Creep (deformation)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Creep_(deformation)",
    prerequisites=["arrhenius"],
))

register_atom(Atom(
    atom_type="formula",
    name="fracture_toughness",
    content=(
        "The stress intensity factor K_I for a through-thickness crack "
        "of length 2a in an infinite plate under tension sigma: "
        "K_I = sigma * sqrt(pi*a). Fracture occurs when K_I >= K_IC "
        "(the critical stress intensity factor or fracture toughness)."
    ),
    example=(
        "Given sigma = 200 MPa, a = 5 mm = 0.005 m: "
        "K_I = 200 * sqrt(pi*0.005) = 200 * 0.1253 = 25.07 MPa*sqrt(m). "
        "If K_IC = 30 MPa*sqrt(m), the crack is stable (K_I < K_IC)."
    ),
    tier=5, domain="materials_science",
    source="Wikipedia contributors, 'Fracture toughness', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fracture_toughness",
    prerequisites=["stress_strain"],
))

register_atom(Atom(
    atom_type="formula",
    name="corrosion_rate",
    content=(
        "Corrosion rate from mass loss: CR = (K * W) / (A * T * D), "
        "where K is a constant (depends on units), W is weight loss, "
        "A is exposed area, T is exposure time, and D is density. "
        "Units commonly in mm/year or mils/year (mpy)."
    ),
    example=(
        "Given W=0.5 g, A=10 cm^2, T=720 h, D=7.87 g/cm^3, "
        "K=8.76e4 (for mm/year): CR = 8.76e4 * 0.5 / (10*720*7.87) = "
        "43800 / 56664 = 0.773 mm/year."
    ),
    tier=4, domain="materials_science",
    source="Wikipedia contributors, 'Corrosion', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Corrosion#Measurements",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="composite_rule_mixtures",
    content=(
        "The rule of mixtures estimates composite properties from "
        "constituent properties: E_c = V_f*E_f + V_m*E_m, where "
        "E_c is composite modulus, V_f and V_m are volume fractions "
        "of fiber and matrix, E_f and E_m are their moduli."
    ),
    example=(
        "Given E_f=230 GPa (carbon fiber), E_m=3.5 GPa (epoxy), "
        "V_f=0.6: E_c = 0.6*230 + 0.4*3.5 = 138 + 1.4 = 139.4 GPa."
    ),
    tier=4, domain="materials_science",
    source="Wikipedia contributors, 'Rule of mixtures', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Rule_of_mixtures",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="definition",
    name="heat_treatment",
    content=(
        "Heat treatment modifies metal microstructure through "
        "controlled heating and cooling. Key processes: annealing "
        "(soften, relieve stress), quenching (rapid cool for hardness), "
        "tempering (reheat quenched steel to reduce brittleness), "
        "normalising (air cool from austenitising temperature)."
    ),
    example=(
        "1045 steel quenched from 850 C: HRC ~ 55-60 (very hard, "
        "brittle). Tempered at 400 C for 1 hour: HRC ~ 40-45 "
        "(reduced hardness, improved toughness)."
    ),
    tier=4, domain="materials_science",
    source="Wikipedia contributors, 'Heat treating', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Heat_treating",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="grain_size",
    content=(
        "The Hall-Petch equation relates yield stress to grain size: "
        "sigma_y = sigma_0 + k_y / sqrt(d), where sigma_0 is the "
        "friction stress (lattice resistance), k_y is the Hall-Petch "
        "slope, and d is the average grain diameter."
    ),
    example=(
        "Given sigma_0=50 MPa, k_y=0.5 MPa*sqrt(m), d=25 um=25e-6 m: "
        "sigma_y = 50 + 0.5/sqrt(25e-6) = 50 + 0.5/5e-3 = "
        "50 + 100 = 150 MPa."
    ),
    tier=5, domain="materials_science",
    source="Wikipedia contributors, 'Hall-Petch relationship', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Grain_boundary_strengthening",
    prerequisites=["division"],
))


# ── RELATIVITY EXT ─────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="relativistic_momentum",
    content=(
        "Relativistic momentum: p = gamma*m*v, where "
        "gamma = 1/sqrt(1 - v^2/c^2) is the Lorentz factor. "
        "As v approaches c, p approaches infinity."
    ),
    example=(
        "Given m=1 kg, v=0.8c: gamma = 1/sqrt(1-0.64) = 1/0.6 = 5/3. "
        "p = (5/3)*1*0.8c = (4/3)*c = 4e8 kg*m/s."
    ),
    tier=5, domain="relativity",
    source="Wikipedia contributors, 'Relativistic mechanics', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Relativistic_mechanics#Relativistic_momentum",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="mass_energy_equivalence",
    content=(
        "Einstein's mass-energy equivalence: E = mc^2, where E is "
        "rest energy, m is rest mass, and c is the speed of light "
        "(2.998e8 m/s). For total energy: E = gamma*m*c^2."
    ),
    example=(
        "Given m=1 kg: E = 1 * (3e8)^2 = 9e16 J = 90 PJ. "
        "This equals about 21.5 megatons of TNT."
    ),
    tier=5, domain="relativity",
    source="Wikipedia contributors, 'Mass-energy equivalence', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence",
    prerequisites=["relativistic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="relativistic_doppler",
    content=(
        "The relativistic Doppler effect for light: "
        "f_obs = f_src * sqrt((1-beta)/(1+beta)) for recession, "
        "where beta = v/c. For approach, swap signs. "
        "This combines classical Doppler with time dilation."
    ),
    example=(
        "Given f_src = 6e14 Hz, v = 0.5c (recession): "
        "f_obs = 6e14 * sqrt(0.5/1.5) = 6e14 * sqrt(1/3) = "
        "6e14 * 0.5774 = 3.464e14 Hz (redshifted)."
    ),
    tier=5, domain="relativity",
    source="Wikipedia contributors, 'Relativistic Doppler effect', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Relativistic_Doppler_effect",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="twin_paradox",
    content=(
        "In the twin paradox, a twin travels at speed v for proper "
        "time tau, while the stay-at-home twin ages by t = gamma*tau. "
        "The traveling twin is younger by Delta_t = (gamma-1)*tau. "
        "Resolution: the traveling twin undergoes acceleration, "
        "breaking the symmetry."
    ),
    example=(
        "Given v=0.9c, tau=10 years (traveler's time): "
        "gamma = 1/sqrt(1-0.81) = 1/0.4359 = 2.294. "
        "Stay-home twin ages t = 2.294*10 = 22.94 years. "
        "Difference = 12.94 years."
    ),
    tier=6, domain="relativity",
    source="Wikipedia contributors, 'Twin paradox', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Twin_paradox",
    prerequisites=["time_dilation"],
))

register_atom(Atom(
    atom_type="formula",
    name="compton_scattering",
    content=(
        "Compton scattering: a photon scatters off a free electron, "
        "changing wavelength by Delta_lambda = (h/(m_e*c))*(1-cos(theta)), "
        "where h/(m_e*c) = 2.426e-12 m is the Compton wavelength "
        "of the electron and theta is the scattering angle."
    ),
    example=(
        "Given theta=90 degrees: Delta_lambda = 2.426e-12 * (1-cos(90)) "
        "= 2.426e-12 * 1 = 2.426e-12 m = 0.02426 Angstroms."
    ),
    tier=6, domain="relativity",
    source="Wikipedia contributors, 'Compton scattering', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Compton_scattering",
    prerequisites=["photon_momentum"],
))

register_atom(Atom(
    atom_type="formula",
    name="relativistic_kinetic",
    content=(
        "Relativistic kinetic energy: KE = (gamma - 1)*m*c^2, "
        "where gamma = 1/sqrt(1-v^2/c^2). At low speeds this "
        "reduces to the classical KE = (1/2)*m*v^2."
    ),
    example=(
        "Given m=1 kg, v=0.6c: gamma = 1/sqrt(1-0.36) = 1/0.8 = 1.25. "
        "KE = (1.25-1)*1*(3e8)^2 = 0.25*9e16 = 2.25e16 J."
    ),
    tier=5, domain="relativity",
    source="Wikipedia contributors, 'Kinetic energy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Kinetic_energy#Relativistic_kinetic_energy",
    prerequisites=["lorentz_factor", "kinetic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="invariant_mass_two_particle",
    content=(
        "The invariant mass of a two-particle system: "
        "M^2*c^4 = (E1+E2)^2 - (p1+p2)^2*c^2, where E_i are "
        "energies and p_i are momenta. This is Lorentz invariant -- "
        "the same in all reference frames."
    ),
    example=(
        "Two photons with E1=E2=100 MeV moving in opposite directions "
        "(p1=-p2): M^2*c^4 = (200)^2 - 0 = 40000 MeV^2. "
        "M = 200 MeV/c^2 (e.g., pi0 decay)."
    ),
    tier=6, domain="relativity",
    source="Wikipedia contributors, 'Invariant mass', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Invariant_mass",
    prerequisites=["relativistic_energy", "relativistic_momentum"],
))

register_atom(Atom(
    atom_type="formula",
    name="photon_momentum",
    content=(
        "A photon has zero rest mass but carries momentum: "
        "p = E/c = h*f/c = h/lambda, where E is photon energy, "
        "h is Planck's constant, f is frequency, and lambda is "
        "wavelength."
    ),
    example=(
        "Given lambda = 500 nm = 5e-7 m: "
        "p = 6.626e-34 / 5e-7 = 1.325e-27 kg*m/s."
    ),
    tier=5, domain="relativity",
    source="Wikipedia contributors, 'Photon', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Photon#Physical_properties",
    prerequisites=["wavelength_energy"],
))
