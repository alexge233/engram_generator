"""Knowledge atoms for classical mechanics (extended) and general chemistry.

Covers projectile motion, collisions, oscillations, rotational dynamics,
electron configuration, molecular geometry, and bonding.
Each atom has a Wikipedia source, worked example, and prerequisites.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Classical Mechanics -- extended (tiers 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="projectile_motion",
    content=(
        "Projectile motion is the motion of an object thrown or projected "
        "into the air, subject only to gravity. The horizontal range for "
        "a projectile launched at speed v_0 and angle theta on level "
        "ground is R = v_0^2 * sin(2*theta) / g. The maximum height is "
        "H = v_0^2 * sin^2(theta) / (2*g). The time of flight is "
        "T = 2*v_0*sin(theta) / g. These formulas assume no air "
        "resistance and constant gravitational acceleration g."
    ),
    example=(
        "Given v0=20 m/s, theta=30 deg, g=9.8 m/s^2: "
        "R = 20^2 * sin(60) / 9.8 = 400 * 0.866 / 9.8 = 35.35 m. "
        "H = 20^2 * sin^2(30) / (2*9.8) = 400 * 0.25 / 19.6 = 5.10 m."
    ),
    tier=4,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Projectile motion', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Projectile_motion",
    prerequisites=["kinematics_velocity", "kinematics_displacement"],
))

register_atom(Atom(
    atom_type="formula",
    name="circular_motion",
    content=(
        "Uniform circular motion is the motion of an object traveling at "
        "constant speed along a circular path of radius r. The centripetal "
        "acceleration is a_c = v^2 / r, directed toward the centre. The "
        "centripetal force is F_c = m * v^2 / r. The period of revolution "
        "is T = 2*pi*r / v, and the angular velocity is omega = v / r = "
        "2*pi / T."
    ),
    example=(
        "Given m=2 kg, v=5 m/s, r=4 m: "
        "a_c = 25/4 = 6.25 m/s^2. "
        "F_c = 2 * 25 / 4 = 12.5 N."
    ),
    tier=4,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Circular motion', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Circular_motion",
    prerequisites=["kinematics_velocity"],
))

register_atom(Atom(
    atom_type="formula",
    name="elastic_collision",
    content=(
        "An elastic collision is a collision in which both momentum and "
        "kinetic energy are conserved. For a 1D elastic collision between "
        "masses m1 and m2 with initial velocities u1 and u2, the final "
        "velocities are: v1 = ((m1-m2)*u1 + 2*m2*u2) / (m1+m2) and "
        "v2 = ((m2-m1)*u2 + 2*m1*u1) / (m1+m2). When m1 = m2, the "
        "objects exchange velocities."
    ),
    example=(
        "Given m1=3 kg, m2=1 kg, u1=4 m/s, u2=0: "
        "v1 = (3-1)*4 / (3+1) = 8/4 = 2 m/s. "
        "v2 = 2*3*4 / (3+1) = 24/4 = 6 m/s."
    ),
    tier=5,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Elastic collision', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Elastic_collision",
    prerequisites=["momentum", "kinetic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="inelastic_collision",
    content=(
        "An inelastic collision is one in which kinetic energy is not "
        "conserved, though momentum is. In a perfectly inelastic collision "
        "the two objects stick together after colliding. By conservation "
        "of momentum: m1*u1 + m2*u2 = (m1+m2)*v_f, so the final "
        "velocity is v_f = (m1*u1 + m2*u2) / (m1+m2). The kinetic "
        "energy lost is converted to heat, sound, or deformation."
    ),
    example=(
        "Given m1=4 kg, u1=6 m/s, m2=2 kg, u2=0 (perfectly inelastic): "
        "v_f = (4*6 + 2*0) / (4+2) = 24/6 = 4 m/s. "
        "KE_lost = 0.5*4*36 + 0 - 0.5*6*16 = 72 - 48 = 24 J."
    ),
    tier=4,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Inelastic collision', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Inelastic_collision",
    prerequisites=["momentum"],
))

register_atom(Atom(
    atom_type="formula",
    name="spring_oscillation",
    content=(
        "Simple harmonic motion of a mass-spring system: a mass m attached "
        "to a spring with spring constant k oscillates with angular "
        "frequency omega = sqrt(k/m), period T = 2*pi*sqrt(m/k), and "
        "frequency f = 1/(2*pi) * sqrt(k/m). The displacement is "
        "x(t) = A*cos(omega*t + phi), where A is the amplitude and phi "
        "the phase. The maximum velocity is v_max = A*omega and the "
        "maximum acceleration is a_max = A*omega^2."
    ),
    example=(
        "Given k=200 N/m, m=0.5 kg: "
        "omega = sqrt(200/0.5) = sqrt(400) = 20 rad/s. "
        "T = 2*pi/20 = 0.3142 s. f = 1/T = 3.1831 Hz."
    ),
    tier=4,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Simple harmonic motion', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Simple_harmonic_motion",
    prerequisites=["kinetic_energy", "potential_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="torque_rotation",
    content=(
        "Torque (moment of force) is the rotational analogue of linear "
        "force. The magnitude of torque about a pivot is tau = r * F * "
        "sin(theta), where r is the distance from the pivot to the point "
        "of force application, F is the magnitude of the force, and theta "
        "is the angle between the force vector and the lever arm. In "
        "vector form, tau = r x F. Newton's second law for rotation is "
        "tau = I * alpha, where I is the moment of inertia and alpha "
        "the angular acceleration."
    ),
    example=(
        "Given F=50 N applied at r=0.3 m, perpendicular (theta=90 deg): "
        "tau = 0.3 * 50 * sin(90) = 0.3 * 50 * 1 = 15 N*m."
    ),
    tier=5,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Torque', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Torque",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="moment_of_inertia_physics",
    content=(
        "The moment of inertia (rotational inertia) of a rigid body is a "
        "quantity that determines the torque needed for a desired angular "
        "acceleration about a rotational axis. For a point mass, I = m*r^2. "
        "For common shapes: solid cylinder I = (1/2)*M*R^2, solid sphere "
        "I = (2/5)*M*R^2, thin rod about centre I = (1/12)*M*L^2, thin "
        "rod about end I = (1/3)*M*L^2. The parallel axis theorem states "
        "I = I_cm + M*d^2."
    ),
    example=(
        "Solid cylinder, M=10 kg, R=0.5 m: "
        "I = 0.5 * 10 * 0.5^2 = 0.5 * 10 * 0.25 = 1.25 kg*m^2."
    ),
    tier=5,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Moment of inertia', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Moment_of_inertia",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="angular_momentum_conservation",
    content=(
        "Angular momentum L of a particle about a point is L = r x p = "
        "m * r * v * sin(theta), or for rotation about a fixed axis, "
        "L = I * omega, where I is the moment of inertia and omega the "
        "angular velocity. The law of conservation of angular momentum "
        "states that if no net external torque acts on a system, its total "
        "angular momentum remains constant: I_1 * omega_1 = I_2 * omega_2."
    ),
    example=(
        "Ice skater: I1=4.0 kg*m^2 at omega1=2 rad/s pulls arms in to "
        "I2=1.6 kg*m^2: omega2 = I1*omega1/I2 = 4.0*2/1.6 = 5.0 rad/s."
    ),
    tier=5,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Angular momentum', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Angular_momentum",
    prerequisites=["moment_of_inertia_physics", "momentum"],
))

register_atom(Atom(
    atom_type="formula",
    name="damped_oscillation",
    content=(
        "A damped harmonic oscillator experiences a resistive force "
        "proportional to velocity. The equation of motion is "
        "m*x'' + b*x' + k*x = 0, where b is the damping coefficient. "
        "The damping ratio is zeta = b / (2*sqrt(m*k)). When zeta < 1 "
        "(underdamped), the solution oscillates with exponentially "
        "decaying amplitude: x(t) = A * exp(-zeta*omega_n*t) * "
        "cos(omega_d*t + phi), where omega_n = sqrt(k/m) and "
        "omega_d = omega_n * sqrt(1 - zeta^2)."
    ),
    example=(
        "Given m=1 kg, k=100 N/m, b=4 Ns/m: "
        "omega_n = sqrt(100/1) = 10 rad/s. "
        "zeta = 4 / (2*sqrt(100)) = 4/20 = 0.2 (underdamped). "
        "omega_d = 10*sqrt(1 - 0.04) = 10*0.9798 = 9.798 rad/s."
    ),
    tier=5,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Harmonic oscillator', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Harmonic_oscillator",
    prerequisites=["spring_oscillation"],
))

register_atom(Atom(
    atom_type="formula",
    name="two_body_problem",
    content=(
        "The classical two-body problem reduces the motion of two "
        "gravitationally interacting masses m1, m2 to an equivalent "
        "one-body problem using the reduced mass mu = m1*m2/(m1+m2). "
        "The relative position vector satisfies mu*r'' = F(r). For a "
        "gravitational force, the solution yields Kepler orbits: "
        "ellipses, parabolas, or hyperbolas depending on total energy. "
        "The orbital period is T^2 = 4*pi^2*a^3 / (G*(m1+m2)), where "
        "a is the semi-major axis (Kepler's third law)."
    ),
    example=(
        "Given m1=5.97e24 kg (Earth), m2=7.35e22 kg (Moon), "
        "a=3.84e8 m: T^2 = 4*pi^2*(3.84e8)^3 / (6.674e-11 * "
        "6.05e24) = 5.63e24 / 4.04e14 = 2.37e6 s (27.4 days)."
    ),
    tier=6,
    domain="classical_mechanics",
    source=(
        "Wikipedia contributors, 'Two-body problem', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Two-body_problem",
    prerequisites=["gravitational_force", "angular_momentum_conservation"],
))


# =========================================================================
# General Chemistry (tiers 3-5)
# =========================================================================

register_atom(Atom(
    atom_type="rule",
    name="electron_config",
    content=(
        "The electron configuration of an atom describes the distribution "
        "of electrons among orbitals. Electrons fill orbitals in order of "
        "increasing energy following the Aufbau principle: 1s, 2s, 2p, 3s, "
        "3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p, 7s, 5f, 6d, 7p. "
        "Each orbital holds a maximum of 2 electrons (Pauli exclusion). "
        "Hund's rule states that electrons fill degenerate orbitals singly "
        "before pairing. Notable exceptions include Cr ([Ar] 3d^5 4s^1) "
        "and Cu ([Ar] 3d^10 4s^1) due to half-filled/filled subshell "
        "stability."
    ),
    example=(
        "Iron (Z=26): 1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^6, "
        "or [Ar] 3d^6 4s^2."
    ),
    tier=3,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Electron configuration', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Electron_configuration",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="periodic_trend",
    content=(
        "Periodic trends describe predictable patterns in element "
        "properties across the periodic table. Atomic radius decreases "
        "left to right across a period (increasing nuclear charge) and "
        "increases top to bottom down a group (additional electron shells). "
        "Ionisation energy increases left to right and decreases down a "
        "group. Electronegativity increases toward the upper right (F is "
        "highest at 3.98). Electron affinity generally increases left to "
        "right, with halogens having the most negative values."
    ),
    example=(
        "Compare Na and Cl: Na has larger atomic radius (190 pm vs 79 pm), "
        "lower ionisation energy (496 vs 1251 kJ/mol), and lower "
        "electronegativity (0.93 vs 3.16)."
    ),
    tier=3,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Periodic trends', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Periodic_trends",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="lewis_structure",
    content=(
        "A Lewis structure shows the bonding between atoms and lone pairs "
        "of electrons. To draw one: (1) count total valence electrons, "
        "(2) place the least electronegative atom as the central atom, "
        "(3) connect atoms with single bonds, (4) distribute remaining "
        "electrons as lone pairs to satisfy octets (duet for H), "
        "(5) if electrons are insufficient for octets, form double or "
        "triple bonds. Formal charge = valence electrons - lone pair "
        "electrons - (1/2)*bonding electrons. The best structure "
        "minimises formal charges."
    ),
    example=(
        "CO2: C has 4 valence e-, each O has 6. Total = 16 e-. "
        "Structure: O=C=O, each O has 2 lone pairs. Formal charges: "
        "C = 4 - 0 - 4 = 0, O = 6 - 4 - 2 = 0."
    ),
    tier=4,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Lewis structure', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lewis_structure",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="rule",
    name="vsepr_geometry",
    content=(
        "VSEPR (Valence Shell Electron Pair Repulsion) theory predicts "
        "molecular geometry from the number of bonding pairs (BP) and "
        "lone pairs (LP) around the central atom. Key geometries: "
        "2 BP, 0 LP = linear (180 deg); 3 BP, 0 LP = trigonal planar "
        "(120 deg); 2 BP, 1 LP = bent (~117 deg); 4 BP, 0 LP = "
        "tetrahedral (109.5 deg); 3 BP, 1 LP = trigonal pyramidal "
        "(~107 deg); 2 BP, 2 LP = bent (~104.5 deg); 5 BP, 0 LP = "
        "trigonal bipyramidal; 6 BP, 0 LP = octahedral."
    ),
    example=(
        "H2O: O has 2 bonding pairs (to H) and 2 lone pairs. "
        "Steric number = 4 (tetrahedral electron geometry). "
        "Molecular geometry = bent, bond angle ~104.5 deg."
    ),
    tier=4,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'VSEPR theory', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/VSEPR_theory",
    prerequisites=["lewis_structure"],
))

register_atom(Atom(
    atom_type="rule",
    name="hybridisation",
    content=(
        "Orbital hybridisation is the mixing of atomic orbitals to form "
        "new hybrid orbitals suitable for bonding. sp hybridisation (2 "
        "hybrid orbitals, linear, 180 deg) forms when an atom has 2 "
        "electron domains. sp2 (3 orbitals, trigonal planar, 120 deg) "
        "for 3 domains. sp3 (4 orbitals, tetrahedral, 109.5 deg) for "
        "4 domains. sp3d (5, trigonal bipyramidal) for 5, and sp3d2 "
        "(6, octahedral) for 6 domains. The number of sigma bonds plus "
        "lone pairs on the central atom equals the number of hybrid "
        "orbitals."
    ),
    example=(
        "Methane CH4: C has 4 bonding pairs, 0 lone pairs. "
        "4 electron domains = sp3 hybridisation. "
        "Geometry: tetrahedral, 109.5 deg bond angles."
    ),
    tier=4,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Orbital hybridisation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Orbital_hybridisation",
    prerequisites=["vsepr_geometry"],
))

register_atom(Atom(
    atom_type="rule",
    name="oxidation_state",
    content=(
        "The oxidation state (oxidation number) of an atom is a measure "
        "of the degree of oxidation. Rules for assignment: (1) free "
        "elements have oxidation state 0; (2) monoatomic ions equal their "
        "charge; (3) oxygen is usually -2 (except in peroxides -1, OF2 "
        "+2); (4) hydrogen is usually +1 (except in metal hydrides -1); "
        "(5) fluorine is always -1; (6) the sum of oxidation states in a "
        "neutral compound is 0; (7) the sum in a polyatomic ion equals "
        "the ion charge."
    ),
    example=(
        "KMnO4: K = +1, O = -2 (x4 = -8). "
        "Sum = 0: +1 + Mn + (-8) = 0, so Mn = +7."
    ),
    tier=4,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Oxidation state', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Oxidation_state",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="definition",
    name="electronegativity_bond",
    content=(
        "Electronegativity is a measure of an atom's ability to attract "
        "shared electrons in a chemical bond (Pauling scale). The "
        "difference in electronegativity (delta EN) between two bonded "
        "atoms determines bond character: delta EN < 0.4 = nonpolar "
        "covalent; 0.4 <= delta EN < 1.7 = polar covalent; delta EN >= "
        "1.7 = ionic. Fluorine has the highest electronegativity (3.98), "
        "followed by oxygen (3.44), nitrogen (3.04), and chlorine (3.16)."
    ),
    example=(
        "NaCl: EN(Na) = 0.93, EN(Cl) = 3.16. "
        "delta EN = 3.16 - 0.93 = 2.23 >= 1.7, so ionic bond."
    ),
    tier=3,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Electronegativity', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Electronegativity",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="ideal_gas_stoich",
    content=(
        "At standard temperature and pressure (STP: 0 deg C, 1 atm), "
        "one mole of an ideal gas occupies 22.414 L (molar volume). "
        "Combined with stoichiometric coefficients, this allows "
        "volume-based calculations for gas-phase reactions. For a "
        "reaction aA + bB -> cC, if A and C are gases at STP, then "
        "volume_C = (c/a) * volume_A. The ideal gas law PV = nRT "
        "generalises to non-STP conditions with R = 8.314 J/(mol*K) "
        "or 0.08206 L*atm/(mol*K)."
    ),
    example=(
        "2H2 + O2 -> 2H2O: 4.48 L of H2 at STP = 4.48/22.414 = 0.2 mol. "
        "Requires 0.1 mol O2 = 2.241 L at STP. "
        "Produces 0.2 mol H2O."
    ),
    tier=5,
    domain="general_chemistry",
    source=(
        "Wikipedia contributors, 'Ideal gas law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Ideal_gas_law",
    prerequisites=["ideal_gas", "molar_mass"],
))
