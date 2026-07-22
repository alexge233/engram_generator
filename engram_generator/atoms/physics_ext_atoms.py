"""Knowledge atoms for optics, fluid mechanics, and nuclear physics.

Registers formula and law atoms with Wikipedia sources and worked
examples for independent verification of generator outputs.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# Optics (tier 4-5)
# ===================================================================

register_atom(Atom(
    atom_type="law",
    name="snells_law",
    content=(
        "Snell's law describes the relationship between the angles of "
        "incidence and refraction when light passes between two media "
        "with different refractive indices: n1 * sin(theta1) = n2 * "
        "sin(theta2), where n1 and n2 are the refractive indices of "
        "the first and second medium, and theta1 and theta2 are the "
        "angles of incidence and refraction measured from the normal."
    ),
    example=(
        "Light passes from air (n1=1.0) to glass (n2=1.5) at "
        "theta1=30 deg: sin(theta2) = (1.0/1.5)*sin(30) = "
        "0.6667*0.5 = 0.3333, theta2 = arcsin(0.3333) = 19.47 deg"
    ),
    tier=4,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Snell's law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Snell%27s_law",
    prerequisites=["trigonometry"],
))

register_atom(Atom(
    atom_type="formula",
    name="thin_lens",
    content=(
        "The thin lens equation relates the focal length f of a thin "
        "lens to the object distance d_o and image distance d_i: "
        "1/f = 1/d_o + 1/d_i. A positive f indicates a converging "
        "lens, negative f a diverging lens. Object distance is "
        "positive when on the incoming side of the lens."
    ),
    example=(
        "Given f=10 cm, d_o=30 cm: 1/d_i = 1/10 - 1/30 = "
        "3/30 - 1/30 = 2/30, d_i = 15 cm"
    ),
    tier=4,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Thin lens', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Thin_lens",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="magnification",
    content=(
        "The lateral (transverse) magnification of an optical system "
        "is the ratio of the image height h_i to the object height "
        "h_o: M = h_i/h_o = -d_i/d_o, where d_i is the image "
        "distance and d_o is the object distance. A negative "
        "magnification indicates an inverted image."
    ),
    example=(
        "Given d_o=20 cm, d_i=40 cm: M = -40/20 = -2 "
        "(image is inverted and twice the size)"
    ),
    tier=4,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Magnification', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Magnification",
    prerequisites=["division", "thin_lens"],
))

register_atom(Atom(
    atom_type="formula",
    name="double_slit",
    content=(
        "Young's double-slit experiment demonstrates the wave nature "
        "of light. Constructive interference (bright fringes) occurs "
        "when d*sin(theta) = m*lambda, where d is the slit separation, "
        "theta is the angle from the central axis, m is the order "
        "(integer), and lambda is the wavelength. The fringe spacing "
        "on a screen at distance L is y = m*lambda*L/d."
    ),
    example=(
        "Given d=0.1 mm, lambda=500 nm, L=1 m, m=1: "
        "y = 1*500e-9*1/0.1e-3 = 5e-3 m = 5 mm"
    ),
    tier=5,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Double-slit experiment', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Double-slit_experiment",
    prerequisites=["trigonometry", "snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="brewster_angle",
    content=(
        "Brewster's angle (polarisation angle) is the angle of "
        "incidence at which reflected light is completely polarised. "
        "It satisfies tan(theta_B) = n2/n1, where n1 and n2 are the "
        "refractive indices of the two media. At this angle, the "
        "reflected and refracted rays are perpendicular."
    ),
    example=(
        "Light hitting glass (n2=1.5) from air (n1=1.0): "
        "theta_B = arctan(1.5/1.0) = arctan(1.5) = 56.31 deg"
    ),
    tier=5,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Brewster's angle', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Brewster%27s_angle",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="diffraction_grating",
    content=(
        "A diffraction grating produces maxima when "
        "d*sin(theta) = m*lambda, where d is the grating spacing "
        "(1/N for N lines per unit length), theta is the diffraction "
        "angle, m is the diffraction order, and lambda is the "
        "wavelength. The resolving power is R = m*N where N is the "
        "total number of slits illuminated."
    ),
    example=(
        "Grating with 500 lines/mm, lambda=600 nm, m=1: "
        "d=1/500000 m=2e-6 m, sin(theta)=600e-9/2e-6=0.3, "
        "theta=arcsin(0.3)=17.46 deg"
    ),
    tier=5,
    domain="optics",
    source=(
        "Wikipedia contributors, 'Diffraction grating', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Diffraction_grating",
    prerequisites=["double_slit"],
))


# ===================================================================
# Fluid Mechanics (tier 4-5)
# ===================================================================

register_atom(Atom(
    atom_type="principle",
    name="bernoulli",
    content=(
        "Bernoulli's principle states that for an inviscid, "
        "incompressible fluid in steady flow, the total mechanical "
        "energy along a streamline is constant: "
        "P + (1/2)*rho*v^2 + rho*g*h = constant, where P is the "
        "static pressure, rho is the fluid density, v is the flow "
        "velocity, g is gravitational acceleration, and h is the "
        "elevation above a reference point."
    ),
    example=(
        "Water (rho=1000) flows at v1=2 m/s, P1=200000 Pa at "
        "h1=0. At h2=5 m with v2=4 m/s: P2 = P1 + 0.5*1000*(4-16) "
        "+ 1000*9.8*(0-5) = 200000 - 6000 - 49000 = 145000 Pa"
    ),
    tier=4,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Bernoulli's principle', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Bernoulli%27s_principle",
    prerequisites=["kinetic_energy", "potential_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="reynolds_number",
    content=(
        "The Reynolds number is a dimensionless quantity that predicts "
        "flow patterns: Re = rho*v*L/mu = v*L/nu, where rho is the "
        "fluid density, v is the flow velocity, L is a characteristic "
        "length, mu is the dynamic viscosity, and nu is the kinematic "
        "viscosity. Re < 2300 indicates laminar flow, Re > 4000 "
        "indicates turbulent flow."
    ),
    example=(
        "Water (rho=1000, mu=1e-3) in a pipe (D=0.05 m) at v=0.5 m/s: "
        "Re = 1000*0.5*0.05/1e-3 = 25000 (turbulent)"
    ),
    tier=4,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Reynolds number', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Reynolds_number",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="continuity_equation",
    content=(
        "The continuity equation for incompressible flow states that "
        "the product of cross-sectional area and flow velocity is "
        "constant along a streamline: A1*v1 = A2*v2, where A is the "
        "cross-sectional area and v is the flow velocity. This "
        "expresses conservation of mass for incompressible fluids."
    ),
    example=(
        "Pipe narrows from A1=0.01 m^2 to A2=0.005 m^2, v1=2 m/s: "
        "v2 = A1*v1/A2 = 0.01*2/0.005 = 4 m/s"
    ),
    tier=4,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Continuity equation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Continuity_equation",
    prerequisites=["multiplication", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="drag_force",
    content=(
        "The drag force on an object moving through a fluid is given by "
        "F_d = (1/2)*C_d*rho*A*v^2, where C_d is the drag coefficient "
        "(dimensionless), rho is the fluid density, A is the reference "
        "area (typically frontal area), and v is the velocity relative "
        "to the fluid."
    ),
    example=(
        "Sphere (C_d=0.47, A=0.01 m^2) in air (rho=1.225) at v=10 m/s: "
        "F_d = 0.5*0.47*1.225*0.01*100 = 0.288 N"
    ),
    tier=5,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Drag (physics)', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Drag_(physics)",
    prerequisites=["kinetic_energy"],
))

register_atom(Atom(
    atom_type="principle",
    name="buoyancy",
    content=(
        "Archimedes' principle states that the upward buoyant force "
        "exerted on a body immersed in a fluid equals the weight of "
        "the fluid displaced: F_b = rho_f * V_disp * g, where rho_f "
        "is the fluid density, V_disp is the volume of displaced "
        "fluid, and g is gravitational acceleration. An object floats "
        "when F_b >= its weight."
    ),
    example=(
        "Object of volume 0.002 m^3 in water (rho=1000): "
        "F_b = 1000*0.002*9.8 = 19.6 N"
    ),
    tier=4,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Buoyancy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Buoyancy",
    prerequisites=["gravitational_force"],
))

register_atom(Atom(
    atom_type="law",
    name="viscous_flow",
    content=(
        "The Hagen-Poiseuille equation describes laminar flow of a "
        "viscous fluid through a long cylindrical pipe: "
        "Q = (pi*r^4*dP)/(8*mu*L), where Q is the volumetric flow "
        "rate, r is the pipe radius, dP is the pressure difference, "
        "mu is the dynamic viscosity, and L is the pipe length. "
        "Flow rate scales with the fourth power of the radius."
    ),
    example=(
        "Pipe r=0.01 m, L=1 m, dP=1000 Pa, mu=1e-3: "
        "Q = pi*(0.01)^4*1000/(8*1e-3*1) = pi*1e-8*1000/8e-3 "
        "= pi*1e-5/8e-3 = 3.927e-3 m^3/s"
    ),
    tier=5,
    domain="fluid_mechanics",
    source=(
        "Wikipedia contributors, 'Hagen-Poiseuille equation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Hagen%E2%80%93Poiseuille_equation",
    prerequisites=["reynolds_number", "continuity_equation"],
))


# ===================================================================
# Nuclear Physics (tier 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="mass_defect",
    content=(
        "The mass defect of a nucleus is the difference between the "
        "sum of the masses of its constituent protons and neutrons "
        "and the actual nuclear mass: dm = Z*m_p + N*m_n - M_nucleus, "
        "where Z is the atomic number, N is the neutron number, m_p "
        "is the proton mass (1.00728 u), m_n is the neutron mass "
        "(1.00866 u), and M_nucleus is the measured nuclear mass."
    ),
    example=(
        "Helium-4 (Z=2, N=2, M=4.00260 u): "
        "dm = 2*1.00728 + 2*1.00866 - 4.00260 = "
        "4.03188 - 4.00260 = 0.02928 u"
    ),
    tier=5,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Nuclear binding energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Nuclear_binding_energy",
    prerequisites=["multiplication", "subtraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="binding_energy_per_nucleon",
    content=(
        "The binding energy per nucleon is the total nuclear binding "
        "energy divided by the mass number A = Z + N: "
        "BE/A = (dm * 931.5 MeV/u) / A, where dm is the mass defect "
        "in atomic mass units. This quantity peaks near iron-56 "
        "(~8.8 MeV/nucleon), explaining why fusion of light nuclei "
        "and fission of heavy nuclei both release energy."
    ),
    example=(
        "Helium-4 (A=4, dm=0.02928 u): "
        "BE = 0.02928*931.5 = 27.28 MeV, "
        "BE/A = 27.28/4 = 6.82 MeV/nucleon"
    ),
    tier=5,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Nuclear binding energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Nuclear_binding_energy",
    prerequisites=["mass_defect"],
))

register_atom(Atom(
    atom_type="law",
    name="radioactive_decay",
    content=(
        "Radioactive decay follows an exponential law: "
        "N(t) = N_0 * exp(-lambda*t), where N_0 is the initial number "
        "of atoms, lambda is the decay constant, and t is time. "
        "The activity (decays per second) is A = lambda*N. "
        "The decay constant is related to the half-life by "
        "lambda = ln(2)/t_half."
    ),
    example=(
        "N_0=1000 atoms, t_half=5 days, t=10 days: "
        "lambda=ln(2)/5=0.1386/day, "
        "N(10)=1000*exp(-0.1386*10)=1000*exp(-1.386)=1000*0.25=250"
    ),
    tier=5,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Radioactive decay', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Radioactive_decay",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="half_life",
    content=(
        "The half-life is the time required for exactly half of the "
        "atoms in a radioactive sample to decay: "
        "t_half = ln(2)/lambda, where lambda is the decay constant. "
        "After n half-lives, the fraction remaining is (1/2)^n. "
        "Half-lives range from fractions of a second (polonium-214) "
        "to billions of years (uranium-238)."
    ),
    example=(
        "Given lambda=0.0866/year: "
        "t_half = ln(2)/0.0866 = 0.6931/0.0866 = 8.0 years. "
        "After 3 half-lives (24 years): fraction = (1/2)^3 = 0.125"
    ),
    tier=5,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Half-life', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Half-life",
    prerequisites=["radioactive_decay"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="decay_chain",
    content=(
        "A radioactive decay chain (or series) is a sequence of "
        "radioactive decays where each nuclide transforms into another "
        "through alpha, beta, or gamma decay until a stable nuclide "
        "is reached. In alpha decay, Z decreases by 2 and A by 4. "
        "In beta-minus decay, Z increases by 1 and A stays the same. "
        "The four natural decay chains end at lead-206, lead-207, "
        "lead-208, or bismuth-209."
    ),
    example=(
        "U-238 alpha decay: (Z=92,A=238) -> (Z=90,A=234) = Th-234. "
        "Th-234 beta decay: (Z=90,A=234) -> (Z=91,A=234) = Pa-234."
    ),
    tier=5,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Decay chain', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Decay_chain",
    prerequisites=["radioactive_decay"],
))

register_atom(Atom(
    atom_type="formula",
    name="nuclear_reaction",
    content=(
        "In a nuclear reaction, conservation laws must be satisfied: "
        "conservation of baryon number (total A), electric charge "
        "(total Z), lepton number, and energy-momentum. The Q-value "
        "is the net energy released: Q = (sum of reactant masses - "
        "sum of product masses) * c^2. Q > 0 is exothermic, Q < 0 "
        "is endothermic."
    ),
    example=(
        "D + T -> He-4 + n: Q = (2.01410 + 3.01605 - 4.00260 - "
        "1.00866)*931.5 = 0.01889*931.5 = 17.59 MeV (exothermic)"
    ),
    tier=6,
    domain="nuclear_physics",
    source=(
        "Wikipedia contributors, 'Nuclear reaction', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Nuclear_reaction",
    prerequisites=["mass_defect", "binding_energy_per_nucleon"],
))
