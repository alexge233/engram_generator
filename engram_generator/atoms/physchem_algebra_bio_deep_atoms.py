"""Knowledge atoms for physical chemistry ext, algebra deep, and biology deep.

Registers formula, theorem, and definition atoms with Wikipedia sources
and worked examples for independent verification of generator outputs.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# Physical Chemistry Ext (tier 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="reaction_half_life",
    content=(
        "The half-life of a reaction is the time required for the "
        "concentration of a reactant to decrease to half its initial "
        "value. For a first-order reaction: t_1/2 = ln(2)/k, where k "
        "is the rate constant. For a second-order reaction: "
        "t_1/2 = 1/(k*[A]_0). For zero-order: t_1/2 = [A]_0/(2k)."
    ),
    example=(
        "First-order, k=0.0693 s^-1: t_1/2 = ln(2)/0.0693 = "
        "0.6931/0.0693 = 10.0 s"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Half-life', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Half-life",
    prerequisites=["rate_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="integrated_rate_law",
    content=(
        "Integrated rate laws relate concentration to time. "
        "Zero-order: [A] = [A]_0 - kt. "
        "First-order: ln([A]) = ln([A]_0) - kt, or [A] = [A]_0*e^(-kt). "
        "Second-order: 1/[A] = 1/[A]_0 + kt."
    ),
    example=(
        "First-order, [A]_0=1.0 M, k=0.1 s^-1, t=5 s: "
        "[A] = 1.0*e^(-0.1*5) = 1.0*e^(-0.5) = 0.6065 M"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Rate equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rate_equation",
    prerequisites=["rate_law", "arrhenius"],
))

register_atom(Atom(
    atom_type="formula",
    name="transition_state",
    content=(
        "Transition state theory (Eyring equation) gives the rate "
        "constant as: k = (k_B*T/h)*exp(-dG_ddagger/(R*T)), where "
        "k_B is Boltzmann's constant, h is Planck's constant, "
        "dG_ddagger is the Gibbs free energy of activation, R is "
        "the gas constant, and T is temperature."
    ),
    example=(
        "T=298 K, dG_ddagger=80 kJ/mol: "
        "k = (1.381e-23*298)/(6.626e-34)*exp(-80000/(8.314*298)) "
        "= 6.212e12*exp(-32.28) = 6.212e12*9.88e-15 = 0.0614 s^-1"
    ),
    tier=6,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Transition state theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transition_state_theory",
    prerequisites=["arrhenius", "gibbs_spontaneity"],
))

register_atom(Atom(
    atom_type="formula",
    name="equilibrium_ice_table",
    content=(
        "An ICE table (Initial, Change, Equilibrium) is used to "
        "calculate equilibrium concentrations. Given initial "
        "concentrations and the equilibrium constant K, set up "
        "the table with change x, then solve K = products/reactants "
        "for x."
    ),
    example=(
        "A <-> B, K=4.0, [A]_0=1.0 M, [B]_0=0: "
        "ICE: [A]=1.0-x, [B]=x. K = x/(1.0-x) = 4.0. "
        "x = 4.0 - 4.0x, 5.0x = 4.0, x = 0.8. "
        "[A]=0.2 M, [B]=0.8 M"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Equilibrium constant', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Equilibrium_constant",
    prerequisites=["equilibrium_constant"],
))

register_atom(Atom(
    atom_type="formula",
    name="colligative_properties",
    content=(
        "Colligative properties depend on the number of solute "
        "particles. Boiling point elevation: dT_b = i*K_b*m. "
        "Freezing point depression: dT_f = i*K_f*m. "
        "Osmotic pressure: pi = i*M*R*T. "
        "Where i is the van't Hoff factor, m is molality, M is "
        "molarity, K_b and K_f are ebullioscopic and cryoscopic "
        "constants."
    ),
    example=(
        "NaCl (i=2) in water, m=0.5, K_f=1.86 K*kg/mol: "
        "dT_f = 2*1.86*0.5 = 1.86 K depression"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Colligative properties', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Colligative_properties",
    prerequisites=["molarity"],
))

register_atom(Atom(
    atom_type="formula",
    name="chemical_kinetics_mechanism",
    content=(
        "A reaction mechanism is a sequence of elementary steps. "
        "The rate-determining step (slowest) controls the overall "
        "rate. The steady-state approximation assumes d[intermediate]/dt "
        "= 0 to derive the rate law from the mechanism."
    ),
    example=(
        "Mechanism: A -> B (k1, slow), B -> C (k2, fast). "
        "Rate = k1*[A] (first-order, determined by slow step)"
    ),
    tier=6,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Reaction mechanism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reaction_mechanism",
    prerequisites=["rate_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="phase_equilibria",
    content=(
        "The Clausius-Clapeyron equation relates vapour pressure "
        "to temperature: ln(P2/P1) = -(dH_vap/R)*(1/T2 - 1/T1), "
        "where dH_vap is the enthalpy of vaporisation. Phase "
        "diagrams show regions of solid, liquid, gas stability "
        "as functions of P and T."
    ),
    example=(
        "Water: dH_vap=40.7 kJ/mol, P1=1 atm at T1=373 K, "
        "find P at T2=383 K: ln(P2/1) = -(40700/8.314)*(1/383 - 1/373) "
        "= -4894*(-7.02e-5) = 0.3437. P2 = e^0.3437 = 1.41 atm"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Clausius-Clapeyron relation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation",
    prerequisites=["first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula",
    name="electrochemistry_cell",
    content=(
        "The cell potential E_cell = E_cathode - E_anode. "
        "Standard cell potential uses standard reduction potentials. "
        "The Nernst equation gives non-standard conditions: "
        "E = E0 - (RT/nF)*ln(Q). Gibbs free energy: dG = -nFE."
    ),
    example=(
        "Zn/Cu cell: E0_Cu=+0.34 V, E0_Zn=-0.76 V. "
        "E_cell = 0.34 - (-0.76) = 1.10 V. "
        "dG = -2*96485*1.10 = -212267 J = -212.3 kJ"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Electrochemical cell', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electrochemical_cell",
    prerequisites=["nernst_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="quantum_chem_orbital",
    content=(
        "Molecular orbital theory constructs molecular orbitals "
        "as linear combinations of atomic orbitals (LCAO). "
        "Bond order = (bonding electrons - antibonding electrons)/2. "
        "Higher bond order means stronger, shorter bonds."
    ),
    example=(
        "O2: 10 bonding, 6 antibonding electrons. "
        "Bond order = (10-6)/2 = 2.0 (double bond)"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Molecular orbital theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molecular_orbital_theory",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="formula",
    name="partition_function_chem",
    content=(
        "The molecular partition function q = sum_i g_i*exp(-E_i/(k_B*T)) "
        "sums over all energy states. For translational motion: "
        "q_trans = (2*pi*m*k_B*T/h^2)^(3/2) * V. "
        "Thermodynamic quantities derive from q: "
        "U = k_B*T^2*(d ln q/dT), S = k_B*ln(q) + U/T."
    ),
    example=(
        "Two-level system, g0=1, E0=0, g1=3, E1=500 cm^-1, T=300 K: "
        "k_B*T = 208.5 cm^-1. q = 1 + 3*exp(-500/208.5) = "
        "1 + 3*0.0907 = 1.272"
    ),
    tier=6,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Partition function (statistical mechanics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Partition_function_(statistical_mechanics)",
    prerequisites=["partition_function_stat"],
))


# ===================================================================
# Algebra Deep (tier 5-7)
# ===================================================================

register_atom(Atom(
    atom_type="theorem",
    name="sylow_theorem",
    content=(
        "Sylow's theorems: Let G be a finite group of order n = p^a*m "
        "where p does not divide m. Then: (1) G has a subgroup of "
        "order p^a (Sylow p-subgroup). (2) All Sylow p-subgroups "
        "are conjugate. (3) The number n_p of Sylow p-subgroups "
        "satisfies n_p = 1 (mod p) and n_p divides m."
    ),
    example=(
        "|G|=12=2^2*3: n_3 divides 4 and n_3=1(mod 3), so n_3 in "
        "{1,4}. n_2 divides 3 and n_2=1(mod 2), so n_2 in {1,3}."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Sylow theorems', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sylow_theorems",
    prerequisites=["lagrange_verify", "normal_subgroup"],
))

register_atom(Atom(
    atom_type="definition",
    name="direct_product_group",
    content=(
        "The direct product G x H of groups G and H has elements "
        "(g,h) with operation (g1,h1)*(g2,h2) = (g1*g2, h1*h2). "
        "|G x H| = |G|*|H|. The direct product is abelian iff both "
        "factors are abelian."
    ),
    example=(
        "Z_2 x Z_3: elements {(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)}, "
        "|Z_2 x Z_3| = 6. (1,2)+(1,1) = (0,0) in Z_2 x Z_3."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Direct product of groups', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Direct_product_of_groups",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="quotient_ring",
    content=(
        "Given a ring R and an ideal I, the quotient ring R/I has "
        "elements as cosets r + I, with operations "
        "(r1+I)+(r2+I) = (r1+r2)+I and (r1+I)*(r2+I) = (r1*r2)+I. "
        "R/I is a field iff I is maximal."
    ),
    example=(
        "Z/3Z: elements {0+3Z, 1+3Z, 2+3Z}. "
        "(2+3Z)*(2+3Z) = 4+3Z = 1+3Z. This is the field F_3."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Quotient ring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quotient_ring",
    prerequisites=["ring_axiom_check", "ideal_test"],
))

register_atom(Atom(
    atom_type="theorem",
    name="polynomial_irreducibility",
    content=(
        "A polynomial f(x) in F[x] is irreducible if it cannot be "
        "factored into non-constant polynomials over F. Tests: "
        "Eisenstein's criterion (exists prime p dividing all "
        "coefficients except the leading one, p^2 not dividing the "
        "constant term). Reduction mod p for irreducibility over Z."
    ),
    example=(
        "f(x) = x^2 + 1 over R: irreducible (no real roots). "
        "Over C: reducible as (x+i)(x-i). "
        "x^3 + 3x + 3 over Q: Eisenstein with p=3 (3|3,3; 9 not | 3)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Irreducible polynomial', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Irreducible_polynomial",
    prerequisites=["polynomial_ring"],
))

register_atom(Atom(
    atom_type="definition",
    name="splitting_field",
    content=(
        "The splitting field of a polynomial f(x) over F is the "
        "smallest field extension of F in which f splits into "
        "linear factors. It is unique up to isomorphism. "
        "The degree [K:F] divides n! where n = deg(f)."
    ),
    example=(
        "f(x) = x^2 - 2 over Q: splitting field is Q(sqrt(2)), "
        "[Q(sqrt(2)):Q] = 2. f splits as (x-sqrt(2))(x+sqrt(2))."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Splitting field', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Splitting_field",
    prerequisites=["field_extension", "polynomial_irreducibility"],
))

register_atom(Atom(
    atom_type="definition",
    name="group_presentation",
    content=(
        "A group presentation <S|R> specifies generators S and "
        "relations R. The group is the quotient of the free group "
        "on S by the normal closure of R. Example: "
        "<a,b | a^n=e, b^2=e, bab=a^{-1}> is the dihedral group D_n."
    ),
    example=(
        "D_3 = <r,s | r^3=e, s^2=e, srs=r^{-1}>: "
        "|D_3|=6, elements {e,r,r^2,s,sr,sr^2}."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Presentation of a group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Presentation_of_a_group",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="smith_normal_form",
    content=(
        "The Smith normal form of an integer matrix A is a diagonal "
        "matrix D = UAV where U, V are invertible over Z, and the "
        "diagonal entries d_1|d_2|...|d_r are the invariant factors. "
        "Used to classify finitely generated abelian groups."
    ),
    example=(
        "A = [[2,4],[6,8]]: row reduce -> [[2,4],[0,-4]] -> "
        "[[2,0],[0,-4]] -> [[2,0],[0,4]]. Smith form: diag(2,4). "
        "Z^2/im(A) = Z_2 x Z_4."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Smith normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Smith_normal_form",
    prerequisites=["determinant"],
))

register_atom(Atom(
    atom_type="definition",
    name="exterior_algebra",
    content=(
        "The exterior algebra (Grassmann algebra) of a vector space V "
        "is the direct sum of exterior powers: Lambda(V) = "
        "sum_{k=0}^n Lambda^k(V). The wedge product is "
        "anticommutative: v^w = -w^v. dim(Lambda^k(V)) = C(n,k)."
    ),
    example=(
        "V = R^3 with basis {e1,e2,e3}: "
        "e1^e2 = -e2^e1, e1^e1 = 0. "
        "dim(Lambda^2(R^3)) = C(3,2) = 3, basis {e1^e2, e1^e3, e2^e3}."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Exterior algebra', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exterior_algebra",
    prerequisites=["tensor_product_modules"],
))

register_atom(Atom(
    atom_type="definition",
    name="tensor_product_modules",
    content=(
        "The tensor product M tensor_R N of R-modules M and N is "
        "the R-module generated by symbols m tensor n, subject to "
        "bilinearity: (m1+m2) tensor n = m1 tensor n + m2 tensor n, "
        "m tensor (n1+n2) = m tensor n1 + m tensor n2, "
        "r*(m tensor n) = (r*m) tensor n = m tensor (r*n)."
    ),
    example=(
        "Z_2 tensor_Z Z_3: every element m tensor n satisfies "
        "2*(m tensor n) = (2m) tensor n = 0 tensor n = 0, and "
        "3*(m tensor n) = m tensor (3n) = m tensor 0 = 0. "
        "Since gcd(2,3)=1, Z_2 tensor_Z Z_3 = 0."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Tensor product of modules', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tensor_product_of_modules",
    prerequisites=["ring_axiom_check"],
))

register_atom(Atom(
    atom_type="theorem",
    name="galois_group",
    content=(
        "The Galois group Gal(K/F) of a field extension K/F is the "
        "group of field automorphisms of K that fix F. For a "
        "separable polynomial f of degree n, |Gal(K/F)| = [K:F] "
        "and Gal(K/F) is a subgroup of S_n. The fundamental theorem "
        "of Galois theory establishes a correspondence between "
        "subgroups of Gal(K/F) and intermediate fields."
    ),
    example=(
        "f(x) = x^2 - 2 over Q: K = Q(sqrt(2)), "
        "Gal(K/Q) = {id, sigma} where sigma(sqrt(2)) = -sqrt(2). "
        "Gal(K/Q) = Z_2."
    ),
    tier=7,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Galois group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Galois_group",
    prerequisites=["splitting_field", "group_axiom_check"],
))


# ===================================================================
# Biology Deep (tier 3-5)
# ===================================================================

register_atom(Atom(
    atom_type="definition",
    name="dna_replication_fork",
    content=(
        "DNA replication proceeds bidirectionally from origins of "
        "replication. At each replication fork, helicase unwinds the "
        "double helix, primase synthesises RNA primers, DNA "
        "polymerase III extends in 5'->3' direction. The leading "
        "strand is synthesised continuously; the lagging strand "
        "is synthesised as Okazaki fragments."
    ),
    example=(
        "E. coli genome: 4.6 Mb, one origin, bidirectional. "
        "At 1000 nt/s per fork, replication time = "
        "4.6e6 / (2*1000) = 2300 s = 38.3 min."
    ),
    tier=4,
    domain="biology",
    source="Wikipedia contributors, 'DNA replication', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/DNA_replication",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="transcription_process",
    content=(
        "Transcription copies DNA to mRNA via RNA polymerase. "
        "Initiation: RNAP binds promoter (TATA box at -25). "
        "Elongation: RNAP reads template 3'->5', synthesises "
        "mRNA 5'->3'. Termination: at terminator sequence or "
        "rho-dependent mechanism. In eukaryotes, mRNA undergoes "
        "5' capping, 3' polyadenylation, and splicing."
    ),
    example=(
        "Template: 3'-TACGGC-5'. mRNA: 5'-AUGCCG-3'. "
        "Codons: AUG (Met), CCG (Pro). Protein: Met-Pro."
    ),
    tier=4,
    domain="biology",
    source="Wikipedia contributors, 'Transcription (biology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transcription_(biology)",
    prerequisites=["dna_replication_fork"],
))

register_atom(Atom(
    atom_type="definition",
    name="translation_elongation",
    content=(
        "Translation converts mRNA to protein at the ribosome. "
        "Initiation: small subunit binds mRNA at AUG start codon "
        "with Met-tRNA. Elongation: aminoacyl-tRNA enters A site, "
        "peptide bond forms, ribosome translocates. Termination: "
        "stop codon (UAA, UAG, UGA) triggers release factor binding."
    ),
    example=(
        "mRNA: AUG-GCU-UAC-UAA. Codons: AUG(Met), GCU(Ala), "
        "UAC(Tyr), UAA(Stop). Protein: Met-Ala-Tyr (3 amino acids)."
    ),
    tier=4,
    domain="biology",
    source="Wikipedia contributors, 'Translation (biology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Translation_(biology)",
    prerequisites=["transcription_process"],
))

register_atom(Atom(
    atom_type="formula",
    name="natural_selection_fitness",
    content=(
        "Fitness (w) measures reproductive success relative to the "
        "population. Selection coefficient s = 1 - w. "
        "Allele frequency change per generation under selection: "
        "dp/dt = s*p*q*(p*h + q*(1-h)) / w_bar, where h is "
        "dominance coefficient, p and q are allele frequencies, "
        "w_bar is mean fitness."
    ),
    example=(
        "p=0.4 (A), q=0.6 (a), w_AA=1.0, w_Aa=0.9, w_aa=0.7: "
        "w_bar = 0.16*1.0 + 0.48*0.9 + 0.36*0.7 = 0.16+0.432+0.252 "
        "= 0.844. Freq of A next gen: p' = (0.16*1.0 + 0.24*0.9)/0.844 "
        "= 0.376/0.844 = 0.4455"
    ),
    tier=5,
    domain="biology",
    source="Wikipedia contributors, 'Natural selection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Natural_selection",
    prerequisites=["hardy_weinberg"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="phylogenetic_parsimony",
    content=(
        "Maximum parsimony reconstructs phylogenetic trees by "
        "minimising the total number of character state changes. "
        "Fitch's algorithm: (1) assign character states to leaves, "
        "(2) at each internal node, take intersection of children's "
        "states (if non-empty) or union (counting one change). "
        "The tree requiring fewest changes is preferred."
    ),
    example=(
        "Species A=C, B=C, C=T, D=T. Tree ((A,B),(C,D)): "
        "Node AB = {C} (intersection), Node CD = {T} (intersection), "
        "Root = {C,T} (union, 1 change). Total = 1 change."
    ),
    tier=5,
    domain="biology",
    source="Wikipedia contributors, 'Maximum parsimony (phylogenetics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_parsimony_(phylogenetics)",
    prerequisites=["phylo_distance"],
))

register_atom(Atom(
    atom_type="definition",
    name="protein_structure",
    content=(
        "Protein structure has four levels: Primary (amino acid "
        "sequence), Secondary (alpha-helices and beta-sheets "
        "stabilised by hydrogen bonds), Tertiary (3D folding "
        "stabilised by hydrophobic interactions, disulfide bonds, "
        "ionic bonds), Quaternary (multiple polypeptide subunits)."
    ),
    example=(
        "Haemoglobin: quaternary structure with 4 subunits "
        "(2 alpha, 2 beta). Each subunit has 8 alpha-helices "
        "(secondary) folded into a globin fold (tertiary)."
    ),
    tier=4,
    domain="biology",
    source="Wikipedia contributors, 'Protein structure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Protein_structure",
    prerequisites=["amino_acid_property"],
))

register_atom(Atom(
    atom_type="formula",
    name="population_growth_rate",
    content=(
        "Intrinsic growth rate r = ln(R0)/T, where R0 is the net "
        "reproductive rate and T is generation time. Population "
        "size: N(t) = N0*e^(r*t) for exponential growth. "
        "Doubling time t_d = ln(2)/r."
    ),
    example=(
        "R0=4.0, T=2 years: r = ln(4)/2 = 1.386/2 = 0.693 yr^-1. "
        "Doubling time = ln(2)/0.693 = 1.0 year. "
        "N(5) = 100*e^(0.693*5) = 100*32 = 3200."
    ),
    tier=5,
    domain="biology",
    source="Wikipedia contributors, 'Population growth', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Population_growth",
    prerequisites=["logistic_growth"],
))

register_atom(Atom(
    atom_type="definition",
    name="immune_response",
    content=(
        "The adaptive immune response involves B cells (humoral "
        "immunity, producing antibodies) and T cells (cell-mediated "
        "immunity). Antibody binding affinity K_d = [Ab][Ag]/[AbAg]. "
        "Clonal selection: antigen-specific lymphocytes proliferate "
        "upon activation. Memory cells provide faster secondary response."
    ),
    example=(
        "Antibody with K_d = 1e-9 M, [Ag] = 1e-8 M: "
        "fraction bound = [Ag]/(K_d + [Ag]) = 1e-8/(1e-9 + 1e-8) "
        "= 1e-8/1.1e-8 = 0.909 (90.9% bound)"
    ),
    tier=4,
    domain="biology",
    source="Wikipedia contributors, 'Adaptive immune system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Adaptive_immune_system",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="allele_frequency_change",
    content=(
        "Under genetic drift, the variance in allele frequency "
        "change per generation is Var(dp) = p*q/(2*N_e), where "
        "p and q are allele frequencies and N_e is effective "
        "population size. Under selection: dp = s*p*q/(2*w_bar) "
        "for a haploid model."
    ),
    example=(
        "p=0.5, q=0.5, N_e=100: Var(dp) = 0.5*0.5/(2*100) = "
        "0.00125. SD = sqrt(0.00125) = 0.0354. Expected drift "
        "per generation is about 3.5% of allele frequency."
    ),
    tier=5,
    domain="biology",
    source="Wikipedia contributors, 'Genetic drift', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Genetic_drift",
    prerequisites=["hardy_weinberg"],
))

register_atom(Atom(
    atom_type="definition",
    name="genetic_code_redundancy",
    content=(
        "The genetic code maps 64 codons to 20 amino acids + 3 "
        "stop codons. Most amino acids are encoded by multiple "
        "codons (degeneracy). Leucine and serine each have 6 "
        "codons. Methionine and tryptophan have only 1 each. "
        "The wobble position (3rd base) allows flexibility."
    ),
    example=(
        "Leucine codons: UUA, UUG, CUU, CUC, CUA, CUG (6 total). "
        "Redundancy = 64/21 = 3.05 codons per assignment on average."
    ),
    tier=3,
    domain="biology",
    source="Wikipedia contributors, 'Genetic code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Genetic_code",
    prerequisites=["codon_translate"],
))
