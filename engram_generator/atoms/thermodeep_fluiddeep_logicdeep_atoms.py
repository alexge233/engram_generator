"""Knowledge atoms for thermo_deep, fluid_deep, and logic_deep generators."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── THERMO_DEEP ──────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="stirling_cycle",
    content=(
        "The Stirling cycle is a thermodynamic cycle consisting of two "
        "isothermal and two isochoric (constant-volume) processes. The "
        "ideal Stirling engine efficiency equals the Carnot efficiency: "
        "eta = 1 - T_cold/T_hot. Work output per cycle: "
        "W = nR(T_hot - T_cold) ln(V_max/V_min)."
    ),
    example=(
        "Given T_hot=600K, T_cold=300K, n=1mol, V_max/V_min=2: "
        "W = 1*8.314*(600-300)*ln(2) = 8.314*300*0.6931 = 1728.5 J"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Stirling cycle', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Stirling_cycle",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="joule_expansion",
    content=(
        "Free expansion (Joule expansion) is an irreversible process "
        "where a gas expands into a vacuum. For an ideal gas: dT = 0 "
        "(no temperature change), dU = 0, dS = nR ln(V2/V1) > 0."
    ),
    example=(
        "Given n=2mol ideal gas, V1=1L, V2=4L: "
        "dS = 2*8.314*ln(4/1) = 2*8.314*1.386 = 23.05 J/K"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Free expansion', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Free_expansion",
    prerequisites=["entropy_change"],
))

register_atom(Atom(
    atom_type="formula",
    name="gibbs_phase_rule",
    content=(
        "The Gibbs phase rule relates the number of degrees of freedom "
        "(F) to the number of components (C) and phases (P) in "
        "thermodynamic equilibrium: F = C - P + 2."
    ),
    example=(
        "Water at triple point: C=1 (H2O), P=3 (solid, liquid, gas): "
        "F = 1 - 3 + 2 = 0 (no degrees of freedom, fixed T and P)"
    ),
    tier=4,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Phase rule', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Phase_rule",
    prerequisites=["first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula",
    name="chemical_potential",
    content=(
        "The chemical potential mu_i of species i is the partial molar "
        "Gibbs free energy: mu_i = (dG/dn_i)_{T,P,n_j}. For an ideal "
        "gas: mu = mu_0 + RT ln(P/P_0). At equilibrium, mu is equal "
        "in all coexisting phases."
    ),
    example=(
        "Ideal gas at T=300K, P=2atm, mu_0=-10kJ/mol: "
        "mu = -10000 + 8.314*300*ln(2) = -10000 + 1729 = -8271 J/mol"
    ),
    tier=6,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Chemical potential', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Chemical_potential",
    prerequisites=["gibbs_free_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_pump",
    content=(
        "A heat pump transfers heat from a cold reservoir to a hot "
        "reservoir using work. The coefficient of performance for "
        "heating: COP_H = Q_H/W = T_H/(T_H - T_C) for a Carnot "
        "heat pump. For cooling: COP_C = Q_C/W = T_C/(T_H - T_C)."
    ),
    example=(
        "Carnot heat pump, T_H=300K, T_C=260K: "
        "COP_H = 300/(300-260) = 300/40 = 7.5"
    ),
    tier=4,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Heat pump', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Heat_pump",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="debye_temperature",
    content=(
        "The Debye temperature Theta_D characterises the temperature "
        "above which all phonon modes are excited. Theta_D = h*nu_D/k_B "
        "where nu_D is the Debye cutoff frequency. The Debye model for "
        "heat capacity: C_V -> 3Nk_B for T >> Theta_D (Dulong-Petit), "
        "C_V -> (12/5)pi^4 Nk_B (T/Theta_D)^3 for T << Theta_D."
    ),
    example=(
        "Diamond: Theta_D = 2230K. At T=300K (T/Theta_D=0.135): "
        "C_V ~ 3Nk_B*(12pi^4/5)*(0.135)^3 = low heat capacity"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Debye model', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Debye_model",
    prerequisites=["heat_capacity"],
))

register_atom(Atom(
    atom_type="formula",
    name="fugacity",
    content=(
        "Fugacity f is an effective pressure that replaces actual "
        "pressure for real gases: mu = mu_0 + RT ln(f/P_0). The "
        "fugacity coefficient phi = f/P. For an ideal gas, phi = 1 "
        "and f = P. Fugacity is related to the equation of state by: "
        "ln(phi) = integral_0^P (Z-1)/P dP."
    ),
    example=(
        "Gas with Z=0.95 at P=10atm (constant Z approximation): "
        "ln(phi) = (0.95-1)*ln(10/1) = -0.05*2.303 = -0.115, "
        "phi = 0.891, f = 0.891*10 = 8.91 atm"
    ),
    tier=6,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Fugacity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fugacity",
    prerequisites=["chemical_potential"],
))

register_atom(Atom(
    atom_type="formula",
    name="availability_exergy",
    content=(
        "Exergy (availability) is the maximum useful work obtainable "
        "from a system as it reaches equilibrium with its environment. "
        "For a closed system: Ex = (U - U_0) + P_0(V - V_0) "
        "- T_0(S - S_0). For a flow stream: ex = (h - h_0) "
        "- T_0(s - s_0) + V^2/2 + gz."
    ),
    example=(
        "Steam at T=500K, h=2800kJ/kg, s=7.0kJ/(kg*K), "
        "environment T_0=300K, h_0=100kJ/kg, s_0=0.3kJ/(kg*K): "
        "ex = (2800-100) - 300*(7.0-0.3) = 2700 - 2010 = 690 kJ/kg"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Exergy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Exergy",
    prerequisites=["first_law_thermo", "entropy_change"],
))

# ── FLUID_DEEP ───────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="mach_number",
    content=(
        "The Mach number M is the ratio of flow velocity to the local "
        "speed of sound: M = v/a, where a = sqrt(gamma*R*T) for an "
        "ideal gas. M < 1 is subsonic, M = 1 transonic, M > 1 "
        "supersonic, M > 5 hypersonic."
    ),
    example=(
        "Aircraft at v=340m/s in air at T=288K (gamma=1.4, R=287): "
        "a = sqrt(1.4*287*288) = sqrt(115891) = 340.4 m/s, "
        "M = 340/340.4 = 0.999 (transonic)"
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Mach number', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mach_number",
    prerequisites=["reynolds_number"],
))

register_atom(Atom(
    atom_type="formula",
    name="isentropic_flow",
    content=(
        "Isentropic flow relations for a calorically perfect gas: "
        "T/T_0 = (1 + (gamma-1)/2 * M^2)^(-1), "
        "P/P_0 = (T/T_0)^(gamma/(gamma-1)), "
        "rho/rho_0 = (T/T_0)^(1/(gamma-1)) where T_0, P_0, rho_0 "
        "are stagnation (total) quantities."
    ),
    example=(
        "Air (gamma=1.4) at M=2: T/T_0 = 1/(1+0.2*4) = 1/1.8 = 0.556, "
        "P/P_0 = 0.556^3.5 = 0.1278"
    ),
    tier=6,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Isentropic process', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Isentropic_process",
    prerequisites=["mach_number"],
))

register_atom(Atom(
    atom_type="formula",
    name="normal_shock",
    content=(
        "Normal shock relations connect upstream (1) and downstream (2) "
        "conditions across a stationary shock wave. For a calorically "
        "perfect gas: M2^2 = ((gamma-1)*M1^2 + 2)/(2*gamma*M1^2 "
        "- (gamma-1)), P2/P1 = 1 + 2*gamma/(gamma+1)*(M1^2 - 1), "
        "T2/T1 = (P2/P1)*(rho1/rho2)."
    ),
    example=(
        "Air (gamma=1.4) with M1=2: "
        "M2^2 = (0.4*4+2)/(2.8*4-0.4) = 3.6/10.8 = 0.333, M2=0.577, "
        "P2/P1 = 1+2.8/2.4*(4-1) = 1+3.5 = 4.5"
    ),
    tier=6,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Normal shock', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Normal_shock",
    prerequisites=["mach_number", "isentropic_flow"],
))

register_atom(Atom(
    atom_type="formula",
    name="boundary_layer",
    content=(
        "The boundary layer is the thin region near a solid surface "
        "where viscous effects are significant. For laminar flow over "
        "a flat plate (Blasius solution): delta = 5x/sqrt(Re_x), "
        "where Re_x = rho*U*x/mu. Skin friction: "
        "C_f = 0.664/sqrt(Re_x)."
    ),
    example=(
        "Air (rho=1.2, mu=1.8e-5) over plate at U=10m/s, x=0.5m: "
        "Re_x = 1.2*10*0.5/1.8e-5 = 333333, "
        "delta = 5*0.5/sqrt(333333) = 2.5/577 = 0.00433 m = 4.33 mm"
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Boundary layer', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Boundary_layer",
    prerequisites=["reynolds_number"],
))

register_atom(Atom(
    atom_type="formula",
    name="orifice_flow",
    content=(
        "Flow through a sharp-edged orifice is given by: "
        "Q = C_d * A * sqrt(2*dP/rho), where C_d is the discharge "
        "coefficient (typically 0.6-0.65 for sharp-edged), A is the "
        "orifice area, dP is the pressure drop, and rho is density."
    ),
    example=(
        "Orifice d=5cm (A=0.00196m^2), C_d=0.62, dP=10kPa, "
        "rho=1000kg/m^3 (water): "
        "Q = 0.62*0.00196*sqrt(2*10000/1000) = 0.00122*4.47 = 0.00544 m^3/s"
    ),
    tier=4,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Orifice plate', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Orifice_plate",
    prerequisites=["bernoulli"],
))

register_atom(Atom(
    atom_type="formula",
    name="water_hammer",
    content=(
        "Water hammer (hydraulic shock) occurs when fluid in motion "
        "is forced to stop abruptly. The Joukowsky equation gives the "
        "pressure rise: dP = rho * a * dv, where a is the wave speed "
        "a = sqrt(K/rho) for rigid pipes or "
        "a = sqrt(K/(rho*(1 + K*D/(E*t)))) for elastic pipes."
    ),
    example=(
        "Water (rho=1000, K=2.2e9 Pa) in rigid pipe, dv=2m/s: "
        "a = sqrt(2.2e9/1000) = 1483 m/s, "
        "dP = 1000*1483*2 = 2,966,000 Pa = 29.7 atm"
    ),
    tier=5,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Water hammer', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Water_hammer",
    prerequisites=["bernoulli"],
))

register_atom(Atom(
    atom_type="formula",
    name="froude_number",
    content=(
        "The Froude number Fr is the ratio of flow inertia to "
        "gravitational effects: Fr = v/sqrt(g*L), where v is flow "
        "velocity, g is gravitational acceleration, and L is a "
        "characteristic length (e.g. water depth). Fr < 1 is subcritical "
        "(tranquil), Fr > 1 is supercritical (rapid)."
    ),
    example=(
        "River flow v=3m/s, depth h=2m: "
        "Fr = 3/sqrt(9.81*2) = 3/4.43 = 0.677 (subcritical)"
    ),
    tier=4,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Froude number', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Froude_number",
    prerequisites=["reynolds_number"],
))

register_atom(Atom(
    atom_type="formula",
    name="weir_flow",
    content=(
        "Flow over a rectangular weir is given by the Francis formula: "
        "Q = C_d * (2/3) * sqrt(2g) * L * H^(3/2), where L is weir "
        "length, H is head above the weir crest, and C_d is the "
        "discharge coefficient (typically 0.6-0.62)."
    ),
    example=(
        "Rectangular weir L=2m, H=0.3m, C_d=0.62: "
        "Q = 0.62*(2/3)*sqrt(2*9.81)*2*0.3^1.5 "
        "= 0.62*0.667*4.43*2*0.1643 = 0.601 m^3/s"
    ),
    tier=4,
    domain="fluid_mechanics",
    source="Wikipedia contributors, 'Weir', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Weir",
    prerequisites=["bernoulli"],
))

# ── LOGIC_DEEP ───────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="ordinal_arithmetic",
    content=(
        "Ordinal arithmetic extends arithmetic to transfinite ordinals. "
        "Addition: alpha + beta is the order type of alpha followed by "
        "beta. Multiplication: alpha * beta is beta copies of alpha. "
        "Key property: ordinal addition is NOT commutative. "
        "1 + omega = omega, but omega + 1 > omega."
    ),
    example=(
        "omega + 3: omega followed by {0,1,2} = omega+3. "
        "3 + omega = omega (absorbed). "
        "omega * 2 = omega + omega."
    ),
    tier=6,
    domain="set_theory",
    source="Wikipedia contributors, 'Ordinal arithmetic', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Ordinal_arithmetic",
    prerequisites=["set_cardinality_infinite"],
))

register_atom(Atom(
    atom_type="definition",
    name="cardinal_arithmetic",
    content=(
        "Cardinal arithmetic extends arithmetic to infinite cardinals. "
        "For infinite cardinals: aleph_0 + aleph_0 = aleph_0, "
        "aleph_0 * aleph_0 = aleph_0, 2^aleph_0 = c (continuum). "
        "For any infinite cardinal kappa: kappa + kappa = kappa, "
        "kappa * kappa = kappa."
    ),
    example=(
        "aleph_0 * 5 = aleph_0 (absorbs finite). "
        "aleph_0 + aleph_0 = aleph_0. "
        "aleph_0^aleph_0 = 2^aleph_0 = c."
    ),
    tier=6,
    domain="set_theory",
    source="Wikipedia contributors, 'Cardinal arithmetic', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Cardinal_number#Cardinal_arithmetic",
    prerequisites=["set_cardinality_infinite"],
))

register_atom(Atom(
    atom_type="theorem",
    name="axiom_of_choice_app",
    content=(
        "The Axiom of Choice (AC) states that for any collection of "
        "non-empty sets, there exists a function that selects one "
        "element from each set. Equivalently: every surjection has a "
        "right inverse. AC is equivalent to Zorn's lemma (every "
        "partially ordered set with upper bounds has a maximal element) "
        "and the well-ordering theorem (every set can be well-ordered)."
    ),
    example=(
        "Using Zorn's lemma: every vector space has a basis. "
        "Proof sketch: partially order linearly independent subsets "
        "by inclusion; upper bound of chain is union; "
        "maximal element is a basis."
    ),
    tier=7,
    domain="set_theory",
    source="Wikipedia contributors, 'Axiom of choice', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Axiom_of_choice",
    prerequisites=["well_ordering"],
))

register_atom(Atom(
    atom_type="theorem",
    name="transfinite_induction",
    content=(
        "Transfinite induction extends mathematical induction to "
        "well-ordered sets. To prove P(alpha) for all ordinals alpha: "
        "(1) Base: P(0). (2) Successor: P(alpha) implies P(alpha+1). "
        "(3) Limit: if P(beta) for all beta < lambda (limit ordinal), "
        "then P(lambda)."
    ),
    example=(
        "Prove every ordinal alpha has alpha + 0 = alpha: "
        "Base: 0 + 0 = 0. Successor: (alpha+1)+0 = alpha+1. "
        "Limit: sup{beta+0 : beta<lambda} = sup{beta} = lambda."
    ),
    tier=7,
    domain="set_theory",
    source="Wikipedia contributors, 'Transfinite induction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Transfinite_induction",
    prerequisites=["ordinal_arithmetic"],
))

register_atom(Atom(
    atom_type="definition",
    name="set_cardinality_infinite",
    content=(
        "Two sets have the same cardinality if there exists a bijection "
        "between them. A set is countably infinite if it has the same "
        "cardinality as the natural numbers (aleph_0). The reals are "
        "uncountable (Cantor's diagonal argument): |R| = c = 2^aleph_0. "
        "Cantor's theorem: |P(A)| > |A| for any set A."
    ),
    example=(
        "Z is countable: bijection n -> {0,1,-1,2,-2,...}. "
        "Q is countable (Cantor pairing). "
        "R is uncountable (diagonal argument)."
    ),
    tier=5,
    domain="set_theory",
    source="Wikipedia contributors, 'Cardinality', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Cardinality",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="well_ordering",
    content=(
        "The well-ordering theorem states that every set can be "
        "well-ordered (i.e., every non-empty subset has a least "
        "element). This is equivalent to the Axiom of Choice and "
        "Zorn's lemma. A well-order on a set S is a total order "
        "such that every non-empty subset has a minimum."
    ),
    example=(
        "N is well-ordered by <=. "
        "Z is NOT well-ordered by <= (no minimum), "
        "but CAN be well-ordered by: 0 < 1 < -1 < 2 < -2 < ..."
    ),
    tier=6,
    domain="set_theory",
    source="Wikipedia contributors, 'Well-ordering theorem', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Well-ordering_theorem",
    prerequisites=["set_cardinality_infinite"],
))

register_atom(Atom(
    atom_type="definition",
    name="boolean_algebra_lattice",
    content=(
        "A Boolean algebra is a complemented distributive lattice. "
        "It has operations meet (AND), join (OR), complement (NOT), "
        "and constants 0 and 1. Key laws: idempotent (a AND a = a), "
        "complement (a AND NOT a = 0), distributive "
        "(a AND (b OR c) = (a AND b) OR (a AND c)), "
        "De Morgan (NOT(a AND b) = NOT a OR NOT b)."
    ),
    example=(
        "Power set P({a,b}) as Boolean algebra: "
        "meet = intersection, join = union, complement = set difference. "
        "{a} AND {b} = {}, {a} OR {b} = {a,b}, NOT {a} = {b}."
    ),
    tier=5,
    domain="logic",
    source="Wikipedia contributors, 'Boolean algebra (structure)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Boolean_algebra_(structure)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="zfc_axiom_apply",
    content=(
        "ZFC (Zermelo-Fraenkel with Choice) is the standard axiomatic "
        "set theory. Key axioms: extensionality (sets equal iff same "
        "members), pairing ({a,b} exists), union (union of a set "
        "exists), power set (P(A) exists), infinity (an infinite set "
        "exists), separation (subsets by formula exist), replacement "
        "(image of a set under a function exists), foundation (no "
        "infinite descending membership chains)."
    ),
    example=(
        "Union axiom: given {{1,2},{3,4}}, union = {1,2,3,4}. "
        "Power set: P({a,b}) = {{}, {a}, {b}, {a,b}}. "
        "Separation: {x in N : x is even} = {0,2,4,...}."
    ),
    tier=7,
    domain="set_theory",
    source="Wikipedia contributors, 'Zermelo-Fraenkel set theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory",
    prerequisites=["well_ordering", "axiom_of_choice_app"],
))
