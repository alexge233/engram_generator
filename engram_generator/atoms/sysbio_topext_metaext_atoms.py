"""Knowledge atoms for systems biology, topology extensions, and meta-reasoning T10 extensions."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Systems Biology ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="hill_function",
    content=(
        "The Hill equation describes the fraction of a macromolecule "
        "saturated by a ligand as a function of ligand concentration: "
        "f = [L]^n / (K_d^n + [L]^n), where [L] is ligand concentration, "
        "K_d is the dissociation constant, and n is the Hill coefficient "
        "indicating cooperativity."
    ),
    example=(
        "Given [L]=10, K_d=5, n=2: "
        "f = 10^2 / (5^2 + 10^2) = 100 / (25 + 100) = 100/125 = 0.8"
    ),
    tier=5,
    domain="systems_biology",
    source="Wikipedia contributors, 'Hill equation (biochemistry)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)",
    prerequisites=["exponentiation", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="gene_regulation",
    content=(
        "Gene regulation models describe how transcription factor "
        "concentration affects gene expression. A simple activation model: "
        "expression = V_max * [TF]^n / (K^n + [TF]^n), where V_max is "
        "maximum expression rate, [TF] is transcription factor concentration, "
        "K is the half-maximal concentration, and n is cooperativity."
    ),
    example=(
        "Given V_max=100, [TF]=8, K=4, n=2: "
        "expression = 100 * 64 / (16 + 64) = 6400/80 = 80"
    ),
    tier=6,
    domain="systems_biology",
    source="Wikipedia contributors, 'Regulation of gene expression', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Regulation_of_gene_expression",
    prerequisites=["hill_function"],
))

register_atom(Atom(
    atom_type="formula",
    name="metabolic_flux",
    content=(
        "Metabolic flux analysis determines the rates of metabolic reactions "
        "in a network. At steady state, S * v = 0, where S is the "
        "stoichiometric matrix and v is the flux vector. For a simple "
        "linear pathway A -> B -> C with fluxes v1 and v2: v1 = v2 at "
        "steady state."
    ),
    example=(
        "Given pathway A->B->C with v1=5 mmol/h: "
        "at steady state v2 = v1 = 5 mmol/h"
    ),
    tier=5,
    domain="systems_biology",
    source="Wikipedia contributors, 'Flux balance analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Flux_balance_analysis",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="toggle_switch",
    content=(
        "A genetic toggle switch consists of two mutually repressing genes. "
        "The dynamics are: du/dt = alpha_1/(1 + v^beta) - u and "
        "dv/dt = alpha_2/(1 + u^gamma) - v, where u, v are protein "
        "concentrations, alpha are production rates, and beta, gamma "
        "are Hill coefficients for repression."
    ),
    example=(
        "Given alpha_1=10, alpha_2=10, beta=2, gamma=2, at steady state u=v: "
        "u = 10/(1+u^2) - u = 0 => u(1+u^2) = 10 => u ~ 1.85"
    ),
    tier=6,
    domain="systems_biology",
    source="Wikipedia contributors, 'Genetic toggle switch', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Toggle_switch_(genetics)",
    prerequisites=["hill_function", "gene_regulation"],
))

register_atom(Atom(
    atom_type="formula",
    name="oscillator_repressilator",
    content=(
        "The repressilator is a synthetic genetic oscillator consisting of "
        "three genes in a ring of mutual repression: A represses B, B "
        "represses C, C represses A. Oscillation occurs when the Hill "
        "coefficient n > 1 and the ratio alpha/K is sufficiently large."
    ),
    example=(
        "Given 3-gene ring with alpha=100, K=1, n=2, degradation=1: "
        "system oscillates with period ~ 2*pi/sqrt(3) * tau where "
        "tau is the characteristic timescale"
    ),
    tier=6,
    domain="systems_biology",
    source="Wikipedia contributors, 'Repressilator', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Repressilator",
    prerequisites=["toggle_switch"],
))

register_atom(Atom(
    atom_type="formula",
    name="growth_rate_dilution",
    content=(
        "In a chemostat or growing cell, protein concentration is affected "
        "by dilution due to growth. The steady-state concentration is "
        "p = alpha / (gamma + mu), where alpha is the production rate, "
        "gamma is the degradation rate, and mu is the growth rate (dilution)."
    ),
    example=(
        "Given alpha=10 proteins/min, gamma=0.1/min, mu=0.02/min: "
        "p = 10 / (0.1 + 0.02) = 10/0.12 = 83.33 proteins"
    ),
    tier=5,
    domain="systems_biology",
    source="Wikipedia contributors, 'Chemostat', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Chemostat",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="flux_balance",
    content=(
        "Flux Balance Analysis (FBA) finds the optimal flux distribution "
        "in a metabolic network by solving: maximise c^T * v subject to "
        "S * v = 0 and v_min <= v <= v_max, where S is the stoichiometric "
        "matrix, v is the flux vector, and c is the objective function "
        "(typically biomass production)."
    ),
    example=(
        "Given S = [[-1,0],[1,-1],[0,1]], c = [0,0,1], v_max=[10,10,10]: "
        "optimal v = [10, 10, 10], max biomass flux = 10"
    ),
    tier=6,
    domain="systems_biology",
    source="Wikipedia contributors, 'Flux balance analysis', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Flux_balance_analysis",
    prerequisites=["linear_program", "metabolic_flux"],
))

register_atom(Atom(
    atom_type="formula",
    name="dose_response_hill",
    content=(
        "The dose-response curve relates drug concentration to biological "
        "effect using the Hill equation: E = E_max * [D]^n / (EC50^n + [D]^n), "
        "where E_max is maximum effect, [D] is drug concentration, EC50 is "
        "the concentration producing 50% effect, and n is the Hill slope."
    ),
    example=(
        "Given E_max=100%, [D]=20uM, EC50=10uM, n=1: "
        "E = 100 * 20 / (10 + 20) = 2000/30 = 66.67%"
    ),
    tier=5,
    domain="systems_biology",
    source="Wikipedia contributors, 'Dose-response relationship', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Dose%E2%80%93response_relationship",
    prerequisites=["hill_function"],
))

# ── Topology Extensions ─────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="knot_invariant",
    content=(
        "A knot invariant is a quantity defined for each knot that is the "
        "same for equivalent knots. The crossing number is the minimum "
        "number of crossings in any diagram. The Jones polynomial V(t) is "
        "a Laurent polynomial invariant. The unknot has V(t) = 1, the "
        "trefoil has V(t) = -t^{-4} + t^{-3} + t^{-1}."
    ),
    example=(
        "Trefoil knot 3_1: crossing number = 3, "
        "Jones polynomial V(t) = -t^{-4} + t^{-3} + t^{-1}"
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Knot invariant', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Knot_invariant",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="theorem",
    name="fundamental_group",
    content=(
        "The fundamental group pi_1(X, x_0) of a topological space X at "
        "basepoint x_0 consists of homotopy classes of loops based at x_0. "
        "pi_1(S^1) = Z (integers), pi_1(S^n) = 0 for n >= 2, "
        "pi_1(T^2) = Z x Z (torus), pi_1(RP^2) = Z/2Z."
    ),
    example=(
        "Circle S^1: pi_1(S^1) = Z. A loop winding twice around "
        "represents the element 2 in Z."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Fundamental group', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Fundamental_group",
    prerequisites=["open_closed_sets", "continuity_topological"],
))

register_atom(Atom(
    atom_type="definition",
    name="covering_space",
    content=(
        "A covering space of a topological space X is a space C together "
        "with a continuous surjective map p: C -> X such that every point "
        "in X has a neighbourhood U whose preimage p^{-1}(U) is a disjoint "
        "union of open sets in C, each mapped homeomorphically onto U by p. "
        "The number of sheets equals |pi_1(X)| / |pi_1(C)|."
    ),
    example=(
        "R covers S^1 via p(t) = e^{2*pi*i*t}. "
        "This is an infinite-sheeted covering. "
        "|pi_1(S^1)| / |pi_1(R)| = |Z| / |0| = infinite."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Covering space', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Covering_space",
    prerequisites=["fundamental_group"],
))

register_atom(Atom(
    atom_type="definition",
    name="homotopy_equivalence",
    content=(
        "Two spaces X and Y are homotopy equivalent if there exist "
        "continuous maps f: X -> Y and g: Y -> X such that g . f is "
        "homotopic to id_X and f . g is homotopic to id_Y. Homotopy "
        "equivalent spaces have isomorphic fundamental groups and "
        "homology groups."
    ),
    example=(
        "R^n \\ {0} is homotopy equivalent to S^{n-1}. "
        "For n=2: R^2 \\ {0} ~ S^1, so pi_1 = Z."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Homotopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Homotopy",
    prerequisites=["fundamental_group"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="simplicial_homology",
    content=(
        "Simplicial homology computes the homology groups of a simplicial "
        "complex by forming chain groups C_n, boundary maps d_n: C_n -> C_{n-1}, "
        "and computing H_n = ker(d_n) / im(d_{n+1}). The Betti numbers "
        "b_n = rank(H_n) count the n-dimensional holes."
    ),
    example=(
        "Triangle (vertices 0,1,2 with edges 01,12,02, face 012): "
        "b_0 = 1 (connected), b_1 = 0 (no holes, face fills it), b_2 = 0"
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Simplicial homology', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Simplicial_homology",
    prerequisites=["chain_complex"],
))

register_atom(Atom(
    atom_type="definition",
    name="manifold_classify",
    content=(
        "Classification of manifolds assigns topological invariants to "
        "distinguish manifold types. For surfaces: genus g determines "
        "orientable surfaces (sphere g=0, torus g=1, double torus g=2). "
        "Euler characteristic chi = 2 - 2g for orientable, chi = 2 - g "
        "for non-orientable."
    ),
    example=(
        "Torus: genus g=1, chi = 2 - 2*1 = 0. "
        "Klein bottle: non-orientable, chi = 0."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Classification of manifolds', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Surface_(topology)#Classification_of_closed_surfaces",
    prerequisites=["euler_characteristic"],
))

register_atom(Atom(
    atom_type="definition",
    name="quotient_topology",
    content=(
        "The quotient topology on a set Y = X/~ (where ~ is an equivalence "
        "relation on X) is the finest topology making the projection map "
        "q: X -> X/~ continuous. A set U in X/~ is open iff q^{-1}(U) is "
        "open in X."
    ),
    example=(
        "[0,1]/~ where 0 ~ 1 gives S^1 (circle). "
        "[0,1]x[0,1] with (x,0) ~ (x,1) and (0,y) ~ (1,y) gives T^2 (torus)."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Quotient space (topology)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Quotient_space_(topology)",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="contractible_check",
    content=(
        "A topological space X is contractible if the identity map on X is "
        "homotopic to a constant map. Equivalently, X is homotopy equivalent "
        "to a point. Contractible spaces have trivial fundamental group and "
        "trivial homology in all positive dimensions."
    ),
    example=(
        "R^n is contractible: H(x,t) = (1-t)*x contracts to origin. "
        "S^1 is NOT contractible: pi_1(S^1) = Z is nontrivial."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Contractible space', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Contractible_space",
    prerequisites=["homotopy_equivalence"],
))

# ── Meta-Reasoning T10 Extensions ────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="architecture_search",
    content=(
        "Neural Architecture Search (NAS) automates the design of neural "
        "network architectures. Methods include random search, evolutionary "
        "algorithms, reinforcement learning, and differentiable approaches "
        "(DARTS). The search space includes layer types, connections, and "
        "hyperparameters. Evaluation uses accuracy, latency, and model size."
    ),
    example=(
        "Given candidates: ResNet (acc=92%, lat=5ms), EfficientNet "
        "(acc=94%, lat=8ms), MobileNet (acc=89%, lat=2ms). "
        "Pareto-optimal: EfficientNet (best acc), MobileNet (best lat)."
    ),
    tier=10,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Neural architecture search', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Neural_architecture_search",
    prerequisites=["attention_score_compute"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="curriculum_design",
    content=(
        "Curriculum learning orders training examples from easy to hard, "
        "following human learning principles. Key decisions: difficulty "
        "metric (loss, complexity, length), pacing function (linear, "
        "exponential, self-paced), and competence threshold for advancement."
    ),
    example=(
        "Given tasks at difficulties [1,3,5,7]: start training on d=1, "
        "when val_acc > 0.95, advance to d=3. Continue until all "
        "difficulties reached."
    ),
    tier=10,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Curriculum learning', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Curriculum_learning",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="definition",
    name="loss_landscape",
    content=(
        "The loss landscape is the surface defined by the loss function "
        "over parameter space. Properties include: local minima, saddle "
        "points, flatness (related to generalisation), and sharpness. "
        "Flat minima tend to generalise better (PAC-Bayes bound). "
        "Visualisation uses random 2D projections of the high-dimensional "
        "surface."
    ),
    example=(
        "Given f(w) = (w-1)^2 + 0.1*sin(10*w): global min at w~1, "
        "local min near w~0.7 and w~1.3 due to sinusoidal perturbation."
    ),
    tier=10,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Loss function', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Loss_function",
    prerequisites=["gradient"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="transfer_learning_strategy",
    content=(
        "Transfer learning reuses a model trained on one task for a "
        "different but related task. Strategies: feature extraction "
        "(freeze pretrained layers, train new head), fine-tuning (unfreeze "
        "some/all layers with small lr), domain adaptation (align source "
        "and target distributions)."
    ),
    example=(
        "ImageNet-pretrained ResNet50 for medical imaging: "
        "freeze conv layers, replace FC head with 2-class output, "
        "train head for 10 epochs at lr=1e-3, then fine-tune all "
        "layers at lr=1e-5."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Transfer learning', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Transfer_learning",
    prerequisites=["attention_score_compute"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="experiment_design_ml",
    content=(
        "ML experiment design involves choosing: independent variables "
        "(hyperparameters, architecture), dependent variables (metrics), "
        "controls (baselines, ablations), and statistical methodology "
        "(cross-validation, significance tests). Key principles: "
        "matched parameters for fair comparison, held-out test sets, "
        "multiple random seeds."
    ),
    example=(
        "Compare model A (510K params) vs B (514K params): "
        "match parameter count, same train/val/test split, "
        "5 random seeds, report mean +/- std, paired t-test for significance."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Design of experiments', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Design_of_experiments",
    prerequisites=["hypothesis_test"],
))

register_atom(Atom(
    atom_type="definition",
    name="proof_complexity",
    content=(
        "Proof complexity studies the lengths of proofs in formal systems. "
        "A proof system is polynomially bounded if every tautology has a "
        "polynomial-length proof. Resolution proofs for pigeonhole "
        "principle require exponential length. The Cook-Reckhow definition "
        "connects proof complexity to the P vs NP problem."
    ),
    example=(
        "Pigeonhole PHP^{n+1}_n in resolution: "
        "requires 2^{Omega(n)} clauses to refute. "
        "In extended Frege, polynomial-length proof exists."
    ),
    tier=8,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Proof complexity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Proof_complexity",
    prerequisites=["resolution_refutation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="debugging_strategy",
    content=(
        "Systematic debugging strategies for ML models include: "
        "1) Overfit a single batch (verify learning capacity), "
        "2) Gradient checking (numerical vs analytical), "
        "3) Ablation studies (remove components one at a time), "
        "4) Learning curve analysis (train vs val loss over time), "
        "5) Activation/gradient statistics (dead neurons, exploding gradients)."
    ),
    example=(
        "Model not learning: Step 1: overfit 1 batch -> loss stays high -> "
        "check lr (too high: oscillating, too low: flat). "
        "Reduce lr from 1e-2 to 1e-4 -> loss decreases -> lr was the issue."
    ),
    tier=8,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Debugging', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Debugging",
    prerequisites=["gradient"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="benchmark_design",
    content=(
        "Benchmark design for ML evaluation requires: representative task "
        "distribution, difficulty stratification, held-out test sets with "
        "no leakage, standardised evaluation metrics, and baseline "
        "comparisons. Good benchmarks measure generalisation, not "
        "memorisation, by including out-of-distribution test cases."
    ),
    example=(
        "Arithmetic benchmark: 5 task types x 8 difficulty levels, "
        "100 samples per combo = 4000 test samples. "
        "OOS test: difficulty 7-8 (never seen in training). "
        "Metric: exact match accuracy per difficulty."
    ),
    tier=9,
    domain="meta_reasoning",
    source="Wikipedia contributors, 'Benchmark (computing)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Benchmark_(computing)",
    prerequisites=["experiment_design_ml"],
))
