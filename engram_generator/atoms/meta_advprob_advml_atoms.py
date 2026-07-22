"""Knowledge atoms for meta-reasoning, advanced probability, and advanced ML.

Covers proof synthesis, scaling laws, moment-generating functions,
central limit theorem, multi-head attention, layer normalisation,
and related topics. Each atom stores an authoritative description,
a worked example, and a Wikipedia source URL.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# -----------------------------------------------------------------------
# Meta-reasoning higher (tier 8-10)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="method",
    name="proof_synthesis",
    content=(
        "Proof synthesis is the task of constructing a formal proof of a "
        "given theorem from a set of axioms and available lemmas. In "
        "automated theorem proving, strategies include resolution, "
        "natural deduction, and tableau methods. The prover must select "
        "and chain applicable lemmas to derive the goal statement."
    ),
    example=(
        "Theorem: gcd(a,b) = ax + by for some integers x,y. "
        "Available: division_algorithm, euclidean_algorithm. "
        "Proof: Apply euclidean_algorithm to get gcd, then back-substitute "
        "using division_algorithm remainders to find x, y."
    ),
    tier=8,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Automated theorem proving', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Automated_theorem_proving",
    prerequisites=["natural_deduction"],
))

register_atom(Atom(
    atom_type="method",
    name="conjecture_test",
    content=(
        "Conjecture testing involves generating and evaluating mathematical "
        "conjectures by testing them against known examples and "
        "counterexamples. A conjecture is considered plausible if it holds "
        "for all tested cases and is falsified if any counterexample is "
        "found. Systematic search over parameter spaces can strengthen or "
        "refute conjectures."
    ),
    example=(
        "Conjecture: All primes > 2 are odd. "
        "Test p=3: odd (supports). p=5: odd (supports). p=7: odd (supports). "
        "No counterexample found in primes up to 1000. Conjecture supported."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Conjecture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjecture",
    prerequisites=["primality"],
))

register_atom(Atom(
    atom_type="method",
    name="algorithm_correctness",
    content=(
        "Algorithm correctness verification proves that an algorithm "
        "produces the correct output for all valid inputs. This involves "
        "establishing a loop invariant (a condition true before and after "
        "each iteration), proving termination (the algorithm halts), and "
        "proving partial correctness (if it halts, the output is correct). "
        "Together these establish total correctness."
    ),
    example=(
        "Binary search invariant: target is in arr[lo..hi] if present. "
        "Initially lo=0, hi=n-1 (covers entire array). "
        "Each step halves the range, so hi-lo decreases. "
        "Terminates when lo > hi. Correct because invariant + termination "
        "implies target found or not in array."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Correctness (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Correctness_(computer_science)",
    prerequisites=["loop_invariant_verify"],
))

register_atom(Atom(
    atom_type="method",
    name="computational_tradeoff",
    content=(
        "Computational tradeoff analysis compares data structures or "
        "algorithms by their time and space complexity for different "
        "operation mixes. The optimal choice depends on the workload: "
        "frequent lookups favour hash tables or balanced BSTs, frequent "
        "insertions favour linked lists or skip lists, and mixed "
        "workloads require balancing multiple costs."
    ),
    example=(
        "Compare linked_list vs balanced_bst for n=50000, mostly lookups: "
        "linked_list lookup O(n)=50000, BST lookup O(log n)=16. "
        "BST wins for lookup-heavy workload."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Amortized analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amortized_analysis",
    prerequisites=["big_o"],
))

register_atom(Atom(
    atom_type="method",
    name="model_architecture_critique",
    content=(
        "Architecture critique evaluates a neural network design by "
        "analysing its computational complexity (FLOPs per forward pass), "
        "parameter efficiency, memory footprint, and inductive biases. "
        "Key metrics include parameters per layer, attention complexity "
        "O(n^2 d) for transformers, and the ratio of compute to "
        "representational capacity."
    ),
    example=(
        "Transformer with d=512, h=8, L=6, seq_len=128: "
        "self-attention FLOPs per layer = 4*128*512^2 + 2*128^2*512 = "
        "134M + 16.8M = 151M. Total 6 layers: ~906M FLOPs."
    ),
    tier=10,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Transformer (deep learning architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["attention_multihead"],
))

register_atom(Atom(
    atom_type="formula",
    name="scaling_law_extrapolate",
    content=(
        "Neural scaling laws describe how model performance (loss or "
        "accuracy) scales as a power law with compute, dataset size, "
        "or parameter count: L(N) = C * N^(-alpha), where L is loss, "
        "N is the scaling variable, C is a constant, and alpha is the "
        "scaling exponent. Extrapolation predicts performance at larger "
        "scales by fitting alpha and C from observed data points."
    ),
    example=(
        "Observed: N=1000 -> acc=50.0, N=2000 -> acc=57.4. "
        "alpha = log(57.4/50.0)/log(2000/1000) = log(1.148)/log(2) = 0.20. "
        "C = 50.0/1000^0.20 = 12.55. "
        "Predict N=4000: 12.55 * 4000^0.20 = 65.9."
    ),
    tier=10,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Neural scaling law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Neural_scaling_law",
    prerequisites=["exponentiation", "polynomial_eval"],
))

register_atom(Atom(
    atom_type="method",
    name="error_taxonomy",
    content=(
        "Error taxonomy classifies computational errors by their root "
        "cause: off-by-one errors (boundary conditions), type errors "
        "(incorrect data types), overflow errors (exceeding numeric "
        "limits), rounding errors (floating-point precision), and logic "
        "errors (incorrect algorithm). Systematic classification aids "
        "debugging and prevention."
    ),
    example=(
        "Error in loop 'for i in range(n+1)': iterates n+1 times "
        "instead of n. Classification: off-by-one error. "
        "Fix: range(n) or range(1, n+1) depending on intent."
    ),
    tier=8,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Software bug', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Software_bug",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="method",
    name="method_comparison",
    content=(
        "Method comparison evaluates competing approaches (algorithms, "
        "models, or techniques) on shared criteria: accuracy, "
        "computational cost, interpretability, robustness, and "
        "scalability. A systematic comparison selects the method best "
        "suited to the problem constraints and data characteristics."
    ),
    example=(
        "Compare decision_tree vs neural_network for 1000 samples, "
        "10 features: decision_tree trains in 0.1s, accuracy 85%, "
        "interpretable. neural_network trains in 10s, accuracy 87%, "
        "black-box. For small data + interpretability: decision_tree."
    ),
    tier=8,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Model selection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Model_selection",
    prerequisites=["complexity_analysis"],
))

# -----------------------------------------------------------------------
# Advanced probability (tier 5-7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="moment_generating",
    content=(
        "The moment-generating function (MGF) of a random variable X "
        "is M_X(t) = E[e^(tX)]. The n-th moment of X equals the n-th "
        "derivative of M_X evaluated at t=0: E[X^n] = M_X^(n)(0). "
        "The MGF uniquely determines the distribution when it exists "
        "in a neighbourhood of t=0."
    ),
    example=(
        "Exponential(lambda=2): M_X(t) = lambda/(lambda-t) = 2/(2-t) for t<2. "
        "E[X] = M'(0) = 2/(2-0)^2 = 1/2. "
        "E[X^2] = M''(0) = 4/(2-0)^3 = 1/2. Var = 1/2 - 1/4 = 1/4."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Moment-generating function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Moment-generating_function",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="characteristic_function_prob",
    content=(
        "The characteristic function of a random variable X is "
        "phi_X(t) = E[e^(itX)], where i is the imaginary unit. It "
        "always exists (unlike the MGF) and uniquely determines the "
        "distribution. For the normal distribution N(mu, sigma^2), "
        "phi(t) = exp(i*mu*t - sigma^2*t^2/2)."
    ),
    example=(
        "Standard normal N(0,1): phi(t) = exp(-t^2/2). "
        "phi(1) = exp(-0.5) = 0.6065. "
        "phi(0) = 1 (always true for any distribution)."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Characteristic function (probability theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Characteristic_function_(probability_theory)",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="theorem",
    name="central_limit",
    content=(
        "The Central Limit Theorem (CLT) states that the sum (or "
        "average) of a large number of independent, identically "
        "distributed random variables with finite mean mu and variance "
        "sigma^2 converges in distribution to a normal distribution: "
        "sqrt(n)(X_bar - mu)/sigma -> N(0,1) as n -> infinity, "
        "regardless of the original distribution's shape."
    ),
    example=(
        "Roll a fair die 100 times. mu=3.5, sigma^2=35/12, sigma=1.708. "
        "Sum S ~ approx N(350, 100*35/12) = N(350, 291.67). "
        "P(S > 370) = P(Z > (370-350)/17.08) = P(Z > 1.17) = 0.121."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Central limit theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Central_limit_theorem",
    prerequisites=["variance", "expected_value"],
))

register_atom(Atom(
    atom_type="theorem",
    name="law_large_numbers",
    content=(
        "The Law of Large Numbers (LLN) states that the sample average "
        "converges to the expected value as the sample size grows. "
        "The weak LLN gives convergence in probability: for any "
        "epsilon > 0, P(|X_bar_n - mu| > epsilon) -> 0 as n -> infinity. "
        "The strong LLN gives almost sure convergence."
    ),
    example=(
        "Fair coin, P(H)=0.5. After n=1000 flips, the proportion of "
        "heads X_bar is within 0.03 of 0.5 with probability > 0.95 "
        "(by Chebyshev: P(|X_bar - 0.5| > 0.03) <= 0.25/(1000*0.0009) = 0.278)."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Law of large numbers', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Law_of_large_numbers",
    prerequisites=["expected_value", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="conditional_expectation",
    content=(
        "The conditional expectation E[X|Y=y] is the expected value of "
        "X given that Y takes the value y. For discrete random variables, "
        "E[X|Y=y] = sum_x x * P(X=x|Y=y). The law of total expectation "
        "states E[X] = E[E[X|Y]], connecting marginal and conditional "
        "expectations."
    ),
    example=(
        "X = die roll, Y = indicator(X > 3). "
        "E[X|Y=1] = E[X|X>3] = (4+5+6)/3 = 5. "
        "E[X|Y=0] = E[X|X<=3] = (1+2+3)/3 = 2. "
        "E[X] = E[E[X|Y]] = 0.5*5 + 0.5*2 = 3.5."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Conditional expectation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conditional_expectation",
    prerequisites=["expected_value", "conditional_prob"],
))

register_atom(Atom(
    atom_type="theorem",
    name="large_deviation",
    content=(
        "Large deviation theory quantifies the exponential decay rate of "
        "probabilities of rare events. Cramer's theorem states that for "
        "i.i.d. random variables with MGF M(t), P(X_bar_n >= a) ~ "
        "exp(-n * I(a)) where I(a) = sup_t(ta - log M(t)) is the "
        "rate function (Legendre transform of the log-MGF)."
    ),
    example=(
        "X_i ~ Bernoulli(0.5), n=100. I(0.7) = 0.7*log(0.7/0.5) + "
        "0.3*log(0.3/0.5) = 0.7*0.3365 + 0.3*(-0.5108) = 0.0823. "
        "P(X_bar >= 0.7) ~ exp(-100*0.0823) = exp(-8.23) = 0.000266."
    ),
    tier=7,
    domain="probability",
    source="Wikipedia contributors, 'Large deviations theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Large_deviations_theory",
    prerequisites=["moment_generating"],
))

register_atom(Atom(
    atom_type="theorem",
    name="coupling_argument",
    content=(
        "A coupling of two probability distributions mu and nu is a "
        "joint distribution (X,Y) whose marginals are mu and nu "
        "respectively. The coupling lemma states that the total "
        "variation distance d_TV(mu, nu) = inf P(X != Y) over all "
        "couplings. Optimal coupling achieves this infimum and is "
        "used to bound mixing times of Markov chains."
    ),
    example=(
        "mu: coin with P(H)=1/3, nu: coin with P(H)=2/3. "
        "d_TV = |1/3 - 2/3| = 1/3. "
        "Optimal coupling: agree on H with probability 1/3, "
        "then X=T,Y=H with probability 1/3."
    ),
    tier=7,
    domain="probability",
    source="Wikipedia contributors, 'Coupling (probability)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coupling_(probability)",
    prerequisites=["total_probability"],
))

register_atom(Atom(
    atom_type="theorem",
    name="concentration_inequality",
    content=(
        "Concentration inequalities bound how far a random variable "
        "deviates from its expectation. Key results include: "
        "Markov: P(X >= a) <= E[X]/a for X >= 0. "
        "Chebyshev: P(|X-mu| >= k*sigma) <= 1/k^2. "
        "Hoeffding: P(X_bar - mu >= t) <= exp(-2nt^2/(b-a)^2) for "
        "X_i in [a,b]."
    ),
    example=(
        "Hoeffding: n=100 fair coins, X_i in [0,1], mu=0.5. "
        "P(X_bar >= 0.6) <= exp(-2*100*0.1^2/1) = exp(-2) = 0.135."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Concentration inequality', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Concentration_inequality",
    prerequisites=["variance", "expected_value"],
))

# -----------------------------------------------------------------------
# Advanced ML (tier 5-6)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="attention_multihead",
    content=(
        "Multi-head attention computes h parallel attention functions, "
        "each with its own learned projection matrices W_Q, W_K, W_V "
        "of dimension d_k = d_model/h. For each head: "
        "Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V. "
        "The h outputs are concatenated and projected by W_O."
    ),
    example=(
        "d_model=512, h=8, d_k=64, seq_len=10. "
        "Q,K,V each 10x64. QK^T is 10x10, divided by sqrt(64)=8. "
        "softmax gives 10x10 attention weights. "
        "Output per head: 10x64. Concat 8 heads: 10x512. "
        "W_O projects to 10x512."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Transformer (deep learning architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["softmax_eval", "dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="layer_norm",
    content=(
        "Layer normalisation normalises inputs across the feature "
        "dimension for each sample independently: "
        "y = (x - mu) / sqrt(sigma^2 + epsilon) * gamma + beta, "
        "where mu and sigma^2 are the mean and variance computed over "
        "the features of a single sample, and gamma, beta are learned "
        "affine parameters."
    ),
    example=(
        "x = [1, 2, 3, 4]. mu = 2.5, sigma^2 = 1.25, eps=1e-5. "
        "x_norm = [-1.342, -0.447, 0.447, 1.342] (with gamma=1, beta=0)."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Layer normalization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Layer_normalization",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="positional_encoding",
    content=(
        "Sinusoidal positional encoding adds position information to "
        "token embeddings in transformers: "
        "PE(pos, 2i) = sin(pos / 10000^(2i/d_model)), "
        "PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model)). "
        "Each dimension uses a different frequency, allowing the model "
        "to attend to relative positions."
    ),
    example=(
        "pos=3, d_model=4: "
        "PE(3,0) = sin(3/10000^0) = sin(3) = 0.1411. "
        "PE(3,1) = cos(3/10000^0) = cos(3) = -0.9900. "
        "PE(3,2) = sin(3/100) = sin(0.03) = 0.0300. "
        "PE(3,3) = cos(3/100) = cos(0.03) = 0.9996."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Transformer (deep learning architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="beam_search_step",
    content=(
        "Beam search is a heuristic search algorithm that explores a "
        "graph by expanding the k most promising nodes at each level "
        "(beam width k). At each step, all successors of the current "
        "k candidates are generated, scored, and the top k are kept. "
        "It trades optimality for efficiency compared to exhaustive "
        "search."
    ),
    example=(
        "Beam width k=2. Step 1 candidates: A(0.6), B(0.3), C(0.1). "
        "Keep top-2: A, B. Step 2 expand A->{A1(0.36), A2(0.24)}, "
        "B->{B1(0.21), B2(0.09)}. Top-2: A1(0.36), A2(0.24)."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Beam search', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Beam_search",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="formula",
    name="contrastive_loss",
    content=(
        "Contrastive loss (InfoNCE / NT-Xent) pulls representations "
        "of similar pairs together and pushes dissimilar pairs apart: "
        "L = -log(exp(sim(z_i, z_j)/tau) / sum_k exp(sim(z_i, z_k)/tau)), "
        "where sim is cosine similarity, tau is the temperature, "
        "z_j is the positive pair, and the sum is over all negatives."
    ),
    example=(
        "z_i=[1,0], z_j=[0.9,0.1] (positive), z_k=[0,-1] (negative). "
        "sim(i,j) = 0.9/sqrt(0.82) = 0.994, sim(i,k) = 0. tau=0.5. "
        "L = -log(exp(1.988) / (exp(1.988) + exp(0))) = "
        "-log(7.30 / 8.30) = -log(0.880) = 0.128."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Contrastive learning', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Contrastive_learning",
    prerequisites=["cross_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="transformer_flops",
    content=(
        "The FLOPs per forward pass of a transformer layer with "
        "d_model dimensions, sequence length n, and h attention heads: "
        "Self-attention: 4nd^2 (Q,K,V,O projections) + 2n^2d (attention). "
        "FFN: 8nd^2 (two linear layers with 4d hidden). "
        "Total per layer: 12nd^2 + 2n^2d."
    ),
    example=(
        "d=512, n=128, L=6: per layer = 12*128*512^2 + 2*128^2*512 = "
        "402,653,184 + 16,777,216 = 419M FLOPs. "
        "Total 6 layers: 2.52 GFLOPs."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Transformer (deep learning architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="lr_schedule",
    content=(
        "Learning rate scheduling adjusts the learning rate during "
        "training. Common schedules include: "
        "Cosine annealing: lr(t) = lr_min + 0.5*(lr_max - lr_min)*(1 + cos(pi*t/T)). "
        "Warmup: lr(t) = lr_max * t/T_warmup for t < T_warmup. "
        "Step decay: lr(t) = lr_0 * gamma^floor(t/step_size)."
    ),
    example=(
        "Cosine: lr_max=0.001, lr_min=1e-6, T=1000, t=500: "
        "lr = 1e-6 + 0.5*0.000999*(1 + cos(pi*500/1000)) = "
        "1e-6 + 0.0005*(1 + 0) = 0.000501."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Learning rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Learning_rate",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="weight_init",
    content=(
        "Weight initialisation sets the starting values of neural "
        "network parameters. Key methods: "
        "Xavier/Glorot: W ~ N(0, 2/(n_in + n_out)) for sigmoid/tanh. "
        "He/Kaiming: W ~ N(0, 2/n_in) for ReLU. "
        "Proper initialisation prevents vanishing/exploding gradients "
        "by maintaining activation variance across layers."
    ),
    example=(
        "He init for layer with n_in=512: "
        "std = sqrt(2/512) = sqrt(0.00391) = 0.0625. "
        "W ~ N(0, 0.0625^2) = N(0, 0.00391)."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Initialization (artificial neural networks)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Initialization_(artificial_neural_networks)",
    prerequisites=["variance"],
))
