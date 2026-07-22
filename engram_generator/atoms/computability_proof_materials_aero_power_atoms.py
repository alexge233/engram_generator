"""Knowledge atoms for computability, proof theory, materials science,
aerospace engineering, and power systems.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Computability (tier 6-7) ──────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="godel_number",
    content=(
        "A Goedel numbering is a function that assigns a unique natural "
        "number to each symbol, formula, and proof in a formal language. "
        "Using prime factorisation, any sequence of symbols (s1, s2, ..., sn) "
        "is encoded as 2^s1 * 3^s2 * 5^s3 * ... * p_n^sn, where p_n is the "
        "n-th prime. This allows metamathematical reasoning about formal "
        "systems within arithmetic itself."
    ),
    example=(
        "Encode sequence (1, 3, 2): "
        "G = 2^1 * 3^3 * 5^2 = 2 * 27 * 25 = 1350"
    ),
    tier=6,
    domain="computability",
    source="Wikipedia contributors, 'Goedel numbering', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/G%C3%B6del_numbering",
    prerequisites=["prime_factorisation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="halting_problem",
    content=(
        "The halting problem asks whether a given program halts on a given "
        "input. Alan Turing proved in 1936 that no general algorithm can "
        "solve the halting problem for all program-input pairs. The proof "
        "uses diagonalisation: assume a decider H exists, construct a "
        "program D that calls H on itself and does the opposite, leading "
        "to contradiction."
    ),
    example=(
        "Program P: while x > 0: x = x - 1. Input x=5: halts after 5 steps. "
        "Program Q: while True: pass. Input any: never halts. "
        "No single algorithm can decide both cases for all programs."
    ),
    tier=7,
    domain="computability",
    source="Wikipedia contributors, 'Halting problem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Halting_problem",
    prerequisites=["godel_number"],
))

register_atom(Atom(
    atom_type="definition",
    name="reduction_computability",
    content=(
        "A many-one reduction from problem A to problem B is a computable "
        "function f such that x in A iff f(x) in B. If A reduces to B "
        "(A <=m B) and B is decidable, then A is decidable. Equivalently, "
        "if A is undecidable and A <=m B, then B is undecidable. "
        "Reductions are the primary tool for proving undecidability."
    ),
    example=(
        "Reduce HALTING to EMPTY_TM: given (M, w), construct M' that "
        "on input x, simulates M on w, then accepts. "
        "L(M') = Sigma* if M halts on w, empty otherwise. "
        "HALTING <=m complement(EMPTY_TM)."
    ),
    tier=7,
    domain="computability",
    source="Wikipedia contributors, 'Many-one reduction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Many-one_reduction",
    prerequisites=["halting_problem"],
))

register_atom(Atom(
    atom_type="theorem",
    name="rice_theorem",
    content=(
        "Rice's theorem states that for any non-trivial property of the "
        "partial functions computed by Turing machines, no general "
        "effective method can decide whether an arbitrary Turing machine "
        "computes a function with that property. A property is non-trivial "
        "if it is satisfied by some but not all partial computable functions."
    ),
    example=(
        "Property: 'the TM accepts at least one string'. This is non-trivial "
        "(some TMs do, some don't). By Rice's theorem, no algorithm can "
        "decide this for all TMs."
    ),
    tier=7,
    domain="computability",
    source="Wikipedia contributors, 'Rice\\'s theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Rice%27s_theorem",
    prerequisites=["halting_problem"],
))

register_atom(Atom(
    atom_type="definition",
    name="recursive_enumerable",
    content=(
        "A set S is recursively enumerable (r.e.) if there exists a Turing "
        "machine that halts and accepts for every input in S, but may loop "
        "forever on inputs not in S. Equivalently, S is r.e. iff S is the "
        "domain of some partial computable function, or S is empty or the "
        "range of some total computable function."
    ),
    example=(
        "The set of provable theorems in PA is r.e.: enumerate all proofs, "
        "output the theorem of each valid proof. Given a formula, we can "
        "confirm it's provable (by finding a proof) but may never confirm "
        "it's unprovable."
    ),
    tier=7,
    domain="computability",
    source="Wikipedia contributors, 'Recursively enumerable set', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Recursively_enumerable_set",
    prerequisites=["halting_problem"],
))

register_atom(Atom(
    atom_type="definition",
    name="kolmogorov_complexity",
    content=(
        "The Kolmogorov complexity K(x) of a string x is the length of "
        "the shortest program (in a fixed universal language) that outputs "
        "x. K(x) is uncomputable in general. A string is random if "
        "K(x) >= |x|, i.e. it cannot be compressed. The invariance theorem "
        "states that K differs by at most a constant across universal languages."
    ),
    example=(
        "String '0000000000' (10 zeros): K <= |'print 0*10'| ~ 12 bits. "
        "String '7391048265' (random): K ~ 10*log2(10) ~ 33 bits. "
        "The patterned string has much lower complexity."
    ),
    tier=7,
    domain="computability",
    source="Wikipedia contributors, 'Kolmogorov complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Kolmogorov_complexity",
    prerequisites=["halting_problem"],
))

# ── Proof Theory (tier 6-8) ──────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="resolution_refutation",
    content=(
        "Resolution is a rule of inference for propositional and first-order "
        "logic. To prove a formula F, negate F, convert to CNF, and "
        "repeatedly apply the resolution rule: from clauses (A v C) and "
        "(not-A v D), derive (C v D). If the empty clause is derived, "
        "F is valid (proof by refutation)."
    ),
    example=(
        "Prove p -> (q -> p). Negate: p AND q AND NOT p. "
        "Clauses: {p}, {q}, {NOT p}. Resolve {p} with {NOT p}: empty clause. "
        "Contradiction found, original formula is valid."
    ),
    tier=6,
    domain="proof_theory",
    source="Wikipedia contributors, 'Resolution (logic)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Resolution_(logic)",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="horn_clause",
    content=(
        "A Horn clause is a disjunction of literals with at most one "
        "positive literal. Forms: definite clause (exactly one positive: "
        "A <- B1, B2, ...), goal clause (no positive: <- B1, B2, ...), "
        "and fact (positive literal only: A <-). Horn clauses are the "
        "foundation of logic programming (Prolog) and can be decided "
        "in linear time."
    ),
    example=(
        "Definite clause: grandparent(X,Z) :- parent(X,Y), parent(Y,Z). "
        "Fact: parent(alice, bob). "
        "Goal: ?- grandparent(alice, charlie). "
        "Resolution finds: parent(alice,bob), parent(bob,charlie) -> yes."
    ),
    tier=6,
    domain="proof_theory",
    source="Wikipedia contributors, 'Horn clause', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Horn_clause",
    prerequisites=["resolution_refutation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="natural_deduction",
    content=(
        "Natural deduction is a proof system where logical reasoning is "
        "expressed through introduction and elimination rules for each "
        "connective. AND-introduction: from A and B, derive A ^ B. "
        "Implication-introduction: assume A, derive B, conclude A -> B "
        "(discharging the assumption). Proofs form tree structures."
    ),
    example=(
        "Prove A -> (B -> (A ^ B)). "
        "1. Assume A. "
        "2. Assume B. "
        "3. A ^ B (AND-intro from 1, 2). "
        "4. B -> (A ^ B) (->-intro, discharge 2). "
        "5. A -> (B -> (A ^ B)) (->-intro, discharge 1)."
    ),
    tier=7,
    domain="proof_theory",
    source="Wikipedia contributors, 'Natural deduction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Natural_deduction",
    prerequisites=["resolution_refutation"],
))

register_atom(Atom(
    atom_type="definition",
    name="modal_logic",
    content=(
        "Modal logic extends propositional logic with operators for "
        "necessity (box, necessarily true in all accessible worlds) and "
        "possibility (diamond, true in at least one accessible world). "
        "Kripke semantics evaluates formulas over frames (W, R) where W "
        "is a set of worlds and R is an accessibility relation. "
        "Common systems: K (minimal), T (reflexive), S4 (transitive), "
        "S5 (equivalence relation)."
    ),
    example=(
        "Frame: worlds {w1, w2}, R = {(w1,w2), (w2,w1), (w1,w1), (w2,w2)}. "
        "V(p) = {w1}. "
        "diamond-p at w2: exists w' with w2Rw' and p in w'. "
        "w2Rw1 and p in w1, so diamond-p is true at w2."
    ),
    tier=7,
    domain="proof_theory",
    source="Wikipedia contributors, 'Modal logic', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Modal_logic",
    prerequisites=["natural_deduction"],
))

register_atom(Atom(
    atom_type="definition",
    name="intuitionistic_logic",
    content=(
        "Intuitionistic logic rejects the law of excluded middle "
        "(A v NOT A) and double negation elimination (NOT NOT A -> A). "
        "A proposition is true only if there is a constructive proof. "
        "The BHK interpretation: a proof of A v B is a proof of A or "
        "a proof of B; a proof of A -> B is a function transforming "
        "proofs of A into proofs of B."
    ),
    example=(
        "Classical: 'there exists an irrational a such that a^sqrt(2) is rational' "
        "(proved by cases without constructing a). "
        "Intuitionistic: must exhibit the actual value of a. "
        "The Gelfond-Schneider theorem gives a = sqrt(2)^sqrt(2)."
    ),
    tier=7,
    domain="proof_theory",
    source="Wikipedia contributors, 'Intuitionistic logic', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Intuitionistic_logic",
    prerequisites=["natural_deduction"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sequent_calculus",
    content=(
        "The sequent calculus (Gentzen's LK/LJ) represents proofs as "
        "trees of sequents Gamma |- Delta, where Gamma is a multiset of "
        "assumptions and Delta of conclusions. Rules include structural "
        "rules (weakening, contraction, exchange) and logical rules "
        "(left/right introduction for each connective). Cut elimination "
        "shows every proof can be made cut-free."
    ),
    example=(
        "Prove A, A->B |- B. "
        "1. A |- A (axiom). "
        "2. B |- B (axiom). "
        "3. A, A->B |- B (->-left on 1, 2)."
    ),
    tier=8,
    domain="proof_theory",
    source="Wikipedia contributors, 'Sequent calculus', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Sequent_calculus",
    prerequisites=["natural_deduction"],
))

# ── Materials Science (tier 4-5) ─────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="stress_strain",
    content=(
        "Engineering stress sigma = F/A0 where F is the applied force "
        "and A0 is the original cross-sectional area. Engineering strain "
        "epsilon = (L - L0)/L0 = delta_L/L0. The stress-strain curve "
        "characterises material behaviour: elastic region (linear, "
        "reversible), yield point, plastic deformation, and fracture."
    ),
    example=(
        "Given F=50kN, A0=100mm^2=1e-4 m^2: "
        "sigma = 50000/1e-4 = 500 MPa. "
        "Given L0=200mm, L=201mm: epsilon = 1/200 = 0.005 (0.5%)."
    ),
    tier=4,
    domain="materials_science",
    source="Wikipedia contributors, 'Stress-strain curve', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Stress%E2%80%93strain_curve",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="youngs_modulus",
    content=(
        "Young's modulus E (elastic modulus) is the ratio of stress to "
        "strain in the linear elastic region: E = sigma/epsilon. "
        "Units: Pa (N/m^2). Typical values: steel ~200 GPa, aluminium "
        "~70 GPa, rubber ~0.01 GPa. Higher E means stiffer material."
    ),
    example=(
        "Given sigma=500 MPa, epsilon=0.0025: "
        "E = 500e6/0.0025 = 200e9 Pa = 200 GPa (steel)."
    ),
    tier=4,
    domain="materials_science",
    source="Wikipedia contributors, 'Young\\'s modulus', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Young%27s_modulus",
    prerequisites=["stress_strain"],
))

register_atom(Atom(
    atom_type="formula",
    name="thermal_expansion",
    content=(
        "Linear thermal expansion: delta_L = alpha * L0 * delta_T, "
        "where alpha is the coefficient of linear thermal expansion "
        "(1/K), L0 is original length, and delta_T is temperature change. "
        "Volumetric expansion: delta_V = beta * V0 * delta_T where "
        "beta ~ 3*alpha for isotropic materials."
    ),
    example=(
        "Steel bar L0=2m, alpha=12e-6/K, delta_T=50K: "
        "delta_L = 12e-6 * 2 * 50 = 1.2e-3 m = 1.2 mm."
    ),
    tier=4,
    domain="materials_science",
    source="Wikipedia contributors, 'Thermal expansion', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Thermal_expansion",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="definition",
    name="crystal_structure",
    content=(
        "A crystal structure is a periodic arrangement of atoms in 3D "
        "space, described by a lattice and a basis. The 14 Bravais lattices "
        "fall into 7 crystal systems: cubic, tetragonal, orthorhombic, "
        "hexagonal, trigonal, monoclinic, triclinic. Common structures: "
        "FCC (4 atoms/cell), BCC (2 atoms/cell), HCP (6 atoms/cell)."
    ),
    example=(
        "FCC unit cell: atoms at corners (8 * 1/8 = 1) plus face centres "
        "(6 * 1/2 = 3). Total = 4 atoms per unit cell. "
        "Packing fraction = (4 * 4/3 * pi * r^3) / a^3 = pi/(3*sqrt(2)) = 0.7405."
    ),
    tier=5,
    domain="materials_science",
    source="Wikipedia contributors, 'Crystal structure', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Crystal_structure",
    prerequisites=["geometry"],
))

register_atom(Atom(
    atom_type="formula",
    name="diffusion_fick",
    content=(
        "Fick's first law: J = -D * dC/dx, where J is the diffusion flux "
        "(mol/m^2/s), D is the diffusion coefficient (m^2/s), and dC/dx "
        "is the concentration gradient. Fick's second law: dC/dt = D * "
        "d^2C/dx^2 describes how concentration changes with time."
    ),
    example=(
        "Given D=1e-10 m^2/s, dC/dx = (0.5-0.1)/(0.001) = 400 mol/m^4: "
        "J = -1e-10 * 400 = -4e-8 mol/m^2/s (negative = down gradient)."
    ),
    tier=5,
    domain="materials_science",
    source="Wikipedia contributors, 'Fick\\'s laws of diffusion', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fick%27s_laws_of_diffusion",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="definition",
    name="phase_diagram",
    content=(
        "A phase diagram maps the thermodynamic conditions (T, P, or "
        "composition) under which distinct phases exist at equilibrium. "
        "The Gibbs phase rule F = C - P + 2 gives the degrees of freedom, "
        "where C is the number of components and P is the number of phases. "
        "Key features: eutectic point, solidus, liquidus, phase boundaries."
    ),
    example=(
        "Binary eutectic (Pb-Sn): C=2, at eutectic point P=3 (liquid + "
        "alpha + beta), F = 2 - 3 + 2 = 1 (but at fixed pressure F = 0, "
        "invariant point). Eutectic at 183 deg C, 61.9% Sn."
    ),
    tier=5,
    domain="materials_science",
    source="Wikipedia contributors, 'Phase diagram', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Phase_diagram",
    prerequisites=["thermal_expansion"],
))

# ── Aerospace (tier 5-6) ─────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="thrust_equation",
    content=(
        "Rocket thrust: F = m_dot * v_e + (p_e - p_0) * A_e, "
        "where m_dot is the mass flow rate, v_e is the exhaust velocity, "
        "p_e is the exit pressure, p_0 is the ambient pressure, and A_e "
        "is the nozzle exit area. In vacuum (p_0=0), this simplifies to "
        "F = m_dot * v_e + p_e * A_e."
    ),
    example=(
        "Given m_dot=100 kg/s, v_e=3000 m/s, matched nozzle (p_e=p_0): "
        "F = 100 * 3000 = 300,000 N = 300 kN."
    ),
    tier=5,
    domain="aerospace",
    source="Wikipedia contributors, 'Rocket engine', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Rocket_engine",
    prerequisites=["momentum"],
))

register_atom(Atom(
    atom_type="formula",
    name="tsiolkovsky",
    content=(
        "The Tsiolkovsky rocket equation relates the change in velocity "
        "(delta-v) to the exhaust velocity and mass ratio: "
        "delta_v = v_e * ln(m_0/m_f), where m_0 is the initial total mass "
        "and m_f is the final mass (after propellant is expended). "
        "Also written as delta_v = I_sp * g_0 * ln(m_0/m_f)."
    ),
    example=(
        "Given v_e=3000 m/s, m_0=1000 kg, m_f=400 kg: "
        "delta_v = 3000 * ln(1000/400) = 3000 * 0.9163 = 2748.9 m/s."
    ),
    tier=5,
    domain="aerospace",
    source="Wikipedia contributors, 'Tsiolkovsky rocket equation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="orbital_velocity",
    content=(
        "The orbital velocity for a circular orbit is v = sqrt(G*M/r), "
        "where G is the gravitational constant, M is the central body mass, "
        "and r is the orbital radius. For Earth surface orbit: "
        "v ~ sqrt(3.986e14/6.371e6) ~ 7905 m/s."
    ),
    example=(
        "LEO at altitude 400 km: r = 6371 + 400 = 6771 km = 6.771e6 m. "
        "v = sqrt(3.986e14/6.771e6) = sqrt(5.887e7) = 7673 m/s."
    ),
    tier=5,
    domain="aerospace",
    source="Wikipedia contributors, 'Orbital speed', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Orbital_speed",
    prerequisites=["gravitational_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="hohmann_transfer",
    content=(
        "A Hohmann transfer orbit is an elliptical orbit used to transfer "
        "between two circular orbits using two engine burns. "
        "delta_v1 = sqrt(mu/r1) * (sqrt(2*r2/(r1+r2)) - 1), "
        "delta_v2 = sqrt(mu/r2) * (1 - sqrt(2*r1/(r1+r2))), "
        "where mu = G*M, r1 is inner orbit radius, r2 is outer."
    ),
    example=(
        "LEO (r1=6571km) to GEO (r2=42164km), mu=3.986e5 km^3/s^2: "
        "delta_v1 = sqrt(3.986e5/6571) * (sqrt(2*42164/48735) - 1) = "
        "7.79 * 0.3155 = 2.458 km/s."
    ),
    tier=6,
    domain="aerospace",
    source="Wikipedia contributors, 'Hohmann transfer orbit', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hohmann_transfer_orbit",
    prerequisites=["orbital_velocity"],
))

register_atom(Atom(
    atom_type="formula",
    name="drag_coefficient",
    content=(
        "The drag equation gives aerodynamic drag force: "
        "F_D = 0.5 * C_D * rho * A * v^2, "
        "where C_D is the drag coefficient (dimensionless), rho is air "
        "density, A is the reference area, and v is the velocity. "
        "Typical C_D: sphere ~0.47, streamlined body ~0.04, flat plate ~1.28."
    ),
    example=(
        "Sphere d=0.1m, v=30m/s, rho=1.225 kg/m^3, C_D=0.47: "
        "A = pi*(0.05)^2 = 7.854e-3 m^2. "
        "F_D = 0.5 * 0.47 * 1.225 * 7.854e-3 * 900 = 2.036 N."
    ),
    tier=5,
    domain="aerospace",
    source="Wikipedia contributors, 'Drag coefficient', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Drag_coefficient",
    prerequisites=["kinetic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="lift_equation",
    content=(
        "Aerodynamic lift: L = 0.5 * C_L * rho * A * v^2, "
        "where C_L is the lift coefficient, rho is air density, "
        "A is the wing planform area, and v is the airspeed. "
        "For level flight, L = W (weight). C_L depends on angle of "
        "attack and airfoil shape."
    ),
    example=(
        "Wing A=20m^2, v=70m/s, rho=1.225 kg/m^3, C_L=1.2: "
        "L = 0.5 * 1.2 * 1.225 * 20 * 4900 = 72,030 N = 72 kN."
    ),
    tier=5,
    domain="aerospace",
    source="Wikipedia contributors, 'Lift (force)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Lift_(force)",
    prerequisites=["kinetic_energy"],
))

# ── Power Systems (tier 4-6) ─────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="three_phase_power",
    content=(
        "Three-phase power: P = sqrt(3) * V_L * I_L * cos(phi), "
        "where V_L is the line-to-line voltage, I_L is the line current, "
        "and cos(phi) is the power factor. For balanced loads, "
        "P_total = 3 * V_ph * I_ph * cos(phi)."
    ),
    example=(
        "Given V_L=400V, I_L=10A, cos(phi)=0.85: "
        "P = sqrt(3) * 400 * 10 * 0.85 = 1.732 * 3400 = 5888.8 W = 5.89 kW."
    ),
    tier=5,
    domain="power_systems",
    source="Wikipedia contributors, 'Three-phase electric power', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Three-phase_electric_power",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="transformer_ratio",
    content=(
        "The ideal transformer equations: V1/V2 = N1/N2 = I2/I1, "
        "where V is voltage, N is number of turns, and I is current. "
        "A step-up transformer has N2 > N1 (higher voltage, lower current). "
        "Power is conserved: P1 = P2 (ideal)."
    ),
    example=(
        "Step-down transformer: N1=1000, N2=100, V1=240V. "
        "V2 = 240 * 100/1000 = 24V. "
        "If I2=5A, then I1 = 5 * 100/1000 = 0.5A. P = 120W both sides."
    ),
    tier=4,
    domain="power_systems",
    source="Wikipedia contributors, 'Transformer', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Transformer",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="power_factor_correction",
    content=(
        "Power factor PF = P/S = cos(phi), where P is real power (W), "
        "S is apparent power (VA). Reactive power Q = S*sin(phi). "
        "To correct PF from cos(phi1) to cos(phi2), the required "
        "capacitive reactive power is Q_c = P*(tan(phi1) - tan(phi2)). "
        "The capacitance needed: C = Q_c/(2*pi*f*V^2)."
    ),
    example=(
        "P=10kW, PF=0.7 lagging, target PF=0.95. "
        "phi1=acos(0.7)=45.57deg, phi2=acos(0.95)=18.19deg. "
        "Q_c = 10000*(tan(45.57)-tan(18.19)) = 10000*(1.020-0.329) = 6914 VAR."
    ),
    tier=6,
    domain="power_systems",
    source="Wikipedia contributors, 'Power factor', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Power_factor",
    prerequisites=["three_phase_power"],
))

register_atom(Atom(
    atom_type="formula",
    name="transmission_loss",
    content=(
        "Power loss in a transmission line: P_loss = I^2 * R, "
        "where I is the current and R is the line resistance. "
        "Since P = V * I, for a given power P, higher voltage means "
        "lower current and thus lower losses: P_loss = P^2 * R / V^2. "
        "This is why long-distance transmission uses high voltage."
    ),
    example=(
        "Transmit P=1MW over R=10 ohm line. "
        "At V=10kV: I=100A, P_loss = 100^2 * 10 = 100 kW (10% loss). "
        "At V=100kV: I=10A, P_loss = 10^2 * 10 = 1 kW (0.1% loss)."
    ),
    tier=4,
    domain="power_systems",
    source="Wikipedia contributors, 'Electric power transmission', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Electric_power_transmission",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="generator_frequency",
    content=(
        "The electrical frequency of an AC generator is f = (N * P) / 120, "
        "where N is the rotational speed in RPM and P is the number of "
        "magnetic poles. For 50 Hz at 2 poles: N = 3000 RPM. "
        "For 60 Hz at 4 poles: N = 1800 RPM."
    ),
    example=(
        "Generator with P=4 poles, N=1500 RPM: "
        "f = (1500 * 4) / 120 = 6000/120 = 50 Hz."
    ),
    tier=4,
    domain="power_systems",
    source="Wikipedia contributors, 'Electric generator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Electric_generator",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="load_flow",
    content=(
        "Load flow (power flow) analysis determines the steady-state "
        "voltages, currents, and power flows in an electrical network. "
        "The Newton-Raphson method iteratively solves P_i = sum_j "
        "|V_i||V_j||Y_ij|cos(theta_ij - delta_i + delta_j) and "
        "Q_i = -sum_j |V_i||V_j||Y_ij|sin(theta_ij - delta_i + delta_j) "
        "for unknown voltage magnitudes and angles."
    ),
    example=(
        "2-bus system: bus 1 (slack, V=1.0, delta=0), bus 2 (PQ, P=-1.0, Q=-0.5). "
        "Y12 = -j5. Newton-Raphson iteration: "
        "J * [d_delta; d_V] = [dP; dQ]. Converges in 3-4 iterations."
    ),
    tier=6,
    domain="power_systems",
    source="Wikipedia contributors, 'Power-flow study', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Power-flow_study",
    prerequisites=["three_phase_power"],
))
