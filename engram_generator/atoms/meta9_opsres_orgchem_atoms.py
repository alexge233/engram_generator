"""Knowledge atoms for meta-reasoning tier 9 ext, operations research, and organic chemistry ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── META-REASONING TIER 9 EXT ─────────────────────────────────────

register_atom(Atom(
    atom_type="skill",
    name="research_question_formulate",
    content=(
        "Research question formulation is the process of defining a clear, "
        "focused, and researchable question that guides an investigation. "
        "A good research question is specific, measurable, and addresses "
        "a gap in existing knowledge. The PICO framework (Population, "
        "Intervention, Comparison, Outcome) is commonly used in clinical "
        "research to structure questions."
    ),
    example=(
        "Given domain: 'transformer efficiency'. "
        "Formulate: 'Does replacing dense attention with sparse attention "
        "in 12-layer transformers reduce inference latency by >30% on "
        "sequence lengths >4096 while maintaining >95% of BLEU score?' "
        "Criteria: specific architecture, measurable threshold, clear comparison."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Research question', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Research_question",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="literature_gap_identify",
    content=(
        "A literature gap (or research gap) is an area where existing "
        "research is insufficient, contradictory, or absent. Identifying "
        "gaps involves systematic review of existing work, noting what "
        "has been studied, what methods have been used, and what remains "
        "unanswered. Common gap types: evidence gap, knowledge gap, "
        "practical-knowledge gap, methodological gap, empirical gap, "
        "theoretical gap, population gap."
    ),
    example=(
        "Given topic: 'neural architecture search for edge devices'. "
        "Gap: 'Existing NAS methods optimise for accuracy/latency on "
        "server GPUs; no published work systematically explores NAS under "
        "memory constraints <512MB with quantisation-aware search.' "
        "Type: methodological + population gap."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Research gap', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Systematic_review",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="experiment_interpret",
    content=(
        "Experiment interpretation involves analysing results in context "
        "of the hypothesis, identifying whether outcomes support, refute, "
        "or are inconclusive regarding the hypothesis. Key considerations: "
        "statistical significance vs practical significance, confounding "
        "variables, effect size, reproducibility, and external validity."
    ),
    example=(
        "Experiment: 'sparse attention vs dense on WMT14'. "
        "Results: BLEU 27.1 vs 27.8, p=0.03, latency 40% lower. "
        "Interpretation: statistically significant BLEU drop (0.7 points) "
        "but practically negligible (<1 point). Latency reduction exceeds "
        "30% target. Conclusion: supports hypothesis with minor quality tradeoff."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Interpretation (logic)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Design_of_experiments",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="algorithm_adapt",
    content=(
        "Algorithm adaptation is modifying an existing algorithm to work "
        "in a new setting -- different data structures, constraints, or "
        "problem domains. Common adaptations: changing the comparison "
        "function, adapting data structures, adding constraints, "
        "parallelising sequential steps, or reducing space complexity."
    ),
    example=(
        "Adapt Dijkstra's shortest path for negative weights: "
        "Problem: Dijkstra fails with negative edges. "
        "Adaptation: use Bellman-Ford (relax all edges V-1 times) "
        "or Johnson's algorithm (reweight edges using potentials from "
        "Bellman-Ford, then run Dijkstra from each source)."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Algorithm', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Algorithm_design",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="theorem",
    name="complexity_lower_bound",
    content=(
        "A lower bound in computational complexity is a proof that any "
        "algorithm solving a given problem must use at least a certain "
        "amount of a resource (time, space, comparisons). Common "
        "techniques: adversary arguments, information-theoretic arguments, "
        "and reductions from known hard problems. Example: comparison-based "
        "sorting requires Omega(n log n) comparisons in the worst case."
    ),
    example=(
        "Prove: comparison-based sorting requires Omega(n log n). "
        "Decision tree has n! leaves (one per permutation). "
        "Binary tree with L leaves has height >= log2(L). "
        "Height >= log2(n!) = Theta(n log n) by Stirling's approximation. "
        "Therefore any comparison sort needs Omega(n log n) comparisons."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Comparison sort', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Comparison_sort#Number_of_comparisons_required_to_sort_a_list",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="proof_generalize",
    content=(
        "Proof generalisation extends a proven result to a broader class "
        "of objects. Techniques: identify which properties of the specific "
        "case the proof actually uses, abstract those into axioms, verify "
        "the proof holds with only those axioms, then state the "
        "generalised theorem."
    ),
    example=(
        "Specific: 'sum of first n natural numbers = n(n+1)/2'. "
        "Generalise to arithmetic progressions: "
        "S = n/2 * (2a + (n-1)d) where a=first term, d=common difference. "
        "Original is special case with a=1, d=1: S = n/2 * (2 + n - 1) = n(n+1)/2."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Generalization', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Generalization",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="abstraction_identify",
    content=(
        "Abstraction identification is recognising the common structure "
        "underlying seemingly different problems. In mathematics, this "
        "leads to unified theories (e.g., group theory unifying symmetries). "
        "In computer science, it produces reusable patterns (e.g., "
        "map-reduce abstracts parallel computation)."
    ),
    example=(
        "Problems: (1) rotate a square, (2) permute elements, (3) "
        "clock arithmetic. Abstraction: all are instances of group theory "
        "-- each has an identity, closure, associativity, and inverses. "
        "The abstract group captures the shared structure."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Abstraction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Abstraction_(mathematics)",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="skill",
    name="failure_predict",
    content=(
        "Failure prediction involves identifying conditions under which "
        "an algorithm, model, or system will fail before running it. "
        "Techniques: boundary analysis, invariant checking, adversarial "
        "input construction, asymptotic analysis of edge cases."
    ),
    example=(
        "Algorithm: binary search on sorted array. "
        "Predicted failures: (1) empty array -- IndexError, "
        "(2) integer overflow in mid = (lo+hi)/2 when lo+hi > 2^31, "
        "(3) duplicates -- may return any index, not leftmost. "
        "Fix: mid = lo + (hi-lo)//2, add empty check, use bisect_left."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Failure mode and effects analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis",
    prerequisites=["error_detection"],
))

# ── OPERATIONS RESEARCH ────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="mm1_queue",
    content=(
        "The M/M/1 queue is a single-server queueing model with Poisson "
        "arrivals (rate lambda) and exponential service times (rate mu). "
        "Key metrics: utilisation rho = lambda/mu, average number in system "
        "L = rho/(1-rho), average wait time W = 1/(mu-lambda), "
        "average queue length Lq = rho^2/(1-rho)."
    ),
    example=(
        "Given lambda=3 arrivals/min, mu=5 services/min: "
        "rho = 3/5 = 0.6, L = 0.6/0.4 = 1.5 customers, "
        "W = 1/(5-3) = 0.5 min, Lq = 0.36/0.4 = 0.9 customers."
    ),
    tier=5,
    domain="operations_research",
    source="Wikipedia contributors, 'M/M/1 queue', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/M/M/1_queue",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="mmc_queue",
    content=(
        "The M/M/c queue extends M/M/1 to c parallel servers. "
        "Arrivals are Poisson (rate lambda), service times exponential "
        "(rate mu per server). Utilisation rho = lambda/(c*mu). "
        "Uses the Erlang C formula for P(wait > 0)."
    ),
    example=(
        "Given lambda=10, mu=4, c=3: rho = 10/(3*4) = 0.833. "
        "System is stable (rho < 1). Average number in queue "
        "Lq = C(c,rho)*rho/(1-rho) where C is the Erlang C probability."
    ),
    tier=6,
    domain="operations_research",
    source="Wikipedia contributors, 'M/M/c queue', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/M/M/c_queue",
    prerequisites=["mm1_queue"],
))

register_atom(Atom(
    atom_type="formula",
    name="inventory_eoq",
    content=(
        "The Economic Order Quantity (EOQ) model determines the optimal "
        "order quantity that minimises total inventory costs (ordering + "
        "holding). EOQ = sqrt(2*D*S/H) where D is annual demand, "
        "S is ordering cost per order, H is holding cost per unit per year."
    ),
    example=(
        "Given D=10000 units/year, S=$50/order, H=$2/unit/year: "
        "EOQ = sqrt(2*10000*50/2) = sqrt(500000) = 707.1 units."
    ),
    tier=4,
    domain="operations_research",
    source="Wikipedia contributors, 'Economic order quantity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Economic_order_quantity",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="newsvendor",
    content=(
        "The newsvendor model determines the optimal stocking quantity "
        "for a perishable product under demand uncertainty. The critical "
        "ratio is CR = (p-c)/(p-s) where p is selling price, c is cost, "
        "s is salvage value. Order Q* such that F(Q*) = CR, where F is "
        "the demand CDF."
    ),
    example=(
        "Given p=$10, c=$6, s=$2: CR = (10-6)/(10-2) = 4/8 = 0.5. "
        "If demand ~ Normal(100, 20): Q* = 100 + 0*20 = 100 units "
        "(z=0 for F=0.5)."
    ),
    tier=5,
    domain="operations_research",
    source="Wikipedia contributors, 'Newsvendor model', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Newsvendor_model",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="project_scheduling",
    content=(
        "Project scheduling determines the minimum project duration using "
        "the Critical Path Method (CPM). Activities are nodes in a DAG "
        "with durations. The critical path is the longest path from start "
        "to finish. Forward pass computes earliest start/finish times; "
        "backward pass computes latest start/finish times. Slack = LS - ES."
    ),
    example=(
        "Activities: A(3), B(2), C(4), D(1). Dependencies: C after A, "
        "D after A and B. Forward pass: A:ES=0,EF=3; B:ES=0,EF=2; "
        "C:ES=3,EF=7; D:ES=3,EF=4. Critical path: A->C, duration=7."
    ),
    tier=5,
    domain="operations_research",
    source="Wikipedia contributors, 'Critical path method', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Critical_path_method",
    prerequisites=["topo_sort"],
))

register_atom(Atom(
    atom_type="formula",
    name="markov_decision",
    content=(
        "A Markov Decision Process (MDP) is defined by states S, actions A, "
        "transition probabilities P(s'|s,a), rewards R(s,a), and discount "
        "factor gamma. The Bellman equation: V(s) = max_a [R(s,a) + "
        "gamma * sum_s' P(s'|s,a) V(s')]. Value iteration updates V "
        "until convergence."
    ),
    example=(
        "2-state MDP: S={s1,s2}, A={stay,go}, gamma=0.9. "
        "R(s1,stay)=5, R(s1,go)=10, P(s2|s1,go)=1, P(s1|s1,stay)=1. "
        "V(s1) = max(5+0.9*V(s1), 10+0.9*V(s2)). Iterate until stable."
    ),
    tier=6,
    domain="operations_research",
    source="Wikipedia contributors, 'Markov decision process', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Markov_decision_process",
    prerequisites=["markov_chain"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="simulation_lcg",
    content=(
        "A Linear Congruential Generator (LCG) produces pseudorandom "
        "numbers using the recurrence X_{n+1} = (a*X_n + c) mod m. "
        "Full period requires: c and m coprime, a-1 divisible by all "
        "prime factors of m, if m divisible by 4 then a-1 divisible by 4."
    ),
    example=(
        "LCG with a=5, c=3, m=16, X_0=7: "
        "X_1 = (5*7+3) mod 16 = 38 mod 16 = 6, "
        "X_2 = (5*6+3) mod 16 = 33 mod 16 = 1, "
        "X_3 = (5*1+3) mod 16 = 8 mod 16 = 8."
    ),
    tier=4,
    domain="operations_research",
    source="Wikipedia contributors, 'Linear congruential generator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Linear_congruential_generator",
    prerequisites=["modular"],
))

register_atom(Atom(
    atom_type="formula",
    name="reliability",
    content=(
        "System reliability is the probability that a system performs its "
        "intended function for a specified period. For series systems: "
        "R_sys = R_1 * R_2 * ... * R_n. For parallel (redundant) systems: "
        "R_sys = 1 - (1-R_1)*(1-R_2)*...*(1-R_n). MTTF for exponential "
        "distribution = 1/lambda."
    ),
    example=(
        "Series system with R_1=0.95, R_2=0.90, R_3=0.98: "
        "R_sys = 0.95 * 0.90 * 0.98 = 0.8379. "
        "Parallel system with same: R_sys = 1 - 0.05*0.10*0.02 = 0.9999."
    ),
    tier=5,
    domain="operations_research",
    source="Wikipedia contributors, 'Reliability engineering', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Reliability_engineering",
    prerequisites=["basic_prob"],
))

# ── ORGANIC CHEMISTRY EXT ──────────────────────────────────────────

register_atom(Atom(
    atom_type="rule",
    name="markovnikov_rule",
    content=(
        "Markovnikov's rule states that in the addition of HX to an "
        "asymmetric alkene, the hydrogen atom adds to the carbon with "
        "more hydrogen atoms (less substituted carbon), and the halide "
        "adds to the more substituted carbon. This produces the more "
        "stable carbocation intermediate."
    ),
    example=(
        "Propene + HBr: CH3-CH=CH2 + HBr -> CH3-CHBr-CH3 (2-bromopropane). "
        "H adds to CH2 (more H's), Br adds to CH (more substituted). "
        "Anti-Markovnikov with peroxides gives 1-bromopropane."
    ),
    tier=5,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Markovnikov's rule', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Markovnikov%27s_rule",
    prerequisites=["functional_group_id"],
))

register_atom(Atom(
    atom_type="rule",
    name="zaitsev_rule",
    content=(
        "Zaitsev's rule (Saytzeff's rule) states that in elimination "
        "reactions (E1 and E2), the major product is the more substituted "
        "alkene (the one with more alkyl groups on the double-bond "
        "carbons), as it is thermodynamically more stable."
    ),
    example=(
        "2-bromobutane + NaOH/EtOH (E2): "
        "Major product: 2-butene (CH3-CH=CH-CH3, more substituted). "
        "Minor product: 1-butene (CH2=CH-CH2-CH3, less substituted). "
        "Ratio typically ~80:20 favouring Zaitsev product."
    ),
    tier=5,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Zaitsev's rule', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Zaitsev%27s_rule",
    prerequisites=["functional_group_id"],
))

register_atom(Atom(
    atom_type="formula",
    name="grignard_reaction",
    content=(
        "A Grignard reaction uses an organomagnesium halide (RMgX, the "
        "Grignard reagent) as a nucleophile to attack electrophilic "
        "carbons. With aldehydes it gives secondary alcohols, with "
        "ketones tertiary alcohols, and with CO2 carboxylic acids. "
        "The reaction requires anhydrous conditions (ether solvent)."
    ),
    example=(
        "CH3MgBr + CH3CHO -> CH3CH(OH)CH3 (2-propanol) after H3O+ workup. "
        "The Grignard reagent (methyl) attacks the aldehyde carbonyl, "
        "forming a magnesium alkoxide, which is protonated to give "
        "a secondary alcohol."
    ),
    tier=6,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Grignard reaction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Grignard_reaction",
    prerequisites=["functional_group_id"],
))

register_atom(Atom(
    atom_type="rule",
    name="oxidation_reduction_organic",
    content=(
        "In organic chemistry, oxidation increases the number of C-O or "
        "C-N bonds (or decreases C-H bonds), while reduction does the "
        "opposite. The oxidation state of carbon ranges from -4 (CH4) to "
        "+4 (CO2). Common oxidising agents: KMnO4, CrO3, PCC, Jones "
        "reagent. Common reducing agents: NaBH4, LiAlH4, H2/Pd."
    ),
    example=(
        "Ethanol -> acetaldehyde -> acetic acid. "
        "CH3CH2OH --[PCC]--> CH3CHO (aldehyde, partial oxidation). "
        "CH3CHO --[KMnO4]--> CH3COOH (carboxylic acid, full oxidation). "
        "Reverse: CH3COOH --[LiAlH4]--> CH3CH2OH (reduction)."
    ),
    tier=5,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Organic redox reaction', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Organic_redox_reaction",
    prerequisites=["oxidation_state"],
))

register_atom(Atom(
    atom_type="rule",
    name="aromatic_substitution",
    content=(
        "Electrophilic aromatic substitution (EAS) replaces a hydrogen "
        "on an aromatic ring with an electrophile. Steps: (1) generation "
        "of electrophile, (2) electrophilic attack forming sigma complex "
        "(arenium ion), (3) deprotonation restoring aromaticity. "
        "Substituent effects: electron-donating groups (EDG) are ortho/para "
        "directors; electron-withdrawing groups (EWG) are meta directors."
    ),
    example=(
        "Nitration of toluene: CH3-C6H5 + HNO3/H2SO4. "
        "CH3 is EDG (ortho/para director). "
        "Products: ~60% ortho-nitrotoluene, ~37% para-nitrotoluene, "
        "~3% meta-nitrotoluene."
    ),
    tier=6,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Electrophilic aromatic substitution', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Electrophilic_aromatic_substitution",
    prerequisites=["functional_group_id"],
))

register_atom(Atom(
    atom_type="definition",
    name="fischer_projection",
    content=(
        "A Fischer projection is a two-dimensional representation of a "
        "three-dimensional organic molecule. Horizontal bonds point toward "
        "the viewer (out of the page), vertical bonds point away. "
        "The most oxidised carbon is placed at the top. Used primarily "
        "for sugars and amino acids. In D-sugars, the OH on the lowest "
        "chiral centre is on the right."
    ),
    example=(
        "D-glucose Fischer projection: CHO at top, then "
        "H-C-OH, HO-C-H, H-C-OH, H-C-OH, CH2OH at bottom. "
        "The OH on C5 (lowest chiral centre) is on the right, "
        "so it is D-glucose."
    ),
    tier=5,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Fischer projection', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fischer_projection",
    prerequisites=["stereocenter_count"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="retrosynthesis",
    content=(
        "Retrosynthetic analysis works backwards from the target molecule "
        "to identify simpler precursors. A disconnection breaks a bond "
        "in the target to reveal a synthon (idealised reactive fragment). "
        "The synthon is then mapped to a real reagent. The process "
        "repeats until commercially available starting materials are reached."
    ),
    example=(
        "Target: PhCH(OH)CH3 (1-phenylethanol). "
        "Disconnection: break C-C bond next to OH. "
        "Synthons: PhCHO (electrophile) + CH3- (nucleophile). "
        "Reagents: benzaldehyde + CH3MgBr (Grignard). "
        "Synthesis: PhCHO + CH3MgBr -> PhCH(OMgBr)CH3 -> PhCH(OH)CH3."
    ),
    tier=7,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Retrosynthetic analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Retrosynthetic_analysis",
    prerequisites=["grignard_reaction"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="spectroscopy_interpretation",
    content=(
        "Spectroscopic interpretation combines data from IR, NMR, and "
        "mass spectrometry to determine molecular structure. IR identifies "
        "functional groups (O-H ~3300 cm-1, C=O ~1700 cm-1). 1H NMR "
        "gives hydrogen environment count, splitting, and chemical shift. "
        "Mass spec gives molecular weight and fragmentation pattern."
    ),
    example=(
        "Unknown C3H6O: MS m/z=58 (M+), IR 1715 cm-1 (C=O), "
        "1H NMR: singlet at 2.1 ppm (3H), quartet 2.4 ppm (2H), "
        "triplet 1.0 ppm (no -- actually singlet 2.1 ppm (6H)). "
        "Structure: acetone (CH3COCH3). The 6 equivalent CH3 protons "
        "give one singlet at 2.1 ppm."
    ),
    tier=6,
    domain="organic_chemistry",
    source="Wikipedia contributors, 'Spectroscopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance_spectroscopy",
    prerequisites=["functional_group_id", "nmr_splitting"],
))
