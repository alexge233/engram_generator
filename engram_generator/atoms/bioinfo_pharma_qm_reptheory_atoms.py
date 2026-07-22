"""Knowledge atoms for bioinformatics, pharmacology, quantum mechanics,
and representation theory domains.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── BIOINFORMATICS ────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="sequence_alignment",
    content=(
        "Sequence alignment arranges DNA, RNA, or protein sequences to "
        "identify regions of similarity. The Needleman-Wunsch algorithm "
        "performs global alignment using dynamic programming with a scoring "
        "matrix S(i,j) = max(S(i-1,j-1)+s(a_i,b_j), S(i-1,j)+gap, "
        "S(i,j-1)+gap), where s is the substitution score and gap is the "
        "gap penalty."
    ),
    example=(
        "Sequences ACGT and AGGT, match=+1, mismatch=-1, gap=-2: "
        "S = [[0,-2,-4,-6],[-2,1,-1,-3],[-4,-1,0,-2],[-6,-3,0,-1],"
        "[-8,-5,-2,1]]. Score=1, alignment: A-CGT / A-GGT"
    ),
    tier=6,
    domain="bioinformatics",
    source="Wikipedia contributors, 'Needleman-Wunsch algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm",
    prerequisites=["edit_distance"],
))

register_atom(Atom(
    atom_type="formula",
    name="blast_evalue",
    content=(
        "The E-value in BLAST estimates the number of alignments with a "
        "score >= S expected by chance. E = K*m*n*exp(-lambda*S), where K "
        "and lambda are statistical parameters, m is the query length, "
        "and n is the database size. Lower E-values indicate more "
        "significant matches."
    ),
    example=(
        "K=0.041, lambda=0.267, m=200, n=1e8, S=50: "
        "E = 0.041 * 200 * 1e8 * exp(-0.267*50) = 8.2e5 * exp(-13.35) "
        "= 8.2e5 * 1.6e-6 = 1.31"
    ),
    tier=5,
    domain="bioinformatics",
    source="Wikipedia contributors, 'BLAST (biotechnology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/BLAST_(biotechnology)",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="phylo_distance",
    content=(
        "Phylogenetic distance estimates evolutionary divergence between "
        "sequences. The Jukes-Cantor model gives d = -3/4 * ln(1 - 4p/3), "
        "where p is the proportion of differing sites. This corrects for "
        "multiple substitutions at the same site."
    ),
    example=(
        "Two sequences of length 100 with 20 differences: p = 0.2, "
        "d = -0.75 * ln(1 - 4*0.2/3) = -0.75 * ln(0.7333) = "
        "-0.75 * (-0.3101) = 0.2326"
    ),
    tier=5,
    domain="bioinformatics",
    source="Wikipedia contributors, 'Models of DNA evolution', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Models_of_DNA_evolution",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="gc_content",
    content=(
        "GC content is the percentage of guanine (G) and cytosine (C) "
        "bases in a DNA or RNA sequence. GC% = (G + C) / (A + T + G + C) "
        "* 100. GC content affects melting temperature and is used to "
        "characterise genomes."
    ),
    example=(
        "Sequence ATGCGCTA: G=2, C=2, A=2, T=2. "
        "GC% = (2+2)/(2+2+2+2) * 100 = 4/8 * 100 = 50%"
    ),
    tier=4,
    domain="bioinformatics",
    source="Wikipedia contributors, 'GC-content', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/GC-content",
    prerequisites=["percentage"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="open_reading_frame",
    content=(
        "An open reading frame (ORF) is a sequence of DNA that begins "
        "with a start codon (ATG) and ends with a stop codon (TAA, TAG, "
        "or TGA). Finding ORFs involves scanning all three reading frames "
        "in both directions. The longest ORF often encodes the protein."
    ),
    example=(
        "Sequence ATGAAACCCTAGGGG: reading frame 1: "
        "ATG-AAA-CCC-TAG -> ORF from pos 0 to 11, length 4 codons, "
        "encodes Met-Lys-Pro-STOP"
    ),
    tier=5,
    domain="bioinformatics",
    source="Wikipedia contributors, 'Open reading frame', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Open_reading_frame",
    prerequisites=["string_reverse"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="restriction_digest",
    content=(
        "Restriction enzymes cut DNA at specific recognition sequences. "
        "A restriction digest predicts fragment sizes by finding all "
        "cut sites in a sequence. EcoRI recognises GAATTC, BamHI "
        "recognises GGATCC. Fragment sizes are the distances between "
        "consecutive cut sites."
    ),
    example=(
        "Circular plasmid 5000 bp with EcoRI sites at positions 500 "
        "and 2000: fragments are 2000-500=1500 bp and 5000-2000+500="
        "3500 bp"
    ),
    tier=4,
    domain="bioinformatics",
    source="Wikipedia contributors, 'Restriction enzyme', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Restriction_enzyme",
    prerequisites=["subtraction"],
))

# ── PHARMACOLOGY ──────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="half_life_drug",
    content=(
        "The elimination half-life of a drug is the time required for "
        "the plasma concentration to decrease by half. t_1/2 = ln(2)/k_e "
        "= 0.693/k_e, where k_e is the elimination rate constant. After "
        "n half-lives, the fraction remaining is (1/2)^n."
    ),
    example=(
        "k_e = 0.1 hr^-1: t_1/2 = 0.693/0.1 = 6.93 hours. "
        "After 3 half-lives: remaining = (0.5)^3 = 12.5%"
    ),
    tier=5,
    domain="pharmacology",
    source="Wikipedia contributors, 'Biological half-life', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Biological_half-life",
    prerequisites=["logarithm", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="dose_response",
    content=(
        "The Hill equation models the dose-response relationship: "
        "E = E_max * C^n / (EC50^n + C^n), where E is the effect, "
        "E_max is the maximal effect, C is the drug concentration, "
        "EC50 is the concentration producing 50% of E_max, and n is "
        "the Hill coefficient."
    ),
    example=(
        "E_max=100, EC50=10 uM, n=2, C=20 uM: "
        "E = 100 * 400 / (100 + 400) = 40000/500 = 80"
    ),
    tier=5,
    domain="pharmacology",
    source="Wikipedia contributors, 'Hill equation (biochemistry)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="bioavailability",
    content=(
        "Bioavailability (F) is the fraction of an administered dose "
        "that reaches systemic circulation. F = (AUC_oral / AUC_iv) * "
        "(Dose_iv / Dose_oral), where AUC is the area under the "
        "plasma concentration-time curve."
    ),
    example=(
        "AUC_oral=80, AUC_iv=100, Dose_iv=50mg, Dose_oral=100mg: "
        "F = (80/100) * (50/100) = 0.8 * 0.5 = 0.4 (40%)"
    ),
    tier=5,
    domain="pharmacology",
    source="Wikipedia contributors, 'Bioavailability', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Bioavailability",
    prerequisites=["percentage"],
))

register_atom(Atom(
    atom_type="formula",
    name="clearance_rate",
    content=(
        "Clearance (CL) is the volume of plasma from which a drug is "
        "completely removed per unit time. CL = Dose / AUC for IV "
        "bolus, or CL = k_e * V_d, where k_e is the elimination rate "
        "constant and V_d is the volume of distribution."
    ),
    example=(
        "Dose=500mg IV, AUC=50 mg*hr/L: CL = 500/50 = 10 L/hr. "
        "If V_d = 100L: k_e = CL/V_d = 10/100 = 0.1 hr^-1"
    ),
    tier=5,
    domain="pharmacology",
    source="Wikipedia contributors, 'Clearance (pharmacology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Clearance_(pharmacology)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="steady_state",
    content=(
        "Steady state is reached when the rate of drug administration "
        "equals the rate of elimination. C_ss = (F * Dose) / (CL * tau), "
        "where tau is the dosing interval. Steady state is reached after "
        "approximately 4-5 half-lives."
    ),
    example=(
        "F=0.8, Dose=200mg, CL=10 L/hr, tau=8hr: "
        "C_ss = (0.8*200)/(10*8) = 160/80 = 2.0 mg/L"
    ),
    tier=5,
    domain="pharmacology",
    source="Wikipedia contributors, 'Steady state (pharmacology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Pharmacokinetics#Steady-state",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="therapeutic_index",
    content=(
        "The therapeutic index (TI) is the ratio of the toxic dose to "
        "the therapeutic dose. TI = TD50 / ED50, where TD50 is the dose "
        "causing toxicity in 50% of the population and ED50 is the dose "
        "effective in 50%. A higher TI indicates a wider margin of safety."
    ),
    example=(
        "TD50=500mg, ED50=50mg: TI = 500/50 = 10. "
        "This drug has a wide safety margin."
    ),
    tier=4,
    domain="pharmacology",
    source="Wikipedia contributors, 'Therapeutic index', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Therapeutic_index",
    prerequisites=["division"],
))

# ── QUANTUM MECHANICS ─────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="schrodinger_1d",
    content=(
        "The time-independent Schrodinger equation in one dimension: "
        "-hbar^2/(2m) * d^2psi/dx^2 + V(x)*psi = E*psi. For the "
        "infinite square well of width L, the energy eigenvalues are "
        "E_n = n^2 * pi^2 * hbar^2 / (2*m*L^2) and the wavefunctions "
        "are psi_n(x) = sqrt(2/L) * sin(n*pi*x/L)."
    ),
    example=(
        "Infinite well, L=1nm, n=1, m=m_e=9.109e-31 kg: "
        "E_1 = pi^2 * (1.055e-34)^2 / (2 * 9.109e-31 * (1e-9)^2) "
        "= 6.024e-20 J = 0.376 eV"
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Particle in a box', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Particle_in_a_box",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="principle",
    name="uncertainty_compute",
    content=(
        "Heisenberg's uncertainty principle states that the product of "
        "uncertainties in position and momentum satisfies "
        "Delta_x * Delta_p >= hbar/2, where hbar = h/(2*pi) = "
        "1.0546e-34 J*s. Similarly, Delta_E * Delta_t >= hbar/2."
    ),
    example=(
        "Delta_x = 1e-10 m (one angstrom): "
        "Delta_p >= hbar/(2*Delta_x) = 1.055e-34/(2e-10) = "
        "5.27e-25 kg*m/s"
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Uncertainty principle', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Uncertainty_principle",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="commutator_compute",
    content=(
        "The commutator of two operators A and B is [A, B] = AB - BA. "
        "The canonical commutation relation is [x, p] = i*hbar. "
        "Commutators determine whether observables can be simultaneously "
        "measured: [A,B]=0 implies compatible observables."
    ),
    example=(
        "[x, p] = xp - px = i*hbar. For angular momentum: "
        "[L_x, L_y] = i*hbar*L_z. For matrices A=[[0,1],[0,0]], "
        "B=[[0,0],[1,0]]: [A,B] = AB-BA = [[1,0],[0,-1]]"
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Commutator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Commutator",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="angular_momentum_qn",
    content=(
        "Orbital angular momentum quantum numbers: l = 0,1,...,n-1 "
        "determines the subshell (s,p,d,f), and m_l = -l,...,+l "
        "determines the orientation. The magnitude is L = hbar*sqrt(l(l+1)) "
        "and the z-component is L_z = m_l*hbar."
    ),
    example=(
        "n=3, l=2 (d orbital): m_l can be -2,-1,0,1,2 (5 values). "
        "L = hbar*sqrt(2*3) = hbar*sqrt(6) = 2.583*hbar"
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Angular momentum quantum number', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Azimuthal_quantum_number",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="spin_addition",
    content=(
        "When adding two angular momenta j_1 and j_2, the total angular "
        "momentum J ranges from |j_1 - j_2| to j_1 + j_2 in integer "
        "steps. The total number of states is (2*j_1+1)*(2*j_2+1). "
        "Clebsch-Gordan coefficients determine the coupling."
    ),
    example=(
        "Two spin-1/2 particles: j_1=1/2, j_2=1/2. "
        "J ranges from 0 to 1. States: (2*0.5+1)*(2*0.5+1) = 4. "
        "J=1 (triplet, 3 states) + J=0 (singlet, 1 state) = 4 total"
    ),
    tier=6,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Angular momentum coupling', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Angular_momentum_coupling",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="hydrogen_energy",
    content=(
        "The energy levels of the hydrogen atom are E_n = -13.6 eV / n^2, "
        "where n is the principal quantum number. The wavelength of a "
        "photon emitted in a transition is given by the Rydberg formula: "
        "1/lambda = R_H * (1/n_f^2 - 1/n_i^2), where R_H = 1.097e7 m^-1."
    ),
    example=(
        "Transition n=3 to n=2 (Balmer H-alpha): "
        "1/lambda = 1.097e7 * (1/4 - 1/9) = 1.097e7 * 5/36 "
        "= 1.524e6 m^-1, lambda = 656.3 nm (red)"
    ),
    tier=5,
    domain="quantum_mechanics",
    source="Wikipedia contributors, 'Hydrogen atom', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hydrogen_atom",
    prerequisites=["exponentiation"],
))

# ── REPRESENTATION THEORY ─────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="character_compute",
    content=(
        "The character of a representation rho is the function "
        "chi(g) = Tr(rho(g)), the trace of the representation matrix "
        "for group element g. Characters are class functions: they are "
        "constant on conjugacy classes."
    ),
    example=(
        "S_3 standard representation, identity e: rho(e) = I_2, "
        "chi(e) = Tr(I_2) = 2. For (12): rho((12)) = [[0,1],[1,0]], "
        "chi((12)) = 0"
    ),
    tier=6,
    domain="representation_theory",
    source="Wikipedia contributors, 'Character theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Character_theory",
    prerequisites=["matrix_trace"],
))

register_atom(Atom(
    atom_type="definition",
    name="character_table",
    content=(
        "A character table lists the characters of all irreducible "
        "representations of a finite group, organised by conjugacy "
        "classes. Rows are irreducible representations, columns are "
        "conjugacy classes. The orthogonality relations state "
        "sum_g chi_i(g)*chi_j(g)* = |G|*delta_ij."
    ),
    example=(
        "Z_3 = {e, r, r^2} character table: "
        "chi_0 = [1, 1, 1], chi_1 = [1, omega, omega^2], "
        "chi_2 = [1, omega^2, omega], where omega = e^(2pi*i/3)"
    ),
    tier=7,
    domain="representation_theory",
    source="Wikipedia contributors, 'Character table', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Character_table",
    prerequisites=["character_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="irreducible_check",
    content=(
        "A representation is irreducible if and only if "
        "(1/|G|) * sum_g |chi(g)|^2 = 1, where chi is the character. "
        "If this sum equals an integer k > 1, the representation "
        "decomposes into k irreducible components."
    ),
    example=(
        "S_3, chi = [2, 0, -1] on classes {e}, {(12),(13),(23)}, "
        "{(123),(132)}: (1/6)*(4 + 3*0 + 2*1) = 6/6 = 1, "
        "so this representation is irreducible"
    ),
    tier=7,
    domain="representation_theory",
    source="Wikipedia contributors, 'Character theory', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Character_theory",
    prerequisites=["character_compute"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="decompose_rep",
    content=(
        "To decompose a representation into irreducibles, compute "
        "the multiplicity of each irreducible chi_i: "
        "n_i = (1/|G|) * sum_g chi(g) * chi_i(g)*. The representation "
        "then decomposes as direct_sum n_i * V_i."
    ),
    example=(
        "S_3, regular representation chi_reg = [6,0,0]: "
        "n_trivial = (1/6)(6*1 + 0 + 0) = 1, "
        "n_sign = (1/6)(6*1 + 0 + 0) = 1, "
        "n_standard = (1/6)(6*2 + 0 + 0) = 2. "
        "Check: 1+1+2*2 = 6 = |S_3|"
    ),
    tier=7,
    domain="representation_theory",
    source="Wikipedia contributors, 'Representation theory of finite groups', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Representation_theory_of_finite_groups",
    prerequisites=["character_table"],
))

register_atom(Atom(
    atom_type="formula",
    name="tensor_rep",
    content=(
        "The tensor product of representations rho_1 and rho_2 is "
        "(rho_1 tensor rho_2)(g) = rho_1(g) tensor rho_2(g). "
        "The character of the tensor product is chi_{1 tensor 2}(g) = "
        "chi_1(g) * chi_2(g) (pointwise multiplication)."
    ),
    example=(
        "S_3: chi_sign = [1,-1,1], chi_standard = [2,0,-1]. "
        "chi_tensor = [1*2, (-1)*0, 1*(-1)] = [2, 0, -1]. "
        "This equals chi_standard, so sign tensor standard = standard"
    ),
    tier=7,
    domain="representation_theory",
    source="Wikipedia contributors, 'Tensor product of representations', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Tensor_product_of_representations",
    prerequisites=["tensor_product"],
))

register_atom(Atom(
    atom_type="theorem",
    name="schur_lemma_apply",
    content=(
        "Schur's lemma: if rho_1 and rho_2 are irreducible "
        "representations, any intertwining map phi: V_1 -> V_2 is "
        "either zero or an isomorphism. Over C, any intertwiner "
        "of an irreducible representation with itself is a scalar "
        "multiple of the identity."
    ),
    example=(
        "V irreducible, T: V->V intertwines with rho. "
        "By Schur's lemma, T = lambda*I for some lambda in C. "
        "If V is the standard rep of S_3 and T commutes with all "
        "rho(g), then T = lambda*I_2"
    ),
    tier=7,
    domain="representation_theory",
    source="Wikipedia contributors, 'Schur's lemma', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Schur%27s_lemma",
    prerequisites=["irreducible_check"],
))
