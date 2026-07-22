"""Knowledge atoms for ML deep2, number theory ext, and combinatorics ext.

Covers SGD momentum, Adam optimizer, cosine annealing, mixup,
knowledge distillation, quadratic reciprocity, primitive roots,
Mobius function, multinomial coefficients, Stirling numbers,
Bell numbers, derangements, and related topics.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# ML Deep2 (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="sgd_momentum_step",
    content=(
        "SGD with momentum maintains a velocity vector v that accumulates "
        "an exponentially decaying moving average of past gradients. The "
        "update rule is: v_t = mu * v_{t-1} + g_t, then "
        "w_t = w_{t-1} - lr * v_t, where mu is the momentum coefficient "
        "(typically 0.9), g_t is the gradient at step t, and lr is the "
        "learning rate."
    ),
    example=(
        "Given w=1.0, g=0.5, v_prev=0.2, mu=0.9, lr=0.01: "
        "v = 0.9*0.2 + 0.5 = 0.68, w_new = 1.0 - 0.01*0.68 = 0.9932"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Stochastic gradient descent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Momentum",
    prerequisites=["gradient", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="adam_full_step",
    content=(
        "Adam (Adaptive Moment Estimation) maintains two moving averages: "
        "first moment m_t = beta1*m_{t-1} + (1-beta1)*g_t and second moment "
        "v_t = beta2*v_{t-1} + (1-beta2)*g_t^2. Bias-corrected estimates: "
        "m_hat = m_t/(1-beta1^t), v_hat = v_t/(1-beta2^t). Update: "
        "w = w - lr * m_hat / (sqrt(v_hat) + epsilon). Default: "
        "beta1=0.9, beta2=0.999, epsilon=1e-8."
    ),
    example=(
        "Given w=0.5, g=0.1, m_prev=0, v_prev=0, t=1, lr=0.001, "
        "beta1=0.9, beta2=0.999: m=0.01, v=0.00001, "
        "m_hat=0.01/0.1=0.1, v_hat=0.00001/0.001=0.01, "
        "w_new = 0.5 - 0.001*0.1/(sqrt(0.01)+1e-8) = 0.5 - 0.001 = 0.499"
    ),
    tier=5,
    domain="machine_learning",
    source="Kingma & Ba, 'Adam: A Method for Stochastic Optimization', 2015.",
    source_url="https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam",
    prerequisites=["sgd_momentum_step"],
))

register_atom(Atom(
    atom_type="formula",
    name="cosine_lr_schedule",
    content=(
        "Cosine annealing decays the learning rate following a cosine curve: "
        "lr_t = lr_min + 0.5*(lr_max - lr_min)*(1 + cos(pi*t/T_max)), "
        "where t is the current step, T_max is the total number of steps, "
        "lr_max is the initial learning rate, and lr_min is the minimum. "
        "This provides a smooth warmup-decay schedule."
    ),
    example=(
        "Given lr_max=0.1, lr_min=0.001, T_max=100, t=50: "
        "lr = 0.001 + 0.5*(0.1-0.001)*(1+cos(pi*50/100)) = "
        "0.001 + 0.0495*(1+0) = 0.0505"
    ),
    tier=4,
    domain="machine_learning",
    source="Loshchilov & Hutter, 'SGDR: Stochastic Gradient Descent with Warm Restarts', 2017.",
    source_url="https://en.wikipedia.org/wiki/Learning_rate#Cosine_annealing",
    prerequisites=["lr_decay"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="mixup_training",
    content=(
        "Mixup creates virtual training examples by taking convex "
        "combinations of pairs of examples and their labels: "
        "x_mix = lambda*x_i + (1-lambda)*x_j, "
        "y_mix = lambda*y_i + (1-lambda)*y_j, "
        "where lambda is sampled from Beta(alpha, alpha) with alpha "
        "typically 0.2 or 0.4. This regularises by encouraging linear "
        "behaviour between training examples."
    ),
    example=(
        "Given x1=[1,2], x2=[3,4], y1=[1,0], y2=[0,1], lambda=0.3: "
        "x_mix = 0.3*[1,2] + 0.7*[3,4] = [2.4, 3.4], "
        "y_mix = 0.3*[1,0] + 0.7*[0,1] = [0.3, 0.7]"
    ),
    tier=5,
    domain="machine_learning",
    source="Zhang et al., 'mixup: Beyond Empirical Risk Minimization', 2018.",
    source_url="https://en.wikipedia.org/wiki/Data_augmentation#Mixup",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="knowledge_distillation",
    content=(
        "Knowledge distillation transfers knowledge from a large teacher "
        "model to a smaller student model. The student is trained on soft "
        "targets: p_i = exp(z_i/T) / sum(exp(z_j/T)), where z_i are the "
        "teacher's logits and T is the temperature (typically 2-20). The "
        "loss combines cross-entropy with hard labels and KL divergence "
        "with soft targets: L = alpha*CE(y, p_student) + "
        "(1-alpha)*T^2*KL(p_teacher_soft, p_student_soft)."
    ),
    example=(
        "Teacher logits [2.0, 1.0, 0.1], T=2: "
        "soft = exp([1.0, 0.5, 0.05]) / sum = [2.718, 1.649, 1.051] / 5.418 "
        "= [0.502, 0.304, 0.194]"
    ),
    tier=6,
    domain="machine_learning",
    source="Hinton et al., 'Distilling the Knowledge in a Neural Network', 2015.",
    source_url="https://en.wikipedia.org/wiki/Knowledge_distillation",
    prerequisites=["softmax_eval", "cross_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="gradient_accumulation",
    content=(
        "Gradient accumulation simulates larger batch sizes by accumulating "
        "gradients over multiple mini-batches before performing a weight "
        "update. After K accumulation steps: "
        "g_accumulated = (1/K) * sum(g_k, k=1..K), then "
        "w = w - lr * g_accumulated. The effective batch size is "
        "K * mini_batch_size."
    ),
    example=(
        "Given mini_batch=32, accumulation_steps=4: effective_batch = 128. "
        "Gradients g1=0.1, g2=0.3, g3=0.2, g4=0.0: "
        "g_acc = (0.1+0.3+0.2+0.0)/4 = 0.15, w_new = w - lr*0.15"
    ),
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Gradient descent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gradient_descent",
    prerequisites=["gradient"],
))

register_atom(Atom(
    atom_type="definition",
    name="normalization_comparison",
    content=(
        "Normalisation layers stabilise training by normalising activations. "
        "Batch Norm: normalise across the batch dimension for each feature. "
        "Layer Norm: normalise across the feature dimension for each sample. "
        "Instance Norm: normalise across spatial dimensions per channel per "
        "sample. Group Norm: normalise across groups of channels. "
        "For input x with mean mu and variance sigma^2: "
        "x_norm = (x - mu) / sqrt(sigma^2 + epsilon), then "
        "y = gamma * x_norm + beta."
    ),
    example=(
        "Layer Norm on [1, 2, 3, 4]: mean=2.5, var=1.25, "
        "x_norm = [-1.342, -0.447, 0.447, 1.342] (with eps=1e-5)"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Batch normalization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Batch_normalization",
    prerequisites=["batch_norm"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sparse_attention",
    content=(
        "Sparse attention reduces the O(n^2) complexity of self-attention "
        "by attending to only a subset of positions. Common patterns: "
        "local attention (fixed window of k neighbours), strided attention "
        "(every s-th position), random attention, or combinations. "
        "Longformer uses local + global attention. BigBird uses local + "
        "random + global. Complexity reduces to O(n*k) or O(n*sqrt(n))."
    ),
    example=(
        "Sequence length n=1024, window k=128: full attention = 1024^2 = "
        "1,048,576 ops, sparse attention = 1024*128 = 131,072 ops (8x reduction)"
    ),
    tier=6,
    domain="machine_learning",
    source="Zaheer et al., 'Big Bird: Transformers for Longer Sequences', 2020.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)#Efficient_transformers",
    prerequisites=["attention_score"],
))

register_atom(Atom(
    atom_type="formula",
    name="model_flops_compute",
    content=(
        "For a transformer model, approximate FLOPs per forward pass: "
        "FLOPs = 2 * n_params * seq_len (for dense layers) + "
        "4 * n_layers * d_model * seq_len^2 (for attention). "
        "Total training FLOPs = 6 * n_params * n_tokens (the 6x factor "
        "accounts for forward, backward, and gradient accumulation). "
        "Chinchilla scaling: optimal tokens = 20 * n_params."
    ),
    example=(
        "Model with 125M params, seq_len=512, 12 layers, d=768: "
        "forward FLOPs = 2*125e6*512 + 4*12*768*512^2 = "
        "128e9 + 9.66e9 = 137.7 GFLOPs per forward pass"
    ),
    tier=5,
    domain="machine_learning",
    source="Kaplan et al., 'Scaling Laws for Neural Language Models', 2020.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="definition",
    name="loss_function_comparison",
    content=(
        "Common loss functions: MSE = (1/n)*sum((y-y_hat)^2), good for "
        "regression. Cross-entropy = -sum(y*log(y_hat)), good for "
        "classification. Huber loss = 0.5*(y-y_hat)^2 if |y-y_hat|<delta, "
        "else delta*(|y-y_hat|-0.5*delta), robust to outliers. "
        "Focal loss = -alpha*(1-p_t)^gamma*log(p_t), addresses class "
        "imbalance by down-weighting easy examples."
    ),
    example=(
        "MSE: y=[1,0,1], y_hat=[0.9,0.1,0.8]: "
        "MSE = ((0.1)^2 + (0.1)^2 + (0.2)^2)/3 = 0.06/3 = 0.02"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Loss function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loss_function",
    prerequisites=["mse_loss", "cross_entropy"],
))


# =========================================================================
# Number Theory Ext (tier 6)
# =========================================================================

register_atom(Atom(
    atom_type="theorem",
    name="quadratic_reciprocity",
    content=(
        "Gauss's law of quadratic reciprocity: for distinct odd primes p "
        "and q, (p/q)*(q/p) = (-1)^{(p-1)(q-1)/4}, where (a/p) is the "
        "Legendre symbol. Equivalently, (p/q) = (q/p) unless both p and q "
        "are congruent to 3 mod 4, in which case (p/q) = -(q/p). "
        "Supplements: (-1/p) = (-1)^{(p-1)/2} and (2/p) = (-1)^{(p^2-1)/8}."
    ),
    example=(
        "p=5, q=7: (5/7)*(7/5) = (-1)^{(4)(6)/4} = (-1)^6 = 1. "
        "Since 5^3 = 125 = 6 mod 7, (5/7) = -1. "
        "So (7/5) = -1 as well. Check: 7 = 2 mod 5, 2^2 = 4 = -1 mod 5, so (7/5) = (2/5) = -1."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Quadratic reciprocity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quadratic_reciprocity",
    prerequisites=["legendre_symbol_compute", "modular"],
))

register_atom(Atom(
    atom_type="definition",
    name="primitive_root",
    content=(
        "A primitive root modulo n is an integer g such that the "
        "multiplicative order of g modulo n equals phi(n), i.e., "
        "g generates the entire group of units (Z/nZ)*. Primitive roots "
        "exist modulo 1, 2, 4, p^k, and 2p^k for odd primes p. "
        "The smallest primitive root of a prime p is always less than "
        "p^{0.499} assuming GRH."
    ),
    example=(
        "Find primitive root mod 7: phi(7)=6. "
        "Try g=3: 3^1=3, 3^2=2, 3^3=6, 3^4=4, 3^5=5, 3^6=1 (mod 7). "
        "Order=6=phi(7), so 3 is a primitive root mod 7."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Primitive root modulo n', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Primitive_root_modulo_n",
    prerequisites=["totient", "modular"],
))

register_atom(Atom(
    atom_type="formula",
    name="sum_of_squares",
    content=(
        "Lagrange's four-square theorem states that every natural number "
        "can be represented as the sum of four integer squares: "
        "n = a^2 + b^2 + c^2 + d^2. For two squares, Fermat's theorem "
        "states a prime p can be expressed as p = a^2 + b^2 if and only "
        "if p = 2 or p = 1 mod 4."
    ),
    example=(
        "Express 13 as sum of two squares: 13 = 1 mod 4, so possible. "
        "13 = 2^2 + 3^2 = 4 + 9 = 13. Verified."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Sum of two squares theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="mobius_function",
    content=(
        "The Mobius function mu(n) is defined as: mu(1) = 1; "
        "mu(n) = (-1)^k if n is a product of k distinct primes; "
        "mu(n) = 0 if n has a squared prime factor. Key property: "
        "sum(mu(d), d|n) = 1 if n=1, 0 otherwise. The Mobius inversion "
        "formula: if g(n) = sum(f(d), d|n) then f(n) = sum(mu(n/d)*g(d), d|n)."
    ),
    example=(
        "mu(30) = mu(2*3*5) = (-1)^3 = -1 (3 distinct primes). "
        "mu(12) = mu(2^2*3) = 0 (squared factor). "
        "mu(1) = 1."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Mobius function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/M%C3%B6bius_function",
    prerequisites=["factorisation"],
))

register_atom(Atom(
    atom_type="formula",
    name="divisor_function",
    content=(
        "The divisor function sigma_k(n) = sum(d^k, d|n). Special cases: "
        "sigma_0(n) = d(n) counts the number of divisors; "
        "sigma_1(n) = sigma(n) gives the sum of divisors. "
        "For a prime p: sigma_k(p) = 1 + p^k. "
        "For prime power: sigma_k(p^a) = (p^{k(a+1)} - 1) / (p^k - 1). "
        "Multiplicative: sigma_k(mn) = sigma_k(m)*sigma_k(n) when gcd(m,n)=1."
    ),
    example=(
        "sigma_0(12) = number of divisors of 12. "
        "Divisors: 1, 2, 3, 4, 6, 12. sigma_0(12) = 6. "
        "sigma_1(12) = 1+2+3+4+6+12 = 28."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Divisor function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Divisor_function",
    prerequisites=["factorisation", "gcd"],
))

register_atom(Atom(
    atom_type="formula",
    name="jacobi_symbol",
    content=(
        "The Jacobi symbol (a/n) generalises the Legendre symbol to "
        "composite odd n. If n = p1^e1 * p2^e2 * ... * pk^ek, then "
        "(a/n) = (a/p1)^e1 * (a/p2)^e2 * ... * (a/pk)^ek. "
        "Properties: (a/n) = 0 if gcd(a,n) > 1; "
        "(ab/n) = (a/n)(b/n); (-1/n) = (-1)^{(n-1)/2}; "
        "(2/n) = (-1)^{(n^2-1)/8}."
    ),
    example=(
        "(2/15) = (2/3)*(2/5). "
        "(2/3) = (-1)^{(9-1)/8} = (-1)^1 = -1. "
        "(2/5) = (-1)^{(25-1)/8} = (-1)^3 = -1. "
        "(2/15) = (-1)*(-1) = 1."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Jacobi symbol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jacobi_symbol",
    prerequisites=["legendre_symbol_compute", "factorisation"],
))

register_atom(Atom(
    atom_type="formula",
    name="pell_equation",
    content=(
        "Pell's equation x^2 - D*y^2 = 1 (D a positive non-square integer) "
        "always has infinitely many solutions. The fundamental solution "
        "(x1, y1) is found from the continued fraction expansion of sqrt(D). "
        "Further solutions: x_{n+1} = x1*x_n + D*y1*y_n, "
        "y_{n+1} = x1*y_n + y1*x_n."
    ),
    example=(
        "D=2: sqrt(2) = [1; 2, 2, 2, ...]. Fundamental solution: "
        "x=3, y=2. Check: 3^2 - 2*2^2 = 9 - 8 = 1. "
        "Next: x=3*3+2*2*2=17, y=3*2+2*3=12. Check: 289-288=1."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Pell's equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pell%27s_equation",
    prerequisites=["continued_fraction", "exponentiation"],
))

register_atom(Atom(
    atom_type="definition",
    name="order_element",
    content=(
        "The multiplicative order of a modulo n (when gcd(a,n)=1) is the "
        "smallest positive integer k such that a^k = 1 mod n. Written "
        "ord_n(a) = k. Properties: ord_n(a) divides phi(n) (Euler's "
        "theorem). If ord_n(a) = phi(n), then a is a primitive root mod n."
    ),
    example=(
        "ord_7(2): 2^1=2, 2^2=4, 2^3=1 mod 7. So ord_7(2) = 3. "
        "Check: 3 divides phi(7) = 6. Yes."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Multiplicative order', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiplicative_order",
    prerequisites=["modular", "totient"],
))


# =========================================================================
# Combinatorics Ext (tier 4-5)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="multinomial_coefficient",
    content=(
        "The multinomial coefficient (n; k1, k2, ..., km) = n! / (k1! * k2! "
        "* ... * km!) counts the number of ways to partition n objects into "
        "groups of sizes k1, k2, ..., km where k1+k2+...+km = n. "
        "Generalises the binomial coefficient: C(n,k) = (n; k, n-k)."
    ),
    example=(
        "(6; 2, 3, 1) = 6! / (2! * 3! * 1!) = 720 / (2 * 6 * 1) = 60. "
        "This is the number of ways to arrange AABBBC (2 A's, 3 B's, 1 C)."
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Multinomial theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multinomial_theorem",
    prerequisites=["binomial", "permutation"],
))

register_atom(Atom(
    atom_type="formula",
    name="derangement_compute",
    content=(
        "A derangement is a permutation with no fixed points. The number "
        "of derangements D(n) (subfactorial !n) is given by: "
        "D(n) = n! * sum_{k=0}^{n} (-1)^k / k! "
        "Approximately D(n) = round(n!/e). "
        "Recurrence: D(n) = (n-1)*(D(n-1) + D(n-2)), with D(0)=1, D(1)=0."
    ),
    example=(
        "D(4) = 4! * (1 - 1 + 1/2 - 1/6 + 1/24) = 24 * (3/8) = 9. "
        "Verify: 24 * (1 - 1 + 0.5 - 0.1667 + 0.0417) = 24 * 0.375 = 9."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Derangement', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Derangement",
    prerequisites=["permutation"],
))

register_atom(Atom(
    atom_type="formula",
    name="stirling_second",
    content=(
        "The Stirling number of the second kind S(n,k) counts the number "
        "of ways to partition a set of n elements into k non-empty subsets. "
        "Formula: S(n,k) = (1/k!) * sum_{j=0}^{k} (-1)^{k-j} * C(k,j) * j^n. "
        "Recurrence: S(n,k) = k*S(n-1,k) + S(n-1,k-1), with "
        "S(n,1) = S(n,n) = 1."
    ),
    example=(
        "S(4,2): partitions of {1,2,3,4} into 2 non-empty subsets. "
        "S(4,2) = 2*S(3,2) + S(3,1) = 2*3 + 1 = 7. "
        "Or by formula: (1/2)*(0^4 - 2*1^4 + 2^4) = (1/2)*(0-2+16) = 7."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Stirling numbers of the second kind', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="formula",
    name="bell_number",
    content=(
        "The Bell number B(n) counts the total number of partitions of a "
        "set of n elements into non-empty subsets. B(n) = sum_{k=0}^{n} S(n,k) "
        "where S(n,k) is a Stirling number of the second kind. "
        "Bell triangle: B(n+1) = sum_{k=0}^{n} C(n,k)*B(k). "
        "First values: B(0)=1, B(1)=1, B(2)=2, B(3)=5, B(4)=15, B(5)=52."
    ),
    example=(
        "B(3) = S(3,1) + S(3,2) + S(3,3) = 1 + 3 + 1 = 5. "
        "The 5 partitions of {1,2,3}: {{1,2,3}}, {{1,2},{3}}, "
        "{{1,3},{2}}, {{2,3},{1}}, {{1},{2},{3}}."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Bell number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bell_number",
    prerequisites=["stirling_second"],
))

register_atom(Atom(
    atom_type="theorem",
    name="twelvefold_way",
    content=(
        "The twelvefold way classifies counting problems by three binary "
        "choices: are the n balls distinguishable? Are the k boxes "
        "distinguishable? Is at most one ball per box (injections), any "
        "number (arbitrary functions), or at least one (surjections)? "
        "This gives 12 cases. Examples: k^n (distinguishable balls, "
        "distinguishable boxes, arbitrary), n! (injections, both "
        "distinguishable), S(n,k)*k! (surjections, both distinguishable)."
    ),
    example=(
        "3 distinguishable balls into 2 distinguishable boxes (arbitrary): "
        "2^3 = 8 ways. Surjections only: S(3,2)*2! = 3*2 = 6."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Twelvefold way', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Twelvefold_way",
    prerequisites=["stirling_second", "binomial"],
))

register_atom(Atom(
    atom_type="theorem",
    name="principle_inclusion_exclusion",
    content=(
        "The principle of inclusion-exclusion: |A1 union A2 union ... union An| = "
        "sum|Ai| - sum|Ai intersect Aj| + sum|Ai intersect Aj intersect Ak| - ... "
        "+ (-1)^{n+1}|A1 intersect ... intersect An|. "
        "For counting elements NOT in any set: "
        "|complement| = |U| - sum|Ai| + sum|Ai intersect Aj| - ..."
    ),
    example=(
        "|A|=10, |B|=15, |C|=12, |A&B|=5, |A&C|=4, |B&C|=6, |A&B&C|=2: "
        "|A union B union C| = 10+15+12 - 5-4-6 + 2 = 24."
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Inclusion-exclusion principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
    prerequisites=["set_operations"],
))

register_atom(Atom(
    atom_type="definition",
    name="latin_square",
    content=(
        "A Latin square of order n is an n x n array filled with n different "
        "symbols, each occurring exactly once in each row and each column. "
        "The number of Latin squares of order n grows super-exponentially: "
        "L(1)=1, L(2)=2, L(3)=12, L(4)=576, L(5)=161280. "
        "Two Latin squares are orthogonal if, when superimposed, each "
        "ordered pair of symbols occurs exactly once."
    ),
    example=(
        "Latin square of order 3: [[1,2,3],[2,3,1],[3,1,2]]. "
        "Each row and column contains {1,2,3} exactly once. "
        "This is also a cyclic Latin square."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Latin square', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Latin_square",
    prerequisites=["permutation"],
))

register_atom(Atom(
    atom_type="formula",
    name="ballot_problem",
    content=(
        "The ballot problem: if candidate A receives a votes and candidate B "
        "receives b votes (a > b), the probability that A is strictly ahead "
        "of B throughout the counting is (a - b) / (a + b). "
        "Equivalently, the number of favourable sequences is "
        "(a - b) / (a + b) * C(a+b, a). Related to Catalan numbers: "
        "C(2n, n) / (n+1) counts Dyck paths of length 2n."
    ),
    example=(
        "A gets 5 votes, B gets 3 votes: P(A always ahead) = "
        "(5-3)/(5+3) = 2/8 = 1/4 = 0.25."
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Bertrand ballot problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bertrand_ballot_problem",
    prerequisites=["basic_prob", "binomial"],
))
