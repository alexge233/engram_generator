"""Knowledge atoms for physical chemistry, genetics, and epidemiology.

Registers formula, law, and model atoms covering reaction kinetics,
thermodynamic equilibria, Mendelian genetics, population genetics,
and epidemiological modelling. Each atom stores the authoritative
statement sourced from Wikipedia, a worked example, tier, domain,
source citation, source URL, and prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Physical chemistry (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="rate_law",
    content=(
        "The rate law or rate equation for a chemical reaction is an "
        "expression that relates the rate of reaction to the concentrations "
        "of the reactants raised to appropriate powers: rate = k[A]^m[B]^n, "
        "where k is the rate constant, [A] and [B] are molar concentrations, "
        "and m, n are the reaction orders with respect to each reactant. "
        "The overall order is m + n."
    ),
    example=(
        "Given k=0.05, [A]=0.2 M, [B]=0.3 M, m=1, n=2: "
        "rate = 0.05 * 0.2^1 * 0.3^2 = 0.05 * 0.2 * 0.09 = 0.0009 M/s"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Rate equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rate_equation",
    prerequisites=["multiplication", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="arrhenius",
    content=(
        "The Arrhenius equation describes the temperature dependence of "
        "reaction rate constants: k = A * exp(-Ea / (R*T)), where k is "
        "the rate constant, A is the pre-exponential factor (frequency "
        "factor), Ea is the activation energy in J/mol, R = 8.314 J/(mol*K) "
        "is the gas constant, and T is the absolute temperature in Kelvin."
    ),
    example=(
        "Given A=1e10, Ea=50000 J/mol, T=300 K: "
        "k = 1e10 * exp(-50000/(8.314*300)) = 1e10 * exp(-20.06) "
        "= 1e10 * 1.96e-9 = 19.6 s^-1"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Arrhenius equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arrhenius_equation",
    prerequisites=["exponentiation", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="equilibrium_constant",
    content=(
        "The equilibrium constant K for a reversible reaction "
        "aA + bB <-> cC + dD is defined as K = [C]^c[D]^d / ([A]^a[B]^b), "
        "where brackets denote equilibrium molar concentrations. For gases, "
        "Kp uses partial pressures. K > 1 favours products, K < 1 favours "
        "reactants. The relationship between Kp and Kc is Kp = Kc(RT)^(dn), "
        "where dn = (c+d) - (a+b)."
    ),
    example=(
        "For N2 + 3H2 <-> 2NH3 at equilibrium: [N2]=0.5, [H2]=0.3, [NH3]=0.2. "
        "K = [NH3]^2 / ([N2]*[H2]^3) = 0.04 / (0.5*0.027) = 0.04/0.0135 = 2.963"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Equilibrium constant', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Equilibrium_constant",
    prerequisites=["division", "exponentiation"],
))

register_atom(Atom(
    atom_type="law",
    name="le_chatelier",
    content=(
        "Le Chatelier's principle states that if a dynamic equilibrium is "
        "disturbed by changing the conditions (concentration, temperature, "
        "pressure, or volume), the position of equilibrium shifts to "
        "counteract the change. Adding reactant shifts equilibrium towards "
        "products. Increasing temperature shifts equilibrium in the "
        "endothermic direction. Increasing pressure shifts equilibrium "
        "towards the side with fewer moles of gas."
    ),
    example=(
        "N2 + 3H2 <-> 2NH3 (exothermic, dH < 0). Increase pressure: "
        "reactant side has 4 mol gas, product side has 2 mol gas, "
        "so equilibrium shifts right (towards NH3). Increase temperature: "
        "shifts left (endothermic direction) to consume added heat."
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Le Chatelier's principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Le_Chatelier%27s_principle",
    prerequisites=["equilibrium_constant"],
))

register_atom(Atom(
    atom_type="law",
    name="hess_law",
    content=(
        "Hess's law states that the total enthalpy change for a reaction "
        "is independent of the pathway taken, depending only on the initial "
        "and final states. This allows calculation of enthalpy changes for "
        "reactions that are difficult to measure directly, by combining "
        "known enthalpy changes of intermediate steps: "
        "dH_rxn = sum(dH_products) - sum(dH_reactants)."
    ),
    example=(
        "Find dH for C + O2 -> CO2 given: "
        "(1) C + 0.5*O2 -> CO, dH1 = -110.5 kJ; "
        "(2) CO + 0.5*O2 -> CO2, dH2 = -283.0 kJ. "
        "dH = dH1 + dH2 = -110.5 + (-283.0) = -393.5 kJ"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Hess's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hess%27s_law",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="nernst_equation",
    content=(
        "The Nernst equation relates the reduction potential of an "
        "electrochemical cell to the standard electrode potential and "
        "the activities of the chemical species: "
        "E = E0 - (RT/(nF)) * ln(Q), where E0 is the standard potential, "
        "R = 8.314 J/(mol*K), T is temperature in K, n is the number of "
        "electrons transferred, F = 96485 C/mol is Faraday's constant, "
        "and Q is the reaction quotient. At 25 C: E = E0 - (0.0257/n)*ln(Q)."
    ),
    example=(
        "Given E0=0.34 V, n=2, T=298 K, Q=0.01: "
        "E = 0.34 - (0.0257/2)*ln(0.01) = 0.34 - 0.01285*(-4.605) "
        "= 0.34 + 0.0592 = 0.399 V"
    ),
    tier=6,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Nernst equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nernst_equation",
    prerequisites=["division", "logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="gibbs_spontaneity",
    content=(
        "The Gibbs free energy change determines the spontaneity of a "
        "process at constant temperature and pressure: dG = dH - T*dS, "
        "where dH is the enthalpy change, T is the absolute temperature "
        "in Kelvin, and dS is the entropy change. A reaction is "
        "spontaneous when dG < 0, non-spontaneous when dG > 0, and at "
        "equilibrium when dG = 0."
    ),
    example=(
        "Given dH = -100 kJ, dS = -0.2 kJ/K, T = 400 K: "
        "dG = -100 - 400*(-0.2) = -100 + 80 = -20 kJ (spontaneous)"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Gibbs free energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gibbs_free_energy",
    prerequisites=["multiplication", "subtraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="reaction_order",
    content=(
        "The order of a chemical reaction with respect to a given reactant "
        "is the exponent to which its concentration is raised in the rate "
        "law. It is determined experimentally by the method of initial rates "
        "or by integrated rate laws. For a zeroth-order reaction: [A] = [A]0 - kt. "
        "For first-order: ln[A] = ln[A]0 - kt. For second-order: "
        "1/[A] = 1/[A]0 + kt."
    ),
    example=(
        "Method of initial rates: doubling [A] quadruples rate. "
        "rate2/rate1 = ([A]2/[A]1)^n => 4 = 2^n => n = 2 (second order). "
        "Half-life for second order: t_1/2 = 1/(k*[A]0)"
    ),
    tier=5,
    domain="physical_chemistry",
    source="Wikipedia contributors, 'Order of reaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Order_of_reaction",
    prerequisites=["logarithm", "division"],
))


# ---------------------------------------------------------------------------
# Genetics (tier 3-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="rule",
    name="punnett_square",
    content=(
        "A Punnett square is a diagram used to predict the genotype and "
        "phenotype combinations of a genetic cross. For a monohybrid cross "
        "between two heterozygous parents (Aa x Aa), the Punnett square "
        "yields genotype ratio 1 AA : 2 Aa : 1 aa, and phenotype ratio "
        "3 dominant : 1 recessive (assuming complete dominance)."
    ),
    example=(
        "Cross Aa x Aa: "
        "| | A | a | => AA, Aa, Aa, aa "
        "|A| AA| Aa| Genotype ratio: 1:2:1 "
        "|a| Aa| aa| Phenotype ratio: 3:1 (75% dominant)"
    ),
    tier=3,
    domain="genetics",
    source="Wikipedia contributors, 'Punnett square', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Punnett_square",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="rule",
    name="dihybrid_cross",
    content=(
        "A dihybrid cross examines the inheritance of two different traits "
        "simultaneously. For two heterozygous parents (AaBb x AaBb), the "
        "F2 generation shows a 9:3:3:1 phenotype ratio assuming independent "
        "assortment and complete dominance: 9 A_B_ : 3 A_bb : 3 aaB_ : 1 aabb. "
        "This results in 16 possible genotype combinations."
    ),
    example=(
        "AaBb x AaBb: 16 offspring. "
        "9/16 both dominant, 3/16 first dominant + second recessive, "
        "3/16 first recessive + second dominant, 1/16 both recessive. "
        "E.g. round-yellow (9) : round-green (3) : wrinkled-yellow (3) : wrinkled-green (1)"
    ),
    tier=4,
    domain="genetics",
    source="Wikipedia contributors, 'Dihybrid cross', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dihybrid_cross",
    prerequisites=["punnett_square"],
))

register_atom(Atom(
    atom_type="formula",
    name="hardy_weinberg",
    content=(
        "The Hardy-Weinberg equilibrium principle states that allele and "
        "genotype frequencies in a population remain constant from "
        "generation to generation in the absence of evolutionary forces. "
        "For two alleles p and q (where p + q = 1): p^2 + 2pq + q^2 = 1, "
        "giving genotype frequencies: p^2 (AA), 2pq (Aa), q^2 (aa)."
    ),
    example=(
        "Given q^2 = 0.04 (frequency of aa): q = 0.2, p = 0.8. "
        "AA = p^2 = 0.64, Aa = 2pq = 0.32, aa = 0.04. "
        "Carrier frequency = 2pq = 32%"
    ),
    tier=4,
    domain="genetics",
    source="Wikipedia contributors, 'Hardy-Weinberg principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hardy%E2%80%93Weinberg_principle",
    prerequisites=["quadratic"],
))

register_atom(Atom(
    atom_type="formula",
    name="chi_square_genetics",
    content=(
        "The chi-square test in genetics compares observed offspring ratios "
        "to expected Mendelian ratios. chi^2 = sum((O - E)^2 / E), where "
        "O is observed count and E is expected count. The result is compared "
        "to a critical value with (categories - 1) degrees of freedom. "
        "If chi^2 < critical value, the data fits the expected ratio."
    ),
    example=(
        "Monohybrid cross, 100 offspring: 80 dominant, 20 recessive. "
        "Expected 3:1 = 75:25. "
        "chi^2 = (80-75)^2/75 + (20-25)^2/25 = 25/75 + 25/25 "
        "= 0.333 + 1.0 = 1.333. df=1, critical=3.84. "
        "1.333 < 3.84, so data fits expected ratio."
    ),
    tier=5,
    domain="genetics",
    source="Wikipedia contributors, 'Chi-squared test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chi-squared_test",
    prerequisites=["subtraction", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="linked_genes",
    content=(
        "Linked genes are genes located on the same chromosome that tend "
        "to be inherited together. The recombination frequency (RF) between "
        "two linked genes equals the number of recombinant offspring divided "
        "by total offspring: RF = recombinants / total. RF ranges from 0 "
        "(completely linked) to 0.5 (unlinked). RF is used as a measure "
        "of genetic distance in centimorgans (cM), where 1 cM = 1% RF."
    ),
    example=(
        "Test cross: 45 parental type AB, 42 parental type ab, "
        "6 recombinant Ab, 7 recombinant aB. Total = 100. "
        "RF = (6+7)/100 = 0.13 = 13 cM apart"
    ),
    tier=4,
    domain="genetics",
    source="Wikipedia contributors, 'Genetic linkage', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Genetic_linkage",
    prerequisites=["division", "percentage"],
))

register_atom(Atom(
    atom_type="rule",
    name="blood_type",
    content=(
        "The ABO blood group system is determined by a single gene with "
        "three alleles: I^A, I^B, and i. I^A and I^B are codominant to "
        "each other and both dominant over i. Possible genotypes: "
        "I^A I^A or I^A i (type A), I^B I^B or I^B i (type B), "
        "I^A I^B (type AB), ii (type O). Type O is the universal donor "
        "and type AB is the universal recipient."
    ),
    example=(
        "Cross: I^A i x I^B i. Punnett square: "
        "I^A I^B (AB), I^A i (A), I^B i (B), ii (O). "
        "Offspring: 25% type AB, 25% type A, 25% type B, 25% type O"
    ),
    tier=3,
    domain="genetics",
    source="Wikipedia contributors, 'ABO blood group system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/ABO_blood_group_system",
    prerequisites=["punnett_square"],
))


# ---------------------------------------------------------------------------
# Epidemiology (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="model",
    name="sir_model",
    content=(
        "The SIR model divides a population into three compartments: "
        "Susceptible (S), Infected (I), and Recovered (R). The differential "
        "equations are: dS/dt = -beta*S*I/N, dI/dt = beta*S*I/N - gamma*I, "
        "dR/dt = gamma*I, where beta is the transmission rate, gamma is "
        "the recovery rate, and N is the total population. "
        "R0 = beta/gamma is the basic reproduction number."
    ),
    example=(
        "N=1000, S=999, I=1, R=0, beta=0.3, gamma=0.1: "
        "R0 = 0.3/0.1 = 3. "
        "dS/dt = -0.3*999*1/1000 = -0.2997. "
        "dI/dt = 0.2997 - 0.1*1 = 0.1997. "
        "dR/dt = 0.1*1 = 0.1"
    ),
    tier=5,
    domain="epidemiology",
    source="Wikipedia contributors, 'Compartmental models in epidemiology', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology",
    prerequisites=["differential_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="basic_reproduction",
    content=(
        "The basic reproduction number R0 is the expected number of "
        "secondary infections produced by a single infected individual "
        "in a fully susceptible population. For the SIR model, "
        "R0 = beta/gamma = beta * D, where D = 1/gamma is the mean "
        "infectious period. If R0 > 1, an epidemic will occur. "
        "If R0 < 1, the infection will die out."
    ),
    example=(
        "Measles: beta=1.5/day, gamma=0.1/day (10-day infectious period). "
        "R0 = 1.5/0.1 = 15. Since R0 >> 1, measles is highly contagious."
    ),
    tier=5,
    domain="epidemiology",
    source="Wikipedia contributors, 'Basic reproduction number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Basic_reproduction_number",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="incidence_rate",
    content=(
        "The incidence rate (or person-time rate) measures the frequency "
        "of new cases of disease in a population over time: "
        "IR = number of new cases / person-time at risk. Person-time "
        "is the sum of time each person was observed while at risk. "
        "Cumulative incidence (risk) = new cases / population at start."
    ),
    example=(
        "100 people followed for 1 year, 10 develop disease (5 at 6 months). "
        "Person-time = 90*1 + 5*0.5 + 5*1 = 97.5 person-years. "
        "IR = 10/97.5 = 0.1026 per person-year"
    ),
    tier=4,
    domain="epidemiology",
    source="Wikipedia contributors, 'Incidence (epidemiology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Incidence_(epidemiology)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="relative_risk",
    content=(
        "Relative risk (RR) compares the probability of an event in an "
        "exposed group to that in an unexposed group: "
        "RR = P(event|exposed) / P(event|unexposed) = (a/(a+b)) / (c/(c+d)), "
        "where a = exposed with event, b = exposed without, c = unexposed "
        "with event, d = unexposed without. RR = 1 means no association, "
        "RR > 1 means increased risk, RR < 1 means decreased risk."
    ),
    example=(
        "Exposed: 30 disease, 70 healthy. Unexposed: 10 disease, 90 healthy. "
        "RR = (30/100) / (10/100) = 0.3/0.1 = 3.0. "
        "Exposed group has 3x the risk."
    ),
    tier=4,
    domain="epidemiology",
    source="Wikipedia contributors, 'Relative risk', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Relative_risk",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="herd_immunity",
    content=(
        "The herd immunity threshold is the proportion of the population "
        "that must be immune to prevent sustained disease transmission: "
        "HIT = 1 - 1/R0, where R0 is the basic reproduction number. "
        "When the proportion immune exceeds HIT, each infected person "
        "infects fewer than one other person on average, and the "
        "epidemic declines."
    ),
    example=(
        "Measles R0 = 15: HIT = 1 - 1/15 = 1 - 0.0667 = 0.9333. "
        "93.3% of the population must be immune to achieve herd immunity."
    ),
    tier=4,
    domain="epidemiology",
    source="Wikipedia contributors, 'Herd immunity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Herd_immunity",
    prerequisites=["division", "basic_reproduction"],
))

register_atom(Atom(
    atom_type="formula",
    name="life_table",
    content=(
        "A life table provides a statistical summary of mortality and "
        "survival in a population by age. Key columns: l_x (number "
        "surviving to age x), d_x = l_x - l_{x+1} (deaths in interval), "
        "q_x = d_x/l_x (probability of dying), p_x = 1 - q_x "
        "(probability of surviving), e_x = T_x/l_x (life expectancy "
        "at age x), where T_x = sum of L_x values from age x onward."
    ),
    example=(
        "l_0=1000, l_1=950, l_2=900, l_3=800, l_4=0. "
        "d_0=50, q_0=50/1000=0.05. "
        "L_0=(1000+950)/2=975, L_1=925, L_2=850, L_3=400. "
        "T_0=975+925+850+400=3150. e_0=3150/1000=3.15 years"
    ),
    tier=5,
    domain="epidemiology",
    source="Wikipedia contributors, 'Life table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Life_table",
    prerequisites=["division", "addition"],
))
