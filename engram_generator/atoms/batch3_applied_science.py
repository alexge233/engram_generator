"""Knowledge atoms for applied science and specialized domains (batch 3).

Covers: chemistry_ext, pharmacology_deep, actuarial, medical_imaging,
cell_biology_ext, geology_ext, linguistics, linguistics_ext, music_theory,
quantum_error_correction, nlp_computation, nonparametric_stats,
dimensionality_reduction, communication_systems, information_geometry,
fuzzy_logic, compressed_sensing, time_series, bayesian_statistics,
causal_inference, queuing_ext, wavelet_theory, rl_ext,
nuclear_ext, game_theory_ext, measurement_ext,
info_theory_ext, info_theory_deep.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Chemistry ext (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula", name="ideal_gas_mixture",
    content="Dalton's law: total pressure P = sum(P_i) where P_i = x_i * P (partial pressures). Amagat's law: total volume V = sum(V_i). For ideal mixtures, properties are mole-fraction weighted averages.",
    example="Gas mixture: 0.79 N2, 0.21 O2 at 1 atm. P_N2 = 0.79 atm, P_O2 = 0.21 atm.",
    tier=5, domain="chemistry",
    source="Wikipedia contributors, 'Dalton's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dalton%27s_law",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula", name="enthalpy_reaction",
    content="Reaction enthalpy dH_rxn = sum(dH_f(products)) - sum(dH_f(reactants)), where dH_f are standard enthalpies of formation. Exothermic: dH < 0 (releases heat). Endothermic: dH > 0.",
    example="2H2(g) + O2(g) -> 2H2O(l). dH = 2*(-285.8) - (2*0 + 0) = -571.6 kJ/mol.",
    tier=5, domain="chemistry",
    source="Wikipedia contributors, 'Standard enthalpy of reaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Standard_enthalpy_of_reaction",
    prerequisites=["summation"],
))

register_atom(Atom(
    atom_type="reference", name="solubility_rules",
    content="General solubility rules: all Na+, K+, NH4+ salts are soluble. All NO3- and CH3COO- salts are soluble. Most Cl-, Br-, I- salts are soluble (except Ag+, Pb2+, Hg22+). Most SO42- soluble (except Ba2+, Pb2+). Most OH-, S2-, CO32-, PO43- insoluble (except Group 1 and NH4+).",
    example="AgCl: Ag+ with Cl- -> insoluble (exception). NaCl: Na+ with Cl- -> soluble.",
    tier=4, domain="chemistry",
    source="Wikipedia contributors, 'Solubility chart', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Solubility_chart",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="method", name="oxidation_number_change",
    content="Oxidation number change method for balancing redox reactions: (1) assign oxidation numbers to all atoms, (2) identify which atoms are oxidised and reduced, (3) balance electron transfer, (4) balance atoms and charge.",
    example="Fe + CuSO4 -> FeSO4 + Cu. Fe: 0->+2 (oxidised, loses 2e-). Cu: +2->0 (reduced, gains 2e-). Already balanced.",
    tier=5, domain="chemistry",
    source="Wikipedia contributors, 'Oxidation state', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Oxidation_state",
    prerequisites=["balancing_equation"],
))

register_atom(Atom(
    atom_type="law", name="gas_effusion",
    content="Graham's law of effusion: rate1/rate2 = sqrt(M2/M1), where M is molar mass. Lighter gases effuse faster. Also applies to diffusion rates. Derived from kinetic molecular theory: v_rms = sqrt(3RT/M).",
    example="H2 (M=2) vs O2 (M=32): rate_H2/rate_O2 = sqrt(32/2) = sqrt(16) = 4. H2 effuses 4x faster.",
    tier=5, domain="chemistry",
    source="Wikipedia contributors, 'Graham's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Graham%27s_law",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula", name="calorimetry",
    content="Calorimetry measures heat: q = m*c*dT (specific heat), q = C*dT (heat capacity). In a coffee-cup calorimeter: q_rxn = -q_solution = -(m*c*dT). Bomb calorimetry: q_rxn = -(C_cal*dT).",
    example="50 g water, dT = 5 C, c = 4.184 J/(g*C). q = 50*4.184*5 = 1046 J = 1.046 kJ.",
    tier=5, domain="chemistry",
    source="Wikipedia contributors, 'Calorimetry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Calorimetry",
    prerequisites=["multiplication"],
))

# ---------------------------------------------------------------------------
# Pharmacology deep (tier 6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula", name="two_compartment_model",
    content="Two-compartment PK model: C(t) = A*exp(-alpha*t) + B*exp(-beta*t), where alpha (distribution) > beta (elimination). A and B are hybrid constants. V_d = dose / (A + B). CL = dose / AUC.",
    example="A=8 mg/L, alpha=2 hr^-1, B=2 mg/L, beta=0.2 hr^-1. At t=1: C = 8*e^-2 + 2*e^-0.2 = 1.083 + 1.637 = 2.72 mg/L.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Pharmacokinetics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pharmacokinetics#Multi-compartment_models",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="concept", name="drug_interaction",
    content="Drug interactions alter a drug's effect: pharmacokinetic (affect absorption, distribution, metabolism, excretion) or pharmacodynamic (synergy, antagonism). CYP450 inhibitors increase drug levels; inducers decrease them. Synergy: combined effect > sum of individual effects.",
    example="Ketoconazole (CYP3A4 inhibitor) + midazolam -> midazolam AUC increases 15x due to reduced metabolism.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Drug interaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Drug_interaction",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula", name="receptor_occupancy",
    content="The Clark equation: occupancy = [D] / ([D] + K_d), where [D] is drug concentration and K_d is dissociation constant. At [D] = K_d, 50% of receptors are occupied. E_max model: E = E_max * [D] / ([D] + EC_50).",
    example="K_d = 10 nM, [D] = 30 nM. Occupancy = 30/(30+10) = 0.75 = 75%.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Receptor occupancy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Occupancy_theory",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula", name="loading_dose",
    content="Loading dose achieves target plasma concentration immediately: LD = V_d * C_target / F, where V_d is volume of distribution, C_target is desired concentration, and F is bioavailability. Maintenance dose: MD = CL * C_target * tau / F.",
    example="V_d = 50 L, C_target = 10 mg/L, F = 1 (IV). LD = 50 * 10 = 500 mg.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Loading dose', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loading_dose",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula", name="pk_nonlinear",
    content="Michaelis-Menten pharmacokinetics: -dC/dt = V_max * C / (K_m + C). At low C (C << K_m): first-order (rate proportional to C). At high C (C >> K_m): zero-order (rate = V_max, constant). Phenytoin and ethanol follow nonlinear kinetics.",
    example="V_max = 500 mg/day, K_m = 5 mg/L, C = 15 mg/L. Rate = 500*15/(5+15) = 375 mg/day.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Michaelis-Menten kinetics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Michaelis%E2%80%93Menten_kinetics",
    prerequisites=["michaelis_menten"],
))

register_atom(Atom(
    atom_type="concept", name="bioequivalence",
    content="Two formulations are bioequivalent if their rate and extent of absorption are not significantly different. Criteria: 90% CI for AUC and C_max ratios must fall within 80-125%. Tested via crossover studies with log-transformed data and ANOVA.",
    example="Test/Reference AUC ratio = 1.05, 90% CI (0.95, 1.15). Within 0.80-1.25 -> bioequivalent.",
    tier=6, domain="pharmacology",
    source="Wikipedia contributors, 'Bioequivalence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bioequivalence",
    prerequisites=["confidence_interval"],
))

# ---------------------------------------------------------------------------
# Quantum error correction (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm", name="bit_flip_code",
    content="The 3-qubit bit flip code encodes |0> as |000> and |1> as |111>. A single bit flip on any qubit is corrected by majority vote. Syndrome measurement: two CNOT parity checks identify which qubit flipped without collapsing the encoded state.",
    example="|0> encoded as |000>. Bit flip on qubit 2: |010>. Syndrome measures parity of qubits (1,2) and (2,3). Syndrome 11 -> error on qubit 2. Correct by flipping qubit 2.",
    tier=6, domain="quantum_computing",
    source="Wikipedia contributors, 'Quantum error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction#Bit_flip_code",
    prerequisites=["qubit_measure"],
))

register_atom(Atom(
    atom_type="algorithm", name="phase_flip_code",
    content="The 3-qubit phase flip code encodes |+> as |+++> and |-> as |--->. A phase flip (Z error) on any qubit is detected by measuring in the X basis. Combines with bit flip code to form the Shor 9-qubit code that corrects arbitrary single-qubit errors.",
    example="|+> encoded as |+++>. Phase flip on qubit 1: |-++>. Hadamard all, measure parity. Syndrome identifies qubit 1.",
    tier=6, domain="quantum_computing",
    source="Wikipedia contributors, 'Quantum error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction",
    prerequisites=["bit_flip_code"],
))

register_atom(Atom(
    atom_type="algorithm", name="shor_code",
    content="The Shor code is a 9-qubit code that corrects any single-qubit error. It concatenates the 3-qubit phase flip code with the 3-qubit bit flip code. |0> -> (|000>+|111>)(|000>+|111>)(|000>+|111>)/2sqrt(2). Each logical qubit uses 9 physical qubits.",
    example="Bit flip on qubit 5: detected by parity checks within the second block of three. Phase flip: detected by inter-block parity checks.",
    tier=7, domain="quantum_computing",
    source="Wikipedia contributors, 'Shor code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction#Shor_code",
    prerequisites=["bit_flip_code", "phase_flip_code"],
))

register_atom(Atom(
    atom_type="concept", name="stabilizer_check",
    content="The stabilizer formalism describes quantum error-correcting codes via a group of Pauli operators that stabilize the code space: S|psi> = |psi> for all S in the stabilizer group. Error detection: if E anticommutes with some stabilizer S, measuring S reveals the error without disturbing the encoded state.",
    example="3-qubit bit flip code stabilizers: Z1Z2 and Z2Z3. Bit flip X1: X1 anticommutes with Z1Z2 (syndrome 1) but commutes with Z2Z3 (syndrome 0). Syndrome 10 -> error on qubit 1.",
    tier=7, domain="quantum_computing",
    source="Wikipedia contributors, 'Stabilizer code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stabilizer_code",
    prerequisites=["shor_code"],
))

register_atom(Atom(
    atom_type="algorithm", name="steane_code",
    content="The Steane code is a [[7,1,3]] CSS code based on the classical [7,4,3] Hamming code. It encodes 1 logical qubit in 7 physical qubits and corrects any single-qubit error. Transversal gates (H, CNOT, S) can be applied fault-tolerantly.",
    example="Logical |0> = (1/sqrt(8)) sum of even-weight codewords of Hamming(7,4). X-type errors detected by Hamming parity checks, Z-type by dual code checks.",
    tier=7, domain="quantum_computing",
    source="Wikipedia contributors, 'Steane code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Steane_code",
    prerequisites=["stabilizer_check"],
))

register_atom(Atom(
    atom_type="concept", name="logical_operators",
    content="Logical operators in a quantum error-correcting code are Pauli operators that commute with all stabilizers but are not themselves stabilizers. They act on the encoded logical qubit. For an [[n,k,d]] code, there are k pairs of logical X and Z operators. They must have weight >= d.",
    example="Shor code logical X: X on all 9 qubits. Logical Z: Z on qubits 1,2,3. Both commute with all stabilizers, anticommute with each other.",
    tier=7, domain="quantum_computing",
    source="Wikipedia contributors, 'Stabilizer code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stabilizer_code#Logical_operators",
    prerequisites=["stabilizer_check"],
))

# ---------------------------------------------------------------------------
# NLP computation (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula", name="tf_idf",
    content="TF-IDF weights terms by their importance: TF(t,d) = count(t in d) / |d|, IDF(t) = log(N / df(t)), where N is total documents and df(t) is documents containing t. TF-IDF = TF * IDF. High value = term is important in document but rare across corpus.",
    example="Term 'quantum' appears 5 times in doc of 100 words. 10000 docs, 50 contain 'quantum'. TF=0.05, IDF=log(10000/50)=5.298. TF-IDF=0.265.",
    tier=5, domain="nlp",
    source="Wikipedia contributors, 'tf-idf', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tf%E2%80%93idf",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula", name="ngram_probability",
    content="N-gram language model: P(w_n | w_1..w_{n-1}) ~ P(w_n | w_{n-N+1}..w_{n-1}) = count(w_{n-N+1}..w_n) / count(w_{n-N+1}..w_{n-1}). Bigram: P(w_n|w_{n-1}). Smoothing (Laplace, Kneser-Ney) handles unseen n-grams.",
    example="Bigram P('the'|'in') = count('in the') / count('in') = 500/1000 = 0.5.",
    tier=5, domain="nlp",
    source="Wikipedia contributors, 'Language model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Language_model#N-gram",
    prerequisites=["conditional_prob"],
))

register_atom(Atom(
    atom_type="formula", name="bleu_score",
    content="BLEU measures translation quality by comparing n-gram precision to references. BLEU = BP * exp(sum(w_n * log(p_n))), where p_n is modified n-gram precision and BP is brevity penalty: BP = min(1, exp(1 - r/c)), r = reference length, c = candidate length.",
    example="Candidate: 'the cat sat'. Reference: 'the cat sat on the mat'. Unigram precision: 3/3 = 1.0. Bigram: 2/2 = 1.0. BP = exp(1-6/3) = exp(-1) = 0.368. BLEU-2 = 0.368.",
    tier=5, domain="nlp",
    source="Wikipedia contributors, 'BLEU', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BLEU",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula", name="perplexity",
    content="Perplexity measures how well a language model predicts text: PP = 2^(-1/N * sum(log2(P(w_i)))). Lower perplexity = better model. Equivalent to the weighted average branching factor. For a uniform distribution over V words: PP = V.",
    example="Model assigns P(w1)=0.5, P(w2)=0.25, P(w3)=0.25. PP = 2^(-1/3 * (log2(0.5)+log2(0.25)+log2(0.25))) = 2^(-1/3*(-1-2-2)) = 2^(5/3) = 3.175.",
    tier=5, domain="nlp",
    source="Wikipedia contributors, 'Perplexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perplexity",
    prerequisites=["info_entropy"],
))

# ---------------------------------------------------------------------------
# Nonparametric statistics (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="method", name="mann_whitney_u",
    content="The Mann-Whitney U test is a nonparametric test comparing two independent samples. Rank all observations together. U = n1*n2 + n1*(n1+1)/2 - R1, where R1 is the rank sum of group 1. Small U indicates different distributions. Normal approximation for large samples.",
    example="Group A: [3,5,7] ranks [2,4,5]. Group B: [1,4,8] ranks [1,3,6]. R1=11. U=3*3+3*4/2-11=9+6-11=4.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Mann-Whitney U test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test",
    prerequisites=["hypothesis_test"],
))

register_atom(Atom(
    atom_type="method", name="kruskal_wallis",
    content="The Kruskal-Wallis test is a nonparametric one-way ANOVA. Rank all observations, compute H = (12/(N(N+1))) * sum(R_i^2/n_i) - 3(N+1), where R_i is rank sum and n_i is group size. H follows chi-squared with k-1 df under H0.",
    example="3 groups, N=12. H = 12/(12*13) * (R1^2/4 + R2^2/4 + R3^2/4) - 39. If H > chi2_crit(2), reject H0.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Kruskal-Wallis one-way analysis of variance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_one-way_analysis_of_variance",
    prerequisites=["mann_whitney_u"],
))

register_atom(Atom(
    atom_type="method", name="permutation_test",
    content="A permutation test assesses significance by computing the test statistic for all (or many random) permutations of the data labels. The p-value is the proportion of permuted statistics as extreme as the observed. No distributional assumptions required.",
    example="Observed mean difference = 5. 10000 random permutations: 300 have |diff| >= 5. p-value = 300/10000 = 0.03.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Resampling (statistics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Resampling_(statistics)#Permutation_tests",
    prerequisites=["hypothesis_test"],
))

register_atom(Atom(
    atom_type="method", name="bootstrap_ci",
    content="Bootstrap confidence intervals: resample with replacement B times, compute the statistic for each resample. The percentile method uses the alpha/2 and 1-alpha/2 quantiles of the bootstrap distribution. BCa method adjusts for bias and skewness.",
    example="Data: [2,4,6,8]. B=1000 bootstrap means. 2.5th percentile = 3.0, 97.5th = 7.0. 95% CI: [3.0, 7.0].",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Bootstrapping (statistics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bootstrapping_(statistics)",
    prerequisites=["confidence_interval"],
))

# ---------------------------------------------------------------------------
# Dimensionality reduction (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm", name="pca_compute",
    content="PCA: centre data, compute covariance matrix, find eigenvalues/eigenvectors. Project onto top k eigenvectors. Variance explained = lambda_k / sum(lambda_i). First PC captures maximum variance direction.",
    example="2D data, eigenvalues [4.5, 0.5]. PC1 explains 4.5/5.0 = 90%. Projecting onto PC1 reduces to 1D with 90% variance retained.",
    tier=5, domain="ml",
    source="Wikipedia contributors, 'Principal component analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Principal_component_analysis",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="algorithm", name="svd_truncated",
    content="Truncated SVD: A ~ U_k * Sigma_k * V_k^T, keeping only top k singular values. Optimal rank-k approximation (Eckart-Young theorem). Used for dimensionality reduction, latent semantic analysis, and matrix completion.",
    example="A (100x50), rank 50. Keep k=10: A_10 = U_10 * diag(s_1..s_10) * V_10^T. Reconstruction error = sum(s_11^2..s_50^2).",
    tier=6, domain="ml",
    source="Wikipedia contributors, 'Singular value decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Singular_value_decomposition#Truncated_SVD",
    prerequisites=["singular_value_decomp"],
))

register_atom(Atom(
    atom_type="formula", name="explained_variance",
    content="Explained variance ratio for PCA component k: EVR_k = lambda_k / sum(lambda_i). Cumulative EVR determines how many components to keep. Typical threshold: 95% cumulative variance. Scree plot visualises the eigenvalue decay.",
    example="Eigenvalues: [10, 5, 2, 1, 0.5]. Total = 18.5. EVR = [54.1%, 27%, 10.8%, 5.4%, 2.7%]. Cumulative: 54.1%, 81.1%, 91.9%, 97.3%. Need 4 components for 95%.",
    tier=5, domain="ml",
    source="Wikipedia contributors, 'Principal component analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Principal_component_analysis#Compute_the_cumulative_energy_content",
    prerequisites=["pca_compute"],
))

register_atom(Atom(
    atom_type="method", name="feature_selection",
    content="Feature selection reduces dimensionality by choosing the most informative features. Filter methods: mutual information, chi-squared, variance threshold. Wrapper methods: forward/backward selection using model performance. Embedded: L1 regularisation (Lasso) drives coefficients to zero.",
    example="10 features. Mutual information scores: [0.8, 0.6, 0.01, 0.5, ...]. Select top 3 by MI score.",
    tier=5, domain="ml",
    source="Wikipedia contributors, 'Feature selection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Feature_selection",
    prerequisites=["information_gain"],
))

# ---------------------------------------------------------------------------
# Communication systems (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula", name="am_modulation",
    content="Amplitude modulation: s(t) = [1 + m*cos(2*pi*f_m*t)] * A_c*cos(2*pi*f_c*t), where m is modulation index (0 to 1), f_m is message frequency, f_c is carrier frequency. Bandwidth = 2*f_m. Efficiency = m^2 / (2 + m^2).",
    example="m=0.5, f_c=1 MHz, f_m=5 kHz. BW = 10 kHz. Efficiency = 0.25/2.25 = 11.1%.",
    tier=5, domain="communications",
    source="Wikipedia contributors, 'Amplitude modulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amplitude_modulation",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula", name="quantization",
    content="Uniform quantization maps continuous values to L = 2^n discrete levels. Step size delta = (V_max - V_min) / L. Quantization noise power = delta^2 / 12. Signal-to-quantization-noise ratio SQNR = 6.02*n + 1.76 dB for n-bit quantization.",
    example="8-bit quantizer, range [-1V, 1V]. L=256, delta=2/256=7.8125 mV. SQNR = 6.02*8+1.76 = 49.92 dB.",
    tier=5, domain="communications",
    source="Wikipedia contributors, 'Quantization (signal processing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantization_(signal_processing)",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="concept", name="companding",
    content="Companding (compressing-expanding) reduces the dynamic range before quantization, improving SNR for low-level signals. mu-law: F(x) = sgn(x)*ln(1+mu*|x|)/ln(1+mu). A-law used in Europe (ITU G.711). Typically mu=255 (North America) or A=87.6 (Europe).",
    example="mu-law, mu=255, x=0.1: F(0.1) = ln(1+25.5)/ln(256) = ln(26.5)/5.545 = 3.277/5.545 = 0.591. Expansion at low levels.",
    tier=5, domain="communications",
    source="Wikipedia contributors, 'Companding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/%CE%9C-law_algorithm",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="concept", name="constellation_diagram",
    content="A constellation diagram plots the in-phase (I) and quadrature (Q) components of a digital modulation scheme. BPSK: 2 points on real axis. QPSK: 4 points at 45/135/225/315 degrees. 16-QAM: 16 points in a 4x4 grid. Symbol error rate depends on minimum distance between points.",
    example="QPSK: symbols at (1,1),(-1,1),(-1,-1),(1,-1). Min distance = 2. BER ~ Q(sqrt(2*Eb/N0)).",
    tier=5, domain="communications",
    source="Wikipedia contributors, 'Constellation diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Constellation_diagram",
    prerequisites=["modulation_bpsk"],
))

# ---------------------------------------------------------------------------
# Information geometry (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula", name="fisher_information",
    content="The Fisher information matrix I(theta)_ij = E[d(log f)/d(theta_i) * d(log f)/d(theta_j)]. For a single parameter: I(theta) = -E[d^2 log f / d theta^2]. The Cramer-Rao bound: Var(theta_hat) >= 1/I(theta). Fisher information is a Riemannian metric on the statistical manifold.",
    example="Bernoulli(p): log f = x*log(p) + (1-x)*log(1-p). I(p) = 1/(p*(1-p)). At p=0.5: I=4. Cramer-Rao: Var >= 0.25/n.",
    tier=6, domain="information_geometry",
    source="Wikipedia contributors, 'Fisher information', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fisher_information",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="formula", name="natural_gradient",
    content="The natural gradient scales the ordinary gradient by the inverse Fisher information matrix: theta_{t+1} = theta_t - eta * I(theta_t)^{-1} * grad L. This makes updates invariant to reparametrisation, converging faster than standard gradient descent in parameter spaces with non-trivial geometry.",
    example="Exponential family with I = [[2,0],[0,4]], grad = [1,2]. Natural grad = [[0.5,0],[0,0.25]] * [1,2] = [0.5, 0.5]. Step is scaled by curvature.",
    tier=7, domain="information_geometry",
    source="Wikipedia contributors, 'Natural gradient descent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Natural_gradient_descent",
    prerequisites=["fisher_information"],
))

register_atom(Atom(
    atom_type="formula", name="kl_geometry",
    content="KL divergence D_KL(P||Q) = sum(P(x)*log(P(x)/Q(x))) is not symmetric and not a true metric. However, for infinitesimally close distributions, d_KL(theta, theta+dtheta) ~ 0.5 * dtheta^T * I(theta) * dtheta, connecting KL divergence to the Fisher information metric.",
    example="P = Bernoulli(0.5), Q = Bernoulli(0.6). D_KL = 0.5*log(0.5/0.6) + 0.5*log(0.5/0.4) = -0.0912 + 0.1116 = 0.0204.",
    tier=7, domain="information_geometry",
    source="Wikipedia contributors, 'Information geometry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Information_geometry",
    prerequisites=["kl_divergence"],
))

register_atom(Atom(
    atom_type="concept", name="exponential_family",
    content="An exponential family distribution has the form f(x|theta) = h(x)*exp(eta(theta)^T * T(x) - A(theta)), where T(x) is sufficient statistic, eta is natural parameter, and A(theta) is log-normalizer. Properties: E[T(x)] = dA/d eta, Var[T(x)] = d^2 A/d eta^2. Bernoulli, Gaussian, Poisson are all exponential family.",
    example="Bernoulli(p): h(x)=1, eta=log(p/(1-p)), T(x)=x, A=log(1+exp(eta))=-log(1-p).",
    tier=6, domain="information_geometry",
    source="Wikipedia contributors, 'Exponential family', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exponential_family",
    prerequisites=["maximum_likelihood"],
))

# ---------------------------------------------------------------------------
# Fuzzy logic (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept", name="membership_function",
    content="A fuzzy membership function mu(x) maps a crisp value x to a degree of membership in [0,1]. Common shapes: triangular (a,m,b), trapezoidal (a,b,c,d), Gaussian (mean, sigma). mu(x) = 0 means 'not a member', 1 means 'fully member'.",
    example="'Warm' temperature: triangular(15,25,35). At T=20: mu = (20-15)/(25-15) = 0.5. At T=25: mu = 1.0.",
    tier=5, domain="fuzzy_logic",
    source="Wikipedia contributors, 'Membership function (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Membership_function_(mathematics)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula", name="fuzzy_operations",
    content="Fuzzy set operations: AND (min): mu_A_AND_B(x) = min(mu_A(x), mu_B(x)). OR (max): mu_A_OR_B(x) = max(mu_A(x), mu_B(x)). NOT: mu_NOT_A(x) = 1 - mu_A(x). T-norms and S-norms generalise AND/OR.",
    example="mu_A(x) = 0.7, mu_B(x) = 0.4. A AND B = min(0.7, 0.4) = 0.4. A OR B = max(0.7, 0.4) = 0.7. NOT A = 0.3.",
    tier=5, domain="fuzzy_logic",
    source="Wikipedia contributors, 'Fuzzy set operations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fuzzy_set#Fuzzy_set_operations",
    prerequisites=["membership_function"],
))

register_atom(Atom(
    atom_type="algorithm", name="fuzzy_inference",
    content="Mamdani fuzzy inference: (1) fuzzify inputs, (2) evaluate rules (IF x IS A AND y IS B THEN z IS C), (3) aggregate rule outputs, (4) defuzzify. Rule strength = min of antecedent membership values. Output fuzzy set is clipped or scaled by rule strength.",
    example="Rule: IF temp IS hot AND humidity IS high THEN fan IS fast. mu_hot(30) = 0.8, mu_high(85) = 0.6. Rule strength = min(0.8, 0.6) = 0.6. Fan 'fast' clipped at 0.6.",
    tier=5, domain="fuzzy_logic",
    source="Wikipedia contributors, 'Fuzzy control system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fuzzy_control_system",
    prerequisites=["fuzzy_operations"],
))

register_atom(Atom(
    atom_type="method", name="defuzzification",
    content="Defuzzification converts a fuzzy output to a crisp value. Centre of gravity (COG): x* = integral(x*mu(x)dx) / integral(mu(x)dx). Centre of area (COA): bisects the area. Mean of maximum (MOM): average of x values where mu is maximum.",
    example="Triangular output clipped at 0.6 over [0,10]. COG ~ weighted centroid. If uniform clip: x* = 5 (centre).",
    tier=5, domain="fuzzy_logic",
    source="Wikipedia contributors, 'Defuzzification', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Defuzzification",
    prerequisites=["fuzzy_inference"],
))

# ---------------------------------------------------------------------------
# Compressed sensing (tier 6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept", name="rip_condition",
    content="The Restricted Isometry Property (RIP): a matrix A satisfies RIP of order s if (1-delta_s)*||x||^2 <= ||Ax||^2 <= (1+delta_s)*||x||^2 for all s-sparse x. If delta_{2s} < sqrt(2)-1, then L1 minimisation exactly recovers s-sparse signals from m = O(s*log(n/s)) measurements.",
    example="n=100 signal, s=5 sparse. Need m ~ 5*log(100/5)*C ~ 5*3*C ~ 50 measurements (with constant C).",
    tier=6, domain="compressed_sensing",
    source="Wikipedia contributors, 'Restricted isometry property', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Restricted_isometry_property",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm", name="sparse_recovery",
    content="Sparse recovery reconstructs a sparse signal x from underdetermined measurements y = Ax. L1 minimisation (basis pursuit): min ||x||_1 subject to Ax = y. Greedy algorithms: OMP (orthogonal matching pursuit) iteratively selects columns of A most correlated with the residual.",
    example="A is 50x100, y = Ax where x has 5 nonzero entries. OMP: 5 iterations, each selecting the column of A most correlated with current residual.",
    tier=6, domain="compressed_sensing",
    source="Wikipedia contributors, 'Compressed sensing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compressed_sensing",
    prerequisites=["rip_condition"],
))

register_atom(Atom(
    atom_type="algorithm", name="basis_pursuit",
    content="Basis pursuit solves min ||x||_1 subject to Ax = y (or Ax ~ y for noisy case: basis pursuit denoising). Equivalent to a linear program. Under RIP, recovers the sparsest solution. LASSO formulation: min ||y-Ax||^2 + lambda*||x||_1.",
    example="A (50x100), y measured. Solve LP: minimise sum|x_i| subject to Ax=y. Solution has ~5 nonzero components.",
    tier=6, domain="compressed_sensing",
    source="Wikipedia contributors, 'Basis pursuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Basis_pursuit",
    prerequisites=["sparse_recovery"],
))

register_atom(Atom(
    atom_type="formula", name="coherence",
    content="The coherence of a matrix A is mu(A) = max_{i!=j} |<a_i, a_j>| / (||a_i||*||a_j||), the maximum absolute normalised inner product between columns. Lower coherence -> better sparse recovery. Random matrices have coherence ~ O(sqrt(log(n)/m)). Coherence bounds recovery: s < (1+1/mu)/2.",
    example="A with columns in R^50. mu = 0.1. Recovery guaranteed for s < (1+10)/2 = 5.5, so s <= 5.",
    tier=6, domain="compressed_sensing",
    source="Wikipedia contributors, 'Mutual coherence (linear algebra)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mutual_coherence_(linear_algebra)",
    prerequisites=["dot_product"],
))

# ---------------------------------------------------------------------------
# Remaining small modules
# ---------------------------------------------------------------------------

# Time series (tier 5)

register_atom(Atom(
    atom_type="formula", name="autocorrelation",
    content="The autocorrelation function rho(k) = Cov(X_t, X_{t+k}) / Var(X_t) measures linear dependence at lag k. For an AR(1) process X_t = phi*X_{t-1} + e_t: rho(k) = phi^k. The partial autocorrelation (PACF) removes intermediate lag effects.",
    example="AR(1) with phi=0.8: rho(1)=0.8, rho(2)=0.64, rho(3)=0.512. Exponential decay.",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Autocorrelation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Autocorrelation",
    prerequisites=["correlation"],
))

register_atom(Atom(
    atom_type="formula", name="exponential_smoothing",
    content="Simple exponential smoothing: S_t = alpha*X_t + (1-alpha)*S_{t-1}, where alpha in (0,1) is the smoothing factor. Higher alpha gives more weight to recent observations. Holt's method adds trend: b_t = beta*(S_t-S_{t-1}) + (1-beta)*b_{t-1}.",
    example="alpha=0.3, X=[10,12,11,13]. S_0=10. S_1=0.3*12+0.7*10=10.6. S_2=0.3*11+0.7*10.6=10.72. S_3=0.3*13+0.7*10.72=11.404.",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Exponential smoothing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exponential_smoothing",
    prerequisites=["weighted_sum"],
))

register_atom(Atom(
    atom_type="formula", name="moving_average",
    content="Simple moving average: MA_t = (1/k)*sum(X_{t-k+1}..X_t). Smooths short-term fluctuations. Weighted moving average assigns different weights. Exponential moving average is a special case. MA is a low-pass filter in frequency domain.",
    example="k=3, data [2,4,6,8,10]. MA_3=4, MA_4=6, MA_5=8.",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Moving average', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Moving_average",
    prerequisites=["arithmetic_mean"],
))

register_atom(Atom(
    atom_type="algorithm", name="arima_forecast",
    content="ARIMA(p,d,q): AutoRegressive Integrated Moving Average. AR(p): X_t = sum(phi_i*X_{t-i}) + e_t. MA(q): X_t = e_t + sum(theta_j*e_{t-j}). I(d): difference d times to achieve stationarity. Box-Jenkins method: identify (ACF/PACF), estimate, diagnose.",
    example="ARIMA(1,1,0): first difference, then AR(1). dX_t = 0.8*dX_{t-1} + e_t. Forecast: dX_{T+1} = 0.8*dX_T.",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Autoregressive integrated moving average', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average",
    prerequisites=["autocorrelation"],
))

register_atom(Atom(
    atom_type="method", name="seasonal_decompose",
    content="Time series decomposition separates a series into trend (T), seasonal (S), and residual (R) components. Additive: Y = T + S + R. Multiplicative: Y = T * S * R. Methods: moving average for trend, then seasonal averages.",
    example="Monthly sales with yearly seasonality. MA(12) extracts trend. Seasonal = original/trend (multiplicative). Residual = original/(trend*seasonal).",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Decomposition of time series', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Decomposition_of_time_series",
    prerequisites=["moving_average"],
))

register_atom(Atom(
    atom_type="concept", name="stationarity_check",
    content="A stationary time series has constant mean, variance, and autocorrelation over time. Tests: Augmented Dickey-Fuller (ADF) tests for unit root (non-stationarity). KPSS tests for stationarity. Differencing (d times) can transform non-stationary to stationary.",
    example="ADF test: H0 = unit root (non-stationary). p-value = 0.03 < 0.05 -> reject H0 -> series is stationary.",
    tier=5, domain="time_series",
    source="Wikipedia contributors, 'Stationary process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stationary_process",
    prerequisites=["autocorrelation"],
))

# Bayesian statistics (tier 5-6)

register_atom(Atom(
    atom_type="concept", name="conjugate_prior",
    content="A conjugate prior is a prior distribution that, combined with a particular likelihood, yields a posterior of the same family. Beta-Binomial: Beta(a,b) prior + Binomial data -> Beta(a+k, b+n-k) posterior. Normal-Normal: known variance, prior N(mu_0,sigma_0^2) + data -> N(mu_n, sigma_n^2).",
    example="Prior Beta(1,1) (uniform). 10 trials, 7 successes. Posterior Beta(1+7, 1+3) = Beta(8,4). Posterior mean = 8/12 = 0.667.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Conjugate prior', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjugate_prior",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="formula", name="posterior_predictive",
    content="The posterior predictive distribution integrates out the parameter: P(x_new|data) = integral(P(x_new|theta)*P(theta|data) dtheta). For Beta-Binomial: posterior predictive of next trial is Beta-Binomial. Accounts for parameter uncertainty.",
    example="Posterior Beta(8,4). P(next success) = E[theta|data] = 8/12 = 0.667.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Posterior predictive distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Posterior_predictive_distribution",
    prerequisites=["conjugate_prior"],
))

register_atom(Atom(
    atom_type="formula", name="credible_interval",
    content="A Bayesian credible interval [a,b] has P(a <= theta <= b | data) = 1-alpha. Unlike frequentist CI, it directly gives the probability that the parameter is in the interval. Highest Density Interval (HDI) is the narrowest such interval.",
    example="Posterior Beta(8,4). 95% credible interval: [0.38, 0.89]. There's a 95% probability theta is in this range.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Credible interval', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Credible_interval",
    prerequisites=["conjugate_prior"],
))

register_atom(Atom(
    atom_type="formula", name="bayes_factor",
    content="The Bayes factor BF_{12} = P(data|M_1)/P(data|M_2) compares two models. BF > 3: moderate evidence for M1. BF > 10: strong. BF > 100: decisive. P(data|M) = integral(P(data|theta,M)*P(theta|M) dtheta) is the marginal likelihood.",
    example="Model 1: P(data|M1) = 0.03. Model 2: P(data|M2) = 0.001. BF = 30. Strong evidence for M1.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Bayes factor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bayes_factor",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="method", name="map_estimate",
    content="The Maximum A Posteriori estimate maximises the posterior: theta_MAP = argmax P(theta|data) = argmax P(data|theta)*P(theta). With a uniform prior, MAP = MLE. With Gaussian prior, MAP = ridge regression. With Laplace prior, MAP = lasso.",
    example="Bernoulli data: 7/10 successes. Uniform prior Beta(1,1). MAP = argmax Beta(8,4) = (8-1)/(8+4-2) = 7/10 = 0.7.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Maximum a posteriori estimation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="method", name="empirical_bayes",
    content="Empirical Bayes estimates hyperparameters of the prior from the data itself: theta_EB = argmax P(data|theta) where P(data|theta) = integral P(data|psi)*P(psi|theta) dpsi. Shrinks individual estimates towards the group mean. Used when many similar parameters are estimated simultaneously.",
    example="100 batting averages. Empirical Bayes prior Beta(a,b) estimated from data. Each player's estimate shrunk towards the overall average.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Empirical Bayes method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Empirical_Bayes_method",
    prerequisites=["map_estimate"],
))

# Causal inference (tier 5-6)

register_atom(Atom(
    atom_type="formula", name="ate_compute",
    content="The Average Treatment Effect ATE = E[Y(1)] - E[Y(0)] = E[Y|T=1] - E[Y|T=0] under unconfoundedness. With confounders X: ATE = E_X[E[Y|T=1,X] - E[Y|T=0,X]]. Estimated via regression, matching, or inverse propensity weighting.",
    example="Treated group mean outcome = 75. Control group mean = 60. Naive ATE = 15. After adjusting for confounder: ATE = 10.",
    tier=5, domain="statistics",
    source="Wikipedia contributors, 'Average treatment effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Average_treatment_effect",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="method", name="propensity_score",
    content="Propensity score e(X) = P(T=1|X) is the probability of treatment given covariates. Rosenbaum & Rubin: conditioning on e(X) removes confounding bias. Methods: stratification, matching, or inverse probability weighting: ATE = E[Y*T/e(X)] - E[Y*(1-T)/(1-e(X))].",
    example="Logistic regression: e(X) = 1/(1+exp(-(0.5*age - 2*income + 1))). Match treated (e=0.7) with control (e=0.68). Estimate ATE from matched pairs.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Propensity score matching', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Propensity_score_matching",
    prerequisites=["logistic_regression_compute"],
))

register_atom(Atom(
    atom_type="method", name="instrumental_variable",
    content="An instrumental variable Z affects treatment T but has no direct effect on outcome Y (only through T). IV estimates: beta_IV = Cov(Y,Z)/Cov(T,Z). Two-stage least squares: (1) regress T on Z, get T_hat, (2) regress Y on T_hat. Requires instrument relevance and exclusion restriction.",
    example="Z = distance to hospital, T = treatment received, Y = health outcome. beta_IV = Cov(Y,distance)/Cov(T,distance).",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Instrumental variables estimation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instrumental_variables_estimation",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="method", name="diff_in_diff",
    content="Difference-in-differences estimates causal effects by comparing pre/post changes between treated and control groups. DiD = (Y_treat_post - Y_treat_pre) - (Y_control_post - Y_control_pre). Assumes parallel trends: without treatment, both groups would have changed equally.",
    example="Pre: treated=50, control=40. Post: treated=70, control=55. DiD = (70-50)-(55-40) = 20-15 = 5.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Difference in differences', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Difference_in_differences",
    prerequisites=["subtraction"],
))

register_atom(Atom(
    atom_type="method", name="regression_discontinuity",
    content="Regression discontinuity design exploits a sharp cutoff in treatment assignment. Units just above the cutoff are treated; those just below are not. The causal effect is estimated as the jump in outcome at the cutoff. Local polynomial regression near the cutoff estimates the discontinuity.",
    example="Scholarship awarded if score >= 80. Compare outcomes of students scoring 79 vs 81. Jump at 80 = causal effect of scholarship.",
    tier=6, domain="statistics",
    source="Wikipedia contributors, 'Regression discontinuity design', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regression_discontinuity_design",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="framework", name="do_calculus",
    content="Pearl's do-calculus provides rules for identifying causal effects from observational data using a causal DAG. The do-operator: P(Y|do(X)) removes incoming edges to X. Three rules handle insertion/deletion of observations, interventions, and conditional independence. A causal effect is identifiable if do-calculus can express P(Y|do(X)) in terms of observational distributions.",
    example="DAG: Z->X->Y, Z->Y. P(Y|do(X)) = sum_Z P(Y|X,Z)*P(Z) (back-door adjustment). Confounding by Z is removed.",
    tier=7, domain="statistics",
    source="Wikipedia contributors, 'Do-calculus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Do_calculus",
    prerequisites=["ate_compute"],
))

# ---------------------------------------------------------------------------
# Remaining small modules (4-6 atoms each)
# ---------------------------------------------------------------------------

# Wavelet theory (tier 5-6)
register_atom(Atom(atom_type="algorithm", name="haar_wavelet_decompose", content="Haar wavelet decomposition: averages (a) and differences (d) of adjacent pairs. Level 1: a_k = (x_{2k}+x_{2k+1})/2, d_k = (x_{2k}-x_{2k+1})/2. Recursively decompose averages. Perfect reconstruction: x_{2k} = a_k+d_k, x_{2k+1} = a_k-d_k.", example="[4,6,10,2]. Averages: [5,6]. Differences: [-1,4]. Next level: avg [5.5], diff [-0.5]. Decomposition: [5.5, -0.5, -1, 4].", tier=5, domain="wavelet_theory", source="Wikipedia contributors, 'Haar wavelet', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Haar_wavelet", prerequisites=["arithmetic_mean"]))

register_atom(Atom(atom_type="algorithm", name="haar_reconstruct", content="Haar wavelet reconstruction (inverse transform): from decomposition coefficients, reconstruct signal by reversing the decomposition. At each level: x_{2k} = a_k + d_k, x_{2k+1} = a_k - d_k. Start from coarsest level, work to finest.", example="Decomposition: [5.5, -0.5, -1, 4]. Level 1: a=[5.5-(-0.5), 5.5+(-0.5)] = [6,5] err -> [5,6]. Level 0: [5+(-1), 5-(-1), 6+4, 6-4] = [4,6,10,2].", tier=5, domain="wavelet_theory", source="Wikipedia contributors, 'Haar wavelet', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Haar_wavelet", prerequisites=["haar_wavelet_decompose"]))

register_atom(Atom(atom_type="concept", name="multiresolution", content="Multiresolution analysis (MRA) provides a framework for wavelet theory: a nested sequence of subspaces V_0 subset V_1 subset ... with a scaling function phi and wavelet psi. V_j captures features at scale 2^j. The wavelet space W_j = V_{j+1} - V_j captures details between scales.", example="Image compression: V_0 = thumbnail (low frequency). W_0 = details needed for full resolution. Keep V_0 + large W_0 coefficients, discard small ones.", tier=6, domain="wavelet_theory", source="Wikipedia contributors, 'Multiresolution analysis', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Multiresolution_analysis", prerequisites=["haar_wavelet_decompose"]))

register_atom(Atom(atom_type="formula", name="wavelet_energy", content="Wavelet energy at scale j: E_j = sum(|d_j,k|^2). Total energy is preserved: sum(E_j) + |a_J|^2 = sum(|x_k|^2) (Parseval's theorem). Energy distribution across scales reveals signal characteristics: concentrated at fine scales for sharp features, coarse for smooth trends.", example="Signal energy: 100. Wavelet: E_1=60 (fine), E_2=30, E_3=10 (coarse). Most energy at fine scale -> signal has sharp features.", tier=5, domain="wavelet_theory", source="Wikipedia contributors, 'Wavelet', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Wavelet#Energy_preservation", prerequisites=["haar_wavelet_decompose"]))

register_atom(Atom(atom_type="concept", name="filter_bank", content="A filter bank implements the discrete wavelet transform: analysis filters (lowpass h0, highpass h1) decompose the signal, followed by downsampling by 2. Synthesis filters reconstruct. Perfect reconstruction requires: H0(z)*G0(z) + H1(z)*G1(z) = 2*z^{-d}.", example="Haar filters: h0 = [1,1]/sqrt(2) (lowpass), h1 = [1,-1]/sqrt(2) (highpass). Convolve signal with filters, downsample by 2.", tier=6, domain="wavelet_theory", source="Wikipedia contributors, 'Filter bank', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Filter_bank", prerequisites=["haar_wavelet_decompose"]))

register_atom(Atom(atom_type="method", name="thresholding", content="Wavelet thresholding for denoising: compute DWT, set small coefficients to zero (hard threshold) or shrink toward zero (soft threshold: sign(d)*(|d|-lambda)+). Universal threshold: lambda = sigma*sqrt(2*log(n)). Preserves significant features while removing noise.", example="Noisy signal, DWT coefficients: [5.2, -3.1, 0.1, -0.05, 4.8]. Threshold lambda=1. Soft: [4.2, -2.1, 0, 0, 3.8]. Hard: [5.2, -3.1, 0, 0, 4.8].", tier=5, domain="wavelet_theory", source="Wikipedia contributors, 'Wavelet shrinkage', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Wavelet_shrinkage", prerequisites=["haar_wavelet_decompose"]))

# RL ext (tier 5)
register_atom(Atom(atom_type="formula", name="td_lambda", content="TD(lambda) combines MC and TD learning: e_t(s) = gamma*lambda*e_{t-1}(s) + I(S_t=s) (eligibility trace). Update: V(s) += alpha*delta_t*e_t(s), where delta_t = R_{t+1} + gamma*V(S_{t+1}) - V(S_t). lambda=0: TD(0), lambda=1: Monte Carlo.", example="lambda=0.9, gamma=0.99. State visited at t=0: e_0=1. At t=1: e_0=0.891. TD error propagates back through trace.", tier=5, domain="reinforcement_learning", source="Wikipedia contributors, 'Temporal difference learning', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Temporal_difference_learning#TD-Lambda", prerequisites=["bellman_equation"]))

register_atom(Atom(atom_type="formula", name="sarsa_update", content="SARSA is an on-policy TD control algorithm: Q(S_t,A_t) += alpha*(R_{t+1} + gamma*Q(S_{t+1},A_{t+1}) - Q(S_t,A_t)). The name comes from (S,A,R,S',A'). Learns the value of the policy being followed, including exploration.", example="Q(s1,right)=5, R=1, Q(s2,up)=8, gamma=0.9, alpha=0.1. Update: Q(s1,right) += 0.1*(1+0.9*8-5) = 5+0.1*3.2 = 5.32.", tier=5, domain="reinforcement_learning", source="Wikipedia contributors, 'State-action-reward-state-action', Wikipedia.", source_url="https://en.wikipedia.org/wiki/State%E2%80%93action%E2%80%93reward%E2%80%93state%E2%80%93action", prerequisites=["q_value_update"]))

register_atom(Atom(atom_type="formula", name="policy_gradient_reinforce", content="REINFORCE policy gradient: nabla J(theta) = E[sum_t(nabla log pi(a_t|s_t,theta) * G_t)], where G_t is return from step t. Update: theta += alpha*G_t*nabla log pi. High variance; reduced by subtracting a baseline b(s): nabla J = E[(G_t - b)*nabla log pi].", example="Episode return G=10. Policy pi(a|s,theta) = softmax. nabla log pi = [0.3, -0.3]. Update: theta += 0.01*10*[0.3,-0.3] = [0.03,-0.03].", tier=5, domain="reinforcement_learning", source="Wikipedia contributors, 'REINFORCE', Wikipedia.", source_url="https://en.wikipedia.org/wiki/REINFORCE_(algorithm)", prerequisites=["gradient_descent"]))

register_atom(Atom(atom_type="algorithm", name="bandit_ucb", content="Upper Confidence Bound (UCB1) for multi-armed bandits: select arm with highest UCB = Q_a + c*sqrt(ln(t)/N_a), where Q_a is estimated value, t is total plays, N_a is plays of arm a, c controls exploration. Achieves O(sqrt(K*T*ln(T))) regret.", example="3 arms, t=100, Q=[0.5,0.3,0.7], N=[40,30,30], c=2. UCB = [0.5+0.43, 0.3+0.49, 0.7+0.49] = [0.93, 0.79, 1.19]. Select arm 3.", tier=5, domain="reinforcement_learning", source="Wikipedia contributors, 'Multi-armed bandit', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Multi-armed_bandit#Upper_confidence_bounds", prerequisites=["logarithm"]))

# Queuing ext, game_theory_ext, etc. handled similarly with concise atoms

# Queuing ext (tier 5-6)
register_atom(Atom(atom_type="formula", name="erlang_b", content="Erlang B formula gives the blocking probability in a loss system with c servers and offered load A (Erlangs): B(c,A) = (A^c/c!) / sum_{k=0}^{c}(A^k/k!). Used in telecom to dimension trunk groups. No queuing: blocked calls are lost.", example="c=3 servers, A=2 Erlangs. B(3,2) = (8/6)/(1+2+2+1.333) = 1.333/6.333 = 0.211. 21.1% of calls blocked.", tier=5, domain="queuing_theory", source="Wikipedia contributors, 'Erlang B formula', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Erlang_B_formula", prerequisites=["factorial"]))

register_atom(Atom(atom_type="formula", name="erlang_c", content="Erlang C gives the probability of queuing (waiting) in a system with c servers and offered load A < c: C(c,A) = B(c,A)*c/(c-A*(1-B(c,A))). Average wait for queued calls: W = C(c,A)*service_time / (c-A). Used for call centres.", example="c=5 servers, A=4 Erlangs, service time 3 min. C(5,4) ~ 0.174. Average wait ~ 0.174*3/(5-4) = 0.522 min.", tier=5, domain="queuing_theory", source="Wikipedia contributors, 'Erlang C formula', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Erlang_C_formula", prerequisites=["erlang_b"]))

register_atom(Atom(atom_type="formula", name="littles_law", content="Little's law: L = lambda * W, where L is average number in system, lambda is arrival rate, W is average time in system. Also: L_q = lambda * W_q (queue only). Universal law: holds for any queueing discipline, any arrival/service distributions.", example="lambda=10 customers/hr, W=0.5 hr. L=10*0.5=5 customers in system on average.", tier=5, domain="queuing_theory", source="Wikipedia contributors, 'Little's law', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Little%27s_law", prerequisites=["multiplication"]))

register_atom(Atom(atom_type="formula", name="mg1_queue", content="M/G/1 queue (Poisson arrivals, general service, 1 server). Pollaczek-Khinchine formula: L_q = (rho^2*(1+C_s^2))/(2*(1-rho)), where rho=lambda/mu, C_s=sigma_s/E[S] is coefficient of variation of service time. If C_s=1 (exponential): reduces to M/M/1 formula.", example="lambda=8/hr, E[S]=6 min=0.1 hr, sigma_s=3 min. rho=0.8, C_s=0.5. L_q = (0.64*1.25)/(2*0.2) = 0.8/0.4 = 2 customers.", tier=6, domain="queuing_theory", source="Wikipedia contributors, 'M/G/1 queue', Wikipedia.", source_url="https://en.wikipedia.org/wiki/M/G/1_queue", prerequisites=["mm1_queue"]))

register_atom(Atom(atom_type="concept", name="jackson_network", content="A Jackson network is an open network of queuing nodes where arrivals are Poisson and service is exponential. Product form solution: P(n1,...,nK) = prod P_k(n_k), where each node behaves as an independent M/M/c queue. Arrival rate at each node found by solving traffic equations.", example="3-node network. External arrivals: lambda_1=5. Routing: 50% from node 1 to node 2, 50% exit. lambda_2=2.5. Each node analysed independently.", tier=6, domain="queuing_theory", source="Wikipedia contributors, 'Jackson network', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Jackson_network", prerequisites=["mg1_queue"]))

register_atom(Atom(atom_type="concept", name="priority_queue", content="Priority queuing serves higher-priority customers first. Preemptive: interrupt current service for higher priority arrival. Non-preemptive: finish current service, then serve highest priority. W_k (wait for class k) depends on traffic from all higher-priority classes.", example="Two priority classes. rho_1=0.3, rho_2=0.4. Class 1 (high) wait: W_1 = W_0/(1-rho_1). Class 2: W_2 = W_0/((1-rho_1)*(1-rho_1-rho_2)).", tier=5, domain="queuing_theory", source="Wikipedia contributors, 'Priority queue (queueing theory)', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Priority_queue_(queueing_theory)", prerequisites=["mm1_queue"]))

# Game theory ext (tier 5-6)
register_atom(Atom(atom_type="concept", name="extensive_form", content="Extensive form games are represented as game trees with nodes (decision points), branches (actions), and leaves (payoffs). Perfect information: all players know prior moves. Imperfect: information sets group indistinguishable nodes. Solve by backward induction (perfect info) or behavioral strategies.", example="Sequential game: Player 1 chooses L or R. If L, Player 2 chooses U or D. Payoffs at leaves. Backward induction from leaves.", tier=5, domain="game_theory", source="Wikipedia contributors, 'Extensive-form game', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Extensive-form_game", prerequisites=["minimax"]))

register_atom(Atom(atom_type="concept", name="repeated_game", content="In a repeated game, players play the same stage game multiple times. Folk theorem: any feasible, individually rational payoff can be sustained as a Nash equilibrium of the infinitely repeated game (with sufficiently high discount factor). Cooperation can emerge through trigger strategies (e.g., grim trigger).", example="Repeated Prisoner's Dilemma: cooperate if partner cooperated; defect forever if partner defects (grim trigger). Sustains cooperation when delta > (T-R)/(T-P).", tier=6, domain="game_theory", source="Wikipedia contributors, 'Repeated game', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Repeated_game", prerequisites=["nash_equilibrium"]))

register_atom(Atom(atom_type="concept", name="bayesian_game", content="A Bayesian game includes incomplete information: players have private types drawn from a known distribution. Players maximise expected utility given their type and beliefs about others' types. Bayesian Nash equilibrium: each type's strategy is optimal given beliefs and other types' strategies.", example="Auction: each bidder's valuation is private, drawn from U[0,1]. First-price: BNE bid = (n-1)/n * value. With 2 bidders: bid half your value.", tier=6, domain="game_theory", source="Wikipedia contributors, 'Bayesian game', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Bayesian_game", prerequisites=["nash_equilibrium"]))

register_atom(Atom(atom_type="concept", name="correlated_equilibrium", content="A correlated equilibrium uses a public signal (correlation device) to coordinate players. A mediator privately recommends actions. If no player benefits from deviating from the recommendation, it's a CE. Every Nash equilibrium is a CE; the set of CEs is convex and often yields higher payoffs.", example="Traffic game: mediator tells one driver to go and the other to wait. Neither wants to deviate. Better than the mixed Nash where both sometimes crash.", tier=6, domain="game_theory", source="Wikipedia contributors, 'Correlated equilibrium', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Correlated_equilibrium", prerequisites=["nash_equilibrium"]))

register_atom(Atom(atom_type="formula", name="shapley_value", content="The Shapley value distributes a cooperative game's worth fairly. Player i's value: phi_i = sum over coalitions S not containing i: (|S|!*(n-|S|-1)!/n!) * (v(S union {i}) - v(S)). Properties: efficiency (sum = total value), symmetry, null player gets 0, additivity.", example="3 players, v({1})=0, v({2})=0, v({1,2})=6, v({1,2,3})=12. phi_1 considers all coalitions player 1 can join.", tier=5, domain="game_theory", source="Wikipedia contributors, 'Shapley value', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Shapley_value", prerequisites=["permutation"]))

register_atom(Atom(atom_type="concept", name="evolutionary_stable", content="An Evolutionary Stable Strategy (ESS) is a strategy that, if adopted by a population, cannot be invaded by a rare mutant strategy. Condition: E(s,s) > E(s',s) for all s' != s, or E(s,s) = E(s',s) and E(s,s') > E(s',s'). ESS is a refinement of Nash equilibrium in biological contexts.", example="Hawk-Dove game: if V < C, mixed ESS with frequency of Hawks = V/C. Neither pure Hawk nor pure Dove is ESS.", tier=6, domain="game_theory", source="Wikipedia contributors, 'Evolutionarily stable strategy', Wikipedia.", source_url="https://en.wikipedia.org/wiki/Evolutionarily_stable_strategy", prerequisites=["nash_equilibrium"]))
