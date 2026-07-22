"""Knowledge atoms for electromagnetism generators.

Registers formula and law atoms covering electrostatics, magnetostatics,
and electromagnetic induction. Each atom is sourced from Wikipedia with
a worked example for verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Electrostatics (tiers 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="coulombs_law",
    content=(
        "Coulomb's law states that the magnitude of the electrostatic "
        "force between two point charges is directly proportional to "
        "the product of the magnitudes of the charges and inversely "
        "proportional to the square of the distance between them: "
        "F = k * |q1 * q2| / r^2, where k = 8.9875517873681764e9 "
        "N m^2 C^-2 is Coulomb's constant (also written as "
        "1 / (4 * pi * epsilon_0)), q1 and q2 are the signed "
        "magnitudes of the charges, and r is the separation distance. "
        "The force is attractive for unlike charges and repulsive for "
        "like charges. The law was first published by Charles-Augustin "
        "de Coulomb in 1785."
    ),
    example=(
        "Given q1 = 2e-6 C, q2 = 3e-6 C, r = 0.1 m: "
        "F = 8.9876e9 * 2e-6 * 3e-6 / 0.1^2 "
        "= 8.9876e9 * 6e-12 / 0.01 = 5.3925 N"
    ),
    tier=4,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Coulomb's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Coulomb%27s_law",
    prerequisites=["multiplication", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="electric_field",
    content=(
        "The electric field E at a point in space due to a point "
        "charge Q is defined as the force per unit positive test "
        "charge: E = k * Q / r^2, where k = 8.9876e9 N m^2 C^-2, "
        "Q is the source charge in coulombs, and r is the distance "
        "from the charge to the field point in metres. The field "
        "points radially outward from a positive charge and radially "
        "inward toward a negative charge. The SI unit of electric "
        "field is volts per metre (V/m) or equivalently newtons per "
        "coulomb (N/C)."
    ),
    example=(
        "Given Q = 5e-6 C, r = 0.2 m: "
        "E = 8.9876e9 * 5e-6 / 0.2^2 "
        "= 8.9876e9 * 5e-6 / 0.04 = 1.1235e6 V/m"
    ),
    tier=5,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Electric field', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Electric_field",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="law",
    name="gauss_law",
    content=(
        "Gauss's law for electricity states that the total electric "
        "flux through any closed surface is proportional to the "
        "enclosed electric charge: Phi_E = Q_enc / epsilon_0, where "
        "Phi_E is the electric flux through the closed surface, "
        "Q_enc is the total charge enclosed by the surface, and "
        "epsilon_0 = 8.8542e-12 F/m is the vacuum permittivity. "
        "In integral form: the surface integral of E dot dA over a "
        "closed surface equals Q_enc / epsilon_0. Gauss's law is one "
        "of Maxwell's four equations and is equivalent to Coulomb's "
        "law for static charges."
    ),
    example=(
        "Given Q_enc = 1e-9 C: "
        "Phi_E = 1e-9 / 8.8542e-12 = 112.94 V m"
    ),
    tier=5,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Gauss's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Gauss%27s_law",
    prerequisites=["electric_field"],
))

register_atom(Atom(
    atom_type="formula",
    name="electric_potential",
    content=(
        "The electric potential V at a distance r from a point charge "
        "Q is the work done per unit charge in bringing a positive "
        "test charge from infinity to that point: V = k * Q / r, "
        "where k = 8.9876e9 N m^2 C^-2, Q is the source charge, "
        "and r is the distance from the charge. Unlike the electric "
        "field which is a vector quantity, the electric potential is "
        "a scalar. The SI unit is the volt (V). The potential "
        "difference between two points equals the negative line "
        "integral of the electric field between those points."
    ),
    example=(
        "Given Q = 4e-6 C, r = 0.5 m: "
        "V = 8.9876e9 * 4e-6 / 0.5 = 71900.8 V"
    ),
    tier=5,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Electric potential', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Electric_potential",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="capacitance",
    content=(
        "Capacitance is the ratio of the amount of electric charge "
        "stored on a conductor to a difference in electric potential. "
        "For a parallel-plate capacitor: C = epsilon_0 * A / d, "
        "where epsilon_0 = 8.8542e-12 F/m is the vacuum permittivity, "
        "A is the area of one plate in m^2, and d is the separation "
        "between the plates in metres. With a dielectric material "
        "between the plates: C = epsilon_r * epsilon_0 * A / d, "
        "where epsilon_r is the relative permittivity (dielectric "
        "constant) of the material. The SI unit of capacitance is "
        "the farad (F)."
    ),
    example=(
        "Given A = 0.01 m^2, d = 0.001 m (vacuum): "
        "C = 8.8542e-12 * 0.01 / 0.001 = 8.8542e-11 F = 88.54 pF"
    ),
    tier=4,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Capacitance', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Capacitance",
    prerequisites=["division", "multiplication"],
))


# ---------------------------------------------------------------------------
# Magnetostatics (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="magnetic_force",
    content=(
        "The magnetic component of the Lorentz force on a charged "
        "particle moving in a magnetic field is: F = q * v * B * "
        "sin(theta), where q is the electric charge, v is the speed "
        "of the particle, B is the magnetic flux density, and theta "
        "is the angle between the velocity vector and the magnetic "
        "field vector. In vector form: F = q(v x B), the cross "
        "product of velocity and field. The force is always "
        "perpendicular to both the velocity and the field, so it "
        "does no work on the particle (it changes direction but not "
        "speed). The SI unit of magnetic flux density is the tesla (T)."
    ),
    example=(
        "Given q = 1.6e-19 C, v = 3e6 m/s, B = 0.5 T, theta = 90 deg: "
        "F = 1.6e-19 * 3e6 * 0.5 * sin(90) = 2.4e-13 N"
    ),
    tier=5,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Lorentz force', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lorentz_force",
    prerequisites=["cross_product"],
))

register_atom(Atom(
    atom_type="law",
    name="lenz_law",
    content=(
        "Lenz's law states that the direction of the current induced "
        "in a conductor by a changing magnetic field is such that the "
        "magnetic field created by the induced current opposes the "
        "change in the original magnetic field. This is a consequence "
        "of conservation of energy. Mathematically, it is expressed "
        "by the negative sign in Faraday's law of induction: "
        "EMF = -d(Phi_B)/dt. If the magnetic flux through a loop is "
        "increasing, the induced current flows in the direction that "
        "creates a magnetic field opposing the increase. If the flux "
        "is decreasing, the induced current creates a field in the "
        "same direction as the original, opposing the decrease."
    ),
    example=(
        "Given Phi_B increasing from 0.1 Wb to 0.3 Wb in 0.5 s: "
        "EMF = -(0.3 - 0.1) / 0.5 = -0.4 V "
        "(negative sign means opposing direction)"
    ),
    tier=5,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Lenz's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lenz%27s_law",
    prerequisites=["multiplication"],
))


# ---------------------------------------------------------------------------
# Electromagnetic induction (tier 6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="faraday_law",
    content=(
        "Faraday's law of electromagnetic induction states that the "
        "electromotive force (EMF) induced in a closed loop is equal "
        "to the negative rate of change of the magnetic flux through "
        "the loop: EMF = -N * d(Phi_B)/dt, where N is the number of "
        "turns in the coil, Phi_B = B * A * cos(theta) is the "
        "magnetic flux, B is the magnetic field strength, A is the "
        "area of the loop, and theta is the angle between the field "
        "and the area normal. The negative sign reflects Lenz's law. "
        "Faraday's law is one of Maxwell's four equations and is the "
        "basis of electric generators, transformers, and inductors."
    ),
    example=(
        "Given N = 100 turns, B changing from 0.5 T to 0.2 T in 0.1 s, "
        "A = 0.04 m^2, theta = 0: "
        "EMF = -100 * (0.2*0.04 - 0.5*0.04) / 0.1 "
        "= -100 * (-0.012) / 0.1 = 12.0 V"
    ),
    tier=6,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Faraday's law of induction', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Faraday%27s_law_of_induction",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="poynting_vector",
    content=(
        "The Poynting vector S represents the directional energy flux "
        "(the energy transfer per unit area per unit time) of an "
        "electromagnetic field. It is defined as: S = (1/mu_0) * "
        "(E x B), where E is the electric field vector, B is the "
        "magnetic field vector, and mu_0 = 4*pi*1e-7 T m/A is the "
        "vacuum permeability. For a plane wave in vacuum, the time-"
        "averaged intensity is: <S> = E_0^2 / (2 * mu_0 * c), where "
        "E_0 is the peak electric field and c is the speed of light. "
        "The SI unit is watts per square metre (W/m^2)."
    ),
    example=(
        "Given E_0 = 100 V/m in vacuum: "
        "<S> = 100^2 / (2 * 4*pi*1e-7 * 3e8) "
        "= 10000 / 753.98 = 13.26 W/m^2"
    ),
    tier=6,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Poynting vector', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Poynting_vector",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="maxwell_displacement",
    content=(
        "Maxwell's correction to Ampere's law introduces the "
        "displacement current density: J_D = epsilon_0 * dE/dt, "
        "where epsilon_0 = 8.8542e-12 F/m is the vacuum permittivity "
        "and dE/dt is the time rate of change of the electric field. "
        "The generalised Ampere's law becomes: curl(B) = mu_0 * "
        "(J + epsilon_0 * dE/dt), where J is the conduction current "
        "density. The displacement current term is essential for the "
        "consistency of Maxwell's equations and predicts the existence "
        "of electromagnetic waves. Between the plates of a charging "
        "capacitor where no conduction current flows, the changing "
        "electric field acts as an effective current source for the "
        "magnetic field."
    ),
    example=(
        "Given dE/dt = 1e12 V/(m s), plate area A = 0.01 m^2: "
        "I_D = epsilon_0 * dE/dt * A "
        "= 8.8542e-12 * 1e12 * 0.01 = 0.0885 A"
    ),
    tier=6,
    domain="electromagnetism",
    source=(
        "Wikipedia contributors, 'Displacement current', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Displacement_current",
    prerequisites=["faraday_law"],
))
