"""Knowledge atoms for biochemistry, organic chemistry, and ecology.

Registers formula, rule, and model atoms covering enzyme kinetics,
molecular biology, organic reaction mechanisms, and population ecology.
Each atom stores the authoritative statement sourced from Wikipedia,
a worked example, tier, domain, source citation, and prerequisites.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Biochemistry (tier 3-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="rule",
    name="amino_acid_property",
    content=(
        "Amino acids are organic compounds containing an amino group "
        "(-NH2) and a carboxyl group (-COOH). The 20 standard amino "
        "acids are classified by their side chain (R group) properties: "
        "nonpolar/hydrophobic (Gly, Ala, Val, Leu, Ile, Pro, Phe, Met, "
        "Trp), polar/uncharged (Ser, Thr, Cys, Tyr, Asn, Gln), "
        "positively charged (Lys, Arg, His), and negatively charged "
        "(Asp, Glu). Each amino acid has a characteristic pKa, pI, "
        "molecular weight, and hydropathy index."
    ),
    example=(
        "Alanine (Ala, A): MW = 89.09 Da, pI = 6.00, "
        "side chain = -CH3 (nonpolar, hydrophobic)"
    ),
    tier=5,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Amino acid', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Amino_acid",
    prerequisites=["chemistry"],
))

register_atom(Atom(
    atom_type="formula",
    name="peptide_bond_count",
    content=(
        "A peptide bond is a covalent bond formed between the carboxyl "
        "group of one amino acid and the amino group of another through "
        "a condensation reaction releasing water. For a polypeptide "
        "chain of n amino acid residues, the number of peptide bonds "
        "is n - 1. The bond has partial double-bond character due to "
        "resonance, making it planar and rigid."
    ),
    example=(
        "A pentapeptide (5 amino acids): "
        "peptide bonds = 5 - 1 = 4"
    ),
    tier=3,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Peptide bond', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Peptide_bond",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="michaelis_menten",
    content=(
        "The Michaelis-Menten equation describes the rate of enzymatic "
        "reactions: v = V_max * [S] / (K_m + [S]), where v is the "
        "reaction rate, V_max is the maximum rate, [S] is the substrate "
        "concentration, and K_m is the Michaelis constant (the substrate "
        "concentration at which v = V_max / 2). The equation assumes "
        "steady-state kinetics and a single substrate."
    ),
    example=(
        "Given V_max = 100 umol/min, K_m = 5 mM, [S] = 10 mM: "
        "v = 100 * 10 / (5 + 10) = 1000 / 15 = 66.67 umol/min"
    ),
    tier=5,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Michaelis-Menten kinetics', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Michaelis%E2%80%93Menten_kinetics",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="lineweaver_burk",
    content=(
        "The Lineweaver-Burk plot is a double reciprocal plot of "
        "enzyme kinetics: 1/v = (K_m / V_max) * (1/[S]) + 1/V_max. "
        "It linearises the Michaelis-Menten equation, with slope = "
        "K_m / V_max, y-intercept = 1/V_max, and x-intercept = "
        "-1/K_m. Used to determine V_max and K_m from experimental "
        "data and to distinguish types of enzyme inhibition."
    ),
    example=(
        "Given V_max = 200 umol/min, K_m = 4 mM: "
        "slope = 4/200 = 0.02 min*mM/umol, "
        "y-intercept = 1/200 = 0.005 min/umol, "
        "x-intercept = -1/4 = -0.25 mM^{-1}"
    ),
    tier=5,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Lineweaver-Burk plot', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lineweaver%E2%80%93Burk_plot",
    prerequisites=["michaelis_menten", "linear_regression"],
))

register_atom(Atom(
    atom_type="rule",
    name="dna_complement",
    content=(
        "In DNA, bases pair according to Watson-Crick base pairing "
        "rules: adenine (A) pairs with thymine (T), and guanine (G) "
        "pairs with cytosine (C). The complementary strand runs in "
        "the antiparallel direction (5' to 3' paired with 3' to 5'). "
        "In RNA, thymine is replaced by uracil (U), so A pairs with U."
    ),
    example=(
        "DNA strand 5'-ATCGGA-3': "
        "complement = 3'-TAGCCT-5' (or written 5'-TCCGAT-3')"
    ),
    tier=3,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Base pair', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Base_pair",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="codon_translate",
    content=(
        "The genetic code maps three-nucleotide codons to amino acids. "
        "There are 64 possible codons (4^3), encoding 20 amino acids "
        "plus 3 stop codons (UAA, UAG, UGA). The code is degenerate "
        "(multiple codons per amino acid) but unambiguous (each codon "
        "encodes exactly one amino acid). AUG serves as both the start "
        "codon and encodes methionine."
    ),
    example=(
        "mRNA: AUG-GCU-UAC-UGA: "
        "Met-Ala-Tyr-Stop = tripeptide MAY"
    ),
    tier=4,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Genetic code', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Genetic_code",
    prerequisites=["dna_complement"],
))

register_atom(Atom(
    atom_type="formula",
    name="protein_mass",
    content=(
        "The molecular weight of a protein is approximately the sum "
        "of the molecular weights of its constituent amino acids, "
        "minus (n-1) * 18.015 Da for water molecules lost during "
        "peptide bond formation. Average amino acid MW is ~110 Da. "
        "For a protein of n residues: MW ~= sum(MW_i) - (n-1) * 18.015."
    ),
    example=(
        "Dipeptide Ala-Gly: MW = 89.09 + 75.03 - 18.015 = 146.105 Da"
    ),
    tier=4,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Protein', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Protein",
    prerequisites=["peptide_bond_count", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="enzyme_inhibition",
    content=(
        "Enzyme inhibition modifies the Michaelis-Menten equation: "
        "Competitive: v = V_max*[S] / (alpha*K_m + [S]), where "
        "alpha = 1 + [I]/K_i. Uncompetitive: v = V_max*[S] / "
        "(K_m + alpha'*[S]), where alpha' = 1 + [I]/K_i'. "
        "Mixed/noncompetitive: v = V_max*[S] / (alpha*K_m + alpha'*[S]). "
        "Competitive inhibitors raise apparent K_m; uncompetitive lower "
        "both apparent K_m and V_max."
    ),
    example=(
        "Competitive inhibition: V_max=100, K_m=5, [S]=10, [I]=5, K_i=5: "
        "alpha = 1 + 5/5 = 2, v = 100*10 / (2*5 + 10) = 1000/20 = 50"
    ),
    tier=6,
    domain="biochemistry",
    source=(
        "Wikipedia contributors, 'Enzyme inhibitor', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Enzyme_inhibitor",
    prerequisites=["michaelis_menten"],
))


# ---------------------------------------------------------------------------
# Organic Chemistry (tier 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="rule",
    name="iupac_naming",
    content=(
        "IUPAC nomenclature for organic compounds follows systematic "
        "rules: (1) identify the longest carbon chain (parent chain), "
        "(2) number carbons from the end nearest the first substituent, "
        "(3) name substituents with position numbers, (4) use prefixes "
        "di-, tri-, tetra- for multiple identical substituents, "
        "(5) list substituents alphabetically. Functional group suffixes: "
        "-ol (alcohol), -al (aldehyde), -one (ketone), -oic acid "
        "(carboxylic acid), -amine (amine)."
    ),
    example=(
        "CH3-CH(CH3)-CH2-CH3: parent chain = butane (4C), "
        "substituent = methyl at C2: 2-methylbutane"
    ),
    tier=4,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'IUPAC nomenclature of organic "
        "chemistry', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_organic_chemistry",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="functional_group_id",
    content=(
        "Functional groups are specific groupings of atoms that "
        "determine the chemical reactivity of a molecule. Key groups: "
        "hydroxyl (-OH, alcohols), carbonyl (C=O, aldehydes/ketones), "
        "carboxyl (-COOH, carboxylic acids), amino (-NH2, amines), "
        "ester (-COO-), amide (-CONH-), ether (-O-), thiol (-SH), "
        "nitro (-NO2), nitrile (-CN), phosphate (-PO4). Each group "
        "has characteristic chemical properties and reactivity."
    ),
    example=(
        "CH3CH2OH: contains hydroxyl group (-OH) -> alcohol. "
        "CH3COOH: contains carboxyl group (-COOH) -> carboxylic acid"
    ),
    tier=4,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Functional group', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Functional_group",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="degree_unsaturation",
    content=(
        "The degree of unsaturation (DoU), also called index of "
        "hydrogen deficiency (IHD), indicates the number of rings "
        "and/or double bonds in a molecule. For CnHmNpOqXr (X=halogen): "
        "DoU = (2n + 2 + p - r - m) / 2. Each double bond or ring "
        "contributes 1 DoU; a triple bond contributes 2. Oxygen and "
        "sulfur do not affect the calculation."
    ),
    example=(
        "Benzene C6H6: DoU = (2*6 + 2 - 6) / 2 = 8/2 = 4 "
        "(3 double bonds + 1 ring)"
    ),
    tier=4,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Degree of unsaturation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Degree_of_unsaturation",
    prerequisites=["addition", "division"],
))

register_atom(Atom(
    atom_type="rule",
    name="stereocenter_count",
    content=(
        "A stereocenter (chiral center) is a carbon atom bonded to "
        "four different substituents. The maximum number of "
        "stereoisomers is 2^n where n is the number of stereocenters. "
        "A meso compound has stereocenters but is achiral due to an "
        "internal plane of symmetry, reducing the actual number of "
        "stereoisomers. Stereocenters are labeled R or S using "
        "Cahn-Ingold-Prelog priority rules."
    ),
    example=(
        "2-bromobutane CH3-CHBr-CH2-CH3: C2 has four different "
        "groups (H, Br, CH3, CH2CH3) -> 1 stereocenter, "
        "2^1 = 2 stereoisomers (R and S)"
    ),
    tier=5,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Chirality (chemistry)', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Chirality_(chemistry)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="sn1_vs_sn2",
    content=(
        "SN1 and SN2 are nucleophilic substitution mechanisms. "
        "SN2: bimolecular, one-step, backside attack, inversion of "
        "configuration, favored by primary substrates, strong "
        "nucleophiles, polar aprotic solvents. Rate = k[substrate][Nu]. "
        "SN1: unimolecular, two-step (carbocation intermediate), "
        "racemisation, favored by tertiary substrates, weak "
        "nucleophiles, polar protic solvents. Rate = k[substrate]."
    ),
    example=(
        "CH3Br + NaOH -> CH3OH + NaBr: "
        "primary substrate + strong nucleophile -> SN2 mechanism"
    ),
    tier=5,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Nucleophilic substitution', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Nucleophilic_substitution",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="reaction_product",
    content=(
        "Predicting the product of an organic reaction requires "
        "identifying the reaction type (addition, elimination, "
        "substitution, rearrangement) and applying the appropriate "
        "rules: Markovnikov's rule for HX addition to alkenes (H adds "
        "to the less substituted carbon), Zaitsev's rule for "
        "elimination (more substituted alkene is major product), "
        "anti-Markovnikov for radical additions."
    ),
    example=(
        "CH2=CH-CH3 + HBr (no peroxides): Markovnikov addition, "
        "H to C1, Br to C2 -> CH3-CHBr-CH3 (2-bromopropane)"
    ),
    tier=6,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Markovnikov\\'s rule', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Markovnikov%27s_rule",
    prerequisites=["sn1_vs_sn2"],
))

register_atom(Atom(
    atom_type="definition",
    name="polymer_repeat_unit",
    content=(
        "A polymer is a macromolecule composed of repeating structural "
        "units (monomers) connected by covalent bonds. The repeat unit "
        "is the smallest structural fragment whose repetition generates "
        "the polymer. Addition polymers form by chain-growth (e.g., "
        "polyethylene from ethylene: -[CH2-CH2]n-). Condensation "
        "polymers form by step-growth with loss of small molecules "
        "(e.g., nylon from diamine + diacid)."
    ),
    example=(
        "Polypropylene: monomer = CH2=CH(CH3), "
        "repeat unit = -[CH2-CH(CH3)]-, n = degree of polymerisation"
    ),
    tier=5,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Polymer', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Polymer",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="isomer_count",
    content=(
        "Constitutional (structural) isomers have the same molecular "
        "formula but differ in the connectivity of atoms. The number "
        "of structural isomers grows rapidly with carbon count: "
        "C4H10 has 2 (butane, isobutane), C5H12 has 3, C6H14 has 5, "
        "C7H16 has 9, C10H22 has 75. Counting isomers of alkanes "
        "is equivalent to counting rooted trees (Cayley's formula), "
        "and there is no simple closed-form expression."
    ),
    example=(
        "C4H10 isomers: (1) n-butane CH3CH2CH2CH3, "
        "(2) isobutane (CH3)3CH -> 2 structural isomers"
    ),
    tier=5,
    domain="organic_chemistry",
    source=(
        "Wikipedia contributors, 'Structural isomer', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Structural_isomer",
    prerequisites=[],
))


# ---------------------------------------------------------------------------
# Ecology (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="logistic_growth",
    content=(
        "The logistic growth model describes population growth with a "
        "carrying capacity: dN/dt = r*N*(1 - N/K), where N is "
        "population size, r is the intrinsic growth rate, and K is "
        "the carrying capacity. The solution is the logistic function: "
        "N(t) = K / (1 + ((K - N0)/N0) * exp(-r*t)). Growth is "
        "exponential at low N, slows as N approaches K, and stabilises "
        "at K."
    ),
    example=(
        "Given N0=100, K=1000, r=0.5, t=5: "
        "N(5) = 1000 / (1 + (900/100)*exp(-2.5)) = "
        "1000 / (1 + 9*0.0821) = 1000 / 1.7389 = 575.1"
    ),
    tier=4,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Logistic function', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Logistic_function",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="lotka_volterra",
    content=(
        "The Lotka-Volterra equations model predator-prey dynamics: "
        "dx/dt = alpha*x - beta*x*y (prey), "
        "dy/dt = delta*x*y - gamma*y (predator), where x and y are "
        "prey and predator populations, alpha is prey growth rate, "
        "beta is predation rate, delta is predator reproduction rate "
        "per prey consumed, and gamma is predator death rate. The "
        "system produces oscillatory solutions."
    ),
    example=(
        "Given x=100, y=20, alpha=0.1, beta=0.01, delta=0.005, gamma=0.1: "
        "dx/dt = 0.1*100 - 0.01*100*20 = 10 - 20 = -10 (prey declining), "
        "dy/dt = 0.005*100*20 - 0.1*20 = 10 - 2 = 8 (predators growing)"
    ),
    tier=5,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Lotka-Volterra equations', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations",
    prerequisites=["logistic_growth"],
))

register_atom(Atom(
    atom_type="formula",
    name="population_doubling",
    content=(
        "The doubling time of a population with exponential growth "
        "N(t) = N0 * 2^(t/T_d) is T_d = ln(2)/r, where r is the "
        "growth rate. Equivalently, for continuous growth N(t) = "
        "N0 * exp(r*t), the doubling time is T_d = ln(2)/r = "
        "0.693/r. This applies to bacteria, investments, and any "
        "exponentially growing quantity."
    ),
    example=(
        "Given growth rate r = 0.05 per hour: "
        "T_d = ln(2)/0.05 = 0.693/0.05 = 13.86 hours"
    ),
    tier=5,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Doubling time', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Doubling_time",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="trophic_efficiency",
    content=(
        "Trophic efficiency is the percentage of energy transferred "
        "from one trophic level to the next: efficiency = "
        "(energy at level n+1 / energy at level n) * 100%. "
        "Typically about 10% (Lindeman's 10% rule). Energy is lost "
        "at each level through metabolism, heat, and waste. For a "
        "food chain with k levels, the energy available at the top "
        "is E_1 * (efficiency)^(k-1)."
    ),
    example=(
        "Primary producers: 10000 kcal, efficiency = 10%: "
        "primary consumers: 1000 kcal, "
        "secondary consumers: 100 kcal, "
        "tertiary consumers: 10 kcal"
    ),
    tier=4,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Trophic level', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Trophic_level",
    prerequisites=["percentage", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="species_diversity",
    content=(
        "The Shannon diversity index (H') quantifies species diversity: "
        "H' = -sum(p_i * ln(p_i)) for i = 1 to S, where p_i is the "
        "proportion of individuals belonging to species i, and S is "
        "the number of species. Higher H' indicates greater diversity. "
        "Maximum H' = ln(S) when all species are equally abundant. "
        "Simpson's index D = 1 - sum(p_i^2) is an alternative."
    ),
    example=(
        "Community with 3 species, proportions p = [0.5, 0.3, 0.2]: "
        "H' = -(0.5*ln(0.5) + 0.3*ln(0.3) + 0.2*ln(0.2)) = "
        "-(0.5*(-0.693) + 0.3*(-1.204) + 0.2*(-1.609)) = "
        "-((-0.347) + (-0.361) + (-0.322)) = 1.030"
    ),
    tier=5,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Shannon index', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Shannon_index",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="carrying_capacity",
    content=(
        "Carrying capacity (K) is the maximum population size that "
        "an environment can sustain indefinitely given available "
        "resources. In the logistic model, K determines the upper "
        "asymptote: dN/dt = r*N*(1 - N/K). When N < K, population "
        "grows; when N > K, population declines; when N = K, "
        "growth rate is zero. K can be estimated from data by "
        "fitting the logistic curve or from resource availability."
    ),
    example=(
        "Given dN/dt = 0 at N = 500: K = 500. "
        "At N = 250 with r = 0.1: dN/dt = 0.1*250*(1-250/500) = "
        "0.1*250*0.5 = 12.5 individuals per time unit"
    ),
    tier=5,
    domain="ecology",
    source=(
        "Wikipedia contributors, 'Carrying capacity', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Carrying_capacity",
    prerequisites=["logistic_growth"],
))
