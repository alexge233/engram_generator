"""Knowledge atoms for ML theory and computational neuroscience.

Covers VC dimension, PAC learning, Rademacher complexity, kernel
methods, regularisation, bias-variance, cross-validation, information
gain, gradient flow, attention complexity, membrane potentials,
Goldman equation, Hodgkin-Huxley, spike rates, receptive fields,
neural coding, synaptic integration, cable equation, fMRI BOLD,
and EEG frequency bands.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# ML Theory (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="theorem",
    name="vc_dimension",
    content=(
        "The Vapnik-Chervonenkis (VC) dimension of a hypothesis class H "
        "is the largest set of points that can be shattered by H. A set "
        "of points is shattered if, for every possible labelling of those "
        "points, there exists a hypothesis in H that correctly classifies "
        "them. For linear classifiers in R^d, the VC dimension is d+1. "
        "The VC dimension provides an upper bound on the sample complexity "
        "needed for PAC learning."
    ),
    example=(
        "Linear classifiers in R^2: VC dim = 2+1 = 3. "
        "Any 3 non-collinear points can be shattered (all 2^3=8 "
        "labellings achievable), but no set of 4 points can be "
        "shattered by a linear separator."
    ),
    tier=7,
    domain="machine_learning",
    source="Wikipedia contributors, 'Vapnik-Chervonenkis dimension', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vapnik%E2%80%93Chervonenkis_dimension",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pac_bound",
    content=(
        "PAC (Probably Approximately Correct) learning bounds give the "
        "minimum number of samples m needed to learn a concept within "
        "error epsilon with probability at least 1-delta. For finite "
        "hypothesis classes: m >= (1/epsilon) * ln(|H|/delta). For "
        "infinite classes with VC dimension d: m >= (1/epsilon^2) * "
        "(d*ln(1/epsilon) + ln(1/delta)). These bounds guarantee that "
        "with enough samples, the empirical risk minimiser generalises."
    ),
    example=(
        "Finite H with |H|=100, epsilon=0.1, delta=0.05: "
        "m >= (1/0.1)*ln(100/0.05) = 10*ln(2000) = 10*7.601 = 76.01, "
        "so m >= 77 samples suffice."
    ),
    tier=7,
    domain="machine_learning",
    source="Wikipedia contributors, 'Probably approximately correct learning', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Probably_approximately_correct_learning",
    prerequisites=["vc_dimension"],
))

register_atom(Atom(
    atom_type="theorem",
    name="rademacher_complexity",
    content=(
        "The empirical Rademacher complexity of a function class F with "
        "respect to a sample S = {x_1,...,x_m} is: "
        "R_S(F) = (1/m) E_sigma[sup_{f in F} sum_i sigma_i f(x_i)], "
        "where sigma_i are iid Rademacher random variables (uniform on "
        "{-1,+1}). It measures the ability of F to fit random noise. "
        "Generalisation bound: with probability >= 1-delta, for all f in F, "
        "R(f) <= R_hat(f) + 2*R_m(F) + sqrt(ln(1/delta)/(2m))."
    ),
    example=(
        "For linear classifiers ||w||<=1 on unit ball in R^d: "
        "R_m(F) <= sqrt(d/m). With d=10, m=1000: "
        "R_m <= sqrt(10/1000) = sqrt(0.01) = 0.1."
    ),
    tier=7,
    domain="machine_learning",
    source="Wikipedia contributors, 'Rademacher complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rademacher_complexity",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="kernel_trick",
    content=(
        "The kernel trick allows algorithms that depend only on dot "
        "products to operate in a high-dimensional feature space without "
        "explicitly computing the mapping. A kernel function K(x,y) = "
        "phi(x) . phi(y) computes the inner product in feature space. "
        "Common kernels: linear K(x,y) = x.y, polynomial K(x,y) = "
        "(x.y + c)^d, RBF/Gaussian K(x,y) = exp(-||x-y||^2 / (2*sigma^2)). "
        "Mercer's theorem guarantees that any positive semi-definite "
        "kernel corresponds to some feature space."
    ),
    example=(
        "Polynomial kernel d=2, c=1 on x=[1,2], y=[3,4]: "
        "K(x,y) = (x.y + 1)^2 = (1*3 + 2*4 + 1)^2 = (12)^2 = 144."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Kernel method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kernel_method",
    prerequisites=["dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="regularisation_path",
    content=(
        "The regularisation path traces how model coefficients change "
        "as the regularisation strength lambda varies from 0 to infinity. "
        "For L2 (ridge) regression: w(lambda) = (X^T X + lambda*I)^{-1} "
        "X^T y. As lambda -> 0, w approaches the OLS solution. As "
        "lambda -> inf, w -> 0. For L1 (lasso): the path is piecewise "
        "linear, and coefficients hit zero at specific lambda values, "
        "performing variable selection."
    ),
    example=(
        "Ridge regression, 1D: X=[1,2,3], y=[2,4,5], X^T X=14, X^T y=29. "
        "lambda=0: w=29/14=2.071. lambda=1: w=29/15=1.933. "
        "lambda=10: w=29/24=1.208. lambda=100: w=29/114=0.254."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Regularization (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regularization_(mathematics)",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="theorem",
    name="bias_variance_decompose",
    content=(
        "The bias-variance decomposition splits the expected prediction "
        "error into three components: E[(y - f_hat(x))^2] = "
        "Bias(f_hat)^2 + Var(f_hat) + sigma^2, where Bias = "
        "E[f_hat(x)] - f(x), Var = E[(f_hat(x) - E[f_hat(x)])^2], "
        "and sigma^2 is irreducible noise. Increasing model complexity "
        "decreases bias but increases variance (overfitting). The "
        "optimal model minimises the sum."
    ),
    example=(
        "True f(x)=2x, noise sigma=0.5. Model A (constant): "
        "bias^2=(2x-mean)^2 high, var=0. Model B (high-degree poly): "
        "bias^2~0, var high. Optimal: linear fit with bias^2~0, "
        "var~sigma^2/n."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Bias-variance tradeoff', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff",
    prerequisites=["variance", "expected_value"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="cross_validation_compute",
    content=(
        "K-fold cross-validation partitions the data into k equal folds. "
        "For each fold i, train on all folds except i, evaluate on fold i. "
        "The CV estimate is the mean of the k evaluation scores: "
        "CV(k) = (1/k) * sum_{i=1}^{k} L(f_{-i}, D_i), where f_{-i} "
        "is the model trained without fold i, and D_i is fold i. "
        "Leave-one-out CV (LOOCV) is the special case k=n."
    ),
    example=(
        "5-fold CV on 100 samples: each fold has 20 samples. "
        "Fold errors: [0.12, 0.15, 0.11, 0.14, 0.13]. "
        "CV estimate = (0.12+0.15+0.11+0.14+0.13)/5 = 0.65/5 = 0.13."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Cross-validation (statistics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cross-validation_(statistics)",
    prerequisites=["mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="information_gain",
    content=(
        "Information gain (IG) measures the reduction in entropy of a "
        "target variable Y when splitting on feature X: "
        "IG(Y, X) = H(Y) - H(Y|X), where H(Y) = -sum p(y)*log2(p(y)) "
        "is the entropy of Y, and H(Y|X) = sum_x p(x)*H(Y|X=x) is the "
        "conditional entropy. IG is used in decision tree algorithms "
        "(ID3, C4.5) to select the best splitting feature."
    ),
    example=(
        "Y: 5 yes, 5 no. H(Y) = -0.5*log2(0.5)*2 = 1.0 bit. "
        "Split on X: left={3 yes, 1 no}, right={2 yes, 4 no}. "
        "H(Y|X=left) = -0.75*log2(0.75)-0.25*log2(0.25) = 0.811. "
        "H(Y|X=right) = -0.333*log2(0.333)-0.667*log2(0.667) = 0.918. "
        "H(Y|X) = 0.4*0.811 + 0.6*0.918 = 0.875. "
        "IG = 1.0 - 0.875 = 0.125 bits."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Information gain in decision trees', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Information_gain_in_decision_trees",
    prerequisites=["info_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="gradient_flow",
    content=(
        "Gradient flow describes how gradients propagate through a neural "
        "network during backpropagation. For a network with layers "
        "f_1, f_2, ..., f_L, the gradient of the loss with respect to "
        "layer i parameters is: dL/dW_i = dL/df_L * df_L/df_{L-1} * "
        "... * df_{i+1}/df_i * df_i/dW_i. The product of Jacobians "
        "can vanish (all gradients near zero) or explode (gradients grow "
        "exponentially). Residual connections mitigate this by adding "
        "identity shortcuts: df/dx = 1 + dg/dx."
    ),
    example=(
        "3-layer network, each layer Jacobian has spectral norm 0.5: "
        "gradient at layer 1 = 0.5^2 = 0.25 of output gradient "
        "(vanishing). With spectral norm 2.0: gradient = 2.0^2 = 4.0 "
        "(exploding). With residual: gradient >= 1.0 always."
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Vanishing gradient problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vanishing_gradient_problem",
    prerequisites=["chain_rule", "backprop_simple"],
))

register_atom(Atom(
    atom_type="formula",
    name="attention_complexity",
    content=(
        "Self-attention in transformers computes Attention(Q,K,V) = "
        "softmax(QK^T / sqrt(d_k)) V. For sequence length n and "
        "head dimension d_k: QK^T requires O(n^2 * d_k) operations, "
        "softmax is O(n^2), and multiplication by V is O(n^2 * d_v). "
        "Total: O(n^2 * d) per head, O(n^2 * d) for all heads. "
        "Memory: O(n^2) for the attention matrix. Multi-head with h "
        "heads of dimension d_k = d/h: total is still O(n^2 * d)."
    ),
    example=(
        "n=512 tokens, d=768, h=12 heads, d_k=64: "
        "QK^T FLOPs per head = 2*512^2*64 = 33,554,432. "
        "All heads = 12 * 33.5M = 402M FLOPs. "
        "Attention matrix memory = 512^2 * 12 * 4 bytes = 12.6 MB."
    ),
    tier=7,
    domain="machine_learning",
    source="Wikipedia contributors, 'Transformer (deep learning architecture)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["matrix_multiply", "softmax_eval"],
))


# =========================================================================
# Computational Neuroscience (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="membrane_potential",
    content=(
        "The Nernst equation gives the equilibrium potential for a single "
        "ion species across a membrane: E = (RT/zF) * ln([ion]_out / "
        "[ion]_in), where R = 8.314 J/(mol*K) is the gas constant, "
        "T is temperature in Kelvin, z is the ion valence, and "
        "F = 96485 C/mol is Faraday's constant. At body temperature "
        "(37C = 310K), RT/F = 0.0267 V. For potassium (z=+1) with "
        "typical concentrations [K+]_out=5mM, [K+]_in=140mM: "
        "E_K = 0.0267 * ln(5/140) = -89 mV."
    ),
    example=(
        "Potassium at 37C: E_K = (8.314*310)/(1*96485) * ln(5/140) "
        "= 0.0267 * (-3.332) = -88.9 mV."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Nernst equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nernst_equation",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="goldman_equation",
    content=(
        "The Goldman-Hodgkin-Katz (GHK) voltage equation gives the "
        "resting membrane potential when multiple ion species are present: "
        "V_m = (RT/F) * ln((P_K[K+]_o + P_Na[Na+]_o + P_Cl[Cl-]_i) / "
        "(P_K[K+]_i + P_Na[Na+]_i + P_Cl[Cl-]_o)), where P_X is the "
        "membrane permeability to ion X. At rest, P_K >> P_Na, so V_m "
        "is close to E_K. During an action potential, P_Na increases "
        "dramatically, driving V_m toward E_Na."
    ),
    example=(
        "P_K:P_Na:P_Cl = 1:0.04:0.45, [K+]o=5, [K+]i=140, "
        "[Na+]o=145, [Na+]i=12, [Cl-]o=120, [Cl-]i=4, T=310K: "
        "V_m = 0.0267*ln((1*5+0.04*145+0.45*4)/(1*140+0.04*12+0.45*120)) "
        "= 0.0267*ln(12.6/194.48) = 0.0267*(-2.737) = -73.1 mV."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Goldman equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Goldman_equation",
    prerequisites=["membrane_potential"],
))

register_atom(Atom(
    atom_type="model",
    name="hodgkin_huxley_gate",
    content=(
        "The Hodgkin-Huxley model describes ion channel gating using "
        "first-order kinetics. Each gate variable x (m, h, or n) follows: "
        "dx/dt = alpha_x(V)*(1-x) - beta_x(V)*x, where alpha and beta "
        "are voltage-dependent rate constants. At steady state: "
        "x_inf = alpha_x / (alpha_x + beta_x), tau_x = 1/(alpha_x + "
        "beta_x). The sodium current is I_Na = g_Na * m^3 * h * (V - E_Na), "
        "and potassium current is I_K = g_K * n^4 * (V - E_K)."
    ),
    example=(
        "At V=-65mV (rest): alpha_n=0.01*(V+55)/(1-exp(-(V+55)/10)) "
        "= 0.01*(-10)/(1-exp(1)) = 0.058. beta_n=0.125*exp(-(V+65)/80) "
        "= 0.125. n_inf = 0.058/(0.058+0.125) = 0.317. "
        "tau_n = 1/(0.058+0.125) = 5.46 ms."
    ),
    tier=6,
    domain="neuroscience",
    source="Wikipedia contributors, 'Hodgkin-Huxley model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model",
    prerequisites=["membrane_potential", "differential_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="spike_rate",
    content=(
        "The firing rate of a neuron can be computed as the number of "
        "action potentials (spikes) per unit time: r = n_spikes / T, "
        "where T is the observation window in seconds. The instantaneous "
        "firing rate is the inverse of the inter-spike interval (ISI): "
        "r_inst = 1 / ISI. For a Poisson neuron with rate lambda, the "
        "probability of k spikes in time T is: P(k) = (lambda*T)^k * "
        "exp(-lambda*T) / k!."
    ),
    example=(
        "Neuron fires 45 spikes in 1.5 seconds: "
        "rate = 45/1.5 = 30 Hz. ISIs = [30, 35, 28, 40, 32] ms: "
        "mean ISI = 33 ms, instantaneous rates = [33.3, 28.6, 35.7, "
        "25.0, 31.3] Hz."
    ),
    tier=4,
    domain="neuroscience",
    source="Wikipedia contributors, 'Neural coding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Neural_coding",
    prerequisites=["division", "mean"],
))

register_atom(Atom(
    atom_type="model",
    name="receptive_field",
    content=(
        "A receptive field is the region of sensory space (e.g. visual "
        "field) that elicits a response from a neuron. In the visual "
        "system, simple cells in V1 have oriented receptive fields that "
        "can be modelled as Gabor functions: "
        "g(x,y) = exp(-(x'^2 + gamma^2*y'^2)/(2*sigma^2)) * "
        "cos(2*pi*x'/lambda + phi), where x'=x*cos(theta)+y*sin(theta), "
        "y'=-x*sin(theta)+y*cos(theta). In CNNs, the receptive field "
        "of a unit grows with depth: RF = RF_prev + (kernel-1)*stride."
    ),
    example=(
        "CNN: 3 conv layers, kernel=3, stride=1 each. "
        "Layer 1 RF = 3. Layer 2 RF = 3+(3-1)*1 = 5. "
        "Layer 3 RF = 5+(3-1)*1 = 7 pixels."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Receptive field', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Receptive_field",
    prerequisites=["convolution"],
))

register_atom(Atom(
    atom_type="model",
    name="neural_coding",
    content=(
        "Neural coding refers to how neurons represent information. "
        "Rate coding: information is in the average firing rate. "
        "Temporal coding: information is in the precise spike timing. "
        "Population coding: information is distributed across many neurons. "
        "For population vectors (Georgopoulos): the movement direction "
        "is decoded as the vector sum of preferred directions weighted "
        "by firing rates: D = sum_i r_i * d_i / sum_i r_i."
    ),
    example=(
        "3 neurons with preferred directions [0, 120, 240] degrees "
        "and rates [10, 5, 3] Hz. Population vector: "
        "x = 10*cos(0)+5*cos(120)+3*cos(240) = 10-2.5-1.5 = 6.0. "
        "y = 10*sin(0)+5*sin(120)+3*sin(240) = 0+4.33-2.60 = 1.73. "
        "Direction = atan2(1.73, 6.0) = 16.1 degrees."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Neural coding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Neural_coding",
    prerequisites=["spike_rate"],
))

register_atom(Atom(
    atom_type="formula",
    name="synaptic_integration",
    content=(
        "Synaptic integration combines excitatory and inhibitory "
        "postsynaptic potentials (EPSPs and IPSPs) to determine whether "
        "a neuron fires. For a passive membrane with time constant "
        "tau_m = R_m*C_m: dV/dt = -(V - V_rest)/tau_m + I_syn/C_m. "
        "Temporal summation: two inputs arriving within tau_m add. "
        "Spatial summation: inputs at different locations add based on "
        "their electrotonic distance. Threshold: V > V_threshold triggers "
        "a spike."
    ),
    example=(
        "V_rest=-70mV, threshold=-55mV, tau_m=20ms. "
        "EPSP1=+8mV at t=0, EPSP2=+8mV at t=10ms. "
        "At t=10ms: V = -70+8*exp(-10/20) = -70+8*0.607 = -65.1mV. "
        "After EPSP2: V = -65.1+8 = -57.1mV. Still below -55mV, no spike."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Summation (neurophysiology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Summation_(neurophysiology)",
    prerequisites=["membrane_potential"],
))

register_atom(Atom(
    atom_type="formula",
    name="cable_equation",
    content=(
        "The cable equation describes how voltage attenuates along a "
        "passive neurite (dendrite or axon): "
        "lambda^2 * d^2V/dx^2 - tau_m * dV/dt = V - V_rest, "
        "where lambda = sqrt(r_m / r_i) is the length constant, "
        "r_m is membrane resistance per unit length, r_i is intracellular "
        "resistance per unit length, and tau_m = r_m * c_m. For steady "
        "state: V(x) = V_0 * exp(-x/lambda). The length constant "
        "lambda is typically 0.1-1 mm for dendrites."
    ),
    example=(
        "Dendrite: lambda=0.5mm. Voltage injection V_0=10mV at x=0. "
        "At x=0.5mm: V = 10*exp(-0.5/0.5) = 10*0.368 = 3.68 mV. "
        "At x=1.0mm: V = 10*exp(-1.0/0.5) = 10*0.135 = 1.35 mV."
    ),
    tier=6,
    domain="neuroscience",
    source="Wikipedia contributors, 'Cable theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cable_theory",
    prerequisites=["membrane_potential"],
))

register_atom(Atom(
    atom_type="model",
    name="fmri_bold",
    content=(
        "The Blood-Oxygen-Level-Dependent (BOLD) signal in fMRI reflects "
        "changes in deoxyhemoglobin concentration. Neural activity increases "
        "local blood flow (neurovascular coupling), oversupplying oxygen, "
        "which decreases deoxyhemoglobin and increases the T2* MRI signal. "
        "The hemodynamic response function (HRF) peaks at ~5-6 seconds "
        "after stimulus onset. The BOLD signal is modelled as the "
        "convolution of neural activity with the HRF: "
        "BOLD(t) = integral(activity(tau) * HRF(t-tau) dtau)."
    ),
    example=(
        "Canonical HRF: h(t) = (t/5.0)^5 * exp(-(t-5)/1.0) for t>0. "
        "Peak at t=5s. Stimulus at t=0 for 1s: BOLD peaks at ~5-6s, "
        "returns to baseline by ~15-20s. Amplitude ~ 1-5% signal change."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Blood-oxygen-level-dependent imaging', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Blood-oxygen-level-dependent_imaging",
    prerequisites=["convolution"],
))

register_atom(Atom(
    atom_type="formula",
    name="eeg_frequency",
    content=(
        "EEG (electroencephalography) records electrical activity from "
        "the scalp. Signals are decomposed into frequency bands: "
        "delta (0.5-4 Hz, deep sleep), theta (4-8 Hz, drowsiness, "
        "memory), alpha (8-13 Hz, relaxed wakefulness, eyes closed), "
        "beta (13-30 Hz, active thinking), gamma (30-100+ Hz, "
        "perception, consciousness). Power spectral analysis uses "
        "the Fourier transform to compute the power in each band: "
        "P_band = integral_{f1}^{f2} |X(f)|^2 df."
    ),
    example=(
        "EEG signal sampled at 256 Hz for 2 seconds (512 samples). "
        "FFT gives frequency resolution df = 256/512 = 0.5 Hz. "
        "Alpha power (8-13 Hz): sum |X(f)|^2 for bins 16-26. "
        "If |X(10Hz)|^2 = 50 uV^2/Hz (dominant), total alpha "
        "power ~ 250 uV^2."
    ),
    tier=5,
    domain="neuroscience",
    source="Wikipedia contributors, 'Electroencephalography', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electroencephalography",
    prerequisites=["dft_compute"],
))
