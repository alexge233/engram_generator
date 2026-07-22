"""Knowledge atoms for PDE extensions, inorganic chemistry extensions,
and general chemistry extensions.

Each atom includes the canonical formula, a Wikipedia source, and a
worked example with known input/output for verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── PDE Extensions (tier 6-7) ───────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="poisson_equation",
    content=(
        "Poisson's equation is a partial differential equation of the "
        "form nabla^2 phi = f, where nabla^2 is the Laplace operator, "
        "phi is the unknown function, and f is a known source term. It "
        "generalises Laplace's equation (where f = 0). In electrostatics, "
        "nabla^2 V = -rho/epsilon_0."
    ),
    example=(
        "Given nabla^2 u = -6 on [0,1]x[0,1] with u=0 on boundary, "
        "and u(x,y) = 3x(1-x) + 3y(1-y) is a solution since "
        "u_xx + u_yy = -6 + 0 + 0 + -6 = ... checking: u_xx = -6, "
        "u_yy = -6, so nabla^2 u = -12 != -6. Correct particular "
        "solution: u = x(1-x) has u_xx = -2, so u = 3x(1-x) gives "
        "nabla^2 u = -6."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Poisson's equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Poisson%27s_equation",
    prerequisites=["laplace_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="helmholtz_equation",
    content=(
        "The Helmholtz equation is nabla^2 f + k^2 f = 0, where k is "
        "the wavenumber. It arises from separation of variables in the "
        "wave equation and describes time-harmonic wave propagation. "
        "Solutions are eigenfunctions of the Laplacian."
    ),
    example=(
        "1D Helmholtz: f'' + k^2 f = 0 with k=pi on [0,1], f(0)=f(1)=0. "
        "Solution: f(x) = sin(pi*x). Check: f'' = -pi^2 sin(pi*x), "
        "k^2 f = pi^2 sin(pi*x), sum = 0."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Helmholtz equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Helmholtz_equation",
    prerequisites=["wave_equation_1d"],
))

register_atom(Atom(
    atom_type="formula",
    name="advection_equation",
    content=(
        "The advection equation is du/dt + c * du/dx = 0, where c is "
        "the advection velocity. The solution is u(x,t) = f(x - ct), "
        "propagating the initial profile f at speed c without distortion."
    ),
    example=(
        "Given u(x,0) = sin(x), c=2: u(x,t) = sin(x - 2t). "
        "At t=1, x=pi: u(pi,1) = sin(pi - 2) = sin(1.1416) = 0.9093."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Advection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Advection",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="burgers_equation",
    content=(
        "Burgers' equation is du/dt + u * du/dx = nu * d^2u/dx^2, "
        "combining nonlinear advection with diffusion. The inviscid form "
        "(nu=0) develops shock waves. The Cole-Hopf transformation "
        "linearises it to the heat equation."
    ),
    example=(
        "Inviscid Burgers (nu=0) with u(x,0) = 1-x for 0<x<1: "
        "characteristics x = x0 + (1-x0)t cross at t=1, forming a shock. "
        "Shock speed from Rankine-Hugoniot: s = (u_L + u_R)/2 = (1+0)/2 = 0.5."
    ),
    tier=7,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Burgers' equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Burgers%27_equation",
    prerequisites=["advection_equation"],
))

register_atom(Atom(
    atom_type="definition",
    name="boundary_conditions_pde",
    content=(
        "Boundary conditions specify the behaviour of a PDE solution on "
        "the domain boundary. Dirichlet: u = g on boundary. Neumann: "
        "du/dn = g on boundary. Robin: a*u + b*du/dn = g (mixed). "
        "Well-posedness requires appropriate conditions for each PDE type."
    ),
    example=(
        "Heat equation u_t = u_xx on [0,1], Dirichlet BCs u(0,t)=0, "
        "u(1,t)=0, IC u(x,0)=sin(pi*x): solution u(x,t) = "
        "sin(pi*x)*exp(-pi^2*t). At t=0.1: u(0.5, 0.1) = "
        "sin(pi/2)*exp(-0.9870) = 1*0.3730 = 0.3730."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Boundary value problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Boundary_value_problem",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="eigenfunction_expansion",
    content=(
        "Eigenfunction expansion (Fourier method) represents the solution "
        "of a linear PDE as a series of eigenfunctions of the spatial "
        "operator. For the heat equation on [0,L] with homogeneous "
        "Dirichlet BCs, u(x,t) = sum_n B_n sin(n*pi*x/L) exp(-n^2*pi^2*t/L^2)."
    ),
    example=(
        "Heat equation on [0,1], u(x,0) = x(1-x): B_n = 2*int_0^1 "
        "x(1-x)sin(n*pi*x)dx. B_1 = 8/pi^3 = 0.2588. Leading term: "
        "u(0.5, 0.1) approx 0.2588*sin(pi/2)*exp(-pi^2*0.1) = "
        "0.2588*0.3730 = 0.0965."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Eigenfunction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Eigenfunction",
    prerequisites=["boundary_conditions_pde"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="crank_nicolson",
    content=(
        "The Crank-Nicolson method is an implicit finite difference scheme "
        "for the heat equation, averaging the spatial discretisation at "
        "time steps n and n+1. It is unconditionally stable and second-order "
        "accurate in both time and space: "
        "(u^{n+1}_j - u^n_j)/dt = (1/2)(D^2 u^n_j + D^2 u^{n+1}_j)."
    ),
    example=(
        "Heat equation u_t = u_xx, dx=0.25, dt=0.1, r=dt/dx^2=1.6. "
        "At interior point j=2, n=0 with u^0 = [0, 0.5, 1, 0.5, 0]: "
        "RHS = u^0_1 + (r/2)(u^0_0 - 2u^0_1 + u^0_2) = "
        "0.5 + 0.8*(0 - 1 + 1) = 0.5."
    ),
    tier=6,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Crank-Nicolson method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Crank%E2%80%93Nicolson_method",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="variational_pde",
    content=(
        "The variational (weak) formulation of a PDE replaces pointwise "
        "equations with integral conditions. For -nabla^2 u = f, the weak "
        "form is: find u in H^1_0 such that int nabla u . nabla v dx = "
        "int f*v dx for all test functions v in H^1_0. This is the basis "
        "for the finite element method."
    ),
    example=(
        "-u'' = 1 on [0,1], u(0)=u(1)=0. Weak form: int_0^1 u'v' dx = "
        "int_0^1 v dx. Exact solution: u(x) = x(1-x)/2. "
        "Check: u(0.5) = 0.5*0.5/2 = 0.125."
    ),
    tier=7,
    domain="partial_differential_equations",
    source="Wikipedia contributors, 'Weak formulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weak_formulation",
    prerequisites=["poisson_equation"],
))


# ── Inorganic Chemistry Extensions (tier 4-5) ───────────────────────

register_atom(Atom(
    atom_type="formula",
    name="lattice_energy",
    content=(
        "Lattice energy is the energy released when gaseous ions combine "
        "to form an ionic solid. The Born-Lande equation gives: "
        "U = -(N_A * M * z+ * z- * e^2)/(4*pi*epsilon_0*r_0) * (1 - 1/n), "
        "where M is the Madelung constant, z are ion charges, r_0 is the "
        "interionic distance, and n is the Born exponent."
    ),
    example=(
        "NaCl: M=1.7476, z+=1, z-=1, r_0=2.81e-10 m, n=8. "
        "U = -(6.022e23*1.7476*1*1*(1.602e-19)^2)/(4*pi*8.854e-12*2.81e-10)"
        "*(1-1/8) = -786 kJ/mol (experimental: -787 kJ/mol)."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Lattice energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lattice_energy",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="rule",
    name="ionic_radius_ratio",
    content=(
        "The radius ratio rule predicts coordination geometry in ionic "
        "crystals from r_cation/r_anion. Ranges: <0.155 linear (CN=2), "
        "0.155-0.225 trigonal (CN=3), 0.225-0.414 tetrahedral (CN=4), "
        "0.414-0.732 octahedral (CN=6), 0.732-1.0 cubic (CN=8)."
    ),
    example=(
        "NaCl: r(Na+)=1.02A, r(Cl-)=1.81A. Ratio = 1.02/1.81 = 0.564. "
        "Falls in 0.414-0.732 range, predicting octahedral (CN=6). "
        "Correct: NaCl has rock salt structure with CN=6."
    ),
    tier=4,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Radius ratio', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radius_ratio",
    prerequisites=["crystal_field"],
))

register_atom(Atom(
    atom_type="definition",
    name="band_theory_ext",
    content=(
        "Band theory describes electronic structure in solids. The valence "
        "band is the highest occupied band, the conduction band is the "
        "lowest unoccupied band. The band gap E_g determines: metal "
        "(E_g=0, overlapping bands), semiconductor (0<E_g<~3 eV), "
        "insulator (E_g>~3 eV)."
    ),
    example=(
        "Silicon: E_g = 1.12 eV at 300K. Semiconductor. "
        "Diamond: E_g = 5.47 eV. Insulator. "
        "Copper: bands overlap. Metal."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Electronic band structure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electronic_band_structure",
    prerequisites=["crystal_field"],
))

register_atom(Atom(
    atom_type="rule",
    name="nomenclature_complex",
    content=(
        "IUPAC nomenclature for coordination compounds: name ligands "
        "alphabetically with prefixes (di-, tri-, tetra-), then metal "
        "with oxidation state in Roman numerals. Anionic ligands end in "
        "-o (chlorido, hydroxido). Anionic complexes end in -ate."
    ),
    example=(
        "[Co(NH3)4Cl2]Cl: tetraamminedichloridocobalt(III) chloride. "
        "K3[Fe(CN)6]: potassium hexacyanidoferrate(III). "
        "[Pt(NH3)2Cl2]: diamminedichloridoplatinum(II)."
    ),
    tier=4,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'IUPAC nomenclature of inorganic chemistry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_inorganic_chemistry",
    prerequisites=["coordination_number"],
))

register_atom(Atom(
    atom_type="rule",
    name="trans_effect",
    content=(
        "The trans effect is the tendency of a ligand to direct "
        "substitution trans to itself in square planar complexes. "
        "Order: CO ~ CN- > NO2- > I- > Br- > Cl- > NH3 > OH-. "
        "Strong trans-effect ligands labilise the bond trans to them."
    ),
    example=(
        "Synthesis of cis-[Pt(NH3)2Cl2] (cisplatin): start with "
        "[PtCl4]2-, add NH3. Cl- has weaker trans effect than NH3, "
        "so first NH3 replaces Cl-. Second NH3 enters trans to Cl- "
        "(not trans to NH3), giving cis product."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Trans effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trans_effect",
    prerequisites=["nomenclature_complex"],
))

register_atom(Atom(
    atom_type="rule",
    name="hard_soft_acid_base",
    content=(
        "Pearson's HSAB principle: hard acids prefer hard bases, soft "
        "acids prefer soft bases. Hard acids: small, high charge, low "
        "polarisability (H+, Li+, Al3+, Ti4+). Soft acids: large, low "
        "charge, high polarisability (Cu+, Ag+, Hg2+, Pt2+). "
        "Hard bases: F-, OH-, NH3. Soft bases: I-, RS-, CO."
    ),
    example=(
        "AgI is insoluble (soft-soft), AgF is soluble (soft-hard mismatch). "
        "LiF is stable (hard-hard), LiI less so. "
        "Hg2+ binds RS- strongly (soft-soft): K_f very large."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'HSAB theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/HSAB_theory",
    prerequisites=["electronegativity_bond"],
))

register_atom(Atom(
    atom_type="definition",
    name="molecular_orbital_diagram",
    content=(
        "Molecular orbital (MO) theory constructs orbitals spanning the "
        "entire molecule from atomic orbital linear combinations. Bonding "
        "MOs have lower energy than constituent AOs; antibonding MOs have "
        "higher energy (marked with *). Bond order = (bonding e- - "
        "antibonding e-)/2."
    ),
    example=(
        "O2: 16 electrons. MO filling: sigma_1s^2 sigma*_1s^2 sigma_2s^2 "
        "sigma*_2s^2 sigma_2p^2 pi_2p^4 pi*_2p^2. Bond order = "
        "(10-6)/2 = 2. Two unpaired electrons in pi* (paramagnetic)."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Molecular orbital diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molecular_orbital_diagram",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="redox_balancing",
    content=(
        "Redox equation balancing by half-reaction method: (1) split into "
        "oxidation and reduction half-reactions, (2) balance atoms other "
        "than O and H, (3) balance O with H2O, (4) balance H with H+, "
        "(5) balance charge with electrons, (6) equalise electron transfer, "
        "(7) add half-reactions, (8) add OH- if basic."
    ),
    example=(
        "MnO4- + Fe2+ -> Mn2+ + Fe3+ (acidic). "
        "Reduction: MnO4- + 8H+ + 5e- -> Mn2+ + 4H2O. "
        "Oxidation: Fe2+ -> Fe3+ + e- (multiply by 5). "
        "Net: MnO4- + 8H+ + 5Fe2+ -> Mn2+ + 4H2O + 5Fe3+."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source="Wikipedia contributors, 'Half-reaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Half-reaction",
    prerequisites=["oxidation_state"],
))


# ── General Chemistry Extensions (tier 3-5) ─────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="limiting_reagent",
    content=(
        "The limiting reagent is the reactant consumed first in a "
        "chemical reaction, determining the maximum product yield. "
        "Compare moles available / stoichiometric coefficient for each "
        "reactant; the smallest ratio identifies the limiting reagent."
    ),
    example=(
        "2H2 + O2 -> 2H2O. Given 3 mol H2, 2 mol O2: "
        "H2: 3/2 = 1.5, O2: 2/1 = 2. H2 is limiting (smaller ratio). "
        "Max H2O = 3 mol (same coefficient as H2)."
    ),
    tier=3,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Limiting reagent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limiting_reagent",
    prerequisites=["stoichiometry"],
))

register_atom(Atom(
    atom_type="formula",
    name="percent_composition",
    content=(
        "Percent composition is the mass percentage of each element in "
        "a compound: % element = (n * atomic_mass / molar_mass) * 100, "
        "where n is the number of atoms of that element."
    ),
    example=(
        "H2O: M = 2(1.008) + 16.00 = 18.016 g/mol. "
        "%H = 2*1.008/18.016 * 100 = 11.19%. "
        "%O = 16.00/18.016 * 100 = 88.81%."
    ),
    tier=3,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Composition of a mixture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mass_fraction_(chemistry)",
    prerequisites=["molar_mass"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="empirical_formula",
    content=(
        "To find the empirical formula: (1) convert mass percentages to "
        "grams (assume 100g sample), (2) convert grams to moles, "
        "(3) divide all mole values by the smallest, (4) round to "
        "nearest whole number (multiply through if needed)."
    ),
    example=(
        "40.0% C, 6.7% H, 53.3% O. Moles: C=40/12.01=3.33, "
        "H=6.7/1.008=6.65, O=53.3/16.00=3.33. Divide by 3.33: "
        "C=1, H=2, O=1. Empirical formula: CH2O."
    ),
    tier=4,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Empirical formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Empirical_formula",
    prerequisites=["percent_composition"],
))

register_atom(Atom(
    atom_type="formula",
    name="solution_dilution",
    content=(
        "The dilution equation relates concentration and volume before "
        "and after dilution: M1*V1 = M2*V2, where M is molarity and V "
        "is volume. This holds because the number of moles of solute "
        "remains constant."
    ),
    example=(
        "Dilute 50 mL of 6.0 M HCl to 2.0 M. "
        "M1*V1 = M2*V2: 6.0*50 = 2.0*V2. V2 = 300/2.0 = 150 mL. "
        "Add 100 mL water to 50 mL stock."
    ),
    tier=3,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Dilution (equation)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dilution_(equation)",
    prerequisites=["molarity"],
))

register_atom(Atom(
    atom_type="formula",
    name="gas_law_combined",
    content=(
        "The combined gas law merges Boyle's, Charles's, and "
        "Gay-Lussac's laws: P1*V1/T1 = P2*V2/T2, where P is pressure, "
        "V is volume, and T is absolute temperature (Kelvin)."
    ),
    example=(
        "Gas at P1=2 atm, V1=3 L, T1=300K is heated to T2=600K at "
        "P2=4 atm. V2 = P1*V1*T2/(T1*P2) = 2*3*600/(300*4) = "
        "3600/1200 = 3.0 L."
    ),
    tier=4,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Combined gas law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Combined_gas_law",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula",
    name="dalton_partial_pressure",
    content=(
        "Dalton's law of partial pressures: the total pressure of a gas "
        "mixture equals the sum of partial pressures: P_total = sum(P_i). "
        "Each component's partial pressure: P_i = x_i * P_total, where "
        "x_i is the mole fraction."
    ),
    example=(
        "Mixture: 2 mol N2, 1 mol O2, total P=3 atm. "
        "x_N2 = 2/3, x_O2 = 1/3. "
        "P_N2 = (2/3)*3 = 2 atm, P_O2 = (1/3)*3 = 1 atm."
    ),
    tier=4,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Dalton's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dalton%27s_law",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula",
    name="acid_base_titration",
    content=(
        "In acid-base titration, the equivalence point is where "
        "moles acid = moles base (for monoprotic). At the equivalence "
        "point: M_acid * V_acid = M_base * V_base. The pH at equivalence "
        "depends on the salt formed: strong-strong gives pH=7, "
        "weak acid-strong base gives pH>7."
    ),
    example=(
        "Titrate 25 mL of 0.1 M HCl with 0.1 M NaOH. "
        "At equivalence: 0.1*25 = 0.1*V_NaOH, V_NaOH = 25 mL. "
        "Strong-strong: pH = 7.0 at equivalence."
    ),
    tier=5,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Acid-base titration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Acid%E2%80%93base_titration",
    prerequisites=["ph_calculation"],
))

register_atom(Atom(
    atom_type="formula",
    name="buffer_capacity",
    content=(
        "Buffer capacity (beta) measures a buffer's resistance to pH "
        "change: beta = dC_b/dpH, where C_b is the amount of strong "
        "base added. Maximum buffer capacity occurs when pH = pKa "
        "(equal concentrations of acid and conjugate base). "
        "Henderson-Hasselbalch: pH = pKa + log([A-]/[HA])."
    ),
    example=(
        "Acetate buffer: pKa = 4.76, [HA] = 0.1 M, [A-] = 0.1 M. "
        "pH = 4.76 + log(0.1/0.1) = 4.76 + 0 = 4.76. "
        "Add 0.01 mol NaOH to 1L: [A-]=0.11, [HA]=0.09. "
        "pH = 4.76 + log(0.11/0.09) = 4.76 + 0.087 = 4.847."
    ),
    tier=5,
    domain="general_chemistry",
    source="Wikipedia contributors, 'Buffer solution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Buffer_solution",
    prerequisites=["ph_calculation"],
))
