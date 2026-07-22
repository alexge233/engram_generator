"""Knowledge atoms for ecology ext, genetics ext, and biochemistry ext.

Registers formula and model atoms covering competition dynamics,
island biogeography, population genetics, enzyme kinetics,
and metabolic thermodynamics. Each atom stores the authoritative
statement sourced from Wikipedia, worked example, tier, domain,
source citation, source URL, and prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# -----------------------------------------------------------------------
# Ecology ext (tier 4-5)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="competition_model",
    content=(
        "The Lotka-Volterra competition model describes two species "
        "competing for the same resource: dN1/dt = r1*N1*(K1-N1-a12*N2)/K1 "
        "and dN2/dt = r2*N2*(K2-N2-a21*N1)/K2, where N1, N2 are population "
        "sizes, r1, r2 are intrinsic growth rates, K1, K2 are carrying "
        "capacities, and a12, a21 are competition coefficients measuring "
        "the effect of one species on the other."
    ),
    example=(
        "Given N1=50, N2=30, r1=0.5, r2=0.3, K1=200, K2=150, a12=0.8, "
        "a21=0.6: dN1/dt = 0.5*50*(200-50-0.8*30)/200 = 0.5*50*126/200 "
        "= 15.75"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'Competitive Lotka-Volterra equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations",
    prerequisites=["logistic_growth"],
))

register_atom(Atom(
    atom_type="formula",
    name="predator_functional_response",
    content=(
        "Holling's Type II functional response describes the rate at which "
        "a predator captures prey as a function of prey density: "
        "f(N) = a*N / (1 + a*h*N), where a is the attack rate, h is the "
        "handling time per prey item, and N is prey density. At high prey "
        "density, the response saturates at 1/h."
    ),
    example=(
        "Given a=0.5, h=0.1, N=20: f(N) = 0.5*20 / (1 + 0.5*0.1*20) "
        "= 10 / (1 + 1) = 10/2 = 5 prey per predator per unit time"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'Functional response', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Functional_response",
    prerequisites=["lotka_volterra"],
))

register_atom(Atom(
    atom_type="formula",
    name="island_biogeography",
    content=(
        "The theory of island biogeography (MacArthur and Wilson, 1967) "
        "predicts that the equilibrium number of species on an island "
        "is determined by the balance between immigration and extinction "
        "rates: S_eq occurs where I(S) = E(S). Immigration rate decreases "
        "with distance from the mainland and with species number; "
        "extinction rate increases with decreasing island area."
    ),
    example=(
        "Given I(S) = I_max*(1-S/P) and E(S) = E_max*S/P with I_max=10, "
        "E_max=5, P=100: at equilibrium I=E, 10*(1-S/100)=5*S/100, "
        "1000-10S=5S, S_eq=1000/15=66.67, so ~67 species"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'The Theory of Island Biogeography', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/The_Theory_of_Island_Biogeography",
    prerequisites=["population_doubling"],
))

register_atom(Atom(
    atom_type="formula",
    name="life_history_table",
    content=(
        "A life table summarises the mortality and survival of a cohort. "
        "Key columns: x (age class), n_x (survivors), d_x (deaths), "
        "q_x = d_x/n_x (mortality rate), l_x = n_x/n_0 (survivorship), "
        "e_x = T_x/n_x (life expectancy). Net reproductive rate "
        "R_0 = sum(l_x * m_x) where m_x is fecundity at age x."
    ),
    example=(
        "Given l_0=1.0, l_1=0.8, l_2=0.5, l_3=0.1, m_0=0, m_1=2, "
        "m_2=3, m_3=1: R_0 = 0*1.0 + 2*0.8 + 3*0.5 + 1*0.1 = 3.2"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'Life table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Life_table",
    prerequisites=["logistic_growth"],
))

register_atom(Atom(
    atom_type="definition",
    name="succession_model",
    content=(
        "Ecological succession is the process of change in the species "
        "structure of an ecological community over time. Primary succession "
        "occurs on bare substrate (lava, rock); secondary succession "
        "follows disturbance (fire, logging). The Markov chain model "
        "assigns transition probabilities between community states."
    ),
    example=(
        "Given 3 states (pioneer, intermediate, climax) with transition "
        "matrix P=[[0.3,0.5,0.2],[0,0.4,0.6],[0,0,1]]: starting from "
        "pioneer, after 1 step: P(intermediate)=0.5, P(climax)=0.2"
    ),
    tier=4,
    domain="ecology",
    source="Wikipedia contributors, 'Ecological succession', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ecological_succession",
    prerequisites=["markov_chain"],
))

register_atom(Atom(
    atom_type="formula",
    name="metapopulation",
    content=(
        "Levins' metapopulation model describes the fraction of occupied "
        "patches: dp/dt = c*p*(1-p) - e*p, where p is the fraction of "
        "occupied patches, c is the colonisation rate, and e is the local "
        "extinction rate. At equilibrium, p* = 1 - e/c (provided c > e)."
    ),
    example=(
        "Given c=0.4, e=0.1: p* = 1 - 0.1/0.4 = 1 - 0.25 = 0.75, "
        "so 75% of patches are occupied at equilibrium"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'Metapopulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Metapopulation",
    prerequisites=["logistic_growth"],
))

register_atom(Atom(
    atom_type="formula",
    name="nutrient_cycling",
    content=(
        "Nutrient cycling models track the flow of elements (C, N, P) "
        "through ecosystem compartments. A simple two-box model: "
        "dA/dt = input - k1*A + k2*B and dB/dt = k1*A - k2*B - loss, "
        "where A is the available pool, B is the bound pool, k1 is the "
        "uptake rate, and k2 is the release rate."
    ),
    example=(
        "Given A=100, B=50, input=10, k1=0.3, k2=0.1, loss=0.05: "
        "dA/dt = 10 - 0.3*100 + 0.1*50 = 10 - 30 + 5 = -15, "
        "dB/dt = 0.3*100 - 0.1*50 - 0.05*50 = 30 - 5 - 2.5 = 22.5"
    ),
    tier=4,
    domain="ecology",
    source="Wikipedia contributors, 'Nutrient cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nutrient_cycle",
    prerequisites=["trophic_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="biodiversity_index",
    content=(
        "The Shannon diversity index measures species diversity: "
        "H' = -sum(p_i * ln(p_i)), where p_i is the proportion of "
        "individuals belonging to species i. Higher values indicate "
        "greater diversity. Simpson's index D = 1 - sum(p_i^2) is "
        "an alternative that gives the probability that two randomly "
        "chosen individuals belong to different species."
    ),
    example=(
        "Given 3 species with abundances 50, 30, 20 (total 100): "
        "p = [0.5, 0.3, 0.2], H' = -(0.5*ln(0.5) + 0.3*ln(0.3) "
        "+ 0.2*ln(0.2)) = -(−0.3466 − 0.3612 − 0.3219) = 1.0297"
    ),
    tier=5,
    domain="ecology",
    source="Wikipedia contributors, 'Shannon index', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shannon_index",
    prerequisites=["species_diversity"],
))


# -----------------------------------------------------------------------
# Genetics ext (tier 5-6)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="epistasis",
    content=(
        "Epistasis occurs when the effect of one gene depends on the "
        "presence of one or more modifier genes. In a dihybrid cross "
        "with epistasis, the classic 9:3:3:1 ratio is modified. "
        "Recessive epistasis gives 9:3:4, dominant epistasis gives "
        "12:3:1, and duplicate recessive epistasis gives 9:7."
    ),
    example=(
        "Recessive epistasis (coat colour): AaBb x AaBb, gene B "
        "epistatic when homozygous recessive. F2 ratio: 9 A_B_ "
        "(colour 1) : 3 A_bb (colour 2) : 4 aaB_ + aabb (colour 3) = 9:3:4"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Epistasis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Epistasis",
    prerequisites=["dihybrid_cross"],
))

register_atom(Atom(
    atom_type="formula",
    name="genetic_drift",
    content=(
        "Genetic drift is the change in allele frequency due to random "
        "sampling in finite populations. The probability that an allele "
        "becomes fixed is equal to its initial frequency p. The expected "
        "heterozygosity after t generations: H_t = H_0 * (1 - 1/(2N))^t, "
        "where N is the effective population size."
    ),
    example=(
        "Given H_0=0.5, N=100, t=50: H_50 = 0.5 * (1 - 1/200)^50 "
        "= 0.5 * 0.995^50 = 0.5 * 0.7783 = 0.3892"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Genetic drift', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Genetic_drift",
    prerequisites=["hardy_weinberg"],
))

register_atom(Atom(
    atom_type="formula",
    name="mutation_selection",
    content=(
        "Mutation-selection balance determines the equilibrium frequency "
        "of a deleterious allele: q* = mu/s for a fully dominant "
        "deleterious allele, and q* = sqrt(mu/s) for a fully recessive "
        "one, where mu is the mutation rate and s is the selection "
        "coefficient against the allele."
    ),
    example=(
        "Given mu=1e-5, s=0.01 (recessive): q* = sqrt(1e-5 / 0.01) "
        "= sqrt(0.001) = 0.0316"
    ),
    tier=6,
    domain="genetics",
    source="Wikipedia contributors, 'Mutation-selection balance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mutation%E2%80%93selection_balance",
    prerequisites=["hardy_weinberg"],
))

register_atom(Atom(
    atom_type="formula",
    name="linkage_disequilibrium",
    content=(
        "Linkage disequilibrium (LD) measures the non-random association "
        "of alleles at two loci: D = f(AB) - f(A)*f(B), where f(AB) "
        "is the frequency of the AB haplotype, and f(A), f(B) are "
        "allele frequencies. D decays over generations: D_t = D_0*(1-r)^t, "
        "where r is the recombination fraction."
    ),
    example=(
        "Given f(AB)=0.4, f(A)=0.6, f(B)=0.5: D = 0.4 - 0.6*0.5 "
        "= 0.4 - 0.3 = 0.1. After 10 generations with r=0.1: "
        "D_10 = 0.1*(1-0.1)^10 = 0.1*0.3487 = 0.0349"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Linkage disequilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linkage_disequilibrium",
    prerequisites=["linked_genes"],
))

register_atom(Atom(
    atom_type="formula",
    name="coalescent_time",
    content=(
        "Coalescent theory traces gene lineages backwards in time. The "
        "expected time for k lineages to coalesce to k-1 is "
        "E[T_k] = 4N / (k*(k-1)), where N is the effective population "
        "size. The total expected time to the most recent common ancestor "
        "for a sample of n: E[T_MRCA] = 4N*(1 - 1/n)."
    ),
    example=(
        "Given N=1000, n=5: E[T_MRCA] = 4*1000*(1 - 1/5) = 4000*0.8 "
        "= 3200 generations. E[T_5] = 4000/(5*4) = 200 generations"
    ),
    tier=6,
    domain="genetics",
    source="Wikipedia contributors, 'Coalescent theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coalescent_theory",
    prerequisites=["genetic_drift"],
))

register_atom(Atom(
    atom_type="formula",
    name="quantitative_trait",
    content=(
        "Quantitative genetics decomposes phenotypic variance: "
        "V_P = V_G + V_E, where V_G is genetic variance and V_E is "
        "environmental variance. Heritability h^2 = V_G/V_P gives the "
        "proportion of phenotypic variation due to genetics. The breeder's "
        "equation predicts response to selection: R = h^2 * S, where S "
        "is the selection differential."
    ),
    example=(
        "Given V_P=10, V_G=6, selection differential S=2: "
        "h^2 = 6/10 = 0.6, R = 0.6*2 = 1.2 units shift in mean"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Heritability', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heritability",
    prerequisites=["hardy_weinberg"],
))

register_atom(Atom(
    atom_type="formula",
    name="population_bottleneck",
    content=(
        "A population bottleneck drastically reduces genetic diversity. "
        "The expected heterozygosity after a bottleneck of size N_b for "
        "one generation followed by recovery: H_after = H_before * "
        "(1 - 1/(2*N_b)). The effective population size over t "
        "generations with varying sizes is the harmonic mean: "
        "1/N_e = (1/t) * sum(1/N_i)."
    ),
    example=(
        "Given H_before=0.8, bottleneck N_b=10: H_after = 0.8 * "
        "(1 - 1/20) = 0.8 * 0.95 = 0.76. Lost 5% of heterozygosity"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Population bottleneck', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Population_bottleneck",
    prerequisites=["genetic_drift"],
))

register_atom(Atom(
    atom_type="formula",
    name="inbreeding_coefficient",
    content=(
        "Wright's inbreeding coefficient F measures the probability "
        "that two alleles at a locus in an individual are identical by "
        "descent. For a diploid with inbreeding: f(AA) = p^2 + F*p*q, "
        "f(Aa) = 2*p*q*(1-F), f(aa) = q^2 + F*p*q. F ranges from 0 "
        "(random mating) to 1 (complete inbreeding)."
    ),
    example=(
        "Given p=0.6, q=0.4, F=0.25: f(AA) = 0.36 + 0.25*0.24 = 0.42, "
        "f(Aa) = 0.48*(1-0.25) = 0.36, f(aa) = 0.16 + 0.06 = 0.22"
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Coefficient of inbreeding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coefficient_of_inbreeding",
    prerequisites=["hardy_weinberg"],
))


# -----------------------------------------------------------------------
# Biochemistry ext (tier 5-6)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="allosteric_regulation",
    content=(
        "Allosteric regulation modifies enzyme activity by binding of "
        "an effector molecule at a site other than the active site. The "
        "Monod-Wyman-Changeux (MWC) model describes cooperative binding: "
        "Y = L*c*alpha*(1+c*alpha)^(n-1) + alpha*(1+alpha)^(n-1) / "
        "[L*(1+c*alpha)^n + (1+alpha)^n], where L is the allosteric "
        "constant, c = K_R/K_T, and alpha = [S]/K_R."
    ),
    example=(
        "Hill equation approximation: Y = [S]^n / (K_0.5^n + [S]^n). "
        "Given [S]=5, K_0.5=4, n=2: Y = 25/(16+25) = 25/41 = 0.6098"
    ),
    tier=6,
    domain="biochemistry",
    source="Wikipedia contributors, 'Allosteric regulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Allosteric_regulation",
    prerequisites=["michaelis_menten"],
))

register_atom(Atom(
    atom_type="formula",
    name="enzyme_kinetics_inhibition_ext",
    content=(
        "Enzyme inhibition modifies Michaelis-Menten kinetics. "
        "Competitive: v = V_max*[S] / (K_m*(1+[I]/K_i) + [S]). "
        "Uncompetitive: v = V_max*[S] / (K_m + [S]*(1+[I]/K_i)). "
        "Mixed/noncompetitive: v = V_max*[S] / (K_m*(1+[I]/K_i) "
        "+ [S]*(1+[I]/K_i'))."
    ),
    example=(
        "Competitive inhibition: V_max=100, K_m=5, [S]=10, [I]=2, "
        "K_i=4: v = 100*10 / (5*(1+2/4) + 10) = 1000 / (5*1.5 + 10) "
        "= 1000/17.5 = 57.14"
    ),
    tier=6,
    domain="biochemistry",
    source="Wikipedia contributors, 'Enzyme inhibitor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Enzyme_inhibitor",
    prerequisites=["michaelis_menten"],
))

register_atom(Atom(
    atom_type="formula",
    name="henderson_hasselbalch",
    content=(
        "The Henderson-Hasselbalch equation relates the pH of a buffer "
        "solution to the pKa and the ratio of conjugate base to acid: "
        "pH = pKa + log10([A-]/[HA]). It is derived from the acid "
        "dissociation equilibrium Ka = [H+][A-]/[HA]."
    ),
    example=(
        "Given pKa=4.76 (acetic acid), [A-]=0.1 M, [HA]=0.05 M: "
        "pH = 4.76 + log10(0.1/0.05) = 4.76 + log10(2) = 4.76 + 0.301 "
        "= 5.061"
    ),
    tier=5,
    domain="biochemistry",
    source="Wikipedia contributors, 'Henderson-Hasselbalch equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Henderson%E2%80%93Hasselbalch_equation",
    prerequisites=["ph_calculation"],
))

register_atom(Atom(
    atom_type="formula",
    name="gibbs_free_energy_biochem",
    content=(
        "The Gibbs free energy change determines reaction spontaneity: "
        "dG = dG0' + R*T*ln(Q), where dG0' is the standard free energy "
        "change at pH 7, R = 8.314 J/(mol*K), T is temperature in K, "
        "and Q is the reaction quotient [products]/[reactants]. "
        "A reaction is spontaneous when dG < 0."
    ),
    example=(
        "ATP hydrolysis: dG0' = -30.5 kJ/mol, T=310K, Q=1 (standard): "
        "dG = -30.5 + 8.314e-3*310*ln(1) = -30.5 + 0 = -30.5 kJ/mol"
    ),
    tier=5,
    domain="biochemistry",
    source="Wikipedia contributors, 'Gibbs free energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gibbs_free_energy",
    prerequisites=["gibbs_spontaneity"],
))

register_atom(Atom(
    atom_type="formula",
    name="metabolic_pathway_energy",
    content=(
        "Metabolic pathway energetics sums the free energy changes of "
        "individual reactions. Glycolysis: glucose -> 2 pyruvate yields "
        "net 2 ATP + 2 NADH. The overall dG0' = -74 kJ/mol. Each ATP "
        "provides dG0' = -30.5 kJ/mol. The energy charge "
        "EC = ([ATP] + 0.5*[ADP]) / ([ATP] + [ADP] + [AMP])."
    ),
    example=(
        "Given [ATP]=3.0, [ADP]=0.8, [AMP]=0.2 mM: "
        "EC = (3.0 + 0.5*0.8) / (3.0 + 0.8 + 0.2) = 3.4/4.0 = 0.85"
    ),
    tier=5,
    domain="biochemistry",
    source="Wikipedia contributors, 'Adenylate energy charge', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Energy_charge",
    prerequisites=["atp_yield"],
))

register_atom(Atom(
    atom_type="formula",
    name="protein_folding_energy",
    content=(
        "Protein stability is determined by the free energy of folding: "
        "dG_fold = dH - T*dS. The hydrophobic effect contributes "
        "favourably (dG < 0) while conformational entropy opposes "
        "folding. Thermal denaturation occurs at T_m where "
        "dG_fold = 0, so T_m = dH/dS."
    ),
    example=(
        "Given dH = -200 kJ/mol, dS = -0.6 kJ/(mol*K): "
        "T_m = 200/0.6 = 333.3 K = 60.3 C. At 25C (298K): "
        "dG = -200 - 298*(-0.6) = -200 + 178.8 = -21.2 kJ/mol (stable)"
    ),
    tier=6,
    domain="biochemistry",
    source="Wikipedia contributors, 'Protein folding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Protein_folding",
    prerequisites=["gibbs_free_energy_biochem"],
))

register_atom(Atom(
    atom_type="formula",
    name="nucleic_acid_melting",
    content=(
        "The melting temperature T_m of DNA is the temperature at which "
        "50% of the double-stranded DNA dissociates. For short oligos "
        "(< 14 nt), Wallace rule: T_m = 2*(A+T) + 4*(G+C) degrees C. "
        "For longer sequences, nearest-neighbour thermodynamics applies: "
        "T_m = dH / (dS + R*ln(C/4)) - 273.15, where C is strand "
        "concentration."
    ),
    example=(
        "Oligo ATGCGATC (3 AT + 5 GC): T_m = 2*3 + 4*5 = 6 + 20 "
        "= 26 C. For GGCCAATTGGCC (4 AT + 8 GC): T_m = 2*4 + 4*8 "
        "= 8 + 32 = 40 C"
    ),
    tier=5,
    domain="biochemistry",
    source="Wikipedia contributors, 'Nucleic acid thermodynamics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nucleic_acid_thermodynamics",
    prerequisites=["gc_content"],
))

register_atom(Atom(
    atom_type="formula",
    name="redox_potential",
    content=(
        "The standard reduction potential E0 determines the direction "
        "of electron transfer in redox reactions. The Nernst equation "
        "for a half-reaction: E = E0 - (RT/nF)*ln(Q), where n is "
        "the number of electrons, F = 96485 C/mol. In biological "
        "systems, E0' is measured at pH 7. A more positive E0' means "
        "a stronger oxidising agent."
    ),
    example=(
        "NAD+/NADH: E0' = -0.32 V. O2/H2O: E0' = +0.816 V. "
        "dE0' = 0.816 - (-0.32) = 1.136 V. dG0' = -n*F*dE0' "
        "= -2*96485*1.136 = -219.2 kJ/mol"
    ),
    tier=5,
    domain="biochemistry",
    source="Wikipedia contributors, 'Reduction potential', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reduction_potential",
    prerequisites=["nernst_equation"],
))
