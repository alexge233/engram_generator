"""Knowledge atoms for physics and astrophysics domains.

Registers formula and principle atoms covering classical mechanics,
waves, electromagnetism, thermodynamics, gravitation, orbital mechanics,
and astrophysics/cosmology. Each atom stores the full authoritative
statement sourced from Wikipedia, its tier, domain, source citation,
source URL, and prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Physics -- mechanics (tier 4)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="kinematics_velocity",
    content=(
        "The first equation of motion for uniform acceleration relates "
        "final velocity to initial velocity, acceleration, and time: "
        "v = v_0 + at, where v is the final velocity, v_0 is the initial "
        "velocity, a is the uniform acceleration, and t is the time "
        "elapsed. This equation is one of the SUVAT equations, named "
        "after their variables: s (displacement), u (initial velocity), "
        "v (final velocity), a (acceleration), and t (time). These "
        "equations are valid only when acceleration is constant "
        "(uniform acceleration) and motion is along a straight line."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Equations of motion', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Equations_of_motion",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="kinematics_displacement",
    content=(
        "The second SUVAT equation of motion relates displacement to "
        "initial velocity, acceleration, and time: s = v_0 t + (1/2)at^2, "
        "where s is the displacement, v_0 is the initial velocity, a is "
        "the uniform acceleration, and t is the time elapsed. This "
        "equation is derived by integrating the velocity equation "
        "v = v_0 + at with respect to time. It applies only under "
        "constant acceleration along a straight line. Together with the "
        "other kinematic equations, it describes the motion of objects "
        "in classical mechanics without reference to the forces that "
        "cause the motion."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Equations of motion', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Equations_of_motion",
    prerequisites=["multiplication", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="kinetic_energy",
    content=(
        "In classical mechanics, the kinetic energy of a non-rotating "
        "rigid body depends on the mass of the body as well as its "
        "speed. The kinetic energy is equal to one half the product of "
        "the body's mass and the square of its speed: KE = (1/2)mv^2, "
        "where m is the mass and v is the speed (or the velocity) of "
        "the body. In SI units, mass is measured in kilograms, speed in "
        "metres per second, and the resulting kinetic energy is in "
        "joules. The formula (1/2)mv^2 given by classical mechanics is "
        "suitable for objects and processes in common human experience, "
        "but is not accurate for objects moving at speeds close to the "
        "speed of light, where relativistic effects become significant."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Kinetic energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Kinetic_energy",
    prerequisites=["multiplication", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="potential_energy",
    content=(
        "Near the surface of the Earth, where the acceleration due to "
        "gravity g can be considered constant (approximately 9.8 m/s^2), "
        "the gravitational potential energy of an object is given by "
        "U = mgh, where U is the potential energy of the object relative "
        "to its being on the Earth's surface, m is the mass of the "
        "object, g is the acceleration due to gravity, and h is the "
        "altitude (height above the reference point). The work done in "
        "lifting an object through a height h is equal to mgh. This "
        "formula is a simplification of the more general expression "
        "U = -GMm/r and is valid only near Earth's surface where "
        "gravity can be treated as uniform."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Gravitational energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Gravitational_energy",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="principle",
    name="conservation_energy",
    content=(
        "The law of conservation of energy states that the total energy "
        "of an isolated system remains constant; it is said to be "
        "conserved over time. Energy can neither be created nor "
        "destroyed; rather, it can only be transformed or transferred "
        "from one form to another. The principle of conservation of "
        "mechanical energy states that if an isolated system is subject "
        "only to conservative forces, then the mechanical energy is "
        "constant. That is, the sum of kinetic and potential energies "
        "remains constant: KE_1 + PE_1 = KE_2 + PE_2. In all real "
        "systems, however, nonconservative forces such as friction will "
        "be present, but if they are of negligible magnitude, the "
        "mechanical energy changes little and its conservation is a "
        "useful approximation."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Conservation of energy', Wikipedia, "
        "The Free Encyclopedia; see also 'Mechanical energy'."
    ),
    source_url="https://en.wikipedia.org/wiki/Conservation_of_energy",
    prerequisites=["kinetic_energy", "potential_energy"],
))

register_atom(Atom(
    atom_type="principle",
    name="conservation_momentum",
    content=(
        "In a closed system (one that does not exchange any matter with "
        "its surroundings and is not acted on by external forces) the "
        "total momentum remains constant. This fact, known as the law "
        "of conservation of momentum, is implied by Newton's laws of "
        "motion. Momentum is a conserved quantity in any inertial "
        "reference frame: if a closed system is not affected by "
        "external forces, its total linear momentum does not change. "
        "For two interacting bodies, m_1 v_1 + m_2 v_2 = m_1 v_1' + "
        "m_2 v_2', where primed quantities denote values after the "
        "interaction. Conservation of momentum is a consequence of "
        "the homogeneity of space (translational symmetry) via "
        "Noether's theorem."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Momentum', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Momentum",
    prerequisites=["multiplication", "system_equations"],
))

register_atom(Atom(
    atom_type="formula",
    name="ohms_law",
    content=(
        "Ohm's law states that the current through a conductor between "
        "two points is directly proportional to the voltage across the "
        "two points, and inversely proportional to the resistance "
        "between them: V = IR, where V is the voltage measured across "
        "the conductor in volts, I is the current through the conductor "
        "in amperes, and R is the resistance of the conductor in ohms. "
        "More specifically, Ohm's law states that the R in this "
        "relation is constant, independent of the current. Materials "
        "or circuit components that obey Ohm's law are called ohmic "
        "materials. The SI unit of resistance is the ohm, equal to one "
        "volt per ampere."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Ohm's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Ohm%27s_law",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="ideal_gas",
    content=(
        "The ideal gas law, also called the general gas equation, is "
        "the equation of state of a hypothetical ideal gas. It is a "
        "good approximation of the behaviour of many gases under many "
        "conditions. The law is expressed as PV = nRT, where P is the "
        "absolute pressure of the gas, V is the volume of the gas, n "
        "is the amount of substance of gas (in moles), R is the ideal "
        "gas constant equal to 8.314 J/(mol*K), and T is the absolute "
        "temperature of the gas in kelvins. The ideal gas law is a "
        "combination of the empirical Boyle's law, Charles's law, "
        "Avogadro's law, and Gay-Lussac's law."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Ideal gas law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Ideal_gas_law",
    prerequisites=["multiplication", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="pendulum_period",
    content=(
        "For small-angle oscillations (where sin(theta) is approximated "
        "by theta), a simple pendulum oscillates with a period "
        "T = 2*pi*sqrt(L/g), where T is the period of oscillation, L "
        "is the length of the pendulum (measured from the pivot to the "
        "centre of mass of the bob), and g is the local acceleration "
        "due to gravity. The equation of motion for the simple pendulum "
        "is d^2(theta)/dt^2 + (g/L)*sin(theta) = 0. In the "
        "small-angle approximation sin(theta) ~ theta, this reduces to "
        "simple harmonic motion. This formula underestimates the true "
        "period for any finite amplitude, but the error is negligible "
        "for small angles (less than about 15 degrees)."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Pendulum (mechanics)', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Pendulum_(mechanics)",
    prerequisites=["division", "multiplication"],
))

# ---------------------------------------------------------------------------
# Physics -- waves (tier 4)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="wave_equation",
    content=(
        "The frequency f of a sinusoidal wave is equal to the phase "
        "velocity v of the wave divided by the wavelength lambda of "
        "the wave: f = v / lambda, or equivalently v = f * lambda. "
        "Here v is the phase velocity (in metres per second), f is "
        "the frequency (in hertz), and lambda is the wavelength (in "
        "metres). Waves with higher frequencies have shorter "
        "wavelengths, and waves with lower frequencies have longer "
        "wavelengths, for a given wave speed. When waves travel from "
        "one medium to another, their frequency remains the same but "
        "their wavelength and speed may change."
    ),
    tier=4,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Wavelength', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Wavelength",
    prerequisites=["multiplication", "division"],
))

# ---------------------------------------------------------------------------
# Physics -- circuits (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="principle",
    name="kirchhoff",
    content=(
        "Kirchhoff's circuit laws are two equalities that deal with "
        "the current and potential difference (voltage) in the lumped "
        "element model of electrical circuits. They were first "
        "described in 1845 by German physicist Gustav Kirchhoff. "
        "Kirchhoff's current law (junction rule): the algebraic sum "
        "of currents in a network of conductors meeting at a point "
        "(node) is zero; equivalently, the sum of currents flowing "
        "into a node equals the sum flowing out. Kirchhoff's voltage "
        "law (loop rule): the directed sum of the potential differences "
        "(voltages) around any closed loop is zero. Both laws are "
        "valid for DC circuits and for AC circuits at frequencies "
        "where the wavelengths of electromagnetic radiation are very "
        "large compared to the circuit dimensions."
    ),
    tier=5,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Kirchhoff's circuit laws', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws",
    prerequisites=["system_equations", "ohms_law"],
))

# ---------------------------------------------------------------------------
# Physics -- gravity (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="gravitational_force",
    content=(
        "Newton's law of universal gravitation states that every "
        "particle attracts every other particle in the universe with a "
        "force that is proportional to the product of their masses and "
        "inversely proportional to the square of the distance between "
        "their centres: F = G*M*m / r^2, where F is the gravitational "
        "force acting between two objects, M and m are the masses of "
        "the objects, r is the distance between the centres of their "
        "masses, and G is the gravitational constant, approximately "
        "6.674 * 10^(-11) m^3 kg^(-1) s^(-2). The force acts along "
        "the line joining the two objects. This law was first stated "
        "by Isaac Newton and published in the Principia in 1687."
    ),
    tier=5,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Newton's law of universal "
        "gravitation', Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/"
        "Newton%27s_law_of_universal_gravitation"
    ),
    prerequisites=["multiplication", "exponentiation", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="escape_velocity",
    content=(
        "In celestial mechanics, escape velocity or escape speed is "
        "the minimum speed needed for an object to escape from contact "
        "with or orbit of a primary body, assuming no other forces act "
        "on the object (no aerodynamic drag, no propulsion). The "
        "escape velocity from the surface of a rotating body depends "
        "on direction. For a spherically symmetric, non-rotating body "
        "of mass M and radius r, the escape velocity at distance r "
        "from the centre is v_e = sqrt(2GM/r), where G is the "
        "gravitational constant. This is derived by equating kinetic "
        "energy to gravitational potential energy: (1/2)mv^2 = GMm/r, "
        "yielding v = sqrt(2GM/r). For Earth's surface, this gives "
        "approximately 11.2 km/s."
    ),
    tier=5,
    domain="physics",
    source=(
        "Wikipedia contributors, 'Escape velocity', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Escape_velocity",
    prerequisites=["gravitational_force"],
))

# ---------------------------------------------------------------------------
# Astrophysics (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="redshift",
    content=(
        "In physics, a redshift is an increase in the wavelength, and "
        "corresponding decrease in the frequency and photon energy, of "
        "electromagnetic radiation. The value of a redshift is often "
        "denoted by the letter z, defined as the fractional change in "
        "wavelength: z = (lambda_obs - lambda_emit) / lambda_emit, "
        "where lambda_obs is the observed wavelength and lambda_emit "
        "is the wavelength at the source at the time of emission. "
        "Equivalently, 1 + z = lambda_obs / lambda_emit. The "
        "corresponding frequency relation is z = (f_emit - f_obs) / "
        "f_obs. A positive z indicates a redshift (recession), while "
        "a negative z indicates a blueshift (approach). In cosmology, "
        "cosmological redshift is attributed to the expansion of "
        "space itself."
    ),
    tier=5,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Redshift', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Redshift",
    prerequisites=["subtraction", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="hubble_law",
    content=(
        "Hubble's law, also known as the Hubble-Lemaitre law, is the "
        "observation in physical cosmology that galaxies are moving "
        "away from Earth at speeds proportional to their distance. "
        "In its simplest form the law is expressed as v = H_0 * d, "
        "where v is the recessional velocity of the galaxy (typically "
        "in km/s), H_0 is Hubble's constant (the rate of expansion at "
        "the present time), and d is the proper distance to the galaxy "
        "(typically in megaparsecs, Mpc). The Hubble constant H_0 is "
        "most frequently quoted in (km/s)/Mpc, with current estimates "
        "near 70 (km/s)/Mpc. The law is a theoretical result derived "
        "from the Friedmann-Robertson-Walker metric. In 2018 the "
        "International Astronomical Union renamed the Hubble law as "
        "the Hubble-Lemaitre law in recognition of Georges Lemaitre's "
        "contribution."
    ),
    tier=5,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Hubble's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Hubble%27s_law",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="schwarzschild_radius",
    content=(
        "The Schwarzschild radius is a parameter in the Schwarzschild "
        "solution to Einstein's field equations that corresponds to "
        "the radius of the event horizon of a Schwarzschild (non-"
        "rotating, uncharged) black hole. The formula is r_s = 2GM / "
        "c^2, where r_s is the Schwarzschild radius, G is the "
        "gravitational constant, M is the mass of the object, and c "
        "is the speed of light in vacuum. The surface at the "
        "Schwarzschild radius demarcates the event horizon of the "
        "black hole: it represents the point past which light can no "
        "longer escape the gravitational field. The Schwarzschild "
        "radius of an object is proportional to its mass. Any amount "
        "of matter will become a black hole if compressed into a space "
        "that fits within its corresponding Schwarzschild radius."
    ),
    tier=6,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Schwarzschild radius', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Schwarzschild_radius",
    prerequisites=["gravitational_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="orbital_period",
    content=(
        "Kepler's third law of planetary motion states that the square "
        "of a planet's orbital period is proportional to the cube of "
        "the semi-major axis of its orbit. Using Newton's law of "
        "gravitation this is expressed as T^2 = (4*pi^2 / GM) * a^3, "
        "where T is the orbital period, a is the semi-major axis of "
        "the orbit, G is the gravitational constant, and M is the mass "
        "of the central body (assuming M >> m, the mass of the "
        "orbiting body). Equivalently, T = 2*pi * sqrt(a^3 / (GM)). "
        "For any two planets orbiting the same star, the ratio "
        "T_1^2 / T_2^2 = a_1^3 / a_2^3. Kepler originally stated "
        "this as an empirical law in 1619; Newton later proved it "
        "from his law of universal gravitation."
    ),
    tier=6,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Kepler's laws of planetary motion', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/"
        "Kepler%27s_laws_of_planetary_motion"
    ),
    prerequisites=["gravitational_force", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="stellar_luminosity",
    content=(
        "The Stefan-Boltzmann law applied to a star gives the total "
        "power (luminosity) radiated by the star as L = 4*pi*R^2 * "
        "sigma * T^4, where L is the luminosity in watts, R is the "
        "stellar radius in metres, T is the effective surface "
        "temperature in kelvins, and sigma is the Stefan-Boltzmann "
        "constant (approximately 5.670 * 10^(-8) W m^(-2) K^(-4)). "
        "The factor 4*pi*R^2 is the surface area of the star. "
        "Because luminosity depends on the fourth power of temperature, "
        "even small changes in stellar surface temperature result in "
        "dramatic changes in luminosity. If a star's surface "
        "temperature doubles, its luminosity increases by a factor "
        "of sixteen, assuming constant radius."
    ),
    tier=6,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Stefan-Boltzmann law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/"
        "Stefan%E2%80%93Boltzmann_law"
    ),
    prerequisites=["exponentiation", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="magnitude_distance",
    content=(
        "The distance modulus is a way of expressing distances that "
        "is often used in astronomy. It describes distances on a "
        "logarithmic scale based on the astronomical magnitude system. "
        "The distance modulus is defined as mu = m - M = 5*log10(d/10), "
        "where m is the apparent magnitude of the object as observed, "
        "M is the absolute magnitude (defined as the apparent magnitude "
        "of an object when seen at a distance of 10 parsecs), and d "
        "is the distance to the object in parsecs. Equivalently, "
        "mu = 5*log10(d) - 5. This definition is convenient because "
        "the observed brightness of a light source is related to its "
        "distance by the inverse square law and because brightnesses "
        "are expressed in magnitudes."
    ),
    tier=6,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Distance modulus', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Distance_modulus",
    prerequisites=["division", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="gravitational_lensing",
    content=(
        "In general relativity, light passing near a point mass M is "
        "deflected by an angle alpha = 4GM / (c^2 * b), where G is "
        "the gravitational constant, M is the mass of the deflecting "
        "body, c is the speed of light, and b is the impact parameter "
        "(the closest distance of approach of the light ray to the "
        "mass). The Einstein radius, a characteristic angular scale "
        "for gravitational lensing, is theta_E = sqrt((4GM / c^2) * "
        "(D_LS / (D_L * D_S))), where D_L is the angular diameter "
        "distance to the lens, D_S is the angular diameter distance "
        "to the source, and D_LS is the angular diameter distance "
        "between lens and source. The deflection formula is twice the "
        "Newtonian prediction and was confirmed during the 1919 solar "
        "eclipse, providing one of the first experimental tests of "
        "general relativity."
    ),
    tier=6,
    domain="astrophysics",
    source=(
        "Wikipedia contributors, 'Einstein radius', Wikipedia, "
        "The Free Encyclopedia; see also 'Gravitational lensing "
        "formalism'."
    ),
    source_url="https://en.wikipedia.org/wiki/Einstein_radius",
    prerequisites=["gravitational_force"],
))
